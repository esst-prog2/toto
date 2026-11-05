"""Synthetic source and exceptional-format tests, no network/private inputs."""
import csv
import io
import json
from urllib.error import HTTPError

import pytest

from scripts import acquire_second_bundesliga as acquisition
from scripts.validate_second_bundesliga import (format_for,parse_eng,parse_football_txt,
                                                special_1991,validate_season)


def regular(year,n):
    return [dict(source_row=i+2,season=f'{year}/{year+1}',date=f'{year}-08-10',
                 home_team=f'Club {h}',away_team=f'Club {a}',home_goals=2,away_goals=0,division='2')
            for i,(h,a) in enumerate((h,a) for h in range(n) for a in range(n) if h!=a)]


@pytest.mark.parametrize('year,n,total',[(1990,20,380),(1992,24,552),(1993,20,380),(1994,18,306),(2025,18,306)])
def test_historical_round_robin_sizes(year,n,total):
    result=validate_season(regular(year,n),year,total)
    assert result['status']=='PASS' and result['actual_teams']==n
    assert result['actual_matches']==total and result['historical_validator']=='PASS'


def special():
    rows=[]
    for division in ('2North','2South'):
        for phase in (1,2):
            for h in range(12):
                for a in range(12):
                    if h==a or (phase==2 and (h<6)!=(a<6)):continue
                    rows.append(dict(source_row=len(rows)+2,season='1991/1992',date='1991-08-10' if phase==1 else '1992-03-10',
                                     home_team=f'{division} Club {h}',away_team=f'{division} Club {a}',
                                     home_goals=2 if h<a else 0,away_goals=0 if h<a else 2,division=division))
    return rows


def test_regional_two_phase_schedule_not_whole_league_round_robin():
    rows=special();result=validate_season(rows,1991,384)
    assert result['status']=='PASS' and result['actual_teams']==24
    assert all(r['first_phase_matches']==132 and r['second_phase_matches']==60 for r in result['special_format'])
    assert all(g['matches']==30 for r in result['special_format'] for g in r['groups'])
    assert len({(r['home_team'],r['away_team']) for r in rows})==264 # 120 legal cross-phase repeats


@pytest.mark.parametrize('change',['missing','cross_group','duplicate','wrong_phase','regional_overlap'])
def test_regional_schedule_rejects_real_anomalies(change):
    rows=special()
    if change=='missing':rows.pop()
    if change=='cross_group':
        row=next(r for r in rows if r['date'].startswith('1992'));row['away_team']='2North Club 10'
    if change=='duplicate':rows[1]=dict(rows[0])
    if change=='wrong_phase':rows[-1]['date']='1991-12-16'
    if change=='regional_overlap':rows[-1]['home_team']='2North Club 0'
    assert validate_season(rows,1991,384)['status']=='REVIEW'


def eng_bytes(**changes):
    row=dict(Date='2005-11-04',Season='2005',home='Wacker Burghausen',visitor='1860 Munchen',
             FT='0-2',hgoal='0',vgoal='2',tier='2',division='2');row.update(changes)
    buffer=io.StringIO();writer=csv.DictWriter(buffer,fieldnames=list(row));writer.writeheader();writer.writerow(row)
    return buffer.getvalue().encode()


def test_eng_preserves_source_schema_and_does_not_correct_annulled_results():
    columns,selected,records,issues=parse_eng(eng_bytes())
    assert not issues and selected[0]['FT']=='0-2'
    assert records[0]['date']=='2005-11-04' and records[0]['away_goals']==2
    assert 'match_id' not in columns


@pytest.mark.parametrize('change',[dict(FT='1-0'),dict(hgoal=''),dict(Date='2003-10-01'),dict(division='1'),dict(home='')])
def test_eng_required_fields_classification_dates_and_scores(change):
    _,selected,records,issues=parse_eng(eng_bytes(**change))
    assert selected and not records and issues


def test_txt_ignores_goal_events_preserves_missing_scores_and_rolls_calendar():
    content='''= 2. Fußball-Bundesliga 2025/2026
▪ 1. Spieltag
Fri Aug 1 2025
  20:30  Team A   v Team B     2-1 (1-0) @ Venue
            (1-0 Player 16'
             2-1 Player 90')
▪ 18. Spieltag
Fri Jan 16
  18:30  Team B   v Team A
'''.encode()
    rows,issues,fixtures=parse_football_txt(content,'2025/2026')
    assert fixtures==2 and len(rows)==1 and rows[0]['home_goals']==2
    assert [i['code'] for i in issues]==['unscored_fixture']


def test_txt_unknown_layout_wrong_competition_and_date_fail_closed():
    with pytest.raises(ValueError,match='competition'):
        parse_football_txt(b'= Deutsche Bundesliga 2025/26','2025/2026')
    content=b'= Deutsche 2. Bundesliga 2025/26\n\xe2\x96\xaa 1. Round\nMon Aug 1 2025\n A v B   1-0\nUNKNOWN STATUS\n'
    rows,issues,_=parse_football_txt(content,'2025/2026')
    assert not rows and {i['code'] for i in issues}=={'invalid_date','missing_fixture_context','unrecognized_line'}


def test_equal_counts_do_not_hide_duplicate_or_missing_pairing():
    rows=regular(2020,18);rows[0]=dict(rows[1])
    assert validate_season(rows,2020,306)['status']=='REVIEW'


def test_acquisition_cache_checks_original_bytes_without_request(tmp_path,monkeypatch):
    monkeypatch.setattr(acquisition,'PRIVATE',tmp_path)
    url='https://raw.githubusercontent.com/example/repo/commit/file.csv'
    path=tmp_path/'file.csv';path.write_bytes(b'original')
    path.with_name('file.csv.provenance.json').write_text(json.dumps(dict(url=url,sha256=acquisition.sha(b'original'))))
    monkeypatch.setattr(acquisition,'urlopen',lambda *a,**k:pytest.fail('cache must not request'))
    assert acquisition.fetch(url,'file.csv')==b'original'
    path.write_bytes(b'changed')
    with pytest.raises(ValueError,match='checksum'):acquisition.fetch(url,'file.csv')


def test_acquisition_denial_stops_without_retry_or_other_hosts(tmp_path,monkeypatch):
    monkeypatch.setattr(acquisition,'PRIVATE',tmp_path);monkeypatch.setattr(acquisition,'LAST_REQUEST',None)
    calls=[]
    def denied(request,**kwargs):
        calls.append(request.full_url);raise HTTPError(request.full_url,429,'limited',{},io.BytesIO(b'limit'))
    monkeypatch.setattr(acquisition,'urlopen',denied)
    with pytest.raises(HTTPError):acquisition.fetch('https://api.github.com/repos/example/repo','metadata.json')
    with pytest.raises(RuntimeError,match='stop'):acquisition.fetch('https://api.github.com/repos/other/repo','other.json')
    assert len(calls)==1 and (tmp_path/'ACCESS_STOP.json').exists()
    for url in ['https://datencenter.dfb.de/','https://www.kicker.de/','https://www.football-data.co.uk/germanym.php']:
        with pytest.raises(ValueError):acquisition.fetch(url,'forbidden')
