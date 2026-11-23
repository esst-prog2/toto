# Primeira Liga — Phase 6 provisional source and fixture policy

Date: 2026-11-23. Approved by the user for Phase 6 only. Branch `feature/data-collection`; protected HEAD `0bb6f393c89fdcc37a52a56bb31e458ff131de47`.

## Scope and source selection

This phase creates processing metadata and a provisional screened population. It does not create the final eight-column CSV or Phase 7 audit archive. Original values and frozen Phase 2–5 evidence remain unchanged. Candidate inclusion is separate from structural validity, independent historical corroboration, administrative finality, chronological eligibility and usage permission.

The complete research objective remains 1990/91–2025/26. Dated originals cover only 1994/95–2025/26. The four early missing seasons remain a separate 1,298-slot research gap, not HOLD OUT, NOT PLAYED or screened records. RSSSF’s 380 undated 1990/91 result identities are not fabricated into dated fixtures.

Deterministic hierarchy:

1. Historical `jalapic/engsoccerdata/data-raw/portugal.csv`, revision `872c5c354161ace8408f3091b758c6af4cccca94`, is selected for 1994/95–2024/25 (8,958 observations/31 seasons).
2. The pinned OpenFootball `europe/portugal/2025-26_pt1.txt`, revision `63df627f3c87ce71708f016522ea236cf74332c3`, is selected for 2025/26 (306 observations).
3. The seven modern overlapping seasons 2018/19–2024/25 remain nonselected comparators: 2,142 original representations. Exact fixture-bound decisions below modify future interpretations only; no original observation is overwritten.

Rationale: the historical source supplies complete contiguous season inventories and consistent selected-source labels. Independent reconstruction of all 2,142 directed pairing joins confirms identical scores and only the two reviewed Santa Clara date disagreements. OpenFootball supplies the sole acquired 2025/26 dated inventory. The hierarchy therefore has measured source-identity and completeness support, not merely convenience; it does not assert historical independence, blanket accuracy superiority, legal identity equivalence or licensing clearance.

## Complete disposition reconciliation

| Accounting level | Total | Completed-result candidate | HOLD OUT | NOT PLAYED | Other exclusions |
|---|---:|---:|---:|---:|---:|
| Unique sourced fixtures | 9,264 | 9,262 | 2 | 0 | 0 |
| Original source observations | 11,406 | 11,403 | 3 | 0 | 0 |

8,958 historical + 2,448 modern = 11,406 original observations. Exactly 9,264 selected observations + 2,142 retained comparator representations account for every original. Exactly one provisional decision exists per sourced fixture. No original disappears and no comparator becomes a second result. Counts were calculated from all decisions; the completed-result count was not forced to 9,264 or a presumed HOLD OUT count.

| Season | Original fixture slots | Completed-result candidates | HOLD OUT | NOT PLAYED |
|---|---:|---:|---:|---:|
| 1994/1995 | 306 | 306 | 0 | 0 |
| 1995/1996 | 306 | 305 | 1 | 0 |
| 1996/1997 | 306 | 306 | 0 | 0 |
| 1997/1998 | 306 | 306 | 0 | 0 |
| 1998/1999 | 306 | 306 | 0 | 0 |
| 1999/2000 | 306 | 306 | 0 | 0 |
| 2000/2001 | 306 | 306 | 0 | 0 |
| 2001/2002 | 306 | 306 | 0 | 0 |
| 2002/2003 | 306 | 306 | 0 | 0 |
| 2003/2004 | 306 | 306 | 0 | 0 |
| 2004/2005 | 306 | 306 | 0 | 0 |
| 2005/2006 | 306 | 306 | 0 | 0 |
| 2006/2007 | 240 | 240 | 0 | 0 |
| 2007/2008 | 240 | 240 | 0 | 0 |
| 2008/2009 | 240 | 240 | 0 | 0 |
| 2009/2010 | 240 | 240 | 0 | 0 |
| 2010/2011 | 240 | 240 | 0 | 0 |
| 2011/2012 | 240 | 240 | 0 | 0 |
| 2012/2013 | 240 | 240 | 0 | 0 |
| 2013/2014 | 240 | 240 | 0 | 0 |
| 2014/2015 | 306 | 306 | 0 | 0 |
| 2015/2016 | 306 | 306 | 0 | 0 |
| 2016/2017 | 306 | 306 | 0 | 0 |
| 2017/2018 | 306 | 306 | 0 | 0 |
| 2018/2019 | 306 | 306 | 0 | 0 |
| 2019/2020 | 306 | 306 | 0 | 0 |
| 2020/2021 | 306 | 306 | 0 | 0 |
| 2021/2022 | 306 | 305 | 1 | 0 |
| 2022/2023 | 306 | 306 | 0 | 0 |
| 2023/2024 | 306 | 306 | 0 | 0 |
| 2024/2025 | 306 | 306 | 0 | 0 |
| 2025/2026 | 306 | 306 | 0 | 0 |

