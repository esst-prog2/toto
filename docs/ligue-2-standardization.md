# Ligue 2 — Phase 7 screened standardization

Date: 2026-11-22. Scope: acquired 2014/15–2024/25 regular-season observations only. User-approved Phase 6 decisions are applied without new historical decisions or source corrections. Phase 8 has not been performed.

## Reconciliation

| Processing disposition | Observations |
|---|---:|
| Full audit archive | 4,106 |
| Included in screened CSV | 4,003 |
| Administrative HOLD OUT | 3 |
| NOT PLAYED | 100 |
| Other HOLD OUT / definitive exclusion | 0 |

Fresh structural parsing of all eleven pinned originals reproduces frozen Phase 4 artifacts. The entire Phase 6 policy regenerates identically and every observation must match exactly one bound decision before projection. Complete audit IDs, source locations and directed pairings are unique. No observation was lost or duplicated. The CSV is exactly the approved archive subset, independently rechecked against source values and saved decisions.

| Season | Archived | Screened | Administrative HOLD OUT | NOT PLAYED |
|---|---:|---:|---:|---:|
| 2014/2015 | 380 | 380 | 0 | 0 |
| 2015/2016 | 380 | 380 | 0 | 0 |
| 2016/2017 | 380 | 380 | 0 | 0 |
| 2017/2018 | 380 | 380 | 0 | 0 |
| 2018/2019 | 380 | 380 | 0 | 0 |
| 2019/2020 | 380 | 280 | 0 | 100 |
| 2020/2021 | 380 | 379 | 1 | 0 |
| 2021/2022 | 380 | 379 | 1 | 0 |
| 2022/2023 | 380 | 379 | 1 | 0 |
| 2023/2024 | 380 | 380 | 0 | 0 |
| 2024/2025 | 306 | 306 | 0 | 0 |

## Output paths and schema

All four principal output types are private under `data/private/france/ligue_2/`:

- `ligue_2_standardized_2014_2025.csv`
- `ligue_2_audit_archive_2014_2025.json`
- `ligue_2_exceptions_2014_2025.json`
- `ligue_2_standardization_manifest.json`

```text
match_id,date,league,season,home_team,away_team,home_goals,away_goals
```

Canonical league is `Ligue 2`; seasons use `YYYY/YYYY`. The shared historical importer validates the bridge, numeric goals, outcome labels, dates, home/away identities and exact fact preservation. IDs use the established SHA-256 of compact UTF-8 JSON `[league, season, date, home_team, away_team]`, not the provisional Phase 6 candidate fingerprint. Rows are sorted by league, season, date, home and away; reversed input reproduces identical CSV bytes. No aliases, accents or original labels are changed. AC Ajaccio and Gazélec remain separate, with QRM/Annecy uncertainties retained.

All 4,003 IDs are unique and collision-free against the protected earlier CSV inventory. The manifest lists all earlier files checked and 113248 unique IDs, including earlier ongoing partitions and a schema-compatible Serie B audit CSV; this broader collision-check set is not a count of screened completed historical matches. All nine prior competitions are represented.

The manifest records source URLs, pinned revision, Git blob identities, SHA-256s, schema, per-season counts, shared-import summary, code/input hashes, prior-file fingerprints, numeric outcomes and output hashes. Each archived record preserves the full structural observation, literal source line, original and standardized values separately, bound Phase 6 decision, chronological fields, evidence references and transformations. The archive also retains the 376-entry historical registry, 23 round contexts, 31 reversal pairs and identity review.

## Approved historical policies applied

| Case | Implementation |
|---|---|
| Niort–Valenciennes, 2020-12-22, 0–3 [awarded] | Administrative HOLD OUT; original values and indexed January 2021 lead retained; no invented finality or availability |
| Bordeaux–Rodez, 2023-06-02, 0–1 | Administrative HOLD OUT; 2023-06-12 disciplinary publication stored separately; no guessed numerical award |
| Nancy–QRM, 2022-04-22, 0–3 | Administrative HOLD OUT; 2022-05-04 penalty publication separate from unresolved homologation, finality and availability |
| AC Ajaccio–Bastia, 2024/25 | Exactly one included 0–0; October 26 interrupted kickoff and December 3 completion retained; source already says December 3, so no fictitious date correction |
| Valenciennes–Béziers, 2019-04-19 | Included unchanged 5–6 with contemporary corroboration reference |
| 2019/20 cancellations | All 380 slots archived; 280 scored results screened; 100 explicit cancelled null-score observations NOT PLAYED |

All administrative HOLD OUTs and cancelled fixtures have null screened projections and IDs in the archive. Unknown or contradictory historical decisions fail explicitly before output generation. Wide rounds, outliers, source-order reversals and lack of bounded historical certification do not themselves cause exclusion. Their overlapping flags and uncertainties are preserved without silent date correction.

