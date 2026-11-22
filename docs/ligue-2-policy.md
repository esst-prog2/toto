# Ligue 2 — Phase 6 processing policy

Approved scope: 2014/15–2024/25 only. Decision date: 2026-11-22. Phase 6 creates provisional processing metadata, not a standardized CSV or complete audit archive.

## Protected starting state

Branch `feature/data-collection`, HEAD `07efff5f014bdd2e7e423f2fee76333346135790`. Previous uncommitted Ligue 2 work and both .DS_Store files were retained. The Phase 6 baseline freezes 122 Phase 2–5 entries and the prior planning-log prefix. Nested checks preserve 676 earlier private files, 185 public files and all original acquisitions, reports, registries and evidence. No external acquisition was performed.

## Source-to-policy reconciliation

| Provisional disposition | Observations | Treatment in a future Phase 7 CSV |
|---|---:|---|
| COMPLETED_RESULT_CANDIDATE | 4,003 | Eligible for projection only after Phase 7 checks |
| ADMINISTRATIVE_HOLD_OUT | 3 | Omit; preserve originals in future archive |
| NOT_PLAYED | 100 | Omit; preserve null scores in future archive |
| Other HOLD OUT | 0 | None |
| Additional definitive exclusion | 0 | None |
| Total | 4,106 | Every source observation has one disposition |

The 4,006 score-bearing observations reconcile as 4,003 candidates plus three administrative HOLD OUTs. The 100 cancelled slots are separate from missing/unknown outcomes. There are zero structurally invalid or unexplained incomplete observations. The builder verifies unique source IDs, unique provisional candidate fingerprints, exact population totals, frozen Phase 5 regeneration and all five special-case bindings. Candidate inclusion is not historical certification, verified availability, training suitability or licensing clearance.

## Exact special-case decisions

| Policy | Source-bound audit ID | Original observation | Provisional decision | Documentary dates |
|---|---|---|---|---|
| VALENCIENNES_BEZIERS | `8601876bb734068cc797791701e774c074eded339984251b5ad9de686fb97ee7` | 2018/2019; 2019-04-19; Valenciennes FC–AS Béziers; 5-6; line 527 | COMPLETED_RESULT_CANDIDATE | publication: None; kickoff: None; completion: None |
| NIORT_VALENCIENNES | `03db5c7de89bb16fb58f71ef939bcb1976e6cc0b66a9b14f7aae3a1d62571ede` | 2020/2021; 2020-12-22; Chamois Niortais–Valenciennes FC; 0-3; line 252 | ADMINISTRATIVE_HOLD_OUT | publication: None; kickoff: None; completion: None |
| NANCY_QRM | `afcb54cb3230a64b091b4980dedb16b65e9ac9df6228d2b3252c2f85b9506862` | 2021/2022; 2022-04-22; AS Nancy Lorraine–US Quevilly-Rouen; 0-3; line 522 | ADMINISTRATIVE_HOLD_OUT | publication: 2022-05-04; kickoff: None; completion: None |
| BORDEAUX_RODEZ | `a56d48ae18688610ad53de15ee0cb1d89051919bbaac6403e0eedb0dffe494d9` | 2022/2023; 2023-06-02; Girondins Bordeaux–Rodez AF; 0-1; line 570 | ADMINISTRATIVE_HOLD_OUT | publication: 2023-06-12; kickoff: None; completion: None |
| AJACCIO_BASTIA | `7accac4a3b7315d4cfbb91cdcb14c73d66b81f779ac1bce0b5e88c565a1896d9` | 2024/2025; 2024-12-03; AC Ajaccio–SC Bastia; 0-0; line 152 | COMPLETED_RESULT_CANDIDATE | publication: None; kickoff: 2024-10-26; completion: 2024-12-03 |

Each per-observation decision also preserves original source path, checksum, physical-line checksum, pinned revision, Git blob identity, original annotation, evidence IDs, historical confidence, open questions, a source-bound decision ID and its reason. Full original event context is retained separately from approved Phase 6 interpretation.

### Administrative cases

