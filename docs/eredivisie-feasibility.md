# Dutch Eredivisie — Phase 2 bounded feasibility

Date: 2026-11-22. Only the six user-approved originals were acquired. No Phase 3 acquisition, normalization, historical correction, screening, standardization, application integration or training has occurred.

## Starting state and preservation

Branch `feature/data-collection`, HEAD `4f8c64433cf6168a06dbde0102e822ce6d2eeffa`; only two pre-existing untracked .DS_Store files. The private `protected_before.json` freezes 839 earlier private and 207 tracked public files across all ten completed competitions, plus the earlier planning-log byte prefix. Private data remain ignored under `data/private/netherlands/eredivisie/`. Originals and notices are immutable; source/cache corruption fails explicitly.

## Exact acquisition and provenance

Historical repository `jalapic/engsoccerdata`, commit `872c5c354161ace8408f3091b758c6af4cccca94`. Modern repository `openfootball/europe`, commit `63df627f3c87ce71708f016522ea236cf74332c3`. Both retained pinned trees were verified before any original request. Relevant README/DESCRIPTION/CC0 notices and tree metadata were reused from the completed Ligue 1 evidence with attribution and receipts, not newly downloaded.

One bounded request per original, maximum 30 seconds and 8 MB, no retries or redirects; requests were spaced by two seconds. Network-enabled execution was used for the explicitly approved downloads. No access/source-identity failure occurred. Cached rerun required zero requests and preserved all 34 then-existing private files byte-for-byte.

| Original path | Bytes | Git blob SHA-1 | SHA-256 | Retrieval UTC |
|---|---:|---|---|---|
| `data-raw/holland.csv` | 1,215,520 | `a84a96a234e7e90dadd3c802b2a277d1e0df33dc` | `6ed2410f59fee88cbb93a1f59fde9c1e5e2cc5bed9282b367c7d7bb712053dbf` | 2026-11-22T22:31:38.693877+00:00 |
| `netherlands/2018-19_nl1.txt` | 24,409 | `5421e6ac82acb4616dec45c11b85325545f39e70` | `31c373c7c51f91bbf76c583222d5ad1eaa11c5fca24f6b184ee62cf8b30f665b` | 2026-11-22T22:31:41.089442+00:00 |
| `netherlands/2019-20_nl1.txt` | 24,558 | `c4541c1a242f6de7dc1268b610e4f6c7fe099043` | `6f0f0cdc802cafcc6aab7afe3d6b30b0429d14a1a53d8ac4d81fbe4081eae06e` | 2026-11-22T22:31:43.605529+00:00 |
| `netherlands/2023-24_nl1.txt` | 24,509 | `6e44e6fbbb162b8475418e282b47ad10714c9d2f` | `2bde6d0ca60ea6c321f359d1042ce20643880ccfb86a4d7c47f993ec546ba227` | 2026-11-22T22:31:45.994173+00:00 |
| `netherlands/2024-25_nl1.txt` | 24,670 | `da18fab2c58b3c6850342f3679918ddaec64b882` | `fe1b42aa86ef00a313e1108a8e6faef9fdd7f26ab612f56f4ed5c08a3b78e041` | 2026-11-22T22:31:48.389683+00:00 |
| `netherlands/2025-26_nl1.txt` | 24,529 | `18739d3c6a7789d74da6a8253e8c6d4c6ee34fb2` | `50216d5c06514cb255141be5f27f247a47a63a6a981ca98e54edd365b55d2387` | 2026-11-22T22:31:50.878022+00:00 |

Exact source URLs follow the pinned form `https://raw.githubusercontent.com/{repository}/{commit}/{original_path}` and are recorded individually in `acquisition.json` and adjacent `.provenance.json` receipts. The historical original matches the independently checked expected blob and size of 1,215,520 bytes. All original bytes were preserved.

## Historical CSV: directly measured contents

The complete original contains **20,776 score-bearing records across 69 seasons, 1956/57–2024/25**, with eight columns in this exact original order:

```text
Date,Season,home,visitor,FT,hgoal,vgoal,tier
```

