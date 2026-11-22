"""Synthetic Phase 4 structural guards; no private historical match data."""
from copy import deepcopy

import pytest

from scripts import validate_la_liga_structure as v


def rows():
    fixtures=[[(0,3),(1,2)],[(0,2),(3,1)],[(0,1),(2,3)]]
    fixtures += [[(a,h) for h,a in rnd] for rnd in fixtures]
    result=[]
    for round_id,pairs in enumerate(fixtures,1):
        for h,a in pairs:
            result.append(dict(source_line=len(result)+1,date=f'2000-09-{round_id*3:02}',home=f'Team {h}',away=f'Team {a}',
                               hg='2',ag='1',HT='1-0',FT='2-1',round=round_id,kickoff=None,stage='league',annotation=''))
    return result


def codes(report):return {c for e in report['errors'] for c in e['codes']}


def test_full_schedule_and_goals_outcomes_halftime_without_mutation():
    rs=rows();before=deepcopy(rs);r=v.validate(rs,2000,4)
    assert r['status']=='STRUCTURAL_PASS' and r['records']==12 and r['clubs']==4
    assert r['outcomes']=={'1':12} and r['halftime_records']==12
    assert r['fixture_error_records']==0 and rs==before


@pytest.mark.parametrize('change,wanted',[
 ('missing','fixture_count'),('duplicate','duplicate_ordered_pair'),('negative','invalid_fulltime_goals'),
 ('fraction','invalid_fulltime_goals'),('missing_score','invalid_fulltime_goals'),('FT','FT_disagrees_with_goals'),
 ('HT','halftime_exceeds_fulltime'),('bad_HT','invalid_halftime'),('date','invalid_date'),('season','date_outside_season'),
 ('team','same_home_away'),('space','invalid_team_label'),('replacement','unicode_replacement'),('round','round_coverage')])
def test_invalid_facts_and_coverage_are_explicit(change,wanted):
    rs=rows()
    if change=='missing':rs.pop()
    if change=='duplicate':rs[-1]=dict(rs[0],hg='3',FT='3-1')
    if change=='negative':rs[0]['hg']='-1'
    if change=='fraction':rs[0]['hg']='2.5'
    if change=='missing_score':rs[0]['hg']=None
    if change=='FT':rs[0]['FT']='9-9'
    if change=='HT':rs[0]['HT']='3-0'
    if change=='bad_HT':rs[0]['HT']='invalid'
    if change=='date':rs[0]['date']='2000-02-30'
    if change=='season':rs[0]['date']='2002-01-01'
    if change=='team':rs[0]['away']=rs[0]['home']
    if change=='space':rs[0]['home']=' Team 0'
    if change=='replacement':rs[0]['home']='Team \ufffd'
    if change=='round':rs[0]['round']=39
    r=v.validate(rs,2000,4)
    assert r['status']=='STRUCTURAL_REVIEW' and wanted in codes(r)


def test_round_team_allocation_detects_error_even_when_round_totals_match():
    rs=rows();rs[0]['round'],rs[2]['round']=rs[2]['round'],rs[0]['round']
    assert 'round_team_allocation' in codes(v.validate(rs,2000,4))


def test_each_half_requires_all_unordered_opponents():
    rs=rows();rs[0]['round'],rs[6]['round']=4,1
    # Swap complete rounds with different opponent sets while retaining per-round games.
    rs=rows()
    for r in rs:
        if r['round']==1:r['round']=5
        elif r['round']==5:r['round']=1
    assert 'half_season_opponent_coverage' in codes(v.validate(rs,2000,4))


def test_same_day_conflicts_and_consecutive_days_are_distinct():
    rs=rows();rs[2]['date']=rs[0]['date']
    assert 'same_team_same_date' in codes(v.validate(rs,2000,4))
    rs=rows();rs[2]['date']='2000-09-04'
    assert any(f['kind']=='consecutive_day_matches' for f in v.validate(rs,2000,4)['flags'])


def test_high_scores_are_review_flags_not_automatic_errors_or_exclusions():
    rs=rows();rs[0].update(hg='10',FT='10-1')
    r=v.validate(rs,2000,4)
    assert r['status']=='STRUCTURAL_PASS' and r['records']==12
    assert r['flags']==[dict(line=1,kind='unusually_high_score',score='10-1')]


def test_unicode_equivalent_labels_not_silently_merged():
    rs=rows();rs[0]['home']='Café';rs[2]['home']='Cafe\u0301'
    assert 'normalized_label_collision' in codes(v.validate(rs,2000,4))


def text(extra='',heading='Primera División 2000/01',weekday='Sun'):
    return f'= {heading}\n▪ Matchday 1\n{weekday} Sep 3 2000\n19:00  Alpha  v Béta  2-1 (1-0)\n{extra}'.encode()


def test_independent_text_parser_unicode_crlf_halftime_and_physical_lines():
    raw=text().replace(b'\n',b'\r\n');before=bytes(raw)
    rs,notes,head=v.parse_text(raw,2000)
    assert len(rs)==1 and rs[0]['source_line']==4 and rs[0]['away']=='Béta'
    assert rs[0]['HT']=='1-0' and head and raw==before
    assert not any(n['kind']=='weekday_error' for n in notes)


