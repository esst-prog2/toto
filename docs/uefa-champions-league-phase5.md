# UEFA Champions League — Phase 5 finalization and pre-publication review

**Verification PASS; publication pending explicit approval of the exact scope.**
Phase 4 and the subsequent targeted README cleanup are owner-approved. This gate
was performed on 2026-11-27 exclusively in the original `toto` worktree on
`feature/data-collection`, HEAD `878d45e47f1ef861b1b774ecc89c94af7851cb34`.
No staging, commit, push, merge, rebase, new acquisition, historical adjudication,
approved-dataset change, other-worktree access, application integration, training,
backtesting or next competition is authorized or performed.

## Baseline and protected scope

A fresh baseline records **2,677 protected-file SHA-256 fingerprints**, worktree,
branch/HEAD/index/configuration, existing dirty/untracked paths, original environment
configuration, restored README and planning prefix. Private records remain under
`data/private/europe/champions_league/phase5/`. The interpreter is the unchanged,
previously approved external CPython 3.13.12 environment; no package installation,
upgrade or environment rebuilding occurred. Git objects, caches, installed package
bytes and unrelated external worktrees are outside exhaustive hashing; no claim
of full installed-package-byte certification is made.

README remains byte-identical to its verified pre-Phase 4 copy and HEAD. Its old
Phase 4 publication-review fingerprint is intentionally superseded by the separately
approved cleanup; frozen Phase 4 receipts themselves are not rewritten. The only
other subsequent differences from old public review hashes are append-only planning
entries. Frozen data, decisions, transformations and output hashes remain unchanged.

## Final population and historical decisions

| Verified population | Count |
|---|---:|
| Unique standardized INCLUDE matches | 6,642 |
| Main / qualifying played matches | 4,127 / 2,515 |
| Completed target seasons, 1992/93–2025/26 | 34 |
| Recovered qualifying descriptions | 692 |
| Recovered played / no-kickoff descriptions | 690 / 2 |
| HOLD OUT | 0 |
| NOT PLAYED | 3 |
| Additional nonstanding OUT OF SCOPE attempts | 3 |
| Standing source-supported event descriptions | 6,645 |
| All reviewed events, including nonstanding contexts | 6,648 |
| In-scope fixture source observations | 12,211 |
| Incorrect numeric regulation-score repairs | 8 |
| Separately resolved unknown regulation periods | 3 |
| Original football-date repairs | 4 |
| Explicit played administrative-result exceptions | 8 |

All values reconcile to the accepted [Phase 3](uefa-champions-league-phase3.md) and
[Phase 4](uefa-champions-league-phase4.md) registries. Original source observations,
first/second orientation, team labels with approved historical overrides, match IDs,
dates, historical results and dispositions have not changed. Corrections remain
bound to raw identity, source SHA-256, original locator and approved evidence.
Excluded events have no canonical played-match row and remain fully audit-only.
No missing fixture was fabricated or recast as NOT PLAYED.

The 76 immutable source/metadata payloads total **3,323,273 bytes** and all match
URL/time/status/byte/hash receipts. The 41 earlier fixture files remain frozen;
supplemental revision/Curley inputs and metadata are referenced in place. Curley's
complete original contains 6,556 rows: 4,401 in the target source population and
2,155 outside target years. The latter are excluded by the acquisition/inventory
scope, not confused with the three separately researched OUT OF SCOPE attempts.

Canonical CSV: `phase4/validated/uefa_champions_league_standardized_1992_2026.csv`,
**939,615 bytes**, SHA-256:

```text
58c4b0453ba7176e34179e70004c443c41fcf97bc97606de5506ad2ef90db827
```

The deterministic phase/manifest chain verifies all **60 Phase 3 input entries,
22 Phase 3 artifacts, 16 Phase 4 input entries and 26 Phase 4 artifacts**. The
[Phase 4 report](uefa-champions-league-phase4.md) and private
`phase4/validated/season_coverage.json` preserve the complete 34-season matrix;
`season_stage_neutrality.json` covers 284 included season/scope/stage groups.
No remaining standing target fixture gap was identified in accepted research,
subject to source-lineage/historical-certification limits. European Cup 1990/91–1991/92
and 2026/27 remain outside scope. Existing domestic gaps/exclusions remain unchanged.

