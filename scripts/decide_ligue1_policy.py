"""Ligue 1 Phase 6: source-bound decisions, no match archive or CSV output.

Policy candidacy is distinct from independent historical certification and from
training permission. Future consumers must call the guarded public evaluator.
"""
import argparse
from collections import Counter
from copy import deepcopy
from datetime import date
from pathlib import Path
import re

from scripts import verify_ligue1_review as review

ROOT, PRIVATE, base = review.ROOT, review.PRIVATE, review.base
BASELINE = 'phase6_protected_before.json'
POLICY = 'phase6_decision_policy.json'
ASSESSMENT = 'phase6_policy_assessment.json'
PUBLIC = review.PUBLIC + ('scripts/verify_ligue1_review.py', 'tests/test_ligue1_review.py',
                          'docs/ligue-1-historical-review.md')
# Selector, action, effective date, documentary decision date. Original facts
# come from immutable bound evidence, never an inferred administrative score.
SPECS = (
    ('BASTIA_LYON', 'HOLD_OUT_ADMIN_SCORE', None, '2017-05-04'),
    ('NANTES_BASTIA', 'HOLD_OUT_ADMIN_SCORE', None, '2014-02-12'),
    ('MONTPELLIER_ASSE', 'HOLD_OUT_ADMIN_FINALITY', None, '2025-04-02'),
    ('NANTES_TOULOUSE_2026', 'HOLD_OUT_ADMIN_FINALITY', None, '2026-05-27'),
    ('NICE_OM', 'APPROVED_REPLAY', '2021-10-27', '2021-09-08'),
    ('MHSC_CLERMONT', 'APPROVED_REPLAY', '2023-11-29', '2023-10-25'),
    ('AUXERRE_LYON', 'HOLD_OUT_DATE_DISPUTE', None, None),
)
MATERIAL_FLAGS = {'ADMINISTRATIVE_RESULT_SEMANTICS', 'ADMINISTRATIVE_SCORE_CONFLICT',
                  'SOURCE_MARKED_ADMINISTRATIVE', 'POST_EVENT_RATIFICATION',
                  'INTERRUPTED_REPLAY', 'REPLAY_DATE_CONTEXT',
                  'CROSS_SOURCE_SCORE_OR_DATE_CONFLICT'}
KNOWN_FLAGS = MATERIAL_FLAGS | {'BREST_DUAL_LABEL_IDENTITY', 'CANCELLED_UNPLAYED_SLOT',
                               'DISTINCT_AJACCIO_CLUB_IDENTITY', 'SYSTEMATIC_SOURCE_LABEL_DEFECT',
                               'UNUSUAL_SCORE', 'WIDE_ROUND_SPAN'}
GAP_REVIEW = dict(review_date='2026-11-22', acquisition_performed=False,
    sources=[
        dict(url='https://www.lequipe.fr/Football/d1/saison-1994-1995/page-calendrier-resultats',
             title='Calendrier et résultats D1 1994-1995', access='INDEX_ONLY_DIRECT_CACHE_MISS',
             coverage='Index exposes 38th matchday with dated results, not proof of all 380 fixture dates',
             permission='No applicable open-data/model-training grant verified; request publisher permission and permitted acquisition method'),
        dict(url='https://www.rsssf.org/tablesf/fran95.html',title='France 1994/95',access='DIRECT',
             publication_or_update='2006-06-05',
             coverage='Inspected top-division section provides final standings, not the required complete dated 380-fixture regular-season record; cup records are different competitions',
             permission='Footer permits copying with RSSSF acknowledgement, reserves rights; no specific model-training clearance established'),
        dict(url='https://www.deux-zero.com/ligue-1/resultats/edition/1994-1995/journee/1150',
             title='1994/95 matchday archive candidate',access='DIRECT_FETCH_CACHE_MISS',
             coverage='Exact supplied page unavailable; earlier indexed one-club season page suggests explicit dates but does not prove complete 380-fixture accuracy',
             permission='Applicable automated acquisition, redistribution and model-training terms unverified; request owner-approved export or bounded access')],
    recommendation='Separately authorize permissions/owner inquiry first (no messages sent), then a small explicit-date sample from permitted publisher/archive access, then approve complete 380-fixture acquisition only after feasibility, date and rights checks. Do not treat RSSSF standings or nominal round dates as fixture evidence.',
    missing_2007='Seek original LFP 25 May 2007 result registration and FFF 12 June appeal text under separate approval before any supplemental scored row; existing court evidence establishes penalty winner/points, not numerical award')


