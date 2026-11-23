"""Offline Phase 7 screened Eredivisie CSV, full observation archive and provenance."""
import argparse
from collections import Counter, defaultdict
from copy import deepcopy
import csv
from datetime import date
import hashlib
import io
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from scripts import decide_eredivisie_policy as policy
from scripts.artifact_io import serialize_csv
from toto_estimator.historical_import import OUTPUT_COLUMNS

ROOT, PRIVATE, base = policy.ROOT, policy.PRIVATE, policy.base
BASELINE = 'phase7_protected_before.json'
NAMES = ('eredivisie_standardized_1990_2026.csv', 'eredivisie_audit_archive_1990_2026.json',
         'eredivisie_exceptions_1990_2026.json', 'eredivisie_standardization_manifest.json')
LEAGUE = 'Eredivisie'
EXPECTED = dict(source_observations=13084,unique_fixture_slots=11016,overlapping_representations=2068,
                dispositions={'COMPLETED_RESULT_CANDIDATE':10939,'NOT_PLAYED':74,'HOLD_OUT':3})


def initialize(directory=PRIVATE,root=ROOT):
    if (directory/BASELINE).exists():return protect(directory,root)
    policy.protect(directory,root);receipt=policy.review.read(directory/'phase6_final_verification.json')
    for n,item in receipt['private_files_before_receipt'].items():
        if base.sha((directory/n).read_bytes())!=item['sha256']:raise ValueError('Approved Phase 6 private entry changed: '+n)
    for n,h in receipt['public_files'].items():
        if base.sha((root/n).read_bytes())!=h:raise ValueError('Approved Phase 6 public entry changed: '+n)
    files={str(p.relative_to(root)):base.sha(p.read_bytes()) for p in directory.rglob('*') if p.is_file()}
    files.update({n:h for n,h in receipt['public_files'].items() if n!='PLANNING_LOG.md'})
    log=(root/'PLANNING_LOG.md').read_bytes()
    base.save(directory/BASELINE,base.encode(dict(files=files,planning_log=dict(bytes=len(log),sha256=base.sha(log)),approval='PHASE7_1990_2026_ONLY')))
    return protect(directory,root)


def protect(directory=PRIVATE,root=ROOT):
    prior=policy.protect(directory,root);saved=policy.review.read(directory/BASELINE)
    if not saved['files'] or saved['approval']!='PHASE7_1990_2026_ONLY':raise ValueError('Invalid Phase 7 approval/baseline')
    for n,h in saved['files'].items():
        if not (root/n).resolve().is_relative_to(root.resolve()) or base.sha((root/n).read_bytes())!=h:raise ValueError('Frozen Phase 2–6 entry changed: '+n)
    log=(root/'PLANNING_LOG.md').read_bytes();prefix=saved['planning_log']
    if len(log)<prefix['bytes'] or base.sha(log[:prefix['bytes']])!=prefix['sha256']:raise ValueError('Planning prefix changed')
    return dict(previous=prior,phase2_6_entries=len(saved['files']))


def standard_id(r):
    return base.sha(json.dumps([LEAGUE,r['season'],r['date'],r['home_team'],r['away_team']],ensure_ascii=False,separators=(',',':')).encode())


def validate_source(r):
    y=int(r['season'][:4])
    if not 1990<=y<=2025 or r['season']!=f'{y}/{y+1}':raise ValueError('Source outside approved season scope')
    if r['stage'] not in {'REGULAR_SEASON','HISTORICAL_TIER1_STAGE_NOT_EXPLICIT'}:raise ValueError('Unapproved competition/stage')
    if r['source'].startswith('jalapic/') and r['original_fields']['tier']!='1':raise ValueError('Wrong historical tier')
    if not date(y,7,1)<=policy.day(r['date'])<=date(y+1,6,30):raise ValueError('Source date outside season')
    for k in ('home','away'):
        if not isinstance(r[k],str) or not r[k] or r[k]!=r[k].strip():raise ValueError('Invalid original team label')
    if r['home']==r['away']:raise ValueError('Identical original opponents')


