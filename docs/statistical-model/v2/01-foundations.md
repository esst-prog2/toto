# Version 2 – Statistical Foundations

Created 2026-11-27. This knowledge synthesis preserves the statistical lessons of the 2026-11-26 audit; it selects no model, feature set, parameter values or development programme. The primary source is the archived [feature availability assessment](../v1/feature-availability.md), supported by the other Version 1 audits linked below. **Evidence labels:** audited facts were verified in that snapshot; documented historical information records earlier reports; statistical considerations explain possible interpretations; illustrative examples are hypothetical, not project measurements. Predictive usefulness remains untested unless explicitly evidenced.

## 1. Lessons Learned from Version 1

Version 1 was a deterministic points/goal-difference rating rule with no outcome probability estimates. Manually chosen weights combined points and goal difference at 70%/30% and overall/venue performance equally; a rating difference outside ±0.10 selected a winner, otherwise a draw. These choices were not statistically optimized. Recency weighting, opponent-strength adjustment and competition-strength adjustment were absent. Ratings on a bounded scale were not probabilities, and rating similarity was not an estimate of draw probability. See the [current-model audit](../v1/current-model-audit.md).

The [evaluation audit](../v1/evaluation-audit.md) records these previous development benchmark results on 380 Premier League 2023/24 matches:

| Method | Accuracy |
|---|---:|
| Original Version 1 rule | 40.00% |
| Version 1 with pooled venue normalization | 41.58% |
| Always-home baseline | 46.05% |
| Closing bookmaker favourite | 59.74% |

The benchmark used 932 prior-season English matches. Its evaluation outcomes informed the normalization change, limiting independence even though held-out matches did not enter rate estimation. Bookmaker ties counted any jointly shortest-priced outcome as correct, and closing-price availability at an earlier prediction time was not established. These figures describe past development evidence, not independent evidence of future predictive performance. Functional reproducibility did not establish statistical adequacy or probability calibration.

## 2. Available Statistical Information

The canonical archive has eight variables, as documented in the [data-readiness audit](../v1/data-readiness-audit.md):

| Variable | Meaning and statistical boundary |
|---|---|
| `match_id` | Deterministic fixture identifier derived from league, season, date and ordered team names; not a persistent club ID or guarantee of independent observations |
| `date` | ISO calendar date under the applicable historical policy; no intrinsic kickoff time, timezone or publication timestamp |
| `league` | Competition identity; not a numerical estimate of competition strength |
| `season` | Canonical season label; not an exact measure of season progress or data availability |
| `home_team` | Source-supported nominal home-team name; continuity and physical home venue are not guaranteed |
| `away_team` | Source-supported nominal away-team name; cross-source/cross-competition identity requires separate evidence |
| `home_goals` | Nonnegative integer goals under the accepted outcome policy; regulation-time and administrative semantics require context |
| `away_goals` | Corresponding away goals; score differences determine 1/X/2 only for the intended outcome definition |

**Audited local evidence:** 1,312 English matches cover Premier League 2022/23 and 2023/24 plus Championship 2022/23, with 44 exact team labels. The local adapted file uses six core history fields plus division, fit/evaluation role and three odds columns; it is not itself the full eight-column canonical archive. Its three raw sources additionally retain times and match statistics. **Documented historical information:** Version 1 reports 156,321 screened historical rows across 14 competitions, with uneven coverage and separate sidecars. Those private files were absent from this worktree at audit time; this synthesis neither accesses nor independently validates them. Their reported size does not imply local access, completeness, regulation-time eligibility or training permission.

The following categories describe potential information, not a final feature list. “Canonical” means structurally derivable if sufficient eligible records are accessible, not that the absent archive was inspected. Let GF and GA denote a team's goals for and against; all historical summaries refer to observations before the relevant cutoff.

