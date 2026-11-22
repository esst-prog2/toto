# Segunda División — Phase 6 decision and exception policy

Decision record: 2026-11-22. Original `toto` worktree, `feature/data-collection`, unchanged HEAD `052d25185182f1edbb80fac51cafbb59e0acf7cf`. This phase formalizes approved evidence-bound processing metadata and provisional eligibility only. No source data, prior report, standardized CSV, complete Phase 7 audit archive or application path is changed. Phase 5 evidence remains immutable; see [historical review](segunda-division-historical-review.md).

## Independent provisional reconciliation

| Measure | Observed policy result |
| --- | --- |
| Source observations | 6006 |
| Original score-bearing observations | 5997 |
| Original blank scores (still blank) | 9 |
| Explicit decision cases | 34 |
| User-approved decisions | 33 |
| Additional proposed conditional decision | 1 |
| Evidence-backed supplements | 9 |
| Screened candidates, not standardized | 5984 |
| Approved unresolved Reus holds | 21 |
| Proposed Deportivo conditional hold | 1 |
| Standardized rows / trained models / cleared licenses | 0 / 0 / 0 |

Measured reconciliation: **5,975 original score-bearing candidates + nine supplements + 21 unresolved Reus holds + one proposed Deportivo hold = 6,006 observations**. The result is **5,984 candidates**, not the 5,985 no-additional-holds scenario. The one-record difference is explicit and attributable solely to the proposed conditional Deportivo hold. No additional record is dropped, inferred or silently corrected. Candidate status is a technical exception-policy classification, not historical certification or training clearance.

| Season | Observations | Candidates | Unresolved holds | Conditional holds | Supplements within candidates |
| --- | --- | --- | --- | --- | --- |
| 2012/2013 | 462 | 462 | 0 | 0 | 0 |
| 2013/2014 | 462 | 462 | 0 | 0 | 0 |
| 2014/2015 | 462 | 462 | 0 | 0 | 0 |
| 2015/2016 | 462 | 462 | 0 | 0 | 0 |
| 2016/2017 | 462 | 462 | 0 | 0 | 0 |
| 2017/2018 | 462 | 462 | 0 | 0 | 0 |
| 2018/2019 | 462 | 441 | 21 | 0 | 0 |
| 2019/2020 | 462 | 461 | 0 | 1 | 0 |
| 2020/2021 | 462 | 462 | 0 | 0 | 0 |
| 2021/2022 | 462 | 462 | 0 | 0 | 0 |
| 2022/2023 | 462 | 462 | 0 | 0 | 0 |
| 2023/2024 | 462 | 462 | 0 | 0 | 0 |
| 2024/2025 | 462 | 462 | 0 | 0 | 9 |

The assessment loops over the frozen 6,006 source observations; counts are derived from decisions rather than forced to the proposed total. No full per-fixture Phase 7 export is generated.

## Nine approved score supplements

All nine are `USER_APPROVED_PHASE6`, `SUPPLEMENT_MISSING_SCORE`. Decisions require the exact pinned source path, SHA-256, commit, physical line, audit ID, original team labels/date, blank original FT/goals and matching Phase 5 directly corroborated result. The original source FT remains null. The policy result is additive metadata, never an overwrite of the original observation. The approved effective calendar date is the independently corroborated playing/completion date; results are unavailable for predictions on that same day or earlier.

| Decision | 2024/25 source line | Fixture | Original FT | Approved supplement | Effective date |
| --- | --- | --- | --- | --- | --- |
| SD6-26 | 745 | Málaga CF — Burgos CF | blank | 2-2 | 2025-05-31 |
| SD6-27 | 747 | SD Huesca — CD Eldense | blank | 3-2 | 2025-06-01 |
| SD6-28 | 748 | UD Almería — CD Tenerife | blank | 2-0 | 2025-06-01 |
| SD6-29 | 749 | FC Cartagena — CD Mirandés | blank | 1-3 | 2025-06-01 |
| SD6-30 | 750 | Deportivo La Coruña — Elche CF | blank | 0-4 | 2025-06-01 |
| SD6-31 | 751 | Real Oviedo — Cádiz CF | blank | 2-1 | 2025-06-01 |
| SD6-32 | 752 | Levante UD — SD Eibar | blank | 1-0 | 2025-06-01 |
| SD6-33 | 753 | Racing Santander — Granada CF | blank | 2-1 | 2025-06-01 |
| SD6-34 | 754 | Córdoba CF — Albacete | blank | 1-1 | 2025-06-01 |

