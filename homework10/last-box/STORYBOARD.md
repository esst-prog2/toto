# The Last Box — concept-only storyboard for approval

## Approved for production — 2026-11-21 (current)

The user approved this storyboard and authorized final-video production and local review, adding an explicit “Estimated probabilities” label and prioritizing readability. The production implementation preserves the 30s narrative and timing; disclosures/reading labels were enlarged and dropdown selection holds refined. Earlier planning-only language below is historical. Embedding, webpage edits, commits, push and deployment remain unauthorized.

Status: detailed planning only, 2026-11-21. Supersedes the prototype-demonstration version of The Last Box in STORYLINES.md. No production composition, final render, new footage or webpage modification is authorized at this stage.

## Authority and scope

Re-read README sections The demo, The shape, The size and How we would know it works and cross-checked the approved homework9/index.html. The intended experience is fourteen manually entered competition/team fixtures, historical-data estimates for home win/draw/away win, a most-likely recommendation and one clear results table; the previous-meeting check uses only information available before that earlier meeting. Per-match unavailable states must not remove other available results. The webpage explicitly says these capabilities are in development; the synthetic prototype is not the film's subject. No accuracy improvement, betting success or new feature is claimed.

## Format and visual rules (proposed)

- Target: 30.0 seconds, 1920×1080 landscape, 30 fps (900 frames), produced with HyperFrames after storyboard approval. Google Chrome only for later visual checks.
- Silent-first: every story point is readable on screen. No voiceover; optional audio must never carry necessary meaning. Music choice is deferred.
- Approved source assets: homework9/assets/the-pick-sheet-logo.png; green #005239, warm yellow #ffcc00, off-white #faf9f3, ink #142d24. Preserve actual logo rather than redrawing it. Use the page's sans-serif/editorial hierarchy; no unapproved style replacement.
- A pencil/yellow mark carries the narrative from paper ticket to row selection, comparison guide, time cutoff and the existing logo's underline. Motion is purposeful match cuts/morphs, with settled reading holds; no slide deck, particles, fake dashboard, success confetti or repeated fade-up transitions.
- Frame-safe content: 192px horizontal and 108px vertical safe margins for essential copy. Proposed headline 72–88px, UI/diagram copy 36–44px, persistent status 32px minimum at 1080p. These are planning targets, not verified rendered sizes.
- Persistent exact status: “Concept preview · In development”, fully opaque on an uncluttered green/off-white contrast surface, visible from frame 0 through frame 899. It is functional disclosure, not a decorative corner label. Reserve a consistent safe-area status strip below the principal action; never cover it with a transition.
- All interface sequences are editorial illustrations, visibly unconnected to a browser or running app. No recorded prototype footage, loading spinner, working-web-app illusion, backend computation claim or final-interface promise. The selected UI arrangement is illustrative, not an additional application requirement.
- During the probability and past-meeting sequences add “Illustration only · No prediction data”. All numeric probability cells use “—”, and recommendation/result/comparison cells remain symbolic placeholders. No fixture date, real club/competition, score, percentage, winner, correctness tick or performance metric is invented. Bars/rails are equal schematic containers, not unequal invented probability magnitudes.

## Shot-by-shot storyboard

