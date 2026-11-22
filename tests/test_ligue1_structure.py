"""Independent structural grammar, classification and review-queue safeguards."""
from copy import deepcopy
import csv
import io
from unittest.mock import patch

import pytest

from scripts import validate_ligue1_structure as s


def csv_raw(**changes):
    row=dict(Date='1990-08-01',Season='1990',home='Alpha',visitor='Béta',FT='0-1',hgoal='0',vgoal='1',division='1',tier='1',totgoal='1',goaldif='-1',result='D')
    row.update(changes);f=io.StringIO(newline='');w=csv.DictWriter(f,fieldnames=list(row));w.writeheader();w.writerow(row);return f.getvalue().encode()


def historical(**changes):
    raw=csv_raw(**changes);return s.read_csv(raw,'historical.csv',s.base.sha(raw))[0]


def text(body,year=2014):
    raw=(f'= French Ligue 1 {year}/{str(year+1)[-2:]}\n'+body).encode()
    return s.read_text(raw,year,'season.txt',s.base.sha(raw))[0]


def fixture(body='Alpha v Béta  1-0 (0-0)'):
    return text('▪ Matchday 1\nFri Aug 8 2014\n'+body+'\n')[0]


def assessed(r):
    r['assessment']=s.inspect_record(r);return r


def test_csv_independent_parser_preserves_literal_fields_utf8_and_physical_hash():
    raw=csv_raw();r=s.read_csv(raw,'h.csv',s.base.sha(raw))[0]
    assert r['source_fields']['result']=='D' and r['away']=='Béta' and r['source_line']==2
    assert r['raw_line_sha256']==s.base.sha(raw.splitlines(keepends=True)[1])
    assert r['audit_id']==s.source_id('h.csv',s.base.sha(raw),2)


def test_csv_multiline_record_binding_covers_entire_physical_record():
    raw=csv_raw(home='Alpha\nSecond line');r=s.read_csv(raw,'h.csv',s.base.sha(raw))[0]
    assert r['source_start_line']==2 and r['source_line']==3
    assert r['raw_line_sha256']==s.base.sha(b''.join(raw.splitlines(keepends=True)[1:3]))
    assert 'INVALID_TEAM_LABEL' in s.inspect_record(r)['malformed_reasons']


def test_source_ids_change_with_path_hash_or_line():
    ids={s.source_id('a','sha',1),s.source_id('b','sha',1),s.source_id('a','other',1),s.source_id('a','sha',2)}
    assert len(ids)==4 and all(x.startswith('ligue1:') for x in ids)


def test_csv_wrong_schema_shape_and_unassignable_season_fail_explicitly():
    with pytest.raises(ValueError,match='schema'):s.read_csv(b'Date,Season\n','x','sha')
    with pytest.raises(ValueError,match='shape'):s.read_csv(csv_raw()+b'broken,row\n','x','sha')
    with pytest.raises(ValueError,match='season'):historical(Season='unknown')


def test_text_parser_does_not_call_feasibility_or_inventory_parsers():
    with patch.object(s.metadata,'parse_text',side_effect=AssertionError('Must be independent')):
        r=fixture();assert r['FT']=='1-0' and r['HT']=='0-0' and r['date']=='2014-08-08'


def test_score_middle_multiline_scorers_and_newline_binding():
    rows=text("▪ Matchday 1\nFri Aug 8 2014\n20:30  Alpha  2-1 (1-0)  Béta\n (Scorer 4',\n Other 50')\n")
    assert len(rows)==1 and rows[0]['source_kickoff_time']=='20:30' and rows[0]['FT']=='2-1'


def test_cancelled_is_null_not_draw_and_future_policy_undecided():
    r=fixture('Alpha v Béta [cancelled]');a=s.inspect_record(r)
    assert r['FT'] is r['hg'] is r['ag'] is None
    assert a['classification']=='CANCELLED_UNSCORED' and a['goal_derived_outcome'] is None
    assert a['chronology']['scheduled_date']=='2014-08-08' and a['chronology']['effective_result_availability'] is None


