"""Offline second-tier adapter; reuse audited parsing, shared conversion and validation.

PYTHONPATH=src .venv/bin/python -m scripts.standardize_second_bundesliga_results [--check]
"""
from collections import Counter, defaultdict
from copy import deepcopy
import argparse
import csv
import io
import json
from pathlib import Path

from scripts.artifact_io import check_overwrite, serialize_csv
from scripts.standardize_england_results import ROOT, convert_rows, digest
from scripts.standardize_bundesliga_results import json_bytes, identity
from scripts.validate_second_bundesliga import PRIVATE, ENG, OPENLIGA, build as audit_build, validate_season
from scripts.verify_second_bundesliga_review import bound_row, check_correction, check_samples
from toto_estimator.data import load_historical_data
from toto_estimator.historical_import import OUTPUT_COLUMNS

LEAGUE = '2. Bundesliga'
OUTPUT_NAMES = ('second_bundesliga_standardized_1990_2025.csv',
                'second_bundesliga_exceptions_1990_2025.json',
                'second_bundesliga_standardization_manifest.json')


def apply_verified_correction(record, correction, directory):
    check_correction(directory, correction)
    if record['source_row'] != correction['source']['source_row'] or record['season'] != '2005/2006':
        raise ValueError('Correction record binding failed')
    raw = correction['source']['original_fields']
    if (record['date'], record['home_team'], record['away_team'], record['home_goals'], record['away_goals']) != (
            raw['Date'], raw['home'], raw['visitor'], int(raw['hgoal']), int(raw['vgoal'])):
        raise ValueError('Correction parsed facts differ')
    result = dict(record)
    result.update(date=correction['replacements']['Date'], home_goals=int(correction['replacements']['hgoal']),
                  away_goals=int(correction['replacements']['vgoal']))
    return result


def convert_records(records, directory):
    # The shared converter requires one ordered club pairing per season per batch.
    # Partition the special season by its documented phase, without changing league,
    # season, date or ID identity. Validate the combined phase schedule separately.
    batches = defaultdict(list)
    for r in records:
        phase = ('first' if r['date'] < '1992-01-01' else 'second') if r['season'] == '1991/1992' else 'ordinary'
        h, a = r['home_goals'], r['away_goals']
        batches[phase].append(dict(Date=r['date'], Season=r['season'], HomeTeam=r['home_team'],
                                  AwayTeam=r['away_team'], hGoal=str(h), aGoal=str(a), Score=f'{h}-{a}',
                                  Result='H' if h > a else 'A' if h < a else 'D', Tier='2', Division=LEAGUE))
    standard, summaries = [], {}
    for phase, rows in sorted(batches.items()):
        content, summary = convert_rows(rows, directory, league=LEAGUE, tier='2',
                                       division_names={y: LEAGUE for y in range(1990, 2026)})
        summaries[phase] = summary
        for row in csv.DictReader(io.StringIO(content.decode())):
            row['home_goals'], row['away_goals'] = int(row['home_goals']), int(row['away_goals'])
            standard.append(row)
    if len({r['match_id'] for r in standard}) != len(standard) or len({identity(r) for r in standard}) != len(standard):
        raise ValueError('Duplicate match instance across batches')
    standard.sort(key=lambda r: (r['league'], r['season'], r['date'], r['home_team'], r['away_team']))
    facts = lambda r: tuple(r[k] for k in ('season', 'date', 'home_team', 'away_team', 'home_goals', 'away_goals'))
    if Counter(map(facts, standard)) != Counter(map(facts, records)):
        raise ValueError('Combined conversion changed match facts')
    content = serialize_csv(standard, OUTPUT_COLUMNS)
    load_historical_data(io.StringIO(content.decode()))
    return content, standard, summaries


def validate_coverage(records):
    if len(records) != 11488 or {r['season'] for r in records} != {f'{y}/{y+1}' for y in range(1990,2026)}:
        raise ValueError('Expected 11488 records and 36 completed seasons')
    reports = []
    for y in range(1990, 2026):
        rows = [r for r in records if r['season'] == f'{y}/{y+1}']
        report = validate_season(rows, y)
        if report['issues']:
            raise ValueError('Season schedule failed: ' + str(report))
        reports.append(report)
    return reports