| Category | Meaning, sources and potential construction | History, limitations and availability |
|---|---|---|
| General team performance | Teams, dates and goals yield PPM = (3W + D)/n, mean GF−GA and W/D/L fractions. These summarize observed results. | Canonical; requires prior games, with unstable small-n rates. Awards affect interpretation. Full-season summaries or normalization bounds can leak later results. |
| Attacking and defensive performance | Teams, venue and goals yield mean GF and mean GA separately; contextualized strength concerns scoring and prevention beyond these raw averages. | Canonical raw rates; enough matches and opponent variety needed. Goals depend on opponents and match context; separate latent strengths are not directly observed. Target-match goals cannot be inputs. |
| Relative team strength | Ordered opponents, dates and results form a match network; performance relative to opponent quality can characterize schedule strength and relative ratings. | Canonical inputs, but adjustment is not supplied by the schema. Disconnected networks, limited overlap and new teams weaken identification. Later opponent results can leak into historical ratings. |
| Temporal performance | Dates and results support last-k-game means, recent sequences and age-weighted summaries. | Canonical; k and decay are unspecified, sparse histories remain sparse. Same-day order and later corrections complicate cutoffs; selecting windows on evaluation outcomes compromises independence. |
| Venue effects | Nominal home/away labels, dates and goals support venue-specific rates and historical home–away contrasts. | Canonical proxies; fewer matches per venue, schedule imbalance and neutral venues limit interpretation. Actual venue metadata is supplementary; full-season venue estimates leak future outcomes. |
| Competition context | League/season labels distinguish contexts; divisions and authoritative tier metadata locate teams within hierarchies. Competition strength concerns the level of opposition, while scoring/draw patterns describe other characteristics. | Labels are canonical; tier histories and links across competitions are supplementary. Local E0/E1 labels exist, but cross-league numerical comparability is unverified. Future membership is not contemporaneous information. |
| Team history | Dated membership supports possible promotion/relegation histories; ordered pair histories support orientation-aware head-to-head rates. Persistent IDs and dated aliases establish continuity. | Canonical pair histories can be sparse; two local seasons provide limited membership evidence. Legal continuity, refoundings and gaps need supplementary evidence. Today's aliases or a later meeting can introduce hindsight. |
| Season context | Season/date/team fields yield prior match counts and observed sample size; they provide a partial measure of progress. | Canonical counts; stages/rounds and a complete schedule require supplements. Postponements and incomplete coverage distort progress; final season totals are unavailable early in the season. |
| Workload | Team dates give days since the previous recorded match and counts in a preceding interval. These are rest/congestion proxies. | Canonical league-only proxies; missing cups/internationals understate workload. Actual times, completion dates and complete schedules are supplementary; corrected future scheduling cannot be treated as previously known. |
| Supplementary information | Odds can yield reciprocal-price quantities; raw shots, on-target shots, corners, fouls, yellows and reds support lagged performance summaries. | Not in the canonical eight fields. Local raw files contain these statistics; the adapter retains only three odds columns. Definitions, missingness and observation times vary. Target-match statistics are post-match; closing odds may postdate the decision. |

For decimal odds oᵢ, qᵢ = 1/oᵢ and qᵢ/Σqⱼ illustrate margin normalization, not demonstrated probability calibration. Local closing Bet365 prices were complete across 1,312 matches, while several other bookmakers/markets had blanks; the raw files' times lack timezone and publication information. Broader odds/statistics coverage cannot be inferred from the canonical archive.

Player availability, lineups, injuries, suspensions, expected goals, weather and travel information require dedicated supplementary sources; no suitable variables were established in the audit. Post-match expected goals or retrospectively corrected injury information would not establish pre-match availability. Unseen teams, identity uncertainty, missing sidecars, source permissions and historical target semantics remain limitations across categories. The [readiness summary](../v1/modelling-readiness-summary.md) distinguishes these gaps from implemented functionality.

## 3. Key Statistical and Methodological Considerations

### 3.1. Relative team strength and opponent quality

Observed performance is conditional on the opponents encountered. **Illustrative example:** two teams each take 12 points and record +4 goal difference over eight matches; one faces predominantly strong opponents, the other predominantly weak opponents. Their identical PPM of 1.5 and GDPM of 0.5 do not establish equal underlying strength. The first schedule may make those results more informative about high strength, but that interpretation itself depends on reliable knowledge of opponent quality.

Raw performance summarizes outcomes without adjusting for the schedule. Opponent-adjusted performance separates, conceptually, a team's contribution from the difficulty of its opposition. Adjustment is relational: opponent strengths are also uncertain, change over time and depend on their schedules. A weakly connected match network may not identify relative levels between groups. Neither raw-rate equality nor an adjustment label proves a reliable ranking.

### 3.2. Attacking and defensive strength

Team strength can be multidimensional. **Illustratively**, mean GF/GA of 2.0/1.0 and 1.2/0.2 both give GDPM +1.0, yet describe different scoring environments and balances between attack and prevention. Collapsing the pair into one difference discards that information. Depending on opponents and context, those patterns can imply different distributions of match outcomes, including draws; the example alone does not establish which team is stronger.

GF contains information about scoring, while GA contains information about preventing opponents from scoring. Neither is a pure measurement of an intrinsic ability: the opposition's defence/attack, venue, match state and administrative treatment also affect scores. Separate goal summaries preserve distinctions that a scalar can hide, but interpreting them as underlying attacking and defensive strength requires assumptions. Their joint information and uncertainty matter; more dimensions do not automatically improve prediction.

