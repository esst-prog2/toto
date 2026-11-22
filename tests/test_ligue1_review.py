"""Fail-closed evidence accounting; synthetic records, no web or private data."""
from copy import deepcopy
import json

import pytest

from scripts import verify_ligue1_review as v


def record(n=0,year=1990,flags=(),outcome='H'):
    return dict(audit_id=f'ligue1:{n}',source='synthetic.txt',source_sha256='sourcehash',
                source_line=n+1,raw_line_sha256=f'line{n}',season=f'{year}/{year+1}',
                date=f'{year}-08-01',home=f'Home{n}',away=f'Away{n}',FT='1-0',
                assessment=dict(flags=list(flags),goal_derived_outcome=outcome))


def evidence(**kw):
    e=dict(id='E',url='https://example.org/report',title='Synthetic narrative',access='DIRECT',
           independence='INDEPENDENT_NARRATIVE',establishes='Explicit fixture facts',
           access_date='2026-11-22',publication_date='1990-08-01',
           facts={k:record()[k] for k in v.FACTS})
    e.update(kw);return e


def item(r=None):
    r=r or record()
    return dict(audit_id=r['audit_id'],binding=v.binding(r),source_values={k:r[k] for k in v.FACTS},
                roles=['ORDINARY_SAMPLE'],evidence_ids=['E'])


def test_direct_independent_all_four_facts_are_verified_not_finality():
    result=v.fixture_status(item(),{'E':evidence()})
    assert result['status']=='VERIFIED'
    assert result['finality']=='NOT_EXHAUSTIVELY_CERTIFIED'


@pytest.mark.parametrize('access',['INDEX_ONLY','INACCESSIBLE'])
def test_search_index_and_denied_access_cannot_certify_match(access):
    assert v.fixture_status(item(),{'E':evidence(access=access)})['status']=='UNRESOLVED'


@pytest.mark.parametrize('independence',['UNESTABLISHED','SHARED_OR_POSSIBLE_UPSTREAM'])
def test_compiled_or_shared_data_agreement_is_not_independent(independence):
    assert v.fixture_status(item(),{'E':evidence(independence=independence)})['status']=='UNRESOLVED'


def test_partial_facts_do_not_gain_missing_date_from_publication():
    e=evidence(facts={'FT':'1-0','home':'Home0','away':'Away0'})
    assert v.fixture_status(item(),{'E':e})['status']=='PARTIAL'


def test_contradiction_blocks_full_verification_and_preserves_original():
    i=item();before=deepcopy(i);e=evidence();e['facts']['date']='1990-07-31'
    result=v.fixture_status(i,{'E':e})
    assert result['status']=='PARTIAL' and result['contradictions'][0]['field']=='date'
    assert i==before


def test_teams_require_literal_fixture_binding_no_global_mapping():
    e=evidence();e['facts']['away']='Gazélec' # cannot silently become AC Ajaccio
    assert v.fixture_status(item(),{'E':e})['contradictions']


@pytest.mark.parametrize('change',[dict(url='http://example.org'),dict(title=''),dict(facts={'winner':'A'}),dict(access='MAYBE'),dict(facts={'date':'bad'}),dict(facts={'FT':None})])
def test_invalid_evidence_fails_actionably(change):
    with pytest.raises(ValueError):v.validate_evidence(evidence(**change))


def test_duplicate_json_keys_rejected(tmp_path):
    p=tmp_path/'duplicate.json';p.write_text('{"id":1,"id":2}')
    with pytest.raises(ValueError,match='Duplicate'):v.read(p)


def test_selection_stable_under_order_and_excludes_flagged_records():
    rows=[record(0),record(1),record(2,flags=['UNUSUAL_SCORE'])]
    chosen=v.selection(rows)
    assert chosen==v.selection(list(reversed(rows))) and len(chosen)==1
    assert chosen[0]['audit_id']!='ligue1:2'


def test_selection_covers_draw_home_and_away_strata():
    rows=[record(0,1990),record(1,1991,outcome='D'),record(2,2016,outcome='A')]
    assert len(v.selection(rows))==3


def test_missing_ordinary_stratum_fails_instead_of_selecting_exception():
    with pytest.raises(ValueError,match='stratum'):v.selection([record(flags=['EXCEPTION'])])


def synthetic_build(tmp_path,monkeypatch):
    rows=[record(n,flags=() if n==0 else ['EXCEPTION']) for n in range(6)]
    ids=[r['audit_id'] for r in rows]
    report=dict(records=rows,seasons=[dict(season='1990/1991',wide_rounds=[dict(round=1,affected_ids=ids)])],
                totals=dict(category_counts=dict(SYSTEMATIC_SOURCE_LABEL_DEFECT=0)))
    ledger=dict(evidence=[evidence()],fixtures=[item(rows[0])],rounds=[dict(season='1990/1991',round=1,
                affected_ids=ids,source_observations=[v.binding(r) for r in rows],status='PARTIAL',evidence_ids=['E'],individually_certified_all_members=False)],
                major_cases=[dict(audit_id=r['audit_id'],binding=v.binding(r),evidence_ids=['E'],chronology=dict(effective_result_availability=None)) for r in rows],
                missing_fixture=dict(source_observation_exists=False),grouped_label_analysis=dict(applied=False,primary_defects=0))
    for name,data in [(v.structural.REPORT,report),(v.SELECTION,dict(ordinary=[v.binding(rows[0])])),(v.LEDGER,ledger)]:
        (tmp_path/name).write_bytes(v.base.encode(data))
    monkeypatch.setattr(v,'protect',lambda *args:dict(synthetic=True))
    return report,ledger


