# La Liga Phase 4: comprehensive structural validation

Date: 2026-11-22 (Europe/Budapest). Branch: `feature/data-collection`.
Original `toto` worktree; HEAD remains `2f2bfe1542c2460111ae685621d138874fa69f52`.

## Outcome and assurance boundary

All **13,844 selected fixtures across 36 seasons** pass the implemented structural
checks. There are **zero fixture-level structural errors, zero season-level error
events, and zero cross-source date/full-time-score discrepancies**. This is not
independent historical certification, final administrative-status verification or
model-training clearance. No source records were repaired, excluded or standardized.

Counts describe different units and must not be added together:

| Measure | Count | Meaning |
|---|---:|---|
| Selected and structurally valid fixture records | 13,844 | Full approved source window |
| Confirmed structural-error fixture records | 0 | No source correction justified |
| Round-level scheduling flags | 34 | All preserved, including five Phase 2 and 29 Phase 3 flags |
| Unique fixtures within those rounds | 340 | Ten per flagged round; not 340 proven anomalous matches |
| Fixtures outside the densest seven-day cluster | 52 | Diagnostic prioritization only; not proven original schedules |
| Unusually high-score records | 1 | Internally consistent 10–2; already within the 340 flagged-round records |
| Additional interruption/resumption leads | 2 | Prior discovery leads without newly certified status; outside the 340 |
| Unique fixtures in the focused historical-review queue | 342 | Union, without double counting |
| Overlapping source observations compared | 4,940 | 13 seasons; agreement does not establish independence |
| Independently historically certified records | 0 | All 13,844 remain unverified at that assurance level |

## Independent implementation and checks

`scripts/validate_la_liga_structure.py` independently reads strict CSV and
Football.TXT fields rather than accepting the Phase 3 parsed records as input.
Each freshly parsed date, team, full-time score and physical source line must
agree with the frozen inventory as an additional consistency check. It reuses
the established exact-integer and goal-derived outcome primitives, not source
counts or a new parallel match-ID implementation.

The checks include:

- Exact CSV schema and row width; explicit tier 1 / league / empty group selection.
- Text competition titles and any stated season; regular-stage grammar only.
- Expected season-specific clubs and counts, every ordered home/away pairing,
  balanced appearances, missing/duplicated/conflicting fixtures.
- Every text round has ten fixtures and each club once; each half-season covers
  each unordered opponent pair once. Repeated headings do not create new rounds.
- Full-time goals are finite nonnegative integers; FT strings must agree. All
  13,465 supplied halftime scores are checked against FT; 379 absent optional HT
  fields are not fabricated or treated as missing full-time results.
- Goal-derived outcomes total 6,598 home wins, 3,598 draws and 3,648 away wins.
- ISO dates, season limits, explicit weekdays and kickoff times; the known 2019/20
  calendar permits July/August 2020. Source years omitted in date headings are
  interpreted explicitly, including July 2020; no original date is rewritten.
- Same-team/same-date conflicts, consecutive-day plausibility leads, unusually
  high scores, source annotations, optional header counts (28 Teams/Matches checks).
- Strict UTF-8, control/replacement characters, whitespace, NFC/case-equivalent
  team-label collisions, full label catalog and consecutive-season label changes.

Unknown or contradictory source structure fails with season/path/line diagnostics.
Global season errors and fixture-level errors are reported separately. No failures
are downgraded merely to obtain the expected total. No selected source contained
a weekday, header-count, halftime, pairing, score or date-boundary contradiction.

## Season-by-season validation

H = engsoccerdata; O = OpenFootball. All rows below have zero structural errors.
The final two columns are non-error historical-review leads.

