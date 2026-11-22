"""Ligue 2 Phase 6: bound provisional decisions, never CSV standardization."""
from collections import Counter
from copy import deepcopy
from datetime import date
from pathlib import Path
import re
from scripts import verify_ligue2_review as review

ROOT, PRIVATE, base = review.ROOT, review.PRIVATE, review.base
BASELINE = 'phase6_protected_before.json'
REGISTRY = 'phase6_decision_registry.json'
EXCEPTIONS = 'phase6_exception_registry.json'
SUMMARY = 'phase6_policy_summary.json'
MANIFEST = 'phase6_policy_manifest.json'
SPECS = {
 '03db5c7de89bb16fb58f71ef939bcb1976e6cc0b66a9b14f7aae3a1d62571ede': ('NIORT_VALENCIENNES', '2020/2021', '2020-12-22', 'Chamois Niortais', 'Valenciennes FC', '0-3', None),
 'a56d48ae18688610ad53de15ee0cb1d89051919bbaac6403e0eedb0dffe494d9': ('BORDEAUX_RODEZ', '2022/2023', '2023-06-02', 'Girondins Bordeaux', 'Rodez AF', '0-1', '2023-06-12'),
 'afcb54cb3230a64b091b4980dedb16b65e9ac9df6228d2b3252c2f85b9506862': ('NANCY_QRM', '2021/2022', '2022-04-22', 'AS Nancy Lorraine', 'US Quevilly-Rouen', '0-3', '2022-05-04'),
 '7accac4a3b7315d4cfbb91cdcb14c73d66b81f779ac1bce0b5e88c565a1896d9': ('AJACCIO_BASTIA', '2024/2025', '2024-12-03', 'AC Ajaccio', 'SC Bastia', '0-0', None),
 '8601876bb734068cc797791701e774c074eded339984251b5ad9de686fb97ee7': ('VALENCIENNES_BEZIERS', '2018/2019', '2019-04-19', 'Valenciennes FC', 'AS Béziers', '5-6', None),
}
ADMIN = {k for k,v in SPECS.items() if v[0] in {'NIORT_VALENCIENNES','BORDEAUX_RODEZ','NANCY_QRM'}}
KNOWN_FLAGS = {'SOURCE_ORDER_DATE_REVERSAL','WIDE_ROUND','DIAGNOSTIC_DATE_OUTLIER','UNUSUAL_SCORE','SOURCE_CANCELLED','SOURCE_MARKED_AWARDED','BORDEAUX_RODEZ_ADMINISTRATIVE_REVIEW'}


def initialize(directory=PRIVATE, root=ROOT):
    if (directory/BASELINE).exists(): return protect(directory, root)
    review.protect(directory, root)
    receipt=review.read(directory/'phase5_final_verification.json')
    for name,item in receipt['private_files_before_receipt'].items():
        if base.sha((directory/name).read_bytes())!=item['sha256']: raise ValueError('Phase 5 artifact changed: '+name)
    for name,digest in receipt['public_files'].items():
        if base.sha((root/name).read_bytes())!=digest: raise ValueError('Phase 5 public file changed: '+name)
    files={str(p.relative_to(root)):base.sha(p.read_bytes()) for p in directory.rglob('*') if p.is_file()}
    files.update({n:h for n,h in receipt['public_files'].items() if n!='PLANNING_LOG.md'})
    log=(root/'PLANNING_LOG.md').read_bytes()
    base.save(directory/BASELINE,base.encode(dict(files=files,planning_log=dict(bytes=len(log),sha256=base.sha(log)))))
    return protect(directory, root)


def protect(directory=PRIVATE, root=ROOT):
    previous=review.protect(directory, root); frozen=review.read(directory/BASELINE)
    for name,digest in frozen['files'].items():
        if not (root/name).resolve().is_relative_to(root.resolve()) or base.sha((root/name).read_bytes())!=digest: raise ValueError('Frozen evidence changed: '+name)
    log=(root/'PLANNING_LOG.md').read_bytes();prefix=frozen['planning_log']
    if len(log)<prefix['bytes'] or base.sha(log[:prefix['bytes']])!=prefix['sha256']: raise ValueError('Planning history changed')
    return dict(previous=previous,phase2_5_entries=len(frozen['files']))


def day(value):
    if not isinstance(value,str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}',value): raise ValueError('Canonical date required')
    return date.fromisoformat(value)


