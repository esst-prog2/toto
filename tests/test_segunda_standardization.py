"""Synthetic source/subset/archive guards; never require private data or network."""
from copy import deepcopy

import pytest

from scripts import standardize_segunda_results as s
from tests.test_segunda_policy import policy, ordinary


def data():
    approved=policy();records=[deepcopy(c['original']) for c in approved['cases']]
    r=ordinary();r['source_fixture_id']=s.policy.review.structural.source_id(r['source_file'],r['source_sha256'],r['source_line'])
    records.append(r)
    return records,approved


def projected(plans):
    return sorted((p['projection'] for p in plans if p['projection'] is not None),
                  key=lambda r:(r['league'],r['season'],r['date'],r['home_team'],r['away_team']))


def test_shared_importer_exact_schema_ids_subset_and_order_invariance(tmp_path):
    records,approved=data();before=deepcopy((records,approved));plans=s.prepare(records,approved,{})
    raw,summary=s.convert(plans,tmp_path);rev,_=s.convert(list(reversed(plans)),tmp_path)
    assert raw==rev and raw.decode().splitlines()[0]==','.join(s.OUTPUT_COLUMNS)
    rows=s.parse_standard(raw);_,counts=s.check_partition(rows,records,approved,{})
    assert counts==dict(archived=35,screened=13,excluded=0,hold_out=22,reus_unresolved_holds=21,deportivo_approved_conservative_holds=1,supplemented=9)
    assert summary==dict(total=13,accepted=13,rejected=0,duplicates=0,fixtures=0,conflicts=0)
    assert rows==projected(plans) and (records,approved)==before
    assert len({r['match_id'] for r in rows})==13 and all(r['league']=='Segunda División' for r in rows)


@pytest.mark.parametrize('line', [745,747,748,749,750,751,752,753,754])
def test_all_supplements_keep_source_null_and_use_approved_values(line):
    records,approved=data();plans=s.prepare(records,approved,{})
    found=next(p for p in plans if p['original']['season']=='2024/2025' and p['original']['source_line']==line)
    assert found['original']['FT'] is None and found['original']['hg'] is None and found['original']['ag'] is None
    expected=next(x for x in s.policy.SUPPLEMENTS if x[0]==line)
    assert (found['projection']['home_goals'],found['projection']['away_goals'])==s.policy.score(expected[4])
    assert found['projection']['date']==expected[1]


@pytest.mark.parametrize('line', s.policy.AWARD_LINES)
def test_every_reus_award_has_no_screened_projection(line):
    records,approved=data();plans=s.prepare(records,approved,{})
    found=next(p for p in plans if p['original']['season']=='2018/2019' and p['original']['source_line']==line)
    assert found['projection'] is None
    assert found['original']['annotation']=='[awarded]' and found['original']['FT'] in {'0-1','1-0'}
    assert found['assessment']['effective_result_date'] is None


def test_both_special_scheduling_decisions_and_high_scores():
    records,approved=data();plans=s.prepare(records,approved,{})
    found={(p['original']['season'],p['original']['source_line']):p for p in plans}
    rayo=found['2019/2020',346];dep=found['2019/2020',722]
    assert rayo['decision']['event_dates']['kickoff']=='2019-12-15'
    assert rayo['projection']['date']=='2020-06-10'
    assert dep['original']['FT']=='2-1' and dep['projection'] is None
    assert dep['decision']['event_dates']['completion']=='2020-08-07'
    for line,score in [(82,(6,4)),(291,(6,6))]:
        r=found['2014/2015',line]['projection'];assert (r['home_goals'],r['away_goals'])==score


@pytest.mark.parametrize('mutation',['missing_reus','missing_supplement','duplicate_source','same_fixture_other_line','wrong_audit_id','wrong_source_hash','wrong_original','unknown_missing_score','new_unresolved','season','out_of_season'])
def test_source_scope_and_policy_fail_closed(mutation):
    records,approved=data();r=records[-1]
    if mutation=='missing_reus':records=[x for x in records if not(x['season']=='2018/2019' and x['source_line']==376)]
    if mutation=='missing_supplement':records=[x for x in records if x['source_line']!=745]
    if mutation=='duplicate_source':records.append(deepcopy(r))
    if mutation=='same_fixture_other_line':
        n=deepcopy(r);n['source_line']=1000;n['source_fixture_id']=s.policy.review.structural.source_id(n['source_file'],n['source_sha256'],1000);records.append(n)
    if mutation=='wrong_audit_id':r['source_fixture_id']='bad'
    if mutation=='wrong_source_hash':r['source_sha256']='0'*64
    if mutation=='wrong_original':records[0]['date']='2014-01-01'
    if mutation=='unknown_missing_score':r.update(FT=None,hg=None,ag=None)
    if mutation=='new_unresolved':r['identified_final_outcome_status']='UNRESOLVED'
    if mutation=='season':r['season']='2025/2026'
    if mutation=='out_of_season':r['date']='2016-01-01'
    with pytest.raises(ValueError):s.prepare(records,approved,{})


