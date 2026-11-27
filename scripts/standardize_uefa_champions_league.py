"""Offline Phase 4 projection of approved UCL decisions; private outputs only.

Stage, period, source and decision evidence stay in a private sidecar. This does
not integrate historical data with the application or change model behavior.
"""
from __future__ import annotations
from collections import Counter, defaultdict
import argparse
import hashlib
import json
from pathlib import Path

from scripts.artifact_io import check_overwrite, serialize_csv
from toto_estimator.historical_import import canonical_season
from toto_estimator.match_schema import CANONICAL_COLUMNS, canonical_match_id, validate_canonical_records
from toto_estimator.validation import team_name

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'data/private/europe/champions_league'
PHASE = BASE / 'phase4'
NAME = 'uefa_champions_league_standardized_1992_2026.csv'
LEAGUE = 'UEFA Champions League'
CONVENTIONAL = {'PRELIMINARY', 'QUALIFYING_ROUND_1', 'QUALIFYING_ROUND_2', 'QUALIFYING_ROUND_3',
                'QUALIFYING_PLAYOFF', 'PRE_GROUP_ROUND_1', 'PRE_GROUP_ROUND_2', 'FIRST_GROUP',
                'SECOND_GROUP', 'LEAGUE_PHASE', 'KNOCKOUT_PLAYOFF', 'ROUND_OF_16', 'QUARTERFINAL', 'SEMIFINAL'}


def read(path): return json.loads(path.read_bytes())
def sha(raw): return hashlib.sha256(raw).hexdigest()
def wire(obj): return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()
def require(test, message):
    if not test: raise ValueError(message)


def classify_format(event, policy):
    """Source-bound overrides precede documented season/stage format rules."""
    if event['event_id'] in policy['event_overrides']:
        rule = policy['event_overrides'][event['event_id']]
        require(all(event[k] == v for k, v in rule['expected'].items()), 'Neutral-format override identity changed')
        return rule['value'], rule['rule']
    year, stage = int(event['season'][:4]), event['stage']
    if stage == 'FINAL': return 1, 'OFFICIAL_FINAL'
    if year == 2019 and stage in {'QUARTERFINAL', 'SEMIFINAL'}:
        return 1, 'LISBON_2020_CENTRALIZED'
    if 2018 <= year <= 2023 and stage in {'PRELIMINARY_SEMIFINAL', 'PRELIMINARY_FINAL'}:
        return 1, 'NEUTRAL_PRELIMINARY_TOURNAMENT'
    if stage in CONVENTIONAL: return 0, 'CONVENTIONAL_HOME_AWAY'
    return None, 'UNESTABLISHED_FORMAT'


def project(event, policy):
    require(event['disposition'] == 'INCLUDE', 'Excluded event cannot enter canonical output')
    score = event['accepted_result']
    require(score is not None and len(score) == 2 and all(type(x) is int and x >= 0 for x in score), 'Unsupported accepted result')
    require(event['result_basis'] in {'SUPPORTED_REGULATION', 'RETROSPECTIVE_PLAYED_ADMINISTRATIVE_EXCEPTION'}, 'Unapproved result basis')
    if event['result_basis'] == 'SUPPORTED_REGULATION':
        require(score == event['regulation_time'], 'Extra-time/aggregate cannot replace regulation')
    else:
        require(score == event['administrative_result'] and event['applied_decisions'], 'Unsupported administrative exception')
    outcome = 'X' if score[0] == score[1] else '1' if score[0] > score[1] else '2'
    require(event['outcome'] == outcome, 'First-listed outcome mismatch')
    season = canonical_season(event['season'])
    home = team_name(event.get('historical_home', event['first_listed']))
    away = team_name(event.get('historical_away', event['second_listed']))
    day = event['football_date']
    neutral, rule = classify_format(event, policy)
    values = (canonical_match_id(LEAGUE, season, day, home, away), day, LEAGUE, season, home, away, *score, neutral)
    return dict(zip(CANONICAL_COLUMNS, values)), rule


def validate_bindings():
    approval = read(PHASE / 'approval.json')
    for rel, digest in approval['phase3_inputs'].items():
        require(sha((BASE / 'phase3' / rel).read_bytes()) == digest, 'Approved Phase 3 input changed: ' + rel)
    frozen = read(BASE / 'phase3/input_freeze.final.json')
    for rel, desc in frozen['files'].items():
        raw = (ROOT / rel).read_bytes()
        require(sha(raw) == desc['sha256'] and len(raw) == desc['bytes'], 'Frozen execution input changed: ' + rel)
    manifest = read(BASE / 'phase3/artifact_manifest.final.json')
    # Manifest shapes are preserved, not rewritten for Phase 4.
    require(bool(manifest), 'Missing frozen artifact manifest')
    return approval


