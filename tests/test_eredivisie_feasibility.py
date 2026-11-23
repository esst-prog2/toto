"""Synthetic bounded acquisition, parsing and diagnostic tests; no network/private data."""
from copy import deepcopy
import csv,io,json,hashlib
import pytest
from scripts import collect_eredivisie_feasibility as c
from scripts import validate_eredivisie_feasibility as v
from scripts import verify_eredivisie_feasibility as independent


def receipt(raw=b'',path='synthetic.txt'):
    return dict(path=path,sha256=c.sha(raw),commit='revision',git_blob_sha1='blob',url='https://example.org/original')


def text(body='A v B  2-1 (1-0)',year=2024,day='Fri Aug 9 2024'):
    return f'= Netherlands Eredivisie {year}/{(year+1)%100:02}\n▪ Matchday 1\n{day}\n{body}\n'.encode()


def parse(body='A v B  2-1 (1-0)'):
    raw=text(body);return v.parse_text(raw,2024,receipt(raw))[0]


def historical(rows=None):
    f=io.StringIO(newline='');w=csv.writer(f);w.writerow(v.CSV_COLUMNS);w.writerows(rows or [['1990-08-24','1990','SVV Schiedam','FC Den Haag','1-0','1','0','1']]);return f.getvalue().encode()


def test_exact_six_paths_and_pins():
    items=c.plan();assert len(items)==6 and len({x['path'] for x in items})==6
    assert items[0]['original_path']=='data-raw/holland.csv'
    assert [r['season'] for r in items[1:]]==['2018/2019','2019/2020','2023/2024','2024/2025','2025/2026']
    assert all(x['commit']==c.PINS[x['repository']] for x in items)


def test_csv_literal_types_dates_names():
    raw=historical();r=v.parse_csv(raw,receipt(raw))[0]
    assert r['season']=='1990/1991' and r['original_fields']['Season']=='1990'
    assert r['home']=='SVV Schiedam' and r['away']=='FC Den Haag'
    assert r['source_line']==r['source_end_line']==2
    assert r['physical_record_sha256']==c.sha(raw.splitlines(keepends=True)[1])


@pytest.mark.parametrize('index,value',[(0,'24/08/1990'),(1,'1990/91'),(4,'0-3'),(5,''),(5,'-1'),(5,'1.0'),(7,'2')])
def test_bad_historical_fields_fail(index,value):
    cells=['1990-08-24','1990','A','B','1-0','1','0','1'];cells[index]=value;raw=historical([cells])
    with pytest.raises(ValueError):v.parse_csv(raw,receipt(raw))


def test_historical_schema_failure():
    raw=b'Date,Season\n1990-08-24,1990\n'
    with pytest.raises(ValueError):v.parse_csv(raw,receipt(raw))


@pytest.mark.parametrize('body,ft,note',[('A v B  2-1','2-1',''),('A v B [cancelled]',None,'[cancelled]'),('A v B',None,''),('A v B  0-3 [awarded]','0-3','[awarded]'),('Ajax v Jong Ajax  1-0','1-0','')])
def test_source_scores_and_annotations(body,ft,note):
    r=parse(body)[0];assert r['FT']==ft and r['annotation']==note


@pytest.mark.parametrize('change',[lambda b:b.replace(b'Netherlands Eredivisie',b'French Ligue 1'),lambda b:b.replace(b'Fri Aug 9 2024',b'Thu Aug 9 2024'),lambda b:b.replace(b'2-1 (1-0)',b'2-?'),lambda b:b.replace(b'Matchday 1',b'Matchday 35'),lambda b:b.replace(b'Fri Aug 9 2024\n',b''),lambda b:b+b'unknown\n'])
def test_invalid_text_fails(change):
    raw=change(text())
    with pytest.raises(ValueError):v.parse_text(raw,2024,receipt(raw))


