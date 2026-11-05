"""Read local Football-Data CSVs without writing files or guessing metadata.

See docs/historical-import.md for metadata, identity and rejection policies.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from .models import DataValidationError, ValidationIssue
from .outcomes import outcome_from_goals
from .validation import exact_integer, team_name

OUTPUT_COLUMNS = (
    "match_id", "date", "league", "season", "home_team", "away_team",
    "home_goals", "away_goals",
)
SCHEMAS = (
    ("HomeTeam", "AwayTeam", "FTHG", "FTAG"),
    ("Home", "Away", "HG", "AG"),
)


@dataclass(frozen=True)
class HistoricalSource:
    path: Path
    league: str
    season: str | None = None
    division: str | None = None
    country: str | None = None
    source_league: str | None = None
    encoding: str = "utf-8-sig"


@dataclass
class ImportResult:
    records: list[dict[str, object]] = field(default_factory=list)
    summary: dict[str, int] = field(default_factory=lambda: {
        "total": 0, "accepted": 0, "rejected": 0,
        "duplicates": 0, "fixtures": 0, "conflicts": 0,
    })
    issues: list[ValidationIssue] = field(default_factory=list)


def canonical_season(value: str) -> str:
    """Accept YYYY, YYYY/YY, YYYY-YY, YYYY/YYYY or YYYY-YYYY."""
    if not isinstance(value, str):
        raise ValueError("season must be a string")
    match = re.fullmatch(r"([0-9]{4})(?:[-/]([0-9]{2}|[0-9]{4}))?", value.strip())
    if not match:
        raise ValueError("season must use YYYY or consecutive YYYY/YYYY")
    start = int(match[1])
    if not 1 <= start <= 9999:
        raise ValueError("invalid season year")
    if match[2] is None:
        return f"{start:04d}"
    end = int(match[2])
    if len(match[2]) == 2:
        end += start // 100 * 100
        if end <= start:
            end += 100
    if end != start + 1 or end > 9999:
        raise ValueError("cross-year season must contain consecutive years")
    return f"{start:04d}/{end:04d}"


def parse_match_date(value: str, season: str) -> str:
    """Resolve DD/MM/YY using season years, never Python's century pivot."""
    match = re.fullmatch(r"([0-9]{1,2})/([0-9]{1,2})/([0-9]{2}|[0-9]{4})", value.strip())
    if not match:
        raise ValueError("Date must use DD/MM/YY or DD/MM/YYYY")
    years = [int(year) for year in season.split("/")]
    year = int(match[3])
    candidates = [y for y in years if y % 100 == year] if len(match[3]) == 2 else [year]
    if len(candidates) != 1 or candidates[0] not in years:
        raise ValueError("Date year does not agree with season")
    return date(candidates[0], int(match[2]), int(match[1])).isoformat()


def _issue(code: str, source: HistoricalSource, row: int | None, message: str) -> ValidationIssue:
    location = f"{source.path}" + (f" row {row}" if row is not None else "")
    return ValidationIssue(code, f"{location}: {message}", row=row)


def _rows(source: HistoricalSource):
    """File/schema errors are fatal: never return a silently truncated import."""
    try:
        with Path(source.path).open(encoding=source.encoding, newline="") as handle:
            reader = csv.reader(handle, strict=True)
            headers = next(reader, None)
            if not headers:
                raise ValueError("empty CSV; missing header")
            named = [h for h in headers if h]
            if len(named) != len(set(named)):
                raise ValueError("duplicate named column headers")
            schemas = [s for s in SCHEMAS if all(c in headers for c in s)]
            if "Date" not in headers or len(schemas) != 1:
                raise ValueError("requires Date and exactly one supported team/score schema")
            if source.season is None and "Season" not in headers:
                raise ValueError("explicit season or Season column required")
            for column, expected in (("Div", source.division), ("Country", source.country),
                                     ("League", source.source_league)):
                if column in headers and (not isinstance(expected, str) or not expected.strip()):
                    raise ValueError(f"explicit source mapping required for {column}")
                if expected is not None and column not in headers:
                    raise ValueError(f"mapped source column {column} is missing")
            for cells in reader:
                if not cells:
                    continue
                # Old exports contain repeated unnamed padding columns. They
                # are safe only when all their cells are empty.
                if len(cells) != len(headers) or any(v.strip() for h, v in zip(headers, cells) if not h):
                    yield reader.line_num, None, schemas[0]
                else:
                    yield reader.line_num, dict(zip(headers, cells)), schemas[0]
    except (OSError, UnicodeError, LookupError, csv.Error, ValueError) as exc:
        raise DataValidationError([_issue("source_error", source, None, str(exc))]) from exc


