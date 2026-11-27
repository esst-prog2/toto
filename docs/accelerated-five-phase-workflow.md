# Accelerated five-phase competition workflow

Prepared 2026-11-26 against Belgian completion commit `b59b274b3177a34ffe7adfe993ae3f54be5a5f15`: 13 completed competitions, 16 remaining. Process exactly one competition at a time. This specification authorizes no acquisition, dataset changes or publication.

## Operating contract

Each phase ends with one short report and a stop. Explicit owner approval of the report and authorization of the next numbered phase are required before proceeding; silence is not approval. Phase 5 requires separate explicit approval of the concrete public staging list and commit/push plan before publication, then a final report and stop. Never automatically start the next competition.

Preserve all 13 completed competitions, original sources, datasets, adjudications, historical outputs, Git history, application and environment. Use the existing approved interpreter; no installation, upgrade, environment rebuilding, model training or application integration. Record baseline HEAD, branch, index, existing dirty paths and protected-file SHA-256 manifest before execution. Protect all prior standardized datasets and relevant audit/source artifacts; identify the exact preservation scope. An incomplete optional broader scan must be disclosed, never described as exhaustive. Never overwrite a frozen artifact or use `--force` to evade a guard.

Classify source issues by evidence and containment, rather than blocking a competition for every anomalous row:

| Issue class | Required action | Can the authorized phase continue? |
|---|---|---|
| **Recoverable source issue** | Inspect the affected original records, compare available evidence first, and establish exact fixture correspondence and source independence. Record a deterministic source-specific correction in private derived metadata, bound to original file/record hashes and inspected evidence. Preserve original fields/bytes and report the correction's scope and limits. | Yes, within the authorized phase. A correction must follow evidence; date arithmetic, coincidental scores or source agreement with common upstreams alone are insufficient. |
| **Unresolved but isolated issue** | Quarantine all affected source representations with exact locators/hashes, reason and coverage impact. Enforce the exclusion in downstream adapters so another representation cannot silently restore the uncertain record. Continue with unaffected sources and reduced coverage. | Yes, if isolation and preservation checks pass. Missing coverage is an acceptable outcome; no invented dates, results or identities. |
| **Material systemic integrity or privacy issue** | Stop immediately, preserve evidence privately and report **BLOCKED**. Examples include altered immutable originals, untrustworthy provenance across an unbounded population, failed quarantine containment, source-to-record binding failures or private-data exposure. | No. Owner review and a verified remedy are required; never bypass guards. |

Use a private issue ledger recording class, affected population, evidence/independence, correction or quarantine rule, focused checks and residual uncertainty. If the scope cannot be bounded, treat it as systemic until demonstrated otherwise. A contained error may be wider than initially found; expand the diagnostic scope only enough to establish safe boundaries. Ordinary historical result decisions remain in Phase 3; source-repair metadata is not an INCLUDE decision or permission to standardize. Phase reports must distinguish a recovered issue, a residual quarantine and a systemic blocker. Explicit approval remains required after every phase; recovery does not authorize advancement.

Access denials, unexpected redirects or rate-limit responses stop that source's acquisition; do not bypass restrictions. Do not automatically retry an access stop. An explicitly authorized follow-up uses a new scoped plan and preserves the earlier stop record. A failed check or timeout is not a pass.

Use the owner's retrospective internal-diagnostics policy: original football dates and accepted final historical results, including documented later adjudications, without administrative-publication-date filtering. Preserve initial kickoff and completion dates separately for resumptions; explain the selected original football date. This does not establish leakage-free forecasting performance. A result awarded without any kickoff is NOT_PLAYED; do not invent a minute threshold. Preserve reported and accepted scores separately.

Keep originals, standardized CSVs, evidence bundles, detailed inventories, adjudications and audit records under ignored `data/private/`. Public documentation contains methods, aggregate coverage, limitations and validation summaries only; inspect it for copied source records, private evidence, credentials and restricted content. Permitted access is distinct from redistribution and model-training rights. Record attribution, upstream uncertainty, licensing and training restrictions; no new rights follow from validation.