def day(value):
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        raise ValueError('Canonical ISO date required')
    return date.fromisoformat(value)


def numeric_outcome(row):
    goals = []
    for key in ('hg', 'ag'):
        value = row[key]
        if not isinstance(value, str) or not re.fullmatch(r'0|[1-9]\d*', value):
            raise ValueError('Missing or invalid numeric goals')
        goals.append(int(value))
    if row['FT'] != f'{goals[0]}-{goals[1]}':
        raise ValueError('Full-time goals inconsistent with source score')
    return 'H' if goals[0] > goals[1] else 'A' if goals[0] < goals[1] else 'D'


def known_strictly_before(availability, prediction):
    prediction_day = day(prediction)
    return availability is not None and day(availability) < prediction_day


def training_allowed(assessment, prediction_date):
    """Offline consumer guard, not integrated application/training code.

    Ordinary source-date candidates are not automatically demonstrably available.
    Rights, model suitability and corroborated availability are separate gates.
    """
    temporal = known_strictly_before(assessment['effective_result_date'], prediction_date)
    return (assessment['status'] == 'CANDIDATE_NOT_STANDARDIZED'
            and assessment['material_conflict'] is False
            and assessment['availability_verified'] is True
            and assessment['model_training_suitability'] == 'CLEARED'
            and assessment['licensing_clearance'] == 'CLEARED' and temporal)


def initialize(directory=PRIVATE, root=ROOT):
    if (directory / BASELINE).exists():
        return preserve(directory, root)
    review.protect(directory, root)
    final = review.read(directory / 'phase5_final_verification.json')
    for name, item in final['new_private_files_before_this_receipt'].items():
        if base.sha((directory / name).read_bytes()) != item['sha256']:
            raise ValueError('Approved Phase 5 artifact changed: ' + name)
    for name, digest in final['public_files'].items():
        if base.sha((root / name).read_bytes()) != digest:
            raise ValueError('Approved Phase 5 public artifact changed: ' + name)
    files = {str(p.relative_to(root)): base.sha(p.read_bytes())
             for p in directory.rglob('*') if p.is_file()}
    files.update({name: base.sha((root / name).read_bytes()) for name in PUBLIC})
    log = (root / 'PLANNING_LOG.md').read_bytes()
    base.save(directory / BASELINE, base.encode(dict(files=files,
              planning_log=dict(bytes=len(log), sha256=base.sha(log)))))
    return preserve(directory, root)


def preserve(directory=PRIVATE, root=ROOT):
    previous = review.protect(directory, root)
    baseline = review.read(directory / BASELINE)
    if not baseline['files']:
        raise ValueError('Empty Phase 6 baseline')
    for name, digest in baseline['files'].items():
        path = root / name
        if not path.resolve().is_relative_to(root.resolve()) or base.sha(path.read_bytes()) != digest:
            raise ValueError('Frozen Phase 2–5 artifact changed: ' + name)
    log = (root / 'PLANNING_LOG.md').read_bytes(); prefix = baseline['planning_log']
    if len(log) < prefix['bytes'] or base.sha(log[:prefix['bytes']]) != prefix['sha256']:
        raise ValueError('Planning history changed')
    return dict(previous=previous, phase2_5_entries=len(baseline['files']))


def binding(row):
    # Policy also binds numerical/auxiliary fields and risk flags, so a caller
    # cannot remove an administrative marker or silently replace a source label.
    return dict(review.binding(row), hg=row['hg'], ag=row['ag'], annotation=row['annotation'],
                source_result=row['assessment']['source_result'],
                flags=sorted(row['assessment']['flags']))


def index_records(records):
    result = {r['audit_id']: r for r in records}
    if len(result) != len(records):
        raise ValueError('Duplicate source observation ID')
    for r in records:
        if r['audit_id'] != review.structural.source_id(r['source'], r['source_sha256'], r['source_line']):
            raise ValueError('Invalid immutable source ID')
        if not set(r['assessment']['flags']) <= KNOWN_FLAGS:
            raise ValueError('New review flag requires explicit policy review')
    return result


