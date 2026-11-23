"""Synthetic screened projection, complete archival and Phase6 integrity checks."""
from copy import deepcopy
import csv
import hashlib
import io
import json
import pytest
from scripts import standardize_eredivisie_results as s
from scripts import decide_eredivisie_policy as p
from test_eredivisie_policy import row,case


def material(rs,hs=None,c=None):
    rs=deepcopy(rs);hs=deepcopy(hs or {})
    for r in rs:
        if r['source'].startswith('jalapic/'):r['original_fields']={'tier':'1'}
        if r['audit_id'] in hs:hs[r['audit_id']]['original']=deepcopy(r)
    overlaps=[dict(matches=[dict(historical_id=rs[0]['audit_id'],modern_id=rs[1]['audit_id'])])] if len(rs)==2 else []
    d=p.decide(rs,hs,c)
    return rs,[d],hs,{c['id']:c} if c else {},overlaps


def plans_for(rs,hs=None,c=None):
    return s.prepare(*material(rs,hs,c))


def test_shared_importer_exact_schema_and_algorithm(tmp_path):
    plans=plans_for([row()]);raw,summary=s.convert(plans,tmp_path);parsed=s.parse_standard(raw)
    assert raw.splitlines()[0]==b'match_id,date,league,season,home_team,away_team,home_goals,away_goals'
    assert parsed==[plans[0]['projection']] and parsed[0]['league']=='Eredivisie'
    assert parsed[0]['match_id']==s.standard_id(parsed[0]) and summary['accepted']==1
    assert s.verify_subset(parsed,plans)==dict(screened=1,hold_out=0,not_played=0,unique_fixtures=1)


def test_one_output_for_two_preserved_observations():
    rs=[row(),row('modern',source='openfootball/season')];plans=plans_for(rs)
    assert len(plans)==1 and len(plans[0]['originals'])==2
    assert s.verify_subset([plans[0]['projection']],plans)['screened']==1


def test_unapproved_overlap_link_fails():
    args=list(material([row(),row('modern',source='openfootball/season')]));args[-1]=[]
    with pytest.raises(ValueError,match='correspondence'):s.prepare(*args)


def test_extra_overlap_endpoint_fails():
    args=list(material([row(),row('modern',source='openfootball/season')]));args[-1][0]['matches'][0]['modern_id']='missing'
    with pytest.raises(KeyError):s.prepare(*args)


def test_groningen_only_approved_date_changes():
    rs,hs,c=case('GRONINGEN_AJAX');plans=plans_for(rs,hs,c);pr=plans[0]['projection']
    assert pr['date']=='2023-05-16' and (pr['home_goals'],pr['away_goals'])==(2,3)
    assert {r['date'] for r in plans[0]['originals']}=={'2023-05-14','2023-05-16'}
    assert not p._eligible(plans[0]['decision'],plans[0]['decision'],'2023-05-16')


def test_nec_final_score_not_intermediate_score():
    rs,hs,c=case('NEC_VITESSE');plans=plans_for(rs,hs,c)
    assert (plans[0]['projection']['home_goals'],plans[0]['projection']['away_goals'])==(1,3)
    assert {r['FT'] for r in plans[0]['originals']}=={'1-3','1-2'}


@pytest.mark.parametrize('kind',['NAC_HEERENVEEN','FEYENOORD_VVV','VITESSE_SPARTA'])
def test_all_three_holdouts_have_no_csv_projection(kind):
    rs,hs,c=case(kind);plans=plans_for(rs,hs,c)
    assert plans[0]['projection'] is None and plans[0]['decision']['disposition']=='HOLD_OUT'
    assert s.verify_subset([],plans)['hold_out']==1


def test_nac_original_null_never_becomes_not_played_or_supplemented():
    rs,hs,c=case('NAC_HEERENVEEN');plan=plans_for(rs,hs,c)[0]
    assert plan['originals'][0]['FT'] is None and plan['originals'][0]['annotation']=='[cancelled]'
    assert plan['decision']['documentary_values']['FT']=='2-0' and plan['projection'] is None
    assert not plan['decision']['supplement_assessment']['approved']


