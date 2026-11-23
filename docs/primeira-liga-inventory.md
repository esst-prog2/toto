# Portuguese Primeira Liga — Phase 3 acquisition and complete source inventory

2026-11-23. Original toto worktree, feature/data-collection, HEAD `0bb6f393c89fdcc37a52a56bb31e458ff131de47`. Phase 3 only: no source preference, historical correction, inclusion/exclusion disposition, screening, standardization, training, integration or Git publication.

## Protection and acquisition

Starting branch/HEAD matched approval; independent remote query returned the identical hash. Previous protection passes for 1,037 private / 228 public files and 127,927 screened historical records across eleven competitions. The Phase 3 baseline additionally freezes 59 Phase 2 public/private entries and the entire current planning-log prefix. The Git index, original .venv, prediction application and promotional worktree remain unchanged.

Exactly three additional originals were acquired. Their paths, blobs and sizes were independently checked against retained, checksum-verified repository tree metadata before requests. All seven Phase 2 originals were reused unchanged, including the historical CSV, five modern TXT files and attributed RSSSF snapshot. No other data acquisition occurred.

Repository: `openfootball/europe`, revision `63df627f3c87ce71708f016522ea236cf74332c3`. Exact URL prefix: `https://raw.githubusercontent.com/openfootball/europe/63df627f3c87ce71708f016522ea236cf74332c3/`.

| Original | Bytes | Git blob | SHA-256 | Retrieval UTC |
|---|---:|---|---|---|
| portugal/2020-21_pt1.txt | 24866 | `ca49d56b7fdb7818f7309ef1b07fd2a33b39de3f` | `381113f27961277c23f9bbc27543a263f6459236860cc3b9c0698e547ab64b12` | 2026-11-23T13:37:51.236394+00:00 |
| portugal/2022-23_pt1.txt | 25043 | `02fcf01267c8ae5305acec400e031519954600bd` | `fa7d1938a28199b2e714437769c4f56ac28f184e0f1ebdfd2603683c1a850a34` | 2026-11-23T13:37:53.649825+00:00 |
| portugal/2023-24_pt1.txt | 25093 | `5b82a592e07f16ad42be4d24e0318cbac4ecf020` | `7f19ddec6033a465ffa1e76b70103aea3005b63c0d27e3f723d0924c814da511` | 2026-11-23T13:37:56.064196+00:00 |

Requests: 30-second timeout, 8 MB bound, two-second spacing, no redirects/retries or alternative revisions, persistent access-stop handling. Originals and receipts use exclusive atomic publication and fail on partial/corrupt caches. Every source has exact URL, revision/blob, physical bytes, size/SHA, timestamp, UTF-8-compatible encoding, response metadata, attribution and rights limitations. Cached rerun made zero requests and preserved all 71 then-existing non-test-log private files byte-identically. No access failure occurred.

## Independent historical CSV inventory

The new inventory parser is separate from the Phase 2 raw parser. A reconciliation verifier independently reparses using the earlier parser and compares all 8,958 historical observations, every physical line binding and all original fields, not merely five sample totals.

Historical source: `jalapic/engsoccerdata@872c5c354161ace8408f3091b758c6af4cccca94`, `data-raw/portugal.csv`. Original bytes and SHA-256 remain identical to Phase 2. Exact columns:

```text
Date,Season,home,visitor,FT,hgoal,vgoal,division,tier,totgoal,goaldif,result
```

Actual coverage is 31 contiguous seasons, 1994/95–2024/25, with 8,958 scored observations, zero unscored, zero invalid dates and zero score/derived-field contradictions. All rows identify P1/tier1. There are no duplicate or conflicting literal directed pairs. No source-order reversals occur. Historical date strings are explicit ISO days; their actual kickoff/completion/availability semantics remain uncertified.

