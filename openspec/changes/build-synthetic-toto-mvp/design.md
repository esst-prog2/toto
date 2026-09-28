## Context

The repository currently contains project documentation and an initialized OpenSpec workspace, but no application code or tests. The MVP spans deterministic data generation, reusable data validation and prediction logic, a UI-independent orchestration layer, and a local Streamlit interface. See `proposal.md` for motivation and the four delta specs for behavioral contracts.

The implementation must preserve a hard information boundary: hidden synthetic strengths belong to an offline generator only, while runtime components consume the public historical CSV. Python 3.11 is the compatibility floor, and development verification uses the installed Python 3.13 environment.

## Goals / Non-Goals

**Goals:**

- Keep domain and workflow logic importable and testable without Streamlit.
- Make the generated dataset byte-reproducible and detect accidental changes.
- Keep public data validation independent of the synthetic source.
- Keep predictor rules centralized, explicit, and replaceable.
- Organize the project so a later real-data adapter can provide the same historical schema.

**Non-Goals:**

- Stabilize a general public Python API or deploy a hosted service.
- Optimize predictor parameters or claim statistical calibration.
- Add real-data downloading, database storage, authentication, or multi-user persistence.
- Automate detailed browser-level Streamlit behavior beyond a documented smoke test.

## Decisions

### 1. Use a src-layout package with a thin Streamlit entry point

Use `pyproject.toml` with `requires-python = ">=3.11"`, runtime dependencies `streamlit`, `pandas`, and `numpy`, a pytest development extra, and pytest configuration. Put reusable modules under `src/toto_estimator/`:

- `config.py`: predictor thresholds, weights, history limits, and default data paths.
- `data.py`: public historical CSV and sample-ticket loading and validation.
- `statistics.py`: team-level overall/home/away aggregates and normalization.
- `predictor.py`: rating composition and fixture predictions.
- `ticket.py`: ticket-specific validation and error representation.
- `service.py`: atomic end-to-end orchestration and result objects.

Use a small root `app.py` only for Streamlit widgets, session state, rendering, and calls into `service.py`. This keeps the UI replaceable and allows end-to-end tests to exercise observable behavior without a browser.

Alternative considered: place workflow logic directly in the Streamlit script. Rejected because it couples validation and prediction to widget state and makes the required service-level testing difficult.

### 2. Keep the generator outside the runtime package

Place the generator at `scripts/generate_synthetic_history.py`. It may own hidden strengths and generator parameters but runtime modules SHALL neither import it nor read a generator configuration artifact. Store public assets under `data/`:

- `historical_matches.csv`
- `historical_matches.sha256`
- `sample_ticket.csv`

The application reads only the two CSV inputs. Checksum verification belongs to generator/integrity tooling and automated tests, so runtime prediction remains source-independent.

Alternative considered: keep generator helpers inside `toto_estimator`. Rejected because importable runtime proximity weakens the hidden-information boundary.

### 3. Define a deterministic schedule and byte serialization

Generate first-half round-robin fixtures with the circle method using the fixed initial ordering Team A through Team F. Preserve the resulting round and within-round order, then append rounds 6-10 in the same order with home and away reversed. Reuse that fixture order for all five seasons.

Start each season on the first Saturday on or after August 10 of its starting year, producing start dates 2020-08-15, 2021-08-14, 2022-08-13, 2023-08-12, and 2024-08-10. Add 21 days per matchday and process seasons, matchdays, and fixtures in their stored order.

Create one `numpy.random.Generator(numpy.random.PCG64(20260927))` for the full dataset. For each fixture, calculate the specified additive rates, draw home goals, then draw away goals. Serialize once as UTF-8 CSV with an LF newline, the specified header order, ISO `YYYY-MM-DD` dates, generation-order rows, and no dataframe index. Calculate SHA-256 over those exact bytes and store the lowercase digest in standard checksum-file form. Generation writes to caller-selected or explicit project paths and avoids silently overwriting unrelated files.

Alternative considered: rely on `default_rng` and dataframe defaults. Rejected because implicit RNG and serialization choices make byte-level reproduction less explicit.

### 4. Separate source-independent validation from generator invariants

