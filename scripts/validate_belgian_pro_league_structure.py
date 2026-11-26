"""Independent offline Phase 4 validation, not historical adjudication.

No Phase 2/3 parser, assessor, alias resolver or queue builder is imported.
Saved inventories are comparison targets only, after raw reconstruction.
"""
from collections import Counter, defaultdict
from datetime import date
from html import unescape
from pathlib import Path
import calendar,csv,hashlib,io,json,os,re,subprocess,tempfile

ROOT=Path(__file__).resolve().parents[1]
PRIVATE=ROOT/'data/private/belgium/pro_league'
HEAD='013bb9c195624d5ac290aeb57dae11c4e21c0b5a'
COLUMNS=('Date','Season','home','visitor','FT','hgoal','vgoal','division','tier','totgoal','goaldif','result')
NAMES=('structural_assessment.json','source_observations.json','overlap_reconciliation.json','exception_registry.json','queue_verification.json','coverage_provenance.json')


def encode(obj):return (json.dumps(obj,sort_keys=True,indent=2,ensure_ascii=False)+'\n').encode()
def sha(raw):return hashlib.sha256(raw).hexdigest()
def sid(digest,start,end):return sha(encode([digest,start,end]))
def expected_clubs(y):return 18 if y<=2008 or 2020<=y<=2022 else 16


def protect(directory=PRIVATE):
    from scripts import collect_belgian_pro_league_history as acquisition
    previous=acquisition.protect(directory)
    baseline=json.loads((directory/'phase4_protected_before.json').read_text())
    for name,digest in baseline['files'].items():
        if sha((ROOT/name).read_bytes())!=digest:raise ValueError('Frozen evidence changed: '+name)
    prefix=baseline['planning_log'];log=(ROOT/'PLANNING_LOG.md').read_bytes()
    if sha(log[:prefix['bytes']])!=prefix['sha256']:raise ValueError('Planning history changed')
    if subprocess.check_output(['git','branch','--show-current'],cwd=ROOT).decode().strip()!='feature/data-collection':raise ValueError('Wrong branch')
    return dict(previous=previous,frozen_phase2_3_entries=len(baseline['files']))


def bind(r,rec,physical,start,end):
    return dict(r,source=rec['path'],source_sha256=rec['sha256'],source_line=start,source_end_line=end,
                physical_record_sha256=sha(b''.join(physical[start-1:end])),audit_id=sid(rec['sha256'],start,end))


def check_row(r):
    errors=[];y=int(r['season'][:4])
    try:
        d=date.fromisoformat(r['date'])
        if d.isoformat()!=r['date'] or not date(y,7,1)<=d<=date(y+1,6,30):errors.append('DATE_OUTSIDE_CANONICAL_SEASON')
    except ValueError:errors.append('INVALID_DATE')
    if r['home']==r['away'] or any(not r[k] or r[k]!=r[k].strip() or '\ufffd' in r[k] for k in ('home','away')):errors.append('INVALID_TEAM_LABEL')
    if (r['hg'] is None)!=(r['ag'] is None):errors.append('PARTIAL_SCORE')
    if r['hg'] is not None:
        if not all(re.fullmatch(r'0|[1-9]\d*',r[k] or '') for k in ('hg','ag')):errors.append('INVALID_GOALS')
        elif r['FT']!=r['hg']+'-'+r['ag']:errors.append('FT_CONTRADICTION')
        if r.get('HT'):
            h,a=map(int,r['HT'].split('-'))
            if r['hg'].isdigit() and r['ag'].isdigit() and (h>int(r['hg']) or a>int(r['ag'])):errors.append('HALFTIME_EXCEEDS_FINAL')
    if 'cancelled' in r['annotation'].lower() and r['FT'] is not None:errors.append('CANCELLED_WITH_SCORE')
    return errors


