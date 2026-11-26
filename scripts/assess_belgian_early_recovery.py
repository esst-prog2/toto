"""Bounded five-season recovery assessment; offline and permission-first.

No network collector is enabled: no new adequately verified, permitted and scoped
fixture original was selected. Pure validators are tested synthetically; they do
not imply that inaccessible seasons were validated. Frozen Phase6 stays intact.
"""
import argparse
from collections import Counter, defaultdict
from datetime import date
from html import unescape
from pathlib import Path
import json
import os
import re
import subprocess
import sys
import tempfile
from scripts import decide_belgian_pro_league_policy as policy

ROOT, PRIVATE = policy.ROOT, policy.PRIVATE
encode, sha = policy.encode, policy.sha
YEARS = tuple(range(1990, 1995))
NAMES = ('source_inventory.json', 'rsssf_structural_corroboration.json',
         'supplemental_registry.json', 'coverage_assessment.json')


def read(path):
    return json.loads(path.read_text())


def preserve(directory=PRIVATE):
    previous = policy.preserve(directory)
    baseline = read(directory/'early_recovery_protected_before.json')
    for name, digest in baseline['files'].items():
        path = ROOT/name
        if not path.resolve().is_relative_to(ROOT.resolve()) or sha(path.read_bytes()) != digest:
            raise ValueError('Frozen prior file changed: '+name)
    prefix = baseline['planning_log']
    if sha((ROOT/'PLANNING_LOG.md').read_bytes()[:prefix['bytes']]) != prefix['sha256']:
        raise ValueError('Planning prefix changed')
    return dict(previous=previous, frozen_pre_recovery_entries=len(baseline['files']))


def require_permitted_original(receipt, raw):
    """No robots-only, mirror-only, search-only or moving-page authorization."""
    if receipt.get('acquisition_authorized') is not True or not receipt.get('permission_basis'):
        raise ValueError('Explicit scoped acquisition permission required')
    if receipt.get('season') not in {f'{y}/{y+1}' for y in YEARS}:
        raise ValueError('Outside five-season scope')
    if not receipt.get('url','').startswith('https://') or not receipt.get('final_url','').startswith('https://'):
        raise ValueError('Exact original/final URLs required')
    if receipt.get('sha256') != sha(raw) or receipt.get('bytes') != len(raw):
        raise ValueError('Original receipt integrity differs')
    if not receipt.get('retrieved_at_utc') or not receipt.get('publisher'):
        raise ValueError('Missing retrieval/provenance')
    raw.decode(receipt['encoding'])
    if receipt.get('source_kind') == 'WEB' and (receipt.get('git_commit') is not None or receipt.get('git_blob') is not None):
        raise ValueError('Web snapshot cannot invent Git identity')


def row_errors(row):
    errors = []
    if row.get('season') not in {f'{y}/{y+1}' for y in YEARS}:
        errors.append('OUTSIDE_APPROVED_SEASONS')
    if row.get('competition') != 'Belgian Pro League' or row.get('stage') != 'REGULAR_SEASON':
        errors.append('WRONG_COMPETITION_OR_STAGE')
    try:
        policy.iso_day(row.get('date'))
        year = int(row['season'][:4])
        if not f'{year}-07-01' <= row['date'] <= f'{year+1}-06-30':
            errors.append('DATE_OUTSIDE_SEASON')
    except (ValueError, TypeError, KeyError):
        errors.append('INVALID_EXPLICIT_MATCH_DATE')
    if row.get('date_basis') != 'EXPLICIT_MATCH_DATE':
        errors.append('UNVERIFIED_DATE_PROXY')
    home, away = row.get('home'), row.get('away')
    if not isinstance(home,str) or not isinstance(away,str) or not home.strip() or not away.strip() or home == away:
        errors.append('INVALID_PARTICIPANTS')
    if any('\ufffd' in value or any(ord(c)<32 for c in value) for value in (home,away) if isinstance(value,str)):
        errors.append('ENCODING_OR_CONTROL_CHARACTER')
    try:
        goals = policy.score(row.get('FT'))
        if str(goals['home_goals']) != str(row.get('hg')) or str(goals['away_goals']) != str(row.get('ag')):
            errors.append('SCORE_FIELDS_DISAGREE')
    except ValueError:
        errors.append('MISSING_OR_INVALID_FINAL_SCORE')
    if not row.get('source_id') or not row.get('original_sha256') or not isinstance(row.get('source_line'),int) or row['source_line'] < 1:
        errors.append('MISSING_PHYSICAL_SOURCE_BINDING')
    return errors


