# La Liga Phase 2: bounded feasibility acquisition

Date: 2026-11-21. Worktree: original `toto`; branch: `feature/data-collection`.
Starting HEAD: `2f2bfe1542c2460111ae685621d138874fa69f52`.

## Scope and decision

The user authorized three revision-pinned dataset originals and their supporting
source/licence documentation, structural assessment of six specified seasons,
and a diagnostic check of the proposed source-window boundary. This is not full
La Liga acquisition, standardization, independent historical certification or
training. No Football-Data URL was requested or retried.

**Result: technically viable for a bounded next acquisition phase, subject to
historical review and unresolved usage rights.** No parser or coverage blocker
was found in the six requested seasons. Expected counts are structural baselines,
not accuracy certification or predetermined accepted totals.

## Preservation and acquisition

Before any dataset download, `protected_competitions_before.json` recorded SHA-256
fingerprints of **428 existing files** across `data/private/england/`, `germany/`
and `italy/`. These cover all six completed competitions and their originals,
standardized outputs, manifests and evidence. Every fingerprint subsequently
matched. The unrelated root-level private `E0.csv` was not a competition-baseline
input and was not modified.

Some iCloud-backed files initially stalled reads. A separate timed-read diagnostic,
`protected_accessible_before.json`, recorded 373 immediately readable files and
55 pending reads. That diagnostic is **superseded by the complete 428-file
baseline**, not a report of missing files. Dataset acquisition waited for the full
baseline. No old private file was overwritten or deleted.

The exact approved Git paths were verified against complete repository trees at
these commits before downloading. Downloaded blobs were also checked using Git's
blob SHA-1 identity against tree entries, alongside locally recorded SHA-256 and
byte lengths:

| Repository | Immutable revision | Dataset path | Bytes | SHA-256 |
|---|---|---|---:|---|
| `jalapic/engsoccerdata` | `872c5c354161ace8408f3091b758c6af4cccca94` | `data-raw/spain.csv` | 2,221,025 | `5d482cb76d8b47f77bec531683510815738bc54feb9f0e2524905665116d02fb` |
| `openfootball/espana` | `80035a93dd4920985af52aa097a54a6fb888563b` | `2012-13/1-liga.txt` | 30,359 | `cb7d1494ada5b0f56e2251d1d9a5fb791734e20e45d9b7a6222ceca79cff1c2b` |
| same | same | `2025-26/1-liga.txt` | 50,394 | `baf2a9ae42c4c6a919eb39aa2476f1d44b9d3b18050adfc6386d36ef2a98e956` |

Exact dataset URLs:

- https://raw.githubusercontent.com/jalapic/engsoccerdata/872c5c354161ace8408f3091b758c6af4cccca94/data-raw/spain.csv
- https://raw.githubusercontent.com/openfootball/espana/80035a93dd4920985af52aa097a54a6fb888563b/2012-13/1-liga.txt
- https://raw.githubusercontent.com/openfootball/espana/80035a93dd4920985af52aa097a54a6fb888563b/2025-26/1-liga.txt

Original byte snapshots and notices reside only under ignored
`data/private/spain/la_liga/`. The six supporting downloads were:

- `jalapic/engsoccerdata/README.md`
- `jalapic/engsoccerdata/DESCRIPTION`
- `jalapic/engsoccerdata/man/spain.Rd`
- `openfootball/espana/README.md`
- `openfootball/espana/LICENSE.md`
- `openfootball/espana/NOTES.md`

The originals were not decoded/re-encoded on disk. `acquisition.json` records exact
raw URLs, repository and commit, UTC retrieval time, original filename, extension,
size, SHA-256, Git blob identity and downstream-rights limitations for all nine
files. Retrievals span 2026-11-21T22:08:35.752999+00:00 through
2026-11-21T22:08:39.484276+00:00. `source_paths.json` records the path-verification
URLs, tree-response hashes and per-file blob/size expectations.

## Observed coverage

