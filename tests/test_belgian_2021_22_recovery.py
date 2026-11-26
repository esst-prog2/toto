"""Synthetic bounded-recovery tests; no private source or network dependency."""
from pathlib import Path
from copy import deepcopy
import json
import pytest
from scripts import recover_belgian_2021_22 as r


def page(body,stage='reg',title='First Division A'):
    return f'<title>Belgium 2021/22</title>\n<h4><a name="pro">{title}</a></h4>\n<b><a name="{stage}">Section</a></b>\n{body}\n'.encode()


def parse(body,stage='reg'):
    raw=page(body,stage);return r.parse_document(raw,dict(sha256=r.sha(raw),encoding='utf-8-sig'))[0]


def test_only_exact_authorized_original_url():
    assert r.URL=='https://www.rsssf.org/tablesb/belg2022.html'
    with pytest.raises(ValueError):r.request('https://www.rsssf.org/tablesb/belg2023.html')


@pytest.mark.parametrize('stage,label',[('reg','REGULAR'),('po1','CHAMPIONSHIP'),('po2','EUROPE'),('prorel','PROMOTION_RELEGATION')])
def test_stage_sections(stage,label):
    heading='First Leg [Apr 23]' if stage=='prorel' else 'Round 1 [Jul 24]'
    rs=parse(heading+'\nA    2-1 B',stage);assert len(rs)==1 and rs[0]['stage']==label


def test_cup_and_second_division_not_imported():
    raw=page('Round 1 [Jul 24]\nA    2-1 B')+b'<h4><a name="cup">Cup</a></h4>\nRound 1 [Aug 1]\nC    5-1 D\n<h4><a name="tweede">First Division B</a></h4>\nE    4-0 F\n'
    rs,_=r.parse_document(raw,dict(sha256=r.sha(raw),encoding='utf-8-sig'))
    assert len(rs)==1 and rs[0]['home']=='A'


def test_standings_never_become_matches():
    rs=parse('Final Table:\n1.Club A 34 10 10 14 30-40 30\nRound 1 [Jul 24]\nA    2-1 B')
    assert len(rs)==1


def test_date_context_crosses_calendar_year():
    rs=parse('Round 1 [Jul 24]\nA    2-1 B\nRound 22 [Jan 15]\nC    1-0 D')
    assert [x['date'] for x in rs]==['2021-07-24','2022-01-15']


def test_exact_source_line_hash_and_literal_html_labels():
    raw=page('Round 1 [Jul 24]\nKortr&#307;k    2-1 B');rs,_=r.parse_document(raw,dict(sha256=r.sha(raw),encoding='utf-8-sig'));x=rs[0]
    assert x['home']=='Kortrĳk' and x['home_html']=='Kortr&#307;k'
    assert x['source_line_sha256']==r.sha(raw.splitlines(keepends=True)[x['source_line']-1])


@pytest.mark.parametrize('first,second,note',[('Jul 24','Jul 27',"[remaining 35']"),('Jan 15','Jan 18','[second half]')])
def test_explicit_interruption_continuation_one_conditional_event(first,second,note):
    rs=parse(f'Round 1 [{first}]\nA    abd B    [abandoned at 0-1]\n[{second}]\nA    0-1 B    {note}')
    events=r.group_events(rs)
    assert len(rs)==2 and len(events)==1 and events[0]['explicit_continuation_group']
    assert len(events[0]['source_ids'])==2 and not events[0]['ambiguous']
    assert events[0]['comparison_date']==rs[1]['date'] and 'disposition' not in events[0]


def test_duplicate_numeric_description_remains_ambiguous():
    rs=parse('Round 1 [Jul 24]\nA    1-0 B\nA    1-0 B');e=r.group_events(rs)[0]
    assert e['ambiguous'] and e['comparison_score'] is None


def test_abandonment_without_completion_not_promoted_to_result():
    e=r.group_events(parse('Round 1 [Jul 24]\nA    abd B    [abandoned at 0-1]'))[0]
    assert e['ambiguous'] and e['comparison_score'] is None


def test_repeated_opponents_different_stage_are_separate():
    raw=page('Round 1 [Jul 24]\nA    1-0 B')+b'<u><a name="po1">Playoff 1</a></u>\nRound 1 [Apr 24]\nA    0-1 B\n'
    rs,_=r.parse_document(raw,dict(sha256=r.sha(raw),encoding='utf-8-sig'))
    assert len(r.group_events(rs))==2


def test_awarded_score_is_separate_from_original_marker():
    x=parse('Round 1 [Jan 15]\nA    awd B    [awarded 5-0, B dns]')[0]
    assert x['score_token']=='awd' and x['numeric_score'] is None and x['reported_award_score']=='5-0'
    assert x['representation_kind']=='REPORTED_ADMINISTRATIVE_AWARD'


