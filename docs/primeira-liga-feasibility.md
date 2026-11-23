# Portuguese Primeira Liga — Phase 2 bounded feasibility

Date: 2026-11-23. Original toto worktree, `feature/data-collection`, HEAD `0bb6f393c89fdcc37a52a56bb31e458ff131de47`. Phase 2 only; no historical policy, corrections, screening, final match IDs, standardization, application integration or training.

## Acquisition and protected scope

Exactly seven approved originals acquired successfully: one historical CSV, five OpenFootball TXT files and one mutable RSSSF HTML snapshot. No restricted/unavailable original and no additional dataset requests. Original bytes, response headers/final URLs, attribution, encoding, retrieval UTC, size, SHA-256 and Git blobs are preserved in private adjacent provenance receipts and acquisition.json. Notices and pinned Git trees were reused from the completed Eredivisie evidence, verified against tree receipts and Git blob identities, without network acquisition.

Protected baseline: **1,037 previous private files and 228 tracked public files**, plus the planning-log prefix, starting HEAD and Git index. Eleven completed competitions contain **127,927 screened historical records**; ongoing files and audit-only records are not added to that screened historical total. All remain unchanged. Application code is protected and the promotional worktree is untouched.

Historical pin: `jalapic/engsoccerdata@872c5c354161ace8408f3091b758c6af4cccca94`. Modern pin: `openfootball/europe@63df627f3c87ce71708f016522ea236cf74332c3`. The raw Git source URL is `https://raw.githubusercontent.com/{repository}/{commit}/{original_path}`. RSSSF URL is https://www.rsssf.org/tablesp/porthist199091.html; it has no Git revision or blob.

| Original | Bytes | Git blob SHA-1 | SHA-256 | Retrieved UTC |
|---|---:|---|---|---|
| data-raw/portugal.csv | 592,748 | ffb6afe2e6fd395269edd2cfe00e5de33a30dbc2 | `75ab6c755bd04d33b803c5655d83822a76c1ac19223b547568467273c4083857` | 2026-11-23T13:23:40.070375+00:00 |
| portugal/2018-19_pt1.txt | 24,871 | fda4562db066b03c72bc7892e5a21527e9e41c5d | `303807322184d100390847e766ddd8a61f6753ecfea8426a564293fee0914271` | 2026-11-23T13:23:42.546449+00:00 |
| portugal/2019-20_pt1.txt | 25,013 | 7d5d7a2df26e2b21be46bb9b08c9c8b007b89632 | `0e57f8019ed50e449428fec2cad7fa8eb35bd868cbcbc7356eae4af9b678e013` | 2026-11-23T13:23:45.172062+00:00 |
| portugal/2021-22_pt1.txt | 24,988 | c448a04c11ae5b96e6bdbedabed75d1558f447df | `5e5593b409d4b4ca31782960897b4e40917cc55370101cd68fea1af51a2a3b1c` | 2026-11-23T13:23:47.580188+00:00 |
| portugal/2024-25_pt1.txt | 25,019 | 0bf964ac3c7767645b4a084a8b11ec1cc0db0e6d | `3bb1acda8822a01e1aef1e70f03607650b97fb6722fd0d777f2ef9bf6544ed6c` | 2026-11-23T13:23:49.956622+00:00 |
| portugal/2025-26_pt1.txt | 25,060 | 1bc5b5eae05bdcefeb64c2ea71ea931d546a6873 | `967a4cde722b5598a5c28da8efa65a0ab28da9b1778cee74455b463216dd1adb` | 2026-11-23T13:23:52.324422+00:00 |
| tablesp/porthist199091.html | 11,968 | Not applicable | `31ec0cd1f12cb9700ab7cb3394ff404bcac68c1876ee28031a3ac70e3edf4b80` | 2026-11-23T13:23:54.665947+00:00 |

Requests were bounded to 30 seconds / 8 MB with two-second spacing, no retries or redirects, exact approved URL selection and persistent source-specific stop records. A failed or restricted source is recorded without a mirror or bypass. Original/receipt partial cache pairs fail closed; complete-file publication is atomic and exclusive. Cached replay verifies all originals and receipts and performs zero network requests. No Football-Data, extra RSSSF season or other unapproved source was accessed.

## Historical original: measured schema and coverage

Actual columns, in source order:

```text
Date,Season,home,visitor,FT,hgoal,vgoal,division,tier,totgoal,goaldif,result
```

