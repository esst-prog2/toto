# Project process

## 2026-11-26 — Statistical model development Phase 1 audit

Executed the attached TOTOdology Phase 1 instructions on `feature/statistical-model`, inspecting clean baseline `878d45e47f1ef861b1b774ecc89c94af7851cb34`. PROCESS.md was absent and is created by this audit.

Deliverables: [current model](docs/statistical-model/current-model-audit.md), [data readiness](docs/statistical-model/data-readiness-audit.md), [feature availability](docs/statistical-model/feature-availability.md), [existing evaluation](docs/statistical-model/evaluation-audit.md), and [modelling readiness summary](docs/statistical-model/modelling-readiness-summary.md).

Findings: implemented synthetic deterministic MVP differs from planned probabilistic workflow; 1,312 real matches locally available, while private multi-league datasets/sidecars are absent here. Collection reports describe 156,321 screened historical rows across 14 competitions; that is documentary coverage, not a fresh data validation. Existing benchmark and both committed artifacts reproduced byte-for-byte in memory: 158/380 correct (41.58%), below the 46.05% always-home baseline. Historical date/result-policy differences and adaptive use of the evaluation season limit forecasting claims.

Verification: complete existing suite passed in an unchanged external environment, 2,678 tests plus 27 subtests, zero failures/errors/skips (20.01 seconds). Exact command, initial missing-pytest attempt and reproducible read-only inspections appear in the evaluation/data reports. No new dependencies, models, features, dataset changes or application changes. Documentation committed locally on the existing branch; no merge, worktree switch or push. Phase 1 complete with explicit evidence limits; stopped pending approval for subsequent statistical work.
