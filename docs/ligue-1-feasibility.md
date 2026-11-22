# Ligue 1 — Phase 2 bounded feasibility

Date: 2026-11-22. Original `toto` worktree, branch `feature/data-collection`, HEAD `81225118ced664f113c19b87cff8095b0333ccda`.

## Outcome and limits

Exactly seven approved source originals acquired. Modern formats are technically usable; the proposed uninterrupted 1990/91–2013/14 historical-source window is **not complete**. No original was changed, no match was corrected/excluded, no standardized output or model was created, and no application or promotional file was touched. Structural agreement is not historical certification or licensing clearance.

## Preservation and acquisition

`data/private/france/ligue_1/protected_before.json` freezes **558 pre-existing private files** and **165 tracked public files**, plus an append-only planning-log prefix. These encompass all eight completed competitions, source originals, outputs and evidence; all checked unchanged. The existing `/data/private/` ignore rule covers every new private original/artifact.

Pinned revisions:

- `jalapic/engsoccerdata`: `872c5c354161ace8408f3091b758c6af4cccca94`.
- `openfootball/europe`: `63df627f3c87ce71708f016522ea236cf74332c3`.

Both repositories were resolved via GitHub commit metadata, then both complete approved path sets were checked against immutable recursive trees before originals were requested. Tree responses/receipts and resolution responses are retained. Seven supporting README/licence/field/notes files were acquired in addition to the seven datasets. Requests have a 30-second timeout, 8 MB cap, two-second spacing, no redirects or automatic retries, and a persistent stop marker on access failure. Initial sandbox DNS failure on metadata access was resolved through authorized network access; no restriction was bypassed. No Football-Data endpoints were requested.

Every original has a per-file provenance JSON with exact pinned URL, commit/path/name/format, UTC retrieval time, byte count, SHA-256, Git blob identity, attribution and qualified rights. SHA-256, blob SHA-1 and tree sizes all agree. Cache reuse was tested with network access disabled; no original was re-downloaded.

| Original | Bytes | SHA-256 | Git blob SHA-1 |
|---|---:|---|---|
| `jalapic/engsoccerdata/data-raw/france.csv` | 2,155,298 | `86d9593d16709b202258a5cf23622966d86873fe4a5eec770e2de26cabcfce7f` | `30805787f1ab1de79b5bc1225abf56e53a71125b` |
| `openfootball/europe/france/2014-15_fr1.txt` | 30,086 | `dbc42a7835cd58b312d4653beadc1dc659d63be61fc1cf2897dc5dfa6b00c587` | `e050b478e48ac338afdd7b1c65ddf7a25700e1f4` |
| `openfootball/europe/france/2016-17_fr1.txt` | 30,063 | `24642e33c7c57b16973b87aebd306eda6ec7bda53ebe1a8e9eb4445974ea4749` | `fd7d69cb3e462e067740eee52f82341753ad5b75` |
| `openfootball/europe/france/2019-20_fr1.txt` | 30,182 | `5cf3583441ac7510fe6fc2334e217157e19ab21a062e19569069915f3900124d` | `fac92bf84ea9bd98a4e90a5f508822baf3c4a6b6` |
| `openfootball/europe/france/2023-24_fr1.txt` | 24,525 | `c4a6995827f65e7c1d36bdc528d5cea284684f27d1fa8f5e5c88fd7d373f8ca9` | `621eea2a9338b1c332e8698bc62dbcddde69612c` |
| `openfootball/europe/france/2025-26_fr1.txt` | 41,179 | `d173d6d5e41ca1f42c1b6b0b4b65fd7eabdd49130867c47dfd3ad2007869d347` | `590cd559087b68e4e556f160afd2662220b7536e` |
| `openfootball/europe/france/2025-26_fr1-full.txt` | 287,036 | `9d737b936f3e3c1edf0b77b84941518737d1dd94d8381c6a9b27b4b9c79c9daf` | `09031f742e1db5eaca0e97c7869a855975ef35eb` |

Exact URL pattern: `https://raw.githubusercontent.com/{repository}/{commit}/{original_path}`. Full receipt registry: private `acquisition.json`. Original bytes and notices remain immutable.

## Historical CSV: actual observed coverage

