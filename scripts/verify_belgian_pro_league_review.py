"""Belgian Phase 5: reproducible evidence assessment, never eligibility decisions.

Offline: consumes immutable Phase 4/recovery artifacts plus the private curated
phase5/evidence_inputs.json. Search leads are not promoted to inspected evidence.
No source selection, score/date changes, screened records or training API.
"""
from collections import Counter, defaultdict
from pathlib import Path
import argparse
import json
import os
import subprocess
import sys
import tempfile

from scripts import recover_belgian_2021_22 as recovery

ROOT, PRIVATE = recovery.ROOT, recovery.PRIVATE
encode, sha = recovery.encode, recovery.sha
NAMES = ('evidence_index.json', 'ordinary_samples.json', 'exception_assessments.json',
         'scheduling_contexts.json', 'review_registry.json', 'stage_identity_assessment.json')
ACCESS = {'PRIMARY_DIRECT', 'SECONDARY_DIRECT', 'SEARCH_INDEX_ONLY', 'INACCESSIBLE'}
STATUSES = {'FULL_CORE', 'PARTIAL', 'UNRESOLVED', 'CONTEXT_ONLY', 'CONTRADICTED'}
HEAD = '013bb9c195624d5ac290aeb57dae11c4e21c0b5a'


def load(path):
    return json.loads(path.read_text())


def protect(directory=PRIVATE):
    prior = recovery.protect(directory)
    frozen = load(directory / 'phase5_protected_before.json')
    for name, digest in frozen['files'].items():
        path = ROOT / name
        if not path.resolve().is_relative_to(ROOT.resolve()) or sha(path.read_bytes()) != digest:
            raise ValueError('Frozen Phase 5 input changed: ' + name)
    prefix = frozen['planning_log']
    if sha((ROOT / 'PLANNING_LOG.md').read_bytes()[:prefix['bytes']]) != prefix['sha256']:
        raise ValueError('Planning history changed')
    if subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip() != HEAD:
        raise ValueError('Unexpected HEAD')
    if subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT):
        raise ValueError('Index must remain empty')
    return dict(previous=prior, frozen_phase2_to_recovery_entries=len(frozen['files']))


def validate_evidence(evidence):
    for key, item in evidence.items():
        if item['id'] != key or item['access'] not in ACCESS:
            raise ValueError('Invalid evidence identity/access')
        if not item['url'].startswith('https://') or not item['supported_facts']:
            raise ValueError('Missing source URL/facts')
        for field in ('title', 'publisher', 'retrieved_date', 'independence', 'rights', 'document_kind'):
            if not item.get(field):
                raise ValueError('Missing evidence metadata: ' + field)


def validate_assessment(item, evidence):
    if item['status'] not in STATUSES:
        raise ValueError('Unknown review status')
    refs = item['evidence_ids']
    if any(key not in evidence for key in refs):
        raise ValueError('Dangling evidence reference')
    direct = [evidence[key] for key in refs if evidence[key]['access'].endswith('_DIRECT')]
    if item['status'] == 'FULL_CORE':
        if not direct or not item.get('facts_checked') == ['teams', 'date', 'score', 'competition']:
            raise ValueError('Full core facts require inspected evidence and explicit fact coverage')
        if all('independent upstream not established' in e['independence'] for e in direct):
            raise ValueError('Statistical database alone is not independent corroboration')
    if any(k in item for k in ('eligible', 'disposition', 'standardized_date', 'canonical_team')):
        raise ValueError('Phase 6 decision field prohibited')


def select_samples(history, modern):
    """Earliest scored league meeting of the high-profile pair; not random sampling.

    2023/24 and 2024/25 historical regular prefixes are the independently validated
    first 240 directed pairs, not a retrospective claim that UNKNOWN stages were
    officially labelled. No global name mapping is produced.
    """
    samples = []
    for year in range(1995, 2026):
        season = f'{year}/{year + 1}'
        rows = [r for r in history if r['season'] == season]
        if year in (2023, 2024):
            rows = rows[:240]
        if year == 2025:
            rows = [r for r in modern['2025-26/be1.txt'] if r['stage'] == 'REGULAR_SEASON']
        labels = {'RSC Anderlecht', 'Club Brugge KV'} if year == 2025 else {'Anderlecht', 'Club Brugge'}
        candidates = [r for r in rows if r['FT'] is not None and {r['home'], r['away']} == labels]
        if not candidates:
            raise ValueError('No deterministic sample: ' + season)
        row = min(candidates, key=lambda r: (r['date'], r['home'], r['away'], r['source_line']))
        samples.append(dict(season=season, observation=row, year=year))
    return samples


