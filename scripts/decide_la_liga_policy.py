"""Phase 6 only: approved exception/date policy and offline assessment metadata.

No standardized match output, corrections, acquisition or model integration.
Source-bound fixture IDs here are audit IDs, not shared-schema match IDs.
"""
import argparse
from collections import Counter
from copy import deepcopy
from datetime import date

from scripts.collect_la_liga_feasibility import ROOT, PRIVATE, sha
from scripts.validate_la_liga_feasibility import encode
from scripts import verify_la_liga_review as review

POLICY = 'phase6_decision_policy.json'
ASSESSMENT = 'phase6_policy_assessment.json'
SPECS = (
    ('LL6-01', 'X01', 'RETAIN', None, '2015-12-20', 10, 2),
    ('LL6-02', 'X04', 'RETAIN_APPEAL_NOTE', None, '2025-03-27', 3, 0),
    ('LL6-03', 'X02', 'COMPLETED_INTERRUPTED_MATCH', '2004-12-12', '2005-01-05', 2, 1),
    ('LL6-04', 'X03', 'COMPLETED_INTERRUPTED_MATCH', '2023-12-10', '2023-12-11', 1, 1),
    ('LL6-05', None, 'HOLD_OUT', None, None, 3, 0),
)


def day(value):
    if not isinstance(value, str) or date.fromisoformat(value).isoformat() != value:
        raise ValueError('Canonical ISO calendar date required; timestamps are not accepted')
    return date.fromisoformat(value)


def source_id(file, digest, line):
    if not isinstance(file, str) or not file or type(line) is not int or line < 1:
        raise ValueError('Invalid source identity')
    if not isinstance(digest, str) or len(digest) != 64 or any(c not in '0123456789abcdef' for c in digest):
        raise ValueError('Invalid source hash')
    return 'laliga:' + sha(encode(dict(file=file, sha256=digest, line=line)))


def known_strictly_before(availability_date, prediction_date):
    prediction = day(prediction_date)
    return availability_date is not None and day(availability_date) < prediction


def validate_case(case):
    spec = next((s for s in SPECS if s[0] == case['decision_id']), None)
    if spec is None or case['action'] != spec[2] or case['approved_source_score'] != list(spec[5:7]):
        raise ValueError('Unapproved decision action/score')
    expected_start = spec[3] if spec[2] == 'COMPLETED_INTERRUPTED_MATCH' else spec[4]
    if (case['original_kickoff_date'], case['completion_date'], case['effective_result_date']) != (expected_start,spec[4],spec[4]):
        raise ValueError('Approved kickoff/completion/effective date policy changed')
    original = case['original']
    expected_id = source_id(case['source_file'], case['source_sha256'], original['source_line'])
    if case['fixture_id'] != expected_id:
        raise ValueError('Decision source ID mismatch')
    if case['approval'] != 'USER_APPROVED_PHASE6' or not case['evidence_urls']:
        raise ValueError('Decision lacks approved evidence')
    if case['approved_source_score'] != [int(original['hg']), int(original['ag'])]:
        raise ValueError('Phase 6 cannot change a score')
    day(original['date'])
    action = case['action']
    if action == 'HOLD_OUT':
        if case['final_outcome_status'] != 'UNRESOLVED' or any(
                case[k] is not None for k in ('effective_result_date', 'completion_date', 'original_kickoff_date')):
            raise ValueError('Unresolved final result/date cannot be silently settled')
    elif action == 'COMPLETED_INTERRUPTED_MATCH':
        start, end = day(case['original_kickoff_date']), day(case['completion_date'])
        if start >= end or case['effective_result_date'] != case['completion_date']:
            raise ValueError('Interrupted match must use later completion date')
        if case['completion_date'] != original['date'] or case['final_outcome_status'] != 'VERIFIED_COMPLETED_RESULT':
            raise ValueError('Unapproved completion/source-date change')
    elif action in ('RETAIN', 'RETAIN_APPEAL_NOTE'):
        if case['effective_result_date'] != original['date'] or case['completion_date'] != original['date']:
            raise ValueError('Retained result date changed')
        if case['original_kickoff_date'] != original['date'] or case['final_outcome_status'] != 'VERIFIED_PLAYED_RESULT':
            raise ValueError('Retained fixture facts/status changed')
    else:
        raise ValueError('Unknown approved decision')


