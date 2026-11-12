"""Offline Serie A adapter to the established TOTOdology importer/validator.

PYTHONPATH=src python3 -m scripts.standardize_serie_a_results [--check]
All outputs stay private. Existing outputs are refused; --check never replaces them.
"""
from collections import Counter, defaultdict
from copy import deepcopy
import argparse
import csv
from datetime import date
import io
import json
from pathlib import Path

from scripts.artifact_io import check_overwrite
from scripts.standardize_england_results import convert_rows, digest
from scripts.standardize_bundesliga_results import json_bytes, identity
from scripts.validate_serie_a import PRIVATE, ROOT, historical, football_txt
from scripts.verify_serie_a_review import bound_facts, date_collisions, review
from toto_estimator.historical_import import OUTPUT_COLUMNS, canonical_season
from toto_estimator.outcomes import outcome_from_goals
from toto_estimator.validation import exact_integer

LEAGUE = 'Serie A'
HISTORICAL = 'jalapic/data-raw/italy.csv'
RECENT = 'openfootball/2025-26/1-seriea.txt'
REVIEW_SHA256 = 'afaea816a68558bd6e91a931f67777ee6367cb96c7ca15316bb20dd026b8a10a'
OUTPUT_NAMES = ('serie_a_standardized_1990_2025.csv',
                'serie_a_exceptions_1990_2025.json',
                'serie_a_standardization_manifest.json')
FACTS = ('season', 'date', 'home_team', 'away_team', 'home_goals', 'away_goals')
DECISIONS = Counter(EXCLUDED=4, ELIGIBLE=1, UNRESOLVED=2)


def parsed_records(directory):
    """Reuse both audited source parsers; retain source location outside output rows."""
    old, old_issues, _ = historical(directory/HISTORICAL)
    new, new_issues = football_txt(directory/RECENT)
    if old_issues or new_issues:
        raise ValueError('Source parsing/consistency issues')
    records = []
    for source_file, rows in ((HISTORICAL, old), (RECENT, new)):
        for r in rows:
            records.append(dict(source_file=source_file, source_row=r['source_row'],
                                season=r['season'], date=r['date'], home_team=r['home'],
                                away_team=r['away'], home_goals=exact_integer(r['hg']),
                                away_goals=exact_integer(r['ag'])))
    return records


def source_key(record):
    return record['source_file'], record['source_row']


def apply_corrections(records, corrections, directory):
    """Apply exact evidence-bound date changes to copies, never to original files."""
    by_source, ids = {}, set()
    for correction in corrections:
        binding = correction['source']
        key = binding['source_file'], binding['source_row']
        if key in by_source or correction['correction_id'] in ids:
            raise ValueError('Duplicate correction binding/ID')
        if (correction['status'] != 'VERIFIED_PENDING_STANDARDIZATION'
                or correction['applied'] is not False
                or not correction['evidence']
                or not any(e['access'] in {'FULL_MATCH_PAGE','FULL_RESULTS_PAGE','FULL_REPORT'} for e in correction['evidence'])):
            raise ValueError('Correction lacks verified, unapplied evidence')
        replacements = correction['replacements']
        if set(replacements) != {'Date'} or 'Date' not in binding['original_fields']:
            raise ValueError('Only a bound source Date correction is allowed')
        new_date = replacements['Date']
        if date.fromisoformat(new_date).isoformat() != new_date or new_date == binding['original_fields']['Date']:
            raise ValueError('Noncanonical or unchanged correction date')
        # Checks whole-file SHA-256, physical row and every original source field.
        facts = bound_facts(directory, binding)
        by_source[key] = (correction, facts)
        ids.add(correction['correction_id'])
    result, applied, seen = [], [], set()
    for record in records:
        key = source_key(record)
        updated = dict(record)
        if key in by_source:
            if key in seen:
                raise ValueError('Correction would apply to multiple source records')
            correction, facts = by_source[key]
            if any(record[k] != facts[k] for k in facts):
                raise ValueError('Correction parsed/source facts differ')
            original = correction['source']['original_fields']
            expected_season = canonical_season(f"{original['Season']}/{int(original['Season'])+1}")
            if record['season'] != expected_season:
                raise ValueError('Correction season binding failed')
            new_date = correction['replacements']['Date']
            year = int(record['season'][:4])
            if not date(year,7,1) <= date.fromisoformat(new_date) <= date(year+1,6,30):
                raise ValueError('Correction outside season')
            updated['date'] = new_date
            applied.append(dict(deepcopy(correction), applied=True,
                                applied_to='derived standardized dataset only'))
            seen.add(key)
        result.append(updated)
    if seen != set(by_source):
        raise ValueError('Correction source record absent')
    return result, sorted(applied, key=lambda c:c['correction_id'])


