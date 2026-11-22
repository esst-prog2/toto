"""Synthetic evidence-strength, source-binding and reproducibility safeguards."""
from copy import deepcopy
import json
import pytest
from scripts import verify_ligue2_review as v


def record(year=2014,key='one',flags=None):
    return dict(audit_id=f'{year}:{key}',source='synthetic.txt',source_sha256='digest',source_line=4,physical_line_sha256='linehash',
        season=f'{year}/{year+1}',date=f'{year}-08-01',home='Home',away='Away',FT='2-1',annotation='',round=1,
        assessment=dict(flags=flags or [],score_bearing=True))


def evidence(r=None,access='DIRECT',independence='INDEPENDENT_NARRATIVE',facts=None):
    r=r or record()
    return dict(id='E1',url='https://example.org/report',title='Synthetic authored match report',organization='Synthetic publisher',publication_date='2014-08-01',
        access_date='2026-11-22',access=access,independence=independence,establishes='Narrow synthetic match facts',limitations='No exhaustive finality/availability or rights clearance',
        fixture_claims=[dict(audit_id=r['audit_id'],facts={k:r[k] for k in v.FACTS} if facts is None else facts)],context_claims=[])


def test_direct_four_facts_not_processing_clearance():
    r=record();a=v.assess_fixture(r,[evidence(r)])
    assert a['classification']=='FULLY_CORROBORATED' and len(a['directly_corroborated_facts'])==4
    assert a['effective_result_availability'] is None and a['phase6_policy']=='NOT_DECIDED';assert r['FT']=='2-1'


@pytest.mark.parametrize('access',['INDEX_ONLY','INACCESSIBLE'])
def test_index_or_inaccessible_not_direct_confirmation(access):
    r=record();a=v.assess_fixture(r,[evidence(r,access=access)]);assert a['classification']=='UNRESOLVED' and not a['directly_corroborated_facts']


@pytest.mark.parametrize('independence',['COMPILED_OR_UNESTABLISHED','SAME_UPSTREAM'])
def test_different_website_not_automatically_independent(independence):
    r=record();assert v.assess_fixture(r,[evidence(r,independence=independence)])['classification']=='UNRESOLVED'


def test_partial_does_not_become_full():
    r=record();a=v.assess_fixture(r,[evidence(r,facts={'home':'Home','away':'Away'})]);assert a['classification']=='PARTIALLY_CORROBORATED'


def test_direct_conflict_preserved_without_correction():
    r=record();a=v.assess_fixture(r,[evidence(r,facts={'FT':'0-3'})]);assert a['classification']=='CONTRADICTED'
    assert a['contradictions']==[dict(field='FT',source='2-1',evidence='0-3',evidence_id='E1')];assert r['FT']=='2-1'


def test_unrelated_fixture_claim_does_not_transfer():
    r=record();e=evidence(record(key='other'));assert v.assess_fixture(r,[e])['classification']=='UNRESOLVED'


def test_context_is_not_fixture_confirmation():
    r=record();e=evidence(r,facts={});e['context_claims']=['2014/2015:R1'];a=v.assess_fixture(r,[e])
    assert a['classification']=='UNRESOLVED' and a['direct_independent_context_evidence_ids']==['E1']


def test_other_round_context_not_transferred():
    r=record();e=evidence(r,facts={});e['context_claims']=['2014/2015:R2'];assert not v.assess_fixture(r,[e])['context_evidence_ids']


def test_cancellation_aggregate_not_individual_certification():
    r=record(2019);r.update(FT=None,annotation='[cancelled]');e=evidence(r,facts={});e['context_claims']=['CANCEL2019'];e['independence']='OFFICIAL_RECORD'
    a=v.assess_fixture(r,[e]);assert a['classification']=='UNRESOLVED' and a['direct_independent_context_evidence_ids']==['E1'];assert r['FT'] is None


