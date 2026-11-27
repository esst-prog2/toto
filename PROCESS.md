# Project data process

Use the [controlled five-phase workflow](docs/accelerated-five-phase-workflow.md).
Each phase ends with a report and explicit owner approval before the next phase.
No phase approval implicitly authorizes publication, training or a broader source scope.

## Score-period requirement

Owner-approved on 2026-11-26: model-eligible **played matches** require a supported
regulation-time result: 90 minutes plus stoppage time, excluding extra time and
penalty shootouts. The advancing team, aggregate winner and first printed score
are not substitutes for that result. The current canonical v2 schema appends
`neutral_venue` to the original eight columns; score semantics remain unchanged.

Preserve original source bytes and every reported period separately in private
metadata: regulation, half-time, cumulative after-extra-time, extra-time-only,
shootout and tie aggregate, with source-specific semantics and uncertainties.
An unspecified `fullTime` field or single parenthesized score is insufficient to
infer a missing regulation score. Unknown periods remain unknown and are queued
for review; no silent repair, score substitution or unsupported inference is allowed.
Preserve stage, round, group, path, leg, status and source-designated orientation.
Parsers and independent validators must retain period annotations through every
intermediate representation. Test extra-time-first and shootout-first notations.

## Administrative results and scope

The previously approved retrospective internal-diagnostics policy remains in force:
original football dates and sufficiently supported accepted final historical
administrative results, without administrative-publication-date filtering. Keep
observed regulation scores distinct from accepted administrative outcomes and
label the policy exception in private audits. Do not misclassify an award as extra
time. Existing no-kickoff, abandonment, replay, eligibility and exclusion decisions
remain unchanged; this methodological requirement does not reopen domestic decisions.

## Approved competition-format neutrality and schema v2

Owner-approved Phase 4, 2026-11-27: `neutral_venue` describes the **official
competition format**, not the physical stadium or measured home advantage:
0 = conventional home/away format; 1 = officially neutral-site format; blank/NA =
format genuinely unestablished. This supersedes the physical-venue interpretation
used in frozen Phase 3 private metadata; those earlier observations stay unchanged.
The project-wide [canonical v2 schema](docs/match-schema.md) appends this ninth
column. Historical v1 adapters and six/eight-column synthetic inputs remain
explicitly supported; newly standardized UCL output and current standardized
domestic datasets use v2. Frozen audit archives and unstandardized data are excluded.

Preserve first-listed/home and second-listed/away orientation and their scores.
Outcome encoding remains 1/X/2 for first-listed win/draw/second-listed win, including
neutral matches. Future neutral matches should contribute to overall team performance
without automatically contributing to home-specific or away-specific statistics.
Official neutral-format finals remain 1 even at a participant's usual stadium.
Centralized neutral knockout/preliminary tournaments are 1; ordinary home/away
qualifiers, league/group fixtures and hosted knockout ties are 0. A single-leg tie,
relocation or stage name alone does not establish neutrality. In particular the
home-hosted 1993/94 UCL semifinals and 2020/21 Q1–Q3 single-leg qualifiers are 0.
Keep actual venue and relocation evidence separately; do not require comprehensive
stadium research or infer actual home advantage from this variable.

Phase 4 authorizes metadata migration of the 16 current domestic CSVs, 156,579
records in 14 competitions, including the two frozen ongoing English snapshots.
Only append the new column: preserve all eight existing fields, IDs and row order,
and verify that removing it reproduces the old bytes. Retain exact private backups,
before/after hashes and per-file comparisons; do not rewrite prior audit manifests.
The accepted score-period audit therefore remains valid with its original limits.

## Deployment and source permissions

The approved deployment strategy remains local/private real-data processing and
modeling, with only a synthetic-data demonstration publicly deployed. Historical
datasets and supporting evidence remain private. Private use does not override an
explicit source restriction: document concrete attribution, retention, use and
acquisition limits without reopening the deployment strategy. Phase 3 supplemental
qualifying recovery is owner-authorized, subject to bounded plans and source-specific
permission checks; it does not authorize restricted scraping, purchases or contacts.

Keep all existing domestic competition exclusions, including excluded knockout
playoffs and cross-division fixtures. A stage called “playoff” is not automatically
an extra-time contest: season-specific league-group and knockout rules differ.
Scope changes and uncertain historical decisions require explicit approval.

## Accepted domestic retrospective audit

The owner accepted the [domestic score-period audit](docs/domestic-score-period-audit.md)
on 2026-11-26. It found no identified extra-time/shootout contamination in 156,579
standardized domestic records across 14 competitions. No standardized correction
was required or made. Fifteen acquired Serie B extra-time records, including three
shootouts, remain excluded. Four excluded intermediate records lose an extra-time
annotation even though the originals preserve it; future adapters must prevent this.
This is a bounded audit, not independent certification of every historical fixture.

The exact accepted report, evidence appendix, hashes, diagnostic registries and
audit scripts are preserved byte-for-byte under the Git-ignored private location
`data/private/audits/domestic_score_period/2026-11-26/`. Detailed match records,
originals, standardized datasets, receipts and evidence must remain private.
Preserve source attribution and all licensing/model-training restrictions.

## Completeness and validation

Report coverage separately by season and stage; preserve missing/unscored fixtures,
source overlaps and quarantines without fabricating records. Prioritize recent
seasons when addressing gaps, consistent with the owner's time-weighted completeness
priority. No numerical completeness weights or decay formula were located in the
repository during the Champions League Phase 2 inspection. The owner explicitly
approved recent-first priorities and reporting numerical weights as unspecified.
Report exact unweighted coverage; do not invent numerical weights or change the model.

Independently reconstruct inventories from original bytes using a separate parser;
compare identical score periods and disclose shared or unknown upstream lineage.
Use focused synthetic/regression checks at intermediate phases, deterministic offline
reproduction and preservation fingerprints. Reserve the full suite for finalization
unless a material integration risk or explicit owner instruction requires it.
The schema-changing UCL Phase 4 explicitly requires the complete repository suite.
Stop for systemic provenance,
integrity or privacy failures; isolate traceable source problems and retain gaps.
