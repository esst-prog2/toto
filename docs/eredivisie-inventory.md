# Dutch Eredivisie — Phase 3 acquisition and full research inventory

Date: 2026-11-23. Scope is acquisition and source-preserving inventory only, not Phase 4 structural certification or a final source-selection, correction, HOLD OUT, eligibility or standardization decision.

## Starting state and preservation

Branch `feature/data-collection`, HEAD `4f8c64433cf6168a06dbde0102e822ce6d2eeffa`. Existing Phase 2 public changes and both untracked .DS_Store files were preserved. The new baseline freezes 56 Phase 2 private/public entries and the full earlier planning-log prefix; nested checks preserve all 839 previous private / 207 tracked public files across ten completed competitions. No application or promotional worktree change, dependency installation or original .venv modification occurred.

## Exactly three new originals

Repository `openfootball/europe`, fixed revision `63df627f3c87ce71708f016522ea236cf74332c3`. Paths, blob identities and sizes were checked against the preserved pinned tree before acquisition. Each original was retrieved once with the bounded nonretrying request helper; no redirect, revision substitution, other season download or access failure occurred. Six Phase 2 originals and all notices/evidence remain unchanged.

| Original path | Bytes | Git blob SHA-1 | SHA-256 | Retrieval UTC |
|---|---:|---|---|---|
| `netherlands/2020-21_nl1.txt` | 24321 | `60762d0a8bbc3b62ea1199706caea7f929ec0a43` | `d33c10a4e39e17d0f4cafeff212cf85deecdc2fd3d9ab33d638df9132cfdb03e` | 2026-11-23T09:52:04.212345+00:00 |
| `netherlands/2021-22_nl1.txt` | 24355 | `6249665f226cf6259bfd2a9e72747295010394bb` | `d201613dcf5ff7ef3b1ede7c23ec7815ff3ad8c04d196c0fb047b54e37faef8f` | 2026-11-23T09:52:06.695361+00:00 |
| `netherlands/2022-23_nl1.txt` | 24367 | `23268303742116f940ca5d763e1ba9b54ab65bf6` | `06f98c12ae5154d547aebb7bf61984e082bbfef5aab7d3b8ea4bad4145735341` | 2026-11-23T09:52:09.078810+00:00 |

Exact URLs use `https://raw.githubusercontent.com/openfootball/europe/63df627f3c87ce71708f016522ea236cf74332c3/{original_path}` and are stored in `phase3_acquisition.json` and adjacent provenance receipts. Attribution, preserved licence notices, full byte hashes, Git blob IDs, retrieval timestamps and unresolved upstream/availability limitations accompany each file. Cached reuse made zero network requests and preserved all 65 then-existing private files byte-for-byte.

## Independent historical completeness assessment

The unchanged Holland original is `jalapic/engsoccerdata/data-raw/holland.csv`, revision `872c5c354161ace8408f3091b758c6af4cccca94`. Fresh CSV parsing and a separate raw verifier re-established 20,776 scored tier-1 observations in 69 seasons, 1956/57–2024/25. Its columns remain Date, Season, home, visitor, FT, hgoal, vgoal, tier. Only the 35 target-window seasons are retained as detailed Phase 3 historical inventory; earlier seasons have metadata only.

All 35 target seasons are present. Every ordinary season has 18 clubs, 306 scored observations and each directed home/away pairing exactly once. The exception is 2019/20, which has 18 clubs, 232 scored observations and 74 absent pairings. There are zero duplicate/conflicting historical pairings, malformed scores, invalid/out-of-season dates or unexplained extra observations. Thus 35 × 306 − 74 = 10,636 is supported season-by-season and by pairing sets, not merely an aggregate coincidence.

This establishes technical inventory completeness against the stated regular-season structure, not independent certification of every historical date/result. The CSV marks tier1 but has no explicit per-row stage field: no extra fixtures or foreign/lower-tier records are apparent, yet legal outcomes and historical stage correctness still require later review. Original dates are not certified result-availability timestamps.

## Complete 36-season source coverage matrix

H = historical CSV; M = modern OpenFootball. Values are source observations, not additive real-world matches. Unscored modern values below are explicitly source-marked cancelled, not final NOT PLAYED decisions. Every target season has 18 observed clubs in each present source. Expected regular-season slots are 306 for each target season; absent-source cells mean no rows in that source, not necessarily missing historical coverage.

