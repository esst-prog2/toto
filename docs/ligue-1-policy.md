# Ligue 1 Phase 6 — historical decisions and chronological safeguards

Date: 2026-11-22. Scope: processing metadata only, on `feature/data-collection` at HEAD `81225118ced664f113c19b87cff8095b0333ccda`. The user approved Phase 5 as an evidence review and authorized conservative Phase 6 decisions. The additional conservative choices below are recorded for review before Phase 7.

No source data, Phase 2–5 evidence, previous competition, application or promotional file was changed. No season dataset was acquired. No standardized CSV or full match audit archive was generated. Policy assessment metadata comprises explicit exception assessments, candidate audit-ID membership, counts and fingerprints; ordinary complete match rows remain only in preserved prior evidence. The complete assessment is evaluated in memory and SHA-bound, rather than emitted as a new full match archive.

## Provisional reconciliation

| Classification | Observations |
|---|---:|
| Original acquired observations retained | 12,707 |
| Score-bearing observations before screening | 12,606 |
| Explicitly not played | 101 |
| Administrative numerical-outcome HOLD OUT | 2 |
| Administrative finality/availability HOLD OUT | 2 |
| Additional disputed-date HOLD OUT | 1 |
| Completed-result candidates, not standardized | 12,601 |
| Other definitive exclusions | 0 |
| Explicit source-bound decision entries | 108 |

The disjoint reconciliation is **12,707 = 12,601 candidates + 4 administrative holdouts + 1 date holdout + 101 not played**. The 108 decisions comprise seven named cases and 101 individually bound cancellations; group rules cover ordinary numeric interpretation, identities and preserved uncertainty. Candidate outcome counts are H=5,832, D=3,581, A=3,188. These are computed policy candidates, not licensed or historically certified model-training records, and not a predetermined accepted-record target.

All 12,707 observations are to remain in a future full audit archive, including not-played and held-out observations. That archive belongs to Phase 7 and has not been created here. The missing 1994/95 season and missing Nantes–Toulouse 2006/07 fixture are not fabricated observations or hidden exclusions in these totals.

## Source-bound decisions

