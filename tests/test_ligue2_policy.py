"""Synthetic policy tests; no private data or network required."""
from copy import deepcopy
import pytest
from scripts import decide_ligue2_policy as p


def row(key='ordinary'):
    spec=p.SPECS.get(key,('ORDINARY','2020/2021','2020-10-01','AC Ajaccio','Gazélec FC Ajaccio','1-0',None))
    _,season,date,home,away,ft,_=spec
    hg,ag=ft.split('-')
    return dict(audit_id=key,season=season,date=date,home=home,away=away,FT=ft,hg=hg,ag=ag,annotation='[awarded]' if key in p.ADMIN else '',source='pinned.txt',source_sha256='a'*64,source_line=12,physical_line_sha256='b'*64,provenance={'commit':'c'*40,'git_blob_sha1':'d'*40},source_competition_title='French Ligue 2',assessment=dict(flags=[],errors=[],structurally_valid=True,score_bearing=True,source_cancelled=False,source_awarded=key in p.ADMIN,chronology={'source_heading_date':date}))


def evidence(r):
    return dict(original=p.review.binding(r),assessment={'classification':'FULLY_CORROBORATED'},evidence_ids=['direct'],open_questions=['Rights unverified'])


def case(r):
    return dict(original=p.review.binding(r),original_kickoff_date='2024-10-26',documented_resumption_completion_date='2024-12-03',corroborated_ft='0-0')


@pytest.mark.parametrize('key',sorted(p.ADMIN))
def test_administrative_hold_out(key):
    r=row(key);d=p.decide(r,evidence(r),case(r))
    assert d['disposition']=='ADMINISTRATIVE_HOLD_OUT'
    assert d['original']==p.review.binding(r)
    assert d['chronology']['effective_result_availability_date'] is None
    assert d['chronology']['administrative_publication_date']==p.SPECS[key][-1]
    assert not p.eligible_for_prediction(d,r,'2030-01-01',historical=evidence(r),case=case(r))


def completion():
    key=next(k for k,v in p.SPECS.items() if v[0]=='AJACCIO_BASTIA');r=row(key);h=evidence(r);c=case(r)
    return r,h,c,p.decide(r,h,c)


def test_same_fixture_completion_without_rewrite():
    r,h,c,d=completion()
    assert d['original']==p.review.binding(r)
    assert d['chronology']['actual_kickoff_date']=='2024-10-26'
    assert d['chronology']['completion_date']=='2024-12-03'
    assert d['disposition']=='COMPLETED_RESULT_CANDIDATE'


@pytest.mark.parametrize('cutoff,allowed',[('2024-10-27',False),('2024-12-02',False),('2024-12-03',False),('2024-12-04',True)])
def test_strict_completion_cutoff(cutoff,allowed):
    r,h,c,d=completion();assert p.eligible_for_prediction(d,r,cutoff,historical=h,case=c) is allowed
    assert not p.training_allowed(d,r,cutoff,historical=h,case=c)


@pytest.mark.parametrize('classification',['UNRESOLVED','PARTIALLY_CORROBORATED','CONTRADICTED'])
def test_completion_insufficient_evidence(classification):
    r,h,c,d=completion();h['assessment']['classification']=classification
    with pytest.raises(ValueError):p.decide(r,h,c)


def test_unusual_score_retained():
    key=next(k for k,v in p.SPECS.items() if v[0]=='VALENCIENNES_BEZIERS');r=row(key)
    d=p.decide(r,evidence(r),case(r));assert d['original']['FT']=='5-6';assert d['disposition']=='COMPLETED_RESULT_CANDIDATE'


def test_exactly_one_hundred_not_played_synthetic():
    records=[]
    for i in range(100):
        r=row('cancel'+str(i));r.update(season='2019/2020',FT=None,hg=None,ag=None,annotation='[cancelled]');r['assessment'].update(source_cancelled=True,score_bearing=False)
        records.append(p.decide(r))
    assert len(records)==100 and all(x['disposition']=='NOT_PLAYED' and x['chronology']['proxy_date'] is None for x in records)


@pytest.mark.parametrize('flag',['WIDE_ROUND','DIAGNOSTIC_DATE_OUTLIER','SOURCE_ORDER_DATE_REVERSAL'])
@pytest.mark.parametrize('classification',['UNRESOLVED','PARTIALLY_CORROBORATED','FULLY_CORROBORATED'])
def test_flags_and_uncertainty_not_automatic_exclusion(flag,classification):
    r=row();r['assessment']['flags']=[flag];h=evidence(r);h['assessment']['classification']=classification
    d=p.decide(r,h);assert d['disposition']=='COMPLETED_RESULT_CANDIDATE'
    assert not p.eligible_for_prediction(d,r,'2030-01-01',historical=h)


def test_unknown_admin_fails_closed():
    r=row();r['assessment']['source_awarded']=True
    with pytest.raises(ValueError):p.decide(r)


def test_contradiction_requires_decision():
    r=row();h=evidence(r);h['assessment']['classification']='CONTRADICTED'
    with pytest.raises(ValueError):p.decide(r,h)


@pytest.mark.parametrize('field',['date','home','away','FT','season','source_line','source_sha256'])
def test_binding_tamper(field):
    r=row();h=evidence(r);r[field]='changed'
    with pytest.raises(ValueError):p.decide(r,h)


@pytest.mark.parametrize('field',['disposition','decision_id','model_training_permission','chronology'])
def test_saved_decision_tampering(field):
    r,h,c,d=completion();d[field]='tampered'
    with pytest.raises(ValueError):p.eligible_for_prediction(d,r,'2025-01-01',historical=h,case=c)


def test_distinct_identity_and_deterministic_ids():
    r=row();before=deepcopy(r);a=p.decide(r);assert r==before and p.decide(r)==a
    other=deepcopy(r);other['home']='Gazélec FC Ajaccio';other['away']='AC Ajaccio'
    assert p.candidate_id(other)!=p.candidate_id(r)
    assert a['original']['home']=='AC Ajaccio' and a['original']['away']=='Gazélec FC Ajaccio'


@pytest.mark.parametrize('bad',['2024-1-01','2024-02-30',None,'2024-12-03T10:00:00'])
def test_cutoff_format(bad):
    r,h,c,d=completion()
    with pytest.raises(ValueError):p.eligible_for_prediction(d,r,bad,historical=h,case=c)


def test_conflicting_cancelled_score():
    r=row();r['assessment']['source_cancelled']=True
    with pytest.raises(ValueError):p.decide(r)


def test_unknown_flag():
    r=row();r['assessment']['flags']=['NEW_INTERRUPTION']
    with pytest.raises(ValueError):p.decide(r)


def test_exception_needs_binding():
    r,h,c,d=completion();c['original']['source_line']=999
    with pytest.raises(ValueError):p.decide(r,h,c)
