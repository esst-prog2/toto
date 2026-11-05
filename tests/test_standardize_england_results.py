"""Synthetic source adapter regressions; no private data required."""
import csv
import hashlib
import io
import json

import pytest

from scripts.standardize_england_results import LEAGUE, convert_rows
from toto_estimator.data import load_historical_data
from toto_estimator.historical_import import OUTPUT_COLUMNS


def match(**changes):
    return dict(dict(Date='1992-08-15', Season='1992/1993', HomeTeam='A', AwayTeam='B',
                     hGoal='2', aGoal='1', Score='2-1', Result='H', Division='Premier League', Tier='1'), **changes)


def test_reuses_existing_identity_and_preserves_match_facts(tmp_path):
    rows = [match(), match(Date='1993-05-01', HomeTeam='B', AwayTeam='A', hGoal='0', aGoal='0', Score='0-0', Result='D')]
    content, summary = convert_rows(rows, tmp_path)
    repeated, _ = convert_rows(list(reversed(rows)), tmp_path)
    assert content == repeated
    parsed = list(csv.DictReader(io.StringIO(content.decode())))
    assert tuple(parsed[0]) == OUTPUT_COLUMNS
    identity = [LEAGUE, '1992/1993', '1992-08-15', 'A', 'B']
    assert parsed[0]['match_id'] == hashlib.sha256(json.dumps(identity, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
    assert parsed[0]['date'] == rows[0]['Date']
    assert parsed[0]['home_goals'] == '2'
    assert len(load_historical_data(io.StringIO(content.decode()))) == 2
    assert summary['accepted'] == 2
    assert not list(tmp_path.iterdir())  # Bridge removed.


@pytest.mark.parametrize('change', [dict(Result='A'), dict(Score='3-1'), dict(Tier='2'), dict(Division='Championship'), dict(HomeTeam=' A '), dict(hGoal=''), dict(Season='1992/93')])
def test_anomalies_fail_instead_of_normalizing_or_dropping(tmp_path, change):
    with pytest.raises(ValueError):
        convert_rows([match(**change)], tmp_path)
    assert not list(tmp_path.iterdir())


@pytest.mark.parametrize('second', [dict(), dict(hGoal='3', Score='3-1'), dict(Date='1992-09-01')])
def test_duplicate_fixture_is_fatal_even_on_another_date(tmp_path, second):
    with pytest.raises(ValueError, match='importer|duplicate'):
        convert_rows([match(), match(**second)], tmp_path)
