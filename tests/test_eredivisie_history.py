"""Synthetic bounded Phase 3 acquisition/inventory checks; no private files/network."""
from copy import deepcopy
import hashlib,json
import pytest
from scripts import collect_eredivisie_history as a
from scripts import inventory_eredivisie_history as v
from scripts import validate_eredivisie_feasibility as f


def source(body='A v B  1-0',year=2024):
    raw=f'= Netherlands Eredivisie {year}/{(year+1)%100:02}\n▪ Matchday 1\nFri Aug 9 2024\n{body}\n'.encode()
    receipt=dict(path='source.txt',sha256=a.c.sha(raw),commit='pin',git_blob_sha1='blob',url='https://example.org/source',season='2024/2025')
    rows,notes=f.parse_text(raw,year,receipt)
    return dict(receipt=receipt,records=rows,assessment=f.assess(rows,year),notes=notes),raw


def test_exact_three_plan():
    assert [x['original_path'] for x in a.plan()]==['netherlands/2020-21_nl1.txt','netherlands/2021-22_nl1.txt','netherlands/2022-23_nl1.txt']
    assert len({x['path'] for x in a.plan()})==3 and all(x['commit']=='63df627f3c87ce71708f016522ea236cf74332c3' for x in a.plan())


def setup_acquisition(tmp_path,monkeypatch):
    raw=b'immutable original\n';blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest();tree={x['original_path']:dict(sha=blob,size=len(raw)) for x in a.plan()}
    monkeypatch.setattr(a,'protect',lambda *x:dict(synthetic=True));monkeypatch.setattr(a,'entries',lambda *x:tree);monkeypatch.setattr(a,'verify_originals',lambda *x:None);monkeypatch.setattr(a.time,'sleep',lambda *x:None)
    calls=[];monkeypatch.setattr(a.c,'request',lambda url,d:(calls.append(url),raw)[1]);return raw,calls


def test_three_downloads_and_zero_request_reuse(tmp_path,monkeypatch):
    raw,calls=setup_acquisition(tmp_path,monkeypatch);manifest=a.collect(tmp_path,tmp_path);assert len(calls)==3 and len(manifest['files'])==3
    before={str(x):x.read_bytes() for x in tmp_path.rglob('*') if x.is_file()};monkeypatch.setattr(a.c,'request',lambda *x:pytest.fail('Cached acquisition requested network'))
    assert a.collect(tmp_path,tmp_path)==manifest
    assert before=={str(x):x.read_bytes() for x in tmp_path.rglob('*') if x.is_file()}


@pytest.mark.parametrize('field,value',[('sha256','bad'),('bytes',0),('commit','bad'),('git_blob_sha1','bad'),('season','2025/2026'),('url','https://wrong'),('licensing','CLEARED')])
def test_cached_receipt_tamper(tmp_path,monkeypatch,field,value):
    setup_acquisition(tmp_path,monkeypatch);m=a.collect(tmp_path,tmp_path);p=tmp_path/m['files'][0]['path'];rec=p.with_name(p.name+'.provenance.json');r=json.loads(rec.read_text());r[field]=value;rec.write_text(json.dumps(r))
    with pytest.raises(ValueError):a.collect(tmp_path,tmp_path)


@pytest.mark.parametrize('missing',['original','receipt'])
def test_partial_cache_stops(tmp_path,monkeypatch,missing):
    setup_acquisition(tmp_path,monkeypatch);m=a.collect(tmp_path,tmp_path);p=tmp_path/m['files'][0]['path'];(p if missing=='original' else p.with_name(p.name+'.provenance.json')).unlink()
    with pytest.raises(ValueError):a.collect(tmp_path,tmp_path)


def test_identity_failure_before_source_save(tmp_path,monkeypatch):
    setup_acquisition(tmp_path,monkeypatch);monkeypatch.setattr(a.c,'request',lambda *x:b'wrong')
    with pytest.raises(ValueError):a.collect(tmp_path,tmp_path)
    assert not list(tmp_path.rglob('*_nl1.txt'))


def test_access_failure_stops_remaining(tmp_path,monkeypatch):
    _,calls=setup_acquisition(tmp_path,monkeypatch)
    def fail(url,d):calls.append(url);raise RuntimeError('access restricted')
    monkeypatch.setattr(a.c,'request',fail)
    with pytest.raises(RuntimeError):a.collect(tmp_path,tmp_path)
    assert len(calls)==1


def test_coverage_keeps_sources_separate():
    h,_=source();m=deepcopy(h);row=v.coverage_row(2024,{2024:h},{2024:m})
    assert row['coverage_status']=='BOTH_SOURCES' and row['historical']['observed']==row['modern']['observed']==1
    assert row['expected_regular_slots']==306


def test_absent_source_explicit():
    row=v.coverage_row(2025,{},{});assert row['coverage_status']=='NO_SOURCE' and row['historical'] is None and row['modern'] is None


def test_score_and_date_conflicts_not_resolved():
    h,_=source('NEC Nijmegen v Vitesse  1-3');m,_=source('NEC v SBV Vitesse  1-2');m['records'][0]['date']='2024-08-10';before=deepcopy((h,m));r=v.overlap_for_season(h['records'],m['records'])
    pair=r['conditional']['comparisons'][0];assert not pair['score_equal'] and not pair['date_equal'];assert (h,m)==before


