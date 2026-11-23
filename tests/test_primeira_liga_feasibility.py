"""Synthetic Portugal Phase 2 checks; no network or private data dependency."""
from copy import deepcopy
import csv,io,json
from pathlib import Path
import pytest
from scripts import collect_primeira_liga_feasibility as c
from scripts import validate_primeira_liga_feasibility as v


def receipt(raw,path='synthetic'):
    return dict(path=path,sha256=c.sha(raw),commit='test',git_blob_sha1='testblob',url='https://example.invalid/original',encoding='utf-8-sig')


def text(body='A v B  2-1 (1-0)',year=2024,day='Fri Aug 9 2024'):
    return f'= Portuguese Primeira Liga {year}/{(year+1)%100:02}\n▪ Matchday 1\n{day}\n{body}\n'.encode()


def parse(body='A v B  2-1 (1-0)',year=2024,day='Fri Aug 9 2024'):
    raw=text(body,year,day);return v.parse_text(raw,year,receipt(raw))[0]


def historical(cells=None):
    f=io.StringIO(newline='');w=csv.writer(f);w.writerow(v.CSV_COLUMNS);w.writerow(cells or ['1994-08-20','1994','Farense','Sp Lisbon','0-2','0','2','P1','1','2','-2','A']);return f.getvalue().encode()


def test_exact_approved_scope():
    p=c.plan();assert len(p)==7 and len({x['url'] for x in p})==7
    assert [x['season'] for x in p[1:6]]==['2018/2019','2019/2020','2021/2022','2024/2025','2025/2026']
    assert p[0]['expected_bytes']==592748 and p[0]['expected_blob']=='ffb6afe2e6fd395269edd2cfe00e5de33a30dbc2'
    assert all('football-data' not in x['url'] and '_pt2' not in x['url'] and '_ptcup' not in x['url'] for x in p)
    assert p[-1]['commit'] is None and p[-1]['expected_blob'] is None


def test_historical_exact_original_fields_and_binding():
    raw=historical();r=v.parse_csv(raw,receipt(raw))[0]
    assert r['season']=='1994/1995' and r['original_fields']['division']=='P1' and not r['field_issues']
    assert r['source_line']==2 and r['physical_record_sha256']==c.sha(raw.splitlines(keepends=True)[1])
    assert 'match_id' not in r


@pytest.mark.parametrize('index,value,issue',[(4,'2-0','FT_CONTRADICTION'),(5,'','INVALID_SCORE'),(5,'-1','INVALID_SCORE'),(5,'1.0','INVALID_SCORE'),(7,'P2','WRONG_COMPETITION'),(8,'2','WRONG_COMPETITION'),(9,'4','GOAL_DERIVED_CONTRADICTION'),(10,'2','GOAL_DERIVED_CONTRADICTION'),(11,'H','OUTCOME_CONTRADICTION'),(0,'20/08/1994','INVALID_DATE')])
def test_historical_contradictions_reported_not_corrected(index,value,issue):
    cells=['1994-08-20','1994','A','B','0-2','0','2','P1','1','2','-2','A'];cells[index]=value;raw=historical(cells);r=v.parse_csv(raw,receipt(raw))[0]
    assert issue in r['field_issues'] and r['original_fields'][v.CSV_COLUMNS[index]]==value


@pytest.mark.parametrize('year,clubs',[(1990,20),(1991,18),(1994,18),(2005,18),(2006,16),(2013,16),(2014,18),(2025,18)])
def test_format_not_forced(year,clubs):
    rows=parse();rows[0].update(date=f'{year}-08-09',season=f'{year}/{year+1}');a=v.assess(rows,year)
    assert a['expected_clubs']==clubs and a['expected_slots']==clubs*(clubs-1) and a['observed']==1


@pytest.mark.parametrize('body,ft,note',[('A v B  0-7 (0-7)','0-7',''),('A v B',None,''),('A v B [cancelled]',None,'[cancelled]'),('A v B  0-3 [awarded]','0-3','[awarded]')])
def test_scores_annotations_not_final_policy(body,ft,note):
    r=parse(body)[0];assert r['FT']==ft and r['annotation']==note and 'disposition' not in r


