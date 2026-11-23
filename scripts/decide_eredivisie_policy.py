"""Phase 6: reproducible provisional policy registries, never final CSV output."""
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import date
import argparse
import re
import subprocess
from scripts import verify_eredivisie_review as review

ROOT, PRIVATE, base = review.ROOT, review.PRIVATE, review.base
BASELINE = 'phase6_protected_before.json'
NAMES = ('phase6_source_observation_policy.json', 'phase6_unique_fixture_policy.json',
         'phase6_source_selection_exceptions.json', 'phase6_chronology_registry.json',
         'phase6_policy_summary.json', 'phase6_policy_manifest.json')
DISPOSITIONS = {'COMPLETED_RESULT_CANDIDATE', 'HOLD_OUT', 'NOT_PLAYED'}
CASES = {
 'GRONINGEN_AJAX': ('2022/2023','2023-05-14','2023-05-16','2-3'),
 'NEC_VITESSE': ('2023/2024','2023-10-01','2023-10-01','1-3'),
 'NAC_HEERENVEEN': ('2025/2026','2026-05-10','2026-05-11','2-0'),
 'AJAX_FEYENOORD': ('2023/2024','2023-09-24','2023-09-27','0-4'),
 'RKC_AJAX': ('2023/2024','2023-09-30','2023-12-06','2-3'),
 'AZ_NEC': ('2023/2024','2023-10-29','2023-12-06','1-2'),
 'FEYENOORD_VVV': ('2018/2019','2018-11-04','2018-12-06','4-1'),
 'VITESSE_SPARTA': ('2021/2022','2022-03-04','2022-04-19','0-1'),
 'HERACLES_GRONINGEN': ('2024/2025','2024-12-21','2025-01-28','1-1'),
}
# Exact original IDs bind every exception. Neither names nor interruption keywords select policies.
CASE_IDS = {
 'GRONINGEN_AJAX': ('183183ef6dc77c37669df8a6a56254d89378f177cfe1f5e2d695678550a0c9f0','8bc80583915c0ad3aa346c90a1a44ae7f03d84510b5b726c966da50ef6556911'),
 'NEC_VITESSE': ('a6ddd7feb4bd0ad2c81a8c27adebebbd46286f3820674c8b1f8a989ab1a096f0','3e4671d6e5c5fd0e81edff3d9df7876d2355eca68d51a33b6d5b85b99fc78e34'),
 'NAC_HEERENVEEN': ('bb7fc1afcd2326f22517d72b9199902179e2d7d23d93247d37c6398e48e1e146',),
 'AJAX_FEYENOORD': ('f784990cb45eec18edc02c0e5af297f0c00e5a2708e3d33415dff1ec455c25d4','f7cc9a0d27b75f6bdcbd57b5212842a6963491cdf452bb58187e6391e137cc7b'),
 'RKC_AJAX': ('fbc534ca109380ca0983875ea9fe8abff146c0568c0cd7cbc9f9e03ccb80621e','9fdf8debd0281e86bec283f8a3eaf29afe0124bd4d761df826b853d0c0937b5a'),
 'AZ_NEC': ('0b0a2ccb3686ee56f5fac8b20ff783eb6357d1cbc486c037324064b237f4baa2','de72734b533e4af4be5d81571b46950367880393d11cb5b6944edbd9862f6197'),
 'FEYENOORD_VVV': ('998e8f9469a3dec44030e4962ccba82e8567b12b3c26c9c54d6fd268250868a3','2a3acfffc5e31539ab9643039019c21091dbdc6f19d18f7bccadfb29affc25ea'),
 'VITESSE_SPARTA': ('8bdefde4686df50b7ef108829a1bfdf974349f9ddc06ebc650ddfc1db07755ab','59f490046a90b465287328a20597ae11aabd80aafc90d5f7caf2d19464cc05bf'),
 'HERACLES_GRONINGEN': ('6bd8edcee19dae7a3d0119f66c558a945d506b721b9806b23b01912ee369d21b','b167d8a9c1422669ea6a6ae36ccbf7c41540463e567188aa4b6e3a47c410f2b4'),
}
KNOWN_FLAGS = {'CROSS_SOURCE_DATE_DISAGREEMENT','CROSS_SOURCE_SCORE_CONFLICT','CROSS_SOURCE_SCORE_DISAGREEMENT',
               'KNOWN_INTERRUPTION_CONTEXT','SOURCE_ANNOTATION','SOURCE_CANCELLED_BUT_COMPLETION_REPORTED',
               'SOURCE_ORDER_REVERSAL','SOURCE_UNSCORED','UNUSUAL_SCORE','WIDE_ROUND'}


