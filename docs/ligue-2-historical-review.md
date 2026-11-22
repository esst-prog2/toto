# Ligue 2 — Phase 5 historical evidence review

Review date: 2026-11-22. Scope: evidence only. No corrections, screening decisions, effective result dates, aliases or standardized outputs are authorized by this report.

## Population and method

The protected Phase 4 population is 4,106 observations across 2014/15–2024/25: 4,006 score-bearing and 100 explicitly cancelled. All 364 queue bindings were independently checked against the structural report. Categories overlap: 228 wide-round members, 25 diagnostic outliers, 62 endpoints of 31 reversals (29 already flagged, 33 additional), 100 cancellations and the three special fixtures.

The frozen ordinary sample chooses the minimum SHA-256 of `ligue2-phase5-v1:` plus audit ID among unflagged score-bearing records in each season. The 78 distinct frozen priority fixtures comprise the samples, outliers, reversal endpoints and special fixtures. One additional administrative discovery brings targeted research to 79 fixtures. All 364 queue records, 11 samples and that discovery appear in the 376-entry registry; 297 received context-only review.

FULLY_CORROBORATED means only that both participants, actual date and score have direct independent support. It does not certify administrative finality, availability, training suitability or licensing. PARTIALLY_CORROBORATED supports a subset of those facts. UNRESOLVED includes context-only entries and cancellations; it does not mean erroneous. Index-only and compiled/shared-upstream pages cannot establish independent fixture corroboration.

## Measured results

```json
{
  "structural_population": {
    "population": 4106,
    "queue": 364,
    "categories": {
      "SOURCE_ORDER_DATE_REVERSAL": 62,
      "WIDE_ROUND": 228,
      "DIAGNOSTIC_DATE_OUTLIER": 25,
      "UNUSUAL_SCORE": 1,
      "SOURCE_CANCELLED": 100,
      "SOURCE_MARKED_AWARDED": 1,
      "BORDEAUX_RODEZ_ADMINISTRATIVE_REVIEW": 1
    },
    "wide_contexts": 23,
    "reversal_pairs": 31,
    "outliers_in_wide": 25,
    "reversal_endpoints_in_wide": 29,
    "additional_reversal_endpoints": 33
  },
  "review_registry": 376,
  "ordinary_samples": 11,
  "frozen_priority_distinct_fixtures": 78,
  "priority_distinct_fixtures": 79,
  "fixture_level_direct_evidence_fixtures": 18,
  "direct_context_referenced_fixtures": 181,
  "additional_discovered_fixtures": 1,
  "fixture_classifications": {
    "FULLY_CORROBORATED": 9,
    "UNRESOLVED": 358,
    "PARTIALLY_CORROBORATED": 9
  },
  "priority_classifications": {
    "FULLY_CORROBORATED": 9,
    "UNRESOLVED": 61,
    "PARTIALLY_CORROBORATED": 9
  },
  "ordinary_classifications": {
    "FULLY_CORROBORATED": 3,
    "UNRESOLVED": 7,
    "PARTIALLY_CORROBORATED": 1
  },
  "research_modes": {
    "PRIORITY_FIXTURE_RESEARCH": 79,
    "CONTEXT_REVIEW_ONLY": 297
  },
  "wide_context_classifications": {
    "PARTIAL": 15,
    "DOCUMENTED": 8
  },
  "reversal_context_classifications": {
    "UNRESOLVED": 25,
    "PARTIAL": 6
  },
  "evidence_access": {
    "DIRECT": 29,
    "INDEX_ONLY": 31
  },
  "evidence_independence": {
    "OFFICIAL_RECORD": 13,
    "INDEPENDENT_NARRATIVE": 18,
    "COMPILED_OR_UNESTABLISHED": 29
  }
}
```

There are 18 fixtures with direct core-fact evidence: nine fully and nine partially corroborated. No inspected evidence establishes a source-value contradiction. The other 358 registry entries remain unresolved at core-fact level. Of 79 targeted fixtures, 61 remain unresolved. Context references supported by directly inspected independent documents cover 181 registry fixtures; this overlaps the 18 and must not be added to them.

## Ordinary historical sample

| Season | Source date | Fixture | Source score | Evidence classification | References |
|---|---|---|---|---|---|
| 2014/2015 | 2014-09-19 | Gazélec FC Ajaccio – Dijon FCO | 2-0 | FULLY_CORROBORATED | D07 |
| 2015/2016 | 2015-08-21 | Stade Lavallois – Red Star FC | 2-1 | FULLY_CORROBORATED | D08 |
| 2016/2017 | 2016-09-20 | Nîmes Olympique – ESTAC Troyes | 2-2 | UNRESOLVED | I10 |
| 2017/2018 | 2017-08-04 | AC Ajaccio – Stade Brestois 29 | 2-1 | UNRESOLVED | I11 |
| 2018/2019 | 2018-11-09 | Gazélec FC Ajaccio – ESTAC Troyes | 2-1 | UNRESOLVED | I12 |
| 2019/2020 | 2019-12-20 | Grenoble Foot 38 – Rodez AF | 2-1 | PARTIALLY_CORROBORATED | D10 |
| 2020/2021 | 2020-12-14 | Havre AC – Clermont Foot 63 | 0-0 | UNRESOLVED | I13 |
| 2021/2022 | 2022-02-12 | Paris FC – US Quevilly-Rouen | 3-0 | UNRESOLVED | I14 |
| 2022/2023 | 2022-11-12 | Chamois Niortais – Nîmes Olympique | 1-1 | UNRESOLVED | I15 |
| 2023/2024 | 2023-11-11 | AC Ajaccio – ESTAC Troyes | 1-0 | FULLY_CORROBORATED | D09 |
| 2024/2025 | 2024-09-13 | Rodez AF – EA Guingamp | 1-2 | UNRESOLVED | I16 |

Three samples are fully corroborated, one partial and seven unresolved. Lack of accessible independent evidence is not a finding of error.

## Administrative and interrupted fixtures

- **Niort–Valenciennes, 2020-12-22, 0–3 [awarded]:** contemporary indexed reporting describes a match not played as scheduled and an administrative award reported on 2021-01-06, with an appeal contemplated. The underlying signed decision, precise numerical homologation and appeal finality were not retrieved. Neither December 22 nor January 6 is approved as result availability. Source values remain unchanged (I01, I02).
- **Bordeaux–Rodez, 2023-06-02, 0–1:** contemporary reporting describes interruption after the Rodez opener. The June 5 LFP decision deferred the sporting outcome; June 12 imposed a defeat by penalty. That text does not itself establish a numerical 0–3 award. The club’s June 27 statement accepts the CNOSF proposal and closes the disciplinary/sporting sequence while reserving other proceedings. Numeric semantics and effective availability still require Phase 6 consideration (D02–D05).
- **Valenciennes–Béziers, 2019-04-19, 5–6:** directly inspected contemporary authored reporting corroborates participants, date and final score. Eleven goals are not a reason to correct or exclude it (D06).
- **Additional discovery — Nancy–Quevilly-Rouen, 2022-04-22, 0–3:** audit ID `afcb54cb3230a64b091b4980dedb16b65e9ac9df6228d2b3252c2f85b9506862`, physical source line 522, absent from the original Phase 4 flags. Official May 4 disciplinary text imposes a defeat by penalty; indexed contemporary reporting describes interruption around minute 39/40 at 0–3. Numeric homologation, finality and availability are unresolved. It was added to Phase 5 only; the Phase 4 queue was not rewritten (D25, I03).
- **AC Ajaccio–Bastia, 2024/25:** club and official documents distinguish October 26 interruption from December 3 resumption at minute 42. Contemporary reporting corroborates the December 3 completion and 0–0. No completion-date policy is applied here (D21–D23, D29).

