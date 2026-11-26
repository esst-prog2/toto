# Belgian Pro League — Phase 4 independent structural validation

Measured 2026-11-25. **PASSED for structural accounting and source preservation.** This is not historical certification, final stage eligibility, administrative adjudication or model-training clearance. Known source defects and incomplete coverage remain explicit.

## Scope and starting state

Original toto worktree; branch `feature/data-collection`; local HEAD and independently queried remote branch `013bb9c195624d5ac290aeb57dae11c4e21c0b5a`. The expected Phase 2–3 uncommitted work was present, plus `.DS_Store` and `data/.DS_Store`; nothing staged. No acquisition or network research was performed during validation.

Protected baselines cover the twelve completed competitions (137,189 screened records), 1,415 prior private files, 250 prior public files and 57 frozen Belgian Phase 2–3 private/public entries. The full planning-log prefix and Git index are protected separately. The application, promotional worktree and original environment were not modified.

## Independent implementation

`scripts/validate_belgian_pro_league_structure.py` implements its own CSV reader, TXT grammar/date resolver, field checks, stage/round/group assessments, documentary exception parser, source-bound correspondence inference and review-queue reconstruction. It imports no earlier Belgian parser, assessor, overlap resolver or queue builder. Existing acquisition helpers are used only by preservation checks. Saved Phase 3 artifacts are comparison targets after reconstruction, not inputs driving counts or links.

Team-label inference uses recorded date/home-away participation patterns only, excluding goals. Unique season-bound one-to-one candidates are then checked against original participants, dates and scores. Consequently score agreement cannot be manufactured by including scores in the identity inference. Ambiguities are retained rather than globally normalizing labels. Agreement remains source reconciliation, not genuinely independent historical evidence.

For every CSV/TXT observation the independent parser reproduces original source SHA-256, physical line range, raw-record SHA-256, season, date, home/away strings, scores, annotations, stage, round/group/leg and stable source-observation identity. CSV original fields and TXT date-heading line bindings are checked separately against Phase 3. No final match IDs or standardized records are created.

## Independently reconstructed populations

| Population | Measured |
|---|---:|
| conditional_events | 8698 |
| conditional_review_entries | 897 |
| documentary_only_review_entries | 30 |
| historical | 8394 |
| matched_pairs | 1402 |
| modern | 1706 |
| observations | 10100 |
| review_entries | 927 |
| scored | 9973 |
| unscored | 127 |
| wide_round_contexts | 15 |

All expected counts match. Every matched pair preserves both source representations, and every legitimate additional-stage rematch remains a distinct conditional event. The 30 documentary-only RSSSF exception entries are outside the 10,100 CSV/TXT population and its 8,698-event union. There are no detected invalid fields, duplicate stage/date identities, dropped observations or reused cross-source links.

## Historical validation and complete 36-season matrix

The CSV has exactly twelve columns: `Date,Season,home,visitor,FT,hgoal,vgoal,division,tier,totgoal,goaldif,result`; division B1, tier 1. All 8,394 records have usable source dates and full-time scores consistent with total goals, goal difference and H/D/A outcome. There are 30 consecutive represented seasons, 1995/96–2024/25. All historical stage fields remain UNKNOWN; diagnostic stage correspondence does not overwrite a source field.

Nominal expectations are not accepted-record totals. Administrative and COVID deficits remain separate from malformed/missing-source observations. In modern sources every explicitly represented regular/group stage has the required participant count, rounds and complete directed pairings, with no repeated club inside a round. Qualifiers are checked separately from home-and-away groups.

