# Segunda División Phase 3: controlled modern-source acquisition and inventory

Date: 2026-11-22. Original `toto` worktree, `feature/data-collection`.
HEAD remains `052d25185182f1edbb80fac51cafbb59e0acf7cf`.

## Outcome and assurance boundary

**Modern source acquisition is complete for the approved 13 seasons,
2012/13–2024/25: ten additional originals acquired, three Phase 2 originals reused,
zero missing files and zero parse failures. Results are not complete.**

Measured from the acquired files: **6,006 regular-season fixture observations,
5,997 with scores and nine without scores**. All nine missing scores are in
2024/25 round 42. Source-marked Reus awards are included in the scored count;
scored does not mean played, independently verified, eligible or training-cleared.
The 6,006 expected fixture slots were not used to manufacture results.

This phase reuses the frozen feasibility grammar for inventory diagnostics.
It is not Phase 4's independent comprehensive structural validation, Phase 5
historical certification, exception-policy approval or standardization. No
fixture was corrected, excluded, silently renamed or integrated into the app.

## Preservation and bounded acquisition

Before acquisition, Phase 2 verification hashes were checked and a new baseline
froze **24 Phase 2 artifacts**: all 20 private files plus the four public scripts,
tests and feasibility documentation. The existing planning-log prefix was sealed
separately, permitting appends only. This supplements the existing **493 private
and 145 tracked public** fingerprints protecting all seven completed competitions,
their implementations, documentation and application files.

All originals remain under the existing ignored
`data/private/spain/segunda_division/` directory. The five Phase 2 originals,
receipts, initial/current assessments and verification evidence are unchanged.
In particular, incomplete 2025/26 and the RSSSF HTML original remain preserved.

Repository: <https://github.com/openfootball/espana>.
Pinned revision: `80035a93dd4920985af52aa097a54a6fb888563b`.
Each original path was verified against the previously preserved complete Git
tree before any request. Exact URLs use:

```text
https://raw.githubusercontent.com/openfootball/espana/80035a93dd4920985af52aa097a54a6fb888563b/<season>/2-liga2.txt
```

Only ten source requests were made. Requests have five-second spacing, a
30-second timeout and 2 MB body cap. Redirects are refused before a follow-up
request; non-200 responses, `Retry-After` and incorrect Git identities trigger a
saved access stop without automatic retry. Complete caches require matching
source/receipt pairs and are reused offline without writes. Originals use
exclusive creation; incomplete pairs fail rather than being silently repaired.

### Exact acquired-file list and checksums

Every row is a new `openfootball/espana/<season>/2-liga2.txt` original.
Every receipt preserves exact URL, commit, original path/name, retrieval timestamp,
headers, byte count, SHA-256, Git blob SHA-1, attribution and licensing limitations.
All retrievals were on 2026-11-22 UTC; exact timestamps are in the receipts.

| Season directory | Bytes | SHA-256 |
|---|---:|---|
| `2013-14` | 35,930 | `60afa9a24b96f04823af1c6b3092e5abd9d14df490837c8fe2794ecdf99cc1ef` |
| `2014-15` | 35,848 | `939f23a767e78e96dc62d640a8834967ff28b974e8e73c9766a51c2b95222faa` |
| `2015-16` | 36,008 | `fd3d139921a4c66372737e0f8bb41b827fbe6427f575afbe4393ec05f87e71fa` |
| `2016-17` | 36,392 | `558e7a88b5208413235a99ff6aa5695d06acc5adb64df64248e26b70da6b9587` |
| `2017-18` | 36,685 | `f7e9c67684ab8dd467a147cb964fbb272d0ad6b10b2fc3c17b15b1ca0aa1632b` |
| `2020-21` | 30,117 | `f1c1006166f91b34b2ab02014668afd4cc8603c892db54620534045ad3eebcd2` |
| `2021-22` | 29,785 | `b1ee260c7a8f236d291db047f3384d49dd8f04cabe10cccae2fc076d1d5ccaf9` |
| `2022-23` | 29,393 | `25136753dc58093975d91648ad5cca7682cd61d801a6eebffa2cfa7c33a08146` |
| `2023-24` | 29,793 | `f2c0ef682c75bef1e4f66667ee049cbed6cc6d78e68371f7feea44dc711bd626` |
| `2024-25` | 36,803 | `0d55243481eabe5e836d86c979fbd600033e10a07946cc9bce224ce13bd183d4` |

