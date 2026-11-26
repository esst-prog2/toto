"""Synthetic Belgian Phase 2 checks: no private data or network dependency."""
from copy import deepcopy
import csv, io, json
from pathlib import Path
import pytest
from scripts import collect_belgian_pro_league_feasibility as c
from scripts import validate_belgian_pro_league_feasibility as v


def receipt(raw,path='synthetic'):
    return dict(path=path,sha256=c.sha(raw),commit='test',git_blob_sha1='testblob',url='https://example.invalid/original',encoding='utf-8-sig')


def text(body='A v B  2-1 (1-0)',year=2023,stage='Matchday 1',day='Fri Aug 4 2023'):
    return f'= Belgium First Division A {year}/{(year+1)%100:02}\n▪ {stage}\n{day}\n{body}\n'.encode()


def parse(body='A v B  2-1',**kwargs):
    raw=text(body,**kwargs);return v.parse_text(raw,kwargs.get('year',2023),receipt(raw))[0]


def historical(cells=None):
    f=io.StringIO(newline='');w=csv.writer(f);w.writerow(v.CSV_COLUMNS);w.writerow(cells or ['1995-08-04','1995','A','B','3-1','3','1','B1','1','4','2','H']);return f.getvalue().encode()


def test_exact_seven_original_boundary():
    plan=c.plan();assert len(plan)==7 and len({x['url'] for x in plan})==7
    assert [x['original_path'] for x in plan]==['data-raw/belgium.csv','2018-19/be1.txt','2019-20/be1.txt','2023-24/be1.txt','2025-26/be1.txt','tablesb/belg93.html','tablesb/belg2010.html']
    assert all(x['expected_blob'] is None and x['commit'] is None for x in plan[-2:])
    assert all('football-data' not in x['url'] and '2026-27' not in x['url'] for x in plan)


def test_unapproved_request_rejected_before_network(tmp_path):
    with pytest.raises(ValueError,match='Unapproved'):c.request(dict(url='https://example.invalid'),tmp_path)


def test_atomic_immutable_save(tmp_path):
    path=tmp_path/'x';c.save(path,b'a')
    with pytest.raises(FileExistsError):c.save(path,b'b')
    c.keep(path,b'a')
    with pytest.raises(ValueError):c.keep(path,b'b')
    assert path.read_bytes()==b'a' and not list(tmp_path.glob('.pending-*'))


@pytest.mark.parametrize('index,value,issue',[(0,'04/08/1995','INVALID_DATE'),(4,'1-3','FT_CONTRADICTION'),(5,'','INVALID_SCORE'),(5,'1.0','INVALID_SCORE'),(5,'-1','INVALID_SCORE'),(7,'B2','WRONG_COMPETITION'),(8,'2','WRONG_COMPETITION'),(9,'6','GOAL_DERIVED_CONTRADICTION'),(10,'0','GOAL_DERIVED_CONTRADICTION'),(11,'A','OUTCOME_CONTRADICTION')])
def test_csv_preserves_and_reports_contradictions(index,value,issue):
    cells=['1995-08-04','1995','A','B','3-1','3','1','B1','1','4','2','H'];cells[index]=value
    raw=historical(cells);r=v.parse_csv(raw,receipt(raw))[0]
    assert issue in r['field_issues'] and r['original_fields'][v.CSV_COLUMNS[index]]==value


def test_csv_source_line_binding_no_stage_invention():
    raw=historical();r=v.parse_csv(raw,receipt(raw))[0]
    assert r['stage']=='UNKNOWN' and r['source_line']==2 and not r['field_issues']
    assert r['physical_record_sha256']==c.sha(raw.splitlines(keepends=True)[1]) and 'match_id' not in r


@pytest.mark.parametrize('stage,expected',[('Matchday 1','REGULAR_SEASON'),('1. Round','REGULAR_SEASON'),('Playoff I, Matchday 1','CHAMPIONSHIP'),('Championship, Matchday 1','CHAMPIONSHIP'),('Europe, Matchday 1','EUROPE'),('Relegation, Matchday 1','PLAYDOWNS'),('ECL Playoff, Final','EUROPE_QUALIFICATION')])
def test_explicit_stage_grammar(stage,expected):
    assert parse(stage=stage)[0]['stage']==expected


@pytest.mark.parametrize('body,score,note',[('A v B',None,''),('A v B [cancelled]',None,'[cancelled]'),('A v B  0-5 [awarded]','0-5','[awarded]'),('A v B  7-0','7-0','')])
def test_source_annotation_not_disposition(body,score,note):
    r=parse(body)[0];assert r['FT']==score and r['annotation']==note and 'disposition' not in r


@pytest.mark.parametrize('change',[lambda x:x.replace(b'First Division A',b'Cup'),lambda x:x.replace(b'Fri Aug 4 2023',b'Thu Aug 4 2023'),lambda x:x.replace(b'Matchday 1',b'Matchday 31'),lambda x:x.replace(b'Matchday 1',b'Unknown 1'),lambda x:x.replace(b'Fri Aug 4 2023\n',b''),lambda x:x.replace(b'2-1 (1-0)',b'2-?'),lambda x:x+b'unknown\n'])
def test_unknown_or_inconsistent_grammar_fails(change):
    raw=change(text())
    with pytest.raises(ValueError):v.parse_text(raw,2023,receipt(raw))


@pytest.mark.parametrize('parser,raw,year',[(v.parse_csv,historical(),None),(v.parse_text,text(),2023)])
def test_checksum_tamper_rejected(parser,raw,year):
    with pytest.raises(ValueError):parser(raw+b' ',receipt(raw)) if year is None else parser(raw+b' ',year,receipt(raw))


