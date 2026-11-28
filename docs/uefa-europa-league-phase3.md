# UEFA Cup / UEFA Europa League — Phase 3: Historical review and adjudication

Date: 2026-11-27. Worktree: `toto-uefa`; branch: `feature/uefa`.

## A. Phase status

**PASS — Phase 3 complete; Phase 4 has not started.** All 1,896 accepted review cases have an explicit, substantive resolution. Every resulting record has a historical disposition and separate statistical eligibility. Five pre-regulation-completion abandonments remain intentionally ineligible; their historical classification is resolved. This does not certify every attribute against an independent primary source.

The accepted baseline was 38,126 observations, 12,311 conditional events, 36 seasons and five publishers. All 85 original payloads and the accepted Phase 2 artifacts were retained. The resulting inventory is private, reversible intermediate work suitable for standardization, not the production dataset.

## B. Historical review results

All 1,896 original cases were investigated and resolved, including 763 priority 1, 1,082 priority 2 and 51 priority 3 cases. None disappeared, were consolidated, or remain unresolved/blocked. The overall resolved count includes 67 confirmed-not-applicable cases. The resolution categories are mutually exclusive:

| Resolution basis | Cases |
|---|---:|
| Reproducible structural reconciliation | 1,759 |
| Directed historical evidence | 38 |
| Established project policy | 32 |
| Confirmed historically not applicable | 67 |
| Total | 1,896 |

“Directed historical evidence” identifies researched, source-bound decisions; it does not claim that every supporting publisher is independent. Structural closure requires the relevant observations and attributes to agree under the documented rules, rather than simply marking a case reviewed.

There are 94 additional cases, all resolved: 60 source-bound reviews, 30 not-applicable scope cases, two historical contexts, one extra-time-abandonment decision and one single-leg topology diagnostic. Their identifiers, evidence and results are retained separately in `new_review_cases.json`.

Original issue counts overlap:

| Original issue | Resolved |
|---|---:|
| `AMBIGUOUS_DUPLICATE_CANDIDATE` | 12 |
| `DATE_CONFLICT` | 281 |
| `DATE_UNRESOLVED` | 726 |
| `DURATION_CONFLICT` | 146 |
| `EXCEPTIONAL_STATUS` | 33 |
| `HISTORICAL_SCORE_CONTEXT` | 1 |
| `NONPLAYED_TIE_WITHOUT_LEG_RESULTS` | 2 |
| `REGULATION_SCORE_UNRESOLVED` | 952 |
| `SCORE_CONFLICT_HALF_TIME` | 3 |
| `SCORE_CONFLICT_REGULATION_TIME` | 65 |
| `SOURCE_LEG_OR_SCHEDULE_CONFLICT` | 19 |
| `SOURCE_ORIENTATION_CONFLICT` | 7 |
| `STAGE_CONFLICT` | 1 |
| `STAGE_UNRESOLVED` | 243 |
| `TIE_TOPOLOGY_COVERAGE_CANDIDATE` | 56 |
| `UNRESOLVED_TEAM_IDENTITY_CANDIDATE` | 258 |
| `VENUE_REVIEW` | 51 |

The review inventory preserves original IDs, issue sets, priorities, observation/event references, investigation method, evidence, resulting decisions and uncertainty. Related cases share evidence only where the same attribute-specific reasoning applies.

## C. Fixture reconciliation

The exact event bridge is **12,311 + 5 split increments − 826 merge decrements + 0 new fixture events = 11,490 adjudicated records**. Five previous conditional events required separation; 1,593 previous events contribute to merged result records. These are source-event counts, not additional played matches.

The mutually exclusive resulting-record categories are 10,205 retained with unchanged core fields, 513 retained corrected/enriched, 769 merged records and three split result records, totaling 11,490. Category precedence prevents counting a merged-and-corrected record twice.

