# French Ligue 2 — Phase 2 feasibility

Date: 2026-11-22. Status: COMPLETE, pending user approval; no Phase 3 authorization.

## Scope and safeguards

Original toto worktree, feature/data-collection, starting HEAD
`07efff5f014bdd2e7e423f2fee76333346135790`. Exactly seven approved dataset originals
were acquired: six OpenFootball season files and RSSSF France 1998/99.
All originals and generated artifacts are under ignored `data/private/france/ligue_2/`.
Nine earlier competitions are protected by SHA-256 fingerprints for **676 private
files and 185 tracked public files**, plus a byte-prefix-protected planning log.
No original dataset was altered, corrected, merged, excluded or standardized.
No application, promotional worktree, environment, Git index or branch was changed.

## Acquisition and provenance

OpenFootball repository: `openfootball/europe`.
Pinned commit: `63df627f3c87ce71708f016522ea236cf74332c3`.
URL pattern: `https://raw.githubusercontent.com/openfootball/europe/63df627f3c87ce71708f016522ea236cf74332c3/{original_path}`.
RSSSF URL: `https://www.rsssf.org/tablesf/fran99.html`.

Before any download, all six paths and blob IDs were checked against the already
preserved immutable Git tree. The tree and four pinned notices (README.md,
LICENSE.md, france/README.md, france/NOTES.md) were reused byte-for-byte with their
prior retrieval receipts, not downloaded again. New receipts retain URLs,
original filenames/paths, UTC retrieval timestamps, byte sizes, SHA-256, Git blob
IDs, attribution, format and rights uncertainty. Full timestamped registry:
private `acquisition.json` and per-original `.provenance.json` files.

Requests use a 30-second timeout, 8 MB cap, two-second spacing, no automatic retry
or redirect following, and a persistent access-stop marker. The initial sandbox
DNS lookup failed before reaching the host; this diagnostic is preserved as
`sandbox_dns_failure.json`. Authorized network access then acquired the seven
files. No HTTP restriction was bypassed. No Football-Data endpoint was accessed.
An initial RSSSF receipt path typo (`tabless` instead of `tablesf`) was corrected
in metadata only; initial receipt/manifest versions are retained as `.initial`.
The URL and downloaded original bytes were always correct and unchanged.

| Original path | Bytes | SHA-256 | Git blob SHA-1 |
|---|---:|---|---|
| `france/2014-15_fr2.txt` | 30043 | `45cb3e1e41efb1e85a4ee14b414d985f71a5d94a1062d35ebc94d15b3a272908` | `f3a08e4ae5948e71ea17101de1cfedd207a8c0fd` |
| `france/2017-18_fr2.txt` | 30152 | `9277357ef8e1bbb611edaede99e80969d70fd2b265bc23115ab86de4f2ea9541` | `7ce9af9fc37c4ab96001c6178194c8ffdb9eb8b6` |
| `france/2019-20_fr2.txt` | 30004 | `5a4bb72c4c40b3d3ad9a3997548a99c73089b3269430d850467593614a55a2a7` | `d8caaffda4c2e3e1313f906692eda39c8cbe3bac` |
| `france/2022-23_fr2.txt` | 29474 | `a90ad2367524ae546e0f6077722aab761c21c18e4d734faa02d857916030fd13` | `db9fc70913bb4bb00024d0f22ea534a0eb50a6ce` |
| `france/2024-25_fr2.txt` | 24225 | `a5421fcd1589ca8c95f3751b8d754996498e05e1a551f0d57d667f049c24236a` | `abc2345644965aa2770ff79866020a7fb14cd05d` |
| `france/2025-26_fr2.txt` | 19744 | `febad1cc854d98f018c9ca007cdd9a2c6984b67e6c2c72b6954585e4ab1cf091` | `a126221c0c39261cb45815c3db67602e72b02298` |
| `tablesf/fran99.html` | 43601 | `511c73a4e8f9e0f9e18dfb0af699821f906984638045cded3530caad64d14a43` | `not applicable` |

## Measured sample inventory

