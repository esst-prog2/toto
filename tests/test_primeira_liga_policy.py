"""Synthetic source selection, exception, chronology and registry integrity checks."""
from copy import deepcopy
from pathlib import Path
import pytest
from scripts import decide_primeira_liga_policy as p


def row(ident='ordinary',year=2000,modern=False,date=None,FT='1-0',home='Home',away='Away'):
    return dict(audit_id=ident,season=f'{year}/{year+1}',source=f'openfootball/europe/portugal/{year}-{(year+1)%100:02}_pt1.txt'if modern else p.HIST_PATH,source_sha256='a'*64,source_line=2,source_end_line=2,physical_record_sha256='b'*64,original_literal='retained bytes',provenance=dict(url='https://example.test/source',commit=p.MODERN_PIN if modern else p.HIST_PIN,git_blob_sha1='c'*40),date=date or f'{year}-08-20',home=home,away=away,FT=FT,hg=FT.split('-')[0],ag=FT.split('-')[1],stage='REGULAR_SEASON'if modern else'HISTORICAL_P1_TIER1_STAGE_NOT_EXPLICIT',annotation='',round=1)


def case(kind):
    spec=p.SPECS[kind];rs=[];reviews={};flags={}
    for index,(ident,line,day,home,away)in enumerate(spec['rows']):
        r=row(ident,int(spec['season'][:4]),index==1,day,spec['score'],home,away);r['source_line']=r['source_end_line']=line;rs.append(r)
        reviews[ident]=dict(original=deepcopy(r),assessment=dict(classification='PARTIALLY CORROBORATED',contradicted={},evidence_ids=[spec['evidence']]))
    ref={spec['evidence']:dict(inspection='ACCESS_RESTRICTED'if kind=='BELENENSES_BENFICA'else'DIRECT_DOCUMENT')}
    return rs,reviews,flags,ref


def test_historical_primary_does_not_rewrite_comparator():
    rs=[row(),row('m',modern=True,home='Other literal spelling')];before=deepcopy(rs);d=p.decide(rs,{}, {},{})
    assert d['selected_source_id']=='ordinary' and d['comparator_source_ids']==['m']
    assert d['approved_values']['home']=='Home' and rs==before


@pytest.mark.parametrize('year',range(2018,2025))
def test_each_overlap_season_one_fixture_two_observations(year):
    rs=[row(year=year),row('m',year,True)];d=p.decide(rs,{}, {},{})
    assert p.reconcile(rs,[d])['overlap_representations']==1
    assert d['selection_reason']=='HISTORICAL_CONTIGUOUS_BASELINE'


def test_modern_only2025_primary():
    d=p.decide([row(year=2025,modern=True)],{}, {},{})
    assert d['selection_reason']=='MODERN_2025_26_PRIMARY'


@pytest.mark.parametrize('year',[1990,1991,1992,1993,2026])
def test_unsourced_early_and_ongoing_seasons_not_fabricated(year):
    with pytest.raises(ValueError,match='Outside approved'):p.decide([row(year=year)],{}, {},{})


def test_modern_only_older_gap_rejected():
    with pytest.raises(ValueError,match='primary-source gap'):p.decide([row(year=2019,modern=True)],{}, {},{})


def test_revision_tamper_rejected():
    r=row();r['provenance']['commit']='wrong'
    with pytest.raises(ValueError,match='revision'):p.decide([r],{}, {},{})


def test_duplicate_historical_source_rejected():
    with pytest.raises(ValueError,match='Ambiguous'):p.decide([row(),row('another')],{}, {},{})


@pytest.mark.parametrize('kind',['SANTA_PACOS','SANTA_BENFICA','NACIONAL_BENFICA'])
def test_bound_completion_decisions_keep_all_originals(kind):
    rs,hr,flags,refs=case(kind);before=deepcopy(rs);d=p.decide(rs,hr,flags,refs)
    assert d['disposition']=='COMPLETED_RESULT_CANDIDATE'
    assert d['approved_values']['date']==p.SPECS[kind]['completion']
    assert d['chronology']['completion_date']==p.SPECS[kind]['completion']
    assert rs==before and d['approved_values']['FT']==p.SPECS[kind]['score']


def test_santa_pacos_schedule_not_promoted_from_source_proxy():
    d=p.decide(*case('SANTA_PACOS'))
    assert d['chronology']['scheduled_date'] is None
    assert d['source_bindings'][p.SPECS['SANTA_PACOS']['rows'][0][0]]['date']=='2020-02-01'
    assert d['event_context']['scheduled_date_verified']is False
    assert d['unresolved_administration']is True
    assert not p._eligible(d,d,'2020-02-03')