| Season | Nominal clubs/regular slots | H observations/clubs | H scored/unscored | Modern declared content |
|---|---|---|---|---|
| 1990/1991 | 18/306 | — | — | — |
| 1991/1992 | 18/306 | — | — | — |
| 1992/1993 | 18/306 | — | — | — |
| 1993/1994 | 18/306 | — | — | — |
| 1994/1995 | 18/306 | — | — | — |
| 1995/1996 | 18/306 | 306/18 | 306/0 | — |
| 1996/1997 | 18/306 | 306/18 | 306/0 | — |
| 1997/1998 | 18/306 | 306/18 | 306/0 | — |
| 1998/1999 | 18/306 | 306/18 | 306/0 | — |
| 1999/2000 | 18/306 | 306/18 | 306/0 | — |
| 2000/2001 | 18/306 | 306/18 | 306/0 | — |
| 2001/2002 | 18/306 | 306/18 | 306/0 | — |
| 2002/2003 | 18/306 | 272/17 | 272/0 | — |
| 2003/2004 | 18/306 | 306/18 | 306/0 | — |
| 2004/2005 | 18/306 | 306/18 | 306/0 | — |
| 2005/2006 | 18/306 | 306/18 | 306/0 | — |
| 2006/2007 | 18/306 | 306/18 | 306/0 | — |
| 2007/2008 | 18/306 | 306/18 | 306/0 | — |
| 2008/2009 | 18/306 | 306/18 | 306/0 | — |
| 2009/2010 | 16/240 | 210/15 | 210/0 | — |
| 2010/2011 | 16/240 | 240/16 | 240/0 | — |
| 2011/2012 | 16/240 | 240/16 | 240/0 | — |
| 2012/2013 | 16/240 | 240/16 | 240/0 | — |
| 2013/2014 | 16/240 | 240/16 | 240/0 | — |
| 2014/2015 | 16/240 | 240/16 | 240/0 | — |
| 2015/2016 | 16/240 | 240/16 | 240/0 | — |
| 2016/2017 | 16/240 | 240/16 | 240/0 | — |
| 2017/2018 | 16/240 | 240/16 | 240/0 | — |
| 2018/2019 | 16/240 | 240/16 | 240/0 | 2018-19/be1.txt: 270/0 scored/unscored |
| 2019/2020 | 16/240 | 232/16 | 232/0 | 2019-20/be1.txt: 232/8 scored/unscored |
| 2020/2021 | 18/306 | 306/18 | 306/0 | 2021-22/be1.txt: 330/0 scored/unscored |
| 2021/2022 | 18/306 | 306/18 | 306/0 | No actual modern 2021/22 counterpart |
| 2022/2023 | 18/306 | 306/18 | 306/0 | — |
| 2023/2024 | 16/240 | 312/16 | 312/0 | 2023-24/be1.txt: 313/0 scored/unscored |
| 2024/2025 | 16/240 | 312/16 | 312/0 | 2024-25/be1.txt: 313/0 scored/unscored |
| 2025/2026 | 16/240 | — | — | 2025-26/be1.txt: 121/119 scored/unscored |

The five early seasons 1990/91–1994/95 still have no acquired dated fixture source. RSSSF 1992/93 standings are not a dated 306-event population. The incomplete 2025/26 snapshot and actual modern 2021/22 gap remain open. No missing slot is classified as NOT PLAYED.

Historical pairing results: ordinary represented seasons through 2022/23 have each directed pairing once among their observed participants, except 2019/20 with eight absent pairings. Lommel 2002/03 and Mouscron 2009/10 use 17- and 15-club retained graphs without reconstructing removed fixtures. Both endpoint seasons have a complete 240-pair prefix plus 72 additional observations. Additional records are retained, not discarded as duplicates.

## Modern stage validation

| Original path | Actual declared season | Regular | Championship | Europe | Playdowns | Qualifier | Scored/unscored |
|---|---|---:|---:|---:|---:|---:|---|
| 2018-19/be1.txt | 2018/2019 | 240 | 30 | 0 | 0 | 0 | 270/0 |
| 2019-20/be1.txt | 2019/2020 | 240 | 0 | 0 | 0 | 0 | 232/8 |
| 2021-22/be1.txt | 2020/2021 | 306 | 12 | 12 | 0 | 0 | 330/0 |
| 2023-24/be1.txt | 2023/2024 | 240 | 30 | 30 | 12 | 1 | 313/0 |
| 2024-25/be1.txt | 2024/2025 | 240 | 30 | 30 | 12 | 1 | 313/0 |
| 2025-26/be1.txt | 2025/2026 | 240 | 0 | 0 | 0 | 0 | 121/119 |

