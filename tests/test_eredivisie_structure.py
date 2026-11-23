"""Synthetic independent structural checks; no private datasets or network."""
from copy import deepcopy
from datetime import date,timedelta
import csv,io
import pytest
from scripts import validate_eredivisie_structure as s


def receipt(raw):return dict(path='synthetic.txt',sha256=s.c.sha(raw),commit='pin',git_blob_sha1='blob',url='https://example.org/source')


def raw(body='A v B  2-1 (1-0)',day='Fri Aug 9 2024',round='Matchday 1'):
    return f'= Netherlands Eredivisie 2024/25\n▪ {round}\n{day}\n{body}\n'.encode()


def parse(body='A v B  2-1 (1-0)'):
    data=raw(body);return s.parse_modern(data,2024,receipt(data))[0]


def test_raw_binding_and_outcome():
    data=raw();rows,_=s.parse_modern(data,2024,receipt(data));r=rows[0]
    assert r['source_line']==4 and r['physical_record_sha256']==s.c.sha(data.splitlines(keepends=True)[3])
    assert s.inspect_record(r)['goal_derived_outcome']=='H'


@pytest.mark.parametrize('change',[lambda b:b.replace(b'Netherlands Eredivisie',b'French Ligue 1'),lambda b:b.replace(b'Fri Aug 9 2024',b'Thu Aug 9 2024'),lambda b:b.replace(b'Matchday 1',b'Matchday 35'),lambda b:b.replace(b'Fri Aug 9 2024\n',b''),lambda b:b.replace(b'2-1 (1-0)',b'2-?')])
def test_bad_grammar_fails(change):
    data=change(raw())
    with pytest.raises(ValueError):s.parse_modern(data,2024,receipt(data))


def test_wrong_hash():
    with pytest.raises(ValueError):s.parse_modern(raw(),2024,receipt(b'wrong'))


def test_invalid_utf8():
    data=raw()+b'\xff'
    with pytest.raises(UnicodeDecodeError):s.parse_modern(data,2024,receipt(data))


def test_leap_year_resolution():
    data=raw().replace(b'Fri Aug 9 2024',b'Sat Mar 1 2025');r=s.parse_modern(data,2024,receipt(data))[0][0];assert r['date']=='2025-03-01'


def test_split_round_preserved():
    data=raw()+b'\xe2\x96\xaa Matchday 1\nSat Aug 10\nC v D  0-0\n';rows,notes=s.parse_modern(data,2024,receipt(data));assert len(rows)==2 and notes['repeated_round_headings']=={'1':2}


def test_postseason_not_regular():
    data=raw()+b'\xe2\x96\xaa Playoff Final\nSat Aug 10\nC v D  2-0\n';r=s.parse_modern(data,2024,receipt(data))[0][1]
    assert 'OTHER_STAGE' in s.inspect_record(r)['errors']


def test_historical_columns_and_literals():
    data=b'Date,Season,home,visitor,FT,hgoal,vgoal,tier\n1990-08-24,1990,SVV Schiedam,FC Den Haag,1-0,1,0,1\n';r=s.parse_historical(data,receipt(data))[0]
    assert r['original_fields']['Season']=='1990' and r['season']=='1990/1991'
    assert r['source_line']==2 and r['stage']=='HISTORICAL_TIER1_STAGE_NOT_EXPLICIT'


@pytest.mark.parametrize('data',[b'Date,Season\n1990-08-24,1990\n',b'Date,Season,home,visitor,FT,hgoal,vgoal,tier\n1990-08-24,1990,A,B,1-0,1,0,2\n'])
def test_historical_unapproved_shape_or_tier(data):
    with pytest.raises(ValueError):s.parse_historical(data,receipt(data))


@pytest.mark.parametrize('changes,error',[({'hg':'-1'},'INVALID_SCORE'),({'FT':'9-9'},'FT_GOAL_CONFLICT'),({'HT':'3-0'},'HT_FT_CONFLICT'),({'home':'B'},'IDENTICAL_TEAMS'),({'date':'bad'},'INVALID_DATE'),({'date':'2026-01-01'},'INVALID_SEASON_DATE'),({'home':' A'},'INVALID_TEAM_LABEL'),({'hg':None},'PARTIAL_SCORE')])
def test_structural_errors_explicit(changes,error):
    r=parse()[0];r.update(changes);a=s.inspect_record(r);assert not a['structurally_valid'] and error in a['errors']


def test_unscored_valid_slot_not_completed_result():
    r=parse('A v B [cancelled]')[0];a=s.inspect_record(r)
    assert a['structurally_valid'] and a['unscored'] and a['result_incomplete']
    assert not a['unexplained_incomplete'] and not a['score_bearing']
    assert a['processing_policy']=='NOT_DECIDED' and a['chronology']['effective_availability'] is None


def test_unknown_unscored_separate():
    a=s.inspect_record(parse('A v B')[0]);assert a['unexplained_incomplete'] and 'UNEXPLAINED_INCOMPLETE' in a['flags']


def test_cancelled_with_score_error():
    a=s.inspect_record(parse('A v B  1-0 [cancelled]')[0]);assert 'CANCELLED_WITH_SCORE' in a['errors']


