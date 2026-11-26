"""Synthetic shared-schema, exact-subset, naming and rematch safeguards."""
from copy import deepcopy
import csv
import hashlib
import io
import json
import pytest
from scripts import standardize_belgian_pro_league_results as s
from scripts import decide_belgian_pro_league_policy as p


def original(sid='a', **changes):
    row=dict(audit_id=sid,source='jalapic/test.csv',source_line=1,season='2021/2022',
             stage='REGULAR_SEASON',home='Club Brugge',away='Cercle Brugge',date='2021-07-27',
             FT='0-1',annotation='',physical_record_sha256='raw')
    row.update(changes);return row


def decision(sid='a', **changes):
    o=original(sid,**changes)
    event=p.make_event([dict(kind='CSV_TXT',binding=o)],{})
    return p.adjudicate(event)


def table_for(d):
    return {(d['season'],'jalapic/test.csv',name):dict(season=d['season'],source='jalapic/test.csv',
        original=name,canonical=name,basis='SYNTHETIC_SOURCE_IDENTITY',scope='SOURCE_AND_SEASON_ONLY') for name in (d['home'],d['away'])}


def test_shared_schema_exact_order():
    assert s.OUTPUT_COLUMNS==('match_id','date','league','season','home_team','away_team','home_goals','away_goals')


