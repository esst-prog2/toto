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

* Given a team that is not found in the dataset, the program shows an error.
* Given a match without enough historical data, the program reports that it cannot make a prediction.
* Given valid matches with enough historical data, the program returns a prediction (1, X, or 2) for each match.

### 5. What could stop this

The main challenge could be finding enough historical match data in a consistent format, especially for older seasons and different competitions. Another challenge will be choosing and developing a prediction method that works well with the available data. The project will use publicly available football match data that can be shown in class; if some years or competitions are not available, the first version will use a smaller dataset.

## Synthetic-data MVP

The current implementation is the first framework-building step toward the broader project above. It runs the complete historical data → prediction logic → 1/X/2 → interface workflow using a fixed synthetic dataset. Real historical football data and statistical model refinement remain planned later stages.

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

The generator uses `Generator(PCG64(20260927))`, base expected goals 1.35, home advantage 0.20, and documented additive expected-goal rates. The predictor uses 70% points and 30% goal difference, equal overall and relevant-venue weighting, a ±0.10 inclusive draw band, at least 10 total matches per team, and at least 5 matches at the relevant venue.

See [docs/manual-smoke-test.md](docs/manual-smoke-test.md) for the Streamlit verification checklist.


