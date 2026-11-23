"""Synthetic pinned acquisition and lossless inventory checks; no private sources."""
from copy import deepcopy
import csv,io,json
import pytest
from scripts import collect_primeira_liga_history as a
from scripts import inventory_primeira_liga_history as v
from scripts import validate_primeira_liga_feasibility as old
c=a.c


def receipt(raw,path='synthetic'):
    return dict(path=path,sha256=c.sha(raw),commit='revision',git_blob_sha1='blob',url='https://example.invalid/original')


def csv_bytes(rows=None):
    out=io.StringIO(newline='');w=csv.writer(out);w.writerow(old.CSV_COLUMNS);w.writerows(rows or [['2011-08-14','2011','Feirense ','Nacional','0-0','0','0','P1','1','0','0','D']]);return out.getvalue().encode()


def txt(year=2024,body='SL Benfica v FC Porto  2-1 (1-0)',day='Fri Aug 9 2024'):
    return f'= Portuguese Primeira Liga {year}/{(year+1)%100:02}\n▪ Matchday 1\n{day}\n{body}\n'.encode()


def test_only_three_exact_pinned_paths():
    items=a.plan();assert len(items)==3 and [x['season'] for x in items]==['2020/2021','2022/2023','2023/2024']
    assert all(x['commit']=='63df627f3c87ce71708f016522ea236cf74332c3' for x in items)
    assert [x['expected_bytes'] for x in items]==[24866,25043,25093]
    assert len({x['url'] for x in items})==3 and all(x['original_path'].endswith('_pt1.txt') for x in items)


def test_independent_historical_parser_preserves_entire_observation():
    raw=csv_bytes();r=receipt(raw)
    assert v.historical(raw,r)==old.parse_csv(raw,r)
    x=v.historical(raw,r)[0];assert x['home']=='Feirense ' and x['source_line']==2
    assert x['physical_record_sha256']==c.sha(raw.splitlines(keepends=True)[1]) and 'match_id' not in x


@pytest.mark.parametrize('column,value,issue',[(0,'bad','INVALID_DATE'),(4,'1-0','FT_CONTRADICTION'),(5,'','INVALID_SCORE'),(5,'-1','INVALID_SCORE'),(6,'1.0','INVALID_SCORE'),(7,'P2','WRONG_COMPETITION'),(8,'2','WRONG_COMPETITION'),(9,'2','GOAL_DERIVED_CONTRADICTION'),(10,'1','GOAL_DERIVED_CONTRADICTION'),(11,'A','OUTCOME_CONTRADICTION')])
def test_bad_source_values_remain_explicit(column,value,issue):
    row=['2011-08-14','2011','A','B','0-0','0','0','P1','1','0','0','D'];row[column]=value;raw=csv_bytes([row]);r=v.historical(raw,receipt(raw))[0]
    assert issue in r['field_issues'] and r['original_fields'][old.CSV_COLUMNS[column]]==value


@pytest.mark.parametrize('year,day',[(2018,'Fri Aug 10 2018'),(2019,'Sun Jul 26 2020'),(2020,'Fri Sep 18 2020'),(2021,'Fri Aug 6 2021'),(2022,'Fri Aug 5 2022'),(2023,'Fri Aug 11 2023'),(2024,'Fri Aug 9 2024'),(2025,'Fri Aug 8 2025')])
def test_all_modern_seasons_match_separate_parser(year,day):
    raw=txt(year,day=day);r=receipt(raw);assert v.modern(raw,year,r)==old.parse_text(raw,year,r)


@pytest.mark.parametrize('change',[lambda r:r.replace(b'Portuguese Primeira Liga',b'Portuguese Segunda Liga'),lambda r:r.replace(b'Fri Aug 9 2024',b'Thu Aug 9 2024'),lambda r:r.replace(b'2-1 (1-0)',b'2-?'),lambda r:r.replace(b'Matchday 1',b'Matchday 35'),lambda r:r.replace(b'Fri Aug 9 2024\n',b''),lambda r:r+b'unknown\n'])
def test_unknown_grammar_fails(change):
    raw=change(txt())
    with pytest.raises(ValueError):v.modern(raw,2024,receipt(raw))


def test_wrong_checksum_fails_for_both_sources():
    raw=txt();r=receipt(raw);r['sha256']='bad'
    with pytest.raises(ValueError):v.modern(raw,2024,r)
    with pytest.raises(ValueError):v.historical(csv_bytes(),r)


