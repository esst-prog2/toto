# Homework 6 review log

## Review 1: Specification compliance

Date: 2026-10-17. Branch: `hw6-review`. Status: documentation changes completed; user approved the dedicated commit on 2026-10-17.

### Scope

Reviewed the entire tracked repository against README.md, AGENTS.md, the append-only PLANNING_LOG.md, all OpenSpec specifications and change artifacts, and other documented requirements. Examined runtime modules, offline scripts, tests, data artifacts, tracked build copies, and supporting documentation. Focused on undocumented features, missing requirements, prediction-rule inconsistencies, undocumented assumptions, and outdated documentation.

The user authorized documentation fixes for findings 1, 2, and 7 only. Findings 3–6 remain deferred to separate specialized reviews. No production Python, tests, prediction algorithm, historical data, or measurements were changed in this review. Earlier planning-log entries were preserved.

### Findings and disposition

Locations below refer to the repository at the initial review, before these documentation edits. OpenSpec paths are relative to `openspec/changes/build-synthetic-toto-mvp/` where indicated.

| ID | Finding and locations | Severity | Why it matters / recommended action | Disposition |
| --- | --- | --- | --- | --- |
| 1 | Superseded independent venue normalization remained in OpenSpec: `design.md:75`, `tasks.md:22`, `specs/match-outcome-prediction/spec.md:15` (OpenSpec paths). Current implementation pools venue rates at `src/toto_estimator/statistics.py:87`. | Medium | Following stale rules could undo the authorized correction. Document shared scales, pooled ties, and missing values while retaining the original design as superseded history. | Addressed through documentation only. |
| 2 | `README.md:36` gave the historical 40.000000% evaluation without distinguishing the current 41.578947% result in `data/real_spike_measurements.json:193`. | Medium | Readers could mistake historical performance for the current predictor's result. Label both versions, preserve baseline figures, and explain development-set reuse. | Addressed. |
| 3 | `build/lib/toto_estimator/statistics.py:87` retains independent venue scales, unlike the current source implementation. | Medium | Two tracked implementations can produce different results. Consider removing generated build output from version control and ignoring it. The normal Streamlit launcher selects `src/`. | Deferred: generated code duplication review. No build files or ignore rules changed. |
| 4 | `src/toto_estimator/service.py:14` bypasses historical validation for direct DataFrame input; negative/fractional goals can produce predictions, and missing fields can raise exceptions. Fractional values are truncated at `src/toto_estimator/statistics.py:17`. | Medium | The atomic workflow specification requires validation before prediction. Reuse source-independent validation at the public service boundary and return structured failures. | Deferred: historical-data validation review. |
| 5 | Empty historical inputs escape the error workflow at `src/toto_estimator/data.py:24`, `src/toto_estimator/statistics.py:72`, and `src/toto_estimator/service.py:57`: empty files raise `EmptyDataError`, and header-only history raises `KeyError: 'team'`. | Medium | Missing history should produce clear errors rather than crash. Handle empty parsing and zero-match aggregation with structured failures. | Deferred: empty-input error handling review. |
| 6 | `src/toto_estimator/ticket.py:49` reports invalid position structure generically, without identifying affected rows or duplicate/missing positions. | Low | The ticket specification requires actionable identification of affected positions. Report duplicate/out-of-range rows and missing positions. Dropdown users cannot introduce this structural error. | Deferred: ticket validation messages review. |
| 7 | `README.md:44` described real-data work and model refinement entirely as future work despite the completed offline adapter, evaluation, and normalization correction. | Low | Completed capabilities and remaining interactive-app work were unclear. Separate offline accomplishments from future integration and evaluation plans. | Addressed. |

No high-severity finding was identified. The real-data spike and shared normalization are intentional changes authorized in the planning log, not unauthorized features. Synthetic-only UI scope and below-baseline accuracy remain acknowledged limitations. No earlier planning decision was erased or rewritten.

### Specific documentation changes

