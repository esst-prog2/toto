## Why

The project needs a complete, inspectable first implementation of its Toto prediction workflow before real football data and statistically refined models are introduced. A fixed synthetic dataset lets the application architecture, validation, predictor, and user experience be built and tested reproducibly without making the MVP depend on external data availability.

## What Changes

- Add a deterministic generator that creates five synthetic seasons for six fictional teams and preserves its output as a canonical historical-match CSV with a verified SHA-256 checksum.
- Add source-independent historical-data loading and validation suitable for both the synthetic CSV and future real match data with the same schema.
- Add transparent team statistics and a fixed rules-based predictor that produces `1`, `X`, or `2` from points, goal difference, and overall/venue performance.
- Add loading and atomic validation for a fixed, editable 14-fixture 13+1 sample ticket.
- Add a local Streamlit interface that preserves session edits, reports all ticket errors, displays all predictions together, and optionally exposes rating details.
- Add a service layer independent of Streamlit plus automated tests for the generator, data loading, statistics, prediction, ticket validation, and end-to-end workflow.
- Keep real football data integration, model tuning, sophisticated evaluation, and a production web application outside this MVP.

## Capabilities

### New Capabilities

- `synthetic-match-history`: Deterministic generation, storage, integrity checking, loading, and source-independent validation of the fixed historical match dataset.
- `match-outcome-prediction`: Calculation of transparent historical team ratings and fixed-parameter `1`/`X`/`2` predictions with minimum-history enforcement.
- `toto-ticket-workflow`: Loading, editing, validating, and predicting the fixed 14-position sample ticket as an atomic unit.
- `streamlit-mvp`: Local Streamlit presentation of the editable ticket, validation feedback, predictions, and optional rating transparency.

### Modified Capabilities

None. The project has no existing capability specifications.

## Impact

- Introduces a Python 3.11+ package under `src/toto_estimator`, a separate synthetic-data generator, CSV data assets, a Streamlit entry point, and a pytest suite.
- Adds runtime dependencies on Streamlit, pandas, and NumPy, with pytest as a development dependency, configured through `pyproject.toml`.
- Establishes CSV and service boundaries intended to support later replacement of synthetic history with real football data without coupling runtime code to generator-only parameters.
- Does not change the README's broader project direction toward real historical football data.