- **Niort–Valenciennes:** retain 2020-12-22 and 0–3 [awarded] unchanged. I01/I02 remain indexed reporting, including a 2021-01-06 award-report lead; no primary publication/finality/availability date is established. Administrative HOLD OUT.
- **Bordeaux–Rodez:** retain 2023-06-02 and 0–1. D02–D05 distinguish interruption, June 12 penalty defeat and June 27 club acceptance. June 12 is the documented first-instance publication date, not approved numerical homologation or availability. No guessed 0–3 substitution. Administrative HOLD OUT.
- **Nancy–QRM:** retain 2022-04-22 and 0–3. D25 documents the May 4 penalty defeat; I03 is indexed interruption context. Publication date 2022-05-04 is separate from unknown numerical homologation, appeal finality and availability. Administrative HOLD OUT.

The defaults are unchanged from user approval. Reinspection of the preserved evidence revealed no material contradiction requiring a different policy. An unrecognized administrative award, unapproved special case, unknown structural flag or contradicted historical classification fails explicitly rather than entering the candidate population.

### Interrupted Ajaccio derby

D21/D22 distinguish the October 26 interrupted event from the December 3 resumption; D23 corroborates teams, completion date and 0–0. This supports a narrowly bound same-fixture completion policy: original kickoff 2024-10-26, actual completion and earliest usable result day 2024-12-03. The source already records December 3, so no source-date value changes. No second fixture is created. Unknown intraday ordering bars use on December 3; the earliest permitted prediction day under this day-granularity guard is December 4. Documentary inconsistencies about a commission date in D29 are not adopted.

No other completed replay/resumption is established by the frozen review that warrants an additional date policy. The Bordeaux and Nancy interruptions are covered by administrative HOLD OUTs. Newly discovered interrupted/replayed cases require explicit source-bound review rather than automatic ordinary treatment.

### Unusual score and cancellations

D06 corroborates Valenciennes–Béziers 2019-04-19, 5–6. Retain as a completed-result candidate without score correction. Its actual availability timestamp is not invented.

For 2019/20, the source has 380 scheduled slots, 280 score-bearing observations and 100 explicit cancellations. D01 provides official aggregate corroboration, not independent certification of each scheduled date. Each cancelled observation is NOT_PLAYED with null score and no availability date. None can pass the chronological eligibility guard.

## Chronological safeguards

`decide_ligue2_policy.py` stores source heading/date, scheduled date, actual kickoff, completion, administrative publication, administrative finality and effective result availability as distinct fields. Unknown dates remain null. Ordinary candidate dates are explicitly SOURCE_DATE_PROXY: they are not independently certified result-availability dates.

`eligible_for_prediction` regenerates the source-bound decision from the supplied immutable observation and historical metadata and rejects altered decision fields. Only a completed-result candidate with verified availability strictly before the prediction day can pass. Unknown availability, same-day use, later completion, administrative HOLD OUTs and NOT_PLAYED cannot pass. `training_allowed` additionally requires suitability and training permissions; neither is cleared, so no current decision authorizes training. Callers must use preserved validated inputs and this guard, rather than accepting a caller-edited registry.

The CSV alone will not guarantee freedom from future-information leakage. Future consumers need validated decision metadata, genuinely established availability and appropriate prediction cutoffs. Ordinary source-date proxies must not be relabelled as known availability by downstream code.

## Scheduling, historical confidence and identity

All 364 structural review candidates, 376 historical registry entries, 23 wide contexts/228 members, 25 outliers and 31 reversal pairs/62 endpoints remain traceable. The exception registry carries the full round/reversal context and identity review; each observation retains its flags and available historical evidence/open questions.

Eight wide contexts have documented explanations and fifteen partial explanations. Six reversal pairs are partial and twenty-five unresolved. Outlier core-fact findings remain five full, six partial and fourteen unresolved. None of these flags alone causes exclusion or a date correction. Of the 376 review entries, 358 unresolved core-fact classifications are not 358 invalid matches. They remain documented limitations unless an explicit material outcome conflict is identified; verified availability is still required for chronological use.

