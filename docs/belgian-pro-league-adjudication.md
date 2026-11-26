# Belgian Pro League — Phase 6 adjudication

Date: 2026-11-25. Original `toto` worktree, branch `feature/data-collection`, unchanged HEAD `013bb9c195624d5ac290aeb57dae11c4e21c0b5a`.

## Owner-approved methodological change

**Purpose: retrospective internal system diagnostics. This is not leakage-free historical forecasting and is not evidence of real-world predictive performance.** The owner explicitly permits accepted final historical results even where administrative determination occurred later. Consequently **no administrative decision/publication timestamp is an eligibility filter**. This supersedes earlier Phase5 proposals for strict availability controls in this Belgian internal diagnostic population. Earlier evidence, findings and planning history were not rewritten. Other competitions and the application/evaluation algorithm were not changed.

The match date remains the original football match date. Judgment dates never replace it. For a resumed event with reliable initial kickoff evidence, choose the initial kickoff date; retain source/completion dates separately. These are derived decisions only: no original source or standardized dataset was modified.

Historical inclusion, technical acceptance, independent corroboration, retrospective evaluation suitability and legal clearance are separate. **No model-training or redistribution rights are inferred or granted.**

## Explicit selection policy

Internal codes reuse familiar underscore-separated disposition spelling; display names map one-to-one:

| Code | Display meaning | Rule |
|---|---|---|
| INCLUDE | Include | Eligible top-flight stage, acceptable final score, supported date/identity, with actual football played; reviewed played administrative result permitted |
| HOLD_OUT | Hold out | Material result/date/identity/stage uncertainty, missing final score, unreviewed exceptional event or unresolved historical treatment |
| NOT_PLAYED | Not played | Documented no-football event/cancellation, including no-kickoff administrative awards; audit retains the award, but it is not an observed football match |
| OUT_OF_SCOPE | Out of scope | Explicitly documented cross-division contest outside the selected top-flight population |
| SOURCE_GAP | Coverage finding only | No adequate dated fixture coverage; never fabricate a fixture or assign NOT_PLAYED from absence |

Three independent dimensions are retained: whether football occurred/completed, what final score the sources and evidence support, and whether the event belongs to the chosen population. A disciplinary result is never relabelled as an ordinary completed on-field score.

For substantially played fixtures with directly inspected official result decisions and no known contrary outcome, accept that numerical result without requiring an exhaustive later-appeal search. Preserve remaining finality limitations as uncertainty flags. Missing direct support for a disputed/exceptional final result remains HOLD_OUT. No arbitrary minimum-minute threshold is introduced: the reviewed played-award cases had material competitive play; any new interrupted/awarded event requires its own explicit reviewed decision.

No kickoff means NOT_PLAYED for this football-match population even where a numerical administrative award exists. This consistent distinction applies to both Leuven–Mechelen and Standard–Westerlo. Their original reported award scores remain in the audit, not in accepted-score fields.

An ordinary uncorroborated sample or a wide round is not automatically erroneous. Date/score agreement is not proof of independent source lineage. Previously established within-season/source fixture correspondences are used only for the approved diagnostic event grouping; no global club aliases or legal continuity claims are created.

## Competition-stage scope

| Stage | Policy | Participation and evidence rationale |
|---|---|---|
| Regular season | INCLUDE if scored and otherwise acceptable | Retained top-flight source fixtures, preserving omissions and uncertainty |
| Championship playoffs | INCLUDE for documented acquired top-flight stages | Legitimate rematches are separate events, not duplicates |
| Europe playoffs | INCLUDE for acquired top-flight-only groups in2020/21,2021/22,2023/24,2024/25 | Historical mixed-tier Europe groups are not automatically eligible; unknown participation remains HOLD_OUT |
| Playdowns | INCLUDE for documented2023/24 and2024/25 groups | Top-flight domestic fixtures; separate stage identities retained |
| Title-deciding tests | Conditionally eligible only with specific top-flight participation/stage evidence; otherwise HOLD_OUT | No individually bound dated title test exists in the current acquired union; none fabricated or assumed never played |
| European qualification | INCLUDE for documented top-flight endpoints2023/24 and2024/25 | Domestic match between top-flight clubs, distinct from UEFA competition or cross-division promotion |
| Cross-division promotion/relegation | OUT_OF_SCOPE | Different participant scope; both2021/22 legs retained in audit |

