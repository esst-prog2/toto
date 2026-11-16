# TOTOdology promotional page: content draft

Status: Draft for review. Page copy is below; editorial notes are not website copy.

## 1. Introduction

# TOTOdology
### Football predictions you can follow.

Choosing outcomes for a 14-match football ticket means comparing many pairs of teams. TOTOdology brings those picks into one place and makes the reasoning visible.

Explore how football results can become a 1/X/2 prediction. Build a 13+1 match ticket in the current demo and see the simple rating rules behind every pick.

**Try the local demo** · **Explore the code**

The demo uses synthetic football results and sample teams. It is an educational prototype with no verified real-world accuracy claim.

## 2. Who it’s for

### Curious about the reasoning behind a prediction?

TOTOdology is for football fans curious about Toto-style tickets, and learners who want to explore a transparent approach to football statistics. It brings 14 match picks into one table and lets you inspect the ratings behind them.

You can start with the prefilled sample ticket, choose different home and away teams from the demo’s lists, and compare the resulting predictions.

## 3. How predictions work

### From results to a clear pick

1. **Look at team performance.** The program calculates average points per match and average goal difference: goals scored minus goals conceded.
2. **Include home and away records.** Each team’s rating combines its overall record with its record at the relevant venue: home for the host, away for the visitor.
3. **Compare the ratings.** When the ratings are close, the rule selects **X** (draw). With a larger gap, it selects **1** (home win) if the home rating is higher, or **2** (away win) if the away rating is higher.

Click **Generate predictions** to see all 14 picks. Open **Show rating details** to inspect the home rating, away rating and their difference.

## 4. Try it yourself

### Run the demo on your computer

Get the project from [GitHub](https://github.com/esst-prog2/toto). You’ll need Python 3.11 or later. From the downloaded repository’s root folder, create and activate a virtual environment, install the project, and start Streamlit.

For macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install .
streamlit run app.py
```

On Windows, create the environment with `py -m venv .venv` and activate it in PowerShell with `.venv\Scripts\Activate.ps1`, then run the same installation and launch commands.

Open the local address printed by Streamlit. Keep the sample ticket or edit the team selections, then click **Generate predictions**. If the ticket has an invalid selection, fix the reported issue and try again.

**[Explore TOTOdology on GitHub](https://github.com/esst-prog2/toto)**

## 5. What to expect

### A small demo with visible reasoning

The current application runs locally with fixed synthetic history. It shows outcome picks and rating details. Its rules are designed to be understandable; they do not establish reliable betting performance or guarantee results.

---

## Editorial notes and evidence (not website copy)

- **Positioning:** The user chose a simple, professional, English-language page explaining the existing application. The audience wording is a proposed positioning choice, not evidence of user research. TOTOdology is the project name supplied by the user; the current application window says “Toto Estimator.”
- **Source hierarchy:** [README](../README.md) supplies the project purpose, Toto context and stated limitations. Its “demo” and “first useful version” also describe planned probabilities, backtesting, competition selection and partial evaluation. Those are not current UI capabilities and are deliberately omitted from the page copy. No development accuracy figures are used.
- **Current behaviour:** [Manual smoke-test guide](manual-smoke-test.md), [application](../app.py), [configuration](../src/toto_estimator/config.py) and [workflow](../src/toto_estimator/service.py) support the 14-position sample ticket, fixed demo files, control labels, rating display and whole-ticket validation. The demo files are public synthetic examples, not the privately collected league archives.
- **Method:** [Statistics](../src/toto_estimator/statistics.py) and [prediction rules](../src/toto_estimator/predictor.py) support the points/goal-difference explanation, venue-specific ratings and draw band. The draw band is checked before choosing the higher-rated side; no outcome probabilities are implied.
- **Local setup:** [Project metadata](../pyproject.toml) declares Python >=3.11 and runtime dependencies. The minimal runtime installation above is derived from that package configuration; [dependency environment notes](dependency-environment.md) document a fuller development install and its compatibility limits. The launch command is documented in the smoke-test guide. The virtual-environment commands are setup guidance, not a quotation from the README. A fresh installation, including Windows execution, was not performed for this content-only step.
- **Links:** The repository URL matches the configured Git remote. “Try the local demo” is intended to link to the setup section on the eventual page. There is no hosted application URL or one-click online demo.
- **gstack /office-hours:** Used Builder mode’s premise checking and alternative framing for this content draft. A task-first explanation was compared with a longer learning narrative; the concise explanation follows the user’s stated single-page direction. The supplied brief settled the purpose and scope, so no new discovery interview, external research, optional cross-model brainstorming, or visual design was run. The separate local office-hours brief passed the skill’s independent spec review with no findings. This is a draft, not a claim of user approval of the wording.
- **Next action:** Review the headline, proposed audience and synthetic-demo wording before the separate Impeccable design step. No content decision blocks review of this draft.
