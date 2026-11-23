"""Eredivisie Phase 5 evidence accounting. Never applies historical policy."""
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import subprocess
from scripts import validate_eredivisie_structure as structure

ROOT, PRIVATE, base = structure.ROOT, structure.PRIVATE, structure.c
BASELINE = 'phase5_protected_before.json'
OUTPUTS = ('phase5_fixture_registry.json', 'phase5_context_assessment.json',
           'phase5_confidence_summary.json', 'phase5_reference_index.json')
STATUSES = {'FULLY CORROBORATED', 'PARTIALLY CORROBORATED', 'CONTRADICTED', 'UNRESOLVED'}


def read(path):
    def unique(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('Duplicate JSON key: ' + key)
            result[key] = value
        return result
    return json.loads(path.read_text(), object_pairs_hook=unique)


def protect(directory=PRIVATE, root=ROOT):
    previous = structure.protect(directory, root)
    frozen = read(directory / BASELINE)
    if not frozen['files']:
        raise ValueError('Empty historical baseline')
    for name, digest in frozen['files'].items():
        path = root / name
        if not path.resolve().is_relative_to(root.resolve()) or base.sha(path.read_bytes()) != digest:
            raise ValueError('Frozen Phase 2–4 entry changed: ' + name)
    prefix = frozen['planning_log']
    if base.sha((root / 'PLANNING_LOG.md').read_bytes()[:prefix['bytes']]) != prefix['sha256']:
        raise ValueError('Planning prefix changed')
    if subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root).decode().strip() != frozen['head']:
        raise ValueError('HEAD changed')
    index = root / subprocess.check_output(['git', 'rev-parse', '--git-path', 'index'], cwd=root).decode().strip()
    if base.sha(index.read_bytes()) != frozen['index_sha256']:
        raise ValueError('Index changed')
    return dict(previous=previous, phase2_4_entries=len(frozen['files']))


def select(rows):
    result = []
    for year in range(1990, 2026):
        candidates = [r for r in rows if r['season'] == f'{year}/{year+1}'
                      and r['structural']['score_bearing'] and not r['structural']['flags']]
        if not candidates:
            raise ValueError('Missing ordinary sampling population')
        result.append(min(candidates, key=lambda r: (r['date'], r['home'], r['away'], r['source'])))
    return result


def validate_references(refs):
    result = {}
    for r in refs:
        if r['id'] in result or not r['url'].startswith('https://') or not r['finding']:
            raise ValueError('Invalid/duplicate reference')
        if r['access'] not in {'DIRECT', 'INDEX_ONLY', 'DIRECT_TITLE_DATE_ONLY', 'DIRECT_MAINTENANCE'}:
            raise ValueError('Unknown access classification')
        for key in ('title', 'organization', 'author', 'publication_date', 'retrieval_date', 'independence', 'rights'):
            if key not in r:
                raise ValueError('Missing reference metadata: ' + key)
        result[r['id']] = r
    return result


def validate_review(review, references):
    if review['status'] not in STATUSES or not review['evidence_ids']:
        raise ValueError('Invalid evidence assessment')
    if any(x not in references for x in review['evidence_ids']):
        raise ValueError('Unbound evidence reference')
    if review['corroborated_core_facts'] and not any(references[x]['access'] == 'DIRECT' for x in review['evidence_ids']):
        raise ValueError('Index cannot certify facts')
    if review['status'] == 'FULLY CORROBORATED' and not {'home', 'away', 'date', 'FT', 'competition_season_context'} <= set(review['corroborated_core_facts']):
        raise ValueError('Full core-fact claim lacks fields')
    if review['status'] == 'FULLY CORROBORATED' and not any(references[x]['access'] == 'DIRECT' for x in review['evidence_ids']):
        raise ValueError('Full claim requires direct inspection')