Dates are explicit ISO `YYYY-MM-DD` strings; `Season` is a starting-year integer token; goal/tier values are integer tokens and FT is a hyphenated score string. All tier values are `1`; all scores parse and agree with numeric goals. This is not a multi-division file. However, it has no independent per-row competition-stage or administrative-status column: tier1 membership and complete pairings are structural support, not legal or historical certification. No score annotations are provided by this CSV.

The README advertises 1956–2025 and old package documentation stops at 2015/16. Actual contents resolve the technical cutoff: the pinned file continues through 2024/25 and contains no 2025/26 rows. The 1990/91–2024/25 target portion has 10,636 scored observations. Detailed extraction is limited to four approved samples and the approved modern overlap; all other seasons receive metadata-level inventory only.

| Historical detailed sample | Observed | Scored | Clubs | Expected | Missing / duplicate pairs |
|---|---:|---:|---:|---:|---|
| 1990/1991 | 306 | 306 | 18 | 306 | 0 / 0 |
| 2005/2006 | 306 | 306 | 18 | 306 | 0 / 0 |
| 2015/2016 | 306 | 306 | 18 | 306 | 0 / 0 |
| 2017/2018 | 306 | 306 | 18 | 306 | 0 / 0 |

All four samples have zero malformed fields, invalid/out-of-season dates or unexplained missing scores. There are no extra fixture slots beyond complete directed pairings. This supports structural stage suitability, not independent proof of every actual match date or administrative outcome. No placeholder date is explicitly identified by the source; parseable dates are not automatically historically valid dates.

### Complete metadata-level historical inventory

Observed fixture counts, labels and pairings were measured for every source season. The four 1962/63–1965/66 seasons contain 16 clubs / 240 fixtures; other seasons contain 18 clubs / 306 fixtures except 2019/20. All inventory seasons have zero malformed score/date records or duplicated directed pairings. The 74 absent historical-CSV pairings in 2019/20 are not explicit cancelled rows.

