# Segunda División Phase 2: bounded feasibility acquisition

Date: 2026-11-22. Original `toto` worktree, `feature/data-collection`.
Unchanged HEAD: `052d25185182f1edbb80fac51cafbb59e0acf7cf`.

## Scope and assurance boundary

Exactly five approved dataset originals were acquired: four OpenFootball
`2-liga2.txt` files at commit
`80035a93dd4920985af52aa097a54a6fb888563b`, and RSSSF's `span97.html` snapshot.
No Football-Data request, BDFutbol purchase, additional-season acquisition,
standardized export, correction, exclusion, application change or training occurred.

**Measured result: the modern source format is usable, but the pinned 2025/26
season is incomplete. RSSSF 1996/97 provides results but mostly round-date proxies.
The 1990/91–2011/12 complete historical-source gap remains open.**

This assessment is not population historical certification or licensing clearance.
Scored records include source-marked administrative awards; a numeric score is
not proof that a game was played or that its score became available on that date.

## Preservation, acquisition and source identity

The private working area is `data/private/spain/segunda_division/`, covered by the
existing `/data/private/` Git ignore rule. `protected_before.json` fingerprints
**493 pre-existing private files**, covering all seven completed competitions,
and **145 tracked public files**. It also seals the existing planning-log prefix
and records HEAD. Public implementation/application files and previous source,
standardized, manifest and historical-evidence files must remain byte-identical;
planning history permits appends only. `.DS_Store` files are preserved, not staged.

Supporting metadata was reused, not downloaded: the pinned OpenFootball README,
LICENSE and NOTES, and the complete pinned Git tree already held by the La Liga
pipeline. Their original receipts, URLs, retrieval timestamps and hashes are
preserved in `metadata_receipts.json`. The complete tree identifies the exact
four paths, byte sizes and Git blob SHA-1s before data requests.

Acquisition used one request per approved original, five-second request spacing,
a 30-second timeout and a 2 MB response cap. Unexpected status, `Retry-After`,
redirect destination, identity or size triggers an explicit stop; no automatic
retry or access bypass. Each original is created exclusively alongside a receipt.
A complete cache is revalidated and reused without networking or writes. An
incomplete source/receipt pair fails rather than being repaired or overwritten.

All retrievals were on 2026-11-22 UTC. Exact per-file timestamps and response
headers are in the individual receipts. Byte counts and SHA-256:

| Original path under working area | Bytes | SHA-256 |
|---|---:|---|
| `openfootball/espana/2012-13/2-liga2.txt` | 36,224 | `88eefef7c2da989057e76e39a0c1a1c96833569ca6d92821fbd4afd85141494e` |
| `openfootball/espana/2018-19/2-liga2.txt` | 36,881 | `5d28c6719b973971f88103f033fa9d10bdc7a7904f30c84fa34d1ed7e299cd14` |
| `openfootball/espana/2019-20/2-liga2.txt` | 36,502 | `4f8f228e2df9b1e7e4c2bb8dbf2834523ef933ac535ab75782b35352c2d3b8fd` |
| `openfootball/espana/2025-26/2-liga2.txt` | 28,808 | `2d3472c87dfaf9db518c58964b1354cc5e5ada758fb4939dae9cce200f117a33` |
| `rsssf/span97.html` | 83,371 | `d66dc7dea8614161069b27d78509b5cb5fdc6bb5ea199d7a4c6aedaf7230d653` |

OpenFootball URLs use
`https://raw.githubusercontent.com/openfootball/espana/80035a93dd4920985af52aa097a54a6fb888563b/<season>/2-liga2.txt`.
RSSSF URL: <https://www.rsssf.org/tabless/span97.html>.
RSSSF's snapshot is identified by its retrieved bytes/SHA-256, not a fictitious
repository revision. The document identifies Juan Pedro Adrados, last updated
26 January 2000, copyright Juan Pedro Adrados and RSSSF 1999/2000.

## Measured season and stage inventory

Counts below are observations, not forced totals. All regular-stage directed
home/away pairings occur exactly once; no regular fixture is missing or duplicated.
No conflicting scores, malformed fields, invalid dates, normalized-name collision,
same-team/date collision, appearance-allocation error or round-allocation error
was found. Each modern regular season has 42 rounds of 11 fixtures; RSSSF's
regular section has 38 rounds of ten. Counts alone do not establish historical truth.

| Season/source | Observed | Regular | Other stage | Scored | Unscored | Expected regular | Regular clubs |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2012/13 OpenFootball | 462 | 462 | 0 | 462 | 0 | 462 | 22 |
| 2018/19 OpenFootball | 462 | 462 | 0 | 462 | 0 | 462 | 22 |
| 2019/20 OpenFootball | 462 | 462 | 0 | 462 | 0 | 462 | 22 |
| 2025/26 OpenFootball | 462 | 462 | 0 | 131 | 331 | 462 | 22 |
| 1996/97 RSSSF selected second-tier section | 382 | 380 | 2 promotion-playoff legs | 382 | 0 | 380 | 20 |
| Total selected observations | 2,230 | 2,228 | 2 | 1,899 | 331 | 2,228 | — |

