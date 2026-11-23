"""Phase 3 source inventory with independent raw parsers; no historical policy."""
import argparse,calendar,csv,io,json,re
from collections import Counter,defaultdict
from copy import deepcopy
from datetime import date
from pathlib import Path
from scripts import collect_primeira_liga_history as acquisition
from scripts import validate_primeira_liga_feasibility as feasibility
c=acquisition.c
ROOT,PRIVATE=c.ROOT,c.PRIVATE
NAMES=('phase3_historical_inventory.json','phase3_modern_inventory.json','phase3_coverage_matrix.json','phase3_overlap_registry.json','phase3_review_candidates.json','phase3_feirense_diagnostic.json','phase3_early_coverage_gap.json','phase3_identity_inventory.json')


def bind(fields,receipt,start,end,literal):
    return dict(fields,source=receipt['path'],source_sha256=receipt['sha256'],source_line=start,source_end_line=end,physical_record_sha256=c.sha(literal),audit_id=c.sha(c.encode([receipt['sha256'],start,end])),provenance={k:receipt[k] for k in ('commit','git_blob_sha1','url')})


def historical(raw,receipt):
    if c.sha(raw)!=receipt['sha256']:raise ValueError('Historical checksum differs')
    physical=raw.splitlines(keepends=True);reader=csv.reader(io.StringIO(raw.decode('utf-8-sig'),newline=''),strict=True)
    columns=next(reader)
    if columns!=['Date','Season','home','visitor','FT','hgoal','vgoal','division','tier','totgoal','goaldif','result']:raise ValueError('Unexpected exact Portugal schema')
    records=[]
    while True:
        start=reader.line_num+1
        try:cells=next(reader)
        except StopIteration:break
        if len(cells)!=12:raise ValueError('Malformed CSV width at '+str(start))
        d,year,home,away,ft,hg,ag,div,tier,total,diff,outcome=cells;issues=[]
        if not re.fullmatch(r'\d{4}',year):raise ValueError('Unknown season at '+str(start))
        if div!='P1' or tier!='1':issues.append('WRONG_COMPETITION')
        try:
            if date.fromisoformat(d).isoformat()!=d:raise ValueError('Noncanonical day')
        except ValueError:issues.append('INVALID_DATE')
        if not re.fullmatch(r'0|[1-9]\d*',hg) or not re.fullmatch(r'0|[1-9]\d*',ag):issues.append('INVALID_SCORE')
        else:
            hi,ai=int(hg),int(ag)
            if ft!=f'{hi}-{ai}':issues.append('FT_CONTRADICTION')
            if total!=str(hi+ai) or diff!=str(hi-ai):issues.append('GOAL_DERIVED_CONTRADICTION')
            if outcome!=('H' if hi>ai else 'A' if hi<ai else 'D'):issues.append('OUTCOME_CONTRADICTION')
        fields=dict(season=f'{year}/{int(year)+1}',date=d,home=home,away=away,hg=hg or None,ag=ag or None,FT=ft or None,HT=None,annotation='',round=None,stage='HISTORICAL_P1_TIER1_STAGE_NOT_EXPLICIT',original_fields=dict(zip(columns,cells)),field_issues=issues,date_semantics='SOURCE_DATE_NOT_VERIFIED_AVAILABILITY',date_basis='EXPLICIT_ISO_DATE',year_explicit=True)
        records.append(bind(fields,receipt,start,reader.line_num,b''.join(physical[start-1:reader.line_num])))
    return records


