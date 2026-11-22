# French Ligue 2 — Phase 3 source acquisition and inventory

Date: 2026-11-22. Status: COMPLETE, pending user approval. Phase 4 not performed.

## Scope and protection

Original toto worktree, branch feature/data-collection; unchanged HEAD
`07efff5f014bdd2e7e423f2fee76333346135790`. Existing Phase 2 work and uncommitted
changes were preserved. No staging, commit, push, merge, rebase, application or
promotional-worktree changes. No correction, final historical policy, HOLD OUT,
exclusion, standardized data or model training was implemented.

Protection passed for all nine earlier competitions: **676 private files and
185 tracked public files**, plus **54 frozen Phase 2 entries** (48 private files
and six public scripts/tests/docs). The existing planning log is protected by
its original byte prefix and appended only. The index hash remains unchanged.
All originals, receipts and generated artifacts remain under Git-ignored
`data/private/france/ligue_2/`; no private data is tracked or staged.

## Exact acquisition and provenance

Repository: `openfootball/europe`.
Pinned revision: `63df627f3c87ce71708f016522ea236cf74332c3`.
Exact URL pattern:
`https://raw.githubusercontent.com/openfootball/europe/63df627f3c87ce71708f016522ea236cf74332c3/{original_path}`.

Exactly **six new originals** acquired, **five existing originals reused** in the
completed-window inventory, **zero missing season files**, **zero extra season
originals**. The separate 2025/26 original and RSSSF original were preserved.
All six paths/blob identities were resolved against the frozen tree before the
first download. Existing pinned notices/tree were reused, not fetched anew.
Receipts retain URL, original path/filename, commit, Git blob ID, UTC retrieval
time, exact byte size, SHA-256, attribution, source-notice references and rights
limitations. Original source bytes were never rewritten. Acquisition is bounded
(30-second timeout, 8 MB cap, two-second spacing), with no automatic retries,
redirect following, revision substitution or access-restriction bypass.

| New original | Bytes | SHA-256 | Git blob SHA-1 |
|---|---:|---|---|
| `france/2015-16_fr2.txt` | 29898 | `69fda01865364e440165ba22a59e19b1583e81950ac85e59ae459ad81c4a2284` | `302b6fb28518e5f94e6641cb3a0d406ada227f9d` |
| `france/2016-17_fr2.txt` | 29998 | `c86fd93f9aa584ad1783defda269045e285f509e47f6ca87a9c2abc240ee0cc0` | `0e927f62765675a08bbcc73bffbbf25cd3fc5ecf` |
| `france/2018-19_fr2.txt` | 29915 | `4d68be40dda6b1232be0d3beb58d22418e7fa4a609508833286fb4750b70d28e` | `01054a7509457402932a52502f7bb3bfa5f2e07b` |
| `france/2020-21_fr2.txt` | 29499 | `2cb20f078c09edbbc3ed6244cd2cec01d26514e9a3a7f4528aa5d8b624a44d33` | `f8c2a1398bb3c3831b5b9c86e48a8b8214fb5571` |
| `france/2021-22_fr2.txt` | 29499 | `72b120c6c31e8a79c0badf08f932d9678245c0e65a921d0aedde060ccce6840e` | `7de752aabdd92f287199f2fe824c1cc4803132ee` |
| `france/2023-24_fr2.txt` | 29314 | `3d46c0893fc4218bb14742a17aeb1c734a5609db3ee01ead58555777b975446c` | `ba6cce18f93e9cfc685c4ab76d00e20f745627a5` |

Full receipts: private `phase3_acquisition.json` and per-original provenance JSON.
All six new and seven Phase 2 originals pass receipt/SHA checks; all twelve pinned
OpenFootball season originals (eleven in-window plus separate 2025/26) pass Git
blob identity checks. Cached reuse makes zero requests and changes no bytes.

## Complete modern inventory

| Season | Observed slots | Score-bearing | Unscored | Expected regular slots | Clubs | Other stages | Wide rounds |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2014/2015 | 380 | 380 | 0 | 380 | 20 | 0 | 0 |
| 2015/2016 | 380 | 380 | 0 | 380 | 20 | 0 | 0 |
| 2016/2017 | 380 | 380 | 0 | 380 | 20 | 0 | 1 |
| 2017/2018 | 380 | 380 | 0 | 380 | 20 | 0 | 3 |
| 2018/2019 | 380 | 380 | 0 | 380 | 20 | 0 | 2 |
| 2019/2020 | 380 | 280 | 100 | 380 | 20 | 0 | 0 |
| 2020/2021 | 380 | 380 | 0 | 380 | 20 | 0 | 7 |
| 2021/2022 | 380 | 380 | 0 | 380 | 20 | 0 | 5 |
| 2022/2023 | 380 | 380 | 0 | 380 | 20 | 0 | 2 |
| 2023/2024 | 380 | 380 | 0 | 380 | 20 | 0 | 1 |
| 2024/2025 | 306 | 306 | 0 | 306 | 18 | 0 | 2 |
| **Total** | **4106** | **4006** | **100** | **4106** | — | **0** | **23** |

