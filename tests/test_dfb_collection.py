"""Synthetic offline collection and transport safety tests; never use real network."""
from datetime import datetime, timezone
import json
from pathlib import Path

import pytest

from tests.test_dfb_html import page, row
from toto_estimator.dfb_html import parse_dfb_matchday
from toto_estimator.dfb_collection import (build_report, classify, ingest_exports,
                                         inventory_from_html, load_reviews, season_format, validate_season)
from toto_estimator.dfb_transport import (AccessStopped, AuthorizedFetcher, ResponseCache,
                                        check_authorization, digest, json_bytes)

URL='https://datencenter.dfb.de/de/competitions/bundesliga/seasons/1990-1991/matchday/1'


def html(rows=None,season='1990-1991',day=1,rounds=34):
    content=page(rows,season=season,matchday=day)
    # Fixtures are fictional; team IDs intentionally differ from display spellings.
    content=content.replace('<a>Home &amp; Club</a>','<a href="/competitions/bundesliga/seasons/'+season+'/teams/h">Home &amp; Club</a>')
    content=content.replace('<a>Away</a>','<a href="/competitions/bundesliga/seasons/'+season+'/teams/a">Away</a>')
    options=''.join(f'<option value="{i}">{i}</option>' for i in range(1,rounds+1) if i!=day)
    return content.replace('</select>\n    <turbo-frame',options+'</select>\n    <turbo-frame')


def cached(content,url=URL):
    return dict(url=url,status=200,sha256=digest(content.encode()),retrieved_at='2026-11-05T00:00:00+00:00'),content.encode()


def reviewed(content,status='finished',**extra):
    return {(digest(content.encode()),'match_1'):dict(status=status,evidence_reference='approved export row 1',reviewer='Operator',**extra)}


def one_round_format():
    return dict(season='1990/1991',teams=2,rounds=1,matches=1,ongoing=False,slug='1990-1991',urls=[URL])


def test_inventory_actual_slugs_and_twenty_team_season():
    content=html().replace('<option>other</option>','<option value="1991-1992">x</option><option value="2025-26">y</option>')
    inv=inventory_from_html(content)
    assert len(inv['seasons'])==37
    assert inv['seasons'][1]['matches']==380 and len(inv['seasons'][1]['urls'])==38
    assert inv['seasons'][35]['urls'][0].endswith('/2025-26/matchday/1')
    assert inv['seasons'][2]['urls']==[None]*34
    assert inv['seasons'][-1]['ongoing']


def test_numeric_score_is_uncertain_until_response_bound_review():
    content=html();fmt=season_format(1990);fmt.update(slug='1990-1991',urls=[URL]+[f'{URL}x{i}' for i in range(2,35)])
    result=validate_season(fmt,[cached(content)],{})
    assert result['numeric_results']==1 and result['accepted_results']==0
    assert result['uncertain_matches'][0]['source_id']=='match_1'
    result=validate_season(fmt,[cached(content)],reviewed(content))
    assert result['accepted_results']==1 and result['status']=='INCOMPLETE'
    assert result['records'][0]['home_team']=='Home & Club'
    assert len(result['missing_matchdays'])==33


@pytest.mark.parametrize('text,state',[('LIVE','live'),('abgebrochen','abandoned'),('verlegt','postponed'),('abgesagt','cancelled')])
def test_negative_status_vetoes_finished_review(text,state):
    content=html().replace('extra c-MatchTable-row','extra c-MatchTable-row '+text)
    ob=parse_dfb_matchday(content).observations[0]
    assert classify(ob,None)[0]==state
    assert classify(ob,dict(status='finished'))[:2]==('unknown','status_evidence_conflict')


def test_awarded_annotation_requires_explicit_outcome_evidence():
    content=html().replace('2 : 1','0 : 2 [awarded]')
    parsed=parse_dfb_matchday(content)
    assert parsed.records[0]['away_goals']==2
    assert classify(parsed.observations[0],None)[0]=='unknown'
    assert classify(parsed.observations[0],dict(status='awarded'))[0]=='unknown'
    assert classify(parsed.observations[0],dict(status='awarded',outcome_policy='official administrative result',confirmed_home_goals=0,confirmed_away_goals=2))[0]=='awarded'


def test_missing_fields_remain_identifiable_uncertain_rows():
    content=html(row(score='-:-',date='unannounced'))
    result=validate_season(dict(one_round_format()),[cached(content)],{})
    ob=result['uncertain_matches'][0]
    assert ob['source_id']=='match_1' and ob['raw_score']=='-:-' and ob['home_team']=='Home & Club'
    assert result['accepted_results']==0 and result['issues']