## Existing infrastructure and minimal adaptation

Repository review covered the acquisition/inventory/structure/review/policy/standardization/final-validation script families, corresponding tests, `docs/historical-import.md`, the collection plan, Belgian final-validation report and environment documentation.

| Component | Safe reuse | Competition-specific work |
|---|---|---|
| `src/toto_estimator/historical_import.py`; `src/toto_estimator/match_schema.py` | `HistoricalSource`, `canonical_season`, explicit v2 import support, canonical column definitions, strict metadata/date/score/neutrality validation and existing identity convention; frozen v1 adapters remain compatible | Explicit league/source mappings, encoding, supported input schema and evidence-bound competition-format neutrality. Calendar-year seasons are supported; do not assume European season dates. Inspect importer rejections rather than discarding them. |
| `scripts/artifact_io.py`; `tests/test_artifact_io.py` | Deterministic CSV bytes, distinct-output and overwrite checks | New private destinations; immutable manifest binding. These helpers alone do not establish provenance or historical acceptance. |
| `acquire_bundesliga_csv.py`, `acquire_second_bundesliga.py`, `collect_belgian_pro_league_{feasibility,history}.py` and acquisition tests | Bounded requests, pinned revisions/blob verification, original/receipt pairs, verified cache replay and access-stop patterns | URLs, permission evidence, source license, headers, pins, limits and coverage. Belgian collectors embed exact file allowlists and preservation chains. |
| `inventory_belgian_pro_league_history.py`, `validate_belgian_pro_league_structure.py`, `verify_belgian_pro_league_inventory.py`; analogous Ligue/Spanish/Portuguese scripts | Physical-record traceability, season/stage matrices, overlap and event accounting, independent raw parsing | Grammar, declared seasons, date windows, club counts, stage/round/group/leg rules, source-specific name correspondences and anomaly thresholds. Belgian counts and misplaced-season exception are not defaults. |
| `verify_belgian_pro_league_review.py`, `decide_belgian_pro_league_policy.py`; corresponding review/policy tests | Evidence-access categories, explicit evidence references, frozen event decisions and four dispositions | Historical facts, finality, actual-play evidence, tier/stage scope and identity boundaries. Reuse the decision contract, never Belgian fixture rules. |
| `standardize_*_results.py`, especially Belgian; standardization/importer tests | Projection of approved INCLUDE events, source/season names, deterministic output and audit reconciliation | League label, mappings and approved population. Regular-pair wrappers from England are unsuitable for split/playoff rematches. Use the shared importer directly when appropriate, retaining its checks. |
| `validate_belgian_pro_league_final.py`; `tests/test_belgian_pro_league_final.py` | Blueprint for stdlib-only raw reconstruction, independent names/IDs/serialization, adverse tests and temporary reproduction | New independently implemented source grammar, baseline and expected season/stage populations. Existing validator is Belgian-specific, not a generic runner. |
| `pyproject.toml`, `tests/`, existing documentation | Existing pytest configuration, focused synthetic tests and final regression suite | Select tests by changed dependencies; do not copy prior pass counts or treat old runs as fresh evidence. |

No generic five-phase runner or league configuration loader is currently supplied by this specification. For the pilot, use a small private, versioned configuration manifest containing competition identity, target seasons/as-of snapshot, source URLs/pins/rights, private paths, grammar, season-format eras, stage/tier eligibility, approved policy version, baseline and exact phase commands. A manifest is declarative input, not executable historical truth. Validate required fields and path containment in any new adapter.

Implement only adapters that the selected competition actually requires, with focused synthetic tests. Reuse shared helpers by import; do not copy whole historical script chains or rewrite completed leagues. Keep independent validation separate from the production parser, mapping tables, ID helpers and serialization. A generic orchestrator, wholesale refactor and new dependencies are unnecessary for a pilot.

## Phase 1 — Source acquisition

