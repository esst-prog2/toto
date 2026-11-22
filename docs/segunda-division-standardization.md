# Segunda División — Phase 7 screened standardization

Completed 2026-11-22 in the original `toto` worktree on `feature/data-collection`, unchanged HEAD `052d25185182f1edbb80fac51cafbb59e0acf7cf`. User approved Phase 6 including the conservative Deportivo–Fuenlabrada hold and authorized Phase 7 only. Earlier sources, policies, reports and competition outputs remain immutable. No acquisition, application integration, training, staging, commit, push or merge.

## Measured reconciliation

| Classification | Observations |
| --- | --- |
| Original fixture observations | 6006 |
| Complete audit-archive observations | 6006 |
| Screened standardized rows | 5984 |
| Unresolved Reus administrative HOLD OUT | 21 |
| Approved conservative Deportivo–Fuenlabrada HOLD OUT | 1 |
| Total HOLD OUT | 22 |
| Definitively excluded | 0 |
| Evidence-backed supplements within screened rows | 9 |
| Original blank scores still preserved | 9 |

Measured identity: **5,975 unchanged original score-bearing inclusions + nine approved supplements + 21 Reus holds + one Deportivo hold = 6,006**. Screened output is exactly the approved 5,984-row subset of the full archive. No duplicate, silently lost or unapproved included observation was found. The code derives counts from source-bound policy decisions; it does not fill records or force totals to the expectation.

| Season | Archived | Screened | Held out | Supplements |
| --- | --- | --- | --- | --- |
| 2012/2013 | 462 | 462 | 0 | 0 |
| 2013/2014 | 462 | 462 | 0 | 0 |
| 2014/2015 | 462 | 462 | 0 | 0 |
| 2015/2016 | 462 | 462 | 0 | 0 |
| 2016/2017 | 462 | 462 | 0 | 0 |
| 2017/2018 | 462 | 462 | 0 | 0 |
| 2018/2019 | 462 | 441 | 21 | 0 |
| 2019/2020 | 462 | 461 | 1 | 0 |
| 2020/2021 | 462 | 462 | 0 | 0 |
| 2021/2022 | 462 | 462 | 0 | 0 |
| 2022/2023 | 462 | 462 | 0 | 0 |
| 2023/2024 | 462 | 462 | 0 | 0 |
| 2024/2025 | 462 | 462 | 0 | 9 |

Each acquired regular season has 462 original directed-fixture observations. Expected full pairings apply to the original population, not to the intentionally screened subset. Screened goal-derived outcomes: **2,703 home wins, 1,804 draws, 1,477 away wins**. These are counts of retained results, not prediction performance or historical-certification claims.

## Private outputs and integrity

All paths below are relative to ignored `data/private/spain/segunda_division/`. The filename range `2012_2024` identifies starting season years and therefore includes **2012/13 through 2024/25**. It does not end at calendar 2024 or include 2025/26.

| File | Bytes | SHA-256 |
| --- | --- | --- |
| segunda_division_standardized_2012_2024.csv | 800569 | 424f5bf3e878ea794a653504076f2ba386c27a562f9cb7ce0abe8fbd4b6b59c0 |
| segunda_division_audit_archive_2012_2024.json | 29572114 | 096b240fce682cad8c4d63c28f51220bc3601565d9f3603be622eeb0838ca228 |
| segunda_division_exceptions_2012_2024.json | 572559 | baf76708d600c6f1d5da42df76a90bd3cce155d356d60dc36b1570b5a7395758 |
| segunda_division_standardization_manifest.json | 27332 | 165863e673724e3bac46db334ba34739d5130d9308552934951137a738923636 |

The CSV is UTF-8 with deterministic LF serialization and this exact column order:

```text
match_id,date,league,season,home_team,away_team,home_goals,away_goals
```

Canonical league: **`Segunda División`**, distinct from La Liga. Seasons use `YYYY/YYYY`. Rows follow the existing shared importer’s ascending `(league, season, date, home_team, away_team)` ordering. IDs use its SHA-256 of compact UTF-8 JSON `[league, season, date, home_team, away_team]` with Unicode preserved. Scores do not form part of identity. All 5,984 IDs are unique; schema, calendar dates, season windows, numeric nonnegative goals and outcomes were checked. No team-label normalization was silently accepted: imported facts must equal the approved projections exactly.

## Approved supplements and exceptions

