"""Synthetic Phase 6 gates; no private datasets or network access."""
from copy import deepcopy

import pytest

from scripts import decide_la_liga_policy as p


def policy():
    cases=[]
    for index,(identifier,_,action,start,end,h,a) in enumerate(p.SPECS,1):
        source_date=end or '2026-03-04'
        original=dict(source_line=index,date=source_date,home=f'Club A{index}',away=f'Club B{index}',hg=str(h),ag=str(a))
        c=dict(decision_id=identifier,source_file='synthetic.txt',source_sha256='0'*64,season='synthetic',
               original=original,action=action,approved_source_score=[h,a],approval='USER_APPROVED_PHASE6',
               evidence_urls=['https://example.test/decision'],original_kickoff_date=start or end,
               completion_date=end,effective_result_date=end,
               final_outcome_status='UNRESOLVED' if action=='HOLD_OUT' else
               'VERIFIED_COMPLETED_RESULT' if start else 'VERIFIED_PLAYED_RESULT')
        c['fixture_id']=p.source_id(c['source_file'],c['source_sha256'],index)
        cases.append(c)
    return dict(approval='USER_APPROVED_PHASE6',cases=cases,
                unresolved_final_outcome_ids=[cases[-1]['fixture_id']])


def fixture(case):
    result={k:deepcopy(case[k]) for k in ('fixture_id','original','source_file','source_sha256','season')}
    result['identified_final_outcome_status']='NO_CONFLICT_IDENTIFIED'
    return result


def assess(f,pol,**kwargs):
    return p.assess(f,pol,technical_status='STRUCTURAL_PASS',historical_status='UNVERIFIED',**kwargs)


@pytest.mark.parametrize('index',range(5))
def test_confirmed_source_scores_and_originals_are_unchanged(index):
    pol=policy(); c=pol['cases'][index]; f=fixture(c); before=deepcopy((f,pol))
    result=assess(f,pol)
    assert (f,pol)==before
    assert result['source_date']==f['original']['date']
    assert result['exception_policy_screenable'] is (index!=4)
    assert result['model_training_suitability']=='NOT_CLEARED'
    assert result['licensing_clearance']=='UNRESOLVED'


@pytest.mark.parametrize('index,start,end',[(2,'2004-12-12','2005-01-05'),(3,'2023-12-10','2023-12-11')])
def test_interrupted_matches_use_completion_and_preserve_kickoff(index,start,end):
    pol=policy(); result=assess(fixture(pol['cases'][index]),pol)
    assert result['original_kickoff_date']==start
    assert result['completion_date']==result['effective_result_date']==end
    assert result['availability_basis']=='APPROVED_COMPLETION_DATE'
    assert not p.known_strictly_before(end,start)
    assert not p.known_strictly_before(end,end)


def test_rayo_source_three_zero_is_neither_swapped_nor_admitted():
    pol=policy(); f=fixture(pol['cases'][4]); result=assess(f,pol)
    assert (f['original']['hg'],f['original']['ag'])==('3','0')
    assert result['screening_status']=='HOLD_OUT' and result['effective_result_date'] is None
    assert result['final_outcome_status']=='UNRESOLVED'
    assert not p.training_allowed(result,'2027-01-01')
    pol['cases'][4]['approved_source_score']=[0,3]
    with pytest.raises(ValueError,match='score'):assess(f,pol)


def other_fixture():
    f=fixture(policy()['cases'][0]); f['original']['source_line']=999
    f['fixture_id']=p.source_id(f['source_file'],f['source_sha256'],999)
    return f


def test_new_unresolved_final_outcome_fails_closed_even_with_clearances():
    f=other_fixture(); f['identified_final_outcome_status']='UNRESOLVED'
    result=assess(f,policy(),identified_final_outcome_unresolved=False)
    assert result['screening_status']=='HOLD_OUT' and result['effective_result_date'] is None
    result.update(model_training_suitability='CLEARED',licensing_clearance='CLEARED')
    assert not p.training_allowed(result,'2027-01-01')


def test_new_conflict_overrides_even_a_previously_verified_retention_decision():
    pol=policy(); f=fixture(pol['cases'][0])
    assert assess(f,pol,identified_final_outcome_unresolved=True)['screening_status']=='HOLD_OUT'


@pytest.mark.parametrize('state',['UNRESOLVED','PARTIAL','EXPLAINED'])
def test_scheduling_uncertainty_does_not_correct_or_exclude(state):
    f=other_fixture(); f['round_review_status']=state; f['diagnostic_outlier']=True
    original=deepcopy(f)
    result=assess(f,policy())
    assert result['screening_status']=='CANDIDATE_NOT_STANDARDIZED'
    assert result['historical_verification']=='UNVERIFIED'
    assert result['effective_result_date']==original['original']['date']
    assert result['availability_basis']=='SOURCE_DATE_PROXY_NOT_INDEPENDENTLY_CERTIFIED'
    assert f==original


