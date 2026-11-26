"""Belgian Phase 6 source-bound retrospective adjudication; no standardized CSV.

Human historical findings are preserved inputs. This module selects no new source
observations and applies no publication-time filter. INCLUDE is technical/historical
acceptance for retrospective diagnostics, never training or redistribution clearance.
"""
import argparse
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import date
from pathlib import Path
import json
import os
import re
import subprocess
import sys
import tempfile

from scripts import verify_belgian_pro_league_review as review

ROOT, PRIVATE = review.ROOT, review.PRIVATE
encode, sha = review.encode, review.sha
POLICY_VERSION = 'BELGIUM_RETROSPECTIVE_INTERNAL_V1'
DISPOSITIONS = {'INCLUDE', 'HOLD_OUT', 'NOT_PLAYED', 'OUT_OF_SCOPE'}
STAGES = ('REGULAR_SEASON', 'CHAMPIONSHIP', 'EUROPE', 'PLAYDOWNS',
          'TITLE_DECIDER', 'EUROPE_QUALIFICATION', 'PROMOTION_RELEGATION')
NAMES = ('policy.json', 'decision_registry.json', 'documentary_decisions.json',
         'exception_decisions.json', 'season_stage_matrix.json', 'reconciliation.json')
# Explicit bindings, not name/date fuzzy matching. The frozen reviewed fixture
# must still match its bound row and its own source date and reported score.
CASE_RULES = {
    'standard_anderlecht_2019': ('HOLD_OUT', 'ADMIN_RESULT_INSUFFICIENT_DIRECT_EVIDENCE'),
    'standard_westerlo_2024': ('NOT_PLAYED', 'NO_FOOTBALL_PLAYED_ADMIN_AWARD'),
    'leuven_mechelen_2022': ('NOT_PLAYED', 'NO_FOOTBALL_PLAYED_ADMIN_AWARD'),
    'union_beerschot_2022': ('INCLUDE', 'PLAYED_OFFICIALLY_ADJUDICATED_RESULT'),
    'standard_charleroi_2021': ('INCLUDE', 'PLAYED_OFFICIALLY_ADJUDICATED_RESULT'),
    'beerschot_cercle_resumed': ('INCLUDE', 'RESUMED_ORIGINAL_KICKOFF_DATE'),
    'seraing_union_resumed': ('INCLUDE', 'RESUMED_ORIGINAL_KICKOFF_DATE'),
}


def read(path):
    return json.loads(path.read_text())


def preserve(directory=PRIVATE):
    previous = review.protect(directory)
    baseline = read(directory / 'phase6_protected_before.json')
    for name, digest in baseline['files'].items():
        path = ROOT / name
        if not path.resolve().is_relative_to(ROOT.resolve()) or sha(path.read_bytes()) != digest:
            raise ValueError('Frozen Phase 2–5/recovery file changed: ' + name)
    prefix = baseline['planning_log']
    if sha((ROOT / 'PLANNING_LOG.md').read_bytes()[:prefix['bytes']]) != prefix['sha256']:
        raise ValueError('Planning history changed')
    return dict(previous=previous, frozen_entries=len(baseline['files']))


def iso_day(value):
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        raise ValueError('Explicit ISO match date required')
    return date.fromisoformat(value)


def score(value):
    if not isinstance(value, str) or not re.fullmatch(r'(0|[1-9]\d*)-(0|[1-9]\d*)', value):
        raise ValueError('Valid source final score required')
    home, away = map(int, value.split('-'))
    return dict(home_goals=home, away_goals=away,
                outcome='H' if home > away else 'A' if home < away else 'D')