def initialize(directory=PRIVATE, root=ROOT):
    if (directory / BASELINE).exists():
        return protect(directory, root)
    review.protect(directory, root)
    receipt = review.read(directory / 'phase5_final_verification.json')
    for name, item in receipt['private_files_before_receipt'].items():
        if base.sha((directory / name).read_bytes()) != item['sha256']:
            raise ValueError('Phase 5 private artifact changed: ' + name)
    for name, digest in receipt['public_files'].items():
        if base.sha((root / name).read_bytes()) != digest:
            raise ValueError('Phase 5 public artifact changed: ' + name)
    files = {str(p.relative_to(root)): base.sha(p.read_bytes()) for p in directory.rglob('*') if p.is_file()}
    files.update({n: h for n, h in receipt['public_files'].items() if n != 'PLANNING_LOG.md'})
    log = (root / 'PLANNING_LOG.md').read_bytes()
    base.save(directory / BASELINE, base.encode(dict(files=files, planning_log=dict(bytes=len(log),sha256=base.sha(log)))))
    return protect(directory, root)


def protect(directory=PRIVATE, root=ROOT):
    prior = review.protect(directory, root)
    saved = review.read(directory / BASELINE)
    if not saved['files']:
        raise ValueError('Empty policy baseline')
    for name, digest in saved['files'].items():
        p = root / name
        if not p.resolve().is_relative_to(root.resolve()) or base.sha(p.read_bytes()) != digest:
            raise ValueError('Frozen Phase 2–5 entry changed: ' + name)
    log = (root / 'PLANNING_LOG.md').read_bytes(); prefix = saved['planning_log']
    if len(log) < prefix['bytes'] or base.sha(log[:prefix['bytes']]) != prefix['sha256']:
        raise ValueError('Planning prefix changed')
    if subprocess.check_output(['git','branch','--show-current'],cwd=root).decode().strip() != 'feature/data-collection':
        raise ValueError('Wrong policy branch')
    return dict(previous=prior,phase2_5_entries=len(saved['files']))


def day(value):
    if not isinstance(value,str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}',value):
        raise ValueError('Canonical date required')
    return date.fromisoformat(value)


def binding(row):
    keys = ('audit_id','source','source_sha256','source_line','source_end_line','physical_record_sha256',
            'provenance','season','date','home','away','FT','hg','ag','annotation','stage','round')
    return {k:deepcopy(row[k]) for k in keys}


def primary(rows):
    if not rows or len({r['season'] for r in rows}) != 1:
        raise ValueError('Invalid fixture group')
    season = rows[0]['season']; historical = [r for r in rows if r['source'].startswith('jalapic/')]
    modern = [r for r in rows if r['source'].startswith('openfootball/')]
    if len(historical)+len(modern) != len(rows) or len(historical)>1 or len(modern)>1:
        raise ValueError('Ambiguous source representations')
    if season == '2025/2026':
        if historical or len(modern)!=1:
            raise ValueError('Unexpected latest-season sources')
        return modern[0], 'MODERN_2025_26_PRIMARY'
    if not 1990 <= int(season[:4]) <= 2024:
        raise ValueError('Outside approved target')
    if historical:
        return historical[0], 'HISTORICAL_CONTIGUOUS_BASELINE'
    if season=='2019/2020' and len(modern)==1 and modern[0]['FT'] is None:
        return modern[0], 'MODERN_EXPLICIT_UNPLAYED_SLOT'
    raise ValueError('Unapproved primary-source gap')


def supplement_assessment(fixture_id, *, identity=False, direct_result=False, traceable=False,
                          access_compatible=False, usage_compatible=False, immutable=False,
                          narrow=False, chronological=False, no_new_dataset=False):
    criteria = dict(identity=identity,direct_result=direct_result,traceable=traceable,
                    access_compatible=access_compatible,usage_compatible=usage_compatible,
                    immutable=immutable,narrow=narrow,chronological=chronological,no_new_dataset=no_new_dataset)
    return dict(approved=fixture_id==CASE_IDS['NAC_HEERENVEEN'][0] and all(x is True for x in criteria.values()),
                criteria=criteria,failed=[k for k,x in criteria.items() if x is not True])


