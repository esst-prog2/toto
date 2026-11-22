"""Phase 7 offline Ligue 2 screened CSV and complete source audit archive."""
import argparse
from collections import Counter
from copy import deepcopy
import csv
from datetime import date
import hashlib
import io
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from scripts import decide_ligue2_policy as policy
from scripts.artifact_io import serialize_csv
from toto_estimator.historical_import import OUTPUT_COLUMNS

ROOT, PRIVATE, base = policy.ROOT, policy.PRIVATE, policy.base
BASELINE='phase7_protected_before.json'
NAMES=('ligue_2_standardized_2014_2025.csv','ligue_2_audit_archive_2014_2025.json','ligue_2_exceptions_2014_2025.json','ligue_2_standardization_manifest.json')
LEAGUE='Ligue 2'


def initialize(directory=PRIVATE,root=ROOT):
    if (directory/BASELINE).exists():return protect(directory,root)
    policy.protect(directory,root);receipt=policy.review.read(directory/'phase6_final_verification.json')
    for n,item in receipt['private_files_before_receipt'].items():
        if base.sha((directory/n).read_bytes())!=item['sha256']:raise ValueError('Phase 6 evidence changed: '+n)
    for n,digest in receipt['public_files'].items():
        if base.sha((root/n).read_bytes())!=digest:raise ValueError('Phase 6 public work changed: '+n)
    files={str(p.relative_to(root)):base.sha(p.read_bytes()) for p in directory.rglob('*') if p.is_file()}
    files.update({n:h for n,h in receipt['public_files'].items() if n!='PLANNING_LOG.md'})
    log=(root/'PLANNING_LOG.md').read_bytes()
    base.save(directory/BASELINE,base.encode(dict(files=files,planning_log=dict(bytes=len(log),sha256=base.sha(log)),approval='USER_APPROVED_PHASE7_2014_2025_ONLY')))
    return protect(directory,root)


def protect(directory=PRIVATE,root=ROOT):
    previous=policy.protect(directory,root);saved=policy.review.read(directory/BASELINE)
    if not saved['files'] or saved['approval']!='USER_APPROVED_PHASE7_2014_2025_ONLY':raise ValueError('Missing approval/baseline')
    for n,h in saved['files'].items():
        if not (root/n).resolve().is_relative_to(root.resolve()) or base.sha((root/n).read_bytes())!=h:raise ValueError('Frozen Phase 2–6 entry changed: '+n)
    log=(root/'PLANNING_LOG.md').read_bytes();prefix=saved['planning_log']
    if len(log)<prefix['bytes'] or base.sha(log[:prefix['bytes']])!=prefix['sha256']:raise ValueError('Planning history changed')
    return dict(previous=previous,phase2_6_entries=len(saved['files']))


def standard_id(row):
    return base.sha(json.dumps([LEAGUE,row['season'],row['date'],row['home_team'],row['away_team']],ensure_ascii=False,separators=(',',':')).encode())


