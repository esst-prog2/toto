"""Phase 7: offline La Liga screening and full private provenance archive.

No acquisition, application integration, training or new historical decisions.
Default creates outputs exclusively; --check regenerates without replacing them.
"""
import argparse
from collections import Counter
from copy import deepcopy
import csv
from datetime import date
import hashlib
import io
import json

from scripts import decide_la_liga_policy as policy
from scripts import verify_la_liga_review as review
from scripts.artifact_io import check_overwrite, serialize_csv
from scripts.collect_la_liga_feasibility import ROOT, PRIVATE, sha
from scripts.standardize_england_results import convert_rows
from scripts.validate_la_liga_feasibility import encode
from toto_estimator.historical_import import OUTPUT_COLUMNS
from toto_estimator.outcomes import outcome_from_goals
from toto_estimator.validation import exact_integer

LEAGUE = 'La Liga'
NAMES = ('la_liga_standardized_1990_2025.csv', 'la_liga_audit_archive_1990_2025.json',
         'la_liga_exceptions_1990_2025.json', 'la_liga_standardization_manifest.json')
POLICY_SHA = 'b77a5cd6ef29114d78da56bae430f535e4bab314a515368e4149ca801bc6a835'


def protect(directory=PRIVATE, root=ROOT):
    baseline = review.read_json(directory/'phase7_protected_before.json')
    if len(baseline) != 504:
        raise ValueError('Phase 7 protected scope changed')
    review.protect(baseline, root)
    policy.check_append_only(review.read_json(directory/'phase7_history_prefixes.json'), root)
    return baseline


def pair(row):
    return row['season'], row['home_team'], row['away_team']


def standard_id(row):
    """Independent check of IDs created by the existing shared importer."""
    values = [LEAGUE,row['season'],row['date'],row['home_team'],row['away_team']]
    return sha(json.dumps(values,ensure_ascii=False,separators=(',',':')).encode())


def prepare(fixtures, approved, verified):
    ids=set(); locations=set(); plans=[]; pairs=set()
    for f in fixtures:
        r=f['original']; line=r['source_line']; key=(f['source_file'],line)
        expected=policy.source_id(f['source_file'],f['source_sha256'],line)
        if expected!=f['fixture_id'] or expected in ids or key in locations:
            raise ValueError('Duplicate/changed source fixture binding')
        ids.add(expected);locations.add(key)
        s=policy.assess(f,approved,technical_status='STRUCTURAL_PASS',
                        historical_status='VERIFIED_FACTS' if key in verified else 'UNVERIFIED')
        h,a=exact_integer(r['hg']),exact_integer(r['ag'])
        if min(h,a)<0 or r['home']==r['away'] or not r['home'] or not r['away']:
            raise ValueError('Invalid source goals/teams')
        if r['FT']!=f'{h}-{a}':
            raise ValueError('Original full-time string contradicts goals')
        include=s['exception_policy_screenable']
        if not include and s['screening_status']!='HOLD_OUT':
            raise ValueError('Unexpected technical rejection; investigate before export')
        effective=s['effective_result_date'] if include else r['date']
        parsed=policy.day(effective); y=int(f['season'][:4])
        end=date(y+1,8,31) if y==2019 else date(y+1,6,30)
        if not date(y,7,1)<=parsed<=end:
            raise ValueError('Effective date outside source season')
        standard=dict(league=LEAGUE,season=f['season'],date=effective,home_team=r['home'],away_team=r['away'],
                      home_goals=h,away_goals=a)
        if pair(standard) in pairs:
            raise ValueError('Duplicate ordered season fixture')
        pairs.add(pair(standard))
        plans.append(dict(fixture=f,assessment=s,fields=standard,
                          goal_derived_outcome=outcome_from_goals(h,a)))
    if {c['fixture_id'] for c in approved['cases']} - ids:
        raise ValueError('Approved exception missing or incorrectly bound to source population')
    return plans


