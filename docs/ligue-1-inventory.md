# Ligue 1 — Phase 3 acquisition and source inventory

Date: 2026-11-22. Original `toto` worktree, `feature/data-collection`, HEAD `81225118ced664f113c19b87cff8095b0333ccda`. Phase 3 only. See [frozen Phase 2 feasibility](ligue-1-feasibility.md).

## Outcome and scope

**Seven new ordinary-season originals acquired; five ordinary originals reused; twelve modern seasons inventoried.** Modern inventory contains **4,338 scheduled/source fixture slots, 4,237 score-bearing observations and 101 explicitly cancelled slots**, with zero other-stage records in the inspected files. This is an inventory, not Phase 4 comprehensive validation, historical certification, eligibility approval or standardization. No corrections, exclusions or model training occurred.

The 36-season 1990/91–2025/26 target remains incomplete. The proposed older window contains 8,369 rows across 23 of 24 season labels, missing 1994/95 and one 2006/07 directed pairing. Counting disjoint intended source windows gives **12,707 observations across 35 represented target seasons**, including 101 cancelled slots. These are not accepted/model-training counts. Overlapping historical CSV observations and the 2025/26 full file are not added a second time.

## Protection and pinned provenance

All **558 prior private files and 165 tracked public files** remain SHA-256-identical. A new `phase3_protected_before.json` also freezes **52 Phase 2 entries** (48 private files and four public implementation/documentation files), plus the complete Phase 2 planning-log prefix. No earlier evidence or report was rewritten. Application and previous standardized outputs remain unchanged.

OpenFootball Europe pin: **`63df627f3c87ce71708f016522ea236cf74332c3`**. The retained, receipt-checked recursive Git tree establishes all seven exact blob paths before requests. Reused notices remain pinned `README.md`, `LICENSE.md`, `france/README.md`, `france/NOTES.md`. The historical CSV remains pinned to `872c5c354161ace8408f3091b758c6af4cccca94`.

New requests were limited to seven approved ordinary files, with 30-second timeout, 8 MB response cap, two-second spacing, no redirects/retries and a persistent access-stop guard. Per-file receipts preserve exact URL/path/revision, season/competition, UTC timestamp, original filename, size, SHA-256, Git blob SHA-1, attribution and qualified rights/notices. A network-disabled rerun verified all seven cached originals plus five reused ordinary receipts without downloads. No Football-Data or other unapproved dataset access.

| Acquired original path in `openfootball/europe` | Bytes | SHA-256 | Git blob SHA-1 |
|---|---:|---|---|
| `france/2015-16_fr1.txt` | 30,104 | `1bc5d4ca32bbff4845fb848480cd9da278b2b9d730dd636f409aefb5ad083ad3` | `4bfa47245c36d78fb727fa575c0e9a1edbd82be1` |
| `france/2017-18_fr1.txt` | 30,081 | `44697ffbe26524c4538e28def6597722479a26ab06f6c63dc1df83d322f5a343` | `0ed604f62f558b3e003e16615dece3372bf8cc2e` |
| `france/2018-19_fr1.txt` | 30,221 | `664c8be6445cee6268ac15fd95a559ad6e232d50d47a759b54a8264db8b7d6d1` | `55930b9d70a4598c41e89f254c6989f83d68e110` |
| `france/2020-21_fr1.txt` | 30,017 | `40f8e3575843933c43d7e6941ae6543475900917878b437d5105b6602926dd73` | `eb24aad43b9c61dc8a644bdd711fa44120550a56` |
| `france/2021-22_fr1.txt` | 29,988 | `a534c4c765b3dfcaed072e6f2bd32513f542f2c84fb61ce44ad24c067ed7984f` | `56f1e5148c5ac41cd4b2739fed50a7b47d6c3ffc` |
| `france/2022-23_fr1.txt` | 29,882 | `bfb04c9b90a8aff058e7631d740f5c9c4d968025a1c14d752c6261cbfd1828aa` | `228ab677025f2b47d101ca3c373bcdb8dfa1a8b2` |
| `france/2024-25_fr1.txt` | 24,519 | `169b86f635d04fefb786cf8e644e57d21bbd5c1dcc36ca1f1469560c699af19b` | `ef156ebbb27cd5b66a2b6f1175df88d95ef41aad` |