def test_changed_date_same_fixture_and_same_id_conflicts_not_silently_resolved():
    first=html(); second=html(row(date='09.08.1990',matchday=2),day=2)
    url2=URL[:-1]+'2';fmt=one_round_format();fmt.update(urls=[URL,url2],rounds=2)
    reviews={**reviewed(first),**reviewed(second)}
    result=validate_season(fmt,[cached(first),cached(second,url2)],reviews)
    assert result['accepted_results']==0
    assert any(i['code']=='conflicting_records' for i in result['issues'])


def test_missing_pair_and_full_roster_are_reported():
    content=html();result=validate_season(one_round_format(),[cached(content)],{})
    assert result['missing_fixtures']==[dict(home_identity='a',away_identity='h')]
    assert not result['missing_fixture_identities_unknown']
    fmt=season_format(1990);fmt.update(slug='1990-1991',urls=[URL])
    result=validate_season(fmt,[cached(content)],{})
    assert result['missing_fixture_identities_unknown'] and result['unseen_fixture_slots']==305


def test_cache_integrity_and_conflicting_version_preservation(tmp_path):
    cache=ResponseCache(tmp_path);content=html().encode()
    cache.store(URL,content,retrieved_at='now',basis='sample',reference='test')
    with pytest.raises(AccessStopped,match='Different snapshot'):
        cache.store(URL,content+b' ',retrieved_at='later',basis='sample',reference='test')
    assert len(list((tmp_path/'conflicts').glob('*.html')))==1
    (tmp_path/'bodies'/(digest(content)+'.html')).write_bytes(b'corruption')
    with pytest.raises(AccessStopped,match='checksum'):cache.get(URL)


def test_offline_import_provenance_and_escape_rejection(tmp_path):
    content=html().encode();(tmp_path/'sample.html').write_bytes(content)
    manifest=dict(pages=[dict(path='sample.html',url=URL,sha256=digest(content),retrieved_at='now',
                              access_basis='bounded public sample',evidence_reference='existing snapshot')])
    path=tmp_path/'manifest.json';path.write_text(json.dumps(manifest))
    cache=ResponseCache(tmp_path/'cache');ingest_exports(cache,path)
    assert cache.get(URL)[1]==content
    manifest['pages'][0]['path']='../escape.html';path.write_text(json.dumps(manifest))
    with pytest.raises(ValueError,match='boundary'):ingest_exports(cache,path)


def test_no_authorization_never_calls_transport(tmp_path):
    calls=[];fetcher=AuthorizedFetcher(ResponseCache(tmp_path),request=lambda u:calls.append(u))
    with pytest.raises(AccessStopped,match='authorization'):fetcher.fetch(URL)
    assert calls==[]


def approval(tmp_path,clock):
    doc=tmp_path/'approval.txt';doc.write_text('Synthetic test authorization, not real permission')
    return dict(network_collection_authorized=True,approved_urls=[URL],evidence_path=str(doc),
                evidence_sha256=digest(doc.read_bytes()),permission_reference='synthetic test',
                minimum_interval_seconds=5,valid_until=datetime.fromtimestamp(clock+1000,timezone.utc).isoformat(),
                conditions_reviewed_at=datetime.fromtimestamp(clock,timezone.utc).isoformat())


def test_transient_retries_pacing_and_resume_without_downloading(tmp_path):
    now=[1800000000.];sleeps=[];calls=[]
    def sleep(n):sleeps.append(n);now[0]+=n
    def request(url):
        calls.append(url)
        return (503,{},b'temporary') if len(calls)==1 else (200,{},html().encode())
    cache=ResponseCache(tmp_path/'cache');auth=approval(tmp_path,now[0])
    f=AuthorizedFetcher(cache,auth,request=request,sleep=sleep,clock=lambda:now[0])
    assert f.fetch(URL)[1]==html().encode()
    assert len(calls)==2 and sleeps==[5]
    # Resuming cached pages requires neither fresh permission nor a request.
    f=AuthorizedFetcher(cache,request=lambda u:pytest.fail('cache hit made network request'))
    assert f.fetch(URL)[1]==html().encode()


@pytest.mark.parametrize('status,body',[(401,b'login'),(403,b'forbidden'),(429,b'limited'),
                                      (200,b'<div>verify you are human</div>'),(200,b'<div class="g-recaptcha">x</div>')])
def test_access_restrictions_stop_persistently_without_retry(tmp_path,status,body):
    now=1800000000.;calls=[];cache=ResponseCache(tmp_path/'cache')
    def request(url):calls.append(url);return status,{},body
    f=AuthorizedFetcher(cache,approval(tmp_path,now),request=request,sleep=lambda n:None,clock=lambda:now)
    with pytest.raises(AccessStopped,match='restriction'):f.fetch(URL)
    assert len(calls)==1 and (cache.root/'STOP.json').exists()
    with pytest.raises(AccessStopped,match='Persistent'):f.fetch(URL)
    assert len(calls)==1 and cache.get(URL) is None


