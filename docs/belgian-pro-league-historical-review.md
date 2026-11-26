# Belgian Pro League — Phase 5 historical evidence review

Review date: 2026-11-25. Branch `feature/data-collection`; starting HEAD `013bb9c195624d5ac290aeb57dae11c4e21c0b5a`.

## Scope and evidence standard

This is a bounded historical assessment, **not historical certification, source selection, final inclusion/exclusion policy or standardization**. Immutable source values remain unchanged. No HOLD OUT or NOT PLAYED dispositions are assigned here. Technical correctness, historical corroboration, chronological suitability and licensing clearance remain separate.

The complete frozen queue was reconciled: **927 entries = 897 conditional event groups + 30 documentary-only representations**. Each retains its original categories, audit IDs, physical lines and source hashes. Context review does not independently certify 927 fixtures. Category memberships overlap and must not be added together:

| Category | Entries |
|---|---:|
| DOCUMENTARY_ADMINISTRATIVE_REPRESENTATION | 30 |
| HISTORICAL_STAGE_UNCERTAINTY | 144 |
| PATH_DECLARED_SEASON_MISMATCH | 330 |
| REPEATED_DIRECTED_PAIR | 400 |
| SOURCE_ANNOTATION | 10 |
| SOURCE_ORDER_REVERSAL | 44 |
| UNMATCHED_MODERN_OBSERVATION | 64 |
| UNSCORED_SOURCE_SLOT | 127 |
| UNUSUAL_SCORE | 50 |
| WIDE_ROUND | 130 |

Immutable accounting remains 8,394 historical CSV + 1,706 TXT = 10,100 representations; 9,973 scored and 127 unscored; 1,402 linked cross-source pairs; 8,698 conditional events. The supplementary RSSSF page contributes 334 descriptions / 332 events, including 306 matched regular events and 26 additional events (24 top-flight playoff and two cross-division legs). Combined: **10,434 representations / 8,724 conditional events**, including two cross-division candidates. Earlier RSSSF 1992/93 and 2009/10 documentary populations remain outside those totals. Research leads add no match records.

The private evidence index contains **69 evidence entries**: 16 primary-direct, 26 secondary-direct and 27 search-index-only. These count entries, not independent publishers or independent confirmations. Repeated syndicated and statistical sources cannot establish independent upstream lineage. Failed direct access, paywalls, anti-bot challenges and cache misses are documented without bypass; root/catalogue URLs are explicitly unresolved leads, not fixture evidence. Targeted reports were inspected ephemerally where copying permissions were unclear. Three public adjudicative PDFs were privately preserved with byte/hash/URL/timestamp receipts and PDFKit-derived text. No new full-season source was acquired.

## Five source-marked awards

“FULL_CORE” below means inspected evidence corroborates the relevant fixture identity, date context and reported official result. It does **not** assert legal finality, actual completed play, a certified publication timestamp or training eligibility.