- `README.md`: added a comparison table for original Homework 4 performance (152/380 = 40.000000%), current shared-normalization performance (158/380 = 41.578947%), and unchanged always-1 (175/380 = 46.052632%) and closing-Bet365 (227/380 = 59.736842%) baselines. Retained all-loaded statistics. Explained the fitting split, development reuse of 2023/24, and need for a later unseen season. Linked the investigation and current measurement artifact. Distinguished completed offline work from the synthetic UI and future real-team integration/model evaluation. Summarized current shared venue scaling.
- `openspec/changes/build-synthetic-toto-mvp/design.md`: marked the original six-independent-scale design as historical and superseded on 2026-10-08; documented current pooled venue bounds, unchanged overall scales, tie/missing-value behavior, fitting-only evaluation bounds, and unchanged rating composition. Clarified that the initial repository description was historical.
- `openspec/changes/build-synthetic-toto-mvp/specs/match-outcome-prediction/spec.md`: recorded the supersession and updated normalization requirements/scenarios for shared venue scales, pooled ties, individually constant but differing venue columns, and missing history. Left weights, thresholds, and eligibility rules intact.
- `openspec/changes/build-synthetic-toto-mvp/tasks.md`: retained the original completed task 4.2, annotated its supersession, and added a documentation reconciliation note referring to existing implementation and regression coverage.
- `openspec/changes/build-synthetic-toto-mvp/proposal.md`: added a historical scope note distinguishing the original MVP from subsequent authorized offline work and the normalization correction.
- `PLANNING_LOG.md`: appended the user's Review 1 scope and deferral decision; preserved all previous bytes.
- `REVIEW_LOG.md`: created this review record, including every finding, severity, disposition, and documentation action.

### Verification and handoff

The initial read-only review ran the existing suite with bytecode/cache writes disabled: 47 tests passed. This documentation-only follow-up does not rerun tests or regenerate measurements. Documentation values were checked against the committed measurement artifact and investigation report. `git diff --check` passed; repository diff inspection confirmed only the documentation files listed above changed and that the planning-log change is append-only. The user approved the dedicated Review 1 commit on 2026-10-17 with message `Review specification compliance and align documentation`, following branch, exact seven-file scope, and whitespace checks. Findings 3–6 remain open for later reviews. No branch change, push, or merge is authorized.

## Review 2: Architecture and duplicated code

Date: 2026-10-17. Branch: `hw6-review`. Status: all four approved fixes implemented and verified; user approved the dedicated commit on 2026-10-17.

### Scope

Reviewed the entire tracked repository for duplicated implementations, architectural inconsistencies, accumulated patches, and generated build artifacts, including the deferred build-copy finding from Review 1. Excluded ignored virtual environments and caches. The user subsequently authorized all four findings below to be addressed in this review. No prediction algorithm changes, new features, committed dataset changes, or measurement changes were authorized or made.

### Findings and fixes

Locations identify the pre-refactor review snapshot; moved code may now have different line numbers.

| ID | Finding and original locations | Severity | Why it matters | Fix applied |
| --- | --- | --- | --- | --- |
| 1 | Eight tracked modules under `build/lib/toto_estimator/`; obsolete independent scaling at `build/lib/toto_estimator/statistics.py:87` versus shared scaling at `src/toto_estimator/statistics.py:87`; missing build exclusion at `.gitignore:1`. | Medium | Seven identical copies and one divergent copy create competing implementations and repeated generated-file changes. | Removed all eight modules from Git tracking, retaining local ignored copies; added `/build/` to `.gitignore`. `src/` remains authoritative. Resolves the build-copy issue deferred as Review 1 finding 3. |
| 2 | Trimmed names in `src/toto_estimator/ticket.py:61` and `src/toto_estimator/service.py:20`, but original names passed into prediction at `service.py:43`. | Medium | A whitespace-padded valid team passed validation but raised an exception during prediction. | Added `data.normalize_ticket`, which copies input and normalizes team-name columns. The service establishes that representation before validation/history checks/prediction; loader and standalone validator reuse the same function. Removed local stripping from ticket validation and service iteration. No mutation of caller tickets. |
| 3 | Actual-outcome calculation duplicated at `src/toto_estimator/data.py:107` and `scripts/build_real_spike_dataset.py:129`. | Low | Two implementations of the same home-perspective rule could drift. | Added `src/toto_estimator/outcomes.py:outcome_from_goals`; loader and real adapter reuse it. Removed the adapter's private duplicate. Test expectations remain independent literal outcomes and independently chosen baseline counts. |
| 4 | Deterministic serialization and overwrite policy duplicated at `scripts/generate_synthetic_history.py:98,110` and `scripts/build_real_spike_dataset.py:229,348`. | Low | Serialization or overwrite-policy edits required synchronized changes despite byte-reproducibility requirements. | Added offline-only `scripts/artifact_io.py` with shared CSV serialization, overwrite checks, and parent-directory creation. Both scripts retain their existing public wrappers and reuse the utilities. Direct-script and package-module launches are supported without importing synthetic generator information into runtime code. |

