# Belgian Pro League — Phase 7 standardization

Date: 2026-11-25. Original `toto` worktree, branch `feature/data-collection`, unchanged HEAD `013bb9c195624d5ac290aeb57dae11c4e21c0b5a`.

## Result and purpose

**All8,592 approved INCLUDE events standardized successfully**, exactly once. No approved event was dropped, reclassified or replaced. No Phase8 independent final review or Phase9 publication was performed.

This is the owner-approved **retrospective internal-diagnostics** population. Accepted final historical results may have been determined later; original football dates remain match dates. There is no administrative/publication availability filter. This is not leakage-free historical forecasting, evidence of real-world predictive performance, model-training permission or redistribution clearance.

Private CSV: `data/private/belgium/pro_league/belgian_pro_league_standardized_1995_2026.csv`.

- Data rows: **8,592**, plus one header.
- Bytes: **1,100,562**.
- SHA-256: `8d4e37b1697ae94c8a54d2247476578b3b85f7076e58c2fe5d024a7721791475`.
-31 represented seasons; full36-season target remains incomplete.

```csv
match_id,date,league,season,home_team,away_team,home_goals,away_goals
```

Canonical league: `Belgian Pro League`; season: consecutive `YYYY/YYYY`; ISO date; nonnegative integer goals. UTF-8 without BOM, LF newlines, deterministic shared-importer ordering by league/season/date/home/away. No stage columns were added.

## Shared IDs, conversion and independent validation

Match ID is the existing shared historical-import convention: lowercase64-character SHA-256 of UTF-8 compact JSON `[league,season,date,home_team,away_team]`, `ensure_ascii=False`, separators `(',',':')`. Scores and stages are not added to the shared ID. The code calls the actual shared `import_historical_csvs` with a temporary supported-schema bridge, not a copied alternative importer. The England conversion wrapper is intentionally not used because its regular-season-only pairing check would reject legitimate Belgian playoff rematches. No shared importer, prior standardizer or application file was modified.

The importer accepted all8,592 with zero rejected/duplicate/fixture/conflict issues. The public historical loader independently preserved every date, team, score and ID. A separate projection-free check rebuilds expected rows directly from the frozen Phase6 decisions, preferred source labels and documented name table, independently recomputes IDs, and compares the exact8,592-row subset. All8,592 decision references are unique.

If two approved events share the complete shared-ID identity (even across stages), generation stops with the exact decision references instead of collapsing them or inventing an incompatible suffix. No such collision occurred. All IDs are unique; zero collisions against previous competition data and compatible earlier audit IDs. The prior SerieB audit happens to share the eight-column header: its IDs are checked, but its12,302 audit rows are not added to historical screened totals.

## Full36-season reconciliation

The approved and actual counts agree per season and per represented stage. Coverage labels describe acquired source populations, not claims of complete historical coverage across every stage. Zero observations do not prove a stage was never played.

