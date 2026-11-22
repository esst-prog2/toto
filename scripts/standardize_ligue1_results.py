"""Phase 7 offline screened Ligue 1 CSV and complete provenance archive.

No acquisition, new historical decisions, application integration or training.
"""
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

from scripts import decide_ligue1_policy as policy
from scripts.artifact_io import serialize_csv
from toto_estimator.historical_import import OUTPUT_COLUMNS

ROOT, PRIVATE, base = policy.ROOT, policy.PRIVATE, policy.base
BASELINE='phase7_protected_before.json'
APPROVAL='phase7_approval.json'
POLICY_SHA='c04e6890ddfb8624446fef19b8fde1a3696e80e2973ca399ea5fe34a5f95f605'
LEAGUE='Ligue 1'
NAMES=('ligue_1_standardized_1990_2025.csv','ligue_1_audit_archive_1990_2025.json',
       'ligue_1_exceptions_1990_2025.json','ligue_1_standardization_manifest.json')
PUBLIC=policy.PUBLIC+('scripts/decide_ligue1_policy.py','tests/test_ligue1_policy.py','docs/ligue-1-policy.md')


def initialize(directory=PRIVATE,root=ROOT):
    if (directory/BASELINE).exists():return protect(directory,root)
    policy.preserve(directory,root)
    final=policy.review.read(directory/'phase6_final_verification.json')
    for item in final['new_private_files_before_receipt']:
        if base.sha((directory/item['name']).read_bytes())!=item['sha256']:raise ValueError('Approved Phase 6 private evidence changed')
    for name,digest in final['public_files'].items():
        if base.sha((root/name).read_bytes())!=digest:raise ValueError('Approved Phase 6 public evidence changed')
    files={str(p.relative_to(root)):base.sha(p.read_bytes()) for p in directory.rglob('*') if p.is_file()}
    files.update({n:base.sha((root/n).read_bytes()) for n in PUBLIC})
    log=(root/'PLANNING_LOG.md').read_bytes()
    base.save(directory/BASELINE,base.encode(dict(files=files,planning_log=dict(bytes=len(log),sha256=base.sha(log)))))
    base.save(directory/APPROVAL,base.encode(dict(phase=7,approval='USER_APPROVED_PHASE7',
              phase6_policy_sha256=POLICY_SHA,scope='Acquired 35 represented seasons; five holdouts and 101 NOT PLAYED retained',
              no_gap_supplement=True,no_new_historical_decisions=True)))
    return protect(directory,root)


def protect(directory=PRIVATE,root=ROOT):
    previous=policy.preserve(directory,root);saved=policy.review.read(directory/BASELINE)
    if not saved['files']:raise ValueError('Empty Phase 7 baseline')
    for name,digest in saved['files'].items():
        path=root/name
        if not path.resolve().is_relative_to(root.resolve()) or base.sha(path.read_bytes())!=digest:raise ValueError('Frozen Phase 2–6 artifact changed: '+name)
    prefix=saved['planning_log'];log=(root/'PLANNING_LOG.md').read_bytes()
    if len(log)<prefix['bytes'] or base.sha(log[:prefix['bytes']])!=prefix['sha256']:raise ValueError('Planning history changed')
    return dict(previous=previous,phase2_6_entries=len(saved['files']))


def standard_id(row):
    values=[LEAGUE,row['season'],row['date'],row['home_team'],row['away_team']]
    return base.sha(json.dumps(values,ensure_ascii=False,separators=(',',':')).encode())


