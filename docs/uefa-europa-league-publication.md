# Europa League publication proposal — approval pending

Date: 2026-11-28. This is an exact **28-file public-safe proposal**, not publication authorization. Nothing has been staged, committed or pushed.

Proposed commit message: `Finalize UEFA Cup and Europa League historical workflow`

## Exact allowlist

- `PROCESS.md`
- `config/uefa_competition_registry.json`
- `scripts/acquire_uefa_europa_league.py`
- `scripts/assess_uefa_europa_league_phase1.py`
- `scripts/check_uefa_europa_league_corruption.py`
- `scripts/check_uefa_europa_league_final_corruption.py`
- `scripts/finalize_uefa_europa_league.py`
- `scripts/inventory_uefa_europa_league.py`
- `scripts/reproduce_uefa_europa_league_pipeline.py`
- `scripts/reproduce_uefa_europa_league_standardization.py`
- `scripts/review_uefa_europa_league_history.py`
- `scripts/standardize_uefa_europa_league.py`
- `scripts/uefa_europa_league_sources.py`
- `scripts/verify_uefa_europa_league_final.py`
- `scripts/verify_uefa_europa_league_history.py`
- `scripts/verify_uefa_europa_league_inventory.py`
- `scripts/verify_uefa_europa_league_standardization.py`
- `tests/test_uefa_europa_league_acquisition.py`
- `tests/test_uefa_europa_league_final.py`
- `tests/test_uefa_europa_league_history.py`
- `tests/test_uefa_europa_league_inventory.py`
- `tests/test_uefa_europa_league_standardization.py`
- `docs/uefa-europa-league-phase1.md`
- `docs/uefa-europa-league-phase2.md`
- `docs/uefa-europa-league-phase3.md`
- `docs/uefa-europa-league-phase4.md`
- `docs/uefa-europa-league-phase5.md`
- `docs/uefa-europa-league-publication.md`

## Exclusions and review boundary

`PLANNING_LOG.md` is modified append-only but excluded: the accumulated local planning history has not been cleared for publication. Preserve it locally. Only the reviewed method additions in PROCESS.md belong to this proposal. Do not use `git add .` or include all modified files indiscriminately.

All of `data/private/` remains ignored and untracked: the finalized CSV, original payloads, observation/adjudication inventories, identity mappings, source crosswalks, exclusion/venue records, evidence, permission drafts and detailed validation receipts are **private/local-only**. Standardization does not remove the original redistribution limits. Permission drafts remain unsent; future permission-dependent material is excluded. Unclear files are excluded by default.

The scripts contain generic processing logic, declared country/competition policy and source URLs. Tests use synthetic inputs. Reports contain aggregate counts, methods and bounded public source references, not copied restricted fixture rows. The JSON registry contains only local competition policy. No private data, credentials or secrets belongs in the allowlist.

The private `phase5/publication_manifest.json` binds every proposed file by SHA-256, classifies every changed/untracked path, records the reviewed prospective diff and secret scan, and identifies the exclusion of the planning log. This document intentionally omits hashes of itself to avoid a self-reference cycle.

Approval must cover the final report, exact manifest and proposed commit message. If any file changes after approval, refresh the relevant review and hashes before publication. Actual dataset publication and combined integration require separate authorization and rights clearance.