The existing division between UI, service, validation, statistics, and prediction remains. Startup and standalone prediction checks retain their intentional safeguards. Committed generated datasets/checksums/measurement evidence remain tracked. Existing import bootstraps remain; no evidence established that they were obsolete. Historical-data validation, empty-input handling, and ticket-message improvements deferred from Review 1 remain outside this review; the ticket-name representation inconsistency above is resolved.

### Tests added

- `tests/test_service.py`: six parameterized home/away leading/trailing/tab/newline whitespace cases compare full workflow results against canonical input and assert that caller input is unchanged. Additional regressions check normalized duplicate/self-pair errors and structured unknown-team failure.
- `tests/test_outcomes.py`: independent literal expectations for home wins, away wins, scoreless draws, and scoring draws.
- `tests/test_artifact_io.py`: verifies Unicode UTF-8 bytes, CSV quoting, column order, and LF endings; four integration cases verify that either existing output blocks both writers without replacing it or creating the other file, while explicit force preserves dataset bytes and creates parent directories.
- Existing tests continue to cover exact synthetic/real artifact regeneration, checksum agreement, fixed predictor rules, fitting isolation, and Streamlit startup/prediction behavior. Independent expectations were not replaced by calls to the new production helper.

### Verification results

- Complete suite: `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m pytest -q -p no:cacheprovider` — **64 passed in 3.49s** (47 existing cases plus 17 new cases).
- `git diff --check` and `git diff --cached --check` passed, including staged build removals.
- Package resolution points to `src/toto_estimator/__init__.py`. Existing Streamlit AppTest and launcher regressions passed; package discovery and pytest still select `src/`. No build files remain in `git ls-files build/`.
- `src/toto_estimator/predictor.py`, `statistics.py`, and `config.py` are byte-identical to pre-review HEAD: prediction formula, weights, thresholds, normalization, and eligibility rules are unchanged.
- Reproduced original evaluation by loading the historical statistics implementation from parent of commit `d98c15e` into memory and using the existing fitting/evaluation pipeline: **152/380 = 40.000000%**, calls **154/77/149**. No checkout or historical source edit was needed.
- Reproduced current evaluation: **158/380 = 41.578947%**, calls **198/86/96**. Both versions retain always-1 **175/380 = 46.052632%** and closing-Bet365 favourite **227/380 = 59.736842%**; fitting uses 932 rows and evaluation uses 380.
- Ran both offline scripts through direct file execution and `python -m` execution into temporary directories. Synthetic CSV/checksum and real CSV/measurement JSON were byte-identical to committed artifacts in both launch modes.
- Compared every tracked `data/` file against HEAD bytes: unchanged, including raw sources, sample ticket, generated CSVs, checksum, and measurements.
- Final scope is limited to the eight build untracking entries, `.gitignore`, the two offline scripts, three runtime boundary/loader modules, two shared utility modules, three test files, and the two logs. Earlier planning-log content is unchanged; only new decisions were appended.

### Remaining concerns and handoff

All four approved architectural findings are addressed. No new behavior risk was identified by the regression, byte-comparison, and historical-evaluation checks. Local build copies remain ignored and may be regenerated; they are no longer versioned sources. Existing valid input behavior and all prediction results are preserved; padded direct-service team names now behave consistently. The user approved the dedicated Review 2 commit on 2026-10-17 with message `Review architecture and eliminate duplicated implementations`. Pre-commit verification again passed all 64 tests (3.39s), whitespace checks, exact review file scope, and build untracking/ignore checks. No push, merge, or branch change is authorized.

