# Serie A structural validation

**Standardization update (2026-11-12): PASS — 12,644 matches / 36 seasons standardized with all 11 derivative-only date corrections and seven match-ID-linked exceptions. All originals remain unchanged; see the final standardization section for outputs, checksums, validation and readiness.**

**Independent review update (2026-11-12): 30 external fixture comparisons identified 11 date-only correction proposals; all originals remain unchanged. The initial structural PASS results below are preserved as the acquisition snapshot. See the independent-review section for two documentary REVIEW seasons and seven exception decisions.**

Retrieved and validated **2026-11-12 (Europe/Budapest)** on `feature/data-collection`, based on Homework 8 commit `e950471`. **36 completed seasons, 12,644 selected regular-season match records; all 36 structural PASS.** No missing fixtures, repeated ordered pairings, invalid required values or source score inconsistencies detected. PASS describes structure and internal consistency, not independent result/status certification. At least one record is an administrative award rather than a played match.

## Acquisition and actual coverage

Original bytes are exclusively in Git-ignored `data/private/italy/serie_a/`. Acquisition used bounded raw-file downloads from public GitHub repositories, with no scraper, API match harvesting, name reconciliation or standardized match export. The historical original includes older seasons outside the requested window; only its 1990–2024 season-start rows are audited. No 2026/27 file was downloaded.