def import_historical_csvs(sources: Iterable[HistoricalSource]) -> ImportResult:
    """Validate sources together; deduplicate across files and quarantine conflicts.

    total = accepted + rejected + duplicates + fixtures. conflicts is a
    subset of rejected. Structural file errors raise DataValidationError.
    """
    result = ImportResult()
    groups = defaultdict(list)
    mappings: dict[str, tuple[object, ...]] = {}
    for source in sources:
        if not isinstance(source.league, str) or not source.league.strip():
            raise DataValidationError([_issue("metadata", source, None, "league must be explicit and nonblank")])
        league = source.league.strip()
        mapping = (source.division, source.country, source.source_league)
        if league in mappings and mappings[league] != mapping:
            raise DataValidationError([_issue("metadata", source, None, "different source competitions mapped to the same league")])
        mappings[league] = mapping
        try:
            explicit_season = canonical_season(source.season) if source.season is not None else None
        except ValueError as exc:
            raise DataValidationError([_issue("metadata", source, None, str(exc))]) from exc
        for number, row, schema in _rows(source):
            result.summary["total"] += 1
            try:
                if row is None:
                    raise ValueError("row width mismatch or nonempty unnamed column")
                for column, expected in (("Div", source.division), ("Country", source.country),
                                         ("League", source.source_league)):
                    if expected is not None and row[column].strip() != expected.strip():
                        raise ValueError(f"{column} does not agree with explicit source mapping")
                season = canonical_season(row["Season"]) if "Season" in row else explicit_season
                if explicit_season is not None and season != explicit_season:
                    raise ValueError("Season does not agree with explicit metadata")
                match_date = parse_match_date(row["Date"], season)
                home, away = team_name(row[schema[0]]), team_name(row[schema[1]])
                if not home or not away or home == away:
                    raise ValueError("teams must be nonblank and distinct")
                score_cells = [row[column].strip() for column in schema[2:]]
                supplied_results = [row[c].strip() for c in ("FTR", "Res") if c in row]
                if score_cells == ["", ""] and not any(supplied_results):
                    result.summary["fixtures"] += 1
                    result.issues.append(_issue("fixture", source, number, "no final result; excluded"))
                    continue
                goals = [exact_integer(value) for value in score_cells]
                if min(goals) < 0:
                    raise ValueError("full-time goals must be nonnegative")
                expected_result = {"1": "H", "X": "D", "2": "A"}[outcome_from_goals(*goals)]
                if any(value and value != expected_result for value in supplied_results):
                    raise ValueError("FTR/Res does not agree with full-time goals")
                identity = (league, season, match_date, home, away)
                digest = hashlib.sha256(json.dumps(identity, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()
                record = dict(zip(OUTPUT_COLUMNS, (digest, match_date, league, season, home, away, *goals)))
                groups[identity].append((record, source, number))
            except ValueError as exc:
                result.summary["rejected"] += 1
                result.issues.append(_issue("invalid_record", source, number, str(exc)))
    for identity, entries in sorted(groups.items()):
        scores = {(r["home_goals"], r["away_goals"]) for r, _, _ in entries}
        if len(scores) > 1:
            evidence = "; ".join(f"{s.path} row {n}: {r['home_goals']}-{r['away_goals']}" for r, s, n in entries)
            result.summary["rejected"] += len(entries)
            result.summary["conflicts"] += len(entries)
            for _, source, number in entries:
                result.issues.append(_issue("conflicting_duplicate", source, number, f"conflicting results; all excluded: {evidence}"))
        else:
            result.records.append(entries[0][0])
            result.summary["accepted"] += 1
            for _, source, number in entries[1:]:
                result.summary["duplicates"] += 1
                first = entries[0]
                result.issues.append(_issue("duplicate", source, number, f"identical match already in {first[1].path} row {first[2]}"))
    return result