The frozen Phase 6 registry is used unchanged; its SHA-256 is `c5140f5113ca4ea4bc605569807c4495e04c1e9e5509fe88d8f2179aa69a5220`. The registry historically calls the Deportivo hold proposed/pending. A separate immutable `phase7_approval.json` records the user’s approval of that hold, bound to the registry hash and exact held fixture ID. The old registry and its original approval labels were not rewritten. Current archive disposition explicitly says HOLD OUT and records `USER_APPROVED_PHASE7`.

| Decision | 2024/25 source line | Fixture | Original FT | Screened supplement | Effective date |
| --- | --- | --- | --- | --- | --- |
| SD6-26 | 745 | Málaga CF — Burgos CF | blank | 2-2 | 2025-05-31 |
| SD6-27 | 747 | SD Huesca — CD Eldense | blank | 3-2 | 2025-06-01 |
| SD6-28 | 748 | UD Almería — CD Tenerife | blank | 2-0 | 2025-06-01 |
| SD6-29 | 749 | FC Cartagena — CD Mirandés | blank | 1-3 | 2025-06-01 |
| SD6-30 | 750 | Deportivo La Coruña — Elche CF | blank | 0-4 | 2025-06-01 |
| SD6-31 | 751 | Real Oviedo — Cádiz CF | blank | 2-1 | 2025-06-01 |
| SD6-32 | 752 | Levante UD — SD Eibar | blank | 1-0 | 2025-06-01 |
| SD6-33 | 753 | Racing Santander — Granada CF | blank | 2-1 | 2025-06-01 |
| SD6-34 | 754 | Córdoba CF — Albacete | blank | 1-1 | 2025-06-01 |

Every supplement requires its immutable source path/commit/SHA-256/physical line/audit ID, exact original fixture/date and approved independent claim/document bindings. The archive retains original `FT`, `hg` and `ag` as null and the unmodified literal scoreless line. Supplemented numeric goals appear separately in `approved_transformed_values`; the independently supported result remains separately identified. No original file or score string was edited. Missing, contradictory or rebound decisions fail closed.

All **21 source-marked Reus awards** are absent from the CSV. Their 2018/19 source dates, 1–0/0–1 strings, goal fields, `[awarded]` annotations, raw lines and provenance remain in the archive. They receive no effective availability day or screened projection. These are unresolved holds, not permanent historical deletions or ordinary played outcomes. The sidecar retains each of the 21 full source-bound decisions; see the [Phase 6 policy table](segunda-division-policy.md).

**Deportivo–Fuenlabrada, 2020-08-07, 2–1** is absent from the CSV and preserved in the archive under the approved conservative HOLD OUT. Its original July 20 scheduled date, intermediate August 5 plan, August 7 actual playing/completion date, verified played score and separate disciplinary/finality uncertainty remain visible. The hold has no effective availability day. It is not a claim that the played score is wrong.

**Rayo–Albacete:** the CSV uses **2020-06-10, 1–0**; the audit chronology retains the **2019-12-15** original kickoff/suspension and June 10 completion. The source already records June 10, so no original source date was corrected. **Osasuna–Mallorca 6–4 (2014-09-21)** and **Numancia–Lugo 6–6 (2014-12-20)** remain unchanged. No score cap, replacement or unapproved score/date change occurred.

## Full audit archive and sidecar

The archive retains **all 6,006 original observations**, each with full audit ID, original source path/physical line, source SHA-256, exact literal source line including its line ending and hash, pinned revision/Git blob, source URL and original parsed fields. Source-document receipts include attribution, retrieval metadata and licensing information. Literal line hashes were independently checked against the original bytes.

Every observation also has inclusion/HOLD OUT status, explicit reason where held, Phase 6 assessment, Phase 7 hold approval where applicable, decision ID, approved transformed values where included, screened ID or null, historical evidence claim if individually reviewed, scheduling/review categories, reserve identity groups and original/effective chronology. Holds never receive a disguised final eight-column projection; their source observations remain available for later evidence-based reconsideration.

The exception sidecar contains all **34 explicit cases**, their full audit links, the frozen uncertainty metadata, evidence-source registry, chronological rule and rights limitations. The manifest records all 13 source receipts/hashes/blob identities, exact schema, source/input/code fingerprints, season counts, outcomes, held audit IDs, uncertainty accounting and output sizes/SHA-256. The manifest’s own SHA-256 is captured separately in the verification receipt and table above.

## Chronology, identity and uncertainty safeguards

The dataset retains all **23 scheduling contexts** (11 documented, 12 partial), **253 affected observations**, **30 diagnostic outliers**, **17 source-order reversals**, **six reserve identity groups / 498 observations**, and all 79 individual review classifications (25 verified playing facts, 33 partial, 21 unresolved). Ordinary observations not individually reviewed are labeled accordingly; group context is not counted as individual certification. No scheduling flag alone causes exclusion or correction.

