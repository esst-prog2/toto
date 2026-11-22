"""Synthetic Phase 7 projection, screening and source binding tests."""
from copy import deepcopy
import json
import pytest
from scripts import standardize_ligue2_results as s
from scripts import decide_ligue2_policy as p
from test_ligue2_policy import row, evidence, case, completion


def fixture(key='ordinary'):
    r=row(key);r['stage']='REGULAR_SEASON';return r


def plans_for(r,h=None,c=None):
    return s.prepare([r],[p.decide(r,h,c)],{r['audit_id']:h} if h else {},{r['audit_id']:c} if c else {})


def test_exact_schema_and_shared_algorithm(tmp_path):
    r=fixture();plans=plans_for(r);raw,summary=s.convert(plans,tmp_path);rows=s.parse_standard(raw)
    assert raw.splitlines()[0]==b'match_id,date,league,season,home_team,away_team,home_goals,away_goals'
    assert rows[0]==plans[0]['projection']
    assert rows[0]['match_id']==s.standard_id(rows[0])
    assert summary['accepted']==1
    assert s.verify_subset(rows,plans)['screened']==1


@pytest.mark.parametrize('key',sorted(p.ADMIN))
def test_administrative_holdouts_absent(key):
    r=fixture(key);plans=plans_for(r,evidence(r),case(r))
    assert plans[0]['projection'] is None
    assert s.verify_subset([],plans)['administrative_hold_out']==1
    assert plans[0]['original']==r


def test_completion_same_source_date_and_strict_cutoffs():
    r,h,c,d=completion();r['stage']='REGULAR_SEASON';plans=plans_for(r,h,c)
    assert plans[0]['projection']['date']==r['date']=='2024-12-03'
    assert len(plans)==1
    assert not p.eligible_for_prediction(d,r,'2024-12-03',historical=h,case=c)
    assert p.eligible_for_prediction(d,r,'2024-12-04',historical=h,case=c)


def test_high_score_stays():
    key=next(k for k,v in p.SPECS.items() if v[0]=='VALENCIENNES_BEZIERS');r=fixture(key)
    projection=plans_for(r,evidence(r),case(r))[0]['projection']
    assert (projection['home_goals'],projection['away_goals'])==(5,6)


def test_not_played_has_no_projection():
    r=fixture();r.update(season='2019/2020',date='2020-04-01',FT=None,hg=None,ag=None,annotation='[cancelled]');r['assessment'].update(source_cancelled=True,score_bearing=False)
    plans=plans_for(r);assert plans[0]['projection'] is None
    assert s.verify_subset([],plans)['not_played']==1


@pytest.mark.parametrize('field,value',[('disposition','COMPLETED_RESULT_CANDIDATE'),('decision_id','forged'),('chronology',{})])
def test_policy_tamper_rejected(field,value):
    key=next(iter(p.ADMIN));r=fixture(key);h=evidence(r);c=case(r);d=p.decide(r,h,c);d[field]=value
    with pytest.raises(ValueError):s.prepare([r],[d],{r['audit_id']:h},{r['audit_id']:c})


@pytest.mark.parametrize('mutation',['missing','duplicate','wrong_id'])
def test_ambiguous_policy_bindings(mutation):
    r=fixture();d=p.decide(r);ds=[d]
    if mutation=='missing':ds=[]
    if mutation=='duplicate':ds=[d,d]
    if mutation=='wrong_id':ds[0]['original']['audit_id']='different'
    with pytest.raises(ValueError):s.prepare([r],ds,{}, {})


@pytest.mark.parametrize('field,value',[('season','2013/2014'),('stage','PLAYOFF'),('date','2021-12-01'),('home',' AC Ajaccio'),('away','AC Ajaccio')])
def test_scope_or_identity_invalid(field,value):
    r=fixture();r[field]=value
    with pytest.raises(ValueError):plans_for(r)


@pytest.mark.parametrize('flag',['WIDE_ROUND','SOURCE_ORDER_DATE_REVERSAL','DIAGNOSTIC_DATE_OUTLIER'])
def test_flags_not_exclusions(flag):
    r=fixture();r['assessment']['flags']=[flag];plans=plans_for(r)
    assert plans[0]['projection'] is not None
    assert not p.eligible_for_prediction(plans[0]['decision'],r,'2025-01-01')