Observed **29,558 rows**, all score-bearing and all labelled tier 1, over **85 distinct season-start labels, 1932–2024**. Literal missing labels inside that range are **1937, 1939–1944 and 1994**. The wartime interval is not automatically classified as missing normal league seasons. The advertised “1933–2025” date span is not evidence of continuous or correctly labelled season coverage.

For the proposed 1990/91–2013/14 window: **23 of 24 season labels, 8,369 observations**, versus 8,750 structurally expected fixtures. The deficit is the absent 1994/95 season (380) plus one missing 2006/07 pairing. These are acquisition/structural findings, not approved supplements or exclusions.

- **1990/91:** 380 rows but 21 literal club labels. `Brest Armorique FC` and `Stade Brest` split the Brest appearances; this creates 40 apparent missing directed pairs at literal-label level. No identity mapping was applied or approved.
- **1994/95:** no rows. No unapproved fallback source acquired.
- **2006/07:** 379 rows; missing directed pairing `FC Nantes`–`Toulouse FC`. Documentary context suggests an administrative case; no result/date inferred.
- **1997/98–2001/02:** 18 clubs, 306 observations each; **2002/03:** back to 20 clubs and 380.
- **5,489 source `result` labels conflict with goal-derived outcomes** (all source `D` versus goal-derived `A`, across pre-2015/16 records); **1,895** occur in the proposed older window. FT strings, goal sums and goal differences otherwise agree. Original result labels remain unchanged; no training labels are exported.
- **1,162 dates lie outside the conventional source-season window**: 1,142 rows in labels 1932–1936 are concentrated on a single 1 July per label, plus ten rows each in 1946 and 1967. They are source date/season anomalies or likely proxies, not certified playing dates. Early label/format alignment remains unresolved.
- No missing/nonnumeric goals and no duplicate literal directed pairings found in the CSV. Other early club-label splits and same-team/date collisions are listed per season in the private assessment. Counts alone do not validate identity, chronology or history.
- `division` contains `1` (26,387) and `F1` (3,171); all `tier` values are `1`. There is **no explicit stage/round column**. No additional competition was positively identified, but tier labels and pairings cannot certify that every early row is an ordinary regular-season match.

## Complete historical source inventory

The following uses literal source season labels. Pre-1990 expected counts are deliberately not guessed. “Dates” counts out-of-window/invalid values; “Result” counts derived-label contradictions. Full physical source-line details remain private.

