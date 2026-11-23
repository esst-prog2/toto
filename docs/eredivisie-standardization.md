# Eredivisie — Phase 7 screened standardization and complete audit archive

Completed 2026-11-23 in the original toto worktree on `feature/data-collection`, HEAD `4f8c64433cf6168a06dbde0102e822ce6d2eeffa`. Phase 6 decisions were approved without modification. This phase implements those decisions only: no acquisition, new historical corrections, application integration, training, staging, publication or Phase 8 review.

## Exact private output paths

All paths are relative to the original toto worktree and remain Git-ignored:

* `data/private/netherlands/eredivisie/eredivisie_standardized_1990_2026.csv`
* `data/private/netherlands/eredivisie/eredivisie_audit_archive_1990_2026.json`
* `data/private/netherlands/eredivisie/eredivisie_exceptions_1990_2026.json`
* `data/private/netherlands/eredivisie/eredivisie_standardization_manifest.json`

The CSV is the screened candidate dataset. The JSON archive preserves every original source observation, including nonselected comparators, and a separate complete unique-fixture view. The exceptions report preserves all dispositions, special decisions, evidence references and scheduling/identity uncertainty. The manifest binds inputs, producing code, schema, provenance, prior collision checks and output hashes.

## Independent two-level reconciliation

Original bytes were checked through the approved policy regeneration and underlying independent raw parser before projection. Reconciliation failures stop generation; no rows are silently dropped to force expected totals. A separate standard-library verification process independently read the final CSV, archive, policy registries and prior datasets, checking every source-to-fixture mapping, physical source hash/blob/line and exact CSV subset.

| Accounting level | Completed-candidate linkage | HOLD OUT linkage | NOT PLAYED linkage | Total |
|---|---:|---:|---:|---:|
| Original source observations | 13,005 | 5 | 74 | 13,084 |
| Unique fixture slots | 10,939 | 3 | 74 | 11,016 |

All 2,068 overlapping representations remain in the archive; they do not become additional fixtures. Exactly 11,016 source representations are selected by the hierarchy, but only 10,939 selected candidate observations project into the CSV. Nonselected comparator observations retain their original conflicting or matching values. Their candidate linkage is a property of their parent fixture, not approval of every raw comparator value. There are zero other exclusions.

The target contains 10,636 historical and 2,448 modern observations: 13,009 score-bearing and 75 null-score slots. The complete historical original remains unchanged at 20,776 rows across 69 seasons, including every out-of-target record; only the 35 target historical seasons are duplicated in this target archive. The separate modern 2025/26 season supplies the 36th represented season.

## Shared schema, importer and deterministic identities

The CSV uses the established exact eight-column order:

```text
match_id,date,league,season,home_team,away_team,home_goals,away_goals
```

Canonical league is `Eredivisie`; seasons retain `YYYY/YYYY`. Dates are canonical ISO days, scores are nonnegative integers and home/away assignments retain the selected original labels. No global alias, reserve-team equivalence or predecessor/successor merger is applied. Competition scope is checked against historical tier 1 and modern Eredivisie regular-season context; cup/playoff/other-stage projections are rejected. Structural scope does not independently certify every historical event.

Approved projections go through the existing `standardize_england_results.convert_rows` bridge with explicit league/tier/division metadata, invoking the shared historical importer, public loader and validation. Any rejection, deduplication, changed fact or conflict fails the conversion. SHA-256 match IDs follow the shared compact UTF-8 JSON algorithm over `[league, season, date, home_team, away_team]`; they are distinct from Phase 6 internal fixture-policy IDs. CSV output sorts by league, season, date, home and away, uses deterministic UTF-8/LF serialization and roundtrips byte-identically. Reversing input plans produces identical bytes.

All 10,939 screened IDs are unique. Collision checking intentionally covered a conservative superset of the ten completed competitions’ screened records: **13 protected CSV files** comprising ten screened historical standardized CSVs (**116,988 distinct IDs**), two ongoing-season CSVs (168 Championship 2026/27 and 90 Premier League 2026/27 records), and one Serie B audit CSV (12,297 IDs already screened plus five additional exceptional-record IDs). The files contain **129,548 rows before deduplication**, yielding **116,988 + 168 + 90 + 5 = 117,251 distinct protected IDs**. There are **zero cross-competition collisions**. Prior file names, SHA-256 values and row counts are recorded in the private manifest. This prior-ID count is a collision-check population, not a new claim about completed historical totals.

## Approved source selection and exceptional fixtures