def prepare(rows,decisions,historical,cases,overlaps):
    lookup={r['audit_id']:r for r in rows}
    if len(lookup)!=len(rows):raise ValueError('Duplicate original source identity')
    expected_groups=policy.review.groups(rows,overlaps);members=defaultdict(list)
    for r in rows:validate_source(r);members[expected_groups[r['audit_id']]].append(r)
    by_members={frozenset(d['source_observation_ids']):d for d in decisions}
    if len(by_members)!=len(decisions) or set(by_members)!={frozenset(r['audit_id'] for r in rs) for rs in members.values()}:raise ValueError('Missing/ambiguous source-to-fixture correspondence')
    plans=[]
    for rs in members.values():
        d=by_members[frozenset(r['audit_id'] for r in rs)];case_keys={historical[r['audit_id']]['assessment']['case_id'] for r in rs if r['audit_id'] in historical and historical[r['audit_id']]['assessment'].get('case_id')}
        if len(case_keys)>1:raise ValueError('Mixed special cases')
        case=cases[next(iter(case_keys))] if case_keys else None
        if policy.decide(rs,historical,case)!=d:raise ValueError('Altered or incorrectly bound Phase 6 decision')
        selected=lookup[d['selected_source_id']];projection=None
        if d['disposition']=='COMPLETED_RESULT_CANDIDATE':
            a=d['approved_values'];y=int(d['season'][:4])
            if a['home']!=selected['home'] or a['away']!=selected['away']:raise ValueError('Unapproved label transformation')
            if not date(y,7,1)<=policy.day(a['date'])<=date(y+1,6,30):raise ValueError('Approved date outside season')
            values=dict(date=a['date'],league=LEAGUE,season=d['season'],home_team=a['home'],away_team=a['away'],home_goals=int(a['hg']),away_goals=int(a['ag']))
            values['match_id']=standard_id(values);projection={k:values[k] for k in OUTPUT_COLUMNS}
        elif d['disposition'] not in {'HOLD_OUT','NOT_PLAYED'}:raise ValueError('Unknown disposition')
        plans.append(dict(originals=deepcopy(rs),decision=deepcopy(d),projection=projection))
    policy.reconcile(rows,decisions)
    return sorted(plans,key=lambda p:p['decision']['fixture_id'])


def convert(plans,directory):
    from scripts.standardize_england_results import convert_rows
    bridge=[]
    for p in plans:
        r=p['projection']
        if r is None:continue
        h,a=r['home_goals'],r['away_goals']
        bridge.append(dict(Date=r['date'],Season=r['season'],HomeTeam=r['home_team'],AwayTeam=r['away_team'],hGoal=str(h),aGoal=str(a),Score=f'{h}-{a}',Result='H' if h>a else 'A' if h<a else 'D',Tier='1',Division=LEAGUE))
    return convert_rows(bridge,directory,league=LEAGUE,tier='1',division_names={int(r['Season'][:4]):LEAGUE for r in bridge})


def parse_standard(raw):
    reader=csv.DictReader(io.StringIO(raw.decode('utf-8')),strict=True)
    if tuple(reader.fieldnames or ())!=OUTPUT_COLUMNS:raise ValueError('Wrong exact eight-column schema/order')
    rows=[]
    for r in reader:
        if None in r or any(v is None or v=='' for v in r.values()):raise ValueError('Malformed CSV record')
        for k in ('home_goals','away_goals'):
            if not r[k].isascii() or not r[k].isdigit() or str(int(r[k]))!=r[k]:raise ValueError('Invalid canonical goals')
            r[k]=int(r[k])
        rows.append(r)
    return rows


