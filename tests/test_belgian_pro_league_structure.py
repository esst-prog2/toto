"""Independent synthetic Phase 4 cases; no previous parser or private fixture use."""
from copy import deepcopy
import csv,io,inspect
import pytest
from scripts import validate_belgian_pro_league_structure as s


def receipt(raw,path='synthetic',season='2023/2024',encoding='utf-8-sig'):
    return dict(path=path,sha256=s.sha(raw),season=season,encoding=encoding)


def original(body='A v B  2-1 (1-0)',year=2023,stage='Matchday 1',day='Fri Aug 4 2023'):
    return f'= Belgium First Division A {year}/{(year+1)%100:02}\n▪ {stage}\n{day}\n{body}\n'.encode()


def parse(body='A v B  2-1',**kwargs):
    raw=original(body,**kwargs);return s.txt_rows(raw,receipt(raw))[0]


def historical(cells=None):
    f=io.StringIO(newline='');w=csv.writer(f);w.writerow(s.COLUMNS);w.writerow(cells or ['1995-08-04','1995','A','B','3-1','3','1','B1','1','4','2','H']);return f.getvalue().encode()


def test_own_parser_path_has_no_previous_validation_imports():
    code=inspect.getsource(s)
    for forbidden in ('import validate_belgian_pro_league_feasibility','import inventory_belgian_pro_league_history','v.parse','v.assess','v.overlap','shared.heading'):
        assert forbidden not in code


def test_csv_schema_and_original_physical_bytes():
    raw=historical();r=s.csv_rows(raw,receipt(raw))[0]
    assert not r['errors'] and r['stage']=='UNKNOWN' and r['source_line']==2
    assert r['physical_record_sha256']==s.sha(raw.splitlines(keepends=True)[1])
    assert r['audit_id']==s.sid(s.sha(raw),2,2) and 'match_id' not in r


@pytest.mark.parametrize('index,value,issue',[(0,'04/08/1995','INVALID_DATE'),(0,'1997-08-04','DATE_OUTSIDE_CANONICAL_SEASON'),(2,'A ','INVALID_TEAM_LABEL'),(3,'A','INVALID_TEAM_LABEL'),(4,'1-3','FT_CONTRADICTION'),(5,'?','INVALID_GOALS'),(5,'-1','INVALID_GOALS'),(7,'B2','WRONG_COMPETITION'),(8,'2','WRONG_COMPETITION'),(9,'9','DERIVED_GOALS_CONTRADICTION'),(10,'-2','DERIVED_GOALS_CONTRADICTION'),(11,'A','OUTCOME_CONTRADICTION')])
def test_all_csv_fields_challenged_without_correction(index,value,issue):
    cells=['1995-08-04','1995','A','B','3-1','3','1','B1','1','4','2','H'];cells[index]=value
    raw=historical(cells);r=s.csv_rows(raw,receipt(raw))[0]
    assert issue in r['errors'] and r['original_fields'][s.COLUMNS[index]]==value


@pytest.mark.parametrize('change',[lambda x:x.replace(b'"Date"',b'"Other"') if b'"Date"' in x else x.replace(b'Date,',b'Other,'),lambda x:x.replace(b'1995-08-04,1995',b'1995-08-04,bad'),lambda x:x.replace(b',4,2,H',b',4,2,H,extra')])
def test_malformed_csv_fails_explicitly(change):
    raw=change(historical())
    with pytest.raises(ValueError):s.csv_rows(raw,receipt(raw))


@pytest.mark.parametrize('year,expected',[(1990,18),(2002,18),(2009,16),(2019,16),(2020,18),(2021,18),(2022,18),(2023,16),(2025,16)])
def test_nominal_expectations_do_not_force_records(year,expected):
    assert s.expected_clubs(year)==expected


@pytest.mark.parametrize('stage,label',[('Matchday 1','REGULAR_SEASON'),('1. Round','REGULAR_SEASON'),('Playoff I, Matchday 1','CHAMPIONSHIP'),('Championship, Matchday 1','CHAMPIONSHIP'),('Europe, Matchday 1','EUROPE'),('Relegation, Matchday 1','PLAYDOWNS'),('ECL Playoff, Final','EUROPE_QUALIFICATION')])
def test_source_stage_not_filename(stage,label):
    raw=original(stage=stage);rs,meta=s.txt_rows(raw,receipt(raw,path='wrong/2025-26.txt',season='2025/2026'))
    assert rs[0]['stage']==label and rs[0]['season']=='2023/2024' and meta['path_season_mismatch']