def decide(rows, historical_reviews, case=None):
    """Pure policy over source-bound inputs; production build verifies original bytes and frozen evidence."""
    selected, selection = primary(rows)
    ids = sorted(r['audit_id'] for r in rows)
    if len(set(ids)) != len(ids):
        raise ValueError('Duplicate source identity')
    for row in rows:
        day(row['date'])
        if not row['structural']['structurally_valid'] or row['structural']['errors']:
            raise ValueError('Invalid structural observation')
        if set(row['structural']['flags']) - KNOWN_FLAGS:
            raise ValueError('Unknown review flag requires explicit policy')
        historical = historical_reviews.get(row['audit_id'])
        if historical is not None and historical['original'] != row:
            raise ValueError('Historical/source binding mismatch')
    matched_cases = [k for k, values in CASE_IDS.items() if set(ids)&set(values)]
    if len(matched_cases)>1:
        raise ValueError('Mixed exception identities')
    kind = matched_cases[0] if matched_cases else None
    if kind:
        if set(ids)!=set(CASE_IDS[kind]) or case is None or case['id']!=kind:
            raise ValueError('Missing/mismatched exact exception binding')
        y,kickoff,completion,score = CASES[kind]
        if selected['season']!=y or case['season']!=y or case['chronology']['original_kickoff']!=kickoff or case['chronology']['reported_completion']!=completion or case['evidence_score']!=score:
            raise ValueError('Approved exception chronology/value mismatch')
        for row in rows:
            if row['home'] not in case['home_labels'] or row['away'] not in case['away_labels']:
                raise ValueError('Exception participant mismatch')
            expected_date = kickoff if kind=='NAC_HEERENVEEN' or (kind=='GRONINGEN_AJAX' and row['audit_id']==CASE_IDS[kind][0]) else completion
            expected_score = None if kind=='NAC_HEERENVEEN' else '1-2' if kind=='NEC_VITESSE' and row['audit_id']==CASE_IDS[kind][1] else score
            if row['date']!=expected_date or row['FT']!=expected_score:
                raise ValueError('Source differs from approved exception result/date')
            if row['audit_id'] not in historical_reviews or historical_reviews[row['audit_id']]['assessment'].get('case_id')!=kind:
                raise ValueError('Missing frozen per-observation exception evidence')
    elif case is not None:
        raise ValueError('Unapproved exception')
    fixture_id = base.sha(base.encode(['Eredivisie',selected['season'],selected['home'],selected['away']]))
    decision_id = 'ERE-P6-' + fixture_id
    disposition = 'COMPLETED_RESULT_CANDIDATE'; policy = 'ORDINARY_SOURCE_CANDIDATE'
    reason = 'Structurally valid scored fixture; no material final-result contradiction identified. Historical and availability uncertainty retained.'
    approved = dict(date=selected['date'],home=selected['home'],away=selected['away'],FT=selected['FT'],hg=selected['hg'],ag=selected['ag'])
    chronology = dict(source_dates={r['audit_id']:r['date'] for r in rows},scheduled_date=None,actual_kickoff=None,
                      interruption_date=None,resumption_date=None,completion_date=None,reported_completion_date=None,administrative_publication_date=None,
                      administrative_finality_date=None,effective_result_availability_date=None,availability_day_verified=False,
                      intraday_order_verified=False,source_date_proxy=selected['date'],date_interpretation='ORDINARY_SOURCE_DATE_PROXY')
    eids = sorted({e for r in rows for e in historical_reviews.get(r['audit_id'],{}).get('assessment',{}).get('evidence_ids',[])})
    supplement = None; hold_type = None
    if kind:
        policy = kind; eids = sorted(set(eids)|set(case['review']['evidence_ids']))
        chronology.update(reported_completion_date=completion,actual_kickoff=kickoff,interruption_date=None if kind=='NEC_VITESSE' else kickoff,
                          completion_date=completion,resumption_date=None if kind=='NEC_VITESSE' else completion,
                          source_date_proxy=None,date_interpretation='APPROVED_COMPLETION_DAY')
        if kind == 'NAC_HEERENVEEN':
            supplement = supplement_assessment(ids[0],identity=True,direct_result=True,traceable=True,
                          access_compatible=True,usage_compatible=False,immutable=True,narrow=True,chronological=True,no_new_dataset=True)
            disposition='HOLD_OUT';hold_type='SUPPLEMENT_USAGE_PERMISSION_PENDING'
            reason='Direct historical 2-0/May11 corroboration exists, but applicable supplemental-value downstream usage permission remains unestablished. No supplemental result adopted.'
            chronology.update(date_interpretation='DOCUMENTED_COMPLETION_PENDING_SUPPLEMENT_POLICY')
        elif kind in {'FEYENOORD_VVV','VITESSE_SPARTA'}:
            disposition='HOLD_OUT';hold_type='MATERIAL_COMPLETION_EVIDENCE_PENDING'
            reason='Known interrupted event requires defensible actual completion/result availability. Frozen scheduling notices/index leads do not directly establish the completed result/date; source agreement alone does not resolve that material exception.'
            chronology.update(completion_date=None,resumption_date=None,date_interpretation='REPORTED_COMPLETION_NOT_DIRECTLY_CERTIFIED')
        else:
            if selected['FT'] != score:
                raise ValueError('Selected score differs from approved exception result')
            if kind == 'NEC_VITESSE':
                if selected['FT']!='1-3':
                    raise ValueError('Corroborated historical score must be selected explicitly')
                reason='Direct club final record/narrative and contemporary reporting support 1-3; modern 1-2 retained as contradicted original, not another fixture.'
            elif kind == 'GRONINGEN_AJAX':
                approved['date']=completion
                reason='Explicit date interpretation: May14 interrupted kickoff and May16 completed 2-3; historical original date unchanged.'
            else:
                if selected['date']!=completion or selected['FT']!=score:
                    raise ValueError('Existing completion representation differs from approval')
                reason='Source already uses corroborated completion date/result; preserve initial interrupted event separately, no fictitious date correction.'
            chronology.update(effective_result_availability_date=completion,availability_day_verified=True)
    elif any(r['FT'] is None for r in rows):
        if selected['season']=='2019/2020' and len(rows)==1 and selected['annotation']=='[cancelled]' and selected['hg'] is None and selected['ag'] is None:
            disposition='NOT_PLAYED';policy='UNPLAYED_2019_20';reason='Explicit null-score cancellation slot in stopped season; historical absence is a distinct coverage fact.'
            eids=['T1','T2','T3'];chronology.update(scheduled_date=selected['date'],source_date_proxy=None,date_interpretation='SOURCE_SCHEDULE_ONLY_NOT_PLAYED')
        else:
            disposition='HOLD_OUT';hold_type='UNRESOLVED_INCOMPLETE_RESULT';policy='UNKNOWN_NULL_RESULT'
            reason='Incomplete result has no approved cancellation or supplemental-result decision.'
    elif len({r['FT'] for r in rows})>1 or len({r['date'] for r in rows})>1:
        disposition='HOLD_OUT';hold_type='UNRESOLVED_MATERIAL_CONTRADICTION';policy='UNRESOLVED_SOURCE_CONFLICT'
        reason='Unresolved score/date conflict cannot silently become a candidate.'
    elif any(historical_reviews.get(r['audit_id'],{}).get('assessment',{}).get('status')=='CONTRADICTED' for r in rows):
        disposition='HOLD_OUT';hold_type='UNRESOLVED_MATERIAL_CONTRADICTION';policy='UNRESOLVED_HISTORICAL_CONTRADICTION'
    if disposition=='COMPLETED_RESULT_CANDIDATE':
        if approved['FT'] is None or not all(isinstance(approved[k],str) and re.fullmatch(r'0|[1-9][0-9]*',approved[k]) for k in ('hg','ag')) or approved['FT']!=f"{approved['hg']}-{approved['ag']}":
            raise ValueError('Invalid completed-result score')
    return dict(fixture_id=fixture_id,decision_id=decision_id,league='Eredivisie',season=selected['season'],
                source_observation_ids=ids,selected_source_id=selected['audit_id'],selection_reason=selection,
                disposition=disposition,hold_type=hold_type,policy=policy,reason=reason,
                approved_values=approved if disposition=='COMPLETED_RESULT_CANDIDATE' else None,
                documentary_values=None if case is None else dict(kickoff=kickoff,completion=completion,FT=score),
                chronology=chronology,evidence_ids=eids,supplement_assessment=supplement,
                historical_confidence={r['audit_id']:historical_reviews.get(r['audit_id'],{}).get('assessment',{}).get('status','NOT_IN_BOUNDED_REVIEW') for r in rows},
                review_flags={r['audit_id']:deepcopy(r['structural']['flags']) for r in rows},
                historical_reviews={r['audit_id']:deepcopy(historical_reviews[r['audit_id']]['assessment']) for r in rows if r['audit_id'] in historical_reviews},
                identity_policy='SELECTED_LITERAL_LABELS; ONLY_FROZEN_SEASON_BOUND_OVERLAP_LINKS; NO_GLOBAL_ALIASES',
                structural_suitability='VALID_SOURCE_STRUCTURE',historical_certification='NOT_DATASET_WIDE',
                unresolved_administration=False,redistribution_permission='NOT_CLEARED',model_training_permission='NOT_CLEARED',
                consumer_requirement='Revalidate complete registry/source bindings; actual result availability strictly before prediction day; separate rights clearance required.')


