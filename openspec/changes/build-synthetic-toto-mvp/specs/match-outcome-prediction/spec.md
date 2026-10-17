## Purpose

Turn public historical match results into understandable team ratings and deterministic 1/X/2 predictions using explicit, replaceable MVP rules.

## ADDED Requirements

### Requirement: Historical performance statistics
The system SHALL derive points per match and goal difference per match for every team, both overall and for the relevant venue split. A win SHALL award three points, a draw one point, and a loss zero points from the team's perspective.

#### Scenario: Overall and venue statistics are calculated
- **WHEN** valid historical matches are supplied
- **THEN** each team has total-match, home-match, and away-match counts plus corresponding points-per-match and goal-difference-per-match values derived only from those matches

### Requirement: Comparable normalized metrics
Historical rule: the original September 2026 design normalized all six overall/home/away metric columns independently, with 0.5 for constant columns. The user-authorized rule of 2026-10-08 superseded independent venue scaling. The following requirements describe the current implementation; the original design and decision history remain in `design.md` and `PLANNING_LOG.md`.

The system SHALL normalize overall points per match (PPM) and overall goal difference per match (GDPM) independently across teams in the supplied history. For each venue metric, it SHALL pool home and away team rates, calculate one minimum and maximum over the non-missing pooled values, and apply that shared min-max scale to both venue columns. In chronological evaluation, statistics and normalization bounds SHALL use only fitting history.

#### Scenario: Values vary within a normalization pool
- **WHEN** an overall metric series or a pooled home/away metric has different minimum and maximum non-missing values
- **THEN** the minimum maps to 0, the maximum maps to 1, and intermediate values use `(value - minimum) / (maximum - minimum)`
- **AND** equal home and away rates map to the same normalized value

#### Scenario: Values are tied within a normalization pool
- **WHEN** all non-missing values in an overall metric series or pooled home/away metric are equal
- **THEN** those values receive 0.5

#### Scenario: Home and away columns are individually constant but differ
- **WHEN** all home rates for a metric equal one value and all away rates equal a different value
- **THEN** the two columns use the shared pooled range rather than each receiving 0.5

#### Scenario: Venue history is missing
- **WHEN** a team has no observations at a venue
- **THEN** its missing venue rates remain missing and are excluded from normalization bounds
- **AND** the minimum-history requirement still prevents predicting a fixture at that venue

### Requirement: Transparent team rating
For a fixture, the system SHALL calculate the home team's rating from its overall and home metrics and the away team's rating from its overall and away metrics. Within both the overall and venue components, normalized points performance SHALL have weight 0.70 and normalized goal-difference performance weight 0.30; the overall and venue components SHALL have equal weight.

#### Scenario: Fixture ratings are calculated
- **WHEN** both teams have sufficient history
- **THEN** the system returns home and away ratings between 0 and 1 using the documented fixed weights

### Requirement: Fixed 1/X/2 decision rule
The system SHALL subtract the away rating from the home rating and predict `1` when the difference is greater than 0.10, `2` when it is less than -0.10, and `X` when it lies inclusively between -0.10 and 0.10.

#### Scenario: Home rating advantage exceeds the draw band
- **WHEN** the rating difference is greater than 0.10
- **THEN** the prediction is `1`

#### Scenario: Ratings fall within the draw band
- **WHEN** the rating difference is between -0.10 and 0.10 inclusive
- **THEN** the prediction is `X`

#### Scenario: Away rating advantage exceeds the draw band
- **WHEN** the rating difference is less than -0.10
- **THEN** the prediction is `2`

### Requirement: Minimum historical coverage
The system SHALL require each team in a fixture to have at least ten total historical matches, the home team to have at least five historical home matches, and the away team to have at least five historical away matches. These limits SHALL be defined as named configuration constants.

#### Scenario: Both teams have sufficient history
- **WHEN** both teams meet the total and relevant-venue limits
- **THEN** the system can calculate ratings and a prediction for the fixture

#### Scenario: A team has insufficient history
- **WHEN** either team fails a total or relevant-venue limit
- **THEN** the system reports which fixture, team, and history requirement is unsatisfied and does not produce a prediction for that fixture

### Requirement: Predictor transparency
Prediction results SHALL make the home rating, away rating, and signed rating difference available to callers without exposing generator-only information.

#### Scenario: Caller requests prediction details
- **WHEN** a valid fixture is predicted
- **THEN** the result includes its `1`, `X`, or `2` value and the three rating values used by the decision rule