def prepare(report,approved,ledger,review_result):
    assessments=policy.evaluate(approved,report,ledger,review_result)
    byid=policy.index_records(report['records']);plans=[];locations=set();pairs=set()
    for assessment in assessments:
        r=byid[assessment['audit_id']];location=(r['source'],r['source_line'])
        if location in locations:raise ValueError('Duplicate physical observation')
        locations.add(location);year=int(r['season'][:4])
        if r['season']!=f'{year}/{year+1}' or not 1990<=year<=2025:raise ValueError('Unapproved season convention/scope')
        if not date(year,7,1)<=policy.day(r['date'])<=date(year+1,6,30):raise ValueError('Source date outside season')
        names=assessment['candidate_identity']
        if any(not isinstance(v,str) or not v or v!=v.strip() for v in names.values()) or names['home']==names['away']:raise ValueError('Invalid team identity')
        pair=(r['season'],names['home'],names['away'])
        if pair in pairs:raise ValueError('Duplicate directed fixture after approved identity rule')
        pairs.add(pair);projection=None
        if assessment['status']=='CANDIDATE_NOT_STANDARDIZED':
            effective=assessment['effective_result_date']
            if effective is None or not date(year,7,1)<=policy.day(effective)<=date(year+1,6,30):raise ValueError('Missing/invalid effective result date')
            outcome=policy.numeric_outcome(r)
            if outcome!=assessment['candidate_outcome']:raise ValueError('Goal-derived outcome differs from policy')
            fields=dict(date=effective,league=LEAGUE,season=r['season'],home_team=names['home'],away_team=names['away'],home_goals=int(r['hg']),away_goals=int(r['ag']))
            projection={k:({'match_id':standard_id(fields),**fields})[k] for k in OUTPUT_COLUMNS}
        elif assessment['status'] not in ('HOLD_OUT','NOT_PLAYED') or assessment['effective_result_date'] is not None or assessment['candidate_outcome'] is not None:
            raise ValueError('Restricted observation silently resolved')
        plans.append(dict(original=r,assessment=assessment,projection=projection))
    return plans


def convert(plans,directory):
    from scripts.standardize_england_results import convert_rows
    bridge=[]
    for item in plans:
        r=item['projection']
        if r is None:continue
        h,a=r['home_goals'],r['away_goals']
        bridge.append(dict(Date=r['date'],Season=r['season'],HomeTeam=r['home_team'],AwayTeam=r['away_team'],
                           hGoal=str(h),aGoal=str(a),Score=f'{h}-{a}',Result='H' if h>a else 'A' if h<a else 'D',Tier='1',Division=LEAGUE))
    return convert_rows(bridge,directory,league=LEAGUE,tier='1',division_names={int(r['Season'][:4]):LEAGUE for r in bridge})


def parse_standard(raw):
    reader=csv.DictReader(io.StringIO(raw.decode('utf-8')),strict=True)
    if tuple(reader.fieldnames or ())!=OUTPUT_COLUMNS:raise ValueError('Wrong eight-column schema/order')
    rows=[]
    for row in reader:
        if None in row or any(v is None or v=='' for v in row.values()):raise ValueError('Missing/malformed standardized field')
        for key in ('home_goals','away_goals'):
            value=row[key]
            if not value.isascii() or not value.isdigit() or str(int(value))!=value:raise ValueError('Noncanonical goal type')
            row[key]=int(value)
        rows.append(row)
    return rows


def verify_subset(rows,report,approved,ledger,review_result):
    plans=prepare(report,approved,ledger,review_result) # recompute independently of importer
    expected={p['projection']['match_id']:p['projection'] for p in plans if p['projection'] is not None}
    if len(expected)!=sum(p['projection'] is not None for p in plans):raise ValueError('Expected match ID collision')
    ids=set();order=[]
    for row in rows:
        if tuple(row)!=OUTPUT_COLUMNS or row['league']!=LEAGUE:raise ValueError('Wrong standardized fields/league')
        identifier=row['match_id']
        if identifier in ids or identifier!=standard_id(row):raise ValueError('Invalid/duplicate deterministic ID')
        if expected.get(identifier)!=row:raise ValueError('Unapproved facts or restricted observation entered CSV')
        ids.add(identifier);order.append(tuple(row[k] for k in ('league','season','date','home_team','away_team')))
    if ids!=set(expected):raise ValueError('Screened subset lost observations')
    if order!=sorted(order):raise ValueError('Noncanonical row order')
    counts=Counter(p['assessment']['status'] for p in plans)
    if len(rows)+counts['HOLD_OUT']+counts['NOT_PLAYED']!=len(plans):raise ValueError('Reconciliation failed')
    return plans,dict(archived=len(plans),screened=len(rows),administrative_holdouts=sum(p['assessment']['decision'].startswith('HOLD_OUT_ADMIN') for p in plans),
                      disputed_date_holdouts=sum(p['assessment']['decision']=='HOLD_OUT_DATE_DISPUTE' for p in plans),
                      hold_out=counts['HOLD_OUT'],not_played=counts['NOT_PLAYED'],other_excluded=0)


