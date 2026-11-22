# Segunda División Phase 4: independent comprehensive structural validation

Date: 2026-11-22. Original `toto` worktree, branch `feature/data-collection`.
HEAD unchanged: `052d25185182f1edbb80fac51cafbb59e0acf7cf`.

## Outcome and units

The independent parser reconciles **all 6,006 raw fixture observations** with
Phase 3, field by field and physical source line. There are **5,997 score-bearing,
structurally consistent observations**, **nine incomplete observations**, **zero
fixture-level structural contradictions**, and **zero season-level error events**.
Missing FT scores are a separate incompleteness class, not invented results or
malformed numeric scores. All 6,006 fixture slots have coherent competition,
round, club and directed-pair topology. This does not make all 6,006 complete
historical matches or all 5,997 scored observations eligible training records.

The **773 unique review observations** comprise 764 score-bearing and nine
incomplete observations. The remaining 5,233 have no selected review flag; that
does not certify their historical facts. Flags are not corrections or exclusions.
Source-marked administrative awards remain in the score-bearing count.

No source acquisition, historical decision, score/date/name correction, exclusion,
standardized export, application modification, training or Git publication occurred.

## Preservation and independent implementation

Before work, `phase4_protected_before.json` froze **52 Phase 2–3 artifacts**:
44 private files plus eight public scripts/tests/documents. The existing planning
log is protected by an append-only prefix. Earlier baselines also verify all
**493 pre-Segunda private files and 145 tracked public files**, covering all seven
completed competitions and application code/data. All hashes match.

`scripts/validate_segunda_structure.py` implements its own raw Football.TXT parser
and validator. It does **not** call the Phase 2/3 parser, assessment function or
saved totals to establish source counts. Synthetic integration tests explicitly
disable the earlier parser/validator and deliberately supply false saved totals;
the new implementation still derives the actual observations.

It verifies:

- Exact acquired path scope, revision-pinned receipts, byte sizes, SHA-256 and Git
  blob identity; all originals remain at commit
  `80035a93dd4920985af52aa097a54a6fb888563b`.
- UTF-8, competition/season titles, stage grammar, round numbering and count
  headers. Unexpected/nonregular stages or unknown rows fail with line diagnostics.
- Both `home v away score` and score-between-teams formats, original FT/HT strings,
  nonnegative digit-string goals within the shared signed-64-bit range, missing
  values, and HT/FT consistency. No numeric conversion overwrites source strings.
- Every source date, weekday, season boundary, explicit/inferred year, optional
  kickoff time, source heading and physical line. The 2019/20 extended calendar
  explicitly permits July/August 2020, without changing a source date.
- Each of 42 rounds has 11 fixtures and each club once; every directed pairing
  appears exactly once; home/away allocations are balanced. Each half-season has
  all 231 unordered opponent pairs once.
- Names, control/replacement characters, NFC/case collisions, accent/punctuation
  review candidates, reserve distinctions, same-day collisions and short-rest leads.
- Original raw line hashes (including line endings), source audit IDs, provenance
  and exact binding of all carried Reus and interruption/postponement context.

For all 6,006 observations, the new parser's date, names, FT/HT strings, goals,
round/stage, kickoff, annotation and literal raw record must agree with Phase 3.
The originals, rather than that agreement, establish the new totals. A disagreement
or changed binding raises explicitly; it is never silently repaired or discarded.

## Season-level results

Each season has **462 observed/expected regular fixture slots, 22 clubs and zero
playoff/other-stage records**. Directed pairings, halves and source bindings pass.

| Season | Observed | Score-bearing | Incomplete | Structurally invalid | Unique review flags | Wide rounds |
|---|---:|---:|---:|---:|---:|---:|
| 2012/13 | 462 | 462 | 0 | 0 | 82 | 0 |
| 2013/14 | 462 | 462 | 0 | 0 | 82 | 0 |
| 2014/15 | 462 | 462 | 0 | 0 | 54 | 1 |
| 2015/16 | 462 | 462 | 0 | 0 | 52 | 1 |
| 2016/17 | 462 | 462 | 0 | 0 | 62 | 2 |
| 2017/18 | 462 | 462 | 0 | 0 | 100 | 2 |
| 2018/19 | 462 | 462 | 0 | 0 | 21 | 0 |
| 2019/20 | 462 | 462 | 0 | 0 | 44 | 4 |
| 2020/21 | 462 | 462 | 0 | 0 | 77 | 7 |
| 2021/22 | 462 | 462 | 0 | 0 | 52 | 1 |
| 2022/23 | 462 | 462 | 0 | 0 | 42 | 0 |
| 2023/24 | 462 | 462 | 0 | 0 | 52 | 1 |
| 2024/25 | 462 | 453 | 9 | 0 | 53 | 4 |
| Total | 6,006 | 5,997 | 9 | 0 | 773 | 23 |

