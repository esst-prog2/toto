# Home advantage investigation — 2026-10-08

Question: Does the current min-max normalisation remove or distort home advantage?

Initial investigation scope: inspect the unchanged Homework 4 predictor; fit statistics on the existing 932 `fit` rows (2022/23 Premier League and Championship), evaluate the fixed predictor on the 380 `evaluation` rows (2023/24 Premier League). No algorithm changes, parameter tuning, counterfactual prediction experiment, or commit in that step. The later authorised implementation and evaluation are recorded below; the original evidence is retained for comparison.

## Original Homework 4 calculation

`src/toto_estimator/statistics.py` creates two team observations for each match, with points 3/1/0 for a win/draw/loss and goal difference equal to that team's goals scored minus goals conceded. For each team, overall PPM is total points divided by total matches; overall GDPM is total goal difference divided by total matches. Home and away PPM/GDPM use only observations at that venue and their corresponding match counts. Overall rates therefore weight home and away rates by match counts, rather than necessarily taking their simple average. No recency weighting, opponent adjustment, or division adjustment is applied.

For each of the six columns independently (overall/home/away × PPM/GDPM), the code takes the minimum and maximum across every team in the fitting data and computes `(value - minimum) / (maximum - minimum)`. These are six different scales, not one scale per metric. Constant non-null columns become 0.5; missing rates remain missing. Fitting contains 44 teams. Extrema are not computed from held-out matches or separately per fixture or division.

`src/toto_estimator/predictor.py` and `config.py` define:

```
C(team, scope) = 0.70 * PPM_norm(team, scope)
               + 0.30 * GDPM_norm(team, scope)
home_rating = 0.50 * C(home_team, overall) + 0.50 * C(home_team, home)
away_rating = 0.50 * C(away_team, overall) + 0.50 * C(away_team, away)
difference = home_rating - away_rating
```

Thus the four effective weights per rating are 0.35 overall PPM, 0.15 overall GDPM, 0.35 venue PPM, and 0.15 venue GDPM. Predict `1` if difference > 0.10; `2` if difference < -0.10; otherwise `X`, including both boundary values. These are rating rules, not outcome probabilities. Prediction requires known teams, at least 10 total historical matches and at least 5 matches at the relevant venue. There is no additional home-advantage term.

## Mechanism and conclusion

Independent venue normalisation makes relative standing among home performances comparable to relative standing among away performances, while discarding their common absolute reference. If all home rates equal the corresponding away rates plus a constant `c`, then home minimum and maximum also increase by `c`, and `(away_value + c - (away_min + c)) / ((away_max + c) - (away_min + c))` equals the away normalised value. A uniform home advantage is cancelled exactly. Unequal venue ranges additionally change the sensitivity to raw performance differences. Ordering within each individual column is preserved, but comparisons between home and away columns can reverse.

The concern is real on these fitting data: home PPM advantage is heavily compressed, and the mean home GDPM advantage reverses after normalisation. It is not accurate to say that all home advantage disappears: team-specific venue differences survive, and the held-out fixture set has a small positive average rating difference. The away-call excess alone does not prove this mechanism causes the entire accuracy deficit or that a repair will improve accuracy.

## Numerical evidence

All values below are from the existing CSV and production calculation. Means in the next table are unweighted across the 44 fitting teams; they differ from match-weighted means because Premier League teams played 38 matches and Championship teams played 46.

| Fitting statistic | Minimum | Maximum | Team mean | Normalised team mean |
| --- | ---: | ---: | ---: | ---: |
| Overall PPM | 0.657895 | 2.342105 | 1.374350 | 0.425395 |
| Overall GDPM | -0.973684 | 1.605263 | 0.000000 | 0.377551 |
| Home PPM | 0.578947 | 2.736842 | 1.584512 | 0.465993 |
| Away PPM | 0.421053 | 2.052632 | 1.164188 | 0.455470 |
| Home GDPM | -0.947368 | 2.263158 | 0.307572 | 0.390883 |
| Away GDPM | -1.736842 | 0.947368 | -0.307572 | 0.532473 |

