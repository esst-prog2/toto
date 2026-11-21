# TOTOdology promotional website: design brief

## Selected direction — 2026-11-21 (current)

The user selected A — Match Programme and the public name The Pick Sheet with the supplied green/yellow logo. The local implementation is at `homework9/index.html`; see [selected design and checks](hw9-final-design.md). This supersedes earlier selection-pending and TOTOdology identity instructions below, which remain historical context. Chrome-only visual review and final implementation approval are still pending. No commit, push or deployment is authorized.

Prepared with the installed Impeccable `shape` workflow on 2026-11-16.

**Status:** Brief prepared for review. The user approved the content structure and selected the modern, professional, football-inspired direction. Specific visual treatments below are design recommendations for the later design step, not a claim that a rendered website has been approved.

## Content revision — 2026-11-21 (current authority)

The user's updated brief supersedes the prototype-only positioning below. Keep the five-section sequence and all three visual designs. Introduction and audience explain the planned product; the three method steps describe manual competition/team entry, historical-data probabilities and the previous meeting. Label this workflow planned, and explain the present synthetic prototype separately beside its setup instructions. Never present the old rating rules as the chosen future statistical model. Keep the opening development notice and the closing model/evaluation/data-rights limitations readable. Browser previews and reviews must use Google Chrome exclusively. The updated `hw9-page-content.md` is the current copy authority; older prose below records the original design context. No invented probability numbers, results, new features or final variant selection.

**Source:** [Approved content structure and draft copy](hw9-page-content.md). Preserve its five sections and factual boundaries; its editorial notes are working evidence, not page content.

## 1. Job, audience and outcome

**Surface mode: Persuade.** Help a first-time visitor understand TOTOdology and decide whether to explore its code or try the local demo. The audience is football fans curious about Toto-style tickets and learners interested in transparent football statistics. Visitors may understand football while being unfamiliar with Python setup.

The page should answer, in order: what this is, who it helps, how a pick is produced, how to try it, and what the current demo can establish. Success means a reader can explain 1/X/2, recognize that the demo uses synthetic history, and locate the local launch instructions. This is a comprehension goal, not a measured conversion claim.

**Primary action:** “Try the local demo” jumps to the setup section. **Secondary action:** “Explore the code” opens the real repository at https://github.com/esst-prog2/toto. Neither action implies a hosted application.

## 2. Visual direction and focal moment

Use the quiet precision of a modern football match programme: strong sans-serif headings, orderly numbered sections, generous space and restrained green accents. Give the page a recognizable football vocabulary through small 1/X/2 labels, fine touchline-like rules and an occasional cropped centre-circle outline. Keep those marks decorative, sparse and clear of text.

The opening leads with the TOTOdology wordmark, the existing “Football predictions you can follow” headline, a short purpose statement, the two actions and the synthetic-demo notice. Keep this notice in the main reading flow near the actions, with normal readable text. The next section should become visible naturally as the visitor scrolls; no fixed-height opening should hide content on short screens.

The focal moment is the method section: a numbered path from team performance, through home/away ratings, to the three fully labelled outcomes. Show the reasoning sequence as typography and simple rules. The 1/X/2 notation is explanatory; it must not look like an interactive predictor or a live score feed. Do not supply invented ratings, teams, fixture results, probabilities or confidence percentages as visual proof.

Use a coherent reading page with changes in density: a spacious opening, compact audience passage, structured method, practical setup panel and a short closing limitation statement. Reserve panels for practical instructions rather than enclosing every paragraph in an identical card.

## 3. Approved section sequence

| Section | Hierarchy and treatment | What the visitor learns or does |
|---|---|---|
| Introduction | Wordmark, one main heading, concise explanation, primary and secondary actions; small decorative pitch reference | Understands the 13+1 demo and sees the synthetic-data limitation immediately |
| Who it’s for | Short prose with a strong section heading and generous reading width | Recognizes the football-fan or learning use case; sees that sample teams can be selected |
| How predictions work | Three numbered steps, followed by a clearly labelled 1 / X / 2 explanation; actual UI labels appear in text | Follows points and goal difference, venue-aware ratings and the draw band; knows about rating details |
| Try it yourself | Practical instruction panel with Python prerequisite, platform-labelled commands, local launch explanation and repository link | Understands the local setup requirement and can follow the documented commands |
| What to expect | Brief closing statement and clear repository link; keep the limitation visible | Leaves with an honest view of the fixed synthetic demo and its unverified predictive performance |

A compact header can link to “How it works,” “Try it” and GitHub. Do not add sections for pricing, testimonials, performance metrics, supported-league claims or an online demo. Preserve the approved prose; the content draft remains the copy source.

## 4. Typography, color and material

**Typography:** Start with a high-quality system sans-serif stack. Use a confident bold heading weight, clear size changes and normal sentence case. Set body copy around 18 px on spacious screens and never below 16 px on narrow screens, with approximately 1.5–1.65 line height and a 60–70 character reading measure. Keep display headings concise, fluid and able to wrap. Use monospace only for the actual commands, not for explanatory body copy. Any later custom typeface needs a specific benefit, verified licensing and a dependable fallback; no font download is required for this brief.

