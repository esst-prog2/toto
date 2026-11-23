"""Phase 5 documentary assessment only: no corrections, dispositions or standardization.

Run offline from frozen Phase 4 observations and explicitly curated research inputs.
Conditional overlap groups are research identities, never canonical match IDs/aliases.
"""
import argparse
from collections import Counter
from copy import deepcopy
from datetime import date
import json
from pathlib import Path
from scripts import validate_primeira_liga_structure as structure
c=structure.c
ROOT,PRIVATE=structure.ROOT,structure.PRIVATE
OUTPUTS=('phase5_review_registry.json','phase5_documentary_evidence_index.json','phase5_scheduling_assessment.json','phase5_conflict_exception_assessment.json','phase5_sample_assessment.json','phase5_confidence_summary.json','phase5_reproducibility_manifest.json')
CORE=('season','home','away','date','FT','completed')
STATUSES=('FULLY CORROBORATED CORE FACTS','PARTIALLY CORROBORATED','CONTRADICTED','UNRESOLVED','CONTEXT-ONLY REVIEWED')
FORBIDDEN=('disposition','canonical_team','standardized_date','accepted','excluded','authoritative_source')


def protect(directory=PRIVATE,root=ROOT):
    prior=structure.protect(directory,root)
    baseline=json.loads((directory/'phase5_protected_before.json').read_text())
    if baseline['approval']!='PHASE5_EVIDENCE_ONLY' or not baseline['files']:raise ValueError('Invalid Phase5 baseline')
    for n,sha in baseline['files'].items():
        path=root/n
        if not path.resolve().is_relative_to(root.resolve()) or c.sha(path.read_bytes())!=sha:raise ValueError('Frozen evidence changed: '+n)
    prefix=baseline['planning_log'];log=(root/'PLANNING_LOG.md').read_bytes()
    if len(log)<prefix['bytes'] or c.sha(log[:prefix['bytes']])!=prefix['sha256']:raise ValueError('Planning log prefix changed')
    return dict(previous=prior,phase2_4_frozen_entries=len(baseline['files']))


def inspect_reference(ref,directory):
    if not ref['url'].startswith('https://') or not ref['title'] or not ref['publisher']:raise ValueError('Incomplete citation')
    if ref['inspection'] not in ('DIRECT_DOCUMENT','INDEX_ONLY','ACCESS_RESTRICTED'):raise ValueError('Unknown inspection status')
    snapshot=ref['snapshot']
    if ref['inspection']=='DIRECT_DOCUMENT':
        if not snapshot:raise ValueError('Direct document has no snapshot')
        path=directory/snapshot['path']
        if not path.resolve().is_relative_to(directory.resolve()):raise ValueError('Snapshot path escape')
        raw=path.read_bytes()
        if len(raw)!=snapshot['bytes'] or c.sha(raw)!=snapshot['sha256']:raise ValueError('Evidence snapshot changed')
    elif snapshot:raise ValueError('Uninspected citation may not imply direct snapshot inspection')
    return ref


def assess(original,finding,references):
    if finding is None:
        return dict(classification='CONTEXT-ONLY REVIEWED',supported={},contradicted={},evidence_ids=[],administrative_finality='UNRESOLVED',result_availability='UNRESOLVED',notes=['Source binding/context reviewed; no individual documentary corroboration claimed.'],phase6_questions=[])
    if any(k in finding for k in FORBIDDEN):raise ValueError('Phase6 disposition/normalization is forbidden')
    if finding['audit_id']!=original['audit_id']:raise ValueError('Finding is bound to a different original')
    evidence=[references[x] for x in finding['evidence_ids']]
    direct=[x for x in evidence if x['inspection']=='DIRECT_DOCUMENT']
    facts=finding['facts']
    if set(facts)-set(CORE):raise ValueError('Unapproved factual dimension')
    if facts and not direct:raise ValueError('Indexed or inaccessible evidence cannot verify/contradict facts')
    if direct and facts and not any(x['claims'] for x in direct):raise ValueError('Direct factual evidence has no inspected claims')
    if 'date'in facts:date.fromisoformat(facts['date'])
    if 'completed'in facts and type(facts['completed']) is not bool:raise ValueError('Completion must be explicit boolean')
    supported={k:v for k,v in facts.items() if k=='completed' or v==original[k]}
    contradicted={k:dict(original=original[k],documentary=v) for k,v in facts.items() if k!='completed' and v!=original[k]}
    if contradicted:status='CONTRADICTED'
    elif finding['core_independently_supported']:
        if not all(k in facts for k in CORE) or not facts['completed'] or not direct:raise ValueError('Full core corroboration lacks dimensions/direct evidence')
        if not any(x['source_type'] in ('PRIMARY_PARTICIPANT_OR_LEAGUE','CONTEMPORARY_JOURNALISM') for x in direct):raise ValueError('Full core corroboration requires qualified independent documentary source')
        status='FULLY CORROBORATED CORE FACTS'
    elif evidence or facts:status='PARTIALLY CORROBORATED'
    else:status='UNRESOLVED'
    return dict(classification=status,supported=supported,contradicted=contradicted,evidence_ids=finding['evidence_ids'],administrative_finality='UNRESOLVED',result_availability='UNRESOLVED',notes=finding['notes'],phase6_questions=finding['phase6_questions'],independence_limit='Documentary narrative is separate from acquired Git files; complete upstream independence not proven. Core facts do not certify legal finality or availability time.')