Counts were obtained from the source bytes, then independently reconciled using
an alternative parser. No total was filled or forced. Every season has every
expected directed home/away pairing exactly once and the expected club count.
Inventory checks found zero missing or duplicate/conflicting pairings, malformed
or contradictory numeric full-time score fields, invalid/out-of-bound dates,
invalid team strings, NFC/casefold name collisions or team/same-day collisions.
These are Phase 3 inventory findings, not Phase 4 comprehensive structural or
Phase 5 independent historical certification.

All files contain regular-season records only; no playoffs or other stages were
parsed. This does not imply such fixtures did not occur. Source title, stage,
round, physical line, literal record, SHA-256 and original score/annotation fields
remain traceable for every observation. The proposed canonical competition name
is **Ligue 2**; the eight-column historical schema remains unchanged:
`match_id,date,league,season,home_team,away_team,home_goals,away_goals`.
No standardized rows or match IDs are generated in Phase 3.

There are 47 distinct literal club labels across the window. AC Ajaccio and
Gazélec FC Ajaccio remain distinct. Names including Évian Thonon Gaillard,
US Quevilly-Rouen, US Créteil-Lusitanos, Havre AC and FC Bourg-Péronnas are retained
literally. No automatic cross-league alias, reserve-side interpretation or
predecessor/successor merger is made. Absence of normalized-string collisions is
not proof that historical club identities have been resolved.

## Date precision and review candidates

Source headings supply day/month/weekday; year is explicit or resolved uniquely
against season and weekday. This is not independent actual-playing/completion
or result-availability evidence. No inferred substitute match dates are added.
Scheduled, kickoff, completion, administrative decision and effective availability
dates must remain distinct when later evidence requires it.

**23 wide-round cases cover 228 fixture observations.** These include all seven
in-window Phase 2 flags (68 members) plus 16 newly inventoried flags (160 members).
The additional separate 2025/26 flag (nine members) is also preserved unchanged.
All member identities, dates, source lines and literal scores are machine-readable
in phase3_inventory.json. Long spans are review flags, not errors or exclusions.

| Season | Round | First source date | Last source date | Span days | Members |
|---|---:|---|---|---:|---:|
| 2016/2017 | 21 | 2017-01-20 | 2017-02-21 | 32 | 10 |
| 2017/2018 | 19 | 2017-12-15 | 2018-01-23 | 39 | 10 |
| 2017/2018 | 29 | 2018-03-09 | 2018-04-03 | 25 | 10 |
| 2017/2018 | 32 | 2018-04-06 | 2018-04-30 | 24 | 10 |
| 2018/2019 | 5 | 2018-08-24 | 2018-10-02 | 39 | 10 |
| 2018/2019 | 19 | 2018-12-21 | 2019-01-29 | 39 | 10 |
| 2020/2021 | 3 | 2020-09-12 | 2020-09-30 | 18 | 10 |
| 2020/2021 | 8 | 2020-10-24 | 2020-11-24 | 31 | 10 |
| 2020/2021 | 9 | 2020-10-31 | 2020-12-15 | 45 | 10 |
| 2020/2021 | 11 | 2020-11-21 | 2020-12-15 | 24 | 10 |
| 2020/2021 | 29 | 2021-03-13 | 2021-04-14 | 32 | 10 |
| 2020/2021 | 31 | 2021-04-03 | 2021-04-28 | 25 | 10 |
| 2020/2021 | 35 | 2021-04-24 | 2021-05-12 | 18 | 10 |
| 2021/2022 | 2 | 2021-07-31 | 2021-08-18 | 18 | 10 |
| 2021/2022 | 5 | 2021-08-21 | 2021-09-14 | 24 | 10 |
| 2021/2022 | 20 | 2022-01-08 | 2022-01-28 | 20 | 10 |
| 2021/2022 | 21 | 2022-01-15 | 2022-02-01 | 17 | 10 |
| 2021/2022 | 22 | 2022-01-22 | 2022-02-15 | 24 | 10 |
| 2022/2023 | 7 | 2022-09-02 | 2022-10-04 | 32 | 10 |
| 2022/2023 | 23 | 2023-02-11 | 2023-03-14 | 31 | 10 |
| 2023/2024 | 13 | 2023-11-04 | 2023-11-28 | 24 | 10 |
| 2024/2025 | 8 | 2024-10-04 | 2024-10-22 | 18 | 9 |
| 2024/2025 | 10 | 2024-10-25 | 2024-12-03 | 39 | 9 |

