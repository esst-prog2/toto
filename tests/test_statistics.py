import pandas as pd
import pytest

from toto_estimator.statistics import (
    calculate_team_statistics,
    normalize_series,
    team_observations,
)


def test_team_observations_and_aggregates_are_team_relative() -> None:
    matches = pd.DataFrame(
        [
            {"home_team": "A", "away_team": "B", "home_goals": 2, "away_goals": 0},
            {"home_team": "B", "away_team": "A", "home_goals": 1, "away_goals": 1},
            {"home_team": "A", "away_team": "C", "home_goals": 0, "away_goals": 1},
        ]
    )
    observations = team_observations(matches)
    assert len(observations) == 6
    statistics = calculate_team_statistics(matches)
    assert statistics.at["A", "overall_matches"] == 3
    assert statistics.at["A", "overall_ppm"] == pytest.approx(4 / 3)
    assert statistics.at["A", "overall_gdpm"] == pytest.approx(1 / 3)
    assert statistics.at["A", "home_matches"] == 2
    assert statistics.at["A", "home_ppm"] == pytest.approx(1.5)
    assert statistics.at["A", "away_matches"] == 1
    assert statistics.at["A", "away_ppm"] == pytest.approx(1.0)
    assert statistics.at["B", "overall_ppm"] == pytest.approx(0.5)
    assert statistics.at["C", "away_ppm"] == pytest.approx(3.0)


def test_min_max_normalization_and_tied_series() -> None:
    values = pd.Series([2.0, 4.0, 3.0], index=["low", "high", "middle"])
    normalized = normalize_series(values)
    assert normalized.to_dict() == {"low": 0.0, "high": 1.0, "middle": 0.5}
    tied = normalize_series(pd.Series([7.0, 7.0], index=["A", "B"]))
    assert tied.to_dict() == {"A": 0.5, "B": 0.5}