**Deliverables:** competition configuration and preservation baseline; scoped source/permission register; immutable originals with URL, publisher, retrieval UTC, response metadata, original filename/encoding, bytes, SHA-256 and pinned revision/blob where available; coverage matrix marking requested, acquired, partial and missing seasons/stages. Include permission/attribution limitations, upstream dependence and any source-repair/quarantine metadata. Show raw counts separately from usable source coverage; do not count overlapping representations as distinct fixtures. Establish access permission before retrieving fixture data; a robots allowance alone is not a reuse license.

**Checks:** exact acquisition allowlist, bounded requests and response/content validation; source/receipt pairing and checksum agreement; no overwrite/path escape; verified offline cache replay makes no request; private destinations are ignored and untracked; protected baseline unchanged. Run only affected collector/provenance tests and shared helper tests if changed.

**Proceed only if:** every acquired original has valid provenance and permitted access, rights limits and gaps are explicit, recovered issues have evidence-bound metadata, unresolved isolated issues are demonstrably quarantined, no systemic blocker remains, preservation/reproduction checks pass and the owner approves Phase 1. A source issue safely corrected or quarantined does not fail the whole phase. Unavailable early seasons need no speculative recovery campaign.

## Phase 2 — Inventory and structural validation

**Deliverables:** one frozen production observation inventory, keyed by source digest and physical line/span or equivalent record locator; season/stage coverage and structural assessment; explicit overlap/event membership reconciliation; targeted anomaly queue; independent structural assessment. Preserve annotations and unscored slots separately from played results.

**Checks:** strict parsing without silent truncation; declared title versus path season; valid dates and season windows, score/auxiliary-field consistency, club/round/stage/group/leg accounting and era-specific expectations. Counts expected from format are diagnostics, not fabricated fixtures. Account for every source representation once; distinguish duplicate representations, distinct rematches, resumptions and actual conflicts. Reconcile overlaps by documented source/season identities, with no city-only or global legal-club merges. Independently parse original bytes and calculate season/stage counts, overlap membership and material exception coverage without importing the production parser or alias resolver. Assert meaningful fixture fields, not merely totals. Run affected parser/structure tests, including malformed and wrong-season inputs.

**Proceed only if:** all records and gaps are accounted for, material parsing/identity conflicts are resolved or explicitly quarantined, the independent assessment agrees, and the owner approves Phase 2. Do not impose a universal double round-robin total or reject legitimate playoff rematches.

## Phase 3 — Historical review and adjudication

**Deliverables:** one private evidence index and decision registry, plus compact season/stage decision totals. Bind each event to its source contributors, evidence, reason, policy version, original/reported values and chosen date/result. Retain separate documentary-only populations.

**Checks:** thoroughly investigate material date/score disagreements, awards, abandonment/resumption, annulments, withdrawals, cancellations, uncertain tiers/stages and club identities. Prefer directly inspected authoritative final decisions; label secondary evidence, inaccessible sources, search-only leads and unresolved finality. Review ordinary fixtures through a documented small deterministic sample across format/source eras and seasons; expand when discrepancies emerge. Sampling is not historical certification of every fixture. Do not manually research every ordinary game. Reuse Phase 2 diagnostics rather than generating another full queue.

Assign exactly one decision per event: **INCLUDE** for supported played, in-scope events with accepted dates/results; **HOLD_OUT** for unresolved, incomplete or insufficiently supported events; **NOT_PLAYED** for evidenced no-play/cancellation entries; **OUT_OF_SCOPE** for events outside the approved competition/tier/stage scope. Unknown play status is HOLD_OUT. Missing seasons remain SOURCE_GAP metadata, never invented NOT_PLAYED fixtures. Verify complete source-to-event-to-decision accounting, evidence references, no unsupported corrections and retrospective-policy consistency. Run affected evidence/policy tests and negative cases.

**Proceed only if:** no material unresolved issue is included, all exclusions/uncertainties and coverage limits are explicit, and the owner approves the frozen registry and Phase 3. New acquisition requires a separately approved return to Phase 1 for a supplementary immutable input, followed by affected downstream checks; never silently alter a frozen input.