def bind_cases(cases, rows, events):
    result = []
    for case in cases:
        copies = [r for r in rows if r['date'] == case['date']
                  and case['home'] in r['home'] and case['away'] in r['away']]
        doc = [e for e in events if e['comparison_date'] == case['date']
               and case['home'] in e['diagnostic_event_key'][4]
               and case['away'] in e['diagnostic_event_key'][5]]
        if not copies or any(r['FT'] != case['score'] for r in copies):
            raise ValueError('Case not bound to immutable expected observation: ' + case['id'])
        if case['date'] in ('2022-01-15', '2022-04-10', '2021-12-05', '2021-07-27', '2022-01-18') and len(doc) != 1:
            raise ValueError('Missing recovered documentary case')
        result.append(dict(case, source_bindings=copies, documentary_events=doc,
                           facts_checked=['teams', 'date', 'score', 'competition'] if case['status'] == 'FULL_CORE' else [],
                           no_processing_decision=True))
    if len(result) != 7 or len({c['id'] for c in result}) != 7:
        raise ValueError('Five awards and two continuations required')
    return result


def scheduling(structure, contexts, index):
    given = {(c['path'], str(c['round'])): c for c in contexts}
    if len(given) != len(contexts):
        raise ValueError('Duplicate scheduling context')
    result = []
    for path, source in sorted(structure['modern_sources'].items()):
        for wide in source['assessment']['wide_rounds']:
            key = (path, str(wide['round']))
            if key not in given:
                raise ValueError('Unreviewed scheduling context')
            item = given.pop(key)
            if item['status'] not in {'DOCUMENTED_CONTEXT', 'PARTIAL', 'UNRESOLVED'}:
                raise ValueError('Invalid context status')
            bindings = [index[sid] for sid in wide['source_ids']]
            if min(r['date'] for r in bindings) != wide['earliest'] or max(r['date'] for r in bindings) != wide['latest']:
                raise ValueError('Scheduling range no longer bound')
            late = [r for r in bindings if r['date'] == wide['latest']]
            result.append(dict(item, frozen_context=wide, source_bindings=bindings,
                               latest_date_fixtures=late, all_fixtures_individually_verified=False,
                               confirmed_date_error=False))
    if given or len(result) != 15:
        raise ValueError('Scheduling population differs')
    return result


def queue_review(queue, index, contexts, cases):
    case_by_id = defaultdict(list)
    for case in cases:
        for row in case['source_bindings']:
            case_by_id[row['audit_id']].append(case['id'])
    context_by_id = defaultdict(list)
    for item in contexts:
        for sid in item['frozen_context']['source_ids']:
            context_by_id[sid].append([item['path'], item['round']])
    result = []
    for item in queue['items']:
        ids = {r['audit_id'] for r in item['bindings']}
        if len(ids) != len(item['bindings']) or not ids:
            raise ValueError('Invalid queue bindings')
        for row in item['bindings']:
            # Documentary-only entries use a separate earlier RSSSF representation.
            if row['audit_id'] in index and row != index[row['audit_id']]:
                raise ValueError('Queue source binding differs')
        if any(not set(flag_ids) <= ids for flag_ids in item['categories'].values()):
            raise ValueError('Category not bound to queue observation')
        result.append(dict(item, review_status='CONTEXT_ONLY',
                           exception_assessment_ids=sorted({c for sid in ids for c in case_by_id[sid]}),
                           scheduling_contexts=sorted({tuple(c) for sid in ids for c in context_by_id[sid]}),
                           historical_certification=False, processing_decision=None))
    actual = Counter(category for item in result for category in item['categories'])
    if len(result) != 927 or dict(actual) != queue['category_counts']:
        raise ValueError('Queue membership changed')
    return result


