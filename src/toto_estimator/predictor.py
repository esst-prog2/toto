"""Fixed, transparent 1/X/2 prediction rules for the MVP."""

import pandas as pd

from .config import (
    DRAW_THRESHOLD,
    GOAL_DIFFERENCE_WEIGHT,
    MIN_TOTAL_MATCHES,
    MIN_VENUE_MATCHES,
    OVERALL_WEIGHT,
    POINTS_WEIGHT,
    VENUE_WEIGHT,
)
from .models import Prediction, ValidationIssue


def history_issues(
    statistics: pd.DataFrame,
    position: int,
    home_team: str,
    away_team: str,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for team, venue, venue_column in (
        (home_team, "home", "home_matches"),
        (away_team, "away", "away_matches"),
    ):
        if team not in statistics.index:
            issues.append(
                ValidationIssue(
                    "unknown_team",
                    f"Position {position}: {team} is not found in the historical data.",
                    position=position,
                )
            )
            continue
        total = int(statistics.at[team, "overall_matches"])
        venue_count = int(statistics.at[team, venue_column])
        if total < MIN_TOTAL_MATCHES:
            issues.append(
                ValidationIssue(
                    "insufficient_total_history",
                    f"Position {position}: {team} has {total} total historical matches; at least {MIN_TOTAL_MATCHES} are required.",
                    position=position,
                )
            )
        if venue_count < MIN_VENUE_MATCHES:
            issues.append(
                ValidationIssue(
                    "insufficient_venue_history",
                    f"Position {position}: {team} has {venue_count} historical {venue} matches; at least {MIN_VENUE_MATCHES} are required.",
                    position=position,
                )
            )
    return issues


def _component(statistics: pd.DataFrame, team: str, prefix: str) -> float:
    return float(
        POINTS_WEIGHT * statistics.at[team, f"{prefix}_ppm_norm"]
        + GOAL_DIFFERENCE_WEIGHT * statistics.at[team, f"{prefix}_gdpm_norm"]
    )


def fixture_ratings(
    statistics: pd.DataFrame, home_team: str, away_team: str
) -> tuple[float, float, float]:
    home_rating = (
        OVERALL_WEIGHT * _component(statistics, home_team, "overall")
        + VENUE_WEIGHT * _component(statistics, home_team, "home")
    )
    away_rating = (
        OVERALL_WEIGHT * _component(statistics, away_team, "overall")
        + VENUE_WEIGHT * _component(statistics, away_team, "away")
    )
    difference = home_rating - away_rating
    return home_rating, away_rating, difference


def outcome_from_difference(difference: float) -> str:
    if difference > DRAW_THRESHOLD:
        return "1"
    if difference < -DRAW_THRESHOLD:
        return "2"
    return "X"


def predict_fixture(
    statistics: pd.DataFrame,
    position: int,
    home_team: str,
    away_team: str,
) -> Prediction:
    issues = history_issues(statistics, position, home_team, away_team)
    if issues:
        raise ValueError("; ".join(issue.message for issue in issues))
    home_rating, away_rating, difference = fixture_ratings(
        statistics, home_team, away_team
    )
    return Prediction(
        position=position,
        home_team=home_team,
        away_team=away_team,
        prediction=outcome_from_difference(difference),
        home_rating=home_rating,
        away_rating=away_rating,
        rating_difference=difference,
    )

