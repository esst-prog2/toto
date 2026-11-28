# UEFA Cup / UEFA Europa League — Phase 4: Standardization and independent validation

Date: 2026-11-28. Worktree: `toto-uefa`; branch: `feature/uefa`.

## A. Phase status

**CONDITIONAL PASS.** Actual standalone standardized artifacts have been generated and independently verified. The confirmed current consolidated schema is available and used. Technical row transfer, score/date integrity, local and current-global match uniqueness, reversibility, preservation and offline reproduction pass. Two project-wide conditions remain: the proposed `uefael` competition prefix is not yet registered, and the available name-derived team abbreviations do not constitute a globally unique club identity registry. Neither condition was hidden by inventing unique team codes or changing previous data.

Phase 3 was accepted by the owner. All 11,422 inclusions and 68 exclusions remain accounted for. One concrete date error was found and corrected in the Phase 4 derivative, with evidence and unchanged Phase 3 originals. No population, score, stage, disposition or neutral-format count changed. Phase 5 has not started.

## B. Standardized dataset and schema

Output, relative to this worktree:

`data/private/europe/europa_league/phase4/validated/uefa_europa_league_standardized_1990_2026.csv`

| Measure | Verified result |
|---|---:|
| Standardized rows | 11,422 |
| Seasons, 1990/91–2025/26 | 36 |
| Main competition | 6,506 |
| Qualifying | 4,916 |
| Preserved exclusions | 68 |
| Neutral-format matches | 38 |
| Estimated dates | 0 |
| Outcome-only records | 0 |
| Bytes | 1,114,212 |

SHA-256: `7d1a4084094368b2a8b17be84b87124ec65d53b0f4beb4184290ceb6e7d43fde`.

The confirmed ten-column consolidated schema, in exact order, is:

```csv
match_id,country,league,season,date,home_team,away_team,home_goals,away_goals,neutral_venue
```

Encoding is UTF-8 without BOM, LF line endings, normal CSV quoting, no index. Goals are nonnegative integer tokens. Dates are ISO YYYY-MM-DD, seasons consecutive YYYY/YYYY. `country=uefa`; league labels retain `UEFA Cup` through 2008/09 and `UEFA Europa League` thereafter. Qualifying and main stages share the competition namespace and remain separately classified in reversible metadata. Outcome is derived as 1/X/2 in supporting records; it is not an extra CSV column.

New rows have deterministic order by country, league, season, date, home and away display names. Existing global ordering and rows remain unchanged. This follows the latest consolidated schema rather than blindly reproducing the older nine-column competition export.

The current `neutral_venue` column has the already approved **official competition-format semantics**: 0 hosted/home-away format, 1 officially neutral format, empty if unknown. All 38 accepted ones are retained; the remaining 11,384 rows are zero. This does not infer physical venue neutrality or actual home advantage. Nominal home/away, evidence, confidence and qualifications remain in `neutral_venue.json` and immutable Phase 3 source records. No reversal or statistical-model exclusion was introduced. No new neutral-representation decision is needed.

The exclusions preserve five pre-regulation-completion abandonments, four no-kickoff descriptions and 59 outside-target records. `excluded_events.json` retains their complete accepted event records and binds the separate historical contexts by checksum. No score is fabricated for these records.

## C. Identifier and team compatibility

### Confirmed current conventions

Read-only inspection found newer infrastructure in the original `toto` worktree: `scripts/build_final_data.py`, `scripts/build_final_data_sum.py`, all eleven country/UEFA exports, `final_data_sum.csv`, `match_id_crosswalk.csv` and `match_id_audit.json`. The upstream `prepare` function independently reconstructed the existing consolidated CSV and crosswalk byte-for-byte and reproduced the audit exactly. The actual baseline is **182,001 rows**, not an assumed report count. A read-only code snapshot and compact derived reference sets are preserved under private `phase4/reference/`; no restricted private raw archive was copied.

The confirmed identifier algorithm is:

`competition prefix + YY(first season year)YY(second year) + YYMMDD + home token + away token`

Team tokens use the actual upstream implementation: lowercase, Unicode NFD, combining-mark removal, Unicode alphanumeric tokenization, punctuation/space boundaries, four characters from one word or two characters from each of the first two words, zero-padding, and the uniform identifier-only leading `1. FC` exception. Stored club names are not stripped to create the tokens. The generator imports the hash-bound upstream snapshot; the validator separately implements the formula without importing it.

