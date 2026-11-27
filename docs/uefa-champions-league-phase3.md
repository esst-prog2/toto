# UEFA Champions League — Phase 3 historical review

**PASS for private historical adjudication, subject to owner review.** Completed
2026-11-27 in the original `toto` worktree on `feature/data-collection`. This phase
does not approve standardization, schema migration, model use or publication.

## Reconciliation and decisions

The accepted [Phase 2](uefa-champions-league-phase2.md) baseline remains unchanged:
41 fixture originals, 6,578 observations, 5,953 conditional events, 4,127 main
descriptions, 1,826 qualifying descriptions, 34 seasons, 13 review events and nine
contexts. Their bytes, identifiers and original observations are preserved.

The expanded inventory contains **12,211 fixture observations and 6,645 fixture
events**. Proposed dispositions are **6,642 INCLUDE, zero HOLD OUT and three NOT
PLAYED**. Three additional researched annulled/superseded attempts are retained
separately as **OUT OF SCOPE** contexts. Thus the complete reviewed population is
**6,648: 6,642 INCLUDE / 0 HOLD OUT / 3 NOT PLAYED / 3 OUT OF SCOPE**. Context-note
observations are explicitly distinguished from downloaded fixture rows.

The baseline contributes 5,952 INCLUDE and one NOT PLAYED; the 692 recovered
qualifying descriptions contribute 690 INCLUDE and two NOT PLAYED. No overlap
increases coverage. No missing fixture was invented as a NOT PLAYED event.

All 13 original review events and nine contexts are addressed. The private candidate
records 36 source-bound derived rules, including eight non-administrative repairs to incorrect primary
regulation scores, four primary football-date repairs, two halftime repairs, two
return-leg label repairs and four season-bound historical club-display assignments.
Some rules address the same event. Ordinary fixtures use explicit original dates,
stage and score evidence; manual research targets material exceptions.

## Supplemental acquisition and source limits

| Source | Acquired or inspected evidence | Use and limits |
|---|---|---|
| Wikipedia contributors | 17 pinned revision JSON originals: 14 qualifying articles and three main-context articles; three revision-metadata responses | 1,232 qualifying observations. CC BY-SA 4.0 attribution, revision/permalink/history references retained; share-alike obligations apply where relevant to distribution. Upstream independence is not certified. |
| James P. Curley, engsoccerdata | One pinned 797,540-byte `champs.csv`, revision `872c5c354161ace8408f3091b758c6af4cccca94` | 4,401 target observations: complete source descriptions through 2015/16 and only one final each in 2016/17 and 2017/18. README noncommercial attribution permission retained; GPL package-code licensing is separate. Strong overlap with FootballCSV is not an independent historical vote. |
| RSSSF contributors | Bounded historical research across 33 season pages, 1992/93–2024/25; page-specific author/copy notices and factual count/exception notes retained | Separate-publisher qualifying counts and targeted historical evidence. These are factual research notes with rendered-view locators, **not frozen provider HTML**. A raw response failed content/copy-grant recognition and was not saved or retried directly. |
| Participant clubs, contemporary reporting and CAS | Targeted factual notes, URLs, research window and evidence references | Used for score periods, awards, continuation dates, replay identity and group membership. Full protected article bodies, images and UEFA snapshots were not acquired. A factual note is not an article-copy or training licence. |

New acquisitions total **18 source payloads / 2,525,136 bytes**, plus **three
metadata payloads / 19,641 bytes**: **21 payloads / 2,544,777 bytes**, each with
URL, UTC retrieval timestamp, SHA-256, byte size and immutable receipt. Fifteen
payloads are fixture inputs; three are main-context evidence. All 41 earlier
fixture originals remain referenced in place. Exact file/hash/revision records are
in the private acquisition manifest.

Wikipedia returned HTTP 429 during optional older-context recovery. Acquisition
stopped; no retry, alternate endpoint or mirror was used. Frozen files support
offline work, and a host-stop guard permits only cached reuse. Existing Kassies
access stops remain. The 2025/26 RSSSF page could not be verified through the web
tool; absence of a page was not asserted.

Alternatives investigated included the CC BY-NC 11footy collection, an MIT-licensed
aggregate club-performance repository, existing OpenFootball/FootballCSV trees,
and licensed API routes. The aggregate repository lacks fixture data; 11footy's
larger competition archives were not downloaded speculatively, and lineage/period
semantics remain unverified. APIs remain subject to entitlement and retention/use
permission. No account, purchase, provider contact, restricted scrape or UEFA
platform acquisition occurred. Private use does not override source restrictions.