Eight accepted administrative scores remain explicit retrospective exceptions,
separate from observed regulation scores; two abandoned played fixtures have no
invented completed 90-minute result. No administrative-publication-date filter was
introduced. The 147 event-level after-extra-time and 66 shootout observations,
source aggregates, 33 aggregate differences, auxiliary-date quarantine, source
period ambiguities and original/completion-date distinctions remain private and
unchanged. A shootout or aggregate winner never substitutes for the Toto outcome.
This is not a leakage-free forecasting or training-eligibility claim.

## Equivalence to the original nine-phase workflow

Actual Primeira Liga acquisition/inventory/structural/evidence/policy/standardization
artifacts were inspected, including its complete 11,406-observation / 9,264-fixture
archive, retained evidence and manifest outputs. Its frozen eight-column CSV is
verified through the exact v1 backup retained by the approved domestic schema
migration; its nine-phase archive and receipts were not modified. The Turkish
accelerated reference was also inspected: 13,894 source observations, 10,574 event
records/decisions, 10,540 canonical rows and its independent/reproduction receipts.

**All 18 required output guarantees are equivalent; none is missing or incomplete.**
Equivalent means preserved coverage/accounting, raw traceability, evidence/decision
binding, independent validation and reproducibility under the approved policy. It
does not require matching filenames, file counts, research-reference counts, or
copying another competition's historical decisions. UCL's linked inventories,
registry, sidecar and exclusion records form a complete audit archive without
creating a redundant monolithic copy. Independent code does not establish disjoint
historical upstreams or primary certification of every ordinary fixture.