def csv_rows(raw,rec):
    if sha(raw)!=rec['sha256']:raise ValueError('CSV hash differs')
    reader=csv.reader(io.StringIO(raw.decode('utf-8-sig'),newline=''),strict=True)
    if tuple(next(reader))!=COLUMNS:raise ValueError('CSV schema differs')
    physical=raw.splitlines(keepends=True);out=[]
    while True:
        start=reader.line_num+1
        try:cells=next(reader)
        except StopIteration:break
        if len(cells)!=12:raise ValueError(f'CSV width at {start}')
        original=dict(zip(COLUMNS,cells))
        if not re.fullmatch(r'\d{4}',original['Season']):raise ValueError('Invalid season')
        y=int(original['Season']);h,a=original['hgoal'],original['vgoal']
        r=dict(season=f'{y}/{y+1}',date=original['Date'],home=original['home'],away=original['visitor'],hg=h or None,ag=a or None,FT=original['FT'] or None,HT=None,stage='UNKNOWN',group=None,round=None,leg=None,annotation='',original_fields=original)
        issues=check_row(r)
        if original['division']!='B1' or original['tier']!='1':issues.append('WRONG_COMPETITION')
        if h.isdigit() and a.isdigit():
            hi,ai=int(h),int(a)
            if original['totgoal']!=str(hi+ai) or original['goaldif']!=str(hi-ai):issues.append('DERIVED_GOALS_CONTRADICTION')
            if original['result']!=('H' if hi>ai else 'A' if ai>hi else 'D'):issues.append('OUTCOME_CONTRADICTION')
        r['errors']=issues;out.append(bind(r,rec,physical,start,reader.line_num))
    if not out:raise ValueError('Empty CSV')
    return out


def day_heading(text,year):
    m=re.fullmatch(r'([A-Z][a-z]{2}) ([A-Z][a-z]{2}) (\d{1,2})(?: (\d{4}))?',text)
    if not m:return None
    days=list(calendar.day_abbr);months=list(calendar.month_abbr)
    if m[1] not in days or m[2] not in months:raise ValueError('Unknown day/month')
    found=[]
    for y in ([int(m[4])] if m[4] else [year,year+1]):
        try:d=date(y,months.index(m[2]),int(m[3]))
        except ValueError:continue
        if date(year,7,1)<=d<=date(year+1,6,30) and d.weekday()==days.index(m[1]):found.append(d.isoformat())
    if len(found)!=1:raise ValueError('Ambiguous/invalid source date: '+text)
    return found[0]


def txt_rows(raw,rec):
    if sha(raw)!=rec['sha256']:raise ValueError('TXT hash differs')
    physical=raw.splitlines(keepends=True);lines=raw.decode('utf-8-sig').splitlines();out=[];headings=[];title=None;year=None;stage=None;rnd=None;current=None;date_line=None
    stage_names={'Playoff I':'CHAMPIONSHIP','Championship':'CHAMPIONSHIP','Europe':'EUROPE','Relegation':'PLAYDOWNS'}
    for number,literal in enumerate(lines,1):
        t=literal.strip()
        if not t or t.startswith('#'):continue
        if t.startswith('='):
            m=re.fullmatch(r'= Belgium First Division A (\d{4})/(\d{2})',t)
            if title or not m or int(m[2])!=(int(m[1])+1)%100:raise ValueError('Invalid/duplicate TXT title')
            title=t;year=int(m[1]);continue
        if year is None:raise ValueError('Missing title')
        if t.startswith('▪'):
            payload=t.removeprefix('▪ ').split(', ')
            if payload==['ECL Playoff','Final']:stage='EUROPE_QUALIFICATION';rnd='Final'
            else:
                if len(payload)==2:
                    if payload[0] not in stage_names:raise ValueError('Unknown stage')
                    stage=stage_names[payload[0]]
                elif len(payload)==1:stage='REGULAR_SEASON'
                else:raise ValueError('Unknown subdivision')
                r=re.fullmatch(r'(?:Matchday (\d+)|(\d+)\. Round)',payload[-1])
                if not r:raise ValueError('Unknown round grammar')
                rnd=int(r[1] or r[2]);limit=2*(expected_clubs(year)-1) if stage=='REGULAR_SEASON' else 6 if stage=='PLAYDOWNS' or (stage in ('CHAMPIONSHIP','EUROPE') and 2020<=year<=2022) else 10
                if not 1<=rnd<=limit:raise ValueError('Round outside stage format')
            headings.append(dict(line=number,text=t,stage=stage,round=rnd));current=None;continue
        parsed=day_heading(t,year)
        if parsed:current=parsed;date_line=number;continue
        if current is None or stage is None:raise ValueError(f'Fixture without dated stage at {number}')
        body=re.sub(r'^\d{1,2}:\d{2}\s+','',t);note=re.search(r'\s+(\[[^\]]+\])$',body)
        annotation=note[1] if note else ''
        if note:body=body[:note.start()].rstrip()
        participants=re.split(r'\s+v\s+',body)
        if len(participants)!=2:raise ValueError('Unknown fixture delimiter')
        home,right=participants;m=re.fullmatch(r'(.+?)\s{2,}([0-9]+)-([0-9]+)(?:\s+\(([0-9]+-[0-9]+)\))?',right)
        if m:away,h,a,half=m.groups();ft=h+'-'+a
        else:
            if re.search(r'\d\s*[-:]|[-:]\s*\d|\?',right):raise ValueError('Malformed score')
            away=right;h=a=half=ft=None
        r=dict(season=f'{year}/{year+1}',date=current,home=home,away=away,hg=h,ag=a,FT=ft,HT=half,annotation=annotation,stage=stage,group=None,round=rnd,leg=None,date_heading_line=date_line)
        r['errors']=check_row(r);out.append(bind(r,rec,physical,number,number))
    if not title or not out:raise ValueError('Incomplete TXT')
    return out,dict(requested_season=rec['season'],declared_season=f'{year}/{year+1}',path_season_mismatch=rec['season']!=f'{year}/{year+1}',title=title,stage_headings=headings)