| Season | Observations | Score-bearing | Unscored | Expected regular slots | Club labels | Other stages | Wide rounds |
|---|---:|---:|---:|---:|---|---|---:|
| 2014/2015 | 380 | 380 | 0 | 380 | 20 | 0 | 0 |
| 2017/2018 | 380 | 380 | 0 | 380 | 20 | 0 | 3 |
| 2019/2020 | 380 | 280 | 100 | 380 | 20 | 0 | 0 |
| 2022/2023 | 380 | 380 | 0 | 380 | 20 | 0 | 2 |
| 2024/2025 | 306 | 306 | 0 | 306 | 18 | 0 | 2 |
| 2025/2026 | 306 | 116 | 190 | 306 | 18 | 0 | 1 |
| 1998/1999 | 380 | 380 | 0 | 380 | 22 literal / 20 diagnostic | 0 in selected block | 0 |

Modern total: **2,132 observations = 1,842 score-bearing + 290 unscored**.
Each modern sample has every expected directed regular-season pairing exactly
once, the expected number of clubs, and zero duplicate/conflicting pairings,
malformed score fields, invalid date/team fields, NFC/casefold identity collisions
or same-team/same-day collisions. These checks establish source structure only.
There are no postseason observations in these six files. This does not establish
that playoffs did not occur; the files end at the regular-season boundary.
All raw lines, source hashes, source line numbers, titles, annotations and date
headings remain in the assessment. Unknown title/stage/fixture grammar fails.

Modern date headings provide day/month/weekday; year may be explicit or uniquely
resolved from the stated season and weekday. They are source dates, not
independent certificates of actual completion or result availability.

## Curtailed 2019/20

The file contains **380 slots: 280 scored and 100 explicitly [cancelled]**.
Scored dates run from 2019-07-26 to 2020-03-09. Cancelled fixtures retain scheduled
headings through 2020-05-15, null goals and their cancellation annotations.
No fixture slot is missing. Official LFP minutes independently corroborate the
aggregate 280 played / 380 planned; they do not certify all individual fixtures.
No cancelled observation is converted into a completed score or excluded here.

## 2025/26 incompleteness and replacement

The pinned version contains all **306 fixture slots**, but only **116 scored**
(2025-08-09 through 2025-11-03) and **190 unscored**. Future source headings extend
to 2026-05-08. Unscored does not imply cancelled or actually unplayed today.
SC Bastia–Stade Lavallois is unscored, dated 2025-10-24 and marked [postponed].

All 18 literal source participants were measured. US Boulogne is present in
34 fixtures (17 home, 17 away); AC Ajaccio is absent. This matches the official
replacement announcement. The first-round Boulogne–Bastia source date is
2025-09-16. LFP minutes distinguish this new fixture from a technical match remis;
those minutes alone do not certify its later playing date/result. No club alias
or fixture-date correction is applied.

## Administrative and scheduling review candidates

Bordeaux–Rodez is source line 570 of 2022-23_fr2.txt, round 38, dated 2023-06-02,
with literal FT **0-1**, HT **0-1** and **no administrative annotation**.
The 2023-06-12 official penalty defeat is separate documentary context. The
inspected decision does not establish a numerical awarded score or exhaustive
appeal finality. Preserve the source record; source date, actual interruption,
decision date and effective availability remain separate review questions.

Eight rounds contain **77 affected fixture observations** with date spans over
14 days. Every member and source binding is preserved in the private assessment.
Long spans are review flags, not established errors or exclusion decisions.

| Season | Round | First source date | Last source date | Days | Members |
|---|---:|---|---|---:|---:|
| 2017/2018 | 19 | 2017-12-15 | 2018-01-23 | 39 | 10 |
| 2017/2018 | 29 | 2018-03-09 | 2018-04-03 | 25 | 10 |
| 2017/2018 | 32 | 2018-04-06 | 2018-04-30 | 24 | 10 |
| 2022/2023 | 7 | 2022-09-02 | 2022-10-04 | 32 | 10 |
| 2022/2023 | 23 | 2023-02-11 | 2023-03-14 | 31 | 10 |
| 2024/2025 | 8 | 2024-10-04 | 2024-10-22 | 18 | 9 |
| 2024/2025 | 10 | 2024-10-25 | 2024-12-03 | 39 | 9 |
| 2025/2026 | 1 | 2025-08-09 | 2025-09-16 | 38 | 9 |