| Season | Source | Observed / scored / expected | Clubs | Source date coverage | Wide rounds | High-score flags |
|---|---|---:|---:|---|---:|---:|
| 1990/1991 | H | 380 / 380 / 380 | 20 | 1990-09-01–1991-06-09 | 0 | 0 |
| 1991/1992 | H | 380 / 380 / 380 | 20 | 1991-08-31–1992-06-07 | 0 | 0 |
| 1992/1993 | H | 380 / 380 / 380 | 20 | 1992-09-05–1993-06-20 | 0 | 0 |
| 1993/1994 | H | 380 / 380 / 380 | 20 | 1993-09-04–1994-05-15 | 0 | 0 |
| 1994/1995 | H | 380 / 380 / 380 | 20 | 1994-09-03–1995-06-18 | 0 | 0 |
| 1995/1996 | H | 462 / 462 / 462 | 22 | 1995-09-02–1996-05-26 | 0 | 0 |
| 1996/1997 | H | 462 / 462 / 462 | 22 | 1996-08-31–1997-06-23 | 0 | 0 |
| 1997/1998 | H | 380 / 380 / 380 | 20 | 1997-08-30–1998-05-16 | 0 | 0 |
| 1998/1999 | H | 380 / 380 / 380 | 20 | 1998-08-29–1999-06-20 | 0 | 0 |
| 1999/2000 | H | 380 / 380 / 380 | 20 | 1999-08-21–2000-05-20 | 0 | 0 |
| 2000/2001 | H | 380 / 380 / 380 | 20 | 2000-09-09–2001-06-17 | 0 | 0 |
| 2001/2002 | H | 380 / 380 / 380 | 20 | 2001-08-25–2002-05-11 | 0 | 0 |
| 2002/2003 | H | 380 / 380 / 380 | 20 | 2002-08-31–2003-06-22 | 0 | 0 |
| 2003/2004 | H | 380 / 380 / 380 | 20 | 2003-08-30–2004-05-23 | 0 | 0 |
| 2004/2005 | H | 380 / 380 / 380 | 20 | 2004-08-28–2005-05-29 | 0 | 0 |
| 2005/2006 | H | 380 / 380 / 380 | 20 | 2005-08-27–2006-05-20 | 0 | 0 |
| 2006/2007 | H | 380 / 380 / 380 | 20 | 2006-08-26–2007-06-17 | 0 | 0 |
| 2007/2008 | H | 380 / 380 / 380 | 20 | 2007-08-25–2008-05-18 | 0 | 0 |
| 2008/2009 | H | 380 / 380 / 380 | 20 | 2008-08-30–2009-05-31 | 0 | 0 |
| 2009/2010 | H | 380 / 380 / 380 | 20 | 2009-08-29–2010-05-16 | 0 | 0 |
| 2010/2011 | H | 380 / 380 / 380 | 20 | 2010-08-28–2011-05-21 | 0 | 0 |
| 2011/2012 | H | 380 / 380 / 380 | 20 | 2011-08-27–2012-05-13 | 0 | 0 |
| 2012/2013 | O | 380 / 380 / 380 | 20 | 2012-08-18–2013-06-01 | 1 | 0 |
| 2013/2014 | O | 380 / 380 / 380 | 20 | 2013-08-17–2014-05-18 | 1 | 0 |
| 2014/2015 | O | 380 / 380 / 380 | 20 | 2014-08-23–2015-05-23 | 1 | 0 |
| 2015/2016 | O | 380 / 380 / 380 | 20 | 2015-08-21–2016-05-15 | 1 | 1 |
| 2016/2017 | O | 380 / 380 / 380 | 20 | 2016-08-19–2017-05-21 | 2 | 0 |
| 2017/2018 | O | 380 / 380 / 380 | 20 | 2017-08-18–2018-05-20 | 2 | 0 |
| 2018/2019 | O | 380 / 380 / 380 | 20 | 2018-08-17–2019-05-19 | 1 | 0 |
| 2019/2020 | O | 380 / 380 / 380 | 20 | 2019-08-16–2020-07-19 | 2 | 0 |
| 2020/2021 | O | 380 / 380 / 380 | 20 | 2020-09-12–2021-05-23 | 5 | 0 |
| 2021/2022 | O | 380 / 380 / 380 | 20 | 2021-08-13–2022-05-22 | 3 | 0 |
| 2022/2023 | O | 380 / 380 / 380 | 20 | 2022-08-12–2023-06-04 | 1 | 0 |
| 2023/2024 | O | 380 / 380 / 380 | 20 | 2023-08-11–2024-05-26 | 4 | 0 |
| 2024/2025 | O | 380 / 380 / 380 | 20 | 2024-08-15–2025-05-25 | 6 | 0 |
| 2025/2026 | O | 380 / 380 / 380 | 20 | 2025-08-15–2026-05-24 | 4 | 0 |

