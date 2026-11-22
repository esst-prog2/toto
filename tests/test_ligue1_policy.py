"""Synthetic Phase 6 decisions, source bindings, uncertainty and temporal gates."""
from copy import deepcopy

import pytest

from scripts import decide_ligue1_policy as p


def row(n, *, home='Alpha', away='Beta', date='2020-01-01', season='2019/2020',
        hg='2', ag='1', flags=(), annotation='', source=None, label='H'):
    source=source or p.review.structural.metadata.HIST
    r=dict(source=source,source_sha256='a'*64,source_line=n+1,raw_line_sha256='b'*64,
           date=date,season=season,home=home,away=away,hg=hg,ag=ag,
           FT=f'{hg}-{ag}' if hg is not None and ag is not None else None,
           annotation=annotation,assessment=dict(flags=list(flags),source_result=label,malformed_reasons=[]))
    r['audit_id']=p.review.structural.source_id(source,r['source_sha256'],r['source_line'])
    return r


def context():
    records=[];major=[];evidence=[]
    specs=[('SC Bastia','Olympique Lyonnais','2017-04-16','2016/2017','0','0'),
           ('FC Nantes','SC Bastia','2013-08-10','2013/2014','0','0'),
           ('Montpellier HSC','AS Saint-Étienne','2025-03-16','2024/2025','0','2'),
           ('FC Nantes','Toulouse FC','2026-05-17','2025/2026','0','0'),
           ('OGC Nice','Olympique Marseille','2021-10-27','2021/2022','1','1'),
           ('Montpellier HSC','Clermont Foot 63','2023-11-29','2023/2024','1','1')]
    for i,(h,a,d,s,hg,ag) in enumerate(specs):
        name,action,effective,pub=p.SPECS[i]
        r=row(i,home=h,away=a,date=d,season=s,hg=hg,ag=ag,
              flags=['REPLAY_DATE_CONTEXT'] if effective else ['SOURCE_MARKED_ADMINISTRATIVE'])
        records.append(r);eid='E'+str(i)
        evidence.append(dict(id=eid,url='https://example.org/'+name,access='DIRECT',
                             independence='OFFICIAL_RECORD',facts=dict(date=d,FT=r['FT'])))
        major.append(dict(case=name,audit_id=r['audit_id'],binding=p.review.binding(r),evidence_ids=[eid],
                          chronology=dict(kickoff=None if effective else d,
                                          original_event='2021-08-22' if i==4 else '2023-10-08' if i==5 else None,
                                          replay=effective,played_score=r['FT'])))
    aux=row(6,home='AJ Auxerre',away='Olympique Lyon',date='1996-10-26',season='1996/1997',hg='7',ag='0')
    records.append(aux);evidence.append(dict(id='AUX',url='https://example.org/interview'))
    brest=[row(10+i,home='Stade Brest' if i%2 else 'Brest Armorique FC',away='Other'+str(i),
               date='1990-08-01',season='1990/1991',flags=['BREST_DUAL_LABEL_IDENTITY']) for i in range(38)]
    records.extend(brest)
    records.extend([row(100),row(101,hg='1',ag='1',label='D'),
                    row(102,hg='0',ag='2',label='D',flags=['SYSTEMATIC_SOURCE_LABEL_DEFECT']),
                    row(103,home='AC Ajaccio'),row(104,home='Gazélec FC Ajaccio'),
                    row(105,flags=['WIDE_ROUND_SPAN','UNUSUAL_SCORE'])])
    records.extend([row(200+i,hg=None,ag=None,annotation='[cancelled]',flags=['CANCELLED_UNPLAYED_SLOT']) for i in range(2)])
    for id in ['COVID','BREST-BNF','L00','S01','S09']:
        evidence.append(dict(id=id,url='https://example.org/'+id))
    ledger=dict(major_cases=major,evidence=evidence,
                identity_cases=[dict(case='BREST_1990',affected_ids=[r['audit_id'] for r in brest]),dict(case='AJACCIO_2015',affected_ids=[])],
                rounds=[],broader_date_candidates=dict(count=1162),missing_fixture=dict(source_observation_exists=False))
    review_result=dict(contradictions=[dict(audit_id=aux['audit_id'],field='date',source='1996-10-26',evidence='1996-10-25',evidence_id='AUX')],
                       fixtures=[dict(audit_id=r['audit_id'],status='VERIFIED') for r in records[:6]])
    return dict(records=records),ledger,review_result


