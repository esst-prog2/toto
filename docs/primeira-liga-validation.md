# Portuguese Primeira Liga — Phase 4 independent structural validation

Date: 2026-11-23. Original toto worktree on feature/data-collection, HEAD `0bb6f393c89fdcc37a52a56bb31e458ff131de47`. Structural validation only: no acquisition, historical evidence research, source preference, normalization approval, dispositions, screening, standardized CSV or final match IDs, prediction eligibility, training, application changes or Git publication.

## Independent method and immutable source scope

A newly written CSV DictReader parser and separate modern text/date parser reconstruct every source observation directly from immutable originals. The validator does not invoke Phase 2 or Phase 3 parsers/assessment functions. It compares all reconstructed facts, original historical fields, audit identities, physical line ranges and physical-record hashes with the frozen Phase 3 population. Exact original labels, scores and literal records remain stored. Overlap reconstruction uses the frozen, explicitly season-bound diagnostic label links, validates complete one-to-one participant boundaries and reconstructs fixture correspondences independently; it does not trust saved comparison totals or apply a global alias.

All ten originals pass receipts, SHA-256, pinned blob and size checks where applicable: historical `jalapic/engsoccerdata@872c5c354161ace8408f3091b758c6af4cccca94/data-raw/portugal.csv`, eight OpenFootball `openfootball/europe@63df627f3c87ce71708f016522ea236cf74332c3/portugal/*_pt1.txt` files for 2018/19–2025/26, and the unchanged RSSSF 1990/91 retrieval snapshot. RSSSF has no Git identity and never enters the dated observation population. No network or source acquisition occurred.

The new baseline freezes 94 Phase 2–3 public/private entries plus the planning prefix, nested inside earlier 59 Phase 2 entries and 1,037 prior private / 228 public fingerprints. The previous eleven competitions retain 127,927 distinct screened historical records. Source receipts, assessments, code, test logs and earlier outputs remain byte-identical.

## Population and classifications

| Measure | Verified count |
|---|---:|
| Historical dated/scored observations | 8,958 |
| Modern dated/scored observations | 2,448 |
| Total dated observations | 11,406 |
| Matched overlap pairs | 2,142 |
| Conditional distinct sourced fixtures | 9,264 |
| Represented seasons | 32 |
| 36-season fixture expectation | 10,562 |
| Missing early dated-source expected slots | 1,298 |
| Structurally valid scored observations | 11,405 |
| Source-label defective observations | 1 |
| Incomplete observations | 0 |
| Other invalid date/scope/score/derived-field observations | 0 |
| Deduplicated flagged source observations | 207 |
| Unflagged source observations | 11,199 |

The 207 flagged observations include the one invalid-label observation and 206 structurally valid observations requiring historical/scheduling review. Thus 11,199 unflagged + 206 valid flagged = 11,405 structurally valid scored observations; adding the one literal label defect gives 11,406. No record is accepted, excluded, held out or declared NOT PLAYED. Structural validity is not historical certification. The conditional 9,264 is a source-coverage reconciliation under diagnostic identity assumptions, not a standardized-record total.

## Complete season-level validation

