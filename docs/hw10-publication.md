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


## Public publication and playback verified — 2026-11-21

- Website: https://esst-prog2.github.io/toto/ (video anchor #concept-film).
- Direct video: https://esst-prog2.github.io/toto/assets/the-pick-sheet-the-last-box-concept.mp4 .
- Main Homework 10 commit c5a57e4a4e4a5ebf8add9f788db2222a03e5fb33 was pushed to origin/hw9-promo. GitHub Pages run https://github.com/esst-prog2/toto/actions/runs/44936977293 completed successfully for that source.
- Independent public requests verified HTTP200 and exact current-source bytes for the HTML, all three stylesheets, logo, poster and approved MP4. MP4 Content-Type video/mp4, 1,809,970 bytes and approved SHA-256 match. A public bytes=1000-1999 request returned206 with exact expected bytes. In-page link targets resolve; all navigation/other existing content remains intact.
- Chrome Headless Shell tested fetched exact live HTML via QA srcdoc frames, with the deployed public URL as the base, so CSS/logo/poster/MP4 were loaded from actual public asset URLs. Desktop viewport1440: video1160×652.5, page width1440, duration30, media clock advanced to0.3977s, readyState4. Mobile viewport390: video350×196.875, page width390, duration30, media clock advanced to0.4049s, readyState4. These are real muted video.play() media-clock advances, not poster-only checks. Both screenshot/metric results were inspected. No horizontal overflow; 16:9 preserved.
- Separate Chrome video-element snapshots loaded/sought the actual public MP4 at0,15,29.8s; inspected beginning/middle/end contact sheet confirms the correct approved film, including concept disclosure and ending logo/address. Screenshot evidence and method/HTTP results are saved in homework10/evidence/.
- Interactive CUA Chrome host was unavailable, so no foreground manual session or physical-phone test is claimed. The user's prior manual approval and these automated headless-public-asset checks are distinct evidence.
- Publication record/source-whitespace follow-up does not alter approved site/media or trigger a redeploy; deployed page bytes remain those verified above. Vendored GSAP changes remove only comment trailing whitespace/EOF blank line; source-generator normalization preserves this on rebuild. Final diff whitespace check passes.
- No data-collection working files, application/model/data, repository/package names or unrelated project files were modified. No merge or branch deletion. Existing untracked homework9/.DS_Store remains untouched and excluded. Generated HyperFrames state and tools/private data were excluded from commits.
- Remaining: submit the public page URL in the required course channel, with repository/branch/PROCESS.md/video evidence if the rubric requests it. Exact portal/deadline requirements are not present in the project; no course submission is claimed.