def candidate_id(row):
    # Length-safe, cross-competition identity; no aliases or source-order inputs.
    return base.sha(base.encode(['Ligue 2',row['season'],row['date'],row['home'],row['away']]))


def decide(row, historical=None, case=None):
    """Pure interpretation of an immutable structural observation."""
    original=review.binding(row); flags=row['assessment']['flags']
    if not row['assessment']['structurally_valid'] or row['assessment']['errors']: raise ValueError('Invalid structural observation')
    if set(flags)-KNOWN_FLAGS: raise ValueError('Unreviewed structural flag')
    if historical is not None and historical['original']!=original: raise ValueError('Historical binding mismatch')
    if historical and historical['assessment']['classification']=='CONTRADICTED': raise ValueError('Contradiction requires explicit policy review')
    day(row['date'])
    decision='ORDINARY_SOURCE_CANDIDATE'; disposition='COMPLETED_RESULT_CANDIDATE'
    reason='Numeric regular-season observation; historical certification and availability remain separate'
    chronology=dict(source_round_heading_date=row['assessment']['chronology']['source_heading_date'],source_date=row['date'],scheduled_date=None,actual_kickoff_date=None,completion_date=None,administrative_publication_date=None,administrative_finality_date=None,effective_result_availability_date=None,date_interpretation='SOURCE_DATE_PROXY',availability_verified=False,proxy_date=row['date'])
    if row['audit_id'] in SPECS:
        spec=SPECS[row['audit_id']]
        if (row['season'],row['date'],row['home'],row['away'],row['FT'])!=spec[1:6]: raise ValueError('Exception selector mismatch')
        if case is None or case['original']!=original: raise ValueError('Missing bound exception evidence')
        decision=spec[0]
        if row['audit_id'] in ADMIN:
            disposition='ADMINISTRATIVE_HOLD_OUT';reason='Numerical homologation, finality or availability unresolved; original values preserved'
            chronology.update(proxy_date=None,date_interpretation='UNRESOLVED_ADMINISTRATIVE_EVENT',administrative_publication_date=spec[6])
        elif decision=='AJACCIO_BASTIA':
            if not historical or historical['assessment']['classification']!='FULLY_CORROBORATED' or case.get('documented_resumption_completion_date')!='2024-12-03' or case.get('original_kickoff_date')!='2024-10-26' or case.get('corroborated_ft')!='0-0': raise ValueError('Completion evidence insufficient')
            chronology.update(actual_kickoff_date='2024-10-26',completion_date='2024-12-03',effective_result_availability_date='2024-12-03',date_interpretation='APPROVED_ACTUAL_COMPLETION_DAY',availability_verified=True)
            reason='Same fixture completed December 3 at 0-0; no new fixture and no score change'
        else:
            if not historical or historical['assessment']['classification']!='FULLY_CORROBORATED': raise ValueError('Unusual-score evidence insufficient')
            reason='Contemporary evidence corroborates 5-6; unusual score is not an exclusion'
    elif case is not None: raise ValueError('Unapproved special case')
    if row['assessment']['source_cancelled']:
        if row['season']!='2019/2020' or row['FT'] is not None or row['hg'] is not None or row['ag'] is not None or row['assessment']['score_bearing']: raise ValueError('Contradictory cancellation')
        disposition='NOT_PLAYED';decision='CANCELLED_2019_20';reason='Explicitly cancelled null-score slot; not an unknown missing result'
        chronology.update(proxy_date=None,date_interpretation='CANCELLED_SCHEDULE_ONLY')
    else:
        if not row['assessment']['score_bearing'] or not all(isinstance(row[x],str) and re.fullmatch(r'0|[1-9]\d*',row[x]) for x in ('hg','ag')) or row['FT']!=f"{row['hg']}-{row['ag']}": raise ValueError('Invalid source score')
    if row['assessment']['source_awarded'] and row['audit_id'] not in ADMIN: raise ValueError('Unreviewed administrative outcome')
    return dict(original=original,provenance=deepcopy(row['provenance']),source_competition_title=row['source_competition_title'],physical_line_sha256=row['physical_line_sha256'],decision_id='L2-P6-'+decision+'-'+row['audit_id'],policy=decision,disposition=disposition,reason=reason,chronology=chronology,flags=deepcopy(flags),historical_confidence=historical['assessment']['classification'] if historical else 'NOT_SAMPLED',evidence_ids=deepcopy(historical['evidence_ids']) if historical else [],historical_open_questions=deepcopy(historical['open_questions']) if historical else ['Not independently sampled; source date is a proxy'],special_event_context=deepcopy(case),identity_policy='ORIGINAL_LABELS_NO_ALIASES',candidate_match_id=candidate_id(row),technical_status='STRUCTURALLY_VALID',model_training_suitability='NOT_CLEARED',redistribution_permission='NOT_CLEARED',model_training_permission='NOT_CLEARED',consumer_requirement='Revalidate source-bound decision; establish actual availability and rights; results must be known strictly before prediction day')


