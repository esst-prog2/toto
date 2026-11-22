# Ligue 1 — Phase 4 independent structural validation

Date: 2026-11-22. Original `toto` worktree, branch `feature/data-collection`, unchanged HEAD `81225118ced664f113c19b87cff8095b0333ccda`. See [Phase 2](ligue-1-feasibility.md) and [Phase 3](ligue-1-inventory.md); both remain frozen.

## Scope and independently measured reconciliation

This phase independently parses immutable originals and creates structural reports/review queues. It does not acquire sources, repair data, decide exceptions or eligibility, standardize, train or integrate application data.

**12,707 target-window source observations = 8,369 historical CSV rows + 4,338 modern ordinary-file slots.** There are **12,606 score-bearing observations and 101 explicitly cancelled/unscored slots**. The 36-season target has **35 represented seasons**, not 36 complete or historically certified seasons. Supplemental historical overlap rows and the preserved 2025/26 full version are not counted as extra primary fixtures.

## Preservation and source provenance

All **558 prior private files**, **165 tracked public files**, and **80 Phase 2–3 entries** (72 private files and eight uncommitted public files) passed protected SHA-256 checks. Nested Phase 3 protection also retains its 52 Phase 2 entries. The entire existing planning-log prefix is protected; only new measured entries are appended. All eight earlier competition datasets, originals, manifests and evidence remain unchanged. The application and promotional worktree are untouched.

Existing pins remain engsoccerdata **`872c5c354161ace8408f3091b758c6af4cccca94`** and OpenFootball Europe **`63df627f3c87ce71708f016522ea236cf74332c3`**. No network acquisition occurred. All fourteen existing dataset originals and seven supporting notices were independently checked against SHA-256, byte-size and saved Git-tree blob identities. The acquisition manifests and per-file receipts retain exact URLs, revisions, timestamps and notices. Every primary observation retains source path/SHA, physical line, literal source values, raw-line SHA-256 and a deterministic source-bound audit ID. These are **not standardized match IDs**.

## Classification: structural fields versus historical confidence

| Disjoint record-field consistency class | Count | Meaning |
|---|---:|---|
| Consistent scored source fields | **10,711** | Exercised intrinsic score/date/team-field rules pass; not historical certification or inclusion approval. |
| Source-label-inconsistent scored records | **1,895** | Auxiliary CSV `result` contradicts numeric goals; originals unchanged, numbers not automatically rejected/corrected. |
| Explicitly cancelled/unscored slots | **101** | Preserved 2019/20 unplayed schedule slots; not ordinary missing results. |
| Malformed/numeric-field conflicts | **0** | No invalid score tokens, FT/goal/derived-numeric contradictions, impossible dates or malformed labels found in primary observations. |
| Unexplained incomplete observations | **0** | No other missing-score records. |
| **Total** | **12,707** | No record loss or screening. |

Thus 12,606 have internally consistent numeric goals/FT fields; 1,895 additionally have defective auxiliary labels. “Invalid” must distinguish these confirmed label defects from malformed numeric records (zero). Missing acquisitions and relational identity problems are separate, not invented rows in this partition. All classifications are diagnostic; there is no accepted/excluded/HOLD OUT policy.

Across all flag categories, **2,473 unique primary observations are flagged** and **10,234 have no enumerated fixture-level flags**. An unflagged record is still not independently historically certified or cleared for training.

## Complete 36-season structural table

Expected is scheduled regular-season slots. “Consistent” excludes auxiliary-label defects and cancellations; “Flagged” includes grouped and fixture-level flags and overlaps those classes. CSV stage remains undocumented even where counts agree.

