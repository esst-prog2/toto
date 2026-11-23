# Eredivisie — Phase 4 independent structural validation

Completed 2026-11-23 in the original toto worktree on `feature/data-collection`, HEAD `4f8c64433cf6168a06dbde0102e822ce6d2eeffa`. Phase 4 only: no acquisition, historical adjudication, source preference, corrections, eligibility decisions or standardization.

## Method and immutable inputs

`validate_eredivisie_structure.py` independently parses original bytes with its own CSV/text grammar, rather than using the Phase 2/3 fixture parsers. It checks exact CSV columns/tier, modern title/stage/round grammar, weekday/calendar/year resolution, required fields, scores/FT/HT, goal-derived H/D/A, season boundaries, literal labels/encoding, directed pairs, duplicate/conflicting pairs, same-day club collisions, round coverage, source-order reversals and wide rounds. Each observation binds revision, Git blob, SHA-256, physical line range, physical bytes and deterministic source-observation audit ID. Every original field is reconciled against frozen Phase 3 records. Season-local diagnostic correspondences are used only for comparison, never to rewrite identities.

The historical original at jalapic/engsoccerdata revision `872c5c354161ace8408f3091b758c6af4cccca94` contains 20,776 scored tier-1 observations across 69 seasons, 1956/57–2024/25. All are retained and individually field-checked. Its target subset is 10,636 observations across 35 seasons. Eight OpenFootball/europe files at `63df627f3c87ce71708f016522ea236cf74332c3` contain 2,448 slots: 2,373 scored and 75 unscored. All nine originals and receipts remain unchanged.

## Season-level target results

All target seasons have 18 literal clubs and 306 expected directed pairings. H = historical source; M = modern source; cells show scored / unscored observations. A dash means no acquired source for that window, not missing fixtures. Modern files have all 306 pairings and rounds 1–34 with nine slots per round, including cancelled slots. No target duplicate/conflicting within-source pairs, same-day club collisions, malformed score/date fields, round-structure failures or other-stage records were detected.

| Season | H scored / null | M scored / null | Expected slots | Structural result |
|---|---:|---:|---:|---|
| 1990/1991 | 306 / 0 | — | 306 | Complete pairings; valid fields |
| 1991/1992 | 306 / 0 | — | 306 | Complete pairings; valid fields |
| 1992/1993 | 306 / 0 | — | 306 | Complete pairings; valid fields |
| 1993/1994 | 306 / 0 | — | 306 | Complete pairings; valid fields |
| 1994/1995 | 306 / 0 | — | 306 | Complete pairings; valid fields |
| 1995/1996 | 306 / 0 | — | 306 | Complete pairings; valid fields |
| 1996/1997 | 306 / 0 | — | 306 | Complete pairings; valid fields |
| 1997/1998 | 306 / 0 | — | 306 | Complete pairings; valid fields |
| 1998/1999 | 306 / 0 | — | 306 | Complete pairings; valid fields |
| 1999/2000 | 306 / 0 | — | 306 | Complete pairings; valid fields |
| 2000/2001 | 306 / 0 | — | 306 | Complete pairings; valid fields |
| 2001/2002 | 306 / 0 | — | 306 | Complete pairings; valid fields |
| 2002/2003 | 306 / 0 | — | 306 | Complete pairings; valid fields |
| 2003/2004 | 306 / 0 | — | 306 | Complete pairings; valid fields |
| 2004/2005 | 306 / 0 | — | 306 | Complete pairings; valid fields |
| 2005/2006 | 306 / 0 | — | 306 | Complete pairings; valid fields |
| 2006/2007 | 306 / 0 | — | 306 | Complete pairings; valid fields |
| 2007/2008 | 306 / 0 | — | 306 | Complete pairings; valid fields |
| 2008/2009 | 306 / 0 | — | 306 | Complete pairings; valid fields |
| 2009/2010 | 306 / 0 | — | 306 | Complete pairings; valid fields |
| 2010/2011 | 306 / 0 | — | 306 | Complete pairings; valid fields |
| 2011/2012 | 306 / 0 | — | 306 | Complete pairings; valid fields |
| 2012/2013 | 306 / 0 | — | 306 | Complete pairings; valid fields |
| 2013/2014 | 306 / 0 | — | 306 | Complete pairings; valid fields |
| 2014/2015 | 306 / 0 | — | 306 | Complete pairings; valid fields |
| 2015/2016 | 306 / 0 | — | 306 | Complete pairings; valid fields |
| 2016/2017 | 306 / 0 | — | 306 | Complete pairings; valid fields |
| 2017/2018 | 306 / 0 | — | 306 | Complete pairings; valid fields |
| 2018/2019 | 306 / 0 | 306 / 0 | 306 | Complete pairings; valid fields |
| 2019/2020 | 232 / 0 | 232 / 74 | 306 | 74 absent H pairings; 74 explicit M null cancellations |
| 2020/2021 | 306 / 0 | 306 / 0 | 306 | Complete pairings; valid fields |
| 2021/2022 | 306 / 0 | 306 / 0 | 306 | Complete pairings; valid fields |
| 2022/2023 | 306 / 0 | 306 / 0 | 306 | Complete pairings; valid fields |
| 2023/2024 | 306 / 0 | 306 / 0 | 306 | Complete pairings; valid fields |
| 2024/2025 | 306 / 0 | 306 / 0 | 306 | Complete pairings; valid fields |
| 2025/2026 | — | 305 / 1 | 306 | One M null cancellation; reported completion unresolved |