def test_repeated_round_is_preserved_not_duplicate_fixture():
    raw=text()+b'\xe2\x96\xaa Matchday 1\nSat Aug 10\nC v D  0-0\n';rs,notes=v.parse_text(raw,2024,receipt(raw))
    assert len(rs)==2 and notes['repeated_round_headings']=={'1':2}


def test_extra_stage_separate():
    raw=text()+b'\xe2\x96\xaa Playoff Final\nSat Aug 10\nC v D  1-0\n';rs,_=v.parse_text(raw,2024,receipt(raw));assert rs[1]['stage']=='OTHER_STAGE'


def test_cancelled_not_missing_source():
    rows=parse('A v B [cancelled]\nC v D');a=v.assess(rows,2024)
    assert a['observed']==2 and a['explicitly_cancelled']==1 and a['unexplained_unscored']==1
    assert len(a['missing_pairings'])==10


@pytest.mark.parametrize('year,n',[(1962,16),(1965,16),(1966,18),(1990,18),(2025,18)])
def test_format_expectation_not_forced(year,n):
    r=parse()[0];r.update(season=f'{year}/{year+1}',date=f'{year}-08-09');a=v.assess([r],year)
    assert a['expected_slots']==n*(n-1) and a['observed']==1


def test_duplicate_conflicting_pair_is_visible():
    rows=parse('A v B  1-0\nA v B  0-3');a=v.assess(rows,2024);assert a['duplicate_pairings'][0]['conflicting']


def test_cancellation_with_score_is_not_accepted_silently():
    rows=parse('A v B  1-0 [cancelled]');assert v.assess(rows,2024)['invalid'][0]['reason']=='CANCELLED_WITH_SCORE'


def test_wide_span_and_order_not_corrections():
    raw=text()+b'Sat Aug 31\nC v D  0-0\nSat Aug 10\nE v F  2-0\n';rs,_=v.parse_text(raw,2024,receipt(raw));before=deepcopy(rs);a=v.assess(rs,2024)
    assert len(a['wide_rounds'])==1 and len(a['source_order_reversals'])==1 and rs==before


def test_no_identity_merger_or_reserve_stripping():
    rows=parse('Ajax v Jong Ajax  1-0\nPSV v Jong PSV  0-0');a=v.assess(rows,2024)
    assert a['reserve_labels']==['Jong Ajax','Jong PSV'] and len(a['team_labels'])==4


def test_alias_comparison_conditional_and_preserves_conflict():
    a=parse('NEC Nijmegen v Vitesse  1-3');b=parse('NEC v SBV Vitesse  1-2');before=deepcopy((a,b));exact=v.overlap(a,b);conditional=v.identity_overlap(a,b)
    assert exact['exact_label_pair_matches']==0 and conditional['comparison_pairs']==1
    assert conditional['comparisons'][0]['score_equal'] is False and (a,b)==before
    assert all(x['status']=='DIAGNOSTIC_ONLY_NOT_APPROVED_ALIAS' for x in conditional['hypothesized_label_correspondences'])


def test_actual_date_difference_retained():
    a=parse();b=deepcopy(a);b[0]['date']='2024-08-10';result=v.overlap(a,b);assert not result['comparisons'][0]['date_equal']


def acquisition_setup(tmp_path,monkeypatch):
    raw=b'bounded synthetic original\n';blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest();trees={repo:{x['original_path']:dict(sha=blob,size=len(raw)) for x in c.plan() if x['repository']==repo} for repo in c.PINS}
    monkeypatch.setattr(c,'protect',lambda *a:dict(private=1,public=1));monkeypatch.setattr(c,'metadata',lambda *a:trees);monkeypatch.setattr(c.time,'sleep',lambda *a:None)
    calls=[];monkeypatch.setattr(c,'request',lambda u,d:(calls.append(u),raw)[1]);return raw,trees,calls


