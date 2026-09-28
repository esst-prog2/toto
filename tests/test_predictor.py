import pandas as pd
import pytest

from toto_estimator.predictor import (
    fixture_ratings,
    history_issues,
    outcome_from_difference,
    predict_fixture,
)


def _statistics() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "overall_matches": [20, 20],
            "home_matches": [10, 10],
            "away_matches": [10, 10],
            "overall_ppm_norm": [0.8, 0.2],
            "overall_gdpm_norm": [0.6, 0.4],
            "home_ppm_norm": [0.9, 0.3],
            "home_gdpm_norm": [0.7, 0.2],
            "away_ppm_norm": [0.6, 0.1],
            "away_gdpm_norm": [0.5, 0.3],
        },
        index=["A", "B"],
    )


def test_fixture_rating_uses_fixed_weights() -> None:
    home, away, difference = fixture_ratings(_statistics(), "A", "B")
    expected_home = 0.5 * (0.7 * 0.8 + 0.3 * 0.6) + 0.5 * (
        0.7 * 0.9 + 0.3 * 0.7
    )
    expected_away = 0.5 * (0.7 * 0.2 + 0.3 * 0.4) + 0.5 * (
        0.7 * 0.1 + 0.3 * 0.3
    )
    assert home == pytest.approx(expected_home)
    assert away == pytest.approx(expected_away)
    assert difference == pytest.approx(expected_home - expected_away)
    assert 0 <= away <= home <= 1


@pytest.mark.parametrize(
    ("difference", "expected"),
    [(0.100001, "1"), (0.10, "X"), (0.0, "X"), (-0.10, "X"), (-0.100001, "2")],
)
def test_draw_threshold_is_inclusive(difference: float, expected: str) -> None:
    assert outcome_from_difference(difference) == expected


def test_prediction_contains_transparent_rating_details() -> None:
    prediction = predict_fixture(_statistics(), 4, "A", "B")
    assert prediction.position == 4
    assert prediction.prediction == "1"
    assert prediction.rating_difference == pytest.approx(
        prediction.home_rating - prediction.away_rating
    )


def test_history_issues_identify_team_venue_and_position() -> None:
    statistics = _statistics()
    statistics.at["A", "overall_matches"] = 9
    statistics.at["B", "away_matches"] = 4
    issues = history_issues(statistics, 7, "A", "B")
    assert {issue.code for issue in issues} == {
        "insufficient_total_history",
        "insufficient_venue_history",
    }
    assert all(issue.position == 7 for issue in issues)
    assert "A" in issues[0].message
    assert "away" in issues[1].message

