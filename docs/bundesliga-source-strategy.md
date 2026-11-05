# Bundesliga historical source investigation

Reviewed 2026-11-05. Scope: candidate inventories and bounded direct-download samples, not full acquisition, standardization or model integration. All downloaded material and diagnostic outputs are in Git-ignored `data/private/germany/source_study/`. Existing DFB parser, tests and reports were left unchanged.

## Recommendation

A practical provisional combination is **deadangel33 CSVs for 1990/91–1992/93, DataHub CSVs for 1993/94–2025/26, and a separately refreshed OpenFootball 2026/27 snapshot for ongoing results**. This minimizes format changes while covering every completed target season at file-inventory level. OpenFootball is also a useful alternative for 2010/11–2025/26, particularly for annotated exceptional results. Recommendations remain subject to upstream rights clarification and validation of every acquired season; an inventory entry is not a completeness certificate.

There is **no missing completed-season file** across the combined inventories. Remaining gaps are uninspected season contents, uncertain per-record upstream rights/lineage, reliable independent verification, and stale ongoing coverage. None of the three should be described as a fully cleared, independently verified 1990–2026 database yet.

## Source evidence and rights

### D — deadangel33/de-deutschland

[Repository](https://github.com/deadangel33/de-deutschland), pinned commit `f64e042d22d2f2a9887c8336125d748ef93269bc` (2018-07-23). GitHub identifies it as a fork of `footballcsv/deutschland`. Its untruncated file inventory includes top-tier `1-bundesliga.csv` files for every target season from 1990/91 to 2017/18, but none later. Paths have decade directories; do not confuse `2-bundesliga2.csv` with the top tier.

The [source declaration](https://github.com/deadangel33/de-deutschland/blob/f64e042d22d2f2a9887c8336125d748ef93269bc/SOURCES.md) names an open-sport forum and Football-Data.co.uk. It does not map individual seasons or rows to an original contributor/source. The [licence](https://github.com/deadangel33/de-deutschland/blob/f64e042d22d2f2a9887c8336125d748ef93269bc/LICENSE.md) is CC0 1.0. This grants/waives the affirmer's rights, not unknown third-party rights; its section 4 disclaims title/non-infringement warranties and responsibility for clearing others' rights. Early-season original provenance remains unresolved. The old fork is reproducibly pinned but unmaintained; it should not be selected over newer sources solely because it is CSV.

### H — DataHub german-bundesliga

[Dataset](https://datahub.io/football/german-bundesliga), [actual resource manifest](https://datahub.io/football/german-bundesliga/_r/-/datapackage.json). The manifest lists **33 CSVs, 1993/94–2025/26**; no 1990/91–1992/93 or 2026/27 resource. This supersedes the landing page's stale “last 10 seasons” synopsis. Advertised direct resource URLs resolve successfully. Metadata supplies ISO-8859-1 encoding and ISO dates. The [README](https://datahub.io/football/german-bundesliga/_r/-/README.md) identifies Football-Data.co.uk as upstream and declares ODC-PDDL-1.0.

The [PDDL](https://opendatacommons.org/licenses/pddl/1-0/) permits broad use of the rights dedicated, but only rights the dedicator owns. [Football-Data](https://football-data.co.uk/germanym.php) explicitly offers CSV downloads for quantitative testing; its homepage also reserves rights. Its [data notes](https://football-data.co.uk/notes.txt) credit XScores for current results and several other services for statistics. A broad upstream open-data licence or complete sublicense/clearance chain was not established. The guessed `/terms.php` page was inaccessible and supplies no usable evidence. Do not equate free downloading with unrestricted redistribution/model deployment. Clarify intended reuse with DataHub/upstream if needed; do not assert an unobserved prohibition.

### O — openfootball/deutschland

[Repository](https://github.com/openfootball/deutschland), pinned commit `c34532ab6950aa0089ef1c736ffdb8c818c3356f` (2026-09-21). Main top-tier Football.TXT files exist for **2010/11–2026/27**. The [CC0 licence](https://github.com/openfootball/deutschland/blob/c34532ab6950aa0089ef1c736ffdb8c818c3356f/LICENSE.md) has the same third-party-rights limitations. Main-file row-level origins are not fully documented by the inspected README/notes.

Separate `openliga/` files are explicitly [converted from OpenLigaDB](https://github.com/openfootball/deutschland/blob/c34532ab6950aa0089ef1c736ffdb8c818c3356f/openliga/README.md). OpenLigaDB's [own homepage](https://www.openligadb.de/) says its community API data uses **ODbL**, so do not apply repository CC0 alone to those conversions. Attribution/share-alike and database-use obligations need assessment if that upstream is selected. The dedicated licence/terms endpoints exposed little usable text in the web tool; the homepage licence statement is available. The presence of `rsssf/` notes does not prove that every main file came from RSSSF; neither a full main-file lineage nor RSSSF reuse clearance was established. Avoid combining folders or importing `1-bundesliga-full.txt` alongside its summary as separate fixtures.

**Independence:** D and H share a declared Football-Data upstream, so their agreement is not independent certification. O may provide useful cross-checks but lacks established independent lineage for every main-file row. Use official Bundesliga/DFL result records for modern match samples and official DFB historical records/decisions for older matches and exceptions, through permitted bounded manual access or approved exports. Do not resume DFB automated collection. No messages requesting permissions were sent.

## Actual season coverage and completeness evidence

The table below is generated from the two saved untruncated GitHub file inventories and DataHub's resource manifest. Exact file paths, recommendations and independent-verification routes for **each season** are in private `coverage.csv` / `coverage.json`.

“Pair-complete sample” means the entire downloaded season sample has the expected scored record count, distinct teams and every ordered home/away pair once, with valid inspected dates/scores and no parser issues. It does not establish independent result accuracy or legal clearance. “File present; completeness unverified” means exactly that: it was inventoried but not downloaded/count-validated. No untested season is labelled complete. For ongoing 2026/27, 306 is schedule capacity, not an expected completed-results count.

| Season | Expected teams / matches | deadangel33 (D) | DataHub (H) | OpenFootball (O) | Recommended primary |
|---|---:|---|---|---|---|
| 1990/1991 | 18 / 306 | 306 scored/18 teams; pair-complete sample | absent | absent | D (provisional) |
| 1991/1992 | 20 / 380 | 380 scored/20 teams; pair-complete sample | absent | absent | D (provisional) |
| 1992/1993 | 18 / 306 | 306 scored/18 teams; pair-complete sample | absent | absent | D (provisional) |
| 1993/1994 | 18 / 306 | file present; completeness unverified | 306 scored/18 teams; pair-complete sample | absent | H (provisional) |
| 1994/1995 | 18 / 306 | file present; completeness unverified | file present; completeness unverified | absent | H (provisional) |
| 1995/1996 | 18 / 306 | file present; completeness unverified | file present; completeness unverified | absent | H (provisional) |
| 1996/1997 | 18 / 306 | file present; completeness unverified | file present; completeness unverified | absent | H (provisional) |
| 1997/1998 | 18 / 306 | file present; completeness unverified | file present; completeness unverified | absent | H (provisional) |
| 1998/1999 | 18 / 306 | file present; completeness unverified | file present; completeness unverified | absent | H (provisional) |
| 1999/2000 | 18 / 306 | file present; completeness unverified | file present; completeness unverified | absent | H (provisional) |
| 2000/2001 | 18 / 306 | file present; completeness unverified | file present; completeness unverified | absent | H (provisional) |
| 2001/2002 | 18 / 306 | file present; completeness unverified | file present; completeness unverified | absent | H (provisional) |
| 2002/2003 | 18 / 306 | file present; completeness unverified | file present; completeness unverified | absent | H (provisional) |
| 2003/2004 | 18 / 306 | file present; completeness unverified | file present; completeness unverified | absent | H (provisional) |
| 2004/2005 | 18 / 306 | file present; completeness unverified | file present; completeness unverified | absent | H (provisional) |
| 2005/2006 | 18 / 306 | 306 scored/18 teams; pair-complete sample | file present; completeness unverified | absent | H (provisional) |
| 2006/2007 | 18 / 306 | file present; completeness unverified | file present; completeness unverified | absent | H (provisional) |
| 2007/2008 | 18 / 306 | file present; completeness unverified | file present; completeness unverified | absent | H (provisional) |
| 2008/2009 | 18 / 306 | file present; completeness unverified | file present; completeness unverified | absent | H (provisional) |
| 2009/2010 | 18 / 306 | file present; completeness unverified | file present; completeness unverified | absent | H (provisional) |
| 2010/2011 | 18 / 306 | file present; completeness unverified | file present; completeness unverified | 306 scored/18 teams; pair-complete sample | H (provisional) |
| 2011/2012 | 18 / 306 | file present; completeness unverified | file present; completeness unverified | file present; completeness unverified | H (provisional) |
| 2012/2013 | 18 / 306 | file present; completeness unverified | file present; completeness unverified | file present; completeness unverified | H (provisional) |
| 2013/2014 | 18 / 306 | file present; completeness unverified | file present; completeness unverified | file present; completeness unverified | H (provisional) |
| 2014/2015 | 18 / 306 | file present; completeness unverified | file present; completeness unverified | file present; completeness unverified | H (provisional) |
| 2015/2016 | 18 / 306 | file present; completeness unverified | 306 scored/18 teams; pair-complete sample | 306 scored/18 teams; pair-complete sample | H (provisional) |
| 2016/2017 | 18 / 306 | file present; completeness unverified | file present; completeness unverified | file present; completeness unverified | H (provisional) |
| 2017/2018 | 18 / 306 | 306 scored/18 teams; pair-complete sample | file present; completeness unverified | file present; completeness unverified | H (provisional) |
| 2018/2019 | 18 / 306 | absent | file present; completeness unverified | file present; completeness unverified | H (provisional) |
| 2019/2020 | 18 / 306 | absent | file present; completeness unverified | file present; completeness unverified | H (provisional) |
| 2020/2021 | 18 / 306 | absent | file present; completeness unverified | file present; completeness unverified | H (provisional) |
| 2021/2022 | 18 / 306 | absent | file present; completeness unverified | file present; completeness unverified | H (provisional) |
| 2022/2023 | 18 / 306 | absent | file present; completeness unverified | file present; completeness unverified | H (provisional) |
| 2023/2024 | 18 / 306 | absent | file present; completeness unverified | file present; completeness unverified | H (provisional) |
| 2024/2025 | 18 / 306 | absent | 306 scored/18 teams; pair-complete sample | 306 scored/18 teams; pair-complete sample | H (provisional) |
| 2025/2026 | 18 / 306 | absent | 306 scored/18 teams; pair-complete sample | 306 scored/18 teams; pair-complete sample | H (provisional) |
| 2026/2027 | 18 / 306 | absent | absent | 36 scored/18 teams; ongoing/incomplete | O (separate ongoing; stale, refresh needed) |

## Bounded downloaded-file inspection

Fourteen season files were downloaded: five D CSVs (1990/91, 1991/92, 1992/93, 2005/06, 2017/18), four H CSVs (1993/94, 2015/16, 2024/25, 2025/26), and five O TXT files (2010/11, 2015/16, 2024/25, 2025/26, 2026/27). This is 10 distinct completed seasons plus ongoing, not the full archive. The 13 completed-season snapshots appear pair-complete: 306 scored matches/18 teams each except D 1991/92 with 380/20. Every inspected completed snapshot has no missing required parsed fields, duplicate ordered pairs or unparsed candidate rows. DataHub FTR values agree with goals. Full-time rather than halftime scores were read. All scored dates fall within the named season's two calendar years; this does not certify finality independently.

Exact date ranges, per-file issue lists, source hashes and reproducible first/middle/last scored-row samples are in `sample_inspection.json`. Important ranges include:

| Source / season | Scored / teams | First date | Last date |
|---|---:|---|---|
| D 1990/91 | 306 / 18 | 1990-08-08 | 1991-06-15 |
| D 1991/92 | 380 / 20 | 1991-08-02 | 1992-05-16 |
| D 1992/93 | 306 / 18 | 1992-08-14 | 1993-06-05 |
| H 1993/94 | 306 / 18 | 1993-08-07 | 1994-05-07 |
| D 2005/06 | 306 / 18 | 2005-08-05 | 2006-05-13 |
| O 2010/11 | 306 / 18 | 2010-08-20 | 2011-05-14 |
| H / O 2015/16 | 306 / 18 each | 2015-08-14 | 2016-05-14 |
| D 2017/18 | 306 / 18 | 2017-08-18 | 2018-05-12 |
| H / O 2024/25 | 306 / 18 each | 2024-08-23 | 2025-05-17 |
| H / O 2025/26 | 306 / 18 each | 2025-08-22 | 2026-05-16 |
| O 2026/27 | 36 / 18 | 2026-08-28 | 2026-09-20 |

### Format and data-quality findings

- D embeds weekday/week annotations in dates and per-team game-count suffixes such as `(1)` in team fields. Inspection removed only these syntactic annotations in memory; raw bytes remain untouched. Do not treat the suffix as part of club identity. Historical-looking labels may be retrospectively named, e.g. `KFC Uerdingen`; source display names are not a certified historical naming registry.
- O main-file syntax changes: older files use `home v away score`, whereas 2025/26 uses `home score (halftime) away` and multiline scorer annotations. The private inspection harness explicitly handles both and ignores balanced scorer annotation blocks. No existing DFB code was changed or repurposed. A production TXT adapter would need its own documented grammar and tests using the existing importer, not this bounded research harness.
- The 2026/27 O file contains 306 scheduled pairings but only 36 scored records through September 20. Repository commit date is September 21; the review is November 5. It is an incomplete/stale snapshot, not current ongoing coverage. Future fixtures must not become zero-score matches. Freshness and explicit finished-state checks remain necessary.
- H and O both encode Union Berlin–Bochum on 2024-12-14 as **0–2 awarded**, whereas the on-field score was 1–1. O retains an `[awarded]` annotation; H leaves halftime and statistics blank. The official [Bundesliga record](https://www.bundesliga.com/en/bundesliga/matchday/2024-2025/14/1-fc-union-berlin-vs-vfl-bochum-1848/news) and [DFB ruling](https://www.dfb.de/news/dfb-bundesgericht-weist-berufung-von-union-berlin-zurueck) explain the award. This is a semantic exception, not a discovered source disagreement. Define on-field FT versus officially awarded outcome before standardization; retain both source notation and ruling provenance, never silently replace a score. Null halftime/statistics are acceptable for this results-only task; null date/team/FT goals are not.
- Cross-source spelling differences include `Bayern Munich` / `Bayern München` / `FC Bayern München`, `Hamburg` / `Hamburger SV`, and abbreviated Mönchengladbach names. Preserve originals and maintain a reviewed, versioned identity map separately. Counts alone cannot detect a correctly sized but incorrect score/date dataset.

## Acquisition strategy — direct files, no DFB crawler

1. **Resolve use conditions.** Retain the displayed CC0/PDDL documents and upstream declarations; establish the permitted scope of local collection, transformations and intended future TOTOdology use. Clarify the early fork's original contributions and DataHub's upstream sublicense basis. If using OpenLigaDB-derived files, record ODbL obligations or obtain another grant. Do not publish raw/derived data or assume repository licensing clears all third-party rights. These uncertainties are not an assertion that private factual analysis is prohibited.
2. **Freeze the inventory.** For the provisional primary combination, download exactly three early CSVs at the verified D commit plus the 33 H resources, rather than cloning repositories or harvesting web match pages. Pin GitHub URLs to commits. DataHub resource URLs are mutable: save the retrieved package, final redirected URL, UTC time, status, encoding, size, SHA-256 and immutable private bytes. If publisher versions/commit IDs become available, retain them too. Do not re-download already cached verified samples unnecessarily.
3. **Preserve separate snapshots.** Keep originals, provenance and diagnostics under ignored `data/private/germany/`; refuse overwrites and version corrections. Store ongoing O 2026/27 separately. Refresh from a permitted current repository snapshot or explicitly licensed upstream API only after resolving its licence and final-status semantics. Do not pretend the stale 36-record snapshot fills the current ongoing gap.
4. **Polite bounded transport.** Use a fixed allowlisted resource list, one concurrent request and a conservative delay (proposed at least five seconds unless provider guidance specifies otherwise). Cache successful immutable bytes and cap ordinary transient retries with backoff. Honor Retry-After; stop for 401/403/429, challenge pages or changed terms. No CAPTCHA solving, impersonation, proxy rotation or DFB fetching. Prefer publisher dataset exports/API routes over any scraping.
5. **Validate each season before acceptance.** Target Bundesliga regular-season top tier, excluding 2. Bundesliga, DFB-Pokal and relegation playoffs. Normally require 18 teams, 306 matches, 34 games per club (17 home/17 away); 1991/92 requires 20, 380 and 38 (19/19). Across 36 completed seasons expect 11,090 regular-season records. Check every ordered team pairing exactly once, required dates/teams/nonnegative integer FT scores, duplicates, result consistency, plausible season dates and retained rescheduling dates. Detect alias collisions and source conflicts; quarantine ambiguous/awarded/abandoned records for a documented outcome policy. Historical competition remains the Bundesliga top tier; do not import the separate East German league in 1990/91 as additional Bundesliga matches. A three-point league table should not be assumed for early seasons; match validation does not need points rules.
6. **Independent verification.** Select deterministic samples from every decade, the 20-team season, postponed/replayed/awarded cases and source handovers. Compare date, teams, competition and score to permitted official Bundesliga/DFL or DFB records. Existing legitimately saved DFB samples can be reused offline without touching the parser or requesting new DFB pages. Record source URLs and alias/outcome differences. H versus D is a lineage cross-check; O agreement alone is not certified independent. No systematic external verification was performed in this source study beyond the awarded-match source check.
7. **Separate later standardization.** Once structural validation, independent samples and legal-use requirements are satisfied, implement narrowly scoped source adapters into existing historical import/validation infrastructure. Preserve source spellings and provenance, generate deterministic IDs and validate byte reproduction. This study creates no standardized Bundesliga dataset and performs no training, evaluation or application integration.

## Reproduction and safeguards

Private `metadata_retrieval.json`, `sample_retrieval.json`, `supplement_retrieval.json`, saved repository/commit metadata and `artifact_checksums.json` record the evidence. GitHub commit metadata was checked against the saved inventory references. No source repositories were cloned. The fixed one-off fetch script is retained as evidence only; it refuses existing targets and must not be rerun as a crawler. Offline reproduction:

```sh
python3 data/private/germany/source_study/inspect_samples.py
python3 data/private/germany/source_study/build_coverage.py
```

These commands regenerate only private diagnostics/tables from cached inputs, not original data or standardized model inputs. The source study's research parsers are not production importers. No application or DFB parser/test/report files were edited. England source/extracted/standardized checksums and the existing cross-era DFB artifact checksums were rechecked. No commit or push was made.

## Subsequent project decision: DFB preferred

On 2026-11-05 the user selected official DFB Datencenter as the preferred source, superseding this report's provisional CSV acquisition recommendation. The CSV study remains a historical investigation; it is not the current acquisition plan. See `docs/dfb-bundesliga-collection.md` for the DFB-only offline/authorized-access pipeline and its unresolved permission/status gates. No CSV sources are used by that pipeline.

## Latest project decision: direct CSV acquisition

On 2026-11-05 the user selected direct historical CSV acquisition: deadangel33 for 1990/91–1992/93 and DataHub for 1993/94–2025/26, superseding the intervening DFB-only acquisition decision. Ongoing 2026/27 remains deferred. The DFB implementation and experiments are preserved. See `docs/bundesliga-validation.md` for the completed 36-season acquisition, reviewed exceptions and unresolved upstream rights.