The original contains **8,958 score-bearing observations across 31 contiguous seasons, 1994/95–2024/25**. Season is starting-year integer text; date is explicit ISO day; division is P1 and tier is 1 throughout. FT matches integer home/away goals, totgoal and goaldif match arithmetic, and result is the goal-derived H/D/A. No missing/nonnumeric goals, malformed widths, date placeholders or contradictory derived fields were found. Original raw bytes are UTF-8-compatible (without conversion); historical labels are largely unaccented abbreviations, while modern names contain Portuguese accents. Literal source fields remain preserved.

**Zero records exist for 1990/91, 1991/92, 1992/93 or 1993/94; no 2025/26 historical CSV rows exist.** There are no gaps within the represented historical interval.

The table below is a metadata-level entire-original inventory. Detailed fixture research is restricted to the five approved historical samples and four acquired overlap seasons. Expected counts do not prove historical correctness or legal result finality. There is no explicit per-row competition-stage/administrative marker in the historical CSV.

| Season | Observed / scored | Literal clubs | Expected clubs / fixtures | Date range | Structural caveat |
|---|---:|---:|---:|---|---|
| 1994/1995 | 306 / 306 | 18 | 18 / 306 | 1994-08-20 – 1995-06-15 | No duplicate/missing literal pairings |
| 1995/1996 | 306 / 306 | 18 | 18 / 306 | 1995-08-20 – 1996-05-12 | No duplicate/missing literal pairings |
| 1996/1997 | 306 / 306 | 18 | 18 / 306 | 1996-08-23 – 1997-06-15 | No duplicate/missing literal pairings |
| 1997/1998 | 306 / 306 | 18 | 18 / 306 | 1997-08-23 – 1998-05-17 | No duplicate/missing literal pairings |
| 1998/1999 | 306 / 306 | 18 | 18 / 306 | 1998-08-21 – 1999-05-30 | No duplicate/missing literal pairings |
| 1999/2000 | 306 / 306 | 18 | 18 / 306 | 1999-08-20 – 2000-05-14 | No duplicate/missing literal pairings |
| 2000/2001 | 306 / 306 | 18 | 18 / 306 | 2000-08-18 – 2001-05-27 | No duplicate/missing literal pairings |
| 2001/2002 | 306 / 306 | 18 | 18 / 306 | 2001-08-10 – 2002-05-05 | No duplicate/missing literal pairings |
| 2002/2003 | 306 / 306 | 18 | 18 / 306 | 2002-08-22 – 2003-06-01 | No duplicate/missing literal pairings |
| 2003/2004 | 306 / 306 | 18 | 18 / 306 | 2003-08-16 – 2004-05-09 | No duplicate/missing literal pairings |
| 2004/2005 | 306 / 306 | 18 | 18 / 306 | 2004-08-28 – 2005-05-22 | No duplicate/missing literal pairings |
| 2005/2006 | 306 / 306 | 18 | 18 / 306 | 2005-08-19 – 2006-05-07 | No duplicate/missing literal pairings |
| 2006/2007 | 240 / 240 | 16 | 16 / 240 | 2006-08-25 – 2007-05-20 | No duplicate/missing literal pairings |
| 2007/2008 | 240 / 240 | 16 | 16 / 240 | 2007-08-17 – 2008-05-11 | No duplicate/missing literal pairings |
| 2008/2009 | 240 / 240 | 16 | 16 / 240 | 2008-08-22 – 2009-05-24 | No duplicate/missing literal pairings |
| 2009/2010 | 240 / 240 | 16 | 16 / 240 | 2009-08-14 – 2010-05-09 | No duplicate/missing literal pairings |
| 2010/2011 | 240 / 240 | 16 | 16 / 240 | 2010-08-13 – 2011-05-14 | No duplicate/missing literal pairings |
| 2011/2012 | 240 / 240 | 17 | 16 / 240 | 2011-08-12 – 2012-05-12 | Feirense trailing-space label; 32 literal missing pairings |
| 2012/2013 | 240 / 240 | 16 | 16 / 240 | 2012-08-17 – 2013-05-19 | No duplicate/missing literal pairings |
| 2013/2014 | 240 / 240 | 16 | 16 / 240 | 2013-08-16 – 2014-05-11 | No duplicate/missing literal pairings |
| 2014/2015 | 306 / 306 | 18 | 18 / 306 | 2014-08-15 – 2015-05-23 | No duplicate/missing literal pairings |
| 2015/2016 | 306 / 306 | 18 | 18 / 306 | 2015-08-14 – 2016-05-15 | No duplicate/missing literal pairings |
| 2016/2017 | 306 / 306 | 18 | 18 / 306 | 2016-08-12 – 2017-05-21 | No duplicate/missing literal pairings |
| 2017/2018 | 306 / 306 | 18 | 18 / 306 | 2017-08-06 – 2018-05-13 | No duplicate/missing literal pairings |
| 2018/2019 | 306 / 306 | 18 | 18 / 306 | 2018-08-10 – 2019-05-19 | No duplicate/missing literal pairings |
| 2019/2020 | 306 / 306 | 18 | 18 / 306 | 2019-08-09 – 2020-07-26 | No duplicate/missing literal pairings |
| 2020/2021 | 306 / 306 | 18 | 18 / 306 | 2020-09-18 – 2021-05-19 | No duplicate/missing literal pairings |
| 2021/2022 | 306 / 306 | 18 | 18 / 306 | 2021-08-06 – 2022-05-15 | No duplicate/missing literal pairings |
| 2022/2023 | 306 / 306 | 18 | 18 / 306 | 2022-08-05 – 2023-05-27 | No duplicate/missing literal pairings |
| 2023/2024 | 306 / 306 | 18 | 18 / 306 | 2023-08-11 – 2024-05-18 | No duplicate/missing literal pairings |
| 2024/2025 | 306 / 306 | 18 | 18 / 306 | 2024-08-09 – 2025-05-17 | No duplicate/missing literal pairings |

