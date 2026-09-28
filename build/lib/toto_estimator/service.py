"""UI-independent orchestration for the complete ticket workflow."""

from pathlib import Path

import pandas as pd

from .data import load_historical_data, load_ticket_data
from .models import DataValidationError, WorkflowResult
from .predictor import history_issues, predict_fixture
from .statistics import calculate_team_statistics
from .ticket import validate_ticket


def run_workflow(history: pd.DataFrame, ticket: pd.DataFrame) -> WorkflowResult:
    statistics = calculate_team_statistics(history)
    issues = validate_ticket(ticket, statistics.index)

    if not any(issue.code in {"missing_columns", "invalid_position"} for issue in issues):
        for row in ticket.sort_values("position").itertuples(index=False):
            home_team = str(row.home_team).strip()
            away_team = str(row.away_team).strip()
            if (
                home_team in statistics.index
                and away_team in statistics.index
                and home_team != away_team
            ):
                issues.extend(
                    history_issues(
                        statistics,
                        int(row.position),
                        home_team,
                        away_team,
                    )
                )

    if issues:
        return WorkflowResult(errors=tuple(issues))

    predictions = tuple(
        predict_fixture(
            statistics,
            int(row.position),
            str(row.home_team),
            str(row.away_team),
        )
        for row in ticket.sort_values("position").itertuples(index=False)
    )
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

