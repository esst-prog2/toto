# French Ligue 2 — Phase 4 independent structural validation

Date: 2026-11-22. Status: COMPLETE, pending user approval. Phase 5 not started.

## Scope, independent method and protection

Work exclusively in original toto worktree, feature/data-collection, unchanged
HEAD `07efff5f014bdd2e7e423f2fee76333346135790`. This phase validates the eleven
acquired 2014/15–2024/25 originals only. No acquisition, score/date correction,
identity mapping, eligibility/HOLD OUT/exclusion policy, standardization,
application integration, model training, staging, commit, push or merge.

The new parser in scripts/validate_ligue2_structure.py does not call Phase 2/3
parsers. It reads immutable UTF-8 source bytes, explicitly validates titles,
round/stage/date grammar, resolves years from source season/weekday, binds physical
lines including original newline bytes, and parses full-time, halftime and status
annotations independently. Unknown grammar or unresolvable dates fail explicitly.
It independently enumerates receipts, recalculates all season and round counts,
pairings, score outcomes and chronology diagnostics, then compares every literal
source fact and review membership with the frozen Phase 3 inventory.

All 13 acquired originals (twelve OpenFootball seasons including separate 2025/26,
plus RSSSF) remain byte-identical. SHA-256 receipts, pinned Git blobs and source
URLs/revisions verify. Existing metadata/notices remain unchanged. Protected
fingerprints cover **676 earlier private files / 185 tracked public files**, the
nested **54 Phase 2 entries**, and **88 frozen Phase 2–3 entries** (78 private files
and ten public files). Planning history is prefix-protected and appended only.
Git HEAD/index remain unchanged; no private data is tracked/staged. All artifacts
remain under ignored data/private/france/ligue_2/. Application and promotional
worktree were not modified.

## Season-by-season structural results

| Season | Observed / expected slots | Clubs | Score-bearing | Cancelled | Valid slots | Invalid records | Incomplete | Flagged observations |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2014/2015 | 380 / 380 | 20 | 380 | 0 | 380 | 0 | 0 | 0 |
| 2015/2016 | 380 / 380 | 20 | 380 | 0 | 380 | 0 | 0 | 0 |
| 2016/2017 | 380 / 380 | 20 | 380 | 0 | 380 | 0 | 0 | 13 |
| 2017/2018 | 380 / 380 | 20 | 380 | 0 | 380 | 0 | 0 | 36 |
| 2018/2019 | 380 / 380 | 20 | 380 | 0 | 380 | 0 | 0 | 23 |
| 2019/2020 | 380 / 380 | 20 | 280 | 100 | 380 | 0 | 0 | 100 |
| 2020/2021 | 380 / 380 | 20 | 380 | 0 | 380 | 0 | 0 | 80 |
| 2021/2022 | 380 / 380 | 20 | 380 | 0 | 380 | 0 | 0 | 54 |
| 2022/2023 | 380 / 380 | 20 | 380 | 0 | 380 | 0 | 0 | 23 |
| 2023/2024 | 380 / 380 | 20 | 380 | 0 | 380 | 0 | 0 | 15 |
| 2024/2025 | 306 / 306 | 18 | 306 | 0 | 306 | 0 | 0 | 20 |
| **Total** | **4106 / 4106** | — | **4006** | **100** | **4106** | **0** | **0** | **364** |

Definitions: a valid slot is a structurally consistent observation, not a certified
played/training result. All 100 null-score [cancelled] observations are valid
scheduled-but-unplayed slots, not unexplained incomplete records. The 4006 numeric
observations include Niort's awarded score and the unannotated Bordeaux case;
they must not all be described as historically certified on-field results.
There are **3742 unflagged observations**, but unflagged is not certified history.
No screening or accepted-model-record count is produced.

Each season has its expected literal club count, every directed home/away pairing
once, complete round set, n/2 fixtures and every club exactly once per round.
No missing/duplicate/conflicting pairing, other-stage record, same-team/same-day
collision, malformed numeric score, halftime/fulltime contradiction, invalid team
label, normalized-label collision or season-date violation was found. Numeric
outcomes are derived from retained goals and do not establish historical accuracy.
The source-order checks do not reorder or rewrite originals.

Original competition titles, round/stage labels, date headings, kickoff-time
strings where present, score strings, source line numbers, source SHA-256, physical
line SHA-256, existing audit IDs, original raw lines and pinned provenance are
retained in every assessment record. The shared eight-column schema and proposed
canonical **Ligue 2** remain compatible, but no standardized rows/IDs are generated.

