"""Transparent team statistics derived only from public match results."""

import pandas as pd


def _points(goals_for: int, goals_against: int) -> int:
    if goals_for > goals_against:
        return 3
    if goals_for == goals_against:
        return 1
    return 0


def team_observations(matches: pd.DataFrame) -> pd.DataFrame:
    records: list[dict[str, object]] = []
    for match in matches.itertuples(index=False):
        home_goals = int(match.home_goals)
        away_goals = int(match.away_goals)
        records.append(
            {
                "team": match.home_team,
                "venue": "home",
                "points": _points(home_goals, away_goals),
                "goals_for": home_goals,
                "goals_against": away_goals,
                "goal_difference": home_goals - away_goals,
            }
        )
        records.append(
            {
                "team": match.away_team,
                "venue": "away",
                "points": _points(away_goals, home_goals),
                "goals_for": away_goals,
                "goals_against": home_goals,
                "goal_difference": away_goals - home_goals,
            }
        )
    return pd.DataFrame.from_records(records)


def normalize_series(series: pd.Series) -> pd.Series:
    """Min-max normalize non-null values, using neutral 0.5 for ties."""

    result = pd.Series(index=series.index, dtype=float)
    valid = series.dropna().astype(float)
    if valid.empty:
        return result
    minimum = valid.min()
    maximum = valid.max()
    if maximum == minimum:
        result.loc[valid.index] = 0.5
    else:
        result.loc[valid.index] = (valid - minimum) / (maximum - minimum)
    return result


def _venue_statistics(observations: pd.DataFrame, venue: str) -> pd.DataFrame:
    subset = observations.loc[observations["venue"] == venue]
    grouped = subset.groupby("team", sort=True).agg(
        matches=("team", "size"),
        points=("points", "sum"),
        goal_difference=("goal_difference", "sum"),
    )
    grouped[f"{venue}_matches"] = grouped["matches"].astype(int)
    grouped[f"{venue}_ppm"] = grouped["points"] / grouped["matches"]
    grouped[f"{venue}_gdpm"] = grouped["goal_difference"] / grouped["matches"]
    return grouped[[f"{venue}_matches", f"{venue}_ppm", f"{venue}_gdpm"]]


def calculate_team_statistics(matches: pd.DataFrame) -> pd.DataFrame:
    observations = team_observations(matches)
    overall = observations.groupby("team", sort=True).agg(
        overall_matches=("team", "size"),
        points=("points", "sum"),
        goal_difference=("goal_difference", "sum"),
    )
    overall["overall_ppm"] = overall["points"] / overall["overall_matches"]
    overall["overall_gdpm"] = overall["goal_difference"] / overall["overall_matches"]
    overall = overall[["overall_matches", "overall_ppm", "overall_gdpm"]]

    statistics = overall.join(_venue_statistics(observations, "home"), how="left")
    statistics = statistics.join(_venue_statistics(observations, "away"), how="left")
    for column in ("home_matches", "away_matches"):
        statistics[column] = statistics[column].fillna(0).astype(int)

    for prefix in ("overall", "home", "away"):
        for metric in ("ppm", "gdpm"):
            column = f"{prefix}_{metric}"
            statistics[f"{column}_norm"] = normalize_series(statistics[column])
    return statistics

