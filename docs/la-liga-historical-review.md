# La Liga Phase 5: independent historical evidence review

Date: 2026-11-22 (Europe/Budapest). Original `toto` worktree, `feature/data-collection`; HEAD remains `2f2bfe1542c2460111ae685621d138874fa69f52`.

## Outcome and assurance boundary

**Evidence review completed with unresolved items retained; the population is not historically certified and is not ready for automatic standardization.** No original or standardized match data, existing evidence, application or promotional files were changed. No corrections, exclusions, training or Git publication occurred.

| Measure | Count | Meaning |
|---|---:|---|
| Original fixtures preserved | 13,844 | Approved 36-season scope |
| Fixed all-season sample | 36 | One fixture in each season; 28 verified, 8 unresolved |
| Additional fixture-level reviews | 6 | Six verified, disjoint from sample |
| Distinct fixture-level reviews | 42 | 34 verified facts, 8 unresolved; not exhaustive disciplinary clearance |
| Flagged rounds researched | 34 | 23 explained/documented date patterns, 8 partial, 3 unresolved |
| Fixtures in flagged rounds | 340 | Round context only, not 340 individual verifications |
| Diagnostic outliers prioritized | 52 | All carried forward and researched at round/fixture-context level |
| Outliers without individual full-fact certification | 49 | Three outliers have separate verified fixture claims |
| Unique priority fixtures | 91 | Union of sample, outliers and supplemental cases |
| Unique fixture/context coverage | 378 | Union of sample, flagged-round fixtures and supplemental cases |
| Confirmed source fact discrepancies | 0 | No evidence-supported unconditional date/score repair |
| Resumption date-policy cases | 2 | Start and completion dates differ; approval required |
| Label groups examined | 18 | 16 spelling/abbreviation candidates, two with identity-boundary cautions |
| Prior artifacts protected | 485 | Includes all 428 previous-competition artifacts and frozen Phase 2–4 files |

These categories overlap and must not be added. Of the six supplemental fixtures, four lie within flagged rounds (three are diagnostic outliers); the two resumed matches lie outside those rounds. The 34 verified fixtures do not establish an error rate or absence of undiscovered administrative changes across all 13,844 matches.

## Reproducible selection and independence

Fixed purposive sample: the unique regular-season Real Madrid home fixture against FC Barcelona in every selected season. Explicit observed labels only; no date/result-based selection. Not random or an accuracy estimate.

`scripts/verify_la_liga_review.py` independently reruns this selection from the original CSV/text files using explicit Real Madrid / Real Madrid C.F. / Real Madrid CF and FC Barcelona / Barcelona labels. It requires exactly one selected home fixture per season and exact source SHA-256, physical line, original values and season bindings. The frozen selection predates evidence classification. This deliberately prominent, two-club sample is biased and is not a probability sample.

Preference was given to contemporary authored reporting, official organizer decisions and participating-club match accounts. UEFA, club and league editorial prose is treated as documentary evidence separate from the acquired compiler files, with independence **inferred from authorship/context**, not proven universally. Club retrospective/background accounts are identified as such; BDFutbol/club player-archive listings are not granted independence merely because their URL differs. The 4,940 observations of cross-source agreement and the five diagnostic 2012/13 aliases remain earlier evidence, not independent certification.

Only readable inspected documents support VERIFIED claims. Search-index summaries, empty pages, 403/502 responses, cache misses and timeouts remain indexed/partial evidence; they are not upgraded after failed access and no access restriction was bypassed. Some contemporary technical sheets establish the score but not an explicit event date in the inspected passage: those samples remain unresolved rather than inferring the date from publication alone.

For VERIFIED, teams/date/full-time score are supported; exceptional status means no exception identified in the inspected material, **not** exhaustive final-legal-status certification. Exact URLs, titles, access, publication dates where established, source-line original facts, team correspondences, findings and independence limitations are retained in the private ledger. Unknown publication dates remain null rather than fabricated.

## All-season sample

All fixtures below are Real Madrid home league matches against Barcelona. Date/score columns are unchanged source values; unresolved rows do not certify those values.

