"""Synthetic Phase 6 policy guards; no private data, network or app mutation."""
from copy import deepcopy
import json

import pytest

from scripts import decide_segunda_policy as p


def case(key):
    y,n=key;s=p.expected_specs()[key];act=s['action'];h,a=(None,None) if s['FT'] is None else s['FT'].split('-')
    file=f'openfootball/espana/{y}-{(y+1)%100:02}/2-liga2.txt'
    r=dict(season=f'{y}/{y+1}',source_line=n,source_file=file,source_sha256=p.HASHES[y],source_commit=p.review.structural.base.PIN,
           date=s['date'],home=s['home'],away=s['away'],FT=s['FT'],hg=h,ag=a,
           annotation='[awarded]' if act=='UNRESOLVED_HOLD_OUT' else '',source_marked_awarded=act=='UNRESOLVED_HOLD_OUT')
    r['source_fixture_id']=p.review.structural.source_id(file,p.HASHES[y],n)
    held=act in {'UNRESOLVED_HOLD_OUT','CONDITIONAL_HOLD_OUT'}
    ev=({'cordoba'} if n==754 else {'missing42'}) if act=='SUPPLEMENT_MISSING_SCORE' else (
        {'reus_expulsion','reus_awards','reus_court','reus_tad'}|({'reus_suspend'} if n==376 else set())) if act=='UNRESOLVED_HOLD_OUT' else (
        {'high64'} if key==(2014,82) else {'high66'} if key==(2014,291) else
        {'rayo_result','rayo_schedule','rayo_appeal'} if key==(2019,346) else
        {'dep_result','dep_schedule','dep_archive','dep_tad'})
    dates=dict(source=r['date'],scheduled=None,kickoff=None if act=='UNRESOLVED_HOLD_OUT' else r['date'],
               completion=None if act=='UNRESOLVED_HOLD_OUT' else r['date'],individual_administrative_decision=None,
               expulsion_decision='2019-01-28' if act=='UNRESOLVED_HOLD_OUT' else None,intermediate_schedule=None)
    if act=='COMPLETED_INTERRUPTED_MATCH':dates['kickoff']='2019-12-15'
    if act=='CONDITIONAL_HOLD_OUT':dates.update(scheduled='2020-07-20',intermediate_schedule='2020-08-05')
    identifier=f'SD6-{sorted(p.expected_specs()).index(key)+1:02}'
    return dict(decision_id=identifier,fixture_id=r['source_fixture_id'],original=r,action=act,approval=p.PROPOSED if act=='CONDITIONAL_HOLD_OUT' else p.APPROVAL,
                evidence=[dict(id=e,url=p.EVIDENCE_BINDINGS[e][0],source_entry_sha256=p.EVIDENCE_BINDINGS[e][1],access=p.EVIDENCE_BINDINGS[e][2]) for e in sorted(ev)],
                phase5_claim_sha256=p.CLAIM_HASHES[key],phase5_status='UNRESOLVED' if act=='UNRESOLVED_HOLD_OUT' else 'VERIFIED',
                result=s.get('result'),effective_result_date=None if held else s['date'],event_dates=dates,
                finality='UNRESOLVED' if act=='UNRESOLVED_HOLD_OUT' else 'PARTIAL_SECONDARY_CLOSURE_EVIDENCE' if act=='CONDITIONAL_HOLD_OUT' else
                'NO_FINAL_OUTCOME_CONFLICT_IDENTIFIED_NOT_EXHAUSTIVELY_CERTIFIED')


def policy():
    cs=[case(key) for key in sorted(p.expected_specs())]
    groups=[dict(source_label=n,parent='Synthetic parent '+str(i),apply_mapping=False,keep_separate_from_parent=True) for i,n in enumerate(sorted(p.review.structural.RESERVES))]
    return dict(phase=6,approval=p.APPROVAL,cases=cs,global_team_mappings={},standardized_output_generated=False,
                uncertainty=dict(identity_groups=groups),
                unresolved_hold_ids=sorted(c['fixture_id'] for c in cs if c['action']=='UNRESOLVED_HOLD_OUT'),
                conditional_hold_ids=sorted(c['fixture_id'] for c in cs if c['action']=='CONDITIONAL_HOLD_OUT'))


def ordinary():
    r=deepcopy(case((2014,82))['original']);r.update(source_line=999,home='Ordinary home',away='Ordinary away',FT='2-1',hg='2',ag='1')
    r['source_fixture_id']='synthetic:ordinary'
    return r


@pytest.mark.parametrize('line,date,home,away,result',p.SUPPLEMENTS)
def test_all_nine_supplements_are_additive_and_evidence_bound(line,date,home,away,result):
    c=case((2024,line));r=deepcopy(c['original']);before=deepcopy(r)
    a=p.assess(r,policy())
    assert r==before and r['FT'] is None and r['hg'] is None and r['ag'] is None
    assert a['source_result'] is None and a['policy_result']==result
    assert a['effective_result_date']==date and a['score_supplement']
    assert a['exception_policy_screenable'] and not p.training_allowed(a,'2026-01-01')