| Source | Pinned commit | Actual coverage and selection |
|---|---|---|
| [James P. Curley / engsoccerdata](https://github.com/jalapic/engsoccerdata) | `872c5c354161ace8408f3091b758c6af4cccca94` | `data-raw/italy.csv`: 28,824 rows, season-start labels 1929–2024; 12,264 rows selected for 1990/91–2024/25 (35 seasons). |
| [OpenFootball / italy](https://github.com/openfootball/italy) | `48954d163c312aa705efacb64f771267031fe6eb` | `2025-26/1-seriea.txt`: 380 scored fixtures, 20 teams, all ordered pairings present. The matching full-detail TXT is retained as a supplemental original and is not counted again or separately certified. |

The historical README advertises results through 2024/25 (package v0.1.8); its DESCRIPTION has a stale 2020 date and a broader 1871–2026 package title. The Italy help file says 1934/35–2024/25, whereas the CSV actually begins in 1929. Actual parsed coverage takes precedence over these inconsistent descriptive dates. The upstream CSV has no explicit played/finished/award/stage field. OpenFootball’s compact header declares 380 matches; the audit parses the records rather than trusting that header.

[Football-Data Italy](https://www.football-data.co.uk/italym.php) was considered but not acquired: page access returned HTTP 429, and its terms page was inaccessible through the browsing tool. Its current coverage and permission terms were therefore not verified, and are not assumed. The two selected repositories supplied all requested seasons without requiring that supplement.

## Season-by-season validation

Expected format: 18 × 17 ordered home-away pairings = 306 matches through 2003/04; 20 × 19 = 380 thereafter. Total = 14 × 306 + 22 × 380 = **12,644**. The expansion is corroborated by [UEFA’s format announcement](https://www.uefa.com/news-media/news/0195-0f845031d5e1-47d7e9543549-1000--new-italian-league-format-agreed/). Each season has exactly n−1 home and n−1 away appearances per participant. Missing entire seasons are explicitly checked.

| Season | Source | Teams / expected | Records / expected | First date | Last date | Structural status | Context requiring result/status review |
|---|---|---:|---:|---|---|---|---|
| 1990/1991 | Curley | 18 / 18 | 306 / 306 | 1990-09-09 | 1991-05-26 | PASS | No structural anomaly; event inventory not exhaustive |
| 1991/1992 | Curley | 18 / 18 | 306 / 306 | 1991-09-01 | 1992-05-24 | PASS | No structural anomaly; event inventory not exhaustive |
| 1992/1993 | Curley | 18 / 18 | 306 / 306 | 1992-09-06 | 1993-06-06 | PASS | No structural anomaly; event inventory not exhaustive |
| 1993/1994 | Curley | 18 / 18 | 306 / 306 | 1993-08-29 | 1994-05-01 | PASS | No structural anomaly; event inventory not exhaustive |
| 1994/1995 | Curley | 18 / 18 | 306 / 306 | 1994-09-04 | 1995-06-04 | PASS | No structural anomaly; event inventory not exhaustive |
| 1995/1996 | Curley | 18 / 18 | 306 / 306 | 1995-08-27 | 1996-05-12 | PASS | No structural anomaly; event inventory not exhaustive |
| 1996/1997 | Curley | 18 / 18 | 306 / 306 | 1996-09-08 | 1997-06-01 | PASS | No structural anomaly; event inventory not exhaustive |
| 1997/1998 | Curley | 18 / 18 | 306 / 306 | 1997-08-31 | 1998-05-16 | PASS | No structural anomaly; event inventory not exhaustive |
| 1998/1999 | Curley | 18 / 18 | 306 / 306 | 1998-09-12 | 1999-05-23 | PASS | No structural anomaly; event inventory not exhaustive |
| 1999/2000 | Curley | 18 / 18 | 306 / 306 | 1999-08-28 | 2000-05-14 | PASS | No structural anomaly; event inventory not exhaustive |
| 2000/2001 | Curley | 18 / 18 | 306 / 306 | 2000-10-01 | 2001-06-17 | PASS | No structural anomaly; event inventory not exhaustive |
| 2001/2002 | Curley | 18 / 18 | 306 / 306 | 2001-08-25 | 2002-05-05 | PASS | No structural anomaly; event inventory not exhaustive |
| 2002/2003 | Curley | 18 / 18 | 306 / 306 | 2002-09-14 | 2003-05-24 | PASS | No structural anomaly; event inventory not exhaustive |
| 2003/2004 | Curley | 18 / 18 | 306 / 306 | 2003-08-30 | 2004-05-16 | PASS | Replayed Rome derby |
| 2004/2005 | Curley | 20 / 20 | 380 / 380 | 2004-09-11 | 2005-05-29 | PASS | Calciopoli standings/title context |
| 2005/2006 | Curley | 20 / 20 | 380 / 380 | 2005-08-27 | 2006-05-14 | PASS | Calciopoli standings/title context |
| 2006/2007 | Curley | 20 / 20 | 380 / 380 | 2006-09-09 | 2007-05-27 | PASS | No structural anomaly; event inventory not exhaustive |
| 2007/2008 | Curley | 20 / 20 | 380 / 380 | 2007-08-25 | 2008-05-18 | PASS | Atalanta–Milan replay |
| 2008/2009 | Curley | 20 / 20 | 380 / 380 | 2008-08-30 | 2009-05-31 | PASS | No structural anomaly; event inventory not exhaustive |
| 2009/2010 | Curley | 20 / 20 | 380 / 380 | 2009-08-22 | 2010-05-16 | PASS | No structural anomaly; event inventory not exhaustive |
| 2010/2011 | Curley | 20 / 20 | 380 / 380 | 2010-08-28 | 2011-05-22 | PASS | No structural anomaly; event inventory not exhaustive |
| 2011/2012 | Curley | 20 / 20 | 380 / 380 | 2011-09-09 | 2012-05-13 | PASS | No structural anomaly; event inventory not exhaustive |
| 2012/2013 | Curley | 20 / 20 | 380 / 380 | 2012-08-25 | 2013-05-19 | PASS | Cagliari–Roma awarded without play |
| 2013/2014 | Curley | 20 / 20 | 380 / 380 | 2013-08-24 | 2014-05-18 | PASS | No structural anomaly; event inventory not exhaustive |
| 2014/2015 | Curley | 20 / 20 | 380 / 380 | 2014-08-30 | 2015-05-31 | PASS | No structural anomaly; event inventory not exhaustive |
| 2015/2016 | Curley | 20 / 20 | 380 / 380 | 2015-08-22 | 2016-05-15 | PASS | No structural anomaly; event inventory not exhaustive |
| 2016/2017 | Curley | 20 / 20 | 380 / 380 | 2016-08-20 | 2017-05-28 | PASS | No structural anomaly; event inventory not exhaustive |
| 2017/2018 | Curley | 20 / 20 | 380 / 380 | 2017-08-19 | 2018-05-20 | PASS | No structural anomaly; event inventory not exhaustive |
| 2018/2019 | Curley | 20 / 20 | 380 / 380 | 2018-08-18 | 2019-05-26 | PASS | No structural anomaly; event inventory not exhaustive |
| 2019/2020 | Curley | 20 / 20 | 380 / 380 | 2019-08-24 | 2020-08-02 | PASS | COVID extension into August 2020 |
| 2020/2021 | Curley | 20 / 20 | 380 / 380 | 2020-09-19 | 2021-05-23 | PASS | Juventus–Napoli: initial award superseded |
| 2021/2022 | Curley | 20 / 20 | 380 / 380 | 2021-08-21 | 2022-05-22 | PASS | No structural anomaly; event inventory not exhaustive |
| 2022/2023 | Curley | 20 / 20 | 380 / 380 | 2022-08-13 | 2023-06-04 | PASS | No structural anomaly; event inventory not exhaustive |
| 2023/2024 | Curley | 20 / 20 | 380 / 380 | 2023-08-19 | 2024-06-02 | PASS | Udinese–Roma resumed |
| 2024/2025 | Curley | 20 / 20 | 380 / 380 | 2024-08-17 | 2025-05-25 | PASS | Fiorentina–Inter resumed |
| 2025/2026 | OpenFootball | 20 / 20 | 380 / 380 | 2025-08-23 | 2026-05-24 | PASS | No structural anomaly; event inventory not exhaustive |

## Validation method and preservation

`scripts/validate_serie_a.py` audits originals offline and reuses `canonical_season`, `exact_integer`, `team_name`, `outcome_from_goals`, `serialize_csv` and overwrite protection. Existing English audit wrappers fix different season/competition schemas, so their parsing logic was reviewed but not modified. The German CSV validator provides the precedent for source-specific, in-memory parsing with private diagnostics. No importer, converter, application or model was changed.

Checks cover exact CSV headers and row widths; required values; valid ISO dates within season bounds and no later than retrieval; nonnegative integral goals; home/away identities; historical CSV FT/goal/total/difference/result agreement; TXT date inheritance, weekdays, kickoff syntax and halftime bounds; team and match counts; every ordered home-away pair; repeated/conflicting fixtures; missing seasons; and per-team venue balance. The COVID-extended 2019/20 season explicitly permits dates through August 2020. Other seasons use July–June bounds. The TXT parser fails on unrecognized lines or unscored fixture syntax instead of dropping them, and determines an omitted year from the month rather than row order.

All raw fields and source order remain unchanged. The only saved tabular output is aggregate season diagnostics; source-specific match representations exist in memory only. Diagnostics include raw CSV line / TXT line references. Every parsed historical row in scope was retained, including awards. No correction, alias substitution, deduplication or eligibility filter was applied.

## Exceptional records and historical context

The following bounded checks locate one final fixture record per case in the original CSV. Detailed original fields, line numbers, review date and the source checksum are retained privately in `exception_review.json`. These references corroborate event context, with result checks where stated; this is not a complete historical exception inventory. No count deficit is inferred from the absence of discarded partial attempts.

| Season | Case | Finding and remaining limitation |
|---|---|---|
| 2003/04 | Lazio–Roma derby | Source dates the one final record to 21 April 2004. [UEFA](https://www.uefa.com/news-media/news/019c-0f845580e89b-01c78a9e50c9-1000--new-date-for-rome-derby/) confirms the abandoned 21 March game was scheduled to be replayed on 21 April. That announcement does not independently certify the final score. |
| 2007/08 | Atalanta–Milan | One final source record dated 23 January 2008; [UEFA’s contemporary report](https://www.uefa.com/news-media/news/01c9-0f84cbfdf466-c0574f58ba48-1000--atalanta-claim-milan-scalp/) agrees on the completed result. Original abandonment circumstances remain a further review item. |
| 2012/13 | Cagliari–Roma | Administrative award retained. [FIGC’s appeal ruling](https://www.figc.it/it/federazione/news/cgf-respinto-il-ricorso-del-cagliari-contro-lo-0-3-a-tavolino-con-la-roma-re8y5u7o) explicitly confirms the award for the 23 September 2012 fixture. It must not be treated as an observed on-field score without an explicit future policy. |
| 2020/21 | Juventus–Napoli | Source contains the played April fixture rather than an additional October award. [Juventus’ announcement](https://www.juventus.com/en/news/articles/official-juve-napoli-to-be-played-on-march-17-2021) confirms 7 April 2021 after the unplayed 4 October date; the [contemporary ANSA result report](https://www.ansa.it/sito/notizie/sport/calcio/2021/04/07/serie-a-juventus-napoli-2-1_71de7180-7d0f-4171-a3f2-6bffb6db86b3.html) agrees with the stored final score. Full appeal-order lineage remains for independent verification. |
| 2023/24 | Udinese–Roma | Source uses completion date 25 April 2024. [Udinese’s report](https://www.udinese.it/news/squad/udinese-1-2-roma) confirms the result and completion of the game stopped on 14 April. One fixture covers play on two dates. |
| 2024/25 | Fiorentina–Inter | Source uses completion date 6 February 2025. [Inter’s procedure notice](https://www.inter.it/en/news/rescheduled-continuation-fiorentina-inter-6-february-2025) confirms continuation from the interrupted 1 December 2024 fixture. The notice establishes resumption context, not the final score. |

[Calciopoli sanctions](https://www.uefa.com/news-media/news/01b7-0f8eee36c65e-730a3fda3edf-1000--fiorentina-and-lazio-reprieved/) affect 2004/05–2005/06 titles and subsequent penalties; title revocation is not evidence that every match result was annulled. No standings, points deductions or result rewrites are inferred. Other sanctions, annulments, neutral venues, administrative awards, abandonments and replay histories may remain undisclosed by these sources. Full fixture coverage cannot detect a wrong date/score or a plausible substitute record.

The source README describes other European league datasets as regular-season-only and excludes promotion/relegation playoffs. The audit confirms full regular double round robins with no extra fixtures. Historical Serie A relegation tie-breakers are outside the requested 306/380 totals; their omission is intentional, not a regular-season deficit. No exhaustive external stage inventory was acquired.

## Historical team-name variations

Raw names are preserved and checked separately within each season. `team_inventory.json` lists every observed spelling and per-team home/away totals by season. Counts and pairings reveal no within-season split-name anomaly. The historical source has 55 distinct spellings in scope; cross-source spelling changes are not silently merged. Examples include `Parma AC` (1990–2003 season starts) versus `Parma FC` (observed later), and `Salernitana Sport` (1998) versus `Salernitana Calcio 1919` (2021–2023). OpenFootball uses forms such as `Milan`, `FC Internazionale Milano`, `Juventus FC`, `Napoli`, `Lazio` and `Parma`, compared with historical `AC Milan`, `Inter`, `Juventus`, `SSC Napoli`, `Lazio Roma` and Parma forms. Names alone do not establish legal club continuity following refoundings. No alias map or standardized identifier was created.

## Provenance, checksums and reproduction

`acquisition.json` records each exact commit-pinned download URL, retrieval date, repository, byte size and SHA-256. `validation_provenance.json` embeds these entries and records selection rules, selected counts, restrictions, code fingerprint and output hashes. The initial acquisition records the client-local retrieval date (not an invented precise timestamp). The reusable downloader additionally records actual UTC timestamps on future retrievals. Snapshot versions are commit SHAs, not mutable branch names.

| Original file (relative to private Serie A directory) | SHA-256 |
|---|---|
| `jalapic/README.md` | `bda9e9fcebe0b2a6a401d756e0720c000b96ab14f362d854802fa576395a8158` |
| `jalapic/DESCRIPTION` | `ebddcf99f1c8c1abd1df9a47f79ee6b676a30b2feddad7a418f73a5f858b3b3f` |
| `jalapic/man/italy.Rd` | `cfed7f93fd7dbf433b9699d905238296c5c3ed6560b3665b1b9341676f52e37a` |
| `jalapic/data-raw/italy.csv` | `bd844da8e5e9196b4207d07afdb160e4c2d10a6d500af5dfb06d4688c476680b` |
| `openfootball/README.md` | `3ece15f94f366f190e0fca770a8499f3c9ae61c461cee9f233add72c57a62257` |
| `openfootball/LICENSE.md` | `36ffd9dc085d529a7e60e1276d73ae5a030b020313e6c5408593a6ae2af39673` |
| `openfootball/2025-26/1-seriea.txt` | `a746c3bb7c1c3a90fa54c50d52b7dd3b5ad5f5c440ebcadb044bbc8554c93a82` |
| `openfootball/2025-26/1-seriea-full.txt` | `c8cc7d5046863cdeae07848e410241de05195a55d70968889d2d4c385feeb2b0` |

| Private diagnostic / manifest | SHA-256 |
|---|---|
| `acquisition.json` | `05a40de2f99fe2ba5eab741177ff26ea98aaef3f5648d750b62e6c583abce892` |
| `season_validation.csv` | `a164ccd07dc7b50cd77cd1dcc7b11c39ad1d75632b949d2b080b3ff613c3f59d` |
| `validation_issues.json` | `37517e5f3dc66819f61f5a7bb8ace1921282415f10551d2defa5c3eb0985b570` |
| `team_inventory.json` | `282993c9e3658f2270650b7ad04d7c6fd664d67ef58eec2c2727fc8b9542c984` |
| `validation_provenance.json` | `bcee7be73192e36aa28f68f2361af251e8bd7b23e7c1398f5aa85fc15079c649` |
| `exception_review.json` | `e9f31188fabea0c1a7ac675daa35100292f48a410a79d1af384b658e11f04c7a` |

First acquisition in a fresh destination: `python3 -m scripts.collect_serie_a`. It refuses existing outputs before network access and downloads only the pinned files listed in code. First audit: `PYTHONPATH=src python3 -m scripts.validate_serie_a`. Audit reproducibility: `PYTHONPATH=src python3 -m scripts.validate_serie_a --check`, which verifies original hashes and compares regenerated diagnostics byte-for-byte without replacing files. Validation code fingerprints intentionally require the same code revision to reproduce the manifest. No force option is provided. The manually reviewed exception sidecar is separately checksum-bound in this report, not generated by the structural audit.

## Licensing and use limitations

[Curley’s saved README](https://github.com/jalapic/engsoccerdata/blob/872c5c354161ace8408f3091b758c6af4cccca94/README.md) permits noncommercial use and requests source credit; [DESCRIPTION](https://github.com/jalapic/engsoccerdata/blob/872c5c354161ace8408f3091b758c6af4cccca94/DESCRIPTION) declares GPL ≥2 for the package. Retain both notices and attribution: James P. Curley, engsoccerdata (README citation: 2016, R package 0.1.5; acquired package metadata: 0.1.8). The relationship between package licensing and the data-use restriction is unresolved; this private academic collection does not establish blanket commercial, redistribution, hosting or model-use rights. The README lists mixed upstream providers, including RSSSF, Wikipedia, ESPN, Statto, 11v11, WorldFootball and Football-Data, without row-level provenance. No explicit clearance of all upstream rights was found.

[OpenFootball’s saved licence](https://github.com/openfootball/italy/blob/48954d163c312aa705efacb64f771267031fe6eb/LICENSE.md) is CC0 1.0. Its waiver applies to rights held by the affirmer, disclaims accuracy/title warranties, and does not clear other parties’ rights. Repository descriptions of public-domain data do not independently prove every upstream right or match fact. No source was accessed by bypassing an access restriction. No private match data is published, committed or pushed.

## Tests and readiness

**26 targeted tests pass; all 481 repository tests pass (14.06 seconds).** Tests use synthetic fixtures only and cover both format boundaries, complete schedules, equal-count missing/duplicate substitution, conflicting scores, missing seasons, invalid dates/goals/names, COVID bounds, unexpected season rejection, raw name variation preservation, explicit/inherited/reordered TXT dates, multiline scorer annotations, unknown/unscored-line rejection, weekday/halftime inconsistencies, CSV schema/width and score consistency, original-byte preservation, checksum tampering, pinned download scope and refusal before network access.

The repository virtual environment stalled during imports. Tests therefore ran with Python 3.13 in `/tmp/toto-serie-a-test`, using installed system pandas 3.0.2 / numpy 2.4.4 plus temporary pytest 9.2.0 and Streamlit 1.67.0 (within declared dependency ranges). The first full run stopped at collection because Streamlit was absent; installing that declared dependency in the temporary environment resolved it. No dependency file or existing virtual environment was changed. Command: `PYTHONPATH=src /tmp/toto-serie-a-test/bin/python -m pytest -q`. The offline `--check` also passes, reproducing all structural diagnostics and provenance byte-for-byte.

Git confirms private Serie A artifacts are ignored. Tracked changes are limited to the append-only planning log; the new collection/audit scripts, synthetic tests and this report are untracked pending user review. Existing English/German data and application/specification files were not written by this work. Unrelated pre-existing `.DS_Store` files remain untouched. No commit or push was performed.

**Ready for independent result verification: yes.** All requested season records are acquired, hash-bound, structurally complete and traceable to originals. Independent verification should prioritize administrative outcomes, multi-date/replayed fixtures, historical club identity, playoff scope and a season-stratified result sample. There is no observed structural discrepancy requiring a source correction. This audit does not certify every result, exhaustive exception status, training eligibility or downstream legal clearance. No standardization, integration, prediction/interface work, training or evaluation was performed.

## Independent result verification and exceptional-fixture review — 2026-11-12

**Review outcome: 30 unique external fixture comparisons, 11 confirmed source-date discrepancies and no compared score or club-orientation discrepancy.** The main 20-match sample has exactly five matches from each calendar decade, 1990s–2020s; it yields 19 complete agreements and one date discrepancy. Ten targeted follow-ups establish ten additional date discrepancies. Seven exceptional fixtures are now documented: the original six plus the newly found Milan–Genoa replay. **No original or prior acquisition artifact was changed; all 11 proposed date corrections remain unapplied.** This section supersedes earlier readiness conclusions and the incomplete acquisition-stage exception interpretations.

### Selection, comparisons and evidence strength

The selection is purposive and driven by accessible evidence, era coverage, known exceptions and the source handover; it is not a random or statistically representative sample. The 1990s sample particularly overrepresents Milan/Fiorentina. Detailed source values, exact raw line numbers, original-row fields, manually transcribed external observations, case-specific name mappings and comparison results remain private in `verification/independent_verification.json` and `supplementary_verification.json`. No match dataset is exported into this report. The table below is a public reference index to the independently published records, not a source-data extract.

For each main sample, the comparison covers date, home/away orientation, final score, Serie A regular-season classification and spelling/identity. The outcome column refers to all those fields after explicit, fixture-specific name lookup; it does not normalize stored names. The COVID-extended August 2020 fixture counts in the **2020s by actual calendar date**, although its source season is 2019/20.

| Sample | Calendar decade | Public reference | Evidence read | Comparison |
|---|---|---|---|---|
| SA-01 | 1990s | [1991-09-22: Milan–Fiorentina](https://www.magliarossonera.it/statistiche/dynamicInfoMatch.php?match=2896) | full match page | Date discrepancy; other fields agree |
| SA-02 | 1990s | [1992-10-04: Fiorentina–Milan](https://www.magliarossonera.it/statistiche/dynamicInfoMatch.php?match=2941) | full match page | All requested fields agree |
| SA-03 | 1990s | [1995-06-04: Fiorentina–Milan](https://www.acmilan.com/it/news/articoli/storia/2026-01-09/time-machine-fiorentina-milan) | full report | All requested fields agree |
| SA-04 | 1990s | [1998-05-16: Fiorentina–Milan](https://www.magliarossonera.it/statistiche/dynamicInfoMatch.php?match=3229) | full match page | All requested fields agree |
| SA-05 | 1990s | [1999-05-23: Perugia–Milan](https://www.magliarossonera.it/statistiche/dynamicInfoMatch.php?match=3267) | full match page | All requested fields agree |
| SA-06 | 2000s | [2001-06-17: AS Roma–Parma](https://www.11v11.com/matches/as-roma-v-parma-17-june-2001-7356/) | full match page | All requested fields agree |
| SA-07 | 2000s | [2002-05-05: Lazio–Inter](https://www.soccerbase.com/matches/results.sd?date=2002-05-05) | full results page | All requested fields agree |
| SA-08 | 2000s | [2006-04-14: AC Milan–Inter](https://www.inter.it/en/match_center/3575) | full match page | All requested fields agree |
| SA-09 | 2000s | [2008-01-23: Atalanta BC–AC Milan](https://www.uefa.com/news-media/news/01c9-0f84cbfdf466-c0574f58ba48-1000--atalanta-claim-milan-scalp/) | full report | All requested fields agree |
| SA-10 | 2000s | [2009-08-29: Milan–Inter](https://www.inter.it/it/match_center/3777) | full match page | All requested fields agree |
| SA-11 | 2010s | [2010-05-16: Siena–Inter](https://www.inter.it/it/match_center/3833) | full match page | All requested fields agree |
| SA-12 | 2010s | [2011-04-02: AC Milan–Inter](https://www.inter.it/en/match_center/3885) | full match page | All requested fields agree |
| SA-13 | 2010s | [2012-10-20: Juventus–Napoli](https://www.juventus.com/en/news/articles/when-juve-napoli-is-1st-vs-2nd) | full report | All requested fields agree |
| SA-14 | 2010s | [2014-05-04: AC Milan–Inter](https://www.inter.it/en/match_center/4040) | full match page | All requested fields agree |
| SA-15 | 2010s | [2017-12-01: Napoli–Juventus](https://sport.sky.it/calcio/serie-a/2017/12/01/napoli-juventus-risultato-gol) | full report | All requested fields agree |
| SA-16 | 2020s | [2020-08-01: Juventus–Roma](https://www.asroma.com/en/news/58314/juventus-1-3-roma-perotti-double-secures-final-day-win) | full report | All requested fields agree |
| SA-17 | 2020s | [2021-04-07: Juventus–Napoli](https://www.juventus.com/en/news/articles/ronaldo-dybala-earn-napoli-win) | full report | All requested fields agree |
| SA-18 | 2020s | [2024-04-25: Udinese–Roma](https://www.udinese.it/news/squad/udinese-1-2-roma) | full report | All requested fields agree |
| SA-19 | 2020s | [2025-02-06: Fiorentina–Inter](https://www.inter.it/en/news/continuation-fiorentina-inter-serie-a-24-25) | full report | All requested fields agree |
| SA-20 | 2020s | [2025-08-23: Sassuolo–Napoli](https://www.sassuolocalcio.it/en/fotogallery/serie-a-enilive-sassuolo-napoli-0-2-2/) | full report | All requested fields agree |

All 20 main comparisons have readable page evidence: **10 individual match pages, nine reports/retrospectives and one dated results page**. That is not a claim of 20 dedicated match sheets. The combined 30 comparisons comprise **12 individual match pages, nine reports/retrospectives and nine dated-results-table comparisons**. The eight additional round-four comparisons use one readable table, so they are eight fixtures, not eight independently collected publications. Combined calendar quotas are 14 / 6 / 5 / 5. Indexed-only sources do not count towards these full-page quotas.

The sample’s official club match centres and reports are preferred over generic archives. The [official Sassuolo report](https://www.sassuolocalcio.it/en/fotogallery/serie-a-enilive-sassuolo-napoli-0-2-2/) directly confirms the OpenFootball-era fixture. A [Lega match-report PDF](https://img.legaseriea.it/vimages/68aa132f/2025-26_A_UNICO_UNI_1_SASNAP_ENG.pdf) was visible in indexed text but failed direct retrieval with HTTP 502; it is only supplemental indexed evidence. The Lega portal was readable but did not establish target-era full historical match records. A search result linking the reverse Napoli–Sassuolo fixture was rejected as evidence for the August home/away orientation.

For SA-06, the readable 11v11 match page is corroborated by [Roma’s official retrospective](https://www.asroma.com/it/notizie/73433/17-giugno-2001-cosa-accadde-in-campo-e-fuori-per-la-festa-scudetto-attesa-18-anni). For SA-17, [Juventus’ reactions report](https://www.juventus.com/en/news/articles/bianconeri-react-to-victory-over-napoli) explicitly confirms the rescheduled Serie A Week 3 classification. For SA-18, [Roma’s Lega continuation notice](https://www.asroma.com/it/notizie/71011/la-lega-serie-a-su-udinese-roma-il-match-proseguira-il-25-aprile-alle-20) supplies the league/matchday context for Udinese’s final report. Dates in retrospectives and publication/update times are not substituted for match dates.

**Publication independence is limited.** 11v11 and RSSSF are explicitly named upstream by engsoccerdata. Agreement with either is useful external corroboration, not proof of independent data generation. Maglia Rossonera, Soccerbase and WLecce are separate specialist publications, but shared archives/feeds and undocumented copying cannot be excluded. Official club and UEFA reports improve authority and add event narratives; their statistics can still share league or agency suppliers. This review does not independently certify every original result or establish 30 independent data-generation chains.

### Confirmed discrepancies and guarded proposals

The first date error prompted a complete same-team/same-date collision scan of the 12,644 selected records. It found **19 team/date collision groups**: all 18 clubs in the September 1991 duplicate-date round, plus Lecce in September 2001. A collision is a candidate flag, not independent truth; the affected fixture dates were then checked against external records. The readable Milan unbeaten-run chronology also exposed a replay-date mismatch that has no same-day collision.

| Confirmed issue | Affected source rows | Proposed future change | Evidence and assurance |
|---|---|---|---|
| Entire 1991/92 round four carries the previous round’s date | Historical CSV physical lines **16895–16903**, nine distinct fixtures | `Date`: **1991-09-15 → 1991-09-22**, individually guarded | [Soccerbase’s readable 22 September results table](https://www.soccerbase.com/matches/results.sd?date=1991-09-22) explicitly identifies all nine Serie A pairings and scores. The Milan–Fiorentina case also has readable [Maglia](https://www.magliarossonera.it/statistiche/dynamicInfoMatch.php?match=2896), [TuttoFotoSport](https://www.tuttofotosport.it/2022/09/26/serie-a-milan-fiorentina-1991-1992-1-1/) and [Viola Vintage](https://www.violavintagefun.it/it/stagione-fiorentina-1991-92.php) support. The other eight rely primarily on the table, with indexed club-round corroboration; separate primary match sheets were not obtained. |
| Milan–Genoa 1991/92 has the replay result against the abandoned attempt’s date | One source-bound fixture, SA-29 / SA-E7 | `Date`: **1991-09-29 → 1991-11-20** | Readable [Maglia replay record](https://www.magliarossonera.it/statistiche/dynamicInfoMatch.php?match=2903) and [RSSSF chronology](https://rsssf.org/miscellaneous/unb-milan-58.html) agree on the completed replay date/result. RSSSF has declared upstream lineage. [Mediaset’s retrospective](https://www.sportmediaset.mediaset.it/calcio/seriea/serie-a-rinviata-milan-genoa-ancora-_15527063-202002a.shtml) confirms the original rain suspension. Some archives repeat the scheduled date; agreement with them alone would miss the error. |
| Brescia–Lecce 2001/02 is dated to Lecce’s next fixture day | Historical CSV physical line **19954**, SA-30 | `Date`: **2001-09-22 → 2001-09-16** | [WLecce’s readable full match record](https://www.wlecce.it/page.php?action=partita&id_partita=274&pg=archivio) gives 16 September, round three, orientation and final score. [Gazzetta’s Baggio chronology](https://www.gazzetta.it/Calcio/Squadra/Brescia/Primo%20Piano/2004/02-febbraio/pop%20Baggio199.shtml) corroborates date/score in indexed text only; direct access returned 403. |

All **11 proposals change `Date` only**. Compared final scores and team labels agree with the references and are retained. `verified_corrections.json` contains a unique correction ID, immutable source SHA-256, physical row, every original field, exact replacement, evidence URLs/access levels, `VERIFIED_PENDING_STANDARDIZATION` and `applied: false` for each fixture. The guard permits no score/name change, no wholesale season offset, no added/dropped fixture and no silent rewrite. None of the proposals changes the original 36-season / 12,644-row count.

An in-memory simulation of just these proposals resolves all 19 observed collision groups without changing pairings, scores or counts. It is not a corrected dataset or a standardization stage. Other wrong dates can exist without causing a collision; the scan and this sample do not exhaustively verify all dates. Broader date checks are advisable, especially within the two affected seasons.

| Season group | Original structural audit | Current documentary review |
|---|---|---|
| 1991/92 | PASS; 306 fixture slots | **REVIEW: 10 date proposals** (nine round-four fixtures plus one replay) |
| 2001/02 | PASS; 306 fixture slots | **REVIEW: one date proposal** |
| Remaining 34 seasons | PASS; expected counts retained | No confirmed date/score discrepancy in the bounded checks; not independently certified in full |

### Exceptional fixtures: final results, event history and training policy

The policy follows the existing [Bundesliga archive/training distinction](bundesliga-validation.md#archive-and-future-training-policy) and [second-tier exception policy](second-bundesliga-validation.md#exception-policy-and-decisions): preserve recognized final archive outcomes, distinguish partial on-field events from awards, keep exception metadata outside match rows, and leave unlisted eligibility unresolved. Completed replays are conservatively excluded by that existing policy. A first actual playing after a cancelled award is assessed separately; medical resumptions are not automatically declared unsuitable.

| Case | Scheduled / original event | Actual playing or completion | Recognized final result | Classification and ordinary 90-minute training recommendation |
|---|---|---|---|---|
| **SA-E1 Lazio–Roma, 2003/04** | 21 March 2004; stopped shortly after half-time amid crowd disturbances. Provisional 0–0 / minute 47 is indexed-only support. | Completed replay 21 April 2004; 14 April was an intermediate planned date, not the actual replay. | **1–1**, on-field replay result | **EXCLUDED conservatively** as a completed replay under the existing policy. The partial 0–0 is not a valid full-time draw. |
| **SA-E2 Atalanta–Milan, 2007/08** | 11 November 2007; formally interrupted after seven minutes, described in the quoted decision as effectively not played. No securely established provisional score is asserted. | Repeated fixture 23 January 2008, behind closed doors. | **2–1**, on-field result | **EXCLUDED conservatively** as a completed replay. A proposed 0–3 award to Milan was explicitly rejected, not the official final outcome. |
| **SA-E3 Cagliari–Roma, 2012/13** | 23 September 2012, prevented by a public-safety postponement following the club’s invitation to fans despite a closed-door order. | **Unplayed; no playing/replay date and no on-field score.** The source date is the scheduled fixture date. | **0–3 administrative award**, imposed 24 September; appeal rejected 20 November. | **EXCLUDED:** an award is not an observed on-field 90-minute target. Preserve the official archive outcome without inventing a played result. |
| **SA-E4 Juventus–Napoli, 2020/21** | Scheduled 4 October 2020; no game played. The initial sporting loss and point deduction were overturned by CONI on 22 December 2020. | **First actual playing 7 April 2021**, completed normally; an intermediate 17 March plan was superseded. | **2–1**, on-field result; October’s temporary award is not a second match. | **ELIGIBLE in match-status terms** under a future ordinary 90-minute policy: completed first playing, not a replay of an earlier played game. This is not training authorization or rights clearance. |
| **SA-E5 Udinese–Roma, 2023/24** | 14 April 2024, interrupted for Ndicka’s medical emergency at 1–1. | Remaining play completed 25 April; Lega notice relayed by Roma specifies 26:30 of second half (71:30 elapsed). | **1–2**, combined on-field final | **UNRESOLVED:** completed cumulatively, not an award or full replay. Existing policy does not certify games split across dates; an explicit resumption/feature-date policy is needed. No automatic medical-event exclusion. |
| **SA-E6 Fiorentina–Inter, 2024/25** | 1 December 2024, interrupted at 0–0 for Bove’s medical emergency. | Continued 6 February 2025 from the stopped game state, with player-availability constraints. | **3–0**, combined on-field final, **not** an administrative award | **UNRESOLVED:** completed cumulatively; long gap and changed available lineups require explicit modelling policy rather than an automatic exclusion or eligibility assumption. |
| **SA-E7 Milan–Genoa, 1991/92 — newly identified** | 29 September 1991 rain suspension. Provisional 1–0 / minute 49 is indexed-only support, not a completed final. | Completed replay 20 November 1991. | **1–1**, on-field replay result | **EXCLUDED conservatively** as a completed replay. Linked date-only proposal required for a future derivative; final score already agrees. |

**Evidence by case:**

- **E1:** [UEFA’s revised replay announcement](https://www.uefa.com/news-media/news/019c-0f845580e89b-01c78a9e50c9-1000--new-date-for-rome-derby/) confirms original/replay scheduling and abandonment; its [contemporary final report](https://www.uefa.com/news-media/news/019c-0f8edf6e4d3e-a3d6714a1dc3-1000--roma-relinquish-title-hopes/) establishes the completed draw and Serie A context. These were fully readable. Nominal Lazio home orientation and the abandoned partial score additionally have indexed archive support; the [Soccer-Europe fixture report](https://soccer-europe.com/Archives/Seriea/Seriea0304/Reports/Round26.html) returned a cache miss, and FootballDerbies timed out. A primary abandonment/replay tribunal order was not obtained.
- **E2:** [Gazzetta’s original report](https://www.gazzetta.it/Calcio/SerieA/Squadre/Atalanta/Primo_Piano/2007/11_Novembre/11/AtaMilan.shtml), [Mediaset’s contemporary quotation of the sporting judge](https://www.tgcom24.mediaset.it/sport/articoli/388645/calcio-si-rigioca-atalanta-milan.shtml) and [UEFA’s completed-match report](https://www.uefa.com/news-media/news/01c9-0f84cbfdf466-c0574f58ba48-1000--atalanta-claim-milan-scalp/) were readable. Mediaset quotes a repetition order and no award; that is authoritative contemporary reporting of a decision, not the primary decision file. RTÉ’s matching report was indexed-only after a direct 403 and is not counted as full-page evidence.
- **E3:** [FIGC’s appeal notice](https://www.figc.it/it/federazione/news/cgf-respinto-il-ricorso-del-cagliari-contro-lo-0-3-a-tavolino-con-la-roma-re8y5u7o) was fully readable and confirms the recognized award. The [original Lega C.U. 51](https://img.legaseriea.it/vimages/16fdc36c555d909d/cu_51.pdf) supplies the initial decision’s date and stated public-safety/club-conduct basis in indexed text only; no full PDF inspection is claimed.
- **E4:** [CONI’s official reasons summary](https://www.coni.it/it/news-attivita-istituzionali/collegio-di-garanzia/le-motivazioni-della-sentenza-afferente-al-ricorso-della-s-s-c-napoli-s-p-a-contro-figc,-juventus-f-c-s-p-a-e-lnp-serie-a.html) was readable and explains the appeal, original date and public-health-order hierarchy. The [superseded FIGC decision](https://www.figc.it/media/127771/sez-i-decisione-n-014-csa-del-10-novembre-2020.pdf) is indexed-only support for the initial 0–3 loss imposed on Napoli. [Juventus’ scheduling notice](https://www.juventus.com/en/news/articles/official-juve-napoli-to-be-played-on-march-17-2021), [final report](https://www.juventus.com/en/news/articles/ronaldo-dybala-earn-napoli-win) and [explicit Serie A reaction report](https://www.juventus.com/en/news/articles/bianconeri-react-to-victory-over-napoli) corroborate the actual first playing and final outcome. It is not treated as the same policy class as a replay after on-field abandonment.
- **E5:** [Roma’s interruption report](https://www.asroma.com/en/news/70951/udinese-1-1-roma-match-suspended-in-the-71st-minute), [Lega continuation notice relayed by Roma](https://www.asroma.com/it/notizie/71011/la-lega-serie-a-su-udinese-roma-il-match-proseguira-il-25-aprile-alle-20) and [Udinese’s final report](https://www.udinese.it/news/squad/udinese-1-2-roma) were readable. The colloquial 71st/72nd-minute descriptions should not overwrite the explicit continuation clock. Completion date and original playing date are retained separately in review metadata.
- **E6:** [Inter’s continuation procedure](https://www.inter.it/en/news/rescheduled-continuation-fiorentina-inter-6-february-2025) and [post-match report](https://www.inter.it/en/news/continuation-fiorentina-inter-serie-a-24-25) were readable. They establish the original score/state, the actual continuation and completed result. The procedure itself alternates “16th” and “17th” minute, while post-match prose mentions a later formal suspension; no unique precise second is invented. Player eligibility was tied to registration at the original interruption, so December and February teams need not be identical.
- **E7:** the readable replay record, RSSSF chronology and Mediaset rain-suspension account are linked in the correction table. The original partial score/minute comes from [indexed Transfermarkt notes](https://www.transfermarkt.it/milan-ac_genoa-1893/index/spielbericht/2216397), not a fully read tribunal or contemporary match sheet; it is explicitly provisional. The recognized replay date/result has readable archive corroboration.

No additional score award or annulment is inferred from a title or standings sanction. Calciopoli remains a separate season/standings context, not a reason to rewrite every 2004/05 or 2005/06 result or automatically exclude all such fixtures. All seven case decisions are source-row/checksum bound in `exception_policy.json`; exactly four are EXCLUDED, one ELIGIBLE and two UNRESOLVED. All unlisted fixtures remain UNRESOLVED, even when they occur in the verified sample. No eligibility filter was implemented.

### Names and club identities needing manual review

The private comparisons explicitly map display names within the individual fixture: Milan ↔ AC Milan; Fiorentina ↔ source ACF Fiorentina; Perugia ↔ AC Perugia; Parma ↔ Parma AC for the 2001 fixture; Lazio ↔ Lazio Roma; Atalanta BC ↔ Atalanta; Siena ↔ AC Siena; Napoli ↔ SSC Napoli; Roma ↔ AS Roma; Udinese ↔ Udinese Calcio. These lookups explain the sample agreements without changing a source name. They are not a global identity map.

Cross-season legal/sporting identity still needs manual review around **Fiorentina’s 2002 refounding, Parma’s 2004/2015 changes and Salernitana’s refoundings**, with similar caution for Venezia and other resurrected clubs. In particular, source `Parma FC` continues in post-2015 seasons; [FIGC’s fully readable admission notice](https://www.figc.it/it/federazione/news/la-ssd-parma-calcio-1913-srl-ammessa-in-soprannumero-in-serie-d-tn388khc) explicitly distinguishes newly admitted S.S.D. Parma Calcio 1913 from the former Parma F.C. after revocation of affiliation. A familiar modern source label is therefore not proof of a continuous legal entity. The source’s `ACF Fiorentina` in early-1990s records likewise identifies the sporting side retrospectively, not necessarily its then-current legal name. Exact incorporation/name-change records for every club were not acquired, and no comprehensive identity system, alias substitution or name correction was implemented.

### Preservation, automation and reproducibility

Before review, SHA-256 fingerprints were frozen for **301 pre-existing private files: 287 England/Germany files and 14 Serie A acquisition files**. The read-only review checker verifies every fingerprint, source file hash, physical row/full-field binding, original TXT line, main-sample selection, external-observation consistency, explicit aliases, calendar-decade quotas, all 11 date-only correction guards and all seven exception decisions. It reruns the unchanged acquisition audit and compares every prior diagnostic/provenance output byte-for-byte. All **36 seasons and 12,644 original selected records remain unchanged**.

`scripts/verify_serie_a_review.py` reuses the existing Serie A parsers/build and performs no network access or writes. Its same-team/date scan is an additional review check; the earlier structural audit and its immutable PASS snapshot were not rewritten. The checker validates the consistency and preservation of manually recorded evidence, not external historical truth. Notes are paraphrased observations rather than downloaded full copyrighted articles; the review hashes bind those notes and source rows, not immutable remote-page snapshots.

New ignored review artifacts:

| File under `data/private/italy/serie_a/verification/` | Purpose | SHA-256 |
|---|---|---|
| `protected_before.json` | 301 immutable pre-review fingerprints | `52aff129015de3fa5f988fdfb34a5e875f7a107d21f356d6ee539b41bb2b3b29` |
| `sample_selection.json` | Main 20 exact source selections | `f02f5f4c1149a617245e362997ea466639970f3cf5361bf7bf619392e4748ab9` |
| `independent_verification.json` | Main 20 external comparisons and explicit aliases | `b099f947b354aeefc62b8b1318dbbfb2b1ed92bee77a0dcb10a13fe00cfe8d1e` |
| `supplementary_verification.json` | Ten targeted additional comparisons | `623462dea46defe756e9ae4c6f96cc0863507f92817e4464d9e7d3abd5e480d8` |
| `verified_corrections.json` | 11 unapplied, guarded date-only proposals | `a7faa2a68cb31e61109c49abb1d86fe66db8ad52a0678fc1261d2b4626622ec2` |
| `exception_policy.json` | Seven cases and status-specific eligibility decisions | `9b4a4ea3a70569da7cdbb1cc544afc1c6abb93446572c306d00e72ecfb6dd181` |
| `access_and_lineage.json` | Access failures, indexed-only evidence and provenance limits | `f94863c4a9d139ae3f8052514f8390054069788e2de2d67380c11880f30f9119` |
| `review_result.json` | Read-only check results | `6709752b76fa8562ea08894ce305873f7153df1ab5f579207ef9f181f6e32b37` |
| `review_manifest.json` | Review artifact hashes and checker/test fingerprints | `afaea816a68558bd6e91a931f67777ee6367cb96c7ca15316bb20dd026b8a10a` |

**Tests: 507 repository tests pass (9.35 seconds), including 26 new review tests and the 26 existing Serie A structural tests.** New synthetic tests cover calendar rather than season-start quotas; snippets versus full-page evidence; duplicated selections/bindings; date/score discrepancy disclosure; competition/stage and explicit identity/orientation; exact raw CSV bindings/checksums/path bounds; read-only date corrections and refusal of score changes, applied corrections or unsupported proposals; policy distinctions between replays, unplayed awards, first play after overturned award and unresolved resumptions; and same-team/date collision detection. No private match records are in tests.

Checks completed:

```sh
PYTHONPATH=src python3 -m scripts.validate_serie_a --check
PYTHONPATH=src python3 -m scripts.verify_serie_a_review
PYTHONPATH=src /tmp/toto-serie-a-test/bin/python -m pytest -q
git diff --check
```

Tests use the same temporary dependency environment described above; project dependency files and the existing virtual environment were not changed. Git confirms the new review artifacts are ignored and untracked. Existing English/German data, all Serie A originals and prior manifests, prediction/interface code, README and Homework 8 OpenSpec files remain unchanged. No standardization, integration, training, evaluation, public match-data export, commit or push occurred.

### Updated readiness and limitations

**Ready to prepare a separately authorized standardization stage with the 11 guarded date-only corrections and separate seven-case metadata; not ready to standardize the raw dates unchanged.** The two affected source seasons remain documentary REVIEW until the proposed changes are applied only to a future derivative. That future stage must preserve originals and the scheduled/partial/replay history, link correction/exception records to derived identities, and retain unresolved training eligibility for both resumptions and unlisted fixtures.

This is bounded external agreement and targeted exception review, not exhaustive independent certification or a training decision for the whole dataset. Some exception event details and original tribunal documents remain unavailable; provisional stopped-game scores supported only by indexed text remain explicitly qualified. Team legal continuity requires further review. Source licensing ambiguities and upstream-rights limitations in the acquisition section remain unresolved; sample verification confers no new rights for model use or publication.

## Standardized TOTOdology dataset — 2026-11-12

**Outcome: PASS. Standardized all 12,644 records across 36 completed seasons (1990/91–2025/26), applied all 11 verified date corrections only to the derivative, and linked all seven reviewed exceptions to output match IDs.** The earlier acquisition/review sections and their source findings remain immutable historical snapshots. Their statements that correction/standardization was pending describe those earlier stages; this section records the newly authorized conversion. All raw files, prior evidence and manifests remain unchanged.

### Shared conversion and exact output schema

`scripts/standardize_serie_a_results.py` reuses the original Serie A parsers and reviewed evidence checker, then calls the established `scripts.standardize_england_results.convert_rows` with explicit Tier 1, source-division mapping and league **`Serie A`** for every season. It follows the Bundesliga adapters’ guarded-correction and separate-sidecar pattern. The shared converter delegates to `import_historical_csvs` and `load_historical_data` / `validate_historical_data`; no existing importer, validator or German/English adapter was changed. Serie A’s ordinary double round-robin schedules need no phase-specific batching.

Saved columns, in exact order:

```text
match_id,date,league,season,home_team,away_team,home_goals,away_goals
```

Dates are ISO `YYYY-MM-DD`; seasons are canonical **`YYYY/YYYY`**. The historical starting-year field is expanded into that syntax, and the 2025/26 text retains its explicit season. All source team spellings and goal values are retained, including different naming vocabularies across the source handover. Source annotations and redundant score/result fields are audited before omission; no club aliases are applied. The temporary supported-schema CSV bridge stays inside private storage and is removed on success or failure.

Match IDs use the existing importer’s full **SHA-256** of compact UTF-8 JSON `[league, season, ISO date, home_team, away_team]`, `ensure_ascii=False`, separators `(",", ":")`. Scores, source paths and input order do not affect identity. Corrected dates enter the ID, so the affected fixtures receive IDs for their verified derivative dates. Fixture membership and home/away identities are preserved; no source record is deleted, merged or replaced. IDs are verified independently against all 12,644 saved rows.

### Private outputs and checksums

All three new outputs are exclusively under Git-ignored `data/private/italy/serie_a/`:

| File | Contents | SHA-256 |
|---|---|---|
| `serie_a_standardized_1990_2025.csv` | 12,644 matches / 36 completed seasons; exact eight columns | `9596da3b2f5ea7e2d4edcf7f37fa37706e8171bc82a226a4a0460e7ac296dc32` |
| `serie_a_exceptions_1990_2025.json` | Seven unique match-ID-linked cases; classifications, dates, on-field/official distinctions, evidence and eligibility retained | `626df408f89044f0010ae6cb69910ed341bf1038fc5ec75148a7644c6c325693` |
| `serie_a_standardization_manifest.json` | Source provenance and input/code hashes; season validation; import summary; applied corrections; 12,644 source-row → match-ID links; output hashes and rights limits | `28e606667c185ee281d9f155564ba47fbaa42f9b8998c7dc222156016f69fe27` |

`standardization_protected_before.json` records **310 pre-standardization file fingerprints**, comprising all prior English/German artifacts and all Serie A originals and review files. Its SHA-256 is `9b719a888ca867c57d14e921e23777aae2ba4ac5bd4d6acbc13a4b8f760d1a2f`. All 310 fingerprints match after conversion and regeneration. This is an additional preservation snapshot, not a replacement for the earlier acquisition or review manifests.

The standardization manifest retains commit-pinned source URLs, source retrieval dates, original byte sizes and checksums, reviewed evidence seal, all actual conversion input hashes, code fingerprints, the original compiler attribution and the unresolved restrictions. Only actual frozen inputs are listed: adding a future unrelated private artifact does not silently make it a conversion input. The manifest itself is checksummed in this report rather than attempting to include its own checksum.

### Applied corrections and preservation of facts

Exactly **11** verified corrections were applied once each to derived dates:

| Group | Number | Original → standardized date |
|---|---:|---|
| September 1991 round-four fixtures | 9 | `1991-09-15` → `1991-09-22` |
| Milan–Genoa completed replay | 1 | `1991-09-29` → `1991-11-20` |
| Brescia–Lecce 2001/02 | 1 | `2001-09-22` → `2001-09-16` |

The converter pins the previously reviewed evidence seal and rechecks every correction’s source file SHA-256, physical row, every original field, parsed facts, season, exact replacement, evidence access level and verified/unapplied review status. Duplicate correction IDs/bindings, absent source rows, repeat application and changes to scores or teams are rejected. The source pending records remain `applied: false`; new copies in the standardization manifest explicitly say `applied: true`, identify the derived output and link the resulting match ID. No original or earlier review artifact was edited to mark a correction applied.

Source-location and multiset comparisons prove preservation of every season, club orientation and final score and of every date outside those 11 replacements. All 12,644 original fixture slots survive exactly once, including awards, completed replays and unresolved resumptions. The corrected derivative has no same-team/same-date collisions and retains complete ordered-pair coverage in every season. The earlier 1991/92 and 2001/02 documentary REVIEW findings are resolved for this derivative by the guarded corrections; the raw-source dates intentionally remain unchanged and their earlier findings are not erased.

### Seven linked exception classifications

All original case fields—including source SHA/row/raw fields, classifications, scheduled and actual dates, partial versus completed on-field events, recognized finals, evidence access levels and reasoning—are preserved in the sidecar. Each entry adds the exact derived `match_id`, standard fixture identity and archived date/goals. The Milan–Genoa case also carries its applied derivative-only correction.

| Case | Classification | Training suitability preserved |
|---|---|---|
| SA-E1: Lazio–Roma 2003/04 | `COMPLETED_REPLAY_AFTER_ABANDONMENT` | **EXCLUDED** |
| SA-E2: Atalanta–Milan 2007/08 | `COMPLETED_REPLAY_AFTER_ABANDONMENT` | **EXCLUDED** |
| SA-E3: Cagliari–Roma 2012/13 | `UNPLAYED_ADMINISTRATIVE_AWARD` | **EXCLUDED** |
| SA-E4: Juventus–Napoli 2020/21 | `FIRST_PLAYED_AFTER_OVERTURNED_AWARD` | **ELIGIBLE** |
| SA-E5: Udinese–Roma 2023/24 | `INTERRUPTED_THEN_RESUMED_AND_COMPLETED` | **UNRESOLVED** |
| SA-E6: Fiorentina–Inter 2024/25 | `INTERRUPTED_THEN_RESUMED_AND_COMPLETED` | **UNRESOLVED** |
| SA-E7: Milan–Genoa 1991/92 | `COMPLETED_REPLAY_AFTER_ABANDONMENT` | **EXCLUDED** |

The four conservative exclusions consist of three completed replays and the unplayed administrative award. Juventus–Napoli remains the single eligible **first actual playing** in match-status terms; no temporary overturned award is added as another match. Udinese–Roma and Fiorentina–Inter remain **UNRESOLVED**, with `ordinary_90_minute_training_eligible: null` and `HOLD_OUT_PENDING_REVIEW`. They are not relabelled confirmed eligible or converted into administrative awards. Their recognized cumulative final results were already documented; standardization adds no certainty to their unresolved training suitability or provisional event details.

All **unlisted** matches have default training suitability **`UNRESOLVED`** and conservative action **`HOLD_OUT_PENDING_REVIEW`**. Absence from the seven-case register does not certify a normal finished match. These are separate metadata recommendations, not a training selection implementation; no record was filtered and no model was run. The sidecar retains the evidence-based reasoning and the distinction between archive final results and ordinary 90-minute targets.

### Validation and reproducibility

- Exactly **12,644 records** and **36 completed seasons**, ending at 2025/26. No 2026/27 data were acquired or included.
- Exactly eight columns, no missing required values, league `Serie A`, canonical seasons and valid dates/nonnegative integer goals.
- **12,644 unique deterministic IDs**; no duplicate dated match identity or season home-away pairing.
- All 14 seasons through 2003/04 have 18 teams and 306 matches; the following 22 have 20 teams and 380 matches. Every ordered home/away pairing appears once, with n−1 home and n−1 away fixtures per team.
- All 11 correction guards pass and apply exactly once. No unintended score, team, orientation, season or fixture membership change. An additional direct comparison against the raw historical CSV confirms exact multiset equality after only the 11 date replacements.
- The shared importer accepts all 12,644 rows with **zero rejected records, duplicates, unscored fixtures or conflicts**. Saved CSV facts survive the existing public historical loader/validator unchanged.
- Seven distinct sidecar match IDs refer to actual CSV rows and their archived dates/results. All seven prior case records remain intact; classification/eligibility counts are exactly four EXCLUDED, one ELIGIBLE and two UNRESOLVED.
- Reversing the parsed input produces identical CSV bytes and IDs. A fresh `--check` rebuild reproduces **all three saved outputs byte-for-byte**, including exception metadata and provenance. Code fingerprints intentionally require the recorded converter revision for manifest reproduction.
- All **310 pre-standardization protected files remain byte-unchanged**. Git confirms that the original data, new standardized data, sidecar, preservation snapshot and provenance manifest remain ignored and untracked.

**Automated tests: 548 pass (9.39 seconds), including 41 new synthetic Serie A standardization tests.** Tests cover historical format boundaries and the full 36-season / 12,644-fixture schedule, exact schema and shared-ID algorithm, reversed-order determinism, date-sensitive/score-insensitive IDs, source-byte and evidence preservation, all correction guard failure modes, duplicate/dangling exception links, corrected-date match-ID linkage, unchanged eligibility counts that could hide swapped case decisions, unresolved conservative handling, overwrite refusal and read-only mismatch reporting. Existing structural/review tests continue to pass. No real private match records were added to tests.

Reproduction from the repository root:

```sh
# First creation only: refuses existing outputs before building.
PYTHONPATH=src python3 -m scripts.standardize_serie_a_results

# Read-only regeneration and byte comparison of all three outputs.
PYTHONPATH=src python3 -m scripts.standardize_serie_a_results --check

# Existing immutable source/review checks remain valid.
PYTHONPATH=src python3 -m scripts.validate_serie_a --check
PYTHONPATH=src python3 -m scripts.verify_serie_a_review

# Full repository tests in the previously prepared temporary environment.
PYTHONPATH=src /tmp/toto-serie-a-test/bin/python -m pytest -q
```

The first build stopped before output creation on a comparison between in-memory integer decade keys and their JSON string-key representation. Canonical JSON comparison resolved that representation mismatch without changing source/evidence bytes or historical facts. The completed build and subsequent read-only regeneration both pass. No force-overwrite option is provided.

### Updated technical readiness and remaining limits

**Technically ready for future integration as a standardized archive with the linked exception policy.** The authorized corrections are now applied in the derivative, all required structural/schema/identity/factual-preservation checks pass, and all outputs reproduce. This readiness does not authorize model integration, training, evaluation or redistribution.

Independent verification remains a bounded sample with shared-source and indexed-only evidence limitations; the exception register is non-exhaustive. Both resumptions and all unlisted fixtures retain unresolved eligibility. Historical legal club continuity, including Parma, Fiorentina and Salernitana transitions, remains a manual-review concern; source names were preserved. engsoccerdata’s noncommercial notice / GPL scope ambiguity and unresolved upstream rights remain in the new manifest. OpenFootball’s CC0 waiver covers only rights held and supplies no blanket third-party clearance. Standardization resolves neither rights nor unreviewed match-status uncertainty.

No original Serie A, English or German data, prior provenance/evidence, DFB pipeline, README, Homework 8 OpenSpec, prediction algorithm or Streamlit application was modified. No integration, model training/evaluation, ongoing-season collection, public match-data export, commit or push was performed.
