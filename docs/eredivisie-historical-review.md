# Eredivisie — Phase 5 historical evidence review

Review date: 2026-11-23. Original toto worktree, `feature/data-collection`, HEAD `4f8c64433cf6168a06dbde0102e822ce6d2eeffa`.

**Phase 5 evidence collection and assessment only.** No authoritative source selection, data corrections, supplemental results, HOLD OUT/NOT PLAYED classifications, eligibility rules, standardized datasets or model training were implemented. The bounded review is documented with explicit gaps; it is not dataset-wide historical certification.

## Population, selection and counting

The new verifier re-runs the independent Phase 4 raw parser against immutable originals and compares all four saved artifacts before validating the evidence registry. Original records retain file/revision/blob/SHA-256, physical line bindings, literal teams/date/FT/annotations and source-observation audit IDs. Queue membership and every category are compared against newly regenerated structural assessments. The existing planning prefix and every frozen Phase 2–4 artifact are protected.

| Population | Count |
|---|---:|
| Target seasons, 1990/91–2025/26 | 36 |
| Historical target observations | 10,636 |
| Modern observations | 2,448 |
| Target source observations | 13,084 |
| Score-bearing / unscored source observations | 13,009 / 75 |
| Conditional scored overlaps | 2,068 pairs |
| Conditional unique scored identities / all slots | 10,941 / 11,016 |
| Flagged source observations / conditional groups | 410 / 395 |
| Registry observations / conditional groups | 452 / 430 |
| Targeted fixture research: observations / conditional groups | 53 / 45 |
| Context-only observations | 399 |
| Conditional groups with no targeted fixture research | 385 |

Groups use only existing season-scoped diagnostic correspondences; they are not new global club aliases or certified entity merges. Context-only observations can share a group with a targeted observation, so observation and group counts must not be added across axes. The 452-entry registry is the union of all 410 flags, the 36 ordinary samples and additional bound exception observations; it is not a claim of direct research on 452 fixtures.

An ordinary scored fixture is selected from each season by earliest source date, then literal home, away and source lexicographic order, excluding every Phase 4 review flag. This fixed rule was saved before sample research. The full source record is saved, and selection is independently recomputed. Search leads were sought for all 36 selected fixtures; direct inspection was attempted selectively. A successful search snippet is never treated as an inspected document body. Of the samples, **9 have directly corroborated core facts and 27 remain unverified**. No replacement sample was chosen to improve the apparent verification rate.

Core facts mean teams, source-aligned match date, full-time score and competition/season context. Even FULLY CORROBORATED does not establish exhaustive disciplinary finality, intraday availability, source rights or season completeness. Cross-source conflicts and chronological semantics remain separate fields. Index-only evidence can support a research lead, not direct fact certification.

| Evidence assessment | Source observations | Conservative conditional groups |
|---|---:|---:|
| FULLY CORROBORATED | 18 | 13 |
| PARTIALLY CORROBORATED | 196 | 193 |
| CONTRADICTED | 1 | 1 |
| UNRESOLVED | 237 | 223 |

Group classification is conservative: any contradicted source observation makes the group a source-conflict group; a group is fully corroborated only if all its registry observations have full core-fact corroboration. This is a source-evidence assessment, not a processing disposition.

## Priority source conflicts and completion chronology

| Fixture | Original source values | Evidence finding | Phase 6 recommendation, not implemented |
|---|---|---|---|
| Groningen–Ajax 2022/23 | Historical 2023-05-14; modern 2023-05-16; both 2–3 | KNVB decision: May 14 stopped at 0–0 after nine minutes; club report: completed May 16 at 2–3. Both source dates describe legitimate event dates. | Preserve kickoff May 14 and completion May 16 separately; completed result must not become available on May 14. |
| NEC–Vitesse 2023/24 | Historical 2023-10-01 1–3; modern same date 1–2 | Direct NEC final display and narrative plus NOS report support 1–3. NEC timeline shows 1–2 at minute 89 and 1–3 at 90+4. | Explicit score-source decision needed. Evidence strongly supports 1–3; exact reason OpenFootball retained 1–2 is unproven. |
| NAC–Heerenveen 2025/26 | Modern line 509, 2026-05-10, null, `[cancelled]` | Direct NAC and NOS narratives establish May 10 fireworks interruption at 2–0 and May 11 completion at 2–0 in Heerenveen; NAC remains designated home. KNVB direct response was maintenance mode. | Decide separately whether source-bound supplementation is permitted with adequate provenance/rights, or preserve a HOLD OUT. Do not classify automatically as NOT PLAYED. |