def eligible_for_prediction(decision, row, prediction_day, *, historical=None, case=None):
    """Fail closed; caller cannot flip eligibility by editing saved decision fields."""
    expected=decide(row,historical,case)
    if expected!=decision: raise ValueError('Decision binding or policy altered')
    cutoff=day(prediction_day); c=expected['chronology'];available=c['effective_result_availability_date']
    return (expected['disposition']=='COMPLETED_RESULT_CANDIDATE' and c['availability_verified'] is True and available is not None and day(available)<cutoff)


def training_allowed(decision, row, prediction_day, *, historical=None, case=None):
    return (eligible_for_prediction(decision,row,prediction_day,historical=historical,case=case) and decision['model_training_suitability']=='CLEARED' and decision['model_training_permission']=='CLEARED')


def build(directory=PRIVATE, root=ROOT):
    protected=protect(directory,root); assessment,registry=review.build(directory,root)
    for name,obj in [(review.OUTPUT,assessment),(review.REGISTRY,registry)]:
        if (directory/name).read_bytes()!=base.encode(obj): raise ValueError('Frozen historical regeneration differs')
    report=review.read(directory/review.structure.REPORT); rows=report['records']
    if len(rows)!=4106 or sum(r['assessment']['score_bearing'] for r in rows)!=4006 or sum(r['assessment']['source_cancelled'] for r in rows)!=100: raise ValueError('Population differs')
    historical={x['audit_id']:x for x in registry['fixtures']};cases={x['original']['audit_id']:x for x in assessment['special_cases']}
    if cases.keys()!=SPECS.keys(): raise ValueError('Exceptional population differs')
    decisions=[decide(r,historical.get(r['audit_id']),cases.get(r['audit_id'])) for r in rows]
    if len({x['original']['audit_id'] for x in decisions})!=4106 or len({x['candidate_match_id'] for x in decisions})!=4106: raise ValueError('Duplicate IDs or lost observations')
    counts=Counter(x['disposition'] for x in decisions)
    if counts!=dict(COMPLETED_RESULT_CANDIDATE=4003,ADMINISTRATIVE_HOLD_OUT=3,NOT_PLAYED=100): raise ValueError('Unexpected provisional reconciliation')
    exceptions=[x for x in decisions if x['original']['audit_id'] in SPECS or x['disposition']=='NOT_PLAYED']
    summary=dict(phase=6,league='Ligue 2',population=4106,score_bearing=4006,dispositions=dict(counts),other_hold_outs=0,definitive_exclusions=0,historical_registry=376,targeted_research=79,context_only=297,wide_rounds=23,wide_members=228,outliers=25,reversal_pairs=31,reversal_endpoints=62,structural_queue=364,protected=protected,limitations='Candidate inclusion is not historical certification, availability verification, training suitability or rights clearance; no CSV or full audit archive generated')
    objects={REGISTRY:dict(phase=6,decisions=decisions),EXCEPTIONS:dict(phase=6,exceptions=exceptions,wide_rounds=assessment['wide_rounds'],reversals=assessment['reversals'],identity_review=assessment['identity_review'],cancellation_review=assessment['cancellation_review']),SUMMARY:summary}
    objects[MANIFEST]=dict(phase=6,inputs={str(p.relative_to(directory)):base.sha(p.read_bytes()) for p in [directory/review.structure.REPORT,directory/review.structure.QUEUE,directory/review.REFERENCES,directory/review.LEDGER,directory/review.REGISTRY,directory/BASELINE]},outputs={n:dict(bytes=len(base.encode(o)),sha256=base.sha(base.encode(o))) for n,o in objects.items()})
    return objects


if __name__=='__main__':
    initialize()
    for name,obj in build().items():
        content=base.encode(obj);target=PRIVATE/name
        if target.exists():
            if target.read_bytes()!=content: raise ValueError('Existing policy output differs: '+name)
        else: base.save(target,content)
    print(__import__('json').dumps(build()[SUMMARY],indent=2))