| Season | Historical observations | Modern observations | Conditional sourced slots | Structurally valid observations | Flagged observations |
|---|---:|---:|---:|---:|---:|
| 1994/1995 | 306 | 0 | 306 | 306 | 0 |
| 1995/1996 | 306 | 0 | 306 | 306 | 1 |
| 1996/1997 | 306 | 0 | 306 | 306 | 1 |
| 1997/1998 | 306 | 0 | 306 | 306 | 2 |
| 1998/1999 | 306 | 0 | 306 | 306 | 2 |
| 1999/2000 | 306 | 0 | 306 | 306 | 0 |
| 2000/2001 | 306 | 0 | 306 | 306 | 0 |
| 2001/2002 | 306 | 0 | 306 | 306 | 1 |
| 2002/2003 | 306 | 0 | 306 | 306 | 1 |
| 2003/2004 | 306 | 0 | 306 | 306 | 0 |
| 2004/2005 | 306 | 0 | 306 | 306 | 0 |
| 2005/2006 | 306 | 0 | 306 | 306 | 0 |
| 2006/2007 | 240 | 0 | 240 | 240 | 0 |
| 2007/2008 | 240 | 0 | 240 | 240 | 0 |
| 2008/2009 | 240 | 0 | 240 | 240 | 0 |
| 2009/2010 | 240 | 0 | 240 | 240 | 1 |
| 2010/2011 | 240 | 0 | 240 | 240 | 0 |
| 2011/2012 | 240 | 0 | 240 | 239 | 1 |
| 2012/2013 | 240 | 0 | 240 | 240 | 0 |
| 2013/2014 | 240 | 0 | 240 | 240 | 0 |
| 2014/2015 | 306 | 0 | 306 | 306 | 0 |
| 2015/2016 | 306 | 0 | 306 | 306 | 0 |
| 2016/2017 | 306 | 0 | 306 | 306 | 1 |
| 2017/2018 | 306 | 0 | 306 | 306 | 0 |
| 2018/2019 | 306 | 306 | 306 | 612 | 4 |
| 2019/2020 | 306 | 306 | 306 | 612 | 26 |
| 2020/2021 | 306 | 306 | 306 | 612 | 41 |
| 2021/2022 | 306 | 306 | 306 | 612 | 28 |
| 2022/2023 | 306 | 306 | 306 | 612 | 32 |
| 2023/2024 | 306 | 306 | 306 | 612 | 20 |
| 2024/2025 | 306 | 306 | 306 | 612 | 18 |
| 2025/2026 | 0 | 306 | 306 | 306 | 27 |

## Historical CSV: all 31 seasons

Exact source column order remains:

```text
Date,Season,home,visitor,FT,hgoal,vgoal,division,tier,totgoal,goaldif,result
```

Source season is starting-year integer text; source day is ISO YYYY-MM-DD. The independent parser verifies schema/field widths and retains original strings. Structural checks verify P1/tier1, nonnegative integer full-time goals, FT syntax, H/D/A, total goals and goal differences, canonical dates/season boundaries, literal labels, self-fixtures, duplicate/conflicting pairs, source-order patterns and identity diagnostics.

| Season | Observed / scored | Literal / expected clubs | Expected slots | Distinct / missing literal pairs | Valid observations | Date range |
|---|---:|---|---:|---|---:|---|
| 1994/1995 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 306 | 1994-08-20 – 1995-06-15 |
| 1995/1996 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 306 | 1995-08-20 – 1996-05-12 |
| 1996/1997 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 306 | 1996-08-23 – 1997-06-15 |
| 1997/1998 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 306 | 1997-08-23 – 1998-05-17 |
| 1998/1999 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 306 | 1998-08-21 – 1999-05-30 |
| 1999/2000 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 306 | 1999-08-20 – 2000-05-14 |
| 2000/2001 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 306 | 2000-08-18 – 2001-05-27 |
| 2001/2002 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 306 | 2001-08-10 – 2002-05-05 |
| 2002/2003 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 306 | 2002-08-22 – 2003-06-01 |
| 2003/2004 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 306 | 2003-08-16 – 2004-05-09 |
| 2004/2005 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 306 | 2004-08-28 – 2005-05-22 |
| 2005/2006 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 306 | 2005-08-19 – 2006-05-07 |
| 2006/2007 | 240 / 240 | 16 / 16 | 240 | 240 / 0 | 240 | 2006-08-25 – 2007-05-20 |
| 2007/2008 | 240 / 240 | 16 / 16 | 240 | 240 / 0 | 240 | 2007-08-17 – 2008-05-11 |
| 2008/2009 | 240 / 240 | 16 / 16 | 240 | 240 / 0 | 240 | 2008-08-22 – 2009-05-24 |
| 2009/2010 | 240 / 240 | 16 / 16 | 240 | 240 / 0 | 240 | 2009-08-14 – 2010-05-09 |
| 2010/2011 | 240 / 240 | 16 / 16 | 240 | 240 / 0 | 240 | 2010-08-13 – 2011-05-14 |
| 2011/2012 | 240 / 240 | 17 / 16 | 240 | 240 / 32 | 239 | 2011-08-12 – 2012-05-12 |
| 2012/2013 | 240 / 240 | 16 / 16 | 240 | 240 / 0 | 240 | 2012-08-17 – 2013-05-19 |
| 2013/2014 | 240 / 240 | 16 / 16 | 240 | 240 / 0 | 240 | 2013-08-16 – 2014-05-11 |
| 2014/2015 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 306 | 2014-08-15 – 2015-05-23 |
| 2015/2016 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 306 | 2015-08-14 – 2016-05-15 |
| 2016/2017 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 306 | 2016-08-12 – 2017-05-21 |
| 2017/2018 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 306 | 2017-08-06 – 2018-05-13 |
| 2018/2019 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 306 | 2018-08-10 – 2019-05-19 |
| 2019/2020 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 306 | 2019-08-09 – 2020-07-26 |
| 2020/2021 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 306 | 2020-09-18 – 2021-05-19 |
| 2021/2022 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 306 | 2021-08-06 – 2022-05-15 |
| 2022/2023 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 306 | 2022-08-05 – 2023-05-27 |
| 2023/2024 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 306 | 2023-08-11 – 2024-05-18 |
| 2024/2025 | 306 / 306 | 18 / 18 | 306 | 306 / 0 | 306 | 2024-08-09 – 2025-05-17 |

