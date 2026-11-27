# UEFA Champions League — Phase 4 standardization and independent validation

**PASS WITH LIMITATIONS for private technical standardization.** Owner-authorized
Phase 4 only, completed 2026-11-27 in the original `toto` worktree on
`feature/data-collection`. Historical upstream independence and downstream rights
remain limited; technical verification does not establish training or publication
permission. No Phase 5, UCL model integration, statistical change, training,
backtesting, acquisition, staging, commit or push was performed.

## Executive summary and approved-baseline reconciliation

The private canonical v2 dataset contains **6,642 unique matches across all 34
seasons, 1992/93–2025/26: 4,127 main and 2,515 qualifying**. Dispositions reconcile
exactly to **6,642 INCLUDE / zero HOLD OUT / three NOT PLAYED**, with **three
additional OUT OF SCOPE attempts** retained separately. All 6,648 reviewed events
and all 12,211 source observations remain accounted for without double-counting.
The 692 recovered qualifying descriptions contribute 690 played matches and two
no-kickoff descriptions; the third NOT PLAYED belongs to the frozen earlier corpus.

The accepted [Phase 3](uefa-champions-league-phase3.md) decisions, 41 earlier fixture
originals, supplemental revisions/Curley original, evidence and receipts are frozen.
Eight incorrect numeric regulation scores and four football dates are repaired
through approved derived decisions. Three independently supported resolutions of
previously unknown regulation periods are counted separately from those eight
numeric repairs. No new historical adjudication was made. The earlier baseline's
188 tests remain covered by the complete current suite.

Unified schema v2 appends `neutral_venue`. UCL counts are **6,584 zeros / 58 ones /
zero NA** under the newly approved **official competition-format definition**.
All **156,579 current domestic rows in 16 CSVs across 14 competitions** were extended:
156,579 zeros, zero ones, zero NA. Every prior domestic field, ID and row order is
unchanged, and removing the new column reproduces every original CSV byte-for-byte.

## Private output and traceability

All detailed deliverables remain Git-ignored under
`data/private/europe/champions_league/phase4/`:

- `validated/uefa_champions_league_standardized_1992_2026.csv`: 6,642 data rows,
  939,615 bytes, SHA-256
  `58c4b0453ba7176e34179e70004c443c41fcf97bc97606de5506ad2ef90db827`.
- `validated/source_to_output.json`: each output ID/physical row, approved event,
  source contributors, URL/file/hash/physical or decoded locator, decision fingerprint,
  outcome and format-classification rule. Original and corrected score/date values,
  source labels, half-time, after-ET, shootout, reported/calculated aggregate,
  administrative outcomes, continuation dates and physical venue evidence remain
  distinct within the complete frozen decision metadata.
- `validated/season_coverage.json`, `validated/season_stage_neutrality.json`:
  the 34-season and **284 season/scope/stage groups**; classification counts, rule
  IDs and evidence references. No unknown season/stage classification remains.
- `validated/excluded_events.json`: the three no-kickoff events and three
  annulled/superseded attempts, preserved without canonical played-match rows.
- `approval.json`, `format_policy.json`, `format_evidence.json` and
  `format_evidence.supplement.json`: approved input hashes, source-bound exceptional
  format rule, cached format locators and bounded factual method notes.
- `domestic_migration_plan.json`, `domestic_migration_applied.json`,
  `independent_validation.json`, `offline_generation.json`,
  `offline_independent_validation.json`, `preservation.json`, `test_results.json`,
  `completion.json` and `report.md`: private execution/validation and exact appendix.

No unified multi-competition model file or application data replacement was created.

## Season-by-season played coverage

Q includes preliminary, qualifying and qualifying play-off stages. NOT PLAYED is
excluded from both played counts and neutrality counts; it is not a fabricated
regulation result. The three separate OUT OF SCOPE attempts are not standing fixtures.
All NA counts below are zero. Exact unweighted counts are reported; numerical
completeness weights remain **unspecified**, with recent-first priorities unchanged.