def test_unexplained_missing_score_is_not_a_cancelled_slot():
    a=s.inspect_record(fixture('Alpha v Béta'))
    assert a['classification']=='INCOMPLETE_UNEXPLAINED' and 'UNEXPLAINED_MISSING_SCORE' in a['flags']


def test_awarded_zero_score_is_not_an_official_draw_decision():
    r=fixture('Alpha v Béta  0-0 [awarded]');a=s.inspect_record(r)
    assert a['goal_derived_outcome']=='D' and 'SOURCE_MARKED_ADMINISTRATIVE' in a['flags']
    assert 'official_outcome' not in a and a['chronology']['effective_result_availability'] is None


@pytest.mark.parametrize('body',['Alpha v Béta  2-?','Alpha v Béta  ?-2','Alpha  garbage  Béta'])
def test_unknown_or_partial_score_fails_with_location(body):
    with pytest.raises(ValueError,match='season.txt:4'):fixture(body)


@pytest.mark.parametrize('heading',['Thu Aug 8 2014','Fri Aug 8 2015','Sun Feb 30 2014'])
def test_date_ambiguity_invalid_calendar_or_season_is_explicit(heading):
    with pytest.raises(ValueError,match='calendar'):text('▪ Matchday 1\n'+heading+'\nAlpha v Beta  0-0\n')


def test_new_round_does_not_inherit_previous_date():
    with pytest.raises(ValueError,match='without'):text('▪ Matchday 1\nFri Aug 8 2014\nAlpha v Beta  0-0\n▪ Matchday 2\nGamma v Delta  1-0\n')


def test_year_inference_disclosed_not_inferred_day_month():
    r=text('▪ Matchday 1\nFri Aug 8\nAlpha v Beta  0-0\n')[0]
    assert r['date_basis']=='EXPLICIT_DAY_MONTH_SEASON_WEEKDAY_YEAR' and not r['year_explicit']
    assert r['date_heading']=='Fri Aug 8'


def test_other_stage_observation_kept_and_flagged():
    r=text('▪ Promotion Playoff Final\nFri Aug 8 2014\nAlpha v Beta  0-0\n')[0]
    assert r['stage']=='OTHER_STAGE' and 'UNCONFIRMED_COMPETITION_STAGE' in s.inspect_record(r)['flags']


@pytest.mark.parametrize('title',['= French Ligue 2 2014/15','= French Ligue 1 2015/16'])
def test_wrong_competition_or_year_rejected(title):
    raw=(title+'\n▪ Matchday 1\nFri Aug 8 2014\nAlpha v Beta  0-0\n').encode()
    with pytest.raises(ValueError):s.read_text(raw,2014,'x',s.base.sha(raw))


def test_label_defect_separate_from_numeric_defect_no_source_rewrite():
    r=historical();original=deepcopy(r);a=s.inspect_record(r)
    assert a['classification']=='SOURCE_LABEL_INCONSISTENT' and a['goal_derived_outcome']=='A'
    assert not a['malformed_reasons'] and r==original


@pytest.mark.parametrize('field,value,reason',[('hgoal','-1','INVALID_GOALS'),('FT','2-0','FT_GOAL_CONFLICT'),('totgoal','9','NUMERIC_DERIVED_FIELD_CONFLICT'),('goaldif','1','NUMERIC_DERIVED_FIELD_CONFLICT')])
def test_numeric_errors_not_conflated_with_auxiliary_label(field,value,reason):
    a=s.inspect_record(historical(**{field:value}))
    assert a['classification']=='MALFORMED_OR_NUMERIC_CONFLICT' and reason in a['malformed_reasons']


def test_half_time_contradiction_and_cancelled_with_score_flagged():
    r=fixture('Alpha v Béta  1-0 (2-0)');assert 'HALFTIME_FT_CONFLICT' in s.inspect_record(r)['malformed_reasons']
    r=fixture('Alpha v Béta  1-0 [cancelled]');assert 'CANCELLED_WITH_SCORE' in s.inspect_record(r)['malformed_reasons']


def test_unusual_score_is_review_flag_not_numeric_error():
    a=s.inspect_record(fixture('Alpha v Béta  0-9'))
    assert a['classification']=='CONSISTENT_SCORE_FIELDS' and a['flags']==['UNUSUAL_SCORE']