**Color strategy:** Light neutral ground, deep green text accents and a solid green primary action. Use color for clear roles, with restrained football references rather than a full pitch background.

| Proposed role | Color | Intended use |
|---|---|---|
| Page ground | `#F6F7F2` | Soft light background |
| Primary ink | `#132B24` | Headings and main text |
| Secondary ink | `#52645B` | Supporting text and limitation explanations |
| Action/link green | `#14563F` | Primary button, links and meaningful emphasis |
| Panel white | `#FFFFFF` | Setup panel and inverse button text |

Calculated solid-color contrast is 13.94:1 for primary ink on the page ground, 5.85:1 for secondary ink on that ground, 8.02:1 for green links on that ground, and 8.63:1 for white text on the green action. These combinations exceed the 4.5:1 normal-text target. These calculations are planning evidence, not an audit of a rendered page; later changes, opacity, hover states and focus indicators must be checked again.

Prefer flat surfaces, simple dividers and modest corner rounding. Decorative pitch lines may be faint because they carry no information; never use faint decoration as a control boundary or the sole way to convey meaning. No stadium photography, club crests or external imagery is needed. Any later screenshot must come from the actual synthetic demo, retain an adjacent label and avoid private records.

## 5. Layout, interaction and responsive behavior

- Use one clear content flow and a bounded reading width, with space for small section numbers in the desktop margin. Keep the approved section order in the reading and keyboard sequence at every size.
- On mobile, use a single column. Let navigation wrap without requiring a hidden menu. Stack actions when necessary and keep them comfortable to tap. Scale pitch decoration down or remove it before it competes with the copy.
- Keep the method steps vertically understandable even if extra desktop width permits a more expansive arrangement. Labels must explain 1, X and 2 in words; neither color nor position alone carries the meaning.
- Keep macOS/Linux and Windows setup guidance labelled and available without tabs or accordions. Show commands as selectable text, not images. A long command may scroll within its own labelled block; the page itself must not overflow horizontally.
- Use ordinary links and in-page anchors with a visible focus state. Prefer a non-sticky header so content and anchor destinations remain unobstructed. Avoid a copy button, carousel or new interactive demo unless separately authorized.
- Keep all content visible by default. No essential animation, parallax, autoplay, scroll hijacking or entrance sequence. Respect reduced-motion preferences if optional motion is introduced later.

## 6. States, content ranges and accessibility

This is one English page with roughly 450–500 words of approved visitor-facing copy, five sections, three method steps and a short setup command block plus Windows guidance. Support heading wrapping and longer translated browser UI without relying on fixed heights. It has no account, form, prediction input, live data or server-loading state to design.

Plan default, hover, keyboard-focus and visited-link states; a clicked primary action lands at the setup heading. External-link behavior must be predictable, and any new-tab behavior must be disclosed. If a decorative asset or optional font fails, the text, links and setup instructions remain usable. The existing application's validation messages remain part of the local app, not a new promotional-page workflow.

Target WCAG 2.2 AA in the eventual implementation: semantic landmarks, one main heading, sequential section headings, a skip link, visible keyboard focus, descriptive links, text alternatives for meaningful images and decorative marks ignored by assistive technology. Aim for 44-by-44 px action targets, readable 200% text zoom and reflow at a 320 CSS-pixel viewport. Verify text at 400% browser zoom on a suitable desktop viewport. Do not place text on a pitch outline or rely on green alone to distinguish links; underline inline links.

Future checks should cover 320/390 px mobile, approximately 768 px tablet and 1280/1440 px desktop, keyboard navigation, reduced motion and the actual command blocks. No rendered responsiveness or accessibility result is claimed at this stage.

## 7. Scope, open choices and handoff

**Current deliverable:** this Markdown design brief, a supporting product-context record and the required process/planning entries. The installed Impeccable engine loaded context; its `shape` playbook organized job, evidence, direction, sequence, states, layout and constraints. The approved content and explicit user direction supplied the settled discovery inputs. No fresh interview answers, visual-choice approval or implementation contract are invented.

**Untouched:** existing app, prediction rules, datasets, acquisition code, README, Homework 8 specifications and the approved content file. Do not publish private data or promise integration, betting accuracy, probabilities or backtesting. The existing app title “Toto Estimator” may be mentioned when useful for recognition; the promotional name remains TOTOdology.

**Deferred:** final typography and spacing, any optional imagery, the implementation stack, and the visual variants to consider during the separately authorized Impeccable `generate` step. Proposed colors and composition can be refined then while preserving the user's direction. No PRODUCT build-path default or DESIGN.md direction contract is set. The eventual public page must support GitHub Pages and relative asset paths; no public URL or deployment behavior is invented here.

**Stop point:** review this brief, then authorize the next design step. No HTML/CSS, mockup generation, `generate`, `critique`, publishing or pushing was performed. This document is the design handoff, not a completed site.
