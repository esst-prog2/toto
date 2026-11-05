# Historical football data collection plan

Prepared 2026-11-02 on `feature/data-collection`. This is a proposal, not
authorization to collect data. No datasets were downloaded for this document.

## Scope and evidence

Aim for 1993/94–2025/26 completed seasons, retaining earlier reliable records
if a source supplies them. Keep ongoing 2026/27 results in a separate update
stream. For calendar-year leagues, the historical estimate ends at 2025 and
the ongoing stream is 2026; do not invent a 2026/27 label for these leagues.

Evidence levels used below:

- **V-index**: country-page CSV links rechecked on 2026-11-02, without fetching
  datasets. A link proves advertised availability, not complete results or
  a successful download. No missing season links were found within the main
  Football-Data ranges below.
- **V-link/P-boundary**: extra-league CSV/XLSX links rechecked today; earliest
  and latest CSV boundaries come from the earlier investigation in this
  conversation and were not independently re-read for this plan. Continuity
  and match completeness remain unverified.
- **P**: prior conversation findings, explicitly not independently reverified
  here. OpenFootball findings refer to revision
  `e6744429ee395bc86f247348c6184bb08d4eb361`.
- **L**: local repository evidence. The existing spike records 1,312 accepted
  matches: E0 2022/23 (380), E1 2022/23 (552), E0 2023/24 (380).
  See [measurement artifact](../data/real_spike_measurements.json),
  [spike builder](../scripts/build_real_spike_dataset.py), and
  [planning log](../PLANNING_LOG.md). The preceding local trial accepted
  all 380 E0 2024/25 matches from ignored `data/private/E0.csv`, with no rejected
  rows or duplicates; it checked 20 teams and every ordered pairing once.
  That trial is prior run evidence, not a fresh import performed for this plan.

The repository had no standalone OpenFootball/Football-Data coverage report;
earlier research was in the conversation. This document persists it while
distinguishing it from the fresh index/terms checks. The repository's
[README](../README.md) and homework artifacts document the much smaller spike,
not approval or verification of a comprehensive collection.

## Primary competition coverage table

FD = Football-Data.co.uk. Codes are source codes, not inferred filenames.
League identifiers below are proposed stable IDs; the two English IDs follow
existing importer examples. Other IDs are planning choices, not implemented
runtime configuration. Counts exclude the ongoing stream and are **potential
league-seasons**, not verified complete seasons. Match estimates use the
explicit annual planning rates in the table, not downloaded row counts.

