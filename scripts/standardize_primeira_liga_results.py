"""Offline Phase 7 screened Primeira Liga CSV, full observation archive and provenance."""
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
from scripts import decide_primeira_liga_policy as policy
from scripts.artifact_io import serialize_csv
from toto_estimator.historical_import import OUTPUT_COLUMNS

ROOT, PRIVATE, base = policy.ROOT, policy.PRIVATE, policy.c
BASELINE = 'phase7_protected_before.json'
NAMES = ('primeira_liga_standardized_1994_2026.csv', 'primeira_liga_audit_archive_1994_2026.json',
         'primeira_liga_exceptions_1994_2026.json', 'primeira_liga_standardization_manifest.json')
LEAGUE = 'Primeira Liga'
EXPECTED = dict(source_observations=11406,unique_fixture_slots=9264,overlap_representations=2142,
                dispositions={'COMPLETED_RESULT_CANDIDATE':9262,'HOLD_OUT':2},
                source_dispositions={'COMPLETED_RESULT_CANDIDATE':11403,'HOLD_OUT':3})


def initialize(directory=PRIVATE,root=ROOT):
    if (directory/BASELINE).exists():return protect(directory,root)
    policy.protect(directory,root);receipt=policy.read(directory/'phase6_final_verification.json')
    for n,item in receipt['private_files_before_receipt'].items():
        if base.sha((directory/n).read_bytes())!=item['sha256']:raise ValueError('Approved Phase 6 private entry changed: '+n)
    for n,h in receipt['public_files'].items():
        if base.sha((root/n).read_bytes())!=h:raise ValueError('Approved Phase 6 public entry changed: '+n)
    files={str(p.relative_to(root)):base.sha(p.read_bytes()) for p in directory.rglob('*') if p.is_file()}
    files.update({n:h for n,h in receipt['public_files'].items() if n!='PLANNING_LOG.md'})
    log=(root/'PLANNING_LOG.md').read_bytes()
    base.save(directory/BASELINE,base.encode(dict(files=files,planning_log=dict(bytes=len(log),sha256=base.sha(log)),approval='PHASE7_1994_2026_ONLY')))
    return protect(directory,root)


def protect(directory=PRIVATE,root=ROOT):
    prior=policy.protect(directory,root);saved=policy.read(directory/BASELINE)
    if not saved['files'] or saved['approval']!='PHASE7_1994_2026_ONLY':raise ValueError('Invalid Phase 7 approval/baseline')
    for n,h in saved['files'].items():
        if not (root/n).resolve().is_relative_to(root.resolve()) or base.sha((root/n).read_bytes())!=h:raise ValueError('Frozen Phase 2–6 entry changed: '+n)
    log=(root/'PLANNING_LOG.md').read_bytes();prefix=saved['planning_log']
    if len(log)<prefix['bytes'] or base.sha(log[:prefix['bytes']])!=prefix['sha256']:raise ValueError('Planning prefix changed')
    return dict(previous=prior,phase2_6_entries=len(saved['files']))


def standard_id(r):
    return base.sha(json.dumps([LEAGUE,r['season'],r['date'],r['home_team'],r['away_team']],ensure_ascii=False,separators=(',',':')).encode())


def validate_source(r):
    y=int(r['season'][:4])
    if not 1994<=y<=2025 or r['season']!=f'{y}/{y+1}':raise ValueError('Source outside approved season scope')
    if r['stage'] not in {'REGULAR_SEASON','HISTORICAL_P1_TIER1_STAGE_NOT_EXPLICIT'}:raise ValueError('Unapproved competition/stage')
    if r['source']==policy.HIST_PATH and (r['original_fields']['tier']!='1' or r['original_fields']['division']!='P1'):raise ValueError('Wrong historical tier/division')
    limit=date(2020,8,2)if y==2019 else date(y+1,6,30)
    if not date(y,7,1)<=policy.day(r['date'])<=limit:raise ValueError('Source date outside season')
    for k in ('home','away'):
        if not isinstance(r[k],str)or not r[k]:raise ValueError('Invalid original team label')
        if r[k]!=r[k].strip()and not(k=='home'and r['audit_id']==policy.SPECS['FEIRENSE_NACIONAL']['rows'][0][0]and r[k]=='Feirense '):raise ValueError('Unapproved original team whitespace')
    if r['home']==r['away']:raise ValueError('Identical original opponents')