| Season | Observed / scored | Clubs literal / expected | Expected fixtures | Literal directed pairs / missing | Date range |
|---|---:|---|---:|---|---|
| 1994/1995 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 1994-08-20 – 1995-06-15 |
| 1995/1996 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 1995-08-20 – 1996-05-12 |
| 1996/1997 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 1996-08-23 – 1997-06-15 |
| 1997/1998 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 1997-08-23 – 1998-05-17 |
| 1998/1999 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 1998-08-21 – 1999-05-30 |
| 1999/2000 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 1999-08-20 – 2000-05-14 |
| 2000/2001 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 2000-08-18 – 2001-05-27 |
| 2001/2002 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 2001-08-10 – 2002-05-05 |
| 2002/2003 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 2002-08-22 – 2003-06-01 |
| 2003/2004 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 2003-08-16 – 2004-05-09 |
| 2004/2005 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 2004-08-28 – 2005-05-22 |
| 2005/2006 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 2005-08-19 – 2006-05-07 |
| 2006/2007 | 240 / 240 | 16 / 16 | 240 | 240 / 0 | 2006-08-25 – 2007-05-20 |
| 2007/2008 | 240 / 240 | 16 / 16 | 240 | 240 / 0 | 2007-08-17 – 2008-05-11 |
| 2008/2009 | 240 / 240 | 16 / 16 | 240 | 240 / 0 | 2008-08-22 – 2009-05-24 |
| 2009/2010 | 240 / 240 | 16 / 16 | 240 | 240 / 0 | 2009-08-14 – 2010-05-09 |
| 2010/2011 | 240 / 240 | 16 / 16 | 240 | 240 / 0 | 2010-08-13 – 2011-05-14 |
| 2011/2012 | 240 / 240 | 17 / 16 | 240 | 240 / 32 | 2011-08-12 – 2012-05-12 |
| 2012/2013 | 240 / 240 | 16 / 16 | 240 | 240 / 0 | 2012-08-17 – 2013-05-19 |
| 2013/2014 | 240 / 240 | 16 / 16 | 240 | 240 / 0 | 2013-08-16 – 2014-05-11 |
| 2014/2015 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 2014-08-15 – 2015-05-23 |
| 2015/2016 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 2015-08-14 – 2016-05-15 |
| 2016/2017 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 2016-08-12 – 2017-05-21 |
| 2017/2018 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 2017-08-06 – 2018-05-13 |
| 2018/2019 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 2018-08-10 – 2019-05-19 |
| 2019/2020 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 2019-08-09 – 2020-07-26 |
| 2020/2021 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 2020-09-18 – 2021-05-19 |
| 2021/2022 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 2021-08-06 – 2022-05-15 |
| 2022/2023 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 2022-08-05 – 2023-05-27 |
| 2023/2024 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 2023-08-11 – 2024-05-18 |
| 2024/2025 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 2024-08-09 – 2025-05-17 |

One label-invalid observation occurs in 2011/12; no CSV-width, numeric-score or derived-field malformed observations exist. Historical stage is not explicitly specified per row. P1/tier1, complete ordinary pairings and season counts support regular-season scope but cannot independently certify absence of historical administrative problems. Gil Vicente, Boavista, União de Leiria and other continuity/disciplinary issues are carried forward without score changes. The historical inventory includes 18 unusual-score observations as review leads only.

## Exact Feirense whitespace diagnostic

At CSV physical line **4877**, the source records **2011-08-14, `Feirense `–`Nacional`**, with the trailing space preserved. Source audit identity: `5265c556cbad744e664ed5f55bec58e0117a48b279d3ef3aa1f435b2753aa25b`.

| Accounting | Rows | Clubs | Directed pairs | Missing pairs | Duplicate pairs |
|---|---:|---:|---:|---:|---:|
| Literal unmodified source | 240 | 17 | 240 | 32 | 0 |
| Hypothetical one-observation whitespace link | 240 | 16 | 240 | 0 | 0 |

Only the exact selected observation is changed in an in-memory comparison copy. The original source, saved source record and all other labels remain untouched. All 30 source observations involving Feirense are retained in the private diagnostic for surrounding-pair inspection. This demonstrates lossless structural reconcilability; it does not approve a global trim, canonical name or final correction. The 32 literal missing pairings are not 32 missing real-world matches.

## Complete modern inventory

Eight originals cover 2018/19–2025/26. Total **2,448 observed, 2,448 scored, zero unscored**. Each has 18 clubs, 306 distinct directed pairings, all 34 rounds with nine fixtures each, zero duplicate/missing pairings, zero invalid dates/scores and zero other-stage rows. There are no explicit cancellation, award or abandonment annotations in these frozen originals. Parser titles/stages and original source lines remain bound to pinned files.

