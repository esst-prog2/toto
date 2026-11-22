"""Synthetic-only independent parser, structural and chronology tests."""
from copy import deepcopy
from datetime import date, timedelta
import json
import pytest
from scripts import validate_ligue2_structure as v


def raw(body='A v B  2-1 (1-0)',day='Fri Aug 1 2014',rnd='Matchday 1',title='French Ligue 2 2014/15'):
    return f'= {title}\n▪ {rnd}\n{day}\n{body}\n'.encode()


def parse(data=None):
    b=raw() if data is None else data
    return v.read_source(b,2014,'synthetic.txt',v.base.sha(b))[0]


def test_bindings_include_original_physical_bytes():
    b=raw();r=parse(b)[0]
    assert r['raw_record']=='A v B  2-1 (1-0)';assert r['source_line']==4
    assert r['physical_line_sha256']==v.base.sha(b.splitlines(keepends=True)[3]);assert r['raw_line_sha256']==v.base.sha(r['raw_record'].encode())
    assert r['audit_id']==v.source_id(v.base.sha(b),4)
    assert r['date_heading_line']==3 and r['date']=='2014-08-01'


@pytest.mark.parametrize('body,ft',[('A v B  2-1','2-1'),('A 2-1 B','2-1'),('A v B',None),('A v B [cancelled]',None),('A v B  0-3 [awarded]','0-3')])
def test_literal_fixture_grammars(body,ft):
    assert parse(raw(body=body))[0]['FT']==ft


@pytest.mark.parametrize('data',[
 raw(title='French Ligue 1 2014/15'),raw(title='French Ligue 2 2013/14'),raw(title='French Ligue 2 2014/1925'),
 raw(day='Thu Aug 1 2014'),raw(day='Fri Aug 1 2016'),raw(day='Fri Feb 30'),raw(rnd='Matchday 39'),
 raw(rnd='Unknown'),raw(body='A v B  ?-1'),raw(body='A v B  2-'),raw(body='24:00 A v B  1-0'),raw(body='12:60 A v B  1-0'),
 raw()+b'garbage\n',raw()+b'(unterminated\n',raw()+raw(),b'= French Ligue 2 2014/15\nA v B  1-0\n'])
def test_invalid_source_fails_explicitly(data):
    with pytest.raises(ValueError):parse(data)


def test_wrong_source_hash():
    with pytest.raises(ValueError):v.read_source(raw(),2014,'synthetic.txt','wrong')


def test_duplicate_round_heading_rejected():
    with pytest.raises(ValueError):parse(raw()+'▪ Matchday 1\nFri Aug 1 2014\nC v D  0-0\n'.encode())


def test_invalid_utf8_not_replaced():
    with pytest.raises(UnicodeDecodeError):parse(raw()+b'\xff')


def test_round_without_date_rejected():
    with pytest.raises(ValueError):parse(raw()+'▪ Matchday 2\nC v D  0-0\n'.encode())


@pytest.mark.parametrize('day,expected,explicit',[('Fri Aug 1 2014','2014-08-01',True),('Fri Aug 1','2014-08-01',False),('Fri Jan 2','2015-01-02',False)])
def test_year_resolution(day,expected,explicit):
    r=parse(raw(day=day))[0];assert r['date']==expected and r['year_explicit']==explicit


def test_cancellations_are_complete_slots_not_missing_results():
    r=parse(raw(body='A v B [cancelled]'))[0];a=v.inspect_record(r)
    assert a['structurally_valid'] and a['source_cancelled'] and not a['score_bearing'] and not a['incomplete']
    assert a['goal_derived_outcome'] is None and a['chronology']['source_scheduled_date']=='2014-08-01'
    assert a['chronology']['effective_result_availability_date'] is None


def test_unexplained_unscored_is_incomplete():
    r=parse(raw(body='A v B'))[0];a=v.inspect_record(r)
    assert a['incomplete'] and not a['source_cancelled'] and 'UNEXPLAINED_INCOMPLETE' in a['flags']