def convert(plans, directory):
    bridge=[]
    for item in plans:
        r=item['fields'];h,a=r['home_goals'],r['away_goals']
        bridge.append(dict(Date=r['date'],Season=r['season'],HomeTeam=r['home_team'],AwayTeam=r['away_team'],
                           hGoal=str(h),aGoal=str(a),Score=f'{h}-{a}',
                           Result={'1':'H','X':'D','2':'A'}[outcome_from_goals(h,a)],Tier='1',Division=LEAGUE))
    return convert_rows(bridge,directory,league=LEAGUE,tier='1',
                        division_names={int(r['Season'][:4]):LEAGUE for r in bridge})


def parse_standard(raw):
    reader=csv.DictReader(io.StringIO(raw.decode('utf-8')),strict=True)
    if tuple(reader.fieldnames or ())!=OUTPUT_COLUMNS:
        raise ValueError('Wrong eight-column standardized schema/order')
    rows=[]
    for row in reader:
        if None in row or any(v is None or v=='' for v in row.values()):
            raise ValueError('Missing/malformed standardized field')
        for field in ('home_goals','away_goals'):
            row[field]=exact_integer(row[field])
        rows.append(row)
    return rows


def check_and_partition(standard, fixtures, approved, verified):
    """Recompute decisions from originals, not from a prepared/converted plan."""
    plans=prepare(fixtures,approved,verified)
    by_pair={pair(item['fields']):item for item in plans}
    if len(standard)!=len(plans):
        raise ValueError('Source-to-archive row count mismatch')
    accepted=[];linked=[];seen=set();ids=set();counts=Counter();outcomes=Counter()
    for row in standard:
        if set(row)!=set(OUTPUT_COLUMNS) or row['league']!=LEAGUE:
            raise ValueError('Wrong standardized fields/league')
        key=pair(row)
        if key in seen or key not in by_pair:
            raise ValueError('Duplicate/unbound standardized fixture')
        seen.add(key);item=by_pair[key];f=item['fixture'];s=item['assessment']
        for name,value in item['fields'].items():
            if row[name]!=value:
                raise ValueError('Date, team, season or score changed from approved source facts: '+name)
        if row['match_id']!=standard_id(row) or row['match_id'] in ids:
            raise ValueError('Invalid/nonunique deterministic shared match ID')
        ids.add(row['match_id'])
        if s['exception_policy_screenable']:
            if s['effective_result_date'] is None or row['date']!=s['effective_result_date']:
                raise ValueError('Screened row lacks approved result-availability date')
            accepted.append(row);counts['accepted']+=1
            outcomes[outcome_from_goals(row['home_goals'],row['away_goals'])]+=1
        else:
            if s['final_outcome_status']!='UNRESOLVED' or s['effective_result_date'] is not None:
                raise ValueError('Holdout was silently resolved')
            counts['unresolved']+=1
        linked.append(dict(source_fixture_id=f['fixture_id'],source_file=f['source_file'],
                           source_sha256=f['source_sha256'],source_line=f['original']['source_line'],
                           season=f['season'],original=deepcopy(f['original']),
                           assessment=s,source_observation_match_id=row['match_id'],
                           screened_match_id=row['match_id'] if s['exception_policy_screenable'] else None,
                           archive_projection=deepcopy(row),
                           projection_date_semantics='EFFECTIVE_RESULT_AVAILABILITY' if s['exception_policy_screenable'] else
                           'UNVERIFIED_SOURCE_DATE_ONLY_NOT_RESULT_AVAILABILITY',
                           goal_derived_outcome=item['goal_derived_outcome']))
    hold_ids={r['source_observation_match_id'] for r in linked if r['screened_match_id'] is None}
    if hold_ids & {r['match_id'] for r in accepted}:
        raise ValueError('Restricted match ID entered screened output')
    result=dict(source_records=len(fixtures),accepted=counts['accepted'],excluded=0,
                unresolved=counts['unresolved'],omitted_from_screened=counts['unresolved'])
    if result['accepted']+result['excluded']+result['unresolved']!=result['source_records']:
        raise ValueError('Record reconciliation failed')
    return accepted,linked,result,dict(outcomes)