| Season | Approved INCLUDE | Standardized | HOLD_OUT | NOT_PLAYED | OUT_OF_SCOPE | Coverage |
|---|---:|---:|---:|---:|---:|---|
| 1990/1991 | 0 | 0 | 0 | 0 | 0 | SOURCE GAP |
| 1991/1992 | 0 | 0 | 0 | 0 | 0 | SOURCE GAP |
| 1992/1993 | 0 | 0 | 0 | 0 | 0 | SOURCE GAP |
| 1993/1994 | 0 | 0 | 0 | 0 | 0 | SOURCE GAP |
| 1994/1995 | 0 | 0 | 0 | 0 | 0 | SOURCE GAP |
| 1995/1996 | 306 | 306 | 0 | 0 | 0 | Observed sources; not all-stage completeness |
| 1996/1997 | 306 | 306 | 0 | 0 | 0 | Observed sources; not all-stage completeness |
| 1997/1998 | 306 | 306 | 0 | 0 | 0 | Observed sources; not all-stage completeness |
| 1998/1999 | 306 | 306 | 0 | 0 | 0 | Observed sources; not all-stage completeness |
| 1999/2000 | 306 | 306 | 0 | 0 | 0 | Observed sources; not all-stage completeness |
| 2000/2001 | 306 | 306 | 0 | 0 | 0 | Observed sources; not all-stage completeness |
| 2001/2002 | 306 | 306 | 0 | 0 | 0 | Observed sources; not all-stage completeness |
| 2002/2003 | 272 | 272 | 0 | 0 | 0 | Observed sources; not all-stage completeness |
| 2003/2004 | 306 | 306 | 0 | 0 | 0 | Observed sources; not all-stage completeness |
| 2004/2005 | 306 | 306 | 0 | 0 | 0 | Observed sources; not all-stage completeness |
| 2005/2006 | 306 | 306 | 0 | 0 | 0 | Observed sources; not all-stage completeness |
| 2006/2007 | 306 | 306 | 0 | 0 | 0 | Observed sources; not all-stage completeness |
| 2007/2008 | 306 | 306 | 0 | 0 | 0 | Observed sources; not all-stage completeness |
| 2008/2009 | 306 | 306 | 0 | 0 | 0 | Observed sources; not all-stage completeness |
| 2009/2010 | 210 | 210 | 0 | 0 | 0 | Observed sources; not all-stage completeness |
| 2010/2011 | 240 | 240 | 0 | 0 | 0 | Observed sources; not all-stage completeness |
| 2011/2012 | 240 | 240 | 0 | 0 | 0 | Observed sources; not all-stage completeness |
| 2012/2013 | 240 | 240 | 0 | 0 | 0 | Observed sources; not all-stage completeness |
| 2013/2014 | 240 | 240 | 0 | 0 | 0 | Observed sources; not all-stage completeness |
| 2014/2015 | 240 | 240 | 0 | 0 | 0 | Observed sources; not all-stage completeness |
| 2015/2016 | 240 | 240 | 0 | 0 | 0 | Observed sources; not all-stage completeness |
| 2016/2017 | 240 | 240 | 0 | 0 | 0 | Observed sources; not all-stage completeness |
| 2017/2018 | 240 | 240 | 0 | 0 | 0 | Observed sources; not all-stage completeness |
| 2018/2019 | 269 | 269 | 1 | 0 | 0 | Observed sources; not all-stage completeness |
| 2019/2020 | 232 | 232 | 0 | 8 | 0 | Observed sources; not all-stage completeness |
| 2020/2021 | 330 | 330 | 0 | 0 | 0 | Observed sources; not all-stage completeness |
| 2021/2022 | 329 | 329 | 0 | 1 | 2 | Observed sources; not all-stage completeness |
| 2022/2023 | 306 | 306 | 0 | 0 | 0 | Observed sources; not all-stage completeness |
| 2023/2024 | 312 | 312 | 0 | 1 | 0 | Observed sources; not all-stage completeness |
| 2024/2025 | 313 | 313 | 0 | 0 | 0 | Observed sources; not all-stage completeness |
| 2025/2026 | 121 | 121 | 119 | 0 | 0 | Incomplete pinned snapshot |
| **Total** | **8,592** | **8,592** | **120** | **10** | **2** | Five early gaps remain |

The matrix preserves specific omissions: Lommel2002/03, separate Mouscron2009/10 documentary material, the misplaced modern2021/22 path, missing historical/postseason material and2025/26 incompleteness. It never forces nominal306/240/330 totals where sources or policy differ.

## Stage composition and legitimate rematches

| Stage | Standardized rows |
|---|---:|
| CHAMPIONSHIP | 113 |
| EUROPE | 83 |
| EUROPE_QUALIFICATION | 2 |
| PLAYDOWNS | 24 |
| REGULAR_SEASON | 8370 |
| **Total** | **8,592** |

**222 directed season/team pairings occur twice, representing444 distinct events.** Dates and match IDs distinguish regular/playoff or qualifier rematches. Each remains linked to its frozen stage/group/round/leg bindings in audit. There are no accidental duplicate IDs, identical shared fixture identities or cross-source duplicates. Stage metadata was not discarded merely because it is absent from the shared CSV.

## Complete source-to-event-to-output accounting

| Population | Count / treatment |
|---|---|
| Frozen CSV/TXT observations |10,100 |
| Supplementary2021/22 RSSSF descriptions |334 |
| Combined contributing representations |**10,434**, each represented exactly once in audit |
| Approved conditional events |**8,724** |
| INCLUDE → CSV |**8,592** |
| HOLD_OUT → audit only |**120**:119 missing2025/26 final scores plus Standard–Anderlecht2019 |
| NOT_PLAYED → audit only |**10**:eight COVID cancelled slots plus two no-kickoff awards |
| OUT_OF_SCOPE → audit only |**2** cross-division legs |
| Earlier Mouscron documentary-only entries |**30**, kept outside the10,434/8,724 union:20HOLD_OUT and10NOT_PLAYED |
| Early recovery additions |**0** |