| Season | Observed / expected | Scored | Literal clubs / expected | Consistent | Label defects | Cancelled | Flagged | Fixture queue |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1990/1991 | 380 / 380 | 380 | 21 / 20 | 323 | 57 | 0 | 90 | 39 |
| 1991/1992 | 380 / 380 | 380 | 20 / 20 | 309 | 71 | 0 | 71 | 0 |
| 1992/1993 | 380 / 380 | 380 | 20 / 20 | 306 | 74 | 0 | 74 | 0 |
| 1993/1994 | 380 / 380 | 380 | 20 / 20 | 314 | 66 | 0 | 67 | 1 |
| 1994/1995 | 0 / 380 | 0 | absent / 20 | 0 | 0 | 0 | 0 | 0 |
| 1995/1996 | 380 / 380 | 380 | 20 / 20 | 306 | 74 | 0 | 74 | 0 |
| 1996/1997 | 380 / 380 | 380 | 20 / 20 | 293 | 87 | 0 | 90 | 3 |
| 1997/1998 | 306 / 306 | 306 | 18 / 18 | 229 | 77 | 0 | 77 | 0 |
| 1998/1999 | 306 / 306 | 306 | 18 / 18 | 241 | 65 | 0 | 65 | 0 |
| 1999/2000 | 306 / 306 | 306 | 18 / 18 | 240 | 66 | 0 | 66 | 0 |
| 2000/2001 | 306 / 306 | 306 | 18 / 18 | 234 | 72 | 0 | 72 | 0 |
| 2001/2002 | 306 / 306 | 306 | 18 / 18 | 245 | 61 | 0 | 62 | 1 |
| 2002/2003 | 380 / 380 | 380 | 20 / 20 | 292 | 88 | 0 | 88 | 0 |
| 2003/2004 | 380 / 380 | 380 | 20 / 20 | 284 | 96 | 0 | 96 | 0 |
| 2004/2005 | 380 / 380 | 380 | 20 / 20 | 309 | 71 | 0 | 72 | 1 |
| 2005/2006 | 380 / 380 | 380 | 20 / 20 | 288 | 92 | 0 | 94 | 2 |
| 2006/2007 | 379 / 380 | 379 | 20 / 20 | 297 | 82 | 0 | 82 | 0 |
| 2007/2008 | 380 / 380 | 380 | 20 / 20 | 283 | 97 | 0 | 97 | 0 |
| 2008/2009 | 380 / 380 | 380 | 20 / 20 | 277 | 103 | 0 | 103 | 0 |
| 2009/2010 | 380 / 380 | 380 | 20 / 20 | 276 | 104 | 0 | 105 | 1 |
| 2010/2011 | 380 / 380 | 380 | 20 / 20 | 287 | 93 | 0 | 93 | 0 |
| 2011/2012 | 380 / 380 | 380 | 20 / 20 | 287 | 93 | 0 | 93 | 0 |
| 2012/2013 | 380 / 380 | 380 | 20 / 20 | 278 | 102 | 0 | 102 | 0 |
| 2013/2014 | 380 / 380 | 380 | 20 / 20 | 276 | 104 | 0 | 105 | 1 |
| 2014/2015 | 380 / 380 | 380 | 20 / 20 | 380 | 0 | 0 | 31 | 31 |
| 2015/2016 | 380 / 380 | 380 | 20 / 20 | 380 | 0 | 0 | 66 | 66 |
| 2016/2017 | 380 / 380 | 380 | 20 / 20 | 380 | 0 | 0 | 52 | 52 |
| 2017/2018 | 380 / 380 | 380 | 20 / 20 | 380 | 0 | 0 | 32 | 32 |
| 2018/2019 | 380 / 380 | 380 | 20 / 20 | 380 | 0 | 0 | 51 | 51 |
| 2019/2020 | 380 / 380 | 279 | 20 / 20 | 279 | 0 | 101 | 131 | 131 |
| 2020/2021 | 380 / 380 | 380 | 20 / 20 | 380 | 0 | 0 | 60 | 60 |
| 2021/2022 | 380 / 380 | 380 | 20 / 20 | 380 | 0 | 0 | 40 | 40 |
| 2022/2023 | 380 / 380 | 380 | 20 / 20 | 380 | 0 | 0 | 13 | 13 |
| 2023/2024 | 306 / 306 | 306 | 18 / 18 | 306 | 0 | 0 | 27 | 27 |
| 2024/2025 | 306 / 306 | 306 | 18 / 18 | 306 | 0 | 0 | 12 | 12 |
| 2025/2026 | 306 / 306 | 306 | 18 / 18 | 306 | 0 | 0 | 20 | 20 |

