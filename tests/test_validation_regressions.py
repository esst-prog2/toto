"""Boundary regressions use malformed inputs and independent expected results."""

import io
from decimal import Decimal

import pandas as pd
import pytest

from toto_estimator.config import HISTORICAL_DATA_PATH, SAMPLE_TICKET_PATH
from toto_estimator.data import load_historical_data, load_ticket_data, validate_historical_data
from toto_estimator.models import DataValidationError
from toto_estimator.service import run_workflow, run_workflow_from_files
from toto_estimator.ticket import validate_ticket
from toto_estimator.validation import exact_integer


@pytest.fixture
def history():
    return load_historical_data(HISTORICAL_DATA_PATH)


@pytest.fixture
def ticket():
    return load_ticket_data(SAMPLE_TICKET_PATH)


@pytest.mark.parametrize("bad", [None, [], {}, "history", pd.DataFrame(), pd.DataFrame({"wrong": [1]})])
def test_service_rejects_invalid_history_shape(bad, ticket):
    result = run_workflow(bad, ticket)
    assert result.errors
    assert result.predictions == ()


@pytest.mark.parametrize(("column", "value", "code"), [
    ("home_goals", -1, "invalid_goals"),
    ("away_goals", 1.5, "invalid_goals"),
    ("home_goals", None, "invalid_goals"),
    ("home_goals", float("inf"), "invalid_goals"),
    ("home_goals", True, "invalid_goals"),
    ("date", "bad", "invalid_date"),
    ("date", 123, "invalid_date"),
    ("date", [], "invalid_date"),
    ("home_team", " ", "blank_home_team"),
    ("away_team", None, "blank_away_team"),
    ("home_team", 123, "blank_home_team"),
    ("result", "H", "invalid_outcome"),
    ("result", None, "invalid_outcome"),
])
def test_invalid_direct_history_is_structured(history, ticket, column, value, code):
    history[column] = history[column].astype(object)
    history.at[0, column] = value
    history.index = [f"source-{i}" for i in range(len(history))]
    result = run_workflow(history, ticket)
    assert result.predictions == ()
    assert any(issue.code == code and issue.row == 2 for issue in result.errors)


def test_history_rejects_conflicting_valid_outcome(history, ticket):
    history.at[0, "result"] = "2" if history.at[0, "result"] != "2" else "1"
    assert any(i.code == "invalid_outcome" for i in run_workflow(history, ticket).errors)


def test_history_preserves_extra_columns_and_caller_input(history):
    history["source_note"] = "evidence"
    before = history.copy(deep=True)
    normalized = validate_historical_data(history)
    assert normalized.source_note.tolist() == ["evidence"] * len(history)
    pd.testing.assert_frame_equal(history, before)


@pytest.mark.parametrize("loader", [load_historical_data, load_ticket_data])
@pytest.mark.parametrize("content", [b"", b"\n\n", b"\xff"])
def test_empty_or_bad_encoding_csv_is_structured(loader, content):
    with pytest.raises(DataValidationError):
        loader(io.BytesIO(content))


def test_header_only_history_fails_before_statistics(ticket):
    content = "season,date,home_team,away_team,home_goals,away_goals\n"
    result = run_workflow_from_files(io.StringIO(content), SAMPLE_TICKET_PATH)
    assert result.predictions == ()
    assert result.errors[0].code == "empty_data"


@pytest.mark.parametrize("content,code", [
    ("position,home_team,away_team,home_team\n1,A,B,C\n", "duplicate_columns"),
    ("position,home_team,away_team\n1,A\n", "row_width"),
    ("position,home_team,away_team\n1,A,B,extra\n", "row_width"),
    ('position,home_team,away_team\n1,"A,B\n', "read_error"),
])
def test_malformed_ticket_csv(content, code):
    with pytest.raises(DataValidationError) as error:
        load_ticket_data(io.StringIO(content))
    assert error.value.issues[0].code == code
    if code == "row_width":
        assert error.value.issues[0].row == 2


@pytest.mark.parametrize("loader", [load_historical_data, load_ticket_data])
def test_invalid_file_argument_is_structured(loader):
    with pytest.raises(DataValidationError):
        loader(None)


@pytest.mark.parametrize("value", [str(2**63), str(2**64 - 1), "1e20", str(-(2**63) - 1), float("nan"), True, [], {}])
def test_exact_integer_rejects_overflow_and_unsupported_values(value):
    with pytest.raises(ValueError):
        exact_integer(value)


@pytest.mark.parametrize("value", ["1", "1.0", "1e0", Decimal("1.00"), 1, 1.0])
def test_exact_integer_preserves_supported_integral_representations(value):
    assert exact_integer(value) == 1


def test_exact_integer_checks_bounds_without_rounding():
    assert exact_integer(str(2**63 - 1)) == 2**63 - 1
    assert exact_integer(str(-(2**63))) == -(2**63)
    assert exact_integer("9007199254740993") == 9007199254740993
    with pytest.raises(ValueError):
        exact_integer("9007199254740993.1")


@pytest.mark.parametrize("value", [str(2**63), str(2**64 - 1), "1e20"])
def test_csv_numeric_overflow_is_field_and_row_specific(value):
    content = f"season,date,home_team,away_team,home_goals,away_goals\nS,2024-01-01,A,B,{value},0\n"
    with pytest.raises(DataValidationError) as error:
        load_historical_data(io.StringIO(content))
    assert error.value.issues[0].row == 2
    assert "home_goals" in error.value.issues[0].message
    with pytest.raises(DataValidationError) as error:
        load_ticket_data(io.StringIO(f"position,home_team,away_team\n{value},A,B\n"))
    assert error.value.issues[0].row == 2
    assert "position" in error.value.issues[0].message


