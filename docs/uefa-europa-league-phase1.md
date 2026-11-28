# UEFA Cup / UEFA Europa League — Phase 1 source discovery and acquisition

**PASS — Phase 1 acquisition completed, with explicitly unverified fixture completeness.** Reviewed 2026-11-27 exclusively in `toto-uefa`, branch `feature/uefa`. Phase 2 is not started. No staging, commit, push, provider messages, model/application changes or production integration.

## Scope and conventions

Investigated all **36 seasons**, UEFA Cup 1990/91–2008/09 and UEFA Europa League 2009/10–2025/26, as a continuous competition while retaining historical labels. All preliminary, qualifying, play-off, group/league and knockout stages remain eligible; no final event adjudication has occurred. Original mixed-competition archive containers remain intact, but diagnostics inspect only the target section/code. No unrelated competition becomes an EL record.

Followed [PROCESS.md](../PROCESS.md), the [five-phase workflow](accelerated-five-phase-workflow.md), [local archive conventions](local-data-integration.md), the Champions League phase reports, acquisition utilities and synthetic boundary tests. Reused immutable save/hash/blob/URL guards; added a competition-specific acquisition plan and minimal acquisition-readability diagnostics, rather than a canonical parser. Unlike the older UCL Phase 1 planning-only report, this explicitly authorized Phase 1 includes actual corpus acquisition.

The clean starting branch/worktree and HEAD are captured privately. **341 existing files** were fingerprinted before changes. This worktree contains domestic sample/raw CSVs and the UCL scripts/reports, but **no pre-existing private domestic/UCL archives**. Other worktrees were not accessed. Preservation certification therefore covers present files; this task cannot freshly certify absent archives. Existing `PROCESS.md` is present, unlike the historical UCL Phase 1 inspection.

## Acquisition results

| Measure | Observed result |
|---|---:|
| Seasons investigated / with acquired target content | 36 / 36 |
| Seasons with main content | 36 (completeness unverified) |
| Seasons with qualifying content | 32, 1994/95–2025/26 (completeness unverified) |
| Earlier four seasons | No qualifying heading in acquired UEFA Cup sections; preliminary non-applicability assessment |
| Sources screened / sources with fixture-bearing originals | 14 / 5 |
| Original payloads / fixture-bearing payloads / metadata | 75 / 58 / 17 |
| Original payload bytes, excluding receipts | 44,222,060 |
| OpenFootball scored description lines | 977 |
| 11footy target-season source rows | 8,467 |
| 11footy target statuses | 8,463 played; 4 awarded |
| Schoch target-era date-window EL-labelled rows | 11,254 |
| Schoch auxiliary goal-event rows | 8,016 |
| RSSSF target-section score-bearing text lines | 4,450 |

**These units must not be summed as matches.** Overlapping source observations, paired-leg grids, commentary, standings, event rows and repeated summaries have different meanings. No final unique fixture total or independently verified complete season is claimed. Wikipedia revisions and RSSSF details were preserved without creating a fixture inventory.

Original file breakdown: seven OpenFootball EL/ELQ TXT files; two Schoch containers; 33 RSSSF summary pages plus seven details; one 26-member 11footy ZIP; eight Wikipedia revision JSONs. There are 16 planned permission/discovery metadata originals and one bootstrap tree. All originals have URL, acquisition UTC, byte size, SHA-256 and receipts; GitHub source files additionally match pinned Git blob IDs/sizes. The initial tree receipt transparently derives its timestamp from the original write mtime and lacks captured response headers; it is discovery-only, not a fixture input.

## Source registry and permissions

The private `source_registry.json` records access, format, verified versus claimed coverage, fields, qualifying limits, rights, suitability, provenance and known limitations. The following is its public assessment summary; it includes no raw fixtures.

