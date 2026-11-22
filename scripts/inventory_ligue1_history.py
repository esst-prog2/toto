"""Phase 3 offline source inventory, not structural/historical certification.

Retains gaps, literal observations and evidence classifications. No corrections,
eligibility decisions, standardization or model use. --check compares saved bytes.
"""
import argparse
from collections import Counter, defaultdict
from datetime import date
import json
import re
import unicodedata

from scripts import collect_ligue1_feasibility as base
from scripts import collect_ligue1_history as acquisition
from scripts import validate_ligue1_feasibility as feasibility

ROOT, PRIVATE = base.ROOT, base.PRIVATE
OUTPUT = 'phase3_inventory.json'


def diagnostic_labels(rows):
    names=defaultdict(set);candidates=defaultdict(list)
    for r in rows:
        for k in ('home','away'):names[r[k]].add(r['season'])
    for name in sorted(names):
        key=unicodedata.normalize('NFD',name).casefold()
        key=''.join(c for c in key if not unicodedata.combining(c))
        candidates[re.sub(r'[^\w]+',' ',key).strip()].append(name)
    return dict(exact_labels={n:sorted(ys) for n,ys in sorted(names.items())},
                distinct_labels=len(names),string_candidates={k:v for k,v in sorted(candidates.items()) if len(v)>1},
                historical_identity_warning='String similarity is not club continuity. Preserve Brest labels, Toulouse entities, Paris clubs, reconstituted clubs and similarly named clubs until independently reviewed. No global mapping.')


def result_diagnosis(rows):
    """Read-only contingency analysis; retain all contradictions and raw fields."""
    matrix=Counter();by_year=defaultdict(Counter);numeric=[];conflicts=[]
    for r in rows:
        f=r['source_fields'];year=int(f['Season'])
        try:
            h,a=feasibility.goals(f['hgoal']),feasibility.goals(f['vgoal'])
            if h is None or a is None:raise ValueError('Missing goals')
        except (ValueError,TypeError) as exc:
            numeric.append(dict(line=r['source_line'],kind='INVALID_GOALS',error=str(exc)));continue
        derived=feasibility.outcome(h,a);key=(derived,f['result'])
        matrix[key]+=1;by_year[year][key]+=1
        checks={'FT':f'{h}-{a}','totgoal':str(h+a),'goaldif':str(h-a)}
        for field,wanted in checks.items():
            if f[field]!=wanted:numeric.append(dict(line=r['source_line'],kind=field,source=f[field],expected_from_goals=wanted))
        if f['result']!=derived:
            conflicts.append(dict(line=r['source_line'],season=r['season'],home=r['home'],away=r['away'],
                                  source_result=f['result'],goal_derived=derived,FT=f['FT']))
    def tab(counts):
        return [dict(goal_derived=k[0],source_result=k[1],count=n) for k,n in sorted(counts.items())]
    early=Counter();late=Counter()
    for y,counts in by_year.items():(early if y<2015 else late).update(counts)
    return dict(matrix=tab(matrix),before_2015=tab(early),from_2015=tab(late),
                by_season={f'{y}/{y+1}':tab(v) for y,v in sorted(by_year.items())},
                contradiction_count=len(conflicts),older_window_contradictions=sum(1990<=int(r['season'][:4])<=2013 for r in conflicts),
                contradictions=conflicts,numeric_internal_disagreements=numeric,
                systematic_pre2015_away_to_draw=(sum(n for (d,s),n in early.items() if d=='A')>0 and
                    all(s=='D' for d,s in early if d=='A') and not any(d!=s for d,s in late)),
                interpretation='Systematic derived-label discrepancy; numerical internal agreement is not independent historical proof. Upstream generation cause unestablished. No source fields replaced.',
                required_evidence='Independent dated fixtures and full-time results, stratified across seasons and outcome classes; official decisions for exceptions, identity/date review and approved later processing policy before use.')


