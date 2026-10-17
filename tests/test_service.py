from pathlib import Path

import pandas as pd
import pytest

from toto_estimator.config import HISTORICAL_DATA_PATH, SAMPLE_TICKET_PATH
from toto_estimator.data import load_historical_data, load_ticket_data
from toto_estimator.service import run_workflow, run_workflow_from_files


def test_service_returns_all_predictions_atomically() -> None:
    result = run_workflow_from_files(HISTORICAL_DATA_PATH, SAMPLE_TICKET_PATH)
    assert result.success
    assert result.errors == ()
    assert len(result.predictions) == 14
    assert [prediction.position for prediction in result.predictions] == list(range(1, 15))
    assert {prediction.prediction for prediction in result.predictions} <= {"1", "X", "2"}


def test_service_returns_no_partial_predictions_on_error() -> None:
    history = load_historical_data(HISTORICAL_DATA_PATH)
    ticket = load_ticket_data(SAMPLE_TICKET_PATH)
    ticket.loc[ticket["position"] == 14, "away_team"] = "Team D"
    result = run_workflow(history, ticket)
    assert not result.success
    assert result.predictions == ()
    assert any(issue.position == 14 for issue in result.errors)


def test_service_reports_file_validation_errors(tmp_path: Path) -> None:
    invalid = tmp_path / "bad.csv"
    invalid.write_text("wrong,columns\n1,2\n", encoding="utf-8")
    result = run_workflow_from_files(invalid, SAMPLE_TICKET_PATH)
    assert not result.success
    assert result.predictions == ()
    assert result.errors[0].code == "missing_columns"



@pytest.mark.parametrize("column", ["home_team", "away_team"])
@pytest.mark.parametrize("padding", [" {}", "{} ", "\t{} \n"])
def test_service_uses_canonical_names_without_mutating_ticket(column, padding) -> None:
    history = load_historical_data(HISTORICAL_DATA_PATH)
    ticket = load_ticket_data(SAMPLE_TICKET_PATH)
    expected = run_workflow(history, ticket)
    ticket[column] = ticket[column].map(padding.format)
    original = ticket.copy(deep=True)

    actual = run_workflow(history, ticket)

    assert actual == expected
    pd.testing.assert_frame_equal(ticket, original)


def test_service_validates_normalized_duplicate_and_identical_teams() -> None:
    history = load_historical_data(HISTORICAL_DATA_PATH)
    ticket = load_ticket_data(SAMPLE_TICKET_PATH)
    ticket.loc[1, ["home_team", "away_team"]] = [" Team B", "Team A "]
    ticket.loc[2, ["home_team", "away_team"]] = [" Team A ", "Team A\t"]

    result = run_workflow(history, ticket)

    assert result.predictions == ()
    assert {issue.position for issue in result.errors if issue.code == "duplicate_pair"} == {1, 2}
    assert any(issue.code == "identical_teams" and issue.position == 3 for issue in result.errors)


def test_service_reports_normalized_unknown_team_without_raising() -> None:
    history = load_historical_data(HISTORICAL_DATA_PATH)
    ticket = load_ticket_data(SAMPLE_TICKET_PATH)
    ticket.loc[0, "home_team"] = " Unknown "

    result = run_workflow(history, ticket)

    assert result.predictions == ()
    assert any(issue.code == "unknown_team" and issue.position == 1 for issue in result.errors)
