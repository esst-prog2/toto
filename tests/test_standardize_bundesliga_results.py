"""Synthetic conversion/evidence regressions; no private datasets required."""
from copy import deepcopy
import csv
import hashlib
import io
import json
import sys

import pytest

from scripts import standardize_bundesliga_results as converter
from scripts.validate_bundesliga_csv import audit_file
from toto_estimator.historical_import import OUTPUT_COLUMNS


def record(**changes):
    return dict(dict(source_row=2, season='1993/1994', date='1994-04-03',
                     home_team='Bayern Munich', away_team='Nurnberg', home_goals=5, away_goals=0), **changes)


def correction():
    return dict(correction_id=converter.CORRECTION_ID, status='VERIFIED_PENDING_STANDARDIZATION',
                source_file='original.csv', source_sha256='expected-hash', source_row=2,
                expected_source_fields={'Date': '1994-04-03', 'FT': '5-0'},
                field='Date', source_value='1994-04-03', verified_value='1994-05-03',
                official_score=dict(home_goals=5, away_goals=0), applied=False,
                sources=['https://example.org/evidence'], justification='Verified replay date.')


def test_correction_only_changes_derived_date_and_uses_existing_identity(tmp_path):
    original = record()
    corrected = converter.apply_correction(original, {'Date':'1994-04-03','FT':'5-0'},
                                          'original.csv', 'expected-hash', correction())
    assert original['date'] == '1994-04-03'
    assert corrected == dict(original, date='1994-05-03')
    rows = [corrected, record(date='1993-11-01',home_team='Nurnberg',away_team='Bayern Munich',home_goals=0,away_goals=1)]
    content, summary = converter.convert_bundesliga_rows(rows, tmp_path)
    assert content == converter.convert_bundesliga_rows(rows[::-1], tmp_path)[0]
    parsed = list(csv.DictReader(io.StringIO(content.decode())))
    assert tuple(parsed[0]) == OUTPUT_COLUMNS
    replay = next(r for r in parsed if r['date']=='1994-05-03')
    identity = ['Bundesliga','1993/1994','1994-05-03','Bayern Munich','Nurnberg']
    assert replay['match_id'] == hashlib.sha256(json.dumps(identity,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
    assert summary['accepted']==2
    assert not list(tmp_path.iterdir())


@pytest.mark.parametrize('change', [dict(source_sha256='wrong'),dict(source_file='other.csv'),
    dict(source_row=3),dict(expected_source_fields={'FT':'2-1'}),dict(status='UNVERIFIED'),
    dict(applied=True),dict(sources=[]),dict(field='Score'),dict(source_value='1994-04-04'),
    dict(official_score={'home_goals':2,'away_goals':1})])
def test_correction_fails_closed_on_changed_or_unverified_evidence(change):
    c=dict(correction(),**change)
    with pytest.raises(ValueError):
        converter.apply_correction(record(),{'Date':'1994-04-03','FT':'5-0'},'original.csv','expected-hash',c)


def test_shared_adapter_retains_awarded_results_and_rejects_duplicate_fixtures(tmp_path):
    r=record(season='1992/1993',date='1993-05-22',home_team='KFC Uerdingen',away_team='Eintracht Frankfurt',home_goals=2)
    parsed=list(csv.DictReader(io.StringIO(converter.convert_bundesliga_rows([r],tmp_path)[0].decode())))
    assert (parsed[0]['home_team'],parsed[0]['home_goals'],parsed[0]['away_goals'])==('KFC Uerdingen','2','0')
    with pytest.raises(ValueError,match='importer|duplicate'):
        converter.convert_bundesliga_rows([r,dict(r,date='1993-05-23')],tmp_path)


def test_audit_exposes_same_annotation_parsing_without_changing_default_report(tmp_path):
    path=tmp_path/'early.csv'
    path.write_text('Round,Date,Team 1,FT,HT,Team 2\n1,(Sat) 22 May 1993 (20),KFC Uerdingen (32),2-0,1-3,Eintracht Frankfurt (32)\n')
    default=audit_file(path,'1992/1993','early')
    expanded=audit_file(path,'1992/1993','early',include_records=True)
    records=expanded.pop('records')
    assert expanded==default
    assert records==[dict(source_row=2,season='1992/1993',date='1993-05-22',home_team='KFC Uerdingen',away_team='Eintracht Frankfurt',home_goals=2,away_goals=0)]
    assert any(i['code']=='halftime_exceeds_fulltime' for i in default['issues'])


def exception_inputs():
    r=record(date='1994-05-03')
    standard=[dict(r,match_id='stable-id',league='Bundesliga')]
    original=record()
    raw={'Date':'1994-04-03','FT':'5-0'}
    e=dict(exception_id='E2',season=r['season'],source_file='original.csv',source_sha256='expected-hash',
           source_row=2,original_fields=raw,classification='COMPLETED_REPLAY_AFTER_ANNULMENT',
           official_archive_score='5-0',on_field_score={'home_goals':5,'away_goals':0},
           on_field_score_is_completed_final=True,ordinary_90_minute_training_eligible=False,
           evidence=['https://example.org/replay'],correction_id=converter.CORRECTION_ID,
           annulled_original={'date':'1994-04-23','home_goals':2,'away_goals':1,'archive_fixture':False})
    policy={'exceptions':[e],'policy':['Preserve official outcomes']}
    originals={('original.csv',2):(raw,original,'expected-hash')}
    applied=[dict(correction(),applied=True)]
    sources={r['season']:{'url':'https://example.org/source.csv'}}
    return policy,originals,standard,applied,sources


def test_exception_links_corrected_id_retains_annulled_original_only_as_metadata():
    args=exception_inputs()
    sidecar=converter.link_exceptions(*args)
    e=sidecar['exceptions'][0]
    assert e['match_id']=='stable-id' and e['date']=='1994-05-03'
    assert e['ordinary_90_minute_training_suitability']=='EXCLUDED'
    assert e['annulled_original']['archive_fixture'] is False
    assert sidecar['unlisted_match_training_suitability']=='UNRESOLVED'
    assert len(args[2])==1


@pytest.mark.parametrize('change',['row','hash','score','duplicate','dangling','correction'])
def test_exception_metadata_rejects_bad_references(change):
    args=deepcopy(exception_inputs());e=args[0]['exceptions'][0]
    if change=='row':e['source_row']=3
    if change=='hash':e['source_sha256']='wrong'
    if change=='score':e['official_archive_score']='2-1'
    if change=='duplicate':args[0]['exceptions'].append(deepcopy(e))
    if change=='dangling':args[2].clear()
    if change=='correction':e['correction_id']='wrong'
    with pytest.raises(ValueError):converter.link_exceptions(*args)


def test_insufficient_eligibility_evidence_is_unresolved():
    args=exception_inputs();args[0]['exceptions'][0]['evidence']=[]
    assert converter.link_exceptions(*args)['exceptions'][0]['ordinary_90_minute_training_suitability']=='UNRESOLVED'


def complete_schedule():
    rows=[]
    for year in range(1990,2026):
        teams=[f'Team {i}' for i in range(20 if year==1991 else 18)]
        rows.extend(dict(season=f'{year}/{year+1}',date=f'{year}-09-01',home_team=h,away_team=a,home_goals=0,away_goals=0)
                    for h in teams for a in teams if h!=a)
    return rows


def test_all_season_coverage_including_twenty_team_season_and_changed_pairing():
    rows=complete_schedule()
    report=converter.validate_coverage(rows)
    assert len(rows)==11090 and len(report)==36
    assert report[1]['matches']==380 and report[1]['teams']==20
    rows[0]=dict(rows[1])  # Same count, one duplicate and one missing pairing.
    with pytest.raises(ValueError,match='fixture coverage'):converter.validate_coverage(rows)


@pytest.mark.parametrize('check',[False,True])
def test_existing_outputs_are_never_replaced(tmp_path,monkeypatch,check):
    target=tmp_path/converter.OUTPUT_NAMES[0];target.write_bytes(b'preserve')
    monkeypatch.setattr(converter,'PRIVATE',tmp_path)
    monkeypatch.setattr(sys,'argv',['standardize_bundesliga_results']+(['--check'] if check else []))
    if check:
        monkeypatch.setattr(converter,'build',lambda:{target.name:b'changed'})
        with pytest.raises(ValueError,match='differs'):converter.main()
    else:
        def unexpected():pytest.fail('must refuse existing output before conversion')
        monkeypatch.setattr(converter,'build',unexpected)
        with pytest.raises(FileExistsError):converter.main()
    assert target.read_bytes()==b'preserve'
