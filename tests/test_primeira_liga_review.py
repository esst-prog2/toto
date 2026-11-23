"""Synthetic confidence, provenance, chronology and scope guards; no network/private data."""
from copy import deepcopy
import pytest
from scripts import verify_primeira_liga_review as v


def original():
    return dict(audit_id='A',season='2020/2021',home='Home',away='Away',date='2021-01-03',FT='1-1')


def reference(mode='DIRECT_DOCUMENT',kind='CONTEMPORARY_JOURNALISM'):
    return dict(evidence_id='E',url='https://example.org/report',title='Match report',publisher='example.org',inspection=mode,source_type=kind,claims=['Completed next day'],snapshot=None)


def finding(core=False):
    return dict(audit_id='A',evidence_ids=['E'],facts={},core_independently_supported=core,notes=[],phase6_questions=[])


def test_context_only_never_certifies_fixture():
    result=v.assess(original(),None,{})
    assert result['classification']=='CONTEXT-ONLY REVIEWED'
    assert result['supported']=={}
    assert result['result_availability']=='UNRESOLVED'


@pytest.mark.parametrize('mode',['INDEX_ONLY','ACCESS_RESTRICTED'])
def test_index_or_restricted_document_cannot_verify_facts(mode):
    f=finding();f['facts']={'FT':'1-1'}
    with pytest.raises(ValueError,match='Indexed or inaccessible'):v.assess(original(),f,{'E':reference(mode)})


@pytest.mark.parametrize('mode',['INDEX_ONLY','ACCESS_RESTRICTED'])
def test_index_leads_are_partial_never_full(mode):
    assert v.assess(original(),finding(),{'E':reference(mode)})['classification']=='PARTIALLY CORROBORATED'


def test_no_evidence_remains_unresolved_not_erroneous():
    f=finding();f['evidence_ids']=[]
    result=v.assess(original(),f,{})
    assert result['classification']=='UNRESOLVED'
    assert result['contradicted']=={}


def test_completion_date_conflict_preserves_original_and_score():
    r=original();before=deepcopy(r);f=finding();f['facts']={'date':'2021-01-04','FT':'1-1','completed':True}
    result=v.assess(r,f,{'E':reference()})
    assert result['classification']=='CONTRADICTED'
    assert result['contradicted']['date']==dict(original='2021-01-03',documentary='2021-01-04')
    assert result['supported']['FT']=='1-1'
    assert r==before
    assert result['result_availability']=='UNRESOLVED'


def test_full_core_does_not_certify_finality_or_availability():
    r=original();f=finding(True);f['facts']={k:r[k] for k in v.CORE if k!='completed'};f['facts']['completed']=True
    result=v.assess(r,f,{'E':reference()})
    assert result['classification']=='FULLY CORROBORATED CORE FACTS'
    assert result['administrative_finality']==result['result_availability']=='UNRESOLVED'


@pytest.mark.parametrize('missing',v.CORE)
def test_full_core_requires_every_dimension(missing):
    r=original();f=finding(True);f['facts']={k:r[k] for k in v.CORE if k!='completed'};f['facts']['completed']=True;del f['facts'][missing]
    with pytest.raises(ValueError,match='Full core'):v.assess(r,f,{'E':reference()})


def test_secondary_archive_cannot_silently_become_independent_core():
    r=original();f=finding(True);f['facts']={k:r[k] for k in v.CORE if k!='completed'};f['facts']['completed']=True
    with pytest.raises(ValueError,match='qualified independent'):v.assess(r,f,{'E':reference(kind='QUALIFIED_SECONDARY')})


@pytest.mark.parametrize('key',v.FORBIDDEN)
def test_phase6_processing_decisions_forbidden(key):
    f=finding();f[key]='PENDING'
    with pytest.raises(ValueError,match='Phase6'):v.assess(original(),f,{'E':reference()})


def test_finding_cannot_bind_another_original():
    f=finding();f['audit_id']='other'
    with pytest.raises(ValueError,match='different original'):v.assess(original(),f,{'E':reference()})


def test_direct_document_requires_snapshot(tmp_path):
    with pytest.raises(ValueError,match='no snapshot'):v.inspect_reference(reference(),tmp_path)


def test_snapshot_tampering_detected(tmp_path):
    (tmp_path/'report').write_bytes(b'changed');r=reference();r['snapshot']=dict(path='report',bytes=8,sha256=v.c.sha(b'original'))
    with pytest.raises(ValueError,match='changed'):v.inspect_reference(r,tmp_path)


