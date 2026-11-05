# Bundesliga CSV acquisition and structural validation

Reviewed 2026-11-05. Scope: 36 completed Bundesliga regular seasons, 1990/91–2025/26. Ongoing 2026/27 is excluded. This report records acquisition, structural validation, targeted external verification and local standardization. It does not certify every historical result or authorize model use. Earlier-stage snapshots below are retained with their original scope; the final standardization section records the current state.

## Outcome

**36 original season CSVs acquired, 11,090 match records, no missing season files or home-away fixtures.** Twenty-nine season files were newly downloaded; seven original cached files were reused with their original retrieval evidence. All originals are retained unchanged under Git-ignored `data/private/germany/csv_history/originals/`.

**Acquisition-stage snapshot: 35 seasons passed (31 PASS, four PASS_WITH_NOTES), with 1993/94 initially REVIEW. The subsequent review resolves its date discrepancy through a separately recorded, unapplied correction. All 36 seasons are technically ready for future standardization subject to that correction and exception metadata.** All 36 have the expected team/count/pair coverage and valid required-field/full-score structure. The lower-level audit separately retains one halftime/fulltime inconsistency in 1992/93; official evidence explains it as an administrative award rather than an ordinary played final. No warning or original source value was deleted.

## Selected sources and immutable provenance

