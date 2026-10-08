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


def test_shared_venue_scale_preserves_uniform_home_advantage() -> None:
    # Equal teams each win 2-0 at home. Separate venue scales would turn
    # every constant column into 0.5 and erase the advantage completely.
    matches = pd.DataFrame(
        [
            {"home_team": "A", "away_team": "B", "home_goals": 2, "away_goals": 0},
            {"home_team": "B", "away_team": "A", "home_goals": 2, "away_goals": 0},
        ]
    )
    statistics = calculate_team_statistics(matches)
    for metric in ("ppm", "gdpm"):
        assert statistics[f"home_{metric}_norm"].tolist() == [1.0, 1.0]
        assert statistics[f"away_{metric}_norm"].tolist() == [0.0, 0.0]
        assert statistics[f"overall_{metric}_norm"].tolist() == [0.5, 0.5]


def test_shared_venue_scale_has_common_reference_and_preserves_missing_rates() -> None:
    matches = pd.DataFrame(
        [
            {"home_team": "A", "away_team": "B", "home_goals": 2, "away_goals": 0},
            {"home_team": "B", "away_team": "A", "home_goals": 1, "away_goals": 1},
            {"home_team": "A", "away_team": "C", "home_goals": 0, "away_goals": 1},
        ]
    )
    statistics = calculate_team_statistics(matches)
    # Pooled PPM bounds are 0 and 3; pooled GDPM bounds are -2 and 1.
    assert statistics.at["A", "home_ppm_norm"] == pytest.approx(0.5)
    assert statistics.at["A", "away_ppm_norm"] == pytest.approx(1 / 3)
    assert statistics.at["A", "home_gdpm_norm"] == pytest.approx(5 / 6)
    assert statistics.at["A", "away_gdpm_norm"] == pytest.approx(2 / 3)
    # Equal rates at different venues map to exactly the same value.
    assert statistics.at["B", "home_ppm_norm"] == statistics.at["A", "away_ppm_norm"]
    assert statistics.at["B", "home_gdpm_norm"] == statistics.at["A", "away_gdpm_norm"]
    assert pd.isna(statistics.at["C", "home_ppm_norm"])
    assert pd.isna(statistics.at["C", "home_gdpm_norm"])
    # Overall PPM still uses its own [0.5, 3] bounds.
    assert statistics.at["A", "overall_ppm_norm"] == pytest.approx(1 / 3)
    assert statistics.at["B", "overall_ppm_norm"] == 0.0
    assert statistics.at["C", "overall_ppm_norm"] == 1.0
    for metric in ("ppm", "gdpm"):
        pd.testing.assert_series_equal(
            statistics[f"overall_{metric}_norm"],
            normalize_series(statistics[f"overall_{metric}"]),
            check_names=False,
        )


def test_shared_venue_scale_remains_neutral_when_pooled_rates_are_tied() -> None:
    matches = pd.DataFrame(
        [{"home_team": "A", "away_team": "B", "home_goals": 0, "away_goals": 0}]
    )
    statistics = calculate_team_statistics(matches)
    for metric in ("ppm", "gdpm"):
        assert statistics.at["A", f"home_{metric}_norm"] == 0.5
        assert statistics.at["B", f"away_{metric}_norm"] == 0.5
        assert pd.isna(statistics.at["A", f"away_{metric}_norm"])
        assert pd.isna(statistics.at["B", f"home_{metric}_norm"])