@pytest.mark.parametrize('changes,error',[
 ({'hg':'3'},'FT_GOAL_CONFLICT'),({'hg':None},'PARTIAL_SCORE'),({'hg':'-1'},'INVALID_SCORE'),
 ({'hg':str(2**63)},'INVALID_SCORE'),({'HT':'3-0'},'HT_FT_CONFLICT'),({'HT':'?-0'},'HT_FT_CONFLICT'),
 ({'away':'A'},'IDENTICAL_TEAMS'),({'home':' A'},'INVALID_TEAM_LABEL'),({'home':'A\ufffd'},'INVALID_TEAM_LABEL'),
 ({'annotation':'[cancelled]'},'CANCELLED_WITH_SCORE'),({'stage':'OTHER_STAGE'},'UNAPPROVED_STAGE'),
 ({'date':'2016-01-01'},'INVALID_SEASON_DATE')])
def test_record_conflicts_visible(changes,error):
    r=parse()[0];r.update(changes);a=v.inspect_record(r);assert not a['structurally_valid'] and error in a['errors']


def test_award_without_score_is_invalid():
    r=parse(raw(body='A v B [awarded]'))[0];assert 'AWARD_WITHOUT_SCORE' in v.inspect_record(r)['errors']


def complete_season():
    teams=[f'Club {i:02}' for i in range(20)];rotation=teams[:];rounds=[]
    for rnd in range(19):
        rounds.append([(rotation[i],rotation[-1-i]) for i in range(10)])
        rotation=[rotation[0],rotation[-1]]+rotation[1:-1]
    lines=['= French Ligue 2 2014/15']
    for rnd,pairs in enumerate(rounds+[[ (a,h) for h,a in pairs] for pairs in rounds],1):
        day=date(2014,8,1)+timedelta(days=(rnd-1)*7)
        lines+=['▪ Matchday '+str(rnd),day.strftime('%a %b ')+str(day.day)+' '+str(day.year)]
        lines += [f'{h} v {a}  1-0 (0-0)' for h,a in pairs]
    b=('\n'.join(lines)+'\n').encode();return v.read_source(b,2014,'synthetic.txt',v.base.sha(b))[0]


def test_full_directed_schedule_rounds():
    rows=complete_season();s=v.validate_season(rows,2014)
    assert s['observed']==s['expected']==s['score_bearing']==380 and s['clubs']==20
    assert s['format_issues']==[] and not s['missing_pairings'] and not s['duplicate_pairings'] and s['flagged']==0


def test_missing_pair_not_filled():
    rows=complete_season();missing=rows.pop();s=v.validate_season(rows,2014)
    assert s['observed']==379 and [missing['home'],missing['away']] in s['missing_pairings']
    assert 'SEASON_FIXTURE_COUNT' in s['format_issues'] and 'ROUND_STRUCTURE' in s['format_issues']


def test_conflicting_pair_does_not_choose_score():
    rows=complete_season();r=deepcopy(rows[0]);r.update(hg='0',ag='0',FT='0-0',HT='0-0',audit_id='duplicate');rows.append(r)
    s=v.validate_season(rows,2014);assert s['duplicate_pairings'][0]['conflicting']
    assert rows[0]['FT']=='1-0' and rows[-1]['FT']=='0-0';assert len(v.queue(rows))>=2


def test_source_order_is_not_chronology():
    rows=complete_season();rows[0]['date']='2014-10-01';s=v.validate_season(rows,2014)
    assert s['wide_rounds'] and s['diagnostic_outliers'] and s['source_order_date_reversals']
    assert rows[0]['date']=='2014-10-01' and rows[0]['assessment']['structurally_valid']
    assert rows[0]['assessment']['chronology']['actual_completion_date'] is None


def test_normalized_collisions_flagged_not_merged():
    rows=parse(raw(body='Équipe v A  1-0\nE\u0301quipe v B  1-0'));s=v.validate_season(rows,2014)
    assert s['normalized_name_collisions'];assert rows[0]['home']!=rows[1]['home'];assert all('NORMALIZED_LABEL_COLLISION' in r['assessment']['flags'] for r in rows)


def test_ajaccio_identities_preserved():
    rows=parse(raw(body='AC Ajaccio v Gazélec FC Ajaccio  1-0'));s=v.validate_season(rows,2014)
    assert s['clubs']==2 and s['team_labels']==['AC Ajaccio','Gazélec FC Ajaccio']


