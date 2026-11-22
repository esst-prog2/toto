"""Synthetic Phase 3 acquisition/cache and inventory tests; no network/data needed."""
from copy import deepcopy
import hashlib
import json
from itertools import permutations

import pytest

from scripts import collect_la_liga_history as c
from scripts.inventory_la_liga_history import inventory_rows,parse_text


def blob(raw):return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()


def test_exact_twelve_paths_at_fixed_revision():
    p=c.plan()
    assert len(p)==12 and len({r['path'] for r in p})==12
    assert [r['season'] for r in p]==[f'{y}/{y+1}' for y in range(2013,2025)]
    assert all(r['commit']==c.PIN and '/1-liga.txt' in r['url'] and 'football-data' not in r['url'] for r in p)
    assert not any('/2012-13/' in r['path'] or '/2025-26/' in r['path'] or '/2026-27/' in r['path'] for r in p)


def test_git_tree_scope_and_blob_integrity():
    raw=b'synthetic'
    entries=[dict(type='blob',path=i['original_path'],sha=blob(raw),size=len(raw)) for i in c.plan()]
    t=dict(sha=c.PIN,truncated=False,tree=entries)
    assert len(c.checked_tree(json.dumps(t).encode()))==12
    assert c.verify_file(raw,entries[0])==blob(raw)
    with pytest.raises(ValueError):c.verify_file(raw+b'changed',entries[0])
    for bad in [dict(t,truncated=True),dict(t,sha='0'*40),dict(t,tree=entries[:-1])]:
        with pytest.raises(ValueError):c.checked_tree(json.dumps(bad).encode())


@pytest.fixture
def cached(tmp_path):
    i=c.plan()[0];raw=b'synthetic';entry=dict(sha=blob(raw),size=len(raw))
    r=dict(i,sha256=c.sha(raw),bytes=len(raw),git_blob_sha1=blob(raw),retrieved_at_utc='2000-01-01T00:00:00Z')
    p=tmp_path/i['path'];c.save(p,raw);c.save(p.with_name(p.name+'.provenance.json'),c.encode(r))
    return tmp_path,i,raw,entry,r


def test_cache_reuses_original_bytes_and_receipt(cached):
    p,i,raw,entry,r=cached
    assert c.cached(p,i,entry)==r
    assert (p/i['path']).read_bytes()==raw


@pytest.mark.parametrize('change',['hash','url','revision','blob','missing_receipt','missing_original'])
def test_cache_corruption_is_not_silently_redownloaded(cached,change):
    directory,i,_,entry,r=cached;p=directory/i['path'];receipt=p.with_name(p.name+'.provenance.json')
    if change=='hash':r['sha256']='0'*64
    if change=='url':r['url']='https://example.org/unapproved'
    if change=='revision':r['commit']='0'*40
    if change=='blob':p.write_bytes(b'changed')
    if change=='missing_receipt':receipt.unlink()
    elif change=='missing_original':p.unlink()
    else:receipt.write_bytes(c.encode(r))
    with pytest.raises(ValueError):c.cached(directory,i,entry)


def test_complete_collection_is_idempotent_and_offline(tmp_path,monkeypatch):
    monkeypatch.setattr(c,'protect',lambda directory:dict(previous_competition_files=428,phase2_files=19))
    raw=b'synthetic';entries=[]
    for item in c.plan():
        entries.append(dict(type='blob',path=item['original_path'],sha=blob(raw),size=len(raw)))
        r=dict(item,sha256=c.sha(raw),bytes=len(raw),git_blob_sha1=blob(raw))
        p=tmp_path/item['path'];c.save(p,raw);c.save(p.with_name(p.name+'.provenance.json'),c.encode(r))
    tree=c.encode(dict(sha=c.PIN,truncated=False,tree=entries));c.save(tmp_path/c.TREE,tree)
    c.save(tmp_path/c.TREE_RECEIPT,c.encode(dict(url=c.TREE_URL,sha256=c.sha(tree))))
    old=[]
    for name in ['jalapic/engsoccerdata/data-raw/spain.csv',c.REPO+'/2012-13/1-liga.txt',c.REPO+'/2025-26/1-liga.txt']:
        c.save(tmp_path/name,raw);old.append(dict(path=name,sha256=c.sha(raw),bytes=len(raw),kind='dataset'))
    c.save(tmp_path/'acquisition.json',c.encode(dict(files=old,rights={'synthetic':'unresolved'})))
    c.save(tmp_path/'feasibility_diagnostics.json',b'{}')
    c.save(tmp_path/c.REPO/'LICENSE.md',b'CC0 1.0 Universal\n')
    def forbidden(*a,**kw):raise AssertionError('Network requested for completed cache')
    monkeypatch.setattr(c,'urlopen',forbidden)
    c.collect(tmp_path)
    before={str(p):p.read_bytes() for p in tmp_path.rglob('*') if p.is_file()}
    c.collect(tmp_path)
    assert before=={str(p):p.read_bytes() for p in tmp_path.rglob('*') if p.is_file()}


def test_covid_july_year_inheritance_preserves_lines_and_bytes():
    raw='= Primera División 2019/20\n▪ Matchday 1\nFri Jun 26 2020\nAlpha  v Beta  1-0\nFri Jul 3\nBeta  v Alpha  0-0\n'.encode()
    before=bytes(raw);rows,notes=parse_text(raw,2019)
    assert rows[1]['date']=='2020-07-03' and rows[1]['source_line']==6 and raw==before
    r=inventory_rows(rows,2019,2,notes)
    assert r['date_error_lines']==[] and r['documented_extended_calendar_lines']==[6]


def test_wide_round_candidates_not_corrections_or_exclusions():
    rows=[dict(source_line=1,home='Alpha',away='Beta',hg='1',ag='0',date='2020-09-01',stage='Matchday 1'),
          dict(source_line=2,home='Beta',away='Alpha',hg='0',ag='1',date='2020-10-01',stage='Matchday 1')]
    before=deepcopy(rows);r=inventory_rows(rows,2020,2)
    assert len(r['wide_round_spans'])==1 and r['records']==2 and rows==before
    assert r['status']=='INVENTORY_COMPLETE'


def test_missing_scores_bad_dates_and_weekdays_are_reported():
    rows=[dict(source_line=1,home='Alpha',away='Beta',hg=None,ag=None,date='2027-01-01',stage='Matchday 1')]
    r=inventory_rows(rows,2020,2,[dict(kind='weekday_mismatch',line=1,text='synthetic')])
    assert r['scored']==0
    assert {'missing_or_invalid_scores','date_errors','weekday_mismatch'}<=set(r['issues'])
