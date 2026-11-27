"""Independent offline UCL historical-decision verification, no production import.

Reads frozen CSV/TXT through the prior independent reader and independently
tokenizes licensed revision JSON. Match boxes reconcile to separate tie-summary
representations before comparing the produced candidate registry.
"""
from collections import Counter,defaultdict
import argparse
import csv
from datetime import date,datetime
import hashlib
import html
import io
import json
from pathlib import Path
import re
import unicodedata

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'data/private/europe/champions_league'
PHASE=BASE/'phase3'

def digest(b):return hashlib.sha256(b).hexdigest()
def wire(x):return (json.dumps(x,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode()
def read(p):return json.loads(p.read_bytes())
def require(x,message):
    if not x:raise ValueError(message)

def templates(text):
    stack=[];result=[]
    for m in re.finditer(r'\{\{|\}\}',text):
        if m[0]=='{{':stack.append(m.start())
        else:
            require(bool(stack),'Unbalanced closing template')
            start=stack.pop();name=re.split(r'[|\n]',text[start+2:m.start()],maxsplit=1)[0].strip().lower().replace('_',' ')
            if name in ('football box','football box collapsible','#invoke:sports series'):result.append((start,m.end(),name))
    require(not stack,'Unbalanced opening template')
    return sorted(result)

def arguments(block):
    s=block[2:-2];depth=links=0;cuts=[-1]
    for m in re.finditer(r'\{\{|\}\}|\[\[|\]\]|\|',s):
        tok=m[0]
        if tok=='{{':depth+=1
        elif tok=='}}':depth-=1
        elif tok=='[[':links+=1
        elif tok==']]':links-=1
        elif depth==links==0:cuts.append(m.start())
    cuts.append(len(s));return [s[a+1:b] for a,b in zip(cuts,cuts[1:])]

def tidy(value):
    value=re.sub(r'<!--.*?-->|<ref\b[^>]*>.*?</ref>|<ref\b[^>]*/>','',value,flags=re.S|re.I)
    # Strip balanced source footnotes separately from any team display text.
    while re.search(r'\{\{\s*(?:refn|efn|sfn|sfnm|harvnb)\s*\|',value,re.I):
        m=re.search(r'\{\{\s*(?:refn|efn|sfn|sfnm|harvnb)\s*\|',value,re.I);depth=0;end=None
        for t in re.finditer(r'\{\{|\}\}',value[m.start():]):
            depth+=1 if t[0]=='{{' else -1
            if depth==0:end=m.start()+t.end();break
        require(end is not None,'Broken team footnote');value=value[:m.start()]+value[end:]
    value=re.sub(r'\{\{(?:flagicon|fbaicon|flag)\|[^{}]*\}\}','',value,flags=re.I)
    value=re.sub(r'\[\[([^\]]+)\]\]',lambda m:m[1].rsplit('|',1)[-1],value)
    value=re.sub(r'<[^>]*>','',value)
    return html.unescape(' '.join(value.split())).strip()

def pair(token):
    m=re.search(r'(\d+)\s*[-–−]\s*(\d+)',token)
    return [int(m[1]),int(m[2])] if m else None

def section(text,offset):
    level2=None;lower=None;path=None
    for m in re.finditer(r'^(={2,5})\s*(.*?)\s*\1\s*$',text[:offset],re.M):
        if len(m[1])==2:level2=m[2];lower=None;path=None
        else:
            lower=m[2]
            if 'Champions Path' in lower:path='CHAMPIONS'
            if 'League Path' in lower:path='LEAGUE'
    codes={'First qualifying round':'QUALIFYING_ROUND_1','Second qualifying round':'QUALIFYING_ROUND_2','Third qualifying round':'QUALIFYING_ROUND_3','Play-off round':'QUALIFYING_PLAYOFF'}
    code=codes.get(level2)
    if level2=='Preliminary round':code='PRELIMINARY_FINAL' if lower=='Final round' else 'PRELIMINARY_SEMIFINAL' if lower=='Semi-final round' else 'PRELIMINARY'
    return code,path

def wikipedia_reader(raw,source):
    require(digest(raw)==source['sha256'] and len(raw)==source['bytes'],'Revision bytes changed')
    d=json.loads(raw);rev=d['query']['pages'][0]['revisions'][0];require(rev['revid']==source['revision'],'Revision pin changed')
    text=rev['slots']['main']['content'];boxes=[];summaries=[];aliases={}
    for start,end,name in templates(text):
        args=arguments(text[start:end]);named={};pos=[]
        for a in args[1:]:
            if '=' in a:
                k,v=a.split('=',1);k=k.strip().lower()
                require(k not in named,'Repeated source argument');named[k]=v.strip()
            else:pos.append(a.strip())
        if name.startswith('football'):
            require('team1' in named and 'team2' in named,'Incomplete source identity')
            m=re.search(r'(?i)\{\{\s*start date(?: and age)?\s*\|\s*(\d{4})\s*\|\s*(\d{1,2})\s*\|\s*(\d{1,2})',named.get('date',''))
            if m:day=date(int(m[1]),int(m[2]),int(m[3])).isoformat()
            else:
                dm=re.search(r'\d{1,2} [A-Z][a-z]+ \d{4}',tidy(named.get('date','')));require(dm,'Missing exact day');day=datetime.strptime(dm[0],'%d %B %Y').date().isoformat()
            reported=pair(tidy(named.get('score','')));extra=named.get('aet','').casefold() in {'yes','y','1'} or bool(re.search(r'a\.?e\.?t\.?|extra\s*time',named.get('score',''),re.I))
            mins=[]
            for key in ('goals1','goals2'):
                g=[]
                for goal in re.finditer(r'(?i)\{\{\s*goal\s*\|([^{}]*)\}\}',named.get(key,'')):
                    g.extend(t.strip() for t in goal[1].split('|') if re.fullmatch(r'\s*\d+(?:\+\d+)?\s*',t))
                mins.append(g)
            complete=reported is not None and list(map(len,mins))==reported
            awarded=bool(re.search(r'award|forfeit|walkover|w/o',named.get('scorenote','')+' '+tidy(named.get('score','')),re.I))
            reg=None
            if reported is not None and not awarded:
                if not extra:reg=reported
                elif complete and sum(reported)>0:reg=[sum(int(t.split('+')[0])<91 for t in times) for times in mins]
            code,path=section(text,start)
            boxes.append({'source_observation_id':digest(wire([source['sha256'],start,end])),'source':source['path'],'source_sha256':source['sha256'],
                          'season':source['season'],'date':day,'home':tidy(named['team1']),'away':tidy(named['team2']),
                          'raw_fields':named,'start':start,'end':end,'decoded_line':text[:start].count('\n')+1,'decoded_end_line':text[:end].count('\n')+1,
                          'template_sha256':digest(text[start:end].encode()),'stage':code,'path':path,'venue':tidy(named.get('stadium','')),
                          'periods':{'regulation_time':reg,'reported_score':reported,'after_extra_time':reported if extra else None,
                                     'shootout':pair(tidy(named.get('penaltyscore',''))),'extra_time_explicit':extra,'goal_minutes_home':mins[0],'goal_minutes_away':mins[1]},
                          'raw_team1':named['team1'],'raw_team2':named['team2']})
        else:
            summaries.append((start,named,pos))
    # Explicit linked-page/display correspondences are confined to this revision.
    clubraw=[x[k] for x in boxes for k in ('raw_team1','raw_team2')]
    for _,named,pos in summaries:
        clubraw+=pos
    for value in clubraw:
        m=re.search(r'\[\[([^\]]+)\]\]',value)
        if m:
            target=m[1].split('|')[0];display=tidy(value)
            if display in aliases:require(aliases[display]==target,'Ambiguous linked club display')
            aliases[display]=target
    def identity(rawname):
        m=re.search(r'\[\[([^\]]+)\]\]',rawname)
        return m[1].split('|')[0] if m else aliases.get(tidy(rawname),tidy(rawname))
    expected=Counter()
    for start,named,pos in summaries:
        if not pos or pos[0]!='main':continue
        values=pos[1:];one=named.get('legs')=='0';width=5 if one else 7
        require(len(values)%width==0,'Tie summary column width unknown')
        for i in range(0,len(values),width):
            row=values[i:i+width];team1,team2=identity(row[0]),identity(row[3]);code,_=section(text,start)
            if one and code=='PRELIMINARY':code='PRELIMINARY_FINAL' if i//width==2 else 'PRELIMINARY_SEMIFINAL'
            if one:
                score=pair(tidy(row[2]));require(score is not None,'Unscored tie summary');expected[(code,team1,team2,tuple(score))]+=1
            else:
                first,second=pair(tidy(row[5])),pair(tidy(row[6]));require(first is not None and second is not None,'Unscored paired tie summary')
                expected[(code,team1,team2,tuple(first))]+=1
                expected[(code,team2,team1,tuple(second[::-1]))]+=1
    observed=Counter((x['stage'],identity(x['raw_team1']),identity(x['raw_team2']),tuple(x['periods']['reported_score'])) for x in boxes)
    require(expected==observed,'Independent tie summary/match-box discrepancy: '+str((expected-observed).most_common(3))+' / '+str((observed-expected).most_common(3)))
    return boxes,{'season':source['season'],'boxes':len(boxes),'summary_expected':sum(expected.values()),'by_stage':dict(Counter(x['stage'] for x in boxes)),'extra_time':sum(x['periods']['extra_time_explicit'] for x in boxes)}

def independent_curley(raw,receipt):
    require(digest(raw)==receipt['sha256'] and len(raw)==receipt['bytes'],'Curley source changed')
    permission=receipt['permission'];reference=ROOT/permission['reference'];require(digest(reference.read_bytes())==permission['reference_sha256'],'Curley permission changed')
    tree=read(ROOT/'data/private/germany/second_bundesliga/metadata/engsoccerdata_tree.json')
    blob=next(x for x in tree['tree'] if x['path']=='data-raw/champs.csv')
    require(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==blob['sha'],'Curley pinned blob changed')
    r=csv.reader(io.StringIO(raw.decode('utf-8')),strict=True);headers=next(r);rows=[];physical=raw.splitlines(keepends=True);previous=r.line_num
    for values in r:
        first=previous+1;last=r.line_num;previous=last;require(len(values)==len(headers),'Curley CSV width changed')
        f=dict(zip(headers,values));year=int(f['Season'])
        if not 1992<=year<=2025:continue
        rows.append({'source_observation_id':digest(wire([receipt['sha256'],first,last])),'raw_fields':f,'physical_line':first,'end_line':last,
                     'physical_sha256':digest(b''.join(physical[first-1:last])),'season':f'{year}/{year+1}',
                     'date':f['Date'],'home':f['home'],'away':f['visitor'],
                     'periods':{k:pair(f[col]) for k,col in [('regulation_time','FT'),('half_time','HT'),('after_extra_time','aet'),('shootout','pens')]}})
    return rows


def independent_club_map(left,right):
    """Reconstruct seasonal links from club appearance fingerprints, not a saved map."""
    def name(s):
        value=''.join(c for c in unicodedata.normalize('NFD',s.casefold()) if not unicodedata.combining(c))
        value=re.sub(r'\b(?:fc|fk|afc|cf|sc|sk|ac|as|rsc|gnk|nk|if|ff|ik|a|s)\b','',value)
        return re.sub(r'\W','',value)
    def fingerprints(rows):
        out=defaultdict(set)
        for r in rows:
            p=r['periods'];score=p.get('reported_score') or p.get('after_extra_time') or p.get('regulation_time')
            for side in ('home','away'):
                out[r[side]].add((r['date'],side,tuple(score or [])))
        return out
    aa,bb=fingerprints(left),fingerprints(right);mapping={}
    for source,features in bb.items():
        exact=[n for n in aa if name(n)==name(source)]
        if len(exact)==1:mapping[source]=exact[0];continue
        scored=sorted(((len(features&f),n) for n,f in aa.items()),reverse=True)
        if scored and scored[0][0]>0 and (len(scored)==1 or scored[0][0]>scored[1][0]):mapping[source]=scored[0][1]
    # Tied appearance fingerprints are disambiguated by already identified
    # opponents and exact source dates, independently of score agreement.
    for _ in range(len(bb)):
        added={}
        for label in bb:
            if label in mapping:continue
            possibilities=[]
            for r in right:
                for side,opposite in (('home','away'),('away','home')):
                    if r[side]!=label or r[opposite] not in mapping:continue
                    options={p[side] for p in left if p['date']==r['date'] and p[opposite]==mapping[r[opposite]]}
                    if options:possibilities.append(options)
            if possibilities:
                candidates=set.intersection(*possibilities)
                if len(candidates)==1:added[label]=next(iter(candidates))
        if not added:break
        mapping.update(added)
    require(len(mapping)==len(set(mapping.values())),'Independent club fingerprint map is not injective')
    return mapping

def verify(output=PHASE/'final'):
    from scripts import verify_uefa_champions_league_inventory as previous
    prior=previous.verify();baseline,_,_,_=previous.raw_inventory(read(BASE/'phase2/acquisition_manifest.json'))
    raw={r['observation_id']:r for r in baseline};supp={};summarychecks=[]
    target=read(output/'supplemental_source_inventory.json')['observations'];targets={r['source_observation_id']:r for r in target}
    index=read(PHASE/'wikipedia_cached_source_index.json')
    for source in index:
        path=PHASE/source['path'];receipt=read(path.with_name(path.name+'.provenance.json'))
        require(receipt['status']==200 and receipt['sha256']==source['sha256'] and receipt['permission']['license']=='CC BY-SA 4.0' and str(source['revision']) in receipt['permission']['permalink'],'Revision provenance differs')
        if source['kind']!='qualifying':
            require(digest(path.read_bytes())==source['sha256'],'Context original changed');continue
        rows,checks=wikipedia_reader(path.read_bytes(),source);summarychecks.append(checks)
        for x in rows:
            t=targets[x['source_observation_id']]
            for k in ('raw_fields','date','home','away','season','stage','path','venue','decoded_line','decoded_end_line','template_sha256'):
                require(t[k]==x[k],'Supplement independent field differs: '+k)
            require(t['decoded_wikitext_start']==x['start'] and t['decoded_wikitext_end']==x['end'],'Decoded locator differs')
            for k,v in x['periods'].items():require(t['periods'][k]==v,'Supplement period differs: '+k)
            supp[x['source_observation_id']]=x
    cp=PHASE/'originals/engsoccerdata/champs.csv';curley=independent_curley(cp.read_bytes(),read(cp.with_name(cp.name+'.provenance.json')))
    for x in curley:
        t=targets[x['source_observation_id']]
        for k,v in x.items():require(t[k]==v,'Curley independent field differs: '+k)
        supp[x['source_observation_id']]=x
    require(set(supp)==set(targets),'Supplement observation population differs')
    registry=read(output/'decision_registry.json');events=registry['fixture_events'];evidence=read(PHASE/'adjudication_evidence.json');rules=defaultdict(list)
    for rule in evidence['rules']:rules[rule['observation_id']].append(rule)
    require(registry['policy_evidence_sha256']==digest((PHASE/'adjudication_evidence.json').read_bytes()),'Decision evidence fingerprint differs')
    membership=Counter();primary=Counter();byid={e['event_id']:e for e in events};owner={}
    frozen=read(BASE/'phase2/validated/event_inventory.json')['events']
    for old in frozen:
        require(old['event_id'] in byid and set(old['observations'])<=set(byid[old['event_id']]['observations']),'Frozen event identity or observation lost')
    for e in events:
        oid=e['primary_observation_id'];primary[oid]+=1;membership.update(e['observations']);owner.update({i:e['event_id'] for i in e['observations']});p=raw.get(oid,supp.get(oid))
        require(p is not None,'Primary original missing');require(e['first_listed']==p['home'] and e['second_listed']==p['away'],'Source orientation changed')
        require(e['season']==p['season'] and e['stage']==p['stage'] and e['source_date']==p['date'],'Source stage/date/season changed')
        require(e['scope']==p.get('scope','QUALIFYING'),'Source stage eligibility scope differs')
        locator=e['source_evidence'][0]
        require(locator['observation_id']==oid and locator['source']==p['source'] and locator['source_sha256']==p['source_sha256'],'Primary source trace differs')
        if oid in raw:require((locator['line'],locator['end_line'])==(p['line'],p['end_line']),'Physical source line trace differs')
        else:require((locator['decoded_line'],locator['decoded_end_line'],locator['decoded_wikitext_start'],locator['decoded_wikitext_end'],locator['template_sha256'],locator['physical_json_line'])==(p['decoded_line'],p['decoded_end_line'],p['start'],p['end'],p['template_sha256'],1),'Revision/decoded source trace differs')
        expected={'regulation_time':p['periods']['regulation_time'],'observed_regulation_time':p['periods']['regulation_time'],
                  'after_extra_time':p['periods'].get('after_extra_time'),'shootout':p['periods'].get('shootout'),
                  'half_time':p['periods'].get('half_time'),'football_date':p['date'],'disposition':'INCLUDE','neutral_venue':None,'administrative_result':None,
                  'leg':p.get('source_leg'),'replay':p.get('replay',False),'venue':None if oid in raw else p['venue']}
        for d in rules[oid]:
            require(d['source_sha256']==p['source_sha256'] if 'source_sha256' in p else True,'Rule source fingerprint differs')
            require((d['expected_date'],d['expected_home'],d['expected_away'])==(p['date'],p['home'],p['away']),'Rule raw identity differs')
            require(all(z in evidence['evidence'] for z in d['evidence_ids']),'Unreferenced adjudication')
            expected.update(d['changes'])
            if 'regulation_time' in d['changes'] and 'observed_regulation_time' not in d['changes']:expected['observed_regulation_time']=d['changes']['regulation_time']
        score=expected['administrative_result'] if expected['administrative_result'] is not None and expected['disposition']=='INCLUDE' else expected['regulation_time'] if expected['disposition']=='INCLUDE' else None
        if expected['disposition']=='INCLUDE' and (score is None or expected['football_date'] is None):expected['disposition']='HOLD OUT';score=None
        for k,v in expected.items():require(e.get(k)==v,'Independently reconstructed decision differs: '+k)
        if e['season']=='2023/2024' and e['stage']=='FIRST_GROUP':
            gs=[g for g,ns in evidence['group_2023_labels'].items() if e['first_listed'] in ns and e['second_listed'] in ns]
            require(len(gs)==1 and e['group']==gs[0] and e['group_evidence']==evidence['group_evidence'],'Researched group membership differs')
        else:require(e['group']==p.get('group'),'Unapproved group change')
        require(e['accepted_result']==score,'Accepted result/administrative exception differs')
        outcome=None if score is None else 'X' if score[0]==score[1] else '1' if score[0]>score[1] else '2'
        require(e['outcome']==outcome,'Outcome depends on something other than first-listed result')
        require(e['neutral_venue'] in (0,1,None),'Invalid venue status')
        if e['disposition']=='NOT PLAYED':require(e['football_date'] is None and e['regulation_time'] is None and e['accepted_result'] is None,'No-kickoff score entered played population')
    require(set(membership)==set(raw)|set(supp) and set(membership.values())=={1},'Source observations lost or multiply counted')
    require(set(primary.values())=={1},'Nonunique event primary')
    new=[e for e in events if e['population']=='RECOVERED_QUALIFYING']
    require(len(new)==692 and all(e['event_id']==digest(wire([e['primary_observation_id']])) for e in new),'New event identity differs')
    # Verify every supplemental overlap from independently parsed raw identities.
    reports=read(output/'source_correspondences.json')['reports'];links=0
    for report in reports:
        mapping={x['source_label']:x['target_label'] for x in report['mapping']};require(len(mapping)==len(set(mapping.values())),'Noninjective source-bound club map')
        left=[r for r in baseline if r['season']==report['season'] and r['publisher'].startswith('footballcsv' if int(r['season'][:4])<=2015 else 'openfootball') and (report['publisher']!='wikipedia' or r['scope']=='QUALIFYING')]
        right=[r for r in supp.values() if r['season']==report['season'] and ('raw_team1' in r)==(report['publisher']=='wikipedia')]
        independent=independent_club_map(left,right)
        require(mapping==independent,'Independent seasonal name correspondence differs')
        for link in report['links']:
            a,b=raw[link['left']],supp[link['right']];reverse=link['orientation']=='REVERSED'
            require((mapping[b['home']],mapping[b['away']])==((a['away'],a['home']) if reverse else (a['home'],a['away'])),'Unsupported seasonal correspondence')
            require(a['season']==b['season'] and membership[link['left']]==membership[link['right']]==1,'Overlap population differs')
            # The two observations must actually belong to the same event.
            require(owner[link['left']]==owner[link['right']],'Overlap was double-counted')
            require(link['date_equal']==(a['date']==b['date']),'Overlap date comparison differs')
            if not link['date_equal']:
                decisions=read(PHASE/'auxiliary_correspondence_evidence.json')['decisions']
                matches=[d for d in decisions if d['auxiliary_observation_id']==link['right'] and d['primary_observation_id']==link['left']]
                require(len(matches)==1 and matches[0]['expected_auxiliary_date']==b['date'] and matches[0]['expected_primary_date']==a['date'],'Uncontained auxiliary date conflict')
            x,z=a['periods']['regulation_time'],b['periods']['regulation_time'];same=None if x is None or z is None else x==(z[::-1] if reverse else z)
            require(link['regulation_equal']==same,'Overlap period comparison differs');links+=1
    # Qualifying fixtures close each independent paired/single summary. Old seasons
    # retain the accepted stage model, with separately reviewed RSSSF count evidence.
    coverage=read(output/'coverage_assessment.json')['seasons'];recounts=[]
    external={x['season']:x for x in read(PHASE/'historical_coverage_evidence.json')}
    for m in coverage:
        es=[e for e in events if e['season']==m['season']];q=[e for e in es if e['scope']=='QUALIFYING']
        require(len(q)==m['qualifying_expected_descriptions']==m['qualifying_observed_descriptions'],'Season qualifying completeness differs')
        require(dict(Counter(e['stage'] for e in es))==m['stages'],'Stage accounting differs')
        require(len([e for e in es if e['scope']=='MAIN'])==m['main_descriptions'],'Main accounting differs')
        require(Counter(e['disposition'] for e in q)==Counter(m['qualifying_dispositions']),'Disposition season accounting differs')
        if m['season'] in external:require(len(q)==external[m['season']]['qualifying_expected_descriptions'],'Separate-publisher qualifying count evidence differs')
        recounts.append({'season':m['season'],'main':m['main_descriptions'],'qualifying':len(q)})
    # Extra time requires a tied regulation aggregate; the pre2021 away-goal rule
    # additionally requires equal away goals. This flags, never infers, scores.
    tie_checks=0
    for e in events:
        if e['after_extra_time'] is None or e['stage']=='FINAL':continue
        earlier=[z for z in events if z['season']==e['season'] and z['stage']==e['stage'] and (z['first_listed'],z['second_listed'])==(e['second_listed'],e['first_listed']) and z['football_date'] and e['football_date'] and z['football_date']<e['football_date']]
        if len(earlier)!=1:continue
        first=earlier[0]['accepted_result'];second=e['regulation_time'];require(first is not None and second is not None,'Unknown extra-time tie')
        require(first[0]+second[1]==first[1]+second[0],'Extra-time regulation aggregate not tied')
        if int(e['season'][:4])<=2020:require(first[1]==second[1],'Extra time violates contemporary away-goal condition')
        tie_checks+=1
    aggregate_checks=0
    for e in events:
        if e['stage'] in ('FIRST_GROUP','SECOND_GROUP','LEAGUE_PHASE'):require('calculated_standing_tie_aggregate' not in e,'Ordinary group fixture treated as two-leg knockout tie')
        if 'calculated_standing_tie_aggregate' not in e:continue
        ids=e['aggregate_calculation_observations'];require(len(ids)==2 and ids[1]==e['primary_observation_id'],'Aggregate input trace differs')
        first=byid[owner[ids[0]]];a=first.get('administrative_result') or first['after_extra_time'] or first['regulation_time'];b=e.get('administrative_result') or e['after_extra_time'] or e['regulation_time']
        require(e['calculated_standing_tie_aggregate']==[a[1]+b[0],a[0]+b[1]],'Audit aggregate calculation differs');aggregate_checks+=1
    contexts=registry['additional_nonstanding_context_events'];require(len(contexts)==len(evidence['additional_nonstanding_contexts'])==3,'Nonstanding attempts lost')
    for c in contexts:require(c['disposition']=='OUT OF SCOPE' and c['accepted_result'] is None and c['outcome'] is None and c['event_id']==digest(wire(['NONSTANDING_CONTEXT',{k:v for k,v in c.items() if k in evidence['additional_nonstanding_contexts'][0] or k in ('partial_played_score','reported_played_score')}])), 'Nonstanding context integrity differs')
    totals=dict(Counter(e['disposition'] for e in events+contexts))
    oldreview=previous.read(previous.INVENTORY/'unresolved_issues.json');resolution=read(output/'review_resolution.json')
    require({r['event_id'] for r in resolution['events']}=={r['event_id'] for r in oldreview['event_queue']},'Frozen review queue not covered')
    for r in resolution['events']:require(r['disposition']==byid[r['event_id']]['disposition'] and r['decision_evidence'],'Review resolution lacks disposition/evidence')
    require(resolution['contexts']==oldreview['contexts'],'Frozen season contexts lost')
    require(len(events)==6645 and totals=={'INCLUDE':6642,'NOT PLAYED':3,'OUT OF SCOPE':3},'Reviewed population totals differ')
    return {'status':'PASS','independent_original_reader':True,'network_requests':0,'phase2_verification':prior['status'],
            'source_observations_reconstructed':len(raw)+len(supp),'fixture_events':len(events),'additional_nonstanding_contexts':len(contexts),
            'dispositions':totals,'wikipedia_tie_summary_checks':summarychecks,'supplemental_overlap_links':links,
            'extra_time_regulation_tie_checks':tie_checks,'separate_publisher_qualifying_season_counts':len(external),'aggregate_audit_checks':aggregate_checks,'season_counts':recounts,
            'limits':'Independent computation and separate representations do not establish disjoint historical upstreams or certify every ordinary fixture.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--inventory',type=Path,default=PHASE/'final');p.add_argument('--output',type=Path);a=p.parse_args();result=verify(a.inventory)
    if a.output:
        require(not a.output.resolve().is_relative_to(ROOT) or a.output.resolve().is_relative_to(ROOT/'data/private'),'Detailed output must remain private')
        with a.output.open('xb') as f:f.write(wire(result))
    print(json.dumps({k:v for k,v in result.items() if k not in ('season_counts','wikipedia_tie_summary_checks')},indent=2))
