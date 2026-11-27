"""Synthetic historical-review regressions; no real fixture/evidence rows."""
import copy
import csv
import io
import json
from pathlib import Path

import pytest

from scripts import review_uefa_champions_league_history as production
from scripts import verify_uefa_champions_league_history as independent


def wiki_source(text):
    raw=json.dumps({'query':{'pages':[{'title':'Synthetic qualifying','revisions':[{'revid':7,'slots':{'main':{'content':text}}}]}]}},ensure_ascii=False).encode()
    return raw,dict(path='synthetic/revision.json',season='2020/2021',revision=7,sha256=production.sha(raw),bytes=len(raw))


def box(**changes):
    f=dict(date='{{Start date|2020|8|1|df=y}}',team1='[[Alpha United|Alpha]] {{fbaicon|ABC}}',team2='{{fbaicon|XYZ}} [[Beta FC|Beta]]',score='3–2',aet='yes',goals1='Player {{goal|45+3||90+9||114}}',goals2='Player {{goal|88||102}}',stadium='Synthetic Field')
    f.update(changes)
    return '{{Football box\n'+'\n'.join('|'+k+' = '+v for k,v in f.items())+'\n}}'


def test_complete_chronology_recovers_regulation_including_stoppage_time():
    raw,s=wiki_source('==First qualifying round==\n'+box())
    r,_=production.parse_wikipedia(raw,s);p=r[0]['periods']
    assert p['regulation_time']==[2,1] and p['after_extra_time']==[3,2]
    assert p['goal_minutes_home']==['45+3','90+9','114']
    assert r[0]['raw_fields']['goals1'].endswith('{{goal|45+3||90+9||114}}')


@pytest.mark.parametrize('kwargs',[
    dict(score='0–0',goals1='',goals2=''),
    dict(score='2–1',goals1='Player {{goal|45}}',goals2='Player {{goal|100}}'),
    dict(score='2–1',goals1='Player {{goal|45||unknown}}',goals2='Player {{goal|100}}'),
])
def test_extra_time_never_fills_unknown_regulation_without_complete_chronology(kwargs):
    raw,s=wiki_source('==First qualifying round==\n'+box(**kwargs));r,_=production.parse_wikipedia(raw,s)
    assert r[0]['periods']['regulation_time'] is None
    assert 'REGULATION_PERIOD_REQUIRES_TARGETED_EVIDENCE' in r[0]['periods']['issues']


def test_award_annotation_outside_score_prevents_played_result_inference():
    raw,s=wiki_source('==First qualifying round==\n'+box(score='3–0',aet='',scorenote='Awarded{{refn|A postponed match never kicked off.}}',goals1='',goals2=''))
    r,_=production.parse_wikipedia(raw,s)
    assert r[0]['periods']['reported_score']==[3,0]
    assert r[0]['periods']['regulation_time'] is None
    assert 'AWARD_OR_WALKOVER_SCORE_CONTEXT' in r[0]['periods']['issues']


def test_shootout_fields_are_separate_and_not_counted_as_goals():
    raw,s=wiki_source('==First qualifying round==\n'+box(penaltyscore='12–11',penalties1='Player {{pengoal}}',penalties2='{{penmiss}} Player'))
    r,_=production.parse_wikipedia(raw,s);p=r[0]['periods']
    assert p['regulation_time']==[2,1] and p['shootout']==[12,11]
    assert len(p['shootout_fields'])==3


def test_nested_footnote_does_not_become_part_of_club_identity():
    raw,s=wiki_source('==First qualifying round==\n'+box(team1='[[Alpha United|Alpha]]{{refn|An abandoned [[Other club]] fixture {{cite web|url=https://example.invalid|title=3–0}}}}'))
    r,_=production.parse_wikipedia(raw,s)
    assert r[0]['home']=='Alpha'
    assert 'Other club' in r[0]['raw_fields']['team1']
    assert independent.tidy(r[0]['raw_fields']['team1'])=='Alpha'