| Source season | Observed / scored | Clubs | Expected scheduled | Missing directed pairs | Date issues | Result conflicts |
|---|---:|---:|---:|---:|---:|---:|
| 1932/1933 | 182 / 182 | 14 | not established | 0 | 182 | 36 |
| 1933/1934 | 240 / 240 | 16 | not established | 0 | 240 | 62 |
| 1934/1935 | 240 / 240 | 16 | not established | 0 | 240 | 59 |
| 1935/1936 | 240 / 240 | 16 | not established | 0 | 240 | 50 |
| 1936/1937 | 240 / 240 | 16 | not established | 0 | 240 | 55 |
| 1937/1938 | **absent** | — | — | — | — | — |
| 1938/1939 | 240 / 240 | 16 | not established | 0 | 0 | 55 |
| 1939/1940 | **absent** | — | — | — | — | — |
| 1940/1941 | **absent** | — | — | — | — | — |
| 1941/1942 | **absent** | — | — | — | — | — |
| 1942/1943 | **absent** | — | — | — | — | — |
| 1943/1944 | **absent** | — | — | — | — | — |
| 1944/1945 | **absent** | — | — | — | — | — |
| 1945/1946 | 306 / 306 | 19 | not established | 36 | 0 | 78 |
| 1946/1947 | 340 / 340 | 21 | not established | 80 | 10 | 76 |
| 1947/1948 | 306 / 306 | 18 | not established | 0 | 0 | 71 |
| 1948/1949 | 306 / 306 | 18 | not established | 0 | 0 | 62 |
| 1949/1950 | 306 / 306 | 18 | not established | 0 | 0 | 74 |
| 1950/1951 | 306 / 306 | 18 | not established | 0 | 0 | 77 |
| 1951/1952 | 306 / 306 | 18 | not established | 0 | 0 | 73 |
| 1952/1953 | 306 / 306 | 18 | not established | 0 | 0 | 66 |
| 1953/1954 | 306 / 306 | 18 | not established | 0 | 0 | 68 |
| 1954/1955 | 306 / 306 | 18 | not established | 0 | 0 | 56 |
| 1955/1956 | 306 / 306 | 18 | not established | 0 | 0 | 65 |
| 1956/1957 | 306 / 306 | 18 | not established | 0 | 0 | 76 |
| 1957/1958 | 306 / 306 | 18 | not established | 0 | 0 | 73 |
| 1958/1959 | 380 / 380 | 20 | not established | 0 | 0 | 83 |
| 1959/1960 | 380 / 380 | 20 | not established | 0 | 0 | 102 |
| 1960/1961 | 380 / 380 | 20 | not established | 0 | 0 | 80 |
| 1961/1962 | 380 / 380 | 20 | not established | 0 | 0 | 87 |
| 1962/1963 | 380 / 380 | 20 | not established | 0 | 0 | 86 |
| 1963/1964 | 306 / 306 | 18 | not established | 0 | 0 | 59 |
| 1964/1965 | 306 / 306 | 18 | not established | 0 | 0 | 63 |
| 1965/1966 | 380 / 380 | 20 | not established | 0 | 0 | 67 |
| 1966/1967 | 380 / 380 | 20 | not established | 0 | 0 | 77 |
| 1967/1968 | 380 / 380 | 20 | not established | 0 | 10 | 84 |
| 1968/1969 | 306 / 306 | 18 | not established | 0 | 0 | 57 |
| 1969/1970 | 306 / 306 | 18 | not established | 0 | 0 | 67 |
| 1970/1971 | 380 / 380 | 20 | not established | 0 | 0 | 73 |
| 1971/1972 | 380 / 380 | 20 | not established | 0 | 0 | 82 |
| 1972/1973 | 380 / 380 | 20 | not established | 0 | 0 | 68 |
| 1973/1974 | 380 / 380 | 20 | not established | 0 | 0 | 70 |
| 1974/1975 | 380 / 380 | 20 | not established | 0 | 0 | 58 |
| 1975/1976 | 380 / 380 | 20 | not established | 0 | 0 | 60 |
| 1976/1977 | 380 / 380 | 20 | not established | 0 | 0 | 67 |
| 1977/1978 | 380 / 380 | 20 | not established | 0 | 0 | 73 |
| 1978/1979 | 380 / 380 | 20 | not established | 0 | 0 | 70 |
| 1979/1980 | 380 / 380 | 20 | not established | 0 | 0 | 81 |
| 1980/1981 | 380 / 380 | 20 | not established | 0 | 0 | 66 |
| 1981/1982 | 380 / 380 | 21 | not established | 40 | 0 | 70 |
| 1982/1983 | 380 / 380 | 20 | not established | 0 | 0 | 52 |
| 1983/1984 | 380 / 380 | 20 | not established | 0 | 0 | 79 |
| 1984/1985 | 380 / 380 | 20 | not established | 0 | 0 | 64 |
| 1985/1986 | 380 / 380 | 20 | not established | 0 | 0 | 55 |
| 1986/1987 | 380 / 380 | 21 | not established | 40 | 0 | 60 |
| 1987/1988 | 380 / 380 | 20 | not established | 0 | 0 | 68 |
| 1988/1989 | 380 / 380 | 21 | not established | 40 | 0 | 67 |
| 1989/1990 | 380 / 380 | 20 | not established | 0 | 0 | 56 |
| 1990/1991 | 380 / 380 | 21 | 380 | 40 | 0 | 57 |
| 1991/1992 | 380 / 380 | 20 | 380 | 0 | 0 | 71 |
| 1992/1993 | 380 / 380 | 20 | 380 | 0 | 0 | 74 |
| 1993/1994 | 380 / 380 | 20 | 380 | 0 | 0 | 66 |
| 1994/1995 | **absent** | — | — | — | — | — |
| 1995/1996 | 380 / 380 | 20 | 380 | 0 | 0 | 74 |
| 1996/1997 | 380 / 380 | 20 | 380 | 0 | 0 | 87 |
| 1997/1998 | 306 / 306 | 18 | 306 | 0 | 0 | 77 |
| 1998/1999 | 306 / 306 | 18 | 306 | 0 | 0 | 65 |
| 1999/2000 | 306 / 306 | 18 | 306 | 0 | 0 | 66 |
| 2000/2001 | 306 / 306 | 18 | 306 | 0 | 0 | 72 |
| 2001/2002 | 306 / 306 | 18 | 306 | 0 | 0 | 61 |
| 2002/2003 | 380 / 380 | 20 | 380 | 0 | 0 | 88 |
| 2003/2004 | 380 / 380 | 20 | 380 | 0 | 0 | 96 |
| 2004/2005 | 380 / 380 | 20 | 380 | 0 | 0 | 71 |
| 2005/2006 | 380 / 380 | 20 | 380 | 0 | 0 | 92 |
| 2006/2007 | 379 / 379 | 20 | 380 | 1 | 0 | 82 |
| 2007/2008 | 380 / 380 | 20 | 380 | 0 | 0 | 97 |
| 2008/2009 | 380 / 380 | 20 | 380 | 0 | 0 | 103 |
| 2009/2010 | 380 / 380 | 20 | 380 | 0 | 0 | 104 |
| 2010/2011 | 380 / 380 | 20 | 380 | 0 | 0 | 93 |
| 2011/2012 | 380 / 380 | 20 | 380 | 0 | 0 | 93 |
| 2012/2013 | 380 / 380 | 20 | 380 | 0 | 0 | 102 |
| 2013/2014 | 380 / 380 | 20 | 380 | 0 | 0 | 104 |
| 2014/2015 | 380 / 380 | 20 | 380 | 0 | 0 | 111 |
| 2015/2016 | 380 / 380 | 20 | 380 | 0 | 0 | 0 |
| 2016/2017 | 380 / 380 | 20 | 380 | 0 | 0 | 0 |
| 2017/2018 | 380 / 380 | 20 | 380 | 0 | 0 | 0 |
| 2018/2019 | 380 / 380 | 20 | 380 | 0 | 0 | 0 |
| 2019/2020 | 279 / 279 | 20 | 380 | 101 | 0 | 0 |
| 2020/2021 | 380 / 380 | 20 | 380 | 0 | 0 | 0 |
| 2021/2022 | 380 / 380 | 20 | 380 | 0 | 0 | 0 |
| 2022/2023 | 380 / 380 | 20 | 380 | 0 | 0 | 0 |
| 2023/2024 | 306 / 306 | 18 | 306 | 0 | 0 | 0 |
| 2024/2025 | 306 / 306 | 18 | 306 | 0 | 0 | 0 |

