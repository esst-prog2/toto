# Phase 1: existing evaluation audit

Snapshot: 2026-11-26, commit `878d45e47f1ef861b1b774ecc89c94af7851cb34`, `feature/statistical-model`. No new model, parameter search or training experiment was run. Existing deterministic calculations were replayed in memory, with no data/report overwrites.

## Existing benchmark and selection procedure

`scripts/build_real_spike_dataset.py:253` (`held_out_evaluation`) computes statistics once on 932 `fit` rows: Premier League 2022/23 (380) and Championship 2022/23 (552), dated 2022-07-29–2023-05-28. It predicts all 380 Premier League 2023/24 matches (2023-08-11–2024-05-19) from these fixed prior-season statistics. It does not update ratings within the test season. The 44 fitting teams have 38 or 46 matches each and all 20 evaluation teams are known, including promoted teams via Championship history. No competition-strength correction is applied.

The declared weights 0.70/0.30, overall/venue weights 0.50/0.50, draw band ±0.10 and minimum histories 10/5 were manual MVP rules recorded in PLANNING_LOG.md, not selected by cross-validation or an optimizer. Empirical rates and scale extrema are fitted only on the supplied fitting rows. `tests/test_real_spike_dataset.py:test_held_out_rows_are_not_passed_to_statistics` captures the exact 932-row, single-season fit boundary.

The normalization correction followed investigation of this same 2023/24 benchmark (`docs/home-advantage-investigation.md`). Consequently, it is no longer an untouched independent test for the modified rule even though held-out rows do not enter rate or extrema calculation. No evidence of a later unseen-season evaluation was found in the scripts, tests, committed measurements or review documentation inspected. README explicitly labels these as previous development results.

## Reported and freshly reproduced results

| Method | Correct / 380 | Accuracy | Evidence |
|---|---:|---:|---|
| Original separate home/away normalization | 152 | 40.000000% | Historical report in home-advantage-investigation.md; old code not restored or rerun |
| Current pooled venue normalization | 158 | 41.578947% | Freshly reproduced; exact JSON/CSV bytes match committed artifacts |
| Always predict home win | 175 | 46.052632% | Freshly reproduced on the same evaluation rows |
| Closing Bet365 favourite | 227 | 59.736842% | Freshly reproduced on the same evaluation rows |

Current calls: 198 home, 86 draw, 96 away. Actual outcomes: 175 home, 82 draw, 123 away. Confusion matrix (actual rows, predicted columns):

| Actual / predicted | 1 | X | 2 |
|---|---:|---:|---:|
| 1 | 99 | 39 | 37 |
| X | 42 | 20 | 20 |
| 2 | 57 | 27 | 39 |

Accuracy is `sum(prediction == goal-derived outcome)/n`. The change improved six correct calls (1.578947 percentage points) on this development sample; the current rule trails always-home by 17 and bookmaker favourite by 69. No confidence intervals, paired comparison, robustness across seasons, log loss, Brier score, ranked probability score, calibration plots, return-on-stake or betting decision evaluation exists in the inspected evaluator. Probability metrics are unavailable because the predictor emits no probabilities. Functional correctness tests do not demonstrate statistical adequacy.

`measurement_report` also describes **all 1,312 loaded rows**, not a separate out-of-sample test: 586 home wins (44.664634%) and 689 successful bookmaker favourites (52.515244%). It must not be compared directly with held-out model accuracy because the denominators differ.

Bookmaker favourite is the outcome with minimum B365 closing decimal odds (B365CH/CD/CA). All equal minima are joint favourites; a row is counted correct if its actual result is in that set (`_favourites`, Decimal comparison). There are 11 joint-favourite rows overall and two in the evaluation partition. This set-valued tie convention is more permissive than one deterministic label, so it is not exactly the same action space as the model. Closing odds are a strong retrospective baseline, but no price timestamp demonstrates that those odds were available at an earlier ticket submission time. No overround adjustment or implied-probability evaluation is performed.

## Leakage and historical meaning

The spike's calendar split is strictly separated and rates/ranges use fitting rows only. This protects against direct held-out outcome leakage in the current calculation. It does not undo adaptive method selection on the test season, cross-division comparability problems, historical record revisions or source availability uncertainty. No nested validation, frozen future holdout registry or tuning audit exists.