def test_retry_after_and_redirect_are_not_followed(tmp_path):
    now=1800000000.;cache=ResponseCache(tmp_path/'cache');calls=[]
    def request(u):calls.append(u);return 503,{'Retry-After':'60'},b'unavailable'
    with pytest.raises(AccessStopped,match='Retry-After'):
        AuthorizedFetcher(cache,approval(tmp_path,now),request=request,clock=lambda:now).fetch(URL)
    assert len(calls)==1
    cache=ResponseCache(tmp_path/'redirect')
    with pytest.raises(AccessStopped,match='HTTP 302'):
        AuthorizedFetcher(cache,approval(tmp_path,now),request=lambda u:(302,{'Location':'https://other.example'},b''),clock=lambda:now).fetch(URL)


@pytest.mark.parametrize('change',[dict(network_collection_authorized=False),dict(approved_urls=[]),
                                    dict(evidence_sha256='0'*64),dict(minimum_interval_seconds=0),
                                    dict(minimum_interval_seconds=float('nan')),dict(valid_until='2020-01-01T00:00:00+00:00'),
                                    dict(valid_until='2030-01-01T00:00:00')])
def test_authorization_scope_evidence_expiry_and_interval(tmp_path,change):
    now=1800000000.;auth=approval(tmp_path,now);auth.update(change)
    with pytest.raises(AccessStopped):check_authorization(auth,URL,now)


def test_review_file_rejects_unbound_or_conflicting_evidence(tmp_path):
    path=tmp_path/'reviews.json';entry=dict(source_id='match_1',page_sha256='a'*64,status='finished',reviewer='Operator',evidence_reference='approved export')
    path.write_text(json.dumps(dict(reviews=[entry,entry])))
    with pytest.raises(ValueError,match='Duplicate'):load_reviews(path)
    path.write_text(json.dumps(dict(reviews=[{**entry,'status':'guess'}])))
    with pytest.raises(ValueError,match='valid status'):load_reviews(path)