`data.py` validates only the public contract: required columns, parseable dates, nonblank distinct opponents, and non-negative integer goals. It returns normalized, chronologically sorted data or structured validation errors. It does not require the six fictional team names, five seasons, exact row count, or synthetic pairing balance.

Generator tests separately enforce all synthetic invariants, exact regeneration, and checksum agreement. This division lets future real data use the runtime path without pretending to be synthetic.

Alternative considered: one validator for both concerns. Rejected because synthetic assumptions would prevent replacing the CSV with compatible real match history.

### 5. Normalize each metric across the loaded competition

First expand match rows into team-perspective observations containing venue, points, goals for, goals against, and goal difference. Aggregate overall, home-only, and away-only match counts, points per match, and goal difference per match.

Apply min-max normalization independently to these six metric series: overall PPM, overall GDPM, home PPM, home GDPM, away PPM, and away GDPM. Use `(value - minimum) / (maximum - minimum)`; when a series has no range, assign 0.5 to every team.

For a fixture:

```text
overall_score(team) = 0.70 * overall_ppm_norm + 0.30 * overall_gdpm_norm
home_score(team)    = 0.70 * home_ppm_norm    + 0.30 * home_gdpm_norm
away_score(team)    = 0.70 * away_ppm_norm    + 0.30 * away_gdpm_norm

home_rating = 0.50 * overall_score(home_team) + 0.50 * home_score(home_team)
away_rating = 0.50 * overall_score(away_team) + 0.50 * away_score(away_team)
difference  = home_rating - away_rating
```

Apply the inclusive draw band defined by the specs. Keep all weights, the draw threshold, and minimum-history values as named constants rather than scattering literals.

Alternative considered: z-scores or learned weights. Rejected because they reduce transparency or introduce tuning outside this framework-focused MVP.

### 6. Return structured validation and workflow results

Represent validation problems with at least a code, human-readable message, and affected ticket position or source row where applicable. Ticket validation performs independent checks and accumulates all detectable errors rather than stopping at the first one. Duplicate-pair errors mark every position participating in the duplicate.

`service.py` accepts validated/loadable history and a ticket, calculates statistics once, checks all fixture history requirements, and returns either:

- a failure result containing all errors and an empty prediction collection; or
- a success result containing fourteen ordered prediction records, including home rating, away rating, and difference.

The Streamlit layer copies startup ticket data into `st.session_state`, renders widgets from that copy, and never writes user selections to disk. Prediction output is cleared or withheld after an invalid submission so stale results cannot appear valid.

Alternative considered: exceptions for all user-correctable ticket errors. Rejected because an explicit aggregate result better supports atomic validation feedback.

### 7. Test logic by layer and keep UI verification small

Use pytest tests for generator invariants and reproducibility, checksum verification, valid and invalid public data, statistic calculations including normalization ties, rating boundaries, history limits, ticket rules and multi-error reporting, service atomicity, and a successful canonical end-to-end run. The end-to-end test imports only runtime modules and reads the committed CSV and sample ticket; it cannot import generator strengths.

Document a manual Streamlit smoke test covering startup defaults, a valid submission, transparency expansion, invalid edits, preserved selections, and restart restoration. Automated widget/browser testing remains out of scope.

## Risks / Trade-offs

- [The fixed sample can make the predictor look more credible than it is] -> Label the rules and synthetic parameters as MVP defaults and avoid accuracy claims.
- [Min-max ratings depend on the set of teams in the loaded dataset] -> Treat normalization as an explicit replaceable rule and cover it with deterministic unit tests.
- [NumPy distribution behavior or CSV serialization could drift across environments] -> Commit the canonical CSV and checksum, make serialization explicit, and fail integrity tests rather than silently replacing the data.
- [A corrupted committed sample ticket can prevent startup] -> Validate it immediately and display a clear startup data error rather than rendering misleading defaults.
- [Streamlit reruns can accidentally reset or overwrite edits] -> Initialize session state only when absent and keep filesystem assets read-only at runtime.

## Migration Plan

This is a greenfield addition, so no data migration is required. Implement the package and tests first, generate and commit the canonical assets once, then run the full automated suite and manual Streamlit smoke test. If the change must be rolled back, remove the newly introduced application, data, generator, and test files; the existing README and broader project intent remain intact.