| Season | Observed / scored | Clubs | Expected slots | Absent pairs |
|---|---:|---:|---:|---:|
| 1956/1957 | 306 / 306 | 18 | 306 | 0 |
| 1957/1958 | 306 / 306 | 18 | 306 | 0 |
| 1958/1959 | 306 / 306 | 18 | 306 | 0 |
| 1959/1960 | 306 / 306 | 18 | 306 | 0 |
| 1960/1961 | 306 / 306 | 18 | 306 | 0 |
| 1961/1962 | 306 / 306 | 18 | 306 | 0 |
| 1962/1963 | 240 / 240 | 16 | 240 | 0 |
| 1963/1964 | 240 / 240 | 16 | 240 | 0 |
| 1964/1965 | 240 / 240 | 16 | 240 | 0 |
| 1965/1966 | 240 / 240 | 16 | 240 | 0 |
| 1966/1967 | 306 / 306 | 18 | 306 | 0 |
| 1967/1968 | 306 / 306 | 18 | 306 | 0 |
| 1968/1969 | 306 / 306 | 18 | 306 | 0 |
| 1969/1970 | 306 / 306 | 18 | 306 | 0 |
| 1970/1971 | 306 / 306 | 18 | 306 | 0 |
| 1971/1972 | 306 / 306 | 18 | 306 | 0 |
| 1972/1973 | 306 / 306 | 18 | 306 | 0 |
| 1973/1974 | 306 / 306 | 18 | 306 | 0 |
| 1974/1975 | 306 / 306 | 18 | 306 | 0 |
| 1975/1976 | 306 / 306 | 18 | 306 | 0 |
| 1976/1977 | 306 / 306 | 18 | 306 | 0 |
| 1977/1978 | 306 / 306 | 18 | 306 | 0 |
| 1978/1979 | 306 / 306 | 18 | 306 | 0 |
| 1979/1980 | 306 / 306 | 18 | 306 | 0 |
| 1980/1981 | 306 / 306 | 18 | 306 | 0 |
| 1981/1982 | 306 / 306 | 18 | 306 | 0 |
| 1982/1983 | 306 / 306 | 18 | 306 | 0 |
| 1983/1984 | 306 / 306 | 18 | 306 | 0 |
| 1984/1985 | 306 / 306 | 18 | 306 | 0 |
| 1985/1986 | 306 / 306 | 18 | 306 | 0 |
| 1986/1987 | 306 / 306 | 18 | 306 | 0 |
| 1987/1988 | 306 / 306 | 18 | 306 | 0 |
| 1988/1989 | 306 / 306 | 18 | 306 | 0 |
| 1989/1990 | 306 / 306 | 18 | 306 | 0 |
| 1990/1991 | 306 / 306 | 18 | 306 | 0 |
| 1991/1992 | 306 / 306 | 18 | 306 | 0 |
| 1992/1993 | 306 / 306 | 18 | 306 | 0 |
| 1993/1994 | 306 / 306 | 18 | 306 | 0 |
| 1994/1995 | 306 / 306 | 18 | 306 | 0 |
| 1995/1996 | 306 / 306 | 18 | 306 | 0 |
| 1996/1997 | 306 / 306 | 18 | 306 | 0 |
| 1997/1998 | 306 / 306 | 18 | 306 | 0 |
| 1998/1999 | 306 / 306 | 18 | 306 | 0 |
| 1999/2000 | 306 / 306 | 18 | 306 | 0 |
| 2000/2001 | 306 / 306 | 18 | 306 | 0 |
| 2001/2002 | 306 / 306 | 18 | 306 | 0 |
| 2002/2003 | 306 / 306 | 18 | 306 | 0 |
| 2003/2004 | 306 / 306 | 18 | 306 | 0 |
| 2004/2005 | 306 / 306 | 18 | 306 | 0 |
| 2005/2006 | 306 / 306 | 18 | 306 | 0 |
| 2006/2007 | 306 / 306 | 18 | 306 | 0 |
| 2007/2008 | 306 / 306 | 18 | 306 | 0 |
| 2008/2009 | 306 / 306 | 18 | 306 | 0 |
| 2009/2010 | 306 / 306 | 18 | 306 | 0 |
| 2010/2011 | 306 / 306 | 18 | 306 | 0 |
| 2011/2012 | 306 / 306 | 18 | 306 | 0 |
| 2012/2013 | 306 / 306 | 18 | 306 | 0 |
| 2013/2014 | 306 / 306 | 18 | 306 | 0 |
| 2014/2015 | 306 / 306 | 18 | 306 | 0 |
| 2015/2016 | 306 / 306 | 18 | 306 | 0 |
| 2016/2017 | 306 / 306 | 18 | 306 | 0 |
| 2017/2018 | 306 / 306 | 18 | 306 | 0 |
| 2018/2019 | 306 / 306 | 18 | 306 | 0 |
| 2019/2020 | 232 / 232 | 18 | 306 | 74 |
| 2020/2021 | 306 / 306 | 18 | 306 | 0 |
| 2021/2022 | 306 / 306 | 18 | 306 | 0 |
| 2022/2023 | 306 / 306 | 18 | 306 | 0 |
| 2023/2024 | 306 / 306 | 18 | 306 | 0 |
| 2024/2025 | 306 / 306 | 18 | 306 | 0 |

## Five modern samples

| Season | Observed | Scored | Unscored | Source-marked cancelled | Clubs | Expected slots | Missing / duplicate pairs | Wide rounds |
|---|---:|---:|---:|---:|---:|---:|---|---:|
| 2018/2019 | 306 | 306 | 0 | 0 | 18 | 306 | 0 / 0 | 1 |
| 2019/2020 | 306 | 232 | 74 | 74 | 18 | 306 | 0 / 0 | 2 |
| 2023/2024 | 306 | 306 | 0 | 0 | 18 | 306 | 0 / 0 | 3 |
| 2024/2025 | 306 | 306 | 0 | 0 | 18 | 306 | 0 / 0 | 7 |
| 2025/2026 | 306 | 305 | 1 | 1 | 18 | 306 | 0 / 0 | 4 |

Total modern observations: 1,530, comprising 1,455 score-bearing and 75 source-marked unscored cancellations. These are source classifications, not approved historical NOT PLAYED decisions: the 2025/26 cancellation conflicts with completion evidence. Every sample has full directed pairing coverage, zero unexplained unscored records, zero invalid full-time fields and no other-stage observations. No source-marked awards/replays occur in these five files; that does not establish absence of administrative history.