def round_robin_pages(start):
    """Complete synthetic home/away schedule; test format rules, not real results."""
    fmt=season_format(start);fmt['slug']=f'{start}-{start+1}'
    n=fmt['teams'];clubs=list(range(n));rounds=[]
    for _ in range(n-1):
        rounds.append([(clubs[i],clubs[-i-1]) for i in range(n//2)])
        clubs=[clubs[0],clubs[-1],*clubs[1:-1]]
    rounds += [[(a,h) for h,a in pairs] for pairs in rounds]
    pages=[];reviews={};urls=[];source_id=1
    for day,pairs in enumerate(rounds,1):
        content_rows=''
        for h,a in pairs:
            rr=row(source_id,home=f'Club {h}',away=f'Club {a}',season=fmt['slug'],matchday=day,date=f'08.08.{start}')
            rr=rr.replace(f'<a>Club {h}</a>',f'<a href="/competitions/bundesliga/seasons/{fmt["slug"]}/teams/t{h}">Club {h}</a>')
            rr=rr.replace(f'<a>Club {a}</a>',f'<a href="/competitions/bundesliga/seasons/{fmt["slug"]}/teams/t{a}">Club {a}</a>')
            content_rows+=rr;source_id+=1
        content=html(content_rows,season=fmt['slug'],day=day,rounds=fmt['rounds'])
        url=f'https://datencenter.dfb.de/de/competitions/bundesliga/seasons/{fmt["slug"]}/matchday/{day}'
        urls.append(url);pages.append(cached(content,url))
        for ob in parse_dfb_matchday(content).observations:
            reviews[(digest(content.encode()),ob['source_id'])]=dict(status='finished',reviewer='Synthetic',evidence_reference='test')
    fmt['urls']=urls
    return fmt,pages,reviews


@pytest.mark.parametrize('start,count,teams',[(1990,306,18),(1991,380,20)])
def test_full_season_acceptance_requires_complete_balanced_home_away_schedule(start,count,teams):
    fmt,pages,reviews=round_robin_pages(start)
    result=validate_season(fmt,pages,reviews)
    assert result['status']=='COMPLETE' and result['accepted_results']==count
    assert result['observed_teams']==teams and not result['issues']
    assert all(v==dict(home=teams-1,away=teams-1) for v in result['balance'].values())
    incomplete=validate_season(fmt,pages[:-1],reviews)
    assert incomplete['status']=='INCOMPLETE' and len(incomplete['missing_fixtures'])==teams//2
    assert len(incomplete['missing_matchdays'])==1


def test_ongoing_partition_never_certified_as_completed_history():
    fmt,pages,reviews=round_robin_pages(2026)
    report=build_report(dict(seasons=[fmt]), type('Cache',(),{'get':lambda self,url:next((p for p in pages if p[0]['url']==url),None)})(),reviews)
    assert report['summary']['accepted_historical']==0
    assert report['summary']['accepted_ongoing']==306
    assert report['seasons'][0]['status']=='ONGOING_PARTIAL'


def test_administrative_note_outside_score_is_not_lost():
    content=html().replace('08.08.1990','08.08.1990 (gewertet)')
    ob=parse_dfb_matchday(content).observations[0]
    assert classify(ob,None)[2] is True
    assert classify(ob,dict(status='finished'))[0]=='unknown'


def test_permission_expiring_during_pacing_prevents_next_request(tmp_path):
    now=[1800000000.];calls=[];cache=ResponseCache(tmp_path/'cache')
    auth=approval(tmp_path,now[0]);auth['valid_until']=datetime.fromtimestamp(now[0]+3,timezone.utc).isoformat()
    url2=URL[:-1]+'2';auth['approved_urls'].append(url2)
    def request(url):calls.append(url);return 200,{},html().encode()
    def sleep(n):now[0]+=n
    fetcher=AuthorizedFetcher(cache,auth,request=request,sleep=sleep,clock=lambda:now[0])
    fetcher.fetch(URL)
    with pytest.raises(AccessStopped,match='expired'):fetcher.fetch(url2)
    assert calls==[URL]


def test_invalid_cached_layout_is_reported_not_certified_complete(tmp_path):
    cache=ResponseCache(tmp_path);cache.store(URL,b'unknown layout',retrieved_at='now',basis='test',reference='synthetic')
    report=build_report(dict(seasons=[one_round_format()]),cache)
    assert report['seasons'][0]['invalid_pages']==[URL]
    assert report['summary']['completed_seasons']==0


def test_response_from_wrong_round_is_not_cached(tmp_path):
    now=1800000000.;cache=ResponseCache(tmp_path/'cache')
    fetcher=AuthorizedFetcher(cache,approval(tmp_path,now),request=lambda u:(200,{},html(day=2).encode()),clock=lambda:now)
    with pytest.raises(AccessStopped,match='canonical'):fetcher.fetch(URL)
    assert cache.get(URL) is None and list((cache.root/'attempts').glob('*.html'))


def test_cli_offline_reproduction_and_network_opt_in_still_needs_permission(tmp_path,monkeypatch,capsys):
    import sys
    import scripts.collect_dfb as cli
    root=tmp_path/'germany';root.mkdir();monkeypatch.setattr(cli,'PRIVATE',root)
    content=html().encode();(root/'seed.html').write_bytes(content)
    manifest=dict(pages=[dict(path='seed.html',url=URL,sha256=digest(content),retrieved_at='2026-11-05',
                              access_basis='synthetic',evidence_reference='unit test')])
    (root/'exports.json').write_text(json.dumps(manifest))
    args=['collect_dfb','--seed',str(root/'seed.html'),'--exports',str(root/'exports.json'),
          '--cache',str(root/'cache'),'--output',str(root/'runs')]
    monkeypatch.setattr(sys,'argv',args);cli.main();first=json.loads(capsys.readouterr().out)
    cli.main();second=json.loads(capsys.readouterr().out)
    assert first==second and first['accepted_historical']==0
    run=Path(first['report']).parent
    assert (run/'completed_history.csv').read_text()==','.join(cli.COLUMNS)+'\n'
    assert (run/'ongoing.csv').read_text()==','.join(cli.COLUMNS)+'\n'
    monkeypatch.setattr(sys,'argv',args+['--network'])
    with pytest.raises(SystemExit,match='NETWORK STOPPED'):cli.main()
    stopped=json.loads(capsys.readouterr().out)
    assert json.loads(Path(stopped['report']).read_text())['network_stop']
    assert not list((root/'cache').glob('attempts/*.html'))


def test_cli_rejects_output_outside_private_germany(tmp_path,monkeypatch):
    import scripts.collect_dfb as cli
    monkeypatch.setattr(cli,'PRIVATE',tmp_path/'germany')
    with pytest.raises(ValueError,match='private/germany'):cli.private_path(tmp_path/'england.csv')


def test_team_cannot_play_twice_in_a_nominal_round_without_an_issue():
    rows=row(1,away='Club A')+row(2,away='Club B')
    content=html(rows);fmt=one_round_format();fmt.update(teams=4,matches=12)
    result=validate_season(fmt,[cached(content)],{})
    assert any(i['code']=='round_team_participation' for i in result['issues'])


def test_awarded_score_conflict_is_quarantined_without_changing_source_goals():
    content=html().replace('2 : 1','0 : 2 [awarded]');ob=parse_dfb_matchday(content).observations[0]
    status,issue,_=classify(ob,dict(status='awarded',outcome_policy='official result',confirmed_home_goals=1,confirmed_away_goals=1))
    assert status=='unknown' and issue=='awarded_score_missing_or_conflicting'
    assert ob['record']['home_goals']==0 and ob['record']['away_goals']==2