def build():
    approval = validate_bindings()
    registry = read(BASE / 'phase3/final/decision_registry.json')
    events = registry['fixture_events']; contexts = registry['additional_nonstanding_context_events']
    dispositions = Counter(e['disposition'] for e in events + contexts)
    require({k: dispositions[k] for k in approval['approved_totals']} == approval['approved_totals'] and len(events) == 6645 and len(contexts) == 3, 'Approved population differs')
    policy = read(PHASE / 'format_policy.json')
    observations = read(BASE / 'phase2/validated/source_inventory.json')['observations'] + read(BASE / 'phase3/final/supplemental_source_inventory.json')['observations']
    by_observation = {x.get('observation_id', x.get('source_observation_id')): x for x in observations}
    require(len(by_observation) == 12211, 'Observation identity collision')
    sources = {}
    for original in read(BASE / 'phase2/acquisition_manifest.json')['originals']:
        sources[original['sha256']] = original
    for original in read(BASE / 'phase3/acquisition_manifest.final.json')['originals']:
        sources[original['sha256']] = original
    records = []; audit = []; excluded = []
    stage_groups = defaultdict(list)
    for event in events:
        if event['disposition'] != 'INCLUDE':
            excluded.append(event); continue
        record, rule = project(event, policy)
        records.append(record)
        contributors = []
        for oid in event['observations']:
            observation = by_observation[oid]
            source = sources[observation['source_sha256']]
            contributors.append({'observation_id': oid, 'source': observation['source'], 'source_sha256': observation['source_sha256'],
                                 'url': source['url'], 'receipt_sha256': source['receipt_sha256'],
                                 'locator': {k: observation[k] for k in ('line', 'end_line', 'physical_line', 'physical_sha256', 'physical_json_line', 'json_pointer', 'decoded_line', 'decoded_end_line', 'decoded_wikitext_start', 'decoded_wikitext_end', 'template_sha256') if k in observation}})
        audit.append({'match_id': record['match_id'], 'canonical': record, 'outcome': event['outcome'], 'neutral_format_rule': rule,
                      'neutral_format_policy_sha256': sha((PHASE / 'format_policy.json').read_bytes()),
                      'frozen_phase3_registry_sha256': approval['phase3_inputs']['final/decision_registry.json'],
                      'approved_event': event, 'contributors': contributors})
        stage_groups[(event['season'], event['scope'], event['stage'])].append((record, rule))
    records.sort(key=lambda r: tuple(r[k] for k in ('league', 'season', 'date', 'home_team', 'away_team')))
    require(validate_canonical_records(records) == 6642, 'Output count differs')
    require(len({r['season'] for r in records}) == 34, 'Season count differs')
    positions = {r['match_id']: i + 2 for i, r in enumerate(records)}
    audit.sort(key=lambda a: positions[a['match_id']])
    for a in audit: a['csv_physical_line'] = positions[a['match_id']]
    coverage = []; stage_inventory = []
    for (season, scope, stage), pairs in sorted(stage_groups.items()):
        stage_inventory.append({'season': season, 'scope': scope, 'stage': stage, 'include': len(pairs),
                                'neutral_counts': dict(Counter('NA' if r['neutral_venue'] is None else str(r['neutral_venue']) for r, _ in pairs)),
                                'rules': dict(Counter(rule for _, rule in pairs)), 'evidence': policy['evidence_references']})
    for year in range(1992, 2026):
        season = f'{year}/{year+1}'; es = [e for e in events if e['season'] == season]; rs = [r for r in records if r['season'] == season]
        coverage.append({'season': season, 'main': sum(e['scope'] == 'MAIN' and e['disposition'] == 'INCLUDE' for e in es),
                         'qualifying': sum(e['scope'] == 'QUALIFYING' and e['disposition'] == 'INCLUDE' for e in es),
                         'include': len(rs), 'not_played': sum(e['disposition'] == 'NOT PLAYED' for e in es),
                         'neutral_counts': {str(v): sum(r['neutral_venue'] == v for r in rs) for v in (0, 1, None)}})
    summary = {'phase': 4, 'schema_version': 2, 'include': len(records), 'seasons': len(coverage), 'main': sum(x['main'] for x in coverage),
               'qualifying': sum(x['qualifying'] for x in coverage), 'dispositions': approval['approved_totals'],
               'neutral_counts': {str(v): sum(r['neutral_venue'] == v for r in records) for v in (0, 1, None)},
               'regulation_score_repairs': 8, 'football_date_repairs': 4,
               'administrative_exceptions': sum(a['approved_event']['result_basis'] != 'SUPPORTED_REGULATION' for a in audit),
               'source_observations': len(by_observation), 'recovered_qualifying_descriptions': 692,
               'recovered_qualifying_include': sum(a['approved_event']['population'] == 'RECOVERED_QUALIFYING' for a in audit),
               'limits': 'Historical upstream independence and downstream rights not established. Eight accepted administrative results remain explicit policy exceptions.'}
    return {NAME: serialize_csv(records, CANONICAL_COLUMNS), 'source_to_output.json': wire({'matches': audit}),
            'season_coverage.json': wire(coverage), 'season_stage_neutrality.json': wire(stage_inventory),
            'excluded_events.json': wire({'not_played': excluded, 'out_of_scope': contexts}), 'summary.json': wire(summary)}


def write(output):
    output = Path(output).resolve()
    require(not output.is_relative_to(ROOT) or output.is_relative_to(ROOT / 'data/private'), 'Detailed output must remain private')
    artifacts = build(); check_overwrite([output / k for k in artifacts]); output.mkdir(parents=True, exist_ok=True)
    for name, payload in artifacts.items():
        with (output / name).open('xb') as handle: handle.write(payload)
    return {k: {'sha256': sha(v), 'bytes': len(v)} for k, v in artifacts.items()}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument('--output', type=Path, default=PHASE / 'validated'); args = parser.parse_args()
    print(json.dumps(write(args.output), indent=2))