def prepare(records,decisions,historical,cases):
    byid={x['original']['audit_id']:x for x in decisions}
    if len(byid)!=len(decisions) or set(byid)!={r['audit_id'] for r in records} or len({r['audit_id'] for r in records})!=len(records):raise ValueError('Ambiguous/missing source decision mapping')
    locations=set();pairs=set();plans=[]
    for r in records:
        key=r['audit_id'];d=byid[key]
        if d!=policy.decide(r,historical.get(key),cases.get(key)):raise ValueError('Altered or incorrectly bound policy decision')
        y=int(r['season'][:4])
        if r['season']!=f'{y}/{y+1}' or not 2014<=y<=2024 or r['stage']!='REGULAR_SEASON':raise ValueError('Unapproved season/stage')
        if not date(y,7,1)<=policy.day(r['date'])<=date(y+1,6,30):raise ValueError('Date outside season')
        for team in (r['home'],r['away']):
            if not isinstance(team,str) or not team or team!=team.strip():raise ValueError('Invalid team label')
        if r['home']==r['away']:raise ValueError('Identical opponents')
        location=(r['source'],r['source_line']);pair=(r['season'],r['home'],r['away'])
        if location in locations or pair in pairs:raise ValueError('Duplicate source or directed fixture')
        locations.add(location);pairs.add(pair);projection=None
        if d['disposition']=='COMPLETED_RESULT_CANDIDATE':
            c=d['chronology'];effective=c['effective_result_availability_date'] if c['date_interpretation']=='APPROVED_ACTUAL_COMPLETION_DAY' else c['proxy_date']
            if effective is None or not date(y,7,1)<=policy.day(effective)<=date(y+1,6,30):raise ValueError('Invalid projection date')
            fields=dict(date=effective,league=LEAGUE,season=r['season'],home_team=r['home'],away_team=r['away'],home_goals=int(r['hg']),away_goals=int(r['ag']))
            projection={k:({'match_id':standard_id(fields),**fields})[k] for k in OUTPUT_COLUMNS}
        elif d['disposition'] not in {'ADMINISTRATIVE_HOLD_OUT','NOT_PLAYED'}:raise ValueError('Unknown disposition')
        plans.append(dict(original=r,decision=d,projection=projection))
    return plans


def convert(plans,directory):
    from scripts.standardize_england_results import convert_rows
    bridge=[]
    for p in plans:
        r=p['projection']
        if r is None:continue
        h,a=r['home_goals'],r['away_goals']
        bridge.append(dict(Date=r['date'],Season=r['season'],HomeTeam=r['home_team'],AwayTeam=r['away_team'],hGoal=str(h),aGoal=str(a),Score=f'{h}-{a}',Result='H' if h>a else 'A' if h<a else 'D',Tier='2',Division=LEAGUE))
    return convert_rows(bridge,directory,league=LEAGUE,tier='2',division_names={int(r['Season'][:4]):LEAGUE for r in bridge})


def parse_standard(raw):
    reader=csv.DictReader(io.StringIO(raw.decode('utf-8')),strict=True)
    if tuple(reader.fieldnames or ())!=OUTPUT_COLUMNS:raise ValueError('Wrong exact schema/order')
    rows=[]
    for r in reader:
        if None in r or any(v is None or v=='' for v in r.values()):raise ValueError('Malformed CSV row')
        for k in ('home_goals','away_goals'):
            v=r[k]
            if not v.isascii() or not v.isdigit() or str(int(v))!=v:raise ValueError('Invalid canonical goals')
            r[k]=int(v)
        rows.append(r)
    return rows


def verify_subset(rows,plans):
    expected=[p['projection'] for p in plans if p['projection'] is not None];byid={r['match_id']:r for r in expected}
    if len(byid)!=len(expected):raise ValueError('Expected ID collision')
    seen=set();order=[]
    for r in rows:
        if tuple(r)!=OUTPUT_COLUMNS or r['league']!=LEAGUE or r['match_id']!=standard_id(r) or r['match_id'] in seen:raise ValueError('Invalid schema, league or deterministic ID')
        if byid.get(r['match_id'])!=r:raise ValueError('Unapproved source facts or excluded match in output')
        seen.add(r['match_id']);order.append(tuple(r[k] for k in ('league','season','date','home_team','away_team')))
    if seen!=byid.keys() or order!=sorted(order):raise ValueError('Lost record or unstable ordering')
    counts=Counter(p['decision']['disposition'] for p in plans)
    if len(rows)+counts['ADMINISTRATIVE_HOLD_OUT']+counts['NOT_PLAYED']!=len(plans):raise ValueError('Nonexclusive reconciliation')
    return dict(archived=len(plans),screened=len(rows),administrative_hold_out=counts['ADMINISTRATIVE_HOLD_OUT'],not_played=counts['NOT_PLAYED'],other_hold_out=0,other_exclusions=0)