## Independent review-set reconciliation and overlaps

All **331 Phase 3 fixture members** reconcile exactly, with original category sets:

- 228 WIDE_ROUND members across 23 contexts.
- 100 SOURCE_CANCELLED observations.
- One SOURCE_ANNOTATION: Niort–Valenciennes, now explicitly SOURCE_MARKED_AWARDED.
- One BORDEAUX_RODEZ_ADMINISTRATIVE_REVIEW.
- One UNUSUAL_SCORE: Valenciennes–Béziers.

These original categories were independently checked and have **zero intersections**
in this population; disjointness was measured rather than assumed.

New structural diagnostics identify **25 date outliers**, all within the existing
228 wide-round members, and **31 adjacent source-order reversal pairs** touching
**62 distinct observations**. Of those 62, 29 were already wide-round members and
33 are additional observations. Therefore the expanded queue contains
**331 + 33 = 364 distinct observations**, not the sum of category membership counts.

| Expanded category | Fixture observations |
|---|---:|
| WIDE_ROUND | 228 |
| DIAGNOSTIC_DATE_OUTLIER | 25 |
| SOURCE_ORDER_DATE_REVERSAL | 62 |
| SOURCE_CANCELLED | 100 |
| SOURCE_MARKED_AWARDED | 1 |
| BORDEAUX_RODEZ_ADMINISTRATIVE_REVIEW | 1 |
| UNUSUAL_SCORE | 1 |

The exact disjoint flag combinations establish every overlap:

| Flag combination | Observations |
|---|---:|
| BORDEAUX_RODEZ_ADMINISTRATIVE_REVIEW | 1 |
| DIAGNOSTIC_DATE_OUTLIER + SOURCE_ORDER_DATE_REVERSAL + WIDE_ROUND | 23 |
| DIAGNOSTIC_DATE_OUTLIER + WIDE_ROUND | 2 |
| SOURCE_CANCELLED | 100 |
| SOURCE_MARKED_AWARDED | 1 |
| SOURCE_ORDER_DATE_REVERSAL | 33 |
| SOURCE_ORDER_DATE_REVERSAL + WIDE_ROUND | 6 |
| UNUSUAL_SCORE | 1 |
| WIDE_ROUND | 197 |

Identity concerns are separately recorded as label/group investigations rather
than marking every match involving those clubs as erroneous. They do not silently
inflate the 364-observation technical/exception queue.

## Scheduling contexts and diagnostic outliers

For every round, choose the lower median of its source dates and flag members
more than 14 days from that median. This is a deterministic diagnostic, not a
rescheduling inference or proposed correction. All 23 wide-round contexts and
228 original memberships remain unchanged. The 25 diagnostic outliers below
require independent event-level evidence in Phase 5. No source annotation explains
the wide spans; postponement, interruption or actual scheduling reasons are not
certified by a long span alone.

