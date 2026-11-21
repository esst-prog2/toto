"""Read-only Serie B review consistency checker; never certifies external truth.

Checks manually transcribed evidence, complete-page quotas, source/line bindings,
private evidence seals, correction scope, exception decisions and preservation.
No network calls, standardization, factual repairs or data writes.
"""
from collections import Counter, defaultdict
from datetime import date
import json
from pathlib import Path

from scripts.acquire_serie_b import ROOT, PRIVATE
from scripts.validate_serie_b import build, encode, sha

FULL_ACCESS={'FULL_RESULTS_PAGE','FULL_MATCH_PAGE','FULL_REPORT','FULL_DECISION_TEXT'}
FACTS=('date','home','away','hg','ag')


def period(day):
    year=date.fromisoformat(day).year
    if 1997<=year<=1999:return '1997–1999'
    if 2000<=year<=2009:return '2000–2009'
    if 2010<=year<=2019:return '2010–2019'
    if 2020<=year<=2026:return '2020–2026'
    raise ValueError('Outside modern verification dates')


def binding(directory,source,details=None):
    path=directory/source['file']
    if not path.resolve().is_relative_to(directory.resolve()):raise ValueError('Source outside private directory')
    raw=path.read_bytes()
    if sha(raw)!=source['sha256']:raise ValueError('Source checksum changed')
    lines=raw.decode('utf-8-sig').splitlines();line=source['line']
    if not isinstance(line,int) or not 1<=line<=len(lines) or lines[line-1]!=source['raw_line']:
        raise ValueError('Physical source line changed')
    if details is None:details=build(directory)['details']
    found=[(d,r) for d in details if d['file']==source['file'] for r in d['records'] if r['source_line']==line]
    if len(found)!=1:raise ValueError('Binding is not one selected regular-season fixture')
    d,r=found[0]
    if int(d['season'][:4])<1997:raise ValueError('Early seasons outside this review')
    return d['season'],dict(date=r['date'],home=r['home'],away=r['away'],hg=int(r['hg']),ag=int(r['ag']))


def check_samples(samples,evidence,require_quotas=True):
    counts=Counter();ids=set();bindings=set();differences={}
    for s in samples:
        source=s['source'];key=(source['file'],source['line'])
        if s['id'] in ids or key in bindings:raise ValueError('Duplicate sample/binding')
        ids.add(s['id']);bindings.add(key)
        observed=s['observed'];ev=evidence[s['evidence_id']]
        if ev['access'] not in FULL_ACCESS and ev['access']!='INDEXED_ONLY':raise ValueError('Unknown access level')
        if not ev['url'].startswith('https://') or not ev['locator'] or not ev['lineage_note']:
            raise ValueError('Missing source/locator/lineage')
        if observed['competition']!='Serie B' or observed['regular_season'] is not True or observed['season']!=s['season']:
            raise ValueError('Wrong competition/season/stage')
        year=int(s['season'][:4]);day=date.fromisoformat(observed['date'])
        end=date(year+1,8,31) if year==2019 else date(year+1,6,30)
        if not date(year,7,1)<=day<=end:raise ValueError('Observed date outside season')
        for side in ('home','away'):
            if s['identity_mapping'].get(observed[side])!=s['original'][side]:
                raise ValueError('Unexplained team identity/orientation')
        for k in ('hg','ag'):
            if type(observed[k]) is not int or observed[k]<0:raise ValueError('Invalid observed score')
        changed=[k for k in ('date','hg','ag') if observed[k]!=s['original'][k]]
        expected='AGREES' if not changed else 'DISAGREES'
        if s['comparison']!=expected:raise ValueError('Concealed or invented discrepancy')
        if changed:differences[s['id']]=changed
        if s['verification_status'] in ('VERIFIED','CONFIRMED_CORRECTION'):
            if (s['verification_status']=='VERIFIED' and changed) or (s['verification_status']=='CONFIRMED_CORRECTION' and not changed) or ev['access'] not in FULL_ACCESS:raise ValueError('Unsupported verification claim')
            if not s['evidence_note']:raise ValueError('Missing evidence reasoning')
            counts[period(observed['date'])]+=1
        elif s['verification_status'] not in ('UNRESOLVED','CONFIRMED_CORRECTION'):
            raise ValueError('Unknown verification status')
    quotas={'1997–1999':5,'2000–2009':10,'2010–2019':10,'2020–2026':5}
    if require_quotas and any(counts[p]<n for p,n in quotas.items()):raise ValueError('Insufficient complete-page verification quotas')
    return dict(verified=sum(counts.values()),period_counts=dict(counts),disagreements=differences)


