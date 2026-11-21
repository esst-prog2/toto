# Serie B acquisition and structural validation

Audit date: 2026-11-12. Branch: `feature/data-collection`; starting commit `95f0a728d965cc1e02458c7754e64436db6e8fcc`.

## Outcome and scope

Originals were acquired for all **36** target seasons, 1990/91–2025/26. The explicit selected-source set contains **14,962 regular-season fixture entries**, of which **14,961 have numeric final scores**. This is not a claim of 14,962 fully dated, verified match results.

There are **29 seasons / 12,302 records with source match dates and final scores**, including 2003/04 whose CSV has an unresolved extra-column warning. Six early seasons have **2,280 undated entries**. The remaining early season, 1995/96, has **380 round-level dates of uncertain individual-match applicability**, and one missing final score. No dates, scores or team identities were repaired. Complete and accurate independent result verification has not yet occurred.

**28 seasons pass all current structural/source checks; 3 have complete undated pairing/score structures; 5 require review.** A structural pass does not certify an ordinary played 90-minute result, final judicial status, exact date accuracy, independent lineage, or training eligibility.

No standardized Serie B dataset, match IDs, club-identity system, integration or model work was produced. No 2026/27 match file was acquired. The five existing standardized competitions remain outside scope.

## Historical format and primary evidence

Expected regular-season fixtures are `n × (n−1)`; tie-breaks and promotion/relegation postseason fixtures are additional and excluded.