| Season | Round | Earliest source date | Latest source date | Lower median | Members | Diagnostic outlier fixtures / source dates |
|---|---:|---|---|---|---:|---|
| 2016/2017 | 21 | 2017-01-20 | 2017-02-21 | 2017-01-20 | 10 | RC Strasbourg – Tours FC (2017-02-21) |
| 2017/2018 | 19 | 2017-12-15 | 2018-01-23 | 2017-12-15 | 10 | Gazélec FC Ajaccio – Nîmes Olympique (2018-01-23) |
| 2017/2018 | 29 | 2018-03-09 | 2018-04-03 | 2018-03-09 | 10 | Tours FC – Valenciennes FC (2018-04-03) |
| 2017/2018 | 32 | 2018-04-06 | 2018-04-30 | 2018-04-06 | 10 | Stade de Reims – Havre AC (2018-04-30) |
| 2018/2019 | 5 | 2018-08-24 | 2018-10-02 | 2018-08-24 | 10 | AS Béziers – RC Lens (2018-10-02) |
| 2018/2019 | 19 | 2018-12-21 | 2019-01-29 | 2018-12-21 | 10 | Havre AC – Valenciennes FC (2019-01-15), FC Metz – AS Nancy Lorraine (2019-01-29) |
| 2020/2021 | 3 | 2020-09-12 | 2020-09-30 | 2020-09-12 | 10 | AC Ajaccio – USL Dunkerque (2020-09-30) |
| 2020/2021 | 8 | 2020-10-24 | 2020-11-24 | 2020-10-24 | 10 | Grenoble Foot 38 – AS Nancy Lorraine (2020-11-24) |
| 2020/2021 | 9 | 2020-10-31 | 2020-12-15 | 2020-10-31 | 10 | Chamois Niortais – Grenoble Foot 38 (2020-12-15) |
| 2020/2021 | 11 | 2020-11-21 | 2020-12-15 | 2020-11-21 | 10 | AS Nancy Lorraine – ESTAC Troyes (2020-12-15) |
| 2020/2021 | 29 | 2021-03-13 | 2021-04-14 | 2021-03-13 | 10 | Clermont Foot 63 – Amiens SC (2021-04-14) |
| 2020/2021 | 31 | 2021-04-03 | 2021-04-28 | 2021-04-03 | 10 | USL Dunkerque – Amiens SC (2021-04-28) |
| 2020/2021 | 35 | 2021-04-24 | 2021-05-12 | 2021-04-24 | 10 | Toulouse FC – Pau FC (2021-05-12) |
| 2021/2022 | 2 | 2021-07-31 | 2021-08-18 | 2021-07-31 | 10 | US Quevilly-Rouen – SC Bastia (2021-08-18) |
| 2021/2022 | 5 | 2021-08-21 | 2021-09-14 | 2021-08-21 | 10 | AC Ajaccio – Paris FC (2021-09-14) |
| 2021/2022 | 20 | 2022-01-08 | 2022-01-28 | 2022-01-08 | 10 | SM Caen – Chamois Niortais (2022-01-28), USL Dunkerque – Paris FC (2022-01-28) |
| 2021/2022 | 21 | 2022-01-15 | 2022-02-01 | 2022-01-15 | 10 | Chamois Niortais – USL Dunkerque (2022-02-01) |
| 2021/2022 | 22 | 2022-01-22 | 2022-02-15 | 2022-01-22 | 10 | Grenoble Foot 38 – Chamois Niortais (2022-02-15) |
| 2022/2023 | 7 | 2022-09-02 | 2022-10-04 | 2022-09-02 | 10 | EA Guingamp – Rodez AF (2022-10-04) |
| 2022/2023 | 23 | 2023-02-11 | 2023-03-14 | 2023-02-11 | 10 | Paris FC – Amiens SC (2023-03-14) |
| 2023/2024 | 13 | 2023-11-04 | 2023-11-28 | 2023-11-04 | 10 | US Concarneau – Pau FC (2023-11-28) |
| 2024/2025 | 8 | 2024-10-04 | 2024-10-22 | 2024-10-05 | 9 | Pau FC – SC Bastia (2024-10-22) |
| 2024/2025 | 10 | 2024-10-25 | 2024-12-03 | 2024-10-25 | 9 | AC Ajaccio – SC Bastia (2024-12-03) |

## Source-order chronology

There are 31 occasions where the next physical fixture line has an earlier date.
The largest backwards step is **38 days** (2020-12-15 to 2020-11-07). Such reversals
can follow round-organized files containing rescheduled fixtures; this is only a
structural explanation of ordering, not verification of the underlying events.
Both endpoint observations retain review flags and original source bindings.
Neither file order nor round number is a valid chronological training order.

