"""Synthetic parser/format tests; no private historical result data included."""
from datetime import date
import json

import pytest

from scripts.acquire_serie_b import fetch, plan
from scripts.validate_serie_b import audit, football_data, football_txt, format_for, record, rsssf


@pytest.mark.parametrize('year,clubs',[(y,20 if y<=2002 or y>=2019 else 24 if y==2003 else 19 if y==2018 else 22) for y in range(1990,2026)])
def test_historical_formats(year,clubs):
    assert format_for(year)==(clubs,clubs*(clubs-1))


def test_scope_and_sources():
    entries=plan()
    assert len(entries)==36
    assert sum(format_for(y)[1] for y in range(1990,2026))==14962
    assert [e['kind'] for e in entries].count('rsssf')==7
    assert all('2627' not in e['url'] and '2026-27' not in e['url'] for e in entries)
    with pytest.raises(ValueError): format_for(2026)


def test_paired_scores_use_printed_team_orientation_for_both_legs():
    rows,excluded,notes=rsssf(b'SERIE B\nStages 1-20\nAlpha - Beta = 2 - 0 * 1 - 3\nFINAL TABLE\nSERIE C/1\n',1991)
    assert [(r['home'],r['away'],r['hg'],r['ag']) for r in rows]==[('Alpha','Beta','2','0'),('Beta','Alpha','3','1')]
    assert all(r['date'] is None for r in rows)
    assert not excluded


def test_footnote_marker_is_annotation_not_an_extra_club():
    rows,_,_=rsssf(b'SERIE B\nStages 1-20\nAlpha* - Beta = 0 - 2 * 1 - 1\n* administrative note\nFINAL TABLE\nSERIE C/1\n',1993)
    assert rows[0]['home']=='Alpha'
    assert rows[1]['away']=='Alpha'


def test_abandoned_fixture_never_uses_interim_score_as_final():
    rows,_,notes=rsssf(b'Italy Second Division (Serie B)\nRound 25 (March 4)\nAlpha - Beta    Abd [abandoned at 1-3]\nFINAL TABLE\nItaly Third Division\n',1995)
    assert rows[0]['hg'] is None and rows[0]['ag'] is None
    assert rows[0]['date_basis']=='source_round_only'
    assert audit(rows,1995)['missing_scores']==1
    assert notes


def test_matrix_handles_unspaced_name_score_and_excludes_diagonal():
    names=[f'Club{chr(65+i)}' for i in range(20)]
    lines=['Second Level (Serie B)']
    for i,name in enumerate(names):
        cells=['-' if i==j else '2-1' for j in range(20)]
        lines.append(f'{i+1}. {name}'+(' ' if i==0 else '')+' '.join(cells))
    lines+=['FINAL TABLE','Third Level']
    rows,_,_=rsssf('\n'.join(lines).encode(),1996)
    result=audit(rows,1996)
    assert result['records']==380 and result['teams']==20
    assert result['status']=='UNDATED_RESULTS'
    assert rows[19]['home']=='ClubB' and rows[19]['away']=='ClubA'


@pytest.mark.parametrize('heading',['▪ Playoff, Final','▪ Relegation, Final','== Playout','== Aufstieg'])
def test_postseason_is_separated_by_source_stage(heading):
    content=f'= Italian Serie B 2024/25\n▪ Matchday 1\nFri Aug 16 2024\nAlpha  v Beta  2-1 (1-0)\n{heading}\nSun Jun 1 2025\nBeta  v Alpha  0-0\n'.encode()
    rows,excluded,notes=football_txt(content,2024)
    assert len(rows)==len(excluded)==1
    assert excluded[0]['stage']!='Regular Season'
    assert not notes


def test_unscored_postponed_fixture_keeps_null_score_and_annotation():
    rows,excluded,_=football_txt(b'= Italian Serie B\nFri Aug 22 2025\nAlpha  v Beta  [postponed]\n',2025)
    assert rows[0]['away']=='Beta'
    assert rows[0]['hg'] is None
    assert rows[0]['annotation']=='[postponed]'


