# Premier League source validation

Retrieved 2026-11-05 (Europe/Budapest). Source: [Sean Elvidge / England-football-results](https://github.com/seanelvidge/England-football-results), commit `84d4d8877def6338a8cf55479f40bbc1216f84bc`.

Original CSV: 212,808 rows; SHA-256 `ac3fb5895c494d1e1e2c70726c1373320461f151966a414fda133f5f262c91dd`.

Scope: Tier 1 from 1992/1993. Raw columns, values and order are preserved; no corrections or deduplication. Completed seasons end at 2025/2026; 2026/2027 is saved separately as ongoing.

Expected double round-robin totals: 22 × 21 = 462 for 1992/1993–1994/1995; 20 × 19 = 380 thereafter. [Premier League history](https://www.premierleague.com/en/history). Missing entire seasons are checked explicitly. Ordered home-away pairings are checked as well as totals.

| Season | Matches / expected | Teams | First date | Last date | Status | Issues |
|---|---:|---:|---|---|---|---|
| 1992/1993 | 462 / 462 | 22 | 1992-08-15 | 1993-05-11 | PASS | none |
| 1993/1994 | 462 / 462 | 22 | 1993-08-14 | 1994-05-08 | PASS | none |
| 1994/1995 | 462 / 462 | 22 | 1994-08-20 | 1995-05-14 | PASS | none |
| 1995/1996 | 380 / 380 | 20 | 1995-08-19 | 1996-05-04 | PASS | none |
| 1996/1997 | 380 / 380 | 20 | 1996-08-17 | 1997-05-11 | PASS | none |
| 1997/1998 | 380 / 380 | 20 | 1997-08-09 | 1998-05-10 | PASS | none |
| 1998/1999 | 380 / 380 | 20 | 1998-08-15 | 1999-05-16 | PASS | none |
| 1999/2000 | 380 / 380 | 20 | 1999-08-07 | 2000-05-14 | PASS | none |
| 2000/2001 | 380 / 380 | 20 | 2000-08-19 | 2001-05-19 | PASS | none |
| 2001/2002 | 380 / 380 | 20 | 2001-08-18 | 2002-05-11 | PASS | none |
| 2002/2003 | 380 / 380 | 20 | 2002-08-17 | 2003-05-11 | PASS | none |
| 2003/2004 | 380 / 380 | 20 | 2003-08-16 | 2004-05-15 | PASS | none |
| 2004/2005 | 380 / 380 | 20 | 2004-08-14 | 2005-05-15 | PASS | none |
| 2005/2006 | 380 / 380 | 20 | 2005-08-13 | 2006-05-07 | PASS | none |
| 2006/2007 | 380 / 380 | 20 | 2006-08-19 | 2007-05-13 | PASS | none |
| 2007/2008 | 380 / 380 | 20 | 2007-08-11 | 2008-05-11 | PASS | none |
| 2008/2009 | 380 / 380 | 20 | 2008-08-16 | 2009-05-24 | PASS | none |
| 2009/2010 | 380 / 380 | 20 | 2009-08-15 | 2010-05-09 | PASS | none |
| 2010/2011 | 380 / 380 | 20 | 2010-08-14 | 2011-05-22 | PASS | none |
| 2011/2012 | 380 / 380 | 20 | 2011-08-13 | 2012-05-13 | PASS | none |
| 2012/2013 | 380 / 380 | 20 | 2012-08-18 | 2013-05-19 | PASS | none |
| 2013/2014 | 380 / 380 | 20 | 2013-08-17 | 2014-05-11 | PASS | none |
| 2014/2015 | 380 / 380 | 20 | 2014-08-16 | 2015-05-24 | PASS | none |
| 2015/2016 | 380 / 380 | 20 | 2015-08-08 | 2016-05-16 | PASS | none |
| 2016/2017 | 380 / 380 | 20 | 2016-08-13 | 2017-05-21 | PASS | none |
| 2017/2018 | 380 / 380 | 20 | 2017-08-11 | 2018-05-13 | PASS | none |
| 2018/2019 | 380 / 380 | 20 | 2018-08-10 | 2019-05-12 | PASS | none |
| 2019/2020 | 380 / 380 | 20 | 2019-08-09 | 2020-07-26 | PASS | none |
| 2020/2021 | 380 / 380 | 20 | 2020-09-12 | 2021-05-23 | PASS | none |
| 2021/2022 | 380 / 380 | 20 | 2021-08-13 | 2022-05-22 | PASS | none |
| 2022/2023 | 380 / 380 | 20 | 2022-08-05 | 2023-05-28 | PASS | none |
| 2023/2024 | 380 / 380 | 20 | 2023-08-11 | 2024-05-19 | PASS | none |
| 2024/2025 | 380 / 380 | 20 | 2024-08-16 | 2025-05-25 | PASS | none |
| 2025/2026 | 380 / 380 | 20 | 2025-08-15 | 2026-05-24 | PASS | none |
| 2026/2027 | 90 / 380 | 20 | 2026-08-21 | 2026-11-02 | ONGOING | in progress; not tested for full-season completeness |

Summary: **13,166 completed-season matches across 34 seasons passed**; **90 ongoing 2026/2027 matches** (2026-08-21–2026-11-02) passed row-level checks. No anomalies were identified.

Row/source issues: 0. Detailed diagnostics including original CSV row numbers: `data/private/england/validation_issues.json`.

Checks: CSV structure; season/tier metadata; missing/invalid dates, teams and goals; nonnegative exact integer goals; Score/goals/Result agreement; future dates; duplicate identities and repeated home-away pairings; team counts and season completeness. Reuses canonical_season, exact_integer, team_name and outcome_from_goals. The existing Football-Data importer is not used directly because this source uses ISO dates and hGoal/aGoal.

Artifacts (all Git-ignored under `data/private/england/`): original `EnglandLeagueResults.csv`; `premier_league_1992_2025.csv`; `premier_league_2026_2027_ongoing.csv`; `season_validation.csv`; `validation_issues.json`; `provenance.json`; source `LICENCE.md` and `SOURCE_README.md`. Provenance records pinned download URL, retrieval date, source SHA, byte sizes and SHA-256 checksums.

Licence: CC BY 4.0 covers only Sean Elvidge’s original contributions and rights he holds. Preserve creator credit, source and licence links, source notices and change indications when sharing. Third-party rights remain reserved; the saved licence names upstream sources including RSSSF, ENFA, football-data.co.uk and others. This audit does not establish blanket rights for downstream redistribution or application use.

Suitability: seasons marked PASS meet the structural, consistency and round-robin checks in this audit. This does not independently verify every real-world result or team identity. Review any REVIEW seasons before future use; retain the ongoing season separately and revalidate updates. No prediction, application or evaluation integration has been performed.

Reproduce against the saved original with `PYTHONPATH=src .venv/bin/python scripts/validate_england_results.py` in a fresh checkout/output location: existing outputs are deliberately refused. The audit date and source commit are fixed for this acquisition snapshot.

Verification: 267 repository tests passed, including three source-audit regression tests. All eight private artifacts are excluded by the existing Git ignore rule; no private files are tracked. Existing prediction/application/evaluation files and historical datasets were left unchanged.

## Targeted independent verification — 2026-11-05

**Outcome:** 20/20 sampled records agree on match date, home/away club identities and final score. This is a bounded spot check, not independent certification of all 13,166 historical results. Nineteen comparisons used directly readable match/result or official article text; the 2020 comparison used a directly readable dated Guardian results headline plus search-indexed PL/Sky match details. The evidence strength and access limits are recorded below.

### Reproducible selection and evidence

From the unchanged completed-season export, use season start years `[1992, 1994, 1996, 1998, 1999, 2000, 2002, 2004, 2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020, 2021, 2022, 2023, 2024]`. Within each season select the first row after ascending, case-sensitive lexical sorting by `(Date, HomeTeam, AwayTeam)`. This produces five matches in each decade. Selection was fixed before external checking; none were replaced because access was difficult. It is intentionally reproducible but biased toward opening weekends and alphabetically earlier home teams; it is not a random or statistically representative accuracy estimate. Mid-season/rescheduled fixtures, 2025/26 and 2026/27 were not independently sampled.

The private `independent_verification_2026-11-05.json` preserves the selection rule, local rows, compared external facts, URLs, access mode, comparison notes and completed-export checksum. External observations use full local club names after manual identity comparison; original external display aliases are described below. Only bounded factual comparisons and links were recorded, without copying articles or acquiring another bulk dataset. Public web search and individual page reads were used; no archive crawling, private endpoints or access-control bypasses were used.

In the table, the date and home-first score shown are both the local and externally observed values; MATCH means date, club identities, venue order and score agree. Here “venue order” means home versus away, not stadium-name verification.

| Season | Match date | Home — Away (local names) | Local / external score | Evidence | Comparison / notes |
|---|---|---|---|---|---|
| 1992/1993 | 1992-08-15 | Arsenal — Norwich City | 2-4 / 2-4 | [Sky Sports](https://www.skysports.com/football/arsenal-vs-norwich-city/teams/275202) | MATCH. Norwich is a short display label for Norwich City. |
| 1994/1995 | 1994-08-20 | Arsenal — Manchester City | 3-0 / 3-0 | [Sky Sports](https://www.skysports.com/football/arsenal-vs-manchester-city/276130) | MATCH. Man City abbreviates Manchester City; Sky historical venue/time metadata was outside scope. |
| 1996/1997 | 1996-08-17 | Arsenal — West Ham United | 2-0 / 2-0 | [Sky Sports](https://www.skysports.com/football/arsenal-vs-west-ham-united/276974) | MATCH. West Ham abbreviates West Ham United. |
| 1998/1999 | 1998-08-15 | Blackburn Rovers — Derby County | 0-0 / 0-0 | [11v11; Sky indexed corroboration](https://www.11v11.com/teams/blackburn-rovers/tab/matches/season/1999/) | MATCH. Blackburn/Derby abbreviate club names. Sky direct fetch failed; indexed Sky result agrees; 11v11 page agrees but is a named upstream source. |
| 1999/2000 | 1999-08-07 | Arsenal — Leicester City | 2-1 / 2-1 | [Sky Sports](https://www.skysports.com/football/arsenal-vs-leicester-city/teams/278107) | MATCH. Leicester abbreviates Leicester City. |
| 2000/2001 | 2000-08-19 | Charlton Athletic — Manchester City | 4-0 / 4-0 | [Sky Sports](https://www.skysports.com/football/charlton-vs-man-city/113672) | MATCH. Charlton/Man City abbreviate club names. |
| 2002/2003 | 2002-08-17 | Blackburn Rovers — Sunderland | 0-0 / 0-0 | [Sky Sports](https://www.skysports.com/football/blackburn-rovers-vs-sunderland/27575) | MATCH. Blackburn abbreviates Blackburn Rovers. |
| 2004/2005 | 2004-08-14 | Aston Villa — Southampton | 2-0 / 2-0 | [Sky Sports](https://www.skysports.com/football/aston-villa-vs-southampton/teams/52152) | MATCH. No differences observed. |
| 2006/2007 | 2006-08-19 | Arsenal — Aston Villa | 1-1 / 1-1 | [Sky Sports](https://www.skysports.com/football/arsenal-vs-aston-villa/74119) | MATCH. No differences observed. |
| 2008/2009 | 2008-08-16 | Arsenal — West Bromwich Albion | 1-0 / 1-0 | [Sky Sports](https://www.skysports.com/football/arsenal-vs-west-bromwich-albion/1815) | MATCH. West Brom abbreviates West Bromwich Albion. Report updated 2008-08-17; match header 2008-08-16. |
| 2010/2011 | 2010-08-14 | Aston Villa — West Ham United | 3-0 / 3-0 | [Sky Sports](https://www.skysports.com/football/aston-villa-vs-west-ham-united/215189) | MATCH. West Ham abbreviates West Ham United. |
| 2012/2013 | 2012-08-18 | Arsenal — Sunderland | 0-0 / 0-0 | [Sky Sports](https://www.skysports.com/football/arsenal-vs-sunderland/report/261561) | MATCH. No differences observed. |
| 2014/2015 | 2014-08-16 | Arsenal — Crystal Palace | 2-1 / 2-1 | [Sky Sports](https://www.skysports.com/football/arsenal-vs-crystal-palace/report/313387) | MATCH. C Palace abbreviates Crystal Palace. Report updated 2014-08-18; match header 2014-08-16. |
| 2016/2017 | 2016-08-13 | Burnley — Swansea City | 0-1 / 0-1 | [Sky Sports](https://www.skysports.com/football/burnley-vs-swansea-city/video/356337) | MATCH. Swansea abbreviates Swansea City. Separate report updated 2016-08-15; match header 2016-08-13. |
| 2018/2019 | 2018-08-10 | Manchester United — Leicester City | 2-1 / 2-1 | [Premier League](https://www.premierleague.com/en/news/723380/match-summary) | MATCH. Man Utd/Leicester are short labels. |
| 2020/2021 | 2020-09-12 | Crystal Palace — Southampton | 1-0 / 1-0 | [Guardian dated index; PL/Sky indexed corroboration](https://www.theguardian.com/football/premierleague?page=381) | MATCH. Direct PL match page was shell-only and Sky fetch failed. Guardian dated index agrees; indexed PL/Sky match details corroborate. |
| 2021/2022 | 2021-08-13 | Brentford — Arsenal | 2-0 / 2-0 | [Premier League](https://www.premierleague.com/en/news/2174882) | MATCH. No differences observed. |
| 2022/2023 | 2022-08-05 | Crystal Palace — Arsenal | 0-2 / 0-2 | [Premier League](https://www.premierleague.com/en/news/2713932) | MATCH. No differences observed. |
| 2023/2024 | 2023-08-11 | Burnley — Manchester City | 0-3 / 0-3 | [Premier League](https://www.premierleague.com/en/news/3627450) | MATCH. Man City abbreviates Manchester City. |
| 2024/2025 | 2024-08-16 | Manchester United — Fulham | 1-0 / 1-0 | [Premier League](https://www.premierleague.com/en/news/4082431) | MATCH. Man Utd abbreviates Manchester United. |

### Differences and source-access limitations

No match-date, home/away club-identity or final-score discrepancy was found. Short display labels include Norwich, Man City, West Ham, Blackburn, Derby, Leicester, Charlton, West Brom, C Palace, Swansea and Man Utd; these are naming conventions, not corrections to the private CSV. No naming map was added to application code.

Article publication/update dates must not be confused with the match date. For example, the Sky reports for Arsenal–West Brom (2008), Arsenal–Crystal Palace (2014), and Burnley–Swansea (2016) have later publication/update dates; their match headers agree with the local match dates. Old Sky pages also expose generic status legends and some present-day venue metadata; neither was used as independent evidence of match status or historical stadium names. This audit compares dates, club identities and final scores only.

The official PL match pages for [Arsenal–Norwich 1992](https://www.premierleague.com/en/match/13320), [Arsenal–Manchester City 1994](https://www.premierleague.com/en/match/13404), [Crystal Palace–Southampton 2020](https://www.premierleague.com/en/match/2128287) and [Brentford–Arsenal 2021](https://www.premierleague.com/en/match/2210271/brentford-vs-arsenal/highlights) returned navigation-only shells when opened. Search-indexed versions sometimes contained match details, but a shell was never treated as a successful direct result check. Readable PL articles were used for 2018 and 2021–2024; Sky supplied most earlier checks.

Direct Sky fetches failed for [Blackburn–Derby 1998](https://www.skysports.com/football/blackburn-rovers-vs-derby-county/277728) and [Crystal Palace–Southampton 2020](https://www.skysports.com/football/c-palace-vs-soton/428838), although indexed results exposed matching dates, teams and scores. For 1998 the directly readable 11v11 club record independently exposes the same fixture, but 11v11 is itself listed in the dataset's upstream sources: it is corroboration from another publication, not proof of independent data lineage. The matching indexed Sky result provides additional corroboration. For 2020 the directly readable Guardian dated results index supports the fixture/date/score, with matching indexed official PL and Sky details; a full directly readable match report was not obtained. BBC access was reported blocked by robots.txt and was not bypassed. Some Sky subpage fetches also failed; readable main match pages were used instead.

“Independent” here means a separate publisher/reference outside the downloaded GitHub CSV. Shared historical sources or data suppliers cannot be excluded. No claim is made that all references are independent at the underlying data-lineage level.

### Finished-result and season-separation recheck

All seven previously checksummed files still match `provenance.json`. The original source was re-audited in memory with the existing audit function: 212,808 source rows, 13,256 selected rows, zero reported structural issues; 34 completed seasons PASS and one ONGOING. The two exports were additionally compared row-for-row with their exact source filters, including order and every source field.

The historical file contains exactly **13,166 rows**, exclusively 1992/1993–2025/2026. Every row has nonnegative integer home/away goals, a matching score string and matching H/D/A result, and a valid past match date. There are no blank-score fixtures or missing results. Full ordered-pairing coverage and expected season counts still hold. The sampled external results confirm played outcomes for those 20 records.

The separate ongoing file contains exactly **90 scored results**, exclusively 2026/2027, dated 2026-08-21–2026-11-02; no 2026/2027 row is in the historical file. It remains incomplete against 380 full-season fixtures and must not be evaluated as a completed season.

The CSV has **no explicit finished/abandoned/postponed status field**. Therefore “finished matches only” is confirmed at the source's documented scored-result representation level, with independent outcome checks for the sample. A numeric score alone cannot prove that every unsampled row was completed rather than an erroneously recorded partial/administrative result. No such anomaly was detected; comprehensive independent status confirmation was not performed.

### Readiness and remaining limits

- **Structural validation: PASS for completed seasons.** Schema, missing values, goal/result consistency, duplicate identities, team counts, expected match totals and ordered pairings have been checked across the full extraction. Existing data and checksums remain unchanged.
- **Independent result verification: sample PASS, with access/lineage limits.** Twenty matches agree across four decades; 2020 has weaker evidence from a dated publisher index and indexed match details. This does not certify unsampled matches, historical identity continuity or every finished status. Future source updates need revalidation; targeted rescheduled/mid-season and latest-season checks would extend confidence.
- **Technical readiness: suitable to begin a separately authorized integration stage for completed-season history, at this stated assurance level.** No observed score/date/identity defect blocks that stage. Full exhaustive result/status certification remains unfulfilled if required. A source-specific adapter and explicit team/competition mappings will be needed because the existing importer expects different date and goal columns; no adapter or model integration was added here. Keep 2026/27 outside completed-season training/evaluation inputs.
- **Legal readiness: unresolved.** CC BY 4.0 applies only to Sean Elvidge's original contributions and rights he holds, as stated in the pinned saved licence. It does not clear third-party rights or establish permission for every downstream use, redistribution, model training or public application deployment. Independent fact agreement does not resolve this. Retain attribution, licence and upstream notices, and establish the necessary third-party permissions for the intended use before treating the source as legally cleared.

Only this documentation, the append-only planning log and a new ignored verification manifest were written during this follow-up. No source data was corrected or overwritten; prediction code, Streamlit, evaluations and the model were untouched. Nothing was committed or pushed.

## Standardized historical format — 2026-11-05

**Conversion outcome: PASS.** The completed-season dataset contains exactly 13,166 matches from 1992/1993 through 2025/2026. A separate standardized ongoing-season file contains 90 matches from 2026/2027. The original CSV and earlier extracts/reports/manifests were not overwritten.

### Reuse and mapping

`scripts/standardize_england_results.py` is an offline source adapter around the existing `import_historical_csvs`, not a second importer. It first checks the saved provenance checksums, invokes the existing source audit, and compares the earlier filtered exports to the exact original-source partitions. It requires `Tier = 1` and `Division = Premier League` explicitly. It uses a temporary supported-schema CSV inside `data/private/england/` (automatically removed) to translate the source into the existing importer's input format:

| Source / metadata | Import bridge | Standard output |
|---|---|---|
| ISO `Date` | Equivalent `DD/MM/YYYY` | `date`, restored to unchanged ISO `YYYY-MM-DD` |
| `Season` | `Season` | `season`, canonical `YYYY/YYYY` |
| `HomeTeam`, `AwayTeam` | Same fields | `home_team`, `away_team`, unchanged names |
| `hGoal`, `aGoal` | `FTHG`, `FTAG` | `home_goals`, `away_goals`, integer values |
| `Result` | `FTR`, checked against goals | Omitted from saved eight-column schema |
| `Score` | Checked against goal columns | Omitted |
| Explicit competition | `HistoricalSource.league` | `league = england.premier-league` |
| Existing importer identity | Existing importer SHA-256 | `match_id` |

The saved CSV columns, in order, are exactly `match_id,date,league,season,home_team,away_team,home_goals,away_goals`. IDs reuse the existing importer algorithm: full SHA-256 of compact UTF-8 JSON `[league, season, ISO date, home team, away team]`, with `ensure_ascii=False`. Goals and source paths are excluded from identity. IDs are stable under input reordering; a later verified date/name correction would intentionally change the ID. Records follow the existing importer's deterministic identity ordering; serialization reuses `scripts.artifact_io.serialize_csv` (UTF-8 and LF).

The adapter refuses any importer issues, including fixtures, rejected rows, deduplication or conflicts. It additionally refuses changes to the multiset of source dates, seasons, names and goals, so normalizations such as trimming team names cannot silently alter this snapshot. It checks fixture uniqueness by `(league, season, home_team, away_team)`, which also catches repeated pairings on different dates.

### Private outputs and validation

All match-bearing bridge and output files stay under Git-ignored `data/private/england/`; no new data is tracked or published.

| Output file | Matches | Season scope | SHA-256 |
|---|---:|---|---|
| `premier_league_standardized_1992_2025.csv` | 13,166 | 1992/1993–2025/2026 | `81ddd6296fa4e07f239b9565e228d4e132ee47cbea85d9faa9275b28ae95604c` |
| `premier_league_standardized_2026_2027_ongoing.csv` | 90 | 2026/2027 only; ongoing | `9088ccc7f3ca328c3e9897d13591c59da74d9461002a66ba21c3515239d9f174` |

`standardization_manifest.json` records source repository/commit/checksum, converter and reused-code checksums, mappings, league/season conventions, partition rules, validation checks, importer summaries, output checksums and retained licensing limits.

Validation performed:

- Exactly 13,166 completed historical matches across all 34 completed seasons, with no 2026/2027 rows; 90 ongoing rows remain separate. Existing source audit reconfirms season counts, team counts and pairing completeness.
- No blank required fields, duplicate IDs or duplicate season home-away fixtures in either standardized output. Import summaries are total = accepted (13,166 and 90 respectively), with zero rejected rows, duplicates, fixtures or conflicts.
- Exact multiset comparison against the original source proves dates, seasons, full team names and integer scores are unchanged; the earlier filtered extracts are also identical to their source partitions.
- Both serialized CSVs pass the existing `load_historical_data` → `validate_historical_data` path. Its in-memory timestamp conversion, sorting and derived `result` column do not change match facts. The saved output retains exactly the requested eight columns.
- Rebuilding each partition with reversed input order gives identical output bytes and IDs. A separate `--check` run rebuilds from the original and compares the saved CSVs and manifest byte-for-byte.
- All 278 repository tests pass, including 11 new adapter cases covering deterministic IDs, factual preservation, validator compatibility, malformed/inconsistent source values, normalization refusal and duplicate/conflicting/repeated-date fixtures. Tests use synthetic temporary inputs; private datasets are not needed by the test suite.

### Local reproduction

From the repository root:

```sh
# First creation only: refuses existing output destinations; no --force option.
PYTHONPATH=src .venv/bin/python -m scripts.standardize_england_results

# Verify the existing snapshot without replacing outputs.
PYTHONPATH=src .venv/bin/python -m scripts.standardize_england_results --check
```

The converter is deliberately pinned to the previously acquired snapshot (13,166 completed and 90 ongoing matches, audit date 2026-11-05). It does not download or automatically accept later source revisions. Check mode still uses and removes a temporary private import bridge. Source/output/code checksums allow another checkout with the same code and local source files to reproduce this conversion; the code fingerprints intentionally detect implementation changes.

### Updated readiness and rights

**Technical readiness: ready for future integration of completed-season history at the documented validation level.** The required standardized data artifact and source adapter now exist, and no schema, count, identity, factual-preservation or validator-compatibility blocker was found. The earlier 20-match verification remains sample-based, with its recorded access/lineage limits; conversion does not independently certify unsampled results or supply a missing finished-status field. Future integration still needs explicit authorization and deliberate competition selection; source-to-standard conversion alone does not connect data to the predictor. Keep the ongoing season separate from completed-season inputs.

**Legal clearance: still unresolved.** Source: Sean Elvidge's England Football Results repository at commit `84d4d8877def6338a8cf55479f40bbc1216f84bc`, as attributed above and in the private manifest. The saved `LICENCE.md` grants CC BY 4.0 only for his original contributions and rights he holds. Third-party rights remain reserved; this conversion supplies no new permission for redistribution, publication, model use or public deployment. Source credits and licence/change notices must be retained where applicable. The only data changes are filtering, schema/date-syntax translation, deterministic ordering and generated IDs; dates, names and scores are preserved. Establish the permissions needed for the intended downstream use before declaring legal readiness.

No prediction or Streamlit changes, training, evaluation, application integration, publication, commits or pushes were performed. Existing historical datasets and evaluation artifacts remain untouched.