### Relational checks and incomplete coverage

- **1994/95:** entirely absent, expected 380 scheduled fixtures. No participating-club list, artificial fixture IDs or guessed match rows created.
- **2006/07:** 379 observed; the sole missing literal pairing is `FC Nantes`–`Toulouse FC`. Date and result remain null in the separate coverage-gap registry, not added to the observation archive.
- **1990/91:** 380 observations but 21 literal labels rather than 20. `Brest Armorique FC` and `Stade Brest` split 38 source fixtures. The literal 21-label pairing universe has 40 absent pairs; these are identity-related structural diagnostics, **not 40 established lost matches**. No merge applied.
- Other represented seasons have expected literal club/pairing coverage. There are zero duplicate directed pairings, within-source conflicting duplicates, same-team/date collisions and case/NFC collisions in the primary scope.
- All twelve modern files have regular-season stages, complete round numbering and expected per-round allocations (38×10 or 34×9). Repeated round headings preserve rescheduling blocks. No modern playoff/cup or other-stage row was found.
- All 8,369 older primary CSV observations are tier-1-labelled but have **no explicit stage/round field**. Pairing/format agreement cannot independently certify historical competition/stage. No non-league row was positively identified; undocumented stage remains an explicit source limitation.
- Per-season appearance allocations and source-line date regressions are retained. File/matchday order is not chronological evaluation order; rescheduled dates need not be monotonically ordered in a source.

## Exact result-label contradiction analysis

Independent full-CSV parsing reconfirms **5,489** affected rows, of which **1,895** are in the primary older window and **3,594** are supplemental/outside that primary window. Every affected row is identified by source-bound ID, line, season, original labels/date/FT and diagnostic goal-derived outcome. Both “all defects are pre-2015/16 D-on-away” and “every pre-2015/16 away victory is labelled D” independently evaluate true.

| Source season labels | Rows | H→H | D→D | A→D defect | A→A |
|---|---:|---:|---:|---:|---:|
| 1932–2014 | 26,007 | 13,661 | 6,857 | **5,489** | 0 |
| 2015–2024 | 3,551 | 1,547 | 910 | 0 | 1,094 |

The numerical fields (FT, home/away goals, sum and goal difference) agree internally for all **29,558** historical rows. This isolates an auxiliary-label consistency defect; it does **not** prove numerical historical accuracy. The exact upstream generation cause is unestablished. Administrative outcomes can disagree with goal-derived outcome even where the auxiliary label technically agrees with the numbers. No source label or score is rewritten or silently reinterpreted.

`GROUP:CSV_RESULT_LABEL` is one grouped investigation containing all 5,489 affected row bindings and season counts. Primary label-only rows are not expanded into thousands of duplicate manual tasks. Independent historical sample verification and later approved policy remain necessary.

## Historical dates and chronological suitability

All historical dates are syntactically valid ISO dates: **zero impossible/unparseable dates**. The broader CSV has **1,162 unusual dates relative to the conventional source-season window**, but **zero belong to the primary 1990/91–2013/14 window**.

| Literal source season | Source date | Rows | Structural interpretation, not historical correction |
|---|---|---:|---|
| 1932/1933 | 1933-07-01 | 182 | Single-date season cluster; suspected placeholder/season-label issue |
| 1933/1934 | 1934-07-01 | 240 | Single-date season cluster; suspected placeholder/season-label issue |
| 1934/1935 | 1935-07-01 | 240 | Single-date season cluster; suspected placeholder/season-label issue |
| 1935/1936 | 1936-07-01 | 240 | Single-date season cluster; suspected placeholder/season-label issue |
| 1936/1937 | 1937-07-01 | 240 | Single-date season cluster; suspected placeholder/season-label issue |
| 1946/1947 | 1946-03-10 | 10 | Before conventional season start; source-date/year question |
| 1967/1968 | 1968-07-03 | 2 | After conventional June boundary; extended-season possibility requires evidence |
| 1967/1968 | 1968-07-05 | 8 | After conventional June boundary; extended-season possibility requires evidence |

