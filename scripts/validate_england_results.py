"""Audit a local Sean Elvidge CSV; preserve rows and refuse output overwrites.

Run: PYTHONPATH=src .venv/bin/python scripts/validate_england_results.py
No downloads, prediction calls, name reconciliation, or corrections are performed.
"""
from collections import Counter, defaultdict
import csv
from datetime import date
import hashlib
import json
from pathlib import Path
import re

from toto_estimator.historical_import import canonical_season
from toto_estimator.outcomes import outcome_from_goals
from toto_estimator.validation import exact_integer, team_name

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / 'data/private/england'
SHA = '84d4d8877def6338a8cf55479f40bbc1216f84bc'
AS_OF = date(2026, 11, 5)
SOURCE = 'https://github.com/seanelvidge/England-football-results'


def audit(source, *, tier=1, first_year=1992, team_counts=None):
    """Audit a tier with explicit season scope and expected league sizes.

    Defaults preserve the original Premier League audit. team_counts maps each
    season start year to its independently specified expected participant count.
    """
    issues, selected = [], []
    def issue(row, season, code, detail):
        issues.append(dict(source_row=row, season=season, code=code, detail=detail))
    with source.open(encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle, strict=True)
        fields = reader.fieldnames
        required = {'Date', 'Season', 'HomeTeam', 'AwayTeam', 'Score', 'hGoal', 'aGoal', 'Division', 'Tier', 'Result'}
        if fields is None or len(fields) != len(set(fields)) or not required <= set(fields):
            raise ValueError('missing or duplicate source headers')
        total = 0
        for row in reader:
            total += 1
            number = reader.line_num
            if None in row or any(v is None for v in row.values()):
                raise ValueError(f'malformed CSV row at line {number}')
            try:
                source_tier = exact_integer(row['Tier'])
                season = canonical_season(row['Season'])
                if not re.fullmatch(r'\d{4}/\d{4}', season):
                    raise ValueError('cross-year season required')
                start = int(season[:4])
            except ValueError as exc:
                issue(number, row['Season'], 'unclassifiable_source_row', str(exc))
                continue
            if source_tier != tier or start < first_year:
                continue
            selected.append((number, row))
            if start > 2026:
                issue(number, season, 'future_season', 'beyond the requested current season')
            if row['Season'] != season or row['Tier'] != str(tier):
                issue(number, season, 'noncanonical_metadata', 'raw season/tier spelling differs from documented format; preserved')
            try:
                day = date.fromisoformat(row['Date'])
                if day.isoformat() != row['Date'] or day.year not in (start, start + 1):
                    raise ValueError('date format/year inconsistent with season')
                if day > AS_OF:
                    raise ValueError('result dated after retrieval date')
            except ValueError as exc:
                issue(number, season, 'invalid_date', str(exc))
            home, away = team_name(row['HomeTeam']), team_name(row['AwayTeam'])
            if not home or not away or home == away:
                issue(number, season, 'invalid_teams', 'missing or identical teams')
            if home != row['HomeTeam'] or away != row['AwayTeam']:
                issue(number, season, 'team_whitespace', 'surrounding whitespace; preserved')
            try:
                h, a = exact_integer(row['hGoal']), exact_integer(row['aGoal'])
                if min(h, a) < 0:
                    raise ValueError('negative goals')
                score = re.fullmatch(r'([0-9]+)-([0-9]+)', row['Score'])
                if score is None or tuple(map(int, score.groups())) != (h, a):
                    issue(number, season, 'score_mismatch', 'Score does not match hGoal/aGoal')
                expected = {'1': 'H', 'X': 'D', '2': 'A'}[outcome_from_goals(h, a)]
                if row['Result'] != expected:
                    issue(number, season, 'result_mismatch', 'Result does not match goals')
            except ValueError as exc:
                issue(number, season, 'invalid_goals', str(exc))
    identities, pairs, seasons = defaultdict(list), defaultdict(list), defaultdict(list)
    for number, row in selected:
        season = canonical_season(row['Season'])
        seasons[season].append(row)
        identities[(season, row['Date'], row['HomeTeam'], row['AwayTeam'])].append((number, row))
        pairs[(season, row['HomeTeam'], row['AwayTeam'])].append((number, row))
    for key, entries in identities.items():
        if len(entries) > 1:
            scores = {(r['hGoal'], r['aGoal'], r['Score'], r['Result']) for _, r in entries}
            issue(entries[0][0], key[0], 'conflicting_duplicate' if len(scores) > 1 else 'duplicate_match', f'identity {key}; source rows {[n for n, _ in entries]}')
    for key, entries in pairs.items():
        if len(entries) > 1:
            issue(entries[0][0], key[0], 'repeated_ordered_pair', f'{key[1:]} appears {len(entries)} times; rows {[n for n, _ in entries]}')
    summary = []
    for start in range(first_year, 2027):
        season = f'{start}/{start+1}'
        rows = seasons[season]
        teams = {r[c] for r in rows for c in ('HomeTeam', 'AwayTeam') if r[c].strip()}
        n = team_counts[start] if team_counts is not None else (22 if start <= 1994 else 20)
        expected = n * (n - 1)
        ongoing = start == 2026
        if len(teams) != n:
            issue(None, season, 'team_count', f'{len(teams)} teams; expected {n}')
        if (not ongoing and len(rows) != expected) or len(rows) > expected:
            issue(None, season, 'match_count', f'{len(rows)} matches; expected {expected}')
        actual_pairs = {(r['HomeTeam'], r['AwayTeam']) for r in rows}
        missing = {(h, a) for h in teams for a in teams if h != a} - actual_pairs
        if not ongoing and missing:
            issue(None, season, 'missing_pairings', f'{len(missing)} missing home-away pairings: {sorted(missing)}')
        dates = sorted(r['Date'] for r in rows if re.fullmatch(r'\d{4}-\d{2}-\d{2}', r['Date']))
        season_issues = [i for i in issues if i['season'] == season]
        summary.append(dict(season=season, matches=len(rows), teams=len(teams), expected_matches=expected,
                            first_date=dates[0] if dates else '', last_date=dates[-1] if dates else '',
                            status=('ONGOING' if ongoing else 'PASS') if not season_issues else 'REVIEW',
                            issues='; '.join(f'{k}: {v}' for k,v in Counter(i['code'] for i in season_issues).items()) or ('in progress; not tested for full-season completeness' if ongoing else 'none')))
    return fields, total, selected, issues, summary


