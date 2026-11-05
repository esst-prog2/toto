"""Bounded saved-snapshot validation. No network access or archive acquisition."""
import argparse
import hashlib
import io
import json
from pathlib import Path

from scripts.artifact_io import check_overwrite, serialize_csv
from toto_estimator.data import load_historical_data
from toto_estimator.dfb_html import COLUMNS, parse_dfb_matchday

PRIVATE = Path(__file__).resolve().parents[1] / 'data/private/germany/cross_era'
SAMPLES = (('1991-1992', 1, 10), ('2005-2006', 1, 9),
           ('2015-2016', 1, 9), ('2025-2026', 1, 9), ('2005-2006', 14, 9))


def validate_samples(directory=PRIVATE):
    """Validate fixed inputs in memory; missing/changed snapshots fail explicitly."""
    directory = Path(directory)
    entries = json.loads((directory / 'retrieval.json').read_text())
    entries.append(json.loads((directory / 'rescheduled_retrieval.json').read_text()))
    provenance = {e['requested_url']: e for e in entries}
    findings, outputs = [], {}
    for season, day, count in SAMPLES:
        name = f'{season}_md{day}'
        source = directory / f'{name}.html'
        content = source.read_bytes()
        url = f'https://datencenter.dfb.de/de/competitions/bundesliga/seasons/{season}/matchday/{day}'
        digest = hashlib.sha256(content).hexdigest()
        if provenance[url].get('status') != 200 or provenance[url].get('sha256') != digest:
            raise ValueError(f'Unverified snapshot: {source.name}')
        result = parse_dfb_matchday(content.decode('utf-8'), expected_season=season,
                                   expected_matchday=day, expected_matches=count)
        if result.issues:
            raise ValueError(result.issues)
        csv = serialize_csv(result.records, COLUMNS)
        if csv != serialize_csv(parse_dfb_matchday(content.decode('utf-8')).records, COLUMNS):
            raise ValueError('Non-reproducible parse')
        validated = load_historical_data(io.StringIO(csv.decode('utf-8')))
        teams = {r[k] for r in result.records for k in ('home_team', 'away_team')}
        fixtures = {(r['home_team'], r['away_team']) for r in result.records}
        if len(validated) != count or len(teams) != count * 2 or len(fixtures) != count:
            raise ValueError(f'Unexpected match/team/fixture coverage: {name}')
        if day == 14:
            target = [r for r in result.records if r['home_team'] == 'MSV Duisburg']
            if len(target) != 1 or target[0] != dict(zip(COLUMNS, (
                    '2005/2006', 14, '2005-12-06', 'MSV Duisburg', '1. FC Köln', 1, 1))):
                raise ValueError('Rescheduled fixture differs from inspected DFB HTML')
        findings.append(dict(file=source.name, url=result.source_url, season=result.season,
                             matchday=day, matches=count, teams=len(teams), issues=result.issues,
                             first_date=min(r['date'] for r in result.records),
                             last_date=max(r['date'] for r in result.records),
                             source_sha256=digest, csv_sha256=hashlib.sha256(csv).hexdigest(),
                             historical_validator='PASS', byte_reproducible=True,
                             finished_status='Numeric result candidates; explicit status not certified'))
        outputs[f'{name}_parsed.csv'] = csv
    return findings, outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Compare existing outputs without writing")
    args = parser.parse_args()
    findings, outputs = validate_samples()
    outputs['validation.json'] = (json.dumps(findings, indent=2, ensure_ascii=False) + '\n').encode()
    if args.check:
        for name, content in outputs.items():
            if (PRIVATE / name).read_bytes() != content:
                raise ValueError(f"Output differs: {name}")
        print("PASS: all saved outputs reproduce byte-for-byte")
        return
    check_overwrite([PRIVATE / name for name in outputs])
    for name, content in outputs.items():
        with (PRIVATE / name).open('xb') as handle:
            handle.write(content)
    print(f'PASS: {len(findings)} snapshots, {sum(r["matches"] for r in findings)} match candidates')


if __name__ == '__main__':
    main()
