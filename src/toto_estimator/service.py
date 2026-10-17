"""UI-independent orchestration for the complete ticket workflow."""

from pathlib import Path

import pandas as pd

from .data import (
    load_historical_data,
    load_ticket_data,
    normalize_ticket,
    validate_historical_data,
)
from .models import DataValidationError, WorkflowResult
from .predictor import history_issues, predict_fixture
from .statistics import calculate_team_statistics
from .ticket import validate_ticket
from .validation import exact_integer


def run_workflow(history: pd.DataFrame, ticket: pd.DataFrame) -> WorkflowResult:
    try:
        history = validate_historical_data(history)
        ticket = normalize_ticket(ticket)
    except DataValidationError as exc:
        return WorkflowResult(errors=tuple(exc.issues))
    statistics = calculate_team_statistics(history)
    issues = validate_ticket(ticket, statistics.index)

    for ordinal, row in enumerate(ticket.itertuples(index=False), start=1):
        home_team, away_team = row.home_team, row.away_team
        try:
            position = exact_integer(row.position)
        except ValueError:
            position = ordinal
        if (
            home_team in statistics.index
            and away_team in statistics.index
            and home_team != away_team
        ):
            issues.extend(history_issues(statistics, position, home_team, away_team))

    if issues:
        return WorkflowResult(errors=tuple(issues))

    try:
        predictions = tuple(
            predict_fixture(
                statistics,
                int(row.position),
                row.home_team,
                row.away_team,
            )
            for row in ticket.sort_values("position").itertuples(index=False)
        )
    except DataValidationError as exc:
        return WorkflowResult(errors=tuple(exc.issues))
    return WorkflowResult(predictions=predictions)


def run_workflow_from_files(
    historical_path: str | Path, ticket_path: str | Path
) -> WorkflowResult:
    try:
        history = load_historical_data(historical_path)
        ticket = load_ticket_data(ticket_path)
    except DataValidationError as exc:
        return WorkflowResult(errors=tuple(exc.issues))
    return run_workflow(history, ticket)

