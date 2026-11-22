"""Synthetic Phase 3 acquisition/inventory checks; no historical data/network."""
from datetime import date
import json
from pathlib import Path
from unittest.mock import patch

import pytest

from scripts import collect_segunda_feasibility as b
from scripts import collect_segunda_history as c
from scripts import inventory_segunda_history as inv
from scripts import validate_segunda_feasibility as f
from test_segunda_feasibility import setup_cache, git_entry


def body(year):
    day = f.DAYS[date(year, 8, 20).weekday()]
    fixture = 'Alpha v Béta  1-0'
    if year == 2018:
        fixture = 'CF Reus Deportiu v Alpha  0-1 [awarded]'
    if year == 2019:
        fixture = 'Rayo Vallecano v Albacete  1-0\nDeportivo La Coruña v CF Fuenlabrada  2-1'
    if year in (2024, 2025):
        fixture = 'Alpha v Béta'
    return (f'= Segunda División de España {year}/{str(year+1)[-2:]}\n# Teams 22\n# Matches 462\n'
            f'▪ Matchday 1\n{day} Aug 20 {year}\n{fixture}\n').encode()


class Response:
    status = 200
    headers = {}
    def __init__(self, url, raw): self.url, self.raw = url, raw
    def __enter__(self): return self
    def __exit__(self, *args): pass
    def read(self, limit): return self.raw[:limit]


def fixture_cache(tmp_path):
    root, directory = setup_cache(tmp_path)
    all_items = list(b.PLAN)+c.plan()
    rsssf = (b'Spain 1996/97\nSpain Segunda Division A 1996/97\nRound 1 [Sep 1]\nAlpha 1-0 Beta\n'
             b'Spain Segunda Division B (Third Level) 1996/97\n'
             b'Juan Pedro Adrados You are free to copy All rights reserved')
    bodies = {p['url']: rsssf if p['source'] == 'RSSSF' else body(int(p['season'][:4])) for p in all_items}
    entries = {p['original_path']: dict(path=p['original_path'], **git_entry(bodies[p['url']]))
               for p in all_items if p['source'] == 'OpenFootball'}
    (directory/'metadata/git_tree.json').write_bytes(b.encode(dict(sha=b.PIN, truncated=False, tree=list(entries.values()))))
    registry = json.loads((directory/'metadata_receipts.json').read_text())
    for r in registry:
        raw = (directory/r['path']).read_bytes(); r.update(sha256=b.sha(raw), bytes=len(raw))
    (directory/'metadata_receipts.json').write_bytes(b.encode(registry))
    with patch.object(b, 'urlopen', side_effect=lambda request, timeout: Response(request.full_url, bodies[request.full_url])), patch.object(b.time, 'sleep'):
        b.collect(directory, root)
    b.save(directory/f.OUTPUT, b.encode(f.build(directory, root)))
    log = (root/'PLANNING_LOG.md').read_bytes()
    frozen = {str(p.relative_to(root)): b.sha(p.read_bytes()) for p in directory.rglob('*') if p.is_file()}
    b.save(directory/c.BASELINE, b.encode(dict(files=frozen, planning_log=dict(bytes=len(log), sha256=b.sha(log)))))
    return root, directory, bodies


def acquire(root, directory, bodies):
    with patch.object(c, 'fetch', side_effect=lambda request, timeout: Response(request.full_url, bodies[request.full_url])), patch.object(c.time, 'sleep'):
        return c.collect(directory, root)


def test_exact_ten_approved_paths_and_thirteen_season_union():
    items = c.plan()
    assert [int(p['season'][:4]) for p in items] == [2013, 2014, 2015, 2016, 2017, 2020, 2021, 2022, 2023, 2024]
    assert len(items) == len({p['url'] for p in items}) == 10
    assert all(p['commit'] == b.PIN and p['original_path'].endswith('/2-liga2.txt') for p in items)
    assert set(c.YEARS) | set(c.REUSED) == set(range(2012, 2025))
    assert not any('football-data' in p['url'] or '2025-26' in p['url'] or '2026-27' in p['url'] for p in items)


def test_real_receipts_complete_cache_is_idempotent_with_network_forbidden(tmp_path):
    root, directory, bodies = fixture_cache(tmp_path)
    with patch.object(c, 'fetch', side_effect=lambda request, timeout: Response(request.full_url, bodies[request.full_url])) as fetch, patch.object(c.time, 'sleep') as sleep:
        result = c.collect(directory, root)
        assert fetch.call_count == 10 and sleep.call_count == 9
        assert len(result['acquired']) == 10 and len(result['reused_phase2']) == 3
    before = {str(p.relative_to(directory)): p.read_bytes() for p in directory.rglob('*') if p.is_file()}
    with patch.object(c, 'fetch', side_effect=AssertionError('No network allowed')):
        assert c.collect(directory, root) == result
    assert before == {str(p.relative_to(directory)): p.read_bytes() for p in directory.rglob('*') if p.is_file()}