def stage_action(stage, season):
    """Policy scope: official top-flight stages, excluding cross-division ties.

    TITLE_DECIDER is conditionally eligible, but no such dated observation is
    independently stage-bound in the current source inventory.
    """
    if stage == 'PROMOTION_RELEGATION':
        return 'OUT_OF_SCOPE', 'CROSS_DIVISION_CONTEST'
    if stage == 'REGULAR_SEASON':
        return 'INCLUDE', 'TOP_FLIGHT_REGULAR'
    years = {'CHAMPIONSHIP': {2018, 2020, 2021, 2023, 2024},
             'EUROPE': {2020, 2021, 2023, 2024},
             'PLAYDOWNS': {2023, 2024},
             'EUROPE_QUALIFICATION': {2023, 2024}}
    if stage in years and int(season[:4]) in years[stage]:
        return 'INCLUDE', 'DOCUMENTED_TOP_FLIGHT_STAGE'
    return 'HOLD_OUT', 'STAGE_OR_PARTICIPANT_SCOPE_NOT_ESTABLISHED'


def policy():
    return dict(version=POLICY_VERSION, purpose='RETROSPECTIVE_INTERNAL_SYSTEM_DIAGNOSTICS',
                leakage_free_historical_forecasting=False,
                result_availability_filter=False,
                date_rule='Original football kickoff when reliably documented; scheduled source fixture date for audit only where no kickoff; administrative judgment never replaces match date',
                result_rule='Accepted final score for a played eligible event, including later administrative results; no elapsed-minute threshold invented',
                played_rule='Recorded competitive football must have occurred; inspected explicit case decision required for abandoned/awarded events',
                no_kickoff_rule='NOT_PLAYED even with an awarded numerical score; award retained as audit evidence only',
                annulment_rule='Annulled documentary events not promoted automatically; unresolved primary treatment remains HOLD_OUT; source n/p slots remain NOT_PLAYED documentary-only',
                source_gap_rule='Coverage metadata only; never fabricate an event, result or NOT_PLAYED disposition',
                source_preference='Historical CSV where agreed; otherwise independently bound modern/RSSSF final representation; all contributing representations preserved',
                stage_rule='Official top-flight regular, championship, top-flight-only Europe, playdown and European qualifier eligible; title tests require specific stage/participant proof; cross-division OUT_OF_SCOPE; unknown/mixed-tier eligibility HOLD_OUT unless explicit scope established',
                uncertainty_rule='Material score/date/identity/stage conflict or unreviewed exceptional result HOLD_OUT; ordinary missing independent certification or long round alone is not an error',
                dispositions=sorted(DISPOSITIONS), source_gap_is_not_disposition=True,
                rights='NOT_CLEARED_FOR_MODEL_TRAINING_OR_REDISTRIBUTION',
                application_or_prediction_algorithm_changes=False)


def union_groups(observed, links, comparison, recovered):
    """Union only the approved 1,402+306 links; never match by score or city."""
    rows = observed['historical'] + [r for rs in observed['modern'].values() for r in rs]
    index = {r['audit_id']: r for r in rows}
    if len(index) != len(rows):
        raise ValueError('Duplicate original identity')
    parent = {key: key for key in index}
    def find(key):
        if key not in parent:
            raise ValueError('Unknown link endpoint')
        while parent[key] != key:
            key = parent[key]
        return key
    def join(a, b):
        a, b = find(a), find(b)
        if a == b:
            raise ValueError('Repeated/cyclic linkage')
        parent[max(a, b)] = min(a, b)
    paired = set()
    for source in links.values():
        for link in source['links']:
            h, m = link['historical_id'], link['modern_id']
            if h in paired or m in paired:
                raise ValueError('Repeated approved pair endpoint')
            if not link['date_equal'] or not link['score_equal']:
                raise ValueError('Conflicting approved pair')
            if index[h]['date'] != index[m]['date'] or index[h]['FT'] != index[m]['FT'] or index[h]['season'] != index[m]['season']:
                raise ValueError('Source pair facts changed')
            paired.update((h, m)); join(h, m)
    groups = defaultdict(list)
    for key, row in index.items():
        groups[find(key)].append(dict(kind='CSV_TXT', binding=deepcopy(row)))
    event_by_key = {tuple(e['diagnostic_event_key']): e for e in recovered['events']}
    if len(event_by_key) != len(recovered['events']):
        raise ValueError('Duplicate recovered event identity')
    attached = set()
    for link in comparison['matches']:
        event = link['documentary']; key = tuple(event['diagnostic_event_key'])
        if key in attached or key not in event_by_key or event_by_key[key] != event:
            raise ValueError('Repeated or changed documentary linkage')
        historical = index[link['historical']['source_id']]
        if historical['source_line'] != link['historical']['source_line'] or historical['physical_record_sha256'] != link['historical']['raw_record_sha256']:
            raise ValueError('Recovery physical binding changed')
        if not link['date_equal'] or not link['score_equal'] or historical['date'] != event['comparison_date'] or historical['FT'] != event['comparison_score']:
            raise ValueError('Recovered date/score conflict')
        groups[find(historical['audit_id'])].append(dict(kind='RSSSF_EVENT', binding=deepcopy(event)))
        attached.add(key)
    for key, event in event_by_key.items():
        if key not in attached:
            groups['RSSSF:' + sha(encode(key))].append(dict(kind='RSSSF_EVENT', binding=deepcopy(event)))
    return [groups[key] for key in sorted(groups)]