The private matrix contains **252 season/stage rows** (36seasons ×7stages) with reason, dispositions, exact source IDs and applicable official evidence references. Stage eligibility alone never overrides a missing score or exceptional-fixture decision. No unacquired playoff is invented.

Measured stage totals in the8,724-event union:

| Stage | INCLUDE | HOLD_OUT | NOT_PLAYED | OUT_OF_SCOPE |
|---|---:|---:|---:|---:|
| REGULAR_SEASON | 8370 | 119 | 9 | 0 |
| CHAMPIONSHIP | 113 | 1 | 0 | 0 |
| EUROPE | 83 | 0 | 1 | 0 |
| PLAYDOWNS | 24 | 0 | 0 | 0 |
| EUROPE_QUALIFICATION | 2 | 0 | 0 | 0 |
| PROMOTION_RELEGATION | 0 | 0 | 0 | 2 |

## Administrative and interruption decisions

All seven exceptional decisions are bound to immutable original audit IDs and physical records from the approved Phase5 assessment. The registry preserves every contributing CSV/TXT and RSSSF representation, including original scores and annotations. No late judgment replaces the original football date.

| Fixture | Decision | Accepted score | Chosen match date | Reason / retained evidence |
|---|---|---|---|---|
| Standard Liège–RSC Anderlecht (2019-04-12) | HOLD_OUT | — (source score preserved) | — (source date preserved) | Played, stopped2-0; reported5-0 award supported only by search/index evidence. Direct final-result evidence insufficient, not an availability-time rejection. |
| Beerschot VA–Cercle Brugge (2021-07-27) | INCLUDE | 0-1 | 2021-07-24 | Original July24 kickoff selected; July27 completion and unchanged0-1 source result separately preserved. |
| Standard–Charleroi (2021-12-05) | INCLUDE | 0-3 | 2021-12-05 | Substantially played0-3; inspected January13,2022 decision fixes unchanged0-3. Original December5 football date retained. |
| Oud-Heverlee Leuven–Mechelen (2022-01-15) | NOT_PLAYED | — (source score preserved) | — (source date preserved) | Primary BAS evidence of nonappearance/no kickoff.5-0 award on March8 preserved but excluded from the football-played population. |
| Seraing–Royal Union Saint-Gilloise (2022-01-18) | INCLUDE | 0-4 | 2022-01-15 | Original January15 kickoff selected; January18 completion and final0-4 preserved separately from0-2 at interruption. |
| Royal Union Saint-Gilloise–Beerschot VA (2022-04-10) | INCLUDE | 5-0 | 2022-04-10 | Played until interruption; inspected April16 decision fixes5-0. Source date April10 retained, no judgment-date filter.82:04 versus81-minute annotation preserved. |
| Standard Liège–KVC Westerlo (2024-05-10) | NOT_PLAYED | — (source score preserved) | — (source date preserved) | No kickoff reported by inspected contemporary sources.0-5 administrative award and May28 decision context preserved, but no played football event selected. |

Primary and contemporary URLs, titles, dates, PDF receipts and evidence limitations remain in the frozen [Phase5 report](belgian-pro-league-historical-review.md) and private evidence index. This phase acquired no additional evidence or season datasets and did not research publication timestamps.

