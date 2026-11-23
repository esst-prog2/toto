"""Synthetic independent structural validation; no historical adjudication."""
import csv,io
from copy import deepcopy
import pytest
from scripts import validate_primeira_liga_structure as v
c=v.c


def receipt(raw,path='synthetic'):
    return dict(path=path,sha256=c.sha(raw),commit='revision',git_blob_sha1='blob',url='https://example.invalid/original')


def historical(cells=None,year=2011):
    out=io.StringIO(newline='');w=csv.writer(out);w.writerow(v.COLUMNS);w.writerow(cells or [f'{year}-08-14',str(year),'A','B','1-0','1','0','P1','1','1','1','H']);raw=out.getvalue().encode();return v.historical(raw,receipt(raw))


def text(body='A v B  2-1 (1-0)',year=2024,day='Fri Aug 9 2024'):
    raw=f'= Portuguese Primeira Liga {year}/{(year+1)%100:02}\n▪ Matchday 1\n{day}\n{body}\n'.encode();return raw


def modern(body='A v B  2-1 (1-0)',year=2024,day='Fri Aug 9 2024'):
    raw=text(body,year,day);return v.modern(raw,year,receipt(raw))[0]


def test_original_fields_and_physical_binding():
    rs=historical();r=rs[0];assert r['original_fields']['division']=='P1' and r['source_line']==2
    assert c.sha(r['original_literal'].encode())==r['physical_record_sha256']
    assert r['effective_result_availability'] is None and r['historical_verification']=='NOT_CERTIFIED' and 'match_id' not in r


@pytest.mark.parametrize('index,value,reason',[(0,'2011-02-30','INVALID_DATE'),(0,'1900-01-01','INVALID_OR_OUTSIDE_DATE'),(2,'A ','SOURCE_LABEL_DEFECT'),(3,'A','SOURCE_LABEL_DEFECT'),(4,'0-1','MALFORMED_OR_CONTRADICTORY_SCORE'),(5,'-1','MALFORMED_OR_CONTRADICTORY_SCORE'),(5,'1.0','MALFORMED_OR_CONTRADICTORY_SCORE'),(7,'P2','WRONG_TIER_OR_DIVISION'),(8,'2','WRONG_TIER_OR_DIVISION'),(9,'2','DERIVED_FIELD_CONTRADICTION'),(10,'-1','DERIVED_FIELD_CONTRADICTION'),(11,'D','DERIVED_FIELD_CONTRADICTION')])
def test_source_defects_reported_not_rewritten(index,value,reason):
    cells=['2011-08-14','2011','A','B','1-0','1','0','P1','1','1','1','H'];cells[index]=value;rs=historical(cells);s=v.assess(rs,2011)
    assert reason in s['invalid'][0]['reasons'] and rs[0]['original_fields'][v.COLUMNS[index]]==value and s['structurally_valid']==0


@pytest.mark.parametrize('year,n',[(1994,18),(2005,18),(2006,16),(2013,16),(2014,18),(2024,18)])
def test_season_format_not_forced(year,n):
    s=v.assess(historical(year=year),year);assert s['expected_clubs']==n and s['expected_slots']==n*(n-1) and s['observed']==1


@pytest.mark.parametrize('year,day',[(2018,'Fri Aug 10 2018'),(2019,'Sun Jul 26 2020'),(2020,'Fri Sep 18 2020'),(2021,'Fri Aug 6 2021'),(2022,'Fri Aug 5 2022'),(2023,'Fri Aug 11 2023'),(2024,'Fri Aug 9 2024'),(2025,'Fri Aug 8 2025')])
def test_all_source_seasons_and_date_precision(year,day):
    r=modern(year=year,day=day)[0];assert r['date_basis']=='EXPLICIT_DAY_MONTH_YEAR_WEEKDAY' and r['effective_result_availability'] is None


@pytest.mark.parametrize('change',[lambda b:b.replace(b'Portuguese Primeira Liga',b'Portuguese Segunda Liga'),lambda b:b.replace(b'Fri Aug 9 2024',b'Thu Aug 9 2024'),lambda b:b.replace(b'2-1 (1-0)',b'2-?'),lambda b:b.replace(b'Matchday 1',b'Matchday 35'),lambda b:b.replace(b'Fri Aug 9 2024\n',b''),lambda b:b+b'unknown\n'])
def test_unrecognized_modern_syntax_fails(change):
    raw=change(text())
    with pytest.raises(ValueError):v.modern(raw,2024,receipt(raw))


def test_checksums_fail_closed():
    raw=text();r=receipt(raw);r['sha256']='bad'
    with pytest.raises(ValueError):v.modern(raw,2024,r)
    with pytest.raises(ValueError):v.historical(raw,r)


def test_schema_order_not_silently_adapted():
    raw=b'Season,Date\n2011,2011-08-14\n'
    with pytest.raises(ValueError):v.historical(raw,receipt(raw))


def test_source_unscored_is_incomplete_without_not_played_policy():
    rs=modern('A v B');s=v.assess(rs,2024,True);assert s['unscored']==1 and s['structurally_valid']==0
    assert 'disposition' not in rs[0]


