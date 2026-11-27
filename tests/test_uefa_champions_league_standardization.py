"""Synthetic Phase 4 policy regressions; original evidence remains private."""
import copy
import pytest
from scripts import standardize_uefa_champions_league as production
from scripts import verify_uefa_champions_league_standardization as independent
from toto_estimator.match_schema import validate_canonical_records


def event(**changes):
    e={'event_id':'synthetic','season':'2020/2021','stage':'QUALIFYING_ROUND_3','first_listed':'Alpha','second_listed':'Beta',
       'football_date':'2020-09-01','source_date':'2020-09-01','accepted_result':[1,1],'regulation_time':[1,1],
       'after_extra_time':[2,1],'shootout':[8,7],'aggregate':[12,12], 'outcome':'X','disposition':'INCLUDE',
       'result_basis':'SUPPORTED_REGULATION','neutral_venue':1,'replay':False,'applied_decisions':[]}
    e.update(changes);return e


def policy():return {'event_overrides':{}}


@pytest.mark.parametrize('reg,aet',[
    ([2,1],[2,2]),([1,2],[4,2]),([3,1],[4,1]),([1,0],[1,1]),
    ([1,0],[1,1]),([0,1],[1,1]),([2,1],[3,1]),([3,3],[4,3])])
def test_all_eight_approved_score_repair_shapes_preserve_regulation(reg,aet):
    outcome='X' if reg[0]==reg[1] else '1' if reg[0]>reg[1] else '2'
    e=event(regulation_time=reg,accepted_result=reg,after_extra_time=aet,outcome=outcome)
    original=copy.deepcopy(e);row,_=production.project(e,policy())
    assert [row['home_goals'],row['away_goals']]==reg and e==original
    assert validate_canonical_records([row])==1


@pytest.mark.parametrize('source,football,season',[
    ('2001-08-21','2001-09-08','2001/2002'),('2001-07-25','2001-07-24','2001/2002'),
    ('2013-12-11','2013-12-10','2013/2014'),('2020-12-09','2020-12-08','2020/2021')])
def test_all_four_date_repair_shapes_use_original_football_date(source,football,season):
    row,_=production.project(event(source_date=source,football_date=football,season=season),policy())
    assert row['date']==football and row['season']==season


@pytest.mark.parametrize('disposition',['HOLD OUT','NOT PLAYED','OUT OF SCOPE'])
def test_excluded_attempts_cannot_be_projected(disposition):
    with pytest.raises(ValueError,match='Excluded'):production.project(event(disposition=disposition),policy())


def test_extra_time_and_shootout_cannot_replace_regulation_or_outcome():
    with pytest.raises(ValueError,match='Extra-time'):production.project(event(accepted_result=[2,1],outcome='1'),policy())
    with pytest.raises(ValueError,match='outcome'):production.project(event(outcome='1'),policy())


def test_played_administrative_exception_remains_distinct_from_observed_score():
    e=event(accepted_result=[3,0],administrative_result=[3,0],regulation_time=None,observed_regulation_time=None,
            partial_played_score=[0,1],outcome='1',result_basis='RETROSPECTIVE_PLAYED_ADMINISTRATIVE_EXCEPTION',applied_decisions=[{'synthetic':'approved'}])
    row,_=production.project(e,policy());assert (row['home_goals'],row['away_goals'])==(3,0)
    assert e['regulation_time'] is None and e['partial_played_score']==[0,1]


@pytest.mark.parametrize('season,stage,expected',[
    ('1993/1994','SEMIFINAL',0),('2020/2021','QUALIFYING_ROUND_1',0),('2020/2021','QUALIFYING_ROUND_3',0),
    ('2019/2020','ROUND_OF_16',0),('2019/2020','QUARTERFINAL',1),('2019/2020','SEMIFINAL',1),
    ('2011/2012','FINAL',1),('2024/2025','FINAL',1),('2024/2025','LEAGUE_PHASE',0),('2025/2026','KNOCKOUT_PLAYOFF',0),
    ('1992/1993','PRELIMINARY',0),('2018/2019','PRELIMINARY_SEMIFINAL',1),('2023/2024','PRELIMINARY_FINAL',1),
    ('2030/2031','UNKNOWN',None)])
def test_format_rules_ignore_physical_venue_and_single_leg_assumptions(season,stage,expected):
    e=event(season=season,stage=stage,football_date=f'{season[:4]}-09-01',venue='Nominal home club usual stadium',single_leg=True)
    assert production.classify_format(e,policy())[0]==expected
    assert independent.expected_neutral(e)==expected


def test_neutral_override_is_source_bound_and_not_all_replays():
    e=event(replay=True)
    p={'event_overrides':{'synthetic':{'expected':{'season':e['season'],'football_date':e['football_date']},'value':1,'rule':'APPROVED_NEUTRAL_REPLAY'}}}
    assert production.classify_format(e,p)==(1,'APPROVED_NEUTRAL_REPLAY')
    assert production.classify_format(e,policy())[0]==0
    with pytest.raises(ValueError,match='identity changed'):production.classify_format(event(football_date='2020-09-02'),p)


def test_neutral_change_never_changes_orientation_ids_goals_or_toto_outcome():
    e=event(historical_home='Approved Historic Alpha',neutral_venue=1)
    before,_=production.project(e,policy())
    after,_=production.project(e,{'event_overrides':{'synthetic':{'expected':{},'value':1,'rule':'APPROVED'}}})
    assert {k:v for k,v in before.items() if k!='neutral_venue'}=={k:v for k,v in after.items() if k!='neutral_venue'}
    assert before['home_team']=='Approved Historic Alpha' and before['away_team']=='Beta'
    assert before['home_goals']==before['away_goals']==1 and e['outcome']=='X'