**Two unmatched endpoints:** Standard–Westerlo2023/24 has an eligible Europe stage but is NOT_PLAYED because no kickoff occurred. Antwerp–Charleroi2024/25,29May2025,1–2, is INCLUDE as a documented top-flight European qualifier. Absence from historical CSV is not an exclusion rule; the latter uses the preserved modern observation. The two cases were decided independently on stage and football/result evidence.

**Date changes authorized only in metadata:** Beerschot–Cercle source2021-07-27 → chosen2021-07-24; Seraing–Union source2022-01-18 → chosen2022-01-15. Completion dates remain separately recorded. All other INCLUDE dates and all accepted final numerical scores remain unchanged from their contributing source result. No chronological availability gating or app changes were implemented.

## Lommel, Mouscron and COVID

**Lommel2002/03:** INCLUDE the272 retained non-Lommel source events. No absent Lommel fixture is reconstructed. The missing played/annulled/never-played population remains an unquantified SOURCE_GAP, not a fabricated NOT_PLAYED list. Contemporary official reports and later annulment reporting remain preserved with primary-finality limitations. No new individually sourced Lommel event was available to adjudicate.

**Mouscron2009/10:** INCLUDE the210 retained non-Mouscron historical results. The separate30 earlier RSSSF documentary-only representations remain outside the10,434/8,724 union:

| Documentary class | Count | Decision | Reason |
|---|---:|---|---|
| Annulled numeric results |18|HOLD_OUT|Played-score reports preserved; original annulment judgment/treatment not sufficiently established to promote them as accepted final competition results |
| Annulled awards |2|HOLD_OUT|No automatic conversion of an annulled documentary award into a source match; final treatment unresolved |
| Explicit n/p slots |10|NOT_PLAYED|Documented n/p, without invented scores or individual ISO match dates |

The ten n/p decisions are documentary assertions, not newly independently certified fixture dates. None receives accepted-score/chosen-date fields. Owner permission to use later determined results does not itself resolve whether voided matches should be reintroduced. Two defensible future options remain explicit: retain voided games outside the accepted final-competition population, or separately authorize a played-on-field diagnostic population with adequate dated originals. This phase **HOLD_OUTs all20 annulled documentary cases** rather than arbitrarily choosing the latter or silently calling annulled games never played.

**COVID2019/20:** INCLUDE232 scored source events; NOT_PLAYED the eight source-marked cancelled final-round slots, using the documented season termination. Scheduled15March2020 context and physical lines417–424 are preserved; no numerical result, kickoff or decision-time availability is invented.

**Partial2025/26:** INCLUDE121 scored regular events and HOLD_OUT119 unscored scheduled slots. Unscored does not mean cancelled or never played. No postseason completion or updated season was acquired.

## Exact population reconciliation

| Population | INCLUDE | HOLD_OUT | NOT_PLAYED | OUT_OF_SCOPE | Total |
|---|---:|---:|---:|---:|---:|
| Source-supported conditional-event union |8,592|120|10|2|8,724|
| Earlier documentary-only Mouscron representations, separate |0|20|10|0|30|

The120 union HOLD_OUT events are119 missing final results plus Standard–Anderlecht2019. The ten union NOT_PLAYED events are eight COVID cancellations plus Leuven–Mechelen and Standard–Westerlo no-kickoff awards. The two OUT_OF_SCOPE events are2021/22 cross-division legs. None is dropped from the decision registry.

Every one of **10,100 frozen CSV/TXT observations +334 supplementary RSSSF descriptions =10,434 contributing representations** is bound exactly once to the8,724 events. Approved links remain1,402 CSV/TXT pairs plus306 RSSSF regular counterparts; two interruption/continuation pairs count descriptions separately but remain single events. The26 new RSSSF conditional events include24 top-flight playoff matches and two cross-division legs. Research documents and earlier RSSSF administrative material do not enlarge this population.

There are no final eight-column CSV records, final match IDs or standardized match files from this phase. Decision IDs identify the versioned, source-bound policy assessments only.

## 36-season coverage and dispositions