def validate_coverage(records, *, years=range(1990,2026)):
    """Use competition-specific formats without weakening the shared validator."""
    years = tuple(years)
    groups = defaultdict(list)
    for r in records:
        groups[r['season']].append(r)
    wanted = {f'{y}/{y+1}' for y in years}
    expected_total = sum((18 if y<=2003 else 20)*(17 if y<=2003 else 19) for y in years)
    if set(groups) != wanted or len(records) != expected_total:
        raise ValueError('Unexpected season scope or match total')
    reports = []
    for year in years:
        season = f'{year}/{year+1}';rows = groups[season]
        n = 18 if year<=2003 else 20
        teams = {r[k] for r in rows for k in ('home_team','away_team')}
        pairs = Counter((r['home_team'],r['away_team']) for r in rows)
        if (len(teams)!=n or len(rows)!=n*(n-1)
                or set(pairs)!={(h,a) for h in teams for a in teams if h!=a}
                or any(count!=1 for count in pairs.values())):
            raise ValueError('Incomplete/duplicate home-away coverage: '+season)
        if any(sum(r['home_team']==t for r in rows)!=n-1 or sum(r['away_team']==t for r in rows)!=n-1 for t in teams):
            raise ValueError('Unbalanced home/away appearances')
        reports.append(dict(season=season,teams=n,matches=len(rows),expected_matches=n*(n-1),status='PASS'))
    return reports


def convert_records(records, directory):
    rows=[]
    for r in records:
        h,a=r['home_goals'],r['away_goals']
        rows.append(dict(Date=r['date'],Season=r['season'],HomeTeam=r['home_team'],
                         AwayTeam=r['away_team'],hGoal=str(h),aGoal=str(a),Score=f'{h}-{a}',
                         Result={'1':'H','X':'D','2':'A'}[outcome_from_goals(h,a)],Tier='1',Division=LEAGUE))
    content, summary = convert_rows(rows,directory,league=LEAGUE,tier='1',
                                   division_names={y:LEAGUE for y in range(1990,2026)})
    reader=csv.DictReader(io.StringIO(content.decode('utf-8')))
    if tuple(reader.fieldnames or ())!=OUTPUT_COLUMNS:
        raise ValueError('Output must have exactly the eight standard columns')
    standard=[]
    for row in reader:
        row['home_goals'],row['away_goals']=int(row['home_goals']),int(row['away_goals'])
        if row['league']!=LEAGUE:
            raise ValueError('Wrong output league')
        standard.append(row)
    if Counter(tuple(r[k] for k in FACTS) for r in standard)!=Counter(tuple(r[k] for k in FACTS) for r in records):
        raise ValueError('Conversion changed historical facts')
    return content,standard,summary


