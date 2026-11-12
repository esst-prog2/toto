"""Synthetic review checks; no private historical records or network calls."""
from copy import deepcopy
import csv
import hashlib

import pytest

from scripts.verify_serie_a_review import (
    bound_facts, check_samples, check_corrections, check_policy, date_collisions,
)


def samples():
    result=[]
    for i in range(20):
        year=(1990,2000,2010,2020)[i//5]+i%5
        result.append(dict(sample_id=f'S{i}',source=dict(source_file='synthetic.csv',source_row=i+2),
                           date=f'{year}-09-01',home_team='Home FC',away_team='Away FC',home_goals=1,away_goals=0,
                           observed=dict(date=f'{year}-09-01',home_team='Home',away_team='Away',home_goals=1,away_goals=0,competition='Serie A',regular_season=True),
                           team_identity_mapping={'Home':'Home FC','Away':'Away FC'},reference_url='https://example.org/match',
                           access='FULL_MATCH_PAGE',evidence_note='Synthetic evidence transcription.',status='AGREES'))
    return result


def test_calendar_decades_use_observed_date_and_require_each_quota():
    rows=samples()
    assert check_samples(rows)['decades']=={1990:5,2000:5,2010:5,2020:5}
    rows[0]['date']='1989-09-01';rows[0]['status']='DISCREPANCY'
    assert check_samples(rows)['decades'][1990]==5
    rows[0]['observed']['date']='1989-09-01';rows[0]['status']='AGREES'
    with pytest.raises(ValueError,match='coverage'): check_samples(rows)


def test_snippets_do_not_satisfy_full_page_quota():
    rows=samples();rows[0]['access']='INDEXED_ONLY'
    with pytest.raises(ValueError,match='coverage'):check_samples(rows)


@pytest.mark.parametrize('change,match', [
    ('duplicate','Duplicate'),('binding','Duplicate'),('competition','competition'),
    ('stage','competition'),('alias','identity'),('orientation','identity'),
    ('concealed','concealed'),('invented','invented'),('access','access'),('url','reference'),
])
def test_review_integrity_errors(change,match):
    rows=samples()
    if change=='duplicate':rows[1]['sample_id']=rows[0]['sample_id']
    if change=='binding':rows[1]['source']=rows[0]['source']
    if change=='competition':rows[0]['observed']['competition']='Coppa Italia'
    if change=='stage':rows[0]['observed']['regular_season']=False
    if change=='alias':rows[0]['team_identity_mapping']={}
    if change=='orientation':rows[0]['observed']['home_team']='Away'
    if change=='concealed':rows[0]['observed']['home_goals']=2
    if change=='invented':rows[0]['status']='DISCREPANCY'
    if change=='access':rows[0]['access']='PAGE_SHELL'
    if change=='url':rows[0]['reference_url']=''
    with pytest.raises(ValueError,match=match):check_samples(rows)


@pytest.fixture
def bound_sample(tmp_path):
    original=dict(Date='2000-09-01',Season='2000',home='Home FC',visitor='Away FC',hgoal='1',vgoal='0')
    p=tmp_path/'synthetic.csv'
    with p.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(original));w.writeheader();w.writerow(original)
    binding=dict(source_file=p.name,source_row=2,source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),original_fields=original)
    sample=samples()[5];sample['source']=binding;sample['observed']['date']='2000-09-02';sample['status']='DISCREPANCY'
    correction=dict(correction_id='TEST-DATE',sample_id=sample['sample_id'],source=deepcopy(binding),replacements={'Date':'2000-09-02'},status='VERIFIED_PENDING_STANDARDIZATION',applied=False,evidence=[dict(url='https://example.org',access='FULL_MATCH_PAGE')])
    return tmp_path,sample,correction


def test_bound_correction_is_read_only(bound_sample):
    directory,sample,correction=bound_sample
    p=directory/'synthetic.csv';before=p.read_bytes()
    check_corrections(directory,[correction],[sample])
    assert p.read_bytes()==before