def save_ledger(tmp_path,ledger):
    (tmp_path/v.LEDGER).write_bytes(v.base.encode(ledger))


def test_build_deterministic_and_counts_distinct_fixtures_not_round_members(tmp_path,monkeypatch):
    synthetic_build(tmp_path,monkeypatch)
    a=v.build(tmp_path,tmp_path);b=v.build(tmp_path,tmp_path)
    assert v.base.encode(a)==v.base.encode(b)
    assert a['individually_reviewed']==1 and a['scheduling_affected_slots']==6
    assert a['standardized_rows']==0


@pytest.mark.parametrize('mutation,message',[
    ('binding','misbound'),('missing_sample','sample missing'),('duplicate_fixture','Duplicate/unknown'),
    ('missing_round','Scheduling scope'),('round_binding','source binding changed'),
    ('certify_round','cannot certify'),('date_policy','cannot implement'),
    ('label_policy','cannot apply'),('supplement','cannot add'),('duplicate_evidence','Duplicate evidence')])
def test_scope_and_phase_guards(tmp_path,monkeypatch,mutation,message):
    report,ledger=synthetic_build(tmp_path,monkeypatch)
    if mutation=='binding':ledger['fixtures'][0]['binding']['date']='1990-08-02'
    if mutation=='missing_sample':ledger['fixtures']=[]
    if mutation=='duplicate_fixture':ledger['fixtures']*=2
    if mutation=='missing_round':ledger['rounds']=[]
    if mutation=='round_binding':ledger['rounds'][0]['source_observations'][0]['FT']='2-0'
    if mutation=='certify_round':ledger['rounds'][0]['individually_certified_all_members']=True
    if mutation=='date_policy':ledger['major_cases'][0]['chronology']['effective_result_availability']='1990-08-01'
    if mutation=='label_policy':ledger['grouped_label_analysis']['applied']=True
    if mutation=='supplement':ledger['missing_fixture']['source_observation_exists']=True
    if mutation=='duplicate_evidence':ledger['evidence']*=2
    save_ledger(tmp_path,ledger)
    with pytest.raises(ValueError,match=message):v.build(tmp_path,tmp_path)


def test_documented_round_requires_direct_independent_document(tmp_path,monkeypatch):
    _,ledger=synthetic_build(tmp_path,monkeypatch);ledger['rounds'][0]['status']='DOCUMENTED';ledger['evidence'][0]['access']='INDEX_ONLY';save_ledger(tmp_path,ledger)
    with pytest.raises(ValueError,match='lacks direct'):v.build(tmp_path,tmp_path)


def test_source_hash_and_line_changes_change_audit_binding():
    a=record();b=deepcopy(a);b['source_sha256']='other'
    assert v.binding(a)!=v.binding(b)
    b=deepcopy(a);b['source_line']+=1
    assert v.binding(a)!=v.binding(b)


def test_protection_rejects_frozen_evidence_mutation(tmp_path,monkeypatch):
    monkeypatch.setattr(v.structural,'protect',lambda *args:{})
    (tmp_path/'frozen.txt').write_bytes(b'original')
    (tmp_path/'PLANNING_LOG.md').write_bytes(b'old\nnew\n')
    baseline=dict(files={'frozen.txt':v.base.sha(b'original')},planning_log=dict(bytes=4,sha256=v.base.sha(b'old\n')))
    (tmp_path/v.BASELINE).write_bytes(v.base.encode(baseline))
    assert v.protect(tmp_path,tmp_path)['phase2_4_entries']==1
    (tmp_path/'frozen.txt').write_bytes(b'changed')
    with pytest.raises(ValueError,match='Frozen'):v.protect(tmp_path,tmp_path)


def test_supplemental_conflict_must_bind_exact_original_csv(tmp_path,monkeypatch):
    _,ledger=synthetic_build(tmp_path,monkeypatch)
    path=v.structural.metadata.HIST;(tmp_path/path).parent.mkdir(parents=True)
    raw=b'Date,Season,home,visitor,FT,hgoal,vgoal,division,tier,totgoal,goaldif,result\n1990-08-01,1990,Alpha,Beta,0-3,0,3,1,1,3,-3,D\n'
    (tmp_path/path).write_bytes(raw)
    r=v.structural.read_csv(raw,path,v.base.sha(raw))[0]
    ledger['major_cases'][0]['overlapping_source_bindings']=[v.binding(r)];save_ledger(tmp_path,ledger)
    assert v.build(tmp_path,tmp_path)['individually_reviewed']==1
    ledger['major_cases'][0]['overlapping_source_bindings'][0]['FT']='0-0';save_ledger(tmp_path,ledger)
    with pytest.raises(ValueError,match='Supplemental'):v.build(tmp_path,tmp_path)
