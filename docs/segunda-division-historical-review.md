# Segunda División — Phase 5 historical evidence review

Reviewed 2026-11-22. Branch `feature/data-collection`; unchanged HEAD `052d25185182f1edbb80fac51cafbb59e0acf7cf`. Phase 5 only: evidence gathering and reproducible accounting, with no correction, exclusion, standardized export or eligibility decision. All earlier uncommitted Phase 2–4 work is retained.

## Classification and measured scope

The acquired population remains **6,006 observations**, including **5,997 score-bearing observations and nine original missing scores**. The frozen Phase 4 queue still contains **773 distinct observations**. The evidence ledger has **79 individually investigated fixtures: 25 VERIFIED, 33 PARTIAL, 21 UNRESOLVED**. VERIFIED means directly inspected independent-authority or authored evidence supports participants, playing/completion date and full-time score; it does not certify legal finality, absence of every possible appeal, dataset-wide correctness, training eligibility or licensing.

The 79 are the deduplicated union of nine incomplete fixtures, 21 awards, 30 diagnostic outliers (including both known exceptional 2019/20 fixtures), two unusual-score fixtures, 13 ordinary samples and four additional earlier fixtures responsible for source-order reversals. These categories do not overlap except the two known exceptions within the outliers. Of the four extra reversal fixtures, Huesca–Barcelona B already belongs to the reserve queue. The review matrix therefore covers 789 unique observations: the original 773, 13 ordinary samples and three other reversal fixtures. **710 matrix observations were not individually full-fact reviewed**; grouped identity/context research must not be counted as individual match certification.

All **23 scheduling contexts / 253 affected observations**, all **30 diagnostic outliers**, all **17 source-order reversals** and all **six reserve groups / 498 affected observations** are accounted for. Scheduling classifications are **11 DOCUMENTED, 12 PARTIAL, zero wholly unsupported contexts**. Documentary scheduling support is narrower than proof of the played date or score. Outlier fixture classifications are three VERIFIED and 27 PARTIAL. The private ledger contains 64 documentary references: 43 directly opened and 21 index-only. Failed opens and a rewritten summary remain index-only; no bypass or bulk scraping was used.

Official match cards are authoritative corroboration separate from the OpenFootball export, but their commercial data-provider independence is not established. Authored club/league narratives, RFEF decisions and contemporary reports provide stronger documentary separation. Syndicated EFE/agency copies and a league widget embedded in a preview are not counted as separate independent witnesses. The scripts check evidence consistency, not internet truth; human transcription and source access limitations remain explicit.

## Nine original missing-score observations

All nine have separately corroborated final scores and dates. No source FT, goals, date or name has been filled or replaced. Physical lines below refer to pinned `openfootball/espana/2024-25/2-liga2.txt`, revision `80035a93dd4920985af52aa097a54a6fb888563b`. Full audit identifiers, raw lines and source hashes are retained in the ignored ledger. Eight rows were directly inspected on the official round page; Córdoba–Albacete uses an authored contemporary report. No exceptional scheduling was established for these nine by the inspected documents.