def _assess(fixture, case, *, technical_status, historical_status,
           identified_final_outcome_unresolved=False):
    """Eligibility assessment only. A new final-outcome conflict always holds out.

    A conflict is not a mere unverified sample or wide-round flag. Resolving one
    requires a new evidence-backed approved policy version; no runtime waiver.
    """
    if type(identified_final_outcome_unresolved) is not bool:
        raise ValueError('Explicit boolean final-outcome conflict state required')
    if technical_status not in ('STRUCTURAL_PASS', 'STRUCTURAL_FAIL'):
        raise ValueError('Unknown technical classification')
    if historical_status not in ('VERIFIED_FACTS', 'UNVERIFIED'):
        raise ValueError('Unknown historical classification')
    state = fixture.get('identified_final_outcome_status')
    if state not in ('NO_CONFLICT_IDENTIFIED', 'UNRESOLVED'):
        raise ValueError('Explicit identified-final-outcome state required')
    original = fixture['original']
    day(original['date'])
    unresolved = identified_final_outcome_unresolved or state == 'UNRESOLVED'
    effective = original['date']
    basis = 'SOURCE_DATE_PROXY_NOT_INDEPENDENTLY_CERTIFIED'
    start = end = None
    if case is not None:
        validate_case(case)
        if any(case[k] != fixture[k] for k in ('fixture_id', 'original', 'season', 'source_file', 'source_sha256')):
            raise ValueError('Decision attached to a different source fixture')
        unresolved = unresolved or case['action'] == 'HOLD_OUT'
        effective = case['effective_result_date']
        start, end = case['original_kickoff_date'], case['completion_date']
        basis = 'APPROVED_COMPLETION_DATE' if case['action'] == 'COMPLETED_INTERRUPTED_MATCH' else 'VERIFIED_SOURCE_DATE'
    if unresolved:
        effective = None
        basis = 'UNRESOLVED_FINAL_RESULT_OR_APPLICABLE_DATE'
    return dict(fixture_id=fixture['fixture_id'], source_date=original['date'],
                original_kickoff_date=start, completion_date=end,
                effective_result_date=effective, availability_basis=basis,
                technical_acceptance=technical_status, historical_verification=historical_status,
                final_outcome_status='UNRESOLVED' if unresolved else case['final_outcome_status'] if case else 'NO_CONFLICT_IDENTIFIED_NOT_CERTIFIED',
                exception_policy_screenable=technical_status == 'STRUCTURAL_PASS' and not unresolved,
                screening_status='HOLD_OUT' if unresolved else 'TECHNICAL_REJECTION' if technical_status != 'STRUCTURAL_PASS' else 'CANDIDATE_NOT_STANDARDIZED',
                model_training_suitability='NOT_CLEARED', licensing_clearance='UNRESOLVED')


def assess(fixture, policy, **classifications):
    """Required policy entry point: missing/changed exception registries fail closed."""
    cases = policy['cases']
    if policy['approval'] != 'USER_APPROVED_PHASE6' or len(cases) != 5:
        raise ValueError('Incomplete approved decision registry')
    if {c['decision_id']:c['action'] for c in cases} != {s[0]:s[2] for s in SPECS}:
        raise ValueError('Approved decision lost or reclassified')
    if len({c['fixture_id'] for c in cases}) != 5:
        raise ValueError('Duplicate decision fixture')
    for case in cases:
        validate_case(case)
    if set(policy['unresolved_final_outcome_ids']) != {c['fixture_id'] for c in cases if c['action'] == 'HOLD_OUT'}:
        raise ValueError('Unresolved final-outcome registry changed')
    case = next((c for c in cases if c['fixture_id'] == fixture['fixture_id']), None)
    return _assess(fixture, case, **classifications)


def training_allowed(assessment, prediction_date):
    """Separate eligibility/rights gates plus strictly-earlier result availability.

    No current La Liga assessment clears the model/rights gates. This is an
    offline policy guard for future callers, not application training logic.
    """
    temporal = known_strictly_before(assessment['effective_result_date'], prediction_date)
    return (assessment['exception_policy_screenable'] is True
            and assessment['final_outcome_status'] != 'UNRESOLVED'
            and assessment['model_training_suitability'] == 'CLEARED'
            and assessment['licensing_clearance'] == 'CLEARED' and temporal)


def check_append_only(prefixes, root=ROOT):
    for name, info in prefixes.items():
        path = root / name
        if not path.resolve().is_relative_to(root.resolve()):
            raise ValueError('History path escapes root')
        raw = path.read_bytes()
        if len(raw) < info['bytes'] or sha(raw[:info['bytes']]) != info['sha256']:
            raise ValueError('Existing documentation/log history changed: ' + name)


def preserve(directory=PRIVATE, root=ROOT):
    baseline = review.read_json(directory / 'phase6_protected_before.json')
    if len(baseline) != 497:
        raise ValueError('Phase 6 baseline scope changed')
    count = review.protect(baseline, root)
    prefixes = review.read_json(directory / 'phase6_history_prefixes.json')
    check_append_only(prefixes, root)
    snapshot = (directory / 'phase5_historical_review_document_snapshot.md').read_bytes()
    original = prefixes['docs/la-liga-historical-review.md']
    if len(snapshot) != original['bytes'] or sha(snapshot) != original['sha256']:
        raise ValueError('Frozen Phase 5 documentation snapshot changed')
    return count


