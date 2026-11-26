"""Adverse synthetic checks for independent Phase8 (no private data required)."""
from copy import deepcopy
import hashlib,json
import pytest
from scripts import validate_belgian_pro_league_final as v


def receipt(raw,path='test.csv',season='1995/1996'):
    return dict(path=path,sha256=v.digest(raw),bytes=len(raw),season=season)


def csv_original(**changes):
    d=dict(Date='1995-08-04',Season='1995',home='Home',visitor='Away',FT='2-1',hgoal='2',vgoal='1',division='B1',tier='1',totgoal='3',goaldif='1',result='H');d.update(changes)
    import csv,io
    b=io.StringIO();w=csv.DictWriter(b,fieldnames=list(d),lineterminator='\n');w.writeheader();w.writerow(d);return b.getvalue().encode()


def fixture(sid='a',**changes):
    r=dict(source_id=sid,source='jalapic/example.csv',date='2021-07-27',home='Home',away='Away',FT='0-1',stage='UNKNOWN',annotation='',season='2021/2022')
    r.update(changes);return r


def event(sid='a',**changes):
    d=dict(decision_id=sid,season='2021/2022',disposition='INCLUDE',stage='REGULAR_SEASON',reported_score='0-1',accepted_score='0-1',accepted_outcome='A',original_fixture_date='2021-07-27',chosen_match_date='2021-07-27',completion_date=None)
    d.update(changes);return d


def names(*rows):
    return {(r['season'],r['source'],r[k]):r[k] for r in rows for k in ('home','away')}


def evaluate_one(d=None,rows=None):
    d=d or event();rows=rows or [fixture()]
    return v.evaluate([(d,rows)],names(*rows),expected_count=1,expected_stages={'REGULAR_SEASON':1},expected_rematches=(0,0))


def test_raw_csv_independent_parse_and_binding():
    raw=csv_original();r=v.parse_csv(raw,receipt(raw))[0]
    assert r['FT']=='2-1' and r['date']=='1995-08-04' and r['line']==2
    assert r['physical_sha256']==v.digest(raw.splitlines(keepends=True)[1])


@pytest.mark.parametrize('change',[
 dict(hgoal='1'),dict(result='D'),dict(FT='2-2'),dict(tier='2'),dict(division='B2'),
 dict(totgoal='4'),dict(goaldif='0'),dict(Date='1996-08-04'),dict(Date='1995-02-30')])
def test_original_contradictions_not_silently_accepted(change):
    raw=csv_original(**change)
    with pytest.raises(ValueError):v.parse_csv(raw,receipt(raw))


def txt(year='2020/21',round='1',body='Home  v Away  2-1 (1-0)'):
    return f'= Belgium First Division A {year}\n▪ Matchday {round}\nSat Aug 8 2020\n{body}\n'.encode()


def test_wrong_path_2021_actually_2020_explicitly_preserved():
    raw=txt();rows,note=v.parse_txt(raw,receipt(raw,'openfootball/belgium/2021-22/be1.txt','2021/2022'))
    assert rows[0]['season']=='2020/2021' and note['path_mismatch']


def test_other_wrong_season_file_blocked():
    raw=txt()
    with pytest.raises(v.Defect,match='wrong-season'):v.parse_txt(raw,receipt(raw,'openfootball/belgium/2018-19/be1.txt','2018/2019'))


def test_round_outside_stage_blocked():
    raw=txt(round='999')
    with pytest.raises(v.Defect,match='Round'):v.parse_txt(raw,receipt(raw,'openfootball/belgium/2021-22/be1.txt','2021/2022'))


def test_halftime_cannot_exceed_final():
    raw=txt(body='Home  v Away  0-0 (1-0)')
    with pytest.raises(v.Defect,match='HT'):v.parse_txt(raw,receipt(raw,'openfootball/belgium/2021-22/be1.txt','2021/2022'))


def test_unscored_source_not_zero_zero():
    raw=txt(body='Home  v Away')
    rows,_=v.parse_txt(raw,receipt(raw,'openfootball/belgium/2021-22/be1.txt','2021/2022'))
    assert rows[0]['FT'] is None


def test_calendar_day_not_inferred_from_wrong_weekday():
    with pytest.raises(v.Defect,match='calendar'):v.heading_day('Sun Aug 8 2020',2020)


def test_independent_accepted_projection_exact():
    rows,*_=evaluate_one();assert rows[0]['date']=='2021-07-27'
    assert (rows[0]['home_goals'],rows[0]['away_goals'])==(0,1)
    assert rows[0]['match_id']==hashlib.sha256(json.dumps(['Belgian Pro League','2021/2022','2021-07-27','Home','Away'],separators=(',',':')).encode()).hexdigest()
    assert v.check_csv(v.csv_bytes(rows),rows)==rows