The approved local/private real-data and synthetic-only public-deployment policy
is unchanged. Originals, detailed evidence, receipts and candidate decisions stay
Git-ignored. No downstream training or redistribution clearance is inferred.

## Mandatory qualifying recovery

All eight missing qualifying seasons were investigated and recovered. Independent
parsing reconciles each acquired match box to a separate tie-summary representation;
RSSSF provides additional count checks. Preliminary single-leg tournaments,
champions/league paths where explicitly supplied, qualifying rounds and qualifying
play-offs remain distinct. None is confused with main knockout play-offs.

| Season | Preliminary SF / final | Q1 | Q2 | Q3 | Qualifying play-offs | Expected / observed | Played INCLUDE / no-kickoff |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2016/17 | — | 8 | 34 | 30 | 20 | 92 / 92 | 92 / 0 |
| 2017/18 | — | 10 | 34 | 30 | 20 | 94 / 94 | 94 / 0 |
| 2018/19 | 2 / 1 | 32 | 24 | 20 | 12 | 91 / 91 | 91 / 0 |
| 2019/20 | 2 / 1 | 32 | 24 | 20 | 12 | 91 / 91 | 91 / 0 |
| 2020/21 | 2 / 1 | 17 | 13 | 8 | 12 | 53 / 53 | 51 / 2 |
| 2021/22 | 2 / 1 | 32 | 26 | 20 | 12 | 93 / 93 | 93 / 0 |
| 2022/23 | 2 / 1 | 30 | 24 | 20 | 12 | 89 / 89 | 89 / 0 |
| 2023/24 | 2 / 1 | 30 | 24 | 20 | 12 | 89 / 89 | 89 / 0 |
| **Total** | | | | | | **692 / 692** | **690 / 2** |

The 2020/21 preliminary final and one first qualifier never kicked off. Their
scheduled dates and awards are preserved; neither has an invented football date
or regulation score. Early-season source tables use different round terminology;
the private assessment preserves their headings and source-bound correspondences.

Other seasons were checked using the existing format inventory, all earlier
Curley overlaps, four additional earlier qualifying revision articles, recent
qualifying comparators and 33 RSSSF count assessments. **No remaining missing
standing qualifying fixture or round was identified.** This is stronger than a
publisher coverage claim, but is not independent primary certification of every
ordinary historical fixture. Shared or unknown upstream lineage remains explicit.

## All target seasons

Standing fixture descriptions include documented no-kickoff awards; INCLUDE does not. The three additional non-standing contexts are accounted separately.

| Season | Main | Qualifying expected / observed | INCLUDE | NOT PLAYED | Identified missing standing fixtures |
|---|---:|---:|---:|---:|---:|
| 1992/93 | 74 | 8 / 8 | 82 | 0 | 0 |
| 1993/94 | 75 | 20 / 20 | 95 | 0 | 0 |
| 1994/95 | 61 | 16 / 16 | 77 | 0 | 0 |
| 1995/96 | 61 | 16 / 16 | 77 | 0 | 0 |
| 1996/97 | 61 | 16 / 16 | 77 | 0 | 0 |
| 1997/98 | 85 | 62 / 62 | 147 | 0 | 0 |
| 1998/99 | 85 | 64 / 64 | 149 | 0 | 0 |
| 1999/00 | 157 | 78 / 78 | 235 | 0 | 0 |
| 2000/01 | 157 | 80 / 80 | 237 | 0 | 0 |
| 2001/02 | 157 | 80 / 80 | 237 | 0 | 0 |
| 2002/03 | 157 | 80 / 80 | 237 | 0 | 0 |
| 2003/04 | 125 | 80 / 80 | 205 | 0 | 0 |
| 2004/05 | 125 | 80 / 80 | 205 | 0 | 0 |
| 2005/06 | 125 | 84 / 84 | 209 | 0 | 0 |
| 2006/07 | 125 | 82 / 82 | 207 | 0 | 0 |
| 2007/08 | 125 | 88 / 88 | 213 | 0 | 0 |
| 2008/09 | 125 | 88 / 88 | 213 | 0 | 0 |
| 2009/10 | 125 | 88 / 88 | 213 | 0 | 0 |
| 2010/11 | 125 | 88 / 88 | 212 | 1 | 0 |
| 2011/12 | 125 | 88 / 88 | 213 | 0 | 0 |
| 2012/13 | 125 | 88 / 88 | 213 | 0 | 0 |
| 2013/14 | 125 | 88 / 88 | 213 | 0 | 0 |
| 2014/15 | 125 | 90 / 90 | 215 | 0 | 0 |
| 2015/16 | 125 | 92 / 92 | 217 | 0 | 0 |
| 2016/17 | 125 | 92 / 92 | 217 | 0 | 0 |
| 2017/18 | 125 | 94 / 94 | 219 | 0 | 0 |
| 2018/19 | 125 | 91 / 91 | 216 | 0 | 0 |
| 2019/20 | 119 | 91 / 91 | 210 | 0 | 0 |
| 2020/21 | 125 | 53 / 53 | 176 | 2 | 0 |
| 2021/22 | 125 | 93 / 93 | 218 | 0 | 0 |
| 2022/23 | 125 | 89 / 89 | 214 | 0 | 0 |
| 2023/24 | 125 | 89 / 89 | 214 | 0 | 0 |
| 2024/25 | 189 | 90 / 90 | 279 | 0 | 0 |
| 2025/26 | 189 | 92 / 92 | 281 | 0 | 0 |

