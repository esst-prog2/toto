"""Synthetic Ligue 1 feasibility checks; no private data or network required."""
from copy import deepcopy
import csv
import io
import json
from unittest.mock import patch

import pytest

from scripts import collect_ligue1_feasibility as c
from scripts import validate_ligue1_feasibility as v


def text(body, year=2014):
    return (f'= French Ligue 1 {year}/{str(year+1)[-2:]}\n'+body).encode()


def parsed(body='Alpha v Béta  1-0 (0-0)', year=2014):
    return v.parse_text(text('▪ Matchday 1\nFri Aug 8 2014\n'+body+'\n',year),year)[0]


def test_exact_scope_and_immutable_revisions():
    assert sum(len(s[3]) for s in c.SOURCES) == 7
    assert c.SOURCES[0][1] == '872c5c354161ace8408f3091b758c6af4cccca94'
    assert c.SOURCES[1][1] == '63df627f3c87ce71708f016522ea236cf74332c3'
    assert c.SOURCES[0][3] == ('data-raw/france.csv',)
    assert c.SOURCES[1][3] == tuple('france/'+p for p in (
        '2014-15_fr1.txt','2016-17_fr1.txt','2019-20_fr1.txt','2023-24_fr1.txt',
        '2025-26_fr1.txt','2025-26_fr1-full.txt'))
    assert all('football-data' not in s[0] and '2026-27' not in ''.join(s[3]) for s in c.SOURCES)


def test_tree_fail_closed_for_missing_path_or_wrong_commit():
    tree=dict(sha='pin',truncated=False,tree=[dict(path='approved',type='blob',sha='x',size=1)])
    assert c.tree_entries(c.encode(tree),'pin',['approved'])['approved']['size']==1
    for commit,paths in [('wrong',['approved']),('pin',['absent'])]:
        with pytest.raises(ValueError):c.tree_entries(c.encode(tree),commit,paths)
    tree['truncated']=True
    with pytest.raises(ValueError):c.tree_entries(c.encode(tree),'pin',['approved'])


def test_blob_binds_exact_bytes_not_only_file_size():
    import hashlib
    raw=b'abc\r\n';entry=dict(size=len(raw),sha=hashlib.sha1(b'blob 5\0'+raw).hexdigest())
    assert c.verify_blob(raw,entry)==entry['sha']
    with pytest.raises(ValueError):c.verify_blob(b'xyz\r\n',entry)
    with pytest.raises(ValueError):c.verify_blob(b'abc\n',entry)


def test_save_never_overwrites_original(tmp_path):
    p=tmp_path/'source';c.save(p,b'original')
    with pytest.raises(FileExistsError):c.save(p,b'changed')
    assert p.read_bytes()==b'original'


def test_access_failure_stops_without_retry(tmp_path):
    with patch.object(c,'build_opener',side_effect=OSError('access denied')) as opener:
        with pytest.raises(OSError):c.request('https://example.invalid/approved',tmp_path)
        with pytest.raises(RuntimeError):c.request('https://example.invalid/approved',tmp_path)
    assert opener.call_count==1 and (tmp_path/'ACCESS_STOP.json').exists()


def test_redirect_is_rejected():
    with pytest.raises(ValueError):c.NoRedirect().redirect_request(None,None,302,'',{},'https://other.invalid')


def test_protection_allows_append_only_planning_and_detects_data_mutation(tmp_path):
    root=tmp_path;directory=root/'data/private/france/ligue_1';directory.mkdir(parents=True)
    (root/'old.csv').write_bytes(b'private');(root/'code.py').write_bytes(b'public');(root/'PLANNING_LOG.md').write_bytes(b'history\n')
    c.save(directory/'protected_before.json',c.encode(dict(private={'old.csv':c.sha(b'private')},public={'code.py':c.sha(b'public')},planning_log=dict(bytes=8,sha256=c.sha(b'history\n')))))
    (root/'PLANNING_LOG.md').write_bytes(b'history\nappended\n');assert c.protect(directory,root)==dict(private=1,public=1)
    (root/'old.csv').write_bytes(b'changed')
    with pytest.raises(ValueError,match='Protected file changed'):c.protect(directory,root)


def test_fixture_unicode_and_literal_award_kept():
    r=parsed('Alpha v Béta  0-0 [awarded]')[0]
    assert r['away']=='Béta' and r['FT']=='0-0' and r['source_marked_awarded']
    assert r['raw_record']=='Alpha v Béta  0-0 [awarded]'
    assert v.outcome(0,0)=='D' # goal-derived only, never administrative winner


def test_cancelled_fixture_has_no_invented_zero_score():
    r=parsed('Alpha v Béta [cancelled]')[0]
    assert r['hg'] is r['ag'] is r['FT'] is None
    s=v.assess([r],2014);assert (s['observed'],s['scored'],s['unscored'])==(1,0,1)


def test_missing_score_non_cancelled_also_remains_null():
    assert parsed('Alpha v Béta')[0]['FT'] is None


