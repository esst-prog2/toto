"""Offline modern Serie B standardization; private archive and screened derivative.

No training or application integration. Run with --check for byte regeneration.
Earlier sealed review and every pre-existing private file remain immutable.
"""
import argparse
from collections import Counter
from copy import deepcopy
import csv
from datetime import date
import io
import json
from pathlib import Path

from scripts.artifact_io import check_overwrite, serialize_csv
from scripts.standardize_england_results import convert_rows, digest
from scripts.acquire_serie_b import PRIVATE, ROOT
from scripts.validate_serie_b import build as source_audit, audit, encode
from scripts.verify_serie_b_review import review, binding, collisions
from toto_estimator.historical_import import OUTPUT_COLUMNS
from toto_estimator.outcomes import outcome_from_goals
from toto_estimator.validation import exact_integer

LEAGUE='Serie B'
REVIEW_SHA='46cca6dd670a50f476f5f2d2d06f879b69c14e72ec7cf9ecea1ec75febb4351a'
OUTPUT_NAMES=('serie_b_standardized_1997_2025.csv','serie_b_audit_archive_1997_2025.csv',
              'serie_b_exceptions_1997_2025.json','serie_b_standardization_manifest.json')
FACTS=('season','date','home_team','away_team','home_goals','away_goals')


def key(r):
    return r['source_file'],r['source_line']


def identity(r):
    return tuple(r[k] for k in ('league','season','date','home_team','away_team'))


def protect(directory):
    raw=(directory/'standardization_protected_before.json').read_bytes()
    files=json.loads(raw)
    for name,sha in files.items():
        p=ROOT/name
        if not p.resolve().is_relative_to((ROOT/'data/private').resolve()) or digest(p.read_bytes())!=sha:
            raise ValueError('Protected private file changed: '+name)
    return raw,files


def modern_records(details):
    selected=[d for d in details if 1997<=int(d['season'][:4])<=2025]
    if {d['season'] for d in selected}!={f'{y}/{y+1}' for y in range(1997,2026)}:
        raise ValueError('Modern season scope changed')
    rows=[];reports=[]
    for d in selected:
        report=audit(d['records'],int(d['season'][:4]))
        if report['status']!='STRUCTURAL_PASS' or report['missing_dates'] or report['round_dates']:
            raise ValueError('Incomplete modern season: '+d['season'])
        reports.append(report)
        for r in d['records']:
            rows.append(dict(source_file=d['file'],source_line=r['source_line'],season=d['season'],
                             date=r['date'],home_team=r['home'],away_team=r['away'],
                             home_goals=exact_integer(r['hg']),away_goals=exact_integer(r['ag'])))
    if len({key(r) for r in rows})!=len(rows):raise ValueError('Duplicate source location')
    return rows,reports


def apply_dates(records,corrections,directory,details):
    by_key={key(r):r for r in records};updates={};applied=[]
    for c in corrections:
        k=(c['source']['file'],c['source']['line'])
        if k in updates or k not in by_key:raise ValueError('Duplicate/missing correction location')
        if c['status']!='VERIFIED_PENDING_STANDARDIZATION' or c['applied'] is not False or not c['evidence_ids']:
            raise ValueError('Unverified correction')
        if set(c['replacements'])!={'date'}:raise ValueError('Only date corrections permitted')
        season,facts=binding(directory,c['source'],details)
        r=by_key[k]
        expected=dict(date=r['date'],home=r['home_team'],away=r['away_team'],hg=r['home_goals'],ag=r['away_goals'])
        if facts!=c['original'] or facts!=expected or season!=r['season']:raise ValueError('Correction facts differ')
        day=c['replacements']['date'];parsed=date.fromisoformat(day);y=int(season[:4])
        if parsed.isoformat()!=day or day==r['date'] or not date(y,7,1)<=parsed<=date(y+1,6,30):
            raise ValueError('Invalid correction date')
        updates[k]=day
        applied.append(dict(deepcopy(c),applied=True,applied_to='derived outputs only'))
    return [dict(r,date=updates.get(key(r),r['date'])) for r in records],applied


