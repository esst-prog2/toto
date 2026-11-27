# UEFA Champions League — Phase 2 inventory and structural validation

**PASS with isolated unresolved observations and documented gaps.** Owner-authorized Phase 2 only, 2026-11-26, original `toto` worktree on `feature/data-collection`. No historical dispositions, source corrections, canonical records, model integration or training were produced. No staging, commit or push.

## Accepted method and domestic audit preservation

The accepted domestic retrospective report and all 16 supporting audit files were copied byte-for-byte to `data/private/audits/domestic_score_period/2026-11-26/`, with a new checksum manifest; temporary originals remain untouched. [Public aggregate summary](domestic-score-period-audit.md) and [PROCESS.md](../PROCESS.md) record the owner-approved regulation-time requirement. Existing domestic datasets, scope exclusions and retrospective administrative-result policy remain unchanged.

Model-eligible played matches require supported 90-minute-plus-stoppage-time scores. Preserve extra-time, shootout and aggregate components separately; an ambiguous period remains unknown. The administrative-result exception retains original football dates and supported accepted historical outcomes without administrative-publication-date filtering; distinguish it from observed regulation scores. Phase 2 assigns no model eligibility.

The owner confirmed **recent-first priorities, numerical weights unspecified**. Acquisition proceeded from recent files to older ones; all 34 seasons receive exact unweighted accounting. No decay coefficients or weighted completeness percentage were invented.

## Bounded acquisition and permissions

The [Phase 1 plan](uefa-champions-league-phase1.md) is completed: **41 fixture originals, 701,486 bytes**. Nine prior samples are referenced in place; **32 new files / 562,642 bytes** were downloaded. There are 24 FootballCSV season files, 15 OpenFootball main files and two separate OpenFootball qualifying files. The 14 earlier metadata/schema originals remain frozen, giving 55 distinct original paths / 778,496 bytes including all fixture inputs. Two existing license originals/receipts were copied into the new acquisition execution area; these are permission references, not additional downloads.

| Source | Frozen revision | Acquired coverage | Permission/independence limit |
|---|---|---|---|
| FootballCSV `europe-champions-league` | `66393c8dc5c86b459dc700a0ae3a0bd0abedb56e` | 24 seasons, 1992/93–2015/16, qualifying and main descriptions | Pinned CC0 for rights held; upstream separation and complete third-party clearance unestablished |
| OpenFootball `champions-league` | `abfaeddc2ee3d14f99ecc163c9ddb46cb4d67cef` | 15 main seasons, 2011/12–2025/26; qualifying 2024/25–2025/26 | Same CC0 limitation; repository agreement is not an independent source vote |

All inputs have URLs, UTC retrieval timestamps, SHA-256, exact sizes and expected Git blob checks; original receipt bytes are retained. The immutable acquisition manifest maps every actual path to the approved plan path. Additional downloads use `phase2/acquisition/originals/`; the nine samples remain under `phase1_research/samples/`.

The first sandbox attempt failed DNS resolution before a source responded. Its stop receipt was retained. A separately scoped direct-network execution used the same approved URLs/pins/limits and existing no-redirect/denial/overwrite safeguards. There was no server restriction retry or source expansion.

No new RSSSF fixture pages, engsoccerdata corpus, API data or UEFA-controlled content were acquired. RSSSF supplements require page-specific permission and a bounded plan; licensed APIs require entitlement/retention/use approval; the prior Kassies 403 stop remains. UEFA harvesting, European Cup extension and 2026/27 remain excluded. Raw/derived datasets, receipts, registries and detailed evidence stay ignored/private. No training or redistribution clearance is inferred.

## Inventory and independent reconciliation

**6,578 source observations** comprise **4,399 CSV** and **2,179 TXT** descriptions. A complete source locator includes file SHA-256, physical row/line span and its SHA-256, with separate date/stage heading locators. All original fields, annotations, directed names/associations, season, stage, group, source leg/replay labels and period values remain available privately. Source names are not silently replaced by global aliases.