Historical totals independently equal 8,958. Zero unscored, invalid dates, score/derived-field contradictions, duplicate/conflicting pairs or physical source-order reversals were found. No competition-field contamination was found. Historical per-row stage is not explicit; ordinary pairing/count completeness supports regular-season scope but cannot certify every administrative or historical event. There are 18 historical unusual-score observations, flagged without correction.

### Feirense: label defect versus actual missing fixtures

At CSV line **4877**, **2011-08-14**, the original home value is `Feirense ` and away is `Nacional`. Exact audit identity: `5265c556cbad744e664ed5f55bec58e0117a48b279d3ef3aa1f435b2753aa25b`. Original literal text/fields remain unchanged in the structural registry.

| Accounting | Observations | Clubs | Directed pairs | Missing pairs | Duplicate pairs |
|---|---:|---:|---:|---:|---:|
| Literal original | 240 | 17 | 240 | 32 | 0 |
| Hypothetical one-occurrence whitespace link | 240 | 16 | 240 | 0 | 0 |

The hypothetical comparison changes only that exact observation in an in-memory copy. It neither alters the original nor approves normalization. This demonstrates structural reconcilability without loss/duplication, not 32 proven missing historical matches. Phase 5 should establish source/team context; Phase 6 would require a separately approved narrow processing decision.

## Modern originals: all eight seasons

Every original contains 306 scored / zero unscored observations, 18 literal clubs, 306 unique directed pairings and all 34 rounds with nine matches and 18 distinct participants per round. There are zero duplicate/missing pairings, invalid dates/scores/HT values, round-participant errors, detected other stages, reserve-team labels or NFC/casefold collisions. Exact titles identify the top flight. No explicit cancellation, award or abandonment annotations occur in the acquired files. Absence of annotation is not administrative certification.

| Season | Scored | First / last source date | Wide rounds | Reversal pairs | Unusual scores |
|---|---:|---|---:|---:|---:|
| 2018/2019 | 306 | 2018-08-10 / 2019-05-19 | 0 | 0 | 2 |
| 2019/2020 | 306 | 2019-08-09 / 2020-07-26 | 2 | 2 | 2 |
| 2020/2021 | 306 | 2020-09-18 / 2021-05-19 | 4 | 4 | 0 |
| 2021/2022 | 306 | 2021-08-06 / 2022-05-15 | 2 | 3 | 3 |
| 2022/2023 | 306 | 2022-08-05 / 2023-05-27 | 3 | 4 | 0 |
| 2023/2024 | 306 | 2023-08-11 / 2024-05-18 | 2 | 0 | 1 |
| 2024/2025 | 306 | 2024-08-09 / 2025-05-17 | 2 | 0 | 0 |
| 2025/2026 | 306 | 2025-08-08 / 2026-05-16 | 3 | 0 | 0 |

