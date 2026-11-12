"""Synthetic Serie A conversion/correction/linkage tests; no private match facts."""
from collections import Counter
from copy import deepcopy
import csv
import hashlib
from itertools import permutations
import json
import sys

import pytest

from scripts import standardize_serie_a_results as converter
from toto_estimator.historical_import import OUTPUT_COLUMNS


def record(**changes):
    r=dict(source_file='synthetic.csv',source_row=2,season='2000/2001',date='2000-09-01',
           home_team='Home FC',away_team='Away FC',home_goals=1,away_goals=0)
    r.update(changes);return r


def source_fixture(tmp_path,records):
    rows=[dict(Date=r['date'],Season=r['season'][:4],home=r['home_team'],visitor=r['away_team'],
               hgoal=str(r['home_goals']),vgoal=str(r['away_goals'])) for r in records]
    path=tmp_path/'synthetic.csv'
    with path.open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    sha=hashlib.sha256(path.read_bytes()).hexdigest()
    bindings=[dict(source_file=path.name,source_row=i+2,source_sha256=sha,original_fields=r) for i,r in enumerate(rows)]
    return path,bindings


@pytest.fixture
def guarded(tmp_path):
    original=record();path,bindings=source_fixture(tmp_path,[original])
    correction=dict(correction_id='TEST-DATE-1',source=bindings[0],replacements={'Date':'2000-09-02'},
                    status='VERIFIED_PENDING_STANDARDIZATION',applied=False,
                    evidence=[dict(url='https://example.org/match',access='FULL_MATCH_PAGE')])
    return tmp_path,path,original,correction


def test_date_correction_changes_only_derived_date_and_preserves_evidence(guarded):
    directory,path,original,correction=guarded
    before=path.read_bytes();old=deepcopy(original);evidence=deepcopy(correction)
    corrected,applied=converter.apply_corrections([original],[correction],directory)
    assert corrected==[dict(original,date='2000-09-02')]
    assert original==old and correction==evidence and path.read_bytes()==before
    assert applied[0]['applied'] is True
    assert applied[0]['source']==correction['source']


@pytest.mark.parametrize('change,match', [
    ('score','Date'),('team','Date'),('applied','unapplied'),('status','verified'),
    ('evidence','evidence'),('snippet','evidence'),('hash','checksum'),('fields','fields'),
    ('row','fields'),('facts','facts'),('season','season'),('date','season'),
    ('unchanged','unchanged'),('noncanonical','Noncanonical'),
])
def test_correction_guards(guarded,change,match):
    directory,_,original,correction=guarded
    if change=='score':correction['replacements']['hgoal']='9'
    if change=='team':correction['replacements']['home']='Other'
    if change=='applied':correction['applied']=True
    if change=='status':correction['status']='UNVERIFIED'
    if change=='evidence':correction['evidence']=[]
    if change=='snippet':correction['evidence'][0]['access']='INDEXED_ONLY'
    if change=='hash':correction['source']['source_sha256']='0'*64
    if change=='fields':correction['source']['original_fields']['home']='Other'
    if change=='row':correction['source']['source_row']=3
    if change=='facts':original['home_goals']=9
    if change=='season':original['season']='1999/2000'
    if change=='date':correction['replacements']['Date']='2002-01-01'
    if change=='unchanged':correction['replacements']['Date']=original['date']
    if change=='noncanonical':correction['replacements']['Date']='20000902'
    with pytest.raises(ValueError,match=match):converter.apply_corrections([original],[correction],directory)


def test_corrections_require_unique_location_and_exactly_one_application(guarded):
    directory,_,original,correction=guarded
    with pytest.raises(ValueError,match='Duplicate'):converter.apply_corrections([original],[correction,deepcopy(correction)],directory)
    with pytest.raises(ValueError,match='multiple'):converter.apply_corrections([original,deepcopy(original)],[correction],directory)
    with pytest.raises(ValueError,match='absent'):converter.apply_corrections([],[correction],directory)


@pytest.mark.parametrize('year,n',[(1990,18),(2003,18),(2004,20),(2025,20)])
def test_full_historical_format_coverage(year,n):
    rows=[record(source_row=i+2,season=f'{year}/{year+1}',date=f'{year}-09-01',home_team=f'Team {h}',away_team=f'Team {a}')
          for i,(h,a) in enumerate(permutations(range(n),2))]
    report=converter.validate_coverage(rows,years=[year])
    assert report==[dict(season=f'{year}/{year+1}',teams=n,matches=n*(n-1),expected_matches=n*(n-1),status='PASS')]
    rows[-1]=deepcopy(rows[0])
    with pytest.raises(ValueError,match='coverage'):converter.validate_coverage(rows,years=[year])