def test_santa_benfica_original_kickoff_and_completion_distinct():
    d=p.decide(*case('SANTA_BENFICA'))
    assert d['chronology']['actual_kickoff_date']=='2021-01-03'
    assert not p._eligible(d,d,'2021-01-03')
    assert not p._eligible(d,d,'2021-01-04')
    assert p._eligible(d,d,'2021-01-05')


def test_nacional_already_records_completion_no_fictitious_source_correction():
    rs,hr,flags,refs=case('NACIONAL_BENFICA');d=p.decide(rs,hr,flags,refs)
    assert all(r['date']=='2024-12-19'for r in rs)
    assert d['chronology']['actual_kickoff_date']=='2024-10-06'
    assert d['approved_values']['date']==rs[0]['date']
    assert not p._eligible(d,d,'2024-10-07')and not p._eligible(d,d,'2024-12-19')
    assert p._eligible(d,d,'2024-12-20')


def test_belenenses_played_holdout_not_notplayed():
    d=p.decide(*case('BELENENSES_BENFICA'))
    assert d['disposition']=='HOLD_OUT'and d['approved_values']is None
    assert d['unresolved_administration']is True
    assert all(r['FT']=='0-7'for r in d['source_bindings'].values())
    assert not p._eligible(d,d,'2026-11-24')


def test_benfica_salgueiros_no_source_preference_resolves_date():
    d=p.decide(*case('BENFICA_SALGUEIROS'))
    assert d['disposition']=='HOLD_OUT'and d['approved_values']is None
    assert d['event_context']['alternative_reported_date']=='1995-09-06'
    assert d['chronology']['completion_date']is None


def test_feirense_only_exact_record_interpretation():
    rs,hr,flags,refs=case('FEIRENSE_NACIONAL');d=p.decide(rs,hr,flags,refs)
    assert d['approved_values']['home']=='Feirense'
    assert rs[0]['home']=='Feirense '
    other=row(home='Feirense ')
    with pytest.raises(ValueError,match='Unapproved whitespace'):p.decide([other],{}, {},{})


def test_leiria_eight_players_does_not_become_award():
    d=p.decide(*case('LEIRIA_FEIRENSE'))
    assert d['disposition']=='COMPLETED_RESULT_CANDIDATE'and d['approved_values']['FT']=='0-4'
    assert 'Eight Leiria starters'in d['event_context']['participation_context']
    assert d['chronology']['effective_result_availability_date']is None


@pytest.mark.parametrize('kind',list(p.SPECS))
def test_exception_physical_line_tamper_rejected(kind):
    rs,hr,flags,refs=case(kind);rs[0]['source_line']+=1;hr[rs[0]['audit_id']]['original']=deepcopy(rs[0])
    with pytest.raises(ValueError,match='Exception source binding'):p.decide(rs,hr,flags,refs)


@pytest.mark.parametrize('kind',['SANTA_BENFICA','NACIONAL_BENFICA','FEIRENSE_NACIONAL'])
def test_indexed_evidence_cannot_authorize_exception(kind):
    rs,hr,flags,refs=case(kind);refs[p.SPECS[kind]['evidence']]['inspection']='INDEX_ONLY'
    with pytest.raises(ValueError,match='inspected documentary'):p.decide(rs,hr,flags,refs)


def test_partial_exception_group_fails():
    rs,hr,flags,refs=case('SANTA_BENFICA')
    with pytest.raises(ValueError,match='Incomplete exception'):p.decide(rs[:1],hr,flags,refs)


def test_ordinary_unverified_sample_and_wide_round_remain_candidates():
    r=row();hr={'ordinary':dict(original=deepcopy(r),assessment=dict(classification='UNRESOLVED',contradicted={},evidence_ids=[]))}
    d=p.decide([r],hr,{'ordinary':['WIDE_ROUND','SOURCE_ORDER_REVERSAL','UNUSUAL_SCORE']},{})
    assert d['disposition']=='COMPLETED_RESULT_CANDIDATE'
    assert not p._eligible(d,d,'2026-11-24')


def test_portugal2019_completed306_not_dutch_cancellations():
    names=[f'Team{i}'for i in range(18)];rs=[row(str(i*18+j),2019,date='2020-07-26',home=h,away=a)for i,h in enumerate(names)for j,a in enumerate(names)if h!=a]
    ds=[p.decide([r],{}, {},{})for r in rs];counts=p.reconcile(rs,ds)
    assert len(rs)==306 and counts['dispositions']=={'COMPLETED_RESULT_CANDIDATE':306}