The first five clusters total **1,142 suspected placeholder records**. The ten `1946-03-10` records predate the conventional 1946/47 start. The ten July 1968 records might represent an extended season rather than errors; no shift to another day, month or year is inferred. All 1,162 remain one grouped date-quality investigation, with exact original facts and cluster memberships. They are not added to primary review counts.

Primary CSV dates are explicit source fields; modern day/month headings are explicit, with missing years uniquely resolved against season and weekday. These syntactic facts do not certify actual playing dates. Source dates, cancelled scheduled dates, independently supported kickoff/completion dates and administrative decision dates have separate fields. **All effective-result-availability fields remain unset: Phase 4 chooses no final date policy.** Ordinary dates remain uncertified event/availability proxies, not blanket approved chronology.

Known replay/ratification cases and 40 long-span rounds identify chronology research priorities. No earlier kickoff date is substituted for replay/completion, and no final result is exposed to a training/backtesting consumer: none is created or run in this phase. Later policy must explicitly address availability before chronological use.

## Independent overlap and historical identity review

Independent comparison preserves the five approved 2014/15 diagnostic correspondences, with all 380 dates/goals agreeing. The eleven scored overlapping seasons yield **3,893 uniquely matched pairings**, all matching dates; one score representation differs. Comparison mappings are explicit season-level diagnostics only; original club labels and identities remain unchanged.

| Mismatch category | Finding |
|---|---|
| Identity | 2015/16: historical `AC Ajaccio` versus modern `Gazélec FC Ajaccio`; **38 unmatched pairings per source**, 342 matched. These distinct labels are not aliases; no one-to-one fixture merge is inferred. |
| Date | Zero discrepancies across matched overlap pairings. Source agreement is not independent historical certification. |
| Score | One: Bastia–Lyon 2016/17, historical 0–3 versus modern 0–0 `[awarded]`. |
| Missing fixture | Separately, older 2006/07 Nantes–Toulouse absent. The Ajaccio unmatched sets are identity conflicts, not 38 proven missing matches. |
| Administrative interpretation | Bastia–Lyon and Nantes–Bastia numerical/winner semantics unresolved; later ratification/replay availability cases preserved separately. Categories overlap, not additional match losses. |

The literal label/season catalogue preserves 105 historical/modern labels without a continuity merge. In particular, identical Toulouse labels across decades do not establish historical entity continuity, Paris FC is not PSG, and similarly named/reconstituted clubs are not automatically unified. The 38 Brest primary fixtures and 38 modern Ajaccio-conflict fixtures are individually visible in the queue. Wider historical entity questions remain contextual limitations, not unsupported global substitutions.

## Administrative and interrupted fixtures

Each case requires exactly one matching primary fixture with the preserved date/FT facts before evidence metadata is attached. Original alternatives remain separately bound; no source score is chosen over another. Retained documentary evidence access/finality limitations remain unchanged.

| Case | Preserved source facts | Separate evidence/date fields and unresolved question |
|---|---|---|

| Bastia–Lyon 2016/17 | Primary modern: 2017-04-16, **0–0 `[awarded]`**; supplemental CSV: same date, **0–3** | Numerical administrative representation and final recognized outcome/availability require primary decision/appeal review. A goal-derived D is not declared the official outcome. |

| Nantes–Bastia 2013/14 | Primary CSV: 2013-08-10, **0–0** | Retained judicial evidence establishes penalty defeat for Nantes and victory for Bastia; numerical score semantics and earliest availability remain unresolved. Supported event date retained separately. |