Across the target window: **13,084 source observations**, **13,009 score-bearing**, **75 result-incomplete**, **zero individually malformed observations**, and **zero unexplained null scores** under the source annotation check. A source-marked cancellation explains a null field structurally; it does not establish that no match was eventually played. There are 410 flagged source observations and 12,674 without the listed review flags; flagged does not mean erroneous. Null scores are structurally valid fixture slots, not completed results.

Outside the target window, the independent whole-file check detected two PEC Zwolle observations on 1980-02-13 (1979/80), IDs `2069c2194d674d2eb7b90d06fe74794bad2e1d1c2e8cbb46e9bcf79cee49f3c6` and `8138529f63e7decc87e1b07ca411c470699cc753d4868b8877dabf15bdabd3f8`. This is a season-level same-day collision, despite individually valid fields. Both remain in the full historical assessment; no correction or target-queue expansion is made. Historical 1962/63–1965/66 have 16 clubs/240 expected pairings; other complete historical seasons have 18/306. The CSV lacks an explicit stage column; pairing completeness and tier 1 support structural scope but do not independently certify historical competition classification.

## Overlap and exceptional observations

Seven seasons yield **2,068 conditionally matched scored pairs**. Under the explicitly scoped diagnostic correspondences, 13,009 scored source observations minus 2,068 overlapping observations equals **10,941 conditional scored fixture identities**. Adding 75 unscored slots yields **11,016 conditional slots**, matching 36 × 306. These are inventory identities, not accepted or historically certified counts. Upstream independence remains unestablished.

* Groningen–Ajax 2022/23: historical 2023-05-14 versus modern 2023-05-16, both 2–3. Both dates are syntactically valid; neither is selected. A two-day difference could reflect event semantics, but Phase 4 does not verify that explanation.
* NEC–Vitesse 2023/24: historical 1–3 versus modern 1–2 on 2023-10-01. Both scores parse; the conflict is preserved in both observations. No authoritative score is chosen.
* 2019/20: historical 232 scored observations leave 74 absent directed pairs. Those identities match exactly the modern 74 explicitly cancelled/null slots. Absence and a cancellation annotation are distinct source representations, not two sets of unplayed fixtures or a final legal disposition.
* NAC–Heerenveen 2025/26: modern line 509 retains 2026-05-10, null score and `[cancelled]`. Frozen evidence separately reports completion on 2026-05-11, 2–0. No score supplementation, correction, HOLD OUT or NOT PLAYED decision is implemented.
* Ajax–Feyenoord, RKC–Ajax and AZ–NEC 2023/24 retain frozen interruption context: initial kickoff dates 2023-09-24, 2023-09-30 and 2023-10-29, respectively; modern source dates 2023-09-27, 2023-12-06 and 2023-12-06. Preserved documentary leads are not newly inspected independent evidence in this phase.