Source/document ambiguities: D13 contains conflicting score wording, so no score claim was extracted. D19 announces an intermediate Clermont–Amiens schedule, not proof against the eventual source date. D29 has a commission-date inconsistency with D21; that date was not adopted. These are documentary limitations, not established dataset contradictions.

## All 23 wide-round contexts

Eight have a documented contextual explanation and 15 are partial. None of these labels certifies all member fixtures. The original 228 members and 25 outliers remain unchanged.

| Season | Round | Source span | Classification | References |
|---|---|---|---|---|
| 2016/2017 | 21 | 2017-01-20–2017-02-21 | PARTIAL | I30 |
| 2017/2018 | 19 | 2017-12-15–2018-01-23 | PARTIAL | I31 |
| 2017/2018 | 29 | 2018-03-09–2018-04-03 | PARTIAL | I32 |
| 2017/2018 | 32 | 2018-04-06–2018-04-30 | PARTIAL | I33 |
| 2018/2019 | 5 | 2018-08-24–2018-10-02 | PARTIAL | I34 |
| 2018/2019 | 19 | 2018-12-21–2019-01-29 | PARTIAL | I35, I36 |
| 2020/2021 | 3 | 2020-09-12–2020-09-30 | PARTIAL | I37 |
| 2020/2021 | 8 | 2020-10-24–2020-11-24 | DOCUMENTED | D17 |
| 2020/2021 | 9 | 2020-10-31–2020-12-15 | PARTIAL | D11, I39 |
| 2020/2021 | 11 | 2020-11-21–2020-12-15 | PARTIAL | D11, I40 |
| 2020/2021 | 29 | 2021-03-13–2021-04-14 | PARTIAL | D19, I41 |
| 2020/2021 | 31 | 2021-04-03–2021-04-28 | PARTIAL | I42 |
| 2020/2021 | 35 | 2021-04-24–2021-05-12 | DOCUMENTED | D18, I43 |
| 2021/2022 | 2 | 2021-07-31–2021-08-18 | DOCUMENTED | D15, I44 |
| 2021/2022 | 5 | 2021-08-21–2021-09-14 | PARTIAL | I45 |
| 2021/2022 | 20 | 2022-01-08–2022-01-28 | PARTIAL | I46, I47 |
| 2021/2022 | 21 | 2022-01-15–2022-02-01 | DOCUMENTED | D12, D16 |
| 2021/2022 | 22 | 2022-01-22–2022-02-15 | PARTIAL | I49 |
| 2022/2023 | 7 | 2022-09-02–2022-10-04 | DOCUMENTED | D24 |
| 2022/2023 | 23 | 2023-02-11–2023-03-14 | DOCUMENTED | D13, D14, I51 |
| 2023/2024 | 13 | 2023-11-04–2023-11-28 | PARTIAL | I52 |
| 2024/2025 | 8 | 2024-10-04–2024-10-22 | DOCUMENTED | D20, I53 |
| 2024/2025 | 10 | 2024-10-25–2024-12-03 | DOCUMENTED | D21, D22, D23 |

Documented contexts concern COVID postponements, Paris FC pitch conditions, Guingamp–Rodez transport disruption, Pau–Bastia transport disruption, and the interrupted Ajaccio derby. Partial contexts retain incomplete evidence about actual dates or causes; long spans are not classified as errors.

## All 25 diagnostic outliers

Five have full four-fact corroboration, six partial and 14 unresolved. No source dates or scores were changed.

| Season | Source date | Fixture | Source score | Core-fact classification | References |
|---|---|---|---|---|---|
| 2016/2017 | 2017-02-21 | RC Strasbourg – Tours FC | 4-2 | UNRESOLVED | I30 |
| 2017/2018 | 2018-01-23 | Gazélec FC Ajaccio – Nîmes Olympique | 2-0 | UNRESOLVED | I31 |
| 2017/2018 | 2018-04-03 | Tours FC – Valenciennes FC | 1-2 | UNRESOLVED | I32 |
| 2017/2018 | 2018-04-30 | Stade de Reims – Havre AC | 0-1 | UNRESOLVED | I33 |
| 2018/2019 | 2018-10-02 | AS Béziers – RC Lens | 0-0 | UNRESOLVED | I34 |
| 2018/2019 | 2019-01-15 | Havre AC – Valenciennes FC | 4-3 | UNRESOLVED | I35 |
| 2018/2019 | 2019-01-29 | FC Metz – AS Nancy Lorraine | 3-0 | UNRESOLVED | I36 |
| 2020/2021 | 2020-09-30 | AC Ajaccio – USL Dunkerque | 1-0 | UNRESOLVED | I37 |
| 2020/2021 | 2020-11-24 | Grenoble Foot 38 – AS Nancy Lorraine | 1-0 | PARTIALLY_CORROBORATED | D17 |
| 2020/2021 | 2020-12-15 | Chamois Niortais – Grenoble Foot 38 | 0-0 | FULLY_CORROBORATED | D11, I39 |
| 2020/2021 | 2020-12-15 | AS Nancy Lorraine – ESTAC Troyes | 2-3 | FULLY_CORROBORATED | D11, I40 |
| 2020/2021 | 2021-04-14 | Clermont Foot 63 – Amiens SC | 3-0 | PARTIALLY_CORROBORATED | D19, I41 |
| 2020/2021 | 2021-04-28 | USL Dunkerque – Amiens SC | 1-1 | UNRESOLVED | I42 |
| 2020/2021 | 2021-05-12 | Toulouse FC – Pau FC | 2-2 | PARTIALLY_CORROBORATED | D18, I43 |
| 2021/2022 | 2021-08-18 | US Quevilly-Rouen – SC Bastia | 1-2 | PARTIALLY_CORROBORATED | D15, I44 |
| 2021/2022 | 2021-09-14 | AC Ajaccio – Paris FC | 1-0 | UNRESOLVED | I45 |
| 2021/2022 | 2022-01-28 | SM Caen – Chamois Niortais | 0-2 | UNRESOLVED | I46 |
| 2021/2022 | 2022-01-28 | USL Dunkerque – Paris FC | 1-1 | UNRESOLVED | I47 |
| 2021/2022 | 2022-02-01 | Chamois Niortais – USL Dunkerque | 2-0 | FULLY_CORROBORATED | D12, D16 |
| 2021/2022 | 2022-02-15 | Grenoble Foot 38 – Chamois Niortais | 1-0 | UNRESOLVED | I49 |
| 2022/2023 | 2022-10-04 | EA Guingamp – Rodez AF | 0-0 | FULLY_CORROBORATED | D24 |
| 2022/2023 | 2023-03-14 | Paris FC – Amiens SC | 3-0 | PARTIALLY_CORROBORATED | D13, D14, I51 |
| 2023/2024 | 2023-11-28 | US Concarneau – Pau FC | 1-2 | UNRESOLVED | I52 |
| 2024/2025 | 2024-10-22 | Pau FC – SC Bastia | 1-1 | PARTIALLY_CORROBORATED | D20, I53 |
| 2024/2025 | 2024-12-03 | AC Ajaccio – SC Bastia | 0-0 | FULLY_CORROBORATED | D21, D22, D23 |