def test_broad_groups_precise_rows_seasons_and_pattern():
    rows=[historical(),historical(Season='2015',Date='2015-08-01',result='A')]
    g=s.broad_groups(rows)['result_label_defect']
    assert g['count']==g['primary_target_count']==1 and g['every_pre2015_away_label_D'] and g['all_defects_pre2015_away_to_draw']
    assert g['counts_by_season']=={'1990/1991':1} and g['members'][0]['source_line']==2


def test_non_systematic_result_pattern_does_not_get_false_confirmation():
    g=s.broad_groups([historical(hgoal='1',vgoal='0',FT='1-0',totgoal='1',goaldif='1',result='D')])['result_label_defect']
    assert not g['all_defects_pre2015_away_to_draw'] and not g['every_pre2015_away_label_D']


def test_placeholder_and_extended_boundary_not_called_impossible():
    rows=[historical(Season='1932',Date='1933-07-01'),historical(Season='1967',Date='1968-07-05')]
    d=s.broad_groups(rows)['historical_date_quality']
    assert d['count']==2 and d['primary_target_count']==0
    assert [x['classification'] for x in d['clusters']]==['SUSPECTED_PLACEHOLDER','SOURCE_SEASON_BOUNDARY_UNCERTAINTY']


def test_invalid_date_and_team_are_malformed_without_inferred_repair():
    r=historical(Date='1990-02-30',home=' Alpha');a=s.inspect_record(r)
    assert set(a['malformed_reasons'])=={'INVALID_DATE','INVALID_TEAM_LABEL'}
    assert r['date']=='1990-02-30' and r['home']==' Alpha'


def test_repeated_round_scheduling_span_keeps_all_fixtures_not_duplicates():
    rows=[assessed(r) for r in text('▪ Matchday 1\nFri Aug 8 2014\nAlpha v Beta  0-0\n▪ Matchday 1\nFri Sep 5\nGamma v Delta  1-0\n')]
    report=s.season_report(rows,2014)
    assert len(report['wide_rounds'])==1 and report['wide_rounds'][0]['span_days']==28
    assert len(report['wide_rounds'][0]['affected_ids'])==2 and not report['duplicates']
    assert all('WIDE_ROUND_SPAN' in r['assessment']['flags'] for r in rows)


def test_duplicate_pairings_and_team_date_collisions_visible():
    rows=[assessed(r) for r in text('▪ Matchday 1\nFri Aug 8 2014\nAlpha v Beta  0-0\nAlpha v Beta  1-0\n')]
    r=s.season_report(rows,2014)
    assert len(r['duplicates'])==1 and len(r['same_team_date_collisions'])==2
    assert all('DUPLICATE_DIRECTED_PAIR' in x['assessment']['flags'] for x in rows)


def test_round_allocation_and_missing_rounds_explicit_not_silently_accepted():
    rows=[assessed(fixture())];r=s.season_report(rows,2014)
    assert r['round_allocation_discrepancies']=={'1':{'observed':1,'expected':10}}
    assert r['missing_rounds']==list(range(2,39)) and 'ROUND_ALLOCATION_OR_COVERAGE' in r['relational_issues']
    assert 'ROUND_ALLOCATION_REVIEW' in rows[0]['assessment']['flags']


def test_broad_group_analysis_survives_missing_numeric_goals():
    r=historical();r['hg']=None;r['ag']=None;r['source_fields']['result']='D'
    groups=s.broad_groups([r]);assert groups['result_label_defect']['matrix'][0]['goal_derived'] is None


def test_competition_formats_and_missing_season_not_fabricated():
    assert [s.clubs(y) for y in (1990,1997,2001,2002,2023)]==[20,18,18,20,18]
    report=s.season_report([],1994);assert report['observed']==0 and report['expected_scheduled']==380 and not report['team_names']
    assert s.season_report([],2019)['expected_played']==279