def build(directory=PRIVATE):
    inputs = load(directory / 'phase5/evidence_inputs.json')
    evidence = inputs['evidence']
    validate_evidence(evidence)
    # Regenerate upstream assessments directly from their immutable originals.
    rebuilt = recovery.structural.build(directory)
    for name, obj in rebuilt.items():
        if encode(obj) != (directory / 'phase4' / name).read_bytes():
            raise ValueError('Upstream regeneration differs: ' + name)
    recovered = recovery.build(directory)
    for name, obj in recovered.items():
        if encode(obj) != (directory / 'recovery2021' / name).read_bytes():
            raise ValueError('Recovered evidence regeneration differs: ' + name)
    observed = rebuilt['source_observations.json']
    structure = rebuilt['structural_assessment.json']
    rows = observed['historical'] + [r for rs in observed['modern'].values() for r in rs]
    index = {r['audit_id']: r for r in rows}
    if len(index) != 10100:
        raise ValueError('Source identities not unique')
    samples = select_samples(observed['historical'], observed['modern'])
    full = {2004, 2005, 2006, 2007, 2008, 2009, 2012, 2014, 2016, 2017, 2018, 2021, 2022, 2025}
    partial = {1995, 2002, 2013}
    for sample in samples:
        y = sample['year']
        sample.update(status='FULL_CORE' if y in full else 'PARTIAL' if y in partial else 'UNRESOLVED',
                      evidence_ids=['sample_' + str(y)], search_performed=True,
                      search_scope='Targeted date, opposing clubs, score and Belgian league; not a season search',
                      facts_checked=['teams', 'date', 'score', 'competition'] if y in full else [],
                      completion='Ordinary completed game corroborated' if y in full else 'SOURCE_REPORTED_NOT_INDEPENDENTLY_CERTIFIED',
                      administrative_finality='No modification found; no exhaustive appeal search',
                      availability='Exact historical result-publication time not certified')
        validate_assessment(sample, evidence)
    events = recovered['event_registry.json']['events']
    cases = bind_cases(inputs['cases'], rows, events)
    for case in cases:
        validate_assessment(case, evidence)
    contexts = scheduling(structure, inputs['contexts'], index)
    for context in contexts:
        if any(key not in evidence for key in context['evidence_ids']):
            raise ValueError('Unbound context evidence')
    queue = queue_review(rebuilt['queue_verification.json'], index, contexts, cases)
    administrative = dict(
        lommel=dict(status='PARTIAL', evidence_ids=['lommel_uefa_march', 'lommel_uefa_april', 'lommel_may'],
                    finding='March28/April24 UEFA news still conditional; May10 fan report of removal/annulment. Primary final decision missing. Retained CSV272/17 is not a complete record of played matches.',
                    finality='UNRESOLVED', individual_absent_fixtures_certified=0),
        mouscron=dict(status='PARTIAL', evidence_ids=['mouscron', 'mouscron_catalogue'],
                      finding='Closure/exclusion context corroborated, original annulment decision and individual documentary slots not certified. Frozen snapshot remains210 retained +18 annulled numeric +2 annulled awards +10 n/p.',
                      finality='UNRESOLVED', individual_documentary_exceptions_certified=0),
        covid=dict(status='PARTIAL', evidence_ids=['covid_bca', 'covid_bas', 'covid_league'],
                   finding='Official record of May15 termination; later relegation appeals and revised next-season format. Eight scheduled March15 slots are source-marked cancelled, not played results; no per-fixture final disposition assigned.',
                   finality='Appeal context documented, not blanket finality',
                   source_bound_slots=rebuilt['exception_registry.json']['cancellations']),
        partial_2025=dict(status='UNRESOLVED', scored=121, unscored=119,
                          finding='Frozen snapshot incomplete; missing scores are not evidence of cancellations; later acquisition needs approval'))
    stage_identity = dict(
        stage_evidence_ids=['stages_2018', 'stages_2024', 'covid_league', 'antwerp_qualifier', 'antwerp_date'],
        findings=[
            '2018/19: CSV240 regular; TXT30 championship additions. Mixed-tier Europe playoffs require separate source and scope decision, not duplicate deletion.',
            'Misplaced2021-22 TXT is2020/21:306 regular+12 championship+12 Europe. Path preserved; no source relabelling.',
            '2021/22 RSSSF:306 regular+12 championship+12 Europe+2 cross-division events; two continuations are representations of single fixtures.',
            '2023/24 CSV312:240 regular+30 championship+29 Europe+12 playdown+1 qualifier. TXT adds Standard–Westerlo award, not duplicate or proved never-played solely from absence.',
            '2024/25 CSV312:240+30+30+12. TXT adds Antwerp–Charleroi May29,2025 1-2 qualifier; official match score corroborated, exact date currently also index-supported.',
            'Source order reversals are not automatic historical date errors. Repeated pairs across real stages are not automatic duplicates.'
        ],
        club_identity_notes=[
            dict(group='Club/Cercle Brugge', finding='Different simultaneous clubs; never collapse by city.', evidence_ids=['beerschot_resume', 'stages_2024']),
            dict(group='Beerschot', finding='Historical reorganizations and reused matricules require season-specific legal review; no global Germinal/Beerschot/Wilrijk alias.', evidence_ids=['beerschot_identity']),
            dict(group='RWDM/Molenbeek', finding='Historical continuity not independently resolved in this review; retain source labels and season bindings.', evidence_ids=[]),
            dict(group='Mouscron', finding='Excelsior and later similarly named clubs must remain distinct pending legal continuity evidence.', evidence_ids=['mouscron']),
            dict(group='KRC Genk', finding='1988 merger does not make Winterslag or Waterschei interchangeable with Genk historical fixtures.', evidence_ids=['genk_identity']),
            dict(group='Senior/reserve and bilingual labels', finding='No reserve promotion or city-only mapping. Existing comparison correspondences are diagnostic season/source-bound only.', evidence_ids=['covid_league'])],
        recommendations_for_phase6=['Decide regular and each top-flight playoff scope separately.',
                                   'Keep mixed-tier and cross-division ties separate pending explicit eligibility decision.',
                                   'Require individual administrative and completion date rules before chronology-sensitive use.',
                                   'Do not create global club aliases from score/date agreement.'],
        eligibility_decided=False, source_selection_decided=False)
    pdfs = []
    for receipt in sorted((directory / 'phase5/evidence').glob('*.receipt.json')):
        rec = load(receipt)
        raw = receipt.with_name(receipt.name.replace('.receipt.json', '.pdf')).read_bytes()
        if sha(raw) != rec['sha256'] or len(raw) != rec['bytes']:
            raise ValueError('Court PDF receipt differs')
        pdfs.append(rec)
    if len(pdfs) != 3:
        raise ValueError('Three inspected adjudicative snapshots required')
    population = dict(phase4_observations=len(rows), phase4_conditional_events=8698,
                      supplementary_descriptions=334, supplementary_events=len(events),
                      combined_representations=len(rows) + 334,
                      combined_conditional_events=8698 + len(events) - recovered['historical_comparison.json']['matched'],
                      early_rsssf_excluded_from_these_totals=True)
    return dict(zip(NAMES, [
        dict(evidence=evidence, court_pdf_receipts=pdfs, research_limits=inputs['research_limits'],
             evidence_access_counts=dict(Counter(e['access'] for e in evidence.values())), rights=inputs['rights']),
        dict(method='Earliest scored regular Anderlecht–Club Brugge meeting; date/home/away/line sort; high-profile convenience sample, not representative',
             samples=samples, counts=dict(Counter(s['status'] for s in samples)), searched=31, whole_season_certification=False),
        dict(fixtures=cases, counts=dict(Counter(c['status'] for c in cases)), administrative_seasons=administrative,
             union_minute_discrepancy='Primary referee82:04 versus RSSSF81: annotation discrepancy, no numerical result/date correction', no_dispositions=True),
        dict(contexts=contexts, counts=dict(Counter(c['status'] for c in contexts)),
             ordering_causes=structure['ordering_causes'], all_round_fixtures_certified=False),
        dict(items=queue, count=len(queue), categories=rebuilt['queue_verification.json']['category_counts'],
             population=population, historically_certified=False, ordinary_sample_overlap_with_queue=sum(any(s['observation']['audit_id'] in {r['audit_id'] for r in q['bindings']} for q in queue) for s in samples)),
        stage_identity]))