def identity(r):return [r['season'],'Belgian Pro League',r['stage'],r['group'],r['round'],r['leg'],r['date'],r['home'],r['away']]


def expected_stage_clubs(stage,year):
    if stage=='REGULAR_SEASON':return expected_clubs(year)
    if stage in ('CHAMPIONSHIP','EUROPE'):return 4 if 2020<=year<=2022 else 6
    return 4 if stage=='PLAYDOWNS' else 2 if stage=='EUROPE_QUALIFICATION' else None


def assess(rows,year,modern=False):
    names=sorted({r[k] for r in rows for k in ('home','away')});pairs=defaultdict(list);rounds=defaultdict(list);identities=defaultdict(list);stages={}
    for r in rows:
        pairs[r['home'],r['away']].append(r)
        identities[json.dumps(identity(r),ensure_ascii=False)].append(r['audit_id'])
        if r['round'] is not None:rounds[r['stage'],str(r['round'])].append(r)
    for stage in sorted({r['stage'] for r in rows}):
        ss=[r for r in rows if r['stage']==stage];clubs=sorted({r[k] for r in ss for k in ('home','away')});pp=Counter((r['home'],r['away']) for r in ss);roundmap=defaultdict(list)
        for r in ss:roundmap[str(r['round'])].append(r)
        regular_or_group=modern and stage!='EUROPE_QUALIFICATION'
        stages[stage]=dict(expected_clubs=expected_stage_clubs(stage,year) if modern else None,observed=len(ss),scored=sum(r['FT'] is not None for r in ss),clubs=len(clubs),team_labels=clubs,directed_pairings=len(pp),missing_directed_pairings=[[h,a] for h in clubs for a in clubs if h!=a and (h,a) not in pp] if regular_or_group else None,repeated_pairings=[dict(home=h,away=a,count=n) for (h,a),n in sorted(pp.items()) if n>1],rounds={rnd:dict(observed=len(rs),clubs=len({r[k] for r in rs for k in ('home','away')}),repeated_clubs=[name for name,n in Counter(r[k] for r in rs for k in ('home','away')).items() if n>1]) for rnd,rs in sorted(roundmap.items())},date_range=[min(r['date'] for r in ss),max(r['date'] for r in ss)])
    wide=[]
    for (stage,rnd),rs in sorted(rounds.items()):
        first=min(r['date'] for r in rs);last=max(r['date'] for r in rs);span=(date.fromisoformat(last)-date.fromisoformat(first)).days
        if span>14:wide.append(dict(stage=stage,round=rnd,earliest=first,latest=last,span_days=span,source_ids=[r['audit_id'] for r in rs]))
    slots=len(names)*(len(names)-1);prefix=rows[:slots];complete=len(prefix)==slots and len({(r['home'],r['away']) for r in prefix})==slots
    return dict(season=f'{year}/{year+1}',observed=len(rows),scored=sum(r['FT'] is not None for r in rows),unscored=sum(r['FT'] is None for r in rows),clubs=len(names),team_labels=names,nominal_clubs=expected_clubs(year),nominal_regular_slots=expected_clubs(year)*(expected_clubs(year)-1),stage_counts=dict(Counter(r['stage'] for r in rows)),stages=stages,prefix_candidate=slots if complete else None,additional_candidate=len(rows)-slots if complete else None,missing_pairs_among_observed_clubs=[[h,a] for h in names for a in names if h!=a and (h,a) not in pairs],pair_repeats=[dict(source_ids=[r['audit_id'] for r in rs]) for pair,rs in sorted(pairs.items()) if len(rs)>1],duplicate_stage_identities=[dict(identity=json.loads(k),source_ids=ids) for k,ids in sorted(identities.items()) if len(ids)>1],wide_rounds=wide,order_reversals=[(a['audit_id'],b['audit_id']) for a,b in zip(rows,rows[1:]) if b['date']<a['date']],errors=[dict(source_id=r['audit_id'],errors=r['errors']) for r in rows if r['errors']])