| Season | Acquired source | Records | Scored | Expected | Source date range | Structural findings |
|---|---|---:|---:|---:|---|---|
| 1990/1991 | engsoccerdata | 380 | 380 | 380 | 1990-09-01–1991-06-09 | Pass |
| 1995/1996 | engsoccerdata | 462 | 462 | 462 | 1995-09-02–1996-05-26 | Pass; 22 clubs |
| 1996/1997 | engsoccerdata | 462 | 462 | 462 | 1996-08-31–1997-06-23 | Pass; 22 clubs |
| 2011/2012 | engsoccerdata | 380 | 380 | 380 | 2011-08-27–2012-05-13 | Pass |
| 2012/2013 | OpenFootball | 380 | 380 | 380 | 2012-08-18–2013-06-01 | Pass; five source-name differences in overlap comparison; wide matchday span below |
| 2025/2026 | OpenFootball | 380 | 380 | 380 | 2025-08-15–2026-05-24 | Pass; scorer annotations and split/repeated round headers handled; wide spans below |

The historical original actually contains **27,335 rows**, season-start labels
1928–2024, and tier 1 throughout. There are 27,245 rows labelled `league` and
90 labelled `phase2`. Its earliest season corresponds to calendar-1929 play but
is labelled 1928. The 1986 season contains 396 rows; the format cannot be treated
as a simple ordinary 18-team double round robin throughout. These earlier eras
are inventory observations, not newly approved acquisition/standardization scope.

For each requested historical season, every record has tier `1`, round `league`
and no populated group field. No lower division or playoff row was silently
included in those season checks. All requested records have dates, nonnegative
integer goals and matching FT strings. There are no missing pairings, duplicate
ordered fixtures, same-team/date collisions, invalid dates, season-boundary
violations, normalized team-name collisions or unbalanced home/away allocations.

Both text sources decode strictly as UTF-8. The 2012/13 original has 626 CRLF line
endings; the 2025/26 original uses LF. Accents remain unchanged, including
Atlético, Málaga, Coruña and Alavés. The older CSV uses unaccented variants in the
inspected seasons. No normalization or source-name replacement was written.
The parser checks stated weekdays; neither text season has a weekday mismatch.

The 2012/13 source uses `v` fixtures and 38 matchday headings. The 2025/26 source
uses score-in-the-middle fixtures, 522 scorer-annotation lines, and 42 round
headings for split/revisited scheduling. Scorer text is preserved diagnostically
and never interpreted as extra fixtures; unbalanced annotations and unknown text
fail parsing. No explicit awarded/resumed-status annotation occurs in the six
inspected seasons. **This absence does not establish ordinary uninterrupted play.**

### Scheduling candidates requiring later historical review

These spans are computed from printed match dates within a round label. They
indicate irregular scheduling to inspect, not proven errors or eligibility decisions:

| Source season / round | Earliest–latest printed date |
|---|---|
| 2012/13, Matchday 3 | 2012-09-01–2012-09-26 |
| 2025/26, Regular Season 6 | 2025-08-27–2025-09-25 |
| 2025/26, Regular Season 19 | 2025-12-02–2026-01-12 |
| 2025/26, Regular Season 16 | 2025-12-12–2026-02-18 |
| 2025/26, Regular Season 23 | 2026-02-06–2026-03-04 |

No original schedule, resumption event or administrative outcome is inferred from
these spans. Later review must distinguish actual playing dates from scheduled
or completion dates. The historical CSV also contains one out-of-sample 1979
note, `1-0 win awarded to AD Almeria` for CD Malaga–AD Almeria. Its README separately
mentions an omitted annulled Málaga–Salamanca result. These are warnings against
assuming that all older coverage is complete ordinary played-match data.

## Source boundary and overlap

The proposed selection ends engsoccerdata at 2011/12 and begins OpenFootball at
2012/13, leaving no season gap. The acquired historical CSV also contains
2012/13, enabling comparison **without downloading another dataset**.

Its 2012/13 slice independently passes structural checks: 380 dated/scored rows,
20 clubs and complete ordered fixtures. A manually explicit bijective diagnostic
mapping covers all 20 teams. Five labels differ:

| OpenFootball | engsoccerdata |
|---|---|
| Athletic Club | Athletic Bilbao |
| Atlético Madrid | Atletico Madrid |
| Deportivo La Coruña | Deportivo La Coruna |
| Málaga CF | Malaga CF |
| RC Celta | Celta Vigo |