def test_split_award_note_belongs_to_previous_match_only():
    rs=parse("Round 1 [Dec 5]\nA    awd B    [awarded 0-3; abandoned at 0-3\nC    1-1 D       due to crowd trouble]")
    assert 'due to crowd trouble]' in rs[0]['annotation']
    assert rs[1]['away']=='D' and rs[1]['annotation']=='' and rs[1]['trailing_note_belongs_to_source_id']==rs[0]['source_id']


def test_promotion_relegation_legs_remain_outside_regular_stage():
    rs=parse('First Leg [Apr 23]\nRWDM    0-1 Seraing\nSecond Leg [Apr 30]\nSeraing    0-0 RWDM','prorel')
    es=r.group_events(rs);assert len(es)==2 and {x['stage'] for x in rs}=={'PROMOTION_RELEGATION'}
    assert [x['leg'] for x in rs]==[1,2]


@pytest.mark.parametrize('body',['A    1-0 B','Round 1 [Foo 24]\nA    1-0 B','Round 1 [Jul 24]\nA    2-? B','Round 1 [Jul 24]\nA    awd B    [awarded 5-0'])
def test_missing_invalid_or_ambiguous_source_context_fails(body):
    with pytest.raises(ValueError):parse(body)


def test_hash_tamper_rejected():
    raw=page('Round 1 [Jul 24]\nA    1-0 B')
    with pytest.raises(ValueError):r.parse_document(raw+b' ',dict(sha256=r.sha(raw),encoding='utf-8-sig'))


def test_correspondence_exposes_date_and_score_conflicts():
    es=r.group_events(parse('Round 1 [Jul 24]\nA    1-0 B'))
    hist=[dict(home='A',away='B',source_id='historic',date='2021-07-25',score='0-0')]
    c=r.compare(es,hist)
    assert c['matched']==1 and c['date_conflicts']==1 and c['score_conflicts']==1


def test_diagnostic_names_are_season_source_bound_not_normalized():
    es=r.group_events(parse('Round 1 [Jul 24]\nLeuven    1-0 Union'))
    h=[dict(home='Oud-Heverlee Leuven',away='Royal Union Saint-Gilloise',source_id='h',date='2021-07-24',score='1-0')]
    c=r.compare(es,h);assert c['matched']==1 and es[0]['diagnostic_event_key'][4]=='Leuven'


def test_ambiguous_regular_pair_does_not_match_twice():
    es=r.group_events(parse('Round 1 [Jul 24]\nA    1-0 B'))
    h=[dict(home='A',away='B',source_id='h'+str(n),date='2021-07-24',score='1-0') for n in range(2)]
    c=r.compare(es,h);assert c['matched']==0 and len(c['unmatched_historical'])==2


def test_deterministic_event_registry():
    rs=parse('Round 1 [Jul 24]\nA    1-0 B\nC    0-0 D')
    assert r.encode(r.group_events(rs))==r.encode(r.group_events(deepcopy(rs)))


def test_immutable_original_and_receipt_verification(tmp_path):
    target=tmp_path/r.PATH;target.parent.mkdir(parents=True);target.write_bytes(b'<html>')
    rec=dict(url=r.URL,final_url=r.URL,original_path=r.PATH,bytes=6,sha256=r.sha(b'<html>'),git_commit=None,git_blob=None,encoding='utf-8-sig')
    Path(str(target)+'.provenance.json').write_bytes(r.encode(rec));assert r.verify_original(tmp_path)[0]==b'<html>'
    target.write_bytes(b'changed')
    with pytest.raises(ValueError):r.verify_original(tmp_path)


def test_no_overwrite_of_original_cache(tmp_path):
    p=tmp_path/'original';r.save(p,b'a')
    with pytest.raises(FileExistsError):r.save(p,b'b')
    assert p.read_bytes()==b'a'


def test_complete_cache_replay_performs_zero_requests(tmp_path,monkeypatch):
    target=tmp_path/r.PATH;target.parent.mkdir(parents=True);raw=b'<html>';target.write_bytes(raw)
    rec=dict(url=r.URL,final_url=r.URL,original_path=r.PATH,bytes=len(raw),sha256=r.sha(raw),git_commit=None,git_blob=None,encoding='utf-8-sig')
    Path(str(target)+'.provenance.json').write_bytes(r.encode(rec));monkeypatch.setattr(r,'protect',lambda directory:None)
    def forbidden(url):raise AssertionError('Network request during cache replay')
    monkeypatch.setattr(r,'request',forbidden);assert r.collect(tmp_path)==rec