Modern dates use explicit day/month/weekday headings, with the year either explicit or uniquely resolved against the season and weekday. No nominal round-number date was substituted. There are 17 wide-round contexts / 153 members and five adjacent physical-order date reversals. These are retained as review diagnostics, not corrections. Repeated round headings in 2023/24, 2024/25 and 2025/26 split rescheduled fixture groups; they are preserved, not mistaken for duplicate matches.

| Season | Repeated round headings | Physical-order reversal pairs |
|---|---|---:|
| 2018/2019 | {} | 3 |
| 2019/2020 | {} | 2 |
| 2023/2024 | {"10": 2, "3": 3, "7": 2} | 0 |
| 2024/2025 | {"17": 2, "20": 2, "23": 2, "25": 2, "3": 2, "31": 2, "4": 2, "5": 2} | 0 |
| 2025/2026 | {"16": 2, "18": 2, "20": 2, "3": 3} | 0 |

## Cancellation semantics: 2019/20

OpenFootball explicitly represents all 306 slots: 232 scored results and 74 `[cancelled]` null-score observations, with zero source-absent directed pairings. The historical CSV contains 232 scored rows and omits the other 74 pairings entirely. Those are different representations and must not be conflated.

C01 is indexed official termination evidence with a maintenance limitation; C02 is directly inspected contemporary participant reporting that standings were retained for European qualification, no champion was selected, and no promotion/relegation took place. This does not establish blanket legal annulment of all played matches. Source cancellation, scheduled date, played status and legal disposition remain separate. No future screening decision was assigned.

## Historical-modern overlap

Exact-label matches are reported separately from conditional season-local label hypotheses. The latter link candidate corresponding observations only to inspect scores/dates; they do not modify source labels, approve global aliases or certify club continuity. Source agreement does not establish upstream independence.

| Season | Historical records | Modern slots | Exact-label matches | Conditional comparisons | Score differences | Date differences |
|---|---:|---:|---:|---:|---:|---:|
| 2018/2019 | 306 | 306 | 272 | 306 | 0 | 0 |
| 2019/2020 | 232 | 306 | 206 | 232 | 0 | 0 |
| 2023/2024 | 306 | 306 | 72 | 306 | 1 | 0 |
| 2024/2025 | 306 | 306 | 72 | 306 | 0 | 0 |
| 2025/2026 | 0 | 306 | 0 | 0 | 0 | 0 |

All 1,150 historical scored observations in the four overlapping sample seasons can be conditionally linked. There are zero date differences and one score conflict. The 74 unmatched modern 2019/20 observations are the explicit cancellations omitted from the historical CSV. There is no historical 2025/26 overlap; its 306 modern observations are not 306 missing historical source records.

**NEC–Vitesse, 2023-10-01:** historical `NEC Nijmegen`–`Vitesse` is 1–3; modern `NEC`–`SBV Vitesse` is 1–2. Both source observations remain unchanged. C09 directly displays 1–3 and the late third goal; C10 directly exposes a dated 1–3 club headline, with narrative available only through index. This supports a historical-review candidate rather than a silent Phase 2 correction.

Conditional hypotheses include Heracles/Heracles Almelo; AZ Alkmaar/AZ; Almere City/Almere City FC; FC Twente/FC Twente ’65; Feyenoord/Feyenoord Rotterdam; NEC Nijmegen/NEC; PSV Eindhoven/PSV; Vitesse/SBV Vitesse; sc Heerenveen/SC Heerenveen; Willem II/Willem II Tilburg. They are explicitly season-local and are not applied to a standardized identity.

## Interrupted fixtures and source bindings

| Fixture | Original OpenFootball line | Source date and FT | Initial event / completion evidence |
|---|---:|---|---|
| AFC Ajax–Feyenoord Rotterdam | 91 | 2023-09-27; 0-4 | 2023-09-24 / 2023-09-27 |
| RKC Waalwijk–AFC Ajax | 228 | 2023-12-06; 2-3 | 2023-09-30 / 2023-12-06 |
| AZ–NEC | 223 | 2023-12-06; 1-2 | 2023-10-29 / 2023-12-06 |