def link_exceptions(policy, originals, corrected, standard, applied, directory):
    if policy['unlisted_training_suitability']!='UNRESOLVED':
        raise ValueError('Unreviewed matches must remain unresolved')
    cases=policy['known_match_cases']
    if Counter(c['training_suitability'] for c in cases)!=DECISIONS:
        raise ValueError('Seven reviewed exception decisions changed')
    if Counter(c['classification'] for c in cases)!=Counter(
            COMPLETED_REPLAY_AFTER_ABANDONMENT=3,UNPLAYED_ADMINISTRATIVE_AWARD=1,
            FIRST_PLAYED_AFTER_OVERTURNED_AWARD=1,INTERRUPTED_THEN_RESUMED_AND_COMPLETED=2):
        raise ValueError('Reviewed exception classifications changed')
    eligibility_by_class={
        'COMPLETED_REPLAY_AFTER_ABANDONMENT':'EXCLUDED',
        'UNPLAYED_ADMINISTRATIVE_AWARD':'EXCLUDED',
        'FIRST_PLAYED_AFTER_OVERTURNED_AWARD':'ELIGIBLE',
        'INTERRUPTED_THEN_RESUMED_AND_COMPLETED':'UNRESOLVED',
    }
    if any(c['training_suitability']!=eligibility_by_class[c['classification']] for c in cases):
        raise ValueError('Exception decision/classification mismatch')
    if (len({(c['source']['source_file'],c['source']['source_row']) for c in cases})!=7
            or len({c['case_id'] for c in cases})!=7):
        raise ValueError('Duplicate exception source or case ID')
    raw_by_key={source_key(r):r for r in originals}
    corrected_by_key={source_key(r):r for r in corrected}
    standard_by_identity={identity(r):r for r in standard}
    applied_by_key={(c['source']['source_file'],c['source']['source_row']):c for c in applied}
    linked=[];seen=set();case_ids=set()
    for case in cases:
        binding=case['source'];key=(binding['source_file'],binding['source_row'])
        if key in seen or key not in raw_by_key or case['case_id'] in case_ids:
            raise ValueError('Duplicate/dangling exception reference')
        seen.add(key);case_ids.add(case['case_id'])
        facts=bound_facts(directory,binding)
        raw=raw_by_key[key]
        if any(raw[k]!=facts[k] for k in facts):
            raise ValueError('Exception source facts differ')
        record=corrected_by_key[key]
        match=standard_by_identity.get(identity(record))
        if match is None or any(match[k]!=record[k] for k in FACTS):
            raise ValueError('Exception does not link to preserved final fixture')
        if (match['date']!=case['official_final_date']
                or f"{match['home_goals']}-{match['away_goals']}"!=case['official_final_result']):
            raise ValueError('Exception official date/result mismatch')
        if not case['evidence'] or not case['training_reason']:
            raise ValueError('Missing exception evidence/reasoning')
        item=deepcopy(case)
        item.update(match_id=match['match_id'],season=match['season'],league=LEAGUE,
                    date=match['date'],home_team=match['home_team'],away_team=match['away_team'],
                    official_archived_result={k:match[k] for k in ('date','home_goals','away_goals')},
                    ordinary_90_minute_training_eligible={'EXCLUDED':False,'ELIGIBLE':True,'UNRESOLVED':None}[case['training_suitability']],
                    conservative_training_action={'EXCLUDED':'EXCLUDE','ELIGIBLE':'MAY_INCLUDE_SUBJECT_TO_FUTURE_POLICY_AND_RIGHTS','UNRESOLVED':'HOLD_OUT_PENDING_REVIEW'}[case['training_suitability']])
        if key in applied_by_key:
            correction=applied_by_key[key]
            if case.get('correction_id')!=correction['correction_id']:
                raise ValueError('Exception/correction linkage mismatch')
            item['applied_correction']=deepcopy(correction)
        elif case.get('source_correction_required'):
            raise ValueError('Missing exception correction')
        linked.append(item)
    if len({c['match_id'] for c in linked})!=7:
        raise ValueError('Exception links must identify seven distinct matches')
    return dict(schema_version=1,dataset=OUTPUT_NAMES[0],exhaustive=False,
                eligibility_scope=policy['eligibility_scope'],policy_sources=policy['policy_sources'],
                unlisted_match_training_suitability='UNRESOLVED',
                unlisted_conservative_training_action='HOLD_OUT_PENDING_REVIEW',
                policy='Preserve every recognized final fixture in the archive. Metadata is not a training filter; unresolved cases must not be assumed eligible.',
                exceptions=sorted(linked,key=lambda e:e['case_id']))