@pytest.mark.parametrize('body',['Alpha v Béta  2-?','Alpha v Béta  ?-2','Alpha  nonsense  Béta'])
def test_malformed_score_is_not_unscored_or_a_team_name(body):
    with pytest.raises(ValueError):parsed(body)


def test_score_middle_scorer_multiline_and_crlf():
    raw=text("▪ Matchday 1\nFri Aug 8 2014\n20:30  Alpha  2-1 (1-0)  Béta\n (Scorer 10';\n Other 50')\n").replace(b'\n',b'\r\n')
    rows,notes=v.parse_text(raw,2014)
    assert rows[0]['FT']=='2-1' and rows[0]['HT']=='1-0'
    assert sum(n['kind']=='scorer_annotation' for n in notes)==2


def test_full_details_not_misparsed_as_fixtures():
    raw=text("▪ Regular Season - 1\nFri Aug 8 20:30 UTC+2 @ Stadium, Att: 100\n Alpha v Béta  1-0\nAlpha: A [c] - B\n      C, D\n Yellow: A 20'\nBéta: E - F\nRefs: Official\n")
    rows,notes=v.parse_text(raw,2014,full=True)
    assert len(rows)==1 and rows[0]['date']=='2014-08-08' and not rows[0]['year_explicit']
    assert sum(n['kind']=='detail_continuation' for n in notes)==1


def test_full_unknown_detail_fails():
    raw=text('▪ Matchday 1\nFri Aug 8 2014\nAlpha v Béta  1-0\nUnrecognized detail\n')
    with pytest.raises(ValueError,match='Unknown'):v.parse_text(raw,2014,full=True)


@pytest.mark.parametrize('s',['Thu Aug 8 2014','Fri Aug 8 2015','Sun Feb 30 2014'])
def test_invalid_weekday_or_season_date_fails(s):
    with pytest.raises(ValueError):v.parse_text(text('▪ Matchday 1\n'+s+'\nAlpha v Beta  0-0\n'),2014)


def test_year_inference_and_explicit_year_are_distinguished():
    assert v.parse_date('Fri Aug 8',2014)['date']=='2014-08-08'
    assert not v.parse_date('Fri Aug 8',2014)['year_explicit']
    assert v.parse_date('Fri Aug 8 2014',2014)['year_explicit']


def test_repeated_round_heading_can_hold_rescheduled_fixture():
    raw=text('▪ Matchday 1\nFri Aug 8 2014\nAlpha v Beta  0-0\n▪ Matchday 1\nFri Sep 5\nGamma v Delta  1-0\n')
    rows,_=v.parse_text(raw,2014);s=v.assess(rows,2014)
    assert len(s['wide_rounds'])==1 and s['wide_rounds'][0]['span_days']==28
    assert len(s['wide_rounds'][0]['fixtures'])==2 and not s['duplicate_directed_pairs']


def test_new_round_cannot_inherit_old_date():
    with pytest.raises(ValueError,match='without'):v.parse_text(text('▪ Matchday 1\nFri Aug 8 2014\nAlpha v Beta  0-0\n▪ Matchday 2\nGamma v Delta  1-0\n'),2014)


def test_other_stage_is_visible_not_regular():
    rows,_=v.parse_text(text('▪ Promotion Playoff Final\nFri Aug 8 2014\nAlpha v Beta  1-0\n'),2014)
    assert rows[0]['stage']=='OTHER_STAGE'


@pytest.mark.parametrize('title',['= French Ligue 2 2014/15','= French Ligue 1 2015/16'])
def test_wrong_competition_or_season_fails(title):
    with pytest.raises(ValueError):v.parse_text((title+'\n▪ Matchday 1\nFri Aug 8 2014\nAlpha v Beta  1-0').encode(),2014)


def csv_bytes(records):
    f=io.StringIO();w=csv.DictWriter(f,fieldnames=['Date','Season','home','visitor','FT','hgoal','vgoal','division','tier','totgoal','goaldif','result']);w.writeheader();w.writerows(records)
    return f.getvalue().encode()


def hist_record(**updates):
    return dict(Date='2014-08-08',Season='2014',home='Alpha',visitor='Beta',FT='0-2',hgoal='0',vgoal='2',division='1',tier='1',totgoal='2',goaldif='-2',result='D',**updates)


def test_historical_contradictory_derived_label_preserved_and_flagged():
    rows=v.historical(csv_bytes([hist_record()]));s=v.assess(rows,2014)
    assert rows[0]['source_fields']['result']=='D' and rows[0]['FT']=='0-2'
    assert s['contradictions']==[dict(line=2,kind='RESULT_LABEL_GOALS_CONFLICT',source='D',goal_derived='A')]


def test_historical_july_proxy_and_same_day_collisions_visible():
    a=hist_record();a['Date']='2015-07-01';b=deepcopy(a);b.update(visitor='Gamma')
    s=v.assess(v.historical(csv_bytes([a,b])),2014)
    assert s['dates']['outside_or_invalid_lines']==[2,3] and s['team_date_collisions']