def generate(directory=PRIVATE, output=None):
    protect(directory)
    output = Path(output) if output else directory / 'phase5/review'
    artifacts = {name: encode(obj) for name, obj in build(directory).items()}
    inputs = [directory / 'phase5/evidence_inputs.json', directory / 'phase5_protected_before.json']
    inputs += sorted(p for p in (directory / 'phase5/evidence').iterdir() if p.is_file())
    artifacts['reproducibility.json'] = encode(dict(
        phase=5, inputs={str(p.relative_to(directory)): sha(p.read_bytes()) for p in inputs},
        artifacts={n: sha(raw) for n, raw in artifacts.items()}, source_data_modified=False,
        historical_certification=False, processing_decisions=False))
    for name, raw in artifacts.items():
        recovery.keep(output / name, raw)
    return {name: sha(raw) for name, raw in artifacts.items()}


def verify(directory=PRIVATE):
    with tempfile.TemporaryDirectory(prefix='belgium-phase5-regeneration-') as tmp:
        process = subprocess.run([sys.executable, '-B', '-m', 'scripts.verify_belgian_pro_league_review', '--output', tmp],
                                 cwd=ROOT, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'),
                                 capture_output=True, text=True, timeout=120)
        if process.returncode:
            raise ValueError(process.stdout + process.stderr)
        result = {}
        for name in (*NAMES, 'reproducibility.json'):
            saved, fresh = (directory / 'phase5/review' / name).read_bytes(), (Path(tmp) / name).read_bytes()
            if saved != fresh:
                raise ValueError('Regeneration differs: ' + name)
            result[name] = dict(sha256=sha(saved), bytes=len(saved), byte_identical=True)
    return dict(artifacts=result, protected=protect(directory))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    print(json.dumps(verify() if args.verify else generate(output=args.output), indent=2))
