"""Synthetic Phase 4 tests: no private files, source rows or network access."""
from copy import deepcopy
from types import SimpleNamespace
import json
from pathlib import Path
import pytest
from scripts import standardize_uefa_europa_league as s
from scripts import verify_uefa_europa_league_standardization as v

@pytest.mark.parametrize('name,expected',[
 ('Alpha','alph'),('A','a000'),('AB','ab00'),('A B','a0b0'),('Alpha Beta Gamma','albe'),
 ('Álpha-Béta','albe'),('1. FC Alpha','alph'),('1 FC Alpha Beta','albe'),
 ('FC Alpha','fcal'),('1 Alpha','10al'),('Øst Łódź','øsło'),('123','1230')])
def test_confirmed_abbreviation_rules(name,expected):assert v.abbreviation(name)==expected

@pytest.mark.parametrize('name',['','!!!','1. FC'])
def test_no_usable_name_rejected(name):
 with pytest.raises(ValueError):v.abbreviation(name)

def fixture():
 e=dict(event_id='fixture-a',disposition='INCLUDE',season='2010/2011',competition='UEFA Europa League',team_identities=['alpha-id','beta-id'],historical_home='Alpha',historical_away='Beta',score=dict(regulation_time=[1,1],regulation_outcome='X'),date=dict(date='2010-08-01',confidence='SOURCE_SUPPORTED'),duration=dict(regulation_completed=True),venue=dict(neutral_venue=0),modelling_eligibility=dict(outcome=True,goals=True,chronological=True))
 mapping={s.mapping_key(e['season'],t):dict(standardized_name=n)for t,n in zip(e['team_identities'],['Alpha','Beta'])}
 convention=SimpleNamespace(season_code=lambda season:season[2:4]+season[7:9],date_code=lambda day:day[2:4]+day[5:7]+day[8:10],team_code=v.abbreviation)
 return e,mapping,convention

def test_final_schema_and_identifier_separate_from_old_sha():
 e,m,c=fixture();r,outcome,old=s.project(e,m,c,'uefael')
 assert tuple(r)==s.COLUMNS and len(r['match_id'])==24 and len(old)==64
 assert r['match_id']=='uefael1011100801alphbeta' and outcome=='X'
 assert list(r.values())[1:]==['uefa','UEFA Europa League','2010/2011','2010-08-01','Alpha','Beta',1,1,0]

@pytest.mark.parametrize('score,outcome',[([2,0],'1'),([0,3],'2'),([0,0],'X')])
def test_regulation_outcome(score,outcome):
 e,m,c=fixture();e['score'].update(regulation_time=score,regulation_outcome=outcome)
 assert s.project(e,m,c,'uefael')[1]==outcome

@pytest.mark.parametrize('score',[None,[1],[1,-1],[1,1.0],[True,1],['1',1]])
def test_invalid_or_missing_goals_rejected(score):
 e,m,c=fixture();e['score']['regulation_time']=score
 with pytest.raises(ValueError):s.project(e,m,c,'uefael')

@pytest.mark.parametrize('change',[
 {'disposition':'HOLD OUT'}, {'score':{'regulation_time':[1,1],'regulation_outcome':'1'}},
 {'duration':{'regulation_completed':False}}, {'date':{'date':'2010-02-30','confidence':'SUPPORTED'}},
 {'date':{'date':'2013-08-01','confidence':'SUPPORTED'}}, {'date':{'date':'2010-08-01','confidence':'ESTIMATED_INTERVAL'}},
 {'competition':'Other Cup'}, {'venue':{'neutral_venue':True}}, {'venue':{'neutral_venue':None}},
 {'modelling_eligibility':{'outcome':True,'goals':False,'chronological':True}},
 ])
def test_ineligible_or_corrupted_input_rejected(change):
 e,m,c=fixture();e.update(change)
 with pytest.raises(ValueError):s.project(e,m,c,'uefael')

def test_historical_competition_label_retained():
 e,m,c=fixture();e.update(season='2000/2001',competition='UEFA Cup');e['date']['date']='2000-08-01';m={s.mapping_key(e['season'],t):dict(standardized_name=n)for t,n in zip(e['team_identities'],['Alpha','Beta'])}
 assert s.project(e,m,c,'uefael')[0]['league']=='UEFA Cup'

def test_admin_extra_time_shootout_and_aggregate_cannot_replace_regulation():
 e,m,c=fixture();e.update(administrative_result=[0,3]);e['score'].update(after_extra_time=[1,2],shootout=[4,5],aggregate=[3,3]);e['duration'].update(extra_time_completed=False,abandonment_period='EXTRA_TIME',score_at_abandonment=[1,2])
 r,_,_=s.project(e,m,c,'uefael');assert(r['home_goals'],r['away_goals'])==(1,1)