def assess_rows(rows):
    """Count observed records honestly; do not fill a 306-fixture template."""
    scored, clubs, fixtures = 0, set(), defaultdict(list)
    failures = []
    for row in rows:
        errors = row_errors(row)
        if errors:
            failures.append(dict(source_id=row.get('source_id'),errors=errors))
        try:
            policy.score(row.get('FT')); scored += 1
        except ValueError:
            pass
        if isinstance(row.get('home'),str) and isinstance(row.get('away'),str):
            clubs.update([row['home'],row['away']]);fixtures[row['home'],row['away']].append(row)
    duplicates = [dict(home=h,away=a,observations=len(rs),conflicting_scores=len({r.get('FT') for r in rs})>1)
                  for (h,a),rs in sorted(fixtures.items()) if len(rs)>1]
    home_counts = Counter(r.get('home') for r in rows)
    away_counts = Counter(r.get('away') for r in rows)
    # Only source observations, not inferred missing games.
    return dict(observations=len(rows),scored=scored,unscored=len(rows)-scored,clubs=len(clubs),
                directed_pairs=len(fixtures),duplicates=duplicates,failures=failures,
                observed_home_away={c:dict(home=home_counts[c],away=away_counts[c]) for c in sorted(clubs)},
                nominal_uncovered_slots=max(0,306-len(fixtures)),
                excess_directed_pairs=max(0,len(fixtures)-306),
                individual_fixture_validation='NOT_EXECUTED_NO_OBSERVATIONS' if not rows else 'ASSESSED_NOT_HISTORICALLY_CERTIFIED')


def compare_explicit_rows(rows, lineage):
    """Exact source labels only. No global aliases or date inference.

    Shared or unknown upstream cannot turn matching databases into independent
    corroboration. Material differences remain visible, with no result decision.
    """
    groups = defaultdict(list)
    for row in rows:
        groups[row['season'],row['home'],row['away']].append(row)
    output = []
    for key, rs in sorted(groups.items()):
        facts = {(r['date'],r['FT']) for r in rs}
        sources = {r['source_id'] for r in rs}
        families = {lineage.get(source) for source in sources}
        independent = len(sources)>=2 and None not in families and len(families)==len(sources)
        status = ('CONFLICTING' if len(facts)>1 else 'FULL_CORE' if independent else 'PARTIAL')
        valid = all(not row_errors(r) for r in rs)
        if not valid:
            status = 'UNRESOLVED'
        exceptional = any(r.get('administrative_or_interruption_flag',False) for r in rs)
        output.append(dict(season=key[0],home=key[1],away=key[2],source_rows=rs,
                           corroboration=status,upstream_independence_established=independent,
                           preliminary_recommendation='PRELIMINARY_CANDIDATE_REQUIRES_SUPPLEMENTAL_PHASE6' if valid and status!='CONFLICTING' and not exceptional else 'UNRESOLVED',
                           adjudicated=False))
    return output


def rsssf_standings(raw):
    """Existing attributed 1992/93 original: standings are not fixture rows."""
    text = unescape(re.sub('<[^>]*>','',raw.decode('utf-8')))
    section = text.split('First Division (Eerste Klasse)',1)[1].split('Second Division (Tweede Klasse)',1)[0]
    pattern = r'^\s*(\d+)\.(.*?)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)-(\d+)\s+(\d+)\s*$'
    table = []
    for number,line in enumerate(section.splitlines(),1):
        m = re.fullmatch(pattern,line)
        if m:
            rank,name,played,wins,draws,losses,gf,ga,points=m.groups()
            table.append(dict(rank=int(rank),name=name.strip(),played=int(played),wins=int(wins),draws=int(draws),losses=int(losses),gf=int(gf),ga=int(ga),points=int(points),section_line=number))
        elif re.match(r'\s*\d+\.',line):
            raise ValueError('Unparsed standings row')
    if len(table)!=18 or len({r['name'] for r in table})!=18 or {r['rank'] for r in table}!=set(range(1,19)):
        raise ValueError('Standings population differs')
    if any(r['played']!=34 or r['wins']+r['draws']+r['losses']!=r['played'] or 2*r['wins']+r['draws']!=r['points'] for r in table):
        raise ValueError('Standings arithmetic differs')
    if sum(r['gf'] for r in table)!=sum(r['ga'] for r in table) or sum(r['wins'] for r in table)!=sum(r['losses'] for r in table):
        raise ValueError('Standings totals differ')
    return dict(season='1992/1993',clubs=18,table=table,played_sum=sum(r['played'] for r in table),
                nominal_aggregate_fixture_count=sum(r['played'] for r in table)//2,
                dated_fixture_observations=0,source_sha256=sha(raw),
                original='rsssf/tablesb/belg93.html',attribution='Dinant Abbink / RSSSF,2004',
                copying='Author acknowledgement required; rights reserved; no model-training grant inferred',
                no_dates_or_scores_reconstructed=True)


