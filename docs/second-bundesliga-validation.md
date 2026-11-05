# German 2. Bundesliga acquisition and structural validation

Completed 2026-11-05; publication review 2026-11-06. Scope: 36 completed seasons, 1990/1991–2025/2026. Acquisition, independent review and local standardization are complete. No ongoing 2026/2027 acquisition, integration, training or evaluation was performed. Earlier sections retain their explicitly chronological audit findings.

**Completed outcome: 11,488 standardized matches, nine linked fixture exceptions and one verified derivative-only replay correction. All originals remain unchanged. See the Standardization section for final results and checksums; raw-source statuses below are acquisition-stage snapshots.**

## Acquisition-stage outcome and source selection

**11,488 selected scored source records across all 36 seasons acquired privately. All 36 fixture schedules pass structural checks.** After documentary exception review, statuses are **30 PASS, five PASS_WITH_NOTES and one REVIEW (2005/06)**. Counts alone conceal one substantive problem: the primary 2005/06 file retains an annulled Burghausen–1860 result rather than the replay. The source has not been repaired. Thus complete fixture slots do not yet constitute a fully validated set of official final outcomes.

Use **engsoccerdata for 1990/91–2024/25 (35 seasons, 11,182 rows)** and **OpenFootball's explicitly OpenLigaDB-derived export for 2025/26 (306 rows)**. This covers the target with one source change. Keep the two provenance/licence families separate. Four original exports were downloaded: two aggregated CSVs and two single-season Football.TXT files. Overlapping supplementary records and unscored fixtures are not added to the 11,488 selected total. No repositories were cloned.

### Candidate comparison, provenance and access