@pytest.mark.parametrize('line',p.AWARD_LINES)
def test_all_twenty_one_reus_awards_remain_held(line):
    c=case((2018,line));r=deepcopy(c['original']);before=deepcopy(r);a=p.assess(r,policy())
    assert r==before and a['source_result']==r['FT'] and r['annotation']=='[awarded]'
    assert a['screening_status']=='UNRESOLVED_HOLD_OUT' and a['effective_result_date'] is None
    assert a['policy_result'] is None and not a['exception_policy_screenable']
    a.update(model_training_suitability='CLEARED',licensing_clearance='CLEARED')
    assert not p.training_allowed(a,'2030-01-01')


def test_rayo_preserves_kickoff_uses_completion_and_prevents_leakage():
    pol=policy();c=case((2019,346));a=p.assess(c['original'],pol)
    assert c['event_dates']['kickoff']=='2019-12-15'
    assert a['policy_result']=='1-0' and a['effective_result_date']=='2020-06-10'
    a.update(model_training_suitability='CLEARED',licensing_clearance='CLEARED')
    assert not p.training_allowed(a,'2019-12-16')
    assert not p.training_allowed(a,'2020-06-10')
    assert p.training_allowed(a,'2020-06-11')


def test_deportivo_additional_hold_is_proposed_not_user_approved():
    c=case((2019,722));a=p.assess(c['original'],policy())
    assert c['approval']==p.PROPOSED
    assert c['event_dates']['scheduled']=='2020-07-20' and c['event_dates']['completion']=='2020-08-07'
    assert a['source_result']==a['policy_result']=='2-1'
    assert a['screening_status']=='CONDITIONAL_HOLD_OUT_PENDING_REVIEW'
    assert a['effective_result_date'] is None and not a['exception_policy_screenable']


@pytest.mark.parametrize('key',[(2014,82),(2014,291)])
def test_unusual_scores_not_capped_or_replaced(key):
    c=case(key);a=p.assess(c['original'],policy())
    assert a['source_result']==a['policy_result']==p.expected_specs()[key]['result']
    assert a['exception_policy_screenable']


@pytest.mark.parametrize('mutation',['missing','duplicate','action','score','date','home','source_hash','commit','id','approval','claim_hash','evidence_url','evidence_digest','evidence_omitted','evidence_duplicate','unresolved_registry','conditional_registry','mapping','reserve_merge'])
def test_missing_conflicting_or_rebound_decisions_fail_closed(mutation):
    pol=policy();c=next(c for c in pol['cases'] if p.source_key(c['original'])==(2024,745));r=deepcopy(c['original'])
    if mutation=='missing':pol['cases'].pop()
    if mutation=='duplicate':pol['cases'].append(deepcopy(c))
    if mutation=='action':c['action']='RETAIN'
    if mutation=='score':c['result']='3-0'
    if mutation=='date':c['effective_result_date']='2025-05-30'
    if mutation=='home':c['original']['home']='Other club'
    if mutation=='source_hash':c['original']['source_sha256']='0'*64
    if mutation=='commit':c['original']['source_commit']='0'*40
    if mutation=='id':c['fixture_id']='wrong'
    if mutation=='approval':c['approval']='ASSUMED'
    if mutation=='claim_hash':c['phase5_claim_sha256']='0'*64
    if mutation=='evidence_url':c['evidence'][0]['url']='https://example.org/mirror'
    if mutation=='evidence_digest':c['evidence'][0]['source_entry_sha256']='0'*64
    if mutation=='evidence_omitted':c['evidence']=[]
    if mutation=='evidence_duplicate':c['evidence']*=2
    if mutation=='unresolved_registry':pol['unresolved_hold_ids']=[]
    if mutation=='conditional_registry':pol['conditional_hold_ids']=[]
    if mutation=='mapping':pol['global_team_mappings']={'FC Barcelona B':'FC Barcelona'}
    if mutation=='reserve_merge':pol['uncertainty']['identity_groups'][0]['keep_separate_from_parent']=False
    with pytest.raises(ValueError):p.assess(r,pol)


@pytest.mark.parametrize('key',[(2018,376),(2019,722)])
def test_holds_cannot_acquire_effective_dates(key):
    pol=policy();c=next(c for c in pol['cases'] if p.source_key(c['original'])==key)
    c['effective_result_date']=c['original']['date']
    with pytest.raises(ValueError):p.assess(c['original'],pol)


