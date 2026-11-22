# La Liga Phase 3: completed bounded acquisition and inventory

Date: 2026-11-21. Branch: `feature/data-collection`; original `toto` worktree.
HEAD remains `2f2bfe1542c2460111ae685621d138874fa69f52`.

## Outcome and assurance boundary

The approved 36-season scope, **1990/91–2025/26**, is fully accounted for:
**13,844 observed fixtures / 13,844 usable full-time scores**, matching the
format baseline of 34×380 + 2×462. Counts were measured from source records and
were not filled, deduplicated, corrected or forced to agree with expectations.

Exactly **12 new dataset files** were downloaded, all first-division OpenFootball
2013/14–2024/25 originals. **Three Phase 2 dataset originals were reused**: one
historical CSV and the 2012/13 and 2025/26 text files. There are **15 primary source
files serving 36 seasons**, with **zero missing files, zero unparseable seasons,
zero checksum failures and zero inventory-level score/pairing/date errors**.

**14 source files have scheduling-review candidates**: all 14 OpenFootball
season files, including all 12 new ones. These flags are not proven errors.
The historical CSV lacks equivalent matchday grouping in the selected rows;
absence of wide-round flags there is not evidence of ordinary scheduling.

This is acquisition/inventory only. Inventory checks do not constitute the later
Phase 4 structural-validation release, independent historical certification,
model-training eligibility or standardization. No match IDs or standardized data
were generated. No original date, score, club name or exception status changed.

## Sources, access and provenance

Source split is unchanged:

- engsoccerdata 1990/91–2011/12: reuse
  `jalapic/engsoccerdata/data-raw/spain.csv`, revision
  `872c5c354161ace8408f3091b758c6af4cccca94`.
- OpenFootball 2012/13–2025/26: use only `YYYY-YY/1-liga.txt` at revision
  `80035a93dd4920985af52aa097a54a6fb888563b` in `openfootball/espana`.
  Phase 2 endpoints were not redownloaded.

The collector verified all 12 exact paths in a complete pinned Git tree before
fetching any additional dataset. It saved the original tree JSON and an access
receipt, then checked downloaded size and Git blob identity before saving each
original and its individual `.provenance.json`. Each receipt includes season,
competition, exact source URL, repository/commit, original path/filename, format,
UTC retrieval timestamp, byte size, SHA-256, Git blob SHA-1, and references to
unchanged Phase 2 source/licence metadata.

Additional file URLs have this exact template, for starting years 2013–2024 only:

`https://raw.githubusercontent.com/openfootball/espana/80035a93dd4920985af52aa097a54a6fb888563b/YYYY-YY/1-liga.txt`

Requests were sequential, spaced at least five seconds apart by request start,
with no retries. The collector stops and records any access/fetch failure; none
occurred. No Football-Data, other division, full-detail alternative, 2026/27 file,
unapproved season or additional source dataset was requested.

A complete-cache rerun was tested with network access explicitly disabled in
process: **zero requests, zero downloads and no changed artifacts**. Each cached
original must match its original receipt and pinned Git blob before reuse.
Incomplete original/receipt pairs require manual inspection instead of an
unrecorded replacement. The aggregate manifest is compared on subsequent runs,
not overwritten.

## Full measured inventory

H = engsoccerdata historical CSV; O = OpenFootball season file. The final column
counts round labels whose printed match dates span at least 14 days; it is a
review trigger rather than an error count.

