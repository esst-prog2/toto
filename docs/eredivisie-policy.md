# Eredivisie — Phase 6 source, exception and chronological policies

Date: 2026-11-23. Original toto worktree on `feature/data-collection`, HEAD `4f8c64433cf6168a06dbde0102e822ce6d2eeffa`.

Phase 6 only: explicit processing metadata and provisional dispositions. No final standardized CSV or complete Phase 7 audit archive has been generated. No original, frozen assessment, application or prior competition dataset was changed. Source acquisition and model training were not performed.

## Reconciliation and provisional Phase 7 scope

The verifier regenerates Phase 5 and its underlying independent Phase 4 source parsing before constructing policy groups. It checks saved assessment bytes, all protected originals/evidence, every source binding, exactly one source-to-fixture linkage and one disposition per unique slot. No observations are discarded to fit expectations.

| Accounting level / disposition | Completed-result candidates | HOLD OUT | NOT PLAYED | Total |
|---|---:|---:|---:|---:|
| Original source observations | 13,005 | 5 | 74 | 13,084 |
| Unique fixture slots | 10,939 | 3 | 74 | 11,016 |

The 13,084 observations comprise 10,636 historical and 2,448 modern records, with 13,009 score-bearing and 75 null-score observations. Exactly 2,068 overlapping representations remain linked for audit, not counted as extra matches. There are 11,016 selected representations and 2,068 nonselected overlap representations. All originals remain traceable through source URL, revision/blob/hash, physical lines and original field bindings.

There are **zero supplemented candidates, zero administrative HOLD OUTs, two material-completion-evidence HOLD OUTs, one supplemental-permission HOLD OUT and zero definitive exclusions**. HOLD OUT is not permanent exclusion or a claim the fixture was not played.

Subject to Phase 7 approval, the measured expected CSV scope is **10,939 provisional candidates across 36 seasons**. The future archive must preserve **all 13,084 original observations and all 11,016 unique dispositions**, including the three HOLD OUTs and 74 NOT PLAYED slots. No final shared-schema match IDs or eight-column CSV rows are emitted in this phase; internal fixture IDs are policy identities, not a replacement for the historical import schema.

## Source hierarchy and its limits

* Historical `jalapic/engsoccerdata/data-raw/holland.csv`, revision `872c5c354161ace8408f3091b758c6af4cccca94`: primary candidate representation for 1990/91–2024/25, covering 10,636 unique slots including two later HOLD OUTs.
* Modern OpenFootball/europe, revision `63df627f3c87ce71708f016522ea236cf74332c3`: primary representation for 306 slots in 2025/26, including NAC's HOLD OUT; sole explicit source for the 74 unplayed 2019/20 slots.
* The seven modern overlap seasons supply 2,068 exact scored comparator representations. These remain nonselected and immutable; conflicting values are never overwritten.

This hierarchy is supported by continuous historical coverage, complete ordinary directed pairings and coherent literal labels. The historical file is the only approved source for earlier seasons. Across the 2,068 scored overlap pairs, the known date and score disagreements are isolated and explicitly adjudicated. Switching wholesale to the modern source would introduce more label/source boundaries without stronger independent accuracy evidence; its known NEC intermediate-score problem and NAC incomplete snapshot do not establish superiority. Conversely, historical coverage and agreement do not prove all historical values correct. Both sources retain upstream provenance and licensing uncertainty.

Every unique policy entry records the selected source ID and selection reason. Exact fixture-level exceptions override only approved date/value interpretations, not the source bytes or unrelated records. No global date/score correction is applied.

## Nine exact source-bound exception decisions

Policy selectors use explicit immutable source-observation IDs, not broad team-name or annotation searches. Each case validates the approved source dates, original scores, season, participants and frozen historical-review binding. The complete source IDs, physical lines, evidence links and alternative representations are private; the public decision table summarizes them.