| Season | Previous line | Previous date | Next fixture line | Next date | Backwards days |
|---|---:|---|---:|---|---:|
| 2016/2017 | 117 | 2016-09-27 | 122 | 2016-09-19 | 8 |
| 2016/2017 | 339 | 2017-02-21 | 344 | 2017-01-27 | 25 |
| 2017/2018 | 307 | 2018-01-23 | 312 | 2018-01-12 | 11 |
| 2017/2018 | 337 | 2018-01-30 | 342 | 2018-01-19 | 11 |
| 2017/2018 | 450 | 2018-03-13 | 455 | 2018-03-09 | 4 |
| 2017/2018 | 467 | 2018-04-03 | 472 | 2018-03-16 | 18 |
| 2017/2018 | 515 | 2018-04-30 | 520 | 2018-04-13 | 17 |
| 2018/2019 | 85 | 2018-10-02 | 90 | 2018-08-31 | 32 |
| 2018/2019 | 308 | 2019-01-29 | 313 | 2019-01-11 | 18 |
| 2020/2021 | 51 | 2020-09-30 | 56 | 2020-09-19 | 11 |
| 2020/2021 | 127 | 2020-11-24 | 132 | 2020-10-31 | 24 |
| 2020/2021 | 143 | 2020-12-15 | 148 | 2020-11-07 | 38 |
| 2020/2021 | 173 | 2020-12-15 | 178 | 2020-11-28 | 17 |
| 2020/2021 | 307 | 2021-01-27 | 312 | 2021-01-23 | 4 |
| 2020/2021 | 439 | 2021-04-14 | 444 | 2021-03-19 | 26 |
| 2020/2021 | 470 | 2021-04-28 | 475 | 2021-04-10 | 18 |
| 2020/2021 | 515 | 2021-05-04 | 520 | 2021-04-24 | 10 |
| 2020/2021 | 531 | 2021-05-12 | 536 | 2021-05-01 | 11 |
| 2021/2022 | 37 | 2021-08-18 | 42 | 2021-08-07 | 11 |
| 2021/2022 | 68 | 2021-08-25 | 73 | 2021-08-21 | 4 |
| 2021/2022 | 84 | 2021-09-14 | 89 | 2021-08-28 | 17 |
| 2021/2022 | 306 | 2022-01-28 | 311 | 2022-01-15 | 13 |
| 2021/2022 | 324 | 2022-02-01 | 329 | 2022-01-22 | 10 |
| 2021/2022 | 341 | 2022-02-15 | 346 | 2022-02-05 | 10 |
| 2022/2023 | 111 | 2022-10-04 | 116 | 2022-09-10 | 24 |
| 2022/2023 | 347 | 2023-03-14 | 352 | 2023-02-18 | 24 |
| 2023/2024 | 110 | 2023-10-03 | 115 | 2023-09-26 | 7 |
| 2023/2024 | 125 | 2023-10-04 | 130 | 2023-09-30 | 4 |
| 2023/2024 | 200 | 2023-11-28 | 205 | 2023-11-11 | 17 |
| 2024/2025 | 122 | 2024-10-22 | 127 | 2024-10-18 | 4 |
| 2024/2025 | 152 | 2024-12-03 | 157 | 2024-10-29 | 35 |

All 4106 heading dates parse within the stated season: **165 observations have
an explicit source year; 3941 resolve year using season and weekday**. The latter
is parsing resolution, not insertion of an unknown match day. It does not make
source headings independently verified actual kickoff/completion dates.

Every record has separate chronology fields for source heading date, source
scheduled date when explicitly cancelled, actual kickoff/completion date,
administrative decision date, secondary-reported decision-date lead and effective
result availability. Actual kickoff/completion and effective availability remain
unassigned unless independently established in future review. No model date policy
is implemented. Source-local times do not establish a timezone or exact availability.

## Exceptional fixtures and Phase 5 evidence requirements

### Niort–Valenciennes, 2020/21

Original Chamois Niortais–Valenciennes FC, **2020-12-22**, **0-3 [awarded]**, source
line **252**, round 17. Numeric fields are structurally consistent; this is not
certification of a played match. The indexed contemporary January 2021 lead is
preserved as secondary_reported_decision_date **2021-01-06**, explicitly not a
verified administrative date. Actual kickoff/completion and effective availability
remain null. No backdating or screening decision. Phase 5 must inspect the primary
competition decision, original scheduled/nonplayed event, numerical award, appeal
outcome/finality and defensible result-availability date.

### Bordeaux–Rodez, 2022/23

Original Girondins Bordeaux–Rodez AF, **2023-06-02**, **0-1**, HT **0-1**, source
line **570**, round 38, no administrative annotation. The existing directly inspected
LFP penalty decision dated **2023-06-12** is retained separately, not used to rewrite
numeric fields or source date. Effective availability remains null. Phase 5 must
establish interruption context, numerical on-field versus legal result, appeals
and finality, and any appropriate result-availability semantics.

### Valenciennes–Béziers, 2018/19

Original **2019-04-19**, **5-6**, source line **527**, round 33. All numeric fields are
valid; unusual magnitude alone is not an error. Phase 5 should corroborate teams,
actual date and full-time result with independent contemporary or official evidence.

### Cancellations and scheduling

2019/20 remains **380 source slots = 280 scored + 100 explicitly cancelled**.
Cancellation nulls, literal headings, source rounds and provenance are unchanged.
The existing LFP aggregate evidence is carried unchanged. Phase 5 should verify
cancellation context and any material exceptional cases without pretending that
an aggregate document verifies every fixture. For the 23 scheduling contexts,
prioritize the 25 outliers; validate round-level explanations separately from
individual-match certification. Review the 33 additional order-reversal endpoints
without assuming their dates are incorrect.

