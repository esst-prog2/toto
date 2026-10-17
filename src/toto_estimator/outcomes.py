"""Home-perspective outcomes derived from validated goal values."""


def outcome_from_goals(home_goals: int, away_goals: int) -> str:
    if home_goals > away_goals:
        return "1"
    if home_goals < away_goals:
        return "2"
    return "X"