def verify_protected():
    content=(PRIVATE/'standardization_protected_before.json').read_bytes()
    fingerprints=json.loads(content)
    for name,sha in fingerprints.items():
        if digest((ROOT/name).read_bytes())!=sha:
            raise ValueError('Pre-standardization protected file changed: '+name)
    return content,len(fingerprints)


def build():
    seal=(PRIVATE/'verification/review_manifest.json').read_bytes()
    if digest(seal)!=REVIEW_SHA256:
        raise ValueError('Reviewed evidence seal changed')
    protected,protected_count=verify_protected()
    review_result=review()  # Reuses source audit, all sample/correction/policy guards.
    saved_review=json.loads((PRIVATE/'verification/review_result.json').read_text())
    if json.loads(json_bytes(review_result))!=saved_review:
        raise ValueError('Independent review no longer reproduces')
    read=lambda name:json.loads((PRIVATE/name).read_text())
    corrections=read('verification/verified_corrections.json')['corrections']
    policy=read('verification/exception_policy.json')
    if len(corrections)!=11:
        raise ValueError('Expected exactly eleven verified date corrections')
    originals=parsed_records(PRIVATE)
    corrected,applied=apply_corrections(originals,corrections,PRIVATE)
    if len(applied)!=11:
        raise ValueError('Each correction must apply exactly once')
    coverage=validate_coverage(corrected)
    if date_collisions([dict(r,home=r['home_team'],away=r['away_team']) for r in corrected]):
        raise ValueError('Unresolved same-team/date collision')
    # Prove each source location survives once and only an approved date differs.
    if len({source_key(r) for r in originals})!=12644:
        raise ValueError('Duplicated/missing original source locations')
    by_key={source_key(r):r for r in corrected}
    allowed={(c['source']['source_file'],c['source']['source_row']):c['replacements']['Date'] for c in applied}
    for original in originals:
        expected=dict(original)
        if source_key(original) in allowed:expected['date']=allowed[source_key(original)]
        if by_key[source_key(original)]!=expected:
            raise ValueError('Unintended historical fact change')
    content,standard,summary=convert_records(corrected,PRIVATE)
    repeated,_,_=convert_records(list(reversed(corrected)),PRIVATE)
    if content!=repeated or validate_coverage(standard)!=coverage:
        raise ValueError('Non-reproducible bytes or altered season coverage')
    matches={identity(r):r for r in standard}
    for correction in applied:
        key=correction['source']['source_file'],correction['source']['source_row']
        correction['match_id']=matches[identity(by_key[key])]['match_id']
    sidecar=link_exceptions(policy,originals,corrected,standard,applied,PRIVATE)
    outputs={OUTPUT_NAMES[0]:content,OUTPUT_NAMES[1]:json_bytes(sidecar)}
    # List actual frozen inputs, not future unrelated files in the private folder.
    input_paths=sorted([PRIVATE/'standardization_protected_before.json',
                        *(ROOT/name for name in json.loads(protected)
                          if (ROOT/name).resolve().is_relative_to(PRIVATE.resolve()))])
    provenance=read('validation_provenance.json')
    manifest=dict(conversion_date='2026-11-12',timezone='Europe/Budapest',converter='scripts.standardize_serie_a_results',
                  schema=list(OUTPUT_COLUMNS),league=LEAGUE,season_format='YYYY/YYYY',records=len(standard),seasons=len(coverage),
                  method='Existing Serie A source parsers -> evidence-bound date-only copies -> shared convert_rows -> import_historical_csvs -> load_historical_data/validate_historical_data. No alias reconciliation, filtering or integration.',
                  identity='Existing importer full SHA-256 of compact UTF-8 JSON [league,season,ISO date,home team,away team], ensure_ascii=False, separators=(comma,colon). Scores/source paths/input order excluded; corrected dates participate in identity.',
                  source_provenance=read('acquisition.json'),source_mapping={
                      HISTORICAL:'Date, starting Season year, home, visitor, hgoal, vgoal; canonical season syntax only. Source FT, result, totgoal and goaldif audited before omission.',
                      RECENT:'Inherit explicit Football.TXT date; parse stated home/away and final goals. Retain exact club spellings. Scorer/time/halftime annotations are outside the eight-column schema.'},
                  protected_files_unchanged=protected_count,protected_fingerprint_sha256=digest(protected),
                  reviewed_evidence_seal_sha256=REVIEW_SHA256,independent_review=review_result,
                  inputs={str(p.relative_to(PRIVATE)):dict(bytes=p.stat().st_size,sha256=digest(p.read_bytes())) for p in input_paths},
                  season_validation=coverage,import_summary=summary,applied_corrections=applied,
                  source_row_links=[dict(source_file=r['source_file'],source_row=r['source_row'],match_id=matches[identity(r)]['match_id'],
                                         corrections=[c['correction_id'] for c in applied if (c['source']['source_file'],c['source']['source_row'])==source_key(r)])
                                    for r in sorted(corrected,key=source_key)],
                  exception_classification_counts=dict(Counter(e['classification'] for e in sidecar['exceptions'])),
                  exception_training_suitability_counts=dict(Counter(e['training_suitability'] for e in sidecar['exceptions'])),
                  unlisted_training_suitability='UNRESOLVED',ongoing_2026_2027='not acquired or included',
                  validations=['12644 records, 36 seasons, exact eight-column schema and no missing values',
                               'unique deterministic IDs and season home-away fixtures; complete historical schedules',
                               'each of 11 source-hash/row/full-field-bound corrections applied exactly once to date only',
                               'all source facts preserved except documented derived dates; no original or prior artifact overwritten',
                               'public historical loader/validator preserves all saved facts',
                               'reversed-input conversion yields identical CSV bytes',
                               'seven unique exception match-ID links; four exclusions, one eligible, two unresolved',
                               'full --check regeneration compares CSV, exception metadata and manifest byte-for-byte'],
                  code_sha256={str(p.relative_to(ROOT)):digest(p.read_bytes()) for p in (
                      Path(__file__).resolve(),ROOT/'scripts/validate_serie_a.py',ROOT/'scripts/verify_serie_a_review.py',
                      ROOT/'scripts/standardize_england_results.py',ROOT/'scripts/standardize_bundesliga_results.py',
                      ROOT/'scripts/artifact_io.py',ROOT/'src/toto_estimator/historical_import.py',
                      ROOT/'src/toto_estimator/data.py',ROOT/'src/toto_estimator/validation.py',ROOT/'src/toto_estimator/outcomes.py')},
                  outputs={name:dict(bytes=len(data),sha256=digest(data)) for name,data in outputs.items()},
                  attribution='James P. Curley / engsoccerdata; OpenFootball / italy. Original compiler citations, commit URLs, source notices and licences retained in source_provenance and private originals.',
                  rights=provenance['rights'],legal_clearance='UNRESOLVED upstream rights and engsoccerdata noncommercial/GPL-scope ambiguity. OpenFootball CC0 covers rights held only. No training, hosting or redistribution clearance inferred.',
                  acquisition_stage_limits=provenance['limitations'],
                  assurance_limits='Review establishes bounded external agreement and documented exception decisions, not exhaustive score/status certification. Historical legal club identities and unlisted training eligibility remain unresolved. Standardization adds no new independent result certification.')
    outputs[OUTPUT_NAMES[2]]=json_bytes(manifest)
    verify_protected()
    return outputs


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true',help='regenerate and compare all saved outputs without replacement')
    args=parser.parse_args()
    if not args.check:check_overwrite([PRIVATE/name for name in OUTPUT_NAMES])
    outputs=build()
    if args.check:
        for name,content in outputs.items():
            if (PRIVATE/name).read_bytes()!=content:
                raise ValueError('Saved output differs: '+name)
    else:
        for name,content in outputs.items():
            with (PRIVATE/name).open('xb') as handle:handle.write(content)
    for name,content in outputs.items():print(name+': SHA-256 '+digest(content))
    print('PASS: 12644 matches / 36 seasons; eleven derived date corrections; seven exception links.')


if __name__=='__main__':main()