Approved linkage remains1,402 CSV/TXT pairs and306 RSSSF regular counterparts. Two interruption/continuation pairs count representations separately while remaining single events. No source representation is lost, reused or imported twice. Every output row links to one Phase6 decision and all original contributors. Audit contains all8,724 full approved decisions, source records, original score strings, paths/hashes/physical lines, original stage/group/round/leg, accepted dates/results, dispositions, uncertainty flags and original acquisition receipts including revisions/attribution. Non-INCLUDE events have no screened ID or standardized projection.

No cancelled, unscored or uncertain source slot receives invented goals. Documentary-only or research evidence is never promoted to a scored observation. The full archive is explicitly unscreened and must not be used as a training dataset.

## Dates, awards and endpoint checks

| Fixture | Frozen decision | Standardized treatment |
|---|---|---|
| Standard–Anderlecht2019-04-12 |HOLD_OUT|Absent; no inferred final score |
| Standard–Westerlo2024-05-10 |NOT_PLAYED|Absent; award retained in audit |
| Leuven–Mechelen2022-01-15 |NOT_PLAYED|Absent; BAS award retained in audit |
| Union–Beerschot2022-04-10 |INCLUDE5–0|Present5–0 on2022-04-10, never April judgment date |
| Standard–Charleroi2021-12-05 |INCLUDE0–3|Present0–3 on2021-12-05, never January judgment date |
| Beerschot–Cercle |INCLUDE0–1|**2021-07-24** kickoff; original source/completion2021-07-27 separately retained |
| Seraing–Union |INCLUDE0–4|**2022-01-15** kickoff; original source/completion2022-01-18 separately retained |
| Antwerp–Charleroi qualifier |INCLUDE1–2|Present on **2025-05-29**, normalized to historical season labels Antwerp/Charleroi |

No other accepted date or numerical result was changed. All decisions and earlier historical evidence remain frozen; no new historical adjudication was made. Later administrative-result information is permitted by the retrospective policy, with no claim of historically realistic prediction timing.

## Source/season-bound club names

The shared convention trims/validates team-name strings; it does not invent global club identifiers. The new standardizer applies **628 source/season name entries**, using historical source spelling as the coeval anchor where available. It uses only frozen Phase4 within-season modern/historical correspondences and the documented2021/22 RSSSF correspondence table. The misplaced `2021-22/be1.txt` mappings use its actual declared2020/21 season, never the misleading directory year.2025/26 has no historical anchor, so its explicit modern labels remain unchanged.

All contributing representations of an included event must resolve to the same two distinct canonical sides. Missing, contradictory or many-to-one mappings stop generation with the affected event/source context. No materially ambiguous mapping was applied. **60 output rows (114 side fields)** use a coeval normalized spelling instead of the Phase6 representative label; the audit also records2,745 renamed contributing-side bindings across all linked representations. These are different accounting measures. Original labels are preserved.

Examples: modern Club Brugge KV→Club Brugge, RSC Anderlecht→Anderlecht, Standard Liège→Standard;2021/22 RSSSF Union→Royal Union Saint-Gilloise. These are documented season/source correspondences, not global legal mergers. Club/Cercle remain separate; Beerschot entities, historical/modern Mouscron, RWDM/Molenbeek, Genk/predecessors and senior/reserve boundaries are not globally merged. Short source labels can recur across years; equal text is not a claim of uninterrupted legal continuity. Downstream entity integration still requires that separate evidence review. No cross-season alias was extrapolated from2025/26 names or a city name.

## Output artifacts and reproducibility

All artifacts remain private/Git-ignored under `data/private/belgium/pro_league/`:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `belgian_pro_league_standardized_1995_2026.csv` | 1100562 | `8d4e37b1697ae94c8a54d2247476578b3b85f7076e58c2fe5d024a7721791475` |
| `belgian_pro_league_audit_archive_1995_2026.json` | 43032002 | `c0fb514bc031c00c8e93a1deac974c44c43dd42a4be21df2590a91d77440c454` |
| `belgian_pro_league_standardization_assessment.json` | 297789 | `6cf5479fef71bdbe9952238856e818322e345c0c5f6cbb5c8ebb7145dcfb6c4a` |
| `belgian_pro_league_standardization_manifest.json` | 7676 | `26c654acf1d042ff1637878612a416a0dbd5e9c4a447d5ca1fea5a2e46d9400c` |