| Season | Source path | SHA-256 | Observed / scored / unscored | Date range | Wide rounds | Reversal pairs | Unusual scores |
|---|---|---|---|---|---:|---:|
| 2018/2019 | openfootball/europe/portugal/2018-19_pt1.txt | `303807322184d100390847e766ddd8a61f6753ecfea8426a564293fee0914271` | 306 / 306 / 0 | 2018-08-10 – 2019-05-19 | 0 | 0 | 2 |
| 2019/2020 | openfootball/europe/portugal/2019-20_pt1.txt | `0e57f8019ed50e449428fec2cad7fa8eb35bd868cbcbc7356eae4af9b678e013` | 306 / 306 / 0 | 2019-08-09 – 2020-07-26 | 2 | 2 | 2 |
| 2020/2021 | openfootball/europe/portugal/2020-21_pt1.txt | `381113f27961277c23f9bbc27543a263f6459236860cc3b9c0698e547ab64b12` | 306 / 306 / 0 | 2020-09-18 – 2021-05-19 | 4 | 4 | 0 |
| 2021/2022 | openfootball/europe/portugal/2021-22_pt1.txt | `5e5593b409d4b4ca31782960897b4e40917cc55370101cd68fea1af51a2a3b1c` | 306 / 306 / 0 | 2021-08-06 – 2022-05-15 | 2 | 3 | 3 |
| 2022/2023 | openfootball/europe/portugal/2022-23_pt1.txt | `fa7d1938a28199b2e714437769c4f56ac28f184e0f1ebdfd2603683c1a850a34` | 306 / 306 / 0 | 2022-08-05 – 2023-05-27 | 3 | 4 | 0 |
| 2023/2024 | openfootball/europe/portugal/2023-24_pt1.txt | `7f19ddec6033a465ffa1e76b70103aea3005b63c0d27e3f723d0924c814da511` | 306 / 306 / 0 | 2023-08-11 – 2024-05-18 | 2 | 0 | 1 |
| 2024/2025 | openfootball/europe/portugal/2024-25_pt1.txt | `3bb1acda8822a01e1aef1e70f03607650b97fb6722fd0d777f2ef9bf6544ed6c` | 306 / 306 / 0 | 2024-08-09 – 2025-05-17 | 2 | 0 | 0 |
| 2025/2026 | openfootball/europe/portugal/2025-26_pt1.txt | `967a4cde722b5598a5c28da8efa65a0ab28da9b1778cee74455b463216dd1adb` | 306 / 306 / 0 | 2025-08-08 – 2026-05-16 | 3 | 0 | 0 |

Modern dates are explicit day/month/weekday headings, with occasional explicit years. The remaining years are uniquely resolved within the source season using weekdays; the inventory retains both the original heading and date-basis classification. This is not an inferred round date or actual result-availability timestamp. The 2019/20 extension through July is explicitly preserved without assuming cancellation. Date precision counts per original are stored in the private source inventory.

## Complete source overlap and conflicts

All seven seasons from 2018/19 through 2024/25 have 306 one-to-one provisional correspondences: **2,142 overlap pairs**, zero unmatched observations in either source and zero score disagreements. Every comparison is exact-season-bound and preserves both original labels, physical lines, dates/scores and annotations. Eighteen explicit diagnostic label links are recorded per season; no global club alias or source-preference choice exists. Upstream independence remains unestablished.

| Season | Matched | Unmatched historical / modern | Date conflicts | Score conflicts |
|---|---:|---|---:|---:|
| 2018/2019 | 306 | 0 / 0 | 0 | 0 |
| 2019/2020 | 306 | 0 / 0 | 1 | 0 |
| 2020/2021 | 306 | 0 / 0 | 1 | 0 |
| 2021/2022 | 306 | 0 / 0 | 0 | 0 |
| 2022/2023 | 306 | 0 / 0 | 0 | 0 |
| 2023/2024 | 306 | 0 / 0 | 0 | 0 |
| 2024/2025 | 306 | 0 / 0 | 0 | 0 |

| Fixture | Historical date / physical line | Modern date / physical line | Both scores | Status |
|---|---|---|---|---|
| Santa Clara–Pacos Ferreira, 2019/2020 | 2020-02-01 / 7290 | 2020-02-02 / 298 | 2-1 | Preserve both; Phase 5 review |
| Santa Clara–Benfica, 2020/2021 | 2021-01-03 / 7532 | 2021-01-04 / 192 | 1-1 | Preserve both; Phase 5 review |

The Santa Clara–Paços de Ferreira conflict is the unchanged Phase 2 case. Santa Clara–Benfica is newly exposed by 2020/21 acquisition. Neither date is selected. Original scheduling, actual event date, continuation/postponement and effective availability require independent historical evidence.

### Belenenses SAD–Benfica

