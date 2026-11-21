# The Pick Sheet — selected Homework 9 direction

Status: local implementation prepared for review, not committed or published. User selected Variant A — Match Programme on 2026-11-21. Final implementation approval is pending.

## Selected page and identity

- Review entry: `homework9/index.html`, served at http://127.0.0.1:8769/ . Variant A retains the same content/branding at `/variants/a/`; B/C remain comparison references.
- Preserve A's original editorial typography, hierarchy, generous spacing, desktop columns, mobile stacking and five sections. Existing base and A styles are reused, with identity overrides in `homework9/assets/brand.css`.
- Public-facing name: The Pick Sheet, including HTML titles, description metadata, navigation labels and footer. GitHub URL, Python package, Streamlit title and internal technical names are unchanged.
- Palette: deep green `#005239`, warm yellow `#ffcc00`, paper `#faf9f3`, ink `#142d24`, supporting text `#506459`. Yellow is restricted to the supplied mark, a fine hero rule and text selection; it is not body text or a dominant surface.
- Header uses one complete logo image, not an image plus duplicated adjacent wordmark. Display width 200–270 CSS px on desktop and 215px on narrow screens, automatic height, preserved aspect ratio, intrinsic dimensions and meaningful alt text. Existing header stacks on mobile and navigation wraps.

## Logo preparation

Used the built-in image generation tool in background-extraction edit mode with the attached logo as the edit target. Prompt: remove only the white/off-white background and excess blank margins; preserve green italic “The Pick Sheet”, the ticket outline/cross/yellow squares and yellow underline; transparent background; no redesign, new text or distortion. The tool-produced derivative retains the original visual character but is not asserted pixel-identical to the attachment. Used sips to crop remaining transparent margins and downsample to 1100 × 253 px. Final alpha PNG: `homework9/assets/the-pick-sheet-logo.png`, 181,163 bytes. Original generated output is retained outside the project; no generated-image path is referenced by the page. Inspected the final asset directly; the full ticket, wordmark and underline remain visible. Tiny edge variations from the extraction should be checked in Chrome at actual display size.

## Content boundaries

The target is still 14 manual competition/team selections, historical-data outcome probabilities, a most-likely recommendation and a valid previous-meeting reconstruction alongside actual results in one table. All are explicitly planned. The currently available local synthetic prototype, fictional teams, rule-based picks and missing competition/probability/backtest UI remain clearly stated. Model selection/evaluation, data rights and no-guarantee limitations are preserved. No new functional or performance claims are introduced.

## Checks completed

Static HTML: five sections, one main heading, one header logo, unique IDs, valid fragment links and existing relative assets. Gallery, selected page, A and linked CSS/logo return HTTP 200 and match local files. `git diff --check` passes.

Calculated solid-color contrast on paper: body 13.92:1, supporting text 6.02:1, links/focus 8.79:1; white on green primary action 9.27:1; dark text on yellow selection 9.71:1. All exceed 4.5:1. This is source-level evidence, not rendered WCAG certification. Skip link, keyboard-focus styles, semantic headings, visible labels and scrollable setup commands are retained.

## Review still pending

Chrome native launch failed with “Sky Computer Use native pipe startup failed”; creating a Chrome tab failed with “The browser access host is unavailable”. No Safari or alternative engine was used. Rendered desktop/mobile spacing, reflow at 320/390/768/1280/1440 CSS px, 200%/400% zoom, keyboard traversal and logo appearance in the actual header remain unverified. The existing loopback server was retained for user review, not created for critique.

Impeccable context ran successfully for the A source and critique-storage resolved the final target slug `homework9-index-html`. Read critique and craft-floor references. The user subsequently authorized two independent agents. Assessment A completed before Assessment B findings were released to the parent. Source-based subtotal: 18/24 (not a rendered grade). Assessment B ran the detector once: 6 warnings (5 cramped-padding, 1 cream-palette), all line 0. Spacing is unconfirmed given explicit CSS padding; off-white is intentional. Two P2 copy recommendations remain: explain repository acquisition/terminal setup and disclose the retained Toto Estimator app title. No ignore file exists. Chrome failure still prevents rendered verification and overlays. The critique snapshot is stored through the official helper; no comparable earlier trend is claimed.


