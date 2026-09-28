from pathlib import Path

import pandas as pd
import pytest

from toto_estimator.data import load_historical_data, load_ticket_data
from toto_estimator.models import DataValidationError


def _write(tmp_path: Path, name: str, content: str) -> Path:
    path = tmp_path / name
    path.write_text(content, encoding="utf-8")
    return path


def test_load_historical_data_parses_sorts_and_derives_result(tmp_path: Path) -> None:
    path = _write(
        tmp_path,
        "history.csv",
        "season,date,home_team,away_team,home_goals,away_goals\n"
        "S,2024-02-01,A,B,0,1\n"
        "S,2024-01-01,B,A,2,2\n",
    )
    frame = load_historical_data(path)
    assert frame["date"].dt.strftime("%Y-%m-%d").tolist() == [
        "2024-01-01",
        "2024-02-01",
    ]
    assert frame["result"].tolist() == ["X", "2"]
    assert frame["home_goals"].dtype.kind in "iu"


@pytest.mark.parametrize(
    ("content", "code"),
    [
        ("season,date,home_team,away_team,home_goals\n", "missing_columns"),
        (
            "season,date,home_team,away_team,home_goals,away_goals\nS,bad,A,B,1,0\n",
            "invalid_date",
        ),
        (
            "season,date,home_team,away_team,home_goals,away_goals\nS,2024-01-01,,B,1,0\n",
            "blank_home_team",
        ),
        (
            "season,date,home_team,away_team,home_goals,away_goals\nS,2024-01-01,A,,1,0\n",
            "blank_away_team",
        ),
        (
            "season,date,home_team,away_team,home_goals,away_goals\nS,2024-01-01,A,A,1,0\n",
            "identical_teams",
        ),
        (
            "season,date,home_team,away_team,home_goals,away_goals\nS,2024-01-01,A,B,-1,0\n",
            "invalid_goals",
        ),
        (
            "season,date,home_team,away_team,home_goals,away_goals\nS,2024-01-01,A,B,1.5,0\n",
            "invalid_goals",
        ),
    ],
)
def test_invalid_historical_data_is_rejected(
    tmp_path: Path, content: str, code: str
) -> None:
    path = _write(tmp_path, "invalid.csv", content)
    with pytest.raises(DataValidationError) as error:
        load_historical_data(path)
    assert code in {issue.code for issue in error.value.issues}


def test_ticket_loader_parses_public_schema(tmp_path: Path) -> None:
    path = _write(
        tmp_path,
        "ticket.csv",
        "position,home_team,away_team\n2, B ,A\n1,A,B\n",
    )
    frame = load_ticket_data(path)
    assert frame.to_dict("records") == [
        {"position": 2, "home_team": "B", "away_team": "A"},
        {"position": 1, "home_team": "A", "away_team": "B"},
    ]


def test_ticket_loader_rejects_bad_schema_and_position(tmp_path: Path) -> None:
    missing = _write(tmp_path, "missing.csv", "position,home_team\n1,A\n")
    bad_position = _write(
        tmp_path,
        "position.csv",
        "position,home_team,away_team\none,A,B\n",
    )
    with pytest.raises(DataValidationError) as missing_error:
        load_ticket_data(missing)
    with pytest.raises(DataValidationError) as position_error:
        load_ticket_data(bad_position)
    assert missing_error.value.issues[0].code == "missing_columns"
    assert position_error.value.issues[0].code == "invalid_position"

