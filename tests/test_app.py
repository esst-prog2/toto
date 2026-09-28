import hashlib
from pathlib import Path

from streamlit.testing.v1 import AppTest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_PATH = PROJECT_ROOT / "app.py"
SAMPLE_TICKET_PATH = PROJECT_ROOT / "data" / "sample_ticket.csv"


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_streamlit_app_starts_with_ticket_and_generates_results() -> None:
    expected_values = [
        team
        for fixture in [
            ("Team A", "Team B"),
            ("Team C", "Team A"),
            ("Team A", "Team D"),
            ("Team E", "Team A"),
            ("Team A", "Team F"),
            ("Team B", "Team C"),
            ("Team B", "Team D"),
            ("Team B", "Team E"),
            ("Team F", "Team B"),
            ("Team C", "Team D"),
            ("Team E", "Team C"),
            ("Team F", "Team C"),
            ("Team D", "Team E"),
            ("Team D", "Team F"),
        ]
        for team in fixture
    ]
    before = _digest(SAMPLE_TICKET_PATH)
    app = AppTest.from_file(APP_PATH, default_timeout=15).run()
    assert not app.exception
    assert len(app.selectbox) == 28
    assert [selectbox.value for selectbox in app.selectbox] == expected_values
    assert len(app.button) == 1
    app.button[0].click().run()
    assert not app.exception
    assert len(app.dataframe) == 2
    predictions = app.dataframe[0].value
    details = app.dataframe[1].value
    assert len(predictions) == 14
    assert predictions.iloc[-1]["Position"] == "14 (+1)"
    assert set(predictions["Prediction"]) <= {"1", "X", "2"}
    assert list(details.columns[-3:]) == [
        "Home rating",
        "Away rating",
        "Rating difference",
    ]
    assert len(app.expander) == 1
    assert app.expander[0].label == "Show rating details"
    assert _digest(SAMPLE_TICKET_PATH) == before


def test_streamlit_validation_is_atomic_and_preserves_edits() -> None:
    before = _digest(SAMPLE_TICKET_PATH)
    app = AppTest.from_file(APP_PATH, default_timeout=15).run()

    app.selectbox[1].select("Team A").run()
    assert len(app.dataframe) == 0
    app.button[0].click().run()
    assert len(app.dataframe) == 0
    assert app.selectbox[1].value == "Team A"
    assert any("Position 1" in error.value for error in app.error)

    app.selectbox[1].select("Team B").run()
    app.selectbox[2].select("Team B").run()
    app.button[0].click().run()
    assert len(app.dataframe) == 0
    error_text = " ".join(error.value for error in app.error)
    assert "Position 1" in error_text
    assert "Position 2" in error_text
    assert app.selectbox[2].value == "Team B"
    assert _digest(SAMPLE_TICKET_PATH) == before


def test_new_streamlit_session_restores_sample_ticket() -> None:
    edited = AppTest.from_file(APP_PATH, default_timeout=15).run()
    edited.selectbox[1].select("Team A").run()
    assert edited.selectbox[1].value == "Team A"

    restarted = AppTest.from_file(APP_PATH, default_timeout=15).run()
    assert restarted.selectbox[0].value == "Team A"
    assert restarted.selectbox[1].value == "Team B"