def identity_ids(representations):
    return sorted(sid for rep in representations for sid in
                  ([rep['binding']['audit_id']] if rep['kind'] == 'CSV_TXT' else rep['binding']['source_ids']))


def make_event(representations, historical_stages):
    originals = [rep['binding'] for rep in representations if rep['kind'] == 'CSV_TXT']
    documents = [rep['binding'] for rep in representations if rep['kind'] == 'RSSSF_EVENT']
    final_scores = {r['FT'] for r in originals}
    final_scores.update(e['comparison_score'] for e in documents)
    dates = {r['date'] for r in originals} | {e['comparison_date'] for e in documents}
    seasons = {r['season'] for r in originals} | {e['diagnostic_event_key'][0] for e in documents}
    stages = set()
    for r in originals:
        stage = r['stage'] if r['stage'] != 'UNKNOWN' else historical_stages.get(r['audit_id'], 'UNKNOWN')
        stages.add(stage)
    for e in documents:
        raw = e['diagnostic_event_key'][1]
        stages.add('REGULAR_SEASON' if raw == 'REGULAR' else raw)
    stages.discard('UNKNOWN')
    # Original round/group/leg labels remain attached even where sources use
    # different conventions. Never invent a shared round or flatten distinct legs.
    stage_bindings = [dict(source_ids=[r['audit_id']], stage=r['stage'],
                           group=r.get('group'), round=r.get('round'), leg=r.get('leg'))
                      for r in originals]
    stage_bindings += [dict(source_ids=e['source_ids'],
                            stage=e['diagnostic_event_key'][1],
                            round=e['diagnostic_event_key'][2],
                            leg=e['diagnostic_event_key'][3], group=None)
                       for e in documents]
    ids = identity_ids(representations)
    if len(ids) != len(set(ids)) or len(seasons) != 1:
        raise ValueError('Duplicate representation or mixed-season event')
    preferred = next((r for r in originals if 'jalapic/' in r['source']), originals[0] if originals else None)
    if preferred:
        home, away, original_date, reported = preferred['home'], preferred['away'], preferred['date'], preferred['FT']
    else:
        e = documents[0]; home, away = e['diagnostic_event_key'][4:6]
        original_date, reported = e['comparison_date'], e['comparison_score']
    return dict(decision_id=sha(encode([POLICY_VERSION, ids])), season=next(iter(seasons)),
                home=home, away=away, original_fixture_date=original_date,
                stage=next(iter(stages)) if len(stages) == 1 else 'UNKNOWN',
                stage_identity_bindings=stage_bindings,
                stage_conflict=len(stages) > 1, source_fact_conflict=len(dates) > 1 or len(final_scores) > 1,
                reported_score=reported, representations=deepcopy(representations), source_ids=ids,
                representations_count=sum(1 if rep['kind'] == 'CSV_TXT' else len(rep['binding']['representations']) for rep in representations),
                kickoff_date=None, completion_date=None, administrative_decision_context=None,
                football_status='SOURCE_REPORTED_COMPLETED' if reported else 'UNSCORED_SCHEDULED_SLOT',
                accepted_score=None, chosen_match_date=None, accepted_outcome=None,
                disposition=None, reason=None, evidence_ids=[],
                uncertainty_flags=['INDEPENDENT_FULL_FACT_CERTIFICATION_NOT_UNIVERSAL', 'UPSTREAM_SOURCE_INDEPENDENCE_NOT_ESTABLISHED'],
                evaluation_purpose='RETROSPECTIVE_INTERNAL_SYSTEM_DIAGNOSTICS',
                licensing_clearance='NOT_CLEARED', model_training_clearance='NOT_CLEARED',
                historical_forecasting_claim_allowed=False)


