import pytest

from toto_estimator.outcomes import outcome_from_goals


@pytest.mark.parametrize(
    ("home", "away", "expected"),
    [(2, 0, "1"), (0, 2, "2"), (0, 0, "X"), (3, 3, "X")],
)
def test_outcome_is_from_home_perspective(home, away, expected) -> None:
    assert outcome_from_goals(home, away) == expected