| Season | Expected | H observed/scored | H absent pairings | M observed | M scored | M unscored | M absent pairings |
|---|---:|---|---:|---:|---:|---:|---:|
| 1990/1991 | 306 | 306/306 | 0 | — | — | — | — |
| 1991/1992 | 306 | 306/306 | 0 | — | — | — | — |
| 1992/1993 | 306 | 306/306 | 0 | — | — | — | — |
| 1993/1994 | 306 | 306/306 | 0 | — | — | — | — |
| 1994/1995 | 306 | 306/306 | 0 | — | — | — | — |
| 1995/1996 | 306 | 306/306 | 0 | — | — | — | — |
| 1996/1997 | 306 | 306/306 | 0 | — | — | — | — |
| 1997/1998 | 306 | 306/306 | 0 | — | — | — | — |
| 1998/1999 | 306 | 306/306 | 0 | — | — | — | — |
| 1999/2000 | 306 | 306/306 | 0 | — | — | — | — |
| 2000/2001 | 306 | 306/306 | 0 | — | — | — | — |
| 2001/2002 | 306 | 306/306 | 0 | — | — | — | — |
| 2002/2003 | 306 | 306/306 | 0 | — | — | — | — |
| 2003/2004 | 306 | 306/306 | 0 | — | — | — | — |
| 2004/2005 | 306 | 306/306 | 0 | — | — | — | — |
| 2005/2006 | 306 | 306/306 | 0 | — | — | — | — |
| 2006/2007 | 306 | 306/306 | 0 | — | — | — | — |
| 2007/2008 | 306 | 306/306 | 0 | — | — | — | — |
| 2008/2009 | 306 | 306/306 | 0 | — | — | — | — |
| 2009/2010 | 306 | 306/306 | 0 | — | — | — | — |
| 2010/2011 | 306 | 306/306 | 0 | — | — | — | — |
| 2011/2012 | 306 | 306/306 | 0 | — | — | — | — |
| 2012/2013 | 306 | 306/306 | 0 | — | — | — | — |
| 2013/2014 | 306 | 306/306 | 0 | — | — | — | — |
| 2014/2015 | 306 | 306/306 | 0 | — | — | — | — |
| 2015/2016 | 306 | 306/306 | 0 | — | — | — | — |
| 2016/2017 | 306 | 306/306 | 0 | — | — | — | — |
| 2017/2018 | 306 | 306/306 | 0 | — | — | — | — |
| 2018/2019 | 306 | 306/306 | 0 | 306 | 306 | 0 | 0 |
| 2019/2020 | 306 | 232/232 | 74 | 306 | 232 | 74 | 0 |
| 2020/2021 | 306 | 306/306 | 0 | 306 | 306 | 0 | 0 |
| 2021/2022 | 306 | 306/306 | 0 | 306 | 306 | 0 | 0 |
| 2022/2023 | 306 | 306/306 | 0 | 306 | 306 | 0 | 0 |
| 2023/2024 | 306 | 306/306 | 0 | 306 | 306 | 0 | 0 |
| 2024/2025 | 306 | 306/306 | 0 | 306 | 306 | 0 | 0 |
| 2025/2026 | 306 | No rows | — | 306 | 305 | 1 | 0 |

All eight modern files have exactly 306 observed slots and 18 clubs with complete directed pairings, zero duplicate/conflicting pairings, no invalid full-time scores, zero unexplained unscored observations and no other-stage records. Modern totals are 2,448 source observations: 2,373 scored and 75 annotated null-score observations. Combining historical and modern files produces 13,084 source observations, not 13,084 distinct matches: seven seasons overlap. No merged or accepted-record total is generated.

## 2019/20 cancellation reconciliation

The historical CSV contains 232 scored records, omitting 74 directed pairings. Under the explicit season-local Heracles/Heracles Almelo correspondence, all 232 link to modern scored observations with identical dates and scores. The 74 modern observations without a historical counterpart are precisely the 74 null-score `[cancelled]` observations. OpenFootball has no absent pairings; historical CSV absence is not an explicit cancelled row. No score was fabricated and no played match counted twice in coverage.

The preserved Phase 2 documentary evidence discusses termination, standings, no champion and no promotion/relegation; it does not approve blanket legal annulment of the 232 played results. No final screening policy was assigned.

## Complete source overlap and disagreements

Exact-label comparison and conditional season-local name hypotheses remain separate. Hypotheses are only diagnostic links; no source labels, canonical model identities or global aliases are changed. Agreement between repositories does not establish independent underlying evidence.