| Line | Playing date corroborated | Fixture | Original FT | Independent FT | Finding | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| 745 | 2025-05-31 | Málaga CF — Burgos CF | missing | 2-2 | VERIFIED | [missing42](#evidence-missing42) |
| 747 | 2025-06-01 | SD Huesca — CD Eldense | missing | 3-2 | VERIFIED | [missing42](#evidence-missing42) |
| 748 | 2025-06-01 | UD Almería — CD Tenerife | missing | 2-0 | VERIFIED | [missing42](#evidence-missing42) |
| 749 | 2025-06-01 | FC Cartagena — CD Mirandés | missing | 1-3 | VERIFIED | [missing42](#evidence-missing42) |
| 750 | 2025-06-01 | Deportivo La Coruña — Elche CF | missing | 0-4 | VERIFIED | [missing42](#evidence-missing42) |
| 751 | 2025-06-01 | Real Oviedo — Cádiz CF | missing | 2-1 | VERIFIED | [missing42](#evidence-missing42) |
| 752 | 2025-06-01 | Levante UD — SD Eibar | missing | 1-0 | VERIFIED | [missing42](#evidence-missing42) |
| 753 | 2025-06-01 | Racing Santander — Granada CF | missing | 2-1 | VERIFIED | [missing42](#evidence-missing42) |
| 754 | 2025-06-01 | Córdoba CF — Albacete | missing | 1-1 | VERIFIED | [cordoba](#evidence-cordoba) |

These are candidate additions for an explicitly approved later metadata/transformation policy, not an acquisition of a replacement season file. The nine original blanks remain a technical completeness limitation.

## Reus: all 21 source-marked administrative awards

LaLiga documents the January 18 interim suspension and January 28 expulsion ([reus_suspend](#evidence-reus_suspend), [reus_expulsion](#evidence-reus_expulsion)). Contemporary reporting describes one-goal second-half losses and three awards reflected by February 7 ([reus_awards](#evidence-reus_awards)). That is not an inspected operative fixture-award decision. Later legal reporting supports the expulsion appeal history, but not individual result finality or earliest availability ([reus_court](#evidence-reus_court), [reus_tad](#evidence-reus_tad)).

Every fixture below is **UNRESOLVED for individual official award/finality and result availability**. Source dates are scheduled-date proxies, not certified decision or knowledge dates. No played score is certified; all 21 remain visibly source-marked awards. January 28 is the expulsion decision, not an assigned award date. For the first three, February 7 is a secondary-reporting upper bound for reported allocation, not the earliest knowledge or appeal-finality date. For the remaining 18, even that fixture-specific bound is absent. No result is accepted for predictive modeling.

| Round | Line | Source date proxy | Fixture | Source award | Reported allocation by | Finality / earliest availability |
| --- | --- | --- | --- | --- | --- | --- |
| 22 | 376 | 2019-01-19 | CF Reus Deportiu — UD Las Palmas | 0-1 | 2019-02-07 (reported) | UNRESOLVED |
| 23 | 401 | 2019-01-27 | Albacete — CF Reus Deportiu | 1-0 | 2019-02-07 (reported) | UNRESOLVED |
| 24 | 419 | 2019-02-03 | CF Reus Deportiu — Elche CF | 0-1 | 2019-02-07 (reported) | UNRESOLVED |
| 25 | 430 | 2019-02-09 | Gimnàstic de Tarragona — CF Reus Deportiu | 1-0 | Not established | UNRESOLVED |
| 26 | 453 | 2019-02-17 | CF Reus Deportiu — UD Almería | 0-1 | Not established | UNRESOLVED |
| 27 | 469 | 2019-02-24 | Granada CF — CF Reus Deportiu | 1-0 | Not established | UNRESOLVED |
| 28 | 483 | 2019-03-03 | CF Reus Deportiu — CD Tenerife | 0-1 | Not established | UNRESOLVED |
| 29 | 501 | 2019-03-10 | CD Lugo — CF Reus Deportiu | 1-0 | Not established | UNRESOLVED |
| 30 | 518 | 2019-03-17 | CF Reus Deportiu — Deportivo La Coruña | 0-1 | Not established | UNRESOLVED |
| 31 | 536 | 2019-03-24 | Extremadura UD — CF Reus Deportiu | 1-0 | Not established | UNRESOLVED |
| 32 | 554 | 2019-03-31 | CF Reus Deportiu — Cádiz CF | 0-1 | Not established | UNRESOLVED |
| 33 | 573 | 2019-04-07 | RCD Mallorca — CF Reus Deportiu | 1-0 | Not established | UNRESOLVED |
| 34 | 591 | 2019-04-14 | CF Reus Deportiu — Real Oviedo | 0-1 | Not established | UNRESOLVED |
| 35 | 608 | 2019-04-21 | Real Zaragoza — CF Reus Deportiu | 1-0 | Not established | UNRESOLVED |
| 36 | 626 | 2019-04-28 | CF Reus Deportiu — AD Alcorcón | 0-1 | Not established | UNRESOLVED |
| 37 | 641 | 2019-05-05 | Córdoba CF — CF Reus Deportiu | 1-0 | Not established | UNRESOLVED |
| 38 | 660 | 2019-05-12 | CA Osasuna — CF Reus Deportiu | 1-0 | Not established | UNRESOLVED |
| 39 | 676 | 2019-05-19 | CF Reus Deportiu — Málaga CF | 0-1 | Not established | UNRESOLVED |
| 40 | 695 | 2019-05-26 | CD Numancia — CF Reus Deportiu | 1-0 | Not established | UNRESOLVED |
| 41 | 711 | 2019-06-02 | CF Reus Deportiu — Sporting Gijón | 0-1 | Not established | UNRESOLVED |
| 42 | 733 | 2019-06-09 | Rayo Majadahonda — CF Reus Deportiu | 1-0 | Not established | UNRESOLVED |

All individual operative decision, publication, appeal-finality, final recognized score and earliest final-result availability fields remain null in `administrative_review`. No automatic use of the scheduled date is proposed. Later lower-division Reus decisions must not be confused with professional 2018/19 expulsion proceedings.

## Interruptions, postponements and chronological integrity

**Rayo–Albacete**, 2019/20, line 346: RFEF appeal expediente 276-2019/20 establishes kickoff and suspension before the second half on **2019-12-15**. The June 3 RFEF notice schedules the second half for June 10; the directly inspected Rayo account establishes completion and **1–0 on 2020-06-10**. The source already records the completion date. The final score could not be known on the December kickoff date. Evidence: [rayo_appeal](#evidence-rayo_appeal), [rayo_schedule](#evidence-rayo_schedule), [rayo_result](#evidence-rayo_result).

**Deportivo–Fuenlabrada**, 2019/20, line 722: the August 4 RFEF resolution distinguishes the original **2020-07-20** suspension, intermediate August 5 plan and August 7 rearrangement. Contemporary RTVE reporting establishes the actual **2020-08-07, 2–1** played outcome. July 20 was not a partially played first half. The scheduling resolution explicitly warned that disciplinary proceedings could affect the result. Later directly read secondary legal reports describe jurisdictional closure on August 27 and TAD rejection dated November 20, reported December 5; the underlying final ruling/service dates were not inspected. The played facts are VERIFIED; ultimate administrative finality is PARTIAL. No earlier final-result date or legal-finality date is assigned. Evidence: [dep_schedule](#evidence-dep_schedule), [dep_result](#evidence-dep_result), [dep_archive](#evidence-dep_archive), [dep_tad](#evidence-dep_tad).

Dates in the ledger are evidence fields only. `result_known_by` for these two refers to the played outcome by the completion day, not an exact timestamp or proof of ultimate legal finality. The eventual Phase 6 policy must distinguish known played results from later administrative changes, keep original kickoff/scheduled/completion dates, and require strictly prior available results in chronological evaluation. No effective standardized dates are generated here.

### All 23 wide-round contexts

| Season | Round | Observed date span | Diagnostic outlier fixtures | Context status | Evidence |
| --- | --- | --- | --- | --- | --- |
| 2014/2015 | 24 | 2015-02-07 → 2015-03-18 | 2015-03-18 CD Alavés–CA Osasuna | DOCUMENTED | [o14](#evidence-o14) |
| 2015/2016 | 27 | 2016-02-27 → 2016-03-16 | 2016-03-16 SD Huesca–RCD Mallorca | PARTIAL | [o15](#evidence-o15) |
| 2016/2017 | 16 | 2016-11-25 → 2016-12-14 | 2016-12-14 Levante UD–Rayo Vallecano | PARTIAL | [o16a](#evidence-o16a) |
| 2016/2017 | 19 | 2016-12-16 → 2017-01-11 | 2017-01-11 UCAM Murcia CF–Levante UD | PARTIAL | [o16b](#evidence-o16b) |
| 2017/2018 | 7 | 2017-09-29 → 2017-11-01 | 2017-11-01 Gimnàstic de Tarragona–FC Barcelona B | PARTIAL | [o17a](#evidence-o17a) |
| 2017/2018 | 17 | 2017-12-02 → 2018-01-18 | 2018-01-18 CA Osasuna–Gimnàstic de Tarragona | PARTIAL | [o17b](#evidence-o17b) |
| 2019/2020 | 6 | 2019-09-17 → 2019-10-16 | 2019-10-16 CF Fuenlabrada–Real Zaragoza | PARTIAL | [o19a](#evidence-o19a) |
| 2019/2020 | 20 | 2019-12-13 → 2020-06-10 | 2020-06-10 Rayo Vallecano–Albacete | DOCUMENTED | [rayo_appeal](#evidence-rayo_appeal), [rayo_result](#evidence-rayo_result), [rayo_schedule](#evidence-rayo_schedule) |
| 2019/2020 | 24 | 2020-01-17 → 2020-02-19 | 2020-02-19 CD Mirandés–Real Zaragoza | PARTIAL | [o19b](#evidence-o19b) |
| 2019/2020 | 42 | 2020-07-20 → 2020-08-07 | 2020-08-07 Deportivo La Coruña–CF Fuenlabrada | DOCUMENTED | [dep_result](#evidence-dep_result), [dep_schedule](#evidence-dep_schedule) |
| 2020/2021 | 1 | 2020-09-12 → 2020-11-05 | 2020-11-04 Real Zaragoza–Girona FC; 2020-11-05 CE Sabadell–UD Almería | PARTIAL | [o20a](#evidence-o20a), [o20z](#evidence-o20z) |
| 2020/2021 | 2 | 2020-09-19 → 2020-12-10 | 2020-12-09 UD Almería–Real Zaragoza; 2020-12-10 Girona FC–UD Logroñés | DOCUMENTED | [o20b](#evidence-o20b) |
| 2020/2021 | 6 | 2020-10-17 → 2020-11-05 | 2020-11-05 AD Alcorcón–SD Ponferradina | DOCUMENTED | [o20c](#evidence-o20c) |
| 2020/2021 | 7 | 2020-10-21 → 2020-12-09 | 2020-12-09 CE Sabadell–AD Alcorcón | DOCUMENTED | [o20b](#evidence-o20b) |
| 2020/2021 | 21 | 2021-01-08 → 2021-02-17 | 2021-01-19 CD Mirandés–Rayo Vallecano; 2021-01-26 AD Alcorcón–Albacete; 2021-02-17 CD Leganés–UD Almería | PARTIAL | [o21a](#evidence-o21a), [o21f](#evidence-o21f) |
| 2020/2021 | 31 | 2021-03-26 → 2021-04-14 | 2021-04-14 Rayo Vallecano–CD Mirandés | PARTIAL | [o21b](#evidence-o21b) |
| 2020/2021 | 32 | 2021-03-30 → 2021-04-21 | 2021-04-21 CD Mirandés–CD Tenerife | PARTIAL | [o21c](#evidence-o21c) |
| 2021/2022 | 21 | 2021-12-17 → 2022-01-19 | 2022-01-19 CD Lugo–UD Almería | DOCUMENTED | [o22](#evidence-o22), [o22cause](#evidence-o22cause) |
| 2023/2024 | 28 | 2024-02-23 → 2024-03-13 | 2024-03-13 Levante UD–FC Andorra | DOCUMENTED | [o24](#evidence-o24) |
| 2024/2025 | 13 | 2024-11-02 → 2024-11-27 | 2024-11-20 CD Eldense–SD Huesca; 2024-11-26 UD Almería–Córdoba CF; 2024-11-27 CD Castellón–Racing Ferrol; 2024-11-27 Levante UD–Málaga CF | DOCUMENTED | [o24almeria](#evidence-o24almeria), [o24dana](#evidence-o24dana) |
| 2024/2025 | 14 | 2024-11-08 → 2025-01-07 | 2025-01-07 CD Tenerife–Levante UD | DOCUMENTED | [o24tenerife](#evidence-o24tenerife) |
| 2024/2025 | 19 | 2024-12-13 → 2025-01-29 | 2025-01-29 CD Tenerife–Deportivo La Coruña | PARTIAL | [o24dep](#evidence-o24dep) |
| 2024/2025 | 24 | 2025-01-24 → 2025-03-05 | 2025-03-05 Racing Ferrol–Burgos CF | DOCUMENTED | [o25ferrol](#evidence-o25ferrol) |

Each round entry binds all eleven original fixture IDs and its diagnostic outliers. A DOCUMENTED context requires directly opened scheduling evidence for each outlier; it need not establish every actual completion or explain every non-outlier. PARTIAL cases include indexed rescheduling accounts, absent original notices, uninspected completion evidence or mixed evidence strength. No long span is classified as a source error or grounds for exclusion.

The Almería–Córdoba case illustrates why provisional schedules must be preserved separately: the RFEF November 6 notice gives November 27, while the November 13 report documents an approved move to **November 26**, consistent with the source. That is not a confirmed source-date discrepancy. Severe weather, delayed playoff-related starts, pandemic outbreaks and personal emergencies are used only to the extent stated by the linked evidence, not inferred from a long span.

### All 17 source-order reversals

| Season | Physical lines | Source date reversal | Earlier-stored fixture | Fixture evidence | Evidence |
| --- | --- | --- | --- | --- | --- |
| 2012/2013 | 174 → 179 | 2012-10-31 → 2012-10-26 | SD Huesca–FC Barcelona B | PARTIAL | [rev12](#evidence-rev12) |
| 2014/2015 | 249 → 254 | 2014-12-10 → 2014-12-06 | CE Sabadell–UD Las Palmas | VERIFIED | [rev14result](#evidence-rev14result), [rev14a](#evidence-rev14a) |
| 2014/2015 | 379 → 384 | 2015-02-10 → 2015-02-07 | CA Osasuna–Real Zaragoza | PARTIAL | [rev14b](#evidence-rev14b) |
| 2014/2015 | 396 → 401 | 2015-03-18 → 2015-02-14 | CD Alavés–CA Osasuna | PARTIAL | [o14](#evidence-o14) |
| 2015/2016 | 445 → 450 | 2016-03-16 → 2016-03-05 | SD Huesca–RCD Mallorca | PARTIAL | [o15](#evidence-o15) |
| 2016/2017 | 271 → 276 | 2016-12-14 → 2016-12-02 | Levante UD–Rayo Vallecano | PARTIAL | [o16a](#evidence-o16a) |
| 2016/2017 | 323 → 328 | 2017-01-11 → 2017-01-06 | UCAM Murcia CF–Levante UD | PARTIAL | [o16b](#evidence-o16b) |
| 2017/2018 | 132 → 137 | 2017-11-01 → 2017-10-07 | Gimnàstic de Tarragona–FC Barcelona B | PARTIAL | [o17a](#evidence-o17a) |
| 2017/2018 | 306 → 311 | 2018-01-18 → 2017-12-08 | CA Osasuna–Gimnàstic de Tarragona | PARTIAL | [o17b](#evidence-o17b) |
| 2017/2018 | 581 → 586 | 2018-04-12 → 2018-04-06 | SD Huesca–Albacete | PARTIAL | [rev17](#evidence-rev17) |
| 2019/2020 | 108 → 113 | 2019-10-16 → 2019-09-20 | CF Fuenlabrada–Real Zaragoza | PARTIAL | [o19a](#evidence-o19a) |
| 2019/2020 | 346 → 351 | 2020-06-10 → 2019-12-20 | Rayo Vallecano–Albacete | VERIFIED | [rayo_result](#evidence-rayo_result), [rayo_schedule](#evidence-rayo_schedule), [rayo_appeal](#evidence-rayo_appeal) |
| 2019/2020 | 416 → 421 | 2020-02-19 → 2020-01-24 | CD Mirandés–Real Zaragoza | PARTIAL | [o19b](#evidence-o19b) |
| 2024/2025 | 239 → 244 | 2024-11-27 → 2024-11-08 | Levante UD–Málaga CF | PARTIAL | [o24dana](#evidence-o24dana) |
| 2024/2025 | 258 → 263 | 2025-01-07 → 2024-11-16 | CD Tenerife–Levante UD | PARTIAL | [o24tenerife](#evidence-o24tenerife) |
| 2024/2025 | 345 → 350 | 2025-01-29 → 2024-12-17 | CD Tenerife–Deportivo La Coruña | PARTIAL | [o24dep](#evidence-o24dep) |
| 2024/2025 | 434 → 439 | 2025-03-05 → 2025-01-31 | Racing Ferrol–Burgos CF | PARTIAL | [o25ferrol](#evidence-o25ferrol) |

All 17 are verified storage-order relationships in the immutable source, not proof of a wrong date. They arise where round-grouped storage places a rearranged fixture before a subsequently listed round; four narrower rearrangements are outside the 23 wide-span contexts. Thirteen reversals involve diagnostic outliers already reviewed; four additional fixtures were investigated. Source storage order must never substitute for chronological sorting. Historical explanation/playing facts remain partial where only indexed evidence was available.

## Unusual scores

Both **Osasuna–Mallorca 6–4, 2014-09-21 (2014/15 line 82)** and **Numancia–Lugo 6–6, 2014-12-20 (line 291)** are corroborated by directly inspected dated LaLiga match narratives. Recommend retaining the legitimate results, subject to Phase 6 approval; no change applied. Evidence: [high64](#evidence-high64), [high66](#evidence-high66).

## Reserve identity groups

| Source label | Affected observations | Source seasons | Diagnostic related label | Keep distinct from | Evidence |
| --- | --- | --- | --- | --- | --- |
| Athletic Club B | 42 | 2015/2016 | Bilbao Athletic | Athletic Club | [i_bilbao](#evidence-i_bilbao) |
| FC Barcelona B | 168 | 2012/2013, 2013/2014, 2014/2015, 2017/2018 | Barça B / Barça Atlètic | FC Barcelona | [i_barca](#evidence-i_barca) |
| Real Madrid Castilla | 84 | 2012/2013, 2013/2014 | Castilla / Real Madrid B | Real Madrid | [i_castilla](#evidence-i_castilla) |
| Real Sociedad B | 42 | 2021/2022 | Sanse | Real Sociedad | [i_sanse](#evidence-i_sanse) |
| Sevilla Atlético | 84 | 2016/2017, 2017/2018 | Sevilla Atlético / Sevilla FC B | Sevilla FC | [i_sevilla](#evidence-i_sevilla) |
| Villarreal CF B | 84 | 2022/2023, 2023/2024 | Villarreal B | Villarreal CF | [i_villarreal](#evidence-i_villarreal) |

The six groups account for **498 distinct affected observations**, with no double counting. Club/league histories establish the reserve/parent distinction. FC Barcelona documents the B/Atlètic naming timeline, including the June 2022 change; this does not justify retroactive relabeling. Real Madrid directly identifies Castilla as its reserve; historical Real Madrid B rename dates and universal cross-source equivalence remain unapproved. Sevilla’s historic FC B label is likewise not a verified global mapping. Athletic Club B is a source label for the Bilbao Athletic reserve, not the parent first team. No mappings are applied, including across the previously standardized La Liga population. These are grouped identity findings, not 498 match-result certifications.

## Deterministic ordinary sample

Selection was frozen before evidence lookup. For each season, remove every Phase 4 flagged observation, rotate round bands 1–14 / 15–28 / 29–42 from 2012, and choose the minimum SHA-256 of UTF-8 `segunda-phase5-v1:` plus the full source audit ID. Source IDs bind path, original SHA-256 and physical line. All 13 selected dates test a year inferred from season window and weekday rather than an explicit year in the date heading. Clubs, results, calendar dates and source positions vary. No substitutions were made after failed searches.

| Season | Line | Date | Fixture | Source FT | Sample result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| 2012/2013 | 205 | 2012-11-04 | CD Lugo — Elche CF | 1-0 | PARTIAL | [s12](#evidence-s12) |
| 2013/2014 | 270 | 2013-12-04 | CD Lugo — AD Alcorcón | 1-2 | PARTIAL | [s13](#evidence-s13) |
| 2014/2015 | 611 | 2015-05-16 | Sporting Gijón — Racing Santander | 3-1 | VERIFIED | [s14](#evidence-s14) |
| 2015/2016 | 224 | 2015-11-21 | SD Huesca — Real Oviedo | 0-1 | VERIFIED | [s15](#evidence-s15) |
| 2016/2017 | 302 | 2016-12-11 | CD Lugo — CD Numancia | 3-1 | VERIFIED | [s16](#evidence-s16) |
| 2017/2018 | 729 | 2018-06-02 | Gimnàstic de Tarragona — Rayo Vallecano | 2-0 | VERIFIED | [s17](#evidence-s17) |
| 2018/2019 | 30 | 2018-08-24 | Extremadura UD — Deportivo La Coruña | 0-1 | VERIFIED | [s18](#evidence-s18) |
| 2019/2020 | 445 | 2020-02-02 | CF Fuenlabrada — Girona FC | 0-1 | PARTIAL | [s19](#evidence-s19) |
| 2020/2021 | 597 | 2021-04-04 | CD Lugo — Málaga CF | 0-1 | VERIFIED | [s20](#evidence-s20) |
| 2021/2022 | 247 | 2021-11-03 | CD Mirandés — CD Lugo | 3-2 | VERIFIED | [s21](#evidence-s21) |
| 2022/2023 | 415 | 2023-01-16 | Albacete — CD Leganés | 1-0 | VERIFIED | [s22](#evidence-s22) |
| 2023/2024 | 696 | 2024-05-11 | Sporting Gijón — FC Andorra | 5-2 | VERIFIED | [s23](#evidence-s23) |
| 2024/2025 | 203 | 2024-10-24 | CD Tenerife — Málaga CF | 0-0 | VERIFIED | [s24](#evidence-s24) |

**10 VERIFIED, 3 PARTIAL, 0 wholly unsupported sample cases.** The partial samples are 2012/13, 2013/14 and 2019/20: relevant contemporary/official information was indexed, but direct document opening failed. Their agreement is not elevated to direct historical verification. The Nàstic 2018 report has a misleading `2-1` URL slug; its title, narrative and goals explicitly establish 2–0. No uncertainty is resolved from a slug alone.

## Preservation, reproduction and tests

Protection verified the existing nested baselines: **493 private and 145 public artifacts for the seven completed competitions**, 24 frozen Phase 2 artifacts, 52 Phase 2–3 protected artifacts and the new **59-file Phase 5 baseline** (48 prior Segunda private artifacts plus 11 public Phase 2–4 files). Planning history is separately protected as an append-only byte prefix. The original 6,006 raw records, all five feasibility originals, all 13 modern originals and earlier reports/queues remain unchanged. No application or promotional worktree file was edited. Private originals/evidence and generated review artifacts remain ignored and untracked; nothing staged.

Commands (offline, from the repository root):

```sh
PYTHONPATH=. python3 -B -m scripts.verify_segunda_review --check
PYTHONPATH=. python3 -B -m scripts.verify_segunda_review --output-directory /tmp/EXISTING_EMPTY_DIR
PYTHONPATH=src:. PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -B -m pytest tests/test_segunda_review.py -q -p no:cacheprovider
```

The output-directory command exclusively creates files and refuses overwrite. A fresh empty temporary directory must already exist. The script never acquires data. Public code alone is insufficient to reconstruct private documentary transcriptions: an authorized local copy of frozen sources, baselines, selection and `phase5_historical_review.json` is required. Assessment outputs can then be regenerated deterministically from those inputs; offline checks do not re-fetch or certify the websites.

New synthetic tests: **35 passed**. All four Segunda test modules: **124 passed**. Full repository regression suite: **933 passed**, including all seven app/launcher tests; zero failures, errors or skips. Tests used the previously established isolated offline environment outside iCloud; the original `.venv` was unchanged, no installation or upgrade. The full run completed in 12.59 seconds. Final verification receipt records logs, JUnit hashes, exact output hashes, independent two-directory byte comparisons, protected fingerprints and Git privacy checks.

Public files added: `scripts/verify_segunda_review.py`, `tests/test_segunda_review.py`, this document. `PLANNING_LOG.md` is appended only. Private files added under `data/private/spain/segunda_division/`: `phase5_protected_before.json`, `phase5_sample_selection.json`, `phase5_historical_review.json`, `phase5_evidence_check.json`, `phase5_review_matrix.json`, `phase5_verification.json`. Temporary test logs and independent regenerated copies remain outside the project. Original Phase 2–4 scripts, tests, documentation and private artifacts were not changed.

## Limits and proposed Phase 6 actions — not implemented

1. Formalize retention of both legitimate unusual scores and prohibit storage-order chronology.
2. Approve completion-date treatment for Rayo–Albacete; keep Deportivo playing date distinct from later administrative-finality evidence and inspect the operative closure if final legal certification is required. Neither result can be available before actual completion.
3. Require explicit decisions for all 21 Reus awards. Seek operative award/notification evidence if modeling them is desired; otherwise consider a conservative holdout/exclusion policy for administrative results. Do not infer availability from scheduled dates.
4. Approve how to treat the nine separately corroborated missing-score candidates. Preserve blanks in the original and require an auditable additive transformation; a replacement source acquisition needs separate approval.
5. Preserve all 23 contexts, 30 outliers and 17 reversals; do not automatically exclude partial scheduling evidence or reserve observations. Retry the three partial ordinary samples only through permitted individual documents if further certification is wanted.
6. Approve scoped reserve identity metadata separately from any future cross-league normalization. Never merge a reserve into its parent.
7. Keep the **22-season 1990/91–2011/12 acquisition gap**, original nine 2024/25 missing scores and pinned **2025/26 131 scored / 331 unscored** scope explicit. The 1996/97 RSSSF round-heading proxies are not verified individual playing dates or a completed historical acquisition.
8. Technical validation, historical corroboration, training suitability and permissions remain separate. Existing OpenFootball notices and unresolved upstream/model-training concerns remain; RSSSF restrictions are unchanged. Official/news evidence does not grant redistribution or model-training rights. No whole-dataset historical certification is claimed.

Stop after this Phase 5 evidence review. No corrections, exclusions, standardization, application integration, training, staging, commit, push or merge.

## Evidence register

Exact URLs, attributed document dates (null where not established), access class and limitations follow. `DOCUMENT_OPENED` means the relevant content was retrieved and inspected, not that video footage was watched. `INDEX_ONLY` includes failed direct retrieval and rewritten summaries. Private ledger adds every full audit identity, raw record, per-fact support, confidence and evidence date.

<a id="evidence-missing42"></a>

**missing42** — [Results of Matchday 42 of LALIGA HYPERMOTION 2024/25](https://www.laliga.com/en-BR/laliga-hypermotion/results/2024-25/gameweek-42). LaLiga; document date None; reviewed 2026-11-22; DOCUMENT_OPENED; PRIMARY_EVENT_RECORD.

Official dated round rows corroborate Malaga 2-2 Burgos on May 31; eight June 1 results except Cordoba row, which was outside the returned extract. Limit: Current official results page; not a contemporaneous publication timestamp or independent source-upstream audit. Only eight specifically inspected rows used.

<a id="evidence-cordoba"></a>

**cordoba** — [Noche de aplausos, postes y un empate para cerrar el telón en El Arcángel](https://cordopolis.eldiario.es/deportes/ccf/noche-aplausos-poste-empate-cerrar-telon-arcangel_129_12347871.html). Cordópolis / Álex Jiménez; document date 2025-06-01; reviewed 2026-11-22; DOCUMENT_OPENED; AUTHORED_CONTEMPORARY_REPORT.

Contemporary authored report, published 23:01 and updated 23:26, describes Cordoba-Albacete 1-1. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-high64"></a>

**high64** — [Empacho de goles y remontada en El Sadar](https://www.laliga.com/noticias/empacho-de-goles-y-remontada-en-el-sadar). LaLiga; document date 2014-09-21; reviewed 2026-11-22; DOCUMENT_OPENED; PRIMARY_EVENT_RECORD.

Round 5 dated match account explicitly establishes Osasuna home win 6-4 over Mallorca. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-high66"></a>

**high66** — [Numancia y Lugo empatan un partido histórico](https://www.laliga.com/noticias/numancia-y-lugo-empatan-en-un-partido-historico). LaLiga; document date 2014-12-20; reviewed 2026-11-22; DOCUMENT_OPENED; PRIMARY_EVENT_RECORD.

Round 18 dated match account explicitly establishes Numancia-Lugo 6-6. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-reus_suspend"></a>

**reus_suspend** — [Nota informativa: suspension del CF Reus Deportiu](https://www.laliga.com/noticias/nota-informativa-cf-reus-deportiu). LaLiga; document date 2019-01-18; reviewed 2026-11-22; DOCUMENT_OPENED; PRIMARY_EVENT_RECORD.

Interim participation suspension and cancellation of referee appointment for January 19 Reus-Las Palmas. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-reus_expulsion"></a>

**reus_expulsion** — [Nota Informativa: expediente disciplinario 4/2018-19](https://www.laliga.com/noticias/nota-informativa-164). LaLiga; document date 2019-01-28; reviewed 2026-11-22; DOCUMENT_OPENED; PRIMARY_EVENT_RECORD.

Three-year professional expulsion and EUR250000 fine for salary obligations. Does not list individual fixture awards. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-reus_awards"></a>

**reus_awards** — [LaLiga quita los puntos al Reus y actualiza la clasificación: el Albacete es el nuevo líder](https://as.com/futbol/2019/02/07/segunda/1549543584_310755.html). Diario AS; document date 2019-02-07; reviewed 2026-11-22; DOCUMENT_OPENED; AUTHORED_CONTEMPORARY_REPORT.

Contemporary report says first-half results retained, second-half 1-0 losses; Las Palmas/Albacete/Elche awards already reflected and subsequent points to be allocated as scheduled dates occur. Notes RFEF disagreement. Limit: Independent authored reporting of policy, not operative RFEF awards, individual notifications, earliest knowledge or legal finality. No inference of future result-availability dates.

<a id="evidence-reus_court"></a>

**reus_court** — [La Justicia da la razón al TAD y a LaLiga y ratifica la expulsión del Reus](https://iusport.com/archive/116565/la-justicia-da-la-razon-al-tad-y-a-laliga-y-ratifica-la-expulsion-del-reus). Iusport; document date 2020-12-28; reviewed 2026-11-22; DOCUMENT_OPENED; SECONDARY_LEGAL_REPORT.

Report quotes court rejection of challenge to expulsion and TAD decision dated May 10 2019. Narrative mentions May 13; preserve distinction between decision and reporting dates. Limit: Directly opened secondary legal report, not inspected judgment or original TAD decision; expulsion finality is not proof of every fixture award or knowledge date.

<a id="evidence-reus_tad"></a>

**reus_tad** — [El TAD rechaza definitivamente el recurso del Reus sobre su exclusión](https://iusport.com/archive/85744/el-tad-rechaza-definitivamente-el-recurso-del-reus-sobre-su-exclusion). Iusport; document date 2019-05-13; reviewed 2026-11-22; INDEX_ONLY; SECONDARY_LEGAL_REPORT.

Linked legal report of rejection of expulsion appeal; rendered as rewritten summary by browser. Limit: Tool returned rewritten summary; not counted as direct inspection of primary TAD document.

<a id="evidence-rayo_appeal"></a>

**rayo_appeal** — [Comité de Apelación, expediente 276-2019/20](https://rfef.es/sites/default/files/pdf/resolucion_apelacion_rayo-albacete.pdf). RFEF; document date 2020-02-07; reviewed 2026-11-22; DOCUMENT_OPENED; PRIMARY_EVENT_RECORD.

Page 1 establishes December 15 2019 kickoff, suspension before second half. Later appeal and sanctions are distinct from final played result. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-rayo_schedule"></a>

**rayo_schedule** — [El Comité de Competición fija el Rayo-Albacete de la jornada 20 para el día 10 de junio](https://rfef.es/es/noticias/comite-competicion-fija-rayo-albacete-jornada-20-dia-10-junio). RFEF; document date 2020-06-03; reviewed 2026-11-22; DOCUMENT_OPENED; PRIMARY_EVENT_RECORD.

Second half ordered for June 10 2020 at 20:00 following TAD appeal rejection. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-rayo_result"></a>

**rayo_result** — [Rayo 1 - Albacete Balompié 0 | vídeo resumen](https://www.rayovallecano.es/noticias/rayo-1-albacete-balompie-0-video-resumen). Rayo Vallecano; document date 2020-06-10; reviewed 2026-11-22; DOCUMENT_OPENED; PRIMARY_EVENT_RECORD.

Club match account explicitly dates second-half completion June 10 and confirms 1-0 final result. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-dep_schedule"></a>

**dep_schedule** — [Comité de Competición: fecha RC Deportivo-CF Fuenlabrada](https://rfef.es/sites/default/files/sanciones/resolucion_comite_de_competicion_-_fecha_rc_deportivo-cf_fuenlabrada.pdf). RFEF; document date 2020-08-04; reviewed 2026-11-22; DOCUMENT_OPENED; PRIMARY_EVENT_RECORD.

Three-page resolution records July 20 suspension, intermediate August 5 plan and agreement to play August 7 at 20:00; administrative reassignment, not a played-score certificate. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-dep_result"></a>

**dep_result** — [El Fuenla se queda sin play-off por un penalti en el último minuto](https://www.rtve.es/deportes/20200807/deportivo-fuenlabrada-penalti-ultimo-minuto-cronica-segunda/2038303.shtml). RTVE / Mario Vallejo; technical box EFE; document date 2020-08-07; reviewed 2026-11-22; DOCUMENT_OPENED; AUTHORED_CONTEMPORARY_REPORT.

Contemporary report published 22:06 states Deportivo 2-1 Fuenlabrada, eighteen days after suspension, and lists teams/goals. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-s12"></a>

**s12** — [El Almería se acerca a la cabeza de la tabla tras el pinchazo del Elche](https://cadenaser.com/ser/2012/11/04/deportes/1351988905_850215.html). Cadena SER / EFE; document date 2012-11-04; reviewed 2026-11-22; INDEX_ONLY; AUTHORED_CONTEMPORARY_REPORT.

Lugo 1-0 Elche, dated contemporary report. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-s13"></a>

**s13** — [CD Lugo vs AD Alcorcón, jornada 17](https://www.laliga.com/partido/temporada-2013-2014-laliga-1-2-3-cd-lugo-ad-alcorcon-17). LaLiga; document date 2013-12-04; reviewed 2026-11-22; INDEX_ONLY; PRIMARY_EVENT_RECORD.

Indexed official match card reports Lugo 1-2 Alcorcon on December 4; direct open failed. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-s14"></a>

**s14** — [Liga Adelante - Crónicas de los partidos del sábado](https://www.laliga.com/es-GB/noticias/liga-adelante-cronicas-de-los-partidos-del-sabado-34). LaLiga; document date 2015-05-16; reviewed 2026-11-22; DOCUMENT_OPENED; PRIMARY_EVENT_RECORD.

Dated round 38 report lists R. Sporting 3-1 R. Racing C. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-s15"></a>

**s15** — [SD Huesca vs Real Oviedo, jornada 14](https://www.laliga.com/partido/temporada-2015-2016-laliga-1-2-3-sd-huesca-real-oviedo-14). LaLiga; document date 2015-11-21; reviewed 2026-11-22; DOCUMENT_OPENED; PRIMARY_EVENT_RECORD.

Official card gives 0-1 final and November 21; corroborating EFE/AS account also inspected. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-s16"></a>

**s16** — [La lucha por la segunda plaza de LaLiga 1|2|3 se pone al rojo vivo](https://www.laliga.com/noticias/la-lucha-por-la-segunda-plaza-de-laliga-123-se-pone-al-rojo-vivo). LaLiga; document date 2016-12-11; reviewed 2026-11-22; DOCUMENT_OPENED; PRIMARY_EVENT_RECORD.

Dated contemporary round account states CD Lugo 3-1 CD Numancia. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-s17"></a>

**s17** — [Nàstic 2-0 Rayo Vallecano](https://gimnasticdetarragona.cat/nastic-2-1-rayo-vallecano/). Gimnàstic de Tarragona; document date 2018-06-02; reviewed 2026-11-22; DOCUMENT_OPENED; PRIMARY_EVENT_RECORD.

Dated club account states 2-0; URL slug says 2-1 but title and narrative establish 2-0. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-s18"></a>

**s18** — [Extremadura UD vs RC Deportivo, jornada 2](https://www.laliga.com/partido/temporada-2018-2019-laliga-1-2-3-extremadura-ud-rc-deportivo-2). LaLiga; document date 2018-08-24; reviewed 2026-11-22; DOCUMENT_OPENED; PRIMARY_EVENT_RECORD.

Official card and full-time commentary establish 0-1 on August 24. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-s19"></a>

**s19** — [Resumen de CF Fuenlabrada vs Girona FC (0-1)](https://www.youtube.com/watch?v=1MkekiFP1pE). LaLiga; document date 2020-02-02; reviewed 2026-11-22; INDEX_ONLY; PRIMARY_EVENT_RECORD.

Official LaLiga video description indexed with February 2 2020 and 0-1; direct opening failed. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-s20"></a>

**s20** — [Resultados de la Jornada 33 de LALIGA HYPERMOTION 2020/21](https://www.laliga.com/laliga-hypermotion/resultados/2020-21/jornada-33). LaLiga; document date None; reviewed 2026-11-22; DOCUMENT_OPENED; PRIMARY_EVENT_RECORD.

Inspected row gives April 4 2021, CD Lugo 0-1 Malaga CF. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-s21"></a>

**s21** — [Resultados de la Jornada 14 de LALIGA HYPERMOTION 2021/22](https://www.laliga.com/laliga-hypermotion/resultados/2021-22/jornada-14). LaLiga; document date None; reviewed 2026-11-22; DOCUMENT_OPENED; PRIMARY_EVENT_RECORD.

Inspected row gives November 3 2021, Mirandes 3-2 Lugo. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-s22"></a>

**s22** — [El C.D. Leganés corta su racha en Albacete (1-0)](https://www.cdleganes.com/noticias/cronica-albacete-leganes-j23). CD Leganés; document date 2023-01-16; reviewed 2026-11-22; DOCUMENT_OPENED; PRIMARY_EVENT_RECORD.

Dated club match account confirms Albacete 1-0 Leganes. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-s23"></a>

**s23** — [El Sporting se merienda al Andorra y alimenta el sueño del playoff](https://cadenaser.com/asturias/2024/05/11/el-sporting-se-merienda-al-andorra-y-alimenta-el-sueno-del-playoff-ser-gijon/). Cadena SER / David González; document date 2024-05-11; reviewed 2026-11-22; DOCUMENT_OPENED; AUTHORED_CONTEMPORARY_REPORT.

Dated authored match report confirms Sporting 5-2 Andorra. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-s24"></a>

**s24** — [Un quiero y no puedo](https://hemeroteca.deporpress.com/un-quiero-y-no-puedo/). DeporPress / Dani Cerdeña; document date 2024-10-24; reviewed 2026-11-22; DOCUMENT_OPENED; AUTHORED_CONTEMPORARY_REPORT.

Dated authored match report confirms Tenerife home draw 0-0 with Malaga. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-o14"></a>

**o14** — [Alavés-Osasuna, suspendido; cuatro duelos se juegan el sábado](https://www.laliga.com/noticias/una-final-se-celebra-en-la-zona-baja). LaLiga; document date 2015-02-07; reviewed 2026-11-22; DOCUMENT_OPENED; PRIMARY_EVENT_RECORD.

Official notice establishes weather postponement on February 7, not eventual March result. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-o15"></a>

**o15** — [1-2. El Mallorca toma aire en Huesca](https://navarra.okdiario.com/deportes/futbol/1-2-mallorca-toma-aire-huesca/20160316232000030895.html). Navarra / EFE; document date 2016-03-16; reviewed 2026-11-22; INDEX_ONLY; AUTHORED_CONTEMPORARY_REPORT.

Indexed contemporary report gives 1-2 on March 16 and snow postponement; direct opening failed. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-o16a"></a>

**o16a** — [Tres partidos en una semana para suavizar la crisis](https://as.com/futbol/2016/12/06/segunda/1481019545_899537.html). Diario AS; document date 2016-12-06; reviewed 2026-11-22; INDEX_ONLY; AUTHORED_CONTEMPORARY_REPORT.

Reports rain postponement of Levante-Rayo and December 14 rescheduling, not completion itself. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-o16b"></a>

**o16b** — [El Levante amplía su ventaja en el liderato tras ganar al UCAM Murcia](https://www.europapress.es/deportes/futbol-00162/noticia-levante-amplia-ventaja-liderato-ganar-ucam-murcia-20170111215032.html). Europa Press; document date 2017-01-11; reviewed 2026-11-22; INDEX_ONLY; AUTHORED_CONTEMPORARY_REPORT.

Indexed agency report confirms postponed round 19 game played January 11, 0-2. Direct opening failed. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-o17a"></a>

**o17a** — [El Nástic-FC Barcelona B se disputará el 1 de noviembre](https://www.laliga.com/es-MX/noticias/el-nastic-fc-barcelona-b-se-disputara-el-1-de-noviembre). LaLiga; document date None; reviewed 2026-11-22; INDEX_ONLY; PRIMARY_EVENT_RECORD.

Indexed official announcement reschedules postponed round 7 to November 1; original cause and completed facts not inspected. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-o17b"></a>

**o17b** — [Descalabro en El Sadar: los rojillos pierden ante el Nástic el partido aplazado por la nieve](https://navarra.okdiario.com/deportes/osasuna/cronica-osasuna-nastic-sadar-futbol/20180118191605165829.html). Navarra / Patxi Cervantes; document date 2018-01-18; reviewed 2026-11-22; INDEX_ONLY; AUTHORED_CONTEMPORARY_REPORT.

Indexed authored report confirms January 18 0-2 following December 1 snow postponement; direct opening failed. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-o19a"></a>

**o19a** — [Así seguimos el directo del Fuenlabrada-Real Zaragoza](https://es.besoccer.com/noticia/sigue-el-directo-del-fuenlabrada-zaragoza-727731). BeSoccer; document date 2019-10-16; reviewed 2026-11-22; INDEX_ONLY; AUTHORED_CONTEMPORARY_REPORT.

Live-report index mentions food-poisoning postponement and October 16 rearrangement. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-o19b"></a>

**o19b** — [El Zaragoza se frena en Anduva con otro empate](https://www.europapress.es/deportes/futbol-00162/noticia-zaragoza-frena-anduva-otro-empate-20200219232310.html). Europa Press; document date 2020-02-19; reviewed 2026-11-22; INDEX_ONLY; AUTHORED_CONTEMPORARY_REPORT.

Indexed agency report establishes February 19 1-1 and earlier rain postponement. Direct opening failed. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-o20a"></a>

**o20a** — [El Almería recuperará el 5 de noviembre uno de los partidos aplazados](https://www.udalmeriasad.com/noticias/el-almeria-recuperara-el-5-de-noviembre-uno-de-los-partidos-aplazados). UD Almería; document date None; reviewed 2026-11-22; INDEX_ONLY; PRIMARY_EVENT_RECORD.

Indexed club notice explains delayed season start after promotion playoffs, November 5 Sabadell rearrangement and pending Almeria-Zaragoza. Direct opening failed. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-o20z"></a>

**o20z** — [Zaragoza-Girona y Sabadell-Almería se jugarán el 4 y 5 de noviembre](https://as.com/futbol/2020/10/22/segunda/1603384092_958695.html). Diario AS; document date 2020-10-22; reviewed 2026-11-22; INDEX_ONLY; AUTHORED_CONTEMPORARY_REPORT.

Indexed report explains delayed opening round following playoffs; contains a Sabadell-Girona typo, so do not use as fixture result certification. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-o20b"></a>

**o20b** — [Designaciones de los partidos aplazados 2ª División, temporada 2020/21](https://rfef.es/sites/default/files/images19/partidos_aplazados_2a.pdf). RFEF; document date None; reviewed 2026-11-22; DOCUMENT_OPENED; PRIMARY_EVENT_RECORD.

One-page appointments document lists Almeria-Zaragoza and Sabadell-Alcorcon December 9, Girona-Logrones December 10. Scheduling only, not proof of scores. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-o20c"></a>

**o20c** — [Alcorcón-Ponferradina, primer partido de Segunda suspendido por el coronavirus esta temporada](https://elpais.com/deportes/2020-10-18/el-comite-de-competicion-suspende-el-alcorcon-ponferradina-por-cuatro-positivos-antes-del-partido.html). El País / Diego Fonseca; document date 2020-10-18; reviewed 2026-11-22; DOCUMENT_OPENED; AUTHORED_CONTEMPORARY_REPORT.

Authored contemporary article reproduces context of federation postponement after four positive tests. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-o21a"></a>

**o21a** — [El partido aplazado ante la U.D. Almería se disputará finalmente el miércoles 17 de febrero](https://www.cdleganes.com/noticias/el-partido-aplazado-ante-la-u-d-almeria-se-disputara-finalmente-el-miercoles-17-de-febrero-a-las-1900-horas). CD Leganés; document date 2021-02-09; reviewed 2026-11-22; DOCUMENT_OPENED; PRIMARY_EVENT_RECORD.

Club announcement establishes Filomena postponement and February 17 plan. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-o21f"></a>

**o21f** — [El País, 10 enero 2021, page 35](https://elpais.com/estaticos/2021/01/filomena/pdf/ep-10012021.pdf). El País; document date 2021-01-10; reviewed 2026-11-22; INDEX_ONLY; AUTHORED_CONTEMPORARY_REPORT.

Indexed contemporary edition lists Mirandes-Rayo, Alcorcon-Albacete and Leganes-Almeria postponed by storm. PDF not directly inspected. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-o21b"></a>

**o21b** — [El Rayo-Mirandés, aplazado por un brote de COVID](https://as.com/futbol/2021/03/26/segunda/1616760231_145464.html). Diario AS; document date 2021-03-26; reviewed 2026-11-22; INDEX_ONLY; AUTHORED_CONTEMPORARY_REPORT.

Indexed contemporary report explains round 31 COVID postponement and recalls January Mirandes-Rayo affected by Filomena. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-o21c"></a>

**o21c** — [El coronavirus condiciona la visita del Mirandés a El Molinón-Quini](https://as.com/futbol/2021/04/03/segunda/1617449109_423979.html). Diario AS; document date 2021-04-03; reviewed 2026-11-22; INDEX_ONLY; AUTHORED_CONTEMPORARY_REPORT.

Indexed contemporary report records postponement of both Rayo and Tenerife fixtures after 13 positive tests at Mirandes. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-o22"></a>

**o22** — [Lugo 2-1 Almería: resumen, goles y resultado del partido](https://as.com/futbol/2022/01/19/segunda/1642616328_075583.html). Diario AS / Daniel Pérez; document date 2022-01-19; reviewed 2026-11-22; DOCUMENT_OPENED; AUTHORED_CONTEMPORARY_REPORT.

Inspected live report gives January 19 full-time 2-1 and identifies postponed round 21. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-o22cause"></a>

**o22cause** — [El posible once del Almería ante el Lugo](https://www.estadiodeportivo.com/noticias-futbol/ud-almeria/2022/01/17/posible-once-almeria-lugo/376169.html). Estadio Deportivo; document date 2022-01-17; reviewed 2026-11-22; INDEX_ONLY; AUTHORED_CONTEMPORARY_REPORT.

Indexed report explains December 20 original fixture postponed by Lugo outbreak; final date January 19. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-o24"></a>

**o24** — [Fijado el nuevo señalamiento de los encuentros aplazados por el incendio de Valencia](https://rfef.es/es/noticias/fijado-el-nuevo-senalamiento-de-los-encuentros-aplazados-por-el-incendio-de-valencia). RFEF; document date 2024-02-28; reviewed 2026-11-22; DOCUMENT_OPENED; PRIMARY_EVENT_RECORD.

Direct federation notice establishes round 28 Levante-Andorra postponed for Valencia fire, rescheduled March 13. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-o24dana"></a>

**o24dana** — [Nuevos señalamientos de los partidos aplazados la semana pasada](https://rfef.es/es/noticias/nuevos-senalamientos-de-los-partidos-aplazados-la-semana-pasada). RFEF; document date 2024-11-06; reviewed 2026-11-22; DOCUMENT_OPENED; PRIMARY_EVENT_RECORD.

Direct federation notice lists all four round 13 postponements and reschedules Eldense November 20 and three others November 27. Almeria was subsequently moved to November 26. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-o24almeria"></a>

**o24almeria** — [El Almería-Córdoba se jugará finalmente el martes 26](https://www.diariodealmeria.es/ud-almeria/almeria-cordoba-jugara-finalmente-martes_0_2002781074.html). Diario de Almería; document date 2024-11-13; reviewed 2026-11-22; DOCUMENT_OPENED; AUTHORED_CONTEMPORARY_REPORT.

Inspected authored report distinguishes original November 3, provisional November 27 and revised November 26 by club agreement and federation approval. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-o24tenerife"></a>

**o24tenerife** — [Determinación fecha partido aplazado Tenerife-Levante, jornada 14](https://rfef.es/sites/default/files/sanciones/Resoluci%C3%B3n%20Juez%20de%20Competiciones%20Profesionales%20Tenerife%20Levante.pdf). RFEF; document date 2024-11-12; reviewed 2026-11-22; DOCUMENT_OPENED; PRIMARY_EVENT_RECORD.

Direct two-page resolution sets January 7 2025 with conditional January 4 alternative after DANA postponement. Does not prove completion. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-o24dep"></a>

**o24dep** — [¿Por qué el Tenerife-Deportivo se juega a la vez que la jornada decisiva de la Champions?](https://as.com/futbol/segunda/por-que-el-tenerife-deportivo-se-juega-a-la-vez-que-la-jornada-decisiva-de-la-champions-n/). Diario AS; document date 2025-01-29; reviewed 2026-11-22; INDEX_ONLY; AUTHORED_CONTEMPORARY_REPORT.

Indexed contemporary explanation: December 15 suspension due to Dorothea storm, rearranged January 29. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-o25ferrol"></a>

**o25ferrol** — [El Racing Club Ferrol-vs Burgos CF se jugará el 5 de marzo](https://www.racingclubferrol.net/noticias/nueva-fecha-para-el-partido-aplazado-racing-club-ferrol-burgos-cf). Racing Club Ferrol; document date None; reviewed 2026-11-22; DOCUMENT_OPENED; PRIMARY_EVENT_RECORD.

Direct club notice distinguishes January 26 original fixture and March 5 new date after adverse weather alert. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-rev12"></a>

**rev12** — [La lluvia obliga a suspender el Huesca-Barça B](https://www.aragondigital.es/articulo/deportes/lluvia-obliga-suspender-huesca-barca-b/20121020202100506849.html). Aragón Digital; document date 2012-10-20; reviewed 2026-11-22; INDEX_ONLY; AUTHORED_CONTEMPORARY_REPORT.

Indexed contemporary report establishes October 20 rain postponement, not eventual October 31 score. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-rev14a"></a>

**rev14a** — [Sabadell-Las Palmas se celebrará el miércoles 10 de diciembre](https://www.laliga.com/noticias/sabadell-las-palmas-se-celebrara-el-miercoles-10-de-diciembre). LaLiga; document date 2014-12-03; reviewed 2026-11-22; DOCUMENT_OPENED; PRIMARY_EVENT_RECORD.

Indexed official notice establishes weather postponement and December 10 rearrangement. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-rev14b"></a>

**rev14b** — [El Osasuna-Zaragoza, suspendido por nieve](https://cadenaser.com/ser/2015/02/01/deportes/1422787730_965476.html). Cadena SER; document date 2015-02-01; reviewed 2026-11-22; INDEX_ONLY; AUTHORED_CONTEMPORARY_REPORT.

Indexed contemporary report establishes snow postponement of round 23, not February 10 final result. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-rev17"></a>

**rev17** — [El Huesca deja escapar el liderato tras empatar con el Albacete en el partido aplazado](https://www.europapress.es/deportes/futbol-00162/noticia-huesca-deja-escapar-liderato-empatar-albacete-partido-aplazado-20180412221615.html). Europa Press; document date 2018-04-12; reviewed 2026-11-22; INDEX_ONLY; AUTHORED_CONTEMPORARY_REPORT.

Indexed agency report establishes April 12 0-0 and postponement following Pelayo Novo accident. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-i_barca"></a>

**i_barca** — [Historia Barça Atlètic](https://www.fcbarcelona.es/es/futbol/barca-atletic/historia). FC Barcelona; document date None; reviewed 2026-11-22; DOCUMENT_OPENED; PRIMARY_CLUB_HISTORY.

Club history documents B/Atletic naming periods: 1991 B, 2008 Atletic, 2010 B, June 2022 Atletic. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-i_bilbao"></a>

**i_bilbao** — [Videoteca: El último ascenso de los cachorros (2014/2015)](https://www.athletic-club.eus/noticias/2020/03/21/videoteca-el-ultimo-ascenso-de-los-cachorros-2014-2015/). Athletic Club; document date 2020-03-21; reviewed 2026-11-22; DOCUMENT_OPENED; PRIMARY_CLUB_HISTORY.

Club retrospective calls Bilbao Athletic its reserve and records promotion to Segunda in 2015. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-i_castilla"></a>

**i_castilla** — [El Castilla empata contra el Antequera](https://www.realmadrid.com/es-ES/noticias/futbol/cantera-masculina/cronicas/cronica-castilla-antequera-j27-liga-09-03-2024). Real Madrid; document date 2024-03-09; reviewed 2026-11-22; DOCUMENT_OPENED; PRIMARY_CLUB_HISTORY.

Club report explicitly calls Real Madrid Castilla its reserve; historic B rename dates not established by this page. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-i_sanse"></a>

**i_sanse** — [History](https://www.realsociedad.eus/en/club/history). Real Sociedad; document date None; reviewed 2026-11-22; DOCUMENT_OPENED; PRIMARY_CLUB_HISTORY.

Official history distinguishes Sanse reserve breeding ground from Real Sociedad first team. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-i_sevilla"></a>

**i_sevilla** — [Diez cosas que quizá no sabías del Sevilla Atlético](https://www.laliga.com/es-GB/noticias/diez-cosas-que-quiza-no-sabias-del-sevilla-atletico). LaLiga; document date 2016-06-30; reviewed 2026-11-22; DOCUMENT_OPENED; PRIMARY_CLUB_HISTORY.

League history identifies Sevilla Atletico as Sevilla reserve, founded from CD Puerto and affiliated in 1958. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-i_villarreal"></a>

**i_villarreal** — [Sí, lo son… ¡de Segunda División (2-0)!](https://villarrealcf.es/es/si-lo-son-de-segunda-division-2-0/). Villarreal CF; document date 2022-06-11; reviewed 2026-11-22; DOCUMENT_OPENED; PRIMARY_CLUB_HISTORY.

Club account explicitly distinguishes Villarreal B reserve and records promotion in 2022. Limit: Only the stated event/context is supported; no population certification or rights clearance. Search-index text is not a directly inspected document.

<a id="evidence-dep_archive"></a>

**dep_archive** — [Competición acata la resolución del TAD y archiva el expediente al Fuenlabrada](https://iusport.com/archive/111994/competicion-acata-la-resolucion-del-tad-y-archiva-el-expediente-al-fuenlabrada). Iusport; document date 2020-08-27; reviewed 2026-11-22; DOCUMENT_OPENED; SECONDARY_LEGAL_REPORT.

Secondary legal report quotes RFEF closure after jurisdiction ruling, expediente207/2020 TAD; not an independently inspected operative award. Limit: Directly opened secondary legal report; original TAD/league-judge closure and service dates not inspected. Do not infer original final-result availability from later reporting.

<a id="evidence-dep_tad"></a>

**dep_tad** — [El TAD confirma el fallo del juez de LaLiga y pone punto y final al caso Dépor-Fuenlabrada](https://iusport.com/archive/115846/el-tad-confirma-el-fallo-del-juez-de-laliga-y-pone-punto-y-final-al-caso-depor-fuenlabrada). Iusport; document date 2020-12-05; reviewed 2026-11-22; DOCUMENT_OPENED; SECONDARY_LEGAL_REPORT.

Secondary legal report dates TAD rejection to November20, confirming August7 league-judge closure. Original resolution and service/finality dates not inspected. Limit: Directly opened secondary legal report; original TAD/league-judge closure and service dates not inspected. Do not infer original final-result availability from later reporting.

<a id="evidence-rev14result"></a>

**rev14result** — [El Sabadell planta cara al líder](https://www.laliga.com/es-GB/noticias/el-sabadell-planta-cara-al-lider). LaLiga; document date 2014-12-10; reviewed 2026-11-22; DOCUMENT_OPENED; PRIMARY_EVENT_RECORD.

Dated official match report establishes Sabadell-Las Palmas2-2 on December10, postponed from November29 by rain. Limit: Direct match narrative, not an additional independent provider of a second feed; no rights clearance.