Main counts preserve the 1992/93 additional standing replay, early pre-group knockout rounds, both group phases in 1999/00–2002/03, the single-leg 2019/20 finish and the 36-club league phases from 2024/25. Qualifying-stage nominal counts include administrative descriptions; missing historical records would remain gaps.

## Score periods, administrative cases and identities

Eight non-administrative incorrect primary regulation values were individually researched and repaired
only in derived decisions. They include reversed regulation scores, extra-time
totals stored in `FT`, and two unannotated extra-time totals in the 2024/25 TXT.
Original fields remain unchanged. Complete explicitly timed goal chronologies are
used only when every reported goal is accounted for; ordinary stoppage time remains
regulation. Zero cumulative extra-time scores never supply a missing regulation
score by arithmetic. Targeted participant/contemporary accounts resolve the original
two TXT ambiguities and the newly recovered zero-score cases.

The candidate separates **147 after-extra-time events and 66 shootout events**
from their supported regulation outcomes. A shootout winner is never substituted
for a 1/X/2 result. Seven supplemental observations retain null parsed regulation
fields: award contexts or zero-score extra-time notation; supported event decisions
and their alternate evidence remain separate from those unchanged observations.

Eight played administrative-result exceptions retain both the observed football
score, where completed, and the supported accepted administrative result. Two were
abandoned after kickoff and have no completed observed 90-minute score. These
remain explicit applications of the established retrospective policy, without
administrative-publication-date filtering. They are distinct from the three
no-kickoff awards. One original played score requires an accepted-result override;
the other seven primary sources already report the accepted award.

Two continued main-stage matches use original kickoff dates and separately retain
completion dates. A misdated qualifying replay and another qualifying fixture date
are also repaired with directed fixture evidence. Annulled/superseded attempts are
preserved separately from standing replays/replacements. Subsequent exclusion of a
club does not automatically turn its earlier played fixtures into invented numeric
walkovers. Season-bound historical display metadata does not merge unrelated
Innsbruck entities or create global aliases.

The source-reported aggregates remain intact. An independent audit calculates
1,663 standing knockout tie totals and records **33 differences** from reported
aggregate fields. Some reflect before/after-extra-time or award semantics; they
are not automatically declared source defects or silently repaired. Group-stage
home/away meetings are not treated as two-leg knockout ties. Aggregate arithmetic
never reconstructs a missing regulation score.

The 2023/24 missing group letters are resolved using a separately reported draw
membership list, checked against all eight complete four-club opponent components.
Nominally reversed final descriptions retain the frozen primary first/second
orientation; comparator reversal is for comparison only.

## Neutral venues and remaining uncertainty

[PROCESS.md](../PROCESS.md) records the approved future project-wide tri-state
`neutral_venue` method. During Phase 3 it is private metadata only. Four fixture
events have targeted evidence for status 1; **6,641 retain NA**, including cases
not researched to that standard. No ordinary home label is converted automatically
to status 0, and no final label automatically to status 1. Participant-home-ground
finals and relocated/adopted grounds require care. Unknown venue status is not an
unknown result or an automatic HOLD OUT.

First-listed orientation, scores and 1/X/2 encoding remain fixed. Future neutral
matches may contribute to overall performance, without automatic home/away-specific
statistics. No canonical-schema, domestic-dataset or model implementation changed.
Venue enrichment and the future schema migration need their own approved work;
this phase does not claim exhaustive venue certification.

Numerical time weights remain **unspecified**, with the approved recent-first
priority. European Cup 1990/91–1991/92 and 2026/27 remain outside this workstream.

## Verification and reproducibility

