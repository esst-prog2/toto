# Toto Estimator

### 1. The demo

I open the Toto estimator and enter the football matches included in the current week’s Toto. For each match, the program uses historical match data to estimate the outcome. It then displays the predicted outcome for each match as 1, X, or 2. I can see all of the week’s matches and predictions in one table and use them to fill in my Toto ticket.


### 2. The shape

in     the football matches included in the current week’s Toto

out    a predicted outcome (1, X, or 2) for each match

in between    compare the teams using historical match data and estimate whether the match will result in a home win, draw, or away win


### 3. The size

##### The first useful version will:
* contain historical football match results from selected leagues and competitions that commonly appear in Toto;
* use historical match results to predict a home win (1), draw (X), or away win (2) for each match;
* present the predictions for the selected Toto matches in a simple, readable table.

##### Not this term:
* use individual player data, injuries, suspensions, or team line-ups;
* predict exact scores;
* cover every football league and competition.


### 4. How we would know it works

Functional validation remains necessary: unknown teams and insufficient history must produce clear errors, while valid matches with enough history must produce a 1/X/2 prediction. Returning a valid label alone is not evidence that the prediction method works.

Prediction success will be evaluated chronologically on real football matches that were not used to fit the method. Accuracy on the same held-out matches will be compared explicitly with at least the trivial always-predict-1 baseline and the closing-Bet365 favourite.

The real-data spike loaded 1,312 matches; across the loaded dataset, the home-win rate was 44.664634% and the closing-Bet365 favourite won 52.515244%. Statistics were fitted only on 932 matches from the 2022/23 Premier League and Championship and evaluated on the same 380-match 2023/24 Premier League season:

| Method | Correct / evaluated | Accuracy |
| --- | ---: | ---: |
| Original Homework 4 predictor (independent venue scales) | 152/380 | 40.000000% |
| Current predictor (shared home/away scales, implemented 2026-10-08) | 158/380 | 41.578947% |
| Always predict `1` (unchanged baseline) | 175/380 | 46.052632% |
| Closing-Bet365 favourite (unchanged baseline) | 227/380 | 59.736842% |

The 2023/24 results motivated the normalization correction, so this evaluation dataset was also used during model development. Although its rows never enter statistics or normalization fitting, it is now a development benchmark rather than an independent test of the revised method. A later unseen season is needed for independent confirmation. The current predictor still does not beat either baseline; no claim of prediction success is made. See the [investigation and original/current comparison](docs/home-advantage-investigation.md) and [current measurement artifact](data/real_spike_measurements.json).

### 5. What could stop this

The main challenge could be finding enough historical match data in a consistent format, especially for older seasons and different competitions. Another challenge will be choosing and developing a prediction method that works well with the available data. The project will use publicly available football match data that can be shown in class; if some years or competitions are not available, the first version will use a smaller dataset.

## Synthetic-data MVP

The Streamlit application runs the complete historical data → prediction logic → 1/X/2 → interface workflow using the fixed synthetic dataset and fictional teams.

Completed offline work includes the Football-Data adapter, three committed real source files, the 1,312-match loader-compatible `data/real_matches.csv`, chronological evaluation against both baselines, and the shared home/away normalization correction. The adapter at `scripts/build_real_spike_dataset.py` reproduces the real dataset and current measurements from the committed source files. It is separate from the synthetic Streamlit workflow.

Future work includes integrating real teams and history into the interactive application, further prediction-method improvement, and independent evaluation on a later unseen season. The offline spike does not provide real-team selection in the current interface.

### Set up and run

Python 3.11 or newer is required. The MVP is developed and verified with Python 3.13.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install '.[dev]'
streamlit run app.py
```

Run the automated checks with:

```bash
pytest
```

### Reproduce the fixed history

The application treats `data/historical_matches.csv` as its canonical input. The offline generator owns the synthetic strengths and is never imported or executed by the runtime application or predictor.

To reproduce the dataset into temporary paths without overwriting the canonical files:

```bash
python scripts/generate_synthetic_history.py --output /tmp/historical_matches.csv --checksum /tmp/historical_matches.sha256
```

To verify the committed file from the repository root:

```bash
cd data
shasum -a 256 -c historical_matches.sha256
```

The generator uses `Generator(PCG64(20260927))`, base expected goals 1.35, home advantage 0.20, and documented additive expected-goal rates. The predictor normalizes overall PPM and GDPM independently, and uses a shared home/away min-max scale per venue metric. It uses 70% points and 30% goal difference, equal overall and relevant-venue weighting, a ±0.10 inclusive draw band, at least 10 total matches per team, and at least 5 matches at the relevant venue.

See [docs/manual-smoke-test.md](docs/manual-smoke-test.md) for the Streamlit verification checklist.