UEFA IDs are 24 lowercase alphanumeric characters. The proposed six-character prefix is **`uefael`**, shared by the historical UEFA Cup and Europa League labels. This is a local documented registry proposal, not a claim that the existing global registry already approves it. The registry and its `uefabl` entry were not edited.

All **11,422 IDs are unique locally**, with **zero collisions against all 182,001 current global IDs** and zero exact existing identity-hash overlap. A 64-character compact-JSON SHA-256 projection identity is retained in `match_id_crosswalk.csv` using the existing `original_match_id,new_match_id` convention. It links through `source_to_output.json` to the accepted Phase 3 event, previous Phase 2 events, observations, original source file/hash/locator and historical decisions. Goals, stage, outcome and neutrality do not enter either identity. Distinct legs and replay dates remain distinct. No existing domestic or Champions League identifier changed.

### Team labels and ambiguity

The mapping retains **4,936 seasonal participant identities** and **1,319 distinct standardized display labels**. Of the seasonal identities, 3,679 have an exact or accent/punctuation-only correspondence to an existing stored baseline name supported by accepted historical/source labels; 1,257 do not. Of the display labels, **672 occur in the baseline and 647 do not**. Absent labels are not automatically certified new clubs: some may be aliases outside the established correspondences.

Original source labels after accepted occurrence corrections were projected through the accepted event orientation. Existing spelling choices require a bound seasonal/source correspondence, not fuzzy similarity, a new global identity assertion, or an inferred legal successor. Every mapping retains the original accepted labels, supporting observation IDs/hashes/locators, candidate baseline names, selected name, season and event membership. `team_mapping.json` also contains the explicitly computed four-character token.

There are **153 nonunique abbreviation groups among the new output labels**. **75 labels absent from the baseline use a token already used by another baseline label**; the baseline itself has 258 multi-label abbreviation groups. These groups can include spelling variants as well as different clubs, and are not reported as a count of distinct-club collisions. They are explicitly listed privately, never resolved by merging clubs or silently changing the approved token algorithm. No resulting match ID collides. Tokens remain abbreviations; full names and seasonal identities retain the distinction.

Available project files do not provide a complete globally unique club identity/code registry. Consequently, global legal-identity and alias consistency cannot be certified beyond the recorded correspondences. `team_compatibility_final.json` distinguishes existing labels, absent labels, candidate aliases and token overlaps. No new global team allocation or previous code rewrite occurred. This is a material integration qualification, not a standardization data-loss defect.

## D. Independent validation and corrections

The independent validator imports no producer, schema-transform or identifier-generation helper. It reparses the accepted JSON and actual CSV and checks every row, identifier, field, orientation, score, outcome, date, season, neutral flag, byte order, crosswalk, observation membership, decision binding and exclusion. It separately checks all 36 season totals, 6,506/4,916 stage totals, the early four seasons without qualifying, both recent 144-match league phases, and original/reference fingerprints. Successful transfer validation is not independent certification of every upstream historical fact or publisher lineage.

### Concrete historical error detected