@pytest.mark.parametrize('change',[
 {'url':'http://example.org'}, {'access':'SNIPPET_VERIFIED'}, {'independence':'AUTOMATICALLY_INDEPENDENT'},
 {'organization':''}, {'limitations':''}, {'title':''}, {'access_date':'not-a-date'}, {'publication_date':'2020-99-99'},
 {'fixture_claims':[dict(audit_id='one',facts={'accuracy':'100%'})]}, {'fixture_claims':[dict(audit_id='one',facts={'FT':None})]}])
def test_invalid_bibliography_rejected(change):
    e=evidence();e.update(change)
    with pytest.raises((ValueError,KeyError)):v.validate_evidence(e)


def test_duplicate_json_key_rejected(tmp_path):
    p=tmp_path/'test.json';p.write_text('{"a":1,"a":2}')
    with pytest.raises(ValueError):v.read(p)


def report():
    return dict(records=[record(y) for y in range(2014,2025)],seasons=[dict(season=f'{y}/{y+1}',wide_rounds=[],source_order_date_reversals=[]) for y in range(2014,2025)])


def test_selection_reproducible_and_not_evidence_dependent():
    r=report();a=v.select(r);r['records'].reverse();assert a==v.select(r);assert len(a['ordinary'])==11


def test_flagged_or_cancelled_not_ordinary_sample():
    r=report();r['records'][0]['assessment']['flags']=['WIDE_ROUND']
    with pytest.raises(ValueError):v.select(r)


def test_queue_members_categories_and_bindings_checked():
    r=report();r['records'][0]['assessment']['flags']=['WIDE_ROUND'];q=dict(fixtures=[deepcopy(r['records'][0])]);v.verify_queue(r,q)
    q['fixtures'][0]['FT']='9-9'
    with pytest.raises(ValueError):v.verify_queue(r,q)


def test_queue_omission_rejected():
    r=report();r['records'][0]['assessment']['flags']=['WIDE_ROUND']
    with pytest.raises(ValueError):v.verify_queue(r,dict(fixtures=[]))


def test_overlap_not_double_counted():
    r=report();r['records'][0]['assessment']['flags']=['WIDE_ROUND','DIAGNOSTIC_DATE_OUTLIER','SOURCE_ORDER_DATE_REVERSAL']
    a=v.verify_queue(r,dict(fixtures=[deepcopy(r['records'][0])]))
    assert a['queue']==1 and a['outliers_in_wide']==1 and a['reversal_endpoints_in_wide']==1 and a['additional_reversal_endpoints']==0


def setup_build(tmp_path,monkeypatch):
    r=report();q=dict(fixtures=[]);selection=v.select(r);e=evidence(r['records'][0])
    ledger=dict(fixtures=[dict(audit_id=x['audit_id'],original=v.binding(x),categories=[],research_mode='PRIORITY_FIXTURE_RESEARCH',evidence_ids=['E1'] if i==0 else [],open_questions=['Finality and availability not decided']) for i,x in enumerate(r['records'])],
        wide_rounds=[],reversals=[],identity_review={},cancellation_review={},coverage={},special_cases=[],additional_discoveries=[])
    for name,obj in [(v.structure.REPORT,r),(v.structure.QUEUE,q),(v.SELECTION,selection),(v.REFERENCES,dict(evidence=[e])),(v.LEDGER,ledger)]:
        (tmp_path/name).write_bytes(v.base.encode(obj))
    monkeypatch.setattr(v,'protect',lambda *a:dict(synthetic=True));return r,ledger


def test_build_reproducible_and_keeps_uncertainty(tmp_path,monkeypatch):
    setup_build(tmp_path,monkeypatch);a,b=v.build(tmp_path,tmp_path);a2,b2=v.build(tmp_path,tmp_path)
    assert v.base.encode(a)==v.base.encode(a2) and v.base.encode(b)==v.base.encode(b2)
    assert a['summary']['fixture_classifications']=={'FULLY_CORROBORATED':1,'UNRESOLVED':10}


