# Primeira Liga — Phase 7 screened standardization

Date: 2026-11-23. Phase7 only, implementing the approved Phase6 decisions without changes. Branch `feature/data-collection`; protected HEAD `0bb6f393c89fdcc37a52a56bb31e458ff131de47`.

## Four private outputs

Dated coverage is **1994/95–2025/26**, exactly32 represented seasons. The full research objective remains1990/91–2025/26. All four outputs are local, Git-ignored and untracked:

- `data/private/portugal/primeira_liga/primeira_liga_standardized_1994_2026.csv`
- `data/private/portugal/primeira_liga/primeira_liga_audit_archive_1994_2026.json`
- `data/private/portugal/primeira_liga/primeira_liga_exceptions_1994_2026.json`
- `data/private/portugal/primeira_liga/primeira_liga_standardization_manifest.json`

| Output | Bytes | SHA-256 |
|---|---:|---|
| `primeira_liga_standardized_1994_2026.csv` | 1141601 | `4297ddb1b979326628d27b1609abd861c41017dcd5c4e44df357f0dceaf2c3e8` |
| `primeira_liga_audit_archive_1994_2026.json` | 103545318 | `4c2d243bd7607278cfbaa3a86b3a1c347d85f0b6b29cfdeb0e7e473fdc61990a` |
| `primeira_liga_exceptions_1994_2026.json` | 1521955 | `ce913f819ac45d5e81385e85b7eb944b917187d4301e34a15f59b5f5ef94ac09` |
| `primeira_liga_standardization_manifest.json` | 17427 | `ec8fb176a74061f3e19eba9de5c8aa125cc43a427246c00608fe44a12985e4f7` |

The first three hashes are bound in the fourth manifest. Its own hash is independently recorded in `phase7_independent_regeneration.json` and the final verification receipt rather than circularly self-hashed.

## Source and fixture reconciliation

| Population | Total | Completed-result candidate | HOLD OUT | NOT PLAYED | Other exclusions |
|---|---:|---:|---:|---:|---:|
| Original dated source observations | 11,406 | 11,403 | 3 | 0 | 0 |
| Unique sourced fixtures | 9,264 | 9,262 | 2 | 0 | 0 |

8,958 historical observations + 2,448 modern observations =11,406 originals. The complete archive retains9,264 selected and2,142 nonselected comparator representations, every original exactly once in observation accounting. All2,142 overlap relationships remain traceable and produce one CSV row per approved candidate, never a second fixture. The independent verifier matched every archive original to frozen Phase4/6 records, every fixture to exactly one Phase6 decision, and every CSV row to one approved candidate.

The shared importer accepted9,262 of9,262 rows, with zero rejected records, duplicates, fixture-only records or conflicts. Goal-derived outcomes are4,291 home wins,2,364 draws and2,607 away wins. These are descriptive counts, not prediction accuracy or historical-certification claims.

| Season | Unique sourced slots | Screened rows | HOLD OUT | NOT PLAYED |
|---|---:|---:|---:|---:|
| 1994/1995 | 306 | 306 | 0 | 0 |
| 1995/1996 | 306 | 305 | 1 | 0 |
| 1996/1997 | 306 | 306 | 0 | 0 |
| 1997/1998 | 306 | 306 | 0 | 0 |
| 1998/1999 | 306 | 306 | 0 | 0 |
| 1999/2000 | 306 | 306 | 0 | 0 |
| 2000/2001 | 306 | 306 | 0 | 0 |
| 2001/2002 | 306 | 306 | 0 | 0 |
| 2002/2003 | 306 | 306 | 0 | 0 |
| 2003/2004 | 306 | 306 | 0 | 0 |
| 2004/2005 | 306 | 306 | 0 | 0 |
| 2005/2006 | 306 | 306 | 0 | 0 |
| 2006/2007 | 240 | 240 | 0 | 0 |
| 2007/2008 | 240 | 240 | 0 | 0 |
| 2008/2009 | 240 | 240 | 0 | 0 |
| 2009/2010 | 240 | 240 | 0 | 0 |
| 2010/2011 | 240 | 240 | 0 | 0 |
| 2011/2012 | 240 | 240 | 0 | 0 |
| 2012/2013 | 240 | 240 | 0 | 0 |
| 2013/2014 | 240 | 240 | 0 | 0 |
| 2014/2015 | 306 | 306 | 0 | 0 |
| 2015/2016 | 306 | 306 | 0 | 0 |
| 2016/2017 | 306 | 306 | 0 | 0 |
| 2017/2018 | 306 | 306 | 0 | 0 |
| 2018/2019 | 306 | 306 | 0 | 0 |
| 2019/2020 | 306 | 306 | 0 | 0 |
| 2020/2021 | 306 | 306 | 0 | 0 |
| 2021/2022 | 306 | 305 | 1 | 0 |
| 2022/2023 | 306 | 306 | 0 | 0 |
| 2023/2024 | 306 | 306 | 0 | 0 |
| 2024/2025 | 306 | 306 | 0 | 0 |
| 2025/2026 | 306 | 306 | 0 | 0 |