@pytest.mark.parametrize('field,value',[('accepted_score','5-0'),('accepted_outcome','H'),('chosen_match_date','2022-03-08'),('season','2020/2021')])
def test_bad_approved_facts_blocked(field,value):
    d=event();d[field]=value
    with pytest.raises(ValueError):evaluate_one(d)


def test_original_kickoff_for_resumption_verified_from_raw_start():
    d=event(case_id='beerschot_cercle_resumed',chosen_match_date='2021-07-24',completion_date='2021-07-27')
    rs=[fixture(),fixture('start',source='rsssf/test',date='2021-07-24',token='abd',FT=None)]
    rows,*_=evaluate_one(d,rs)
    assert rows[0]['date']=='2021-07-24'


def test_missing_original_interruption_cannot_justify_date_change():
    d=event(case_id='beerschot_cercle_resumed',chosen_match_date='2021-07-24',completion_date='2021-07-27')
    with pytest.raises(v.Defect,match='Missing original interruption'):evaluate_one(d)


def test_administrative_award_outcome_must_match_approved_case():
    d=event(case_id='union_beerschot_2022')
    with pytest.raises(v.Defect,match='award'):evaluate_one(d)


def test_hold_out_cannot_carry_accepted_score():
    with pytest.raises(v.Defect,match='Excluded'):evaluate_one(event(disposition='HOLD_OUT'))


def test_same_date_stage_collision_blocked():
    a,b=event(),event('b',stage='CHAMPIONSHIP')
    with pytest.raises(v.Defect,match='collision'):
        v.evaluate([(a,[fixture()]),(b,[fixture('b')])],names(fixture()))


def test_legitimate_rematch_kept_with_two_ids():
    a,b=event(),event('b',stage='CHAMPIONSHIP',original_fixture_date='2022-05-01',chosen_match_date='2022-05-01')
    rows,_,_,_,_,rematches=v.evaluate([(a,[fixture()]),(b,[fixture('b',date='2022-05-01')])],names(fixture()),expected_count=2,expected_stages={'REGULAR_SEASON':1,'CHAMPIONSHIP':1},expected_rematches=(1,2))
    assert len({r['match_id'] for r in rows})==2 and len(rematches)==1


def test_club_and_cercle_not_city_merged():
    d=event();r=fixture(home='Club Brugge',away='Cercle Brugge');n=names(r)
    n[(r['season'],r['source'],r['home'])]=n[(r['season'],r['source'],r['away'])]='Brugge'
    with pytest.raises(v.Defect,match='teams'):
        v.evaluate([(d,[r])],n)


def test_unproven_alias_not_guessed():
    with pytest.raises(v.Defect,match='identity'):v.evaluate([(event(),[fixture()])],{})


def test_coeval_names_derive_from_raw_shared_event_not_global_alias():
    h=fixture();m=fixture('b',source='modern/test',home='Bilingual Home')
    n,proof=v.coeval_names([(event(),[h,m])])
    assert n['2021/2022','modern/test','Bilingual Home']=='Home'
    assert ('2020/2021','modern/test','Bilingual Home') not in n


def test_inconsistent_coeval_mapping_blocked():
    h=fixture();m=fixture('b',source='modern/test',home='Bilingual Home')
    with pytest.raises(v.Defect,match='Ambiguous'):
        v.coeval_names([(event(),[h,m]),(event('b'),[fixture('c',home='Other'),m])])


def test_exact_schema_and_row_order_required():
    rows,*_=evaluate_one();raw=v.csv_bytes(rows)
    with pytest.raises(v.Defect,match='schema'):v.check_csv(raw.replace(b'match_id,date',b'date,match_id',1),rows)


def test_duplicate_csv_id_blocked():
    rows,*_=evaluate_one()
    with pytest.raises(v.Defect,match='duplicate'):v.check_csv(v.csv_bytes(rows+rows),rows)


def test_wrong_csv_id_blocked():
    rows,*_=evaluate_one();altered=deepcopy(rows);altered[0]['match_id']='0'*64
    with pytest.raises(v.Defect,match='ID'):v.check_csv(v.csv_bytes(altered),rows)


def test_unapproved_inclusion_not_accepted():
    rows,*_=evaluate_one();altered=deepcopy(rows);altered[0]['away_goals']=2
    with pytest.raises(v.Defect,match='Exact'):v.check_csv(v.csv_bytes(altered),rows)


def test_omitted_csv_event_detected():
    rows,*_=evaluate_one()
    with pytest.raises(v.Defect,match='Exact'):v.check_csv(v.csv_bytes([]),rows)