## Reviewer corrections — 2026-11-21

Both P2 recommendations from the independent review are resolved in the final page and mirrored variants: GitHub Code → Download ZIP, extraction, finding app.py/pyproject.toml, opening Terminal/PowerShell, changing directory with a quoted path, then per-OS installation/run commands. These now invoke the virtual environment Python directly without activation; Windows does not require changing PowerShell execution policy. The page explains that the existing local app opens as Toto Estimator under the new public-facing The Pick Sheet name and gives Ctrl+C shutdown guidance. README/package metadata and current UI labels ground these instructions. No dependency installation or fresh Windows execution was performed, so cross-platform execution is not claimed verified.

No CSS, logo, colors, typography, layout rules, application source or technical identifiers changed in this correction. Five sections and planned/current feature boundaries are preserved. Final page and A have identical visible text. Static structure/anchors/assets/corrected-copy checks and git diff --check passed. The final page and A/B/C returned HTTP 200 with exact current file content.

Chrome was attempted once for this correction; tab creation failed with “The browser access host is unavailable”. No repeated attempts or Safari fallback. Desktop/mobile screenshots, responsive rendering, zoom, actual focus behavior and visual spacing remain unverified. The earlier critique snapshot describes the pre-correction page; its copy findings are now resolved, while detector spacing warnings remain unconfirmed and the intentional off-white palette remains unchanged. No new visual score is claimed.

### Manual review in Google Chrome

1. Open http://127.0.0.1:8769/ and refresh with Cmd+Shift+R (macOS) or Ctrl+Shift+R (Windows/Linux).
2. At a desktop viewport around 1280 or 1440px wide, inspect the logo, editorial columns, all five sections and the expanded setup text. Use Tab to check visible keyboard focus and both navigation anchors and the demo link.
3. Open Chrome DevTools (Cmd+Option+I on macOS, Ctrl+Shift+I on Windows/Linux). Toggle the device toolbar (Cmd+Shift+M or Ctrl+Shift+M). Select Responsive and inspect at 320px and 390px wide, then 768px. Check that navigation wraps, logo keeps its proportions, columns stack, text stays readable and the page has no horizontal overflow. Only command blocks may scroll internally.
4. Test desktop zoom at 200% and 400%; check all content remains reachable and the setup paths/commands are readable. DevTools mobile simulation is not a physical-device test.
5. Review the two copy corrections and approve the finished page before publication. If the server has stopped, from hw9-promo run `python3 -B -m http.server 8769 --bind 127.0.0.1 --directory homework9`, keeping the terminal open. Do not launch a second server if port 8769 is already occupied.

### Remaining Homework 9 completion work

Complete and record actual Chrome desktop/mobile review and resolve any observed issue; obtain user approval of the finished page; then, only after authorization, commit the public-safe Homework 9 files, push the intended branch, configure/deploy GitHub Pages and verify the public page/assets. Add publication/verification evidence and final public URL to PROCESS.md and the required course submission. The exact course submission destination/rubric is not present in the inspected project, so it remains to be confirmed. This correction performed no commit, push or deployment.

## User approval and publishing entry — 2026-11-21

The user manually reviewed and approved the finished page, authorizing scoped commit/push and GitHub Pages publication. This supersedes earlier approval-pending statements. No claim is made that automated Chrome review succeeded. Publishing entry: homework9/index.html. The branch-only workflow .github/workflows/homework9-pages.yml assembles six files: index.html, assets/brand.css, assets/the-pick-sheet-logo.png, variants/assets/base.css, variants/assets/a.css and .nojekyll. Only this artifact is deployed at the repository Pages root; unrelated project files are excluded. Relative paths preserve the /toto/ project prefix. Publication verification is recorded in PROCESS.md after actual deployment.
