"""Synthetic Phase 2 checks: no private fixtures or real network requests."""
from copy import deepcopy
import hashlib
from itertools import permutations
import json
from pathlib import Path
from unittest.mock import patch

import pytest

from scripts import collect_segunda_feasibility as c
from scripts import validate_segunda_feasibility as v


def test_exact_approved_scope_and_pinned_paths():
    assert len(c.PLAN) == 5
    assert [p['original_path'] for p in c.PLAN[:4]] == [f'{y}/2-liga2.txt' for y in ('2012-13', '2018-19', '2019-20', '2025-26')]
    assert all(p['commit'] == '80035a93dd4920985af52aa097a54a6fb888563b' for p in c.PLAN[:4])
    assert c.PLAN[-1]['url'] == 'https://www.rsssf.org/tabless/span97.html'
    assert not any('football-data' in p['url'] or '2026-27' in p['url'] for p in c.PLAN)


def text(body, year=2012):
    return (f'= Segunda División de España {year}/{str(year+1)[-2:]}\n'+body).encode()


def test_source_syntax_crlf_unicode_halftime_and_awards_preserved():
    raw = text('▪ Matchday 1\nSat Aug 18 2012\n19:00  Alphá  v Beta  1-0 (0-0) [awarded]\n').replace(b'\n', b'\r\n')
    rows, _ = v.parse_text(raw, 2012)
    assert len(rows) == 1 and rows[0]['date'] == '2012-08-18'
    assert rows[0]['home'] == 'Alphá' and rows[0]['HT'] == '0-0'
    assert rows[0]['source_marked_awarded'] and rows[0]['annotation'] == '[awarded]'
    assert '19:00' in rows[0]['raw_record']


def test_unscored_fixture_is_not_a_zero_draw():
    rows, _ = v.parse_text(text('▪ 1. Round\nSat Aug 18 2012\nAlpha v Beta\n'), 2012)
    assert rows[0]['hg'] is rows[0]['ag'] is rows[0]['FT'] is None
    result = v.assess(rows, 2012, 2)
    assert result['scored'] == 0 and result['unscored'] == 1 and not result['outcomes']


def test_non_v_score_syntax():
    rows, _ = v.parse_text(text('▪ Regular Season - 1\nSat Aug 18 2012\nAlpha  2-1 (1-0)  Beta\n'), 2012)
    assert rows[0]['FT'] == '2-1'


def test_covid_calendar_july_august_and_completion_not_kickoff():
    rows, _ = v.parse_text(text('▪ Matchday 42\nFri Aug 7 2020\nAlpha v Beta  2-1\n', 2019), 2019)
    assert rows[0]['date'] == '2020-08-07'
    rows, _ = v.parse_text(text('▪ Matchday 42\nFri Aug 7\nAlpha v Beta  2-1\n', 2019), 2019)
    assert rows[0]['date'] == '2020-08-07'
    assert not v.assess(rows, 2019, 2)['date_error_lines']


def test_playoff_stage_and_scorer_lines_remain_separate():
    raw = text('▪ Matchday 1\nSat Aug 18 2012\nAlpha v Beta  1-0\n (A 10\'(p))\n▪ Promotion Playoff Final\nSun Aug 19\nBeta v Alpha  0-0\n')
    rows, notes = v.parse_text(raw, 2012)
    assert len(rows) == 2 and rows[1]['stage'] == 'PLAYOFF_OR_OTHER'
    result = v.assess(rows, 2012, 2)
    assert result['regular'] == 1 and result['other'] == 1
    assert any(n['kind'] == 'scorer_annotation' for n in notes)


@pytest.mark.parametrize('body', [
    '▪ Unknown competition phase\n',
    '▪ Matchday 43\n',
    '▪ Matchday 1\nSun Aug 18 2012\nAlpha v Beta  1-0\n',
    '▪ Matchday 1\nSat Aug 18 2012\nAlpha v Beta  1-?\n',
    '▪ Matchday 1\nSat Aug 18 2012\nAlpha v Beta  1-0\n (unclosed\n',
    '▪ Matchday 1\nSat Aug 18 2012\n25:00 Alpha v Beta  1-0\n',
    'Alpha v Beta  1-0\n',
])
def test_unknown_or_contradictory_text_fails_explicitly(body):
    with pytest.raises(ValueError):
        v.parse_text(text(body), 2012)


