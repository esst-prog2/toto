"""Offline audit of pinned Serie A originals; no standardized match export.

Run: PYTHONPATH=src .venv/bin/python -m scripts.validate_serie_a
Outputs are refused if present. --check verifies input hashes and saved diagnostics.
"""
import argparse
from collections import Counter, defaultdict
import csv
from datetime import date, datetime
import hashlib
import json
from pathlib import Path
import re

from scripts.artifact_io import check_overwrite, serialize_csv
from toto_estimator.historical_import import canonical_season
from toto_estimator.validation import exact_integer, team_name
from toto_estimator.outcomes import outcome_from_goals

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = ROOT / 'data/private/italy/serie_a'
AS_OF = date(2026, 11, 12)
CSV_FIELDS = ['Date', 'Season', 'home', 'visitor', 'FT', 'hgoal', 'vgoal',
              'tier', 'division', 'totgoal', 'goaldif', 'result']


def historical(path):
    """Retain source row references; never repair values or infer missing results."""
    records, issues = [], []
    with Path(path).open(encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle, strict=True)
        if reader.fieldnames != CSV_FIELDS:
            raise ValueError('Unexpected historical CSV schema')
        total = 0
        for row in reader:
            total += 1
            if None in row or any(v is None for v in row.values()):
                raise ValueError(f'Malformed CSV row {reader.line_num}')
            year = exact_integer(row['Season'])
            if not 1990 <= year <= 2024:
                continue
            season = canonical_season(f'{year}/{year+1}')
            record = dict(season=season, source_row=reader.line_num, date=row['Date'],
                          home=row['home'], away=row['visitor'], hg=row['hgoal'], ag=row['vgoal'])
            records.append(record)
            try:
                if any(not row[f].strip() for f in CSV_FIELDS):
                    raise ValueError('Missing source value')
                h, a = exact_integer(row['hgoal']), exact_integer(row['vgoal'])
                if row['tier'] != '1' or row['division'] != '1':
                    raise ValueError('Unexpected competition metadata')
                if row['FT'] != f'{h}-{a}' or exact_integer(row['totgoal']) != h+a or exact_integer(row['goaldif']) != h-a:
                    raise ValueError('Inconsistent score/total/difference')
                if row['result'] != {'1':'H','X':'D','2':'A'}[outcome_from_goals(h,a)]:
                    raise ValueError('Inconsistent result')
            except ValueError as exc:
                issues.append(dict(season=season, source_row=reader.line_num, code='source_consistency', detail=str(exc)))
    return records, issues, total


