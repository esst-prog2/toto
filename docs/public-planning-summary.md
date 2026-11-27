# Public planning summary

The demonstration uses invented teams and reproducible synthetic fixtures. Its
runtime must work without a private research archive.

Historical research sources, match datasets, provenance, adjudication records and
research logs remain local. A public release must use an explicit file allowlist;
ignore rules do not remove files from the current index or earlier history.

The offline CSV auditor provides structural checks without embedding source data.
Its tests use invented fixtures. Structural validity does not establish source-use
permission or historical completeness.

Historical replay checks must use captured input inventories, validate original
hashes and byte counts, and retain output equality checks. New acquisitions must
not silently change the scope of a frozen replay.

This summary is independently written for publication. It does not replace or
redact the append-only private planning history. Publication and any migration of
previously tracked research material require separate owner approval.

## 2026-11-27 — Hungarian integration and worktree closure

The original `toto` directory on `feature/data-collection` now contains the
consolidated domestic, UEFA Champions League and Hungarian collection work.
Hungarian private sources, intermediate releases, final outputs, provenance,
restrictions and unresolved observations remain under `data/private/hungary/`.
They are not tracked or published by this integration.

| Local inventory | Verified fixtures |
| --- | ---: |
| Existing domestic competitions | 156,579 |
| UEFA Champions League, 34 seasons | 6,642 |
| Hungarian NB I | 8,301 |
| Hungarian NB II | 10,479 |
| **Total distinct match IDs** | **182,001** |

These are aggregate inventory counts, not released fixture records or a claim
that the entire population is eligible for statistical modelling. Existing date,
score-period, administrative, coverage and source-use limitations remain.

Required original files became readable through targeted local materialization;
no dataset replacement was needed. Historical Git-state assertions continue to
verify their captured snapshots, with separate checks for the current archive.
Git bundles and isolated recovery checks complement verified working-file
backups. Both complete planning histories remain preserved locally; this summary
does not replace them or publish their private research additions.

Integration commit `3b94f1c` was published and independently verified before the
redundant `toto-hungary` worktree was removed. Every source-worktree file was
accounted for in retained copies. The local and remote `feature/hungarian-nb1`
branches remain preserved, as do all recovery archives and the promotional worktree.

Verification after removal passed **3,038 tests and 35 subtests**. Original dataset
fingerprints, identifiers and ordering were preserved; Hungarian final outputs
were reproduced offline with access to the removed worktree forbidden. No new
source collection, model development or expansion of publication rights occurred.