@pytest.mark.parametrize('mutation',['sample','binding','categories','unknown_reference','missing_fixture','duplicate_fixture','unknown_claim'])
def test_registry_mutations_fail(tmp_path,monkeypatch,mutation):
    r,ledger=setup_build(tmp_path,monkeypatch)
    if mutation=='sample':
        p=tmp_path/v.SELECTION;d=v.read(p);d['ordinary'][0]['FT']='wrong';p.write_bytes(v.base.encode(d))
    elif mutation=='binding':ledger['fixtures'][0]['original']['source_line']=100
    elif mutation=='categories':ledger['fixtures'][0]['categories']=['WIDE_ROUND']
    elif mutation=='unknown_reference':ledger['fixtures'][0]['evidence_ids']=['UNKNOWN']
    elif mutation=='missing_fixture':ledger['fixtures'].pop()
    elif mutation=='duplicate_fixture':ledger['fixtures'].append(deepcopy(ledger['fixtures'][0]))
    else:
        p=tmp_path/v.REFERENCES;d=v.read(p);d['evidence'][0]['fixture_claims'][0]['audit_id']='UNKNOWN';p.write_bytes(v.base.encode(d))
    (tmp_path/v.LEDGER).write_bytes(v.base.encode(ledger))
    with pytest.raises(ValueError):v.build(tmp_path,tmp_path)


def test_previous_evidence_protected(tmp_path,monkeypatch):
    d=tmp_path/'private';d.mkdir();p=tmp_path/'frozen';p.write_bytes(b'original');log=tmp_path/'PLANNING_LOG.md';log.write_bytes(b'log\n')
    monkeypatch.setattr(v.structure,'protect',lambda *a:None)
    (d/v.BASELINE).write_bytes(v.base.encode(dict(files={'frozen':v.base.sha(b'original')},planning_log=dict(bytes=4,sha256=v.base.sha(b'log\n')))))
    assert v.protect(d,tmp_path)['phase2_4_entries']==1;log.write_bytes(b'log\nappend\n');v.protect(d,tmp_path)
    p.write_bytes(b'changed')
    with pytest.raises(ValueError):v.protect(d,tmp_path)


@pytest.mark.parametrize('access,independent,raises',[('DIRECT','OFFICIAL_RECORD',False),('DIRECT','INDEPENDENT_NARRATIVE',False),('INDEX_ONLY','OFFICIAL_RECORD',True),('DIRECT','COMPILED_OR_UNESTABLISHED',True)])
def test_documented_context_requires_direct_independent_claim(access,independent,raises):
    e=evidence(access=access,independence=independent,facts={});e['context_claims']=['2014/2015:R1']
    item=dict(classification='DOCUMENTED',limitations='Only context, not every fixture',finding='Documented scheduling event',evidence_ids=['E1'],member_ids=['one'])
    if raises:
        with pytest.raises(ValueError):v.validate_context(item,('2014/2015','1'),{'E1':e},{'one'})
    else:v.validate_context(item,('2014/2015','1'),{'E1':e},{'one'})


def test_context_members_and_scope_must_match():
    e=evidence(facts={});e['context_claims']=['2014/2015:R2'];item=dict(classification='DOCUMENTED',limitations='Limited',finding='Context',evidence_ids=['E1'],member_ids=['one'])
    with pytest.raises(ValueError):v.validate_context(item,('2014/2015','1'),{'E1':e},{'one'})
    item['classification']='PARTIAL';item['member_ids']=['wrong']
    with pytest.raises(ValueError):v.validate_context(item,('2014/2015','1'),{'E1':e},{'one'})


@pytest.mark.parametrize('field,value',[('effective_result_availability','2014-08-01'),('phase6_processing_policy','HOLD_OUT')])
def test_evidence_cannot_assign_phase6_processing_policy(tmp_path,monkeypatch,field,value):
    r,ledger=setup_build(tmp_path,monkeypatch);case=dict(original=v.binding(r['records'][0]),effective_result_availability=None,phase6_processing_policy='NOT_DECIDED');case[field]=value;ledger['special_cases']=[case]
    (tmp_path/v.LEDGER).write_bytes(v.base.encode(ledger))
    with pytest.raises(ValueError):v.build(tmp_path,tmp_path)