def sample_selection(rows,flagged):
    result=[]
    for year in range(1994,2026):
        frame=[r for r in rows if r['season']==f'{year}/{year+1}' and r['audit_id'] not in flagged and ('original_fields'in r if year<2025 else 'original_fields'not in r)]
        if not frame:raise ValueError('Empty sampling season')
        result.append(min(frame,key=lambda r:(r['date'],r['home'],r['away'],r['audit_id'])))
    return result


def memberships(context):
    if context['kind']=='WIDE_ROUND':return context['fixture_ids']
    if context['kind']=='SOURCE_ORDER_REVERSAL':return [context['previous_id'],context['current_id']]
    raise ValueError('Unknown context kind')


def group_rows(rows,overlaps):
    groups={r['audit_id']:(r['audit_id'],) for r in rows}
    seen=set()
    for season in overlaps['seasons']:
        for pair in season['comparisons']:
            ids=(pair['historical_id'],pair['modern_id'])
            if seen.intersection(ids):raise ValueError('Non one-to-one overlap')
            if any(i not in groups for i in ids):raise ValueError('Unbound overlap')
            seen.update(ids)
            for i in ids:groups[i]=tuple(sorted(ids))
    return groups


def context_status(evidence_ids,references):
    if any(references[i]['inspection']=='DIRECT_DOCUMENT' for i in evidence_ids):return 'PARTIAL_DIRECT_ENDPOINT'
    if evidence_ids:return 'INDEX_LEAD_ONLY'
    return 'UNRESOLVED'


def count_classes(records):
    totals=Counter(r['assessment']['classification'] for r in records)
    return {status:totals[status] for status in STATUSES}


