"""Synthetic source/format/identity/reconciliation tests; no restricted fixtures."""
import csv
import io
import json
from pathlib import Path
import zipfile
import pytest
from scripts import uefa_europa_league_sources as s
from scripts import inventory_uefa_europa_league as p
from scripts import verify_uefa_europa_league_inventory as v


def rec(path='originals/rsssf/synthetic.html',season='2004/2005',publisher='synthetic'):
    return dict(path=path,season=season,publisher=publisher,sha256='a'*64)


def obs(oid,home='Alpha',away='Beta',day='2005-02-17',stage='Round of 32',publisher='one',season='2004/2005',**kw):
    r=s.observation(rec('originals/'+publisher+'.txt',season,publisher),oid,season,home,away,raw_fields={},when=day,raw_stage=stage,p=s.periods(regulation_time=[1,0],published_final=[1,0]),**kw)
    return r


@pytest.mark.parametrize('token,reg,extra,pens',[
 ('2-1 (1-0)',[2,1],None,None),('4-3 pen. 2-2 a.e.t. (1-1, 0-0)',[1,1],[2,2],[4,3]),('2-1 a.e.t.',None,[2,1],None)])
def test_txt_periods_and_original_score_annotation(token,reg,extra,pens):
    raw=('= UEFA Europa League 2024/25\n▪ Final\nWed May 21 2025\nAlpha (ABC) v Beta (DEF)  '+token+'\n').encode()
    rows,errors,_=s.parse_openfootball(raw,rec('2024-25/el.txt','2024/2025'))
    r=rows[0];assert not errors;assert r['periods']['regulation_time']==reg;assert r['periods']['after_extra_time']==extra;assert r['periods']['shootout']==pens
    assert r['source_fields']['score']==token and r['source_sha256']=='a'*64


@pytest.mark.parametrize('source,title',[('2024-25/el.txt','= UEFA Champions League 2024/25'),('2024-25/el.txt','= UEFA Europa League 2023/24')])
def test_wrong_competition_or_season_rejected(source,title):
    with pytest.raises(ValueError):s.parse_openfootball((title+'\n').encode(),rec(source,'2024/2025'))


def test_unrecognized_txt_line_accounted_as_exception():
    rows,errors,ledger=s.parse_openfootball(b'= UEFA Europa League 2024/25\nBAD FIXTURE\n',rec('2024-25/el.txt','2024/2025'))
    assert not rows and errors[0]['code']=='UNSUPPORTED_TXT_CANDIDATE' and ledger['raw_units']==1


@pytest.mark.parametrize('year,label,qual,when,expected',[
 (1990,'First Round',False,None,('MAIN','ROUND_1')),
 (1994,'Preliminary Round',False,None,('QUALIFYING','PRELIMINARY')),
 (2004,'Intermediate Round',False,None,('MAIN','ROUND_OF_32')),
 (2002,'Third Round',False,None,('MAIN','ROUND_OF_32')),
 (1996,'Third Round',False,None,('MAIN','ROUND_OF_16')),
 (2011,'First Round (Aug 18 and 25)',False,None,('QUALIFYING','QUALIFYING_PLAYOFF')),
 (2021,'Qualifying Round',False,None,('QUALIFYING','QUALIFYING_ROUND_3')),
 (2025,'Playoffs',False,'2026-02-19',('MAIN','KNOCKOUT_PLAYOFF')),
 (2025,'Playoff Round',False,'2025-08-21',('QUALIFYING','QUALIFYING_PLAYOFF')),
 (2024,'League, Matchday 1',False,None,('MAIN','LEAGUE_PHASE')),
 (2024,'Finals, Final',False,None,('MAIN','FINAL'))])
def test_historical_stage_rules(year,label,qual,when,expected):assert s.stage(year,label,qualifier=qual,when=when)==expected


@pytest.mark.parametrize('token,year,expected',[('[Mar 6]',2007,'2008-03-06'),('13 July 2006 Stadium',None,'2006-07-13'),('{{Start date|2026|2|19|df=y}}',None,'2026-02-19'),('2020-08-21',None,'2020-08-21')])
def test_date_representations(token,year,expected):assert s.parse_day(token,year)==expected


