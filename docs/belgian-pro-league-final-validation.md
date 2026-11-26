# Belgian Pro League — Phase 8 independent final validation

Review date: 2026-11-26. Original `toto`, branch `feature/data-collection`, expected HEAD `013bb9c195624d5ac290aeb57dae11c4e21c0b5a`.

**Final status: PASS for the approved Belgian dataset, independent reproduction, regression tests and required preservation scope.** No material data inconsistency was found. No approved match, adjudication or earlier artifact is corrected by this review.

## Independent method

The new `scripts/validate_belgian_pro_league_final.py` imports only Python standard-library modules. It does **not** import the Phase7 standardizer, projection, name-table, match-ID, conversion, serialization or validation functions. Its own parsers read original historical CSV, six OpenFootball TXT originals and the supplementary2021/22 RSSSF HTML, preserving original bytes, physical-line hashes and source IDs. Existing1992/93 and2009/10 documentary originals remain separately protected.

The parser independently checks raw scores and auxiliary goals/outcomes, explicit calendar headings/weekday/year, actual title seasons, stage/round/leg context, named entities, source hashes and pinned Git blob identities. The intentionally misplaced `2021-22/be1.txt` must declare2020/21; other unapproved path/title disagreements block validation. RSSSF interruptions and continuations remain distinct descriptions of single frozen events. Award numbers are read from the source annotations, not invented from on-field scores.

All10,434 original representations are rebound to the authoritative8724 Phase6 decisions. Each physical contributor must appear exactly once; original dates, teams, numerical results, stage/round/leg and source hashes are independently checked. Grouping follows the approved event membership, not newly invented fixture or eligibility rules.

Canonical names are independently reconstructed from raw coeval representations sharing an approved event: historical source labels anchor that season, and modern/RSSSF labels must map consistently and injectively to them.2025/26 preserves original modern labels. No Phase7 mapping table is used. Unresolved, contradictory, many-to-one or city-only merges block the check. These are source/season correspondences, not global legal-continuity aliases.

Expected rows are reconstructed directly from the approved dates/results and independent names. Every ID is independently calculated as SHA-256 of UTF-8 compact JSON `[league,season,date,home_team,away_team]`. The validator independently serializes a sorted eight-column CSV, then compares all row values, order, bytes and SHA-256 with the approved original. The independent regenerated CSV is written only into temporary storage during reproduction; the approved CSV is never overwritten.

The complete Phase7 archive is compared with each frozen Phase6 decision and independently expected output. Name proofs must match original event participants and standardized sides. The30 earlier Mouscron documentary entries are checked against their original physical source lines and remain outside the10,434/8,724 union.

## Dataset and accounting being verified

Approved CSV: `data/private/belgium/pro_league/belgian_pro_league_standardized_1995_2026.csv`.

Expected/independently reconstructed SHA-256:
`8d4e37b1697ae94c8a54d2247476578b3b85f7076e58c2fe5d024a7721791475`.

Exact schema:

```csv
match_id,date,league,season,home_team,away_team,home_goals,away_goals
```

| Population | Count |
|---|---:|
| Original CSV observations |8,394|
| Original TXT observations |1,706|
| Supplementary RSSSF descriptions |334|
| Combined contributing representations |10,434|
| Approved event groups |8,724|
| INCLUDE / standardized |8,592|
| HOLD_OUT |120|
| NOT_PLAYED |10|
| OUT_OF_SCOPE |2|
| Separate earlier Mouscron documentary entries |30|

No historical research lead becomes a source record. The supplementary early-season candidate list remains empty. All five early seasons remain gaps, not fabricated zero-score or NOT_PLAYED records.

## Season, stage and exceptional-event checks

The independently reconstructed36-season matrix is saved privately. It must match every approved INCLUDE count and actual CSV count, not merely the aggregate. Sensitive season counts are2018/19:269;2019/20:232;2020/21:330;2021/22:329;2023/24:312;2024/25:313;2025/26:121.1990/91–1994/95 each have zero approved records.

| Stage | Independently required rows |
|---|---:|
|Regular season|8,370|
|Championship playoffs|113|
|Europe playoffs|83|
|Playdowns|24|
|European qualifiers|2|
|Total|8,592|

Required date/result checks: Beerschot–Cercle2021-07-24,0–1; Seraing–Union2022-01-15,0–4; Union–Beerschot2022-04-10,5–0; Standard–Charleroi2021-12-05,0–3; Antwerp–Charleroi2025-05-29,1–2. The two original interruption dates and later completions must remain traceable in the raw and audit evidence.

