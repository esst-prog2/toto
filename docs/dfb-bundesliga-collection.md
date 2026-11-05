# Official DFB Bundesliga collection pipeline

Status reviewed 2026-11-05. DFB Datencenter is the preferred and exclusive source for this pipeline, superseding the provisional CSV-source recommendation. No DataHub, Football-Data or OpenFootball acquisition is used here. No archive-wide network collection has been initiated.

## Implemented components

- `src/toto_estimator/dfb_html.py`: the existing scoped HTML parser now also returns row observations, source match IDs, source team slugs, original displayed names, raw date/score/status evidence and row errors. The existing seven-column candidate records remain compatible. Recognized `[awarded]` / `[gewertet]` numeric score annotations retain their evidence; unsupported formats remain uncertain.
- `src/toto_estimator/dfb_collection.py`: actual season-selector slug discovery, expected regular-season inventory, local export ingestion, response-bound status reviews, source-ID/fixture reconciliation, full-season validation and coverage generation. Accepted records reuse `validate_historical_data` for fields, dates, teams and goals. No predictor, training or evaluation code is called.
- `src/toto_estimator/dfb_transport.py`: permission-gated single-process transport, content-addressed original responses, SHA-256 verification, immutable page provenance, cache reuse, detailed append-only event logging, pacing and bounded retries. Writes publish complete artifacts atomically. Changed cached versions are retained as conflicts and stop the run; none wins silently.
- `scripts/collect_dfb.py`: offline-by-default CLI. All CLI inputs/outputs must resolve under Git-ignored `data/private/germany/`. Completed-history and ongoing records are always separate. Content-addressed run directories retain reports, accepted CSVs and checksums without overwriting previous runs.
- `tests/test_dfb_collection.py`: synthetic complete 18-/20-team schedules and safety/edge-case tests. Original parser regressions remain in `tests/test_dfb_html.py`.

The inventory covers 36 completed target seasons (1990/91–2025/26) plus separate 2026/27. Normal expectations are 18 clubs, 34 matchdays and 306 matches. **1991/92 uses 20 clubs, 38 matchdays and 380 matches.** Completed-history capacity is 11,090 matches across 1,228 matchdays; ongoing adds 34 planned matchdays. Actual advertised season slugs are used, including abbreviated end years; unadvertised seasons are reported, not guessed. Each acquired page's selected round inventory must match the season format. Relegation playoffs, cups and lower divisions are outside scope.

## Finality, postponements and administrative decisions

The real cached matchday HTML has numeric scores but no certified final-status field. The pipeline therefore does **not** infer finality from a numeric score, a historical date or the presence of a Liveticker link. Every observed fixture is retained with its source ID, page hash, raw evidence and parse diagnostics, including rows with missing dates/teams/scores.

Dedicated status text/attributes, score/date descriptions and row-class hints for live, scheduled, postponed, cancelled or abandoned states veto acceptance. These are conservative recognizers tested synthetically, not claims that all such real DFB layouts have been observed. Positive finality requires a reviewed source/export record tied to the exact HTML response checksum and match ID. When hints contradict review evidence, the fixture stays uncertain. Unknown fields/layouts never produce invented zero scores. Approved real status exports or documented DFB status semantics remain an external evidence requirement.

A status-review JSON has a `reviews` array. Each item needs:

```json
{
  "page_sha256": "<exact 64-character response SHA-256>",
  "source_id": "match_<DFB numeric ID>",
  "status": "finished",
  "reviewer": "<responsible operator>",
  "evidence_reference": "<approved DFB export row or independently reviewed official evidence>"
}
```

Supported states are `finished`, `awarded`, `scheduled`, `postponed`, `live`, `abandoned`, `cancelled`, `unknown`. This is an evidence interface, not a generated approval. Do not label old samples finished merely to increase accepted counts. Changed page bytes invalidate old reviews; duplicate/conflicting reviews are rejected and unused reviews are reported.

An `awarded` review additionally requires `outcome_policy`, `confirmed_home_goals` and `confirmed_away_goals`. Those confirmed goals must equal the displayed numeric result; otherwise the match is quarantined. The collector never substitutes a different administrative/on-field score. Administrative hints without explicit reviewed evidence remain uncertain. Keep the official ruling/export reference and its outcome interpretation with the record; a production decision on how the future model should use awarded matches is outside this work.

Rescheduled fixtures keep their displayed actual date and original matchday. Date sorting is not inferred from round order. Duplicate source IDs and duplicate ordered team identities across rounds are detected independently of dates. Changed dates, scores, opponents or round assignments are reported as conflicts and all colliding candidates are quarantined. No automatic “latest wins” or date correction is applied. Missing source team identities and ambiguous aliases prevent full-season acceptance. Source spellings are preserved even where one source team slug has multiple display labels.

## Season validation and reports