def main():
    source = DIRECTORY / 'EnglandLeagueResults.csv'
    targets = [DIRECTORY / n for n in ('premier_league_1992_2025.csv', 'premier_league_2026_2027_ongoing.csv', 'validation_issues.json', 'season_validation.csv', 'provenance.json')]
    report = ROOT / 'docs/england-premier-league-validation.md'
    for target in [*targets, report]:
        if target.exists():
            raise FileExistsError(f'refusing to overwrite {target}')
    fields, total, selected, issues, summary = audit(source)
    for target, ongoing in zip(targets[:2], (False, True)):
        with target.open('x', encoding='utf-8', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(row for _, row in selected if (int(row['Season'][:4]) == 2026 if ongoing else 1992 <= int(row['Season'][:4]) <= 2025))
    targets[2].write_text(json.dumps(issues, indent=2) + '\n')
    with targets[3].open('x', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary[0]))
        writer.writeheader()
        writer.writerows(summary)
    provenance = dict(source_url=SOURCE, source_commit_sha=SHA, source_commit_api=f'https://api.github.com/repos/seanelvidge/England-football-results/commits/{SHA}',
                      download_url=f'https://raw.githubusercontent.com/seanelvidge/England-football-results/{SHA}/EnglandLeagueResults.csv',
                      retrieval_date=AS_OF.isoformat(), retrieval_timezone='Europe/Budapest', source_rows=total,
                      filters='Tier = 1; season start >= 1992; 2026/2027 separate; raw columns and rows preserved without correction/deduplication',
                      licence='CC BY 4.0 for Sean Elvidge original contributions and rights he holds only; third-party rights remain reserved. See saved LICENCE.md and SOURCE_README.md.',
                      attribution='English Football League Data, compiled and maintained by Sean Elvidge, drawing on RSSSF, Curley & Malmedal (2014), and references therein.',
                      files={p.name: dict(sha256=hashlib.sha256(p.read_bytes()).hexdigest(), bytes=p.stat().st_size) for p in [source, DIRECTORY/'LICENCE.md', DIRECTORY/'SOURCE_README.md', *targets[:4]]})
    targets[4].write_text(json.dumps(provenance, indent=2) + '\n')
    lines = ['# Premier League source validation', '', f'Retrieved {AS_OF} (Europe/Budapest). Source: [Sean Elvidge / England-football-results]({SOURCE}), commit `{SHA}`.', '',
             f'Original CSV: {total:,} rows; SHA-256 `{provenance["files"][source.name]["sha256"]}`.', '',
             'Scope: Tier 1 from 1992/1993. Raw columns, values and order are preserved; no corrections or deduplication. Completed seasons end at 2025/2026; 2026/2027 is saved separately as ongoing.', '',
             'Expected double round-robin totals: 22 × 21 = 462 for 1992/1993–1994/1995; 20 × 19 = 380 thereafter. [Premier League history](https://www.premierleague.com/en/history). Missing entire seasons are checked explicitly. Ordered home-away pairings are checked as well as totals.', '',
             '| Season | Matches / expected | Teams | First date | Last date | Status | Issues |', '|---|---:|---:|---|---|---|---|']
    lines += [f'| {s["season"]} | {s["matches"]} / {s["expected_matches"]} | {s["teams"]} | {s["first_date"]} | {s["last_date"]} | {s["status"]} | {s["issues"]} |' for s in summary]
    lines += ['', f'Summary: {sum(s["matches"] for s in summary[:-1]):,} completed-season matches; {summary[-1]["matches"]} ongoing-season matches. Season statuses and issues are listed above.', '', f'Row/source issues: {len(issues)}. Detailed diagnostics including original CSV row numbers: `data/private/england/validation_issues.json`.', '',
              'Checks: CSV structure; season/tier metadata; missing/invalid dates, teams and goals; nonnegative exact integer goals; Score/goals/Result agreement; future dates; duplicate identities and repeated home-away pairings; team counts and season completeness. Reuses canonical_season, exact_integer, team_name and outcome_from_goals. The existing Football-Data importer is not used directly because this source uses ISO dates and hGoal/aGoal.', '',
              'Artifacts (all Git-ignored under `data/private/england/`): original `EnglandLeagueResults.csv`; `premier_league_1992_2025.csv`; `premier_league_2026_2027_ongoing.csv`; `season_validation.csv`; `validation_issues.json`; `provenance.json`; source `LICENCE.md` and `SOURCE_README.md`. Provenance records pinned download URL, retrieval date, source SHA, byte sizes and SHA-256 checksums.', '',
              'Licence: CC BY 4.0 covers only Sean Elvidge’s original contributions and rights he holds. Preserve creator credit, source and licence links, source notices and change indications when sharing. Third-party rights remain reserved; the saved licence names upstream sources including RSSSF, ENFA, football-data.co.uk and others. This audit does not establish blanket rights for downstream redistribution or application use.', '',
              'Suitability: seasons marked PASS meet the structural, consistency and round-robin checks in this audit. This does not independently verify every real-world result or team identity. Review any REVIEW seasons before future use; retain the ongoing season separately and revalidate updates. No prediction, application or evaluation integration has been performed.', '',
              'Reproduce against the saved original with `PYTHONPATH=src .venv/bin/python scripts/validate_england_results.py` in a fresh checkout/output location: existing outputs are deliberately refused. The audit date and source commit are fixed for this acquisition snapshot.']
    report.write_text('\n'.join(lines) + '\n')
    print(json.dumps(dict(source_rows=total, extracted_rows=len(selected), issues=len(issues), statuses=Counter(s['status'] for s in summary)), indent=2))


if __name__ == '__main__':
    main()