2019/20 historical CSV contains 279 scored matches; its 101 absent scheduled pairings agree with the curtailed-season scope, rather than proving acquisition loss.

## OpenFootball samples

| Original | Observed | Scored | Unscored | Clubs | Expected slots / played | Other stage | Wide rounds |
|---|---:|---:|---:|---:|---:|---:|---:|
| `2014-15_fr1.txt` | 380 | 380 | 0 | 20 | 380 / 380 | 0 | 3 |
| `2016-17_fr1.txt` | 380 | 380 | 0 | 20 | 380 / 380 | 0 | 5 |
| `2019-20_fr1.txt` | 380 | 279 | 101 | 20 | 380 / 279 | 0 | 4 |
| `2023-24_fr1.txt` | 306 | 306 | 0 | 18 | 306 / 306 | 0 | 3 |
| `2025-26_fr1.txt` | 306 | 306 | 0 | 18 | 306 / 306 | 0 | 2 |
| `2025-26_fr1-full.txt` | 306 | 306 | 0 | 18 | 306 / 306 | 0 | 2 |

All six files have complete literal directed pairings, zero duplicates/conflicts within a file, valid numeric scored results and valid season/weekday-resolved dates. They decode strictly as UTF-8, preserving accents, CRLF/LF and raw lines. All encountered fixture stages are regular season; repeated round headings are rescheduling blocks, **not extra stages**. There are no normalized case/NFC label collisions in these samples.

Day/month values are explicit source date headings; the year is often inferred from the season and verified weekday. A scheduled heading is not independent evidence of actual kickoff, completion or result availability. Date/time/venue strings are preserved separately in the full-file parse.

### 2019/20 reconciliation