def test_round_schedule_never_promoted_to_actual_date():
    raw=b'<h2><a name="uefa">UEFA Cup</a></h2>First Round (Sep 16 and 30)\nAlpha Club               Eng  Beta Club                Sco   2-0  1-0  3-0\n<h2>Other Cup</h2>'
    rows,errors,_=s.parse_rsssf_summary(raw,rec())
    assert not errors and len(rows)==2
    assert all(r['date'] is None for r in rows)
    assert rows[0]['date_interval']==['2004-09-16']*2
    assert [rows[1]['home'],rows[1]['away']]==['Beta Club','Alpha Club']
    assert rows[1]['periods']['published_final']==[0,1] and rows[1]['periods']['aggregate']==[0,3]


def test_mixed_html_competitions_excluded():
    raw=b'<h2><a name="cc">Other</a></h2>Alpha Eng  Beta Sco  9-0\n<h2><a name="uefa">UEFA Cup</a></h2>\nFirst Round\nAlpha                    Eng  Beta                     Sco   1-0  2-0  3-0\n<h2>Super Cup</h2>Wrong Eng  Other Sco  8-0'
    rows,_,_=s.parse_rsssf_summary(raw,rec());assert len(rows)==2
    assert all(r['periods']['published_final'] not in ([9,0],[8,0]) for r in rows)


def test_all_caps_club_acronym_not_misparsed_as_country():
    raw=b'<h2><a name="uefa">UEFA Cup</a></h2>\nFirst Round\nAlpha                    Eng  Example ZTS Town    Tch   1-0  2-0  3-0\n<h2>Other</h2>'
    rows,_,_=s.parse_rsssf_summary(raw,rec());assert rows[0]['away']=='Example ZTS Town'


def test_goal_events_grouped_without_treating_running_scores_as_full_time():
    out=io.StringIO();w=csv.DictWriter(out,fieldnames=['game','date','season','GH','GA','time']);w.writeheader()
    for minute,gh,ga in [('10','1','0'),('80','1','1')]:w.writerow(dict(game='Alpha vs. Beta 1:1 \n(Hinspiel 2:0)',date='2005-03-10',season='2004-2005',GH=gh,GA=ga,time=minute))
    rows,errors,ledger=s.parse_goals(out.getvalue().encode(),rec('goals_time/europa-league.csv'))
    assert not errors and len(rows)==1 and ledger['represented_goal_rows']==2
    assert rows[0]['periods']['published_final']==[1,1] and rows[0]['periods']['aggregate'] is None and rows[0]['periods']['regulation_time'] is None


def wiki(raw,title='1990–91 UEFA Cup'):
    return json.dumps({'query':{'pages':[{'title':title,'revisions':[{'revid':123,'slots':{'main':{'content':raw}}}]}]}}).encode()


def test_named_wiki_args_do_not_shift_positional_leg_scores():
    source='==First round==\n{{TwoLegResult|[[Alpha]]|England|var1=1990|3–1|[[Beta]]|Scotland|2–0|1–1 {{aet}}}}'
    rows,errors,_=s.parse_wikipedia(wiki(source),rec(season='1990/1991'))
    assert not errors and len(rows)==2 and rows[0]['home']=='Alpha'
    assert rows[0]['periods']['published_final']==[2,0] and rows[1]['periods']['after_extra_time']==[1,1]


def test_lua_wiki_box_and_unexpanded_transclusion_accounted():
    source='{{#invoke:Football box|main|date={{Start date|2025|9|24}}|team1=[[Alpha]] {{#invoke:flag|fbaicon|ENG}}|team2=[[Beta]]|score=2–0}}\n{{#lst:2025–26 UEFA Europa League final|F}}'
    rows,errors,ledger=s.parse_wikipedia(wiki(source,'2025–26 UEFA Europa League league phase'),rec(season='2025/2026'))
    assert not errors and len(rows)==1 and rows[0]['home']=='Alpha' and rows[0]['date']=='2025-09-24'
    assert len(ledger['transclusions'])==1


def test_team_keys_keep_geography_and_do_not_merge_similar_clubs():
    assert s.team_key('Dinamo (Minsk)')!=s.team_key('Dinamo (Kyiv)')
    assert s.team_key('Manchester City')!=s.team_key('Manchester United')
    assert s.team_key('FC Köln')==s.team_key('Koln')
    for label in ['FC Köln','Dinamo (Minsk)','Brøndby IF','Łódź','Manchester United']:assert v.name(label)==s.team_key(label)