The original 2012/13, 2018/19 and 2019/20 files were reused with their original
Phase 2 receipts. All 13 modern size/SHA-256/Git blob checks pass. All five Phase 2
sources, including the outside-scope 2025/26 and RSSSF samples, also revalidate.
Licence/tree notices were reused, not redownloaded or changed.

## Complete measured season inventory

All rows have **462 observed regular fixtures, 22 clubs, zero playoff/other-stage
records, complete unique directed pairings, zero duplicate/conflicting fixtures,
and zero inventory date, name, appearance or round-allocation errors**. These are
inventory findings from the feasibility parser, not independent certification.

| Season | Acquisition | Observed | Scored | Unscored | Expected regular | Source date range | Wide rounds |
|---|---|---:|---:|---:|---:|---|---:|
| 2012/13 | Reused | 462 | 462 | 0 | 462 | 2012-08-17–2013-06-09 | 0 |
| 2013/14 | New | 462 | 462 | 0 | 462 | 2013-08-16–2014-06-08 | 0 |
| 2014/15 | New | 462 | 462 | 0 | 462 | 2014-08-23–2015-06-07 | 1 |
| 2015/16 | New | 462 | 462 | 0 | 462 | 2015-08-22–2016-06-04 | 1 |
| 2016/17 | New | 462 | 462 | 0 | 462 | 2016-08-19–2017-06-11 | 2 |
| 2017/18 | New | 462 | 462 | 0 | 462 | 2017-08-18–2018-06-02 | 2 |
| 2018/19 | Reused | 462 | 462 | 0 | 462 | 2018-08-17–2019-06-09 | 0 |
| 2019/20 | Reused | 462 | 462 | 0 | 462 | 2019-08-17–2020-08-07 | 4 |
| 2020/21 | New | 462 | 462 | 0 | 462 | 2020-09-12–2021-05-30 | 7 |
| 2021/22 | New | 462 | 462 | 0 | 462 | 2021-08-13–2022-05-29 | 1 |
| 2022/23 | New | 462 | 462 | 0 | 462 | 2022-08-12–2023-05-28 | 0 |
| 2023/24 | New | 462 | 462 | 0 | 462 | 2023-08-11–2024-06-02 | 1 |
| 2024/25 | New; review | 462 | 453 | 9 | 462 | 2024-08-15–2025-06-01 | 4 |
| Total | 10 new / 3 reused | 6,006 | 5,997 | 9 | 6,006 | — | 23 |

All 6,006 rows inherit their explicit source date headings; no RSSSF round-heading
proxy enters this modern inventory. This does not establish actual playing dates
or result availability for administrative awards, resumptions or unscored schedules.
Season 2019/20 retains the explicit July/August 2020 extended calendar. Missing
optional kickoff/halftime values are preserved rather than invented. All files
decode strictly as UTF-8; raw physical lines and original labels remain bound
to source path/SHA-256/line. Count headers are checked separately against observed
fixture slots, not interpreted as counts of completed matches.
The 2020/21–2023/24 files use the score-between-teams syntax, while the other
nine modern files use `home v away` syntax; both are inventoried explicitly.

### Nine new missing-result observations

All are 2024/25 round 42. Goals, FT and outcomes remain absent; these are not
0–0 results or proven unplayed matches. Source dates/times are not certified actual dates.

| Physical line | Source date | Home | Away |
|---:|---|---|---|
| 745 | 2025-05-31 | Málaga CF | Burgos CF |
| 747 | 2025-06-01 | SD Huesca | CD Eldense |
| 748 | 2025-06-01 | UD Almería | CD Tenerife |
| 749 | 2025-06-01 | FC Cartagena | CD Mirandés |
| 750 | 2025-06-01 | Deportivo La Coruña | Elche CF |
| 751 | 2025-06-01 | Real Oviedo | Cádiz CF |
| 752 | 2025-06-01 | Levante UD | SD Eibar |
| 753 | 2025-06-01 | Racing Santander | Granada CF |
| 754 | 2025-06-01 | Córdoba CF | Albacete |