@pytest.mark.parametrize('title', ['= Primera División 2012/13', '= Segunda División B 2012/13', '= Segunda División 2013/14'])
def test_wrong_competition_or_season_fails(title):
    with pytest.raises(ValueError):
        v.parse_text((title+'\n▪ Matchday 1\nSat Aug 18 2012\nAlpha v Beta  1-0\n').encode(), 2012)


def rsssf(body):
    return ('<pre>\nSpain Primera Division 1996/97\nBogus  9-9 Fake\nSpain Segunda Division A 1996/97\nTable:\n'+body+
            '\nTop Goalscorers\nA 20\nSpain Segunda Division B (Third Level) 1996/97\nFake  8-8 Fake2\n</pre>').encode('latin-1')


def test_rsssf_round_proxy_is_not_an_explicit_fixture_date_and_stages_are_bounded():
    rows, _ = v.parse_rsssf(rsssf('Round 1 [Sep 1]\nAlpha  1-0 Beta\nBeta  0-0 Alpha [Sep 2]\nTable:\nPromotion Playoff\nFirst leg [Jun 25]\nAlpha  1-0 Gamma\nSecond leg [Jun 29]\nGam  0-0 Alpha'))
    assert len(rows) == 4
    assert rows[0]['date_basis'] == 'ROUND_HEADING_PROXY'
    assert rows[1]['date_basis'] == 'FIXTURE_EXPLICIT' and rows[1]['date'] == '1996-09-02'
    assert [r['stage'] for r in rows[2:]] == ['PROMOTION_PLAYOFF']*2
    assert rows[3]['home'] == 'Gam'  # Never silently map this to Gamma.
    assert all('Fake' not in r['raw_record'] for r in rows)


def test_rsssf_unrecognized_result_row_and_missing_boundaries_fail():
    with pytest.raises(ValueError):
        v.parse_rsssf(rsssf('Round 1 [Sep 1]\nAlpha  won Beta'))
    with pytest.raises(ValueError):
        v.parse_rsssf(b'Round 1 [Sep 1]\nAlpha  1-0 Beta')


def full_rows():
    rows = []
    for i, (h, a) in enumerate(permutations(range(2), 2)):
        rows.append(dict(source_line=i+1, date=f'2012-09-{i+1:02}', home=f'Club {h}', away=f'Club {a}',
                         hg='1', ag='0', FT='1-0', HT=None, annotation='', source_marked_awarded=False,
                         date_basis='SOURCE_DATE_HEADING', stage='REGULAR_SEASON', round=i+1, raw_record='synthetic'))
    return rows


@pytest.mark.parametrize('change,issue', [('duplicate', 'duplicate_pairings'), ('negative', 'invalid_scores'),
    ('float', 'invalid_scores'), ('partial', 'invalid_scores'), ('date', 'dates'), ('team', 'teams'),
    ('halftime', 'invalid_scores'), ('missing', 'missing_pairings'), ('collision', 'same_team_date_collision'),
    ('normalization', 'normalized_name_collision')])
def test_assessment_guards_and_input_immutability(change, issue):
    rows = full_rows()
    if change == 'duplicate': rows[-1] = deepcopy(rows[0])
    if change == 'negative': rows[0]['hg'] = '-1'
    if change == 'float': rows[0]['hg'] = '1.1'
    if change == 'partial': rows[0]['hg'] = None
    if change == 'date': rows[0]['date'] = '2014-01-01'
    if change == 'team': rows[0]['away'] = rows[0]['home']
    if change == 'halftime': rows[0]['HT'] = '2-0'
    if change == 'missing': rows.pop()
    if change == 'collision': rows[1]['date'] = rows[0]['date']
    if change == 'normalization': rows[0]['home'] = 'club 0'
    before = deepcopy(rows); result = v.assess(rows, 2012, 2)
    assert issue in result['issues'] and rows == before


def test_complete_synthetic_regular_season_passes_without_inference():
    result = v.assess(full_rows(), 2012, 2)
    assert result['issues'] == [] and result['regular'] == result['scored'] == 2


def git_entry(raw):
    return dict(size=len(raw), sha=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(), type='blob')