def test_unusual_score_not_invalid():
    a=s.inspect_record(parse('A v B  0-13')[0]);assert a['structurally_valid'] and 'UNUSUAL_SCORE' in a['flags']


def complete_schedule():
    names=[f'Team {i:02}' for i in range(18)];rotating=list(names);rows=[];line=1
    for leg in range(2):
        for rnd in range(17):
            d=date(2024,8,9)+timedelta(days=(17*leg+rnd)*7)
            for i in range(9):
                home,away=rotating[i],rotating[-1-i]
                if leg:home,away=away,home
                r=deepcopy(parse()[0]);r.update(home=home,away=away,date=d.isoformat(),round=17*leg+rnd+1,source_line=line,audit_id=str(line));rows.append(r);line+=1
            rotating=[rotating[0],rotating[-1],*rotating[1:-1]]
    return rows


def test_all_directed_pairings_and_rounds():
    rows=complete_schedule();a=s.season_check(rows,2024,True)
    assert a['observed']==a['valid']==306 and a['clubs']==18
    assert not a['missing_pairings'] and not a['duplicate_pairings'] and not a['format_issues']


def test_missing_fixture_visible():
    rows=complete_schedule();rows.pop();a=s.season_check(rows,2024,True)
    assert len(a['missing_pairings'])==1 and 'OBSERVED_COUNT' in a['format_issues']


def test_duplicate_conflicting_fixture_visible():
    rows=complete_schedule();duplicate=deepcopy(rows[0]);duplicate.update(audit_id='duplicate',FT='0-3',hg='0',ag='3',HT=None);rows.append(duplicate);a=s.season_check(rows,2024,True)
    assert a['duplicate_pairings'][0]['conflicting']


def test_source_order_and_long_span_not_corrections():
    rows=complete_schedule();rows[0]['date']='2024-10-01';before=[r['date'] for r in rows];a=s.season_check(rows,2024,True)
    assert a['wide_rounds'] and a['reversals'];assert [r['date'] for r in rows]==before


def test_same_day_team_collision_visible():
    rows=complete_schedule();rows[9]['date']=rows[0]['date'];a=s.season_check(rows,2024,True);assert a['same_day_collisions']


def test_casefold_identity_collision_not_merged():
    rows=complete_schedule();rows[0]['home']='TEAM 00';a=s.season_check(rows,2024,True);assert a['normalized_label_collisions'];assert rows[0]['home']=='TEAM 00'


def test_original_binding_tampering():
    rows=parse();prior=deepcopy(rows);rows[0]['source_line']=999
    with pytest.raises(ValueError):s.reconcile_rows(rows,prior)


def test_ambiguous_audit_id_rejected():
    rows=parse()
    with pytest.raises(ValueError):s.reconcile_rows(rows+rows,rows)


def test_conditional_conflicts_preserved_without_policy():
    h=parse('NEC Nijmegen v Vitesse  1-3');m=parse('NEC v SBV Vitesse  1-2');m[0]['date']='2024-08-10';before=deepcopy((h,m));maps=[dict(historical='NEC Nijmegen',modern='NEC',status='DIAGNOSTIC_ONLY_NOT_APPROVED_ALIAS'),dict(historical='Vitesse',modern='SBV Vitesse',status='DIAGNOSTIC_ONLY_NOT_APPROVED_ALIAS')]
    pair=s.compare_sources(h,m,maps)['matches'][0];assert not pair['date_equal'] and not pair['score_equal'] and (h,m)==before


def test_ambiguous_label_mapping_rejected():
    rows=parse()
    with pytest.raises(ValueError):s.compare_sources(rows,rows,[dict(historical='A',modern='A',status='DIAGNOSTIC_ONLY_NOT_APPROVED_ALIAS')])


def test_duplicate_overlap_pair_rejected():
    rows=parse()
    with pytest.raises(ValueError):s.compare_sources(rows+rows,rows,[])


def test_missing_source_record_remains_missing():
    h=parse('A v B  1-0');m=parse('A v B  1-0\nB v A [cancelled]');r=s.compare_sources(h,m,[]);assert len(r['matches'])==1 and len(r['unmatched_modern'])==1


def test_reserves_distinct():
    rows=parse('Ajax v Jong Ajax  1-0\nPSV v Jong PSV  0-0');a=s.season_check(rows,2024,False);assert len(a['team_labels'])==4


def test_frozen_evidence_and_append_only_log(tmp_path,monkeypatch):
    directory=tmp_path/'private';directory.mkdir();f=tmp_path/'frozen';f.write_bytes(b'original');log=tmp_path/'PLANNING_LOG.md';log.write_bytes(b'log\n');monkeypatch.setattr(s.acquisition,'protect',lambda *a:None)
    (directory/s.BASELINE).write_bytes(s.c.encode(dict(files={'frozen':s.c.sha(b'original')},planning_log=dict(bytes=4,sha256=s.c.sha(b'log\n')))))
    s.protect(directory,tmp_path);log.write_bytes(b'log\nappend\n');s.protect(directory,tmp_path);f.write_bytes(b'changed')
    with pytest.raises(ValueError):s.protect(directory,tmp_path)