def provenance(directory):
    first=review.read_json(directory/'acquisition.json')
    later=review.read_json(directory/'phase3_acquisition.json')
    docs=[x for x in first['files'] if x['kind']=='dataset']+later['additional_files']
    result={}
    for entry in docs:
        file=entry['path'];raw=(directory/file).read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        if file in result or sha(raw)!=entry['sha256'] or len(raw)!=entry['bytes'] or blob!=entry['git_blob_sha1']:
            raise ValueError('Source receipt/hash/blob mismatch')
        result[file]=deepcopy(entry)
    if len(result)!=15:
        raise ValueError('Approved source-document inventory changed')
    return result,deepcopy(first['rights'])


def raw_records(directory, files):
    """Preserve complete logical CSV records and literal text match lines."""
    raw={}
    for file in sorted(files):
        with (directory/file).open(encoding='utf-8-sig',newline='') as stream:text=stream.read()
        lines=text.splitlines(keepends=True)
        if file.endswith('.csv'):
            reader=csv.reader(io.StringIO(text),strict=True);headers=next(reader);previous=reader.line_num
            for cells in reader:
                last=reader.line_num
                if len(cells)!=len(headers):raise ValueError('Raw source CSV width changed')
                raw[file,last]=dict(raw_record=''.join(lines[previous:last]),original_fields=dict(zip(headers,cells)))
                previous=last
        else:
            for n,line in enumerate(lines,1):raw[file,n]=dict(raw_record=line)
    return raw