All32 season-level directed home/away pair sets were independently checked after the one approved Feirense interpretation, including the original slots of HOLD OUT fixtures. Expected club counts are 16 for2006/07–2013/14 and18 otherwise. These are structural pair checks, not independent certification of every historical outcome.

## Seven exact exception decisions

| Policy | Disposition | Future interpreted date/score/label | Reason and retained uncertainty |
|---|---|---|---|
| SANTA_PACOS | COMPLETED_RESULT_CANDIDATE | 2020-02-02, 2–1 | Direct contemporary report describes a victory “today”, with Feb2 article context and completed-match narrative; not publication metadata alone. Historical Feb1 and modern Feb2 stay immutable. Feb1 is only an unverified reported scheduling interpretation, not established actual kickoff. No inspected later score-changing decision was established. Known protest finality remains unresolved, so chronological consumption is blocked. |
| SANTA_BENFICA | COMPLETED_RESULT_CANDIDATE | 2021-01-04, 1–1 | Direct report establishes Sunday start/Monday completion. Jan3 kickoff/interruption and Jan4 completion/resumption remain distinct. No invented publication timestamp. |
| BELENENSES_BENFICA | HOLD_OUT | No approved standardized values | The event was played but abnormally terminated. Both originals’0–7 agreement cannot establish formally recognized final result, disciplinary finality, appeals or defensible availability. Restricted FPF material remains uninspected. Not NOT_PLAYED. |
| FEIRENSE_NACIONAL | COMPLETED_RESULT_CANDIDATE | 2011-08-14, 0–0; only `Feirense ` → `Feirense` on exact CSV line4877 | Single-record interpretation supported by contemporary fixture identity and restoration from17 literal labels/32 apparent missing pairs to16 clubs/zero missing pairs/zero duplicates. Original space remains in provenance. No global trim; documentary confidence remains partial. |
| BENFICA_SALGUEIROS | HOLD_OUT | No approved date | CSV1995-08-20 versus fan archive1995-09-06 remains a material date contradiction. Direct fan archive and indexed contemporary pre-match newspaper are not authoritative completed-match confirmation. No further download or forced source preference was used; neither date is adopted. |
| NACIONAL_BENFICA | COMPLETED_RESULT_CANDIDATE | 2024-12-19, 0–2 | Historical CSV line8779 and modern line230 both already record Dec19. Direct club match centre preserves Oct6 fog interruption, restart after eight minutes, and Dec19 completion. No fictitious source-date correction; no score supplement. |
| LEIRIA_FEIRENSE | COMPLETED_RESULT_CANDIDATE | 2012-04-29, 0–4 | Direct contemporary RTP/Lusa reporting supports a played match with eight Leiria starters during strike. No administrative award is invented. Availability is not independently promoted from source date; the chronology gate remains closed. |

The two HOLD OUTs are exactly Benfica–Salgueiros1995/96 (one original) and Belenenses SAD–Benfica2021/22 (two originals). They remain in source/fixture registries. No early unsourced slot is counted as a HOLD OUT.

Santa Clara–Paços distinction: a completed-result candidate here represents the defensibly documented on-field2–1 and completion date. It is not a declaration that the protest is final. Its explicit `unresolved_administration=true` keeps chronological use blocked even though it is retained in the provisional historical screening population. No late administrative score change is asserted absent inspected evidence. This is a deliberate separation of candidate screening from availability/legal-consumption clearance.

