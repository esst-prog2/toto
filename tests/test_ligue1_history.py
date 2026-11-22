"""Synthetic Phase 3 acquisition/inventory tests; no private/network dependency."""
from copy import deepcopy
import hashlib
import json
from unittest.mock import patch

import pytest

from scripts import collect_ligue1_feasibility as base
from scripts import collect_ligue1_history as c
from scripts import inventory_ligue1_history as v
from scripts import validate_ligue1_feasibility as feasibility


def row(year=2014,h='0',a='1',label='D',home='Alpha',away='Beta',day=None,line=2):
    f=dict(Date=day or f'{year}-08-01',Season=str(year),home=home,visitor=away,FT=f'{h}-{a}',
           hgoal=h,vgoal=a,division='1',tier='1',totgoal=str(int(h)+int(a)),goaldif=str(int(h)-int(a)),result=label)
    return dict(source_line=line,date=f['Date'],source_fields=f,home=home,away=away,hg=h,ag=a,FT=f['FT'],HT=None,
                season=f'{year}/{year+1}',stage='SOURCE_TIER1_NO_EXPLICIT_STAGE',round=None,annotation='')


def test_exact_seven_new_season_paths_and_pin():
    plans=c.plan()
    assert [int(p['season'][:4]) for p in plans]==[2015,2017,2018,2020,2021,2022,2024]
    assert len(plans)==7 and len(c.REUSED)==5 and not set(c.YEARS)&set(c.REUSED)
    assert set(c.YEARS)|set(c.REUSED)==set(range(2014,2026))
    assert all(p['commit']=='63df627f3c87ce71708f016522ea236cf74332c3' and p['repository']=='openfootball/europe' for p in plans)
    assert all(p['url'].endswith(p['original_path']) and p['original_path']==f"france/{p['season'][:4]}-{str(int(p['season'][:4])+1)[-2:]}_fr1.txt" for p in plans)
    assert not any('full' in p['path'] or 'football-data' in p['url'] or '2026-27' in p['path'] for p in plans)


def fake_sources():
    entries={};raws={}
    for p in c.plan():
        raw=(p['season']+' synthetic\r\n').encode();raws[p['url']]=raw
        entries[p['original_path']]=dict(size=len(raw),sha=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest())
    reused=[dict(kind='dataset',repository=c.REPO,original_filename=f'{y}-{(y+1)%100:02}_fr1.txt',path=f'reused/{y}') for y in c.REUSED]
    return entries,raws,dict(files=reused)


def acquired(tmp_path):
    entries,raws,old=fake_sources();base.save(tmp_path/'acquisition.json',b'Phase 2 immutable')
    with patch.object(c,'protect',return_value={'frozen':True}),patch.object(c,'metadata',return_value=entries),patch.object(base,'verify_originals',return_value=old),patch.object(base,'request',side_effect=lambda url,d:raws[url]) as request,patch.object(c.time,'sleep'):
        result=c.collect(tmp_path)
    return result,entries,raws,old,request.call_count


def test_exact_acquisition_no_extra_requests_and_cache_reuse(tmp_path):
    result,entries,raws,old,calls=acquired(tmp_path)
    assert calls==7 and len(result['acquired'])==7 and len(result['reused_phase2'])==5
    with patch.object(c,'protect',return_value={'frozen':True}),patch.object(c,'metadata',return_value=entries),patch.object(base,'verify_originals',return_value=old),patch.object(base,'request',side_effect=AssertionError('No network on reuse')):
        assert c.collect(tmp_path)==result
        assert c.verify(tmp_path)==result
    assert (tmp_path/'acquisition.json').read_bytes()==b'Phase 2 immutable'


def test_cached_receipt_byte_tampering_fails(tmp_path):
    result,entries,_,_,_=acquired(tmp_path);r=result['acquired'][0];p=tmp_path/r['path']
    p.write_bytes(b'tampered')
    with pytest.raises(ValueError):c.cached(tmp_path,c.plan()[0],entries)


def test_receipt_scope_or_url_tampering_fails(tmp_path):
    result,entries,_,_,_=acquired(tmp_path);r=result['acquired'][0];p=tmp_path/r['path'];receipt=p.with_name(p.name+'.provenance.json')
    r['url']='https://unapproved.invalid';receipt.write_bytes(base.encode(r))
    with pytest.raises(ValueError,match='receipt'):c.cached(tmp_path,c.plan()[0],entries)


def test_partial_source_receipt_pair_never_repaired(tmp_path):
    p=c.plan()[0];base.save(tmp_path/p['path'],b'original')
    with pytest.raises(ValueError,match='Incomplete'):c.cached(tmp_path,p,{})


def test_manifest_missing_or_duplicate_season_fails(tmp_path):
    result,entries,_,old,_=acquired(tmp_path)
    result['acquired']=result['acquired'][:-1];(tmp_path/c.MANIFEST).write_bytes(base.encode(result))
    with patch.object(c,'metadata',return_value=entries):
        with pytest.raises(ValueError,match='scope'):c.verify(tmp_path)


def test_frozen_phase2_private_public_and_log_prefix_protected(tmp_path):
    directory=tmp_path/'private';directory.mkdir();(tmp_path/'source').write_bytes(b'unchanged');(tmp_path/'PLANNING_LOG.md').write_bytes(b'history\n')
    base.save(directory/c.BASELINE,base.encode(dict(files={'source':base.sha(b'unchanged')},planning_log=dict(bytes=8,sha256=base.sha(b'history\n')))))
    with patch.object(base,'protect',return_value={'private':1,'public':1}):
        (tmp_path/'PLANNING_LOG.md').write_bytes(b'history\nappend\n');assert c.protect(directory,tmp_path)['frozen_phase2_entries']==1
        (tmp_path/'source').write_bytes(b'changed')
        with pytest.raises(ValueError,match='Frozen'):c.protect(directory,tmp_path)


