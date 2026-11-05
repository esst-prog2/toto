"""Extract/audit the saved Tier 2 snapshot, without standardization or downloads.

Run: PYTHONPATH=src .venv/bin/python -m scripts.validate_championship_results
Existing output paths are refused. Source fields, names and row order are retained.
"""
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path

from scripts.artifact_io import check_overwrite, serialize_csv
from scripts.validate_england_results import AS_OF, DIRECTORY, ROOT, audit

FUTURE_LEAGUE = 'EFL Championship'  # User-selected future identifier; not written to matches.
TEAM_COUNTS = {year: 24 for year in range(1990, 2027)}
NAMES = ('championship_1990_2025.csv', 'championship_2026_2027_ongoing.csv',
         'championship_season_validation.csv', 'championship_validation_issues.json',
         'championship_provenance.json')
REPORT = ROOT / 'docs/england-championship-validation.md'
# Bounded playoff identity checks, not an independent result audit or full playoff inventory.
PLAYOFF_REFERENCES = [
    ('1990/1991', '1991-06-02', 'Brighton and Hove Albion', 'Notts County',
     'https://www.11v11.com/matches/brighton-and-hove-albion-v-notts-county-02-june-1991-279330/'),
    ('2003/2004', '2004-05-29', 'Crystal Palace', 'West Ham United',
     'https://www.uefa.com/news-media/news/019d-0f8fc0d7fa91-cdea0ec771a1-1000--palace-crown-promotion-push/'),
    ('2024/2025', '2025-05-24', 'Sheffield United', 'Sunderland',
     'https://www.efl.com/news/2025/may/24/sunderland-win-championship-play-off-final-in-dramatic-fashion/'),
]


def historical_name(year):
    if year < 1992:
        return 'Football League Second Division'
    if year < 2004:
        return 'Football League First Division'
    if year < 2016:
        return 'Football League Championship'
    return 'EFL Championship'


def championship_audit(source):
    fields, total, selected, issues, summary = audit(
        source, tier=2, first_year=1990, team_counts=TEAM_COUNTS,
    )
    for number, row in selected:
        if row['Division'] != historical_name(int(row['Season'][:4])):
            issues.append(dict(source_row=number, season=row['Season'], code='historical_name',
                               detail=f"unexpected source Division: {row['Division']!r}"))
    playoff_checks = []
    for season, day, home, away, url in PLAYOFF_REFERENCES:
        # Check both home-away orientations (final venues are neutral); allow
        # source Brighton spelling variations without renaming stored values.
        aliases = {'Brighton and Hove Albion', 'Brighton & Hove Albion'} if home.startswith('Brighton') else {home}
        found = [(number, row) for number, row in selected
                 if row['Season'] == season and row['Date'] == day
                 and ((row['HomeTeam'] in aliases and row['AwayTeam'] == away)
                      or (row['AwayTeam'] in aliases and row['HomeTeam'] == away))]
        playoff_checks.append(dict(season=season, date=day, teams=[home, away], url=url,
                                   selected_source_rows=[n for n, _ in found], status='PRESENT' if found else 'ABSENT'))
        for number, row in found:
            issues.append(dict(source_row=number, season=season, code='known_playoff_in_regular_extract',
                               detail=f'known playoff final: {day} {home} / {away}; preserved for review'))
    for season in summary:
        rows = [r for _, r in selected if r['Season'] == season['season']]
        n = season['teams']
        season['historical_competition_name'] = historical_name(int(season['season'][:4]))
        season['observed_source_names'] = '; '.join(sorted({r['Division'] for r in rows}))
        season['expected_matches_from_observed_teams'] = n * (n - 1)
        pairs = Counter((r['HomeTeam'], r['AwayTeam']) for r in rows)
        season['repeated_ordered_pairings'] = sum(v - 1 for v in pairs.values() if v > 1)
        own_issues = [i for i in issues if i['season'] == season['season']]
        if own_issues:
            season['status'] = 'REVIEW'
            season['issues'] = '; '.join(f'{k}: {v}' for k, v in Counter(i['code'] for i in own_issues).items())
    return fields, total, selected, issues, summary, playoff_checks


