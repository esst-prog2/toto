# Phase 1: modelling readiness summary

Completed 2026-11-26 on `feature/statistical-model`; inspected HEAD `878d45e47f1ef861b1b774ecc89c94af7851cb34`. **The repository provides a reproducible deterministic benchmark and substantial historical collection infrastructure. It does not yet provide an implemented probabilistic model, a locally available multi-league modelling dataset or an independent evaluation of the intended next model.** Phase 1 is complete as an audit, with unavailable data and methodological uncertainties explicitly bounded; this is not a training-readiness certification.

## Verified facts

- [Current model audit](current-model-audit.md): the application uses 150 synthetic records, fixed points/goal-difference ratings, common venue min/max scaling and ±0.10 label thresholds. It returns no outcome probabilities. README's competition selection, individual failures and previous-meeting backtests remain planned.
- [Data readiness audit](data-readiness-audit.md): 1,312 unique locally available real-match rows across three English source files; adapted CSV and existing JSON reproduce byte-for-byte. All eight local data files have recorded SHA-256 versions. No `data/private/` is present here. Reported private historical screened coverage totals 156,321 rows in 14 competitions; those bytes were not inspected or revalidated here.
- [Feature availability](feature-availability.md): lagged team/venue/goal/form features are technically constructible locally; broad cross-era identity, player variables and timestamped availability are missing. Feature feasibility does not establish utility or training permission.
- [Evaluation audit](evaluation-audit.md): current fixed-rule replay scores 158/380 (41.58%), below always-home 175/380 (46.05%) and closing favourite 227/380 (59.74%). The benchmark informed the normalization correction and is development evidence. Fresh full suite: 2,678 tests and 27 subtests passed, zero failures/errors/skips.

## Infrastructure assessment

| Area | Existing reusable evidence | Limitation / future integration requirement |
|---|---|---|
| Python architecture | `src/toto_estimator/`: data, validation, statistics, predictor, typed models, ticket and UI-independent service; thin Streamlit app | Service has no competition or prediction-date argument; grouping by bare team name mixes leagues if a caller concatenates them |
| Input validation | `data.py`, `validation.py`, `outcomes.py`; strict score/date/name/result checks | Schema validation does not enforce chronology, permissions or match status; season blanks and duplicate-history checks differ between runtime loader and importer |
| Historical normalization | `historical_import.py`, explicit HistoricalSource metadata, canonical seasons/dates, deterministic IDs, duplicate/conflict accounting | Identity depends on date/name; no stable club entity table, persistent reconciliation store or universal stage field |
| Reproducible artifacts | `scripts/artifact_io.py`, immutable-source acquisition/receipt families, manifests, source-specific policy/standardizers, independent validators | No generic modelling dataset builder/availability join; private inputs and full sidecars absent here; many scripts expect paths in another original worktree |
| Statistical components | `statistics.py` rates and scaling; `predictor.py` deterministic rating; synthetic generator isolated from runtime | No probability model/calibration, optimizer, uncertainty estimates or serialized fitted-model protocol |
| Evaluation | `build_real_spike_dataset.py`, deterministic split and baseline measurements; exact reproducibility and fitting-isolation tests | One development test season, no rolling/nested evaluation, probability metrics, model registry, frozen unseen test protocol or last-meeting reconstruction |
| Dependencies | `pyproject.toml`: Python >=3.11, NumPy >=2.1.0, pandas >=2.2.3, Streamlit >=1.49.0, Jinja2 >=3.1.5; optional pytest >=8.3.3; constraints-tested-py313.txt and dependency-environment.md | No declared SciPy/scikit-learn/statsmodels modelling dependency. System interpreter has SciPy but not sklearn/statsmodels; incidental installation is not project support. Exact constraints describe an earlier tested snapshot, not current portable lock or Python 3.11 test |
| Verification | Full existing suite passed in external environment; tests cover malformed inputs, guards, reproducibility, workflow and app | No new tests needed for documentation; no fresh manual UI test; synthetic collector tests are not validation of absent real sources |

System replay environment: `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3`, CPython 3.13.12, pandas 3.0.2, NumPy 2.4.4; pytest/Streamlit absent there. Full-suite interpreter and exact invocation are recorded in evaluation-audit.md. Existing external environment was reused; nothing installed, upgraded or reconfigured. Source/API web research was unnecessary for this repository audit; dependency statements describe inspected files/runtime, not current upstream recommendations.

