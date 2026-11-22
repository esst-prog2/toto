"""Independent Phase 4 synthetic tests; no real sources or network needed."""
from copy import deepcopy
import json
from unittest.mock import patch

import pytest

from scripts import collect_segunda_feasibility as base
from scripts import collect_segunda_history as acquisition
from scripts import inventory_segunda_history as inventory
from scripts import validate_segunda_feasibility as feasibility
from scripts import validate_segunda_structure as s
from test_segunda_history import fixture_cache, acquire


def raw(body, year=2012):
    return (f'= Segunda División de España {year}/{str(year+1)[-2:]}\n# Teams 22\n# Matches 462\n'+body).encode()


def test_independent_parser_v_and_middle_score_utf8_crlf_and_missing_result():
    data = raw('▪ Matchday 1\nSat Aug 18 2012\n19:00  Alphá  v Beta  1-0 (0-0) [awarded]\n'
               '▪ 2. Round\nSun Aug 19\nBeta  0-0  Alphá\n▪ Regular Season - 3\nMon Aug 20\nAlphá v Beta\n').replace(b'\n', b'\r\n')
    records, notes, header = s.parse_source(data, 2012)
    assert len(records) == 3 and header['Teams'] == 22
    assert records[0]['home'] == 'Alphá' and records[0]['FT'] == '1-0'
    assert records[0]['HT'] == '0-0' and records[0]['annotation'] == '[awarded]'
    assert records[0]['year_basis'] == 'EXPLICIT_IN_DATE_HEADING'
    assert records[1]['year_basis'] == 'INFERRED_YEAR_SEASON_WINDOW_AND_WEEKDAY'
    assert records[2]['hg'] is records[2]['ag'] is records[2]['FT'] is None
    assert records[0]['raw_line_sha256'] == base.sha(data.splitlines(keepends=True)[records[0]['source_line']-1])


def test_covid_august_year_resolution_retains_heading_semantics():
    records, _, _ = s.parse_source(raw('▪ Matchday 42\nFri Aug 7\nAlpha v Beta  2-1\n', 2019), 2019)
    assert records[0]['date'] == '2020-08-07'
    assert records[0]['date_heading'] == 'Fri Aug 7'
    assert records[0]['year_basis'].startswith('INFERRED')


@pytest.mark.parametrize('body', [
    '▪ Promotion Playoff Final\n', '▪ Unknown stage\n',
    '▪ Matchday 1\nSun Aug 18 2012\nAlpha v Beta  1-0\n',
    '▪ Matchday 1\nSat Aug 18 2014\nAlpha v Beta  1-0\n',
    '▪ Matchday 1\nSat Aug 18 2012\nAlpha v Beta  1-?\n',
    '▪ Matchday 1\nSat Aug 18 2012\nAlpha v Beta  -1-0\n',
    '▪ Matchday 1\nSat Aug 18 2012\nAlpha v Beta  1.5-0\n',
    '▪ Matchday 1\nSat Aug 18 2012\n24:30 Alpha v Beta  1-0\n',
    '▪ Matchday 1\nAlpha v Beta  1-0\n',
    '▪ Matchday 1\nSat Aug 18 2012\nAlpha v Beta  1-0\n (unfinished\n',
])
def test_unrecognized_or_contradictory_source_fails_without_guessing(body):
    with pytest.raises(ValueError): s.parse_source(raw(body), 2012)


@pytest.mark.parametrize('title', ['Primera División 2012/13', 'Segunda División B 2012/13', 'Segunda División 2013/14'])
def test_competition_and_season_guard(title):
    data = ('= '+title+'\n▪ Matchday 1\nSat Aug 18 2012\nAlpha v Beta  1-0\n').encode()
    with pytest.raises(ValueError): s.parse_source(data, 2012)