| Season | Main | Q played | INCLUDE | NOT PLAYED | Neutral 0 | Neutral 1 |
|---|---:|---:|---:|---:|---:|---:|
| 1992/1993 | 74 | 8 | 82 | 0 | 80 | 2 |
| 1993/1994 | 75 | 20 | 95 | 0 | 94 | 1 |
| 1994/1995 | 61 | 16 | 77 | 0 | 76 | 1 |
| 1995/1996 | 61 | 16 | 77 | 0 | 76 | 1 |
| 1996/1997 | 61 | 16 | 77 | 0 | 76 | 1 |
| 1997/1998 | 85 | 62 | 147 | 0 | 146 | 1 |
| 1998/1999 | 85 | 64 | 149 | 0 | 148 | 1 |
| 1999/2000 | 157 | 78 | 235 | 0 | 234 | 1 |
| 2000/2001 | 157 | 80 | 237 | 0 | 236 | 1 |
| 2001/2002 | 157 | 80 | 237 | 0 | 236 | 1 |
| 2002/2003 | 157 | 80 | 237 | 0 | 236 | 1 |
| 2003/2004 | 125 | 80 | 205 | 0 | 204 | 1 |
| 2004/2005 | 125 | 80 | 205 | 0 | 204 | 1 |
| 2005/2006 | 125 | 84 | 209 | 0 | 208 | 1 |
| 2006/2007 | 125 | 82 | 207 | 0 | 206 | 1 |
| 2007/2008 | 125 | 88 | 213 | 0 | 212 | 1 |
| 2008/2009 | 125 | 88 | 213 | 0 | 212 | 1 |
| 2009/2010 | 125 | 88 | 213 | 0 | 212 | 1 |
| 2010/2011 | 125 | 87 | 212 | 1 | 211 | 1 |
| 2011/2012 | 125 | 88 | 213 | 0 | 212 | 1 |
| 2012/2013 | 125 | 88 | 213 | 0 | 212 | 1 |
| 2013/2014 | 125 | 88 | 213 | 0 | 212 | 1 |
| 2014/2015 | 125 | 90 | 215 | 0 | 214 | 1 |
| 2015/2016 | 125 | 92 | 217 | 0 | 216 | 1 |
| 2016/2017 | 125 | 92 | 217 | 0 | 216 | 1 |
| 2017/2018 | 125 | 94 | 219 | 0 | 218 | 1 |
| 2018/2019 | 125 | 91 | 216 | 0 | 212 | 4 |
| 2019/2020 | 119 | 91 | 210 | 0 | 200 | 10 |
| 2020/2021 | 125 | 51 | 176 | 2 | 173 | 3 |
| 2021/2022 | 125 | 93 | 218 | 0 | 214 | 4 |
| 2022/2023 | 125 | 89 | 214 | 0 | 210 | 4 |
| 2023/2024 | 125 | 89 | 214 | 0 | 210 | 4 |
| 2024/2025 | 189 | 90 | 279 | 0 | 278 | 1 |
| 2025/2026 | 189 | 92 | 281 | 0 | 280 | 1 |
| **Total** | **4,127** | **2,515** | **6,642** | **3** | **6,584** | **58** |

No remaining missing standing target fixture or round was identified in accepted
Phase 3. This is not primary historical certification of every fixture or disjoint
publisher lineage. 1990/91–1991/92 European Cup remain outside approved scope;
2026/27 is excluded. Existing domestic coverage gaps and scope exclusions are
unchanged, including Turkish early-season gaps and missing postseason descriptions.

## Stage accounting

Stages preserve the accepted early pre-group round interpretation, the distinct
1992/93 standing replay, dual group phases, ordinary two-leg knockouts, the 2019/20
centralized finish, the 2020/21 single-leg qualification exception and the 36-club
league phases/main knockout play-offs. Qualifying and main play-offs are not merged.

| Stage | INCLUDE | Neutral 0 | Neutral 1 |
|---|---:|---:|---:|
| FINAL | 34 | 0 | 34 |
| FIRST_GROUP | 2736 | 2736 | 0 |
| KNOCKOUT_PLAYOFF | 32 | 32 | 0 |
| LEAGUE_PHASE | 288 | 288 | 0 |
| PRELIMINARY | 76 | 76 | 0 |
| PRELIMINARY_FINAL | 5 | 0 | 5 |
| PRELIMINARY_SEMIFINAL | 12 | 0 | 12 |
| PRE_GROUP_ROUND_1 | 65 | 64 | 1 |
| PRE_GROUP_ROUND_2 | 32 | 32 | 0 |
| QUALIFYING_PLAYOFF | 280 | 280 | 0 |
| QUALIFYING_ROUND_1 | 563 | 563 | 0 |
| QUALIFYING_ROUND_2 | 843 | 843 | 0 |
| QUALIFYING_ROUND_3 | 736 | 736 | 0 |
| QUARTERFINAL | 252 | 248 | 4 |
| ROUND_OF_16 | 368 | 368 | 0 |
| SECOND_GROUP | 192 | 192 | 0 |
| SEMIFINAL | 128 | 126 | 2 |