R/C/E/P/Q/X = observed regular/championship/Europe/playdown/European qualifier/cross-division events. These are observed diagnostic populations, not nominal accepted-season expectations. Zero does not mean no such historical stage existed.

| Season | R/C/E/P/Q/X observed | INCLUDE | HOLD_OUT | NOT_PLAYED | OUT_OF_SCOPE | Coverage |
|---|---|---:|---:|---:|---:|---|
| 1990/1991 | 0/0/0/0/0/0 | 0 | 0 | 0 | 0 | SOURCE_GAP |
| 1991/1992 | 0/0/0/0/0/0 | 0 | 0 | 0 | 0 | SOURCE_GAP |
| 1992/1993 | 0/0/0/0/0/0 | 0 | 0 | 0 | 0 | SOURCE_GAP |
| 1993/1994 | 0/0/0/0/0/0 | 0 | 0 | 0 | 0 | SOURCE_GAP |
| 1994/1995 | 0/0/0/0/0/0 | 0 | 0 | 0 | 0 | SOURCE_GAP |
| 1995/1996 | 306/0/0/0/0/0 | 306 | 0 | 0 | 0 | OBSERVED_SOURCES_NOT_COMPLETE_ALL_STAGES |
| 1996/1997 | 306/0/0/0/0/0 | 306 | 0 | 0 | 0 | OBSERVED_SOURCES_NOT_COMPLETE_ALL_STAGES |
| 1997/1998 | 306/0/0/0/0/0 | 306 | 0 | 0 | 0 | OBSERVED_SOURCES_NOT_COMPLETE_ALL_STAGES |
| 1998/1999 | 306/0/0/0/0/0 | 306 | 0 | 0 | 0 | OBSERVED_SOURCES_NOT_COMPLETE_ALL_STAGES |
| 1999/2000 | 306/0/0/0/0/0 | 306 | 0 | 0 | 0 | OBSERVED_SOURCES_NOT_COMPLETE_ALL_STAGES |
| 2000/2001 | 306/0/0/0/0/0 | 306 | 0 | 0 | 0 | OBSERVED_SOURCES_NOT_COMPLETE_ALL_STAGES |
| 2001/2002 | 306/0/0/0/0/0 | 306 | 0 | 0 | 0 | OBSERVED_SOURCES_NOT_COMPLETE_ALL_STAGES |
| 2002/2003 | 272/0/0/0/0/0 | 272 | 0 | 0 | 0 | OBSERVED_SOURCES_NOT_COMPLETE_ALL_STAGES |
| 2003/2004 | 306/0/0/0/0/0 | 306 | 0 | 0 | 0 | OBSERVED_SOURCES_NOT_COMPLETE_ALL_STAGES |
| 2004/2005 | 306/0/0/0/0/0 | 306 | 0 | 0 | 0 | OBSERVED_SOURCES_NOT_COMPLETE_ALL_STAGES |
| 2005/2006 | 306/0/0/0/0/0 | 306 | 0 | 0 | 0 | OBSERVED_SOURCES_NOT_COMPLETE_ALL_STAGES |
| 2006/2007 | 306/0/0/0/0/0 | 306 | 0 | 0 | 0 | OBSERVED_SOURCES_NOT_COMPLETE_ALL_STAGES |
| 2007/2008 | 306/0/0/0/0/0 | 306 | 0 | 0 | 0 | OBSERVED_SOURCES_NOT_COMPLETE_ALL_STAGES |
| 2008/2009 | 306/0/0/0/0/0 | 306 | 0 | 0 | 0 | OBSERVED_SOURCES_NOT_COMPLETE_ALL_STAGES |
| 2009/2010 | 210/0/0/0/0/0 | 210 | 0 | 0 | 0 | OBSERVED_SOURCES_NOT_COMPLETE_ALL_STAGES |
| 2010/2011 | 240/0/0/0/0/0 | 240 | 0 | 0 | 0 | OBSERVED_SOURCES_NOT_COMPLETE_ALL_STAGES |
| 2011/2012 | 240/0/0/0/0/0 | 240 | 0 | 0 | 0 | OBSERVED_SOURCES_NOT_COMPLETE_ALL_STAGES |
| 2012/2013 | 240/0/0/0/0/0 | 240 | 0 | 0 | 0 | OBSERVED_SOURCES_NOT_COMPLETE_ALL_STAGES |
| 2013/2014 | 240/0/0/0/0/0 | 240 | 0 | 0 | 0 | OBSERVED_SOURCES_NOT_COMPLETE_ALL_STAGES |
| 2014/2015 | 240/0/0/0/0/0 | 240 | 0 | 0 | 0 | OBSERVED_SOURCES_NOT_COMPLETE_ALL_STAGES |
| 2015/2016 | 240/0/0/0/0/0 | 240 | 0 | 0 | 0 | OBSERVED_SOURCES_NOT_COMPLETE_ALL_STAGES |
| 2016/2017 | 240/0/0/0/0/0 | 240 | 0 | 0 | 0 | OBSERVED_SOURCES_NOT_COMPLETE_ALL_STAGES |
| 2017/2018 | 240/0/0/0/0/0 | 240 | 0 | 0 | 0 | OBSERVED_SOURCES_NOT_COMPLETE_ALL_STAGES |
| 2018/2019 | 240/30/0/0/0/0 | 269 | 1 | 0 | 0 | OBSERVED_SOURCES_NOT_COMPLETE_ALL_STAGES |
| 2019/2020 | 240/0/0/0/0/0 | 232 | 0 | 8 | 0 | OBSERVED_SOURCES_NOT_COMPLETE_ALL_STAGES |
| 2020/2021 | 306/12/12/0/0/0 | 330 | 0 | 0 | 0 | OBSERVED_SOURCES_NOT_COMPLETE_ALL_STAGES |
| 2021/2022 | 306/12/12/0/0/2 | 329 | 0 | 1 | 2 | OBSERVED_SOURCES_NOT_COMPLETE_ALL_STAGES |
| 2022/2023 | 306/0/0/0/0/0 | 306 | 0 | 0 | 0 | OBSERVED_SOURCES_NOT_COMPLETE_ALL_STAGES |
| 2023/2024 | 240/30/30/12/1/0 | 312 | 0 | 1 | 0 | OBSERVED_SOURCES_NOT_COMPLETE_ALL_STAGES |
| 2024/2025 | 240/30/30/12/1/0 | 313 | 0 | 0 | 0 | OBSERVED_SOURCES_NOT_COMPLETE_ALL_STAGES |
| 2025/2026 | 240/0/0/0/0/0 | 121 | 119 | 0 | 0 | INCOMPLETE_PINNED_SNAPSHOT |