@pytest.mark.parametrize("representation", [str, lambda v: f"{v}.0", lambda v: Decimal(v), lambda v: str(v) if v % 2 else v])
def test_service_canonical_position_order(history, ticket, representation):
    expected = run_workflow(history, ticket)
    ticket["position"] = ticket.position.map(representation)
    ticket = ticket.iloc[::-1]
    before = ticket.copy(deep=True)
    actual = run_workflow(history, ticket)
    assert actual == expected
    assert [p.position for p in actual.predictions] == list(range(1, 15))
    pd.testing.assert_frame_equal(ticket, before)


@pytest.mark.parametrize("bad", [None, [], {}, pd.DataFrame({"wrong": [1]})])
def test_bad_ticket_shape_returns_errors(history, bad):
    result = run_workflow(history, bad)
    assert result.errors and result.predictions == ()


@pytest.mark.parametrize("kind", ["history", "ticket"])
def test_duplicate_dataframe_columns_are_rejected(history, ticket, kind):
    if kind == "history":
        history = pd.concat([history, history[["home_goals"]]], axis=1)
    else:
        ticket = pd.concat([ticket, ticket[["position"]]], axis=1)
    result = run_workflow(history, ticket)
    assert result.errors[0].code == "duplicate_columns"
    assert result.predictions == ()


@pytest.mark.parametrize("value", ["bad", True, None, [], 1.5, 2**64])
def test_bad_positions_report_source_row_not_index_label(history, ticket, value):
    ticket["position"] = ticket.position.astype(object)
    ticket.at[0, "position"] = value
    ticket.index = [f"label-{i}" for i in range(14)]
    result = run_workflow(history, ticket)
    assert result.predictions == ()
    assert any(i.code == "invalid_position" and i.row == 2 for i in result.errors)


def test_detailed_position_errors(history, ticket):
    ticket.at[0, "position"] = 2
    ticket.at[2, "position"] = 15
    issues = validate_ticket(ticket, history.home_team.unique())
    assert any(i.row == 2 and "duplicated" in i.message and "2, 3" in i.message for i in issues)
    assert any(i.row == 3 and "duplicated" in i.message for i in issues)
    assert any(i.row == 4 and i.position == 15 and "out of range" in i.message for i in issues)
    assert any("Missing ticket positions: 1, 3" in i.message for i in issues)


def test_invalid_position_does_not_suppress_other_history_errors(history, ticket):
    ticket["position"] = ticket.position.astype(object)
    ticket.at[0, "position"] = "bad"
    history = history.loc[history.home_team != "Team B"]
    # Team B is still known from away matches, but has no home history.
    result = run_workflow(history, ticket)
    assert result.predictions == ()
    assert any(i.code == "invalid_position" for i in result.errors)
    assert any(i.code == "insufficient_venue_history" and i.position != 1 for i in result.errors)


@pytest.mark.parametrize("content,code", [
    ("season,date,home_team,away_team,home_goals,home_goals,away_goals\nS,2024-01-01,A,B,1,9,0\n", "duplicate_columns"),
    ("season,date,home_team,away_team,home_goals,away_goals\nS,2024-01-01,A,B,1\n", "row_width"),
    ("season,date,home_team,away_team,home_goals,away_goals\nS,2024-01-01,A,B,1,0,extra\n", "row_width"),
])
def test_malformed_history_csv_is_structured(content, code):
    with pytest.raises(DataValidationError) as error:
        load_historical_data(io.StringIO(content))
    assert error.value.issues[0].code == code


def test_csv_history_preserves_legitimate_extra_columns():
    frame = load_historical_data(io.StringIO(
        "season,date,home_team,away_team,home_goals,away_goals,source_note\n"
        "S,2024-01-01,A,B,1,0,kept\n"
    ))
    assert frame.source_note.tolist() == ["kept"]
    assert frame.result.tolist() == ["1"]


def test_empty_direct_history_is_structured(history, ticket):
    result = run_workflow(history.iloc[:0], ticket)
    assert result.predictions == ()
    assert result.errors[0].code == "empty_data"


def test_identical_historical_opponents_are_rejected(history, ticket):
    history.at[0, "away_team"] = history.at[0, "home_team"]
    result = run_workflow(history, ticket)
    assert result.predictions == ()
    assert any(i.code == "identical_teams" and i.row == 2 for i in result.errors)


def test_header_only_ticket_is_rejected_atomically(history):
    ticket = load_ticket_data(io.StringIO("position,home_team,away_team\n"))
    result = run_workflow(history, ticket)
    assert result.predictions == ()
    assert {i.code for i in result.errors} >= {"ticket_size", "ticket_positions"}


def test_late_numeric_prediction_failure_never_returns_partial_results(history, ticket, monkeypatch):
    import toto_estimator.service as service
    from toto_estimator.models import ValidationIssue
    original = service.predict_fixture
    calls = []

    def fail_late(statistics, position, home_team, away_team):
        calls.append(position)
        if position == 14:
            raise DataValidationError([ValidationIssue("invalid_rating", "Rating must be finite.", position=position)])
        return original(statistics, position, home_team, away_team)

    monkeypatch.setattr(service, "predict_fixture", fail_late)
    result = service.run_workflow(history, ticket)
    assert calls == list(range(1, 15))
    assert result.predictions == ()
    assert result.errors[0].code == "invalid_rating"
