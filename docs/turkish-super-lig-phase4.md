# Turkish Süper Lig — Phase 4 standardization

**PASS. Phase 4 only; stop before finalization.** The owner approved Phase 3 and all 480 supplemental early recoveries, including nine explicitly bound TFF source repairs. A new derived registry composes those approvals while preserving the frozen Phase 3 records, supplemental proposals and original bytes unchanged.

## Population and canonical output

| Disposition | Events | CSV rows |
| --- | ---: | ---: |
| INCLUDE | 10,540 | 10,540 |
| HOLD OUT | 3 | 0 |
| NOT PLAYED | 30 | 0 |
| OUT OF SCOPE | 1 | 0 |
| **Total conditional events** | **10,574** | **10,540** |

The private canonical CSV is `data/private/turkey/super_lig/phase4/validated/turkish_super_lig_standardized_1992_2026.csv`. Its exact columns are:

```csv
match_id,date,league,season,home_team,away_team,home_goals,away_goals
```

There are 10,540 unique identities and full SHA-256 IDs, across 34 represented seasons, 1992/93–2025/26. The league label is `Turkish Süper Lig`. IDs follow the existing compact UTF-8 JSON `[league,season,date,home_team,away_team]` convention. The shared historical importer supplies validation, IDs and identity ordering; `artifact_io.serialize_csv` supplies UTF-8 without BOM, LF and existing CSV quoting. No deduplication or conflict rejection was needed at this projection boundary.

Names come from the frozen identity anchor for later seasons and explicit professional TFF fixture labels for both recovered seasons. This avoids treating 1993/94 grid abbreviations as club names. Source/season correspondence evidence remains bound in the frozen inventory; no global alias, transliteration or legal-continuity merger was added. Distinct match dates preserve legitimate rematches. No stage suffix or alternative ID convention was introduced.

CSV SHA-256: `c3385ac2ce9d2e963ba34dfdd4cb59090a2f30b147d91a547e3bcdfc061863b8`.

## Complete season and stage matrix

All standardized rows are **REGULAR_SEASON**. Eligible 2011/12 championship/European league postseason fixtures remain a documented 24-description source gap; none were fabricated. The separate optional cup description retains OUT OF SCOPE.

| Season | INCLUDE rows | Clubs | HOLD OUT | NOT PLAYED | OUT OF SCOPE | Absent regular source slots |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1990/91 | 0 | 0 | 0 | 0 | 0 | 240 |
| 1991/92 | 0 | 0 | 0 | 0 | 0 | 240 |
| 1992/93 | 240 | 16 | 0 | 0 | 0 | 0 |
| 1993/94 | 240 | 16 | 0 | 0 | 0 | 0 |
| 1994/95 | 306 | 18 | 0 | 0 | 0 | 0 |
| 1995/96 | 305 | 18 | 1 | 0 | 0 | 0 |
| 1996/97 | 306 | 18 | 0 | 0 | 0 | 0 |
| 1997/98 | 305 | 18 | 1 | 0 | 0 | 0 |
| 1998/99 | 306 | 18 | 0 | 0 | 0 | 0 |
| 1999/00 | 306 | 18 | 0 | 0 | 0 | 0 |
| 2000/01 | 306 | 18 | 0 | 0 | 0 | 0 |
| 2001/02 | 306 | 18 | 0 | 0 | 0 | 0 |
| 2002/03 | 306 | 18 | 0 | 0 | 0 | 0 |
| 2003/04 | 306 | 18 | 0 | 0 | 0 | 0 |
| 2004/05 | 306 | 18 | 0 | 0 | 0 | 0 |
| 2005/06 | 306 | 18 | 1 | 0 | 0 | 0 |
| 2006/07 | 306 | 18 | 0 | 0 | 0 | 0 |
| 2007/08 | 306 | 18 | 0 | 0 | 0 | 0 |
| 2008/09 | 306 | 18 | 0 | 0 | 0 | 0 |
| 2009/10 | 272 | 17 | 0 | 0 | 0 | 34 |
| 2010/11 | 305 | 18 | 0 | 1 | 0 | 0 |
| 2011/12 | 306 | 18 | 0 | 0 | 1 | 0 |
| 2012/13 | 306 | 18 | 0 | 0 | 0 | 0 |
| 2013/14 | 306 | 18 | 0 | 0 | 0 | 0 |
| 2014/15 | 306 | 18 | 0 | 0 | 0 | 0 |
| 2015/16 | 306 | 18 | 0 | 0 | 0 | 0 |
| 2016/17 | 306 | 18 | 0 | 0 | 0 | 0 |
| 2017/18 | 306 | 18 | 0 | 0 | 0 | 0 |
| 2018/19 | 306 | 18 | 0 | 0 | 0 | 0 |
| 2019/20 | 306 | 18 | 0 | 0 | 0 | 0 |
| 2020/21 | 420 | 21 | 0 | 0 | 0 | 0 |
| 2021/22 | 380 | 20 | 0 | 0 | 0 | 0 |
| 2022/23 | 313 | 19 | 0 | 29 | 0 | 0 |
| 2023/24 | 380 | 20 | 0 | 0 | 0 | 0 |
| 2024/25 | 342 | 19 | 0 | 0 | 0 | 0 |
| 2025/26 | 306 | 18 | 0 | 0 | 0 | 0 |

