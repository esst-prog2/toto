# Toto Estimator

## 1. The demo

I open the Toto Estimator in the browser using the Streamlit application (`app.py`) and manually enter 14 football matches, selecting the competition, home team, and away team for each match. I click **Predict**, and the application displays the recommended 1/X/2 outcome and the estimated probabilities of all three outcomes for each match. It also shows the result of a historical backtest against the teams' most recent previous meeting, including whether the prediction was correct. If a match cannot be evaluated because of missing or insufficient data, the application displays a clear message for that match without affecting the others. All 14 matches, predictions, probabilities, and available backtesting results appear in one table, helping me fill out my Toto ticket.

## 2. The shape

**in** – 14 manually entered football matches, each specifying the competition, home team, and away team.

**out** – A recommended 1/X/2 outcome, the estimated probabilities of all three outcomes, and a historical backtesting result where available. Unsupported matches are clearly marked.

**on screen** – The user selects competitions and teams, clicks Predict, and reviews the results in one table. The table shows predictions, probabilities, and whether the method would have correctly predicted the teams' most recent previous meeting.

## 3. The size

### The first useful version will:

- Allow manual entry of 14 football matches, including competition and team selection.
- Use historical results from supported competitions to generate predictions.
- Display a recommended 1/X/2 outcome and the probabilities of all three possible results.
- Show whether the prediction method would have correctly predicted the teams' most recent previous meeting, when sufficient historical data are available.
- Display clear, match-specific messages when predictions or backtests are unavailable, without preventing other matches from being evaluated.
- Present all results in one readable table.

### Not this term:

- Use individual player statistics, injuries, suspensions, or team line-ups.
- Predict exact match scores.
- Automatically download the current weekly Toto ticket.
- Guarantee coverage of every football league and competition.
- Allow users to choose between multiple statistical models.

## 4. How we would know it works

Three testable behaviours define functional success:

1. **Valid matches:** Given 14 supported matches with sufficient historical data, the application produces 14 recommended 1/X/2 predictions and three estimated probabilities for each match, adding up to 100%, allowing for rounding.
2. **Invalid or insufficient data:** Given an unsupported team or competition, or insufficient historical data, the application displays a clear message for that match while continuing to evaluate the other valid matches.
3. **Historical backtesting:** Given sufficient historical information, the application identifies the teams' most recent previous meeting, displays the actual result and the historical prediction, and correctly reports whether the prediction succeeded, without using information from after that match. If a reliable backtest is impossible, it reports that the comparison is unavailable.

The statistical prediction method is also evaluated chronologically on previously unseen matches, using prediction accuracy, probability quality, and comparison with simple baselines. Historical performance information helps users interpret the recommendations; improved accuracy is not guaranteed.

The previous algorithm achieved 40.00% accuracy, increasing to 41.58% after a normalization adjustment, compared with 46.05% for always predicting a home win and 59.74% for the Bet365 favourite. These are development results, not an independent evaluation of the new method.

See [Home Advantage Investigation](docs/home-advantage-investigation.md).

## 5. What could stop this

The main risks are obtaining sufficient historical match data, resolving licensing restrictions, and developing a prediction method that provides meaningful estimates. Differences in historical team names, competition structures, and available match histories may also complicate the work.

Historical results come from publicly accessible football databases and repositories. Some sources have unresolved redistribution rights, so the collected datasets are stored locally rather than published on GitHub.

If suitable freely redistributable sources cannot be obtained, the public GitHub application may use a smaller demonstration dataset. For the December presentation, screenshots and predictions generated using locally stored historical data may be shown where the applicable data-use conditions permit. Otherwise, the demonstration can use synthetic data.

The demonstration dataset may produce different predictions and predictive performance from the full historical dataset. If predictive performance is weak, the application documents this limitation rather than claiming unverified accuracy.