def modern(raw,year,receipt):
    if c.sha(raw)!=receipt['sha256']:raise ValueError('Modern checksum differs')
    months={m:i for i,m in enumerate(calendar.month_abbr) if m};end=date(2020,8,2) if year==2019 else date(year+1,6,30)
    rows=[];notes=[];current=None;rnd=None;stage=None;title=False;repeated=Counter();depth=0
    for number,literal in enumerate(raw.splitlines(keepends=True),1):
        line=literal.decode('utf-8-sig').rstrip('\r\n');t=line.strip()
        if not t:continue
        if t.startswith('#'):notes.append(dict(line=number,kind='COMMENT',text=t));continue
        if depth or t.startswith('('):
            if not rows:raise ValueError('Detail without fixture')
            depth+=t.count('(')-t.count(')')
            if depth<0:raise ValueError('Unbalanced detail')
            notes.append(dict(line=number,kind='DETAIL',text=t));continue
        if t.startswith('='):
            if title or t!=f'= Portuguese Primeira Liga {year}/{(year+1)%100:02}':raise ValueError('Wrong title')
            title=True;notes.append(dict(line=number,kind='TITLE',text=t));continue
        if t.startswith('▪'):
            m=re.fullmatch(r'▪ Matchday (\d+)',t)
            if m:
                rnd=int(m[1]);stage='REGULAR_SEASON'
                if not 1<=rnd<=34:raise ValueError('Round outside format')
                repeated[rnd]+=1
            elif re.search(r'play.?off|cup|final|promotion',t,re.I):stage='OTHER_STAGE';rnd=t
            else:raise ValueError('Unknown round/stage')
            current=None;notes.append(dict(line=number,kind='ROUND',text=t));continue
        m=re.fullmatch(r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun) ([A-Z][a-z]{2}) (\d{1,2})(?: (\d{4}))?',t)
        if m:
            dates=[]
            for y in [int(m[4])] if m[4] else [year,year+1]:
                try:d=date(y,months[m[2]],int(m[3]))
                except (KeyError,ValueError):continue
                if date(year,7,1)<=d<=end and calendar.day_abbr[d.weekday()]==m[1]:dates.append(d.isoformat())
            if len(dates)!=1:raise ValueError('Invalid/ambiguous heading at '+str(number))
            current=dict(date=dates[0],date_heading=t,date_heading_line=number,date_basis='EXPLICIT_DAY_MONTH_YEAR_WEEKDAY' if m[4] else 'EXPLICIT_DAY_MONTH_WITH_SEASON_WEEKDAY_YEAR_RESOLUTION',year_explicit=bool(m[4]));continue
        if not title or current is None or stage is None:raise ValueError('Missing fixture context')
        body=re.sub(r'^\d{1,2}:\d{2}\s+','',t);annotation='';note=re.search(r'\s+(\[[^\]]+\])$',body)
        if note:annotation=note[1];body=body[:note.start()].rstrip()
        m=re.fullmatch(r'(.+?)\s+v\s+(.+?)\s{2,}(\d+)-(\d+)(?:\s+\((\d+-\d+)\))?',body)
        if m:home,away,hg,ag,ht=m.groups();ft=f'{hg}-{ag}'
        else:
            parts=re.split(r'\s+v\s+',body)
            if len(parts)!=2 or re.search(r'\d\s*[-:]|\?\s*[-:]|[-:]\s*\d',parts[-1]):raise ValueError('Unknown/partial fixture at '+str(number))
            home,away=parts;hg=ag=ht=ft=None
        fields=dict(current,season=f'{year}/{year+1}',home=home,away=away,hg=hg,ag=ag,FT=ft,HT=ht,annotation=annotation,round=rnd,stage=stage,raw_record=line,date_semantics='SOURCE_DAY_HEADING_NOT_AVAILABILITY_CERTIFICATION')
        rows.append(bind(fields,receipt,number,number,literal))
    if not title or not rows or depth:raise ValueError('Incomplete original grammar')
    return rows,dict(notes=notes,repeated_round_headings={str(k):v for k,v in sorted(repeated.items()) if v>1})


def summarize(rows,year):
    result=feasibility.assess(rows,year)
    result['field_issues']=[dict(id=r['audit_id'],issues=r['field_issues']) for r in rows if r.get('field_issues')]
    result['round_counts']=dict(sorted(Counter(str(r['round']) for r in rows if r['round'] is not None).items()))
    result['malformed_observations']=len({x['id'] for x in result['invalid']+result['field_issues']})
    return result


def whitespace_diagnostic(rows):
    literal=[r for r in rows if r['season']=='2011/2012'];targets=[r for r in literal if r['date']=='2011-08-14' and r['home']=='Feirense ' and r['away']=='Nacional']
    if len(targets)!=1:raise ValueError('Frozen Feirense anomaly selector differs')
    hypothetical=deepcopy(literal)
    for r in hypothetical:
        if r['audit_id']==targets[0]['audit_id']:r['home']='Feirense'
    original=summarize(literal,2011);diagnostic=summarize(hypothetical,2011)
    if len(hypothetical)!=len(literal) or len({r['audit_id'] for r in hypothetical})!=len(literal):raise ValueError('Whitespace diagnostic loses observations')
    return dict(original_observation=targets[0],literal=original,hypothetical_whitespace_only=diagnostic,scope='Only the exact selected source ID; not source mutation, approved alias or final standardized identity',related_observations=[r for r in literal if r['home'] in {'Feirense','Feirense '} or r['away'] in {'Feirense','Feirense '}])