@pytest.mark.parametrize('mutation',['missing_case','duplicate','missing_registry','wrong_action','approval',
                                     'changed_score','early_completion','wrong_binding','missing_outcome_state'])
def test_decision_registry_and_bound_facts_cannot_be_bypassed(mutation):
    pol=policy(); f=fixture(pol['cases'][2])
    if mutation=='missing_case':pol['cases'].pop()
    if mutation=='duplicate':pol['cases'][1]['fixture_id']=pol['cases'][0]['fixture_id']
    if mutation=='missing_registry':pol['unresolved_final_outcome_ids']=[]
    if mutation=='wrong_action':pol['cases'][4]['action']='RETAIN'
    if mutation=='approval':pol['approval']='UNAPPROVED'
    if mutation=='changed_score':pol['cases'][2]['approved_source_score']=[3,1]
    if mutation=='early_completion':pol['cases'][2]['effective_result_date']='2004-12-12'
    if mutation=='wrong_binding':f['original']['date']='2004-12-12'
    if mutation=='missing_outcome_state':del f['identified_final_outcome_status']
    with pytest.raises(ValueError):assess(f,pol)


def test_unknown_technical_or_history_status_is_not_accepted():
    f=other_fixture(); pol=policy()
    with pytest.raises(ValueError):p.assess(f,pol,technical_status='ASSUMED',historical_status='UNVERIFIED')
    with pytest.raises(ValueError):p.assess(f,pol,technical_status='STRUCTURAL_PASS',historical_status='CERTIFIED')
    result=p.assess(f,pol,technical_status='STRUCTURAL_FAIL',historical_status='UNVERIFIED')
    assert not result['exception_policy_screenable']


def test_technical_history_rights_training_and_time_are_separate_gates():
    f=other_fixture(); result=assess(f,policy()); prediction='2015-12-21'
    assert not p.training_allowed(result,prediction)
    result['model_training_suitability']='CLEARED'
    assert not p.training_allowed(result,prediction)
    result['licensing_clearance']='CLEARED'
    assert p.training_allowed(result,prediction)
    assert not p.training_allowed(result,'2015-12-20')
    assert not p.training_allowed(result,'2015-12-19')
    result['exception_policy_screenable']=False
    assert not p.training_allowed(result,prediction)


@pytest.mark.parametrize('effective,prediction,expected',[
    ('2005-01-05','2005-01-06',True),('2005-01-05','2005-01-05',False),
    ('2023-12-11','2023-12-10',False),(None,'2023-12-12',False)])
def test_strict_result_availability(effective,prediction,expected):
    assert p.known_strictly_before(effective,prediction) is expected


@pytest.mark.parametrize('value',['2023-12-11T22:00:00','20231211','2023-02-29','unknown',None])
def test_ambiguous_or_invalid_prediction_dates_are_rejected(value):
    with pytest.raises(ValueError):p.known_strictly_before('2023-12-11',value)


def test_source_audit_id_is_deterministic_and_sensitive_to_provenance():
    assert p.source_id('a','0'*64,1)==p.source_id('a','0'*64,1)
    assert len({p.source_id('a','0'*64,1),p.source_id('b','0'*64,1),
                p.source_id('a','1'*64,1),p.source_id('a','0'*64,2)})==4
    with pytest.raises(ValueError):p.source_id('a','bad',1)


def test_frozen_history_allows_append_but_not_rewrite_or_deletion(tmp_path):
    file=tmp_path/'history'; old=b'Existing evidence\n'
    prefixes={'history':dict(bytes=len(old),sha256=p.sha(old))}
    file.write_bytes(old+b'Approved policy\n'); p.check_append_only(prefixes,tmp_path)
    file.write_bytes(b'Changed evidence\n')
    with pytest.raises(ValueError):p.check_append_only(prefixes,tmp_path)
    file.write_bytes(old[:-1])
    with pytest.raises(ValueError):p.check_append_only(prefixes,tmp_path)
    with pytest.raises(ValueError):p.check_append_only({'../outside':prefixes['history']},tmp_path)


def test_previous_source_output_hashes_are_protected(tmp_path):
    old=tmp_path/'previous_standardized.csv'; old.write_bytes(b'previous competition output\n')
    baseline={'previous_standardized.csv':p.sha(old.read_bytes())}
    assert p.review.protect(baseline,tmp_path)==1
    old.write_bytes(b'changed\n')
    with pytest.raises(ValueError):p.review.protect(baseline,tmp_path)
