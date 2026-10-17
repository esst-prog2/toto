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