## Phase 4 — Standardization and independent validation

**Deliverables:** private canonical CSV, detailed source-to-decision-to-output audit, deterministic manifest and independent reconstruction assessment. Schema, in this exact order:

```csv
match_id,date,league,season,home_team,away_team,home_goals,away_goals,neutral_venue
```

Schema v2 was owner-approved during Champions League Phase 4 on 2026-11-27;
the first eight fields and match-ID definition are unchanged. `neutral_venue`
describes official competition format: 0 conventional home/away, 1 officially
neutral-site, empty when genuinely unknown. It does not describe actual stadium
neutrality or measured home advantage. Preserve first/second orientation and
document season/stage format rules; a single-leg tie or relocation alone does not
establish neutrality. Keep period scores, administrative exceptions and physical
venue evidence in private metadata, following [PROCESS.md](../PROCESS.md) and
[the canonical schema](match-schema.md). Historical v1 outputs/receipts and legacy
inputs remain reproducible; extending another approved dataset requires explicit
owner authorization and zero changes to its pre-existing fields, IDs or ordering.

Use ISO dates, canonical single-year or consecutive `YYYY/YYYY` seasons, approved league label and source-supported season-bound team names. Preserve the existing SHA-256 identity of UTF-8 compact JSON `[league,season,date,home_team,away_team]`; follow existing output ordering and CSV byte conventions explicitly. Never add stage suffixes or change shared identity rules to hide a collision: stop and resolve the identity issue.

**Checks:** output equals exactly the approved INCLUDE population; all other dispositions remain audit-only. Validate integers, dates, names, unique IDs, cross-competition collisions, source traceability and per-season/stage counts. Confirm legitimate rematches remain separate and name mappings are consistent/injective within source/season.

The independent validator reads original bytes and frozen approved event membership/decisions, independently reconstructs names, dates, results, IDs, ordering and serialization, and compares every field and full CSV bytes/SHA-256. It must not import production content/parsing/naming/ID/serialization helpers or use the production inventory as its raw truth. Sharing the approved policy and event membership is allowed; independently verify every bound contributor and decision projection. Cross-source historical corroboration and code independence are separate claims: disclose common upstreams and missing external corroboration.

Reproduce production artifacts and the independently reconstructed CSV in separate processes and fresh temporary directories; compare deterministic bytes/hashes without overwriting approved outputs. Keep run-specific metadata outside deterministic content; retain immutable source-provenance and evidence timestamps. Run focused standardization/importer/independent-validator tests, including incorrect IDs, missing/extra rows, changed source bytes, alias collisions and valid rematches. Reuse Phase 2 independent parsing implementation, pinned to original hashes, without weakening its separation from production.

**Proceed only if:** exact independent reconciliation and reproducibility pass, required protected fingerprints match, privacy checks pass, limitations are reported, and the owner approves Phase 4. A rerun of the production standardizer alone is not independent validation.

## Phase 5 — Finalization

**Deliverables before publication:** concise public methods/coverage/limitations and test summary; private final preservation and validation receipt; exact public path allowlist, reviewed diff and proposed commit message/branch/remote. Append project decisions to `PLANNING_LOG.md`, preserving its earlier bytes.

**Checks:** run the complete repository suite once with the unchanged approved environment (`<approved-python> -B -m pytest`), after final code changes and before publication. Record command, interpreter, exit status and passed/failed/skipped counts; explain skips. Recheck independent reproduction if its inputs or code changed after Phase 4. Verify preservation scope, HEAD/index and unrelated dirty files, private ignore/untracked status, public diff and license/training disclosures. Inspect allowlisted files for embedded raw records, detailed private audits, credentials and restrictive source content; ignore rules alone do not prove privacy.

**Publication gate:** present the short report and exact staging/commit/push plan; stop for explicit owner authorization. Only then stage named public paths individually (`git add -- <approved-paths>`), never `git add .` or private/force-added artifacts. Inspect the actual staged diff, run `git diff --cached --check`, verify staged names equal the approved list and repeat staged-content privacy review. If approval scope or content changes, stop for renewed approval. Commit normally, push only to the approved branch/remote, and verify the resulting commit/upstream identity. No merge, rebase, force push or automatic next competition.

