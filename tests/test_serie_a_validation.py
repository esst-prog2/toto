"""Synthetic fixtures only: no private source dependency or match-data publication."""
import csv
from itertools import permutations

import pytest

from scripts.artifact_io import check_overwrite
from scripts.validate_serie_a import CSV_FIELDS, audit, football_txt, historical


def complete(year):
    n = 18 if year <= 2003 else 20
    return [dict(season=f'{year}/{year+1}', source_row=i+2, date=f'{year}-09-01',
                 home=f'Team {h}', away=f'Team {a}', hg='1', ag='0')
            for i,(h,a) in enumerate(permutations(range(n),2))]


@pytest.mark.parametrize('year,n,count', [(1990,18,306),(2003,18,306),(2004,20,380),(2025,20,380)])
def test_historical_format_boundaries(year,n,count):
    summary,issues,names = audit(complete(year), years=[year])
    assert not issues
    assert summary[0]['status']=='PASS'
    assert summary[0]['matches']==count
    assert len(names[f'{year}/{year+1}']['teams'])==n


def test_equal_count_duplicate_cannot_mask_missing_pair():
    rows=complete(2004)
    rows[-1]=dict(rows[0],source_row=999)
    summary,issues,_=audit(rows,years=[2004])
    assert summary[0]['matches']==380
    assert {'duplicate_fixture','missing_pairings','home_away_balance'} <= {i['code'] for i in issues}


def test_conflicting_fixture_and_missing_season():
    rows=complete(2003)
    rows.append(dict(rows[0],hg='7',source_row=999))
    _,issues,_=audit(rows,years=[2003,2004])
    assert 'conflicting_fixture' in {i['code'] for i in issues}
    assert any(i['season']=='2004/2005' and i['code']=='match_count' for i in issues)


@pytest.mark.parametrize('field,value', [('date','2005-02-30'),('date','2027-01-01'),('hg',''),('hg','-1'),('ag','1.5'),('home',''),('away','Team 0'),('home',' Team 0')])
def test_invalid_values_preserved_and_reported(field,value):
    rows=complete(2004); rows[0][field]=value
    _,issues,_=audit(rows,years=[2004])
    assert 'invalid_required_value' in {i['code'] for i in issues}
    assert rows[0][field]==value


def test_covid_extension_and_future_scope():
    rows=complete(2019);rows[0]['date']='2020-08-02'
    assert not audit(rows,years=[2019])[1]
    rows[0]['season']='2026/2027'
    with pytest.raises(ValueError,match='Unexpected seasons'): audit(rows,years=[2019])


def test_txt_explicit_and_inherited_dates_reordered(tmp_path):
    p=tmp_path/'season.txt'
    p.write_text('= Serie A\n▪ Regular Season - 1\nSat Aug 23 2025\n  20:45   Team A  2-1 (1-0)  Team B\n                  (Player 10\',\n                   Other 20\')\nSun Jan 4\n  15:00   Team B  0-0 (0-0)  Team A\nSun Sep 7\n  15:00   Team C  1-0  Team D\n')
    rows,issues=football_txt(p)
    assert [r['date'] for r in rows]==['2025-08-23','2026-01-04','2025-09-07']
    assert not issues
    assert rows[0]['home']=='Team A'


@pytest.mark.parametrize('text', ['  15:00   Team A  1-0  Team B\n','Sat Aug 23 2025\n  Team A  ?-?  Team B\n','Sat Aug 23 2025\nunknown line\n'])
def test_txt_fails_closed(tmp_path,text):
    p=tmp_path/'season.txt';p.write_text(text)
    with pytest.raises(ValueError): football_txt(p)


def test_txt_weekday_and_halftime(tmp_path):
    p=tmp_path/'season.txt';p.write_text('Sun Aug 23 2025\n  15:00   Team A  0-0 (1-0)  Team B\n')
    assert {i['code'] for i in football_txt(p)[1]}=={'weekday_mismatch','halftime_exceeds_fulltime'}


def csv_source(tmp_path,**changes):
    row=dict(zip(CSV_FIELDS,['2004-09-01','2004','Team A','Team B','2-1','2','1','1','1','3','1','H']))
    row.update(changes);p=tmp_path/'original.csv'
    with p.open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=CSV_FIELDS);writer.writeheader();writer.writerow(row)
    return p


def test_source_score_consistency_and_row_reference(tmp_path):
    p=csv_source(tmp_path,FT='0-0')
    before=p.read_bytes();rows,issues,total=historical(p)
    assert total==1 and rows[0]['source_row']==2
    assert issues[0]['code']=='source_consistency'
    assert p.read_bytes()==before


def test_csv_schema_and_width_rejected(tmp_path):
    p=csv_source(tmp_path);p.write_text(p.read_text()+ 'broken,row\n')
    with pytest.raises(ValueError,match='Malformed'): historical(p)
    p.write_text('Date,Date\n')
    with pytest.raises(ValueError,match='schema'): historical(p)


def test_no_ongoing_selection_and_overwrite(tmp_path):
    p=csv_source(tmp_path,Season='2026')
    assert historical(p)==([],[],1)
    with pytest.raises(FileExistsError): check_overwrite([p])


def test_checksum_tampering_fails_before_parsing(tmp_path):
    import hashlib
    import json
    from scripts.validate_serie_a import build
    p=tmp_path/'original';p.write_bytes(b'changed')
    (tmp_path/'acquisition.json').write_text(json.dumps([dict(file='original',bytes=8,sha256=hashlib.sha256(b'original').hexdigest())]))
    with pytest.raises(ValueError,match='checksum mismatch'): build(tmp_path)


def test_collector_pins_scope_and_refuses_before_network(tmp_path,monkeypatch):
    from scripts import collect_serie_a as collector
    assert len(collector.SOURCES)==2
    assert all(len(sha)==40 for _,sha,_ in collector.SOURCES)
    assert not any('2026-27' in path for _,_,paths in collector.SOURCES for path in paths)
    (tmp_path/'acquisition.json').write_text('existing')
    def forbidden(*args,**kwargs): raise AssertionError('network accessed')
    monkeypatch.setattr(collector,'urlopen',forbidden)
    with pytest.raises(FileExistsError): collector.collect(tmp_path)


def test_raw_team_variations_are_not_merged():
    rows=complete(2004)
    rows[0]['home']='Team Zero Alternate'
    summary,issues,names=audit(rows,years=[2004])
    assert summary[0]['teams']==21
    assert 'team_count' in {i['code'] for i in issues}
    assert 'Team Zero Alternate' in names['2004/2005']['teams']