| Decision | Source date / score | Action | Effective result date | Reason and evidence |
|---|---|---|---|---|
| Bastia–Lyon 2016/17 | 2017-04-16 / modern 0–0 `[awarded]`; overlapping CSV 0–3 | UNRESOLVED / HOLD OUT: numerical semantics | Unknown | Awarded Lyon winner cannot safely be represented as an ordinary draw or an invented numeric award. Indexed May 4 report and preserved FFF appeal document do not establish operative numerical finality. |
| Nantes–Bastia 2013/14 | 2013-08-10 / 0–0 | UNRESOLVED / HOLD OUT: numerical semantics | Unknown | [Conseil d’État](https://www.legifrance.gouv.fr/ceta/id/CETATEXT000032528070/) establishes penalty defeat decided 2014-02-12, upheld 2014-02-26, judicial rejection 2016-05-11. Numerical awarded score remains unknown. This match is not reclassified as interrupted. |
| Montpellier–Saint-Étienne 2024/25 | 2025-03-16 / 0–2 `[awarded]` | UNRESOLVED / HOLD OUT: finality/availability | Unknown; administrative bound 2025-04-02 | [LFP notice](https://www.lfp.fr/article/commission-de-discipline-les-decisions-du-2-avril-2025) ratifies interrupted on-field score. The played 0–2 is corroborated. Conservative holdout retains Phase 5's materially unresolved appeal/finality and operational availability classification; a known score is not being declared wrong. |
| Nantes–Toulouse 2025/26 | 2026-05-17 / 0–0 | UNRESOLVED / HOLD OUT: finality/availability | Unknown; administrative bound 2026-05-27 | [LFP notice](https://www.lfp.fr/article/commission-de-discipline-les-decisions-du-27-mai-2026) ratifies 0–0 with immediate effect. It does not establish exhausted appeals. Retain that material uncertainty conservatively; do not backdate ratification to May 17. |
| Nice–Marseille 2021/22 | 2021-10-27 / 1–1 | Approved replay date and unchanged score | 2021-10-27 | Original event 2021-08-22, replay ordered 2021-09-08. [Club replay narrative](https://www.ogcnice.com/fr/resume/119578/un-derby-sans-vainqueur-1-1.html) directly corroborates 1–1 at Troyes on October 27. |
| Montpellier–Clermont 2023/24 | 2023-11-29 / 1–1 | Approved replay date and unchanged score | 2023-11-29 | Original event 2023-10-08, replay ordered 2023-10-25. [Contemporary replay report](https://www.sofoot.com/breves/pas-de-vainqueur-entre-montpellier-et-clermont-dans-leur-match-rejoue) corroborates November 29 result. Abandoned 4–1 is not substituted for the replay. |
| Auxerre–Lyon 1996/97 | 1996-10-26 / 7–0 | UNRESOLVED / conditional HOLD OUT: date dispute | Unknown | [Participant interview](https://www.lyonfoot.com/article/6127/ce-match-qui-m-a-marque-auxerre-ol-en-1996-par-sylvain-deplace) dates play October 25. One retrospective interview is insufficient to apply the correction. Keep the original date and both candidate event dates; exclude from chronological screening pending further evidence. |

The four administrative holdouts include two distinct kinds of uncertainty: two numerical-outcome conflicts and two conditional finality/availability cases. The latter two have supported numerical ratifications; unknown appeal exhaustion is not an assertion that the LFP notices are invalid. This is the conservative Phase 6 choice pending review, not a fabricated contrary decision. No unverified appeal finality date is populated.

Full source file SHA-256, physical line, raw-line SHA-256, original numeric goals, auxiliary label, annotation, risk flags, evidence IDs/URLs and evidence fingerprints bind each decision. Overlapping CSV bindings remain separate from the primary observation. Selected IDs and physical locations are listed below; these are source audit IDs, not shared-schema match IDs.

| Decision ID | Immutable audit ID | Source path and physical line |
|---|---|---|
| `MHSC_CLERMONT` | `ligue1:01d891740e2dbde119c46a4a869ab12541661a7fd719edc0abf6f55dd492337c` | `openfootball/europe/france/2023-24_fr1.txt:204` |
| `MONTPELLIER_ASSE` | `ligue1:01e5de681c1868bf3cc747a6f38140ec81f56f6ce2b6e62ab733033f87a0545e` | `openfootball/europe/france/2024-25_fr1.txt:394` |
| `BASTIA_LYON` | `ligue1:05f31775318ea5c878f79145960a82cc085cfb500f411a879f881d7f361e36e9` | `openfootball/europe/france/2016-17_fr1.txt:533` |
| `AUXERRE_LYON` | `ligue1:1bd9dbdf620f055b8fe6efe3ed9b891eaa524d3fc85f38de2369b8bcd90b8e1d` | `jalapic/engsoccerdata/data-raw/france.csv:19293` |
| `NANTES_TOULOUSE_2026` | `ligue1:37bd9ef80eeee6537469820256f03ae41d7f0d82620314de9d791e826077b27b` | `openfootball/europe/france/2025-26_fr1.txt:890` |
| `NICE_OM` | `ligue1:530274bda49038f57f263d6be523991e8757cfcabd85a4cf246e2baabee98a75` | `openfootball/europe/france/2021-22_fr1.txt:55` |
| `NANTES_BASTIA` | `ligue1:6a3952b7e398605cc943e89e86df35ca10a182074ab0f0c9f5e88fe30ab9ea7f` | `jalapic/engsoccerdata/data-raw/france.csv:25254` |

## Numeric outcomes and defective auxiliary labels

The source-bound interpretation rule covers the preserved historical CSV and its 1,895 primary auxiliary-label contradictions. For ordinary accepted full-time results only, derive H, D or A by comparing nonnegative integer home and away goals. Require their canonical score string to agree with FT; reject missing, invalid or contradictory numeric values. Preserve every original label and goal in source/audit evidence.

This is **not** a global D→A replacement: an actual 1–1 stays a draw, a 2–1 stays a home win, and numeric 0–2 is an away win whether the auxiliary label says D or A. Administrative representations go through their explicit decision instead, and the four administrative holdouts receive no candidate outcome. Source-marked administrative or unresolved material cases cannot silently use this ordinary rule.

Phase 5's directly inspected signed Toulouse–PSG 2–3 narrative supports a numeric away victory despite a source D label, alongside independently corroborated home/draw examples. The 1990s and 2010s extra away examples remain limited by evidence provenance/access; the 5,489 broader CSV label defects do not certify all numeric goals. This is an interpretation of a demonstrably defective auxiliary field, not population-wide historical certification or permission to change original labels.

## Not played, rather than missing or awarded

The original OpenFootball annotation and null goals/FT must agree with the `NOT_PLAYED` decision. Each of all 101 slots is bound individually. [Official LFP board minutes, 30 April 2020](https://www.lfp.fr/assets/20200430_PV_Conseil_Administration_LFP_e824a457fa.pdf), page 9, establish 279 played out of 380 scheduled. The independent source reconciliation remains **380 = 279 + 101**. All 101 are in the future audit population, and none can enter a future screened completed-result dataset as an invented 0–0 or an unresolved administrative award.

No ordinary fixture is held out simply because independent sampling failed. A long round, an unusual score or absent independent corroboration alone is not a positive finding of incorrectness.

## Club identity interpretation

Only the historical CSV's **1990/91** observations explicitly bound to the Brest evidence may interpret `Stade Brest` and `Brest Armorique FC` as the same season sporting entrant, using the existing source label `Brest Armorique FC` for candidate identity. The [BnF authority record](https://catalogue.bnf.fr/ark:/12148/cb123358120) supports the historical names and also records subsequent liquidation/succession, so no global legal-entity or successor alias is authorized.

The identity rule covers 38 bound fixtures, changes 18 candidate labels, and independently reconciles the whole 1990/91 season to **20 clubs, 380 directed home/away pairings, each exactly once**. The source bytes and labels are unchanged. Other seasons and sources do not inherit this rule.

AC Ajaccio and Gazélec FC Ajaccio remain distinct. The [FFF archive](https://www.fff.fr/216-parcours-national-ajaccio-gfc.html) identifies Gazélec as the 2015/16 Ligue 1 entrant; the modern primary labels remain literal, and the 38 unmatched pairings on each side of the CSV/modern overlap remain visible. No AC Ajaccio→Gazélec mapping is implemented. Historical Toulouse continuity and other reconstituted entities retain their Phase 5 limitations rather than acquiring unverified global aliases.

## Chronology: current enforcement and future obligations

Decision metadata distinguishes source date, scheduled date (unknown unless established), original kickoff/event, interruption, replay/completion, administrative publication, appeal/judicial notes, finality and effective result date. Unknown values remain null. Ratification dates are not relabelled as dates of play. The two approved replays use their verified replay dates; all five holdouts have unknown effective availability and cannot screen in.

For otherwise ordinary candidates the source date is retained as a **source-reported date**, not invented independent availability certification. A full-fact independent match corroboration or the approved replay establishes the stronger availability classification; absence of corroboration does not automatically reject an ordinary screening candidate. Source order, round number and nominal fixture date never override a material unresolved conflict.

Current policy code enforces:

- Exact regeneration and validation of the complete decision registry against preserved evidence before assessment.
- Fail-closed handling of missing/duplicate/altered decisions, changed source bindings, missing evidence, new unknown risk flags and additional positive material conflicts.
- No candidate outcome/date for cancelled slots or holdouts; unchanged numeric goals only for ordinary candidates.
- `known_strictly_before`: a result date must be strictly earlier than prediction date. Same-day, future and unknown availability cannot pass; noncanonical dates are rejected.
- `training_allowed`: candidate eligibility, no material conflict, independently supported availability, model suitability clearance, licensing clearance and strict chronology must all pass.

Every current assessment leaves model suitability `NOT_CLEARED` and licensing `UNRESOLVED`, so **zero observations are training-cleared**. Even setting future rights flags would not make an uncorroborated source date demonstrably known. Future training/backtesting consumers must actually call the validated policy and chronology guards; this phase does **not** integrate enforcement into application/model code. A future consumer bypassing these functions is not protected by merely having a policy file.

## Preserved uncertainty and confidence

All **40 scheduling contexts / 394 affected slots** are copied with their exact frozen member sets and classifications: 9 documented, 31 partial. The 35 ordinary sample statuses remain 15 verified, 2 partial, 18 unresolved. All individual Phase 5 review statuses, identity concerns, source-boundary limitations, unusual scores, additional unreviewed legal lead and 1,162 broader date candidates remain visible, with no additional correction/exclusion inferred from those flags.

| Policy confidence class | Observations |
|---|---:|
| `INDEPENDENT_FULL_FACTS` | 23 |
| `MATERIAL_UNCERTAINTY` | 5 |
| `PARTIAL_EVIDENCE` | 3 |
| `SOURCE_REPORTED_UNVERIFIED` | 12575 |
| `VERIFIED_NOT_PLAYED` | 101 |

The 23 remaining full-fact corroborations and three partial candidates are not a claim to exhaustive legal finality. The five material holdouts have their prior full/partial fact status preserved separately. No dataset-wide historical certification is claimed.

## Coverage gaps and compliant recovery

| Candidate source | What the bounded inspection established | Permission / acquisition limit |
|---|---|---|
| [L’Équipe 1994/95](https://www.lequipe.fr/Football/d1/saison-1994-1995/page-calendrier-resultats) | Search index exposes dated 38th-round results. Direct fetch returned cache miss; complete 380-fixture date coverage was not established. | Applicable export/automation/redistribution and model-training grant not verified. Ask publisher for a permitted method or export before acquisition. |
| [RSSSF France 1994/95](https://www.rsssf.org/tablesf/fran95.html) | Directly inspected top-division section is final standings, not a complete dated league-fixture record. Later cup sections are not substitute league fixtures. Page update: 2006-06-05. | Footer permits copying with RSSSF acknowledgement and reserves rights. This is not a verified specific model-training clearance, and the required data is not established on this page. |
| [Deux-Zéro supplied matchday page](https://www.deux-zero.com/ligue-1/resultats/edition/1994-1995/journee/1150) | Exact page fetch returned cache miss. Earlier indexed one-club archive shows explicit dates but does not establish complete 380-fixture coverage, independence or accuracy. | Access/export, redistribution and training conditions remain unverified. Seek owner-approved export or bounded access; no scraping or bypass attempted. |

The concrete next gap-recovery step requires **separate authorization**: first obtain the relevant owner's permitted access/reuse terms, then acquire a small explicit-date feasibility sample, validate it against independent event evidence, and approve complete acquisition only after completeness/date/provenance/rights checks. No permission inquiry was sent and no additional dataset downloaded. RSSSF standings and inferred round dates cannot silently fill the gap.

The missing Nantes–Toulouse 2006/07 source pairing remains absent. Existing [court evidence](https://www.legifrance.gouv.fr/ceta/id/CETATEXT000019427811) establishes penalty winner/points, appeal and homologation but not the numerical awarded score. Request the original LFP 25 May 2007 registration and FFF 12 June appeal text before separately approving any supplemental scored record. Three points are not three goals.

The target remains 36 seasons, with **1994/95's expected 380 fixtures and the one 2006/07 pairing still open**. Neither successful policy reconciliation nor later standardization of the acquired subset completes full historical acquisition. Technical usability, historical confidence, redistribution and model-training authorization remain separate classifications. Existing source-specific licensing limitations remain unchanged.

## Season-level provisional accounting

| Season | Candidates | Administrative/date HOLD OUT | Not played | Original observations |
|---|---:|---:|---:|---:|
| 1990/1991 | 380 | 0 | 0 | 380 |
| 1991/1992 | 380 | 0 | 0 | 380 |
| 1992/1993 | 380 | 0 | 0 | 380 |
| 1993/1994 | 380 | 0 | 0 | 380 |
| 1995/1996 | 380 | 0 | 0 | 380 |
| 1996/1997 | 379 | 1 | 0 | 380 |
| 1997/1998 | 306 | 0 | 0 | 306 |
| 1998/1999 | 306 | 0 | 0 | 306 |
| 1999/2000 | 306 | 0 | 0 | 306 |
| 2000/2001 | 306 | 0 | 0 | 306 |
| 2001/2002 | 306 | 0 | 0 | 306 |
| 2002/2003 | 380 | 0 | 0 | 380 |
| 2003/2004 | 380 | 0 | 0 | 380 |
| 2004/2005 | 380 | 0 | 0 | 380 |
| 2005/2006 | 380 | 0 | 0 | 380 |
| 2006/2007 | 379 | 0 | 0 | 379 |
| 2007/2008 | 380 | 0 | 0 | 380 |
| 2008/2009 | 380 | 0 | 0 | 380 |
| 2009/2010 | 380 | 0 | 0 | 380 |
| 2010/2011 | 380 | 0 | 0 | 380 |
| 2011/2012 | 380 | 0 | 0 | 380 |
| 2012/2013 | 380 | 0 | 0 | 380 |
| 2013/2014 | 379 | 1 | 0 | 380 |
| 2014/2015 | 380 | 0 | 0 | 380 |
| 2015/2016 | 380 | 0 | 0 | 380 |
| 2016/2017 | 379 | 1 | 0 | 380 |
| 2017/2018 | 380 | 0 | 0 | 380 |
| 2018/2019 | 380 | 0 | 0 | 380 |
| 2019/2020 | 279 | 0 | 101 | 380 |
| 2020/2021 | 380 | 0 | 0 | 380 |
| 2021/2022 | 380 | 0 | 0 | 380 |
| 2022/2023 | 380 | 0 | 0 | 380 |
| 2023/2024 | 306 | 0 | 0 | 306 |
| 2024/2025 | 305 | 1 | 0 | 306 |
| 2025/2026 | 305 | 1 | 0 | 306 |

1994/95 has zero acquired observations and remains outside the table, not a zero-match historical season. The 2006/07 source count is 379; no fictional 380th observation was created.

## Reproduction, verification and preservation

New public files: `scripts/decide_ligue1_policy.py`, `tests/test_ligue1_policy.py`, and this document. `PLANNING_LOG.md` is appended only. Existing Phase 2–5 public documents/scripts/tests and private evidence are frozen by the Phase 6 baseline, including the complete Phase 5 ledger and test evidence.

Ignored private additions under `data/private/france/ligue_1/` are `phase6_protected_before.json`, `phase6_decision_policy.json`, `phase6_policy_assessment.json`, `phase6_reproducibility.json`, test XML/log/verification receipt and final preservation receipt. No full audit archive or standardized CSV is among them.

From repository root, with the working existing Python environment and no network:

```sh
python -B -m scripts.decide_ligue1_policy --check
python -B -m scripts.decide_ligue1_policy --write --output-directory /tmp/new-ligue1-policy-check
```

`--init` is first-run baseline creation and is not needed for routine reproduction. The writer accepts identical existing outputs and refuses to overwrite changed output bytes. Use a fresh temporary output directory for byte comparisons. The public evaluator regenerates the expected registry before applying it; do not bypass it with the internal per-record function or a standalone numeric-outcome helper.

An independent Python process regenerated both outputs into a temporary directory and compared each byte and SHA-256. It also regenerated the frozen Phase 5 evidence check unchanged. Recursive preservation passed for 558 private files from eight completed competitions, 165 tracked public files, and **113 frozen Phase 2–5 entries** (along with nested earlier baselines). Originals, receipts, prior assessments and evidence remain byte-identical.

| Artifact | Bytes | SHA-256 | Result |
|---|---:|---|---|
| `phase6_decision_policy.json` | 655217 | `c04e6890ddfb8624446fef19b8fde1a3696e80e2973ca399ea5fe34a5f95f605` | Byte-identical |
| `phase6_policy_assessment.json` | 1075130 | `19067ea72e21f0e45e130b74224b4aec13704249329dfe76f60d97f9bda51e9b` | Byte-identical |

Final repository tests: **1,267 passed**, zero failures/errors/skips; this includes **192 focused Ligue 1 tests, 57 new Phase 6 synthetic tests, six app tests and one launcher test**. The original `.venv` was not changed. The established offline temporary Python 3.13.12 environment (pytest 9.1.1, pandas 3.0.6) was reused with disabled bytecode/project-cache writes, test caches/output in temporary locations and a 180-second timeout. Final run completed in 13.60 seconds (pytest 12.88 seconds). No environment rebuild, install or dependency upgrade occurred.

The tests cover home/draw/away interpretation, defective labels, missing/inconsistent goals, awarded outcomes, cancellation semantics, all named holdouts/replays, disputed dates, season/source-bound identities, unverified ordinary/long-round candidacy, positive new conflicts, registry/source/evidence mutations, same-day/unknown chronology and independent rights/availability gates. Privacy checks confirm the new private files are ignored, no private data is tracked/staged, HEAD/index are unchanged, and known `.DS_Store` files remain untracked. Application and promotional files were not changed.

## Prerequisites for Phase 7

Review and approve the seven named decisions, all 101 not-played entries, numeric interpretation, Brest season rule, conservative holdouts and provisional 12,601-candidate subset. Resolve any requested changes through new evidence-backed, source-bound decisions rather than runtime waivers. Keep incomplete historical scope explicit; obtain separate acquisition approval before attempting gap recovery. Then authorize Phase 7 standardization of the explicitly bounded acquired subset, preserving all original/audit metadata and the five holdouts separately. Training/redistribution clearance is still a separate requirement, not granted by Phase 7 approval.

Stopped after Phase 6. No acquisition, standardized output, model training, staging, commit, push or merge performed.
