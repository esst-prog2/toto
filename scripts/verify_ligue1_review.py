"""Offline Phase 5 evidence accounting, never corrections or certification.

Human-inspected evidence lives in the private ledger. These checks enforce source
bindings and claim strength; they do not establish that a web assertion is true.
"""
import argparse
from collections import Counter
from datetime import date
import json
from pathlib import Path

from scripts import validate_ligue1_structure as structural

ROOT, PRIVATE = structural.ROOT, structural.PRIVATE
base=structural.base
BASELINE='phase5_protected_before.json'
SELECTION='phase5_sample_selection.json'
LEDGER='phase5_historical_review.json'
OUTPUT='phase5_evidence_check.json'
FACTS={'date','home','away','FT'}
PUBLIC=structural.PUBLIC+('scripts/validate_ligue1_structure.py','tests/test_ligue1_structure.py','docs/ligue-1-validation.md')


def read(path):
    def unique(items):
        result={}
        for key,value in items:
            if key in result:raise ValueError('Duplicate evidence key: '+key)
            result[key]=value
        return result
    return json.loads(path.read_text(),object_pairs_hook=unique)


def initialize(directory=PRIVATE,root=ROOT):
    if (directory/BASELINE).exists():return protect(directory,root)
    structural.protect(directory,root);final=read(directory/'phase4_final_verification.json')
    for name,item in final['new_private_files_before_this_receipt'].items():
        if base.sha((directory/name).read_bytes())!=item['sha256']:raise ValueError('Approved Phase 4 evidence changed: '+name)
    for name,digest in final['public_files'].items():
        if base.sha((root/name).read_bytes())!=digest:raise ValueError('Approved Phase 4 public file changed: '+name)
    files={str(p.relative_to(root)):base.sha(p.read_bytes()) for p in directory.rglob('*') if p.is_file()}
    files.update({n:base.sha((root/n).read_bytes()) for n in PUBLIC})
    log=(root/'PLANNING_LOG.md').read_bytes()
    base.save(directory/BASELINE,base.encode(dict(files=files,planning_log=dict(bytes=len(log),sha256=base.sha(log)))))
    return protect(directory,root)


def protect(directory=PRIVATE,root=ROOT):
    previous=structural.protect(directory,root);frozen=read(directory/BASELINE)
    if not frozen['files']:raise ValueError('Empty evidence baseline')
    for name,digest in frozen['files'].items():
        path=root/name
        if not path.resolve().is_relative_to(root.resolve()) or base.sha(path.read_bytes())!=digest:raise ValueError('Frozen Phase 2–4 file changed: '+name)
    prefix=frozen['planning_log'];log=(root/'PLANNING_LOG.md').read_bytes()
    if len(log)<prefix['bytes'] or base.sha(log[:prefix['bytes']])!=prefix['sha256']:raise ValueError('Planning history changed')
    return dict(previous=previous,phase2_4_entries=len(frozen['files']))


def selection(records):
    chosen=[]
    for y in range(1990,2026):
        season=f'{y}/{y+1}';all_season=[r for r in records if r['season']==season]
        if not all_season:continue
        # Rotate H/D in the old window (away results carry known label flags),
        # then H/D/A in the modern window. No source/evidence-dependent selection.
        preferred=('H','D')[(y-1990)%2] if y<2014 else ('H','D','A')[(y-2014)%3]
        candidates=[r for r in all_season if not r['assessment']['flags'] and r['assessment']['goal_derived_outcome']==preferred]
        if not candidates:raise ValueError('Empty ordinary outcome stratum: '+season)
        chosen.append(min(candidates,key=lambda r:base.sha(('ligue1-phase5-v1:'+r['audit_id']).encode())))
    return chosen


def binding(r):
    return {k:r[k] for k in ('audit_id','source','source_sha256','source_line','raw_line_sha256','season','date','home','away','FT')}


