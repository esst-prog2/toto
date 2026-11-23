"""Synthetic Phase7 exact projection, source archive, ID and chronology checks."""
from copy import deepcopy
import hashlib,json
import pytest
from scripts import standardize_primeira_liga_results as s
from scripts import decide_primeira_liga_policy as p
from test_primeira_liga_policy import row,case


def material(rs,hr=None,flags=None,refs=None):
    rs=deepcopy(rs);hr=deepcopy(hr or {});flags=deepcopy(flags or {});refs=deepcopy(refs or {})
    for r in rs:
        if r['source']==p.HIST_PATH:r['original_fields']={'tier':'1','division':'P1'}
        if r['audit_id']in hr:hr[r['audit_id']]['original']=deepcopy(r)
    overlaps={'seasons':[dict(comparisons=[dict(historical_id=rs[0]['audit_id'],modern_id=rs[1]['audit_id'])])]}if len(rs)==2 else{'seasons':[]}
    d=p.decide(rs,hr,flags,refs)
    return rs,[d],hr,flags,refs,overlaps


def plans_for(rs,hr=None,flags=None,refs=None):return s.prepare(*material(rs,hr,flags,refs))


def case_plans(kind):return plans_for(*case(kind))


def test_shared_importer_schema_season_and_independent_id(tmp_path):
    plans=plans_for([row()]);raw,result=s.convert(plans,tmp_path);parsed=s.parse_standard(raw)
    assert raw.splitlines()[0]==b'match_id,date,league,season,home_team,away_team,home_goals,away_goals'
    assert parsed==[plans[0]['projection']]and parsed[0]['season']=='2000/2001'
    r=parsed[0];expected=hashlib.sha256(json.dumps([r['league'],r['season'],r['date'],r['home_team'],r['away_team']],ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
    assert expected==r['match_id']==s.standard_id(r)and result['accepted']==1
    assert s.verify_subset(parsed,plans)==dict(screened=1,hold_out=0,not_played=0,unique_fixtures=1)


@pytest.mark.parametrize('year',range(2018,2025))
def test_all_seven_overlap_years_one_output_two_originals(year):
    plans=plans_for([row(year=year),row('m',year,True)])
    assert len(plans)==1 and len(plans[0]['originals'])==2
    assert plans[0]['decision']['selected_source_id']=='ordinary'


def test_modern2025_primary_retained():
    plan=plans_for([row(year=2025,modern=True)])[0]
    assert plan['projection']['season']=='2025/2026'
    assert plan['decision']['selection_reason']=='MODERN_2025_26_PRIMARY'


def test_missing_or_invalid_overlap_cannot_silently_duplicate():
    args=list(material([row(),row('m',modern=True)]));args[-1]={'seasons':[]}
    with pytest.raises(ValueError,match='correspondence'):s.prepare(*args)


@pytest.mark.parametrize('kind',['SANTA_PACOS','SANTA_BENFICA'])
def test_santa_completion_date_preserves_two_source_dates(kind):
    plans=case_plans(kind);a=plans[0]
    assert a['projection']['date']==p.SPECS[kind]['completion']
    assert len({r['date']for r in a['originals']})==2
    assert len(plans)==1
    assert not p._eligible(a['decision'],a['decision'],a['projection']['date'])


def test_santa_pacos_screened_but_chronologically_blocked():
    plan=case_plans('SANTA_PACOS')[0]
    assert plan['projection']is not None and plan['projection']['date']=='2020-02-02'
    assert not p._eligible(plan['decision'],plan['decision'],'2026-11-24')


@pytest.mark.parametrize('kind',['BELENENSES_BENFICA','BENFICA_SALGUEIROS'])
def test_exact_holdouts_no_projection_not_notplayed(kind):
    plans=case_plans(kind)
    assert plans[0]['projection']is None and plans[0]['decision']['disposition']=='HOLD_OUT'
    assert s.verify_subset([],plans)['hold_out']==1 and s.verify_subset([],plans)['not_played']==0


def test_feirense_only_single_approved_literal_interpretation(tmp_path):
    plan=case_plans('FEIRENSE_NACIONAL')[0]
    assert plan['originals'][0]['home']=='Feirense '
    assert plan['projection']['home_team']=='Feirense'
    raw,_=s.convert([plan],tmp_path);assert s.parse_standard(raw)[0]['home_team']=='Feirense'
    r=row(home=' Other ')
    with pytest.raises(ValueError):plans_for([r])


def test_nacional_no_fictitious_source_date_change():
    plan=case_plans('NACIONAL_BENFICA')[0]
    assert plan['projection']['date']=='2024-12-19'
    assert all(r['date']=='2024-12-19'for r in plan['originals'])
    assert plan['decision']['chronology']['actual_kickoff_date']=='2024-10-06'
    assert not p._eligible(plan['decision'],plan['decision'],'2024-10-07')
    assert p._eligible(plan['decision'],plan['decision'],'2024-12-20')


def test_leiria_score_participation_not_award():
    plan=case_plans('LEIRIA_FEIRENSE')[0]
    assert(plan['projection']['home_goals'],plan['projection']['away_goals'])==(0,4)
    assert'Eight Leiria starters'in plan['decision']['event_context']['participation_context']


def test_completed2019_season306_and_zero_notplayed(tmp_path):
    names=[f'Team{i}'for i in range(18)];plans=[]
    for i,h in enumerate(names):
        for j,a in enumerate(names):
            if i!=j:plans+=plans_for([row(f'{i}-{j}',2019,date='2020-07-26',home=h,away=a)])
    raw,_=s.convert(plans,tmp_path);report=s.verify_subset(s.parse_standard(raw),plans)
    assert report==dict(screened=306,hold_out=0,not_played=0,unique_fixtures=306)
    assert len({r['home_team']for r in s.parse_standard(raw)})==18


@pytest.mark.parametrize('year,clubs',[(2006,16),(2013,16),(2014,18)])
def test_season_specific_participant_pair_counts(year,clubs):
    plans=[]
    for i in range(clubs):
        for j in range(clubs):
            if i!=j:plans+=plans_for([row(f'{i}-{j}',year,home=f'T{i}',away=f'T{j}')])
    rows=sorted([x['projection']for x in plans],key=lambda r:tuple(r[k]for k in ['league','season','date','home_team','away_team']))
    assert s.verify_subset(rows,plans)['screened']==clubs*(clubs-1)


@pytest.mark.parametrize('year',[1990,1991,1992,1993,2026])
def test_unsourced_and_ongoing_seasons_rejected(year):
    with pytest.raises(ValueError):plans_for([row(year=year)])


@pytest.mark.parametrize('field,value',[('stage','PLAYOFF'),('stage','SECOND_TIER'),('date','2001-07-01'),('away','Home')])
def test_contamination_and_boundary_rejected(field,value):
    r=row();r[field]=value
    with pytest.raises(ValueError):plans_for([r])


def test_wrong_historical_division_or_tier_rejected():
    for key,value in [('division','P2'),('tier','2')]:
        args=list(material([row()]));args[0][0]['original_fields'][key]=value
        with pytest.raises(ValueError,match='tier/division'):s.prepare(*args)


@pytest.mark.parametrize('field,value',[('disposition','NOT_PLAYED'),('approved_values',{}),('decision_id','forged'),('chronology',{}),('source_observation_ids',[])])
def test_frozen_policy_tampering_rejected(field,value):
    args=list(material([row()]));args[1][0][field]=value
    with pytest.raises((ValueError,KeyError)):s.prepare(*args)


def test_global_alias_or_new_score_cannot_pass():
    for field,value in [('home','Renamed'),('hg','9')]:
        args=list(material([row()]));args[1][0]['approved_values'][field]=value
        with pytest.raises(ValueError):s.prepare(*args)


@pytest.mark.parametrize('mutation',['lost','duplicate','unknown'])
def test_observation_decision_accounting_rejected(mutation):
    args=list(material([row()]))
    if mutation=='lost':args[1]=[]
    if mutation=='duplicate':args[0].append(deepcopy(args[0][0]))
    if mutation=='unknown':args[1][0]['source_observation_ids']=['unknown']
    with pytest.raises(ValueError):s.prepare(*args)


def test_reverse_input_and_csv_roundtrip_identical(tmp_path):
    plans=plans_for([row(home='Z')])+plans_for([row('other',date='2000-08-19',home='Á')]);raw,_=s.convert(plans,tmp_path);reverse,_=s.convert(list(reversed(plans)),tmp_path)
    assert raw==reverse and s.serialize_csv(s.parse_standard(raw),s.OUTPUT_COLUMNS)==raw
    assert s.verify_subset(s.parse_standard(raw),plans)['screened']==2


@pytest.mark.parametrize('mutation',['missing','duplicate','score','id','league','column'])
def test_screened_exact_subset_guard(mutation):
    plans=plans_for([row()]);rows=[deepcopy(plans[0]['projection'])]
    if mutation=='missing':rows=[]
    if mutation=='duplicate':rows.append(deepcopy(rows[0]))
    if mutation=='score':rows[0]['away_goals']=8
    if mutation=='id':rows[0]['match_id']='forged'
    if mutation=='league':rows[0]['league']='Other'
    if mutation=='column':rows[0]['outcome']='H'
    with pytest.raises(ValueError):s.verify_subset(rows,plans)


def test_holdout_cannot_leak_through_csv():
    with pytest.raises(ValueError):s.verify_subset([plans_for([row()])[0]['projection']],case_plans('BELENENSES_BENFICA'))


@pytest.mark.parametrize('goal',['-1','1.0','01','١'])
def test_noncanonical_goals_rejected(goal):
    r=plans_for([row()])[0]['projection'];r['home_goals']=goal
    with pytest.raises(ValueError):s.parse_standard(s.serialize_csv([r],s.OUTPUT_COLUMNS))


def test_wrong_column_order_rejected():
    r=plans_for([row()])[0]['projection']
    with pytest.raises(ValueError):s.parse_standard(s.serialize_csv([r],tuple(reversed(s.OUTPUT_COLUMNS))))


def test_cross_competition_collision_rejected():
    r=plans_for([row()])[0]['projection']
    with pytest.raises(ValueError,match='collision'):s.verify_collisions([r],{r['match_id']})
    s.verify_collisions([r],{'different'})
    other=s.base.sha(json.dumps(['Ligue 1',r['season'],r['date'],r['home_team'],r['away_team']],ensure_ascii=False,separators=(',',':')).encode())
    assert other!=r['match_id']


def literal_plans(tmp_path):
    raw=b'header\nfixture literal\n';r=row();r['source_sha256']=s.base.sha(raw);r['physical_record_sha256']=s.base.sha(raw.splitlines(keepends=True)[1]);r['provenance']['git_blob_sha1']=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest();r['source_end_line']=2
    path=tmp_path/r['source'];path.parent.mkdir(parents=True);path.write_bytes(raw)
    return plans_for([r])


def test_archive_preserves_original_literal_provenance(tmp_path):
    plans=literal_plans(tmp_path);archive=s.archive_records(plans,tmp_path)
    assert archive[0]['original']==plans[0]['originals'][0]
    assert archive[0]['literal_original_record']=='fixture literal\n'
    assert s.verify_archive(archive,plans)==dict(archived=1,source_dispositions={'COMPLETED_RESULT_CANDIDATE':1},selected_for_csv=1)


@pytest.mark.parametrize('mutation',['bytes','blob','literal'])
def test_source_provenance_tampering_rejected(tmp_path,mutation):
    plans=literal_plans(tmp_path);r=plans[0]['originals'][0]
    if mutation=='bytes':(tmp_path/r['source']).write_bytes(b'changed')
    if mutation=='blob':r['provenance']['git_blob_sha1']='forged'
    if mutation=='literal':r['physical_record_sha256']='forged'
    with pytest.raises(ValueError):s.archive_records(plans,tmp_path)


@pytest.mark.parametrize('mutation',['lost','duplicate','original','fixture','decision','projection','selected'])
def test_archive_accounting_tampering_rejected(tmp_path,mutation):
    plans=literal_plans(tmp_path);records=s.archive_records(plans,tmp_path)
    if mutation=='lost':records=[]
    if mutation=='duplicate':records.append(deepcopy(records[0]))
    if mutation=='original':records[0]['original']['date']='2000-08-21'
    if mutation=='fixture':records[0]['fixture_id']='forged'
    if mutation=='decision':records[0]['decision_id']='forged'
    if mutation=='projection':records[0]['approved_standardized_values']=None
    if mutation=='selected':records[0]['selected_for_csv']=False
    with pytest.raises(ValueError):s.verify_archive(records,plans)


def test_same_day_future_unknown_availability_and_admin_rejection():
    ordinary=plans_for([row()])[0]
    assert ordinary['projection']is not None and not p._eligible(ordinary['decision'],ordinary['decision'],'2026-11-24')
    d=case_plans('SANTA_BENFICA')[0]['decision']
    assert not p._eligible(d,d,'2021-01-03')and not p._eligible(d,d,'2021-01-04')and p._eligible(d,d,'2021-01-05')
    fake=deepcopy(d);fake['chronology']['effective_result_availability_date']='2021-01-03'
    with pytest.raises(ValueError):p._eligible(d,fake,'2021-01-05')


def test_protected_archive_inventory_includes_reserved_match_ids_only():
    a='a'*64;b='b'*64;c='c'*64
    ids,counts=s.audit_match_ids(dict(records=[dict(match_id=a,screened_match_id=a,source_observation_match_id=b,candidate_match_id=c,audit_id='d'*64,fixture_id='e'*64,decision_id='f'*64),dict(screened_match_id=None)]))
    assert ids=={a,b,c}and counts['screened_match_id']==1


def test_protected_archive_checks_hash_and_keeps_unexported_id(tmp_path):
    archive=tmp_path/'prior_audit_archive.json';raw=s.base.encode(dict(records=[dict(source_observation_match_id='a'*64)]));archive.write_bytes(raw)
    (tmp_path/'protected_before.json').write_bytes(s.base.encode(dict(private={archive.name:s.base.sha(raw)})))
    ids,files=s.protected_audit_ids(tmp_path,tmp_path)
    assert ids=={'a'*64}and files[0]['unique_ids']==1
    archive.write_bytes(b'{}')
    with pytest.raises(ValueError,match='archive changed'):s.protected_audit_ids(tmp_path,tmp_path)