def test_round_pairing_and_participant_constraints():
    rs=modern('A v B  1-0\nA v C  0-0');s=v.assess(rs,2024,True)
    assert s['round_errors'][0]['records']==2 and s['round_errors'][0]['distinct_participants']==3


def test_half_time_cannot_exceed_full_time():
    s=v.assess(modern('A v B  1-0 (2-0)'),2024,True);assert 'HT_EXCEEDS_FT_OR_INVALID' in s['invalid'][0]['reasons']


def test_other_stage_is_visible_not_regular():
    raw=text()+b'\xe2\x96\xaa Playoff Final\nSat Aug 10\nC v D  1-0\n';rs,_=v.modern(raw,2024,receipt(raw));s=v.assess(rs,2024,True)
    assert s['stage_counts']['OTHER_STAGE']==1 and 'OTHER_STAGE' in s['invalid'][0]['reasons']


def test_wide_round_and_reverse_order_do_not_invalidate_scores():
    raw=text()+b'Fri Sep 6 2024\nC v D  1-0\nThu Sep 5 2024\nE v F  0-0\n';rs,_=v.modern(raw,2024,receipt(raw));s=v.assess(rs,2024,True)
    assert len(s['wide_rounds'])==1 and len(s['source_order_reversals'])==1 and not s['invalid'] and s['structurally_valid']==3


def test_unusual_score_is_not_automatically_error():
    s=v.assess(modern('A v B  10-0'),2024,True);assert len(s['unusual_scores'])==1 and not s['invalid']


def test_senior_reserve_and_vitorias_retained():
    rs=modern('Benfica v Benfica B  1-0\nVitória SC v Vitória FC  0-0');s=v.assess(rs,2024,True);assert s['clubs']==4 and s['reserve_labels']==['Benfica B']


def mapping(season='2024/2025'):
    return [dict(season=season,historical='Benfica',modern='SL Benfica'),dict(season=season,historical='Porto',modern='FC Porto')]


def test_overlap_preserves_conflicting_dates():
    hs=modern('Benfica v Porto  1-1');ms=modern('SL Benfica v FC Porto  1-1');ms[0]['audit_id']='other';ms[0]['date']='2024-08-10';before=deepcopy((hs,ms));r=v.correspondence(hs,ms,mapping(),'2024/2025')
    assert r['matched']==1 and not r['comparisons'][0]['date_equal'] and r['comparisons'][0]['score_equal'] and (hs,ms)==before


@pytest.mark.parametrize('mode',['cross_season','nonbijective','missing','duplicate_target','many_to_one'])
def test_ambiguous_or_wrong_overlap_fails(mode):
    hs=modern('Benfica v Porto  1-1');ms=modern('SL Benfica v FC Porto  1-1');links=mapping()
    if mode=='cross_season':links[0]['season']='2023/2024'
    elif mode=='nonbijective':links[1]['modern']='SL Benfica'
    elif mode=='missing':links.pop()
    elif mode=='duplicate_target':ms+=deepcopy(ms)
    elif mode=='many_to_one':hs+=deepcopy(hs)
    with pytest.raises(ValueError):v.correspondence(hs,ms,links,'2024/2025')


def test_duplicate_source_pairs_not_dropped():
    rs=modern('A v B  1-0\nA v B  0-3');s=v.assess(rs,2024,True);assert s['observed']==2 and s['duplicate_pairings'][0]['conflicting']


def test_exact_feirense_hypothesis_is_non_destructive():
    rs=historical(['2011-08-14','2011','Feirense ','Nacional','0-0','0','0','P1','1','0','0','D']);rs[0]['source_line']=4877;before=deepcopy(rs);r=v.feirense(rs)
    assert rs==before and r['original']['home']=='Feirense ' and r['hypothetical_one_occurrence']['team_labels']==['Feirense','Nacional']
    rs[0]['source_line']=4878
    with pytest.raises(ValueError):v.feirense(rs)


def test_no_abandonment_finality_inferred_from_score():
    r=modern('Belenenses SAD v SL Benfica  0-7 (0-7)')[0];assert r['annotation']=='' and r['effective_result_availability'] is None and 'disposition' not in r


def test_frozen_phase3_change_rejected(tmp_path,monkeypatch):
    monkeypatch.setattr(v.acquisition,'protect',lambda *args:{})
    p=tmp_path/'frozen';p.write_bytes(b'original');(tmp_path/'PLANNING_LOG.md').write_bytes(b'log\n')
    c.save(tmp_path/v.BASELINE,c.encode(dict(files={'frozen':c.sha(b'original')},planning_log=dict(bytes=4,sha256=c.sha(b'log\n')),approval='PHASE4_STRUCTURE_ONLY')))
    assert v.protect(tmp_path,tmp_path)['phase2_3_frozen_entries']==1
    p.write_bytes(b'changed')
    with pytest.raises(ValueError):v.protect(tmp_path,tmp_path)