Mean home-minus-away PPM changes from +0.420325 raw to +0.010524 normalised. Mean home-minus-away GDPM changes from +0.615145 raw to -0.141590 normalised. Among the 44 teams, 15 have better raw home PPM but worse normalised home PPM; 28 have better raw home GDPM but worse normalised home GDPM.

For example, Manchester City has home GDPM 2.263158 and away GDPM 0.947368, but both become 1.000000 because City is the maximum in each venue column. Burnley's home/away PPM are 2.347826/2.043478, yet normalise to 0.819724/0.994390; its home/away GDPM are 1.478261/0.782609, yet normalise to 0.755524/0.938619. Better raw home performance can therefore contribute a lower venue rating.

Match-weighted fitting means are home/away PPM 1.576180/1.170601 and GDPM +0.298283/-0.298283. Fitting outcomes are 411 home wins, 236 draws, and 285 away wins. The historical home advantage is present before normalisation.

For the 20 teams appearing in the held-out season, using their fitting statistics and the unchanged 44-team normalisation bounds, mean raw home-minus-away PPM is +0.590046 and GDPM is +0.871167. The corresponding normalised gaps are +0.073696 and -0.067681. Every held-out team appears 19 times at each venue, so the overall component cancels in the mean fixture difference. The remaining mean difference is `0.5 * (0.7 * 0.073696 + 0.3 * -0.067681) = +0.015641`, small relative to the 0.10 draw threshold. Across all 44 fitting teams, the analogous balanced venue contribution is -0.017555.

| Held-out result | `1` | `X` | `2` | Correct / accuracy |
| --- | ---: | ---: | ---: | --- |
| Actual outcomes | 175 | 82 | 123 | — |
| Unchanged predictor calls | 154 | 77 | 149 | 152/380 = 40.000000% |
| Always predict `1` | 380 | 0 | 0 | 175/380 = 46.052632% |

Actual rows versus predicted columns:

| Actual / predicted | `1` | `X` | `2` |
| --- | ---: | ---: | ---: |
| `1` | 80 | 33 | 62 |
| `X` | 33 | 17 | 32 |
| `2` | 41 | 27 | 55 |

Held-out home/away PPM are 1.597368/1.186842 and GDPM +0.321053/-0.321053. These held-out outcomes are evidence only; none were used to calculate statistics or bounds.

## Smallest principled next test (proposed during investigation)

For each metric, use one common min/max fitted to the pooled home and away team rates, and apply that same transformation to both venue columns. Keep overall normalisation, all weights, the draw threshold, data split, and all other rules unchanged. This directly restores a common reference for the venue comparison without adding or tuning a home bonus. The fitting-only pooled bounds would be PPM [0.421053, 2.736842] and GDPM [-1.736842, 2.263158]. With a shared scale, each venue difference is simply its raw difference divided by a positive common range, so its sign cannot reverse.

In that future test, reproduce prediction counts, the confusion matrix, and accuracy against the same always-1 baseline. Treat 2023/24 as a development benchmark now that its result motivated the change; reserve a later unseen season for independent confirmation. Shared scaling does not solve division comparability, promotion effects, sample uncertainty, or all weaknesses of the rating rule, and improvement remains unmeasured.

## Reproduction of the diagnostic measurements

The snippet uses the checked-out implementation: after the change below, it reproduces the new measurements rather than the original independent venue scales.

Run from the repository root with the installed pandas dependency:

```python
import pandas as pd
from toto_estimator.statistics import calculate_team_statistics, team_observations
from toto_estimator.predictor import predict_fixture

matches = pd.read_csv("data/real_matches.csv")
fit = matches.loc[matches.dataset_role == "fit"]
held_out = matches.loc[matches.dataset_role == "evaluation"]
stats = calculate_team_statistics(fit)
for prefix in ("overall", "home", "away"):
    for metric in ("ppm", "gdpm"):
        column = f"{prefix}_{metric}"
        print(column, stats[column].min(), stats[column].max(),
              stats[column].mean(), stats[column + "_norm"].mean())
for rows in (fit, held_out):
    print(team_observations(rows).groupby("venue")
          [["points", "goal_difference"]].mean())
predictions = [predict_fixture(stats, i, row.home_team, row.away_team)
               for i, row in enumerate(held_out.itertuples(), 1)]
actual = pd.Series(["1" if row.home_goals > row.away_goals else
                    "2" if row.home_goals < row.away_goals else "X"
                    for row in held_out.itertuples()], name="actual")
calls = pd.Series([p.prediction for p in predictions], name="predicted")
print(calls.value_counts(), (calls == actual).sum())
print(pd.crosstab(actual, calls))
print(pd.Series([p.rating_difference for p in predictions]).mean())
```