## Review 3: Error handling and input validation

Date: 2026-10-17. Branch: `hw6-review`. Status: all nine approved fixes implemented and verified; user approved the dedicated commit on 2026-10-17.

### Scope

Reviewed the entire tracked repository, tracing input failures through historical/ticket loaders, service orchestration, Streamlit, prediction, offline source adaptation, and artifact writing. Revisited deferred Review 1 findings 4–6. The user authorized all nine findings below, focused regression tests, and documentation; no formula changes, features, committed data/measurement changes, commit, push, merge, or branch switch were authorized.

### Findings and fixes

Locations refer to the pre-implementation Review 3 snapshot; refactored code may have moved.

| ID | Finding / original locations | Severity | Fix implemented |
| --- | --- | --- | --- |
| 1 | Historical validation bypassed at `src/toto_estimator/service.py:14`; `statistics.py:17` truncated fractional goals. Invalid history could produce successful predictions or uncaught exceptions. | Medium | Extracted `validate_historical_data` and applied it to CSV loading and direct service input. Shared shape checks reject unsupported input types, duplicate/missing columns, invalid dates, non-string/blank or identical opponents, invalid goals, and optional supplied results that are not 1/X/2 or disagree with goals. Retains legitimate extra columns and copies caller input. Resolves deferred Review 1 finding 4. |
| 2 | Empty files/header-only history escaped structured handling at `data.py:25`, `statistics.py:72`, `service.py:58`, and `app.py:39`. | Medium | Empty CSV text produces `DataValidationError`; zero-match history is rejected before statistics. Existing Streamlit startup error rendering handles these structured failures without new UI exception handlers. Resolves deferred Review 1 finding 5. |
| 3 | Unchecked numeric casts at `data.py:86,106,131,144` could wrap oversized goals/positions and change outcomes. | Medium | Shared exact integer parsing checks finite integral values and signed 64-bit representability before conversion. Decimal strings are not routed through floats; already supplied floats are checked using their exact represented value. Booleans and unsupported objects are rejected. Errors identify field, source row, and offending value. No football-specific score cap was introduced. |
| 4 | Ambiguous CSV headers/row widths and bad encoding were inconsistently handled at `data.py:25,38,53`. | Medium | Strict CSV parsing rejects duplicate headers and short/long rows before DataFrame construction. Expected file, UTF-8, and CSV syntax errors become contextual `DataValidationError`. Distinct additional columns remain permitted. |
| 5 | Parsed ticket positions were not used consistently at `ticket.py:36,42` and `service.py:20,31`; string sorting and conversion failures remained. | Medium | Ticket normalization converts accepted integers, integral decimal strings/numbers, and mixed supported representations to canonical integers. Validation, ordering, and prediction use those values. Invalid values remain available for structured diagnostics and cannot reach prediction. Source rows use ordinal positions independently of DataFrame index labels. |
| 6 | Generic position messages and globally skipped history checks at `ticket.py:50` and `service.py:19`. | Low | Reports duplicate positions with every affected source row, missing positions, out-of-range values, and malformed position values. Fixture checks continue independently, and service history checks continue for safely identifiable teams even when another position is invalid. Atomic behavior remains: failures return zero predictions. Resolves deferred Review 1 finding 6. |
| 7 | Missing source cells/non-finite odds escaped contextual validation at `scripts/build_real_spike_dataset.py:121,128,150,185`. | Medium | Required cells are checked before string operations; malformed source structure/encoding receives filename context. Odds must be finite decimal values greater than one; all field errors preserve filename/row/field. Goals reuse exact integer checks. The adapter remains fail-fast. |
| 8 | NaN rating values could become draws at `predictor.py:80,97`. | Low | Added finite guards for every rating component input, calculated ratings/difference, and direct difference classification. Structured errors propagate atomically through the service, including a late fixture failure. Formula expressions, classification branches, thresholds, and weights remain intact. |
| 9 | Colliding output destinations were accepted at `scripts/artifact_io.py:17`, generator `:110`, and adapter `:342`. | Low | Shared pre-write checks reject identical/resolved equivalent paths, symlink aliases, and existing hard-link aliases, including with `--force`. Checks precede directory creation and output writes. Existing distinct-path overwrite protection/force behavior remains. |