Exclusions remain Standard–Anderlecht2019 HOLD_OUT, Standard–Westerlo2024 and Leuven–Mechelen2022 NOT_PLAYED, eight cancelled2019/20 slots,119unscored2025/26 slots and two cross-division legs. None may carry a screened projection. The source award numbers are retained in audit, not silently relabelled as ordinarily played results.

The independent pairing calculation must reproduce222repeated directed pairings/444distinct fixtures. Same-team playoff rematches remain separate by date and match ID. Shared-ID collisions, source reuse, missing/extra rows, wrong scores/dates, duplicate IDs and unauthorized inclusions are blocking defects. Club/Cercle and other legal-identity boundaries are not globally merged.

## Reproducibility and operational safeguards

Four validation assessments plus a deterministic manifest are private under `data/private/belgium/pro_league/phase8/`:

- `raw_source_traceability.json`
- `record_reconciliation.json`
- `season_stage_and_rematches.json`
- `findings_and_preservation.json`
- `reproducibility.json`

A separate process and temporary directory regenerate these five artifacts; bytes and SHA-256 must agree. The same process independently reconstructs the entire approved CSV and compares its temporary bytes with the preserved original. This is independent dataset regeneration, not merely rerunning Phase7 conversion.

```sh
PYTHONDONTWRITEBYTECODE=1 python -B scripts/validate_belgian_pro_league_final.py
PYTHONDONTWRITEBYTECODE=1 python -B scripts/validate_belgian_pro_league_final.py --verify
```

The initial preservation check reached25/45/90/240-second diagnostic bounds during file reads; no timeout was counted as success. A traceback established that imports had completed and the delay occurred during protected-file reads. Controlled canonical reads outside the filesystem sandbox completed promptly for three sampled files, but the exact file-provider/sandbox contribution is not proven as a universal root cause.

Two initially strict guards stopped when file metadata changed during a read. Repeated bytes for the affected older Ligue2 status/log files matched their frozen SHA-256 values; stable subsequent reads showed no data discrepancy. The new validator therefore confirms a metadata-transition read with a second matching hash and requires both reads to match the approved bytes; metadata changes alone are not treated as altered content. Actual checksum mismatches still block; approved data was never repaired. Synthetic tests cover that distinction.

Fresh SHA-256 reads are checkpointed only in temporary storage, under this exact Phase8 baseline. Reuse requires unchanged file identity/size/mtime/ctime and the expected digest; no previous-phase check is silently substituted. Eight local read-only workers avoid serial file-access latency. New assessments and temporary checkpoints are the only writes. The original environment and all prior project data were never written by this review. The exact fresh-content verification scope and limits are recorded below.

## Tests and remaining limitations

Focused synthetic tests cover raw CSV contradictions, wrong-season files, bad rounds/calendar headings, unscored slots, multiline RSSSF awards, interruptions, incorrect IDs, missing/extra/duplicate rows, stage collisions, legitimate rematches, unsupported aliases, metadata transitions and immutable assessment writes.

Final fresh results are recorded below. Test selections overlap and must not be added together. Earlier completed test runs are not treated as fresh passes for any check that timed out.

Technical PASS does not certify every historical fact or legal outcome. The five early gaps, partial2025/26 snapshot, omitted/annulled populations, incomplete independent sampling, upstream source dependence, club continuity, finality and publication-time uncertainties remain. Owner-approved use is **retrospective internal diagnostics**, not leakage-free forecasting or real-world predictive-performance evidence. No publication or model-training rights follow from validation.

## Phase9 recommendation — no authorization exercised here

After owner approval, inspect and explicitly stage only the public Belgian scripts/tests/docs listed below plus append-only `PLANNING_LOG.md`. Run staged-diff checks and privacy checks, then use a normal commit/push only if separately authorized. Exclude all `data/private/`, CSV/audit/receipt/evidence bundles, environments, temporary files and both `.DS_Store` files. Do not merge branches or alter the application/promotional worktree. Preserve coverage and rights disclosures in the final commit documentation.

Exact intended public scope follows below. No files were staged by Phase8.