Both original observations remain bound: historical CSV line **7838**, modern 2021/22 TXT line **187**, date **2021-11-27**, score **0–7**. The modern HT is 0–7, and neither source provides an abandonment annotation. Reported match state, early termination, legally recognized result and administrative finality are distinct and remain undecided. Source agreement is not independent legal certification.

Preserved evidence leads from Phase 1: https://www.fpf.pt/DownloadDocument.ashx?id=20842 and https://www.fpf.pt/DownloadDocument.ashx?id=21435 . These are documentary/index leads, not newly downloaded documents or newly certified findings. No accepted-result, HOLD OUT or NOT PLAYED policy was assigned.

## Scheduling and deduplicated review inventory

All Phase 2 category bindings are preserved. Across all eight modern seasons there are **18 wide-round contexts / 162 members**, **13 source-order reversal pairs / 26 distinct endpoints**, and **eight unusual-score observations**. Historical unusual-score observations add 18, giving 26 source observations in that category; they can represent the same match in both sources.

| Season | Round | First / last source dates | Span days | Members |
|---|---|---|---:|---:|
| 2019/2020 | 1 | 2019-08-09 / 2019-09-08 | 30 | 9 |
| 2019/2020 | 9 | 2019-10-05 / 2019-10-31 | 26 | 9 |
| 2020/2021 | 1 | 2020-09-18 / 2020-10-28 | 40 | 9 |
| 2020/2021 | 12 | 2021-01-02 / 2021-01-21 | 19 | 9 |
| 2020/2021 | 14 | 2021-01-15 / 2021-02-17 | 33 | 9 |
| 2020/2021 | 7 | 2020-11-06 / 2020-12-01 | 25 | 9 |
| 2021/2022 | 13 | 2021-12-03 / 2022-01-03 | 31 | 9 |
| 2021/2022 | 16 | 2021-12-28 / 2022-01-13 | 16 | 9 |
| 2022/2023 | 14 | 2022-12-23 / 2023-02-09 | 48 | 9 |
| 2022/2023 | 20 | 2023-01-26 / 2023-02-13 | 18 | 9 |
| 2022/2023 | 25 | 2023-03-17 / 2023-04-05 | 19 | 9 |
| 2023/2024 | 20 | 2024-02-03 / 2024-04-16 | 73 | 9 |
| 2023/2024 | 3 | 2023-08-25 / 2023-09-09 | 15 | 9 |
| 2024/2025 | 24 | 2025-03-01 / 2025-03-28 | 27 | 9 |
| 2024/2025 | 8 | 2024-10-04 / 2024-12-19 | 76 | 9 |
| 2025/2026 | 1 | 2025-08-08 / 2025-09-23 | 46 | 9 |
| 2025/2026 | 16 | 2025-12-27 / 2026-01-11 | 15 | 9 |
| 2025/2026 | 26 | 2026-03-14 / 2026-04-29 | 46 | 9 |

Long rounds, reversals and unusual valid scores are diagnostics, not proof of error or grounds for exclusion. The existing nine Phase 2 wide rounds/81 members, five reversal pairs and seven modern unusual scores remain unchanged; new files add nine wide rounds, eight reversal pairs and one unusual modern score.

Deduplicated review queue: **207 source observations**, with overlapping category memberships:

| Category | Source observations |
|---|---:|
| KNOWN_ABANDONMENT_REQUIRES_REVIEW | 2 |
| SOURCE_DISAGREEMENT | 4 |
| SOURCE_FIELD_OR_LABEL | 1 |
| SOURCE_ORDER_REVERSAL | 26 |
| UNUSUAL_SCORE | 26 |
| WIDE_ROUND | 162 |

These category counts must not be added as distinct fixtures. The queue retains physical source bindings and original values. A separate complete literal identity inventory records per-source season participants and per-label source occurrences, preserving Belenenses/SAD, Benfica/Porto/Sporting senior/B sides, Vitória SC/FC, AVS/Aves, Gil Vicente/Boavista, União de Leiria, accents, abbreviations and historic continuity issues without normalization.

## Complete 36-season coverage matrix

Historical and modern observations are counted separately. Conditional distinct slots subtract only bijective same-season diagnostic overlaps; they are not screened, standardized, legally finalized or independently certified matches. The Feirense diagnostic is provisional, and date conflicts remain unresolved.