## Identity and Ligue 1 compatibility

The modern window contains **47 literal team labels**; NFC/casefold and diagnostic
accent-fold checks found no within-window collisions. **29 exact labels** also
occur in the protected Ligue 1 screened CSV; **18 do not match that CSV exactly**.
This is a string comparison only, not a finding that those clubs never played
Ligue 1, nor proof that identical labels certify historical continuity.

AC Ajaccio and Gazélec FC Ajaccio are preserved as distinct entities. No explicit
reserve-team suffix was detected; reserve/first-team status still needs evidence
if an ambiguous source is found. Diagnostic cross-league name groups and ten
continuity-review labels are retained separately: AC Ajaccio, AC Arles-Avignon,
FC Annecy, Gazélec FC Ajaccio, Red Star FC, SC Bastia, Stade Brestois 29,
US Créteil-Lusitanos, US Quevilly-Rouen and Évian Thonon Gaillard. These are review
leads only. Abbreviations, predecessor/successor clubs and sporting continuity
must be verified season-by-season; no global aliases or club mergers are applied.
All labels and source-bound occurrences remain recoverable from the full report.

## Outside-population sources, coverage and rights

The **2025/26 snapshot is not included** in the 4106: it remains 306 slots / 116
score-bearing / 190 unscored. Boulogne replacing Ajaccio, the separately preserved
wide round, and unscored SC Bastia–Stade Lavallois [postponed] on 2025-10-24 remain
unchanged in Phase 2 evidence. No new revision or supplementary result was acquired.

The full target remains 1990/91–2025/26; **24 older seasons 1990/91–2013/14** still
lack an approved complete primary source. The RSSSF 1998/99 original and its
round-heading proxies, unresolved return-score orientation, aggregate discrepancies
and diagnostic-only spelling mappings remain frozen. No older records are parsed
into this validation population, repaired, supplemented or standardized.

Pinned notices and source attributions remain preserved. OpenFootball CC0 applies
to rights held; upstream provenance/third-party rights are not warranted. RSSSF
copying/attribution terms do not establish training permission. Technical validity,
independent historical confidence, model suitability and redistribution/training
clearance remain separate; no model-training clearance is declared.

## Reproducibility and tests

New public files: scripts/validate_ligue2_structure.py,
tests/test_ligue2_structure.py and this document. PLANNING_LOG.md appended only.
All Phase 2–3 scripts/tests/docs and original evidence remain unchanged.
Private outputs: phase4_protected_before.json, phase4_structural_validation.json,
phase4_review_queue.json, phase4_reproducibility.json, verification_phase4 logs/XML
and phase4_final_verification.json. No standardized CSV or application data output.

```sh
python -B -m scripts.validate_ligue2_structure --init
python -B -m pytest -q -p no:cacheprovider tests/test_ligue2_structure.py
python -B -m pytest -q -p no:cacheprovider tests
```

Fresh verification: **63 new synthetic tests; 137 focused Ligue 2; 1429 non-UI;
seven app/launcher; 1436 complete repository tests passed**, zero failures/errors/
skips. Existing offline Python 3.13.12 temporary environment used, with declared
Python >=3.11 compatibility. No installation or original .venv changes.
Tests cover lossless bindings, malformed grammar, score/halftime/cancellation
conflicts, incomplete versus cancelled semantics, full synthetic 380-pair/38-round
coverage, duplicate/missing fixtures, Unicode labels, chronology overlaps, separate
administrative dates, frozen evidence and raw/category/member reconciliation.

A separate fresh process regenerated the complete report and queue into safe
temporary storage and compared bytes and SHA-256 against saved outputs. The frozen
Phase 3 inventory also regenerated identically. All source receipt/Git blob and
protected fingerprint checks passed. Exact hashes and paths are retained privately
in phase4_reproducibility.json. Git-ignore safeguards and unchanged HEAD/index
were verified; no private files are tracked or staged.

## Stopping point

Phase 4 structural validation is complete. No source correction or historical
eligibility/date policy is proposed as an implemented decision. Phase 5 should
independently review reproducibly selected ordinary matches across all eleven
seasons, the two administrative cases, unusual score, 23 scheduling contexts and
25 diagnostic outliers, source-order chronology, cancellations and identity groups.
Preserve all unresolved cases. No acquisition, Phase 5 work, standardization,
training or Git publication is authorized by this completion.
