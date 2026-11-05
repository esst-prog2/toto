"""Season scope regressions using local fictional HTML and injected transport."""
import csv
import io
import json
from pathlib import Path
import sys

import pytest

import scripts.collect_dfb as cli
from tests.test_dfb_collection import URL, approval, html, reviewed
from tests.test_dfb_html import row
from toto_estimator.dfb_transport import AuthorizedFetcher, digest


@pytest.mark.parametrize('value', ['1990/91', '1990/1991', '1990-91', '1990-1991'])
def test_season_argument_reuses_canonical_identifiers(value):
    assert cli.season_argument(value) == '1990/1991'


@pytest.mark.parametrize('value', ['1990', '1990/92', '1989/90', '2027/28', 'bad'])
def test_invalid_or_out_of_range_season_is_rejected(value):
    import argparse
    with pytest.raises(argparse.ArgumentTypeError):
        cli.season_argument(value)


def setup_cli(tmp_path, monkeypatch):
    root = tmp_path/'germany'
    root.mkdir()
    monkeypatch.setattr(cli, 'PRIVATE', root)
    content = html().replace('<option>other</option>', '<option value="2015-2016">Other season</option>')
    (root/'seed.html').write_text(content)
    # An unrelated season's unavailable export must not be opened/imported.
    manifest = dict(pages=[
        dict(path='seed.html', url=URL, sha256=digest(content.encode()), retrieved_at='2026-11-05',
             access_basis='synthetic bounded sample, NOT permission', evidence_reference='test'),
        dict(path='../not-present.html', url=URL.replace('1990-1991','2015-2016'),
             sha256='0'*64, retrieved_at='not checked outside scope',
             access_basis='unrelated', evidence_reference='unrelated')])
    (root/'exports.json').write_text(json.dumps(manifest))
    args=['collect_dfb', '--season', '1990/91', '--seed', str(root/'seed.html'),
          '--exports', str(root/'exports.json'), '--cache', str(root/'cache'), '--output', str(root/'runs')]
    monkeypatch.setattr(sys, 'argv', args)
    return root, content, args


def output(capsys):
    summary=json.loads(capsys.readouterr().out)
    report=json.loads(Path(summary['report']).read_text())
    return summary, report, Path(summary['report']).parent


def test_scoped_export_report_candidates_and_evidence_acceptance(tmp_path, monkeypatch, capsys):
    root, content, args=setup_cli(tmp_path, monkeypatch)
    def no_fetcher(*a, **kw):
        pytest.fail('Offline export mode constructed a network fetcher')
    monkeypatch.setattr(cli, 'AuthorizedFetcher', no_fetcher)
    cli.main()
    summary, report, run=output(capsys)
    assert report['selected_season']=='1990/1991'
    assert len(report['seasons'])==1 and len(report['inventory']['seasons'])==1
    assert report['export_import']['imported_pages']==1
    assert report['export_import']['skipped_out_of_scope']==[URL.replace('1990-1991','2015-2016')]
    season=report['seasons'][0]
    assert (season['expected_teams'],season['expected_matchdays'],season['expected_matches'])==(18,34,306)
    assert len(season['missing_matchdays'])==33
    assert summary['numeric_candidates']==1 and summary['accepted_historical']==0
    assert report['provenance'][0]['access_basis']=='synthetic bounded sample, NOT permission'
    inventory=list(csv.DictReader((run/'matchday_inventory.csv').read_text().splitlines()))
    assert len(inventory)==34 and inventory[0]['cache_status']=='CACHED'
    assert all(r['cache_status']=='MISSING' for r in inventory[1:])
    candidates=list(csv.DictReader(io.StringIO((run/'completed_history_candidates.csv').read_text())))
    assert candidates[0]['home_team']=='Home & Club' and candidates[0]['home_goals']=='2'
    assert (run/'completed_history.csv').read_text()==','.join(cli.COLUMNS)+'\n'
    assert (run/'ongoing_candidates.csv').read_text()==','.join(cli.COLUMNS)+'\n'
    assert not (root/'cache/attempts').exists()
    # Repeated import reuses the same response and reproduces the complete run.
    cli.main()
    again, _, _=output(capsys)
    assert again==summary
    for name, sha in json.loads((run/'checksums.json').read_text()).items():
        assert digest((run/name).read_bytes())==sha
    # Supplying explicit synthetic finality evidence changes acceptance, not scores.
    review=next(iter(reviewed(content).values()))
    review.update(page_sha256=digest(content.encode()),source_id='match_1')
    (root/'reviews.json').write_text(json.dumps(dict(reviews=[review])))
    monkeypatch.setattr(sys, 'argv', args+['--reviews',str(root/'reviews.json')])
    cli.main()
    accepted, verified, final_run=output(capsys)
    assert accepted['accepted_historical']==1 and accepted['numeric_candidates']==1
    assert verified['seasons'][0]['status']=='INCOMPLETE'
    assert (final_run/'completed_history.csv').read_bytes()==(run/'completed_history_candidates.csv').read_bytes()