def test_append_only_planning_guard_rejects_rewrite(tmp_path):
    directory=tmp_path/'private';directory.mkdir();(tmp_path/'source').write_bytes(b'x');(tmp_path/'PLANNING_LOG.md').write_bytes(b'rewrite\n')
    base.save(directory/c.BASELINE,base.encode(dict(files={'source':base.sha(b'x')},planning_log=dict(bytes=8,sha256=base.sha(b'history\n')))))
    with patch.object(base,'protect',return_value={}):
        with pytest.raises(ValueError,match='history'):c.protect(directory,tmp_path)


def test_systematic_away_to_draw_pattern_measured_not_repaired():
    rows=[row(),row(h='1',a='1',label='D',line=3),row(h='2',a='0',label='H',line=4),row(year=2015,label='A',line=5)]
    original=deepcopy(rows);d=v.result_diagnosis(rows)
    assert d['systematic_pre2015_away_to_draw'] and d['contradiction_count']==1
    assert d['older_window_contradictions']==0 and not d['numeric_internal_disagreements']
    assert rows==original and rows[0]['source_fields']['result']=='D'


def test_non_systematic_pattern_and_later_errors_not_hidden():
    d=v.result_diagnosis([row(label='A'),row(year=2015,label='D')])
    assert not d['systematic_pre2015_away_to_draw'] and d['contradiction_count']==1


def test_numeric_fields_independently_checked_against_goals():
    r=row();r['source_fields'].update(FT='2-0',totgoal='3',goaldif='1')
    d=v.result_diagnosis([r]);assert {x['kind'] for x in d['numeric_internal_disagreements']}=={'FT','totgoal','goaldif'}


@pytest.mark.parametrize('value',['-1','2.5','unknown'])
def test_invalid_numeric_goals_never_silently_accepted(value):
    r=row();r['source_fields']['hgoal']=value
    assert v.result_diagnosis([r])['numeric_internal_disagreements'][0]['kind']=='INVALID_GOALS'


def test_historical_target_window_absence_and_literal_identity_preserved():
    rows=[row(1990,home='Brest Armorique FC'),row(1990,home='Stade Brest',line=3)]
    w=v.historical_window(rows)
    assert len(w['seasons'])==24 and w['observations']==2 and '1994/1995' in w['missing_seasons']
    assert w['seasons'][0]['clubs']==3
    assert 'Brest Armorique FC' in w['seasons'][0]['team_names'] and 'Stade Brest' in w['seasons'][0]['team_names']


def test_club_labels_are_candidates_without_merging_parents_or_distinct_clubs():
    rows=[row(home='AS Saint-Étienne',away='AS Saint-Etienne'),row(home='AC Ajaccio',away='Gazélec FC Ajaccio')]
    cat=v.diagnostic_labels(rows)
    assert cat['distinct_labels']==4 and cat['string_candidates']['as saint etienne']==['AS Saint-Etienne','AS Saint-Étienne']
    assert 'AC Ajaccio' in cat['exact_labels'] and 'Gazélec FC Ajaccio' in cat['exact_labels']
    assert 'Gazélec FC Ajaccio' not in feasibility.DIAGNOSTIC_VARIANTS


def test_distinct_ajaccio_clubs_do_not_become_approved_diagnostic_alias():
    left=[row(year=2015,home='AC Ajaccio')];right=[row(year=2015,home='Gazélec FC Ajaccio')]
    o=feasibility.compare(left,right)
    assert o['matched_pairs']==0 and len(o['unmatched_left'])==len(o['unmatched_right'])==1


def test_unusual_date_count_and_invalid_date_are_separate():
    rows=[row(1932,day='1933-07-01'),row(2014,day='2014-02-30',line=3)]
    d=v.date_inventory(rows)
    assert d['outside_source_season_count']==1 and len(d['invalid_dates'])==1
    assert rows[0]['date']=='1933-07-01'


def test_day_month_explicit_and_year_inferred_counts_separate():
    rows=[dict(year_explicit=True),dict(year_explicit=False),dict(year_explicit=False)]
    d=v.date_precision(rows)
    assert d['explicit_day_month']==3 and d['explicit_year']==1 and d['season_weekday_inferred_year']==2
    assert d['day_month_inferred']==d['ambiguities']==0


def test_phase2_flags_and_fixtures_cannot_be_dropped_or_changed():
    flag=dict(round='1',span_days=20);r=dict(source='x',assessment=dict(season='2014/2015',wide_rounds=[flag]),records=[dict(date='2014-08-01')])
    assert len(v.carried_flags(dict(modern=[r]),[deepcopy(r)]))==1
    modified=deepcopy(r);modified['assessment']['wide_rounds']=[]
    with pytest.raises(ValueError):v.carried_flags(dict(modern=[r]),[modified])
    with pytest.raises(ValueError):v.carried_flags(dict(modern=[r]),[])


def test_full_version_not_counted_as_an_additional_modern_season():
    assert not v.carried_flags(dict(modern=[dict(source='2025-26_fr1-full.txt')]),[])


def test_diagnosis_and_inventory_parts_are_byte_deterministic():
    rows=[row(1990),row(2015,label='A')]
    first=base.encode(dict(diagnosis=v.result_diagnosis(rows),window=v.historical_window(rows),labels=v.diagnostic_labels(rows)))
    second=base.encode(dict(diagnosis=v.result_diagnosis(deepcopy(rows)),window=v.historical_window(deepcopy(rows)),labels=v.diagnostic_labels(deepcopy(rows))))
    assert first==second and base.sha(first)==base.sha(second)
