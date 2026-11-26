# Belgian Pro League — Phase 2 bounded feasibility

Measured 2026-11-24. Phase 2 only: seven originals, no screening, final IDs, historical corrections, final dispositions, global aliases or model use. Canonical proposed league: `Belgian Pro League`.

## Starting state and preservation

Original toto worktree, feature/data-collection, HEAD and independently queried origin branch `013bb9c195624d5ac290aeb57dae11c4e21c0b5a`. No initial staged/tracked changes; only .DS_Store and data/.DS_Store untracked. Protected baseline: 1,415 prior private files and 250 public files, plus append-only planning-log prefix and Git index fingerprint. Twelve separately counted prior screened CSVs total 137,189 rows. Originals, application, promotional worktree and original .venv are unchanged. All Belgian originals and assessments are ignored under data/private/belgium/pro_league/.

## Exact seven-original acquisition

All seven acquired with HTTP 200; zero blockers, zero substitutes. Five Git originals independently match approved Git blob SHA-1 and byte size. Complete receipts preserve UTC retrieval time, final URL, HTTP headers, decoder, SHA-256 and rights/source statements. Originals use atomic exclusive publication; partial cache pairs fail closed. Requests are bounded to 30 seconds/8 MB, spaced two seconds, with no redirects or retries. Persistent per-URL stop records prevent retries after access failure. Valid cached replay makes zero network requests and changes no files.