## All 34 scheduling cases

Each case remains **UNRESOLVED_HISTORICAL_SCHEDULING**, with no confirmed structural
error. R = repeated source round heading with separated printed date blocks;
D = different date blocks under one round heading. Neither proves postponement,
advancement, continuation or its reason. No selected non-scorer source note
explicitly explains the exceptional status of these rounds.

The fixture column lists all records outside the densest seven-day cluster,
which is only a reproducible reference window, not an inferred original schedule.
Every case also retains all ten fixtures, earliest/latest boundary fixtures and
physical source lines in `phase4_structural_validation.json`. Full boundary lists
are printed in the following appendix. No long span is classified as an error.

| ID | Season / round | Earliest–latest date | Outside reference cluster: date, home–away | Source hint / origin |
|---|---|---|---|---|
| S01 | 2012/2013 / 3 | 2012-09-01–2012-09-26 | 2012-09-26: Real Betis–Atlético Madrid (L54) | D / PHASE_2 |
| S02 | 2013/2014 / 34 | 2014-04-18–2014-05-07 | 2014-05-07: Real Valladolid–Real Madrid (L570) | D / PHASE_3 |
| S03 | 2014/2015 / 16 | 2014-12-19–2015-02-04 | 2015-02-04: Real Madrid–Sevilla FC (L270) | D / PHASE_3 |
| S04 | 2015/2016 / 16 | 2015-12-19–2016-02-17 | 2016-02-17: Sporting Gijón–FC Barcelona (L265) | D / PHASE_3 |
| S05 | 2016/2017 / 16 | 2016-12-16–2017-02-22 | 2017-02-22: Valencia CF–Real Madrid (L272) | D / PHASE_3 |
| S06 | 2016/2017 / 21 | 2017-02-04–2017-05-17 | 2017-03-08: Deportivo La Coruña–Real Betis (L354)<br>2017-05-17: RC Celta–Real Madrid (L356) | D / PHASE_3 |
| S07 | 2017/2018 / 16 | 2017-12-15–2018-02-21 | 2018-02-21: CD Leganés–Real Madrid (L272) | D / PHASE_3 |
| S08 | 2017/2018 / 34 | 2018-04-20–2018-05-09 | 2018-05-09: FC Barcelona–Villarreal CF (L572)<br>2018-05-09: Sevilla FC–Real Madrid (L573) | D / PHASE_3 |
| S09 | 2018/2019 / 3 | 2018-08-31–2018-10-24 | 2018-10-24: Rayo Vallecano–Athletic Club (L57) | D / PHASE_3 |
| S10 | 2019/2020 / 10 | 2019-10-25–2019-12-18 | 2019-12-18: FC Barcelona–Real Madrid (L167) | D / PHASE_3 |
| S11 | 2019/2020 / 24 | 2020-02-14–2020-03-10 | 2020-03-10: SD Eibar–Real Sociedad (L390) | D / PHASE_3 |
| S12 | 2020/2021 / 1 | 2020-09-12–2021-02-24 | 2021-01-12: Club Atlético de Madrid–Sevilla FC (L309)<br>2021-02-09: Real Madrid CF–Getafe CF (L379)<br>2021-02-24: FC Barcelona–Elche CF (L423) | R / PHASE_3 |
| S13 | 2020/2021 / 2 | 2020-09-19–2021-03-17 | 2021-01-06: Athletic Club–FC Barcelona (L283)<br>2021-02-17: Levante UD–Club Atlético de Madrid (L401)<br>2021-03-17: Sevilla FC–Elche CF (L484) | R / PHASE_3 |
| S14 | 2020/2021 / 4 | 2020-09-29–2021-01-12 | 2021-01-12: Granada CF–CA Osasuna (L304) | R / PHASE_3 |
| S15 | 2020/2021 / 19 | 2020-12-15–2021-01-21 | 2020-12-15: Real Madrid CF–Athletic Club (L213)<br>2020-12-16: FC Barcelona–Real Sociedad de Fútbol (L215) | R / PHASE_3 |
| S16 | 2020/2021 / 18 | 2021-01-08–2021-03-10 | 2021-03-10: Club Atlético de Madrid–Athletic Club (L462) | R / PHASE_3 |
| S17 | 2021/2022 / 4 | 2021-09-11–2021-12-21 | 2021-12-21: Villarreal CF–Deportivo Alavés (L309)<br>2021-12-21: Sevilla FC–FC Barcelona (L310) | R / PHASE_3 |
| S18 | 2021/2022 / 9 | 2021-10-16–2021-12-22 | 2021-12-01: Real Madrid CF–Athletic Club (L253)<br>2021-12-22: Granada CF–Club Atlético de Madrid (L315) | R / PHASE_3 |
| S19 | 2021/2022 / 21 | 2021-12-22–2022-04-24 | 2021-12-22: Athletic Club–Real Madrid CF (L320)<br>2022-02-16: Club Atlético de Madrid–Levante UD (L420)<br>2022-03-02: RCD Mallorca–Real Sociedad de Fútbol (L459)<br>2022-04-24: FC Barcelona–Rayo Vallecano de Madrid (L580) | R / PHASE_3 |
| S20 | 2022/2023 / 17 | 2023-01-13–2023-02-02 | 2023-02-01: Real Betis Balompié–FC Barcelona (L327)<br>2023-02-02: Real Madrid CF–Valencia CF (L329) | R / PHASE_3 |
| S21 | 2023/2024 / 4 | 2023-09-01–2023-12-23 | 2023-12-23: Club Atlético de Madrid–Sevilla FC (L314) | R / PHASE_3 |
| S22 | 2023/2024 / 13 | 2023-11-10–2023-11-29 | 2023-11-29: RCD Mallorca–Cádiz CF (L242) | R / PHASE_3 |
| S23 | 2023/2024 / 20 | 2024-01-12–2024-02-01 | 2024-01-31: FC Barcelona–CA Osasuna (L382)<br>2024-01-31: Club Atlético de Madrid–Rayo Vallecano de Madrid (L383)<br>2024-02-01: Getafe CF–Real Madrid CF (L385) | R / PHASE_3 |
| S24 | 2023/2024 / 26 | 2024-02-23–2024-04-04 | 2024-04-04: Granada CF–Valencia CF (L524) | R / PHASE_3 |
| S25 | 2024/2025 / 3 | 2024-08-26–2024-09-18 | 2024-09-18: Real Betis Balompié–Getafe CF (L98) | R / PHASE_3 |
| S26 | 2024/2025 / 12 | 2024-11-01–2025-01-03 | 2024-12-18: Villarreal CF–Rayo Vallecano de Madrid (L309)<br>2025-01-03: Valencia CF–Real Madrid CF (L335) | R / PHASE_3 |
| S27 | 2024/2025 / 13 | 2024-11-08–2024-12-18 | 2024-12-18: RCD Espanyol de Barcelona–Valencia CF (L314) | R / PHASE_3 |
| S28 | 2024/2025 / 19 | 2024-12-03–2025-01-13 | 2024-12-03: RCD Mallorca–FC Barcelona (L269)<br>2024-12-04: Athletic Club–Real Madrid CF (L271) | R / PHASE_3 |
| S29 | 2024/2025 / 26 | 2025-02-28–2025-04-27 | 2025-04-27: Villarreal CF–RCD Espanyol de Barcelona (L591) | R / PHASE_3 |
| S30 | 2024/2025 / 27 | 2025-03-08–2025-03-27 | 2025-03-27: FC Barcelona–CA Osasuna (L503) | R / PHASE_3 |
| S31 | 2025/2026 / 6 | 2025-08-27–2025-09-25 | 2025-08-27: RC Celta–Real Betis (L70) | R / PHASE_2 |
| S32 | 2025/2026 / 19 | 2025-12-02–2026-01-12 | 2025-12-02: Barcelona–Atlético de Madrid (L420)<br>2025-12-03: Athletic Club–Real Madrid C.F. (L424) | R / PHASE_2 |
| S33 | 2025/2026 / 16 | 2025-12-12–2026-02-18 | 2026-02-18: Levante UD–Villarreal (L713) | R / PHASE_2 |
| S34 | 2025/2026 / 23 | 2026-02-06–2026-03-04 | 2026-03-04: Rayo Vallecano–Real Oviedo (L780) | R / PHASE_2 |