@pytest.mark.parametrize('kind',['AJAX_FEYENOORD','RKC_AJAX','AZ_NEC','HERACLES_GRONINGEN'])
def test_existing_completion_representation_once(kind):
    rs,hs,c=case(kind);plans=plans_for(rs,hs,c)
    assert len(plans)==1 and plans[0]['projection']['date']==p.CASES[kind][2]
    assert len(plans[0]['originals'])==2
    assert all(r['date']==plans[0]['projection']['date'] for r in plans[0]['originals'])


def test_exact_74_unplayed_slots_and_absent_historical_representation():
    plans=[]
    for i in range(74):
        r=row(str(i),'2019/2020','openfootball/season','2020-04-01',None,home='H'+str(i));plans.extend(plans_for([r]))
    assert s.verify_subset([],plans)['not_played']==74
    assert all(len(p['originals'])==1 and p['originals'][0]['FT'] is None for p in plans)


@pytest.mark.parametrize('flag',['WIDE_ROUND','SOURCE_ORDER_REVERSAL','UNUSUAL_SCORE'])
def test_context_flag_kept_without_automatic_exclusion(flag):
    plan=plans_for([row(flags=[flag])])[0]
    assert plan['projection'] is not None and plan['originals'][0]['structural']['flags']==[flag]


def test_unknown_availability_rejected_despite_csv_inclusion():
    plan=plans_for([row()])[0];assert plan['projection'] is not None
    assert not p._eligible(plan['decision'],plan['decision'],'2026-11-23')


@pytest.mark.parametrize('field,value',[('disposition','NOT_PLAYED'),('decision_id','forged'),('chronology',{}),('source_observation_ids',[]),('approved_values',{})])
def test_altered_decision_rejected(field,value):
    args=list(material([row()]));args[1][0][field]=value
    with pytest.raises((ValueError,KeyError,TypeError)):s.prepare(*args)


@pytest.mark.parametrize('mutation',['missing','duplicate','unknown'])
def test_source_binding_inventory_rejection(mutation):
    args=list(material([row()]))
    if mutation=='missing':args[1]=[]
    if mutation=='duplicate':args[0].append(deepcopy(args[0][0]))
    if mutation=='unknown':args[1][0]['source_observation_ids']=['missing']
    with pytest.raises(ValueError):s.prepare(*args)


@pytest.mark.parametrize('field,value',[('season','1989/1990'),('season','2026/2027'),('stage','PLAYOFF'),('date','2001-07-01'),('home',' H'),('away','H')])
def test_scope_and_identity_rejection(field,value):
    r=row();r[field]=value
    with pytest.raises(ValueError):plans_for([r])


def test_wrong_historical_tier_rejected():
    args=list(material([row()]));args[0][0]['original_fields']['tier']='2'
    with pytest.raises(ValueError,match='tier'):s.prepare(*args)


def test_global_alias_or_reserve_relabel_not_allowed():
    args=list(material([row(home='Jong H')]));args[1][0]['approved_values']['home']='H'
    with pytest.raises(ValueError):s.prepare(*args)


def test_stable_sorting_and_reversed_input_serialization(tmp_path):
    a=plans_for([row('a',home='Z')]);b=plans_for([row('b',date='2000-08-02',home='B')]);raw,_=s.convert(a+b,tmp_path);reverse,_=s.convert(b+a,tmp_path)
    assert raw==reverse and s.verify_subset(s.parse_standard(raw),a+b)['screened']==2


def test_unicode_labels_preserved(tmp_path):
    plans=plans_for([row(home='Club é',away='Club ’65')]);raw,_=s.convert(plans,tmp_path)
    assert s.parse_standard(raw)[0]['home_team']=='Club é' and s.parse_standard(raw)[0]['away_team']=='Club ’65'


def test_league_participates_in_id():
    r=plans_for([row()])[0]['projection'];other=s.base.sha(json.dumps(['Ligue 1',r['season'],r['date'],r['home_team'],r['away_team']],ensure_ascii=False,separators=(',',':')).encode())
    assert s.standard_id(r)!=other


