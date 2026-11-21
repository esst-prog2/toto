# Homework 10 — approved concept-video embedding and publication

## Approved scope (2026-11-21)

The user approved the final 30-second The Last Box video and authorized responsive embedding, checks, scoped commit/push and GitHub Pages deployment on hw9-promo. No modification of data-collection or unrelated application files is authorized. This approval supersedes earlier production documents' approval-pending statements.

## Website changes

The native HTML video player lives inside the existing introduction at #concept-film; all five sections, prior copy, branding and logo remain. Controls, muted, playsinline and preload=metadata are set, with no autoplay. An extracted opening-frame JPEG poster reserves a useful first frame; intrinsic 1920×1080 plus fluid width/auto height/16:9 CSS prevents stretching. The figcaption explicitly identifies concept/in-development/no-real-data and silence; fallback offers the MP4 directly. The content conveys the same planned experience described in adjacent text. No JavaScript player or external video service was introduced.

Site media: homework9/assets/the-pick-sheet-the-last-box-concept.mp4 and the-pick-sheet-concept-poster.jpg. MP4 SHA-256 8c57298d61efcc4c5aa556837d6a813f53ba7ee91900fcb059408be1493aeb43, exactly the approved render, 1,809,970 bytes, 30.000s, H.264 High/yuv420p, 1920×1080, 30fps/900 frames, no audio. Faststart moov precedes mdat. Rechecked encoded beginning/middle/end review sheet; representative images retain concept disclosure, clear estimate labels and undistorted actual logo.

The existing Pages workflow publishes an explicit site bundle only: index.html, three CSS files, logo, video and poster, plus .nojekyll. Video production sources, local review server, runtime/caches and datasets are excluded from the website artifact. The generated .hyperframes directories are ignored; editable HyperFrames source, storyboard, production review and the approved render are retained in Git for assignment evidence. No tools/node_modules/private datasets are staged.

## Local verification

Static comparison removing just the new figure reproduced the previous approved HTML exactly. HTML structure, unique IDs, fragment targets, all relative assets, declared video MIME and correct approved video hash passed. git diff --check passed.

Chrome Headless Shell via HyperFrames rendered exact artifact copies in 1440px and 390px iframe viewports. JavaScript QA inside a separate ignored fixture asserted controls/muted/playsinline, 30s duration, no horizontal overflow and 16:9 aspect ratio, then called video.play() and waited for media time to advance beyond 0.25s before capturing. Desktop capture reports PASS, video 1160×652.5px, document width1440px and playback advanced to ~0.397s with readyState4. Mobile capture reports PASS at viewport390px; video CSS width350px and approximately196.875px high, with document width390px. Actual advancing playback, not only poster loading, is the readiness gate. The initial test fixture had a frame-load listener race; it was corrected with an already-loaded-document path and a buildReady promise before treating results as passing.

Chrome screenshots were inspected: responsive player/caption and adjacent approved sections fit both widths. Small video details remain best viewed fullscreen. Native player controls can temporarily overlay the burned-in lower disclosure, while the separate figcaption also discloses concept status. This is normal native-control behavior, not a change to the approved film.

Interactive foreground Chrome CUA failed once with browser access host unavailable; no repeated attempt or Safari fallback. The headless Chrome playback/viewport checks above succeeded. No physical mobile-device or other-browser testing is claimed.

## Public deployment

Pending until the pushed deployment and live page/video are actually verified. Results will be appended after deployment; a successful push is not publication evidence.