- **E — [jalapic/engsoccerdata](https://github.com/jalapic/engsoccerdata)**, commit `872c5c354161ace8408f3091b758c6af4cccca94`, package version 0.1.8. [Pinned Germany CSV](https://raw.githubusercontent.com/jalapic/engsoccerdata/872c5c354161ace8408f3091b758c6af4cccca94/data-raw/germany.csv): 38,918 total source rows, mixed tiers and earlier history; select only `tier=2`, `Season=1990..2024`. The resulting 11,182 rows cover all 35 seasons at the expected counts, including 384 in 1991/92. Retain source `division` values `2North`/`2South` in that season. No 2025/26 records exist in this snapshot. The repository's old `germany2.csv` is not needed: the current combined export already includes the second tier. The [update script](https://github.com/jalapic/engsoccerdata/blob/872c5c354161ace8408f3091b758c6af4cccca94/data-raw/munge/germany_munge.R) explicitly uses Football-Data for modern updates; older rows lack a complete per-row source chain. Team labels are the compiler's conventions, often modernized/transliterated, and are preserved rather than converted to historical names.
- **A — [AllBundesligaGamesEver](https://github.com/thomascamminady/AllBundesligaGamesEver)**, commit `9da303b7f8ee074c53f64f8f1f54b58013d3a9c3`. The [semicolon CSV](https://raw.githubusercontent.com/thomascamminady/AllBundesligaGamesEver/9da303b7f8ee074c53f64f8f1f54b58013d3a9c3/AllBundesligaGamesEver.csv) has 36,962 mixed-tier/all-era rows. Target-scope `League=2. Bundesliga` rows cover 1990/91–2019/20: **9,783 raw rows, including 126 exact dated-fixture/score duplicate excess rows**. Five further excess rows remain after exact duplicate counting versus the 9,652 expected fixture slots; these cannot be silently treated as additional league matches. Its flags identify two annulled originals, but the README and actual flags do not consistently describe the same cases. Two 2017/18 abandoned 0–0 originals are unflagged; the 2003 Aachen annulled original is also misreported as 3–0 versus the club archive's 1–0. These errors concern the rejected supplementary rows, not additional accepted matches. Required date/team/full-score fields are present and Score90 agrees with its goal columns in the inspected target rows; **6,982 points-column outcomes disagree with the displayed goals under the applicable two-/three-point rules**. Do not use these points columns to infer results, group rankings or administrative decisions. The author's README says results were scraped from Kicker. The already published export was downloaded; its scraper/notebook was not run, Kicker was not scraped, and no deduplication or silent substitution was applied. Retain only as a supplementary diagnostic reference, not a primary or independent ground truth.
- **F — [Football-Data Germany archive](https://www.football-data.co.uk/germanym.php)**: the web reader returned **HTTP 429** during this study. No dataset requests, retries, alternate-host access or challenge bypass followed. Consequently current direct `D2.csv` season availability was not verified and no F originals were acquired. E's declared modern Football-Data lineage does not make E/F agreement independent, or clear upstream rights. Do not characterize a web-reader 429 as proof that every CSV URL is permanently unavailable.
- **O — [OpenFootball/deutschland](https://github.com/openfootball/deutschland)**, commit `c34532ab6950aa0089ef1c736ffdb8c818c3356f`. The complete saved tree lists main `2-bundesliga2.txt` files for 2012/13–2025/26, and distinct `openliga/*_de.2.txt` exports for 2020/21–2026/27. File existence alone does not certify contents: only the two 2025/26 files were downloaded/tested here. The [main 2025/26 file](https://github.com/openfootball/deutschland/blob/c34532ab6950aa0089ef1c736ffdb8c818c3356f/2025-26/2-bundesliga2.txt) contains all 306 scheduled fixtures but **only 99 scored matches; 207 are unscored**. It was rejected for completed-season acquisition. The separate [OpenLigaDB-derived file](https://github.com/openfootball/deutschland/blob/c34532ab6950aa0089ef1c736ffdb8c818c3356f/openliga/2025-26_de.2.txt) contains 306 scored fixtures, 18 clubs and 34 complete rounds. Its own header identifies `https://api.openligadb.de/getmatchdata/bl2/2025` as upstream. It is the selected 2025/26 supplement. No API call or ongoing-season export download was needed.

Publication independence is limited: E and F share declared lineage; A is Kicker-derived, and O/OpenLigaDB is community-maintained. Those different publications are useful for discrepancy detection, but unknown older E origins and community contributors prevent a blanket independent-generation claim. This is **structural validation and targeted anomaly research, not the later reproducible external sample-verification stage**. A's agreement cannot resolve an exception by itself.

## Licensing and restrictions

[GitHub's platform/API terms](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service) apply to the direct public metadata/raw routes. Requests were bounded, sequential and paced at least five seconds apart within each batch, with immutable caching and SHA-256 receipts. All GitHub responses used for originals succeeded without authentication or bypass. No DFB request or collector execution occurred.

E's saved [README](https://github.com/jalapic/engsoccerdata/blob/872c5c354161ace8408f3091b758c6af4cccca94/README.md) permits non-commercial use and requests attribution to James P. Curley (2016), while [DESCRIPTION](https://github.com/jalapic/engsoccerdata/blob/872c5c354161ace8408f3091b758c6af4cccca94/DESCRIPTION) declares GPL (>=2). **Preserve both notices; do not treat the package GPL declaration as unambiguous commercial data clearance.** The current acquisition is private inspection only; no commercial, model, public-service or redistribution permission is inferred. The README lists several historical providers and the modern update script uses Football-Data; no complete upstream sublicense/rights chain was established.

A has an [MIT notice](https://github.com/thomascamminady/AllBundesligaGamesEver/blob/9da303b7f8ee074c53f64f8f1f54b58013d3a9c3/LICENSE), retained verbatim. It does not establish clearance for Kicker-derived data. The Kicker terms page exposed robot/JavaScript verification in the reader, not readable conditions; this was not bypassed and no upstream scraping was attempted. Data-specific licence scope and upstream rights remain uncertain.

O's repository [CC0 notice](https://github.com/openfootball/deutschland/blob/c34532ab6950aa0089ef1c736ffdb8c818c3356f/LICENSE.md) only covers rights held by its affirmer. The selected `openliga/` export is explicitly a conversion from OpenLigaDB: the [upstream homepage](https://www.openligadb.de/) declares **ODbL**, and the [ODbL 1.0 text](https://opendatacommons.org/licenses/odbl/1-0/) governs attribution/share-alike obligations where applicable. **Do not relabel the selected export CC0-only or merge away its ODbL provenance.** The upstream detailed terms/licence pages returned no readable text in the web reader; its homepage nevertheless explicitly describes automated data access and the data licence. Intended-use, derivative-database and redistribution obligations require review before future use. No blanket third-party clearance is claimed for any candidate.

## Historical formats and validation rules

The [official league history](https://www.bundesliga.com/de/bundesliga/news/60-jahre-bundesliga-1983-1993-live-tv-24519) describes the reunification expansion. A [DFL historical report](https://media.dfl.de/sites/3/2018/11/dfl-report-2009-en.pdf) identifies the 24- and 20-club transitional seasons. The [1991/92 format synopsis](https://en.wikipedia.org/wiki/1991%E2%80%9392_2._Bundesliga) and observed source schedules distinguish integrated promotion/relegation **league groups** from external promotion/relegation playoffs. These documentary format references are not independent certification of all match results.

- 1990/91 and 1993/94: 20 clubs, 380 fixtures, 19 home/19 away per club.
- 1992/93: 24 clubs in one division, 552 fixtures, 23 home/23 away.
- 1994/95–2025/26: 18 clubs, 306 fixtures, 17 home/17 away.
- 1991/92: two regional divisions of 12. Each first phase has 12 × 11 = 132 fixtures. Each region then divides into top-six promotion and bottom-six relegation league groups, each with 6 × 5 = 30 further fixtures. Total **2 × (132 + 30 + 30) = 384**; every club plays 32 games, 16 home/16 away. Across the full target: 380 + 384 + 552 + 380 + 32 × 306 = **11,488**.

For 1991/92, the source's first phases end 15 December 1991; second phases begin 6 March 1992 (South) and 7 March (North). The validator uses the explicit season-specific year boundary, not an arbitrary first-132-row split. It checks disjoint 12-team regional rosters, every ordered pairing exactly once in each first phase, and uses the first-phase two-points table (points, goal difference, goals) to require the actual second phase to match the top-six and bottom-six schedules separately. Both regions contain precisely 60 second-phase matches. All four group memberships and balances are retained privately. **120 repeated ordered pairings across phases are legitimate**, not duplicate league records; same-date duplicate/conflicting matches and repeated pairings within a phase remain errors. No ordinary 24-team/552-match requirement was applied to this season.

`scripts/validate_second_bundesliga.py` reuses the existing historical dataframe validator, season canonicalizer, exact-integer/team validation, outcome helper and deterministic CSV serializer. New code supplies source-specific adapters and the exceptional schedule logic, rather than a new importer. The existing Bundesliga validator and DFB code are unchanged.

All selected source records are checked for required dates/names/nonnegative integer full scores, correct tier/division or explicit Football.TXT competition/season heading, FT versus separate goal-column agreement where available, season calendar bounds, future dates, exact dated duplicates/conflicts, season-specific team/count expectations and home-away completeness. The public historical validator accepts every selected scored record. The single-phase ordered-pair requirement implies balanced home-away schedules. For the 2025/26 export, all 34 rounds have nine fixtures and each club appears exactly once per round; optional halftime scores cannot exceed the final score. English month/day context and season years are explicit; unknown lines/layouts, absent dates and unscored fixtures are reported rather than filled.

Football.TXT goal-event continuation lines and venue annotations are excluded from match counts. No missing values are filled, no aliases mapped, no results corrected, and no duplicate rows silently dropped. E has no separate H/D/A column; its FT string is compared with separately supplied hgoal/vgoal. O's goals derive from its displayed score, so agreement with an independent Result column cannot be claimed. Neither selected export supplies exhaustive official finality/administrative-status evidence. Numeric, internally consistent scores are not proof of normal 90-minute completion.

## Season-by-season coverage and validation

PASS = structural checks passed with no identified documentary issue, not exhaustive factual verification. PASS_WITH_NOTES = structural pass with disclosed exceptional/administrative context. REVIEW = fixture-complete but a known result/date issue remains unresolved. A counts below are **raw overlapping supplementary rows**, not additional accepted matches. O entries marked "listed" are inventory evidence only, not downloaded/validated seasons. Football-Data current coverage is unverified throughout because access stopped at the 429 response.

| Season | Primary | Teams actual/expected | Matches actual/expected | First date | Last date | Status | A raw rows | O availability | Notes |
|---|---|---:|---:|---|---|---|---:|---|---|
| 1990/1991 | E | 20/20 | 380/380 | 1990-07-27 | 1991-06-16 | PASS_WITH_NOTES | 394 | not listed | Essen licence/forced relegation; no score edits |
| 1991/1992 | E | 24/24 | 384/384 | 1991-07-23 | 1992-05-17 | PASS | 388 | not listed | Two regional + four second-phase group schedules pass |
| 1992/1993 | E | 24/24 | 552/552 | 1992-07-10 | 1993-06-06 | PASS | 559 | not listed | none detected |
| 1993/1994 | E | 20/20 | 380/380 | 1993-07-27 | 1994-06-11 | PASS_WITH_NOTES | 395 | not listed | Essen table sanction; Uerdingen–Bochum replay |
| 1994/1995 | E | 18/18 | 306/306 | 1994-08-19 | 1995-06-18 | PASS | 309 | not listed | none detected |
| 1995/1996 | E | 18/18 | 306/306 | 1995-08-04 | 1996-06-08 | PASS | 316 | not listed | none detected |
| 1996/1997 | E | 18/18 | 306/306 | 1996-08-02 | 1997-06-11 | PASS | 310 | not listed | none detected |
| 1997/1998 | E | 18/18 | 306/306 | 1997-07-25 | 1998-06-07 | PASS | 312 | not listed | none detected |
| 1998/1999 | E | 18/18 | 306/306 | 1998-07-30 | 1999-06-17 | PASS | 311 | not listed | none detected |
| 1999/2000 | E | 18/18 | 306/306 | 1999-08-13 | 2000-05-26 | PASS | 309 | not listed | none detected |
| 2000/2001 | E | 18/18 | 306/306 | 2000-08-11 | 2001-05-20 | PASS | 316 | not listed | none detected |
| 2001/2002 | E | 18/18 | 306/306 | 2001-07-27 | 2002-05-05 | PASS | 308 | not listed | none detected |
| 2002/2003 | E | 18/18 | 306/306 | 2002-08-10 | 2003-05-25 | PASS | 312 | not listed | none detected |
| 2003/2004 | E | 18/18 | 306/306 | 2003-08-03 | 2004-05-23 | PASS_WITH_NOTES | 311 | not listed | Aachen–Nürnberg replay retained |
| 2004/2005 | E | 18/18 | 306/306 | 2004-08-07 | 2005-05-22 | PASS_WITH_NOTES | 313 | not listed | Ahlen replay; Erfurt award; manipulation concerns |
| 2005/2006 | E | 18/18 | 306/306 | 2005-08-06 | 2006-05-14 | REVIEW | 321 | not listed | Annulled Burghausen–1860 original retained; replay missing |
| 2006/2007 | E | 18/18 | 306/306 | 2006-08-11 | 2007-05-20 | PASS | 306 | not listed | none detected |
| 2007/2008 | E | 18/18 | 306/306 | 2007-08-10 | 2008-05-18 | PASS | 306 | not listed | none detected |
| 2008/2009 | E | 18/18 | 306/306 | 2008-08-15 | 2009-05-24 | PASS | 306 | not listed | none detected |
| 2009/2010 | E | 18/18 | 306/306 | 2009-08-07 | 2010-05-09 | PASS | 308 | not listed | none detected |
| 2010/2011 | E | 18/18 | 306/306 | 2010-08-20 | 2011-05-15 | PASS | 307 | not listed | none detected |
| 2011/2012 | E | 18/18 | 306/306 | 2011-07-15 | 2012-05-06 | PASS | 307 | not listed | none detected |
| 2012/2013 | E | 18/18 | 306/306 | 2012-08-03 | 2013-05-19 | PASS | 306 | main listed, untested | none detected |
| 2013/2014 | E | 18/18 | 306/306 | 2013-07-19 | 2014-05-11 | PASS | 306 | main listed, untested | none detected |
| 2014/2015 | E | 18/18 | 306/306 | 2014-08-01 | 2015-05-24 | PASS | 306 | main listed, untested | none detected |
| 2015/2016 | E | 18/18 | 306/306 | 2015-07-24 | 2016-05-15 | PASS | 306 | main listed, untested | none detected |
| 2016/2017 | E | 18/18 | 306/306 | 2016-08-05 | 2017-05-21 | PASS | 306 | main listed, untested | none detected |
| 2017/2018 | E | 18/18 | 306/306 | 2017-07-28 | 2018-05-13 | PASS_WITH_NOTES | 310 | main listed, untested | Heidenheim–Aue and Darmstadt–FCK replays retained |
| 2018/2019 | E | 18/18 | 306/306 | 2018-08-03 | 2019-05-19 | PASS | 310 | main listed, untested | none detected |
| 2019/2020 | E | 18/18 | 306/306 | 2019-07-26 | 2020-06-28 | PASS | 309 | main listed, untested | none detected |
| 2020/2021 | E | 18/18 | 306/306 | 2020-09-18 | 2021-05-23 | PASS | — | main + openliga listed, untested | none detected |
| 2021/2022 | E | 18/18 | 306/306 | 2021-07-23 | 2022-05-15 | PASS | — | main + openliga listed, untested | none detected |
| 2022/2023 | E | 18/18 | 306/306 | 2022-07-15 | 2023-05-28 | PASS | — | main + openliga listed, untested | none detected |
| 2023/2024 | E | 18/18 | 306/306 | 2023-07-28 | 2024-05-19 | PASS | — | main + openliga listed, untested | none detected |
| 2024/2025 | E | 18/18 | 306/306 | 2024-08-02 | 2025-05-18 | PASS | — | main + openliga listed, untested | none detected |
| 2025/2026 | O/OpenLigaDB | 18/18 | 306/306 | 2025-08-01 | 2026-05-17 | PASS | — | main: 99 scored; openliga: 306 scored | none detected |

There are **no missing source season files, required dates/teams/full scores, same-date duplicate/conflicting selected matches, invalid competition labels, or missing expected fixture slots**. However, one *valid replay outcome* is missing/replaced by an annulled original in 2005/06, despite its correct raw count. This is a data-quality blocker, not an excuse to increase or reduce the 306 expected fixture slots. No external playoff fixtures were detected: selected tier/heading scope and exact season/phase schedules exclude extra playoff rounds and outside-club pairings. Source-classification correctness beyond these structural gates still needs external samples.

## Exceptional and uncertain results

`exception_review.json` records source SHA-256, exact original row/fields and evidence for nine targeted match cases, plus team-level context. It is explicitly non-exhaustive and applies no corrections.

- **1993/94 Uerdingen–Bochum:** source records the 31 May 1994 3–0 replay. [Uerdingen's club history](https://www.kfc-uerdingen.de/2020/04/tbt-der-fuenfte-aufstieg-in-die-bundesliga-1994/) explains the annulled 9 May 3–1 original. Retain only the valid fixture slot in a later archive, with original/replay metadata; no source record is altered here.
- **2003/04 Aachen–Nürnberg:** source records 26 January 2004, 3–2. [Aachen's official replay page](https://www.alemannia-aachen.de/profis/spielinfo/2-Bundesliga-Alemannia-Aachen-gegen-1-FC-Nuernberg-65979U/) and [separate annulled-game record](https://www.alemannia-aachen.de/profis/spielinfo/Alemannia-Aachen-1-FC-Nuernberg-91254u/) distinguish it from 24 November 2003, 1–0. That original is not another league fixture.
- **2004/05 Ahlen–Burghausen:** source records 27 April 2005, 1–3 replay. The 22 October 2004 1–0 original was annulled in the match-fixing case; see the [historical season archive](https://rsssf.github.io/tables/duit05.html). The unfiltered A export contains original/replay and duplicates and cannot simply be appended.
- **2004/05 Erfurt–Unterhaching:** source records 6 April 2005, official 0–2 award; played score was 2–0 following the later doping decision. The [historical archive](https://rsssf.github.io/tables/duit05.html) distinguishes them; the [contemporary-case retrospective](https://www.welt.de/sport/article942791/Dokumentation-16-Dopingfaelle-im-deutschen-Fussball.html) reports the sanction. This is an administrative away win, not the on-field outcome. Primary court documentation remains a later verification task.
- **2005/06 Burghausen–1860 — unresolved blocker:** E retains **4 November 2005, 0–2**, which A flags annulled. A also contains **29 March 2006, 1–0**, corroborated by the [indexed historical result](https://www.weltfussball.de/spielbericht/co3/2-bundesliga/ma196175/wacker-burghausen_tsv-1860-muenchen/). The direct historical-page fetch returned a cache miss, so it is not counted as a full-page verification. A [contemporary official Aachen report](https://www.alemannia-aachen.de/profis/spielinfo/2-Bundesliga-Alemannia-Aachen-gegen-TSV-1860-Muenchen-68153k/) separately discusses 1860 losing the replay that week. Obtain primary/official match or ruling evidence, resolve the finalized date/score and record a guarded future correction before standardization; **no result or date was replaced here**.
- **2017/18 Heidenheim–Aue and Darmstadt–Kaiserslautern:** source correctly retains the 9 August 2017 2–1 and 21 February 2018 1–2 replay records, respectively. The [Aue official programme](https://www.fc-erzgebirge.de/fileadmin/user_upload/202021/veilchenecho/20_ST_HSV_5_2_web.pdf) distinguishes the weather-abandoned 30 July 0–0 original from the replay; the [FCK club announcement](https://fck.de/blog/spielabbruch-in-darmstadt/) documents abandonment on 24 January 2018 because of a medical emergency, and the [Darmstadt archive](https://www.sv98.de/news/page/453/?cHash=38a2713a64ce58bd18bd77a0e22be126&tx_news_pi1%5Baction%5D=detail&tx_news_pi1%5Bcontroller%5D=News&tx_news_pi1%5Bnews%5D=8361) reports the replay loss. A retains both 0–0 originals without reliable abandonment flags. Do not interpret either original as a normal finished draw or append it to the selected season. These are targeted documentary checks, not the later fixed random/sample verification exercise.
- **Two further 2004/05 manipulation concerns:** Unterhaching–Saarbrücken and Karlsruhe–Duisburg are described as manipulation/attempt cases whose outcomes stood in the [historical scandal synopsis](https://en.wikipedia.org/wiki/2005_German_football_match-fixing_scandal). These are secondary-source leads, not newly certified awards; keep scores and review suitability/evidence later.

**Team/table sanctions are distinct:** Essen's 1990/91 licence-related relegation and 1993/94 special table treatment must not be converted into invented match awards. The [club's 1994 retrospective](https://www.rot-weiss-essen.de/2013/05/14/heute-vor-19-jahren-ganz-berlin-erstrahlt-in-rot-weiss/) supports the licence event. Detailed [1993/94 historical treatment](https://de.wikipedia.org/wiki/2._Fu%C3%9Fball-Bundesliga_1993/94) explains that opponents retained match results while Essen was classified without its sporting record. All 38 Essen fixtures in each season remain present; detailed table/decision semantics need primary confirmation. The private register binds affected source rows without asserting that 76 match scores were administratively changed.

The source declarations, A's status flags, optional O halftime information and targeted documentary research can identify known exceptions; they cannot establish that every unflagged match finished ordinarily. No match has been declared automatically model-eligible.

## Private artifacts and reproduction

All originals, extracts, receipts, source inventories, provenance, exception register and validation details live exclusively under ignored `data/private/germany/second_bundesliga/`:

- `originals/`: four byte-preserved exports, each with URL/final URL, original UTC retrieval timestamp, response metadata, byte length and SHA-256 receipt. Repository versions are pinned above and in `metadata/pins.json`.
- `metadata/`: untruncated GitHub trees/commit metadata and original licence/README/schema/update declarations. No guessed README coverage substitutes for file inspection.
- `acquisition.json`: selected/unselected sources, exact original download provenance, licence/attribution limitations and access observations.
- `engsoccerdata_second_tier_1990_2024.csv`: 11,182 unchanged source-schema rows; the original nine columns are retained, with no eight-column standardization.
- `structural_validation.json`: raw audit snapshot and extracted score facts; full 1991/92 group memberships/schedules, selected 2025/26 rounds, supplementary counts/flags and rejected main-file diagnostics.
- `validation.json`: 30 PASS / five PASS_WITH_NOTES / one REVIEW, explicitly separate from all 36 schedule-level passes.
- `exception_review.json`, `candidate_diagnostics.json`: bound documentary cases and the unselected A export's duplicate/points limitations. Private `review_sources.py` reproduces recorded documentary interpretation; it does not fetch or independently discover evidence.
- `protected_before.json`, `integrity_check.json`, `checksums.json`: pre-task fingerprints, post-task comparison and new-artifact checksums.

| Original filename | SHA-256 |
|---|---|
| `originals/engsoccerdata_germany.csv` | `e955aef5dabb62909d584ae3ba77c994078d031976b52241aebff190bf67d931` |
| `originals/AllBundesligaGamesEver.csv` | `8e5b22bf799a130bb2b307339ae98523d88707cd91ae2dd259540024fec61aba` |
| `originals/openfootball_2025-26_2-bundesliga2.txt` | `132ccb69da3633c3789bf0bb43b34f80c4e92a2e51b3ad926bb8ecfa93604aab` |
| `originals/openfootball_openliga_2025-26_de.2.txt` | `3b4613640c989703abe7517ad3132f1561f7be52e6a613174a1167e82ac34007` |

```sh
# Fixed inspected GitHub snapshot; reuse checksummed originals without new requests.
PYTHONPATH=src .venv/bin/python -m scripts.acquire_second_bundesliga
# First audit creates new artifacts; differing existing outputs are refused.
PYTHONPATH=src .venv/bin/python -m scripts.validate_second_bundesliga
# Read-only reconstruction of saved extract/structural diagnostics.
PYTHONPATH=src .venv/bin/python -m scripts.validate_second_bundesliga --check
# Reproduce previously recorded documentary review, without network research.
PYTHONPATH=src:. .venv/bin/python data/private/germany/second_bundesliga/review_sources.py
```

## Tests and preservation checks

**Full suite: 435 passed**, including 22 new synthetic tests for historical league sizes, valid/invalid regional phases, duplicates, source fields and classification, Football.TXT goal-event exclusion/unscored fixtures/calendar failures, immutable cache checks and access-denial stops. All network tests use injected responses; none requests DFB or Kicker. The read-only audit reproduces the saved extract and structural report byte-for-byte. Cached acquisition rechecks original hashes without new requests. The pre-task integrity snapshot confirms all earlier private artifacts and existing source/test files remain unchanged. All private files are Git-ignored and none are tracked.

## Acquisition-stage readiness snapshot

The complete selected snapshot is **ready for reproducible independent result verification**, with priority checks for the 1991/92 phase memberships/dates, source handover, replay/award cases, and 2005/06 Burghausen–1860. It is **not ready for whole-dataset standardization** until that date/outcome discrepancy is resolved with appropriate evidence and separately documented correction policy. Reassess the match-status/exception register and intended-use rights before future integration. No private data were published, no existing England/Bundesliga datasets or DFB code were changed, and no commit or push occurred.

## Independent verification and exception resolution — 2026-11-05

This section supersedes the acquisition-stage readiness conclusion, not its immutable source audit. No original, extract or earlier private report was rewritten. **21 full-page comparisons succeeded**, with five matches dated in each of the 1990s, 2000s and 2010s and six in the 2020s. Five additional matches agree in indexed evidence only and are **not** included in that 21. No sampled date, score or team-identity discrepancy was found; explicit aliases are documented below. This is bounded sample assurance, not certification of every result or training eligibility.

The fixed selection is recorded in `verification/sample_selection.json`: source order, offsets and scope were fixed before reference searches. The original 20 were retained even where a full reference was unavailable. `supplementary_selection.json` adds the first physical source rows for 1992/93, 2001/02, 2008/09, 2011/12 and 2023/24; `calendar_supplement_selection.json` adds the first 2015/16 row. These supplements were selected before their reference lookups. Calendar decades use actual match dates, not season labels: a March 2010 match from 2009/10 belongs to the 2010s. Each observation is tied to its original file checksum and physical source row.

### Match comparisons

All references classify these as second-tier regular-season fixtures. “Full” means the returned full page was inspected; “index only” is weaker evidence with the access limitation explicitly retained. Full fixture facts and reference labels with umlauts, prefixes or expanded names remain in the private comparison evidence; those identity mappings do not change the dataset. The machine-readable observations and exact mappings are private in `verification/independent_verification.json`.

| Sample ID | Reference | Access / result |
|---|---|---|
| SB-01 | [External reference](https://schalke04.de/verein/tradition/alle-spiele-alle-tore/bundesliga/zweitliga-saison-19901991/) | Full page; agrees |
| SB-02 | [External reference](https://datencenter.dfb.de/competitions/2-bundesliga/seasons/1991-1992-nord?datacenter_name=datencenter) | Full page; agrees |
| SB-03 | [External reference](https://datencenter.dfb.de/competitions/2-bundesliga/seasons/1991-1992-sued-abstieg/matchday?datacenter_name=datencenter) | Full page; agrees |
| SB-04 | [External reference](https://datencenter.dfb.de/competitions/2-bundesliga/seasons/1993-1994/teams/fc-st-pauli) | Full page; agrees |
| SB-05 | [External reference](https://www.fcenergie-museum.de/spiele-98-99.html) | Index only; agrees |
| SB-06 | [External reference](https://www.kickers-archiv.de/index.php/Main/2000-2001) | Index only; agrees |
| SB-07 | [External reference](https://www.alemannia-aachen.de/archiv/saisonarchiv/Spiele-Tabelle-2g/2002-2003-1l/) | Full page; agrees |
| SB-08 | [External reference](https://datencenter.dfb.de/competitions/2-bundesliga/seasons/2004-2005/teams/karlsruher-sc) | Full page; agrees |
| SB-09 | [External reference](https://www.kleeblatt-chronik.de/v3/saison/spiel_detail.php?id=11411&saison=20062007&team=1) | Full page; agrees |
| SB-10 | [External reference](https://www.alemannia-aachen.de/archiv/saisonarchiv/Spiele-Tabelle-2g/2009-2010-4182N/28-Spieltag-28q/) | Index only; agrees |
| SB-11 | [External reference](https://datencenter.dfb.de/competitions/2-bundesliga/seasons/2010-2011/teams/hertha-bsc) | Full page; agrees |
| SB-12 | [External reference](https://www.fc-union-berlin.de/de/matchcenter-tScyuUX2fgXxO3hkVFyuAss9d) | Full page; agrees |
| SB-13 | [External reference](https://www.fcn.de/news/artikel/das-club-magazin-zum-ingolstadt-spiel/) | Full page; agrees |
| SB-14 | [External reference](https://www.f95.de/uploads/tx_clubmanagement/magazine/FA_871_1._FC_Heidenheim.pdf) | Index only; agrees |
| SB-15 | [External reference](https://www.skysports.com/football/sv-wehen-wiesbaden-vs-sandhausen/teams/413290) | Full page; agrees |
| SB-16 | [External reference](https://www.hsv.de/en/news/match-report-hamburger-sv-fortuna-duesseldorf) | Full page; agrees |
| SB-17 | [External reference](https://www.ndr.de/sport/ergebnisse/Spielstatistik-Erzgebirge-Aue-SC-Paderborn-07%2Cspielstatistik2780.html) | Full page; agrees |
| SB-18 | [External reference](https://datencenter.dfb.de/mannschaftsvergleich/fc-st-pauli/sv-darmstadt-98) | Full page; agrees |
| SB-19 | [External reference](https://www.bundesliga.com/de/2bundesliga/news/1-fc-magdeburg-1-fc-nurnberg-spieltag-21-spielbericht-highlights-30842) | Full page; agrees |
| SB-20 | [External reference](https://www.bundesliga.com/de/2bundesliga/news/1-fc-kaiserslautern-fortuna-duesseldorf-spieltag-28-spielbericht-highlights-36729) | Full page; agrees |
| SB-21 | [External reference](https://www.fcc-supporters.org/wiki/SpVgg_Unterhaching) | Full page; agrees |
| SB-22 | [External reference](https://www.kleeblatt-chronik.de/v3/saison/spiel_detail.php?id=14&saison=20012002&team=1) | Full page; agrees |
| SB-23 | [External reference](https://www.alemannia-aachen.de/profis/spielinfo/2-Bundesliga-Alemannia-Aachen-gegen-SV-Wehen-Wiesbaden-88658M/) | Full page; agrees |
| SB-24 | [External reference](https://datencenter.dfb.de/competitions/2-bundesliga/seasons/2011-2012/teams/energie-cottbus) | Full page; agrees |
| SB-25 | [External reference](https://www.fussballtransfers.com/spiel/7298032823517602585-hamburger-sv-vs-fc-schalke-04) | Index only; agrees |
| SB-26 | [External reference](https://datencenter.dfb.de/competitions/2-bundesliga/seasons/2015-2016/teams/msv-duisburg) | Full page; agrees |

The full row-level comparison table, dates, club-name mappings and source-row bindings remain exclusively in the private verification evidence; they are not reproduced in this public report.

Publication independence is stronger than comparing the two downloaded CSV compilations, but **independent generation is not proved**. Official club narratives, DFB/league archives, NDR, Sky and historical fan archives are different publications; older engsoccerdata row lineage is incomplete, commercial feeds may overlap, and fan histories/chronicles may copy another archive. No agreement with the Kicker-derived supplementary CSV was counted as an independent sample comparison. SB-21 uses a fan-maintained Jena archive and SB-09/SB-22 a club history chronicle; these carry less authority than DFB or contemporary club reporting. SB-24 additionally agrees with the [contemporary Tagesspiegel report](https://www.tagesspiegel.de/sport/energie-cottbus-schlagt-dynamo-dresden-21-6438466.html); DFB establishes classification. SB-13's pre-match article has an updated result widget: the match date, not publication date, was compared.

Access limitations: SB-05's museum full page returned HTTP 502; SB-06 and SB-10 returned reader cache misses; SB-14's indexed Fortuna PDF URL returned HTTP 404; SB-25 was retained as indexed evidence only. Failed alternate DFB team URLs/timeouts and reader cache misses were not treated as successful checks or proof of a general site-wide denial. No restrictions were bypassed and no archive crawl was conducted.

### The 1991/92 format

SB-02 verifies the North first-phase fixture; SB-03 verifies Darmstadt–Halle in **South Abstieg**, the six-team second-phase relegation *league group*, not an external promotion/relegation playoff. The DFB selectors explicitly distinguish North/South first phases and their promotion/relegation groups. The structural audit retains two 12-team regions (132 first-phase matches each), then four six-team groups (30 each): **264 + 120 = 384**. Teams play 32 fixtures each; 120 ordered pairings legitimately repeat across phases. All four second-phase group schedules pass the existing structural audit, but only these two phase-specific fixtures were externally sampled: we do not claim independent verification of all group memberships, every date or all 384 outcomes. No ordinary whole-league 24-team pairing rule was applied.

### Burghausen–1860: resolved evidence, pending derived correction

The [official DFB 2005/06 Burghausen schedule](https://datencenter.dfb.de/competitions/2-bundesliga/seasons/2005-2006/teams/sv-wacker-burghausen) explicitly records **29 March 2006, SV Wacker Burghausen 1–0 TSV 1860 München** in 2. Bundesliga. This confirms the replay outcome. The supplied [Veilchen page](https://www.veilchenpower.de/2.bundesliga_2005_06/round025_Ergebnisse_und_Tabelle%2825__Spieltag%29.php) was unavailable to the reader (cache miss) and is not claimed as corroboration. The original court decision was not retrieved; the annulled original is separately supported by the documented supplementary flag and prior contemporary-club discussion, not credited as independent sample proof.

`verification/verified_corrections.json` contains one **VERIFIED_PENDING_STANDARDIZATION**, `applied=false` correction. It binds the original CSV SHA-256 `e955aef5dabb62909d584ae3ba77c994078d031976b52241aebff190bf67d931`, its physical row **26879** and all nine original fields. Only a future derived dataset may replace `Date=2005-11-04` with `2006-03-29`, `FT=0-2` with `1-0`, `hgoal=0` with `1`, and `vgoal=2` with `0`. Season, clubs, tier and division remain unchanged. Reject application if checksum, row or any expected original field differs. This replaces the annulled outcome within the same fixture slot; it neither adds a 307th fixture nor discards the original event history. **Nothing has been applied to source or derived match data in this stage.**

### Exception policy and decisions

Apply the same conservative archive-versus-training distinction as the Bundesliga review. Preserve recognized historical outcomes in future archive data and record played/annulled/abandoned events and supporting decisions separately. Match IDs do not exist yet: the private policy is source-row/checksum linked and must be linked to deterministic IDs during a later standardization stage. It remains non-exhaustive.

| Case | Classification | Official outcome / original event | Ordinary 90-minute training |
|---|---|---|---|
| Uerdingen–Bochum 1993/94 | Completed replay | 1994-05-31 3–0; annulled 1994-05-09 3–1 | Exclude conservatively |
| Aachen–Nürnberg 2003/04 | Completed replay | 2004-01-26 3–2; annulled 2003-11-24 1–0 | Exclude conservatively |
| Ahlen–Burghausen 2004/05 | Completed replay after annulment | 2005-04-27 1–3; annulled 2004-10-22 1–0 | Exclude conservatively |
| Erfurt–Unterhaching 2004/05 | Completed, then administratively awarded | Official 0–2 on 2005-04-06; played 2–0, doping decision | Exclude: award is not on-field 1/X/2 |
| Burghausen–1860 2005/06 | Completed replay; guarded correction pending | 2006-03-29 1–0; annulled 2005-11-04 0–2 | Exclude conservatively |
| Heidenheim–Aue 2017/18 | Completed replay after abandonment | 2017-08-09 2–1; 2017-07-30 stopped at 0–0, minute 12, weather | Exclude conservatively |
| Darmstadt–Kaiserslautern 2017/18 | Completed replay after abandonment | 2018-02-21 1–2; 2018-01-24 stopped at 0–0, halftime, medical emergency | Exclude conservatively |
| Unterhaching–Saarbrücken 2004/05 | Reported manipulation concern; result retained | Source 1–3 retained; not reclassified as an award | Exclude provisionally; ruling-level evidence incomplete |
| Karlsruhe–Duisburg 2004/05 | Reported manipulation concern; result retained | Source 0–3 retained; not reclassified as an award | Exclude provisionally; ruling-level evidence incomplete |

Thus nine known fixture exceptions comprise **six completed replays (two following abandonment), one administrative award and two reported manipulation concerns with results retained**. All nine are conservatively excluded. Replay exclusion is an intentional cautious policy, not a claim that every replay lacked 90 completed minutes. Abandoned 0–0 states are not full-time draws. The previous section's source URLs remain the evidence register. In this review, Uerdingen/Aachen club pages, WELT's doping retrospective and FCK's abandonment announcement were accessible; RSSSF returned a reader cache miss, the Aue PDF exceeded the reader's content-size limit, and the Darmstadt archive returned a cache miss. These latter details retain prior documentary/indexed support, not newly retrieved full-page proof. Primary tribunal documents and complete match-status certification remain unavailable. Secondary scandal summaries justify precautionary flags, not claims of proven score alteration for every reported concern.

The two Essen contexts (1990/91 and 1993/94) are **team licence/standings sanctions**, not 76 match awards. All 38 played fixture records in each season remain intact. The club retrospective supports the 1994 licence event; precise table treatment relies on the earlier historical synopsis and still needs primary decision evidence. Do not zero opponents' scores, delete Essen fixtures or infer automatic training exclusion solely from table treatment. Individual eligibility remains unresolved without separate evidence.

`verification/exception_policy.json` separates official fields from original on-field events, preserves source bindings and evidence, and records exclusion reasons. Its default for every unlisted fixture is **UNRESOLVED**, not “eligible”: structural validation and a small sample do not certify all unflagged matches for training.

### Integrity, reproduction and current readiness

The new read-only checker reuses the existing structural build and immutable original receipts. It verifies all pre-review protected fingerprints, exact sample selections and source facts, calendar-decade quotas, team mappings, guarded correction scope and nine source-bound exception records. It validates recorded evidence consistency; it does not automate external truth verification or silently fetch changing pages.

```sh
PYTHONPATH=src .venv/bin/python -m scripts.validate_second_bundesliga --check
PYTHONPATH=src .venv/bin/python -m scripts.verify_second_bundesliga_review
PYTHONPATH=src .venv/bin/python -m pytest -q
```

The pre-review snapshot covers **333 protected files**, including all four original exports, all earlier second-tier extracts/audits/checksums, England and Bundesliga artifacts, DFB experiments and existing Python source/tests. All remain byte-identical. All **11,488 source records**, 36 seasons and expected phase-aware fixture coverage are retained. The four original SHA-256 values in the earlier table are unchanged. New review artifacts are confined to the ignored `verification/` subdirectory; its separate `checksums.json` seals the new review without replacing the acquisition checksum manifest. No private file is tracked or staged.

**Current readiness:** all 36 seasons are technically ready for a future standardization stage that applies the single guarded replay correction and carries the exception policy separately. The raw 2005/06 source still intentionally contains the annulled original; the earlier REVIEW status is an immutable raw-source finding, not an unresolved proposed final outcome. Independent verification is sample-based and publication-level; detailed rulings, complete exception discovery and blanket training eligibility remain unresolved. Licensing limitations above remain fully applicable: compiler licences do not clear upstream rights, including non-commercial/GPL ambiguity and OpenLigaDB-related obligations. Legal clearance and explicit eligibility review are still needed before any intended model use or redistribution. No standardization, integration, source editing, commit or push was performed.

Final review validation: **448 tests passed** (435 existing plus 13 new synthetic review guards). Read-only structural reconstruction and review integrity checks passed; `git diff --check` passed. No tracked private files were found.

## Standardization — 2026-11-05

**11,488 historical matches across 36 completed seasons have been standardized locally**, using league `2. Bundesliga`, seasons `YYYY/YYYY`, and exactly `match_id,date,league,season,home_team,away_team,home_goals,away_goals`. No ongoing 2026/27 matches are included. Original team labels remain unchanged.

The adapter `scripts/standardize_second_bundesliga_results.py` reuses the existing second-tier source audit, checksum-bound correction checker, shared England/Bundesliga conversion utilities, historical importer/ID generation, serializer and public historical loader. No shared importer, predictor, application or DFB code was modified.

### Private standardized outputs

All outputs are exclusively under Git-ignored `data/private/germany/second_bundesliga/`:

| Filename | SHA-256 |
|---|---|
| `second_bundesliga_standardized_1990_2025.csv` | `02ce666a330a6afe6791facc22b627037eaaaaf40a22cb44a5456145c16dc354` |
| `second_bundesliga_exceptions_1990_2025.json` | `b861a2034820b1a8132ab59ed9bc2e64d810cab33dc2e8ac0c09548f3eba2168` |
| `second_bundesliga_standardization_manifest.json` | `fdea94257ae953ea679e6da63e5cc494c475bfd4eba94527ea7a5e84252630a0` |

The CSV contains all 11,488 fixtures in the exact eight-column schema. The exception JSON contains nine unique match-ID-linked cases: four completed replays after annulment, two completed replays after abandonment, one administrative award and two reported manipulation concerns. The latter retain `UNRESOLVED_CONCERN` evidence status, distinct from documented exceptional outcomes. Official archived dates/scores, original on-field events (including provisional abandoned scores), supporting sources, exact source bindings, exclusion reasons and conservative exclusion flags are retained. The two Essen licence/standings contexts are separate `team_level_contexts`, not additional fixture exceptions. All unlisted matches retain **UNRESOLVED** training suitability.

The provenance manifest embeds original acquisition provenance and licensing limitations, SHA-256/size of all sealed inputs, relevant code fingerprints, season-level validation, importer summaries, one applied derivative correction and source-row-to-match-ID lineage. Source region/division, phase and available matchday annotations remain in this manifest rather than expanding the eight-column schema. Original raw evidence remains immutable and still records the unapplied proposal; the derivative manifest truthfully records its application.

### Replay correction and historical fixture identity

Exactly one correction was applied in the standardized derivative: Wacker Burghausen–1860 München changed from **2005-11-04, 0–2** to **2006-03-29, 1–0**. The correction requires the unchanged original SHA-256, physical source row, all nine expected fields, verified pending status and evidence. Only date, FT and numeric goal fields change in the adapter; the standard CSV carries the corrected date and goals. No original CSV, source-schema extract, earlier audit or evidence was rewritten. The annulled original event remains in separate exception metadata, not as an additional fixture.

Stable IDs come from the existing importer: SHA-256 of the compact JSON identity `[league,season,date,home_team,away_team]`. Goals, file paths and row ordering do not affect identity. For 1991/92, different actual dates distinguish legitimate repeated ordered pairings across phases. The shared converter's conventional pairing guard is satisfied by converting the documented first and second phases in separate batches, then recombining without changing league/season identifiers. Full combined validation retains the two regions and four second-phase groups: **264 first-phase plus 120 second-phase fixtures**, 24 teams and 384 matches. No legitimate repeats were deduplicated; true repeated dated instances are rejected. Other seasons retain ordinary season-specific home/away completeness, including the 20- and 24-team formats.

### Reproduction and verification

```sh
# Create new private artifacts; refuses any existing output.
PYTHONPATH=src .venv/bin/python -m scripts.standardize_second_bundesliga_results
# Rebuild from immutable originals and evidence; compare all outputs without writing.
PYTHONPATH=src .venv/bin/python -m scripts.standardize_second_bundesliga_results --check
PYTHONPATH=src .venv/bin/python -m pytest -q
```

Validation checks exact counts and columns, required values, deterministic unique IDs, dated fixture uniqueness, phase-aware schedule completeness, single guarded correction, preservation of all other match facts, nine exception links and official outcomes, and unresolved unreviewed eligibility. The public historical loader validates the complete combined CSV. Reversed input order produces identical CSV bytes; the read-only command also reconstructs all three outputs byte-for-byte. No default validation gates were relaxed.

New synthetic tests cover all 384 phase fixtures and their 120 legitimate repeated ordered pairings, reversed-order deterministic IDs/bytes, true duplicate rejection, correction-only changes with source guards, nine exception links and the distinction between unresolved concerns, standings contexts and unreviewed eligibility. All 333 pre-review protected file fingerprints remain unchanged, including all original sources and earlier England/Bundesliga/DFB work. Private files remain ignored and untracked.

**Readiness:** technically ready for future integration as an archive with the linked exception policy. This is not authorization for training, evaluation, model integration or publication. Upstream rights remain unresolved: engsoccerdata's noncommercial/attribution terms and GPL scope ambiguity, and OpenFootball/OpenLigaDB upstream obligations, are preserved. The independent review remains sample-based; complete tribunal evidence, exhaustive exception discovery and blanket training eligibility are not established. No training, evaluation, integration, commit or push occurred.

Final standardization test run: **455 passed** across the complete suite, including seven new synthetic adapter tests. The integrity comparison confirms 333 protected files unchanged, all originals retaining their previous checksums, and no tracked private files. `git diff --check` passes.
