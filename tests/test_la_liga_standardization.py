"""Synthetic La Liga standardization/exception guards; no private data."""
from copy import deepcopy

import pytest

from scripts import standardize_la_liga_results as s


def data():
    cases=[];fixtures=[]
    for i,(identifier,_,action,start,end,h,a) in enumerate(s.policy.SPECS,1):
        source_date=end or '2026-03-04';year=int(source_date[:4])-(int(source_date[5:7])<7)
        original=dict(source_line=i,date=source_date,home=f'Home {i}',away=f'Away {i}',hg=str(h),ag=str(a),FT=f'{h}-{a}')
        c=dict(decision_id=identifier,source_file='synthetic.txt',source_sha256='0'*64,season=f'{year}/{year+1}',
               original=original,action=action,approved_source_score=[h,a],approval='USER_APPROVED_PHASE6',
               evidence_urls=['https://example.test/decision'],original_kickoff_date=start or end,
               completion_date=end,effective_result_date=end,
               final_outcome_status='UNRESOLVED' if action=='HOLD_OUT' else 'VERIFIED_COMPLETED_RESULT' if start else 'VERIFIED_PLAYED_RESULT')
        c['fixture_id']=s.policy.source_id(c['source_file'],c['source_sha256'],i);cases.append(c)
        f={k:deepcopy(c[k]) for k in ('fixture_id','source_file','source_sha256','season','original')}
        f['identified_final_outcome_status']='UNRESOLVED' if action=='HOLD_OUT' else 'NO_CONFLICT_IDENTIFIED'
        fixtures.append(f)
    ordinary=deepcopy(fixtures[0]);ordinary['original'].update(source_line=99,date='2020-07-01',home='Other Home',away='Other Away',hg='0',ag='1',FT='0-1')
    ordinary.update(season='2019/2020',fixture_id=s.policy.source_id('synthetic.txt','0'*64,99))
    fixtures.append(ordinary)
    return fixtures,dict(approval='USER_APPROVED_PHASE6',cases=cases,unresolved_final_outcome_ids=[cases[-1]['fixture_id']])


def standard(plans):
    result=[]
    for plan in plans:
        fields=plan['fields'];row={'match_id':s.standard_id(fields),**fields}
        result.append({k:row[k] for k in s.OUTPUT_COLUMNS})
    return result


def test_shared_importer_schema_reconciliation_ids_and_order_invariance(tmp_path):
    fixtures,policy=data();before=deepcopy((fixtures,policy));plans=s.prepare(fixtures,policy,set())
    raw,summary=s.convert(plans,tmp_path);reverse,_=s.convert(list(reversed(plans)),tmp_path)
    assert raw==reverse and raw.decode().splitlines()[0]==','.join(s.OUTPUT_COLUMNS)
    rows=s.parse_standard(raw)
    accepted,archive,counts,outcomes=s.check_and_partition(rows,fixtures,policy,set())
    assert summary==dict(total=6,accepted=6,rejected=0,duplicates=0,fixtures=0,conflicts=0)
    assert counts==dict(source_records=6,accepted=5,excluded=0,unresolved=1,omitted_from_screened=1)
    assert len(archive)==6 and len({r['match_id'] for r in rows})==6
    assert outcomes=={'1':3,'X':1,'2':1}
    assert (fixtures,policy)==before
    hold=[r for r in archive if r['screened_match_id'] is None]
    assert len(hold)==1 and hold[0]['original']['FT']=='3-0'
    assert hold[0]['source_observation_match_id'] not in {r['match_id'] for r in accepted}
    assert hold[0]['assessment']['effective_result_date'] is None


@pytest.mark.parametrize('mutation',['missing_hold','missing_interruption','wrong_hold_action','wrong_date',
                                     'wrong_kickoff','wrong_score','wrong_source_binding','missing_held_fixture'])
def test_missing_corrupt_or_misbound_approved_decisions_fail(mutation):
    fixtures,policy=data()
    if mutation=='missing_hold':policy['cases'].pop()
    if mutation=='missing_interruption':policy['cases'].pop(2)
    if mutation=='wrong_hold_action':policy['cases'][4]['action']='RETAIN'
    if mutation=='wrong_date':policy['cases'][2]['effective_result_date']='2004-12-12'
    if mutation=='wrong_kickoff':policy['cases'][3]['original_kickoff_date']='2023-12-09'
    if mutation=='wrong_score':policy['cases'][0]['approved_source_score']=[2,10]
    if mutation=='wrong_source_binding':fixtures[2]['original']['source_line']=90
    if mutation=='missing_held_fixture':fixtures.pop(4)
    with pytest.raises(ValueError):s.prepare(fixtures,policy,set())


