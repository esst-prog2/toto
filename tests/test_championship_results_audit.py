"""Synthetic Tier 2 tests; no private dataset or network required."""
import csv

import pytest

from scripts.validate_championship_results import championship_audit, historical_name
from scripts.validate_england_results import audit

FIELDS = 'Date Season HomeTeam AwayTeam Score hGoal aGoal Division Tier Result'.split()


def match(**changes):
    return dict(dict(zip(FIELDS, ['1990-08-25', '1990/1991', 'A', 'B', '1-0', '1', '0', historical_name(1990), '2', 'H'])), **changes)


def write_source(tmp_path, rows):
    path = tmp_path/'source.csv'
    with path.open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    return path


@pytest.mark.parametrize('year,name', [(1990,'Football League Second Division'), (1991,'Football League Second Division'), (1992,'Football League First Division'), (2003,'Football League First Division'), (2004,'Football League Championship'), (2015,'Football League Championship'), (2016,'EFL Championship')])
def test_historical_names(year, name):
    assert historical_name(year) == name


def test_complete_round_robin_missing_season_and_ongoing(tmp_path):
    teams = [f'Team {i:02d}' for i in range(24)]
    rows = [match(HomeTeam=h, AwayTeam=a) for h in teams for a in teams if h != a]
    rows += [match(Date='2026-08-14', Season='2026/2027', Division='EFL Championship', HomeTeam=h, AwayTeam=teams[(i+1)%24]) for i,h in enumerate(teams)]
    fields,total,selected,issues,summary,checks = championship_audit(write_source(tmp_path,rows))
    assert total == len(selected) == 576
    assert summary[0]['matches'] == summary[0]['expected_matches_from_observed_teams'] == 552
    assert summary[0]['status'] == 'PASS'
    assert summary[1]['status'] == 'REVIEW'  # Absent season not silently skipped.
    assert summary[-1]['status'] == 'ONGOING'
    assert all(c['status']=='ABSENT' for c in checks)
    assert audit(write_source(tmp_path, rows))[2] == []  # PL defaults unchanged.


def test_errors_and_extra_playoff_are_preserved_and_flagged(tmp_path):
    rows = [match(), match(), match(HomeTeam='C', AwayTeam='D'),
            match(HomeTeam='C', AwayTeam='D'), match(Date='', HomeTeam='', hGoal=''),
            match(Score='2-0',Result='A'), match(Division='Premier League'),
            match(Date='1990-09-01'),
            match(Date='1991-06-02', HomeTeam='Brighton and Hove Albion', AwayTeam='Notts County')]
    _,_,selected,issues,summary,checks=championship_audit(write_source(tmp_path, rows))
    assert len(selected)==len(rows)
    assert {'duplicate_match','conflicting_duplicate','repeated_ordered_pair','invalid_date','invalid_teams',
            'invalid_goals','score_mismatch','result_mismatch','historical_name',
            'known_playoff_in_regular_extract'} <= {i['code'] for i in issues}
    assert summary[0]['status']=='REVIEW'
    assert checks[0]['status']=='PRESENT'
