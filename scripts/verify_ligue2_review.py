"""Phase 5 source-bound evidence accounting, not historical processing policy."""
from collections import Counter
from datetime import date
import json
from pathlib import Path
import subprocess
from scripts import validate_ligue2_structure as structure

ROOT, PRIVATE, base = structure.ROOT, structure.PRIVATE, structure.base
BASELINE='phase5_protected_before.json'
SELECTION='phase5_sample_selection.json'
LEDGER='phase5_historical_review.json'
REFERENCES='phase5_evidence_inventory.json'
OUTPUT='phase5_evidence_assessment.json'
REGISTRY='phase5_fixture_registry.json'
FACTS={'date','home','away','FT'}


def read(path):
    def unique(items):
        d={}
        for k,v in items:
            if k in d:raise ValueError('Duplicate JSON key: '+k)
            d[k]=v
        return d
    return json.loads(path.read_text(),object_pairs_hook=unique)


def initialize(directory=PRIVATE,root=ROOT):
    if (directory/BASELINE).exists():return protect(directory,root)
    structure.protect(directory,root);final=read(directory/'phase4_final_verification.json')
    for name,item in final['private_files_before_receipt'].items():
        if base.sha((directory/name).read_bytes())!=item['sha256']:raise ValueError('Approved private evidence changed: '+name)
    for name,digest in final['public_files'].items():
        if base.sha((root/name).read_bytes())!=digest:raise ValueError('Approved public work changed: '+name)
    publics=set(final['public_files'])|set(read(directory/'phase3_final_verification.json')['public_files'])|set(read(directory/'phase2_final_verification.json')['public_files'])
    files={str(p.relative_to(root)):base.sha(p.read_bytes()) for p in directory.rglob('*') if p.is_file()}
    files.update({n:base.sha((root/n).read_bytes()) for n in publics if n!='PLANNING_LOG.md'})
    log=(root/'PLANNING_LOG.md').read_bytes()
    base.save(directory/BASELINE,base.encode(dict(files=files,planning_log=dict(bytes=len(log),sha256=base.sha(log)))))
    return protect(directory,root)


def protect(directory=PRIVATE,root=ROOT):
    previous=structure.protect(directory,root);frozen=read(directory/BASELINE)
    if not frozen['files']:raise ValueError('Empty historical review baseline')
    for name,digest in frozen['files'].items():
        p=root/name
        if not p.resolve().is_relative_to(root.resolve()) or base.sha(p.read_bytes())!=digest:raise ValueError('Frozen Phase 2–4 file changed: '+name)
    prefix=frozen['planning_log'];log=(root/'PLANNING_LOG.md').read_bytes()
    if len(log)<prefix['bytes'] or base.sha(log[:prefix['bytes']])!=prefix['sha256']:raise ValueError('Planning prefix changed')
    return dict(previous=previous,phase2_4_entries=len(frozen['files']))


def binding(r):
    return {k:r[k] for k in ['audit_id','source','source_sha256','source_line','physical_line_sha256','season','date','home','away','FT','annotation']}


def select(report):
    ordinary=[]
    for year in range(2014,2025):
        candidates=[r for r in report['records'] if r['season']==f'{year}/{year+1}' and r['assessment']['score_bearing'] and not r['assessment']['flags']]
        if not candidates:raise ValueError('No ordinary sampling population')
        ordinary.append(min(candidates,key=lambda r:base.sha(('ligue2-phase5-v1:'+r['audit_id']).encode())))
    priority={r['audit_id'] for r in report['records'] if any(k in r['assessment']['flags'] for k in ['DIAGNOSTIC_DATE_OUTLIER','SOURCE_ORDER_DATE_REVERSAL','SOURCE_MARKED_AWARDED','BORDEAUX_RODEZ_ADMINISTRATIVE_REVIEW','UNUSUAL_SCORE'])}
    priority.update(r['audit_id'] for r in ordinary)
    return dict(rule='For each season, minimum SHA256(ligue2-phase5-v1: + audit_id) among score-bearing observations with no Phase 4 flags; frozen before research',
                ordinary=[binding(r) for r in ordinary],priority_ids=sorted(priority))