**625 conditional overlap links** across 2011/12–2015/16 reconcile the population to **5,953 conditional events**: **4,127 main** descriptions, including one explicitly described replay, and **1,826 qualifying** descriptions. Overlap does not create extra coverage. All 6,578 observations belong to exactly one conditional event; all 5,953 have one primary-source representation. There are zero exact duplicate fixture groups within a source. The 1992/93 replay is a legitimate separate description for historical review, not a duplicate automatically discarded.

The independent validator imports no production acquisition/parser/stage/period/naming/ID helpers. It reads original bytes, verifies receipts/blobs/permissions, reconstructs every retained raw and semantic field and physical locator, independently derives season-bound club correspondences and event links, and checks full population accounting. Primary counts and detailed main-stage expectations were independently checked for all 34 seasons. All 17 TXT publisher match headers also match independently counted physical fixture lines.

Across the 625 overlaps: **all dates agree**; **624 comparable regulation pairs agree**, with one unresolved TXT period not compared as a regulation score. There are **two halftime conflicts**, **three source-designated final orientation differences**, and **no comparable regulation/after-extra-time/shootout conflicts**. Scores are reversed only for comparison when the independently linked final descriptions designate opposite home/away order; raw order is unchanged. Final venue/home-advantage meaning is not inferred. Source-specific names remain conditional structural correspondences, not approved legal club-identity mergers.

FootballCSV's dedicated `FT` and cumulative `ET` fields are treated separately using
the inspected source-specific convention, rather than a universal interpretation
of the word full-time. Ten overlapping after-extra-time component comparisons and
six shootout comparisons agree with the explicit TXT period syntax. This checks
the field interpretation; it does not establish disjoint historical upstreams.
An unreported extra-time-only component stays null; it is not substituted for the
cumulative after-extra-time result or used to reconstruct an absent regulation score.

## Season/stage coverage

Counts below are primary-source descriptions, not final INCLUDE totals or model-eligible fixtures. CSV is primary through 2015/16; TXT is primary thereafter. The five-season overlap is additional comparator evidence. Q = qualifying/preliminary/qualifying play-offs, separately from main. The early first/second knockout rounds are preserved as pre-group main stages; no official-stage descriptions were removed because of branding terminology.

| Season | Main descriptions | Nominal main format | Qualifying descriptions | Regulation score unknown in primary | Note |
|---|---:|---:|---:|---:|---|
| 1992/93 | 74 | 73 | 8 | 0 | 73 nominal +1 replay; source leg-label/tie context review |
| 1993/94 | 75 | 75 | 20 | 0 | Two groups; single-leg semifinals; pre-group rounds retained |
| 1994/95 | 61 | 61 | 16 | 0 | Observed qualifying ties structurally accounted; external completeness unproven |
| 1995/96 | 61 | 61 | 16 | 0 | Observed qualifying ties structurally accounted; external completeness unproven |
| 1996/97 | 61 | 61 | 16 | 0 | Observed qualifying ties structurally accounted; external completeness unproven |
| 1997/98 | 85 | 85 | 62 | 0 | Observed qualifying ties structurally accounted; external completeness unproven |
| 1998/99 | 85 | 85 | 64 | 0 | Observed qualifying ties structurally accounted; external completeness unproven |
| 1999/00 | 157 | 157 | 78 | 0 | First and second group stages kept distinct |
| 2000/01 | 157 | 157 | 80 | 0 | First and second group stages kept distinct |
| 2001/02 | 157 | 157 | 80 | 0 | First and second group stages kept distinct |
| 2002/03 | 157 | 157 | 80 | 0 | First and second group stages kept distinct |
| 2003/04 | 125 | 125 | 80 | 0 | Observed qualifying ties structurally accounted; external completeness unproven |
| 2004/05 | 125 | 125 | 80 | 0 | Observed qualifying ties structurally accounted; external completeness unproven |
| 2005/06 | 125 | 125 | 84 | 0 | Observed qualifying ties structurally accounted; external completeness unproven |
| 2006/07 | 125 | 125 | 82 | 0 | Observed qualifying ties structurally accounted; external completeness unproven |
| 2007/08 | 125 | 125 | 88 | 0 | Observed qualifying ties structurally accounted; external completeness unproven |
| 2008/09 | 125 | 125 | 88 | 0 | Observed qualifying ties structurally accounted; external completeness unproven |
| 2009/10 | 125 | 125 | 88 | 0 | Observed qualifying ties structurally accounted; external completeness unproven |
| 2010/11 | 125 | 125 | 88 | 0 | Observed qualifying ties structurally accounted; external completeness unproven |
| 2011/12 | 125 | 125 | 88 | 0 | Observed qualifying ties structurally accounted; external completeness unproven |
| 2012/13 | 125 | 125 | 88 | 0 | Observed qualifying ties structurally accounted; external completeness unproven |
| 2013/14 | 125 | 125 | 88 | 0 | Observed qualifying ties structurally accounted; external completeness unproven |
| 2014/15 | 125 | 125 | 90 | 0 | Observed qualifying ties structurally accounted; external completeness unproven |
| 2015/16 | 125 | 125 | 92 | 0 | Observed qualifying ties structurally accounted; external completeness unproven |
| 2016/17 | 125 | 125 | 0 | 0 | Qualifying source gap |
| 2017/18 | 125 | 125 | 0 | 0 | Qualifying source gap |
| 2018/19 | 125 | 125 | 0 | 0 | Qualifying source gap |
| 2019/20 | 119 | 119 | 0 | 0 | COVID: August finish; single-leg quarterfinals/semifinals; qualifying gap |
| 2020/21 | 125 | 125 | 0 | 0 | Qualifying source gap |
| 2021/22 | 125 | 125 | 0 | 0 | Qualifying source gap |
| 2022/23 | 125 | 125 | 0 | 0 | Qualifying source gap |
| 2023/24 | 125 | 125 | 0 | 0 | Qualifying gap; group letters absent, eight components independently reconstructed |
| 2024/25 | 189 | 189 | 90 | 0 | 144 league +16 main knockout play-off +29 later knockout fixtures |
| 2025/26 | 189 | 189 | 92 | 1 | 144 league +16 main knockout play-off +29 later knockout fixtures |