def prior_ids(root,directory):
    baseline=policy.review.read(directory/'protected_before.json')['private'];ids=set();files=[]
    for name in sorted(baseline):
        if not name.endswith('.csv'):continue
        with (root/name).open(encoding='utf-8-sig',newline='') as f:
            reader=csv.DictReader(f)
            if tuple(reader.fieldnames or ())!=OUTPUT_COLUMNS:continue
            rows=list(reader)
        if base.sha((root/name).read_bytes())!=baseline[name]:raise ValueError('Prior dataset changed')
        ids.update(r['match_id'] for r in rows);files.append(dict(path=name,records=len(rows),sha256=baseline[name]))
    if not ids or not files:raise ValueError('Missing previous competition collision check')
    return ids,files


def archive_records(plans,directory):
    lines={};records=[]
    for p in sorted(plans,key=lambda p:p['original']['audit_id']):
        r=p['original'];source=r['source']
        if source not in lines:
            raw=(directory/source).read_bytes();blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
            if base.sha(raw)!=r['source_sha256'] or blob!=r['provenance']['git_blob_sha1']:raise ValueError('Source SHA/blob differs')
            lines[source]=raw.splitlines(keepends=True)
        literal=lines[source][r['source_line']-1]
        if base.sha(literal)!=r['physical_line_sha256'] or literal.decode('utf-8-sig').rstrip('\r\n')!=r['raw_record']:raise ValueError('Physical record binding differs')
        included=p['projection'] is not None
        records.append(dict(audit_id=r['audit_id'],original=deepcopy(r),literal_original_record=literal.decode('utf-8-sig'),source_url=r['provenance']['url'],pinned_revision=r['provenance']['commit'],git_blob_sha1=r['provenance']['git_blob_sha1'],source_sha256=r['source_sha256'],source_document=source,source_line=r['source_line'],physical_line_sha256=r['physical_line_sha256'],approved_decision=deepcopy(p['decision']),chronology=deepcopy(p['decision']['chronology']),provisional_disposition=p['decision']['disposition'],final_processing_disposition='INCLUDED' if included else p['decision']['disposition'],approved_standardized_values=deepcopy(p['projection']),screened_match_id=p['projection']['match_id'] if included else None,transformations=['Schema projection and goal strings to integers; original labels and source date unchanged'] if included else [],historical_certification='NOT_CLAIMED',training_authorized=False))
    return records