Belenenses distinctions: raw score0–7 is preserved; start date2021-11-27 is retained; precise termination chronology, regulatory completion, official homologation/finality, decision publication and appeal closure are not promoted to verified facts from indexed documents. Nothing in the policy invents a replacement score or legally final timestamp.

Exact policy identities and source/evidence bindings:

### SANTA_PACOS

Stable provisional fixture ID: `2670b3156d51618e955ca4f59a949eaf68ddfb3d8748f869f6a08ecbc8642e65`. Decision ID: `PT-P6-SANTA_PACOS-2670b3156d51618e955ca4f59a949eaf68ddfb3d8748f869f6a08ecbc8642e65`.

- `33862b4501af82fe70d76532a67a228dee8f326b6136ba54ef3dba90d8bab0a2`: `jalapic/engsoccerdata/data-raw/portugal.csv`, physical line7290, 2020-02-01, home `Santa Clara`, away `Pacos Ferreira`, FT`2-1`; SHA-256`75ab6c755bd04d33b803c5655d83822a76c1ac19223b547568467273c4083857`. Role: SELECTED.
- `87d755690d6f59d64062dcec4f832c2ff220c3b65ce50ef518daaac10fbfecb8`: `openfootball/europe/portugal/2019-20_pt1.txt`, physical line298, 2020-02-02, home `CD Santa Clara`, away `Paços de Ferreira`, FT`2-1`; SHA-256`0e57f8019ed50e449428fec2cad7fa8eb35bd868cbcbc7356eae4af9b678e013`. Role: COMPARATOR_RETAINED.

