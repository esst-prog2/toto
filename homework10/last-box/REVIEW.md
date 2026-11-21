# The Last Box — production review

Status: rendered locally and ready for user review; embedding/publication not authorized. 2026-11-21.

## Creative calls

Built only the approved concept-only The Last Box narrative. No prototype recording or mock working application is claimed. Five editable HyperFrames scene files cover the approved eight beats: ticket/table, manual entry, probability/table, historical reconstruction, logo close. A sixth topmost composition keeps the exact concept disclosure continuously visible. “Estimated probabilities” is explicit; outputs are em dashes and equal schematic rails, not fictitious data. Used the existing logo bytes, editorial sans-serif type, approved green/yellow/off-white palette and purposeful yellow-carrier/geometry transitions. No other storyline was produced. The film is intentionally silent so no essential content depends on audio; no paid music, generation service or login was used.

## Validation and corrections

First Chrome check exposed initial-hidden-state warnings and incorrect absolute SVG transform targets. Corrected GSAP initial hiding and coordinates; raised ticket/table indices to >=28px, persistent status to 56px, no-data disclosure to 42px, probability label to 52px, and refined repeated dropdown copy holds. Removed text overlap during the detail-to-table transition. Added matching yellow row→manual-field, unavailable-row→historical-cutoff and comparison-line→logo transitions. Backed up source before polishing under the ignored tools folder.

Final HyperFrames check (last-box-check-final.json) reports ok true, browserSkipped false; zero lint/runtime/layout/contrast errors, zero lint/runtime/layout/contrast warnings. Craft warning film_silent retained intentionally. One layout info container_overflow on ticket-carrier reflects the initially hidden future wide-table geometry inside the ticket illustration; inspected beginning/transition frames show no unintended visible text clipping. No suppression was added to conceal an error.

## What was inspected

Chrome Headless Shell through HyperFrames: settled beats, four seam strips and 360px phone-width sheet, then corrected exact frames at beginning, manual selection, probabilities, full table, cutoff, historical comparison and final hold. A fresh independent agent reviewed the final sheets and found no P0/P1 issues; still-frame limits were explicit. Critical status, title and probability labels remain readable; fine 14-row placeholders are secondary schematic detail and best inspected fullscreen.

The encoded MP4 itself was loaded and sought in Chrome through a separate playback-check composition at 0s, 15s and 29.8s; the resulting contact sheet was inspected. FFmpeg-decoded frames at 0, 1.8, 4.5, 8.5, 12.5, 15.5, 18.5, 23, 25.5, 28.5 and 29.966s were saved, with representative beginning/middle/end images visually inspected. No blank start/end or clipped logo was observed. Continuous interactive foreground playback was not observed: the CUA Chrome tab creation failed once with “The browser access host is unavailable”; it was not repeated and no Safari fallback was used. Chrome headless rendering/check/snapshot and actual encoded-video seeks succeeded.

## Measured delivery

Exactly 30.000000s; H.264 High profile; yuv420p; 1920×1080; 30/1 fps; 900 decoded frames; 1,809,970 bytes. No audio stream by design. Delivery-quality HyperFrames render completed in approximately 25.7s with one low-memory worker. Full FFmpeg decode-to-null passed without errors. MP4 moov precedes mdat (faststart). The exact bottom disclosure crop was compared across all 900 decoded frames; maximum mean absolute grayscale difference from the inspected first-frame strip was 0.193/255, below the 2/255 tolerance. This verifies near-constant visible disclosure, not general OCR or every text's legibility. Final logo is fully revealed at 27.35s and held through the last frame (~2.65s).

## Review delivery and limits

MP4: ../renders/the-pick-sheet-the-last-box-concept.mp4
Local Chrome watch page: http://127.0.0.1:8770/review/
Direct MP4: http://127.0.0.1:8770/renders/the-pick-sheet-the-last-box-concept.mp4
The local-only review server is homework10/serve_review.py; it supports MP4 byte-range requests for seeking. HTTP checks passed: player 200, video 200 with video/mp4 and exact bytes, partial request 206 with exact byte range. Restart from hw9-promo with `python3 -B homework10/serve_review.py --port 8770`; do not start a duplicate listener. Its PID and stop command are in .hw9-tools/hw10/review-server.json. The official HyperFrames editor preview was also started and returned HTTP 200 before rendering; it is stopped after review to avoid unnecessary background processes, while the lightweight watch page remains available for the user.

Weakest beat: the 3-second whole-table pullback explains shared structure and per-row unavailable state, but its 14 tiny row labels are not primary mobile reading content. The main title, highlighted unavailable row and persistent disclosure carry that beat; view fullscreen for detail. No specific phone/device runtime, real-time frame pacing or cross-browser claim is made. The output intentionally contains no numerical probability, selected outcome or successful historical prediction.

No webpage/application changes, embedding, commit, push or deployment. User approval of this final video is pending.

## Final video approval and embedding authorization — 2026-11-21

The user approved the final render and authorized embedding, commit/push and GitHub Pages deployment. Earlier approval-pending text is retained as historical context. See docs/hw10-publication.md (relative to worktree root) and PROCESS.md for actual embedding/public checks. Approved video bytes remain unchanged.
