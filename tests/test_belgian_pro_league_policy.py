"""Synthetic retrospective-selection and source-accounting safeguards."""
from copy import deepcopy
import pytest
from scripts import decide_belgian_pro_league_policy as p


def row(sid='a', **changes):
    r = dict(audit_id=sid, source='jalapic/test.csv', season='2021/2022', stage='REGULAR_SEASON',
             home='Home', away='Away', date='2022-01-15', FT='3-1', annotation='',
             source_line=2, physical_record_sha256='raw', errors=[])
    r.update(changes)
    return r


def event(**changes):
    return p.make_event([dict(kind='CSV_TXT', binding=row(**changes))], {})


def case(key, source=None):
    source = source or row()
    c = dict(id=key, date=source['date'], score=source['FT'], source_bindings=[source],
             evidence_ids=['direct_decision'], decision='Judgment published months later',
             completion='PLAYED_OR_INTERRUPTED', finality='Later appeals not exhaustively searched',
             availability='Not known on original fixture date')
    if key.endswith('_resumed'):
        c.update(kickoff='2022-01-12', completion_date='2022-01-15')
    return c


def test_policy_is_explicitly_retrospective():
    policy = p.policy()
    assert policy['result_availability_filter'] is False
    assert policy['leakage_free_historical_forecasting'] is False
    assert policy['application_or_prediction_algorithm_changes'] is False
    assert policy['rights'] == 'NOT_CLEARED_FOR_MODEL_TRAINING_OR_REDISTRIBUTION'
    assert policy['source_gap_is_not_disposition']
    assert 'SOURCE_GAP' not in p.DISPOSITIONS


@pytest.mark.parametrize('stage,season', [('REGULAR_SEASON','1995/1996'), ('CHAMPIONSHIP','2018/2019'),
 ('CHAMPIONSHIP','2021/2022'), ('EUROPE','2020/2021'), ('EUROPE','2021/2022'),
 ('EUROPE','2023/2024'), ('PLAYDOWNS','2023/2024'), ('PLAYDOWNS','2024/2025'),
 ('EUROPE_QUALIFICATION','2023/2024'), ('EUROPE_QUALIFICATION','2024/2025')])
def test_documented_top_flight_stage_eligible(stage, season):
    assert p.stage_action(stage, season)[0] == 'INCLUDE'


@pytest.mark.parametrize('stage,season', [('UNKNOWN','2021/2022'), ('TITLE_DECIDER','2008/2009'),
 ('EUROPE','2018/2019'), ('MIXED_TIER','2018/2019'), ('EUROPE_QUALIFICATION','1995/1996')])
def test_uncertain_stage_or_mixed_participation_is_held(stage, season):
    assert p.stage_action(stage, season)[0] == 'HOLD_OUT'


def test_cross_division_outside_scope():
    result = p.adjudicate(event(stage='PROMOTION_RELEGATION'))
    assert result['disposition'] == 'OUT_OF_SCOPE'
    assert result['accepted_score'] is None and not p.eligible_for_phase7(result)


def test_ordinary_source_date_and_score_preserved_without_availability_filter():
    original = event(); before = deepcopy(original)
    result = p.adjudicate(original)
    assert result['chosen_match_date'] == '2022-01-15'
    assert result['accepted_score'] == '3-1' and result['accepted_outcome'] == 'H'
    assert p.eligible_for_phase7(result)
    assert original == before
    assert result['licensing_clearance'] == 'NOT_CLEARED'


@pytest.mark.parametrize('key,action', list((k,v[0]) for k,v in p.CASE_RULES.items()))
def test_seven_case_dispositions_and_later_judgment_not_used_as_date(key, action):
    e = event(); c = case(key)
    result = p.adjudicate(e, c)
    assert result['disposition'] == action
    if action == 'INCLUDE':
        assert result['accepted_score'] == e['reported_score']
        assert result['chosen_match_date'] == ('2022-01-12' if key.endswith('_resumed') else '2022-01-15')
        assert p.eligible_for_phase7(result)
    else:
        assert result['accepted_score'] is None and result['chosen_match_date'] is None
        assert not p.eligible_for_phase7(result)