## Chronology and consumer limitations

Candidate screening remains separate from availability for prediction or training. The CSV date is an ordinary source-day proxy except for the specifically approved completion interpretation. It is not an independently verified availability timestamp. Audit metadata distinguish source heading/date, scheduled date, actual kickoff/completion, administrative publication/finality and effective availability. Unknown values stay null.

Future consumers must use the bound `decide_ligue2_policy.eligible_for_prediction` guard: it rejects unknown required availability, same-day use, future completion, unresolved administrative outcomes and altered decision bindings. The Ajaccio completion is unavailable before or on 2024-12-03 under the day-level ordering rule; earliest permitted prediction day is December 4. `training_allowed` additionally requires suitability and permission clearance, which have not been granted. The CSV alone is not a guarantee against future-information leakage. No application integration, evaluation or training occurred.

## Reproduction and checks

Use the existing working dependency environment with `PYTHONPATH=src:.` and bytecode disabled:

```sh
python -B scripts/standardize_ligue2_results.py --init
python -B scripts/standardize_ligue2_results.py --write
python -B scripts/standardize_ligue2_results.py --check
python -B scripts/standardize_ligue2_results.py --write --output-directory /tmp/your-new-review-directory
```

Existing differing outputs are refused rather than overwritten. Temporary importer bridges are removed after conversion. Original acquisitions and all Phase 2–6 artifacts are frozen by the 144-entry Phase 7 baseline; earlier planning-log bytes are separately hashed so only append-only updates are permitted. Nested baselines preserve 676 earlier private and 185 public files. No previous environment was modified or dependencies installed.

Fresh bounded runs used the preserved external Python 3.13.12 environment, with no installs, original .venv modifications or dependency upgrades:

| Scope | Passed | Failed / unverified |
|---|---:|---:|
| New standardization tests | 37 | 0 |
| All Ligue 2 tests | 260 | 0 |
| Non-UI regression suite | 1,552 | 0 |
| App/launcher tests | 7 | 0 |
| Full repository suite | 1,559 | 0 |

These overlapping runs are not additive. Logs, JUnit XML and exit statuses are preserved in private `verification_phase7/`.

An independent subprocess regenerated all four principal outputs in external temporary storage. Every output matched saved bytes and SHA-256. A separate saved-output reconciliation independently reconstructed CSV rows and IDs from original values and saved decisions, checked all eleven original SHA/blob identities and physical line bindings, and established exactly 4,106 archived / 4,003 screened / three administrative HOLD OUT / 100 NOT PLAYED. Numeric-goal outcomes are 1,700 home wins, 1,161 draws and 1,142 away wins; these are descriptive source outcomes, not prediction results.

| Output | Bytes | SHA-256 |
|---|---:|---|
| `ligue_2_audit_archive_2014_2025.json` | 30,985,692 | `9bb00bca994a6ff377d956187094647d50b5e3b9d7a749b6c9d1442a0cb3ede1` |
| `ligue_2_exceptions_2014_2025.json` | 1,212,144 | `c7f73b6e86b631ac8f194f0d399df653b68e6563957206f0a04ade309b4e463e` |
| `ligue_2_standardization_manifest.json` | 13,393 | `0b432c40f486b0fe72a2c42a16ac9af202495a0c586a9768c7a7c28ad220fbd0` |
| `ligue_2_standardized_2014_2025.csv` | 497,155 | `c372a0558f5c5325c4b066a5303930ff7a8b41cbcd1b411e0913942eca9147a4` |
 An initial synthetic archive fixture lacked a URL field; its test fixture was completed and fresh final runs were performed. No source-data defect was involved.

## Remaining scope and rights limitations

The 24 missing seasons 1990/91–2013/14, unresolved RSSSF 1998/99 date/orientation/identity issues and incomplete pinned 2025/26 source (306 slots, 116 scored, 190 unscored) remain outside this population. No additional datasets or supplementary records were acquired. Three administrative cases remain held out. Bounded historical corroboration is not complete certification; source-day and administrative availability uncertainties remain.

Technical screening, historical confidence, chronological suitability, redistribution rights and model-training permissions remain distinct. OpenFootball CC0 does not establish every upstream right. Redistribution and model-training clearance remain unresolved; training is not authorized.

## Files and review gate

Public Phase 7 changes are `scripts/standardize_ligue2_results.py`, `tests/test_ligue2_standardization.py`, this report and appended `PLANNING_LOG.md` lines. Private artifacts include the four principal outputs, baseline and verification receipts/logs. They remain Git-ignored. No application, promotional worktree, prior competition or immutable evidence was changed. No staging, commit, push or merge occurred.

The outputs are prepared for an independent Phase 8 review, subject to user approval. Phase 8 has not been started.