def football_txt(path, start=2025):
    """Parse compact Football.TXT with explicit dates and inherited season year.

    Month determines year, never source row order (postponed games can go back).
    Unknown non-comment/non-scorer lines fail closed to avoid losing fixtures.
    """
    records, issues = [], []
    current = None
    match = re.compile(r'^\s+(\d{1,2}:\d{2})\s+(.+?)\s{2,}(\d+)-(\d+)(?:\s+\((\d+)-(\d+)\))?\s{2,}(.+?)\s*$')
    annotation = False
    for number, line in enumerate(Path(path).read_text(encoding='utf-8-sig').splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped.startswith(('#', '=', '▪')):
            continue
        dm = re.fullmatch(r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun) ([A-Z][a-z]{2}) (\d{1,2})(?: (\d{4}))?', stripped)
        if dm:
            month = datetime.strptime(dm[2], '%b').month
            year = int(dm[4]) if dm[4] else start + (month < 7)
            current = date(year, month, int(dm[3])); annotation = False
            if current.strftime('%a') != dm[1]:
                issues.append(dict(season=f'{start}/{start+1}', source_row=number, code='weekday_mismatch', detail=stripped))
            continue
        m = match.fullmatch(line)
        if m:
            if current is None:
                raise ValueError(f'Match before date at line {number}')
            datetime.strptime(m[1], '%H:%M')
            record = dict(season=f'{start}/{start+1}', source_row=number, date=current.isoformat(), home=m[2], away=m[7], hg=m[3], ag=m[4])
            records.append(record)
            if m[5] is not None and (int(m[5]) > int(m[3]) or int(m[6]) > int(m[4])):
                issues.append(dict(season=record['season'], source_row=number, code='halftime_exceeds_fulltime', detail=stripped))
            annotation = False
            continue
        if stripped.startswith('(') or annotation:
            annotation = not stripped.endswith(')')
            continue
        raise ValueError(f'Unrecognized Football.TXT line {number}: {stripped}')
    return records, issues


def audit(records, source_issues=(), years=range(1990, 2026)):
    issues = list(source_issues)
    summaries, inventories = [], {}
    for year in years:
        season = canonical_season(f'{year}/{year+1}')
        rows = [r for r in records if r['season'] == season]
        n = 18 if year <= 2003 else 20
        def issue(code, detail, line=None):
            issues.append(dict(season=season, source_row=line, code=code, detail=detail))
        for r in rows:
            try:
                d = date.fromisoformat(r['date'])
                # July–June permits the COVID-extended 2019/20 season explicitly.
                end = date(year+1, 8, 31) if year == 2019 else date(year+1, 6, 30)
                if d.isoformat() != r['date'] or not date(year, 7, 1) <= d <= end or d > AS_OF:
                    raise ValueError('Date outside season/snapshot bounds')
                h, a = exact_integer(r['hg']), exact_integer(r['ag'])
                if min(h,a) < 0:
                    raise ValueError('Negative goals')
                home, away = team_name(r['home']), team_name(r['away'])
                if not home or not away or home == away or home != r['home'] or away != r['away']:
                    raise ValueError('Missing/identical/noncanonical whitespace in team names; source preserved')
            except (ValueError, TypeError) as exc:
                issue('invalid_required_value', str(exc), r['source_row'])
        teams = sorted({r[k] for r in rows for k in ('home','away')})
        pairs = defaultdict(list)
        for r in rows:
            pairs[(r['home'],r['away'])].append(r)
        repeated = 0
        for pair, entries in pairs.items():
            if len(entries) > 1:
                repeated += len(entries)-1
                conflict = len({(r['hg'],r['ag']) for r in entries}) > 1
                issue('conflicting_fixture' if conflict else 'duplicate_fixture', dict(pair=pair, source_rows=[r['source_row'] for r in entries]))
        missing = sorted({(h,a) for h in teams for a in teams if h != a} - set(pairs))
        if len(rows) != n*(n-1): issue('match_count', f'{len(rows)} / {n*(n-1)}')
        if len(teams) != n: issue('team_count', f'{len(teams)} / {n}')
        if missing: issue('missing_pairings', missing)
        balance = {t:dict(home=sum(r['home']==t for r in rows), away=sum(r['away']==t for r in rows)) for t in teams}
        if any(v != dict(home=n-1,away=n-1) for v in balance.values()):
            issue('home_away_balance', balance)
        own = [i for i in issues if i['season']==season]
        summaries.append(dict(season=season, matches=len(rows), expected=n*(n-1), teams=len(teams), expected_teams=n,
                              first_date=min((r['date'] for r in rows), default=''), last_date=max((r['date'] for r in rows), default=''),
                              missing_pairings=len(missing), repeated_pairings=repeated,
                              status='REVIEW' if own else 'PASS', issues='; '.join(f'{k}: {v}' for k,v in Counter(i['code'] for i in own).items()) or 'none'))
        inventories[season] = dict(teams=teams, balance=balance)
    unexpected = sorted({r['season'] for r in records} - {s['season'] for s in summaries})
    if unexpected: raise ValueError(f'Unexpected seasons: {unexpected}')
    return summaries, issues, inventories


def build(directory=PRIVATE):
    manifest = json.loads((directory/'acquisition.json').read_text())
    for entry in manifest:
        b = (directory/entry['file']).read_bytes()
        if hashlib.sha256(b).hexdigest() != entry['sha256'] or len(b) != entry['bytes']:
            raise ValueError(f'Source checksum mismatch: {entry["file"]}')
    old, oi, total = historical(directory/'jalapic/data-raw/italy.csv')
    new, ni = football_txt(directory/'openfootball/2025-26/1-seriea.txt')
    summaries, issues, names = audit(old+new, oi+ni)
    provenance = dict(retrieval_date=AS_OF.isoformat(), timezone='Europe/Budapest', sources=manifest,
                      historical_source_rows=total, selected_historical_rows=len(old), selected_2025_rows=len(new),
                      selection='Season start 1990–2024 from historical CSV; compact 2025/26 Football.TXT only; full text retained as supplemental original, never counted twice. No ongoing file downloaded.',
                      parsing='Source-specific in-memory audit only; original bytes, names and scores preserved. No standardized match export, aliases, corrections or deduplication.',
                      rights='James P. Curley / engsoccerdata: README noncommercial use and attribution, DESCRIPTION GPL >=2; conflict and upstream rights unresolved. OpenFootball: CC0 1.0 for rights held, no accuracy/title warranties or third-party clearance.',
                      limitations='Structural PASS does not establish played/finished status, score accuracy, team legal continuity, exclusion of every playoff substitution, or exhaustive exception coverage. Independent result verification remains outstanding.',
                      code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    outputs = {'season_validation.csv':serialize_csv(summaries,list(summaries[0])),
               'validation_issues.json':(json.dumps(issues,indent=2,ensure_ascii=False)+'\n').encode(),
               'team_inventory.json':(json.dumps(names,indent=2,ensure_ascii=False)+'\n').encode()}
    provenance['outputs'] = {k:dict(bytes=len(v),sha256=hashlib.sha256(v).hexdigest()) for k,v in outputs.items()}
    outputs['validation_provenance.json'] = (json.dumps(provenance,indent=2,ensure_ascii=False)+'\n').encode()
    return outputs, summaries


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args = parser.parse_args()
    outputs, summaries = build()
    if args.check:
        for name, content in outputs.items():
            if (PRIVATE/name).read_bytes() != content:
                raise ValueError(f'Diagnostic mismatch: {name}')
    else:
        check_overwrite([PRIVATE/name for name in outputs])
        for name, content in outputs.items():
            with (PRIVATE/name).open('xb') as handle: handle.write(content)
    print(json.dumps(dict(seasons=len(summaries),matches=sum(s['matches'] for s in summaries),statuses=Counter(s['status'] for s in summaries)),indent=2))


if __name__ == '__main__': main()
