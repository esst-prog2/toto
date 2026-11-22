"""Synthetic Phase 3 acquisition/inventory checks; no private sources/network."""
import hashlib
import json
from copy import deepcopy
import pytest
from scripts import collect_ligue2_history as c
from scripts import inventory_ligue2_history as inventory
from scripts import validate_ligue2_feasibility as v


def source(body='A v B  1-0',year=2024):
    raw=f'= French Ligue 2 {year}/{str(year+1)[-2:]}\n▪ Matchday 1\nFri Aug 16 2024\n{body}\n'.encode()
    rows,notes=v.parse_text(raw,year)
    for r in rows:r.update(audit_id=str(r['source_line']),source='source.txt',source_sha256='digest')
    return dict(records=rows,notes=notes,assessment=v.assess(rows,year))


def test_exact_six_plan_and_pin():
    p=c.plan();assert [r['original_path'] for r in p]==[f'france/{x}_fr2.txt' for x in ['2015-16','2016-17','2018-19','2020-21','2021-22','2023-24']]
    assert len(p)==6 and len({r['path'] for r in p})==6
    assert all(r['commit']=='63df627f3c87ce71708f016522ea236cf74332c3' for r in p)
    assert all('/2025-26_' not in r['url'] for r in p)


def acquisition_fixture(tmp_path,monkeypatch):
    raw=b'immutable synthetic original\n';blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    tree={x['original_path']:dict(sha=blob,size=len(raw)) for x in c.plan()}
    monkeypatch.setattr(c,'protect',lambda *a:dict(synthetic=True))
    monkeypatch.setattr(c,'entries',lambda *a:tree)
    monkeypatch.setattr(c,'verify_originals',lambda *a:None)
    monkeypatch.setattr(c.time,'sleep',lambda *a:None)
    calls=[]
    monkeypatch.setattr(c.base,'request',lambda url,d:(calls.append(url),raw)[1])
    return raw,calls


def test_acquisition_exact_and_cached_immutable(tmp_path,monkeypatch):
    raw,calls=acquisition_fixture(tmp_path,monkeypatch);m=c.collect(tmp_path,tmp_path)
    assert len(calls)==6 and len(m['files'])==6
    before={str(p):p.read_bytes() for p in tmp_path.rglob('*') if p.is_file()}
    monkeypatch.setattr(c.base,'request',lambda *a:pytest.fail('Cached reuse requested network'))
    assert c.collect(tmp_path,tmp_path)==m
    assert before=={str(p):p.read_bytes() for p in tmp_path.rglob('*') if p.is_file()}
    assert all((tmp_path/x['path']).read_bytes()==raw for x in c.plan())


@pytest.mark.parametrize('field,value',[('sha256','wrong'),('bytes',0),('commit','wrong'),('git_blob_sha1','wrong'),('url','https://wrong'),('season','2025/2026'),('licensing','CLEARED')])
def test_cached_receipt_tamper_rejected(tmp_path,monkeypatch,field,value):
    acquisition_fixture(tmp_path,monkeypatch);m=c.collect(tmp_path,tmp_path);p=tmp_path/m['files'][0]['path'];rec=p.with_name(p.name+'.provenance.json')
    r=json.loads(rec.read_text());r[field]=value;rec.write_text(json.dumps(r))
    with pytest.raises(ValueError):c.collect(tmp_path,tmp_path)


@pytest.mark.parametrize('missing',['original','receipt'])
def test_partial_original_pair_rejected(tmp_path,monkeypatch,missing):
    acquisition_fixture(tmp_path,monkeypatch);m=c.collect(tmp_path,tmp_path);p=tmp_path/m['files'][0]['path']
    (p if missing=='original' else p.with_name(p.name+'.provenance.json')).unlink()
    with pytest.raises(ValueError):c.collect(tmp_path,tmp_path)


def test_blob_mismatch_blocks_save(tmp_path,monkeypatch):
    acquisition_fixture(tmp_path,monkeypatch);monkeypatch.setattr(c.base,'request',lambda *a:b'wrong')
    with pytest.raises(ValueError):c.collect(tmp_path,tmp_path)
    assert not list(tmp_path.rglob('*_fr2.txt'))


