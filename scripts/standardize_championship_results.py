"""Standardize the local Tier 2 snapshot through the shared England converter.

PYTHONPATH=src .venv/bin/python -m scripts.standardize_championship_results [--check]
No downloads or model calls. Creation refuses existing outputs; --check never replaces them.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from scripts.artifact_io import check_overwrite
from scripts.standardize_england_results import PRIVATE, ROOT, convert_rows, digest
from scripts.validate_championship_results import FUTURE_LEAGUE, championship_audit, historical_name
from toto_estimator.historical_import import OUTPUT_COLUMNS

LEAGUE = FUTURE_LEAGUE
DIVISIONS = {year: historical_name(year) for year in range(1990, 2027)}
OUTPUT_NAMES = ('championship_standardized_1990_2025.csv',
                'championship_standardized_2026_2027_ongoing.csv',
                'championship_standardization_manifest.json')


def convert_championship_rows(rows, directory):
    """Supply competition metadata to the existing converter, without new row logic."""
    return convert_rows(rows, directory, league=LEAGUE, tier='2', division_names=DIVISIONS)


def build(directory: Path = PRIVATE) -> dict[str, bytes]:
    provenance = json.loads((directory/'championship_provenance.json').read_text())
    source = directory/'EnglandLeagueResults.csv'
    if digest(source.read_bytes()) != provenance['source_sha256']:
        raise ValueError('original source checksum differs from validated snapshot')
    for name, info in provenance['outputs'].items():
        if digest((directory/name).read_bytes()) != info['sha256']:
            raise ValueError(f'previously validated Championship artifact changed: {name}')
    verification_path = directory/'championship_independent_verification_2026-11-05.json'
    verification = json.loads(verification_path.read_text())
    if verification['selection']['historical_export_sha256'] != digest((directory/'championship_1990_2025.csv').read_bytes()):
        raise ValueError('independently sampled export differs from this snapshot')
    _, source_count, selected, issues, seasons, playoff_checks = championship_audit(source)
    if issues or [s['status'] for s in seasons] != ['PASS']*36 + ['ONGOING']:
        raise ValueError(f'Championship source audit/coverage failed: {issues}')
    historical = [r for _,r in selected if 1990 <= int(r['Season'][:4]) <= 2025]
    ongoing = [r for _,r in selected if r['Season']=='2026/2027']
    if (len(historical),len(ongoing),len(selected)) != (19872,168,20040):
        raise ValueError('expected exactly 19872 historical and 168 ongoing snapshot records')
    for rows, name in ((historical,'championship_1990_2025.csv'),
                       (ongoing,'championship_2026_2027_ongoing.csv')):
        with (directory/name).open(encoding='utf-8',newline='') as handle:
            if list(csv.DictReader(handle)) != rows:
                raise ValueError(f'extract does not match original source partition: {name}')
    outputs, summaries = {}, {}
    for rows, name in zip((historical,ongoing),OUTPUT_NAMES[:2]):
        content, summary = convert_championship_rows(rows,directory)
        repeat, _ = convert_championship_rows(list(reversed(rows)),directory)
        if content != repeat:
            raise ValueError('conversion does not reproduce under source row reordering')
        outputs[name] = content
        summaries[name] = summary
    # Explicitly verify uniqueness across both partitions as well as within them.
    combined = [r for content in outputs.values()
                for r in csv.DictReader(content.decode('utf-8').splitlines())]
    if len({r['match_id'] for r in combined}) != len(combined):
        raise ValueError('match ID collision across completed/ongoing partitions')
    input_names = ['EnglandLeagueResults.csv','championship_1990_2025.csv',
                   'championship_2026_2027_ongoing.csv','championship_provenance.json',
                   verification_path.name,'LICENCE.md']
    manifest = dict(
        conversion_date='2026-11-05', source_url=provenance['source_url'],
        source_commit_sha=provenance['source_commit_sha'], retrieval_date=provenance['retrieval_date'],
        source_rows=source_count, source_sha256=provenance['source_sha256'],
        inputs={name:dict(sha256=digest((directory/name).read_bytes()),bytes=(directory/name).stat().st_size)
                for name in input_names},
        converter='scripts/standardize_championship_results.py',
        shared_conversion='scripts.standardize_england_results.convert_rows -> import_historical_csvs -> load_historical_data / validate_historical_data',
        code_sha256={str(p.relative_to(ROOT)):digest(p.read_bytes()) for p in (
            Path(__file__).resolve(), ROOT/'scripts/standardize_england_results.py',
            ROOT/'scripts/validate_championship_results.py', ROOT/'scripts/validate_england_results.py',
            ROOT/'scripts/artifact_io.py', ROOT/'src/toto_estimator/historical_import.py',
            ROOT/'src/toto_estimator/data.py', ROOT/'src/toto_estimator/validation.py',
            ROOT/'src/toto_estimator/outcomes.py',
        )},
        schema=list(OUTPUT_COLUMNS), league=LEAGUE, season_format='YYYY/YYYY',
        historical_names=provenance['historical_names'],
        identity='Existing importer: SHA-256 of compact UTF-8 JSON [league,season,ISO date,home team,away team], ensure_ascii=False, separators=(comma,colon); goals/path/order excluded',
        mapping={'Tier':'explicit 2','Division':'historical_name(season start); documented, not an output column',
                 'Date':'ISO date unchanged via day-first importer bridge','Season':'canonical YYYY/YYYY',
                 'HomeTeam/AwayTeam':'home_team/away_team exactly preserved',
                 'hGoal/aGoal':'home_goals/away_goals as nonnegative integers',
                 'Score/Result':'validated against goals, omitted from eight-column output',
                 'league':'EFL Championship for every season'},
        partitions={'completed':'1990/1991–2025/2026; 19872 records',
                    'ongoing':'2026/2027 only; 168 records'},
        validations=['source/extraction checksums match','full Championship structural audit passes',
                     'exact original-source partitions match saved extracts','exact requested counts',
                     'required eight-column schema/no blank fields','no importer rejection/fixture/duplicate/conflict',
                     'unique match IDs within/across partitions','unique season ordered home-away fixtures',
                     'multiset equality of dates/seasons/teams/goals against original source',
                     'existing public CSV loader and historical validator pass without match-fact changes',
                     'reversed-input conversions reproduce identical bytes'],
        playoff_checks=playoff_checks,
        outputs={name:dict(rows=summaries[name]['accepted'],sha256=digest(content),bytes=len(content),
                           import_summary=summaries[name]) for name,content in outputs.items()},
        attribution=provenance['attribution'], licence=provenance['licence'],
        legal_clearance='UNRESOLVED third-party rights. CC BY 4.0 covers only author original contributions/rights held. Local preparation only; no model integration, training, evaluation, publication or redistribution.',
        assurance_limits='External 20-match sample corroborated, but 15 references are named upstream 11v11; no exhaustive independently sourced verification or explicit source finished-status field. See docs/england-championship-validation.md.',
    )
    outputs[OUTPUT_NAMES[2]] = (json.dumps(manifest,indent=2,ensure_ascii=False)+'\n').encode('utf-8')
    return outputs


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true',help='rebuild and compare existing outputs byte-for-byte')
    args=parser.parse_args()
    if not args.check:
        check_overwrite([PRIVATE/name for name in OUTPUT_NAMES])
    outputs=build()
    if args.check:
        for name,content in outputs.items():
            if (PRIVATE/name).read_bytes()!=content:
                raise ValueError(f'saved output differs from reproducible conversion: {name}')
        print('PASS: both Championship CSVs and manifest reproduce byte-for-byte.')
    else:
        for name,content in outputs.items():
            with (PRIVATE/name).open('xb') as handle:
                handle.write(content)
        print('Created private standardized outputs: 19,872 historical; 168 ongoing matches.')
    for name in OUTPUT_NAMES[:2]:
        print(f'{name}: SHA-256 {digest(outputs[name])}')


if __name__=='__main__':
    main()