### Boundary fixtures for every scheduling case

- **S01 — 2012/2013, round 3**: earliest 2012-09-01: RC Celta–CA Osasuna 2–0 (L43); Real Zaragoza–Málaga CF 0–1 (L44); Deportivo La Coruña–Getafe CF 1–1 (L45); RCD Mallorca–Real Sociedad 1–0 (L46). Latest 2012-09-26: Real Betis–Atlético Madrid 2–4 (L54).
- **S02 — 2013/2014, round 34**: earliest 2014-04-18: Atlético Madrid–Elche CF 2–0 (L557). Latest 2014-05-07: Real Valladolid–Real Madrid 1–1 (L570).
- **S03 — 2014/2015, round 16**: earliest 2014-12-19: RC Celta–UD Almería 0–1 (L258). Latest 2015-02-04: Real Madrid–Sevilla FC 2–1 (L270).
- **S04 — 2015/2016, round 16**: earliest 2015-12-19: Valencia CF–Getafe CF 2–2 (L254); Espanyol Barcelona–UD Las Palmas 1–0 (L255); Real Betis–Sevilla FC 0–0 (L256); Deportivo La Coruña–SD Eibar 2–0 (L257). Latest 2016-02-17: Sporting Gijón–FC Barcelona 1–3 (L265).
- **S05 — 2016/2017, round 16**: earliest 2016-12-16: CD Alavés–Real Betis 1–0 (L259). Latest 2017-02-22: Valencia CF–Real Madrid 2–1 (L272).
- **S06 — 2016/2017, round 21**: earliest 2017-02-04: Málaga CF–Espanyol Barcelona 0–1 (L343); FC Barcelona–Athletic Club 3–0 (L344); Atlético Madrid–CD Leganés 2–0 (L345); Valencia CF–SD Eibar 0–4 (L346). Latest 2017-05-17: RC Celta–Real Madrid 1–4 (L356).
- **S07 — 2017/2018, round 16**: earliest 2017-12-15: Sevilla FC–Levante UD 0–0 (L259). Latest 2018-02-21: CD Leganés–Real Madrid 1–3 (L272).
- **S08 — 2017/2018, round 34**: earliest 2018-04-20: CD Leganés–Deportivo La Coruña 0–0 (L560). Latest 2018-05-09: FC Barcelona–Villarreal CF 5–1 (L572); Sevilla FC–Real Madrid 3–2 (L573).
- **S09 — 2018/2019, round 3**: earliest 2018-08-31: Getafe CF–Real Valladolid 0–0 (L45); SD Eibar–Real Sociedad 2–1 (L46); Villarreal CF–Girona FC 0–1 (L47). Latest 2018-10-24: Rayo Vallecano–Athletic Club 1–1 (L57).
- **S10 — 2019/2020, round 10**: earliest 2019-10-25: Villarreal CF–CD Alavés 4–1 (L155). Latest 2019-12-18: FC Barcelona–Real Madrid 0–0 (L167).
- **S11 — 2019/2020, round 24**: earliest 2020-02-14: Valencia CF–Atlético Madrid 2–2 (L378). Latest 2020-03-10: SD Eibar–Real Sociedad 1–2 (L390).
- **S12 — 2020/2021, round 1**: earliest 2020-09-12: SD Eibar–RC Celta de Vigo 0–0 (L11); Granada CF–Athletic Club 2–0 (L12); Cádiz CF–CA Osasuna 0–2 (L13). Latest 2021-02-24: FC Barcelona–Elche CF 3–0 (L423).
- **S13 — 2020/2021, round 2**: earliest 2020-09-19: Villarreal CF–SD Eibar 2–1 (L23); Getafe CF–CA Osasuna 1–0 (L24); RC Celta de Vigo–Valencia CF 2–1 (L25). Latest 2021-03-17: Sevilla FC–Elche CF 2–0 (L484).
- **S14 — 2020/2021, round 4**: earliest 2020-09-29: Real Sociedad de Fútbol–Valencia CF 0–1 (L50); Getafe CF–Real Betis Balompié 3–0 (L51). Latest 2021-01-12: Granada CF–CA Osasuna 2–0 (L304).
- **S15 — 2020/2021, round 19**: earliest 2020-12-15: Real Madrid CF–Athletic Club 3–1 (L213). Latest 2021-01-21: Valencia CF–CA Osasuna 1–1 (L322); SD Eibar–Club Atlético de Madrid 1–2 (L323).
- **S16 — 2020/2021, round 18**: earliest 2021-01-08: RC Celta de Vigo–Villarreal CF 0–4 (L288). Latest 2021-03-10: Club Atlético de Madrid–Athletic Club 2–1 (L462).
- **S17 — 2021/2022, round 4**: earliest 2021-09-11: Levante UD–Rayo Vallecano de Madrid 1–1 (L61); Athletic Club–RCD Mallorca 2–0 (L62). Latest 2021-12-21: Villarreal CF–Deportivo Alavés 5–2 (L309); Sevilla FC–FC Barcelona 1–1 (L310).
- **S18 — 2021/2022, round 9**: earliest 2021-10-16: Levante UD–Getafe CF 0–0 (L140); Real Sociedad de Fútbol–RCD Mallorca 1–0 (L141). Latest 2021-12-22: Granada CF–Club Atlético de Madrid 2–1 (L315).
- **S19 — 2021/2022, round 21**: earliest 2021-12-22: Athletic Club–Real Madrid CF 1–2 (L320). Latest 2022-04-24: FC Barcelona–Rayo Vallecano de Madrid 0–1 (L580).
- **S20 — 2022/2023, round 17**: earliest 2023-01-13: RC Celta de Vigo–Villarreal CF 1–1 (L278). Latest 2023-02-02: Real Madrid CF–Valencia CF 2–0 (L329).
- **S21 — 2023/2024, round 4**: earliest 2023-09-01: Cádiz CF–Villarreal CF 3–1 (L62); UD Almería–RC Celta de Vigo 2–3 (L63). Latest 2023-12-23: Club Atlético de Madrid–Sevilla FC 1–0 (L314).
- **S22 — 2023/2024, round 13**: earliest 2023-11-10: Athletic Club–RC Celta de Vigo 4–3 (L210). Latest 2023-11-29: RCD Mallorca–Cádiz CF 1–1 (L242).
- **S23 — 2023/2024, round 20**: earliest 2024-01-12: Sevilla FC–Deportivo Alavés 2–3 (L335). Latest 2024-02-01: Getafe CF–Real Madrid CF 0–2 (L385).
- **S24 — 2023/2024, round 26**: earliest 2024-02-23: Real Sociedad de Fútbol–Villarreal CF 1–3 (L441). Latest 2024-04-04: Granada CF–Valencia CF 0–1 (L524).
- **S25 — 2024/2025, round 3**: earliest 2024-08-26: Villarreal CF–RC Celta de Vigo 4–3 (L45). Latest 2024-09-18: Real Betis Balompié–Getafe CF 2–1 (L98).
- **S26 — 2024/2025, round 12**: earliest 2024-11-01: Deportivo Alavés–RCD Mallorca 1–0 (L206). Latest 2025-01-03: Valencia CF–Real Madrid CF 1–2 (L335).
- **S27 — 2024/2025, round 13**: earliest 2024-11-08: Rayo Vallecano de Madrid–UD Las Palmas 1–3 (L221). Latest 2024-12-18: RCD Espanyol de Barcelona–Valencia CF 1–1 (L314).
- **S28 — 2024/2025, round 19**: earliest 2024-12-03: RCD Mallorca–FC Barcelona 1–5 (L269). Latest 2025-01-13: Real Sociedad de Fútbol–Villarreal CF 1–0 (L350).
- **S29 — 2024/2025, round 26**: earliest 2025-02-28: Real Valladolid CF–UD Las Palmas 1–1 (L457). Latest 2025-04-27: Villarreal CF–RCD Espanyol de Barcelona 1–0 (L591).
- **S30 — 2024/2025, round 27**: earliest 2025-03-08: RC Celta de Vigo–CD Leganés 2–1 (L472); Deportivo Alavés–Villarreal CF 1–0 (L473); Valencia CF–Real Valladolid CF 2–1 (L474). Latest 2025-03-27: FC Barcelona–CA Osasuna 3–0 (L503).
- **S31 — 2025/2026, round 6**: earliest 2025-08-27: RC Celta–Real Betis 1–1 (L70). Latest 2025-09-25: CA Osasuna–Elche CF 1–1 (L180); Real Oviedo–Barcelona 1–3 (L182).
- **S32 — 2025/2026, round 19**: earliest 2025-12-02: Barcelona–Atlético de Madrid 3–1 (L420). Latest 2026-01-12: Sevilla–RC Celta 0–1 (L557).
- **S33 — 2025/2026, round 16**: earliest 2025-12-12: Real Sociedad–Girona FC 1–2 (L455). Latest 2026-02-18: Levante UD–Villarreal 0–1 (L713).
- **S34 — 2025/2026, round 23**: earliest 2026-02-06: RC Celta–CA Osasuna 1–2 (L654). Latest 2026-03-04: Rayo Vallecano–Real Oviedo 3–0 (L780).