@pytest.mark.parametrize('key', ['beerschot_cercle_resumed','seraing_union_resumed'])
def test_resumption_preserves_all_originals(key):
    e = event(); c = case(key); before = deepcopy((e,c))
    result = p.adjudicate(e,c)
    assert result['original_fixture_date'] == '2022-01-15'
    assert result['completion_date'] == '2022-01-15'
    assert result['kickoff_date'] == result['chosen_match_date'] == '2022-01-12'
    assert result['representations'][0]['binding']['date'] == '2022-01-15'
    assert (e,c) == before


def test_invalid_completion_chronology_fails():
    c = case('seraing_union_resumed'); c['kickoff'] = '2022-02-01'
    with pytest.raises(ValueError, match='chronology'):
        p.adjudicate(event(),c)


def test_unreviewed_award_requires_explicit_decision():
    result = p.adjudicate(event(annotation='[awarded]'))
    assert result['disposition'] == 'HOLD_OUT'
    assert result['reason'] == 'EXCEPTION_REQUIRES_EXPLICIT_REVIEW'


def test_unusual_score_without_material_problem_not_automatically_excluded():
    result = p.adjudicate(event(FT='5-5',annotation=''))
    assert result['disposition'] == 'INCLUDE' and result['accepted_outcome'] == 'D'


def test_incomplete_snapshot_not_cancellation():
    result = p.adjudicate(event(FT=None,season='2025/2026'))
    assert result['disposition'] == 'HOLD_OUT'
    assert result['reason'] == 'MISSING_FINAL_SCORE_NOT_CANCELLATION'


def test_covid_cancelled_slots_not_invented_scores():
    result = p.adjudicate(event(FT=None,season='2019/2020',annotation='[cancelled]'))
    assert result['disposition'] == 'NOT_PLAYED'
    assert result['accepted_score'] is None and result['chosen_match_date'] is None


@pytest.mark.parametrize('changes',[dict(FT='0-0'),dict(season='2025/2026'),dict(stage='EUROPE')])
def test_unapproved_cancellation_fails(changes):
    changes = dict(FT=None,season='2019/2020',annotation='[cancelled]',**{}) | changes
    with pytest.raises(ValueError, match='Unreviewed cancellation'):
        p.adjudicate(event(**changes))


def test_unknown_case_fails():
    with pytest.raises(ValueError, match='Unapproved'):
        p.adjudicate(event(),case('new_award'))


@pytest.mark.parametrize('field,value',[('date','2022-01-14'),('score','5-0')])
def test_exception_cannot_attach_to_other_source_fact(field,value):
    c=case('union_beerschot_2022');c[field]=value
    with pytest.raises(ValueError, match='detached'):
        p.adjudicate(event(),c)


def test_exception_cannot_override_unresolved_stage():
    with pytest.raises(ValueError, match='cannot override'):
        p.adjudicate(event(stage='UNKNOWN'),case('union_beerschot_2022',row(stage='UNKNOWN')))


def test_exception_requires_complete_physical_binding():
    c=case('union_beerschot_2022');c['source_bindings'][0]['source_line']=99
    with pytest.raises(ValueError,match='physical source'):
        p.adjudicate(event(),c)


def test_conflicting_representations_are_held():
    e=p.make_event([dict(kind='CSV_TXT',binding=row()),dict(kind='CSV_TXT',binding=row('b',FT='5-0'))],{})
    r=p.adjudicate(e)
    assert r['disposition']=='HOLD_OUT' and r['accepted_score'] is None


def test_same_teams_in_distinct_stages_are_distinct_events():
    a=event();b=event(sid='b',stage='CHAMPIONSHIP')
    assert a['decision_id']!=b['decision_id']
    assert p.adjudicate(a)['disposition']==p.adjudicate(b)['disposition']=='INCLUDE'


@pytest.mark.parametrize('bad',['5:0','-1-0','01-0','1-?','',None])
def test_invalid_final_score_never_included(bad):
    if bad is None:
        assert p.adjudicate(event(FT=bad))['disposition']=='HOLD_OUT'
    else:
        with pytest.raises(ValueError,match='score'):
            p.adjudicate(event(FT=bad))


@pytest.mark.parametrize('bad',['2022-1-15','2022-02-30',None])
def test_explicit_match_date_required(bad):
    with pytest.raises(ValueError):
        p.adjudicate(event(date=bad))


def test_later_judgment_date_substitution_fails_consumer_guard():
    d=p.adjudicate(event());d['chosen_match_date']='2022-03-08'
    with pytest.raises(ValueError,match='kickoff'):
        p.eligible_for_phase7(d)