The RSSSF original also contains Primera, cup and third-tier sections; these are
preserved in the original but explicitly outside the selected assessment. No
claim is made about counts or completeness of those other competitions. Its
two cross-division promotion-playoff legs remain separate: Mallorca–Rayo Vallecano
1–0 (25 June 1997) and `Rayo Vall`–Mallorca 2–1 (29 June), with dates labelled
leg-heading proxies. `Rayo Vall` and `Rayo Vallecano` are not silently merged.
All four OpenFootball files contain regular-season records only; this is not a
claim that promotion playoffs did not occur or are covered elsewhere by these files.

### Exact 2025/26 missing-result coverage

The last scored source date is **2025-11-03**. Missing results are:

- **330 fixtures:** all eleven games in each round 13 through 42.
- **One fixture:** Real Sociedad B–SD Huesca, round 10, source scheduled date
  **2025-11-05**. Its goals and outcome remain null, not 0–0.

The file represents 462 fixture slots through 31 May 2026, not 462 completed
results. It is an incomplete frozen source for a now-completed season; no later
score, actual playing date or updated revision was fetched or inferred.

### Dates, encoding and naming

OpenFootball originals decode strictly as UTF-8, preserving accents, original
labels and raw physical lines. Weekday/season checks determine omitted years,
including the documented July/August 2020 extended calendar. Unknown titles,
stage syntax, malformed scores or contradictory dates fail explicitly. No team
alias or cross-league identity mappings were applied. Reserve sides remain distinct.

RSSSF decodes as ISO-8859-1, preserving physical HTML source-line bindings and
raw records. Of the **380 regular fixtures**, **379** receive a date proxy from
their round heading; only **Mérida's source label `Merida`–Lleida 0–2** has an
explicit fixture-date annotation, **19 February 1997**, physical line **1820**.
This is in round 15, otherwise headed 15 December 1996. The explicit annotation
is retained; it is not an independently certified playing date. The 379 other
dates must not be advertised as individually verified dates or used as final
result-availability dates without further evidence.

Six wide-round scheduling candidates are retained, not treated as errors:

| Season | Round | Earliest–latest source dates |
|---|---:|---|
| 2019/20 | 6 | 2019-09-17–2019-10-16 |
| 2019/20 | 20 | 2019-12-13–2020-06-10 |
| 2019/20 | 24 | 2020-01-17–2020-02-19 |
| 2019/20 | 42 | 2020-07-20–2020-08-07 |
| 2025/26 | 10 | 2025-10-17–2025-11-05 |
| 1996/97 RSSSF | 15 | 1996-12-15–1997-02-19 |

These six rounds cover 65 distinct source fixture observations. Their complete
fixtures and source lines are in `feasibility_assessment.json`; a long span is
not an automatic correction or exclusion criterion.

## Exceptional-case context, unchanged source facts

The assessment binds contextual notes to original path/SHA-256/physical line and
source audit IDs. These are not standardized match IDs or approved processing
decisions. All observations remain present.

| Case | Original source observations | Documentary context and unresolved limits |
|---|---|---|
| Reus 2018/19 | 42 fixture observations: 21 not marked awarded, 21 explicitly `[awarded]`; award score strings preserved as 0–1 or 1–0 | Official LaLiga notice establishes expulsion on 28 January 2019. It does not certify all individual award scores, final appeals or availability dates. First source-marked award is Reus–Las Palmas, 19 January 2019, 0–1, line 376: notably before that expulsion notice. Do not treat the source calendar date as the date that an administrative result became known. |
| Rayo–Albacete 2019/20 | 10 June 2020, 1–0 (HT 0–0), round 20, line 346 | RFEF appeal decision establishes original kickoff/suspension on 15 December 2019. RFEF resumption notice, official annual report and LaLiga's later match widget support completion on 10 June 2020 and 1–0. Original kickoff and completion are separate contextual fields; no source date changed. Not exhaustive disciplinary clearance. |
| Deportivo–Fuenlabrada 2019/20 | 7 August 2020, 2–1 (HT 0–1), round 42, line 722 | Official annual report supports the actual playing date and Deportivo victory. An indexed scheduling notice refers to 20 July and an intermediate 5 August plan, not actual kickoff. Exact 2–1 remains a source observation in this limited review; final legal/administrative clearance is not claimed. |

Directly inspected evidence (paraphrased scope, no full-document archival claim):