def configure_simulated_network(root, monkeypatch, args, responder):
    now=[1800000000.]
    grant=approval(root,now[0])
    grant['approved_urls']=[URL.rsplit('/',1)[0]+f'/{d}' for d in range(1,35)]
    (root/'authorization.json').write_text(json.dumps(grant))
    waits=[]
    def sleep(delay):
        waits.append(delay)
        now[0]+=delay
    def factory(cache, configured):
        return AuthorizedFetcher(cache,configured,request=responder,sleep=sleep,clock=lambda:now[0])
    monkeypatch.setattr(cli,'AuthorizedFetcher',factory)
    monkeypatch.setattr(sys,'argv',args+['--network','--authorization',str(root/'authorization.json')])
    return waits


def test_authorized_scope_pacing_and_resume_never_requests_other_seasons(tmp_path,monkeypatch,capsys):
    root,_,args=setup_cli(tmp_path,monkeypatch)
    calls=[]
    def request(url):
        calls.append(url)
        day=int(url.rsplit('/',1)[1])
        content=html(row(day,matchday=day),day=day)
        return 200,{},content.encode()
    waits=configure_simulated_network(root,monkeypatch,args,request)
    cli.main()
    first, report, _=output(capsys)
    assert calls==[URL.rsplit('/',1)[0]+f'/{d}' for d in range(2,35)]
    assert len(waits)==32 and all(delay>=5 for delay in waits)
    assert report['network_stop'] is None and first['acquired_matchdays']==34
    # A complete synthetic response inventory does not certify fixture completeness.
    assert report['seasons'][0]['status']=='INCOMPLETE' and first['accepted_historical']==0
    cli.main()
    resumed,_,_=output(capsys)
    assert len(calls)==33 and resumed==first


@pytest.mark.parametrize('status',[403,429])
def test_scoped_collection_stops_on_first_access_denial(tmp_path,monkeypatch,capsys,status):
    root,_,args=setup_cli(tmp_path,monkeypatch)
    calls=[]
    def request(url):
        calls.append(url)
        return status,{},b'synthetic restriction'
    configure_simulated_network(root,monkeypatch,args,request)
    with pytest.raises(SystemExit,match='NETWORK STOPPED'):
        cli.main()
    summary,report,_=output(capsys)
    assert calls==[URL[:-1]+'2'] and summary['acquired_matchdays']==1
    assert len(report['seasons'][0]['missing_matchdays'])==33
    assert (root/'cache/STOP.json').exists()


def test_explicit_ongoing_network_scope_requires_existing_opt_in(tmp_path,monkeypatch):
    root,_,args=setup_cli(tmp_path,monkeypatch)
    args[2]='2026/27'
    monkeypatch.setattr(sys,'argv',args+['--network'])
    with pytest.raises(SystemExit) as error:
        cli.main()
    assert error.value.code==2
    assert not (root/'cache').exists()


def test_full_local_export_keeps_candidates_separate_until_finality_review(tmp_path,monkeypatch,capsys):
    from tests.test_dfb_collection import round_robin_pages
    root=tmp_path/'germany';root.mkdir();monkeypatch.setattr(cli,'PRIVATE',root)
    _,pages,reviews=round_robin_pages(1990)
    entries=[]
    for day,(entry,content) in enumerate(pages,1):
        path=root/f'md{day:02d}.html';path.write_bytes(content)
        entries.append(dict(path=path.name,url=entry['url'],sha256=entry['sha256'],
                            retrieved_at='2026-11-05',access_basis='synthetic export, unit test only',evidence_reference='test'))
    (root/'exports.json').write_text(json.dumps(dict(pages=entries)))
    bound_reviews=[dict(page_sha256=sha,source_id=source_id,**evidence) for (sha,source_id),evidence in reviews.items()]
    (root/'reviews.json').write_text(json.dumps(dict(reviews=bound_reviews)))
    args=['collect_dfb','--season','1990/91','--seed',str(root/'md01.html'),
          '--exports',str(root/'exports.json'),'--cache',str(root/'cache'),'--output',str(root/'runs')]
    monkeypatch.setattr(sys,'argv',args)
    monkeypatch.setattr(cli,'AuthorizedFetcher',lambda *a,**kw:pytest.fail('Offline full export attempted network'))
    cli.main()
    summary,report,run=output(capsys)
    assert summary['acquired_matchdays']==34 and summary['numeric_candidates']==306
    assert summary['accepted_historical']==0 and len(report['seasons'][0]['uncertain_matches'])==306
    assert not report['seasons'][0]['missing_matchdays']
    assert len(list(csv.DictReader((run/'completed_history_candidates.csv').read_text().splitlines())))==306
    monkeypatch.setattr(sys,'argv',args+['--reviews',str(root/'reviews.json')])
    cli.main()
    summary,report,run=output(capsys)
    assert summary['completed_seasons']==1 and summary['accepted_historical']==306
    assert report['seasons'][0]['status']=='COMPLETE' and report['seasons'][0]['observed_teams']==18
    assert not report['seasons'][0]['issues'] and not report['seasons'][0]['missing_fixtures']
    assert len(list(csv.DictReader((run/'completed_history.csv').read_text().splitlines())))==306
