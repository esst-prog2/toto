"""Offline Phase 5 evidence accounting; never corrections or certification.

Human-inspected documents are transcribed into the ignored ledger. These checks
validate bindings, scope and claim strength, not the truth of an internet page.
No network access, match export, eligibility decision or source mutation.
"""
import argparse
from collections import Counter
from datetime import date
import json
from pathlib import Path

from scripts import validate_segunda_structure as structural

ROOT, PRIVATE = structural.ROOT, structural.PRIVATE
base = structural.base
BASELINE = 'phase5_protected_before.json'
SELECTION = 'phase5_sample_selection.json'
LEDGER = 'phase5_historical_review.json'
OUTPUT = 'phase5_evidence_check.json'
MATRIX = 'phase5_review_matrix.json'
FACTS = {'date', 'home', 'away', 'FT'}
STATUSES = {'VERIFIED', 'PARTIAL', 'UNRESOLVED'}


def read(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('Duplicate JSON key: '+key)
            result[key] = value
        return result
    return json.loads(path.read_text(), object_pairs_hook=unique)


def protect(directory=PRIVATE, root=ROOT):
    previous = structural.protect(directory, root)
    frozen = read(directory/BASELINE)
    if not frozen['files']:
        raise ValueError('Empty historical-review baseline')
    for name, digest in frozen['files'].items():
        path = root/name
        if not path.resolve().is_relative_to(root.resolve()) or base.sha(path.read_bytes()) != digest:
            raise ValueError('Phase 5 protected file changed: '+name)
    prefix = frozen['planning_log']; log = (root/'PLANNING_LOG.md').read_bytes()
    if len(log) < prefix['bytes'] or base.sha(log[:prefix['bytes']]) != prefix['sha256']:
        raise ValueError('Planning history changed')
    return dict(previous=previous, phase2_4_files=len(frozen['files']))


def selection(records, flagged):
    chosen = []
    for year in range(2012, 2025):
        season = f'{year}/{year+1}'; band = (year-2012) % 3
        candidates = [r for r in records if r['season'] == season and
                      r['source_fixture_id'] not in flagged and
                      band*14+1 <= r['round'] <= band*14+14 and r['FT'] is not None]
        if not candidates:
            raise ValueError('Empty ordinary sample stratum: '+season)
        chosen.append(min(candidates, key=lambda r: base.sha(
            ('segunda-phase5-v1:'+r['source_fixture_id']).encode())))
    return chosen


def sources(items):
    indexed = {}
    for item in items:
        key = item['id']
        if key in indexed:
            raise ValueError('Duplicate evidence ID')
        if (not item['url'].startswith('https://') or not item['title'] or
                not item['publisher'] or not item['finding'] or not item['limitations']):
            raise ValueError('Incomplete evidence metadata')
        date.fromisoformat(item['reviewed_on'])
        if item['document_date'] is not None:
            date.fromisoformat(item['document_date'])
        if item['access'] not in {'DOCUMENT_OPENED', 'INDEX_ONLY'}:
            raise ValueError('Unknown evidence access')
        if item['independence'] not in {'PRIMARY_EVENT_RECORD', 'AUTHORED_CONTEMPORARY_REPORT',
                                        'PRIMARY_CLUB_HISTORY', 'SECONDARY_LEGAL_REPORT', 'UNKNOWN_UPSTREAM'}:
            raise ValueError('Unknown independence assessment')
        if not set(item['supports']).issubset(FACTS | {'scheduling', 'identity', 'administrative_context'}):
            raise ValueError('Unknown evidence capability')
        indexed[key] = item
    return indexed


def check_claim(claim, original, evidence):
    if claim['original'] != original or claim['source_fixture_id'] != original['source_fixture_id']:
        raise ValueError('Original fixture/identity binding changed')
    if (claim['status'] not in STATUSES or not claim['finding'] or
            not claim['limitations'] or not claim['confidence']):
        raise ValueError('Invalid review classification')
    if not claim['evidence'] or len(set(claim['evidence'])) != len(claim['evidence']):
        raise ValueError('Missing/duplicate claim evidence')
    for key in claim['evidence']:
        if key not in evidence:
            raise ValueError('Unknown claim evidence')
    facts = claim['independent_facts']; support = claim['fact_support']
    if set(facts) != set(support) or not set(facts).issubset(FACTS):
        raise ValueError('Unsupported independent facts')
    strong = set()
    for fact, value in facts.items():
        if not support[fact] or not set(support[fact]).issubset(claim['evidence']):
            raise ValueError('Fact evidence not bound to claim')
        if fact == 'date': date.fromisoformat(value)
        if fact == 'FT':
            values = value.split('-')
            if len(values) != 2 or any(not s.isdecimal() for s in values):
                raise ValueError('Invalid independently reported full-time score')
        if fact in {'home', 'away'} and not value:
            raise ValueError('Empty independently identified participant')
        docs = [evidence[key] for key in support[fact]]
        if any(fact not in d['supports'] for d in docs):
            raise ValueError('Scheduling/identity document cannot certify this fact')
        if any(d['access'] == 'DOCUMENT_OPENED' and d['independence'] in
               {'PRIMARY_EVENT_RECORD', 'AUTHORED_CONTEMPORARY_REPORT'} for d in docs):
            strong.add(fact)
    if claim['status'] == 'VERIFIED' and strong != FACTS:
        raise ValueError('Full-fact verification requires directly inspected independent evidence')
    if original['source_marked_awarded'] and claim['status'] == 'VERIFIED':
        raise ValueError('Administrative finality cannot be certified by a played-score comparison')
    if original['source_marked_awarded']:
        administrative = claim['administrative_review']
        if (claim['status'] != 'UNRESOLVED' or
                administrative['source_date_proxy'] != original['date'] or
                administrative['source_award'] != original['FT']):
            raise ValueError('Unresolved administrative source/decision binding changed')
        unknown = ('on_field_result', 'official_final_result', 'individual_award_decision_date',
                   'individual_publication_date', 'individual_appeal_finality_date',
                   'earliest_final_result_available')
        if any(administrative[k] is not None for k in unknown):
            raise ValueError('Unapproved administrative finality/availability assignment')
    chronology = claim['event_dates']
    for key, value in chronology.items():
        if value is not None: date.fromisoformat(value)
    if chronology['result_known_by'] is not None and chronology['actual_completion'] is not None:
        if chronology['result_known_by'] < chronology['actual_completion']:
            raise ValueError('Result availability precedes completion')
    if original['source_marked_awarded'] and any(chronology.get(k) is not None for k in
                                               ('result_known_by', 'actual_completion')):
        raise ValueError('Unapproved administrative chronology assignment')
    # This phase records evidence dates, never an effective standardized date.
    if claim['processing_decision'] != 'NONE_PHASE5':
        raise ValueError('Historical processing decision is outside Phase 5')
    return sorted(k for k in facts if original[k] is not None and original[k] != facts[k])


def assess(report, queue, selected, ledger):
    records = {r['source_fixture_id']: r for r in report['records']}
    if len(records) != len(report['records']): raise ValueError('Duplicate raw audit ID')
    flagged = {r['fixture']['source_fixture_id']: r for r in queue['records']}
    if len(flagged) != len(queue['records']): raise ValueError('Duplicate queue identity')
    if selected['records'] != selection(report['records'], set(flagged)):
        raise ValueError('Deterministic sample changed')
    sample_ids = {r['source_fixture_id'] for r in selected['records']}
    wanted = set(sample_ids)
    target_categories = {'MISSING_FULLTIME_SCORE', 'SOURCE_MARKED_ADMINISTRATIVE_AWARD',
                         'DIAGNOSTIC_DATE_OUTLIER', 'UNUSUAL_SCORE_REVIEW'}
    wanted.update(k for k, r in flagged.items() if target_categories.intersection(r['categories']))
    reversals = []
    by_line = {(r['season'], r['source_line']): r for r in records.values()}
    for season in report['seasons']:
        for v in season['validation']['source_order_reversals']:
            a = by_line[season['season'], v['previous_line']]; b = by_line[season['season'], v['line']]
            wanted.add(a['source_fixture_id'])
            reversals.append(dict(season=season['season'], previous_fixture=a['source_fixture_id'],
                                  next_fixture=b['source_fixture_id'], source_relation=v,
                                  conclusion='ROUND_GROUPED_STORAGE_NOT_CHRONOLOGICAL_SORT'))
    evidence = sources(ledger['sources']); claims = {}; discrepancies = []
    for c in ledger['fixtures']:
        key = c['source_fixture_id']
        if key in claims or key not in records: raise ValueError('Duplicate/unknown reviewed fixture')
        diffs = check_claim(c, records[key], evidence)
        if diffs and c['status'] == 'VERIFIED': discrepancies.append(dict(source_fixture_id=key, fields=diffs))
        claims[key] = c
    if set(claims) != wanted: raise ValueError('Target review coverage missing or extra')
    contexts = {(s['season'], s['round']): s for s in report['scheduling']}
    seen = set(); context_summary = Counter()
    for c in ledger['rounds']:
        key = (c['season'], c['round'])
        if key in seen or key not in contexts: raise ValueError('Duplicate/unknown scheduling context')
        seen.add(key); original = contexts[key]
        if c['original'] != original: raise ValueError('Scheduling evidence binding changed')
        if c['status'] not in {'DOCUMENTED', 'PARTIAL', 'UNRESOLVED'}:
            raise ValueError('Invalid scheduling status')
        ids = [by_line[key[0], n]['source_fixture_id'] for n in original['lines']]
        outliers = [by_line[key[0], n]['source_fixture_id'] for n in original['diagnostic_outlier_lines']]
        if c['fixture_ids'] != ids or c['outlier_ids'] != outliers:
            raise ValueError('Round fixture/outlier scope changed')
        for ev in c['evidence']:
            if ev not in evidence: raise ValueError('Unknown scheduling evidence')
        if not c['finding'] or not c['limitations']: raise ValueError('Missing scheduling limitations')
        if c['status'] == 'DOCUMENTED' and not all(any(
                evidence[e]['access'] == 'DOCUMENT_OPENED' and
                'scheduling' in evidence[e]['supports'] for e in claims[i]['evidence']) for i in outliers):
            raise ValueError('Documented round requires inspected context for every diagnostic outlier')
        context_summary[c['status']] += 1
    if seen != set(contexts): raise ValueError('Scheduling context omitted')
    groups = {}; reserve_ids = set()
    for g in ledger['identities']:
        label = g['source_label']
        if label in groups: raise ValueError('Duplicate reserve identity group')
        expected = sorted(k for k, r in records.items() if label in (r['home'], r['away']))
        if g['fixture_ids'] != expected or not expected: raise ValueError('Reserve observation binding changed')
        seasons = sorted({records[k]['season'] for k in expected})
        if g['seasons'] != seasons: raise ValueError('Reserve season pattern changed')
        if not g['keep_separate_from_parent'] or g['apply_mapping']:
            raise ValueError('Parent merge/global mapping outside Phase 5')
        if not g['evidence'] or any(e not in evidence for e in g['evidence']):
            raise ValueError('Missing reserve identity evidence')
        reserve_ids.update(expected); groups[label] = g
    if set(groups) != structural.RESERVES: raise ValueError('Reserve label scope changed')
    by_season = {}
    for r in selected['records']:
        c = claims[r['source_fixture_id']]
        by_season[r['season']] = dict(source_fixture_id=r['source_fixture_id'], status=c['status'],
                                      year_basis=r['year_basis'])
    matrix = []
    for key in sorted(set(flagged) | set(claims)):
        matrix.append(dict(source_fixture_id=key, categories=flagged.get(key, {}).get('categories', []),
                           fixture_review_status=claims[key]['status'] if key in claims else 'NOT_INDIVIDUALLY_REVIEWED',
                           identity_group_review=key in reserve_ids,
                           round_context_review=any(key in c['fixture_ids'] for c in ledger['rounds'])))
    counts = dict(Counter(c['status'] for c in claims.values()))
    return dict(scope='PHASE5_EVIDENCE_ONLY_NOT_HISTORICAL_CERTIFICATION',
                original_observations=len(records), original_queue=len(flagged), individually_reviewed=len(claims),
                fixture_status_counts=counts, sample_by_season=by_season,
                sample_status_counts=dict(Counter(claims[i]['status'] for i in sample_ids)),
                scheduling_context_status_counts=dict(context_summary), source_order_reversals=reversals,
                grouped_reserve_observations=len(reserve_ids), grouped_reserve_labels=len(groups),
                confirmed_source_discrepancies=discrepancies,
                missing_original_scores=sum(r['FT'] is None for r in records.values()),
                unresolved_administrative_awards=sum(r['source_marked_awarded'] for r in records.values()),
                matrix_observations=len(matrix), model_training_clearance='NOT_ESTABLISHED',
                rights='Historical corroboration grants no redistribution or model-training permission'), matrix


def build(directory=PRIVATE, root=ROOT):
    protection = protect(directory, root)
    report = read(directory/structural.REPORT); queue = read(directory/structural.QUEUE)
    # Reparse each pinned original, including physical line hashes, independently
    # of the human ledger before using saved Phase 4 identities.
    for s in report['seasons']:
        raw = (directory/s['source_file']).read_bytes()
        if base.sha(raw) != s['source_sha256']: raise ValueError('Pinned source changed')
        fresh = structural.parse_source(raw, int(s['season'][:4]))[0]
        old = [r for r in report['records'] if r['season'] == s['season']]
        if len(fresh) != len(old) or any(any(r[k] != o[k] for k in r) for r, o in zip(fresh, old)):
            raise ValueError('Fresh source/Phase 4 record disagreement')
    ledger = read(directory/LEDGER)
    result, matrix = assess(report, queue, read(directory/SELECTION), ledger)
    result.update(preservation=protection, input_sha256={n: base.sha((directory/n).read_bytes()) for n in
                  (structural.REPORT, structural.QUEUE, LEDGER, SELECTION, BASELINE)})
    return {OUTPUT: base.encode(result), MATRIX: base.encode(dict(warning='Group/context review is not fixture certification', records=matrix))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, default=PRIVATE)
    parser.add_argument('--output-directory', type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args(); outputs = build(args.directory)
    target = args.output_directory or args.directory
    for name, raw in outputs.items():
        if args.check:
            if (target/name).read_bytes() != raw: raise ValueError('Saved evidence assessment differs: '+name)
        else:
            base.save(target/name, raw)
        print(name, base.sha(raw))


if __name__ == '__main__':
    main()