def make_policy(report, ledger, review_result):
    records = index_records(report['records'])
    evidence = {e['id']: e for e in ledger['evidence']}
    if len(evidence) != len(ledger['evidence']):
        raise ValueError('Duplicate evidence ID')
    if not {'COVID','BREST-BNF','L00','S01','S09'} <= set(evidence):
        raise ValueError('Missing grouped interpretation evidence')
    entries = []; major = {c['case']: c for c in ledger['major_cases']}
    if len(major) != 6 or set(major) != {s[0] for s in SPECS[:-1]}:
        raise ValueError('Incomplete or ambiguous major-case registry')
    for name, action, effective, publication in SPECS:
        if name == 'AUXERRE_LYON':
            contradictions = review_result['contradictions']
            matching = [c for c in contradictions if c['field'] == 'date'
                        and c['source'] == '1996-10-26' and c['evidence'] == '1996-10-25']
            if len(matching) != 1 or len(contradictions) != 1:
                raise ValueError('New or ambiguous historical discrepancy requires explicit policy review')
            c = matching[0]; row = records[c['audit_id']]
            if (row['home'], row['away'], row['FT']) != ('AJ Auxerre', 'Olympique Lyon', '7-0'):
                raise ValueError('Auxerre discrepancy attached to different fixture')
            eids = [c['evidence_id']]
            chronology = dict(source_date=row['date'], scheduled_date=None, kickoff_date=None,
                              original_event_date=None, completion_date=None, replay_date=None,
                              original_kickoff_date=None, interruption_date=None,
                              disputed_playing_dates=['1996-10-25', '1996-10-26'])
            overlapping = []
        else:
            case = major[name]; row = records[case['audit_id']]
            if case['binding'] != review.binding(row):
                raise ValueError('Decision misbound to historical evidence')
            eids = case['evidence_ids']; old = case['chronology']
            chronology = dict(source_date=row['date'], scheduled_date=None,
                              kickoff_date=old.get('kickoff'), original_event_date=old.get('original_event'),
                              original_kickoff_date=old.get('original_event') or old.get('kickoff'),
                              interruption_date=(old.get('original_event') or old.get('kickoff')) if name!='NANTES_BASTIA' else None,
                              completion_date=effective, replay_date=old.get('replay'),
                              played_score_note=old.get('played_score'),
                              appeal_note=old.get('appeal'), judicial_decision=old.get('judicial_decision'))
            overlapping = deepcopy(case.get('overlapping_source_bindings', []))
        if not eids or any(e not in evidence for e in eids):
            raise ValueError('Missing cited decision evidence')
        if effective:
            day(effective)
            # Replay day must be a directly corroborated date and score, not a
            # schedule announcement or an index-only mention.
            direct = [evidence[e] for e in eids if evidence[e]['access'] == 'DIRECT'
                      and evidence[e]['independence'] in ('OFFICIAL_RECORD', 'INDEPENDENT_NARRATIVE')]
            if not any(e.get('facts', {}).get('date') == effective and
                       e.get('facts', {}).get('FT') == row['FT'] for e in direct):
                raise ValueError('Replay lacks directly verified completion date/score')
        entries.append(dict(decision_id=name, audit_id=row['audit_id'], original=binding(row),
                            action=action, effective_result_date=effective, chronology=chronology,
                            resolution_status='UNRESOLVED' if action.startswith('HOLD_OUT') else 'VERIFIED_REPLAY_RESULT',
                            administrative_publication_date=publication,
                            earliest_documented_admin_bound=publication if name in ('MONTPELLIER_ASSE', 'NANTES_TOULOUSE_2026') else None,
                            administrative_score=row['FT'] if name in ('MONTPELLIER_ASSE', 'NANTES_TOULOUSE_2026') else None,
                            awarded_winner='Olympique Lyonnais' if name == 'BASTIA_LYON' else 'SC Bastia' if name == 'NANTES_BASTIA' else None,
                            finality='NOT_EXHAUSTIVELY_ESTABLISHED', evidence_ids=list(eids),
                            administrative_finality_date=None,
                            evidence_urls=[evidence[e]['url'] for e in eids],
                            evidence_sha256=base.sha(base.encode([evidence[e] for e in eids])),
                            overlapping_source_bindings=overlapping))
    cancelled = [r for r in records.values()
                 if 'CANCELLED_UNPLAYED_SLOT' in r['assessment']['flags']]
    for row in cancelled:
        if row['season'] != '2019/2020' or any(row[k] is not None for k in ('FT', 'hg', 'ag')) or row['annotation'] != '[cancelled]':
            raise ValueError('Cancelled classification contradicts source')
        entries.append(dict(decision_id='NOT_PLAYED:' + row['audit_id'], audit_id=row['audit_id'],
                            original=binding(row), action='NOT_PLAYED', effective_result_date=None,
                            resolution_status='VERIFIED_NOT_PLAYED',
                            evidence_ids=['COVID'], evidence_urls=[evidence['COVID']['url']],
                            evidence_sha256=base.sha(base.encode(evidence['COVID']))))
    if len({e['audit_id'] for e in entries}) != len(entries):
        raise ValueError('Conflicting decisions for source observation')
    # Every materially flagged fixture requires an explicit decision. Long spans,
    # unusual scores and unverified samples alone do not meet this condition.
    covered = {e['audit_id'] for e in entries}
    if any(set(r['assessment']['flags']) & MATERIAL_FLAGS and r['audit_id'] not in covered
           for r in records.values()):
        raise ValueError('Material exception lacks required review decision')
    identities = {c['case']: c for c in ledger['identity_cases']}
    brest = identities['BREST_1990']; brest_ids = brest['affected_ids']
    actual_brest = [r for r in records.values() if r['season'] == '1990/1991'
                    and any(r[k] in ('Brest Armorique FC', 'Stade Brest') for k in ('home', 'away'))]
    if set(brest_ids) != {r['audit_id'] for r in actual_brest} or len(brest_ids) != 38:
        raise ValueError('Brest identity scope differs from evidence')
    if {r['audit_id'] for r in records.values() if 'BREST_DUAL_LABEL_IDENTITY' in r['assessment']['flags']} != set(brest_ids):
        raise ValueError('Brest identity risk outside approved scope')
    ajaccio_ids=set(identities['AJACCIO_2015']['affected_ids'])
    if ajaccio_ids != {r['audit_id'] for r in records.values() if 'DISTINCT_AJACCIO_CLUB_IDENTITY' in r['assessment']['flags']}:
        raise ValueError('Ajaccio identity risk differs from reviewed scope')
    for identifier in ajaccio_ids:
        r=records[identifier]
        if r['season']!='2015/2016' or r['source']!='openfootball/europe/france/2015-16_fr1.txt' or 'Gazélec FC Ajaccio' not in (r['home'],r['away']):
            raise ValueError('Ajaccio identity must retain exact modern entrant')
    identity_rule = dict(id='BREST_1990_ONLY', source=review.structural.metadata.HIST,
                         season='1990/1991', original_labels=['Brest Armorique FC', 'Stade Brest'],
                         candidate_label='Brest Armorique FC', evidence_ids=['BREST-BNF'],
                         evidence_url=evidence['BREST-BNF']['url'],
                         bindings=[binding(r) for r in sorted(actual_brest, key=lambda r:r['audit_id'])],
                         meaning='Same season sporting entrant only; no global legal-successor mapping')
    return dict(phase=6, authorization='USER_PHASE6_CONSERVATIVE_RULES',
                decisions=sorted(entries, key=lambda e:e['audit_id']),
                source_population_sha256=base.sha(base.encode(report['records'])),
                phase5_ledger_sha256=base.sha(base.encode(ledger)),
                phase5_assessment_sha256=base.sha(base.encode(review_result)),
                outcome_rule=dict(id='ACCEPTED_NUMERIC_GOALS_ONLY', source=review.structural.metadata.HIST,
                                  primary_label_defect_ids=sorted(r['audit_id'] for r in records.values()
                                    if 'SYSTEMATIC_SOURCE_LABEL_DEFECT' in r['assessment']['flags']),
                                  evidence_ids=['L00','S01','S09'],
                                  preserve_auxiliary=True, global_D_replacement=False,
                                  administrative_scores_are_not_ordinary=True),
                identity_rules=[identity_rule],
                uncertainty=dict(rounds=deepcopy(ledger['rounds']),
                                 individually_reviewed=deepcopy(review_result['fixtures']),
                                 identity_cases=deepcopy(ledger['identity_cases']),
                                 source_boundary_note='AC Ajaccio and Gazélec remain distinct; 38 unmatched pairs each side unchanged',
                                 additional_unreviewed_lead=deepcopy(ledger.get('additional_unreviewed_lead')),
                                 broader_date_candidates=deepcopy(ledger['broader_date_candidates'])),
                coverage=dict(target_seasons=36,represented_seasons=35,
                              missing_season='1994/1995',missing_season_expected=380,
                              missing_pairing=deepcopy(ledger['missing_fixture']),
                              gap_recovery=deepcopy(GAP_REVIEW)),
                temporal_rule='Verified result availability strictly before prediction date; no same-day use',
                licensing_clearance='UNRESOLVED', model_training_suitability='NOT_CLEARED')