**380 source slots = 279 scored + 101 explicitly `[cancelled]`**. Exactly one cancelled slot is in round 28; the other 100 are rounds 29–38. Scored-date coverage is 2019-08-09–2020-03-08; cancelled slots retain scheduled dates through 2020-05-23. The LFP board minutes of 2020-04-30, page 9 (L1-E01), independently establish 279 matches played out of 380 planned. No cancelled result was filled or classified as a played 0–0. The historical CSV matches all 279 scored observations under explicit diagnostic name correspondences.

### 2025/26 versions

Both contain the same 306 unique regular-season pairings, 18 club labels, 306 FT scores, zero blanks, and source dates 2025-08-15–2026-05-17. Direct fixture comparison finds **zero home/away, date or score discrepancies**. The full version adds scorers, lineups, substitutions, cards, referees, venues, attendance and timezone strings; it is not a second set of fixtures and must not be appended to the ordinary file. Both are score-complete, but **not historically certified reliable finished-match datasets**: Nantes–Toulouse at source date 2026-05-17, 0–0, is an unannotated abandoned/administratively ratified case.

Recommend the ordinary file as the simpler future parsing candidate, preserving the full version as supporting detail. This recommendation is based on measured equivalence, not a processing selection or correction approval.

## Overlap and diagnostic names

| Scored overlap | Matched | Date/score discrepancies |
|---|---:|---:|
| 2014/15 | 380 | 0 |
| 2016/17 | 380 | **1: Bastia–Lyon, 0–3 versus 0–0 `[awarded]`** |
| 2019/20 | 279 | 0 |
| 2023/24 | 306 | 0 |

2014/15 requires five non-identical correspondences: `AS Saint-Étienne` ↔ `AS Saint-Etienne`; `Olympique Lyonnais` ↔ `Olympique Lyon`; `Stade Rennais` ↔ `Stade Rennes`; `Stade de Reims` ↔ `Stade Reims`; `Évian Thonon Gaillard` ↔ `Evian Thonon Gaillard`. Exact remaining labels match unchanged. Each comparison requires a bijective mapping and unique pairings; all unmatched and duplicate pairs are reported. Additional inspected season-specific correspondences are in `additional_overlaps` and `DIAGNOSTIC_VARIANTS`. No global name mapping or original/source-window merge was made. Upstream independence remains unestablished; the CSV itself includes `F1` division labels and the compiler lists multiple external sources.

## Scheduling candidates

**17 distinct season/round flags, covering 165 unique fixture slots**, or 19 file-level flags when both 2025/26 versions are counted. A span exceeding 14 days is a review flag, not an error. One 2019/20 round-31 span comprises cancelled scheduled fixtures, not actual playing dates. Fixture-level dates/lines/annotations for every flag are retained in the private assessment.

| Season | Round | First–last source date |
|---|---:|---|
| 2014/2015 | 14 | 2014-11-21–2015-01-07 |
| 2014/2015 | 25 | 2015-02-13–2015-04-07 |
| 2014/2015 | 32 | 2015-04-10–2015-04-28 |
| 2016/2017 | 16 | 2016-12-02–2017-04-05 |
| 2016/2017 | 17 | 2016-12-10–2017-01-18 |
| 2016/2017 | 21 | 2017-01-20–2017-02-21 |
| 2016/2017 | 24 | 2017-02-07–2017-03-01 |
| 2016/2017 | 31 | 2017-03-31–2017-05-17 |
| 2019/2020 | 12 | 2019-11-01–2020-01-15 |
| 2019/2020 | 15 | 2019-11-29–2020-01-15 |
| 2019/2020 | 16 | 2019-12-03–2020-01-15 |
| 2019/2020 | 31 | 2020-04-05–2020-04-22 |
| 2023/2024 | 8 | 2023-10-06–2023-11-29 |
| 2023/2024 | 10 | 2023-10-27–2023-12-06 |
| 2023/2024 | 12 | 2023-11-10–2023-12-07 |
| 2025/2026 | 26 | 2026-03-13–2026-04-22 |
| 2025/2026 | 29 | 2026-04-10–2026-05-13 |

## Bounded exceptional-case evidence (no decisions applied)

| Case | Preserved source observation | Established context and remaining uncertainty |
|---|---|---|

| Bastia–Lyon 2016/17 | CSV line 26714: 2017-04-16, **0–3**; OpenFootball line 533: same date, **0–0 `[awarded]`** | Primary FFF record references appeal sanctions; indexed contemporary report describes awarded Lyon victory without goal-difference loss. Numerical-result conflict and effective availability remain unresolved pending primary decision/appeal review. Do not derive an official draw from 0–0 or assume an invented 0–3. |