## Additional fixture and identity findings

**Real Madrid–Rayo Vallecano, 20 December 2015: 10–2.** OpenFootball 2015/16
line 259. This triggers a transparent score-plausibility threshold of ten goals
for one team; FT and halftime are consistent and the acquired historical source
agrees. It is not an error or exclusion. It belongs to S04, so it adds no new
fixture to the 340 flagged-round records.

Two prior source-discovery leads are bound to exact stored records but were not
newly accessed or certified during Phase 4:

| Stored record | Source binding | Reason for Phase 5 |
|---|---|---|
| Real Madrid–Real Sociedad, 2005-01-05, 2–1 | Historical CSV L19526, 2004/05 | Earlier discovery described a December interruption and January continuation; establish original/continuation dates and archival-date policy. |
| Granada CF–Athletic Club, 2023-12-11, 1–1 | OpenFootball 2023/24 L275 | Earlier RFEF discovery described continuation from minute 17; establish event/date semantics and final status. |

Lead URLs (not newly consulted evidence in this phase):
- https://as.com/futbol/2004/12/13/mas_futbol/1102892401_850215.html
- https://rfef.es/es/noticias/el-granada-athletic-se-reanudara-este-lunes-las-21-horas

The sources provide no explicit selected-record award/resumption annotations.
Absence of notes is not evidence that every match was an ordinary uninterrupted
90-minute fixture. Existing out-of-scope administrative/annulment notes remain
unchanged; they do not justify altering records in the approved window.