def test_retrieval_failure_stops_remaining(tmp_path,monkeypatch):
    _,calls=acquisition_fixture(tmp_path,monkeypatch)
    def fail(url,d):calls.append(url);raise RuntimeError('access restriction')
    monkeypatch.setattr(c.base,'request',fail)
    with pytest.raises(RuntimeError):c.collect(tmp_path,tmp_path)
    assert len(calls)==1


def test_counts_measured_not_forced():
    s=source();result=inventory.summarize([s]);assert result['totals']['observed']==1 and result['totals']['expected']==306
    assert result['totals']['scored']==1 and result['totals']['unscored']==0


def test_cancelled_and_unexplained_distinct():
    s=source('A v B [cancelled]\nC v D');r=inventory.summarize([s]);assert r['totals']['unscored']==2
    assert r['review_category_members']=={'SOURCE_CANCELLED':1,'UNSCORED_UNEXPLAINED':1}


def test_review_overlap_deduplicated():
    s=source('A v B  8-3 [awarded]');row=s['records'][0];s['assessment']['wide_rounds']=[dict(fixtures=[dict(source_line=row['source_line'])])]
    r=inventory.summarize([s]);assert r['deduplicated_review_candidates']==1
    assert set(r['review_candidates'][0]['categories'])=={'WIDE_ROUND','SOURCE_ANNOTATION','UNUSUAL_SCORE'}
    assert row['FT']=='8-3'


def test_duplicate_line_binding_rejected():
    s=source();s['records'].append(deepcopy(s['records'][0]))
    with pytest.raises(ValueError):inventory.summarize([s])


def test_ajaccio_clubs_not_merged():
    s=source('AC Ajaccio v Gazélec FC Ajaccio  1-0');r=inventory.summarize([s])
    assert s['assessment']['team_names']==['AC Ajaccio','Gazélec FC Ajaccio'];assert r['literal_label_changes']==[]


def test_independent_check_detects_changed_score(tmp_path):
    s=source();s['receipt']=dict(repository=c.REPO,path='source.txt',season='2024/2025')
    raw=b'= French Ligue 2 2024/25\n\xe2\x96\xaa Matchday 1\nFri Aug 16 2024\nA v B  1-0\n';(tmp_path/'source.txt').write_bytes(raw);s['receipt']['sha256']=c.base.sha(raw)
    inventory.independent_check([s],tmp_path)
    s['records'][0]['hg']='9'
    with pytest.raises(ValueError):inventory.independent_check([s],tmp_path)


def test_frozen_phase2_change_rejected(tmp_path,monkeypatch):
    d=tmp_path/'private';d.mkdir();f=tmp_path/'frozen';f.write_bytes(b'original');log=tmp_path/'PLANNING_LOG.md';log.write_bytes(b'log\n')
    monkeypatch.setattr(c.base,'protect',lambda *a:dict(private=1,public=1))
    frozen=dict(files={'frozen':c.base.sha(b'original')},planning_log=dict(bytes=4,sha256=c.base.sha(b'log\n')))
    (d/c.BASELINE).write_bytes(c.base.encode(frozen));assert c.protect(d,tmp_path)['phase2_protected_entries']==1
    log.write_bytes(b'log\nappend\n');c.protect(d,tmp_path)
    f.write_bytes(b'changed')
    with pytest.raises(ValueError):c.protect(d,tmp_path)


def test_planning_rewrite_rejected(tmp_path,monkeypatch):
    d=tmp_path/'private';d.mkdir();f=tmp_path/'frozen';f.write_bytes(b'original');log=tmp_path/'PLANNING_LOG.md';log.write_bytes(b'bad\n')
    monkeypatch.setattr(c.base,'protect',lambda *a:None)
    (d/c.BASELINE).write_bytes(c.base.encode(dict(files={'frozen':c.base.sha(b'original')},planning_log=dict(bytes=4,sha256=c.base.sha(b'log\n')))))
    with pytest.raises(ValueError):c.protect(d,tmp_path)