All 5,331 supplied halftime strings are internally consistent with FT; absent
optional HT values are not fabricated. No same-team/same-date collision or team
rest interval of one day or less was found. Seventeen reversals in physical source
date order are recorded: round-ordered files are not a chronological event stream.
They are storage-order diagnostics, not proof of incorrect match dates.

## Deduplicated fixture-level review queue

Private file: `data/private/spain/segunda_division/phase4_review_queue.json`.
Each item contains a stable source audit ID, season, file/revision/SHA-256, physical
line and raw line hash, original values, chronology metadata, categories and
structural-error codes. It has **773 distinct IDs**, one item per observation.
No standardized match IDs or eligibility decisions are generated.

| Category | Unique observations in category | Relationship |
|---|---:|---|
| Missing FT score | 9 | All in 2024/25 round 42 |
| Source-marked administrative award | 21 | All Reus 2018/19; also have source-annotation category |
| Wide-round context | 253 | All fixtures in 23 rounds |
| Diagnostic date outlier | 30 | Subset of the 253; outside densest seven-day cluster |
| Known interruption/postponement | 2 | Rayo–Albacete and Deportivo–Fuenlabrada; both within the 30 outliers |
| Reserve-team identity review | 498 | Ten also belong to wide-round context |
| Unusual score review | 2 | Internally valid 6–6 and 6–4; outside the other categories |

Do not sum those category counts. The deduplicated union is:
`9 + 21 + 253 + 498 + 2 − 10 = 773`.
Exact combinations and their counts are stored in `overlap_combinations`.
The 30 outliers, two known cases and 21 source annotations add no extra fixtures.

Diagnostic thresholds are explicit and synthetic-tested: wide round at least
14 days, largest seven-day cluster with earliest-start tie-breaking (as in La Liga),
short rest at most one day, unusually high score at least eight for one side or
ten total. They identify review leads only; they are not evidence of an error.

The two new score leads are **CA Osasuna–RCD Mallorca 6–4, source 21 September
2014, line 82**, and **CD Numancia–CD Lugo 6–6, source 20 December 2014, line 291**.
Their scores and goal-derived outcomes are internally consistent and unchanged.
Phase 5 must seek independent evidence rather than correcting an unusual value.

All 23 modern wide-round spans, dates and affected fixtures independently match
Phase 3. All six original Phase 2 flags remain preserved, including the outside-
scope 2025/26 and RSSSF flags; these are not silently folded into the 13 seasons.
The complete scheduling table remains in `segunda-division-inventory.md`; the new
private report adds independently calculated source lines and diagnostic outliers.

### Nine incomplete observations

All are 2024/25 round 42; their scores remain null. Source dates may be schedules,
not verified actual playing dates. The exact source line and raw text remain in
both outputs and the original file.

| Source line | Source date | Home | Away |
|---:|---|---|---|
| 745 | 2025-05-31 | Málaga CF | Burgos CF |
| 747 | 2025-06-01 | SD Huesca | CD Eldense |
| 748 | 2025-06-01 | UD Almería | CD Tenerife |
| 749 | 2025-06-01 | FC Cartagena | CD Mirandés |
| 750 | 2025-06-01 | Deportivo La Coruña | Elche CF |
| 751 | 2025-06-01 | Real Oviedo | Cádiz CF |
| 752 | 2025-06-01 | Levante UD | SD Eibar |
| 753 | 2025-06-01 | Racing Santander | Granada CF |
| 754 | 2025-06-01 | Córdoba CF | Albacete |

## Chronology: facts, context and unresolved availability

All 6,006 records preserve source date, raw date heading and year basis.
**72 observations** inherit headings containing an explicit calendar year;
**5,934** resolve an omitted year from the stated season window and weekday.
No missing day/month was fabricated. Parsed ISO dates are source interpretations,
not assertions that all actual kickoff/completion dates are historically verified.

Separate chronology fields preserve source kickoff times, scheduled-date proxies,
original kickoff dates, actual completion/playing dates and administrative context.
**No effective-result-date policy is assigned during Phase 4**: all corresponding
fields are null and explicitly labelled policy-pending. This is not a decision
that ordinary fixtures are erroneous or must be excluded.

| Availability classification | Observations | Meaning |
|---|---:|---|
| Unverified source playing-date proxy | 5,974 | Ordinary source observation; no population historical certification |
| Unresolved administrative result/availability | 21 | Reus source-marked awards; nominal source dates do not establish when awards became known |
| Missing result, no availability date | 9 | A complete result cannot be made available from absent scores |
| Documented completion context, policy pending | 1 | Rayo–Albacete: kickoff 2019-12-15, completion/source date 2020-06-10, source 1–0 |
| Documented playing-date context, score certification pending | 1 | Deportivo–Fuenlabrada: original schedule 2020-07-20, actual/source date 2020-08-07, source 2–1; prior evidence limitations unchanged |