def check_corrections(corrections,samples,evidence):
    by_id={s['id']:s for s in samples};ids=set();keys=set()
    for c in corrections:
        key=(c['source']['file'],c['source']['line'])
        if c['id'] in ids or key in keys:raise ValueError('Duplicate correction')
        ids.add(c['id']);keys.add(key)
        s=by_id.get(c['sample_id'])
        if s is None or s['verification_status']!='CONFIRMED_CORRECTION' or s['comparison']!='DISAGREES':
            raise ValueError('Correction lacks confirmed discrepancy')
        if c['source']!=s['source'] or c['original']!=s['original']:raise ValueError('Correction binding changed')
        if c['applied'] is not False or c['status']!='VERIFIED_PENDING_STANDARDIZATION':raise ValueError('Applied/unapproved correction')
        replacements=c['replacements']
        expected={k:s['observed'][k] for k in ('date','hg','ag') if s['observed'][k]!=s['original'][k]}
        if replacements!=expected or not replacements:raise ValueError('Unsupported correction scope')
        if any(k in replacements for k in ('hg','ag')) and c.get('final_administrative_status')!='CONFIRMED_FINAL':
            raise ValueError('Score correction lacks final outcome confirmation')
        if not c['evidence_ids'] or any(evidence[e]['access'] not in FULL_ACCESS for e in c['evidence_ids']):
            raise ValueError('Correction lacks full evidence')
    if {c['sample_id'] for c in corrections}!={s['id'] for s in samples if s['verification_status']=='CONFIRMED_CORRECTION'}:
        raise ValueError('Missing confirmed correction')


def check_exceptions(policy,evidence):
    if policy['unlisted_training_suitability']!='UNRESOLVED':raise ValueError('Unlisted eligibility assumed')
    cases=policy['regular_cases'];ids=set();keys=set();counts=Counter()
    for c in cases:
        key=(c['source']['file'],c['source']['line'])
        if c['id'] in ids or key in keys:raise ValueError('Duplicate exception')
        ids.add(c['id']);keys.add(key)
        if not c['reason'] or not c['evidence_ids']:raise ValueError('Unsupported exception')
        full=any(evidence[e]['access'] in FULL_ACCESS for e in c['evidence_ids'])
        kind=c['classification'];elig=c['training_suitability']
        if kind=='UNPLAYED_ADMINISTRATIVE_AWARD':
            if not full or elig!='EXCLUDED' or c['actual_date'] is not None or c['on_field_result'] is not None:
                raise ValueError('Invalid unplayed-award treatment')
        elif kind=='PLAYED_MATCH_FIXING_CASE':
            if not full or elig!='EXCLUDED' or c['actual_date'] is None or c['on_field_result'] is None:
                raise ValueError('Unsupported fixing classification')
        elif kind=='PLAYED_ADMINISTRATIVE_STATUS_UNRESOLVED':
            if elig!='UNRESOLVED' or c['official_final_result'] is not None:
                raise ValueError('Unresolved outcome silently settled')
        else:raise ValueError('Unknown exception classification')
        if elig=='UNRESOLVED' and c['future_training_action']!='HOLD_OUT_PENDING_REVIEW':
            raise ValueError('Unresolved training eligibility not held out')
        counts[elig]+=1
    if len(cases)!=5:raise ValueError('Missing reviewed/discovered regular exception')
    return dict(counts)


def collisions(details):
    groups=defaultdict(list)
    for d in details:
        if int(d['season'][:4])<1997:continue
        for r in d['records']:
            for team in (r['home'],r['away']):groups[(d['season'],r['date'],team)].append(r['source_line'])
    return [dict(season=s,date=d,team=t,lines=ls) for (s,d,t),ls in sorted(groups.items()) if len(ls)>1]