The inventory contains **331 deduplicated fixture-level review candidates**:
228 wide-round members, 100 cancellations, one administrative source annotation,
one unusual score and the unannotated Bordeaux–Rodez administrative case. Category
counts happen not to overlap in this window; code still deduplicates by bound
observation ID. No candidate is corrected or excluded.

### 2019/20 cancellations

Independently rechecked **380 slots = 280 score-bearing + 100 [cancelled]**.
All null scores, literal annotations and scheduled headings remain intact.
There are no ordinary unexplained missing results in this completed-window
inventory. Phase 2 official LFP aggregate evidence is carried unchanged; it does
not certify each individual fixture. Cancelled slots are not played results.

### Niort–Valenciennes, 2020/21

New source annotation: Chamois Niortais–Valenciennes FC, source date **2020-12-22**,
literal **0-3 [awarded]**, line **252**, round 17. This is one score-bearing
administrative observation, not a certified played result. Indexed contemporary
reporting dated 2021-01-06 describes an award following the scheduled December
fixture. Primary decision, appeal finality and effective result availability are
not established. Preserve all source values; do not backdate administrative
availability to the source date or adopt the reported decision date as policy.

[Contemporary secondary lead](https://www.leprogres.fr/sport/2021/01/06/ligue-2-niort-perd-son-match-face-a-valenciennes-sur-tapis-vert)
was inspected through its search index only. The private phase3_documentary_context
ledger binds this lead to the original fixture and explicitly leaves actual
kickoff/completion, verified administrative decision and effective dates null.

### Bordeaux–Rodez, 2022/23

Phase 2 binding unchanged: source date **2023-06-02**, literal **0-1 (HT 0-1)**,
line **570**, no award annotation. The official penalty decision dated **2023-06-12**
remains separate. No numerical administrative replacement, finality inference or
effective-date change. See the frozen Phase 2 documentary ledger and
[official decision](https://www.lfp.fr/article/commission-de-discipline-les-decisions-du-12-juin-2023).

### Unusual score

Valenciennes FC–AS Béziers, **2019-04-19**, literal **5-6**, line **527**, round 33,
is retained unchanged and flagged for later review. Contemporary indexed reports
provide research leads, not Phase 3 certification or a correction decision.

## Preserved separate 2025/26 snapshot

Original and Phase 2 assessment remain byte-identical: **306 slots, 116 scored,
190 unscored**, excluded from all 4106/4006 totals above. US Boulogne occurs in
34 fixtures, AC Ajaccio is absent; the frozen official replacement evidence is
retained. SC Bastia–Stade Lavallois remains unscored, source dated **2025-10-24**,
with [postponed]. No source revision or supplemental result was acquired.

The [official original calendar](https://www.lfp.fr/article/ligue-2-bkt-le-calendrier-de-la-saison-2025-2026)
shows 34 planned rounds and a conditional Ajaccio participant. It is a planned
calendar, not a recovery source for final results. A later acquisition stage
should first inspect permitted current repository metadata, pin a new revision,
then obtain separately approved bounded files and compare all 306 fixture slots,
190 missing-score positions, participant/date changes and administrative notes.
Keep the present original immutable. If a newer OpenFootball original remains
incomplete, seek an organizer-approved export or another permitted provider;
do not scrape or silently merge supplements.

## Historical acquisition objective and permissions

The full target is still **1990/91–2025/26, 36 seasons**. Modern source inventory
completion is not historical Ligue 2 completion. All **24 seasons 1990/91–2013/14**
remain without an approved complete primary source. The older RSSSF 1998/99 original
and its frozen assessment/independent diagnostics are unchanged: 380 score
observations, 22 literal labels, all dates from round headings, unresolved return
score semantics, and alternative aggregate discrepancies for 19 and five clubs.
The two diagnostic spelling substitutions are not production aliases. No score
reading or date inference is approved.

Bounded read-only metadata research during Phase 3 established:

| Candidate | Evidence status / coverage indication | Next permitted step |
|---|---|---|
| [Football-Data F2 catalogue](https://www.football-data.co.uk/francem.php) | Search index advertises F2 from 1996/97, potentially addressing 18 target seasons through 2013/14. No CSV, restricted endpoint or direct catalogue request made. Individual completeness and permission remain unverified. | Ask provider for an allowed acquisition method/export and explicit intended-use conditions; then seek separate approval for a small pilot such as 1996/97 and 2013/14, not bulk acquisition. |
| [StatFootballClubFrance 1993/94](https://statfootballclubfrance.fr/championnat.php?id=177) | Directly inspected 22-club standings and selected extreme scores; no complete dated fixture export demonstrated. | Ask owner about dated-results coverage, provenance and permitted export; standings cannot reconstruct fixtures. |
| [Deux-Zéro club archive](https://www.deux-zero.com/stade-rennais/arbitrage-club/equipe/375/arbitre/372) | Direct browser fetch failed Unicode decoding; prior index-only dated-club leads do not prove full-season coverage. No alternate scraping/bypass attempted. | Seek permission-compatible export/coverage inventory; verify complete fixtures and individual dates on a separately approved sample. |
| [RSSSF historical tables](https://www.rsssf.org/tablesf/fran2hist.html) | Historical format/standings context exists, not demonstrated continuous dated fixtures. Frozen 1998/99 problems remain. | Resolve date/orientation/score discrepancies with independent evidence before any use. |

For **1990/91–1995/96 (six seasons)**, seek organizer/archivist-authorized dated
fixture exports; pilot a grouped season and the 1993/94 single-group transition.
The pre-1993 two-group competition needs within-group pairings, separate playoffs
and championship ties. Brest 1991/92 exclusion/annulment needs primary decisions,
played-versus-recognized fixture counts and season-scoped identity evidence.
For **1996/97–2013/14 (18 seasons)**, the F2 route is only a conditional candidate,
not approved access or established completeness. No contact, purchase, additional
season download or bulk scraping was performed.

OpenFootball CC0 applies to rights held; upstream provenance/third-party rights
are not warranted. RSSSF attribution/copying language reserves rights and does
not establish model-training clearance. Preserve original notices. Technical
completeness, historical confidence, redistribution and training clearance are
separate. No source is declared training-cleared.

## Reproducibility, tests and file scope

New public files: scripts/collect_ligue2_history.py,
scripts/inventory_ligue2_history.py, tests/test_ligue2_history.py and this document.
PLANNING_LOG.md appended only. Every Phase 2 script/test/document remains unchanged.
Private additions: frozen baseline, six originals and six provenance receipts,
phase3_acquisition.json, phase3_inventory.json (all source-bound observations,
review candidates and independent reconciliation), documentary context,
reproducibility receipt, test logs/XML/status and final verification receipt.

Reproduction commands (repository root, with an environment meeting pyproject):

```sh
python -B -m scripts.collect_ligue2_history --init-only
python -B -m scripts.collect_ligue2_history
python -B -m scripts.inventory_ligue2_history
python -B -m pytest -q -p no:cacheprovider tests/test_ligue2_feasibility.py tests/test_ligue2_independent_feasibility.py tests/test_ligue2_history.py
python -B -m pytest -q -p no:cacheprovider tests
```

Fresh results: **21 new synthetic tests, 74 focused Ligue 2, 1366 non-UI,
seven app/launcher and 1373 full repository tests passed**; zero failures/errors/
skips. Existing offline Python 3.13.12 environment used; no dependency installation
or modification of original .venv. Logs/XML are private under verification_phase3/.

The independent parser reconciled all 11 originals line-by-line without using
the production parser. Phase 3 inventory regenerated byte-for-byte / SHA-identical
in safe temporary storage. Both frozen Phase 2 assessment artifacts also regenerate
identically. Cached acquisition was run with network requests prohibited and all
private bytes before/after identical. Hashes and protection details are recorded
in phase3_reproducibility.json. No Phase 2 file was overwritten.

## Phase 4 prerequisites and stopping point

The approved eleven-file modern acquisition is complete; zero missing files.
Before separately approved Phase 4, retain the frozen source hashes/receipts,
23 wide-round memberships, 331 review candidates, administrative/date risks and
separate incomplete/historical sources. Phase 4 should independently validate all
4106 observations and pairing/source bindings comprehensively; later Phase 5
should investigate history and chronology, particularly Niort–Valenciennes and
Bordeaux–Rodez. No eligibility or result-availability policy is decided here.
The older gap and 2025/26 recovery require separate acquisition authorization.

Stopped after Phase 3; awaiting approval. No Phase 4, standardization, corrections,
HOLD OUT/exclusion decisions, model training or Git publication performed.