- **D, 1990/91–1992/93:** [deadangel33/de-deutschland](https://github.com/deadangel33/de-deutschland), fork of footballcsv/deutschland, commit `f64e042d22d2f2a9887c8336125d748ef93269bc`. Direct raw paths are `1990s/YYYY-YY/1-bundesliga.csv` at that commit. Three original UTF-8 CSVs were reused byte-for-byte from the earlier source study.
- **H, 1993/94–2025/26:** [DataHub german-bundesliga](https://datahub.io/football/german-bundesliga). The freshly retrieved [resource manifest](https://datahub.io/football/german-bundesliga/_r/-/datapackage.json) lists all 33 required resources. URLs are the advertised `https://datahub.io/football/german-bundesliga/_r/-/season-YYZZ.csv` downloads, redirected normally to the publisher’s R2 storage. Four cached original CSVs were reused; 29 were downloaded. DataHub does not expose a Git commit/version for this snapshot; response ETags, exact final URLs, timestamps, package checksum and content SHA-256 fingerprints pin the privately retained bytes.

`acquisition.json` records **every file’s** requested/final URL, original UTC retrieval timestamp, HTTP status/headers, source commit (where available), SHA-256, byte size, source kind and whether/from where it was reused. Reuse does not fabricate a new retrieval date or a network download. Files use private names `originals/early/bundesliga_YYYY-YYYY.csv` and `originals/datahub/bundesliga_YYYY-YYYY.csv`; their bytes are identical to the downloaded inputs.

DataHub package SHA-256: `a31946f923ec0c0a89ba9155de6795332ca8ce6e6f1a254a3a2912d5e462dcb6`. All 36 complete file checksums are in the private acquisition manifest; `checksums.json` inventories acquisition, audit, review and source artifacts. Original-source licences/declarations are retained in `metadata/`.

No missing, inaccessible or substituted resource was encountered. New dataset requests were sequential with at least five seconds between request starts, without authentication, challenge handling or bypass. There were no HTTP access denials or rate-limit responses. No DFB matchday requests or collector executions occurred. Only bounded documentary research into exceptional results used official/public source references.

## Historical format and validation method

The [official Bundesliga format history](https://www.bundesliga.com/en/faq/10-things-on-the-bundesliga) confirms the one-off 20-team 1991/92 competition following reunification. The audit expects 380 matches and 38 games per club (19 home/19 away) for that season; other selected seasons use 18 teams, 306 matches and 34 games per club (17/17). Thus 35 × 306 + 380 = **11,090** expected regular-season matches. No format/count discrepancy was found. The separate East German competition, relegation playoffs, cups and lower divisions were not selected.

`scripts/validate_bundesliga_csv.py` reuses `canonical_season`, `exact_integer`, `team_name`, `outcome_from_goals` and `validate_historical_data`. It validates checksums and season-specific source URL/filename scope; unique/required CSV headers and row widths; required names/dates/full scores; nonnegative integer goals; season calendar years/future dates; FTR/goals consistency; duplicate dated fixtures and repeated ordered pairs; complete home-away pair coverage; and per-club home/away totals. Optional halftime fields are checked when present. Source files are never rewritten.

The early schema has `Round, Date, Team 1, FT, HT, Team 2`; dates and teams carry documented weekday/week/game-count annotations. These syntactic annotations are parsed only in memory for checks, with no team alias mapping or persisted converted match dataset. The three early seasons also pass round-count and per-round fixture-count checks. DataHub has ISO dates, HomeTeam/AwayTeam/FTHG/FTAG/FTR and optional statistics, decoded with its declared ISO-8859-1 encoding. DataHub has no round/status field, so round assignment and finished/abandoned status cannot be independently inferred from those CSVs. No eight-column TOTOdology standardization or match IDs were generated.

Empty optional referee/statistics/halftime fields are counted privately rather than filled with zero. There are **no missing required dates, teams or full scores, no duplicate fixtures, no absent ordered pairs, no full-score/FTR mismatches and no home/away balance failures** in the 36 selected files. Earlier files have no independent Result column; their FT score is the source from which goals are read, so independent score/result agreement is not claimed for that schema. Calendar validity alone does not establish that each date is historically correct.

## Season-by-season results

PASS means the checks at this stage passed; NOTES identifies an evidenced administrative outcome. Neither means every match was independently verified. READY_WITH_CORRECTION means documentary resolution is recorded but the original erroneous date remains unchanged; future conversion must apply the guarded correction.

| Season | Source | Teams / expected | Matches / expected | First source date | Last source date | Status | Issues / notes |
|---|---|---:|---:|---|---|---|---|
| 1990/1991 | D | 18 / 18 | 306 / 306 | 1990-08-08 | 1991-06-15 | PASS | none detected |
| 1991/1992 | D | 20 / 20 | 380 / 380 | 1991-08-02 | 1992-05-16 | PASS | none detected |
| 1992/1993 | D | 18 / 18 | 306 / 306 | 1992-08-14 | 1993-06-05 | PASS_WITH_NOTES | E1: official award; played HT retained |
| 1993/1994 | H | 18 / 18 | 306 / 306 | 1993-08-07 | 1994-05-07 | READY_WITH_CORRECTION | E2: verified 1994-05-03; separate pending correction |
| 1994/1995 | H | 18 / 18 | 306 / 306 | 1994-08-19 | 1995-06-17 | PASS | none detected |
| 1995/1996 | H | 18 / 18 | 306 / 306 | 1995-08-11 | 1996-05-18 | PASS | none detected |
| 1996/1997 | H | 18 / 18 | 306 / 306 | 1996-08-16 | 1997-05-31 | PASS | none detected |
| 1997/1998 | H | 18 / 18 | 306 / 306 | 1997-08-01 | 1998-05-09 | PASS | none detected |
| 1998/1999 | H | 18 / 18 | 306 / 306 | 1998-08-14 | 1999-05-29 | PASS | none detected |
| 1999/2000 | H | 18 / 18 | 306 / 306 | 1999-08-13 | 2000-05-20 | PASS | none detected |
| 2000/2001 | H | 18 / 18 | 306 / 306 | 2000-08-11 | 2001-05-19 | PASS | none detected |
| 2001/2002 | H | 18 / 18 | 306 / 306 | 2001-07-28 | 2002-05-04 | PASS | none detected |
| 2002/2003 | H | 18 / 18 | 306 / 306 | 2002-08-09 | 2003-05-24 | PASS | none detected |
| 2003/2004 | H | 18 / 18 | 306 / 306 | 2003-08-01 | 2004-05-22 | PASS | none detected |
| 2004/2005 | H | 18 / 18 | 306 / 306 | 2004-08-06 | 2005-05-21 | PASS | none detected |
| 2005/2006 | H | 18 / 18 | 306 / 306 | 2005-08-05 | 2006-05-13 | PASS | none detected |
| 2006/2007 | H | 18 / 18 | 306 / 306 | 2006-08-11 | 2007-05-19 | PASS | none detected |
| 2007/2008 | H | 18 / 18 | 306 / 306 | 2007-08-10 | 2008-05-17 | PASS | none detected |
| 2008/2009 | H | 18 / 18 | 306 / 306 | 2008-08-15 | 2009-05-23 | PASS | none detected |
| 2009/2010 | H | 18 / 18 | 306 / 306 | 2009-08-07 | 2010-05-08 | PASS | none detected |
| 2010/2011 | H | 18 / 18 | 306 / 306 | 2010-08-20 | 2011-05-14 | PASS_WITH_NOTES | E3: abandoned/awarded match |
| 2011/2012 | H | 18 / 18 | 306 / 306 | 2011-08-05 | 2012-05-05 | PASS | none detected |
| 2012/2013 | H | 18 / 18 | 306 / 306 | 2012-08-24 | 2013-05-18 | PASS | none detected |
| 2013/2014 | H | 18 / 18 | 306 / 306 | 2013-08-09 | 2014-05-10 | PASS | none detected |
| 2014/2015 | H | 18 / 18 | 306 / 306 | 2014-08-22 | 2015-05-23 | PASS | none detected |
| 2015/2016 | H | 18 / 18 | 306 / 306 | 2015-08-14 | 2016-05-14 | PASS | none detected |
| 2016/2017 | H | 18 / 18 | 306 / 306 | 2016-08-26 | 2017-05-20 | PASS | none detected |
| 2017/2018 | H | 18 / 18 | 306 / 306 | 2017-08-18 | 2018-05-12 | PASS | none detected |
| 2018/2019 | H | 18 / 18 | 306 / 306 | 2018-08-24 | 2019-05-18 | PASS | none detected |
| 2019/2020 | H | 18 / 18 | 306 / 306 | 2019-08-16 | 2020-06-27 | PASS | none detected |
| 2020/2021 | H | 18 / 18 | 306 / 306 | 2020-09-18 | 2021-05-22 | PASS | none detected |
| 2021/2022 | H | 18 / 18 | 306 / 306 | 2021-08-13 | 2022-05-14 | PASS_WITH_NOTES | E4: abandoned/awarded match |
| 2022/2023 | H | 18 / 18 | 306 / 306 | 2022-08-05 | 2023-05-27 | PASS | none detected |
| 2023/2024 | H | 18 / 18 | 306 / 306 | 2023-08-18 | 2024-05-18 | PASS | none detected |
| 2024/2025 | H | 18 / 18 | 306 / 306 | 2024-08-23 | 2025-05-17 | PASS_WITH_NOTES | E5: official award differs from played score |
| 2025/2026 | H | 18 / 18 | 306 / 306 | 2025-08-22 | 2026-05-16 | PASS | none detected |

## Exceptional results and unresolved data quality

- **E1 — 1992/93, 22 May 1993, Uerdingen–Frankfurt (source row 284):** original FT `2-0`, HT `1-3`. [Eintracht’s official history](https://profis.eintracht.de/news/yeboahs-spannendes-rennen-um-die-torjaegerkanone-151022/) explains that the on-field 2–5 was awarded 2–0 to Uerdingen after an ineligible fourth foreign player entered. The halftime score belongs to play; the FT field contains the official award. The raw audit warning is retained and explained, with no correction to either value. Source label `KFC Uerdingen` is retained even though the contemporary club name differed.

- **E2 — 1993/94, Bayern Munich–Nurnberg (source row 254):** DataHub records `1994-04-03`, `5-0`. [Bundesliga’s account](https://www.bundesliga.com/en/bundesliga/news/bizarre-ghost-goals-bayern-munich-bayer-leverkusen-kiessling-24771) identifies 5–0 as the replay; [Bayern’s history](https://fcbayern.com/museum/de/news/2013/04/die-historische-woche-vom-22.-bis-28.-april) dates the original phantom-goal match to 23 April, so a 3 April replay is chronologically inconsistent. The [broadcast results archive](https://www.sportschau.de/live-und-ergebnisse/fussball/deutschland-bundesliga/ma179072/bayern-muenchen_1-fc-nuernberg/taktische-aufstellung) dates the replay to **3 May 1994**. The source date has **not** been changed. The discrepancy is now resolved by the additional official DFB and Sportschau references below; a guarded correction is recorded separately for future standardization. This does not establish the accuracy of every other source date. The file has exactly one ordered fixture for this pairing, not an extra replay duplicate.

- **E3 — 2010/11, 1 April 2011, St Pauli–Schalke:** stored `0-2`. The game was abandoned while Schalke led; see [UEFA’s contemporary account](https://de.uefa.com/news-media/news/01f0-0f8626904786-4709edc4dc66-1000--entscheidung-am-grunen-tisch/) and the [result archive’s awarded-result notation](https://www.skysports.com/football/st-pauli-vs-schalke/teams/233512). Do not interpret this as a normal completed 90-minute match.

- **E4 — 2021/22, 18 March 2022, Bochum–Mönchengladbach:** stored `0-2`. The [official sporting-court decision of 24 March](https://www.dfb.de/fileadmin/_dfbdam/257416-220324_VfL_Bochum.pdf) awards this result following abandonment. The court text was identified through indexed documentary research, not a Datencenter collection run.

- **E5 — 2024/25, 14 December 2024, Union Berlin–Bochum:** stored `0-2`, optional halftime/statistics empty. The [official Bundesliga record](https://www.bundesliga.com/en/bundesliga/matchday/2024-2025/14/1-fc-union-berlin-vs-vfl-bochum-1848/news) distinguishes the original 1–1 from the later 0–2 award. Empty optional fields are preserved.

`known_exceptions.json` records source row numbers, unchanged source values, explanations and evidence URLs. `validation.json` retains the lower-level warnings and the reviewed interpretation separately; it does not erase the halftime warning or rewrite the replay date. This targeted exception register is **not exhaustive**. CSVs lack comprehensive status metadata, so absence of a flag cannot prove that every other fixture finished normally. The following stage supplies a reproducible cross-era sample and reviews these five exceptions; it does not exhaustively certify every date or match status.

## Access conditions and unresolved rights

GitHub’s [service terms](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service) and DataHub’s [service terms](https://docs.datahub.io/terms-of-service) govern platform access. DataHub explicitly advertises direct script/API dataset downloads. Normal public dataset routes were used; no access controls or rate limits were bypassed.

The pinned early repository declares **CC0 1.0**; its source list names an open-sport forum and Football-Data without a season/row-level rights chain. CC0 covers the affirmer’s rights and disclaims third-party clearance. DataHub declares **ODC-PDDL-1.0** and credits Football-Data. The [PDDL](https://opendatacommons.org/licenses/pddl/1-0/) can only dedicate rights the publisher holds. [Football-Data notes](https://football-data.co.uk/notes.txt) credit XScores for current results and other providers for statistics, while its website reserves rights. No complete upstream sublicense chain was established.

These uncertainties did not block the advertised private dataset downloads, but **publisher public-domain labels are not blanket upstream clearance**. Preserve the saved notices and clarify intended model/application use and any redistribution with the relevant rights holders. No commercial-use permission or redistribution clearance is claimed; the data remains private. No OpenFootball/ODbL data was substituted. `access_review.json` records the reviewed terms and limitations.

## Artifacts, tests and reproduction

**Full test suite: 389 passed.** The five new CSV audit tests passed individually; the full suite also confirms no regressions in the existing infrastructure. Cached acquisition/diagnostic reruns reproduced the saved results without new dataset requests. Fingerprints confirmed all 153 protected prior Germany/DFB files and 15 England source/extracted/standardized artifacts unchanged.

- `scripts/acquire_bundesliga_csv.py`: fixed 36-resource acquisition with manifest checkpoints, five-second request pacing, checksum-verified resume/cache reuse, raw-byte preservation and stop-on-error behavior. No DFB downloader is invoked.
- `scripts/validate_bundesliga_csv.py`: read-only audit; creates/reproduces the private `structural_validation.json` and refuses differing outputs.
- Private `build_report.py`: builds the reviewed `validation.json` and `known_exceptions.json` from the unchanged lower-level audit and explicitly recorded documentary evidence.
- `tests/test_bundesliga_csv.py`: synthetic 18-/20-team schedules, source annotation parsing, score/result mismatch, missing required fields, wrong season dates, duplicates/missing pairings and halftime-review regressions.

```sh
PYTHONPATH=src .venv/bin/python -m scripts.acquire_bundesliga_csv
PYTHONPATH=src .venv/bin/python -m scripts.validate_bundesliga_csv
python3 data/private/germany/csv_history/build_report.py
```

Acquisition reruns use all 36 checksummed cached originals and make no new dataset requests when the manifest is complete. Diagnostics reproduce byte-for-byte. Originals and earlier England/DFB files are never overwritten. No standardized Bundesliga match dataset, training/evaluation run, prediction/Streamlit change, publication, commit or push was performed.

## Targeted independent verification and anomaly resolution — 2026-11-05

### Replay correction (E2)

The [official DFB Bayern 1993/94 archive](https://datencenter.dfb.de/competitions/bundesliga/seasons/1993-1994/teams/bayern-muenchen) explicitly records **3 May 1994, Bayern München 5–0 1. FC Nürnberg**. [Sportschau’s May 1994 historical feature](https://www.sportschau.de/tor-des-monats/archiv/chronik90er/mai1994tdm-sp-100.html) independently identifies the same replay date and score. The original 23 April 2–1 phantom-goal match was annulled; it is not a second valid regular-season fixture.

Private `verification/verified_corrections.json` records `BL-DATE-1993-94-REPLAY`: source row 254, `Date` **1994-04-03 → 1994-05-03**, with source SHA-256 `7bc8f2a97e0be1278be69a33c739007ae039e74efa5d4aa6c02aefa828f0dbce`, expected teams/score/result, references and justification. **Applied: false in this immutable review-stage evidence.** The subsequent standardization stage below applies it only to the derivative. Standardization must verify the source hash, row and all expected fields before applying this one-field correction to a derivative. No source CSV or score was changed.

### Archive and future training policy

Preserve official historical outcomes for archive/validation, together with their evidence. Record on-field results separately from court decisions. Do not silently change, delete, substitute or filter fixtures. Exception status, played scores, administrative decisions, eligibility and correction IDs remain in a separate sidecar outside the eight-column match schema; bind them to source SHA-256/row and later to match IDs.

| Case | Classification | On-field result | Official archive outcome | Ordinary 90-minute 1/X/2 training |
|---|---|---|---|---|
| E1, 1992/93 Uerdingen–Frankfurt | Completed, subsequently awarded | 2–5; HT 1–3 | 2–0 | Exclude |
| E2, 1993/94 Bayern–Nürnberg | Annulled original; completed replay | Original 2–1 annulled; replay 5–0 on 3 May | Replay 5–0 only | Exclude by default; future explicit replay policy required |
| E3, 2010/11 St Pauli–Schalke | Abandoned, subsequently awarded | 0–2 when abandoned, not a completed final | 0–2 | Exclude |
| E4, 2021/22 Bochum–Gladbach | Abandoned, subsequently awarded | 0–2 when abandoned in minute 69 | 0–2 | Exclude |
| E5, 2024/25 Union–Bochum | Interrupted, resumed/completed, subsequently awarded | 1–1 | 0–2 | Exclude |

Normal completed matches can be eligible under a future modelling policy. Unflagged CSV records are not automatically certified normal: the exception register is targeted, not exhaustive. No training selection is implemented here.

E3’s [UEFA report](https://de.uefa.com/news-media/news/01f0-0f8626904786-4709edc4dc66-1000--entscheidung-am-grunen-tisch/) predates the ruling and proves abandonment, not the later award. The [contemporary 5 April court-decision report](https://www.n-tv.de/sport/fussball/Schalker-gewinnen-mit-2-0-article3027141.html) reports the 0–2 award; the original court document was not obtained. E4’s [DFB court PDF](https://www.dfb.de/fileadmin/_dfbdam/257416-220324_VfL_Bochum.pdf) was accessible and directly states abandonment and the award. E5’s [Bundesliga chronology](https://www.bundesliga.com/en/bundesliga/matchday/2024-2025/14/1-fc-union-berlin-vs-vfl-bochum-1848/news) distinguishes the played 1–1 from the subsequent award, including confirmation in April 2025. It must not be classified simply as an abandoned game. The E1 club history above directly explains its changed outcome. Private `verification/exception_policy.json` binds all five cases to unchanged source rows and records this policy. The earlier `known_exceptions.json` and `validation.json` remain acquisition-stage snapshots, superseded in interpretation by this review rather than overwritten.

### Reproducible sample

The initial selection was fixed before reference checks: five seasons per decade, using CSV data-row offsets 0, 61, 122, 183 and 244 in each decade (physical CSV rows 2, 63, 124, 185 and 246). Season starts: 1990/1991/1994/1996/1998; 2000/2002/2004/2006/2008; 2010/2012/2014/2016/2018; 2020/2021/2022/2023/2025. Four direct-page retrievals failed, so four supplementary first-row checks against already cached official matchday HTML were added without replacing the initial selections. Each selection records source hash and row in `verification/sample_selection.json` or `supplementary_selection.json`.

**20 full-page/cached-official comparisons succeeded; four additional indexed-only corroborations are not counted toward those 20.** Every comparison covers date, home/away identity, full-time score and Bundesliga regular-season/top-tier classification, excluding cups and playoffs. No sampled date/score discrepancy was found. E2 is a separate anomaly check, not hidden in this zero-discrepancy sample count.

V = full-page or retained official HTML evidence; I = indexed corroboration only (direct fetch timeout/cache miss, not an observed server denial). Team labels below are source labels; reference-label differences are explicit in the last column and are not applied to data.

| ID / source row | Season | Date | Source fixture | Score | Evidence | Reference label differences |
|---|---|---|---|---|---|---|
| BL-01 / 2 | 1990/1991 | 1990-08-08 | Borussia Dortmund – VfB Stuttgart | 0–3 | [V](https://datencenter.dfb.de/de/competitions/bundesliga/seasons/1990-1991/matchday/1) | none |
| BL-02 / 63 | 1991/1992 | 1991-08-30 | Fortuna Düsseldorf – SG Wattenscheid 09 | 4–3 | [V](https://datencenter.dfb.de/competitions/bundesliga/seasons/1991-1992/teams/fortuna-duesseldorf) | none |
| BL-03 / 124 | 1994/1995 | 1994-11-19 | Karlsruhe – Bayern Munich | 2–2 | [V](https://datencenter.dfb.de/competitions/bundesliga/seasons/1994-1995/teams/karlsruher-sc?datacenter_name=datencenter%3Fhistorize_title%3DManfred+Binz+-+Spielerprofil&historize_url=) | home: Karlsruhe → Karlsruher SC; away: Bayern Munich → Bayern München |
| BL-04 / 185 | 1996/1997 | 1997-03-08 | M'gladbach – Werder Bremen | 4–1 | [I](https://datencenter.dfb.de/competitions/bundesliga/seasons/1996-1997/teams/borussia-moenchengladbach?datacenter_name=datencenter%3Fhistorize_title%3DKarlsruher+SC+-+Borussia+M%C3%B6nchengladbach%2C+1%3A1%2C+Bundesliga+1996%2F97+20.+Spieltag&historize_url=) | home: M'gladbach → Borussia Mönchengladbach |
| BL-05 / 246 | 1998/1999 | 1999-04-23 | Stuttgart – Leverkusen | 0–1 | [I](https://datencenter.dfb.de/en/competitions/bundesliga/seasons/1998-1999) | home: Stuttgart → VfB Stuttgart; away: Leverkusen → Bayer 04 Leverkusen |
| BL-06 / 2 | 2000/2001 | 2000-08-11 | Dortmund – Hansa Rostock | 1–0 | [V](https://datencenter.dfb.de/bundesliga/2000-2001/mannschaft/borussia-dortmund) | home: Dortmund → Borussia Dortmund |
| BL-07 / 63 | 2002/2003 | 2002-09-29 | Bochum – Werder Bremen | 1–4 | [V](https://datencenter.dfb.de/competitions/bundesliga/seasons/2002-2003/teams/vfl-bochum) | home: Bochum → VfL Bochum |
| BL-08 / 124 | 2004/2005 | 2004-11-20 | Mainz – Bochum | 1–0 | [V](https://datencenter.dfb.de/datencenter/bundesliga/2004-2005/14-spieltag/1-fsv-mainz-05-vfl-bochum-175653) | home: Mainz → 1. FSV Mainz 05; away: Bochum → VfL Bochum |
| BL-09 / 185 | 2006/2007 | 2007-02-10 | Mainz – Cottbus | 4–1 | [I](https://datencenter.dfb.de/competitions/bundesliga/seasons/2006-2007/teams/energie-cottbus?datacenter_name=datencenter%3Fhistorize_title%3DChristian+Lell+-+Spielerprofil&historize_url=) | home: Mainz → 1. FSV Mainz 05; away: Cottbus → Energie Cottbus |
| BL-10 / 246 | 2008/2009 | 2009-04-18 | Bielefeld – Bayern Munich | 0–1 | [V](https://datencenter.dfb.de/datencenter/bundesliga/2008-2009/28-spieltag/arminia-bielefeld-bayern-muenchen-10812) | home: Bielefeld → Arminia Bielefeld; away: Bayern Munich → Bayern München |
| BL-11 / 2 | 2010/2011 | 2010-08-20 | Bayern Munich – Wolfsburg | 2–1 | [V](https://datencenter.dfb.de/competitions/bundesliga/seasons/2010-2011/teams/vfl-wolfsburg?datacenter_name=datencenter) | home: Bayern Munich → Bayern München; away: Wolfsburg → VfL Wolfsburg |
| BL-12 / 63 | 2012/2013 | 2012-10-07 | M'gladbach – Ein Frankfurt | 2–0 | [V](https://datencenter.dfb.de/competitions/bundesliga/seasons/2012-2013/teams/borussia-moenchengladbach) | home: M'gladbach → Borussia Mönchengladbach; away: {'source': 'Ein Frankfurt', 'reference': 'Eintracht Frankfurt'} |
| BL-13 / 124 | 2014/2015 | 2014-12-06 | Paderborn – Freiburg | 1–1 | [V](https://datencenter.dfb.de/datencenter/bundesliga/2014-2015/14/sc-paderborn-07-sc-freiburg-2211163) | home: Paderborn → SC Paderborn 07; away: Freiburg → SC Freiburg |
| BL-14 / 185 | 2016/2017 | 2017-02-18 | Hamburg – Freiburg | 2–2 | [V](https://datencenter.dfb.de/datencenter/mannschaftsvergleich/hamburger-sv/sc-freiburg) | home: Hamburg → Hamburger SV; away: Freiburg → SC Freiburg |
| BL-15 / 246 | 2018/2019 | 2019-04-06 | Bayern Munich – Dortmund | 5–0 | [V](https://www.bundesliga.com/de/bundesliga/spieltag/2018-2019/28/fc-bayern-muenchen-vs-borussia-dortmund/liveticker) | home: Bayern Munich → Bayern München; away: Dortmund → Borussia Dortmund |
| BL-16 / 2 | 2020/2021 | 2020-09-18 | Bayern Munich – Schalke 04 | 8–0 | [V](https://fcbayern.com/de/news/spielberichte/2020/09/spielbericht-bundesliga-fc-bayern---fc-schalke-04) | home: Bayern Munich → FC Bayern München; away: Schalke 04 → FC Schalke 04 |
| BL-17 / 63 | 2021/2022 | 2021-10-03 | Bayern Munich – Ein Frankfurt | 1–2 | [V](https://datencenter.dfb.de/competitions/bundesliga/seasons/2021-22/teams/eintracht-frankfurt) | home: Bayern Munich → Bayern München; away: Ein Frankfurt → Eintracht Frankfurt |
| BL-18 / 124 | 2022/2023 | 2022-11-09 | Ein Frankfurt – Hoffenheim | 4–2 | [V](https://www.bundesliga.com/de/bundesliga/spieltag/2022-2023/14/eintracht-frankfurt-vs-tsg-hoffenheim/liveticker) | home: Ein Frankfurt → Eintracht Frankfurt; away: Hoffenheim → TSG Hoffenheim |
| BL-19 / 185 | 2023/2024 | 2024-02-10 | M'gladbach – Darmstadt | 0–0 | [I](https://datencenter.dfb.de/en/data-center/bundesliga/18805/21-matchday/2354256) | home: M'gladbach → Borussia Mönchengladbach; away: {'source': 'Darmstadt', 'reference': 'SV Darmstadt 98'} |
| BL-20 / 246 | 2025/2026 | 2026-04-04 | Hamburg – Augsburg | 1–1 | [V](https://www.bundesliga.com/de/bundesliga/news/hamburger-sv-fc-augsburg-spieltag-28-spielbericht-highlights-36739) | home: Hamburg → Hamburger SV; away: Augsburg → FC Augsburg |
| BL-21 / 2 | 1991/1992 | 1991-08-02 | MSV Duisburg – VfB Stuttgart | 1–0 | [V](https://datencenter.dfb.de/de/competitions/bundesliga/seasons/1991-1992/matchday/1) | none |
| BL-22 / 2 | 2005/2006 | 2005-08-05 | Bayern Munich – M'gladbach | 3–0 | [V](https://datencenter.dfb.de/de/competitions/bundesliga/seasons/2005-2006/matchday/1) | home: Bayern Munich → Bayern München; away: M'gladbach → Borussia Mönchengladbach |
| BL-23 / 2 | 2015/2016 | 2015-08-14 | Bayern Munich – Hamburg | 5–0 | [V](https://datencenter.dfb.de/de/competitions/bundesliga/seasons/2015-2016/matchday/1) | home: Bayern Munich → Bayern München; away: Hamburg → Hamburger SV |
| BL-24 / 2 | 2025/2026 | 2025-08-22 | Bayern Munich – RB Leipzig | 6–0 | [V](https://datencenter.dfb.de/de/competitions/bundesliga/seasons/2025-2026/matchday/1) | home: Bayern Munich → FC Bayern München |

DFB federation archives, the Bundesliga league archive and official club reports are authoritative publications separate from the CSV repositories. Their underlying commercial score feeds are not proven independent of every upstream dataset provider; this is publication-level external corroboration, not a guarantee of independent data generation. No mirror of the same CSV was counted. Cached HTML carries its original provenance/checksum; it was not represented as newly fetched. Some current reader results may themselves be cached. BL-15 additionally uses the [dated league Klassiker retrospective](https://www.bundesliga.com/de/bundesliga/news/der-klassiker-grosse-spiele-borussia-dortmund-bvb-fc-bayern-munchen-fcb-181); BL-18 uses the [dated matchday news listing](https://www.bundesliga.com/de/bundesliga/spieltag/2022-2023/14/eintracht-frankfurt-vs-tsg-hoffenheim/news) (indexed date evidence; direct news fetch unavailable) alongside its accessible match centre. These establish calendar dates where the match centre emphasizes matchday. Historical abbreviations, transliterations and modern club labels are identity equivalences only; no historical team names were rewritten. Sample verification cannot certify every match or detect every unknown administrative decision.

### Reproduction, integrity and readiness

`verification/independent_verification.json` retains the observed reference fields, source rows/hashes, label comparisons, access limitations and cached-evidence hashes. `record_evidence.py` reproduces these recorded observations; it does not re-fetch or independently discover them. Re-run the existing read-only structural audit and the new evidence/integrity check:

```sh
PYTHONPATH=src .venv/bin/python -m scripts.validate_bundesliga_csv
PYTHONPATH=src .venv/bin/python data/private/germany/csv_history/verification/check_review.py
```

Review-stage checks: **5 relevant CSV tests passed**, the read-only structural audit reproduced exactly, the evidence/integrity check passed, and `git diff --check` passed. Production code was unchanged; the previously reported 389-test full-suite run was not repeated unnecessarily. Private storage remains ignored and no private files are tracked.

The fresh audit confirms **36 complete fixture sets and 11,090 unchanged original records**, including 380 in the 20-team 1991/92 season and 306 in every other season. All original SHA-256 fingerprints still match acquisition provenance. The known halftime/administrative warning remains visible. Protected prior DFB/Germany experiments and England data are unchanged. No Bundesliga standardization or integration was performed during that review stage; the later standardization results follow below.

**Review-stage readiness:** all 36 seasons were technically ready for subsequent standardization with the guarded E2 date correction and separate exception metadata. This is not blanket 90-minute training eligibility or legal clearance. Upstream third-party rights remain unresolved as described above; clarify intended model/application use and redistribution rights before such use. No data were published, committed or pushed.

## Local standardization — 2026-11-05

**11,090 records across all 36 completed seasons (1990/1991–2025/2026) standardized successfully.** No 2026/2027 acquisition or merge was performed. All outputs below are exclusively under Git-ignored `data/private/germany/`; they are not application inputs and were not used for training or evaluation.

### Conversion and reproducibility

`scripts/standardize_bundesliga_results.py` reuses `scripts.validate_bundesliga_csv.audit_file(include_records=True)` for source parsing and structural validation. This optional return exposes the existing parser's records without changing the default audit/report bytes. The converter supplies explicit Bundesliga competition metadata to the shared `scripts.standardize_england_results.convert_rows`, which delegates IDs, sorting, import validation and public-loader checks to the existing historical infrastructure. There is no second importer or ID algorithm. Premier League and Championship converters/data remain unchanged.

The exact output columns are `match_id,date,league,season,home_team,away_team,home_goals,away_goals`. Every league value is `Bundesliga`, and seasons use `YYYY/YYYY`. IDs use the existing importer SHA-256 of compact UTF-8 JSON `[league,season,ISO date,home team,away team]`; scores, input paths and row order do not affect identity. The corrected replay date participates in its final ID. Original team labels are retained, including historical/modern naming inconsistencies already disclosed; only early-source weekday/game-count syntax is removed as documented schema annotation.

Every original source hash and prior acquisition/review artifact hash is checked. A fresh audit must match the saved structural snapshot, retaining only the evidenced E1 halftime warning. The replay correction must match its source file hash, row, expected source fields and score. Only `BL-DATE-1993-94-REPLAY` is authorized, and it must apply exactly once. Thus Bayern Munich–Nurnberg in 1993/1994 is **1994-05-03, 5–0 in the derived CSV**, while source row 254 remains **1994-04-03, 5–0**. Immutable correction evidence retains `applied: false` as the prior-stage record; the new manifest and linked exception record explicitly record application to the derivative. No new correction was inferred.

Creation refuses any existing output. `--check` rebuilds all three artifacts and compares them byte-for-byte without replacing files. Conversion also repeats with reversed input rows and requires identical match CSV bytes. Temporary importer bridges are confined to private storage and removed automatically.

```sh
PYTHONPATH=src .venv/bin/python -m scripts.standardize_bundesliga_results
PYTHONPATH=src .venv/bin/python -m scripts.standardize_bundesliga_results --check
```

### Private output artifacts

| Filename | Contents | SHA-256 |
|---|---|---|
| `bundesliga_standardized_1990_2025.csv` | 11,090 matches; exact eight-column schema | `4d1f35d7eae6be069435a566341d9d8767060483618e93df1811df8e6a522cdf` |
| `bundesliga_exceptions_1990_2025.json` | Five match-ID-linked exceptions and explicit default eligibility policy | `5215b2cf3d72aff1f1062fb406cd8a112e7f3aba47cd46667332710cbb3f6642` |
| `bundesliga_standardization_manifest.json` | 36 original file provenances/checksums, input/code/output hashes, 11,090 source-row-to-match-ID links, correction log and season validation | `7c6853079783066c804aa8f1b7081d0a7f86fa9f9c0911de1904e26aa214c172` |

### Exception metadata and preserved archive

All 11,090 official fixture rows remain in the CSV. The five known exceptions classify as **one COMPLETED_THEN_AWARDED, one COMPLETED_REPLAY_AFTER_ANNULMENT, two ABANDONED_THEN_AWARDED and one INTERRUPTED_COMPLETED_THEN_AWARDED**. Each sidecar entry links a valid unique output `match_id`, exact original file/hash/row/URL, official archived score, reliably evidenced on-field score, whether that score is a completed final, evidence URLs, training suitability and an exclusion/uncertainty reason. The replay entry also links its correction and the annulled original's 23 April 2–1 result as metadata, not as an extra valid fixture. There was no dropped match or substitution of played scores for official awards.

All five known exceptions are `EXCLUDED` from ordinary 90-minute 1/X/2 training under the documented policy. The completed replay is excluded conservatively pending a future explicit modelling decision. An abandoned match's score at cessation is explicitly not labelled a completed final. `UNRESOLVED` is the default for unlisted matches because the status review is not exhaustive; absence of an exception entry does not assume eligibility. Missing reviewed eligibility evidence likewise yields `UNRESOLVED`. No training filter or model integration was implemented. All exception and eligibility fields remain outside the eight-column schema.

### Standardization validation

- Exactly 11,090 matches and 36 seasons; 1991/1992 has 20 teams/380 fixtures, each other season 18 teams/306 fixtures.
- Exact eight-column CSV; no blank required values, rejected rows, dropped fixtures, duplicate IDs or duplicate season home-away pairings.
- Complete ordered home-away pair coverage retained for every season, checked again on the standardized output.
- Exact multiset agreement with audited source dates, teams, seasons and scores after the single guarded replay-date correction; no aliases, score corrections or other fact changes.
- Existing public `load_historical_data`/historical validator accepts every record without factual changes.
- Source-row lineage covers every output record; all five sidecar references bind exact unchanged source rows and preserved official output results.
- Independent reversed-order conversion yields identical CSV bytes; a separate `--check` run reproduces the CSV, sidecar and manifest byte-for-byte.

The original 36 CSV checksums remain unchanged, as do the 153 protected earlier Germany/DFB artifacts and 15 England artifacts checked by the existing offline review integrity tool. Existing DFB collection code and experiments were not changed.

**Tests and reproducibility:** 413 tests passed in the complete suite, including 24 new synthetic Bundesliga-standardization regressions (29 focused checks together with the five existing CSV-audit tests). The separate `--check` and protected-artifact integrity runs passed. The review checker still prints `correction_applied: false` for its immutable pre-standardization evidence; the standardized derivative and new provenance manifest separately record the actual application.

### Remaining limits

The early publisher's CC0 and DataHub's PDDL declarations do not establish clearance of third-party upstream rights. Existing notices, provenance and unresolved licensing statements remain intact in the manifest and this report. Sample verification and targeted exception review are not an exhaustive certification of every date or match status. The dataset is **technically ready for future integration**, subject to a deliberate model policy for eligibility/status uncertainty and resolution of intended-use licensing requirements. No model, prediction algorithm, Streamlit application or prior evaluation results were changed; no training, evaluation, publication, commit or push occurred.
