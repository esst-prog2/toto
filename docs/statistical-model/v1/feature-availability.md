> **Status: ARCHIVED — Version 1**
>
> - Model generation: Deterministic MVP
> - Audit date: 2026-11-26
> - Inspected commit: `878d45e`
> - Original audit commit: `15012b4`
>
> This document is preserved as a historical record and does not represent the current model development direction. Its findings may still inform subsequent model generations.

# Phase 1: feature availability

Snapshot: 2026-11-26, commit `878d45e47f1ef861b1b774ecc89c94af7851cb34`. This assesses construction feasibility, not predictive value or permission to train. No features were implemented. Local evidence: `data/real_matches.csv` and three `data/football_data_raw/*.csv`; the larger eight-column private archive exists only as committed reports here. See [inventory](data-readiness-audit.md).

For every historical feature, use only eligible information strictly before the target cutoff; fit normalization, priors and any tuning only inside training history. A date-only conservative filter is `history.date < target.date`, excluding all same-day rows. Original-date/final-result retrospective diagnostics require a separate interpretation from real-time reconstruction. The following formulas are candidate definitions for assessment, not approved methodological choices.

| Candidate | Sources and mathematical meaning | History required / missingness | Temporal leakage risk | Feasibility now |
|---|---|---|---|---|
| Points-based strength | Goals, team, date; sum(3 win + 1 draw)/n | At least prior results; small n unstable, unseen teams undefined | Full-season rates for earlier fixtures; extrema from future rows | Yes; existing overall PPM in statistics.py |
| Goal-difference strength | Goals; mean(GF-GA) | Prior games, sensitive to outliers/awards | Same cutoff risk; final adjudications known later | Yes; existing GDPM |
| Attack and defence rates | Goals and venue; sum(GF)/n, sum(GA)/n separately | Prior matches per team; opponent adjustment needs connected schedule | Including target goals or fitting whole-season strengths | Yes as raw averages; adjusted strengths require future research |
| Home/away performance | Team, venue, goals; venue-specific PPM/GDPM or GF/GA | Fewer observations per venue; no away history for new clubs | Target/future rows and future normalization bounds | Yes; existing venue PPM/GDPM, 5-game runtime minimum |
| Rolling form | Team/date/results; mean points or goals over last k games | k prior eligible games; fallback policy undecided | Including target or season-end tables; same-day ordering | Yes with date cutoffs; k and fallback unapproved |
| Recency-weighted form | Dates/results; sum(exp(-lambda*age)*value)/sum(weights) | Earlier dates; effective sample size can be small | Lambda chosen on test outcomes; later final results backdated | Yes mathematically; decay and time semantics undecided |
| Head-to-head | Ordered teams/date/goals; prior pair outcome fractions | Sparse pair history, changed personnel, orientation matters | Selecting most recent meeting from whole archive instead of pre-target history | Limited yes; last-meeting lookup absent, no implementation authorized |
| Home advantage estimate | Venue/results; historical home-away rate difference or coefficient | Enough league/season history, team/schedule imbalance | Full-season estimate or future teams contaminating early season | Descriptive comparison feasible; fitted coefficient not present |
| Competition/tier context | source_division locally; league in canonical schema; possible tier metadata | E0/E1 observed; broader archives unavailable; cross-tier links sparse | Future promotion status or outcome-derived competition rating | Labels feasible for local English data; numeric competition strength unvalidated |
| Opponent-adjusted strength | Team pair/date/goals; strength relative to schedule | Connected historical match network; new teams and disconnected leagues problematic | Ratings computed using later opponents/results | Source inputs available locally; method and estimation undecided |
| Promotion/relegation indicator | Season membership plus authoritative division/tier continuity | Only two local seasons and prior E1; gaps/renamings undermine inference | Using next-season membership as current information | Partial membership comparison; reliable long panel unavailable here |
| Season progress / sample count | Season/date/team; number of prior eligible games | Reschedules and incomplete seasons distort nominal rounds | Final season match totals used as pre-match feature | Prior counts feasible; stage/round absent in standardized CSV |
| Rest days / congestion | Consecutive team dates; date difference and prior-window counts | Only league matches locally; cup/international workload absent | Future schedule corrections, unknown time or completion | League-only proxy feasible; total workload unavailable |
| Bookmaker implied odds | B365CH/CD/CA or adapted odds; q_i=1/o_i, illustrative normalized q_i/sum(q) | Local 1,312 rows complete; broader archive strips odds | Closing prices may be later than prediction timestamp; availability not timestamped | Local only; normalization not calibration, timestamp protocol absent |
| Shots, shots on target, cards, corners, fouls | Raw HS/AS/HST/AST/HY/AY/HR/AR/HC/AC/HF/AF; lagged aggregates | Present in three raw files, lost in adapter; verify semantics and missingness | Target-match statistics are post-match and unusable as predictors | Local lagged construction possible; no broad standardized coverage |
| Team identity continuity | Persistent team IDs and dated aliases | None supplied; match_id identifies fixtures, not clubs | Modern alias knowledge or successor clubs merged retrospectively | Exact-name within-source grouping only; cross-era continuity unresolved |
| Players, lineups, injuries, xG, weather, travel | Dedicated timestamped sources, coordinates or player events | No suitable local variables | Post-match xG, hindsight injuries/lineups | Unavailable; README explicitly defers player-level scope |

Minimum history and smoothing are research questions, not justified by the MVP thresholds. The locally available period supports limited demonstrations, not a multi-decade out-of-time assessment. Missing private sidecars prevent deciding exceptional-match eligibility or stage-specific features from the eight-column schema alone. No current feature candidate resolves intended-use rights or information-time ambiguity automatically.