@pytest.mark.parametrize('problem', ['403', 'retry-after', 'redirect', 'blob'])
def test_responsible_access_stop_no_retry_or_partial_source_write(tmp_path, problem):
    root, directory, bodies = fixture_cache(tmp_path)
    def response(request, timeout):
        if problem == '403': raise OSError('403 access denied')
        r = Response(request.full_url, bodies[request.full_url])
        if problem == 'retry-after': r.headers = {'Retry-After': '60'}
        if problem == 'redirect': r.url = 'https://other.example/unapproved'
        if problem == 'blob': r.raw += b'changed'
        return r
    with patch.object(c, 'fetch', side_effect=response) as fetch:
        with pytest.raises((ValueError, OSError)): c.collect(directory, root)
        assert fetch.call_count == 1
    assert (directory/c.STOP).is_file() and not (directory/c.plan()[0]['path']).exists()
    with patch.object(c, 'fetch', side_effect=AssertionError('No retry')):
        with pytest.raises(RuntimeError): c.collect(directory, root)


def test_redirect_rejected_before_followup_request():
    with pytest.raises(ValueError):
        c.NoRedirect().redirect_request(None, None, 302, '', {}, 'https://other.example/data')


@pytest.mark.parametrize('which', ['private', 'public', 'phase2', 'log'])
def test_frozen_sources_public_files_and_log_prefix_are_protected(tmp_path, which):
    root, directory, _ = fixture_cache(tmp_path)
    target = {'private': root/'data/private/prior.txt', 'public': root/'keep',
              'phase2': directory/f.OUTPUT, 'log': root/'PLANNING_LOG.md'}[which]
    target.write_bytes(b'changed')
    with pytest.raises(ValueError): c.protect(directory, root)


@pytest.mark.parametrize('part', ['source', 'receipt'])
def test_incomplete_new_cache_pair_fails_without_fetch(tmp_path, part):
    root, directory, _ = fixture_cache(tmp_path)
    path = directory/c.plan()[0]['path']
    target = path if part == 'source' else path.with_name(path.name+'.provenance.json')
    b.save(target, b'incomplete')
    with patch.object(c, 'fetch', side_effect=AssertionError('No silent repair')):
        with pytest.raises(ValueError): c.collect(directory, root)


def test_inventory_measures_missing_scores_without_forcing_expected_total(tmp_path):
    root, directory, bodies = fixture_cache(tmp_path); acquire(root, directory, bodies)
    first = inv.build(directory, root); second = inv.build(directory, root)
    assert b.encode(first) == b.encode(second)
    assert first['scope_counts']['parsed'] == 13
    assert first['expected_regular'] == 6006 and first['totals']['observed'] == 14
    assert first['totals']['unscored'] == 1 and first['totals']['scored'] == 13
    assert len(first['administrative_awards']) == 1
    assert first['gaps']['older']['seasons'] == 22
    assert first['gaps']['newer']['unscored'] == 1
    assert first['preserved_phase2_exception_context'] == json.loads((directory/f.OUTPUT).read_text())['exceptions']
    latest = first['seasons'][-1]
    assert latest['status'] == 'INVENTORIED_REVIEW' and latest['header_contradictions']
    assert latest['unscored_records'][0]['FT'] is None


def test_changed_source_receipt_and_scope_fail(tmp_path):
    root, directory, bodies = fixture_cache(tmp_path); acquire(root, directory, bodies)
    path = directory/c.plan()[0]['path']; path.write_bytes(path.read_bytes()+b'changed')
    with pytest.raises(ValueError): inv.build(directory, root)


def test_changed_aggregate_registry_fails(tmp_path):
    root, directory, bodies = fixture_cache(tmp_path); acquire(root, directory, bodies)
    path = directory/c.MANIFEST; manifest = json.loads(path.read_text()); manifest['acquired'].pop()
    path.write_bytes(b.encode(manifest))
    with pytest.raises(ValueError): inv.build(directory, root)


def test_label_catalog_preserves_reserve_first_team_and_diagnostic_variants():
    report = inv.label_catalog([dict(season='2020/2021', club_names=['Alpha', 'Alpha B', 'FC Barcelona B', 'Sevilla Atlético', 'Cádiz CF', 'Cadiz CF'])])
    assert report['distinct_exact_labels'] == 6
    assert set(report['accent_case_punctuation_candidates']['cadiz cf']) == {'Cádiz CF', 'Cadiz CF'}
    assert 'Alpha B' in report['reserve_label_candidates'] and 'Alpha' not in report['reserve_label_candidates']
    assert 'FC Barcelona B' in report['reserve_label_candidates']
    assert set(report['exact_labels']) == {'Alpha', 'Alpha B', 'FC Barcelona B', 'Sevilla Atlético', 'Cádiz CF', 'Cadiz CF'}


def test_all_phase2_flags_carried_even_outside_modern_scope_and_loss_fails():
    flag = dict(round=1, earliest='2020-01-01', latest='2020-02-01', records=[])
    phase2 = dict(seasons=[dict(season='2019/2020', source_file='old', wide_rounds=[flag]),
                          dict(season='2025/2026', source_file='new', wide_rounds=[flag])])
    modern = [dict(season='2019/2020', wide_rounds=[flag])]
    carried = inv.check_carried_flags(phase2, modern)
    assert len(carried) == 2 and [r['within_modern_scope'] for r in carried] == [True, False]
    with pytest.raises(ValueError): inv.check_carried_flags(phase2, [dict(season='2019/2020', wide_rounds=[])])