The **2011/12 Feirense–Nacional record on 2011-08-14** uses `Feirense ` with a trailing space. Literal preservation yields 17 labels and 32 absent directed pairings in the 17-label Cartesian population, despite the ordinary 16-club / 240-fixture expectation. One source observation is flagged for invalid surrounding whitespace. No trim, correction, exclusion or global alias was applied. The exact source line and audit identity are in exception_diagnostics.json and coverage_inventory.json. This is a source-label defect, not evidence of 32 unplayed matches.

## Five detailed historical samples

| Season | Observed | Scored | Unscored | Clubs | Expected | Missing / duplicate pairs |
|---|---:|---:|---:|---:|---:|---|
| 1994/1995 | 306 | 306 | 0 | 18 | 306 | 0 / 0 |
| 2005/2006 | 306 | 306 | 0 | 18 | 306 | 0 / 0 |
| 2006/2007 | 240 | 240 | 0 | 16 | 240 | 0 / 0 |
| 2013/2014 | 240 | 240 | 0 | 16 | 240 | 0 / 0 |
| 2014/2015 | 306 | 306 | 0 | 18 | 306 | 0 / 0 |

All five samples have valid dates/scores, complete directed pairings, correct ordinary club counts, no reserve labels, no source-order reversals and no individually invalid fields. No extra stage is detectable from the measured counts/pairings and P1/tier1 fields; this is structural support, not certification that the source is historically error-free. Gil Vicente eligibility/relegation context in 2005/06, the 2013/14 relegation playoff and Boavista/expansion context in 2014/15 remain later documentary-review tasks. No administrative outcome was adjudicated.

## Five modern samples

| Season | Observed | Scored | Unscored | Clubs / expected fixtures | Source dates | Wide rounds | Order reversals |
|---|---:|---:|---:|---|---|---:|---:|
| 2018/2019 | 306 | 306 | 0 | 18 / 306 | 2018-08-10 – 2019-05-19 | 0 | 0 |
| 2019/2020 | 306 | 306 | 0 | 18 / 306 | 2019-08-09 – 2020-07-26 | 2 | 2 |
| 2021/2022 | 306 | 306 | 0 | 18 / 306 | 2021-08-06 – 2022-05-15 | 2 | 3 |
| 2024/2025 | 306 | 306 | 0 | 18 / 306 | 2024-08-09 – 2025-05-17 | 2 | 0 |
| 2025/2026 | 306 | 306 | 0 | 18 / 306 | 2025-08-08 – 2026-05-16 | 3 | 0 |

All five have 306 distinct directed pairings, 18 clubs, all 34 round numbers, nine fixtures per round, no duplicate/conflicting pairings, no missing pairings, no invalid parsed dates/scores and no other stages. Exact titles identify Portuguese Primeira Liga; `_pt2`, `_ptcup` and other-stage inputs are outside acquisition scope. Dates come from day/month headings; missing heading years are resolved explicitly using the season and weekday, not guessed from round ordering. That does not certify actual kickoff/completion dates.

Modern totals: **1,530 scored observations, zero unscored/cancelled/awarded annotations**. The 2025/26 pinned snapshot is structurally score-complete at 306/306, not automatically independently historically certified.

