# Primeira Liga — Phase 5 bounded historical evidence review

Review date: 2026-11-23. Branch: `feature/data-collection`. Protected HEAD: `0bb6f393c89fdcc37a52a56bb31e458ff131de47`.

## Scope and decision boundary

This is an evidence assessment, not historical certification or a Phase 6 policy. All originals, source dates/labels/scores and prior outputs remain unchanged. No authoritative source, normalization, accepted/excluded/HOLD OUT/NOT PLAYED disposition or standardized record is selected. Proposals below require explicit Phase 6 approval.

The research objective remains 1990/91–2025/26. Dated coverage represents only 1994/95–2025/26 (32 seasons). The missing four early seasons account for 1,298 expected slots: 380 + 306 + 306 + 306. The RSSSF 1990/91 snapshot has 380 undated result identities; those are not dated observations or NOT PLAYED records.

## Reconciliation and preserved review population

| Measure | Count |
|---|---:|
| Historical observations | 8,958 |
| Modern observations | 2,448 |
| Total source observations | 11,406 |
| Conditional overlap pairs | 2,142 |
| Conditional distinct fixture slots | 9,264 |
| Structurally valid observations | 11,405 |
| Literal-label defect | 1 |
| Flagged source observations | 207 |

Reparsing the nine dated originals, with checksum verification of all ten originals, independently reproduces all six frozen Phase 4 assessment artifacts. The 207 flagged observations have 221 overlapping category memberships, not 221 distinct fixtures. The 26 unusual-score memberships correspond to 18 conditional events (18 historical + eight modern observations). Wide rounds: 18 contexts/162 memberships; reversal pairs: 13 contexts/26 endpoints. Every flagged original and category binding is checked against preserved physical source bytes.

The final registry includes 392 original observations in 228 conditional research groups: all flagged observations, 32 ordinary samples, the newly researched Leiria event, and their diagnostic overlap partners. Exactly 84 observations/74 conditional groups received targeted fixture research attempts; 308 observations/154 groups have only contextual or linked-original review. Targeted research means an actual bounded evidence search, not necessarily successful independent corroboration. Linked counterparts do not inherit documentary confidence automatically.

| Evidence classification | Source observations | Conditional research groups |
|---|---:|---:|
| FULLY CORROBORATED CORE FACTS | 25 | 19 |
| PARTIALLY CORROBORATED | 11 | 10 |
| CONTRADICTED | 3 | 3 |
| UNRESOLVED | 45 | 42 |
| CONTEXT-ONLY REVIEWED | 308 | 154 |

Conditional group counts use conservative priority: contradicted, full core, partial, unresolved, context-only. A group with one completion-date contradiction does not make every partner wrong. These research identities are not canonical match IDs or approved team mappings.

FULLY CORROBORATED CORE FACTS covers teams, league/season, event date, score and completed-match status from directly inspected primary participant/league reports or contemporary journalism. It does not certify administrative finality, appeals, intraday publication or result-availability timestamps. The two Santa Clara CSV dates conflict with independently supported playing/completion dates, but could preserve legitimate kickoff/schedule meanings. The 1995 sample conflict has weaker secondary corroboration and remains provisional. All finality and availability dimensions remain explicitly unresolved in this phase.

## Material conflicts and exceptional cases

| Case | Original source evidence | Inspected finding and limitations | Proposed Phase 6 question |
|---|---|---|---|
| Santa Clara–Paços 2019/20 | CSV line 7290: 2020-02-01, 2–1; modern line 298: 2020-02-02, 2–1 | Direct RTP completed-match narrative supports Feb 2. Indexed VSports postponement and FPF scheduling/protest leads support a scheduling interpretation but are not directly inspected final decisions. No timezone explanation established. | Consider Feb 2 effective completion date; preserve both original dates and seek protest finality. |
| Santa Clara–Benfica 2020/21 | CSV line 7532: Jan 3; modern line 192: Jan 4; both 1–1 | Direct RTP report says Sunday start, Monday completion, 1–1. Article first publication Jan 3 and update Jan 4 are separately visible; club report timed out. Exact interruption minute remains an indexed club lead, not directly established by that inaccessible report. | Preserve Jan 3 kickoff/Jan 4 completion; consider Jan 4 effective date with strict chronology. |
| Belenenses SAD–Benfica 2021/22 | CSV line 7838 and modern line 187: Nov 27 2021, 0–7; modern has no abandonment annotation | Original score agreement is not administrative finality. Indexed reporting indicates early termination/insufficient players; FPF process 33–21/22 decision lead and referee-report lead are not directly inspected. Both relevant official decision retrievals remained HTTP403. | Obtain authoritative final-result, decision/publication and appeal evidence. Consider HOLD OUT only in Phase 6 if finality cannot be established. No disposition assigned now. |
| Feirense–Nacional 2011/12 | CSV line 4877: `Feirense ` (trailing space), Aug 14 2011, 0–0 | Direct contemporary local blog supports Feirense home to Nacional and score/date, but writer/upstream independence is unproven. Structural one-row whitespace hypothesis gives 16 clubs/zero missing pairings. | Review only this audit ID for canonical interpretation; no global trim. The 32 apparent pairing gaps are literal-label artifacts, not 32 proven missing matches. |
| Benfica–Salgueiros 1995/96 — newly discovered sample issue | CSV line 308: Aug 20 1995, 0–0 | Direct fan archive says completed Sept 6 1995, 0–0. Contemporary Sept 6 newspaper index describes an overdue first-round fixture that evening; full 32.5MB PDF was refused by web tool and not acquired. Other indexed databases support Sept 6, but shared upstream is unknown. | Preserve original; seek directly inspected contemporary completion evidence before approving any date interpretation/correction. |
| União Leiria–Feirense 2011/12 — new participation exception | Apr 29 2012, 0–4; exact source binding in registry | Direct RTP/Lusa narrative describes eight Leiria starters during player strike, completed 0–4. An eight-player side does not by itself imply an awarded score. | Preserve on-field score; review participation context separately from any later administrative consequences. |
| Nacional–Benfica 2024/25 | Source completion date Dec 19 2024, 0–2 | Direct club live report preserves Oct 6 fog interruption and restart after eight minutes, then Dec 19 completion and 0–2. | Keep kickoff Oct 6/completion Dec 19 separately; do not expose completed result on Oct 6. No source correction is currently implied. |

Exact source identities for the three completion-date contradictions and narrow whitespace candidate:

- Santa Clara 1-1 Benfica: `07e7ee52db6b6ec435b234243d03e1ab9fb89b4cd4e4571aa587e7e06c1be69d`, `jalapic/engsoccerdata/data-raw/portugal.csv`, physical line 7532.
- Benfica 0-0 Salgueiros: `2675bb5e1717d5c4f907df689ded4a41889858974d19d18892a3035cb827570a`, `jalapic/engsoccerdata/data-raw/portugal.csv`, physical line 308.
- Santa Clara 2-1 Pacos Ferreira: `33862b4501af82fe70d76532a67a228dee8f326b6136ba54ef3dba90d8bab0a2`, `jalapic/engsoccerdata/data-raw/portugal.csv`, physical line 7290.
- Feirense  0-0 Nacional: `5265c556cbad744e664ed5f55bec58e0117a48b279d3ef3aa1f435b2753aa25b`, `jalapic/engsoccerdata/data-raw/portugal.csv`, physical line 4877.

Belenenses distinctions remain open: the database value (0–7), score at termination, regulatory completion, formally recognized result, later disciplinary treatment and legally final availability are separate facts. Indexed allegations, a sanction list or a later decision excerpt cannot substitute for an inspected final decision and appeal status. Do not code this as accepted or NOT PLAYED from two agreeing databases.

## All 18 wide-round and 13 reversal contexts

Each table row preserves its entire original context privately, including all member audit IDs/physical lines. Direct means only the named diagnostic endpoint is supported; no context is fully historically certified. Nominal matchday numbers are not actual chronological order. Earlier/later endpoints can be advanced games, rescheduling or data defects; a long span alone proves none of those.

