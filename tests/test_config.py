from toto_estimator import config


def test_documented_configuration_constants() -> None:
    assert config.POINTS_WEIGHT == 0.70
    assert config.GOAL_DIFFERENCE_WEIGHT == 0.30
    assert config.OVERALL_WEIGHT == 0.50
    assert config.VENUE_WEIGHT == 0.50
    assert config.DRAW_THRESHOLD == 0.10
    assert config.MIN_TOTAL_MATCHES == 10
    assert config.MIN_VENUE_MATCHES == 5
    assert config.TICKET_SIZE == 14

