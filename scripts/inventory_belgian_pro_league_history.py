"""Phase 3 source inventory only. No screening or historical policy.

Sources are reparsed from immutable bytes; paths and declared seasons are separate.
"""
from collections import Counter, defaultdict
from pathlib import Path
from datetime import date
import json,re
from scripts import collect_belgian_pro_league_history as acquisition
from scripts import validate_belgian_pro_league_feasibility as v
c=acquisition.c
shared,fixture=v.shared,v.fixture
NAMES=('historical_inventory.json','modern_inventory.json','overlap_inventory.json','event_diagnostics.json','review_queue.json','coverage_matrix.json','source_manifest.json')

def parse_original(raw,year,receipt):
    if c.sha(raw)!=receipt['sha256']:raise ValueError('TXT checksum mismatch')
    rows=[];notes=[];current=None;stage=None;rnd=None;title=False;physical=raw.splitlines(keepends=True)
    stages={'Playoff I':'CHAMPIONSHIP','Championship':'CHAMPIONSHIP','Europe':'EUROPE','Relegation':'PLAYDOWNS','ECL Playoff':'EUROPE_QUALIFICATION'}
    for number,line in enumerate(raw.decode('utf-8-sig').splitlines(),1):
        text=line.strip()
        if not text:continue
        if text.startswith('#'):notes.append(dict(line=number,kind='COMMENT',text=text));continue
        if text.startswith('='):
            if title or text!=f'= Belgium First Division A {year}/{(year+1)%100:02}':raise ValueError('Wrong/duplicate title')
            title=True;notes.append(dict(line=number,kind='TITLE',text=text));continue
        if text.startswith('▪'):
            m=re.fullmatch(r'▪ (?:(Playoff I|Championship|Europe|Relegation), )?(?:Matchday (\d+)|(\d+)\. Round)',text)
            if m:
                stage=stages[m[1]] if m[1] else 'REGULAR_SEASON';rnd=int(m[2] or m[3])
                if not 1<=rnd<=((34 if 2020<=year<=2022 else 30) if stage=='REGULAR_SEASON' else 10):raise ValueError('Round outside source format')
            elif text=='▪ ECL Playoff, Final':stage='EUROPE_QUALIFICATION';rnd='Final'
            else:raise ValueError(f'Unknown stage heading at {number}: {text}')
            current=None;notes.append(dict(line=number,kind='STAGE_ROUND',stage=stage,round=rnd,text=text));continue
        parsed=shared.heading(text,year)
        if parsed:current=dict(parsed,heading_line=number);continue
        if not title or stage is None or current is None:raise ValueError(f'Fixture without context at {number}')
        body=re.sub(r'^\d{1,2}:\d{2}\s+','',text);r=fixture(body)
        r.update(season=f'{year}/{year+1}',date=current['date'],date_basis=current['date_basis'],date_heading=current['date_heading'],date_heading_line=current['heading_line'],date_semantics='SOURCE_HEADING_NOT_RESULT_AVAILABILITY_CERTIFICATION',stage=stage,round=rnd,group=None,leg=None,raw_record=line,field_issues=[])
        rows.append(shared.bound(r,receipt,number,number,physical[number-1]))
    if not title or not rows:raise ValueError('Empty/incomplete TXT original')
    # Comments are diagnostic assertions, not inputs driving fixture classification.
    declared=next((int(m[1]) for n in notes if (m:=re.fullmatch(r'# Matches\s+(\d+)',n['text']))),None)
    return rows,dict(notes=notes,declared_matches=declared,declared_count_matches=declared==len(rows))



def declared_year(raw):
    first=raw.decode('utf-8-sig').splitlines()[0]
    m=re.fullmatch(r'= Belgium First Division A (\d{4})/(\d{2})',first)
    if not m or int(m[2])!=(int(m[1])+1)%100:raise ValueError('Invalid season declaration')
    return int(m[1])