Main-stage gates distinguish 1992/93–1993/94 pre-group rounds/two groups, the 16- and 24-club group eras, dual group phases in 1999/00–2002/03, the round-of-16 era, the 2019/20 exception and the 36-club league phase. Every observed four-club group is a complete 12-fixture directed round robin. For 2024/25–2025/26 each league phase has 144 distinct pairings, 36 clubs, eight opponents per club and four home/four away designations. Qualifying and main knockout play-offs are distinct categories. June qualifying and the August 2020 finish are accepted within evidence-bound source-season windows.

**Eight qualifying-season gaps remain: 2016/17–2023/24.** Other qualifying counts establish acquired descriptions, opposite-leg accounting and source structure; they do not independently certify the complete historical entrant population. Entire missing ties cannot be discovered from a publisher's own file alone. Champions/league qualifying paths are not explicitly labelled in these inputs and were not invented. Zero rows for a missing stage mean a SOURCE GAP, never invented NOT PLAYED events.

The 2023/24 TXT omits group letters. Independent opponent-graph reconstruction confirms eight disconnected four-club groups, 12 directed fixtures each; labels A–H remain unknown in that source. Complete source format counts do not certify every kickoff date, legal outcome or stage's full historical availability.

## Score-period ambiguities and historical review queue

There are **106 after-extra-time source observations** and **54 shootout source observations**, including overlap. These are not counts of distinct historical matches or model records. Regulation, halftime, cumulative after-extra-time, shootout, aggregate and raw unassigned components remain separate; an extra-time-only score is not invented where not explicitly supplied.

**Two TXT observations have one parenthesized pair after explicit extra-time/shootout notation.** Their regulation fields remain null even when the cumulative post-extra-time score is zero. One belongs to the 2015/16 comparator: a separately linked CSV supplies an explicit regulation value, retained as comparator evidence without filling the TXT field. The other is a 2025/26 qualifying primary observation with no approved alternate in the corpus. Thus primary source coverage has **5,952 explicit regulation-score descriptions and one unresolved period**, before historical/administrative review. All 4,127 main primary descriptions have explicit source-labelled regulation values; that is not a declaration that every event was played or eligible.