| Decision | Source / event chronology | Provisional result and date | Disposition and justification |
|---|---|---|---|
| GRONINGEN_AJAX | 2022/23; historical 2023-05-14, modern 2023-05-16; both 2–3 | Historical selected representation; approved date 2023-05-16, 2–3 | Candidate. May 14 interrupted event remains separate; one date interpretation, not a second fixture. |
| NEC_VITESSE | 2023/24; both 2023-10-01; historical 1–3, modern 1–2 | Historical final 1–3 on 2023-10-01 | Candidate. Direct club final record/narrative and contemporary report support 1–3. Intermediate 1–2 is documented, but the upstream error mechanism remains unproven. |
| NAC_HEERENVEEN | 2025/26; modern line 509: 2026-05-10, null, `[cancelled]`; evidence: May 11 completion, 2–0 | No approved candidate values; documentary 2–0/May 11 retained separately | HOLD OUT. Supplemental-value usage compatibility is unestablished; the original null/cancellation remains unchanged. Not NOT PLAYED. |
| AJAX_FEYENOORD | 2023-09-24 interruption; both sources date completion 2023-09-27 | 0–4, 2023-09-27 | Candidate; existing source completion date unchanged. |
| RKC_AJAX | 2023-09-30 interruption; both sources date completion 2023-12-06 | 2–3, 2023-12-06 | Candidate; existing source completion date unchanged. |
| AZ_NEC | 2023-10-29 interruption; both sources date completion 2023-12-06 | 1–2, 2023-12-06 | Candidate; existing source completion date unchanged. |
| FEYENOORD_VVV | 2018/19; November 4 floodlight interruption; both sources December 6, 4–1 | No approved candidate values; reported December 6 completion retained separately | HOLD OUT. Directly inspected interruption and replay-scheduling evidence do not directly establish actual completion and the completed result. |
| VITESSE_SPARTA | 2021/22; March 4 interruption; both sources April 19, 0–1 | No approved candidate values; reported April 19 completion retained separately | HOLD OUT. Frozen primary scheduling/contemporary completion leads are index-only; direct completion retrieval failed. |
| HERACLES_GRONINGEN | 2024/25; December 21 interruption, January 28 completion | 1–1, 2025-01-28 | Candidate. Direct contemporary completion report; both source dates already reflect completion. |