All original club labels remain unchanged. AC Ajaccio and Gazélec stay distinct. QRM/Annecy sporting histories do not justify universal predecessor/successor identity mappings. The 29 exact Ligue 1 string overlaps do not certify continuity. No normalized aliases are approved. Provisional candidate fingerprints hash an unambiguous JSON tuple containing league, season, source date and both labels; they are distinct from immutable source audit IDs. Phase 7 must use the established shared eight-column ID implementation and check collisions against all earlier competitions; these Phase 6 fingerprints are not a replacement schema.

## Outputs and reproduction

- `phase6_decision_registry.json`: all 4,106 bound provisional decisions.
- `phase6_exception_registry.json`: five special cases plus 100 cancelled observations and preserved chronology/identity contexts.
- `phase6_policy_summary.json`: mutually exclusive counts and protected evidence summary.
- `phase6_policy_manifest.json`: input/output SHA-256 hashes and output sizes.
- `phase6_protected_before.json`: frozen Phase 2–5 baseline.
- `phase6_reproducibility.json` and verification receipts: independent comparisons and fresh test evidence.

All are private under ignored `data/private/france/ligue_2/`. Run `PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python -B scripts/decide_ligue2_policy.py` from the repository root. Existing outputs are compared rather than overwritten. The historical review is regenerated and compared to frozen outputs first.

## Tests and independent reproducibility

Fresh bounded execution used the preserved external Python 3.13.12 environment, without installs, dependency upgrades or original .venv changes:

| Scope | Passed | Failed / unverified |
|---|---:|---:|
| New synthetic policy tests | 43 | 0 |
| All focused Ligue 2 tests | 223 | 0 |
| Non-UI regressions | 1,515 | 0 |
| App/launcher | 7 | 0 |
| Complete repository suite | 1,522 | 0 |

Runs overlap and must not be added together. Logs, XML and subprocess exit statuses are preserved under private `verification_phase6/`.

A separate Python process regenerated all four outputs in safe external temporary storage. All matched saved bytes and SHA-256; the comparison receipt is private. This verifies deterministic processing from frozen inputs, not exhaustive independent historical certification.

| Output | SHA-256 |
|---|---|
| Decision registry | `3f73a84d8612334ab41e5dfcd1e9b1ea894c0a6c16e380f4773f81489db5eae5` |
| Exception registry | `b71b295126748f6262e65445f8f0b527fa5238b1075e865dfdb2c0f50b2f50e9` |
| Policy summary | `42b3b216bbc86e33d5cc762ad6e1f9d43e8a241b0b5c37f793781f403e1b1e1c` |
| Manifest | `a68e356c83dde0ee9a3200a0f19ee0813b5fe58f74b5b436c7f2a28699fac41c` |

Protected fingerprints pass, all private artifacts are Git-ignored, no private paths are tracked, and the Git index and HEAD remain unchanged. Public Phase 6 changes are this report, `scripts/decide_ligue2_policy.py`, `tests/test_ligue2_policy.py` and appended planning-log lines. No other project file was changed. Synthetic tests require no private data or network and cover all three administrative HOLD OUTs, completion evidence, strict dates, 5–6 retention, cancellation accounting, scheduling flags, unknown/contradicted evidence, immutable bindings, distinct identities and stable decisions.

## Coverage, rights and Phase 7 approval gate

Only eleven acquired seasons are in this policy. The 24-season 1990/91–2013/14 acquisition gap, unresolved RSSSF 1998/99 sample and separate incomplete 2025/26 source (306 slots, 116 scored, 190 unscored) remain outside scope. Full 36-season historical coverage is not claimed.

OpenFootball CC0 addresses rights held by that publisher; upstream rights are not guaranteed. Technical suitability, historical confidence, redistribution permission and model-training permission remain separate. Both rights categories and model suitability are NOT_CLEARED. No application integration or training occurred.

Phase 7 requires explicit approval, successful protected-baseline checks, these frozen policies, shared-schema/ID compatibility checks and independent regeneration. Its expected scope is all 4,106 original observations in a full audit archive and 4,003 completed-result candidates in the eight-column projection, omitting three administrative HOLD OUTs and 100 NOT_PLAYED. Counts must be reverified, not forced. Preserve source dates and all decision metadata; apply the approved completion policy only to the bound derby. No such CSV or complete archive was generated in Phase 6.