| Disposition | Records |
|---|---:|
| INCLUDE | 11,422 |
| HOLD OUT | 5 |
| NOT PLAYED | 4 |
| OUT OF SCOPE | 59 |
| Total | 11,490 |

There were 11,427 target kickoffs: 11,422 completed regulation and five ended before regulation finished. Of the 11,422, one was abandoned during extra time, so **11,421 football matches were fully completed**. Completed-regulation counts are **6,506 main competition and 4,916 qualifying**; kickoff counts including incomplete games are 6,508 and 4,919 respectively. Eleven completed-regulation matches have administrative exceptions. These exceptional counts overlap the inclusion counts.

The 59 outside-target records comprise 58 Intertoto descriptions and one parsed heading that is not a fixture. Its `record_unit` and historical validity explicitly prevent treating it as a historical match. Four no-kickoff fixture descriptions have no regulation score or playing date. Separately preserved contexts include three unplayed ties and an annulled earlier attempt preceding a replay; contexts are not added to the fixture denominator or used as ordinary modelling observations.

The observation bridge is **38,126 + 8 recovered observations from existing originals + 0 newly acquired observations = 38,134**. The eight are recovered return-leg descriptions, not newly discovered unique fixtures. All original observations occur exactly once in the adjudicated membership mapping, including conflicting, duplicate, excluded and non-played descriptions. `event_crosswalk.json` preserves both directions through original event IDs and observation membership.

## D. Data quality and adjudication

### Regulation time and exceptional results

All 146 original duration cases and 65 regulation-score conflict cases were resolved. The entire event population was also checked for score-period contamination. Regulation includes stoppage time and excludes extra time and shootouts. Every record separately retains available half-time, regulation, cumulative extra-time, extra-time-only, shootout, aggregate, published-final and administrative evidence. Missing half-time values do not exclude otherwise supported regulation results.

The inventory has **11,422 supported exact regulation scores**, with the same number eligible for outcome, goal and chronological use. No currently eligible record has only an outcome with unknown exact goals. The implementation nevertheless preserves that category and tests it: an extra-time draw or identified first-leg equality may establish 1/X/2 without exact goals. It never infers 0–0 merely from a shootout. The five held-out abandoned matches retain partial scores as partial scores; there is no unresolved score admitted to modelling.

Evidence is evaluated by attribute. Complete timed-goal logs must agree with cumulative totals and chronological constraints before deriving scores. Pre-2021 return-leg inference requires an identified first leg and applicable tie rules. Old two-legged finals instead require a unique aggregate/cumulative bound; ordinary away-goals assumptions are not transferred automatically. Sparse ordinary-match scores are accepted only after duration and source semantics checks; source voting is not used.

An aggregate third-column footnote `p` had been interpreted as a shootout and suppressed return-leg observations. Eight returns were recovered from unchanged original bytes. A guard excludes genuine fourth-column shootouts after an awarded result. Original period claims and before/after repairs remain recorded.