def test_id_is_established_compact_json_sha256():
    d=decision();r,_=s.project(d,table_for(d))
    expected=hashlib.sha256(json.dumps(['Belgian Pro League','2021/2022','2021-07-27','Club Brugge','Cercle Brugge'],ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
    assert r['match_id']==expected and len(expected)==64


def test_projection_is_exact_and_does_not_mutate_decision():
    d=decision();before=deepcopy(d);r,b=s.project(d,table_for(d))
    assert tuple(r)==s.OUTPUT_COLUMNS
    assert r['home_goals']==0 and r['away_goals']==1
    assert r['date']=='2021-07-27' and r['league']=='Belgian Pro League'
    assert len(b)==2 and d==before


@pytest.mark.parametrize('disposition',['HOLD_OUT','NOT_PLAYED','OUT_OF_SCOPE'])
def test_noninclude_never_projects_even_if_reported_score_exists(disposition):
    d=decision();d.update(disposition=disposition,accepted_score=None,chosen_match_date=None,accepted_outcome=None)
    assert s.project(d,{})==(None,[])


def test_resumption_uses_approved_kickoff_and_retains_completion():
    d=decision();d.update(case_id='beerschot_cercle_resumed',kickoff_date='2021-07-24',chosen_match_date='2021-07-24',completion_date='2021-07-27')
    r,_=s.project(d,table_for(d))
    assert r['date']=='2021-07-24' and d['original_fixture_date']=='2021-07-27' and d['completion_date']=='2021-07-27'


def test_judgment_date_substitution_rejected():
    d=decision();d['chosen_match_date']='2022-03-08'
    with pytest.raises(ValueError,match='kickoff'):s.project(d,table_for(d))


def test_malformed_outcome_rejected():
    d=decision();d['accepted_outcome']='H'
    with pytest.raises(ValueError,match='outcome'):s.project(d,table_for(d))


@pytest.mark.parametrize('season',['1990/1991','2026/2027','2021/22'])
def test_unapproved_season_or_noncanonical_format_fails(season):
    d=decision();d['season']=season
    with pytest.raises(ValueError):s.project(d,table_for(d))


def test_date_outside_season_fails():
    d=decision();d['chosen_match_date']=d['kickoff_date']=d['original_fixture_date']='2023-01-01'
    with pytest.raises(ValueError,match='outside season'):s.project(d,table_for(d))


def test_unknown_name_binding_is_exact_blocker():
    d=decision()
    with pytest.raises(ValueError,match=d['decision_id']):s.project(d,{})


def test_city_alias_cannot_merge_club_and_cercle():
    d=decision();t=table_for(d)
    for v in t.values():v['canonical']='Brugge'
    with pytest.raises(ValueError,match='collapsed'):s.project(d,t)


def test_conflicting_cross_source_canonical_sides_fail():
    d=decision();extra=deepcopy(d['representations'][0]);extra['binding'].update(source='openfootball/test',audit_id='b')
    d['representations'].append(extra);t=table_for(d)
    for side in ['home','away']:
        n=d[side];t[d['season'],'openfootball/test',n]=dict(t[d['season'],'jalapic/test.csv',n],canonical='Other '+n)
    with pytest.raises(ValueError,match='Conflicting canonical'):s.project(d,t)


def test_legitimate_playoff_rematch_retains_distinct_shared_ids():
    a=decision();b=decision('b',stage='CHAMPIONSHIP',date='2022-05-01')
    prepared=s.plans([a,b],table_for(a))
    assert len({x['projection']['match_id'] for x in prepared})==2
    assert {x['decision']['stage'] for x in prepared}=={'REGULAR_SEASON','CHAMPIONSHIP'}


def test_same_date_same_teams_across_stages_cannot_be_silently_collapsed():
    a=decision();b=decision('b',stage='CHAMPIONSHIP')
    with pytest.raises(ValueError,match='cannot be represented'):s.plans([a,b],table_for(a))


def test_duplicate_include_event_fails_before_serialization():
    a=decision()
    with pytest.raises(ValueError,match='cannot be represented'):s.plans([a,a],table_for(a))


def test_shared_importer_accepts_rematches_and_preserves_all_facts(tmp_path):
    a=decision();b=decision('b',stage='CHAMPIONSHIP',date='2022-05-01');prepared=s.plans([b,a],table_for(a))
    selected=[p['projection'] for p in prepared]
    raw,summary=s.convert(selected,tmp_path);rows=s.parse_standard(raw)
    assert summary==dict(total=2,accepted=2,rejected=0,duplicates=0,fixtures=0,conflicts=0)
    assert s.verify_subset(rows,prepared)['rows']==2
    assert s.independent_registry_check(rows,[a,b],table_for(a))['exact_subset']
    s.validate_public_loader(raw,rows)
    assert raw.endswith(b'\n') and b'\r' not in raw


def test_missing_approved_row_detected():
    d=decision();prepared=s.plans([d],table_for(d))
    with pytest.raises(ValueError,match='Missing'):s.verify_subset([],prepared)


def test_duplicate_csv_row_detected():
    d=decision();prepared=s.plans([d],table_for(d));r=prepared[0]['projection']
    with pytest.raises(ValueError,match='duplicate'):s.verify_subset([r,r],prepared)


@pytest.mark.parametrize('field,value',[('date','2022-01-01'),('home_goals',3),('away_team','Unknown'),('league','Other')])
def test_unapproved_fact_changes_fail_independent_registry_check(field,value):
    d=decision();r,_=s.project(d,table_for(d));r[field]=value
    with pytest.raises(ValueError,match='Independent'):s.independent_registry_check([r],[d],table_for(d))


def test_independent_checker_rejects_excluded_output():
    d=decision();r,_=s.project(d,table_for(d));d['disposition']='HOLD_OUT'
    with pytest.raises(ValueError,match='Independent'):s.independent_registry_check([r],[d],table_for(d))


def test_sorting_is_deterministic_and_verified():
    a=decision();b=decision('b',date='2022-05-01');prepared=s.plans([a,b],table_for(a))
    rows=[p['projection'] for p in reversed(prepared)]
    with pytest.raises(ValueError,match='ordering'):s.verify_subset(rows,prepared)


@pytest.mark.parametrize('goals',['-1','1.0','01','', 'NaN'])
def test_noncanonical_goal_serialization_fails(goals):
    d=decision();r,_=s.project(d,table_for(d));r['home_goals']=goals
    raw=s.serialize_csv([r],s.OUTPUT_COLUMNS)
    with pytest.raises(ValueError,match='goals'):s.parse_standard(raw)


def test_wrong_column_order_fails():
    raw=s.serialize_csv([],tuple(reversed(s.OUTPUT_COLUMNS)))
    with pytest.raises(ValueError,match='schema'):s.parse_standard(raw)


def test_extra_column_or_row_width_fails():
    d=decision();r,_=s.project(d,table_for(d));raw=s.serialize_csv([r],s.OUTPUT_COLUMNS)
    with pytest.raises(ValueError,match='width'):s.parse_standard(raw.rstrip(b'\n')+b',extra\n')


def test_name_table_uses_actual_declared_season_not_misplaced_path():
    h=original(season='2020/2021');observed=dict(historical=[h],modern={'2021-22/be1.txt':[]})
    links={'2021-22/be1.txt':dict(mapping=[dict(modern='Club Brugge KV',historical='Club Brugge')])}
    structure=dict(modern_sources={'2021-22/be1.txt':dict(declared_season='2020/2021')})
    table=s.name_table(observed,links,structure,dict(mapping=[]))
    assert table['2020/2021','openfootball/belgium/2021-22/be1.txt','Club Brugge KV']['canonical']=='Club Brugge'
    assert not any(key[0]=='2021/2022' for key in table if key[1].startswith('openfootball'))


def test_no_unsupported_cross_season_alias():
    table=s.name_table(dict(historical=[original()],modern={}),{},dict(modern_sources={}),dict(mapping=[]))
    assert ('2020/2021','jalapic/test.csv','Club Brugge') not in table


def test_many_to_one_mapping_rejected():
    observed=dict(historical=[original()],modern={})
    links={'x':dict(mapping=[dict(modern='Club',historical='Brugge'),dict(modern='Cercle',historical='Brugge')])}
    with pytest.raises(ValueError,match='Many-to-one'):
        s.name_table(observed,links,dict(modern_sources={'x':dict(declared_season='2021/2022')}),dict(mapping=[]))


def test_ambiguous_mapping_rejected():
    observed=dict(historical=[],modern={});links={'x':dict(mapping=[dict(modern='Club',historical='A'),dict(modern='Club',historical='B')])}
    with pytest.raises(ValueError,match='Ambiguous'):
        s.name_table(observed,links,dict(modern_sources={'x':dict(declared_season='2021/2022')}),dict(mapping=[]))


def test_modern_only_2025_names_preserved_without_global_guess():
    r=original(season='2025/2026',source='openfootball/belgium/2025-26/be1.txt')
    table=s.name_table(dict(historical=[],modern={'2025-26/be1.txt':[r]}),{},dict(modern_sources={}),dict(mapping=[]))
    assert table[r['season'],r['source'],r['home']]['canonical']==r['home']