def link_exceptions(policy, corrected, standard, directory, correction):
    by_source = {(ENG if r['season'] != '2025/2026' else OPENLIGA, r['source_row']): r for r in corrected}
    by_identity = {identity(r): r for r in standard}
    inventory = Counter(c['classification'] for c in policy['known_match_cases'])
    if inventory != Counter(COMPLETED_REPLAY=4, COMPLETED_REPLAY_AFTER_ABANDONMENT=2,
                            COMPLETED_THEN_AWARDED=1, REPORTED_MANIPULATION_RESULT_RETAINED=2):
        raise ValueError('Unexpected exception inventory')
    linked = []
    for case in policy['known_match_cases']:
        binding = case['source'];bound_row(directory, binding)
        record = by_source[(binding['source_file'], binding['source_row'])]
        match = by_identity[identity(record)]
        official = case['official_archived_fields']
        if (match['date'],match['home_goals'],match['away_goals']) != (official['Date'],int(official['hgoal']),int(official['vgoal'])):
            raise ValueError('Exception official outcome mismatch')
        if case['training_suitability'] != 'EXCLUDED' or not case['evidence']:
            raise ValueError('Missing exclusion evidence')
        item = deepcopy(case)
        item.update(match_id=match['match_id'], official_archived_result={k:match[k] for k in ('date','home_goals','away_goals')},
                    evidence_status='UNRESOLVED_CONCERN' if 'MANIPULATION' in case['classification'] else 'DOCUMENTED_EXCEPTION')
        if case.get('correction_id'):
            if case['correction_id'] != correction['correction_id']:
                raise ValueError('Wrong exception correction link')
            item['evidence'] = list(dict.fromkeys(item['evidence'] + correction['evidence']))
        linked.append(item)
    if len({e['match_id'] for e in linked}) != 9:
        raise ValueError('Duplicate exception links')
    if policy['unlisted_training_suitability'] != 'UNRESOLVED':
        raise ValueError('Unreviewed eligibility must remain unresolved')
    return dict(dataset=OUTPUT_NAMES[0], policy=policy['policy'], exhaustive=False,
                unlisted_match_training_suitability='UNRESOLVED', exceptions=linked,
                team_level_contexts=deepcopy(policy['team_level_notes']),
                team_context_policy='Two licence/standings sanctions are not additional fixture exceptions or fabricated awards.')