**Completion criterion:** authorized public commit/push verified, all checks pass, protected data unchanged and final report delivered. If publication is not authorized, report “publication pending,” preserve the unstaged result and stop. After Phase 5, require explicit approval before selecting or starting another competition. For preparation of this specification itself: no staging, commit, push or full-suite run.

## Efficient execution and verification

Produce one authoritative artifact per purpose, referenced by hash across phases; do not duplicate full inventories/reports for each check. Production parsing runs once per frozen input/parser revision, with a hash-keyed private cache if useful. Independent parsing remains a separate necessary pass. Invalidate caches on source, parser or configuration changes. New process byte reproduction remains mandatory in Phase 4; it is purposeful verification, not redundant reporting.

At each phase, run focused tests for changed behavior/dependencies; reserve the complete suite for Phase 5. Repeat it only after a relevant change/failure or unresolved concern. Reuse a still-valid final run for the same tested code tree; never claim a stale run covers new code. Use bounded diagnostics for slow filesystem reads, with exact fresh-versus-cached scope; do not repeatedly hash every installed package or claim uncompleted scans passed. Required protected-data checks remain mandatory. No parallel competitions.

Privately record phase/attempt IDs, approval requests/receipts, commands, interpreter, input/config/code digests, outcomes and cache status. Preserve failed-attempt evidence and access-stop records. Execution-time measurement and reporting, separate timing ledgers and execution-speed comparisons are not required.

Preserve timestamps needed for source provenance, acquisition receipts, historical evidence and audit traceability, including approval records. These are distinct from execution-duration measurements. Previously recorded timing information in completed reports and historical logs must remain unchanged. All data-quality, nine-phase output-equivalence, independent-validation, reproducibility, testing, preservation, privacy, licensing and phase/publication approval requirements remain in force.

## One-report template

```text
Competition / phase / attempt / status (PASS, BLOCKED, publication pending):
Scope and frozen input/config/code hashes; private deliverable references:
Coverage and accounting (representations/events/decisions/output; gaps):
Checks: exact commands, exit status, results; independent method and limits:
Preservation/privacy/rights findings; failures or unresolved risks:
Decision requested: approve Phase N and authorize Phase N+1 only
(or Phase 5 exact public paths + commit/push plan; then STOP).
```

## Reusable Codex prompt

```text
Follow docs/accelerated-five-phase-workflow.md and AGENTS.md for [competition].
Authorize Phase [N] ONLY. Prior approved report/manifest: [reference, or none
for Phase 1]. Target seasons/snapshot: [scope]. Approved interpreter: [path].
Use a new competition-private scope; reuse tested shared utilities and add only
necessary adapters. Preserve all 13 completed competitions and the application,
environment and history. Retain retrospective original football dates/accepted
final results, independent raw reconstruction, documented gaps and all rights
restrictions. Repair recoverable source issues only in evidence-bound derived
metadata; quarantine isolated unresolved representations and continue with
reduced coverage. Do not fabricate or include unresolved results. Stop for
systemic/uncontained integrity, provenance or privacy failure. Run focused checks; run the
full suite only for final publication as specified. Append decisions to the
planning log. Preserve provenance and evidence timestamps. Deliver one short phase report and
STOP for explicit approval; do not advance or start another competition.
No staging/commit/push unless separately authorized against an exact public
allowlist after the Phase 5 report.
```

## Pilot readiness

The workflow specification is ready for owner review and a gated pilot. Shared import/serialization utilities are reusable immediately; acquisition, structure, evidence and independent-validation patterns are established by existing scripts/tests. A selected competition still needs a scoped manifest, source permission/coverage assessment and any minimal production and independent-parser adapters. No generic automation has been implemented or validated by this documentation change. Readiness means Phase 1 can begin after explicit approval and competition selection, not that all 16 competitions can run unattended. No next competition has been processed.