## Unchanged source hierarchy

Historical primary: `jalapic/engsoccerdata/data-raw/portugal.csv`, revision `872c5c354161ace8408f3091b758c6af4cccca94`, for1994/95–2024/25. Modern primary: `openfootball/europe/portugal/2025-26_pt1.txt`, revision `63df627f3c87ce71708f016522ea236cf74332c3`, for2025/26. Seven overlapping modern seasons remain comparator-only. Each source’s exact URL, SHA-256, Git blob/revision, physical lines and provenance receipt are preserved.

This phase selects no new sources, approves no new aliases and changes no historical policy. The Phase6 policies and measured complete season inventories remain the basis for the hierarchy, without claiming independent upstream origins or superior universal historical truth.

## Exact approved interpretations and HOLD OUTs

| Fixture | Screened interpretation | Original/audit preservation and restriction |
|---|---|---|
| Santa Clara–Paços2019/20 | One row, **2020-02-02**, 2–1 | Historical line7290 remains Feb1; modern line298 remains Feb2. Protest/finality guard remains active: screened inclusion does not grant chronological eligibility. |
| Santa Clara–Benfica2020/21 | One row, **2021-01-04**, 1–1 | Historical line7532 retains Jan3; modern line192 retains Jan4. Jan3 kickoff/interruption and Jan4 completion remain separate; no invented publication timestamp. |
| Belenenses SAD–Benfica2021/22 | **HOLD OUT; absent from CSV** | Both originals0–7, Nov27, lines7838/187, remain in archive. Administrative finality/availability insufficiently established. Played but terminated abnormally, not NOT PLAYED. |
| Benfica–Salgueiros1995/96 | **HOLD OUT; absent from CSV** | Original Aug20 source line308 remains; Sept6 research lead and its limitations remain. Neither date is adopted as authoritative; no completion/publication timestamp fabricated. |
| Feirense–Nacional2011/12 | One row, Aug14,0–0; `Feirense` home label | Only approved line4877/audit ID receives the future representation; original `Feirense ` remains unchanged in physical CSV, source record and archive. No global trim or synthetic missing matches. |
| Nacional–Benfica2024/25 | One row, **2024-12-19**,0–2 | Both originals already contain Dec19 (historical line8779, modern line230). Oct6 interruption context retained; no fictitious source correction. |
| Leiria–Feirense2011/12 | One row, Apr29,0–4 | Eight-player participation context preserved; no award or substitute score. Ordinary availability restrictions remain. |

Independent selected-source comparison found **exactly three changed fields across three records**: the two Santa Clara date interpretations and the single Feirense home-label interpretation. No selected score, away label or other date/label changed. Nacional’s completion date was already present in both sources.

Stable Phase6 decision references are preserved without regeneration under a new policy:

- NACIONAL_BENFICA: `PT-P6-NACIONAL_BENFICA-96148395ec97843379452bf5db49e553984816555b317fa57baafde0b4cb67c8`; fixture `96148395ec97843379452bf5db49e553984816555b317fa57baafde0b4cb67c8`.
- SANTA_BENFICA: `PT-P6-SANTA_BENFICA-52c7368dffa4b73d69c041310be3ec2cda42ff10994e0b48d98b9182c2d99f7c`; fixture `52c7368dffa4b73d69c041310be3ec2cda42ff10994e0b48d98b9182c2d99f7c`.
- LEIRIA_FEIRENSE: `PT-P6-LEIRIA_FEIRENSE-ad0f1d83cff70c1fdf03539626df3ce45ad342b43349e0711c12e1d95ce02e24`; fixture `ad0f1d83cff70c1fdf03539626df3ce45ad342b43349e0711c12e1d95ce02e24`.
- BENFICA_SALGUEIROS: `PT-P6-BENFICA_SALGUEIROS-506ea92837a3c91f4e50a239830c95fc5dcad5d05273b7935ecca85e622e6471`; fixture `506ea92837a3c91f4e50a239830c95fc5dcad5d05273b7935ecca85e622e6471`.
- BELENENSES_BENFICA: `PT-P6-BELENENSES_BENFICA-590de1a604f7ce5ee00f775655831b47f65771ab296be77ca2feb0e7ebb93d82`; fixture `590de1a604f7ce5ee00f775655831b47f65771ab296be77ca2feb0e7ebb93d82`.
- SANTA_PACOS: `PT-P6-SANTA_PACOS-2670b3156d51618e955ca4f59a949eaf68ddfb3d8748f869f6a08ecbc8642e65`; fixture `2670b3156d51618e955ca4f59a949eaf68ddfb3d8748f869f6a08ecbc8642e65`.
- FEIRENSE_NACIONAL: `PT-P6-FEIRENSE_NACIONAL-6be498676b5c4719b6b9629afd6d8be9ec31c5408d8d1f0b0b283c818d5a50b5`; fixture `6be498676b5c4719b6b9629afd6d8be9ec31c5408d8d1f0b0b283c818d5a50b5`.