def _eligible(expected, supplied, prediction_day):
    """Pure check; expected MUST come from a freshly integrity-verified registry."""
    if expected != supplied:
        raise ValueError('Altered/incomplete decision or source binding')
    cutoff=day(prediction_day);c=expected['chronology'];available=c['effective_result_availability_date'];completed=c['completion_date']
    return (expected['disposition']=='COMPLETED_RESULT_CANDIDATE' and expected['unresolved_administration'] is False
            and c['availability_day_verified'] is True and available is not None and completed is not None
            and day(completed)<=day(available)<cutoff)


def reconcile(rows, decisions):
    assigned=[x for d in decisions for x in d['source_observation_ids']]
    if len(assigned)!=len(rows) or len(set(assigned))!=len(assigned) or set(assigned)!={r['audit_id'] for r in rows}:
        raise ValueError('Source observations lost or assigned multiple times')
    if len({d['fixture_id'] for d in decisions})!=len(decisions) or any(d['disposition'] not in DISPOSITIONS for d in decisions):
        raise ValueError('Duplicate fixture/disposition or unknown status')
    return dict(source_observations=len(rows),unique_fixture_slots=len(decisions),overlapping_representations=len(rows)-len(decisions),dispositions=dict(Counter(d['disposition'] for d in decisions)))