### Source defect: misplaced 2020/21 payload

`2021-22/be1.txt` remains at its original immutable path and matches its approved Git blob. Its title, explicit 2020-08-08 opening date, participant set, 34 regular rounds and 306 historical 2020/21 correspondences independently establish its declared content. Its final source date is in May 2021. The 24 remaining observations are 12 championship and 12 Europe fixtures.

All 330 observations are attributed only to declared 2020/21; requested season/path 2021/22 remain visible in the permanent exception registry. No actual modern 2021/22 overlap is claimed. No renaming, replacement or reacquisition occurred. This source defect is contained by the inventory; it is not a new parser defect or an approved correction.

## Independent overlap validation

| Declared season | H/O | Matched | Date/score disagreements | Unmatched modern |
|---|---|---:|---|---|
| 2018/2019 | 240/270 | 240 | 0/0 | 30 |
| 2019/2020 | 232/240 | 232 | 0/0 | 8 |
| 2020/2021 | 306/330 | 306 | 0/0 | 24 |
| 2023/2024 | 312/313 | 312 | 0/0 | 1 |
| 2024/2025 | 312/313 | 312 | 0/0 | 1 |

The independent link set is exactly the frozen Phase 3 link set: 1,402 pairs, zero date/score disagreements and no unmatched historical observation in the five comparable seasons. Unmatched modern populations: 30 championship (2018/19), eight cancelled slots (2019/20), 24 playoffs (declared 2020/21), one awarded Europe observation (2023/24), one qualifier (2024/25). The 2025/26 original has no historical counterpart.

2023/24 historical correspondence: 240 regular + 30 championship + 29 Europe + 12 playdown + 1 qualifier. Modern has the same plus one Europe observation: Standard Liège–KVC Westerlo, 2024-05-10, 0-5 [awarded], Europe round 8, physical line 573.

2024/25 historical correspondence: 240 regular + 30 championship + 30 Europe + 12 playdown. The modern source adds Antwerp–Charleroi, 2025-05-29, 1-2, European qualifier, line 507. The two historical stage compositions are demonstrably different.

## Exceptions and documentary accounting

- **Lommel 2002/03:** 272 scored CSV observations, 17 literal club labels; Lommel absent. The source cannot reconstruct played/annulled/awarded/unplayed missing events. No final historical disposition is assigned.
- **Mouscron 2009/10:** 210 scored CSV observations, 15 labels; Mouscron absent. Independent RSSSF extraction yields 240 regular documentary slots: 210 non-Mouscron results, 18 annulled numeric Mouscron results, two annulled awards and ten n/p representations. These stay separate from CSV/TXT events.
- **2019/20:** 232 scored historical results and 232 scored modern results, plus eight explicit cancelled source slots. They are not annulled played results.
- **2018/19 award:** Standard–Anderlecht, 2019-04-12, 5-0 [awarded], championship round 4, line 454.
- **2023/24 award:** Standard–Westerlo, 2024-05-10, 0-5 [awarded], Europe round 8, line 573.
- **2025/26:** 240 regular slots, 121 scored, 119 unscored, no postseason section. The frozen snapshot is not a complete historical season. No supplementary results were fetched.

Exact 2019/20 cancelled bindings follow. Every row has source heading 2020-03-15, round 30, no FT score and literal [cancelled]; the date is scheduled context, not certified actual completion/decision/availability.