Exact source URLs are `https://raw.githubusercontent.com/openfootball/europe/63df627f3c87ce71708f016522ea236cf74332c3/{original_path}`. All seven raw-byte SHA-256, size and Git blob checks passed, and aggregate receipts match individual receipts. Five reused ordinary seasons are 2014/15, 2016/17, 2019/20, 2023/24 and 2025/26. The historical CSV and sixth Phase 2 OpenFootball original (`2025-26_fr1-full.txt`) are retained unchanged; the latter is supporting evidence, not a thirteenth season.

## Complete modern inventory

| Season | Observed slots | Score-bearing | Unscored | Expected scheduled / played | Clubs | Other stage | Missing pairs | Duplicates | Wide rounds |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2014/2015 | 380 | 380 | 0 | 380 / 380 | 20 | 0 | 0 | 0 | 3 |
| 2015/2016 | 380 | 380 | 0 | 380 / 380 | 20 | 0 | 0 | 0 | 3 |
| 2016/2017 | 380 | 380 | 0 | 380 / 380 | 20 | 0 | 0 | 0 | 5 |
| 2017/2018 | 380 | 380 | 0 | 380 / 380 | 20 | 0 | 0 | 0 | 3 |
| 2018/2019 | 380 | 380 | 0 | 380 / 380 | 20 | 0 | 0 | 0 | 5 |
| 2019/2020 | 380 | 279 | 101 | 380 / 279 | 20 | 0 | 0 | 0 | 4 |
| 2020/2021 | 380 | 380 | 0 | 380 / 380 | 20 | 0 | 0 | 0 | 6 |
| 2021/2022 | 380 | 380 | 0 | 380 / 380 | 20 | 0 | 0 | 0 | 4 |
| 2022/2023 | 380 | 380 | 0 | 380 / 380 | 20 | 0 | 0 | 0 | 1 |
| 2023/2024 | 306 | 306 | 0 | 306 / 306 | 18 | 0 | 0 | 0 | 3 |
| 2024/2025 | 306 | 306 | 0 | 306 / 306 | 18 | 0 | 0 | 0 | 1 |
| 2025/2026 | 306 | 306 | 0 | 306 / 306 | 18 | 0 | 0 | 0 | 2 |

All twelve files have complete literal directed home/away pairings and unique source observations; no within-file conflicting pairings, missing scored-goal values, invalid goal syntax, FT/goal discrepancies, noncanonical dates, normalized-name collisions or same-team/date collisions were observed. Counts are measured from fixtures, not copied from advertised headers. Numeric score-bearing includes administrative representations and is **not** the same as independently verified completed on-field matches.

All inspected stages are regular season. Repeated round headings retain rescheduled fixture blocks and are not extra fixtures/stages. Full physical lines, literal record strings, score/halftime strings, comments, annotations, source commit/SHA/blob and dates are retained in the private inventory and originals. UTF-8/accents and CRLF/LF originals are preserved.

### Date precision

| Season | Explicit day/month | Explicit year | Season/weekday-resolved year | Inferred day/month | Ambiguities | First–last source date |
|---|---:|---:|---:|---:|---:|---|
| 2014/2015 | 380 | 4 | 376 | 0 | 0 | 2014-08-08–2015-05-23 |
| 2015/2016 | 380 | 2 | 378 | 0 | 0 | 2015-08-07–2016-05-14 |
| 2016/2017 | 380 | 12 | 368 | 0 | 0 | 2016-08-12–2017-05-20 |
| 2017/2018 | 380 | 2 | 378 | 0 | 0 | 2017-08-04–2018-05-19 |
| 2018/2019 | 380 | 16 | 364 | 0 | 0 | 2018-08-10–2019-05-24 |
| 2019/2020 | 380 | 12 | 368 | 0 | 0 | 2019-08-09–2020-05-23 |
| 2020/2021 | 380 | 15 | 365 | 0 | 0 | 2020-08-21–2021-05-23 |
| 2021/2022 | 380 | 4 | 376 | 0 | 0 | 2021-08-06–2022-05-21 |
| 2022/2023 | 380 | 7 | 373 | 0 | 0 | 2022-08-05–2023-06-03 |
| 2023/2024 | 306 | 2 | 304 | 0 | 0 | 2023-08-11–2024-05-19 |
| 2024/2025 | 306 | 2 | 304 | 0 | 0 | 2024-08-16–2025-05-17 |
| 2025/2026 | 306 | 2 | 304 | 0 | 0 | 2025-08-15–2026-05-17 |