def correspond(historical,modern):
    if len({r['season'] for r in historical+modern})!=1:raise ValueError('Mixed-season correspondence')
    # Independent candidate criterion: dates and home/away orientation ONLY.
    # Goals are deliberately excluded from label inference and checked afterwards.
    def patterns(rows):
        out=defaultdict(set)
        for r in rows:
            if r['FT'] is not None:
                out[r['home']].add((r['date'],'H'));out[r['away']].add((r['date'],'A'))
        return out
    hp,mp=patterns(historical),patterns(modern);mapping={};evidence=[]
    for name,pattern in sorted(mp.items()):
        scored=sorted([(len(pattern&other)/min(len(pattern),len(other)),old,len(pattern&other)) for old,other in hp.items()],reverse=True)
        if scored and scored[0][0]>=0.8 and (len(scored)==1 or scored[0][0]>scored[1][0]):
            strength,old,shared=scored[0];mapping[name]=old;evidence.append(dict(modern=name,historical=old,shared_date_sides=shared,agreement=strength,status='SEASON_BOUND_DIAGNOSTIC_ONLY'))
    if len(set(mapping.values()))!=len(mapping):raise ValueError('Ambiguous many-to-one identity candidates')
    hi=defaultdict(list);mi=defaultdict(list)
    for r in historical:hi[r['home'],r['away']].append(r)
    for r in modern:
        if r['home'] in mapping and r['away'] in mapping:mi[mapping[r['home']],mapping[r['away']]].append(r)
    links=[];ambiguous=[];used=set()
    for pair,hrs in sorted(hi.items()):
        mrs=mi.get(pair,[])
        for h in hrs:
            candidates=[r for r in mrs if r['date']==h['date']]
            if len(candidates)!=1:candidates=mrs if len(hrs)==len(mrs)==1 else []
            if len(candidates)!=1:
                if mrs:ambiguous.append(h['audit_id'])
                continue
            m=candidates[0]
            if m['audit_id'] in used:raise ValueError('One observation reused across event links')
            used.add(m['audit_id']);links.append(dict(historical_id=h['audit_id'],modern_id=m['audit_id'],stage=m['stage'],date_equal=h['date']==m['date'],score_equal=h['FT']==m['FT']))
    hs={x['historical_id'] for x in links}
    return dict(mapping=evidence,links=links,matched=len(links),matched_stages=dict(Counter(x['stage'] for x in links)),unmatched_historical=[r['audit_id'] for r in historical if r['audit_id'] not in hs],unmatched_modern=[r['audit_id'] for r in modern if r['audit_id'] not in used],date_conflicts=sum(not x['date_equal'] for x in links),score_conflicts=sum(not x['score_equal'] for x in links),ambiguous=ambiguous)


def documentary(raw,rec):
    lines=raw.decode(rec['encoding']).splitlines();physical=raw.splitlines(keepends=True);rows=[];regular=False;round_id=None;date_context=None
    for line,literal in enumerate(lines,1):
        if '<a name="reg">Regular Stage' in literal:regular=True
        if '<a name="play">Playoff Stage' in literal:regular=False
        text=unescape(re.sub('<[^>]*>','',literal)).strip()
        if not regular:continue
        if text.startswith('Round '):round_id=int(re.match(r'Round (\d+)',text)[1]);date_context=None
        if re.search(r'\[(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d',text):date_context=text
        if not text or not text[0].isalpha() or text.startswith(('NB:','record at exclusion:')):continue
        note=re.search(r'\s+(\[.*)$',text);body=text[:note.start()] if note else text
        m=re.fullmatch(r'(.+?)\s+(\d+-\d+|awd|n/p)\s+(.+)',body)
        if m and not m[3][0].isdigit():
            rows.append(dict(source=rec['path'],source_sha256=rec['sha256'],source_line=line,source_line_sha256=sha(physical[line-1]),home=m[1],away=m[3],score=m[2],annotation=note[1] if note else '',stage='REGULAR_SEASON',round=round_id,date_heading=date_context,audit_id=sha(encode([rec['sha256'],line,'RSSSF_DOCUMENTARY']))))
    return rows


