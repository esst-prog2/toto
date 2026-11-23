"""Synthetic policy and chronology tests; no private originals or network required."""
from copy import deepcopy
import pytest
from scripts import decide_eredivisie_policy as p


def row(key='ordinary',season='2000/2001',source='jalapic/holland.csv',date='2000-08-01',FT='1-0',home='H',away='A',flags=None):
    goals=FT.split('-') if FT else [None,None]
    return dict(audit_id=key,source=source,source_sha256='a'*64,source_line=2,source_end_line=2,
                physical_record_sha256='b'*64,provenance=dict(url='https://example.test/file',commit='c'*40,git_blob_sha1='d'*40),
                season=season,date=date,home=home,away=away,FT=FT,hg=goals[0],ag=goals[1],annotation='[cancelled]' if FT is None else '',
                stage='REGULAR_SEASON',round=1,structural=dict(structurally_valid=True,errors=[],flags=flags or []))


def case(kind):
    season,kickoff,completion,FT=p.CASES[kind];rs=[];reviews={}
    for i,key in enumerate(p.CASE_IDS[kind]):
        modern=kind=='NAC_HEERENVEEN' or i==1
        date=kickoff if kind=='NAC_HEERENVEEN' or (kind=='GRONINGEN_AJAX' and not modern) else completion
        score=None if kind=='NAC_HEERENVEEN' else '1-2' if kind=='NEC_VITESSE' and modern else FT
        r=row(key,season,'openfootball/europe/season.txt' if modern else 'jalapic/holland.csv',date,score)
        rs.append(r);reviews[key]=dict(original=deepcopy(r),assessment=dict(case_id=kind,status='PARTIALLY CORROBORATED',evidence_ids=['E']))
    c=dict(id=kind,season=season,home_labels=['H'],away_labels=['A'],evidence_score=FT,
           chronology=dict(original_kickoff=kickoff,reported_completion=completion),review=dict(evidence_ids=['E']))
    return rs,reviews,c


def test_historical_baseline_and_literal_labels():
    a=row();b=row('comparator',source='openfootball/season',home='Historical spelling differs')
    d=p.decide([b,a],{});assert d['selected_source_id']==a['audit_id'] and d['approved_values']['home']=='H'
    assert d['selection_reason']=='HISTORICAL_CONTIGUOUS_BASELINE'


def test_latest_modern_primary():
    r=row(season='2025/2026',source='openfootball/season',date='2025-08-01')
    assert p.decide([r],{})['selection_reason']=='MODERN_2025_26_PRIMARY'


@pytest.mark.parametrize('season',['1989/1990','2026/2027'])
def test_outside_scope_fails(season):
    with pytest.raises(ValueError):p.decide([row(season=season)],{})


def test_modern_only_gap_not_silently_selected():
    with pytest.raises(ValueError,match='primary-source gap'):p.decide([row(source='openfootball/season')],{})


def test_duplicate_source_representation_rejected():
    with pytest.raises(ValueError):p.decide([row(),row('other')],{})


def test_one_decision_for_two_source_observations():
    rs=[row(),row('m',source='openfootball/season')];d=p.decide(rs,{})
    assert p.reconcile(rs,[d])['overlapping_representations']==1


def test_duplicate_fixture_decision_rejected():
    r=row();d=p.decide([r],{})
    with pytest.raises(ValueError):p.reconcile([r],[d,d])


def test_lost_observation_rejected():
    r=row();d=p.decide([r],{})
    with pytest.raises(ValueError):p.reconcile([r,row('lost')],[d])


def test_groningen_actual_completion_single_fixture():
    rs,hs,c=case('GRONINGEN_AJAX');before=deepcopy(rs);d=p.decide(rs,hs,c)
    assert d['approved_values']['date']=='2023-05-16' and d['chronology']['actual_kickoff']=='2023-05-14'
    assert rs==before and p.reconcile(rs,[d])['unique_fixture_slots']==1
    assert not p._eligible(d,d,'2023-05-14') and not p._eligible(d,d,'2023-05-16')
    assert p._eligible(d,d,'2023-05-17')


def test_nec_final_score_preserves_contradictory_original():
    rs,hs,c=case('NEC_VITESSE');d=p.decide(rs,hs,c)
    assert d['approved_values']['FT']=='1-3' and rs[1]['FT']=='1-2'
    assert d['policy']=='NEC_VITESSE' and len(d['source_observation_ids'])==2


@pytest.mark.parametrize('kind',['AJAX_FEYENOORD','RKC_AJAX','AZ_NEC','HERACLES_GRONINGEN'])
def test_existing_completion_dates_are_not_fictitiously_corrected(kind):
    rs,hs,c=case(kind);d=p.decide(rs,hs,c)
    assert d['approved_values']['date']==rs[0]['date']==p.CASES[kind][2]
    assert d['approved_values']['FT']==p.CASES[kind][3]
    assert d['chronology']['availability_day_verified'] is True