def build(directory=PRIVATE, root=ROOT):
    baseline=protect(directory,root)
    approved,policy_report=policy.build(directory,root)
    if sha(encode(approved))!=POLICY_SHA or encode(approved)!=(directory/policy.POLICY).read_bytes() or encode(policy_report)!=(directory/policy.ASSESSMENT).read_bytes():
        raise ValueError('Approved Phase 6 metadata changed')
    ledger=review.read_json(directory/review.LEDGER);source_rows=review.records(directory)
    source_docs,rights=provenance(directory)
    fixtures=[]
    for (file,line),(season,row) in sorted(source_rows.items()):
        digest=source_docs[file]['sha256'];identifier=policy.source_id(file,digest,line)
        fixtures.append(dict(fixture_id=identifier,source_file=file,source_sha256=digest,season=season,
                             original=deepcopy(row),identified_final_outcome_status='UNRESOLVED' if identifier in approved['unresolved_final_outcome_ids'] else 'NO_CONFLICT_IDENTIFIED'))
    verified={(s['source_file'],s['original']['source_line']) for s in ledger['samples']+ledger['supplemental_fixtures'] if s['status']=='VERIFIED'}
    plans=prepare(fixtures,approved,verified)
    archive_csv,summary=convert(plans,directory)
    repeat,_=convert(list(reversed(plans)),directory)
    if repeat!=archive_csv:raise ValueError('Importer output changes under input reordering')
    standard=parse_standard(archive_csv)
    accepted,archive_rows,counts,outcomes=check_and_partition(standard,fixtures,approved,verified)
    screened=serialize_csv(accepted,OUTPUT_COLUMNS)
    independent,_=convert([p for p in plans if p['assessment']['exception_policy_screenable']],directory)
    if screened!=independent or parse_standard(screened)!=accepted:
        raise ValueError('Independently imported screened subset differs')
    originals=raw_records(directory,source_docs)
    case_by_id={c['fixture_id']:c for c in approved['cases']}
    for entry in archive_rows:
        key=(entry['source_file'],entry['source_line'])
        entry['raw_source']=originals[key]
        entry['exception_decision_id']=case_by_id.get(entry['source_fixture_id'],{}).get('decision_id')
        if entry['exception_decision_id'] and entry['raw_source']['raw_record'].rstrip('\r\n')!=case_by_id[entry['source_fixture_id']]['source_raw_line']:
            raise ValueError('Exceptional raw source record differs from approved evidence')
    archive=dict(league=LEAGUE,scope='1990/1991–2025/2026',counts=counts,
                 warning='Full audit archive includes unresolved source observations; never use this archive as training input.',
                 source_documents=source_docs,rights=rights,phase6_policy_sha256=POLICY_SHA,records=archive_rows)
    exceptions=dict(approved_cases=approved['cases'],uncertainty=approved['uncertainty'],
                    exceptional_links=[r for r in archive_rows if r['exception_decision_id']],
                    counts=counts,chronological_rule=approved['chronological_rule'],
                    date_semantics=approved['standard_date_semantics'],ordinary_date_basis=approved['ordinary_date_basis'],
                    training_authorized=False,model_training_suitability='NOT_CLEARED',licensing_clearance='UNRESOLVED',rights=rights)
    outputs={NAMES[0]:screened,NAMES[1]:encode(archive),NAMES[2]:encode(exceptions)}
    coverage=[]
    for y in range(1990,2026):
        season=f'{y}/{y+1}';rs=[r for r in archive_rows if r['season']==season]
        coverage.append(dict(season=season,source_records=len(rs),accepted=sum(r['screened_match_id'] is not None for r in rs),
                             unresolved=sum(r['screened_match_id'] is None for r in rs)))
    code=['scripts/standardize_la_liga_results.py','tests/test_la_liga_standardization.py',
          'scripts/standardize_england_results.py','scripts/artifact_io.py','src/toto_estimator/historical_import.py',
          'src/toto_estimator/data.py','src/toto_estimator/validation.py','src/toto_estimator/outcomes.py']
    inputs=['phase7_protected_before.json','phase7_history_prefixes.json',policy.POLICY,policy.ASSESSMENT,
            review.LEDGER,'phase4_structural_validation.json','acquisition.json','phase3_acquisition.json']
    links={(r['source_file'],r['source_line']):r for r in archive_rows}
    sample_refs=approved['uncertainty']['unverified_samples'];outlier_refs=approved['uncertainty']['diagnostic_fixture_refs']
    uncertainty=dict(round_classifications=dict(Counter(r['status'] for r in approved['uncertainty']['rounds'])),
                     unverified_samples=len(sample_refs),unverified_samples_accepted=sum(links[r['source_file'],r['source_line']]['screened_match_id'] is not None for r in sample_refs),
                     diagnostic_outliers=len(outlier_refs),outliers_accepted=sum(links[r['source_file'],r['source_line']]['screened_match_id'] is not None for r in outlier_refs),
                     outliers_without_individual_full_fact_certification=sum(not r['individual_full_fact_claim'] for r in outlier_refs))
    manifest=dict(league=LEAGUE,schema=list(OUTPUT_COLUMNS),counts=counts,coverage=coverage,import_summary=summary,
                  uncertainty_preservation=uncertainty,
                  protected_files=len(baseline),input_sha256={n:sha((directory/n).read_bytes()) for n in inputs},
                  code_sha256={n:sha((root/n).read_bytes()) for n in code},source_documents=source_docs,
                  screened_goal_derived_outcomes=outcomes,
                  archive_goal_derived_outcomes=dict(Counter(r['goal_derived_outcome'] for r in archive_rows)),
                  historical_verification_counts=dict(Counter(r['assessment']['historical_verification'] for r in archive_rows)),
                  restricted_match_ids=[r['source_observation_match_id'] for r in archive_rows if r['screened_match_id'] is None],
                  model_training_cleared=0,licensing_cleared=0,source_corrections=0,training_authorized=False,
                  rights=rights,outputs={n:dict(bytes=len(b),sha256=sha(b)) for n,b in outputs.items()},
                  note='Screened acceptance is technical inclusion only; historical uncertainty and rights are not cleared.')
    outputs[NAMES[3]]=encode(manifest)
    protect(directory,root)
    return outputs


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    if not args.check:check_overwrite([PRIVATE/n for n in NAMES])
    outputs=build()
    for name,raw in outputs.items():
        path=PRIVATE/name
        if args.check:
            if path.read_bytes()!=raw:raise ValueError('Saved output differs: '+name)
        else:
            with path.open('xb') as stream:stream.write(raw)
        print(name,sha(raw))
    print(json.loads(outputs[NAMES[3]])['counts'])


if __name__=='__main__':
    main()