| Country / competition | Standard league ID | Primary source / code | Earliest potential season | Latest advertised / historical cutoff | Historical seasons | Approx. historical matches (rate/year) | Format | Limitations and evidence |
|---|---|---|---|---|---:|---:|---|---|
| England — Premier League | `england.premier-league` | FD `E0` | 1993/94 | 2026/27 / 2025/26 | 33 | 12,540 (380) | CSV | V-index + L; older 22-team seasons make fixed-rate estimate approximate. [England](https://www.football-data.co.uk/englandm.php) |
| England — Championship | `england.championship` | FD `E1` | 1993/94 | 2026/27 / 2025/26 | 33 | 18,216 (552) | CSV | V-index + L; historical name Division 1; playoff inclusion must be audited. [England](https://www.football-data.co.uk/englandm.php) |
| Germany — Bundesliga | `germany.bundesliga` | FD `D1` | 1993/94 | 2026/27 / 2025/26 | 33 | 10,098 (306) | CSV | V-index; relegation playoffs not assumed included. [Germany](https://www.football-data.co.uk/germanym.php) |
| Germany — 2. Bundesliga | `germany.2-bundesliga` | FD `D2` | 1993/94 | 2026/27 / 2025/26 | 33 | 10,098 (306) | CSV | V-index; historical format/playoffs require checks. [Germany](https://www.football-data.co.uk/germanym.php) |
| Italy — Serie A | `italy.serie-a` | FD `I1` | 1993/94 | 2026/27 / 2025/26 | 33 | 12,540 (380) | CSV | V-index; historical team counts differed. [Italy](https://www.football-data.co.uk/italym.php) |
| Italy — Serie B | `italy.serie-b` | FD `I2` | 1997/98 | 2026/27 / 2025/26 | 29 | 12,180 (420) | CSV | V-index; 1993/94–1996/97 unavailable here; variable team counts and playoffs. [Italy](https://www.football-data.co.uk/italym.php) |
| Spain — La Liga | `spain.la-liga` | FD `SP1` | 1993/94 | 2026/27 / 2025/26 | 33 | 12,540 (380) | CSV | V-index; historical team-count changes. [Spain](https://www.football-data.co.uk/spainm.php) |
| Spain — Segunda División | `spain.segunda-division` | FD `SP2` | 1996/97 | 2026/27 / 2025/26 | 30 | 13,860 (462) | CSV | V-index; first three target seasons absent; playoffs unverified. [Spain](https://www.football-data.co.uk/spainm.php) |
| France — Ligue 1 | `france.ligue-1` | FD `F1` | 1993/94 | 2026/27 / 2025/26 | 33 | 11,550 (350) | CSV | V-index; changing team counts and shortened seasons invalidate constant totals. [France](https://www.football-data.co.uk/francem.php) |
| France — Ligue 2 | `france.ligue-2` | FD `F2` | 1996/97 | 2026/27 / 2025/26 | 30 | 11,400 (380) | CSV | V-index; first three target seasons absent; format changes. [France](https://www.football-data.co.uk/francem.php) |
| Netherlands — Eredivisie | `netherlands.eredivisie` | FD `N1` | 1993/94 | 2026/27 / 2025/26 | 33 | 10,098 (306) | CSV | V-index; playoff coverage and exceptional seasons need review. [Netherlands](https://www.football-data.co.uk/netherlandsm.php) |
| Portugal — Primeira Liga | `portugal.primeira-liga` | FD `P1` | 1994/95 | 2026/27 / 2025/26 | 32 | 9,280 (290) | CSV | V-index; 1993/94 absent; changing league size. [Portugal](https://www.football-data.co.uk/portugalm.php) |
| Belgium — Pro League | `belgium.pro-league` | FD `B1` | 1995/96 | 2026/27 / 2025/26 | 31 | 8,680 (280) | CSV | V-index; first two target seasons absent; split/playoff structure varies. [Belgium](https://www.football-data.co.uk/belgiumm.php) |
| Turkey — Süper Lig | `turkey.super-lig` | FD `T1` | 1994/95 | 2026/27 / 2025/26 | 32 | 9,792 (306) | CSV | V-index; 1993/94 absent; exceptional seasons/administrative results need checks. [Turkey](https://www.football-data.co.uk/turkeym.php) |
| Scotland — Premiership | `scotland.premiership` | FD `SC0` | 1994/95 | 2026/27 / 2025/26 | 32 | 7,296 (228) | CSV | V-index; 1993/94 absent; team-count and split-stage changes. [Scotland](https://www.football-data.co.uk/scotlandm.php) |
| Austria — Bundesliga | `austria.bundesliga` | FD `AUT`; OF `at.1` | FD 2012/13; OF 2010/11 (P) | FD 2026/27 / 2025/26 | 14 FD | 2,800 (200) | CSV/XLSX; OF JSON | V-link/P-boundary; FD 1993–2012 missing; split stages require audit. [Austria](https://www.football-data.co.uk/austria.php) |
| Switzerland — Super League | `switzerland.super-league` | FD `SWZ`; OF `ch.1` | FD 2012/13; OF 2014/15 (P) | FD 2026/27 / 2025/26 | 14 FD | 2,800 (200) | CSV/XLSX; OF JSON | V-link/P-boundary; FD 1993–2012 missing; historical format changes. [Switzerland](https://www.football-data.co.uk/switzerland.php) |
| Denmark — Superliga | `denmark.superliga` | FD `DNK` | 2012/13 | 2026/27 / 2025/26 | 14 | 3,220 (230) | CSV/XLSX | V-link/P-boundary; earlier history absent; stages and team counts vary. [Denmark](https://www.football-data.co.uk/denmark.php) |
| Sweden — Allsvenskan | `sweden.allsvenskan` | FD `SWE` | 2012 | 2026 / 2025 | 14 | 3,360 (240) | CSV/XLSX | V-link/P-boundary; 1993–2011 missing; 2026 treated as ongoing. [Sweden](https://www.football-data.co.uk/sweden.php) |
| Norway — Eliteserien | `norway.eliteserien` | FD `NOR` | 2012 | 2026 / 2025 | 14 | 3,360 (240) | CSV/XLSX | V-link/P-boundary; 1993–2011 missing; playoff coverage unverified. [Norway](https://www.football-data.co.uk/norway.php) |
| Hungary — NB I | `hungary.nb-i` | No FD; OF `hu.1` (P) | OF 2018/19 | OF 2020/21 | 2 isolated OF seasons | ~396 (198) | JSON | P only: 2018/19 and 2020/21; no continuous history/current season established. [Pinned OF repository](https://github.com/openfootball/football.json/tree/e6744429ee395bc86f247348c6184bb08d4eb361) |
| Hungary — NB II | `hungary.nb-ii` | Neither researched source (P) | Unknown | Unknown | Unknown | Not estimated | Unknown | Separate source research required; not proof that data does not exist elsewhere. [FD source list](https://www.football-data.co.uk/data.php), [OF](https://github.com/openfootball/football.json) |

All FD coverage remains subject to the restrictions below. No 2025/26 file
was newly audited for completeness for this document. Earlier observations
of fresh 2026/27 FD results do not establish a refresh guarantee today.

## OpenFootball as a complementary source

These are **P findings**, preserved from the earlier pinned-revision review,
not a new dataset audit. Inclusive ranges denote file existence. Separate
provider coverage overlaps FD and must not be added to its totals.

| Target league(s) / OF code | Previously observed files | Important quality findings from prior inspection |
|---|---|---|
| Premier League `en.1`; Bundesliga `de.1` | 2010/11–2026/27 | 2025/26: 380/380 and 306/306 scored; alternate `-full` files exist. |
| Championship `en.2` | 2010/11–2015/16; 2018/19–2026/27 | 2016/17–2017/18 absent; 2025/26 557/557 includes playoffs. |
| 2. Bundesliga `de.2` | 2012/13–2025/26 | 2025/26 only 99/306 scored; no 2026/27. |
| Serie A `it.1` | 2013/14–2026/27 | 2025/26 380/380 scored. |
| Serie B `it.2` | 2013/14–2020/21; 2024/25–2025/26 | 2021/22–2023/24 absent; 2025/26 only 309/380 scored. |
| La Liga `es.1` | 2012/13–2026/27 | 2025/26 380/380 scored. |
| Segunda `es.2` | 2012/13–2020/21; 2024/25–2025/26 | 2021/22–2023/24 absent; 2025/26 only 131/462 scored. |
| Ligue 1 `fr.1` | 2014/15–2026/27 | 2025/26 305/306 scored; one marked canceled. |
| Ligue 2 `fr.2` | 2014/15–2020/21; 2024/25–2025/26 | 2021/22–2023/24 absent; 2025/26 only 116/306 scored. |
| Eredivisie `nl.1` | 2018/19–2026/27 | 2025/26 305/306 scored; one canceled, regular-season scope. |
| Primeira Liga `pt.1` | 2018/19–2026/27 | 2025/26 306/306 scored. |
| Belgium `be.1`; Turkey `tr.1`; Scotland `sco.1` | 2018/19–2020/21; 2024/25–2025/26 | 2021/22–2023/24 absent; 2025/26 respectively 104/240, 99/306, 63/198 scored; Belgian/Scottish later stages absent. |
| Austria `at.1` | 2010/11–2025/26 | Prefer 2025/26 `at.1-full.json`: 195/195 including split/playoffs; ordinary file only 71/132 scored. Could add two pre-FD seasons if validated. |
| Switzerland `ch.1` | 2014/15; 2018/19–2020/21 | 2020/21 180/180 scored; does not extend FD history. |
| Hungary `hu.1` | 2018/19; 2020/21 | 198/198 scored in each; isolated coverage only. |
| Hungary NB II; Denmark; Sweden; Norway | No files found in prior complete index | Reverify absence before rejecting OF as a future option. |

Earlier 2026/27 OF inspection found files for eight targets only: Premier
League, Championship, Bundesliga, Serie A, La Liga, Ligue 1, Eredivisie,
Primeira Liga. Each stopped recording results on 2026-09-20. The
[README](https://github.com/openfootball/football.json#frequently-asked-questions--answers)
explains that JSON generation is daily but upstream text updates are not
automatic. Generation frequency is not a freshness guarantee.

JSON is not accepted by the existing CSV importer. A separately approved,
tested adapter would have to handle both `score.ft` and direct score arrays,
preserve source identity/status, and map teams only with verified evidence.
Do not relabel JSON or merge providers as if they were one source.

## Source restrictions and unresolved permissions

Reviewed public documentation on 2026-11-02; this section records provider
statements, not a legal determination. Source access permissions and file
privacy are separate questions.

| Use | Football-Data.co.uk | OpenFootball football.json |
|---|---|---|
| Personal research | Page describes free data for private individuals; its model-training wording leaves the precise TOTOdology use unresolved. | CC0 supports reuse of rights held by the affirmer. |
| Academic/classroom research | No blanket academic exception verified; ask about this specific educational prediction project. | No academic-only limitation in CC0. |
| Automated downloading / bulk collection | No permission for this collection verified; page explicitly restricts products using bots/scrapers/AI. Do not treat accessible URLs as consent. | CC0 permits copying; it does not waive GitHub access/rate limits. No unlimited-download service promise verified. |
| Model fitting / training | Explicit restrictive wording creates an unresolved issue even for locally stored data. | CC0 has no model-training restriction on the affirmer's rights. |
| Redistribution / public datasets | No redistribution grant verified. Existing homework publication does not establish permission for new publication. | CC0 permits redistribution under the rights waived; third-party rights are not guaranteed. Project policy still keeps collected data local. |
| Use in Streamlit/application | Clarify private classroom demo versus hosted/public or commercial service and whether displaying derived outputs is permitted. | CC0 supports application reuse; quality and third-party-rights limitations remain. |

FD evidence: [data page](https://www.football-data.co.uk/data.php) states use
is intended for private individuals and excludes commercial or data-training
products using automated tools. Its language does not settle this project's
specific permission. Obtain a written answer covering manual versus scripted
collection, volume, academic model fitting, local application use, hosted
demonstrations, derived predictions, and raw/normalized redistribution.
No contact is sent as part of this task. The
[disclaimer](https://www.football-data.co.uk/disclaimer.php) disclaims accuracy;
it is not a redistribution license.

OF evidence: the repository's
[LICENSE.md](https://github.com/openfootball/football.json/blob/master/LICENSE.md)
is CC0 1.0 Universal. The [CC0 explanation](https://creativecommons.org/publicdomain/zero/1.0/)
supports copying, adaptation and distribution, including commercial use,
subject to rights outside the dedication. The license disclaims accuracy and
third-party-rights warranties. Record the exact revision and license at later
acquisition; do not infer that every upstream site has identical terms.

Keeping data under ignored `data/private/` prevents ordinary Git staging of
untracked files; it neither grants a license nor protects against forced adds,
cloud syncing, deployment packaging, backups or application disclosure. The
workspace is in iCloud: local-to-Git is not proof of device-only storage.
Do not change storage policy or move files without a separate decision.

## Size estimate and counting method

FD main competitions: **480 league-seasons, ~170,168 matches** using the table's
fixed annual rates. Five extra targets add **70 league-seasons, ~15,540 matches**:
**550 league-seasons, ~185,708 matches** in total across 20 targets.

Use **170,000–205,000 matches** as a provisional capacity range, not a statistical
confidence interval or completeness claim. Team-count changes, shortened
seasons, stage inclusion, missing results and eligibility may shift totals.
The 33-season maximum is inclusive 1993/94–2025/26. Calendar histories use
2012–2025 inclusive (14). These counts concern competition-seasons, not 550
distinct calendar years or necessarily 550 separate files.

The two isolated Hungarian OF seasons could add 396 matches and two
league-seasons (552 overall), subject to renewed verification and adaptation.
Austria's two earlier OF seasons could extend coverage further, but no match
estimate is added without checking those files. NB II remains unestimated.
Do not double-count the 1,312 existing raw spike rows, generated copies, or the
380-match local trial when collecting overlapping seasons.

Illustrative storage assumptions for ~186k matches:

- Standardized eight-column UTF-8 CSV at 150–250 bytes/match: roughly **28–47 MB**.
- Original provider files, including unused odds/statistics, budget **100–300 MB**;
  this is an unmeasured estimate, not an observed archive size.
- Proposed working allowance **1 GB** for originals, normalized outputs,
  manifests, rejected-row reports and a small number of snapshots. Repeated
  snapshots or a database may need more. This is not a user-approved quota.

Current-season capacity is excluded from the historical totals. Full-season
rates for the 20 FD targets sum to 6,436 matches, but ongoing data must
be counted from validated snapshots, not assumed to have full-season results.

## Proposed priorities and first batch

1. **Permission and inventory first.** Resolve FD usage questions and agree
   storage/privacy scope. Reuse the already downloaded E0 2024/25 file rather
   than fetching it again. Maintain the current homework artifacts unchanged.
2. **Conditional first new collection batch: E0 2025/26, E1 2024/25 and E1
   2025/26.** Three files, approximately **1,484 regular-season matches**
   (380 + 552 + 552; stage scope to verify). They extend the proven English
   source schemas and avoid duplicate downloads of existing spike/trial files.
   Approval requires permitted use and a separate collection instruction.
   Counts are expectations, not verified source totals.
3. **English historical backfill**, starting with a few older seasons to test
   formats, then 1993/94–2025/26 E0/E1 after successful validation. These have
   the strongest local compatibility evidence, not independently measured
   superiority for predicting actual Hungarian TOTÓ tickets.
4. **Other main targets:** D1/D2, I1/I2, SP1/SP2, F1/F2, N1, P1, B1, T1, SC0.
   Prioritize the first divisions and commonly used second divisions, but
   verify actual TOTÓ ticket frequency before claiming a relevance ranking.
   Audit split/playoff competitions separately.
5. **Five shorter-history targets:** AUT, SWZ, DNK, SWE, NOR. Their second CSV
   schema is implemented, but source mappings, season boundaries, stage
   completeness and encoding need real-file trials before wider ingestion.
6. **OpenFootball route:** if FD permission is unavailable, reassess a smaller
   CC0 collection rather than bypassing restrictions. Reverify pinned file
   coverage, approve adapter work, then trial selected completed seasons.
   Its shorter coverage cannot replace the 30-year plan wholesale.
7. **Hungary source research runs separately:** investigate official MLSZ
   results/archives, league and club records, and appropriately licensed
   alternatives for NB I and NB II. These are research candidates only:
   no CSV access, coverage dates, bulk rights or automation permission have
   been verified. Investigate earlier Austrian/Swiss/Scandinavian history
   separately after the core collection is proven.

Keep 2026/27 (calendar 2026) out of immutable completed-season snapshots.
FD advertises at least twice-weekly updates on its data page; observe actual
last-result dates and keep retrieval timestamps. Existing OF freshness
findings make it unsuitable as an assumed live feed. No updater is approved
or implemented here.

## Proposed acquisition and acceptance workflow

For a later authorized trial/batch:

1. Prepare a manifest with explicit league ID, provider competition mapping,
   source URL, canonical season, stage scope, expected-count rationale,
   rights evidence, retrieval timestamp and raw SHA-256. For extra FD files,
   explicitly map `Country` and `League`, not the filename.
2. Preserve originals under ignored storage without overwriting existing
   files. Use separate raw, normalized, diagnostics and ongoing snapshots;
   exact directory names and manifest implementation remain proposals.
3. Use the existing importer documented in
   [historical-import.md](historical-import.md). It returns records and reports
   in memory; persistence and an acquisition manifest are not implemented.
4. Inspect accepted/rejected/fixture/duplicate/conflict counts. Quarantine
   conflicts; never silently select scores or drop rejected rows. Validate
   team/date coverage, home-away pairing counts and stage-aware expectations.
   A season with fewer rows is not automatically a bad source: canceled games
   and changed formats need evidence. CSV availability alone is insufficient.
5. Review UTF-8 versus legacy encodings explicitly, historical date forms,
   trailing empty columns and source result/goal consistency. Do not guess
   team aliases. Keep corrections and provenance separate from raw files.
6. Keep providers separate until cross-provider identity reconciliation is
   approved. The importer intentionally rejects different source mappings
   assigned to one league within a call. Matching names/dates are not proof
   of independent corroboration; providers may share upstream sources.
7. Validate normalized data through existing structures but do not feed a
   combined multi-league history to the predictor: the current workflow does
   not isolate competitions. Keep existing evaluations frozen and define a
   new chronological training/development/held-out split before modeling.
8. Check Git exclusion and staging before any later commit; no new raw or
   normalized datasets belong in public Git. Separate future deployment
   artifact checks from Git ignore checks.

## Uncertainties and approval checkpoints

- Actual complete FD row counts across all advertised seasons are unresolved.
  The five extra histories have not had continuity independently reverified.
- The earlier OF coverage/quality audit is revision-specific and needs renewed
  confirmation before any acquisition; its historical files are not uniformly
  complete. Source format compatibility requires additional adapter work.
- Hungary's long-term sources and pre-2012 extra-league history remain open.
- Obtain/record FD permission before expanded use or automated collection;
  if unavailable, choose a permissible alternative and accept reduced scope.
- User decisions needed before action: approve a permitted source route and
  the bounded first batch; clarify private/classroom/hosted use and iCloud
  storage expectations; approve any later adapter, persistence or integration
  work. None of these approvals is inferred from this planning task.

Only this document and append-only planning entries are changed by this task.
No source code, application, predictor, raw data or evaluation results change.

## Bundesliga source decision and implementation (2026-11-05)

The user selected official DFB Datencenter for Bundesliga history, superseding provisional Football-Data/DataHub/OpenFootball acquisition recommendations for this competition. `docs/dfb-bundesliga-collection.md` describes the implemented DFB-only pipeline, 18-/20-team format gates, private cache/provenance, response-bound status reviews and explicit written-authorization gate. Only the six existing bounded sample pages have been processed offline; no complete Bundesliga season, approved archive export or archive-wide network authorization is available. Prediction/training/evaluation integration remains outside scope.

## Latest Bundesliga acquisition decision (2026-11-05)

The user selected direct CSVs for completed Bundesliga history: pinned deadangel33 originals for 1990/91–1992/93 and DataHub originals for 1993/94–2025/26. This supersedes the intervening DFB-only collection plan; preserve its code/experiments. All 36 selected files are now acquired privately (11,090 match records). See `docs/bundesliga-validation.md`: 35 seasons pass the reviewed stage, while 1993/94 retains an unresolved replay-date discrepancy. Independent result verification, an administrative-outcome policy and upstream-rights assessment precede standardization/integration; ongoing 2026/27 is deferred.

## Completed Bundesliga CSV preparation (2026-11-05)

The later review resolved the Bayern–Nürnberg replay date as 1994-05-03; only the derived standardized dataset applies the checksum-bound correction. All 36 seasons and 11,090 source records are preserved, independently sampled and standardized privately, with five match-ID-linked exception records. Full fixture coverage and reproducibility passed. The earlier DFB pipeline remains a separately preserved, permission-gated alternative; no archive-wide DFB collection occurred. Upstream third-party rights and ordinary-training suitability for unreviewed matches remain unresolved. See `docs/bundesliga-validation.md` for the staged history, evidence and current readiness. No model integration, training or evaluation is authorized by this preparation.