def test_two_distinct_dates_support_conditional_alias():
    rows=[obs('a','Alpha Club','Beta','2005-02-17',publisher='one'),obs('b','Alpha Alternative','Beta','2005-02-17',publisher='two'),obs('c','Beta','Alpha Club','2005-02-24',publisher='one'),obs('d','Beta','Alpha Alternative','2005-02-24',publisher='two')]
    mapping,labels,proofs=p.identities(rows)
    assert len(proofs)==1
    assert mapping[(rows[0]['season'],'one','Alpha Club')]==mapping[(rows[0]['season'],'two','Alpha Alternative')]


def test_single_coincidental_score_or_similar_name_never_merges_clubs():
    rows=[obs('a','Alpha','Beta',publisher='one'),obs('b','Gamma','Beta',publisher='two')]
    mapping,_,proofs=p.identities(rows);assert not proofs
    events,_,_=p.reconcile(rows,mapping);assert len(events)==2


def test_leg_orientation_and_repeated_meetings_replays_preserved():
    rows=[obs('a','Alpha','Beta',stage='Group Stage'),obs('b','Beta','Alpha','2005-02-24',stage='Group Stage'),obs('c','Alpha','Beta','2005-03-10',stage='Round of 16'),obs('d','Alpha','Beta','2005-03-12',stage='Round of 16',replay=True)]
    mapping,_,_=p.identities(rows);events,_,_=p.reconcile(rows,mapping);assert len(events)==4


def test_conflicting_dates_and_scores_remain_conditional_review_evidence():
    a=obs('a',publisher='one');b=obs('b',day='2005-02-18',publisher='two');b['periods']['regulation_time']=[0,1]
    rows=[a,b];mapping,_,_=p.identities(rows);events,_,dups=p.reconcile(rows,mapping)
    assert len(events)==1 and {'DATE_CONFLICT','SCORE_CONFLICT_REGULATION_TIME'}<=set(events[0]['flags'])
    queue=p.review_queue(events,[],dups,rows);assert queue[0]['priority']==1 and queue[0]['observations']


def test_neutral_orientation_preserved_and_flagged():
    a=obs('a','Alpha','Beta',stage='Final',publisher='one');b=obs('b','Beta','Alpha',stage='Final',publisher='two');b['periods']['regulation_time']=[0,1]
    rows=[a,b];mapping,_,_=p.identities(rows);events,_,_=p.reconcile(rows,mapping)
    assert len(events)==1 and 'SOURCE_ORIENTATION_CONFLICT'in events[0]['flags'] and 'SCORE_CONFLICT_REGULATION_TIME'not in events[0]['flags']
    assert a['home']=='Alpha' and b['home']=='Beta'


def test_same_source_two_dates_not_silently_deduplicated():
    rows=[obs('a'),obs('b',day='2005-02-18')];mapping,_,_=p.identities(rows)
    assert len(p.reconcile(rows,mapping)[0])==2


def test_multiple_possible_undated_matches_stay_separate():
    rows=[obs('a',stage='Group Stage'),obs('b',day='2005-03-17',stage='Group Stage'),obs('c',day=None,stage='Group Stage',publisher='two')]
    mapping,_,_=p.identities(rows);events,_,duplicates=p.reconcile(rows,mapping)
    assert len(events)==3 and len(duplicates)==1


def test_narrow_interval_retained_without_selecting_a_date():
    r=obs('a',day=None,interval=['2005-02-17','2005-02-18'])
    assert r['date'] is None and r['date_interval']==['2005-02-17','2005-02-18']


def test_admin_status_does_not_invent_regulation_or_played_result():
    r=s.observation(rec(),'a','2004/2005','Alpha','Beta',raw_fields={},raw_stage='First Round',status='awarded',p=s.periods(administrative_result=[3,0],published_final=[3,0]))
    assert r['periods']['regulation_time'] is None and 'EXCEPTIONAL_STATUS'in r['issues']


def test_early_two_leg_final_not_assumed_neutral():
    r=obs('a',stage='Final',season='1990/1991',day='1991-05-08')
    assert r['official_neutral_candidate']==0 and r['source_neutral_venue'] is None


def test_output_private_and_overwrite_guards(tmp_path,monkeypatch):
    with pytest.raises(ValueError):p.destination(p.ROOT/'data/leaked_inventory')
    monkeypatch.setattr(p,'build',lambda cache=None:{'summary.json':{'synthetic':1}})
    out=tmp_path/'phase2';p.run(out)
    with pytest.raises(FileExistsError):p.run(out)
    p.run(out,check=True)
    (out/'summary.json').write_text('{}')
    with pytest.raises(ValueError):p.run(out,check=True)