| Original | Bytes | SHA-256 | Git blob |
|---|---:|---|---|
| [data-raw/belgium.csv](https://raw.githubusercontent.com/jalapic/engsoccerdata/872c5c354161ace8408f3091b758c6af4cccca94/data-raw/belgium.csv) | 555878 | `7eb7b3d83da5313834a25592edf0cc2f8ca02c94a4dcf444a344844ab2386021` | `949da4ac0a95ec17ffa883b7b497553c9ec38a96` |
| [2018-19/be1.txt](https://raw.githubusercontent.com/openfootball/belgium/1166d3c9c5725aec01e1bbeaa20f6467e39ddbb8/2018-19/be1.txt) | 22252 | `8a81bb72140d317afb415bbc1bc0d8f318eaf06ebf205235981e988e0e8406f0` | `fd7f187a36a4c4c1389aab3d4a736bb1ca3802ee` |
| [2019-20/be1.txt](https://raw.githubusercontent.com/openfootball/belgium/1166d3c9c5725aec01e1bbeaa20f6467e39ddbb8/2019-20/be1.txt) | 19469 | `0baeba403fcf316f5e65248ec0de258381ede230a038bcf24b326534d01eb10f` | `f1e6e2e6d3684dcf8335efd66473cc54ef2af0c4` |
| [2023-24/be1.txt](https://raw.githubusercontent.com/openfootball/belgium/1166d3c9c5725aec01e1bbeaa20f6467e39ddbb8/2023-24/be1.txt) | 26414 | `700b4a84a5190eeaff538695ef2e632ee6e0544e916e76c1c2b0a5d5609d763b` | `c28e1faff98417df5ff0e72085d4fdbdb3d756eb` |
| [2025-26/be1.txt](https://raw.githubusercontent.com/openfootball/belgium/1166d3c9c5725aec01e1bbeaa20f6467e39ddbb8/2025-26/be1.txt) | 16867 | `06f1504f54b05e4a334b76eb91a4a1799ca13acc7eb659a61d63a107a00e7232` | `dbca2186e03f1a8372902f58eddfa174a2124a22` |
| [tablesb/belg93.html](https://www.rsssf.org/tablesb/belg93.html) | 5531 | `741ab42252840042e61363965535e0c4efb71c8d389e6790989b7e85be2832ae` | `None` |
| [tablesb/belg2010.html](https://www.rsssf.org/tablesb/belg2010.html) | 168329 | `97ce6267fe0fae39258b7c1dab97ba77f0267b432f35c440760ab9024e27ec48` | `None` |

Git pins: jalapic/engsoccerdata `872c5c354161ace8408f3091b758c6af4cccca94`; openfootball/belgium `1166d3c9c5725aec01e1bbeaa20f6467e39ddbb8`. RSSSF pages are mutable snapshots with no Git identity. Historical pinned-tree evidence is referenced from the preserved Portuguese metadata; approved modern path/blob/size identities come from the Phase 1 catalogue and are checked against retrieved bytes. No other season original was requested.

## Historical CSV: measured contents

Exact schema: `Date,Season,home,visitor,FT,hgoal,vgoal,division,tier,totgoal,goaldif,result`. It contains **8,394 scored observations, 30 consecutive season labels, 1995/96–2024/25**. Division is B1 and tier is 1. Dates are ISO YYYY-MM-DD; season is starting year; FT is hgoal-vgoal, totgoal is their sum, goaldif is home minus away and result is H/D/A. All required scores and derived fields agree; zero malformed rows, invalid dates or diagnostic identity duplicates. Original physical CSV line ranges/bytes are bound by SHA-256. All records remain in their original source order.

**1994/95 is absent**, as are 1990/91–1993/94 and 2025/26. The README starting-year claim is not supported by this pinned original; the Belgium-specific 8,394/1995–2024 documentation is numerically correct. Its playoff-exclusion claim is not correct for the entire file.

For 1995/96–2022/23 the observed populations have regular-season-like pairing structure, with the administrative/COVID qualifications below. In 2023/24 and 2024/25 the first 240 observations cover every directed pair once; 72 later observations follow, producing repeated pairings. Those prefixes end 2024-03-17 and 2025-03-16; suffixes run 2024-03-29–06-02 and 2025-03-28–05-25 respectively. These are diagnostic partitions, not approved inclusion decisions. Every CSV source stage remains UNKNOWN because no stage field exists.

2023/24 overlap identifies 240 regular, 30 championship, 29 Europe, 12 playdown and one European-qualification counterpart. Thus extra 72 does not imply a complete 30+30+12 group population. 2024/25 has no acquired modern counterpart and its precise postseason composition remains unresolved.

## Measured 36-season matrix

Nominal counts below are format expectations, not accepted records. H: acquired historical CSV. O: approved acquired OpenFootball sample only. H candidate partition is inferred from pairing prefixes or overlap, never a source stage label. All H observations are scored; all H stage fields remain UNKNOWN. Dates exist for every parsed observation but are not certified result-availability dates. No historical or training eligibility is certified.

| Season | Nominal clubs / slots | H observations / clubs | H provisional regular + later | O regular scored/unscored | O other-stage observations | Gap / exception |
|---|---|---|---|---|---|
| 1990/91 | 18 / 306 | — | — | not sampled | — | No acquired dated source |
| 1991/92 | 18 / 306 | — | — | not sampled | — | No acquired dated source |
| 1992/93 | 18 / 306 | — | — | not sampled | — | No acquired dated source |
| 1993/94 | 18 / 306 | — | — | not sampled | — | No acquired dated source |
| 1994/95 | 18 / 306 | — | — | not sampled | — | No acquired dated source |
| 1995/96 | 18 / 306 | 306 / 18 | 306 + 0 | not sampled | — | Stage/chronology not historically certified |
| 1996/97 | 18 / 306 | 306 / 18 | 306 + 0 | not sampled | — | Stage/chronology not historically certified |
| 1997/98 | 18 / 306 | 306 / 18 | 306 + 0 | not sampled | — | Stage/chronology not historically certified |
| 1998/99 | 18 / 306 | 306 / 18 | 306 + 0 | not sampled | — | Stage/chronology not historically certified |
| 1999/00 | 18 / 306 | 306 / 18 | 306 + 0 | not sampled | — | Stage/chronology not historically certified |
| 2000/01 | 18 / 306 | 306 / 18 | 306 + 0 | not sampled | — | Stage/chronology not historically certified |
| 2001/02 | 18 / 306 | 306 / 18 | 306 + 0 | not sampled | — | Stage/chronology not historically certified |
| 2002/03 | 18 / 306 | 272 / 17 | 272 + 0 | not sampled | — | Lommel absent; 272 observed, not 306 |
| 2003/04 | 18 / 306 | 306 / 18 | 306 + 0 | not sampled | — | Stage/chronology not historically certified |
| 2004/05 | 18 / 306 | 306 / 18 | 306 + 0 | not sampled | — | Stage/chronology not historically certified |
| 2005/06 | 18 / 306 | 306 / 18 | 306 + 0 | not sampled | — | Stage/chronology not historically certified |
| 2006/07 | 18 / 306 | 306 / 18 | 306 + 0 | not sampled | — | Stage/chronology not historically certified |
| 2007/08 | 18 / 306 | 306 / 18 | 306 + 0 | not sampled | — | Stage/chronology not historically certified |
| 2008/09 | 18 / 306 | 306 / 18 | 306 + 0 | not sampled | — | No repeated title-test pairing in H |
| 2009/10 | 16 / 240 | 210 / 15 | 210 + 0 | not sampled | — | Mouscron absent; 210 observed, not 240 |
| 2010/11 | 16 / 240 | 240 / 16 | 240 + 0 | not sampled | — | Stage/chronology not historically certified |
| 2011/12 | 16 / 240 | 240 / 16 | 240 + 0 | not sampled | — | Stage/chronology not historically certified |
| 2012/13 | 16 / 240 | 240 / 16 | 240 + 0 | not sampled | — | Stage/chronology not historically certified |
| 2013/14 | 16 / 240 | 240 / 16 | 240 + 0 | not sampled | — | Stage/chronology not historically certified |
| 2014/15 | 16 / 240 | 240 / 16 | 240 + 0 | not sampled | — | Stage/chronology not historically certified |
| 2015/16 | 16 / 240 | 240 / 16 | 240 + 0 | not sampled | — | Only regular-like H prefix; postseason not represented |
| 2016/17 | 16 / 240 | 240 / 16 | 240 + 0 | not sampled | — | Stage/chronology not historically certified |
| 2017/18 | 16 / 240 | 240 / 16 | 240 + 0 | not sampled | — | Stage/chronology not historically certified |
| 2018/19 | 16 / 240 | 240 / 16 | 240 + 0 | 240/0 | 30 | Stage/chronology not historically certified |
| 2019/20 | 16 / 240 | 232 / 16 | 232 + 0 (overlap) | 232/8 | 0 | H missing 8 directed pairs; O explicitly cancels 8 |
| 2020/21 | 18 / 306 | 306 / 18 | 306 + 0 | not sampled | — | Stage/chronology not historically certified |
| 2021/22 | 18 / 306 | 306 / 18 | 306 + 0 | not sampled | — | Stage/chronology not historically certified |
| 2022/23 | 18 / 306 | 306 / 18 | 306 + 0 | not sampled | — | Stage/chronology not historically certified |
| 2023/24 | 16 / 240 | 312 / 16 | 240 + 72 | 240/0 | 73 | Mixed stages; awarded Europe fixture absent from H |
| 2024/25 | 16 / 240 | 312 / 16 | 240 + 72 | not sampled | — | 72 extra observations; precise stages unresolved |
| 2025/26 | 16 / 240 | — | — | 121/119 | 0 | 121 scored;119 unscored; no postseason sections |

For ordinary historical seasons through 2022/23, all directed pairings among observed clubs exist once, except 2019/20 with eight missing. Administrative 2002/03 and 2009/10 have complete graphs among 17 and 15 retained clubs, which does not establish historical completeness. 2023/24 and 2024/25 each have 72 repeated directed-pair groups; no extra observation was dropped. Each full modern regular-season schedule covers 240 directed pairings with 16 clubs; none are missing as source slots.

## Historical sample and administrative limits

- Earliest: 1995/96, 306 scored rows, 18 clubs, complete directed pairings, dates 1995-08-04–1996-05-12. No early-1990s gap is filled.
- 2002/03: 272 scored rows and 17 clubs; no Lommel label or annulment metadata in the CSV. Nominal 306, final-table implication 272 and actual played/annulled/awarded populations are separate. The source cannot reconstruct the removed Lommel events. No new 2002/03 documentary original was acquired.
- 2008/09: 306 rows, 18 clubs, each directed pair once, last date 2009-05-16. The documented later title test is not represented as an additional pairing.
- 2009/10: 210 scored rows, 15 clubs; Mouscron absent. RSSSF preserves a different observation population including annulled, awarded and unplayed fixtures. Do not turn 210 into an approved screened count.
- 2015/16: 240 scored rows, 16 clubs; the CSV has no playoff/relegation-stage markers.
- 2018/19: H 240 versus O 270; the additional 30 O records are explicitly Playoff I. European/mixed-tier playoffs and qualification ties are not present in this O original.
- 2019/20: H 232 scored observations, missing eight directed pairings. O has 232 scored plus eight unscored records explicitly annotated [cancelled], all round 30 with source heading 2020-03-15. This is scheduled context, not completion or final-decision dating. No final NOT PLAYED policy was assigned. Both scored sources end 2020-03-07.
- 2020/21: 306 scored H observations, 18 clubs; all directed pairings once.
- 2024/25: 312 scored H observations, 16 clubs; 240-pair prefix plus 72 later observations, not a verified regular-only original.

## OpenFootball stage grammar and measurements

A title is required. `▪ Matchday N` and `▪ N. Round` explicitly identify the regular sequence in these originals; `▪ Playoff I, Matchday N`, `▪ Championship, Matchday N`, `▪ Europe, Matchday N`, `▪ Relegation, Matchday N` and `▪ ECL Playoff, Final` identify separate stages. Day/month headings inherit a season year only when the weekday and season window resolve it uniquely; the source heading line and original text are retained. Unknown grammar fails explicitly. Comments are checked against measured fixture counts, not used to force them.

| Season | All | Scored | Unscored | Regular | Championship | Europe | Playdowns | Europe qualifier |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2018/19 | 270 | 270 | 0 | 240 | 30 | 0 | 0 | 0 |
| 2019/20 | 240 | 232 | 8 | 240 | 0 | 0 | 0 | 0 |
| 2023/24 | 313 | 313 | 0 | 240 | 30 | 30 | 12 | 1 |
| 2025/26 | 240 | 121 | 119 | 240 | 0 | 0 | 0 | 0 |

2025/26 is an incomplete results snapshot: 121 scores through 2025-11-28 and 119 unscored slots; its schedule runs to 2026-03-21. No cancellation annotations or postseason sections occur. Do not supplement it or infer that absent playoffs were not played.

Four wide-round flags (>14 days) are preserved, covering 32 distinct source fixture observations: 2019/20 round 5 (159 days), round 23 (18 days), 2023/24 round 5 (33 days), 2025/26 round 5 (32 days). Long spans are review candidates, not errors. All modern observations have usable source-date context. No interruption/completion or administrative-finality date is certified.

## Historical-modern overlap

Candidate label correspondences are derived separately per season using date/side/score participation signatures (minimum 80% containment agreement, unique best match and one-to-one labels). This is a diagnostic aid, not an identity policy or an independent historical check. Event comparison uses mapped pair plus date to distinguish rematches; a unique remaining single pair may expose a date conflict. Ambiguities/unmatched records remain visible. Original labels, scores, dates and UNKNOWN historical stages are never rewritten.

| Season | H | O | Candidate matches | Date conflicts | Score conflicts | Unmatched H / O |
|---|---:|---:|---:|---:|---:|---|
| 2018/19 | 240 | 270 | 240 regular | 0 | 0 | 0 / 30 championship |
| 2019/20 | 232 | 240 | 232 regular | 0 | 0 | 0 / 8 cancelled slots |
| 2023/24 | 312 | 313 | 312 across stages | 0 | 0 | 0 / 1 awarded Europe fixture |
| 2025/26 | 0 | 240 | No H overlap | — | — | Not comparable |

The unmatched 2023/24 O observation is Standard Liège–KVC Westerlo, 2024-05-10, source score 0-5 [awarded], Europe round 8, physical line 573. Preserve it unchanged for later independent administrative/finality review. An unmatched observation is not a conflicting matched result. No award was substituted into the CSV.

All three overlap years have 16 one-to-one diagnostic label candidates. Typical literal differences include Club Brugge/Club Brugge KV, Gent/KAA Gent, Standard/Standard Liège, St Truiden/Sint-Truidense VV and Charleroi/Sporting Charleroi. Mouscron/Royal Excel Mouscron correspondence in an overlap year must not merge the earlier Excelsior entity. Germinal, Mouscron-Peruwelz, Beerschot VA and Molenbeek remain separate historical labels. Brugge clubs remain distinct. RSCA Futures and Genk predecessor labels are not introduced by inference. No global aliases, reserve-team merger or legal continuity assumption was applied.

## RSSSF documentary capability and attribution

**1992/93:** 18 first-division standings rows with 34 games each; no full 306-event list, individual fixture dates, fixture-result cross-table or extractable dated match population. Other division/cup summary material is separate. Author Dinant Abbink; updated 5 Sep 2004; copyright Dinant Abbink/RSSSF 2004.

**2009/10:** stage-aware extraction finds 240 regular source slots: 228 numeric scores, two `awd` tokens and ten `n/p` tokens. The numeric population includes 210 non-Mouscron fixtures and 18 annulled Mouscron scores; two additional annulled Mouscron awards are explicit, with details in following source lines. The narrative record at exclusion reports 20 fixtures; this must not be described as 20 verified on-pitch games.

Separate sections contain 30 championship results, two 12-result European groups, two European-group-final legs, two European-qualification legs and 12 cross-division promotion/relegation fixtures: 310 documentary fixture-line candidates overall. These are not 310 unique additional dataset events. Standings rows are not parsed as matches. Raw date headings are retained as documentary context; round-level heading dates are not certified actual kickoff/completion dates. Later lower-tier regular/cup sections are not imported.

Author Jan Schoenmakers; updated 29 Sep 2011; copyright Jan Schoenmakers/RSSSF 2009/11. Both pages explicitly permit copying with proper acknowledgement while reserving rights. Original notices and full source bytes are retained. No broader model-training/commercial permission is inferred.

## Private identity, chronology and licensing

Physical source identity binds source SHA-256, physical line range and raw line/record SHA-256. Diagnostic event identity includes season, competition, stage, group, round, leg, date and literal teams. It is private and is not the final shared match_id. Source representations are not summed as unique events; repeated same-orientation pairs across stages are retained. Future importers must replace pair-only duplicate guards with stage-aware audit checks before any playoff inclusion can be safe. The shared eight-column schema remains unchanged.

Dates mean source dates only. Actual kickoff, resumption/completion, administrative decision and final result availability require later evidence. Future chronology policy must prevent earlier access to unfinished/undecided results; no result-availability correction is implemented now.

Technical acquisition/private inspection, historical confidence, technical eligibility, redistribution, commercial use and model training are separate. engsoccerdata README noncommercial/attribution wording and GPL package metadata do not resolve upstream rights. Later Belgian processing uses Football-Data, so reposting is not independent evidence or permission laundering. OpenFootball CC0 applies only to rights held; upstream independence/ownership is unestablished. No Football-Data endpoint, extra season original, mirror, official bulk archive or paid source was acquired. All twelve previous competitions retain their existing restrictions.

## Reproduction and fresh tests

Commands from the original worktree, with PYTHONDONTWRITEBYTECODE=1:

```sh
python -m scripts.collect_belgian_pro_league_feasibility --init
python -m scripts.collect_belgian_pro_league_feasibility
python -m scripts.validate_belgian_pro_league_feasibility
python -m scripts.verify_belgian_pro_league_feasibility
```

Initialization enforces approved initial HEAD/branch/unstaged state and private ignored storage. The approved existing initialized workspace is reused; originals/receipts cannot be overwritten. All seven assessment JSONs plus their reproducibility manifest regenerate into a safe temporary directory and match saved bytes and SHA-256. Independent raw CSV counting and independent TXT physical fixture-line census reconcile saved observations; cached collection is exercised with the request function forced to fail on any network attempt.

Fresh tests use the existing external CPython 3.13.12 environment at the retained Phase 8 temporary location, with bytecode and pytest cache disabled. No packages installed, no original .venv execution or modification. A stale older /private/tmp test environment and system Python lacked pytest; no tests passed there and neither was modified.

| Selection (overlapping; do not sum) | Passed | Failed / errors / skipped |
|---|---:|---|
| focused | 53 | 0 / 0 / 0 |
| acquisition_importer | 473 | 0 / 0 / 0 |
| non_ui | 2207 | 0 / 0 / 0 |
| app_launcher | 7 | 0 / 0 / 0 |
| full | 2214 | 0 / 0 / 0 |

New synthetic tests cover exact acquisition scope, immutable atomic writes, malformed CSV fields, checksums/provenance, explicit stages, missing/cancelled/awarded score representations, ambiguous/invalid grammar/dates, playoff rematches, source-bound overlap, visible conflicts and unmatched evidence, non-forced fixture expectations and RSSSF standings-versus-fixture handling. Test selections and logs are preserved privately; import failures were not treated as passes.

## Recommended Phase 3 boundary — not started

Reuse the CSV for a complete source inventory, not blindly as a regular-only primary input. Its measured range is exactly 1995/96–2024/25. Investigate stage separation in 2023/24 and 2024/25 and administrative history in 2002/03 and 2009/10 before any screening policy. Preserve all 8,394 observations.

At the same approved OpenFootball pin, only two additional in-target top-flight originals were verified in Phase 1:

| Proposed additional path | Git blob | Bytes | Purpose |
|---|---|---:|---|
| `2021-22/be1.txt` | `2e554912605069d2979b413ae696bf2aced1e4d1` | 27,360 | Eighteen-club transition and overlap |
| `2024-25/be1.txt` | `a883cd17078b92e876a11e150538c39122769b51` | 26,302 | Resolve endpoint stage scope and overlap |

URL prefix for both: https://raw.githubusercontent.com/openfootball/belgium/1166d3c9c5725aec01e1bbeaa20f6467e39ddbb8/ . These originals have NOT been acquired. No 2020/21 or 2022/23 original exists in the verified pin catalogue. The 2025/26 gap requires separately approved research for a complete revision/source, not automatic replacement of the preserved snapshot.

1990/91–1994/95 remain five missing dated seasons. Recommend bounded metadata/permissions research for dated archival material and official administrative evidence, not another acquisition disguised as inventory. RSSSF 1992/93 cannot fill dates. Exact new original URLs and access rights must be approved before acquisition.

No final regular-season/playoff inclusion policy, HOLD OUT/NOT PLAYED decision, correction, standardization, training, application integration, staging, commit or push has occurred. Stop after Phase 2.