## Score, date, identity and exclusion decisions

Canonical goals normally represent supported 90 minutes including stoppage time.
**Eight played administrative-result exceptions** retain approved accepted historical
scores under the unchanged retrospective policy. These are labelled separately
from observed regulation in the sidecar; two abandoned played events do not have
an invented completed regulation score. Do not describe every canonical score as
an observed 90-minute result. No administrative-publication-date filter was imposed.
No-kickoff awards remain NOT PLAYED, not administrative played exceptions.

All eight non-administrative numeric regulation repairs, four original-kickoff date
repairs, three recovered unknown periods, two half-time repairs, two leg-label
repairs and four season-bound historical club-display assignments survive unchanged.
Some rules address the same event. Original dates/notations remain in private
metadata; continuation dates do not replace original kickoff dates. Source-directed
orientation and paired team scores are preserved, including finals with reversed
comparator orientation. Only approved source/season club-label corrections and
existing whitespace normalization apply; no new global aliases were invented.

All 147 event-level after-extra-time observations and 66 shootout observations remain
in the historical registry, including exclusions where applicable. They are not
substituted for canonical regulation goals or Toto outcomes. Outcome stays
1 = first-listed win, X = draw, 2 = second-listed win, with administrative exceptions
explicitly labelled. The exact repair/exclusion IDs and source evidence are in the
private independent report and detailed appendix, not publicly redistributed here.

## Unified schema and neutrality method

See [schema v2](match-schema.md), [PROCESS.md](../PROCESS.md), and
[importer compatibility](historical-import.md). The ordered columns are:

```csv
match_id,date,league,season,home_team,away_team,home_goals,away_goals,neutral_venue
```

CSV uses UTF-8 without BOM, LF, ordinary quoting, integer `0`/`1` and blank for missing
neutrality. The application loader validates the optional column as nullable `Int8`.
Six/eight-column legacy and synthetic inputs remain compatible. New v2 output uses
the shared identity algorithm: SHA-256 of compact UTF-8 JSON
`[league,season,date,home_team,away_team]`. Neutrality never enters identity.
Existing frozen v1 adapters keep an explicit compatibility alias and default output;
the shared importer also supports explicit v2 output with reviewed source metadata.
UCL uses the previously proposed league label `UEFA Champions League`.

The variable describes **official competition-format neutrality**, not stadium
location or realized home advantage. Earlier Phase 3 physical-venue observations
remain unchanged in private metadata and are not the source of the new flag.
A previously researched physical relocation can therefore coexist with format 0.
No comprehensive stadium investigation was conducted.

| Format rule | Classification and boundary | Played neutral count |
|---|---|---:|
| Official final, all 34 seasons | 1 even at a participant's normal ground; orientation unchanged | 34 |
| 2018/19–2023/24 centralized preliminary SF/final | 1; two SF and one final each, except 2020/21 final never kicked off | 17 |
| 2019/20 Lisbon quarterfinals/semifinals | 1; four QF and two SF; remaining R16 return legs stay 0 | 6 |
| 1992/93 specially ordered neutral replay | 1, source-bound exceptional event; ordinary replays do not inherit it | 1 |
| Ordinary qualifying, pre-group, groups, league and home/away knockout format | 0; includes early two-leg preliminary rounds | 0 |
| 1993/94 home-hosted single-leg semifinals; 2020/21 drawn-home Q1–Q3 | 0; single-leg status and relocation do not imply neutral format | 0 |
| Unestablished format | blank/NA, never silently defaulted to 0 | 0 |