The independent verifier imports no Phase 3 production parser, naming, period,
decision-application or ID helpers. It reuses the previous independent original
CSV/TXT reader, independently tokenizes revision JSON, reconstructs all supplemental
fields/locators, derives seasonal club correspondences from appearance/opponent
fingerprints, reconciles match boxes to tie summaries, then independently applies
the frozen evidence decisions.

It checks all 12,211 observations exactly once, all 5,953 frozen event identities,
692 new event IDs, 4,941 supplemental overlap links, 129 extra-time regulation ties,
33 separate-publisher seasonal qualifying counts, group membership, stage accounting,
all exclusions and administrative exceptions. Among supplemental raw overlaps,
4,940 dates agree; one auxiliary date stays quarantined. There are 4,938 comparable
regulation pairs: 4,936 agree and two conflicts are resolved by targeted evidence.
Agreement between related repositories/Curley is not independent historical truth.

Focused synthetic and relevant acquisition/import/artifact regressions cover nested
annotations, preserved score periods, complete/incomplete goal chronology, stoppage
time, zero-score non-inference, awards outside score fields, shootout separation,
return-leg orientation, missing tie members, source-bound decisions, no-kickoff
exclusions, administrative exceptions, neutral tri-state outcomes and immutable
private output. Independent reconciliation additionally detects ordinary group
fixtures incorrectly treated as knockout aggregates.

Final test, offline reproduction, preservation and measured-time receipts are
recorded in the completion checkpoint below. No full repository suite, environment
rebuild, training or backtesting is part of this intermediate phase.

Reproduce from the ignored frozen workspace, with repository `PYTHONPATH` and the
existing approved external Python environment:

```sh
python -B -m scripts.review_uefa_champions_league_history --check
python -B -m scripts.verify_uefa_champions_league_history
```

Production refuses to overwrite candidate artifacts or write detailed evidence to
public repository paths. Offline reproduction uses fresh temporary directories and
blocks network connections. Network acquisition helpers are not required to reproduce
the candidate. Earlier Phase 3 exploratory directories remain private drafts;
**`phase3/final/` is the review candidate**.

## Deliverables and approval gate

Private `data/private/europe/champions_league/phase3/` contains the acquisition
manifest, pinned originals/receipts, attribution records, factual research notes,
source-bound adjudication evidence, auxiliary quarantine decision and detailed
report/evidence appendix. `final/` contains eight deterministic artifacts: supplemental
inventory, correspondences, decision registry, season/stage coverage, review resolution,
aggregate differences, discrepancy registry and summary. A separate independent
validation result is also reproduced, giving nine byte-compared outputs.

Approve the composed private Phase 3 decisions, the recovered qualifying population,
the source-bound repairs and the three non-standing exclusions before Phase 4.
Phase 4 must use supported regulation results or the labelled existing administrative
exception, retain all period/stage/provenance metadata, preserve venue NA, and build
an independent source-to-output reconstruction. No standardized UCL data, model
integration, staging, commit or push has occurred. **STOP after Phase 3.**

## Completion checkpoint

Final focused result: **188 tests passed**, zero failures, using the existing external environment with bytecode/cache/plugin writes disabled. **Eight production artifacts plus the independent validation result (nine outputs) reproduced byte-for-byte** in a new process and temporary directory with networking prohibited. Independent checks pass on all12,211observations,6,645fixtureevents andthree additional non-standing contexts.

All **2,476 prior fingerprints** are preserved apart from the authorized PROCESS insertions and append-only planning additions; the original PROCESS bytes are recoverable exactly by removing those two added sections. All60frozen execution inputs verify. Prior domestic datasets, application files, source originals, audit evidence, environment configuration, HEAD, branch, Git index/configuration and pre-existing unfinished work are preserved. No installed-package/Git-object exhaustive scan is claimed. Public candidates contain methods/aggregate statistics/synthetic tests; private evidence remains ignored and nothing is staged. Source-period, neutral-metadata and permission limits above remain explicit.

Measured phase elapsed: **1 h 12 min 29 sec (4349.560 seconds)**, `2026-11-26T22:50:19+00:00` to `2026-11-27T00:02:48.559551+00:00`. Owner approval wait: **0 seconds**. The continuous-session wall interval uses those UTC timestamps and includes research, tool/file/network waits and failed attempts. A whole-phase monotonic start was not captured; command timings use monotonic clocks. Successful direct-acquisition requests separately total 13.102 seconds; the full web/file wait breakdown is unavailable and was not estimated. No speedup percentage is asserted. The append-only private timing ledger preserves these limits.

**Phase3 PASS; STOP. Await explicit approval of these decisions and authorization for Phase4.** No standardization, schema/model migration, staging, commit or push.