def test_covid_july_date_allowed_only_for_extended_season():
    r=parse(year=2019,day='Sun Jul 26 2020')[0];assert r['date']=='2020-07-26' and not v.assess([r],2019)['invalid']
    with pytest.raises(ValueError):parse(year=2018,day='Fri Jul 26 2019')


@pytest.mark.parametrize('change',[lambda b:b.replace(b'Portuguese Primeira Liga',b'Portuguese Segunda Liga'),lambda b:b.replace(b'Fri Aug 9 2024',b'Thu Aug 9 2024'),lambda b:b.replace(b'2-1 (1-0)',b'2-?'),lambda b:b.replace(b'Matchday 1',b'Matchday 35'),lambda b:b.replace(b'Fri Aug 9 2024\n',b''),lambda b:b+b'unknown\n'])
def test_unknown_source_grammar_fails(change):
    raw=change(text())
    with pytest.raises(ValueError):v.parse_text(raw,2024,receipt(raw))


def test_duplicate_conflicting_pair_preserved():
    a=v.assess(parse('A v B  1-0\nA v B  0-3'),2024)
    assert a['observed']==2 and a['duplicate_pairings'][0]['conflicting']


def test_senior_reserve_and_vitorias_not_merged():
    a=v.assess(parse('Benfica v Benfica B  2-0\nVitória SC v Vitória FC  1-1'),2024)
    assert a['clubs']==4 and a['reserve_labels']==['Benfica B']


def test_whitespace_label_preserved_and_flagged():
    rs=parse();rs[0]['home']='Feirense ';a=v.assess(rs,2011)
    assert a['invalid'][0]['reason']=='INVALID_TEAM' and rs[0]['home']=='Feirense '


def test_season_bound_diagnostic_is_not_global_alias():
    h=parse('Belenenses v Benfica  0-7');m=parse('Belenenses SAD v SL Benfica  0-7');o=v.identity_overlap(h,m)
    assert o['comparison_pairs']==1 and h[0]['home']=='Belenenses' and o['mapping'][0]['status'].startswith('DIAGNOSTIC')
    m[0]['season']='2023/2024'
    with pytest.raises(ValueError):v.identity_overlap(h,m)


def test_overlap_preserves_conflicting_date_score():
    h=parse('Benfica v Porto  2-1');m=parse('SL Benfica v FC Porto  1-1');m[0]['date']='2024-08-10';o=v.identity_overlap(h,m)
    assert not o['comparisons'][0]['date_equal'] and not o['comparisons'][0]['score_equal']


def test_duplicate_overlap_rejected():
    h=parse('Benfica v Porto  2-1');m=parse('SL Benfica v FC Porto  2-1\nSL Benfica v FC Porto  2-1')
    with pytest.raises(ValueError):v.identity_overlap(h,m)


def rsssf():
    rows=[]
    for i in range(20):rows.append(f'{i+1} Club {i+1}  '+' '.join('X' if i==j else '1-0' for j in range(20)))
    return ('Final Table\nCross Table\n'+'\n'.join(rows)+'\nAccumulated Table\nAbout this document\nCopyright; acknowledgement required').encode()


def test_rsssf_results_do_not_invent_dates_or_finality():
    raw=rsssf();r=v.rsssf_capabilities(raw,receipt(raw));assert r['reconstructable_scores']==380 and r['dated_fixtures']==0
    assert all(x['date'] is None and x['historical_legal_finality']=='NOT_ESTABLISHED' for x in r['fixtures'])


def test_bad_rsssf_geometry_fails():
    raw=rsssf().replace(b'1-0',b'?',1)
    with pytest.raises(ValueError):v.rsssf_capabilities(raw,receipt(raw))


def test_atomic_exclusive_save_never_overwrites(tmp_path):
    p=tmp_path/'x';c.save(p,b'original')
    with pytest.raises(FileExistsError):c.save(p,b'changed')
    assert p.read_bytes()==b'original' and not list(tmp_path.glob('.pending-*'))


def test_keep_detects_corruption(tmp_path):
    p=tmp_path/'x';c.keep(p,b'a');c.keep(p,b'a')
    with pytest.raises(ValueError):c.keep(p,b'b')