No replacement revision or scores were acquired to patch these observations.

## Scheduling and historical exceptions

**23 modern wide-round candidates cover 253 distinct fixture observations**:
four carried from Phase 2 plus 19 newly observed cases. A span of at least 14 days
is a review flag, not a structural error, scheduling explanation or exclusion.

| Season | Round: earliest–latest source dates |
|---|---|
| 2014/15 | 24: 2015-02-07–2015-03-18 |
| 2015/16 | 27: 2016-02-27–2016-03-16 |
| 2016/17 | 16: 2016-11-25–2016-12-14; 19: 2016-12-16–2017-01-11 |
| 2017/18 | 7: 2017-09-29–2017-11-01; 17: 2017-12-02–2018-01-18 |
| 2019/20 | 6: 2019-09-17–2019-10-16; 20: 2019-12-13–2020-06-10; 24: 2020-01-17–2020-02-19; 42: 2020-07-20–2020-08-07 |
| 2020/21 | 1: 2020-09-12–2020-11-05; 2: 2020-09-19–2020-12-10; 6: 2020-10-17–2020-11-05; 7: 2020-10-21–2020-12-09; 21: 2021-01-08–2021-02-17; 31: 2021-03-26–2021-04-14; 32: 2021-03-30–2021-04-21 |
| 2021/22 | 21: 2021-12-17–2022-01-19 |
| 2023/24 | 28: 2024-02-23–2024-03-13 |
| 2024/25 | 13: 2024-11-02–2024-11-27; 14: 2024-11-08–2025-01-07; 19: 2024-12-13–2025-01-29; 24: 2025-01-24–2025-03-05 |

All **six original Phase 2 flags** are preserved exactly, including the two outside
this modern scope: 2025/26 round 10 and RSSSF 1996/97 round 15. There are 25 distinct
flags across the preserved evidence and expanded modern inventory, not 29:
four modern flags overlap the six Phase 2 flags. Do not double-count them.

The complete Phase 2 exceptional-context object reproduces unchanged:

- **Reus 2018/19:** 42 source fixture observations, 21 explicitly marked `[awarded]`.
  Original scores/calendar dates and the 28 January 2019 expulsion decision remain
  separate. Individual final awards, appeal status and result-availability dates
  remain unresolved for later policy. No additional marked awards were found in
  the other twelve source files; absence of notes does not establish ordinary play.
- **Rayo–Albacete:** source 10 June 2020 / 1–0; original kickoff 15 December 2019
  and completion 10 June 2020 remain in bound context, without rewriting the source.
- **Deportivo–Fuenlabrada:** source 7 August 2020 / 2–1; originally scheduled
  20 July, actual playing date 7 August, and applicable evidence limitations remain
  separate. Intermediate scheduling proposals are not substituted for actual dates.

No fresh independent historical certification or processing decision was made.
All source annotations and current evidence classifications are retained.

## Team labels and identity risks

The modern files contain **64 distinct exact team labels**. No accent/case/
punctuation-only collision groups were found. Exact labels and season membership
are retained in the inventory; this is not proof of 64 legally continuous clubs.

Six reserve-label review candidates are kept distinct from first teams:
`Athletic Club B`, `FC Barcelona B`, `Real Madrid Castilla`, `Real Sociedad B`,
`Sevilla Atlético`, `Villarreal CF B`. No automatic parent/reserve merger occurred.
For future cross-league integration, source-specific labels such as `CD Alavés`,
`Espanyol Barcelona` and `Racing Santander` need evidence-backed identity handling,
not blanket replacement with La Liga labels. `Lorca FC`, `UD Logroñés` and similarly
named historical/successor entities likewise require continuity review.

## Reproduction and verification