All 2,448 observations retain source day/heading, heading physical line, original fixture physical line and literal text, original score/HT/annotation, round/stage and source provenance. Explicit heading years versus season/weekday-resolved years remain distinguished. The 2019/20 July extension is narrowly recognized through the existing 2020-08-02 outer bound. No nominal round dates are substituted for actual source day headings. No actual result-publication time or model eligibility is inferred.

## Independent overlap reconciliation and conflicts

Seven overlap seasons 2018/19–2024/25 each yield 306 one-to-one diagnostic correspondences: **2,142 matched pairs, zero unmatched observations, zero score disagreements and two date disagreements**. Every season participant set and mapping is checked for completeness/bijection; duplicate targets and cross-season links fail explicitly. Original names remain distinct in both observations; frozen links are comparison hypotheses, not historical/legal continuity approval. Repository agreement is not independent corroboration.

| Fixture | Historical source date / line | Modern source date / line | Both FT | Structural finding |
|---|---|---|---|---|
| Santa Clara–Pacos Ferreira, 2019/2020 | 2020-02-01 / 7290 | 2020-02-02 / 298 | 2-1 | Both ISO days valid/in-season; interpretation unresolved |
| Santa Clara–Benfica, 2020/2021 | 2021-01-03 / 7532 | 2021-01-04 / 192 | 1-1 | Both ISO days valid/in-season; interpretation unresolved |

No additional disagreements were found. A one-day difference could concern source-date semantics or an event chronology issue; structural checks cannot choose a historical explanation or authoritative date. Both original dates/scores and all four physical bindings remain intact for Phase 5.

### Belenenses SAD–Benfica

The validator independently confirms historical line **7838** and modern 2021/22 line **187**, date **2021-11-27**, FT **0–7**; modern HT is **0–7** and annotation empty. Historical labels Belenenses/Benfica and modern Belenenses SAD/SL Benfica remain unchanged.

Both observations carry KNOWN_ABANDONMENT_REQUIRES_REVIEW. Source score, reported termination, officially recognized result, administrative decision/finality, actual completion and effective availability are separate. Actual completion/finality/availability are null in the review queue. Matching source scores do not settle those questions. No historical documents were researched and no completed-result/HOLD OUT/NOT PLAYED decision was made. Existing Phase 1–3 documentary leads remain in frozen evidence.

## All scheduling contexts and deduplicated review queue

| Season | Round | First source day | Last source day | Span days | Members |
|---|---|---|---|---:|---:|
| 2019/2020 | 1 | 2019-08-09 | 2019-09-08 | 30 | 9 |
| 2019/2020 | 9 | 2019-10-05 | 2019-10-31 | 26 | 9 |
| 2020/2021 | 1 | 2020-09-18 | 2020-10-28 | 40 | 9 |
| 2020/2021 | 12 | 2021-01-02 | 2021-01-21 | 19 | 9 |
| 2020/2021 | 14 | 2021-01-15 | 2021-02-17 | 33 | 9 |
| 2020/2021 | 7 | 2020-11-06 | 2020-12-01 | 25 | 9 |
| 2021/2022 | 13 | 2021-12-03 | 2022-01-03 | 31 | 9 |
| 2021/2022 | 16 | 2021-12-28 | 2022-01-13 | 16 | 9 |
| 2022/2023 | 14 | 2022-12-23 | 2023-02-09 | 48 | 9 |
| 2022/2023 | 20 | 2023-01-26 | 2023-02-13 | 18 | 9 |
| 2022/2023 | 25 | 2023-03-17 | 2023-04-05 | 19 | 9 |
| 2023/2024 | 20 | 2024-02-03 | 2024-04-16 | 73 | 9 |
| 2023/2024 | 3 | 2023-08-25 | 2023-09-09 | 15 | 9 |
| 2024/2025 | 24 | 2025-03-01 | 2025-03-28 | 27 | 9 |
| 2024/2025 | 8 | 2024-10-04 | 2024-12-19 | 76 | 9 |
| 2025/2026 | 1 | 2025-08-08 | 2025-09-23 | 46 | 9 |
| 2025/2026 | 16 | 2025-12-27 | 2026-01-11 | 15 | 9 |
| 2025/2026 | 26 | 2026-03-14 | 2026-04-29 | 46 | 9 |

