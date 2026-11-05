"""Offline synthetic tests of the second-tier adapter and shared converter."""
from copy import deepcopy
import pytest
from scripts.standardize_second_bundesliga_results import convert_records, apply_verified_correction, LEAGUE
from test_second_bundesliga import special
from test_second_bundesliga_review import correction_fixture


def test_two_phases_keep_all_instances_and_stable_ids(tmp_path):
    rows = special()
    content, records, summary = convert_records(rows, tmp_path)
    repeat, _, _ = convert_records(list(reversed(rows)), tmp_path)
    assert repeat == content
    assert len(records) == len({r['match_id'] for r in records}) == 384
    assert len({(r['home_team'], r['away_team']) for r in records}) == 264
    assert {r['league'] for r in records} == {LEAGUE}
    assert summary['first']['accepted'] == 264
    assert summary['second']['accepted'] == 120


def test_true_duplicate_instance_rejected(tmp_path):
    rows=special();rows.append(deepcopy(rows[0]))
    with pytest.raises(ValueError):convert_records(rows,tmp_path)


def test_guarded_derivative_changes_only_replay_facts(tmp_path):
    correction=correction_fixture(tmp_path)
    record=dict(source_row=2,season='2005/2006',date='2005-11-04',home_team='Wacker Burghausen',
                away_team='1860 Munchen',home_goals=0,away_goals=2,division='2')
    original=deepcopy(record)
    result=apply_verified_correction(record,correction,tmp_path)
    assert record==original
    assert result==dict(record,date='2006-03-29',home_goals=1,away_goals=0)
    assert correction['applied'] is False


@pytest.mark.parametrize('key,value',[('date','2005-11-05'),('home_goals',1),('source_row',3)])
def test_correction_rejects_different_record(tmp_path,key,value):
    correction=correction_fixture(tmp_path)
    record=dict(source_row=2,season='2005/2006',date='2005-11-04',home_team='Wacker Burghausen',
                away_team='1860 Munchen',home_goals=0,away_goals=2,division='2')
    record[key]=value
    with pytest.raises(ValueError):apply_verified_correction(record,correction,tmp_path)


def test_exception_links_and_unreviewed_policy(tmp_path,monkeypatch):
    from scripts import standardize_second_bundesliga_results as module
    classes=['COMPLETED_REPLAY']*4+['COMPLETED_REPLAY_AFTER_ABANDONMENT']*2+['COMPLETED_THEN_AWARDED']+['REPORTED_MANIPULATION_RESULT_RETAINED']*2
    cases=[];rows=[];standard=[]
    monkeypatch.setattr(module,'bound_row',lambda directory,binding: binding['original_fields'])
    for i,classification in enumerate(classes):
        row=dict(source_row=i+2,season='2000/2001',date=f'2000-08-{i+1:02}',home_team=f'Home{i}',away_team='Away',home_goals=1,away_goals=0)
        rows.append(row);standard.append(dict(row,match_id=f'id{i}'))
        cases.append(dict(classification=classification,source=dict(source_file=module.ENG,source_row=i+2,original_fields={}),
                          official_archived_fields=dict(Date=row['date'],hgoal='1',vgoal='0'),training_suitability='EXCLUDED',evidence=['https://example.org/result']))
    policy=dict(known_match_cases=cases,unlisted_training_suitability='UNRESOLVED',policy='Preserve archive',team_level_notes=[{'classification':'STANDINGS_ONLY'}]*2)
    result=module.link_exceptions(policy,rows,standard,tmp_path,{})
    assert len(result['exceptions'])==9 and len(result['team_level_contexts'])==2
    assert result['unlisted_match_training_suitability']=='UNRESOLVED'
    assert sum(e['evidence_status']=='UNRESOLVED_CONCERN' for e in result['exceptions'])==2
    policy['unlisted_training_suitability']='ELIGIBLE'
    with pytest.raises(ValueError):module.link_exceptions(policy,rows,standard,tmp_path,{})