def test_compact_scores_and_award_annotations():
    rows,_,_=football_txt(b'= Italian Serie B\nSat Oct 31 2020\nAlpha  3-0  Beta  [awarded]\n',2020)
    assert rows[0]['away']=='Beta'
    assert rows[0]['annotation']=='[awarded]'


def test_covid_year_inheritance_after_june():
    rows,_,notes=football_txt(b'= Italian Serie B\nFri Jun 26 2020\nAlpha  v Beta  1-0\nFri Jul 3\nBeta  v Alpha  0-0\n',2019)
    assert rows[1]['date']=='2020-07-03'
    assert not notes


def test_unknown_text_fails_closed():
    with pytest.raises(ValueError,match='Unrecognized'):
        football_txt(b'= Italian Serie B\nUNEXPECTED FIXTURE FORMAT\n',2024)


def test_csv_dates_competition_padding_and_result_checks():
    header='Div,Date,HomeTeam,AwayTeam,FTHG,FTAG,FTR\n'
    rows,_,notes=football_data((header+'I2,01/09/03,Alpha,Beta,2,0,H,,,\n').encode(),2003)
    assert rows[0]['date']=='2003-09-01'
    assert notes[0]['code']=='empty_csv_padding'
    _,_,notes=football_data((header+'I2,ambiguous,Alpha,Beta,2,0,A,extra\n').encode(),2003)
    assert {n['code'] for n in notes}=={'extra_csv_fields','invalid_or_missing_date','result_disagreement'}
    with pytest.raises(ValueError,match='competition'):
        football_data((header+'I1,01/09/03,Alpha,Beta,2,0,H\n').encode(),2003)


def test_duplicate_pair_missing_values_bad_dates_and_scores():
    rows=[record(1,'Alpha','Beta','-1','1','2027-01-01'),record(2,'Alpha','Beta')]
    result=audit(rows,2025)
    assert result['duplicate_fixtures']==1
    assert result['missing_dates']==1 and result['missing_scores']==1
    assert {'negative_score','date_outside_season','missing_pairings'}<=set(result['issues'])


def test_cached_sources_are_checksum_bound_and_denied_hosts_stay_stopped(tmp_path):
    url='https://www.rsssf.org/tablesi/ital91.html'
    p=tmp_path/'originals/a';p.parent.mkdir();p.write_bytes(b'changed')
    p.with_name('a.provenance.json').write_text(json.dumps(dict(url=url,sha256='wrong',bytes=7)))
    with pytest.raises(ValueError,match='checksum'):fetch(url,'originals/a',tmp_path)
    (tmp_path/'access_stops').mkdir();(tmp_path/'access_stops/www.rsssf.org.json').write_text('{}')
    with pytest.raises(RuntimeError,match='stopped'):fetch(url,'originals/b',tmp_path)
    with pytest.raises(ValueError):fetch('https://example.com/data','x',tmp_path)
    with pytest.raises(ValueError):fetch(url,'../escape',tmp_path)


def test_early_decisive_match_is_excluded_and_original_context_retained():
    content=b'SERIE B\nStages 1-20\nAlpha - Beta = 0 - 0 * 1 - 1\nFINAL TABLE\n(*)Decisive match (16th place):\nNeutral ground, 20 giu 1992\nAlpha - Beta    2-1 a.e.t.\nSERIE C/1\n'
    rows,excluded,notes=rsssf(content,1991)
    assert len(rows)==2 and len(excluded)==1
    assert excluded[0]['stage']=='Decisive tie-break'
    assert any('20 giu 1992' in line['text'] for note in notes if note['code']=='section_text' for line in note['lines'])


def test_internal_table_disagreement_is_reported_without_repair():
    content=b'SERIE B\nStages 1-20\nAlpha - Beta = 1 - 0 * 0 - 0\nFINAL TABLE\n1. ALPHA  38  1 0 0 0 1 0 1 1 0  9 0 2\nSERIE C/1\n'
    rows,_,notes=rsssf(content,1991)
    disagreements=[n for n in notes if n['code']=='table_goal_disagreement']
    assert disagreements[0]['parsed_goals']==[1,0]
    assert disagreements[0]['table_goals']==[9,0]
    assert rows[0]['hg']=='1'