@pytest.mark.parametrize('mutation',['missing','duplicate','score','team','date','id','league','order','hold_leak'])
def test_independent_subset_check_detects_corrupted_output(mutation):
    records,approved=data();rows=deepcopy(projected(s.prepare(records,approved,{})))
    if mutation=='missing':rows.pop()
    if mutation=='duplicate':rows.append(deepcopy(rows[0]))
    if mutation=='score':rows[0]['home_goals']+=1
    if mutation=='team':rows[0]['home_team']='Parent club';rows[0]['match_id']=s.standard_id(rows[0])
    if mutation=='date':rows[0]['date']='2014-01-01';rows[0]['match_id']=s.standard_id(rows[0])
    if mutation=='id':rows[0]['match_id']='bad'
    if mutation=='league':rows[0]['league']='La Liga'
    if mutation=='order':rows.reverse()
    if mutation=='hold_leak':
        r=next(r for r in records if r['season']=='2018/2019')
        row=dict(date=r['date'],league=s.LEAGUE,season=r['season'],home_team=r['home'],away_team=r['away'],home_goals=int(r['hg']),away_goals=int(r['ag']))
        row['match_id']=s.standard_id(row);rows.append({k:row[k] for k in s.OUTPUT_COLUMNS})
    with pytest.raises(ValueError):s.check_partition(rows,records,approved,{})


def test_reserves_are_never_merged_and_proxy_is_not_training_clearance():
    records,approved=data();r=records[-1];r['home']='FC Barcelona B';r['away']='FC Barcelona'
    plans=s.prepare(records,approved,{});row=plans[-1]['projection']
    assert row['home_team']=='FC Barcelona B' and row['away_team']=='FC Barcelona'
    a=plans[-1]['assessment'];a.update(model_training_suitability='CLEARED',licensing_clearance='CLEARED')
    assert not s.policy.training_allowed(a,'2030-01-01')
    rayo=next(p for p in plans if p['original']['season']=='2019/2020' and p['original']['source_line']==346)
    a=rayo['assessment'];a.update(model_training_suitability='CLEARED',licensing_clearance='CLEARED')
    assert not s.policy.training_allowed(a,'2020-06-10')
    assert not s.policy.training_allowed(a,'2019-12-16')


@pytest.mark.parametrize('mutation',['columns','missing','extra','negative','leading_zero','invalid_utf8'])
def test_malformed_screened_csv_rejected(mutation):
    rows=projected(s.prepare(*data(),{}));raw=s.serialize_csv(rows,s.OUTPUT_COLUMNS)
    text=raw.decode()
    if mutation=='columns':raw=text.replace('match_id,date','date,match_id',1).encode()
    if mutation=='missing':raw=text.replace(',6,4\n',',,4\n',1).encode()
    if mutation=='extra':raw=(text+'extra,fields\n').encode()
    if mutation=='negative':raw=text.replace(',6,4\n',',-6,4\n',1).encode()
    if mutation=='leading_zero':raw=text.replace(',6,4\n',',06,4\n',1).encode()
    if mutation=='invalid_utf8':raw=b'\xff'+raw
    with pytest.raises((ValueError,UnicodeDecodeError)):s.parse_standard(raw)


def test_phase7_conditional_hold_approval_cannot_be_missing_or_broadened(monkeypatch):
    approved=policy();digest=s.base.sha(s.base.encode(approved));monkeypatch.setattr(s,'POLICY_SHA',digest)
    a=dict(phase=7,approval='USER_APPROVED_PHASE7',approved_phase6_policy_sha256=digest,approved_conditional_hold_ids=approved['conditional_hold_ids'])
    s.validate_approval(a,approved)
    for mutation in ['approval','ids','hash']:
        wrong=deepcopy(a)
        if mutation=='approval':wrong['approval']='PROPOSED'
        if mutation=='ids':wrong['approved_conditional_hold_ids']=[]
        if mutation=='hash':wrong['approved_phase6_policy_sha256']='0'*64
        with pytest.raises(ValueError):s.validate_approval(wrong,approved)


def test_output_preflight_refuses_existing_artifacts(tmp_path):
    paths=[tmp_path/n for n in s.NAMES];paths[-1].write_bytes(b'original')
    with pytest.raises(FileExistsError):s.check_overwrite(paths)
    assert paths[-1].read_bytes()==b'original' and not any(p.exists() for p in paths[:-1])


def test_standard_ids_include_competition_identity():
    r=projected(s.prepare(*data(),{}))[0]
    assert s.standard_id(r)==r['match_id']
    import json,hashlib
    parent=hashlib.sha256(json.dumps(['La Liga',r['season'],r['date'],r['home_team'],r['away_team']],ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
    assert parent!=r['match_id']
