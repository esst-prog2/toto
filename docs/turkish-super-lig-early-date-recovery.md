# Turkish Süper Lig — supplemental early-date recovery

**Investigation PASS; proposals await owner approval.** The frozen Phase 3 registry remains unchanged: 10,060 INCLUDE and 483 HOLD OUT events. This supplement proposes recovery of all 480 targeted early events, including nine separately documented source repairs. It does not authorize Phase 4.

## Exact affected population

The extraction contains every target's frozen event/source IDs, source URL/SHA-256, physical line or grid-cell locator, original team labels and reported full-time score, available date context, insufficiency reason and proposed evidence. Detailed records remain private in `early_date_recovery/proposed/affected_events.json`; team-participation, reported-score and heading-frequency distributions are included there.

| Season | Existing original | Events | Existing date evidence | Proposed recovery |
|---|---|---:|---|---:|
| 1992/93 | [RSSSF round listings](https://www.rsssf.org/tablest/tur93.html) | 240 | 128 attached to single-day nominal headings; 112 attached to ranges | 240 |
| 1993/94 | [RSSSF result grid](https://www.rsssf.org/tablest/tur94.html) | 240 | No dates in any of the 240 grid cells | 240 |
| **Total** | **Two originals** | **480** | **Zero certified fixture-specific dates in the frozen inventory** | **480** |

Single-day round headings were not promoted into exact match dates. A nominal round day does not certify each fixture's actual kickoff, particularly for Saturday games and postponements. The grid supplies directed teams/scores but no calendar information. The new dates come from explicit individual fixture records.

The earlier **four exact-date-gap seasons overlap this population**. They are not four additional entirely uncovered seasons: 1990/91 and 1991/92 have tables but no conditional fixture descriptions; 1992/93 and 1993/94 contain these 480 held descriptions. The other three Phase 3 HOLD OUT events—two older award-date uncertainties and one abandoned original—are outside this supplement and remain unchanged. No missing fixture was invented or classified NOT PLAYED.

## Sources and permissions

All **26 existing originals and their receipts** were rechecked first. Only the two RSSSF files contain the targeted fixture descriptions. Engsoccerdata and Football-Data start later; the preserved OpenFootball originals cover later seasons. Other existing documents supply tables, later fixtures or metadata. The private `existing_source_review.json` accounts for every original, its coverage, fields, provenance and limitations.

New acquisition is exactly **70 TFF originals, 15,577,479 bytes**:

- One terms page, preserved before fixture acquisition.
- Sixty round pages: 30 per season, eight explicitly dated/scored fixtures per page, **480 distinct primary fixture IDs**.
- Nine linked professional match-detail pages for the isolated discrepancies; these corroborate existing events and do not add nine fixtures.

The governing-body archive provides [1992/93](https://www.tff.org/Default.aspx?pageID=560) and [1993/94](https://www.tff.org/Default.aspx?pageID=559) top-division records. Each acquisition is allowlisted, bounded, privately saved without overwrite, and paired with its exact URL, UTC retrieval timestamp, response metadata, bytes and SHA-256. Requests used light pacing; no login, access restriction or redirect was bypassed. The earlier Phase 1 encoding-stop record remains unchanged; this is a separately authorized and documented supplemental scope with the correct source encoding.

[TFF terms](https://www.tff.org/Default.aspx?pageID=179) permit attributed factual-information use and personal/noncommercial use of site facilities while retaining copyright. The acquisition assessment limits preservation to these bounded private research copies. It asserts no general archive-export, redistribution, commercial-use or model-training license. Original HTML, individual fixture lists and detailed audits remain private. Prior RSSSF attribution and all other licensing restrictions continue unchanged.

Sporzip pages were directly inspected for selected discrepancy comparisons; their upstream independence was not established and no dataset was downloaded. Mackolik and Worldfootball search results remained leads, with existing copying restrictions respected. RSSSF and legacy Turkish-Soccer material did not supply a new independent dated fixture population. Two misleading TFF season pages were rejected as lower-tier archives, and a same-day youth match was rejected as the wrong competition.

**Independence claim:** an authoritative TFF date attached to the actual fixture, reconciled with the frozen source observation, is independent of inferring a date from that observation's heading. This is not a claim that every fixture has two independently sourced exact-date confirmations or that all publishers have disjoint upstreams. Round and match-detail pages share TFF's database and count as one historical authority.

## Recovery and source discrepancies

| Season | Date-only recoveries | Additional source repairs | Unresolved target events |
|---|---:|---:|---:|
| 1992/93 | 233 | 7 | 0 |
| 1993/94 | 238 | 2 | 0 |
| **Total** | **471** | **9** | **0** |

All proposed dates are compared by season, directed clubs, score and fixture identity; existing round identity is also checked where present. The recovered dates span **23 August 1992–30 May 1993** and **28 August 1993–15 May 1994**.

The full comparison showed that nine records had defects beyond their missing certified dates: **six incorrect reported scores, two wrong-opponent descriptions and one malformed club label**. Each has an explicit physical-record-bound proposed repair in `repair_rules.json`, supported by both the acquired round row and the linked professional match panel. The underlying historical transcription process is not proven. These are isolated source-content defects, not a rule to prefer TFF automatically whenever sources disagree.

The two opponent repairs restore missing directed pairings while preserving the distinct, correctly described fixtures that had been duplicated by the bad labels. The malformed label is repaired for its one bound observation; no global alias is created. Score repairs preserve the directed clubs. These safeguards are enforced separately from ordinary date matching, and unreviewed discrepancies fail closed to HOLD OUT.

After the proposed repairs, every event corresponds one-to-one with the primary population: **240 unique directed pairings, 16 clubs and 30 participations per club in each season**. Independently reconstructed wins, draws, losses, goals for/against and points agree with **all 32 club-season rows in the preserved RSSSF final tables**. Aggregate tables corroborate the population; they never supply dates or fabricate fixtures.

| Disposition | Frozen Phase 3 | Proposed after approval |
|---|---:|---:|
| INCLUDE | 10,060 | 10,540 |
| HOLD OUT | 483 | 3 |
| NOT PLAYED | 30 | 30 |
| OUT OF SCOPE | 1 | 1 |
| **Total conditional events** | **10,574** | **10,574** |

Approval must cover both the **471 date-only recoveries and nine explicit source repairs**. The existing 10,060 accepted events have not been changed or silently enlarged. If approved, the two targeted early seasons' exact-date gaps close; 1990/91 and 1991/92 remain source gaps. Original fields, bytes and all frozen Phase 1–3 decisions remain intact.

## Verification and reproducibility

The adapter reuses established acquisition, checksum, immutable-save and permission-binding infrastructure. No shared infrastructure or prior competition script was changed. A separate verifier uses its own HTMLParser, field/record-locator reconstruction and decision checks; it imports no production recovery parser or selection helper. It also reuses the existing independent RSSSF parser to reconstruct all 480 original observations directly from preserved bytes. Season-bound correspondence declarations and explicitly reviewed historical repair facts are shared inputs, not independent repetitions of historical judgment.

**80 focused tests passed:** 25 new supplemental checks and 55 Turkish acquisition/recovery/structure/policy regressions. They cover exact fixture matching, reversed venues, wrong seasons/stages/tiers, missing dates, truncated rows, duplicates, unreviewed score conflicts, bound source repairs, changed originals, invented opponents and youth/professional confusion. Full-suite testing remains reserved for finalization.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -p 'test_turkish*.py' -v
PYTHONDONTWRITEBYTECODE=1 python3 -B -m scripts.recover_turkish_early_dates --verify
PYTHONDONTWRITEBYTECODE=1 python3 -B -m scripts.verify_turkish_early_dates --verify
```

The four authoritative proposed artifacts are private under `data/private/turkey/super_lig/early_date_recovery/proposed/`: `affected_events.json`, `supplemental_decisions.json`, `recovery_assessment.json` and `independent_recovery_validation.json`. Every decision is explicitly `PROPOSED_ONLY`; the frozen registry hash is an input boundary. Earlier diagnostic candidates remain preserved and are not downstream inputs. The private source manifest lists all 70 new source hashes and receipts; offline cache replay makes zero requests.

All four artifacts regenerated byte-for-byte/SHA-identically in separate fresh processes with network connections forbidden. All 70 new original/receipt pairs also verified offline. The supplemental-registry SHA-256 is `38b531d70e3e7418671e9006da17370b589ed9708d30f9317f788cc882520c87`; the complete new-source receipt manifest is `586b10788e1fe04a32e2864c755b75b02507a1b12cd63772bc2f20feb9103944`.

## Preservation and stop

The preservation baseline covers **2,011 existing entries, including 1,710 prior private files**, the planning-log prefix, all completed competitions, existing uncommitted work, Turkish frozen decisions/originals, Git index and environment configuration. No package installation, environment rebuilding, prediction changes, standardized data, branch/worktree changes, staging, commit or push occurred. The Hungarian worktree was accessed only for a read-only Git-state snapshot; no file there was written. Concurrent-agent changes, if any, are distinguished from preservation of the Turkish baseline in the final receipt.

The fresh audit matched every Turkish baseline entry and the append-only planning prefix. The Hungarian worktree's HEAD, branch and index matched its initial snapshot; its untracked-file list changed during the parallel work. Those changes were neither reset nor attributed to this supplement. No exhaustive installed-package-byte or Hungarian-file-content certificate is claimed.

`PLANNING_LOG.md` records the authorization, evidence and proposed decisions append-only. Exact source/code/configuration/output hashes, focused checks, offline reproduction, preservation and timing are retained privately.

**STOP. Await explicit approval of the supplemental registry and nine source repairs. Phase 4 has not begun.**

Measured execution: **23 min 50 sec** (1430.2 seconds active-session wall), from `2026-11-26T15:02:12+00:00` to audit checkpoint `2026-11-26T15:26:02.142451+00:00`. Approval wait: **0 seconds**; total elapsed **1430.1 seconds**. Successful acquisition request durations sum to **61.20 seconds**, already included in wall time. Research, web/tool and file-provider waits, acquisition pacing, the corrected initializer-import failure, verification and reporting are included. Web-search/tool wait was not separately instrumented; final receipt emission and chat rendering after this checkpoint are excluded.
