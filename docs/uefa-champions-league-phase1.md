# UEFA Champions League — Phase 1 source discovery and acquisition plan

Reviewed **2026-11-26**, original `toto` worktree, `feature/data-collection`, HEAD `878d45e47f1ef861b1b774ecc89c94af7851cb34`.

## Executive summary

**Phase 1 discovery/planning PASS; acquisition and Phase 2 execution require approval.** The strongest immediately practical combination is **FootballCSV for 1992/93–2015/16**, **OpenFootball for 2016/17–2025/26 main competition**, and **OpenFootball's separate 2024/25–2025/26 qualifying files**, with RSSSF for targeted structural/result corroboration and historical exceptions. Retain the five-season machine-source overlap for reconciliation, not extra coverage or assumed independent votes.

Pinned repository trees confirm candidate main-competition files spanning **all 34 target seasons**. This is **file availability, not 34 independently verified complete seasons**. Nine small representative files were inspected and preserved privately with provenance; no season-wide corpus, ingestion pipeline, normalized records, model run or application integration was created. The selected repositories leave **at least eight qualifying-season gaps, 2016/17–2023/24**. Qualification completeness in the other seasons still needs a full inventory. Licensed APIs and RSSSF are possible supplements, not confirmed replacements.

A central decision is the score basis. For the project's 1/X/2 purpose, **recommend 90 minutes including stoppage time, excluding extra time and shootouts**, while preserving all reported score components privately. This is a proposal requiring owner approval, not a change to existing datasets or policy. Original football dates, sufficiently supported historical administrative results and no administrative-publication-date filtering remain the retrospective review framework. Their interaction with a 90-minute target must be explicit for exceptional cases.

## Project inspection and scope

Read `AGENTS.md`, `README.md`, the historical collection/import documentation, the accelerated workflow and Turkish acquisition/standardization/independent-validation patterns. **`PROCESS.md` is absent** after a worktree-wide filename search; no substitute file was invented. The controlling process is [the existing five-phase workflow](accelerated-five-phase-workflow.md). The original application, prior work, environments and completed competitions remain protected. No other worktree was accessed.

Use the established exact canonical schema only in a later approved phase:

```csv
match_id,date,league,season,home_team,away_team,home_goals,away_goals
```

Existing conventions are consecutive `YYYY/YYYY` seasons, ISO football dates, source-supported names with whitespace normalization, full SHA-256 of compact UTF-8 JSON `[league,season,date,home_team,away_team]`, identity sorting, UTF-8/LF and ordinary CSV quoting. Scores, stage, leg or source identifiers must not be added to the shared match ID to conceal collisions. The eight columns cannot express score-period/status/stage uncertainty: retain those in private sidecar metadata and exclude unsupported records later.

Propose the canonical league label **`UEFA Champions League`**, with qualifying versus main scope retained in private stage metadata and separately reported coverage. This naming choice requires approval; it has not been added to the application or any dataset.

Primary scope is men's UEFA Champions League **1992/93–2025/26**, including qualifying/preliminary rounds and qualifying play-offs, reported separately from the main competition. Exclude Europa League, Conference League, Cup Winners' Cup, Super Cup, youth/women's competitions and 2026/27. The **1990/91 and 1991/92 European Cup** files/index entries are confirmed leads for a separately approved extension; they are outside the proposed acquisition list and were not sampled.

Proposed competition namespace is `data/private/europe/champions_league/`. Current metadata, samples and research notes are under `phase1_research/`; later acquisition would use immutable `phase1/originals/` plus exact references to the existing samples. Inventories, decisions, canonical CSV and detailed audits remain separate private artifacts. Git-ignored is not a claim of device-only storage: the existing worktree is iCloud-backed and storage policy was not changed.

## Source comparison and licensing matrix