### 3.3. Temporal relevance of historical information

Squads, coaching, tactics and competitive circumstances can change, so old and recent results need not be equally informative about present performance. Recency also trades historical sample size against responsiveness: recent observations may reflect current conditions more closely but be noisier. Greater recency does not make every recent result intrinsically more reliable.

Exponential weighting illustrates a continuous age effect:

\[
w(t)=\exp(-\lambda t)=2^{-t/h},\qquad h=\frac{\log 2}{\lambda},\quad \lambda>0.
\]

Here t ≥ 0 is observation age in a consistent time unit, λ is the decay rate in inverse units, and h is the half-life. Larger λ means faster decay; larger h means slower decay. At λ = 0, weights are equal and the half-life is unbounded. A weighted mean has the form Σwᵢxᵢ/Σwᵢ.

**Illustrative relative weights, without choosing a calendar half-life:**

| Age | 0 | h | 2h | 3h |
|---|---:|---:|---:|---:|
| Weight | 1.000 | 0.500 | 0.250 | 0.125 |

This gives a numerical decay illustration without selecting λ or h. Weighting cannot repair incorrect dates or make a later-published result available earlier.

### 3.4. Training history versus current team history

The observation period used to estimate general model parameters and the history used to characterize a team's current performance are different statistical objects. The first can contain evidence about recurring relationships, population variation or scoring/venue patterns across many teams. The second concerns how informative particular observations are about a specific team at a particular date. They need not have the same temporal extent or weighting.

Decades of results may therefore contain useful information about general relationships even when one decades-old game says little directly about today's squad. That value is conditional on historical comparability: changes in rules, scoring environments, competition formats and source coverage can make pooled relationships nonstationary. A long archive is neither inherently irrelevant nor automatically exchangeable across eras. This distinction selects no estimation period or team-history window.

### 3.5. Home advantage and venue-specific performance

General team strength concerns performance beyond the fixture's venue. Overall home advantage is a systematic venue-associated difference within a population. Team-specific home/away performance can additionally reflect distinct local patterns, but observed venue differences also contain sampling variation and opponent imbalance. These concepts are related, not interchangeable.

The Version 1 audit showed why independently rescaling home and away rates can erase a common uplift or reverse cross-venue comparisons. Pooled scaling retained a common reference; it did not prove that the remaining venue signal adequately represented home advantage. Venue effects may differ by competition and period, and their empirical comparison depends on comparable schedules and information cutoffs.

Venue subsets have fewer observations than overall histories, making apparent team-specific effects unstable. Nominal home designation is also not proof of physical home advantage: neutral venues, relocations and unusual attendance conditions are not encoded in the canonical schema. Without that context, venue rates measure designation-associated performance rather than an isolated causal home effect.

### 3.6. Competition strength and cross-division comparability

A high PPM against lower-tier opponents is not automatically equivalent to the same PPM against stronger opposition. Promotion changes the opponent population; relegation changes it in the opposite direction. Carrying raw rates across that boundary preserves observations but does not establish their scale equivalence. Changes in personnel and identity can further complicate continuity.

Team-level strength describes individual teams; competition strength concerns the level/distribution of the participant population. Competition-specific characteristics such as scoring frequency, draw rate, schedule structure or venue effects are distinct from that strength level. High-scoring matches alone do not identify a stronger league. Differences in these characteristics and unequal schedules can confound comparisons across leagues, divisions and eras. Version 1's inclusion of Championship history supplied promoted teams with records, without validating a cross-tier conversion.

### 3.7. International competitions as connecting match networks

Conceptually, teams are nodes and played matches are edges in a comparison network. Domestic competitions mostly connect clubs within countries; international club competitions, particularly the UEFA Champions League, can add cross-country edges. Such links may provide relative information where otherwise separate domestic networks have no direct match comparisons. Their statistical relevance is connectivity, not proof that a particular cross-league method will work. No international match dataset is established as accessible by this synthesis.

Participants are selected, often from the upper part of their domestic distributions, and are not representative samples of their entire leagues. Countries have unequal representation; successful clubs accumulate more matches; qualification and progression condition the observed sample. Sparse or uneven international links can make country-level comparisons highly uncertain and concentrated on a few clubs or periods. Strong international performance by selected clubs is insufficient evidence of the overall strength of their domestic league.

Consistent team identities across competitions are essential to interpret an international edge as joining the correct domestic node. Name variants, refoundings or incorrect merges can falsely disconnect or connect networks. Connectivity alone does not eliminate selection bias, temporal change or context differences between domestic and international fixtures.