| Season | H records | M slots | Exact-label pairs | Conditional scored pairs | Date agreements/differences | Score agreements/differences | Unmatched H / M |
|---|---:|---:|---:|---:|---|---|---|
| 2018/2019 | 306 | 306 | 272 | 306 | 306 / 0 | 306 / 0 | 0 / 0 |
| 2019/2020 | 232 | 306 | 206 | 232 | 232 / 0 | 232 / 0 | 0 / 74 |
| 2020/2021 | 306 | 306 | 272 | 306 | 306 / 0 | 306 / 0 | 0 / 0 |
| 2021/2022 | 306 | 306 | 272 | 306 | 306 / 0 | 306 / 0 | 0 / 0 |
| 2022/2023 | 306 | 306 | 306 | 306 | 305 / 1 | 306 / 0 | 0 / 0 |
| 2023/2024 | 306 | 306 | 72 | 306 | 306 / 0 | 305 / 1 | 0 / 0 |
| 2024/2025 | 306 | 306 | 72 | 306 | 306 / 0 | 306 / 0 | 0 / 0 |

Across seven overlapping seasons: 2,068 conditionally matched scored fixtures, 2,067 exact date agreements, 2,067 exact score agreements, one date disagreement and one score disagreement. Zero unmatched historical scored observations; the 74 unmatched modern 2019/20 cancellation slots are explicitly retained. The historical CSV has no 2025/26 rows, so that season is outside cross-source comparison rather than an invented overlap gap.

| Fixture | Historical source date / FT / line | Modern source date / FT / line | Inventory treatment |
|---|---|---|---|
| FC Groningen–AFC Ajax | 2023-05-14 / 2-3 / 20147 | 2023-05-16 / 2-3 / 486 | Both unchanged; explicit source-bound review candidate |
| NEC Nijmegen–Vitesse | 2023-10-01 / 1-3 / 20223 | 2023-10-01 / 1-2 / 109 | Both unchanged; explicit source-bound review candidate |

NEC–Vitesse retains the Phase 2 club-report lead supporting investigation of the 1–3 versus 1–2 discrepancy. Groningen–Ajax has a newly discovered May 14 versus May 16 date disagreement with the same 2–3 score; this is a possible kickoff/completion distinction requiring Phase 5 evidence, not an approved correction. No new historical research or source-preference decision was made here.

Conditional label differences remain the same explicit Phase 2 hypotheses: Heracles/Heracles Almelo; AZ Alkmaar/AZ; Almere City/Almere City FC; FC Twente/FC Twente ’65; Feyenoord/Feyenoord Rotterdam; NEC Nijmegen/NEC; PSV Eindhoven/PSV; Vitesse/SBV Vitesse; sc Heerenveen/SC Heerenveen; Willem II/Willem II Tilburg. Every application is scoped to its particular season; exact matches are independently reported.

## Frozen interruption and NAC 2025/26 evidence

The queue verifies exact equality of every frozen documentary source observation against freshly parsed rows; original SHA, physical line, date, score and audit ID remain bound. The three 2023/24 records remain on reported completion dates: Ajax–Feyenoord 2023-09-27 0–4 (line 91), RKC–Ajax 2023-12-06 2–3 (line 228), AZ–NEC 2023-12-06 1–2 (line 223). Earlier event dates 2023-09-24, 2023-09-30 and 2023-10-29, evidence references/access limitations and unknown effective availability remain separate in the preserved documentary context.

NAC–Heerenveen remains source date 2026-05-10, line 509, null score and `[cancelled]`. The preserved club/narrative references report interruption at 2–0 and completion May 11 at 2–0, with NAC still the home-designated side despite the changed venue. This completion evidence is separate from the original source, with no result insertion, revised pin, supplemental dataset or definitive NOT PLAYED classification. It is an unresolved source-status/result-completeness case for Phase 5/6.

No administrative-publication/finality date or effective result availability was invented. Other wide rounds, reversals and unusual scores are only candidate indicators; later phases must investigate interruptions, postponements, administrative outcomes and source-date reliability without guessing from file order.

## Scheduling and review inventory

All source records remain distinct. The review queue contains 410 distinct source observations, not 410 distinct real-world fixtures. Categories overlap and must not be added. No category causes an exclusion.

| Category | Source observations |
|---|---:|
| CROSS_SOURCE_DATE_DISAGREEMENT | 2 |
| CROSS_SOURCE_SCORE_CONFLICT | 2 |
| CROSS_SOURCE_SCORE_DISAGREEMENT | 2 |
| KNOWN_INTERRUPTION_CONTEXT | 3 |
| SOURCE_ANNOTATION | 75 |
| SOURCE_CANCELLED_BUT_COMPLETION_REPORTED | 1 |
| SOURCE_ORDER_REVERSAL | 32 |
| SOURCE_UNSCORED | 75 |
| UNUSUAL_SCORE | 89 |
| WIDE_ROUND | 225 |