@pytest.mark.parametrize('home,away',[('Benfica','Benfica B'),('Porto','Porto B'),('Sporting CP','Sporting B'),('Vitoria SC','Vitoria FC'),('AVS','Aves'),('CF Os Belenenses','Belenenses SAD')])
def test_identity_boundaries_are_not_merged(home,away):
    a=p.decide([row(home=home,away='Other')],{}, {},{});b=p.decide([row(home=away,away='Other')],{}, {},{})
    assert a['fixture_id']!=b['fixture_id']and a['approved_values']['home']==home and b['approved_values']['home']==away


def test_unknown_admin_without_exact_case_fails_closed():
    d=p.decide([row()],{}, {'ordinary':['KNOWN_ABANDONMENT_REQUIRES_REVIEW']},{})
    assert d['disposition']=='HOLD_OUT'and not p._eligible(d,d,'2026-11-24')


@pytest.mark.parametrize('change',['date','FT'])
def test_unapproved_source_conflicts_not_silently_selected(change):
    a=row();b=row('modern',modern=True)
    if change=='date':b['date']='2000-08-21'
    else:b.update(FT='2-0',hg='2')
    assert p.decide([a,b],{}, {},{})['disposition']=='HOLD_OUT'


def test_unresolved_historical_contradiction_is_holdout():
    r=row();hr={'ordinary':dict(original=deepcopy(r),assessment=dict(classification='CONTRADICTED',contradicted={'date':{}},evidence_ids=[]))}
    assert p.decide([r],hr,{}, {})['disposition']=='HOLD_OUT'


def test_review_binding_tamper_rejected():
    r=row();other=deepcopy(r);other['home']='Forged'
    with pytest.raises(ValueError,match='Historical binding'):p.decide([r],{'ordinary':dict(original=other)}, {},{})


def test_registry_source_loss_or_duplicate_rejected():
    rs=[row(),row('m',modern=True)];d=p.decide(rs,{}, {},{})
    with pytest.raises(ValueError,match='Lost/duplicated'):p.reconcile(rs+[row('lost')],[d])
    with pytest.raises(ValueError):p.reconcile(rs,[d,d])


def test_unknown_disposition_rejected():
    r=row();d=p.decide([r],{}, {},{});d['disposition']='NEW_UNJUSTIFIED'
    with pytest.raises(ValueError,match='invalid category'):p.reconcile([r],[d])


@pytest.mark.parametrize('field',['source_bindings','chronology','approved_values','disposition','model_training_permission'])
def test_decision_tampering_rejected(field):
    d=p.decide(*case('SANTA_BENFICA'));bad=deepcopy(d);bad[field]='forged'
    with pytest.raises(ValueError,match='Altered/incomplete'):p._eligible(d,bad,'2021-01-05')


def test_unknown_availability_and_future_rejected():
    d=p.decide([row()],{}, {},{})
    assert not p._eligible(d,d,'2026-11-24')
    d=p.decide(*case('NACIONAL_BENFICA'))
    assert not p._eligible(d,d,'2024-12-18')


def test_missing_completion_cannot_pass_availability_day():
    d=p.decide(*case('SANTA_BENFICA'));d['chronology']['completion_date']=None
    assert not p._eligible(d,d,'2021-01-05')


def test_availability_cannot_precede_completion():
    d=p.decide(*case('SANTA_BENFICA'));d['chronology']['effective_result_availability_date']='2021-01-02'
    assert not p._eligible(d,d,'2021-01-05')


def test_supplementary_result_not_approved():
    d=p.decide(*case('SANTA_BENFICA'));d['supplement_approved']=True
    assert not p._eligible(d,d,'2021-01-05')


def test_gate_rejects_missing_or_tampered_saved_artifact(tmp_path,monkeypatch):
    d=p.decide(*case('SANTA_BENFICA'));outputs={n:dict(phase=6)for n in p.NAMES};outputs[p.NAMES[1]]=dict(records=[d])
    monkeypatch.setattr(p,'build',lambda *args:deepcopy(outputs))
    for n,obj in outputs.items():(tmp_path/n).write_bytes(p.c.encode(obj))
    gate=p.PredictionGate(tmp_path,tmp_path)
    assert gate.eligible_for_prediction(d,'2021-01-05')and not gate.training_allowed(d,'2021-01-05')
    (tmp_path/p.NAMES[0]).write_bytes(b'{}')
    with pytest.raises(ValueError,match='Altered/missing'):p.PredictionGate(tmp_path,tmp_path)