The 1990/91 and 1991/92 originals contain aggregate tables but no individual fixture descriptions. Their 240 nominal slots each remain gaps, not invented NOT PLAYED records. The 1992/93 and 1993/94 exact-date gaps are closed by the approved 240 recoveries per season. The 34 absent 2009/10 Ankaraspor descriptions remain outside the frozen population, including played/later-awarded and no-kickoff slots; no source acquisition or historical decision was added in this phase.

The three retained HOLD OUTs are the unresolved award-football-date cases in 1995/96 and 1997/98, and the abandoned original in 2005/06. Its supported replay remains separate. NOT PLAYED comprises the 2010/11 no-kickoff cancellation and 29 earthquake-related no-play awards in 2022/23. These 34 exclusions have audit entries and no CSV rows.

## Approved corrections and historical semantics

The 480 recovered fixtures comprise 471 date-only recoveries and nine approved source repairs: six scores, two opponents and one malformed club label. Every recovered event retains the original RSSSF observation, its frozen decision hash, exact TFF fixture evidence, and any bound professional-detail panel. Round/detail pages share one TFF authority; no claim of two independent exact-date providers is made. The existing independent final-table reconciliation covers all 32 early club-season rows.

All 143 earlier 2006/07 date corrections remain derived metadata. The ten formerly quarantined one-day disagreements retain their frozen observations and explicit approved Phase 3 resolutions. All 13 prior structurally quarantined events remain tied to their individual historical cases. No quarantine was silently restored through an alternate representation.

Dates use original football kickoff semantics and supported final historical results, without administrative-publication-date filtering. Original kickoff and completion dates remain separate in private decisions for interrupted/resumed fixtures. COVID scheduling through 26 July 2020, earthquake withdrawals, played-and-awarded results and no-kickoff exclusions retain their approved treatment. The 2025/26 primary contributes all 306 completed fixtures; its partial alternate does not override scored primary results.

## Traceability and independent checks

Private outputs under `phase4/validated/` are the CSV, `approved_decision_registry.json`, `source_to_output_audit.json`, `season_stage_coverage.json`, `standardization_manifest.json` and `independent_standardization_validation.json`. The approval record binds the two frozen registries by SHA-256. The audit covers every one of the 10,574 events and all 13,894 prior source observations, including excluded and alternate representations. Each row has its event/decision hash, CSV physical row, original source URL/file/SHA-256 and physical line/span or grid-cell locator; recovered evidence additionally carries TFF byte spans, record hashes and fixture IDs. Original fields, corrections, historical evidence and completion dates remain available through the bound private inputs.

