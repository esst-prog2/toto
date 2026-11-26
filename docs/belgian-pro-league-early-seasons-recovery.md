# Belgian Pro League — bounded early-season recovery

Date: 2026-11-25. Original `toto`, branch `feature/data-collection`, unchanged HEAD `013bb9c195624d5ac290aeb57dae11c4e21c0b5a`.

## Outcome and limits

**NO ADEQUATELY VERIFIED, PERMITTED DATASET IS AVAILABLE within this bounded investigation.** This is a finding about the sources/routes inspected, not proof that no such historical records exist anywhere.

No new dated/scored fixture original was acquired. The supplemental candidate registry is empty. No fixture was fabricated, inferred from standings, assigned NOT PLAYED from absence, or added to the approved Phase6 population. Nominal expectations remain18clubs,34rounds and306fixtures per season (1,530 slots across five seasons), not validated individual results.

The owner permits incomplete recovery. Recommend retaining the five source gaps and, after separate approval, proceeding with the already approved8,592 INCLUDE events. Phase7 has not begun.

## Permission-first source assessment

Permission assessment and source selection are recorded privately in `early_recovery/source_assessment_inputs.json`. No collector is enabled for blocked or uncleared fixture pages. `automation_authorized=false` in this assessment means no permission-cleared, bounded fixture acquisition route was selected for this task; it does not assert that every publisher prohibits every automated access method.

| Candidate | Actual inspection | Access/rights assessment | Acquisition decision |
|---|---|---|---|
| BDFutbol, five owner-supplied season URLs | Official API documentation appeared in search results; direct API page returned403. One direct canonical robots request also returned403. Canonical llms policy was not inspectable. | Paid authenticated data service is advertised. A secondary policy mirror reports restrictions, but is not treated as verified current canonical terms. No active API licence or written permission established. | STOP; no season fixture pages extracted, no API purchase, login, challenge bypass or retry of denied data endpoints |
| Global Sports Archive, five supplied season routes |1990/91 page inspected for source suitability;1991/92 indexed title/date-result examples found. Other supplied season routes remain unverified leads. Public homepage/footer inspected ephemerally for legal notices. | Robots returned200 and allows `/`, but this does not grant a data-use licence. Footer reserves rights; a readable applicable terms document or permitted historical export was not established. | STOP fixture acquisition; no fixture-list archive, pagination/API extraction or candidate-row import |
| Existing RSSSF1992/93 original | Reparsed the immutable attributed snapshot independently;18 first-division standings rows,34 games each | Existing copying-with-author-acknowledgement notice preserved; no model-training grant inferred | Reuse standings for structural corroboration only, zero new match records or downloads |
| RSSSF1993/94 and1994/95 capability checks | Top-flight portions directly inspected: final standings, not dated league fixture lists; other division/cup data kept separate |1994/95 footer permits attributed copying, but permission cannot create missing top-flight dates | No new original acquired; no cross-competition imports |
| RSSSF1990/91 and1991/92 canonical season paths | Web tool could not inspect those URLs | Contents/dated coverage not established; no alternate-host or access-control workaround | Research leads only |
| OpenFootball Belgium | Current root metadata inspected: modern season directories; no five target-season files shown | CC0 declaration is a positive reuse statement, not evidence that missing seasons exist | No new target original found or moving-branch data acquired |
| schochastics/football-data | README and `data/results` directory metadata inspected | README declares Open Data Commons Attribution. Exact Belgian coverage, upstream provenance and historical accuracy remain unverified; author warns about older results and identity continuity. | Promising future lead, but only global `games.parquet` exposed; no verified five-season export. Whole worldwide bundle not downloaded outside bounded scope |

Exact candidate links:

| Season | BDFutbol lead | GSA lead |
|---|---|---|
|1990/91|[BDFutbol](https://www.bdfutbol.com/en/t/tbel1990-91.html)|[GSA5820](https://globalsportsarchive.com/en/soccer/competition/eerste-klasse---division-1-1990-1991/5820)|
|1991/92|[BDFutbol](https://www.bdfutbol.com/en/t/tbel1991-92.html)|[GSA5819](https://globalsportsarchive.com/en/soccer/competition/eerste-klasse---division-1-1991-1992/5819)|
|1992/93|[BDFutbol](https://www.bdfutbol.com/en/t/tbel1992-93.html)|[GSA5818](https://globalsportsarchive.com/en/soccer/competition/eerste-klasse---division-1-1992-1993/5818)|
|1993/94|[BDFutbol](https://www.bdfutbol.com/en/t/tbel1993-94.html)|[GSA5817](https://globalsportsarchive.com/en/soccer/competition/eerste-klasse---division-1-1993-1994/5817)|
|1994/95|[BDFutbol](https://www.bdfutbol.com/en/t/tbel1994-95.html)|[GSA5816](https://globalsportsarchive.com/en/soccer/competition/eerste-klasse---division-1-1994-1995/5816)|

Permission/provenance references:

- [BDFutbol API](https://www.bdfutbol.com/en/c/api2.html): official search-index information; direct403, not claimed directly inspected current full terms.
- [Canonical BDFutbol robots](https://www.bdfutbol.com/robots.txt): direct403. [Canonical llms policy](https://www.bdfutbol.com/llms.txt): web-tool unavailable. [Secondary mirror](https://llmscentral.com/domain/bdfutbol.com): lead only, no substitute authorisation.
- [GSA robots](https://globalsportsarchive.com/robots.txt): one privately preserved access-policy original, exact URL/final URL, HTTP headers, UTC timestamp, byte size and SHA-256. [Homepage](https://globalsportsarchive.com/en/soccer): footer/legal inspection only; full HTML not retained. Robots allows crawling, not blanket extraction, redistribution or model training.
- [DSG official football offering](https://datasportsgroup.com/package/top-50-pack/): Belgian top-flight listed in commercial API offering; no trial/account activated or sales message sent.
- [RSSSF1992/93](https://www.rsssf.org/tablesb/belg93.html), [1993/94](https://www.rsssf.org/tablesb/belg94.html), [1994/95](https://www.rsssf.org/tablesb/belg95.html): first-division standings must not be confused with dated cup or lower-division results.
- [OpenFootball metadata](https://github.com/openfootball/belgium).
- [Schoch README](https://github.com/schochastics/football-data) and [results directory](https://github.com/schochastics/football-data/tree/master/data/results): metadata only, no Parquet payload downloaded. A declared open licence is not dismissed; what remains missing is a bounded, provenance-reviewed, independently validated target extract. Its goals may include extra time/penalties, so any future extract needs full-time semantics checks.

No Git commit or blob was invented for a web page. No moving Git fixture source was acquired. Search-index/cache availability is not equivalent to a fresh successful direct HTTP response. Missing HTTP metadata is left unknown rather than fabricated.

## Exact five-season coverage

Counts below refer to recovered permitted fixture observations, not how many results a candidate publisher might display. Full source-list completeness could not be measured without a qualifying acquisition.

| Season | Nominal fixtures | Recovered source observations | Distinct events | Fully corroborated | Partially corroborated | Conflicting/unresolved observed candidates | Preliminary candidates | Nominal uncovered slots |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
|1990/91|306|0|0|0|0|0|0|306|
|1991/92|306|0|0|0|0|0|0|306|
|1992/93|306|0|0|0|0|0|0|306|
|1993/94|306|0|0|0|0|0|0|306|
|1994/95|306|0|0|0|0|0|0|306|
|Total|1,530|0|0|0|0|0|0|1,530|

Zero observed conflicts is **not** evidence of agreement: fixture-level cross-source comparison was **NOT EXECUTED / NOT ASSESSABLE**, because no qualifying fixture lists were acquired. All five remain SOURCE_GAP coverage findings. The1,530 nominal uncovered slots are not1,530 known unplayed or identified missing matches.

Dates, individual scores, round schedules, directed pairing completeness, postponed/administrative events and match-level identity exceptions remain unverified for all five seasons. No claim of historical certification or even a complete structural fixture pass is made. There are no newly identified fixture exceptions to disposition; that is not proof none existed.

## Independently reused structural evidence

The existing1992/93 RSSSF original (Dinant Abbink/RSSSF,updated5September2004) has SHA-256 `741ab42252840042e61363965535e0c4efb71c8d389e6790989b7e85be2832ae` and remained unchanged.

The new offline parser confirms18 distinct top-flight labels/ranks,34played per club,612 club-match participations, W+D+L consistency, two-points-per-win arithmetic, equal aggregate wins/losses and equal goals for/against (947each).612/2 yields the306 aggregate fixture expectation. This does **not** recover the306 pairings, dates or scores.

Original labels such as FC Brugge/Cercle Brugge, Germinal Ekeren, RC Genk and RWD Molenbeek remain unchanged. No legal continuity or global alias is inferred from standings. An [indexed BDFutbol forum lead](https://www.bdfutbol.com/foro/showthread.php?pid=57730&tid=15504) indicates RSSSF-based standings, so future standings agreement may share upstream; fixture-source independence remains unknown. No database pair is counted as independent historical confirmation.

## Separate populations and preliminary recommendation

The frozen Phase6 registry remains exactly:

| Disposition | Events |
|---|---:|
|INCLUDE|8,592|
|HOLD_OUT|120|
|NOT_PLAYED|10|
|OUT_OF_SCOPE|2|
|Total|8,724|

All10,434 contributing representations and30 separate Mouscron documentary entries are preserved. The early supplemental registry contains **zero observations and zero events**. Nothing was merged, reclassified, standardized or assigned a new shared match ID.

Retrospective internal-diagnostic policy is unchanged: original football dates, accepted final historical results where sufficiently supported, no judgment-publication timestamp filtering, and no claims of leakage-free historical forecasting or predictive performance. Rights and model-training clearance remain separate.

Recommendation: preserve the early gaps and proceed with the already approved8,592 INCLUDE events **only after explicit Phase7 approval**. No supplemental adjudication is needed for an empty candidate registry.

If recovery is revisited, first obtain either a permission-cleared five-season publisher export or a season-scoped extract from the openly licensed lead with exact lineage and source identity. Do not download a worldwide bundle, buy API access, contact a publisher, or access restricted endpoints under this task. Then pin/snapshot the exact bounded originals, preserve bytes/receipts, validate all dated pairings/results, perform independent historical comparison, and submit a separate supplemental Phase6 adjudication recommendation with measured counts before any merge or standardization. No messages requesting permission were sent.

## Implementation and reproducibility

New public work:

- `scripts/assess_belgian_early_recovery.py`: offline source assessment, frozen-population protection, existing standings parser and permission/provenance/fixture/cross-source validation helpers. No network fixture collector is enabled.
- `tests/test_belgian_early_recovery.py`:49 focused synthetic tests for permission gates, exact scope, receipt integrity, invalid/proxy dates, scores, encoding, source bindings, directed pairings, duplicates, source independence, immutable atomic preservation and standings-versus-fixtures distinction. Synthetic passing tests do not imply unavailable historical fixtures were validated.
- This report and append-only `PLANNING_LOG.md` entries.

Private new files: `early_recovery_protected_before.json` (112 frozen prior entries); `early_recovery/source_assessment_inputs.json`; `early_recovery/access_receipts.json`; `early_recovery/gsa_robots.txt`; under `early_recovery/assessment/`, four JSON assessments plus `reproducibility.json`; final receipt `early_recovery_final_verification.json`. There are **zero new match-data originals**, one small preserved robots policy file, and reused—not redownloaded—RSSSF1992/93 bytes. Unclear-rights fixture HTML was not preserved.

```sh
PYTHONDONTWRITEBYTECODE=1 python -B -m scripts.assess_belgian_early_recovery
PYTHONDONTWRITEBYTECODE=1 python -B -m scripts.assess_belgian_early_recovery --verify
```

Generation is offline, deterministic and refuses to overwrite differing artifacts. A separate process/temp directory regenerates all five outputs and compares bytes and SHA-256. The manifest binds the access receipts, permission assessment, robots bytes, implementation and frozen baseline. No access-denied route is retried by regeneration, and no nominal fixture placeholders are fabricated.

Fresh test and preservation results are recorded below after execution. The task stops at this supplementary assessment: no Phase7, standardized CSV, training, application changes, staging, commit, push, merge or rebase.

## Executed checks and preservation

- **49 focused tests passed;324 Belgian tests passed;503 acquisition/importer tests passed;7 app/launcher tests passed;2,485 full-suite tests passed.** These selections overlap. Zero final failures, errors or skips; no timeout counted as a pass.
- All **five new assessment artifacts** independently regenerated in a separate process/temp directory, byte-for-byte and SHA-256-identical. Fixture acquisition requests during generation/regeneration:zero.
- All **112 frozen pre-recovery entries**, earlier nested Phase2–6/recovery baselines, original1,415 private and250 public fingerprints and planning-log history remain unchanged. All ten existing Belgian source originals preserved. The approved Phase6 registry was neither rewritten nor supplemented.
- Twelve prior completed historical outputs still contain **137,189** screened records; the separate **258** ongoing English records remain unchanged. Original environment/application/promotional worktree untouched. All **6,200** original runtime-package fingerprints match. Reused the existing external offline CPython3.13.12 environment; no installations or dependency downloads.
- Private originals, access receipts, source notes and assessments remain Git-ignored. No private datasets tracked or staged. HEAD and index unchanged. Existing uncommitted work and the two untracked `.DS_Store` files preserved.
- Only this report, the new assessment script/tests, append-only planning entries and new private recovery artifacts were created/updated for this task. No Phase7, standardized CSV, model training, application integration or Git publication occurred.

**Final classification: NO ADEQUATELY VERIFIED, PERMITTED DATASET IS AVAILABLE in this bounded recovery. Preserve the five gaps; await explicit approval before any further acquisition, supplemental adjudication or Phase7.**