def verify_subset(rows,plans):
    projections=[p['projection'] for p in plans if p['projection'] is not None];expected={r['match_id']:r for r in projections}
    if len(expected)!=len(projections):raise ValueError('Match ID collision')
    seen=set();order=[];pairs=set()
    for r in rows:
        if tuple(r)!=OUTPUT_COLUMNS or r['league']!=LEAGUE or r['match_id']!=standard_id(r) or r['match_id'] in seen:raise ValueError('Invalid schema/league/ID')
        if expected.get(r['match_id'])!=r:raise ValueError('Unapproved result or HOLD OUT/NOT PLAYED leakage')
        pair=(r['season'],r['home_team'],r['away_team'])
        if pair in pairs:raise ValueError('Duplicate directed fixture')
        pairs.add(pair);seen.add(r['match_id']);order.append(tuple(r[k] for k in ('league','season','date','home_team','away_team')))
    if seen!=expected.keys() or order!=sorted(order):raise ValueError('Lost record or nondeterministic sorting')
    counts=Counter(p['decision']['disposition'] for p in plans)
    if len(rows)+counts['HOLD_OUT']+counts['NOT_PLAYED']!=len(plans):raise ValueError('Unique disposition reconciliation failed')
    return dict(screened=len(rows),hold_out=counts['HOLD_OUT'],not_played=counts['NOT_PLAYED'],unique_fixtures=len(plans))


def prior_ids(directory=PRIVATE,root=ROOT):
    saved=policy.review.read(directory/'protected_before.json')['private'];ids=set();files=[];leagues=set()
    for name,h in sorted(saved.items()):
        if not name.endswith('.csv'):continue
        raw=(root/name).read_bytes()
        if raw.splitlines()[0].lstrip(b'\xef\xbb\xbf')!=','.join(OUTPUT_COLUMNS).encode():continue
        if base.sha(raw)!=h:raise ValueError('Previous standardized data changed: '+name)
        rows=list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))
        for r in rows:
            if not r['match_id'] or r['league']==LEAGUE:raise ValueError('Unexpected previous ID/league')
            ids.add(r['match_id']);leagues.add(r['league'])
        files.append(dict(path=name,records=len(rows),sha256=h,leagues=sorted({r['league'] for r in rows})))
    if not files or len(leagues)!=10:raise ValueError('Expected ten prior competitions for collision checking: '+repr(sorted(leagues)))
    return ids,files,sorted(leagues)


def archive_records(plans,directory):
    cache={};records=[]
    for p in plans:
        d=p['decision'];projection=p['projection']
        for r in p['originals']:
            if r['source'] not in cache:
                raw=(directory/r['source']).read_bytes();blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
                if base.sha(raw)!=r['source_sha256'] or blob!=r['provenance']['git_blob_sha1']:raise ValueError('Original source SHA/blob mismatch')
                cache[r['source']]=raw.splitlines(keepends=True)
            literal=b''.join(cache[r['source']][r['source_line']-1:r['source_end_line']])
            if base.sha(literal)!=r['physical_record_sha256']:raise ValueError('Physical source record differs')
            selected=r['audit_id']==d['selected_source_id'];included=projection is not None
            changes=[]
            if included and selected:
                changes=['Shared eight-column projection; numeric goals; original selected labels retained']
                if r['date']!=projection['date']:changes.append('Exact approved Groningen–Ajax completion-date interpretation; original date preserved')
            records.append(dict(audit_id=r['audit_id'],original=deepcopy(r),literal_original_record=literal.decode('utf-8-sig'),
                 source_provenance=deepcopy(r['provenance']),original_competition_context=dict(league=LEAGUE,stage=r['stage'],tier=r.get('original_fields',{}).get('tier'),source_title='Holland tier-1 CSV' if r['source'].startswith('jalapic/') else 'Netherlands Eredivisie '+r['season']),
                 fixture_id=d['fixture_id'],decision_id=d['decision_id'],source_role='SELECTED' if selected else 'NONSELECTED_OVERLAP_RETAINED',
                 fixture_disposition=d['disposition'],selected_for_csv=selected and included,
                 approved_standardized_values=deepcopy(projection),screened_match_id=None if projection is None else projection['match_id'],
                 chronology=deepcopy(d['chronology']),historical_confidence=d['historical_confidence'][r['audit_id']],
                 historical_review=deepcopy(d['historical_reviews'].get(r['audit_id'])),evidence_ids=d['evidence_ids'],
                 transformations=changes,source_coverage=dict(historical_absence=d['policy']=='UNPLAYED_2019_20',modern_explicit_null_cancellation=r['FT'] is None and r['annotation']=='[cancelled]'),
                 training_authorized=False))
    return sorted(records,key=lambda r:r['audit_id'])


