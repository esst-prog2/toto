"""Synthetic feasibility guards: no private historical data or network requests."""
from copy import deepcopy
from itertools import permutations

import pytest

from scripts.validate_la_liga_feasibility import assess,historical,text_results
from scripts.collect_la_liga_feasibility import SOURCES


def test_only_three_approved_datasets_and_immutable_revisions():
    files=[(repo,sha,p) for repo,sha,_,paths in SOURCES for p in paths]
    assert len(files)==3 and all(len(sha)==40 for _,sha,_ in files)
    assert {p for _,_,p in files}=={'data-raw/spain.csv','2012-13/1-liga.txt','2025-26/1-liga.txt'}


def test_old_fixture_format_year_inheritance_utf8_and_crlf():
    raw='= Primera División 2012/13\r\n▪ Matchday 1\r\nSat Aug 18 2012\r\n19:00  Alpha  v Béta  2-1 (1-0)\r\nTue Jan 1\r\nBéta  v Alpha  0-0\r\n'.encode()
    rows,notes=text_results(raw,2012)
    assert [(r['date'],r['home'],r['away'],r['hg'],r['ag']) for r in rows]==[
        ('2012-08-18','Alpha','Béta','2','1'),('2013-01-01','Béta','Alpha','0','0')]
    assert not any(n['kind']=='weekday_mismatch' for n in notes)


def test_scorer_lines_not_counted_as_matches():
    raw=b'= Spain | Primera Division 2025/26\n\n\xe2\x96\xaa Regular Season - 1\nFri Aug 15 2025\n19:00  Alpha  2-1 (0-1)  Beta\n (One 50\'(p), Two 60\';\n Three 10\')\n'
    rows,notes=text_results(raw,2025)
    assert len(rows)==1 and rows[0]['hg']=='2'
    assert sum(n['kind']=='scorer_annotation' for n in notes)==2


@pytest.mark.parametrize('raw',[
    '= Wrong league\n',
    '= Primera Division\n▪ Playoff\n',
    '= Primera Division\nUNKNOWN ROW\n',
    '= Primera Division\n▪ Matchday 1\nAlpha  v Beta  1-0\n',
    '= Primera Division\n▪ Matchday 1\nFri Aug 15 2025\nAlpha  1-0  Beta\n (unclosed\n',
])
def test_unknown_competition_stage_text_and_unclosed_annotation_fail(raw):
    with pytest.raises(ValueError):text_results(raw.encode(),2025)


def full_rows():
    return [dict(source_line=i+1,home=f'Club {h}',away=f'Club {a}',hg='1',ag='0',date=f'2012-09-{i+1:02}')
            for i,(h,a) in enumerate(permutations(range(3),2))]


def test_pair_coverage_balanced_appearances_and_missing_scores():
    rows=full_rows();before=deepcopy(rows)
    assert assess(rows,2012,3)['status']=='STRUCTURAL_PASS'
    assert rows==before
    rows[-1]['hg']=None
    report=assess(rows,2012,3)
    assert report['scored']==5 and 'missing_or_invalid_scores' in report['issues']


@pytest.mark.parametrize('change,issue',[
    ('duplicate','duplicate_pairings'),('score','missing_or_invalid_scores'),('date','date_errors'),
    ('collision','same_team_date_collisions'),('team','invalid_teams'),('FT','FT_score_disagreement')])
def test_structural_guards(change,issue):
    rows=full_rows()
    if change=='duplicate':rows[-1]=dict(rows[0])
    if change=='score':rows[0]['ag']='-1'
    if change=='date':rows[0]['date']='2014-01-01'
    if change=='collision':rows[1]['date']=rows[0]['date']
    if change=='team':rows[0]['away']=rows[0]['home']
    if change=='FT':rows[0]['FT']='9-9'
    assert issue in assess(rows,2012,3)['issues']


def test_missing_fixture_and_normalized_name_collision_are_visible():
    rows=full_rows();assert 'fixture_count' in assess(rows[:-1],2012,3)['issues']
    rows[0]['home']='club 0'
    assert 'normalized_team_collisions' in assess(rows,2012,3)['issues']


def test_historical_csv_requires_schema_shape_and_utf8():
    with pytest.raises(ValueError):historical(b'Date,Season\n2012-01-01,2011\n')
    with pytest.raises(UnicodeDecodeError):historical(b'\xff')