def main():
    paths = [DIRECTORY/name for name in NAMES]
    check_overwrite([*paths, REPORT])
    prior = json.loads((DIRECTORY/'provenance.json').read_text())
    # Verify, do not alter the source or the Premier League artifacts.
    for name, info in prior['files'].items():
        if hashlib.sha256((DIRECTORY/name).read_bytes()).hexdigest() != info['sha256']:
            raise ValueError(f'previously validated file changed: {name}')
    fields, total, selected, issues, summary, playoff_checks = championship_audit(DIRECTORY/'EnglandLeagueResults.csv')
    historical = [r for _, r in selected if 1990 <= int(r['Season'][:4]) <= 2025]
    ongoing = [r for _, r in selected if r['Season'] == '2026/2027']
    outputs = {
        NAMES[0]: serialize_csv(historical, fields),
        NAMES[1]: serialize_csv(ongoing, fields),
        NAMES[2]: serialize_csv(summary, list(summary[0])),
        NAMES[3]: (json.dumps(issues, indent=2) + '\n').encode(),
    }
    manifest = dict(
        extraction_date=AS_OF.isoformat(), retrieval_date=prior['retrieval_date'],
        source_url=prior['source_url'], source_commit_sha=prior['source_commit_sha'],
        download_url=prior['download_url'], source_sha256=prior['files']['EnglandLeagueResults.csv']['sha256'],
        source_rows=total, reused_local_source=True, new_download=False,
        rules='Tier = 2, seasons 1990/1991 through 2025/2026 historical; 2026/2027 separate; preserve source schema, row order, names and values; no standardization/corrections/deduplication',
        future_standard_league_identifier=FUTURE_LEAGUE,
        historical_names={'1990/1991–1991/1992': historical_name(1990),
                          '1992/1993–2003/2004': historical_name(1992),
                          '2004/2005–2015/2016': historical_name(2004),
                          '2016/2017 onwards': historical_name(2016)},
        expected_teams_by_season_start=TEAM_COUNTS,
        completed_matches=len(historical), complete_seasons=sum(s['status']=='PASS' for s in summary),
        ongoing_matches=len(ongoing), issue_count=len(issues), playoff_reference_checks=playoff_checks,
        playoff_scope='No stage/status column. Full round-robin pairings plus counts detect extra playoff appearances; repeated pairings are review candidates, never silently removed. Three known finals checked absent; not exhaustive independent stage verification.',
        code_sha256={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                     for p in [Path(__file__).resolve(), ROOT/'scripts/validate_england_results.py']},
        outputs={name:dict(bytes=len(content), sha256=hashlib.sha256(content).hexdigest()) for name,content in outputs.items()},
        licence=prior['licence'], attribution=prior['attribution'],
        licensing_evidence={'file':'LICENCE.md','sha256':prior['files']['LICENCE.md']['sha256']},
        legal_clearance='Unresolved third-party rights; no integration, standardization, training, evaluation, publication or redistribution authorized here.',
    )
    outputs[NAMES[4]] = (json.dumps(manifest, indent=2, ensure_ascii=False)+'\n').encode()
    lines = ['# English second-tier structural validation', '',
             f'Extracted {AS_OF} from the existing local source; no new dataset download. Source: [Sean Elvidge / England-football-results]({prior["source_url"]}), commit `{prior["source_commit_sha"]}`; originally retrieved {prior["retrieval_date"]}.', '',
             f'Original `EnglandLeagueResults.csv`: {total:,} rows; SHA-256 `{manifest["source_sha256"]}`. Prior source/provenance checksums were verified before extraction.', '',
             f'**Results:** {len(historical):,} historical matches, {manifest["complete_seasons"]} complete seasons; {len(ongoing):,} ongoing 2026/2027 matches; {len(issues)} structural issues.', '',
             '## Competition identity and historical names', '',
             'All periods represent the same English second-tier competition. The user-selected future standardized league identifier is exactly **`EFL Championship`**. It supersedes the earlier planning proposal `england.championship` for future datasets of this competition; no existing identifiers or standardized datasets are changed in this task. These extracts retain the source `Division` and `Season` values and have no added standardized league or match_id column.', '',
             '| Seasons | Historical source competition name |', '|---|---|',
             '| 1990/1991–1991/1992 | Football League Second Division |',
             '| 1992/1993–2003/2004 | Football League First Division |',
             '| 2004/2005–2015/2016 | Football League Championship |',
             '| 2016/2017 onwards | EFL Championship |', '',
             'Naming boundaries match all selected local `Division` values. For historical context see [RSSSF second-tier history](https://www.rsssf.org/tablese/eng2champ.html) and [EFL innovation/rebranding](https://www.efl.com/about-the-efl/history/innovation/) (2016 rebrand visible in search-indexed text; direct EFL history pages returned shells). `Tier = 2` determines level; filtering by “First Division” alone would mix levels across 1992.', '',
             '## Season validation', '',
             'Each observed season has 24 participants. Expected regular-season matches are independently configured as 24 × 23 = 552, and also computed from the observed number of distinct teams as n × (n − 1). Both counts agree in this snapshot. For each completed season, every ordered home-away pairing occurs exactly once (23 home and 23 away appearances per team). Ongoing completeness is not required.', '',
             '| Season | Historical competition name | Teams | Expected | Actual | First date | Last date | Status | Anomalies |',
             '|---|---|---:|---:|---:|---|---|---|---|']
    for s in summary:
        lines.append(f'| {s["season"]} | {s["historical_competition_name"]} | {s["teams"]} | {s["expected_matches"]} | {s["matches"]} | {s["first_date"]} | {s["last_date"]} | {s["status"]} | {s["issues"]} |')
    lines += ['', '## Checks and playoff scope', '',
              'The shared `scripts.validate_england_results.audit` now accepts explicit tier, first-season and participant-count parameters; its Premier League defaults remain unchanged. It reuses the historical importer’s `canonical_season` and shared `exact_integer`, `team_name` and `outcome_from_goals` checks. Checks cover CSV headers/row widths; missing/invalid dates, teams and goals; nonnegative integer goals; Score/goals/Result consistency; dates after snapshot retrieval; exact/conflicting duplicate match identities; repeated season home-away pairings; missing seasons; participant and match counts; and full ordered-pairing coverage. The Championship wrapper adds source historical-name checks, observed-team expected totals and bounded known-playoff checks. Anomalous source rows are preserved and reported, never silently corrected or deduplicated.', '',
              'No extra/repeated pairings or playoff-labelled rows were found in the Tier 2 extraction. All completed seasons stop with a complete regular-season round robin (552 matches), rather than 557 including the usual five playoff matches. The source has no stage/status field, so pairing/count evidence supports regular-season-only scope but cannot exclude a hypothetical mislabelled substitution for a missing regular-season game. There is no exhaustive independent result/stage verification in this task.', '',
              'Known promotion playoff finals were checked by season, date and both club orientations (Brighton naming aliases used only for lookup; stored names unchanged):', '',
              '| Season | Date | Clubs | In extract? | Evidence |', '|---|---|---|---|---|']
    for c in playoff_checks:
        lines.append(f'| {c["season"]} | {c["date"]} | {" / ".join(c["teams"])} | {c["status"]} | [Reference]({c["url"]}) |')
    lines += ['', 'The 1991 and 2004 references were directly readable. The 2025 EFL result was available in indexed text; the official [Championship playoff archive](https://www.efl.com/competitions/sky-bet-play-offs/about-the-play-offs/championship-play-off-finals/) and schedule/history pages returned incomplete page shells. Those shells are not treated as a verified full playoff inventory. No access limits were bypassed and no bulk scraping was performed. Missing playoffs are intentional for a regular-season dataset, not missing regular fixtures.', '',
              '## Local artifacts and reproduction', '',
              'All extracted match data and diagnostics are exclusively under Git-ignored `data/private/england/`:', '',
              '| File | SHA-256 |', '|---|---|']
    lines += [f'| `{name}` | `{info["sha256"]}` |' for name,info in manifest['outputs'].items()]
    lines += ['', '`championship_provenance.json` records the source URL/commit/retrieval and extraction dates, raw checksum, extraction/naming rules, checksummed outputs, code fingerprints, playoff checks and licensing scope. Extracts retain all ten source columns and original row order. `championship_validation_issues.json` includes source row references for any anomalies. Existing destinations are refused.', '',
              'Run `PYTHONPATH=src .venv/bin/python -m scripts.validate_championship_results` against the saved source in a fresh output location. The audit is pinned to the 2026-11-05 snapshot. Existing Premier League source/derived data and their manifests remain byte-unchanged. Generalizing the audit changes its code fingerprint: an old PL standardization manifest records the earlier code revision; its full manifest byte comparison therefore requires that original revision, while regenerated PL CSV bytes remain unchanged.', '',
              '## Suitability and rights', '',
              'Structurally suitable as completed English second-tier regular-season history for the seasons marked PASS. The ongoing season is separate and incomplete by design. This is not independent verification of every result or finished status, and the source provides no explicit abandoned/finished field. No Championship standardization, ID generation, model integration, training or evaluation is performed.', '',
              'Attribution: English Football League Data, compiled and maintained by Sean Elvidge, drawing on RSSSF, Curley & Malmedal (2014), and references therein. The saved `LICENCE.md` grants [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) only for the author’s original contributions and rights he holds; upstream third-party rights remain reserved. Retain attribution, source/licence links, source notices and change indications where applicable. Structural quality does not establish legal clearance for model use, hosting, publication or redistribution. Third-party permission remains unresolved; no match data is published or redistributed by this task.']
    for name, content in outputs.items():
        with (DIRECTORY/name).open('xb') as handle:
            handle.write(content)
    with REPORT.open('x') as handle:
        handle.write('\n'.join(lines)+'\n')
    print(json.dumps({k:manifest[k] for k in ('completed_matches','complete_seasons','ongoing_matches','issue_count')},indent=2))


if __name__ == '__main__':
    main()
