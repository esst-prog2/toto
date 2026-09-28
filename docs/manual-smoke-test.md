# Streamlit MVP manual smoke test

Run `streamlit run app.py`, then verify each item in a fresh browser session.

- [ ] The app opens without an error and shows fourteen prefilled ticket positions; position 14 is labelled `14 (+1)`.
- [ ] The prefilled teams match `data/sample_ticket.csv` and every row has editable home and away dropdowns.
- [ ] Selecting **Generate predictions** displays one table containing all fourteen positions and only `1`, `X`, or `2` predictions.
- [ ] Expanding **Show rating details** displays home rating, away rating, and rating difference for all fourteen positions, with no generator strengths.
- [ ] Editing a row to use the same team at home and away, then submitting, displays a message naming that position and displays no prediction table.
- [ ] Editing another row to duplicate an existing unordered pair, then submitting, identifies every position involved in the duplicate and displays no prediction table.
- [ ] All current dropdown selections remain unchanged after validation errors.
- [ ] `data/sample_ticket.csv` is byte-for-byte unchanged after edits.
- [ ] Restarting the Streamlit process restores the original sample ticket selections.

Record the smoke test date and result in the implementation handoff when all items pass.

## Implementation verification record

On 2026-09-28, the same checklist was exercised through Streamlit's application-testing runtime because the in-app browser connection was unavailable. All checks passed, including exact startup defaults, successful fourteen-row output, rating details, atomic same-team and duplicate-pair errors, preserved edits, unchanged CSV bytes, and clean-session restoration. The live Streamlit server also started successfully on port 8501.
