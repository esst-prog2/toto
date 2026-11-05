# Local historical CSV importer

`toto_estimator.historical_import.import_historical_csvs` reads local files only.
It returns an `ImportResult` containing `records`, `summary` and source/row
`issues`. It never writes files, downloads data, or calls prediction code.
The existing homework readers, spike builder and evaluation remain unchanged.

From the repository root, run `.venv/bin/python` with `PYTHONPATH=src`, then:

```python
from pathlib import Path
from toto_estimator.historical_import import HistoricalSource, import_historical_csvs

result = import_historical_csvs([
    HistoricalSource(
        Path("data/football_data_raw/E0_2223.csv"),
        league="england.premier-league",
        season="2022/23",
        division="E0",
    ),
])
print(result.summary)
for issue in result.issues:
    print(issue.code, issue.message)
```

For future local data, use paths inside Git-ignored `data/private/`. No actual
datasets are included in this change. Source usage permissions remain the
caller's responsibility.

## Explicit metadata

- `league` is a caller-managed, globally distinct competition ID. Never reuse
  it for different competitions. No filenames or team names determine leagues.
- When a CSV contains `Div`, provide `division`; when it contains `Country`
  or `League`, provide `country` or `source_league` respectively. Every row
  must match these explicit source identifiers, with surrounding whitespace
  removed. Mixed-competition files must be separated or filtered explicitly
  by the caller; mismatched rows are rejected and reported.
- Sources assigned the same output league must have identical source mappings.
  Cross-provider reconciliation is deliberately not automatic.
- Provide `season` for season-specific files. An explicit `Season` column can
  instead supply seasons per row in multi-season files. If both exist they
  must agree. Accepted spellings are `YYYY`, `YYYY/YY`, `YYYY-YY`,
  `YYYY/YYYY`, and `YYYY-YYYY`; output is `YYYY` or `YYYY/YYYY`.
  Cross-year seasons must use consecutive years, including `1999/00`.
- Dates accept day-first `DD/MM/YY` and `DD/MM/YYYY`. Two-digit years are
  resolved against the season's year(s), with no century pivot. Dates outside
  those calendar years are rejected. No July/August season boundary is guessed;
  exceptional postponed matches outside these years need explicit review.
- Input defaults to UTF-8 with optional BOM. Supply `encoding` explicitly for
  a verified legacy encoding; decoding errors are never silently replaced.

## Validation and duplicates

Exactly one full team/score schema is required: `HomeTeam/AwayTeam/FTHG/FTAG`
or `Home/Away/HG/AG`, plus `Date`. Extra named columns are permitted. Repeated
unnamed padding columns from older exports are permitted only with empty cells.
Malformed CSV syntax, missing files, invalid headers or missing metadata cause
`DataValidationError`; no partial result is returned for that import call.
An empty file is an error; a valid header-only file returns zero counts.
Blank physical rows are ignored. Row-width errors are reported as rejected rows.

Scores use the existing exact signed-int64 integer validator and must be
nonnegative. Integral decimal strings such as `1.0` are accepted. Both blank
scores with no supplied result are excluded and counted as `fixtures` (this
does not assert why a result is absent). One missing score, invalid numbers,
invalid dates or blank/identical teams cause rejection. Nonblank `FTR`/`Res`
must be H/D/A and agree with goals. Team spelling, case and punctuation are
preserved; only surrounding whitespace is removed by the existing helper.

Identity is `(league, canonical season, ISO date, home team, away team)`.
`match_id` is the full SHA-256 of that tuple encoded as compact UTF-8 JSON.
IDs do not depend on file paths, input order or goals. Records are sorted by
the identity tuple. Same-day replays with otherwise identical identities cannot
be distinguished automatically; changed dates or team spellings are not fuzzy
matched.

Exact repeated matches contribute one accepted record; extra rows are counted
as `duplicates`, with source references. If validated rows for an identity
contain different scores, **all rows in that group are excluded** and reported
with the competing scores and source locations. No score wins by input order.
Submit overlapping files in one call to detect cross-file duplicates; persistent
database reconciliation is not implemented.

Counts satisfy `total = accepted + rejected + duplicates + fixtures`.
`conflicts` counts rows in conflicting groups and is a subset of `rejected`.
Review the issues before accepting an import, including when accepted is zero.

Output columns are `match_id,date,league,season,home_team,away_team,home_goals,away_goals`.
For optional serialization, reuse `scripts.artifact_io.serialize_csv` with
`OUTPUT_COLUMNS`; the importer intentionally does not choose destinations or
overwrite anything. The existing predictor does not isolate leagues itself:
select the intended competition before passing records to existing workflows.
This importer verifies format and consistency, not real-world score accuracy
or season completeness.