The independent validator imports no production standardizer, production content/name parser, shared importer, ID helper or serializer. It reconstructs original CSV/TXT/RSSSF observations with the established independent grammars, checks every frozen historical decision against original fields and approved facts, reconstructs the TFF records independently, and compares every output field, ID, order and complete CSV bytes. It checks all 480 recoveries, nine repairs, 143 earlier corrections, three retained holds, all exclusions, season/stage counts and source accounting. Human-reviewed policies and historical judgments are shared inputs; code independence does not independently repeat that research or establish disjoint publisher upstreams.

Cross-competition validation inspected all 15 pre-existing standardized CSVs across the 13 completed competitions, including ongoing snapshots: **146,039 rows**, zero Turkish league-label or match-ID collisions. Protected fingerprints separately verify their preservation.

## Focused verification and reproduction

**210 tests and 27 subtests passed**, with no final failures, errors or skips: 105 Turkish tests (25 new standardization safeguards) plus shared importer/artifact-I/O and Belgian standardization regressions. Adverse cases cover missing/extra/duplicate rows, valid rematches, wrong IDs, venue reversal, changed scores, wrong seasons/stages, COVID boundaries, kickoff/completion confusion, invalid goals, source identity collapse, serialization changes and overwrite refusal. Existing recovery tests cover changed originals, unreviewed repairs and professional/youth identity confusion. The complete suite is reserved for Phase 5.

A read-only original-venv probe stalled during an installed dependency import and was interrupted. The already existing external CPython 3.13.12/pytest environment was reused without downloads, copying, installation or changes to the original environment. One initial independent-verifier source-counter comparison defect was corrected; the final independent reconstruction passed. Both attempts remain recorded privately and included in elapsed time.

```sh
PYTHONPATH=src:. PYTHONDONTWRITEBYTECODE=1 python3 -B -m scripts.standardize_turkish_super_lig_results --verify
PYTHONPATH=src:. PYTHONDONTWRITEBYTECODE=1 python3 -B -m scripts.verify_turkish_super_lig_standardization --verify
```

The exact selected-test command/interpreter, fresh-process commands and results are recorded privately. Production artifacts and the independent assessment are reproduced in separate fresh processes and temporary directories with network connections forbidden; the independently serialized CSV is compared byte-for-byte too. Deterministic artifacts contain no execution timestamps. Acquisition is unnecessary; all 96 preserved originals (26 prior and 70 supplemental, including permission/metadata documents) remain immutable inputs.

## Rights, preservation and stop

Originals, canonical CSV, event lists and detailed audits stay under ignored `data/private/`; public documentation contains methods and aggregate results. Attribute James Curley/engsoccerdata, Football-Data, OpenFootball, RSSSF and TFF as recorded in source receipts. Existing noncommercial, attribution, upstream licensing, preservation and model-training restrictions remain unchanged. GPL package-code terms and accessible website data do not establish general data redistribution or training rights. The TFF supplementary scope remains bounded private personal/noncommercial research. No new rights or external corroboration follow from standardization.

The baseline covers **2,206 existing entries, including 1,888 private files**, all previous competition artifacts, existing dirty work, append-only planning history, Git index and original environment configuration. Git objects, caches and installed package bytes are not exhaustively rehashed. No access to `toto-hungary` occurred. No application, prediction logic, previous datasets, frozen records, branches, worktrees or shared infrastructure were changed. No stage, commit, push or Phase 5.

Final preservation, reproduction, code/input/output hashes and measured timing are recorded in private execution receipts. `PLANNING_LOG.md` is append-only.

**STOP after Phase 4. Await explicit owner approval before Phase 5.**

Final preservation audit: **all 2,206 baseline entries matched**, including **1,888 prior private files**; the planning-log prefix, HEAD, branch and Git index matched. All Phase 4 private files were ignored and untracked, and the public status delta contained exactly the two new Turkish scripts, one synthetic test module and this report.

Measured execution: **11 min 35 sec** (695.2 seconds active-session wall), from `2026-11-26T16:54:30+00:00` to `2026-11-26T17:06:05.145622+00:00`. Approval wait: **0 seconds**; total elapsed **695.1 seconds**. File-provider waits, the interrupted import probe, the corrected verifier comparison, implementation, checks and reporting are included. No network acquisition occurred. Final receipt emission and chat rendering after the checkpoint are excluded.