| Candidate | Confirmed evidence and fields | Coverage / maintenance limit | Rights, independence and decision |
| --- | --- | --- | --- |
| [footballcsv/europe-champions-league](https://github.com/footballcsv/europe-champions-league/tree/66393c8dc5c86b459dc700a0ae3a0bd0abedb56e) | Complete pinned file index: 1955/56–2015/16; 24 target files. Four samples have explicit dates, directed teams, stage/round/group and separate `FT`, `HT`, `∑FT`, `ET`, `P`, comments. | Repository `pushed_at` 2020-04-12; no 2016/17+ files. Some early stage cells are blank, matchday labels unknown and leg labels inconsistent. File presence is not completeness. | Actual pinned `LICENSE.md` is CC0-1.0 for rights held; third-party clearance not warranted. Sparse source documentation; lineage to other compilations unestablished. Preferred early candidate, with a dedicated adapter. |
| [openfootball/champions-league](https://github.com/openfootball/champions-league/tree/abfaeddc2ee3d14f99ecc163c9ddb46cb4d67cef) | Complete pinned index: 15 main `cl.txt` files, 2011/12–2025/26; two `clq.txt` files, 2024/25–2025/26. Five samples contain dates, teams, results and stage headings. | `pushed_at` 2026-07-02. Qualifiers before 2024/25 are absent from this pin. Different competition files coexist. Scores require a period-aware grammar; update activity is not an accuracy guarantee. | Pinned CC0-1.0, with third-party-rights disclaimer. README/NOTES refer to Wikipedia and UEFA pages; these references neither authorize UEFA harvesting nor prove the record-level upstream. Preferred recent main candidate. |
| [RSSSF European Cups Archive](https://www.rsssf.org/ec/) | Index links for all 33 target seasons through 2024/25; eight era/season pages viewed. Qualifying and main sections, tie scores, aggregate/away-goal/ET/shootout and administrative notes are visible. | Early knockout grids can lack exact dates; later pages mix dated single matches with two-leg grids and round-date headings. A 2025/26 archive was not established. Index completeness is a publisher claim, not a fixture audit. | Page-specific author/copying grants were inspected, including [1992/93](https://www.rsssf.org/ec/ec199293.html) and [2024/25](https://www.rsssf.org/ec/ec202425.html). Recheck each prospective page's acknowledgement before preservation. Separately attributed compilation; fully disjoint upstreams unproven. Corroboration/targeted gap research. |
| [engsoccerdata `champs`](https://github.com/jalapic/engsoccerdata/tree/872c5c354161ace8408f3091b758c6af4cccca94) | Reused existing pinned README/DESCRIPTION/tree. Two small schema documents explicitly define `FT`, `hgoal`, `vgoal` at 90 minutes, with separate ET, penalties, tie totals and winner. A 797,540-byte CSV exists at the pin. | README claims 1955–2017; schema title says 1955–2016 and describes 6,554 rows/23 variables. These are documentation claims; the CSV was not downloaded or inventoried. Possible 2016/17 extension is unverified. | README's noncommercial attribution grant to James Curley and GPL package-code terms are distinct from complete upstream data clearance. No independent source vote against FootballCSV until lineage is established. Conditional alternative, not added speculatively to the primary plan. |
| [football-data.org API](https://www.football-data.org/coverage) | Provider lists Champions League and separate Champions League Qualification. [v4 score documentation](https://docs.football-data.org/general/v4/overtime.html) distinguishes `regularTime`, `duration`, ET and shootouts. | No authenticated coverage/match request was made; no season/stage is certified here. [Pricing](https://www.football-data.org/pricing) advertises a ten-season history package, not 34 seasons. Qualification entitlement may differ from the main CL offer. | [Registration terms](https://www.football-data.org/client/register) require a registered application/key, fair use and attribution and restrict post-cancellation service references. Obtain confirmation of archive retention, history, qualification and intended use. Different service from Football-Data.co.uk. No account, spend or contact authorized. |
| [API-Football](https://www.api-football.com/coverage) | CL appears on the coverage list. Provider [terms](https://www.api-football.com/terms) explicitly warn availability varies. | No season-specific authenticated coverage/fixture sample. Current docs are client-rendered; no verified period-field contract was extracted here. No historical season is marked confirmed. | Licensed account/subscription path; confirm historical years, qualifier inclusion, period semantics, raw-response retention and intended use before acquisition. No account, purchase or credential handling. |
| [Bert Kassies](https://kassiesa.net/uefa/data/method5/match2026.html) | Search results expose a potential 2025/26 stage/result corroboration lead. | Two initial direct page views returned **HTTP 403**; no archive/date/field/permission verification. | Access stopped; no retry, proxy, alternate client or scraping. Search-only leads cannot settle fixtures or establish independence. |
| [UEFA platforms](https://www.uefa.com/termsconditions/) | Policy-only inspection of §6.2. | **Excluded from automated acquisition.** | Terms restrict systematic database collection, automated scraping and software/model/AI-development use. No UEFA fixture page, hidden endpoint or controlled dataset was harvested. Public access or another repository's links do not grant permission. |

Both CC0 licenses were read at the exact repository pins. CC0 applies to rights held by the affirmer, with no third-party warranty; it does not make every publisher an independent source. Keep all acquired data private, preserve attribution and restrictions, and do not infer model-training or redistribution clearance from this assessment. No scraping workaround or paid API is part of the recommendation.

## Season-by-season coverage inventory

Evidence: **F** = exact file path/blob exists in a pinned, nontruncated repository tree; contents not fully inspected. **S** = bounded file sampled and aggregate observations counted. **I** = RSSSF index link; **I+V** = linked season page directly viewed for structure, not fully inventoried. **—** = no file at the pin / no established RSSSF index entry. **?** = qualifying/main split unverified. No row represents independently validated complete historical coverage.

CSV column is **qualifying / other-main observations** where sampled; `?/F` means one candidate CSV exists but its stage split is unverified. `8/74†` uses a provisional preliminary-versus-other split; early round eligibility needs approval. OpenFootball counts are scored fixture-description lines, not deduplicated accepted matches.

| Season | FootballCSV Q / main | OpenFootball main | OpenFootball qualifying | RSSSF | Principal limit |
| --- | --- | --- | --- | --- | --- |
| 1992/93 | S 8 / 74† | — | — | I+V | Early scope, leg labels, award/replay |
| 1993/94 | ? / F | — | — | I | Early pre-group scope; dates unverified |
| 1994/95 | ? / F | — | — | I+V | 16-club group era |
| 1995/96 | ? / F | — | — | I | Uninspected stage/date completeness |
| 1996/97 | ? / F | — | — | I | Uninspected stage/date completeness |
| 1997/98 | ? / F | — | — | I+V | 24-club group era |
| 1998/99 | ? / F | — | — | I | Uninspected stage/date completeness |
| 1999/00 | S 78 / 157 | — | — | I+V | Two group phases sampled |
| 2000/01 | ? / F | — | — | I | Two group phases |
| 2001/02 | ? / F | — | — | I | Two group phases |
| 2002/03 | ? / F | — | — | I+V | Two group phases |
| 2003/04 | ? / F | — | — | I+V | Round-of-16 era |
| 2004/05 | ? / F | — | — | I | Uninspected stage/date completeness |
| 2005/06 | ? / F | — | — | I | Uninspected stage/date completeness |
| 2006/07 | ? / F | — | — | I | Uninspected stage/date completeness |
| 2007/08 | ? / F | — | — | I | Uninspected stage/date completeness |
| 2008/09 | ? / F | — | — | I | Uninspected stage/date completeness |
| 2009/10 | ? / F | — | — | I | Uninspected stage/date completeness |
| 2010/11 | ? / F | — | — | I | Uninspected stage/date completeness |
| 2011/12 | ? / F | S 125 | — | I | Main-only OF sample; CSV overlap |
| 2012/13 | ? / F | F | — | I | Five-season overlap |
| 2013/14 | S 88 / 125 | F | — | I | FT/ET separation sampled |
| 2014/15 | ? / F | F | — | I | Five-season overlap |
| 2015/16 | S 92 / 125 | F | — | I | June qualifying date; shootouts |
| 2016/17 | — | F | — | I | Qualifying gap in selected machine files |
| 2017/18 | — | F | — | I | Qualifying gap in selected machine files |
| 2018/19 | — | F | — | I | Qualifying gap in selected machine files |
| 2019/20 | — | S 119 | — | I+V | COVID extension/single-leg finish |
| 2020/21 | — | F | — | I | Qualifying gap; COVID format exceptions |
| 2021/22 | — | F | — | I | Qualifying gap in selected machine files |
| 2022/23 | — | F | — | I | Qualifying gap in selected machine files |
| 2023/24 | — | F | — | I | Qualifying gap in selected machine files |
| 2024/25 | — | F; H 189 | S 90 | I+V | H189 is publisher header only |
| 2025/26 | — | S 189 | S 92 | — | No RSSSF archive established |

**H 189** is the publisher's inspected 2024/25 main-file header, not an independently counted total in that unsaved web view. The 2025/26 preserved sample has 189 scored lines matching its declared 144 league + 16 knockout play-off + 29 final-stage split; its qualifiers separately have 92 scored lines. This completed target season is not the ongoing 2026/27 stream. The 2019/20 main sample has 119 scored lines and ends on 23 August 2020. None of these counts certifies dates/results, unique event identities or historical eligibility.

The selected machine-file union spans all 34 main-season candidates: 24 CSV + 15 TXT − 5 overlapping seasons. Qualifying files/sections remain unestablished for at least 2016/17–2023/24; other unsampled CSVs may reveal further gaps. RSSSF links cover 33 target seasons, but exact dates and 90-minute values cannot be assumed from a round heading or an after-ET tie grid. Licensed API access is **unverified for every season** in this matrix. No estimate is added as a fabricated fixture.

## Qualification, main competition and format boundaries

Preserve original stage names and add reviewed private taxonomy: preliminary qualifying, qualifying rounds, qualifying play-offs, pre-group knockout rounds, first/second group stage, league phase, main knockout play-offs, round of 16, quarterfinal, semifinal and final; retain group, leg, tie and neutral-venue fields separately. **February knockout play-offs after the league phase are main competition; August qualifying play-offs are qualification.** Never identify scope by the word “playoff” alone or by dates alone.

Early 1992/93–1993/94 files describe rounds before the branded group phase. Recommend preliminary rounds as qualifying and named first/second knockout rounds as separately labelled pre-group main competition, pending owner approval. Do not silently use modern “group stage onward” statistical scope or retroactively recode all those rounds as qualifying. The early European Cup extension remains separate.

Illustrative format gates, to confirm season by season in Phase 2: early two-group formats; four groups of four from 1994/95; six groups of four from 1997/98; eight first groups plus four second groups in 1999/00–2002/03; eight groups then round of 16 from 2003/04; the 2019/20 COVID exception; and the 36-club league phase from 2024/25. For the latter, 36 × 8 / 2 = 144 league fixtures, plus 16 main knockout play-off fixtures and 29 later knockout fixtures. These are diagnostic expectations, never substitute records. Keep Group A in the first phase distinct from Group A in a second phase. Retain actual single-leg/replay exceptions and qualifying champions/non-champions paths.

Qualification can start in June: the 2015/16 CSV sample begins **30 June 2015**. Existing domestic July-to-June wrappers would wrongly reject that observation. The COVID main competition runs into August 2020. Use source-declared season and stage-specific, evidence-bound date windows; do not change the shared importer or assign seasons from dates alone. Neutral-site finals and relocated games retain source-designated home/away order without claiming actual home advantage.

## Score semantics, discrepancies and remaining risks

- **FootballCSV:** sampled extra-time cases separate a 90-minute-looking `FT` from cumulative `ET`, penalties `P` and aggregate `∑FT`. Existing engsoccerdata schema documents independently specify FT/goal columns at 90 minutes, but do not prove common lineage or every CSV field's correctness. Validate the source-specific interpretation on preserved cases before any conversion. Never select `ET`, tie aggregates or tie winners as 90-minute scores.
- **OpenFootball:** observed shootout tallies can precede `pen.`, followed by an `a.e.t.` score and parenthesized period values. The first score pair is unsafe. Identify named periods with a tested, source-bound grammar and corroborated cases; an absent/ambiguous 90-minute component stays unknown. Do not assume a single parenthesized pair always has the same meaning, or copy an unverified parser from another project.
- **APIs:** `fullTime` is not a cross-provider 90-minute contract. Football-data.org explicitly supplies `regularTime`; its documented shootout example even folds penalties into `fullTime`. Check duration, cumulative versus incremental ET, null fields, API version and finality. Penalty goals never become football goals; the advancing team is not necessarily the winner at 90 minutes.
- **RSSSF:** distinguish a match result from a two-leg aggregate; reverse home/away correctly for return legs. Preserve away-goal, ET, penalties, awarded/abandoned and replay notes. Nominal round dates and date ranges do not independently certify every fixture's kickoff date.
- **Observed source issues:** the 1992/93 preliminary sample has six “Leg 1” labels and two “Leg 2” labels across eight descriptions, including two apparent later-leg label inconsistencies. The publisher's pinned NOTES also documents a wrong-year date correction in an unsampled season. These are bounded review leads, not corrections applied here. The 1992/93 award/replay context is a Phase 3 historical case. Do not suppress an entire competition for traceable issues that can be isolated.
- **Names and dates:** CSV labels embed association and parenthesized sequence annotations; some matchday labels are `?`. TXT labels use different country codes, accents, abbreviations and sponsor names. Keep raw labels and source/season-bound, injective club correspondences. Never merge clubs by city alone. Use explicit day/month/year with weekday checks; source week annotations are not an exact-date substitute. Preserve UTC/local-date and kickoff/completion distinctions when those fields exist.
- **Status:** preserve completed, scheduled/postponed, suspended/abandoned, replayed, awarded and no-kickoff descriptions separately. A future inventory is not an adjudication. Later dispositions remain INCLUDE / HOLD OUT / NOT PLAYED / OUT OF SCOPE; missing seasons are gaps, not NOT PLAYED events. No match decision or invented date/score was made in Phase 1.

## Recommended acquisition and verification approach

The proposed immutable input list contains **41 CC0 files, 701,486 bytes at the pins**: 24 FootballCSV seasons, 15 OpenFootball main seasons and two OpenFootball qualifying seasons. Nine representative files are already privately preserved; **32 remaining files / 562,642 bytes** would need separately approved bounded acquisition. Their exact URLs, Git blob IDs, byte limits, season/scope, license references and existing-sample references are in the private `proposed_acquisition_plan.v2.json`. It is explicitly **DRAFT / not executable without approval**. No archive ZIP, clone, speculative full engsoccerdata export or RSSSF season crawl was performed.

Recheck the pinned license and plan, make one bounded request per approved missing file with light pacing, stop on denial/redirect/rate restriction, and use verified cache replay for existing originals. Save exact raw bytes and immutable receipts with URL/final URL, publisher, retrieval UTC, bytes, SHA-256, commit/blob, encoding, rights and permission reference. Preserve failures/stop records; never overwrite an original. Reference the nine sample originals in place without downloading or manufacturing duplicate originals. Distinguish a cache/tool fetch failure from verified access or verified absence.

Use RSSSF initially for the sampled era/exception contexts and expand only to necessary, permission-checked pages. Its separate compilation is useful corroboration; unknown upstream overlap remains disclosed. For eight qualifying gaps, request a provider's season/stage inventory and explicit retained-archive/intended-use terms before any authenticated match sample or purchase. If a permitted source cannot establish exact dates/90-minute scores, retain documented gaps. No messages to providers were sent.

Keep a private source dependency graph, input hashes and source-specific corrections/quarantines. Ordinary fixtures can later receive structural and overlap validation without extensive manual research; thoroughly research material score/date/identity/status anomalies. Independent code must reconstruct observations/fields from originals with a separate parser, not validate an inventory solely against itself. Historical source independence and code independence are separate claims.

## Concrete Phase 2 implementation plan — not implemented

1. **Input prerequisite:** approve and complete the bounded Phase 1 acquisition list, verify every receipt/blob/license, then freeze the corpus and stage/score-policy configuration. This planning-only Phase 1 does not authorize bulk completion or Phase 2 execution.
2. **Minimal adapters:** reuse existing acquisition/hash/blob/overwrite helpers by import with a UCL-scoped allowlist/private root. Add only strict FootballCSV and period-aware Football.TXT inventory adapters; use RSSSF-specific parsing only for approved pages. Reuse shared schema/serialization in Phase 4, not as an excuse to discard stage/score metadata now. Domestic regular-pair validators and ordinary-score parsers are not suitable unchanged.
3. **Private observation inventory:** retain every original field, physical CSV row or TXT line/span and SHA-256, raw/normalized season/stage/round/group/path/leg, names/associations, date precision, status, 90-minute/after-ET/ET-only/penalty/aggregate components and parse uncertainties. Emit one inventory, one coverage matrix, overlap assessment and deduplicated anomaly queue; no canonical output or INCLUDE decisions in Phase 2.
4. **Independent reconciliation:** independently parse originals and reconcile exact fixture identities across the five overlap seasons, qualifiers/main boundaries and source-bound club correspondences. Compare 90 minutes with 90 minutes, never with a tie aggregate or ET result. Account for each representation once; preserve separate legitimate rematches and source conflicts.
5. **Focused safeguards:** test UTF-8/CSV width and quoted fields, decorated dates and blank stages, two group phases, June qualification/August COVID boundaries, both play-off meanings, reversed return legs, neutral finals, replay/award descriptions, score-period/shootout ambiguity, changed bytes, missing dates, aliases/collisions and unresolved isolation. Counts derive from the season's actual format; no universal double round robin. Reproduce inventory and independent reports offline and run relevant regressions. Reserve the complete suite for finalization.
6. **Acceptance/stop:** account for every acquired observation and season/stage gap, preserve all originals, contain conflicts and verify independent reconciliation; then issue the short Phase 2 report and stop for approval. Systemic/unbounded integrity, provenance or privacy failures block; isolated uncertain cases remain quarantined. No automatic historical adjudication, standardization, prediction changes or advancement.

## Explicit decisions requiring owner approval

- Approve the 34-season primary scope and league label `UEFA Champions League`, **qualification and main competition separately**, and keep 1990/91–1991/92 as a separate extension.
- Approve the proposed **90-minute score basis** and private preservation of ET/shootout/aggregate components. Set the rule for administrative outcomes versus observed regulation-time scores in Phase 3; do not silently mix bases.
- Approve the early pre-group round classification described above and preserve source labels where scope remains uncertain.
- Approve the 41-file pinned input plan, referencing nine existing samples and acquiring only 32 further files; authorize no UEFA scrape, API account/purchase or archive-wide RSSSF acquisition.
- Choose whether to pursue explicitly licensed qualifying-gap recovery or accept bounded gaps while proceeding with unaffected main-competition coverage. No provider contact or expenditure is implied.
- After input freezing, separately authorize Phase 2's minimal adapters, inventory and independent validation. No generic framework, new dependency or shared application/schema change is needed.

## Verification, preservation and stop

Research preservation is **14 metadata/schema originals plus nine representative fixture files: 23 originals, 215,854 bytes**, each with URL, UTC timestamp, SHA-256 and immutable receipt. Metadata includes both nontruncated repository trees and exact CC0 licenses; the two small engsoccerdata schema files use the existing project pin/permission context. These samples are not the 41-file corpus. Detailed source fields and sample exceptions remain private. Web-only RSSSF/API/terms inspections are short factual notes with URLs/access limitations, not claims of preserved full-page originals or offline re-authentication of live sites.

No public script or ingestion test was added. Focused checks verify the metadata/sample receipts and Git blobs offline, recompute the 34-row file inventory from preserved trees, check the proposed 41-file bounds and sample counts, and inspect report links/privacy. A first research summary compared decorated date strings lexicographically; a preserved v2 corrects diagnostic chronological bounds only. Originals and match records were not changed. Existing acquisition safeguard tests are reused; no full-suite, training or backtest run is necessary.

The baseline contains **2,258 existing entries, including 1,934 private files**, all prior competition artifacts/application code, dirty files, planning history, Git index/config and environment configuration. Git objects, caches and installed package bytes are outside the exhaustive content-hash scope. Existing `.DS_Store` files are preserved. Final focused-check and preservation outcomes, exact hashes and measured time are recorded below and privately. No package installation, original environment change, dataset edit, branch/worktree switch, staging, commit or push occurred.

**STOP after Phase 1. Await review and explicit approval of the scope, score policy and acquisition plan.**

Final checkpoint: **12 existing acquisition safeguard tests passed** (0.028 seconds reported test execution), all 23 original/receipt pairs and pinned blobs verified offline with **zero requests**, all 34 matrix rows and the 41-file proposed bounds checked, and all **2,258 protected entries / 1,934 prior private files** matched freshly. The only public changes are this report and append-only `PLANNING_LOG.md`; all research bytes/notes remain ignored and untracked. HEAD, branch, index and Git configuration matched. No full suite or Phase 2 work was performed.

Measured Phase 1 execution: **15 min 44 sec** (944.1 seconds active-session wall), from `2026-11-26T20:53:28+00:00` to `2026-11-26T21:09:12.021029+00:00`. Approval wait: **0 seconds**; total elapsed **944.0 seconds**. Tool/file-provider/network waits, the corrected date-bound diagnostic, research, limited sample acquisition and verification are included. Successfully measured acquisition request durations sum to **10.16 seconds**, already included in wall time; web-search waits were not separately instrumented. Receipt emission and final chat after this checkpoint are excluded.

**Phase 1 discovery/planning is ready for review. STOP; no acquisition-plan execution or Phase 2 without explicit approval.**