| Source | Coverage evidence and field assessment | Rights / disposition |
|---|---|---|
| [OpenFootball](https://github.com/openfootball/champions-league) | **football.txt**. Verified 2020/21–2024/25 main; 2024/25–2025/26 qualifying; no earlier EL or 2025/26 main at pin. date headings; oriented team labels; printed scores/HT/ET/penalty annotations; no guaranteed aggregates or neutral fields. Recent primary/corroboration; no completeness certification. | CC0 rights held; third-party clearance not warranted. **acquired**. |
| [RSSSF contributors](https://www.rsssf.org/ec/) | **HTML/preformatted text**. 33 summary pages 1990/91–2022/23; seven linked details 2002/03–2008/09; 2023/24–2024/25 rendered-only; 2025/26 unverified. oriented tie grids and dates/round dates; FT/HT/ET/penalties/aggregates/venues/administrative notes vary; 90-minute result often ambiguous. Historical primary/corroboration; summary lines are not fixture totals. | Page-specific acknowledgement copying grants; retain full author/footer; local-only under project policy. **acquired**. |
| [David Schoch](https://github.com/schochastics/football-data) | **Parquet and goal-event CSV**. Actual 1,309,501-row mixed archive; 14,679 UEFA EL-labelled rows, 11,254 in target-era July 1990–June 2026 date window; last date 2025-08-28; no source season/stage. directed names/identifiers, exact dates, gh/ga and F/E/P status; goals include ET/penalties; HT/90-minute/aggregates/neutral absent in results; event CSV auxiliary. Early dates/score corroboration; source warns old errors and team identity ambiguity. | README ODC-By database grant; retain David Schoch attribution; underlying content rights not warranted. **acquired**. |
| [11footy](https://github.com/fm-devlab/11footy-dataset) | **CSV ZIP, 26 members**. Verified 2001/02–2025/26 season content, uneven early qualifying; release also contains 224 out-of-scope 2026/27 rows. dates/kickoff precision, team IDs, stage, group, leg, ties, status, goals/on-pitch/HT/regular-time/ET flag/shootout, neutral flag; populated fields vary; tie table retained. Primary recent source; explicit regular-time fields only 215 target rows; lineage unproven. | CC BY-NC 4.0; credit 11footy, noncommercial only; all originals private. **acquired**. |
| [Wikipedia contributors](https://en.wikipedia.org/wiki/UEFA_Europa_League) | **MediaWiki revision JSON/wikitext**. Eight revision JSON payloads: six early/context articles and 2025/26 league/knockout subarticles. match/tie templates, oriented labels, dates and score annotations where supplied; HT/90-minute/venue availability varies; final-score text not automatically regulation. Targeted corroboration and format leads; not an independent fixture-count audit. | CC BY-SA 4.0 text; title/revision/permalink/history attribution; share-alike where applicable; no media acquired. **acquired**. |
| [FootballCSV](https://github.com/footballcsv/europe-champions-league) | **CSV**. Pinned tree inspected: Champions League files, no UEFA Cup/EL corpus verified. Target EL fields unverified; UCL schema must not be assumed transferable. Not suitable for this target at inspected tree. | Pinned CC0 notice; third-party disclaimer retained. **screened-no-target**. |
| [James Curley engsoccerdata](https://github.com/jalapic/engsoccerdata) | **CSV/R**. Pinned recursive tree inspected; no UEFA Cup/Europa League fixture file found; champs.csv is another competition. Target EL fields unverified. No speculative UCL reuse. | README noncommercial attribution; GPL package code separate. **screened-no-target**. |
| [UEFA official platforms](https://www.uefa.com/termsconditions/) | **Web/API not acquired**. Official archive is a potential reference; no target season content audited. All target fields and season/stage completeness unverified in this task. Permission-dependent primary authority; unsent request prepared. | Section 6.2 restrictions on systematic collection/automation/software uses; no fixture harvesting. **permission-required**. |
| [football-data.org](https://www.football-data.org/coverage) | **API JSON**. EL is listed; no historical season/qualifier entitlement verified. Provider v4 regularTime/duration semantics documented, but actual target dates/teams/HT/ET/penalties/neutral completeness unverified. Optional licensed supplement, not certified gap recovery. | Account/entitlement and retention/use terms need confirmation; no spend or contact. **entitlement-required**. |
| [API-Football](https://www.api-football.com/terms) | **API JSON**. No authenticated season-specific EL coverage query. Actual target period/date/stage/neutral fields unverified. Optional licensed supplement. | Registered service; resale restricted; verify scope and archive retention. **entitlement-required**. |
| [FootyStats](https://footystats.org/europe/uefa-europa-league/datasets) | **CSV advertised**. Index claims 2009/10 onward season CSVs, including 477 rows for 2009/10; not acquired or verified. Target fields and stage/date/period/neutral completeness unverified. Potential qualifier supplement; index row count is not a historical total. | Download entitlement and reuse/retention permission not established; no gated access. **permission-required**. |
| [Bert Kassies](https://kassiesa.net/uefa/) | **HTML not acquired**. Season/stage results are a lead only; no fresh target contents audited. All target fields unverified. Potential structural corroboration only. | Earlier UCL documentation records 403 access stop; no retry/bypass; permission unclear. **access-stop-inherited**. |
| [Zafronix UEL Explorer](https://api.zafronix.com/uel-explorer/) | **Dashboard/JSON API**. Advertises seasons since 1971; visible dashboard totals/index do not establish complete fixtures/qualifying. Advertised matches/venues, but dates/periods/stages/neutral availability unverified. Early-era alternative investigated; no authenticated acquisition. | API key and retention/reuse terms unestablished; no account created. **permission-required**. |
| [FutPythonTrader](https://futpythontrader.com.br/datasets) | **CSV advertised**. Catalogue lists recent EL seasons and differently named calendar-year datasets; contents unverified. All target fields and season/stage/period semantics unverified. Alternative investigated; do not infer rights from a download button. | CSV downloads advertised; no explicit data reuse/retention licence established. **unclear-rights**. |

For non-acquired candidates every unverified field remains explicitly unverified: neither an index entry nor API marketing certifies dates, directed teams, half-time, regulation, extra-time, shootouts, aggregates, venue or stage completeness. OpenFootball and Wikipedia may share upstreams; Schoch and 11footy independence is also unestablished. A separate publisher is not an independent historical vote.

Pinned repository commits: OpenFootball `abfaeddc2ee3d14f99ecc163c9ddb46cb4d67cef`; Schoch `6ba5e7e8f8657b6ccdeb0e89778765423f8d5aaf`; 11footy metadata `37db9c77c4509b9dcf4915b60b058cdeb1a6a772`, release `11footy-2026-11-10`. The original ZIP matches the release asset SHA-256 `ae2045c472f7ac8e29d17719b8e36b84f02b458fa0f252e7028c32b44735105c`; its CRC check passes for all 26 members. Release payload digest, rather than the repository commit, identifies that original.

All raw data, permission notices, inventories, detailed diagnostics and drafts remain under Git-ignored `data/private/europe/europa_league/phase1/`. CC0 may support public redistribution for rights held; ODC-By requires attribution and does not license all individual contents; CC BY-NC restricts commercial use; CC BY-SA attribution/share-alike and RSSSF author acknowledgements must be retained. Project policy keeps the entire real-data corpus private. No source is promoted to model-use or publication clearance. This directory is iCloud-backed: Git-ignored does not mean device-only.

## Complete preliminary season matrix

R = acquired RSSSF target-section score-bearing **text lines**, not matches; N = 11footy source-declared target-season **rows**, including awards; O = OpenFootball scored main / qualifying **description lines**. A dash means that source file is absent/unacquired, never zero historical fixtures. All seasons have directed/date-bearing Schoch observations in the target-era archive; its lack of season/stage fields prevents reliable per-season totals here. Six early Wikipedia contexts and the latest league/knockout revisions provide additional bounded corroboration.

Main content is present for every row, with no completeness certification. Q = qualifying content acquired; NA? = no qualifying heading in the target section, subject to later format confirmation. RSSSF does not always print each group fixture; its low 2021/22–2022/23 line counts demonstrate why source-line counts are unsafe fixture totals. Detailed per-row dates, score semantics, primary/corroborating sources, rights and remaining gaps appear in `season_coverage.csv`.

| Season | Historical name | R lines | N rows | O main / Q | Q assessment |
|---|---|---:|---:|---|---|
| 1990/91 | UEFA Cup | 66 | — | — / — | NA? |
| 1991/92 | UEFA Cup | 66 | — | — / — | NA? |
| 1992/93 | UEFA Cup | 70 | — | — / — | NA? |
| 1993/94 | UEFA Cup | 65 | — | — / — | NA? |
| 1994/95 | UEFA Cup | 95 | — | — / — | Q; incomplete/unverified |
| 1995/96 | UEFA Cup | 104 | — | — / — | Q; incomplete/unverified |
| 1996/97 | UEFA Cup | 127 | — | — / — | Q; incomplete/unverified |
| 1997/98 | UEFA Cup | 113 | — | — / — | Q; incomplete/unverified |
| 1998/99 | UEFA Cup | 115 | — | — / — | Q; incomplete/unverified |
| 1999/00 | UEFA Cup | 141 | — | — / — | Q; incomplete/unverified |
| 2000/01 | UEFA Cup | 153 | — | — / — | Q; incomplete/unverified |
| 2001/02 | UEFA Cup | 148 | 286 | — / — | Q; incomplete/unverified |
| 2002/03 | UEFA Cup | 144 | 196 | — / — | Q; incomplete/unverified |
| 2003/04 | UEFA Cup | 144 | 244 | — / — | Q; incomplete/unverified |
| 2004/05 | UEFA Cup | 128 | 138 | — / — | Q; incomplete/unverified |
| 2005/06 | UEFA Cup | 128 | 141 | — / — | Q; incomplete/unverified |
| 2006/07 | UEFA Cup | 138 | 236 | — / — | Q; incomplete/unverified |
| 2007/08 | UEFA Cup | 140 | 275 | — / — | Q; incomplete/unverified |
| 2008/09 | UEFA Cup | 140 | 278 | — / — | Q; incomplete/unverified |
| 2009/10 | Europa League | 170 | 437 | — / — | Q; incomplete/unverified |
| 2010/11 | Europa League | 179 | 481 | — / — | Q; incomplete/unverified |
| 2011/12 | Europa League | 179 | 482 | — / — | Q; incomplete/unverified |
| 2012/13 | Europa League | 176 | 478 | — / — | Q; incomplete/unverified |
| 2013/14 | Europa League | 176 | 441 | — / — | Q; incomplete/unverified |
| 2014/15 | Europa League | 172 | 481 | — / — | Q; incomplete/unverified |
| 2015/16 | Europa League | 171 | 475 | — / — | Q; incomplete/unverified |
| 2016/17 | Europa League | 171 | 468 | — / — | Q; incomplete/unverified |
| 2017/18 | Europa League | 169 | 473 | — / — | Q; incomplete/unverified |
| 2018/19 | Europa League | 196 | 519 | — / — | Q; incomplete/unverified |
| 2019/20 | Europa League | 188 | 511 | — / — | Q; incomplete/unverified |
| 2020/21 | Europa League | 192 | 362 | 205 / — | Q; incomplete/unverified |
| 2021/22 | Europa League | 42 | 175 | 139 / — | Q; incomplete/unverified |
| 2022/23 | Europa League | 44 | 175 | 141 / — | Q; incomplete/unverified |
| 2023/24 | Europa League | — | 175 | 141 / — | Q; incomplete/unverified |
| 2024/25 | Europa League | — | 269 | 189 / 80 | Q; incomplete/unverified |
| 2025/26 | Europa League | — | 271 | — / 82 | Q; incomplete/unverified |

## Coverage gaps and historical complexity

- **No missing source season** remains. Missing fixtures may still exist: source content presence is not complete competition coverage. The machine files have significant stage/count discrepancies, including 11footy 2002/03, 2004/05 and 2005/06 without explicitly tagged qualifying rows. RSSSF summary/detail originals supply alternative qualifying material. Its 2003/04 and 2006/07 qualifying observations are also partial; later generic first-round/play-off labels require season-specific interpretation.
- **2009/10 and 2013/14** 11footy coverage is visibly lower than adjacent formats; **2018/19–2019/20** generic stage labels distort a provisional qualifier split. Do not equate “other rows” in private diagnostics with verified main fixtures. Acquired RSSSF and Schoch alternatives preserve the material for structural comparison. A final stage taxonomy belongs to Phase 2.
- **Early dates**: Schoch has exact row dates but no declared seasons/stages; RSSSF often provides nominal round dates and exception notes. Targeted 1990/91, 1994/95 and 2000/01 Wikipedia articles and seven 2002/03–2008/09 RSSSF detail pages were acquired. Detailed per-fixture date corroboration remains later work; no round date has been assigned to every tie.
- **Recent gaps**: OpenFootball has no 2025/26 main file. The 11footy release contains 189 main source rows plus qualifying material, with Wikipedia league/knockout revision corroboration. RSSSF 2025/26 could not be established through the web tool; absence is not asserted. For 2023/24 and 2024/25 its rendered author grants were seen, but direct-response grant recognition failed; raw pages were not saved. Existing OpenFootball/11footy data cover those seasons. No repeated workaround is planned.
- **Regulation scores**: Schoch explicitly says goals include extra time and penalties. Its F/E/P flag is retained, not converted into a 90-minute result. Only 215 target 11footy rows populate the explicit regular-time field; ordinary full scores are not relabelled automatically. OpenFootball can print shootout-first and extra-time-first notations. RSSSF tie aggregates and ET suffixes must remain distinct. HT, on-pitch, cumulative ET, shootouts, aggregates and original annotations remain in original bytes. No missing period was inferred.
- **Formats**: retain early two-leg finals, later single-match finals, pre-2004 knockout formats, five-team UEFA Cup groups, 48-team Europa League groups, the 2021 competition restructuring and 2024 league phase. The modern 36-team, eight-opponent league phase implies 144 league games and 45 later knockout games (189 total); 189 source rows is only a format cross-check. Actual match identity and completeness remain unverified.
- **Dates/status/neutrality**: preserve June qualifiers and the COVID August 2020 finish. Four 11footy target rows are source-labelled awarded; no date/result/status adjudication has been applied. Preserve abandonment/replay/walkover notes, original names, IDs and source-designated orientation. Source neutral flags describe uncertain provider semantics; later official-format neutrality follows PROCESS.md, not an assumption from single-leg or stadium location. No administrative-decision-date research was performed.
- **Containers**: Schoch includes unrelated domestic/European competitions and out-of-period Fairs Cup-era labels; only target-era UEFA EL-labelled observations are provisionally considered here. The 11footy ZIP also contains 224 out-of-scope 2026/27 rows. They stay in immutable original containers and are excluded from target diagnostics. No production dataset was changed.

## Reproduction, validation and preservation

Use the unchanged existing research environment, without installation or dependency changes:

```sh
/private/tmp/toto-hungary-phase4-tests-20261127/bin/python -B -m scripts.acquire_uefa_europa_league
/private/tmp/toto-hungary-phase4-tests-20261127/bin/python -B -m scripts.assess_uefa_europa_league_phase1
```

Acquisition is offline by default; `--network` only requests missing plan entries. Existing pairs are verified, never redownloaded. Source plan records original paths/filenames, URLs, pinned blob/digest/size, permission notice hashes, bounds and encodings. Missing GitHub sources can be reproduced at their pins; unversioned RSSSF pages/API queries cannot promise future identical server bytes. Frozen originals and receipts are the offline authority. Wikipedia attribution preserves the exact acquired revision IDs and permalinks.

No authentication, access-denial retry, rate-limit bypass or UEFA fixture harvesting occurred. The only approved redirect path is normal public GitHub release distribution to `release-assets.githubusercontent.com`; temporary signed query strings are omitted from receipts. RSSSF encoding/HTML-grant failures remain recorded; corrected legacy pages were acquired after reviewing the parser errors. Sandboxed DNS failure was followed by normal authorized network execution, not an access-control workaround.

Targeted validation covers immutable caches and tampering, permission evidence, URLs/private paths/bounds, host access stops, release redirect/digest constraints, HTML copy-grant recognition and mixed-competition section boundaries. Existing Champions League acquisition/inventory, schema and source-validation tests are included in the focused run. Full-suite finalization is not part of this Phase 1. **144 focused tests passed, zero failures/skips.** Exact commands/results and preservation checks are in private `verification.json`.

Deliverables: public acquisition/assessment scripts, synthetic tests and this report; append-only `PLANNING_LOG.md`; private `source_registry.json`, `source_plan.json`, `acquisition_manifest.json`, `season_coverage.csv`, `preliminary_readability.json`, `wikipedia_attribution.json`, `permission_requests_unsent.md`, original/receipt pairs, access-failure records, initial diagnostic attempt, baseline and final verification. No existing tracked file other than the appended planning log is changed.

## Phase 2 readiness and user decisions

The preserved TXT, CSV/Parquet, HTML and revision JSON originals are readable and ready for authorized structural processing. Required adapters are source-specific football.txt periods/dates; Parquet competition/season/stage assessment; RSSSF mixed sections/two-leg grids/detail pages; 11footy ZIP tables/IDs/statuses and missing regular-time semantics; and Wikipedia wikitext/templates. The goal-event CSV is auxiliary, never a fixture inventory.

**No known remaining permitted acquisition gap materially prevents Phase 2.** Source disagreements, missing individual fixtures, exact dates, score periods, awards, replays, historical names and format-neutrality decisions remain unresolved for the later workflow. No final unique-event inventory, adjudication, standardization or integration has been produced.

No routine acquisition decision requires approval. Private unsent permission drafts are available if restricted sources become necessary; sending, account creation or spending would need separate authorization. **Stop here; explicit owner approval is required before Phase 2.**