def run(ctx,policy=None,**kwargs):
    report,ledger,review=ctx
    policy=policy or p.make_policy(report,ledger,review)
    return p.evaluate(policy,report,ledger,review,**kwargs)


def test_reconciliation_cancelled_admin_date_holdouts_and_no_source_mutation():
    ctx=context();before=deepcopy(ctx);results=run(ctx)
    assert len(results)==len(ctx[0]['records'])
    assert sum(x['status']=='HOLD_OUT' for x in results)==5
    assert sum(x['status']=='NOT_PLAYED' for x in results)==2
    assert ctx==before


@pytest.mark.parametrize('hg,ag,label,expected',[('2','1','H','H'),('1','1','D','D'),('0','2','D','A'),('0','2','A','A'),('0','0','D','D')])
def test_outcomes_come_from_numeric_goals_not_global_D_replacement(hg,ag,label,expected):
    r=row(0,hg=hg,ag=ag,label=label);before=deepcopy(r)
    assert p.numeric_outcome(r)==expected and r==before


@pytest.mark.parametrize('hg,ag',[(None,'0'),('0',None),('-1','0'),('x','0'),('1.0','0'),(True,'0'),('01','0'),('','0')])
def test_inconsistent_or_missing_goals_fail_closed(hg,ag):
    with pytest.raises(ValueError,match='goals'):p.numeric_outcome(row(0,hg=hg,ag=ag))


def test_FT_conflict_does_not_pass_numeric_interpretation():
    r=row(0);r['FT']='0-0'
    with pytest.raises(ValueError,match='inconsistent'):p.numeric_outcome(r)


def test_awarded_tied_score_is_not_an_ordinary_draw():
    results=run(context());held=[r for r in results if r['decision']=='HOLD_OUT_ADMIN_SCORE']
    assert len(held)==2 and all(r['candidate_outcome'] is None for r in held)


def test_ratification_dates_preserved_but_unresolved_finality_still_holds_out():
    ctx=context();policy=p.make_policy(*ctx)
    cases={e['decision_id']:e for e in policy['decisions']}
    assert cases['MONTPELLIER_ASSE']['earliest_documented_admin_bound']=='2025-04-02'
    assert cases['NANTES_TOULOUSE_2026']['earliest_documented_admin_bound']=='2026-05-27'
    assert cases['MONTPELLIER_ASSE']['administrative_score']=='0-2'
    assert cases['NANTES_TOULOUSE_2026']['administrative_score']=='0-0'
    assert all(cases[n]['effective_result_date'] is None for n in ('MONTPELLIER_ASSE','NANTES_TOULOUSE_2026'))


def test_replays_use_verified_replay_dates_and_preserve_original_events():
    ctx=context();policy=p.make_policy(*ctx);cases={e['decision_id']:e for e in policy['decisions']}
    for name,original,completion in [('NICE_OM','2021-08-22','2021-10-27'),('MHSC_CLERMONT','2023-10-08','2023-11-29')]:
        c=cases[name]
        assert c['chronology']['original_event_date']==original and c['effective_result_date']==completion
        a=next(r for r in run(ctx,policy) if r['audit_id']==c['audit_id'])
        assert a['availability_verified'] and a['effective_result_date']==completion


def test_Auxerre_one_interview_does_not_correct_source_date():
    ctx=context();policy=p.make_policy(*ctx);c=next(e for e in policy['decisions'] if e['decision_id']=='AUXERRE_LYON')
    assert c['original']['date']=='1996-10-26' and c['effective_result_date'] is None
    assert c['chronology']['disputed_playing_dates']==['1996-10-25','1996-10-26']


def test_cancelled_slots_never_become_draws_or_unknown_admin_outcomes():
    a=[r for r in run(context()) if r['status']=='NOT_PLAYED']
    assert all(r['candidate_outcome'] is None and r['effective_result_date'] is None for r in a)
    assert all(r['historical_confidence']=='VERIFIED_NOT_PLAYED' for r in a)