def test_all_36_seasons_and_total_without_private_data():
    rows=[]
    for year in range(1990,2026):
        n=18 if year<=2003 else 20
        rows.extend(record(source_row=len(rows)+i+2,season=f'{year}/{year+1}',date=f'{year}-09-01',home_team=f'Team {h}',away_team=f'Team {a}')
                    for i,(h,a) in enumerate(permutations(range(n),2)))
    assert len(rows)==12644 and len(converter.validate_coverage(rows))==36
    rows[0]['season']='2026/2027'
    with pytest.raises(ValueError,match='scope'):converter.validate_coverage(rows)


def test_shared_conversion_exact_schema_facts_ids_and_reordering(tmp_path):
    rows=[record(),record(source_row=3,date='2000-09-02',home_team='Away FC',away_team='Home FC',home_goals=0,away_goals=0)]
    content,standard,summary=converter.convert_records(rows,tmp_path)
    repeat,other,_=converter.convert_records(list(reversed(rows)),tmp_path)
    assert content==repeat and standard==other
    assert tuple(next(csv.reader(content.decode().splitlines())))==OUTPUT_COLUMNS
    assert summary==dict(total=2,accepted=2,rejected=0,duplicates=0,fixtures=0,conflicts=0)
    for r in standard:
        expected=hashlib.sha256(json.dumps([converter.LEAGUE,r['season'],r['date'],r['home_team'],r['away_team']],ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
        assert r['match_id']==expected and r['league']=='Serie A'
    assert not list(tmp_path.glob('.standardize-*'))


def test_correction_date_changes_id_scores_do_not_and_aliases_stay_raw(guarded):
    directory,_,original,correction=guarded
    _,old,_=converter.convert_records([original],directory)
    corrected,_=converter.apply_corrections([original],[correction],directory)
    _,new,_=converter.convert_records(corrected,directory)
    assert old[0]['match_id']!=new[0]['match_id']
    assert old[0]['home_team']==new[0]['home_team']=='Home FC'
    _,score,_=converter.convert_records([dict(corrected[0],home_goals=4)],directory)
    assert new[0]['match_id']==score[0]['match_id']


@pytest.mark.parametrize('change', ['date','missing','negative','duplicate','whitespace','future'])
def test_shared_converter_rejects_bad_or_normalized_facts(tmp_path,change):
    rows=[record()]
    if change=='date':rows[0]['date']='2000-02-30'
    if change=='missing':rows[0]['home_team']=''
    if change=='negative':rows[0]['home_goals']=-1
    if change=='duplicate':rows.append(dict(rows[0],date='2000-09-02'))
    if change=='whitespace':rows[0]['home_team']=' Home FC'
    if change=='future':rows[0]['season']='2026/2027'
    with pytest.raises(ValueError):converter.convert_records(rows,tmp_path)


def seven_cases(tmp_path):
    kinds=[('COMPLETED_REPLAY_AFTER_ABANDONMENT','EXCLUDED')]*3+[
        ('UNPLAYED_ADMINISTRATIVE_AWARD','EXCLUDED'),('FIRST_PLAYED_AFTER_OVERTURNED_AWARD','ELIGIBLE')]+[
        ('INTERRUPTED_THEN_RESUMED_AND_COMPLETED','UNRESOLVED')]*2
    records=[record(source_row=i+2,date=f'2000-09-{i+1:02}',home_team=f'Home {i}',away_team=f'Away {i}') for i in range(7)]
    _,bindings=source_fixture(tmp_path,records)
    cases=[dict(case_id=f'E{i+1}',source=binding,classification=kind,training_suitability=decision,
                training_reason='Synthetic documented reason.',evidence=[dict(url='https://example.org',access='FULL_REPORT')],
                original_on_field_event=dict(score=None,completed=False,evidence_status='SYNTHETIC'),
                original_scheduled_date=r['date'],actual_playing_or_completion_date=None if 'AWARD'==kind[-5:] else r['date'],
                official_final_date=r['date'],official_final_result='1-0',source_correction_required=False)
           for i,(r,binding,(kind,decision)) in enumerate(zip(records,bindings,kinds))]
    policy=dict(unlisted_training_suitability='UNRESOLVED',eligibility_scope='Synthetic scope',policy_sources=['synthetic'],known_match_cases=cases)
    _,standard,_=converter.convert_records(records,tmp_path)
    return records,standard,policy


def test_seven_exception_links_preserve_decisions_evidence_and_unknown_default(tmp_path):
    records,standard,policy=seven_cases(tmp_path);before=deepcopy(policy)
    sidecar=converter.link_exceptions(policy,records,records,standard,[],tmp_path)
    assert len(sidecar['exceptions'])==7
    assert len({e['match_id'] for e in sidecar['exceptions']})==7
    assert Counter(e['training_suitability'] for e in sidecar['exceptions'])==converter.DECISIONS
    assert sidecar['unlisted_match_training_suitability']=='UNRESOLVED'
    for case in sidecar['exceptions']:
        if case['training_suitability']=='UNRESOLVED':
            assert case['ordinary_90_minute_training_eligible'] is None
            assert case['conservative_training_action']=='HOLD_OUT_PENDING_REVIEW'
        assert case['original_on_field_event']['score'] is None
    assert policy==before


@pytest.mark.parametrize('change,match', [('duplicate','Duplicate'),('dangling','dangling'),('decision','decisions'),('default','Unreviewed'),('result','result'),('evidence','evidence'),('correction','correction')])
def test_exception_guards(tmp_path,change,match):
    records,standard,policy=seven_cases(tmp_path)
    case=policy['known_match_cases'][0]
    if change=='duplicate':case['source']=deepcopy(policy['known_match_cases'][1]['source'])
    if change=='dangling':case['source']['source_row']=999
    if change=='decision':case['training_suitability']='ELIGIBLE'
    if change=='default':policy['unlisted_training_suitability']='ELIGIBLE'
    if change=='result':case['official_final_result']='0-0'
    if change=='evidence':case['evidence']=[]
    if change=='correction':case['source_correction_required']=True
    with pytest.raises(ValueError,match=match):converter.link_exceptions(policy,records,records,standard,[],tmp_path)


def test_cli_refuses_existing_outputs_before_build(tmp_path,monkeypatch):
    monkeypatch.setattr(converter,'PRIVATE',tmp_path)
    (tmp_path/converter.OUTPUT_NAMES[0]).write_text('existing')
    def forbidden():raise AssertionError('build ran')
    monkeypatch.setattr(converter,'build',forbidden);monkeypatch.setattr(sys,'argv',['converter'])
    with pytest.raises(FileExistsError):converter.main()
    assert (tmp_path/converter.OUTPUT_NAMES[0]).read_text()=='existing'


def test_check_mode_reports_mismatch_without_replacing_files(tmp_path,monkeypatch):
    monkeypatch.setattr(converter,'PRIVATE',tmp_path)
    name=converter.OUTPUT_NAMES[0];p=tmp_path/name;p.write_bytes(b'original')
    monkeypatch.setattr(converter,'build',lambda:{name:b'different'})
    monkeypatch.setattr(sys,'argv',['converter','--check'])
    with pytest.raises(ValueError,match='differs'):converter.main()
    assert p.read_bytes()==b'original'


def test_swapped_eligibility_cannot_hide_behind_unchanged_counts(tmp_path):
    records,standard,policy=seven_cases(tmp_path)
    cases=policy['known_match_cases']
    cases[0]['training_suitability'],cases[4]['training_suitability']='ELIGIBLE','EXCLUDED'
    assert Counter(c['training_suitability'] for c in cases)==converter.DECISIONS
    with pytest.raises(ValueError,match='classification mismatch'):
        converter.link_exceptions(policy,records,records,standard,[],tmp_path)


def test_corrected_exception_links_new_id_and_retains_original_binding(tmp_path):
    records,_,policy=seven_cases(tmp_path)
    case=policy['known_match_cases'][0]
    case.update(official_final_date='2000-09-10',source_correction_required=True,correction_id='TEST-REPLAY-DATE')
    correction=dict(correction_id='TEST-REPLAY-DATE',source=deepcopy(case['source']),replacements={'Date':'2000-09-10'},
                    status='VERIFIED_PENDING_STANDARDIZATION',applied=False,
                    evidence=[dict(url='https://example.org',access='FULL_REPORT')])
    corrected,applied=converter.apply_corrections(records,[correction],tmp_path)
    _,standard,_=converter.convert_records(corrected,tmp_path)
    sidecar=converter.link_exceptions(policy,records,corrected,standard,applied,tmp_path)
    linked=sidecar['exceptions'][0]
    match=next(r for r in standard if r['home_team']==records[0]['home_team'])
    assert linked['match_id']==match['match_id'] and linked['date']=='2000-09-10'
    assert linked['source']['original_fields']['Date']=='2000-09-01'
    assert linked['applied_correction']['applied'] is True
    assert case['source']['original_fields']['Date']=='2000-09-01'