def test_distinct_ajaccio_labels_and_ids():
    r=fixture();a=plans_for(r)[0]['projection'];r['home'],r['away']=r['away'],r['home'];b=plans_for(r)[0]['projection']
    assert a['match_id']!=b['match_id'];assert a['home_team']=='AC Ajaccio';assert a['away_team']=='Gazélec FC Ajaccio'
    assert s.standard_id(a)!=s.base.sha(json.dumps(['Ligue 1',a['season'],a['date'],a['home_team'],a['away_team']],ensure_ascii=False,separators=(',',':')).encode())


@pytest.mark.parametrize('mutation',['lost','duplicate','goals','date','id','league'])
def test_subset_integrity(mutation):
    plans=plans_for(fixture());rows=[deepcopy(plans[0]['projection'])]
    if mutation=='lost':rows=[]
    elif mutation=='duplicate':rows*=2
    elif mutation=='goals':rows[0]['home_goals']=9
    elif mutation=='date':rows[0]['date']='2020-10-02'
    elif mutation=='id':rows[0]['match_id']='0'*64
    elif mutation=='league':rows[0]['league']='Ligue 1'
    with pytest.raises(ValueError):s.verify_subset(rows,plans)


@pytest.mark.parametrize('raw',[b'date,match_id\n',b'match_id,date,league,season,home_team,away_team,home_goals,away_goals\na,2020-10-01,Ligue 2,2020/2021,A,B,01,0\n',b'match_id,date,league,season,home_team,away_team,home_goals,away_goals\na,2020-10-01,Ligue 2,2020/2021,A,B,-1,0\n'])
def test_bad_csv(raw):
    with pytest.raises(ValueError):s.parse_standard(raw)


def test_order_independence(tmp_path):
    a=fixture();b=fixture('second');b.update(home='Team C',away='Team D',source_line=13)
    plans=s.prepare([a,b],[p.decide(a),p.decide(b)],{},{});raw,_=s.convert(plans,tmp_path);reverse,_=s.convert(list(reversed(plans)),tmp_path)
    assert raw==reverse;assert s.verify_subset(s.parse_standard(raw),plans)['screened']==2


def test_duplicate_pair_rejected():
    a=fixture();b=fixture('second');b['source_line']=13
    with pytest.raises(ValueError):s.prepare([a,b],[p.decide(a),p.decide(b)],{}, {})


def test_archive_physical_binding(tmp_path):
    r=fixture();literal=b'A literal fixture\n';(tmp_path/'pinned.txt').write_bytes(literal)
    r.update(raw_record='A literal fixture',source_line=1,source_sha256=s.base.sha(literal),physical_line_sha256=s.base.sha(literal))
    import hashlib
    r['provenance']['url']='https://example.org/pinned.txt'
    r['provenance']['git_blob_sha1']=hashlib.sha1(b'blob '+str(len(literal)).encode()+b'\0'+literal).hexdigest()
    plans=plans_for(r);original=deepcopy(r);archive=s.archive_records(plans,tmp_path)
    assert archive[0]['original']==original and r==original
    assert archive[0]['approved_standardized_values']==plans[0]['projection']
    (tmp_path/'pinned.txt').write_bytes(b'changed\n')
    with pytest.raises(ValueError):s.archive_records(plans,tmp_path)


def test_holdout_cannot_be_injected():
    key=next(iter(p.ADMIN));r=fixture(key);plans=plans_for(r,evidence(r),case(r))
    fields=dict(date=r['date'],league='Ligue 2',season=r['season'],home_team=r['home'],away_team=r['away'],home_goals=int(r['hg']),away_goals=int(r['ag']))
    injected={k:({'match_id':s.standard_id(fields),**fields})[k] for k in s.OUTPUT_COLUMNS}
    with pytest.raises(ValueError):s.verify_subset([injected],plans)


def test_missing_completion_evidence_cannot_project():
    r,h,c,d=completion();r['stage']='REGULAR_SEASON'
    with pytest.raises(ValueError):s.prepare([r],[d],{}, {r['audit_id']:c})


def test_score_outcome_agrees_with_shared_importer(tmp_path):
    for hg,ag in [(0,0),(5,6),(3,0)]:
        r=fixture();r.update(FT=f'{hg}-{ag}',hg=str(hg),ag=str(ag));plans=plans_for(r)
        raw,_=s.convert(plans,tmp_path);out=s.parse_standard(raw)[0]
        assert (out['home_goals'],out['away_goals'])==(hg,ag)