@pytest.mark.parametrize('bad',['-1','01','1.0',''])
def test_invalid_serialized_goals_rejected(bad):
    rows,*_=evaluate_one();altered=deepcopy(rows);altered[0]['home_goals']=bad
    with pytest.raises(v.Defect,match='goals'):v.check_csv(v.csv_bytes(altered),rows)


def test_crlf_serialization_not_byte_identical():
    rows,*_=evaluate_one();raw=v.csv_bytes(rows).replace(b'\n',b'\r\n')
    with pytest.raises(v.Defect,match='byte-for-byte'):v.check_csv(raw,rows)


def test_existing_assessment_not_overwritten(tmp_path):
    p=tmp_path/'f.json';v.keep(p,b'original');v.keep(p,b'original')
    with pytest.raises(v.Defect,match='Refusing'):v.keep(p,b'changed')
    assert p.read_bytes()==b'original'


def test_raw_rsssf_interruption_and_continuation_preserved_separately():
    raw=b'<h4><a name="pro">First Division A</a></h4>\n<a name="reg">Regular Stage</a>\nRound 1\n[Jul 24]\nBeerschot  abd Cercle Brugge  [abandoned at 0-1]\n[Jul 27]\nBeerschot  0-1 Cercle Brugge  [remaining 35 minutes]\n<h4><a name="cup">Cup</a></h4>\n[Jul 28]\nOther  1-0 Team\n'
    rec=dict(sha256=v.digest(raw),encoding='utf-8')
    rows=v.parse_rsssf(raw,rec)
    assert len(rows)==2 and rows[0]['token']=='abd' and rows[1]['FT']=='0-1'
    assert [r['date'] for r in rows]==['2021-07-24','2021-07-27']
    assert len({r['source_id'] for r in rows})==2


def test_raw_rsssf_award_from_multiline_annotation_not_onfield_invention():
    raw=b'<h4><a name="pro">First Division A</a></h4>\n<a name="reg">Regular Stage</a>\nRound 17\n[Dec 5]\nStandard  awd Charleroi  [awarded 0-3;\n abandoned at 0-3 due to crowd trouble]\n'
    rows=v.parse_rsssf(raw,dict(sha256=v.digest(raw),encoding='utf-8'))
    assert len(rows)==1 and rows[0]['token']=='awd' and rows[0]['FT']=='0-3'
    assert 'crowd trouble' in rows[0]['annotation']


def test_raw_rsssf_unresolved_award_is_blocked():
    raw=b'<h4><a name="pro">First Division A</a></h4>\n<a name="reg">Regular Stage</a>\nRound 17\n[Dec 5]\nStandard  awd Charleroi\n'
    with pytest.raises(v.Defect,match='numerical award'):
        v.parse_rsssf(raw,dict(sha256=v.digest(raw),encoding='utf-8'))


def test_protected_hash_does_not_ignore_actual_content_change(tmp_path):
    p=tmp_path/'old';p.write_bytes(b'changed')
    with pytest.raises(v.Defect,match='Protected file changed'):
        v.verify_protected_bytes(p,v.digest(b'original'))


def test_metadata_transition_requires_a_second_matching_read():
    from types import SimpleNamespace
    class HydratingFile:
        def __init__(self,second):self.stats=iter([1,2,2]);self.reads=iter([b'original',second])
        def stat(self):return SimpleNamespace(st_dev=1,st_ino=next(self.stats),st_size=8,st_mtime_ns=1,st_ctime_ns=1)
        def read_bytes(self):return next(self.reads)
        def __str__(self):return 'synthetic-hydrating-file'
    assert v.verify_protected_bytes(HydratingFile(b'original'),v.digest(b'original'))[1]==2
    with pytest.raises(v.Defect,match='confirmation'):
        v.verify_protected_bytes(HydratingFile(b'changed!'),v.digest(b'original'))


def test_continuing_metadata_transition_does_not_hide_a_byte_mismatch():
    from types import SimpleNamespace
    class FileProviderRead:
        def __init__(self,second):self.i=0;self.data=iter([b'original',second])
        def stat(self):
            self.i+=1
            return SimpleNamespace(st_dev=1,st_ino=self.i,st_size=8,st_mtime_ns=1,st_ctime_ns=self.i)
        def read_bytes(self):return next(self.data)
        def __str__(self):return 'synthetic-file-provider-read'
    assert v.verify_protected_bytes(FileProviderRead(b'original'),v.digest(b'original'))[1]==3
    with pytest.raises(v.Defect,match='confirmation'):
        v.verify_protected_bytes(FileProviderRead(b'changed!'),v.digest(b'original'))