def verify_archive(records,plans):
    originals={r['audit_id']:r for p in plans for r in p['originals']};lookup={r['audit_id']:r for r in records}
    if len(originals)!=len(records) or len(lookup)!=len(records) or set(lookup)!=set(originals):raise ValueError('Archive lost/duplicated source observations')
    by_fixture={p['decision']['fixture_id']:p for p in plans}
    for key,record in lookup.items():
        if record['original']!=originals[key]:raise ValueError('Original source values changed in archive')
        plan=by_fixture.get(record['fixture_id'])
        if plan is None or key not in plan['decision']['source_observation_ids'] or record['decision_id']!=plan['decision']['decision_id']:raise ValueError('Invalid archive source/fixture/decision linkage')
        if record['approved_standardized_values']!=plan['projection'] or record['fixture_disposition']!=plan['decision']['disposition']:raise ValueError('Archive decision/projection differs')
        if record['selected_for_csv']!=(plan['projection'] is not None and key==plan['decision']['selected_source_id']):raise ValueError('Archive selected-source role differs')
        if plan['projection'] is None and record['screened_match_id'] is not None:raise ValueError('Noncandidate match ID leakage')
    return dict(archived=len(records),source_dispositions=dict(Counter(r['fixture_disposition'] for r in records)),selected_for_csv=sum(r['selected_for_csv'] for r in records))