A completed season is `COMPLETE` only when all expected pages pass metadata/layout checks, all expected results have valid final/awarded evidence, the club count matches, every ordered home-away pairing occurs exactly once, each club has 17/19 home and away matches, each nominal round contains each team once, and no unresolved errors/conflicts remain. Accepted rows pass the existing historical validator. Ongoing data is never marked as completed history.

Each run contains:

- `inventory.json`: the selected season and expected matchday URLs, or all 37 target seasons when `--season` is omitted.
- `validation.json`: source provenance, code/input checksums, counts, date ranges, club label/identity maps, per-club balance, every missing matchday, every inferred missing fixture, all uncertain and accepted match observations, administrative issues and duplicate/conflict references.
- `coverage.md`: a season-by-season summary, with missing/uncertain details in JSON.
- `completed_history.csv` and `ongoing.csv`: accepted seven-column extraction records only. These are not model-integrated or standardized datasets. Empty files retain their headers.
- `completed_history_candidates.csv` and `ongoing_candidates.csv`: parsed score candidates, including results that still lack finality evidence. These must not be treated as verified official finals.
- `matchday_inventory.csv`: every expected matchday in scope, canonical URL, `CACHED` / `INVALID_CACHED` / `MISSING` state and available source checksum. `CACHED` describes local availability, not finality or season completeness.
- `checksums.json`: SHA-256 fingerprints of the run artifacts.

If the full club roster cannot be established, the report explicitly counts unseen fixture slots and says identities are unknown. It cannot name nonexistent, unacquired fixtures without evidence. Missing fixture pairs are enumerated only from a complete verified source roster; uncertain observed fixtures remain individually identified even with parse errors.

## Offline saved pages and approved exports

The implemented pipeline was exercised using the six existing legitimately obtained bounded samples only. `data/private/germany/collection/available_samples.json` records their original provenance and expressly labels them **bounded samples, not archive permission or an approved full export**.

```sh
PYTHONPATH=src .venv/bin/python -m scripts.collect_dfb \
  --season 1990/91 \
  --seed data/private/germany/bundesliga_1990_1991_md1.html \
  --exports data/private/germany/collection/available_samples.json
```

`--season` accepts `1990/91`, `1990/1991`, `1990-91` or `1990-1991` through the existing season canonicalizer. Single-year, nonconsecutive and out-of-target seasons are rejected. Omitting the option preserves the all-season workflow. The selection restricts export ingestion, cached-page reporting and network requests. A mixed-season export manifest is allowed: out-of-scope URLs are reported under `export_import.skipped_out_of_scope` and their files are not opened or imported. Unadvertised selected seasons remain visibly missing; URL slugs are not guessed.

The command above uses only existing samples and makes no network requests. It currently reports one of 34 matchdays, nine numeric candidates and zero evidence-accepted finals for 1990/91. The target stays 18 clubs, 34 matchdays and 306 regular-season matches.

Repeated execution verifies and reuses cached originals without requests. Identical inputs/code produce identical content-addressed validation artifacts. Event timestamps are audit logging and are outside the deterministic report. Source inputs and earlier experiment artifacts are not overwritten.

For approved HTML exports, supply a manifest with `pages` entries containing `path` (relative to the manifest), `url` (the exact canonical DFB matchday URL), `sha256`, `retrieved_at`, `access_basis` and `evidence_reference`. Referenced HTML must stay within the private Germany/export boundary. Preserve the original export/grant as evidence. Pass `--reviews` for response-bound status evidence supplied by/reviewed against that export. Full German pages with the observed canonical/filter/result layout are supported; arbitrary CSV/XML, Turbo fragments and unknown HTML layouts are not silently adapted.

For a future **approved** local 1990/91 HTML export and its reviewed status evidence, the exact command is below. The example export/review paths must first be populated with real permitted content; this change creates neither an export nor permission evidence.

```sh
PYTHONPATH=src .venv/bin/python -m scripts.collect_dfb \
  --season 1990/91 \
  --seed data/private/germany/bundesliga_1990_1991_md1.html \
  --exports data/private/germany/exports/1990-1991/manifest.json \
  --reviews data/private/germany/exports/1990-1991/status_reviews.json
```

Omit `--reviews` to inspect candidates and gaps before finality evidence is available. A complete set of pages with 306 numeric scores still does not become accepted history automatically. Export `access_basis` and `evidence_reference` are retained verbatim as provenance, not interpreted as a legal permission determination.

## Authorized network mode — unavailable until real approval exists