def test_git_tree_blob_identity_and_rsssf_identity_checks():
    raw = b'synthetic'; entries = {p['original_path']: dict(path=p['original_path'], **git_entry(raw)) for p in c.PLAN[:4]}
    tree = dict(sha=c.PIN, truncated=False, tree=list(entries.values()))
    assert c.checked_tree(c.encode(tree)) == entries
    assert c.verify(raw, c.PLAN[0], entries) == git_entry(raw)['sha']
    with pytest.raises(ValueError): c.verify(raw+b'changed', c.PLAN[0], entries)
    tree['truncated'] = True
    with pytest.raises(ValueError): c.checked_tree(c.encode(tree))
    with pytest.raises(ValueError): c.verify(b'<html>Access denied</html>', c.PLAN[-1], entries)


def setup_cache(tmp_path):
    root = tmp_path/'root'; directory = root/'data/private/spain/segunda_division'; directory.mkdir(parents=True)
    (root/'keep').write_bytes(b'protected'); (root/'PLANNING_LOG.md').write_bytes(b'history\n')
    prior = root/'data/private/prior.txt'; prior.write_bytes(b'private')
    baseline = dict(private={'data/private/prior.txt': c.sha(b'private')}, public={'keep': c.sha(b'protected')},
                    planning_log=dict(bytes=8, sha256=c.sha(b'history\n')))
    c.save(directory/'protected_before.json', c.encode(baseline))
    raw = b'synthetic'; entries = [dict(path=p['original_path'], **git_entry(raw)) for p in c.PLAN[:4]]
    c.save(directory/'metadata/git_tree.json', c.encode(dict(sha=c.PIN, truncated=False, tree=entries)))
    c.save(directory/'metadata/LICENSE.md', b'CC0 1.0 Universal\n')
    c.save(directory/'metadata/README.md', b'synthetic notices')
    c.save(directory/'metadata/NOTES.md', b'synthetic notes')
    metadata = [dict(path='metadata/'+n, sha256=c.sha((directory/'metadata'/n).read_bytes()),
                     bytes=len((directory/'metadata'/n).read_bytes()))
                for n in ('README.md', 'LICENSE.md', 'NOTES.md', 'git_tree.json')]
    c.save(directory/'metadata_receipts.json', c.encode(metadata))
    return root, directory


def test_complete_acquisition_is_offline_idempotent_and_receipt_tampering_fails(tmp_path):
    root, directory = setup_cache(tmp_path)
    rsssf_raw = b'Spain 1996/97 Spain Segunda Division A 1996/97 Juan Pedro Adrados You are free to copy All rights reserved'
    class Response:
        status = 200
        headers = {}
        def __init__(self, request): self.url = request.full_url
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def read(self, limit): return rsssf_raw if self.url == c.RSSSF else b'synthetic'
    with patch.object(c, 'urlopen', side_effect=lambda request, timeout: Response(request)) as fetch, patch.object(c.time, 'sleep'):
        first = c.collect(directory, root)
        assert fetch.call_count == 5
    before = {str(p.relative_to(directory)): p.read_bytes() for p in directory.rglob('*') if p.is_file()}
    with patch.object(c, 'urlopen', side_effect=AssertionError('Network forbidden')):
        assert c.collect(directory, root) == first
    assert before == {str(p.relative_to(directory)): p.read_bytes() for p in directory.rglob('*') if p.is_file()}
    receipt = directory/(c.PLAN[0]['path']+'.provenance.json'); value = json.loads(receipt.read_text()); value['commit'] = '0'*40
    receipt.write_bytes(c.encode(value))
    with pytest.raises(ValueError): c.collect(directory, root)


def test_access_failure_sets_stop_and_never_retries(tmp_path):
    root, directory = setup_cache(tmp_path)
    with patch.object(c, 'urlopen', side_effect=OSError('403 denied')) as fetch:
        with pytest.raises(OSError): c.collect(directory, root)
        assert fetch.call_count == 1
    assert (directory/'ACCESS_STOP.json').exists()
    with patch.object(c, 'urlopen', side_effect=AssertionError('Must not retry')):
        with pytest.raises(RuntimeError): c.collect(directory, root)


def test_prior_private_public_and_log_changes_are_detected(tmp_path):
    root, directory = setup_cache(tmp_path)
    (root/'PLANNING_LOG.md').write_bytes(b'history\nappend\n'); c.protect(directory, root)
    (root/'data/private/prior.txt').write_bytes(b'changed')
    with pytest.raises(ValueError): c.protect(directory, root)