The deduplicated Phase 3 queue contains **13 events**, with overlapping categories: two period ambiguities, two halftime conflicts, three final source-order differences, seven observations in source-leg-label review, and the three-description 1992/93 repeated-tie/replay context. No correction or historical disposition was applied. Nine season contexts separately retain eight qualifying gaps and the missing 2023/24 group labels. Source numeric scores do not prove absence of administrative awards/abandonments; the early replay context remains targeted historical work.

Exact observation/event identifiers, original files/rows/hashes, raw score notation, every conflict and comparator link are in the private Phase 2 report and registries. A structurally quarantined observation is not a Phase 3 HOLD OUT decision. Ordinary missing independent certification is not treated as evidence that a fixture was not played.

## Implementation and verification

Reused immutable acquisition, SHA/blob verification, permission checks, access-stop handling and overwrite helpers. Added only UCL-scoped acquisition/inventory and an independent original reader. Domestic regular-season and ordinary-score adapters were not reused for extra-time parsing. The canonical schema, shared importer, prediction/application code and existing domestic datasets are unchanged.

Synthetic regressions cover extra-time-first and shootout-first score notation, annotation survival through intermediate rows, single/missing period parentheses, zero-score non-inference, unknown/administrative trailers, CSV widths/quoting/multiline physical spans, named aggregate fields, two group phases, both play-off meanings, date/heading provenance, June/August boundaries, stale date inheritance, replay retention, reversed final comparisons, exposed score conflicts, unknown comparator isolation, immutable output refusal, exact URL/season/blob/permission bounds and denied-source safeguards.

Final focused results: **115 tests and 21 subtests passed**, zero failures/errors/skips; 38 new UCL tests plus relevant existing acquisition/artifact/import regressions. Used the existing approved external CPython environment without installation or environment rebuilding. Full repository testing is reserved for finalization. Production artifacts and independent reconstruction were reproduced in separate processes in fresh temporary storage with network connections prohibited; all seven deterministic artifacts matched byte-for-byte. Detailed output destinations also reject public repository paths.

## Deliverables, limits and next gate

Public implementation/tests and this aggregate report contain no original fixture rows or private evidence. Private `phase2/` artifacts include `acquisition_manifest.json`, `input_freeze.final.json`, `validated/source_inventory.json`, `validated/structural_validation.json` (the full machine-readable season/stage matrix), `validated/overlap_assessment.json`, `validated/event_inventory.json`, `validated/unresolved_issues.json`, `score_period_ambiguities.json`, `permission_holds.json`, independent validation, test/reproduction receipts and `report.md` with the exact review evidence appendix. Earlier exploratory inventories and the pre-output-guard freeze manifest remain private historical drafts; `validated/` is the final Phase 2 candidate, not a standardized dataset.

Independent code verification does not establish independently researched historical truth or disjoint upstream provenance. Count agreement does not certify permission for downstream model use. All rights restrictions, stage gaps and uncertain periods remain explicit.

**STOP after Phase 2.** Phase 3 should target the 13-event queue, verify administrative/replay and source-designated orientation policy, resolve or retain period quarantines and preserve all official-stage eligibility distinctions. Additional qualifying recovery needs a separately permitted bounded source plan. No source expansion, historical adjudication, final standardization, model integration/training, staging, commit, push or automatic advancement is authorized.

Final preservation/privacy checkpoint: all **2,332 pre-existing fingerprints** match, with only append-only planning additions; all 16 accepted domestic-audit copies and all 55 source/metadata originals verify. All prior standardized datasets, application files, original environment configuration, HEAD, branch, Git index/configuration and pre-existing unfinished work are preserved. Installed package bytes and Git objects/caches were not exhaustively rehashed; no environment-mutating commands ran. Private artifacts are ignored/untracked; no source rows, receipts, detailed audit registries or credentials appear in the public candidates.

Measured execution including prerequisite domestic-audit preservation/process documentation, bounded acquisition, implementation, diagnostics, tests and reproduction: **26 min 9 sec** (1570.0 seconds), 2026-11-26T22:00:48+00:00 to 2026-11-26T22:26:57.956188+00:00. No blocking owner-approval wait; tool/network waits and retained failed attempts are included. STOP after Phase 2.