| Season | Source | Observed | Usable scores | Expected | Clubs | Source date coverage | Wide rounds |
|---|---|---:|---:|---:|---:|---|---:|
| 1990/1991 | H | 380 | 380 | 380 | 20 | 1990-09-01–1991-06-09 | 0 |
| 1991/1992 | H | 380 | 380 | 380 | 20 | 1991-08-31–1992-06-07 | 0 |
| 1992/1993 | H | 380 | 380 | 380 | 20 | 1992-09-05–1993-06-20 | 0 |
| 1993/1994 | H | 380 | 380 | 380 | 20 | 1993-09-04–1994-05-15 | 0 |
| 1994/1995 | H | 380 | 380 | 380 | 20 | 1994-09-03–1995-06-18 | 0 |
| 1995/1996 | H | 462 | 462 | 462 | 22 | 1995-09-02–1996-05-26 | 0 |
| 1996/1997 | H | 462 | 462 | 462 | 22 | 1996-08-31–1997-06-23 | 0 |
| 1997/1998 | H | 380 | 380 | 380 | 20 | 1997-08-30–1998-05-16 | 0 |
| 1998/1999 | H | 380 | 380 | 380 | 20 | 1998-08-29–1999-06-20 | 0 |
| 1999/2000 | H | 380 | 380 | 380 | 20 | 1999-08-21–2000-05-20 | 0 |
| 2000/2001 | H | 380 | 380 | 380 | 20 | 2000-09-09–2001-06-17 | 0 |
| 2001/2002 | H | 380 | 380 | 380 | 20 | 2001-08-25–2002-05-11 | 0 |
| 2002/2003 | H | 380 | 380 | 380 | 20 | 2002-08-31–2003-06-22 | 0 |
| 2003/2004 | H | 380 | 380 | 380 | 20 | 2003-08-30–2004-05-23 | 0 |
| 2004/2005 | H | 380 | 380 | 380 | 20 | 2004-08-28–2005-05-29 | 0 |
| 2005/2006 | H | 380 | 380 | 380 | 20 | 2005-08-27–2006-05-20 | 0 |
| 2006/2007 | H | 380 | 380 | 380 | 20 | 2006-08-26–2007-06-17 | 0 |
| 2007/2008 | H | 380 | 380 | 380 | 20 | 2007-08-25–2008-05-18 | 0 |
| 2008/2009 | H | 380 | 380 | 380 | 20 | 2008-08-30–2009-05-31 | 0 |
| 2009/2010 | H | 380 | 380 | 380 | 20 | 2009-08-29–2010-05-16 | 0 |
| 2010/2011 | H | 380 | 380 | 380 | 20 | 2010-08-28–2011-05-21 | 0 |
| 2011/2012 | H | 380 | 380 | 380 | 20 | 2011-08-27–2012-05-13 | 0 |
| 2012/2013 | O | 380 | 380 | 380 | 20 | 2012-08-18–2013-06-01 | 1 |
| 2013/2014 | O | 380 | 380 | 380 | 20 | 2013-08-17–2014-05-18 | 1 |
| 2014/2015 | O | 380 | 380 | 380 | 20 | 2014-08-23–2015-05-23 | 1 |
| 2015/2016 | O | 380 | 380 | 380 | 20 | 2015-08-21–2016-05-15 | 1 |
| 2016/2017 | O | 380 | 380 | 380 | 20 | 2016-08-19–2017-05-21 | 2 |
| 2017/2018 | O | 380 | 380 | 380 | 20 | 2017-08-18–2018-05-20 | 2 |
| 2018/2019 | O | 380 | 380 | 380 | 20 | 2018-08-17–2019-05-19 | 1 |
| 2019/2020 | O | 380 | 380 | 380 | 20 | 2019-08-16–2020-07-19 | 2 |
| 2020/2021 | O | 380 | 380 | 380 | 20 | 2020-09-12–2021-05-23 | 5 |
| 2021/2022 | O | 380 | 380 | 380 | 20 | 2021-08-13–2022-05-22 | 3 |
| 2022/2023 | O | 380 | 380 | 380 | 20 | 2022-08-12–2023-06-04 | 1 |
| 2023/2024 | O | 380 | 380 | 380 | 20 | 2023-08-11–2024-05-26 | 4 |
| 2024/2025 | O | 380 | 380 | 380 | 20 | 2024-08-15–2025-05-25 | 6 |
| 2025/2026 | O | 380 | 380 | 380 | 20 | 2025-08-15–2026-05-24 | 4 |

## Inventory checks and review candidates

For all 36 selected seasons, the scan checks required headers/grammar, top-tier
league selection, complete ordered pairings and balanced home/away appearances,
nonblank/distinct teams, integer nonnegative scores, FT agreement where supplied,
ISO-parsed dates and calendar boundaries, duplicate fixtures, team/date collisions,
UTF-8 decoding, replacement characters, normalized-name collisions, weekday
mismatches and retained source notes/annotations. Names remain source-specific.

No such error was found. This does not prove that a source date is the actual
playing date, that every result is judicially final, or that all matches are
suitable for ordinary played-result modelling.

The 2019/20 season requires an explicit COVID calendar exception. Omitted date
years in July are read as 2020 after the preceding 2020 dates; the resulting
season ends on the source date **2020-07-19**. This is source-date interpretation,
not an original date correction. The ordinary June-cutoff warnings and their
explicit calendar treatment remain visible in the inventory. The original Phase
2 parser and assessment were preserved unchanged.