def test_revision_json_physical_line_is_distinct_from_decoded_lines():
    raw,s=wiki_source('==First qualifying round==\n\n'+box());r,_=production.parse_wikipedia(raw,s);x=r[0]
    assert x['physical_json_line']==1 and x['decoded_line']==3
    assert x['decoded_end_line']>x['decoded_line']
    text=json.loads(raw)['query']['pages'][0]['revisions'][0]['slots']['main']['content']
    assert production.sha(text[x['decoded_wikitext_start']:x['decoded_wikitext_end']].encode())==x['template_sha256']


@pytest.mark.parametrize('field,value',[('sha256','f'*64),('revision',8)])
def test_revision_identity_and_original_bytes_are_bound(field,value):
    raw,s=wiki_source('==First qualifying round==\n'+box());s[field]=value
    with pytest.raises(ValueError):production.parse_wikipedia(raw,s)


def test_broken_nested_template_fails_closed():
    with pytest.raises(ValueError,match='Unbalanced'):production.template_end('{{Football box|team1={{bad}',0)


def test_independent_tie_summary_reverses_return_leg_score_and_clubs():
    summary='{{#invoke:Sports series|main|generate_links=y\n|[[Alpha United|Alpha]]|ABC|5–3|[[Beta FC|Beta]]|XYZ|2–1|3–2\n}}'
    text='==First qualifying round==\n'+summary+'\n'+box(score='2–1',aet='')+'\n'+box(date='{{Start date|2020|8|8}}',team1='[[Beta FC|Beta]]',team2='[[Alpha United|Alpha]]',score='2–3',aet='')
    raw,s=wiki_source(text);rows,check=independent.wikipedia_reader(raw,s)
    assert len(rows)==check['summary_expected']==2
    assert rows[1]['home']=='Beta' and rows[1]['periods']['reported_score']==[2,3]


def test_independent_summary_catches_missing_return_fixture():
    text='==First qualifying round==\n{{#invoke:Sports series|main|[[Alpha United|Alpha]]|ABC|5–3|[[Beta FC|Beta]]|XYZ|2–1|3–2}}\n'+box(score='2–1',aet='')
    raw,s=wiki_source(text)
    with pytest.raises(ValueError,match='summary/match-box'):independent.wikipedia_reader(raw,s)


def test_independent_single_leg_summary_is_not_a_two_leg_tie():
    text='==First qualifying round==\n{{#invoke:Sports series|main|legs=0|[[Alpha United|Alpha]]|ABC|3–2|[[Beta FC|Beta]]|XYZ}}\n'+box()
    raw,s=wiki_source(text);rows,check=independent.wikipedia_reader(raw,s)
    assert len(rows)==check['summary_expected']==1
    assert rows[0]['periods']['regulation_time']==[2,1]


def event():
    return dict(primary_observation_id='id',event_id='e',first_listed='Alpha',second_listed='Beta',
                football_date='2020-08-01',regulation_time=[1,0],observed_regulation_time=[1,0],neutral_venue=None,disposition='INCLUDE')


def rule(changes):return dict(observation_id='id',changes=changes,evidence_ids=['fact'])


@pytest.mark.parametrize('neutral',[None,0,1])
@pytest.mark.parametrize('score,outcome',[([1,0],'1'),([0,0],'X'),([0,1],'2')])
def test_neutral_status_never_reorients_result_or_outcome(neutral,score,outcome):
    x=event();before=copy.deepcopy(x)
    result=production.apply_decisions(x,[rule(dict(neutral_venue=neutral,regulation_time=score))],{'fact':{}})
    assert result['outcome']==outcome and (result['first_listed'],result['second_listed'])==('Alpha','Beta')
    assert x==before


def test_no_kickoff_award_has_no_football_date_or_model_outcome():
    r=production.apply_decisions(event(),[rule(dict(disposition='NOT PLAYED',football_date=None,regulation_time=None,observed_regulation_time=None,administrative_result=[0,3]))],{'fact':{}})
    assert r['accepted_result'] is None and r['outcome'] is None
    assert r['administrative_result']==[0,3]