def provenance(directory):
    first=policy.review.read(directory/'acquisition.json');later=policy.review.read(directory/'phase3_acquisition.json')
    entries=[e for e in first['files'] if e['kind']=='dataset']+later['acquired'];documents={}
    for entry in entries:
        path=entry['path'];raw=(directory/path).read_bytes();blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        if path in documents or base.sha(raw)!=entry['sha256'] or len(raw)!=entry['bytes'] or blob!=entry['git_blob_sha1']:raise ValueError('Source receipt/hash/blob mismatch')
        if entry['url']!=f'https://raw.githubusercontent.com/{entry["repository"]}/{entry["commit"]}/{entry["original_path"]}':raise ValueError('Source URL/revision inconsistent')
        documents[path]=deepcopy(entry)
    if len(documents)!=14:raise ValueError('Original source inventory changed')
    return documents,first['rights']


def archive_records(plans,approved,ledger,documents,directory):
    lines={name:(directory/name).read_bytes().splitlines(keepends=True) for name in documents}
    decisions={c['audit_id']:c for c in approved['decisions']}
    claims={c['audit_id']:c for c in ledger['fixtures']};rounds=defaultdict(list);identities=defaultdict(list)
    for w in ledger['rounds']:
        for identifier in w['affected_ids']:
            rounds[identifier].append({k:deepcopy(w[k]) for k in ('season','round','status','evidence_ids','finding','first_date','last_date')})
    for group in ledger['identity_cases']:
        for identifier in group['affected_ids']:identities[identifier].append(deepcopy(group))
    archive=[]
    for item in sorted(plans,key=lambda p:p['original']['audit_id']):
        r=item['original'];identifier=r['audit_id'];doc=documents[r['source']]
        literal=b''.join(lines[r['source']][r.get('source_start_line',r['source_line'])-1:r['source_line']])
        if base.sha(literal)!=r['raw_line_sha256'] or doc['sha256']!=r['source_sha256'] or literal.decode('utf-8-sig').rstrip('\r\n')!=r['raw_record']:
            raise ValueError('Raw original record/provenance binding changed')
        assessment=item['assessment'];decision=decisions.get(identifier);included=item['projection'] is not None
        event=deepcopy(decision.get('chronology',{})) if decision else deepcopy(r['assessment']['chronology'])
        event.update(source_date=r['date'],effective_result_date=assessment['effective_result_date'],availability_basis=assessment['availability_basis'],availability_verified=assessment['availability_verified'])
        if decision:
            event.update(administrative_publication_date=decision.get('administrative_publication_date'),administrative_finality_date=decision.get('administrative_finality_date'))
        archive.append(dict(audit_id=identifier,original=deepcopy(r),literal_original_record=literal.decode('utf-8-sig'),
                            source_url=doc['url'],pinned_revision=doc['commit'],git_blob_sha1=doc['git_blob_sha1'],source_document=doc['path'],
                            source_sha256=r['source_sha256'],source_line=r['source_line'],raw_record_sha256=base.sha(literal),
                            historical_competition_label=r.get('source_fields',{}).get('division') if r['source'].endswith('.csv') else [n['text'] for n in ledger.get('source_notes',{}).get(r['source'],[]) if n['kind']=='TITLE'],
                            inclusion_status='INCLUDED' if included else assessment['status'],
                            hold_out_reason=assessment['decision'] if assessment['status']=='HOLD_OUT' else None,
                            decision_id=decision['decision_id'] if decision else 'ACCEPTED_NUMERIC_GOALS_ONLY',
                            approved_decision=deepcopy(decision),phase6_assessment=deepcopy(assessment),chronology=event,
                            approved_standardized_values=deepcopy(item['projection']),screened_match_id=item['projection']['match_id'] if included else None,
                            historical_review=deepcopy(claims.get(identifier)),scheduling_context=rounds.get(identifier,[]),identity_context=identities.get(identifier,[])))
    return archive