Reus's 28 January 2019 expulsion decision is contextual metadata, not the verified
decision/availability date for every individual 0–1/1–0 award. In particular, a
nominal 19 January award date must not silently make an administrative result
available before the operative decision. On-field and source administrative
result fields remain distinct; no missing played score is invented.

Future chronological evaluation must use only results known strictly before its
prediction date, not source order, a nominal award schedule or the earlier kickoff
of an unfinished match. No such evaluation is implemented here. Phase 5 evidence
and later approved policy must establish effective dates; Phase 4 does not grant
rights, historical certification or training suitability.

## Labels, reserves and identities

All 64 exact modern labels remain unchanged. There are no NFC/case collision
groups and no accent/case/punctuation variant groups in these 13 source files.
The report retains entered/left labels between adjacent seasons without treating
ordinary promotion/relegation as spelling changes or inferring legal continuity.

The 498 reserve-related observations involve `Athletic Club B`, `FC Barcelona B`,
`Real Madrid Castilla`, `Real Sociedad B`, `Sevilla Atlético` or `Villarreal CF B`.
Those labels remain distinct from their first teams and from one another. Review
flags indicate identity safeguards, not suspicion that all those results are wrong.
Cross-source aliases and historical successor relationships remain for evidence
review; no global mapping or parent/reserve merger was applied.

## Reproducibility, tests and artifacts

Public files created: `scripts/validate_segunda_structure.py`,
`tests/test_segunda_structure.py`, this document. `PLANNING_LOG.md` only appends.
All eight earlier Segunda public files and all earlier competition files are unchanged.

New private files: `phase4_protected_before.json`,
`phase4_structural_validation.json`, `phase4_review_queue.json`,
`phase4_verification.json`. The area contains 48 private files after this phase;
all 541 project private files remain Git-ignored, with none tracked or staged.

| Output | Bytes | SHA-256 |
|---|---:|---|
| `phase4_structural_validation.json` | 10,559,168 | `fcac9970e945e8972c879f4e2ed27e971e498f8d9fb8d04cb4b3914fbeb95e1e` |
| `phase4_review_queue.json` | 1,576,022 | `a989f7ca29e56b522d98554b5f56dcd5160cba8ae67bb58d551afa80b354cd8a` |

Two fresh builds were written to safe temporary storage and compared against both
saved artifacts by actual bytes and SHA-256: identical. The Phase 2 assessment and
Phase 3 inventory also still regenerate byte-identically. Earlier baseline/source
receipts, Git blobs, source-line bindings and protected prefixes pass.

**38 new tests / 89 combined Segunda tests passed. 898 full repository tests passed
in 12.32 seconds**, including all seven app/launcher tests. These counts overlap.
Tests cover independent grammar, missing values, scoring contradictions, round
topology, chronology, Unicode/identity checks, source/context binding, deduplication,
tamper detection and byte-deterministic builds. No skipped/unverified test gap remains
in that full run. Tests used the existing temporary Python 3.13 environment outside
iCloud with a 180-second timeout; no dependency installation or environment repair
was needed during this phase, and the original `.venv` was untouched.

```sh
PYTHONPATH=src:. python -B scripts/validate_segunda_structure.py --init
PYTHONPATH=src:. python -B scripts/validate_segunda_structure.py --check
PYTHONPATH=src:. python -B -m pytest tests/test_segunda_structure.py -q -p no:cacheprovider
```

Initial report creation refuses existing outputs. Subsequent `--check` runs compare
without replacing them. Reproduction requires retained private Phase 2–3 evidence.

## Phase 5 queue, coverage and permissions

Phase 5 should independently verify a reproducible all-season sample and prioritize
the nine missing results, 21 administrative awards, 23 scheduling cases/30 outliers,
two known interrupted/postponed cases, the 6–6 and 6–4 scores, and the identity review
catalog. A contextual explanation of a round must not be represented as individual
verification of every affected fixture. Preserve unresolved facts and do not apply
corrections/exclusions without later approval.

The full Segunda historical target remains unfinished:

- 1990/91–2011/12: 22 seasons still lack an approved complete historical source.
  The preserved RSSSF sample's 379 round-date proxies are not verified fixture dates.
- 2024/25: nine scores remain absent in the approved pinned modern source.
- 2025/26: the separate frozen sample remains 131 scored / 331 unscored; it was
  not downloaded again or included in the 13-season validation.

No additional historical source was acquired. OpenFootball CC0 applies to rights
held, without blanket upstream-rights clearance; RSSSF attribution/reserved-rights
limitations remain preserved for its outside-scope sample. Technical completeness,
historical confidence, redistribution and model-training permissions remain separate.
**Model-training clearance remains unresolved. Stop before Phase 5 pending approval.**
