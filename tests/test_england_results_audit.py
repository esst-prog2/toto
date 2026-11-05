"""Exercise source-specific diagnostics without network or real datasets."""
import csv

from scripts.validate_england_results import audit

FIELDS = 'Date Season HomeTeam AwayTeam Score hGoal aGoal Division Tier Result'.split()


def source(tmp_path, rows):
    path = tmp_path / 'source.csv'
    with path.open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    return path


def match(**changes):
    return dict(dict(zip(FIELDS, ['2026-08-15', '2026/2027', 'A', 'B', '2-1', '2', '1', 'Premier League', '1', 'H'])), **changes)


def test_filter_and_ongoing_separation(tmp_path):
    _, total, selected, issues, summary = audit(source(tmp_path, [match(), match(Tier='2'), match(Season='1991/1992', Date='1991-08-15')]))
    assert total == 3
    assert len(selected) == 1
    assert summary[-1]['matches'] == 1
    assert not any(i['code'] in ('match_count', 'missing_pairings') and i['season'] == '2026/2027' for i in issues)
    assert summary[0]['status'] == 'REVIEW'  # Entire absent historical season.


def test_missing_values_and_inconsistent_scores_are_reported(tmp_path):
    rows = [match(Date='', HomeTeam='', hGoal=''), match(Score='1-2', Result='A')]
    _, _, selected, issues, _ = audit(source(tmp_path, rows))
    assert len(selected) == 2  # Audit preserves anomalous rows.
    codes = {i['code'] for i in issues}
    assert {'invalid_date', 'invalid_teams', 'invalid_goals', 'score_mismatch', 'result_mismatch'} <= codes


def test_duplicate_conflicts_and_pairings(tmp_path):
    rows = [match(), match(), match(hGoal='3', Score='3-1'), match(Date='2026-09-01')]
    _, _, selected, issues, _ = audit(source(tmp_path, rows))
    assert len(selected) == 4
    assert {'conflicting_duplicate', 'repeated_ordered_pair'} <= {i['code'] for i in issues}
