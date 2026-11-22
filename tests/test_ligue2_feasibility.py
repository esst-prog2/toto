"""Synthetic-only feasibility and acquisition integrity tests; no network/data."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import pytest
from scripts import collect_ligue2_feasibility as c
from scripts import validate_ligue2_feasibility as v


def modern(body='A v B  2-1',year=2024,label='Matchday 1',day='Fri Aug 16 2024'):
    return f'= French Ligue 2 {year}/{str(year+1)[-2:]}\n▪ {label}\n{day}\n{body}\n'.encode()


def rsssf(body='A - B = 1-0 - 2-3',heading='Stages 1-20 08.08. 21.05.'):
    return f'<html><pre>Other league 3-0\n</pre><pre>Division 2\n{heading}\n{body}\nFinal Table:\n1.A 38 18 14 6 56-38 68\n</pre></html>'.encode('latin1')


def test_scope_exact():
    p=c.plan();assert len(p)==7;assert [x['season'] for x in p]==['2014/2015','2017/2018','2019/2020','2022/2023','2024/2025','2025/2026','1998/1999']
    assert all(x['commit']==c.PIN for x in p[:-1]);assert p[-1]['url']==c.RSSSF;assert p[-1]['original_path']=='tablesf/fran99.html'


@pytest.mark.parametrize('label',['Matchday 1','Regular Season - 1','1. Round'])
def test_round_grammars(label):
    rows,_=v.parse_text(modern(label=label),2024);assert rows[0]['round']==1;assert rows[0]['FT']=='2-1'


@pytest.mark.parametrize('body,status',[('A v B  2-1','2-1'),('A 2-1 B','2-1'),('A v B',None),('A v B [cancelled]',None),('A v B [postponed]',None)])
def test_literal_scores_and_unplayed(body,status):
    rows,_=v.parse_text(modern(body),2024);assert rows[0]['FT']==status
    if status is None:assert rows[0]['hg'] is None and rows[0]['ag'] is None


@pytest.mark.parametrize('change',[
 lambda b:b.replace(b'Ligue 2',b'Ligue 1'),lambda b:b.replace(b'2024/25',b'2023/24'),
 lambda b:b.replace(b'Fri Aug 16',b'Thu Aug 16'),lambda b:b.replace(b'Matchday 1',b'Matchday 35'),
 lambda b:b.replace(b'A v B  2-1',b'A v B  ?-1'),lambda b:b.replace(b'A v B  2-1',b'A v B  2-'),
 lambda b:b.replace(b'Matchday 1',b'Unknown stage'),lambda b:b.replace(b'Fri Aug 16 2024\n',b''),
 lambda b:b+b'garbage\n',lambda b:b+b'(unclosed\n'])
def test_unknown_or_invalid_source_fails(change):
    with pytest.raises(ValueError):v.parse_text(change(modern()),2024)


def test_postseason_separate():
    b=modern()+'\n▪ Promotion Playoffs Final\nFri May 23 2025\nC v D  1-0\n'.encode()
    rows,_=v.parse_text(b,2024);a=v.assess(rows,2024);assert a['observed']==1;assert a['other_stage_observations']==1;assert a['total_observations']==2


@pytest.mark.parametrize('year,n',[(2014,20),(2017,20),(2019,20),(2022,20),(2024,18),(2025,18)])
def test_ligue2_counts_not_ligue1(year,n):
    day={2014:'Fri Aug 1 2014',2017:'Fri Jul 28 2017',2019:'Fri Jul 26 2019',2022:'Sat Jul 30 2022',2024:'Fri Aug 16 2024',2025:'Sat Aug 9 2025'}[year]
    rows,_=v.parse_text(modern(year=year,day=day),year);a=v.assess(rows,year);assert a['expected_clubs']==n;assert a['expected_scheduled']==n*(n-1);assert a['expected_played']==(280 if year==2019 else n*(n-1))


def test_cancelled_preserved_distinct_missing_result():
    rows,_=v.parse_text(modern('A v B [cancelled]\nC v D'),2024);a=v.assess(rows,2024)
    assert a['unscored']==2 and len(a['source_cancelled_lines'])==1


def test_duplicates_missing_and_names_visible():
    rows,_=v.parse_text(modern('A v B  1-0\nA v B  2-0\nÁ v C  0-0'),2024);a=v.assess(rows,2024)
    assert len(a['duplicate_directed_pairs'])==1;assert a['missing_directed_pairs'];assert 'Á' in a['team_names'];assert rows[0]['FT']=='1-0'


def test_rsssf_preserves_literal_columns_and_proxies():
    rows,notes=v.rsssf(rsssf());assert len(rows)==2;assert rows[0]['home']=='A';assert rows[1]['home']=='B';assert rows[1]['FT']=='2-3'
    assert rows[1]['source_left_team']=='A';assert rows[1]['source_score_left']=='2';assert rows[1]['venue_and_score_semantics'].endswith('UNRESOLVED')
    assert all(r['date_semantics']=='ROUND_HEADING_PROXY_NOT_EXPLICIT_FIXTURE_DATE' for r in rows)
    assert rows[0]['date']=='1998-08-08' and rows[1]['date']=='1999-05-21';assert notes['headers']


@pytest.mark.parametrize('raw',[b'<pre>none</pre>',rsssf(body='A - B = ?-0 - 2-3'),rsssf(heading='Stages 1-20 31.02. 21.05.'),rsssf()+rsssf()])
def test_bad_rsssf_fails(raw):
    with pytest.raises(ValueError):v.rsssf(raw)


def test_rsssf_no_aliases():
    rows,_=v.rsssf(rsssf(body='A - B = 1-0 - 2-3\nAA - B = 0-0 - 0-0'));a=v.rsssf_assess(rows)
    assert a['literal_clubs']==3;assert a['missing_literal_pairs'];assert rows[2]['home']=='AA'


def test_tree_paths_and_pin_fail_closed():
    for d in [dict(sha=c.PIN,truncated=True,tree=[]),dict(sha='wrong',tree=[]),dict(sha=c.PIN,tree=[])]:
        with pytest.raises(ValueError):c.base.tree_entries(c.encode(d),c.PIN,c.PATHS)


def test_blob_identity():
    b=b'original\n';e=dict(sha=hashlib.sha1(b'blob 9\0'+b).hexdigest(),size=9)
    assert c.base.verify_blob(b,e)==e['sha']
    with pytest.raises(ValueError):c.base.verify_blob(b+b'changed',e)


def test_access_stop_prevents_network(tmp_path,monkeypatch):
    c.save(tmp_path/'ACCESS_STOP.json',b'{}')
    monkeypatch.setattr(c,'build_opener',lambda *a:pytest.fail('network attempted'))
    with pytest.raises(RuntimeError):c.request('https://example.com',tmp_path)


def test_preservation_detects_changed_previous_file(tmp_path):
    d=tmp_path/'data/private/france/ligue_2';d.mkdir(parents=True);a=tmp_path/'prior';a.write_bytes(b'prior');log=tmp_path/'PLANNING_LOG.md';log.write_bytes(b'history\n')
    baseline=dict(private={'prior':c.sha(b'prior')},public={'prior':c.sha(b'prior')},planning_log=dict(bytes=8,sha256=c.sha(b'history\n')))
    c.save(d/'protected_before.json',c.encode(baseline));assert c.protect(d,tmp_path)=={'private':1,'public':1}
    log.write_bytes(b'history\nappended\n');c.protect(d,tmp_path)
    a.write_bytes(b'changed')
    with pytest.raises(ValueError):c.protect(d,tmp_path)


def test_missing_and_one_sided_score_rejected():
    for value in ['A v B  1-?','A v B  -1']:
        with pytest.raises(ValueError):v.parse_text(modern(value),2024)