def test_structural_missing_candidates_are_not_fabricated_events():
    r=obs('a');mapping,_,_=p.identities([r]);events,_,_=p.reconcile([r],mapping);coverage=p.format_inventory([r],events,[])
    assert len(coverage)==36 and coverage[0]['expected_main_format_slots']==126
    assert coverage[14]['main_events']==1 and len(events)==1 and not events[0]['dispositions_assigned']


def test_bare_group_results_are_fixture_observations_not_standings():
    raw=b'<h2><a name="uefa">UEFA Cup</a></h2>\nGroup Phase\nGroup A\nOct 21: Alpha Club                   3  Beta Club                    0\nAlpha Club 4 2 1 1 6 3 7\n<h2>Other</h2>'
    rows,errors,_=s.parse_rsssf_summary(raw,rec())
    assert not errors and len(rows)==1 and rows[0]['stage']=='GROUP_STAGE' and rows[0]['date']=='2004-10-21'


def test_qualified_teams_heading_is_not_a_qualifying_round():
    assert s.stage(2002,'Qualified teams')==('UNKNOWN','UNKNOWN')
    source='==Qualified teams==\n{{football box|team1=[[Alpha]]|team2=[[Beta]]|score=1–0|date=19 September 2002}}'
    rows,_,_=s.parse_wikipedia(wiki(source,'2002–03 UEFA Cup first round'),rec(season='2002/2003'))
    assert rows[0]['scope']=='MAIN' and rows[0]['stage']=='ROUND_1'


def test_detail_date_before_header_and_internal_hyphen():
    raw='<h3><a name="uefadet">UEFA Cup Details</a></h3>\nFIRST ROUND\n20 September 2007 Stadium\nAlpha-Town – Beta Club 3-0\nAlpha-Town: Keeper / Players\nBeta Club: Keeper / Players\n<h3>Other</h3>'.encode()
    rows,errors,_=s.parse_rsssf_detail(raw,rec(season='2007/2008'))
    assert len(rows)==1 and rows[0]['home']=='Alpha-Town' and rows[0]['date']=='2007-09-20'


def test_schoch_period_flags_and_missing_display_name_preserved():
    import pyarrow as pa
    import pyarrow.parquet as pq
    from datetime import date
    records=[dict(home=None,away='Beta',home_ident='Alpha (England)',away_ident='Beta (Scotland)',date=date(2005,2,17),competition='UEFA EL',gh=5,ga=4,full_time='P'),dict(home='Other',away='Outside',home_ident='x',away_ident='y',date=date(2005,2,17),competition='UEFA CL',gh=1,ga=0,full_time='F')]
    b=io.BytesIO();pq.write_table(pa.Table.from_pylist(records),b)
    rows,errors,ledger=s.parse_schoch(b.getvalue(),rec('games.parquet'))
    assert len(rows)==1 and not errors and rows[0]['source_fields']['home'] is None
    assert rows[0]['home']=='Alpha' and rows[0]['periods']['regulation_time'] is None
    assert rows[0]['periods']['published_final']==[5,4] and ledger['excluded']['OTHER_COMPETITION']==1


@pytest.fixture
def synthetic_inventory(tmp_path,monkeypatch):
    base=tmp_path/'private';base.mkdir();(base/'phase1').mkdir();(base/'phase1/acquisition_manifest.json').write_text('[]')
    path='originals/openfootball/2024-25/el.txt';f=base/path;f.parent.mkdir(parents=True)
    raw=b'= UEFA Europa League 2024/25\n\xe2\x96\xaa Final\nWed May 21 2025\nAlpha (ABC) v Beta (DEF)  1-0 (1-0)\n'
    f.write_bytes(raw);record=dict(path=path,sha256=s.sha(raw),bytes=len(raw),publisher='openfootball/champions-league',kind='fixture',url='https://example.invalid/synthetic')
    rows,exceptions,ledger=s.parse_openfootball(raw,record)
    monkeypatch.setattr(p,'BASE',base);monkeypatch.setattr(v,'BASE',base)
    monkeypatch.setattr(p,'raw_inventory',lambda:(rows,exceptions,[dict(source=path,**ledger)],[record]))
    out=tmp_path/'output';p.run(out)
    return out,base,path


def test_independent_raw_reconstruction_passes_synthetic_inventory(synthetic_inventory):
    out,_,_=synthetic_inventory;result=v.verify(out)
    assert result['status']=='PASS' and result['all_observations_accounted_once']