All three modern observations use the reported completion day, and the corresponding historical CSV observations also use those dates and scores. The two repositories’ agreement is not independently certified source lineage. C04 corroborates Ajax completion/result; C05 and C06 distinguish RKC scheduling from actual completion; C07 is indexed-only scheduling evidence and C08 a directly inspected club matchcenter for AZ–NEC. Exact audit IDs, physical lines, SHA-256 bindings, original kickoff/completion research and unresolved availability fields are private. Phase 5 must assess evidence strength and Phase 6 must approve actual availability rules; a completion-day-looking source heading is not by itself training authorization.

**Additional 2025/26 anomaly — NAC Breda–SC Heerenveen:** line 509 records source date 2026-05-10 and `[cancelled]` without goals. C12 documents interruption at 2–0 and intended next-day continuation; directly inspected C13 reports actual completion on May 11 at 2–0, with NAC still the home-designated side despite the continuation venue in Heerenveen. The original null score and annotation remain unchanged. This is a source-completeness/status conflict, not an approved NOT PLAYED classification. Any supplemental source/result acquisition or correction needs separate approval and later policy review. No new season dataset was fetched to fill it.

## Club identities, schema and permissions

Observed historical labels include NEC Nijmegen, RKC Waalwijk, NAC Breda, FC Zwolle, PEC Zwolle, PEC Zwolle ’82, FC Den Haag, FC Den Haag-ADO, ADO Den Haag, SVV Schiedam, S.V.V./Dordrecht ’90, Dordrecht ’90 and FC Dordrecht. Modern labels include NEC, RKC Waalwijk and NAC Breda. Literal `N.E.C.` is present in evidence, not these five modern source files. No Jong/reserve labels occur in the acquired fixture population, which is not proof of universal identity equivalence. Ajax/Jong Ajax and PSV/Jong PSV remain distinct by design; no reserve prefix is stripped. No predecessor/successor merger is authorized.

Both formats can support the future exact eight-column schema, canonical `Eredivisie`, YYYY/YYYY seasons, source-bound audit IDs and the shared deterministic match-ID algorithm. No final match IDs or standardized records were generated. Complete numeric goals, dates and venue assignments can be extracted, but legal outcomes, interrupted availability and historical identity confidence need separate audit metadata. Postseason, Eerste Divisie, cup and friendly records must remain excluded from eventual regular-season selection.

Technical usability, acquisition authorization, historical confidence, redistribution rights and model-training permission are distinct. The historical README permits noncommercial use with attribution; GPL >=2 package metadata is not assumed to settle underlying data rights. OpenFootball CC0 applies to rights held, with upstream provenance unestablished. Acquisition was authorized for private feasibility; neither dataset has been cleared here for unrestricted redistribution or model training. Only source notices, bibliographic references and concise documentary findings are retained; full copyrighted articles were not copied.

## Individual evidence references