@pytest.mark.parametrize('kind',['FEYENOORD_VVV','VITESSE_SPARTA'])
def test_material_interruption_completion_gap_is_explicit_hold(kind):
    rs,hs,c=case(kind);d=p.decide(rs,hs,c)
    assert d['disposition']=='HOLD_OUT' and d['approved_values'] is None
    assert not p._eligible(d,d,'2026-11-23')
    assert d['chronology']['effective_result_availability_date'] is None
    assert d['chronology']['completion_date'] is None
    assert d['chronology']['reported_completion_date']==p.CASES[kind][2]


def test_nac_hold_no_source_supplementation():
    rs,hs,c=case('NAC_HEERENVEEN');d=p.decide(rs,hs,c)
    assert d['disposition']=='HOLD_OUT' and d['hold_type']=='SUPPLEMENT_USAGE_PERMISSION_PENDING'
    assert d['documentary_values']['FT']=='2-0' and d['approved_values'] is None
    assert rs[0]['FT'] is None and rs[0]['annotation']=='[cancelled]'
    assert d['supplement_assessment']['failed']==['usage_compatible']


CRITERIA=['identity','direct_result','traceable','access_compatible','usage_compatible','immutable','narrow','chronological','no_new_dataset']
@pytest.mark.parametrize('missing',CRITERIA)
def test_any_failed_supplement_criterion_fails_closed(missing):
    kwargs=dict.fromkeys(CRITERIA,True);kwargs[missing]=False
    assert not p.supplement_assessment(p.CASE_IDS['NAC_HEERENVEEN'][0],**kwargs)['approved']


def test_supplement_does_not_generalize_to_another_fixture():
    assert not p.supplement_assessment('another',**dict.fromkeys(CRITERIA,True))['approved']
    assert p.supplement_assessment(p.CASE_IDS['NAC_HEERENVEEN'][0],**dict.fromkeys(CRITERIA,True))['approved']


def test_74_explicit_unplayed_slots_not_74_scored_results():
    rs=[row(str(i),'2019/2020','openfootball/season','2020-04-01',None,home='H'+str(i)) for i in range(74)]
    ds=[p.decide([r],{}) for r in rs];counts=p.reconcile(rs,ds)
    assert counts['dispositions']=={'NOT_PLAYED':74}
    assert all(d['approved_values'] is None for d in ds)


def test_unknown_null_is_not_assumed_not_played():
    r=row(season='2025/2026',source='openfootball/season',date='2025-08-01',FT=None)
    assert p.decide([r],{})['disposition']=='HOLD_OUT'


@pytest.mark.parametrize('flag',['WIDE_ROUND','SOURCE_ORDER_REVERSAL','UNUSUAL_SCORE'])
def test_context_flags_alone_do_not_exclude(flag):
    r=row(flags=[flag]);assert p.decide([r],{})['disposition']=='COMPLETED_RESULT_CANDIDATE'


def test_unverified_sample_does_not_exclude():
    r=row();hs={r['audit_id']:dict(original=deepcopy(r),assessment=dict(status='UNRESOLVED'))}
    assert p.decide([r],hs)['disposition']=='COMPLETED_RESULT_CANDIDATE'


def test_unknown_flag_cannot_silently_pass():
    with pytest.raises(ValueError):p.decide([row(flags=['ADMINISTRATIVE_AWARD'])],{})


@pytest.mark.parametrize('field,value',[('FT','2-0'),('date','2000-08-02'),('home','Jong H')])
def test_changed_original_breaks_historical_binding(field,value):
    r=row();hs={r['audit_id']:dict(original=deepcopy(r),assessment={})};r[field]=value
    with pytest.raises(ValueError,match='binding mismatch'):p.decide([r],hs)


def test_unresolved_conflicting_score_is_held():
    assert p.decide([row(),row('m',source='openfootball/season',FT='2-0')],{})['disposition']=='HOLD_OUT'


def test_unresolved_conflicting_date_is_held():
    assert p.decide([row(),row('m',source='openfootball/season',date='2000-08-02')],{})['disposition']=='HOLD_OUT'


def test_unresolved_historical_contradiction_is_held():
    r=row();hs={r['audit_id']:dict(original=deepcopy(r),assessment=dict(status='CONTRADICTED'))}
    assert p.decide([r],hs)['disposition']=='HOLD_OUT'


def test_missing_exception_context_rejected():
    rs,hs,c=case('NEC_VITESSE')
    with pytest.raises(ValueError):p.decide(rs,hs)


def test_incomplete_exception_group_rejected():
    rs,hs,c=case('NEC_VITESSE')
    with pytest.raises(ValueError):p.decide(rs[:1],hs,c)