The historical CSV remains primary for 1990/91–2024/25; pinned OpenFootball is primary for 2025/26 and the sole explicit original for the 74 unplayed 2019/20 slots. The 2,068 exact scored source correspondences remain season- and fixture-bound. Every original has one source identity, one unique fixture link, a selected/comparator role and the exact approved decision ID. The hierarchy is not a claim of upstream independence or universal accuracy.

| Policy | Season | Original dates / scores | Screened treatment |
|---|---|---|---|
| Groningen–Ajax | 2022/23 | Historical 2023-05-14 and modern 2023-05-16; both 2–3 | Exactly one 2–3 row dated **2023-05-16**. May 14 interrupted event and both source dates remain in provenance. |
| NEC–Vitesse | 2023/24 | Both 2023-10-01; historical 1–3, modern 1–2 | Exactly one **1–3** row. Original modern 1–2 remains searchable in archive; no other score is corrected. |
| Ajax–Feyenoord | 2023/24 | Interruption 2023-09-24; sources already date completion 2023-09-27, 0–4 | One 0–4 row on 2023-09-27; no fictitious source-date correction. |
| RKC–Ajax | 2023/24 | Interruption 2023-09-30; sources already date completion 2023-12-06, 2–3 | One 2–3 row on 2023-12-06. |
| AZ–NEC | 2023/24 | Interruption 2023-10-29; sources already date completion 2023-12-06, 1–2 | One 1–2 row on 2023-12-06. |
| Heracles–Groningen | 2024/25 | Interruption 2024-12-21; sources already date completion 2025-01-28, 1–1 | One 1–1 row on 2025-01-28. |
| NAC–Heerenveen | 2025/26 | Modern line 509: 2026-05-10, null, `[cancelled]`; documentary completion 2026-05-11, 2–0 | HOLD OUT. No 2–0 row or source supplementation. Historical completion context is separate from unresolved supplemental-use permission. Not NOT PLAYED. |
| Feyenoord–VVV | 2018/19 | Both source dates 2018-12-06, 4–1; original interruption 2018-11-04 | HOLD OUT under approved material completion/availability evidence limitation. Reported completion remains separate from verified completion. |
| Vitesse–Sparta | 2021/22 | Both source dates 2022-04-19, 0–1; interruption 2022-03-04 | HOLD OUT under the approved material chronology limitation. No unsupported effective availability is assigned. |

Each exception is selected by the approved source IDs and validates the exact original dates, scores, participants and historical-review binding. Final projections are compared against freshly recomputed Phase 6 decisions, not merely against saved counts. The archive contains the full decisions and evidence references from the frozen review. The following exact HOLD OUT decision IDs are retained:

* VITESSE_SPARTA (2021/2022): `ERE-P6-8b3d613bf922b5d88653674a44256c63063ad64ce98c6f3ebbb9ad0e284b6ab0`; 2 original observation(s).
* NAC_HEERENVEEN (2025/2026): `ERE-P6-9ce6cd87a4b5bb4968ab0a3589fca2de60a8b13eee7da8ffb32e5337acc630a3`; 1 original observation(s).
* FEYENOORD_VVV (2018/2019): `ERE-P6-ef51a2a0d9864f71cb4955b193772fa2067dc9f584f2c63a1a6ff23b3f651bb1`; 2 original observation(s).

These three fixtures account for exactly five original observations and remain absent from the screened set. No other fixture is omitted for weak sampling evidence, wide scheduling spans, source-order reversals or unusual valid scores.

## 2019/20 coverage and cancellation semantics

The unique view reconciles 306 original season slots: **232 completed results in the screened CSV and 74 NOT PLAYED fixtures**. Each of the 74 unplayed slots has one explicit modern null-score cancellation original and no historical CSV row. Historical absence and explicit cancellation are retained as distinct source-coverage facts, not counted as two fixtures. `source_coverage.historical_absence` marks this specific approved 2019/20 missing-pairing condition; it is not a blanket description of historical-source coverage in other seasons.

No unplayed score is fabricated. Played records are not classified as universally annulled because the season stopped. NAC's later cancellation annotation remains associated with its separate HOLD OUT and does not enter the 74 NOT PLAYED total.

## Complete archival and uncertainty preservation

The source-observation archive contains all 13,084 target originals exactly once, including original CSV fields or text row, literal physical source bytes decoded without stripping, file path/URL, pinned revision, Git blob, original SHA-256, physical line/range and record hash. Every archive original is checked against its approved source-policy binding and its source bytes. The complete nine immutable source files remain separate and protected.

Each original links to its unique fixture, exact decision, selected/comparator role, approved standardized projection where applicable, chronology, confidence, source disagreements and evidence. The separate 11,016-fixture view contains the complete approved decision and zero or one screened projection per fixture. Thus the selected NEC score is visible alongside both raw scores, and the Groningen output date is visible alongside both raw dates. Comparator projections are linked views of the approved unique result; they never overwrite the comparator's `original` fields or add CSV rows.

