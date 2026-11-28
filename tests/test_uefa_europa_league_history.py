"""Synthetic Phase 3 checks; no copied historical fixture rows."""
from copy import deepcopy
from pathlib import Path
import pytest
from scripts import review_uefa_europa_league_history as h


def row(oid='a',score=None,*,date='2010-08-01',ids=('alpha','beta'),stage='ROUND_1',season='2010/2011',publisher='RSSSF contributors',leg=None):
 return dict(observation_id=oid,source='fixture/'+oid,source_sha256='0'*64,locator='line:1',representation='fixture',publisher=publisher,source_fields={},periods={k:None for k in ('regulation_time','half_time','after_extra_time','extra_time_only','shootout','aggregate','published_final','administrative_result')},season=season,identity_candidates=list(ids),date=date,date_interval=None,source_leg=leg,stage=stage,scope='MAIN',status='published',issues=[],home='Alpha',away='Beta',raw_home='Alpha',raw_away='Beta',replay=False,competition='UEFA Cup',raw_stage='First Round',venue=None,source_neutral_venue=None,official_neutral_candidate=0) | {'periods':{k:(score if k=='published_final'else None)for k in ('regulation_time','half_time','after_extra_time','extra_time_only','shootout','aggregate','published_final','administrative_result')}}

@pytest.mark.parametrize('score,result',[([2,1],'1'),([1,1],'X'),([0,3],'2')])
def test_outcome(score,result):assert h.outcome(score)==result

@pytest.mark.parametrize('time,expected',[('90+6',90),("45'",45),('105+2',105),('91',91),('unknown',None)])
def test_period_minute(time,expected):assert h.minute(time)==expected

def test_complete_cumulative_goals_separate_extra_time_and_stoppage():
 r=row(score=[2,1]);r['source_fields']['goal_rows']=[dict(GH=1,GA=0,time='45+3'),dict(GH=1,GA=1,time='90+4'),dict(GH=2,GA=1,time='109')]
 assert h.chronology(r)==[1,1]
 assert h.chronology(r,45)==[1,0]

@pytest.mark.parametrize('changes',[dict(GH=2,GA=0,time='3'),dict(GH=1,GA=0,time='unknown'),dict(GH=0,GA=0,time='3')])
def test_incomplete_or_invalid_cumulative_goals_do_not_supply_regulation(changes):
 r=row(score=[1,0]);r['source_fields']['goal_rows']=[changes];assert h.chronology(r)is None

def test_missing_goal_log_does_not_invent_zero():assert h.chronology(row(score=[0,0]))is None

def test_wiki_complete_goals_include_own_goal_and_stoppage():
 r=row(score=[2,1]);r['source_fields']['fields']=dict(goals1='A {{goal|20}} B {{goal|90+3|o.g.}}',goals2='C {{goal|112}}')
 assert h.chronology(r)==[2,0]


def test_pre_abolition_return_leg_score_is_not_reversed_in_numeric_result():
 first=row('first',[2,1],ids=('beta','alpha'),leg=1,date='2010-07-01');second=row('second',[3,1],leg=2);second['periods']['after_extra_time']=[3,1]
 ev=[dict(season=first['season'],identity_candidates=first['identity_candidates'],observations=['first'],_rows=[first])]
 d=h.score_decision([second],['alpha','beta'],ev)
 assert d['regulation_time']==[2,1]and d['regulation_outcome']=='1'
 assert d['method'].startswith('PRE_2021')


def test_post_abolition_aggregate_equality_does_not_supply_exact_goals():
 first=row('first',[2,1],ids=('beta','alpha'),leg=1,date='2022-07-01',season='2022/2023');second=row('second',[3,1],leg=2,season='2022/2023');second['periods']['after_extra_time']=[3,1]
 ev=[dict(season=first['season'],identity_candidates=first['identity_candidates'],observations=['first'],_rows=[first])]
 decision=h.score_decision([second],['alpha','beta'],ev)
 assert decision['regulation_time']is None and decision['regulation_outcome']=='1'


def test_extra_time_final_preserves_outcome_only_without_invented_goals():
 r=row(score=[5,4],stage='FINAL');r['periods']['after_extra_time']=[5,4];d=h.score_decision([r],r['identity_candidates'],[])
 assert d['regulation_time']is None and d['regulation_outcome']=='X'


def test_zero_bound_requires_single_match_format():
 r=row(score=[1,0],stage='FINAL');r['periods']['after_extra_time']=[1,0]
 assert h.score_decision([r],r['identity_candidates'],[])['regulation_time']==[0,0]
 r['stage']='ROUND_OF_16'
 assert h.score_decision([r],r['identity_candidates'],[])['regulation_time']is None


def test_shootout_number_cannot_become_regulation():
 r=row(score=[0,0],stage='FINAL');r['periods']['shootout']=[5,4];r['periods']['regulation_time']=[5,4]
 assert h.score_decision([r],r['identity_candidates'],[])['regulation_time']==[0,0]