Eight cases bind the inspected [LaLiga round 42 results](https://www.laliga.com/en-BR/laliga-hypermotion/results/2024-25/gameweek-42); Córdoba–Albacete binds the [contemporary authored report](https://cordopolis.eldiario.es/deportes/ccf/noche-aplausos-poste-empate-cerrar-telon-arcangel_129_12347871.html). The policy pins the saved document metadata and historical claim hashes, not a moving web response. Fresh source replacement or additional acquisition remains unauthorized. Missing, changed, ambiguous or conflicting corroboration fails closed.

## Twenty-one approved Reus holds

Every source-marked second-half Reus award has an explicit `USER_APPROVED_PHASE6`, `UNRESOLVED_HOLD_OUT` decision. Preserve source date, 1–0/0–1 string, goal fields, `[awarded]` annotation, raw source line and provenance in any future audit archive. No on-field policy result or effective availability day is assigned. January 28, 2019 is recorded only as the common expulsion decision; no individual award-decision day, kickoff, completion or result-availability date is inferred. The dates below remain **source proxies**, not certified dates of administrative availability.

| Decision | 2018/19 source line | Source date proxy | Fixture | Source award | Policy |
| --- | --- | --- | --- | --- | --- |
| SD6-03 | 376 | 2019-01-19 | CF Reus Deportiu — UD Las Palmas | 0-1 | UNRESOLVED HOLD OUT |
| SD6-04 | 401 | 2019-01-27 | Albacete — CF Reus Deportiu | 1-0 | UNRESOLVED HOLD OUT |
| SD6-05 | 419 | 2019-02-03 | CF Reus Deportiu — Elche CF | 0-1 | UNRESOLVED HOLD OUT |
| SD6-06 | 430 | 2019-02-09 | Gimnàstic de Tarragona — CF Reus Deportiu | 1-0 | UNRESOLVED HOLD OUT |
| SD6-07 | 453 | 2019-02-17 | CF Reus Deportiu — UD Almería | 0-1 | UNRESOLVED HOLD OUT |
| SD6-08 | 469 | 2019-02-24 | Granada CF — CF Reus Deportiu | 1-0 | UNRESOLVED HOLD OUT |
| SD6-09 | 483 | 2019-03-03 | CF Reus Deportiu — CD Tenerife | 0-1 | UNRESOLVED HOLD OUT |
| SD6-10 | 501 | 2019-03-10 | CD Lugo — CF Reus Deportiu | 1-0 | UNRESOLVED HOLD OUT |
| SD6-11 | 518 | 2019-03-17 | CF Reus Deportiu — Deportivo La Coruña | 0-1 | UNRESOLVED HOLD OUT |
| SD6-12 | 536 | 2019-03-24 | Extremadura UD — CF Reus Deportiu | 1-0 | UNRESOLVED HOLD OUT |
| SD6-13 | 554 | 2019-03-31 | CF Reus Deportiu — Cádiz CF | 0-1 | UNRESOLVED HOLD OUT |
| SD6-14 | 573 | 2019-04-07 | RCD Mallorca — CF Reus Deportiu | 1-0 | UNRESOLVED HOLD OUT |
| SD6-15 | 591 | 2019-04-14 | CF Reus Deportiu — Real Oviedo | 0-1 | UNRESOLVED HOLD OUT |
| SD6-16 | 608 | 2019-04-21 | Real Zaragoza — CF Reus Deportiu | 1-0 | UNRESOLVED HOLD OUT |
| SD6-17 | 626 | 2019-04-28 | CF Reus Deportiu — AD Alcorcón | 0-1 | UNRESOLVED HOLD OUT |
| SD6-18 | 641 | 2019-05-05 | Córdoba CF — CF Reus Deportiu | 1-0 | UNRESOLVED HOLD OUT |
| SD6-19 | 660 | 2019-05-12 | CA Osasuna — CF Reus Deportiu | 1-0 | UNRESOLVED HOLD OUT |
| SD6-20 | 676 | 2019-05-19 | CF Reus Deportiu — Málaga CF | 0-1 | UNRESOLVED HOLD OUT |
| SD6-21 | 695 | 2019-05-26 | CD Numancia — CF Reus Deportiu | 1-0 | UNRESOLVED HOLD OUT |
| SD6-22 | 711 | 2019-06-02 | CF Reus Deportiu — Sporting Gijón | 0-1 | UNRESOLVED HOLD OUT |
| SD6-23 | 733 | 2019-06-09 | Rayo Majadahonda — CF Reus Deportiu | 1-0 | UNRESOLVED HOLD OUT |

Individual finality and earliest availability were not established in Phase 5. The expulsion notice, reported one-goal-loss policy and later legal reporting do not close those individual gaps. All 21 are barred from future screened output until a separately approved, evidence-backed policy version replaces the hold. A runtime waiver, scheduled fixture day or blanket administrative score substitution is not allowed.

## Special playing dates and unusual scores

**SD6-01 — CA Osasuna — RCD Mallorca**, 2014/2015, source line 82, 6-4. RETAIN_UNUSUAL_SCORE.

User-approved unchanged retention; effective playing day **2014-09-21**. Directly corroborated unusual result: no score cap, replacement or automatic outlier correction. The fixture’s original score remains identical.

**SD6-02 — CD Numancia — CD Lugo**, 2014/2015, source line 291, 6-6. RETAIN_UNUSUAL_SCORE.

User-approved unchanged retention; effective playing day **2014-12-20**. Directly corroborated unusual result: no score cap, replacement or automatic outlier correction. The fixture’s original score remains identical.

**SD6-24 — Rayo Vallecano — Albacete**, 2019/2020, source line 346, 1-0. COMPLETED_INTERRUPTED_MATCH.

Approved: preserve original kickoff/suspension **2019-12-15** and completion **2020-06-10**. Use June 10 as the played 1–0 result’s effective calendar day. The source already records June 10, so no source date correction occurs. Evidence binds RFEF appeal expediente 276-2019/20, June 3 resumption notice and Rayo’s completion account. No outcome can enter an earlier or same-day prediction window.

**SD6-25 — Deportivo La Coruña — CF Fuenlabrada**, 2019/2020, source line 722, 2-1. CONDITIONAL_HOLD_OUT.

**Agent-proposed conservative hold, awaiting user review; not an approved permanent exclusion.** Preserve the verified **2020-08-07, 2–1 played result**, original July 20 scheduled date, intermediate August 5 plan and actual August 7 playing/completion date. The operative disciplinary closure/finality documents and earliest final administrative availability were not directly established. Secondary reports support closure, but cannot justify silently certifying its exact timing. The provisional assessment therefore uses `CONDITIONAL_HOLD_OUT_PENDING_REVIEW`, with **no effective result date**. Phase 7 must retain the hold unless the user explicitly approves a source-bound alternative, supported by suitable evidence. This is uncertainty about finality/availability, not evidence that 2–1 is wrong.

The policy has **zero source-score overwrites and zero source-date corrections**. Nine independent supplements and two explicitly separated interrupted/postponed histories are retained as metadata. Verified playing facts and ultimate legal/administrative finality are distinct classifications.

## Identity policy

| Preserved source label | Affected observations | Seasons | Reviewed related labels | Keep separate from parent |
| --- | --- | --- | --- | --- |
| Athletic Club B | 42 | 2015/2016 | Bilbao Athletic | Athletic Club |
| FC Barcelona B | 168 | 2012/2013, 2013/2014, 2014/2015, 2017/2018 | Barça B / Barça Atlètic | FC Barcelona |
| Real Madrid Castilla | 84 | 2012/2013, 2013/2014 | Castilla / Real Madrid B | Real Madrid |
| Real Sociedad B | 42 | 2021/2022 | Sanse | Real Sociedad |
| Sevilla Atlético | 84 | 2016/2017, 2017/2018 | Sevilla Atlético / Sevilla FC B | Sevilla FC |
| Villarreal CF B | 84 | 2022/2023, 2023/2024 | Villarreal B | Villarreal CF |

Preserve all six reserve labels exactly; never merge parent and reserve histories. The six groups cover 498 distinct observations. Barcelona’s B/Atlètic name-period continuity is supported by the club history, but is documented rather than applied as a global mapping. Bilbao Athletic is the reserve associated with the source label Athletic Club B. Castilla’s reserve identity is supported; historical Real Madrid B naming dates and universal equivalence are not sufficiently established here for a global mapping. Sevilla’s historical FC B equivalence is likewise not an approved rename. Sanse and Villarreal B remain distinct from their parents. There are **no applied global team-name mappings**. Ambiguous, colliding or nonempty replacement mappings are rejected by the policy helper. No earlier La Liga names or standardized files are modified.

## Scheduling, chronology and uncertainty

The policy carries forward all **23 round contexts** (11 DOCUMENTED, 12 PARTIAL), all **253 affected fixture references**, **30 diagnostic outliers**, **17 source-order date reversals**, **33 partial individual claims**, the six identity groups and the frozen sample-selection fingerprint. Partial history is not reclassified as erroneous or fully verified. Long round spans, storage order, reserve status and absence of individual verification alone do not trigger correction or exclusion.

Dates have separate fields: source date, independently supported scheduled date, original kickoff/suspension day, actual completion day, individual administrative-decision day, common expulsion day, and approved effective result-availability day. Unestablished event dates remain null. Source and round order must never substitute for chronology. Future consumers must sort and filter on the appropriate effective availability semantics and require **effective day strictly earlier than prediction day**; same-day outcomes are unavailable because exact timestamps are not established.

Ordinary complete records retain their unchanged source playing date only as **SOURCE_PLAYING_DATE_PROXY_NOT_CERTIFIED** for provisional screening. This does not demonstrate final-result availability. `training_allowed` additionally rejects such proxies even if separate clearance flags were later changed; source-bound availability review would be required. It also rejects every held, incomplete, structurally failed or newly conflicted result, and requires independent model-suitability and licensing clearances. **No current assessment permits training**. The helper is tested policy infrastructure; no application training/evaluation path was changed.

## Reproducibility, integrity and tests

New public implementation: `scripts/decide_segunda_policy.py`; tests: `tests/test_segunda_policy.py`; this document: `docs/segunda-division-policy.md`. `PLANNING_LOG.md` is appended only. Existing Phase 2–5 scripts, tests, documents, originals and reports remain byte-identical.

Private artifacts under ignored `data/private/spain/segunda_division/`:

- `phase6_protected_before.json`: 68 protected entries (54 previous private artifacts and 14 previous public files), plus append-only planning-log prefix.
- `phase6_decision_policy.json`: 34 source/evidence-bound cases; 33 user-approved and one explicitly proposed conditional hold; full audit identifiers, original records and uncertainty metadata.
- `phase6_policy_assessment.json`: measured season-level reconciliation, action/uncertainty counts and input/policy SHA-256 hashes.
- `phase6_verification.json`: test/JUnit fingerprints, regeneration byte comparisons, public/private hashes and final Git/preservation checks.

Nested preservation checks additionally cover all **493 private and 145 public protected artifacts** from the seven completed competitions and the earlier frozen Segunda baselines. Before building, the script independently replays the Phase 5 offline checks and compares both saved Phase 5 outputs byte-for-byte, including raw parsing/source bindings. Frozen documentary digests bind each decision to the saved claim and source metadata; the code does not re-fetch or independently certify web truth.

Offline commands, using the established isolated Python environment when necessary:

```sh
PYTHONPATH=. python3 -B -m scripts.decide_segunda_policy --check
PYTHONPATH=. python3 -B -m scripts.decide_segunda_policy --write --output-directory /tmp/EXISTING_EMPTY_DIR
PYTHONPATH=src:. PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -B -m pytest tests/test_segunda_policy.py -q -p no:cacheprovider
```

Writes preflight all existing outputs and refuse changed bytes; identical saved outputs are reused. Regeneration in two independently created temporary directories, in separate processes, produced byte-identical policy and assessment files. Reproduction requires authorized local private inputs and their preserved evidence ledger; public code alone does not contain the private source bundle. No downloads or package/environment changes were made.

**80 new synthetic policy tests passed**; **204 focused Segunda tests passed**; **1,013 full repository tests passed**, including all **seven app/launcher tests**. Zero failures, errors or skips. The full suite completed in 12.49 seconds using the previously established temporary offline environment outside iCloud; the original `.venv` was preserved. Cases cover every supplement and every Reus hold, both special scheduling cases, both high scores, reserve separation, source/evidence rebinding, missing/duplicate/conflicting registry cases, strict chronology, technical/rights gates, deterministic assessment and protected-byte preservation.

## Remaining limitations and Phase 7 approval gate

1. Decide whether to approve the proposed Deportivo–Fuenlabrada conditional hold or authorize an alternative evidence-backed finality/availability treatment. Until then it remains conditionally held; do not force the 5,985 scenario.
2. Approve Phase 7 explicitly before writing any standardized CSV or complete audit archive. The nine approved supplements must remain traceable to blank source records; all 21 Reus holds and any remaining conditional hold must stay outside screened output.
3. Preserve all partial historical classifications and original date semantics. The dataset is structurally validated and selectively corroborated, not historically certified in full.
4. Keep the **1990/91–2011/12 22-season source gap** and incomplete pinned **2025/26: 131 scored, 331 unscored** explicit. The original nine 2024/25 source blanks remain even though approved supplements now exist. Modern 2012/13–2024/25 coverage is not the complete historical Segunda database.
5. Model-training suitability and redistribution/model-training rights remain unresolved. Existing OpenFootball/third-party provenance and RSSSF limitations are unchanged. Official/news corroboration grants no new permission.

Stop after Phase 6. No Phase 7 exports, source mutation, application integration, training, staging, commit, push or merge.
