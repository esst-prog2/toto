# UEFA Cup / UEFA Europa League — Phase 5 finalization and final acceptance

Date: 2026-11-28. Worktree: `toto-uefa`; branch: `feature/uefa`. HEAD remains `96d2302f5eaa63ef78630f335b39ddee817aa956`.

## A. Final phase status

**CONDITIONAL PASS — standalone five-phase work completed and ready for conditional owner acceptance.** The local dataset is finalized, independently validated and unchanged from the accepted Phase 4 CSV. Actual identity reconciliation has been performed across all remaining abbreviation cases; supported mappings and unresolved boundaries are explicit. Publication and combined integration have not occurred.

The conditions are precise: `uefael` is locally registered and collision-free against the current inventory, but formal registration in the original-worktree consolidated builder is pending a separate integration operation. Complete project-wide club identity compatibility remains unverified for unresolved aliases and continuity. Neither condition is concealed by the workflow-completed statement.

## B. Final dataset

Exact final path, relative to this worktree:

`data/private/europe/europa_league/phase4/validated/uefa_europa_league_standardized_1990_2026.csv`

SHA-256: **`7d1a4084094368b2a8b17be84b87124ec65d53b0f4beb4184290ceb6e7d43fde`**.

The accepted Phase 4 CSV is **byte-identical**. No display name, date, score, neutral flag or match identifier changed in Phase 5. The final manifest in `phase5/final/final_dataset.json` references this existing file rather than creating another large copy.

| Final population | Verified result |
|---|---:|
| Standardized matches | 11,422 |
| Seasons, 1990/91–2025/26 | 36 |
| Main competition | 6,506 |
| Qualifying | 4,916 |
| Preserved exclusions | 68 |
| All adjudicated records | 11,490 |
| Neutral-format matches | 38 |
| Estimated dates / outcome-only rows | 0 / 0 |

Historical labels remain UEFA Cup through 2008/09 and UEFA Europa League thereafter. Qualifying and main matches share the continuous competition namespace and retain stage/scope/leg/replay metadata. 2026/27 and unrelated UEFA competitions were not acquired.

Exact confirmed schema:

```csv
match_id,country,league,season,date,home_team,away_team,home_goals,away_goals,neutral_venue
```

UTF-8 without BOM, LF, ordinary quoting, no index; ISO dates, consecutive YYYY/YYYY seasons and nonnegative integer goals. The full coverage matrix is the accepted `phase4/validated/season_coverage.csv`; all 36 seasons reconcile independently.

## C. Competition and club identities

### Competition registration

`config/uefa_competition_registry.json` now registers **`uefael` locally** for both historical league labels, scope MAIN and QUALIFYING, country `uefa`, 24-character IDs. The owner accepted this prefix in principle subject to compatibility; the confirmed six-character UEFA convention and absence of namespace/ID collisions satisfy the local check. The existing normalization, season/date encoding and four-character team tokens remain unchanged.

The precise original-worktree proposal is private `final/registration_proposal.json`: add `UEFA Cup: (uefa, uefael)` and `UEFA Europa League: (uefa, uefael)` to the existing `scripts/build_final_data_sum.py:COMPETITIONS`, preserving every old entry. No external registry was edited. **Local registration is complete; formal global registration is not claimed.**

### Actual reconciliation results

All **228 Phase 4 ambiguity cases** were investigated: 153 local multi-label abbreviation groups plus 75 cross-baseline label/token overlaps. These categories overlap in labels and records and are not a count of distinct clubs.

- **189 cases resolved** through scoped alias, distinct-club/context or full-label spelling evidence.
- **39 cases unresolved or partially resolved**; every remaining pair and affected event is retained explicitly.
- **2,401 of 4,936 seasonal participant mappings** link to a single supported existing project identity ID.
- **2,535 retain their accepted seasonal identity** because there is no unique, qualified existing project ID. These include new-to-baseline clubs and historical/association ambiguities, not 2,535 known errors.
- **3,807 matches** have both participants mapped to available existing project IDs; all 11,422 remain in the historical dataset.

