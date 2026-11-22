# La Liga Phase 7: reproducible standardization

Date: 2026-11-22. Original `toto` worktree, branch `feature/data-collection`. Phase 7 only; stopped before Phase 8 independent review.

## Measured outputs and reconciliation

**13,843 accepted + 0 definitively excluded + 1 unresolved HOLD OUT = 13,844 source records.** Exactly one record is omitted from the screened CSV. The unresolved category is separate from definitive exclusions; do not add the same omitted fixture twice. Counts were measured after importing and applying the approved policy, not forced to a target accepted total.

| Artifact under `data/private/spain/la_liga/` | Contents | SHA-256 |
|---|---|---|
| `la_liga_audit_archive_1990_2025.json` | Full audit archive; 13,844 records, original parsed/raw values, provenance and date/eligibility metadata; 33,838,571 bytes | `d33881fdbf9557a9866b02c1142e9fad7496e175383310abeda5093d265450ae` |
| `la_liga_exceptions_1990_2025.json` | Five approved exception decisions, shared-ID links, preserved uncertainty, chronological/rights policy; 46,693 bytes | `b621d3cbe731bd7c5fc6cc2faaa072d353249b0b31aa8c94b569f19ad7136653` |
| `la_liga_standardized_1990_2025.csv` | Screened eight-column CSV; 13,843 rows; 1,734,390 bytes | `5cee37c7bacd76877f366bda6f496617830550707f5efedc7e5ab65fb6372ab2` |

`la_liga_standardization_manifest.json` records per-season coverage, reconciliation, input/source/code/test fingerprints, output hashes/sizes, goal-derived outcome totals, exact restricted IDs and measured uncertainty preservation. All four artifacts are private and Git-ignored. Filename end-year `2025` denotes the starting year of the final season, **2025/26**. No 2026/27 data or the 90 historical 1986/87 `phase2` rows were added.

## Importer, schema and validation

The canonical league is **La Liga**. The screened header is exactly:

```text
match_id,date,league,season,home_team,away_team,home_goals,away_goals
```

The adapter reuses the existing `standardize_england_results.convert_rows` bridge, `historical_import.import_historical_csvs`, shared deterministic ID implementation and public historical loader/validator. No parallel ID generator creates records. An independent SHA-256 identity calculation verifies importer-created IDs from `[league, season, ISO date, home team, away team]`; goals do not participate in identity. No team alias/canonicalization table was applied: original season-specific team labels are preserved. The bridge refuses any changed fact or rejected/duplicate/conflicting input.

All fifteen source documents match their original receipt byte sizes, SHA-256 and Git blob identities. Original pinned revisions, exact URLs, retrieval timestamps and licensing/provenance fields are carried into the archive/manifest. The selected 36-season population is parsed from the original files rather than importing a previous standardized output.

Validation checks required fields, exact schema order, season/date validity including the 2019/20 extended season, nonnegative integer goals, goal-derived outcomes, distinct teams, ordered season-pair uniqueness, source/audit-ID bindings, unique deterministic shared IDs and unchanged source facts. Reversed-input conversion must produce identical bytes. The screened subset is separately converted through the shared importer/loader and must equal the policy-partitioned CSV byte-for-byte.

Independent inspection of the saved outputs (separate from the build/manifest counts) checked all 13,844 source bindings and literal raw source records, every screened row/date/score/team/ID, all five exceptional links, the precise restricted-ID absence and saved artifact hashes. It passed. CSV raw text, including line endings and quoted logical records, is preserved outside the eight-column export.

Goal-derived screened outcomes: **6,597 home wins (1), 3,598 draws (X), 3,648 away wins (2)**. Full archive outcomes: **6,598 / 3,598 / 3,648** respectively. The held record’s source score derives a home-win label internally; this does not certify its official outcome.

## Approved exception decisions and shared IDs

| Decision | Fixture | Source date / score | Screened treatment | Shared match ID |
|---|---|---|---|---|
| LL6-01 | Real Madrid–Rayo Vallecano | 2015-12-20 / 10–2 | Included; effective 2015-12-20 | `76c64aed66d861d28c52b7cc551120dd650684e8eff3e8f54c5705042b953025` |
| LL6-02 | FC Barcelona–CA Osasuna | 2025-03-27 / 3–0 | Included; effective 2025-03-27 | `e81c6e060002e852cdc27474d3b9f2c37a984fbf1b5601605ddd70c8bbf3de65` |
| LL6-03 | Real Madrid–Real Sociedad | 2005-01-05 / 2–1 | Included; effective 2005-01-05; original kickoff 2004-12-12 | `24ea388200cdcbcc1a308686e69ed913bb5d2f36ef5104cedb9c9b0498a14659` |
| LL6-04 | Granada CF–Athletic Club | 2023-12-11 / 1–1 | Included; effective 2023-12-11; original kickoff 2023-12-10 | `1fccfd72f2a7054776b95de49dfc866fe513a8e32da9f01d034e24dfd1ce2f90` |
| LL6-05 | Rayo Vallecano–Real Oviedo | 2026-03-04 / 3–0 | UNRESOLVED / HOLD OUT; no effective result date | `083b9316e4189579c5e6b1498eb8214283a43df5d59bd13befd3c01d25d2094f` |