The 18 wide-round contexts bind 162 distinct modern observations. Thirteen source-order reversal pairs have 26 distinct endpoints. There are eight modern and 18 historical unusual-score observations. These are source-observation counts; overlap representations and review categories must not be counted as separate real-world fixtures. All Phase 3 category memberships reconcile exactly.

| Category | Source-observation memberships |
|---|---:|
| KNOWN_ABANDONMENT_REQUIRES_REVIEW | 2 |
| SOURCE_DISAGREEMENT | 4 |
| SOURCE_FIELD_OR_LABEL | 1 |
| SOURCE_ORDER_REVERSAL | 26 |
| UNUSUAL_SCORE | 26 |
| WIDE_ROUND | 162 |

There are **207 distinct flagged observations**, versus 221 category memberships. Every queue entry retains the complete original observation, every reason, provenance/line/hash, related overlap audit IDs, source season/round and separate unknown actual completion, administrative finality and result availability. A reversal refers to physical file order; a long round may reflect legitimate rescheduling. Neither implies an incorrect result or automatic exclusion.

## Identity boundaries and evidence limits

The complete per-source participant sets remain available in both assessments and the private identity review. No reserve labels or NFC/casefold collisions were found in actual top-flight records. Only the Feirense occurrence produces a whitespace-collision diagnostic. Original accents, punctuation and abbreviations remain preserved.

Belenenses versus Belenenses SAD/B-SAD, Benfica/Porto/Sporting senior versus B sides, Vitória SC/Guimarães versus Vitória FC/Setúbal and AVS versus Aves must remain distinct until explicit evidence supports a narrowly scoped link. Gil Vicente, Boavista and União de Leiria/historical entity continuity are later historical-review questions; promotion, bankruptcy, points deductions or disciplinary standings changes do not automatically modify full-time scores. All 126 season-local overlap label links remain diagnostic only.

## Four-season source gap and RSSSF separation

| Season | Approved dated observations | Expected slots | Status |
|---|---:|---:|---|
| 1990/1991 | 0 | 380 | Missing approved dated source |
| 1991/1992 | 0 | 306 | Missing approved dated source |
| 1992/1993 | 0 | 306 | Missing approved dated source |
| 1993/1994 | 0 | 306 | Missing approved dated source |

The unchanged RSSSF snapshot has 380 reconstructed 1990/91 result identities and zero dates. It remains outside the 11,406 dated observations and conditional 9,264 distinct sourced fixtures. Source hashes and previous capability assessment are preserved; no additional page or historical source was accessed. The full 36-season expectation remains **10,562**, with **1,298 early expected slots lacking an approved dated source**. They are not NOT PLAYED, accepted, held out or proven exclusions.

## Reproducibility and tests

Six outputs regenerate in a separate fresh process into safe temporary storage; all bytes and SHA-256 match saved artifacts:

| Output | SHA-256 |
|---|---|
| phase4_historical_structure.json | `e08081b19e87331faf88e4488f979d8fa5d9ad2fc6af9dbce1305ab42b9f295a` |
| phase4_modern_structure.json | `6bcf358bc3560e561c14bdcec8a0ec6571abd65a7e03a5aa8af217d760c74172` |
| phase4_overlap_reconciliation.json | `fdf8fbb644742fc35251885dc0bafde4d8dbf5cdf8c51148b1326d7ccfcfe56b` |
| phase4_review_queue.json | `70d5a89241a877428534b068179b67af1b6d7896f654a8179fe4f47880cc0be8` |
| phase4_coverage_gap.json | `863f4094faa37a01c7fae6bebcb558da1f895ab18dee7b718702bc0380c775e0` |
| phase4_integrity_manifest.json | `4b37c23bff45aebf67b62031b02afef6adc6461ddfbb810ebfb1245942362ee7` |