def test_no_kickoff_with_played_date_is_rejected():
    with pytest.raises(ValueError,match='No-kickoff'):production.apply_decisions(event(),[rule({'disposition':'NOT PLAYED','regulation_time':None})],{'fact':{}})


def test_played_abandonment_can_use_explicit_approved_administrative_exception():
    r=production.apply_decisions(event(),[rule(dict(regulation_time=None,observed_regulation_time=None,administrative_result=[0,3]))],{'fact':{}})
    assert r['disposition']=='INCLUDE' and r['accepted_result']==[0,3]
    assert r['regulation_time'] is None and r['result_basis']=='RETROSPECTIVE_PLAYED_ADMINISTRATIVE_EXCEPTION'


def test_unresolved_regulation_is_held_out_without_inventing_a_score():
    x=event();x['regulation_time']=None
    r=production.apply_decisions(x,[],{})
    assert r['disposition']=='HOLD OUT' and r['accepted_result'] is None


@pytest.mark.parametrize('changes',[{'first_listed':'Other'},{'season':'Other'},{'neutral_venue':2}])
def test_unsupported_derived_mutations_fail(changes):
    with pytest.raises(ValueError):production.apply_decisions(event(),[rule(changes)],{'fact':{}})


def test_decision_requires_evidence():
    with pytest.raises(ValueError,match='evidence'):production.apply_decisions(event(),[rule({'regulation_time':[2,0]})],{})


@pytest.mark.parametrize('field', ['source','source_sha256','date','home','away'])
def test_rule_is_bound_to_source_and_directed_fixture(field):
    row=dict(source='synthetic/a',source_sha256='a'*64,date='2020-08-01',home='Alpha',away='Beta')
    r=dict(source=row['source'],source_sha256=row['source_sha256'],expected_date=row['date'],expected_home=row['home'],expected_away=row['away'])
    row[field]='different'
    with pytest.raises(ValueError,match='binding'):production.validate_rule(row,r)


def test_no_public_detailed_output():
    with pytest.raises(ValueError,match='private'):production.run(production.ROOT/'docs/synthetic-private-audit')


def test_curley_trailing_space_does_not_drop_separate_shootout():
    columns='Date Season round leg home visitor FT HT aet pens hgoal vgoal FTagg_home FTagg_visitor aethgoal aetvgoal tothgoal totvgoal totagg_home totagg_visitor tiewinner hcountry vcountry'.split()
    f=dict.fromkeys(columns,'NA');f.update(Date='2000-08-01',Season='2000',round='Q-2',leg='2',home='Alpha',visitor='Beta',FT='1-0 ',HT='0-0',aet='1-0',pens='4-2 ')
    out=io.StringIO(newline='');w=csv.DictWriter(out,fieldnames=columns,lineterminator='\n');w.writeheader();w.writerow(f);raw=out.getvalue().encode()
    r=production.parse_curley(raw,dict(path='synthetic/champs.csv',sha256=production.sha(raw)))[0]
    assert r['periods']['shootout']==[4,2] and r['periods']['regulation_time']==[1,0]
    assert r['raw_fields']['pens']=='4-2 '


def test_independent_name_fingerprint_exposes_score_conflict_without_global_alias():
    left=[dict(date='2020-08-01',home='Alpha FC',away='Beta',periods=dict(regulation_time=[1,0])),dict(date='2020-08-08',home='Beta',away='Alpha FC',periods=dict(regulation_time=[0,2]))]
    right=[dict(date='2020-08-01',home='Other Alpha',away='Beta',periods=dict(regulation_time=[1,0])),dict(date='2020-08-08',home='Beta',away='Other Alpha',periods=dict(regulation_time=[0,3]))]
    assert independent.independent_club_map(left,right)=={'Other Alpha':'Alpha FC','Beta':'Beta'}
