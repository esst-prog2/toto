"""Phase 4 independent offline structural validation; never historical policy.

The parser does not call Phase 2/3 parsers. Unknown grammar fails explicitly.
Original values, source dates, uncertainties and overlapping flags are retained.
"""
import argparse
from collections import Counter, defaultdict
import csv
from datetime import date
import json
from pathlib import Path
import re
import subprocess
import unicodedata
from scripts import collect_ligue2_history as acquisition

ROOT, PRIVATE = acquisition.ROOT, acquisition.PRIVATE
base = acquisition.base
BASELINE = 'phase4_protected_before.json'
REPORT = 'phase4_structural_validation.json'
QUEUE = 'phase4_review_queue.json'
MONTHS = {m:i+1 for i,m in enumerate('Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split())}
DAYS = ('Mon','Tue','Wed','Thu','Fri','Sat','Sun')


def initialize(directory=PRIVATE,root=ROOT):
    if (directory/BASELINE).exists():return protect(directory,root)
    acquisition.protect(directory,root)
    final=json.loads((directory/'phase3_final_verification.json').read_text())
    for name,item in final['private_files_before_receipt'].items():
        if base.sha((directory/name).read_bytes())!=item['sha256']:raise ValueError('Approved evidence changed: '+name)
    for name,digest in final['public_files'].items():
        if base.sha((root/name).read_bytes())!=digest:raise ValueError('Approved public file changed: '+name)
    files={str(p.relative_to(root)):base.sha(p.read_bytes()) for p in directory.rglob('*') if p.is_file()}
    phase2=json.loads((directory/'phase2_final_verification.json').read_text())
    public=set(final['public_files'])|set(phase2['public_files'])
    files.update({n:base.sha((root/n).read_bytes()) for n in public if n!='PLANNING_LOG.md'})
    log=(root/'PLANNING_LOG.md').read_bytes();index=subprocess.check_output(['git','rev-parse','--git-path','index'],cwd=root).decode().strip()
    base.save(directory/BASELINE,base.encode(dict(files=files,planning_log=dict(bytes=len(log),sha256=base.sha(log)),
        head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root).decode().strip(),index_sha256=base.sha((root/index).read_bytes()))))
    return protect(directory,root)


def protect(directory=PRIVATE,root=ROOT):
    previous=acquisition.protect(directory,root);saved=json.loads((directory/BASELINE).read_text())
    if not saved['files']:raise ValueError('Empty Phase 4 protected baseline')
    for name,digest in saved['files'].items():
        p=root/name
        if not p.resolve().is_relative_to(root.resolve()) or base.sha(p.read_bytes())!=digest:raise ValueError('Frozen Phase 2–3 file changed: '+name)
    log=(root/'PLANNING_LOG.md').read_bytes();prefix=saved['planning_log']
    if len(log)<prefix['bytes'] or base.sha(log[:prefix['bytes']])!=prefix['sha256']:raise ValueError('Planning history changed')
    return dict(previous=previous,phase2_3_entries=len(saved['files']))


def source_id(digest,line):
    return base.sha(base.encode([digest,line,None,None]))


def heading(s,year):
    match=re.fullmatch(r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun) ([A-Z][a-z]{2}) (\d{1,2})(?: (\d{4}))?',s)
    if not match:return None
    found=[]
    for y in (int(match[4]),) if match[4] else (year,year+1):
        try:day=date(y,MONTHS[match[2]],int(match[3]))
        except (ValueError,KeyError):continue
        if date(year,7,1)<=day<=date(year+1,6,30) and DAYS[day.weekday()]==match[1]:found.append(day.isoformat())
    if len(found)!=1:raise ValueError('Invalid/ambiguous date heading: '+s)
    return dict(date=found[0],date_heading=s,year_explicit=bool(match[4]),
                date_basis='EXPLICIT_DAY_MONTH_YEAR_WEEKDAY' if match[4] else 'EXPLICIT_DAY_MONTH_WITH_SEASON_WEEKDAY_YEAR_RESOLUTION')


def fixture(body):
    note='';annotation=re.search(r'\s+(\[[^\]]+\])$',body)
    if annotation:note=annotation[1];body=body[:annotation.start()].rstrip()
    if re.search(r'\s+v\s+',body):
        home,tail=re.split(r'\s+v\s+',body,maxsplit=1)
        score=re.fullmatch(r'(.+?)\s{2,}([0-9]+)-([0-9]+)(?:\s+\(([0-9]+-[0-9]+)\))?',tail)
        if score:away,h,a,ht=score.groups()
        else:
            if re.search(r'\d\s*[-:]|\?\s*[-:]|[-:]\s*\d',tail):raise ValueError('Malformed/partial score')
            away=tail;h=a=ht=None
    else:
        score=re.fullmatch(r'(.+?)\s+([0-9]+)-([0-9]+)(?:\s+\(([0-9]+-[0-9]+)\))?\s+(.+)',body)
        if not score:raise ValueError('Unknown fixture grammar')
        home,h,a,ht,away=score.groups()
    return dict(home=home,away=away,hg=h,ag=a,HT=ht,FT=f'{h}-{a}' if h is not None else None,annotation=note)


def read_source(raw,year,path,digest):
    if base.sha(raw)!=digest:raise ValueError('Source hash mismatch')
    physical=raw.splitlines(keepends=True);rows=[];notes=[];current=None;stage=None;round_id=None;title=None;depth=0;round_headings=[]
    for number,line in enumerate(raw.decode('utf-8-sig').splitlines(),1):
        text=line.strip()
        if not text:continue
        def fail(message):raise ValueError(f'{path}:{number}: {message}: {text}')
        if depth or text.startswith('('):
            if not rows:fail('Scorer note without fixture')
            depth+=text.count('(')-text.count(')')
            if depth<0:fail('Unbalanced scorer annotation')
            notes.append(dict(line=number,kind='SCORER_NOTE',text=text));continue
        if text.startswith('#'):notes.append(dict(line=number,kind='COMMENT',text=text));continue
        if text.startswith('='):
            m=re.fullmatch(r'= French Ligue 2 (\d{4})/(\d{2}|\d{4})',text)
            if title or not m or int(m[1])!=year or int(m[2])!=(year+1 if len(m[2])==4 else (year+1)%100):fail('Wrong/duplicate title')
            title=text;notes.append(dict(line=number,kind='TITLE',text=text));continue
        if text.startswith('▪'):
            label=text[1:].strip();m=re.fullmatch(r'(?:Matchday (\d+)|Regular Season - (\d+)|(\d+)\. Round)',label)
            if m:
                stage='REGULAR_SEASON';round_id=int(next(x for x in m.groups() if x))
                if not 1<=round_id<=2*((18 if year>=2024 else 20)-1):fail('Round outside competition format')
                if round_id in round_headings:fail('Duplicate round heading')
                round_headings.append(round_id)
            elif re.search(r'play.?off|promotion|final',label,re.I):stage='OTHER_STAGE';round_id=label
            else:fail('Unknown stage')
            current=None;notes.append(dict(line=number,kind='ROUND',stage=stage,label=label));continue
        resolved=heading(text,year)
        if resolved:
            current=dict(resolved,date_heading_line=number);continue
        if not title or current is None or stage is None:fail('Fixture missing title/stage/date')
        time=re.match(r'^(\d{1,2}:\d{2})\s+',text);body=text[time.end():] if time else text
        if time and (int(time[1].split(':')[0])>23 or int(time[1].split(':')[1])>59):fail('Invalid kickoff time')
        try:r=fixture(body)
        except ValueError as exc:fail(str(exc))
        r.update(current,source=path,source_sha256=digest,source_line=number,raw_record=line,
                 raw_line_sha256=base.sha(line.encode('utf-8')),physical_line_sha256=base.sha(physical[number-1]),
                 audit_id=source_id(digest,number),season=f'{year}/{year+1}',source_competition_title=title,
                 stage=stage,round=round_id,source_kickoff_time=time[1] if time else None)
        rows.append(r)
    if not title or not rows or depth:raise ValueError('Missing or unterminated source content: '+path)
    return rows,notes


def inspect_record(r):
    errors=[];flags=set();h=a=None;cancelled=bool(re.search(r'cancel',r['annotation'],re.I));awarded=bool(re.search(r'award',r['annotation'],re.I))
    for t in (r['home'],r['away']):
        if not t or t!=t.strip() or '\ufffd' in t or any(unicodedata.category(ch).startswith('C') for ch in t):errors.append('INVALID_TEAM_LABEL')
    if r['home']==r['away']:errors.append('IDENTICAL_TEAMS')
    if r['stage']!='REGULAR_SEASON':errors.append('UNAPPROVED_STAGE')
    y=int(r['season'][:4])
    try:
        d=date.fromisoformat(r['date'])
        if d.isoformat()!=r['date'] or not date(y,7,1)<=d<=date(y+1,6,30):errors.append('INVALID_SEASON_DATE')
    except (ValueError,TypeError):errors.append('INVALID_DATE')
    try:
        for token in (r['hg'],r['ag']):
            if token is not None and (not re.fullmatch(r'[0-9]+',token) or int(token)>2**63-1):raise ValueError()
        h=int(r['hg']) if r['hg'] is not None else None;a=int(r['ag']) if r['ag'] is not None else None
        if (h is None)!=(a is None):errors.append('PARTIAL_SCORE')
        if h is not None and a is not None and r['FT']!=f'{h}-{a}':errors.append('FT_GOAL_CONFLICT')
        if h is None and a is None and r['FT'] is not None:errors.append('FT_WITHOUT_GOALS')
        if cancelled and h is not None:errors.append('CANCELLED_WITH_SCORE')
        if awarded and h is None:errors.append('AWARD_WITHOUT_SCORE')
        if r['HT'] is not None:
            m=re.fullmatch(r'([0-9]+)-([0-9]+)',r['HT'])
            if not m or h is None or a is None or int(m[1])>h or int(m[2])>a:errors.append('HT_FT_CONFLICT')
    except (ValueError,TypeError):errors.append('INVALID_SCORE')
    incomplete=h is None and a is None and not cancelled
    if cancelled:flags.add('SOURCE_CANCELLED')
    if awarded:flags.add('SOURCE_MARKED_AWARDED')
    if r['annotation'] and not cancelled and not awarded:flags.add('OTHER_SOURCE_ANNOTATION')
    if h is not None and a is not None and (max(h,a)>=7 or h+a>=10):flags.add('UNUSUAL_SCORE')
    if incomplete:flags.add('UNEXPLAINED_INCOMPLETE')
    if errors:flags.add('STRUCTURALLY_INVALID')
    if r['season']=='2022/2023' and r['home']=='Girondins Bordeaux' and r['away']=='Rodez AF':flags.add('BORDEAUX_RODEZ_ADMINISTRATIVE_REVIEW')
    chronology=dict(source_heading_date=r['date'],source_heading_line=r.get('date_heading_line'),
        source_scheduled_date=r['date'] if cancelled else None,actual_kickoff_date=None,actual_completion_date=None,
        administrative_decision_date=None,secondary_reported_decision_date=None,effective_result_availability_date=None,
        meaning='SOURCE_SCHEDULED_CANCELLED' if cancelled else 'SOURCE_DATE_NOT_INDEPENDENTLY_CERTIFIED',
        date_resolution=r.get('date_basis'),historical_policy='NOT_DECIDED')
    if 'BORDEAUX_RODEZ_ADMINISTRATIVE_REVIEW' in flags:
        chronology['administrative_decision_date']='2023-06-12';chronology['meaning']='SOURCE_EVENT_DATE_AND_SEPARATELY_DOCUMENTED_PENALTY_DECISION; numerical/finality/availability unresolved'
    if awarded and r['season']=='2020/2021' and r['home']=='Chamois Niortais' and r['away']=='Valenciennes FC':
        chronology['secondary_reported_decision_date']='2021-01-06';chronology['meaning']='SOURCE_DATE_AND_INDEX_ONLY_LATER_AWARD_LEAD; primary decision/finality/availability unresolved'
    return dict(structurally_valid=not errors,errors=sorted(set(errors)),incomplete=incomplete,
                source_cancelled=cancelled,source_awarded=awarded,score_bearing=h is not None and a is not None,
                goal_derived_outcome=None if h is None or a is None else 'H' if h>a else 'A' if h<a else 'D',
                flags=sorted(flags),chronology=chronology,historical_verification='NOT_CERTIFIED')


def validate_season(rows,year):
    if not rows:raise ValueError('Empty season population')
    n=18 if year>=2024 else 20;names=sorted({r[k] for r in rows for k in ('home','away')});pairs=defaultdict(list);rounds=defaultdict(list);events=defaultdict(list);norm=defaultdict(list)
    for name in names:norm[unicodedata.normalize('NFC',name).casefold()].append(name)
    for r in rows:
        r['assessment']=inspect_record(r)
        if any(len(norm[unicodedata.normalize('NFC',t).casefold()])>1 for t in (r['home'],r['away'])):r['assessment']['flags'].append('NORMALIZED_LABEL_COLLISION')
        pairs[r['home'],r['away']].append(r);rounds[str(r['round'])].append(r)
        for team in (r['home'],r['away']):events[r['date'],team].append(r)
    missing=[[h,a] for h in names for a in names if h!=a and (h,a) not in pairs]
    duplicates=[]
    for (h,a),rs in sorted(pairs.items()):
        if len(rs)>1:
            conflict=len({(r['hg'],r['ag']) for r in rs})>1
            duplicates.append(dict(home=h,away=a,conflicting=conflict,audit_ids=[r['audit_id'] for r in rs]))
            for r in rs:r['assessment']['flags'].append('CONFLICTING_PAIR' if conflict else 'DUPLICATE_PAIR')
    collisions=[]
    for (day,team),rs in sorted(events.items()):
        if len(rs)>1:
            collisions.append(dict(date=day,team=team,audit_ids=[r['audit_id'] for r in rs]))
            for r in rs:r['assessment']['flags'].append('TEAM_SAME_DAY_COLLISION')
    wide=[];round_checks=[];outliers=[]
    for rnd,rs in sorted(rounds.items(),key=lambda x:int(x[0]) if x[0].isdigit() else 999):
        days=sorted(r['date'] for r in rs);median=days[(len(days)-1)//2];counts=Counter(r[k] for r in rs for k in ('home','away'))
        span=(date.fromisoformat(days[-1])-date.fromisoformat(days[0])).days
        record=dict(round=rnd,first_date=days[0],last_date=days[-1],span_days=span,median_date=median,
                    fixtures=[dict(audit_id=r['audit_id'],source_line=r['source_line'],date=r['date'],home=r['home'],away=r['away'],FT=r['FT']) for r in rs])
        if span>14:
            wide.append(record)
            for r in rs:r['assessment']['flags'].append('WIDE_ROUND')
        for r in rs:
            distance=abs((date.fromisoformat(r['date'])-date.fromisoformat(median)).days)
            if distance>14:
                outliers.append(dict(audit_id=r['audit_id'],round=rnd,date=r['date'],median_date=median,distance_days=distance,home=r['home'],away=r['away']))
                r['assessment']['flags'].append('DIAGNOSTIC_DATE_OUTLIER')
        issues=[]
        if len(rs)!=n//2:issues.append('ROUND_FIXTURE_COUNT')
        if len(counts)!=n or any(v!=1 for v in counts.values()):issues.append('ROUND_TEAM_COVERAGE')
        if issues:
            for r in rs:r['assessment']['flags'].append('ROUND_STRUCTURE_REVIEW')
        round_checks.append(dict(round=rnd,observed=len(rs),expected=n//2,distinct_teams=len(counts),issues=issues))
    reversals=[]
    for previous,current in zip(rows,rows[1:]):
        if current['date']<previous['date']:
            reversals.append(dict(previous_id=previous['audit_id'],previous_line=previous['source_line'],previous_date=previous['date'],
                current_id=current['audit_id'],current_line=current['source_line'],current_date=current['date'],
                backwards_days=(date.fromisoformat(previous['date'])-date.fromisoformat(current['date'])).days))
            previous['assessment']['flags'].append('SOURCE_ORDER_DATE_REVERSAL');current['assessment']['flags'].append('SOURCE_ORDER_DATE_REVERSAL')
    format_issues=[]
    if len(rows)!=n*(n-1):format_issues.append('SEASON_FIXTURE_COUNT')
    if len(names)!=n:format_issues.append('SEASON_CLUB_COUNT')
    if missing:format_issues.append('MISSING_DIRECTED_PAIRINGS')
    if duplicates:format_issues.append('DUPLICATE_OR_CONFLICTING_PAIRINGS')
    expected_rounds={str(x) for x in range(1,2*(n-1)+1)}
    if set(rounds)!=expected_rounds:format_issues.append('ROUND_SET')
    if any(x['issues'] for x in round_checks):format_issues.append('ROUND_STRUCTURE')
    if collisions:format_issues.append('TEAM_SAME_DAY_COLLISION')
    if any(r['stage']!='REGULAR_SEASON' for r in rows):format_issues.append('OTHER_STAGE')
    if len({r['season'] for r in rows})!=1 or rows[0]['season']!=f'{year}/{year+1}':format_issues.append('SEASON_ASSIGNMENT')
    for r in rows:r['assessment']['flags']=sorted(set(r['assessment']['flags']))
    return dict(season=f'{year}/{year+1}',observed=len(rows),expected=n*(n-1),score_bearing=sum(r['assessment']['score_bearing'] for r in rows),
        cancelled=sum(r['assessment']['source_cancelled'] for r in rows),unscored=sum(not r['assessment']['score_bearing'] for r in rows),
        incomplete=sum(r['assessment']['incomplete'] for r in rows),structurally_valid=sum(r['assessment']['structurally_valid'] for r in rows),
        structurally_invalid=sum(not r['assessment']['structurally_valid'] for r in rows),flagged=sum(bool(r['assessment']['flags']) for r in rows),
        clubs=len(names),expected_clubs=n,team_labels=names,stage_counts=dict(Counter(r['stage'] for r in rows)),
        missing_pairings=missing,duplicate_pairings=duplicates,team_same_day_collisions=collisions,
        normalized_name_collisions={k:v for k,v in norm.items() if len(v)>1},format_issues=format_issues,round_checks=round_checks,
        first_source_date=min(r['date'] for r in rows),last_source_date=max(r['date'] for r in rows),
        explicit_year_observations=sum(r['year_explicit'] for r in rows),season_weekday_resolved_year_observations=sum(not r['year_explicit'] for r in rows),
        wide_rounds=wide,diagnostic_outliers=outliers,source_order_date_reversals=reversals)


def queue(records):
    result=[]
    for r in records:
        if r['assessment']['flags']:
            result.append({k:r[k] for k in ('audit_id','source','source_sha256','source_line','physical_line_sha256','raw_record','season','date','home','away','hg','ag','FT','HT','round','annotation','assessment')})
    if len({r['audit_id'] for r in result})!=len(result):raise ValueError('Duplicate review audit ID')
    return sorted(result,key=lambda r:(r['season'],r['source_line']))


def reconcile_phase3(records,reports,prior):
    old={r['audit_id']:r for s in prior['sources'] for r in s['records']};new={r['audit_id']:r for r in records}
    if len(old)!=sum(len(s['records']) for s in prior['sources']) or len(new)!=len(records) or old.keys()!=new.keys():raise ValueError('Phase 3 population/bindings differ')
    for key,r in new.items():
        for field in ('source','source_sha256','source_line','raw_record','raw_line_sha256','season','date','home','away','hg','ag','FT','HT','round','stage','annotation','year_explicit'):
            if r[field]!=old[key][field]:raise ValueError('Independent raw fact differs: '+field)
    old_queue={r['audit_id']:set(r['categories']) for r in prior['summary']['review_candidates']};expected={}
    for r in records:
        flags=set(r['assessment']['flags']);cats=set()
        if 'WIDE_ROUND' in flags:cats.add('WIDE_ROUND')
        if 'SOURCE_CANCELLED' in flags:cats.add('SOURCE_CANCELLED')
        if 'SOURCE_MARKED_AWARDED' in flags or 'OTHER_SOURCE_ANNOTATION' in flags:cats.add('SOURCE_ANNOTATION')
        if 'UNUSUAL_SCORE' in flags:cats.add('UNUSUAL_SCORE')
        if 'BORDEAUX_RODEZ_ADMINISTRATIVE_REVIEW' in flags:cats.add('BORDEAUX_RODEZ_ADMINISTRATIVE_REVIEW')
        if 'UNEXPLAINED_INCOMPLETE' in flags:cats.add('UNSCORED_UNEXPLAINED')
        if cats:expected[r['audit_id']]=cats
    if expected!=old_queue:raise ValueError('Independent Phase 3 category/member reconciliation differs')
    for season in reports:
        source=next(s for s in prior['sources'] if s['receipt']['season']==season['season']);old_rounds={str(w['round']):{f['source_line'] for f in w['fixtures']} for w in source['assessment']['wide_rounds']}
        new_rounds={str(w['round']):{f['source_line'] for f in w['fixtures']} for w in season['wide_rounds']}
        if old_rounds!=new_rounds:raise ValueError('Wide-round member binding differs')
    membership=Counter(k for cats in expected.values() for k in cats);overlaps=Counter('+'.join(sorted(cats)) for cats in expected.values() if len(cats)>1)
    return dict(observations=len(records),old_review_members=len(old_queue),independent_review_members=len(expected),category_counts=dict(sorted(membership.items())),overlap_combinations=dict(sorted(overlaps.items())),exact_original_facts=True,exact_review_members_and_categories=True)


def identity_review(records,root):
    labels=sorted({r[k] for r in records for k in ('home','away')});groups=defaultdict(list);reserve=[]
    for name in labels:
        key=''.join(ch for ch in unicodedata.normalize('NFKD',name).casefold() if not unicodedata.combining(ch))
        groups[key].append(name)
        if re.search(r'(?:\bII\b|\b[Bb]\b|[Rr]éserve)',name):reserve.append(name)
    path=root/'data/private/france/ligue_1/ligue_1_standardized_1990_2025.csv'
    if not path.exists():raise ValueError('Expected protected Ligue 1 comparison missing')
    with path.open(newline='') as f:other={r[k] for r in csv.DictReader(f) for k in ('home_team','away_team')}
    # Human-readable diagnostic groups, never mappings applied to any observation.
    candidates=[['AC Ajaccio','Ajaccio'],['Gazélec FC Ajaccio','Gazélec Ajaccio'],['Girondins Bordeaux','Bordeaux'],['Havre AC','Le Havre'],['Stade Brestois 29','Brest'],['RC Strasbourg','Strasbourg'],['Évian Thonon Gaillard','Evian TG'],['FC Annecy','Annecy'],['US Quevilly-Rouen','Quevilly Rouen']]
    return dict(distinct_literal_labels=len(labels),labels=labels,unicode_accentfold_groups=[v for v in groups.values() if len(v)>1],reserve_label_candidates=reserve,
        exact_labels_shared_with_ligue1=sorted(set(labels)&other),ligue2_labels_not_exactly_matching_ligue1=sorted(set(labels)-other),
        diagnostic_crossleague_groups=[dict(labels=g,ligue2_present=[x for x in g if x in labels],ligue1_present=[x for x in g if x in other]) for g in candidates if any(x in labels for x in g)],
        continuity_review_labels=[x for x in labels if any(k in x for k in ('Arles','Annecy','Brest','Évian','Quevilly','Créteil','Bastia','Ajaccio','Red Star'))],
        policy='No identity mappings applied; sporting continuity, abbreviations and successor entities require Phase 5 evidence. Exact shared labels do not certify continuity.')


def build(directory=PRIVATE,root=ROOT):
    protection=protect(directory,root);prior=json.loads((directory/'phase3_inventory.json').read_text());phase2=base.verify_originals(directory);phase3=acquisition.verify_originals(directory)
    receipts=[r for r in phase2['files']+phase3['files'] if r['repository']==acquisition.REPO and 2014<=int(r['season'][:4])<=2024]
    if len(receipts)!=11 or {r['season'] for r in receipts}!={f'{y}/{y+1}' for y in range(2014,2025)}:raise ValueError('Wrong independent population')
    records=[];reports=[];notes=[]
    for receipt in sorted(receipts,key=lambda r:r['season']):
        raw=(directory/receipt['path']).read_bytes();rows,annotations=read_source(raw,int(receipt['season'][:4]),receipt['path'],receipt['sha256'])
        for row in rows:row['provenance']=dict(commit=receipt['commit'],git_blob_sha1=receipt['git_blob_sha1'],url=receipt['url'],retrieved_at_utc=receipt['retrieved_at_utc'])
        reports.append(validate_season(rows,int(receipt['season'][:4])));records.extend(rows);notes.append(dict(source=receipt['path'],annotations=annotations))
    reconciliation=reconcile_phase3(records,reports,prior);review=queue(records);categories=Counter(k for r in review for k in r['assessment']['flags']);combinations=Counter('+'.join(r['assessment']['flags']) for r in review)
    report=dict(phase=4,scope='2014/15–2024/25 only; independent structural validation, no historical decisions',protected=protection,
        summary=dict(observed=len(records),score_bearing=sum(r['assessment']['score_bearing'] for r in records),cancelled=sum(r['assessment']['source_cancelled'] for r in records),
            structurally_valid=sum(r['assessment']['structurally_valid'] for r in records),structurally_invalid=sum(not r['assessment']['structurally_valid'] for r in records),
            incomplete=sum(r['assessment']['incomplete'] for r in records),flagged=len(review),category_counts=dict(sorted(categories.items())),flag_combinations=dict(sorted(combinations.items())),
            wide_round_contexts=sum(len(s['wide_rounds']) for s in reports),wide_round_members=sum(len(w['fixtures']) for s in reports for w in s['wide_rounds']),
            diagnostic_outliers=sum(len(s['diagnostic_outliers']) for s in reports),source_order_reversal_pairs=sum(len(s['source_order_date_reversals']) for s in reports)),
        seasons=reports,records=records,source_notes=notes,phase3_reconciliation=reconciliation,identity_review=identity_review(records,root),
        preserved_separate_sources=dict(incomplete_2025_26=prior['incomplete_2025_26'],rsssf_1998_99=prior['rsssf_1998_99'],historical_gap=prior['historical_gap']),
        documentary_context=dict(phase2=prior['documentary_context'],phase3=json.loads((directory/'phase3_documentary_context.json').read_text())),
        date_diagnostic_method='Within each round choose lower median source date; flag observations more than 14 days away. Flag both sides of adjacent physical-order date reversals. Neither test establishes a historical error.',
        rights=base.RIGHTS,policy='No historical certification, aliases, result/date corrections, screening, exclusions, standardization, integration or training')
    review_output=dict(phase=4,scope=report['scope'],summary=report['summary'],phase3_reconciliation=reconciliation,fixtures=review,identity_review=report['identity_review'])
    return report,review_output


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--init',action='store_true');args=parser.parse_args()
    if args.init:initialize()
    report,review=build()
    for name,obj in [(REPORT,report),(QUEUE,review)]:
        target=PRIVATE/name;content=base.encode(obj)
        if target.exists():
            if target.read_bytes()!=content:raise ValueError('Output changed; inspect before replacing: '+name)
        else:base.save(target,content)
    print(json.dumps(report['summary'],indent=2))