The reproducibility verifier also independently reruns the earlier complete-source inventory/reconciliation unchanged, rechecks all **11,406 physical source-line bindings** against original bytes, recomputes pairing populations and confirms exact review-category equality. All 96 then-existing non-test-log private artifacts remain unchanged. The integrity manifest binds all ten original hashes/revisions/sizes and the five main structural outputs. Earlier evidence remains frozen.

Reproduction (no acquisition):

```sh
PYTHONPATH=src:. python -B scripts/validate_primeira_liga_structure.py --init
PYTHONPATH=src:. python -B scripts/validate_primeira_liga_structure.py
PYTHONPATH=src:. python -B scripts/validate_primeira_liga_structure.py --output-directory /path/to/safe/temporary-directory
```

`--init` creates a baseline only once; existing baselines and output bytes are verified and never silently replaced. Fresh runs used the unchanged external Python 3.13.12 environment, bounded timeouts, project bytecode/pytest cache disabled and safe temporary pytest directories; no install or original .venv modification.

| Fresh selection | Passed | Failures / errors / skips |
|---|---:|---|
| New structural tests | 52 | 0 / 0 / 0 |
| All Primeira Liga tests | 141 | 0 / 0 / 0 |
| Acquisition/importer selection | 707 | 0 / 0 / 0 |
| Non-UI | 1,980 | 0 / 0 / 0 |
| App/launcher | 7 | 0 / 0 / 0 |
| Full repository | 1,987 | 0 / 0 / 0 |

Selections overlap and are not additive. Synthetic tests cover season formats, physical provenance, exact schema, date/goal/derived-field validation, source-label preservation, source grammar, HT/FT consistency, rounds/participant integrity, other stages, score/scheduling nonexclusion, bijective season-bound overlap, Feirense isolation and frozen-evidence tampering.

## Changed files and protection

New public files: scripts/validate_primeira_liga_structure.py, tests/test_primeira_liga_structure.py and this report. PLANNING_LOG.md receives append-only measured decisions. Private additions: phase4_protected_before.json, six named structural outputs, phase4_reproducibility.json, verification_phase4 logs/XML/status, test summary and final verification receipt. All previous Phase 2–3 files remain unchanged.

All eleven earlier competitions, their 127,927 screened records, ten source originals and frozen evidence pass protected checks. Private files remain Git-ignored and untracked; no credentials or raw private data are included in public changes. HEAD/index and prediction application are unchanged, the promotional worktree is untouched, and nothing is staged.

## Prioritized proposed Phase 5 agenda — approval required

1. Verify actual event/completion/source-date semantics for the two exact Santa Clara date conflicts, using official or authoritative contemporary evidence; preserve both originals until an explicit later policy decision.
2. Inspect permitted official evidence for Belenenses SAD–Benfica 2021-11-27: interruption, recognized result, administrative decision/finality and defensible availability. Distinguish directly inspected documents from index-only leads.
3. Corroborate the exact Feirense source identity/whitespace context; defer any normalization decision to separately approved Phase 6.
4. Review all 18 wide rounds and 13 reversal contexts, prioritizing diagnostic date endpoints and exceptional events; do not certify every member from a round-level explanation.
5. Review unusual-score and administrative/identity candidates, without double-counting overlapping source representations. Preserve Gil Vicente/Boavista history, senior/B and Belenenses/AVS entity boundaries.
6. Propose reproducible ordinary sampling covering all 32 represented seasons, selected before research. Record source independence, exact evidence, date/result corroboration, limitations and unresolved status; structural completeness must not become historical certification.

Separate future request: bounded, permission-aware dated-source discovery for 1990/91–1993/94; no early source acquisition or research was performed or approved in Phase 4. RSSSF results may corroborate scores but cannot supply dates.

Technical completeness, historical truth, administrative finality, actual availability, source independence, permitted acquisition, redistribution and model training remain separate. README noncommercial/GPL metadata, OpenFootball CC0 and RSSSF copying conditions do not establish blanket upstream/training clearance. No models, prediction eligibility policies or application integration are authorized.

Stop after Phase 4 and await approval. No Phase 5 research, processing decisions, source acquisition, standardized data, staging, commit, push, merge or rebase occurred.