def build(directory=PRIVATE, root=ROOT):
    protected=protect(directory,root)
    regenerated=review.build(directory,root)
    for name,obj in regenerated.items():
        if base.encode(obj)!=(directory/name).read_bytes():
            raise ValueError('Frozen Phase 5 assessment differs: '+name)
    structure=review.structure
    h=review.read(directory/structure.NAMES[0]);m=review.read(directory/structure.NAMES[1]);o=review.read(directory/structure.NAMES[2])
    rows=[r for r in h['all_source_records'] if 1990<=int(r['season'][:4])<=2024]+m['records']
    groups=review.groups(rows,o['overlaps']);members=defaultdict(list)
    for r in rows:members[groups[r['audit_id']]].append(r)
    historical={r['original']['audit_id']:r for r in regenerated[review.OUTPUTS[0]]['records']}
    inputs=review.read(directory/'phase5_research_inputs.json');cases={x['id']:x for x in inputs['special_cases']}
    if set(cases)!=set(CASES):raise ValueError('Unexpected exception inventory')
    refs={x['id']:x for x in review.read(directory/'phase5_evidence_inventory.json')['references']}
    decisions=[];source_records=[];exceptions=[];correspondences=[]
    for key,rs in sorted(members.items()):
        kinds=[k for k,ids in CASE_IDS.items() if set(ids)&{r['audit_id'] for r in rs}]
        if len(kinds)>1:raise ValueError('Multiple case policies')
        decision=decide(rs,historical,cases[kinds[0]] if kinds else None)
        if any(e not in refs for e in decision['evidence_ids']):raise ValueError('Unknown decision evidence')
        decisions.append(decision)
        for row in sorted(rs,key=lambda r:r['audit_id']):
            source_records.append(dict(original=binding(row),original_assessment=deepcopy(row['structural']),
                   fixture_id=decision['fixture_id'],decision_id=decision['decision_id'],
                   source_role='SELECTED' if row['audit_id']==decision['selected_source_id'] else 'NONSELECTED_OVERLAP_RETAINED',
                   disposition=decision['disposition'],policy=decision['policy'],
                   historical_review_reference=row['audit_id'] if row['audit_id'] in historical else None))
        if kinds:exceptions.append(deepcopy(decision))
        if len(rs)>1:correspondences.append(dict(fixture_id=decision['fixture_id'],source_ids=decision['source_observation_ids'],season=decision['season'],scope='EXACT_FROZEN_SCORED_PAIR_ONLY'))
    counts=reconcile(rows,decisions)
    summary=dict(phase=6,**counts,score_bearing_source_observations=sum(r['FT'] is not None for r in rows),
                 unscored_source_observations=sum(r['FT'] is None for r in rows),
                 historical_observations=sum(r['source'].startswith('jalapic/') for r in rows),modern_observations=sum(r['source'].startswith('openfootball/') for r in rows),
                 source_selected=sum(r['source_role']=='SELECTED' for r in source_records),phase4_flags=o['summary']['queue'],
                 phase5_review_observations=len(historical),source_selection=dict(Counter(d['selection_reason'] for d in decisions)),
                 hold_types=dict(Counter(d['hold_type'] for d in decisions if d['disposition']=='HOLD_OUT')),
                 administrative_hold_outs=0,supplemental_candidates=0,definitive_exclusions=0,
                 actual_completion_day_decisions=sum(d['chronology']['availability_day_verified'] for d in decisions),
                 season_dispositions={s:dict(Counter(d['disposition'] for d in decisions if d['season']==s)) for s in sorted({d['season'] for d in decisions})},
                 policy_outputs_not_final_standardization=True,protected=protected)
    source=dict(phase=6,records=source_records,warning='Processing metadata only; immutable originals remain in Phase2–5 evidence, not a final Phase7 archive')
    unique=dict(phase=6,records=sorted(decisions,key=lambda d:d['fixture_id']),summary=summary)
    selection=dict(phase=6,hierarchy='Historical primary 1990/91–2024/25; modern primary 2025/26 and sole explicit 74 unplayed 2019/20 slots; exact fixture exceptions only',
                   justification='Continuous historical coverage, complete ordinary pairings and coherent repeated labels avoid a new source boundary; 2068 scored comparisons reveal only the two explicitly reviewed conflicts. Modern has the known NEC score error and NAC incomplete snapshot. Neither is historically independent or rights-cleared; hierarchy asserts no blanket accuracy superiority.',
                   exceptions=exceptions,overlap_correspondences=correspondences,
                   season_diagnostic_correspondences={x['season']:next(old for old in review.read(directory/'phase3_overlap_registry.json')['overlaps'] if old['season']==x['season'])['conditional']['hypothesized_label_correspondences'] for x in o['overlaps']},
                   global_aliases=[],preserved_phase5_contexts=regenerated[review.OUTPUTS[1]],rights='Acquisition approval, historical accuracy, redistribution and training permissions remain separate; no downstream clearance')
    chronology=dict(phase=6,records=[dict(fixture_id=d['fixture_id'],decision_id=d['decision_id'],disposition=d['disposition'],chronology=d['chronology'],unresolved_administration=d['unresolved_administration']) for d in unique['records']],
                    rule='Known completion and availability days both strictly before prediction day; unknown information fails closed. CSV alone is not leakage-safe. Training independently blocked pending rights clearance.')
    outputs={NAMES[0]:source,NAMES[1]:unique,NAMES[2]:selection,NAMES[3]:chronology,NAMES[4]:summary}
    outputs[NAMES[5]]=dict(phase=6,files={name:dict(bytes=len(base.encode(obj)),sha256=base.sha(base.encode(obj))) for name,obj in outputs.items()},
                 input_hashes={name:base.sha((directory/name).read_bytes()) for name in [*structure.NAMES,*review.OUTPUTS,'phase5_evidence_inventory.json','phase5_research_inputs.json']},
                 summary=counts,private=True,no_csv_or_complete_audit_archive=True)
    return outputs