def test_legitimate_playoff_rematch_is_not_lost():
    regular=parse()[0];playoff=parse(stage='Championship, Matchday 1',day='Fri Apr 5 2024')[0]
    a=v.assess([regular,playoff],2023)
    assert len(a['pairing_repeats'])==1 and a['pairing_repeats'][0]['kind']=='CROSS_STAGE_REPEAT'
    assert v.diagnostic_identity(regular)!=v.diagnostic_identity(playoff) and not a['duplicate_diagnostic_identities']


def test_exact_duplicate_diagnostic_identity_is_visible():
    r=parse()[0];assert len(v.assess([r,deepcopy(r)],2023)['duplicate_diagnostic_identities'])==1


def test_overlap_matches_by_date_across_stages_without_collapsing():
    regular=parse()[0];playoff=parse(stage='Championship, Matchday 1',day='Fri Apr 5 2024')[0]
    h=[deepcopy(regular),deepcopy(playoff)]
    for i,r in enumerate(h):r.update(stage='UNKNOWN',home='Historical A',away='Historical B',audit_id='historical'+str(i))
    result=v.overlap(h,[regular,playoff])
    assert result['candidate_event_matches']==2 and not result['unmatched_historical'] and result['matched_modern_stage_counts']=={'REGULAR_SEASON':1,'CHAMPIONSHIP':1}
    assert h[0]['stage']=='UNKNOWN'


def test_overlap_score_disagreement_not_hidden():
    modern=parse('\n'.join('A v B  2-1' for _ in range(6)))
    # Distinct dates provide enough unaffected signature evidence for candidate names.
    for i,r in enumerate(modern):r.update(date=f'2023-08-{i+4:02}',audit_id='m'+str(i),away='B'+str(i))
    hist=deepcopy(modern)
    for i,r in enumerate(hist):r.update(audit_id='h'+str(i),stage='UNKNOWN')
    hist[0].update(FT='0-0',hg='0',ag='0')
    # B0 cannot be inferred with only a conflicting signature: retain unmatched, never force.
    result=v.overlap(hist,modern)
    assert result['candidate_event_matches']==5 and len(result['unmatched_historical'])==1


def test_overlap_season_guard():
    a=parse();b=deepcopy(a);b[0]['season']='2024/2025'
    with pytest.raises(ValueError):v.overlap(a,b)


@pytest.mark.parametrize('year,n',[(1990,18),(2002,18),(2009,16),(2019,16),(2020,18),(2022,18),(2023,16),(2025,16)])
def test_expected_slots_never_force_observation_count(year,n):
    rs=parse();rs[0]['date']=f'{year}-08-04';a=v.assess(rs,year)
    assert a['observed']==1 and a['nominal_regular_slots']==n*(n-1)


def test_rsssf_standings_not_misread_as_fixtures():
    raw=b'<title>Belgium 2009/10</title>\n<b><a name="reg">Regular Stage</a></b>\n1.Club A  28 10 8 10  30-20 38\nRound 1 [Aug 1]\nA 1-2 B [annulled]\nC awd D [annulled; awarded 5-0]\nE n/p F\n'
    a=v.rsssf(raw,receipt(raw));assert a['fixture_candidates']==3
    assert a['score_token_counts']=={'NUMERIC':1,'awd':1,'n/p':1}
    assert a['fixture_line_candidates'][0]['away']=='B' and a['fixture_line_candidates'][0]['annotation']=='[annulled]'
    assert a['fixture_line_candidates'][0]['source_line_sha256']==c.sha(raw.splitlines(keepends=True)[4])


def test_rsssf_early_standings_cannot_create_dates():
    raw=b'<title>Belgium 1992/93</title>\nFinal Table:\n1.Club A 34 10 10 14 30-40 30\n'
    a=v.rsssf(raw,receipt(raw));assert a['standings_only'] and not a['fixture_line_candidates']


def test_cache_verification_requires_immutable_receipt(tmp_path):
    item=c.plan()[0];raw=b'bad';rec=dict(item,sha256=c.sha(raw),bytes=len(raw),licensing=c.RIGHTS[c.HIST],retrieved_at_utc='today',attribution='author',git_blob_sha1=item['expected_blob'])
    target=tmp_path/item['path'];target.parent.mkdir(parents=True);target.write_bytes(raw)
    with pytest.raises(ValueError):c.verify_record(tmp_path,item,rec)


def test_conflict_detected_after_unaffected_evidence_links_labels():
    modern=[]
    for i in range(6):
        r=parse()[0];r.update(date=f'2023-08-{i+4:02}',audit_id='m'+str(i));modern.append(r)
    hist=deepcopy(modern)
    for i,r in enumerate(hist):r.update(audit_id='h'+str(i),stage='UNKNOWN',home='Historic A',away='Historic B')
    hist[0].update(FT='0-0',hg='0',ag='0')
    o=v.overlap(hist,modern)
    assert o['candidate_event_matches']==6 and o['score_conflicts']==1


def test_inferred_prefix_does_not_rewrite_unknown_stage():
    rs=parse('A v B  1-0\nB v A  0-1\nA v B  2-2')
    for r in rs:r['stage']='UNKNOWN'
    a=v.assess(rs,2023)
    assert a['provisional_pairing_partition']['candidate_regular']==2
    assert a['provisional_pairing_partition']['additional_observations']==1
    assert all(r['stage']=='UNKNOWN' for r in rs)


def test_invalid_goals_remain_actionable_in_assessment():
    raw=historical(['1995-08-04','1995','A','B','?-1','?','1','B1','1','4','2','H'])
    rs=v.parse_csv(raw,receipt(raw));a=v.assess(rs,1995)
    assert 'INVALID_SCORE' in a['invalid'][0]['issues']