def build(directory=PRIVATE,root=ROOT):
    protected=protect(directory,root)
    # Fresh raw parsing precedes projection: frozen saved totals are not trusted.
    report,queue=policy.review.structure.build(directory,root)
    for name,obj in [(policy.review.structure.REPORT,report),(policy.review.structure.QUEUE,queue)]:
        if (directory/name).read_bytes()!=base.encode(obj):raise ValueError('Raw structural reconciliation changed')
    approved=policy.build(directory,root)
    for name,obj in approved.items():
        if (directory/name).read_bytes()!=base.encode(obj):raise ValueError('Approved policy no longer reproduces')
    historical=policy.review.read(directory/policy.review.REGISTRY);h={r['audit_id']:r for r in historical['fixtures']}
    review_result=policy.review.read(directory/policy.review.OUTPUT);cases={r['original']['audit_id']:r for r in review_result['special_cases']}
    plans=prepare(report['records'],approved[policy.REGISTRY]['decisions'],h,cases)
    with TemporaryDirectory(prefix='ligue2-standardization-') as tmp:
        raw,summary=convert(plans,Path(tmp));repeat,_=convert(list(reversed(plans)),Path(tmp))
    if raw!=repeat:raise ValueError('Input-order dependent importer')
    rows=parse_standard(raw);counts=verify_subset(rows,plans)
    if serialize_csv(rows,OUTPUT_COLUMNS)!=raw:raise ValueError('CSV roundtrip differs')
    if counts!=dict(archived=4106,screened=4003,administrative_hold_out=3,not_played=100,other_hold_out=0,other_exclusions=0):raise ValueError('Unexpected reconciliation; stop')
    prior,files=prior_ids(root,directory)
    if prior & {r['match_id'] for r in rows}:raise ValueError('Cross-competition match ID collision')
    records=archive_records(plans,directory)
    if len(records)!=len(report['records']) or len({r['audit_id'] for r in records})!=len(records):raise ValueError('Lost/duplicate archive observation')
    included=[r['approved_standardized_values'] for r in records if r['final_processing_disposition']=='INCLUDED']
    if {r['match_id']:r for r in included}!={r['match_id']:r for r in rows}:raise ValueError('Archive subset differs')
    if any(r['screened_match_id'] is not None for r in records if r['final_processing_disposition']!='INCLUDED'):raise ValueError('Excluded record ID leakage')
    archive=dict(league=LEAGUE,counts=counts,records=records,wide_rounds=review_result['wide_rounds'],reversal_pairs=review_result['reversals'],identity_review=review_result['identity_review'],historical_registry=historical,warning='Contains NOT PLAYED and HOLD OUT; not training data',rights=report['rights'])
    exceptions=dict(league=LEAGUE,counts=counts,exception_records=[r for r in records if r['final_processing_disposition']!='INCLUDED' or r['audit_id'] in policy.SPECS],scheduling_context=approved[policy.EXCEPTIONS],coverage=review_result['coverage'],evidence_inventory=policy.review.read(directory/policy.review.REFERENCES),chronological_rule='Use policy.eligible_for_prediction with bound source/evidence; verified availability strictly before prediction day. CSV dates may be proxies.',training_authorized=False,rights=report['rights'])
    outputs={NAMES[0]:raw,NAMES[1]:base.encode(archive),NAMES[2]:base.encode(exceptions)}
    coverage=[]
    for y in range(2014,2025):
        rs=[r for r in records if r['original']['season']==f'{y}/{y+1}'];coverage.append(dict(season=f'{y}/{y+1}',archived=len(rs),screened=sum(r['final_processing_disposition']=='INCLUDED' for r in rs),administrative_hold_out=sum(r['final_processing_disposition']=='ADMINISTRATIVE_HOLD_OUT' for r in rs),not_played=sum(r['final_processing_disposition']=='NOT_PLAYED' for r in rs)))
    code=['scripts/standardize_ligue2_results.py','tests/test_ligue2_standardization.py','scripts/decide_ligue2_policy.py','scripts/verify_ligue2_review.py','scripts/validate_ligue2_structure.py','scripts/standardize_england_results.py','scripts/artifact_io.py','src/toto_estimator/historical_import.py']
    inputs=[BASELINE,policy.REGISTRY,policy.EXCEPTIONS,policy.SUMMARY,policy.MANIFEST,policy.review.REFERENCES,policy.review.LEDGER,policy.review.REGISTRY,policy.review.OUTPUT,policy.review.structure.REPORT,policy.review.structure.QUEUE]
    manifest=dict(league=LEAGUE,schema=list(OUTPUT_COLUMNS),counts=counts,coverage=coverage,shared_import_summary=summary,protected=protected,inputs={n:base.sha((directory/n).read_bytes()) for n in inputs},code={n:base.sha((root/n).read_bytes()) for n in code},source_documents={r['source']:dict(sha256=r['source_sha256'],**r['provenance']) for r in report['records']},prior_standardized_files_checked=files,prior_unique_ids=len(prior),prior_collisions=0,numeric_goal_outcomes=dict(Counter('H' if r['home_goals']>r['away_goals'] else 'A' if r['home_goals']<r['away_goals'] else 'D' for r in rows)),coverage_gaps=review_result['coverage'],historical_certification='NOT_CLAIMED',training_authorized=False,licensing_clearance='UNRESOLVED',outputs={n:dict(bytes=len(raw),sha256=base.sha(raw)) for n,raw in outputs.items()})
    outputs[NAMES[3]]=base.encode(manifest);protect(directory,root)
    return outputs


def main():
    parser=argparse.ArgumentParser(description=__doc__);mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--init',action='store_true');mode.add_argument('--write',action='store_true');mode.add_argument('--check',action='store_true');parser.add_argument('--output-directory',type=Path,default=PRIVATE);args=parser.parse_args()
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
