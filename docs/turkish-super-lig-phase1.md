# Turkish Süper Lig — Phase 1/5 final source assessment

**PASS with an isolated source-date quarantine.** Updated 2026-11-26 following the owner's explicit source-recovery authorization. Competition #14; target 1990/91–2025/26; baseline HEAD `b59b274b3177a34ffe7adfe993ae3f54be5a5f15`. Phase 2 has not started.

The initial BLOCKED assessment is superseded by demonstrated containment under the revised [five-phase workflow](accelerated-five-phase-workflow.md). Its originals, receipts, diagnostic/stop records and timing remain immutable under `data/private/turkey/super_lig/phase1/`; the earlier public report is preserved byte-for-byte in `phase1_followup/pre_followup/`. New detailed evidence and metadata remain private under `data/private/turkey/super_lig/phase1_followup/`.

## Root cause and exact disposition of the source issue

All **153** affected physical records were inspected with all 12 original fields, source/record hashes and line locators. The original CSV itself contains the anomalous ISO dates: this is not an error introduced by the local parser. First comparison against all **23 already-acquired originals** found no independent 2006/07 fixture list and no exact date/team/score duplicate in another historical row. There are **15** same-pair/score coincidences in 2005/06, on different dates; the supplementary RSSSF 2005/06 document also shows those coincidences. They are insufficient to reassign a season.