## Source windows, diagnostic names and older stages

The selected primary split remains historical CSV 1990/91–2011/12 and
OpenFootball 2012/13–2025/26. Nothing was merged. The historical original also
contains later seasons; these already acquired rows were used only for comparisons.

All **4,940** overlapping 2012/13–2024/25 fixtures agree on dates and full-time
goals after explicit per-season bijective diagnostic name mappings. The 2012/13
380-match result and its five original differing aliases are preserved exactly:
Athletic Club/Bilbao, Atlético/Atletico Madrid, Coruña/Coruna, Málaga/Malaga CF,
and RC Celta/Celta Vigo. No dates, scores or team labels were replaced.

Expanded comparisons expose source spelling/style variants, including club
prefixes and suffixes. The assessment records **18 diagnostic label-variant
groups**, the complete label/season catalog and all 35 consecutive-season label
change lists. These are spelling/identity review aids, not confirmed legal-entity
continuity or a comprehensive canonical club system. Promotions/relegations and
re-founded clubs must not be equated with mere renaming. No within-season
normalized-label collision was detected.

The historical **90 phase2 rows from 1986/87** remain outside the selected scope.
The entire historical original, its older result notes and all Phase 2/3
receipts/manifests remain unchanged. Agreement between these compilers does not
establish historically independent lineage.