A HOLD OUT may still have a selected provenance source. That selection does not approve its raw date or score for the CSV: its standardized projection and screened match ID remain null. Both HOLD OUT fixtures (three original observations) are retained in the archive and exception report. There are no additional exclusions and zero NOT PLAYED fixtures.

Portugal2019/20 retains all306 approved scored fixtures. The suspension, restart and extended July calendar are preserved in frozen context; no Dutch cancellation rule or new unplayed slot is imported. All26 unusual-score original memberships (18 conditional events) remain represented without new score corrections or magnitude-based exclusions.

## Schema, serialization and ID integrity

Exact schema and ordering:

```text
match_id,date,league,season,home_team,away_team,home_goals,away_goals
```

`league` is `Primeira Liga`; seasons use the established consecutive `YYYY/YYYY` convention; dates are ISO calendar days; goals are canonical nonnegative integers. The existing shared historical importer, bridge and public historical-data loader are reused unchanged. Serialization uses the existing UTF-8 CSV writer and stable `(league,season,date,home_team,away_team)` ordering. Reversing input order produces identical bytes, and a parse/serialize round trip is byte-identical.

Each match ID is the established SHA-256 of compact UTF-8 JSON `[league,season,ISO date,home team,away team]`, `ensure_ascii=False`, separators comma/colon; goals are excluded. Every one of the9,262 IDs was independently recalculated from the serialized CSV using a separate implementation. IDs and directed season fixtures are unique, with no overlap duplicates. All records conform to the approved first-division regular-season scope; no unsourced years, other divisions, cups, playoffs or reserve competitions were added. Literal club labels are preserved except the exact Feirense decision.

### Protected collision population

The protected CSV convention covers **14 eight-column CSV files**, **140,487 row instances** and **128,190 distinct IDs** across eleven prior competitions. It includes the two ongoing English partitions and the SerieB audit CSV, so the correct population is larger than the127,927 screened historical rows.

The check additionally reserves explicit `match_id`, `screened_match_id`, `source_observation_match_id` and `candidate_match_id` fields from **five protected JSON audit archives**. Those archives contain51,477 distinct identifiers, with **4,107 not already in the CSV inventory**. The full union checked is therefore **132,297 distinct protected identifiers**, with **zero collisions** against all9,262 new IDs. Some older candidate identifiers use a different algorithm from the final shared-import CSV IDs; they are still conservatively reserved. Generic audit, fixture and decision hashes are not conflated with match-ID fields. The manifest records file hashes, per-field occurrences and file-level counts.

An initial verification-helper estimate assumed greater overlap between candidate and final CSV IDs. Comparing the actual sets corrected that estimate without changing any output, source policy, dataset row or disposition. The independent checker agrees with the saved manifest’s measured union; totals are not forced to a screened-only count.

## Complete audit archive structure

- `records`: exactly11,406 original dated source observations, sorted by stable audit ID. Each retains the complete original representation, physical literal, source SHA/blob/URL, competition context and receipt reference; selected/comparator role; fixture and exact Phase6 decision IDs; disposition; approved projection or null; evidence and historical confidence; chronological and administrative restrictions; documented transformations and `training_authorized=false`.
- `unique_fixtures`: exactly9,264 fixture entries, each with the unchanged approved Phase6 decision, original source bindings, approved standardized projection or null, and screened match ID or null.
- `source_context`: receipt metadata for all nine dated files and modern source notes; immutable originals remain separately preserved.
- `rsssf_result_only_snapshot`: the tenth original’s provenance/licensing receipt and380 undated result identities, explicitly outside the dated population. No fixture dates or source-observation IDs are invented.
- `source_correspondences`: all2,142 exact season-bound comparator links.
- `scheduling_and_identity`, `historical_review_registry`, `evidence_inventory`, `coverage_gap`: frozen exception decisions, all18 wide-round contexts/162 memberships,13 reversal pairs/26 endpoints,207 flagged observations,392 reviewed observations/228 conditional groups, documentary inspection classifications and remaining uncertainty.

The exception report retains all seven exact special-case decisions, both HOLD OUTs and their original records, all approved source correspondences, the historical-confidence summary and original evidence limitations. The archive is **not** training data. Selected historical labels do not approve a global legal identity across Belenenses/its SAD, AVS/Aves, Vitória SC/FC or predecessor/successor entities. Senior/B-team distinctions and all source literals remain intact.

