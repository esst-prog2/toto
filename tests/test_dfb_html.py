"""Synthetic DFB layout regressions; no live access or private fixture required."""
import pytest

from toto_estimator.dfb_html import parse_dfb_matchday


def row(number=1, home='Home &amp; Club', away='Away', score='2 : 1', date='08.08.1990', season='1990-1991', matchday=1):
    return f'''<div class="extra c-MatchTable-row">
    <div id="match_{number}">Mittwoch, {date} 20:00 Uhr</div>
    <div class="c-MatchTable-team--home"><a>{home}</a><img alt="ignored logo"></div>
    <div class="c-MatchTable-score"><a href="https://datencenter.dfb.de/datencenter/bundesliga/{season}/{matchday}-spieltag/game-{number}">{score}</a></div>
    <div class="c-MatchTable-team--away"><img><a>{away}</a></div></div>'''


def page(rows=None, season='1990-1991', matchday=1, distractions=''):
    rows=row(season=season,matchday=matchday) if rows is None else rows
    return f'''<!doctype html><html><head><meta charset="utf-8">
    <link rel="canonical" href="https://datencenter.dfb.de/de/competitions/bundesliga/seasons/{season}/matchday/{matchday}"></head><body>
    <select name="season_id"><option>other</option><option selected value="{season}">season</option></select>
    <select name="matchday_id"><option selected="selected" value="{matchday}">day</option></select>
    <turbo-frame id="league_matches"><div class="c-MatchTable-head">{row(900)}</div>
    <div class="c-MatchTable-body">{rows}</div>{distractions}</turbo-frame>
    <table><tr><td>Home</td><td>9:4</td><td>18</td></tr></table></body></html>'''


def test_scoped_results_ignore_headers_standings_cross_tables_and_scripts():
    html=page(distractions=row(999,score='99:99')+'<table><tr><td>4:2</td></tr></table><script>"3:1"</script>')
    result=parse_dfb_matchday(html,expected_season='1990/91',expected_matchday=1,expected_matches=1)
    assert not result.issues and result.candidate_rows==1
    assert result.records==[dict(season='1990/1991',matchday=1,date='1990-08-08',home_team='Home & Club',away_team='Away',home_goals=2,away_goals=1)]
    assert parse_dfb_matchday(html).records==result.records


def test_supports_ten_matches_without_fixed_nine_assumption():
    rows=''.join(row(i,home=f'H{i}',away=f'A{i}',season='1991-1992',date='10.08.1991') for i in range(10))
    result=parse_dfb_matchday(page(rows,season='1991-1992'),expected_matches=10)
    assert len(result.records)==10 and not result.issues


def test_short_season_slug_and_later_matchday():
    html=page(row(season='2023-24',matchday=34,date='18.05.2024'),season='2023-24',matchday=34)
    result=parse_dfb_matchday(html,expected_season='2023/2024',expected_matchday=34)
    assert result.season=='2023/2024' and result.matchday==34


@pytest.mark.parametrize('change',[dict(score='- : -'),dict(score='1:1 (0:0)'),dict(score='1:1 n.V.'),
                                    dict(score='LIVE'),dict(date='31.02.1990'),dict(date='10.08.1992'),
                                    dict(home=''),dict(home='Away'),dict(season='1991-1992')])
def test_ambiguous_or_invalid_rows_reported_and_count_gate_fails(change):
    html=page(row(**change))
    result=parse_dfb_matchday(html)
    assert not result.records and len(result.issues)==1
    with pytest.raises(ValueError,match='expected 1 matches'):
        parse_dfb_matchday(html,expected_matches=1)


def test_duplicate_match_is_reported_not_accepted_twice():
    result=parse_dfb_matchday(page(row()+row()))
    assert len(result.records)==1 and 'duplicate' in result.issues[0]['message']


@pytest.mark.parametrize('transform',[
    lambda s:s.replace('id="league_matches"','id="other"'),
    lambda s:s.replace('class="c-MatchTable-body"','class="unknown"'),
    lambda s:s.replace('value="1990-1991"','value="1991-1992"'),
    lambda s:s.replace('/de/competitions/bundesliga/','/de/competitions/dfb-pokal/'),
    lambda s:s.replace('datencenter.dfb.de/de/','untrusted.example/de/'),
])
def test_layout_or_page_identity_mismatch_fails_closed(transform):
    with pytest.raises(ValueError):parse_dfb_matchday(transform(page()))


def test_missing_page_or_wrong_expected_metadata_rejected():
    with pytest.raises(ValueError):parse_dfb_matchday('blocked or loading')
    with pytest.raises(ValueError,match='unexpected season'):parse_dfb_matchday(page(),expected_season='1991/92')
    with pytest.raises(ValueError,match='unexpected matchday'):parse_dfb_matchday(page(),expected_matchday=2)


def test_rescheduled_fixture_retains_actual_date_and_original_matchday():
    rows = row(1, home='Other', away='Club', season='2005-2006', matchday=14, date='26.11.2005')
    rows += row(2, home='Historical Name', away='Visitor', season='2005-2006', matchday=14, date='06.12.2005')
    result = parse_dfb_matchday(page(rows, season='2005-2006', matchday=14), expected_matches=2)
    assert result.records[1]['date'] == '2005-12-06'
    assert result.records[1]['matchday'] == 14
    assert result.records[1]['home_team'] == 'Historical Name'


@pytest.mark.parametrize('score', ['-:-', 'abgesagt', 'verlegt', 'abgebrochen'])
def test_unfinished_rows_are_reported_without_zero_score_substitution(score):
    result = parse_dfb_matchday(page(row() + row(2, home='Other', score=score)))
    assert len(result.records) == 1 and len(result.issues) == 1
    with pytest.raises(ValueError, match='expected 2 matches'):
        parse_dfb_matchday(page(row() + row(2, home='Other', score=score)), expected_matches=2)


def test_duplicate_fixture_with_distinct_source_ids_is_flagged():
    result = parse_dfb_matchday(page(row(1) + row(2)))
    assert len(result.records) == 1 and 'duplicate' in result.issues[0]['message']


def test_numeric_live_score_is_not_certified_finished_known_limitation():
    # Documents a required acquisition gate: numeric text alone cannot prove finality.
    html = page(row().replace('extra c-MatchTable-row', 'extra c-MatchTable-row live'))
    result = parse_dfb_matchday(html)
    assert len(result.records) == 1
    assert 'status' not in result.records[0]


def test_reschedule_snapshots_need_season_wide_identity_reconciliation():
    # Per-page date-inclusive checks cannot merge pre/post-rescheduling snapshots.
    result = parse_dfb_matchday(page(row(1) + row(2, date='09.08.1990')))
    assert len(result.records) == 2