def adjudicate(event, case=None):
    result = deepcopy(event)
    action, reason = stage_action(event['stage'], event['season'])
    if event['stage_conflict'] or event['source_fact_conflict']:
        action, reason = 'HOLD_OUT', 'MATERIAL_SOURCE_CONFLICT'
    annotations = [rep['binding'].get('annotation', '') for rep in event['representations'] if rep['kind'] == 'CSV_TXT']
    documentary_exception = any(e['binding'].get('explicit_continuation_group') or
        any(r['score_token'] in {'awd', 'abd'} for r in e['binding']['representations'])
        for e in event['representations'] if e['kind'] == 'RSSSF_EVENT')
    material = any(re.search(r'awarded|abandon|annull|interrupted', a, re.I) for a in annotations) or documentary_exception
    cancelled = any('[cancelled]' in a for a in annotations)
    selected_date = event['original_fixture_date']
    if case is not None:
        if case['id'] not in CASE_RULES:
            raise ValueError('Unapproved exceptional case')
        bound = {r['audit_id'] for r in case['source_bindings']}
        if not bound or not bound <= set(event['source_ids']) or event['original_fixture_date'] != case['date'] or event['reported_score'] != case['score']:
            raise ValueError('Exceptional decision detached from approved source')
        original_bindings = {rep['binding']['audit_id']: rep['binding']
                             for rep in event['representations'] if rep['kind'] == 'CSV_TXT'}
        if any(original_bindings.get(r['audit_id']) != r for r in case['source_bindings']):
            raise ValueError('Exceptional physical source binding differs')
        if action != 'INCLUDE' or event['source_fact_conflict'] or event['stage_conflict']:
            raise ValueError('Exceptional case cannot override material identity/stage conflict')
        action, reason = CASE_RULES[case['id']]
        result.update(case_id=case['id'], evidence_ids=case['evidence_ids'],
                      administrative_decision_context=case['decision'],
                      football_status=case['completion'])
        result['uncertainty_flags'].append(case['finality'])
        if case['id'].endswith('_resumed'):
            selected_date = case['kickoff']
            iso_day(selected_date); iso_day(case['completion_date'])
            if selected_date >= case['completion_date']:
                raise ValueError('Invalid kickoff/completion chronology')
            result.update(kickoff_date=selected_date, completion_date=case['completion_date'])
        elif action == 'INCLUDE':
            result['kickoff_date'] = event['original_fixture_date']
        result['availability_history_audit_only'] = case['availability']
    elif material:
        action, reason = 'HOLD_OUT', 'EXCEPTION_REQUIRES_EXPLICIT_REVIEW'
    elif cancelled:
        if event['season'] != '2019/2020' or event['stage'] != 'REGULAR_SEASON' or event['reported_score'] is not None:
            raise ValueError('Unreviewed cancellation')
        action, reason = 'NOT_PLAYED', 'DOCUMENTED_COVID_TERMINATION'
        result['football_status'] = 'CANCELLED_SOURCE_AND_SEASON_TERMINATION'
        result['evidence_ids'] = ['covid_bca', 'covid_bas', 'covid_league']
    elif action == 'INCLUDE' and event['reported_score'] is None:
        action, reason = 'HOLD_OUT', 'MISSING_FINAL_SCORE_NOT_CANCELLATION'
    if action == 'INCLUDE':
        facts = score(event['reported_score']); iso_day(selected_date)
        result.update(accepted_score=event['reported_score'], chosen_match_date=selected_date,
                      accepted_outcome=facts['outcome'])
        if result['kickoff_date'] is None:
            result['kickoff_date'] = selected_date
            result['uncertainty_flags'].append('ORDINARY_SOURCE_MATCH_DATE_NOT_UNIVERSALLY_INDEPENDENTLY_VERIFIED')
    result.update(disposition=action, reason=reason)
    return result