def test_snapshot_path_escape_rejected(tmp_path):
    r=reference();r['snapshot']=dict(path='../report',bytes=0,sha256='x')
    with pytest.raises(ValueError,match='escape'):v.inspect_reference(r,tmp_path)


def test_sampling_covers32_seasons_and_avoids_flags():
    rows=[]
    for year in range(1994,2026):
        for ident,day in [('flag','01'),('chosen','02'),('later','03')]:
            r=dict(audit_id=str(year)+ident,season=f'{year}/{year+1}',date=f'{year}-08-{day}',home='A',away='B')
            if year<2025:r['original_fields']={}
            rows.append(r)
    selected=v.sample_selection(rows,{str(y)+'flag' for y in range(1994,2026)})
    assert len(selected)==32
    assert all(r['audit_id'].endswith('chosen') for r in selected)
    assert v.sample_selection(list(reversed(rows)),{str(y)+'flag' for y in range(1994,2026)})==selected


def test_conditional_overlap_one_to_one_and_not_global_alias():
    rows=[dict(audit_id=x) for x in 'abc'];o=dict(seasons=[dict(comparisons=[dict(historical_id='a',modern_id='b')])])
    groups=v.group_rows(rows,o)
    assert groups=={'a':('a','b'),'b':('a','b'),'c':('c',)}
    o['seasons'][0]['comparisons'].append(dict(historical_id='c',modern_id='b'))
    with pytest.raises(ValueError,match='Non one-to-one'):v.group_rows(rows,o)


def test_no_upstream_claim_can_certify_without_evidence_claims():
    f=finding();f['facts']={'FT':'1-1'};r=reference();r['claims']=[]
    with pytest.raises(ValueError,match='no inspected claims'):v.assess(original(),f,{'E':r})


def test_frozen_phase4_file_change_rejected(tmp_path,monkeypatch):
    monkeypatch.setattr(v.structure,'protect',lambda *args: {})
    (tmp_path/'frozen').write_bytes(b'changed');(tmp_path/'PLANNING_LOG.md').write_bytes(b'old\n')
    saved=dict(approval='PHASE5_EVIDENCE_ONLY',files={'frozen':v.c.sha(b'original')},planning_log=dict(bytes=4,sha256=v.c.sha(b'old\n')))
    (tmp_path/'phase5_protected_before.json').write_bytes(v.c.encode(saved))
    with pytest.raises(ValueError,match='Frozen evidence'):v.protect(tmp_path,tmp_path)


def test_planning_prefix_append_allowed_rewrite_forbidden(tmp_path,monkeypatch):
    monkeypatch.setattr(v.structure,'protect',lambda *args: {})
    (tmp_path/'frozen').write_bytes(b'original');(tmp_path/'PLANNING_LOG.md').write_bytes(b'old\nnew\n')
    saved=dict(approval='PHASE5_EVIDENCE_ONLY',files={'frozen':v.c.sha(b'original')},planning_log=dict(bytes=4,sha256=v.c.sha(b'old\n')))
    (tmp_path/'phase5_protected_before.json').write_bytes(v.c.encode(saved))
    assert v.protect(tmp_path,tmp_path)['phase2_4_frozen_entries']==1
    (tmp_path/'PLANNING_LOG.md').write_bytes(b'bad\nnew\n')
    with pytest.raises(ValueError,match='prefix changed'):v.protect(tmp_path,tmp_path)


def test_incomplete_match_cannot_be_full_core():
    r=original();f=finding(True);f['facts']={k:r[k] for k in v.CORE if k!='completed'};f['facts']['completed']=False
    with pytest.raises(ValueError,match='Full core'):v.assess(r,f,{'E':reference()})


def test_factual_dimensions_cannot_silently_assign_result_availability():
    f=finding();f['facts']={'result_availability':'2021-01-03'}
    with pytest.raises(ValueError,match='Unapproved factual dimension'):v.assess(original(),f,{'E':reference()})


def test_context_classification_tracks_actual_document_access():
    assert v.context_status([],{})=='UNRESOLVED'
    assert v.context_status(['E'],{'E':reference('INDEX_ONLY')})=='INDEX_LEAD_ONLY'
    assert v.context_status(['E'],{'E':reference()})=='PARTIAL_DIRECT_ENDPOINT'


def test_direct_endpoint_never_means_whole_round_verified():
    assert v.context_status(['E'],{'E':reference()})!='FULLY CORROBORATED CORE FACTS'