There are **34 wide-round scheduling candidates** across the 14 OpenFootball
seasons. All five Phase 2 candidates survive with the same dates, labels and
physical source lines; **29 additional candidates** are retained without
correction, exclusion or eligibility reassignment. Several may reflect ordinary
rescheduling, advanced fixtures or COVID interruption. Their meaning is unverified.
Complete labels, date ranges and source lines are in `phase3_inventory.json`.

No explicit awarded/resumed annotation is present in the selected records. This
is a limitation of the source annotations, not clearance of exceptional status.
Known Phase 2 historical administrative/annulment leads remain in the preserved
README, assessment and report and must be considered when planning later review.

The historical original's **90 `phase2` records belong to 1986/87**, outside the
approved window. They are retained verbatim as separate diagnostics and never
included in the 13,844 records. All other historical rows outside the selected
1990–2011 start years remain outside the selected inventory. No extra season,
stage or duplicate-source row is silently merged into the selected scope.

## Preservation and artifact inventory

- All **428** prior England/Germany/Italy artifacts remain SHA-256 identical,
  covering the six completed competitions and their originals, standardized
  outputs, manifests and evidence.
- All **19 Phase 2 artifacts** are fingerprinted and unchanged: 15 private files
  plus the collector, feasibility validator, synthetic tests and feasibility report.
- The Phase 2 acquisition receipts, code/assessment diagnostics, baseline files,
  380-fixture overlap finding and all five prior scheduling candidates remain valid.
- Phase 3 adds **29 private files**: 12 originals, 12 individual receipts, the
  protected baseline, pinned tree JSON, tree receipt, aggregate acquisition
  manifest and complete inventory report. No existing original was rewritten.

Exact new private JSON artifact names at `data/private/spain/la_liga/`:

- `phase3_protected_before.json`
- `phase3_git_tree.json`
- `phase3_git_tree_receipt.json`
- `phase3_acquisition.json`
- `phase3_inventory.json`

Each new original is under `openfootball/espana/YYYY-YY/1-liga.txt`, with its receipt
at `1-liga.txt.provenance.json`. There are **44 private La Liga artifacts** in total.
All remain ignored by Git. No private dataset or evidence path is Git-tracked.

New public code/tests/report are `scripts/collect_la_liga_history.py`,
`scripts/inventory_la_liga_history.py`, `tests/test_la_liga_history.py` and this
report. Only append-only decisions/results were added to `PLANNING_LOG.md`.
Existing Phase 2 public files, application and promotional worktree were untouched.

## Tests and reproduction

- **30 focused tests passed**: 13 new Phase 3 tests and 17 existing Phase 2 tests.
  Coverage includes exact download scope, pinned path/tree/blob checks, cache
  corruption/incomplete receipts, completed-run offline idempotence, COVID year
  inheritance/source-line preservation, review-candidate preservation, and
  reporting invalid scores/dates/weekdays.
- Phase 3 acquisition rerun with networking forbidden: PASS, all 12 reused from
  cache and aggregate manifest identical.
- Phase 3 inventory regeneration: byte-identical.
- Phase 2 feasibility assessment regeneration: byte-identical.
- Original SHA-256/size checks and reused Git blob identities: PASS.
- Existing competition and Phase 2 protected-file checks: PASS.
- Git privacy and `git diff --check`: PASS.

Offline inventory check:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -B -m scripts.inventory_la_liga_history --check
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -B -m scripts.validate_la_liga_feasibility --check
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 .venv/bin/python -B -m pytest tests/test_la_liga_history.py tests/test_la_liga_feasibility.py -q -p no:cacheprovider
```

Private originals and preserved baseline bundles are required to regenerate the
real inventory; synthetic tests do not require real datasets. No source download
is needed to reproduce either saved inventory or Phase 2 assessment.

## Outstanding Phase 4 work and rights

Phase 4 should review all 34 scheduling candidates, establish actual playing,
completion and scheduled dates where relevant, investigate historical exceptional
fixtures (including resumed matches that lack annotations), verify season formats
and aggregate consistency, and examine season-aware club identities and source
lineage. Independent historical certification and any correction proposals remain
separate later work, not accomplished by these inventory counts.

Rights restrictions are unchanged: engsoccerdata's noncommercial statement and GPL
package metadata leave dataset/upstream and statistical-model-training scope
unresolved. OpenFootball CC0 covers only rights held and does not clear third-party
rights. No training, redistribution or public dataset-hosting permission is inferred.

No standardized dataset, application integration, model training, commit, push,
merge or further acquisition is authorized by this report. Stop for user review.
