# Ligue 1 Phase 7 — screened standardization and complete audit archive

2026-11-22. Original `toto` worktree, `feature/data-collection`, HEAD `81225118ced664f113c19b87cff8095b0333ccda`. The user approved all Phase 6 decisions and Phase 7 standardization of the acquired material only. No new historical decision, source acquisition, application/promo modification, model training or Git publication occurred.

## Reconciliation and bounded scope

| Classification | Observations |
|---|---:|
| Complete original audit population | 12,707 |
| Score-bearing originals | 12,606 |
| Screened standardized results | 12,601 |
| Administrative HOLD OUT | 4 |
| Disputed-date HOLD OUT | 1 |
| Cancelled / NOT PLAYED | 101 |
| Other definitive exclusions | 0 |

The disjoint partition is **12,707 = 12,601 + 4 + 1 + 101**. These figures were independently reproduced rather than used to synthesize missing rows. Every source audit ID appears exactly once in the archive; the CSV is precisely the included archive projections, with no silent loss or extra row. A holdout or not-played observation has no approved standardized projection or screened ID.

Coverage remains **35 represented seasons in the planned 36-season 1990/91–2025/26 window**. All of 1994/95 (expected 380 fixtures) and the Nantes–Toulouse 2006/07 pairing are absent from acquired source material. They are open acquisition objectives, not fabricated archive observations or hidden exclusions. This is not a complete historical Ligue 1 dataset.

## Outputs

All four outputs are Git-ignored under `data/private/france/ligue_1/`:

- `ligue_1_standardized_1990_2025.csv`: screened eight-column results only.
- `ligue_1_audit_archive_1990_2025.json`: every original observation, including holdouts and cancellations, with immutable source values and full provenance.
- `ligue_1_exceptions_1990_2025.json`: all approved decisions, 108 explicit exception links, evidence registry, grouped uncertainty, coverage gaps, chronology obligations and licensing restrictions.
- `ligue_1_standardization_manifest.json`: source receipts, input/code fingerprints, counts, coverage, earlier-ID collision checks and hashes of the three data outputs. The separate verification receipt records the manifest's own SHA-256, avoiding a self-referential digest.

Filenames use season-start years; the last represented season is 2025/2026. The archive includes 14 immutable original source documents in its provenance inventory, including preserved diagnostic sources not substituted for the primary source window.

## Shared schema and IDs

The CSV header is exactly:

```text
match_id,date,league,season,home_team,away_team,home_goals,away_goals
```

Every screened row uses `league = "Ligue 1"`, consecutive `YYYY/YYYY` seasons, canonical ISO calendar dates and nonnegative integer goal fields. Historical CSV division labels and modern source competition headings are preserved in audit metadata. No global team-name aliasing was introduced.

The established shared historical importer generates IDs and validates the CSV. An independent implementation checks SHA-256 of UTF-8 compact JSON `[league, season, date, home_team, away_team]`, with Unicode preserved. The exporter independently checks exact source/policy facts, schema order, goal types, unique IDs, directed season pairings and canonical `(league, season, date, home_team, away_team)` ordering. Reversed input plans produce identical shared-importer bytes. CSV parsing/serialization roundtrips identically and the public historical loader accepts the same match facts.

The collision check scanned all 11 previously preserved exact-schema standardized CSVs, including existing ongoing/legacy outputs, containing 100,647 distinct IDs. No new Ligue 1 ID collided. That inventory is not a redefinition of the eight completed competitions' historical totals; its exact paths and hashes are in the manifest.

## Approved historical decisions implemented

| Fixture | Screened treatment | Preserved audit context |
|---|---|---|
| Bastia–Lyon, 2017-04-16 | HOLD OUT | Modern 0–0 awarded representation, overlapping CSV 0–3 binding, uncertain numerical award and finality. No ordinary draw inferred. |
| Nantes–Bastia, 2013-08-10 | HOLD OUT | Source 0–0, penalty winner evidence, decision/appeal/judicial dates and unresolved numeric administrative score. |
| Montpellier–Saint-Étienne, 2025-03-16 | HOLD OUT | Original 0–2, interrupted play, ratification 2025-04-02; material finality/availability uncertainty remains. |
| Nantes–Toulouse, 2026-05-17 | HOLD OUT | Original 0–0, interruption, ratification 2026-05-27; no backdating of official availability or assumed exhausted appeals. |
| Auxerre–Lyon, source 1996-10-26 | HOLD OUT | Original 7–0 and date unchanged; 25-versus-26 October discrepancy retained. No correction based on one interview. |
| Nice–Marseille | Include 1–1 on 2021-10-27 | Original interrupted event 2021-08-22, replay order and verified replay context retained separately. |
| Montpellier–Clermont | Include 1–1 on 2023-11-29 | Original abandoned event 2023-10-08, replay order and verified replay context retained separately. Abandoned 4–1 is not substituted. |