def test_missing_pair_not_filled_or_selected():
    h,_=source('A v B  1-0\nB v A  0-0');m,_=source('A v B  1-0');r=v.overlap_for_season(h['records'],m['records'])
    assert len(r['conditional']['unmatched_historical_ids'])==1 and r['conditional']['comparison_pairs']==1


def test_cancelled_slot_distinct_from_absent():
    h,_=source();m,_=source('A v B  1-0\nB v A [cancelled]');r=v.overlap_for_season(h['records'],m['records'])
    assert len(r['conditional']['unmatched_modern_ids'])==1 and len(m['records'])==2
    assert m['records'][1]['FT'] is None


def test_review_queue_deduplicates_category_overlap():
    m,_=source('A v B  8-3 [awarded]');key=m['records'][0]['audit_id'];m['assessment']['wide_rounds']=[dict(fixture_ids=[key])]
    r=v.review_queue([], [m], [],dict(exceptions=[]));assert r['distinct_source_observations']==1 and set(r['records'][0]['categories'])=={'WIDE_ROUND','UNUSUAL_SCORE','SOURCE_ANNOTATION'}


def test_cross_source_queue_preserves_both_records():
    h,_=source('NEC Nijmegen v Vitesse  1-3');m,_=source('NEC v SBV Vitesse  1-2');o=v.overlap_for_season(h['records'],m['records']);q=v.review_queue([h],[m],[o],dict(exceptions=[]))
    assert q['distinct_source_observations']==2 and q['categories']=={'CROSS_SOURCE_SCORE_DISAGREEMENT':2}


def test_duplicate_source_id_is_error():
    m,_=source()
    with pytest.raises(ValueError):v.review_queue([m],[deepcopy(m)],[],dict(exceptions=[]))


def test_context_binding_must_match():
    m,_=source();r=deepcopy(m['records'][0]);r['FT']='9-9'
    with pytest.raises(ValueError):v.review_queue([], [m], [],dict(exceptions=[dict(source_observation=r)]))


def test_context_reference_cannot_be_unbound():
    m,_=source();ctx=dict(exceptions=[dict(original_comparison={'historical_id':'unknown','modern_id':'unknown'},kind='CONFLICT')])
    with pytest.raises(ValueError):v.review_queue([], [m], [],ctx)


def test_named_reserves_not_merged():
    m,_=source('Ajax v Jong Ajax  1-0\nPSV v Jong PSV  0-0');before=deepcopy(m);q=v.review_queue([], [m], [],dict(exceptions=[]))
    assert m==before and m['assessment']['reserve_labels']==['Jong Ajax','Jong PSV']


def test_independent_modern_raw_check(tmp_path):
    m,raw=source();(tmp_path/'source.txt').write_bytes(raw)
    hist_raw=b'Date,Season,home,visitor,FT,hgoal,vgoal,tier\n1990-08-24,1990,A,B,1-0,1,0,1\n';(tmp_path/'history.csv').write_bytes(hist_raw);rec=dict(path='history.csv',sha256=a.c.sha(hist_raw));rows=f.parse_csv(hist_raw,dict(rec,commit='pin',git_blob_sha1='blob',url='https://example.org'))
    h=dict(receipt=rec,total_records=1,samples=[dict(records=rows)]);out=v.independent_check(h,[m],dict(seasons=[f.assess(rows,1990)]),tmp_path);assert len(out['sources'])==2
    m['records'][0]['date']='2024-08-10'
    with pytest.raises(ValueError):v.independent_check(h,[m],dict(seasons=[f.assess(rows,1990)]),tmp_path)


def test_phase2_fingerprint_and_log_prefix(tmp_path,monkeypatch):
    directory=tmp_path/'private';directory.mkdir();frozen=tmp_path/'frozen';frozen.write_bytes(b'original');log=tmp_path/'PLANNING_LOG.md';log.write_bytes(b'log\n');monkeypatch.setattr(a.c,'protect',lambda *x:dict(private=1,public=1));(directory/a.BASELINE).write_bytes(a.c.encode(dict(files={'frozen':a.c.sha(b'original')},planning_log=dict(bytes=4,sha256=a.c.sha(b'log\n')))))
    a.protect(directory,tmp_path);log.write_bytes(b'log\nappend\n');a.protect(directory,tmp_path);frozen.write_bytes(b'changed')
    with pytest.raises(ValueError):a.protect(directory,tmp_path)


def test_planning_rewrite_rejected(tmp_path,monkeypatch):
    directory=tmp_path/'private';directory.mkdir();f=tmp_path/'frozen';f.write_bytes(b'original');(tmp_path/'PLANNING_LOG.md').write_bytes(b'bad\n');monkeypatch.setattr(a.c,'protect',lambda *x:None);(directory/a.BASELINE).write_bytes(a.c.encode(dict(files={'frozen':a.c.sha(b'original')},planning_log=dict(bytes=4,sha256=a.c.sha(b'log\n')))))
    with pytest.raises(ValueError):a.protect(directory,tmp_path)