There are 25 modern wide-round contexts / 225 members, 16 physical-order reversal pairs / 32 endpoints, and 89 unusual-score observations across both sources (74 historical + 15 modern), with overlapping copies explicitly preserved. Source-marker cancellation flags are observations, not final historical statuses. Repeated round headings are preserved as scheduling structure rather than assumed duplicated fixtures.

| Modern season | Wide rounds | Reversal pairs | Repeated round headings |
|---|---:|---:|---|
| 2018/2019 | 1 | 3 | {} |
| 2019/2020 | 2 | 2 | {} |
| 2020/2021 | 3 | 3 | {} |
| 2021/2022 | 4 | 4 | {} |
| 2022/2023 | 1 | 4 | {} |
| 2023/2024 | 3 | 0 | {"10": 2, "3": 3, "7": 2} |
| 2024/2025 | 7 | 0 | {"17": 2, "20": 2, "23": 2, "25": 2, "3": 2, "31": 2, "4": 2, "5": 2} |
| 2025/2026 | 4 | 0 | {"16": 2, "18": 2, "20": 2, "3": 3} |

### All wide-round spans

| Season | Round | Earliest source date | Latest source date | Days | Members |
|---|---|---|---|---:|---:|
| 2018/2019 | 11 | 2018-11-02 | 2018-12-06 | 34 | 9 |
| 2019/2020 | 22 | 2020-02-07 | 2020-04-09 | 62 | 9 |
| 2019/2020 | 4 | 2019-08-24 | 2019-09-26 | 33 | 9 |
| 2020/2021 | 1 | 2020-09-12 | 2020-12-27 | 106 | 9 |
| 2020/2021 | 21 | 2021-02-05 | 2021-04-22 | 76 | 9 |
| 2020/2021 | 4 | 2020-10-02 | 2020-10-21 | 19 | 9 |
| 2021/2022 | 2 | 2021-08-20 | 2021-12-02 | 104 | 9 |
| 2021/2022 | 23 | 2022-02-19 | 2022-04-16 | 56 | 9 |
| 2021/2022 | 25 | 2022-03-05 | 2022-04-19 | 45 | 9 |
| 2021/2022 | 4 | 2021-09-11 | 2021-12-01 | 81 | 9 |
| 2022/2023 | 25 | 2023-03-11 | 2023-04-19 | 39 | 9 |
| 2023/2024 | 10 | 2023-10-27 | 2023-12-06 | 40 | 9 |
| 2023/2024 | 3 | 2023-08-26 | 2023-11-02 | 68 | 9 |
| 2023/2024 | 7 | 2023-09-30 | 2023-12-06 | 67 | 9 |
| 2024/2025 | 17 | 2024-12-20 | 2025-01-28 | 39 | 9 |
| 2024/2025 | 20 | 2025-01-24 | 2025-02-23 | 30 | 9 |
| 2024/2025 | 25 | 2025-03-07 | 2025-04-02 | 26 | 9 |
| 2024/2025 | 3 | 2024-08-24 | 2024-09-18 | 25 | 9 |
| 2024/2025 | 31 | 2025-04-19 | 2025-05-04 | 15 | 9 |
| 2024/2025 | 4 | 2024-08-30 | 2024-10-30 | 61 | 9 |
| 2024/2025 | 5 | 2024-09-14 | 2024-12-04 | 81 | 9 |
| 2025/2026 | 16 | 2025-12-13 | 2026-01-21 | 39 | 9 |
| 2025/2026 | 18 | 2026-01-10 | 2026-02-11 | 32 | 9 |
| 2025/2026 | 20 | 2026-01-24 | 2026-02-11 | 18 | 9 |
| 2025/2026 | 3 | 2025-08-23 | 2025-09-24 | 32 | 9 |

## Identity, dates and future schema

Across target source inventories there are 47 literal club labels. The source-local label occurrence registry preserves each spelling, source and season. NEC/N.E.C., RKC, NAC, Zwolle, Den Haag, SVV/Dordrecht histories and senior/reserve distinctions remain review subjects; N.E.C. is an evidence label rather than an automatically substituted source label. No Jong/reserve labels were found in this population, which does not authorize merging senior and reserve identities elsewhere.

No global casefold, punctuation, predecessor/successor or cross-league alias was implemented. Raw home/away labels, starting-year season tokens, ISO dates, numeric full-time scores, annotations, source hashes, revisions and blob identities support the eventual eight-column schema with canonical Eredivisie. Per-source audit hashes remain immutable source identities, not final standardized match IDs.