Format evidence uses frozen original stage headings and administrative-home
explanations with decoded locators, the accepted Phase 2 structural format checks,
Phase 3 replay evidence and targeted participant factual notes. For example,
[Lincoln's 2018 mini-tournament account](https://lincolnredimpsfc.co.uk/club-info/match-programme),
[its 2019 preliminary account](https://lincolnredimpsfc.co.uk/news/victor-afonso-mateo--preparation-is-key),
and [Bayern's 2020 chronology](https://fcbayern.com/en/matches/profis/champions-league/2019-2020/champions-league-achtelfinale-rueckspiel-fc-bayern-fc-chelsea-18-03-2020/liveticker)
corroborate those specific formats. These are factual research notes with access
limits, not newly acquired article originals or independent upstream guarantees.
No UEFA dataset, Wikipedia retry/mirror or additional domestic source was acquired.

Future neutral-format matches should contribute to overall performance without
being automatically counted as ordinary venue-specific home/away observations.
That statistical implementation is deferred. Neither prediction logic nor current
synthetic-demo behavior changed, and UCL is not integrated into the prediction path.

## Domestic extension and preservation

The accepted [score-period audit](domestic-score-period-audit.md) reconciles exactly
to the current 14-competition/16-file inventory. The two ongoing English snapshots
retain all 258 frozen rows; no fresh acquisition occurred. Conventional league and
postseason league-group formats are 0. The two included Belgian qualification finals
are hosted fixtures, not presumed neutral because of their title. Bundesliga's
1991/92 second-phase groups are ordinary home/away league groups. Existing excluded
knockout/cross-tier fixtures and unstandardized acquisitions remain excluded.

| Current CSV / competition | Rows before = after | Columns | Unchanged old fields | Changed fields / IDs | Neutral 0 / 1 / NA |
|---|---:|---|---:|---|---|
| Belgian Pro League | 8,592 | 8 → 9 | 68,736 | 0 / 0 | 8,592 / 0 / 0 |
| EFL Championship | 19,872 | 8 → 9 | 158,976 | 0 / 0 | 19,872 / 0 / 0 |
| EFL Championship (ongoing snapshot) | 168 | 8 → 9 | 1,344 | 0 / 0 | 168 / 0 / 0 |
| england.premier-league | 13,166 | 8 → 9 | 105,328 | 0 / 0 | 13,166 / 0 / 0 |
| england.premier-league (ongoing snapshot) | 90 | 8 → 9 | 720 | 0 / 0 | 90 / 0 / 0 |
| Ligue 1 | 12,601 | 8 → 9 | 100,808 | 0 / 0 | 12,601 / 0 / 0 |
| Ligue 2 | 4,003 | 8 → 9 | 32,024 | 0 / 0 | 4,003 / 0 / 0 |
| Bundesliga | 11,090 | 8 → 9 | 88,720 | 0 / 0 | 11,090 / 0 / 0 |
| 2. Bundesliga | 11,488 | 8 → 9 | 91,904 | 0 / 0 | 11,488 / 0 / 0 |
| Serie A | 12,644 | 8 → 9 | 101,152 | 0 / 0 | 12,644 / 0 / 0 |
| Serie B | 12,297 | 8 → 9 | 98,376 | 0 / 0 | 12,297 / 0 / 0 |
| Eredivisie | 10,939 | 8 → 9 | 87,512 | 0 / 0 | 10,939 / 0 / 0 |
| Primeira Liga | 9,262 | 8 → 9 | 74,096 | 0 / 0 | 9,262 / 0 / 0 |
| La Liga | 13,843 | 8 → 9 | 110,744 | 0 / 0 | 13,843 / 0 / 0 |
| Segunda División | 5,984 | 8 → 9 | 47,872 | 0 / 0 | 5,984 / 0 / 0 |
| Turkish Süper Lig | 10,540 | 8 → 9 | 84,320 | 0 / 0 | 10,540 / 0 / 0 |
| **Total, 16 CSVs / 14 competitions** | **156,579** | **8 → 9** | **1,252,632** | **0 / 0** | **156,579 / 0 / 0** |

The 12,302-row Serie B audit archive was not migrated. No raw, original, audit archive,
unstandardized or unrelated acquired dataset was modified. Exact v1 backups remain
under private `phase4/backups/`; old manifests still refer to those original bytes,
while the migration receipt binds the v2 files. Original row order and serialization
project back byte-identically. The accepted regulation-time audit remains valid with
its original bounded-evidence and source-lineage limitations.

## Independent validation and tests

The separate verifier imports no new generator, migration, ID or format helper.
It reparses original CSV/TXT using the earlier independent reader, independently
reads revision JSON and the Curley CSV, then applies source/hash/identity-bound
approved evidence. It reconstructs every canonical field, ID, orientation, season,
stage, outcome, ordering and serialized byte, checks all 12,211 observation
memberships and all dispositions, and checks source/output links and physical
locators. An independent per-season format ledger expects 58 neutral matches,
including one neutral final per season and all exceptional neutral formats.
The 284 stage-group and 34-season ledgers reconcile to the accepted coverage.

Fresh Phase 3 independent revalidation also passes: 4,941 supplemental overlap
links, 129 regulation/extra-time tie gates, 33 separate-publisher qualifying-season
count checks and 1,663 aggregate checks. Reported aggregate differences and the
isolated auxiliary-date quarantine remain preserved, not silently corrected.

All 67 new focused synthetic schema, migration, UCL and compatibility regressions passed. The final
**complete repository suite passes: 2,822 tests and 27 subtests**, zero failures,
errors or skips. Synthetic tests cover all eight numeric repair shapes and four
date-repair shapes, period separation, outcomes, administrative versus no-kickoff
exceptions, stable IDs/duplicates, finals at participant grounds, centralized formats,
single-leg home formats, missing neutrality, byte-preserving domestic migration,
private-output safeguards, loaders and unchanged synthetic predictions. Existing
period-annotation and extra-time-first/shootout-first regressions remain covered.
No dependency installation or environment rebuilding was performed.

The first independent diagnostic counted three null-to-supported period recoveries
alongside numeric repairs; its retained failure was resolved by separating those
categories, while still validating all eleven transitions. No historical decision
or validation condition was relaxed. Repeated final suite runs followed actual
verification/privacy changes; the latest complete result is authoritative.

Offline reproduction uses two fresh processes with socket connection and DNS access
forbidden: all six UCL artifacts plus 16 domestic CSVs reproduce **22 byte-identical
artifacts**. Independent reconstruction reproduces the UCL CSV byte-for-byte from
original observations and verifies all reproduced domestic projections. Input/output
hashes, commands, full test output and zero-network receipts remain private.

## Rights, preservation and remaining limits

FootballCSV/OpenFootball pinned CC0 applies only to rights held, with third-party
lineage unestablished. Wikipedia revision attribution/permalinks and CC BY-SA limits
are retained. Curley is a noncommercial attributed comparator, not an independently
certified historical vote or unrestricted training source. RSSSF/participant factual
notes are not article-copy licences or frozen provider HTML. Source-specific access
stops and permission registers remain unchanged. This phase grants no additional
training, redistribution or commercial rights; there is no new technical blocker
for approved private standardization.

Preservation rechecks all 2,583 pre-phase fingerprints, distinguishing the authorized
16 domestic metadata extensions and six existing public code/documentation changes
from protected files. The planning log is append-only. Original sources, frozen
Phase 1–3 decisions/evidence, audit archives, application/model files outside the
approved loader/importer compatibility changes, prior unfinished work, HEAD, index,
Git configuration and original environment configuration are preserved. Git objects,
caches and installed environment package bytes are outside exhaustive hashing; no
mutating environment/Git command ran. Private outputs/backups/evidence remain ignored.
No other worktree was accessed.

Measured recorded execution: **26 min 36 sec** (1596.992 monotonic seconds),
2026-11-27T00:12:32.319782+00:00 through 2026-11-27T00:39:09.279976+00:00.
Calendar elapsed 1596.960 seconds; owner-approval wait zero. The recorded
interval includes implementation, retained diagnostic attempts, tool/file waits,
tests, documentation and verification. No unrecorded preliminary instruction-inspection
duration was reconstructed. Final timing/preservation receipts are private
`completion.json` and `preservation.json`.

## Phase 5 recommendations and stopping gate

Review this technical result and the retained administrative/rights limits. If
approved, Phase 5 should recheck the final input/output manifest and migration
receipts, rerun final checks only as justified by intervening changes, audit an exact
public code/documentation allowlist, and keep every real dataset, backup, receipt
and detailed registry private. Publication requires explicit owner authorization.
Do not treat Phase 4 as approval for model integration or venue-specific statistics.

**STOP after Phase 4. Await explicit owner approval before Phase 5.**