No broad `except Exception` handler was introduced. Expected conversion/file/parser failures are handled explicitly; existing standalone prediction eligibility checks and independent test expectations remain. The outcome-from-goals helper, normalization calculation, and configuration were not modified.

### Regression tests added

- New `tests/test_validation_regressions.py`: direct historical/ticket type and schema failures, duplicate DataFrame columns, invalid goals/dates/opponents/results, empty history, caller immutability and extra columns, empty/encoded/malformed CSVs, exact integer bounds and fractional precision, row/field overflow diagnostics, canonical mixed/decimal/string position ordering, index-independent errors, duplicate/missing/out-of-range position details, independent history checks after a position failure, and atomic late prediction failure.
- New `tests/test_source_validation.py`: malformed/missing/non-finite/too-small odds for all three bookmaker fields; every required blank source cell; truncated rows, duplicate headers, surplus fields and bad encoding; invalid/oversized source goals; FTR consistency and legitimate extra fields.
- `tests/test_predictor.py`: NaN and positive/negative infinite differences and rating components, plus invalid calculated results. Existing hand-calculated formula and inclusive-boundary tests remain unchanged.
- `tests/test_artifact_io.py`: both writers reject identical, resolved-equivalent, symlink, and hard-link destinations with and without force, without changing existing bytes or creating output directories. Existing overwrite/force and byte-reproduction cases remain unchanged.
- `tests/test_app.py`: empty, header-only, and invalid UTF-8 history renders startup errors without an unexpected exception or prediction table.

### Verification results

- Complete suite: `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m pytest -q -p no:cacheprovider` — **220 passed in 6.06s**, comprising 64 existing cases and 156 added cases.
- `git diff --check` passed. Final scope inspection confirms only the validation/guard changes, focused tests, and the two logs changed; earlier planning-log bytes are intact.
- Predictor file changes are limited to finite-value validation. AST comparison against pre-review HEAD confirms unchanged component arithmetic, all rating/difference assignments, and inclusive 1/X/2 classification branches. `history_issues` and `predict_fixture` remain structurally identical. `statistics.py`, `config.py`, and `outcomes.py` are byte-identical to HEAD.
- Original evaluation reproduced using the historical statistics implementation from the parent of `d98c15e`, loaded into memory without changing checkout: **152/380 = 40.000000%**, calls **154/77/149**.
- Current evaluation reproduced: **158/380 = 41.578947%**, calls **198/86/96**. Both evaluations use 932 fitting rows and 380 evaluation rows, with no held-out fitting rows.
- Baselines unchanged for both versions: always-1 **175/380 = 46.052632%**; closing-Bet365 favourite **227/380 = 59.736842%**. Complete regenerated reports also preserve the all-loaded measurements.
- Both offline scripts executed through direct file and `python -m` launch modes into temporary directories. Synthetic CSV/checksum and real CSV/measurement JSON are byte-identical to committed artifacts in both modes.
- Every tracked file under `data/` matches HEAD bytes, including raw source files, sample ticket, generated history, real matches, checksum, and measurements. Package import resolves to `src/`; existing Streamlit/launcher tests pass.

### Remaining concerns and handoff

All nine approved findings are addressed. No change to documented valid-input prediction behavior was required. Invalid inputs now fail explicitly; permitted integral position representations receive consistent numeric ordering. The supported numeric storage limit is representability, not an arbitrary score threshold. Configuration, normalization, datasets, and measured results remain unchanged. The user approved the dedicated Review 3 commit on 2026-10-17 with message `Review error handling and strengthen input validation`. Pre-commit checks again confirmed the exact 14-file scope, whitespace checks, all 220 tests passing (6.24s), unchanged datasets/measurements, and intact earlier planning-log entries. No push, merge, or branch change is authorized.
