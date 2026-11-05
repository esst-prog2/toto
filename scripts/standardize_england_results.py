"""Offline bridge to the existing historical importer; all match artifacts stay private.

PYTHONPATH=src .venv/bin/python -m scripts.standardize_england_results [--check]
Default creates new outputs exclusively; --check verifies existing outputs without writing.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
from datetime import date
import hashlib
import io
import json
from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd

from scripts.artifact_io import check_overwrite, serialize_csv
from scripts.validate_england_results import audit
from toto_estimator.data import load_historical_data
from toto_estimator.historical_import import (
    HistoricalSource, OUTPUT_COLUMNS, canonical_season, import_historical_csvs,
)
from toto_estimator.validation import exact_integer

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = ROOT / 'data/private/england'
LEAGUE = 'england.premier-league'
OUTPUT_NAMES = ('premier_league_standardized_1992_2025.csv',
                'premier_league_standardized_2026_2027_ongoing.csv',
                'standardization_manifest.json')
BRIDGE_COLUMNS = ('Date', 'Season', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR')


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def convert_rows(
    rows: list[dict[str, str]], private_directory: Path, *, league=LEAGUE,
    tier='1', division_names=None,
) -> tuple[bytes, dict]:
    """Translate only source columns/date syntax, then delegate validation and IDs.

    The caller chooses the season partition. Any rejection, duplicate, fixture,
    conflict, or normalization of match facts fails the conversion.
    Explicit tier/division_names/league arguments support historical names of
    another competition; defaults retain the Premier League mapping.
    """
    if not isinstance(league, str) or not league.strip() or league != league.strip():
        raise ValueError('league must be explicit, nonblank and canonical')
    bridge = []
    for row in rows:
        expected_division = (division_names.get(int(row['Season'][:4]))
                             if division_names is not None else 'Premier League')
        if row['Tier'] != tier or expected_division is None or row['Division'] != expected_division:
            raise ValueError('source tier/division does not agree with explicit competition mapping')
        day = date.fromisoformat(row['Date'])
        if day.isoformat() != row['Date']:
            raise ValueError('source date is not canonical ISO date')
        season = canonical_season(row['Season'])
        if season != row['Season']:
            raise ValueError('source season is not canonical YYYY/YYYY')
        h, a = exact_integer(row['hGoal']), exact_integer(row['aGoal'])
        if row['Score'] != f'{h}-{a}':
            raise ValueError('source Score does not agree with goal columns')
        bridge.append(dict(zip(BRIDGE_COLUMNS, (
            f'{day.day:02d}/{day.month:02d}/{day.year:04d}', season,
            row['HomeTeam'], row['AwayTeam'], row['hGoal'], row['aGoal'], row['Result'],
        ))))
    # The original importer is file-based. Its temporary supported-schema input
    # is kept inside private storage, and removed on success or failure.
    with TemporaryDirectory(prefix='.standardize-', dir=private_directory) as temp:
        path = Path(temp) / 'import_bridge.csv'
        path.write_bytes(serialize_csv(bridge, BRIDGE_COLUMNS))
        imported = import_historical_csvs([HistoricalSource(path, league)])
    if imported.issues or imported.summary != dict(
        total=len(rows), accepted=len(rows), rejected=0, duplicates=0, fixtures=0, conflicts=0,
    ):
        raise ValueError(f'importer rejected/changed rows: {imported.summary}; {imported.issues}')
    records = imported.records
    if any(any(r[c] is None or str(r[c]).strip() == '' for c in OUTPUT_COLUMNS) for r in records):
        raise ValueError('missing standard field')
    if len({r['match_id'] for r in records}) != len(records):
        raise ValueError('duplicate match IDs')
    # These regular-season leagues have each ordered club pairing once, even if dates differ.
    if len({(r['league'], r['season'], r['home_team'], r['away_team']) for r in records}) != len(records):
        raise ValueError('duplicate season home-away fixture')
    expected = Counter((r['Date'], r['Season'], r['HomeTeam'], r['AwayTeam'],
                        exact_integer(r['hGoal']), exact_integer(r['aGoal'])) for r in rows)
    actual = Counter((r['date'], r['season'], r['home_team'], r['away_team'],
                      r['home_goals'], r['away_goals']) for r in records)
    if actual != expected:
        raise ValueError('dates, seasons, teams or goals changed during conversion')
    content = serialize_csv(records, OUTPUT_COLUMNS)
    # Exercise the public CSV loader and validator, without prediction/evaluation.
    validated = load_historical_data(io.StringIO(content.decode('utf-8')))
    validated['date'] = validated['date'].dt.strftime('%Y-%m-%d')
    validated_records = validated[list(OUTPUT_COLUMNS)].to_dict(orient='records')
    if Counter(tuple(r[c] for c in OUTPUT_COLUMNS) for r in validated_records) != Counter(tuple(r[c] for c in OUTPUT_COLUMNS) for r in records):
        raise ValueError('public historical validator changed standard match facts')
    # Verify serialization parses into the exact eight requested columns.
    parsed = pd.read_csv(io.BytesIO(content), keep_default_na=False)
    if tuple(parsed.columns) != OUTPUT_COLUMNS or len(parsed) != len(rows) or parsed.isna().any().any():
        raise ValueError('serialized standard schema/row count mismatch')
    return content, imported.summary


def build(directory: Path = PRIVATE) -> dict[str, bytes]:
    provenance = json.loads((directory / 'provenance.json').read_text())
    for name, info in provenance['files'].items():
        if digest((directory / name).read_bytes()) != info['sha256']:
            raise ValueError(f'previously validated input has changed: {name}')
    source = directory / 'EnglandLeagueResults.csv'
    _, source_count, selected, issues, season_summary = audit(source)
    if issues:
        raise ValueError(f'source audit failed: {issues}')
    historical = [r for _, r in selected if 1992 <= int(r['Season'][:4]) <= 2025]
    ongoing = [r for _, r in selected if r['Season'] == '2026/2027']
    if len(historical) != 13166 or len(ongoing) != 90 or len(selected) != 13256:
        raise ValueError('pinned snapshot row counts changed')
    for rows, name in ((historical, 'premier_league_1992_2025.csv'),
                       (ongoing, 'premier_league_2026_2027_ongoing.csv')):
        with (directory / name).open(encoding='utf-8', newline='') as handle:
            if rows != list(csv.DictReader(handle)):
                raise ValueError(f'source/export partition mismatch: {name}')
    if [s['status'] for s in season_summary] != ['PASS'] * 34 + ['ONGOING']:
        raise ValueError('unexpected season coverage')
    outputs, summaries = {}, {}
    for rows, name in zip((historical, ongoing), OUTPUT_NAMES[:2]):
        content, summary = convert_rows(rows, directory)
        # Order-independent importer IDs and deterministic bytes, independently rebuilt.
        repeat, _ = convert_rows(list(reversed(rows)), directory)
        if content != repeat:
            raise ValueError('conversion is not reproducible under input reordering')
        outputs[name] = content
        summaries[name] = summary
    manifest = dict(
        conversion_date='2026-11-05', source_url=provenance['source_url'],
        source_commit_sha=provenance['source_commit_sha'], source_rows=source_count,
        source_sha256=digest(source.read_bytes()),
        converter='scripts/standardize_england_results.py',
        code_sha256={str(p.relative_to(ROOT)): digest(p.read_bytes()) for p in (
            Path(__file__).resolve(), ROOT/'scripts/validate_england_results.py',
            ROOT/'scripts/artifact_io.py', ROOT/'src/toto_estimator/historical_import.py',
            ROOT/'src/toto_estimator/data.py', ROOT/'src/toto_estimator/validation.py',
            ROOT/'src/toto_estimator/outcomes.py',
        )},
        schema=list(OUTPUT_COLUMNS), league=LEAGUE, season_format='YYYY/YYYY',
        identity='SHA-256 of compact UTF-8 JSON [league,season,ISO date,home team,away team], ensure_ascii=False; goals excluded; existing importer algorithm',
        mapping={'Date': 'date (ISO preserved via DD/MM/YYYY bridge)', 'Season': 'season',
                 'HomeTeam': 'home_team', 'AwayTeam': 'away_team', 'hGoal': 'home_goals',
                 'aGoal': 'away_goals', 'Result': 'bridge FTR, checked against goals; omitted from eight-column output',
                 'Score': 'checked against hGoal/aGoal; omitted', 'Tier/Division': 'explicitly require 1 / Premier League'},
        partitions={'completed': '1992/1993 through 2025/2026', 'ongoing': '2026/2027 only'},
        validations=['all prior provenance checksums match', 'original source audit passes',
                     'exact source/export partitions', '13166 historical / 90 ongoing rows',
                     'no missing required fields', 'unique IDs and season home-away fixtures',
                     'exact multiset equality of source dates/seasons/teams/goals',
                     'public load_historical_data and validate_historical_data pass without factual changes',
                     'reversed-input conversion yields identical bytes'],
        outputs={name: dict(rows=summaries[name]['accepted'], bytes=len(content), sha256=digest(content),
                            import_summary=summaries[name]) for name, content in outputs.items()},
        licence=provenance['licence'], attribution=provenance['attribution'],
        legal_clearance='UNRESOLVED: original-contribution CC BY 4.0 does not clear third-party rights; local preparation only, no publication, redistribution, training or evaluation.',
        assurance_limits='Earlier 20-match independent verification is a bounded sample; source has no explicit finished-status field. See docs/england-premier-league-validation.md.',
    )
    outputs[OUTPUT_NAMES[2]] = (json.dumps(manifest, indent=2, ensure_ascii=False) + '\n').encode('utf-8')
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='rebuild in memory and compare existing outputs; never overwrite')
    args = parser.parse_args()
    if not args.check:
        check_overwrite([PRIVATE/name for name in OUTPUT_NAMES])
    outputs = build()
    if args.check:
        for name, content in outputs.items():
            if (PRIVATE/name).read_bytes() != content:
                raise ValueError(f'existing output differs from reproducible conversion: {name}')
        print('PASS: saved standardized CSVs and manifest reproduce byte-for-byte.')
    else:
        for name, content in outputs.items():
            with (PRIVATE/name).open('xb') as handle:
                handle.write(content)
        print('Created private standardized outputs: 13,166 historical matches; 90 ongoing matches.')
    for name in OUTPUT_NAMES[:2]:
        print(f'{name}: SHA-256 {digest(outputs[name])}')


if __name__ == '__main__':
    main()