The exact held fixture is `openfootball/espana/2025-26/1-liga.txt`, physical line **780**, source Rayo Vallecano–Real Oviedo **2026-03-04, 3–0**, recorded halftime 1–0. Source audit ID `laliga:5a6b3dcf91f5e0fa5311fdc6a0249f71cf21c3fa99db993843a33b5697631f87` maps to shared observation ID `083b9316e4189579c5e6b1498eb8214283a43df5d59bd13befd3c01d25d2094f`. That shared ID is absent from the screened CSV. The requested administrative 0–3 result was not substituted.

The full JSON archive retains all 13,844 original parsed records and raw source records, complete per-file acquisition receipts, source audit/shared-ID links, goal-derived labels and separate assessments. Each record has a nullable `screened_match_id`. The held fixture has `screened_match_id: null` and `effective_result_date: null`; its archive projection explicitly means **unverified source date only**, not known result availability. The archive must never be used directly as model-training input.

LL6-01 retains 10–2 unchanged. LL6-02 retains 3–0 with the frozen RFEF appeal evidence. LL6-03 and LL6-04 preserve original kickoff and completion dates separately; their exported dates are the approved completion/result-availability dates. Because their original source dates already equal completion dates, no factual source-date correction was needed. No date, score or team-identity repair was invented or applied.

## Date semantics, uncertainty and separate eligibility gates

The screened date denotes the approved calendar day the final result became available. For ordinary fixtures it remains the unchanged source playing date, explicitly an uncertified availability proxy. For interrupted fixtures it is the verified completion date. Source and event dates remain in audit metadata; no early kickoff date replaces completion in the screened CSV.

The preserved downstream rule is **effective result date strictly before prediction date**; same-day results are unavailable at date precision. The existing Phase 6 guard is retained and tested. Future consumers must enforce it; this phase does not integrate a dataset or training/evaluation pipeline into the application. Newly identified unresolved final outcomes must HOLD OUT until an explicit evidence-backed approved policy revision; missing/corrupted/misbound decisions fail, rather than defaulting to inclusion.

Preserved uncertainty is measured against actual output links:

- **34 scheduling cases:** 23 documented, 8 partial, 3 unresolved; frozen classifications unchanged.
- **52 diagnostic outliers:** 51 included, one explicit Rayo–Oviedo final-outcome holdout; **49 lack individual full-fact certification**.
- **8 unverified historical samples:** all eight remain unverified and included, not relabelled erroneous.
- **34 factual verifications / 13,810 unverified source fixtures:** unchanged historical assurance categories, not population certification.
- **0 model-training suitability clearances / 0 licensing clearances.** Technical screening acceptance grants neither.

No fixture is automatically corrected/excluded because its matchday spans a long interval or its historical verification is incomplete. The 18 club-label variant groups and identity-boundary limitations remain unresolved/noncanonical as documented previously; no global mappings were applied.

## Season-by-season measured coverage

| Season | Source/archive | Screened accepted | Definitively excluded | Unresolved HOLD OUT |
|---|---:|---:|---:|---:|
| 1990/1991 | 380 | 380 | 0 | 0 |
| 1991/1992 | 380 | 380 | 0 | 0 |
| 1992/1993 | 380 | 380 | 0 | 0 |
| 1993/1994 | 380 | 380 | 0 | 0 |
| 1994/1995 | 380 | 380 | 0 | 0 |
| 1995/1996 | 462 | 462 | 0 | 0 |
| 1996/1997 | 462 | 462 | 0 | 0 |
| 1997/1998 | 380 | 380 | 0 | 0 |
| 1998/1999 | 380 | 380 | 0 | 0 |
| 1999/2000 | 380 | 380 | 0 | 0 |
| 2000/2001 | 380 | 380 | 0 | 0 |
| 2001/2002 | 380 | 380 | 0 | 0 |
| 2002/2003 | 380 | 380 | 0 | 0 |
| 2003/2004 | 380 | 380 | 0 | 0 |
| 2004/2005 | 380 | 380 | 0 | 0 |
| 2005/2006 | 380 | 380 | 0 | 0 |
| 2006/2007 | 380 | 380 | 0 | 0 |
| 2007/2008 | 380 | 380 | 0 | 0 |
| 2008/2009 | 380 | 380 | 0 | 0 |
| 2009/2010 | 380 | 380 | 0 | 0 |
| 2010/2011 | 380 | 380 | 0 | 0 |
| 2011/2012 | 380 | 380 | 0 | 0 |
| 2012/2013 | 380 | 380 | 0 | 0 |
| 2013/2014 | 380 | 380 | 0 | 0 |
| 2014/2015 | 380 | 380 | 0 | 0 |
| 2015/2016 | 380 | 380 | 0 | 0 |
| 2016/2017 | 380 | 380 | 0 | 0 |
| 2017/2018 | 380 | 380 | 0 | 0 |
| 2018/2019 | 380 | 380 | 0 | 0 |
| 2019/2020 | 380 | 380 | 0 | 0 |
| 2020/2021 | 380 | 380 | 0 | 0 |
| 2021/2022 | 380 | 380 | 0 | 0 |
| 2022/2023 | 380 | 380 | 0 | 0 |
| 2023/2024 | 380 | 380 | 0 | 0 |
| 2024/2025 | 380 | 380 | 0 | 0 |
| 2025/2026 | 380 | 379 | 0 | 1 |