@pytest.mark.parametrize('mutation',['missing','duplicate','score','id','league','extra_column'])
def test_screened_exact_subset_guards(mutation):
    plans=plans_for([row()]);rows=[deepcopy(plans[0]['projection'])]
    if mutation=='missing':rows=[]
    if mutation=='duplicate':rows.append(deepcopy(rows[0]))
    if mutation=='score':rows[0]['away_goals']=8
    if mutation=='id':rows[0]['match_id']='wrong'
    if mutation=='league':rows[0]['league']='Other'
    if mutation=='extra_column':rows[0]['result']='H'
    with pytest.raises(ValueError):s.verify_subset(rows,plans)


def test_holdout_cannot_leak_into_screened_output():
    rs,hs,c=case('NAC_HEERENVEEN');plans=plans_for(rs,hs,c)
    fake=plans_for([row()])[0]['projection']
    with pytest.raises(ValueError):s.verify_subset([fake],plans)


@pytest.mark.parametrize('goals',['-1','1.0','01','١'])
def test_bad_csv_goal_serialization(goals):
    r=plans_for([row()])[0]['projection'];r['home_goals']=goals
    with pytest.raises(ValueError):s.parse_standard(s.serialize_csv([r],s.OUTPUT_COLUMNS))


def test_wrong_schema_order_rejected():
    r=plans_for([row()])[0]['projection']
    with pytest.raises(ValueError):s.parse_standard(s.serialize_csv([r],tuple(reversed(s.OUTPUT_COLUMNS))))


def literal_plan(tmp_path):
    raw=b'header\noriginal fixture row\n';r=row();r['original_fields']={'tier':'1'}
    r.update(source_sha256=s.base.sha(raw),physical_record_sha256=s.base.sha(raw.splitlines(keepends=True)[1]))
    r['provenance']['git_blob_sha1']=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    path=tmp_path/r['source'];path.parent.mkdir(parents=True);path.write_bytes(raw)
    return plans_for([r])


def test_full_archive_preserves_exact_original_and_physical_bytes(tmp_path):
    plans=literal_plan(tmp_path);records=s.archive_records(plans,tmp_path)
    assert records[0]['original']==plans[0]['originals'][0]
    assert records[0]['literal_original_record']=='original fixture row\n'
    assert s.verify_archive(records,plans)['archived']==1


@pytest.mark.parametrize('mutation',['source_bytes','blob','literal_hash'])
def test_physical_provenance_tamper_rejected(tmp_path,mutation):
    plans=literal_plan(tmp_path);r=plans[0]['originals'][0]
    if mutation=='source_bytes':(tmp_path/r['source']).write_bytes(b'changed\n')
    if mutation=='blob':r['provenance']['git_blob_sha1']='wrong'
    if mutation=='literal_hash':r['physical_record_sha256']='wrong'
    with pytest.raises(ValueError):s.archive_records(plans,tmp_path)


@pytest.mark.parametrize('mutation',['lost','duplicated','original','fixture','decision','projection','selection'])
def test_archive_accounting_and_bindings_rejected(tmp_path,mutation):
    plans=literal_plan(tmp_path);records=s.archive_records(plans,tmp_path)
    if mutation=='lost':records=[]
    if mutation=='duplicated':records.append(deepcopy(records[0]))
    if mutation=='original':records[0]['original']['FT']='9-9'
    if mutation=='fixture':records[0]['fixture_id']='missing'
    if mutation=='decision':records[0]['decision_id']='wrong'
    if mutation=='projection':records[0]['approved_standardized_values']=None
    if mutation=='selection':records[0]['selected_for_csv']=False
    with pytest.raises(ValueError):s.verify_archive(records,plans)


def test_whole_csv_serialization_roundtrip(tmp_path):
    plans=plans_for([row()]);raw,_=s.convert(plans,tmp_path)
    assert s.serialize_csv(s.parse_standard(raw),s.OUTPUT_COLUMNS)==raw
