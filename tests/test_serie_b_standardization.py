"""Synthetic guards for the modern Serie B derivative; no private data required."""
from copy import deepcopy
import hashlib
import json
import sys

import pytest

from scripts import standardize_serie_b_results as s


def fixture(tmp_path):
    path=tmp_path/'synthetic.csv'
    lines=['Div,Date,HomeTeam,AwayTeam,FTHG,FTAG,FTR']+[
        f'I2,{i+1:02}/09/00,Home {i},Away {i},1,0,H' for i in range(6)]
    path.write_text('\n'.join(lines)+'\n')
    sha=hashlib.sha256(path.read_bytes()).hexdigest()
    raw=[dict(source_line=i+2,date=f'2000-09-{i+1:02}',home=f'Home {i}',away=f'Away {i}',hg=1,ag=0) for i in range(6)]
    details=[dict(file=path.name,season='2000/2001',records=raw)]
    records=[dict(source_file=path.name,source_line=r['source_line'],season='2000/2001',date=r['date'],home_team=r['home'],away_team=r['away'],home_goals=1,away_goals=0) for r in raw]
    bindings=[dict(file=path.name,line=i+2,raw_line=lines[i+1],sha256=sha) for i in range(6)]
    cases=[dict(id=f'E{i+1}',source=bindings[i],original={k:r[k] for k in ('date','home','away','hg','ag')},training_suitability='UNRESOLVED' if i in (0,4) else 'EXCLUDED') for i,r in enumerate(raw[:5])]
    return records,details,bindings,dict(regular_cases=cases,unlisted_training_suitability='UNRESOLVED')


def test_partition_physically_omits_all_five_cases_and_preserves_archive(tmp_path):
    records,details,_,policy=fixture(tmp_path)
    before=deepcopy(records);_,standard,_=s.convert(records,tmp_path)
    accepted,cases=s.partition(standard,records,policy,tmp_path,details)
    assert len(accepted)==1 and accepted[0]['home_team']=='Home 5'
    assert len(standard)==6 and records==before
    assert not {c['match_id'] for c in cases}&{r['match_id'] for r in accepted}
    assert sum(c['training_suitability']=='UNRESOLVED' for c in cases)==2


@pytest.mark.parametrize('change',['missing','swapped','duplicate','source','facts','default'])
def test_partition_fails_closed(tmp_path,change):
    records,details,_,policy=fixture(tmp_path);_,standard,_=s.convert(records,tmp_path)
    if change=='missing':policy['regular_cases'].pop()
    if change=='swapped':
        a,b=policy['regular_cases'][:2];a['training_suitability'],b['training_suitability']=b['training_suitability'],a['training_suitability']
    if change=='duplicate':policy['regular_cases'][1]['source']=deepcopy(policy['regular_cases'][0]['source'])
    if change=='source':policy['regular_cases'][0]['source']['sha256']='0'*64
    if change=='facts':policy['regular_cases'][0]['original']['hg']=9
    if change=='default':policy['unlisted_training_suitability']='ELIGIBLE'
    with pytest.raises(ValueError):s.partition(standard,records,policy,tmp_path,details)


def correction(records,bindings):
    r=records[0]
    return dict(id='SYNTHETIC',source=bindings[0],original=dict(date=r['date'],home=r['home_team'],away=r['away_team'],hg=1,ag=0),
                evidence_ids=['SYNTHETIC'],status='VERIFIED_PENDING_STANDARDIZATION',applied=False,replacements={'date':'2000-09-10'})


def test_date_correction_is_bound_derived_only_and_changes_id(tmp_path):
    records,details,bindings,_=fixture(tmp_path);c=correction(records,bindings)
    raw=(tmp_path/'synthetic.csv').read_bytes();original=deepcopy(records)
    changed,applied=s.apply_dates(records,[c],tmp_path,details)
    assert changed==[dict(records[0],date='2000-09-10'),*records[1:]]
    assert records==original and (tmp_path/'synthetic.csv').read_bytes()==raw
    assert applied[0]['applied'] and c['applied'] is False
    assert s.standard_id(changed[0])!=s.standard_id(records[0])
    assert s.standard_id(dict(records[0],home_goals=9))==s.standard_id(records[0])


@pytest.mark.parametrize('change',['score','hash','facts','duplicate','missing','unverified','evidence','noncanonical','season'])
def test_date_correction_guards(tmp_path,change):
    records,details,bindings,_=fixture(tmp_path);c=correction(records,bindings);cs=[c]
    if change=='score':c['replacements']['hg']=9
    if change=='hash':c['source']['sha256']='0'*64
    if change=='facts':records[0]['home_goals']=3
    if change=='duplicate':cs.append(deepcopy(c))
    if change=='missing':records=records[1:]
    if change=='unverified':c['status']='PENDING'
    if change=='evidence':c['evidence_ids']=[]
    if change=='noncanonical':c['replacements']['date']='20000910'
    if change=='season':c['replacements']['date']='2002-09-10'
    with pytest.raises(ValueError):s.apply_dates(records,cs,tmp_path,details)


def test_shared_conversion_reordering_schema_ids_and_invalid_records(tmp_path):
    records,_,_,_=fixture(tmp_path)
    content,standard,summary=s.convert(records,tmp_path)
    assert s.convert(list(reversed(records)),tmp_path)[0]==content
    assert content.decode().splitlines()[0].split(',')==list(s.OUTPUT_COLUMNS)
    assert summary['accepted']==6
    assert all(r['match_id']==s.standard_id(r) for r in standard)
    for bad in [dict(records[0],home_goals=-1),dict(records[0],home_team=''),dict(records[0],date='2000-02-30'),dict(records[0],season='1996/1997')]:
        with pytest.raises(ValueError):s.convert([bad],tmp_path)
    with pytest.raises(ValueError):s.convert(records+[records[0]],tmp_path)


def test_existing_output_refused_and_check_never_replaces(tmp_path,monkeypatch):
    monkeypatch.setattr(s,'PRIVATE',tmp_path);p=tmp_path/s.OUTPUT_NAMES[0];p.write_bytes(b'old')
    monkeypatch.setattr(sys,'argv',['converter'])
    monkeypatch.setattr(s,'build',lambda:(_ for _ in ()).throw(AssertionError('must not build')))
    with pytest.raises(FileExistsError):s.main()
    monkeypatch.setattr(sys,'argv',['converter','--check']);monkeypatch.setattr(s,'build',lambda:{p.name:b'new'})
    with pytest.raises(ValueError):s.main()
    assert p.read_bytes()==b'old'
