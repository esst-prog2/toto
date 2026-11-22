"""Phase 4 independent offline raw-source validation and review queues.

No acquisition, correction, eligibility policy, standardization or model use.
Parsers below do not call the Phase 2/3 parsers. Source observations are immutable.
"""
import argparse
from collections import Counter, defaultdict
import csv
from datetime import date
import io
import json
import re
import unicodedata

from scripts import collect_ligue1_feasibility as base
from scripts import collect_ligue1_history as acquisition
from scripts import validate_ligue1_feasibility as metadata

ROOT, PRIVATE = base.ROOT, base.PRIVATE
BASELINE = 'phase4_protected_before.json'
REPORT = 'phase4_structural_validation.json'
QUEUE = 'phase4_review_queue.json'
PUBLIC = ('scripts/collect_ligue1_feasibility.py','scripts/validate_ligue1_feasibility.py',
          'tests/test_ligue1_feasibility.py','docs/ligue-1-feasibility.md',
          'scripts/collect_ligue1_history.py','scripts/inventory_ligue1_history.py',
          'tests/test_ligue1_history.py','docs/ligue-1-inventory.md')
MONTHS = {m:i+1 for i,m in enumerate('Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split())}
DAYS = 'Mon Tue Wed Thu Fri Sat Sun'.split()


def initialize(directory=PRIVATE, root=ROOT):
    if (directory/BASELINE).exists():return protect(directory,root)
    acquisition.protect(directory,root)
    final=json.loads((directory/'phase3_final_verification.json').read_bytes())
    for name,record in final['new_private_files_before_this_receipt'].items():
        if base.sha((directory/name).read_bytes())!=record['sha256']:raise ValueError('Approved Phase 3 evidence changed: '+name)
    for name,digest in final['public_files'].items():
        if base.sha((root/name).read_bytes())!=digest:raise ValueError('Approved Phase 3 public file changed: '+name)
    files={str(p.relative_to(root)):base.sha(p.read_bytes()) for p in directory.rglob('*') if p.is_file()}
    files.update({n:base.sha((root/n).read_bytes()) for n in PUBLIC})
    log=(root/'PLANNING_LOG.md').read_bytes()
    base.save(directory/BASELINE,base.encode(dict(files=files,planning_log=dict(bytes=len(log),sha256=base.sha(log)))))
    return protect(directory,root)


def protect(directory=PRIVATE,root=ROOT):
    prior=acquisition.protect(directory,root);saved=json.loads((directory/BASELINE).read_bytes())
    if not saved['files']:raise ValueError('Empty Phase 4 baseline')
    for name,digest in saved['files'].items():
        path=root/name
        if not path.resolve().is_relative_to(root.resolve()) or base.sha(path.read_bytes())!=digest:
            raise ValueError('Frozen Phase 2–3 artifact changed: '+name)
    log=(root/'PLANNING_LOG.md').read_bytes();prefix=saved['planning_log']
    if len(log)<prefix['bytes'] or base.sha(log[:prefix['bytes']])!=prefix['sha256']:raise ValueError('Planning prefix changed')
    return dict(previous=prior,phase2_3_entries=len(saved['files']))


def source_id(path,sha,line):
    return 'ligue1:'+base.sha(base.encode(dict(source=path,sha256=sha,line=line)))


def bind(record,path,digest,raw_lines):
    line=record['source_line'];start=record.get('source_start_line',line)
    raw=b''.join(raw_lines[start-1:line])
    record.update(source=path,source_sha256=digest,audit_id=source_id(path,digest,line),raw_line_sha256=base.sha(raw))
    return record


def read_csv(raw,path,digest):
    text=raw.decode('utf-8-sig');physical=raw.splitlines(keepends=True)
    reader=csv.DictReader(io.StringIO(text,newline=''),strict=True)
    required={'Date','Season','home','visitor','FT','hgoal','vgoal','division','tier','totgoal','goaldif','result'}
    if set(reader.fieldnames or ())!=required or len(reader.fieldnames)!=len(required):raise ValueError('Unexpected CSV schema')
    rows=[];previous=reader.line_num
    for r in reader:
        start=previous+1;previous=reader.line_num
        if None in r or any(v is None for v in r.values()):raise ValueError(f'CSV row shape at line {previous}')
        if not re.fullmatch(r'\d{4}',r['Season']):raise ValueError(f'Unassignable source season at line {previous}')
        year=int(r['Season']);record=dict(source_line=previous,source_start_line=start,source_fields=r,
            raw_record=b''.join(physical[start-1:previous]).decode('utf-8-sig').rstrip('\r\n'),
            season=f'{year}/{year+1}',date=r['Date'],home=r['home'],away=r['visitor'],hg=r['hgoal'],ag=r['vgoal'],
            FT=r['FT'],HT=None,round=None,stage='CSV_TIER1_STAGE_UNDOCUMENTED' if r['tier']=='1' and r['division'] in ('1','F1') else 'OTHER_OR_UNKNOWN_COMPETITION',
            annotation='',date_basis='EXPLICIT_ISO_SOURCE_FIELD_UNCERTIFIED_EVENT_DATE')
        rows.append(bind(record,path,digest,physical))
    return rows


def read_text(raw,year,path,digest):
    physical=raw.splitlines(keepends=True);rows=[];notes=[];current=None;stage=None;round_id=None;title=False;depth=0
    for number,line in enumerate(raw.decode('utf-8-sig').splitlines(),1):
        s=line.strip()
        if not s:continue
        def fail(reason):raise ValueError(f'{path}:{number}: {reason}: {s}')
        if depth or s.startswith('('):
            if not rows:fail('scorer note without fixture')
            depth+=s.count('(')-s.count(')')
            if depth<0:fail('unbalanced scorer note')
            notes.append(dict(line=number,kind='SCORER_NOTE',text=s));continue
        if s.startswith('#'):
            notes.append(dict(line=number,kind='COMMENT',text=s));continue
        if s.startswith('='):
            m=re.search(r'(\d{4})/(\d{2,4})',s)
            if title or not re.search(r'\bLigue 1\b',s) or not m or int(m[1])!=year or int(m[2])%100!=(year+1)%100:fail('wrong competition/season')
            title=True;notes.append(dict(line=number,kind='TITLE',text=s));continue
        if s.startswith('▪'):
            label=s[1:].strip();m=re.fullmatch(r'(?:Matchday|Regular Season -) (\d+)',label)
            if m:
                stage='REGULAR_SEASON';round_id=int(m[1])
                if not 1<=round_id<=2*((18 if year>=2023 else 20)-1):fail('round outside competition format')
            elif re.search(r'play.?off|promotion|final',label,re.I):stage='OTHER_STAGE';round_id=label
            else:fail('unknown stage')
            current=None;notes.append(dict(line=number,kind='ROUND',text=s));continue
        dm=re.fullmatch(r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun) ([A-Z][a-z]{2}) (\d{1,2})(?: (\d{4}))?',s)
        if dm:
            candidates=[]
            for y in (int(dm[4]),) if dm[4] else (year,year+1):
                try:d=date(y,MONTHS[dm[2]],int(dm[3]))
                except (ValueError,KeyError):continue
                if date(year,7,1)<=d<=date(year+1,6,30) and DAYS[d.weekday()]==dm[1]:candidates.append(d.isoformat())
            if len(candidates)!=1:fail('invalid/ambiguous calendar heading')
            current=dict(date=candidates[0],date_heading=s,date_heading_line=number,year_explicit=bool(dm[4]),
                         date_basis='EXPLICIT_DAY_MONTH_AND_YEAR' if dm[4] else 'EXPLICIT_DAY_MONTH_SEASON_WEEKDAY_YEAR')
            continue
        if not title or stage is None or current is None:fail('fixture without competition/round/date')
        kickoff=re.match(r'^(\d{1,2}:\d{2})\s+',s);body=s[kickoff.end():] if kickoff else s
        annotation='';tail=re.search(r'\s+(\[[^\]]+\])\s*$',body)
        if tail:annotation=tail[1];body=body[:tail.start()].rstrip()
        if re.search(r'\s+v\s+',body):
            home,rest=re.split(r'\s+v\s+',body,maxsplit=1)
            score=re.fullmatch(r'(.+?)\s{2,}(\d+)-(\d+)(?:\s+\((\d+-\d+)\))?',rest)
            if score:away,hg,ag,ht=score.groups()
            else:
                if re.search(r'\d\s*[-:]|\?\s*[-:]|[-:]\s*\d',rest):fail('malformed/partial score')
                away=rest;hg=ag=ht=None
        else:
            score=re.fullmatch(r'(.+?)\s{2,}(\d+)-(\d+)(?:\s+\((\d+-\d+)\))?\s{2,}(.+?)',body)
            if not score:fail('unknown fixture syntax')
            home,hg,ag,ht,away=score.groups()
        record=dict(current,source_line=number,raw_record=line,season=f'{year}/{year+1}',home=home,away=away,
                    hg=hg,ag=ag,FT=f'{hg}-{ag}' if hg is not None else None,HT=ht,stage=stage,round=round_id,
                    annotation=annotation,source_kickoff_time=kickoff[1] if kickoff else None)
        rows.append(bind(record,path,digest,physical))
    if depth or not rows or not title:raise ValueError('Unterminated/missing fixture content: '+path)
    return rows,notes


def integer(value):
    if value is None or value in ('','NA'):return None
    if not isinstance(value,str) or not re.fullmatch(r'[0-9]+',value):raise ValueError('Invalid goal token')
    return int(value)


def inspect_record(record):
    flags=set();malformed=[];label_defect=False;h=a=None;year=int(record['season'][:4])
    for name in (record['home'],record['away']):
        if not name.strip() or name!=name.strip() or '\ufffd' in name or any(ord(x)<32 for x in name):malformed.append('INVALID_TEAM_LABEL')
    if record['home']==record['away']:malformed.append('SELF_FIXTURE')
    try:
        d=date.fromisoformat(record['date'])
        if d.isoformat()!=record['date']:raise ValueError()
        if not date(year,7,1)<=d<=date(year+1,6,30):flags.add('SOURCE_DATE_OUTSIDE_CONVENTIONAL_SEASON')
    except (ValueError,TypeError):malformed.append('INVALID_DATE')
    try:
        h,a=integer(record['hg']),integer(record['ag'])
        if (h is None)!=(a is None):raise ValueError()
        if h is not None and record['FT']!=f'{h}-{a}':malformed.append('FT_GOAL_CONFLICT')
    except (ValueError,TypeError):malformed.append('INVALID_GOALS')
    derived=None if h is None or a is None else 'H' if h>a else 'A' if h<a else 'D'
    if derived is not None:
        fields=record.get('source_fields')
        if fields:
            if fields['result']!=derived:label_defect=True;flags.add('SYSTEMATIC_SOURCE_LABEL_DEFECT')
            if fields['totgoal']!=str(h+a) or fields['goaldif']!=str(h-a):malformed.append('NUMERIC_DERIVED_FIELD_CONFLICT')
        if max(h,a)>=7 or h+a>=10:flags.add('UNUSUAL_SCORE')
        if record['HT'] is not None:
            ht=re.fullmatch(r'(\d+)-(\d+)',record['HT'])
            if not ht or int(ht[1])>h or int(ht[2])>a:malformed.append('HALFTIME_FT_CONFLICT')
    if record['stage'] not in ('REGULAR_SEASON','CSV_TIER1_STAGE_UNDOCUMENTED'):flags.add('UNCONFIRMED_COMPETITION_STAGE')
    cancelled='cancelled' in record['annotation'].lower()
    if cancelled:
        flags.add('CANCELLED_UNPLAYED_SLOT')
        if derived is not None:malformed.append('CANCELLED_WITH_SCORE')
    elif derived is None:flags.add('UNEXPLAINED_MISSING_SCORE')
    if 'award' in record['annotation'].lower():flags.add('SOURCE_MARKED_ADMINISTRATIVE')
    flags.update(malformed)
    classification=('MALFORMED_OR_NUMERIC_CONFLICT' if malformed else 'CANCELLED_UNSCORED' if cancelled else
                    'INCOMPLETE_UNEXPLAINED' if derived is None else 'SOURCE_LABEL_INCONSISTENT' if label_defect else 'CONSISTENT_SCORE_FIELDS')
    return dict(classification=classification,malformed_reasons=sorted(set(malformed)),goal_derived_outcome=derived,
                flags=sorted(flags),source_result=record.get('source_fields',{}).get('result'),
                chronology=dict(source_date=record['date'],scheduled_date=record['date'] if cancelled else None,
                    independently_supported_kickoff=None,independently_supported_completion=None,administrative_decision_date=None,
                    effective_result_availability=None,status='POLICY_NOT_DECIDED; source date is not certified result availability'))


def clubs(year):return 18 if 1997<=year<=2001 or year>=2023 else 20


def season_report(records,year):
    names=sorted({r[k] for r in records for k in ('home','away')});pairs=defaultdict(list);events=defaultdict(list)
    for r in records:
        pairs[r['home'],r['away']].append(r['audit_id'])
        for k in ('home','away'):events[r['date'],r[k]].append(r['audit_id'])
    collisions=[dict(date=d,team=t,ids=ids) for (d,t),ids in sorted(events.items()) if len(ids)>1]
    duplicate=[dict(home=h,away=a,ids=ids) for (h,a),ids in sorted(pairs.items()) if len(ids)>1]
    for item in duplicate:
        for r in records:
            if r['audit_id'] in item['ids']:r['assessment']['flags'].append('DUPLICATE_DIRECTED_PAIR')
    for item in collisions:
        for r in records:
            if r['audit_id'] in item['ids']:r['assessment']['flags'].append('SAME_TEAM_DATE_COLLISION')
    normalized=defaultdict(list)
    for n in names:normalized[unicodedata.normalize('NFC',n).casefold()].append(n)
    name_collisions={k:v for k,v in normalized.items() if len(v)>1}
    for r in records:
        if any(r[k] in sum(name_collisions.values(),[]) for k in ('home','away')):r['assessment']['flags'].append('NORMALIZED_LABEL_COLLISION')
    rounds=defaultdict(list);wide=[]
    for r in records:
        if r['round'] is not None and r['stage']=='REGULAR_SEASON':rounds[r['round']].append(r)
    for rnd,rs in sorted(rounds.items()):
        ds=sorted(r['date'] for r in rs);span=(date.fromisoformat(ds[-1])-date.fromisoformat(ds[0])).days
        if span>14:
            ref=f'WIDE:{year}:{rnd}'
            wide.append(dict(id=ref,round=rnd,first_date=ds[0],last_date=ds[-1],span_days=span,
                             affected_ids=[r['audit_id'] for r in rs],date_scope='CANCELLED_SCHEDULE_ONLY' if all(r['FT'] is None for r in rs) else 'SOURCE_DATES_NOT_COMPLETION_CERTIFICATION'))
            for r in rs:r['assessment']['flags'].append('WIDE_ROUND_SPAN');r.setdefault('review_refs',[]).append(ref)
    appearance={n:dict(home=sum(r['home']==n for r in records),away=sum(r['away']==n for r in records)) for n in names}
    expected=clubs(year)*(clubs(year)-1)
    round_errors={str(k):dict(observed=len(rs),expected=clubs(year)//2) for k,rs in rounds.items() if len(rs)!=clubs(year)//2}
    missing_rounds=sorted(set(range(1,2*(clubs(year)-1)+1))-set(rounds)) if rounds else []
    for r in records:
        if str(r['round']) in round_errors:r['assessment']['flags'].append('ROUND_ALLOCATION_REVIEW')
    missing_pairs=[[h,a] for h in names for a in names if h!=a and (h,a) not in pairs]
    relational=[]
    if len(records)!=expected:relational.append('OBSERVED_SCHEDULED_COUNT_DIFFERS')
    if len(names)!=clubs(year):relational.append('LITERAL_CLUB_COUNT_DIFFERS')
    if missing_pairs:relational.append('MISSING_LITERAL_DIRECTED_PAIRINGS')
    if duplicate:relational.append('DUPLICATE_DIRECTED_PAIRINGS')
    if collisions:relational.append('SAME_TEAM_DATE_COLLISIONS')
    if round_errors or missing_rounds:relational.append('ROUND_ALLOCATION_OR_COVERAGE')
    return dict(season=f'{year}/{year+1}',observed=len(records),score_bearing=sum(r['assessment']['goal_derived_outcome'] is not None for r in records),
        expected_scheduled=expected,expected_played=279 if year==2019 else expected,club_labels=len(names),expected_clubs=clubs(year),team_names=names,
        missing_literal_pairs=missing_pairs,duplicates=duplicate,relational_issues=relational,
        same_team_date_collisions=collisions,normalized_name_collisions=name_collisions,appearance_counts=appearance,
        stage_counts=dict(Counter(r['stage'] for r in records)),round_counts={str(k):len(v) for k,v in sorted(rounds.items())},
        round_allocation_discrepancies=round_errors,missing_rounds=missing_rounds,wide_rounds=wide,
        source_line_date_regressions=sum(records[i]['date']<records[i-1]['date'] for i in range(1,len(records))),
        chronology_note='File/matchday order is not a chronological evaluation order. Historical stage remains undocumented where CSV has no stage field.')


def broad_groups(records):
    defects=[];dates=[];clusters=defaultdict(list);matrix=Counter();early_away=[]
    for r in records:
        a=inspect_record(r);fields=r['source_fields'];key=(a['goal_derived_outcome'],fields['result']);matrix[key]+=1
        if int(r['season'][:4])<2015 and a['goal_derived_outcome']=='A':early_away.append(fields['result'])
        item=dict(audit_id=r['audit_id'],source_line=r['source_line'],season=r['season'],date=r['date'],home=r['home'],away=r['away'],FT=r['FT'])
        if 'SYSTEMATIC_SOURCE_LABEL_DEFECT' in a['flags']:defects.append(dict(item,source_result=fields['result'],goal_derived=a['goal_derived_outcome']))
        if 'SOURCE_DATE_OUTSIDE_CONVENTIONAL_SEASON' in a['flags'] or 'INVALID_DATE' in a['flags']:
            dates.append(item);clusters[r['season'],r['date']].append(r['audit_id'])
    return dict(result_label_defect=dict(id='GROUP:CSV_RESULT_LABEL',members=defects,count=len(defects),
                    primary_target_count=sum(1990<=int(r['season'][:4])<=2013 for r in defects),
                    counts_by_season=dict(sorted(Counter(r['season'] for r in defects).items())),
                    all_defects_pre2015_away_to_draw=bool(defects) and all(int(r['season'][:4])<2015 and r['source_result']=='D' and r['goal_derived']=='A' for r in defects),
                    every_pre2015_away_label_D=bool(early_away) and set(early_away)=={'D'},
                    matrix=[dict(goal_derived=d,source_result=s,count=n) for (d,s),n in sorted(matrix.items(),key=lambda item:(str(item[0][0]),item[0][1]))],
                    root_cause='Unestablished; observed systematic encoding defect, no correction applied'),
                historical_date_quality=dict(id='GROUP:CSV_DATES',members=dates,count=len(dates),
                    primary_target_count=sum(1990<=int(r['season'][:4])<=2013 for r in dates),
                    clusters=[dict(season=y,source_date=d,member_ids=ids,classification='SUSPECTED_PLACEHOLDER' if 1932<=int(y[:4])<=1936 and d.endswith('-07-01') else 'SOURCE_SEASON_BOUNDARY_UNCERTAINTY') for (y,d),ids in sorted(clusters.items())]))


def compare_sources(old,new,mapping):
    if set(mapping)!={r[k] for r in new for k in ('home','away')} or len(set(mapping.values()))!=len(mapping):raise ValueError('Nonbijective diagnostic mapping')
    left=defaultdict(list);right=defaultdict(list)
    for r in old:left[r['home'],r['away']].append(r)
    for r in new:right[mapping[r['home']],mapping[r['away']]].append(r)
    differences=[];matched=0
    for pair in sorted(set(left)&set(right)):
        if len(left[pair])!=1 or len(right[pair])!=1:raise ValueError('Duplicate overlap pairing')
        a,b=left[pair][0],right[pair][0];matched+=1
        delta={k:dict(historical=a[k],modern=b[k]) for k in ('date','hg','ag') if a[k]!=b[k]}
        if delta:differences.append(dict(historical_id=a['audit_id'],modern_id=b['audit_id'],home=pair[0],away=pair[1],differences=delta))
    return dict(matched=matched,differences=differences,
                unmatched_historical=[r['audit_id'] for k,rs in sorted(left.items()) if k not in right for r in rs],
                unmatched_modern=[r['audit_id'] for k,rs in sorted(right.items()) if k not in left for r in rs],
                diagnostic_mapping=mapping,independence='UNESTABLISHED; no source mapping or history correction applied')


CASE_SPECS=(
    ('BASTIA_LYON',2016,'SC Bastia',{'Olympique Lyon','Olympique Lyonnais'},'ADMINISTRATIVE_SCORE_CONFLICT',None,None,None,['L1-E05','L1-E06']),
    ('NANTES_BASTIA',2013,'FC Nantes',{'SC Bastia'},'ADMINISTRATIVE_RESULT_SEMANTICS','2013-08-10',None,None,['L1-E02','L1-E03']),
    ('NICE_MARSEILLE',2021,'OGC Nice',{'Olympique Marseille'},'INTERRUPTED_REPLAY',None,'2021-10-27',None,['L1-E04']),
    ('MONTPELLIER_CLERMONT',2023,'Montpellier HSC',{'Clermont Foot 63'},'REPLAY_DATE_CONTEXT',None,None,'2023-10-25',['L1-E11','L1-E12']),
    ('MONTPELLIER_ST_ETIENNE',2024,'Montpellier HSC',{'AS Saint-Étienne','AS Saint-Etienne'},'SOURCE_MARKED_ADMINISTRATIVE',None,None,None,[]),
    ('NANTES_TOULOUSE_2026',2025,'FC Nantes',{'Toulouse FC'},'POST_EVENT_RATIFICATION','2026-05-17',None,'2026-05-27',['L1-E07','L1-E08','L1-E09']),
)
CASE_FACTS={
    'BASTIA_LYON':('2017-04-16','0-0'), 'NANTES_BASTIA':('2013-08-10','0-0'),
    'NICE_MARSEILLE':('2021-10-27','1-1'), 'MONTPELLIER_CLERMONT':('2023-11-29','1-1'),
    'MONTPELLIER_ST_ETIENNE':('2025-03-16','0-2'), 'NANTES_TOULOUSE_2026':('2026-05-17','0-0'),
}


def cases(primary,all_historical):
    result=[]
    for name,year,home,away,flag,kickoff,completion,decision,refs in CASE_SPECS:
        selected=[r for r in primary if r['season']==f'{year}/{year+1}' and r['home']==home and r['away'] in away]
        if len(selected)!=1:raise ValueError('Known review fixture missing/ambiguous: '+name)
        r=selected[0]
        if (r['date'],r['FT'])!=CASE_FACTS[name]:raise ValueError('Known case source facts changed: '+name)
        r['assessment']['flags'].append(flag);r.setdefault('review_refs',[]).append('CASE:'+name)
        r['assessment']['chronology'].update(independently_supported_kickoff=kickoff,independently_supported_completion=completion,administrative_decision_date=decision,evidence_ids=refs)
        alternatives=[x for x in all_historical if x['season']==r['season'] and x['home']==home and x['away'] in away and x['audit_id']!=r['audit_id']]
        result.append(dict(id='CASE:'+name,primary_ids=[r['audit_id']],source_values=[dict(audit_id=x['audit_id'],source=x['source'],line=x['source_line'],date=x['date'],home=x['home'],away=x['away'],FT=x['FT'],annotation=x['annotation']) for x in selected+alternatives],evidence_ids=refs,
                           effective_date_policy='NOT_DECIDED',note='Original kickoff, replay/completion and administrative date meanings are separate; retained evidence limitations apply.'))
    return result


def queue_records(records,groups):
    manual=[];flagged=set();by_category=defaultdict(set);strict=Counter()
    for r in records:
        a=r['assessment'];a['flags']=sorted(set(a['flags']));strict[a['classification']]+=1
        for flag in a['flags']:by_category[flag].add(r['audit_id']);flagged.add(r['audit_id'])
        individual=[f for f in a['flags'] if f!='SYSTEMATIC_SOURCE_LABEL_DEFECT']
        if individual:
            manual.append(dict(audit_id=r['audit_id'],season=r['season'],source=r['source'],source_line=r['source_line'],
                               date=r['date'],home=r['home'],away=r['away'],FT=r['FT'],flags=individual,
                               grouped_flags=['GROUP:CSV_RESULT_LABEL'] if 'SYSTEMATIC_SOURCE_LABEL_DEFECT' in a['flags'] else [],review_refs=r.get('review_refs',[])))
    if len({r['audit_id'] for r in manual})!=len(manual):raise ValueError('Review queue contains duplicate observations')
    return dict(manual_fixtures=manual,grouped_source_quality=groups,
                stats=dict(observations=len(records),strict_consistency_partition=dict(sorted(strict.items())),
                    unique_flagged_observations=len(flagged),manual_fixture_count=len(manual),
                    grouped_only_flagged=len(flagged-{r['audit_id'] for r in manual}),grouped_analysis_jobs=len(groups),
                    category_counts={k:len(ids) for k,ids in sorted(by_category.items())},
                    flag_instances=sum(len(ids) for ids in by_category.values()),
                    warning='Category counts overlap. Label-only records are grouped, not thousands of manual tasks. Cancelled slots remain observations, not missing historical acquisitions.'))


def build(directory=PRIVATE,root=ROOT):
    protection=protect(directory,root);manifest=acquisition.verify(directory)
    phase3=json.loads((directory/'phase3_inventory.json').read_bytes())
    hist_raw=(directory/metadata.HIST).read_bytes();hist=read_csv(hist_raw,metadata.HIST,base.sha(hist_raw))
    saved_hist=json.loads((directory/metadata.OUTPUT).read_bytes())['historical']['records']
    if [(r['source_line'],r['source_fields']) for r in hist]!=[(r['source_line'],r['source_fields']) for r in saved_hist]:
        raise ValueError('Independent CSV extraction differs from frozen Phase 2')
    primary=[r for r in hist if 1990<=int(r['season'][:4])<=2013];source_notes={}
    modern=[]
    for rec in sorted(manifest['acquired']+manifest['reused_phase2'],key=lambda r:r['original_filename']):
        raw=(directory/rec['path']).read_bytes();year=int(rec['original_filename'][:4])
        rows,notes=read_text(raw,year,rec['path'],rec['sha256']);source_notes[rec['path']]=notes
        saved=next(s for s in phase3['modern'] if s['source']==rec['path'])
        fields=('source_line','raw_record','season','date','home','away','hg','ag','FT','HT','round','annotation')
        if [{k:r[k] for k in fields} for r in rows]!=[{k:r[k] for k in fields} for r in saved['records']]:raise ValueError('Independent parser differs from frozen inventory: '+rec['path'])
        modern.extend(rows)
    primary+=modern
    if len({r['audit_id'] for r in primary})!=len(primary):raise ValueError('Nonunique audit IDs')
    for r in primary:r['assessment']=inspect_record(r)
    reports=[]
    for year in range(1990,2026):
        rows=[r for r in primary if r['season']==f'{year}/{year+1}'];report=season_report(rows,year)
        if year==1990:
            for r in rows:
                if any(r[k] in ('Brest Armorique FC','Stade Brest') for k in ('home','away')):r['assessment']['flags'].append('BREST_DUAL_LABEL_IDENTITY')
        reports.append(report)
    groups=broad_groups(hist)
    overlaps={}
    for year in range(2014,2025):
        old=[r for r in hist if r['season']==f'{year}/{year+1}'];new=[r for r in modern if r['season']==f'{year}/{year+1}' and r['FT'] is not None]
        mapping=metadata.OVERLAP_NAMES if year==2014 else {t:metadata.DIAGNOSTIC_VARIANTS.get(t,t) for r in new for t in (r['home'],r['away'])}
        o=compare_sources(old,new,mapping);overlaps[str(year)]=o
        if o['matched']!=phase3['scored_source_overlaps'][str(year)]['matched_pairs'] or len(o['differences'])!=len(phase3['scored_source_overlaps'][str(year)]['discrepancies']):raise ValueError('Frozen overlap changed')
        for diff in o['differences']:
            r=next(r for r in primary if r['audit_id']==diff['modern_id']);r['assessment']['flags'].append('CROSS_SOURCE_SCORE_OR_DATE_CONFLICT')
        if year==2015:
            for r in primary:
                if r['audit_id'] in o['unmatched_modern']:r['assessment']['flags'].append('DISTINCT_AJACCIO_CLUB_IDENTITY')
    case_registry=cases(primary,hist)
    queue=queue_records(primary,groups)
    for report in reports:
        rs=[r for r in primary if r['season']==report['season']]
        report['consistency_partition']=dict(sorted(Counter(r['assessment']['classification'] for r in rs).items()))
        report['flagged_observations']=sum(bool(r['assessment']['flags']) for r in rs)
        report['manual_queue_count']=sum(q['season']==report['season'] for q in queue['manual_fixtures'])
    wide=[dict(season=s['season'],**w) for s in reports for w in s['wide_rounds']]
    previous_wide={(w['season'],int(w['details']['round'])) for w in phase3['scheduling']['all_flags']}
    if {(w['season'],w['round']) for w in wide}!=previous_wide:raise ValueError('Scheduling case lost/changed')
    wide_ids={a for w in wide for a in w['affected_ids']}
    coverage=[dict(season=s['season'],status='ABSENT_SEASON',expected_fixture_count=s['expected_scheduled']) for s in reports if not s['observed']]
    missing_2006=next(s for s in reports if s['season']=='2006/2007')['missing_literal_pairs']
    if ['FC Nantes','Toulouse FC'] in missing_2006:
        coverage.append(dict(season='2006/2007',status='MISSING_SOURCE_PAIRING',home='FC Nantes',away='Toulouse FC',date=None,FT=None,evidence=['L1-E10'],policy='NOT_DECIDED'))
    cancelled=[r for r in primary if r['assessment']['classification']=='CANCELLED_UNSCORED']
    if (len(primary)!=phase3['modern_totals']['observed']+phase3['historical_source']['window']['observations'] or
            len(cancelled)!=101 or len(wide)!=40 or len(wide_ids)!=394):raise ValueError('Independent totals differ from frozen inventory')
    if groups['result_label_defect']['count']!=5489 or groups['result_label_defect']['primary_target_count']!=1895 or groups['historical_date_quality']['count']!=1162:raise ValueError('Frozen broad-source diagnostics changed')
    queue.update(scope='Phase 4 review only; flags are not approved corrections, exclusions or HOLD OUT decisions',coverage_gaps=coverage,known_cases=case_registry)
    report=dict(scope='Ligue 1 Phase 4 independent structural validation, no historical certification or processing decisions',protected=protection,
        source_manifest_sha256=base.sha((directory/acquisition.MANIFEST).read_bytes()),phase3_inventory_sha256=base.sha((directory/'phase3_inventory.json').read_bytes()),
        documentary_context_sha256=base.sha((directory/'documentary_context.json').read_bytes()),
        totals=dict(queue['stats'],historical_primary=sum(r['source']==metadata.HIST for r in primary),modern_primary=len(modern),score_bearing=sum(r['assessment']['goal_derived_outcome'] is not None for r in primary),
                    represented_seasons=sum(bool(s['observed']) for s in reports),target_seasons=len(reports),wide_rounds=len(wide),wide_fixture_slots=len(wide_ids)),
        seasons=reports,records=primary,groups=groups,overlaps=overlaps,coverage_gaps=coverage,cases=case_registry,source_notes=source_notes,
        historical_date_invalid_count=sum('INVALID_DATE' in inspect_record(r)['malformed_reasons'] for r in hist),
        historical_numeric_defect_count=sum(bool([f for f in inspect_record(r)['malformed_reasons'] if f in ('INVALID_GOALS','FT_GOAL_CONFLICT','NUMERIC_DERIVED_FIELD_CONFLICT')]) for r in hist),
        identity_review_context=dict(source_label_seasons={name:sorted({r['season'] for r in hist+modern if name in (r['home'],r['away'])}) for name in sorted({r[k] for r in hist+modern for k in ('home','away')})},
            warning='No continuity is inferred for identical names across decades, historical Toulouse entities, Paris clubs or reconstituted clubs. Season-scoped diagnostic overlap mappings are not global identities.'),
        limitations=dict(csv_stage_undocumented_records=sum(r['stage']=='CSV_TIER1_STAGE_UNDOCUMENTED' for r in primary),source_independence='UNESTABLISHED',licensing=base.RIGHTS,
                         training_permission='UNRESOLVED',eligibility_policy='NOT_DECIDED',effective_date_policy='NOT_DECIDED',
                         historical_certification='NOT_CLAIMED',audit_ids='SOURCE-BOUND IDs; not standardized match IDs'))
    return report,queue


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--init',action='store_true');p.add_argument('--check',action='store_true');args=p.parse_args()
    if args.init:initialize()
    report,queue=build()
    for name,value in ((REPORT,report),(QUEUE,queue)):
        raw=base.encode(value);path=PRIVATE/name
        if args.check:
            if path.read_bytes()!=raw:raise ValueError('Nonreproducible assessment: '+name)
        else:base.save(path,raw)
        print(name,len(raw),base.sha(raw))
    print(json.dumps(report['totals'],indent=2))
