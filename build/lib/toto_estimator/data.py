"""Source-independent loading and validation for public CSV inputs."""

from pathlib import Path

import pandas as pd

from .models import DataValidationError, ValidationIssue

HISTORICAL_COLUMNS = (
    "season",
    "date",
    "home_team",
    "away_team",
    "home_goals",
    "away_goals",
)
TICKET_COLUMNS = ("position", "home_team", "away_team")


def _missing_columns(frame: pd.DataFrame, required: tuple[str, ...]) -> list[str]:
    return [column for column in required if column not in frame.columns]


def _read_csv(path: str | Path, input_name: str) -> pd.DataFrame:
    try:
        return pd.read_csv(path, dtype=object, keep_default_na=False)
    except (OSError, pd.errors.ParserError) as exc:
        raise DataValidationError(
            [ValidationIssue("read_error", f"Could not read {input_name}: {exc}")]
        ) from exc


def load_historical_data(path: str | Path) -> pd.DataFrame:
    """Load, validate, normalize, and chronologically sort match history."""

    frame = _read_csv(path, "historical data")
    missing = _missing_columns(frame, HISTORICAL_COLUMNS)
    if missing:
        raise DataValidationError(
            [
                ValidationIssue(
                    "missing_columns",
                    f"Historical data is missing required columns: {', '.join(missing)}.",
                )
            ]
        )

    frame = frame.loc[:, HISTORICAL_COLUMNS].copy()
    issues: list[ValidationIssue] = []

    for index, row in frame.iterrows():
        csv_row = int(index) + 2
        home = str(row["home_team"]).strip()
        away = str(row["away_team"]).strip()
        if not home:
            issues.append(
                ValidationIssue("blank_home_team", "Home team must not be blank.", row=csv_row)
            )
        if not away:
            issues.append(
                ValidationIssue("blank_away_team", "Away team must not be blank.", row=csv_row)
            )
        if home and away and home == away:
            issues.append(
                ValidationIssue(
                    "identical_teams",
                    f"Home and away teams must differ at historical row {csv_row}.",
                    row=csv_row,
                )
            )

    parsed_dates = pd.to_datetime(frame["date"], format="%Y-%m-%d", errors="coerce")
    for index in frame.index[parsed_dates.isna()]:
        csv_row = int(index) + 2
        issues.append(
            ValidationIssue(
                "invalid_date",
                f"Date at historical row {csv_row} must use YYYY-MM-DD.",
                row=csv_row,
            )
        )

    parsed_goals: dict[str, pd.Series] = {}
    for column in ("home_goals", "away_goals"):
        numeric = pd.to_numeric(frame[column], errors="coerce")
        parsed_goals[column] = numeric
        invalid = numeric.isna() | (numeric < 0) | (numeric % 1 != 0)
        for index in frame.index[invalid]:
            csv_row = int(index) + 2
            issues.append(
                ValidationIssue(
                    "invalid_goals",
                    f"{column} at historical row {csv_row} must be a non-negative integer.",
                    row=csv_row,
                )
            )

    if issues:
        raise DataValidationError(issues)

    frame["season"] = frame["season"].astype(str).str.strip()
    frame["home_team"] = frame["home_team"].astype(str).str.strip()
    frame["away_team"] = frame["away_team"].astype(str).str.strip()
    frame["date"] = parsed_dates
    frame["home_goals"] = parsed_goals["home_goals"].astype(int)
    frame["away_goals"] = parsed_goals["away_goals"].astype(int)
    frame["result"] = "X"
    frame.loc[frame["home_goals"] > frame["away_goals"], "result"] = "1"
    frame.loc[frame["home_goals"] < frame["away_goals"], "result"] = "2"
    return frame.sort_values("date", kind="stable").reset_index(drop=True)


def load_ticket_data(path: str | Path) -> pd.DataFrame:
    """Load the public ticket schema; complete rules are applied by ticket.py."""

    frame = _read_csv(path, "ticket data")
    missing = _missing_columns(frame, TICKET_COLUMNS)
    if missing:
        raise DataValidationError(
            [
                ValidationIssue(
                    "missing_columns",
                    f"Ticket data is missing required columns: {', '.join(missing)}.",
                )
            ]
        )

    frame = frame.loc[:, TICKET_COLUMNS].copy()
    numeric_positions = pd.to_numeric(frame["position"], errors="coerce")
    invalid = numeric_positions.isna() | (numeric_positions % 1 != 0)
    if invalid.any():
        issues = [
            ValidationIssue(
                "invalid_position",
                f"Position at ticket row {int(index) + 2} must be an integer.",
                row=int(index) + 2,
            )
            for index in frame.index[invalid]
        ]
        raise DataValidationError(issues)

    frame["position"] = numeric_positions.astype(int)
    frame["home_team"] = frame["home_team"].astype(str).str.strip()
    frame["away_team"] = frame["away_team"].astype(str).str.strip()
    return frame

