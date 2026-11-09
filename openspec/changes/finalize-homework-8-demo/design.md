## Context

See proposal.md for motivation. app.py currently edits a synthetic 14-match ticket with team dropdowns and a Generate predictions button. service.run_workflow validates the ticket atomically and returns deterministic predictions; the existing predictor has no probability interface. Earlier synthetic MVP specs remain unarchived, while published openspec/specs is empty. The approved README describes future scope, not implementation evidence.

## Goals / Non-Goals

**Goals:** Plan a competition-aware workflow with explicit probabilities, per-row outcomes and reproducible pre-match historical comparisons while reusing historical validation and private provenance.

**Non-Goals:** No implementation in this commit, no new dataset acquisition/integration, no automatic weekly-ticket download, no exact-score UI, no player-level features or model-selection UI. No statistical model or dependency is selected by this proposal.

## Decisions

- Preserve exact approved README wording and record the current-versus-target distinction here, rather than adding an unapproved README status section.
- Extend the existing app/service boundary in a later apply phase, rather than introduce a second application. Represent prediction and backtest availability separately per row; the existing atomic failure behavior cannot satisfy this target.
- Scope team/history lookup by competition. Do not feed an unfiltered multi-league private history into the current predictor. Keep source corrections, exception eligibility and provenance available outside the eight-column match schema.
- Add a genuine three-outcome probability contract; current rating differences must not be relabeled probabilities. Statistical model selection and probability evaluation are explicit future implementation tasks, rather than an unsupported choice in this documentation commit.
- Establish a deterministic prediction cutoff from available fixture metadata or an explicitly recorded as-of time. For the previous meeting, reconstruct all calculations using only earlier eligible history. If ordering or eligibility is uncertain, return unavailable instead of guessing. Compare results in the historical fixture's original home/away orientation.
- Keep the previous single-meeting comparison separate from aggregate unseen chronological evaluation; one prior match is illustrative feedback, not evidence of predictive quality.
- Retain local data and unresolved licensing limits; a permitted demo subset or synthetic fallback is preferable to packaging private data with the public app.

## Risks / Trade-offs

- [README target can be mistaken for delivered functionality] → Preserve this explicit planning status; implementation tasks remain unchecked.
- [Leakage from future observations or parameter tuning] → Use strict historical cutoffs for every backtest stage and an independent chronological evaluation split.
- [Team aliases, phase repeats and uncertain administrative results] → Reuse validated competition/source identities and conservative eligibility metadata; report uncertainty.
- [Source rights limit model or presentation use] → Review intended-use permissions before implementation data selection; retain synthetic fallback.

## Migration Plan

This commit replaces README and adds planning only. Future implementation requires a separate apply instruction, targeted regression/UI checks and evaluation of a selected probabilistic method. Do not overwrite existing development measurements. Rollback of this documentation scope is a normal revert; no dataset or runtime migration is performed now.