def build(directory=PRIVATE,root=ROOT):
    protected=protect(directory,root);approved=policy.build(directory,root)
    for n,obj in approved.items():
        if base.encode(obj)!=(directory/n).read_bytes():raise ValueError('Approved Phase 6 policy no longer reproduces: '+n)
    structure=policy.review.structure
    h=policy.review.read(directory/structure.NAMES[0]);m=policy.review.read(directory/structure.NAMES[1]);o=policy.review.read(directory/structure.NAMES[2])
    originals=[r for r in h['all_source_records'] if 1990<=int(r['season'][:4])<=2024]+m['records']
    decisions=approved[policy.NAMES[1]]['records'];counts=policy.reconcile(originals,decisions)
    if counts!=EXPECTED:raise ValueError('Approved accounting differs; STOP before output generation: '+repr(counts))
    source_policy={r['original']['audit_id']:r for r in approved[policy.NAMES[0]]['records']}
    if len(source_policy)!=len(originals) or any(source_policy[r['audit_id']]['original']!=policy.binding(r) for r in originals):raise ValueError('Source policy bindings differ')
    registry=policy.review.read(directory/policy.review.OUTPUTS[0]);historical={r['original']['audit_id']:r for r in registry['records']}
    evidence=policy.review.read(directory/'phase5_research_inputs.json');cases={r['id']:r for r in evidence['special_cases']}
    plans=prepare(originals,decisions,historical,cases,o['overlaps'])
    prior,files,leagues=prior_ids(directory,root)
    with TemporaryDirectory(prefix='eredivisie-phase7-import-') as tmp:
        raw,import_summary=convert(plans,Path(tmp));reverse,_=convert(list(reversed(plans)),Path(tmp))
    if raw!=reverse:raise ValueError('Shared importer depends on input order')
    rows=parse_standard(raw);screened=verify_subset(rows,plans)
    if len(rows)!=counts['dispositions']['COMPLETED_RESULT_CANDIDATE']:raise ValueError('Unexpected screened count')
    if serialize_csv(rows,OUTPUT_COLUMNS)!=raw:raise ValueError('CSV serialization roundtrip differs')
    if prior & {r['match_id'] for r in rows}:raise ValueError('Cross-competition ID collision')
    archived=archive_records(plans,directory);archival=verify_archive(archived,plans)
    if archival['source_dispositions']!={'COMPLETED_RESULT_CANDIDATE':13005,'HOLD_OUT':5,'NOT_PLAYED':74} or archival['selected_for_csv']!=len(rows):raise ValueError('Unexpected source-level accounting')
    unique=[dict(approved_decision=deepcopy(p['decision']),approved_standardized_values=deepcopy(p['projection']),screened_match_id=None if p['projection'] is None else p['projection']['match_id']) for p in plans]
    archive=dict(phase=7,league=LEAGUE,counts=dict(**counts,**archival,screened=len(rows)),records=archived,unique_fixtures=unique,
                 source_context=dict(historical_receipt=h['receipt'],modern_receipts=m['receipts'],modern_source_notes=m['source_notes']),
                 scheduling_and_identity=approved[policy.NAMES[2]]['preserved_phase5_contexts'],historical_review_registry=registry,
                 evidence_inventory=policy.review.read(directory/'phase5_evidence_inventory.json'),
                 source_correspondences=approved[policy.NAMES[2]]['overlap_correspondences'],
                 warning='Complete archive includes comparator, HOLD OUT and NOT PLAYED observations; not model-training data',
                 historical_certification='NOT_DATASET_WIDE',rights='Redistribution/model-training permission unresolved; no publication authorized')
    exceptions=dict(phase=7,league=LEAGUE,counts=archive['counts'],unique_exception_fixtures=[x for x in unique if x['approved_decision']['policy']!='ORDINARY_SOURCE_CANDIDATE'],
                    source_exception_observations=[x for x in archived if x['fixture_disposition']!='COMPLETED_RESULT_CANDIDATE' or source_policy[x['audit_id']]['policy'] in policy.CASES],
                    approved_source_selection=approved[policy.NAMES[2]],evidence_inventory=archive['evidence_inventory'],
                    historical_confidence='Frozen 18 fully corroborated /196 partial /1 contradicted /237 unresolved source-observation classifications preserved; no automatic exclusions',
                    chronology='Use integrity-verified Phase6 PredictionGate. Ordinary CSV dates may be proxies; CSV alone is not leakage-safe.',training_authorized=False)
    outputs={NAMES[0]:raw,NAMES[1]:base.encode(archive),NAMES[2]:base.encode(exceptions)}
    code=['scripts/standardize_eredivisie_results.py','tests/test_eredivisie_standardization.py','scripts/decide_eredivisie_policy.py','scripts/verify_eredivisie_review.py','scripts/validate_eredivisie_structure.py','scripts/standardize_england_results.py','scripts/artifact_io.py','src/toto_estimator/historical_import.py']
    inputs=[BASELINE,*policy.NAMES,*structure.NAMES,*policy.review.OUTPUTS,'phase5_evidence_inventory.json','phase5_research_inputs.json']
    manifest=dict(phase=7,league=LEAGUE,schema=list(OUTPUT_COLUMNS),counts=archive['counts'],screened_counts=screened,
                  coverage=approved[policy.NAMES[4]]['season_dispositions'],shared_import_summary=import_summary,protected=protected,
                  source_documents={r['source']:dict(sha256=r['source_sha256'],**r['provenance']) for r in originals},
                  inputs={n:base.sha((directory/n).read_bytes()) for n in inputs},code={n:base.sha((root/n).read_bytes()) for n in code},
                  prior_standardized_files_checked=files,prior_competitions=leagues,prior_unique_ids=len(prior),prior_collisions=0,
                  numeric_goal_outcomes=dict(Counter('H' if r['home_goals']>r['away_goals'] else 'A' if r['home_goals']<r['away_goals'] else 'D' for r in rows)),
                  outputs={n:dict(bytes=len(data),sha256=base.sha(data)) for n,data in outputs.items()},
                  historical_certification='NOT_DATASET_WIDE',training_authorized=False,licensing_clearance='UNRESOLVED')
    outputs[NAMES[3]]=base.encode(manifest);protect(directory,root)
    return outputs


def main():
    parser=argparse.ArgumentParser(description=__doc__);mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--init',action='store_true');mode.add_argument('--write',action='store_true');mode.add_argument('--check',action='store_true')
    parser.add_argument('--output-directory',type=Path,default=PRIVATE);args=parser.parse_args()
    if args.init:print(initialize());return
    outputs=build()
    for n,raw in outputs.items():
        target=args.output_directory/n
        if target.exists() and target.read_bytes()!=raw:raise ValueError('Refusing to overwrite changed output: '+n)
        if args.check and not target.exists():raise ValueError('Missing output: '+n)
    if args.write:
        for n,raw in outputs.items():
            if not (args.output_directory/n).exists():base.save(args.output_directory/n,raw)
    for n,raw in outputs.items():print(n,len(raw),base.sha(raw))


if __name__=='__main__':main()
