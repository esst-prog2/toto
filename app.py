"""Local Streamlit interface for the synthetic-data Toto MVP."""

from dataclasses import asdict
from pathlib import Path
import sys

# Streamlit executes this repository-root file as a script. Add the src-layout
# package explicitly so the documented launch command does not depend on an
# editable-install .pth file being honored by the local Python installation.
SOURCE_ROOT = Path(__file__).resolve().parent / "src"
if str(SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ROOT))

import pandas as pd
import streamlit as st

from toto_estimator.config import HISTORICAL_DATA_PATH, SAMPLE_TICKET_PATH
from toto_estimator.data import load_historical_data, load_ticket_data
from toto_estimator.models import DataValidationError
from toto_estimator.service import run_workflow
from toto_estimator.ticket import validate_ticket

st.set_page_config(page_title="Toto Estimator", page_icon="⚽", layout="wide")
st.title("Toto Estimator")
st.caption(
    "Framework-focused MVP using fixed synthetic history and transparent rules—not a calibrated betting model."
)


@st.cache_data
def load_startup_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    return load_historical_data(HISTORICAL_DATA_PATH), load_ticket_data(
        SAMPLE_TICKET_PATH
    )


try:
    history, sample_ticket = load_startup_data()
except DataValidationError as exc:
    st.error("Startup data is invalid.")
    for issue in exc.issues:
        st.error(issue.message)
    st.stop()

teams = sorted(set(history["home_team"]) | set(history["away_team"]))
startup_issues = validate_ticket(sample_ticket, teams)
if startup_issues:
    st.error("The committed sample ticket is invalid.")
    for issue in startup_issues:
        st.error(issue.message)
    st.stop()

if "ticket" not in st.session_state:
    st.session_state.ticket = sample_ticket.copy(deep=True)
if "workflow_result" not in st.session_state:
    st.session_state.workflow_result = None

st.subheader("13+1 ticket")
st.write("Edit any fixture, then generate all fourteen predictions together.")

for index, row in st.session_state.ticket.iterrows():
    position = int(row["position"])
    label = "14 (+1)" if position == 14 else str(position)
    position_column, home_column, separator_column, away_column = st.columns(
        [1, 4, 1, 4]
    )
    position_column.markdown(f"**{label}**")
    old_home = str(row["home_team"])
    old_away = str(row["away_team"])
    home = home_column.selectbox(
        f"Home team for position {position}",
        teams,
        index=teams.index(old_home),
        key=f"home_team_{position}",
        label_visibility="collapsed",
    )
    separator_column.markdown("**vs**")
    away = away_column.selectbox(
        f"Away team for position {position}",
        teams,
        index=teams.index(old_away),
        key=f"away_team_{position}",
        label_visibility="collapsed",
    )
    if home != old_home or away != old_away:
        st.session_state.ticket.at[index, "home_team"] = home
        st.session_state.ticket.at[index, "away_team"] = away
        st.session_state.workflow_result = None

if st.button("Generate predictions", type="primary", width="stretch"):
    st.session_state.workflow_result = run_workflow(
        history, st.session_state.ticket.copy(deep=True)
    )

result = st.session_state.workflow_result
if result is not None and result.errors:
    st.error("Correct the affected ticket positions before generating predictions.")
    for issue in result.errors:
        st.error(issue.message)
elif result is not None and result.success:
    st.subheader("Predictions")
    prediction_rows = []
    detail_rows = []
    for prediction in result.predictions:
        values = asdict(prediction)
        position_label = (
            "14 (+1)" if prediction.position == 14 else str(prediction.position)
        )
        prediction_rows.append(
            {
                "Position": position_label,
                "Home team": prediction.home_team,
                "Away team": prediction.away_team,
                "Prediction": prediction.prediction,
            }
        )
        detail_rows.append(
            {
                "Position": position_label,
                "Home team": prediction.home_team,
                "Away team": prediction.away_team,
                "Home rating": values["home_rating"],
                "Away rating": values["away_rating"],
                "Rating difference": values["rating_difference"],
            }
        )
    st.dataframe(pd.DataFrame(prediction_rows), hide_index=True, width="stretch")
    with st.expander("Show rating details"):
        st.dataframe(
            pd.DataFrame(detail_rows).style.format(
                {
                    "Home rating": "{:.3f}",
                    "Away rating": "{:.3f}",
                    "Rating difference": "{:+.3f}",
                }
            ),
            hide_index=True,
            width="stretch",
        )