def verify_queue(report,queue):
    byid={r['audit_id']:r for r in report['records']}
    expected={k for k,r in byid.items() if r['assessment']['flags']}
    actual={r['audit_id'] for r in queue['fixtures']}
    if len(byid)!=len(report['records']) or len(actual)!=len(queue['fixtures']) or expected!=actual:raise ValueError('Queue population differs')
    for r in queue['fixtures']:
        original=byid[r['audit_id']]
        for key,value in r.items():
            if original[key]!=value:raise ValueError('Queue binding changed: '+key)
    outliers={r['audit_id'] for r in report['records'] if 'DIAGNOSTIC_DATE_OUTLIER' in r['assessment']['flags']}
    wide={r['audit_id'] for r in report['records'] if 'WIDE_ROUND' in r['assessment']['flags']}
    reversals={r['audit_id'] for r in report['records'] if 'SOURCE_ORDER_DATE_REVERSAL' in r['assessment']['flags']}
    if not outliers<=wide:raise ValueError('Outlier outside wide-round population')
    return dict(population=len(byid),queue=len(actual),categories=dict(Counter(k for r in queue['fixtures'] for k in r['assessment']['flags'])),
                wide_contexts=sum(len(s['wide_rounds']) for s in report['seasons']),reversal_pairs=sum(len(s['source_order_date_reversals']) for s in report['seasons']),
                outliers_in_wide=len(outliers&wide),reversal_endpoints_in_wide=len(reversals&wide),additional_reversal_endpoints=len(reversals-wide))


def validate_evidence(e):
    if not e.get('id') or not e.get('title') or not e.get('organization') or not e.get('establishes') or not e.get('limitations'):raise ValueError('Incomplete bibliography')
    if not e['url'].startswith('https://'):raise ValueError('Non-HTTPS evidence URL')
    if e['access'] not in {'DIRECT','INDEX_ONLY','INACCESSIBLE'}:raise ValueError('Unknown access strength')
    if e['independence'] not in {'OFFICIAL_RECORD','INDEPENDENT_NARRATIVE','COMPILED_OR_UNESTABLISHED','SAME_UPSTREAM'}:raise ValueError('Unknown independence')
    date.fromisoformat(e['access_date'])
    if e.get('publication_date'):date.fromisoformat(e['publication_date'])
    for claim in e.get('fixture_claims',[]):
        if not claim.get('audit_id') or not set(claim.get('facts',{}))<=FACTS:raise ValueError('Invalid fixture claim')
        if not all(isinstance(v,str) and v for v in claim.get('facts',{}).values()):raise ValueError('Invalid fact value')


def assess_fixture(r,entries):
    verified={};contradictions=[];contexts=[];direct_contexts=[];references=[]
    for e in entries:
        validate_evidence(e);references.append(e['id'])
        for claim in e.get('fixture_claims',[]):
            if claim['audit_id']!=r['audit_id']:continue
            if e['access']!='DIRECT' or e['independence'] not in {'OFFICIAL_RECORD','INDEPENDENT_NARRATIVE'}:continue
            for key,value in claim.get('facts',{}).items():
                if value==r[key]:verified.setdefault(key,[]).append(e['id'])
                else:contradictions.append(dict(field=key,source=r[key],evidence=value,evidence_id=e['id']))
        context_key=f"{r['season']}:R{r['round']}"
        context_match=context_key in e.get('context_claims',[]) or (r['season']=='2019/2020' and 'cancelled' in r.get('annotation','').lower() and 'CANCEL2019' in e.get('context_claims',[]))
        if context_match:
            contexts.append(e['id'])
            if e['access']=='DIRECT' and e['independence'] in {'OFFICIAL_RECORD','INDEPENDENT_NARRATIVE'}:direct_contexts.append(e['id'])
    status='CONTRADICTED' if contradictions else 'FULLY_CORROBORATED' if set(verified)==FACTS else 'PARTIALLY_CORROBORATED' if verified else 'UNRESOLVED'
    return dict(classification=status,directly_corroborated_facts=verified,contradictions=contradictions,context_evidence_ids=sorted(set(contexts)),direct_independent_context_evidence_ids=sorted(set(direct_contexts)),evidence_ids=sorted(set(references)),
                confidence_limit='Four-fact corroboration is not exhaustive legal finality or result-availability certification; no inclusion/exclusion follows',
                effective_result_availability=None,phase6_policy='NOT_DECIDED')