The source-bound Phase 6 policy is pinned to SHA-256 `c04e6890ddfb8624446fef19b8fde1a3696e80e2973ca399ea5fe34a5f95f605`. Its regeneration must exactly match the approved policy and assessment before export. Each named decision retains its audit ID, original source/hash/physical location, evidence IDs/URLs, timeline, uncertainty and HOLD OUT reason.

All 1,895 older auxiliary-label contradictions remain unchanged in original audit values. For ordinary included results the shared importer receives an outcome freshly derived from accepted numeric goals, not the defective source D. Actual numeric draws stay draws; there is no global D→A replacement. The screened goal-derived totals are H=5,832, D=3,581, A=3,188. Administrative representations remain controlled by explicit decisions, not this ordinary interpretation. Numeric interpretation does not independently certify historical score accuracy.

The 2019/20 archive preserves all **380 scheduled slots**: **279 included played results and 101 NOT PLAYED observations**. Cancelled goals and FT remain null; no zero-score draw is fabricated. NOT PLAYED is distinct from HOLD OUT and unexplained missing data.

The exact source/season-bound Brest rule applies to 38 observations in 1990/91, transforming 18 candidate labels while preserving original names. It reconciles 20 clubs and 380 unique directed pairings, with no ID duplication. AC Ajaccio and Gazélec remain distinct; the 38 unmatched cross-source pairings per side and other historical continuity warnings remain visible. No unapproved team or date mapping is applied.

## Full audit provenance and uncertainty

Each audit record preserves the complete parsed source observation, original raw literal record, auxiliary labels, goals, teams, source dates, annotations and source line/hash binding. It also records exact source URL, pinned revision, Git blob SHA-1, file SHA-256 and raw-record SHA-256. Source-document receipts preserve original paths, attribution, retrieval timestamps, bytes and licensing notices. All 14 original file hashes and blob identities were rechecked.

Included records have their exact approved standardized projection and shared match ID; restricted records have neither. Record metadata retains Phase 6 classification, historical fact status, exception decision, original/effective chronology, replay/administrative dates, scheduling context and identity findings. Original Phase 4 chronology remains inside the unchanged original record; approved chronology is separately identified, so earlier unset/provisional fields are not silently rewritten.

The sidecar carries the complete approved policy, 101 cancellation decisions plus seven named cases, all 118 bibliographic entries, 40 scheduling contexts / 394 affected slots, grouped label-defect IDs, club-identity findings and individual historical review classifications. All original review flags remain in the archive, including 2,473 uniquely flagged observations from Phase 4. The 584 fixture-level review queue and earlier grouped investigations remain frozen in their existing evidence files.

## Chronological safety and its limits

Unknown or materially unresolved administrative/date results never reach the CSV. Replayed results use the approved replay dates. Ordinary dates remain source-reported calendar days; they are not claimed to be independently certified result-availability timestamps. The archive/sidecar retains this distinction and the stronger availability flag only where supported.

Existing policy tests enforce strictly earlier availability: same-day, future or required unknown dates fail, as do unresolved outcomes, modified decisions, invalid bindings and out-of-scope identities. Training requires separate eligibility, verified availability, suitability and licensing gates. **No record is currently cleared for model training.** Future evaluators must actually apply these guards and the audit/sidecar availability evidence; loading the eight-column CSV alone cannot enforce all historical availability or rights restrictions. No application consumer or model was integrated in this phase.

## Independent regeneration and tests

A separate Python process reparsed the immutable sources through the independent Phase 4 parser and byte-compared both frozen structural outputs. It then regenerated all four Phase 7 outputs into a new temporary directory and compared their complete bytes and SHA-256 against the saved artifacts. Additional checks independently verified CSV/archive subset identity, ID hashing, goals against originals, all five holdouts, 101 null-score cancellations, 2019/20 counts, 1,895 preserved labels, replay dates, ratification metadata and Brest changes.

| Output | Bytes | SHA-256 | Independent comparison |
|---|---:|---|---|
| `ligue_1_standardized_1990_2025.csv` | 1569127 | `e9343d10f68794d64e7184bcf67fb7fc4c1496e50ddb0de92c100961641d134b` | Byte-identical |
| `ligue_1_audit_archive_1990_2025.json` | 60896009 | `69ebabb83f5d6f63eec9c76c2f8c887b1750f2fb399cbc8d5d6334b4093be863` | Byte-identical |
| `ligue_1_exceptions_1990_2025.json` | 1358616 | `d14e6ac9237d57eba6ddb3dd8727d04ce815225a29ed92bbd2a9c31100d8e1d9` | Byte-identical |
| `ligue_1_standardization_manifest.json` | 58042 | `8f439d3887011dc077a91631e63280c316d110d01d4e2a63aaf3755e9ad686c2` | Byte-identical |

Full repository suite: **1,299 passed**, zero failed/errors/skips. This includes **224 focused Ligue 1 tests**, **32 new standardization tests**, six app tests and one launcher test. The earlier test-draft run caught two synthetic fixture setup errors; both were corrected in the new test file before final verification. The successful final run completed in 16.35 seconds (pytest 15.55 seconds). No test remains unverified.

