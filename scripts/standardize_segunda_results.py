"""Phase 7 offline screened CSV, complete audit archive, sidecar and manifest.

No acquisition, policy changes, application integration or training. All outputs
are private; existing outputs are never overwritten. Requires frozen Phase 6.
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

from scripts import decide_segunda_policy as policy
from scripts.artifact_io import check_overwrite, serialize_csv
from toto_estimator.historical_import import OUTPUT_COLUMNS
from toto_estimator.outcomes import outcome_from_goals
from toto_estimator.validation import exact_integer

ROOT, PRIVATE, base = policy.ROOT, policy.PRIVATE, policy.base
BASELINE='phase7_protected_before.json'
APPROVAL='phase7_approval.json'
POLICY_SHA='c5140f5113ca4ea4bc605569807c4495e04c1e9e5509fe88d8f2179aa69a5220'
LEAGUE='Segunda División'
NAMES=('segunda_division_standardized_2012_2024.csv','segunda_division_audit_archive_2012_2024.json',
       'segunda_division_exceptions_2012_2024.json','segunda_division_standardization_manifest.json')


def protect(directory=PRIVATE,root=ROOT):
    previous=policy.protected(directory,root);saved=policy.review.read(directory/BASELINE)
    if len(saved['files'])!=75:raise ValueError('Phase 7 protected scope changed')
    for name,digest in saved['files'].items():
        path=root/name
        if not path.resolve().is_relative_to(root.resolve()) or base.sha(path.read_bytes())!=digest:
            raise ValueError('Frozen Phase 2–6 artifact changed: '+name)
    prefix=saved['planning_log'];raw=(root/'PLANNING_LOG.md').read_bytes()
    if len(raw)<prefix['bytes'] or base.sha(raw[:prefix['bytes']])!=prefix['sha256']:
        raise ValueError('Planning history changed')
    return dict(previous=previous,phase2_6_files=len(saved['files']))


def validate_approval(approval,approved):
    cases=policy.validate_registry(approved)
    if (approval['phase']!=7 or approval['approval']!='USER_APPROVED_PHASE7' or
            approval['approved_phase6_policy_sha256']!=POLICY_SHA or
            base.sha(base.encode(approved))!=POLICY_SHA):
        raise ValueError('Frozen Phase 6 or Phase 7 approval changed')
    if approval['approved_conditional_hold_ids']!=approved['conditional_hold_ids']:
        raise ValueError('Deportivo hold approval missing or broadened')
    return cases


def standard_id(row):
    values=[LEAGUE,row['season'],row['date'],row['home_team'],row['away_team']]
    return base.sha(json.dumps(values,ensure_ascii=False,separators=(',',':')).encode())


def pair(row):return row['season'],row['home_team'],row['away_team']


def prepare(records,approved,historical):
    """Pure source-to-policy plan. No held record receives a screened projection."""
    cases=policy.validate_registry(approved);ids=set();locations=set();pairs=set();plans=[]
    for r in records:
        identifier=r['source_fixture_id'];location=(r['source_file'],r['source_line'])
        if identifier!=policy.review.structural.source_id(r['source_file'],r['source_sha256'],r['source_line']):
            raise ValueError('Raw source audit ID mismatch')
        if identifier in ids or location in locations:raise ValueError('Duplicate source observation')
        ids.add(identifier);locations.add(location)
        fields=dict(league=LEAGUE,season=r['season'],date=r['date'],home_team=r['home'],away_team=r['away'])
        if pair(fields) in pairs:raise ValueError('Duplicate directed season fixture')
        pairs.add(pair(fields));policy.identity_labels(r['home'],r['away'])
        source_date=policy.day(r['date']);year=int(r['season'][:4])
        if r['season']!=f'{year}/{year+1}' or not 2012<=year<=2024:raise ValueError('Wrong acquired season scope')
        end=date(year+1,8,31) if year==2019 else date(year+1,6,30)
        if not date(year,7,1)<=source_date<=end:raise ValueError('Source date outside season')
        assessment=policy.assess_record(r,cases,historical_status=historical.get(identifier,'UNVERIFIED'))
        include=assessment['exception_policy_screenable']
        if not include and assessment['screening_status'] not in {'UNRESOLVED_HOLD_OUT','CONDITIONAL_HOLD_OUT_PENDING_REVIEW'}:
            raise ValueError('Unexpected missing/technical/conflicting result; investigate before export')
        projection=None
        if include:
            effective=assessment['effective_result_date']
            if effective is None or not date(year,7,1)<=policy.day(effective)<=end:
                raise ValueError('Screened effective date missing/outside season')
            h,a=policy.score(assessment['policy_result'])
            fields.update(date=effective,home_goals=h,away_goals=a)
            projection={k:({'match_id':standard_id(fields),**fields})[k] for k in OUTPUT_COLUMNS}
        plans.append(dict(original=deepcopy(r),assessment=assessment,projection=projection,
                          decision=deepcopy(cases.get(identifier))))
    if set(cases)-ids:raise ValueError('Required exceptional fixture absent from source population')
    return plans


def convert(plans,directory):
    from scripts.standardize_england_results import convert_rows
    bridge=[]
    for item in plans:
        r=item['projection']
        if r is None:continue
        h,a=r['home_goals'],r['away_goals']
        bridge.append(dict(Date=r['date'],Season=r['season'],HomeTeam=r['home_team'],AwayTeam=r['away_team'],
                           hGoal=str(h),aGoal=str(a),Score=f'{h}-{a}',Result={'1':'H','X':'D','2':'A'}[outcome_from_goals(h,a)],
                           Tier='2',Division=LEAGUE))
    return convert_rows(bridge,directory,league=LEAGUE,tier='2',division_names={int(r['Season'][:4]):LEAGUE for r in bridge})


def parse_standard(raw):
    reader=csv.DictReader(io.StringIO(raw.decode('utf-8')),strict=True)
    if tuple(reader.fieldnames or ())!=OUTPUT_COLUMNS:raise ValueError('Wrong eight-column schema/order')
    rows=[]
    for row in reader:
        if None in row or any(v is None or v=='' for v in row.values()):raise ValueError('Missing/malformed CSV field')
        for key in ('home_goals','away_goals'):
            n=exact_integer(row[key])
            if n<0 or str(n)!=row[key]:raise ValueError('Noncanonical nonnegative goal field')
            row[key]=n
        rows.append(row)
    return rows


def check_partition(rows,records,approved,historical):
    """Recompute expected subset from originals independently of the importer."""
    plans=prepare(records,approved,historical)
    expected={x['projection']['match_id']:x['projection'] for x in plans if x['projection'] is not None}
    if len(expected)!=sum(x['projection'] is not None for x in plans):raise ValueError('Duplicate expected match ID')
    seen=set();ordering=[]
    for r in rows:
        if tuple(r)!=OUTPUT_COLUMNS or r['league']!=LEAGUE:raise ValueError('Wrong standardized schema/league')
        if r['match_id']!=standard_id(r) or r['match_id'] in seen:raise ValueError('Wrong/duplicate shared deterministic ID')
        if expected.get(r['match_id'])!=r:raise ValueError('Unapproved row, score, date, identity or hold leakage')
        seen.add(r['match_id']);ordering.append((r['league'],r['season'],r['date'],r['home_team'],r['away_team']))
    if seen!=set(expected):raise ValueError('Screened subset missing accepted observation')
    if ordering!=sorted(ordering):raise ValueError('Noncanonical deterministic ordering')
    counts=dict(archived=len(plans),screened=len(rows),excluded=0,hold_out=sum(x['projection'] is None for x in plans),
                reus_unresolved_holds=sum(x['assessment']['screening_status']=='UNRESOLVED_HOLD_OUT' for x in plans),
                deportivo_approved_conservative_holds=sum(x['assessment']['screening_status']=='CONDITIONAL_HOLD_OUT_PENDING_REVIEW' for x in plans),
                supplemented=sum(x['assessment']['score_supplement'] for x in plans))
    if counts['screened']+counts['hold_out']+counts['excluded']!=counts['archived']:raise ValueError('Observation reconciliation failed')
    held_observation_ids={standard_id(dict(season=x['original']['season'],date=x['original']['date'],home_team=x['original']['home'],away_team=x['original']['away'])) for x in plans if x['projection'] is None}
    if held_observation_ids & seen:raise ValueError('Held source-observation ID leaked to screened CSV')
    return plans,counts


def provenance(directory):
    inventory=policy.review.read(directory/'phase3_acquisition.json')
    entries=inventory['acquired']+inventory['reused_phase2'];result={}
    if len(entries)!=13:raise ValueError('Wrong modern source inventory')
    for e in entries:
        file=e['path'];raw=(directory/file).read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        year=int(e['season'][:4]);expected=f'openfootball/espana/{year}-{(year+1)%100:02}/2-liga2.txt'
        if (file in result or file!=expected or not 2012<=year<=2024 or e['commit']!=policy.review.structural.base.PIN or
                base.sha(raw)!=e['sha256'] or len(raw)!=e['bytes'] or blob!=e['git_blob_sha1'] or
                e['url']!=f'https://raw.githubusercontent.com/openfootball/espana/{e["commit"]}/{year}-{(year+1)%100:02}/2-liga2.txt'):
            raise ValueError('Source receipt/hash/blob/scope mismatch')
        result[file]=deepcopy(e)
    if len(result)!=13:raise ValueError('Duplicate source receipts')
    return result,inventory['rights']


def audit_rows(plans,documents,directory,ledger,queue):
    raw={file:(directory/file).read_bytes().splitlines(keepends=True) for file in documents}
    claims={c['source_fixture_id']:c for c in ledger['fixtures']};flags={c['fixture']['source_fixture_id']:c for c in queue['records']}
    contexts=defaultdict(list);identities=defaultdict(list)
    for c in ledger['rounds']:
        for i in c['fixture_ids']:contexts[i].append(dict(season=c['season'],round=c['round'],status=c['status'],evidence=c['evidence']))
    for g in ledger['identities']:
        for i in g['fixture_ids']:identities[i].append(g['source_label'])
    rows=[]
    for item in sorted(plans,key=lambda x:x['original']['source_fixture_id']):
        r=item['original'];key=r['source_fixture_id'];file=r['source_file'];line=r['source_line']
        literal=raw[file][line-1]
        if (base.sha(literal)!=r['raw_line_sha256'] or literal.decode('utf-8').rstrip('\r\n')!=r['raw_record'] or
                documents[file]['sha256']!=r['source_sha256']):raise ValueError('Physical source line/provenance binding changed')
        decision=item['decision'];assessment=item['assessment'];included=item['projection'] is not None
        reason=None if included else ('UNRESOLVED_INDIVIDUAL_REUS_AWARD_FINALITY_AND_AVAILABILITY' if assessment['screening_status']=='UNRESOLVED_HOLD_OUT' else
                                      'USER_APPROVED_CONSERVATIVE_DEPORTIVO_ADMINISTRATIVE_FINALITY_AVAILABILITY_HOLD')
        event=deepcopy(decision['event_dates']) if decision else deepcopy(r['chronology'])
        event['effective_result_date']=assessment['effective_result_date']
        row=dict(source_fixture_id=key,source_file=file,source_line=line,source_sha256=r['source_sha256'],source_url=documents[file]['url'],
                 pinned_commit=documents[file]['commit'],git_blob_sha1=documents[file]['git_blob_sha1'],original=deepcopy(r),
                 literal_source_line=literal.decode('utf-8'),literal_source_line_sha256=base.sha(literal),
                 inclusion_status='INCLUDED' if included else 'HOLD_OUT',hold_out_reason=reason,
                 phase6_assessment=assessment,phase7_hold_approval='USER_APPROVED_PHASE7' if not included else None,
                 exception_decision_id=decision['decision_id'] if decision else None,
                 original_phase6_decision_approval=decision['approval'] if decision else None,
                 historical_review=deepcopy(claims.get(key)),review_categories=flags.get(key,{}).get('categories',[]),
                 scheduling_context=contexts.get(key,[]),reserve_identity_groups=identities.get(key,[]),
                 chronology=event,approved_policy_result=assessment['policy_result'],
                 approved_transformed_values=deepcopy(item['projection']),screened_match_id=item['projection']['match_id'] if included else None,
                 goal_derived_outcome=outcome_from_goals(*policy.score(assessment['policy_result'])) if included else None)
        rows.append(row)
    return rows


def build(directory=PRIVATE,root=ROOT):
    preservation=protect(directory,root)
    for n,raw in policy.build(directory,root).items():
        if (directory/n).read_bytes()!=raw:raise ValueError('Frozen Phase 6 output no longer reproduces')
    approved=policy.review.read(directory/policy.POLICY);approval=policy.review.read(directory/APPROVAL)
    validate_approval(approval,approved)
    report=policy.review.read(directory/policy.review.structural.REPORT);records=report['records']
    ledger=policy.review.read(directory/policy.review.LEDGER);queue=policy.review.read(directory/policy.review.structural.QUEUE)
    historical={c['source_fixture_id']:c['status'] for c in ledger['fixtures']}
    documents,rights=provenance(directory)
    if set(documents)!={r['source_file'] for r in records}:raise ValueError('Source population/inventory disagreement')
    plans=prepare(records,approved,historical)
    # Shared importer uses temporary bridge files outside all original bundles.
    with TemporaryDirectory(prefix='toto-segunda-import-') as temp:
        raw,summary=convert(plans,Path(temp));reverse,_=convert(list(reversed(plans)),Path(temp))
    if raw!=reverse:raise ValueError('Shared importer ordering changes with input order')
    rows=parse_standard(raw);plans,counts=check_partition(rows,records,approved,historical)
    if serialize_csv(rows,OUTPUT_COLUMNS)!=raw:raise ValueError('CSV does not serialize canonically')
    archive_rows=audit_rows(plans,documents,directory,ledger,queue)
    if len(archive_rows)!=len(records) or len({r['source_fixture_id'] for r in archive_rows})!=len(records):
        raise ValueError('Complete audit archive lost/duplicated observations')
    if {r['screened_match_id'] for r in archive_rows if r['inclusion_status']=='INCLUDED'}!={r['match_id'] for r in rows}:
        raise ValueError('Audit/screened subset mismatch')
    archive=dict(league=LEAGUE,scope='2012/2013–2024/2025 acquired modern sources only',counts=counts,records=archive_rows,
                 source_documents=documents,rights=rights,phase6_policy_sha256=POLICY_SHA,phase7_approval=approval,
                 warning='Includes held/unresolved observations; never use the audit archive directly as training data.')
    exceptions=dict(league=LEAGUE,counts=counts,phase6_policy_sha256=POLICY_SHA,phase7_approval=approval,
                    approved_cases=approved['cases'],uncertainty=approved['uncertainty'],evidence_registry=ledger['sources'],
                    exceptional_links=[r for r in archive_rows if r['exception_decision_id']],
                    date_semantics='Approved playing/completion calendar day for explicit decisions; unchanged ordinary source-date proxy is not independently certified availability.',
                    chronological_rule=approved['chronological_rule'],rights=rights,training_authorized=False)
    outputs={NAMES[0]:raw,NAMES[1]:base.encode(archive),NAMES[2]:base.encode(exceptions)}
    coverage=[]
    for year in range(2012,2025):
        rs=[r for r in archive_rows if int(r['original']['season'][:4])==year]
        coverage.append(dict(season=f'{year}/{year+1}',archived=len(rs),screened=sum(r['inclusion_status']=='INCLUDED' for r in rs),
                             held_out=sum(r['inclusion_status']=='HOLD_OUT' for r in rs),supplemented=sum(r['phase6_assessment']['score_supplement'] for r in rs)))
    code=['scripts/standardize_segunda_results.py','tests/test_segunda_standardization.py','scripts/decide_segunda_policy.py',
          'scripts/verify_segunda_review.py','scripts/standardize_england_results.py','scripts/artifact_io.py',
          'src/toto_estimator/historical_import.py','src/toto_estimator/data.py','src/toto_estimator/validation.py','src/toto_estimator/outcomes.py']
    inputs=[BASELINE,APPROVAL,policy.POLICY,policy.ASSESSMENT,policy.review.LEDGER,policy.review.OUTPUT,
            policy.review.structural.REPORT,policy.review.structural.QUEUE,'acquisition.json','phase3_acquisition.json']
    manifest=dict(league=LEAGUE,schema=list(OUTPUT_COLUMNS),counts=counts,coverage=coverage,shared_import_summary=summary,
                  screened_goal_derived_outcomes=dict(Counter(outcome_from_goals(r['home_goals'],r['away_goals']) for r in rows)),
                  source_documents=documents,preservation=preservation,input_sha256={n:base.sha((directory/n).read_bytes()) for n in inputs},
                  code_sha256={n:base.sha((root/n).read_bytes()) for n in code},
                  uncertainty_counts=dict(rounds=len(ledger['rounds']),round_classifications=dict(Counter(c['status'] for c in ledger['rounds'])),
                    outliers=sum('DIAGNOSTIC_DATE_OUTLIER' in x['categories'] for x in queue['records']),
                    affected_round_observations=len({i for c in ledger['rounds'] for i in c['fixture_ids']}),
                    reversals=sum(len(s['validation']['source_order_reversals']) for s in report['seasons']),
                    reserve_observations=sum(bool(r['reserve_identity_groups']) for r in archive_rows),
                    historical_claims=dict(Counter(r['historical_review']['status'] if r['historical_review'] else 'NOT_INDIVIDUALLY_REVIEWED' for r in archive_rows))),
                  hold_out_fixture_ids=sorted(r['source_fixture_id'] for r in archive_rows if r['inclusion_status']=='HOLD_OUT'),
                  global_team_mappings={},source_score_overwrites=0,source_date_corrections=0,training_authorized=False,
                  model_training_clearance='NOT_CLEARED',licensing_clearance='UNRESOLVED',rights=rights,coverage_gaps=report['gaps'],
                  outputs={n:dict(bytes=len(content),sha256=base.sha(content)) for n,content in outputs.items()})
    outputs[NAMES[3]]=base.encode(manifest);protect(directory,root)
    return outputs


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true')
    parser.add_argument('--output-directory',type=Path,default=PRIVATE);args=parser.parse_args()
    if not args.check:check_overwrite([args.output_directory/n for n in NAMES])
    outputs=build()
    for name,raw in outputs.items():
        path=args.output_directory/name
        if args.check:
            if path.read_bytes()!=raw:raise ValueError('Saved standardization output differs: '+name)
        else:base.save(path,raw)
        print(name,base.sha(raw))
    print(json.loads(outputs[NAMES[3]])['counts'])


if __name__=='__main__':main()