## Explicit Phase 5 queue

1. Resolve S01–S34 using independent dated records, original schedules and, where
   applicable, federation decisions. Prioritize the 52 reference-window outliers
   while retaining all 340 round fixtures as context; distinguish advanced,
   postponed and resumed fixtures without assuming a cause from dates alone.
2. Verify the two bound interruption/resumption leads and determine archive-date
   versus actual-event semantics before proposing any derivative correction.
3. Independently verify the 2015 10–2 score rather than treating the threshold
   as proof of error. It is already counted within S04.
4. Review season-specific club identities, the 18 label groups and source lineage;
   do not infer legal continuity from diagnostic name equivalence.
5. Perform a reproducible cross-era/per-season independent match sample and
   targeted exceptional-result investigation across all 36 seasons. Unlisted
   matches remain historically unverified; 342 focused queue records are not
   the only records requiring eventual confidence assessment.

## Files, preservation and reproduction

Created:
- `scripts/validate_la_liga_structure.py` — offline independent structural validator.
- `tests/test_la_liga_structure.py` — focused synthetic guard tests.
- `docs/la-liga-validation.md` — this report.
- `data/private/spain/la_liga/phase4_protected_before.json` — 52-file Phase 2/3 baseline.
- `data/private/spain/la_liga/phase4_structural_validation.json` — reproducible assessment,
  all candidate details, source comparisons, names, counts and frozen input/code hashes.