## Review queue and chronology

The private queue retains all **410 deduplicated source-observation entries**, with zero lost or newly added target entries. It is not 410 distinct real-world matches. Every entry retains original fields, source-bound ID, structural assessment and any frozen documentary context. Categories overlap:

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

The two score-conflict category names describe the same two observations, not four. Wide rounds intersect reversal endpoints in 11 observations, unscored slots in two, unusual scores in two, interruption contexts in two and the score-conflict pair in one. The machine-readable category combinations provide the complete deduplication breakdown.

All **25 wide-round contexts / 225 members** and **16 source-order reversal pairs / 32 endpoints** are independently rederived. These are scheduling review signals, not structural errors or exclusion rules. The full fixture identities and earliest/latest dates are in each season report and queue.

| Season | Round | First source date | Last source date | Span days |
|---|---:|---|---|---:|
| 2018/2019 | 11 | 2018-11-02 | 2018-12-06 | 34 |
| 2019/2020 | 4 | 2019-08-24 | 2019-09-26 | 33 |
| 2019/2020 | 22 | 2020-02-07 | 2020-04-09 | 62 |
| 2020/2021 | 1 | 2020-09-12 | 2020-12-27 | 106 |
| 2020/2021 | 4 | 2020-10-02 | 2020-10-21 | 19 |
| 2020/2021 | 21 | 2021-02-05 | 2021-04-22 | 76 |
| 2021/2022 | 2 | 2021-08-20 | 2021-12-02 | 104 |
| 2021/2022 | 4 | 2021-09-11 | 2021-12-01 | 81 |
| 2021/2022 | 23 | 2022-02-19 | 2022-04-16 | 56 |
| 2021/2022 | 25 | 2022-03-05 | 2022-04-19 | 45 |
| 2022/2023 | 25 | 2023-03-11 | 2023-04-19 | 39 |
| 2023/2024 | 3 | 2023-08-26 | 2023-11-02 | 68 |
| 2023/2024 | 7 | 2023-09-30 | 2023-12-06 | 67 |
| 2023/2024 | 10 | 2023-10-27 | 2023-12-06 | 40 |
| 2024/2025 | 3 | 2024-08-24 | 2024-09-18 | 25 |
| 2024/2025 | 4 | 2024-08-30 | 2024-10-30 | 61 |
| 2024/2025 | 5 | 2024-09-14 | 2024-12-04 | 81 |
| 2024/2025 | 17 | 2024-12-20 | 2025-01-28 | 39 |
| 2024/2025 | 20 | 2025-01-24 | 2025-02-23 | 30 |
| 2024/2025 | 25 | 2025-03-07 | 2025-04-02 | 26 |
| 2024/2025 | 31 | 2025-04-19 | 2025-05-04 | 15 |
| 2025/2026 | 3 | 2025-08-23 | 2025-09-24 | 32 |
| 2025/2026 | 16 | 2025-12-13 | 2026-01-21 | 39 |
| 2025/2026 | 18 | 2026-01-10 | 2026-02-11 | 32 |
| 2025/2026 | 20 | 2026-01-24 | 2026-02-11 | 18 |

All historical dates are explicit ISO fields. Modern day/month headings are explicit; omitted years are resolved using season boundaries and weekday agreement, not assumed to be independently verified full dates. No target historical January 1/July 1 anchor dates were found; this does not rule out other date proxies. No invalid dates or target boundary violations were detected. Source-order reversals do not imply chronological result availability.