def prior_ids(root,directory):
    frozen=policy.review.read(directory/'protected_before.json')['private'];ids=set();files=[]
    for name in sorted(frozen):
        if not name.endswith('.csv'):continue
        with (root/name).open(encoding='utf-8-sig',newline='') as f:
            reader=csv.DictReader(f)
            if tuple(reader.fieldnames or ())!=OUTPUT_COLUMNS:continue
            count=0
            for row in reader:ids.add(row['match_id']);count+=1
            files.append(dict(path=name,records=count,sha256=frozen[name]))
    if not files or not ids:raise ValueError('No previous standardized datasets checked')
    return ids,files


def build(directory=PRIVATE,root=ROOT):
    protection=protect(directory,root);approval=policy.review.read(directory/APPROVAL)
    if approval!=dict(phase=7,approval='USER_APPROVED_PHASE7',phase6_policy_sha256=POLICY_SHA,scope='Acquired 35 represented seasons; five holdouts and 101 NOT PLAYED retained',no_gap_supplement=True,no_new_historical_decisions=True):raise ValueError('Phase 7 approval changed')
    for name,raw in policy.build(directory,root).items():
        if raw!=(directory/name).read_bytes():raise ValueError('Frozen Phase 6 artifact no longer reproduces')
    approved=policy.review.read(directory/policy.POLICY)
    if base.sha(base.encode(approved))!=POLICY_SHA:raise ValueError('Approved Phase 6 policy SHA changed')
    report=policy.review.read(directory/policy.review.structural.REPORT);ledger=policy.review.read(directory/policy.review.LEDGER);r5=policy.review.read(directory/policy.review.OUTPUT)
    plans=prepare(report,approved,ledger,r5)
    with TemporaryDirectory(prefix='ligue1-import-') as temp:
        raw,summary=convert(plans,Path(temp));repeat,_=convert(list(reversed(plans)),Path(temp))
    if raw!=repeat:raise ValueError('Shared importer is input-order dependent')
    rows=parse_standard(raw);plans,counts=verify_subset(rows,report,approved,ledger,r5)
    if serialize_csv(rows,OUTPUT_COLUMNS)!=raw:raise ValueError('CSV serialization roundtrip differs')
    previous,prior_files=prior_ids(root,directory)
    if previous & {r['match_id'] for r in rows}:raise ValueError('Match ID collision with previous competitions')
    documents,rights=provenance(directory)
    # Source title annotations are frozen structural evidence, not added history.
    audit_ledger=deepcopy(ledger);audit_ledger['source_notes']=report['source_notes']
    records=archive_records(plans,approved,audit_ledger,documents,directory)
    if len(records)!=len(report['records']) or len({r['audit_id'] for r in records})!=len(records):raise ValueError('Archive lost/duplicated observations')
    projected=[r['approved_standardized_values'] for r in records if r['inclusion_status']=='INCLUDED']
    if {r['match_id']:r for r in projected}!={r['match_id']:r for r in rows}:raise ValueError('Archive/screened subset not exact')
    if any(r['screened_match_id'] is not None for r in records if r['inclusion_status']!='INCLUDED'):raise ValueError('Held/not-played ID leakage')
    archive=dict(league=LEAGUE,counts=counts,records=records,source_documents=documents,rights=rights,
                 policy_sha256=POLICY_SHA,warning='Includes HOLD OUT and NOT PLAYED observations; never use archive as training data.')
    exceptions=dict(league=LEAGUE,counts=counts,policy=approved,evidence_registry=ledger['evidence'],
                    exception_records=[r for r in records if r['inclusion_status']!='INCLUDED' or r['approved_decision'] is not None],
                    coverage=approved['coverage'],chronological_rule=approved['temporal_rule'],
                    ordinary_date_warning='Unchanged source calendar day is not independently certified availability; future consumers must enforce policy.training_allowed.',
                    rights=rights,training_authorized=False)
    outputs={NAMES[0]:raw,NAMES[1]:base.encode(archive),NAMES[2]:base.encode(exceptions)}
    coverage=[]
    for year in range(1990,2026):
        rs=[r for r in records if r['original']['season']==f'{year}/{year+1}']
        coverage.append(dict(season=f'{year}/{year+1}',archived=len(rs),screened=sum(r['inclusion_status']=='INCLUDED' for r in rs),hold_out=sum(r['inclusion_status']=='HOLD_OUT' for r in rs),not_played=sum(r['inclusion_status']=='NOT_PLAYED' for r in rs)))
    code=['scripts/standardize_ligue1_results.py','tests/test_ligue1_standardization.py','scripts/decide_ligue1_policy.py','scripts/standardize_england_results.py','scripts/artifact_io.py','src/toto_estimator/historical_import.py','src/toto_estimator/data.py','src/toto_estimator/outcomes.py','src/toto_estimator/validation.py']
    inputs=[BASELINE,APPROVAL,policy.POLICY,policy.ASSESSMENT,policy.review.LEDGER,policy.review.OUTPUT,policy.review.structural.REPORT,policy.review.structural.QUEUE,'acquisition.json','phase3_acquisition.json']
    manifest=dict(league=LEAGUE,schema=list(OUTPUT_COLUMNS),counts=counts,coverage=coverage,shared_import_summary=summary,
                  source_documents=documents,rights=rights,preservation=protection,
                  inputs={n:base.sha((directory/n).read_bytes()) for n in inputs},code={n:base.sha((root/n).read_bytes()) for n in code},
                  prior_standardized_files_checked=prior_files,prior_unique_ids=len(previous),prior_collisions=0,
                  numeric_goal_outcomes=dict(Counter('H' if r['home_goals']>r['away_goals'] else 'A' if r['home_goals']<r['away_goals'] else 'D' for r in rows)),
                  auxiliary_label_defects_preserved=len(approved['outcome_rule']['primary_label_defect_ids']),
                  replay_dates={c['decision_id']:c['effective_result_date'] for c in approved['decisions'] if c['action']=='APPROVED_REPLAY'},
                  brest_identity_rule=approved['identity_rules'],coverage_gaps=approved['coverage'],
                  historical_certification='NOT_CLAIMED',training_authorized=False,licensing_clearance='UNRESOLVED',
                  outputs={n:dict(bytes=len(value),sha256=base.sha(value)) for n,value in outputs.items()})
    outputs[NAMES[3]]=base.encode(manifest);protect(directory,root)
    return outputs


def main():
    parser=argparse.ArgumentParser(description=__doc__);mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--init',action='store_true');mode.add_argument('--write',action='store_true');mode.add_argument('--check',action='store_true');parser.add_argument('--output-directory',type=Path,default=PRIVATE);args=parser.parse_args()
    if args.init:print(initialize());return
    outputs=build()
    for name,raw in outputs.items():
        path=args.output_directory/name
        if path.exists() and path.read_bytes()!=raw:raise ValueError('Existing output differs; no overwrite: '+name)
        if args.check and not path.exists():raise ValueError('Missing output: '+name)
    if args.write:
        for name,raw in outputs.items():
            if not (args.output_directory/name).exists():base.save(args.output_directory/name,raw)
    for name,raw in outputs.items():print(name,len(raw),base.sha(raw))


if __name__=='__main__':main()
