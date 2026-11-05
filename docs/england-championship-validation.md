# English second-tier structural validation

Extracted 2026-11-05 from the existing local source; no new dataset download. Source: [Sean Elvidge / England-football-results](https://github.com/seanelvidge/England-football-results), commit `84d4d8877def6338a8cf55479f40bbc1216f84bc`; originally retrieved 2026-11-05.

Original `EnglandLeagueResults.csv`: 212,808 rows; SHA-256 `ac3fb5895c494d1e1e2c70726c1373320461f151966a414fda133f5f262c91dd`. Prior source/provenance checksums were verified before extraction.

**Results:** 19,872 historical matches, 36 complete seasons; 168 ongoing 2026/2027 matches; 0 structural issues.

## Competition identity and historical names

All periods represent the same English second-tier competition. The user-selected future standardized league identifier is exactly **`EFL Championship`**. It supersedes the earlier planning proposal `england.championship` for future datasets of this competition; no existing identifiers or standardized datasets are changed in this task. These extracts retain the source `Division` and `Season` values and have no added standardized league or match_id column.

| Seasons | Historical source competition name |
|---|---|
| 1990/1991–1991/1992 | Football League Second Division |
| 1992/1993–2003/2004 | Football League First Division |
| 2004/2005–2015/2016 | Football League Championship |
| 2016/2017 onwards | EFL Championship |

Naming boundaries match all selected local `Division` values. For historical context see [RSSSF second-tier history](https://www.rsssf.org/tablese/eng2champ.html) and [EFL innovation/rebranding](https://www.efl.com/about-the-efl/history/innovation/) (2016 rebrand visible in search-indexed text; direct EFL history pages returned shells). `Tier = 2` determines level; filtering by “First Division” alone would mix levels across 1992.

## Season validation

Each observed season has 24 participants. Expected regular-season matches are independently configured as 24 × 23 = 552, and also computed from the observed number of distinct teams as n × (n − 1). Both counts agree in this snapshot. For each completed season, every ordered home-away pairing occurs exactly once (23 home and 23 away appearances per team). Ongoing completeness is not required.

| Season | Historical competition name | Teams | Expected | Actual | First date | Last date | Status | Anomalies |
|---|---|---:|---:|---:|---|---|---|---|
| 1990/1991 | Football League Second Division | 24 | 552 | 552 | 1990-08-25 | 1991-05-11 | PASS | none |
| 1991/1992 | Football League Second Division | 24 | 552 | 552 | 1991-08-17 | 1992-05-02 | PASS | none |
| 1992/1993 | Football League First Division | 24 | 552 | 552 | 1992-08-15 | 1993-05-09 | PASS | none |
| 1993/1994 | Football League First Division | 24 | 552 | 552 | 1993-08-14 | 1994-05-08 | PASS | none |
| 1994/1995 | Football League First Division | 24 | 552 | 552 | 1994-08-13 | 1995-05-07 | PASS | none |
| 1995/1996 | Football League First Division | 24 | 552 | 552 | 1995-08-12 | 1996-05-05 | PASS | none |
| 1996/1997 | Football League First Division | 24 | 552 | 552 | 1996-08-16 | 1997-05-04 | PASS | none |
| 1997/1998 | Football League First Division | 24 | 552 | 552 | 1997-08-09 | 1998-05-03 | PASS | none |
| 1998/1999 | Football League First Division | 24 | 552 | 552 | 1998-08-08 | 1999-05-09 | PASS | none |
| 1999/2000 | Football League First Division | 24 | 552 | 552 | 1999-08-07 | 2000-05-07 | PASS | none |
| 2000/2001 | Football League First Division | 24 | 552 | 552 | 2000-08-12 | 2001-05-06 | PASS | none |
| 2001/2002 | Football League First Division | 24 | 552 | 552 | 2001-08-11 | 2002-04-21 | PASS | none |
| 2002/2003 | Football League First Division | 24 | 552 | 552 | 2002-08-10 | 2003-05-04 | PASS | none |
| 2003/2004 | Football League First Division | 24 | 552 | 552 | 2003-08-09 | 2004-05-09 | PASS | none |
| 2004/2005 | Football League Championship | 24 | 552 | 552 | 2004-08-07 | 2005-05-08 | PASS | none |
| 2005/2006 | Football League Championship | 24 | 552 | 552 | 2005-08-06 | 2006-04-30 | PASS | none |
| 2006/2007 | Football League Championship | 24 | 552 | 552 | 2006-08-05 | 2007-05-06 | PASS | none |
| 2007/2008 | Football League Championship | 24 | 552 | 552 | 2007-08-11 | 2008-05-04 | PASS | none |
| 2008/2009 | Football League Championship | 24 | 552 | 552 | 2008-08-09 | 2009-05-03 | PASS | none |
| 2009/2010 | Football League Championship | 24 | 552 | 552 | 2009-08-07 | 2010-05-02 | PASS | none |
| 2010/2011 | Football League Championship | 24 | 552 | 552 | 2010-08-06 | 2011-05-07 | PASS | none |
| 2011/2012 | Football League Championship | 24 | 552 | 552 | 2011-08-05 | 2012-04-28 | PASS | none |
| 2012/2013 | Football League Championship | 24 | 552 | 552 | 2012-08-17 | 2013-05-04 | PASS | none |
| 2013/2014 | Football League Championship | 24 | 552 | 552 | 2013-08-03 | 2014-05-03 | PASS | none |
| 2014/2015 | Football League Championship | 24 | 552 | 552 | 2014-08-08 | 2015-05-02 | PASS | none |
| 2015/2016 | Football League Championship | 24 | 552 | 552 | 2015-08-07 | 2016-05-07 | PASS | none |
| 2016/2017 | EFL Championship | 24 | 552 | 552 | 2016-08-05 | 2017-05-07 | PASS | none |
| 2017/2018 | EFL Championship | 24 | 552 | 552 | 2017-08-04 | 2018-05-06 | PASS | none |
| 2018/2019 | EFL Championship | 24 | 552 | 552 | 2018-08-03 | 2019-05-05 | PASS | none |
| 2019/2020 | EFL Championship | 24 | 552 | 552 | 2019-08-02 | 2020-07-22 | PASS | none |
| 2020/2021 | EFL Championship | 24 | 552 | 552 | 2020-09-11 | 2021-05-08 | PASS | none |
| 2021/2022 | EFL Championship | 24 | 552 | 552 | 2021-08-06 | 2022-05-07 | PASS | none |
| 2022/2023 | EFL Championship | 24 | 552 | 552 | 2022-07-29 | 2023-05-08 | PASS | none |
| 2023/2024 | EFL Championship | 24 | 552 | 552 | 2023-08-04 | 2024-05-04 | PASS | none |
| 2024/2025 | EFL Championship | 24 | 552 | 552 | 2024-08-09 | 2025-05-03 | PASS | none |
| 2025/2026 | EFL Championship | 24 | 552 | 552 | 2025-08-08 | 2026-05-02 | PASS | none |
| 2026/2027 | EFL Championship | 24 | 552 | 168 | 2026-08-14 | 2026-11-04 | ONGOING | in progress; not tested for full-season completeness |

## Checks and playoff scope

The shared `scripts.validate_england_results.audit` now accepts explicit tier, first-season and participant-count parameters; its Premier League defaults remain unchanged. It reuses the historical importer’s `canonical_season` and shared `exact_integer`, `team_name` and `outcome_from_goals` checks. Checks cover CSV headers/row widths; missing/invalid dates, teams and goals; nonnegative integer goals; Score/goals/Result consistency; dates after snapshot retrieval; exact/conflicting duplicate match identities; repeated season home-away pairings; missing seasons; participant and match counts; and full ordered-pairing coverage. The Championship wrapper adds source historical-name checks, observed-team expected totals and bounded known-playoff checks. Anomalous source rows are preserved and reported, never silently corrected or deduplicated.

No extra/repeated pairings or playoff-labelled rows were found in the Tier 2 extraction. All completed seasons stop with a complete regular-season round robin (552 matches), rather than 557 including the usual five playoff matches. The source has no stage/status field, so pairing/count evidence supports regular-season-only scope but cannot exclude a hypothetical mislabelled substitution for a missing regular-season game. There is no exhaustive independent result/stage verification in this task.

Known promotion playoff finals were checked by season, date and both club orientations (Brighton naming aliases used only for lookup; stored names unchanged):

| Season | Date | Clubs | In extract? | Evidence |
|---|---|---|---|---|
| 1990/1991 | 1991-06-02 | Brighton and Hove Albion / Notts County | ABSENT | [Reference](https://www.11v11.com/matches/brighton-and-hove-albion-v-notts-county-02-june-1991-279330/) |
| 2003/2004 | 2004-05-29 | Crystal Palace / West Ham United | ABSENT | [Reference](https://www.uefa.com/news-media/news/019d-0f8fc0d7fa91-cdea0ec771a1-1000--palace-crown-promotion-push/) |
| 2024/2025 | 2025-05-24 | Sheffield United / Sunderland | ABSENT | [Reference](https://www.efl.com/news/2025/may/24/sunderland-win-championship-play-off-final-in-dramatic-fashion/) |

The 1991 and 2004 references were directly readable. The 2025 EFL result was available in indexed text; the official [Championship playoff archive](https://www.efl.com/competitions/sky-bet-play-offs/about-the-play-offs/championship-play-off-finals/) and schedule/history pages returned incomplete page shells. Those shells are not treated as a verified full playoff inventory. No access limits were bypassed and no bulk scraping was performed. Missing playoffs are intentional for a regular-season dataset, not missing regular fixtures.

## Local artifacts and reproduction

All extracted match data and diagnostics are exclusively under Git-ignored `data/private/england/`:

| File | SHA-256 |
|---|---|
| `championship_1990_2025.csv` | `6c0bf7449436fb34bdcb183d838237d6b3657e7fdc2f7d1e815a7862147e45b7` |
| `championship_2026_2027_ongoing.csv` | `4146e72ad9aa0e51373fe435780deca1004ea169d75d0b641d8174cd8769c162` |
| `championship_season_validation.csv` | `9d5eda56a7c8d4c30ef87d192dff02d29c7faa47f7f778d1267bfed5bac00423` |
| `championship_validation_issues.json` | `37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570` |

`championship_provenance.json` records the source URL/commit/retrieval and extraction dates, raw checksum, extraction/naming rules, checksummed outputs, code fingerprints, playoff checks and licensing scope. Extracts retain all ten source columns and original row order. `championship_validation_issues.json` includes source row references for any anomalies. Existing destinations are refused.

Run `PYTHONPATH=src .venv/bin/python -m scripts.validate_championship_results` against the saved source in a fresh output location. The audit is pinned to the 2026-11-05 snapshot. Existing Premier League source/derived data and their manifests remain byte-unchanged. Generalizing the audit changes its code fingerprint: an old PL standardization manifest records the earlier code revision; its full manifest byte comparison therefore requires that original revision, while regenerated PL CSV bytes remain unchanged.

## Suitability and rights

Structurally suitable as completed English second-tier regular-season history for the seasons marked PASS. The ongoing season is separate and incomplete by design. This is not independent verification of every result or finished status, and the source provides no explicit abandoned/finished field. No Championship standardization, ID generation, model integration, training or evaluation is performed.

Attribution: English Football League Data, compiled and maintained by Sean Elvidge, drawing on RSSSF, Curley & Malmedal (2014), and references therein. The saved `LICENCE.md` grants [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) only for the author’s original contributions and rights he holds; upstream third-party rights remain reserved. Retain attribution, source/licence links, source notices and change indications where applicable. Structural quality does not establish legal clearance for model use, hosting, publication or redistribution. Third-party permission remains unresolved; no match data is published or redistributed by this task.

Verification: all 287 repository tests passed, including nine new Championship cases for naming boundaries, a full synthetic 24-team round robin, missing-season/ongoing behavior and anomaly/playoff detection. All 12 pre-existing England files remain byte-unchanged, and both standardized Premier League CSVs still regenerate identically. The five new private Championship artifacts are ignored and untracked; `git diff --check` passes. No commit or push was performed.

## Independent result verification — 2026-11-05

**Outcome: 20/20 selected matches corroborated against directly readable external records**, with five match dates in each of the 1990s, 2000s, 2010s and 2020s. Dates, home/away identities, final scores and historical second-tier regular-season classification agree with the local dataset. There are no unresolved discrepancies in the selected local records. One conflicting third-party season page is documented below. This verifies a sample at the separate-publication level; shared upstream sources prevent a claim of fully independent data lineage.

### Reproducible sample

Visit season start years `[1990, 1992, 1994, 1996, 1998, 2000, 2002, 2004, 2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020, 2021, 2022, 2023, 2024]` in that order. Set `seed = "TOTOdology Championship verification v1"` and an initially empty used-home-team set. In each season exclude rows whose home team has already been selected; select the minimum hexadecimal SHA-256 of compact UTF-8 JSON `[seed, Season, Date, HomeTeam, AwayTeam]`, using `ensure_ascii=False` and separators `(',', ':')`. Add its home team to the set. Match scores are not used for selection. This rule was applied to the unchanged completed export with SHA-256 `6c0bf7449436fb34bdcb183d838237d6b3657e7fdc2f7d1e815a7862147e45b7` before external lookup. No match was replaced because of access difficulty or disagreement.

The sample covers 20 seasons and 20 distinct home teams, with autumn, winter and late-season fixtures rather than only opening days. It is deterministic and diversity-constrained, not a statistically representative accuracy estimate. Neither 2025/26 nor ongoing 2026/27 was sampled. Full local rows, external observations, URLs, access modes, selection method, naming equivalences and unchanged-file checksums are saved privately in `data/private/england/championship_independent_verification_2026-11-05.json`. No full articles or external bulk datasets were copied.

### Match comparisons

For each MATCH row the date and home-away identities shown agree in both records (apart from the explicit Brighton spelling convention), and the local and external final scores are listed separately. Every external competition label below is an ordinary league entry, not a cup/playoff label. “Level 2” interprets that label in its historical season; a page's current club-navigation division is not used as evidence of historical level.

| # | Season | Match date (local = external) | Home — Away (local names) | Local FT | External FT | External competition / level / stage | Readable reference | Findings |
|---:|---|---|---|---|---|---|---|---|
| 1 | 1990/1991 | 1990-11-07 | Millwall — Oxford United | 1-2 | 1-2 | League Division Two; level 2; regular season | [11v11](https://www.11v11.com/teams/millwall/tab/opposingTeams/opposition/Oxford%20United/) | MATCH. No differences observed. |
| 2 | 1992/1993 | 1992-09-15 | Peterborough United — Millwall | 0-0 | 0-0 | League Division 1; level 2; regular season | [11v11](https://www.11v11.com/teams/peterborough-united/tab/opposingTeams/opposition/Millwall/) | MATCH. No differences observed. |
| 3 | 1994/1995 | 1995-03-19 | Grimsby Town — Sunderland | 3-1 | 3-1 | League Division 1; level 2; regular season | [11v11](https://www.11v11.com/teams/sunderland/tab/opposingTeams/opposition/Grimsby%20Town/) | MATCH. No differences observed. |
| 4 | 1996/1997 | 1996-09-29 | Port Vale — Bradford City | 1-1 | 1-1 | League Division 1; level 2; regular season | [11v11](https://www.11v11.com/teams/port-vale/tab/opposingTeams/opposition/Bradford%20City/) | MATCH. External-source conflict: Wikipedia reverses home/away; 11v11 and contemporary newspaper support local orientation. |
| 5 | 1998/1999 | 1999-01-30 | Oxford United — Barnsley | 1-0 | 1-0 | League Division 1; level 2; regular season | [11v11](https://www.11v11.com/teams/oxford-united/tab/opposingTeams/opposition/Barnsley/) | MATCH. No differences observed. |
| 6 | 2000/2001 | 2001-03-03 | Stockport County — Wimbledon | 2-2 | 2-2 | League Division 1; level 2; regular season | [11v11](https://www.11v11.com/teams/stockport-county/tab/opposingTeams/opposition/Wimbledon/) | MATCH. No differences observed. |
| 7 | 2002/2003 | 2002-08-11 | Bradford City — Wolverhampton Wanderers | 0-0 | 0-0 | Football League (N1); level 2; regular season | [Wolves Complete History](https://wolvescompletehistory.co.uk/bradford-city-first-team-fixtures/) | MATCH. Archive is Wolves-oriented; Valley Parade establishes Bradford at home; 0-0 is symmetric. N1 denotes the post-1992 First Division. |
| 8 | 2004/2005 | 2005-04-09 | Watford — Leeds United | 1-2 | 1-2 | Championship; level 2; regular season | [Old Watford](https://oldwatford.com/2005/04/09/9th-april-2005-championship-watford-1-leeds-united-2/) | MATCH. Fan-maintained scrapbook archive; result and league heading readable, with source links/programme material; less authoritative than a governing-body record. |
| 9 | 2006/2007 | 2007-02-10 | Coventry City — Cardiff City | 2-2 | 2-2 | League Championship; level 2; regular season | [11v11](https://www.11v11.com/teams/coventry-city/tab/matches/season/2007/) | MATCH. No differences observed. |
| 10 | 2008/2009 | 2008-09-14 | Queens Park Rangers — Southampton | 4-1 | 4-1 | League Championship; level 2; regular season | [11v11](https://www.11v11.com/teams/queens-park-rangers/tab/opposingTeams/opposition/Southampton/) | MATCH. Indexed Sky report agrees; direct Sky fetch failed. Readable 11v11 fallback used. |
| 11 | 2010/2011 | 2011-01-01 | Swansea City — Reading | 1-0 | 1-0 | League Championship; level 2; regular season | [11v11](https://www.11v11.com/teams/swansea-city/tab/opposingTeams/opposition/Reading/) | MATCH. Indexed Sky report agrees; direct Sky fetch failed. Readable archive separately labels the May playoff final. |
| 12 | 2012/2013 | 2013-02-09 | Brighton & Hove Albion — Hull City | 1-0 | 1-0 | League Championship; level 2; regular season | [11v11](https://www.11v11.com/teams/brighton-and-hove-albion/tab/opposingTeams/opposition/Hull%20City/) | MATCH. External spelling Brighton and Hove Albion versus local Brighton & Hove Albion; identity agrees. Indexed Sky report/date header also agree; direct Sky fetch failed. |
| 13 | 2014/2015 | 2015-05-02 | Leeds United — Rotherham United | 0-0 | 0-0 | League Championship; level 2; regular season | [11v11](https://www.11v11.com/teams/leeds-united/tab/opposingTeams/opposition/Rotherham%20United/) | MATCH. Indexed Soccerbase result agrees; direct Soccerbase request timed out. Readable 11v11 fallback used. |
| 14 | 2016/2017 | 2017-01-21 | Wigan Athletic — Brentford | 2-1 | 2-1 | League Championship; level 2; regular season | [11v11](https://www.11v11.com/teams/wigan-athletic/tab/opposingTeams/opposition/Brentford/) | MATCH. Official Brentford result agrees in indexed text; direct report inaccessible. Readable official preview confirms date/competition; 11v11 supplies readable result. |
| 15 | 2018/2019 | 2019-04-10 | Rotherham United — Aston Villa | 1-2 | 1-2 | League Championship; level 2; regular season | [11v11](https://www.11v11.com/teams/rotherham-united/tab/opposingTeams/opposition/Aston%20Villa/) | MATCH. Indexed Sky report agrees; direct Sky fetch failed. Readable 11v11 fallback used. |
| 16 | 2020/2021 | 2020-09-19 | Luton Town — Derby County | 2-1 | 2-1 | Sky Bet Championship; level 2; regular season | [Sky Sports](https://www.skysports.com/football/luton-vs-derby/report/429720) | MATCH. No differences observed. |
| 17 | 2021/2022 | 2021-09-18 | Hull City — Sheffield United | 1-3 | 1-3 | League Championship; level 2; regular season | [11v11](https://www.11v11.com/teams/hull-city/tab/opposingTeams/opposition/Sheffield%20United/) | MATCH. Indexed Sky report agrees; direct Sky fetch failed. Readable 11v11 fallback used. |
| 18 | 2022/2023 | 2023-03-18 | Blackpool — Coventry City | 1-4 | 1-4 | Sky Bet Championship; level 2; regular season | [Sky Sports](https://www.skysports.com/football/blackpool-vs-coventry-city/468269) | MATCH. No differences observed. |
| 19 | 2023/2024 | 2024-02-10 | Sunderland — Plymouth Argyle | 3-1 | 3-1 | League Championship; level 2; regular season | [11v11](https://www.11v11.com/teams/sunderland/tab/opposingTeams/opposition/Plymouth%20Argyle/) | MATCH. Indexed Sky report agrees; direct Sky fetch failed. Readable 11v11 fallback used. |
| 20 | 2024/2025 | 2024-11-27 | Cardiff City — Queens Park Rangers | 0-2 | 0-2 | Sky Bet Championship; level 2; regular season | [Sky Sports](https://www.skysports.com/football/cardiff-city-vs-queens-park-rangers/report/509543) | MATCH. No differences observed. |

Historical source names remain unchanged: Football League Second Division through 1991/92, Football League First Division from 1992/93 through 2003/04, Football League Championship from 2004/05 through 2015/16, and EFL Championship thereafter. External “League Division 1”/“Football League (N1)” in 1992–2004 means the second tier, not the former top tier. “League Championship”, “Championship” and sponsored “Sky Bet Championship” labels identify the same level after 2004; retrospective website branding is not adopted as the historical source name. The agreed future identifier remains exactly `EFL Championship`; no standardized match file or identifier was generated here.

Regular-season checks used the external per-match competition field and season context, not merely the match date. Archive lists distinguish other encounters between the same clubs as cup or playoff fixtures. In particular, the Swansea–Reading page separately labels the 30 May 2011 meeting as a playoff and the sampled 1 January 2011 match as League Championship; the Brighton–Hull page labels their 2014/2016 cup meetings separately. Sky's readable Luton, Blackpool and Cardiff reports describe league standings/points, not knockout progression. The Wolves archive records the Bradford fixture as Football League (N1), while its cup encounters have separate FL Cup labels. The Old Watford entry explicitly places Watford–Leeds under Championship. No sampled fixture is classified as a promotion playoff or cup match.

### Discrepancies and reference limitations

- **Home-away conflict in a reference, not an adopted dataset correction:** the [Port Vale 1996/97 Wikipedia season page](https://en.wikipedia.org/wiki/1996%E2%80%9397_Port_Vale_F.C._season) lists the 29 September 1996 match as Bradford City hosting Port Vale. The directly readable 11v11 record instead lists Port Vale hosting Bradford, 1-1, matching the local CSV. The contemporary [Independent report](https://www.the-independent.com/sport/jacobs-makes-bradford-s-point-with-late-equaliser-1365669.html) also describes Bradford as the visiting side; [Soccerbase's indexed record](https://www.soccerbase.com/teams/head_to_head.sd?team2_id=2083&team_id=234) agrees with Port Vale at home on 29 September. The newspaper page is dated 29 September but says “yesterday”, so its relative-date wording is not used to independently establish the exact match date. The explicit archive date is used. No local value was changed. Wikipedia and its mirrors are not counted as additional corroboration.
- **Names:** 11v11 uses `Brighton and Hove Albion`, while the CSV uses `Brighton & Hove Albion`; the club identity and home-away placement agree. Short forms in supplemental reports include QPR, Wolves, Leeds, Rotherham, Hull, Swansea and Cardiff. Wimbledon is retained as the historical club name; it was not relabelled AFC Wimbledon or Milton Keynes Dons.
- **Publication dates:** the [Brighton–Hull report](https://www.skysports.com/football/news/11741/8487916/championship-vicentes-late-free-kick-snatched-a-1-0-win-for-brighton-over-hull) was updated on 11 February 2013; the sampled game is 9 February, as explicitly recorded in the archive and indexed match header. Publication/update dates are not substituted for match dates.
- **Official access:** [EFL Matches](https://www.efl.com/matches) returned only “Loading...” and supplied no usable historical match record. No EFL page shell is counted as verification. Earlier official archive access limits remain as described above; no private endpoint or access-control workaround was used.
- **Initial unavailable pages, followed by readable fallbacks:** direct Sky requests failed for [QPR–Southampton 2008](https://www.skysports.com/football/queens-park-rangers-vs-southampton/report/3999), [Swansea–Reading 2011](https://www.skysports.com/football/swansea-city-vs-reading/report/216843), [Brighton–Hull 2013](https://www.skysports.com/football/brighton-and-hove-albion-vs-hull-city/teams/262407), [Rotherham–Villa 2019](https://www.skysports.com/football/news/11679252/rotherham-1-2-aston-villa-jack-grealish-fires-winner-for-10-man-side), [Hull–Sheffield United 2021](https://www.skysports.com/football/hull-city-vs-sheffield-united/447427) and [Sunderland–Plymouth 2024](https://www.skysports.com/football/sunderland-vs-plymouth-argyle/485072), although indexed text supported the records. [Soccerbase's 2 May 2015 results](https://www.soccerbase.com/matches/results.sd?date=2015-05-02) timed out. The [official Brentford report](https://www.brentfordfc.com/en/news/wigan-athletic-v-brentford_143906) was inaccessible directly, while indexed text supported the 2-1 result and its [readable official preview](https://www.brentfordfc.com/en/news/match-preview-wigan-athletic-vs-brentford_144212) confirmed date and Championship context. In each case the table uses a readable archive fallback; the unavailable page is only supplemental, not assumed to have loaded successfully. All 20 sample records ultimately have readable references; there are no wholly unavailable sample records.

### Reliability and independence

Fifteen primary table references are 11v11 historical records with explicit date, match orientation, score and competition fields. It is a useful specialist archive, but **11v11 is a named upstream source in Sean Elvidge's saved licence**: these checks establish external-record agreement, not independent provenance for those 15 matches. The source list also names Statto, RSSSF, Wikipedia, BBC and other providers; repeating those records does not multiply independent evidence.

Three primary references are readable Sky Sports match reports, providing contemporary narrative and league context; indexed Sky and official-club reports supply additional agreement for several other matches. Shared news/data suppliers cannot be excluded. Wolves Complete History states it has been taken over by Wolves Museum; its compact club fixture record provides a separate historical reference but does not document independent data lineage for this record. Old Watford is a fan-maintained historical scrapbook, useful for its explicit match heading and supporting material, but lower-authority than a governing-body database; its embedded results cite Statto, itself an upstream source. The contemporary Independent report helps resolve the Port Vale orientation conflict, with the relative-date caveat above. These are bounded public page reads and searches, not a bulk scrape.

### Data preservation and readiness

SHA-256 checks before and after verification confirm that all 17 pre-existing files in `data/private/england/` are byte-unchanged, including the original source, both Championship extracts, their provenance/diagnostics, and all Premier League files. The completed file still has exactly **19,872 rows** and equals the original source's Tier 2, 1990/1991–2025/2026 partition, including row order and every source column. The separate ongoing file still has **168 rows**, exclusively 2026/2027, and equals its original-source partition. No ongoing-season row entered completed history. The new verification manifest is Git-ignored and untracked.

**Ready for a separately authorized standardization stage at the stated assurance level:** full structural checks pass and the 20-match external sample corroborates dates, identities, scores and regular-season second-tier classification. No observed local-data discrepancy blocks standardization. This is not exhaustive real-world result/status verification, and shared-source lineage prevents calling the entire dataset independently certified. The source still lacks an explicit finished/abandoned status field. Further independently sourced checks, especially for unsampled seasons and fixtures, would strengthen assurance.

**Licensing remains unresolved:** the original-contribution CC BY 4.0 grant does not clear all third-party rights. Preserve Sean Elvidge's attribution, original source/commit, licence and upstream notices, and document future schema transformations when authorized. The future league identifier and historical names remain as recorded above. This verification provides no new rights for model use, public hosting or redistribution. No match data was changed, standardized, integrated, committed or pushed; prediction, Streamlit and Premier League files were untouched.

## Standardized TOTOdology format — 2026-11-05

**Outcome: PASS.** Standardized 19,872 completed regular-season records (1990/1991–2025/2026) and 168 ongoing 2026/2027 records into separate new files. Earlier source/extracted data, Premier League outputs and all existing manifests remain byte-unchanged. This section records the newly authorized conversion; earlier statements that standardization had not yet occurred describe those earlier stages.

### Shared conversion and identity

The existing `scripts.standardize_england_results.convert_rows` now accepts explicit `league`, `tier` and season-to-source-division mappings. Its Premier League defaults are retained. `scripts/standardize_championship_results.py` supplies **`EFL Championship`**, Tier 2, and the historical-name mapping already used by the Championship audit. It reuses the entire conversion/validation path; no second row converter or ID implementation was added.

The adapter first verifies the source and extraction checksums, matches the sampled historical export checksum, reruns the Championship structural audit, checks the 36 PASS completed seasons plus one ONGOING season, and requires exact source/extract partition equality. The shared converter then translates ISO dates into a temporary supported-schema day-first CSV inside private storage and delegates to `import_historical_csvs`. That importer generates IDs, canonical seasons and deterministic record ordering. Temporary bridge files are removed automatically.

| Source field / explicit metadata | Standard output / handling |
|---|---|
| `Date` | `date`, unchanged ISO `YYYY-MM-DD` after the importer bridge |
| `Season` | `season`, unchanged canonical `YYYY/YYYY`, matching the PL convention |
| `HomeTeam`, `AwayTeam` | `home_team`, `away_team`, exact source names; no aliases applied |
| `hGoal`, `aGoal` | `home_goals`, `away_goals`, nonnegative integers |
| Tier 2 and historical `Division` | Checked against explicit historical mapping; not saved as extra columns |
| `Score`, `Result` | Checked against goals, then omitted from the eight-column output |
| User-selected league identifier | `league = EFL Championship` for the entire historical and ongoing period |
| Existing importer identity algorithm | `match_id` as described below |

Saved columns, in order: `match_id,date,league,season,home_team,away_team,home_goals,away_goals`.

IDs use the same full SHA-256 algorithm as Premier League standardization: compact UTF-8 JSON `[league, season, ISO date, home_team, away_team]`, `ensure_ascii=False`, separators `(',', ':')`. The league string is exactly `EFL Championship` for all predecessor eras. Scores, source paths and input row order do not affect IDs; verified changes to dates/names would change identity. CSV serialization reuses `scripts.artifact_io.serialize_csv` with UTF-8 and LF. Historical source division names and ranges remain documented above, without renaming the original data or adding columns to the standard schema.

### Outputs and validation

All three new artifacts are exclusively under Git-ignored `data/private/england/`:

| File | Records | Season scope | SHA-256 |
|---|---:|---|---|
| `championship_standardized_1990_2025.csv` | 19,872 | 1990/1991–2025/2026 | `922f376ee98320356bcd90117f1baec2901958c994f6eed46f5721ff47fc49fe` |
| `championship_standardized_2026_2027_ongoing.csv` | 168 | 2026/2027 only; ongoing | `04f1c7203c985d9b91a9d88d11908261ebba09a2ec623924b2dea8637158ee1a` |

`championship_standardization_manifest.json` records source URL/commit/retrieval date, conversion date, input and code fingerprints, historical mappings, league/season conventions, validations, playoff checks, importer summaries, output byte counts/checksums, attribution and unresolved licensing restrictions.

Validation results:

- Exactly **19,872** historical and **168** ongoing records. No 2026/2027 row enters historical output; completed season scope remains 1990/1991–2025/2026.
- Exactly the eight requested columns, with no blank required fields. Import totals equal accepted counts; rejected, fixtures, duplicates and conflicts are zero in both partitions.
- Match IDs are unique within and across the two partitions. Season home-away fixture keys are unique even when match dates are ignored; no repeated fixture was silently removed.
- Multiset equality against the original source partitions proves all match dates, canonical seasons, full team names and integer final scores are preserved. The source Score and Result columns are checked against those goals before omission.
- Both serialized outputs pass the existing `load_historical_data` → `validate_historical_data` path. Its date/type conversion, ordering and derived result field do not alter saved match facts; the saved CSVs retain only eight columns.
- Reversed-input conversions produce identical bytes and IDs. A separate `--check` rebuild from the unchanged original source confirms both saved CSVs and the new manifest reproduce byte-for-byte.
- All **303 repository tests pass**, including 16 new Championship converter cases: four historical naming eras, explicit competition rejection, malformed/inconsistent values, preservation/normalization refusal, repeated/conflicting fixtures, competition-specific IDs, unchanged PL defaults, overwrite refusal and mismatch reporting without replacing outputs.
- All 18 pre-existing England files remain byte-unchanged. The two existing standardized PL CSVs still reproduce identically with the extended shared converter. Old PL manifests retain their original code fingerprints and were not rewritten.

### Reproduction and overwrite protection

From the repository root:

```sh
# First creation only; refuses existing output destinations.
PYTHONPATH=src .venv/bin/python -m scripts.standardize_championship_results

# Rebuild and compare both existing CSVs and the manifest without overwriting them.
PYTHONPATH=src .venv/bin/python -m scripts.standardize_championship_results --check
```

The converter is pinned to this saved 2026-11-05 source/extraction snapshot and expected counts; it performs no downloads. Check mode uses and removes a temporary private import bridge, but never replaces source/extracted/standardized output files. Code fingerprints are intentionally part of provenance: reproducing a manifest after future implementation changes requires its recorded code revision. No force-overwrite option is provided.

### Updated readiness and unresolved rights

**Technically ready for future integration at the documented assurance level.** The required standardized artifacts now exist and pass schema, count, identity, factual-preservation, historical-validator compatibility and reproducibility checks. No conversion anomaly was found. The previous 20-match external verification remains sample-based, with shared-source and access limitations; conversion does not establish exhaustive result/stage accuracy or supply a missing finished-status field. The ongoing season must remain separate from completed-season inputs. No application/model connection was made.

**Legal clearance remains unresolved.** Sean Elvidge's original-contribution CC BY 4.0 grant does not clear all third-party rights. The private manifest preserves creator attribution, original source and commit, licence scope and upstream-rights limitations. Changes consist of season/tier filtering, schema/date-syntax translation, deterministic ordering and generated IDs; match dates, names and scores are unchanged. Preserve required source/licence/change notices and establish permissions needed for intended downstream use before treating the dataset as legally cleared for model use, hosting, publication or redistribution.

No original, extracted or Premier League match data was overwritten; no prediction/Streamlit changes, model integration, training, evaluation, publication, commits or pushes were performed.