New public files: `scripts/collect_segunda_history.py`,
`scripts/inventory_segunda_history.py`, `tests/test_segunda_history.py`, this document.
`PLANNING_LOG.md` is append-only. All four Phase 2 public files are unchanged.

New private artifacts (**24 files**): `phase3_protected_before.json`; ten exact
originals and their ten `.provenance.json` receipts; `phase3_acquisition.json`;
`phase3_inventory.json`; `phase3_verification.json`. Together with the 20 unchanged
Phase 2 files, the Segunda area contains 44 private files. There is no standardized CSV.

```sh
PYTHONPATH=src:. python -B scripts/collect_segunda_history.py --init
PYTHONPATH=src:. python -B scripts/inventory_segunda_history.py
PYTHONPATH=src:. python -B scripts/inventory_segunda_history.py --check
PYTHONPATH=src:. python -B -m pytest tests/test_segunda_feasibility.py tests/test_segunda_history.py -q -p no:cacheprovider
```

Requires retained Phase 2 private evidence. First inventory creation refuses an
existing output; `--check` compares without replacing it. The complete acquisition
cache can be replayed offline; no moving branch or redownload is needed.

Measured checks:

- **18 new Phase 3 tests / 51 combined Segunda tests passed.**
- **860 full repository tests passed in 12.09 seconds**, including all seven
  app/launcher tests. Counts overlap; do not add them.
- Two actual complete-cache calls with network forbidden: no writes, all ten
  cached and three Phase 2 files reused.
- Two inventory regenerations are byte-identical, SHA-256:
  `777dbeb78e42f7035f362100984b62310b947063dfaf84d62794758d4397cb5e`.
- Phase 2 assessment regenerates byte-identically; all six scheduling flags,
  reused raw observations and exceptional context are unchanged.
- All 493 prior private / 145 tracked public and 24 frozen Phase 2 fingerprints
  match. No source data, previous outputs, app or promotional files changed.
- No packages installed or upgraded. Tests used the existing temporary Python
  3.13 verification environment outside iCloud, with a 180-second timeout.

The inventory reports completeness issues; it does not assert that every observed
fixture can be accepted into a future screened dataset.

## Historical coverage gaps, permissions and next gate

| Gap | Current evidence | Concrete next requirement |
|---|---|---|
| 1990/91–2011/12, 22 seasons | No approved complete source; the preserved RSSSF 1996/97 sample has 379 regular round-date proxies | Seek a permission-compliant dated results export, potentially BDFutbol. Before acquisition, establish exact fields/stages/coverage and explicit academic storage, redistribution and statistical-training terms. No purchase or scraping authorized. |
| 2024/25, within modern scope | Nine missing round-42 scores in the approved pinned file | Propose a separately approved newer Git revision or permission-compliant completion source. Verify individual dates/results; preserve the present snapshot and record discrepancies, never silently patch it. |
| 2025/26, completed season | Preserved pinned source still 131 scored / 331 unscored, outside the 13-season modern inventory | Independently establish a complete permitted source/revision, then seek approval for bounded acquisition and comparison. Do not infer results from schedules or standings. |

Useful source-discovery starting points from Phase 1 remain the
[OpenFootball repository](https://github.com/openfootball/espana),
[BDFutbol data-service catalogue](https://www.bdfutbol.com/es/c/archives.html),
and official LaLiga/RFEF records. This phase made no additional-source acquisition,
Football-Data request, BDFutbol purchase or bulk scrape. No new permission was inferred.

OpenFootball's CC0 notice covers rights held, without upstream-rights warranty.
RSSSF's retained attribution/copying conditions still apply to that separate sample.
Technical completeness, historical confidence, redistribution and model-training
clearance remain separate: **model-training clearance is unresolved**.

After approval, Phase 4 should independently validate all 6,006 source fixture slots,
keep the nine missing scores explicit, investigate all 23 modern scheduling flags,
check identities/stages and retain Reus/interruption evidence without decisions.
Acquiring missing results requires separate authorization; Phase 4 must not guess
them or label the full historical target complete. Stop before Phase 4.