Across 4,338 slots, all day/month headings are explicit; 80 fixture dates inherit an explicitly written year and 4,258 have a year uniquely resolved from season and weekday. No day/month is invented. These are **source headings**, including cancelled scheduled dates, not certified actual kickoff, completion or effective-result dates. The 2019/20 last source date is a cancelled scheduled slot, not the final played match.

### Preserved 2019/20 reconciliation

Independent raw extraction confirms **380 slots = 279 scored + 101 `[cancelled]`**. One cancelled fixture is Strasbourg–PSG in round 28; the remaining 100 are rounds 29–38. Scored dates run 2019-08-09–2020-03-08. All cancellation strings and scheduled dates remain in the inventory. No result was manufactured or automatically marked an ordinary missing result.

Frozen Phase 2 reference **L1-E01**, the [LFP board minutes of 30 April 2020](https://www.lfp.fr/assets/20200430_PV_Conseil_Administration_LFP_e824a457fa.pdf), page 9, establishes 279 of 380 fixtures played. The retained ledger identifies direct PDF inspection and the aggregate scope of that evidence; no claim that it certifies each fixture individually. The 279 scored historical CSV observations agree with the OpenFootball scored subset under explicit diagnostic correspondences.

## Older proposed source window: complete inventory

Historical original: `jalapic/engsoccerdata/data-raw/france.csv`, 29,558 score-bearing rows over 85 literal season-start labels, 1932–2024. Missing labels between endpoints remain 1937, 1939–1944 and 1994. No earlier coverage extension is authorized, and no actual-season relabelling is inferred from source labels.

| Source season | Observed / scored | Expected | Literal clubs | Missing literal directed pairs | Result-label contradictions |
|---|---:|---:|---:|---:|---:|
| 1990/1991 | 380 / 380 | 380 | 21 | 40 | 57 |
| 1991/1992 | 380 / 380 | 380 | 20 | 0 | 71 |
| 1992/1993 | 380 / 380 | 380 | 20 | 0 | 74 |
| 1993/1994 | 380 / 380 | 380 | 20 | 0 | 66 |
| 1994/1995 | 0 / 0 | 380 | 0 | 0 | 0 |
| 1995/1996 | 380 / 380 | 380 | 20 | 0 | 74 |
| 1996/1997 | 380 / 380 | 380 | 20 | 0 | 87 |
| 1997/1998 | 306 / 306 | 306 | 18 | 0 | 77 |
| 1998/1999 | 306 / 306 | 306 | 18 | 0 | 65 |
| 1999/2000 | 306 / 306 | 306 | 18 | 0 | 66 |
| 2000/2001 | 306 / 306 | 306 | 18 | 0 | 72 |
| 2001/2002 | 306 / 306 | 306 | 18 | 0 | 61 |
| 2002/2003 | 380 / 380 | 380 | 20 | 0 | 88 |
| 2003/2004 | 380 / 380 | 380 | 20 | 0 | 96 |
| 2004/2005 | 380 / 380 | 380 | 20 | 0 | 71 |
| 2005/2006 | 380 / 380 | 380 | 20 | 0 | 92 |
| 2006/2007 | 379 / 379 | 380 | 20 | 1 | 82 |
| 2007/2008 | 380 / 380 | 380 | 20 | 0 | 97 |
| 2008/2009 | 380 / 380 | 380 | 20 | 0 | 103 |
| 2009/2010 | 380 / 380 | 380 | 20 | 0 | 104 |
| 2010/2011 | 380 / 380 | 380 | 20 | 0 | 93 |
| 2011/2012 | 380 / 380 | 380 | 20 | 0 | 93 |
| 2012/2013 | 380 / 380 | 380 | 20 | 0 | 102 |
| 2013/2014 | 380 / 380 | 380 | 20 | 0 | 104 |

- **1994/95:** the whole 380-fixture season is absent. No new older dataset acquired.
- **2006/07:** 379 rows; missing `FC Nantes`–`Toulouse FC`. Retained Phase 2 club context describes an administrative event; no date/result supplement or decision made.
- **1990/91:** 380 rows but 21 literal labels, with Brest split between `Brest Armorique FC` and `Stade Brest`. The 40 apparent missing pairings are label-level diagnostics, not 40 proven missing fixtures. No alias applied.
- All 8,369 older-window rows have numeric goals and ISO-formatted dates within the conventional 1990–2013 source-season windows. This does not establish historically correct dates or legal results.
- `tier`/`division` cannot establish stage: the CSV has no explicit stage/round field. Historical formats and identity continuity remain open review questions.

## Bounded diagnosis of the result-label discrepancy

Independent raw CSV contingency analysis gives:

| Source period | Rows | Goal-derived H / source H | Goal-derived D / source D | Goal-derived A / source D | Goal-derived A / source A |
|---|---:|---:|---:|---:|---:|
| Labels 1932–2014 (before 2015/16) | 26,007 | 13,661 | 6,857 | **5,489** | 0 |
| Labels 2015–2024 | 3,551 | 1,547 | 910 | 0 | 1,094 |

The pattern is systematic: **every goal-derived away win before 2015/16 is labelled `D`**, while home wins and draws retain matching labels. From 2015/16 onward all derived labels agree with the numeric goals. The 1990/91–2013/14 proposed window contains 1,895 of these contradictions. The exact upstream code/version cause is **not established**; an observed pattern is not proof of a particular programming mistake.

For all 29,558 rows, FT string, home/away goals, goal sum and goal difference agree internally. No numerical corruption was detected by those internal checks; that does **not** prove historical numerical accuracy. The 2014/15 comparison corroborates numeric values across the two compiled files, whose independence remains unestablished. The separate Bastia–Lyon numerical disagreement persists. Administrative decisions can also differ from goal-derived outcomes even when no technical label mismatch is present.

Before any later use: sample genuinely independent dated match records across seasons/outcomes, review numerical outliers and official exceptional decisions, resolve team/date issues, then obtain explicit processing-policy approval. This phase neither rewrites source `result` nor substitutes derived labels into a dataset.

### Broader-source date anomalies

All **1,162** out-of-window source dates are preserved:

| Source label | Count |
|---|---:|
| 1932/1933 | 182 |
| 1933/1934 | 240 |
| 1934/1935 | 240 |
| 1935/1936 | 240 |
| 1936/1937 | 240 |
| 1946/1947 | 10 |
| 1967/1968 | 10 |

The first five groups (1,142 rows) are concentrated on 1 July immediately beyond the conventional season boundary. The other 20 rows belong to source labels 1946 and 1967. All dates are syntactically valid ISO dates; historical accuracy/proxy/season-label semantics are unverified. No date, season or historical format was repaired. Full lines, dates and fixtures are retained in the machine-readable diagnosis.

## Source overlap and club identity

| Scored season overlap | Unique matched pairs | Date/score discrepancies | Unmatched historical / modern pairs |
|---|---:|---:|---:|
| 2014/2015 | 380 | 0 | 0 / 0 |
| 2015/2016 | 342 | 0 | 38 / 38 |
| 2016/2017 | 380 | 1 | 0 / 0 |
| 2017/2018 | 380 | 0 | 0 / 0 |
| 2018/2019 | 380 | 0 | 0 / 0 |
| 2019/2020 | 279 | 0 | 0 / 0 |
| 2020/2021 | 380 | 0 | 0 / 0 |
| 2021/2022 | 380 | 0 | 0 / 0 |
| 2022/2023 | 380 | 0 | 0 / 0 |
| 2023/2024 | 306 | 0 | 0 / 0 |
| 2024/2025 | 306 | 0 | 0 / 0 |

The approved 2014/15 comparison and five non-identical name correspondences remain byte-equivalent to Phase 2: Saint-Étienne/Saint-Etienne, Olympique Lyonnais/Olympique Lyon, Stade Rennais/Stade Rennes, Stade de Reims/Stade Reims, Évian/Evian Thonon Gaillard. These and other previously inspected spelling/abbreviation correspondences are used only in explicit season-level diagnostic comparisons. No source name is rewritten, and no global identity mapping is applied.

**New 2015/16 identity conflict:** the CSV uses **`AC Ajaccio`** while the ordinary OpenFootball file uses **`Gazélec FC Ajaccio`**. These must not be treated as spelling variants or merged. There are 342 matched pairings with agreeing dates/goals, and **38 unmatched pairings on each side** involving these distinct labels. Independent club/season identity verification is needed before deciding which source values are correct. No mapping or correction has been proposed as approved.

**2016/17 numerical conflict:** Bastia–Lyon is CSV 0–3 versus OpenFootball 0–0 `[awarded]`, both source-dated 2017-04-16. All other matched sample observations agree; that is source consistency evidence, not independent historical certification.

The combined literal-label catalogue contains 105 labels across the retained historical file and modern originals. Accent/case/punctuation similarity produces three string-candidate groups (Saint-Étienne, Évian and Nîmes). This is not a club identity registry: dissimilar names can represent continuity, and similar names can represent different clubs. Preserve Paris FC/PSG, historical Toulouse entities, Ajaccio clubs, Brest and reconstituted clubs until evidence supports a season-scoped treatment.

## Scheduling, administrative results and chronological uncertainty

All **17 Phase 2 wide-round candidates** remain unchanged. Seven new files add **23**, giving **40 round flags covering 394 unique fixture slots**. Fixtures belonging to multiple diagnostic categories are not separate source observations. One cancelled 2019/20 round-31 span reflects scheduled dates only. A long span is not automatically an error; interruption, replay and administrative-date questions remain later-phase work.

| Season | Round | First–last source date | Span (days) |
|---|---:|---|---:|
| 2014/2015 | 14 | 2014-11-21–2015-01-07 | 47 |
| 2014/2015 | 25 | 2015-02-13–2015-04-07 | 53 |
| 2014/2015 | 32 | 2015-04-10–2015-04-28 | 18 |
| 2015/2016 | 9 | 2015-10-02–2015-11-04 | 33 |
| 2015/2016 | 27 | 2016-02-19–2016-03-09 | 19 |
| 2015/2016 | 35 | 2016-04-22–2016-05-11 | 19 |
| 2016/2017 | 16 | 2016-12-02–2017-04-05 | 124 |
| 2016/2017 | 17 | 2016-12-10–2017-01-18 | 39 |
| 2016/2017 | 21 | 2017-01-20–2017-02-21 | 32 |
| 2016/2017 | 24 | 2017-02-07–2017-03-01 | 22 |
| 2016/2017 | 31 | 2017-03-31–2017-05-17 | 47 |
| 2017/2018 | 8 | 2017-09-29–2017-11-20 | 52 |
| 2017/2018 | 24 | 2018-02-02–2018-02-20 | 18 |
| 2017/2018 | 31 | 2018-03-14–2018-04-04 | 21 |
| 2018/2019 | 17 | 2018-12-08–2019-02-20 | 74 |
| 2018/2019 | 18 | 2018-12-15–2019-03-12 | 87 |
| 2018/2019 | 23 | 2019-02-01–2019-02-20 | 19 |
| 2018/2019 | 27 | 2019-03-02–2019-04-09 | 38 |
| 2018/2019 | 28 | 2019-03-09–2019-04-17 | 39 |
| 2019/2020 | 12 | 2019-11-01–2020-01-15 | 75 |
| 2019/2020 | 15 | 2019-11-29–2020-01-15 | 47 |
| 2019/2020 | 16 | 2019-12-03–2020-01-15 | 43 |
| 2019/2020 | 31 | 2020-04-05–2020-04-22 | 17 |
| 2020/2021 | 1 | 2020-08-21–2020-09-17 | 27 |
| 2020/2021 | 8 | 2020-10-23–2020-11-25 | 33 |
| 2020/2021 | 9 | 2020-10-31–2021-01-20 | 81 |
| 2020/2021 | 11 | 2020-11-20–2021-02-17 | 89 |
| 2020/2021 | 21 | 2021-01-22–2021-02-24 | 33 |
| 2020/2021 | 22 | 2021-01-29–2021-03-10 | 40 |
| 2021/2022 | 3 | 2021-08-20–2021-10-27 | 68 |
| 2021/2022 | 14 | 2021-11-19–2022-02-01 | 74 |
| 2021/2022 | 19 | 2021-12-22–2022-01-19 | 28 |
| 2021/2022 | 20 | 2022-01-07–2022-01-26 | 19 |
| 2022/2023 | 2 | 2022-08-12–2022-09-07 | 26 |
| 2023/2024 | 8 | 2023-10-06–2023-11-29 | 54 |
| 2023/2024 | 10 | 2023-10-27–2023-12-06 | 40 |
| 2023/2024 | 12 | 2023-11-10–2023-12-07 | 27 |
| 2024/2025 | 16 | 2024-12-18–2025-01-05 | 18 |
| 2025/2026 | 26 | 2026-03-13–2026-04-22 | 40 |
| 2025/2026 | 29 | 2026-04-10–2026-05-13 | 33 |

The two source-marked administrative results are Bastia–Lyon (2016/17, 0–0 `[awarded]`) and **Montpellier–Saint-Étienne (2024/25, 2025-03-16, 0–2 `[awarded]`, source line 394)**. They are counted as score-bearing observations, not certified ordinary played results. Other exceptional fixtures are unannotated, so absence of a marker never proves ordinary status.

| Preserved case | Source values retained | Evidence and availability limits |
|---|---|---|

| Bastia–Lyon 2016/17 | CSV line 26714: 2017-04-16, 0–3; ordinary text line 533: same date, 0–0 `[awarded]` | Conflicting numerical/administrative representations remain unresolved; do not turn an awarded winner into a draw or invent an administrative score. Phase 2 primary/secondary access limitations preserved. |

| Nantes–Bastia 2013/14 | CSV line 25254: 2013-08-10, 0–0 | Retained judicial evidence confirms penalty defeat for Nantes and victory for Bastia; inspected passages do not establish numerical administrative score or earliest availability. |

| Nice–Marseille 2021/22 | CSV line 28297 and modern line 55: 2021-10-27, 1–1 | Replay after August interruption; distinguish original event from replay. No kickoff-date substitution or finality policy. |

| Montpellier–Clermont 2023/24 | Modern line 204: 2023-11-29, 1–1 | Retained LFP order concerns October 8 interruption and replay; preserve October 25 decision separately. Full replay-result/finality certification still later work. |

| Nantes–Toulouse 2025/26 | Modern line 890: 2026-05-17, 0–0; full version unchanged | Retained official decision ratifies 0–0 on 2026-05-27, after abandonment. May 17 must not silently become certified final-result availability; appeal scope remains separately unverified. |

| Montpellier–Saint-Étienne 2024/25 | Modern line 394: 2025-03-16, 0–2 `[awarded]` | Newly acquired source-marked case. Actual interruption/completion/decision dates and finality require independent evidence. No policy applied. |

| Nantes–Toulouse 2006/07 | Missing CSV directed pairing | Retained retrospective club context only; no guessed match date/result or invented source row. |

All twelve Phase 2 documentary references, exact URLs, document dates, access classifications and limitations are carried unchanged through the inventory’s `documentary_context` object. Its SHA-256 binds the frozen ledger. No new historical certification or exclusion policy is introduced. High scores and all affected fixture lines remain visible in the detailed assessment.

## Verification and reproducibility

**22 new synthetic tests passed; all 57 Ligue 1 focused tests passed. All 1,132 repository tests passed, including all seven app/launcher tests.** Full suite: 13.20 seconds pytest time, 14.26 seconds process wall time. Tests used the previously established offline Python 3.13.12 environment outside iCloud; pytest 9.1.1 and pandas 3.0.6, no installs/upgrades or original `.venv` changes. Cache/test output remained outside the project, with bytecode writes disabled.

Independent raw extraction (separate implementation) reconciled every modern source line/date/pairing/score/round and every historical CSV row/count against the inventory; per-file hashes, sizes and Git blobs were independently recalculated. It reconfirmed 4,338/4,237/101 modern totals, 8,369 older-window observations, 5,489 label contradictions and 1,162 unusual dates.

Fresh-process regeneration into a safe temporary directory is **byte-identical and SHA-256-identical** to saved `phase3_inventory.json`: **5,418,782 bytes**, SHA-256 **`9e824e5fa7cd0034da33b00600eeb2ef63949da376699f4910b69b227ed99882`**. Phase 2 assessment also regenerates byte-identically: SHA-256 `4b330225e14188a82018faa74f7aca5a181992bfa81d7836fbd91c5ec2541a42`. No original/output overwritten.

Reproduction, using a working project-compatible Python and `PYTHONPATH=src:.`, `PYTHONDONTWRITEBYTECODE=1`:

```sh
python -B -m scripts.inventory_ligue1_history --check
python -B -m pytest tests/test_ligue1_feasibility.py tests/test_ligue1_history.py -q -p no:cacheprovider
```

Serialize `inventory_ligue1_history.build()` with `collect_ligue1_feasibility.encode()` to a new temporary path for a separate-location comparison. The acquisition script’s `--init` creates the protection baseline; cached acquisition is idempotent and fails on partial/tampered receipts. Never retry an access-stopped bundle without investigation.

## Technical suitability, rights and stopping point

| Classification | Phase 3 status |
|---|---|
| Modern technical inventory | Twelve ordinary seasons accounted for; 101 explicitly cancelled slots kept separate from score-bearing observations. |
| Older technical inventory | 23/24 target labels represented, absent season and fixture, identity and derived-label issues remain explicit. |
| Historical reliability | No population certification; administrative and chronology cases need independent review. Source agreement does not establish independent lineage. |
| Redistribution | Unresolved upstream/dataset scope; originals remain private. OpenFootball CC0 covers rights held, not all possible upstream rights. engsoccerdata README noncommercial statement and GPL package metadata remain qualified. |
| Model training | **Not cleared; no model trained.** Technical counts are not training suitability or permission. |

Public Phase 3 changes only: `scripts/collect_ligue1_history.py`, `scripts/inventory_ligue1_history.py`, `tests/test_ligue1_history.py`, this document, and append-only `PLANNING_LOG.md`. Phase 2 public files are unchanged. All private source/evidence files remain Git-ignored and unstaged. New private artifacts comprise seven originals/seven receipts, Phase 3 protected baseline, acquisition manifest, inventory, independent verification receipt, test/helper evidence and final verification/file inventory. Full exact names/hashes are in `phase3_final_verification.json`. The promotional worktree was not accessed.

## Recommended Phase 4 and remaining acquisition

For separate approval, comprehensively structurally validate the acquired **12,707 target-window source observations**: 8,369 older-window CSV rows plus 4,338 modern text slots. Explicitly retain the absent 1994/95 season and missing 2006/07 pairing; validate 35 represented seasons without pretending the 36-season target is complete. Keep all 101 cancelled slots and administrative results as source observations, with no eligibility decision yet.

Phase 4 should independently reconstruct pairings/stages, dates, scores, source-line/hash bindings, fixture-level anomaly overlaps and identity risks; preserve all 40 round flags, the 2015/16 Ajaccio conflict, historical Brest split, result-label pattern, broader-source 1,162 date anomalies and known administrative/replay cases. Keep the 2025/26 full original as corroborating detail, not another fixture population. Earlier-than-1990 rows remain diagnostic evidence outside the proposed primary window.

To reach the full 36-season target, **1994/95 still needs an explicitly approved dated source and rights assessment**. Metadata research or author/official-archive permission enquiries can precede any acquisition; no restricted Football-Data access, repackaged mirror circumvention or extra download is authorized here. The missing 2006/07 fixture needs independently dated primary evidence and later explicit supplementation/exception approval. None of these gaps may be filled speculatively.

No standardization, historical correction/exclusion policy, application change, training, staging, commit, push or merge. Stop after Phase 3 for user approval.