No additional awarded/interruptive source annotation was found beyond the 100
cancellations and one postponement. Unannotated historical exceptions may still
exist. AC Ajaccio and Gazélec FC Ajaccio coexist distinctly in 2014/15 and 2017/18.
Cross-season abbreviations, accents, reserve suffixes and predecessor/successor
identities require explicit later review; no global mapping is implemented.

## RSSSF 1998/99: extractable observations, unresolved semantics

The HTML document mixes first division, cups, second division and lower levels.
The parser selects only the unique PRE block containing `Stages 1-20`, parses
19 paired-round headings and 190 paired lines, and stops before the following
final standings. It extracts **380 numeric score observations** without importing
other stages. The original is decoded as ISO-8859-1 (no explicit charset was found),
with HTML entities decoded; original bytes are preserved. Bindings use PRE-block
line plus leg, not claimed original HTML physical-line numbers.

There are **22 literal labels**, including `Beuvais`/`Beauvais` and
`St.Étieene`/`St.Étienne`. Two explicitly documented **diagnostic-only** substitutions
produce 20 labels and all 380 directed pairings once under provisional return-venue
reversal. Neither source nor production records are renamed.

All **380 dates are round-heading proxies**, not explicit individual-match dates.
Return-leg venue/score orientation is **UNRESOLVED**. Literal left/right team and
score columns remain preserved alongside clearly provisional parsed fields.
Independent diagnostics tested two interpretations against the printed D2 table:

- Treating each score as home/away after reversing return venues matches all six
  aggregate fields (P/W/D/L/GF/GA) for only **1 of 20 clubs**.
- Treating return scores in original left/right order matches **15 of 20 clubs**.
  Ajaccio, Cannes, Châteauroux, Laval and Nîmes still disagree with printed totals.

These comparisons are within one document, not independent historical evidence.
They do not identify which particular scores or standings are wrong. No orientation,
score repair, name mapping or missing date is approved. The sample demonstrates
literal extractability, **not a reliable standardized dated season**. It does not
establish continuous older coverage.

## Documentary context and evidence limitations

All accesses below were bounded document inspections; no additional season
originals or bulk archives were acquired. The private documentary ledger retains
access date 2026-11-22, titles, exact URLs, independence and claim limitations.