def build(directory=PRIVATE,root=ROOT):
    protected=protect(directory,root)
    # Reparse originals, then compare all Phase4 artifacts rather than trusting their totals.
    regenerated=structure.build(directory,root)
    for n,obj in regenerated.items():
        if c.encode(obj)!=(directory/n).read_bytes():raise ValueError('Phase4 reconstruction differs: '+n)
    historical=regenerated['phase4_historical_structure.json'];modern=regenerated['phase4_modern_structure.json']
    rows=[r for season in historical['seasons']+modern['seasons'] for r in season['records']];by={r['audit_id']:r for r in rows}
    if len(by)!=len(rows):raise ValueError('Duplicate source audit identity')
    queue=regenerated['phase4_review_queue.json'];overlaps=regenerated['phase4_overlap_reconciliation.json']
    flagged={r['original']['audit_id']:r for r in queue['records']}
    if len(flagged)!=207 or sum(len(r['categories']) for r in queue['records'])!=221:raise ValueError('Flagged population changed')
    plan=json.loads((directory/'phase5_research_plan.json').read_text());inputs=json.loads((directory/'phase5_research_inputs.json').read_text())
    samples=sample_selection(rows,flagged)
    if samples!=plan['samples']:raise ValueError('Deterministic sample or preserved source binding changed')
    references={r['evidence_id']:inspect_reference(r,directory) for r in inputs['reference_items']}
    if len(references)!=len(inputs['reference_items']):raise ValueError('Duplicate evidence identity')
    for n,sha in inputs['research_log_files'].items():
        path=directory/n
        if not path.resolve().is_relative_to(directory.resolve()) or c.sha(path.read_bytes())!=sha:raise ValueError('Research log changed')
    findings={r['audit_id']:r for r in inputs['targeted_findings']}
    if len(findings)!=len(inputs['targeted_findings']) or set(findings)-by.keys():raise ValueError('Unbound/duplicate finding')
    groups=group_rows(rows,overlaps)
    selected=set(flagged)|set(findings)
    # Linked originals retained for diagnostic comparison, without inheriting another source's confidence.
    selected|={partner for i in tuple(selected) for partner in groups[i]}
    context_map={ctx['context_id']:ctx for ctx in plan['contexts']}
    assessments={x['context_id']:x for x in inputs['contexts']}
    if len(context_map)!=31 or set(context_map)!=set(assessments) or len(assessments)!=len(inputs['contexts']):raise ValueError('Scheduling context coverage differs')
    for name,ctx in context_map.items():
        ids=memberships(ctx)
        if len(ids)!=len(set(ids)) or not set(ids)<=flagged.keys():raise ValueError('Unbound scheduling context member')
        a=assessments[name]
        if not set(a['targeted_diagnostic_ids'])<=set(ids) or not set(a['targeted_diagnostic_ids'])<=findings.keys():raise ValueError('Unbound diagnostic target')
        for i in a['evidence_ids']:
            if i not in references:raise ValueError('Unknown context evidence')
        if a['status']!=context_status(a['evidence_ids'],references):raise ValueError('Context classification inconsistent with its evidence')
    registry=[]
    for i in sorted(selected):
        original=by[i];raw=(directory/original['source']).read_bytes();literal=b''.join(raw.splitlines(keepends=True)[original['source_line']-1:original['source_end_line']])
        if c.sha(literal)!=original['physical_record_sha256']:raise ValueError('Physical source line differs')
        registry.append(dict(original=original,conditional_research_group=c.sha(c.encode(groups[i])),conditional_partner_ids=list(groups[i]),research_scope='TARGETED_FIXTURE_RESEARCH' if i in findings else'CONTEXT_ONLY_OR_LINKED_ORIGINAL',categories=flagged[i]['categories'] if i in flagged else[],context_ids=sorted(name for name,ctx in context_map.items() if i in memberships(ctx)),assessment=assess(original,findings.get(i),references)))
    indexed={r['original']['audit_id']:r for r in registry}
    conditional={}
    for r in registry:conditional.setdefault(r['conditional_research_group'],[]).append(r)
    group_counts=Counter()
    # Priority is conservative: one contradicted original does not mean every partner is incorrect.
    priority=('CONTRADICTED','FULLY CORROBORATED CORE FACTS','PARTIALLY CORROBORATED','UNRESOLVED','CONTEXT-ONLY REVIEWED')
    for members in conditional.values():
        statuses={r['assessment']['classification'] for r in members}
        group_counts[next(s for s in priority if s in statuses)]+=1
    sample_records=[indexed[r['audit_id']] for r in samples]
    scheduling=[dict(deepcopy(context_map[n]),evidence_assessment=assessments[n],warning='Only named diagnostic endpoints have individual evidence; no all-member verification or date correction.') for n in sorted(context_map)]
    unusual={r['audit_id'] for r in plan['unusual']};target_groups={c.sha(c.encode(groups[i])) for i in findings}
    summary=dict(phase=5,population=queue['totals'],reviewed_source_observations=len(registry),flagged_source_observations=len(flagged),conditional_review_groups=len(conditional),targeted_source_observations=len(findings),targeted_conditional_groups=len(target_groups),context_only_or_linked_observations=len(registry)-len(findings),context_only_conditional_groups=len(conditional)-len(target_groups),source_confidence=count_classes(registry),conditional_group_confidence={s:group_counts[s] for s in STATUSES},ordinary_samples=dict(count=len(samples),classifications=count_classes(sample_records)),unusual_scores=dict(source_observations=len(unusual),conditional_events=len({groups[i] for i in unusual})),scheduling=dict(wide_round_contexts=sum(x['kind']=='WIDE_ROUND' for x in scheduling),reversal_contexts=sum(x['kind']=='SOURCE_ORDER_REVERSAL' for x in scheduling),classifications=dict(Counter(x['evidence_assessment']['status'] for x in scheduling))),protected=protected,limits=inputs['limits'],early_gap=dict(seasons=['1990/1991','1991/1992','1992/1993','1993/1994'],expected_slots=1298,approved_dated_observations=0,rsssf_1990_result_identities=380),permissions='Technical access, historical correctness, administrative finality, chronology, redistribution and model-training clearance remain separate. No training clearance established.')
    output={OUTPUTS[0]:dict(phase=5,records=registry),OUTPUTS[1]:dict(phase=5,references=list(references.values()),research_logs=inputs['research_log_files'],issues=inputs['issues']),OUTPUTS[2]:dict(phase=5,contexts=scheduling),OUTPUTS[3]:dict(phase=5,records=[r for r in registry if r['categories'] or r['assessment']['contradicted'] or r['assessment']['phase6_questions']],issues=inputs['issues'],no_dispositions=True),OUTPUTS[4]:dict(phase=5,selection_rule=plan['sample_rule'],records=sample_records),OUTPUTS[5]:summary}
    for issue in inputs['issues']:
        if not set(issue['evidence_ids'])<=references.keys():raise ValueError('Unbound issue evidence')
    dependencies={n:c.sha((directory/n).read_bytes()) for n in ['phase5_protected_before.json','phase5_research_plan.json','phase5_research_inputs.json',*structure.OUTPUTS]}
    output[OUTPUTS[6]]=dict(phase=5,inputs=dependencies,outputs={n:dict(sha256=c.sha(c.encode(v)),bytes=len(c.encode(v))) for n,v in output.items()},method='Offline assessment from preserved documentary snapshots and curated claims; no network; no historical corrections/dispositions; regeneration checks assessment reproducibility, not historical truth.')
    return output


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output-directory',type=Path,default=PRIVATE);args=parser.parse_args()
    output=build();args.output_directory.mkdir(exist_ok=True,parents=True)
    for n,obj in output.items():c.keep(args.output_directory/n,c.encode(obj))
    print(json.dumps(output['phase5_confidence_summary.json'],indent=2))

if __name__=='__main__':main()