def test_award_chronology_not_backdated():
    r=parse(raw(body='Chamois Niortais v Valenciennes FC  0-3 [awarded]'))[0];r.update(season='2020/2021',date='2020-12-22')
    a=v.inspect_record(r);assert a['source_awarded'] and a['goal_derived_outcome']=='A'
    assert a['chronology']['secondary_reported_decision_date']=='2021-01-06'
    assert a['chronology']['administrative_decision_date'] is None and a['chronology']['effective_result_availability_date'] is None
    assert r['date']=='2020-12-22' and r['FT']=='0-3'


def test_bordeaux_source_and_decision_dates_separate():
    r=parse(raw(body='Girondins Bordeaux v Rodez AF  0-1'))[0];r.update(season='2022/2023',date='2023-06-02')
    a=v.inspect_record(r);assert a['chronology']['administrative_decision_date']=='2023-06-12';assert a['chronology']['effective_result_availability_date'] is None
    assert r['FT']=='0-1' and r['annotation']==''


def test_unusual_score_not_error():
    r=parse(raw(body='Valenciennes FC v AS Béziers  5-6'))[0];a=v.inspect_record(r)
    assert a['structurally_valid'] and a['flags']==['UNUSUAL_SCORE'];assert r['FT']=='5-6'


def test_review_deduplicates_overlapping_flags():
    r=parse()[0];r['assessment']=v.inspect_record(r);r['assessment']['flags']=['WIDE_ROUND','DIAGNOSTIC_DATE_OUTLIER']
    q=v.queue([r]);assert len(q)==1 and len(q[0]['assessment']['flags'])==2
    with pytest.raises(ValueError):v.queue([r,r])


def test_protection_rejects_changes(tmp_path,monkeypatch):
    d=tmp_path/'private';d.mkdir();p=tmp_path/'frozen';p.write_bytes(b'original');log=tmp_path/'PLANNING_LOG.md';log.write_bytes(b'log\n')
    monkeypatch.setattr(v.acquisition,'protect',lambda *a:None)
    (d/v.BASELINE).write_bytes(v.base.encode(dict(files={'frozen':v.base.sha(b'original')},planning_log=dict(bytes=4,sha256=v.base.sha(b'log\n')))))
    assert v.protect(d,tmp_path)['phase2_3_entries']==1;log.write_bytes(b'log\nappend\n');v.protect(d,tmp_path)
    p.write_bytes(b'changed')
    with pytest.raises(ValueError):v.protect(d,tmp_path)


def prior_context(rows):
    return dict(sources=[dict(records=deepcopy(rows),receipt=dict(season='2014/2015'),assessment=dict(wide_rounds=[]))],summary=dict(review_candidates=[]))


@pytest.mark.parametrize('field,value',[('hg','9'),('date','2014-08-02'),('source_line',100),('raw_line_sha256','wrong'),('annotation','[awarded]'),('stage','OTHER_STAGE')])
def test_prior_raw_reconciliation_rejects_changed_fact(field,value):
    rows=parse();prior=prior_context(rows);reports=[v.validate_season(rows,2014)]
    v.reconcile_phase3(rows,reports,prior)
    prior['sources'][0]['records'][0][field]=value
    with pytest.raises(ValueError):v.reconcile_phase3(rows,reports,prior)


def test_prior_queue_cannot_drop_cancelled_observation():
    rows=parse(raw(body='A v B [cancelled]'));prior=prior_context(rows);reports=[v.validate_season(rows,2014)]
    with pytest.raises(ValueError):v.reconcile_phase3(rows,reports,prior)
    prior['summary']['review_candidates']=[dict(audit_id=rows[0]['audit_id'],categories=['SOURCE_CANCELLED'])]
    r=v.reconcile_phase3(rows,reports,prior);assert r['independent_review_members']==1 and r['overlap_combinations']=={}


def test_changed_wide_round_member_rejected():
    rows=parse();prior=prior_context(rows);reports=[v.validate_season(rows,2014)]
    prior['sources'][0]['assessment']['wide_rounds']=[dict(round='1',fixtures=[dict(source_line=4)])]
    with pytest.raises(ValueError):v.reconcile_phase3(rows,reports,prior)