def build(directory=PRIVATE):
    preserve(directory)
    source = read(directory/'early_recovery/source_assessment_inputs.json')
    access = read(directory/'early_recovery/access_receipts.json')
    if source['candidate_observations']:
        raise ValueError('No new permitted fixture original selected; new acquisition requires explicit permission assessment')
    if any(s['automation_authorized'] or s['fixture_originals_acquired'] for s in source['sources']):
        raise ValueError('No collector/permission approval exists for this outcome')
    for rec in access['robots']:
        if rec.get('original_bytes_preserved'):
            raw=(directory/'early_recovery/gsa_robots.txt').read_bytes()
            if sha(raw)!=rec['sha256'] or len(raw)!=rec['bytes']:
                raise ValueError('Robots policy receipt differs')
    frozen = read(directory/'phase6/reconciliation.json')
    expected = dict(INCLUDE=8592,HOLD_OUT=120,NOT_PLAYED=10,OUT_OF_SCOPE=2)
    if frozen['conditional_events']!=8724 or frozen['dispositions']!=expected or frozen['documentary_only_observations']!=30:
        raise ValueError('Frozen approved Phase6 population differs')
    structure = rsssf_standings((directory/'rsssf/tablesb/belg93.html').read_bytes())
    candidates = compare_explicit_rows([], {})
    coverage = []
    for y in YEARS:
        rows=[r for r in source['candidate_observations'] if r['season']==f'{y}/{y+1}']
        coverage.append(dict(season=f'{y}/{y+1}',nominal_expected_fixtures=306,nominal_clubs=18,nominal_rounds=34,
                             source_observations=len(rows),distinct_conditional_events=0,fully_corroborated=0,
                             partially_corroborated=0,conflicting_or_unresolved_observed_results=0,
                             preliminary_candidates=0,nominal_uncovered_slots=306,
                             fixture_validation=assess_rows(rows),
                             comparison_status='NOT_ASSESSABLE_NO_PERMITTED_FIXTURE_LISTS',
                             structural_corroboration='EXISTING_18_CLUB_34_MATCH_STANDINGS_ONLY' if y==1992 else 'USER_NOMINAL_EXPECTATION_NOT_INDEPENDENT_FIXTURE_VALIDATION',
                             coverage_status='SOURCE_GAP_NOT_NOT_PLAYED'))
    return dict(zip(NAMES,[dict(sources=source['sources'],access_receipts=access,
                                  new_fixture_originals=0,policy_files_preserved=1,
                                  no_circumvention=True,source_selection=source['source_selection']),structure,
        dict(candidates=candidates,source_observations=0,distinct_conditional_events=0,
             frozen_phase6_population_untouched=True,frozen_phase6_dispositions=expected,
             supplemental_adjudication_performed=False,standardization_performed=False),
        dict(seasons=coverage,nominal_slots=1530,observed_fixture_records=0,nominal_uncovered_slots=1530,
             actual_historical_missing_or_unplayed_counts='NOT_ESTABLISHED',
             cross_source_matched=0,cross_source_contradictions_observed=0,
             cross_source_validation_status='NOT_EXECUTED_NO_QUALIFYING_FIXTURE_DATASETS',
             conclusion=source['conclusion'],
             recommendation='Proceed only after owner approval with frozen8592INCLUDE; alternatively obtain a permitted five-season export, then separately validate and adjudicate supplement before Phase7; never download broad world bundle or restricted data to force coverage')]))


def generate(directory=PRIVATE, output=None):
    output=Path(output) if output else directory/'early_recovery/assessment'
    artifacts={name:encode(obj) for name,obj in build(directory).items()}
    inputs=[directory/'early_recovery_protected_before.json',directory/'early_recovery/source_assessment_inputs.json',directory/'early_recovery/access_receipts.json',directory/'early_recovery/gsa_robots.txt']
    artifacts['reproducibility.json']=encode(dict(artifacts={n:sha(raw) for n,raw in artifacts.items()},
        inputs={str(p.relative_to(directory)):sha(p.read_bytes()) for p in inputs},implementation_sha256=sha(Path(__file__).read_bytes()),
        network_requests_during_generation=0,new_match_originals=0))
    for name,raw in artifacts.items():
        policy.review.recovery.keep(output/name,raw)
    return {name:sha(raw) for name,raw in artifacts.items()}


def verify(directory=PRIVATE):
    with tempfile.TemporaryDirectory(prefix='belgium-early-recovery-') as tmp:
        proc=subprocess.run([sys.executable,'-B','-m','scripts.assess_belgian_early_recovery','--output',tmp],cwd=ROOT,
                            env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True,timeout=120)
        if proc.returncode:
            raise ValueError(proc.stdout+proc.stderr)
        result={}
        for name in (*NAMES,'reproducibility.json'):
            saved,fresh=(directory/'early_recovery/assessment'/name).read_bytes(),(Path(tmp)/name).read_bytes()
            if saved!=fresh:
                raise ValueError('Regeneration differs: '+name)
            result[name]=dict(sha256=sha(saved),bytes=len(saved),byte_identical=True)
    return dict(artifacts=result,protected=preserve(directory))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--verify',action='store_true')
    args=parser.parse_args()
    print(json.dumps(verify() if args.verify else generate(output=args.output),indent=2))