def test_overlap_preserves_distinct_ajaccio_clubs_and_score_conflicts():
    a=historical(home='AC Ajaccio');b=historical(home='Gazélec FC Ajaccio')
    o=s.compare_sources([a],[b],{'Gazélec FC Ajaccio':'Gazélec FC Ajaccio','Béta':'Béta'})
    assert o['matched']==0 and len(o['unmatched_historical'])==len(o['unmatched_modern'])==1
    b=deepcopy(a);b['ag']='0';b['date']='1990-08-02';b['audit_id']='other'
    o=s.compare_sources([a],[b],{'AC Ajaccio':'AC Ajaccio','Béta':'Béta'})
    assert set(o['differences'][0]['differences'])=={'date','ag'} and a['ag']=='1'


def test_overlap_mapping_must_be_bijective_and_duplicates_fail():
    a=historical()
    with pytest.raises(ValueError):s.compare_sources([a],[a],{'Alpha':'x','Béta':'x'})
    with pytest.raises(ValueError,match='Duplicate'):s.compare_sources([a,a],[a],{'Alpha':'Alpha','Béta':'Béta'})


def test_queue_groups_label_only_records_and_deduplicates_overlapping_flags():
    a=assessed(historical());b=assessed(fixture('Alpha v Béta  0-0 [awarded]'))
    b['assessment']['flags']+=['WIDE_ROUND_SPAN','WIDE_ROUND_SPAN'];q=s.queue_records([a,b],{'label':{},'dates':{}})
    assert q['stats']['unique_flagged_observations']==2 and q['stats']['manual_fixture_count']==1
    assert q['stats']['grouped_only_flagged']==1 and len(q['manual_fixtures'][0]['flags'])==2


def test_queue_rejects_duplicate_observation_ids():
    a=assessed(fixture('Alpha v Béta [cancelled]'))
    with pytest.raises(ValueError,match='duplicate'):s.queue_records([a,deepcopy(a)],{})


def test_known_case_requires_one_exact_primary_binding():
    with pytest.raises(ValueError,match='Known review fixture'):s.cases([],[])


def test_case_dates_distinct_and_never_effective_policy():
    primary=[]
    for name,year,home,away,_,_,_,_,_ in s.CASE_SPECS:
        day,ft=s.CASE_FACTS[name];h,a=ft.split('-')
        r=historical(Season=str(year),Date=day,home=home,visitor=sorted(away)[0],FT=ft,hgoal=h,vgoal=a,totgoal=str(int(h)+int(a)),goaldif=str(int(h)-int(a)))
        primary.append(assessed(r))
    cases=s.cases(primary,[]);assert len(cases)==6
    nice=next(r for r in primary if r['home']=='OGC Nice');assert nice['assessment']['chronology']['independently_supported_completion']=='2021-10-27'
    nantes=next(r for r in primary if r['season']=='2025/2026');assert nantes['assessment']['chronology']['administrative_decision_date']=='2026-05-27'
    assert all(r['assessment']['chronology']['effective_result_availability'] is None for r in primary)


def test_known_case_cannot_bind_to_wrong_date_or_score():
    r=assessed(historical(Season='2016',home='SC Bastia',visitor='Olympique Lyonnais'))
    with pytest.raises(ValueError,match='source facts changed'):s.cases([r],[])


def test_canonical_output_serialization_and_group_membership_deterministic():
    rows=[assessed(historical()),assessed(fixture('Alpha v Béta [cancelled]'))]
    assert s.base.encode(s.queue_records(deepcopy(rows),{}))==s.base.encode(s.queue_records(deepcopy(rows),{}))


def test_protected_sources_and_append_only_log_never_silently_ignored(tmp_path):
    private=tmp_path/'private';private.mkdir();(tmp_path/'source').write_bytes(b'original');(tmp_path/'PLANNING_LOG.md').write_bytes(b'history\nappend\n')
    s.base.save(private/s.BASELINE,s.base.encode(dict(files={'source':s.base.sha(b'original')},planning_log=dict(bytes=8,sha256=s.base.sha(b'history\n')))))
    with patch.object(s.acquisition,'protect',return_value={}):
        assert s.protect(private,tmp_path)['phase2_3_entries']==1
        (tmp_path/'source').write_bytes(b'changed')
        with pytest.raises(ValueError,match='Frozen'):s.protect(private,tmp_path)