def build(directory=PRIVATE,root=ROOT):
    protected=acquisition.protect(directory,root);old=c.verify_originals(directory);new=acquisition.verify_originals(directory)
    hr=next(r for r in old['files'] if r['repository']==c.HIST);hs=historical((directory/hr['path']).read_bytes(),hr);grouped=defaultdict(list)
    for r in hs:grouped[int(r['season'][:4])].append(r)
    hist=[dict(receipt=hr,records=rs,assessment=summarize(rs,y)) for y,rs in sorted(grouped.items())]
    modern_sources=[]
    for rec in sorted([r for r in old['files']+new['files'] if r['repository']==c.MODERN],key=lambda r:r['season']):
        y=int(rec['season'][:4]);rs,notes=modern((directory/rec['path']).read_bytes(),y,rec);modern_sources.append(dict(receipt=rec,records=rs,assessment=summarize(rs,y),notes=notes))
    overlaps=[feasibility.identity_overlap(grouped[int(s['receipt']['season'][:4])],s['records']) for s in modern_sources if int(s['receipt']['season'][:4]) in grouped]
    hby={s['assessment']['season']:s for s in hist};mby={s['assessment']['season']:s for s in modern_sources};oby={o['season']:o for o in overlaps};coverage=[]
    for y in range(1990,2026):
        label=f'{y}/{y+1}';h=hby.get(label);m=mby.get(label);o=oby.get(label);n=20 if y==1990 else 16 if 2006<=y<=2013 else 18
        coverage.append(dict(season=label,expected_clubs=n,expected_regular_slots=n*(n-1),historical_observations=h['assessment']['observed'] if h else 0,modern_observations=m['assessment']['observed'] if m else 0,matched_overlap_pairs=o['comparison_pairs'] if o else 0,conditional_distinct_slots=(h['assessment']['observed'] if h else 0)+(m['assessment']['observed'] if m else 0)-(o['comparison_pairs'] if o else 0),status='BOTH_SOURCES' if h and m else 'HISTORICAL_ONLY' if h else 'MODERN_ONLY' if m else 'NO_APPROVED_DATED_SOURCE',date_conflicts=sum(not p['date_equal'] for p in o['comparisons']) if o else 0,score_conflicts=sum(not p['score_equal'] for p in o['comparisons']) if o else 0,warning='Inventory identity under scoped diagnostic correspondences, not accepted/screened or certified fixtures'))
    allrows=hs+[r for s in modern_sources for r in s['records']];lookup={r['audit_id']:r for r in allrows}
    if len(lookup)!=len(allrows):raise ValueError('Repeated source identity')
    queue={}
    def flag(key,category):
        if key not in lookup:raise ValueError('Unbound anomaly')
        entry=queue.setdefault(key,dict(original=lookup[key],categories=[]))
        if category not in entry['categories']:entry['categories'].append(category)
    for s in hist+modern_sources:
        a=s['assessment']
        for x in a['invalid']+a['field_issues']:flag(x['id'],'SOURCE_FIELD_OR_LABEL')
        for w in a['wide_rounds']:
            for key in w['fixture_ids']:flag(key,'WIDE_ROUND')
        for rev in a['source_order_reversals']:
            flag(rev['previous_id'],'SOURCE_ORDER_REVERSAL');flag(rev['current_id'],'SOURCE_ORDER_REVERSAL')
        for x in a['unusual_scores']:flag(x['id'],'UNUSUAL_SCORE')
        for x in a['annotations']:flag(x['id'],'SOURCE_ANNOTATION')
        for r in s['records']:
            if r['hg'] is None:flag(r['audit_id'],'UNSCORED')
    conflicts=[]
    for o in overlaps:
        for p in o['comparisons']:
            if not p['date_equal'] or not p['score_equal']:
                conflicts.append(dict(p,season=o['season'],historical_original=lookup[p['historical_id']],modern_original=lookup[p['modern_id']],decision='NOT_DECIDED'))
                for key in ('historical_id','modern_id'):flag(p[key],'SOURCE_DISAGREEMENT')
    bel=[r for r in allrows if r['season']=='2021/2022' and r['date']=='2021-11-27' and (r['home'],r['away']) in {('Belenenses','Benfica'),('Belenenses SAD','SL Benfica')}]
    if len(bel)!=2:raise ValueError('Belenenses exception binding differs')
    for r in bel:flag(r['audit_id'],'KNOWN_ABANDONMENT_REQUIRES_REVIEW')
    candidates=sorted(queue.values(),key=lambda x:(x['original']['source'],x['original']['source_line']))
    early=dict(seasons=[x for x in coverage if x['status']=='NO_APPROVED_DATED_SOURCE'],expected_missing_source_slots=sum(x['expected_regular_slots'] for x in coverage if x['status']=='NO_APPROVED_DATED_SOURCE'),rsssf='Unchanged Phase2 snapshot: 380 undated score identities; not included in dated observation totals',recommendation='Separately authorize bounded discovery of permitted dated official/club or historical-provider evidence; no acquisition approved here',not_not_played=True)
    labels=defaultdict(lambda:defaultdict(list))
    for r in allrows:
        for role in ('home','away'):labels[r[role]][r['season']].append(dict(source_id=r['audit_id'],role=role,source=r['source'],line=r['source_line']))
    identities=dict(phase=3,literal_labels=[dict(label=label,seasons=[dict(season=season,occurrences=items) for season,items in sorted(seasons.items())]) for label,seasons in sorted(labels.items())],season_participants=[dict(source=x['receipt']['path'],season=x['assessment']['season'],literal_clubs=x['assessment']['team_labels'],reserve_labels=x['assessment']['reserve_labels'],casefold_collisions=x['assessment']['casefold_collisions']) for x in hist+modern_sources],risks=['Belenenses versus Belenenses SAD/B-SAD continuity not approved','Benfica/Porto/Sporting senior versus B sides remain distinct','Vitoria SC/Guimaraes versus Vitoria FC/Setubal remain distinct','AVS and Aves not merged','Gil Vicente/Boavista administrative context not a score correction','Leiria, Madeira/Nacional, Chaves/Desp. Chaves, Campomaior/Campomaiorense and Estrela continuity require historical evidence','Accents/abbreviations/whitespace preserved; no global normalization'],diagnostic_mapping_scope='Only explicit overlap season links; no entity continuity approval')
    return dict(zip(NAMES,[dict(phase=3,total_records=len(hs),seasons=hist,protected=protected),dict(phase=3,total_records=sum(len(s['records']) for s in modern_sources),seasons=modern_sources),dict(phase=3,seasons=coverage,totals=dict(expected=sum(x['expected_regular_slots'] for x in coverage),historical=len(hs),modern=sum(len(s['records']) for s in modern_sources),overlap=sum(x['comparison_pairs'] for x in overlaps),conditional_distinct=sum(x['conditional_distinct_slots'] for x in coverage),missing_early_expected=early['expected_missing_source_slots'])),dict(phase=3,seasons=overlaps,conflicts=conflicts,upstream_independence='UNESTABLISHED'),dict(phase=3,distinct_flagged_source_observations=len(candidates),category_counts=dict(Counter(k for x in candidates for k in x['categories'])),records=candidates,belenenses=dict(originals=bel,reported_vs_official_finality='UNKNOWN; no disposition',evidence_leads=['https://www.fpf.pt/DownloadDocument.ashx?id=20842','https://www.fpf.pt/DownloadDocument.ashx?id=21435'],lead_status='Phase1 documentary/index leads; not newly acquired or independently certified',effective_availability=None),identity_risks='Preserve Belenenses/SAD, senior/B sides, Vitoria SC/FC, AVS/Aves, Gil Vicente/Boavista administrative and historical label continuity questions; no global aliases'),whitespace_diagnostic(hs),early,identities]))


if __name__=='__main__':
    for n,obj in build().items():c.keep(PRIVATE/n,c.encode(obj))
    print('VERIFIED_PHASE3_INVENTORY')