class PredictionGate:
    """Verified, detached expected decisions. Loading fails on any altered saved policy file."""
    def __init__(self,directory=PRIVATE,root=ROOT):
        outputs=build(directory,root)
        for name,obj in outputs.items():
            if not (directory/name).exists() or (directory/name).read_bytes()!=base.encode(obj):
                raise ValueError('Altered/missing policy registry: '+name)
        self._expected={d['fixture_id']:deepcopy(d) for d in outputs[NAMES[1]]['records']}

    def eligible_for_prediction(self,decision,prediction_day):
        key=decision.get('fixture_id')
        if key not in self._expected:raise ValueError('Unknown fixture decision')
        return _eligible(self._expected[key],decision,prediction_day)

    def training_allowed(self,decision,prediction_day):
        eligible=self.eligible_for_prediction(decision,prediction_day)
        return eligible and decision['model_training_permission']=='CLEARED'


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--init',action='store_true');args=parser.parse_args()
    if args.init:initialize()
    outputs=build()
    for name,obj in outputs.items():
        raw=base.encode(obj);target=PRIVATE/name
        if target.exists():
            if target.read_bytes()!=raw:raise ValueError('Policy output differs: '+name)
        else:base.save(target,raw)
    print(outputs[NAMES[4]]['dispositions'])