def test_whitespace_hypothesis_changes_only_target_copy():
    names=['Feirense','Nacional']+[f'C{i}' for i in range(14)]
    rows=[['2011-08-14','2011','Feirense ' if h=='Feirense' and away=='Nacional' else h,away,'0-0','0','0','P1','1','0','0','D'] for h in names for away in names if h!=away]
    raw=csv_bytes(rows);records=v.historical(raw,receipt(raw));before=deepcopy(records);result=v.whitespace_diagnostic(records)
    assert records==before and result['literal']['clubs']==17 and len(result['literal']['missing_pairings'])==32
    assert result['hypothetical_whitespace_only']['clubs']==16 and not result['hypothetical_whitespace_only']['missing_pairings'] and not result['hypothetical_whitespace_only']['duplicate_pairings']
    assert result['original_observation']['home']=='Feirense ' and len(result['related_observations'])==30


def test_missing_or_ambiguous_whitespace_selector_fails():
    raw=csv_bytes();rs=v.historical(raw,receipt(raw))
    with pytest.raises(ValueError):v.whitespace_diagnostic([])
    with pytest.raises(ValueError):v.whitespace_diagnostic(rs+rs)


def test_ordinary_source_dates_are_not_availability():
    raw=txt(body='Belenenses SAD v SL Benfica  0-7 (0-7)');rs,_=v.modern(raw,2024,receipt(raw));assert 'AVAILABILITY_CERTIFICATION' in rs[0]['date_semantics']
    assert not any('disposition' in x or 'match_id' in x for x in rs)


def test_stage_and_annotation_preservation():
    raw=txt()+b'\xe2\x96\xaa Playoff Final\nSat Aug 10\nA v B  0-3 [awarded]\n';rs,_=v.modern(raw,2024,receipt(raw));assert rs[-1]['stage']=='OTHER_STAGE' and rs[-1]['annotation']=='[awarded]'


def test_wide_and_reverse_round_are_flags_only():
    raw=txt()+b'Fri Sep 6 2024\nA v B  1-0\nThu Sep 5 2024\nC v D  0-0\n';rs,_=v.modern(raw,2024,receipt(raw));s=v.summarize(rs,2024)
    assert s['observed']==3 and len(s['wide_rounds'])==1 and len(s['source_order_reversals'])==1


def test_unapproved_network_item_fails_without_request(tmp_path,monkeypatch):
    monkeypatch.setattr(a,'build_opener',lambda *args:pytest.fail('Network forbidden'))
    with pytest.raises(ValueError):a.request({'url':'https://example.invalid/unapproved'},tmp_path)


def test_access_stop_persists_without_retry(tmp_path,monkeypatch):
    c.save(tmp_path/'phase3_access'/'ACCESS_STOP.json',b'{}');monkeypatch.setattr(a,'build_opener',lambda *args:pytest.fail('Network forbidden'))
    with pytest.raises(RuntimeError):a.request(a.plan()[0],tmp_path)


def test_frozen_evidence_tampering_fails(tmp_path,monkeypatch):
    monkeypatch.setattr(c,'protect',lambda *args:{})
    original=tmp_path/'frozen';original.write_bytes(b'a');log=tmp_path/'PLANNING_LOG.md';log.write_bytes(b'log\n')
    c.save(tmp_path/'phase3_protected_before.json',c.encode(dict(files={'frozen':c.sha(b'a')},planning_log=dict(bytes=4,sha256=c.sha(b'log\n')),approval='PHASE3_THREE_MODERN_ORIGINALS_ONLY')))
    assert a.protect(tmp_path,tmp_path)['phase2_frozen_entries']==1
    original.write_bytes(b'b')
    with pytest.raises(ValueError,match='Frozen Phase2'):a.protect(tmp_path,tmp_path)


def test_duplicate_pair_is_reported_not_dropped():
    raw=txt(body='A v B  1-0\nA v B  0-3');rs,_=v.modern(raw,2024,receipt(raw));s=v.summarize(rs,2024)
    assert s['observed']==2 and s['duplicate_pairings'][0]['conflicting']


def test_literal_reserve_identity_and_accent_preserved():
    raw=txt(body='Benfica v Benfica B  1-0\nVitória SC v Vitória FC  0-0');rs,_=v.modern(raw,2024,receipt(raw));s=v.summarize(rs,2024)
    assert s['clubs']==4 and s['reserve_labels']==['Benfica B'] and rs[1]['home']=='Vitória SC'