- **L2-E01** [LFP Conseil administration, proces-verbal du 30 avril 2020](https://www.lfp.fr/assets/20200430_PV_Conseil_Administration_LFP_e824a457fa.pdf) (2020-04-30; DIRECTLY_INSPECTED_PDF). 280 Ligue 2 matches played out of 380 planned; aggregate corroboration, not individual fixture certification. Independence: OFFICIAL_RECORD.
- **L2-E02** [Commission de discipline : les decisions du 12 juin 2023](https://www.lfp.fr/article/commission-de-discipline-les-decisions-du-12-juin-2023) (2023-06-12; DIRECTLY_INSPECTED). Bordeaux-Rodez of 2023-06-02 lost by penalty by Bordeaux. Does not itself supply a numerical administrative score or exhaustive appeal finality. Independence: OFFICIAL_RECORD.
- **L2-E03** [US Boulogne rep echee en Ligue 2 BKT](https://www.lfp.fr/article/l-us-boulogne-cote-d-opale-repechee-en-ligue-2-bkt) (2025-08-07; DIRECTLY_INSPECTED). AC Ajaccio not participating in 2025/26; US Boulogne admitted instead. Not a global alias or club continuity claim. Independence: OFFICIAL_RECORD.
- **L2-E04** [LFP Conseil administration, proces-verbal du 7 aout 2025](https://www.lfp.fr/assets/20250807_PV_CA_9fed4c00eb.pdf) (2025-08-07; DIRECTLY_INSPECTED_PDF). Boulogne takes Ajaccio schedule position; first-round Boulogne-Bastia not classified as a match remis. Does not itself certify final playing date/result. Independence: OFFICIAL_RECORD_SAME_EVENT_AS_E03.
- **L2-E05** [Brest mis en liquidation judiciaire et exclu du championnat de deuxieme division](https://www.lemonde.fr/archives/article/1991/12/08/football-le-club-de-brest-est-mis-en-liquidation-judiciaire-et-exclu-du-championnat-de-deuxieme-division_4028688_1819218.html) (1991-12-08; DIRECT_PAGE_PARTIAL_PREVIEW). Accessible contemporary report describes Brest exclusion and annulment of results. Primary decision and fixture-level inventory still required; no exclusion policy implemented. Independence: CONTEMPORARY_SECONDARY_REPORT.

Brest 1991/92 remains an older-source research objective: exclusion/annulment is
supported by an accessible contemporary report, not a recovered primary decision
or fixture-by-fixture dataset. No historical decision or exclusion is implemented.

## Schema and downstream use

Proposed canonical competition: **Ligue 2**. Future schema remains:
`match_id,date,league,season,home_team,away_team,home_goals,away_goals`.
Modern observations are structurally convertible after later evidence/policy
approval. No standardized CSV or match IDs are generated in Phase 2. Original
competition labels, stages/groups, team strings and chronology must remain in
future audit metadata. Scheduled, kickoff, completion and administrative decision
dates cannot be collapsed without evidence. Future evaluation must use results
known strictly before prediction date. The RSSSF provisional fields are not
approved input for such conversion.

## Rights and historical coverage

OpenFootball declares CC0-1.0 for rights held; upstream lineage and third-party
rights are not warranted. RSSSF credits Jérôme Faugeras, Frédéric Pauron, Sorin
Arotaritei and RSSSF; copying with acknowledgement is stated while rights are
reserved. Technical acquisition does not clear redistribution or model training.
Official decisions supply historical evidence, not a bulk-data licence.
No source is marked training-cleared; no application integration or training occurs.

The overall target remains **1990/91–2025/26 (36 seasons)**. All **24 seasons of
1990/91–2013/14 remain an unresolved acquisition objective**, despite the bounded
1998/99 sample. Pre-1993 two-group pairings, Brest annulments, 22-to-20 club changes,
reserve sides and club continuity need separate evidence. The pinned 2025/26
source is incomplete. The ongoing 2026/27 season is outside scope.

## Reproducibility and fresh tests

Commands from repository root (use the preserved offline temporary environment
if original-venv imports stall):

```sh
python -B -m scripts.collect_ligue2_feasibility --init
python -B -m scripts.validate_ligue2_feasibility
python -B -m scripts.verify_ligue2_feasibility
python -B -m pytest -q -p no:cacheprovider tests/test_ligue2_feasibility.py tests/test_ligue2_independent_feasibility.py
python -B -m pytest -q -p no:cacheprovider tests
```

Fresh results: **53 focused**, **1,345 non-UI**, **7 app/launcher**, and **1,352 full
repository tests passed**, zero failures/errors/skips. The existing offline
Python 3.13.12 temporary environment met declared Python >=3.11 constraints;
original .venv and installed dependencies were not changed. Logs/XML/status files
are retained privately under verification/. Tests use synthetic fixtures only.

A separate raw parser reconciled all six modern files line-by-line against the
assessment and independently extracted all 190 RSSSF paired lines. It does not
call the production parser. Both assessment and independent reconciliation were
regenerated into temporary storage and compared byte-for-byte and by SHA-256.
Cached acquisition was rerun with network access disabled and every private
source/receipt/metadata byte unchanged. Full details: phase2_reproducibility.json.
All seven receipt SHA-256 values and six Git blob IDs pass. Protection checks for
676 prior private / 185 tracked public files and append-only log pass. Every new
private artifact is Git-ignored; no private data is tracked/staged.

## Proposed Phase 3 and stopping point

Subject to separate approval, acquire **only six remaining modern files** at the
same verified pin: 2015-16_fr2.txt, 2016-17_fr2.txt, 2018-19_fr2.txt,
2020-21_fr2.txt, 2021-22_fr2.txt, 2023-24_fr2.txt (all under france/).
Reuse the five already acquired seasons in 2014/15–2024/25 and inventory that
11-season source window without assuming accepted counts. Preserve 2025/26 as
an incomplete separate snapshot. A newer revision or different permitted source
for its 190 missing results requires separate approval; never silently replace it.

Continue bounded permission/metadata research for older dated sources; RSSSF
requires date/orientation/discrepancy resolution, and Football-Data remains outside
approved access. No purchase, bulk scraping or unapproved season acquisition.
Stop after Phase 2: no full acquisition, structural certification, final historical
policy, standardization, application change, training, staging, commit, push or merge.