Targeted comparison establishes that all **153** rows correspond to unique **2006/07** directed fixtures and scores in both the direct upstream CSV and [RSSSF's 2006/07 account](https://www.rsssf.org/tablest/tur07.html). All 306 season pairings/scores agree across the three representations; the other 153 rows also agree on exact dates. In the affected half, every engsoccerdata date is precisely one year earlier than the direct upstream date. This bounds the observed source-file year corruption; the historical code operation that introduced it is not proven.

| Outcome | Records | Derived treatment |
|---|---:|---|
| Season, participants and score corroborated as 2006/07 | 153 | No reassignment to 2005/06 |
| Exact date agrees in upstream and separately compiled RSSSF | 143 | Source-specific derived date correction, bound to file/record hashes and both evidence locators |
| Exact dates disagree by one day between comparison sources | 10 | Quarantine every compared representation; no chosen date or silent fallback |
| Other half of 2006/07, dates/scores agree | 153 | Original fields retained |

**No original was corrected. No scores or club identities were changed.** The correction registry is derived metadata, not a canonical dataset or historical INCLUDE decision. It contains a separately recorded award/abandonment annotation that still requires later historical review; date recovery does not certify ordinary competitive play or accept an administrative result.

The quarantine leaves **296 usable source candidates** for 2006/07. `source_candidates` applies the same season-bound quarantine to upstream and RSSSF alternatives; loading another representation cannot restore the ten unresolved fixtures. `apply_metadata` checks the whole-source digest, original fields and physical-record hashes before applying any correction. Unsupported corrections, missing bindings or expanded discrepancies fail checks.

## Sources, provenance and permissions

There are now **26 unique network-acquired originals**, **1,441,747 bytes**: the original 23 plus exactly these three. Copies of retained permission/tree metadata are not counted again.

| New original | Bytes | SHA-256 |
|---|---:|---|
| [RSSSF 2005/06](https://www.rsssf.org/tablest/tur06.html) | 50,164 | `521e9c7283d0d2d56a0beb456dd514a0ff9a369fc56ae8001d89134fcb6b2b59` |
| [RSSSF 2006/07](https://www.rsssf.org/tablest/tur07.html) | 94,652 | `6949de9ddf9fe294c98319147daac6c0d391e58fd74614187f0592af3d13ef38` |
| [Football-Data 2006/07](https://football-data.co.uk/mmz4281/0607/T1.csv) | 73,061 | `3208f9e8171e0d3c91e9168a0076d73368e825f9de41ae836c3daede3e01322c` |

They were retrieved on 2026-11-26 at 13:33:50, 13:33:51 and 13:33:52 UTC respectively; exact fractional timestamps, original bytes, response metadata, URLs and attribution remain in immutable receipts. RSSSF page-specific copying grants were inspected before acquisition: attribute Erdinç Sivritepe/Jan Schoenmakers for 2005/06 and Erdinç Sivritepe/Sener Yelkenci for 2006/07, with RSSSF and retained acknowledgements. ISO-8859-2 declarations and HTML entities are handled explicitly for these comparisons.

The original engsoccerdata CSV remains SHA-256 `cb1d8d58a99213d4b6bcb44a54f5f0f4de0127771171e7969043b59837993a54`, pinned at `872c5c354161ace8408f3091b758c6af4cccca94`. OpenFootball remains pinned at `63df627f3c87ce71708f016522ea236cf74332c3`. All original 23 hashes/receipts remain valid.

[Football-Data fair use](https://football-data.co.uk/contact.php) permits personal/academic research with limited light automated download and excludes commercial/AI training use. This follow-up acquired one scoped CSV, the second direct fixture CSV counting the initial 2025/26 request; no further Football-Data acquisition was performed. Engsoccerdata's noncommercial attribution grant, OpenFootball's CC0 for rights held and RSSSF's page grants do not resolve every upstream right or authorize model training/redistribution. All original data, odds, detailed evidence and audits remain private.

Football-Data and engsoccerdata are upstream/derivative, not independent votes. RSSSF is a separately attributed compilation with its own fixture headings and ten differing dates; its fully independent upstream lineage is not established. This is separate documentary corroboration with explicit limits, not a guarantee that every historical fact has been independently proven. A [TFF disciplinary notice](https://www.tff.org/default.aspx?ftxtID=525&pageID=246) was inspected on the web for primary date context in several examples; it was neither acquired nor used to override any quarantine. The earlier TFF encoding stop was not retried. Mackolik and legacy archive restrictions/leads remain unchanged.

## Updated 36-season coverage matrix

H raw/usable = historical CSV raw rows versus source candidates after this repair/quarantine; O = OpenFootball scored/total fixture descriptions; F = separately acquired direct 2025/26 CSV rows. These are **source feasibility counts, not accepted final dataset counts**. Overlapping sources are not added as distinct fixtures. “Usable” means the Phase 1 source checks pass with explicit metadata; structural completeness, historical finality and stage eligibility still require later phases.

| Season | H raw/usable | O scored/total | F | Limit or overlap |
|---|---:|---:|---:|---|
| 1990/91 | — | — | — | Exact-date gap; RSSSF table only |
| 1991/92 | — | — | — | Exact-date gap; RSSSF table only |
| 1992/93 | — | — | — | Round/date-range evidence; exact fixture dates unconfirmed |
| 1993/94 | — | — | — | Undated result grid; exact-date gap |
| 1994/95 | 306/306 | — | — | Source coverage, not historical certification |
| 1995/96 | 306/306 | — | — | Source coverage, not historical certification |
| 1996/97 | 306/306 | — | — | Source coverage, not historical certification |
| 1997/98 | 306/306 | — | — | Source coverage, not historical certification |
| 1998/99 | 306/306 | — | — | Source coverage, not historical certification |
| 1999/00 | 306/306 | — | — | Source coverage, not historical certification |
| 2000/01 | 306/306 | — | — | Source coverage, not historical certification |
| 2001/02 | 306/306 | — | — | Source coverage, not historical certification |
| 2002/03 | 306/306 | — | — | Source coverage, not historical certification |
| 2003/04 | 306/306 | — | — | Source coverage, not historical certification |
| 2004/05 | 306/306 | — | — | Source coverage, not historical certification |
| 2005/06 | 306/306 | — | — | Supplementary RSSSF comparison, not complete reconstruction |
| 2006/07 | 306/296 | — | — | 143 corrected dates; 10 quarantined; two additional overlapping sources |
| 2007/08 | 306/306 | — | — | Source coverage, not historical certification |
| 2008/09 | 306/306 | — | — | Source coverage, not historical certification |
| 2009/10 | 272/272 | — | — | 272 source rows; omissions/administrative context unresolved |
| 2010/11 | 306/306 | — | — | Source coverage, not historical certification |
| 2011/12 | 306/306 | — | — | Historical source excludes playoffs |
| 2012/13 | 306/306 | — | — | Source coverage, not historical certification |
| 2013/14 | 306/306 | — | — | Source coverage, not historical certification |
| 2014/15 | 306/306 | — | — | Source coverage, not historical certification |
| 2015/16 | 306/306 | — | — | Source coverage, not historical certification |
| 2016/17 | 306/306 | — | — | Source coverage, not historical certification |
| 2017/18 | 306/306 | — | — | Source coverage, not historical certification |
| 2018/19 | 306/306 | 306/306 | — | H/O overlap |
| 2019/20 | 306/306 | 306/306 | — | COVID finish through 2020-07-26 |
| 2020/21 | 420/420 | 420/420 | — | 21-team format era; H/O overlap |
| 2021/22 | 380/380 | — | — | 20-team format era |
| 2022/23 | 342/342 | — | — | Earthquake withdrawals/administrative awards require review |
| 2023/24 | 380/380 | 380/380 | — | 20-team format era; H/O overlap |
| 2024/25 | 342/342 | 338/342 | — | 19-team era; four O unscored slots; award annotation |
| 2025/26 | — | 99/306 | 306 | O partial snapshot; F through 2026-05-17,18-team era |

The historical CSV has **9,786 raw / 9,776 source-usable rows** over 31 seasons, 1994/95–2024/25. The direct 2025/26 CSV supplies **306** further season-disjoint source candidates, giving **32 represented target seasons**. Four early seasons remain gaps in acquired exact-date coverage; this does not mean fixtures did not occur. RSSSF date ranges and undated grids never become invented dates.

Football-Data advertises 1994/95 onward, but only 2006/07 and 2025/26 were directly acquired. TFF's web-inspected catalogue lists the target seasons; actual full fixture coverage and bulk preservation permission remain unverified. The OpenFootball 2025/26 snapshot has 99 scored/207 unscored descriptions; the direct CSV has 306 rows through May 2026. Do not label that older snapshot as the complete season or call 2025/26 the ongoing season on this review date. No 2026/27 fixtures were acquired.

Remaining risks: historical “1. Lig” versus the modern second-tier name; changing team counts and stage formats; 2009/10 omissions; incomplete 2011/12 postseason coverage; administrative awards, interruptions and withdrawals; Turkish diacritics, sponsor labels, city/club identity boundaries; source dependence and rights. The 2005/06 comparison parser retains abandonment/replay narrative and an unbound spelling separately rather than inventing a club/date or certifying full documentary coverage. None of these contained limitations fails Phase 1.

## Verification, reproducibility and preservation

Reusable acquisition/hash/blob/overwrite/fixture utilities remain in use. Minimal Turkish additions are the source-recovery adapter and targeted tests; no shared importer, application, prediction logic or completed competition was changed. The adapters explicitly handle the new CSV's BOM, bounded empty padding and one source-labelled abandonment annex, preserving every annex value. A Turkish COVID window is configured rather than weakening date validation globally.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -p 'test_turkish_super_lig*.py' -v
PYTHONDONTWRITEBYTECODE=1 python3 -B -m scripts.recover_turkish_super_lig_sources --verify
PYTHONDONTWRITEBYTECODE=1 python3 -B data/private/turkey/super_lig/phase1_followup/execution/verify_recovery.py
```

**24 focused tests passed**, including the original 12 acquisition safeguards and 12 recovery checks. New checks reject unsupported corrections, altered file/record bindings, score conflicts, ambiguous pairings, expanded uncontained defects and quarantine fallback; test explicit source annotations, BOM, date windows and all three issue classes. Intermediate adapter failures exposed the original CSV annex and BOM and were addressed with bounded rules and tests, not changes to originals. No full-suite run, installs or original-environment execution occurred.

The independent audit imports no production recovery parser, mapper or serializer. It independently parses all 306 scoped fixtures and infers **18 injective coeval team correspondences** using first-half date/score intersections, reproducing **153 season/score correspondences, 143 corrected dates and 10 quarantines**. This is a targeted source-recovery audit, not the later full independent structural or canonical reconstruction.

All **26 originals** verify offline with zero requests. A separate process and fresh temporary directory regenerate the three artifacts byte-for-byte/SHA-identically. Deterministic content excludes runtime timings. Private `verification.json` records artifact hashes, commands, results and scope; `execution/verify_recovery.py` can repeat those checks without overwriting the receipt.

Preservation accounts for **1,913 baseline entries**: **1,907 protected files remain byte-identical**, while six explicitly editable public entries are accounted for by preserved preimages (and the planning log's unchanged prefix). This includes **all 1,622 prior private files** and all 13 completed competitions, earlier Turkish originals/audits/stop records, unrelated work, Git index and environment configuration. Authorized current documentation/source-adapter edits are distinguished from unchanged protected files. Installed-package bytes were not exhaustively fingerprinted; no such certificate is claimed. HEAD remains `b59b274b3177a34ffe7adfe993ae3f54be5a5f15`; nothing was staged, committed or pushed. Final timing and release-of-blocker checkpoint follow below.

## Phase 2 recommendation — pending approval

Use the frozen source hash manifest and recovery registry; apply its 143 exact record-bound date corrections and all-source quarantine for the ten unresolved fixtures. Never feed the original uncorrected dates directly into downstream processing or use upstream alternatives to undo quarantine. Inventory all acquired representations with physical spans, reconcile overlaps without double counting, check season/format/stage accounting, and implement a separate raw structural checker. Keep four early gaps and 2011/12/2009/10 limitations explicit; research material award/interruption cases in the later historical phase. Preserve original football dates and accepted final results for retrospective internal diagnostics, without administrative-publication-date filtering.

**Phase 1 PASS does not authorize Phase 2, historical inclusion decisions or standardized records. STOP for explicit owner approval.**

## Final checkpoint and measured execution time

**Phase 1 final status: PASS with ten isolated quarantines.** Final review reconfirmed all 26 source originals/receipts and three deterministic artifact hashes offline, with no network requests. The saved independent checker repeated successfully after documentation updates. All prior private artifacts, frozen decisions, protected code/application files, Git history/index and original environment configuration remain preserved. Final public whitespace/syntax/privacy checks and the 36-season matrix check passed. No standardized records, Phase 2 work, staging, commit or push occurred.

Recovery artifact SHA-256 values: registry `a7c16963e3f880021cc264188da9278ad0e8e0582d8f279ebe2afd3d94c7b5b9`; feasibility `0417a608c9bf67971dce87bd6182ba4cc112fcb4148e59aa871cd01b0741c831`; source manifest `405fcd37f2fdfb946479850678aef170cf913e67133864308a49733feb2f06a5`. Private `final_status.json` explicitly supersedes the earlier blocker under the owner's authorization; it does not delete or rewrite that historical diagnostic.

Measured follow-up execution: **16 min 38 sec**, from `2026-11-26T13:32:06+00:00` to audit checkpoint `2026-11-26T13:48:44.371398+00:00`. Active wall **998.4 s**, within-follow-up approval wait **0 s**, elapsed **998.4 s**; failed adapter diagnostics, source research, tests and reporting are included. Monotonic timing is reconciled with the initial UTC interval; pre-observation time and final chat rendering are excluded. The three successful request durations sum to **0.76 s**, already included in wall time. The prior attempt measured 13 min 53 sec; combined active execution through this checkpoint is **30 min 32 sec**. The **215.8 s** inter-attempt gap is excluded from active totals and is not asserted to be an exact human approval-wait measurement. Private timing JSON and append-only ledger retain the readings. No speedup percentage is claimed.

**STOP. Await explicit approval before Phase 2.**
