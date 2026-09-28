from toto_estimator.config import HISTORICAL_DATA_PATH, SAMPLE_TICKET_PATH
from toto_estimator.service import run_workflow_from_files


def test_canonical_inputs_complete_the_observable_workflow() -> None:
    result = run_workflow_from_files(HISTORICAL_DATA_PATH, SAMPLE_TICKET_PATH)
    assert result.success
    assert len(result.predictions) == 14
    assert [prediction.position for prediction in result.predictions] == list(range(1, 15))
    assert all(prediction.prediction in {"1", "X", "2"} for prediction in result.predictions)
    assert all(0.0 <= prediction.home_rating <= 1.0 for prediction in result.predictions)
    assert all(0.0 <= prediction.away_rating <= 1.0 for prediction in result.predictions)