def aggregate_results(rows):
    totals={}
    for r in rows:
        h,a=int(r['hg']),int(r['ag'])
        for team,own,other in ((r['home'],h,a),(r['away'],a,h)):
            t=totals.setdefault(team,dict.fromkeys(('W','D','L','GF','GA','points'),0))
            t['W']+=int(own>other);t['D']+=int(own==other);t['L']+=int(own<other)
            t['GF']+=own;t['GA']+=other;t['points']+=3*int(own>other)+int(own==other)
    return totals


def check_format_report(report,samples,details):
    d=next(d for d in details if d['season']=='2003/2004')
    expected={n['line'] for n in d['notes'] if n['code']=='extra_csv_fields'}
    rows=report['rows']
    if {r['line'] for r in rows}!=expected or len(rows)!=len(expected):raise ValueError('Surplus-field rows incompletely reviewed')
    by_id={s['id']:s for s in samples}
    for row in rows:
        s=by_id[row['sample_id']]
        if s['source']['file']!=report['file'] or s['source']['sha256']!=report['sha256'] or s['source']['line']!=row['line'] or s['source']['raw_line']!=row['raw_line']:
            raise ValueError('Format evidence binding changed')
        if s['comparison']!='AGREES' or s['verification_status']!='VERIFIED':raise ValueError('Unresolved required-field format discrepancy')


def review(directory=PRIVATE):
    v=directory/'verification';load=lambda name:json.loads((v/name).read_text())
    seal=load('review_manifest.json')
    for name,digest in seal['files'].items():
        p=v/name
        if not p.resolve().is_relative_to(v.resolve()) or sha(p.read_bytes())!=digest:raise ValueError('Review evidence seal changed')
    if sha(Path(__file__).read_bytes())!=seal['checker_sha256']:raise ValueError('Checker revision changed')
    protected=load('protected_before.json')
    for name,digest in protected.items():
        p=ROOT/name
        if not p.resolve().is_relative_to(ROOT.resolve()) or sha(p.read_bytes())!=digest:raise ValueError('Pre-review private artifact changed')
    a=build(directory)
    if encode(a)!=(directory/'structural_audit.json').read_bytes():raise ValueError('Original structural audit changed')
    samples=load('samples.json');evidence=load('evidence_catalog.json')
    for s in samples:
        season,facts=binding(directory,s['source'],a['details'])
        if season!=s['season'] or facts!=s['original']:raise ValueError('Sample/source facts changed')
    summary=check_samples(samples,evidence)
    check_corrections(load('verified_corrections.json')['corrections'],samples,evidence)
    candidates=load('correction_candidates.json')['candidates']
    for c in candidates:
        _,facts=binding(directory,c['source'],a['details'])
        if facts!=c['original'] or c['applied'] is not False or c['status']!='HOLD_PENDING_FINAL_STATUS':
            raise ValueError('Pending candidate changed/approved')
        if not c['unresolved_reason'] or not c['evidence_ids']:raise ValueError('Unsupported pending candidate')
    policy=load('exception_policy.json')
    decisions=check_exceptions(policy,evidence)
    for c in policy['regular_cases']:
        _,facts=binding(directory,c['source'],a['details'])
        if facts!=c['original']:raise ValueError('Exception/source facts changed')
    selection=load('sample_selection.json')
    if selection!=[dict(id=s['id'],source=s['source']) for s in samples]:raise ValueError('Sample selection changed')
    check_format_report(load('2003_format_review.json'),samples,a['details'])
    aggregate=load('2025_aggregate_review.json')
    selected_2025=next(d for d in a['details'] if d['season']=='2025/2026')
    calculated=aggregate_results(selected_2025['records'])
    if calculated!=aggregate['computed'] or calculated!=aggregate['observed'] or len(calculated)!=20:
        raise ValueError('Independent 2025 table aggregate disagreement')
    modern=[d for d in a['details'] if int(d['season'][:4])>=1997]
    return dict(**summary,modern_seasons=len(modern),modern_records=sum(len(d['records']) for d in modern),
                protected_files_unchanged=len(protected),exception_decisions=decisions,
                confirmed_corrections=len(load('verified_corrections.json')['corrections']),
                pending_correction_candidates=len(candidates),corrections_applied=0,
                collision_groups=len(collisions(a['details'])),verified_2025_club_aggregates=len(calculated))


if __name__=='__main__':print(json.dumps(review(),indent=2,ensure_ascii=False))