Use `PYTHONPATH=src` when running this snippet so it imports the repository's current implementation.

## Authorised implementation and measured result — 2026-10-08

Only the normalisation loop in `src/toto_estimator/statistics.py` changed. Overall PPM and overall GDPM still each call `normalize_series` independently. For each metric, home and away rates are concatenated with venue keys, passed together through the existing `normalize_series`, and assigned back to their respective normalised columns. This fits a single pooled range per venue metric from the supplied history. The evaluation supplies only the 932 fitting rows, as verified by the existing fitting-isolation test; the 380 held-out rows never enter statistics or range fitting. Tie handling (0.5), missing-value handling, raw statistics, weights, ratings, eligibility rules, and inclusive ±0.10 draw boundaries remain unchanged.

The fitting-only shared ranges are PPM [0.421053, 2.736842] and GDPM [-1.736842, 2.263158].

| Held-out comparison | Correct | Accuracy | `1` calls | `X` calls | `2` calls |
| --- | ---: | ---: | ---: | ---: | ---: |
| Original independent venue scales | 152/380 | 40.000000% | 154 | 77 | 149 |
| Shared venue scales | 158/380 | 41.578947% | 198 | 86 | 96 |
| Always predict `1` | 175/380 | 46.052632% | 380 | 0 | 0 |
| Closing-Bet365 favourite | 227/380 | 59.736842% | — | — | — |
| Actual outcomes | — | — | 175 | 82 | 123 |

Accuracy improved by six correct predictions, or 1.578947 percentage points. It remains 17 correct calls (4.473684 percentage points) below always-1 and 69 correct calls (18.157895 percentage points) below the closing-Bet365 favourite. No weights or thresholds were selected or changed in response to this measurement.

| Mean fitting-statistic home-minus-away gap | Original normalisation | Shared normalisation |
| --- | ---: | ---: |
| PPM, all 44 fitting teams | +0.010524 | +0.181504 |
| GDPM, all 44 fitting teams | -0.141590 | +0.153786 |
| PPM, 20 held-out teams using fitting history | +0.073696 | +0.254792 |
| GDPM, 20 held-out teams using fitting history | -0.067681 | +0.217792 |

These are unweighted team means. The held-out-team gaps still use only their previous-season fitting rates and the bounds fitted across all 44 teams. The mean held-out fixture rating difference rises from +0.015641 to +0.121846. The change preserves home advantage better: a positive raw venue gap now remains positive after scaling, and the mean GDPM advantage no longer reverses. This addresses the identified scaling defect; the accuracy increase on this development benchmark does not establish generalisation to a new season.

New confusion matrix (actual rows, predicted columns):

| Actual / predicted | `1` | `X` | `2` |
| --- | ---: | ---: | ---: |
| `1` | 99 | 39 | 37 |
| `X` | 42 | 20 | 20 |
| `2` | 57 | 27 | 39 |

Regression tests added in `tests/test_statistics.py` cover a uniform home uplift that separate scales would erase, explicit pooled scale values and equal cross-venue rates, unchanged overall scaling, missing venue history, and neutral output when pooled rates are tied. The exact real-data evaluation expectation now asserts 158 correct calls and 198/86/96 predictions. Existing tests retain fitting-only isolation, fixed rating weights, and ±0.10 boundary checks.

The existing adapter regenerated `data/real_spike_measurements.json` to describe the current predictor; its original result remains in this report and the append-only planning log. `data/real_matches.csv` and the source data are unchanged. Reproduce the artifact with `python3 scripts/build_real_spike_dataset.py --force`.

Validation: `.venv/bin/python -m pytest -q` completed with **46 passed in 3.48s**, no failures or skips. An initial attempt with system `python3` could not start pytest because that interpreter has no pytest installed; the project virtual environment successfully ran the full suite. No commit was made.