Audit chronology keeps source/heading dates distinct from actual kickoff, completion, administrative publication/finality and effective availability. Actual event/availability fields remain null pending evidence/policy. The cancelled-slot `scheduled_date` is only its source heading date, not a verified scheduling fact. Frozen documentary dates remain separate evidence leads. No training chronology or screening policy is authorized.

There are 47 literal target labels; no within-season NFC/casefold collisions were detected. Exact spellings, accents and seasonal diagnostic links remain visible. Cross-season identity/continuity questions (including Den Haag, Zwolle, Dordrecht/SVV-related labels) require evidence, not global aliases. Reserve-team equivalence is not inferred.

## Reproducibility, tests and preservation

Fresh tests used the previously established external temporary Python 3.13.12 environment, without installs or changes to the original `.venv`. Bytecode and pytest cache writes into the project were disabled; tests had bounded process-group timeouts. Runs overlap and must not be added:

| Run | Passed | Failed/errors/skipped |
|---|---:|---|
| acquisition_importer | 556 | 0/0/0 |
| app_launcher | 7 | 0/0/0 |
| eredivisie | 115 | 0/0/0 |
| full | 1674 | 0/0/0 |
| non_ui | 1667 | 0/0/0 |

The structural test file adds 40 synthetic cases covering malformed grammar, wrong competition/stage, ambiguous dates, source binding tampering, score contradictions, null-result semantics, duplicate/missing pairings, scheduling signals, literal identities and append-only protection.

A fresh independent invocation rebuilt all four assessment objects into a separate temporary directory and compared saved bytes and SHA-256 values; all matched:

| Artifact | SHA-256 |
|---|---|
| phase4_historical_structure.json | `1863e6f88332da3deec0dadd36173bf9665037917886e8cebc62521c4fc03984` |
| phase4_modern_structure.json | `5a6872aad9e736de55c9f3577cbc6e65e418af9dfe19b29579ab027cdb5c95e2` |
| phase4_overlap_reconciliation.json | `2929860fc1f90d64ce5747b40ca18c6fc6dd550adaccdad37f6a74df2b3fef81` |
| phase4_review_queue.json | `61846d54dbf3b88bd366a5657d61c37a960a621ad35cceada5863f22b6314207` |

Reproduce without acquisition:

```sh
PYTHONPATH=. python -B scripts/validate_eredivisie_structure.py
PYTHONPATH=src:. PYTHONDONTWRITEBYTECODE=1 python -B -m pytest tests/test_eredivisie_structure.py -q -p no:cacheprovider
```

The CLI compares existing outputs and refuses changed bytes rather than overwriting them. Private baseline verification protects 839 previous private files / 207 public files, 56 frozen Phase 2 entries and 86 Phase 2/3 entries, plus the planning-log prefix. All original hashes, receipts and provenance bindings pass. Git HEAD and index remain unchanged. No prior competition, application or promotional file was changed. Detailed sources, reports, queue, tests/logs and receipts remain Git-ignored.

Public Phase 4 work consists only of `scripts/validate_eredivisie_structure.py`, `tests/test_eredivisie_structure.py`, this report and appended `PLANNING_LOG.md` lines. Private additions: `phase4_protected_before.json`, four assessment JSON files, `phase4_reproducibility.json`, `phase4_test_summary.json`, `verification_phase4/` logs/XML/status and the final verification receipt.

## Phase 5 evidence priorities and restrictions

Requires separate approval: resolve both cross-source conflicts; investigate NAC completion versus the pinned cancellation; independently verify the three interruption timelines; review the 25 wide rounds, 16 reversal pairs, unusual scores and team-identity questions; select reproducible ordinary-season historical samples. Preserve 2019/20 absence/cancellation semantics and investigate actual result-availability where relevant. No historical case has been newly certified by structural completeness.

Technical structure, historical confidence, source independence, redistribution permission and model-training permission remain separate. Historical noncommercial-attribution/provenance notices and GPL package licensing do not establish all data rights; OpenFootball CC0 does not warrant every upstream right. Redistribution and training clearance remain unresolved. No standardized output or application integration exists for this phase. Stop after Phase 4 for approval.