def test_blob_tampering_fails():
    with pytest.raises(ValueError):c.base.verify_blob(b'bad',{'sha':'0'*40,'size':3})


def test_unapproved_request_rejected_before_network(tmp_path,monkeypatch):
    monkeypatch.setattr(c,'build_opener',lambda *a:pytest.fail('Network forbidden'))
    with pytest.raises(ValueError):c.request({'url':'https://example.org/unapproved'},tmp_path)


def test_prior_access_stop_no_retry(tmp_path,monkeypatch):
    item=c.plan()[-1];p=tmp_path/'access'/f"{c.sha(item['url'].encode())}.STOP.json";c.save(p,c.encode({'error':'403'}))
    monkeypatch.setattr(c,'build_opener',lambda *a:pytest.fail('Network forbidden'))
    with pytest.raises(RuntimeError):c.request(item,tmp_path)


def test_receipt_mutation_detected(tmp_path):
    item=c.plan()[-1];raw=b'document';p=tmp_path/item['path'];c.save(p,raw)
    r=dict(item,sha256=c.sha(raw),bytes=len(raw),git_blob_sha1=None,retrieved_at_utc='test',attribution='RSSSF',licensing=c.RIGHTS['RSSSF']);assert c.verify_record(tmp_path,item,r)==raw
    r['git_blob_sha1']='invented'
    with pytest.raises(ValueError):c.verify_record(tmp_path,item,r)


def test_wide_round_is_diagnostic_not_exclusion():
    raw=text()+b'Fri Sep 6 2024\nC v D  1-0\n';rows,_=v.parse_text(raw,2024,receipt(raw));a=v.assess(rows,2024)
    assert len(a['wide_rounds'])==1 and a['wide_rounds'][0]['span_days']==28 and a['observed']==2
    assert not any('disposition' in r for r in rows)


def test_source_order_reversal_visible():
    raw=text()+b'Thu Aug 8 2024\nC v D  1-0\n';rs,_=v.parse_text(raw,2024,receipt(raw));assert len(v.assess(rs,2024)['source_order_reversals'])==1


def test_historical_checksum_guard():
    raw=historical();r=receipt(raw);r['sha256']='wrong'
    with pytest.raises(ValueError):v.parse_csv(raw,r)


def test_round_repeat_preserved():
    raw=text()+b'\xe2\x96\xaa Matchday 1\nSat Aug 10\nC v D  0-0\n';rows,notes=v.parse_text(raw,2024,receipt(raw));assert len(rows)==2 and notes['repeated_round_headings']=={'1':2}


def test_other_stage_is_separate():
    raw=text()+b'\xe2\x96\xaa Playoff Final\nSat Aug 10\nC v D  1-0\n';rs,_=v.parse_text(raw,2024,receipt(raw));assert rs[-1]['stage']=='OTHER_STAGE'


def test_partial_cache_fails_before_request(tmp_path,monkeypatch):
    monkeypatch.setattr(c,'protect',lambda *a:{'private':1,'public':1});monkeypatch.setattr(c,'metadata',lambda *a:{})
    p=tmp_path/c.plan()[0]['path'];c.save(p,b'partial');monkeypatch.setattr(c,'request',lambda *a:pytest.fail('No network on partial cache'))
    with pytest.raises(ValueError,match='Partial original'):c.collect(tmp_path,tmp_path)


def test_restricted_source_cached_without_retry(tmp_path,monkeypatch):
    monkeypatch.setattr(c,'protect',lambda *a:{'private':1,'public':1});monkeypatch.setattr(c,'metadata',lambda *a:{})
    items=c.plan();monkeypatch.setattr(c,'plan',lambda:[items[-1]])
    p=tmp_path/'access'/f"{c.sha(items[-1]['url'].encode())}.STOP.json";c.save(p,c.encode({'error':'HTTP 403'}))
    monkeypatch.setattr(c,'request',lambda *a:pytest.fail('No network after access stop'))
    first=c.collect(tmp_path,tmp_path);second=c.collect(tmp_path,tmp_path)
    assert first==second and not first['files'] and first['blocked'][0]['error']=='HTTP 403'