| Source line | Home | Away |
|---:|---|---|
| 417 | KRC Genk | KV Mechelen |
| 418 | KAS Eupen | Club Brugge KV |
| 419 | SV Zulte Waregem | Standard Liège |
| 420 | Cercle Brugge | KV Oostende |
| 421 | Sporting Charleroi | KV Kortrijk |
| 422 | Royal Antwerp FC | Royal Excel Mouscron |
| 423 | Waasland-Beveren | KAA Gent |
| 424 | Sint-Truidense VV | RSC Anderlecht |

## Queue and scheduling validation

Every Phase 3 event/category membership, underlying per-observation flag, retained source binding, score/annotation and wide-round context was checked against independent reconstruction. Membership is identical: **927 entries = 897 conditional match groups + 30 documentary-only exceptions**. Categories overlap and must not be summed.

| Category | Deduplicated memberships |
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

The 15 independent wide-round contexts are:

| Original path | Stage / round | Earliest | Latest | Span days |
|---|---|---|---|---:|
| 2019-20/be1.txt | REGULAR_SEASON / 23 | 2020-01-24 | 2020-02-11 | 18 |
| 2019-20/be1.txt | REGULAR_SEASON / 5 | 2019-08-23 | 2020-01-29 | 159 |
| 2021-22/be1.txt | REGULAR_SEASON / 10 | 2020-10-23 | 2020-12-03 | 41 |
| 2021-22/be1.txt | REGULAR_SEASON / 11 | 2020-10-30 | 2020-12-01 | 32 |
| 2021-22/be1.txt | REGULAR_SEASON / 12 | 2020-11-06 | 2020-12-08 | 32 |
| 2021-22/be1.txt | REGULAR_SEASON / 16 | 2020-12-11 | 2020-12-29 | 18 |
| 2021-22/be1.txt | REGULAR_SEASON / 17 | 2020-12-18 | 2021-01-13 | 26 |
| 2021-22/be1.txt | REGULAR_SEASON / 18 | 2020-12-15 | 2021-01-06 | 22 |
| 2021-22/be1.txt | REGULAR_SEASON / 26 | 2021-02-12 | 2021-03-12 | 28 |
| 2021-22/be1.txt | REGULAR_SEASON / 28 | 2021-02-26 | 2021-03-15 | 17 |
| 2021-22/be1.txt | REGULAR_SEASON / 31 | 2021-03-19 | 2021-04-07 | 19 |
| 2021-22/be1.txt | REGULAR_SEASON / 9 | 2020-10-17 | 2020-11-24 | 38 |
| 2023-24/be1.txt | REGULAR_SEASON / 5 | 2023-08-26 | 2023-09-28 | 33 |
| 2024-25/be1.txt | REGULAR_SEASON / 5 | 2024-08-24 | 2024-09-26 | 33 |
| 2025-26/be1.txt | REGULAR_SEASON / 5 | 2025-08-23 | 2025-09-24 | 32 |

These contexts have 130 event memberships. Modern source ordering has 22 adjacent reversals: five cross-stage block transitions and 17 within-stage reversals. Their 44 review memberships are not 44 distinct confirmed postponements. Five reversals have an immediate stage-block ordering explanation; the remaining recorded order does not independently establish actual rescheduling or interruption. No parser-created date or round error was found in the frozen observations.

Literal club identities, bilingual variants and legal continuity remain unresolved where relevant. No global Beerschot/Germinal, Mouscron, RWDM/Molenbeek, Genk predecessor, Kortrijk/Courtrai or Sint-Truiden/Saint-Trond mapping is created. The independent date/side correspondences are local diagnostics only.

## Shared schema compatibility

The eight-column output schema remains unchanged: `match_id,date,league,season,home_team,away_team,home_goals,away_goals`. The common importer identity input is league/season/date/home/away; inspection found no same-source season/date/home/away collision in any of the seven match originals. Different-date playoff rematches therefore remain distinguishable before IDs, but pair-only import guards must not be reused to discard them. Stage/group/round/leg remains necessary private audit metadata. No final match-ID hashes were generated.

## Reproduction and environment