Modified: `PLANNING_LOG.md`, appended approval, implementation choices and measured
results only. No existing Phase 2/3 code, tests, report or private artifact changed.

All **428** previous-competition artifacts and **52** Phase 2/3 artifacts remain
byte-identical; the frozen Phase 2 subset of 19 artifacts also passes. No application
or promotional-worktree files changed. Private artifacts remain Git-ignored.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -B -m scripts.validate_la_liga_structure --check
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -B -m scripts.inventory_la_liga_history --check
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -B -m scripts.validate_la_liga_feasibility --check
```

The validator has no network path, refuses existing output on default creation
and compares complete regenerated bytes under `--check`. A changed protected
source/evidence file fails before parsing. Inputs and validation/test code are
fingerprinted. Real-data reproduction requires the retained private bundle;
synthetic tests use no historical datasets or network.

Licence restrictions remain unchanged: engsoccerdata noncommercial/GPL-scope and
upstream model-training rights are unresolved; OpenFootball CC0 covers rights
held without clearing third-party rights. No statistical model training, public
dataset hosting or redistribution permission is inferred.

No acquisition, factual correction, match exclusion, standardization, application
integration, model training, commit, push or merge occurred. Stop for review.

## Executed verification results

- **35 new Phase 4 tests** plus 30 existing La Liga tests and 60 Serie A/Serie B
  adapter regression tests: **125 passed**.
- Broader repository suite excluding `tests/test_app.py` and
  `tests/test_launcher.py`: **712 passed in 32.58 seconds**.
- Full-suite attempt: **timed out after 90 seconds**, without a completed result.
  A separate 15-second diagnostic stalled in `importlib.get_data` while loading
  `streamlit/runtime/app_session.py`. The seven app/launcher tests are therefore
  **UNVERIFIED in this phase**, not reported as passing. No dependency was installed
  or modified to bypass the issue.
- Phase 4 structural assessment, Phase 3 inventory and Phase 2 feasibility
  assessment all regenerate **byte-identically**.
- All frozen input, original-source, acquisition/evidence and validation/test-code
  hashes match. All 428 previous-competition artifacts, 19 frozen Phase 2 artifacts
  and 52 complete Phase 2/3 artifacts remain unchanged.
- All **475 current private files** are ignored and none tracked; the La Liga
  directory contains 46 private artifacts, exactly two more than Phase 3.
- `git diff --check` passes. Nothing is staged; HEAD and branch are unchanged.