The app's `service.run_workflow` accepts a history frame without a target date. It does not enforce chronological safety and computes no historical accuracy. README's most-recent-previous-meeting backtest remains an unchecked OpenSpec task. A last-meeting comparison would require reconstructing features, scale bounds and all estimation using only information before that meeting; using today's team rates would leak later results. One selected previous meeting is also a sparse, selective illustration rather than a representative performance test.

Respect the current retrospective policy in `docs/accelerated-five-phase-workflow.md`: use accepted final historical results at original football dates without filtering by later administrative-publication date. This can be a coherent internal final-history diagnostic. A later award or resumed result entered at an earlier original date may contain information unavailable then, so this policy cannot establish realistic pre-match forecasting performance. Earlier league reports use differing availability/completion semantics; absent sidecars prevent reconciling their current versions. No dates, scores, exclusions or existing policies were altered here.

For a future real-time reconstruction, separate original kickoff, completion, decision/publication and data-availability times, declare the forecast cutoff and censor all transformations accordingly. Date-only history cannot reliably sequence same-day matches. Final administrative labels can themselves differ from regulation-time football outcomes; the desired target must be approved before interpreting model quality. This audit does not substitute a new eligibility rule.

## Reproduction: read-only benchmark

Run from the repository root. This invokes only the existing statistics/evaluation functions, not artifact-writing main or `--force`:

```sh
PYTHONPATH=src python3 -B - <<'PY'
from pathlib import Path
import pandas as pd
from scripts.build_real_spike_dataset import (
    build_records, measurement_report, serialize_records, serialize_report,
)
from toto_estimator.statistics import calculate_team_statistics
from toto_estimator.predictor import predict_fixture
from toto_estimator.outcomes import outcome_from_goals
records, evidence = build_records(Path('data/football_data_raw'))
report = measurement_report(records, evidence)
assert serialize_records(records) == Path('data/real_matches.csv').read_bytes()
assert serialize_report(report) == Path('data/real_spike_measurements.json').read_bytes()
print(report['held_out_evaluation'])
fit = pd.DataFrame([r for r in records if r['dataset_role'] == 'fit'])
test = [r for r in records if r['dataset_role'] == 'evaluation']
stats = calculate_team_statistics(fit)
actual = pd.Series([outcome_from_goals(r['home_goals'], r['away_goals'])
                    for r in test], name='actual')
calls = pd.Series([predict_fixture(stats, i, r['home_team'], r['away_team']).prediction
                   for i, r in enumerate(test, 1)], name='predicted')
print(pd.crosstab(actual, calls).reindex(index=['1','X','2'], columns=['1','X','2']))
PY
```

Observed with CPython 3.13.12, pandas 3.0.2, NumPy 2.4.4. Both byte assertions passed; report metrics and confusion matrix above matched. SHA-256 versions are in [data-readiness-audit.md](data-readiness-audit.md).

## Regression evidence and limits

Fresh complete repository run, exit 0:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /private/tmp/belgium-phase4-env-xgpvyf0n/venv/bin/python -B -m pytest -q -p no:cacheprovider
```

**2,678 passed, 27 subtests passed in 20.01 seconds**, no failures/errors/skips. This used an existing external environment, unchanged: CPython 3.13.12, NumPy 2.5.3, pandas 3.0.6, pytest 9.1.1, Streamlit 1.64.0 and Jinja2 3.1.6; no dependencies were installed. This differs from the system interpreter used for the independent read-only replay above. The first attempt using `/private/tmp/toto-serie-a-test/bin/python` exited 1 because pytest was absent; the available second interpreter completed the full run. System Python also lacks pytest and Streamlit. Temporary environment paths are machine-specific, not portable reproducibility guarantees; use an existing compatible environment elsewhere without assuming these paths persist.

Relevant existing tests: `test_statistics.py` (rate computation/pooled scales/missing venue), `test_predictor.py` and `test_config.py` (fixed rules/boundaries/history), `test_real_spike_dataset.py` (fitting isolation/exact results/artifact reproduction), `test_end_to_end.py`, `test_service.py`, `test_app.py` and `test_launcher.py` (workflow/UI), plus collection/importer structural and adverse-case suites. Most historical collection tests use synthetic fixtures; their success cannot validate absent private datasets. `docs/manual-smoke-test.md` records an earlier UI check, not a fresh manual browser test in this audit.
