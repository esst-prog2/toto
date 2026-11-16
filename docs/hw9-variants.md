# Homework 9: three promotional-page variants

Prepared 2026-11-16 using the installed Impeccable `generate` workflow. **Selection pending:** all three candidates are separate; no final site, critique, publication or push is part of this step.

## Preview

From the `hw9-promo` worktree root:

```bash
python3 -m http.server 8769 --bind 127.0.0.1 --directory homework9
```

Open [the comparison gallery](http://127.0.0.1:8769/variants/). A server is already running there for this session; do not start a second one on the same port. The command above also lets a later session restart it.

The gallery presents all three options equally, with embedded previews and full-size links. “Side by side” and “Wide previews” change only the comparison layout. They do not accept a design. At narrow browser widths the gallery stacks the candidates. Choose by replying A, B or C in the conversation; no choice is stored by the page.

| Candidate | Full-size local preview | Primary design axis | Files |
|---|---|---|---|
| A — Match Programme | [Open A](http://127.0.0.1:8769/variants/a/) | Hierarchy: expansive heading, editorial scale, two-column method on desktop | `homework9/variants/a/index.html`, `assets/a.css` |
| B — Touchline | [Open B](http://127.0.0.1:8769/variants/b/) | Color strategy: green opening and close, centered introduction and focused reading column | `homework9/variants/b/index.html`, `assets/b.css` |
| C — Playbook | [Open C](http://127.0.0.1:8769/variants/c/) | Layout topology: desktop navigation rail, compact headings and a continuous reading column | `homework9/variants/c/index.html`, `assets/c.css` |

CSS paths in the table are relative to `homework9/variants/`. `assets/base.css` supplies the shared content, accessibility and responsive foundations. The gallery has its own `index.html` and `assets/comparison.css`.

These localhost URLs serve **promotional comparison pages**, not the Streamlit application. The only external destination in the candidate pages is the existing GitHub repository. No public application URL is asserted.

## Content and identity

Source authority: [content](hw9-page-content.md), [design brief](hw9-design-brief.md), and the actual package metadata and application. The approved five sections appear in order in every candidate, with identical visitor-facing text. Editorial notes are omitted from the website.

Impeccable identity lock: light `#F6F7F2` ground, `#132B24` ink and `#14563F` green; the brief’s system sans-serif stack; flat surfaces, fine rules, modest practical panels and sparse pitch geometry; factual, accessible English. All three vary expression within that identity rather than introducing unrelated brands. No remote font, stock image, JavaScript bundle, package install or build step is needed.

Every candidate includes a visible synthetic-data notice near its opening action and a closing explanation of unverified betting performance. The method explains points, goal difference, venue-specific ratings and the draw band without invented match records or probabilities. Local setup is selectable text with separate macOS/Linux and Windows PowerShell instructions. Windows explicitly uses `.\.venv\Scripts\Activate.ps1`; the installation and launch commands remain `python -m pip install .` and `streamlit run app.py`. A fresh Python installation on each operating system was not performed during this website step.

The pages use relative stylesheet paths and ordinary in-page anchors, so they can run under a GitHub Pages project subpath. No Pages configuration, workflow, root publishing entry or final variant promotion has been added.

## What Impeccable did

Codex loaded the installed skill and its `generate`, live-variant and craft-floor references, ran the project-local context helper, and used the native `live-generate` browser workflow with three candidates and the approved brief as its prompt. A real browser connected and minted the session. Codex delivered all three complete page replacements atomically using the helper’s scaffold and scoped preview controls; the helper acknowledged delivery and reported three arrived candidates.

The stable standalone HTML/CSS candidates and gallery are the review artifacts. Native preview controls and runtime markers are not part of those files. The temporary live helper was stopped without accepting a keeper; its temporary source/config were removed, and its runtime state stays under ignored `.hw9-tools/`. This adapts the helper’s usual immediate accept-and-bake flow to the user’s explicit request to commit three separate candidates and choose later. No final design approval is claimed.

Browser automation initially failed, then recovered through native Safari control. Safari’s accessibility tree confirmed the gallery, both preview-layout controls, all three loaded candidate documents, their content and setup commands. The browser is left on the equal side-by-side comparison view. No screenshot review or `critique` was run before selection.

## Checks and remaining review

- Static checks cover valid nesting, exactly five ordered sections within one main landmark, a single main heading per candidate, unique IDs, anchor/ARIA targets, local assets, no injected live markers or scripts, identical candidate text, and the required commands/limitations.
- HTTP checks cover the comparison page, all three candidates and their linked stylesheets. Only the `homework9` directory is served, bound to loopback; private datasets are outside the served directory.
- Accessibility is built in: labelled navigation, skip links, visible keyboard focus (including the inverse green-opening button), semantic headings and outcome labels, selectable scrollable command blocks, and no required motion. Proposed solid text-color pairs meet the brief’s calculated contrast targets. This is not a WCAG conformance certification.
- Impeccable’s mechanical detector was run once, separately from critique. It returned `cramped-padding` warnings on section/list/outcome dividers. The styles declare logical `padding-block` spacing, including 4rem section padding and 1.5rem list padding; the detector result is retained as an unresolved review item rather than called a clean pass. Check rendered spacing on the selected variant during the later authorized critique step. No suppression or automated setup repair was added.
- Full visual inspection across viewport sizes, zoom, assistive technology and browser engines remains for review of the selected design. No prediction tests or model evaluation were performed; the existing Python/Streamlit application, source content, README and historical data were not changed.