def groups(rows, overlaps):
    parent = {r['audit_id']: r['audit_id'] for r in rows}
    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x
    for overlap in overlaps:
        for pair in overlap['matches']:
            a, b = find(pair['historical_id']), find(pair['modern_id'])
            parent[max(a, b)] = min(a, b)
    return {key: find(key) for key in parent}


def build(directory=PRIVATE, root=ROOT):
    protected = protect(directory, root)
    regenerated = structure.build(directory, root)
    for name, obj in regenerated.items():
        if base.encode(obj) != (directory / name).read_bytes():
            raise ValueError('Phase 4 regeneration differs: ' + name)
    historical = regenerated[structure.NAMES[0]]
    modern = regenerated[structure.NAMES[1]]
    overlap = regenerated[structure.NAMES[2]]
    queue = regenerated[structure.NAMES[3]]
    rows = [r for r in historical['all_source_records'] if 1990 <= int(r['season'][:4]) <= 2024] + modern['records']
    lookup = {r['audit_id']: r for r in rows}
    if len(lookup) != len(rows):
        raise ValueError('Duplicate audit IDs')
    selected = select(rows)
    if selected != read(directory / 'phase5_sample_selection.json')['samples']:
        raise ValueError('Saved deterministic sample differs')
    refs = validate_references(read(directory / 'phase5_evidence_inventory.json')['references'])
    inputs = read(directory / 'phase5_research_inputs.json')
    if inputs['policy'] != 'NO_PHASE6_DECISIONS':
        raise ValueError('Wrong phase')
    sample_reviews = inputs['sample_reviews']
    if len(sample_reviews) != 36 or {r['audit_id'] for r in sample_reviews} != {r['audit_id'] for r in selected}:
        raise ValueError('Missing or duplicated season sample')
    memberships = {r['original']['audit_id']: r['assessment']['flags'] for r in queue['records']}
    for r in queue['records']:
        key = r['original']['audit_id']
        if {k: v for k, v in lookup[key].items() if k != 'structural'} != r['original'] or lookup[key]['structural']['flags'] != memberships[key]:
            raise ValueError('Queue binding/category mismatch')
    diagnostic_groups = groups(rows, overlap['overlaps'])
    reviews = {}
    for review in sample_reviews:
        validate_review(review, refs)
        reviews[review['audit_id']] = deepcopy(review)
    for case in inputs['special_cases']:
        bound = [r for r in rows if r['season'] == case['season'] and r['home'] in case['home_labels'] and r['away'] in case['away_labels']]
        if not bound or len(bound) != case['expected_source_observations']:
            raise ValueError('Special-case binding mismatch: ' + case['id'])
        for r in bound:
            evidence = case['review']
            validate_review(evidence, refs)
            assessment = deepcopy(evidence)
            assessment.update(audit_id=r['audit_id'], case_id=case['id'], chronology=deepcopy(case['chronology']))
            if case['id'] == 'NEC_VITESSE' and r['FT'] != case['evidence_score']:
                assessment.update(status='CONTRADICTED', contradicted_facts=['FT'])
            if case['id'] == 'NAC_HEERENVEEN':
                assessment.update(status='PARTIALLY CORROBORATED', contradicted_facts=['Source cancellation is inconsistent with directly reported completion; null remains null'])
            reviews[r['audit_id']] = assessment
    wide = []
    reversals = []
    for season in modern['seasons']:
        for context in season['wide_rounds']:
            key = season['season'] + ':round:' + str(context['round'])
            if key not in inputs['wide_reviews']:
                raise ValueError('Unreviewed wide context: ' + key)
            review = inputs['wide_reviews'][key]
            validate_review(review, refs)
            wide.append(dict(id=key, season=season['season'], source_context=deepcopy(context), **deepcopy(review)))
        for i, context in enumerate(season['reversals'], 1):
            key = season['season'] + ':reversal:' + str(i)
            if key not in inputs['reversal_reviews']:
                raise ValueError('Unreviewed reversal context: ' + key)
            review = inputs['reversal_reviews'][key]
            validate_review(review, refs)
            reversals.append(dict(id=key, season=season['season'], source_context=deepcopy(context), endpoints=[deepcopy(lookup[context[k]]) for k in ('previous_id', 'current_id')], **deepcopy(review)))
    if len(wide) != len(inputs['wide_reviews']) or len(reversals) != len(inputs['reversal_reviews']):
        raise ValueError('Extra/unbound context review')
    selected_ids = set(memberships) | set(reviews)
    registry = []
    for key in sorted(selected_ids):
        r = lookup[key]
        contexts = [w for w in wide if key in w['source_context']['fixture_ids']] + [w for w in reversals if key in (w['source_context']['previous_id'], w['source_context']['current_id'])]
        review = deepcopy(reviews.get(key, dict(status='PARTIALLY CORROBORATED' if any(any(refs[e]['access'] == 'DIRECT' for e in w['evidence_ids']) for w in contexts) else 'UNRESOLVED', evidence_ids=sorted({e for w in contexts for e in w['evidence_ids']}), targeted_research=False, corroborated_core_facts=[], unresolved=['No direct full-fact individual certification; context is not fixture certification'])))
        if not review['evidence_ids'] and r['season'] == '2019/2020' and r['FT'] is None:
            review.update(evidence_ids=['T1', 'T2'], status='PARTIALLY CORROBORATED')
        registry.append(dict(original=deepcopy(r), conditional_fixture_group=diagnostic_groups[key], review_categories=memberships.get(key, []), context_ids=[x['id'] for x in contexts], assessment=review, processing_policy='NOT_DECIDED', effective_availability=None, training_permission='NOT_ESTABLISHED'))
    summary = dict(population=overlap['summary'], registry_source_observations=len(registry), registry_conditional_fixture_groups=len({x['conditional_fixture_group'] for x in registry}), flagged_source_observations=len(memberships), flagged_conditional_fixture_groups=len({diagnostic_groups[k] for k in memberships}), targeted_source_observations=len(reviews), targeted_conditional_fixture_groups=len({diagnostic_groups[k] for k in reviews}), context_only_source_observations=sum(not x['assessment']['targeted_research'] for x in registry), context_only_groups_without_targeted_review=len({x['conditional_fixture_group'] for x in registry}-{diagnostic_groups[k] for k in reviews}), source_observation_confidence=dict(Counter(x['assessment']['status'] for x in registry)), sample_confidence=dict(Counter(x['status'] for x in sample_reviews)), wide_context_confidence=dict(Counter(x['status'] for x in wide)), reversal_context_confidence=dict(Counter(x['status'] for x in reversals)), reference_access=dict(Counter(x['access'] for x in refs.values())), full_label_scope='Core teams/date/FT/competition-season context only; no exhaustive disciplinary finality, availability, rights or season certification', protected=protected)
    return {OUTPUTS[0]:dict(phase=5,records=registry,summary=summary), OUTPUTS[1]:dict(phase=5,wide_rounds=wide,reversals=reversals,cancellation=inputs['cancellation'],identities=inputs['identities'],outside_target='Both 1979/80 PEC Zwolle collision records preserved outside population'), OUTPUTS[2]:summary, OUTPUTS[3]:dict(references=list(refs.values()),bindings={e:sorted(x['original']['audit_id'] for x in registry if e in x['assessment']['evidence_ids']) for e in refs},input_hashes={name:base.sha((directory/name).read_bytes()) for name in ['phase5_evidence_inventory.json','phase5_research_inputs.json','phase5_sample_selection.json']})}


if __name__ == '__main__':
    for name, obj in build().items():
        raw = base.encode(obj)
        target = PRIVATE / name
        if target.exists():
            if target.read_bytes() != raw:
                raise ValueError('Historical assessment changed: ' + name)
        else:
            base.save(target, raw)
    print('Reproduced four Phase 5 evidence assessments; no processing policy applied.')