Read-only inspection used the actual newer project `identity-v1` registry, source-backed evidence graph, blocked links and prepared-record inventory. It was not assumed that the older final exports constituted a complete identity registry. The 1,900 available mapping rows and supporting source fingerprints remain reference-only; the original statistical-model code/data was not modified or executed for fitting.

Five concepts remain separate: displayed name; four-character match-ID abbreviation; existing canonical/project club ID; historical alias; and the qualified cross-competition mapping. The private `club_identity_crosswalk.json` records all five, original seasonal identity, source-association declarations, existing registry rows, candidate IDs and affected events. Reconciliation introduces **zero match-ID changes**.

Evidence-backed case methods include: existing source-qualified project alias paths; names occurring for the same accepted season participant; association-qualified stable provider catalogue IDs where no refoundation annotation or corrected provider occurrence is used; original opponent co-occurrence; disjoint documented association contexts; and directed primary club/federation evidence. Full-label punctuation/diacritic correspondence resolves a label question only, without allocating a new global identity or asserting succession. Provider continuity and coeval aliases are explicitly bounded; sensitive continuity labels retain separate season contexts.

Targeted primary references establish, for example, separate clubs in the [FAW composition list](https://media-faw-cymru.s3.eu-west-2.amazonaws.com/faw/20250604094634/2025-26-FAW-Mens-National-Leagues-Composition.pdf), the [Northern Ireland league directory](https://www.nifootballleague.com/premiership/2023-2024/clubs/), and [Norwegian federation head-to-head records](https://www.fotball.no/fotballdata/kamp/?fiksId=8986847). A [club museum history](https://www.fcnantes.com/musee/articles/article2809.php?num=24101) supports a historical name correspondence. These are bounded factual notes, not newly acquired fixture corpora or full copied articles.

The 39 remaining cases have no complete positive path for every label/context, or involve reserve/successor/merger/association boundaries. They retain distinct historical identities and precise pair-level evidence gaps. Do not interpret similar abbreviations, different provisional IDs, translated city names or a modern club label as a universal legal-continuity certificate. Complete global identity compatibility remains NOT VERIFIABLE. Cross-competition statistical preparation must use the supported links and preserve unresolved contexts separately; no fitting population was silently enlarged.

## D. Final validation

### Historical and regulation guarantees

All 11,422 rows were revalidated exhaustively against accepted evidence. Goals equal the supported regulation result, including stoppage time and excluding extra time/shootouts/aggregates. Administrative awards remain separate. The one match abandoned during extra time retains completed regulation and its separate partial/awarded results; all five pre-regulation-completion abandonments remain excluded. Nominal orientation is unchanged.

The Phase 4 date correction remains explicit: the original Phase 3 date, corrected playing date, source checksum/locator, [UEFA contemporary evidence](https://www.uefa.com/uefaeuropaleague/news/025a-0eaad371d500-9ec4de3a2afe-1000--dortmund-ease-past-austria/), standardized date, derived match ID and original-ID crosswalk are bound and compared. Scores and eligibility did not change. All 4,251 supported two-leg chronology comparisons and 36 final-progression checks pass. No Phase 3 artifact was rewritten.

All 38 `neutral_venue=1` rows retain the established **official competition-format** meaning, not a new physical-stadium-neutrality assertion. Early hosted two-legged finals remain hosted. Relocation alone is not neutrality. Evidence and qualifications stay reversible, and nominal orientation is preserved.

The original bridges remain exact: **12,311 + 5 − 826 = 11,490**, and **11,422 + 68 = 11,490**. Exclusions remain **5 incomplete / 4 not played / 59 outside scope**, with all original observations and separate historical contexts recoverable.

### Eighteen output guarantees

| No. | Guarantee | Final result |
|---|---|---|
| 1 | 36 target seasons | PASS |
| 2 | 11422 standardized matches | PASS |
| 3 | 6506 main matches | PASS |
| 4 | 4916 qualifying matches | PASS |
| 5 | 11490 historical records accounted | PASS |
| 6 | 68 exclusions preserved | PASS |
| 7 | Valid supported regulation scores | PASS |
| 8 | No period contamination | PASS |
| 9 | Administrative results separate | PASS |
| 10 | Valid actual playing dates | PASS |
| 11 | No estimated dates | PASS |
| 12 | Unique approved-convention match identifiers | NOT VERIFIABLE |
| 13 | Global team identity/code compatibility | NOT VERIFIABLE |
| 14 | Neutral evidence preserved | PASS |
| 15 | Reversible provenance | PASS |
| 16 | Confirmed current CSV schema | PASS |
| 17 | Deterministic output | PASS |
| 18 | Prior data and protected files preserved | PASS |

**16 PASS, zero FAIL, two NOT VERIFIABLE.** The registry-related condition now distinguishes successful local registration from pending formal global registration. The identity condition now has 189 resolved cases and supported existing-ID links, while complete compatibility remains unverified. Neither prior condition was upgraded to an unsupported global PASS.

The separate final validator reconstructs association bindings from original observations after accepted corrections, checks every existing-ID candidate, canonical assignment and pair decision, and independently checks semantic overlap where identities are available. Only declarative country policy is shared with the finalizer. It does not reuse the finalizer's transformation or case-resolution functions. The inherited independent standardization validator continues its exhaustive row/byte/score/date/exclusion/neutral/provenance checks. This is independent processing verification, not independent historical certification of every original source fact.

### Complete tests and adverse checks

The **complete applicable repository suite passes: 3,057 tests and 27 subtests**, including 28 new Phase 5 synthetic tests and all existing domestic, Champions League, Europa League Phase 1–4, schema, identifier, preservation and validation tests. There are zero failures, errors, skips or blocked tests in this run. Private external raw archives are not implied to have been tested merely because the synthetic/public-code suite passes.

All **33 adverse corruptions** are detected: the previous 22 plus 11 finalization cases for invalid/unregistered prefixes, false global registration, wrong canonical mapping, accidental unresolved-club merger, wrong historical alias, lost identity cases, false case closure, unreported ID collision, overstated semantic coverage and missing historical registration. Tests use disposable serialized copies; accepted artifacts remain untouched.

### Complete offline rebuild

A fresh process with connections and DNS prohibited reproduces **48 artifacts byte-for-byte**: Phase 1 diagnostics/manifest/coverage (4); fresh raw Phase 2 inventories plus independent receipt (12); Phase 3 adjudication plus independent receipt (14); Phase 4 standardized outputs plus independent receipt (13); and final Phase 5 metadata plus independent receipt (5).

There is no observation cache. Original payloads, recorded historical decisions, code snapshots, mapping evidence and local policy produce the accepted results offline. Fresh phase outputs feed subsequent transformations; immutable receipts/decision inputs remain bound. The final CSV checksum, ordering, exclusions, IDs, mapping, neutral metadata, coverage, corrections and validation receipts agree. No additional online acquisition is required. The fingerprinted research notes preserve their access/source limitations; full publisher articles were not retrospectively invented as retained payloads.

## E. Coverage and preservation

All 36 seasons remain represented, with no newly identified missing played target fixture. Existing completeness qualifications remain: bracket/count agreement does not certify every historical attribute independently. No scope expansion or new historical score/date correction was introduced in Phase 5.

The final preservation baseline contains **654 local fingerprints**: **652 files remain byte-identical**, and PLANNING_LOG.md / PROCESS.md retain their exact original prefixes with authorized appended additions. All **85 original payloads / 44,970,420 bytes**, accepted Phase 1–4 artifacts, decisions, exclusions and provenance remain preserved. All **16 original-worktree reference files** and the four additionally inspected identity/model reference files are unchanged.

The accepted standalone CSV and existing domestic/Champions League final exports, identifiers, global crosswalk and audit remain unchanged. No unrelated worktree, model, Streamlit file or private archive was altered. Preservation does not claim exhaustive fresh certification of inaccessible domestic/UCL raw archives, all other worktree files, installed packages or Git object storage. The lack of those unrelated raw archives does not block local Europa League finalization.

## F. Licensing and publication preparation

The final CSV and all detailed real-data artifacts remain **private/local-only and not cleared for public redistribution**. Source transformation does not remove RSSSF, noncommercial, attribution/share-alike or other underlying restrictions. Training/commercial rights and independent publisher lineage are not newly certified. Permission drafts remain unsent and preserved. Git-ignore separation is verified, with the existing iCloud configuration unchanged.

The exact proposed **28 public-safe files** are listed in [the publication proposal](uefa-europa-league-publication.md). They contain generic code, synthetic tests, local competition policy and aggregate documentation. The private `publication_manifest.json` binds their hashes, classifies every changed/untracked path and records the reviewed prospective diff and credential scan. Raw payloads, standardized CSV, intermediate inventories, historical decisions, identity mappings, provenance, detailed validation artifacts and drafts are excluded. PLANNING_LOG.md remains local because its accumulated history is not publication-cleared. Unclear or permission-dependent files are excluded by default.

Proposed commit message: **`Finalize UEFA Cup and Europa League historical workflow`**.

Nothing has been staged, committed, pushed or published. User acceptance must cover the final report and exact publication manifest before any such operation. Dataset publication would additionally require rights clearance; approval of code/docs is not approval to publish data.

## G. Non-destructive integration readiness

The latest accessible inventory was independently rechecked at **182,001 records**. The final EL population is **11,422**, so the conditional prospective total is **193,423**. Local and current-global match-ID collisions are zero. Current schema, types, date/season encoding, column order and neutral semantics are confirmed compatible.

Semantic uniqueness is assessed separately from identifier uniqueness. There is no identified overlap under full-label/date checks across the inventory, or under existing project IDs for the 3,807 fully linked matches. **Complete semantic non-overlap cannot be certified for unresolved aliases.** The prospective total therefore remains conditional, rather than a claim that different namespaces prove different historical matches.

A separate authorized integration should: recheck the current global hashes/counts; apply the precise two-entry registration proposal; preserve every existing record and ID; consume supported identity links while isolating unresolved contexts; repeat both ID and semantic overlap checks; retain neutral and exceptional provenance; and observe source licensing. Only then prepare any combined-data transaction. No combined dataset or external registry was changed here.

## H. Overall five-phase result

| Phase | Accepted/final status | Principal deliverable | Final relevance |
|---|---|---|---|
| 1 — discovery/acquisition | PASS | 85 preserved originals across Phase 1/2 | Original evidence and rights trail retained |
| 2 — structural inventory | CONDITIONAL PASS, accepted | 38,126 observations; 12,311 conditional events; 1,896 cases | Reproduced raw inventory and source lineage |
| 3 — historical adjudication | PASS, accepted | 11,490 adjudicated records; 11,422 inclusions | Preserved original decisions and exclusions |
| 4 — standardization | CONDITIONAL PASS, accepted | Ten-column CSV; one evidenced derivative date correction | Final CSV preserved byte-for-byte |
| 5 — finalization | CONDITIONAL PASS | Local registration, actual identity reconciliation, final audit and publication proposal | Ready for conditional final owner acceptance |

Phase 1 originally acquired 75 payloads; ten targeted originals were added in Phase 2. The 85 total is not retroactively described as the original Phase 1 count. The one Phase 4 correction does not erase or rewrite the accepted Phase 3 evidence.

Detailed final artifacts are under `data/private/europe/europa_league/phase5/`: `final/final_dataset.json`, `final/club_identity_crosswalk.json`, `final/identity_case_dispositions.json`, `final/registration_proposal.json`, `independent_validation.json`, `adverse_validation.json`, `pipeline_reproduction.json`, `publication_manifest.json` and `verification.json`. Earlier draft ledgers and diagnostic receipts remain preserved privately and are clearly distinguished from final outputs.

The standalone five-phase workflow is complete **with the stated registration and identity conditions**. It is ready for final user acceptance. **Stop before publication or actual combined integration; await explicit authorization.**