## Strict chronology and permissions

The unchanged Phase6 `PredictionGate` verifies sources, evidence and all seven policy files before accepting a supplied decision. Same-day/future results, unknown required completion/availability, HOLD OUTs, unresolved administration, unapproved supplemental data and altered policy/source bindings reject. The CSV does not replace this gate.

The real registry check still finds only Santa Clara–Benfica and Nacional–Benfica chronologically eligible after their supported completion days. Santa Clara–Paços is still blocked by its protest/finality guard. Ordinary source-date proxies are not promoted to verified availability timestamps; source date, kickoff, interruption, completion, decision/publication and finality remain separate. No intraday timestamp is invented. All model-training/evaluation and redistribution clearances remain unresolved; every training-authorization check returns false, including for the two chronologically supported cases. No model is trained or evaluated with Portuguese records.

## Independent reproduction and fresh tests

All four saved outputs were regenerated by a separate Python process into safe temporary storage and matched byte-for-byte and by SHA-256. The independent checker also read the CSV separately, recalculated every ID, reconciled every archived original and fixture, verified the exact candidate subset and all source roles, checked both HOLD OUTs and all approved transformations, and independently rebuilt the protected ID union. All seven frozen Phase6 policy artifacts separately regenerated byte-identically. Saved artifacts were never overwritten.

Example using the established external verification environment:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. "$VERIFICATION_PYTHON" -B scripts/standardize_primeira_liga_results.py --write --output-directory "$TEMP_STANDARD_DIR"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. "$VERIFICATION_PYTHON" -B scripts/standardize_primeira_liga_results.py --check
```

Use safe temporary storage for regeneration and the existing external Python3.13.12 environment. No installation, network acquisition or original `.venv` execution is needed. Private immutable sources/evidence are required; they are intentionally not distributed with public code.

| Test selection (overlapping; do not sum) | Passed | Failed | Errors | Skipped |
|---|---:|---:|---:|---:|
| acquisition_importer | 776 | 0 | 0 | 0 |
| app_launcher | 7 | 0 | 0 | 0 |
| focused | 315 | 0 | 0 | 0 |
| full | 2161 | 0 | 0 | 0 |
| non_ui | 2154 | 0 | 0 | 0 |
| standardization | 69 | 0 | 0 | 0 |

The complete repository suite passed **2,161 tests**, versus the2,092 baseline. There are69 new focused standardization tests covering shared serialization/IDs, all seven overlap years, season-specific participants/pairings, all seven special cases, source provenance/archival accounting, excluded scope, policy tampering, collision rejection including reserved JSON identifiers, and chronology restrictions.

## Preservation and remaining limits

Protected fingerprints confirm all eleven prior competitions and their127,927 screened records unchanged, alongside1,037 earlier private files,228 public files and355 frozen Phase2–6 entries. All ten Portuguese originals, existing evidence/receipts/policies and planning-log prefix remain unchanged. The application and promotional worktree were not edited. The original `.venv` was not invoked, installed into or rebuilt; no complete historical bytewise environment baseline existed, so no stronger environment-forensics claim is made.

All private source/audit/verification artifacts remain ignored and untracked. Public code/report checks found no credentials or private dataset bundles. HEAD and index remain unchanged; no staging, commit, push, merge, rebase, deployment or Phase8 review occurred. The known `.DS_Store` files remain outside Git.

The 36-season objective is not complete:1990/91 has380 unsourced expected slots and1991/92–1993/94 each306, totaling **1,298**. Those are research/acquisition gaps, not source-derived HOLD OUT or NOT PLAYED records. Closing the gap requires separately approved source discovery, permissions and acquisition; no new data were acquired here.

Screened inclusion is not independent historical certification, administrative finality, safe result availability, legal identity resolution or model-training permission. The engsoccerdata noncommercial/attribution notice and software licensing, OpenFootball’s rights-held CC0 and publishers’ documentary conditions remain distinct. No redistribution, commercial-use or model-training clearance is inferred from accessibility, official hosting or successful conversion.

## Files changed and stopping point

New public files: `scripts/standardize_primeira_liga_results.py`, `tests/test_primeira_liga_standardization.py`, this report. Modified public file: append-only `PLANNING_LOG.md`. Shared importer/serializer/application code and all previous Portuguese code/reports are unchanged.

New private files: `phase7_protected_before.json`, the four listed standardization outputs, `phase7_independent_regeneration.json`, `phase7_test_summary.json`, `phase7_final_verification.json`, and bounded logs/XML/status receipts under `verification_phase7/`. The final verification receipt lists exact private paths/checksums.

The implementation and measured outputs are ready for a **separately approved Phase8 independent review**. No Phase8 work has begun. Stop after Phase7 pending explicit user approval.
