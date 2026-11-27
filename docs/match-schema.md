# Canonical match schema v2

Owner-approved 2026-11-27 during Champions League Phase 4. Historical datasets and
detailed metadata remain private; this document contains schema instructions only.

```csv
match_id,date,league,season,home_team,away_team,home_goals,away_goals,neutral_venue
```

The first eight columns retain their meanings and order. UTF-8 without BOM,
LF line endings, ordinary CSV quoting, one header and no index are canonical.
Dates use ISO `YYYY-MM-DD`; seasons use `YYYY` or consecutive `YYYY/YYYY`.
Names retain source-supported spelling, case and punctuation after surrounding
whitespace removal; club corrections require approved source/season-bound evidence.
Goals are nonnegative integers. Played matches require supported regulation-time
scores including stoppage time; preserve the explicit retrospective administrative
exception in [PROCESS.md](../PROCESS.md). Extra-time totals, shootouts and aggregates
are distinct private metadata and cannot silently replace regulation scores.

`match_id` remains the full SHA-256 of compact UTF-8 JSON
`[league,season,date,home_team,away_team]`, using `ensure_ascii=False` and separators
`(',', ':')`. Goals, stage, sources, outcome and neutrality do not enter the ID.
New output sorts by that identity tuple. Existing domestic rows retain their frozen
order during migration. A collision is an error to investigate, not a reason to
alter the ID definition or silently drop an event.

## Neutrality

`neutral_venue` is the **official competition-format classification**, not actual
stadium neutrality or realized home advantage:

| CSV value | Meaning |
|---|---|
| `0` | Conventional home/away competition format |
| `1` | Officially neutral-site competition format |
| empty | Format cannot reliably be established |

Write integers `0`/`1` or an empty cell. `NA`, `null`, booleans, floating-point
tokens and whitespace-padded tokens are not canonical CSV values. In memory use
integers/`None`; the optional application-loader column uses pandas nullable `Int8`
with `pd.NA`. Direct missing-value inputs are accepted by the loader. No source
home label, single-leg status, relocation, or word “final” substitutes for format
evidence. Official neutral-format finals remain 1 at a participant's usual ground.
Preserve physical venue evidence independently; comprehensive stadium research is
not a prerequisite.

First/second orientation and associated goals remain unchanged. Outcome is derived:
1 = first-listed win, X = draw, 2 = second-listed win, with documented administrative
exceptions labelled privately. Do not add outcome or period scores to this schema.
Stage/scope/group/path/leg, source URL/hash/physical locator, period components,
original venue evidence, accepted decision and output linkage belong in a private
sidecar. Future venue-specific statistics must not automatically treat neutral-format
matches as ordinary home/away observations. That model change remains deferred;
current prediction behavior is unchanged and UCL is not integrated into the model.

## Compatibility and migration

`toto_estimator.match_schema` defines `CANONICAL_COLUMNS`, `LEGACY_COLUMNS`,
`canonical_match_id`, strict `neutral_value` and the v2 record validator.
`historical_import.OUTPUT_COLUMNS` remains the legacy eight-column alias so frozen
adapters can reproduce their historical outputs. The shared importer has explicit
`include_neutral_venue=True` support and source-level neutrality metadata; heterogeneous
stages require a reviewed fixture-level adapter such as the UCL standardizer.
The application loader accepts existing six/eight-column inputs and validates the
ninth column when present. Absence does not silently become 0. Synthetic demo files
and model logic remain unchanged.

`scripts/extend_domestic_neutrality.py` prepares privately from exact frozen backups,
checks original hashes and original-byte projection, then explicitly applies only
the approved current standardized targets. It must not target raw sources, frozen
audit archives, or acquired competitions awaiting validation. Before/after reports
retain counts, field comparisons, IDs, neutrality counts and hashes. Existing
historical receipts continue to identify the backed-up v1 bytes; the new migration
receipt identifies v2 bytes without rewriting old provenance.

`scripts/standardize_uefa_champions_league.py` consumes hash-bound approved decisions
and format rules, writes v2 plus private sidecars, and refuses existing destinations.
`scripts/verify_uefa_champions_league_standardization.py` separately reconstructs
fields/IDs/order/CSV from original observations and approved evidence, using the
earlier independent raw readers, independent format expectations and independent
serialization. No generator, migration or canonical-ID helper is imported there.