## Reproduction, protection and changed files

```sh
# Create exclusively when none of the four outputs already exists:
PYTHONPATH=src:. .venv/bin/python -B -m scripts.standardize_la_liga_results
# Rebuild and compare existing bytes; no persistent files replaced:
PYTHONPATH=src:. .venv/bin/python -B -m scripts.standardize_la_liga_results --check
PYTHONPATH=src:. .venv/bin/python -B -m pytest tests/test_la_liga_standardization.py -q -p no:cacheprovider
```

Temporary importer bridge files remain inside private storage and are removed on success/failure. Existing outputs are never overwritten by the CLI. A preflight checks every destination before generating/writing artifacts. There is no network acquisition path in the new adapter.

New public files:

- `scripts/standardize_la_liga_results.py` — private output adapter, independent fact/ID/partition checks and deterministic manifest.
- `tests/test_la_liga_standardization.py` — 27 focused synthetic tests, including shared-importer integration and missing/corrupt/misbound decision failures.
- `docs/la-liga-standardization.md` — this measured Phase 7 report.

`PLANNING_LOG.md` is appended only. Earlier acquisition, structural validation, historical review and policy documents/scripts/tests remain byte-identical. New private artifacts are the four outputs listed above plus `phase7_protected_before.json` (504 fingerprints) and `phase7_history_prefixes.json` (append-only planning-log seal).

All six previously completed competitions remain protected by their existing 428-file baseline. Phase 7 adds a 504-file protection scope covering earlier private evidence and public implementation/documentation; no application data paths or promotional files were changed. Final regression/reproduction measurements are appended after execution.

## Remaining limitations and review gate

Rayo–Oviedo’s recognized final result/applicable date remains unresolved and held out. The eight unverified samples, eleven partial/unresolved scheduling explanations, 49 outliers without individual certification and club-identity caveats remain evidence limits, not automatic extra exclusions.

engsoccerdata retains its noncommercial-use/GPL-package/upstream-scope uncertainty; OpenFootball CC0 covers rights held without a third-party clearance warranty. No new model-training or redistribution permission is inferred. All real-data artifacts remain private and must not be staged.

Seven previously unverified app/launcher tests remain a separate final-project regression item; no full-suite or UI success is implied. Phase 7 stops before independent Phase 8 review, application integration, model training or Git publication.

## Final measured test results and environment issue

The **27 focused Phase 7 tests passed in 0.78 seconds**. The non-UI regression suite then completed with **802 passed in 296.74 seconds**. Its elapsed time includes a diagnosed iCloud file-read stall; the same running suite resumed after local availability was restored, without being restarted or skipping additional tests. The seven pre-existing app/launcher tests were explicitly excluded and remain a separate closure item.

The read stalls were confirmed by zero-CPU process states, a native stack sample blocked in `read`, open-file inspection and macOS `dataless` flags. They affected the Phase 6 policy, the new manifest, an existing application module and older protected source files. macOS accepted requests to restore local copies of existing files; no new source datasets were acquired and no source/application content was edited. Hydration changes local availability, not the intended file contents; final checksum verification remains required.

Final completion: the outstanding checksum/regeneration check finished successfully after existing placeholders became locally readable. **All four saved Phase 7 artifacts regenerated byte-for-byte**, including the manifest. The build's before/after protection checks passed for all **504** frozen artifacts; all six prior competitions' 428 protected artifacts and original Phase 2–6 evidence remain unchanged. There was no test timeout or test restart in this phase; the environmental stall delayed completion but did not produce a validation failure. No full app/launcher-suite success is claimed.

Final housekeeping additionally confirmed **493 private files ignored / zero private files tracked**, an empty Git index, unchanged `feature/data-collection` HEAD `2f2bfe1542c2460111ae685621d138874fa69f52`, matching output/code hashes and clean whitespace checks. A later helper was manually interrupted after blocking on an existing NumPy bytecode placeholder; an equivalent standard-library-only integrity/privacy check passed. This interruption was not a test or output-regeneration failure. No dependency was installed or updated.
