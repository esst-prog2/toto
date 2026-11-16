# Homework 9 environment preparation

Prepared 2026-11-16. Branch/worktree: `hw9-promo`, sibling of the original `toto`
worktree. Base: `95f0a728d965cc1e02458c7754e64436db6e8fcc`.
The original `feature/data-collection` worktree retains all unfinished Serie B
changes and both existing untracked `.DS_Store` files. No stash/reset/cleanup was used.

## Official sources inspected

- [OpenAI project skills](https://developers.openai.com/codex/skills): repository skills under `.agents/skills`; reload/open the new worktree to discover newly installed skills.
- [gstack README](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/README.md), [host guidance](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/docs/hosts.md) and inspected `setup`: official Codex support is experimental, not the full Claude Code tier. Its supported repository-local layout is `.agents/skills/gstack`; use `--host codex` explicitly.
- [Impeccable installation/commands](https://impeccable.style/docs/), [official source](https://github.com/pbakaus/impeccable/tree/d41d9860b0094dcb68030657da63461212835aaa) and inspected `cli/bin/cli.js`: explicit project/provider/no-hook installation, checksum-verified native engine and signature-verified skill bundle.
- [Bun installation/direct downloads](https://bun.sh/docs/installation): official single-binary distribution; downloaded the pinned macOS ARM64 release and verified its GitHub release SHA-256 before execution. No curl-to-shell Bun installer or shell-profile edits.

## Installed locally

| Component | Version/revision | Location |
|---|---|---|
| Bun | 1.4.2, revision 744846f84 | `.hw9-tools/bin/bun` |
| gstack | 1.99.5.0, commit `5dcd76b4eae6bb06f73460d3ab29cef8e33e8537` | `.agents/skills/gstack` plus generated `gstack-*` skill links |
| Impeccable installer source | npm package version 4.9.2, source commit `d41d9860b0094dcb68030657da63461212835aaa` | inspected official source; installed bundle below |
| Impeccable skill bundle | metadata 4.9.1 | `.agents/skills/impeccable` |
| Impeccable engine | 0.1.24, darwin-arm64 | `.hw9-tools/impeccable/bin/0.1.24/impeccable` |

These version numbers intentionally differ: installer, delivered skill bundle and
native engine have independent versioning. Installed fingerprints are in
`docs/hw9-tool-installation.json`. Third-party checkouts, generated absolute links,
binaries, dependency trees, logs and state are ignored, not vendored into this repo.
A fresh clone must repeat the documented local installation before using the tools.

The reviewed Impeccable launcher was run from its pinned official source with
`IMPECCABLE_HOME` set to the new worktree's `.hw9-tools/impeccable` and:

```sh
node /path/to/pinned/impeccable/cli/bin/cli.js install --providers=codex --scope=project --no-hooks --yes
```

The launcher verified the engine against its shipped checksums; the native installer
verified the remote skill bundle signature before extraction. Bundle is a separately
signed upstream release, not asserted byte-identical to the installer-source commit.

The pinned gstack source was cloned into `.agents/skills/gstack` and its reviewed
installer was invoked with local PATH, `GSTACK_STATE_ROOT` and
`BUN_INSTALL_CACHE_DIR`:

```sh
.agents/skills/gstack/setup --host codex --no-browser --no-harness-auto --no-team
```

**Unexpected optional dependency:** gstack installed Homebrew `coreutils` 9.12_1
(`/opt/homebrew/bin/gtimeout`) for Codex timeout protection. This was not anticipated
in the initial installation explanation; it is a host package side effect, not a
project-local component. It has not been silently removed. Future setup must set
`GSTACK_SKIP_COREUTILS=1` as the project wrapper does. No global Codex configuration
or shell profile was edited; the Codex model profile was read from existing config.
No Claude directory was created. Do not rerun setup/upgrade indiscriminately: this
upstream's status command warns that re-registering an in-place runtime checkout
can require moving it first; follow its official repair guidance if needed.

## Using the tools in Codex

Open this new worktree as the Codex project and reload skill discovery. A fresh
turn/session should discover the installed skills; automatic UI discovery has not
yet been demonstrated in the currently running original-worktree session.

- Content step: explicitly ask for **gstack-office-hours**, the Codex invocation of
  gstack `/office-hours`. Use builder mode for the homework promotional-site brief.
- Design steps: **`$impeccable shape`**, **`$impeccable generate`**, then
  **`$impeccable critique`**. These are agent skill workflows, not terminal commands.
  `shape` plans before implementation; `generate` compares named-element variants;
  `critique` evaluates the rendered design. `init` may first collect product context.
- Launch terminal helpers via `scripts/hw9-tool` to keep state/cache in this worktree.
  For example `scripts/hw9-tool impeccable engine-probe` and
  `scripts/hw9-tool gstack setup --status`. Do not run office-hours/content now.
- User scope overrides tool defaults: no application/model/data edits, no automatic
  shipping/merging/pushing, and no replacing user choices with invented decisions.

## Verified and pending

Verified: gstack setup completed with Codex/project scope; status reports current
installation and all 75 router-section links resolve. Impeccable engine handshake
returns `impeccable-engine 0.1.24`; its installed references include shape, generate
and critique. Bun reports 1.4.2. Wrapper syntax and original-worktree preservation
are checked. No application tests were needed for this environment/documentation
step; no application code changed.

Pending: actual office-hours and design workflow runs; browser-based visual
validation and any image-generation/account prerequisites needed by the chosen
design workflow. gstack Chromium was deliberately skipped; its browser-dependent
skills are not ready until Chromium is installed. Docker/qualified CSO runtime
images are unavailable and irrelevant to this preparation. No global standalone
`gstack` or `impeccable` command is claimed. gstack's Codex integration remains
experimental. GitHub Pages permissions/authentication and deployment remain for a
later authorized step; nothing was pushed.

Next step: run gstack office-hours for the English promotional-site content,
collect the user's audience/value/action decisions, then record that completed step
in PROCESS.md and commit its scoped artifacts.