### 3.8. Historical sample size and statistical uncertainty

Small samples produce unstable rates: a few wins or extreme scores can dominate PPM, GF/GA and venue differences. Nominal n counts recorded observations, but repeated opponents, correlated matches, shared team trajectories and unequal weights affect how much independent information those observations contain.

For nonnegative weights, a common weight-concentration diagnostic is

\[
n_{\mathrm{eff}}=\frac{(\sum_i w_i)^2}{\sum_i w_i^2}.
\]

Equal positive weights yield n; concentrating weight on a few matches reduces this quantity. It does not by itself account for dependence, changing team strength, biased coverage or differences in observation quality, and it is not a universal uncertainty calculation.

Smoothing can stabilize noisy frequencies; shrinkage can moderate extreme estimates toward an explicitly contextual reference, trading variance against possible bias. Uncertainty expresses limited information rather than concealing it behind a single estimate. These concepts prescribe no implementation here. New or insufficiently observed teams may have no defined empirical rate; promoted teams may have many observations but little directly comparable top-tier history. Version 1's 10/5 thresholds were manual sufficiency rules, not evidence that uncertainty becomes negligible above those counts.

### 3.9. Feature availability versus predictive value

Constructibility is a data property; incremental predictive information is an empirical property under a specified prediction setting. Related summaries can be redundant: with common denominators, PPM = 3p(win) + p(draw), while GDPM = mean(GF) − mean(GA). Including several transformations of the same outcomes does not create independent evidence. Correlation can make attribution difficult; exact or near-linear relationships can create multicollinearity and unstable interpretations where quantities are estimated jointly.

Descriptive association in historical data does not establish additional out-of-sample contribution beyond other available information. Apparent gains may reflect sampling noise, flexible selection or leakage. Head-to-head rates are especially sparse and can span different players, tactics, divisions or legal club identities; old meetings may say little about the current pairing. None of these considerations proves that head-to-head information is useless or another feature is superior. Empirical assessment of incremental information must be distinguished from plausibility, and Version 1 provides no such comparative evidence for the unimplemented candidates.

### 3.10. Temporal leakage and historical information semantics

For a target fixture with cutoff τ, its own goals, shots or disciplinary events are target-match information, not historical inputs. Earlier observed results may inform historical summaries; later matches, later-updated ratings, season-end standings and future membership are future information. All outcome-dependent transformations—including scale bounds, shared parameter estimates and feature-selection/tuning decisions—have temporal provenance, not just the rows explicitly assigned to a team. Reusing an evaluation season for development reduces independence without requiring a direct row-level leak.

Under realistic pre-match reconstruction, the relevant boundary is when information was available before τ. A playing date alone does not establish that boundary: same-day ordering, postponed/resumed games, closing prices and later administrative decisions complicate it. The date-only strict-earlier-day interpretation in the archived feature audit is conservative about same-day results, but cannot establish publication-time availability.

**Existing project policy is preserved:** retrospective internal diagnostics use original football dates and accepted final historical results, including documented later adjudications, without administrative-publication-date filtering. Initial kickoff and completion dates remain separate in supporting records; a no-kickoff award is NOT_PLAYED. This is documented in the [collection workflow](../../accelerated-five-phase-workflow.md) and the [Version 1 evaluation audit](../v1/evaluation-audit.md). It defines final-history semantics; it does not establish what was knowable before each match. A subsequently awarded result associated with an earlier football date may affect later historical summaries despite being unknown then. Calling that exercise retrospective is essential to interpreting its claims, without changing the approved policy.

**The established international outcome policy is also preserved as stated in the instruction for this document:** 1/X/2 concerns regulation time, including stoppage time, rather than extra time, shootout success, aggregate tie victory or qualification. A regulation-time draw stays a draw even if a club subsequently advances. Accepted administrative-result treatment and source-specific decisions retain their existing documented authority; this synthesis creates no new precedence or eligibility rule. The five archived audits do not independently document the provenance or record-level application of that international policy, so it is attributed to the current user instruction rather than presented as a newly verified archive finding.

Earlier collection reports describe differing completion/availability-date conventions, while canonical rows omit event status, regulation-time breakdowns and publication timestamps. Absent private sidecars prevent establishing which policy versions apply to every output. These ambiguities remain documented, without rewriting dates, overriding dispositions or reopening approved historical decisions. Structural validation, historical adjudication, access rights and predictive readiness are distinct assurances. As preserved in the [data audit](../v1/data-readiness-audit.md), source-use restrictions and unresolved upstream rights also survive standardization. This foundation makes no claim that the complete private archive is modelling-ready.