| Fixture and unchanged source score | Actual play | Decision evidence and chronology | Assessment / unresolved facts |
|---|---|---|---|
| 2019-04-12 Standard–Anderlecht **5-0** | 2-0 at interruption; no completion | 2019-04-30 reported by search index only; [De Standaard](https://www.standaard.be/sport/voetbal/geschillencommissie-hard-voor-anderlecht-match-achter-gesloten-deuren-boete-en-forfaitnederlaag-na-wantoestanden-in-luik/32588132.html), [Nieuwsblad](https://www.nieuwsblad.be/sport/voetbal/ongezien-standard-anderlecht-definitief-afgefloten-bij-2-0-nadat-boze-uitfans-met-rookbommen-bleven-gooien/57235906.html) | PARTIAL; PRIMARY_DECISION_AND_APPEAL_UNRESOLVED. Not April12 ordinary-play availability; April30 award only search-supported, exact effective date unresolved |
| 2024-05-10 Standard–Westerlo **0-5** | No kickoff: bus blocked | 2024-05-28 reported by contemporary secondary sources; [Qu4tre / Belga](https://www.qu4tre.be/sport/football/standard-westerlo-defaite-et-score-de-forfait-pour-les-liegeois/1519193), [RTV](https://www.rtv.be/regionale-sport/forfaitzege-voor-westerlo-na-niet-gespeelde-match-op-standard) | PARTIAL; PRIMARY_DECISION_AND_APPEAL_UNRESOLVED. No result on scheduled May10; May28 decision reported May28/29, legal effective timing unresolved |
| 2022-01-15 Leuven–Mechelen **5-0** | No kickoff: Mechelen nonappearance | 2022-02-07 replay order reversed on appeal2022-03-08 to5-0; [BAS/CBAS](https://www.bas-cbas.be/cms/resources/arbitrale-uitspraak-08.03.2022-web.pdf) | FULL_CORE; BAS_APPEAL_DECISION_INSPECTED_LATER_CHALLENGES_NOT_EXHAUSTED. 5-0 award cannot be known as official outcome before2022-03-08; exact publication/effect time not certified |
| 2022-04-10 Union–Beerschot **5-0** | 0-0 at stoppage; primary referee82:04 vs RSSSF81-minute annotation | 2022-04-16 5-0 award; sanctions deferredJune1; [RBFA disciplinary council](https://cdn.uc.assets.prezly.com/0c9a8235-4c81-4bc8-aabe-b35a0bb3fd5e/-/inline/no/Dossier%2051%20-%20Tussenbeslissing%20DRP%20-%20R.%20Union%20SG%20-%20Beerschot%20VA.pdf) | FULL_CORE; DECISION_INSPECTED_APPEAL_OUTCOME_NOT_ESTABLISHED. 5-0 award not an April10 completed on-field result; no earlier than April16 inspected decision, exact legal effect unresolved |
| 2021-12-05 Standard–Charleroi **0-3** | 0-3 at definitive stoppage; RSSSF87-minute annotation not independently certified | 2022-01-13 fixed0-3, numerical score unchanged; [RBFA disciplinary council](https://cdn.uc.assets.prezly.com/44ba235e-bba4-49bc-be6c-73e6ecdf0d16/-/inline/no/standard-charleroi.pdf) | FULL_CORE; DECISION_INSPECTED_APPEAL_OUTCOME_NOT_ESTABLISHED. Pitch score December5 differs from January13 administrative ratification; Phase6 must specify target label and legal availability |

The Leuven case is particularly important: the first disciplinary decision on 7 February 2022 ordered a replay; BAS reversed it on **8 March** and awarded 5–0. Agreement between CSV and RSSSF on 15 January / 5–0 therefore does not make that score a result known on 15 January. The BAS appeal document, pages 2–3 and 35, establishes this distinction.

Union–Beerschot's inspected **16 April 2022** interim decision fixes the score at 5–0 even though further sanctions were deferred until 1 June. The disposition is a decision, not merely a prosecutor's request. Its quoted referee account places the interruption at **82:04**; RSSSF says 81 minutes. Preserve both: this is an annotation/time-semantics discrepancy, not evidence for a score/date correction. No fixture score or calendar date was contradicted by sufficiently strong inspected evidence in this review.

For Standard–Charleroi, the numerical 0–3 remained unchanged, but on-field stoppage and the **13 January 2022** official ratification are distinct facts. For Standard–Westerlo, contemporary reporting says there was no kickoff and reports a **28 May 2024** award; the primary judgment and later appeals remain unverified. Standard–Anderlecht's 2–0 stopped score must never be conflated with the 5–0 award; primary April decision/appeal evidence is still missing.

Exact original source bindings (full hashes and any supplementary representations are in the private registry):

| Case | Original path / physical line | Audit ID |
|---|---|---|
| standard_anderlecht_2019 | `openfootball/belgium/2018-19/be1.txt:454` | `bce835997e1a97204f67dbb9b10ea7a5bca304ddddd6bb5cf50f0392ff15354c` |
| standard_westerlo_2024 | `openfootball/belgium/2023-24/be1.txt:573` | `ff448c25985240112d9a33e5f63fe204cc05f09ba3bac736d19860be2bd4d5c0` |
| leuven_mechelen_2022 | `jalapic/engsoccerdata/data-raw/belgium.csv:7348` | `5ad0d66412d8e89fe9a90bcb2f404c3eb25d3e19acf1e269e1934bbd7d39cf3e` |
| union_beerschot_2022 | `jalapic/engsoccerdata/data-raw/belgium.csv:7464` | `e4c69389a73171c51ae6507c44027ef7de6ac2cec8945973cac0bf2ab9d17401` |
| standard_charleroi_2021 | `jalapic/engsoccerdata/data-raw/belgium.csv:7311` | `9a7ebd633064e5e0fce7229acf1decd728708d4280b2537e215325d56985a691` |
| beerschot_cercle_resumed | `jalapic/engsoccerdata/data-raw/belgium.csv:7168` | `0f78335cfb25a5e263cb2c64c1c85e9edec79fc8c3eafaa424e25d8fa57c87b9` |
| seraing_union_resumed | `jalapic/engsoccerdata/data-raw/belgium.csv:7354` | `a1b8a5156d2be2140685bc1809bd7eab76dc672a7ab3f49141943a0546776753` |

## Two interrupted and resumed matches

| Fixture | Original kickoff / interruption | Completion / result | Independent inspected evidence | Remaining limit |
|---|---|---|---|---|
| Beerschot–Cercle Brugge | 2021-07-24; 0-1 at55-minute weather interruption, completed0-1 three days later | 2021-07-27, 0-1 | [AS Monaco](https://www.asmonaco.com/fr/news/le-cercle-bruges-simpose-en-deux-temps-pour-la-reprise) | Final completed result cannot be used before July27; exact time not certified; no exhaustive later-appeal certification |
| Seraing–Union | 2022-01-15; 0-2 halftime January15; January18 continuation ends0-4; fog explanation search-index only | 2022-01-18, 0-4 | [Walfoot / Florian Fiammetti](https://www.walfoot.be/belgique/jupiler-pro-league/2021-2022/calendrier/journee-22/rfc-seraing/union-sg/suivez-en-direct-commente-la-rencontre-entre-seraing-et-lunion-saint-gilloise), [BX1](https://bx1.be/categories/news/seraing-union-reprendra-mardi-soir-pour-une-rencontre-de-45-minutes/) | 0-4 final unavailable January15; completion January18, exact time not certified; no exhaustive later-appeal certification |

AS Monaco's affiliated-club report, published 28 July 2021, confirms Beerschot–Cercle was stopped by rain on Saturday at 55 minutes and completed Tuesday without changing 0–1. Walfoot's contemporary 18 January report explicitly describes Seraing–Union continuing from Saturday's 0–2 halftime and ending 0–4. Fog is corroborated only by the separate BX1 search lead. Historical CSV dates already correspond to completion. Phase 6 should decide a completion/result-availability policy; Phase 5 implements none. Continuations remain descriptions of the same events, not additional fixtures.

## Administrative seasons and termination

### Lommel 2002/03

[UEFA](https://www.uefa.com/news-media/news/018f-0f8e98001628-b6e0d29fc21e-1000--end-of-the-road-for-lommel/) (28 March) documents withdrawal/liquidation and the last played defeat at Standard on 22 March; it still describes alternative administrative outcomes. [UEFA](https://www.uefa.com/news-media/news/0190-0f8e9943a8f4-0354e55b8435-1000--sad-end-to-lommel-s-season/) (24 April) says five remaining fixtures would not be played but still treats the federation's annulment/award choice as pending. Neither article establishes a March/April final annulment date. [Anderlecht-online](https://www.anderlecht-online.be/fr/article/8006) (10 May) reports removal and annulment after unpaid debts, but the primary decision and appeal finality were not obtained.

The retained CSV's 272 fixtures among 17 clubs omit Lommel. This does not mean no Lommel games were played. No absent fixture-level list was newly acquired or independently certified. Counts of absent played/annulled/never-played Lommel events cannot be reconstructed from standings or these articles alone. Phase 6 needs a specific policy for played-but-annulled events and adequate original judgment evidence; no records are invented here.

### Mouscron 2009/10

[DH / Laurent Denuit](https://dossiers.dhnet.be/_sports/et-l-excelsior-mourut/) distinguishes the December 2009 demise from later similarly named clubs and describes the last December5 victory, last played Lokeren game on December12 and December28 closure. [L’Equipe](https://www.lequipe.fr/Archives/20091228) points to a contemporary exclusion report, but its article and the primary annulment judgment were not inspected. This establishes administrative context, not individual certification of all 30 exceptional documentary slots.

Preserved accounting: **210 retained non-Mouscron results + 18 annulled numeric Mouscron results + two annulled administrative awards + ten n/p representations = 240 nominal slots**. A numeric result subsequently annulled is not equivalent to no play. The exact original judgment date, effective annulment and appeal history remain unresolved. No fixture-level missing result or outcome is inferred.

### COVID 2019/20 and partial 2025/26

The [Belgian Competition Authority](https://www.belgiancompetition.be/sites/default/files/content/download/files/20200702_press_release_27_bca.pdf) dated 2 July 2020 explicitly records the Pro League's **15 May termination decision**, alongside relegation litigation. The [BAS/CBAS](https://www.bas-cbas.be/cms/resources/gedeeltelijke-arbitrale-uitspraak-08.07.2020-web-1.pdf) of 8 July is a partial arbitration award; its existence is not a blanket certification of every earlier sporting consequence. The [Pro League](https://www.proleague.be/nieuws/communicatie-na-algemene-vergadering-pro-league) records the subsequent 18-team configuration and illustrates why next-season consequences must be distinguished from cancelled fixtures.

All eight source-bound cancelled slots at physical lines **417–424** remain under the scheduled 15 March 2020 round heading, separate from the 232 retained scored games. The evidence supports season termination and non-completion of the final round; this review does not assign final NOT PLAYED statuses, invent scores, or use 15 March as an actual result-availability date. Per-fixture administrative finality is not exhaustively certified.

The 2025/26 pinned snapshot remains **121 scored + 119 unscored regular slots**, with no postseason. Missing scores are not cancellations. Future completion requires a separately approved revision-pinned acquisition and structural/historical review. No updates were fetched.

## Stage boundaries, omitted endpoints and identity

Official [Pro League](https://www.proleague.be/nieuws/standard-antwerp-opener-van-jupiler-pro-league-play-offs) distinguishes the six-club championship group from mixed-tier Europe groups. The [Pro League](https://www.proleague.be/nieuws/hoe-verlopen-de-play-offs-in-het-seizoen-2024-25) distinguishes championship, Europe, playdown, qualification and cross-division paths. They establish legitimate stage distinctions, not permission to include every stage in a training dataset.

| Season | Preserved diagnostic stage accounting | Phase 6 issue |
|---|---|---|
| 2018/19 | CSV240 regular; TXT adds30 championship | Administrative Standard–Anderlecht separate; mixed-tier Europe is not automatically top-flight scope |
| 2020/21 | Misplaced `2021-22/be1.txt`:306 regular +12 championship +12 Europe | Preserve wrong-path/declared-season distinction; do not rename or relabel originals |
| 2021/22 | RSSSF306 regular +12 championship +12 Europe +2 cross-division events | Actual OpenFootball original absent; two continuation descriptions are not duplicates |
| 2023/24 | CSV240 regular +30 championship +29 Europe +12 playdown +1 qualifier =312 | TXT additionally records Standard–Westerlo award; absence does not alone prove no play |
| 2024/25 | CSV240+30+30+12=312 | TXT additionally records Antwerp–Charleroi qualifier,29 May2025,1–2 |

The unmatched Antwerp endpoint is supported by an [Pro League](https://www.proleague.be/fr/matchs/saison-2024-2025-jupiler-pro-league-41-r-antwerp-fc-vs-sporting-charleroi) showing a finished 1–2 at Bosuil, with match commentary; the [Antwerpsupporter](https://www.antwerpsupporter.be/v2/matchfiches/matchfiche.php?matchid=5732) also indexes 29 May. The official page's generated heading reverses team names, so the ground and ANT/CHA score identifiers are important. Its exact date remains supplemented by search evidence rather than pretending all dynamic page fields were read. Standard–Westerlo's endpoint is addressed in the award table. Neither unmatched event is silently dropped or automatically approved.

Club identity notes: [Beerschot](https://www.beerschot.be/nl/geschiedenis.php) distinguishes historical reorganizations and registration numbers; [KRC Genk Talent](https://www.krcgenk-talent.be/nl/club/historiek) records the 1988 predecessor merger. Neither justifies global aliases. Club Brugge and Cercle are distinct; historical Beerschot, Germinal, Wilrijk and reused matricules need season-specific treatment; Excelsior Mouscron and later namesakes remain separate. RWDM/Molenbeek continuity remains unresolved here. Senior/reserve identities and bilingual source labels require source-bound evidence, not city-name matching. Existing RSSSF/CSV correspondences stay diagnostic, never legal identity merges.

## Deterministic ordinary-season sample

Method: for each 1995/96–2024/25 historical season, choose the earliest scored Anderlecht–Club Brugge meeting, either home orientation, sorted by date/home/away/physical line. For 2023/24 and 2024/25 use the independently validated first240 regular-pair prefix; retain original UNKNOWN stage metadata. For 2025/26 use only explicitly regular scored pinned TXT records. Label correspondences are confined to this sampling procedure. This is a high-profile convenience sample, not random or representative sampling and not whole-season certification.

All **31** samples received a targeted match search. Results: **14 FULL_CORE, three PARTIAL, 14 UNRESOLVED, zero confirmed material date/score contradictions**. Full means directly inspected contemporary narrative or official record supports teams/date/score/competition. Partial includes a statistical record with unknown upstream lineage and imported/relative-date ambiguities. Unresolved search-index, catalogue or blocked-document leads are not counted as independent confirmation. No absence of an administrative modification is claimed as an exhaustive legal search.

| Season | Source date | Home–away | FT | Assessment | Evidence / lead |
|---|---|---|---|---|---|
| 1995/1996 | 1995-08-29 | Anderlecht–Club Brugge | 2-1 | PARTIAL | [Transfermarkt](https://www.transfermarkt.com/rsc-anderlecht_club-brugge-kv/vorbericht/spielbericht/3194016) |
| 1996/1997 | 1996-11-10 | Club Brugge–Anderlecht | 2-1 | UNRESOLVED | [Search lead](https://www.fcupdate.nl/voetbalcompetities/belgie) |
| 1997/1998 | 1997-11-30 | Club Brugge–Anderlecht | 2-1 | UNRESOLVED | [Search lead](https://www.transfermarkt.be/club-brugge-kv_rsc-anderlecht/index/spielbericht/3112100) |
| 1998/1999 | 1998-09-09 | Anderlecht–Club Brugge | 2-3 | UNRESOLVED | [Search lead](https://www.besoccer.com/match/anderlecht/club-brugge/199945349) |
| 1999/2000 | 2000-02-06 | Anderlecht–Club Brugge | 1-1 | UNRESOLVED | [Search lead](https://www.nieuwsblad.be/sport/voetbal/waarom-lukte-het-al-20-jaar-en-27-matchen-niet-voor-club-brugge-in-anderlecht/59693341.html) |
| 2000/2001 | 2000-12-01 | Anderlecht–Club Brugge | 2-0 | UNRESOLVED | [Search lead](https://www.nieuwsblad.be/sport/voetbal/waarom-lukte-het-al-20-jaar-en-27-matchen-niet-voor-club-brugge-in-anderlecht/59693341.html) |
| 2001/2002 | 2001-12-21 | Anderlecht–Club Brugge | 1-0 | UNRESOLVED | [Search lead](https://www.nieuwsblad.be/sport/voetbal/waarom-lukte-het-al-20-jaar-en-27-matchen-niet-voor-club-brugge-in-anderlecht/59693341.html) |
| 2002/2003 | 2002-12-07 | Club Brugge–Anderlecht | 2-1 | PARTIAL | [Anderlecht-online](https://www.anderlecht-online.be/nl/article/10484) |
| 2003/2004 | 2003-10-05 | Anderlecht–Club Brugge | 1-1 | UNRESOLVED | [Search lead](https://www.anderlecht-online.be/) |
| 2004/2005 | 2004-12-11 | Anderlecht–Club Brugge | 2-1 | FULL_CORE | [UEFA / Berend Scholten](https://www.uefa.com/news-media/news/025e-0f9092097697-aeca39d0f083-1000--brugge-broken-by-jestrovic/) |
| 2005/2006 | 2005-10-23 | Anderlecht–Club Brugge | 2-2 | FULL_CORE | [Anderlecht-online](https://www.anderlecht-online.be/nl/article/3694) |
| 2006/2007 | 2006-08-27 | Anderlecht–Club Brugge | 1-0 | FULL_CORE | [Anderlecht-online](https://www.anderlecht-online.be/nl/article/5473) |
| 2007/2008 | 2007-12-16 | Club Brugge–Anderlecht | 1-0 | FULL_CORE | [Anderlecht-online](https://www.anderlecht-online.be/nl/article/10782) |
| 2008/2009 | 2008-11-16 | Club Brugge–Anderlecht | 1-1 | FULL_CORE | [Anderlecht-online](https://www.anderlecht-online.be/nl/article/13537) |
| 2009/2010 | 2009-10-04 | Club Brugge–Anderlecht | 4-2 | FULL_CORE | [Anderlecht-online](https://www.anderlecht-online.be/nl/article/15822) |
| 2010/2011 | 2010-11-07 | Anderlecht–Club Brugge | 2-2 | UNRESOLVED | [Search lead](https://www.footballinfo.in/) |
| 2011/2012 | 2011-08-28 | Club Brugge–Anderlecht | 1-1 | UNRESOLVED | [Search lead](https://www.footballinfo.in/) |
| 2012/2013 | 2012-11-11 | Anderlecht–Club Brugge | 6-1 | FULL_CORE | [Anderlecht-online](https://www.anderlecht-online.be/nl/article/23979) |
| 2013/2014 | 2013-09-22 | Club Brugge–Anderlecht | 4-0 | PARTIAL | [Anderlecht-online](https://www.anderlecht-online.be/en/article/15225) |
| 2014/2015 | 2014-08-31 | Club Brugge–Anderlecht | 2-2 | FULL_CORE | [Anderlecht-online](https://www.anderlecht-online.be/nl/article/30916) |
| 2015/2016 | 2015-10-25 | Anderlecht–Club Brugge | 3-1 | UNRESOLVED | [Search lead](https://www.youtube.com/watch?v=bOmiOonfHE4) |
| 2016/2017 | 2016-10-23 | Club Brugge–Anderlecht | 2-1 | FULL_CORE | [BRUZZ / Belga](https://www.bruzz.be/actua/club-brugge-verslaat-anderlecht-2016-10-23) |
| 2017/2018 | 2017-11-05 | Anderlecht–Club Brugge | 0-0 | FULL_CORE | [Voetbalkrant / Johan Walckiers](https://www.voetbalkrant.com/belgie/jupiler-pro-league/2017-2018/kalender/speeldag-14/anderlecht/club-brugge) |
| 2018/2019 | 2018-08-26 | Club Brugge–Anderlecht | 2-1 | FULL_CORE | [BRUZZ / Godfried Roelant](https://www.bruzz.be/sport/anderlecht-verliest-maximum-op-bezoek-bij-aartsrivaal-club-brugge-2018-08-26) |
| 2019/2020 | 2019-09-22 | Club Brugge–Anderlecht | 2-1 | UNRESOLVED | [Search lead](https://www.footballinfo.in/) |
| 2020/2021 | 2020-10-04 | Club Brugge–Anderlecht | 3-0 | UNRESOLVED | [Search lead](https://www.clubbrugge.be/) |
| 2021/2022 | 2021-10-03 | Anderlecht–Club Brugge | 1-1 | FULL_CORE | [Anderlecht-online](https://www.anderlecht-online.be/nl/article/209857) |
| 2022/2023 | 2022-10-16 | Anderlecht–Club Brugge | 0-1 | FULL_CORE | [Brussels Times / Belga](https://www.brusselstimes.com/307473/club-brugge-battle-to-a-hard-fought-victory-at-anderlecht) |
| 2023/2024 | 2023-09-24 | Anderlecht–Club Brugge | 1-1 | UNRESOLVED | [Search lead](https://www.proleague.be/wedstrijden/seizoen-2023-2024-jupiler-pro-league-8-rsc-anderlecht-vs-club-brugge-kv) |
| 2024/2025 | 2024-10-27 | Club Brugge–Anderlecht | 2-1 | UNRESOLVED | [Search lead](https://www.clubbrugge.be/en/news/club-wint-topper-tegen-anderlecht-met-2-1) |
| 2025/2026 | 2025-11-09 | RSC Anderlecht–Club Brugge KV | 1-0 | FULL_CORE | [RSC Anderlecht](https://www.rsca.be/nl/fixture/view/2550) |

The private registry contains every sample's original line, raw fields, physical-record/source hashes, search coverage and explicit completion/finality/availability limitations. Root/catalogue links in unresolved rows indicate a failed documentary lead, not evidence supporting the row. Four ordinary samples overlap the original queue; counts are not added to queue totals. The seven priority fixtures are separate from these31 ordinary samples: **38 targeted fixture assessments =19 FULL_CORE +5 PARTIAL +14 UNRESOLVED**. None of these totals include whole-round certification or the administrative-season documentary slots.

## All15 scheduling contexts and source ordering

All15 contexts and their **130 source-observation memberships** were retained, including the original15wide-round flags. Six have directly documented context; eight are partial; one is unresolved. DOCUMENTED_CONTEXT may explain only a selected delayed fixture, not every member or its complete result. Long span alone is never classified as an error. Extreme-date fixtures are shown below; every bound member remains in the private output.

| Actual season / original path | Round | Earliest–latest | Latest-date fixture(s) | Status | Finding / evidence |
|---|---|---|---|---|---|
| 2019/2020 / `2019-20/be1.txt` | 23 | 2020-01-24–2020-02-11 | Sporting Charleroi–KV Mechelen 2-1 | PARTIAL | Charleroi–Mechelen February11 2-1 date/score lead; postponement reason unestablished. Ciara hypothesis not established. [Walfoot or cited historical source](https://www.fussballtransfers.com/spiel/4960418690748319499-sporting-charleroi-vs-kv-mechelen) |
| 2019/2020 / `2019-20/be1.txt` | 5 | 2019-08-23–2020-01-29 | Sporting Charleroi–Club Brugge KV 0-0 | DOCUMENTED_CONTEXT | Contemporary January29,2020 report0-0 says postponed from August; not each round fixture independently verified. [Walfoot or cited historical source](https://www.walfoot.be/belgique/jupiler-pro-league/2019-2020/calendrier/journee-5/charleroi/fc-bruges) |
| 2020/2021 / `2021-22/be1.txt` | 10 | 2020-10-23–2020-12-03 | KAS Eupen–KV Mechelen 1-1 | PARTIAL | Index lead suggests October23 Covid postponement Eupen–Mechelen; full multi-report compilation not acquired. [Walfoot or cited historical source](https://www.stamnummer25.be/wp-content/upLoads/Nieuwsoverzicht-2020-2021.pdf) |
| 2020/2021 / `2021-22/be1.txt` | 11 | 2020-10-30–2020-12-01 | Royal Excel Mouscron–Sint-Truidense VV 3-2 | PARTIAL | December1 Mouscron3-2STVV report index; direct cache miss; cause not established. [Walfoot or cited historical source](https://www.notele.be/si103-media88724-l-excel-mouscron-s-impose-face-a-saint-trond-et-quitte-la-derniere-place-du-classement.html) |
| 2020/2021 / `2021-22/be1.txt` | 12 | 2020-11-06–2020-12-08 | Oud-Heverlee Leuven–Royal Excel Mouscron 2-0 | PARTIAL | December8 Leuven2-0Mouscron index; no inspected rescheduling decision. [Walfoot or cited historical source](https://www.lequipe.fr/Football/match-direct/championnat-de-belgique/2020-2021/oh-louvain-mouscron-live/479428) |
| 2020/2021 / `2021-22/be1.txt` | 16 | 2020-12-11–2020-12-29 | KAS Eupen–SV Zulte Waregem 2-3 | DOCUMENTED_CONTEXT | December11 contemporary notice quotes ProLeague postponement Eupen–Zulte following seven positive tests; eventual December29 result not individually certified. [Walfoot or cited historical source](https://www.walfoot.be/news/2020-12-11/pro-league-eupen-zulte-waregem-reporte) |
| 2020/2021 / `2021-22/be1.txt` | 17 | 2020-12-18–2021-01-13 | K Beerschot VA–Cercle Brugge 1-1 | PARTIAL | January13 Beerschot1-1Cercle make-up game index; original cause unestablished. [Walfoot or cited historical source](https://www.walfoot.be/news/2021-01-13/jpl--le-cercle-met-fin-a-sa-spirale-negative-sur-la-pelouse-du-beerschot) |
| 2020/2021 / `2021-22/be1.txt` | 18 | 2020-12-15–2021-01-06 | KAS Eupen–KRC Genk 1-4 | DOCUMENTED_CONTEXT | December19 contemporary report says Eupen–Genk, Zulte and Ostende postponed following Covid cluster; January6 final score not individually certified. [Walfoot or cited historical source](https://www.walfoot.be/news/2020-12-19/eupen-ne-veut-pas-dun-calendrier-surcharge) |
| 2020/2021 / `2021-22/be1.txt` | 26 | 2021-02-12–2021-03-12 | Sporting Charleroi–Club Brugge KV 1-1 | PARTIAL | March12 Charleroi1-1Brugge lead; cause unestablished. [Walfoot or cited historical source](https://www.lequipe.fr/Football/match-direct/championnat-de-belgique/2020-2021/charleroi-sc-club-bruges-live/479550) |
| 2020/2021 / `2021-22/be1.txt` | 28 | 2021-02-26–2021-03-15 | KAA Gent–Club Brugge KV 0-4 | UNRESOLVED | Targeted Gent–Brugge March15,2021 0-4 search did not establish reason for span. No usable independent document |
| 2020/2021 / `2021-22/be1.txt` | 31 | 2021-03-19–2021-04-07 | K Beerschot VA–Sporting Charleroi 2-1 | PARTIAL | April7 Beerschot2-1Charleroi result lead; weather hypothesis not established. [Walfoot or cited historical source](https://www.maxifoot.fr/match/beerschot-wilrijk-charleroi-20210407.htm) |
| 2020/2021 / `2021-22/be1.txt` | 9 | 2020-10-17–2020-11-24 | Waasland-Beveren–KV Oostende 2-0 | DOCUMENTED_CONTEXT | October17 contemporary notice quotes league Covid protocol postponement; does not individually certify November24 final score. [Walfoot or cited historical source](https://www.walfoot.be/news/2020-10-17/covid--la-rencontre-entre-waasland-beveren-et-ostende-reportee) |
| 2023/2024 / `2023-24/be1.txt` | 5 | 2023-08-26–2023-09-28 | RWD Molenbeek–Union Saint-Gilloise 2-3; Club Brugge KV–KRC Genk 1-1 | DOCUMENTED_CONTEXT | RWDM–Union moved to September28 after European playoffs; separate Brugge–Genk explanation not independently established. [Walfoot or cited historical source](https://www.walfoot.be/news/2023-09-19/rwdm---union-un-derby-meprise--si-cela-avait-ete-le-derby-des-flandres) |
| 2024/2025 / `2024-25/be1.txt` | 5 | 2024-08-24–2024-09-26 | Cercle Brugge–KAA Gent 2-1 | PARTIAL | Cercle–Gent September26 2-1 lead; cause not directly established. [Walfoot or cited historical source](https://www.vi.nl/wedstrijden/2024-09-26/cercle-brugge-vs-kaa-gent) |
| 2025/2026 / `2025-26/be1.txt` | 5 | 2025-08-23–2025-09-24 | Club Brugge KV–KVC Westerlo 5-5 | DOCUMENTED_CONTEXT | September24,2025 5-5 match report explicitly says delayed for Brugge Champions League playoff preparation; unusual score corroborated, not corrected. [Walfoot or cited historical source](https://www.walfoot.be/belgique/jupiler-pro-league/2025-2026/calendrier/journee-5/fc-bruges/westerlo/dix-buts-un-de-chaque-cote-dans-les-arrets-de-jeu--scenario-incroyable-entre-le-club-de-bruges-et-westerlo) |

All22 modern adjacent ordering reversals are context-reviewed: **five stage-block transitions and17 within-stage source-order reversals**. Their44 category memberships stay preserved. A backwards physical-source date sequence is not itself a historical calendar error, and no source date was corrected. Fixture-level targeted confirmation must not be inferred from this ordering assessment.

## Coverage, rights and remaining uncertainties

The36-season1990/91–2025/26 target is not complete. **1990/91–1994/95** still lack approved complete dated sources. The existing1992/93 standings document is not a fixture inventory. Genuine OpenFootball2021/22 remains missing; the RSSSF recovery supplies an explicitly separate regular-season comparison, with no independent upstream guarantee. The2025/26 snapshot is incomplete.

OpenFootball's copying notice, engsoccerdata provenance, RSSSF attribution requirements and legal-document publication do not collectively establish commercial redistribution or model-training permission. Contemporary newspaper/fan reports remain copyrighted; only factual review notes and links are retained where no copying right was established. Public reports omit source datasets and documentary bundles. Historical corroboration does not grant rights or authorize application integration.

Unresolved priorities: primary2019 and2024 award judgments and appeals; later challenges to the three inspected decisions; exact publication/effective times; Lommel/Mouscron original annulment decisions and individual absent/annulled fixture evidence; RWDM/Beerschot legal continuity; unverified ordinary samples and scheduling leads; rules for same-day result access and delayed administrative labels. No entire dataset is called historically certified.

## Reproduction, tests and preservation

The new offline module consumes frozen original-backed Phase4 and recovery inputs plus the curated private evidence notes. It independently reruns the existing original-byte structural reconstruction and documentary recovery, compares all saved objects, verifies court-PDF receipts, binds all case references, reconciles the unchanged927-entry queue, and generates six assessment outputs plus a hash manifest. The code is a reconciliation/evidence workflow, not an automated fact-checker: human source readings are explicit reproducible inputs, not regenerated historical truth.

```sh
PYTHONDONTWRITEBYTECODE=1 python -B -m scripts.verify_belgian_pro_league_review
PYTHONDONTWRITEBYTECODE=1 python -B -m scripts.verify_belgian_pro_league_review --verify
```

Generation refuses to overwrite differing saved assessments. Verification runs generation in a separate process and temporary directory, comparing all seven outputs byte-for-byte and by SHA-256. Frozen original raw scores, annotations, phases, revisions and physical bindings remain untouched. Evidence notes and temporary environments are private/untracked, not application inputs.

Fresh results and preservation measurements are appended after execution below.

## Prioritized Phase6 decision agenda — not implemented

1. Decide finality requirements and result-availability semantics for each of the five awards. Do not use scheduled date as availability, especially Leuven's reversed replay order. Seek primary/later appeal evidence where absent.
2. Define completion-date treatment for both resumptions, preserving kickoff/interruption/completion separately; prevent access to completed outcomes before they exist. Specify strict-before prediction chronology and same-day uncertainty.
3. Decide treatment of genuinely played but annulled Lommel/Mouscron events separately from awards and never-played slots; primary documentary gaps remain visible.
4. Decide regular, top-flight playoff, mixed-tier Europe, qualifier and cross-division scope individually. Preserve administrative endpoint events and source-path mismatch in audit metadata whatever the eventual decision.
5. Decide explicit uncertainty handling for incomplete2025/26 and COVID slots without invented results or retrospective timestamps; retain early missing-season gaps.
6. Keep diagnostic aliases source/season-bound, retain uncorroborated samples/scheduling contexts, and establish licensing clearance separately before any training/integration.

No Phase6 disposition, standardized date, final ID, eligibility list, corrected source value, final screened CSV or model was produced. No staging, commit or push is authorized by this review.

## Executed verification results

- Focused new tests: **38 passed**; all Belgian tests: **211 passed**; acquisition/importer selection: **503 passed**; app/launcher separately: **7 passed**; complete repository: **2,372 passed**. These selections overlap. All final runs had zero failed, errored or skipped tests. No timeout was counted as a pass.
- All **seven** Phase5 artifacts reproduced byte-for-byte and with identical SHA-256 in a separate process/temp directory. The build also re-parsed and compared the six frozen Phase4 objects and four recovery objects against the originals; no saved upstream output was rewritten.
- Protected chain verified **1,415 prior private files,250 prior public files**, then36 frozen Phase2,57 Phase2/3,71 Phase2–4 and83 pre-Phase5 entries (nested overlapping baselines, not additive totals). All original-byte and revision receipts remain valid.
- The12 completed historical screened CSVs remain byte-identical and contain **137,189** records. Two separate existing ongoing English CSVs,168+90=258 rows, also remain unchanged; they are outside that historical total.
- Reused the existing external offline environment at `/private/tmp/belgium-phase4-env-xgpvyf0n/venv` (CPython3.13.12; pytest9.1.1,NumPy2.5.3,pandas3.0.6,Streamlit1.64.0,Jinja2 3.1.6). No packages installed or downloaded; all **6,200** original runtime-package fingerprints match the pre-existing copy manifest. The original `.venv` was not modified.
- Private Phase5 originals, receipts, evidence notes, review outputs and verification records remain Git-ignored. No private data is tracked or staged. HEAD and index hash match the starting baseline; no staging, commit or push. Only the planning-log append and three new Phase5 public files were added to the previously existing uncommitted work. The two existing `.DS_Store` files remain untracked.
- The application and promotional worktree were not edited. Prior planning-log bytes are preserved by hash-prefix checks. No model training, integration, corrections, final dispositions or standardization occurred.

New public work: `scripts/verify_belgian_pro_league_review.py`, `tests/test_belgian_pro_league_review.py`, this report, and append-only `PLANNING_LOG.md`. Private new work: `phase5_protected_before.json`; `phase5/evidence_inputs.json`; `phase5/context_access.json`; three PDF/receipt/extracted-text triplets under `phase5/evidence/`; six assessments plus `reproducibility.json` under `phase5/review/`; `phase5_final_verification.json`. Existing Phase2–4/recovery files are unchanged. Public scripts require the preserved private source/evidence inputs to reproduce the assessment; public checkout alone does not include datasets or evidence bundles.