The 2019/20 source spans 2019-08-09 to 2020-07-26 and contains all 306 scores. Its explicit July completion is permitted by a narrowly scoped extended-season boundary through 2020-08-02, following the previously discovered official season-extension notice. No Dutch-style cancellation assumption is imported. Scheduling was disrupted, but no individual fixture receives a historical chronology ruling in Phase 2.

### Scheduling and unusual-score review candidates

| Season | Round | First date | Last date | Span | Affected source observations |
|---|---|---|---|---:|---:|
| 2019/2020 | 1 | 2019-08-09 | 2019-09-08 | 30 | 9 |
| 2019/2020 | 9 | 2019-10-05 | 2019-10-31 | 26 | 9 |
| 2021/2022 | 13 | 2021-12-03 | 2022-01-03 | 31 | 9 |
| 2021/2022 | 16 | 2021-12-28 | 2022-01-13 | 16 | 9 |
| 2024/2025 | 24 | 2025-03-01 | 2025-03-28 | 27 | 9 |
| 2024/2025 | 8 | 2024-10-04 | 2024-12-19 | 76 | 9 |
| 2025/2026 | 1 | 2025-08-08 | 2025-09-23 | 46 | 9 |
| 2025/2026 | 16 | 2025-12-27 | 2026-01-11 | 15 | 9 |
| 2025/2026 | 26 | 2026-03-14 | 2026-04-29 | 46 | 9 |

There are **nine wide-round contexts / 81 member observations**, and five source-order reversal pairs. Long spans are review flags, not errors or exclusions. Source-bound fixture IDs are private audit identifiers, not final shared-schema match IDs. Seven modern unusual-score observations are preserved for later review, including Benfica–Nacional 10–0 and Belenenses SAD–Benfica 0–7; unusual valid scores are never auto-corrected.

## Provisional overlap and identity diagnostics

| Season | Compared pairs | Scoped label links | Date conflicts | Score conflicts | Unmatched historical / modern |
|---|---:|---:|---:|---:|---|
| 2018/2019 | 306 | 18 | 0 | 0 | 0 / 0 |
| 2019/2020 | 306 | 18 | 1 | 0 | 0 / 0 |
| 2021/2022 | 306 | 18 | 0 | 0 | 0 / 0 |
| 2024/2025 | 306 | 18 | 0 | 0 | 0 / 0 |

**1,224 scored overlap pairs** are linked provisionally under explicit one-to-one, season-local source-label hypotheses. They are not 1,224 additional unique fixtures, and agreement is not proof of independent upstream provenance. There are zero score disagreements and one date conflict: **Santa Clara–Paços de Ferreira 2–1, historical 2020-02-01 versus modern 2020-02-02**. Both values remain unchanged pending later independent review.

Historical `Belenenses` is compared diagnostically with modern `Belenenses SAD` only within acquired overlap seasons. This is not legal/entity continuity approval and is never used to rewrite an original. Other exact scoped hypotheses include Benfica/SL Benfica/Sport Lisboa e Benfica, Sp Lisbon/Sporting CP, Guimaraes/Vitória Guimarães and Setubal/Vitória Setúbal. Full lists, reasons and source IDs are in overlap_diagnostics.json. Senior/B sides remain distinct. AVS versus historical Aves must not be merged; historical AVS Futebol SAD/modern AVS is only a specific overlap label hypothesis. Campomaior/Campomaiorense, Chaves/Desp. Chaves, Est Amadora/Estrela da Amadora and Madeira/Nacional are inventory labels requiring historical continuity review, not approved aliases.

### Belenenses SAD–Benfica 2021/22

The frozen modern original at physical line **187**, Matchday 12, records **2021-11-27, Belenenses SAD v SL Benfica, 0–7 (0–7)**, with an empty annotation string. The historical observation also records 2021-11-27 / 0–7 under Belenenses/Benfica. Neither acquired source marks abandonment. This omission illustrates why a syntactically complete score cannot establish legal finality. Prior discovery identified the interrupted event and an FPF disciplinary decision; the actual completion, administrative finality and result-availability fields remain unknown in Phase 2 metadata. No score selection, HOLD OUT or NOT PLAYED decision is made.

## RSSSF 1990/91: results without fixture dates

The preserved snapshot is ASCII-compatible HTML with entity-encoded accents. It contains final standings, a 20-club results cross-table and an accumulated historical table. The author is Jorge Miguel Teixeira; last update 31 May 2002; copyright Jorge Miguel Teixeira and RSSSF 1999/2002. The page permits copying all or part with proper author acknowledgement and reserves other rights. That permits this bounded attributed preservation; it does not establish unrestricted commercial/model-training rights.