def validate_context(item,key,evidence,expected):
    if item['classification'] not in {'DOCUMENTED','PARTIAL','UNRESOLVED'} or not item.get('limitations') or not item.get('finding'):raise ValueError('Invalid context classification/limits')
    if not set(item['evidence_ids'])<=evidence.keys():raise ValueError('Unknown context reference')
    if set(item['member_ids'])!=expected or len(item['member_ids'])!=len(expected):raise ValueError('Context source membership differs')
    if item['classification']=='DOCUMENTED' and not any(evidence[x]['access']=='DIRECT' and evidence[x]['independence'] in {'OFFICIAL_RECORD','INDEPENDENT_NARRATIVE'} and f"{key[0]}:R{key[1]}" in evidence[x].get('context_claims',[]) for x in item['evidence_ids']):raise ValueError('Documented context lacks direct independent evidence')


def build(directory=PRIVATE,root=ROOT):
    protected=protect(directory,root);report=read(directory/structure.REPORT);queue=read(directory/structure.QUEUE);checks=verify_queue(report,queue)
    selection=select(report)
    if selection!=read(directory/SELECTION):raise ValueError('Frozen sample selection changed')
    ledger=read(directory/LEDGER);bibliography=read(directory/REFERENCES);evidence={e['id']:e for e in bibliography['evidence']}
    if len(evidence)!=len(bibliography['evidence']):raise ValueError('Duplicate evidence ID')
    for e in evidence.values():validate_evidence(e)
    records={r['audit_id']:r for r in report['records']};ordinary={r['audit_id'] for r in selection['ordinary']};population={r['audit_id'] for r in queue['fixtures']}|ordinary
    discoveries=ledger.get('additional_discoveries',[])
    if len({x['audit_id'] for x in discoveries})!=len(discoveries):raise ValueError('Duplicate discovery')
    for discovery in discoveries:
        key=discovery['audit_id']
        if key not in records or discovery['original']!=binding(records[key]):raise ValueError('Discovery source binding differs')
        population.add(key)
    entries={r['audit_id']:r for r in ledger['fixtures']}
    for e in evidence.values():
        if any(c['audit_id'] not in population for c in e.get('fixture_claims',[])):raise ValueError('Evidence fixture outside registry')
    if len(entries)!=len(ledger['fixtures']) or entries.keys()!=population:raise ValueError('Historical registry population differs')
    registry=[]
    for key in sorted(population,key=lambda k:(records[k]['season'],records[k]['source_line'])):
        r=records[key];entry=entries[key]
        if entry['original']!=binding(r) or entry['categories']!=r['assessment']['flags']:raise ValueError('Historical source/category binding changed')
        if not entry['open_questions'] or entry['research_mode'] not in {'PRIORITY_FIXTURE_RESEARCH','CONTEXT_REVIEW_ONLY'}:raise ValueError('Missing uncertainty/research classification')
        ids=entry['evidence_ids']
        if len(set(ids))!=len(ids) or not set(ids)<=evidence.keys():raise ValueError('Unknown/duplicate evidence reference')
        registry.append(dict(entry,assessment=assess_fixture(r,[evidence[x] for x in ids])))
    wide_expected={(s['season'],w['round']):{r['audit_id'] for r in w['fixtures']} for s in report['seasons'] for w in s['wide_rounds']}
    contexts={(r['season'],r['round']):r for r in ledger['wide_rounds']}
    if len(contexts)!=len(ledger['wide_rounds']) or contexts.keys()!=wide_expected.keys():raise ValueError('Wide contexts differ')
    for key,item in contexts.items():
        validate_context(item,key,evidence,wide_expected[key])
    expected_pairs={(s['season'],x['previous_id'],x['current_id']) for s in report['seasons'] for x in s['source_order_date_reversals']}
    actual_pairs={(x['season'],x['previous_id'],x['current_id']) for x in ledger['reversals']}
    for pair in ledger['reversals']:
        if pair['classification'] not in {'DOCUMENTED','PARTIAL','UNRESOLVED'} or not pair.get('limitations') or not set(pair['evidence_ids'])<=evidence.keys():raise ValueError('Invalid reversal review metadata')
        if pair['classification']=='DOCUMENTED':
            for endpoint in ('previous_id','current_id'):
                assessed=next(x for x in registry if x['audit_id']==pair[endpoint])
                if 'date' not in assessed['assessment']['directly_corroborated_facts']:raise ValueError('Documented reversal lacks two actual dates')
    if actual_pairs!=expected_pairs or len(actual_pairs)!=len(ledger['reversals']):raise ValueError('Reversal context differs')
    for case in ledger['special_cases']:
        original=case['original'];key=original['audit_id']
        if key not in population or original!=binding(records[key]):raise ValueError('Special-case source binding differs')
        if case['effective_result_availability'] is not None or case['phase6_processing_policy']!='NOT_DECIDED':raise ValueError('Phase 6 processing decision not authorized')
    if not set(selection['priority_ids'])<=population:raise ValueError('Priority outside population')
    summary=dict(structural_population=checks,review_registry=len(registry),ordinary_samples=len(ordinary),frozen_priority_distinct_fixtures=len(selection['priority_ids']),priority_distinct_fixtures=sum(x['research_mode']=='PRIORITY_FIXTURE_RESEARCH' for x in registry),
        fixture_level_direct_evidence_fixtures=sum(bool(x['assessment']['directly_corroborated_facts'] or x['assessment']['contradictions']) for x in registry),
        direct_context_referenced_fixtures=sum(bool(x['assessment']['direct_independent_context_evidence_ids']) for x in registry),
        additional_discovered_fixtures=len(discoveries),fixture_classifications=dict(Counter(r['assessment']['classification'] for r in registry)),
        priority_classifications=dict(Counter(r['assessment']['classification'] for r in registry if r['research_mode']=='PRIORITY_FIXTURE_RESEARCH')),
        ordinary_classifications=dict(Counter(r['assessment']['classification'] for r in registry if r['audit_id'] in ordinary)),
        research_modes=dict(Counter(r['research_mode'] for r in registry)),wide_context_classifications=dict(Counter(x['classification'] for x in ledger['wide_rounds'])),
        reversal_context_classifications=dict(Counter(x['classification'] for x in ledger['reversals'])),
        evidence_access=dict(Counter(e['access'] for e in evidence.values())),evidence_independence=dict(Counter(e['independence'] for e in evidence.values())))
    assessment=dict(phase=5,protected=protected,summary=summary,selection=selection,wide_rounds=ledger['wide_rounds'],reversals=ledger['reversals'],
        special_cases=ledger['special_cases'],additional_discoveries=discoveries,identity_review=ledger['identity_review'],cancellation_review=ledger['cancellation_review'],coverage=ledger['coverage'],
        policy='Evidence review only: no corrections, HOLD OUTs, effective dates, screening, aliases, standardization or training')
    return assessment,dict(phase=5,summary=summary,fixtures=registry)


if __name__=='__main__':
    assessment,registry=build()
    for name,obj in [(OUTPUT,assessment),(REGISTRY,registry)]:
        target=PRIVATE/name;content=base.encode(obj)
        if target.exists():
            if target.read_bytes()!=content:raise ValueError('Historical output changed: '+name)
        else:base.save(target,content)
    print(json.dumps(assessment['summary'],indent=2))