def build(directory=c.PRIVATE):
    old=c.verify_originals(directory);new=acquisition.verify_originals(directory)
    receipts=old['files']+new['files'];historical=[];modern={};rsssf={};by=defaultdict(list)
    for rec in receipts:
        raw=(directory/rec['path']).read_bytes()
        if rec['repository']==c.HIST:historical=v.parse_csv(raw,rec)
        elif rec['repository']==c.MODERN:
            y=declared_year(raw);rows,grammar=parse_original(raw,y,rec)
            modern[rec['original_path']]=dict(requested_season=rec['season'],declared_season=f'{y}/{y+1}',path_season_mismatch=rec['season']!=f'{y}/{y+1}',all_stages=v.assess(rows,y),stages={stage:v.assess([r for r in rows if r['stage']==stage],y) for stage in sorted({r['stage'] for r in rows})},grammar=grammar,observations=rows)
        else:rsssf[rec['original_path']]=v.rsssf(raw,rec)
    for r in historical:by[int(r['season'][:4])].append(r)
    hi={str(y):v.assess(rows,y) for y,rows in sorted(by.items())}
    overlap={};anchors={};event_bindings=defaultdict(list);allrows={r['audit_id']:r for r in historical}
    for path,m in sorted(modern.items()):
        y=int(m['declared_season'][:4]);rs=m['observations'];allrows.update({r['audit_id']:r for r in rs})
        o=v.overlap(by[y],rs) if by.get(y) else dict(status='NO_HISTORICAL_COUNTERPART',historical_observations=0,modern_observations=len(rs))
        o.update(requested_season=m['requested_season'],declared_season=m['declared_season'],path_season_mismatch=m['path_season_mismatch']);overlap[path]=o
        for pair in o.get('comparisons',[]):
            h,mo=pair['historical_id'],pair['modern_id']
            if h in anchors:raise ValueError('Historical representation linked twice')
            anchors[h]=mo
    for sid,r in sorted(allrows.items()):event_bindings[anchors.get(sid,sid)].append(sid)
    queue={}
    def flag(sid,category,context):
        key=anchors.get(sid,sid);q=queue.setdefault(key,dict(conditional_event_anchor=key,categories=set(),contexts=[],source_ids=event_bindings[key]))
        q['categories'].add(category)
        item=dict(source_id=sid,category=category,context=context)
        if item not in q['contexts']:q['contexts'].append(item)
    for y,h in hi.items():
        rs=by[int(y)];p=h['provisional_pairing_partition']
        if p['additional_observations']:
            for r in rs[p['candidate_regular']:]:flag(r['audit_id'],'HISTORICAL_STAGE_UNCERTAINTY','Additional prefix observations; source stage UNKNOWN')
    for rows,a in [(by[int(y)],h) for y,h in hi.items()]+[(m['observations'],m['all_stages']) for m in modern.values()]:
        for r in rows:
            if r['FT'] is None:flag(r['audit_id'],'UNSCORED_SOURCE_SLOT',r['annotation'] or 'No score; no final disposition')
            if r['annotation']:flag(r['audit_id'],'SOURCE_ANNOTATION',r['annotation'])
        for d in a['pairing_repeats']:
            for sid in d['source_ids']:flag(sid,'REPEATED_DIRECTED_PAIR',d['kind'])
        for d in a['unusual_scores']:flag(d['source_id'],'UNUSUAL_SCORE',d['FT'])
        for d in a['wide_rounds']:
            for sid in d['source_ids']:flag(sid,'WIDE_ROUND',dict(stage=d['stage'],round=d['round'],span_days=d['span_days'],earliest=d['earliest'],latest=d['latest']))
        for d in a['source_order_reversals']:
            flag(d['previous_id'],'SOURCE_ORDER_REVERSAL',d);flag(d['current_id'],'SOURCE_ORDER_REVERSAL',d)
        for d in a['invalid']:flag(d['source_id'],'STRUCTURAL_FIELD_CANDIDATE',d['issues'])
    for path,m in modern.items():
        if m['path_season_mismatch']:
            for r in m['observations']:flag(r['audit_id'],'PATH_DECLARED_SEASON_MISMATCH',dict(path=path,requested=m['requested_season'],declared=m['declared_season']))
        o=overlap[path]
        if o.get('comparisons'):
            for sid in o['unmatched_modern']:flag(sid,'UNMATCHED_MODERN_OBSERVATION',path)
            for sid in o['unmatched_historical']:flag(sid,'UNMATCHED_HISTORICAL_OBSERVATION',path)
            for d in o['comparisons']:
                if not d['date_equal'] or not d['score_equal']:flag(d['modern_id'],'OVERLAP_CONFLICT',d)
    # Documentary exceptions stay source-bound, never merged into CSV events.
    for path,doc in rsssf.items():
        rec=next(r for r in receipts if r['original_path']==path)
        for r in doc['fixture_line_candidates']:
            if r['stage']=='REGULAR_SEASON' and ('annulled' in r['annotation'] or r['score'] in ('awd','n/p')):
                sid=c.sha(c.encode([rec['sha256'],r['line'],'RSSSF_DOCUMENTARY']))
                allrows[sid]=dict(r,source=rec['path'],source_sha256=rec['sha256'],source_line=r['line'],audit_id=sid,season='2009/2010')
                event_bindings[sid]=[sid];flag(sid,'DOCUMENTARY_ADMINISTRATIVE_REPRESENTATION',r['annotation'] or r['score'])
    # Identity candidates are review metadata, not aliases or proof of continuity.
    labels=defaultdict(list)
    for sid,r in allrows.items():
        for side in ('home','away'):labels[r[side]].append(sid)
    identity={label:sorted(set(ids)) for label,ids in sorted(labels.items()) if re.search('Beerschot|Germinal|Mouscron|Moeskroen|Peruwelz|Molenbeek|RWDM|Genk|Truid|Trond|Kortr|Courtr',label,re.I)}
    items=[]
    for key,q in sorted(queue.items()):
        q['categories']=sorted(q['categories']);q['bindings']=[allrows[sid] for sid in q['source_ids']];items.append(q)
    category=Counter(cat for q in items for cat in q['categories']);case_reviews=[dict(case='LOMMEL_2002_03',csv_observations=len(by[2002]),csv_clubs=hi['2002']['clubs'],absent_label='Lommel',status='MISSING_ADMINISTRATIVE_POPULATION_NOT_RECONSTRUCTED'),dict(case='MOUSCRON_2009_10',csv_observations=len(by[2009]),rsssf_regular_slots=240,status='DOCUMENTARY_REPRESENTATIONS_SEPARATE_FROM_CSV'),dict(case='REQUESTED_2021_22',status='APPROVED_PATH_CONTAINS_DECLARED_2020_21; NO_MODERN_2021_22_COUNTERPART')]
    matrix=[]
    for y in range(1990,2026):
        relevant={path:m for path,m in modern.items() if m['declared_season']==f'{y}/{y+1}'}
        matrix.append(dict(season=f'{y}/{y+1}',expected_clubs=v.expected_clubs(y),nominal_regular_slots=v.expected_clubs(y)*(v.expected_clubs(y)-1),historical=hi.get(str(y)),modern_sources={path:dict(requested_season=m['requested_season'],declared_season=m['declared_season'],path_season_mismatch=m['path_season_mismatch'],all_stages=m['all_stages'],stage_counts=m['all_stages']['stage_counts']) for path,m in relevant.items()},overlaps={path:o for path,o in overlap.items() if o['declared_season']==f'{y}/{y+1}'},gap='NO_ACQUIRED_DATED_SOURCE' if y<1995 else None,requested_modern_missing=y==2021,eligibility='UNDECIDED; NO_SCREENING',rights='NOT_CLEARED_FOR_TRAINING_OR_REDISTRIBUTION'))
    return dict(zip(NAMES,[dict(observed=len(historical),schema=list(v.CSV_COLUMNS),seasons=hi,observations=historical),modern,overlap,dict(conditional_events=[dict(anchor=k,source_ids=ids) for k,ids in sorted(event_bindings.items()) if k in allrows and 'FT' in allrows[k]],match_source_observations=sum(len(by[y]) for y in by)+sum(len(m['observations']) for m in modern.values()),matched_representation_pairs=len(anchors),conditional_match_events=len(historical)+sum(len(m['observations']) for m in modern.values())-len(anchors),identity_candidates=identity,identity_rule='Diagnostic only; season/stage/round/leg/date/literal teams; source SHA+line remains separate'),dict(fixture_events=len(items),conditional_match_events=sum('FT' in allrows[q['source_ids'][0]] for q in items),documentary_only_events=sum('FT' not in allrows[q['source_ids'][0]] for q in items),category_counts=dict(sorted(category.items())),items=items,case_reviews=case_reviews,rsssf_capabilities=rsssf),matrix,dict(originals=receipts,phase=3,original_count=len(receipts),rights=c.RIGHTS,policy='NO_FINAL_STAGE_POLICY_NO_DISPOSITIONS_NO_STANDARDIZATION')]))


def generate(directory=c.PRIVATE,output=None):
    output=Path(output) if output else directory/'phase3';out=build(directory)
    for name,value in out.items():c.keep(output/name,c.encode(value))
    hashes={n:c.sha(c.encode(value)) for n,value in out.items()};c.keep(output/'reproducibility.json',c.encode(dict(artifacts=hashes)));return hashes


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);args=p.parse_args();print(generate(output=args.output))