The unchanged offline Python 3.13.12 environment outside iCloud was reused with pytest 9.1.1 and pandas 3.0.6. No installation, environment rebuild or original `.venv` change. Bytecode and test-cache output were disabled/redirected; shared-importer bridge files were temporary and removed. No new original dataset or replacement source was acquired.

To reproduce from repository root using the working environment:

```sh
PYTHONPATH=src:. python -B -m scripts.standardize_ligue1_results --check
PYTHONPATH=src:. python -B -m scripts.standardize_ligue1_results --write --output-directory /tmp/new-ligue1-phase7
```

Use a fresh output directory for independent regeneration. The writer accepts identical existing outputs and refuses to overwrite changed bytes. `--init` is baseline/approval initialization, not routine regeneration. No online access is required for either command.

## Season-level accounting

| Season | Archived | Screened | HOLD OUT | NOT PLAYED |
|---|---:|---:|---:|---:|
| 1990/1991 | 380 | 380 | 0 | 0 |
| 1991/1992 | 380 | 380 | 0 | 0 |
| 1992/1993 | 380 | 380 | 0 | 0 |
| 1993/1994 | 380 | 380 | 0 | 0 |
| 1994/1995 | 0 | 0 | 0 | 0 |
| 1995/1996 | 380 | 380 | 0 | 0 |
| 1996/1997 | 380 | 379 | 1 | 0 |
| 1997/1998 | 306 | 306 | 0 | 0 |
| 1998/1999 | 306 | 306 | 0 | 0 |
| 1999/2000 | 306 | 306 | 0 | 0 |
| 2000/2001 | 306 | 306 | 0 | 0 |
| 2001/2002 | 306 | 306 | 0 | 0 |
| 2002/2003 | 380 | 380 | 0 | 0 |
| 2003/2004 | 380 | 380 | 0 | 0 |
| 2004/2005 | 380 | 380 | 0 | 0 |
| 2005/2006 | 380 | 380 | 0 | 0 |
| 2006/2007 | 379 | 379 | 0 | 0 |
| 2007/2008 | 380 | 380 | 0 | 0 |
| 2008/2009 | 380 | 380 | 0 | 0 |
| 2009/2010 | 380 | 380 | 0 | 0 |
| 2010/2011 | 380 | 380 | 0 | 0 |
| 2011/2012 | 380 | 380 | 0 | 0 |
| 2012/2013 | 380 | 380 | 0 | 0 |
| 2013/2014 | 380 | 379 | 1 | 0 |
| 2014/2015 | 380 | 380 | 0 | 0 |
| 2015/2016 | 380 | 380 | 0 | 0 |
| 2016/2017 | 380 | 379 | 1 | 0 |
| 2017/2018 | 380 | 380 | 0 | 0 |
| 2018/2019 | 380 | 380 | 0 | 0 |
| 2019/2020 | 380 | 279 | 0 | 101 |
| 2020/2021 | 380 | 380 | 0 | 0 |
| 2021/2022 | 380 | 380 | 0 | 0 |
| 2022/2023 | 380 | 380 | 0 | 0 |
| 2023/2024 | 306 | 306 | 0 | 0 |
| 2024/2025 | 306 | 305 | 1 | 0 |
| 2025/2026 | 306 | 305 | 1 | 0 |

The zero-observation 1994/95 row denotes missing acquisition, not a historically empty season. The 2006/07 archive has 379 source observations; the missing Nantes–Toulouse administrative case is not supplemented with an invented numeric score.

## Preservation and stopping point

Protected fingerprints passed for all eight previous competitions: **558 private files and 165 tracked public files**, plus **124 frozen Ligue 1 Phase 2–6 entries** and nested earlier baselines. Earlier source originals, generated evidence, scripts/tests/docs and standardized outputs remain unchanged. The planning log is prefix-protected and appended only. No application or promotional worktree files changed.

This phase adds `scripts/standardize_ligue1_results.py`, `tests/test_ligue1_standardization.py`, this document and appended `PLANNING_LOG.md`. Private additions comprise the Phase 7 baseline/approval, four outputs, independent verification, test XML/log/receipt and final verification receipt. All private files are Git-ignored; no private data is tracked or staged. HEAD/index remain unchanged, and the two known `.DS_Store` files remain untracked.

The acquired subset is technically standardized, not fully historically certified or cleared for redistribution/training. The missing 1994/95 season, missing 2006/07 pairing, individual historical uncertainties and all five approved HOLD OUT cases remain open. See [historical review](ligue-1-historical-review.md) and [approved policy](ligue-1-policy.md). Separately authorized gap recovery and source-specific permissions are still required; no full historical completion is claimed.

Stopped after Phase 7. Await user approval before Phase 8 review; no staging, commit, push, merge or next competition.
