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

The main challenge could be finding enough historical match data in a consistent format, especially for older seasons and different competitions. Another challenge will be choosing and developing a prediction method that works well with the available data.