All original team labels are preserved. Athletic Club B/Bilbao Athletic, FC Barcelona B/Barça Atlètic, Castilla, Real Sociedad B/Sanse, Sevilla Atlético and Villarreal B remain distinct from their parents. Reviewed relationships are retained as metadata; **no global team mappings are applied**. CSV IDs include competition identity, allowing future cross-league work without silently merging reserves or renaming earlier datasets.

For explicit approved inclusions, effective date is the verified playing/completion calendar day. Ordinary source dates remain **uncertified source-playing-date proxies**, explicitly identified in the audit assessment/sidecar. They are not claimed to be independently established result-availability dates. Source/round storage order never substitutes for chronology. A result must be available **strictly before** the prediction calendar day; same-day and incomplete/unresolved outcomes fail closed under the Phase 6 policy guard.

The bare eight-column CSV cannot enforce downstream temporal or permission rules by itself. Future consumers must preserve the linked assessment/availability semantics and use the policy gates. Those gates reject ordinary uncertified availability proxies even if external clearance flags are changed, reject all holds and same-day outcomes, and require separate model-suitability and licensing clearance. **No training is currently cleared or performed, and no application consumer was changed.**

## Reproduction and verification

Public files added: `scripts/standardize_segunda_results.py`, `tests/test_segunda_standardization.py`, this document. `PLANNING_LOG.md` is appended only. Private Phase 7 additions: `phase7_protected_before.json`, `phase7_approval.json`, the four outputs above, and `phase7_verification.json`. Earlier scripts, tests, documentation, source originals and generated Phase 2–6 evidence remain unchanged.

The new baseline protects **75 prior entries** (58 private Segunda artifacts and 17 public Segunda files), plus an append-only planning-log prefix. Nested fingerprints also protect **493 private and 145 public artifacts** from all seven earlier completed competitions. Before export, Phase 6 and Phase 5 assessments are replayed and matched against saved bytes, including fresh pinned-source parsing. Source receipts, 13 SHA-256 values and 13 Git blob identities are verified; no source was downloaded.

The established shared historical importer generates IDs/validation at tier 2 with explicit Segunda mapping. Its temporary bridge files are created outside the source bundles and removed. Reversed input produces identical CSV bytes. An independent stdlib check then compares every archived original and literal line, the exact screened subset, schema/IDs/outcomes, nine approved score/date pairs, both hold categories, Rayo chronology and both unusual scores. Separate-process regeneration into **two safe temporary directories** produced **byte-identical copies of all four outputs**, with matching SHA-256 values.

Tests: **62 new synthetic standardization tests passed; 266 focused Segunda tests passed; all 1,075 repository tests passed**, including the **seven app/launcher tests**, with zero failures, errors or skips. The full suite completed in **12.74 seconds** using the existing isolated offline environment outside iCloud. The original `.venv` and project environment were unchanged; no dependency installation or upgrade.

Commands, using the tested environment with `PYTHONPATH=src:.`:

```sh
python -B -m scripts.standardize_segunda_results --check
python -B -m scripts.standardize_segunda_results --output-directory /tmp/EXISTING_EMPTY_DIR
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -B -m pytest tests/test_segunda_standardization.py -q -p no:cacheprovider
```

Default generation preflights all destinations and refuses to overwrite any existing artifact; `--check` regenerates in memory and compares saved bytes. Independent temporary outputs must use a fresh directory. Authorized local frozen private inputs are required; public code alone does not include original datasets or evidence bundles. The verification receipt stores test-log/JUnit hashes, exact code/output hashes, independent comparisons, fingerprints and Git privacy checks.

## Coverage, rights and stopping point

This output covers **only acquired 2012/13–2024/25 material**, not the complete historical Segunda database. Preserve the unresolved **22-season 1990/91–2011/12 acquisition gap**, pinned **2025/26 131 scored / 331 unscored** source limitation, original nine missing scores, and incomplete individual historical certification. All original blanks remain despite the nine approved supplements.

Technical screened acceptance, historical corroboration, administrative finality, training suitability and licensing clearance are separate. Existing OpenFootball/third-party provenance and RSSSF restrictions remain unchanged; independent official/news evidence is not permission to redistribute datasets or train models. All generated datasets/evidence remain ignored and untracked. No application or promotional worktree files were modified; nothing staged, committed, pushed or merged.

Stop after Phase 7 for user review. Independent final pipeline review and later carefully scoped commit/push remain separate phases requiring approval; no next competition is started.