| Season | Expected clubs / slots | Historical observations | Modern observations | Overlap pairs | Conditional distinct sourced slots | Coverage |
|---|---|---:|---:|---:|---:|---|
| 1990/1991 | 20 / 380 | 0 | 0 | 0 | 0 | NO_APPROVED_DATED_SOURCE |
| 1991/1992 | 18 / 306 | 0 | 0 | 0 | 0 | NO_APPROVED_DATED_SOURCE |
| 1992/1993 | 18 / 306 | 0 | 0 | 0 | 0 | NO_APPROVED_DATED_SOURCE |
| 1993/1994 | 18 / 306 | 0 | 0 | 0 | 0 | NO_APPROVED_DATED_SOURCE |
| 1994/1995 | 18 / 306 | 306 | 0 | 0 | 306 | HISTORICAL_ONLY |
| 1995/1996 | 18 / 306 | 306 | 0 | 0 | 306 | HISTORICAL_ONLY |
| 1996/1997 | 18 / 306 | 306 | 0 | 0 | 306 | HISTORICAL_ONLY |
| 1997/1998 | 18 / 306 | 306 | 0 | 0 | 306 | HISTORICAL_ONLY |
| 1998/1999 | 18 / 306 | 306 | 0 | 0 | 306 | HISTORICAL_ONLY |
| 1999/2000 | 18 / 306 | 306 | 0 | 0 | 306 | HISTORICAL_ONLY |
| 2000/2001 | 18 / 306 | 306 | 0 | 0 | 306 | HISTORICAL_ONLY |
| 2001/2002 | 18 / 306 | 306 | 0 | 0 | 306 | HISTORICAL_ONLY |
| 2002/2003 | 18 / 306 | 306 | 0 | 0 | 306 | HISTORICAL_ONLY |
| 2003/2004 | 18 / 306 | 306 | 0 | 0 | 306 | HISTORICAL_ONLY |
| 2004/2005 | 18 / 306 | 306 | 0 | 0 | 306 | HISTORICAL_ONLY |
| 2005/2006 | 18 / 306 | 306 | 0 | 0 | 306 | HISTORICAL_ONLY |
| 2006/2007 | 16 / 240 | 240 | 0 | 0 | 240 | HISTORICAL_ONLY |
| 2007/2008 | 16 / 240 | 240 | 0 | 0 | 240 | HISTORICAL_ONLY |
| 2008/2009 | 16 / 240 | 240 | 0 | 0 | 240 | HISTORICAL_ONLY |
| 2009/2010 | 16 / 240 | 240 | 0 | 0 | 240 | HISTORICAL_ONLY |
| 2010/2011 | 16 / 240 | 240 | 0 | 0 | 240 | HISTORICAL_ONLY |
| 2011/2012 | 16 / 240 | 240 | 0 | 0 | 240 | HISTORICAL_ONLY |
| 2012/2013 | 16 / 240 | 240 | 0 | 0 | 240 | HISTORICAL_ONLY |
| 2013/2014 | 16 / 240 | 240 | 0 | 0 | 240 | HISTORICAL_ONLY |
| 2014/2015 | 18 / 306 | 306 | 0 | 0 | 306 | HISTORICAL_ONLY |
| 2015/2016 | 18 / 306 | 306 | 0 | 0 | 306 | HISTORICAL_ONLY |
| 2016/2017 | 18 / 306 | 306 | 0 | 0 | 306 | HISTORICAL_ONLY |
| 2017/2018 | 18 / 306 | 306 | 0 | 0 | 306 | HISTORICAL_ONLY |
| 2018/2019 | 18 / 306 | 306 | 306 | 306 | 306 | BOTH_SOURCES |
| 2019/2020 | 18 / 306 | 306 | 306 | 306 | 306 | BOTH_SOURCES |
| 2020/2021 | 18 / 306 | 306 | 306 | 306 | 306 | BOTH_SOURCES |
| 2021/2022 | 18 / 306 | 306 | 306 | 306 | 306 | BOTH_SOURCES |
| 2022/2023 | 18 / 306 | 306 | 306 | 306 | 306 | BOTH_SOURCES |
| 2023/2024 | 18 / 306 | 306 | 306 | 306 | 306 | BOTH_SOURCES |
| 2024/2025 | 18 / 306 | 306 | 306 | 306 | 306 | BOTH_SOURCES |
| 2025/2026 | 18 / 306 | 0 | 306 | 0 | 306 | MODERN_ONLY |

Verified accounting: **8,958 + 2,448 = 11,406 dated source observations; 11,406 − 2,142 = 9,264 conditional distinct sourced slots across 32 seasons**. The 36-season regular-slot expectation is **10,562**, with **1,298 expected slots lacking an approved dated source**. These are coverage numbers, not accepted-record totals.