All 25 wide-round contexts / 225 members, 16 reversal pairs / 32 endpoints, 410 flagged observations, 452 Phase 5 registry observations and the 47 literal labels remain represented through the embedded registry, context/identity assessment and evidence inventory. The frozen classifications remain 18 fully corroborated, 196 partial, one contradicted and 237 unresolved source observations. No historical-confidence upgrade or global mapping is performed. The two out-of-target 1979/80 PEC Zwolle observations remain in the unchanged historical source file, outside this target archive.

## Chronological gate and future-consumer obligations

Phase 6 chronology is reused without alteration. The archive distinguishes source dates, original scheduled/kickoff/interruption context, actual or reported completion, unknown administrative publication/finality, effective availability and ordinary source-date proxies. No publication timestamp is manufactured.

`PredictionGate` first regenerates and byte-validates all six saved Phase 6 policy artifacts against protected sources and evidence. Supplied decisions must equal trusted regenerated entries. Its strict day-level requirement remains:

```text
completion_day <= defensible_availability_day < prediction_day
```

Same-day use is rejected without verified intraday order. Future results, unknown required availability, unresolved administration, HOLD OUTs, unapproved supplements and altered/incomplete decisions cannot pass. Source-to-fixture/projection tampering is additionally rejected by this phase's exact subset and archive-binding checks.

The actual-population check confirms **six** accepted exceptional fixtures have day-level eligibility at the 2026-11-23 cutoff, **zero same-day eligible records** and **zero training-authorized decisions**. Ordinary source dates remain proxies and fail the availability gate until separately established; they are nevertheless valid historical screening candidates under the approved policy. Candidate inclusion does not authorize use before a prediction date. **The CSV alone does not enforce leakage-free training or evaluation.** Rights clearance remains separate and the application has not been changed.

## Season-level screened scope

| Season | Screened | HOLD OUT | NOT PLAYED | Unique slots |
|---|---:|---:|---:|---:|
| 1990/1991 | 306 | 0 | 0 | 306 |
| 1991/1992 | 306 | 0 | 0 | 306 |
| 1992/1993 | 306 | 0 | 0 | 306 |
| 1993/1994 | 306 | 0 | 0 | 306 |
| 1994/1995 | 306 | 0 | 0 | 306 |
| 1995/1996 | 306 | 0 | 0 | 306 |
| 1996/1997 | 306 | 0 | 0 | 306 |
| 1997/1998 | 306 | 0 | 0 | 306 |
| 1998/1999 | 306 | 0 | 0 | 306 |
| 1999/2000 | 306 | 0 | 0 | 306 |
| 2000/2001 | 306 | 0 | 0 | 306 |
| 2001/2002 | 306 | 0 | 0 | 306 |
| 2002/2003 | 306 | 0 | 0 | 306 |
| 2003/2004 | 306 | 0 | 0 | 306 |
| 2004/2005 | 306 | 0 | 0 | 306 |
| 2005/2006 | 306 | 0 | 0 | 306 |
| 2006/2007 | 306 | 0 | 0 | 306 |
| 2007/2008 | 306 | 0 | 0 | 306 |
| 2008/2009 | 306 | 0 | 0 | 306 |
| 2009/2010 | 306 | 0 | 0 | 306 |
| 2010/2011 | 306 | 0 | 0 | 306 |
| 2011/2012 | 306 | 0 | 0 | 306 |
| 2012/2013 | 306 | 0 | 0 | 306 |
| 2013/2014 | 306 | 0 | 0 | 306 |
| 2014/2015 | 306 | 0 | 0 | 306 |
| 2015/2016 | 306 | 0 | 0 | 306 |
| 2016/2017 | 306 | 0 | 0 | 306 |
| 2017/2018 | 306 | 0 | 0 | 306 |
| 2018/2019 | 305 | 1 | 0 | 306 |
| 2019/2020 | 232 | 0 | 74 | 306 |
| 2020/2021 | 306 | 0 | 0 | 306 |
| 2021/2022 | 305 | 1 | 0 | 306 |
| 2022/2023 | 306 | 0 | 0 | 306 |
| 2023/2024 | 306 | 0 | 0 | 306 |
| 2024/2025 | 306 | 0 | 0 | 306 |
| 2025/2026 | 305 | 1 | 0 | 306 |

## Independent regeneration and tests

All four outputs were regenerated by a separate fresh CLI process into a safe temporary directory, without overwriting saved outputs. Every byte and SHA-256 matched:

| Artifact | Bytes | SHA-256 | Comparison |
|---|---:|---|---|
| eredivisie_audit_archive_1990_2026.json | 103609483 | `870a8b030da1567a4c2960a21cf5687b0c7f1e8afb09a14f041b321eecdd1f68` | Byte-identical |
| eredivisie_exceptions_1990_2026.json | 1806730 | `4513a601fa70daeffb55d91d1b6d19b93b2da809757f834463cd6e73ce4169e1` | Byte-identical |
| eredivisie_standardization_manifest.json | 14598 | `e46ab339056bee3c9fe90eb74098fc809970083238c39e00c8dcabbacb598a3c` | Byte-identical |
| eredivisie_standardized_1990_2026.csv | 1369358 | `927feed07901850f8d88bd8349b1eb292f2eb2af2078ac3cec044f2402421531` | Byte-identical |

All six frozen Phase 6 policy artifacts also regenerated byte-identically. A separate standard-library CSV/JSON verifier independently checked 13,084 originals, 11,016 unique dispositions, exact CSV/approved-policy equality, all nine source SHA/blob/physical-line bindings, every selected-source role, the 410 flags, 452 historical-review entries, both source conflicts, NAC's null original, all HOLD OUTs, 232 played 2019/20 results and prior-dataset collision hashes.

Fresh final-state test results (overlapping selections, not additive):

| Selection | Passed | Failures / errors / skips |
|---|---:|---|
| acquisition_importer | 618 | 0 / 0 / 0 |
| app_launcher | 7 | 0 / 0 / 0 |
| eredivisie | 287 | 0 / 0 / 0 |
| full | 1846 | 0 / 0 / 0 |
| historical_review | 32 | 0 / 0 / 0 |
| non_ui | 1839 | 0 / 0 / 0 |
| policy | 78 | 0 / 0 / 0 |
| standardization | 62 | 0 / 0 / 0 |

The 62 new synthetic standardization tests cover the exact schema/shared importer, scoped correspondence, overlap deduplication, every approved exception and HOLD OUT, the 74 unplayed slots, untouched conflicting originals, reserve/identity guards, deterministic serialization/IDs, subset protection, physical provenance and full archive accounting. Phase 6 tests freshly rerun the complete chronological/integrity rejection cases, including future, unknown, same-day and unresolved-administrative outcomes. An initial synthetic sorting fixture accidentally had identical opponents; that test-data error was corrected before the final passing runs. No match-data discrepancy or new historical correction was found.

Tests used the previously established external Python 3.13.12 environment with bounded timeouts and no project bytecode/pytest-cache writes. No dependency was installed, and the original `.venv` was not altered.

Reproduction without acquisition:

```sh
PYTHONPATH=src:. python -B scripts/standardize_eredivisie_results.py --check
# To regenerate into an existing safe empty temporary directory:
PYTHONPATH=src:. python -B scripts/standardize_eredivisie_results.py --write --output-directory /path/to/temporary-directory
```

`--init` creates the protected baseline once after validating the approved Phase 6 receipt. Writes are exclusive; changed existing outputs are refused. Generated artifacts and source data stay private.

## Protected state, changed files and stopping point

Protected verification passes for the ten earlier competitions (839 previous private / 207 public fingerprint entries), all nine Eredivisie originals and 168 frozen Phase 2–6 entries, including all earlier receipts, evidence and policy outputs. The planning-log prefix is preserved. HEAD and Git index remain unchanged; nothing is staged. Application and promotional-worktree files were not touched. All private files are ignored and untracked; no private dataset was published.

Public Phase 7 additions are `scripts/standardize_eredivisie_results.py`, `tests/test_eredivisie_standardization.py`, this report and append-only `PLANNING_LOG.md` entries. Private additions are the four named outputs, `phase7_protected_before.json`, `phase7_independent_reconciliation.json`, `phase7_reproducibility.json`, `phase7_test_summary.json`, `verification_phase7/` logs/XML/status and the final verification receipt. Earlier public work and evidence remain unchanged.

The dataset represents 36 seasons but is not entirely independently historically certified. The three HOLD OUTs, incomplete individual corroboration, club-identity questions, ordinary availability limitations and upstream source-independence uncertainty remain open. Historical noncommercial/GPL metadata and OpenFootball CC0 do not establish blanket downstream rights. Redistribution and model-training permission remain unresolved; training and application integration are not authorized.

The measured artifacts are ready for a separately approved **read-only Phase 8 review**. Phase 8 has not begun. No staging, commit, push, merge, rebase or new acquisition was performed. Stop after Phase 7 for approval.