def test_mutating_kickoff_too_cannot_smuggle_judgment_date():
    d=p.adjudicate(event());d['chosen_match_date']=d['kickoff_date']='2022-03-08'
    with pytest.raises(ValueError,match='Administrative'):
        p.eligible_for_phase7(d)


def test_score_substitution_fails_consumer_guard():
    d=p.adjudicate(event());d['accepted_score']='5-0'
    with pytest.raises(ValueError,match='substitution'):
        p.eligible_for_phase7(d)


def test_noninclude_cannot_carry_screened_values():
    d=p.adjudicate(event(FT=None));d['accepted_score']='0-0'
    with pytest.raises(ValueError,match='Non-INCLUDE'):
        p.check_registry([d],['a'])


def test_registry_detects_lost_and_reused_representations():
    d=p.adjudicate(event())
    with pytest.raises(ValueError,match='Missing/reused'):
        p.check_registry([d],['a','b'])
    with pytest.raises(ValueError,match='Missing/reused'):
        p.check_registry([d,d],['a'])


@pytest.mark.parametrize('token,annotation,expected', [('1-2','[annulled]','HOLD_OUT'),('awd','[annulled]','HOLD_OUT'),('n/p','','NOT_PLAYED')])
def test_mouscron_documentary_not_promoted(token,annotation,expected):
    original=dict(audit_id='doc',score=token,annotation=annotation,date_heading='[Aug 1]')
    before=deepcopy(original)
    result=p.documentary_decisions([original])[0]
    assert result['disposition']==expected
    assert result['chosen_match_date'] is result['accepted_score'] is None
    assert result['included_in_10434_population'] is False
    assert original==before


def test_unreviewed_documentary_exception_fails():
    with pytest.raises(ValueError,match='Unreviewed'):
        p.documentary_decisions([dict(audit_id='doc',score='1-2',annotation='')])


def test_no_global_city_alias_or_score_matching_in_union():
    observations=dict(historical=[row('a'),row('b',home='Other Home')],modern={})
    groups=p.union_groups(observations,{},dict(matches=[]),dict(events=[]))
    assert len(groups)==2
    assert p.identity_ids(groups[0])!=p.identity_ids(groups[1])


def test_approved_link_does_not_rewrite_names():
    a=row('a');b=row('b',source='openfootball/test',home='Bilingual Home')
    obs=dict(historical=[a],modern={'x':[b]})
    link=dict(historical_id='a',modern_id='b',date_equal=True,score_equal=True)
    out=p.union_groups(obs,{'x':dict(links=[link])},dict(matches=[]),dict(events=[]))
    assert len(out)==1 and len(out[0])==2
    assert {rep['binding']['home'] for rep in out[0]}=={'Home','Bilingual Home'}


def test_conflicting_or_repeated_pair_not_silently_linked():
    a=row('a');b=row('b',FT='5-0')
    obs=dict(historical=[a],modern={'x':[b]})
    link=dict(historical_id='a',modern_id='b',date_equal=True,score_equal=True)
    with pytest.raises(ValueError,match='facts changed'):
        p.union_groups(obs,{'x':dict(links=[link])},dict(matches=[]),dict(events=[]))
    b['FT']='3-1'
    with pytest.raises(ValueError,match='Repeated'):
        p.union_groups(obs,{'x':dict(links=[link,link])},dict(matches=[]),dict(events=[]))


def test_recovered_continuation_does_not_become_two_events():
    h=row('a')
    doc=dict(diagnostic_event_key=['2021/2022','REGULAR',1,None,'Home','Away'],
             comparison_date='2022-01-15',comparison_score='3-1',source_ids=['start','finish'],
             representations=[dict(date='2022-01-12'),dict(date='2022-01-15')])
    link=dict(documentary=doc,historical=dict(source_id='a',source_line=2,raw_record_sha256='raw'),date_equal=True,score_equal=True)
    groups=p.union_groups(dict(historical=[h],modern={}),{},dict(matches=[link]),dict(events=[doc]))
    assert len(groups)==1 and p.identity_ids(groups[0])==['a','finish','start']
    e=p.make_event(groups[0],{'a':'REGULAR_SEASON'})
    assert e['representations_count']==3 and e['reported_score']=='3-1'