The four missing seasons remain 1990/91–1993/94: 380 + 306 + 306 + 306 = 1,298 expected slots. The immutable RSSSF 1990/91 snapshot has 380 undated results; it is kept outside the dated-source inventory and cannot close the gap. Missing-source slots are not NOT PLAYED or definitive exclusions. No new early source was acquired.

## Schema, rights and chronological limitations

Future schema remains `match_id,date,league,season,home_team,away_team,home_goals,away_goals`, with proposed canonical `Primeira Liga`. ISO source days, starting-year season tokens, numeric full-time goals and exact home/away roles are compatible in principle. The inventory creates only source-audit identifiers, not final shared-schema match IDs or standardized CSVs. Score finality, date conflicts, label decisions and effective result availability require later phases. No prediction eligibility policy exists here.

Private access, technical completeness, historical independence, attribution, redistribution, commercial use and model-training permission remain separate. Historical README noncommercial/GPL metadata, OpenFootball CC0 for rights held and RSSSF page-specific copying conditions do not establish blanket upstream or training clearance. No Football-Data access, restriction bypass, application integration, evaluation or training occurred.

## Reproducibility and fresh tests

Commands (offline inventory after approved acquisition):

```sh
PYTHONPATH=src:. python -B scripts/collect_primeira_liga_history.py --init
PYTHONPATH=src:. python -B scripts/collect_primeira_liga_history.py
PYTHONPATH=src:. python -B scripts/inventory_primeira_liga_history.py
PYTHONPATH=src:. python -B scripts/verify_primeira_liga_inventory.py
```

Baseline creation is exclusive; reruns verify rather than overwrite. Eight Phase 3 inventories plus independent reconciliation reproduce byte-for-byte/SHA-identically. A separate process regenerated the eight inventories and all five frozen Phase 2 assessments in safe temporary storage. Both phases' independent reconciliations remained identical. No saved artifact was overwritten. Source receipts, pinned blobs, all previous baselines and 59 frozen Phase 2 entries pass. Cached Phase 3 acquisition made zero network requests and changed none of 71 existing non-test-log private files.

| Fresh test selection | Passed | Failures / errors / skips |
|---|---:|---|
| New Phase 3 synthetic tests | 37 | 0 / 0 / 0 |
| All focused Primeira Liga | 89 | 0 / 0 / 0 |
| Acquisition/importer selection | 707 | 0 / 0 / 0 |
| Non-UI | 1,928 | 0 / 0 / 0 |
| App/launcher | 7 | 0 / 0 / 0 |
| Full repository | 1,935 | 0 / 0 / 0 |

Selections overlap and are not additive. External Python 3.13.12 was reused with bounded process timeouts, bytecode/cache disabled and safe temporary pytest directories; original .venv unchanged and no installation. Tests cover exact acquisition scope, source checksums/blobs, source grammar, derived-field conflicts, season formats, lossless source bindings, diagnostic whitespace isolation, unknown stages, senior/reserve distinctions, access stops, immutable evidence and anomaly preservation. Logs/XML/status, hashes, original receipts and final verification remain private.

## Files and proposed Phase 4

New public files: scripts/collect_primeira_liga_history.py, scripts/inventory_primeira_liga_history.py, scripts/verify_primeira_liga_inventory.py, tests/test_primeira_liga_history.py and this report. PLANNING_LOG.md receives append-only measured findings. All Phase 2 public files remain byte-identical. Private additions include the three originals/receipts, Phase 3 protected baseline/acquisition manifest, eight named inventories, independent reconciliation, reproducibility report, verification_phase3 logs/XML/status and final receipt. No private data is tracked or staged.

Propose Phase 4 only after approval: comprehensive structural validation of all **11,406** dated observations across **32 represented seasons**, retaining seven overlap seasons and both date conflicts; independently test complete directed pairings, date/score/identity/stage/provenance integrity, the isolated Feirense hypothesis, all 207 review observations and 18 scheduling contexts. Keep RSSSF result-only evidence and the four-season gap separate. No source selection or historical decision should occur in Phase 4.

Separate early-period recommendation (not approved here): bounded metadata/permission research for 1990/91–1993/94 using official/club archives and legally accessible dated historical providers, followed by explicit sample approval. Preserve RSSSF for score corroboration, distinguish indexed from inspected evidence and do not bypass HTTP403 or infer dates.

Stop after Phase 3. Do not begin Phase 4, acquire other originals, screen/standardize records, assign dispositions, train/integrate data or stage/commit/push.