```text
PLANNING_LOG.md
docs/belgian-pro-league-2021-22-recovery.md
docs/belgian-pro-league-adjudication.md
docs/belgian-pro-league-early-seasons-recovery.md
docs/belgian-pro-league-feasibility.md
docs/belgian-pro-league-final-validation.md
docs/belgian-pro-league-historical-review.md
docs/belgian-pro-league-inventory.md
docs/belgian-pro-league-standardization.md
docs/belgian-pro-league-validation.md
scripts/assess_belgian_early_recovery.py
scripts/collect_belgian_pro_league_feasibility.py
scripts/collect_belgian_pro_league_history.py
scripts/decide_belgian_pro_league_policy.py
scripts/inventory_belgian_pro_league_history.py
scripts/recover_belgian_2021_22.py
scripts/standardize_belgian_pro_league_results.py
scripts/validate_belgian_pro_league_feasibility.py
scripts/validate_belgian_pro_league_final.py
scripts/validate_belgian_pro_league_structure.py
scripts/verify_belgian_pro_league_feasibility.py
scripts/verify_belgian_pro_league_inventory.py
scripts/verify_belgian_pro_league_review.py
tests/test_belgian_2021_22_recovery.py
tests/test_belgian_early_recovery.py
tests/test_belgian_pro_league_feasibility.py
tests/test_belgian_pro_league_final.py
tests/test_belgian_pro_league_history.py
tests/test_belgian_pro_league_policy.py
tests/test_belgian_pro_league_review.py
tests/test_belgian_pro_league_standardization.py
tests/test_belgian_pro_league_structure.py
```

## Final measured results and preservation scope

**PASS.** Independent original-byte parsing and decision/output reconciliation found no material defects. All8,592 CSV rows match the approved registry exactly. Every ID was recomputed independently; no duplicate, shared-identity or prior-competition collision occurred. Independent coeval name reconstruction produced628source/season correspondences. The raw overlap calculation independently recovers1,402CSV/TXT paired events and306historical/RSSSF regular counterparts. All10434representations,8724events and30separate documentary entries reconcile without loss or duplication.

The five assessment files regenerated in a separate process/temp directory with identical bytes and SHA-256. The independently reconstructed temporary CSV also matches the preserved approved CSV byte-for-byte and has SHA-256 `8d4e37b1697ae94c8a54d2247476578b3b85f7076e58c2fe5d024a7721791475`. No Phase7 content function or name table was imported for that reconstruction.

Fresh final tests: **48focused;412Belgian;503acquisition/importer;7app/launcher;2573full repository passed**. These selections overlap; all final runs had zero failed, errored or skipped tests. The environment was the pre-existing external offline CPython3.13.12 environment; no dependency installation, download or original-venv execution was needed. Early timeouts and transient metadata-only guard stops were not counted as passes.

Fresh completed byte-preservation scope is **418 unique files**:153frozen Belgian/pre-Phase8 public/private entries,250previous public-code files, and15previous compatible screened/audit CSVs. That includes alltenBelgian originals, allfrozen Phase2–7/recovery evidence, twelve earlier screened historical datasets containing137189records and the two separate ongoing English datasets containing258records. The SerieB audit is included only for compatible ID coverage, not added to screened totals. Planning-log prefixes, expected HEAD and original index hash match.

**Limits on broader preservation claims:** the full population of1400other older non-Belgian private artifacts (originals, logs and verification files beyond the screened/audit CSVs) was not exhaustively rehashed; interrupted attempts checked some, but no complete claim is made. Those files were never written by this work. An additional optional original-environment package rehash was stopped after500checkpointed matching package hashes; a fresh full6200package-byte certificate is **not** claimed. No environment, package, configuration, application or promotional files were written or rebuilt. These extended scans are distinguished from the completed Belgian/source-output and prior-standardized-data checks.

Private CSV and detailed artifacts remain Git-ignored; no private data is tracked or staged. Nothing was staged, committed, pushed, merged, rebased, trained or integrated. Existing uncommitted Belgian work and both `.DS_Store` files remain. The32-file public scope above is a recommendation for later explicit approval, not a staging action.

The initial broader scan was intentionally narrowed to the Phase8 required assets after file-access delays; the narrower completed scope is disclosed rather than claiming all earlier private fingerprints or package bytes were freshly checked. No reviewed result, identity, date, source, Phase6 disposition or existing artifact was altered.

Phase9 may proceed only on explicit owner authorization, with the documented coverage/licensing limits and this preservation scope visible in the finalization report. Any separately requested exhaustive legacy-private/package rehash remains an additional check, not a completed result here. **Stop after Phase8.**

Validated artifact SHA-256 values:

| Artifact | SHA-256 |
|---|---|
| `raw_source_traceability.json` | `aa6d78ee11643f9c1632909cd835345c69b55d90b4af3bd4ef7775adbfd1c087` |
| `record_reconciliation.json` | `e24fb984fda8bb22246ec27175478cc1113dfdea3fd6c2d8e798053b30767533` |
| `season_stage_and_rematches.json` | `6326a28d4e7cc7d04804a8425ea9b934876b400d7217997c304e7f4b1da2d4c7` |
| `findings_and_preservation.json` | `edcfa39bfea7ae7405567d0890e429a51eb99c1b8a38e3e9a842dedd77c93061` |
| `reproducibility.json` | `eaf07f1ebf28418b727442f3dbc60a25f6db2368c9cbb66e81bdf24edf748f91` |