Six Phase 4 assessments plus a reproducibility manifest regenerate in a separate bounded Python process into temporary storage and match all seven saved artifacts byte-for-byte and by SHA-256. Original bytes and all frozen Phase 2–3 artifacts remain unchanged. Preservation verification runs with network calls forbidden. Commands:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m scripts.validate_belgian_pro_league_structure
PYTHONDONTWRITEBYTECODE=1 python3 -m scripts.validate_belgian_pro_league_structure --verify
```

The previous external environment was incomplete (missing pyvenv.cfg and empty pytest directory). A read-only project-environment pytest attempt timed out after 45 seconds; a separate 15-second import trace showed roughly 1.2–1.5 seconds in several individual pytest module imports. This supports path-associated import latency, not a proven root cause or a test pass.

A fresh offline environment was created at `/private/tmp/belgium-phase4-env-xgpvyf0n/venv`. Its 6,200 package files were copied from the existing project installation and verified byte-identical. No network installation, upgrade or original-environment modification occurred. Versions: CPython3.13.12, pytest9.1.1, NumPy2.5.3, pandas3.0.6, Streamlit1.64.0, Jinja2 3.1.6. Bytecode, automatic plugin loading and pytest-cache writes were disabled for testing.

| Fresh selection (overlapping; do not sum) | Passed | Failed/errors/skipped |
|---|---:|---|
| new | 61 | 0/0/0 |
| belgian | 144 | 0/0/0 |
| acquisition_importer | 564 | 0/0/0 |
| non_ui | 2298 | 0/0/0 |
| app_launcher | 7 | 0/0/0 |
| full | 2305 | 0/0/0 |

New synthetic tests challenge original-field contradictions, malformed schemas, source checksums, precise line bindings, weekday/year resolution, actual versus requested season, stage-specific club/round rules, rematches, duplicate identities, group/pair gaps, score-independent identity inference, halftime consistency and distinct annulment/award/unplayed documentary tokens. The two import timeouts are recorded as unsuccessful execution attempts; all final requested selections subsequently passed in the offline environment.

## Historical research agenda for Phase 5 — not started

1. Obtain authoritative disciplinary decisions and appeal/finality chronology for Standard–Anderlecht 2019 and Standard–Westerlo 2024. Separate on-pitch events, awards and result-availability dates.
2. Independently establish official season/fixture identities behind the wrong-season source; retain its original path. Research a real modern 2021/22 source only under separate acquisition approval.
3. Investigate Lommel 2002/03 and Mouscron 2009/10 legal outcomes and annulment/award timing, preserving played-versus-unplayed distinctions.
4. Verify Belgian COVID termination and the final status/date semantics of the eight cancelled slots using official evidence, without adopting another country’s policy.
5. Verify the endpoint missing award/qualifier and all 15 scheduling contexts, prioritizing diagnostic long spans and any interrupted/completed-match chronology. A round explanation does not certify every fixture.
6. Review season-bound club registration/name histories and perform reproducible independent historical sampling across represented seasons. Do not treat overlap agreement between potentially related statistical sources as independent confirmation.
7. Keep the five early dated-season gaps, incomplete 2025/26, actual modern 2021/22 absence and rights/provenance gaps visible. Additional datasets or replacement originals require separate approval.

## Conclusion and boundaries

**Phase 4 PASSED.** Zero material structural-parser or reconciliation defects were found in the preserved population. The wrong-season original is a confirmed, contained source defect; source omissions, administrative results and historical/chronological uncertainties remain unresolved, not silently corrected.

Technical acceptance, historical verification, stage eligibility, redistribution and model-training permission remain separate. engsoccerdata later Football-Data lineage is not independent proof or a rights workaround; OpenFootball CC0 does not warrant upstream clearance; RSSSF attribution permission is not blanket model-training clearance. No final stage inclusion, HOLD OUT/NOT PLAYED disposition, award acceptance, correction, standardization, application integration, training, staging, commit, push, merge or Phase 5 work occurred.