| Nantes–Bastia 2013/14 | CSV line 25254: 2013-08-10, **0–0**, unannotated | Club context describes an on-field Nantes victory; Conseil d’État ruling confirms penalty defeat, Bastia victory and rejected challenges on 2016-05-11. Numerical administrative score and earliest effective availability are not established by inspected passages. |

| Nice–Marseille 2021/22 | CSV line 28297: **2021-10-27, 1–1** | Direct contemporary club account establishes Troyes replay after August interruption, completing 1–1 on October 27. Keep original event and replay distinct; no kickoff-date substitution. Exact August day not certified in this bounded review. |

| Nantes–Toulouse 2006/07 | Pairing absent; no source result/date to replace | Club retrospective describes 0–0 on field and points awarded to Toulouse after pitch invasion. No missing score/date supplemented; primary decision and dated fixture evidence needed. |

| Montpellier–Clermont 2023/24 | OpenFootball line 204: **2023-11-29, 1–1**, unannotated | LFP 2023-10-25 decision orders replay of October 8 abandoned match. November 29 date has limited official indexed corroboration; complete replay result/finality review remains later work. |

| Nantes–Toulouse 2025/26 | Both files: **2026-05-17, 0–0**, unannotated | Direct club report establishes permanent interruption after 22 minutes; LFP decision of **2026-05-27** ratifies 0–0. Indexed club statement reserves appeal rights. Do not equate May 17 source date with final-result availability; no date policy or appeal-finality conclusion applied. |

Other high scores, same-team/date collisions, early identity/date problems and rescheduling flags remain visible in assessment metadata. This is not exhaustive historical certification of all observed fixtures.

### Documentary references and access classification