## Phase 9 — finalization and authorized publication

Measured 2026-11-26. The owner approved Phase 8 and explicitly authorized the exact 32 public paths above for a normal commit and push on `feature/data-collection`. Starting HEAD and freshly queried upstream both equal `013bb9c195624d5ac290aeb57dae11c4e21c0b5a`; initial staging was empty. Earlier phase reports remain historical records, not current authorization or completeness claims.

Final competition name is **Belgian Pro League**. Target coverage remains **1990/91–2025/26**; actual standardized coverage is **31 represented seasons, 1995/96–2025/26**, with **8,592** screened records. The five seasons **1990/91–1994/95 remain missing**. The partial 2025/26 snapshot contributes **121 accepted fixtures**, with 119 unscored slots held out. Original OpenFootball `2021-22/be1.txt` contains actual **2020/21**; the genuine 2021/22 comparison is separately attributed to RSSSF.

Approved retrospective internal-diagnostic policy remains original football dates and accepted historical final scores, including the two approved initial-kickoff dates for resumed events. This is not publication-time-safe historical forecasting. Unplayed awards, unresolved results, annulled documentary entries and cross-division events remain separate. Source access, technical correctness and historical acceptance establish neither redistribution nor model-training permission. No application integration or training is authorized.

Fresh Phase 9 execution passed **412 Belgian tests, 503 acquisition/importer tests, seven app/launcher tests and all 2,573 repository tests**, with zero failures, errors or skips (overlapping selections). The pre-existing external offline environment was reused; no package installation, dependency change or original-environment execution occurred.

The independent final validator freshly reconstructed all 10,434 representations, 8,724 event decisions and 8,592 CSV rows, and independently regenerated the CSV and all five Phase 8 artifacts in a separate temporary process with identical bytes and SHA-256. CSV SHA-256 remains `8d4e37b1697ae94c8a54d2247476578b3b85f7076e58c2fe5d024a7721791475`. All 418 required protected fingerprints remain valid, including ten Belgian originals, frozen evidence, prior public code, twelve previous historical screened datasets (137,189 rows) and separate ongoing English data (258 rows).

Bounded extended preservation read **1,136 of 1,415 older private baseline files**, all matching; **279 were not freshly rehashed in that optional run**. The required screened/audit subset is checked separately by the independent validator, so this optional count is not additive to 418. A separate original-environment attempt matched **530 of 6,200 package files**, leaving **5,670 without a fresh Phase 9 package hash**. No actual content mismatch was found. These incomplete optional scans do not block publication under the owner's express instruction; no exhaustive legacy-private/environment certification is claimed.

All documented earlier verification entry points were attempted with bounded execution. The Phase 4 structural generator completed and returned the seven saved artifact hashes. The Phase 2 feasibility verifier timed out at 60 seconds, as did a sequential inventory attempt; bounded 30-second attempts of inventory, structural `--verify`, recovery, historical review, policy, early recovery and Phase 7 `--verify` also timed out. Their preservation chains include the older private files implicated in prior file-read delays. These timeouts are **not passes** and do not establish fresh full Phase 2–7 regeneration. Approved Phase 8 byte-identical Phase 7 reproduction remains prior evidence; the fresh independent Phase 8 reconstruction and required preservation checks passed. Temporary timed-out workers were ended; no guards were bypassed or source files changed.

Final public-scope review found no dataset exports, downloaded originals, private evidence bundles, credentials or personal home-directory paths in the proposed changes. Historical reports contain bounded factual samples, source attribution and links, not private bulk extracts. Deliberate temporary-environment paths document earlier execution provenance. Local documentation links and referenced script modules resolve. All 132 Belgian private files are Git-ignored and no `data/private/` file is tracked. Both existing `.DS_Store` files are excluded.

Publication procedure: explicitly stage only the 32 listed paths, inspect staged contents and exact scope, require `git diff --cached --check`, commit `Complete Belgian Pro League historical data screening`, then push normally and independently compare local and remote hashes. Commit/push outcomes are reported after execution; this paragraph does not claim publication in advance. Frozen pre-publication validators intentionally bind the original HEAD and empty index; run them before staging, rather than rewriting their historical guards after publication.