| Seasons | Clubs | Fixtures per season | Basis |
|---|---:|---:|---|
| 1990/91–2002/03 | 20 | 380 | RSSSF final tables/result structures for the first seven; dated Football-Data pairing coverage thereafter; UEFA describes subsequent expansion from 20. |
| 2003/04 | 24 | 552 | [UEFA contemporary expansion report](https://www.uefa.com/news-media/news/0194-0f8edd00fe3c-366c9a7529d7-1000--fiorentina-gain-from-expansion/), complete 24-club source pairings. |
| 2004/05–2017/18 | 22 | 462 | [FC Crotone historical overview](https://www.fccrotone.it/news/lega-serie-b-info-curiosita-storia-statistiche-pillole/) identifies the run from 2004; each acquired season has 22 clubs and all ordered pairings. |
| 2018/19 | 19 | 342 | [Administrative court summary of reduction from 22 to 19](https://www.giustizia-amministrativa.it/web/guest/-/riduzione-da-22-a-19-squadre-dell-organico-del-campionato-di-serie-b-2018-2019), source 19-club coverage; 38 matchdays with byes, 36 games per club. |
| 2019/20–2025/26 | 20 | 380 | [FIGC decision returning the league to 20 clubs](https://www.figc.it/it/federazione/news/il-consiglio-federale-da-il-via-alla-riforma-dei-campionati-dal-2019-20-la-serie-b-a-20-squadre-sc5mrekd), supported by each source's pairing inventory. |

The total expected regular-season inventory is **14,962** (13×380 + 552 + 14×462 + 342 + 7×380). The 2019/20 bounds explicitly allow COVID-delayed matches through August 2020. Points deductions, club demotions and admission litigation do not automatically change the expected fixture inventory or authorize replacing source scores.

## Source selection and actual coverage

- **R — RSSSF:** seven whole-country original HTML documents, `ital91.html` through `ital97.html`, for 1990/91–1996/97. Only their explicitly bounded Serie B section is counted. Other divisions remain in the unchanged original but are not included in the audit inventory. 1990/91–1994/95 use paired first/return stages; 1995/96 has rounds and dates; 1996/97 uses a complete result matrix. Exact match dates are absent for six seasons. Authors and acknowledgements, including Maurizio Mariani, Misha Miladinovich and Sorin Arotaritei where credited, remain in each original and its retained Serie B context.
- **F — Football-Data:** [Italy download index](https://www.football-data.co.uk/italym.php) advertises Serie B from 1997/98 through 2025/26. Acquired I2 CSVs for **1997/98–2012/13 plus 2025/26**: 17 selected seasons. Only inspected completed-season URLs were requested. Intermediate advertised years were not downloaded a second time; this is advertised coverage, not independently tested completeness of those unacquired CSVs. Required fields are Div, Date, HomeTeam, AwayTeam, FTHG, FTAG and FTR; betting/half-time columns are not required. These files contain exactly the expected regular-season pairings and no additional postseason rows.
- **O — OpenFootball:** [commit-pinned repository](https://github.com/openfootball/italy/tree/48954d163c312aa705efacb64f771267031fe6eb) contains `2-serieb.txt` for 2013/14–2025/26; no earlier Serie B originals were present in the inspected tree. All 13 files were acquired; 12 seasons, **2013/14–2024/25**, were selected. Full snapshot revision: `48954d163c312aa705efacb64f771267031fe6eb`. Source stages delimit postseason fixtures.

The OpenFootball 2025/26 candidate lists 380 fixtures but only **309 scores**, leaving **71 unscored entries**. Its scheduled dates are not certified actual playing dates. The complete 380-result Football-Data alternative was selected for the entire season using `selection.json`. Both originals remain unchanged. No fixture-level merge or score/date correction was performed. There are **37 acquired season files**, representing 36 selected seasons plus one duplicate-season candidate, not 37 distinct seasons.

Earlier dated alternatives were investigated, including [Adamoli's 1990/91 almanac](https://www.adamoli.org/almanacco/serie-b-1990-1991-home.html). Its round-by-round pages are not a directly inspected bulk dataset with an established copying grant; they were not crawled. [AIDb's Serie B description](https://aidb.si/d/serie-b-results) points to OpenFootball from 2013/14 and therefore does not fill early gaps or constitute independent evidence. RSSSF and other archives may share contributors; Football-Data acknowledges external score services. Cross-source independence must be established during verification, not assumed from different websites.

## Season-by-season selected inventory

`PASS` = counts, names as supplied, ordered home/away pairing coverage, dates, numeric scores and applicable source checks pass. `UNDATED` = pairing/score structure passes but exact dates are absent. `REVIEW` includes the limitation in the final column. Counts include exceptional regular-season entries and exclude postseason. A source pass is not independent certification.

| Season | Source | Clubs observed / expected | Entries / expected | Scored | Exact source dates | Status / limitation |
|---|---|---:|---:|---:|---:|---|
| 1990/1991 | R | 21 / 20 | 380 / 380 | 380 | 0 | REVIEW: Parma label in a paired row; no dates; internal total discrepancy |
| 1991/1992 | R | 20 / 20 | 380 / 380 | 380 | 0 | UNDATED |
| 1992/1993 | R | 20 / 20 | 380 / 380 | 380 | 0 | REVIEW: no dates; five club goal-total disagreements |
| 1993/1994 | R | 20 / 20 | 380 / 380 | 380 | 0 | UNDATED; asterisks extracted as footnote markers; awarded fixture retained |
| 1994/1995 | R | 20 / 20 | 380 / 380 | 380 | 0 | REVIEW: no dates; four club goal-total disagreements |
| 1995/1996 | R | 20 / 20 | 380 / 380 | 379 | 0 | REVIEW: 380 round dates only; one abandoned entry has no final score |
| 1996/1997 | R | 20 / 20 | 380 / 380 | 380 | 0 | UNDATED; matrix abbreviations retained |
| 1997/1998 | F | 20 / 20 | 380 / 380 | 380 | 380 | PASS |
| 1998/1999 | F | 20 / 20 | 380 / 380 | 380 | 380 | PASS |
| 1999/2000 | F | 20 / 20 | 380 / 380 | 380 | 380 | PASS |
| 2000/2001 | F | 20 / 20 | 380 / 380 | 380 | 380 | PASS |
| 2001/2002 | F | 20 / 20 | 380 / 380 | 380 | 380 | PASS |
| 2002/2003 | F | 20 / 20 | 380 / 380 | 380 | 380 | PASS |
| 2003/2004 | F | 24 / 24 | 552 / 552 | 552 | 552 | REVIEW: four rows have nonempty unheaded extra CSV fields |
| 2004/2005 | F | 22 / 22 | 462 / 462 | 462 | 462 | PASS |
| 2005/2006 | F | 22 / 22 | 462 / 462 | 462 | 462 | PASS |
| 2006/2007 | F | 22 / 22 | 462 / 462 | 462 | 462 | PASS |
| 2007/2008 | F | 22 / 22 | 462 / 462 | 462 | 462 | PASS |
| 2008/2009 | F | 22 / 22 | 462 / 462 | 462 | 462 | PASS |
| 2009/2010 | F | 22 / 22 | 462 / 462 | 462 | 462 | PASS |
| 2010/2011 | F | 22 / 22 | 462 / 462 | 462 | 462 | PASS |
| 2011/2012 | F | 22 / 22 | 462 / 462 | 462 | 462 | PASS |
| 2012/2013 | F | 22 / 22 | 462 / 462 | 462 | 462 | PASS |
| 2013/2014 | O | 22 / 22 | 462 / 462 | 462 | 462 | PASS |
| 2014/2015 | O | 22 / 22 | 462 / 462 | 462 | 462 | PASS |
| 2015/2016 | O | 22 / 22 | 462 / 462 | 462 | 462 | PASS |
| 2016/2017 | O | 22 / 22 | 462 / 462 | 462 | 462 | PASS |
| 2017/2018 | O | 22 / 22 | 462 / 462 | 462 | 462 | PASS |
| 2018/2019 | O | 19 / 19 | 342 / 342 | 342 | 342 | PASS; source administrative 0–3 retained |
| 2019/2020 | O | 20 / 20 | 380 / 380 | 380 | 380 | PASS; COVID extension through July 2020 |
| 2020/2021 | O | 20 / 20 | 380 / 380 | 380 | 380 | PASS; source administrative 3–0 retained |
| 2021/2022 | O | 20 / 20 | 380 / 380 | 380 | 380 | PASS |
| 2022/2023 | O | 20 / 20 | 380 / 380 | 380 | 380 | PASS |
| 2023/2024 | O | 20 / 20 | 380 / 380 | 380 | 380 | PASS |
| 2024/2025 | O | 20 / 20 | 380 / 380 | 380 | 380 | PASS |
| 2025/2026 | F | 20 / 20 | 380 / 380 | 380 | 380 | PASS; whole-season F alternative; O incomplete |

No selected season has duplicate ordered fixtures. All ordered home/away pairings and per-club home/away counts pass except 1990/91 with its unresolved source team label. Missing dates are explicitly null in private diagnostics; round dates carry `source_round_only`, never an invented individual-match date. No arbitrary date placeholders are used.

## Preserved discrepancies and historical names

1. **1990/91:** RSSSF physical line 859 prints `Parma–Brescia` in paired stages 14/33, although the final table and result matrix contain Pescara, not Parma. This creates two diagnostic entries with Parma, leaves Pescara with 18 home/18 away fixtures, and produces 21 observed labels instead of 20. The same document's matrix suggests a transcription problem; it is not independent proof. No team substitution was applied. Pescara's parsed goal totals are 33/31 versus table 36/32; this is consistent with but does not independently resolve the label issue.
2. **1992/93:** paired results disagree with final-table goals for Piacenza, Padova, Cesena, Venezia and Ternana. Neither result rows nor table values were privileged. The exact observed/table totals and source lines are retained in `structural_audit.json`.
3. **1994/95:** paired results disagree with final-table goals for Piacenza, Salernitana, Venezia and Fidelis Andria. The source remains unchanged. These are internal inconsistencies, not yet independently confirmed match-level errors.
4. **1995/96:** all 380 dates are source round headings, not individually labelled playing dates. Round 25 says March 4; search-index results suggest March 3 for Foggia–Salernitana, but no correction is supported by a completed evidence review. The source says `Abd` at 1–3; final goals remain null, even though table arithmetic is consistent with counting that score. The crowd-disturbance annotation continues into the next physical fixture line; full context is retained, and the continuation is not treated as proof that Genoa–Chievo was also abandoned.
5. **2003/04:** four CSV rows have nonempty fields beyond the header, in addition to empty trailing padding on other rows. Required match fields are intact and all 552 fixtures pass structural checks. The unknown extra values are preserved in diagnostics, not reinterpreted as match fields. Empty padding also occurs in 2001/02, 2002/03 and 2004/05 and is recorded separately.
6. **2025/26 alternative:** the OpenFootball missing-score inventory is retained as a candidate original, never counted as additional historical results or filled from the selected CSV.

RSSSF's `Venezia*` and `Brescia *` in 1993/94 have explicit nearby footnotes: respectively an administrative score and a neutral venue. The parser extracts the marker from the club label and retains the original source line plus complete context; this is syntactic footnote parsing, not a club-identity correction. For paired stages the return score is printed in the same team-column orientation as the first score: both teams **and score columns** are reversed when interpreting the return fixture. Final-table goal arithmetic supports this interpretation; residual inconsistencies above are exposed rather than suppressed.

Names remain source-specific: `C.d.Sangro` and `Salernit.` in the 1996/97 matrix, Fidelis Andria/Andria variants, Chievo/Chievo Verona, Verona/Hellas Verona, Reggina versus Reggiana, AlbinoLeffe spellings, and modern corporate prefixes such as SSC Bari, AC Cesena, AC Pisa/Pisa SC, US Palermo/Palermo FC, L.R. Vicenza Virtus and FC Südtirol/Sudtirol. Re-founded entities (including Fiorentina, Bari, Siena, Palermo, Parma and Vicenza) require season-aware manual identity checks before any cross-season reconciliation. No comprehensive mapping or merger of distinct clubs was implemented. All season-specific source labels are listed privately.

## Exceptional regular-season fixtures: review queue

This is a bounded source-annotation and historical-context review, **not an exhaustive independent exception review**, a correction file, or a training-eligibility classification. All seven candidates below remain in the inventory; no default eligibility is assigned to unreviewed matches. Private `review_candidates.json` links each to its source file SHA-256, physical line and original interpreted record.

| Season / fixture | Acquired-source treatment | Evidence and outstanding work |
|---|---|---|
| 1990/91 Barletta–Cosenza | Return-stage score 0–2; `x Tavolino` on the paired line | RSSSF source-only award flag. Establish exact date, on-field events and official ruling independently; do not apply the paired-line marker automatically to both legs. |
| 1993/94 Venezia–Acireale | First-stage awarded 0–2; source explicitly says 2–1 on field | RSSSF source-only. Reason, date and authoritative final decision need verification. |
| 1995/96 Foggia–Salernitana | `Abd`; no numeric final score; source interim score 1–3 | Crowd disturbance note; unresolved recognized result and exact date. Do not convert interim score into a final result. |
| 2002/03 Catania–Siena | CSV 1–1, 2003-04-12 | Full [UEFA expansion article](https://www.uefa.com/news-media/news/0194-0f8edd00fe3c-366c9a7529d7-1000--fiorentina-gain-from-expansion/) reports the eligibility dispute and consequences. Final administrative sequence/result requires the actual decisions; a search-index Senate reference is only a lead. |
| 2004/05 Genoa–Venezia | CSV 3–2, 2005-06-11 | Full [UEFA disciplinary report](https://www.uefa.com/news-media/news/01ab-0e6d13e4770b-b31bda94b665-1000--genoa-to-drop-two-divisions/) supports the played score and fixing-related demotion. A club demotion alone is not evidence of an awarded replacement score. |
| 2018/19 Cosenza–Hellas Verona | OpenFootball 0–3 `[awarded]`, scheduled 2018-09-01 | Full [FIGC appeal report](https://www.figc.it/it/federazione/news/csa-confermata-la-sconfitta-0-3-a-tavolino-per-il-cosenza-nel-match-con-il-verona-k2kxxzpp) confirms the loss for the home pitch being unplayable. Date/nonplaying circumstances still belong in a future match-level evidence review. |
| 2020/21 Salernitana–Reggiana | OpenFootball 3–0 `[awarded]`, scheduled 2020-10-31 | [CU 74 decision PDF lead](https://www.ilgiornaledisalerno.it/wp-content/uploads/2020/11/Cu74-Salernitana-Reggiana.pdf) and news search-index excerpts report a COVID nonappearance and 19 November ruling. Full decision has not been reviewed here; these excerpts are not complete-page verification. |

Neutral venues are not automatically exceptional outcomes: the 1990/91 return Reggina–Udinese note specifies Siderno; 1993/94 Brescia–Modena specifies Mantova. These annotations remain in complete source context for later date/venue review. League-wide points deductions, fixing investigations, 2003 boycotts/admission disputes and the 2018/19 Palermo decisions merit a broader verification pass; the current CSV sources do not reliably flag every administrative event. No assumption of exhaustive discovery is made.

## Postseason separation and limitations

The audit excludes **120 explicitly parsed non-regular entries**: four early RSSSF decisive tie-breaks and 116 OpenFootball postseason entries. This is an acquired-source count, not a claim of complete historical postseason coverage. The four early tie-breaks are 1990/91 Cosenza–Salernitana, 1991/92 Taranto–Casertana, and 1993/94 Padova–Cesena plus Acireale–Pisa. Their dates, extra-time/penalty details and neutral grounds remain in the original and complete private section context. The private excluded-entry date field remains null where that contextual date was not parsed.

OpenFootball stage headings (`Relegation`, `Aufstieg`, `Playoff`, `Playout` and variants) delimit exclusions. Extra-time/penalty annotations are preserved and are not treated as ordinary regular-season scores. The 2024/25 candidate contains outdated/postponed Salernitana–Frosinone playout listings and an unscored promotion-final leg; the regular-season 380 rows are complete. The 2022/23 excluded Brescia–Cosenza playout is marked awarded. These excluded originals are retained for future review; no attempt was made to reconstruct the full postseason from other sources.

## Licensing, provenance and acquisition restrictions

- **Football-Data:** its [usage policy](https://football-data.co.uk/contact.php) permits private personal betting/academic research and only light manual/automated downloading (at most twice weekly). It restricts commercial and AI data-training projects/heavy scraping. This one-off cached, sequential, paced research acquisition does not confer future model-training or redistribution rights. Do not schedule refreshes or assume permission for later TOTOdology training. The provider's notes and policy originals are saved privately; unversioned URLs can change and local SHA-256 snapshots are the evidence of acquired bytes.
- **RSSSF:** each of the seven original documents actually carries its own copying grant, conditional on proper acknowledgement to the author; it also retains copyright/all-rights-reserved wording. This is not CC0, a blanket database license, or assurance that contributors hold every upstream right. Original author/footer wording is retained unchanged. No private result dataset is published here.
- **OpenFootball:** the pinned [CC0 text](https://github.com/openfootball/italy/blob/48954d163c312aa705efacb64f771267031fe6eb/LICENSE.md) waives rights held by the contributor, with no assurance about accuracy, title or third-party rights. It does not independently certify score lineage or remove restrictions applicable to other sources.

Retrieval date is 2026-11-12. Every downloaded artifact has a sidecar `.provenance.json` containing requested/final URL, retrieval date, actual UTC timestamp, HTTP status/headers, byte length and SHA-256. OpenFootball URLs and acquisition entries identify the pinned revision; an HTTP receipt's generic unversioned-response wording does not replace that Git pin. RSSSF and Football-Data have no available immutable revision identifier: their exact local byte snapshots are checksum-bound. Source HTML/footer modification dates are distinct from retrieval dates. No denial, access challenge, rate-limit bypass, retries or ongoing-season download was used. The cached replay performs no network requests when receipts match.

Private storage below `data/private/italy/serie_b/`:

- `originals/rsssf/`, `originals/football_data/`, `originals/openfootball/`: initial immutable source downloads, plus individual receipts.
- `alternatives/football_data/2025-2026_I2.csv`: separately retained complete alternative and receipt.
- `metadata/`: Football-Data policy, Italy index, field notes; OpenFootball pinned tree, README and CC0 text, all with receipts.
- `acquisition.json`: initial 36-file plan/outcomes, source URLs and version pins; no failures.
- `selection.json`: explicit whole-season selection and reason for the 2025/26 alternative.
- `structural_audit.json`: deterministic private diagnostic records with source-line references, null/round-date semantics, excluded entries, full early Serie B section context, inventories and unresolved issues. This is not an eight-column standardized export.
- `review_candidates.json`: seven checksum/line-bound review candidates, without final eligibility decisions.
- `protected_before.json`: frozen SHA-256 inventory of 315 pre-task private artifacts.
- `inventory.json`: SHA-256/length inventory of all other current Serie B private artifacts, excluding itself.

## Reproduction and automated checks

```sh
# Offline replay: verifies every downloaded original/metadata receipt, then
# compares the complete regenerated diagnostic bytes with the saved audit.
PYTHONPATH=src python3 -m scripts.validate_serie_b --check

# Original acquisition is one-off, cached and subject to source restrictions.
# Existing matching receipts reuse local bytes; changed snapshots are refused.
PYTHONPATH=src python3 -m scripts.acquire_serie_b --completed-2025-alternative

PYTHONPATH=src python3 -m pytest tests/test_serie_b.py -q
PYTHONPATH=src python3 -m pytest -q
```

Tests use synthetic examples, not private match rows. They cover all 36 format expectations, the 14,962-fixture total, source/scope selection, paired-score orientation, footnote extraction, unspaced matrix cells, absent/abandoned scores, round-date ambiguity, COVID year inheritance, postseason boundaries, award annotations, missing/invalid values, duplicate/missing pairings, CSV padding/unknown fields, internal goal-total disagreements, checksum cache refusal and denied-host stopping. Unknown Football.TXT lines fail closed. Source parser date/score failures are never silently filled.

Validation is repeatable byte for byte from unchanged originals and selection. Required score/club fields, season bounds, dates, per-team home/away allocation, all ordered pairs, duplicates, team counts and source result codes were checked. RSSSF internal final-table goal comparisons are additional consistency checks, not independent proof of which match is wrong. The earlier historical standard validator requires real individual match dates and normalized records; it was not used to label undated diagnostic entries as standardization-ready.

**Verification readiness:** the 29 modern seasons can proceed to independent result/date verification, with 2003/04 extra-field review and the historical exception queue retained. The seven early seasons can support source comparison and result verification, but six still lack exact dates, 1995/96 has only round-date evidence and an unresolved final result, and several original internal inconsistencies remain. The collection as a whole is **not yet ready for standardization or training**. Source licensing and shared-lineage limitations persist.

## Completed validation evidence

- Targeted tests: **54 passed**. Complete repository suite: **602 passed** (9.57 seconds), using the existing isolated `/tmp/toto-serie-a-test` environment with `PYTHONPATH=src`.
- Saved audit regenerates byte for byte; all 43 original/metadata HTTP receipts and the separate selection were checked. The 91-entry private artifact inventory passes SHA-256 and byte-length verification.
- All **315** pre-task private artifacts remain byte-for-byte unchanged, including English/German/Serie A originals, standardized outputs, corrections and provenance. Git reports no tracked changes to existing league implementations, prediction code, Streamlit, README, OpenSpec or DFB pipeline.
- All **92** current Serie B private artifacts are ignored by Git; `git ls-files data/private` is empty. Public changes are confined to two new scripts, synthetic tests, this report and four appended planning-log decisions. The pre-existing `.DS_Store` files were not touched. `git diff --check` passes. Nothing was staged, committed or pushed.

Explicit RSSSF attribution: Maurizio Mariani and RSSSF for all seven documents; Maurizio Mariani and Misha Miladinovich for 1992/93; Sorin Arotaritei is thanked for Serie B stage results in 1990/91–1994/95; Ken Butler and Misha Miladinovich are thanked in 1996/97. The 1990/91–1994/95 documents show 31 October 2000 updates and 1999/2000 copyright; 1995/96 shows 5 January 2000, and 1996/97 31 January 2000, both copyright 2000. Original notices and their conditional acknowledgement requirements remain in the private originals.

| Private manifest / diagnostic | SHA-256 |
|---|---|
| `acquisition.json` | `34c08a516f651ec01b983bd747127abda58d7dfdf36b6a216f5b774e879e0586` |
| `selection.json` | `3c7740c53c16234d9cf7e0a650a5e5cf08379a1ae526b983da8d7d021ca6d01b` |
| `structural_audit.json` | `16697f9fef115feff0d47128d1683ef8f945b6a0b6017df5fb5db56310587c3b` |
| `review_candidates.json` | `38b8f979ddb3fd602b4a99591d74c899d8f5b872066108fc4812c14c2fbe44ff` |
| `inventory.json` | `5373c297238d84704890e92046838104fb80e6ca25f12c480ff349a958f6fcaa` |

## Source file checksums

Full SHA-256 values below identify original bytes, not corrections or independent authenticity. Paths are relative to the private Serie B root; the link is the original acquisition URL.

| Season | Source file / URL | SHA-256 |
|---|---|---|
| 1990/1991 | [originals/rsssf/ital91.html](https://www.rsssf.org/tablesi/ital91.html) | `e1ef0b544316218454f3369d1c283f31de8ffa6d4353e136422733f2c235909b` |
| 1991/1992 | [originals/rsssf/ital92.html](https://www.rsssf.org/tablesi/ital92.html) | `2013e5778ab853551671db239ab743f513d8f6a66948350872b1a3f6f2974b41` |
| 1992/1993 | [originals/rsssf/ital93.html](https://www.rsssf.org/tablesi/ital93.html) | `e7ef68a74ecc8e430ce46733cc972cd6d7e0f7950eadf91a8cbbee21531e2e40` |
| 1993/1994 | [originals/rsssf/ital94.html](https://www.rsssf.org/tablesi/ital94.html) | `1577631858cc9c430d7b541898b755ba064c2a4f8704915be5ac908562c5ed98` |
| 1994/1995 | [originals/rsssf/ital95.html](https://www.rsssf.org/tablesi/ital95.html) | `de5f10a093248014a2cb9f727f1237e8d16da71e38297673ecc8cbc5da5f9e8a` |
| 1995/1996 | [originals/rsssf/ital96.html](https://www.rsssf.org/tablesi/ital96.html) | `4d3c16de7e18d125a7781adfbd3476de1e8fa7f3125e297b02eb4609ffc0bda6` |
| 1996/1997 | [originals/rsssf/ital97.html](https://www.rsssf.org/tablesi/ital97.html) | `ae4e855694d4b8f3448f066eb082b8aa796499aab9a19b0d0ed92b8600fbda6b` |
| 1997/1998 | [originals/football_data/1997-1998_I2.csv](https://www.football-data.co.uk/mmz4281/9798/I2.csv) | `e7440875c309101ab5eb80ede2f2e5310cad88778cf7017a84f6fef9e1aa909f` |
| 1998/1999 | [originals/football_data/1998-1999_I2.csv](https://www.football-data.co.uk/mmz4281/9899/I2.csv) | `eb74f2b4d2e0ac63fdc0555f37323cb6572ae61858b27f00a8d1cccd9ab90033` |
| 1999/2000 | [originals/football_data/1999-2000_I2.csv](https://www.football-data.co.uk/mmz4281/9900/I2.csv) | `ee482c172f2ed5ece14d2d370642e0bfcdf26c40497952d6466c354d31849741` |
| 2000/2001 | [originals/football_data/2000-2001_I2.csv](https://www.football-data.co.uk/mmz4281/0001/I2.csv) | `aeda074bbbddad77fc73045146f67dcad0db3f15376b91cece7771ad75f6bd0b` |
| 2001/2002 | [originals/football_data/2001-2002_I2.csv](https://www.football-data.co.uk/mmz4281/0102/I2.csv) | `9b041141ac550d11a5914fc98fbf17586c9d94a5c42aa6c8bce49c5c6822cfaf` |
| 2002/2003 | [originals/football_data/2002-2003_I2.csv](https://www.football-data.co.uk/mmz4281/0203/I2.csv) | `4d9b201d926d3eff80c1621e16d7f5ddd198c6e96a672118b98712641f45df9b` |
| 2003/2004 | [originals/football_data/2003-2004_I2.csv](https://www.football-data.co.uk/mmz4281/0304/I2.csv) | `4699231e8b0570ba241dddd774dbc8581f4d2b37a2ac64c817ec5a997f90f439` |
| 2004/2005 | [originals/football_data/2004-2005_I2.csv](https://www.football-data.co.uk/mmz4281/0405/I2.csv) | `90d43448fea4e5655a09477125a1c09c5c443a0dd75337bce02afa897010ef89` |
| 2005/2006 | [originals/football_data/2005-2006_I2.csv](https://www.football-data.co.uk/mmz4281/0506/I2.csv) | `020def7afe911b644281af30d984b8420f52959ef4a25aa256b81f5f7d0acc43` |
| 2006/2007 | [originals/football_data/2006-2007_I2.csv](https://www.football-data.co.uk/mmz4281/0607/I2.csv) | `9395ce8f01979c5567f89a4fb693dabe3976fd16cb73c18ba2fc1f85f103fc22` |
| 2007/2008 | [originals/football_data/2007-2008_I2.csv](https://www.football-data.co.uk/mmz4281/0708/I2.csv) | `03af6f3fb1e96d9cd74166c5a0484eb70c2ca832e00e5394b20079512f43c23f` |
| 2008/2009 | [originals/football_data/2008-2009_I2.csv](https://www.football-data.co.uk/mmz4281/0809/I2.csv) | `e1c3f889e5993f851fdf22fe68e3e78cb694389c6072ce54737b18af8fa7ca25` |
| 2009/2010 | [originals/football_data/2009-2010_I2.csv](https://www.football-data.co.uk/mmz4281/0910/I2.csv) | `5f02e023255035744fd38f0fd95ea89a79a7d4865cc87120ebc7ec0c3d6e4c3c` |
| 2010/2011 | [originals/football_data/2010-2011_I2.csv](https://www.football-data.co.uk/mmz4281/1011/I2.csv) | `7b787793d7295803dc0d5c6cacce980538ca7731370105e33ce33fd4cc8439b7` |
| 2011/2012 | [originals/football_data/2011-2012_I2.csv](https://www.football-data.co.uk/mmz4281/1112/I2.csv) | `a270c5a8449e84a73c179f7e364689ef601b089b738227750526eac7c5bba2ee` |
| 2012/2013 | [originals/football_data/2012-2013_I2.csv](https://www.football-data.co.uk/mmz4281/1213/I2.csv) | `d8c4d86595c42c05115ce6ca0b3e3fa3bd31d295862705248a7517f4e209e76c` |
| 2013/2014 | [originals/openfootball/2013-14_2-serieb.txt](https://raw.githubusercontent.com/openfootball/italy/48954d163c312aa705efacb64f771267031fe6eb/2013-14/2-serieb.txt) | `02bf4c8410e68651a17849eb18c61c65ebd80a6d6b6a692a46876fd7f008eb4a` |
| 2014/2015 | [originals/openfootball/2014-15_2-serieb.txt](https://raw.githubusercontent.com/openfootball/italy/48954d163c312aa705efacb64f771267031fe6eb/2014-15/2-serieb.txt) | `670117036204fa3f460fd891e922b6462f0f7b2e02ff142f014c894a8bad2e6b` |
| 2015/2016 | [originals/openfootball/2015-16_2-serieb.txt](https://raw.githubusercontent.com/openfootball/italy/48954d163c312aa705efacb64f771267031fe6eb/2015-16/2-serieb.txt) | `2a9fec281616cfe56a30a829732ff000c8b77089768a61810fd331161212c783` |
| 2016/2017 | [originals/openfootball/2016-17_2-serieb.txt](https://raw.githubusercontent.com/openfootball/italy/48954d163c312aa705efacb64f771267031fe6eb/2016-17/2-serieb.txt) | `42166ac10f741048b59b3f7b3fb9490cbf0dc799626387465978f93a630e90c6` |
| 2017/2018 | [originals/openfootball/2017-18_2-serieb.txt](https://raw.githubusercontent.com/openfootball/italy/48954d163c312aa705efacb64f771267031fe6eb/2017-18/2-serieb.txt) | `c5f7d0b48af5b6088ecd49c9dd5c3a1468aa0fad6d0d4bd74bfccb6b4b309816` |
| 2018/2019 | [originals/openfootball/2018-19_2-serieb.txt](https://raw.githubusercontent.com/openfootball/italy/48954d163c312aa705efacb64f771267031fe6eb/2018-19/2-serieb.txt) | `5f671ef367719a460b287f0e14b5b56aae974f08dcfc1e8f05bf1aa6bc84bfdf` |
| 2019/2020 | [originals/openfootball/2019-20_2-serieb.txt](https://raw.githubusercontent.com/openfootball/italy/48954d163c312aa705efacb64f771267031fe6eb/2019-20/2-serieb.txt) | `2b42adde783c6f12951bb049adc6081226d37ddc5c55ee0fdc0a2da582eb9525` |
| 2020/2021 | [originals/openfootball/2020-21_2-serieb.txt](https://raw.githubusercontent.com/openfootball/italy/48954d163c312aa705efacb64f771267031fe6eb/2020-21/2-serieb.txt) | `9299ab8d62a83f44f6c550562dc236c46c0363815ba685b6b520e059ff8de302` |
| 2021/2022 | [originals/openfootball/2021-22_2-serieb.txt](https://raw.githubusercontent.com/openfootball/italy/48954d163c312aa705efacb64f771267031fe6eb/2021-22/2-serieb.txt) | `e82c50c484dbc45f67d1d436240e26703785cf993984eb2892e0ddb38afe86d7` |
| 2022/2023 | [originals/openfootball/2022-23_2-serieb.txt](https://raw.githubusercontent.com/openfootball/italy/48954d163c312aa705efacb64f771267031fe6eb/2022-23/2-serieb.txt) | `26997f9e9be1491219f209cde82ee70821c03c47ea5b8c799a0256302d9bda37` |
| 2023/2024 | [originals/openfootball/2023-24_2-serieb.txt](https://raw.githubusercontent.com/openfootball/italy/48954d163c312aa705efacb64f771267031fe6eb/2023-24/2-serieb.txt) | `3be0dd5060db797931912dc0b37b3ddf583407e12f2eb79ed69f09b269a18e15` |
| 2024/2025 | [originals/openfootball/2024-25_2-serieb.txt](https://raw.githubusercontent.com/openfootball/italy/48954d163c312aa705efacb64f771267031fe6eb/2024-25/2-serieb.txt) | `312af0edceeb40d0c38cb3ac53b942e0c66595b00ed7ad4f75a2d5f9c46a82d1` |
| 2025/2026 | [originals/openfootball/2025-26_2-serieb.txt](https://raw.githubusercontent.com/openfootball/italy/48954d163c312aa705efacb64f771267031fe6eb/2025-26/2-serieb.txt) | `252e858b3e1745b6d149db73f6e6cb98c7576e41ea6e7111ad706ddf92e881fb` |
| 2025/2026 | [alternatives/football_data/2025-2026_I2.csv](https://www.football-data.co.uk/mmz4281/2526/I2.csv) | `ed4bcece92bb8b09aa94768bc77d3529fa29339ec70fa7867a9fbc3ca0954731` |


## Independent modern-period review — 2026-11-12

This section records the later, separately authorized independent review. The acquisition-stage findings above remain a historical snapshot. Scope is **1997/98–2025/26: 29 seasons and 12,302 selected regular-season records**. The seven 1990/91–1996/97 seasons, their 2,660 entries and unresolved date/score issues were not repaired or re-reviewed.

### Sample, evidence strength and limitations

**39 distinct fixtures have independently consulted complete-page/text evidence for date, home/away orientation, score and Serie B/season classification.** Thirty-eight agree on these fields; one has a confirmed date-only discrepancy. Calendar-period counts are **5 in 1997–1999, 15 in 2000–2009, 11 in 2010–2019 and 8 in 2020–2026**, exceeding every requested quota. Two samples are unplayed administrative awards: their verified date is explicitly the scheduled fixture date, never an actual playing date.

This is a purposive, clustered documentary sample, not a random accuracy estimate or a full match-by-match census of 12,302 results. Direct verified samples occur in eight seasons; one additional season, 2002/03, has unresolved administrative-result review. The other seasons retain their structural checks and source inventories but have not each received an individual externally verified match. No claim of universal independent certification is made. All 29 season inventories were rechecked read-only; a same-team/same-date scan found no collision groups, which does not prove every date correct.

References are independent consultations outside the selected original files, **not a proven independent chain of underlying score collection**. RSSSF and Wikipedia may share historical contributors. Wikinews cites Lega B match reports that could also underlie OpenFootball; the old Avellino–Novara match report was inaccessible. SoccerNews uses an unspecified feed; its `football-data.org` crest URLs do not establish identity with, or independence from, `football-data.co.uk`. Official FIGC, Lega B, participant-club and Genoa foundation records were preferred for adjudicating exceptions and the confirmed correction. No number of derivative sites is treated as independent votes.

`FULL_RESULTS_PAGE`, `FULL_REPORT` and `FULL_DECISION_TEXT` describe readable result blocks, reports or complete relevant decision text. A PDF text view is not a claim that the screenshot/render service worked; PDF screenshot requests failed. Several web-access responses and manually transcribed observations are sealed privately, but those access snapshots are **not complete byte-for-byte copies of every external HTML page or original PDF**. URLs, section/page/entry locators, retrieval date, access status, lineage notes, original bindings and observations are the reproducible review evidence. Web references can change; the checksum seal protects our recorded evidence, not the remote website or external truth.

The official 2025/26 Pescara–Cesena match URL currently renders “match data unavailable,” despite a detailed search-index entry. That URL is recorded as **INDEXED_ONLY** and contributes zero complete-page confirmations. Sky's readable contemporary report supplies the sample evidence. Likewise the old Lega B Salernitana–Sampdoria suspension URL returned 404: its indexed interim 0–2 is distinguished from the fully readable subsequent 0–3 disciplinary summary.

### Independently checked fixtures

All rows below are Serie B regular season in the stated season. Dates/results are the external observations; `DATE CORRECTION` identifies the sole source disagreement. Asterisks denote a scheduled date for an unplayed award. Identity mappings and exact source rows are in private `samples.json`; no comprehensive team normalization is implemented.

| ID | Season | Observed date | Home – away | Final score | Evidence | Comparison |
|---|---|---|---|---|---|---|
| B01 | 1997/1998 | 1997-08-31 | Ancona – Torino | 1–0 | [T97](https://it.wikipedia.org/wiki/Torino_Calcio_1997-1998) | Agrees |
| B02 | 1997/1998 | 1997-09-07 | Torino – Padova | 2–1 | [T97](https://it.wikipedia.org/wiki/Torino_Calcio_1997-1998) | Agrees |
| B03 | 1997/1998 | 1997-09-14 | Torino – Foggia | 1–1 | [T97](https://it.wikipedia.org/wiki/Torino_Calcio_1997-1998) | Agrees |
| B04 | 1997/1998 | 1997-09-21 | Pescara – Torino | 3–0 | [T97](https://it.wikipedia.org/wiki/Torino_Calcio_1997-1998) | Agrees |
| B05 | 1997/1998 | 1997-09-27 | Torino – Genoa | 2–1 | [FG97](https://www.fondazionegenoa.com/wp-content/uploads/2026/02/Tutti-i-precedenti-tra-il-Genoa-e-il-Torino-e-le-sue-antecedenti.pdf) | DATE CORRECTION |
| B06 | 2000/2001 | 2000-09-10 | Ancona – Monza | 1–0 | [R00](https://www.rsssf.org/tablesi/ital01.html) | Agrees |
| B07 | 2000/2001 | 2000-09-10 | Crotone – Ravenna | 2–1 | [R00](https://www.rsssf.org/tablesi/ital01.html) | Agrees |
| B08 | 2000/2001 | 2000-09-10 | Genoa – Siena | 1–1 | [R00](https://www.rsssf.org/tablesi/ital01.html) | Agrees |
| B09 | 2000/2001 | 2000-09-10 | Pescara – Empoli | 1–3 | [R00](https://www.rsssf.org/tablesi/ital01.html) | Agrees |
| B10 | 2000/2001 | 2000-09-10 | Piacenza – Cosenza | 2–0 | [R00](https://www.rsssf.org/tablesi/ital01.html) | Agrees |
| B11 | 2000/2001 | 2000-09-10 | Pistoiese – Torino | 1–1 | [R00](https://www.rsssf.org/tablesi/ital01.html) | Agrees |
| B12 | 2000/2001 | 2000-09-10 | Ternana – Chievoverona | 1–0 | [R00](https://www.rsssf.org/tablesi/ital01.html) | Agrees |
| B13 | 2000/2001 | 2000-09-10 | Treviso – Cagliari | 2–3 | [R00](https://www.rsssf.org/tablesi/ital01.html) | Agrees |
| B14 | 2000/2001 | 2000-09-10 | Venezia – Cittadella | 2–2 | [R00](https://www.rsssf.org/tablesi/ital01.html) | Agrees |
| B15 | 2000/2001 | 2000-09-11 | Salernitana – Sampdoria | 2–3 | [R00](https://www.rsssf.org/tablesi/ital01.html) | Agrees |
| B16 | 2013/2014 | 2013-08-23 | Reggina – Bari | 0–0 | [W13](https://it.wikinews.org/wiki/Calcio,_Serie_B_2013-2014:_1%C2%AA_giornata) | Agrees |
| B17 | 2013/2014 | 2013-08-24 | Avellino – Novara | 2–1 | [W13](https://it.wikinews.org/wiki/Calcio,_Serie_B_2013-2014:_1%C2%AA_giornata) | Agrees |
| B18 | 2013/2014 | 2013-08-24 | Brescia – Virtus Lanciano | 2–2 | [W13](https://it.wikinews.org/wiki/Calcio,_Serie_B_2013-2014:_1%C2%AA_giornata) | Agrees |
| B19 | 2013/2014 | 2013-08-24 | Empoli – Latina | 3–1 | [W13](https://it.wikinews.org/wiki/Calcio,_Serie_B_2013-2014:_1%C2%AA_giornata) | Agrees |
| B20 | 2013/2014 | 2013-08-24 | Modena – Palermo | 1–1 | [W13](https://it.wikinews.org/wiki/Calcio,_Serie_B_2013-2014:_1%C2%AA_giornata) | Agrees |
| B21 | 2013/2014 | 2013-08-24 | Padova – Trapani | 0–2 | [W13](https://it.wikinews.org/wiki/Calcio,_Serie_B_2013-2014:_1%C2%AA_giornata) | Agrees |
| B22 | 2013/2014 | 2013-08-24 | Pescara – Juve Stabia | 3–0 | [W13](https://it.wikinews.org/wiki/Calcio,_Serie_B_2013-2014:_1%C2%AA_giornata) | Agrees |
| B23 | 2013/2014 | 2013-08-24 | Siena – Crotone | 5–2 | [W13](https://it.wikinews.org/wiki/Calcio,_Serie_B_2013-2014:_1%C2%AA_giornata) | Agrees |
| B24 | 2013/2014 | 2013-08-24 | Spezia – Cittadella | 0–0 | [W13](https://it.wikinews.org/wiki/Calcio,_Serie_B_2013-2014:_1%C2%AA_giornata) | Agrees |
| B25 | 2013/2014 | 2013-08-24 | Ternana – Carpi | 1–0 | [W13](https://it.wikinews.org/wiki/Calcio,_Serie_B_2013-2014:_1%C2%AA_giornata) | Agrees |
| B26 | 2025/2026 | 2026-05-08 | Avellino – Modena | 1–0 | [S26](https://www.soccernews.com/soccer-stats/serie-b/fixtures-and-results/2025-26/) | Agrees |
| B27 | 2025/2026 | 2026-05-08 | Catanzaro – Bari | 2–3 | [S26](https://www.soccernews.com/soccer-stats/serie-b/fixtures-and-results/2025-26/) | Agrees |
| B28 | 2025/2026 | 2026-05-08 | Cesena – Padova | 3–4 | [S26](https://www.soccernews.com/soccer-stats/serie-b/fixtures-and-results/2025-26/) | Agrees |
| B29 | 2025/2026 | 2026-05-08 | Frosinone – Mantova | 5–0 | [S26](https://www.soccernews.com/soccer-stats/serie-b/fixtures-and-results/2025-26/) | Agrees |
| B30 | 2025/2026 | 2026-05-08 | Monza – Empoli | 2–2 | [S26](https://www.soccernews.com/soccer-stats/serie-b/fixtures-and-results/2025-26/) | Agrees |
| B31 | 2003/2004 | 2003-10-12 | Atalanta – Triestina | 4–1 | [X1](https://it.wikipedia.org/wiki/Atalanta_Bergamasca_Calcio_2003-2004) | Agrees |
| B32 | 2003/2004 | 2003-10-12 | Avellino – Messina | 0–1 | [X2](https://it.wikipedia.org/wiki/Unione_Sportiva_Avellino_2003-2004) | Agrees |
| B33 | 2003/2004 | 2003-10-12 | Bari – Ascoli | 1–2 | [X3](https://it.wikipedia.org/wiki/Ascoli_Calcio_1898_2003-2004) | Agrees |
| B34 | 2003/2004 | 2003-10-12 | Cagliari – Ternana | 3–0 | [X4](https://it.wikipedia.org/wiki/Cagliari_Calcio_2003-2004) | Agrees |
| B35 | 2004/2005 | 2005-06-11 | Genoa 1893 – AC Venezia | 3–2 | [G05](https://www.uefa.com/news-media/news/01aa-0f84751fa93c-bbd39c30f1f3-1000--genoa-back-in-the-big-time/) | Agrees |
| B36 | 2018/2019 | 2018-09-01* | Cosenza – Hellas Verona | 0–3 | [CA18](https://www.figc.it/it/federazione/news/csa-confermata-la-sconfitta-0-3-a-tavolino-per-il-cosenza-nel-match-con-il-verona-k2kxxzpp) | Agrees |
| B37 | 2020/2021 | 2020-10-31* | Salernitana – Reggiana | 3–0 | [D20](https://www.ilgiornaledisalerno.it/wp-content/uploads/2020/11/Cu74-Salernitana-Reggiana.pdf) | Agrees |
| B38 | 2025/2026 | 2025-08-22 | Pescara – Cesena | 1–3 | [P25](https://sport.sky.it/calcio/serie-b/2025/08/22/serie-b-pescara-cesena-risultato-tabellino) | Agrees |
| B39 | 2025/2026 | 2025-08-23 | Empoli – Padova | 3–1 | [E25](https://www.pianetaempoli.it/empoli-vs-padova-live-match/) | Agrees |

T97: Torino 1997/98, Serie B first-half-season individual match blocks. R00: RSSSF 2000/01, Second Level, **Round 2**, dates September 10/11. W13: Wikinews 2013/14 Round 1 **date-specific Tabellini**, not its generic “24 August” summary header (Friday Reggina–Bari was August 23; the Monday Cesena–Varese entry was not included in that cluster). W13 contains some anomalous scorer/standings text; those secondary fields are not relied on. S26: SoccerNews 2025/26, May 8 regular-season Matchweek 38 FT blocks. X1–X4: individual dated October 12 2003 club-season match records. G05: contemporary UEFA June 11 2005 report. CA18: FIGC award confirmation plus Sky's September 1 scheduled-date/nonplaying report. D20: full relevant CU 74 decision text on its third-party mirror. P25/E25: contemporary Sky and PianetaEmpoli opening-round reports.

### Confirmed correction and unresolved reference conflicts

**One verified, unapplied date-only correction:** Torino–Genoa, 1997/98, played 2–1, source date **1997-09-28 → 1997-09-27**. [Genoa foundation historical PDF](https://www.fondazionegenoa.com/wp-content/uploads/2026/02/Tutti-i-precedenti-tra-il-Genoa-e-il-Torino-e-le-sue-antecedenti.pdf), PDF page 7, entry 106, explicitly gives Saturday 27 September, Serie B and Torino–Genoa 2–1. [Torino's secondary season record](https://it.wikipedia.org/wiki/Torino_Calcio_1997-1998) independently agrees in the fifth-round dated block. The foundation is a football-history institution; a complete contemporary referee report was not obtained. Some generic indexed score services repeat September 28, so agreement among such services is not assumed independent corroboration.

Private `verified_corrections.json` binds this proposal to the original file SHA-256, complete physical CSV line, parsed original facts, sample B05, exact replacement and complete-page evidence. It remains `applied: false`, `VERIFIED_PENDING_STANDARDIZATION`; only canonical fact `date` / source column `Date` can change. Scores, orientation, clubs, season and competition remain unchanged. No corrected dataset has been created.

RSSSF 2000/01 Round 1 headings place nine games on September 4 and Torino–Ancona on September 2; the selected CSV dates them September 3 and September 1 respectively. This is a **reference conflict**, retained in `reference_conflicts.json`, not evidence authorizing ten CSV date changes. The Round 2 sample dates agree. No replacement is proposed for the opening round without further corroboration. Discovering this conflict was not suppressed by selecting a different round for the confirmed sample.

### Modern exceptional fixtures and training policy

The four previously flagged modern regular-season cases were investigated. The connected Catania–Venezia case was also discovered and retained. All five remain present in the original inventory. Three have conservative exclusions; two remain unresolved and held out pending review. **No unlisted match is individually certified training-eligible.** No filtering or model training occurred.

| Case | Original schedule / actual playing | Played and administrative outcomes | Training decision |
|---|---|---|---|
| E1: Catania–Siena, 2002/03 | Original schedule unestablished; actual 2003-04-12; no replay established | Played 1–1. CAF imposed 2–0, Corte Federale restored 1–1, and FIGC CU 4/A on July 2 reinstated the CAF outcome while referring consequences to arbitration. The selected CSV/RSSSF retain 1–1. Ultimate final homologation after the full litigation sequence remains unresolved. | **UNRESOLVED — HOLD OUT.** A completed first playing is not automatically unsuitable because it was appealed; the unresolved choice of played versus final administrative label prevents certification here. |
| E2: Genoa–Venezia, 2004/05 | Original schedule unestablished separately; actual 2005-06-11; no replay established | Played 3–2. UEFA's August 8 appeal report confirms the fixing finding, bottom-of-table demotion and disciplinary bans. No score-changing order was located; the archival played score is retained, not labelled a separately proved homologation order. | **EXCLUDED for ordinary 90-minute sporting-result training:** specific fixing evidence, not merely a general club or standings sanction. |
| E3: Cosenza–Hellas Verona, 2018/19 | Scheduled 2018-09-01; actual/replay date null | Never started because of unsafe pitch. Awarded home loss 0–3, confirmed by FIGC appeal report October 18. No on-field score exists. | **EXCLUDED — UNPLAYED ADMINISTRATIVE AWARD.** |
| E4: Salernitana–Reggiana, 2020/21 | Scheduled 2020-10-31; actual/replay date null | Never started: Reggiana did not appear amid COVID cases. CU 74 of November 19 imposes a 0–3 loss on Reggiana, hence home 3–0. The ruling date is not a playing date. | **EXCLUDED — UNPLAYED ADMINISTRATIVE AWARD.** |
| E5: Catania–Venezia, 2002/03, newly identified | Original schedule unresolved; source/secondary playing date 2003-05-17; no replay established | Acquired played score 2–0 conflicts with a reported administrative 0–2 in the Venezia season archive and retrospective chronology. Final primary decision and possible subsequent changes unlocated. | **UNRESOLVED — HOLD OUT**, not automatically declared permanently unsuitable. |

E1 evidence is the readable [FIGC CU 4/A](https://files.figc.it/version/c%3AMjAxMDAzZDAtM2NlYS00%3AOTcyYWU1MmYtYjM3ZC00/C_2_ContenutoGenerico_4963_lstAllegati_Allegato0_upfAllegato.pdf), page 2, and [CAF CU 1/C](https://files.figc.it/version/c%3AMzkwODU0ZjUtNTc1MS00%3ANTYwOGZmOWEtMjA4Zi00/C_2_ContenutoGenerico_5186_lstAllegati_Allegato0_upfAllegato.pdf), PDF pages 3–4, supplemented by the [contemporary July 16 chronology](https://www.nove.firenze.it/a307162038-calcio-le-tappe-del-caso-catania.htm). These confirm a genuine discrepancy between the acquired played score and the reinstated July 2 administrative score. They do **not** settle the outcome of every later proceeding. The old FIGC legacy link returned 404; the replacement official `files.figc.it` documents were read, rather than substituting an indexed snippet as evidence.

E2: [UEFA rejection of Genoa's appeal](https://www.uefa.com/news-media/news/01ac-0e6d13e48221-5671be69e6cb-1000--italian-court-rejects-genoa-appeal/). E3: [Sky scheduled-date/nonplaying account](https://sport.sky.it/calcio/serie-b/2018/09/01/cosenza-verona-rinvio) and [FIGC appellate award](https://www.figc.it/it/federazione/news/csa-confermata-la-sconfitta-0-3-a-tavolino-per-il-cosenza-nel-match-con-il-verona-k2kxxzpp). E4: [CU 74 full decision text](https://www.ilgiornaledisalerno.it/wp-content/uploads/2020/11/Cu74-Salernitana-Reggiana.pdf), pages 1–2, mirrored outside the league, corroborated by [Sky's decision report](https://sport.sky.it/calcio/serie-b/2020/11/19/salernitana-reggiana-decisione-giudice-sportivo). E5: [Venezia's secondary season archive](https://it.wikipedia.org/wiki/Associazione_Calcio_Venezia_2002-2003) and [retrospective chronology](https://www.calcioromantico.com/a-spasso-nel-tempo/il-papocchio-della-b-a-24-squadre/), which draws on Carlo Caliceti's October 2003 account. These sources are leads for the missing final order, not two independent primary decisions.

Two checksum/line-bound **score correction candidates** are held separately in `correction_candidates.json`: E1 `1–1 → 2–0` and E5 `2–0 → 0–2`. Both are `HOLD_PENDING_FINAL_STATUS`, unapplied and explicitly **not authorized for standardization**. They are not mixed with the one approved date-only proposal. No absence of a later ruling is used as proof of finality. A future adapter must not blindly apply this candidates file.

Postseason cases were also kept separate:

- **2022/23 Brescia–Cosenza return playout:** [Lega B's June 7 disciplinary summary](https://www.legab.it/news/brescia-0-3-a-tavolino-e-due-gare-a-porte-chiuse) confirms awarded 0–3 and ground sanctions. The reported June 1 interruption at 1–1 is not fully independently established in this review. It remains excluded because it is postseason, without modifying the regular-season Brescia–Cosenza record.
- **2024/25 playout:** the OpenFootball original's postponed May Salernitana–Frosinone listings are obsolete postseason entries, not regular-season gaps. [Lega B's June 23 summary](https://www.legab.it/news/giudice-sportivo-finale-ritorno-playout) confirms Salernitana's 0–3 loss. The June 22 actual Salernitana–Sampdoria suspension and interim 0–2 currently have official-origin indexed evidence; the old direct page returned 404. The exact initial scheduling/revised calendar and every interruption detail were not fully adjudicated. Preserve and exclude the obsolete original listings, do not relabel or merge them into regular-season data.

The 2003 admission/boycott context and 2018/19 Palermo proceedings remain season/standings matters unless match-specific evidence is found. No season-wide score correction or training exclusion is inferred from them.

### 2003/04 surplus-column warning resolved for required match fields

The warning is a genuine **non-rectangular CSV format defect**, but the four affected required match-field records are independently corroborated:

| Physical CSV line | Date | Fixture | FT | Evidence |
|---|---|---|---|---|
| 86 | 2003-10-12 | Atalanta–Triestina | 4–1 | X1 / B31 |
| 87 | 2003-10-12 | Avellino–Messina | 0–1 | X2 / B32 |
| 88 | 2003-10-12 | Bari–Ascoli | 1–2 | X3 / B33 |
| 89 | 2003-10-12 | Cagliari–Ternana | 3–0 | X4 / B34 |

All 552 rows have the required named match fields and the complete 24-club regular-season pairing inventory. The four affected rows append seven unnamed values after the header-defined columns. Their Date, HomeTeam, AwayTeam, FTHG, FTAG and FTR remain correctly aligned and agree with the externally checked date/orientation/score. The surplus values' meanings have **not** been established; they are neither shifted into named fields nor interpreted as extra matches or goals. Thus the warning is **harmless to the explicitly guarded required-field projection**, not proof the whole source is a clean rectangle or that all optional statistics are trustworthy. No correction to the required match records is warranted. The old structural audit retains its original REVIEW flag; this later adjudication is separate in `2003_format_review.json`.

### 2025/26 independent review

Seven selected regular-season results were checked across the opening and closing rounds: five May 8 FT blocks plus Pescara–Cesena (August 22) and Empoli–Padova (August 23). All agree. The official [Frosinone participant report](https://www.frosinonecalcio.com/frosinone-mantova-5-0/) additionally corroborates the May 8 home 5–0 win; SoccerNews supplies the explicit league/season/regular-round context. Contemporary [Sky](https://sport.sky.it/calcio/serie-b/2025/08/22/serie-b-pescara-cesena-risultato-tabellino) and [PianetaEmpoli](https://www.pianetaempoli.it/empoli-vs-padova-live-match/) provide the opening-round reports.

A separate manually transcribed [RSSSF final Serie B table](https://www.rsssf.org/tablesi/ital2026.html) was compared against all **380** selected CSV results. **All 20 clubs agree on wins, draws, losses, goals for, goals against and points**, with 38 matches per club. Credit: Roberto Di Maggio and Karel Stokkermans, RSSSF 2026, updated June 21 2026; its copying notice requires attribution. This is a strong season-level arithmetic cross-check, **not 380 individual date/result verifications**: offsetting match errors and date mistakes can evade totals. Full published labels are interpreted only within this season; no global identity mapping is created.

The selected complete Football-Data file and the separate incomplete OpenFootball original remain byte-for-byte unchanged. The 71 unscored OpenFootball entries were not filled, compared as confirmed finals, or merged. No 2025/26 selected-data correction was established.

### Historical identities and unresolved modern coverage

Observed versus source labels are explicitly mapped per sample: Chievoverona/Chievo; Avellino/AS Avellino; Bari/AS Bari; Reggina/Reggina Calcio; Pescara/Delfino Pescara; Padova/Calcio Padova; Siena/AC Siena; Spezia/Spezia Calcio and similar corporate prefixes. Reggina and Reggiana are kept distinct. The 1997 Torino is **Torino Calcio**, not an assertion that its post-2005 legal entity existed then. Genoa 1893/AC Venezia references identify the sporting participants, not legal continuity into every later re-founded club. Modern Cesena, Palermo, Bari, Avellino, Siena, Vicenza and Modena labels require season-aware identity review before cross-season pooling; examples such as SoccerNews's old corporate display names are not treated as definitive legal names. No club names are corrected in the raw files.

Remaining limitations: two unresolved 2002/03 administrative final results; the RSSSF opening-round date conflict; limited, clustered rather than per-season individual sample coverage; incomplete access to some primary historical match sheets/final rulings; unidentified upstream score lineage; and source licensing restrictions already documented. The seven early seasons remain entirely separate and unresolved. No new training or redistribution rights were established by this review.

### Reproduction, preservation and technical readiness

The new `scripts.verify_serie_b_review` is read-only. It verifies whole-source SHA-256 and exact physical-line bindings, all 39 original/observed facts and aliases, complete-page calendar quotas, the guarded unapplied date-only proposal, separate unapproved score candidates, five regular exception classifications, every surplus-column row, and all 20 independently transcribed 2025/26 club aggregates. It re-runs the unchanged structural audit and compares its complete saved bytes, then verifies the **407 pre-review private artifact fingerprints**. Its private evidence seal also pins the checker revision; tests validate record consistency and refusal paths, **not external historical truth**.

```sh
PYTHONPATH=src python3 -m scripts.verify_serie_b_review
PYTHONPATH=src python3 -m pytest tests/test_serie_b_review.py -q
PYTHONPATH=src python3 -m pytest -q
```

Private new files under `data/private/italy/serie_b/verification/` include `protected_before.json`, `sample_selection.json`, `samples.json`, `evidence_catalog.json`, access snapshots, `verified_corrections.json`, `correction_candidates.json`, `exception_policy.json`, `2003_format_review.json`, `2025_aggregate_review.json`, `reference_conflicts.json` and `review_manifest.json`. The older acquisition manifests/inventory are not rewritten to include these later review artifacts; the new review manifest seals this stage separately.

**Technical readiness: not an unconditional release of all 29 modern seasons for standardization.** Their 12,302-record structures and required fields remain technically sound; the 2003/04 required-field warning is adjudicated and the 2025/26 sample/aggregate checks pass. The verified Torino–Genoa date proposal must be applied only to a future derivative. The two 2002/03 score candidates must remain held until final administrative status is resolved or an explicit future archival policy authorizes retaining played scores with unresolved final-status metadata. No such policy choice or standardization was implemented here. Unresolved training suitability must remain explicit; no integration or training is authorized by this review.

### Completed modern-review validation evidence

- **39 externally corroborated fixture observations**: 38 agreements and one confirmed date-only discrepancy; calendar quotas 5 / 15 / 11 / 8. This count includes two explicitly unplayed administrative awards, not 39 ordinary played matches.
- **33 targeted review tests passed**; the complete repository suite passed **635 tests in 9.94 seconds**. The isolated existing test environment was `/tmp/toto-serie-a-test/bin/python`, with `PYTHONPATH=src`.
- Read-only review replay passes: **29 modern seasons / 12,302 records**, **407 pre-review private files unchanged**, original 36-season / 14,962-entry structural audit byte-for-byte unchanged, one unapplied verified date proposal, two held score candidates, three exclusions / two unresolved cases, zero same-team/date collision groups, and 20 matching 2025/26 club aggregates.
- All 108 Serie B artifacts, including the new review evidence, are Git-ignored; no `data/private/` files are tracked. The old 91-entry Serie B inventory remains unchanged and valid. Existing English, German and Serie A datasets and all five standardized leagues remain byte-identical. README, Homework 8 OpenSpec, Streamlit, prediction code and DFB pipeline have no changes.
- Branch remains `feature/data-collection`, HEAD remains `95f0a728d965cc1e02458c7754e64436db6e8fcc`. No files were staged, committed or pushed. Pre-existing `.DS_Store` files were left alone. Public review additions are the read-only checker, synthetic tests, this appended report and planning-log lines; prior acquisition-stage uncommitted work remains present.

| Private verification artifact | SHA-256 |
|---|---|
| `sample_selection.json` | `44dfd5659ae0f437d927fd3be40781880af337c2763046a4f6967c59f7d1eb63` |
| `samples.json` | `816d11d7a83bc0ebfd47623c384286374504c03819c0a2214612c2d572063fb6` |
| `evidence_catalog.json` | `00783f74f95036161c0677c801eb66552ed2cd0ef52f962830ee5d374528091c` |
| `verified_corrections.json` | `54795c1257ac172035196730cc5661f08c93902befcd6315c15b2c6375865b7c` |
| `correction_candidates.json` | `1c6be9dd89eb1b5eb270f1dbe8812875507eaa3c10ecd1d7dd2e854efadcd1d6` |
| `exception_policy.json` | `07a21570a027af1d68263504bd18225dc0f2624eca724040aabadb6dbfd1585b` |
| `2003_format_review.json` | `2b102f8f49e7719e833aa5c1ecea70b6a1556b25ef32bffe70c0093366379fe9` |
| `2025_aggregate_review.json` | `02dec44264a87b9acc114fd8294f01336af4fec505d9dd4c2311dbd05ebc6fd4` |
| `review_manifest.json` | `46cca6dd670a50f476f5f2d2d06f879b69c14e72ec7cf9ecea1ec75febb4351a` |

## Approved modern standardization — 21 November 2026

This section records the user's subsequent authorization and supersedes the earlier
pending-policy restriction for **technical standardization only**. The earlier
acquisition, investigation and sealed review remain intact. No source score has
been changed and no additional historical result has been inferred.

The user approved retaining both Catania played scores in the source archive,
recording administrative decisions separately, and holding both matches out of
the screened derivative. This authorizes processing without claiming that the
ultimate legal results have been established. No further historical investigation,
application integration or model training is part of this step.

### Administrative evidence and decisions

- **E1, Catania–Siena, 12 April 2003:** retain played/source 1–1.
  [FIGC CU 4/A, 2 July 2003](https://files.figc.it/version/c%3AMjAxMDAzZDAtM2NlYS00%3AOTcyYWU1MmYtYjM3ZC00/C_2_ContenutoGenerico_4963_lstAllegati_Allegato0_upfAllegato.pdf)
  reinstates the CAF 2–0 award in operative paragraph 1, while paragraph 2 refers
  consequential matters to arbitration. Record 2–0 **as of that decision**, not as
  a certified ultimate final result. **UNRESOLVED / HOLD OUT.**
- **E5, Catania–Venezia, 17 May 2003:** retain played/source 2–0.
  [Original FIGC CAF CU 4/C, meeting of 16 July 2003](https://www.figc.it/FigcLegacyAssets/Assets/contentresources_2/ContenutoGenerico/602/C_2_ContenutoGenerico_5185_lstAllegati_Allegato0_upfAllegato.pdf),
  printed pages 28/4–30/4, establishes the administrative 0–2 award. This upgrades
  the evidence for the award itself from the earlier secondary-only assessment.
  Later court intervention remains a lead: the indexed
  [13 August contemporary report](https://www.corriere.it/Primo_Piano/Sport/2003/08_Agosto/13/catania.shtml)
  describes interim suspension; full retrieval failed, and it is not proof of
  final annulment or homologation. **UNRESOLVED / HOLD OUT.**

These primary texts were consulted during the preceding read-only investigation.
The new `standardization_decisions.json` records URLs, decision dates, findings,
access limits and user approval separately. It is a transcription supplement, not
newly downloaded PDF source bytes. Existing `verification/*` evidence, pending
score candidates and their seal were not rewritten.

### Transformation and outputs

`scripts/standardize_serie_b_results.py` reuses the existing source audit and
review checker, then the shared `convert_rows` → historical importer → public
historical loader/validator. The standard schema is exactly
`match_id,date,league,season,home_team,away_team,home_goals,away_goals`; league is `Serie B`
and seasons use YYYY/YYYY. Source team spellings are preserved. Outcomes are
checked against goals through the importer; no extra outcome column is invented.

The one verified, checksum/physical-line/full-fact-bound Torino–Genoa correction
changes **1997-09-28 to 1997-09-27** only in derived records. Its deterministic
match ID uses the corrected date. Both Catania score candidates remain unapplied.
The seven early seasons, 1990/91–1996/97, are not standardized.

All artifacts below are private under `data/private/italy/serie_b/`:

| Artifact | Purpose |
|---|---|
| `standardization_protected_before.json` | SHA-256 baseline of all 423 pre-existing private files, covering every previously standardized competition and the original Serie B review |
| `standardization_decisions.json` | Approved hold policy and separate administrative evidence |
| `serie_b_standardized_1997_2025.csv` | Screened technical derivative; physically omits all five restricted fixtures |
| `serie_b_audit_archive_1997_2025.csv` | Full derived audit archive; contains excluded/held rows and **must not be used as model-training input** |
| `serie_b_exceptions_1997_2025.json` | Five exact source/match-ID links, reasons, retained statuses, approval and training limitations |
| `serie_b_standardization_manifest.json` | Input/output fingerprints, source links, coverage, counts, applied date correction, importer results, code hashes and limitations |

Counts are measured from parsed and partitioned records, not used as a preset
accepted-output target:

| Category | Records | Reason |
|---|---:|---|
| Modern source/audit archive | 12,302 | 29 complete regular seasons, 1997/98–2025/26 |
| Accepted into screened derivative | 12,297 | Pass technical checks; none of the five identified restricted fixtures |
| EXCLUDED | 3 | E2 fixing case; E3 and E4 unplayed administrative awards |
| UNRESOLVED / HOLD OUT | 2 | E1/E5 ultimate administrative outcomes unresolved |

The categories reconcile as 12,297 + 3 + 2 = 12,302. “Accepted” is technical
inclusion, **not** a claim that every unlisted match is training-eligible.
Unlisted training suitability remains unresolved. Football-Data's existing
academic/private-use and no-AI-training/commercial-clearance restrictions remain;
OpenFootball CC0 covers only rights held. No new training or redistribution
permission is inferred, and no application data path is changed.

### Verification

The adapter verifies full source season coverage before screening, season date
bounds (including the documented 2019/20 extension), nonblank distinct teams,
integer nonnegative goals, consistent results, unique home/away season fixtures,
unique deterministic IDs, and absence of same-team/date collisions. The shared
importer must accept every supplied row without rejection, duplication, conflict
or fact normalization. Reverse input order must produce identical archive bytes;
the screened subset is independently reconverted through the same importer.
Every restricted case must link exactly once, and the screened IDs must be
disjoint from all five exception IDs. A missing or altered decision fails closed.

`--check` regenerates all four outputs and compares their bytes without replacing
saved outputs. Default creation refuses existing outputs. All protected file
hashes are checked before and after building. No originals, previous competition
artifacts or sealed evidence are overwritten. Synthetic guard tests are in
`tests/test_serie_b_standardization.py`; final execution results follow below.

Execution results on 21 November 2026:

- Standardization creation and full `--check` regeneration: **PASS**, byte-identical
  screened CSV, audit archive, exception sidecar and manifest.
- Existing structural audit (also rerun by the review checker), 39-sample sealed
  review, correction/source bindings and aggregate checks: **PASS**. Its historical
  `corrections_applied: 0` describes the unchanged original review; the new
  standardization manifest separately records the one applied derivative date.
- New synthetic standardization tests: **19 passed**. Full repository regression
  suite: **654 passed**.
- Independent saved-output checks: screened IDs exclude all five restricted cases;
  the archive retains both Catania played scores; Torino–Genoa has the corrected
  date in both derivatives; the public historical loader accepts the screened CSV.
- All **423** pre-existing private file hashes match, including the five previously
  standardized competitions. All **429** current private files are ignored by Git;
  zero private paths are tracked. `git diff --check` passes.

No commit, push, merge, model training or application integration was performed.