def test_exception_cannot_change_approved_result():
    rs,hs,c=case('GRONINGEN_AJAX');rs[0].update(FT='2-4',ag='4');hs[rs[0]['audit_id']]['original']=deepcopy(rs[0])
    with pytest.raises(ValueError,match='approved exception result'):p.decide(rs,hs,c)


def test_identity_includes_season_and_preserves_reserves():
    senior=p.decide([row()],{})['fixture_id'];reserve=p.decide([row(home='Jong H')],{})['fixture_id']
    renamed=p.decide([row(home='H successor')],{})['fixture_id']
    assert len({senior,reserve,renamed})==3


def test_ordinary_proxy_does_not_authorize_chronological_use():
    d=p.decide([row()],{});assert not p._eligible(d,d,'2026-11-23')


@pytest.mark.parametrize('cutoff',['2023-09-24','2023-09-27'])
def test_interrupted_result_rejected_before_or_same_day(cutoff):
    rs,hs,c=case('AJAX_FEYENOORD');d=p.decide(rs,hs,c);assert not p._eligible(d,d,cutoff)


def test_unknown_availability_rejected():
    rs,hs,c=case('AJAX_FEYENOORD');d=p.decide(rs,hs,c);d['chronology']['effective_result_availability_date']=None
    assert not p._eligible(d,d,'2023-09-28')


def test_unresolved_administration_rejected():
    rs,hs,c=case('AJAX_FEYENOORD');d=p.decide(rs,hs,c);d['unresolved_administration']=True
    assert not p._eligible(d,d,'2023-09-28')


def test_future_availability_rejected():
    rs,hs,c=case('AJAX_FEYENOORD');d=p.decide(rs,hs,c);d['chronology']['effective_result_availability_date']='2023-09-29'
    assert not p._eligible(d,d,'2023-09-28')


@pytest.mark.parametrize('field',['source_observation_ids','decision_id','approved_values','chronology','disposition','historical_reviews'])
def test_altered_registry_entry_rejected(field):
    d=p.decide([row()],{});changed=deepcopy(d);del changed[field]
    with pytest.raises(ValueError,match='Altered/incomplete'):p._eligible(d,changed,'2026-11-23')


@pytest.mark.parametrize('value',['2023-9-27','2023-02-29',None,'2023-09-27T10:00:00'])
def test_noncanonical_or_invalid_day(value):
    with pytest.raises(ValueError):p.day(value)


def synthetic_outputs():
    d=p.decide([row()],{})
    outputs={name:dict(phase=6) for name in p.NAMES};outputs[p.NAMES[1]]=dict(records=[d])
    return outputs,d


def test_prediction_gate_loads_only_exact_regenerated_artifacts(tmp_path,monkeypatch):
    outputs,d=synthetic_outputs()
    for name,obj in outputs.items():(tmp_path/name).write_bytes(p.base.encode(obj))
    monkeypatch.setattr(p,'build',lambda directory,root:deepcopy(outputs))
    gate=p.PredictionGate(tmp_path,tmp_path)
    assert not gate.eligible_for_prediction(d,'2026-11-23')
    assert not gate.training_allowed(d,'2026-11-23')


@pytest.mark.parametrize('which',p.NAMES)
def test_any_altered_policy_artifact_fails_gate_load(tmp_path,monkeypatch,which):
    outputs,d=synthetic_outputs()
    for name,obj in outputs.items():(tmp_path/name).write_bytes(p.base.encode(obj))
    (tmp_path/which).write_bytes(b'{}\n')
    monkeypatch.setattr(p,'build',lambda directory,root:deepcopy(outputs))
    with pytest.raises(ValueError,match='Altered/missing'):p.PredictionGate(tmp_path,tmp_path)


def test_gate_does_not_trust_supplied_training_clearance(tmp_path,monkeypatch):
    outputs,d=synthetic_outputs()
    for name,obj in outputs.items():(tmp_path/name).write_bytes(p.base.encode(obj))
    monkeypatch.setattr(p,'build',lambda directory,root:deepcopy(outputs));gate=p.PredictionGate(tmp_path,tmp_path)
    changed=deepcopy(d);changed['model_training_permission']='CLEARED'
    with pytest.raises(ValueError):gate.training_allowed(changed,'2026-11-23')


@pytest.mark.parametrize('kind',list(p.CASES))
def test_known_exception_original_dates_cannot_drift_even_with_matching_review_copy(kind):
    rs,hs,c=case(kind);rs[0]['date']=p.CASES[kind][0][:4]+'-08-01'
    hs[rs[0]['audit_id']]['original']=deepcopy(rs[0])
    with pytest.raises(ValueError,match='approved exception result/date'):p.decide(rs,hs,c)