Coverage remains incomplete:1990/91–1994/95 lack approved complete dated originals;1992/93 standings are not a fixture inventory. Lommel's absent fixtures remain unquantified. The misplaced `2021-22/be1.txt` stays byte-for-byte2020/21 content; no file renamed. Actual2021/22 comparison uses the approved RSSSF recovery, with its own provenance. The pinned2025/26 snapshot remains incomplete. Missing other stages are not silently treated as NOT_PLAYED. No totals were forced to a nominal season count.

Additional-stage outcomes:2018/19 modern30championship =29INCLUDE+1HOLD_OUT;2020/21 modern12+12playoffs all24INCLUDE;2021/22 RSSSF12+12playoffs all24INCLUDE and two separate cross-division legs OUT_OF_SCOPE;2023/24 extra Standard–Westerlo NOT_PLAYED while other documented group stages/qualifier retained;2024/25 extra Antwerp–Charleroi qualifier INCLUDE. Legitimate repeated pairings retain distinct stage/source identities.

## Implementation, reproduction and fresh checks

New public implementation: `scripts/decide_belgian_pro_league_policy.py`; focused tests: `tests/test_belgian_pro_league_policy.py`; this report; append-only `PLANNING_LOG.md`.

New private files: `phase6_protected_before.json` (106 frozen pre-Phase6 entries); under `phase6/`: `policy.json`, `decision_registry.json`, `documentary_decisions.json`, `exception_decisions.json`, `season_stage_matrix.json`, `reconciliation.json`, `reproducibility.json`; final receipt `phase6_final_verification.json`. All remain Git-ignored. Existing source/evidence inventories and previous private assessments were not rewritten.