def validate_policy(policy, report, ledger, review_result):
    expected = make_policy(report, ledger, review_result)
    if policy != expected:
        raise ValueError('Missing, altered or conflicting source-bound decision policy')
    return {e['audit_id']: e for e in policy['decisions']}


def _assess(row, decisions, identity_rule, historical, *, material_conflict=False):
    """Internal only: caller validates entire policy and population first."""
    if type(material_conflict) is not bool:
        raise ValueError('Explicit boolean material conflict required')
    day(row['date']); case = decisions.get(row['audit_id'])
    if case is not None and case['original'] != binding(row):
        raise ValueError('Decision attached to changed source observation')
    flags = set(row['assessment']['flags'])
    if flags & MATERIAL_FLAGS and case is None:
        raise ValueError('Material exception cannot pass without decision')
    action = case['action'] if case else 'ORDINARY_NUMERIC_RESULT'
    outcome = None; effective = None; availability = False; numeric = None
    if action == 'NOT_PLAYED':
        if any(row[k] is not None for k in ('FT','hg','ag')):
            raise ValueError('Not-played observation cannot contain result')
        status='NOT_PLAYED'; confidence='VERIFIED_NOT_PLAYED'
    elif action.startswith('HOLD_OUT') or material_conflict:
        status='HOLD_OUT'; confidence='MATERIAL_UNCERTAINTY'
        # Preserve but do not reinterpret an administrative numeric representation.
    else:
        numeric = numeric_outcome(row); outcome = numeric
        if row['assessment']['malformed_reasons']:
            raise ValueError('Structurally invalid result cannot become candidate')
        effective = case['effective_result_date'] if case else row['date']
        status='CANDIDATE_NOT_STANDARDIZED'
        availability=action=='APPROVED_REPLAY' or historical=='VERIFIED'
        confidence='INDEPENDENT_FULL_FACTS' if historical=='VERIFIED' else 'PARTIAL_EVIDENCE' if historical=='PARTIAL' else 'SOURCE_REPORTED_UNVERIFIED'
    canon = dict(home=row['home'],away=row['away'])
    if row['audit_id'] in {b['audit_id'] for b in identity_rule['bindings']}:
        if (row['source'],row['season']) != (identity_rule['source'],identity_rule['season']):
            raise ValueError('Identity rule cannot escape source/season')
        for k in canon:
            if canon[k] in identity_rule['original_labels']:
                canon[k] = identity_rule['candidate_label']
    return dict(audit_id=row['audit_id'],status=status,decision=action,
                historical_confidence=confidence,phase5_fact_status=historical,
                source_date=row['date'],effective_result_date=effective,
                availability_verified=availability,availability_basis='VERIFIED_REPLAY_DATE' if action=='APPROVED_REPLAY' else 'CORROBORATED_MATCH_DATE' if availability else 'SOURCE_REPORTED_DATE_NOT_INDEPENDENTLY_CERTIFIED' if effective else 'UNKNOWN_OR_NOT_APPLICABLE',
                material_conflict=material_conflict or action.startswith('HOLD_OUT'),
                candidate_outcome=outcome,candidate_identity=canon,
                licensing_clearance='UNRESOLVED',model_training_suitability='NOT_CLEARED')


