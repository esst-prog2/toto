## Purpose

Define the planned Homework 8 demo contract for competition-aware football outcome probabilities and trustworthy historical comparisons, without claiming these capabilities already exist.

## ADDED Requirements

### Requirement: Fourteen competition-scoped manual fixtures
The application SHALL accept 14 manually entered fixtures, each with competition, home team and away team selection, and SHALL evaluate them when the user clicks Predict.

#### Scenario: Supported ticket submission
- **WHEN** the user enters 14 supported fixtures and clicks Predict
- **THEN** the results table contains all 14 fixtures in ticket order with their competitions and teams

### Requirement: Probabilistic predictions
For each supported fixture with sufficient history, the application SHALL display a recommended 1/X/2 outcome and estimated probabilities for all three outcomes. Probabilities SHALL be finite, nonnegative, at most 100%, and sum to 100% allowing for displayed rounding.

#### Scenario: All fixtures are supported
- **WHEN** 14 supported fixtures have sufficient historical data
- **THEN** all 14 rows contain a recommended 1/X/2 result and three valid estimated probabilities

### Requirement: Match-specific failure isolation
The application SHALL clearly identify unsupported competitions or teams and insufficient data for each affected fixture while continuing to evaluate other valid fixtures.

#### Scenario: Mixed valid and unsupported fixtures
- **WHEN** a ticket contains both predictable and unsupported fixtures
- **THEN** unsupported rows show actionable messages and the other valid rows retain their predictions and probabilities

### Requirement: Leakage-free previous-meeting backtest
When reliable history is available, the application SHALL identify the teams' most recent meeting strictly before the submitted fixture's prediction cutoff, display its actual outcome and reconstructed historical prediction, and report correctness. Reconstruction SHALL use only information available strictly before that historical match, including fitting, normalization and parameter selection. A historical result SHALL be interpreted relative to the home and away teams in that historical meeting.

#### Scenario: Reliable historical comparison
- **WHEN** a previous meeting and sufficient earlier eligible history are available
- **THEN** the table shows that meeting, its actual 1/X/2 outcome, the historical prediction and whether they agree, without later information

#### Scenario: Reliable comparison unavailable
- **WHEN** the previous meeting, its ordering, or sufficient pre-match history cannot be established reliably
- **THEN** the row explicitly reports the backtest unavailable without suppressing an otherwise available current prediction

### Requirement: Honest evaluation and permitted demonstration
The method SHALL be evaluated chronologically on previously unseen matches using accuracy, probability quality and simple baselines. Earlier 40.00% and 41.58% results SHALL remain labeled development results, not evidence for the new method. Downloaded private historical datasets SHALL remain excluded from public Git; demonstration use SHALL comply with applicable source conditions.

#### Scenario: Full data cannot be redistributed
- **WHEN** source rights do not permit publication of the full historical data
- **THEN** the public demo uses a permitted smaller demonstration dataset or synthetic data, discloses possible performance differences and makes no unsupported accuracy claim

#### Scenario: Local presentation requires permission
- **WHEN** screenshots or predictions from locally stored data are proposed for the December presentation
- **THEN** they are used only where applicable data-use conditions permit; otherwise synthetic data are used