@pytest.mark.parametrize('stage,year,n',[('REGULAR_SEASON',2020,18),('REGULAR_SEASON',2023,16),('CHAMPIONSHIP',2020,4),('CHAMPIONSHIP',2023,6),('EUROPE',2020,4),('EUROPE',2024,6),('PLAYDOWNS',2024,4),('EUROPE_QUALIFICATION',2024,2)])
def test_group_participant_expectations_are_independent(stage,year,n):
    assert s.expected_stage_clubs(stage,year)==n


@pytest.mark.parametrize('stage,day,year',[('Matchday 31','Fri Aug 4 2023',2023),('Championship, Matchday 7','Sat Aug 8 2020',2020),('Relegation, Matchday 7','Fri Aug 4 2023',2023),('Other 1','Fri Aug 4 2023',2023)])
def test_invalid_stage_round_fails(stage,day,year):
    raw=original(stage=stage,day=day,year=year)
    with pytest.raises(ValueError):s.txt_rows(raw,receipt(raw))


@pytest.mark.parametrize('day',['Thu Aug 4 2023','Fri Foo 4 2023','Fri Aug 32 2023','Fri Aug 4 2024'])
def test_invalid_day_or_season_year_rejected(day):
    raw=original(day=day)
    with pytest.raises(ValueError):s.txt_rows(raw,receipt(raw))


@pytest.mark.parametrize('body,ft,note',[('A v B',None,''),('A v B [cancelled]',None,'[cancelled]'),('A v B  0-5 [awarded]','0-5','[awarded]')])
def test_unfinished_and_awarded_are_not_eligibility_decisions(body,ft,note):
    r=parse(body)[0];assert r['FT']==ft and r['annotation']==note and 'disposition' not in r


def test_halftime_is_checked_against_fulltime():
    r=parse('A v B  1-0 (2-0)')[0];assert 'HALFTIME_EXCEEDS_FINAL' in r['errors']


def test_source_checksum_tamper_is_not_accepted():
    raw=original()
    with pytest.raises(ValueError):s.txt_rows(raw+b' ',receipt(raw))


def test_same_pair_new_stage_is_not_a_duplicate_identity():
    raw=original()+b'\n\xe2\x96\xaa Championship, Matchday 1\nFri Apr 5 2024\nA v B  2-1\n'
    rs,_=s.txt_rows(raw,receipt(raw));a=s.assess(rs,2023,True)
    assert len(a['pair_repeats'])==1 and not a['duplicate_stage_identities']
    assert s.identity(rs[0])!=s.identity(rs[1])


def test_duplicate_same_stage_date_detected():
    rs=parse('A v B  2-1\nA v B  2-1');assert s.assess(rs,2023,True)['duplicate_stage_identities']


def test_opponent_group_pairings_and_round_collisions_visible():
    rs=parse('A v B  2-1\nA v C  0-0');a=s.assess(rs,2023,True)['stages']['REGULAR_SEASON']
    assert a['missing_directed_pairings'] and a['rounds']['1']['repeated_clubs']==['A']


def test_independent_identity_inference_ignores_scores():
    modern=[]
    for n in range(6):
        r=parse()[0];r.update(date=f'2023-08-{n+4:02}',audit_id='m'+str(n));modern.append(r)
    historical=deepcopy(modern)
    for n,r in enumerate(historical):r.update(home='Historical A',away='Historical B',stage='UNKNOWN',audit_id='h'+str(n))
    historical[0].update(FT='0-0',hg='0',ag='0')
    result=s.correspond(historical,modern)
    assert result['matched']==6 and result['score_conflicts']==1


def test_overlap_season_guard():
    a=parse();b=deepcopy(a);b[0]['season']='2024/2025'
    with pytest.raises(ValueError):s.correspond(a,b)


def test_documentary_annulment_award_and_unplayed_are_distinct():
    raw=b'<b><a name="reg">Regular Stage</a></b>\n1.A 28 10 8 10 30-20 38\nRound 1 [Aug 1]\nA 1-2 Mouscron [annulled]\nB awd Mouscron [annulled; awarded 5-0]\nC n/p Mouscron\n<b><a name="play">Playoff Stage</a></b>\nA 3-1 B\n'
    rows=s.documentary(raw,receipt(raw))
    assert len(rows)==3 and [r['score'] for r in rows]==['1-2','awd','n/p']
    assert rows[0]['source_line']==4 and rows[0]['source_line_sha256']==s.sha(raw.splitlines(keepends=True)[3])


def test_early_standings_never_manufacture_dated_events():
    raw=b'First Division\n1.Club A 34 10 10 14 30-40 30\n'
    assert s.documentary(raw,receipt(raw))==[]