| ID | Title / URL | Publication | Access | Establishes / limits |
|---|---|---|---|---|
| C01 | [Afwikkeling voetbalseizoen 2019/20 een feit](https://www.knvb.nl/node/59905) | 2020-04-24 | INDEX_ONLY_DIRECT_MAINTENANCE | Official indexed termination notice; direct page returned maintenance. No blanket match-annulment inference. |
| C02 | [PSV eindigt Eredivisie als vierde](https://www.psv.nl/media/artikel/psv-eindigt-eredivisie-als-vierde) | 2020-04-24 | DIRECT | Contemporary participant report: existing standings used, no champion, no promotion/relegation; remaining fixtures not played. Not a signed legal decision for every result. |
| C03 | [Ajax – Feyenoord wordt 27 september uitgespeeld](https://www.knvb.nl/nieuws/betaald-voetbal/competitiezaken/68180/ajax-%E2%80%93-feyenoord-wordt-27-september-uitgespeeld) | 2023-09-25 | DIRECT_WITH_MAINTENANCE_BANNER | Article body was available in earlier Phase 1 inspection; Phase 2 direct return had maintenance banner. Preserve as scheduling reference, not fresh full primary certification. |
| C04 | [Verslag: Ajax verliest Klassieker in eigen huis](https://www.ajax.nl/artikelen/verslag-ajax-verliest-klassieker-in-eigen-huis) | 2023-09-27 | DIRECT | Participant-authored narrative establishes resumed Wednesday match and final 0-4; completion date September 27. |
| C05 | [Restant RKC Waalwijk–Ajax uitgespeeld op woensdag 6 december](https://eredivisie.nl/nieuws/rkc-waalwijk-ajax-uitgespeeld-op-woensdag-6-december/) | 2023-10-04 | DIRECT | Official scheduling explanation: original September 30 interruption and planned December 6 resumption; scheduling alone does not certify actual completion. |
| C06 | [Ajax trekt zege in duel van tien minuten bij RKC Waalwijk over de streep](https://nos.nl/artikel/2500620-ajax-trekt-zege-in-duel-van-tien-minuten-bij-rkc-waalwijk-over-de-streep) | 2023-12-06 | DIRECT | Contemporary narrative establishes completion December 6 without further goals, final home-away score 2-3. |
| C07 | [Restant AZ–NEC wordt uitgespeeld op woensdag 6 december](https://www.knvb.nl/node/68342) | 2023-11-02 | INDEX_ONLY_DIRECT_CACHE_MISS | Official indexed scheduling explanation: October 29 interruption and December 6 resumption. Direct retrieval unavailable. |
| C08 | [AZ–NEC matchcenter](https://www.nec-nijmegen.nl/wedstrijden/wedstrijd/az-nec-2023-12-06z-180000z.htm) | 2023-12-06 | DIRECT | Club matchcenter lists December 6 completion at 1-2. Participant platform/feed independence from compiled sources not established. |
| C09 | [NEC–Vitesse matchcenter](https://www.nec-nijmegen.nl/wedstrijden/wedstrijd/nec-vitesse-2023-10-01z-101500z.htm) | 2023-10-01 | DIRECT | Club record lists 1-3 on October 1 and late third goal; independently supports investigating OpenFootball 1-2. Feed upstream independence not established. |
| C10 | [Vitesse wint de 61ste Gelderse derby met 1-3 van NEC](https://www.vitesse.nl/nieuws/2023/vitesse-wint-de-61ste-gelderse-derby-met-1-3-van-nec) | 2023-10-01 | DIRECT_TITLE_DATE_ONLY | Direct page exposes title and date supporting 1-3. Narrative appears in search index but not directly rendered body; no full article certification. |
| C11 | [Wedstrijd NAC Breda–sc Heerenveen definitief gestaakt](https://www.knvb.nl/nieuws/betaald-voetbal/vriendenloterij-eredivisie/71803/wedstrijd-nac-breda-sc-heerenveen-definitief) | 2026-05-10 | INDEX_ONLY_DIRECT_MAINTENANCE | Indexed official announcement says remaining minutes to be played May 11 at opponent venue; not treated as directly inspected decision body. |
| C12 | [Update duel NAC–sc Heerenveen](https://www.nac.nl/nieuws/update-duel-nac-sc-heerenveen) | 2026-05-10 | DIRECT | Participant narrative: stopped after 82 minutes at 2-0; continuation next afternoon in Heerenveen. Home designation remains NAC despite changed venue. |
| C13 | [Gedegradeerd NAC pakt in Heerenveen drie punten, geen goals meer in restant duel](https://nos.nl/artikel/2613947-gedegradeerd-nac-pakt-in-heerenveen-drie-punten-geen-goals-meer-in-restant-duel) | 2026-05-11 | DIRECT | Contemporary authored report: resumed fixture completed May 11 at 2-0 for NAC. Evidence only; no source score filled. |

Access date for these documents: 2026-11-22. Official titles or snippets are not promoted to directly inspected primary decisions. Participant matchcenter feeds may share upstream providers; authored narratives and official decisions are assessed separately.

## Reproducibility and fresh tests

The production assessment and separate verifier use different parsing paths. The independent verifier rechecks historical coverage and selected source-row bindings, then independently parses every modern fixture/date/score/annotation. Its six-source reconciliation succeeds. All six generated assessment/reconciliation artifacts were regenerated in a separate Python process in safe temporary storage and match saved bytes and SHA-256.

| Artifact | SHA-256 |
|---|---|
| `coverage_inventory.json` | `eb38870e3c236723a71d4e57b8d61c53afac0dc64dc37d8dd2ca5cddce392be5` |
| `exception_diagnostics.json` | `a30626f6712c6050a6ce48f313a5e38b1c39aba0061ae1a717baa90c3954d926` |
| `feasibility_assessment.json` | `a665d88cc7c6d48ffebc4d738f31fdbbfcf7152258a96676f334d21396519641` |
| `identity_overlap_diagnostics.json` | `feb076ab4718986c4ec166a35a39e32308b7b5f7b99fd307e92946a5f736e428` |
| `independent_reconciliation.json` | `8236226e2a4199214949f55d546dfd6fa4f66750b3d9090f548b0043daac1803` |
| `overlap_diagnostics.json` | `2aec3c634d42fc4a6bda7fe956f9eb62b3204c9ad3bba7c930cf81954457bcd9` |

```sh
PYTHONPATH=. python -B scripts/collect_eredivisie_feasibility.py --init-only
PYTHONPATH=. python -B scripts/collect_eredivisie_feasibility.py
PYTHONPATH=. python -B scripts/validate_eredivisie_feasibility.py
PYTHONPATH=. python -B scripts/verify_eredivisie_feasibility.py
```

The collector is bounded to six fixed paths, refuses partial/tampered caches and never overwrites differing originals. A retained access-stop receipt prevents retries. Assessment entry points refuse differing outputs. No dependency installation or original .venv modification was needed; the preserved external Python 3.13.12 environment ran fresh tests with bytecode/pytest caching disabled.

| Scope | Passed | Failures | Errors | Skipped |
|---|---:|---:|---:|---:|
| New Eredivisie | 48 | 0 | 0 | 0 |
| Existing acquisition/importer-related selection | 529 | 0 | 0 | 0 |
| Non-UI regression suite | 1,600 | 0 | 0 | 0 |
| App/launcher | 7 | 0 | 0 | 0 |
| Full repository | 1,607 | 0 | 0 | 0 |

Scopes overlap; counts are not additive. The acquisition/importer selection covers existing feasibility, history, historical-import and standardization test files. Logs, XML and exit statuses are private. Protected earlier files, planning prefix, source hashes/blobs, Git HEAD/staging-state and private-ignore checks pass; no prior assessment, earlier competition implementation, application or promotional worktree was changed.

Public Phase 2 files are three scripts (`collect_eredivisie_feasibility.py`, `validate_eredivisie_feasibility.py`, `verify_eredivisie_feasibility.py`), `tests/test_eredivisie_feasibility.py`, this report and appended PLANNING_LOG entries. Private files include six originals/receipts, reused metadata/notices, protected baseline, five assessment/diagnostic outputs, independent reconciliation, documentary references and verification receipts/logs.

## Exact proposed Phase 3 scope — not started

The complete 36-season objective remains 1990/91–2025/26. A provisional source split is the existing historical CSV for 1990/91–2017/18 and OpenFootball for 2018/19–2025/26. The CSV provides measured continuity through 2017/18 and beyond, but final historical confidence is not established. Retain later CSV overlap for comparison; do not silently choose between conflicting sources.

If approved, acquire only the three remaining pinned modern originals:

- `netherlands/2020-21_nl1.txt` — blob `60762d0a8bbc3b62ea1199706caea7f929ec0a43`
- `netherlands/2021-22_nl1.txt` — blob `6249665f226cf6259bfd2a9e72747295010394bb`
- `netherlands/2022-23_nl1.txt` — blob `23268303742116f940ca5d763e1ba9b54ab65bf6`

Use the same OpenFootball revision and reuse all existing originals. Build the complete bounded inventory before structural/historical certification. The three path/blob identities are confirmed in the retained pinned tree, but those files have not been downloaded in Phase 2.

Carry NEC–Vitesse score conflict, NAC–Heerenveen missing completion/status conflict, three 2023/24 interruptions, 2019/20 cancellation semantics, wide spans/reversals and identity risks forward. Resolving NAC 2025/26 requires separately authorized evidence/supplemental treatment; do not change revision or import the reported 2–0 automatically. No older acquisition gap is currently demonstrated in 1990/91–2024/25, but source completeness is not historical correctness. Permissions and actual availability remain approval gates before downstream use.

Stop after Phase 2. No Phase 3 acquisition, final historical decisions, screening, standardization, integration, training or Git publication has occurred.