def evaluate(policy, report, ledger, review_result, *, conflicts=()):
    """Public entry: fail closed on modified registry, records or new conflicts.

    These are minimal policy assessments, not standardized rows/audit archives.
    """
    decisions = validate_policy(policy, report, ledger, review_result)
    rows = index_records(report['records']); conflict_ids = set(conflicts)
    if not conflict_ids <= set(rows):
        raise ValueError('Unknown material-conflict fixture')
    hist = {f['audit_id']: f['status'] for f in review_result['fixtures']}
    return [_assess(r, decisions, policy['identity_rules'][0], hist.get(r['audit_id'],'UNREVIEWED'),
                    material_conflict=r['audit_id'] in conflict_ids)
            for r in sorted(rows.values(),key=lambda r:r['audit_id'])]


def build(directory=PRIVATE, root=ROOT):
    protection = preserve(directory, root)
    r5 = review.build(directory, root)
    if base.encode(r5) != (directory / review.OUTPUT).read_bytes():
        raise ValueError('Frozen Phase 5 assessment does not reproduce')
    report = review.read(directory / review.structural.REPORT)
    ledger = review.read(directory / review.LEDGER)
    policy = make_policy(report,ledger,r5)
    evaluations = evaluate(policy,report,ledger,r5)
    counts = Counter(e['status'] for e in evaluations)
    scored = sum(r['FT'] is not None for r in report['records'])
    cancelled = sum(e['action']=='NOT_PLAYED' for e in policy['decisions'])
    covid = [r for r in report['records'] if r['season']=='2019/2020']
    covid_counts = dict(scheduled=len(covid),played=sum(r['FT'] is not None for r in covid),
                       not_played=sum('CANCELLED_UNPLAYED_SLOT' in r['assessment']['flags'] for r in covid))
    if covid_counts != dict(scheduled=380,played=279,not_played=101):
        raise ValueError('Official curtailed-season reconciliation changed')
    if len(evaluations)!=len(report['records']) or sum(counts.values())!=len(evaluations):
        raise ValueError('Observation reconciliation failed')
    seasons={}
    byid=index_records(report['records'])
    for e in evaluations:
        seasons.setdefault(byid[e['audit_id']]['season'],Counter())[e['status']]+=1
    brest_season=[e['candidate_identity'] for e in evaluations
                 if byid[e['audit_id']]['season']=='1990/1991']
    clubs={t for e in brest_season for t in e.values()}
    pairings=Counter((e['home'],e['away']) for e in brest_season)
    if len(clubs)!=20 or pairings!=Counter({(a,b):1 for a in clubs for b in clubs if a!=b}):
        raise ValueError('Season-scoped Brest interpretation does not reconcile directed pairings')
    assessment=dict(phase=6,original_observations=len(evaluations),source_scored=scored,
                    source_unscored=len(evaluations)-scored,counts=dict(counts),
                    administrative_holdouts=sum(e['action'].startswith('HOLD_OUT_ADMIN') for e in policy['decisions']),
                    conditional_date_holdouts=sum(e['action']=='HOLD_OUT_DATE_DISPUTE' for e in policy['decisions']),
                    not_played=cancelled,definitive_other_exclusions=0,
                    explicit_decisions=len(policy['decisions']),action_counts=dict(Counter(e['action'] for e in policy['decisions'])),
                    covid_reconciliation=covid_counts,season_counts={k:dict(c) for k,c in sorted(seasons.items())},
                    outcome_counts=dict(Counter(e['candidate_outcome'] for e in evaluations if e['candidate_outcome'])),
                    confidence_counts=dict(Counter(e['historical_confidence'] for e in evaluations)),
                    identity_rule_fixture_count=len(policy['identity_rules'][0]['bindings']),
                    brest_season_identity_check=dict(clubs=len(clubs),directed_pairings=len(pairings),complete=True),
                    changed_candidate_identity_count=sum(e['candidate_identity']!={'home':byid[e['audit_id']]['home'],'away':byid[e['audit_id']]['away']} for e in evaluations),
                    uncertainty=dict(rounds=len(ledger['rounds']),round_counts=dict(Counter(w['status'] for w in ledger['rounds'])),
                                     affected_slots=len({a for w in ledger['rounds'] for a in w['affected_ids']}),
                                     primary_label_defects=len(policy['outcome_rule']['primary_label_defect_ids']),
                                     ordinary_counts=r5['ordinary_counts']),
                    protected=protection,policy_sha256=base.sha(base.encode(policy)),
                    exception_assessments=[e for e in evaluations if e['decision']!='ORDINARY_NUMERIC_RESULT'],
                    candidate_ids=[e['audit_id'] for e in evaluations if e['status']=='CANDIDATE_NOT_STANDARDIZED'],
                    complete_assessment_sha256=base.sha(base.encode(evaluations)),
                    standardized_rows_written=0,full_audit_archives_written=0,
                    training_cleared=0,licensing_cleared=0)
    return {POLICY:base.encode(policy),ASSESSMENT:base.encode(assessment)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--init',action='store_true');mode.add_argument('--write',action='store_true');mode.add_argument('--check',action='store_true')
    parser.add_argument('--output-directory',type=Path,default=PRIVATE);args=parser.parse_args()
    if args.init:
        print(initialize());return
    outputs=build();target=args.output_directory
    for name,raw in outputs.items():
        path=target/name
        if path.exists() and path.read_bytes()!=raw:raise ValueError('Existing policy output differs; no overwrite: '+name)
        if args.check and not path.exists():raise ValueError('Missing policy artifact: '+name)
    if args.write:
        for name,raw in outputs.items():
            if not (target/name).exists():base.save(target/name,raw)
    for name,raw in outputs.items():print(name,len(raw),base.sha(raw))


if __name__=='__main__':main()