@pytest.mark.parametrize('state',['PARTIAL','UNVERIFIED','VERIFIED'])
def test_round_flags_and_partial_history_are_not_exclusions(state):
    r=ordinary();r.update(round=1,diagnostic_outlier=True,source_order=0,round_context='PARTIAL')
    before=deepcopy(r);a=p.assess(r,policy(),historical_status=state)
    assert a['exception_policy_screenable'] and a['effective_result_date']==r['date']
    assert a['availability_basis']=='SOURCE_PLAYING_DATE_PROXY_NOT_CERTIFIED' and r==before


def test_new_unresolved_or_incomplete_result_fails_closed():
    r=ordinary();a=p.assess(r,policy(),identified_final_outcome='UNRESOLVED')
    assert not a['exception_policy_screenable'] and a['effective_result_date'] is None
    r.update(FT=None,hg=None,ag=None);a=p.assess(r,policy())
    assert a['screening_status']=='MISSING_RESULT_HOLD_OUT' and a['effective_result_date'] is None


def test_stored_unresolved_outcome_cannot_be_waived_by_caller_default():
    r=ordinary();r['identified_final_outcome_status']='UNRESOLVED'
    a=p.assess(r,policy(),identified_final_outcome='NO_CONFLICT_IDENTIFIED')
    assert not a['exception_policy_screenable'] and a['effective_result_date'] is None


def test_new_unreviewed_award_fails_closed():
    r=ordinary();r['source_marked_awarded']=True
    a=p.assess(r,policy());assert not a['exception_policy_screenable']


@pytest.mark.parametrize('mutation',['partial_goals','FT_conflict','invalid_score','invalid_date','same_teams'])
def test_invalid_ordinary_record_does_not_pass(mutation):
    r=ordinary()
    if mutation=='partial_goals':r.update(FT=None,hg='2',ag=None)
    if mutation=='FT_conflict':r['hg']='3'
    if mutation=='invalid_score':r['FT']='2-?'
    if mutation=='invalid_date':r['date']='2014-2-31'
    if mutation=='same_teams':r['away']=r['home']
    with pytest.raises(ValueError):p.assess(r,policy())


@pytest.mark.parametrize('label',sorted(p.review.structural.RESERVES))
def test_reserve_labels_preserved_and_parent_mappings_rejected(label):
    assert p.identity_labels(label,'Parent club')==(label,'Parent club')
    with pytest.raises(ValueError):p.identity_labels(label,'Parent club',{label:'Parent club'})


def test_missing_required_exception_cannot_be_bypassed_through_batch_primitive():
    with pytest.raises(ValueError):p.assess_record(case((2024,745))['original'],{})


def test_classification_and_clearance_are_independent():
    a=p.assess(ordinary(),policy());a.update(model_training_suitability='CLEARED',licensing_clearance='CLEARED')
    assert not p.training_allowed(a,'2030-01-01') # ordinary proxy is not demonstrated availability
    assert not p.assess(ordinary(),policy(),technical_status='STRUCTURAL_FAIL')['exception_policy_screenable']
    with pytest.raises(ValueError):p.assess(ordinary(),policy(),identified_final_outcome='ASSUMED')


@pytest.mark.parametrize('available,prediction,expected',[(None,'2020-06-11',False),('2020-06-10','2020-06-10',False),('2020-06-10','2020-06-09',False),('2020-06-10','2020-06-11',True)])
def test_strict_calendar_day_availability(available,prediction,expected):
    assert p.known_strictly_before(available,prediction) is expected


def test_registry_determinism_and_nonmutation():
    pol=policy();before=deepcopy(pol)
    first=p.base.encode({k:p.assess_record(v['original'],p.validate_registry(pol)) for k,v in sorted(p.validate_registry(pol).items())})
    second=p.base.encode({k:p.assess_record(v['original'],p.validate_registry(pol)) for k,v in sorted(p.validate_registry(pol).items())})
    assert first==second and pol==before


def test_phase6_protected_sources_and_history(tmp_path,monkeypatch):
    monkeypatch.setattr(p.review,'protect',lambda *a:{})
    files={f'old{i}':p.base.sha(b'original') for i in range(68)}
    for n in files:(tmp_path/n).write_bytes(b'original')
    (tmp_path/'PLANNING_LOG.md').write_bytes(b'history\nappend\n')
    (tmp_path/p.BASELINE).write_bytes(p.base.encode(dict(files=files,planning_log=dict(bytes=8,sha256=p.base.sha(b'history\n')))))
    p.protected(tmp_path,tmp_path)
    (tmp_path/'old0').write_bytes(b'changed')
    with pytest.raises(ValueError,match='Protected'):p.protected(tmp_path,tmp_path)
    (tmp_path/'old0').write_bytes(b'original');(tmp_path/'PLANNING_LOG.md').write_bytes(b'changed')
    with pytest.raises(ValueError,match='Planning'):p.protected(tmp_path,tmp_path)