| ID | Season | Source date | Source FT | Status | Evidence |
|---|---|---|---|---|---|
| L01 | 1990/1991 | 1991-06-08 | 1–0 | UNRESOLVED | [D17](https://hemeroteca-paginas.mundodeportivo.com/EMD01/HEM/1991/06/09/MD19910609-007.pdf) |
| L02 | 1991/1992 | 1991-10-19 | 1–1 | UNRESOLVED | [D18](https://hemeroteca-paginas.mundodeportivo.com/EMD01/HEM/1991/10/20/MD19911020-008.pdf) |
| L03 | 1992/1993 | 1993-01-30 | 2–1 | UNRESOLVED | [D08](https://elpais.com/diario/1993/01/31/deportes/728434815_850215.html) |
| L04 | 1993/1994 | 1994-05-07 | 0–1 | UNRESOLVED | [D37](https://www.bdfutbol.com/es/p/p.php?id=19360) |
| L05 | 1994/1995 | 1995-01-07 | 5–0 | VERIFIED | [D76](https://www.realmadrid.com/es-ES/el-club/historia/leyendas-futbol/ivan-luis-zamorano-zamora) |
| L06 | 1995/1996 | 1995-09-30 | 1–1 | VERIFIED | [D19](https://hemeroteca-paginas.mundodeportivo.com/EMD01/HEM/1995/10/01/MD19951001-002.pdf) |
| L07 | 1996/1997 | 1996-12-07 | 2–0 | UNRESOLVED | [D09](https://elpais.com/diario/1996/12/08/deportes/849999611_850215.html) |
| L08 | 1997/1998 | 1997-11-01 | 2–3 | VERIFIED | [D10](https://elpais.com/diario/1997/11/02/portada/878425203_850215.html?outputType=amp) |
| L09 | 1998/1999 | 1998-09-19 | 2–2 | VERIFIED | [D11](https://elpais.com/diario/1998/09/20/deportes/906242407_850215.html?outputType=amp) |
| L10 | 1999/2000 | 2000-02-26 | 3–0 | UNRESOLVED | [D12](https://elpais.com/diario/2000/02/27/deportes/951606016_850215.html) |
| L11 | 2000/2001 | 2001-03-03 | 2–2 | VERIFIED | [D06](https://elpais.com/deportes/2001/03/03/actualidad/983607715_850215.html) |
| L12 | 2001/2002 | 2001-11-04 | 2–0 | UNRESOLVED | [D13](https://elpais.com/diario/2001/11/05/deportes/1004914802_850215.html) |
| L13 | 2002/2003 | 2003-04-19 | 1–1 | VERIFIED | [D92](https://www.uefa.com/news-media/news/025e-0f9086d577c5-e33ba36a1609-1000--spain-round-up-barcelona-frustrate-madrid/) |
| L14 | 2003/2004 | 2004-04-25 | 1–2 | VERIFIED | [D85](https://www.uefa.com/news-media/news/019c-0f8455f60fd3-2767f0f509cd-1000--barca-roar-into-contention/) |
| L15 | 2004/2005 | 2005-04-10 | 4–2 | VERIFIED | [D60](https://www.laliga.com/es-GB/noticias/clasicos-para-recordar) |
| L16 | 2005/2006 | 2005-11-19 | 0–3 | VERIFIED | [D48](https://www.fcbarcelona.com/en/news/1899174/15-years-to-the-day-since-a-famous-clsico) |
| L17 | 2006/2007 | 2006-10-22 | 2–0 | VERIFIED | [D86](https://www.uefa.com/news-media/news/01ba-0e6db41cd226-d1a95e3c838e-1000--madrid-triumph-in-el-clasico/) |
| L18 | 2007/2008 | 2008-05-07 | 4–1 | VERIFIED | [D87](https://www.uefa.com/news-media/news/01cd-0f84da0e7cd5-791c157fefc8-1000--barca-beaten-as-villarreal-seal-second/) |
| L19 | 2008/2009 | 2009-05-02 | 2–6 | VERIFIED | [D47](https://www.fcbarcelona.com/en/news/1663569/11-years-to-the-day-since-the-6-2-away-win-against-real-madrid) |
| L20 | 2009/2010 | 2010-04-10 | 0–2 | VERIFIED | [D49](https://www.fcbarcelona.com/en/news/2096982/laporta-gets-his-hands-on-the-clasico-shirt) |
| L21 | 2010/2011 | 2011-04-16 | 1–1 | VERIFIED | [D88](https://www.uefa.com/news-media/news/01f0-0e77e658d364-da5f24e31c1d-1000--ten-man-madrid-fight-back-to-deny-barcelona/) |
| L22 | 2011/2012 | 2011-12-10 | 1–3 | VERIFIED | [D93](https://www.uefa.com/news/01f8-0e7c7b3a7400-35a09e92cfaf-1000--barcelona-rally-to-claim-clasico-bragging-rights/) |
| L23 | 2012/2013 | 2013-03-02 | 2–1 | VERIFIED | [D89](https://www.uefa.com/news-media/news/0207-0e9ec7425a92-1ed4dbd30bc6-1000--ramos-earns-madrid-another-win-against-barca/) |
| L24 | 2013/2014 | 2014-03-23 | 3–4 | VERIFIED | [D90](https://www.uefa.com/news-media/news/0213-0e899ae289d9-cf4a91729648-1000--messi-treble-helps-barcelona-edge-clasico-thriller/) |
| L25 | 2014/2015 | 2014-10-25 | 3–1 | VERIFIED | [D91](https://www.uefa.com/news-media/news/021a-0f8a6f036cdd-c6c02bb540d8-1000--madrid-dominate-to-get-better-of-barcelona/) |
| L26 | 2015/2016 | 2015-11-21 | 0–4 | VERIFIED | [D94](https://www.uefa.com/uefachampionsleague/news/0227-0e928ed66790-708b6f41f368-1000--real-madrid-0-4-barcelona-what-we-learned/) |
| L27 | 2016/2017 | 2017-04-23 | 2–3 | VERIFIED | [D95](https://www.uefa.com/uefachampionsleague/news/0238-0e96c9f3cce6-13c9b518ea8d-1000--messi-sinks-madrid-juventus-and-monaco-triumph/) |
| L28 | 2017/2018 | 2017-12-23 | 0–3 | VERIFIED | [D96](https://www.uefa.com/uefachampionsleague/news/0241-0e983e58104c-837a077fccf3-1000--chelsea-and-barcelona-renew-rivalry/) |
| L29 | 2018/2019 | 2019-03-02 | 0–1 | VERIFIED | [D50](https://www.fcbarcelona.es/es/futbol/primer-equipo/noticias/1085320/reial-madrid-barca-ya-es-un-clasico-0-1) |
| L30 | 2019/2020 | 2020-03-01 | 2–0 | UNRESOLVED | [D20](https://players.fcbarcelona.com/en/match/f1075071-real-madrid-barcelona) |
| L31 | 2020/2021 | 2021-04-10 | 2–1 | VERIFIED | [D79](https://www.realmadrid.com/es-ES/noticias/futbol/primer-equipo/cronicas/2-1-victoria-en-el-clasico) |
| L32 | 2021/2022 | 2022-03-20 | 0–4 | VERIFIED | [D44](https://www.fcbarcelona.com/en/football/first-team/news/2544426/real-madrid-0-4-barca-the-clasico-is-blaugrana/featured) |
| L33 | 2022/2023 | 2022-10-16 | 3–1 | VERIFIED | [D80](https://www.realmadrid.com/es-ES/noticias/futbol/primer-equipo/cronicas/3-1-el-madrid-gana-el-clasico-y-es-lider) |
| L34 | 2023/2024 | 2024-04-21 | 3–2 | VERIFIED | [D81](https://www.realmadrid.com/es-ES/noticias/futbol/primer-equipo/cronicas/cronica-21-04-2024-rm-barcelona) |
| L35 | 2024/2025 | 2024-10-26 | 0–4 | VERIFIED | [D45](https://www.fcbarcelona.com/en/football/first-team/news/4156771/real-madrid-04-fc-barcelona-viva-la-vida) |
| L36 | 2025/2026 | 2025-10-26 | 2–1 | VERIFIED | [D82](https://www.realmadrid.com/es-ES/noticias/futbol/primer-equipo/cronicas/cronica-real-madrid-barcelona-jornada-10-liga-26-10-2025) |

Unresolved sample limits:

- **L01 (1990/1991):** Technical sheet confirms teams/1-0; next-day publication alone is insufficient to certify the precise event date.
- **L02 (1991/1992):** Technical sheet confirms teams/1-1; exact event date not independently established from inspected text.
- **L03 (1992/1993):** Contemporary report supports Madrid victory; exact date and full score not explicitly established in inspected passages.
- **L04 (1993/1994):** BDFutbol listing supports 7 May/0-1, but compiler independence is not established and no readable primary confirmation was located.
- **L07 (1996/1997):** Contemporary narrative supports two Madrid goals and none for Barcelona; date only corroborated by indexed preview.
- **L10 (1999/2000):** Contemporary report appears in search index but direct fetch timed out; no full-document verification claimed.
- **L12 (2001/2002):** Contemporary technical sheet confirms 2-0; precise event date is not explicit in inspected passages.
- **L30 (2019/2020):** Club match archive and secondary listings agree, but archive fetch failed (502); archive upstream lineage is also unspecified.

## All 34 scheduling cases

EXPLAINED means a directly inspected document supports postponement, advancement or the observed date pattern. It does not necessarily establish the underlying cause, every final playing date, every score or all ten fixtures. PARTIAL retains unsupported diagnostic dates/mechanisms. UNRESOLVED means no substantive direct confirmation sufficient to explain the case was obtained.

The immutable sources generally print date blocks, not explicit postponement/resumption annotations for these fixtures. No long span is classified as an error merely because it exceeds 14 days. The full ten-fixture sets, original five Phase 2 flags, 29 additional Phase 3 flags, all 52 diagnostic outlier rows and per-outlier limitations remain in `phase5_historical_review.json`; none was reclassified or discarded from the frozen Phase 4 record.

| ID | Season / round | Earliest → latest | Diagnostic fixtures and source dates | Assessment / evidence |
|---|---|---|---|---|
| S01 | 2012/2013 / 3 | 2012-09-01 → 2012-09-26 | Real Betis–Atlético Madrid 2012-09-26 | **UNRESOLVED** — Indexed broadcaster notice describes postponement to 26 September; direct document unavailable. Reason/date not certified. [D05](https://cadenaser.com/ser/2012/09/03/deportes/1346628495_850215.html) |
| S02 | 2013/2014 / 34 | 2014-04-18 → 2014-05-07 | Real Valladolid–Real Madrid 2014-05-07 | **UNRESOLVED** — Indexed UEFA report gives 7 May draw; direct document unavailable. Postponement cause remains unverified. [D15](https://es.uefa.com/news-media/news/0215-0e8aab60f2d4-59ba1cbeec8d-1000--el-valladolid-salva-un-punto/) |
| S03 | 2014/2015 / 16 | 2014-12-19 → 2015-02-04 | Real Madrid–Sevilla FC 2015-02-04 | **EXPLAINED** — League explicitly moved Madrid-Sevilla to 4 February for Club World Cup participation. [D65](https://www.laliga.com/noticias/horario-del-real-madrid-sevilla-de-la-jornada-16-de-la-liga-bbva) |
| S04 | 2015/2016 / 16 | 2015-12-19 → 2016-02-17 | Sporting Gijón–FC Barcelona 2016-02-17 | **EXPLAINED** — Club training notice identifies Sporting fixture as rescheduled for Club World Cup commitments; dates are consistent with February midweek. [D46](https://www.fcbarcelona.com/en/news/1070912/training-schedule-ahead-of-busy-week-with-two-league-matches) |
| S05 | 2016/2017 / 16 | 2016-12-16 → 2017-02-22 | Valencia CF–Real Madrid 2017-02-22 | **EXPLAINED** — League explicitly rescheduled Valencia-Madrid to 22 February after Club World Cup. [D57](https://www.laliga.com/en-GB/news/the-postponed-game-valencia-cf-v-real-madrid-will-be-played-on-february-22) |
| S06 | 2016/2017 / 21 | 2017-02-04 → 2017-05-17 | Deportivo La Coruña–Real Betis 2017-03-08; RC Celta–Real Madrid 2017-05-17 | **EXPLAINED** — League identifies Deportivo-Betis as postponed round 21 on 8 March; RTVE reports Celta-Madrid moved to 17 May. Specific storm mechanism for each remains partly indexed. [D69](https://www.laliga.com/noticias/pepe-mel-y-victor-sanchez-del-amo-ante-sus-ex), [D84](https://www.rtve.es/deportes/20170505/celta-real-madrid-se-jugara-miercoles-17-mayo-a-2100-horas/1539265.shtml), [D61](https://www.laliga.com/es-GB/noticias/nota-informativa-93) |
| S07 | 2017/2018 / 16 | 2017-12-15 → 2018-02-21 | CD Leganés–Real Madrid 2018-02-21 | **EXPLAINED** — UEFA actual-match report confirms 21 February 1-3, round 16 postponed for Club World Cup. [D16](https://es.uefa.com/news-media/news/0242-0f8e5d90441a-f425072d9fe9-1000--el-real-madrid-recupera-la-tercera-plaza/) |
| S08 | 2017/2018 / 34 | 2018-04-20 → 2018-05-09 | FC Barcelona–Villarreal CF 2018-05-09; Sevilla FC–Real Madrid 2018-05-09 | **PARTIAL** — League confirms Sevilla-Madrid postponed round 34 on 9 May; Barcelona-Villarreal same-day lead remains indexed only. Copa-final explanation not fully established for both. [D64](https://www.laliga.com/noticias/el-sevilla-en-busca-de-la-septima-plaza-en-el-sanchez-pizjuan), [D41](https://www.elnacional.cat/es/en-directo-deportes/barca-villarreal-liga_2796_126.html) |
| S09 | 2018/2019 / 3 | 2018-08-31 → 2018-10-24 | Rayo Vallecano–Athletic Club 2018-10-24 | **EXPLAINED** — Rayo official notice gives postponed Athletic fixture 24 October. Underlying stadium cause not certified here. [D74](https://www.rayovallecano.es/noticias/rayo-athletic-club-el-miercoles-24-de-octubre-a-las-1900-horas) |
| S10 | 2019/2020 / 10 | 2019-10-25 → 2019-12-18 | FC Barcelona–Real Madrid 2019-12-18 | **EXPLAINED** — RFEF decision moves round 10 Clasico from 26 October to 18 December for exceptional circumstances. [D25](https://rfef.es/es/noticias/oficial-competicion-fija-el-clasico-fc-barcelona-real-madrid-cf-para-el-18-de-diciembre) |
| S11 | 2019/2020 / 24 | 2020-02-14 → 2020-03-10 | SD Eibar–Real Sociedad 2020-03-10 | **EXPLAINED** — RFEF order explicitly postpones Eibar-Sociedad for toxic-air health advice and sets 10 March. [D28](https://rfef.es/sites/default/files/images19/acuerdo_comite_nueva_fecha.pdf) |
| S12 | 2020/2021 / 1 | 2020-09-12 → 2021-02-24 | Club Atlético de Madrid–Sevilla FC 2021-01-12; Real Madrid CF–Getafe CF 2021-02-09; FC Barcelona–Elche CF 2021-02-24 | **PARTIAL** — RFEF confirms Atletico-Sevilla 12 January and Madrid confirms Getafe 9 February; Barcelona-Elche 24 February remains indexed-only. [D77](https://www.realmadrid.com/es-ES/noticias/futbol/primer-equipo/actualidad/el-real-madrid-getafe-se-jugara-finalmente-el-martes-9-de-febrero-a-las-21-00-h), [D31](https://rfef.es/sites/default/files/images19/partidos_aplazados_1a_division.pdf), [D38](https://www.besoccer.com/new/barcelona-v-elche-as-it-happened-959759) |
| S13 | 2020/2021 / 2 | 2020-09-19 → 2021-03-17 | Athletic Club–FC Barcelona 2021-01-06; Levante UD–Club Atlético de Madrid 2021-02-17; Sevilla FC–Elche CF 2021-03-17 | **PARTIAL** — Club confirms Athletic-Barcelona January recovery break; RFEF confirms Sevilla-Elche 17 March; precise Levante-Atletico date remains indexed-only. [D43](https://www.fcbarcelona.com/en/football/first-team/news/1922697/three-new-kick-off-times-confirmed-for-fc-barcelona/featured), [D29](https://rfef.es/sites/default/files/images19/partido_aplazado_1a_3.pdf), [D40](https://www.comuniate.com/noticias/8142/jornada-extra-en-comunio-levante-atletico) |
| S14 | 2020/2021 / 4 | 2020-09-29 → 2021-01-12 | Granada CF–CA Osasuna 2021-01-12 | **EXPLAINED** — RFEF referee appointment confirms postponed Granada-Osasuna on 12 January; Europa League condition only indexed, not certified. [D31](https://rfef.es/sites/default/files/images19/partidos_aplazados_1a_division.pdf), [D53](https://www.laliga.com/calendario-2020-2021/laliga-santander) |
| S15 | 2020/2021 / 19 | 2020-12-15 → 2021-01-21 | Real Madrid CF–Athletic Club 2020-12-15; FC Barcelona–Real Sociedad de Fútbol 2020-12-16 | **PARTIAL** — Club explicitly advanced Barcelona-Sociedad to 16 December for Super Cup. Madrid-Athletic 15 December listed in indexed annual report, not directly inspected there. [D42](https://www.fcbarcelona.com/en/football/first-team/actualites/1898219/le-calendrier-de-la-fin-dannee-2020/featured) |
| S16 | 2020/2021 / 18 | 2021-01-08 → 2021-03-10 | Club Atlético de Madrid–Athletic Club 2021-03-10 | **PARTIAL** — League confirms storm/airport/pitch postponement; exact 10 March completion date only indexed club evidence. [D56](https://www.laliga.com/en-GB/news/official-statement-jan-9-2021), [D36](https://www.atleticodemadrid.com/clasificacion-primer-equipo-2020-2021) |
| S17 | 2021/2022 / 4 | 2021-09-11 → 2021-12-21 | Villarreal CF–Deportivo Alavés 2021-12-21; Sevilla FC–FC Barcelona 2021-12-21 | **EXPLAINED** — RFEF round-4 appointments confirm both matches 21 December; calendar split is documented. International-window cause not independently certified here. [D30](https://rfef.es/sites/default/files/images19/partidos_1a_division_211217_154720.pdf), [D55](https://www.laliga.com/en-GB/news/kick-off-times-confirmed-for-postponed-matches-from-matchdays-4-and-9) |
| S18 | 2021/2022 / 9 | 2021-10-16 → 2021-12-22 | Real Madrid CF–Athletic Club 2021-12-01; Granada CF–Club Atlético de Madrid 2021-12-22 | **PARTIAL** — Granada-Atletico 22 December supported. League announcement confusingly mixes Athletic-Madrid round21 with its round9 heading; Madrid-Athletic 1 December needs separate primary confirmation. [D55](https://www.laliga.com/en-GB/news/kick-off-times-confirmed-for-postponed-matches-from-matchdays-4-and-9), [D01](https://as.com/futbol/2021/11/17/primera/1637171450_840773.html) |
| S19 | 2021/2022 / 21 | 2021-12-22 → 2022-04-24 | Athletic Club–Real Madrid CF 2021-12-22; Club Atlético de Madrid–Levante UD 2022-02-16; RCD Mallorca–Real Sociedad de Fútbol 2022-03-02; FC Barcelona–Rayo Vallecano de Madrid 2022-04-24 | **PARTIAL** — Barcelona-Rayo 24 April and Athletic-Madrid 22 December documented. Atletico-Levante 16 February and Mallorca-Sociedad 2 March remain indexed only; do not claim all four individually verified. [D51](https://www.fcbarcelona.es/es/noticias/2513425/el-barca-rayo-vallecano-ya-tiene-fecha-y-hora), [D83](https://www.realsociedad.eus/es/noticias/detalle/impulso), [D02](https://as.com/futbol/2022/02/16/primera/1645032626_333477.html), [D55](https://www.laliga.com/en-GB/news/kick-off-times-confirmed-for-postponed-matches-from-matchdays-4-and-9) |
| S20 | 2022/2023 / 17 | 2023-01-13 → 2023-02-02 | Real Betis Balompié–FC Barcelona 2023-02-01; Real Madrid CF–Valencia CF 2023-02-02 | **PARTIAL** — Madrid official notice confirms Super Cup displacement and 2 February Madrid-Valencia; Betis-Barcelona 1 February primary preview currently indexed-only. [D78](https://www.realmadrid.com/es-ES/noticias/futbol/primer-equipo/actualidad/el-real-madrid-valencia-se-jugara-el-jueves-2-de-febrero-a-las-21-00-h), [D52](https://www.fcbarcelona.es/es/noticias/3041872/betis-barca-a-cerrar-la-primera-vuelta-con-victoria/amp) |
| S21 | 2023/2024 / 4 | 2023-09-01 → 2023-12-23 | Club Atlético de Madrid–Sevilla FC 2023-12-23 | **UNRESOLVED** — Sevilla official notice indexed 23 December reschedule; opened page yielded no readable body. Do not certify weather explanation from memory. [D35](https://sevillafc.es/actualidad/noticias/fecha-atletico-sevilla-aplazado-2324) |
| S22 | 2023/2024 / 13 | 2023-11-10 → 2023-11-29 | RCD Mallorca–Cádiz CF 2023-11-29 | **EXPLAINED** — Cadiz official announcement gives 29 November and extended international release window as postponement reason. [D39](https://www.cadizcf.com/noticias/el-partido-aplazado-ante-el-mallorca-ya-tiene-nueva-fecha) |
| S23 | 2023/2024 / 20 | 2024-01-12 → 2024-02-01 | FC Barcelona–CA Osasuna 2024-01-31; Club Atlético de Madrid–Rayo Vallecano de Madrid 2024-01-31; Getafe CF–Real Madrid CF 2024-02-01 | **EXPLAINED** — League result page confirms all three late fixtures January31/February1 and scores. Super Cup mechanism is not separately certified by this page. [D59](https://www.laliga.com/es-DE/noticias/horarios-de-la-jornada-20-de-laliga-ea-sports), [D63](https://www.laliga.com/laliga-easports/resultados/2023-24/jornada-20) |
| S24 | 2023/2024 / 26 | 2024-02-23 → 2024-04-04 | Granada CF–Valencia CF 2024-04-04 | **EXPLAINED** — Valencia official ticket notice explicitly links 4 April postponement to Campanar fire. [D97](https://www.valenciacf.com/cuando-y-donde-ver-en-directo-el-granada-cf-valencia-cf1), [D98](https://www.valenciacf.com/ya-a-la-venta-las-entradas-de-publico-visitante-para-el-partido-del-valencia-cf-ante-el-granada-cf) |
| S25 | 2024/2025 / 3 | 2024-08-26 → 2024-09-18 | Real Betis Balompié–Getafe CF 2024-09-18 | **EXPLAINED** — RFEF appeal records actual Betis-Getafe on 18 September; club report confirms 2-1 and postponed round3. Specific Conference League cause remains unverified. [D33](https://rfef.es/sites/default/files/sanciones/Apelaci%C3%B3n%20Primera%20Divisi%C3%B3n%2C%20Jornada%203%20%28aplazado%29.pdf), [D75](https://www.realbetisbalompie.es/noticias/primer-equipo/cronica-el-real-betis-encadena-su-segunda-victoria-consecutiva-tras-vencer-al-getafe-2-1-30543) |
| S26 | 2024/2025 / 12 | 2024-11-01 → 2025-01-03 | Villarreal CF–Rayo Vallecano de Madrid 2024-12-18; Valencia CF–Real Madrid CF 2025-01-03 | **EXPLAINED** — League updated schedule gives Villarreal-Rayo 18 December and Valencia-Madrid 3 January. DANA cause appears in indexed league statement; exact proposed-date chain not fully certified. [D66](https://www.laliga.com/noticias/horarios-de-la-jornada-12-de-laliga-ea-sports-2024-25), [D62](https://www.laliga.com/es-US/noticias/nota-informativa-sobre-la-confirmacion-nuevas-fechas-partidos-aplazados-por-la-dana-y-solicitud-un-minuto-de-silencio) |
| S27 | 2024/2025 / 13 | 2024-11-08 → 2024-12-18 | RCD Espanyol de Barcelona–Valencia CF 2024-12-18 | **EXPLAINED** — RFEF expressly identifies DANA postponement and sets Espanyol-Valencia for 18 December. [D23](https://rfef.es/es/noticias/el-rcd-espanyol-valencia-se-jugara-el-18-de-diciembre) |
| S28 | 2024/2025 / 19 | 2024-12-03 → 2025-01-13 | RCD Mallorca–FC Barcelona 2024-12-03; Athletic Club–Real Madrid CF 2024-12-04 | **EXPLAINED** — League explicitly advances Mallorca-Barcelona to 3 December and Athletic-Madrid to 4 December. [D67](https://www.laliga.com/noticias/horarios-de-los-partidos-adelantados-de-la-jornada-19-de-laliga-ea-sports) |
| S29 | 2024/2025 / 26 | 2025-02-28 → 2025-04-27 | Villarreal CF–RCD Espanyol de Barcelona 2025-04-27 | **EXPLAINED** — RFEF second-instance order sets Villarreal-Espanyol for 27 April; detailed reason/earlier date sequence not fully certified. [D24](https://rfef.es/es/noticias/nueva-fecha-para-el-villarreal-cf-rcd-espanyol-de-barcelona) |
| S30 | 2024/2025 / 27 | 2025-03-08 → 2025-03-27 | FC Barcelona–CA Osasuna 2025-03-27 | **EXPLAINED** — RFEF scheduling appeal retains 27 March; later discipline appeal confirms actual Barcelona-Osasuna 3-0 and rejects ineligibility complaint. [D26](https://rfef.es/es/noticias/resolucion-de-segunda-instancia-fc-barcelona-ca-osasuna), [D34](https://rfef.es/sites/default/files/sanciones/Apelacion_Primera_Division_Jornada_27__FC_Barcelona_-_C_AT_Osasuna_.pdf) |
| S31 | 2025/2026 / 6 | 2025-08-27 → 2025-09-25 | RC Celta–Real Betis 2025-08-27 | **EXPLAINED** — Celta actual report dated 27 August confirms 1-1 and explicit advancement of round6 for European commitments. [D21](https://rccelta.es/equipo/actualidad/el-celta-perdona-y-el-betis-sobrevive-celta-1-1-betis/) |
| S32 | 2025/2026 / 19 | 2025-12-02 → 2026-01-12 | Barcelona–Atlético de Madrid 2025-12-02; Athletic Club–Real Madrid C.F. 2025-12-03 | **EXPLAINED** — League explicitly advances round19 matches to 2/3 December for Spanish Super Cup; no individual final-score verification claimed. [D58](https://www.laliga.com/es-BR/noticias/horarios-de-los-partidos-adelantados-de-la-jornada-19-de-laliga-ea-sports-2025-26) |
| S33 | 2025/2026 / 16 | 2025-12-12 → 2026-02-18 | Levante UD–Villarreal 2026-02-18 | **EXPLAINED** — League postpones 14 December for red rain warning; Levante February notice identifies Villarreal as Wednesday18 February opponent. No final-score certification. [D68](https://www.laliga.com/noticias/nota-informativa-aplazado-el-levante-ud-villarreal-cf-tras-los-avisos-de-alerta-roja-por-fuertes-lluvias), [D70](https://www.levanteud.com/noticias/fbr-comunicado-oficial-del-levante-ud) |
| S34 | 2025/2026 / 23 | 2026-02-06 → 2026-03-04 | Rayo Vallecano–Real Oviedo 2026-03-04 | **EXPLAINED** — RFEF first ruling challenges suspension; 25 February second-instance decision annuls it and exhausts federation route. Club advertises 4 March; no final-score or later civil-litigation certification. [D32](https://rfef.es/sites/default/files/sanciones/15_Resolucion_JUCP_Expdte_12_T_25-26.pdf), [D27](https://rfef.es/sites/default/files/2026-02/resolucion_cnsi_expdte_51_suspension_partido_rv-oviedo_vf_signed.pdf), [D73](https://www.rayovallecano.es/noticias/entradas-para-el-rayo-vallecano-real-oviedo-del-miercoles-4-de-marzo) |

The eleven unresolved/partial rounds are S01, S02, S08, S12, S13, S15, S16, S18, S19, S20 and S21. Their unsupported dates, causes or document access are specified above. Forty-nine diagnostic outliers lack separate full-fact certification even where their round has an explanation.

One league scheduling announcement headed matchdays 4/9 also includes Athletic–Real Madrid on 22 December, which belongs to round 21, while the reverse Real Madrid–Athletic round-9 fixture was on 1 December according to an indexed contemporary report. This is an ambiguity in the verification document, **not evidence to change the acquired match dates**. Similarly, the Valencia–Madrid rescheduling chain includes a proposed 2 January date while the updated league page gives 3 January; the original source is unchanged.

## Exceptional matches and proposed policy

### Real Madrid–Rayo, 20 December 2015, 10–2

LaLiga’s actual-match narrative ends at 10–2 and describes the goals and dismissals. This establishes a played result, not an administrative award. Propose retaining 10–2 and documenting the high-score review; no correction/exclusion is justified by the unusually large score alone. [D54](https://www.laliga.com/en-GB/news/bale-hits-four-as-real-madrid-swamp-rayo-10-2)

### Real Madrid–Real Sociedad, started 12 December 2004; completed 5 January 2005

Contemporary reporting describes the December bomb-threat interruption at 1–1 and the remaining six minutes completed on 5 January, when Zidane’s penalty produced the final 2–1. The acquired 2005-01-05 date is the completion date; it is not intrinsically false. Propose an explicit resumption flag and a user-approved date convention: original kickoff date for match chronology plus private completion/as-of metadata, or HOLD OUT until the eight-column representation is agreed. A final score must not become available to a historical prediction before the completion date. No date/score has been changed. [D07](https://elpais.com/deportes/2005/01/05/actualidad/1104913316_850215.html), [D14](https://elpais.com/diario/2005/01/05/deportes/1104879604_850215.html)

### Granada–Athletic, started 10 December 2023; completed 11 December 2023

RFEF orders resumption from minute 17 on 11 December following a spectator’s death. The contemporary live report confirms the completed 1–1; the original interruption was at 0–1. The stored 11 December is the completion date. Apply the same proposed explicit date/as-of policy as above; do not call it an unconditional one-day source correction or a new replay. [D03](https://as.com/futbol/primera/granada-athletic-en-directo-laliga-ea-sports-en-vivo-n/), [D22](https://rfef.es/es/noticias/el-granada-athletic-se-reanudara-este-lunes-las-21-horas)

### Barcelona–Osasuna, 27 March 2025, 3–0

The inspected RFEF appeal decision dated 8 May 2025 states the played date and 3–0 score and rejects Osasuna’s appeal against the 11 April discipline decision on alleged Íñigo Martínez ineligibility. The scheduling appeals and later eligibility complaint are separate proceedings. Propose retaining the played result with the appeal note; do not invent an administrative loss. No later judicial-finality claim is made. [D34](https://rfef.es/sites/default/files/sanciones/Apelacion_Primera_Division_Jornada_27__FC_Barcelona_-_C_AT_Osasuna_.pdf)

### Rayo–Oviedo, scheduled 4 March 2026

The first ruling of 19 February questions the authority for the postponement and records Oviedo’s requested 0–3 award. The inspected second-instance ruling of 25 February **annuls that first ruling** and says the federation route is exhausted while civil jurisdiction remains open; a club ticket notice supports the 4 March schedule. A requested award is not an awarded result. The actual final score and any later litigation were not independently certified here; preserve the source and unresolved outcome/status, with no invented 0–3 or exclusion. [D27](https://rfef.es/sites/default/files/2026-02/resolucion_cnsi_expdte_51_suspension_partido_rv-oviedo_vf_signed.pdf), [D32](https://rfef.es/sites/default/files/sanciones/15_Resolucion_JUCP_Expdte_12_T_25-26.pdf), [D73](https://www.rayovallecano.es/noticias/entradas-para-el-rayo-vallecano-real-oviedo-del-miercoles-4-de-marzo)

No other verified award, annulment or replay requiring a data change was established in this bounded review. This is not proof that none exists. Proposed corrections/exclusions applied: **zero**. The two resumption cases require policy approval; eight sample records, eleven round explanations/partial explanations and the Rayo–Oviedo final-outcome question retain their stated limits. No blanket training eligibility is assigned.

## Club-label review

No global name mapping was applied. Sixteen groups look like spelling/abbreviation/location-prefix variants in the selected fixture context; that classification is not a legal continuity certificate.

| Group | Observed labels | Finding |
|---|---|---|
| Athletic Bilbao | Athletic Bilbao, Athletic Club | SPELLING_OR_ABBREVIATION_CANDIDATE: Observed labels appear to be spelling, diacritic, location or club-prefix expansions for the same sporting side within scope. This is a linguistic/fixture-context assessment, not proof of legal continuity or an approved global mapping.  |
| Atletico Madrid | Atletico Madrid, Atlético Madrid, Atlético de Madrid, Club Atlético de Madrid | SPELLING_OR_ABBREVIATION_CANDIDATE: Observed labels appear to be spelling, diacritic, location or club-prefix expansions for the same sporting side within scope. This is a linguistic/fixture-context assessment, not proof of legal continuity or an approved global mapping.  |
| CD Alaves | CD Alaves, CD Alavés, Deportivo Alavés | SPELLING_OR_ABBREVIATION_CANDIDATE: Observed labels appear to be spelling, diacritic, location or club-prefix expansions for the same sporting side within scope. This is a linguistic/fixture-context assessment, not proof of legal continuity or an approved global mapping.  |
| Cadiz CF | Cadiz CF, Cádiz CF | SPELLING_OR_ABBREVIATION_CANDIDATE: Observed labels appear to be spelling, diacritic, location or club-prefix expansions for the same sporting side within scope. This is a linguistic/fixture-context assessment, not proof of legal continuity or an approved global mapping.  |
| Celta Vigo | Celta Vigo, RC Celta, RC Celta de Vigo | SPELLING_OR_ABBREVIATION_CANDIDATE: Observed labels appear to be spelling, diacritic, location or club-prefix expansions for the same sporting side within scope. This is a linguistic/fixture-context assessment, not proof of legal continuity or an approved global mapping.  |
| Deportivo La Coruna | Deportivo La Coruna, Deportivo La Coruña | SPELLING_OR_ABBREVIATION_CANDIDATE: Observed labels appear to be spelling, diacritic, location or club-prefix expansions for the same sporting side within scope. This is a linguistic/fixture-context assessment, not proof of legal continuity or an approved global mapping.  |
| Espanyol Barcelona | Espanyol Barcelona, RCD Espanyol, RCD Espanyol de Barcelona | SPELLING_OR_ABBREVIATION_CANDIDATE: Observed labels appear to be spelling, diacritic, location or club-prefix expansions for the same sporting side within scope. This is a linguistic/fixture-context assessment, not proof of legal continuity or an approved global mapping.  |
| FC Barcelona | Barcelona, FC Barcelona | SPELLING_OR_ABBREVIATION_CANDIDATE: Observed labels appear to be spelling, diacritic, location or club-prefix expansions for the same sporting side within scope. This is a linguistic/fixture-context assessment, not proof of legal continuity or an approved global mapping.  |
| Malaga CF | Malaga CF, Málaga CF | IDENTITY_BOUNDARY: Current Malaga CF derives from Atletico Malagueno name change in 1994. Do not merge CD Malaga into it merely because the city/name agrees. Official history explicitly describes the 1994 rename; distinct registration detail remains indexed only. [D72](https://www.malagacf.com/1994-2001-el-regreso-a-la-elite) |
| Rayo Vallecano | Rayo Vallecano, Rayo Vallecano de Madrid | SPELLING_OR_ABBREVIATION_CANDIDATE: Observed labels appear to be spelling, diacritic, location or club-prefix expansions for the same sporting side within scope. This is a linguistic/fixture-context assessment, not proof of legal continuity or an approved global mapping.  |
| Real Betis | Real Betis, Real Betis Balompié | SPELLING_OR_ABBREVIATION_CANDIDATE: Observed labels appear to be spelling, diacritic, location or club-prefix expansions for the same sporting side within scope. This is a linguistic/fixture-context assessment, not proof of legal continuity or an approved global mapping.  |
| Real Madrid | Real Madrid, Real Madrid C.F., Real Madrid CF | SPELLING_OR_ABBREVIATION_CANDIDATE: Observed labels appear to be spelling, diacritic, location or club-prefix expansions for the same sporting side within scope. This is a linguistic/fixture-context assessment, not proof of legal continuity or an approved global mapping.  |
| Real Sociedad | Real Sociedad, Real Sociedad de Fútbol | SPELLING_OR_ABBREVIATION_CANDIDATE: Observed labels appear to be spelling, diacritic, location or club-prefix expansions for the same sporting side within scope. This is a linguistic/fixture-context assessment, not proof of legal continuity or an approved global mapping.  |
| Real Valladolid | Real Valladolid, Real Valladolid CF | SPELLING_OR_ABBREVIATION_CANDIDATE: Observed labels appear to be spelling, diacritic, location or club-prefix expansions for the same sporting side within scope. This is a linguistic/fixture-context assessment, not proof of legal continuity or an approved global mapping.  |
| Sevilla FC | Sevilla, Sevilla FC | SPELLING_OR_ABBREVIATION_CANDIDATE: Observed labels appear to be spelling, diacritic, location or club-prefix expansions for the same sporting side within scope. This is a linguistic/fixture-context assessment, not proof of legal continuity or an approved global mapping.  |
| Sporting Gijon | Sporting Gijon, Sporting Gijón | SPELLING_OR_ABBREVIATION_CANDIDATE: Observed labels appear to be spelling, diacritic, location or club-prefix expansions for the same sporting side within scope. This is a linguistic/fixture-context assessment, not proof of legal continuity or an approved global mapping.  |
| UD Almeria | UD Almeria, UD Almería | SPELLING_WITH_IDENTITY_BOUNDARY: Accent-only labels within scope. League 2005/06 annual report identifies Union Deportiva Almeria founded 1989; do not map a different AD Almeria identity by city string. Earlier AD legal history not independently certified. [D04](https://assets.laliga.com/assets/2019/12/17/originals/89afda2c9b0d68df72c33407c5e27d96.pdf) |
| Villarreal CF | Villarreal, Villarreal CF | SPELLING_OR_ABBREVIATION_CANDIDATE: Observed labels appear to be spelling, diacritic, location or club-prefix expansions for the same sporting side within scope. This is a linguistic/fixture-context assessment, not proof of legal continuity or an approved global mapping.  |

Málaga’s official history directly supports the 1994 Atlético Malagueño → Málaga CF name change; the detail that CD Málaga and Atlético Malagueño held distinct registrations was only available in indexed text during this review. The league annual report identifies UD Almería as founded in 1989. Do not generalize either city name across predecessor/different clubs. The five explicitly scoped 2012/13 diagnostic name correspondences and all 90 excluded historical 1986/87 `phase2` rows remain unchanged.

## Reproduction, integrity and verification

Run from the original worktree with existing dependencies (nothing installed):

```sh
PYTHONPATH=src:. .venv/bin/python -B -m scripts.verify_la_liga_review --check
PYTHONPATH=src:. .venv/bin/python -B -m scripts.validate_la_liga_structure --check
PYTHONPATH=src:. .venv/bin/python -B -m scripts.inventory_la_liga_history --check
PYTHONPATH=src:. .venv/bin/python -B -m scripts.validate_la_liga_feasibility --check
PYTHONPATH=src:. .venv/bin/python -B -m pytest tests/test_la_liga_review.py tests/test_la_liga_structure.py tests/test_la_liga_history.py tests/test_la_liga_feasibility.py -q -p no:cacheprovider
```

The evidence checker rejects lost seasons, nonunique sampling, changed original hashes/lines/facts, duplicate JSON keys, unsupported indexed-only verification, unexplained team correspondence, score/date contradictions, lost cases/outliers, blanket fixture claims from round explanations, and applied transformations. It deterministically regenerates the private assessment and seals evidence/code/test hashes. It validates the **recorded review**, not external historical truth; human transcriptions and URLs remain auditable and external pages may change.

Initial focused run: **92 passed** (27 Phase 5 guards plus 65 earlier La Liga tests). Final regression and integrity results are appended below after execution. Seven previously unverified app/launcher tests remain a separate regression-check item for final project closure; no new UI-test pass is claimed.

## Files and privacy

Public files created this phase: `scripts/verify_la_liga_review.py`, `tests/test_la_liga_review.py`, `docs/la-liga-historical-review.md`. `PLANNING_LOG.md` is append-only. Phase 2–4 public documentation/scripts/tests remain byte-identical.

New Git-ignored files under `data/private/spain/la_liga/`:

- `phase5_protected_before.json` — 485 pre-review fingerprints.
- `phase5_sample_selection.json` — frozen deterministic selection with source identities.
- `phase5_document_discovery.json` — search/discovery metadata, not inspected-evidence certification.
- `phase5_document_access.json` — additional discovery/access metadata.
- `phase5_review_sources.json` — initial targeted URL/access binding snapshot; later inspected access is recorded in the ledger.
- `phase5_historical_review.json` — manually reviewed 36 samples, six supplemental fixtures, 34 full round contexts/52 outliers, 18 label groups, proposed policy, source access and limitations.
- `phase5_evidence_check.json` — deterministic counts and SHA-256 seals.

Only targeted documentary pages were researched. No new season dataset or Football-Data request was made. Original licensing/provenance and unresolved downstream model-training/redistribution rights remain unchanged. Private artifacts and pre-existing `.DS_Store` files must remain excluded from Git; no staging occurred.

## Documentary index

Access labels describe readable text availability, not automatic verification of every statement. Publication dates marked “not established” remain explicitly unknown; event dates above must not be mistaken for publication dates. Source-specific factual/independence limits are in the sample/case findings and private ledger.

| ID | Document | Publication date | Access |
|---|---|---|---|
| D01 | [LaLiga anuncia las fechas de los partidos aplazados por el Virus CONMEBOL - AS.com](https://as.com/futbol/2021/11/17/primera/1637171450_840773.html) | Not separately established | INDEXED_ONLY |
| D02 | [El Atleti sigue en su derrumbe - AS.com](https://as.com/futbol/2022/02/16/primera/1645032626_333477.html) | Not separately established | INDEXED_ONLY |
| D03 | [Granada 1 - Athletic 1, en directo: resumen, goles y resultado - AS.com](https://as.com/futbol/primera/granada-athletic-en-directo-laliga-ea-sports-en-vivo-n/) | Not separately established | DOCUMENT_OPENED |
| D04 | [portadas memoria 05/06](https://assets.laliga.com/assets/2019/12/17/originals/89afda2c9b0d68df72c33407c5e27d96.pdf) | Not separately established | DOCUMENT_OPENED |
| D05 | [El Betis-Atlético se disputará el 26 de septiembre a las 21.00 horas / Deportes / Cadena SER](https://cadenaser.com/ser/2012/09/03/deportes/1346628495_850215.html) | Not separately established | INDEXED_ONLY |
| D06 | [Un gol anulado al Barcelona en tiempo de descuento evita la derrota del Madrid / Deportes / EL PAÍS](https://elpais.com/deportes/2001/03/03/actualidad/983607715_850215.html) | 2001-03-03 | DOCUMENT_OPENED |
| D07 | [El Madrid gana a la Real Sociedad de penalti en los seis minutos aplazados / Deportes / EL PAÍS](https://elpais.com/deportes/2005/01/05/actualidad/1104913316_850215.html) | Not separately established | DOCUMENT_OPENED |
| D08 | [El Real Madrid gana 'a la italiana' / Deportes / EL PAÍS](https://elpais.com/diario/1993/01/31/deportes/728434815_850215.html) | Not separately established | DOCUMENT_OPENED |
| D09 | [El Madrid se impuso a la ltaliana / Deportes / EL PAÍS](https://elpais.com/diario/1996/12/08/deportes/849999611_850215.html) | Not separately established | DOCUMENT_OPENED |
| D10 | [Un Barça eficaz gana el Bernabéu / Hemeroteca / EL PAÍS](https://elpais.com/diario/1997/11/02/portada/878425203_850215.html?outputType=amp) | 1997-11-02 | DOCUMENT_OPENED |
| D11 | [Un resultado inédito / Deportes / EL PAÍS](https://elpais.com/diario/1998/09/20/deportes/906242407_850215.html?outputType=amp) | 1998-09-20 | DOCUMENT_OPENED |
| D12 | [El Madrid dispara su euforia / Deportes / EL PAÍS](https://elpais.com/diario/2000/02/27/deportes/951606016_850215.html) | Not separately established | INDEXED_ONLY |
| D13 | [Dos directos a la mandíbula / Deportes / EL PAÍS](https://elpais.com/diario/2001/11/05/deportes/1004914802_850215.html) | Not separately established | DOCUMENT_OPENED |
| D14 | [Seis minutos de estrategia / Deportes / EL PAÍS](https://elpais.com/diario/2005/01/05/deportes/1104879604_850215.html) | Not separately established | DOCUMENT_OPENED |
| D15 | [El Valladolid salva un punto / UEFA.com](https://es.uefa.com/news-media/news/0215-0e8aab60f2d4-59ba1cbeec8d-1000--el-valladolid-salva-un-punto/) | Not separately established | INDEXED_ONLY |
| D16 | [El Real Madrid recupera la tercera plaza / UEFA.com](https://es.uefa.com/news-media/news/0242-0f8e5d90441a-f425072d9fe9-1000--el-real-madrid-recupera-la-tercera-plaza/) | Not separately established | DOCUMENT_OPENED |
| D17 | [El Partido del Bernabéu / Crónica, Mundo Deportivo p7](https://hemeroteca-paginas.mundodeportivo.com/EMD01/HEM/1991/06/09/MD19910609-007.pdf) | 1991-06-09 | DOCUMENT_OPENED |
| D18 | [Mundo Deportivo, match technical sheet p8](https://hemeroteca-paginas.mundodeportivo.com/EMD01/HEM/1991/10/20/MD19911020-008.pdf) | 1991-10-20 | DOCUMENT_OPENED |
| D19 | [Super punto, Mundo Deportivo p2](https://hemeroteca-paginas.mundodeportivo.com/EMD01/HEM/1995/10/01/MD19951001-002.pdf) | 1995-10-01 | DOCUMENT_OPENED |
| D20 | [Real Madrid - Barcelona (2-0) - League - 01/03/2020 / FC Barcelona Players](https://players.fcbarcelona.com/en/match/f1075071-real-madrid-barcelona) | Not separately established | INDEXED_ONLY |
| D21 | [El Celta perdona y el Betis sobrevive / Celta 1-1 Betis / Celta](https://rccelta.es/equipo/actualidad/el-celta-perdona-y-el-betis-sobrevive-celta-1-1-betis/) | Not separately established | DOCUMENT_OPENED |
| D22 | [El Granada-Athletic se reanudará este lunes a las 21 horas / www.rfef.es](https://rfef.es/es/noticias/el-granada-athletic-se-reanudara-este-lunes-las-21-horas) | 2023-12-11 | DOCUMENT_OPENED |
| D23 | [El RCD Espanyol-Valencia se jugará el 18 de diciembre / www.rfef.es](https://rfef.es/es/noticias/el-rcd-espanyol-valencia-se-jugara-el-18-de-diciembre) | 2024-11-14 | DOCUMENT_OPENED |
| D24 | [Nueva fecha para el Villarreal CF - RCD Espanyol de Barcelona / www.rfef.es](https://rfef.es/es/noticias/nueva-fecha-para-el-villarreal-cf-rcd-espanyol-de-barcelona) | 2025-03-13 | DOCUMENT_OPENED |
| D25 | [OFICIAL / Competición fija el clásico FC Barcelona - Real Madrid CF para el 18 de diciembre / www.rfef.es](https://rfef.es/es/noticias/oficial-competicion-fija-el-clasico-fc-barcelona-real-madrid-cf-para-el-18-de-diciembre) | Not separately established | DOCUMENT_OPENED |
| D26 | [Resolución de Segunda Instancia: FC Barcelona - CA Osasuna / www.rfef.es](https://rfef.es/es/noticias/resolucion-de-segunda-instancia-fc-barcelona-ca-osasuna) | 2025-03-20 | DOCUMENT_OPENED |
| D27 | [REAL FEDERACIÓN ESPAÑOLA DE FÚTBOL](https://rfef.es/sites/default/files/2026-02/resolucion_cnsi_expdte_51_suspension_partido_rv-oviedo_vf_signed.pdf) | 2026-02-25 | DOCUMENT_OPENED |
| D28 | [Real Federación Española de Fútbol](https://rfef.es/sites/default/files/images19/acuerdo_comite_nueva_fecha.pdf) | 2020-02-19 | DOCUMENT_OPENED |
| D29 | [-](https://rfef.es/sites/default/files/images19/partido_aplazado_1a_3.pdf) | Not separately established | DOCUMENT_OPENED |
| D30 | [PARTIDOS DE 1ª DIVISIÓN - JORNADA 4 -](https://rfef.es/sites/default/files/images19/partidos_1a_division_211217_154720.pdf) | Not separately established | DOCUMENT_OPENED |
| D31 | [COMITÉ TÉCNICO DE ÁRBITROS](https://rfef.es/sites/default/files/images19/partidos_aplazados_1a_division.pdf) | Not separately established | DOCUMENT_OPENED |
| D32 | [REAL FEDERACIÓN ESPAÑOLA DE FÚTBOL](https://rfef.es/sites/default/files/sanciones/15_Resolucion_JUCP_Expdte_12_T_25-26.pdf) | 2026-02-19 | DOCUMENT_OPENED |
| D33 | [Dominio de Intranet](https://rfef.es/sites/default/files/sanciones/Apelaci%C3%B3n%20Primera%20Divisi%C3%B3n%2C%20Jornada%203%20%28aplazado%29.pdf) | Not separately established | DOCUMENT_OPENED |
| D34 | [Dominio de Intranet](https://rfef.es/sites/default/files/sanciones/Apelacion_Primera_Division_Jornada_27__FC_Barcelona_-_C_AT_Osasuna_.pdf) | 2025-05-08 | DOCUMENT_OPENED |
| D35 | [EL ATLÉTICO DE MADRID-SEVILLA FC SE JUGARÁ EL SÁBADO 23 DE DICIEMBRE / Sevilla FC](https://sevillafc.es/actualidad/noticias/fecha-atletico-sevilla-aplazado-2324) | Not separately established | INDEXED_ONLY |
| D36 | [Clasificación del Atlético de Madrid en LaLiga](https://www.atleticodemadrid.com/clasificacion-primer-equipo-2020-2021) | Not separately established | INDEXED_ONLY |
| D37 | [Real Madrid–Barcelona, 7 May 1994](https://www.bdfutbol.com/es/p/p.php?id=19360) | Not separately established | INDEXED_ONLY |
| D38 | [Barcelona v Elche - as it happened](https://www.besoccer.com/new/barcelona-v-elche-as-it-happened-959759) | Not separately established | INDEXED_ONLY |
| D39 | [El partido aplazado ante el Mallorca ya tiene nueva fecha / Cádiz Club de Fútbol / Web Oficial](https://www.cadizcf.com/noticias/el-partido-aplazado-ante-el-mallorca-ya-tiene-nueva-fecha) | Not separately established | DOCUMENT_OPENED |
| D40 | [Jornada extra en Comunio: Levante - Atlético](https://www.comuniate.com/noticias/8142/jornada-extra-en-comunio-levante-atletico) | Not separately established | INDEXED_ONLY |
| D41 | [El Barça, a dos partidos de la Liga perfecta](https://www.elnacional.cat/es/en-directo-deportes/barca-villarreal-liga_2796_126.html) | Not separately established | INDEXED_ONLY |
| D42 | [A hectic fixture list to round off the year](https://www.fcbarcelona.com/en/football/first-team/actualites/1898219/le-calendrier-de-la-fin-dannee-2020/featured) | Not separately established | DOCUMENT_OPENED |
| D43 | [Three new kick off times confirmed for FC Barcelona](https://www.fcbarcelona.com/en/football/first-team/news/1922697/three-new-kick-off-times-confirmed-for-fc-barcelona/featured) | Not separately established | DOCUMENT_OPENED |
| D44 | [Real Madrid 0-4 Barça: The Clásico is blaugrana!](https://www.fcbarcelona.com/en/football/first-team/news/2544426/real-madrid-0-4-barca-the-clasico-is-blaugrana/featured) | 2022-03-20 | DOCUMENT_OPENED |
| D45 | [Real Madrid 0-4 FC Barcelona: Viva la vida!](https://www.fcbarcelona.com/en/football/first-team/news/4156771/real-madrid-04-fc-barcelona-viva-la-vida) | 2024-10-26 | DOCUMENT_OPENED |
| D46 | [Training schedule ahead of busy week with two league matches](https://www.fcbarcelona.com/en/news/1070912/training-schedule-ahead-of-busy-week-with-two-league-matches) | Not separately established | DOCUMENT_OPENED |
| D47 | [11 years to the day since the 6-2 away win against Real Madrid](https://www.fcbarcelona.com/en/news/1663569/11-years-to-the-day-since-the-6-2-away-win-against-real-madrid) | 2020-05-02 | DOCUMENT_OPENED |
| D48 | [15 years to the day since a famous 'Clásico'](https://www.fcbarcelona.com/en/news/1899174/15-years-to-the-day-since-a-famous-clsico) | 2020-11-19 | DOCUMENT_OPENED |
| D49 | [Laporta gets his hands on the Clásico shirt](https://www.fcbarcelona.com/en/news/2096982/laporta-gets-his-hands-on-the-clasico-shirt) | Not separately established | DOCUMENT_OPENED |
| D50 | [Madrid – Barça: Ya es un Clásico (0-1)](https://www.fcbarcelona.es/es/futbol/primer-equipo/noticias/1085320/reial-madrid-barca-ya-es-un-clasico-0-1) | 2019-03-02 | DOCUMENT_OPENED |
| D51 | [El Barça - Rayo Vallecano ya tiene fecha y hora](https://www.fcbarcelona.es/es/noticias/2513425/el-barca-rayo-vallecano-ya-tiene-fecha-y-hora) | Not separately established | DOCUMENT_OPENED |
| D52 | [Betis - Barça: A cerrar la primera vuelta con victoria](https://www.fcbarcelona.es/es/noticias/3041872/betis-barca-a-cerrar-la-primera-vuelta-con-victoria/amp) | Not separately established | INDEXED_ONLY |
| D53 | [Calendario 20/21 / LALIGA](https://www.laliga.com/calendario-2020-2021/laliga-santander) | Not separately established | INDEXED_ONLY |
| D54 | [Bale hits four as Real Madrid swamp Rayo 10-2 / LALIGA](https://www.laliga.com/en-GB/news/bale-hits-four-as-real-madrid-swamp-rayo-10-2) | Not separately established | DOCUMENT_OPENED |
| D55 | [Kick-off times confirmed for postponed matches from Matchdays 4 and 9 / LALIGA](https://www.laliga.com/en-GB/news/kick-off-times-confirmed-for-postponed-matches-from-matchdays-4-and-9) | Not separately established | DOCUMENT_OPENED |
| D56 | [Official statement / LALIGA](https://www.laliga.com/en-GB/news/official-statement-jan-9-2021) | Not separately established | DOCUMENT_OPENED |
| D57 | [The postponed game Valencia CF v Real Madrid will be played on February 22 / LALIGA](https://www.laliga.com/en-GB/news/the-postponed-game-valencia-cf-v-real-madrid-will-be-played-on-february-22) | Not separately established | DOCUMENT_OPENED |
| D58 | [Horarios de los partidos adelantados de la jornada 19 de LALIGA EA SPORTS 2025/26 / LALIGA](https://www.laliga.com/es-BR/noticias/horarios-de-los-partidos-adelantados-de-la-jornada-19-de-laliga-ea-sports-2025-26) | Not separately established | DOCUMENT_OPENED |
| D59 | [Horarios de la jornada 20 de LALIGA EA SPORTS / LALIGA](https://www.laliga.com/es-DE/noticias/horarios-de-la-jornada-20-de-laliga-ea-sports) | Not separately established | INDEXED_ONLY |
| D60 | [Clásicos para recordar / LALIGA](https://www.laliga.com/es-GB/noticias/clasicos-para-recordar) | 2014-10-20 | DOCUMENT_OPENED |
| D61 | [Nota informativa / LALIGA](https://www.laliga.com/es-GB/noticias/nota-informativa-93) | Not separately established | INDEXED_ONLY |
| D62 | [Nota informativa / LALIGA](https://www.laliga.com/es-US/noticias/nota-informativa-sobre-la-confirmacion-nuevas-fechas-partidos-aplazados-por-la-dana-y-solicitud-un-minuto-de-silencio) | Not separately established | INDEXED_ONLY |
| D63 | [Resultados de la Jornada 20 de LALIGA EA SPORTS 2023/24 / LALIGA](https://www.laliga.com/laliga-easports/resultados/2023-24/jornada-20) | Not separately established | DOCUMENT_OPENED |
| D64 | [El Sevilla, en busca de la séptima plaza en el Sánchez-Pizjuán / LALIGA](https://www.laliga.com/noticias/el-sevilla-en-busca-de-la-septima-plaza-en-el-sanchez-pizjuan) | Not separately established | DOCUMENT_OPENED |
| D65 | [Horario del Real Madrid - Sevilla de la jornada 16 de la Liga BBVA / LALIGA](https://www.laliga.com/noticias/horario-del-real-madrid-sevilla-de-la-jornada-16-de-la-liga-bbva) | Not separately established | DOCUMENT_OPENED |
| D66 | [Horarios de la jornada 12 de LALIGA EA SPORTS 2024/25 / LALIGA](https://www.laliga.com/noticias/horarios-de-la-jornada-12-de-laliga-ea-sports-2024-25) | Not separately established | DOCUMENT_OPENED |
| D67 | [Horarios de los partidos adelantados de la jornada 19 de LALIGA EA SPORTS / LALIGA](https://www.laliga.com/noticias/horarios-de-los-partidos-adelantados-de-la-jornada-19-de-laliga-ea-sports) | Not separately established | DOCUMENT_OPENED |
| D68 | [Nota informativa / LALIGA](https://www.laliga.com/noticias/nota-informativa-aplazado-el-levante-ud-villarreal-cf-tras-los-avisos-de-alerta-roja-por-fuertes-lluvias) | Not separately established | DOCUMENT_OPENED |
| D69 | [Pepe Mel y Víctor Sánchez del Amo, ante sus ex / LALIGA](https://www.laliga.com/noticias/pepe-mel-y-victor-sanchez-del-amo-ante-sus-ex) | Not separately established | DOCUMENT_OPENED |
| D70 | [COMUNICADO OFICIAL DEL LEVANTE UD / Levante UD / Web Oficial](https://www.levanteud.com/noticias/fbr-comunicado-oficial-del-levante-ud) | Not separately established | DOCUMENT_OPENED |
| D71 | [1992-1994: Club Atlético Malagueño / Málaga CF / Web Oficial](https://www.malagacf.com/1992-1994-club-atletico-malagueno) | Not separately established | INDEXED_ONLY |
| D72 | [1994-2001: El regreso a la élite / Málaga CF / Web Oficial](https://www.malagacf.com/1994-2001-el-regreso-a-la-elite) | Not separately established | DOCUMENT_OPENED |
| D73 | [Entradas para el Rayo Vallecano - Real Oviedo del miércoles 4 de marzo / Rayo Vallecano / Web Oficial](https://www.rayovallecano.es/noticias/entradas-para-el-rayo-vallecano-real-oviedo-del-miercoles-4-de-marzo) | Not separately established | DOCUMENT_OPENED |
| D74 | [Rayo - Athletic Club el miércoles 24 de octubre a las 19:00 horas / Rayo Vallecano / Web Oficial](https://www.rayovallecano.es/noticias/rayo-athletic-club-el-miercoles-24-de-octubre-a-las-1900-horas) | Not separately established | DOCUMENT_OPENED |
| D75 | [CRÓNICA / El Real Betis encadena su segunda victoria consecutiva tras vencer al Getafe (2-1) - Real Betis Balompié](https://www.realbetisbalompie.es/noticias/primer-equipo/cronica-el-real-betis-encadena-su-segunda-victoria-consecutiva-tras-vencer-al-getafe-2-1-30543) | Not separately established | DOCUMENT_OPENED |
| D76 | [Iván Luis Zamorano Zamora - Historia y palmarés / Web oficial Real Madrid C.F.](https://www.realmadrid.com/es-ES/el-club/historia/leyendas-futbol/ivan-luis-zamorano-zamora) | Not separately established | DOCUMENT_OPENED |
| D77 | [El Real Madrid-Getafe se jugará finalmente el martes, 9 de febrero, a las 21:00 h/ Real Madrid C.F.](https://www.realmadrid.com/es-ES/noticias/futbol/primer-equipo/actualidad/el-real-madrid-getafe-se-jugara-finalmente-el-martes-9-de-febrero-a-las-21-00-h) | Not separately established | DOCUMENT_OPENED |
| D78 | [El Real Madrid-Valencia se jugará el jueves, 2 de febrero, a las 21:00 h/ Real Madrid C.F.](https://www.realmadrid.com/es-ES/noticias/futbol/primer-equipo/actualidad/el-real-madrid-valencia-se-jugara-el-jueves-2-de-febrero-a-las-21-00-h) | Not separately established | DOCUMENT_OPENED |
| D79 | [2-1: Victoria en el Clásico/ Real Madrid C.F.](https://www.realmadrid.com/es-ES/noticias/futbol/primer-equipo/cronicas/2-1-victoria-en-el-clasico) | 2021-04-10 | DOCUMENT_OPENED |
| D80 | [3-1: El Madrid gana el Clásico y es líder/ Real Madrid C.F.](https://www.realmadrid.com/es-ES/noticias/futbol/primer-equipo/cronicas/3-1-el-madrid-gana-el-clasico-y-es-lider) | 2022-10-16 | DOCUMENT_OPENED |
| D81 | [Remontada en el Clásico y 11 puntos de ventaja en el liderato](https://www.realmadrid.com/es-ES/noticias/futbol/primer-equipo/cronicas/cronica-21-04-2024-rm-barcelona) | 2024-04-21 | DOCUMENT_OPENED |
| D82 | [El Madrid gana el Clásico](https://www.realmadrid.com/es-ES/noticias/futbol/primer-equipo/cronicas/cronica-real-madrid-barcelona-jornada-10-liga-26-10-2025) | 2025-10-26 | DOCUMENT_OPENED |
| D83 | [Impulso](https://www.realsociedad.eus/es/noticias/detalle/impulso) | Not separately established | INDEXED_ONLY |
| D84 | [El Celta-Real Madrid se jugará el miércoles 17 de mayo a las 21.00 horas](https://www.rtve.es/deportes/20170505/celta-real-madrid-se-jugara-miercoles-17-mayo-a-2100-horas/1539265.shtml) | Not separately established | DOCUMENT_OPENED |
| D85 | [Barça roar into contention / UEFA.com](https://www.uefa.com/news-media/news/019c-0f8455f60fd3-2767f0f509cd-1000--barca-roar-into-contention/) | 2004-04-25 | DOCUMENT_OPENED |
| D86 | [Madrid triumph in 'El Clásico' / UEFA.com](https://www.uefa.com/news-media/news/01ba-0e6db41cd226-d1a95e3c838e-1000--madrid-triumph-in-el-clasico/) | 2006-10-22 | DOCUMENT_OPENED |
| D87 | [Barça beaten as Villarreal seal second / UEFA.com](https://www.uefa.com/news-media/news/01cd-0f84da0e7cd5-791c157fefc8-1000--barca-beaten-as-villarreal-seal-second/) | 2008-05-07 | DOCUMENT_OPENED |
| D88 | [Ten-man Madrid fight back to deny Barcelona / UEFA.com](https://www.uefa.com/news-media/news/01f0-0e77e658d364-da5f24e31c1d-1000--ten-man-madrid-fight-back-to-deny-barcelona/) | 2011-04-16 | DOCUMENT_OPENED |
| D89 | [Ramos earns Madrid another win against Barça / UEFA.com](https://www.uefa.com/news-media/news/0207-0e9ec7425a92-1ed4dbd30bc6-1000--ramos-earns-madrid-another-win-against-barca/) | 2013-03-02 | DOCUMENT_OPENED |
| D90 | [Messi treble helps Barcelona edge Clásico thriller / UEFA.com](https://www.uefa.com/news-media/news/0213-0e899ae289d9-cf4a91729648-1000--messi-treble-helps-barcelona-edge-clasico-thriller/) | 2014-03-23 | DOCUMENT_OPENED |
| D91 | [Madrid 'dominate' to get better of Barcelona / UEFA.com](https://www.uefa.com/news-media/news/021a-0f8a6f036cdd-c6c02bb540d8-1000--madrid-dominate-to-get-better-of-barcelona/) | 2014-10-25 | DOCUMENT_OPENED |
| D92 | [Spain round-up: Barcelona frustrate Madrid / UEFA.com](https://www.uefa.com/news-media/news/025e-0f9086d577c5-e33ba36a1609-1000--spain-round-up-barcelona-frustrate-madrid/) | 2003-04-19 | DOCUMENT_OPENED |
| D93 | [Barcelona rally to claim Clásico bragging rights / UEFA.com](https://www.uefa.com/news/01f8-0e7c7b3a7400-35a09e92cfaf-1000--barcelona-rally-to-claim-clasico-bragging-rights/) | 2011-12-10 | DOCUMENT_OPENED |
| D94 | [Real Madrid 0-4 Barcelona: what we learned / UEFA Champions League 2015/16 / UEFA.com](https://www.uefa.com/uefachampionsleague/news/0227-0e928ed66790-708b6f41f368-1000--real-madrid-0-4-barcelona-what-we-learned/) | 2015-11-21 | DOCUMENT_OPENED |
| D95 | [Messi sinks Madrid, Juventus and Monaco triumph / UEFA Champions League 2016/17 / UEFA.com](https://www.uefa.com/uefachampionsleague/news/0238-0e96c9f3cce6-13c9b518ea8d-1000--messi-sinks-madrid-juventus-and-monaco-triumph/) | 2017-04-23 | DOCUMENT_OPENED |
| D96 | [Chelsea and Barcelona renew rivalry / UEFA Champions League 2017/18 / UEFA.com](https://www.uefa.com/uefachampionsleague/news/0241-0e983e58104c-837a077fccf3-1000--chelsea-and-barcelona-renew-rivalry/) | Not separately established | DOCUMENT_OPENED |
| D97 | [Cuándo y dónde ver en directo el Granada CF – Valencia CF - Valencia CF](https://www.valenciacf.com/cuando-y-donde-ver-en-directo-el-granada-cf-valencia-cf1) | Not separately established | DOCUMENT_OPENED |
| D98 | [YA A LA VENTA LAS ENTRADAS DE PÚBLICO VISITANTE PARA EL PARTIDO APLAZADO DEL VALENCIA CF ANTE EL GRANADA CF - Valencia CF](https://www.valenciacf.com/ya-a-la-venta-las-entradas-de-publico-visitante-para-el-partido-del-valencia-cf-ante-el-granada-cf) | Not separately established | DOCUMENT_OPENED |

## Final measured verification

- All **739 non-UI regression tests passed** in 7.45 seconds; this includes the 27 new Phase 5 tests. The earlier focused 92-test run also passed. No app/launcher tests were rerun or reclassified.
- Phase 2 feasibility, Phase 3 inventory, Phase 4 structural validation and Phase 5 evidence checks regenerate **byte-identically**.
- All **485 pre-review fingerprints** match, including all **428 artifacts from the six prior competitions**, all 19 frozen Phase 2 files and later frozen La Liga evidence.
- All **482 current private files** are Git-ignored; **zero private files are tracked**. Existing `.DS_Store` files were left untouched and unstaged.
- Tracked diff checks and explicit whitespace checks for all three new public Phase 5 files pass. No files were staged, committed, pushed or merged; branch and HEAD remain unchanged.
- One initial helper invocation omitted `src` from `PYTHONPATH` and failed to import the existing validation module; rerunning with the documented `PYTHONPATH=src:.` succeeded. An optional process listing was denied by the sandbox and was not retried. No installation or permissions change was needed.
- The application and promotional worktree were not modified. No source/standardized data correction, exclusion or final La Liga export was made.

Review gate: approve the proposed exception/date policy before any implementation. The eight unresolved sample verifications, eleven incomplete round explanations, 49 non-certified outliers and Rayo–Oviedo final-outcome/later-proceedings limits remain explicitly visible; none is silently cleared for training.

## Phase 6 — approved historical exception, date and exclusion policy

Date: 2026-11-22. User approved the Phase 5 review and the conservative decisions below. This appended section formalizes processing policy; the earlier Phase 5 narrative remains unchanged as historical evidence. Its exact pre-append bytes are preserved privately in `phase5_historical_review_document_snapshot.md`.

### Approved fixture decisions and exact audit identities

Audit IDs bind the immutable source path, SHA-256 and physical line. They are **not** the shared eight-column `match_id`; eventual standardization must reuse the established shared ID implementation and link these source audit IDs to those IDs in a provenance manifest. No standardized match IDs or rows were generated in Phase 6.

| Decision | Fixture / unchanged source FT | Source location | Approved treatment | Exact source audit ID |
|---|---|---|---|---|
| LL6-01 | Real Madrid–Rayo Vallecano (2015/2016), 10–2 | `openfootball/espana/2015-16/1-liga.txt` line **259** | RETAIN; effective date 2015-12-20 | `laliga:e04048203266049f60f5bccac4400c8e76e20b32ada4209bf82c697821e9be50` |
| LL6-02 | FC Barcelona–CA Osasuna (2024/2025), 3–0 | `openfootball/espana/2024-25/1-liga.txt` line **503** | RETAIN_APPEAL_NOTE; effective date 2025-03-27 | `laliga:6f7a3f038c1c7723977278ac0a01c7e95c38655faf1b939888314c02ddd2b448` |
| LL6-03 | Real Madrid–Real Sociedad (2004/2005), 2–1 | `jalapic/engsoccerdata/data-raw/spain.csv` line **19526** | COMPLETED_INTERRUPTED_MATCH; kickoff 2004-12-12; completion/effective 2005-01-05 | `laliga:c7279b035949311a1c250da70ef5e548f228fca61f9ed1c22a6f01ffa8135298` |
| LL6-04 | Granada CF–Athletic Club (2023/2024), 1–1 | `openfootball/espana/2023-24/1-liga.txt` line **275** | COMPLETED_INTERRUPTED_MATCH; kickoff 2023-12-10; completion/effective 2023-12-11 | `laliga:743e3113d76c733983bdd2e07dd34eeeb6237477639329c55d0f61289dd6ea26` |
| LL6-05 | Rayo Vallecano–Real Oviedo (2025/2026), 3–0 | `openfootball/espana/2025-26/1-liga.txt` line **780** | HOLD_OUT; source date 2026-03-04 retained, recognized final result/applicable date unresolved; effective date null | `laliga:5a6b3dcf91f5e0fa5311fdc6a0249f71cf21c3fa99db993843a33b5697631f87` |

Rayo–Oviedo’s source record is **Rayo Vallecano 3–0 Real Oviedo, 2026-03-04**, round 23, line 780, with recorded halftime 1–0. These are preserved source observations, not a newly verified official outcome. The requested administrative **0–3** is not substituted. `LL6-05` is `UNRESOLVED / HOLD OUT` with no certified completion/effective date. Resolving it requires authoritative final-result/date evidence and a new explicit approved policy decision.

Barcelona–Osasuna retains 3–0 and its existing RFEF 8 May 2025 appeal evidence; Real Madrid–Rayo retains 10–2. Both interrupted matches retain their source dates/scores unchanged and gain separate original-kickoff/completion metadata; completion is their approved effective result-availability date. The Phase 5 evidence URLs are attached to each bound decision. No additional legal finality is claimed.

### Eight-column date and chronological rule

The eventual La Liga schema remains `match_id,date,league,season,home_team,away_team,home_goals,away_goals`. Its **date represents the calendar day the final result became available**. For the two known interrupted matches this is the completion day, not the earlier kickoff day. Source date, original kickoff, completion, original score/raw source line, provenance and the approved decision remain in the private audit sidecar.

For ordinary fixtures, the unchanged source playing date is an explicit **availability proxy**, not independently certified publication/knowledge time. Newly identified interruptions, later administrative outcomes or date conflicts require explicit review. Unknown final-outcome/applicable-date cases receive a null effective date and HOLD OUT, rather than an invented calendar placeholder.

Only results with `effective_result_date < prediction_date` may enter a chronological training/evaluation window. Equality is rejected: no same-day result is assumed known when only date precision exists. A result from the Real Madrid–Real Sociedad fixture is unavailable throughout December 2004 and on 5 January 2005; it can pass the temporal guard from 6 January onward. Granada–Athletic similarly cannot enter a window for 10 or 11 December 2023 and can pass from 12 December onward. Independent training/rights gates must also clear.

`assess()` is the required policy entry point for future screening: it validates the complete approved five-case registry and the unresolved-outcome registry, binds decisions to exact original facts, and refuses missing/reclassified decisions. Every fixture must explicitly state whether an unresolved final-outcome issue has been identified. Any such issue forces HOLD OUT, even if the fixture previously had a retain decision; no runtime waiver exists. A new evidence-backed approved policy revision is needed before inclusion. This is a future-consumer contract tested offline, not an application/model integration.

### Separate classifications and measured decision counts

| Classification | Measured result |
|---|---|
| Explicit exceptional decisions | **5:** retain 1; retain with appeal note 1; completed/interrupted 2; HOLD OUT 1 |
| Structural technical acceptance | 13,844 previously structurally valid source fixtures; unchanged |
| Exception-policy screening candidates | **13,843** — candidates only, not an accepted standardized export |
| Explicit policy HOLD OUT | **1** — exact Rayo–Oviedo fixture |
| Historical factual verification | **34 verified facts / 13,810 unverified**; not whole-population certification |
| Previously unverified sample fixtures | **8 remain unverified and screening candidates**, not erroneous/excluded |
| Scheduling classifications | **34 retained: 23 documented, 8 partial, 3 unresolved** |
| Diagnostic date outliers | **52 visible**, including all **49 without individual full-fact certification** |
| Outlier screening dispositions | **51 candidates / 1 HOLD OUT**, with holdout solely due to explicit Rayo–Oviedo final-outcome uncertainty |
| Model-training suitability cleared | **0** — all remain NOT_CLEARED |
| Licensing clearance granted | **0** — all remain UNRESOLVED |
| Source corrections / standardized rows written | **0 / 0** |

No date is corrected or fixture excluded solely because of a wide round span, partial scheduling explanation, diagnostic-outlier membership or lack of individual historical verification. Those issues remain visible and separate from identified final-outcome conflicts. Historical factual confirmation does not grant licensing or model-training clearance.

### Artifacts and reproducibility

New public implementation: `scripts/decide_la_liga_policy.py` and `tests/test_la_liga_policy.py`. Existing historical-review documentation and `PLANNING_LOG.md` are appended only. New private, Git-ignored artifacts:

- `phase5_historical_review_document_snapshot.md` — exact original Phase 5 report bytes.
- `phase6_history_prefixes.json` — original document/log lengths and SHA-256, enforcing append-only history.
- `phase6_protected_before.json` — **497** protected artifact fingerprints, including prior competitions and all Phase 2–5 evidence.
- `phase6_decision_policy.json` — five bound decisions, original parsed/raw source values, evidence URLs, date rules, all 34 case references, all 52 outlier identities and the eight unverified sample references.
- `phase6_policy_assessment.json` — deterministic reconciliation, exceptional eligibility assessments, source/evidence/code/test hashes; no standardized match export.

```sh
PYTHONPATH=src:. .venv/bin/python -B -m scripts.decide_la_liga_policy --check
PYTHONPATH=src:. .venv/bin/python -B -m pytest tests/test_la_liga_policy.py -q -p no:cacheprovider
```

`--write` creates only the two private policy/assessment artifacts, is offline/idempotent, preflights both outputs and refuses different existing bytes. `--check` regenerates and compares exact bytes without writing. Original match bytes and earlier generated evidence are never rewritten. The immutable Phase 5 report snapshot and append-only prefix seals reconcile preservation with this documentation update.

The 36 focused synthetic tests cover unchanged scores/source facts, both completion-date rules, the Rayo holdout and prohibited score substitution, newly identified unresolved outcomes, missing/changed decision registries, non-exclusion of scheduling candidates, strict date cutoffs, independent training/licensing gates, deterministic source audit IDs, and preservation of earlier outputs and documentation history. Final integration/regression measurements follow below.

Remaining evidence limits are unchanged: eight unverified sample fixtures; eleven partially explained/unresolved scheduling rounds; 49 outliers without individual full-fact certification; and Rayo–Oviedo’s recognized final outcome/date. These are not silently certified. Seven previously unverified app/launcher tests remain a separate final-project regression item. No new data acquisition, standardization, application change, model training or Git publication is authorized by this phase.

### Phase 6 final measured verification and stopping point

- **36 focused policy tests passed**; the final non-UI regression suite reports **775 passed in 7.41 seconds**, including all previous competition/La Liga tests. The seven earlier unverified app/launcher tests remain separate and were not reclassified.
- Two successive Phase 6 policy/assessment regenerations are byte-identical to the saved artifacts. Phase 2 feasibility, Phase 3 inventory, Phase 4 structural validation and Phase 5 evidence checks also reproduce byte-identically.
- All **497 protected fingerprints** match, including all **428 artifacts from the six previous competitions** and frozen Phase 2–5 evidence. Original report/log prefixes match; only authorized appendices were added.
- All **487 private files** are Git-ignored and **zero are tracked**. The Git index remains empty; tracked and new-public-file whitespace checks pass. Pre-existing `.DS_Store` files and unrelated uncommitted work remain untouched.
- The original **13,844 fixtures** are unchanged. Five explicit exception decisions reconcile to **13,843 policy candidates / 1 HOLD OUT**; no final standardized dataset or model/application integration exists. Technical screening candidacy does not imply historical certification, training suitability or licensing clearance.
- Work stayed in the original `toto` worktree on `feature/data-collection`; no acquisition, install, commit, push, merge, model training or promotional/application modification occurred.

Phase 6 stops here. Standardization requires the user's next approval and must consume the complete approved decision registry, preserve source-to-shared-ID provenance, enforce the Rayo–Oviedo holdout and carry the completion-date/uncertainty metadata forward. The remaining historical/access and licensing limitations are unchanged.