@pytest.mark.parametrize('mutation',['date','team','score','id','duplicate','missing','league'])
def test_independent_output_checks_reject_corrupted_conversion(mutation):
    fixtures,policy=data();rows=standard(s.prepare(fixtures,policy,set()))
    if mutation=='date':rows[2]['date']='2004-12-12';rows[2]['match_id']=s.standard_id(rows[2])
    if mutation=='team':rows[0]['home_team']='Different Club'
    if mutation=='score':rows[0]['home_goals']=9
    if mutation=='id':rows[0]['match_id']='bad'
    if mutation=='duplicate':rows[-1]=deepcopy(rows[0])
    if mutation=='missing':rows.pop()
    if mutation=='league':rows[0]['league']='Primera Division'
    with pytest.raises(ValueError):s.check_and_partition(rows,fixtures,policy,set())


def test_both_resumptions_retain_completion_dates_and_original_kickoffs():
    fixtures,policy=data();rows=standard(s.prepare(fixtures,policy,set()))
    accepted,archive,_,_=s.check_and_partition(rows,fixtures,policy,set())
    for i,start,end in [(2,'2004-12-12','2005-01-05'),(3,'2023-12-10','2023-12-11')]:
        r=next(x for x in archive if x['source_fixture_id']==fixtures[i]['fixture_id'])
        assert r['original']['date']==end and r['assessment']['original_kickoff_date']==start
        assert r['archive_projection']['date']==r['assessment']['effective_result_date']==end
        assert r['screened_match_id'] in {x['match_id'] for x in accepted}
        assert not s.policy.known_strictly_before(end,start)
        assert not s.policy.known_strictly_before(end,end)


def test_new_unresolved_final_result_is_held_without_forcing_expected_count():
    fixtures,policy=data();fixtures[-1]['identified_final_outcome_status']='UNRESOLVED'
    rows=standard(s.prepare(fixtures,policy,set()))
    accepted,archive,counts,_=s.check_and_partition(rows,fixtures,policy,set())
    assert len(accepted)==4 and counts['unresolved']==2
    assert sum(r['screened_match_id'] is None for r in archive)==2


def test_unverified_scheduling_candidate_is_not_corrected_or_excluded():
    fixtures,policy=data();fixtures[-1].update(scheduling_status='UNRESOLVED',diagnostic_outlier=True)
    rows=standard(s.prepare(fixtures,policy,set()))
    accepted,archive,counts,_=s.check_and_partition(rows,fixtures,policy,set())
    candidate=next(r for r in archive if r['source_fixture_id']==fixtures[-1]['fixture_id'])
    assert counts['accepted']==5 and candidate['screened_match_id'] in {r['match_id'] for r in accepted}
    assert candidate['assessment']['historical_verification']=='UNVERIFIED'
    assert candidate['archive_projection']['date']==fixtures[-1]['original']['date']


@pytest.mark.parametrize('mutation',['negative','fraction','date','FT','pair_duplicate'])
def test_invalid_source_facts_are_not_silently_dropped(mutation):
    fixtures,policy=data();r=fixtures[-1]['original']
    if mutation=='negative':r['hg']='-1'
    if mutation=='fraction':r['hg']='0.5'
    if mutation=='date':r['date']='2020-02-30'
    if mutation=='FT':r['FT']='1-0'
    if mutation=='pair_duplicate':
        original=fixtures[0];r.update(home=original['original']['home'],away=original['original']['away'],date=original['original']['date']);fixtures[-1]['season']=original['season']
    with pytest.raises(ValueError):s.prepare(fixtures,policy,set())


def test_csv_header_order_and_missing_fields_are_explicit_failures():
    header=','.join(reversed(s.OUTPUT_COLUMNS))+'\n'
    with pytest.raises(ValueError):s.parse_standard(header.encode())
    raw=(','.join(s.OUTPUT_COLUMNS)+'\n'+'a,2020-01-01,La Liga,2019/2020,A,B,1\n').encode()
    with pytest.raises(ValueError):s.parse_standard(raw)


def test_shared_identity_uses_date_teams_season_league_but_not_score():
    fixtures,policy=data();row=s.prepare(fixtures,policy,set())[0]['fields'];before=s.standard_id(row)
    assert s.standard_id(dict(row,home_goals=99))==before
    assert s.standard_id(dict(row,date='2015-12-21'))!=before
    assert s.standard_id(dict(row,home_team='Other'))!=before


def test_original_logical_csv_record_bytes_and_accents_survive(tmp_path):
    file=tmp_path/'source.csv';raw='Date,home,notes\r\n2000-01-01,Málaga,"first\r\nsecond"\r\n'
    file.write_bytes(raw.encode())
    records=s.raw_records(tmp_path,['source.csv'])
    assert records['source.csv',3]['raw_record']=='2000-01-01,Málaga,"first\r\nsecond"\r\n'
    assert records['source.csv',3]['original_fields']['home']=='Málaga'