@pytest.mark.parametrize('change,match', [
    ('applied','cannot apply'),('score','scope'),('date','scope'),('missing','Missing'),
    ('duplicated','unique'),('evidence','evidence'),('binding','binding'),
])
def test_correction_guards(bound_sample,change,match):
    directory,sample,correction=bound_sample;corrections=[correction]
    if change=='applied':correction['applied']=True
    if change=='score':correction['replacements']['hgoal']='5'
    if change=='date':correction['replacements']['Date']='2000-10-01'
    if change=='missing':corrections=[]
    if change=='duplicated':corrections.append(deepcopy(correction))
    if change=='evidence':correction['evidence'][0]['access']='INDEXED_ONLY'
    if change=='binding':correction['source']['source_row']=3
    with pytest.raises(ValueError,match=match):check_corrections(directory,corrections,[sample])


def test_source_checksums_exact_fields_and_paths(bound_sample):
    directory,sample,_=bound_sample;binding=sample['source']
    assert bound_facts(directory,binding)['home_goals']==1
    changed=deepcopy(binding);changed['original_fields']['home']='Changed'
    with pytest.raises(ValueError,match='fields'):bound_facts(directory,changed)
    changed=deepcopy(binding);changed['source_sha256']='0'*64
    with pytest.raises(ValueError,match='checksum'):bound_facts(directory,changed)
    changed=deepcopy(binding);changed['source_file']='../outside.csv'
    with pytest.raises(ValueError,match='outside'):bound_facts(directory,changed)


def policy_for(sample,kind,decision):
    return dict(unlisted_training_suitability='UNRESOLVED',known_match_cases=[dict(
        case_id='E1',source=sample['source'],classification=kind,training_suitability=decision,
        training_reason='Explicit synthetic policy reason.',evidence=[dict(url='https://example.org',access='FULL_REPORT')],
        actual_playing_or_completion_date='2000-09-01',original_on_field_event=dict(completed=True,score='1-0'),
        official_final_result='1-0',official_final_date='2000-09-01',source_correction_required=False)])


@pytest.mark.parametrize('kind,decision', [
    ('COMPLETED_REPLAY_AFTER_ABANDONMENT','EXCLUDED'),
    ('INTERRUPTED_THEN_RESUMED_AND_COMPLETED','UNRESOLVED'),
    ('FIRST_PLAYED_AFTER_OVERTURNED_AWARD','ELIGIBLE'),
])
def test_status_specific_policy_avoids_blanket_exclusion(bound_sample,kind,decision):
    directory,sample,_=bound_sample
    policy=policy_for(sample,kind,decision)
    assert check_policy(directory,policy,[],expected_cases=1)=={decision:1}
    policy['unlisted_training_suitability']='ELIGIBLE'
    with pytest.raises(ValueError,match='Unlisted'):check_policy(directory,policy,[],expected_cases=1)


def test_award_cannot_invent_play_and_replay_not_automatically_eligible(bound_sample):
    directory,sample,_=bound_sample
    policy=policy_for(sample,'UNPLAYED_ADMINISTRATIVE_AWARD','EXCLUDED')
    with pytest.raises(ValueError,match='Invented'):check_policy(directory,policy,[],expected_cases=1)
    case=policy['known_match_cases'][0];case['actual_playing_or_completion_date']=None;case['original_on_field_event']={'completed':False,'score':None}
    assert check_policy(directory,policy,[],expected_cases=1)=={'EXCLUDED':1}
    case['classification']='COMPLETED_REPLAY_AFTER_ABANDONMENT';case['training_suitability']='ELIGIBLE'
    with pytest.raises(ValueError,match='policy'):check_policy(directory,policy,[],expected_cases=1)


def test_same_team_date_collisions_ignore_score_and_orientation():
    rows=[dict(date='2000-09-01',home='A',away='B',source_row=2),dict(date='2000-09-01',home='C',away='A',source_row=3)]
    assert date_collisions(rows)==[dict(date='2000-09-01',team='A',source_rows=[2,3])]
    rows[1]['date']='2000-09-02'
    assert not date_collisions(rows)