def validate_evidence(e):
    if e['access'] not in {'DIRECT','INDEX_ONLY','INACCESSIBLE'}:raise ValueError('Unknown access class')
    if e['independence'] not in {'INDEPENDENT_NARRATIVE','OFFICIAL_RECORD','UNESTABLISHED','SHARED_OR_POSSIBLE_UPSTREAM'}:raise ValueError('Unknown independence')
    if not e['url'].startswith('https://') or not e['title'] or not e['establishes']:raise ValueError('Incomplete evidence provenance')
    if not set(e.get('facts',{}))<=FACTS:raise ValueError('Unknown fact field')
    if e.get('publication_date'):date.fromisoformat(e['publication_date'])
    date.fromisoformat(e['access_date'])
    for field,value in e.get('facts',{}).items():
        if not isinstance(value,str) or not value:raise ValueError('Empty/nonliteral evidence fact')
        if field=='date':date.fromisoformat(value)


def fixture_status(item,evidence):
    matched=set();contradictions=[]
    for identifier in item['evidence_ids']:
        e=evidence[identifier];validate_evidence(e)
        if e['access']!='DIRECT' or e['independence'] not in {'INDEPENDENT_NARRATIVE','OFFICIAL_RECORD'}:continue
        for field,value in e.get('facts',{}).items():
            if value==item['source_values'][field]:matched.add(field)
            else:contradictions.append(dict(evidence_id=identifier,field=field,source=item['source_values'][field],evidence=value))
    # VERIFIED means full-fact match corroboration, not exhaustive legal finality.
    status='VERIFIED' if matched==FACTS and not contradictions else 'PARTIAL' if matched or contradictions else 'UNRESOLVED'
    return dict(status=status,matched_facts=sorted(matched),contradictions=contradictions,
                finality=item.get('finality','NOT_EXHAUSTIVELY_CERTIFIED'))