| Nice–Marseille 2021/22 | Primary modern: 2021-10-27, **1–1**; agreeing supplemental CSV | Retained contemporary account supports replay/completion on October 27 after August interruption. The original August kickoff day is not invented. Effective-date policy remains undecided. |

| Montpellier–Clermont 2023/24 | Primary modern: 2023-11-29, **1–1** | October 8 interruption and October 25 replay order preserved in retained evidence. Full replay result/completion/finality confirmation remains later work; indexed evidence is not upgraded to directly inspected certification. |

| Montpellier–Saint-Étienne 2024/25 | Primary modern: 2025-03-16, **0–2 `[awarded]`** | Source annotation is preserved, not treated as an independently certified final decision. Actual playing/interruption, legal decision and availability require evidence. |

| Nantes–Toulouse 2025/26 | Primary modern: 2026-05-17, **0–0** | Retained club account supports event/abandonment May 17; official ratification dated **May 27** is separate. No final availability or appellate-finality policy applied. |

No corrections, inclusions, exclusions or HOLD OUT decisions are authorized by these case records. The missing Nantes–Toulouse 2006/07 fixture remains a coverage-gap case, not a fabricated seventh primary observation.

## Deduplicated review queue

**584 unique primary fixture entries + two grouped source-quality investigations.** The record-level report retains every primary observation; the fixture queue includes all records with a non-systematic flag. Label-only defects are routed to their grouped job.

| Flag category | Primary observations |
|---|---:|
| `ADMINISTRATIVE_RESULT_SEMANTICS` | 1 |
| `ADMINISTRATIVE_SCORE_CONFLICT` | 1 |
| `BREST_DUAL_LABEL_IDENTITY` | 38 |
| `CANCELLED_UNPLAYED_SLOT` | 101 |
| `CROSS_SOURCE_SCORE_OR_DATE_CONFLICT` | 1 |
| `DISTINCT_AJACCIO_CLUB_IDENTITY` | 38 |
| `INTERRUPTED_REPLAY` | 1 |
| `POST_EVENT_RATIFICATION` | 1 |
| `REPLAY_DATE_CONTEXT` | 1 |
| `SOURCE_MARKED_ADMINISTRATIVE` | 2 |
| `SYSTEMATIC_SOURCE_LABEL_DEFECT` | 1895 |
| `UNUSUAL_SCORE` | 22 |
| `WIDE_ROUND_SPAN` | 394 |

Overlap accounting:

- Label-defect primary members: **1,895**.
- Fixture-level queue: **584**.
- Intersection: **6**.
- Union: **1,895 + 584 − 6 = 2,473 uniquely flagged observations**.
- Label-only grouped members: **1,889**.
- Category flag instances: **2,496**, not 2,496 distinct fixtures.
- No enumerated fixture-level flags: **10,234**.

All **101 cancelled slots** are visible as cancelled/unplayed, not as malformed or unexplained missing results. All **40 scheduling cases** and their **394 distinct fixture slots** are preserved; these include the 17 original Phase 2 cases. Per-round IDs and fixture membership are retained. Cancelled scheduled spans are distinguished from source dates of scored fixtures. Long spans/high scores are research flags, not confirmed historical errors.

The two grouped jobs additionally retain supplemental members outside the primary window: 3,594 label-defect rows and all 1,162 date candidates. These are not added to 12,707 primary observations or 2,473 primary flags. The missing-season/missing-pairing registry is separate, with no phantom source rows. Queue entries can be researched in round/cancellation batches; their count is not a claim that 584 independent individual fact-certifications have been performed.

## Tests and independent reproducibility

**45 new synthetic tests, 102 focused Ligue 1 tests and all 1,177 repository tests passed**, including all **seven app/launcher tests**. No failed/skipped/unverified tests in that run. Full suite: 13.26 seconds pytest time, 13.99 seconds process wall time. The existing offline temporary Python 3.13.12 environment was reused with pytest 9.1.1 and pandas 3.0.6; no installation, upgrade or original `.venv` changes. Caches, test outputs and bytecode settings keep generated runtime files outside the worktree.