@pytest.mark.parametrize('change',['original','regulation','date','team','locator','membership','period_projection'])
def test_independent_verifier_rejects_tampering(synthetic_inventory,change):
    out,base,path=synthetic_inventory
    if change=='original':(base/path).write_bytes(b'changed')
    elif change in ('membership','period_projection'):
        target=out/'event_inventory.json';value=json.loads(target.read_bytes());e=value['events'][0]
        if change=='membership':e['observations']=[]
        else:e['score_evidence']['regulation_time'][0]['value']=[8,8]
        target.write_bytes(s.encode(value))
    else:
        target=out/'source_inventory.json';value=json.loads(target.read_bytes());r=value['observations'][0]
        if change=='regulation':r['periods']['regulation_time']=[9,9]
        elif change=='date':r['date']='2025-05-22'
        elif change=='team':r['home']='Wrong Club'
        else:r['locator']='line:999'
        target.write_bytes(s.encode(value))
    with pytest.raises((ValueError,KeyError,IndexError)):v.verify(out)


def test_awarded_leg_placeholder_keeps_unknown_played_score_and_aggregate():
    raw=b'<h2><a name="uefa">Europa League</a></h2>\nFirst Round (Aug 20 and 27)\nAlpha                    Eng* Beta                     Sco   awd  3-0  3-3a 9-8p\na awarded after abandonment\n<h2>Other</h2>'
    rows,errors,_=s.parse_rsssf_summary(raw,rec(season='2009/2010'))
    assert not errors and len(rows)==2
    assert rows[0]['periods']['published_final'] is None and rows[0]['status']=='awarded_unscored'
    assert rows[0]['periods']['aggregate']==[3,3] and rows[0]['periods']['regulation_time'] is None
    assert rows[1]['periods']['published_final']==[0,3] and rows[1]['periods']['shootout']==[8,9]


def test_many_representations_on_one_date_are_not_multiple_identity_fixtures():
    rows=[obs('a','Alpha','Beta',publisher='one'),obs('b','Gamma','Beta',publisher='two'),obs('c','Gamma','Beta',publisher='three')]
    mapping,labels,proofs=p.identities(rows)
    assert not proofs and mapping[('2004/2005','one','Alpha')]!=mapping[('2004/2005','two','Gamma')]


def test_single_date_core_name_opponent_evidence_is_conditional_not_confirmed():
    rows=[obs('a','Alpha Club','Beta',publisher='one'),obs('b','Alpha Club Town','Beta',publisher='two')]
    _,_,proofs=p.identities(rows)
    assert len(proofs)==1 and proofs[0]['method']=='SINGLE_FIXTURE_DATE_OPPONENT_AND_CORE_NAME'
    assert proofs[0]['status']=='STRONGLY_SUPPORTED_CONDITIONAL_IDENTITY'


def test_detailed_standings_rows_do_not_become_fixtures_or_manual_cases():
    raw=b'<h3><a name="uefadet">UEFA Cup Details</a></h3>\nGROUP A\nAlpha Club 4 2 1 1 5 - 4 7\nBeta Club 4 1 2 1 5 - 5 5\n<h3>Other</h3>'
    rows,errors,ledger=s.parse_rsssf_detail(raw,rec(),['Alpha Club','Beta Club'])
    assert rows==[] and errors==[]
    assert sum(c.get('classification')=='STANDINGS_NOT_FIXTURE' for c in ledger['sections'])==2


def test_distinct_same_publisher_files_can_establish_structural_name_match():
    rows=[obs('a','Alpha Club','Beta',publisher='same'),obs('b','Alpha Club Town','Beta',publisher='same')]
    rows[1]['source']='same_publisher_goal_log.csv'
    mapping,_,proofs=p.identities(rows)
    assert len(proofs)==1
    events,_,_=p.reconcile(rows,mapping)
    assert len(events)==1 and events[0]['publishers']==['same']


def test_original_score_note_is_structured_and_queued_without_new_fixture():
    raw=b'<h2><a name="uefa">Europa League</a></h2>\nFirst Round\n  Alpha 3-1 Beta\n<h2>Other</h2>'
    rows,errors,_=s.parse_rsssf_summary(raw,rec(season='2011/2012'))
    assert rows==[] and errors[0]['code']=='HISTORICAL_SCORE_CONTEXT'
    assert errors[0]['reported_score']==[3,1] and errors[0]['score_period']=='UNKNOWN_NOT_ASSUMED_REGULATION'
    assert p.review_queue([],errors,[],[])[0]['priority']==1