| Context | Earliest–latest diagnostic source dates | Targeted fixture | Evidence assessment | Citations |
|---|---|---|---|---|
| 2019/2020:REV:1 | 2019-08-16–2019-09-08 | Rio Ave FC 1-1 Vitória Guimarães (2019-09-08) | UNRESOLVED | No qualifying documentary citation secured |
| 2019/2020:REV:2 | 2019-10-05–2019-10-28 | CD Aves 0-1 CD Tondela (2019-10-05) | UNRESOLVED | No qualifying documentary citation secured |
| 2019/2020:ROUND:1 | 2019-08-09–2019-09-08 | Rio Ave FC 1-1 Vitória Guimarães (2019-09-08) | UNRESOLVED | No qualifying documentary citation secured |
| 2019/2020:ROUND:9 | 2019-10-05–2019-10-31 | CD Aves 0-1 CD Tondela (2019-10-05) | UNRESOLVED | No qualifying documentary citation secured |
| 2020/2021:REV:1 | 2020-09-25–2020-10-28 | Sporting CP 3-1 Gil Vicente (2020-10-28) | PARTIAL_DIRECT_ENDPOINT | [Ef40f7e04a14b6bc6](https://www.rtp.pt/noticias/desporto/sporting-cp-gil-vicente-i-liga-em-direto_e1270878) (DIRECT_DOCUMENT) |
| 2020/2021:REV:2 | 2020-11-27–2020-12-01 | Moreirense FC 0-1 Paços de Ferreira (2020-12-01) | UNRESOLVED | No qualifying documentary citation secured |
| 2020/2021:REV:3 | 2021-01-07–2021-01-21 | Vitória Guimarães 3-1 CD Nacional (2021-01-21) | PARTIAL_DIRECT_ENDPOINT | [E046c2cb69a194176](https://www.cdnacional.pt/vitoria-s-c-vs-c-d-nacional-equipas-oficiais/) (DIRECT_DOCUMENT) |
| 2020/2021:REV:4 | 2021-01-24–2021-02-17 | Vitória Guimarães 2-2 SC Farense (2021-02-17) | INDEX_LEAD_ONLY | [Ed97dcff02fe5609d](https://www.zerozero.pt/noticias/incrivel-v-guimaraes-x-farense-adiado-para-17-de-fevereiro/309870) (INDEX_ONLY) |
| 2020/2021:ROUND:1 | 2020-09-18–2020-10-28 | Sporting CP 3-1 Gil Vicente (2020-10-28) | PARTIAL_DIRECT_ENDPOINT | [Ef40f7e04a14b6bc6](https://www.rtp.pt/noticias/desporto/sporting-cp-gil-vicente-i-liga-em-direto_e1270878) (DIRECT_DOCUMENT) |
| 2020/2021:ROUND:12 | 2021-01-02–2021-01-21 | Vitória Guimarães 3-1 CD Nacional (2021-01-21) | PARTIAL_DIRECT_ENDPOINT | [E046c2cb69a194176](https://www.cdnacional.pt/vitoria-s-c-vs-c-d-nacional-equipas-oficiais/) (DIRECT_DOCUMENT) |
| 2020/2021:ROUND:14 | 2021-01-15–2021-02-17 | Vitória Guimarães 2-2 SC Farense (2021-02-17) | INDEX_LEAD_ONLY | [Ed97dcff02fe5609d](https://www.zerozero.pt/noticias/incrivel-v-guimaraes-x-farense-adiado-para-17-de-fevereiro/309870) (INDEX_ONLY) |
| 2020/2021:ROUND:7 | 2020-11-06–2020-12-01 | Moreirense FC 0-1 Paços de Ferreira (2020-12-01) | UNRESOLVED | No qualifying documentary citation secured |
| 2021/2022:REV:1 | 2021-12-10–2022-01-03 | CD Tondela 2-1 Moreirense FC (2022-01-03) | UNRESOLVED | No qualifying documentary citation secured |
| 2021/2022:REV:2 | 2022-01-07–2022-01-13 | FC Famalicão 1-0 Belenenses SAD (2022-01-13) | INDEX_LEAD_ONLY | [E9659326bc27740df](https://www.rtp.pt/noticias/1a-liga/i-liga-famalicao-e-b-sad-acertam-calendario_d1376502) (INDEX_ONLY) |
| 2021/2022:REV:3 | 2022-01-21–2022-01-27 | GD Estoril 1-2 FC Arouca (2022-01-27) | PARTIAL_DIRECT_ENDPOINT | [E1ce204e5a960de24](https://www.rtp.pt/noticias/futebol-nacional/arouca-vence-estoril-praia-com-golo-marcado-aos-907_d1380179) (DIRECT_DOCUMENT) |
| 2021/2022:ROUND:13 | 2021-12-03–2022-01-03 | CD Tondela 2-1 Moreirense FC (2022-01-03) | UNRESOLVED | No qualifying documentary citation secured |
| 2021/2022:ROUND:16 | 2021-12-28–2022-01-13 | FC Famalicão 1-0 Belenenses SAD (2022-01-13) | INDEX_LEAD_ONLY | [E9659326bc27740df](https://www.rtp.pt/noticias/1a-liga/i-liga-famalicao-e-b-sad-acertam-calendario_d1376502) (INDEX_ONLY) |
| 2022/2023:REV:1 | 2022-08-26–2022-08-30 | SL Benfica 3-2 Paços de Ferreira (2022-08-30) | UNRESOLVED | No qualifying documentary citation secured |
| 2022/2023:REV:2 | 2023-01-05–2023-02-09 | GD Estoril 2-1 Boavista (2023-02-09) | UNRESOLVED | No qualifying documentary citation secured |
| 2022/2023:REV:3 | 2023-01-26–2023-02-06 | Paços de Ferreira 0-2 SL Benfica (2023-01-26) | PARTIAL_DIRECT_ENDPOINT | [E317f02ae323c4b95](https://www.rtp.pt/noticias/desporto/benfica-vence-pacos-de-ferreira-por-2-0_e1462856) (DIRECT_DOCUMENT) |
| 2022/2023:REV:4 | 2023-03-31–2023-04-05 | Gil Vicente 0-0 Sporting CP (2023-04-05) | UNRESOLVED | No qualifying documentary citation secured |
| 2022/2023:ROUND:14 | 2022-12-23–2023-02-09 | GD Estoril 2-1 Boavista (2023-02-09) | UNRESOLVED | No qualifying documentary citation secured |
| 2022/2023:ROUND:20 | 2023-01-26–2023-02-13 | Paços de Ferreira 0-2 SL Benfica (2023-01-26) | PARTIAL_DIRECT_ENDPOINT | [E317f02ae323c4b95](https://www.rtp.pt/noticias/desporto/benfica-vence-pacos-de-ferreira-por-2-0_e1462856) (DIRECT_DOCUMENT) |
| 2022/2023:ROUND:25 | 2023-03-17–2023-04-05 | Gil Vicente 0-0 Sporting CP (2023-04-05) | UNRESOLVED | No qualifying documentary citation secured |
| 2023/2024:ROUND:20 | 2024-02-03–2024-04-16 | FC Famalicão 0-1 Sporting Clube de Portugal (2024-04-16) | INDEX_LEAD_ONLY | [Eb920cd862d866bbf](https://fcfamalicao.pt/noticias/bilhetes-para-os-jogos-com-fc-porto-e-sporting-cp/) (INDEX_ONLY) |
| 2023/2024:ROUND:3 | 2023-08-25–2023-09-09 | Moreirense FC 2-3 Sporting Clube de Braga (2023-09-09) | UNRESOLVED | No qualifying documentary citation secured |
| 2024/2025:ROUND:24 | 2025-03-01–2025-03-28 | Gil Vicente FC 0-3 Sport Lisboa e Benfica (2025-03-28) | INDEX_LEAD_ONLY | [E1b3f09669cefa2e3](https://www.rtp.pt/noticias/benfica/benfica-acerta-calendario-em-barcelos-de-olho-na-lideranca_d1644052) (INDEX_ONLY) |
| 2024/2025:ROUND:8 | 2024-10-04–2024-12-19 | CD Nacional 0-2 Sport Lisboa e Benfica (2024-12-19) | PARTIAL_DIRECT_ENDPOINT | [E6cf539bf7db64abd](https://www.slbenfica.pt/pt-pt/futebol/match-center/nacional-benfica-19-dezembro-2024) (DIRECT_DOCUMENT) |
| 2025/2026:ROUND:1 | 2025-08-08–2025-09-23 | Sport Lisboa e Benfica 1-1 Rio Ave FC (2025-09-23) | PARTIAL_DIRECT_ENDPOINT | [E63f12a9fe8613033](https://www.rtp.pt/noticias/desporto/sl-benfica-rio-ave-20h15_e1685664) (DIRECT_DOCUMENT) |
| 2025/2026:ROUND:16 | 2025-12-27–2026-01-11 | CD Nacional 3-3 CD Santa Clara (2026-01-11) | PARTIAL_DIRECT_ENDPOINT | [Ef6aa3c27fddd0f29](https://www.cdnacional.pt/ultimo-lance-dita-empate-a-tres-bolas-com-o-santa-clara/) (DIRECT_DOCUMENT) |
| 2025/2026:ROUND:26 | 2026-03-14–2026-04-29 | Sporting Clube de Portugal 2-2 CD Tondela (2026-04-29) | INDEX_LEAD_ONLY | [E93cbccc64c67cf9f](https://www.abola.pt/noticias/oficial-sporting-falha-o-tricampeonato-havera-novo-campeao-2026042921365419728) (INDEX_ONLY) |

Summary: 10 contexts have a directly inspected diagnostic endpoint, seven have only indexed scheduling/reporting leads, and 14 lack qualifying documentary corroboration. None establishes every member’s completion or administrative finality. Examples of source leads: Guimarães–Farense ice rescheduling; Famalicão–B-SAD COVID scheduling; Famalicão–Sporting policing postponement; Gil–Benfica rescheduling. These explanations remain index-only where the table says so. Paços–Benfica Jan 26 2023 is an advanced round-20 game directly reported by RTP; it must not be treated as a future February result merely because of its nominal round.

## All 18 unusual-score conditional events

| Original date | Original fixture | Source observations | Conditional evidence status | Documentary citations |
|---|---|---:|---|---|
| 2024-01-29 | Sp Lisbon 8-0 Casa Pia AC | 2 | UNRESOLVED | No qualifying documentary citation secured |
| 2022-04-16 | FC Porto 7-0 Portimonense SC | 2 | FULLY CORROBORATED CORE FACTS | [E9facbabea2e18d3b](https://www.portimonensesad.portimonense.pt/fc-porto-7-portimonense-0-liga-portugal-bwin_17318) (DIRECT_DOCUMENT) |
| 2001-12-09 | Leiria 7-0 Salgueiros | 1 | UNRESOLVED | No qualifying documentary citation secured |
| 2021-11-27 | Belenenses 0-7 Benfica | 2 | PARTIALLY CORROBORATED | [E743f4cb2ffd885b5](https://www.fpf.pt/DownloadDocument.ashx?id=21435) (INDEX_ONLY); [Ee5426512a1469489](https://www.fpf.pt/DownloadDocument.ashx?id=20842) (ACCESS_RESTRICTED) |
| 2020-01-04 | Belenenses SAD 1-7 Sporting Braga | 2 | FULLY CORROBORATED CORE FACTS | [Ea5d9d9f0f6eafbbb](https://www.ligaportugal.pt/news/4127/sc-braga-triunfa-no-terreno-do-belenenses) (DIRECT_DOCUMENT) |
| 1999-05-16 | Porto 7-1 Academica | 1 | UNRESOLVED | No qualifying documentary citation secured |
| 2021-12-19 | SL Benfica 7-1 CS Marítimo | 2 | FULLY CORROBORATED CORE FACTS | [E34be195f204cebfb](https://www.slbenfica.pt/pt-pt/agora/noticias/2021/12/19/futebol-cronica-benfica-maritimo-15-jornada-liga-bwin) (DIRECT_DOCUMENT) |
| 1998-05-10 | Porto 7-2 Salgueiros | 1 | UNRESOLVED | No qualifying documentary citation secured |
| 2009-08-31 | Benfica 8-1 Setubal | 1 | UNRESOLVED | No qualifying documentary citation secured |
| 1998-05-17 | Benfica 7-1 Leca | 1 | UNRESOLVED | No qualifying documentary citation secured |
| 2019-05-05 | Belenenses 1-8 Sp Lisbon | 2 | UNRESOLVED | No qualifying documentary citation secured |
| 2019-02-10 | Benfica 10-0 Nacional | 2 | FULLY CORROBORATED CORE FACTS | [E86b98a31f9c7922a](https://www.cdnacional.pt/nacional-goleado-na-luz/) (DIRECT_DOCUMENT) |
| 1999-01-24 | Porto 7-0 Beira Mar | 1 | UNRESOLVED | No qualifying documentary citation secured |
| 2020-02-08 | FC Famalicão 0-7 Vitória Guimarães | 2 | UNRESOLVED | No qualifying documentary citation secured |
| 1995-09-18 | Sp Lisbon 7-1 Campomaior | 1 | UNRESOLVED | No qualifying documentary citation secured |
| 1997-04-27 | Boavista 7-0 Gil Vicente | 1 | UNRESOLVED | No qualifying documentary citation secured |
| 2002-11-10 | Benfica 7-0 Pacos Ferreira | 1 | UNRESOLVED | No qualifying documentary citation secured |
| 2017-03-04 | Porto 7-0 Nacional | 1 | UNRESOLVED | No qualifying documentary citation secured |

Direct participant/league reports support Benfica–Nacional 10–0, Belenenses–Braga 1–7, Benfica–Marítimo 7–1 and Porto–Portimonense 7–0. Remaining uncorroborated high scores are not deemed erroneous and no score changes are proposed solely from magnitude. Belenenses–Benfica is separately constrained by its unresolved termination/finality question.

## Deterministic ordinary sample: all 32 seasons

Before research: one earliest (date,home,away,audit_id) nonflagged scored historical observation per 1994/95–2024/25; modern frame only for 2025/26. Sampling frame is not authoritative source selection.

| Season | Original date | Source fixture | Assessment | Evidence |
|---|---|---|---|---|
| 1994/1995 | 1994-08-20 | Farense 0-2 Sp Lisbon | PARTIALLY CORROBORATED | [Eb80a184d8fca9442](https://futebol365.pt/jogo/6087/) (INDEX_ONLY) |
| 1995/1996 | 1995-08-20 | Benfica 0-0 Salgueiros | CONTRADICTED | [E77aa0d10c222e30c](https://static-storage.dnoticias.pt/www-assets.dnoticias.pt/documents/Diario.06.09.1995.pdf) (INDEX_ONLY); [E9711d66249d15bab](https://serbenfiquista.com/jogo/futebol/masculino/seniores/19951996/campeonato-nacional/1995-09-06/sl-benfica-salgueiros) (DIRECT_DOCUMENT) |
| 1996/1997 | 1996-08-23 | Espinho 1-3 Sp Lisbon | PARTIALLY CORROBORATED | [E2d17b75c2e3c97dd](https://www.wikisporting.com/index.php?title=1996-08-23_Sp._Espinho_%E2%80%93_SPORTING) (INDEX_ONLY) |
| 1997/1998 | 1997-08-23 | Farense 0-0 Sp Lisbon | UNRESOLVED | No qualifying documentary citation secured |
| 1998/1999 | 1998-08-21 | Benfica 2-0 Est Amadora | UNRESOLVED | No qualifying documentary citation secured |
| 1999/2000 | 1999-08-20 | Setubal 1-1 Guimaraes | PARTIALLY CORROBORATED | [Edd866b59db34cec3](https://donfutbolisto.com/pt/jogo/vitoria-de-setubal-vitoria-de-guimaraes-primeira-liga-20-08-1999/) (INDEX_ONLY) |
| 2000/2001 | 2000-08-18 | Beira Mar 2-4 Boavista | UNRESOLVED | No qualifying documentary citation secured |
| 2001/2002 | 2001-08-10 | Boavista 3-0 Beira Mar | UNRESOLVED | No qualifying documentary citation secured |
| 2002/2003 | 2002-08-22 | Setubal 1-1 Boavista | UNRESOLVED | No qualifying documentary citation secured |
| 2003/2004 | 2003-08-16 | Academica 1-2 Sp Lisbon | UNRESOLVED | No qualifying documentary citation secured |
| 2004/2005 | 2004-08-28 | Belenenses 3-0 Maritimo | UNRESOLVED | No qualifying documentary citation secured |
| 2005/2006 | 2005-08-19 | Sp Lisbon 2-1 Belenenses | UNRESOLVED | No qualifying documentary citation secured |
| 2006/2007 | 2006-08-25 | Porto 2-1 Leiria | UNRESOLVED | No qualifying documentary citation secured |
| 2007/2008 | 2007-08-17 | Sp Lisbon 4-1 Academica | UNRESOLVED | No qualifying documentary citation secured |
| 2008/2009 | 2008-08-22 | Guimaraes 1-1 Setubal | UNRESOLVED | No qualifying documentary citation secured |
| 2009/2010 | 2009-08-14 | Leixoes 0-0 Belenenses | FULLY CORROBORATED CORE FACTS | [Ed67174ac1bbb1c67](https://www.rtp.pt/noticias/futebol-nacional/leixoes-e-belenenses-empatam-a-abrir-campeonato_d271236) (DIRECT_DOCUMENT) |
| 2010/2011 | 2010-08-13 | Sp Braga 3-1 Portimonense | FULLY CORROBORATED CORE FACTS | [E847dbfca38f35e73](https://www.rtp.pt/noticias/futebol-nacional/sp-braga-3-1-portimonense_d367581) (DIRECT_DOCUMENT) |
| 2011/2012 | 2011-08-12 | Gil Vicente 2-2 Benfica | FULLY CORROBORATED CORE FACTS | [Ed8d8e3ccb28df996](https://www.rtp.pt/noticias/benfica/jesus-diz-que-benfica-perdeu-dois-pontos_d469696) (DIRECT_DOCUMENT) |
| 2012/2013 | 2012-08-17 | Olhanense 2-1 Estoril | UNRESOLVED | No qualifying documentary citation secured |
| 2013/2014 | 2013-08-16 | Pacos Ferreira 0-2 Sp Braga | UNRESOLVED | No qualifying documentary citation secured |
| 2014/2015 | 2014-08-15 | Porto 2-0 Maritimo | UNRESOLVED | No qualifying documentary citation secured |
| 2015/2016 | 2015-08-14 | Tondela 1-2 Sp Lisbon | UNRESOLVED | No qualifying documentary citation secured |
| 2016/2017 | 2016-08-12 | Rio Ave 1-3 Porto | UNRESOLVED | No qualifying documentary citation secured |
| 2017/2018 | 2017-08-06 | Aves 0-2 Sp Lisbon | UNRESOLVED | No qualifying documentary citation secured |
| 2018/2019 | 2018-08-10 | Benfica 3-2 Guimaraes | FULLY CORROBORATED CORE FACTS | [Ec8a803950859e4db](https://www.slbenfica.pt/pt-pt/agora/noticias/2018-2019/08/10/direto-futebol-benfica-vitoria-guimaraes-1-jornada-liga-nos) (DIRECT_DOCUMENT) |
| 2019/2020 | 2019-08-09 | Portimonense 0-0 Belenenses | UNRESOLVED | No qualifying documentary citation secured |
| 2020/2021 | 2020-09-18 | Famalicao 1-5 Benfica | UNRESOLVED | No qualifying documentary citation secured |
| 2021/2022 | 2021-08-06 | Sp Lisbon 3-0 FC Vizela | FULLY CORROBORATED CORE FACTS | [E3eb94849972150a9](https://www.rtp.pt/noticias/sporting/sporting-vizela-o-inicio-da-i-liga-em-direto_d1340667) (DIRECT_DOCUMENT) |
| 2022/2023 | 2022-08-05 | Benfica 4-0 Arouca | FULLY CORROBORATED CORE FACTS | [E706cf5489c96c5d1](https://www.rtp.pt/noticias/desporto/i-liga-sl-benfica-fc-arouca-ao-minuto_e1424608) (DIRECT_DOCUMENT) |
| 2023/2024 | 2023-08-11 | Sp Braga 1-2 Famalicao | UNRESOLVED | No qualifying documentary citation secured |
| 2024/2025 | 2024-08-09 | Sp Lisbon 3-1 Rio Ave | FULLY CORROBORATED CORE FACTS | [E63d72793fa4e8598](https://www.rtp.pt/noticias/desporto/sporting-comeca-defesa-do-titulo-com-triunfo-sobre-rio-ave_e1592083) (DIRECT_DOCUMENT) |
| 2025/2026 | 2025-08-15 | AVS 0-2 Casa Pia AC | UNRESOLVED | No qualifying documentary citation secured |

Sample results: seven full core, three partial, one provisional date contradiction, 21 unresolved. All 32 had bounded research attempts. An unresolved search is not evidence that a match was wrong or unplayed. Historical-only years remain especially weakly independently documented. The 2006/07 16-club sample, 2014/15 18-club sample and modern-only 2025/26 sample received research but no qualifying direct documentary completion evidence within these bounds. One verified sample never certifies a season.

## Chronology and identity findings

### COVID_2019_20

Official plan May29 and schedule support restart June3; actual June3 Portimonense 1-0 Gil Vicente report confirms resumption. Official last-round summary July26 2020 confirms a completed final-round match. Does not individually certify all306 recorded results, or prove every result final at a common time. March suspension date not independently fixed here. Portugal resumed; Dutch cancellation policy inapplicable.

[Ed1565448b37c36bb](https://www.ligaportugal.pt/news/5372/comunicado-sobre-o-plano-de-retoma-da-competicao) (DIRECT_DOCUMENT); [Ed1d3c4f10ce54b23](https://www.ligaportugal.pt/news/4224/horarios-da-jornada-25-a-33-da-liga-nos) (DIRECT_DOCUMENT); [E6c173e0731fd263d](https://www.ligaportugal.pt/news/4227/%22bomba%22-de-lucas-fernandes-abrilhantou-regresso-da-liga-nos) (DIRECT_DOCUMENT); [Ebc215b1c1072aaab](https://www.ligaportugal.pt/video/38326/liga-nos-%2834aj%29%3A-resumo-portimonense-2-0-cd-aves) (DIRECT_DOCUMENT)

### BELENENSES_SAD

Official Liga explanation addresses registered professional SAD name versus founding club. Literal historical Belenenses labels cannot be globally merged across the split; season-local diagnostic overlap maps stay nonauthoritative.

[Ed0e37048926d9ec2](https://www.ligaportugal.pt/news/6774/liga-explica-denominacao-belenenses-sad) (DIRECT_DOCUMENT)

### GIL_VICENTE

Contemporary RTP/Lusa reports administrative 2006 demotion, later court history and 2017 agreement for return2019/20. League participation sanction does not automatically imply particular score annulments; underlying judgments not directly inspected.

[E3fc38041689ad019](https://www.rtp.pt/noticias/futebol-nacional/gil-vicente-e-belenenses-encerram-caso-mateus-minhotos-podem-subir-a-i-liga-em-201920_d1045957) (DIRECT_DOCUMENT)

### BOAVISTA

RTP retrospective describes 2008 administrative demotion and return context; no fixture-score amendment or legal-entity mapping approved.

[Eef332c5189bb77ea](https://www.rtp.pt/noticias/futebol-nacional/boavista-o-sonho-apos-o-pesadelo_d727665) (DIRECT_DOCUMENT)

### UNIAO_LEIRIA

RTP/Lusa2015 report describes proposed new professional company and earlier SAD liquidation. Club and legal company continuity must not be conflated.

[E1ea53faa56a8bc8c](https://www.rtp.pt/noticias/futebol-nacional/uniao-de-leiria-marca-assembleia-para-debater-nova-sociedade-desportiva_d800218) (DIRECT_DOCUMENT)

### RESERVES_VITORIA_AVS

Senior versus B teams and Guimaraes versus Setubal must remain distinct; naming alone does not establish an AVS/Aves successor relationship. Bounded research did not establish legal continuity. Global aliases, reserve stripping and predecessor/successor merges not approved.

No qualifying documentary citation secured

Official COVID evidence supports the restart decision and actual June 3 resumption, and a completed July 26 last-round game. It does not individually establish that all 306 source results were played or administratively final. The exact March suspension decision date remains unverified in the directly inspected set. No Dutch-style cancellation or Portuguese season-wide exception policy is selected.

Senior/B identities, Vitória Guimarães/Setúbal, AVS/Aves and company/club continuity remain distinct questions. The Liga Belenenses explanation and Leiria/Gil/Boavista journalism do not authorize global aliases or retroactive score removals. In particular, administrative relegation and a standings penalty are not synonymous with an awarded match result.

## Evidence access, independence and permissions

The private documentary index holds 451 citation records: 31 directly inspected snapshots, 418 index-only leads and two restricted official decision citations. Many indexed results are discovery leads, not used factual evidence. Each retained snapshot has URL, retrieval time, bytes and SHA-256; the original retrieval receipt’s `inspected:false` records initial download state, while the curated index records subsequent manual inspection. Original download receipts were not rewritten. Publication/authority fields remain unknown when not ascertainable; article update time is not automatically event time.

Sandbox DNS failures on a bounded second document batch were retained as failed receipts. Network-enabled retrieval then succeeded for most of those same public documents; this was not an access-control bypass. Restricted FPF endpoints were not retried through mirrors. Club timeout/failure receipts remain. The oversized historical newspaper was not bulk-downloaded.

Narrative primary club/league reports and contemporary journalism are separate documents from the Git files, but complete upstream independence is not provable for every factual feed. RTP/Lusa republications are not counted as independent sources from Lusa. Statistical portals, fan archives and indexed snippets never become primary decisions because their URL differs. Full-core classification is documentary corroboration with these limitations, not certification of every upstream fact.

engsoccerdata README noncommercial/attribution limitations and package GPL do not settle upstream data rights. OpenFootball CC0 applies only to rights held. RSSSF and documentary publishers retain their respective attribution/copyright conditions. No commercial redistribution or model-training clearance is established. Private evidence must not be committed or fed into the application.

## Offline regeneration and tests

Run with the existing external Python 3.13.12 verification environment (declared/tested constraints retained); no dependency installation or original `.venv` invocation was needed:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. "$VERIFICATION_PYTHON" -B scripts/verify_primeira_liga_review.py --output-directory "$TEMP_REVIEW_DIR"
```

`TEMP_REVIEW_DIR` must be a safe temporary output directory; compare its seven files with the saved private artifacts. The script reparses all nine dated original files through the Phase 4 pipeline and verifies all ten original hashes, checks all six Phase 4 bytes, validates all207 queue bindings, physical source hashes, frozen evidence, 32 deterministic samples, one-to-one overlap groups and snapshot integrity. No live web access is required. Reproducing this private assessment requires the preserved curated evidence inputs; public code does not distribute private data.

| Test selection (overlapping; do not sum) | Passed | Failed | Errors | Skipped |
|---|---:|---:|---:|---:|
| acquisition_importer | 707 | 0 | 0 | 0 |
| app_launcher | 7 | 0 | 0 | 0 |
| focused | 175 | 0 | 0 | 0 |
| full | 2021 | 0 | 0 | 0 |
| historical_review | 34 | 0 | 0 | 0 |
| non_ui | 2014 | 0 | 0 | 0 |

Fresh full-suite result: **2,021 passed**, compared with the previous 1,987 baseline; 34 new focused historical-review tests. Seven app/launcher tests were separately executed successfully. The safe external environment and bounded subprocesses avoided touching the iCloud-backed `.venv`.

All seven final Phase 5 derived artifacts regenerated in a separate Python process and compared byte-for-byte and by SHA-256. Detailed hashes are in `phase5_independent_regeneration.json`; the seventh manifest hashes the other six outputs and frozen assessment inputs (not itself). This proves deterministic assessment reproduction, not documentary historical truth. Internal curation drafts are explicitly superseded and are not downstream inputs.

Protected baselines: 1,037 prior private files, 228 prior public files and 120 frozen Phase 2–4 entries; all eleven prior screened outputs/127,927 records independently re-counted and hashed unchanged. All ten Portuguese originals and Phase 2–4 evidence are unchanged. Planning-log prefix and Git index/HEAD are checked. No application/promotional files are edited, no original environment is rebuilt or installed into, and all private evidence remains ignored/untracked.

## Direct documentary citations and restricted official decisions

These are the inspected-document citations and restricted decisions, not a claim that every citation independently establishes all facts of an issue. Issue and fixture bindings above identify the narrower supported claims. Unknown publication dates and authors remain unknown; article update times below are explicitly labeled in the private index.

| Evidence | Publisher | Title | Direct-inspection status | Publication/update metadata |
|---|---|---|---|---|
| [E046c2cb69a194176](https://www.cdnacional.pt/vitoria-s-c-vs-c-d-nacional-equipas-oficiais/) | www.cdnacional.pt | Vitória S.C. (3-1) C.D. Nacional: Resultado final em Guimarães - Clube Desportivo Nacional - Madeira | DIRECT_DOCUMENT | Not established in curated metadata; see factual date claim if available |
| [E0ca6a2deb4cf1d2a](https://www.rtp.pt/noticias/desporto/santa-clara-2-1-pacos-de-ferreira-veja-as-estatisticas_e1202367) | www.rtp.pt | Santa Clara 2- 1 Paços de Ferreira, veja as estatísticas | DIRECT_DOCUMENT | 2020-02-02T19:35:02Z |
| [E0d667469ea54709f](https://www.fpf.pt/DownloadDocument.ashx?id=16933) | www.fpf.pt | FPF Santa Clara-Pacos scheduling decision (restricted) | ACCESS_RESTRICTED | Not established in curated metadata; see factual date claim if available |
| [E1ce204e5a960de24](https://www.rtp.pt/noticias/futebol-nacional/arouca-vence-estoril-praia-com-golo-marcado-aos-907_d1380179) | www.rtp.pt | Arouca vence Estoril Praia com golo marcado aos 90+7 | DIRECT_DOCUMENT | 2022-01-27T22:36:20Z |
| [E1ea53faa56a8bc8c](https://www.rtp.pt/noticias/futebol-nacional/uniao-de-leiria-marca-assembleia-para-debater-nova-sociedade-desportiva_d800218) | www.rtp.pt | União de Leiria marca assembleia para debater nova sociedade desportiva | DIRECT_DOCUMENT | 2015-01-27T15:06:54Z |
| [E317f02ae323c4b95](https://www.rtp.pt/noticias/desporto/benfica-vence-pacos-de-ferreira-por-2-0_e1462856) | www.rtp.pt | Benfica vence Paços de Ferreira por 2-0 | DIRECT_DOCUMENT | 2023-01-26T22:14:16Z |
| [E34be195f204cebfb](https://www.slbenfica.pt/pt-pt/agora/noticias/2021/12/19/futebol-cronica-benfica-maritimo-15-jornada-liga-bwin) | www.slbenfica.pt | Benfica Marítimo Crónica Liga Bwin Futebol - SL Benfica | DIRECT_DOCUMENT | Not established in curated metadata; see factual date claim if available |
| [E3eb94849972150a9](https://www.rtp.pt/noticias/sporting/sporting-vizela-o-inicio-da-i-liga-em-direto_d1340667) | www.rtp.pt | Noite inspirada de Pote abre caminho para vitória do Sporting | DIRECT_DOCUMENT | 2021-08-06T21:13:12Z |
| [E3fc38041689ad019](https://www.rtp.pt/noticias/futebol-nacional/gil-vicente-e-belenenses-encerram-caso-mateus-minhotos-podem-subir-a-i-liga-em-201920_d1045957) | www.rtp.pt | Gil Vicente sobe à I Liga em 2019/20 | DIRECT_DOCUMENT | 2017-12-13T06:37:08Z |
| [E5fffdc976f255faa](https://23kronikasfeirenses.blogspot.com/2011/08/) | 23kronikasfeirenses.blogspot.com | Krónikas Feirenses: agosto 2011 | DIRECT_DOCUMENT | Not established in curated metadata; see factual date claim if available |
| [E63d72793fa4e8598](https://www.rtp.pt/noticias/desporto/sporting-comeca-defesa-do-titulo-com-triunfo-sobre-rio-ave_e1592083) | www.rtp.pt | Sporting começa defesa do título com triunfo sobre Rio Ave | DIRECT_DOCUMENT | 2024-08-09T22:05:27Z |
| [E63f12a9fe8613033](https://www.rtp.pt/noticias/desporto/sl-benfica-rio-ave-20h15_e1685664) | www.rtp.pt | Rio Ave resgata um ponto na Luz nos descontos | DIRECT_DOCUMENT | 2025-09-23T21:30:13Z |
| [E6c173e0731fd263d](https://www.ligaportugal.pt/news/4227/%22bomba%22-de-lucas-fernandes-abrilhantou-regresso-da-liga-nos) | www.ligaportugal.pt | Liga Portugal - “Bomba” de Lucas Fernandes abrilhantou regresso da Liga NOS | DIRECT_DOCUMENT | Not established in curated metadata; see factual date claim if available |
| [E6cf539bf7db64abd](https://www.slbenfica.pt/pt-pt/futebol/match-center/nacional-benfica-19-dezembro-2024) | www.slbenfica.pt | Direto CD Nacional - SL Benfica 19 dezembro 2024 - SL Benfica | DIRECT_DOCUMENT | Not established in curated metadata; see factual date claim if available |
| [E706cf5489c96c5d1](https://www.rtp.pt/noticias/desporto/i-liga-sl-benfica-fc-arouca-ao-minuto_e1424608) | www.rtp.pt | I Liga. SL Benfica - FC Arouca ao minuto | DIRECT_DOCUMENT | 2022-08-05T21:29:47Z |
| [E78919b2e402516bd](https://www.rtp.pt/noticias/feirense/uniao-de-leiria-com-oito-perdeu-apenas-por-4-0_d549225) | www.rtp.pt | União de Leiria - com oito - perdeu "apenas" por 4-0 | DIRECT_DOCUMENT | 2012-04-29T19:59:44Z |
| [E847dbfca38f35e73](https://www.rtp.pt/noticias/futebol-nacional/sp-braga-3-1-portimonense_d367581) | www.rtp.pt | Sp. Braga 3 – 1 Portimonense | DIRECT_DOCUMENT | 2010-08-13T21:10:07Z |
| [E86b98a31f9c7922a](https://www.cdnacional.pt/nacional-goleado-na-luz/) | www.cdnacional.pt | Nacional goleado na Luz - Clube Desportivo Nacional - Madeira | DIRECT_DOCUMENT | Not established in curated metadata; see factual date claim if available |
| [E9711d66249d15bab](https://serbenfiquista.com/jogo/futebol/masculino/seniores/19951996/campeonato-nacional/1995-09-06/sl-benfica-salgueiros) | serbenfiquista.com | SL Benfica 0 - 0 SC Salgueiros, Campeonato Nacional 1995/1996 / Serbenfiquista.com | DIRECT_DOCUMENT | Not established in curated metadata; see factual date claim if available |
| [E9facbabea2e18d3b](https://www.portimonensesad.portimonense.pt/fc-porto-7-portimonense-0-liga-portugal-bwin_17318) | www.portimonensesad.portimonense.pt | FC Porto 7 - Portimonense 0, Liga Portugal BWIN | DIRECT_DOCUMENT | Not established in curated metadata; see factual date claim if available |
| [Ea5d9d9f0f6eafbbb](https://www.ligaportugal.pt/news/4127/sc-braga-triunfa-no-terreno-do-belenenses) | www.ligaportugal.pt | Liga Portugal - SC Braga triunfa no terreno do Belenenses | DIRECT_DOCUMENT | Not established in curated metadata; see factual date claim if available |
| [Eb98306db9fa073df](https://www.rtp.pt/noticias/mundo/i-liga-em-direto-santa-clara-sl-benfica_e1286708) | www.rtp.pt | I Liga em direto. Santa Clara - SL Benfica | DIRECT_DOCUMENT | 2021-01-04T22:05:05Z |
| [Ebc215b1c1072aaab](https://www.ligaportugal.pt/video/38326/liga-nos-%2834aj%29%3A-resumo-portimonense-2-0-cd-aves) | www.ligaportugal.pt | Liga Portugal - Liga NOS (34ªJ): Resumo Portimonense 2-0 CD Aves | DIRECT_DOCUMENT | Not established in curated metadata; see factual date claim if available |
| [Ec8a803950859e4db](https://www.slbenfica.pt/pt-pt/agora/noticias/2018-2019/08/10/direto-futebol-benfica-vitoria-guimaraes-1-jornada-liga-nos) | www.slbenfica.pt | JOGO EM DIRETO. Benfica-V. Guimarães Liga NOS - SL Benfica | DIRECT_DOCUMENT | Not established in curated metadata; see factual date claim if available |
| [Ed0e37048926d9ec2](https://www.ligaportugal.pt/news/6774/liga-explica-denominacao-belenenses-sad) | www.ligaportugal.pt | Liga Portugal - Liga explica denominação Belenenses SAD | DIRECT_DOCUMENT | Not established in curated metadata; see factual date claim if available |
| [Ed1565448b37c36bb](https://www.ligaportugal.pt/news/5372/comunicado-sobre-o-plano-de-retoma-da-competicao) | www.ligaportugal.pt | Liga Portugal - Comunicado sobre o Plano de Retoma da Competição | DIRECT_DOCUMENT | Not established in curated metadata; see factual date claim if available |
| [Ed1d3c4f10ce54b23](https://www.ligaportugal.pt/news/4224/horarios-da-jornada-25-a-33-da-liga-nos) | www.ligaportugal.pt | Liga Portugal - Horários da jornada 25 à 33 da Liga NOS | DIRECT_DOCUMENT | Not established in curated metadata; see factual date claim if available |
| [Ed67174ac1bbb1c67](https://www.rtp.pt/noticias/futebol-nacional/leixoes-e-belenenses-empatam-a-abrir-campeonato_d271236) | www.rtp.pt | Leixões e Belenenses Empatam a abrir campeonato | DIRECT_DOCUMENT | 2009-08-14T22:00:58Z |
| [Ed8d8e3ccb28df996](https://www.rtp.pt/noticias/benfica/jesus-diz-que-benfica-perdeu-dois-pontos_d469696) | www.rtp.pt | Jesus diz que Benfica perdeu dois pontos | DIRECT_DOCUMENT | 2011-08-12T22:52:53Z |
| [Ee5426512a1469489](https://www.fpf.pt/DownloadDocument.ashx?id=20842) | www.fpf.pt | FPF Processo Disciplinar 33-21/22 (restricted) | ACCESS_RESTRICTED | Not established in curated metadata; see factual date claim if available |
| [Eef332c5189bb77ea](https://www.rtp.pt/noticias/futebol-nacional/boavista-o-sonho-apos-o-pesadelo_d727665) | www.rtp.pt | Boavista, o sonho após o pesadelo | DIRECT_DOCUMENT | 2014-04-01T18:04:26Z |
| [Ef40f7e04a14b6bc6](https://www.rtp.pt/noticias/desporto/sporting-cp-gil-vicente-i-liga-em-direto_e1270878) | www.rtp.pt | Sporting CP - Gil Vicente, I Liga em direto | DIRECT_DOCUMENT | 2020-10-28T23:42:41Z |
| [Ef6aa3c27fddd0f29](https://www.cdnacional.pt/ultimo-lance-dita-empate-a-tres-bolas-com-o-santa-clara/) | www.cdnacional.pt | Último lance dita empate a três bolas com o Santa Clara - Clube Desportivo Nacional - Madeira | DIRECT_DOCUMENT | Not established in curated metadata; see factual date claim if available |

No restricted document was directly read. Snapshot hashes, retrieval timestamps and claims are private; publisher rights remain reserved.

## Public and private file scope

New public files: `scripts/verify_primeira_liga_review.py`, `tests/test_primeira_liga_review.py`, this document. Modified public file: append-only `PLANNING_LOG.md`. All earlier Portuguese public scripts/tests/docs are preserved unchanged.

New private inputs/evidence: `phase5_protected_before.json`, `phase5_research_plan.json`, `phase5_research_inputs.json`, bounded `phase5_search_logs/`, `phase5_evidence/`, `phase5_evidence_network/`, `phase5_evidence_final/` snapshots/receipts, and clearly superseded `phase5_internal_draft*/`. No new full-season source dataset was acquired.

Final private derived files: `phase5_review_registry.json`, `phase5_documentary_evidence_index.json`, `phase5_scheduling_assessment.json`, `phase5_conflict_exception_assessment.json`, `phase5_sample_assessment.json`, `phase5_confidence_summary.json`, `phase5_reproducibility_manifest.json`, `phase5_independent_regeneration.json`, `phase5_test_summary.json`, `phase5_final_verification.json`, and private bounded test logs/XML under `verification_phase5*/`.

## Proposed Phase 6 agenda — not implemented

1. Decide source preference only within approved season windows; preserve both overlapping originals and all disagreements. Do not silently deduplicate disagreeing sources.
2. Consider Santa Clara completion dates Feb 2 2020 and Jan 4 2021, with kickoff/scheduled dates preserved and formal finality assessed separately.
3. Resolve Belenenses–Benfica official final result and decision/appeal chronology; seek approval for conservative HOLD OUT if evidence remains inadequate.
4. Approve or reject a one-audit-ID Feirense whitespace interpretation; never authorize a global trim/identity merge from this single case.
5. Research the new Benfica–Salgueiros Sept 6 1995 completion-date candidate before any correction; retain Leiria’s eight-starter context without inventing an award.
6. Preserve Nacional–Benfica Oct 6 kickoff and Dec 19 completion; retain all31 context uncertainties, unverified samples and literal labels without automatic exclusions.
7. Define date/result-availability policy with strict known-before prediction cutoffs, separate kickoff/completion/decision/publication/finality dates, and explicit review of interrupted/administratively unsettled outcomes. Do not assume a day-level date provides an intraday availability timestamp.
8. Keep the four early dated-source gaps and unresolved licensing/model-training permission outside any claim of complete historical coverage.

Stopped after Phase 5. No corrections, final dispositions, canonical aliases, standardized outputs, integration, model training, staging, commit or push.