def test_neutral_format_preserves_orientation_and_identity():
 e,m,c=fixture();a=s.project(e,m,c,'uefael')[0];e['venue']['neutral_venue']=1;b=s.project(e,m,c,'uefael')[0]
 assert a['match_id']==b['match_id'] and b['home_team']=='Alpha'and b['away_team']=='Beta'and b['neutral_venue']==1

def test_goals_do_not_enter_identity():
 e,m,c=fixture();a=s.project(e,m,c,'uefael')[0];e['score'].update(regulation_time=[3,1],regulation_outcome='1');b=s.project(e,m,c,'uefael')[0]
 assert a['match_id']==b['match_id']

def test_different_legs_and_replay_dates_are_distinct():
 e,m,c=fixture();a=s.project(e,m,c,'uefael')[0];e['team_identities'].reverse();b=s.project(e,m,c,'uefael')[0];e['date']['date']='2010-08-08';d=s.project(e,m,c,'uefael')[0]
 assert len({r['match_id']for r in(a,b,d)})==3

def test_abbreviations_can_collide_without_same_club_identity():
 assert v.abbreviation('Alpha Beta')==v.abbreviation('Alpine Betis')
 assert s.mapping_key('2010/2011','one')!=s.mapping_key('2010/2011','two')

def test_missing_team_mapping_rejected():
 e,m,c=fixture();m.clear()
 with pytest.raises(KeyError):s.project(e,m,c,'uefael')

def test_same_participant_rejected():
 e,m,c=fixture()
 for r in m.values():r['standardized_name']='Alpha'
 with pytest.raises(ValueError):s.project(e,m,c,'uefael')

def test_mapping_is_deterministic_and_not_fuzzy():
 e,_,_=fixture();ref={'teams':{'Álpha':{},'Beta':{},'Alpine':{}}}
 a=s.prepare_mapping([e],ref);b=s.prepare_mapping([e],ref)
 assert a==b and {r['standardized_name']for r in a}=={'Álpha','Beta'}
 assert not any('Alpine'in r['existing_registry_candidates']for r in a)

def test_mapping_keeps_distinct_seasonal_identities():
 e,_,_=fixture();b=deepcopy(e);b['event_id']='fixture-b';b['season']='2011/2012'
 assert len(s.prepare_mapping([e,b],{'teams':{}}))==4

@pytest.mark.parametrize('raw',[b'\xef\xbb\xbfmatch_id\n',b'match_id\r\n'])
def test_noncanonical_encoding_rejected(raw):
 with pytest.raises(ValueError):v.parse_csv(raw)

def test_no_public_output_even_when_build_is_stubbed(tmp_path,monkeypatch):
 monkeypatch.setattr(s,'build',lambda:{'fixture.csv':b'a\n'})
 with pytest.raises(ValueError):s.run(s.ROOT/'data'/'public-phase4-test')
 assert not(s.ROOT/'data/public-phase4-test').exists()

def test_csv_roundtrip_and_column_order():
 e,m,c=fixture();r,_,_=s.project(e,m,c,'uefael');raw=s.serialize_csv([r],s.COLUMNS)
 parsed=v.parse_csv(raw);assert parsed[0]==v.COLUMNS and parsed[1]==[str(x)for x in r.values()]

def test_proposed_prefix_does_not_change_algorithm():
 e,m,c=fixture();r,_,_=s.project(e,m,c,'uefael');assert r['match_id']==v.reconstructed_identifier('uefael',e['season'],e['date']['date'],'Alpha','Beta')

def test_bound_date_correction_preserves_accepted_original():
 e,m,c=fixture();e['date']['original_dates']=['2010-08-01','2010-08-08'];before=deepcopy(e)
 rule=dict(event_id=e['event_id'],field='date',before='2010-08-01',after='2010-08-08',evidence=[{'source':'synthetic'}])
 original=s.project(e,m,c,'uefael')[0];corrected=s.project(e,m,c,'uefael',rule)[0]
 assert corrected['date']=='2010-08-08'and original['match_id']!=corrected['match_id']and e==before

@pytest.mark.parametrize('change',[{'event_id':'other'},{'before':'2010-07-01'},{'after':'2010-09-09'},{'evidence':[]}])
def test_unbound_date_correction_rejected(change):
 e,m,c=fixture();e['date']['original_dates']=['2010-08-01','2010-08-08'];rule=dict(event_id=e['event_id'],field='date',before='2010-08-01',after='2010-08-08',evidence=[{'source':'synthetic'}]);rule.update(change)
 with pytest.raises(ValueError):s.project(e,m,c,'uefael',rule)