Manifest hashes the CSV/archive/assessment, implementation, frozen Phase6 registry and source receipts; it records prior file hashes and importer results. Audit preserves all original provenance; assessment includes the36-season/stage matrix, normalization table, special-case checks and rematch enumeration. `phase7_protected_before.json` freezes144 pre-Phase7 files; `phase7_final_verification.json` records final checks. No source data is in public documentation or Git.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. python -B -m scripts.standardize_belgian_pro_league_results
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. python -B -m scripts.standardize_belgian_pro_league_results --verify
```

The default generator writes only new/identical Phase7 artifacts and refuses differing saved files. Verification uses a separate process and clean temporary directory, compares allfour artifacts byte-for-byte and by SHA-256, and rechecks preservation. Prior Phase6 objects are independently recomputed and compared without rewriting them. Temporary importer bridge files live outside the synchronized project and are removed. No source acquisition occurs.

## Fresh tests, limitations and preservation

Final totals and preservation results are recorded after execution below. An initial focused run found one missing rejection of a noncanonical synthetic season string (39passed/1failed). The guard was fixed; all approved actual seasons were already canonical, so this changed no CSV match facts. The corrected focused run passed all40tests. The collision check also distinguishes a previous same-schema SerieB audit from screened datasets; no prior files were modified.

Limitations remain: no dated early-season1990/91–1994/95 recovery; incomplete2025/26 with only121approved scored events; omitted/annulled historical populations; no universal independent historical certification; unresolved legal continuity and administrative-finality evidence; source copying/attribution, redistribution and model-training restrictions. Historical acceptance and technical standardization do not grant legal clearance or authorize training/application integration.

## Phase8 agenda — not performed here

1. Independently inspect all Belgian acquisition/validation/review/policy/recovery/standardization code and tests rather than relying on this report.
2. Reparse pinned originals, reconstruct10,434representations/8,724events and verify the exact8,592-row approved subset; preserve30documentary entries outside that union.
3. Independently assess the628 source/season name bindings, legal-identity limits and60changed output rows; verify no global alias or within-season club collapse.
4. Check shared schema/ID derivation,222legitimate rematch pairs, dates, accepted administrative scores, explicit exclusions and all36season/stage counts.
5. Regenerate allfour Phase7 artifacts in clean temporary storage and compare hashes/bytes; verify prior fingerprints, private-data exclusion and no application/environment changes.
6. Rerun focused/full regressions and inspect public commit scope, rights disclosures and remaining coverage gaps. No publication or training clearance follows from Phase8 technical checks.

**Stop after Phase7. No Phase8 final review, Phase9 commit/push, application integration, acquisition or model training.**

## Executed verification and repository state

- Final focused tests: **40passed**; all Belgian: **364passed**; acquisition/importer: **503passed**; additional source/general/SerieA validation regressions: **150passed**; app/launcher: **7passed**; full repository: **2,525passed**. Selections overlap. All final runs: zero failed, errored or skipped tests. The earlier synthetic-season failure and its correction are recorded above.
- All **four** final artifacts independently regenerated byte-for-byte and SHA-256-identically in a separate process/temp directory. The CSV hash remained unchanged throughout the validation-guard hardening.
- All **144** frozen pre-Phase7 files and nested Phase2–6/early-recovery baselines match. All ten Belgian originals, earlier public scripts/docs/tests, original planning-log prefix,1,415prior private/250prior public fingerprints and6,200original runtime-package hashes remain unchanged.
- Twelve earlier historical screened outputs remain byte-identical with **137,189records**, plus the separate **258ongoing English records**. The compatible prior SerieB audit was included only in ID collision checks, not in screened counts.
- Private CSV/archive/assessments/manifests remain Git-ignored; no private files tracked or staged. Original `.venv`, application and promotional worktree untouched. Existing external offline environment reused; no installations or dependency downloads.
- HEAD `013bb9c195624d5ac290aeb57dae11c4e21c0b5a` and index hash unchanged. No staging, commit, push, merge or rebase. Existing uncommitted work and two `.DS_Store` files preserved.

New public files: `scripts/standardize_belgian_pro_league_results.py`, `tests/test_belgian_pro_league_standardization.py`, this report; append-only `PLANNING_LOG.md`. Private additions: the four named outputs, `phase7_protected_before.json`, `phase7_final_verification.json`. No previous competition, application file or frozen Belgian adjudication was changed.