Historical CSV tier1 has no explicit stage metadata; modern files explicitly identify regular-season rounds. Source day headings have validated weekday/season year resolution, but neither parseability, source order nor repository agreement certifies actual completion/availability. No eligibility logic or standardized projections were produced in Phase 3.

## Reproducibility and tests

Fresh independent raw verification checked the full historical CSV season inventory, all 10,636 target historical row bindings and all 2,448 modern observations using a separate parser through temporary read-only source links. All five frozen Phase 2 derived outputs and its independent reconciliation regenerate unchanged before inventory construction.

A separate subprocess regenerated all five Phase 3 inventories in safe temporary storage; each matched bytes and SHA-256.

| Output | Bytes | SHA-256 |
|---|---:|---|
| `phase3_coverage_matrix.json` | 146706 | `55e88202b1192dafa9ef14952d2e2f3d03695ebbe66f62042c891919c0cc1431` |
| `phase3_historical_inventory.json` | 16498810 | `9be643516bc93c87692a022e10e9e3a41bd4639eeec34117f392c5bc59b053f9` |
| `phase3_modern_inventory.json` | 3639606 | `11baec58fb3b906523787be3ffc7952e85231098846e76ca7f9e1eb406627986` |
| `phase3_overlap_registry.json` | 2090454 | `1a57c5be34ed8b60c44fd193b775aa89e9ea679728b559ed37224b9b36320e2c` |
| `phase3_review_candidates.json` | 753135 | `74803a01a8e52309de802d4b9b912f90add890f9a84b7593aa56ecb310f99473` |

Fresh bounded runs used the preserved external Python 3.13.12 environment, with bytecode and pytest caches disabled:

| Scope | Passed | Failed | Errors | Skipped |
|---|---:|---:|---:|---:|
| All Eredivisie (27 new Phase 3 cases + 48 Phase 2) | 75 | 0 | 0 | 0 |
| Acquisition/importer-related selection | 556 | 0 | 0 | 0 |
| Non-UI repository regressions | 1,627 | 0 | 0 | 0 |
| App/launcher | 7 | 0 | 0 | 0 |
| Complete repository | 1,634 | 0 | 0 | 0 |

Runs overlap; do not add their totals. Logs, XML, statuses and reproduction/cache receipts are private. Source hashes, all new blob identities, frozen Phase 2 evidence and earlier competition baselines pass. Git HEAD/staging state remain unchanged and all detailed private artifacts remain ignored/untracked. Whitespace/privacy checks are recorded in the final verification receipt.

```sh
PYTHONPATH=. python -B scripts/collect_eredivisie_history.py --init-only
PYTHONPATH=. python -B scripts/collect_eredivisie_history.py
PYTHONPATH=. python -B scripts/inventory_eredivisie_history.py
```

Cached valid originals are never re-downloaded; partial pairs or receipt/blob mismatches fail explicitly. Inventory entry points compare existing outputs and refuse changed bytes rather than overwrite. No Phase 2 or earlier competition file was overwritten.

## Files, restrictions and Phase 4 proposal

Public changes are `scripts/collect_eredivisie_history.py`, `scripts/inventory_eredivisie_history.py`, `tests/test_eredivisie_history.py`, this report and append-only PLANNING_LOG entries. Private changes comprise three originals/receipts, acquisition manifest, frozen baseline, five inventories and verification receipts/logs. All nine physical source originals (six reused + three new) remain under the ignored Eredivisie area. No other source files were downloaded.

Technical completeness, historical accuracy/independence, private acquisition permission, redistribution permission and model-training permission remain separate. Historical noncommercial-attribution and GPL package notices do not establish every data right; OpenFootball CC0 does not warrant all upstream rights. Redistribution and training clearance remain unresolved. No application integration or model training is authorized.

Proposed Phase 4 scope: comprehensively validate all 36 target seasons while retaining 10,636 historical and 2,448 modern source observations separately; use explicit diagnostic links for the 2,068 scored overlaps, preserving all 410 source review candidates and both disagreements. Verify season/stage/round structures, directed pairings, fields, literal identities, provenance and chronology without selecting a preferred source or certifying history. Carry NAC 2025/26, 2019/20 cancellation semantics, all interruption context, unusual scores and identity risks into later evidence/policy phases. No accepted match total, final HOLD OUT, source preference or standardized CSV exists yet.

Phase 3 stops for approval; Phase 4 has not begun.