def build(directory=PRIVATE):
    inputs = {}
    def read(name, expected=None):
        content = (directory/name).read_bytes()
        if expected is not None and digest(content) != expected:
            raise ValueError('Reviewed input changed: ' + name)
        inputs[name] = dict(sha256=digest(content), bytes=len(content))
        return content
    for seal in ('checksums.json','verification/checksums.json'):
        for name, info in json.loads(read(seal)).items():
            read(('verification/' if seal.startswith('verification/') else '')+name, info['sha256'])
    fresh = audit_build(directory)
    for name, content in fresh.items():
        if read(name) != content:
            raise ValueError('Source audit differs from reviewed snapshot')
    audit = json.loads(fresh['structural_validation.json'])
    check_samples(json.loads(read('verification/independent_verification.json'))['matches'])
    corrections = json.loads(read('verification/verified_corrections.json'))['corrections']
    if len(corrections) != 1:
        raise ValueError('Expected single reviewed correction')
    correction = corrections[0]
    check_correction(directory, correction)
    policy = json.loads(read('verification/exception_policy.json'))
    records = deepcopy(audit['extracted_records']); applied = 0
    for i, r in enumerate(records):
        if r['season'] == '2005/2006' and r['source_row'] == correction['source']['source_row']:
            records[i] = apply_verified_correction(r, correction, directory);applied += 1
    if applied != 1:
        raise ValueError('Correction must apply exactly once')
    coverage = validate_coverage(records)
    content, standard, summary = convert_records(records, directory)
    repeat, _, _ = convert_records(list(reversed(records)), directory)
    if repeat != content:
        raise ValueError('Not reproducible under input reordering')
    # Recover phase/round annotations only for schedule validation, outside eight columns.
    annotated = {identity(r): r for r in records}
    enriched = [dict(r, **{k: annotated[identity(r)][k] for k in ('division', 'source_row')}) for r in standard]
    output_coverage = validate_coverage(enriched)
    for before, after in zip(coverage, output_coverage):
        if any(before[k] != after[k] for k in ('actual_matches', 'actual_teams', 'special_format', 'status')):
            raise ValueError('Output schedule changed')
    sidecar = link_exceptions(policy, records, standard, directory, correction)
    matches = {identity(r):r for r in standard}
    outputs = {OUTPUT_NAMES[0]:content, OUTPUT_NAMES[1]:json_bytes(sidecar)}
    manifest = dict(conversion_date='2026-11-05', converter='scripts.standardize_second_bundesliga_results',
                    schema=list(OUTPUT_COLUMNS), league=LEAGUE, season_format='YYYY/YYYY', records=11488, seasons=36,
                    source_provenance=json.loads(read('acquisition.json')), inputs=inputs,
                    identity='Shared importer SHA-256 of compact JSON [league,season,date,home,away]; phase preserved in lineage. Different dates distinguish legitimate repeated ordered pairs in 1991/92.',
                    method='Reuse source audit and phase schedule validation, shared convert_rows/importer and public historical loader. Partition 1991/92 by phase only to satisfy converter pairing gate; recombine without changing identifiers.',
                    season_validation=coverage, import_summaries=summary,
                    applied_corrections=[dict(correction,applied=True,applied_to='derived standardized output only')],
                    source_row_links=[dict(source_file=ENG if r['season']!='2025/2026' else OPENLIGA,
                                           source_row=r['source_row'],match_id=matches[identity(r)]['match_id'],
                                           division=r['division'],phase=('first' if r['date']<'1992-01-01' else 'second') if r['season']=='1991/1992' else 'regular',
                                           matchday=r.get('matchday')) for r in records],
                    exception_counts=dict(Counter(e['classification'] for e in sidecar['exceptions'])),
                    validations=['11488 rows; 36 seasons; exact eight columns; no missing fields; unique IDs and dated fixtures',
                                 'phase-aware and ordinary home-away schedules complete; one guarded correction only',
                                 'all previous source/evidence seals match; reversed-input bytes identical; public validator passes',
                                 'nine unique exception links with verified official fields; unlisted eligibility unresolved'],
                    code_sha256={str(p.relative_to(ROOT)):digest(p.read_bytes()) for p in [Path(__file__).resolve(),ROOT/'scripts/standardize_england_results.py',ROOT/'scripts/validate_second_bundesliga.py',ROOT/'scripts/verify_second_bundesliga_review.py',ROOT/'src/toto_estimator/historical_import.py']},
                    outputs={n:dict(sha256=digest(b),bytes=len(b)) for n,b in outputs.items()},
                    legal_clearance='UNRESOLVED upstream third-party rights. Preserve engsoccerdata noncommercial/attribution and GPL scope ambiguity; OpenFootball CC0 does not clear OpenLigaDB ODbL/upstream rights. No training or redistribution clearance inferred.',
                    ongoing_2026_2027='not acquired or included', training='No training/evaluation; unreviewed eligibility unresolved')
    outputs[OUTPUT_NAMES[2]] = json_bytes(manifest)
    return outputs


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    if not args.check:check_overwrite([PRIVATE/n for n in OUTPUT_NAMES])
    outputs=build()
    for name,content in outputs.items():
        if args.check:
            if (PRIVATE/name).read_bytes()!=content:raise ValueError('Saved output differs: '+name)
        else:
            with (PRIVATE/name).open('xb') as handle:handle.write(content)
        print(name+': SHA-256 '+digest(content))
    print('PASS: 11488 matches / 36 seasons; nine exceptions; one derivative correction; reproducible bytes.')


if __name__=='__main__':main()
