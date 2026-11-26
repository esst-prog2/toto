"""Synthetic Phase 3 checks; no network/private source dependency."""
from copy import deepcopy
from pathlib import Path
import json
import pytest
from scripts import collect_belgian_pro_league_history as a
from scripts import inventory_belgian_pro_league_history as i
from scripts import validate_belgian_pro_league_feasibility as v
from tests.test_belgian_pro_league_feasibility import receipt, text


def test_exact_two_new_originals():
    p=a.plan();assert len(p)==2
    assert [(x['original_path'],x['expected_blob'],x['expected_bytes']) for x in p]==[('2021-22/be1.txt','2e554912605069d2979b413ae696bf2aced1e4d1',27360),('2024-25/be1.txt','a883cd17078b92e876a11e150538c39122769b51',26302)]
    assert all(x['commit']=='1166d3c9c5725aec01e1bbeaa20f6467e39ddbb8' for x in p)


def test_unapproved_acquisition_fails_before_network(tmp_path):
    with pytest.raises(ValueError,match='Unapproved'):a.request(dict(url='https://invalid'),tmp_path)


@pytest.mark.parametrize('year',[2018,2019,2020,2021,2023,2024,2025])
def test_content_season_from_literal_title(year):
    raw=text(year=year);assert i.declared_year(raw)==year


@pytest.mark.parametrize('bad',[b'= Belgium First Division A 2020/22',b'= Belgian Cup 2020/21',b''])
def test_no_invented_season_declaration(bad):
    with pytest.raises((ValueError,IndexError)):i.declared_year(bad)


def test_mislabeled_path_cannot_turn_content_into_requested_season():
    raw=text(year=2020,day='Sat Aug 8 2020');rec=receipt(raw,'openfootball/belgium/2021-22/be1.txt')
    year=i.declared_year(raw);rows,_=i.parse_original(raw,year,rec)
    assert rows[0]['season']=='2020/2021' and rows[0]['source']==rec['path']
    with pytest.raises(ValueError):i.parse_original(raw,2021,rec)


@pytest.mark.parametrize('year,round_id,accepted',[(2020,34,True),(2021,34,True),(2022,34,True),(2019,31,False),(2023,31,False),(2024,31,False),(2020,35,False)])
def test_competition_specific_round_boundaries(year,round_id,accepted):
    raw=text(year=year,stage=f'Matchday {round_id}',day={2020:'Sat Aug 8 2020',2021:'Sun Aug 8 2021',2022:'Mon Aug 8 2022',2019:'Thu Aug 8 2019',2023:'Tue Aug 8 2023',2024:'Thu Aug 8 2024'}[year])
    if accepted:assert i.parse_original(raw,year,receipt(raw))[0][0]['round']==round_id
    else:
        with pytest.raises(ValueError):i.parse_original(raw,year,receipt(raw))


@pytest.mark.parametrize('stage,label',[('Matchday 1','REGULAR_SEASON'),('Championship, Matchday 1','CHAMPIONSHIP'),('Europe, Matchday 1','EUROPE'),('Relegation, Matchday 1','PLAYDOWNS'),('ECL Playoff, Final','EUROPE_QUALIFICATION')])
def test_stage_population_not_based_on_filename(stage,label):
    raw=text(stage=stage);r=i.parse_original(raw,2023,receipt(raw))[0][0]
    assert r['stage']==label and 'match_id' not in r and 'disposition' not in r


def test_physical_original_line_bytes_retained():
    raw=text().replace(b'\n',b'\r\n');r=i.parse_original(raw,2023,receipt(raw))[0][0]
    assert r['source_line']==4 and r['physical_record_sha256']==a.c.sha(raw.splitlines(keepends=True)[3])


def test_cancellation_is_not_a_result_or_policy():
    raw=text('A v B [cancelled]');r=i.parse_original(raw,2023,receipt(raw))[0][0]
    assert r['FT'] is None and r['annotation']=='[cancelled]' and 'disposition' not in r


def test_stage_rematch_stays_separate_in_diagnostic_identity():
    raw=text()+b'\n\xe2\x96\xaa Championship, Matchday 1\nFri Apr 5 2024\nA v B  1-0\n'
    rows,_=i.parse_original(raw,2023,receipt(raw));assert len(rows)==2
    assert v.diagnostic_identity(rows[0])!=v.diagnostic_identity(rows[1])


def test_immutable_phase3_output_publication(tmp_path):
    p=tmp_path/'inventory.json';a.c.keep(p,b'{}');a.c.keep(p,b'{}')
    with pytest.raises(ValueError):a.c.keep(p,b'{"changed":true}')


def test_repeat_pair_overlap_preserves_both_event_representations():
    raw=text()+b'\n\xe2\x96\xaa Championship, Matchday 1\nFri Apr 5 2024\nA v B  1-0\n'
    modern=i.parse_original(raw,2023,receipt(raw))[0];historic=deepcopy(modern)
    for n,r in enumerate(historic):r.update(audit_id=f'h{n}',stage='UNKNOWN')
    o=v.overlap(historic,modern)
    assert o['candidate_event_matches']==2 and o['matched_modern_stage_counts']=={'REGULAR_SEASON':1,'CHAMPIONSHIP':1}
