"""UCL Phase 3: read licensed frozen supplemental evidence without canonical output.

Raw Wikipedia revision JSON and decoded-wikitext locators remain separate. No live
requests, shared schema/model changes or edits to earlier inventory artifacts.
"""
from collections import Counter, defaultdict
import argparse
import csv
from datetime import date
import hashlib
import html
import json
import io
from pathlib import Path
import re
import unicodedata

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'data/private/europe/champions_league'
PHASE=BASE/'phase3'


def sha(raw):return hashlib.sha256(raw).hexdigest()
def enc(value):return (json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()


def template_end(text,start):
    depth=0;i=start
    while i<len(text)-1:
        if text[i:i+2]=='{{':depth+=1;i+=2
        elif text[i:i+2]=='}}':
            depth-=1;i+=2
            if depth==0:return i
        else:i+=1
    raise ValueError('Unbalanced evidence template')


def parts(text):
    """Split top-level template arguments without losing nested templates/links."""
    result=[];begin=0;i=0;braces=links=0
    while i<len(text):
        token=text[i:i+2]
        if token=='{{':braces+=1;i+=2
        elif token=='}}':braces-=1;i+=2
        elif token=='[[':links+=1;i+=2
        elif token==']]':links-=1;i+=2
        elif text[i]=='|' and braces==links==0:result.append(text[begin:i]);begin=i+1;i+=1
        else:i+=1
    result.append(text[begin:]);return result


def fields(block):
    out={}
    for arg in parts(block[2:-2])[1:]:
        if '=' in arg:
            key,value=arg.split('=',1);key=key.strip().lower()
            if key in out:raise ValueError('Duplicate named evidence field: '+key)
            out[key]=value.strip()
    return out


def plain(text):
    text=re.sub(r'<ref\b[^>]*>.*?</ref>|<ref\b[^>]*/>', '',text,flags=re.S|re.I)
    text=re.sub(r'<!--.*?-->', '',text,flags=re.S)
    # Footnote templates can contain linked teams and scores. Remove the whole
    # balanced annotation before reading the display name, retaining raw_fields.
    while (note:=re.search(r'\{\{\s*(?:refn|efn|sfn|sfnm|harvnb)\s*\|',text,re.I)):
        end=template_end(text,note.start());text=text[:note.start()]+text[end:]
    text=re.sub(r'\[\[([^\[\]]+)\]\]',lambda m:m[1].split('|')[-1],text)
    text=re.sub(r'\{\{(?:fbaicon|flagicon|flag)\|[^{}]*\}\}','',text,flags=re.I)
    text=re.sub(r'<[^>]+>','',text)
    return html.unescape(' '.join(text.split())).strip()


def goals(text):
    times=[];raw=[]
    for m in re.finditer(r'\{\{\s*goal\s*\|',text,re.I):
        end=template_end(text,m.start());block=text[m.start():end];args=parts(block[2:-2])[1:];raw.append(block)
        for arg in args:
            a=arg.strip()
            if re.fullmatch(r'\d+(?:\+\d+)?',a):times.append(a)
    return times,raw


def stage_at(text,offset):
    stage=None;path=None;sub=None
    for m in re.finditer(r'^(={2,5})\s*(.*?)\s*\1\s*$',text[:offset],re.M):
        level=len(m[1]);title=m[2].strip()
        if level==2:
            stage=title;path=None;sub=None
        else:
            sub=title
            if 'Champions Path' in title:path='CHAMPIONS'
            elif 'League Path' in title:path='LEAGUE'
    mapping={'First qualifying round':'QUALIFYING_ROUND_1','Second qualifying round':'QUALIFYING_ROUND_2',
             'Third qualifying round':'QUALIFYING_ROUND_3','Play-off round':'QUALIFYING_PLAYOFF'}
    normalized=mapping.get(stage)
    if stage=='Preliminary round':normalized='PRELIMINARY_FINAL' if sub=='Final round' else 'PRELIMINARY_SEMIFINAL' if sub=='Semi-final round' else 'PRELIMINARY'
    return stage,sub,path,normalized


def score_components(f):
    token=f.get('score','');clean=plain(token);pair=re.search(r'(\d+)\s*[–−-]\s*(\d+)',clean)
    reported=[int(pair[1]),int(pair[2])] if pair else None
    et=bool(re.search(r'a\.?e\.?t\.?|after extra time|extra ?time',token,re.I))
    # Some source boxes use a separate aet flag rather than spelling it in score.
    et=et or f.get('aet','').lower() in ('yes','y','1')
    h,hr=goals(f.get('goals1',''));a,ar=goals(f.get('goals2',''))
    complete=reported is not None and [len(h),len(a)]==reported
    normal=None;basis=None;issues=[]
    if re.search(r'walkover|w/o|awarded|forfeit',clean+' '+f.get('scorenote',''),re.I):issues.append('AWARD_OR_WALKOVER_SCORE_CONTEXT')
    elif reported is not None:
        if not et:normal=reported;basis='EXPLICIT_ORDINARY_MATCH_SCORE'
        elif complete and sum(reported)>0:
            normal=[sum(int(t.split('+')[0])<=90 for t in times) for times in (h,a)]
            basis='COMPLETE_EXPLICIT_GOAL_CHRONOLOGY;STOPPAGE_TIME_BASE_90_INCLUDED'
        else:issues.append('REGULATION_PERIOD_REQUIRES_TARGETED_EVIDENCE')
    else:issues.append('NO_NUMERIC_MATCH_SCORE')
    pens=[]
    for key in ('penaltyscore','penalties','penaltyscore1','penaltyscore2'):
        if f.get(key):pens.append({'field':key,'raw':f[key]})
    if f.get('penalties1') or f.get('penalties2'):
        pens += [{'field':k,'raw':f.get(k,'')} for k in ('penalties1','penalties2')]
    shootout_token=plain(f.get('penaltyscore',''));sp=re.fullmatch(r'(\d+)\s*[–−-]\s*(\d+)',shootout_token)
    return {'reported_score':reported,'regulation_time':normal,'after_extra_time':reported if et else None,
            'shootout':[int(sp[1]),int(sp[2])] if sp else None,
            'shootout_fields':pens,'goal_minutes_home':h,'goal_minutes_away':a,'goal_templates_home':hr,'goal_templates_away':ar,
            'goal_chronology_complete':complete,'score_period_basis':basis,'extra_time_explicit':et,'issues':issues}


def parse_wikipedia(raw,source):
    if len(raw.splitlines())!=1:raise ValueError('Revision JSON physical-line convention differs')
    data=json.loads(raw);page=data['query']['pages'][0];revision=page['revisions'][0];text=revision['slots']['main']['content'];rows=[]
    if revision['revid']!=source['revision']:raise ValueError('Revision identity differs')
    if sha(raw)!=source['sha256']:raise ValueError('Supplement original changed')
    for m in re.finditer(r'\{\{\s*football[ _]box(?:[ _]collapsible)?\s*(?:\n|\|)',text,re.I):
        end=template_end(text,m.start());block=text[m.start():end];f=fields(block)
        if 'team1' not in f or 'team2' not in f:raise ValueError('Incomplete fixture identity')
        dm=re.search(r'\{\{\s*(?:start date|start date and age)\s*\|\s*(\d{4})\s*\|\s*(\d{1,2})\s*\|\s*(\d{1,2})',f.get('date',''),re.I)
        when=date(*map(int,dm.groups())).isoformat() if dm else None
        if when is None:
            ds=plain(f.get('date',''));d=re.search(r'(\d{1,2}) ([A-Z][a-z]+) (\d{4})',ds)
            if d:
                from datetime import datetime
                when=datetime.strptime(d[0],'%d %B %Y').date().isoformat()
        st,sub,path,stage=stage_at(text,m.start());first=text.count('\n',0,m.start())+1;last=text.count('\n',0,end)+1
        row={'source_observation_id':sha(enc([source['sha256'],m.start(),end])), 'source':source['path'],
             'source_sha256':source['sha256'],'revision':revision['revid'],'page_title':page['title'],'season':source['season'],
             'json_pointer':'/query/pages/0/revisions/0/slots/main/content','physical_json_line':1,
             'decoded_wikitext_start':m.start(),'decoded_wikitext_end':end,'decoded_line':first,'decoded_end_line':last,
             'template_sha256':sha(block.encode()),'raw_fields':f,'date':when,'home':plain(f['team1']),'away':plain(f['team2']),
             'raw_home':f['team1'],'raw_away':f['team2'],'raw_stage':st,'raw_substage':sub,'path':path,'stage':stage,
             'venue':plain(f.get('stadium','')),'neutral_venue':None,'neutral_evidence':[],
             'periods':score_components(f),'permission':'CC BY-SA 4.0;Wikipedia contributors; preserve revision/page attribution'}
        rows.append(row)
    return rows,text


def parse_all_sources():
    indices=[PHASE/'wikipedia_cached_source_index.json'];out=[]
    for index in indices:
        if not index.exists():continue
        for source in json.loads(index.read_bytes()):
            if 'qualifying' not in source.get('title',''):continue
            rows,_=parse_wikipedia((PHASE/source['path']).read_bytes(),source)
            if any(r['stage'] is None for r in rows):raise ValueError('Unclassified qualifying evidence')
            out+=rows
    return out


def parse_curley(raw,source):
    """Explicit FT/HT/aet/pens columns; never substitute total/aggregate columns."""
    if sha(raw)!=source['sha256']:raise ValueError('Curley original digest differs')
    lines=raw.splitlines(keepends=True);reader=csv.DictReader(io.StringIO(raw.decode('utf-8')));rows=[];previous=1
    expected='Date Season round leg home visitor FT HT aet pens hgoal vgoal FTagg_home FTagg_visitor aethgoal aetvgoal tothgoal totvgoal totagg_home totagg_visitor tiewinner hcountry vcountry'.split()
    if reader.fieldnames!=expected:raise ValueError('Curley source columns differ')
    stages={'PrelimF':'PRELIMINARY','prelim':'PRELIMINARY','Q-1':'QUALIFYING_ROUND_1',
            'Q-2':'QUALIFYING_ROUND_2','Q-3':'QUALIFYING_ROUND_3','Q-PO':'QUALIFYING_PLAYOFF'}
    def pair(s):
        value=s.strip()
        return list(map(int,value.split('-'))) if re.fullmatch(r'\d+-\d+',value) else None
    for f in reader:
        if None in f or any(v is None for v in f.values()):raise ValueError('Curley source width differs')
        first=previous+1;last=reader.line_num;previous=last
        year=int(f['Season'])
        if not 1992<=year<=2025:continue
        physical=b''.join(lines[first-1:last])
        rows.append({'source_observation_id':sha(enc([source['sha256'],first,last])),
                     'source':source['path'],'source_sha256':source['sha256'],'physical_line':first,'end_line':last,
                     'physical_sha256':sha(physical),'raw_fields':f,'season':f'{year}/{year+1}','date':f['Date'],
                     'home':f['home'],'away':f['visitor'],'home_association':f['hcountry'],'away_association':f['vcountry'],
                     'stage':stages.get(f['round'],f['round']),'scope':'QUALIFYING' if f['round'] in stages else 'MAIN',
                     'periods':{'regulation_time':pair(f['FT']),'half_time':pair(f['HT']),
                                'after_extra_time':pair(f['aet']),'shootout':pair(f['pens'])},
                     'permission':'James P. Curley; non-commercial attribution grant; upstream independence not established'})
    return rows


def display_key(s):
    text=unicodedata.normalize('NFKD',s.casefold()).encode('ascii','ignore').decode()
    return tuple(w for w in re.findall(r'[a-z0-9]+',text) if w not in {'fc','fk','afc','cf','sc','sk','ac','as','rsc','gnk','nk','if','ff','ik','a','s'})


def source_correspondences(left,right):
    """Season/source-bound label evidence, then fixture identity independent of score.

    Equal date/score signatures seed provisional label correspondences. They are
    not independent historical votes or global aliases. Final pairing ignores
    scores, thereby exposing disagreements rather than dropping them.
    """
    votes=defaultdict(Counter);proof=defaultdict(list);mapping={}
    targets={p[s] for p in left for s in ('home','away')}
    labels={r[s] for r in right for s in ('home','away')}
    for name in sorted(labels):
        exact={t for t in targets if display_key(t)==display_key(name)}
        if len(exact)==1:mapping[name]=next(iter(exact))
    buckets=defaultdict(list)
    for p in left:buckets[(p['date'],tuple(p['periods'].get('regulation_time') or []))].append(p)
    for r in right:
        candidates=buckets[(r['date'],tuple(r['periods'].get('regulation_time') or []))]
        if len(candidates)==1:
            p=candidates[0]
            for side in ('home','away'):
                votes[r[side]][p[side]]+=1;proof[(r[side],p[side])].append([p.get('observation_id',p.get('source_observation_id')),r['source_observation_id']])
    for name,count in sorted(votes.items()):
        if name not in mapping and len(count)==1:mapping[name]=next(iter(count))
    for _ in range(len(labels)+1):
        additions={}
        for r in right:
            for side,other in (('home','away'),('away','home')):
                if r[side] in mapping or r[other] not in mapping:continue
                candidates=[p for p in left if p['date']==r['date'] and p[other]==mapping[r[other]]]
                options={p[side] for p in candidates}
                if len(options)==1:additions[r[side]]=next(iter(options))
        if not additions:break
        mapping.update(additions)
    if len(mapping)!=len(set(mapping.values())):raise ValueError('Non-injective seasonal club correspondence')
    links=[];unlinked=[]
    for r in right:
        candidates=[p for p in left if (p['home'],p['away'])==(mapping.get(r['home']),mapping.get(r['away']))]
        if len(candidates)>1:candidates=[p for p in candidates if p['date']==r['date']]
        orientation='SAME'
        if not candidates and len(right)==1:
            candidates=[p for p in left if (p['home'],p['away'])==(mapping.get(r['away']),mapping.get(r['home'])) and p['date']==r['date']]
            orientation='REVERSED'
        if len(candidates)!=1:unlinked.append(r['source_observation_id']);continue
        p=candidates[0];rp=r['periods'].get('regulation_time');lp=p['periods'].get('regulation_time')
        links.append({'left':p.get('observation_id',p.get('source_observation_id')),'right':r['source_observation_id'],
                      'orientation':orientation,'date_equal':p['date']==r['date'],
                      'regulation_equal':None if rp is None or lp is None else lp==(rp if orientation=='SAME' else rp[::-1])})
    return {'mapping':[{'source_label':a,'target_label':b,'evidence_pairs':proof[(a,b)],
                        'status':'SOURCE_AND_SEASON_BOUND_CORRESPONDENCE;UPSTREAM_INDEPENDENCE_NOT_ESTABLISHED'} for a,b in sorted(mapping.items())],
            'links':links,'unlinked':unlinked}


def validate_rule(row,rule):
    if (row['source'],row['source_sha256'],row['date'],row['home'],row['away'])!=(rule['source'],rule['source_sha256'],rule['expected_date'],rule['expected_home'],rule['expected_away']):
        raise ValueError('Decision/source binding differs')


def apply_decisions(event, rules, facts):
    """Apply explicit derived changes, preserving raw fields and orientation."""
    allowed={'regulation_time','after_extra_time','half_time','observed_regulation_time',
             'administrative_result','football_date','completion_date','partial_played_score',
             'scheduled_dates','disposition','leg','replay','neutral_venue','venue',
             'historical_home','historical_away'}
    result=json.loads(json.dumps(event));result['applied_decisions']=[]
    for rule in rules:
        if rule['observation_id']!=event['primary_observation_id']:continue
        if set(rule['changes'])-allowed:raise ValueError('Unapproved derived field')
        if not rule['evidence_ids'] or any(e not in facts for e in rule['evidence_ids']):raise ValueError('Missing decision evidence')
        result.update(rule['changes'])
        if 'regulation_time' in rule['changes'] and 'observed_regulation_time' not in rule['changes']:
            result['observed_regulation_time']=rule['changes']['regulation_time']
        result['applied_decisions'].append(rule)
    if result['neutral_venue'] not in (None,0,1):raise ValueError('Invalid venue tri-state')
    admin=result.get('administrative_result')
    result['accepted_result']=admin if admin is not None and result['disposition']=='INCLUDE' else result['regulation_time'] if result['disposition']=='INCLUDE' else None
    result['result_basis']='RETROSPECTIVE_PLAYED_ADMINISTRATIVE_EXCEPTION' if admin is not None and result['disposition']=='INCLUDE' else 'SUPPORTED_REGULATION' if result['disposition']=='INCLUDE' else None
    if result['disposition']=='INCLUDE' and (result['accepted_result'] is None or result['football_date'] is None):
        result['disposition']='HOLD OUT';result['accepted_result']=None;result['result_basis']=None
        result['hold_reason']='UNRESOLVED_EXACT_DATE_OR_SCORE_PERIOD'
    if result['disposition']=='NOT PLAYED' and (result['football_date'] is not None or result['regulation_time'] is not None):raise ValueError('No-kickoff event given played fields')
    result['outcome']=None if result['accepted_result'] is None else ('1' if result['accepted_result'][0]>result['accepted_result'][1] else '2' if result['accepted_result'][0]<result['accepted_result'][1] else 'X')
    return result


def build():
    from scripts.inventory_uefa_champions_league import primary
    original=json.loads((BASE/'phase2/validated/source_inventory.json').read_bytes())['observations']
    frozen=json.loads((BASE/'phase2/validated/event_inventory.json').read_bytes())['events']
    if len(original)!=6578 or len(frozen)!=5953:raise ValueError('Accepted Phase 2 population differs')
    p2manifest=json.loads((BASE/'phase2/acquisition_manifest.json').read_bytes())
    for item in p2manifest['originals']:
        if sha((BASE/item['path']).read_bytes())!=item['sha256']:raise ValueError('Frozen Phase 2 original changed')
    old={r['observation_id']:r for r in original};selected=[r for r in original if primary(r)]
    evidence=json.loads((PHASE/'adjudication_evidence.json').read_bytes());facts=evidence['evidence']
    wiki=parse_all_sources();curley_file=PHASE/'originals/engsoccerdata/champs.csv'
    cr=json.loads(curley_file.with_name(curley_file.name+'.provenance.json').read_bytes())
    if sha(curley_file.read_bytes())!=cr['sha256']:raise ValueError('Curley original changed')
    curley=parse_curley(curley_file.read_bytes(),{'path':str(curley_file.relative_to(PHASE)),'sha256':cr['sha256']})
    supplement={r['source_observation_id']:r for r in wiki+curley};correspondences=[];new=[]
    auxiliary= json.loads((PHASE/'auxiliary_correspondence_evidence.json').read_bytes())['decisions']
    for publisher,rows in [('engsoccerdata',curley),('wikipedia',wiki)]:
        for season in sorted({r['season'] for r in rows}):
            rr=[r for r in rows if r['season']==season]
            ll=[r for r in selected if r['season']==season and (r['scope']=='QUALIFYING' if publisher=='wikipedia' else True)]
            if not ll:
                if publisher!='wikipedia' or not '2016/2017'<=season<='2023/2024':raise ValueError('Unexpected supplemental scope')
                new+=rr;continue
            report=source_correspondences(ll,rr)
            # Explicit private decisions can contain an isolated auxiliary date
            # defect without changing any original or creating an extra event.
            for d in auxiliary:
                if d['season']!=season or d['auxiliary_observation_id'] not in report['unlinked']:continue
                r=supplement[d['auxiliary_observation_id']];p=old[d['primary_observation_id']]
                if (r['source_sha256'],r['date'],r['home'],r['away'],r['raw_fields'].get('round'))!=(d['auxiliary_source_sha256'],d['expected_auxiliary_date'],d['expected_auxiliary_home'],d['expected_auxiliary_away'],d['expected_auxiliary_round']):raise ValueError('Auxiliary decision binding differs')
                if (p['source_sha256'],p['date'],p['stage'])!=(d['primary_source_sha256'],d['expected_primary_date'],d['expected_primary_stage']):raise ValueError('Auxiliary primary binding differs')
                report['links'].append({'left':p['observation_id'],'right':r['source_observation_id'],'orientation':'SAME','date_equal':p['date']==r['date'],'regulation_equal':p['periods']['regulation_time']==r['periods']['regulation_time'],'quarantine':'RAW_AUXILIARY_DATE;NOT_AN_ADDITIONAL_EVENT','evidence_file':'auxiliary_correspondence_evidence.json'})
                report['unlinked'].remove(r['source_observation_id'])
            if report['unlinked']:raise ValueError('Uncontained supplemental correspondence')
            correspondences.append({'publisher':publisher,'season':season,**report})
    events=[];membership={}
    for e in frozen:
        candidates=[old[i] for i in e['observations'] if primary(old[i])]
        if len(candidates)!=1:raise ValueError('Frozen primary selection differs')
        p=candidates[0];i=p['observation_id'];periods=p['periods']
        event={'event_id':e['event_id'],'population':'FROZEN_PHASE2','primary_observation_id':i,
               'observations':list(e['observations']),'season':p['season'],'scope':p['scope'],'stage':p['stage'],
               'group':p['group'],'path':p.get('source_path_label'),'leg':p.get('source_leg'),'replay':p['replay'],
               'first_listed':p['home'],'second_listed':p['away'],'source_date':p['date'],'football_date':p['date'],
               'regulation_time':periods['regulation_time'],'observed_regulation_time':periods['regulation_time'],
               'after_extra_time':periods['after_extra_time'],'shootout':periods['shootout'],'half_time':periods['half_time'],
               'aggregate':periods['aggregate'],'source_periods':periods,'neutral_venue':None,'venue':None,'disposition':'INCLUDE',
               'source_evidence':[{'observation_id':i,'source':p['source'],'source_sha256':p['source_sha256'],'line':p['line'],'end_line':p['end_line']}],
               'frozen_review_issues':e['issues'],'ordinary_basis':'OFFICIAL_STAGE;SOURCE_EXPLICIT_DATE_AND_REGULATION;NO_IDENTIFIED_MATERIAL_EXCEPTION'}
        events.append(event)
        for oid in e['observations']:membership[oid]=e['event_id']
    for p in new:
        i=p['source_observation_id'];event_id=sha(enc([i]));periods=p['periods']
        event={'event_id':event_id,'population':'RECOVERED_QUALIFYING','primary_observation_id':i,'observations':[i],
               'season':p['season'],'scope':'QUALIFYING','stage':p['stage'],'group':None,'path':p['path'],'leg':None,'replay':False,
               'first_listed':p['home'],'second_listed':p['away'],'source_date':p['date'],'football_date':p['date'],
               'regulation_time':periods['regulation_time'],'observed_regulation_time':periods['regulation_time'],
               'after_extra_time':periods['after_extra_time'],'shootout':periods['shootout'],'half_time':None,'aggregate':None,'source_periods':periods,
               'neutral_venue':None,'venue':p['venue'],'disposition':'INCLUDE','source_evidence':[{'observation_id':i,'source':p['source'],'source_sha256':p['source_sha256'],'json_pointer':p['json_pointer'],'physical_json_line':1,'decoded_line':p['decoded_line'],'decoded_end_line':p['decoded_end_line'],'decoded_wikitext_start':p['decoded_wikitext_start'],'decoded_wikitext_end':p['decoded_wikitext_end'],'template_sha256':p['template_sha256']}],
               'frozen_review_issues':[],'ordinary_basis':periods['score_period_basis']}
        events.append(event);membership[i]=event_id
    byid={e['event_id']:e for e in events}
    for report in correspondences:
        for link in report['links']:
            eid=membership[link['left']];byid[eid]['observations'].append(link['right']);membership[link['right']]=eid
    if len(new)!=692 or len(membership)!=len(original)+len(supplement):raise ValueError('Population not conserved')
    for rule in evidence['rules']:
        p=old.get(rule['observation_id'],supplement.get(rule['observation_id']))
        if not p:raise ValueError('Decision observation missing')
        validate_rule(p,rule)
    events=[apply_decisions(e,evidence['rules'],facts) for e in events]
    if sum(len(e['applied_decisions']) for e in events)!=len(evidence['rules']):raise ValueError('A decision was not applied exactly once')
    # Resolved group letters use a separately researched membership list, not file order.
    groups=evidence['group_2023_labels'];allclubs=[n for ns in groups.values() for n in ns]
    if len(allclubs)!=32 or len(set(allclubs))!=32:raise ValueError('Group evidence population differs')
    for e in events:
        if e['season']=='2023/2024' and e['stage']=='FIRST_GROUP':
            candidates=[g for g,ns in groups.items() if e['first_listed'] in ns and e['second_listed'] in ns]
            if len(candidates)!=1:raise ValueError('Researched group membership fails source-bound club identity')
            e['group']=candidates[0];e['group_evidence']=evidence['group_evidence']
    # Additional historical attempts have factual-note provenance, separate from
    # downloaded fixture observations and the accepted nominal-format population.
    context_events=[]
    for c in evidence['additional_nonstanding_contexts']:
        context_events.append({**c,'event_id':sha(enc(['NONSTANDING_CONTEXT',c])),
                               'source_type':'FACTUAL_RESEARCH_NOTE;NOT_DOWNLOADED_FIXTURE_ROW',
                               'evidence_file_sha256':sha((PHASE/'adjudication_evidence.json').read_bytes()),
                               'accepted_result':None,'neutral_venue':None,'outcome':None})
    events.sort(key=lambda e:(e['season'],e['football_date'] or e['source_date'],e['event_id']))
    # Audit-only arithmetic never fills a missing regulation score. Retain the
    # publisher aggregate separately even if it disagrees with the supported legs.
    aggregates=[]
    for e in events:
        e['aggregate_basis']='SOURCE_REPORTED;NOT_REPLACED_BY_CALCULATION'
        if e['stage'] in ('FIRST_GROUP','SECOND_GROUP','LEAGUE_PHASE'):continue
        others=[z for z in events if z['season']==e['season'] and z['stage']==e['stage'] and z['first_listed']==e['second_listed'] and z['second_listed']==e['first_listed'] and z['football_date'] and e['football_date'] and z['football_date']<e['football_date'] and not e['replay']]
        if len(others)!=1 or e['disposition']!='INCLUDE' or others[0]['disposition']!='INCLUDE':continue
        first=others[0];a=first.get('administrative_result') or first['after_extra_time'] or first['regulation_time'];b=e.get('administrative_result') or e['after_extra_time'] or e['regulation_time']
        if a is None or b is None:continue
        value=[a[1]+b[0],a[0]+b[1]]
        e['calculated_standing_tie_aggregate']=value;e['aggregate_calculation_observations']=[first['primary_observation_id'],e['primary_observation_id']]
        if e['aggregate'] is not None and e['aggregate']!=value:
            aggregates.append({'event_id':e['event_id'],'reported_aggregate':e['aggregate'],'calculated_standing_tie_aggregate':value,'policy':'REPORTED_VALUE_RETAINED;AUDIT_ARITHMETIC_ONLY;NEVER_A_REGULATION_SCORE_INFERENCE'})
    expected=[8,20,16,16,16,62,64,78,80,80,80,80,80,84,82,88,88,88,88,88,88,88,90,92,92,94,91,91,53,93,89,89,90,92]
    matrix=[]
    for y,qexpected in zip(range(1992,2026),expected):
        season=f'{y}/{y+1}';ee=[e for e in events if e['season']==season];q=[e for e in ee if e['scope']=='QUALIFYING'];m=[e for e in ee if e['scope']=='MAIN']
        if len(q)!=qexpected:raise ValueError('Qualifying expected/observed mismatch')
        duplicates=Counter((e['football_date'],e['first_listed'],e['second_listed']) for e in ee if e['disposition']=='INCLUDE')
        if max(duplicates.values(),default=0)>1:raise ValueError('Duplicate eligible fixture')
        matrix.append({'season':season,'main_descriptions':len(m),'qualifying_expected_descriptions':qexpected,'qualifying_observed_descriptions':len(q),
                       'qualifying_dispositions':dict(sorted(Counter(e['disposition'] for e in q).items())),
                       'main_dispositions':dict(sorted(Counter(e['disposition'] for e in m).items())),
                       'stages':dict(sorted(Counter(e['stage'] for e in ee).items())),
                       'new_qualifying_descriptions':sum(e['population']=='RECOVERED_QUALIFYING' for e in ee),
                       'identified_missing_standing_fixtures':[],'unverified_historical_universe_caveat':True})
    review=json.loads((BASE/'phase2/validated/unresolved_issues.json').read_bytes())
    rawlinks=[link for r in correspondences for link in r['links']]
    discrepancy={'source_bound_derived_rules':evidence['rules'],
                 'raw_supplemental_overlap_conflicts':[link for link in rawlinks if link['date_equal'] is False or link['regulation_equal'] is False],
                 'auxiliary_source_periods_remain_unfilled':[r['source_observation_id'] for r in wiki if r['periods']['regulation_time'] is None],
                 'quarantine_policy':'Raw conflicting/ambiguous observations stay intact. A supported event may INCLUDE using explicit evidence or a scoped rule; no silent alteration/discard of raw observations.',
                 'overlap_counts':{'links':len(rawlinks),'dates_equal':sum(l['date_equal'] for l in rawlinks),
                                   'regulation_comparable':sum(l['regulation_equal'] is not None for l in rawlinks),
                                   'regulation_equal':sum(l['regulation_equal'] is True for l in rawlinks)},
                 'remaining_event_holdouts':[e['event_id'] for e in events if e['disposition']=='HOLD OUT']}
    summary={'phase':3,'status':'CANDIDATE_FOR_OWNER_REVIEW','frozen_phase2_observations':6578,'frozen_phase2_events':5953,
             'supplemental_wikipedia_observations':len(wiki),'supplemental_curley_target_observations':len(curley),
             'total_fixture_observations':len(membership),'conditional_fixture_events':len(events),
             'new_qualifying_descriptions':len(new),'main_descriptions':sum(e['scope']=='MAIN' for e in events),
             'qualifying_descriptions':sum(e['scope']=='QUALIFYING' for e in events),
             'fixture_event_dispositions':dict(sorted(Counter(e['disposition'] for e in events).items())),
             'additional_nonstanding_context_events':len(context_events),
             'all_reviewed_event_dispositions':dict(sorted(Counter(e['disposition'] for e in events+context_events).items())),
             'target_seasons':len(matrix),'resolved_frozen_review_events':len(review['event_queue']),
             'resolved_frozen_contexts':len(review['contexts']),'explicit_derived_rules':len(evidence['rules']),
             'new_regulation_repairs_to_incorrect_primary_values':8,'retained_frozen_originals':41,
             'reported_aggregate_discrepancies':len(aggregates),
             'after_extra_time_events':sum(e['after_extra_time'] is not None for e in events),'shootout_events':sum(e['shootout'] is not None for e in events),
             'neutral_venue_counts':dict(sorted(Counter(str(e['neutral_venue']) for e in events).items())),
             'numeric_time_weights':'UNSPECIFIED;RECENT_FIRST','phase4_started':False}
    resolution=[{'event_id':q['event_id'],'issues':q['issues'],'disposition':next(e['disposition'] for e in events if e['event_id']==q['event_id']),
                 'decision_evidence':next([d['evidence_ids'] for d in e['applied_decisions']] for e in events if e['event_id']==q['event_id'])+
                    ([['LEG-LABELS-1992']] if 'SOURCE_LEG_LABEL_REVIEW' in q['issues'] else [])+
                    ([['OWNER_APPROVED_FIRST_LISTED_ORIENTATION_POLICY;FROZEN_EXPLICIT_PERIOD_COMPARISON']] if 'NEUTRAL_FINAL_SOURCE_ORIENTATION_DIFFERENCE' in q['issues'] else []),
                 'orientation':'FROZEN_PRIMARY_RETAINED;COMPARATOR_REVERSED_FOR_COMPARISON_ONLY'} for q in review['event_queue']]
    return {'supplemental_source_inventory.json':{'observations':wiki+curley},
            'source_correspondences.json':{'reports':correspondences,'source_independence':'NOT_ESTABLISHED;PUBLISHER_AGREEMENT_NOT_AN_INDEPENDENT_VOTE'},
            'decision_registry.json':{'fixture_events':events,'additional_nonstanding_context_events':context_events,'policy_evidence_sha256':sha((PHASE/'adjudication_evidence.json').read_bytes())},
            'coverage_assessment.json':{'seasons':matrix,'gap_seasons_before':list(range(2016,2024)),'identified_remaining_qualifying_gap_fixtures':[],
                                         'limits':'Format, tie and separate-publisher checks establish no identified standing gaps; not independent primary historical certification of every ordinary match.'},
            'review_resolution.json':{'events':resolution,'contexts':review['contexts'],'context_resolution':'Eight qualifying gaps filled;2023 group labels supported by separately researched draw membership'},
            'aggregate_discrepancies.json':{'observations':aggregates,'limits':'Calculated two-leg standing totals are private structural diagnostics, not silently repaired publisher aggregate fields.'},
            'discrepancy_registry.json':discrepancy,
            'summary.json':summary}


def run(output=PHASE/'final',check=False):
    output=Path(output).resolve()
    if output.is_relative_to(ROOT.resolve()) and not output.is_relative_to((ROOT/'data/private').resolve()):raise ValueError('Detailed evidence output must be private')
    artifacts=build()
    if not check:output.mkdir(parents=True,exist_ok=True)
    for name,value in artifacts.items():
        path=output/name;raw=enc(value)
        if check:
            if not path.exists() or path.read_bytes()!=raw:raise ValueError('Non-reproducible adjudication artifact: '+name)
        else:
            with path.open('xb') as f:f.write(raw)
    return artifacts['summary.json']


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,default=PHASE/'final');parser.add_argument('--check',action='store_true');args=parser.parse_args()
    print(json.dumps(run(args.output,args.check),indent=2))