Tests cover independent syntax, exact source/physical-line identity, multibyte/CRLF/multiline bindings, strict malformed-score/date handling, cancellation and awards, numeric/label separation, halftime consistency, repeated rounds/round allocation, source identity conflicts, missing coverage, queue deduplication/group routing, known-case source-fact binding, date-policy non-implementation and protected fingerprints.

A separate raw extractor reconciled all 12,707 primary observations and all 29,558 historical CSV rows without using the production Phase 4 parsers. It independently recomputed source hashes/Git blobs, row/score/date/group counts, raw-line hashes, queue intersections and scheduling membership. Both outputs were regenerated in a safe temporary directory and compared byte-for-byte and by SHA-256, without overwriting saved artifacts.

| Output | Bytes | SHA-256 |
|---|---:|---|
| `phase4_review_queue.json` | 2,761,449 | `32a35ee8acabe9d48f0fe68fcb3ac6cd0f708a53edfaa0b39e8ca8317225a4d8` |
| `phase4_structural_validation.json` | 24,828,538 | `d4b6ccb74df1b74ea8bdcc8dbdca737f9163b734a16a3f1c64131e03cb66eff3` |

Reproduce offline with a working project-compatible Python, `PYTHONPATH=src:.` and `PYTHONDONTWRITEBYTECODE=1`:

```sh
python -B -m scripts.validate_ligue1_structure --check
python -B -m pytest tests/test_ligue1_feasibility.py tests/test_ligue1_history.py tests/test_ligue1_structure.py -q -p no:cacheprovider
```

For independent-location regeneration, serialize both return values of `validate_ligue1_structure.build()` with `collect_ligue1_feasibility.encode()` to new temporary paths, then compare bytes/SHA with the two saved artifacts. `--init` creates a new protection baseline only when absent; originals and prior baselines are never overwritten.

## Files, privacy and permission limits

New public files:

- `scripts/validate_ligue1_structure.py`.
- `tests/test_ligue1_structure.py`.
- `docs/ligue-1-validation.md`.

Only `PLANNING_LOG.md` is appended; earlier public files remain unchanged. No application, promotional, original dataset or previous standardized file is edited. No staging/commit/push/merge.

Private outputs under `data/private/france/ligue_1/` include the new protected baseline, final structural report, review queue, independent verification receipt, test/helper evidence and final file/checksum registry. Intermediate Phase 4 drafts are retained under explicitly different names, not used as authoritative reports. All originals and Phase 2–3 evidence remain frozen. `phase4_final_verification.json` lists exact generated filenames/hashes and privacy checks. No private datasets or `.DS_Store` files are staged/tracked as part of this work.

Licensing remains separate: engsoccerdata’s README noncommercial statement, GPL package metadata and upstream dataset rights are unresolved in scope; OpenFootball CC0 covers rights held without clearing every upstream right. Original data remain private. Technical validation, independent historical confidence, training suitability and permission are separate classifications. **No training or redistribution clearance is claimed.**

## Phase 5 research priorities and remaining gaps

After separate approval, independently sample the **35 represented seasons** and research the six bound administrative/replay cases, the 2015/16 Ajaccio identities, Brest continuity, the missing Nantes–Toulouse 2006/07 fixture, high-score candidates and scheduling dates. Keep grouped label/date investigations separate from individual fixture certification. Preserve all remaining uncertainties rather than inferring a result or effective date.

**1994/95 is still wholly absent.** Reaching the 36-season source target requires a separately approved, permission-compatible dated source; Phase 4 acquired none. The 2006/07 missing fixture needs independently dated primary evidence and a later explicit decision before any supplementation. Earlier-than-1990 date/identity questions remain outside primary standardization scope. No population historical certification is claimed. Stop after Phase 4 for user review.