- [S2-E01: LaLiga, Nota Informativa, 28 January 2019](https://www.laliga.com/noticias/nota-informativa-164).
- [S2-E02: RFEF Comité de Apelación, expediente 276–2019/20, page 1](https://rfef.es/sites/default/files/pdf/resolucion_apelacion_rayo-albacete.pdf).
- [S2-E03: RFEF resumption notice, 3 June 2020](https://rfef.es/es/noticias/comite-competicion-fija-rayo-albacete-jornada-20-dia-10-junio).
- [S2-E04: LaLiga suspension article, dated 15 December 2019, with later match widget](https://www.laliga.com/noticias/nota-informativa-rayo-albacete).
- [S2-E05: LaLiga Annual Report 2019–2020, Actividades Deportivas](https://memorias.laliga.com/2019/es/actividades-deportivas).
- S2-E06 is **search-index evidence only**: [intermediate Deportivo–Fuenlabrada scheduling notice](https://www.laliga.com/noticias/nota-informativa-deportivo-fuenlabrada-play-off-2020).

Organizer/federation documentary context differs from acquired compiler files,
but no universal independence or exhaustive absence of later decisions is claimed.
Reus's individual final administrative outcomes/dates remain unresolved for policy.
The RSSSF rescheduling annotation and 379 date proxies need independent checking.

## Reproduction, tests and actual artifacts

Public implementation:

- `scripts/collect_segunda_feasibility.py`: guarded initialization, exact five-URL
  plan, immutable Git identity checks, receipts, cached reuse and stop-on-failure.
- `scripts/validate_segunda_feasibility.py`: independent source parsing,
  stage-separated counts, pairings, date precision, scores, names, scheduling and
  bound exceptional context. Standard library only; source goals must be digit
  strings within the shared signed-64-bit range. No application/importer is invoked.
- `tests/test_segunda_feasibility.py`: synthetic cases; no private files or real
  network needed.

Private artifacts (**20 files**): baseline (1); reused metadata (4) and its receipt
registry (1); five originals (5) and per-original receipts (5); acquisition manifest
(1); current assessment (1); retained initial pre-context assessment (1); final
verification receipt (1). `feasibility_assessment_initial.json` preserves the first
current-phase measured assessment before contextual evidence was added; it is
not a source original or the current authoritative report.

Commands, from the original worktree, with project-compatible Python:

```sh
PYTHONPATH=src:. python -B scripts/collect_segunda_feasibility.py --init
PYTHONPATH=src:. python -B scripts/validate_segunda_feasibility.py
PYTHONPATH=src:. python -B scripts/validate_segunda_feasibility.py --check
PYTHONPATH=src:. python -B -m pytest tests/test_segunda_feasibility.py -q -p no:cacheprovider
```

First assessment creation refuses an existing output. Use `--check` for subsequent
comparisons. Initialization requires the preserved La Liga metadata bundle; a
fresh public clone without private evidence is not a complete acquisition cache.

Measured verification:

- **33 focused synthetic tests passed.**
- **842 full repository tests passed in 14.89 seconds**, including all seven
  app/launcher tests and the existing La Liga tests. Counts overlap, do not add.
- Actual acquisition cache ran twice with network forbidden: no writes and
  identical receipts/manifest. All five original SHA-256/size checks and four
  Git blob checks pass.
- Two offline assessment regenerations matched the saved bytes and SHA-256:
  `09d7aec5b9f9db484e7571ac77be2bae9879092acee57d6cc8b3b6e30b94cfea`.
- Protected 493 private / 145 tracked public hashes and planning prefix match.
- No private data tracked or staged; no commit, push or merge.

Technical issue: the original iCloud-hosted `.venv` stalled on NumPy/pytest file
reads. A previously created temporary verification environment had lost files;
it was restored by bounded copying of existing installed files, without package
downloads/upgrades or modifying the original `.venv`. Fresh full-suite results
above came from that restored environment (Python 3.13.12; NumPy 2.5.3, pandas
3.0.6, Streamlit 1.64.0, pytest 9.1.1, Protobuf 7.36.2). The earlier stalled attempts
are not counted as passes. Assessment CLI itself now needs only the standard library.

## Viability, rights and next gate

| Classification | Conclusion |
|---|---|
| Technical suitability | Football.TXT is parseable with complete directed fixture schedules for the four samples. 2025/26 has 331 missing results; RSSSF has 379 round-date proxies. |
| Historical confidence | Source observations plus limited documentary context only; source counts and labels are not certification. |
| Redistribution | OpenFootball CC0 applies to rights held, without upstream warranty. RSSSF requires acknowledgement of Juan Pedro Adrados and reserves rights. Private retention continues. |
| Model-training clearance | **UNRESOLVED for both sources.** Neither successful parsing nor this acquisition authorizes training. |

Before Phase 3, recommend agreeing a bounded modern candidate scope of
**2012/13–2024/25**: 13 seasons, three already held, ten additional files to acquire
only after exact pinned-path approval. Completeness of those ten is not yet known.
Keep the frozen incomplete 2025/26 sample visible; a complete replacement/source
requires separate research and approval, not silent patching or score inference.

For **1990/91–2011/12**, obtain suitable source permissions and fixture-level dates
(potentially a licensed BDFutbol export). The single RSSSF sample does not establish
complete historical coverage, accurate per-match dates, compiler independence or
training permission. Earlier expansion likewise requires format/stage research.
Reus awards require authoritative operative decisions/appeals and result-availability
policy later; do not resolve or exclude them during acquisition. Stop for approval.