def test_covid_qualifying_playoff_single_leg_not_flagged_as_missing_return():
    r=obs('a',day='2020-10-01',stage='Playoff',season='2020/2021',qualifier=True)
    mapping,_,_=p.identities([r]);events,_,_=p.reconcile([r],mapping)
    assert p.tie_gaps(events,[r])==[]


def test_explicit_txt_leg_is_extracted_without_reordering_participants():
    raw=b'= UEFA Europa League - Quali 2024/25\n\xe2\x96\xaa Round 1 | Leg 2\nThu Jul 18 2024\nAlpha (ABC) v Beta (DEF)  2-0\n'
    rows,errors,_=s.parse_openfootball(raw,rec('2024-25/elq.txt','2024/2025'))
    assert not errors and rows[0]['source_leg']==2 and rows[0]['home']=='Alpha'


@pytest.mark.parametrize('change',['missing_leg','wrong_participant'])
def test_independent_html_reconstruction_rejects_record_loss_and_wrong_names(tmp_path,monkeypatch,change):
    raw=b'<h2><a name="uefa">UEFA Cup</a></h2>\nFirst Round\nAlpha                    Eng  Beta                     Sco   1-0  2-1  3-1\n<h2>Other</h2>'
    path='originals/rsssf/synthetic.html';file=tmp_path/path;file.parent.mkdir(parents=True);file.write_bytes(raw)
    record=rec(path);record['sha256']=s.sha(raw);rows,errors,_=s.parse_rsssf_summary(raw,record)
    assert not errors and len(rows)==2
    if change=='missing_leg':rows.pop()
    else:rows[0]['home']='Wrong Club'
    monkeypatch.setattr(v,'BASE',tmp_path)
    freeze={'inputs':[dict(path=path,sha256=s.sha(raw),bytes=len(raw),kind='fixture')]}
    with pytest.raises(ValueError):v.raw_checks(freeze,rows,errors)


def test_country_substring_inside_club_name_never_splits_participant():
    raw=b'<h2><a name="uefa">UEFA Cup</a></h2>\nFirst Round\nAdvenir United            Lux  Example ZTS Town    Tch   2-1  0-5  2-6\n<h2>Other</h2>'
    rows,errors,_=s.parse_rsssf_summary(raw,rec())
    assert not errors and rows[0]['home']=='Advenir United' and rows[0]['away']=='Example ZTS Town'
    assert rows[1]['home']=='Example ZTS Town'


def test_group_context_is_reset_before_knockout_records():
    raw=b'<h2><a name="uefa">UEFA Cup</a></h2>\nGroup Phase\nGroup A\nOct 21: Alpha                        3  Beta                         0\nQuarter-Finals\nAlpha                    Eng  Beta                     Sco   1-0  2-0  3-0\n<h2>Other</h2>'
    rows,errors,_=s.parse_rsssf_summary(raw,rec())
    assert not errors and rows[0]['source_fields']['group']=='A'
    assert all(r['source_fields']['group'] is None for r in rows[1:])


def test_schoch_extra_time_duration_assigns_after_extra_time_not_regulation():
    import pyarrow as pa
    import pyarrow.parquet as pq
    from datetime import date
    b=io.BytesIO();pq.write_table(pa.Table.from_pylist([dict(home='Alpha',away='Beta',home_ident='Alpha (England)',away_ident='Beta (Scotland)',date=date(2005,2,17),competition='UEFA EL',gh=3,ga=1,full_time='E')]),b)
    rows,errors,_=s.parse_schoch(b.getvalue(),rec('games.parquet'))
    assert not errors and rows[0]['periods']['after_extra_time']==[3,1] and rows[0]['periods']['regulation_time'] is None


def test_opposing_duration_flags_are_unresolved_even_when_scores_agree():
    a=obs('a',publisher='one');b=obs('b',publisher='two')
    a['source_fields']['full_time']='F';b['periods']['after_extra_time']=[1,0]
    rows=[a,b];mapping,_,_=p.identities(rows);events,_,_=p.reconcile(rows,mapping)
    assert len(events)==1 and {'DURATION_CONFLICT','REGULATION_SCORE_UNRESOLVED'}<=set(events[0]['flags'])
    queue=p.review_queue(events,[],[],rows)
    assert queue[0]['priority']==1 and queue[0]['competing_interpretations']['duration_claims']['after_extra_time_claims']