def test_explicit_period_component_precedes_sparse_full_time_claim():
 r=row(score=[4,1],publisher='11footy');r['periods']['regulation_time']=[2,1];r['periods']['after_extra_time']=[4,1];r['source_fields']['home_goals_regular_time']='2'
 assert h.score_decision([r],r['identity_candidates'],[])['regulation_time']==[2,1]


def test_date_interval_not_automatically_first_or_last():
 r=row(date=None);r['date_interval']=['2010-08-03','2010-08-04'];d=h.date_decision([r]);assert d['date']is None and d['original_intervals'][0]['interval']==r['date_interval']


def test_actual_report_date_precedes_scheduled_provider_day():
 r=row(date='2010-08-05');r['source_fields']['date_source_line']=2;b=row('b',date='2010-08-03',publisher='11footy');b['status']='played'
 d=h.date_decision([r,b]);assert d['date']=='2010-08-05'and d['original_dates']==['2010-08-03','2010-08-05']

@pytest.mark.parametrize('year,stage,expected',[(1996,'FINAL',0),(1997,'FINAL',1),(2024,'GROUP_STAGE',0),(2024,'UNKNOWN',None),(2019,'QUARTERFINAL',1),(2020,'QUALIFYING_ROUND_1',0)])
def test_official_format_venue(year,stage,expected):
 r=row(stage=stage,season=f'{year}/{year+1}');r['source_neutral_venue']='1'
 assert h.venue_decision([r],stage,r['season'])['neutral_venue']==expected


def test_distinct_opposite_legs_on_same_erroneous_source_date_stay_distinct():
 a=row('a',[1,0],leg=1);b=row('b',[0,2],ids=('beta','alpha'),leg=2);b['home'],b['away']='Beta','Alpha'
 mapping={h.namespace(r,s):r['identity_candidates'][i]for r in(a,b)for i,s in enumerate(('home','away'))}
 events,_,_=h.reconcile_directed([a,b],mapping);assert len(events)==2


def test_repeated_same_source_rematches_cannot_be_merged_by_participants():
 a=row('a',[1,0]);b=row('b',[1,0],date='2010-11-01');b['source']=a['source']
 mapping={h.namespace(r,s):r['identity_candidates'][i]for r in(a,b)for i,s in enumerate(('home','away'))}
 assert len(h.reconcile_directed([a,b],mapping)[0])==2


def test_replays_remain_distinct():
 a=row('a',[1,0]);b=row('b',[1,0],date='2010-08-08');b['replay']=True
 mapping={h.namespace(r,s):r['identity_candidates'][i]for r in(a,b)for i,s in enumerate(('home','away'))}
 assert len(h.reconcile_directed([a,b],mapping)[0])==2


def test_unique_directed_bracket_can_reconcile_gross_source_date_error():
 a=row('a',[1,0]);b=row('b',[1,0],date='2010-11-01')
 mapping={h.namespace(r,s):r['identity_candidates'][i]for r in(a,b)for i,s in enumerate(('home','away'))}
 assert len(h.reconcile_directed([a,b],mapping)[0])==1
 assert a['date']=='2010-08-01'and b['date']=='2010-11-01'


def test_public_output_rejected(tmp_path):
 with pytest.raises(ValueError):h.run(tmp_path/'public-output')


def test_aggregate_footnote_recovery_preserves_original_and_recovers_return():
 r=row(score=[1,0],leg=1);r.update(locator='line:7:leg:1',associations=['ENG','FRA'],team_candidates=['alpha','beta']);r['source_fields']['raw_line']='Alpha Eng  Beta Fra  1-0  0-1  1-1p'
 r['periods']['shootout']=[1,1];before=deepcopy(r)
 allrows,fixes,added=h.repair_grid_observations([r])
 assert len(fixes)==1 and len(added)==1 and added[0]['periods']['published_final']==[1,0]
 assert added[0]['home']=='Beta'and added[0]['away']=='Alpha'
 assert before['periods']['shootout']==[1,1]and r['periods']['shootout']is None


def test_award_placeholder_does_not_shift_columns_into_aggregate_footnote_repair():
 r=row(leg=1);r['source_fields']['raw_line']='Alpha Eng  Beta Fra  awd  3-0  3-3a  9-8p'
 allrows,fixes,added=h.repair_grid_observations([r])
 assert not fixes and not added and r['periods']['published_final']is None


def test_multiple_attribute_rules_combine_without_last_write_loss():
 a=dict(source_sha256='a',decision_id='one',changes=dict(date='2000-01-02'),evidence=['date-source']);b=dict(source_sha256='a',decision_id='two',changes=dict(regulation_time=[1,0]),evidence=['score-source'])
 merged=h.combine_rules([a,b]);assert merged['changes']==dict(date='2000-01-02',regulation_time=[1,0])and merged['decision_ids']==['one','two']
 b['changes']=dict(date='2000-01-03')
 with pytest.raises(ValueError):h.combine_rules([a,b])