A separate chronology check found one accepted return-leg date equal to its first-leg date. The detailed historical listing had repeated the earlier date. The retained raw season grid and two provider contexts indicated the later date, and [UEFA's contemporary return-leg report](https://www.uefa.com/uefaeuropaleague/news/025a-0eaad371d500-9ec4de3a2afe-1000--dortmund-ease-past-austria/) confirms it. The exact fixture/date values, source checksum and locator are private in `historical_corrections.json`.

One hash-bound Phase 4 date correction changes the derived date and its derived IDs. The original Phase 3 event, old date, conflicting source evidence, every source payload and previous reports remain byte-identical. The lineage retains both `date_evidence` (the accepted original) and `standardized_date`, with the correction ID and evidence. No score, population or historical identity changed. This is the concrete-error exception expressly allowed by the owner, not an unreported reopening of historical decisions.

Counter-evidence screening across all detailed-report date selections found one such candidate; it was individually resolved, rather than choosing dates by source majority. All **4,251 uniquely labelled two-leg chronology comparisons** and **36 final-progression checks** now pass. The retained pre-correction diagnostic is marked separately; the final independent validator also performs these checks. No estimated or scheduled date was introduced.

### Regulation-time and exception audit

All 11,422 numeric results are exhaustively compared to the accepted exact regulation score and derived outcome. Half-time absence does not exclude a result. Aggregate, shootout, cumulative extra-time and administrative values remain separate. Eleven completed-regulation administrative exceptions retain the on-field regulation result; awards remain supporting evidence.

The single match abandoned during extra time is specifically checked: regulation was completed, extra time was not, the regulation score differs from the partial abandonment score and award, and no completed extra-time score is invented. All five abandonments before completed regulation remain excluded. The standalone output contains zero outcome-only or estimated-score rows.

### Eighteen output guarantees

Each guarantee is assessed individually by the independent validator:

| No. | Guarantee | Result |
|---|---|---|
| 1 | 36 target seasons | PASS |
| 2 | 11422 standardized matches | PASS |
| 3 | 6506 main matches | PASS |
| 4 | 4916 qualifying matches | PASS |
| 5 | 11490 historical records accounted | PASS |
| 6 | 68 exclusions preserved | PASS |
| 7 | Valid supported regulation scores | PASS |
| 8 | No period contamination | PASS |
| 9 | Administrative results separate | PASS |
| 10 | Valid actual playing dates | PASS |
| 11 | No estimated dates | PASS |
| 12 | Unique approved-convention match identifiers | NOT VERIFIABLE |
| 13 | Global team identity/code compatibility | NOT VERIFIABLE |
| 14 | Neutral evidence preserved | PASS |
| 15 | Reversible provenance | PASS |
| 16 | Confirmed current CSV schema | PASS |
| 17 | Deterministic output | PASS |
| 18 | Prior data and protected files preserved | PASS |

There are **16 PASS, zero FAIL and two NOT VERIFIABLE** results. No. 12: technical format, local uniqueness and current-global collision checks pass under the proposed prefix; approved registry membership cannot be claimed before registration. No. 13: recorded participant correspondences and token generation pass, but a globally unique club identity registry and all remaining aliases are unavailable/unresolved. All other guarantees have corresponding exhaustive field, membership, byte or fingerprint checks.

### Tests, adverse checks and reproduction

**381 relevant tests pass**, including **55 new Phase 4 synthetic tests**. The selection includes Europa League acquisition/inventory/history, Champions League acquisition/inventory/history/standardization, shared schema v2, source validation and audit snapshot tests. No existing expectation was weakened. A synthetic Unicode-token expected value was corrected to the actual documented first-two-word rule; no algorithm changed.

All **22 adverse corruption cases** are detected using disposable in-memory serialized copies: missing/duplicate rows, duplicate/malformed IDs, wrong team, reversed orientation, altered regulation score, substituted extra-time/shootout/administrative scores, wrong outcome, invalid date/season/stage, lost neutrality, incorrect exclusions, broken source lineage, column-order changes, changed team token, lost original-ID crosswalk, corrupted coverage total and reversion of the corrected historical date. Accepted originals are never mutated. Earlier 21-case receipts refer to the retained pre-date-correction draft, not the final outputs.

Two fresh offline child processes prohibit socket connections and DNS resolution. All **12 standardized producer artifacts plus the independent receipt (13 artifacts)** reproduce byte-for-byte in a new temporary directory, including the CSV, IDs, ordering, mapping, exclusions, lineage, neutrality and date-correction sidecar. Recorded mapping/reference inputs are frozen decisions; code snapshots and their hashes are preserved. Execution logs and preservation receipts are not misrepresented as deterministic data artifacts.

## Season coverage

All counts below are completed-regulation matches transferred to the standardized CSV. The one extra-time abandonment is included; the five pre-90-minute abandonments are in the exclusions. Every included row has a supported exact regulation score and actual playing date; no estimated date or outcome-only row exists in any season.

| Season | Include | Main | Qualifying | Excluded | Neutral format |
|---|---:|---:|---:|---:|---:|
| 1990/1991 | 126 | 126 | 0 | 0 | 0 |
| 1991/1992 | 126 | 126 | 0 | 0 | 0 |
| 1992/1993 | 125 | 125 | 0 | 1 | 0 |
| 1993/1994 | 126 | 126 | 0 | 0 | 0 |
| 1994/1995 | 180 | 126 | 54 | 0 | 0 |
| 1995/1996 | 190 | 126 | 64 | 4 | 0 |
| 1996/1997 | 232 | 126 | 106 | 18 | 0 |
| 1997/1998 | 201 | 125 | 76 | 18 | 1 |
| 1998/1999 | 204 | 124 | 80 | 19 | 1 |
| 1999/2000 | 281 | 205 | 76 | 0 | 1 |
| 2000/2001 | 287 | 205 | 82 | 0 | 1 |
| 2001/2002 | 286 | 204 | 82 | 0 | 2 |
| 2002/2003 | 287 | 205 | 82 | 0 | 1 |
| 2003/2004 | 287 | 205 | 82 | 0 | 1 |
| 2004/2005 | 334 | 220 | 114 | 1 | 1 |
| 2005/2006 | 333 | 221 | 112 | 0 | 1 |
| 2006/2007 | 353 | 219 | 134 | 0 | 1 |
| 2007/2008 | 359 | 221 | 138 | 0 | 1 |
| 2008/2009 | 358 | 221 | 137 | 0 | 1 |
| 2009/2010 | 476 | 205 | 271 | 1 | 1 |
| 2010/2011 | 481 | 205 | 276 | 0 | 1 |
| 2011/2012 | 480 | 205 | 275 | 0 | 1 |
| 2012/2013 | 478 | 205 | 273 | 1 | 1 |
| 2013/2014 | 479 | 205 | 274 | 0 | 1 |
| 2014/2015 | 483 | 205 | 278 | 0 | 1 |
| 2015/2016 | 474 | 205 | 269 | 1 | 1 |
| 2016/2017 | 468 | 205 | 263 | 0 | 1 |
| 2017/2018 | 473 | 205 | 268 | 0 | 1 |
| 2018/2019 | 519 | 205 | 314 | 0 | 1 |
| 2019/2020 | 511 | 197 | 314 | 0 | 9 |
| 2020/2021 | 360 | 204 | 156 | 2 | 1 |
| 2021/2022 | 175 | 139 | 36 | 2 | 1 |
| 2022/2023 | 175 | 141 | 34 | 0 | 1 |
| 2023/2024 | 175 | 141 | 34 | 0 | 1 |
| 2024/2025 | 269 | 189 | 80 | 0 | 1 |
| 2025/2026 | 271 | 189 | 82 | 0 | 1 |

No match, historical stage or source observation was lost through stage normalization. Existing Phase 3 completeness qualifications remain: no missing played target fixture was identified by the bracket checks, but counts do not independently certify every historical attribute.

## E. Preservation, licensing and deliverables

The pre-phase manifest freezes **602 local files and 16 read-only reference files**. Final verification confirms **600 local files byte-identical** and the exact original prefixes of PLANNING_LOG.md and PROCESS.md followed only by authorized additions. All 16 external reference files remain unchanged. This covers all 85 original payloads (44,970,420 bytes), accepted Phase 1/2/3 artifacts, decision files, receipts, tracked domestic/UCL files, public samples and prior work. No accepted Phase 3 artifact was edited to hide the date correction.

The newer consolidated final exports, global crosswalk/audit and identifier implementation were checked read-only and remain unchanged. No private domestic or Champions League raw archives were copied or freshly certified. Protection of the inspected final exports does not imply an exhaustive check of those separate raw archives, all other worktree files, installed packages or Git object storage.

The mixed-source standardized dataset remains **private and not cleared for public redistribution**. Standardization does not remove RSSSF acknowledgements/use limits, 11footy noncommercial terms, Wikipedia attribution/share-alike obligations, or other source-specific restrictions. Publisher lineage and commercial/training rights are not newly certified. Original notices, receipts and historical observations remain available. No permission request or publication occurred. Git-ignore separation is verified; it is not a claim that the owner's existing iCloud-backed directory is device-only.

### Deliverable map

Detailed paths below are relative to `data/private/europe/europa_league/phase4/`.

| Requested deliverable | Artifact |
|---|---|
| Standalone CSV | `validated/uefa_europa_league_standardized_1990_2026.csv` |
| Reproducible generator | Public `scripts/standardize_uefa_europa_league.py`; frozen private convention/reference inputs |
| Schema assessment | `validated/schema_compatibility.json` |
| Match identifiers/audit | `validated/identifier_audit.json`, `code_policy.json`, `reference/global_reference.json` |
| Team identities/codes | `team_mapping_decisions.json`, `validated/team_mapping.json`, `team_compatibility_final.json` |
| Reversible ID/source crosswalk | `validated/match_id_crosswalk.csv`, `validated/source_to_output.json` |
| Exclusion inventory | `validated/excluded_events.json` plus immutable Phase 3 contexts |
| Neutral evidence | `validated/neutral_venue.json` |
| Season coverage | `validated/season_coverage.csv` |
| Regulation audit | `validated/score_period_audit.json`; per-event score, duration and administrative evidence in lineage |
| Independent implementation | Public `scripts/verify_uefa_europa_league_standardization.py` |
| Independent results | `independent_validation.json`, `chronology_validation.json` |
| Output guarantees | All eighteen entries in `independent_validation.json` |
| Adverse results | `adverse_validation.json`; public `scripts/check_uefa_europa_league_corruption.py` |
| Offline checksums | `reproduction.json`; public `scripts/reproduce_uefa_europa_league_standardization.py` |
| Preservation | `protected_before.json`, `verification.json` |
| Licensing/publication | This section and existing preserved Phase 1 rights records |
| Completion report | This document |

`approval.json` binds the accepted inputs and working decisions; `validated/historical_corrections.json` records the one new evidence-backed correction. `validated/summary.json` reconciles all counts and records the non-destructive integration dry run. Private supporting code preserves reference/mapping/diagnostic preparation procedures. Descriptively named earlier drafts and before-correction receipts are retained and are not accepted final outputs.

New public files are this report, four Phase 4 scripts (generator, independent verifier, corruption checker, offline reproducer), and `tests/test_uefa_europa_league_standardization.py`. Only PLANNING_LOG.md and PROCESS.md were appended among pre-existing files. Earlier uncommitted phase work remains intact. No existing final-data export, global registry/crosswalk/audit, domestic/UCL record, statistical model, Streamlit file or other worktree was changed. Nothing was staged, committed, merged, rebased or pushed.

Read-only checks from this worktree, using the existing compatible environment:

```sh
PYTHONPATH=src python -B -m scripts.standardize_uefa_europa_league --check
PYTHONPATH=src python -B -m scripts.verify_uefa_europa_league_standardization --check
PYTHONPATH=src python -B -m pytest -q tests/test_uefa_europa_league_standardization.py
```

The generator and validation receipts exclusive-create outputs; preserve an existing receipt before rerunning the corruption/reproduction commands. Detailed outputs are restricted to private or temporary destinations.

## F. Integration readiness

The standalone dataset is technically validated against the **confirmed latest consolidated schema**. The non-destructive dry run finds zero local/global match ID collisions and zero exact fixture overlap against the current 182,001-row baseline; the prospective combined count is **193,423**. This count is verified arithmetic against the current frozen inventory, not an instruction to replace the combined database. No combined output was written.

Integration remains conditional on registering the proposed competition namespace for both historical labels and accepting or extending the explicit identity/alias handling. All known code ambiguity groups are visible; no unique-team-code guarantee is implied. Current-global match uniqueness is verified under the proposed prefix, while future global changes require a fresh check. No neutral-column decision is needed because its existing semantics are confirmed. Publication remains constrained by source rights.

The genuine owner decisions belong to finalization: accept the proposed competition registry extension and the documented scope of identity compatibility, authorize any future integration, and separately decide whether a permitted publication scope exists. Routine projection and the evidenced date correction were completed under the current authorization; no extra approval was requested for them.

## G. Phase 5 readiness and stop

The standalone result is ready for **conditional final acceptance**. Before integration, Phase 5 should recheck the current baseline and hashes, resolve/accept registry and identity qualifications, confirm the publication allowlist/rights, and approve any subsequent integration explicitly. Alias ambiguities must not be silently treated as legal club mergers or repaired by arbitrary token changes.

No technical standardization, score-transfer, exclusion, lineage, chronology, preservation or reproduction blocker remains. The two compatibility qualifications above remain material and prevent an unconditional PASS. **Phase 5 has not started. Await explicit owner authorization.**
