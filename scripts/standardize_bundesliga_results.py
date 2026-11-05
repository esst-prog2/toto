"""Offline Bundesliga adapter to the shared historical importer and validator.

PYTHONPATH=src .venv/bin/python -m scripts.standardize_bundesliga_results [--check]
Creates private outputs exclusively; --check rebuilds without replacing anything.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from copy import deepcopy
import csv
import io
import json
from pathlib import Path

from scripts.artifact_io import check_overwrite
from scripts.standardize_england_results import ROOT, convert_rows, digest
from scripts.validate_bundesliga_csv import audit_file
from toto_estimator.historical_import import OUTPUT_COLUMNS

PRIVATE = ROOT / 'data/private/germany'
LEAGUE = 'Bundesliga'
OUTPUT_NAMES = ('bundesliga_standardized_1990_2025.csv',
                'bundesliga_exceptions_1990_2025.json',
                'bundesliga_standardization_manifest.json')
CORRECTION_ID = 'BL-DATE-1993-94-REPLAY'
REASONS = {
    'COMPLETED_THEN_AWARDED': 'Official awarded outcome differs from the completed on-field result.',
    'COMPLETED_REPLAY_AFTER_ANNULMENT': 'Completed replay after annulment; excluded conservatively pending an explicit future replay modelling policy.',
    'ABANDONED_THEN_AWARDED': 'Not a normally completed 90-minute match; official awarded score is not a completed on-field final.',
    'INTERRUPTED_COMPLETED_THEN_AWARDED': 'Interrupted and resumed/completed match with a subsequent administrative outcome replacing the played score.',
}


def json_bytes(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode('utf-8')


def identity(row):
    return tuple(row[k] for k in ('season', 'date', 'home_team', 'away_team'))


def apply_correction(record, original_fields, source_file, source_sha256, correction):
    """Return a copy only after evidence, source and exact-field guards pass."""
    if (correction.get('status') != 'VERIFIED_PENDING_STANDARDIZATION'
            or correction.get('applied') is not False
            or not correction.get('sources') or not correction.get('justification')):
        raise ValueError('correction lacks verified, unapplied evidence')
    if correction['source_file'] != source_file or correction['source_sha256'] != source_sha256:
        raise ValueError('correction source checksum/file guard failed')
    if record['source_row'] != correction['source_row']:
        raise ValueError('correction source row guard failed')
    if any(original_fields.get(k) != v for k, v in correction['expected_source_fields'].items()):
        raise ValueError('correction expected source fields guard failed')
    if correction['field'] != 'Date' or record['date'] != correction['source_value']:
        raise ValueError('unsupported correction or date guard failed')
    if correction['official_score'] != {k: record[k] for k in ('home_goals', 'away_goals')}:
        raise ValueError('correction score guard failed')
    result = dict(record)
    result['date'] = correction['verified_value']
    return result


def convert_bundesliga_rows(records, directory):
    """Adapt audited facts to the shared converter; never map club aliases."""
    rows = []
    for r in records:
        h, a = r['home_goals'], r['away_goals']
        rows.append(dict(Date=r['date'], Season=r['season'], HomeTeam=r['home_team'],
                         AwayTeam=r['away_team'], hGoal=str(h), aGoal=str(a), Score=f'{h}-{a}',
                         Result='H' if h > a else 'A' if h < a else 'D',
                         Tier='1', Division=LEAGUE))
    return convert_rows(rows, directory, league=LEAGUE, tier='1',
                        division_names={year: LEAGUE for year in range(1990, 2026)})


def validate_coverage(records):
    groups = defaultdict(list)
    for r in records:
        groups[r['season']].append(r)
    expected_seasons = {f'{y}/{y+1}' for y in range(1990, 2026)}
    if set(groups) != expected_seasons or len(records) != 11090:
        raise ValueError('expected exactly 11090 records across 36 completed seasons')
    report = []
    for season, rows in sorted(groups.items()):
        n = 20 if season == '1991/1992' else 18
        teams = {r[k] for r in rows for k in ('home_team', 'away_team')}
        pairs = Counter((r['home_team'], r['away_team']) for r in rows)
        if (len(teams) != n or len(rows) != n*(n-1)
                or set(pairs) != {(h, a) for h in teams for a in teams if h != a}
                or any(count != 1 for count in pairs.values())):
            raise ValueError('incomplete/duplicate home-away fixture coverage: ' + season)
        report.append(dict(season=season, teams=n, matches=len(rows), expected_matches=n*(n-1),
                           home_away_coverage='PASS'))
    return report


def link_exceptions(policy, originals, standardized, applied, acquisition):
    """Link reviewed exceptions; no eligibility is inferred for unlisted matches."""
    by_identity = {identity(r): r for r in standardized}
    corrections = {(c['source_file'], c['source_row']): c for c in applied}
    linked, seen = [], set()
    for e in policy['exceptions']:
        key = (e['source_file'], e['source_row'])
        if key in seen or key not in originals:
            raise ValueError('duplicate or dangling exception source reference')
        seen.add(key)
        raw, record, source_sha = originals[key]
        if raw != e['original_fields'] or source_sha != e['source_sha256']:
            raise ValueError('exception source row/checksum guard failed')
        corrected = dict(record)
        if key in corrections:
            correction = corrections[key]
            if e.get('correction_id') != correction['correction_id']:
                raise ValueError('exception/correction linkage mismatch')
            corrected['date'] = correction['verified_value']
        match = by_identity.get(identity(corrected))
        if match is None or (match['home_goals'], match['away_goals']) != (record['home_goals'], record['away_goals']):
            raise ValueError('exception does not link to the preserved official result')
        if e['official_archive_score'] != f"{match['home_goals']}-{match['away_goals']}":
            raise ValueError('exception archived score mismatch')
        classification = e['classification']
        if classification not in REASONS:
            raise ValueError('unreviewed exception classification')
        eligible = e.get('ordinary_90_minute_training_eligible')
        # Only an explicit reviewed exclusion is known for these exceptional cases.
        suitability = 'EXCLUDED' if eligible is False and e.get('evidence') else 'UNRESOLVED'
        item = dict(exception_id=e['exception_id'], match_id=match['match_id'],
                    exception_type=classification, season=match['season'], date=match['date'],
                    home_team=match['home_team'], away_team=match['away_team'],
                    official_archived_result={k: match[k] for k in ('home_goals', 'away_goals')},
                    on_field_result=e.get('on_field_score'),
                    on_field_result_is_completed_final=e.get('on_field_score_is_completed_final'),
                    ordinary_90_minute_training_suitability=suitability,
                    reason=REASONS[classification] if suitability == 'EXCLUDED' else 'Insufficient reviewed eligibility evidence.',
                    source=dict(file=e['source_file'], sha256=source_sha, row=e['source_row'],
                                url=acquisition[e['season']]['url']),
                    supporting_evidence=e['evidence'])
        if 'annulled_original' in e:
            item['annulled_original'] = deepcopy(e['annulled_original'])
        if key in corrections:
            item['correction'] = corrections[key]
            item['supporting_evidence'] = list(dict.fromkeys(e['evidence'] + corrections[key]['sources']))
        linked.append(item)
    if len({r['match_id'] for r in linked}) != len(linked):
        raise ValueError('duplicate exception match IDs')
    return dict(schema_version=1, match_dataset=OUTPUT_NAMES[0],
                policy=policy['policy'], exhaustive=False,
                unlisted_match_training_suitability='UNRESOLVED',
                unlisted_reason='No exhaustive finished-status/administrative-decision audit; absence from the targeted exception register does not certify eligibility.',
                exceptions=sorted(linked, key=lambda e: e['exception_id']))


def build(directory: Path = PRIVATE):
    base = directory / 'csv_history'
    inputs = {}

    def read_checked(name, expected=None):
        path = base/name
        content = path.read_bytes()
        if expected is not None and digest(content) != expected:
            raise ValueError('previously reviewed input changed: ' + name)
        inputs['csv_history/'+name] = dict(sha256=digest(content), bytes=len(content))
        return content

    # Keep the acquisition and prior independent-review snapshots immutable.
    for name, info in json.loads((base/'checksums.json').read_text()).items():
        read_checked(name, info['sha256'])
    for name, info in json.loads((base/'verification/checksums.json').read_text()).items():
        read_checked('verification/'+name, info['sha256'])
    read_checked('checksums.json')
    read_checked('verification/checksums.json')
    acquisition = json.loads(read_checked('acquisition.json'))
    correction_evidence = json.loads(read_checked('verification/verified_corrections.json'))
    corrections = correction_evidence['corrections']
    if (len(corrections) != 1 or corrections[0]['correction_id'] != CORRECTION_ID
            or corrections[0]['source_value'] != '1994-04-03'
            or corrections[0]['verified_value'] != '1994-05-03'
            or corrections[0]['official_score'] != dict(home_goals=5, away_goals=0)):
        raise ValueError('only the documented Bayern-Nurnberg replay-date correction is authorized')
    policy = json.loads(read_checked('verification/exception_policy.json'))
    if Counter(e['classification'] for e in policy['exceptions']) != Counter({
            'COMPLETED_THEN_AWARDED': 1, 'COMPLETED_REPLAY_AFTER_ANNULMENT': 1,
            'ABANDONED_THEN_AWARDED': 2, 'INTERRUPTED_COMPLETED_THEN_AWARDED': 1}):
        raise ValueError('reviewed exception inventory changed')
    expected_seasons = {f'{y}/{y+1}' for y in range(1990, 2026)}
    if set(acquisition['files']) != expected_seasons:
        raise ValueError('acquisition season scope differs')
    expected_audits = {s['season']: s for s in json.loads(read_checked('structural_validation.json'))['seasons']}
    records, originals, applied = [], {}, []
    for season, entry in sorted(acquisition['files'].items()):
        read_checked(entry['file'], entry['sha256'])
        audit = audit_file(base/entry['file'], season, entry['source_kind'], include_records=True)
        source_records = audit.pop('records')
        expected = {k: v for k, v in expected_audits[season].items() if k not in ('source_url', 'file', 'sha256')}
        # JSON report stringifies round keys; compare canonical JSON-compatible values.
        if json.loads(json_bytes(audit)) != expected:
            raise ValueError('fresh source audit differs from reviewed snapshot: ' + season)
        allowed_issues = [dict(source_row=284, code='halftime_exceeds_fulltime', detail='1-3')] if season == '1992/1993' else []
        if audit['issues'] != allowed_issues:
            raise ValueError('unreviewed source anomaly: ' + season)
        encoding = 'utf-8-sig' if entry['source_kind'] == 'early' else 'ISO-8859-1'
        with (base/entry['file']).open(encoding=encoding, newline='') as handle:
            raw_rows = list(csv.DictReader(handle))
        for record in source_records:
            raw = raw_rows[record['source_row']-2]
            key = (entry['file'], record['source_row'])
            originals[key] = (raw, dict(record), entry['sha256'])
            for c in corrections:
                if key == (c['source_file'], c['source_row']):
                    record = apply_correction(record, raw, entry['file'], entry['sha256'], c)
                    applied.append(dict(c, applied=True, applied_to='derived standardized dataset only'))
            records.append(record)
    if len(applied) != 1:
        raise ValueError('correction must apply exactly once')
    coverage = validate_coverage(records)
    content, summary = convert_bundesliga_rows(records, directory)
    repeated, _ = convert_bundesliga_rows(list(reversed(records)), directory)
    if repeated != content:
        raise ValueError('conversion is not byte-reproducible under input reordering')
    standard = list(csv.DictReader(io.StringIO(content.decode('utf-8'))))
    for r in standard:
        r['home_goals'], r['away_goals'] = int(r['home_goals']), int(r['away_goals'])
    if any(r['league'] != LEAGUE for r in standard):
        raise ValueError('incorrect output league')
    output_coverage = validate_coverage(standard)
    if output_coverage != coverage:
        raise ValueError('output coverage changed')
    sidecar = link_exceptions(policy, originals, standard, applied, acquisition['files'])
    if len(sidecar['exceptions']) != 5:
        raise ValueError('expected five match-linked exceptions')
    by_identity = {identity(r): r for r in standard}
    lineage = []
    for (file, row), (_, original, _) in sorted(originals.items()):
        corrected = dict(original)
        ids = []
        for c in applied:
            if (file, row) == (c['source_file'], c['source_row']):
                corrected['date'] = c['verified_value']; ids.append(c['correction_id'])
        lineage.append(dict(source_file=file, source_row=row,
                            match_id=by_identity[identity(corrected)]['match_id'], corrections=ids))
    outputs = {OUTPUT_NAMES[0]: content, OUTPUT_NAMES[1]: json_bytes(sidecar)}
    manifest = dict(conversion_date='2026-11-05', converter='scripts/standardize_bundesliga_results.py',
                    shared_conversion='audit_file(include_records=True) -> standardize_england_results.convert_rows -> import_historical_csvs -> load_historical_data',
                    schema=list(OUTPUT_COLUMNS), league=LEAGUE, season_format='YYYY/YYYY',
                    identity='Existing importer SHA-256 of compact UTF-8 JSON [league,season,ISO date,home team,away team]; goals/path/order excluded.',
                    mapping='Reuse audited source parsing: early weekday/game-count syntax removed only as schema annotations; no team alias changes. DataHub ISO dates/names/goals retained. Only the evidence-bound replay date changes in the derivative. Official awarded outcomes retained.',
                    records=11090, seasons=36, ongoing_2026_2027='not acquired, merged or standardized',
                    source_files=acquisition['files'], inputs=inputs,
                    code_sha256={str(p.relative_to(ROOT)): digest(p.read_bytes()) for p in (
                        Path(__file__).resolve(), ROOT/'scripts/validate_bundesliga_csv.py',
                        ROOT/'scripts/standardize_england_results.py', ROOT/'scripts/artifact_io.py',
                        ROOT/'src/toto_estimator/historical_import.py', ROOT/'src/toto_estimator/data.py',
                        ROOT/'src/toto_estimator/validation.py', ROOT/'src/toto_estimator/outcomes.py')},
                    season_validation=coverage, import_summary=summary,
                    applied_corrections=applied, source_row_links=lineage,
                    validations=['all original and reviewed-evidence SHA-256 fingerprints match',
                                 'fresh source audit matches reviewed snapshot; only explained E1 halftime warning retained',
                                 '11090 rows, 36 seasons, exact eight-column schema and no missing fields',
                                 'unique deterministic IDs and fixtures; no importer rejection or dropped records',
                                 'complete home-away pairings including 20-team 1991/1992',
                                 'source dates/teams/goals preserved except one guarded verified date correction',
                                 'public historical loader/validator passes without factual changes',
                                 'reversed-input conversion yields identical bytes',
                                 'five exception references bind exact original rows and output IDs/results'],
                    outputs={name: dict(bytes=len(data), sha256=digest(data)) for name, data in outputs.items()},
                    exception_counts=dict(Counter(e['exception_type'] for e in sidecar['exceptions'])),
                    licence='Early publisher CC0 1.0; DataHub ODC-PDDL-1.0. Original declarations and source references retained in csv_history/metadata and acquisition.json.',
                    legal_clearance='UNRESOLVED upstream third-party rights: publisher dedications only cover rights held. No model-use or redistribution clearance claimed; local preparation only.',
                    assurance_limits='Targeted, non-exhaustive exception register and 20 full-evidence sample comparisons plus four indexed-only corroborations. Unlisted training suitability unresolved, not assumed eligible. See docs/bundesliga-validation.md.')
    outputs[OUTPUT_NAMES[2]] = json_bytes(manifest)
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='rebuild and compare all saved outputs; never replace')
    args = parser.parse_args()
    if not args.check:
        check_overwrite([PRIVATE/name for name in OUTPUT_NAMES])
    outputs = build()
    if args.check:
        for name, content in outputs.items():
            if (PRIVATE/name).read_bytes() != content:
                raise ValueError('saved output differs from reproducible conversion: ' + name)
        print('PASS: all three outputs reproduce byte-for-byte.')
    else:
        for name, content in outputs.items():
            with (PRIVATE/name).open('xb') as handle:
                handle.write(content)
        print('Created 11090 private standardized matches across 36 seasons; five exception links.')
    for name, content in outputs.items():
        print(f'{name}: SHA-256 {digest(content)}')


if __name__ == '__main__':
    main()