Groningen sources: [G1](https://www.knvb.nl/nieuws/betaald-voetbal/eredivisie/67697/fc-groningen-ajax-op-dinsdag-16-mei-uitgespeeld), [G2](https://www.ajax.nl/artikelen/verslag-ajax-wint-nipt-in-groningen/). NEC sources: [N1](https://www.nec-nijmegen.nl/wedstrijden/wedstrijd/nec-vitesse-2023-10-01z-101500z.htm), [N2](https://www.nec-nijmegen.nl/sitewide/vraag/n.e.c.-verliest-de-gelderse-derby.htm), [N3](https://nos.nl/artikel/2492493-vitesse-scoort-weer-eens-en-wint-opnieuw-gelderse-derby-in-nijmegen). NAC sources: [B1](https://www.nac.nl/nieuws/winst-in-twee-delen-voor-gedegradeerd-nac), [B2](https://nos.nl/artikel/2613947-gedegradeerd-nac-pakt-in-heerenveen-drie-punten-geen-goals-meer-in-restant-duel), [B3](https://www.knvb.nl/nieuws/betaald-voetbal/vriendenloterij-eredivisie/71803/wedstrijd-nac-breda-sc-heerenveen-definitief).

The NEC search index selected an intermediate 1–2 from the same matchcenter whose directly inspected final result is 1–3. The temporary on-field interruption is also reported in contemporary coverage. This illustrates why snippets and intermediate states cannot decide final scores. No later administrative score change was established by the inspected material; absence of such a discovery is not exhaustive legal certification. The club feed's upstream provenance is unestablished, whereas authored club and broadcaster narratives provide a different kind of evidence.

| Interrupted fixture | Initial event | Completion supported/reported | Final score | Direct evidence and limits |
|---|---|---|---|---|
| Ajax–Feyenoord | 2023-09-24 | 2023-09-27 | 0–4 | Club narrative directly inspected; KNVB direct request maintenance page. Both archives store completion date. |
| RKC–Ajax | 2023-09-30 | 2023-12-06 | 2–3 | Official league scheduling notice and NOS completion report directly inspected. Keeper injury interruption. Both archives store completion date. |
| AZ–NEC | 2023-10-29 | 2023-12-06 | 1–2 | Direct NEC matchcenter plus direct VI completion report; original medical-emergency report indexed. Both archives store completion date. |
| Feyenoord–VVV | 2018-11-04 | 2018-12-06, scheduled replay | Source 4–1 | KNVB interruption and NOS replay scheduling directly inspected; final score is still an unverified completion lead here. |
| Vitesse–Sparta | 2022-03-04 | 2022-04-19, indexed completion | Source 0–1 | Primary scheduling and contemporary completion leads; direct completion request cache miss. Partial evidence only. |
| Heracles–Groningen | 2024-12-21 | 2025-01-28 | 1–1 | Direct NOS report establishes delayed completion with no further goals. Both archives store completion date. |

References: [A1](https://www.ajax.nl/artikelen/verslag-ajax-verliest-klassieker-in-eigen-huis), [A2](https://www.knvb.nl/nieuws/betaald-voetbal/competitiezaken/68180/ajax-%E2%80%93-feyenoord-wordt-27-september-uitgespeeld), [R1](https://nos.nl/artikel/2500620-ajax-trekt-zege-in-duel-van-tien-minuten-bij-rkc-waalwijk-over-de-streep), [R2](https://eredivisie.nl/nieuws/rkc-waalwijk-ajax-uitgespeeld-op-woensdag-6-december/), [Z1](https://www.nec-nijmegen.nl/wedstrijden/wedstrijd/az-nec-2023-12-06z-180000z.htm), [Z2](https://az.nl/inside-az/nieuws/2023/oktober/az-nec-gestaakt), [Z3](https://www.vi.nl/nieuws/nec-houdt-voorsprong-op-az-vast-in-restant-van-in-oktober-gestaakt-duel), [Z4](https://www.knvb.nl/node/68342), [F1](https://www.knvb.nl/nieuws/betaald-voetbal/eredivisie/51160/feyenoord-%E2%80%93-vvv-gestaakt-vanwege-uitvallen-lichtmasten), [F2](https://nos.nl/artikel/2258030-feyenoord-vvv-op-donderdag-6-december-overgespeeld), [VS](https://vitesse.nl/nieuws/2022/restant-vitesse-vs-sparta-rotterdam-op-dinsdag-19-april-uitgespeeld), [VS2](https://www.nhnieuws.nl/nieuws/n76469/sparta-houdt-stand-in-resterende-374-seconden-en-boekt-belangrijke-zege-op-vitesse), [HG](https://nos.nl/artikel/2553645-groningen-en-heracles-komen-in-resterende-21-minuten-niet-tot-scoren).

The earliest defensible completed-result date recommendations are May 16 for Groningen–Ajax, May 11 for NAC–Heerenveen, September 27 for Ajax–Feyenoord, December 6 for RKC–Ajax and AZ–NEC, and January 28 for Heracles–Groningen. Original kickoff dates remain distinct. These are recommendations, not effective-availability policies. Exact final-whistle timestamps and later administrative finality are not exhaustively established. Historical backtesting must eventually respect completion, rather than use final scores at initial kickoff.

## 2019/20 termination and cancellation representations

The directly inspected KNVB notice dated **2020-04-24** stops the competition, awards no championship and orders no promotion/relegation, while using existing standings for European allocation. PSV's contemporary report corroborates the retained fourth place. This does not support describing all played results as retrospectively annulled. References: [T1](https://www.knvb.nl/node/59905), [T2](https://www.psv.nl/media/artikel/psv-eindigt-eredivisie-als-vierde).

Independent research methods also directly report **232 completed matches out of 306**, based on paired official club commentaries; their match statistics came through VI/Opta, which is disclosed rather than treated as fully independent federation data: [T3](https://pure.uva.nl/ws/files/89216271/Burgers_Beukeboom_Smith_Van_Biemen_2023_.pdf). This is separate corroboration of the aggregate, not a new fixture dataset or individual legal record.

The originals independently reconcile 232 scored historical rows, 74 missing historical pairings and the corresponding 74 explicit modern null-score cancellation slots. Historical absence is not a cancellation annotation. The 74 identities are not double-counted across sources. The two April slots contributing to the wide round are unscored dates in a stopped competition, not future completed-result observations. No final NOT PLAYED policy is implemented, and no fixture-by-fixture signed cancellation/finality ledger was inspected.

## All 25 wide-round contexts

All 225 members retain source-bound IDs in the private registry. The table assesses the explanation and evidence available for the context; it does not certify every member fixture. 13 contexts have partial corroboration; 12 remain unresolved under the direct-inspection rule.

| Season / round | First–last source dates | Assessment | Finding and references |
|---|---|---|---|
| 2018/2019 / 11 | 2018-11-02 – 2018-12-06 | Partial/context only | Floodlight interruption/replay; original event directly corroborated, final-date/score context indexed. [F1](https://www.knvb.nl/nieuws/betaald-voetbal/eredivisie/51160/feyenoord-%E2%80%93-vvv-gestaakt-vanwege-uitvallen-lichtmasten), [F2](https://nos.nl/artikel/2258030-feyenoord-vvv-op-donderdag-6-december-overgespeeld), [F3](https://nos.nl/liveblog/2262325-larsson-heeft-de-vorm-gevonden-en-helpt-feyenoord-aan-eenvoudige-zege) |
| 2019/2020 / 4 | 2019-08-24 – 2019-09-26 | Unresolved | European postponements documented for PSV-Groningen; other two diagnostic fixtures not independently certified. [S19](https://www.vi.nl/nieuws/fraaie-tiki-taka-goal-hoogtepunt-bij-zege-psv-op-groningen) |
| 2019/2020 / 22 | 2020-02-07 – 2020-04-09 | Partial/context only | Postponed April slots overtaken by season termination; null fields are not completed results. [T1](https://www.knvb.nl/node/59905), [T2](https://www.psv.nl/media/artikel/psv-eindigt-eredivisie-als-vierde) |
| 2020/2021 / 1 | 2020-09-12 – 2020-12-27 | Partial/context only | Official body gives December27 rescheduling for AZ European preparation; contradictory September27 image caption preserved. [U1](https://www.knvb.nl/nieuws/betaald-voetbal/eredivisie/61553/nieuwe-datum-voor-fc-utrecht-az) |
| 2020/2021 / 4 | 2020-10-02 – 2020-10-21 | Unresolved | Coronavirus postponement of RKC-PEC; completion requires direct corroboration. [S20](https://www.omroepbrabant.nl/nieuws/3271547/na-elf-weken-zonder-positieve-test-opeens-veel-coronagevallen-bij-rkc-dit-is-enorm-schrikken) |
| 2020/2021 / 21 | 2021-02-05 – 2021-04-22 | Unresolved | Weather postponement context; several later dates present; not all four diagnostic fixtures individually verified. [S21](https://www.knvb.nl/downloads/bestand/23429/conceptprogramma-eredivisie-2021), [S21b](https://nos.nl/artikel/2377817-ajax-morst-punten-tegen-utrecht-in-aanloop-naar-35ste-landstitel) |
| 2021/2022 / 2 | 2021-08-20 – 2021-12-02 | Unresolved | AZ-Fortuna postponed; exact original decision body and completion not directly inspected. [S22](https://www.voetbalprimeur.nl/nieuws/996047/knvb-schuift-opnieuw-met-aanvangstijden-zes-wedstrijden-tien-clubs-betrokken.html) |
| 2021/2022 / 4 | 2021-09-11 – 2021-12-01 | Partial/context only | Feyenoord-Heracles moved September12 to December1; KNVB direct cache miss. [S22b](https://www.knvb.nl/node/64502), [S22d](https://nos.nl/artikel/2407827-winnend-feyenoord-moet-hard-werken-tegen-heracles-maar-heeft-sinisterra) |
| 2021/2022 / 23 | 2022-02-19 – 2022-04-16 | Partial/context only | Fortuna-Sparta postponed for storm Eunice; completion not individually verified. [S22c](https://eredivisie.nl/nieuws/wedstrijd-fortuna-sittard-sparta-rotterdam-afgelast-vanwege-storm-eunice/) |
| 2021/2022 / 25 | 2022-03-05 – 2022-04-19 | Unresolved | Vitesse-Sparta interruption March4 and reported completion April19; direct final report unavailable. [VS](https://vitesse.nl/nieuws/2022/restant-vitesse-vs-sparta-rotterdam-op-dinsdag-19-april-uitgespeeld), [VS2](https://www.nhnieuws.nl/nieuws/n76469/sparta-houdt-stand-in-resterende-374-seconden-en-boekt-belangrijke-zege-op-vitesse) |
| 2022/2023 / 25 | 2023-03-11 – 2023-04-19 | Unresolved | GoAhead-RKC March10 snow postponement; 403 respected; source April19 completion remains individually unverified. [S23](https://www.ga-eagles.nl/go-ahead-eagles-rkc-waalwijk-op-laatste-moment-afgelast/) |
| 2023/2024 / 3 | 2023-08-26 – 2023-11-02 | Partial/context only | Ajax-Volendam moved to November2 to accommodate Klassieker resumption; other three round3 deferred matches not fully verified. [V24](https://www.ajax.nl/artikelen/ajax-op-2-november-tegen-fc-volendam) |
| 2023/2024 / 7 | 2023-09-30 – 2023-12-06 | Partial/context only | RKC-Ajax September30 to December6 keeper injury interruption, completed 2-3. [R1](https://nos.nl/artikel/2500620-ajax-trekt-zege-in-duel-van-tien-minuten-bij-rkc-waalwijk-over-de-streep), [R2](https://eredivisie.nl/nieuws/rkc-waalwijk-ajax-uitgespeeld-op-woensdag-6-december/) |
| 2023/2024 / 10 | 2023-10-27 – 2023-12-06 | Partial/context only | AZ-NEC October29 to December6 medical interruption, completed 1-2. [Z1](https://www.nec-nijmegen.nl/wedstrijden/wedstrijd/az-nec-2023-12-06z-180000z.htm), [Z2](https://az.nl/inside-az/nieuws/2023/oktober/az-nec-gestaakt), [Z3](https://www.vi.nl/nieuws/nec-houdt-voorsprong-op-az-vast-in-restant-van-in-oktober-gestaakt-duel), [Z4](https://www.knvb.nl/node/68342) |
| 2024/2025 / 3 | 2024-08-24 – 2024-09-18 | Partial/context only | Two delayed round3 dates explicitly set September17/18 in official league notice. [C24](https://eredivisie.nl/nieuws/7-wedstrijdwijzigingen-in-september-en-oktober/) |
| 2024/2025 / 4 | 2024-08-30 – 2024-10-30 | Unresolved | Police-related Klassieker postponement; exact final score not researched in this context. [S24b](https://www.knvb.nl/node/69526) |
| 2024/2025 / 5 | 2024-09-14 – 2024-12-04 | Unresolved | Police-action postponement Ajax-Utrecht, scheduled December4; final score not certified. [S24c](https://nos.nl/artikel/2538560-ajax-en-fc-utrecht-halen-afgelast-eredivisieduel-in-op-4-december) |
| 2024/2025 / 17 | 2024-12-20 – 2025-01-28 | Partial/context only | Heracles-Groningen December21 interruption, January28 completion 1-1. [HG](https://nos.nl/artikel/2553645-groningen-en-heracles-komen-in-resterende-21-minuten-niet-tot-scoren) |
| 2024/2025 / 20 | 2025-01-24 – 2025-02-23 | Unresolved | European preparation deferments for Ajax, Feyenoord and Twente; no claim every endpoint score verified. [S25](https://www.vi.nl/nieuws/waarom-er-maar-vier-duels-op-het-programma-staan-dit-eredivisie-weekend) |
| 2024/2025 / 25 | 2025-03-07 – 2025-04-02 | Partial/context only | European preparation explanation for AZ-RKC and Feyenoord-Groningen; indexed evidence, no primary decision body. [S25b](https://www.vi.nl/nieuws/az-loopt-pijnlijke-averij-op-in-inhaalduel-met-rkc), [S25c](https://sportnieuws.nl/voetbal/nieuws/feyenoord-staat-voor-cruciaal-duel-om-champions-league-miljoenen-jacht-om-plek-twee-hervat-tegen-fc-groningen-2025040208231402841/) |
| 2024/2025 / 31 | 2025-04-19 – 2025-05-04 | Unresolved | Utrecht-Ajax brought forward because of early-May police capacity; Heerenveen-Almere not individually verified. [S25d](https://nos.nl/liveblog/2564291-koploper-ajax-druipt-af-farioli-geen-drama-van-maken-fc-utrecht-europa-in-met-4-0-zege) |
| 2025/2026 / 3 | 2025-08-23 – 2025-09-24 | Unresolved | European scheduling caused Feyenoord-Fortuna September17 and AZ-PEC September24; official index only. [S26](https://www.knvb.nl/node/70910) |
| 2025/2026 / 16 | 2025-12-13 – 2026-01-21 | Partial/context only | AZ-Excelsior completed January21 1-1; European postponement lead, not a fog explanation. [E26](https://excelsiorrotterdam.nl/2026/01/late-gelijkmaker-levert-excelsior-verdiend-punt-op-in-alkmaar/), [S26b](https://nos.nl/artikel/2599162-trainerswissel-baat-az-nog-niet-gelijkspel-tegen-excelsior-in-inhaalduel) |
| 2025/2026 / 18 | 2026-01-10 – 2026-02-11 | Partial/context only | January9 NEC-Utrecht winter-weather postponement directly established; February11 completion not directly inspected. [U26](https://www.fcutrecht.nl/nieuws/2026/januari/nec-nijmegen-fc-utrecht-afgelast/) |
| 2025/2026 / 20 | 2026-01-24 – 2026-02-11 | Unresolved | Competing indexed explanations: ANP says European preparation, NOS says winter weather. Cause unresolved; no date/score correction. [S26c](https://www.zeelandnet.nl/nieuws/duel-go-ahead-heerenveen-uitgesteld-om-europa-league), [S26d](https://nos.nl/artikel/2601987-heerenveen-drukt-go-ahead-eagles-verder-in-de-penarie-druk-op-coach-boel-neemt-toe) |

The latest Go Ahead–Heerenveen case has competing indexed explanations: ANP attributes movement to European preparation while a NOS result lead attributes it to winter weather. It remains unresolved rather than selecting the convenient explanation. The KNVB Utrecht–AZ page has a September 27 image caption but December 27 in its scheduling body; that internal contradiction is documented. No data values are silently changed because of either documentary inconsistency.

## All 16 source-order reversal contexts

Both endpoint records, physical lines and dates are retained for each pair. A source organized by nominal rounds need not be chronologically ordered. The table distinguishes partial contextual explanation from unresolved chronology; no final-result use before completion is authorized.

| Season / pair | Previous endpoint → next endpoint | Assessment | Finding and references |
|---|---|---|---|
| 2018/2019 / 1 | 2018-12-06 Feyenoord–VVV-Venlo → 2018-11-09 PEC Zwolle–Willem II | Partial/context only | Replay appears under earlier nominal round, not physical chronology. [F1](https://www.knvb.nl/nieuws/betaald-voetbal/eredivisie/51160/feyenoord-%E2%80%93-vvv-gestaakt-vanwege-uitvallen-lichtmasten), [F2](https://nos.nl/artikel/2258030-feyenoord-vvv-op-donderdag-6-december-overgespeeld) |
| 2018/2019 / 2 | 2019-03-13 AFC Ajax–PEC Zwolle → 2019-03-08 FC Utrecht–FC Groningen | Unresolved | Disputed Ajax-PEC March2 to March13 movement; second endpoint not certified. [RV1](https://www.knvb.nl/downloads/bestand/19153/1498---20190306-schriftelijke-uitwerking-arbitraal-vonnis-d) |
| 2018/2019 / 3 | 2019-05-15 FC Emmen–FC Groningen → 2019-05-12 sc Heerenveen–NAC Breda | Unresolved | Round33 moved after round34; source-order reversal need not be error. [RV2](https://www.knvb.nl/nieuws/betaald-voetbal/eredivisie/55163/slot-eredivisie-definitief-op-15-mei) |
| 2019/2020 / 1 | 2019-09-26 Feyenoord–AZ Alkmaar → 2019-08-30 FC Emmen–PEC Zwolle | Unresolved | European rearrangement; second endpoint not individually verified. [S19](https://www.vi.nl/nieuws/fraaie-tiki-taka-goal-hoogtepunt-bij-zege-psv-op-groningen) |
| 2019/2020 / 2 | 2020-04-09 FC Utrecht–AFC Ajax → 2020-02-14 VVV-Venlo–Heracles Almelo | Partial/context only | Unplayed April slot before February result; must never be treated as available result. [T1](https://www.knvb.nl/node/59905) |
| 2020/2021 / 1 | 2020-12-27 FC Utrecht–AZ Alkmaar → 2020-09-18 VVV-Venlo–FC Utrecht | Partial/context only | Round1 December rescheduling followed by September source record. [U1](https://www.knvb.nl/nieuws/betaald-voetbal/eredivisie/61553/nieuwe-datum-voor-fc-utrecht-az) |
| 2020/2021 / 2 | 2020-10-21 RKC Waalwijk–PEC Zwolle → 2020-10-17 Heracles Almelo–RKC Waalwijk | Unresolved | Coronavirus-delayed round4 before next-round record. [S20](https://www.omroepbrabant.nl/nieuws/3271547/na-elf-weken-zonder-positieve-test-opeens-veel-coronagevallen-bij-rkc-dit-is-enorm-schrikken) |
| 2020/2021 / 3 | 2021-04-22 AFC Ajax–FC Utrecht → 2021-02-12 RKC Waalwijk–FC Emmen | Unresolved | April result under February round; no use before completion. [S21](https://www.knvb.nl/downloads/bestand/23429/conceptprogramma-eredivisie-2021), [S21b](https://nos.nl/artikel/2377817-ajax-morst-punten-tegen-utrecht-in-aanloop-naar-35ste-landstitel) |
| 2021/2022 / 1 | 2021-12-02 AZ Alkmaar–Fortuna Sittard → 2021-08-27 Fortuna Sittard–RKC Waalwijk | Unresolved | Delayed round2; source order not event order. [S22](https://www.voetbalprimeur.nl/nieuws/996047/knvb-schuift-opnieuw-met-aanvangstijden-zes-wedstrijden-tien-clubs-betrokken.html) |
| 2021/2022 / 2 | 2021-12-01 Feyenoord–Heracles Almelo → 2021-09-17 Sparta Rotterdam–NEC Nijmegen | Partial/context only | Delayed round4; source order not event order. [S22b](https://www.knvb.nl/node/64502), [S22d](https://nos.nl/artikel/2407827-winnend-feyenoord-moet-hard-werken-tegen-heracles-maar-heeft-sinisterra) |
| 2021/2022 / 3 | 2022-04-16 Fortuna Sittard–Sparta Rotterdam → 2022-02-25 RKC Waalwijk–FC Twente | Partial/context only | Storm-delayed match; final date needs corroboration. [S22c](https://eredivisie.nl/nieuws/wedstrijd-fortuna-sittard-sparta-rotterdam-afgelast-vanwege-storm-eunice/) |
| 2021/2022 / 4 | 2022-04-19 Vitesse–Sparta Rotterdam → 2022-03-11 SC Cambuur–AFC Ajax | Unresolved | Interrupted fixture requires completion semantics, not March kickoff. [VS](https://vitesse.nl/nieuws/2022/restant-vitesse-vs-sparta-rotterdam-op-dinsdag-19-april-uitgespeeld), [VS2](https://www.nhnieuws.nl/nieuws/n76469/sparta-houdt-stand-in-resterende-374-seconden-en-boekt-belangrijke-zege-op-vitesse) |
| 2022/2023 / 1 | 2022-09-01 AZ Alkmaar–NEC Nijmegen → 2022-08-26 NEC Nijmegen–FC Groningen | Unresolved | AZ-NEC date lead only; scheduling cause unresolved. [RV3](https://www.nec-nijmegen.nl/wedstrijden/wedstrijd/az-nec-2022-09-01z-180000z.htm) |
| 2022/2023 / 2 | 2022-11-10 Feyenoord–SC Cambuur → 2022-11-04 SC Cambuur–NEC Nijmegen | Unresolved | Feyenoord-Cambuur November10 date/score lead; scheduling reason unresolved. [RV4](https://feyenoordhistorie.nl/wedstrijden/4531-feyenoord-cambuur-2022) |
| 2022/2023 / 3 | 2023-02-01 RKC Waalwijk–Go Ahead Eagles → 2023-01-24 FC Emmen–PSV Eindhoven | Unresolved | RKC-GoAhead snow postponement lead; February1 completion and next endpoint unverified. [RV5](https://nos.nl/artikel/2460675-eredivisieduel-tussen-rkc-en-go-ahead-eagles-afgelast-vanwege-winterweer) |
| 2022/2023 / 4 | 2023-04-19 Go Ahead Eagles–RKC Waalwijk → 2023-03-17 FC Volendam–Fortuna Sittard | Unresolved | GoAhead-RKC snow-postponed round25; next endpoint unverified. [S23](https://www.ga-eagles.nl/go-ahead-eagles-rkc-waalwijk-op-laatste-moment-afgelast/) |

No automatic error classification follows from a reversal. Full independent factual certification of the second endpoint was not obtained merely by finding a postponement notice for the first. The explicit unresolved questions remain in the registry.

## Deterministic 36-season ordinary sample

All rows received bounded fixture-specific research. Unresolved means search-only or insufficiently independent/direct evidence, not an erroneous source record. The final nine directly corroborated samples are 2011/12, 2013/14, 2014/15, 2017/18, 2019/20, 2022/23, 2023/24, 2024/25 and 2025/26. Publication dates are null where not established; a match date is not silently used as the publication date of a retrospective page.

| Season | Original source date / fixture / FT | Assessment | Reference |
|---|---|---|---|
| 1990/1991 | 1990-08-24 · Roda JC Kerkrade–FC Twente · 1-2 | Unresolved | [SAMPLE1990](https://www.fcupdate.nl/voetbalcompetities/nederland/eredivisie/programma-uitslagen/1990-1991) |
| 1991/1992 | 1991-08-17 · MVV–Fortuna Sittard · 0-0 | Unresolved | [SAMPLE1991](https://fortuna-online.nl/fortuna-woordenlijst/marco-boogers/) |
| 1992/1993 | 1992-08-14 · Fortuna Sittard–MVV · 1-1 | Unresolved | [SAMPLE1992](https://www.fcupdate.nl/voetbalcompetities/nederland/eredivisie/programma-uitslagen/1992-1993) |
| 1993/1994 | 1993-08-14 · Go Ahead Eagles–Vitesse · 1-4 | Unresolved | [SAMPLE1993](https://wildstat.com/p/3001/ch/HOL_1_1993_1994/stg/1/tour/all/club1/HOL_Go_Ahead_Deventer/club2/HOL_Vitesse_Arnhem) |
| 1994/1995 | 1994-08-26 · sc Heerenveen–FC Groningen · 2-0 | Unresolved | [SAMPLE1994](https://www.voetbalarchieven.nl/competitie/Eredivisie-1994-1995/) |
| 1995/1996 | 1995-08-18 · Fortuna Sittard–PSV Eindhoven · 1-3 | Unresolved | [SAMPLE1995](https://www.psv.nl/en/match-center?competition=all&season=1995-1996&team=psv1&toplevel=results) |
| 1996/1997 | 1996-08-20 · Roda JC Kerkrade–Feyenoord · 1-1 | Unresolved | [SAMPLE1996](https://www.transfermarkt.nl/roda-jc-kerkrade_feyenoord-rotterdam/index/spielbericht/1047943) |
| 1997/1998 | 1997-08-19 · AFC Ajax–Vitesse · 5-0 | Unresolved | [SAMPLE1997](https://stats.vitesse.org/wedstrijd/436.html) |
| 1998/1999 | 1998-08-20 · sc Heerenveen–FC Twente · 1-0 | Unresolved | [SAMPLE1998](https://www.vi.nl/nieuws/sc-heerenveen-wint-openingsduel) |
| 1999/2000 | 1999-08-12 · Sparta Rotterdam–Willem II · 0-2 | Unresolved | [SAMPLE1999](https://www.fcupdate.nl/voetbalcompetities/nederland/eredivisie/programma-uitslagen/1999-2000) |
| 2000/2001 | 2000-08-18 · Sparta Rotterdam–Roda JC Kerkrade · 2-2 | Unresolved | [SAMPLE2000](https://www.11v11.com/matches/sparta-rotterdam-v-roda-jc-18-august-2000-2867/) |
| 2001/2002 | 2001-08-17 · FC Twente–RKC Waalwijk · 1-0 | Unresolved | [SAMPLE2001](https://schatkamer.beeldengeluid.nl/serie/2101608030021690631/nos-studio-sport/aflevering/2101608060042143631) |
| 2002/2003 | 2002-08-16 · RBC Roosendaal–FC Zwolle · 1-1 | Unresolved | [SAMPLE2002](https://www.voetbalstats.nl/allespereclubtegen.php?clubid=79) |
| 2003/2004 | 2003-08-15 · Roda JC Kerkrade–PSV Eindhoven · 2-2 | Unresolved | [SAMPLE2003](https://www.voetbalkrant.com/nieuws/2003-08-15/psv-opent-met-gelijkspel) |
| 2004/2005 | 2004-08-13 · Roda JC Kerkrade–Vitesse · 2-3 | Unresolved | [SAMPLE2004](https://www.transfermarkt.com/roda-jc-kerkrade_vitesse-arnhem/index/spielbericht/26686) |
| 2005/2006 | 2005-08-12 · AZ Alkmaar–Sparta Rotterdam · 3-0 | Unresolved | [SAMPLE2005](https://frontpage.fok.nl/all/archief/2005/08/12) |
| 2006/2007 | 2006-08-18 · Sparta Rotterdam–Vitesse · 1-2 | Unresolved | [SAMPLE2006](https://www.bdfutbol.com/p/p.php?id=693366) |
| 2007/2008 | 2007-08-17 · sc Heerenveen–Willem II · 0-0 | Unresolved | [SAMPLE2007](https://www.vi.nl/nieuws/heerenveen-en-willem-ii-hebben-het-nog-niet) |
| 2008/2009 | 2008-08-29 · Vitesse–FC Groningen · 0-4 | Unresolved | [SAMPLE2008](https://www.voetbalstats.nl/opstelere.php?match=29-08-2008-eredivisie-vitesse-fc-groningen) |
| 2009/2010 | 2009-07-31 · sc Heerenveen–Roda JC Kerkrade · 0-0 | Unresolved | [SAMPLE2009](https://frontpage.fok.nl/nieuws/351091/1/1/50/uitslag-sc-heerenveen-roda-jc.html) |
| 2010/2011 | 2010-08-06 · Roda JC Kerkrade–FC Twente · 0-0 | Unresolved | [SAMPLE2010](https://nos.nl/artikel/176869-twente-morst-punten-bij-roda) |
| 2011/2012 | 2011-08-05 · SBV Excelsior–Feyenoord · 0-2 | Full core facts | [SAMPLE2011](https://www.skysports.com/football/excelsior-vs-feyenoord/report/239507) |
| 2012/2013 | 2012-08-10 · Willem II–NAC Breda · 1-1 | Unresolved | [SAMPLE2012](https://www.voetbalstats.nl/allespereclubclub.php?clubid1=121&clubid2=2719) |
| 2013/2014 | 2013-08-02 · AFC Ajax–Roda JC Kerkrade · 3-0 | Full core facts | [SAMPLE2013](https://nos.nl/artikel/536127-simpele-zege-ajax-op-roda-jc) |
| 2014/2015 | 2014-08-08 · PEC Zwolle–FC Utrecht · 2-0 | Full core facts | [SAMPLE2014](https://www.fcutrecht.nl/nieuws/2014/08/fc-utrecht-onderuit-tegen-pec-zwolle/) |
| 2015/2016 | 2015-08-08 · Feyenoord–FC Utrecht · 3-2 | Unresolved | [SAMPLE2015](https://feyod.nl/competities/eredivisie/2015) |
| 2016/2017 | 2016-08-05 · NEC Nijmegen–PEC Zwolle · 1-1 | Unresolved | [SAMPLE2016](https://nos.nl/artikel/2123419-nec-en-pec-openen-met-gelijkspel) |
| 2017/2018 | 2017-08-11 · ADO Den Haag–FC Utrecht · 0-3 | Full core facts | [SAMPLE2017](https://adodenhaag.nl/nl/component/game/game/405-ado-den-haag-fc-utrecht-405) |
| 2018/2019 | 2018-08-10 · PEC Zwolle–sc Heerenveen · 2-3 | Unresolved | [SAMPLE2018](https://nos.nl/liveblog/2245469-tiental-heerenveen-klopt-pec-zwolle-in-seizoensopening-lozano-weer-fit-bij-psv) |
| 2019/2020 | 2019-08-02 · PEC Zwolle–Willem II · 1-3 | Full core facts | [SAMPLE2019](https://peczwolle.nl/nieuws/wrange-start-van-het-seizoen-voor-zwolle) |
| 2020/2021 | 2020-09-12 · FC Twente–Fortuna Sittard · 2-0 | Unresolved | [SAMPLE2020](https://www.fctwentestatistieken.nl/wedstrijden/wedstrijddetail.php?id=2143502344) |
| 2021/2022 | 2021-08-13 · Go Ahead Eagles–sc Heerenveen · 0-1 | Unresolved | [SAMPLE2021](https://www.nhnieuws.nl/nieuws/n51828/bekijk-de-samenvatting-van-go-ahead-eagles-heerenveen-0-1) |
| 2022/2023 | 2022-08-05 · sc Heerenveen–Sparta Rotterdam · 0-0 | Full core facts | [SAMPLE2022](https://nos.nl/artikel/2439531-sparta-pakt-punt-bij-slaapverwekkende-seizoensouverture-in-heerenveen) |
| 2023/2024 | 2023-08-11 · FC Volendam–SBV Vitesse · 1-2 | Full core facts | [SAMPLE2023](https://fcvolendam.nl/wedstrijdnieuws/rode-kaart-en-late-tegentreffer-nekken-fc-volendam-in-seizoenopener/) |
| 2024/2025 | 2024-08-09 · FC Groningen–NAC Breda · 4-1 | Full core facts | [SAMPLE2024](https://nos.nl/liveblog/2532531-groningen-wint-ruim-van-nac-wedstrijd-snel-beslist-na-vroege-rode-kaart) |
| 2025/2026 | 2025-08-08 · Fortuna Sittard–Go Ahead Eagles · 2-2 | Full core facts | [SAMPLE2025](https://nos.nl/artikel/2578014-go-ahead-eagles-knokt-zich-met-tien-man-naast-fortuna-in-eerste-duel-eredivisie) |

Earlier CSV-only seasons mostly have secondary or index-only leads and therefore lower direct-evidence confidence in this review. Overlap agreement is not independent certification: the two repositories may share upstream data. Modern authored reports improve confidence for particular fixtures, but do not certify their season. The latest season still contains the source-bound NAC incompleteness despite direct completion reports.

## Club identities and out-of-window source risk

All 47 literal target labels remain unchanged and are listed in the private identity assessment. Relationships are findings, not mappings:

* NEC, NEC Nijmegen, N.E.C.: Cosmetic/locational label relationship supported in senior context; no legal entity merge. [I5](https://www.nec-nijmegen.nl/club/historie.htm)
* RKC, RKC Waalwijk: 1996 rename lead; secondary only, no global alias. [I4](https://www.rsssf.org/nedfer/ned-allclubs-w.html)
* NAC, NAC Breda: Senior historical narrative continuity; exact rename act not verified. [I6](https://www.nac.nl/historie)
* FC Zwolle, PEC Zwolle: 2012 name change distinct from 1990 bankruptcy/new establishment; do not map predecessors indiscriminately. [I1](https://peczwolle.nl/clubhistorie)
* FC Den Haag, ADO Den Haag: 1996 merger documented, not merely punctuation. [I2](https://adodenhaag.nl/nl/club/historie/historische-tijdlijn)
* SVV, SVV/Dordrecht 90, Dordrecht 90: 1991 merger and1992 rename indexed; exact legal continuity unresolved. [I3](https://www.tekst-advies.nu/wp-content/uploads/2022/01/ENERGIEK-DORDT-2021-2025.pdf)
* Senior, Jong/reserve: No equivalence inferred; tier/title and pairings establish structural scope only.

The other literal names and season-scoped diagnostic correspondences remain unmerged. Senior and reserve teams must remain distinct. Club histories do not automatically establish license-holder or successor continuity; the Zwolle bankruptcy and Den Haag merger especially require date-bounded treatment.

Both 1979/80 PEC Zwolle observations dated 1980-02-13 remain preserved outside the Phase 5 target. The two source IDs are recorded in the Phase 4 report. The historical file parses syntactically, but this collision demonstrates that date syntax and aggregate completeness do not guarantee factual chronology. The target window was not expanded and those observations were not corrected.

## Evidence inventory, provenance and limitations

The private evidence inventory has 96 references: 40 directly inspected, 54 index-only, and 2 maintenance responses. Exact titles, URLs, organizations, authors where known, publication/retrieval dates, supported findings, access status, independence and rights limits are recorded. A direct title alone, maintenance page or cache miss cannot certify a body. Several requests failed; restrictions were respected without bypasses or bulk scraping. No new season datasets were acquired.

Direct evidence includes participant/federation narratives and contemporary editorial reporting. Feeds, secondary archives and agency relationships remain explicitly uncertain. Distinct repository filenames do not establish upstream independence. The inventory stores brief paraphrases and bibliographic references, not full copyrighted articles or downloaded season collections. No model-training or redistribution permission is inferred from accessibility. Source technical structure, independent historical accuracy, actual result availability, redistribution and training clearance remain separate.

## Fresh tests, deterministic regeneration and preservation

Tests used the existing safe external Python 3.13.12 environment, with bounded timeouts, disabled project bytecode/cache writes and no dependency installation or original `.venv` changes. Runs overlap:

| Run | Passed | Failures / errors / skips |
|---|---:|---|
| acquisition_importer | 556 | 0 / 0 / 0 |
| app_launcher | 7 | 0 / 0 / 0 |
| eredivisie | 147 | 0 / 0 / 0 |
| full | 1706 | 0 / 0 / 0 |
| historical_review | 32 | 0 / 0 / 0 |
| non_ui | 1699 | 0 / 0 / 0 |

The 32 new synthetic cases cover deterministic sampling, exclusion of flagged/null candidates from the ordinary sample, missing seasons, stable ordering, reference metadata/duplicates/access classes, rejection of snippet-based full certification, required core facts, dangling references, unchanged conflicting originals, conditional group bindings and duplicate JSON keys.

A separate fresh invocation regenerated all four Phase 5 outputs into temporary storage and compared bytes and SHA-256 values against saved artifacts. All matched:

| Artifact | SHA-256 |
|---|---|
| phase5_confidence_summary.json | `ea0b85a73653a5f6b42514238122f18f5ff1dd5ca2690268014d26a396c618c4` |
| phase5_context_assessment.json | `8ea17d426c9a5db2ac737d329cd43ba82741c43e0f0e666d9110d6497ed60b36` |
| phase5_fixture_registry.json | `aba53f0613f325b7aa452ef19e8dcfd4485428869c3b229faad0405e0f91d264` |
| phase5_reference_index.json | `463bb5478c5d66e11af1882be5f1aa8c35c56f46653003fc6b969d880e92b541` |

Reproduce offline, using preserved originals and recorded evidence inputs:

```sh
PYTHONPATH=. python -B scripts/verify_eredivisie_review.py
PYTHONPATH=src:. PYTHONDONTWRITEBYTECODE=1 python -B -m pytest tests/test_eredivisie_review.py -q -p no:cacheprovider
```

This reproduces saved evidence accounting; it does not re-fetch changing websites or independently repeat human interpretation. Input hashes are bound into the reference index. The CLI refuses to overwrite changed outputs. Frozen verification protects 839 previous private files and 207 public files, plus 117 frozen Phase 2–4 entries and the original planning prefix. All nine originals and their provenance remain byte-identical. HEAD/index remain unchanged; private files are ignored and untracked. No previous competition, application or promotional-worktree change occurred.

Public Phase 5 changes: `scripts/verify_eredivisie_review.py`, `tests/test_eredivisie_review.py`, this report and append-only `PLANNING_LOG.md`. Private additions: baseline, deterministic sample, evidence inventory, research inputs, four generated assessment/index JSON files, reproducibility/test/final verification receipts and `verification_phase5/` logs/XML/status.

## Proposed Phase 6 agenda — requires approval

1. Decide the Groningen–Ajax kickoff/completion semantics, preserving both source dates and forbidding completed-result availability before May 16.
2. Decide the NEC–Vitesse source-score conflict explicitly using the directly inspected 1–3 evidence; retain contradictory 1–2 unchanged in the audit archive. Do not assert a proven upstream error mechanism.
3. Decide whether to permit NAC supplementation from source-bound evidence, after rights/provenance review, or keep an explicit HOLD OUT. Null plus cancellation must not silently become NOT PLAYED.
4. Define completion-date/result-availability treatment for the three 2023/24 interruptions and the additional Feyenoord–VVV, Vitesse–Sparta and Heracles–Groningen cases, preserving confidence gaps. Pending evidence must remain visible.
5. Define the 74 unplayed 2019/20 slot treatment separately from the 232 played results and independently of season-champion rules.
6. Preserve all 25 scheduling contexts, 16 reversals, 410 flags and 27 unverified ordinary samples without automatic corrections/exclusions. Long spans alone do not establish errors. Resolve or conservatively retain contradictory scheduling explanations.
7. Require explicit evidence-bound decisions for any unresolved final-result case; preserve original identities and distinguish cosmetic labels from mergers/successors and reserve sides. No global aliases are approved.
8. Require chronological evaluation to use only completed, known results strictly before prediction time; define intraday/date-only uncertainty conservatively. Keep historical confidence and licensing/training clearance separate from technical eligibility.

Stop after Phase 5. No Phase 6 policy is implemented and no final accepted-record total is claimed.