def test_gate_unknown_fixture_rejected(tmp_path,monkeypatch):
    outputs={n:dict(phase=6)for n in p.NAMES};outputs[p.NAMES[1]]=dict(records=[]);monkeypatch.setattr(p,'build',lambda *a:outputs)
    for n,obj in outputs.items():(tmp_path/n).write_bytes(p.c.encode(obj))
    with pytest.raises(ValueError,match='Unknown fixture'):p.PredictionGate(tmp_path,tmp_path).eligible_for_prediction({},'2020-01-01')


def test_order_independent_decision_bytes():
    rs=[row(),row('m',modern=True)]
    assert p.c.encode(p.decide(rs,{}, {},{}))==p.c.encode(p.decide(list(reversed(rs)),{}, {},{}))


def test_frozen_phase5_evidence_tamper_rejected(tmp_path,monkeypatch):
    monkeypatch.setattr(p.review,'protect',lambda *a:{})
    (tmp_path/'frozen').write_bytes(b'changed');(tmp_path/'PLANNING_LOG.md').write_bytes(b'old\n')
    baseline=dict(approval='PHASE6_POLICY_ONLY',files={'frozen':p.c.sha(b'original')},planning_log=dict(bytes=4,sha256=p.c.sha(b'old\n')))
    (tmp_path/p.BASELINE).write_bytes(p.c.encode(baseline))
    with pytest.raises(ValueError,match='Frozen Phase2'):p.protect(tmp_path,tmp_path)


def test_unknown_annotation_cannot_silently_be_candidate():
    r=row();r['annotation']='[awarded]'
    with pytest.raises(ValueError,match='Unreviewed source annotation'):p.decide([r],{}, {},{})


def test_invalid_score_and_stage_rejected():
    r=row();r['hg']='9'
    with pytest.raises(ValueError,match='Invalid scored'):p.decide([r],{}, {},{})
    r=row();r['stage']='PLAYOFF'
    with pytest.raises(ValueError,match='Non-approved stage'):p.decide([r],{}, {},{})


def synthetic_overlaps():
    h={'seasons':[]};m={'seasons':[]};o={'seasons':[]}
    for year in range(2018,2025):
        season=f'{year}/{year+1}';left=[];right=[];comparisons=[]
        for i in range(18):
            for j in range(18):
                if i==j:continue
                a=row(f'h{year}-{i}-{j}',year,home=f'H{i}',away=f'H{j}');b=row(f'm{year}-{i}-{j}',year,True,home=f'M{i}',away=f'M{j}')
                if i==0 and j==1 and year in [2019,2020]:
                    spec=p.SPECS['SANTA_PACOS'if year==2019 else'SANTA_BENFICA'];a['audit_id']=spec['rows'][0][0];b['audit_id']=spec['rows'][1][0];a['date']=spec['rows'][0][2];b['date']=spec['rows'][1][2]
                left.append(a);right.append(b);comparisons.append(dict(historical_id=a['audit_id'],modern_id=b['audit_id']))
        h['seasons'].append(dict(assessment=dict(season=season),records=left));m['seasons'].append(dict(assessment=dict(season=season),records=right));o['seasons'].append(dict(season=season,mapping=[dict(season=season,historical=f'H{i}',modern=f'M{i}')for i in range(18)],comparisons=comparisons))
    return h,m,o


def test_all2142_season_bound_correspondences_reconstructed():
    h,m,o=synthetic_overlaps();result=p.verify_correspondences(h,m,o)
    assert len(result)==7 and sum(len(x['pairs'])for x in result)==2142
    assert all(x['status']=='APPROVED_EXACT_SEASON_FIXTURE_REPRESENTATION_ONLY'for x in result)


def test_mapping_cannot_cross_seasons_or_merge_clubs():
    h,m,o=synthetic_overlaps();o['seasons'][0]['mapping'][0]['season']='2019/2020'
    with pytest.raises(ValueError,match='cross-season'):p.verify_correspondences(h,m,o)
    h,m,o=synthetic_overlaps();o['seasons'][0]['mapping'][0]['modern']='M1'
    with pytest.raises(ValueError,match='Ambiguous'):p.verify_correspondences(h,m,o)


def test_join_cannot_silently_rebind_comparator_or_change_score():
    h,m,o=synthetic_overlaps();o['seasons'][0]['comparisons'][0]['modern_id']='different'
    with pytest.raises(ValueError,match='Overlap binding'):p.verify_correspondences(h,m,o)
    h,m,o=synthetic_overlaps();m['seasons'][0]['records'][0]['FT']='8-0'
    with pytest.raises(ValueError,match='score contradiction'):p.verify_correspondences(h,m,o)