- **L1-E01 — LFP Conseil d’administration, procès-verbal du 30 avril 2020** (2020-04-30; `DIRECTLY_INSPECTED_PDF`). https://www.lfp.fr/assets/20200430_PV_Conseil_Administration_LFP_e824a457fa.pdf — Season ended after 279 Ligue 1 fixtures out of 380 planned; aggregate evidence, not individual-match certification. Independence: Official organizer document; distinct documentary role from compiled match files.
- **L1-E02 — Conseil d’État, 11 mai 2016, 388322 et affaires jointes** (2016-05-11; `DIRECTLY_INSPECTED`). https://www.legifrance.gouv.fr/ceta/id/CETATEXT000032528070/ — Nantes–Bastia played 2013-08-10; decision gave Nantes a penalty defeat and Bastia victory; challenges rejected. No numerical administrative score established in inspected passage. Independence: Official judicial decision, independently authored legal evidence; not a match-results feed.
- **L1-E03 — Communiqué officiel du FC Nantes** (publication date not established; `SEARCH_INDEX_ONLY`). https://www.fcnantes.com/articles/article2809.php?num=9261 — Contemporary club statement describes the Nantes on-field victory and disputed points reassignment; not final legal certification. Independence: Interested party; claim assessed against judicial decision.
- **L1-E04 — Un derby sans vainqueur (1-1)** (2021-10-27; `DIRECTLY_INSPECTED`). https://www.ogcnice.com/fr/resume/119578/un-derby-sans-vainqueur-1-1.html — Nice–Marseille replayed in Troyes on 2021-10-27 after August interruption, finishing 1–1. Original August day and all appeal finality not certified here. Independence: Contemporary participant-authored narrative; match widget distinguished from authored account.
- **L1-E05 — FFF Commission fédérale des pratiques seniors, section masculine, 19 septembre 2017** (2017-09-19; `DIRECTLY_INSPECTED_PDF`). https://media.fff.fr/uploads/document/d177722a933bf0d34930691c85b8d9e2.pdf — References 23 May appeal sanctions relating to Bastia–Lyon of 2017-04-16; passage does not establish a numerical FT score or the awarded winner. Independence: Federation administrative record; limited scope explicitly preserved.
- **L1-E06 — Discipline : défaite sur tapis vert pour Bastia contre Lyon et trois matches à huis clos** (2017-05-04; `SEARCH_INDEX_ONLY_SECONDARY`). https://www.lequipe.fr/Football/Actualites/Discipline-defaite-sur-tapis-vert-pour-bastia-contre-lyon-et-trois-matches-a-huis-clos/798557 — Contemporary report describes awarded Lyon victory without goal-difference loss. This indexed secondary summary does not settle the source score conflict. Independence: Secondary contemporary reporting; not treated as definitive primary certification.
- **L1-E07 — Commission de discipline : les décisions du 27 mai 2026** (2026-05-27; `DIRECTLY_INSPECTED`). https://www.lfp.fr/article/commission-de-discipline-les-decisions-du-27-mai-2026 — Nantes–Toulouse of 2026-05-17 permanently interrupted; commission ratifies 0–0 on 2026-05-27. Does not establish exhaustive appeal clearance or justify May 17 result availability. Independence: Official first-instance disciplinary decision; later appeal position remains separate.
- **L1-E08 — FC Nantes-TéFéCé arrêté après un envahissement de terrain** (2026-05-18; `DIRECTLY_INSPECTED`). https://www.toulousefc.com/play/blog/2026/05/le-compte-rendu-de-fc-nantes-tefece-34eme-journee-de-ligue-1-mcdonald-s — Club account records interruption after 22 minutes on May 17 and permanent abandonment. Independence: Contemporary participant account, corroborates interruption rather than final legal result.
- **L1-E09 — Communiqué relatif à l’annonce de la commission de discipline de la LFP après l’arrêt de FC Nantes-TéFéCé** (2026-05-27; `SEARCH_INDEX_ONLY_DIRECT_OPEN_TIMED_OUT`). https://www.toulousefc.com/play/blog/2026/05/communique-relatif-a-l-annonce-de-la-commission-de-discipline-de-la-lfp-apres-l-arret-de-fc-nantes-tefece — Indexed club statement reserves right to appeal ratification; actual appeal/final adjudication not established. Independence: Interested-party statement; not a final appellate decision.
- **L1-E10 — L’histoire du TéFéCé, section 2007** (publication date not established; `DIRECTLY_INSPECTED`). https://www.toulousefc.com/region/histoire — Retrospective club account describes Nantes pitch invasion, on-field 0–0 and three points awarded to Toulouse in 2006/07. Exact fixture date, administrative score and availability require further evidence. Independence: Participant retrospective; does not independently certify a missing dated result.
- **L1-E11 — Commission de discipline : les décisions du 25 octobre 2023** (2023-10-25; `DIRECTLY_INSPECTED`). https://www.lfp.fr/article/commission-de-discipline-les-decisions-du-25-octobre-2023 — Montpellier–Clermont of 2023-10-08 permanently interrupted; ordered replay behind closed doors. Does not itself certify eventual replay result. Independence: Official organizer disciplinary decision.
- **L1-E12 — Commission de discipline : les décisions du 30 novembre 2023** (2023-11-30; `SEARCH_INDEX_ONLY`). https://www.lfp.fr/article/commission-de-discipline-les-decisions-du-30-novembre-2023 — Names round-8 Montpellier–Clermont as played on 2023-11-29; limited indexed date context, not full-fact result verification. Independence: Official organizer document, index-only access distinguished.

The ledger preserves document title, URL, publication/access classification, inspected scope and limitations. Documents opened through the research tool are distinguished from search-index-only summaries; no complete additional season dataset was acquired. No administrative case is certified solely from a secondary summary.

## Schema, chronology and permissions

Future schema remains exactly `match_id,date,league,season,home_team,away_team,home_goals,away_goals`; proposed canonical league is **`Ligue 1`**. Preserve original Division 1/F1 labels and source year fields in future audit metadata, and delegate IDs to the shared importer. No IDs or standardized output generated here.

Ordinary dated/scored fixtures are technically extractable. Administrative results may not be faithfully representable by goal-derived outcome alone; unresolved outcomes and effective dates require explicit later policy. Preserve source/scheduled date, actual kickoff, abandonment, replay/completion and decision date separately. Chronological use must never expose results before availability, and date-precision consumers must use results strictly before prediction date.

| Classification | Assessment |
|---|---|
| Technical usability | Modern grammar usable; older source needs gap, identity, date and derived-label review. |
| Historical reliability | Structural only plus bounded documentary cases; no population certification. |
| Redistribution | engsoccerdata README noncommercial statement versus GPL package metadata and upstream rights unresolved. OpenFootball CC0 covers rights held, without third-party warranty. Original bytes stay private. |
| Model-training clearance | **UNRESOLVED for both sources**; neither parsing success nor acquisition approval clears downstream use. |

