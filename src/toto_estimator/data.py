"""Source-independent loading and validation for public CSV inputs."""

import csv
import io
from datetime import date, datetime
from pathlib import Path

import pandas as pd

from .models import DataValidationError, ValidationIssue
from .outcomes import outcome_from_goals
from .validation import exact_integer, frame_issues, team_name

HISTORICAL_COLUMNS = ("season", "date", "home_team", "away_team", "home_goals", "away_goals")
TICKET_COLUMNS = ("position", "home_team", "away_team")


def _read_csv(path: str | Path, input_name: str) -> pd.DataFrame:
    source = str(path) if isinstance(path, (str, Path)) else input_name
    try:
        if not isinstance(path, (str, Path)) and not callable(getattr(path, "read", None)):
            raise DataValidationError([ValidationIssue("invalid_type", f"{input_name} must be a path or readable CSV stream.")])
        content = Path(path).read_bytes() if isinstance(path, (str, Path)) else path.read()
        if isinstance(content, bytes):
            content = content.decode("utf-8-sig")
        if not isinstance(content, str):
            raise DataValidationError([ValidationIssue("invalid_type", f"{input_name} must provide CSV text.")])
        reader = csv.reader(io.StringIO(content, newline=""), strict=True)
        header = next((row for row in reader if row), None)
        if header is None:
            raise DataValidationError([ValidationIssue("empty_data", f"{input_name} ({source}) is empty.")])
        if len(header) != len(set(header)):
            raise DataValidationError([ValidationIssue("duplicate_columns", f"{input_name} ({source}) has duplicate column headers.")])
        rows = []
        issues = []
        for row in reader:
            if not row:
                continue
            if len(row) != len(header):
                issues.append(ValidationIssue("row_width", f"{input_name} ({source}) row {reader.line_num}: expected {len(header)} fields, found {len(row)}.", row=reader.line_num))
            else:
                rows.append(row)
        if issues:
            raise DataValidationError(issues)
        return pd.DataFrame(rows, columns=header)
    except (OSError, UnicodeError, csv.Error) as exc:
        raise DataValidationError([ValidationIssue("read_error", f"Could not read {input_name} ({source}): {exc}")]) from exc


def validate_historical_data(frame: pd.DataFrame) -> pd.DataFrame:
    """Validate/copy public history from files or direct callers, retaining extra columns."""
    issues = frame_issues(frame, HISTORICAL_COLUMNS, "Historical data")
    if issues:
        raise DataValidationError(issues)
    if frame.empty:
        raise DataValidationError([ValidationIssue("empty_data", "Historical data must contain at least one match.")])
    normalized = frame.copy(deep=True).reset_index(drop=True)
    dates = []
    goals = {column: [] for column in ("home_goals", "away_goals")}
    results = []
    for index, row in normalized.iterrows():
        source_row = index + 2
        names = {}
        for column in ("home_team", "away_team"):
            names[column] = team_name(row[column])
            if not names[column]:
                issues.append(ValidationIssue(f"blank_{column}", f"{column} at historical row {source_row} must be a nonblank team name string.", row=source_row))
        if names["home_team"] and names["home_team"] == names["away_team"]:
            issues.append(ValidationIssue("identical_teams", f"Home and away teams must differ at historical row {source_row}.", row=source_row))
        for column, name in names.items():
            normalized.at[index, column] = name
        value = row["date"]
        parsed = pd.NaT
        if isinstance(value, (str, date, datetime, pd.Timestamp)):
            try:
                parsed = pd.to_datetime(value, format="%Y-%m-%d", errors="coerce")
            except (ValueError, TypeError, OverflowError):
                parsed = pd.NaT
        if pd.isna(parsed) or getattr(parsed, "tzinfo", None) is not None:
            issues.append(ValidationIssue("invalid_date", f"Date at historical row {source_row} must use YYYY-MM-DD without a timezone.", row=source_row))
        dates.append(parsed)
        for column in goals:
            try:
                number = exact_integer(row[column])
                if number < 0:
                    raise ValueError("must be non-negative")
            except ValueError as exc:
                issues.append(ValidationIssue("invalid_goals", f"{column} at historical row {source_row} {exc}; received {row[column]!r}.", row=source_row))
                number = None
            goals[column].append(number)
        if all(goals[column][-1] is not None for column in goals):
            result = outcome_from_goals(goals["home_goals"][-1], goals["away_goals"][-1])
        else:
            result = None
        if "result" in normalized.columns:
            supplied = row["result"]
            if not isinstance(supplied, str) or supplied not in ("1", "X", "2") or (result is not None and supplied != result):
                issues.append(ValidationIssue("invalid_outcome", f"result at historical row {source_row} must be 1/X/2 and agree with the goals; received {supplied!r}.", row=source_row))
        results.append(result)
    if issues:
        raise DataValidationError(issues)
    normalized["season"] = normalized["season"].astype(str).str.strip()
    normalized["date"] = pd.to_datetime(dates)
    for column, values in goals.items():
        normalized[column] = pd.Series(values, dtype="int64")
    normalized["result"] = results
    return normalized.sort_values("date", kind="stable").reset_index(drop=True)


def load_historical_data(path: str | Path) -> pd.DataFrame:
    return validate_historical_data(_read_csv(path, "historical data"))


def normalize_ticket(ticket: pd.DataFrame) -> pd.DataFrame:
    """Copy and normalize names and convertible positions; leave invalid values for diagnostics."""
    issues = frame_issues(ticket, TICKET_COLUMNS, "Ticket")
    if issues:
        raise DataValidationError(issues)
    normalized = ticket.copy(deep=True).reset_index(drop=True)
    for column in ("home_team", "away_team"):
        normalized[column] = normalized[column].map(team_name)
    positions = []
    for value in normalized["position"]:
        try:
            positions.append(exact_integer(value))
        except ValueError:
            positions.append(value)
    normalized["position"] = pd.Series(positions, dtype=object)
    return normalized


def load_ticket_data(path: str | Path) -> pd.DataFrame:
    frame = normalize_ticket(_read_csv(path, "ticket data"))
    issues = []
    for index, value in enumerate(frame["position"]):
        try:
            exact_integer(value)
        except ValueError as exc:
            issues.append(ValidationIssue("invalid_position", f"position at ticket row {index + 2} {exc}; received {value!r}.", row=index + 2))
    if issues:
        raise DataValidationError(issues)
    frame["position"] = frame["position"].astype("int64")
    return frame
