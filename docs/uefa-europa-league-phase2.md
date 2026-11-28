# UEFA Cup / Europa League — Phase 2 inventory and structural validation

2026-11-27. **CONDITIONAL PASS** for inventory and review preparation. Phase 1 is the accepted acquisition baseline. Phase 3 requires explicit owner approval. No final historical adjudication, canonical dataset, production import, model or application change was performed.

## A. Outcome and scope

All 36 seasons, 1990/91–2025/26, were processed across five publishers. All 75 accepted Phase 1 payloads (44,222,060 bytes), including all 58 fixture-bearing files, were verified. Ten targeted Wikipedia revision payloads add 748,360 bytes, bringing the input freeze to 85 payloads and 68 declared fixture-bearing files. Original bytes, retrieval receipts, hashes, permission evidence and source locators remain private.

The inventory contains **38,126 observations**: 35,369 direct fixture observations and 2,757 auxiliary goal-log fixture contexts representing 8,016 raw goal rows. Conditional reconciliation produces **12,311 events**: 6,676 main competition, 5,438 qualifying and 197 unresolved scope. These are candidates, not certified unique or played matches. There are 11,275 multi-publisher and 1,036 single-publisher events; shared upstream provenance has not been established, so publisher agreement is not proof of independence.

## B. Processing and reconciliation

Source-specific adapters processed RSSSF target competition sections and detail reports, OpenFootball text, the 11footy relational ZIP, Schoch Parquet and goal CSV, and pinned Wikipedia revision text. Observation counts: RSSSF 12,600; OpenFootball 979 (including two unscored descriptions); 11footy 8,467; Schoch 14,011; Wikipedia 2,069. ZIP CRCs and joins were checked; 224 records for 2026/27 were excluded from scope. Eighteen Parquet display-name gaps retain original nulls and source-identifier recovery evidence.

Every observation has an original-payload hash and record locator. Source accounting distinguishes 138 non-event records: 135 scored contextual descriptions (including a historical played-score note), two no-play tie descriptions without leg results, and one acquired detail page concerning the Champions League alone. Standings, aggregate columns, goal progressions and non-target competitions are not silently converted to fixtures. Four original Wikipedia root pages expose unexpanded transclusions; targeted supplements address these dependencies where acquired.

Season-specific identity normalization keeps geographic distinctions. There are 3,449 conditional identity correspondences and 258 unresolved identity candidates. Correspondences require opponent/date evidence over two distinct fixture dates, or a narrowly supported core-name correspondence on one date; provider-ID collisions are prohibited. Separate files from one publisher can establish textual correspondence but do not establish independent corroboration. Two-leg topology can supply auxiliary correspondence evidence. No global legal club identity was adjudicated.

Events retain all contributing observations, original orientation, dates, stage labels and competing period-specific score claims. Exact-date grouping is preferred; conservative unique stage/leg/schedule correspondences retain explicit uncertainty. Replays and rematches remain distinct. Schoch candidate-season reassignment, including August 2020, requires other-source evidence and preserves the original date. Reconciliation adds 25,815 contributor links rather than asserting that all repeated descriptions are redundant. Twelve duplicate candidates remain explicitly queued.

Regulation, half-time, cumulative after-extra-time, extra-time-only, shootout, aggregate, published and administrative scores have separate fields. Schoch E is cumulative after extra time; P remains unsplit. Goal-running totals are not final scores. Provider no-extra-time flags are source claims, not final historical truth. An extra-time claim opposed by an ordinary-duration claim makes regulation unresolved even if printed scores agree. No 90-minute score is derived by subtracting unverified values. Numeric source-supported regulation counts can overlap unresolved cases; they do not establish modelling eligibility.

## C. Coverage and competition structures

The detailed private CSV includes source records, stages, overlap, dates, scores, identity, venue and tie diagnostics for every season. Main-slot expectations below are format diagnostics, **not independently verified played totals**. Expected qualifying totals remain UNKNOWN. Conditional excesses or deficits can reflect unresolved identity, duplication, scope, no-play slots or actual gaps.

