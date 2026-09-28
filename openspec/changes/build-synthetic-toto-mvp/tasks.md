## 1. Project Foundation

- [x] 1.1 Create `pyproject.toml` for Python 3.11+, the `src/toto_estimator` package, Streamlit/pandas/NumPy runtime dependencies, pytest development dependency, and pytest configuration; verify installation succeeds in the Python 3.13 development environment and the package imports.
- [x] 1.2 Add `config.py` with named predictor weights, draw threshold, minimum-history limits, and default public data paths; verify unit tests assert the documented constant values.

## 2. Synthetic Dataset and Fixed Assets

- [x] 2.1 Implement the separate deterministic generator in `scripts/generate_synthetic_history.py`, including the circle-method schedule, season dates, explicit PCG64 generator, additive Poisson rates, and home-then-away draws; verify focused generator tests reproduce identical records across repeated runs.
- [x] 2.2 Add generator-invariant tests for team names, five seasons, dates, matchday structure, 150-match count, pair coverage, and balanced pair orientations; verify `pytest` passes all invariant cases.
- [x] 2.3 Generate `data/historical_matches.csv` with the specified deterministic serialization and record `data/historical_matches.sha256`; verify regeneration produces byte-identical CSV output and checksum verification passes.
- [x] 2.4 Create the exact fixed `data/sample_ticket.csv` with its fourteen positions and omitted Team E-Team F pairing; verify a fixture-level test compares every committed row with the specified sample ticket.

## 3. Public Data Loading and Validation

- [x] 3.1 Implement structured validation errors and historical CSV loading for the public schema, type conversion, chronological ordering, and derived home-perspective results; verify tests cover a valid compatible dataset and each required schema/value failure.
- [x] 3.2 Implement sample-ticket CSV loading with required-column and position parsing checks; verify valid loading and malformed-file tests pass without involving Streamlit.
- [x] 3.3 Add an integrity test that reads the committed checksum and verifies the canonical historical CSV bytes, including a negative test for changed bytes.

## 4. Statistics and Prediction

- [x] 4.1 Implement team-perspective observations and overall/home/away match counts, points per match, and goal-difference per match; verify hand-calculated fixture tests cover wins, draws, losses, and venue splits.
- [x] 4.2 Implement independent min-max normalization for all six metric series with the neutral 0.5 tied-series rule; verify minimum, maximum, intermediate, and constant-series test cases.
- [x] 4.3 Implement home and away rating composition using the fixed 70/30 metric weights and equal overall/venue weights; verify tests compare ratings with hand-calculated expected values and keep them within zero to one.
- [x] 4.4 Implement the inclusive ±0.10 draw band and prediction detail results; verify boundary tests produce `1`, `X`, and `2` exactly as specified and include both ratings plus their signed difference.
- [x] 4.5 Enforce named minimum-history requirements for total and relevant-venue matches; verify tests identify the fixture, team, and failed limit without accessing generator-only information.

## 5. Ticket Validation and Service Workflow

- [x] 5.1 Implement complete ticket validation for row count, unique positions 1-14, known and distinct opponents, and unique unordered pairings while permitting repeated teams; verify tests cover a valid ticket and aggregated multi-position errors, including marking both sides of duplicated pairs.
- [x] 5.2 Implement `service.py` orchestration that loads/accepts public inputs, calculates statistics once, aggregates ticket and history errors, and returns either zero predictions or all fourteen ordered prediction records; verify atomic failure and successful service tests.
- [x] 5.3 Add the observable end-to-end test using only the committed historical CSV, sample ticket, and runtime modules; verify it returns fourteen ordered `1`/`X`/`2` predictions and does not import or inspect the generator or hidden strengths.

## 6. Streamlit MVP

- [x] 6.1 Implement `app.py` with validated startup loading, a session-only editable copy of all fourteen fixtures, and home/away dropdowns; verify code-level tests where practical and the smoke-test procedure confirms startup defaults and unchanged CSV files after edits.
- [x] 6.2 Add atomic submission behavior that preserves selections, lists every affected position, withholds stale or partial predictions on failure, and shows all fourteen ordered predictions on success with position 14 marked `+1`; verify each behavior through the documented manual smoke test.
- [x] 6.3 Add an optional transparency section for home rating, away rating, and rating difference while excluding generator-only values; verify the manual smoke test inspects all displayed fields.

## 7. Documentation and Final Verification

- [x] 7.1 Document environment setup, generator and checksum commands, Streamlit launch, MVP rule parameters, the runtime/generator information boundary, and the manual smoke-test steps while preserving the README's broader real-data project scope; verify all documented commands are valid.
- [x] 7.2 Run the complete pytest suite under the installed Python 3.13 environment and execute the manual Streamlit smoke test; verify all automated tests pass and record successful completion of every smoke-test step.
- [x] 7.3 Inspect runtime imports and the end-to-end test to confirm they do not reference `scripts/generate_synthetic_history.py` or hidden strengths, and verify the application operates using only the two committed CSV inputs.
- [x] 7.4 Make the repository-root Streamlit launcher resolve the `src` package independently of editable-install `.pth` processing; verify the documented activated-environment command starts successfully and add a regression test for an absent editable import path.