def date_inventory(rows):
    counts=Counter();out=[];invalid=[]
    for r in rows:
        y=int(r['season'][:4])
        try:
            if date.fromisoformat(r['date']).isoformat()!=r['date']:raise ValueError('Noncanonical date')
        except (ValueError,TypeError):
            invalid.append(dict(line=r['source_line'],season=r['season'],date=r['date']));continue
        if not f'{y}-07-01'<=r['date']<=f'{y+1}-06-30':
            counts[r['season']]+=1
            out.append(dict(line=r['source_line'],season=r['season'],date=r['date'],home=r['home'],away=r['away'],FT=r['FT']))
    return dict(outside_source_season_count=len(out),counts_by_season=dict(sorted(counts.items())),records=out,invalid_dates=invalid,
                warning='Date parsing and concentration do not establish actual match dates; no proxy replacement or season relabelling.')


def date_precision(rows):
    return dict(explicit_day_month=len(rows),explicit_year=sum(r.get('year_explicit',False) for r in rows),
                season_weekday_inferred_year=sum(not r.get('year_explicit',False) for r in rows),
                day_month_inferred=0,ambiguities=0,
                note='All source day/month headings explicit; missing year resolved uniquely within season by weekday. Scheduled dates are not certified playing/completion/availability dates.')


def carried_flags(phase2, modern):
    by_source={r['source']:r for r in modern};carried=[]
    for s in phase2['modern']:
        if s['source'].endswith('-full.txt'):continue
        now=by_source.get(s['source'])
        if now is None:raise ValueError('Missing Phase 2 ordinary season')
        if now['assessment']!=s['assessment'] or now['records']!=s['records']:
            raise ValueError('Frozen Phase 2 observations/assessment changed')
        for flag in s['assessment']['wide_rounds']:
            if flag not in now['assessment']['wide_rounds']:raise ValueError('Phase 2 flag lost')
            carried.append(dict(source=s['source'],season=s['assessment']['season'],details=flag))
    return carried


def historical_window(rows):
    reports=[]
    for y in range(1990,2014):
        selected=[r for r in rows if r['season']==f'{y}/{y+1}']
        report=feasibility.assess(selected,y)
        report['source_presence']='PRESENT' if selected else 'MISSING_SEASON'
        reports.append(report)
    return dict(seasons=reports,observations=sum(r['observed'] for r in reports),
                score_bearing=sum(r['scored'] for r in reports),
                missing_seasons=[r['season'] for r in reports if r['source_presence']=='MISSING_SEASON'],
                source_stage_counts=dict(Counter(r['stage'] for r in rows if 1990<=int(r['season'][:4])<=2013)),
                warning='The source has no stage column. Literal club names preserved; missing pairings can reflect label splits, not necessarily missing matches.')