def eligible_for_phase7(decision):
    """Fail-closed metadata guard only, not a model-training permission gate."""
    if decision['disposition'] != 'INCLUDE':
        return False
    if decision['source_fact_conflict'] or decision['stage_conflict'] or not decision['source_ids']:
        raise ValueError('Invalid INCLUDE binding')
    score(decision['accepted_score']); iso_day(decision['chosen_match_date'])
    if decision['accepted_score'] != decision['reported_score']:
        raise ValueError('Unapproved score substitution')
    if decision['chosen_match_date'] != decision['kickoff_date']:
        raise ValueError('Chosen date must retain the documented kickoff')
    if decision.get('case_id', '').endswith('_resumed'):
        if not decision['completion_date'] or decision['kickoff_date'] >= decision['completion_date']:
            raise ValueError('Resumption chronology lost')
    elif decision['chosen_match_date'] != decision['original_fixture_date']:
        raise ValueError('Administrative date cannot replace fixture date')
    return True


def documentary_decisions(rows):
    output = []
    for row in rows:
        token = row['score']
        is_np = token == 'n/p'
        if not is_np and not ('annulled' in row['annotation'] or token == 'awd'):
            raise ValueError('Unreviewed Mouscron documentary exception')
        output.append(dict(documentary_id=row['audit_id'], source_binding=deepcopy(row), season='2009/2010',
                           disposition='NOT_PLAYED' if is_np else 'HOLD_OUT',
                           reason='DOCUMENTARY_EXPLICIT_NP' if is_np else 'ANNULLED_TREATMENT_AND_PRIMARY_EVIDENCE_UNRESOLVED',
                           reported_score=token, accepted_score=None, chosen_match_date=None,
                           football_status='DOCUMENTARY_NOT_PLAYED' if is_np else 'ANNULLED_AWARD' if token == 'awd' else 'PLAYED_NUMERIC_RESULT_REPORTED_ANNULLED',
                           evidence_ids=['mouscron', 'mouscron_catalogue'],
                           uncertainty_flags=['DOCUMENTARY_ONLY_NOT_NEW_STANDARD_SOURCE', 'NO_VERIFIED_INDIVIDUAL_ISO_DATE', 'PRIMARY_ANNULMENT_JUDGMENT_NOT_INSPECTED'],
                           included_in_10434_population=False))
    if len({r['documentary_id'] for r in output}) != len(output):
        raise ValueError('Duplicate documentary representation')
    return output


def check_registry(decisions, expected_source_ids):
    used = [sid for d in decisions for sid in d['source_ids']]
    if len(used) != len(set(used)) or set(used) != set(expected_source_ids):
        raise ValueError('Missing/reused original representations')
    if len({d['decision_id'] for d in decisions}) != len(decisions):
        raise ValueError('Duplicate decision identity')
    for d in decisions:
        if d['disposition'] not in DISPOSITIONS:
            raise ValueError('Unknown disposition')
        if not eligible_for_phase7(d) and any(d[k] is not None for k in ('accepted_score', 'chosen_match_date', 'accepted_outcome')):
            raise ValueError('Non-INCLUDE carries screened values')


