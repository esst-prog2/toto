## Why

Homework 8 needs an approved, testable demo scope for the next useful version. The current synthetic MVP returns deterministic labels, lacks competition selection, and does not expose outcome probabilities or previous-meeting backtests; the approved README describes the target, not delivered features.

## What Changes

- Replace README with the user's exact five-section Homework 8 wording, removing all additional sections.
- Plan manual entry of 14 competition-scoped fixtures, probability outputs and a single results table.
- Plan match-specific failures and leakage-free backtests of the most recent previous meeting.
- Preserve chronological evaluation, honest performance reporting and private-data/licensing restrictions.
- Keep all application implementation, datasets and existing evaluation artifacts unchanged in this planning-only change.

## Capabilities

### New Capabilities

- `homework-8-demo`: Target competition-aware 14-match workflow, probability contract, historical backtest and permitted demonstration fallback.

### Modified Capabilities

None. `openspec/specs/` has no published capabilities. The earlier unarchived `build-synthetic-toto-mvp` change defines the current deterministic synthetic MVP; this proposal explicitly supersedes its synthetic-only UI, all-ticket failure and deterministic-only target scope for a future implementation, without rewriting that historical change.

## Impact

This commit changes README and planning artifacts only. A later approved implementation would affect app.py, service/ticket validation, prediction result types, competition-scoped historical access and evaluation. No statistical model or new dependency is selected here. Existing 40.00%/41.58% results remain development evidence, not validation of the proposed method. Private raw and derived datasets must remain excluded from Git and deployment unless separately cleared.
