# The Pick Sheet promotional page: revised content

Status: Revised 2026-11-21 for user review; no final variant selected. Website language remains English. Five sections and A/B/C visual designs are preserved.

## What was outdated

The earlier draft made the synthetic MVP the product identity, intentionally omitted the agreed future capabilities, and presented the points/goal-difference rating and draw band as the central product explanation. Those rules describe the prototype, not a selected future probability model. The copy was accurate about the demo but incomplete as a description of the intended product.

## Source authority and verified boundaries

- README sections Demo, Shape, Size and How We Would Know It Works in both worktrees describe the agreed target: 14 manual competition/team selections, historical data, three outcome probabilities, recommendations, one results table and a previous-meeting comparison.
- `openspec/changes/finalize-homework-8-demo/design.md`, `specs/homework-8-demo/spec.md` and `tasks.md` distinguish this target from delivered functionality. Implementation tasks remain unchecked. Historical reconstruction must use only information available before the previous meeting, including fitting and parameter selection; one match is not aggregate validation.
- `app.py`, `src/toto_estimator/service.py`, `predictor.py` and the smoke-test guide establish the current fictional-team, fixed-synthetic-history prototype, rating details and whole-ticket validation. It has no competition picker, probabilities or historical-comparison UI. Planned per-match availability is not existing error behavior.
- Data collection/validation documents show historical-data preparation, not integration into the application. README source-rights limits justify the permitted-small-demo or synthetic fallback; no league coverage or performance claim is added.
- The statistical probability method is still to be selected and evaluated. Existing rating differences are not probabilities, and earlier development accuracy is not evidence for the future model.
- Setup commands and Python >=3.11 remain grounded in project metadata and existing launch documentation. No fresh dependency installation or platform certification was performed.

## Revised website copy (in reading order)

Football predictions you can follow.

Fourteen matches. Three possible outcomes each. The Pick Sheet is being developed to help you compare the possibilities before filling out a Toto ticket.

The goal: choose your matches, see the estimated chances of a home win, draw or away win, and review a recommended pick for every match in one clear table. Try the local demoExplore the code

In development. This page describes the intended experience. The local prototype currently uses synthetic results and fictional teams; probabilities and previous-meeting comparisons are not available yet.

More context for every pick

For football fans weighing up a Toto ticket, a single pick tells only part of the story. The planned table will put the three outcome probabilities beside the recommendation, helping you see when the alternatives are close.

You will also be able to look back at the teams’ most recent meeting: what the model would have predicted before that match, what actually happened, and whether the pick matched the result.

Your 14 matches, in perspective

The planned experience — not yet available in the prototype

Choose your matches.

Manually enter 14 matches by choosing the competition, home team and away team for each row. Then select Predict.

Compare the possibilities.

A statistical model will use historical football results to estimate the chances of a home win, draw and away win. The table will show all three probabilities and recommend the most likely outcome for each match.

Check the last meeting.

Where reliable history allows, the same table will show a prediction reconstructed for the teams’ most recent previous meeting, alongside its actual result. That prediction must use only information available before that earlier match.

Missing data should stay visible. The planned application will flag unavailable predictions or historical comparisons for the affected match while keeping other available results. One past meeting is a useful comparison, not proof of future accuracy. 1Home winXDraw2Away win

Try the prototype today
The current local demo lets you edit a prefilled 14-match ticket of fictional teams and see rule-based picks with rating details. It has no competition selector, outcome probabilities or previous-meeting comparison. You’ll need Python 3.11 or later installed on your computer. This is a local Python application, not an online demo.
Open the GitHub repository, choose Code → Download ZIP, then extract the ZIP. Open the extracted project folder containing app.py and pyproject.toml.
Open Terminal on macOS or Linux, or PowerShell on Windows. Type cd, a space, and the full path to that extracted folder in double quotes, then press Enter. For example, cd "/full/path/to/toto-main" on macOS/Linux or cd "C:\Users\YourName\Downloads\toto-main" on Windows. Replace the example path with your own folder’s location. Keep this terminal open.
In that terminal, run the commands below for your operating system, one line at a time. They create a separate Python environment, install the project and start the prototype. The environment is used directly, so you do not need to activate it.
macOS or Linuxpython3 -m venv .venv
.venv/bin/python -m pip install .
.venv/bin/python -m streamlit run app.py
Windows · PowerShellpy -m venv .venv
.\.venv\Scripts\python.exe -m pip install .
.\.venv\Scripts\python.exe -m streamlit run app.py
Open the local address printed by Streamlit in your browser. The local prototype still opens as “Toto Estimator”. That is the existing application behind The Pick Sheet; its internal name has not changed. Keep the sample ticket or edit the team selections, then click Generate predictions. If the ticket has an invalid selection, fix the reported issue and try again. To stop the app, return to the terminal and press Ctrl+C.
Explore The Pick Sheet on GitHub

A clear goal. An honest work in progress.

Competition selection, real-history integration, probability estimates and historically valid previous-meeting comparisons remain development work. The new statistical method still needs to be selected and evaluated on previously unseen matches; no accuracy improvement or reliable betting performance has been established.

Public demos may use a smaller permitted dataset or synthetic data because some historical sources have unresolved redistribution rights. Coverage and results may differ from the full local data. Predictions are estimates, not guarantees.Explore the project
