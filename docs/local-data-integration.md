# Local research data integration

Competition research archives belong under `data/private/`, using the existing
competition-specific source, intermediate, adjudication and versioned-output
directories. Keep original bytes, provenance, permissions, exclusions and review
queues together. Git integration and a verified local archive transfer are
separate operations; neither substitutes for the other.

Use the shared importer, schema validators and data loader where their contracts
apply. Legacy eight-column research releases remain readable without inventing
neutral-venue information or rewriting their identifiers. A successful load is
not permission clearance or statistical modelling eligibility. Preserve date
uncertainty, score-period distinctions, administrative decisions and original
ordering in the archived CSVs. Do not concatenate research releases into a
model-ready population merely because they pass structural validation.

Historical acquisition audits may require an old commit and its captured index.
`toto_estimator.audit_snapshot` checks that the captured index represents the
recorded ancestor and supplies isolated temporary Git metadata for replay. It
does not change the current branch, index or historical receipts. Preserved
source snapshots support historical byte comparisons; separate current-state
checks must protect the actual integrated archive and current implementation.

Research helpers, archive-dependent tests, reports and their local pytest fixture
remain excluded from public commits. The synthetic application and the new
generic snapshot tests do not require a private archive. Install the optional `research`
dependency group when running the local source-parser tests; normal development
dependencies remain in `dev`.

Before committing an integration, inspect every staged path and its contents.
Keep source-use restrictions and research-bearing planning additions local.
Retain recovery references, verified history bundles and checksummed working-file
backups. Do not remove a source worktree until its replacement passes preservation,
reproduction and operational-independence checks and its owner approves removal.