After that mapping, all **380 dates and full-time scores agree**, with zero
unmatched pairings and zero discrepancies. Both physical line locations are
available through the parsed assessment. No files were merged, corrected or
aliased into a derivative. Cross-source agreement is not independent historical
verification: upstream lineage remains unestablished. The historical CSV stops
at 2024/25, so no 2025/26 overlap comparison is possible from these three files.

## Technical compatibility and permissions

Required fields can be extracted into the established eight-column schema in a
future authorized phase. Preserve source labels, translate season-start years to
YYYY/YYYY, use ISO dates, and delegate deterministic IDs to the existing shared
importer. Stage/status metadata belongs in provenance/exception sidecars. No
standardized CSV, match IDs, application data changes or model fitting were
produced by this assessment.

Technical usability is **PASS for these six seasons**. Historical confidence is
**structural only**, supplemented by the bounded 380-match overlap agreement;
no final-status or exhaustive independent-result certification is claimed.

Usage rights remain qualified:

- engsoccerdata: pinned README states noncommercial use; DESCRIPTION declares GPL
  >=2 for the package. Dataset-specific application, upstream rights and
  statistical model-training permission remain unresolved. This acquisition is
  private academic feasibility and grants no new downstream permission.
- OpenFootball: pinned CC0 1.0 covers rights the affirmer holds; its disclaimer
  does not clear third-party rights. This is more permissive at contributor level
  but not a warranty of upstream rights. No model training or redistribution is
  authorized or performed here.

## Reproduction and exact generated inventory

Public additions are `scripts/collect_la_liga_feasibility.py`,
`scripts/validate_la_liga_feasibility.py`, `tests/test_la_liga_feasibility.py`,
this report, and appended decisions in `PLANNING_LOG.md`.

Six new private JSON files accompany the nine acquired originals:

1. `protected_competitions_before.json` — complete 428-file baseline.
2. `protected_accessible_before.json` — superseded timed-read diagnostic.
3. `source_paths.json` — immutable Git path/blob checks.
4. `acquisition.json` — source receipts, checksums, times and rights statements.
5. `feasibility_assessment.json` — six season reports, source-line records,
   historical inventory and overlap comparison.
6. `feasibility_diagnostics.json` — wide-round candidates, five differing aliases,
   assessment/code fingerprints and diagnostic-baseline clarification.

The collector refuses existing destinations and downloads only the three pinned
datasets plus six notices. Do not rerun it to overwrite this snapshot. The
validator's `--check` performs offline regeneration and byte comparison:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -B -m scripts.validate_la_liga_feasibility --check
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 .venv/bin/python -B -m pytest tests/test_la_liga_feasibility.py -q -p no:cacheprovider
```

Fresh reproduction requires the retained private baseline and input bundle;
synthetic tests do not require real datasets. No historical claim is validated
merely by passing a synthetic test.

## Validation results and next gate

- Offline assessment creation and full byte-reproduction `--check`: PASS.
- New synthetic tests: **17 passed** (approved source scope, formats, CRLF/accents,
  scorer exclusion, strict headings, score/date/fixture/collision guards).
- Complete 428-file prior-competition baseline: unchanged.
- All 15 new private artifacts are ignored; no private paths are Git-tracked.
- `git diff --check`: PASS.

Technical issues were environmental: sandbox DNS required approved network
execution for GitHub; iCloud reads delayed baseline access and virtual-environment
imports. A diagnostic pytest import timed out after 15 seconds while reading
Pygments; a subsequent bounded test run succeeded, 17 tests in 0.65 seconds.
A delayed earlier validator invocation refused to overwrite the already-created
assessment, as designed. No source data were replaced.

Recommend continuing the proposed two-source strategy after separate approval:
acquire only the remaining selected OpenFootball season originals, structurally
validate each selected historical season from the existing CSV, and then conduct
independent historical/exception review before standardization. Retain current
source labels and rights restrictions. Do not acquire 2026/27 or pool additional
earlier eras under flat-format assumptions. No full acquisition, standardization,
training, commit, push or merge has occurred.