def test_historical_wrong_header_and_shape_fail():
    with pytest.raises(ValueError):v.historical(b'Date,Season\n2014-01-01,2014\n')
    raw=csv_bytes([hist_record()])+b'incomplete,row\n'
    with pytest.raises(ValueError):v.historical(raw)


def test_pairing_duplicates_and_identity_collision_are_not_normalized_away():
    rows=parsed();duplicate=deepcopy(rows[0]);duplicate['source_line']=99
    variant=deepcopy(rows[0]);variant['home']='ALPHA';variant['source_line']=100
    s=v.assess(rows+[duplicate,variant],2014)
    assert s['duplicate_directed_pairs'] and s['normalized_name_collisions']['alpha']==['ALPHA','Alpha']


def test_competition_size_and_covid_expectations():
    assert [v.expected_clubs(y) for y in (1990,1996,1997,2001,2002,2022,2023,2025)]==[20,20,18,18,20,20,18,18]
    s=v.assess([],2019);assert s['expected_scheduled']==380 and s['expected_played']==279
    assert v.expected_clubs(1932) is None


def test_compare_preserves_conflicting_dates_scores_and_missing_pairs():
    left=parsed();right=deepcopy(left);right[0].update(date='2014-08-09',hg='2')
    comparison=v.compare(left,right)
    assert comparison['matched_pairs']==1 and set(comparison['discrepancies'][0]['differences'])=={'date','hg'}
    assert left[0]['hg']=='1' and left[0]['date']=='2014-08-08'
    assert len(v.compare([],right)['unmatched_right'])==1


def test_compare_requires_explicit_bijective_mapping_and_exposes_duplicates():
    rows=parsed()
    with pytest.raises(ValueError):v.compare(rows,rows,{'Alpha':'same','Béta':'same'})
    with pytest.raises(ValueError):v.compare(rows,rows,{'Alpha':'Alpha'})
    assert v.compare(rows+rows,rows)['duplicate_left']==[['Alpha','Béta']]


def test_assessment_serialization_deterministic_and_goal_values_strict():
    assert c.encode(v.assess(parsed(),2014))==c.encode(v.assess(parsed(),2014))
    for g in ('-1','1.0','nan',True,1):
        with pytest.raises(ValueError):v.goals(g)
    assert v.goals('0')==0 and v.goals(None) is None


def fake_bundle():
    """Synthetic original/tree responses for the entire fixed allowlist."""
    import hashlib
    responses={}
    for repo,commit,notices,datasets in c.SOURCES:
        entries=[]
        for name in notices+datasets:
            raw=(b'CC0 1.0 Universal\n' if name=='LICENSE.md' else b'GPL >=2\n' if name=='DESCRIPTION'
                 else b'non-commercial use\n' if repo.startswith('jalapic/') and name=='README.md' else (name+' synthetic\n').encode())
            entries.append(dict(path=name,type='blob',size=len(raw),sha=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()))
            responses[f'https://raw.githubusercontent.com/{repo}/{commit}/{name}']=raw
        responses[f'https://api.github.com/repos/{repo}/git/trees/{commit}?recursive=1']=c.encode(dict(sha=commit,truncated=False,tree=entries))
    return responses


def test_acquisition_idempotent_exact_allowlist_and_receipt_integrity(tmp_path):
    responses=fake_bundle()
    with patch.object(c,'protect',return_value={'private':1,'public':1}), patch.object(c.time,'sleep'), patch.object(c,'request',side_effect=lambda url,d:responses[url]) as request:
        manifest=c.collect(tmp_path)
        calls=[x.args[0] for x in request.call_args_list]
        assert calls[:2]==[f'https://api.github.com/repos/{repo}/git/trees/{pin}?recursive=1' for repo,pin,_,_ in c.SOURCES]
        assert sum(r['kind']=='dataset' for r in manifest['files'])==7 and set(calls)==set(responses)
        count=request.call_count;assert c.collect(tmp_path)==manifest and request.call_count==count
        assert c.verify_originals(tmp_path)==manifest
        row=next(r for r in manifest['files'] if r['kind']=='dataset');(tmp_path/row['path']).write_bytes(b'tampered')
        with pytest.raises(ValueError):c.collect(tmp_path)
        with pytest.raises(ValueError):c.verify_originals(tmp_path)


def test_manifest_scope_and_provenance_url_tampering_fail(tmp_path):
    with patch.object(c,'protect',return_value={'private':1,'public':1}),patch.object(c.time,'sleep'),patch.object(c,'request',side_effect=lambda url,d:fake_bundle()[url]):
        manifest=c.collect(tmp_path)
    manifest['files'][0]['url']='https://unapproved.invalid'
    (tmp_path/'acquisition.json').write_bytes(c.encode(manifest))
    with pytest.raises(ValueError):c.verify_originals(tmp_path)
    manifest['files'].append(deepcopy(manifest['files'][0]));(tmp_path/'acquisition.json').write_bytes(c.encode(manifest))
    with pytest.raises(ValueError):c.verify_originals(tmp_path)