def test_Brest_rule_is_source_season_and_fixture_bound_and_preserves_labels():
    ctx=context();before=deepcopy(ctx);out=run(ctx)
    changed=[r for r in out if r['candidate_identity']['home']=='Brest Armorique FC']
    assert len(changed)==38 and ctx==before
    extra=row(999,home='Stade Brest',season='2010/2011',date='2010-08-01');ctx[0]['records'].append(extra)
    a=next(x for x in run(ctx) if x['audit_id']==extra['audit_id'])
    assert a['candidate_identity']['home']=='Stade Brest'


def test_distinct_Ajaccio_clubs_never_merged():
    output=run(context())
    names={r['candidate_identity']['home'] for r in output}
    assert 'AC Ajaccio' in names and 'Gazélec FC Ajaccio' in names


def test_unverified_ordinary_and_long_round_flags_are_candidates_not_automatic_holdouts():
    ctx=context();r=ctx[0]['records'][-3];assert 'WIDE_ROUND_SPAN' in r['assessment']['flags']
    a=next(x for x in run(ctx) if x['audit_id']==r['audit_id'])
    assert a['status']=='CANDIDATE_NOT_STANDARDIZED' and not a['availability_verified']
    assert a['historical_confidence']=='SOURCE_REPORTED_UNVERIFIED'


def test_new_positive_material_conflict_holds_out_even_ordinary_record():
    ctx=context();identifier=ctx[0]['records'][-3]['audit_id']
    a=next(r for r in run(ctx,conflicts=[identifier]) if r['audit_id']==identifier)
    assert a['status']=='HOLD_OUT' and a['candidate_outcome'] is None and a['effective_result_date'] is None


@pytest.mark.parametrize('mutation',[ 'missing_case','duplicate_case','binding','action','source_score',
                                      'effective_date','evidence','identity','unknown_added_decision','label_rule'])
def test_policy_mutations_cannot_silently_pass(mutation):
    ctx=context();policy=p.make_policy(*ctx)
    if mutation=='missing_case':policy['decisions'].pop()
    if mutation=='duplicate_case':policy['decisions'].append(deepcopy(policy['decisions'][0]))
    if mutation=='binding':policy['decisions'][0]['original']['source_line']+=1
    if mutation=='action':policy['decisions'][0]['action']='ORDINARY_NUMERIC_RESULT'
    if mutation=='source_score':policy['decisions'][0]['original']['FT']='0-3'
    if mutation=='effective_date':policy['decisions'][0]['effective_result_date']='2020-01-01'
    if mutation=='evidence':policy['decisions'][0]['evidence_ids']=[]
    if mutation=='identity':policy['identity_rules'][0]['season']='ANY'
    if mutation=='unknown_added_decision':policy['decisions'].append(dict(audit_id='unknown'))
    if mutation=='label_rule':policy['outcome_rule']['global_D_replacement']=True
    with pytest.raises(ValueError,match='policy'):run(ctx,policy)


def test_missing_major_review_evidence_fails_closed():
    ctx=context();ctx[1]['major_cases'].pop()
    with pytest.raises(ValueError,match='major-case'):p.make_policy(*ctx)


def test_replay_index_only_cannot_approve_completion():
    ctx=context();ctx[1]['evidence'][4]['access']='INDEX_ONLY'
    with pytest.raises(ValueError,match='Replay lacks'):p.make_policy(*ctx)


def test_new_discrepancy_requires_new_explicit_review():
    ctx=context();ctx[2]['contradictions'].append(deepcopy(ctx[2]['contradictions'][0]))
    with pytest.raises(ValueError,match='discrepancy'):p.make_policy(*ctx)


def test_unknown_material_flag_and_missing_material_decision_fail_closed():
    ctx=context();ctx[0]['records'][-3]['assessment']['flags'].append('NEW_UNRESOLVED_IDENTITY')
    with pytest.raises(ValueError,match='New review flag'):p.make_policy(*ctx)
    ctx=context();ctx[0]['records'][-3]['assessment']['flags'].append('ADMINISTRATIVE_SCORE_CONFLICT')
    with pytest.raises(ValueError,match='lacks required'):p.make_policy(*ctx)


def test_changed_original_population_cannot_reuse_saved_registry():
    ctx=context();policy=p.make_policy(*ctx);ctx[0]['records'][-3]['FT']='8-0'
    with pytest.raises(ValueError,match='policy'):run(ctx,policy)