Potential integration would need a competition-scoped, cutoff-aware data contract, explicit linkage to accepted historical policy/sidecars and provenance, identity decisions, a genuine three-outcome prediction interface, row-specific availability, and an evaluation boundary independent of the UI. These are gaps identified, not implementation instructions or an approved design.

## Existing assumptions

Fixed weights, draw band, equal old/new match weight, 10/5 sufficiency thresholds, cross-tier comparability and exact-name identity are inherited MVP assumptions, not validated statistical conclusions. Private collection reports assume source-specific approved decisions and limited external verification; structural PASS is not exhaustive historical truth. No-use restrictions are lifted by schema validation.

The current retrospective diagnostics policy deliberately pairs original football dates with accepted final historical results, including later administrative decisions. Earlier standardized collections describe different availability/completion-date rules. This audit preserves both the latest stated policy and the documentary discrepancy; it cannot certify unobserved migrations or silently unify dates.

## Identified weaknesses

The deterministic predictor cannot express uncertainty or calibrated draw probability; it trails simple baselines on its one development season. Min/max scaling depends on the supplied team population and extreme rates. No opponent strength, promotion correction, recency or sample-size shrinkage is implemented. Date filtering is delegated to callers; app/service APIs cannot guarantee historical pre-match reconstruction. Match IDs do not solve club identity; the standardized schema does not encode stages, regulation-time outcomes or chronological/rights metadata. Older league reports have differing completeness, status and date semantics. Model comparison using closing odds also needs a consistent decision time and tie convention.

## Missing information

Actual private originals, manifests, sidecars and current policy versions in this worktree; comprehensive persistent team identity/continuity; target outcome definition (accepted final or regulation-time result); timestamped pre-match availability and kickoff timezone; independently untouched evaluation period; intended-use permission for each selected source; agreed small-sample policy and assessment metrics. No broad dataset availability or training clearance is inferred from reported counts. Existing restrictions and upstream uncertainty are documented in the collection reports; they require source-specific resolution if relevant to later work.

## Potential research directions (not model selection)

Investigate whether recency, explicit home effects, opponent-adjusted strength, separate goals-for/against information and principled uncertainty improve on the frozen benchmark. Compare draw handling and probabilistic calibration to simple league-frequency and odds-derived references under consistent information cutoffs. Examine promotion/tier transfer and stability across seasons/competitions. These are audit-derived research questions only: no model design, literature review, experiments or new features were undertaken.

## Methodological decisions requiring human approval

1. Define whether the next workstream targets retrospective final-history diagnostics, real-time pre-match forecasting, or separately labelled evaluations of both; choose regulation-time versus accepted administrative targets.
2. Decide how the existing original-date/final-result policy interacts with older availability/completion-based collections. Approve any future derivative policy changes rather than silently rewriting historical evidence.
3. Select accessible permitted datasets and accepted match-status/identity scope, with explicit handling of holds, awards, resumptions, playoff/extra-time outcomes, incomplete seasons and unseen/promoted teams.
4. Approve the independent temporal evaluation boundary, development/validation protocol, probability and label metrics, and comparable baseline timing/ties before model selection or tuning.
5. Authorize the next development phase and any eventual model/dependency choices separately. This audit makes no such choices.

## Preservation and documentation scope

A SHA-256 comparison of all 306 pre-existing tracked files against the initial commit found 305 byte-unchanged files; only PLANNING_LOG.md has authorized appended lines, with its complete earlier byte prefix intact. All application/source/scripts/tests/data/configuration and earlier reports are unchanged. The five new audit files plus new PROCESS.md and append-only planning log comprise the exact seven-file local commit scope. No private inputs, credentials, new raw records or source extracts were added. Relative deliverable links and whitespace checks passed. This covers this worktree’s tracked files, not absent private files or another worktree.

## Recommended next steps

First resolve the target and historical information-time interpretation. Then arrange a separately authorized, hash-bound local snapshot of selected private data plus required sidecars without disturbing collection work. Verify that snapshot's identities, eligibility, dates and intended-use constraints. Reserve an unseen chronological assessment period before research/model selection. Only after explicit approval proceed to methodology/design and later feature implementation or training. Stop here as requested.