def convert(records,directory):
    rows=[]
    for r in records:
        y=int(r['season'][:4]);day=date.fromisoformat(r['date'])
        end=date(y+1,8,31) if y==2019 else date(y+1,6,30)
        if not 1997<=y<=2025 or not date(y,7,1)<=day<=end:raise ValueError('Date outside modern season')
        h,a=r['home_goals'],r['away_goals']
        rows.append(dict(Date=r['date'],Season=r['season'],HomeTeam=r['home_team'],AwayTeam=r['away_team'],
                         hGoal=str(h),aGoal=str(a),Score=f'{h}-{a}',Result={'1':'H','X':'D','2':'A'}[outcome_from_goals(h,a)],
                         Tier='2',Division=LEAGUE))
    content,summary=convert_rows(rows,directory,league=LEAGUE,tier='2',division_names={y:LEAGUE for y in range(1997,2026)})
    standard=list(csv.DictReader(io.StringIO(content.decode())))
    for r in standard:r['home_goals'],r['away_goals']=int(r['home_goals']),int(r['away_goals'])
    if Counter(tuple(r[k] for k in FACTS) for r in standard)!=Counter(tuple(r[k] for k in FACTS) for r in records):
        raise ValueError('Historical facts changed')
    return content,standard,summary


def partition(standard,records,policy,directory,details):
    """Fail closed on any changed/missing exception; derive the screened CSV here."""
    cases=policy['regular_cases']
    if policy['unlisted_training_suitability']!='UNRESOLVED':raise ValueError('Unlisted eligibility changed')
    expected={'E1':'UNRESOLVED','E2':'EXCLUDED','E3':'EXCLUDED','E4':'EXCLUDED','E5':'UNRESOLVED'}
    if len(cases)!=5 or {c['id']:c['training_suitability'] for c in cases}!=expected:
        raise ValueError('Exception decisions changed')
    by_source={key(r):r for r in records};by_identity={identity(r):r for r in standard}
    excluded=set();linked=[]
    for c in cases:
        k=(c['source']['file'],c['source']['line'])
        season,facts=binding(directory,c['source'],details)
        if k not in by_source or facts!=c['original']:raise ValueError('Exception source mismatch')
        r=by_source[k]
        if facts!=dict(date=r['date'],home=r['home_team'],away=r['away_team'],hg=r['home_goals'],ag=r['away_goals']) or season!=r['season']:
            raise ValueError('Exception parsed facts differ')
        match=by_identity.get(identity(dict(r,league=LEAGUE)))
        if match is None or match['match_id'] in excluded:raise ValueError('Missing/duplicate exception link')
        excluded.add(match['match_id'])
        linked.append(dict(deepcopy(c),match_id=match['match_id'],included_in_screened_output=False))
    accepted=[r for r in standard if r['match_id'] not in excluded]
    if excluded & {r['match_id'] for r in accepted} or len(accepted)+len(excluded)!=len(standard):
        raise ValueError('Excluded record leakage')
    return accepted,sorted(linked,key=lambda c:c['id'])