Path abbreviations: **PT/** = `data/private/portugal/primeira_liga/`;
**U/** = `data/private/europe/champions_league/`;
**TR/** = `data/private/turkey/super_lig/`. Exact Turkish counterpart references
and machine-readable verification statements are in private `phase5/output_equivalence.json`.

| Required output | Nine-phase reference artifact | Champions League equivalent | Verification performed | Status | Remaining action |
|---|---|---|---|---|---|
| Immutable original sources | `PT/jalapic/engsoccerdata/data-raw/portugal.csv`<br>`PT/openfootball/europe/portugal/2025-26_pt1.txt` | `U/phase2/acquisition_manifest.json`<br>`U/phase3/acquisition_manifest.final.json`<br>`U/phase1_research/metadata_receipt_index.json` | Fresh SHA256/byte/receipt checks for all76 UCL payloads; no network/new acquisition. Nine-phase originals and frozen v1 CSV references checked; approved v2 backup mapping explicit. | equivalent | None |
| Acquisition receipts and provenance | `PT/phase3_acquisition.json`<br>`PT/acquisition.json` | `U/phase5/frozen_inputs_and_provenance.json`<br>`U/phase2/acquisition_manifest.json`<br>`U/phase3/acquisition_manifest.final.json` | All76 immutable payloads bind exact receipt URL/time/status/size/hash; revision/blob and source grants checked by independent original readers. | equivalent | None |
| Source and permission register | `PT/acquisition.json`<br>`PT/primeira_liga_standardization_manifest.json` | `U/phase1_research/research_register.json`<br>`U/phase2/permission_holds.json`<br>`U/phase3/permission_holds.final.json`<br>`U/phase3/rsssf_permission_research.json` | Retained source-specific attribution/use/access-stop limits; metadata/raw-original distinctions and unknown upstream lineage explicit; no training/redistribution clearance inferred. | equivalent | None |
| Production observation inventory | `PT/phase3_historical_inventory.json`<br>`PT/phase3_modern_inventory.json` | `U/phase2/validated/source_inventory.json`<br>`U/phase3/final/supplemental_source_inventory.json` | Fresh independent reconstruction verifies6578base+5633supplemental=12211target observations, raw fields/periods/physical or decoded locators and one event membership each; Curley2155off-target rows separately accounted. | equivalent | None |
| Season/stage coverage matrices | `PT/phase3_coverage_matrix.json`<br>`PT/phase4_modern_structure.json`<br>`PT/phase4_coverage_gap.json` | `U/phase2/validated/structural_validation.json`<br>`U/phase3/final/coverage_assessment.json`<br>`U/phase4/validated/season_coverage.json`<br>`U/phase4/validated/season_stage_neutrality.json` | Recount34seasons/284included season-scope-stage groups;4127main/2515qualifying;no fabricated gaps/no-play entries; legacy era/dual-group/league/COVID formats retained. | equivalent | None |
| Independent structural assessment | `PT/phase3_independent_reconciliation.json`<br>`PT/phase4_integrity_manifest.json` | `U/phase2/independent_validation.final.json`<br>`U/phase5/independent_history.json` | Fresh independent raw readers recheck source/stage membership,33separate-publisher season counts,4941supplemental overlap links,129extra-time tie gates and1663aggregate checks; parser independence distinct from upstream independence. | equivalent | None |
| Historical evidence index | `PT/phase5_documentary_evidence_index.json`<br>`PT/phase5_review_registry.json`<br>`PT/phase5_sample_assessment.json` | `U/phase3/adjudication_evidence.json`<br>`U/phase3/historical_coverage_evidence.json`<br>`U/phase3/final/review_resolution.json`<br>`U/phase4/format_evidence.supplement.json` | Existing targeted factual evidence and36source-bound rules inspected; ordinary fixtures retain explicit source/period basis and complete structural/original-field checks; research depth/status differs by risk, not file count. No new historical research or certification claim. | equivalent | None |
| Frozen event decision registry | `PT/phase6_unique_fixture_policy.json` | `U/phase3/final/decision_registry.json`<br>`U/phase4/approval.json` | All6645standing descriptions plus3nonstanding contexts retain frozen IDs/decisions;6642INCLUDE/0HOLD/3NOTPLAYED/3OOS reconcile; source-bound changes independently reapplied without new decisions. | equivalent | None |
| Standardized canonical CSV | `PT/primeira_liga_standardization_manifest.json` | `U/phase4/validated/uefa_champions_league_standardized_1992_2026.csv`<br>`U/phase4/validated/summary.json` | Exactly6642unique deterministic IDs; everyfield/order andCSVbyte independently rebuilt. Approved schema-v2 ninth metadata column is a documented project-wide extension, not reduced v1 guarantees; original domestic fields unchanged. | equivalent | None |
| Complete source-decision-output audit | `PT/primeira_liga_audit_archive_1994_2026.json` | `U/phase2/validated/source_inventory.json`<br>`U/phase3/final/supplemental_source_inventory.json`<br>`U/phase3/final/decision_registry.json`<br>`U/phase4/validated/source_to_output.json`<br>`U/phase4/validated/excluded_events.json` | Functionally complete linked archive: all raw observations remain in inventories; frozen decisions own every observation;6642output links include sources/hashes/locators/decisions/periods;all exclusions remain traceable audit-only. No redundant monolithic archive created. | equivalent | None |
| Exception/correction/exclusion registry | `PT/primeira_liga_exceptions_1994_2026.json`<br>`PT/phase6_exception_registry.json` | `U/phase3/adjudication_evidence.json`<br>`U/phase3/final/discrepancy_registry.json`<br>`U/phase3/final/aggregate_discrepancies.json`<br>`U/phase4/validated/excluded_events.json` | Reconcile8numeric regulation repairs/3unknown-period recoveries/4date repairs/8played admin exceptions;3NP/3OOSexcluded;auxiliary-date quarantine and33aggregate differences retained separately. | equivalent | None |
| Deterministic manifests | `PT/primeira_liga_standardization_manifest.json` | `U/phase3/input_freeze.final.json`<br>`U/phase3/artifact_manifest.final.json`<br>`U/phase4/input_freeze.final.json`<br>`U/phase4/artifact_manifest.final.json` | Fresh verification of60+22+16+26manifest entries; raw/output/code hashes unchanged. Prior publication-review README/log hashes handled as owner-approved subsequent documentation changes, not rewritten frozen receipts. | equivalent | None |
| Reproducible acquisition/transformation scripts | `scripts/collect_primeira_liga_feasibility.py`<br>`scripts/collect_primeira_liga_history.py`<br>`scripts/standardize_primeira_liga_results.py` | `scripts/acquire_uefa_champions_league.py`<br>`scripts/inventory_uefa_champions_league.py`<br>`scripts/review_uefa_champions_league_history.py`<br>`scripts/standardize_uefa_champions_league.py`<br>`U/phase3/acquire_wikipedia_pages.py`<br>`U/phase3/acquire_curley_alternative.py` | Pinned sources/bounded plans/immutable cache and private supplemental acquisition harnesses retained. AST inspected, no acquisition executed. Fresh transformation reproduces6UCL+16domestic artifacts; future network acquisition remains subject to existing stops/permission. | equivalent | None |
| Independent reconstruction/validation tooling | `scripts/verify_primeira_liga_inventory.py`<br>`scripts/validate_primeira_liga_structure.py`<br>`scripts/standardize_primeira_liga_results.py` | `scripts/verify_uefa_champions_league_inventory.py`<br>`scripts/verify_uefa_champions_league_history.py`<br>`scripts/verify_uefa_champions_league_standardization.py` | Separate original parsers/identity/format/serialization path imports no new production transforms; every UCLfield/ID/CSVbyte reconstructed; final independent report byte-identical to Phase4 in fresh network-disabled process. | equivalent | None |
| Automated tests | `tests/test_primeira_liga_feasibility.py`<br>`tests/test_primeira_liga_structure.py`<br>`tests/test_primeira_liga_history.py`<br>`tests/test_primeira_liga_policy.py`<br>`tests/test_primeira_liga_standardization.py` | `tests/test_uefa_champions_league_acquisition.py`<br>`tests/test_uefa_champions_league_inventory.py`<br>`tests/test_uefa_champions_league_history.py`<br>`tests/test_uefa_champions_league_standardization.py`<br>`tests/test_match_schema_v2.py` | Fresh complete-suite2822tests+27subtests; no failures/errors/skips; source-period annotation, all repair shapes, format neutrality, migration/legacy/synthetic behavior regressions included; exact final code-tree hashes bound. | equivalent | None |
| Public methods/coverage/limits documentation | `docs/primeira-liga-inventory.md`<br>`docs/primeira-liga-historical-review.md`<br>`docs/primeira-liga-policy.md`<br>`docs/primeira-liga-standardization.md` | `PROCESS.md`<br>`docs/match-schema.md`<br>`docs/domestic-score-period-audit.md`<br>`docs/uefa-champions-league-phase1.md`<br>`docs/uefa-champions-league-phase2.md`<br>`docs/uefa-champions-league-phase3.md`<br>`docs/uefa-champions-league-phase4.md` | Accepted phase reports cover inputs/formats/decisions/coverage/periods/rights; final Phase5report adds this explicit equivalence map and publication gate. Current workflow schema clause aligned with owner-approved v2; restored README unchanged. | equivalent | None |
| Private preservation/validation receipts | `PT/phase7_independent_regeneration.json`<br>`PT/phase7_final_verification.json` | `U/phase4/preservation.json`<br>`U/phase4/independent_validation.json`<br>`U/phase4/offline_generation.json`<br>`U/phase5/protected_before.json`<br>`U/phase5/complete_tests.json`<br>`U/phase5/reproducibility.json` | Fresh2677-file baseline, unchanged originals/code/data/README/index/environment; private full receipts retained. New phase5 final preservation/privacy receipts supplement, not replace, existing phase4 receipts. | equivalent | None |
| Append-only planning documentation | `PLANNING_LOG.md` | `PLANNING_LOG.md`<br>`U/phase5/planning_log.before.txt` | Original planning bytes retained as exact prefix; only factual owner/assistant decisions appended. All earlier competition histories remain untouched. | equivalent | None |
| Legacy forecast-availability/model-training gate | `PT/phase6_chronology_registry.json` | `PROCESS.md`<br>`U/phase3/permission_holds.final.json` | Not a missing historical output. Portuguese availability/finality policy is not imposed on the explicitly approved retrospective original-football-date/accepted-admin-result policy. No UCL integration/training or forecasting-performance claim is authorized. | not applicable | None |

The additional legacy forecast-availability row is not applicable to this historical
workstream: the owner-approved retrospective original-football-date/accepted-result
policy supersedes imposing Portuguese completion/publication/finality filters.
Training/use permission and future model integration remain separately gated.

A further conservative collision assessment checked 17 prior CSVs (including the
separate Serie B audit CSV) and seven JSON audit archives. It reserves only explicit
match/screened/source-match/candidate-match ID fields, not generic event/decision
hashes: **168,881 CSV row instances, 156,584 CSV IDs plus 4,107 additional audit-only
IDs = 160,691 protected unique IDs**. All 6,642 UCL IDs have **zero collisions**.

## Schema v2, domestic migration and compatibility

Current canonical schema, in order:

```csv
match_id,date,league,season,home_team,away_team,home_goals,away_goals,neutral_venue
```

The appended variable describes **official competition format**, not actual stadium
neutrality or realized home advantage. UCL is **6,584 zeros / 58 ones / zero NA**:
34 official finals, 17 played centralized preliminary matches, six Lisbon 2020
quarterfinals/semifinals and one specially ordered neutral replay. Single-leg
hosted matches and ordinary relocations stay 0; an official final remains 1 at a
participant's usual stadium. All season/stage expectations reconcile independently.
Physical-venue evidence stays distinct, and prior Phase 3 physical classifications
remain frozen rather than silently reinterpreted. First-listed goals and 1/X/2
orientation are unchanged; future venue-specific model changes remain deferred.

All **14 domestic competitions / 16 current CSVs / 156,579 rows** retain the approved
v2 extension, all neutrality 0. Reproduction and independent comparisons again
confirm **1,252,632 unchanged old fields, zero changed old fields, zero changed IDs
and zero reordered rows**. Removing the ninth column reproduces every original
v1 CSV byte-for-byte. The 258 ongoing English snapshot rows were not refreshed;
the 12,302-row Serie B audit archive and all raw/unstandardized data remain unchanged.
The accepted [domestic score-period audit](domestic-score-period-audit.md) remains
valid with its original limitations.

[PROCESS.md](../PROCESS.md), [schema documentation](match-schema.md) and
[importer documentation](historical-import.md) retain neutral-value serialization,
nullable Int8 loading, stable compact-JSON SHA-256 IDs, explicit v2 import support
and frozen v1 adapter/six/eight-column synthetic compatibility. The workflow's
schema/tool reference was minimally aligned with this already approved v2 decision;
phase gates and historical policies were not changed. README was not edited.
No prediction/statistical/feature code changed. Compatibility and synthetic-demo
prediction-equivalence regressions pass in the complete suite.

## Fresh verification versus reused evidence

Phase 4 input/code/output hashes were freshly checked against frozen manifests.
Existing approved historical judgments, permission records and earlier research are
reused as immutable inputs, not newly re-adjudicated or presented as fresh research.

Phase 5 performed a **fresh network-disabled independent original-source historical
and output reconstruction**. It imports no new production parsing/ID/format/CSV
helpers. It checks every output field/ID/order/byte, all original observation
memberships, source locators, decisions, exclusions, repairs, stage/neutrality counts
and domestic before/after values. The independent report matches Phase 4 byte-for-byte.
Independent historical gates freshly confirm 4,941 supplemental overlaps, 129
extra-time regulation tie gates, 33 separately published qualifying-season counts
and 1,663 aggregate checks. Historical upstream independence remains unestablished.

Six UCL artifacts and 16 domestic CSVs were freshly regenerated in separate fresh
private destinations with network connections/DNS forbidden: **all 22 artifacts
match approved bytes/SHA-256**. Approved originals and datasets were not overwritten.
This purposeful check corroborates, rather than replaces, existing Phase 4 receipts.

## Complete repository suite

**2,822 tests and 27 subtests passed; zero failures, errors or skips.** This is a
fresh, complete Phase 5 run with no test-selection exclusions. CPython **3.13.12**,
pytest **9.1.1**, unchanged approved external interpreter:

```sh
PYTHONPATH=src:. PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /private/tmp/belgium-phase4-env-xgpvyf0n/venv/bin/python -B -m pytest -q -p no:cacheprovider
```

Exit status **0**; pytest duration **20.54 seconds**, measured subprocess wall
**21.089 seconds**. Only documentation/planning changed after this run; exact tested
code-tree fingerprints remain unchanged. No environment was installed, rebuilt or
updated. The previous Phase 4 pass is retained as historical evidence, not counted
as another fresh run. One complete suite was run for this finalization gate.

## Privacy and preservation review

All 2,677 pre-phase fingerprints are compared freshly. Only the declared current
workflow-documentation alignment and append-only planning entries may differ;
all historical data, source/evidence/decision inventories, approved outputs, prior
competition artifacts, application files, restored README, unrelated dirty work,
HEAD/index/configuration and environment references must match. No other worktree
was accessed. Existing `.DS_Store` files remain outside publication scope.

Every proposed public path is reviewed as UTF-8 text by role, with syntax/whitespace,
credential, original-source-fragment and private fixture/observation-ID checks.
Scripts implement acquisition/validation/projection; tests use synthetic fixtures;
documents contain methods, aggregate coverage and limitations; planning is append-only.
Any intentionally synthetic security/example tokens are distinguished from secrets.
No raw/standardized dataset, receipt, evidence snapshot, detailed inventory/decision
registry, generated cache or environment is a publication candidate. All private
files are ignored and none tracked; ignore rules alone are not the content audit.
The exact reviewed patch and full 27-path SHA-256 register remain private.

Existing CC0-rights-held/third-party limitations, Wikipedia revision attribution
and applicable share-alike obligations, Curley noncommercial attribution, RSSSF
factual-note/copy distinctions, unknown upstream lineage and all access stops remain
in force. UEFA harvesting and denied-source retries remain excluded. The approved
private real-data/synthetic-only-public deployment strategy is unchanged. Technical
validation or publication of code establishes no training, commercial or historical
data redistribution clearance.

## Exact proposed publication scope

**27 public paths**, excluding README, both `.DS_Store` files, every private source,
dataset, receipt, evidence/audit artifact, environment, cache and temporary driver.
The domestic audit summary/PROCESS changes are approved UCL methodology prerequisites;
shared changes implement only the approved schema-v2 compatibility extension.

```text
PLANNING_LOG.md
PROCESS.md
docs/accelerated-five-phase-workflow.md
docs/domestic-score-period-audit.md
docs/historical-import.md
docs/match-schema.md
docs/uefa-champions-league-phase1.md
docs/uefa-champions-league-phase2.md
docs/uefa-champions-league-phase3.md
docs/uefa-champions-league-phase4.md
docs/uefa-champions-league-phase5.md
scripts/acquire_uefa_champions_league.py
scripts/extend_domestic_neutrality.py
scripts/inventory_uefa_champions_league.py
scripts/review_uefa_champions_league_history.py
scripts/standardize_uefa_champions_league.py
scripts/verify_uefa_champions_league_history.py
scripts/verify_uefa_champions_league_inventory.py
scripts/verify_uefa_champions_league_standardization.py
src/toto_estimator/data.py
src/toto_estimator/historical_import.py
src/toto_estimator/match_schema.py
tests/test_match_schema_v2.py
tests/test_uefa_champions_league_acquisition.py
tests/test_uefa_champions_league_history.py
tests/test_uefa_champions_league_inventory.py
tests/test_uefa_champions_league_standardization.py
```

Public-file SHA-256 values below bind the final reviewed bytes of the other 26 paths. This report's own final hash is recorded out of
band in private `phase5/publication_scope.json` to avoid circular self-hashing.
That register binds all 27 files, the reviewed patch/hash, diff statistics and plan.

| Public file | SHA-256 |
|---|---|
| `PLANNING_LOG.md` | `12ba0c8f972ab96e50418313d0b28f80dc063457ed6f366429103ff7e20169d9` |
| `PROCESS.md` | `bd3f40cdf07fe9f3d2261900ac21f5dbf6088f34ce73dbce9027d3131e13f80d` |
| `docs/accelerated-five-phase-workflow.md` | `b532df08ecee787c72359f371119142656d1e8eb8e8da1a86f02bb6cefc160e0` |
| `docs/domestic-score-period-audit.md` | `acae40bc0287e945f9a1980ed1a99fc04b97231958072a3ec711599b783ab17f` |
| `docs/historical-import.md` | `be26939d245eea7bb41dd66074233f4de7a1daa787f0f795b3fc386fb460cd76` |
| `docs/match-schema.md` | `3ec12bd1a82a0c1e7ed9789408cb8c137def271665f83d035565faa891c0330d` |
| `docs/uefa-champions-league-phase1.md` | `0e8885270fc940664091ad941323e44b44acd24c95e82cefdc012d5afa1d7531` |
| `docs/uefa-champions-league-phase2.md` | `544106951a9aaf2d2d25154beedee1c5cbc067f994417a40c84f8ee0c9ba14d7` |
| `docs/uefa-champions-league-phase3.md` | `64f0f84fb3e1111a52d9ef281002f13935d3b162701dbffb5030d7c34ccca052` |
| `docs/uefa-champions-league-phase4.md` | `beb1d2e7febec0427baa8b666a03c782227a96d504bcada080db5bd0ae923d22` |
| `scripts/acquire_uefa_champions_league.py` | `5adcdd85c66b92ac9f124bfc9e64ecfd84fa317757b1a95332d6f9eba016ccec` |
| `scripts/extend_domestic_neutrality.py` | `c4fd23daae64a02d9724eb0d1a01fd5355fe6d3920bb18ac0fbe209439a2c0b2` |
| `scripts/inventory_uefa_champions_league.py` | `6cebe5e2b978ad5b068f7945c38ed8637b6aaae6669d61c5b9302880db0f8d97` |
| `scripts/review_uefa_champions_league_history.py` | `7a2adcddd3bbe1e6525307fbdd47b805b91bc024bc80e8c6099caa3204672b64` |
| `scripts/standardize_uefa_champions_league.py` | `cce40393abdba9a126645b30ed5152918e201f26b394a8309e7ad19a1a8682b3` |
| `scripts/verify_uefa_champions_league_history.py` | `d330af91976f26c1536e9f7e27810490b3a0cca9b820d09deb89034dd0834f50` |
| `scripts/verify_uefa_champions_league_inventory.py` | `dafef7c987457990fcd77e2b301e306f41673aaa66d1ae452a84944f41db3430` |
| `scripts/verify_uefa_champions_league_standardization.py` | `801b4597b67751719d9c57a0610ce6bf831d686774c0c7b0488e8f0706755697` |
| `src/toto_estimator/data.py` | `28db55b39df5b883992fe9cad9cea61ffc587db1048c209af5fb45a8fa219b1a` |
| `src/toto_estimator/historical_import.py` | `3fa39c1163eadec9eba95316e253820fdab967340c5deac380432b74cddab051` |
| `src/toto_estimator/match_schema.py` | `012e0b2bd994d10929574be80320783dbb9ca060b230f0ecbd1da6c416bfb565` |
| `tests/test_match_schema_v2.py` | `c82c513098bd3041e5224c2825bdc9c5ac1cb357bfe96646247e49959bff8a03` |
| `tests/test_uefa_champions_league_acquisition.py` | `de3dc468cf0262f0055734142609fc6171b5ee7eac204adba5b91c579d498537` |
| `tests/test_uefa_champions_league_history.py` | `53dcb26d43902779732947a3740fe00057ccae098997f316f9115f8e8666be56` |
| `tests/test_uefa_champions_league_inventory.py` | `186f66dcef370f2c210047227c921732ac9b20c7769681aee0ed26273db7fd17` |
| `tests/test_uefa_champions_league_standardization.py` | `2ab3586c0af4545b8367ce5da49a7bb5287d1897adaf5fccc8d6b92511060117` |

Reviewed diff summary: five previously tracked public files plus 22 new public
files. Existing shared code changes are the minimal loader/importer support;
no prediction/model algorithm, feature, sample dataset or README change is included.
Phase 5 itself adds this report, appends the planning log and aligns the workflow's
schema clause/tool row; it changes no code, dataset or historical decision.

Proposed commit subject:

```text
Add audited UEFA Champions League workflow and schema v2
```

Current/proposed branch: **`feature/data-collection`**. Current HEAD:
`878d45e47f1ef861b1b774ecc89c94af7851cb34`. Intended remote: **`origin`**, configured
push URL **`https://github.com/esst-prog2/toto.git`**. Destination:
**`refs/heads/feature/data-collection`**. Exact proposed normal push:

```sh
git push origin HEAD:refs/heads/feature/data-collection
```

After separate explicit approval, recheck these exact public hashes, protected
inputs/data/README, branch/HEAD/index and intended remote tip. Stage only the 27
named paths individually with `git add -- <approved-path>`; compare staged names
to the approved list, inspect the actual staged diff and rerun its privacy and
`git diff --cached --check` checks. Commit normally with the reviewed subject,
then execute only the push above and verify local/remote commit identity. Stop
for renewed review if scope/content changes. No force, merge, rebase or other branch.
No remote write or remote-tip network query was performed at this review gate;
the configured destination was checked locally.

The [authoritative workflow](accelerated-five-phase-workflow.md) requires
“present the short report and exact staging/commit/push plan; stop for explicit
owner authorization.” This review provides that concrete plan; it grants no
publication permission.

## Measured timing and stopping point

Measured **active wall: 1273.234 seconds (21 min 13 sec)**;
**owner-approval wait: 0 seconds**; **total elapsed: 1273.201 seconds**.
Recorded interval: `2026-11-27T00:55:09.450162+00:00` to `2026-11-27T01:16:22.651272+00:00`.
This continuous task session includes the interrupted/continued instruction delivery,
analysis, documentation, file/tool waits, audits, tests and reproduction. Work
continued while the remaining instruction text arrived; no blocked approval wait
was counted. The 21.089-second complete-suite command and
21.938-second fresh reproduction/independent command are included, not added again.
File-provider/tool wait components were not separately instrumented and are not
estimated. Source-network acquisition requests: zero. Receipt emission/final chat
and future approval/publication work are outside this checkpoint. The append-only
private timing ledger and `timing_final.json` retain exact measurement scope.

**Verification PASS; publication pending explicit approval of the exact scope.**
Stop here. No staged files, commit, push, another competition or model work.

## Approved timing-policy amendment and publication refresh

The owner accepted the preceding Phase 5 verification and approved removal of
mandatory execution-time measurement and reporting. This addendum preserves the
entire accepted report, including its historical timing information, as an exact
prefix. Its earlier hash table and scope pointers describe the accepted original
gate; the refreshed publication register below supersedes those pointers for the
current publication proposal only.

The accelerated workflow no longer requires session, approval-wait, calendar,
command/test or network/file-wait measurements, separate timing ledgers, failed-
attempt timing or execution-speed comparisons. Its phase requirements, report
template and reusable prompt were updated. Provenance, acquisition, historical-
evidence and audit-traceability timestamps remain required. Previously recorded
measurements in completed reports and logs are unchanged.

Only `docs/accelerated-five-phase-workflow.md`, this appended addendum and the
append-only `PLANNING_LOG.md` changed. PROCESS.md was inspected and contains no
execution-timing requirement; its score-period and recent-first completeness
policies remain unchanged. README, datasets/originals, historical decisions/evidence,
canonical schema, application/prediction/model code, tests and dependencies were
not modified. All data-quality, nine-phase output-equivalence, independent-validation,
reproduction, testing, preservation, privacy/licensing and phase/publication approval
requirements remain intact.

The accepted 18-output equivalence assessment, complete suite (2,822 tests and
27 subtests), independent original-source reconstruction and 22 byte-identical
reproduced artifacts remain valid. Their immutable receipt and manifest bindings
were checked; no relevant code or data input was changed by this documentation-only
amendment. These are reused accepted results, not newly rerun tests/reconstruction.
Fresh checks cover the public bytes, changed documentation, tested publication-code
hashes, frozen verification bindings, restored README and Git HEAD/index/configuration.
The accepted broader preservation receipt is retained. Optional wider filesystem
reads were interrupted while blocked; no new exhaustive worktree/archive/environment
rescan is claimed and those incomplete reads are not treated as successful checks.

The exact public allowlist remains the same 27 paths listed above. Three files
have refreshed content hashes; the other 24 remain byte-identical to the accepted
proposal. Current complete public-file SHA-256 values, reviewed diff/statistics,
privacy/preservation results and publication-scope manifest are retained privately
under `data/private/europe/champions_league/phase5/publication_refresh/`:
`publication_scope.json`, `reviewed_public.patch`, `verification.json` and
`privacy_review.json`. Earlier accepted receipts and the original scope manifest
remain unchanged rather than being overwritten.

Proposed commit remains `Add audited UEFA Champions League workflow and schema v2`.
Branch remains `feature/data-collection`, HEAD
`878d45e47f1ef861b1b774ecc89c94af7851cb34`; remote `origin` points to
`https://github.com/esst-prog2/toto.git`. Proposed normal push remains:

```sh
git push origin HEAD:refs/heads/feature/data-collection
```

**Verification remains PASS; publication pending explicit approval of the refreshed
exact scope.** Nothing is staged, committed or pushed. Stop for owner approval.

## Owner-approved publication authorization

The owner explicitly approved the refreshed 27-path publication scope, the commit
subject `Add audited UEFA Champions League workflow and schema v2`, and a normal
push exclusively to `origin/feature/data-collection` from the original `toto`
worktree. The approved pre-publication HEAD is
`878d45e47f1ef861b1b774ecc89c94af7851cb34`; the remote branch tip was verified equal.
The approved refreshed scope manifest has SHA-256
`0072ff6314b466d9210d284f356b4bcfc1093b319735ea88e2c6dc0d8faeee84`.

Before staging, all 27 approved public hashes and all 2,677 required protected-file
checks passed freshly; the earlier interrupted wider reads are not used as proof.
The final tested code and validation-input bindings remain unchanged: accepted
2,822 tests/27 subtests, 18 equivalent output guarantees, independent reconstruction
and 22 byte-identical reproduced artifacts remain valid without redundant reruns.
Only this approval note and the required append-only planning entry are added to
the approved public contents, as explicitly authorized. No historical data, schema,
model, dependency, README or unrelated file is part of these additional changes.

Stage only the named 27 public paths, inspect and verify the actual staged scope,
content/privacy and whitespace, then create the approved normal commit and execute
only `git push origin HEAD:refs/heads/feature/data-collection`. No merge, rebase,
forced operation or other branch/worktree is authorized. The final private receipt
under `phase5/publication/` records the resulting commit/remote identity, actual
committed paths, final preservation/privacy checks and Git status. Publication and
closure are complete only if those checks succeed; otherwise stop and report the
exact blocker. No further competition or model work is authorized.