def test_generic_aek_does_not_merge_greek_and_cypriot_clubs():
 a=row('a',[1,0],ids=('greek','opponent'));b=row('b',[1,0],ids=('cypriot','opponent'))
 a['home']=a['raw_home']='AEK';b['home']=b['raw_home']='AEK Larnaca'
 identities=dict(labels=[dict(identity_candidate='greek',lexical_key='aek'),dict(identity_candidate='cypriot',lexical_key='aek larnaca'),dict(identity_candidate='opponent',lexical_key='beta')])
 h.expand_aliases([a,b],identities)
 assert a['identity_candidates'][0]!=b['identity_candidates'][0]


def test_generic_inter_country_occurrences_do_not_overwrite_namespace(monkeypatch):
 a=row('a',ids=('inter','opponent'));b=row('b',ids=('inter','opponent'))
 for r,country in [(a,'Italy'),(b,'Azerbaijan')]:r.update(home='Inter',raw_home='Inter',associations=[country,'England'])
 identities=dict(labels=[dict(identity_candidate='inter',identity_root=['2010/2011','inter']),dict(identity_candidate='opponent',identity_root=['2010/2011','beta'])])
 monkeypatch.setattr(h,'load',lambda p:dict(events=[dict(observations=['a']),dict(observations=['b'])]))
 mapping=h.identity_map([a,b],identities,[])
 assert a['identity_candidates'][0]!=b['identity_candidates'][0]
 assert h.namespace(a,'home')!=h.namespace(b,'home')


def test_independent_bracket_scan_handles_inline_heading_and_starred_footnote(tmp_path,monkeypatch):
 from scripts import verify_uefa_europa_league_history as verify
 base=tmp_path/'private';folder=base/'phase1/originals/rsssf';folder.mkdir(parents=True)
 (folder/'ec200001.html').write_text('<h2><a name=uefa>Target</a></h2><pre><a name=uefaq>Qualifying Phase</a>\nAlpha Eng  Beta Fra  1-0  0-1  1-1\nGamma Ger  Delta Ita  2-0  0-1  2-1*a\na UEFA Intertoto Cup Semi-Finals\nFirst Round\n</pre>')
 monkeypatch.setattr(verify,'BASE',base)
 ev=[dict(season='2000/2001',scope='QUALIFYING',status='PLAYED_SOURCE_SUPPORTED')for _ in range(2)]
 result=verify.independent_qualifying_counts(ev)
 assert len(result)==1 and result[0]['raw_bracket_fixture_descriptions']==2 and result[0]['difference']==0


def test_extra_time_abandonment_preserves_completed_regulation_eligibility():
 score=dict(regulation_time=[0,0],regulation_outcome='X');day=dict(date='2000-09-01');venue=dict(neutral_venue=0)
 assert h.model_eligibility('PLAYED_ADMINISTRATIVE_EXCEPTION',score,day,venue,regulation_completed=True)['goals']
 assert not h.model_eligibility('ABANDONED_INCOMPLETE',score,day,venue,regulation_completed=False)['outcome']
 assert not h.model_eligibility('NOT PLAYED',score,day,venue)['goals']


def test_two_leg_final_without_away_goals_needs_unique_bound():
 first=row('first',[2,1],ids=('beta','alpha'),leg=1,date='1996-05-01',season='1995/1996',stage='FINAL');second=row('second',[3,2],leg=2,date='1996-05-15',season='1995/1996',stage='FINAL');second['periods']['after_extra_time']=[3,2]
 ev=[dict(season=first['season'],identity_candidates=first['identity_candidates'],observations=['first'],_rows=[first])]
 d=h.score_decision([second],second['identity_candidates'],ev)
 assert d['regulation_time']is None and d['regulation_outcome']=='1'
 first['periods']['published_final']=[1,0];second['periods'].update(published_final=[1,0],after_extra_time=[1,0]);d=h.score_decision([second],second['identity_candidates'],ev)
 assert d['regulation_time']==[1,0]and d['method'].startswith('UNIQUE_SECOND_LEG_FINAL')


def test_unknown_venue_does_not_exclude_supported_goals():
 eligible=h.model_eligibility('PLAYED_SOURCE_SUPPORTED',dict(regulation_time=[2,1],regulation_outcome='1'),dict(date='2000-01-01'),dict(neutral_venue=None))
 assert eligible['goals']and eligible['outcome']and not eligible['venue_dependent']


def test_unknown_date_blocks_chronology_but_preserves_result():
 eligible=h.model_eligibility('PLAYED_SOURCE_SUPPORTED',dict(regulation_time=[2,1],regulation_outcome='1'),dict(date=None),dict(neutral_venue=0))
 assert eligible['goals']and eligible['outcome']and not eligible['chronological']


def test_outcome_only_record_is_not_goal_eligible():
 eligible=h.model_eligibility('PLAYED_SOURCE_SUPPORTED',dict(regulation_time=None,regulation_outcome='X'),dict(date='2000-01-01'),dict(neutral_venue=0))
 assert eligible['outcome']and eligible['chronological']and not eligible['goals']
