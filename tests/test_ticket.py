from pathlib import Path

import pandas as pd

from toto_estimator.data import load_ticket_data
from toto_estimator.ticket import validate_ticket

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEAMS = [f"Team {letter}" for letter in "ABCDEF"]

EXPECTED = [
    (1, "Team A", "Team B"),
    (2, "Team C", "Team A"),
    (3, "Team A", "Team D"),
    (4, "Team E", "Team A"),
    (5, "Team A", "Team F"),
    (6, "Team B", "Team C"),
    (7, "Team B", "Team D"),
    (8, "Team B", "Team E"),
    (9, "Team F", "Team B"),
    (10, "Team C", "Team D"),
    (11, "Team E", "Team C"),
    (12, "Team F", "Team C"),
    (13, "Team D", "Team E"),
    (14, "Team D", "Team F"),
]


def test_committed_sample_ticket_is_exact_and_valid() -> None:
    ticket = load_ticket_data(PROJECT_ROOT / "data" / "sample_ticket.csv")
    assert list(ticket.itertuples(index=False, name=None)) == EXPECTED
    assert validate_ticket(ticket, TEAMS) == []
    pairs = {tuple(sorted((home, away))) for _, home, away in EXPECTED}
    assert tuple(sorted(("Team E", "Team F"))) not in pairs


def test_ticket_validation_aggregates_all_affected_positions() -> None:
    ticket = pd.DataFrame(EXPECTED, columns=["position", "home_team", "away_team"])
    ticket.loc[ticket["position"] == 2, ["home_team", "away_team"]] = [
        "Team B",
        "Team A",
    ]
    ticket.loc[ticket["position"] == 3, "away_team"] = "Team A"
    ticket.loc[ticket["position"] == 4, "home_team"] = "Unknown"
    issues = validate_ticket(ticket, TEAMS)
    duplicate_positions = {
        issue.position for issue in issues if issue.code == "duplicate_pair"
    }
    assert duplicate_positions == {1, 2}
    assert any(issue.code == "identical_teams" and issue.position == 3 for issue in issues)
    assert any(issue.code == "unknown_team" and issue.position == 4 for issue in issues)


def test_repeated_teams_are_allowed_when_pairs_differ() -> None:
    ticket = pd.DataFrame(EXPECTED, columns=["position", "home_team", "away_team"])
    assert validate_ticket(ticket, TEAMS) == []