## All 31 source-order reversal pairs

Every pair received a bounded targeted search, retained in the private search log. Zero pairs have both actual endpoint dates independently certified; six are partial and 25 unresolved. Source order alone cannot establish a date correction.

| Season | Previous source endpoint | Next source endpoint | Classification | References |
|---|---|---|---|---|
| 2016/2017 | 2016-09-27: Gazélec FC Ajaccio–Amiens SC (line 117) | 2016-09-19: RC Strasbourg–Red Star FC (line 122) | UNRESOLVED | None sufficient |
| 2016/2017 | 2017-02-21: RC Strasbourg–Tours FC (line 339) | 2017-01-27: FC Bourg-Péronnas–AC Ajaccio (line 344) | UNRESOLVED | I30 |
| 2017/2018 | 2018-01-23: Gazélec FC Ajaccio–Nîmes Olympique (line 307) | 2018-01-12: AJ Auxerre–Havre AC (line 312) | UNRESOLVED | I31 |
| 2017/2018 | 2018-01-30: RC Lens–FC Sochaux (line 337) | 2018-01-19: FC Bourg-Péronnas–Stade de Reims (line 342) | UNRESOLVED | None sufficient |
| 2017/2018 | 2018-03-13: FC Sochaux–AJ Auxerre (line 450) | 2018-03-09: AC Ajaccio–US Quevilly-Rouen (line 455) | UNRESOLVED | None sufficient |
| 2017/2018 | 2018-04-03: Tours FC–Valenciennes FC (line 467) | 2018-03-16: FC Bourg-Péronnas–Chamois Niortais (line 472) | UNRESOLVED | I32 |
| 2017/2018 | 2018-04-30: Stade de Reims–Havre AC (line 515) | 2018-04-13: AC Ajaccio–AS Nancy Lorraine (line 520) | UNRESOLVED | I33 |
| 2018/2019 | 2018-10-02: AS Béziers–RC Lens (line 85) | 2018-08-31: Gazélec FC Ajaccio–Red Star FC (line 90) | UNRESOLVED | I34 |
| 2018/2019 | 2019-01-29: FC Metz–AS Nancy Lorraine (line 308) | 2019-01-11: AC Ajaccio–AS Béziers (line 313) | UNRESOLVED | I36 |
| 2020/2021 | 2020-09-30: AC Ajaccio–USL Dunkerque (line 51) | 2020-09-19: Clermont Foot 63–Toulouse FC (line 56) | UNRESOLVED | I37 |
| 2020/2021 | 2020-11-24: Grenoble Foot 38–AS Nancy Lorraine (line 127) | 2020-10-31: Paris FC–SM Caen (line 132) | UNRESOLVED | D17 |
| 2020/2021 | 2020-12-15: Chamois Niortais–Grenoble Foot 38 (line 143) | 2020-11-07: Clermont Foot 63–EA Guingamp (line 148) | PARTIAL | D11, I39 |
| 2020/2021 | 2020-12-15: AS Nancy Lorraine–ESTAC Troyes (line 173) | 2020-11-28: Toulouse FC–Chamois Niortais (line 178) | PARTIAL | D11, I40 |
| 2020/2021 | 2021-01-27: FC Chambly–Chamois Niortais (line 307) | 2021-01-23: Clermont Foot 63–AJ Auxerre (line 312) | UNRESOLVED | None sufficient |
| 2020/2021 | 2021-04-14: Clermont Foot 63–Amiens SC (line 439) | 2021-03-19: FC Chambly–AC Ajaccio (line 444) | UNRESOLVED | D19, I41 |
| 2020/2021 | 2021-04-28: USL Dunkerque–Amiens SC (line 470) | 2021-04-10: Paris FC–ESTAC Troyes (line 475) | UNRESOLVED | I42 |
| 2020/2021 | 2021-05-04: Havre AC–Toulouse FC (line 515) | 2021-04-24: ESTAC Troyes–Grenoble Foot 38 (line 520) | UNRESOLVED | D18 |
| 2020/2021 | 2021-05-12: Toulouse FC–Pau FC (line 531) | 2021-05-01: Paris FC–Toulouse FC (line 536) | UNRESOLVED | D18, I43 |
| 2021/2022 | 2021-08-18: US Quevilly-Rouen–SC Bastia (line 37) | 2021-08-07: SM Caen–FC Sochaux (line 42) | UNRESOLVED | D15, I44 |
| 2021/2022 | 2021-08-25: AC Ajaccio–SM Caen (line 68) | 2021-08-21: Dijon FCO–Toulouse FC (line 73) | UNRESOLVED | None sufficient |
| 2021/2022 | 2021-09-14: AC Ajaccio–Paris FC (line 84) | 2021-08-28: Toulouse FC–Valenciennes FC (line 89) | UNRESOLVED | I45 |
| 2021/2022 | 2022-01-28: USL Dunkerque–Paris FC (line 306) | 2022-01-15: AS Nancy Lorraine–SC Bastia (line 311) | UNRESOLVED | D12, D16, I47 |
| 2021/2022 | 2022-02-01: Chamois Niortais–USL Dunkerque (line 324) | 2022-01-22: Havre AC–Rodez AF (line 329) | PARTIAL | D12, D16 |
| 2021/2022 | 2022-02-15: Grenoble Foot 38–Chamois Niortais (line 341) | 2022-02-05: Toulouse FC–Dijon FCO (line 346) | UNRESOLVED | I49 |
| 2022/2023 | 2022-10-04: EA Guingamp–Rodez AF (line 111) | 2022-09-10: AS Saint-Étienne–Girondins Bordeaux (line 116) | PARTIAL | D24 |
| 2022/2023 | 2023-03-14: Paris FC–Amiens SC (line 347) | 2023-02-18: Girondins Bordeaux–Paris FC (line 352) | PARTIAL | D13, D14, I51 |
| 2023/2024 | 2023-10-03: Girondins Bordeaux–SM Caen (line 110) | 2023-09-26: AJ Auxerre–FC Annecy (line 115) | UNRESOLVED | None sufficient |
| 2023/2024 | 2023-10-04: AS Saint-Étienne–USL Dunkerque (line 125) | 2023-09-30: ESTAC Troyes–AS Saint-Étienne (line 130) | UNRESOLVED | None sufficient |
| 2023/2024 | 2023-11-28: US Concarneau–Pau FC (line 200) | 2023-11-11: Girondins Bordeaux–FC Annecy (line 205) | UNRESOLVED | I52 |
| 2024/2025 | 2024-10-22: Pau FC–SC Bastia (line 122) | 2024-10-18: EA Guingamp–Pau FC (line 127) | UNRESOLVED | D20, I53 |
| 2024/2025 | 2024-12-03: AC Ajaccio–SC Bastia (line 152) | 2024-10-29: EA Guingamp–AC Ajaccio (line 157) | PARTIAL | D21, D22, D23 |