def build(directory=PRIVATE):
    protected,files=protect(directory)
    if digest((directory/'verification/review_manifest.json').read_bytes())!=REVIEW_SHA:raise ValueError('Review seal changed')
    checked=review(directory)
    audited=source_audit(directory);details=audited['details']
    read=lambda name:json.loads((directory/name).read_text())
    originals,coverage=modern_records(details)
    corrected,applied=apply_dates(originals,read('verification/verified_corrections.json')['corrections'],directory,details)
    if len(applied)!=1:raise ValueError('Expected one verified date correction')
    collision_details=[dict(season=s,records=[dict(home=r['home_team'],away=r['away_team'],date=r['date'],source_line=r['source_line']) for r in corrected if r['season']==s]) for s in sorted({r['season'] for r in corrected})]
    if collisions(collision_details):raise ValueError('Same-team/date collision')
    archive,standard,summary=convert(corrected,directory)
    repeat,_,_=convert(list(reversed(corrected)),directory)
    if archive!=repeat:raise ValueError('Input order changed output')
    accepted,exceptions=partition(standard,corrected,read('verification/exception_policy.json'),directory,details)
    screened=serialize_csv(accepted,OUTPUT_COLUMNS)
    # Exercise shared importer/loader independently on the screened subset as well.
    accepted_ids={r['match_id'] for r in accepted}
    independently,_,_=convert([r for r in corrected if standard_id(r) in accepted_ids],directory)
    if screened!=independently:raise ValueError('Screened conversion differs')
    decisions=read('standardization_decisions.json')
    if decisions['cases']!={'E1':'UNRESOLVED / HOLD OUT','E5':'UNRESOLVED / HOLD OUT'}:raise ValueError('Approved hold decisions changed')
    counts=dict(source_records=len(originals),accepted=len(accepted),excluded=sum(c['training_suitability']=='EXCLUDED' for c in exceptions),
                unresolved=sum(c['training_suitability']=='UNRESOLVED' for c in exceptions))
    if sum(counts[k] for k in ('accepted','excluded','unresolved'))!=counts['source_records']:raise ValueError('Partition counts disagree')
    sidecar=dict(exhaustive=False,exceptions=exceptions,approval=decisions,counts=counts,
                 unlisted_training_suitability='UNRESOLVED',training_authorized=False,
                 notice='Screened acceptance is technical inclusion only. Unlisted eligibility and source rights remain unresolved; no training integration.',
                 archive_notice='Audit archive includes five excluded/held rows and must not be used as model-training input.')
    outputs={OUTPUT_NAMES[0]:screened,OUTPUT_NAMES[1]:archive,OUTPUT_NAMES[2]:encode(sidecar)}
    matches={identity(r):r for r in standard}
    links=[dict(source_file=r['source_file'],source_line=r['source_line'],match_id=matches[identity(dict(r,league=LEAGUE))]['match_id'],
                screened=matches[identity(dict(r,league=LEAGUE))]['match_id'] in accepted_ids) for r in sorted(corrected,key=key)]
    manifest=dict(date='2026-11-21',league=LEAGUE,schema=list(OUTPUT_COLUMNS),counts=counts,seasons=len(coverage),
                  early_seasons='1990/1991–1996/1997 remain separate; not standardized',
                  coverage=coverage,independent_review=checked,import_summary=summary,applied_corrections=applied,source_links=links,
                  protected_files=len(files),protected_sha256=digest(protected),review_seal_sha256=REVIEW_SHA,
                  inputs={str(p.relative_to(directory)):digest(p.read_bytes()) for p in sorted(directory.rglob('*')) if p.is_file() and p.name not in OUTPUT_NAMES},
                  code_sha256={str(p.relative_to(ROOT)):digest(p.read_bytes()) for p in [Path(__file__).resolve(),ROOT/'scripts/standardize_england_results.py',ROOT/'src/toto_estimator/historical_import.py']},
                  identity='Existing importer SHA-256 of league, season, ISO date, home and away team; corrected date participates; scores do not.',
                  method='Audited required fields; source team labels preserved; one evidence-bound date correction; shared importer/loader; explicit five-match screening; no score substitutions.',
                  training_authorized=False,rights='Original acquisition restrictions remain: Football-Data academic/private use, no AI-training or commercial clearance; OpenFootball CC0 applies only to rights held. No new redistribution or training permission.',
                  limitations='Bounded external sample review, not exhaustive certification. Unlisted training suitability remains unresolved. Administrative awards recorded separately; final Catania outcomes unresolved.',
                  outputs={name:dict(bytes=len(raw),sha256=digest(raw)) for name,raw in outputs.items()})
    outputs[OUTPUT_NAMES[3]]=encode(manifest)
    protect(directory)
    return outputs


def standard_id(r):
    import hashlib
    return hashlib.sha256(json.dumps([LEAGUE,r['season'],r['date'],r['home_team'],r['away_team']],ensure_ascii=False,separators=(',',':')).encode()).hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    if not args.check:check_overwrite([PRIVATE/n for n in OUTPUT_NAMES])
    outputs=build()
    for name,content in outputs.items():
        path=PRIVATE/name
        if args.check:
            if path.read_bytes()!=content:raise ValueError('Saved output differs: '+name)
        else:
            with path.open('xb') as f:f.write(content)
        print(name,digest(content))
    print(json.loads(outputs[OUTPUT_NAMES[3]])['counts'])


if __name__=='__main__':main()