Evidence: [Santa Clara 2- 1 Paços de Ferreira, veja as estatísticas ](https://www.rtp.pt/noticias/desporto/santa-clara-2-1-pacos-de-ferreira-veja-as-estatisticas_e1202367) — DIRECT_DOCUMENT; snapshot integrity retained in frozen Phase5 index. Direct completed-match reporting supports February2 and unchanged2-1; historical February1 remains preserved. No inspected evidence establishes a changed result. Candidate represents played result; known protest finality is not established, so chronology use remains blocked.

### BENFICA_SALGUEIROS

Stable provisional fixture ID: `506ea92837a3c91f4e50a239830c95fc5dcad5d05273b7935ecca85e622e6471`. Decision ID: `PT-P6-BENFICA_SALGUEIROS-506ea92837a3c91f4e50a239830c95fc5dcad5d05273b7935ecca85e622e6471`.

- `2675bb5e1717d5c4f907df689ded4a41889858974d19d18892a3035cb827570a`: `jalapic/engsoccerdata/data-raw/portugal.csv`, physical line308, 1995-08-20, home `Benfica`, away `Salgueiros`, FT`0-0`; SHA-256`75ab6c755bd04d33b803c5655d83822a76c1ac19223b547568467273c4083857`. Role: SELECTED.

Evidence: [SL Benfica 0 - 0 SC Salgueiros, Campeonato Nacional 1995/1996 / Serbenfiquista.com ](https://serbenfiquista.com/jogo/futebol/masculino/seniores/19951996/campeonato-nacional/1995-09-06/sl-benfica-salgueiros) — DIRECT_DOCUMENT; snapshot integrity retained in frozen Phase5 index. CSV August20 and direct fan archive September6 conflict. Indexed contemporary preview is not directly inspected completion evidence. Neither date selected.

### SANTA_BENFICA

Stable provisional fixture ID: `52c7368dffa4b73d69c041310be3ec2cda42ff10994e0b48d98b9182c2d99f7c`. Decision ID: `PT-P6-SANTA_BENFICA-52c7368dffa4b73d69c041310be3ec2cda42ff10994e0b48d98b9182c2d99f7c`.

- `07e7ee52db6b6ec435b234243d03e1ab9fb89b4cd4e4571aa587e7e06c1be69d`: `jalapic/engsoccerdata/data-raw/portugal.csv`, physical line7532, 2021-01-03, home `Santa Clara`, away `Benfica`, FT`1-1`; SHA-256`75ab6c755bd04d33b803c5655d83822a76c1ac19223b547568467273c4083857`. Role: SELECTED.
- `7d350c9a6179c225329dbe7c3ec85aede0f7d538a0d8b53e9ef3fe4d26828c26`: `openfootball/europe/portugal/2020-21_pt1.txt`, physical line192, 2021-01-04, home `CD Santa Clara`, away `SL Benfica`, FT`1-1`; SHA-256`381113f27961277c23f9bbc27543a263f6459236860cc3b9c0698e547ab64b12`. Role: COMPARATOR_RETAINED.

Evidence: [I Liga em direto. Santa Clara - SL Benfica ](https://www.rtp.pt/noticias/mundo/i-liga-em-direto-santa-clara-sl-benfica_e1286708) — DIRECT_DOCUMENT; snapshot integrity retained in frozen Phase5 index. Direct completion narrative supports unchanged score on approved completion day; interrupted kickoff preserved separately. No material contradictory final-result evidence identified; no invented publication timestamp.

### BELENENSES_BENFICA

Stable provisional fixture ID: `590de1a604f7ce5ee00f775655831b47f65771ab296be77ca2feb0e7ebb93d82`. Decision ID: `PT-P6-BELENENSES_BENFICA-590de1a604f7ce5ee00f775655831b47f65771ab296be77ca2feb0e7ebb93d82`.

- `26b0148abfd2b370cf6d06a838a61f067cb93ddbeb693a132e5fdc73a08f74bc`: `jalapic/engsoccerdata/data-raw/portugal.csv`, physical line7838, 2021-11-27, home `Belenenses`, away `Benfica`, FT`0-7`; SHA-256`75ab6c755bd04d33b803c5655d83822a76c1ac19223b547568467273c4083857`. Role: SELECTED.
- `422e5675208bd540a079b9a9cd94eb773db0e3efc128ed42b4da1f69480ddb9f`: `openfootball/europe/portugal/2021-22_pt1.txt`, physical line187, 2021-11-27, home `Belenenses SAD`, away `SL Benfica`, FT`0-7`; SHA-256`5e5593b409d4b4ca31782960897b4e40917cc55370101cd68fea1af51a2a3b1c`. Role: COMPARATOR_RETAINED.

Evidence: [FPF referee-report lead Belenenses-Benfica ](https://www.fpf.pt/DownloadDocument.ashx?id=21435) — INDEX_ONLY; snapshot integrity retained in frozen Phase5 index. Played but abnormally terminated event: recorded 0-7 is not verified administrative finality. Official FPF documents remain restricted; recognized final score, appeal/finality and availability not established. Not NOT_PLAYED.

### FEIRENSE_NACIONAL

Stable provisional fixture ID: `6be498676b5c4719b6b9629afd6d8be9ec31c5408d8d1f0b0b283c818d5a50b5`. Decision ID: `PT-P6-FEIRENSE_NACIONAL-6be498676b5c4719b6b9629afd6d8be9ec31c5408d8d1f0b0b283c818d5a50b5`.

- `5265c556cbad744e664ed5f55bec58e0117a48b279d3ef3aa1f435b2753aa25b`: `jalapic/engsoccerdata/data-raw/portugal.csv`, physical line4877, 2011-08-14, home `Feirense `, away `Nacional`, FT`0-0`; SHA-256`75ab6c755bd04d33b803c5655d83822a76c1ac19223b547568467273c4083857`. Role: SELECTED.

Evidence: [Krónikas Feirenses: agosto 2011 ](https://23kronikasfeirenses.blogspot.com/2011/08/) — DIRECT_DOCUMENT; snapshot integrity retained in frozen Phase5 index. Only the exact line4877/audit-ID interpretation Feirense<space>→Feirense is approved: one isolated whitespace defect, direct contemporary fixture identity and season pairing restoration. Original literal remains unchanged; no global trim.

### NACIONAL_BENFICA

Stable provisional fixture ID: `96148395ec97843379452bf5db49e553984816555b317fa57baafde0b4cb67c8`. Decision ID: `PT-P6-NACIONAL_BENFICA-96148395ec97843379452bf5db49e553984816555b317fa57baafde0b4cb67c8`.

- `04a240ec3a2d9e77cceec3b782bc854f068b27feadd4e46ecf09168c44ccb3b9`: `jalapic/engsoccerdata/data-raw/portugal.csv`, physical line8779, 2024-12-19, home `Nacional`, away `Benfica`, FT`0-2`; SHA-256`75ab6c755bd04d33b803c5655d83822a76c1ac19223b547568467273c4083857`. Role: SELECTED.
- `7a4a507f2e90976518ac3037c1d5d8f5ae433b521d1a6f17b4d4f05bd885272d`: `openfootball/europe/portugal/2024-25_pt1.txt`, physical line230, 2024-12-19, home `CD Nacional`, away `Sport Lisboa e Benfica`, FT`0-2`; SHA-256`3bb1acda8822a01e1aef1e70f03607650b97fb6722fd0d777f2ef9bf6544ed6c`. Role: COMPARATOR_RETAINED.

Evidence: [Direto CD Nacional - SL Benfica 19 dezembro 2024 - SL Benfica ](https://www.slbenfica.pt/pt-pt/futebol/match-center/nacional-benfica-19-dezembro-2024) — DIRECT_DOCUMENT; snapshot integrity retained in frozen Phase5 index. Direct completion narrative supports unchanged score on approved completion day; interrupted kickoff preserved separately. No material contradictory final-result evidence identified; no invented publication timestamp.

### LEIRIA_FEIRENSE

Stable provisional fixture ID: `ad0f1d83cff70c1fdf03539626df3ce45ad342b43349e0711c12e1d95ce02e24`. Decision ID: `PT-P6-LEIRIA_FEIRENSE-ad0f1d83cff70c1fdf03539626df3ce45ad342b43349e0711c12e1d95ce02e24`.

- `187a370c18418bea735c0a27add3d826c1cc8e01ba6af2d2ee9524bfafed2cbd`: `jalapic/engsoccerdata/data-raw/portugal.csv`, physical line5094, 2012-04-29, home `Leiria`, away `Feirense`, FT`0-4`; SHA-256`75ab6c755bd04d33b803c5655d83822a76c1ac19223b547568467273c4083857`. Role: SELECTED.

Evidence: [União de Leiria - com oito - perdeu "apenas" por 4-0 ](https://www.rtp.pt/noticias/feirense/uniao-de-leiria-com-oito-perdeu-apenas-por-4-0_d549225) — DIRECT_DOCUMENT; snapshot integrity retained in frozen Phase5 index. Direct contemporary report supports actual 0-4 with eight Leiria starters. Unusual participation is not an awarded score. First defensible availability not separately certified.

## Scheduling, confidence and unusual results

All207 Phase4 flagged observations and392 Phase5 reviewed originals remain source-bound. Their original classifications remain25 full core,11 partial,3 contradicted,45 unresolved and308 context-only. Evidence classifications do not automatically determine dispositions. The18 wide-round contexts/162 memberships and13 reversal contexts/26 endpoints retain their complete original assessments. File-order reversal is not necessarily an actual chronology error, and a context-level explanation does not certify every fixture.

All26 unusual-score original memberships (18 conditional events) remain visible. The exception registry includes18 unique unusual-score decision references. Large margins, partial research, unknown upstream independence or absence of individual documentary confirmation do not automatically cause exclusions. Source annotations or new material conflicts without an explicit policy fail closed rather than being silently accepted.

Portugal2019/20 retains all306 sourced scored fixtures as completed-result candidates, with match-specific chronology restrictions preserved. No Dutch cancellation policy is copied, no NOT_PLAYED slots invented, and no blank/unplayed scores are present in this approved dated population. The general restart history does not independently certify every result or timestamp.

## Club and source identity limits

The2,142 source-to-source correspondences were reconstructed using complete season-bound literal-label bijections and exact directed pairings, then matched against frozen source IDs. All scores agree and only the two documented date conflicts occur. Approval is restricted to those exact representations of fixtures in those seven seasons. It is not a reusable cross-season alias dictionary or a legal entity merger.

Original labels and source paths remain in every observation registry entry. Selected historical labels are retained except the one Feirense occurrence. Source-local or season-local representations of Belenenses do not erase the CF Os Belenenses/professional SAD split. Benfica/BenficaB, Porto/PortoB, Sporting/SportingB, Vitória SC/FC and AVS/Aves are not merged. Gil Vicente, Boavista and Leiria administrative/organizational history is preserved as contextual evidence, not blanket score awards or global club continuity. Global aliases remain empty.

Provisional fixture IDs are stable policy identities based on competition, season and selected original participant labels; they are not the final shared-schema match IDs. They do not imply globally approved club identities. Future standardization must retain policy-to-source traceability.

## Fail-closed chronological eligibility

`PredictionGate` rebuilds the source-bound expected policies, rechecks frozen source/evidence fingerprints and compares every saved policy artifact byte-for-byte before accepting any decision. It rejects missing, incomplete or tampered registries, unknown fixture IDs, modified source bindings and changed decision values. A caller cannot gain eligibility by flipping a flag on a saved decision.

The day-level gate requires a completed-result candidate with no known unresolved administrative outcome, known actual completion and independently defensible availability day, and completion ≤ availability < prediction day. Therefore same-day results are rejected, even if an article contains a clock time. No intraday timestamp is invented or approved. Future results, unknown completion/availability, HOLD OUTs and unapproved supplemental-result interpretations fail closed. Source-date proxies never count as verified availability.

Three specific completion-day interpretations exist: the two Santa Clara cases and Nacional–Benfica. Santa Clara–Paços additionally has an administrative/protest guard and fails eligibility. At the diagnostic late cutoff used during verification, only Santa Clara–Benfica and Nacional–Benfica pass the chronological day gate. This is not permission to train, evaluate or integrate them. All9,264 policy decisions retain training suitability/permission and redistribution permission as NOT_CLEARED. All model-training checks return false.

Ordinary candidates, including directly sampled or high-scoring matches, do not acquire result-availability certification automatically. Leiria has documentary completion context but no approved availability day. A future consumer must load and validate these policy registries and establish any required chronology and rights; the eventual eight-column CSV alone is not leakage-safe.

## Artifacts and offline reproduction

New public files: `scripts/decide_primeira_liga_policy.py`, `tests/test_primeira_liga_policy.py`, this report. `PLANNING_LOG.md` receives append-only Phase6 decisions/results. All earlier Portuguese scripts/tests/docs remain unchanged.

Private inputs: `phase6_protected_before.json` (317 protected entries plus original planning prefix), `phase6_approval_receipt.json` (exact request hash). Seven deterministic policy outputs:

- `phase6_source_observation_policy.json`
- `phase6_unique_fixture_policy.json`
- `phase6_source_selection_registry.json`
- `phase6_exception_registry.json`
- `phase6_chronology_registry.json`
- `phase6_policy_summary.json`
- `phase6_policy_manifest.json`

The observation registry retains all11,406 originals with selected/comparator role and unique decision references. The fixture registry contains exactly9,264 provisional decisions with source bindings and evidence. The selection registry retains all2,142 approved exact overlap links. The exception registry retains the seven exact decisions, unusual-score references, all31 scheduling contexts and Phase5 identity/COVID findings. The chronology registry contains one record per fixture. The manifest hashes all six other outputs, the approved inputs and the public policy implementation; it does not self-hash. None is the Phase7 final audit archive or a CSV.

Additional private verification: `phase6_independent_regeneration.json`, `phase6_test_summary.json`, `phase6_final_verification.json`, and `verification_phase6/` logs/XML. Preliminary Phase6 curation files under `phase6_initial_working_draft/` are explicitly superseded, excluded from downstream inputs, and remain private; frozen Phase2–5 artifacts were never rewritten.

Offline regeneration into safe temporary storage:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. "$VERIFICATION_PYTHON" -B scripts/decide_primeira_liga_policy.py --output-directory "$TEMP_POLICY_DIR"
```

Use the existing external Python3.13.12 verification environment and preserved private inputs. No package installation, original `.venv` execution or live web access is required. Compare every temporary output with its saved counterpart. Separate-process regeneration succeeded byte-for-byte and by SHA-256 for all seven files:

| Output | Bytes | SHA-256 |
|---|---:|---|
| `phase6_source_observation_policy.json` | 22780457 | `bc788c7a505b2589d579e8951d48a49196ab90f0c22f8564a1a3410dda46253c` |
| `phase6_unique_fixture_policy.json` | 44518198 | `32bfb1fe1917f5f75e691243a63a649759e3dcadc504f5b18741992c66b07b76` |
| `phase6_source_selection_registry.json` | 751658 | `a78adf0f2d305325e0673d9a97eb67776f9f999b7691ec8ec6521fa4dfa03d76` |
| `phase6_exception_registry.json` | 225875 | `6cfba1862732f780703e6c16de2d4c675783f0f8535e48f9de3000e980dc1a64` |
| `phase6_chronology_registry.json` | 9452145 | `e554f8e7817161f3db09c90de7e073336db17a97e1a48451daeef261c9089b44` |
| `phase6_policy_summary.json` | 8511 | `44771a1b322dbb3bc5f4c984a70e8b4d56aaf8881ae1894aff5749d03847dde0` |
| `phase6_policy_manifest.json` | 2261 | `4c72672297279cdc52393bd84056d67375b851ab6e15feccecb2b637f5fa4345` |

Independent checks additionally reparsed the original historical CSV with a separate reader (8,958 rows), re-ran the earlier independent Phase3 raw-source reconciliation, compared every original policy binding, verified all32 interpreted directed pair sets, measured all disposition counts and exercised the real saved-registry prediction gate. No original/generated saved artifact was overwritten during regeneration.

## Fresh tests and preservation

| Test selection (overlapping; never sum) | Passed | Failed | Errors | Skipped |
|---|---:|---:|---:|---:|
| acquisition_importer | 707 | 0 | 0 | 0 |
| app_launcher | 7 | 0 | 0 | 0 |
| focused | 246 | 0 | 0 | 0 |
| full | 2092 | 0 | 0 | 0 |
| non_ui | 2085 | 0 | 0 | 0 |
| policy | 71 | 0 | 0 | 0 |

Fresh complete repository result: **2,092 passed**, versus the2,021 Phase5 baseline. There are71 new focused synthetic policy tests. They cover source windows/pins, all seven overlap seasons, exact exception bindings, restricted/index-only evidence, whitespace scope, played-versus-unplayed distinctions, COVID306 fixtures, club boundaries, source observation accounting, unknown conflicts/annotations, same-day/future/unknown availability, administrative guards, training blocks, tampered registries and deterministic ordering.

Preservation verification protects the eleven previous competitions and all127,927 screened records, including1,037 earlier private files and228 public files. All ten Portuguese originals, frozen Phase2–5 receipts/evidence/output bytes, all earlier public Portuguese code and the planning-log prefix remain unchanged. All private policy/evidence files are ignored and untracked; no private dataset is staged. HEAD/index stay unchanged and only PLANNING_LOG.md is a tracked modification (earlier plus appended work). Application and promotional files were not edited. The original `.venv` was not invoked, installed into or rebuilt; a complete historical bytewise `.venv` baseline was not available, so no stronger environment-forensics claim is made.

## Licensing, open issues and Phase 7 boundary

The engsoccerdata noncommercial/attribution notice and software GPL do not grant universal upstream data-use clearance. OpenFootball CC0 covers rights held and does not establish every upstream permission or independence. RSSSF and documentary publishers retain their own conditions. No training, evaluation, commercial-use or redistribution clearance is inferred from technical access or official hosting. Private originals and audit extracts must remain out of Git.

Outstanding issues: two HOLD OUTs; Santa Clara–Paços protest finality and eligibility guard; ordinary availability proxies; incomplete independent historical coverage; club/legal-entity continuity questions; the four early missing dated seasons; and downstream licensing/model-training restrictions. No new dataset or documentary download was made in Phase6.

Independently verified expected Phase7 scope, only if separately approved:

- 9,262 screened completed-result candidate rows, not automatically training-eligible.
- 9,264 unique sourced fixture entries in a future complete audit archive, including both HOLD OUTs.
- All11,406 original observation references, including2,142 comparators.
- Exact shared schema: `match_id,date,league,season,home_team,away_team,home_goals,away_goals`; canonical league `Primeira Liga`.
- The four early seasons/1,298 unsourced slots remain outside sourced disposition totals.

No final standardized CSV or Phase7 audit archive has been generated. No model training/evaluation, application integration, staging, commit, push, merge or rebase. Stop after Phase6 pending user approval.