def test_scorer_continuations_cannot_create_fixtures():
    raw=b'= Primera Division\n\xe2\x96\xaa Regular Season - 1\nFri Aug 15 2025\n19:00  Alpha  2-1 (0-0)  Beta\n (One 1\'(p), Two 2\';\n Three 3\')\n'
    rs,notes,_=v.parse_text(raw,2025)
    assert len(rs)==1 and sum(n['kind']=='scorer' for n in notes)==2


@pytest.mark.parametrize('raw',[
 text(heading='Segunda Division'),text(heading='Primera Division 2001/02'),text(extra='UNKNOWN\n'),
 text(extra='(unclosed\n'),text().replace(b'19:00',b'25:00'),
 text().replace('▪ Matchday 1'.encode(),'▪ Playoff'.encode()),
 text().replace(b'2-1 (1-0)',b'[postponed]'),
])
def test_unknown_or_contradictory_source_structure_fails_closed(raw):
    with pytest.raises(ValueError):v.parse_text(raw,2000)


def test_weekday_disagreement_and_covid_inheritance_are_preserved():
    _,notes,_=v.parse_text(text(weekday='Mon'),2000)
    assert any(n['kind']=='weekday_error' for n in notes)
    raw='= Primera División\n▪ Matchday 1\nFri Jun 26 2020\nAlpha  v Beta  1-0\nFri Jul 3\nBeta  v Alpha  0-0\n'.encode()
    rs,_,_=v.parse_text(raw,2019)
    assert rs[-1]['date']=='2020-07-03' and not v.validate(rs,2019,2)['fixture_error_records']


def test_csv_schema_scope_and_fulltime_contradiction():
    header=','.join(v.FIELDS)+'\n'
    good='2000-09-03,2000,Alpha,Beta,1-0,2-1,2,1,1,league,NA,NA\n'
    old=v.parse_csv((header+good).encode());rs=v.csv_season(old,2000)
    assert len(rs)==1 and rs[0]['FT']=='2-1'
    bad=deepcopy(old);bad[0]['round']='phase2'
    with pytest.raises(ValueError,match='tier/stage'):v.csv_season(bad,2000)
    with pytest.raises(ValueError,match='header'):v.parse_csv(b'Date,Season,Season\n')
    with pytest.raises(ValueError,match='malformed'):v.parse_csv((header+good.rstrip()+',EXTRA\n').encode())


def test_scheduling_preserves_all_candidate_fixtures_and_does_not_assign_cause():
    rs=rows();rs=rs[:2];rs[0]['date']='2000-09-01';rs[1]['date']='2000-10-01'
    span=dict(stage='Matchday 1',first='2000-09-01',last='2000-10-01',lines=[1,2]);before=deepcopy(rs)
    c=v.scheduling(rs,[],span,'2000/2001')
    assert c['structural_error'] is False and len(c['all_round_fixtures'])==2
    assert c['decision']=='UNRESOLVED_HISTORICAL_SCHEDULING' and rs==before
    with pytest.raises(ValueError):v.scheduling(rs,[],dict(span,lines=[1]),'2000/2001')


def test_cross_source_comparison_reports_conflicts_and_refuses_unmapped_names():
    old=rows();new=deepcopy(old)
    assert not v.compare_sources(old,new,2000)['differences']
    new[0]['date']='2000-09-02';new[0]['hg']='3'
    result=v.compare_sources(old,new,2000)
    assert set(result['differences'][0]['differences'])=={'date','hg'}
    new[0]['home']='UNKNOWN'
    with pytest.raises(ValueError,match='identity mapping'):v.compare_sources(old,new,2000)


def test_cli_refuses_overwrite_and_check_does_not_replace(tmp_path,monkeypatch):
    import sys
    monkeypatch.setattr(v,'PRIVATE',tmp_path);path=tmp_path/v.OUTPUT;path.write_bytes(b'preserved')
    monkeypatch.setattr(sys,'argv',['validator'])
    monkeypatch.setattr(v,'build',lambda:(_ for _ in ()).throw(AssertionError('should refuse before build')))
    with pytest.raises(FileExistsError):v.main()
    monkeypatch.setattr(sys,'argv',['validator','--check'])
    monkeypatch.setattr(v,'build',lambda:dict(totals={},seasons=[]))
    with pytest.raises(ValueError,match='differs'):v.main()
    assert path.read_bytes()==b'preserved'


def test_changed_frozen_evidence_fails_before_parsing(tmp_path,monkeypatch):
    import json
    monkeypatch.setattr(v,'ROOT',tmp_path)
    monkeypatch.setattr(v,'protect',lambda d:{})
    baseline={}
    for i in range(52):
        name=f'original-{i}';(tmp_path/name).write_bytes(b'original');baseline[name]=v.sha(b'original')
    (tmp_path/'phase4_protected_before.json').write_text(json.dumps(baseline))
    (tmp_path/'original-0').write_bytes(b'changed')
    with pytest.raises(ValueError,match='Frozen evidence changed'):v.build(tmp_path)