Evidence for Groningen: [G1](https://www.knvb.nl/nieuws/betaald-voetbal/eredivisie/67697/fc-groningen-ajax-op-dinsdag-16-mei-uitgespeeld), [G2](https://www.ajax.nl/artikelen/verslag-ajax-wint-nipt-in-groningen/). NEC: [N1](https://www.nec-nijmegen.nl/wedstrijden/wedstrijd/nec-vitesse-2023-10-01z-101500z.htm), [N2](https://www.nec-nijmegen.nl/sitewide/vraag/n.e.c.-verliest-de-gelderse-derby.htm), [N3](https://nos.nl/artikel/2492493-vitesse-scoort-weer-eens-en-wint-opnieuw-gelderse-derby-in-nijmegen). NAC: [B1](https://www.nac.nl/nieuws/winst-in-twee-delen-voor-gedegradeerd-nac), [B2](https://nos.nl/artikel/2613947-gedegradeerd-nac-pakt-in-heerenveen-drie-punten-geen-goals-meer-in-restant-duel), [B3](https://www.knvb.nl/nieuws/betaald-voetbal/vriendenloterij-eredivisie/71803/wedstrijd-nac-breda-sc-heerenveen-definitief). The three 2023/24 fixtures: [A1](https://www.ajax.nl/artikelen/verslag-ajax-verliest-klassieker-in-eigen-huis), [A2](https://www.knvb.nl/nieuws/betaald-voetbal/competitiezaken/68180/ajax-%E2%80%93-feyenoord-wordt-27-september-uitgespeeld), [R1](https://nos.nl/artikel/2500620-ajax-trekt-zege-in-duel-van-tien-minuten-bij-rkc-waalwijk-over-de-streep), [R2](https://eredivisie.nl/nieuws/rkc-waalwijk-ajax-uitgespeeld-op-woensdag-6-december/), [Z1](https://www.nec-nijmegen.nl/wedstrijden/wedstrijd/az-nec-2023-12-06z-180000z.htm), [Z2](https://az.nl/inside-az/nieuws/2023/oktober/az-nec-gestaakt), [Z3](https://www.vi.nl/nieuws/nec-houdt-voorsprong-op-az-vast-in-restant-van-in-oktober-gestaakt-duel), [Z4](https://www.knvb.nl/node/68342). Additional interruptions: [F1](https://www.knvb.nl/nieuws/betaald-voetbal/eredivisie/51160/feyenoord-%E2%80%93-vvv-gestaakt-vanwege-uitvallen-lichtmasten), [F2](https://nos.nl/artikel/2258030-feyenoord-vvv-op-donderdag-6-december-overgespeeld), [F3](https://nos.nl/liveblog/2262325-larsson-heeft-de-vorm-gevonden-en-helpt-feyenoord-aan-eenvoudige-zege), [VS](https://vitesse.nl/nieuws/2022/restant-vitesse-vs-sparta-rotterdam-op-dinsdag-19-april-uitgespeeld), [VS2](https://www.nhnieuws.nl/nieuws/n76469/sparta-houdt-stand-in-resterende-374-seconden-en-boekt-belangrijke-zege-op-vitesse), [HG](https://nos.nl/artikel/2553645-groningen-en-heracles-komen-in-resterende-21-minuten-niet-tot-scoren).

The two additional HOLD OUTs have a specific material chronology problem: the result concerns a known interrupted fixture, and the frozen record does not directly establish the actual completion/result-availability event. Source agreement and a planned resumption alone do not resolve that risk. This narrow decision does **not** create a rule excluding every ordinary fixture lacking direct historical corroboration. Releasing either HOLD OUT requires a separately evidenced decision; no fresh historical research was undertaken here.

For the six accepted exception decisions, completion-day knowledge is established at day precision: Groningen May 16, NEC–Vitesse October 1, Ajax–Feyenoord September 27, RKC–Ajax and AZ–NEC December 6, and Heracles–Groningen January 28. No precise publication timestamp is invented. Reported-but-unverified completion dates for the two evidence HOLD OUTs are stored separately; verified `completion_date` and effective availability stay null. NAC's documented actual completion is preserved, but its unapproved supplemental value has no approved effective availability.

## NAC supplementary-result assessment

Exact identity, direct result/completion corroboration, traceable references, bounded permitted inspection, original immutability, fixture-specific scope, a completion-based chronology condition and no new dataset acquisition are satisfied by the recorded evidence. **Compatibility with applicable downstream usage restrictions remains unestablished.** Public access and the existing article citations do not supply that missing clearance.

The decision is therefore **B: HOLD OUT pending additional permitted evidence or authorization**. The registry separately retains the source null score, the historical documentary result 2–0, May 10 kickoff/interruption and May 11 completion. No 2–0 value is inserted into any source or candidate record. The supplementary guard requires every criterion to be explicitly true and is restricted to this exact source ID; the current policy does not approve supplementation.

This does not assert that using an individual historical fact is legally prohibited. It records that the specific required usage condition has not been established under the approved conservative gate. Technical candidates elsewhere also remain uncleared for redistribution or training.

## 2019/20 NOT PLAYED policy

The source inventory independently reconciles 306 season slots: **232 played results and 74 unplayed slots**. The 232 played results remain completed-result candidates; historical overlap observations are not extra fixtures. The 74 explicit modern `[cancelled]` observations retain null scores and receive exactly one NOT PLAYED disposition each. Their historical-source absence remains a different coverage fact. A cancellation annotation outside this exact season/approved case does not automatically establish NOT PLAYED.

The frozen directly inspected KNVB April 24 decision stops the competition and uses existing standings for European qualification, without supporting blanket annulment of played results. The PSV report and independently inspected research aggregate remain attached. Evidence: [T1](https://www.knvb.nl/node/59905), [T2](https://www.psv.nl/media/artikel/psv-eindigt-eredivisie-als-vierde), [T3](https://pure.uva.nl/ws/files/89216271/Burgers_Beukeboom_Smith_Van_Biemen_2023_.pdf). No score is fabricated and no ordinary played fixture is excluded merely because the season ended early.

## Scheduling, confidence and club identities

All 25 wide-round contexts / 225 members, 16 reversal pairs / 32 endpoints, 410 Phase 4 flagged observations and 452 Phase 5 review observations remain visible. The frozen classifications remain 18 fully corroborated, 196 partial, one contradicted and 237 unresolved source observations. Phase 6 does not upgrade them to certification. The single contradicted NEC modern value is resolved through its explicit score-selection policy; it remains contradicted in provenance.

Long spans, physical source-order reversals, unusual scores, diagnostic label differences and lack of direct review alone do not exclude a fixture. Other newly encountered material score/date contradictions or incomplete results fail closed to an explicit HOLD OUT; an unknown structural/administrative flag requires explicit policy review instead of silently passing. Unknown flags, altered historical bindings or missing exception evidence cause validation failure.

Only the 2,068 exact scored observation pairs from the frozen, season-local overlap comparison are approved correspondence links. Pair identities are supported by participant sets, directed pairing structure, match-level dates/scores and the two separately reviewed disagreements. Literal originals remain intact. Correspondence metadata is scoped to season and exact source IDs; it does not assert global legal continuity or change output names. The 74 modern-only cancellation slots remain individual source-bound identities.

The selected source's literal labels are retained. NEC/N.E.C., RKC/Waalwijk, NAC/Breda and other abbreviations do not trigger global aliases. The Zwolle bankruptcy/name changes, Den Haag merger and SVV/Dordrecht history remain evidence-specific uncertainties. Senior, Jong/reserve and predecessor/successor identities are not merged. No new cross-season correspondence rule was introduced. The two 1979/80 PEC Zwolle observations remain outside the target population and unchanged.

## Strict chronological consumer contract

The per-fixture chronology distinguishes source dates, source-only scheduled dates, actual/approved kickoff, interruption, resumption/completion, reported completion, administrative publication/finality, source-date proxies and effective availability. Unknown information stays null. Administrative finality is not invented. The ordinary source date remains a proxy, even for an independently sampled fixture, until an explicit availability policy establishes otherwise.

`PredictionGate` regenerates the policy from protected originals and frozen evidence, then byte-compares **every saved policy artifact**, including the manifest, before retaining detached expected decisions. Every supplied decision must exactly equal its trusted expected entry. A caller cannot turn eligibility on by editing dates, source IDs, confidence, disposition, chronology, permission or other fields.

Chronological eligibility requires a completed-result candidate, no unresolved administration, a verified availability day, a known completion day and:

```text
completion_day <= effective_availability_day < prediction_day
```

Same-day use is always rejected because intraday ordering is unverified. Future completions, later availability, unknown required information and unresolved material cases cannot pass. Malformed cutoffs and altered/incomplete decision entries fail explicitly. The independent actual-population check found only **six** exception decisions with established day-level eligibility at the November 23 cutoff, **zero same-day eligible candidates**, and **zero training-authorized decisions**. All ordinary source-date proxies fail the chronology gate; this does not remove them from the provisional historical candidate population.

Historical screening, chronology eligibility and training authorization are different classifications. `training_allowed` remains false because model-training permission is NOT_CLEARED. No application consumer is modified or integrated. **The future CSV alone must not be described as leakage-safe.**

## Season-level provisional dispositions

| Season | Completed candidates | HOLD OUT | NOT PLAYED | Unique slots |
|---|---:|---:|---:|---:|
| 1990/1991 | 306 | 0 | 0 | 306 |
| 1991/1992 | 306 | 0 | 0 | 306 |
| 1992/1993 | 306 | 0 | 0 | 306 |
| 1993/1994 | 306 | 0 | 0 | 306 |
| 1994/1995 | 306 | 0 | 0 | 306 |
| 1995/1996 | 306 | 0 | 0 | 306 |
| 1996/1997 | 306 | 0 | 0 | 306 |
| 1997/1998 | 306 | 0 | 0 | 306 |
| 1998/1999 | 306 | 0 | 0 | 306 |
| 1999/2000 | 306 | 0 | 0 | 306 |
| 2000/2001 | 306 | 0 | 0 | 306 |
| 2001/2002 | 306 | 0 | 0 | 306 |
| 2002/2003 | 306 | 0 | 0 | 306 |
| 2003/2004 | 306 | 0 | 0 | 306 |
| 2004/2005 | 306 | 0 | 0 | 306 |
| 2005/2006 | 306 | 0 | 0 | 306 |
| 2006/2007 | 306 | 0 | 0 | 306 |
| 2007/2008 | 306 | 0 | 0 | 306 |
| 2008/2009 | 306 | 0 | 0 | 306 |
| 2009/2010 | 306 | 0 | 0 | 306 |
| 2010/2011 | 306 | 0 | 0 | 306 |
| 2011/2012 | 306 | 0 | 0 | 306 |
| 2012/2013 | 306 | 0 | 0 | 306 |
| 2013/2014 | 306 | 0 | 0 | 306 |
| 2014/2015 | 306 | 0 | 0 | 306 |
| 2015/2016 | 306 | 0 | 0 | 306 |
| 2016/2017 | 306 | 0 | 0 | 306 |
| 2017/2018 | 306 | 0 | 0 | 306 |
| 2018/2019 | 305 | 1 | 0 | 306 |
| 2019/2020 | 232 | 0 | 74 | 306 |
| 2020/2021 | 306 | 0 | 0 | 306 |
| 2021/2022 | 305 | 1 | 0 | 306 |
| 2022/2023 | 306 | 0 | 0 | 306 |
| 2023/2024 | 306 | 0 | 0 | 306 |
| 2024/2025 | 306 | 0 | 0 | 306 |
| 2025/2026 | 305 | 1 | 0 | 306 |

## Artifacts, reproducibility and fresh tests

Public Phase 6 work consists of `scripts/decide_eredivisie_policy.py`, `tests/test_eredivisie_policy.py`, this report and append-only `PLANNING_LOG.md` entries. Private additions are the protected baseline, six policy artifacts, test/reproducibility/final receipts and `verification_phase6/` logs/XML/status. The source-observation registry holds policy provenance bindings; it is not the final Phase 7 complete audit archive.

The six deterministic artifacts cover all source-observation policies, all unique dispositions, source selection/correspondences/exceptions, chronology, summary and the hash manifest. The manifest binds frozen assessment/evidence inputs and the other five output byte counts/SHA-256 values. Each unique fixture has one internal ID independent of source date changes, preventing the Groningen date interpretation from creating another fixture; league/season/literal selected teams are length-safely encoded. Production reconciliation rejects lost, multiply assigned or duplicate fixture/source identities.

A fresh regeneration into separate safe temporary storage was byte-identical for all six outputs:

| Policy artifact | SHA-256 |
|---|---|
| phase6_chronology_registry.json | `02232738728cc3f5a8e2b5922a7f44d91294285905dde4dbe959337a673d46f1` |
| phase6_policy_manifest.json | `23250d6cca4ac6265612380da893168999ea1a406ff3e8959f1c5b7a389b4ba8` |
| phase6_policy_summary.json | `17ac3414fcc552ece867e275dbb0b3d9e8b51c79494e35f87dc61fc85a95127b` |
| phase6_source_observation_policy.json | `e307a907bed305568a9eeb7cc2dc5a3794882706c3984a1e591c2e14f96ce26e` |
| phase6_source_selection_exceptions.json | `33dbc9cccc089b6c274a4b17119a25aaa60675c320c816fc9e97596da1f4a282` |
| phase6_unique_fixture_policy.json | `43ebe3d970e6f33cd67b43e3b785abb47e1a7695ebc6527097baa93554bb6a5f` |

The fresh final-state test runs used the existing external Python 3.13.12 environment, with bounded timeouts and disabled project bytecode/pytest-cache writes. The original `.venv` was not modified and nothing was installed. Suites overlap and must not be added:

| Test selection | Passed | Failures / errors / skips |
|---|---:|---|
| acquisition_importer | 556 | 0 / 0 / 0 |
| app_launcher | 7 | 0 / 0 / 0 |
| eredivisie | 225 | 0 / 0 / 0 |
| full | 1784 | 0 / 0 / 0 |
| historical_review | 32 | 0 / 0 / 0 |
| non_ui | 1777 | 0 / 0 / 0 |
| policy | 78 | 0 / 0 / 0 |

The 78 new policy cases exercise source hierarchy, overlap accounting, every exception and original-date/score binding, supplementary criteria and HOLD OUT behavior, cancellation accounting, context-only uncertainty, reserve/distinct identities, unknown contradictions/flags, manifest/file-integrity loading, same-day/future/unknown availability and unresolved administration rejection, unchanged source inputs and caller-supplied permission tampering. Actual-population regeneration separately verifies all 74 NOT PLAYED slots and the 232 retained 2019/20 results, plus original Groningen/NEC/NAC representations and the chronological gate.

Reproduction, without acquisition or standardization:

```sh
PYTHONPATH=. python -B scripts/decide_eredivisie_policy.py
PYTHONPATH=src:. PYTHONDONTWRITEBYTECODE=1 python -B -m pytest tests/test_eredivisie_policy.py -q -p no:cacheprovider
```

`--init` establishes the baseline once after validating approved Phase 5 receipts. Ordinary runs compare existing output bytes and refuse changes rather than overwrite them. Protection passes for 839 earlier private files / 207 public files, plus 137 frozen Phase 2–5 entries and the planning prefix. All ten prior competitions, nine Eredivisie originals and frozen assessments remain unchanged. HEAD and Git index remain unchanged; all private artifacts are Git-ignored and untracked. No application or promotional-worktree file was changed. No staging, commit, push, merge or rebase occurred.

## Remaining limits and stopping point

Structural suitability, historical corroboration, actual availability, acquisition permission, redistribution rights and training permission remain separate. Historical noncommercial notices/GPL metadata and OpenFootball CC0 do not establish every upstream right. Ordinary candidates are not individually historically certified; Phase 5 confidence gaps and club-identity questions persist. The three HOLD OUTs need separate evidence/permission review, not automatic release.

Phase 7 requires explicit approval. Its currently measured scope is 10,939 candidate CSV records, 13,084 original observations preserved in the complete audit trail and 11,016 unique dispositions. It must use the existing eight-column schema and shared ID conventions, retain the one approved Groningen date interpretation and NEC score decision, exclude the 74 NOT PLAYED and three HOLD OUT fixtures from screening, and preserve all alternative original values. Do not train or integrate data merely because that future CSV can be generated.

Stop after Phase 6 for review. No Phase 7 standardization has begun.