def build(directory=PRIVATE):
    receipts=json.loads((directory/'acquisition.json').read_text())['files']+json.loads((directory/'phase3_acquisition.json').read_text())['files']
    if len(receipts)!=9 or len({r['path'] for r in receipts})!=9:raise ValueError('Wrong approved original population')
    history=[];modern={};docs={};provenance=[];defects=[]
    def require(ok,message):
        if not ok:defects.append(message)
    for rec in receipts:
        raw=(directory/rec['path']).read_bytes()
        if sha(raw)!=rec['sha256'] or len(raw)!=rec['bytes']:raise ValueError('Immutable original differs: '+rec['path'])
        if rec['git_blob_sha1']:
            blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
            if blob!=rec['expected_blob'] or blob!=rec['git_blob_sha1'] or len(raw)!=rec['expected_bytes']:raise ValueError('Pinned blob differs')
        sidecar=json.loads((directory/rec['path']).with_name(Path(rec['path']).name+'.provenance.json').read_text())
        if sidecar!=rec:raise ValueError('Receipt binding differs')
        provenance.append(dict(path=rec['path'],sha256=sha(raw),bytes=len(raw),git_blob=rec['git_blob_sha1'],commit=rec['commit']))
        if rec['repository']=='jalapic/engsoccerdata':history=csv_rows(raw,rec)
        elif rec['repository']=='openfootball/belgium':
            rows,meta=txt_rows(raw,rec);year=int(meta['declared_season'][:4]);modern[rec['original_path']]=dict(meta,assessment=assess(rows,year,True),observations=rows)
        else:docs[rec['original_path']]=documentary(raw,rec)
    by=defaultdict(list)
    for r in history:by[r['season']].append(r)
    hs={season:assess(rows,int(season[:4])) for season,rows in sorted(by.items())}
    allrows={r['audit_id']:r for r in history};links={};anchors={}
    for path,m in sorted(modern.items()):
        rs=m['observations'];allrows.update({r['audit_id']:r for r in rs})
        o=correspond(by[m['declared_season']],rs) if by[m['declared_season']] else dict(matched=0,links=[],mapping=[],unmatched_historical=[],unmatched_modern=[r['audit_id'] for r in rs],status='NO_HISTORICAL_COUNTERPART')
        links[path]=o
        for pair in o['links']:
            if pair['historical_id'] in anchors:raise ValueError('Historical observation reused')
            anchors[pair['historical_id']]=pair['modern_id']
    require(len(allrows)==len(history)+sum(len(m['observations']) for m in modern.values()),'Source observation ID collision')
    event_members=defaultdict(list)
    for source_id in sorted(allrows):event_members[anchors.get(source_id,source_id)].append(source_id)
    queue=defaultdict(lambda:defaultdict(set));contexts={}
    def flag(source_id,category,context=None):
        anchor=anchors.get(source_id,source_id);queue[anchor][category].add(source_id)
        if context is not None:contexts.setdefault(anchor,[]).append(dict(source_id=source_id,category=category,context=context))
    for season,a in hs.items():
        if a['additional_candidate']:
            for r in by[season][a['prefix_candidate']:]:flag(r['audit_id'],'HISTORICAL_STAGE_UNCERTAINTY')
    for rows,a in [(by[s],h) for s,h in hs.items()]+[(m['observations'],m['assessment']) for m in modern.values()]:
        for r in rows:
            if r['FT'] is None:flag(r['audit_id'],'UNSCORED_SOURCE_SLOT')
            if r['annotation']:flag(r['audit_id'],'SOURCE_ANNOTATION',r['annotation'])
            if r['FT'] is not None and r['hg'].isdigit() and r['ag'].isdigit() and (max(int(r['hg']),int(r['ag']))>=7 or int(r['hg'])+int(r['ag'])>=10):flag(r['audit_id'],'UNUSUAL_SCORE')
            if r['errors']:flag(r['audit_id'],'STRUCTURAL_FIELD_CANDIDATE',r['errors'])
        for pair in a['pair_repeats']:
            for source_id in pair['source_ids']:flag(source_id,'REPEATED_DIRECTED_PAIR')
        for w in a['wide_rounds']:
            for source_id in w['source_ids']:flag(source_id,'WIDE_ROUND',dict(stage=w['stage'],round=w['round'],span_days=w['span_days'],earliest=w['earliest'],latest=w['latest']))
        for first,second in a['order_reversals']:
            flag(first,'SOURCE_ORDER_REVERSAL');flag(second,'SOURCE_ORDER_REVERSAL')
        require(not a['errors'],'Structurally invalid fields in '+a['season'])
        require(not a['duplicate_stage_identities'],'Duplicate stage/date identity in '+a['season'])
    for path,m in modern.items():
        if m['path_season_mismatch']:
            for r in m['observations']:flag(r['audit_id'],'PATH_DECLARED_SEASON_MISMATCH')
        o=links[path]
        if o['matched']:
            for source_id in o['unmatched_modern']:flag(source_id,'UNMATCHED_MODERN_OBSERVATION')
            for source_id in o['unmatched_historical']:flag(source_id,'UNMATCHED_HISTORICAL_OBSERVATION')
            for pair in o['links']:
                if not pair['date_equal'] or not pair['score_equal']:flag(pair['modern_id'],'OVERLAP_CONFLICT')
        for stage,s in m['assessment']['stages'].items():
            require(s['clubs']==s['expected_clubs'],'Incorrect participant count in '+path+' '+stage)
            if stage!='EUROPE_QUALIFICATION':require(len(s['rounds'])==2*(s['expected_clubs']-1),'Incomplete round identities in '+path+' '+stage)
            require(not s['repeated_pairings'],'Repeated pairing within explicit '+path+' '+stage)
            require(not s['missing_directed_pairings'],'Missing pairing within explicit '+path+' '+stage)
            for rnd,r in s['rounds'].items():require(not r['repeated_clubs'],'Club appears twice in round '+path+' '+stage+' '+rnd)
    documentary_exceptions=[]
    for path,rows in docs.items():
        for r in rows:
            if 'annulled' in r['annotation'] or r['score'] in ('awd','n/p'):
                allrows[r['audit_id']]=r;event_members[r['audit_id']]=[r['audit_id']];flag(r['audit_id'],'DOCUMENTARY_ADMINISTRATIVE_REPRESENTATION');documentary_exceptions.append(r)
    # Compare saved representations only after constructing the raw population.
    old_h=json.loads((directory/'phase3/historical_inventory.json').read_text());old_m=json.loads((directory/'phase3/modern_inventory.json').read_text());old_o=json.loads((directory/'phase3/overlap_inventory.json').read_text());old_q=json.loads((directory/'phase3/review_queue.json').read_text());old_matrix=json.loads((directory/'phase3/coverage_matrix.json').read_text())
    saved_rows=old_h['observations']+[r for m in old_m.values() for r in m['observations']]
    require(len(saved_rows)==len(history)+sum(len(m['observations']) for m in modern.values()),'Phase3 source census differs')
    for saved in saved_rows:
        r=allrows.get(saved['audit_id'])
        require(r is not None,'Missing saved source observation')
        if r is None:continue
        fields=('source','source_sha256','source_line','source_end_line','physical_record_sha256','season','date','home','away','hg','ag','FT','HT','annotation','stage','group','round','leg')
        require(all(r[k]==saved[k] for k in fields),'Phase3 source binding differs: '+r['audit_id'])
        if 'original_fields' in r:require(r['original_fields']==saved['original_fields'],'Saved original CSV fields differ')
        if 'date_heading_line' in r:require(r['date_heading_line']==saved['date_heading_line'],'Saved date-heading line differs')
    for path,o in links.items():
        saved=old_o[path];pairs={(x['historical_id'],x['modern_id']) for x in o['links']};saved_pairs={(x['historical_id'],x['modern_id']) for x in saved.get('comparisons',[])}
        require(pairs==saved_pairs,'Independent overlap differs: '+path)
        require(o.get('date_conflicts',0)==saved.get('date_conflicts',0) and o.get('score_conflicts',0)==saved.get('score_conflicts',0),'Overlap conflict totals differ')
    independent_membership={anchor:sorted(categories) for anchor,categories in queue.items()};saved_membership={r['conditional_event_anchor']:r['categories'] for r in old_q['items']}
    require(independent_membership==saved_membership,'Phase3 queue event/category membership differs')
    for item in old_q['items']:
        anchor=item['conditional_event_anchor']
        require(set(item['source_ids'])==set(event_members[anchor]),'Queue source bindings differ: '+anchor)
        own={(source_id,category) for category,ids in queue[anchor].items() for source_id in ids}
        saved={(x['source_id'],x['category']) for x in item['contexts']}
        require(own==saved,'Queue per-observation flag membership differs: '+anchor)
        for binding in item['bindings']:
            r=allrows.get(binding['audit_id'])
            require(r is not None and all(r[k]==binding[k] for k in ('source','source_sha256','source_line','home','away','stage')),'Queue binding payload differs')
            if r is not None:
                for k in ('FT','score','annotation','source_line_sha256'):
                    if k in r:require(r[k]==binding[k],'Queue score/annotation/line hash differs')
        for context in item['contexts']:
            if context['category']=='WIDE_ROUND':
                own=[x['context'] for x in contexts.get(anchor,[]) if x['source_id']==context['source_id'] and x['category']=='WIDE_ROUND']
                require(context['context'] in own,'Wide-round context differs')
    matrix=[]
    for y in range(1990,2026):
        season=f'{y}/{y+1}';h=hs.get(season);mm={path:m for path,m in modern.items() if m['declared_season']==season};saved=next(x for x in old_matrix if x['season']==season)
        require((h['observed'] if h else None)==(saved['historical']['observed'] if saved['historical'] else None),'Coverage historical census differs')
        require(set(mm)==set(saved['modern_sources']),'Coverage source-season attribution differs')
        require(saved['expected_clubs']==expected_clubs(y) and saved['nominal_regular_slots']==expected_clubs(y)*(expected_clubs(y)-1),'Coverage nominal expectation differs')
        for path,m in mm.items():require(m['assessment']['stage_counts']==saved['modern_sources'][path]['stage_counts'],'Coverage stage counts differ')
        matrix.append(dict(season=season,nominal_clubs=expected_clubs(y),nominal_regular_slots=expected_clubs(y)*(expected_clubs(y)-1),historical_observations=h['observed'] if h else 0,historical_clubs=h['clubs'] if h else None,historical_stage='UNKNOWN',modern_sources={path:dict(requested_season=m['requested_season'],declared_season=m['declared_season'],mismatch=m['path_season_mismatch'],stages=m['assessment']['stage_counts'],scored=m['assessment']['scored'],unscored=m['assessment']['unscored']) for path,m in mm.items()},dated_gap=y<1995,actual_modern_2021_22_unavailable=y==2021,eligibility='UNDECIDED',availability='NOT_CERTIFIED',licensing='NOT_CLEARED_FOR_TRAINING_OR_REDISTRIBUTION'))
    scored=sum(r['FT'] is not None for r in history)+sum(m['assessment']['scored'] for m in modern.values());total=len(history)+sum(len(m['observations']) for m in modern.values());matched=len(anchors);categories=Counter(cat for flags in queue.values() for cat in flags)
    counts=dict(historical=len(history),modern=total-len(history),observations=total,scored=scored,unscored=total-scored,matched_pairs=matched,conditional_events=total-matched,review_entries=len(queue),documentary_only_review_entries=len(documentary_exceptions),conditional_review_entries=len(queue)-len(documentary_exceptions),wide_round_contexts=sum(len(m['assessment']['wide_rounds']) for m in modern.values()))
    expected=dict(historical=8394,modern=1706,observations=10100,scored=9973,unscored=127,matched_pairs=1402,conditional_events=8698,review_entries=927,documentary_only_review_entries=30,conditional_review_entries=897,wide_round_contexts=15)
    require(counts==expected,'Approved population expectations differ; preserve actual counts')
    known_registry=[dict(kind='PATH_CONTENT_MISMATCH',source=path,requested=m['requested_season'],declared=m['declared_season'],source_ids=[r['audit_id'] for r in m['observations']]) for path,m in modern.items() if m['path_season_mismatch']]
    awards=[r for m in modern.values() for r in m['observations'] if 'awarded' in r['annotation']]
    cancelled=[r for m in modern.values() for r in m['observations'] if 'cancelled' in r['annotation']]
    rsssf=docs.get('tablesb/belg2010.html',[]);mouscron=Counter('NON_MOUSCRON' if 'Mouscron' not in r['home'] and 'Mouscron' not in r['away'] else 'ANNULLED_NUMERIC' if r['score'][0].isdigit() else r['score'] for r in rsssf)
    order_causes=Counter('STAGE_BLOCK_ORDER' if allrows[a]['stage']!=allrows[b]['stage'] else 'WITHIN_STAGE_SOURCE_ORDER' for m in modern.values() for a,b in m['assessment']['order_reversals'])
    return dict(zip(NAMES,[dict(phase=4,status='PASSED' if not defects else 'REQUIRES_CORRECTIVE_WORK',counts=counts,defects=defects,historical_seasons=hs,modern_sources={path:{k:v for k,v in m.items() if k!='observations'} for path,m in modern.items()},ordering_causes=dict(order_causes),historical_certification=False),dict(historical=history,modern={path:m['observations'] for path,m in modern.items()}),links,dict(registry=known_registry,awards=awards,cancellations=cancelled,mouscron_documentary_counts=dict(mouscron),documentary_regular=rsssf,documentary_exceptions=documentary_exceptions,lommel=dict(observations=hs['2002/2003']['observed'],clubs=hs['2002/2003']['clubs'],present=any('Lommel' in x for x in hs['2002/2003']['team_labels'])),no_dispositions=True),dict(counts=counts,category_counts=dict(sorted(categories.items())),items=[dict(anchor=k,categories={cat:sorted(ids) for cat,ids in sorted(flags.items())},bindings=[allrows[sid] for sid in event_members[k]]) for k,flags in sorted(queue.items())],phase3_membership_identical=independent_membership==saved_membership),dict(matrix=matrix,originals=provenance,independent_method='Own raw parsers and date/side-only label constraints; no previous parser/assessor/queue calls',future_schema='match_id,date,league,season,home_team,away_team,home_goals,away_goals',stage_audit_required=True,final_ids_created=False)]))