The policy registry preserves original fields and raw score strings, audit IDs, physical line/hash, original paths/revisions, stage/round/group/leg bindings, exact source contributors, selected disposition/date/result, reason and uncertainty flags. It reuses only the approved source-bound links; no city, global alias or score-based fuzzy merging. Unknown stages/conflicts fail closed; unseen awards/interruption annotations require explicit review. Non-INCLUDE events cannot expose accepted-score/date fields. The Phase7 metadata guard rejects substituted scores or judgment dates. This guard is not training or licensing permission.

```sh
PYTHONDONTWRITEBYTECODE=1 python -B -m scripts.decide_belgian_pro_league_policy
PYTHONDONTWRITEBYTECODE=1 python -B -m scripts.decide_belgian_pro_league_policy --verify
```

Seven artifacts independently regenerated in a separate process/temp directory and compared byte-for-byte and by SHA-256. The manifest binds the implementation, frozen-input baseline and individual assessment hashes. Regeneration refuses to overwrite differing saved outputs. Human historical findings are preserved evidence inputs; reproducibility does not manufacture historical certainty.

Fresh tests: **64 focused policy tests;275 all Belgian;503 acquisition/importer;7 app/launcher;2,436 full repository passed**. Selections overlap. All final runs: zero failed, errored or skipped tests. No timeout counted as a pass. Reused the existing external offline CPython3.13.12 environment; no installations, dependency downloads or changes to original `.venv`.

Protection checks: all106 frozen Phase2–5/recovery entries, nested original baselines and prior planning-prefix hashes unchanged. Twelve prior historical screened outputs/137,189 records plus258 separate ongoing English rows unchanged. The original1,415 private/250 public protected fingerprints and6,200 original runtime-package fingerprints match. All ten Belgian source originals remain unchanged. Application and promotional worktree untouched; no model training or integration. HEAD/index unchanged; no staging, commit, push, merge or rebase. Existing uncommitted work and two untracked `.DS_Store` files preserved.

## Phase7 handoff — explicit approval still required

1. Consume this exact frozen policy registry and all contributing originals; use `eligible_for_phase7` plus integrity checks. Expected currently eligible decision count:8,592, measured from this registry, not a forced source total.
2. Produce a full audit covering all8,724 source-supported events and their10,434 representations; preserve the30 earlier documentary-only entries as a separate audit population. Do not promote coverage gaps or research leads to fixtures.
3. Preserve kickoff/completion/administrative contexts; use original kickoff for the two approved resumptions. Use accepted final scores, never administrative judgment dates as match dates. Keep retrospective-use labeling and no forecasting-performance claims.
4. Verify eight-column schema and canonical competition name, deterministic stage-aware identity, unique IDs, accepted-subset equality, score-derived outcomes and no leakage of120HOLD_OUT/10NOT_PLAYED/2OUT_OF_SCOPE source events into screened output.
5. Resolve source-bound team labels without global legal-identity merges. Retain verification, coverage, source-independence and licensing limitations. Any new evidence/decision changing the accepted population requires explicit review rather than silent reclassification.
6. Independently regenerate and preserve all previous competitions. No application integration or training permission is implied by subsequent technical standardization.

**Stopped after Phase6. No standardized CSV, application change, training or Git publication.**