## Cancellation and club identities

Official LFP board minutes dated 2020-04-30 report 280 Ligue 2 matches played out of 380 scheduled. This corroborates the aggregate difference of 100 unplayed fixtures, not each individual scheduled date or pairing. All 100 null-score observations are retained, without a screening decision (D01, page 9).

The 47 literal labels and 29 exact Ligue 1 string matches remain diagnostic only. Official separate listings support keeping AC Ajaccio and Gazélec distinct. QRM’s club history supports a sporting project involving US Quevilly and Rouen, not an unconditional merged historical identity; Annecy’s club history describes rebuilding without certifying legal continuity. Four of ten identity-risk labels have partial documentary support; six remain unresolved. No reserve-label candidates were detected structurally, which does not prove historical identity equivalence. No mappings are applied.

| Label | Status | Finding |
|---|---|---|
| AC Ajaccio | PARTIAL | Separate Ajaccio club listing supported; no merger |
| AC Arles-Avignon | UNRESOLVED | Original label retained; no sufficient independent continuity evidence in bounded review |
| FC Annecy | PARTIAL | Club-authored sporting project/history supported; legal continuity not fully certified |
| Gazélec FC Ajaccio | PARTIAL | Separate Ajaccio club listing supported; no merger |
| Red Star FC | UNRESOLVED | Original label retained; no sufficient independent continuity evidence in bounded review |
| SC Bastia | UNRESOLVED | Original label retained; no sufficient independent continuity evidence in bounded review |
| Stade Brestois 29 | UNRESOLVED | Original label retained; no sufficient independent continuity evidence in bounded review |
| US Créteil-Lusitanos | UNRESOLVED | Original label retained; no sufficient independent continuity evidence in bounded review |
| US Quevilly-Rouen | PARTIAL | Club-authored sporting project/history supported; legal continuity not fully certified |
| Évian Thonon Gaillard | UNRESOLVED | Original label retained; no sufficient independent continuity evidence in bounded review |

## Evidence inventory and rights

The private inventory contains 60 curated references: 29 directly inspected and 31 index-only. Thirteen are official records, 18 authored/independent narratives and 29 compiled or of unestablished upstream independence. Access status and independence are separate: an official title in a search index is not a directly inspected decision. Participant reports establish their own reported events, not blanket historical independence. Access failures and limitations are retained rather than bypassed. The separate reversal-search log contains candidate metadata only and is not additional confirmed evidence.

Only bibliographic metadata and concise findings were retained, not complete external season datasets or article copies. OpenFootball notices and previous provenance remain intact. Historical corroboration does not establish redistribution or statistical-model-training permission; neither is cleared.