def rows():
    fixtures = [('A', 'D'), ('B', 'C'), ('A', 'C'), ('D', 'B'), ('A', 'B'), ('C', 'D'),
                ('D', 'A'), ('C', 'B'), ('C', 'A'), ('B', 'D'), ('B', 'A'), ('D', 'C')]
    dates = ['2012-09-01', '2012-09-08', '2012-09-15', '2012-09-22', '2012-09-29', '2012-10-06']
    return [dict(source_line=i+1, home=h, away=a, date=dates[i//2], hg='1', ag='0', FT='1-0', HT='0-0',
                 round=i//2+1, stage='REGULAR_SEASON', annotation='', source_marked_awarded=False)
            for i, (h, a) in enumerate(fixtures)]


def test_complete_round_robin_halves_and_source_immutability():
    original = rows(); before = deepcopy(original); result = s.validate(original, 2012, 4)
    assert result['observed'] == result['score_bearing'] == result['complete_structurally_valid'] == 12
    assert result['structurally_invalid'] == result['incomplete'] == 0
    assert result['season_errors'] == [] and result['fixture_errors'] == {}
    assert all(h['complete'] and h['unique_pairs'] == 6 for h in result['half_seasons'])
    assert original == before


@pytest.mark.parametrize('change,code', [
    ('negative', 'INVALID_OR_CONTRADICTORY_SCORE'), ('float', 'INVALID_OR_CONTRADICTORY_SCORE'),
    ('partial', 'INVALID_OR_CONTRADICTORY_SCORE'), ('FT', 'INVALID_OR_CONTRADICTORY_SCORE'),
    ('HT', 'INVALID_OR_CONTRADICTORY_SCORE'), ('date', 'INVALID_DATE_OR_SEASON_BOUNDARY'),
    ('boundary', 'INVALID_DATE_OR_SEASON_BOUNDARY'), ('team', 'INVALID_TEAM_LABEL'),
    ('unicode', 'INVALID_TEAM_LABEL'), ('stage', 'NONREGULAR_STAGE')])
def test_fixture_level_contradictions_are_explicit(change, code):
    records = rows()
    if change == 'negative': records[0]['hg'] = '-1'
    if change == 'float': records[0]['hg'] = '1.1'
    if change == 'partial': records[0]['ag'] = None
    if change == 'FT': records[0]['FT'] = '9-9'
    if change == 'HT': records[0]['HT'] = '2-0'
    if change == 'date': records[0]['date'] = 'not a date'
    if change == 'boundary': records[0]['date'] = '2014-01-01'
    if change == 'team': records[0]['home'] = ' A'
    if change == 'unicode': records[0]['home'] = 'A\ufffd'
    if change == 'stage': records[0]['stage'] = 'PLAYOFF'
    before = deepcopy(records); result = s.validate(records, 2012, 4)
    assert code in result['fixture_errors']['1'] and records == before


def test_missing_score_is_incomplete_not_an_invented_draw_or_contradiction():
    records = rows(); records[0].update(hg=None, ag=None, FT=None, HT=None)
    result = s.validate(records, 2012, 4)
    assert result['incomplete'] == 1 and result['score_bearing'] == 11
    assert result['structurally_invalid'] == 0 and result['complete_structurally_valid'] == 11
    assert result['outcomes'] == {'1': 11}


def test_duplicate_missing_pairs_rounds_and_appearance_counts_are_not_forced():
    records = rows(); records[-1] = dict(records[0], source_line=12)
    result = s.validate(records, 2012, 4)
    assert result['duplicate_pairs'] and result['missing_pairs']
    assert 'DUPLICATE_DIRECTED_PAIR' in result['fixture_errors']['1']
    assert 'APPEARANCE_ALLOCATION' in result['season_errors']
    assert any('HALF_SEASON_PAIRING' in e for e in result['season_errors'])


def test_case_and_unicode_equivalent_labels_are_not_silently_merged():
    records = rows(); records[0]['home'] = 'a'
    result = s.validate(records, 2012, 4)
    assert result['normalized_collisions'] == {'a': ['A', 'a']}
    assert 'TEAM_IDENTITY_COLLISION' in result['season_errors']


def test_review_flags_are_distinct_from_structural_errors():
    records = rows(); records[0].update(hg='6', ag='6', FT='6-6', annotation='[awarded]', source_marked_awarded=True)
    result = s.validate(records, 2012, 4)
    assert result['structurally_invalid'] == 0
    assert set(result['flags']['1']) == {'SOURCE_ANNOTATION', 'SOURCE_MARKED_ADMINISTRATIVE_AWARD', 'UNUSUAL_SCORE_REVIEW'}


def test_short_rest_and_same_day_collision_are_different():
    records = rows(); records[2]['date'] = '2012-09-02'
    result = s.validate(records, 2012, 4)
    assert 'SHORT_REST_DATE_REVIEW' in result['flags']['3']
    assert result['structurally_invalid'] == 0
    records[2]['date'] = '2012-09-01'
    result = s.validate(records, 2012, 4)
    assert 'SAME_TEAM_DATE_COLLISION' in result['fixture_errors']['3']


def test_wide_round_tie_uses_earliest_cluster_and_never_changes_dates():
    records = [dict(round=1, source_line=1, date='2012-09-01'), dict(round=1, source_line=2, date='2012-10-01')]
    before = deepcopy(records); span = s.wide_rounds(records)[0]
    assert span['diagnostic_cluster_start'] == '2012-09-01'
    assert span['diagnostic_outlier_lines'] == [2] and records == before


def context():
    return dict(reus=dict(expulsion_decision_date='2019-01-28', evidence=['reus']),
                rayo_albacete=dict(source_file='raw', original=dict(source_line=1), original_kickoff_date='2019-12-15',
                                   completion_date='2020-06-10', evidence=['rayo']),
                deportivo_fuenlabrada=dict(source_file='raw', original=dict(source_line=2),
                                          original_scheduled_date='2020-07-20', actual_playing_date='2020-08-07', evidence=['dep']))


def chronology_row(line, **extra):
    return dict(source_file='raw', source_line=line, date='2020-06-10', date_heading='Wed Jun 10 2020',
                year_basis='EXPLICIT_IN_DATE_HEADING', kickoff='20:00', hg='1', ag='0', FT='1-0',
                home='A', away='B', source_marked_awarded=False, **extra)


def test_chronology_context_never_assigns_policy_or_replaces_source_dates():
    r = chronology_row(1); result = s.chronology(r, context())
    assert result['source_date'] == '2020-06-10' and result['original_kickoff_date'] == '2019-12-15'
    assert result['actual_completion_date'] == '2020-06-10' and result['effective_result_date'] is None
    r = chronology_row(2); r['date'] = '2020-08-07'; result = s.chronology(r, context())
    assert result['scheduled_date'] == '2020-07-20' and result['actual_playing_date'] == '2020-08-07'
    assert result['original_kickoff_date'] is None and result['effective_result_date'] is None


def test_award_and_missing_scores_have_no_known_result_availability():
    r = chronology_row(3); r.update(home='CF Reus Deportiu', source_marked_awarded=True)
    result = s.chronology(r, context())
    assert result['source_administrative_result'] == '1-0' and result['on_field_result'] is None
    assert result['administrative_decision_date'] == '2019-01-28' and result['effective_result_date'] is None
    r.update(source_marked_awarded=False, hg=None, ag=None, FT=None)
    assert s.chronology(r, context())['availability'] == 'MISSING_RESULT_NO_AVAILABILITY_DATE'


def test_label_variants_are_diagnostics_and_reserve_names_stay_distinct():
    records = [dict(home='Cádiz CF', away='Alpha B'), dict(home='Cadiz CF', away='Alpha')]
    assert s.label_variants(records) == {'cadiz cf': ['Cadiz CF', 'Cádiz CF']}
    assert records[0]['home'] == 'Cádiz CF' and records[0]['away'] == 'Alpha B'


def test_context_identity_hash_and_facts_must_all_match():
    r = rows()[0]; receipt = dict(path='raw', sha256='0'*64)
    case = dict(source_sha256=receipt['sha256'], source_fixture_id=s.source_id('raw', '0'*64, 1), original=deepcopy(r))
    # Supply the source-contract fields relevant to this binding.
    for k in ('raw_record', 'kickoff'): r[k] = case['original'][k] = None
    s.context_binding(case, {1: r}, receipt)
    case['source_sha256'] = '1'*64
    with pytest.raises(ValueError): s.context_binding(case, {1: r}, receipt)


def build_fixture(tmp_path):
    root, directory, bodies = fixture_cache(tmp_path); acquire(root, directory, bodies)
    phase3 = inventory.build(directory, root)
    # Saved counts are deliberately false: Phase 4 must derive its own totals.
    phase3['totals']['observed'] = 6006
    base.save(directory/'phase3_inventory.json', base.encode(phase3))
    log = (root/'PLANNING_LOG.md').read_bytes()
    files = {str(p.relative_to(root)): base.sha(p.read_bytes()) for p in directory.rglob('*') if p.is_file()}
    base.save(directory/s.BASELINE, base.encode(dict(files=files, planning_log=dict(bytes=len(log), sha256=base.sha(log)))))
    return root, directory


def test_build_is_independent_deterministic_deduplicated_and_preserves_sources(tmp_path):
    root, directory = build_fixture(tmp_path)
    before = {str(p): p.read_bytes() for p in directory.rglob('*') if p.is_file()}
    with patch.object(feasibility, 'parse_text', side_effect=AssertionError('Do not use old parser')), \
         patch.object(feasibility, 'assess', side_effect=AssertionError('Do not use old validator')):
        first = s.build(directory, root); second = s.build(directory, root)
    assert first == second
    report, queue = json.loads(first[s.REPORT]), json.loads(first[s.QUEUE])
    assert report['totals']['observed'] == 14 and len(report['records']) == 14
    assert len(queue['records']) == len({r['fixture']['source_fixture_id'] for r in queue['records']})
    assert sum(queue['category_counts'].values()) > len(queue['records'])
    assert all(r['chronology']['effective_result_date'] is None for r in report['records'])
    assert before == {str(p): p.read_bytes() for p in directory.rglob('*') if p.is_file()}


def test_frozen_inventory_and_original_tampering_are_rejected(tmp_path):
    root, directory = build_fixture(tmp_path)
    path = directory/'phase3_inventory.json'; path.write_bytes(path.read_bytes()+b' ')
    with pytest.raises(ValueError): s.build(directory, root)