def prepare(rows,decisions,historical,flags,references,overlaps):
    lookup={r['audit_id']:r for r in rows}
    if len(lookup)!=len(rows):raise ValueError('Duplicate original source identity')
    groups=policy.review.group_rows(rows,overlaps);members=defaultdict(list)
    for r in rows:validate_source(r);members[groups[r['audit_id']]].append(r)
    by_members={frozenset(d['source_observation_ids']):d for d in decisions}
    if len(by_members)!=len(decisions)or set(by_members)!={frozenset(r['audit_id']for r in rs)for rs in members.values()}:raise ValueError('Missing/ambiguous source-to-fixture correspondence')
    plans=[]
    for rs in members.values():
        d=by_members[frozenset(r['audit_id']for r in rs)]
        if policy.decide(sorted(rs,key=lambda r:r['audit_id']),historical,flags,references)!=d:raise ValueError('Altered or incorrectly bound Phase6 decision')
        selected=lookup[d['selected_source_id']];projection=None
        if d['disposition']=='COMPLETED_RESULT_CANDIDATE':
            a=d['approved_values'];y=int(d['season'][:4]);limit=date(2020,8,2)if y==2019 else date(y+1,6,30)
            if a['FT']!=selected['FT']or a['hg']!=selected['hg']or a['ag']!=selected['ag']:raise ValueError('Unapproved score transformation')
            if a['away']!=selected['away']:raise ValueError('Unapproved away-label transformation')
            if a['home']!=selected['home']and not(d['policy']=='FEIRENSE_NACIONAL'and a['home']=='Feirense'and selected['home']=='Feirense '):raise ValueError('Unapproved home-label transformation')
            if a['date']!=selected['date']and d['policy']not in {'SANTA_PACOS','SANTA_BENFICA'}:raise ValueError('Unapproved date interpretation')
            if not date(y,7,1)<=policy.day(a['date'])<=limit:raise ValueError('Approved date outside season')
            if any(a[k]!=a[k].strip()for k in ['home','away']):raise ValueError('Unapproved projected whitespace')
            values=dict(date=a['date'],league=LEAGUE,season=d['season'],home_team=a['home'],away_team=a['away'],home_goals=int(a['hg']),away_goals=int(a['ag']))
            values['match_id']=standard_id(values);projection={k:values[k]for k in OUTPUT_COLUMNS}
        elif d['disposition']not in {'HOLD_OUT','NOT_PLAYED'}:raise ValueError('Unknown disposition')
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
    saved=policy.read(directory/'protected_before.json')['private'];ids=set();files=[];leagues=set()
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
    if not files or len(leagues)!=11:raise ValueError('Expected eleven prior competitions for collision checking: '+repr(sorted(leagues)))
    return ids,files,sorted(leagues)


def audit_match_ids(value):
    """Reserve explicit match-ID fields, never generic audit/fixture/decision hashes."""
    keys={'match_id','screened_match_id','source_observation_match_id','candidate_match_id'}
    ids=set();occurrences=Counter();stack=[value]
    while stack:
        item=stack.pop()
        if isinstance(item,dict):
            for key,val in item.items():
                if key in keys and isinstance(val,str):
                    if len(val)!=64 or any(c not in '0123456789abcdef'for c in val):raise ValueError('Malformed protected archive match ID')
                    ids.add(val);occurrences[key]+=1
                if isinstance(val,(dict,list)):stack.append(val)
        elif isinstance(item,list):stack.extend(x for x in item if isinstance(x,(dict,list)))
    return ids,dict(sorted(occurrences.items()))


def protected_audit_ids(directory=PRIVATE,root=ROOT):
    saved=policy.read(directory/'protected_before.json')['private'];ids=set();files=[]
    for name,digest in sorted(saved.items()):
        if not name.endswith('.json')or'audit_archive'not in Path(name).name:continue
        path=root/name
        if not path.resolve().is_relative_to(root.resolve()):raise ValueError('Protected archive path escape')
        raw=path.read_bytes()
        if base.sha(raw)!=digest:raise ValueError('Protected archive changed: '+name)
        observed,fields=audit_match_ids(json.loads(raw))
        ids.update(observed);files.append(dict(path=name,sha256=digest,unique_ids=len(observed),field_occurrences=fields))
    return ids,files