def test_cache_zero_requests_and_no_bytes_change(tmp_path,monkeypatch):
    raw,trees,calls=acquisition_setup(tmp_path,monkeypatch);m=c.collect(tmp_path,tmp_path);assert len(calls)==6
    before={str(x):x.read_bytes() for x in tmp_path.rglob('*') if x.is_file()}
    monkeypatch.setattr(c,'request',lambda *a:pytest.fail('Unexpected network'));assert c.collect(tmp_path,tmp_path)==m
    assert before=={str(x):x.read_bytes() for x in tmp_path.rglob('*') if x.is_file()}


@pytest.mark.parametrize('field,value',[('sha256','bad'),('bytes',1),('commit','bad'),('url','https://wrong'),('git_blob_sha1','bad'),('licensing','CLEARED')])
def test_cached_receipt_tamper_rejected(tmp_path,monkeypatch,field,value):
    acquisition_setup(tmp_path,monkeypatch);m=c.collect(tmp_path,tmp_path);p=tmp_path/m['files'][0]['path'];rec=p.with_name(p.name+'.provenance.json');r=json.loads(rec.read_text());r[field]=value;rec.write_text(json.dumps(r))
    with pytest.raises(ValueError):c.collect(tmp_path,tmp_path)


def test_blob_failure_before_source_save(tmp_path,monkeypatch):
    acquisition_setup(tmp_path,monkeypatch);monkeypatch.setattr(c,'request',lambda *a:b'wrong')
    with pytest.raises(ValueError):c.collect(tmp_path,tmp_path)
    assert not list(tmp_path.rglob('holland.csv'))


def test_partial_cache_fails(tmp_path,monkeypatch):
    acquisition_setup(tmp_path,monkeypatch);m=c.collect(tmp_path,tmp_path);p=tmp_path/m['files'][0]['path'];p.unlink()
    with pytest.raises(ValueError):c.collect(tmp_path,tmp_path)


def test_access_stop_before_request(tmp_path,monkeypatch):
    (tmp_path/'ACCESS_STOP.json').write_text('{}');monkeypatch.setattr(c,'build_opener',lambda *a:pytest.fail('Must not access network'))
    with pytest.raises(RuntimeError):c.request('https://example.org',tmp_path)


def test_tree_revision_and_truncation():
    for tree in [{'sha':'wrong','tree':[]},{'sha':'pin','truncated':True,'tree':[]}]:
        with pytest.raises(ValueError):c.base.tree_entries(c.encode(tree),'pin',['approved'])


def test_previous_bytes_protected(tmp_path):
    directory=tmp_path/'private';directory.mkdir();f=tmp_path/'previous';f.write_bytes(b'original');log=tmp_path/'PLANNING_LOG.md';log.write_bytes(b'log\n');d=c.sha(b'original')
    (directory/'protected_before.json').write_bytes(c.encode(dict(private={'previous':d},public={'previous':d},planning_log=dict(bytes=4,sha256=c.sha(b'log\n')))))
    c.protect(directory,tmp_path);f.write_bytes(b'changed')
    with pytest.raises(ValueError):c.protect(directory,tmp_path)


def test_independent_csv_reconciliation_and_tamper(tmp_path):
    raw=historical();rec=receipt(raw,'historical.csv');(tmp_path/'historical.csv').write_bytes(raw);rows=v.parse_csv(raw,rec)
    saved=dict(historical=dict(receipt=rec,total_records=1,samples=[dict(records=rows)]),modern=[])
    (tmp_path/'feasibility_assessment.json').write_bytes(c.encode(saved));(tmp_path/'coverage_inventory.json').write_bytes(c.encode(dict(seasons=[v.assess(rows,1990)])))
    assert independent.reconcile(tmp_path)['sources'][0]['exact']
    saved['historical']['samples'][0]['records'][0]['home']='Changed';(tmp_path/'feasibility_assessment.json').write_bytes(c.encode(saved))
    with pytest.raises(ValueError):independent.reconcile(tmp_path)
