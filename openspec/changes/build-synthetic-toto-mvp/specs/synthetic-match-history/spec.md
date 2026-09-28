## Purpose

Provide a fixed, reproducible match-history input and a source-independent validation boundary that can later accept real football results using the same public schema.

## ADDED Requirements

### Requirement: Fixed historical competition structure
The generated history SHALL contain Team A, Team B, Team C, Team D, Team E, and Team F across seasons 2020-21 through 2024-25. Each season SHALL contain ten chronologically ordered matchdays spaced three weeks apart, with three matches per matchday; matchdays 1-5 SHALL cover every unordered team pair once, and matchdays 6-10 SHALL repeat those fixtures with home and away reversed.

#### Scenario: Generated history has the required coverage
- **WHEN** the synthetic history is generated
- **THEN** it contains 150 matches, 30 per season, ten per unordered team pair, with each pair having five matches in each home/away orientation

#### Scenario: Match dates follow the deterministic schedule
- **WHEN** matches are inspected in generator order
- **THEN** dates are chronological across the five seasons, all three fixtures on a matchday share a date, and consecutive matchdays within a season are three weeks apart

### Requirement: Deterministic synthetic scores
The generator SHALL use `Generator(PCG64(20260927))`, a base expected-goals rate of 1.35, a home advantage of 0.20, and hidden strengths Team A 0.35, Team B 0.20, Team C 0.08, Team D -0.05, Team E -0.18, and Team F -0.32. For each fixture it SHALL calculate `home_rate = 1.35 + home_strength - away_strength + 0.20` and `away_rate = 1.35 + away_strength - home_strength`, then make independent Poisson draws for home goals first and away goals second.

#### Scenario: Repeating generation is reproducible
- **WHEN** the generator is run more than once with its documented configuration and deterministic fixture order
- **THEN** every run produces identical match records and CSV bytes

#### Scenario: Outcomes include random variation
- **WHEN** scores are generated
- **THEN** match outcomes are determined by the independent goal draws rather than directly assigned from hidden team strengths

### Requirement: Generator-only information boundary
Hidden strengths and other generator-only parameters SHALL NOT appear in the historical CSV and SHALL NOT be imported, executed, or accessed by the runtime application, statistics calculation, predictor, or application-facing end-to-end tests.

#### Scenario: Runtime predictions use public history only
- **WHEN** the application produces predictions
- **THEN** it infers team performance exclusively from historical CSV records and has no access to hidden strengths

### Requirement: Canonical historical CSV
The committed historical CSV SHALL be the canonical runtime input and SHALL contain the columns `season`, `date`, `home_team`, `away_team`, `home_goals`, and `away_goals`. A match's `1`, `X`, or `2` result SHALL be derived from its goal values rather than stored as hidden generator information.

#### Scenario: Historical data is loaded
- **WHEN** the canonical CSV is loaded successfully
- **THEN** its dates and goal values are parsed into usable types and each result can be derived from the home-team perspective

### Requirement: Dataset integrity verification
The canonical CSV SHALL have a recorded SHA-256 checksum, and the project SHALL provide an automated verification that reports a failure when the committed bytes do not match that checksum.

#### Scenario: Canonical data is unchanged
- **WHEN** checksum verification runs against the committed canonical CSV
- **THEN** the calculated SHA-256 value matches the recorded value

#### Scenario: Canonical data changes unexpectedly
- **WHEN** any byte of the canonical CSV changes without updating the recorded checksum
- **THEN** checksum verification fails with an integrity error

### Requirement: Source-independent historical-data validation
Historical-data validation SHALL operate only on the public CSV schema and SHALL reject missing columns, invalid dates, blank or identical opponents, and goal values that are not non-negative integers with clear error messages.

#### Scenario: Compatible history is accepted
- **WHEN** a dataset satisfies the public historical schema and value rules
- **THEN** it is accepted without relying on synthetic-generator configuration

#### Scenario: Invalid history is rejected
- **WHEN** one or more schema or value rules are violated
- **THEN** loading fails with messages that identify the invalid fields or records

