# Belgian Pro League — targeted 2021/22 source recovery

Measured 2026-11-25. Supplementary evidence recovery after approved Phase 4; NOT Phase 5 adjudication. No historical corrections, final match dispositions, stage-inclusion policy, standardization or model use.

## Acquisition and attribution

Approved original and final URL: https://www.rsssf.org/tablesb/belg2022.html

Retrieved UTC: `2026-11-25T14:43:49.181319+00:00`. HTTP200; 27,614 bytes; original ISO-8859-1 HTML. Title: Belgium 2021/22. SHA-256: `03e8db8b09e3220fa0a3afc74325179997ef1dc688e33cb783a0387f88a72fc5`. No Git commit/blob applies to this mutable web snapshot.

Authors: **Hans Schöggl and Karel Stokkermans**, Rec.Sport.Soccer Statistics Foundation. Page last updated 8 Apr 2025; copyright authors/RSSSF2021/25. The preserved notice permits copying in whole or part with proper acknowledgement and reserves rights. Exact notice and all available response headers are retained in the private receipt. No broader commercial, redistribution or model-training permission is inferred.

The unchanged original is `data/private/belgium/pro_league/rsssf/tablesb/belg2022.html`, with `.provenance.json` beside it. Acquisition is restricted to this exact URL, bounded to30seconds/2MB, with no redirects, retries, mirrors or substitute source. Atomic exclusive writes prevent overwriting; partial source/receipt pairs fail. Cached replay makes zero requests and changes no bytes. No other historical original, Walfoot dataset, newer OpenFootball revision or Football-Data file was acquired.

## Measured documentary population

| First Division A stage | Source representations | Conditional events | Clubs |
|---|---:|---:|---:|
| Regular |308|306|18|
| Championship playoff |12|12|4|
| Europe playoff |12|12|4|
| Promotion/relegation |2|2|2|
| Total |334|332|—|

Raw tokens:329 numeric scores,two abd markers,three awd markers. Numeric score tokens and scores reported in administrative award annotations remain separate fields. None is silently promoted to an ordinary played result or approved for screening. Cup, First Division B and lower-tier sections are excluded by explicit section boundaries.

The regular stage contains34 rounds and306 unique directed pairings, with no missing/repeated event pairing. Championship and Europe stages each contain six rounds and all12 directed pairings among four clubs. The two promotion/relegation legs are retained separately, not added to the330 top-flight regular/championship/Europe event identities.

## Source-observation versus event identity

Each documentary observation retains exact HTML line, line SHA-256, full-source SHA-256, original section, round/leg, day/month heading context, source-year resolution, literal decoded labels and original entity-encoded team strings, raw score token and annotation fragments. `Kortr&#307;k` is retained alongside decoded `Kortrĳk`; no global string alias is applied.

A private conditional event groups season/stage/round-or-leg/home/away observations only when source evidence supports it. A repeated description is linked as an interruption/continuation only when there is one abd entry and one numeric result with an explicit remaining/second-half annotation. Otherwise repetition remains ambiguous. Different stages/legs remain distinct even for the same clubs. All334 original representations remain available; grouping the two explicit continuations produces332 events, not334 real-world matches.

The Standard–Charleroi award annotation continues on the following Mechelen–Genk line. The parser preserves both physical lines but attaches the trailing crowd-trouble text to Standard–Charleroi, not to the unrelated Mechelen result. Synthetic tests cover this actual grammar hazard.

## Complete historical comparison

**306 historical regular observations have306 RSSSF conditional regular counterparts.** Unmatched historical:0; unmatched documentary regular events:0; source-date disagreements:0; reported-score disagreements:0; ambiguous grouped events:0.

Comparison uses the frozen raw historical CSV for Season2021,B1,tier1 and exactly one source/season-bound diagnostic correspondence for each literal label. Six non-identical label pairs include Beerschot/Beerschot VA,Leuven/Oud-Heverlee Leuven,Union/Royal Union Saint-Gilloise,Sint-Truiden/St Truiden,Kortrĳk/Kortrijk,Zulte Waregem/Waregem. This is not a global alias or legal identity determination. Original labels and values in both sources remain unchanged.

For ordinary numeric entries, reported scores are compared directly. For awd entries, the original token remains awd and the explicitly reported award score is compared separately. Zero disagreements therefore does not mean that all306 results were ordinary played matches or that every award is legally final. Source independence is not established.

## Interruption and award candidates