Targeted research also corrected positive-only duration flags: four cases required ordinary-duration or exact 90-minute clarification, using a [historical Stuttgart competition account](https://www.rsssf.org/tablesd/duitec-stuttgart05.html), an [official UEFA match record](https://www.uefa.com/uefaeuropaleague/match/2020424--apollon-vs-grasshoppers/), a [participant match report](https://www.dac1904.sk/en/zapas.asp?id=2786), and a [participant fixture record](https://kfshkendija.com/football-match/fc-ludogorets-fc-shkendija-00/). Exact fixture-level decisions remain private.

A further abandonment happened during extra time, after a completed regulation draw. Its regulation result is eligible; incomplete extra-time and administrative results remain separate. The [UEFA disciplinary release](https://www.uefa.com/newsfiles/8285.pdf) and [period timeline](https://www.romaniansoccer.ro/europeancups/2001_02/rapid_psg_02.shtml) support the distinction. Sources differ on the exact abandonment minute; that uncertainty is retained and does not change regulation eligibility. No completed extra-time score is fabricated.

The current owner's explicit regulation-time target governs modelling of played administrative exceptions. Historical awards remain separate. The appended PROCESS section states this scope without rewriting previous domestic/Champions League decisions. Administrative decision publication dates were not reconstructed unnecessarily.

### Dates, identities, stages and venues

All 281 original date conflicts and 726 unresolved-date flags were resolved using report-specific dates, directed occurrence corrections, and season/tie context. Original intervals and conflicting dates remain in the evidence. All 11,422 eligible records have supported actual playing dates; **zero estimated interval selections** were required, and no eligible record has material date uncertainty. No-kickoff schedules are stored as scheduled evidence, not playing dates.

All 258 identity candidates were reviewed: 228 seasonal name correspondences, 18 distinct-club decisions, seven contextual generic-name disambiguations and five source-label-only correspondences. Additional directed seasonal/occurrence decisions are recorded separately. Historic names, source IDs and country claims remain preserved. Seasonal identity reconciliation does not assert legal succession or rewrite established project IDs. Generic Inter, AEK and Slavia require contextual safeguards rather than broad string merging. Participant errors in individual source rows are corrected only through bound occurrence decisions with source hash, locator, before/after fields and corroborating descriptions.

The independent raw-bracket check detected four duplicate descriptions in 2004/05: generic club labels had merged one participant incorrectly and a transliteration had split another. Those correspondences were corrected before acceptance, bringing qualifying kickoffs into agreement with the independently reconstructed bracket. Replays, distinct legs and repeated meetings remain separate; schedule/score disagreement alone cannot create a second played match. Directed chronology, stage and replay evidence control reconciliation.

Historical stage labels and normalized stages are both retained. Qualifying remains inapplicable in 1990/91–1993/94, with independent 64-club first-round checks. No modern group/league format is projected onto those seasons.

All 51 venue cases were reviewed under the established official-format neutrality convention: **38 neutral-format records**, comprising 29 single-match finals, eight centralized 2020 non-final fixtures and one explicitly neutral single tie. Earlier two-legged finals are hosted. A relocation or foreign stadium is not alone proof of neutrality; nominal home/away orientation remains separate. The established mapping is hosted=0, neutral-format=1, uncertain=NA. Venue-dependent eligibility is **11,384**, excluding the 38 neutral-format games. This is not an exhaustive certification of physical home advantage at every venue.

No material unresolved identity, stage, score or date issue affects an included record. Remaining minor uncertainties and unavailable fields remain attached to their records; upstream source independence remains unestablished.

## E. Historical coverage

All 56 original tie-coverage candidates were resolved. Post-reconciliation diagnostics also account for single-match ties, cancelled returns, a transferred club and the non-fixture heading. No confirmed or suspected missing played target fixture remains identified by these checks. No fixture was manufactured to satisfy an expected total.

For example, official records establish a [bye after exclusion](https://www.uefa.com/uefaeuropaleague/news/01bd-0ea89a03ed70-091aa78ac150-1000--tottenham-get-uefa-cup-bye/) and a [transfer to Champions League qualifying](https://www.uefa.com/uefachampionsleague/news/022f-0e9491c5366c-7f36115c125a-1000--partizani-replace-sk%D0%B5nderbeu-in-champions-league/); neither creates a missing played Europa League return leg. Frozen archive footnotes and directed notes cover other exceptions, including a strike and a [contemporaneously documented one-match arrangement](https://www.derstandard.at/story/1218533872039/austria-nur-einmal-gegen-tiflis). A final reference audit replaced an unverified UEFA URL for that arrangement with this contemporary account; the unused reference is explicitly labelled unverified in the private decision history.

All 36 main kickoff totals agree with season-specific format totals adjusted only for documented historical exceptions. Qualifying totals are checked independently against 33 raw frozen archive sections, two frozen recent qualifying TXT files, and the documented 2023/24 access structure of seven third-round plus ten playoff two-legged ties (34 matches). The last is a researched official structure note, not a newly frozen primary fixture listing. The two recent league phases retain 144 games, 36 teams, eight appearances each and four home/four away games each.

No new original source payload was acquired in Phase 3. Targeted historical searches and rendered records supplied factual URL/attribute notes, not full article bodies or a systematic UEFA archive. Coverage improvement consists of recovered descriptions, corrected reconciliation and resolved false gaps. Wikipedia's inherited 429 stop, Kassies' access stop and the unsuccessful direct 2023/24 archive path were respected; no mirror retry was used to evade restrictions.

Post-2000 kickoff coverage and date support meet the requested priorities under these checks. No season or stage has an identified outstanding played-fixture gap. Count agreement is strong structural evidence, not independent primary certification of every ordinary score, identity or venue. `coverage_certified=false` deliberately retains that limitation.

The following matrix counts completed regulation as “played”; kickoffs before incomplete abandonment are shown separately in the private matrix. Dates are sufficiently supported, not all independently verified from primary sources. Estimated dates, outcome-only records and identified remaining kickoff gaps are zero in every season.

| Season | Records | Main 90m | Qualifying 90m | Supported 90m score/date | Held out | No kickoff | Outside scope | Neutral |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1990/1991 | 126 | 126 | 0 | 126 | 0 | 0 | 0 | 0 |
| 1991/1992 | 126 | 126 | 0 | 126 | 0 | 0 | 0 | 0 |
| 1992/1993 | 126 | 125 | 0 | 125 | 1 | 0 | 0 | 0 |
| 1993/1994 | 126 | 126 | 0 | 126 | 0 | 0 | 0 | 0 |
| 1994/1995 | 180 | 126 | 54 | 180 | 0 | 0 | 0 | 0 |
| 1995/1996 | 194 | 126 | 64 | 190 | 0 | 0 | 4 | 0 |
| 1996/1997 | 250 | 126 | 106 | 232 | 0 | 0 | 18 | 0 |
| 1997/1998 | 219 | 125 | 76 | 201 | 0 | 0 | 18 | 1 |
| 1998/1999 | 223 | 124 | 80 | 204 | 1 | 0 | 18 | 1 |
| 1999/2000 | 281 | 205 | 76 | 281 | 0 | 0 | 0 | 1 |
| 2000/2001 | 287 | 205 | 82 | 287 | 0 | 0 | 0 | 1 |
| 2001/2002 | 286 | 204 | 82 | 286 | 0 | 0 | 0 | 2 |
| 2002/2003 | 287 | 205 | 82 | 287 | 0 | 0 | 0 | 1 |
| 2003/2004 | 287 | 205 | 82 | 287 | 0 | 0 | 0 | 1 |
| 2004/2005 | 335 | 220 | 114 | 334 | 0 | 0 | 1 | 1 |
| 2005/2006 | 333 | 221 | 112 | 333 | 0 | 0 | 0 | 1 |
| 2006/2007 | 353 | 219 | 134 | 353 | 0 | 0 | 0 | 1 |
| 2007/2008 | 359 | 221 | 138 | 359 | 0 | 0 | 0 | 1 |
| 2008/2009 | 358 | 221 | 137 | 358 | 0 | 0 | 0 | 1 |
| 2009/2010 | 477 | 205 | 271 | 476 | 1 | 0 | 0 | 1 |
| 2010/2011 | 481 | 205 | 276 | 481 | 0 | 0 | 0 | 1 |
| 2011/2012 | 480 | 205 | 275 | 480 | 0 | 0 | 0 | 1 |
| 2012/2013 | 479 | 205 | 273 | 478 | 1 | 0 | 0 | 1 |
| 2013/2014 | 479 | 205 | 274 | 479 | 0 | 0 | 0 | 1 |
| 2014/2015 | 483 | 205 | 278 | 483 | 0 | 0 | 0 | 1 |
| 2015/2016 | 475 | 205 | 269 | 474 | 1 | 0 | 0 | 1 |
| 2016/2017 | 468 | 205 | 263 | 468 | 0 | 0 | 0 | 1 |
| 2017/2018 | 473 | 205 | 268 | 473 | 0 | 0 | 0 | 1 |
| 2018/2019 | 519 | 205 | 314 | 519 | 0 | 0 | 0 | 1 |
| 2019/2020 | 511 | 197 | 314 | 511 | 0 | 0 | 0 | 9 |
| 2020/2021 | 362 | 204 | 156 | 360 | 0 | 2 | 0 | 1 |
| 2021/2022 | 177 | 139 | 36 | 175 | 0 | 2 | 0 | 1 |
| 2022/2023 | 175 | 141 | 34 | 175 | 0 | 0 | 0 | 1 |
| 2023/2024 | 175 | 141 | 34 | 175 | 0 | 0 | 0 | 1 |
| 2024/2025 | 269 | 189 | 80 | 269 | 0 | 0 | 0 | 1 |
| 2025/2026 | 271 | 189 | 82 | 271 | 0 | 0 | 0 | 1 |

## F. Preservation, validation and deliverables

All 85 original payloads (44,970,420 bytes), their provenance/receipts and accepted Phase 2 artifacts remain preserved. Of 570 baseline protected files, 568 are byte-identical; PLANNING_LOG.md and PROCESS.md retain their exact original byte prefixes with authorized append-only additions. Existing domestic/Champions League tracked files and public samples are included in this protection. Their private acquired archives are absent from this worktree and were not freshly certified.

The final checks are recorded in private `independent_validation.json`, `adverse_validation.json`, `reproduction.json` and `verification.json`. The separate verifier imports no Phase 3 adjudication helpers. It checks original bytes, goal chronology, score-column repairs, directed rule bindings, corrected participant occurrences, country-collision safeguards, every membership/crosswalk, all original case IDs/priorities/issues, all score/eligibility methods, dates, venue mapping and season counts. Its raw qualifying reconstruction exposed and corrected the four duplicates described above. This is implementation independence, not an independent human historian or proof of independent publisher origins.

**293 relevant automated tests passed**, including 44 new Phase 3 tests; those 44 were repeated after the final private-binding refactor. Existing Europa League acquisition/inventory, Champions League acquisition/inventory/history, source validation, match schema and audit snapshot tests were included. Synthetic fixtures test period separation, outcome-only eligibility, old-final uniqueness, dates, identities, legs/replays, statuses, abandonment before/after regulation, lineage, merging/splitting, coverage and private outputs. Ten adverse mutations were all rejected independently: missing/duplicate cases, lost membership, shootout leakage, partial abandoned scores, no-kickoff admission, erased date conflict, neutral flip, bridge corruption and season-total corruption.

A separate-process offline rebuild prohibits socket connections and writes a fresh temporary directory. All **13 producer artifacts plus the independent validation receipt (14 artifacts)** reproduce byte-for-byte from preserved originals and recorded decisions. It does not use a cached inventory as the producer input. Final file hashes and preservation results are bound by `verification.json`.

Restricted evidence, match records, decisions, receipts, logs and intermediate artifacts remain under ignored `data/private/`. Public code/tests contain generic logic and synthetic cases; this report contains aggregate results and source links, not copied raw fixture rows. Local-only Git exclusion does not claim protection from the owner's existing iCloud storage configuration. No permissions were requested externally.

### Deliverable map

Paths below are relative to `data/private/europe/europa_league/phase3/`; final artifacts are under `final/`. Attribute inventories are integrated into event records to avoid redundant copies.

| Requested deliverable | Location |
|---|---|
| 1. Complete original review dispositions | `final/review_dispositions.json` |
| 2. Evidence-backed decisions | `historical_decisions.json`, `observation_decisions.json`, `identity_decisions.json`, `coverage_decisions.json`, `additional_context_decisions.json`; bound by `final/input_freeze.json` |
| 3. Adjudicated intermediate inventory | `final/adjudicated_inventory.json` |
| 4. Regulation-time resolutions | Every event's `score`, `duration`, `period_evidence`, `decision_ids`; `final/observation_repairs.json` |
| 5. Date resolutions | Every event's `date`, original evidence and uncertainty |
| 6. Team identity resolutions | `final/identity_resolutions.json`, occurrence repairs and original source IDs |
| 7. Merger/split crosswalk | `final/event_crosswalk.json` |
| 8. Missing fixture investigation | `final/missing_fixture_investigation.json`, `qualifying_count_evidence.json` |
| 9. Additional acquisition accounting | Zero new payloads in `final/numerical_reconciliation.json`; frozen original input manifest in `final/input_freeze.json`; recovered observations in repairs |
| 10. Administrative/exceptional inventory | Event status, administrative evidence/result, duration, historical validity; `final/historical_contexts.json` |
| 11. Neutral venue inventory | Every event's `venue`, evidence, confidence and orientation |
| 12. Modelling eligibility | Every event's `modelling_eligibility`, disposition and result basis |
| 13. 36-season coverage | `final/season_coverage.csv` and `.json` |
| 14. Remaining holdouts | `final/remaining_holdouts.json`, corresponding complete event records |
| 15. Numerical reconciliation | `final/numerical_reconciliation.json` |
| 16. Independent validation | `independent_validation.json`, `adverse_validation.json` |
| 17. Automated test results | `verification.json`; private test logs |
| 18. Preservation/reproducibility | `verification.json`, `protected_before.json`, `process_prefix.json`, `reproduction.json` |
| 19. Completion report | This document |

`final/new_review_cases.json` accounts for all newly discovered cases. Earlier drafts are retained privately with descriptive draft/pre-correction names and are not the accepted final artifacts.

New public files are this report, `scripts/review_uefa_europa_league_history.py`, `scripts/verify_uefa_europa_league_history.py`, and `tests/test_uefa_europa_league_history.py`. Existing PLANNING_LOG.md and PROCESS.md received append-only additions. Earlier uncommitted Phase 1/2 files were left intact. No production dataset, models, application, other worktree, commit, index or remote was changed.

Offline review commands, from this worktree with the existing project-compatible Python environment:

```sh
python -B -m scripts.review_uefa_europa_league_history --check
python -B -m scripts.verify_uefa_europa_league_history --check
python -B -m pytest -q tests/test_uefa_europa_league_history.py
```

The producer's default output directory is private and exclusive-create; use `--check` against frozen artifacts. Both scripts prohibit ordinary public output paths. The complete test selection and receipt hashes are retained in the preservation receipt. The private `offline_rebuild.py` and `adverse_checks.py` preserve the fresh-build and mutation-check procedures; they exclusive-create their receipts, so preserve an existing receipt before rerunning them.

## G. Phase 4 readiness

The 11,422 INCLUDE records are ready for standardization for regulation outcome/goals and chronological evaluation; neutrality remains a separate eligibility dimension. Their seasonal identity correspondence must be mapped through the existing project identity conventions without asserting unreviewed legal succession or rewriting previous IDs.

Five pre-90-minute abandonments require historical retention and modelling exclusion. Four no-kickoff descriptions, 59 outside-target records, unplayed tie contexts and the annulled attempt remain outside ordinary modelling output. The extra-time abandonment retains its supported completed-regulation result while explicitly preserving incomplete extra time and the administrative award. Half-time absence and minor non-material uncertainty remain visible.

No material blocker or unresolved methodological dilemma remains for Phase 3. Absolute primary-source certainty and publisher independence have not been claimed. The only next approval required is the owner's explicit authorization to begin **Phase 4**. No standardization or production integration has started.
