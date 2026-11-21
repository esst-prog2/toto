# Homework 10 — technical setup and scope evidence

Prepared 2026-11-21 in hw9-promo. No commit, push, deployment, final promotional video or webpage modification.

## Official instructions and versions

Sources checked: https://github.com/heygen-com/hyperframes , https://hyperframes.heygen.com/quickstart and bundled 0.9.77 HyperFrames/CLI skills. Official CLI path is init → check/preview → render; requirements Node >=22 and FFmpeg. The npm registry and official version-aware skill launcher both reported 0.9.77.

- Node v26.10.0 (existing), npm 11.19.1 (existing). No Node/npm upgrade.
- HyperFrames 0.9.77 installed from official npm release to .hw9-tools/hw10/runtime with package-lock and cache local to the existing ignored tools tree. Version-aware bundled launcher used with --cli-version 0.9.77 for init/check/render/snapshot. No global HyperFrames install, no core-agent skill overwrite. Bundled skills are read directly; init used --skip-skills.
- FFmpeg and FFprobe 9.0.2 newly installed via existing Homebrew. Formula ffmpeg 9.0.2_1 also installed dav1d 1.5.4, mpg123 1.33.7, lame 4.0, libvmaf 3.2.1, libvpx 1.17.0, opus 1.6.1, sdl3 3.4.20, sdl2-compat 2.32.74, svt-av1 4.3.0, x264 r3222, x265 4.3. Auto-update and cleanup were disabled for the installation. These are host dependencies, not asserted project-local.
- System Google Chrome: 157.0.8103.80. HyperFrames subsequently provisioned/selected Chrome Headless Shell 158.0.8127.36 under ~/.cache/hyperframes/chrome/ for rendering. Headless checks and snapshots succeeded; no Safari or other browser engine used. No interactive Chrome visual pass is claimed.

## Technical test

Official init scaffold: .hw9-tools/hw10/render-smoke (ignored). Replaced only its generic test composition with a two-second 640×360 green test card and a moving yellow bar, using locally saved GSAP 3.15.0. This is an infrastructure test, not a promo scene, storyboard, brand decision or final video. It contains no application screens/results or product-function claims.

Final check: ok true, browserSkipped false; lint/runtime/layout/contrast/craft each zero errors and zero warnings. Audio_none info is intentional. Final report .hw9-tools/hw10/check-final.json, with the CLI's own saved report under the test project's .hyperframes/artifacts/checks/.

Render: --fps 30 --workers 1 --low-memory-mode --quality draft --no-best-effort. Output .hw9-tools/hw10/render-test.mp4, 9,247 bytes. ffprobe confirmed H.264, 640×360, 30/1 fps, 60 frames, exactly 2.000000 seconds. Full FFmpeg decode-to-null completed without errors. Decoded frames at 0.2 and 1.6 seconds were visually inspected and show the yellow bar moving. HyperFrames snapshot captured the same two times through Chrome; contact sheet inspected. Probe JSON, decoded PNGs and snapshots remain in the ignored setup folder.

## Warnings, corrected issues and side effects

- Initial doctor detected only ~1.4GB available on an 8GB Mac. Single-worker low-memory rendering succeeded; this does not guarantee 1080p/30s performance.
- First check found a nested_structure_needs_subcomposition warning for the generic bar wrapper. Flattened the test-only markup; the repeated final check had zero warnings/errors.
- npm warned that esbuild's install script lacked an allowScripts entry. No extra script approval was performed; CLI/check/render succeeded. No install failure is claimed.
- A non-escalated early browser query could not persist telemetry settings in ~/.hyperframes (EPERM). Later test calls used HYPERFRAMES_NO_TELEMETRY=1 and appropriate execution permissions; the render succeeded. An attempted sandboxed doctor report write was also blocked; the report was then saved successfully with authorized permissions. These were execution-sandbox restrictions, not unresolved rendering failures.
- HyperFrames cached a Chrome Headless Shell and Inter font resources outside the repo under ~/.cache/hyperframes, plus normal tool runtime state; no claim of fully hermetic installation.
- Doctor lists missing optional transcription/TTS/music-generation tools and Docker. None is required for this silent local test. FFmpeg doctor notes loudness comparisons assume 8.0.1; no loudness comparison was attempted with 9.0.2.
- No blocking setup failure remains. Future genuine app-screen capture/1080p production is not yet tested. No accounts, cloud/paid services, voice models or publishing were used.

## Scope and preservation

Reviewed README, published approved HTML, planning decisions, Homework 8 design/spec/tasks, app.py and service.py. Current synthetic-team picks/rating details are implemented; competition selection, three probabilities and valid previous-meeting reconstruction are planned. The published HTML was fetched (HTTP 200) and matched the approved local bytes. Protected file SHA-256 baseline is saved at .hw9-tools/hw10/protected-files.json and rechecked unchanged after setup. All published HTML/CSS/logo and app/service bytes were preserved. Concepts are saved separately in homework10/STORYLINES.md; none selected. The other worktree is untouched.

Reproduction uses the bundled official launcher with HYPERFRAMES_NO_TELEMETRY=1 and project-local NPM_CONFIG_CACHE. Do not run unpinned updates, global installers or site publishing during this concept-selection stage. No final video or embed should be created until the user selects a storyline.

## Final video approval and embedding authorization — 2026-11-21

The user approved the final render and authorized embedding, commit/push and GitHub Pages deployment. Earlier approval-pending text is retained as historical context. See docs/hw10-publication.md (relative to worktree root) and PROCESS.md for actual embedding/public checks. Approved video bytes remain unchanged.