| ID | Access / independence | Title and exact URL | Publication date | Establishes / limitation |
|---|---|---|---|
| D01 | DIRECT / OFFICIAL_RECORD | [Conseil administration LFP, proces-verbal du 30 avril 2020](https://www.lfp.fr/assets/20200430_PV_Conseil_Administration_LFP_e824a457fa.pdf) | 2020-04-30 | Page 9 states 280 Ligue 2 matches played out of 380 planned; 100 unplayed follows arithmetic and source cancellation accounting.; Aggregate termination context only, not independent individual verification of the 100 fixture dates or pairings. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| D02 | DIRECT / OFFICIAL_RECORD | [Commission de discipline : la decision du 5 juin 2023](https://www.lfp.fr/article/commission-de-discipline-les-decisions-du-5-juin-2023) | 2023-06-05 | Bordeaux-Rodez of June 2 put under investigation; result not counted in standings pending June 12 decision.; Does not certify 0-1 as final numerical result or final outcome availability. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| D03 | DIRECT / OFFICIAL_RECORD | [Commission de discipline : les decisions du 12 juin 2023](https://www.lfp.fr/article/commission-de-discipline-les-decisions-du-12-juin-2023) | 2023-06-12 | Bordeaux loses the June 2 fixture by penalty; additional sanctions. Numerical awarded score not supplied in inspected decision.; First-instance decision; no automatic numerical replacement or June 2 availability follows. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| D04 | DIRECT / INDEPENDENT_NARRATIVE | [Communique du Club](https://backend.girondins.com/node/36805) | 2023-06-27 | Club accepts CNOSF conciliators proposal not to reverse LFP decision, says disciplinary/sporting sequence closed while reserving other proceedings.; Interested-party primary statement; not the signed CNOSF opinion, numerical homologation or exhaustive judicial-finality certificate. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| D05 | DIRECT / INDEPENDENT_NARRATIVE | [Ligue 2 : le CNOSF confirme les sanctions du match Bordeaux-Rodez](https://www.leparisien.fr/sports/football/ligue-2-le-cnosf-confirme-les-sanctions-du-match-bordeaux-rodez-27-06-2023-HIIZUFKDRRAG7OGJWU47QFY3LM.php) | 2023-06-27 | Contemporary report describes interruption after Rodez opener and June 27 conciliation/club acceptance.; Narrative corroboration of event and procedure; does not turn interruption score into numerical legal FT. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| I01 | INDEX_ONLY / INDEPENDENT_NARRATIVE | [La LFP donne match perdu aux Chamois apres la deprogrammation de Niort-Valenciennes](https://www.lequipe.fr/Football/Actualites/La-lfp-donne-match-perdu-aux-chamois-apres-la-deprogrammation-de-niort-valenciennes/1212247) | 2021-01-06 | Indexed report attributes 0-3 loss to LFP Competition Commission after December 22 deprogramming.; Direct open returned HTTP 403; primary decision, appeals and finality unavailable; source date is scheduled, not award availability. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| I02 | INDEX_ONLY / COMPILED_OR_UNESTABLISHED | [Ligue 2 : Niort perd son match face a Valenciennes sur tapis vert](https://www.leprogres.fr/sport/2021/01/06/ligue-2-niort-perd-son-match-face-a-valenciennes-sur-tapis-vert) | 2021-01-06 | Indexed report describes a nonplayed scheduled December 22 fixture, January 6 award and intention to challenge.; Direct fetch cache miss; possible shared reporting/agency upstream; no final appeal outcome independently established. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| D06 | DIRECT / INDEPENDENT_NARRATIVE | [Ligue 2 : Valenciennes et Beziers battent le record de buts en un match](https://www.leparisien.fr/sports/football/ligue-2-valenciennes-et-beziers-battent-le-record-de-buts-en-un-match-19-04-2019-8057043.php) | 2019-04-19 | Dated contemporary narrative records visiting Beziers winning 6-5 at Valenciennes after trailing 5-3; normal on-field scoring narrative.; No exhaustive legal finality, rights clearance or result-availability certification. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| D07 | DIRECT / INDEPENDENT_NARRATIVE | [Le jour ou... Le Gazelec a enfin gagne](https://www.lequipe.fr/Football/Article/Le-jour-ou-le-gazelec-a-enfin-gagne/619822) | 2015-12-28 | Coach retrospective explicitly locates Dijons 0-2 defeat at Mezzavia on September 19, 2014; interpreted as home Gazelec 2-0 Dijon.; Retrospective authored interview, not contemporaneous match sheet or exhaustive legal finality. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| D08 | DIRECT / INDEPENDENT_NARRATIVE | [La revanche !](https://www.redstar.fr/2016-01-22/les-pros/la-revanche/) | 2016-01-22 | Authored return-fixture preview explicitly recalls Laval-Red Star 2-1 on August 21, 2015 with lineups.; Uses retrospective match-aller passage; dynamic page footer refers to different return game and was not used. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| D09 | DIRECT / INDEPENDENT_NARRATIVE | [L AC Ajaccio s impose sans trembler face a Troyes (1-0)](https://www.corsenetinfos.corsica/L-AC-Ajaccio-s-impose-sans-trembler-face-a-Troyes-1-0_a74706.html) | 2023-11-11 | Dated authored report and match sheet establish Ajaccio home win 1-0 over Troyes.; No exhaustive legal finality, rights clearance or result-availability certification. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| D10 | DIRECT / INDEPENDENT_NARRATIVE | [Jessy Benet : des nerfs d acier pour le tireur de penalty patente](https://www.grenoblefoot.info/jessy-benet-des-nerfs-dacier-pour-le-tireur-de-penalty-patente/) | 2025-01-09 | Authored retrospective identifies Grenoble versus Rodez on December 20, 2019 through Benets penalty.; Does not establish full-time score; report is retrospective, not a new season dataset. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| D11 | DIRECT / INDEPENDENT_NARRATIVE | [Grenoble et Sochaux calent, Troyes nouveau leader](https://www.sofoot.com/breves/grenoble-et-sochaux-calent-troyes-nouveau-leader) | 2020-12-15 | Dated authored match narratives establish Niort-Grenoble 0-0 and Nancy-Troyes 2-3 played that evening.; Corroborates two individual events, not all round fixtures or original postponement causes. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| D12 | DIRECT / INDEPENDENT_NARRATIVE | [#CNFCUSLD : l USL Dunkerque s incline face a Niort](https://www.usldunkerque.com/cnfcusld-lusl-dunkerque-sincline-face-a-niort/) | 2022-02-01 | Participant-authored report and match sheet state Niort 2-0 Dunkerque on Tuesday February 1, round 21.; No exhaustive legal finality, rights clearance or result-availability certification. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| D13 | DIRECT / INDEPENDENT_NARRATIVE | [Le Paris FC deroule contre Amiens](https://www.sofoot.com/breves/le-paris-fc-deroule-contre-amiens) | 2023-03-14 | Authored report establishes March 14 game and pitch-related postponement.; Header and three listed scorers indicate 3-0 but one body sentence says 2-0. Internal documentary inconsistency recorded; no FT claim extracted and no corpus contradiction inferred. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| D14 | DIRECT / OFFICIAL_RECORD | [Paris FC – Amiens SC reprogramme le 14 mars](https://www.lfp.fr/article/paris-fc-programme-le-14-mars) | 2023-02-17 | Official round 23 rescheduling from February 11 to March 14 because of unsafe pitch.; Scheduling decision alone is not actual playing/completion or FT certification. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| D15 | DIRECT / OFFICIAL_RECORD | [Quevilly Rouen / SC Bastia et SC Bastia / AS Nancy Lorraine reportes](https://www.lfp.fr/article/quevilly-rouen-sc-bastia-et-sc-bastia-as-nancy-lorraine-reportes) | 2021-07-28 | Official COVID rescheduling of QRM-Bastia from July 31 to August 18.; Planned playing date, not completed-event score evidence. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| D16 | DIRECT / OFFICIAL_RECORD | [Chamois Niortais FC / USL Dunkerque reporte](https://www.lfp.fr/article/chamois-niortais-fc-usl-dunkerque-reporte) | 2022-01-12 | COVID rescheduling of round 21 from January 15 to February 1.; Actual completion separately corroborated by D12; no general availability policy. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| D17 | DIRECT / INDEPENDENT_NARRATIVE | [Grenoble-Nancy reporte](https://www.asnl.net/58/actualites/actualites/fiche/27205) | 2020-10-23 | Official participant announcement records LFP postponement of round 8 owing to Grenoble COVID cases.; Does not establish final November 24 playing date or score. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| D18 | DIRECT / OFFICIAL_RECORD | [Toulouse FC / Pau FC et Havre AC / Toulouse FC reportes](https://www.lfp.fr/article/toulouse-fc-pau-fc-et-havre-ac-toulouse-fc-reportes) | 2021-04-21 | Official COVID postponement of round 35 Toulouse-Pau scheduled April 24.; Does not establish actual May 12 completion date or score. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| D19 | DIRECT / OFFICIAL_RECORD | [Clermont Foot 63 / Amiens SC reporte au mercredi 7 avril 2021 a 19h](https://www.lfp.fr/article/clermont-foot-63-amiens-sc-reporte-au-mercredi-7-avril-2021-a-19h) | Not established | Official interim COVID rescheduling from March 13 to April 7.; Interim schedule differs from source actual-date candidate April 14; not a contradiction of actual date. Page publication metadata appears March 5; no final availability or decision date inferred. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| D20 | DIRECT / OFFICIAL_RECORD | [Pau FC – SC Bastia reprogrammee au mardi 22 octobre 2024](https://www.lfp.fr/article/pau-fc-sc-bastia-reprogrammee-au-mardi-22-octobre-2024) | 2024-10-09 | Strike-related transport blockage caused October 4 postponement; official rescheduling to October 22.; Scheduled rather than individually certified actual result date/score. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| D21 | DIRECT / OFFICIAL_RECORD | [Le derby AC Ajaccio-SC Bastia reprendra le mardi 3 decembre 2024](https://www.lfp.fr/article/le-derby-ac-ajaccio-sc-bastia-reprendra-le-mardi-3-decembre-2024) | 2024-10-30 | Commission sets December 3 resumption at minute 42, score 0-0.; Scheduled resumption, not itself final completion/score evidence. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| D22 | DIRECT / INDEPENDENT_NARRATIVE | [Un derby plus que particulier](https://sc-bastia.corsica/blogs/equipe-premiere/un-derby-plus-que-particulier) | 2024-12-02 | Club preview identifies October 26 original interruption, December 3 resumption, same match sheet and 0-0 at 42 minutes.; Pre-match article; completion separately supported by D23. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| D23 | DIRECT / INDEPENDENT_NARRATIVE | [Trente-huit jours plus tard, le derby entre l AC Ajaccio et Bastia se solde par un match nul](https://www.lequipe.fr/Football/Actualites/Trente-huit-jours-plus-tard-le-derby-entre-l-ac-ajaccio-et-bastia-se-solde-par-un-match-nul/1524395) | 2024-12-03 | Dated authored report confirms resumption/completion December 3 and final 0-0, following October 26 interruption.; Here the source date is corroborated as completion date, not original kickoff; no Phase 6 effective-date policy assigned. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| D24 | DIRECT / INDEPENDENT_NARRATIVE | [Ligue 2 : Guingamp rate le coche face a Rodez](https://www.lequipe.fr/Football/Actualites/Ligue-2-guingamp-rate-le-coche-face-a-rodez/1357578) | 2022-10-04 | Contemporary authored 0-0 match report identifies round 7 September 2 postponement caused by flight problem and actual October 4 game.; No exhaustive legal finality, rights clearance or result-availability certification. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| D25 | DIRECT / OFFICIAL_RECORD | [Commission de discipline : les decisions du 4 mai 2022](https://www.lfp.fr/article/commission-de-discipline-les-decisions-du-4-mai-2022) | 2022-05-04 | Official penalty defeat for Nancy-QRM of April 22 after incidents; newly discovered unannotated exceptional observation.; Inspected decision does not give numerical homologation or exhaustive appeals; source 0-3 is not certified as completed on-field FT. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| I03 | INDEX_ONLY / INDEPENDENT_NARRATIVE | [Nancy mene face a QRM, le match pour le maintien definitivement interrompu](https://www.lequipe.fr/Football/Actualites/Nancy-mene-face-a-qrm-le-match-interrompu/1329252) | 2022-04-22 | Indexed contemporary account describes interruption around minute 39 at 0-3.; Not directly inspected; interruption score is not automatically legal FT. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| D26 | DIRECT / INDEPENDENT_NARRATIVE | [Le projet QRM](https://qrm.fr/le-projet-qrm/) | Not established | Club identifies 2015 project rooted in US Quevilly, association with FC Rouen and subsequent Rouen departure.; Sporting/project account, not a licence to merge all Rouen identities or proof of every legal successor relationship. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| D27 | DIRECT / INDEPENDENT_NARRATIVE | [Notre Club / L histoire du FC Annecy](https://www.fc-annecy.fr/histoire) | Not established | Club history describes 1927 founding, 1993/94 administrative descent, rebuilding and 2022 Ligue 2 return.; Narrated sporting history, not comprehensive legal continuity or predecessor mapping. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| D28 | DIRECT / OFFICIAL_RECORD | [Proces-verbal Assemblee generale FFF du 24 juin 2017](https://media.fff.fr/uploads/document/a9df379f45b949bce508072ee2779886.pdf) | 2017-06-24 | Official assembly lists AC Ajaccio and Gazelec as separate L2 clubs; also lists several abbreviation forms.; Separate club listing only; no automated identity normalization or reserve-team inference. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| D29 | DIRECT / OFFICIAL_RECORD | [Tout savoir sur la reprise du match entre l AC Ajaccio et le SC Bastia](https://ligue1.com/fr/articles/l1_article_1327-tout-savoir-sur-la-reprise-du-match-entre-l-ac-ajaccio-et-le-sc-bastia) | 2024-12-02 | Explains October 26 kickoff and resumption rules for December 3.; Article says commission met November 30 whereas dated LFP D21 is October 30. Do not adopt that commission-date assertion or overwrite sources. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| I10 | INDEX_ONLY / COMPILED_OR_UNESTABLISHED | [Nimes Olympique : Il n y aura pas de passe de Troyes](https://www.objectifsud.fr/sports-gard/nimes-olympique/nimes-olympique-il-ny-aura-pas-de-passe-de-troyes-59938.php) | 2016-09-20 | Indexed lead agrees with source date, participants and numerical score; not direct corroboration.; Direct fetch timed out; indexed narrative only. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| I11 | INDEX_ONLY / COMPILED_OR_UNESTABLISHED | [AC Ajaccio bat Brest pour sa premiere a Francois-Coty (2-1)](https://www.alta-frequenza.corsica/football-ligue-2-lac-ajaccio-bat-brest-pour-sa-premiere-a-francois-coty-2-1) | 2017-08-04 | Indexed lead agrees with source date, participants and numerical score; not direct corroboration.; Direct fetch cache miss. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| I12 | INDEX_ONLY / COMPILED_OR_UNESTABLISHED | [Resultats Ligue 2, journee 14](https://www.footmercato.net/france/ligue-2/2018-2019/resultat/8856022225809686746-journee-14) | Not established | Indexed lead agrees with source date, participants and numerical score; not direct corroboration.; Compiled feed; upstream independence unestablished. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. Publication date not established; any indexed fixture date is distinct. |
| I13 | INDEX_ONLY / COMPILED_OR_UNESTABLISHED | [Le Havre-Clermont 0-0](https://www.foot-direct.com/live/4818971162094440020-le-havre-vs-clermont) | Not established | Indexed lead agrees with source date, participants and numerical score; not direct corroboration.; Compiled feed; upstream independence unestablished. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. Publication date not established; any indexed fixture date is distinct. |
| I14 | INDEX_ONLY / COMPILED_OR_UNESTABLISHED | [Net vainqueur de Quevilly, le Paris FC consolide sa deuxieme place](https://www.leparisien.fr/sports/football/ligue-2-net-vainqueur-de-quevilly-3-0-le-paris-fc-consolide-sa-2e-place-12-02-2022-AL2SAKQLF5HAXKSHAZOIIG4CFQ.php) | 2022-02-12 | Indexed lead agrees with source date, participants and numerical score; not direct corroboration.; Direct fetch cache miss. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| I15 | INDEX_ONLY / COMPILED_OR_UNESTABLISHED | [Chamois Niortais-Nimes Olympique (1-1), resume](https://www.youtube.com/watch?v=XfFAN0E7mK4) | Not established | Indexed lead agrees with source date, participants and numerical score; not direct corroboration.; Official-channel indexed metadata, direct fetch failed; video publication and playing date must be distinguished. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. Publication date not established; any indexed fixture date is distinct. |
| I16 | INDEX_ONLY / COMPILED_OR_UNESTABLISHED | [Rodez 1-2 Guingamp, resume](https://www.lequipe.fr/Football/match-direct/ligue-2/2024-2025/rodez-guingamp-live/656434) | Not established | Indexed lead agrees with source date, participants and numerical score; not direct corroboration.; Compiled match feed; independence not established. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. Publication date not established; any indexed fixture date is distinct. |
| I30 | INDEX_ONLY / COMPILED_OR_UNESTABLISHED | [RC Strasbourg – Tours FC: indexed event/scheduling lead](https://www.football365.fr/l2-match-retard-remonter-podium-strasbourg-passe-etats-3082978.html) | Not established | Bounded search located a fixture/date or scheduling lead for this source-bound case.; No direct independent four-fact confirmation extracted. Match preview/feed/automated text may not certify final score or actual date. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| I31 | INDEX_ONLY / COMPILED_OR_UNESTABLISHED | [Gazélec FC Ajaccio – Nîmes Olympique: indexed event/scheduling lead](https://www.footmercato.net/live/5085155055900420705-gazelec-ajaccio-vs-nimes) | Not established | Bounded search located a fixture/date or scheduling lead for this source-bound case.; No direct independent four-fact confirmation extracted. Match preview/feed/automated text may not certify final score or actual date. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| I32 | INDEX_ONLY / COMPILED_OR_UNESTABLISHED | [Tours FC – Valenciennes FC: indexed event/scheduling lead](https://www.worldfootball.net/match-report/co72/france-ligue-2/ma8406959/tours-fc_valenciennes-fc/) | Not established | Bounded search located a fixture/date or scheduling lead for this source-bound case.; No direct independent four-fact confirmation extracted. Match preview/feed/automated text may not certify final score or actual date. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| I33 | INDEX_ONLY / COMPILED_OR_UNESTABLISHED | [Stade de Reims – Havre AC: indexed event/scheduling lead](https://www.sofoot.com/breves/le-havre-fait-tomber-reims-et-continue-de-croire-a-la-montee) | Not established | Bounded search located a fixture/date or scheduling lead for this source-bound case.; No direct independent four-fact confirmation extracted. Match preview/feed/automated text may not certify final score or actual date. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| I34 | INDEX_ONLY / COMPILED_OR_UNESTABLISHED | [AS Béziers – RC Lens: indexed event/scheduling lead](https://www.lensois.com/l2-j5-beziers-rc-lens-0-0-le-racing-assure-le-minimum-beziers/) | Not established | Bounded search located a fixture/date or scheduling lead for this source-bound case.; No direct independent four-fact confirmation extracted. Match preview/feed/automated text may not certify final score or actual date. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| I35 | INDEX_ONLY / COMPILED_OR_UNESTABLISHED | [Havre AC – Valenciennes FC: indexed event/scheduling lead](https://www.sofoot.com/breves/le-havre-simpose-au-terme-dun-match-fou) | Not established | Bounded search located a fixture/date or scheduling lead for this source-bound case.; No direct independent four-fact confirmation extracted. Match preview/feed/automated text may not certify final score or actual date. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| I36 | INDEX_ONLY / COMPILED_OR_UNESTABLISHED | [FC Metz – AS Nancy Lorraine: indexed event/scheduling lead](https://www.worldfootball.net/match-report/co72/france-ligue-2/ma8739968/fc-metz_as-nancy-lorraine/) | Not established | Bounded search located a fixture/date or scheduling lead for this source-bound case.; No direct independent four-fact confirmation extracted. Match preview/feed/automated text may not certify final score or actual date. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| I37 | INDEX_ONLY / COMPILED_OR_UNESTABLISHED | [AC Ajaccio – USL Dunkerque: indexed event/scheduling lead](https://www.20minutes.fr/sport/football/2874359-20200930-ligue-2-3eme-journee-succes-1-0-de-l-ac-ajaccio-face-a-dunkerque) | Not established | Bounded search located a fixture/date or scheduling lead for this source-bound case.; No direct independent four-fact confirmation extracted. Match preview/feed/automated text may not certify final score or actual date. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| I39 | INDEX_ONLY / COMPILED_OR_UNESTABLISHED | [Chamois Niortais – Grenoble Foot 38: indexed event/scheduling lead](https://www.lequipe.fr/Football/match-direct/ligue-2/2020-2021/niort-grenoble-live/477621) | Not established | Bounded search located a fixture/date or scheduling lead for this source-bound case.; No direct independent four-fact confirmation extracted. Match preview/feed/automated text may not certify final score or actual date. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| I40 | INDEX_ONLY / COMPILED_OR_UNESTABLISHED | [AS Nancy Lorraine – ESTAC Troyes: indexed event/scheduling lead](https://www.youtube.com/watch?v=776wCbBLAaY) | Not established | Bounded search located a fixture/date or scheduling lead for this source-bound case.; No direct independent four-fact confirmation extracted. Match preview/feed/automated text may not certify final score or actual date. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| I41 | INDEX_ONLY / COMPILED_OR_UNESTABLISHED | [Clermont Foot 63 – Amiens SC: indexed event/scheduling lead](https://www.20minutes.fr/sport/football/3021295-20210414-ligue-2-29eme-journee-3-0-pour-le-clermont-foot-contre-amiens-au-stade-gabriel-montpied) | Not established | Bounded search located a fixture/date or scheduling lead for this source-bound case.; No direct independent four-fact confirmation extracted. Match preview/feed/automated text may not certify final score or actual date. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| I42 | INDEX_ONLY / COMPILED_OR_UNESTABLISHED | [USL Dunkerque – Amiens SC: indexed event/scheduling lead](https://www.lequipe.fr/Football/match-direct/ligue-2/2020-2021/dunkerque-amiens-live/477835) | Not established | Bounded search located a fixture/date or scheduling lead for this source-bound case.; No direct independent four-fact confirmation extracted. Match preview/feed/automated text may not certify final score or actual date. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| I43 | INDEX_ONLY / COMPILED_OR_UNESTABLISHED | [Toulouse FC – Pau FC: indexed event/scheduling lead](https://www.lequipe.fr/Football/match-direct/ligue-2/2020-2021/toulouse-pau-live/477884) | Not established | Bounded search located a fixture/date or scheduling lead for this source-bound case.; No direct independent four-fact confirmation extracted. Match preview/feed/automated text may not certify final score or actual date. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| I44 | INDEX_ONLY / COMPILED_OR_UNESTABLISHED | [US Quevilly-Rouen – SC Bastia: indexed event/scheduling lead](https://www.lequipe.fr/Football/Actualites/Bastia-s-impose-a-quevilly-rouen-en-ligue-2/1279057) | Not established | Bounded search located a fixture/date or scheduling lead for this source-bound case.; No direct independent four-fact confirmation extracted. Match preview/feed/automated text may not certify final score or actual date. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| I45 | INDEX_ONLY / COMPILED_OR_UNESTABLISHED | [AC Ajaccio – Paris FC: indexed event/scheduling lead](https://www.lequipe.fr/Football/Actualites/Ligue-2-l-ac-ajaccio-bat-le-paris-fc-en-fin-de-match/1285518) | Not established | Bounded search located a fixture/date or scheduling lead for this source-bound case.; No direct independent four-fact confirmation extracted. Match preview/feed/automated text may not certify final score or actual date. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| I46 | INDEX_ONLY / COMPILED_OR_UNESTABLISHED | [SM Caen – Chamois Niortais: indexed event/scheduling lead](https://www.smcaen.fr/calendrier-resultat/2021-2022/premiere/complet) | Not established | Bounded search located a fixture/date or scheduling lead for this source-bound case.; No direct independent four-fact confirmation extracted. Match preview/feed/automated text may not certify final score or actual date. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| I47 | INDEX_ONLY / COMPILED_OR_UNESTABLISHED | [USL Dunkerque – Paris FC: indexed event/scheduling lead](https://www.leparisien.fr/sports/football/ligue-2-malgre-son-calendrier-decousu-le-paris-fc-a-tout-a-gagner-a-dunkerque-28-01-2022-XQ5RO4BKGBFBVLKKFJJO7QMAIA.php) | Not established | Bounded search located a fixture/date or scheduling lead for this source-bound case.; No direct independent four-fact confirmation extracted. Match preview/feed/automated text may not certify final score or actual date. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| I49 | INDEX_ONLY / COMPILED_OR_UNESTABLISHED | [Grenoble Foot 38 – Chamois Niortais: indexed event/scheduling lead](https://www.sofoot.com/breves/vainqueur-de-niort-grenoble-nest-plus-relegable-ligue-2-j22-1-0) | Not established | Bounded search located a fixture/date or scheduling lead for this source-bound case.; No direct independent four-fact confirmation extracted. Match preview/feed/automated text may not certify final score or actual date. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| I51 | INDEX_ONLY / COMPILED_OR_UNESTABLISHED | [Paris FC – Amiens SC: indexed event/scheduling lead](https://www.lequipe.fr/Football/Actualites/Le-paris-fc-surclasse-amiens-en-ligue-2/1385878) | Not established | Bounded search located a fixture/date or scheduling lead for this source-bound case.; No direct independent four-fact confirmation extracted. Match preview/feed/automated text may not certify final score or actual date. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| I52 | INDEX_ONLY / COMPILED_OR_UNESTABLISHED | [US Concarneau – Pau FC: indexed event/scheduling lead](https://www.sofoot.com/breves/pau-simpose-tout-en-realisme-a-concarneau) | Not established | Bounded search located a fixture/date or scheduling lead for this source-bound case.; No direct independent four-fact confirmation extracted. Match preview/feed/automated text may not certify final score or actual date. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |
| I53 | INDEX_ONLY / COMPILED_OR_UNESTABLISHED | [Pau FC – SC Bastia: indexed event/scheduling lead](https://www.matchendirect.fr/live-score/pau-sc-bastia_dpq69xjt0dj79l7yksuqpizo4.html) | Not established | Bounded search located a fixture/date or scheduling lead for this source-bound case.; No direct independent four-fact confirmation extracted. Match preview/feed/automated text may not certify final score or actual date. Bibliographic references/paraphrases only; no licence to redistribute full content or train models established. |

The machine-readable inventory additionally retains issuing organization/author where known, access date, explicit supported facts and source-bound audit IDs.

## Reproducibility, preservation and tests

Run `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python -B scripts/verify_ligue2_review.py` from the repository root. Existing saved outputs are compared before any write; changed evidence fails explicitly. The script verifies protected fingerprints, exact queue bindings, frozen samples, evidence access/independence, context memberships and source-bound special cases. Synthetic tests exercise tampering, duplicated JSON keys, context-only overclaiming, index-only claims and unauthorized policy fields.

Fresh tests use the preserved external Python 3.13.12 environment because system Python has no pytest; no dependency installations or original .venv changes were made. Fresh execution completed successfully:

| Test scope | Passed | Failed / unverified |
|---|---:|---:|
| Historical-review synthetic tests | 43 | 0 |
| All focused Ligue 2 tests | 180 | 0 |
| Non-UI regression suite | 1,472 | 0 |
| App/launcher tests | 7 | 0 |
| Full repository suite | 1,479 | 0 |

These are overlapping runs, not additive test totals. Each ran in a bounded subprocess with bytecode and pytest caches disabled. Logs, JUnit XML and exit statuses are preserved privately in `verification_phase5/`.

An independent Python process regenerated both outputs in external temporary storage. Both matched saved bytes and SHA-256:

| Output | Bytes | SHA-256 |
|---|---:|---|
| `phase5_evidence_assessment.json` | 87,788 | `6a1329be56cb00bc3a8f8cba5c6eeca81421eebcb58bbaf9470e80341da68daa` |
| `phase5_fixture_registry.json` | 647,758 | `02f79011178876ffe1765f556864989c78892307d76d1ee002641d462b6b52cd` |

The private `phase5_reproducibility.json` preserves comparisons and the temporary destination. This verifies deterministic assessment from the frozen evidence ledger; it does not independently recertify the external publications.

Protected checks cover 676 previous private files and 185 previous public files, nested Phase 2/3 baselines, and 108 Phase 2–4 entries. The original planning-log prefix is hashed separately so only append-only additions are permitted. No application, promotional, source or prior assessment file was changed. Private artifacts are Git-ignored and nothing is staged.

Public Phase 5 changes: `scripts/verify_ligue2_review.py`, `tests/test_ligue2_review.py`, this report, and an append-only `PLANNING_LOG.md` entry. Private Phase 5 files: protected baseline, frozen selection, evidence inventory, authored review ledger, reversal-search metadata, generated evidence assessment and fixture registry, plus verification receipts.

## Proposed Phase 6 agenda — no decisions implemented

1. Decide treatment of Niort–Valenciennes, Bordeaux–Rodez and newly identified Nancy–QRM, separating played score, administrative decision, numerical homologation, appeal finality and availability. Missing primary evidence must stay explicit.
2. Decide kickoff/completion semantics for Ajaccio–Bastia and any additional interruption cases; never infer availability from source order or administrative scheduled dates.
3. Preserve uncertainty for all 25 outliers and 31 reversals; do not automatically exclude long-span members or uncorroborated samples.
4. Formalize the 100 cancelled null-score observations separately from completed results, without inventing outcomes.
5. Keep team identity, technical acceptance, historical confidence, chronology, training eligibility and licensing as distinct classifications.
6. Preserve the 24-season 1990/91–2013/14 acquisition gap, unresolved RSSSF 1998/99 issues and separate incomplete 2025/26 source (306 slots, 116 scored, 190 unscored). None entered this review population.

Phase 5 completes the bounded evidence review, not historical certification. Await approval before implementing Phase 6.