| Candidate | Original source representation | Continuation / reported result | Historical CSV comparison |
|---|---|---|---|
| Beerschot–Cercle Brugge |2021-07-24,abd at0-1 in55 minutes,weather;line53|2021-07-27,0-1,remaining35 minutes;line60|2021-07-27,0-1|
| Seraing–Union |2022-01-15,abd at0-2 at halftime,fog;line351|2022-01-18,0-4,second half;line359|2022-01-18,0-4|
| Leuven–Mechelen |2022-01-15,awd,reported5-0,Mechelen dns;line352|Administrative result described in same source row|2022-01-15,5-0|
| Union–Beerschot |2022-04-10,awd,reported5-0;abandoned0-0 in81 minutes;line530|Administrative result described in same source row|2022-04-10,5-0|
| Standard–Charleroi |2021-12-05,awd,reported0-3;abandoned0-3 in87 minutes;lines286–287|Multiline administrative annotation preserved|2021-12-05,0-3|

The two continuation dates agree with the existing CSV; nothing was corrected. Award rows use the documentary fixture-date context, not a verified administrative-decision/finality date. The on-pitch state, continuation result, reported award and eventual final result availability remain separate. All five cases require later authoritative evidence review. No HOLD OUT/NOT PLAYED/award-acceptance decision has been assigned.

## Postseason and cross-division inventory

Championship labels: Club Brugge,Union,Anderlecht,Antwerp;12 fixtures. Europe labels: Gent,Genk,Charleroi,Mechelen;12 fixtures. These24 outcomes are supplemental postseason evidence, not additions to the screened dataset.

Promotion/relegation legs:2022-04-23 RWDM–Seraing0-1;2022-04-30 Seraing–RWDM0-0. These are two separate stage/leg identities. RWDM is not globally merged with any other Molenbeek-labelled entity.

## Transparent combined accounting

| Population | Count |
|---|---:|
| Frozen Phase4 CSV/TXT representations (unchanged) |10100|
| Frozen Phase4 conditional events (unchanged) |8698|
| New selected RSSSF documentary representations |334|
| New grouped documentary events |332|
| Regular counterparts already represented in H |306|
| Additional championship/Europe candidates |24|
| Separate cross-division candidates |2|
| Combined CSV/TXT plus new documentary representations |10434|
| Conditional event union with only these306 links |8724|

The8724 diagnostic union comprises8722 top-flight event candidates plus the two explicitly separate cross-division candidates. It is not a standardized/model-training population. Earlier RSSSF documentary archives remain separate just as in the original Phase4 baseline; they are not silently mixed into this union. Original Phase2–4 counts, manifests and decisions are unchanged.

The misplaced OpenFootball `2021-22/be1.txt` is still the same2020/21 original. It has not been renamed,replaced or reattributed. Actual2021/22 now has a technically complete RSSSF regular-season comparison and24 postseason counterparts,while OpenFootball actual2021/22 remains absent. The five early dated-season gaps and incomplete2025/26 snapshot are unaffected.

## Verification and fresh tests

Four supplemental assessments plus a reproducibility manifest regenerated in a separate bounded process in temporary storage and matched byte-for-byte/SHA-256. Cache replay with the request function forbidden made zero network calls and changed no files. All71 frozen Phase2–4 private/public entries and planning-log prefixes are protected. The nine previous originals are immutable; the new HTML is the tenth approved original. All detailed data remain Git-ignored.

Existing external CPython3.13.12 environment reused without installation or original .venv modification. Bytecode and pytest cache writes disabled. Test selections overlap and must not be added together.

| Fresh selection | Passed | Failed/errors/skipped |
|---|---:|---|
| new | 29 |0/0/0|
| belgian | 173 |0/0/0|
| full | 2334 |0/0/0|

Tests cover stage boundaries, standings rejection, literal/HTML labels, date context, physical line hashes, explicit continuations, ambiguous duplicate descriptions, awards versus numeric results, multiline annotation ownership,promotion/relegation legs,cross-source conflicts,determinism,source hashes,exclusive publication and zero-request cache replay.

Reproduction commands from the original worktree:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m scripts.recover_belgian_2021_22 --collect
PYTHONDONTWRITEBYTECODE=1 python3 -m scripts.recover_belgian_2021_22
PYTHONDONTWRITEBYTECODE=1 python3 -m scripts.recover_belgian_2021_22 --verify
```

## Conclusion and remaining limits

**Actual2021/22 comparative coverage is adequately documented for Phase5**, with306 complete regular counterparts and independently traceable interruption/award representations. It is not authoritative certification of final results,appeals,actual result-availability dates or independent upstream lineage.

Prioritize the five documented exception cases in Phase5,using bounded official disciplinary/match evidence after separate approval. No additional dataset is needed merely to fill an RSSSF regular pairing gap: none was found. A genuine OpenFootball2021/22 replacement remains a separately authorized acquisition question. No Walfoot bulk data or additional original was used.

Twelve completed competitions and137189 screened records remain unchanged. No prior assessment,source,application,promotional file,shared schema or match-ID convention was changed. Only this supplemental report,new recovery script/tests and append-only planning entries are public changes. No historical correction,disposition,stage inclusion,standardization,training,staging,commit,push or Phase5 adjudication occurred.