| Time / frames (30fps, inclusive) | Picture and action | Exact on-screen text and reading window |
|---|---|---|
| 0.0–3.0s / 0–89 | Close view of a traditional 13+1 Toto ticket: 14 numbered rows, columns 1 / X / 2. The pencil hovers over the last row without committing to an outcome; push in just enough to make hesitation legible. Status disclosure already visible. | “Fourteen matches” at 0.0–1.2s; replaced by “Which outcome?” at 1.2–3.0s. Ticket notation “1”, “X”, “2” and “14 (+1)”. |
| 3.0–6.0s / 90–179 | The yellow focus moves along the blank row. Paper rules straighten into a spacious editorial table with exactly 14 numbered rows; the transformation is visibly graphic, not an app launching. The last row remains the carrier. | “A clearer way to choose” from 3.3–6.0s. Column labels appear as part of the drawing: “Competition”, “Home team”, “Away team”. |
| 6.0–11.0s / 180–329 | Close into the same row. Three conceptual selection fields open one at a time; a pointer deliberately selects a fictional placeholder competition and two placeholder teams, then the frame pulls back to retain the 14-row context. No automatic weekly-ticket import is implied. | “Choose competitions and teams” from 6.0–11.0s. Field values: “Example competition”, “Home team A”, “Away team B”. Small table indicator “14 matches · entered manually”. |
| 11.0–17.0s / 330–509 | The row's three outcome columns unfold as equal-width comparison rails. A small labelled historical-data graphic feeds the schematic; yellow alignment guides connect all three columns to a blank recommendation cell, illustrating comparison without a made-up winning result. | “Compare all three outcomes” from 11.0–14.0s. Outcome labels: “1 · Home win”, “X · Draw”, “2 · Away win”; estimate placeholders “—”. “Suggest the most likely” from 14.0–17.0s, beside “Recommended outcome —”. Source label “Historical results → statistical model”. Secondary disclosure “Illustration only · No prediction data” begins at 11.0s. |
| 17.0–20.0s / 510–599 | Pull back: the same sheet contains competition/teams, three estimate columns and recommendation together. In one secondary row a clearly readable unavailable placeholder appears while the other rows remain present; this is a schematic availability state, not a simulated error. | “One table. Every match.” from 17.0–20.0s. One secondary-row label “Insufficient history”. Do not show a success state in any other row. |
| 20.0–24.0s / 600–719 | One row expands into a short timeline: earlier history → most recent meeting → selected future fixture. The yellow mark becomes a cutoff immediately before the earlier meeting. Only earlier history moves toward “Prediction then”; later events stay beyond the cutoff, with the actual-result field initially closed. | “Their most recent meeting” from 20.0–22.0s; replaced by “Use only earlier information” from 22.0–24.0s. Diagram labels “Earlier history”, “Last meeting”, “Your match”. |
| 24.0–27.0s / 720–809 | The prediction placeholder locks before the actual-result panel opens beside it. A neutral comparison bracket joins the two; no outcome values or correctness tick appear. A small availability note prevents a promise of universal backtest coverage. | “Prediction then ↔ Actual result” from 24.0–27.0s. Both fields show “—”. Supporting line “Where reliable history is available”. “Illustration only · No prediction data” remains visible until 27.0s. |
| 27.0–30.0s / 810–899 | The comparison line match-cuts into the actual supplied logo's yellow underline; reveal the complete original logo without warping it, then hold the finished lockup and address for at least 2.5s. Keep the concept status visible. | Actual logo text “The Pick Sheet”. CTA “Explore the project”. Address “esst-prog2.github.io/toto/”. Persistent “Concept preview · In development”. |

## Exact copy hierarchy and reading constraints

Only one main message occupies a shot at a time. The two changing headline windows in the opening contain two words each; main claim lines are at most six words. Supporting UI labels are a secondary reading layer; they must not compete with the headline. The probability sequence intentionally illustrates the data contract rather than an invented calculation, and the historical sequence intentionally illustrates temporal ordering rather than a successful prediction.

No additional caveat paragraph is required to understand the film: concept/in-development status is visible continuously, and the no-data disclosure is visible over all purported output illustrations. The end card invites exploration, not immediate access to a finished application.

## Production and QA after approval (not performed now)

Build seekable HyperFrames scenes and inspect exact timing/status continuity at every transition in Chrome. Check title/label legibility at embedded player size, 16:9 framing, full logo edges, all 14 rows in the pullback, conceptual/unavailable states, earlier-only historical cutoff and the 2.5s final hold. Render only after the approved production-preview review/authorization. No new model, real data or application capture is needed for this concept-only film.

Open approval point: accept this storyboard or request edits. No production has begun and no storyboard frame image has been generated.