def build(directory=PRIVATE,root=ROOT):
    protection=protect(directory,root);report=read(directory/structural.REPORT);ledger=read(directory/LEDGER)
    records={r['audit_id']:r for r in report['records']};selected=selection(list(records.values()))
    saved=read(directory/SELECTION)
    if saved['ordinary']!=[binding(r) for r in selected]:raise ValueError('Deterministic selection changed')
    ev={e['id']:e for e in ledger['evidence']}
    if len(ev)!=len(ledger['evidence']):raise ValueError('Duplicate evidence IDs')
    for e in ev.values():validate_evidence(e)
    results=[];seen=set()
    for item in ledger['fixtures']:
        identifier=item['audit_id']
        if identifier in seen or identifier not in records:raise ValueError('Duplicate/unknown reviewed fixture')
        seen.add(identifier);r=records[identifier]
        if item['binding']!=binding(r) or item['source_values']!={k:r[k] for k in FACTS}:raise ValueError('Evidence misbound to source facts')
        if any(e not in ev for e in item['evidence_ids']):raise ValueError('Missing evidence ID')
        results.append(dict(audit_id=identifier,season=r['season'],roles=item['roles'],**fixture_status(item,ev)))
    if not {r['audit_id'] for r in selected}<=seen:raise ValueError('Ordinary sample missing a represented season')
    rounds=ledger['rounds'];expected={(s['season'],w['round']):set(w['affected_ids']) for s in report['seasons'] for w in s['wide_rounds']}
    if len(rounds)!=len(expected) or {(r['season'],r['round']) for r in rounds}!=set(expected):raise ValueError('Scheduling scope changed')
    for r in rounds:
        if set(r['affected_ids'])!=expected[r['season'],r['round']] or len(r['affected_ids'])!=len(set(r['affected_ids'])):raise ValueError('Round fixture membership changed')
        if r['status'] not in {'DOCUMENTED','PARTIAL','UNRESOLVED'}:raise ValueError('Unknown round status')
        supporting=[ev[e] for e in r['evidence_ids']]
        if {x['audit_id'] for x in r['source_observations']}!=expected[r['season'],r['round']]:raise ValueError('Round source bindings missing')
        if len(r['source_observations'])!=len(r['affected_ids']):raise ValueError('Duplicate round source binding')
        for x in r['source_observations']:
            if x!=binding(records[x['audit_id']]):raise ValueError('Round source binding changed')
        if r['individually_certified_all_members'] is not False:raise ValueError('Round explanation cannot certify all fixtures')
        if r['status']=='DOCUMENTED' and not any(e['access']=='DIRECT' and e['independence'] in {'OFFICIAL_RECORD','INDEPENDENT_NARRATIVE'} for e in supporting):raise ValueError('Documented round lacks direct independent evidence')
    if len(ledger['major_cases'])!=6 or len({c['audit_id'] for c in ledger['major_cases']})!=6:raise ValueError('Major exception scope changed')
    for c in ledger['major_cases']:
        if c['binding']!=binding(records[c['audit_id']]):raise ValueError('Major case binding changed')
        if c['chronology']['effective_result_availability'] is not None:raise ValueError('Phase 5 cannot implement date policy')
        if not c['evidence_ids'] or any(e not in ev for e in c['evidence_ids']):raise ValueError('Case evidence missing')
    # Rebind supplemental conflicts to the immutable CSV as well as the primary
    # observations. Extra source observations are not extra distinct fixtures.
    supplemental=[b for c in ledger['major_cases'] for b in c.get('overlapping_source_bindings',[])]
    if supplemental:
        path=structural.metadata.HIST;raw=(directory/path).read_bytes()
        historical={r['audit_id']:r for r in structural.read_csv(raw,path,base.sha(raw))}
        for b in supplemental:
            if b['audit_id'] not in historical or b!=binding(historical[b['audit_id']]):raise ValueError('Supplemental source binding changed')
    if ledger['missing_fixture']['source_observation_exists'] is not False:raise ValueError('Phase 5 cannot add missing fixture')
    if ledger['grouped_label_analysis']['applied'] is not False:raise ValueError('Phase 5 cannot apply label policy')
    grouped=report['totals']['category_counts']['SYSTEMATIC_SOURCE_LABEL_DEFECT']
    if ledger['grouped_label_analysis']['primary_defects']!=grouped:raise ValueError('Label analysis scope changed')
    return dict(scope='Phase 5 evidence accounting only; no correction/eligibility/date policy',protected=protection,
                ledger_sha256=base.sha((directory/LEDGER).read_bytes()),selection_sha256=base.sha((directory/SELECTION).read_bytes()),
                ordinary_sample_count=len(selected),individually_reviewed=len(results),fixture_counts=dict(Counter(r['status'] for r in results)),
                ordinary_results=[r for r in results if 'ORDINARY_SAMPLE' in r['roles']],fixtures=results,
                scheduling_counts=dict(Counter(r['status'] for r in rounds)),scheduling_rounds=len(rounds),
                scheduling_affected_slots=len({a for r in rounds for a in r['affected_ids']}),
                primary_observations=len(records),primary_scored=sum(r['FT'] is not None for r in records.values()),
                primary_unscored=sum(r['FT'] is None for r in records.values()),
                ordinary_counts=dict(Counter(r['status'] for r in results if 'ORDINARY_SAMPLE' in r['roles'])),
                evidence_access_counts=dict(Counter(e['access'] for e in ev.values())),
                contradictions=[dict(audit_id=r['audit_id'],**c) for r in results for c in r['contradictions']],
                warnings=['Verified sample is not population certification.','Full-fact corroboration is distinct from administrative finality and result availability.','Source agreement and index snippets cannot independently verify a fixture.'],
                training_clearance='UNRESOLVED',redistribution_clearance='UNRESOLVED',standardized_rows=0)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--init',action='store_true');p.add_argument('--select',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--output',type=Path);args=p.parse_args()
    if args.init:initialize()
    if args.select:
        r=read(PRIVATE/structural.REPORT);chosen=selection(r['records']);base.save(PRIVATE/SELECTION,base.encode(dict(method='Outcome-stratified minimum SHA256(ligue1-phase5-v1:audit_id), ordinary unflagged only; old H/D, modern H/D/A rotation',ordinary=[binding(x) for x in chosen])))
        for x in chosen:print(x['season'],x['date'],x['home'],x['away'],x['FT'])
    else:
        result=build();raw=base.encode(result);destination=args.output or PRIVATE/OUTPUT
        if args.check:
            if destination.read_bytes()!=raw:raise ValueError('Evidence check not deterministic')
        else:base.save(destination,raw)
        print(json.dumps({k:v for k,v in result.items() if k not in ('fixtures','ordinary_results')},indent=2))
