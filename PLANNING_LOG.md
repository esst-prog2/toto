2026-09-27 — Use OpenSpec version 1.13.0 and initialize it in this repository. — Decided by the user.
2026-09-27 — Configure OpenSpec for Codex using its default core workflow profile. — Decided by the assistant.
2026-09-27 — Use Python as the implementation language. — Decided by the user.
2026-09-27 — Use a small local Streamlit app as the MVP interface; defer a proper web application as a possible later development step. — Decided by the user.
2026-09-27 — Use a small reproducible synthetic historical dataset with fictional teams for the MVP. — Decided by the user.
2026-09-27 — The MVP will demonstrate the complete historical data → prediction logic → 1/X/2 predictions → Streamlit workflow. — Decided by the user.
2026-09-27 — Defer real historical football data integration and refinement of the statistical prediction model to later development stages. — Decided by the user.
2026-09-27 — Use 6 fictional teams, giving 15 unique unordered team pairings, with 10 historical matches per pairing and 150 historical matches in total. — Decided by the user.
2026-09-27 — Test the MVP with a standard 13+1 Toto ticket containing 14 distinct team pairings selected from the 15 possible pairings; teams may appear in multiple fixtures, but no pair may repeat on one ticket. — Decided by the user.
2026-09-27 — Generate the synthetic dataset once with a documented random seed, store the fixed data in CSV, and retain the generator so the CSV can be recreated. — Decided by the user.
2026-09-27 — Use a historical-match CSV structure that can later be replaced by real football data with minimal changes to the rest of the application. — Decided by the user.
2026-09-27 — Organize the synthetic history as five chronologically ordered double round-robin seasons, yielding 30 matches per season, 150 matches total, 10 matches per team pair, and an equal home/away balance. — Decided by the user.
2026-09-27 — Name the six fictional teams Team A, Team B, Team C, Team D, Team E, and Team F. — Decided by the user.
2026-09-27 — Every historical match record will contain a date, home team, away team, home goals, and away goals; derive the 1/X/2 result from the goals from the home team’s perspective. — Decided by the user.
2026-09-27 — Assign dates in a realistic chronological sequence across all five synthetic seasons. — Decided by the user.
2026-09-27 — Generate synthetic scores using fixed hidden team strengths, a modest home advantage, and random variation so draws and occasional unexpected results remain possible. — Decided by the user.
2026-09-27 — Keep hidden strengths exclusively inside the data generator; exclude them from the historical CSV and predictor so team differences must be inferred only from historical match results. — Decided by the user.
2026-09-27 — Use a transparent points-and-goal-difference rating as the MVP predictor, based on historical points per match, goal difference per match, and home/away performance, to produce 1/X/2 predictions. — Decided by the user.
2026-09-27 — Leave the predictor’s exact component weights and draw threshold undecided until the alternatives and their effects have been explored. — Decided by the user.
2026-09-27 — Use fixed, documented predictor parameters for the framework-focused MVP instead of selecting them through backtesting; defer tuning and sophisticated statistical evaluation to a later stage. — Decided by the user.
2026-09-27 — Normalize the predictor inputs as proposed, weight points performance at 70% and goal-difference performance at 30%, and weight overall and venue-specific performance equally within each component. — Decided by the user.
2026-09-27 — Use a normalized rating-difference draw threshold of 0.10: predict 1 above the threshold, 2 below its negative, and X within the draw band. — Decided by the user.
2026-09-27 — Treat the predictor parameters as explicit, replaceable MVP rules rather than statistically optimized values. — Decided by the user.
2026-09-27 — Open the Streamlit MVP with the same fixed, valid, prefilled 13+1 sample ticket on every start; it contains 14 of the 15 possible unique team pairings and remains fully editable. — Decided by the user.
2026-09-27 — Allow users to change every ticket row’s home and away teams through dropdowns, while enforcing all defined 14-match ticket validation rules before prediction. — Decided by the user.
2026-09-27 — Include an optional transparency section showing each prediction’s home rating, away rating, and rating difference without exposing generator-only hidden information. — Decided by the user.
2026-09-27 — Treat the 13+1 ticket as one atomic unit: if any fixture is invalid, generate no predictions until the entire 14-match ticket is valid. — Decided by the user.
2026-09-27 — On ticket validation failure, identify every affected position with a clear correction message while preserving all current dropdown selections. — Decided by the user.
2026-09-27 — Once ticket validation succeeds, generate and display predictions for all 14 fixtures together. — Decided by the user.
2026-09-27 — Require at least 10 total historical matches per team and at least 5 historical matches at the relevant venue before predicting a fixture. — Decided by the user.
2026-09-27 — Define the minimum total-history and venue-history requirements as clearly named configuration constants so they can be changed for future real data. — Decided by the user.
2026-09-27 — Keep synthetic-generator validation separate from source-independent application data validation. — Decided by the user.
2026-09-27 — Generate home and away goals with independent Poisson draws whose expected values use a base scoring rate, the hidden team-strength difference, and a fixed home advantage. — Decided by the user.
2026-09-27 — Configure the synthetic generator with random seed 20260927, base expected goals 1.35, and home advantage 0.20. — Decided by the user.
2026-09-27 — Configure hidden generator-only strengths as Team A +0.35, Team B +0.20, Team C +0.08, Team D -0.05, Team E -0.18, and Team F -0.32. — Decided by the user.
2026-09-27 — Treat all generator values as synthetic parameters, not statistically calibrated football parameters. — Decided by the user.
2026-09-27 — Enforce a strict runtime boundary: the generator creates the fixed historical CSV, while the Streamlit application and predictor neither import nor execute the generator nor access hidden strengths, and use only the CSV. — Decided by the user.
2026-09-27 — Label the five synthetic seasons 2020-21, 2021-22, 2022-23, 2023-24, and 2024-25. — Decided by the user.
2026-09-27 — Schedule each synthetic season as 10 matchdays with 3 matches per matchday, covering every team pair once in matchdays 1–5 and repeating those fixtures with home and away reversed in matchdays 6–10. — Decided by the user.
2026-09-27 — Space matchdays deterministically three weeks apart, allow all three fixtures on a matchday to share a date, and build and process the full schedule in stable deterministic order. — Decided by the user.
2026-09-27 — Use the exact fixed sample ticket: 1 Team A–Team B; 2 Team C–Team A; 3 Team A–Team D; 4 Team E–Team A; 5 Team A–Team F; 6 Team B–Team C; 7 Team B–Team D; 8 Team B–Team E; 9 Team F–Team B; 10 Team C–Team D; 11 Team E–Team C; 12 Team F–Team C; 13 Team D–Team E; 14 (+1) Team D–Team F, omitting Team E–Team F. — Decided by the user.
2026-09-27 — Store the fixed startup ticket in sample_ticket.csv with columns position, home_team, and away_team; load and validate it at application startup. — Decided by the user.
2026-09-27 — Copy the startup ticket into editable Streamlit session state; never persist user edits to sample_ticket.csv, and restore the original ticket on application restart. — Decided by the user.
2026-09-27 — Include an automated pytest suite in the MVP covering the synthetic generator, historical-data loader, statistics calculation, predictor, ticket validator, and observable end-to-end workflow. — Decided by the user.
2026-09-27 — Verify Streamlit behavior primarily through a short documented manual smoke test instead of extensive automated UI testing. — Decided by the user.
2026-09-27 — In the automated end-to-end test, use only the generated historical CSV and sample ticket as application inputs and never access the generator’s hidden team strengths. — Decided by the user.
2026-09-27 — Use a src/toto_estimator package structure and pyproject.toml for project metadata, runtime dependencies, development dependencies, and pytest configuration. — Decided by the user.
2026-09-27 — Use the proposed module responsibility boundaries, including a service.py orchestration layer independent of Streamlit and a synthetic-data generator completely separate from the runtime application. — Decided by the user.
2026-09-27 — Preserve the README’s broader project scope, including the planned use of real historical football data; treat the synthetic-data MVP as the first implementation step toward that broader version rather than redefining the overall project. — Decided by the user.
2026-09-27 — Support Python 3.11 or newer while developing and verifying the MVP with the currently installed Python 3.13 environment. — Decided by the user.
2026-09-27 — Use streamlit, pandas, and numpy as runtime dependencies, with pytest as a development dependency. — Decided by the user.
2026-09-27 — Generate the fixed synthetic dataset with an explicit numpy.random.Generator(numpy.random.PCG64(20260927)) setup. — Decided by the user.
2026-09-27 — Treat the committed historical CSV as the canonical application input, record its SHA-256 checksum, and verify that checksum to detect unexpected changes to the fixed dataset. — Decided by the user.
2026-09-27 — Calculate each fixture’s Poisson rates additively as home rate = 1.35 + home strength − away strength + 0.20 and away rate = 1.35 + away strength − home strength. — Decided by the user.
2026-09-27 — Process fixtures in deterministic schedule order and, for every fixture, draw home goals first and away goals second. — Decided by the user.
2026-09-27 — Name the OpenSpec change for the synthetic-data MVP `build-synthetic-toto-mvp`. — Decided by the assistant.
2026-09-28 — Place runtime modules under `src/toto_estimator`, keep the synthetic generator in `scripts/generate_synthetic_history.py`, use a thin root `app.py`, and store canonical CSV and checksum assets under `data/`. — Decided by the assistant.
2026-09-28 — Build each season’s deterministic fixture order with the circle method using Team A through Team F, and start each season on the first Saturday on or after August 10 of its starting year. — Decided by the assistant.
2026-09-28 — Serialize the canonical historical dataset as deterministic UTF-8 CSV with LF newlines, fixed column and row order, ISO dates, and no dataframe index; store its lowercase SHA-256 digest in standard checksum-file form. — Decided by the assistant.
2026-09-28 — Normalize overall, home, and away points-per-match and goal-difference-per-match series independently with min-max normalization, using 0.5 when a series has no range. — Decided by the assistant.
2026-09-28 — Use `toto-estimator` as the Python distribution name with initial package version 0.1.0. — Decided by the assistant.
2026-09-28 — Make the repository-root Streamlit launcher add the local `src` directory explicitly so the documented run command does not depend on editable-install `.pth` processing. — Decided by the assistant.
2026-09-28 — Document a normal local package installation instead of an editable installation because Python 3.13 skips the editable `.pth` file when macOS marks it hidden on this iCloud-backed workspace. — Decided by the assistant.