def archive_records(plans,directory):
    cache={};records=[]
    for p in plans:
        d=p['decision'];projection=p['projection']
        for r in p['originals']:
            if r['source'] not in cache:
                raw=(directory/r['source']).read_bytes();blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
                if base.sha(raw)!=r['source_sha256'] or blob!=r['provenance']['git_blob_sha1']:raise ValueError('Original source SHA/blob mismatch')
                cache[r['source']]=dict(lines=raw.splitlines(keepends=True),sha256=base.sha(raw),blob=blob)
            source=cache[r['source']]
            if r['source_sha256']!=source['sha256']or r['provenance']['git_blob_sha1']!=source['blob']:raise ValueError('Inconsistent per-observation source hash/blob')
            literal=b''.join(source['lines'][r['source_line']-1:r['source_end_line']])
            if base.sha(literal)!=r['physical_record_sha256']:raise ValueError('Physical source record differs')
            selected=r['audit_id']==d['selected_source_id'];included=projection is not None
            changes=[]
            if included and selected:
                changes=['Shared eight-column projection; numeric goals; selected labels retained except exact approved Feirense interpretation']
                if r['date']!=projection['date']:changes.append('Exact approved '+d['policy']+' completion-date interpretation; original date preserved')
                if r['home']!=projection['home_team']:changes.append('Only exact Feirense line4877 trailing-space interpretation; original literal preserved')
            records.append(dict(audit_id=r['audit_id'],original=deepcopy(r),literal_original_record=literal.decode('utf-8-sig'),
                 source_provenance=deepcopy(r['provenance']),original_competition_context=dict(league=LEAGUE,stage=r['stage'],tier=r.get('original_fields',{}).get('tier'),source_title='Portugal P1 tier-1 CSV' if r['source'].startswith('jalapic/') else 'Portuguese Primeira Liga '+r['season']),
                 fixture_id=d['fixture_id'],decision_id=d['decision_id'],source_role='SELECTED' if selected else 'NONSELECTED_OVERLAP_RETAINED',
                 fixture_disposition=d['disposition'],selected_for_csv=selected and included,
                 approved_standardized_values=deepcopy(projection),screened_match_id=None if projection is None else projection['match_id'],
                 chronology=deepcopy(d['chronology']),historical_confidence=d['historical_reviews'].get(r['audit_id'],{}).get('classification','NOT_IN_BOUNDED_REVIEW'),
                 historical_review=deepcopy(d['historical_reviews'].get(r['audit_id'])),evidence_ids=d['evidence_ids'],
                 transformations=changes,source_receipt_reference=r['source'],administrative_uncertainty=dict(known_unresolved=d['unresolved_administration'],finality=d['administrative_finality']),exception_policy=d['policy'],
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
        if base.encode(obj)!=(directory/n).read_bytes():raise ValueError('Approved Phase6 policy no longer reproduces: '+n)
    structure=policy.review.structure
    h=policy.read(directory/'phase4_historical_structure.json');m=policy.read(directory/'phase4_modern_structure.json');o=policy.read(directory/'phase4_overlap_reconciliation.json')
    originals=[r for season in h['seasons']+m['seasons']for r in season['records']]
    decisions=approved[policy.NAMES[1]]['records'];counts=policy.reconcile(originals,decisions)
    if counts!=EXPECTED:raise ValueError('Approved accounting differs; STOP before standardization: '+repr(counts))
    source_policy={r['original']['audit_id']:r for r in approved[policy.NAMES[0]]['records']}
    if len(source_policy)!=len(originals)or any(source_policy[r['audit_id']]['original']!=r for r in originals):raise ValueError('Source policy bindings differ')
    registry=policy.read(directory/'phase5_review_registry.json');historical={r['original']['audit_id']:r for r in registry['records']}
    evidence=policy.read(directory/'phase5_documentary_evidence_index.json');references={r['evidence_id']:r for r in evidence['references']}
    queue=policy.read(directory/'phase4_review_queue.json');flags={r['original']['audit_id']:r['categories']for r in queue['records']}
    plans=prepare(originals,decisions,historical,flags,references,o)
    prior_csv,files,leagues=prior_ids(directory,root)
    prior_audit,audit_files=protected_audit_ids(directory,root);prior=prior_csv|prior_audit
    with TemporaryDirectory(prefix='primeira-liga-phase7-import-')as tmp:
        raw,import_summary=convert(plans,Path(tmp));reverse,_=convert(list(reversed(plans)),Path(tmp))
    if raw!=reverse:raise ValueError('Shared importer depends on input order')
    rows=parse_standard(raw);screened=verify_subset(rows,plans)
    if len(rows)!=9262:raise ValueError('Unexpected screened count')
    if serialize_csv(rows,OUTPUT_COLUMNS)!=raw:raise ValueError('CSV serialization roundtrip differs')
    verify_collisions(rows,prior)
    archived=archive_records(plans,directory);archival=verify_archive(archived,plans)
    if archival['source_dispositions']!={'COMPLETED_RESULT_CANDIDATE':11403,'HOLD_OUT':3}or archival['selected_for_csv']!=len(rows):raise ValueError('Unexpected source-level accounting')
    unique=[dict(approved_decision=deepcopy(p['decision']),approved_standardized_values=deepcopy(p['projection']),screened_match_id=None if p['projection']is None else p['projection']['match_id'])for p in plans]
    receipts={season['receipt']['path']:season['receipt']for season in h['seasons']+m['seasons']}
    rsssf=next(r for r in policy.read(directory/'acquisition.json')['files']if r['repository']=='RSSSF')
    archive=dict(phase=7,league=LEAGUE,counts=dict(counts,**archival,screened=len(rows)),records=archived,unique_fixtures=unique,
                 source_context=dict(receipts=receipts,modern_source_notes={s['receipt']['path']:s['notes']for s in m['seasons']}),
                 rsssf_result_only_snapshot=dict(receipt=rsssf,result_identities=380,dated_observations=0,in_dated_population=False),
                 scheduling_and_identity=approved[policy.NAMES[3]],historical_review_registry=registry,evidence_inventory=evidence,
                 source_correspondences=approved[policy.NAMES[2]]['overlap_correspondences'],coverage_gap=approved[policy.NAMES[5]]['early_gap'],
                 warning='Complete archive includes retained comparator and HOLD OUT observations; not model-training data',historical_certification='NOT_DATASET_WIDE',rights='Redistribution/model-training permission unresolved; no publication authorized')
    exceptions=dict(phase=7,league=LEAGUE,counts=archive['counts'],unique_exception_fixtures=[x for x in unique if x['approved_decision']['policy']!='ORDINARY_SOURCE_CANDIDATE'],source_exception_observations=[x for x in archived if x['fixture_disposition']!='COMPLETED_RESULT_CANDIDATE'or source_policy[x['audit_id']]['policy']in policy.SPECS],approved_source_selection=approved[policy.NAMES[2]],approved_exception_policies=approved[policy.NAMES[3]],evidence_inventory=evidence,coverage_gap=archive['coverage_gap'],historical_confidence=approved[policy.NAMES[5]]['phase5_source_confidence'],chronology='Use integrity-verified Phase6 PredictionGate; CSV dates may be unverified proxies. Santa Clara-Pacos protest guard unchanged. No expanded eligibility.',training_authorized=False)
    outputs={NAMES[0]:raw,NAMES[1]:base.encode(archive),NAMES[2]:base.encode(exceptions)}
    code=['scripts/standardize_primeira_liga_results.py','tests/test_primeira_liga_standardization.py','scripts/decide_primeira_liga_policy.py','scripts/verify_primeira_liga_review.py','scripts/validate_primeira_liga_structure.py','scripts/standardize_england_results.py','scripts/artifact_io.py','src/toto_estimator/historical_import.py','src/toto_estimator/data.py','src/toto_estimator/validation.py','src/toto_estimator/outcomes.py']
    inputs=[BASELINE,*policy.NAMES,*structure.OUTPUTS,*policy.review.OUTPUTS,'phase5_research_inputs.json']
    manifest=dict(phase=7,league=LEAGUE,schema=list(OUTPUT_COLUMNS),counts=archive['counts'],screened_counts=screened,coverage=approved[policy.NAMES[5]]['season_dispositions'],shared_import_summary=import_summary,protected=protected,
                  source_documents={r['source']:dict(sha256=r['source_sha256'],**r['provenance'])for r in originals},
                  inputs={n:base.sha((directory/n).read_bytes())for n in inputs},code={n:base.sha((root/n).read_bytes())for n in code},
                  prior_standardized_files_checked=files,prior_competitions=leagues,prior_row_instances=sum(f['records']for f in files),prior_csv_unique_ids=len(prior_csv),prior_audit_id_files_checked=audit_files,prior_audit_unique_ids=len(prior_audit),additional_audit_only_ids=len(prior_audit-prior_csv),prior_unique_ids=len(prior),prior_collisions=0,
                  numeric_goal_outcomes=dict(Counter('H'if r['home_goals']>r['away_goals']else'A'if r['home_goals']<r['away_goals']else'D'for r in rows)),
                  outputs={n:dict(bytes=len(data),sha256=base.sha(data))for n,data in outputs.items()},
                  coverage_gap=archive['coverage_gap'],historical_certification='NOT_DATASET_WIDE',training_authorized=False,licensing_clearance='UNRESOLVED')
    outputs[NAMES[3]]=base.encode(manifest);protect(directory,root)
    return outputs


def verify_collisions(rows,prior):
    if prior&{r['match_id']for r in rows}:raise ValueError('Cross-competition ID collision')


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