The independent reconstruction yields **380 home/away score identities and zero dated fixture records**. All reconstructed dates remain null, with historical/legal finality NOT ESTABLISHED. No fixture dates, matchday dates, score-cell administrative annotations or distinct playoff block were found in the inspected relevant section. The page update date is not a match date. No standardized records or invented dates are produced. This supports result-only 1990/91 reference work but does not close any of the four dated-source gaps.

## Rights and source provenance

Technical availability, bounded private inspection, licence, upstream ownership, attribution, redistribution, commercial use, model training and corroboration independence are separate. engsoccerdata retains README noncommercial wording and GPL >=2 package metadata; that does not resolve underlying data ownership. OpenFootball CC0 applies to rights held and does not warrant upstream clearance. RSSSF retains its page-specific conditions. No claim of independent source lineage is based merely on repository disagreement/agreement. Football-Data restrictions and its Phase 1 HTTP 429 remain respected; no requests were made there. No training or application integration is authorized.

## Reproducibility and fresh verification

The acquisition, assessment and separate-parser commands are:

```sh
PYTHONPATH=src:. python -B scripts/collect_primeira_liga_feasibility.py --init
PYTHONPATH=src:. python -B scripts/collect_primeira_liga_feasibility.py
PYTHONPATH=src:. python -B scripts/validate_primeira_liga_feasibility.py
PYTHONPATH=src:. python -B scripts/verify_primeira_liga_feasibility.py
```

`--init` is exclusive baseline creation, not a reinitialization instruction for existing data. All writes are exclusive and mismatched existing artifacts fail. The separate verifier implements its own CSV/TXT/RSSSF parsers and checks source binding, full historical inventory, every sampled modern record and all overlap comparisons. Five derived assessments plus independent reconciliation regenerated byte-for-byte and SHA-256 identically using safe temporary files; a separate process regenerated the five assessments. Cached acquisition replay made **zero requests** with a network-failing stub and left all 35 then-existing private artifacts byte-identical. All seven original receipts and six Git blobs/sizes pass.

Fresh tests use the established external Python 3.13.12 environment; no installation or original .venv modification. Bounded processes disable project bytecode and pytest cache and use temporary pytest directories.

| Test selection | Passed | Failed / errors / skipped |
|---|---:|---|
| New focused Portugal | 52 | 0 / 0 / 0 |
| Acquisition / importer selection | 670 | 0 / 0 / 0 |
| Non-UI | 1,891 | 0 / 0 / 0 |
| App / launcher | 7 | 0 / 0 / 0 |
| Full repository | 1,898 | 0 / 0 / 0 |

Selections overlap and are not additive. An initial synthetic test incorrectly expected a July date at the beginning of the next season to be invalid; its test fixture was corrected to test July after a nonextended season. No historical values or original files changed. Test logs/XML/status, regeneration hashes and final preservation receipts remain private.

## Precise proposed Phase 3 and stopping boundary

The historical CSV is technically promising as a contiguous 1994/95–2024/25 main-source candidate, subject to full validation and later historical review, particularly the 2011/12 whitespace defect. Do not certify the full original from sample completeness.

Propose acquisition of **only three additional OpenFootball originals** at the existing `63df627f3c87ce71708f016522ea236cf74332c3` pin: `portugal/2020-21_pt1.txt`, `portugal/2022-23_pt1.txt` and `portugal/2023-24_pt1.txt`. Their retained-tree identities are: 2020/21 blob `ca49d56b7fdb7818f7309ef1b07fd2a33b39de3f` / 24,866 bytes; 2022/23 blob `02fcf01267c8ae5305acec400e031519954600bd` / 25,043 bytes; 2023/24 blob `5b82a592e07f16ad42be4d24e0318cbac4ecf020` / 25,093 bytes. Exact identity must be rechecked immediately before approved acquisition. Reuse all seven originals unchanged. Inventory the resulting 32 represented dated-source seasons 1994/95–2025/26 without silently merging overlaps or accepting records.

1990/91–1993/94 remain a four-season dated-acquisition gap. A separate source-discovery/permission step should seek permitted dated records from official/club archives or accessible historical providers; use RSSSF only as result corroboration. Index-only or HTTP403 records are leads, not acquired evidence. Do not bulk scrape, purchase or substitute a mirror without approval.

Future phases must review the date conflict, Belenenses abandoned fixture, nine wide rounds, five reversals, Feirense label and historical identity/administrative issues. Rights remain unresolved. Phase 3 has not begun. No screening, final standardization, Git staging/commit/push, model use or application change occurred.