## Verification and reproduction

35 synthetic feasibility tests cover exact source scope, tree/path/blob checks, cache reuse and tampering, access stops, immutable writes, protected files, score/date grammar, annotations, season/stage handling, missing results, contradictions, identities, overlap differences and deterministic serialization. All **1,110 repository tests passed**, including app/launcher tests (prior 1,075 plus 35 new cases).

The original `.venv` pytest/pandas import timed out at 20 seconds. It was not modified. Reused the existing offline environment `/var/folders/00/_mqs0s6n56g22kfzlmmm54rm0000gn/T/toto-phase8-completion-eum02_co/venv`, Python 3.13.12, pytest 9.1.1, pandas 3.0.6. No dependencies installed/upgraded. Full suite completed in 84.98 seconds with caches/output directed outside the project and bytecode writes disabled. The timeout is not a test pass.

An independent raw CSV/text extraction checked every historical row and every modern fixture against the saved assessment, without using the production parser for extraction. A fresh-process build in a safe temporary directory produced **byte-identical and SHA-256-identical** assessment output. Saved assessment: **30,016,840 bytes**, SHA-256 `4b330225e14188a82018faa74f7aca5a181992bfa81d7836fbd91c5ec2541a42`. The saved original and assessment were not overwritten during comparison.

Offline reproduction (use a working project-compatible Python; `PYTHONDONTWRITEBYTECODE=1` and `PYTHONPATH=src:.`):

```sh
python -B -m scripts.validate_ligue1_feasibility --check
python -B -m pytest tests/test_ligue1_feasibility.py -q -p no:cacheprovider
```

For a separate-location regeneration, serialize `scripts.validate_ligue1_feasibility.build()` using `scripts.collect_ligue1_feasibility.encode()` to a new temporary path and compare bytes and SHA-256 with the saved assessment. The public collector is idempotent; never rerun against a partial/access-stopped bundle without investigation.

## Files and stopping point

Public changes are only:

- `scripts/collect_ligue1_feasibility.py` (new).
- `scripts/validate_ligue1_feasibility.py` (new).
- `tests/test_ligue1_feasibility.py` (new).
- `docs/ligue-1-feasibility.md` (new).
- `PLANNING_LOG.md` (append only).

Private area contains seven exact source originals and seven supporting notices/field documents, per-file receipts, two Git trees/receipts, two resolved-head responses/receipts, the protected baseline, acquisition manifest, final assessment, two explicitly superseded assessment drafts retained for transparency, documentary-context ledger, independent verification receipt and final verification/inventory evidence. Complete generated-file names and hashes are in `phase2_final_verification.json`. No private data is tracked/staged. Temporary test logs, regenerated assessment and offline-check helper are outside the project; no promotional worktree access.

## Recommended Phase 3 (approval required)

1. Acquire only the **seven missing ordinary OpenFootball seasons** at the already inspected pin: 2015/16, 2017/18, 2018/19, 2020/21, 2021/22, 2022/23, 2024/25. Resolve exact `france/YYYY-YY_fr1.txt` paths/blobs first. Reuse the five ordinary originals and preserve the 2025/26 full original separately. This would inventory twelve modern seasons, not certify all fixtures.
2. Reuse the historical CSV unchanged for an explicit older-window inventory; do not declare the 24-season window complete. Carry 1994/95 missing season, Nantes–Toulouse 2006/07, Brest label split, erroneous result labels and all exceptional/date cases forward unchanged.
3. Keep **1994/95** an open source/permission task. Seek a separately approved, rights-compatible dated source or permission-compliant bounded alternative; no restricted Football-Data request, mirror circumvention or speculative filling. The single missing 2006/07 fixture needs primary evidence and later approved policy, not an automatic supplement.
4. Do not extend earlier than 1990/91 until proxy dates, shifted/missing labels, historical formats and club continuity have been independently assessed. Retain 2026/27 outside scope.
5. Keep technical inventory, Phase 5 historical evidence, Phase 6 decisions and licensing/training clearance separate. Do not standardize, train, stage, commit or push during Phase 2.