def test_missing_cancellation_flag_cannot_turn_blank_score_into_candidate():
    ctx=context();ctx[0]['records'][-1]['assessment']['flags']=[]
    with pytest.raises(ValueError,match='goals'):run(ctx)


def test_missing_grouped_evidence_rejected():
    ctx=context();ctx[1]['evidence']=[e for e in ctx[1]['evidence'] if e['id']!='L00']
    with pytest.raises(ValueError,match='grouped'):p.make_policy(*ctx)


def test_same_day_and_unknown_availability_are_rejected():
    assert not p.known_strictly_before('2021-10-27','2021-10-27')
    assert not p.known_strictly_before('2021-10-27','2021-10-26')
    assert p.known_strictly_before('2021-10-27','2021-10-28')
    assert not p.known_strictly_before(None,'2021-10-28')


@pytest.mark.parametrize('bad',['20211027','2021-1-1','2021-02-29','2021-10-27T20:00:00',None,True])
def test_invalid_prediction_dates_rejected(bad):
    with pytest.raises((ValueError,TypeError)):p.known_strictly_before(None,bad)


def test_training_separates_rights_eligibility_confidence_and_time():
    ctx=context();a=next(r for r in run(ctx) if r['decision']=='APPROVED_REPLAY')
    assert not p.training_allowed(a,'2024-01-01')
    a.update(licensing_clearance='CLEARED',model_training_suitability='CLEARED')
    assert p.training_allowed(a,'2024-01-01')
    assert not p.training_allowed(a,a['effective_result_date'])
    for key,value in [('availability_verified',False),('material_conflict',True),('status','HOLD_OUT'),('licensing_clearance','UNRESOLVED')]:
        b=deepcopy(a);b[key]=value;assert not p.training_allowed(b,'2024-01-01')


def test_historical_source_date_is_not_demonstrably_available_by_itself():
    ctx=context();a=next(r for r in run(ctx) if r['decision']=='ORDINARY_NUMERIC_RESULT')
    a.update(licensing_clearance='CLEARED',model_training_suitability='CLEARED')
    assert not p.training_allowed(a,'2030-01-01')


def test_unknown_conflict_ID_and_duplicate_source_records_fail_closed():
    with pytest.raises(ValueError,match='Unknown'):run(context(),conflicts=['unknown'])
    ctx=context();ctx[0]['records'].append(deepcopy(ctx[0]['records'][0]))
    with pytest.raises(ValueError,match='Duplicate'):run(ctx)


def test_policy_generation_byte_deterministic():
    ctx=context()
    assert p.base.encode(p.make_policy(*ctx))==p.base.encode(p.make_policy(*ctx))


def test_completed_Nantes_Bastia_not_misclassified_as_interrupted():
    policy=p.make_policy(*context());c=next(e for e in policy['decisions'] if e['decision_id']=='NANTES_BASTIA')
    assert c['chronology']['interruption_date'] is None
    assert c['chronology']['original_kickoff_date']=='2013-08-10'


def test_coverage_gap_remains_open_without_supplement_or_acquisition():
    policy=p.make_policy(*context())
    assert policy['coverage']['missing_season']=='1994/1995'
    assert policy['coverage']['missing_season_expected']==380
    assert policy['coverage']['missing_pairing']['source_observation_exists'] is False
    assert policy['coverage']['gap_recovery']['acquisition_performed'] is False


@pytest.mark.parametrize('flag,message',[('BREST_DUAL_LABEL_IDENTITY','Brest identity risk'),('DISTINCT_AJACCIO_CLUB_IDENTITY','Ajaccio identity risk')])
def test_identity_risk_cannot_be_reused_outside_exact_evidence_scope(flag,message):
    ctx=context();ctx[0]['records'][-3]['assessment']['flags'].append(flag)
    with pytest.raises(ValueError,match=message):p.make_policy(*ctx)


def test_Ajaccio_reviewed_scope_still_cannot_map_AC_to_Gazelec():
    ctx=context();r=row(999,home='AC Ajaccio',season='2015/2016',date='2015-08-01',flags=['DISTINCT_AJACCIO_CLUB_IDENTITY'],source='openfootball/europe/france/2015-16_fr1.txt')
    ctx[0]['records'].append(r);ctx[1]['identity_cases'][1]['affected_ids']=[r['audit_id']]
    with pytest.raises(ValueError,match='exact modern entrant'):p.make_policy(*ctx)