def build(directory=PRIVATE):
    preserve(directory)
    observed = read(directory / 'phase4/source_observations.json')
    structure = read(directory / 'phase4/structural_assessment.json')
    recovered = read(directory / 'recovery2021/event_registry.json')
    comparison = read(directory / 'recovery2021/historical_comparison.json')
    links = read(directory / 'phase4/overlap_reconciliation.json')
    cases = read(directory / 'phase5/review/exception_assessments.json')['fixtures']
    groups = union_groups(observed, links, comparison, recovered)
    inferred = {}
    for season, assessment in structure['historical_seasons'].items():
        prefix = assessment['prefix_candidate']
        if prefix is not None:
            historical = [r for r in observed['historical'] if r['season'] == season]
            for row in historical[:prefix]:
                inferred[row['audit_id']] = 'REGULAR_SEASON'
    by_sid = {}
    for case in cases:
        for row in case['source_bindings']:
            if row['audit_id'] in by_sid:
                raise ValueError('Repeated exceptional binding')
            by_sid[row['audit_id']] = case
    decisions = []
    for reps in groups:
        event = make_event(reps, inferred)
        bound_cases = {by_sid[sid]['id']: by_sid[sid] for sid in event['source_ids'] if sid in by_sid}
        if len(bound_cases) > 1:
            raise ValueError('Multiple exceptional decisions for one event')
        decisions.append(adjudicate(event, next(iter(bound_cases.values()), None)))
    decisions.sort(key=lambda d: (d['season'], d['original_fixture_date'], d['decision_id']))
    expected_ids = [r['audit_id'] for r in observed['historical']] + [r['audit_id'] for rows in observed['modern'].values() for r in rows]
    expected_ids += [sid for e in recovered['events'] for sid in e['source_ids']]
    check_registry(decisions, expected_ids)
    counts = Counter(d['disposition'] for d in decisions)
    representations = sum(d['representations_count'] for d in decisions)
    if len(decisions) != 8724 or representations != 10434 or len(expected_ids) != 10434:
        raise ValueError('Approved source-to-event population changed')
    documentary = documentary_decisions(read(directory / 'phase4/exception_registry.json')['documentary_exceptions'])
    stage_matrix = []
    coverage = []
    for year in range(1990, 2026):
        season = f'{year}/{year+1}'; ds = [d for d in decisions if d['season'] == season]
        coverage.append(dict(season=season, source_events=len(ds), representations=sum(d['representations_count'] for d in ds),
                             dispositions=dict(Counter(d['disposition'] for d in ds)),
                             coverage_status='SOURCE_GAP' if year < 1995 else 'INCOMPLETE_PINNED_SNAPSHOT' if year == 2025 else 'OBSERVED_SOURCES_NOT_COMPLETE_ALL_STAGES',
                             missing_coverage_notes=('No approved complete dated source; no fabricated fixtures' if year < 1995 else
                               'Lommel played/annulled/never-played population missing;272 retained records only' if year == 2002 else
                               'Mouscron30 documentary slots separate; primary treatment unresolved' if year == 2009 else
                               'Actual OpenFootball2021/22 absent; RSSSF recovery used explicitly' if year == 2021 else
                               '119 unscored slots, no postseason; not assumed cancelled' if year == 2025 else
                               'No claim that absent playoffs/title tests were never played'),
                             documentary_only_dispositions=dict(Counter(d['disposition'] for d in documentary)) if year == 2009 else {}))
        for stage in STAGES:
            subset = [d for d in ds if d['stage'] == stage]
            action, reason = stage_action(stage, season)
            stage_matrix.append(dict(season=season, stage=stage, stage_policy=action, reason=reason,
                                     observed_events=len(subset), dispositions=dict(Counter(d['disposition'] for d in subset)),
                                     source_ids=sorted(sid for d in subset for sid in d['source_ids']),
                                     no_observation_is_not_not_played=True))
    special = [d for d in decisions if 'case_id' in d]
    if len(special) != 7:
        raise ValueError('Exceptional decisions incomplete')
    for item in stage_matrix:
        item['evidence_ids'] = (['stages_2018'] if item['season'] == '2018/2019' else ['covid_league'] if item['season'] == '2020/2021' else ['stages_2024'] if item['season'] in {'2023/2024','2024/2025'} else [])
    endpoints = [d for d in decisions if d.get('case_id') == 'standard_westerlo_2024' or
                 (d['season'] == '2024/2025' and d['stage'] == 'EUROPE_QUALIFICATION')]
    if len(endpoints) != 2:
        raise ValueError('Unmatched endpoints not uniquely adjudicated')
    documentary_counts = dict(Counter(d['disposition'] for d in documentary))
    return dict(zip(NAMES, [policy(), dict(decisions=decisions, counts=dict(counts), historical_certification=False),
        dict(decisions=documentary, counts=documentary_counts, outside_combined_source_population=True),
        dict(fixtures=special, endpoints=endpoints,
             lommel=dict(retained_events=272, added_events=0, coverage='SOURCE_GAP_UNQUANTIFIED_PLAYED_AND_ANNULLED_EVENTS',
                         evidence_ids=['lommel_uefa_march','lommel_uefa_april','lommel_may'],
                         reason='No adequate individually dated omitted source inventory; never equate absence with no play'),
             mouscron=dict(retained_events=210, documentary_only=30, documentary_dispositions=documentary_counts,
                           reason='No promotion of annulled numeric/award documentary slots pending defensible final treatment; n/p not played without invented dates'),
             covid=dict(source_slots=8, disposition='NOT_PLAYED', reason='Documented termination; source-bound cancelled round, no scores invented')),
        dict(coverage=coverage, stages=stage_matrix, target_seasons=36),
        dict(csv_txt_observations=10100, supplemental_descriptions=334, combined_representations=representations,
             conditional_events=len(decisions), dispositions=dict(counts),
             documentary_only_observations=len(documentary), documentary_dispositions=documentary_counts,
             source_gap_seasons=[c['season'] for c in coverage if c['coverage_status']=='SOURCE_GAP'],
             population_not_enlarged_by_research=True, data_filtering_by_administrative_timestamp=False,
             source_representation_unique=True, rights_clearance=False)]))