def build(directory=PRIVATE, root=ROOT):
    protected = preserve(directory, root)
    p5_report = review.build(directory, root)
    if encode(p5_report) != (directory / review.OUTPUT).read_bytes():
        raise ValueError('Phase 5 evidence no longer reproduces')
    ledger = review.read_json(directory / review.LEDGER)
    rows = review.records(directory)
    cases = []
    for decision, sample, action, kickoff, completion, hg, ag in SPECS:
        if sample:
            chosen = [s for s in ledger['supplemental_fixtures'] if s['id'] == sample]
            if len(chosen) != 1:
                raise ValueError('Approved exceptional fixture lost')
            s = chosen[0]
            item = {k:deepcopy(s[k]) for k in ('season', 'original', 'source_file', 'source_sha256', 'evidence_urls')}
        else:
            matches = [(key, season, row) for key, (season, row) in rows.items()
                       if season == '2025/2026' and row['home'] == 'Rayo Vallecano' and row['away'] == 'Real Oviedo']
            if len(matches) != 1:
                raise ValueError('Rayo-Oviedo source fixture not uniquely identified')
            (file, line), season, row = matches[0]
            if file != 'openfootball/espana/2025-26/1-liga.txt' or line != 780 or row['date'] != '2026-03-04':
                raise ValueError('Rayo-Oviedo source binding changed')
            evidence = next(r['evidence_urls'] for r in ledger['rounds'] if r['id'] == 'S34')
            item = dict(season=season, original=deepcopy(row), source_file=file,
                        source_sha256=sha((directory/file).read_bytes()), evidence_urls=deepcopy(evidence))
        if [int(item['original']['hg']), int(item['original']['ag'])] != [hg, ag]:
            raise ValueError('Approved unchanged source score differs')
        item.update(decision_id=decision, phase5_fixture_claim=sample, action=action,
                    approval='USER_APPROVED_PHASE6', approved_source_score=[hg, ag],
                    original_kickoff_date=kickoff if action == 'COMPLETED_INTERRUPTED_MATCH' else completion,
                    completion_date=completion, effective_result_date=completion,
                    final_outcome_status='UNRESOLVED' if action == 'HOLD_OUT' else
                    'VERIFIED_COMPLETED_RESULT' if action == 'COMPLETED_INTERRUPTED_MATCH' else 'VERIFIED_PLAYED_RESULT')
        item['fixture_id'] = source_id(item['source_file'], item['source_sha256'], item['original']['source_line'])
        item['source_raw_line'] = (directory/item['source_file']).read_text(encoding='utf-8-sig').splitlines()[item['original']['source_line']-1]
        review.binding(item, rows, directory)
        validate_case(item)
        cases.append(item)
    if len({c['fixture_id'] for c in cases}) != 5:
        raise ValueError('Duplicate exceptional fixture')
    carry = dict(rounds=[dict(id=r['id'], season=r['original']['season'], round=r['original']['round'],
                             status=r['status'], frozen_case_sha256=sha(encode(r))) for r in ledger['rounds']],
                 unverified_samples=[dict(id=s['id'], season=s['season'], source_file=s['source_file'],
                                          source_line=s['original']['source_line'], status=s['status'])
                                     for s in ledger['samples'] if s['status'] == 'UNRESOLVED'],
                 diagnostic_outliers=52, outliers_without_individual_full_fact_certification=49,
                 source_ledger_sha256=sha((directory/review.LEDGER).read_bytes()))
    full_claims = {(s['source_file'],s['original']['source_line']) for s in ledger['samples']+ledger['supplemental_fixtures']}
    carry['diagnostic_fixture_refs'] = []
    for case in ledger['rounds']:
        season = case['original']['season']
        file = f'openfootball/espana/{season[:4]}-{season[-2:]}/1-liga.txt'
        digest = sha((directory/file).read_bytes())
        for row in case['original']['outside_densest_seven_day_cluster']:
            carry['diagnostic_fixture_refs'].append(dict(
                fixture_id=source_id(file,digest,row['source_line']),source_file=file,source_line=row['source_line'],
                season=season,round_case=case['id'],round_evidence_status=case['status'],
                individual_full_fact_claim=(file,row['source_line']) in full_claims))
    if len(carry['diagnostic_fixture_refs']) != 52 or sum(not r['individual_full_fact_claim'] for r in carry['diagnostic_fixture_refs']) != 49:
        raise ValueError('Outlier certification scope changed')
    if Counter(x['status'] for x in carry['rounds']) != {'EXPLAINED':23, 'PARTIAL':8, 'UNRESOLVED':3} or len(carry['unverified_samples']) != 8:
        raise ValueError('Frozen uncertainty classifications changed')
    policy = dict(phase=6, approval='USER_APPROVED_PHASE6', cases=cases, uncertainty=carry,
                  unresolved_final_outcome_ids=[c['fixture_id'] for c in cases if c['action']=='HOLD_OUT'],
                  standard_date_semantics='Calendar day final result became available; completed interrupted matches use completion day.',
                  ordinary_date_basis='Unchanged source playing date is a proxy, not independent availability certification.',
                  chronological_rule='Effective result date must be strictly earlier than prediction date; same-day results are unavailable.',
                  new_unresolved_outcome_rule='HOLD_OUT until a new explicit evidence-backed approved policy decision; no runtime waiver.',
                  scheduling_rule='Wide round span, partial explanation, or lack of individual verification alone never corrects/excludes a fixture.',
                  no_population_certification=True, model_training_clearance='NOT_CLEARED', licensing_clearance='UNRESOLVED',
                  standardized_output_generated=False, source_corrections_applied=0)
    case_ids = {c['fixture_id'] for c in cases}
    digests = {file:sha((directory/file).read_bytes()) for file in {file for file,_ in rows}}
    verified = {(s['source_file'],s['original']['source_line']) for s in ledger['samples']+ledger['supplemental_fixtures'] if s['status']=='VERIFIED'}
    decisions = Counter(); history = Counter(); actions = Counter(c['action'] for c in cases)
    case_assessments = []
    unverified_sample_keys = {(s['source_file'],s['original']['source_line']) for s in ledger['samples'] if s['status']=='UNRESOLVED'}
    outlier_keys = {(r['source_file'],r['source_line']) for r in carry['diagnostic_fixture_refs']}
    sample_screening = Counter(); outlier_screening = Counter()
    for (file,line),(season,row) in rows.items():
        digest = digests[file]
        item = dict(fixture_id=source_id(file,digest,line), season=season, original=row, source_file=file,
                    source_sha256=digest, identified_final_outcome_status='NO_CONFLICT_IDENTIFIED')
        result = assess(item, policy, technical_status='STRUCTURAL_PASS',
                        historical_status='VERIFIED_FACTS' if (file,line) in verified else 'UNVERIFIED')
        decisions[result['screening_status']] += 1
        history[result['historical_verification']] += 1
        if (file,line) in unverified_sample_keys:sample_screening[result['screening_status']] += 1
        if (file,line) in outlier_keys:outlier_screening[result['screening_status']] += 1
        if item['fixture_id'] in case_ids:case_assessments.append(result)
    if sum(decisions.values()) != 13844 or decisions['HOLD_OUT'] != 1:
        raise ValueError('Unexpected exception decision reconciliation')
    input_names = ['phase6_protected_before.json','phase6_history_prefixes.json', review.LEDGER, review.OUTPUT]
    report = dict(phase=6, original_fixtures=13844, protected_files=protected,
                  exceptional_decisions=5, action_counts=dict(actions), screening_policy_counts=dict(decisions),
                  historical_verification_counts=dict(history), exceptional_assessments=case_assessments,
                  unverified_sample_screening=dict(sample_screening), diagnostic_outlier_screening=dict(outlier_screening),
                  uncertainty_counts=dict(rounds=34,documented=23,partial=8,unresolved=3,outliers=52,not_individually_certified=49,unverified_samples=8),
                  model_training_cleared=0, licensing_cleared=0, standardized_rows_written=0,
                  policy_sha256=sha(encode(policy)),
                  input_sha256={n:sha((directory/n).read_bytes()) for n in input_names},
                  code_sha256={n:sha((root/n).read_bytes()) for n in
                               ['scripts/decide_la_liga_policy.py','tests/test_la_liga_policy.py']})
    return policy, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--write', action='store_true')
    args = parser.parse_args()
    values = build()
    outputs = [(PRIVATE/name, encode(value)) for name,value in zip((POLICY,ASSESSMENT),values)]
    # Verify every existing output before creating anything; never overwrite.
    for path, raw in outputs:
        if path.exists() and path.read_bytes() != raw:
            raise ValueError('Decision metadata differs: '+path.name)
        if args.check and not path.exists():
            raise ValueError('Missing decision metadata: '+path.name)
    if args.write:
        for path,raw in outputs:
            if not path.exists():
                with path.open('xb') as stream:
                    stream.write(raw)
    print(encode(values[1]).decode(),end='')


if __name__ == '__main__':
    main()