The four early seasons have independently checked target first-round brackets of 32 ties / 64 clubs and no preceding target qualifying stage in the acquired bracket. Qualifying is therefore not applicable for 1990/91–1993/94, rather than recorded as a failed download. Evidence: [1990/91](https://www.rsssf.org/ec/ec199091.html), [1991/92](https://www.rsssf.org/ec/ec199192.html), [1992/93](https://www.rsssf.org/ec/ec199293.html), [1993/94](https://www.rsssf.org/ec/ec199394.html), with pinned Wikipedia cross-checks. This finding does not certify every reconciled event.

Era checks distinguish two-leg finals through 1996/97, single-match finals thereafter, 8×5 single-round groups in 2004–08, 12×4 double-round groups in 2009–20, 8×4 groups plus knockout playoffs in 2021–23, and the 36-club league phase in 2024 onward. The two recent league phases independently contain 144 games, 36 teams and eight appearances per team, four home and four away. Their main competition candidate totals are 189 each. Incoming eliminated Champions League clubs are counted only in target brackets; their former-competition fixtures are excluded. Earlier entry mechanisms remain source-specific rather than assuming present rules.

COVID exceptions include the two source-annotated single-leg 2019/20 round-of-16 ties, single-leg quarterfinals/semifinals, and all single-leg 2020/21 qualifying rounds including playoffs. Withdrawals, byes, administrative results and no-play descriptions remain linked context or exceptional candidates. No return match is invented from a two-leg expectation.

Targeted acquisition added three early structure pages and missing 2000/01 and 2002/03 transclusions: 1,273 observations, contributors to 902 conditional events, six supplemental-only events and six events whose sole exact-date source is supplemental. Wikipedia then returned HTTP 429; acquisition stopped without retries or circumvention. Remaining dependencies use acquired alternative publishers and remain visible as coverage limitations. No broad discovery restart occurred.

| Season | Main candidates | Qualifying candidates | Unknown scope | Main format slots | Review cases |
|---|---:|---:|---:|---:|---:|
| 1990/1991 | 144 | 0 | 0 | 126 | 82 |
| 1991/1992 | 140 | 0 | 0 | 126 | 62 |
| 1992/1993 | 132 | 0 | 0 | 126 | 21 |
| 1993/1994 | 132 | 0 | 0 | 126 | 34 |
| 1994/1995 | 132 | 60 | 3 | 126 | 57 |
| 1995/1996 | 126 | 68 | 10 | 126 | 35 |
| 1996/1997 | 126 | 124 | 28 | 126 | 85 |
| 1997/1998 | 125 | 94 | 31 | 125 | 94 |
| 1998/1999 | 125 | 98 | 12 | 125 | 53 |
| 1999/2000 | 205 | 76 | 34 | 205 | 84 |
| 2000/2001 | 213 | 85 | 2 | 205 | 62 |
| 2001/2002 | 224 | 96 | 15 | 205 | 124 |
| 2002/2003 | 222 | 94 | 1 | 205 | 66 |
| 2003/2004 | 211 | 94 | 7 | 205 | 58 |
| 2004/2005 | 237 | 131 | 0 | 221 | 53 |
| 2005/2006 | 235 | 125 | 5 | 221 | 77 |
| 2006/2007 | 226 | 140 | 5 | 221 | 39 |
| 2007/2008 | 229 | 150 | 2 | 221 | 37 |
| 2008/2009 | 226 | 175 | 0 | 221 | 68 |
| 2009/2010 | 205 | 288 | 5 | 205 | 63 |
| 2010/2011 | 205 | 296 | 0 | 205 | 53 |
| 2011/2012 | 206 | 307 | 0 | 205 | 55 |
| 2012/2013 | 210 | 288 | 18 | 205 | 80 |
| 2013/2014 | 205 | 295 | 13 | 205 | 80 |
| 2014/2015 | 206 | 298 | 0 | 205 | 36 |
| 2015/2016 | 207 | 283 | 0 | 205 | 28 |
| 2016/2017 | 205 | 286 | 0 | 205 | 36 |
| 2017/2018 | 205 | 292 | 0 | 205 | 34 |
| 2018/2019 | 205 | 331 | 0 | 205 | 26 |
| 2019/2020 | 197 | 337 | 0 | 197 | 47 |
| 2020/2021 | 207 | 249 | 6 | 205 | 109 |
| 2021/2022 | 141 | 40 | 0 | 141 | 11 |
| 2022/2023 | 143 | 40 | 0 | 141 | 16 |
| 2023/2024 | 141 | 34 | 0 | 141 | 5 |
| 2024/2025 | 189 | 80 | 0 | 189 | 14 |
| 2025/2026 | 189 | 84 | 0 | 189 | 12 |

All seasons retain some investigation needs; the matrix is not a complete-coverage certificate. In particular 2025/26 qualifying has 84 conditional events against 82 in one source, requiring reconciliation rather than treating the larger count as verified coverage.

## D. Data quality and historical review

There are **1,896 review cases**: priority 1: 763; priority 2: 1,082; priority 3: 51. Cases may carry multiple issue codes. Each event case links original observations, competing evidence, materiality and an investigation path; identity, topology and contextual exceptions have separate evidence-bearing cases. No INCLUDE/HOLD_OUT dispositions are assigned.

| Issue | Cases / events |
|---|---:|
| AMBIGUOUS_DUPLICATE_CANDIDATE | 12 |
| DATE_CONFLICT | 281 |
| DATE_UNRESOLVED | 726 |
| DURATION_CONFLICT | 146 |
| EXCEPTIONAL_STATUS | 33 |
| HISTORICAL_SCORE_CONTEXT | 1 |
| NONPLAYED_TIE_WITHOUT_LEG_RESULTS | 2 |
| REGULATION_SCORE_UNRESOLVED | 952 |
| SCORE_CONFLICT_HALF_TIME | 3 |
| SCORE_CONFLICT_REGULATION_TIME | 65 |
| SOURCE_LEG_OR_SCHEDULE_CONFLICT | 19 |
| SOURCE_ORIENTATION_CONFLICT | 7 |
| STAGE_CONFLICT | 1 |
| STAGE_UNRESOLVED | 243 |
| TIE_TOPOLOGY_COVERAGE_CANDIDATE | 56 |
| UNRESOLVED_TEAM_IDENTITY_CANDIDATE | 258 |
| VENUE_REVIEW | 51 |

Sixty-five events have competing numeric regulation scores; 33 change the 1/X/2 result class. Another 146 have opposing duration claims. There are 952 regulation-unresolved events, 281 conflicting-date events and 726 undated events. Round schedule intervals are not fabricated exact dates. Season membership and date roles remain explicit.

Material cases include a played-score note attached to an administratively changed tie, awards without recoverable on-pitch leg scores, unsplit shootout totals, geographically ambiguous club names, reversed orientations and mismatched leg schedules. The original played-score context is retained separately and not promoted to a new event without investigation. Source-declared neutral venues and single-final format candidates generate 51 venue reviews; neither a relocation nor single-leg format automatically proves official neutrality. Fifty-six tie-topology cases identify possible missing returns, duplicates or stage/identity problems, rather than declaring 56 missing matches. Named source evidence stays in the private queue to avoid publishing restricted source rows.

## E. Artifacts, validation and preservation

Private deliverables under `data/private/europe/europa_league/phase2/validated/`:

- `source_inventory.json`: source files, parser accounting, observations, original labels, statuses and locators.
- `event_inventory.json`: conditional source-event membership and competing dates, stages, scores and duration claims.
- `team_identity_inventory.json`: original labels, seasonal correspondences, evidence and unresolved candidates.
- `structural_validation.json`: season structures, expected format slots and source-backed diagnostics.
- `overlap_assessment.json`: publisher overlap, duplicate candidates and independence limitations.
- `score_semantics_exceptions.json`: period-aware score exceptions, contextual/no-play records and venue/status evidence through linked observations.
- `date_exceptions.json`: source dates, intervals, conflicts and justified candidate-season changes.
- `season_coverage.csv`: all 36 seasons and detailed stage/quality coverage columns.
- `review_queue.json`: prioritized investigation cases without historical dispositions.
- `input_freeze.json` and `summary.json`: immutable input bindings and machine-readable totals.

Acquisition receipts, the supplemental frozen plan and copied original permission evidence reside in `supplemental/`; original Phase 1 manifests and attribution remain authoritative. The input freeze binds all 85 payload paths, sizes, URLs and SHA-256 values. Independent validation, offline reproduction and preservation receipts are adjacent to `validated/`. Earlier attempts are segregated under `attempts/` and are not accepted results.

The independent verifier reads original bytes using separately implemented record checks, without importing the production parser, alias or event-ID functions. It verifies structured records, text/wiki boundaries, RSSSF physical line/name/leg accounting, every membership and correspondence, score projections, early brackets, recent league-phase topology and coverage counts. Adverse tests cover changed names, scores, dates, locators, omitted legs/membership, tampering and standings incorrectly treated as fixtures. This is structural independence, not new historical research or proven upstream publisher independence.

A separate fresh-process, network-disabled reproduction reparses originals without a cache and requires all eleven deterministic output files to match byte-for-byte. Focused acquisition, inventory, Champions League, schema, source-validation and audit regression tests pass **210 tests**. The final independent verifier reports PASS for all 85 original payloads, all 38,126 observations and all 3,449 conditional identity correspondences. The fresh offline reproduction reports PASS for all eleven byte-identical artifacts. Machine receipts record both outcomes and hashes.

Preservation checks compare all 526 pre-existing fingerprints: 525 files must remain byte-identical, with the original planning-log prefix retained and only append entries added. Accepted Phase 1 originals and receipts remain unchanged. No staged changes, commits, pushes, production imports or unrelated-worktree changes are authorized. Existing private domestic and Champions League archives are absent in this worktree; their bytes and private-data-dependent validations cannot be certified, and no archive was copied from another worktree. Available public samples and relevant code are covered by preservation and focused regressions.

Raw and derived source data stay under ignored `data/private/`; public code/tests use synthetic fixtures and this report publishes aggregate findings. Source-specific CC0, ODC-By, acknowledgement, CC BY-NC and CC BY-SA restrictions remain recorded; acquisition does not grant new training, redistribution or downstream publication rights. The workspace is iCloud-backed, so “private” does not mean device-only. Source reads use read-only memory mapping to handle local cloud-file buffering without modifying originals or bypassing hashes.

New public files: this report; `scripts/uefa_europa_league_sources.py`; `scripts/inventory_uefa_europa_league.py`; `scripts/verify_uefa_europa_league_inventory.py`; `tests/test_uefa_europa_league_inventory.py`. `PLANNING_LOG.md` is append-only. Existing uncommitted Phase 1 files remain preserved. No dependencies were installed or configuration changed.

## F. Phase 3 readiness

The source inventory, immutable lineage, full observation membership, score-period separation and mechanically checked brackets are ready to support historical adjudication. The remaining identity, duration, regulation, date, orientation, stage, exceptional-status, neutrality and coverage cases require individual investigation. There is no identified blocker to beginning that review; there is a material blocker to calling the inventory complete or generating production/model-ready rows now.

**Owner decision required: approve starting Phase 3.** No approval of a score, club merge, date, neutral designation or inclusion decision is implied by accepting this Phase 2 inventory. Phase 3 has not started.