def generate(directory=PRIVATE, output=None):
    output = Path(output) if output else directory / 'phase6'
    artifacts = {name: encode(obj) for name, obj in build(directory).items()}
    artifacts['reproducibility.json'] = encode(dict(policy_version=POLICY_VERSION,
        inputs={str(p.relative_to(directory)): sha(p.read_bytes()) for p in (directory/'phase6_protected_before.json', directory/'phase5/review/reproducibility.json')},
        implementation_sha256=sha(Path(__file__).read_bytes()),
        artifacts={name: sha(raw) for name, raw in artifacts.items()}, standardized_dataset_created=False))
    for name, raw in artifacts.items():
        review.recovery.keep(output / name, raw)
    return {name: sha(raw) for name, raw in artifacts.items()}


def verify(directory=PRIVATE):
    with tempfile.TemporaryDirectory(prefix='belgium-phase6-regeneration-') as tmp:
        proc = subprocess.run([sys.executable, '-B', '-m', 'scripts.decide_belgian_pro_league_policy', '--output', tmp],
                              cwd=ROOT, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'),
                              capture_output=True, text=True, timeout=120)
        if proc.returncode:
            raise ValueError(proc.stdout + proc.stderr)
        result = {}
        for name in (*NAMES, 'reproducibility.json'):
            saved, fresh = (directory / 'phase6' / name).read_bytes(), (Path(tmp)/name).read_bytes()
            if saved != fresh:
                raise ValueError('Regeneration differs: ' + name)
            result[name] = dict(sha256=sha(saved), bytes=len(saved), byte_identical=True)
    return dict(artifacts=result, protected=preserve(directory))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    print(json.dumps(verify() if args.verify else generate(output=args.output), indent=2))