The [DFB terms](https://www.dfb.de/nutzungsbedingungen) were checked again on 2026-11-05. Section 5 restricts unauthorized automated crawling/scraping and bypassing security measures. Section 7 restricts protected-content reuse and reserves commercial text/data mining. Public accessibility and the previously observed robots.txt 404 do not grant archive access or third-party rights. **No written archive permission or approved full HTML export is available in this workspace.** A project instruction to build software is not DFB authorization.

Network collection requires both explicit `--network` and `--authorization <private JSON path>`. That JSON must have:

- `network_collection_authorized: true`, set only after genuine written permission.
- `permission_reference`, `evidence_path` and `evidence_sha256` binding the actual nonempty permission document; the CLI requires it under private Germany storage.
- `approved_urls`: an exact allowlist of permitted matchday URLs; no wildcard inventory or unrelated host is accepted.
- Timezone-aware `valid_until` and `conditions_reviewed_at`; access conditions must have been reviewed within seven days. This is a conservative local gate, not a DFB-published interval.
- `minimum_interval_seconds`, at least five and at least any stricter interval required by DFB. Software validates configuration/evidence integrity, not the legal authenticity or sufficiency of the grant; the operator must establish that.

Once genuine scoped authorization has been obtained and configured, use:

```sh
PYTHONPATH=src .venv/bin/python -m scripts.collect_dfb \
  --season 1990/91 \
  --seed data/private/germany/bundesliga_1990_1991_md1.html \
  --network \
  --authorization data/private/germany/authorization/1990-1991.json
```

This is a future-use command, not evidence that authorization exists or a command executed during this change. The authorization must cover the selected season's actual URLs. A local configuration flag is not a legal grant. Supply `--reviews` during or after authorized retrieval to certify finals against real evidence.

With `--season 1990/91`, only that season's 34 URLs are visited sequentially, with cache hits reused and missing pages fetched through the unchanged authorized transport. Normal unfiltered network scope is the completed-history inventory only. `--include-ongoing` additionally requests 2026/27 only if those exact URLs are authorized. Explicit `--season 2026/27 --network` also requires `--include-ongoing`; offline selection does not. Ongoing results always retain their separate output partition. Cached pages need no request. Authorization scope/expiry is checked before every request and again after a pacing wait. A persistent lock prevents concurrent collectors; persisted request times enforce pacing across runs. Default transient retries are two, with backoff, for transport errors and HTTP 500/502/503/504. No other host, redirected endpoint, cookie session or authentication mechanism is followed automatically.

401/403/429/451, CAPTCHA/challenge/denial indicators and Retry-After stop the run and leave a persistent `STOP.json`; there is no automated clearing or retry around that restriction. Error/blocked response bodies and response-status/header events are retained privately; sensitive cookie/auth headers are excluded. Other HTTP failures, redirects, unknown/mismatched layouts and exhausted retries also stop archive continuation. Partial coverage is saved where possible and the CLI exits unsuccessfully. Resolve server restrictions with the provider before any operator changes a stop state; never reset it simply to try around a block.

Approved credentials/API-specific acquisition is not implemented as a bypass for protected endpoints. If DFB authorizes a different interface or layout, implement that explicit grant/interface separately or use approved full-page exports.

## Actual acquisition status

| Season | Available matchdays | Numeric candidates | Accepted finals | Season complete? |
|---|---:|---:|---:|---|
| 1990/91 | 1 / 34 | 9 | 0 | No |
| 1991/92 | 1 / 38 | 10 | 0 | No |
| 2005/06 | 2 / 34 | 18 | 0 | No |
| 2015/16 | 1 / 34 | 9 | 0 | No |
| 2025/26 | 1 / 34 | 9 | 0 | No |
| Other 31 completed seasons | 0 | 0 | 0 | No |
| 2026/27, separate ongoing | 0 / 34 | 0 | 0 | No |

Thus **six cached pages, 55 numeric candidates, zero complete seasons, zero evidence-accepted historical/ongoing finals**, with **1,222 historical matchdays still unacquired**. The new report deliberately makes a stronger acceptance distinction than the earlier parser-only trials, which validated extraction without certifying finality. It does not revoke those successful parsing results.

The automated suite now passes **384 tests** (including season-scoped CLI regressions). Tests include full synthetic 306-/380-match seasons, removed-page completeness failures, postponements, numeric-live-score rejection at acceptance, awarded-score evidence conflicts, source-ID/fixture/date conflicts, missing data, cache corruption/version conflicts, interruption resume/cache reuse, authorization/expiry/scope checks, post-wait expiry, pacing, transient retries, rate-limit/challenge/redirect stops, private path restrictions and offline CLI reproduction. Additional CLI tests cover mixed-season export filtering, exact 34-page scope, candidate/final separation, complete synthetic local 306-match exports, cache-only resumption and first-response access-denial stops. All network tests inject synthetic responses; no DFB archive requests are made.

Before complete historical acquisition: obtain the actual grant/export and trustworthy final/status/administrative evidence; acquire remaining approved pages; resolve all season report issues; independently verify a reproducible official-result sample; and confirm intended-use rights. The reusable pipeline and acceptance gates are implemented, but real archive completeness and unattended real-world status coverage have not been demonstrated. England datasets, prediction/Streamlit code and previous evaluation results remain unchanged. No model use, commit or push occurred.