def build(directory=PRIVATE, root=ROOT):
    protection=acquisition.protect(directory,root);manifest=acquisition.verify(directory)
    phase2raw=(directory/feasibility.OUTPUT).read_bytes();phase2=json.loads(phase2raw)
    if base.encode(feasibility.build(directory,root))!=phase2raw:
        raise ValueError('Phase 2 assessment no longer reproduces')
    hist_raw=(directory/feasibility.HIST).read_bytes();hist=feasibility.historical(hist_raw)
    if hist!=phase2['historical']['records']:
        raise ValueError('Historical observations differ from Phase 2')
    receipts=manifest['acquired']+manifest['reused_phase2'];by_year={}
    for r in receipts:
        year=int(r['original_filename'][:4])
        if year in by_year:raise ValueError('Duplicate modern season receipt')
        by_year[year]=r
    if set(by_year)!=set(range(2014,2026)):raise ValueError('Wrong twelve-season modern scope')
    modern=[];all_records=[];wide=[];overlaps={}
    variants={**feasibility.DIAGNOSTIC_VARIANTS}
    for year,receipt in sorted(by_year.items()):
        raw=(directory/receipt['path']).read_bytes();rows,notes=feasibility.parse_text(raw,year)
        regular=[r for r in rows if r['stage']=='REGULAR_SEASON'];assessment=feasibility.assess(regular,year)
        report=dict(source=receipt['path'],commit=receipt['commit'],sha256=receipt['sha256'],git_blob_sha1=receipt['git_blob_sha1'],
                    bytes=len(raw),assessment=assessment,all_observations=len(rows),other_stage_records=len(rows)-len(regular),
                    date_precision=date_precision(regular),records=rows,notes=notes,
                    source_headers=[n for n in notes if n['kind']=='comment'],encoding='UTF-8 strict',CRLF_lines=raw.count(b'\r\n'))
        modern.append(report);all_records.extend(rows)
        for flag in assessment['wide_rounds']:
            wide.append(dict(season=assessment['season'],source=receipt['path'],source_sha256=receipt['sha256'],details=flag,
                             date_scope='CANCELLED_SCHEDULE_ONLY' if all(r['FT'] is None for r in flag['fixtures']) else 'SCORED_SOURCE_DATES_WITH_POSSIBLE_SCHEDULED_SLOTS'))
        if year<=2024:
            historical=[r for r in hist if r['season']==f'{year}/{year+1}']
            scored=[r for r in regular if r['FT'] is not None]
            mapping=feasibility.OVERLAP_NAMES if year==2014 else {t:variants.get(t,t) for r in scored for t in (r['home'],r['away'])}
            overlaps[str(year)]=feasibility.compare(historical,scored,mapping)
    carried=carried_flags(phase2,modern)
    if overlaps['2014']!=phase2['overlap_2014']:
        raise ValueError('Approved boundary comparison changed')
    window=historical_window(hist);diagnosis=result_diagnosis(hist);dates=date_inventory(hist)
    if (diagnosis['contradiction_count']!=5489 or diagnosis['older_window_contradictions']!=1895 or
            dates['outside_source_season_count']!=1162):
        raise ValueError('Frozen Phase 2 diagnostic counts changed')
    context_raw=(directory/'documentary_context.json').read_bytes()
    affected={(w['season'],r['home'],r['away']) for w in wide for r in w['details']['fixtures']}
    return dict(scope='Ligue 1 Phase 3 source inventory only, not Phase 4 or historical certification',
                acquisition_sha256=base.sha((directory/acquisition.MANIFEST).read_bytes()),phase2_assessment_sha256=base.sha(phase2raw),
                protected=protection,modern=modern,modern_totals=dict(seasons=len(modern),
                    observed=sum(s['assessment']['observed'] for s in modern),score_bearing=sum(s['assessment']['scored'] for s in modern),
                    unscored=sum(s['assessment']['unscored'] for s in modern),other_stage=sum(s['other_stage_records'] for s in modern)),
                historical_source=dict(path=feasibility.HIST,sha256=base.sha(hist_raw),records=len(hist),
                    season_counts=dict(sorted(Counter(r['season'] for r in hist).items())),
                    window=window,result_diagnosis=diagnosis,date_diagnosis=dates),
                scheduling=dict(carried_phase2=carried,all_flags=wide,round_count=len(wide),unique_fixture_slots=len(affected),
                                warning='Wide span is not a structural error; source dates need independent historical review.'),
                club_labels=diagnostic_labels(all_records+hist),scored_source_overlaps=overlaps,
                phase2_2025_full_comparison=phase2['versions_2025'],
                documentary_context=dict(sha256=base.sha(context_raw),ledger=json.loads(context_raw),
                    warning='All Phase 2 evidence access/finality limitations carried unchanged; no new historical certification or processing policy.'),
                rights=base.RIGHTS,training_clearance='UNRESOLVED',redistribution_clearance='UNRESOLVED',
                proposed_canonical_league='Ligue 1',standardized_rows_generated=0)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args()
    raw=base.encode(build());target=PRIVATE/OUTPUT
    if args.check:
        if target.read_bytes()!=raw:raise ValueError('Inventory not byte-reproducible')
    else:base.save(target,raw)
    print('INVENTORY_BYTES',len(raw),'SHA256',base.sha(raw))