def generate(directory=PRIVATE,output=None):
    output=Path(output) if output else directory/'phase4';result=build(directory);output.mkdir(parents=True,exist_ok=True)
    objects={name:encode(obj) for name,obj in result.items()};objects['reproducibility.json']=encode(dict(artifacts={name:sha(raw) for name,raw in objects.items()}))
    for name,raw in objects.items():
        path=output/name
        if path.exists():
            if path.read_bytes()!=raw:raise ValueError('Saved Phase4 assessment differs: '+name)
        else:
            fd,temp=tempfile.mkstemp(dir=output,prefix='.pending-')
            try:
                with os.fdopen(fd,'wb') as stream:stream.write(raw)
                os.link(temp,path)
            finally:os.unlink(temp)
    return {name:sha(raw) for name,raw in objects.items()}


def verify(directory=PRIVATE):
    import sys
    from unittest.mock import patch
    hashes={}
    with tempfile.TemporaryDirectory(prefix='belgium-phase4-regenerate-') as temp:
        command=[sys.executable,'-B','-m','scripts.validate_belgian_pro_league_structure','--output',temp]
        result=subprocess.run(command,cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=90)
        if result.returncode:raise ValueError('Independent regeneration failed: '+result.stdout)
        for name in (*NAMES,'reproducibility.json'):
            saved=(directory/'phase4'/name).read_bytes();fresh=(Path(temp)/name).read_bytes()
            if saved!=fresh or sha(saved)!=sha(fresh):raise ValueError('Regeneration mismatch: '+name)
            hashes[name]=dict(bytes=len(saved),sha256=sha(saved),byte_identical=True)
    with patch('urllib.request.OpenerDirector.open',side_effect=AssertionError('Phase4 must be offline')):
        protection=protect(directory)
    return dict(phase=4,regeneration=hashes,protected=protection,network_requests=0)


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);p.add_argument('--verify',action='store_true');args=p.parse_args();print(json.dumps(verify() if args.verify else generate(output=args.output),indent=2))
