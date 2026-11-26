"""Belgian Phase 7: approved retrospective subset, shared schema/IDs, private audit.

Offline. No new historical decisions, global aliases, sources, application inputs
or model-training permission. The Phase6 registry is authoritative.
"""
import argparse
from collections import Counter, defaultdict
from copy import deepcopy
import csv
import hashlib
from datetime import date
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from scripts import assess_belgian_early_recovery as early
from scripts.artifact_io import serialize_csv
from toto_estimator.historical_import import OUTPUT_COLUMNS, HistoricalSource, canonical_season, import_historical_csvs

ROOT, PRIVATE, policy = early.ROOT, early.PRIVATE, early.policy
encode, sha = early.encode, early.sha
LEAGUE = 'Belgian Pro League'
NAMES = ('belgian_pro_league_standardized_1995_2026.csv',
         'belgian_pro_league_audit_archive_1995_2026.json',
         'belgian_pro_league_standardization_assessment.json',
         'belgian_pro_league_standardization_manifest.json')
EXPECTED = dict(INCLUDE=8592, HOLD_OUT=120, NOT_PLAYED=10, OUT_OF_SCOPE=2)


def read(path):
    return json.loads(path.read_text())


def protect(directory=PRIVATE):
    previous = early.preserve(directory)
    baseline = read(directory/'phase7_protected_before.json')
    if baseline['scope'] != 'USER_APPROVED_PHASE7_ONLY_8592_INCLUDE':
        raise ValueError('Unexpected Phase7 scope')
    for name, digest in baseline['files'].items():
        path = ROOT/name
        if not path.resolve().is_relative_to(ROOT.resolve()) or sha(path.read_bytes()) != digest:
            raise ValueError('Frozen pre-Phase7 file changed: '+name)
    prefix = baseline['planning_log']
    if sha((ROOT/'PLANNING_LOG.md').read_bytes()[:prefix['bytes']]) != prefix['sha256']:
        raise ValueError('Planning history changed')
    return dict(previous=previous,frozen_pre_phase7_entries=len(baseline['files']))


def standard_id(row):
    return sha(json.dumps([LEAGUE,row['season'],row['date'],row['home_team'],row['away_team']],
                          ensure_ascii=False,separators=(',',':')).encode())


def name_table(observed, overlaps, structure, recovery_comparison):
    """Canonical means one source-supported label per club/season, not legal merger.

    Historical source spelling is the within-season anchor. Only previously
    documented coeval correspondences may join modern/RSSSF spellings to it.
    2025/26 has no historical anchor: keep explicit modern source labels.
    """
    table = {}
    def add(season,source,original,canonical,basis):
        key=(season,source,original)
        if key in table and table[key]['canonical'] != canonical:
            raise ValueError('Ambiguous source/season name correspondence: '+repr(key))
        if not isinstance(canonical,str) or not canonical.strip() or canonical != canonical.strip():
            raise ValueError('Noncanonical team whitespace')
        table[key]=dict(season=season,source=source,original=original,canonical=canonical,basis=basis,
                        scope='SOURCE_AND_SEASON_ONLY_NOT_LEGAL_CONTINUITY')
    for row in observed['historical']:
        for side in ('home','away'):
            add(row['season'],row['source'],row[side],row[side],'ORIGINAL_HISTORICAL_LABEL')
    for path, comparison in sorted(overlaps.items()):
        season=structure['modern_sources'][path]['declared_season']
        for mapping in comparison['mapping']:
            add(season,'openfootball/belgium/'+path,mapping['modern'],mapping['historical'],
                'FROZEN_PHASE4_COEVAL_CORRESPONDENCE:'+path)
    for path, rows in observed['modern'].items():
        for row in rows:
            if row['season']=='2025/2026':
                for side in ('home','away'):
                    add(row['season'],row['source'],row[side],row[side],'ORIGINAL_MODERN_ONLY_SEASON_LABEL')
    for mapping in recovery_comparison['mapping']:
        add('2021/2022','rsssf/tablesb/belg2022.html',mapping['rsssf'],mapping['historical'],
            'FROZEN_RECOVERY2021_COEVAL_CORRESPONDENCE')
    # Verify injectivity per source: two different clubs must not collapse.
    by_source=defaultdict(dict)
    for (season,source,original), entry in table.items():
        previous=by_source[season,source].get(entry['canonical'])
        if previous is not None and previous != original:
            raise ValueError('Many-to-one club collapse within source/season')
        by_source[season,source][entry['canonical']]=original
    return table


def canonical_teams(decision, table):
    sides={'home':set(),'away':set()};bindings=[]
    for representation in decision['representations']:
        if representation['kind']=='CSV_TXT':
            row=representation['binding']
            values=[(side,row[side],row['source']) for side in ('home','away')]
        elif representation['kind']=='RSSSF_EVENT':
            event=representation['binding']; source=event['representations'][0]['source']
            values=[('home',event['diagnostic_event_key'][4],source),('away',event['diagnostic_event_key'][5],source)]
        else:
            raise ValueError('Unknown representation kind')
        for side,original,source in values:
            key=(decision['season'],source,original)
            if key not in table:
                raise ValueError('Unresolved name binding for '+decision['decision_id']+': '+repr(key))
            entry=table[key];sides[side].add(entry['canonical']);bindings.append(dict(side=side,**entry))
    if any(len(values)!=1 for values in sides.values()):
        raise ValueError('Conflicting canonical sides: '+decision['decision_id'])
    home,away=next(iter(sides['home'])),next(iter(sides['away']))
    if home==away:
        raise ValueError('Distinct source opponents collapsed')
    return home,away,bindings


def project(decision, table):
    if not policy.eligible_for_phase7(decision):
        return None, []
    season=canonical_season(decision['season']);year=int(season[:4])
    if decision['season']!=season or season!=f'{year}/{year+1}' or not 1995<=year<=2025:
        raise ValueError('Unapproved standardized season')
    match_date=decision['chosen_match_date'];day=policy.iso_day(match_date)
    if not date(year,7,1)<=day<=date(year+1,6,30):
        raise ValueError('Accepted football date outside season')
    home,away,bindings=canonical_teams(decision,table)
    goals=policy.score(decision['accepted_score'])
    if goals['outcome'] != decision['accepted_outcome']:
        raise ValueError('Accepted score/outcome mismatch')
    fields=dict(date=match_date,league=LEAGUE,season=season,home_team=home,away_team=away,
                home_goals=goals['home_goals'],away_goals=goals['away_goals'])
    fields['match_id']=standard_id(fields)
    return {key:fields[key] for key in OUTPUT_COLUMNS},bindings


def plans(decisions,table):
    result=[];identities={};ids=set()
    for decision in decisions:
        row,bindings=project(decision,table)
        if row is not None:
            identity=tuple(row[k] for k in ('league','season','date','home_team','away_team'))
            if identity in identities or row['match_id'] in ids:
                raise ValueError('Two approved events cannot be represented by the shared ID: '+decision['decision_id']+' / '+identities.get(identity,''))
            identities[identity]=decision['decision_id'];ids.add(row['match_id'])
        result.append(dict(decision=deepcopy(decision),projection=row,name_bindings=bindings))
    return result


def convert(selected, temp_parent):
    """Use shared importer directly; regular-only wrapper rejects real rematches."""
    bridge=[]
    for row in selected:
        day=date.fromisoformat(row['date']);h,a=row['home_goals'],row['away_goals']
        bridge.append(dict(Date=f'{day.day:02d}/{day.month:02d}/{day.year:04d}',Season=row['season'],
            HomeTeam=row['home_team'],AwayTeam=row['away_team'],FTHG=h,FTAG=a,FTR='H' if h>a else 'A' if h<a else 'D'))
    with tempfile.TemporaryDirectory(prefix='belgian-import-bridge-',dir=temp_parent) as tmp:
        path=Path(tmp)/'bridge.csv'
        path.write_bytes(serialize_csv(bridge,('Date','Season','HomeTeam','AwayTeam','FTHG','FTAG','FTR')))
        imported=import_historical_csvs([HistoricalSource(path,LEAGUE)])
    expected=dict(total=len(selected),accepted=len(selected),rejected=0,duplicates=0,fixtures=0,conflicts=0)
    if imported.issues or imported.summary != expected:
        raise ValueError('Shared importer changed/rejected approved events: '+repr(imported.summary))
    if Counter(tuple(r[k] for k in OUTPUT_COLUMNS) for r in imported.records)!=Counter(tuple(r[k] for k in OUTPUT_COLUMNS) for r in selected):
        raise ValueError('Shared importer transformed approved facts')
    return serialize_csv(imported.records,OUTPUT_COLUMNS),imported.summary


def parse_standard(raw):
    reader=csv.DictReader(io.StringIO(raw.decode('utf-8')),strict=True)
    if tuple(reader.fieldnames or ())!=OUTPUT_COLUMNS:
        raise ValueError('Wrong exact eight-column schema/order')
    rows=[]
    for row in reader:
        if None in row or any(value is None for value in row.values()):
            raise ValueError('CSV row width differs')
        for key in ('home_goals','away_goals'):
            value=row[key]
            if not value.isascii() or not value.isdigit() or str(int(value)) != value:
                raise ValueError('Noncanonical integer goals')
            row[key]=int(value)
        rows.append(row)
    return rows


def verify_subset(rows, prepared):
    expected={p['projection']['match_id']:p['projection'] for p in prepared if p['projection'] is not None}
    if len(expected)!=sum(p['projection'] is not None for p in prepared):
        raise ValueError('Expected ID collision')
    seen=set();order=[]
    for row in rows:
        if tuple(row)!=OUTPUT_COLUMNS or row['league']!=LEAGUE or row['match_id']!=standard_id(row) or row['match_id'] in seen:
            raise ValueError('Invalid schema/league/ID or duplicate row')
        if expected.get(row['match_id'])!=row:
            raise ValueError('Unapproved or excluded event in output')
        if not row['home_team'] or not row['away_team'] or row['home_team']==row['away_team']:
            raise ValueError('Invalid opponent identity')
        if any(type(row[key]) is not int or row[key]<0 for key in ('home_goals','away_goals')):
            raise ValueError('Invalid goals')
        policy.iso_day(row['date'])
        seen.add(row['match_id']);order.append(tuple(row[key] for key in ('league','season','date','home_team','away_team')))
    if seen!=set(expected) or order!=sorted(order):
        raise ValueError('Missing approved event or nondeterministic ordering')
    # Exact per-season AND per-stage agreement from the event-to-row association.
    by_id={p['projection']['match_id']:p['decision'] for p in prepared if p['projection'] is not None}
    return dict(rows=len(rows),unique_ids=len(seen),
                seasons=dict(Counter(r['season'] for r in rows)),
                stages=dict(Counter(by_id[r['match_id']]['stage'] for r in rows)))


def independent_registry_check(rows, decisions, table):
    """Separate projection-free comparison against authoritative frozen values.

    Chooses the registry's own preferred representation, looks up its two names
    directly, and recomputes the shared ID without calling project/standard_id.
    """
    expected={};references={}
    for d in decisions:
        if d['disposition']!='INCLUDE':
            continue
        originals=[r['binding'] for r in d['representations'] if r['kind']=='CSV_TXT']
        preferred=next((r for r in originals if r['source'].startswith('jalapic/')),originals[0] if originals else None)
        if preferred is None:
            documentary=next(r['binding'] for r in d['representations'] if r['kind']=='RSSSF_EVENT')
            source=documentary['representations'][0]['source']
        else:
            source=preferred['source']
        home=table[d['season'],source,d['home']]['canonical']
        away=table[d['season'],source,d['away']]['canonical']
        hg,ag=map(int,d['accepted_score'].split('-'))
        identity=[LEAGUE,d['season'],d['chosen_match_date'],home,away]
        identifier=hashlib.sha256(json.dumps(identity,ensure_ascii=False,separators=(',',':')).encode('utf-8')).hexdigest()
        record=dict(zip(OUTPUT_COLUMNS,[identifier,d['chosen_match_date'],LEAGUE,d['season'],home,away,hg,ag]))
        if identifier in expected:
            raise ValueError('Independent event identity collision')
        expected[identifier]=record;references[identifier]=d['decision_id']
    actual={r['match_id']:r for r in rows}
    if len(actual)!=len(rows) or actual!=expected:
        raise ValueError('Independent frozen-registry/output disagreement')
    return dict(approved_events_checked=len(expected),exact_subset=True,
                distinct_decision_references=len(set(references.values())))


def prior_ids(directory=PRIVATE):
    baseline=read(directory/'protected_before.json')['private'];ids=set();files=[];leagues=set()
    for name,digest in sorted(baseline.items()):
        if not name.endswith('.csv'):
            continue
        raw=(ROOT/name).read_bytes()
        if raw.splitlines()[0].lstrip(b'\xef\xbb\xbf')!=','.join(OUTPUT_COLUMNS).encode():
            continue
        if sha(raw)!=digest:
            raise ValueError('Previous standardized file changed')
        rows=list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))
        for row in rows:
            if row['league']==LEAGUE:
                raise ValueError('Unexpected previous Belgian output')
            ids.add(row['match_id']);leagues.add(row['league'])
        files.append(dict(path=name,records=len(rows),sha256=digest,ongoing='ongoing' in name,
                          screened='standardized' in Path(name).name))
    if len(leagues)!=12 or sum(f['records'] for f in files if f['screened'] and not f['ongoing'])!=137189 or sum(f['records'] for f in files if f['screened'] and f['ongoing'])!=258:
        raise ValueError('Previous competition population differs')
    return ids,files


def validate_public_loader(raw, rows):
    from toto_estimator.data import load_historical_data
    frame=load_historical_data(io.StringIO(raw.decode('utf-8')))
    frame['date']=frame['date'].dt.strftime('%Y-%m-%d')
    actual=frame[list(OUTPUT_COLUMNS)].to_dict(orient='records')
    if Counter(tuple(r[k] for k in OUTPUT_COLUMNS) for r in actual)!=Counter(tuple(r[k] for k in OUTPUT_COLUMNS) for r in rows):
        raise ValueError('Public loader changed standardized facts')


def build(directory=PRIVATE):
    protected=protect(directory)
    approved=read(directory/'phase6/decision_registry.json')
    # Recompute policy metadata without writing or changing any adjudication.
    rebuilt=policy.build(directory)
    for name,obj in rebuilt.items():
        if encode(obj)!=(directory/'phase6'/name).read_bytes():
            raise ValueError('Approved Phase6 reproducibility differs: '+name)
    decisions=approved['decisions']
    if dict(Counter(d['disposition'] for d in decisions))!=EXPECTED or len(decisions)!=8724:
        raise ValueError('Approved disposition population differs')
    supplemental=read(directory/'early_recovery/assessment/supplemental_registry.json')
    if supplemental['candidates'] or supplemental['distinct_conditional_events']:
        raise ValueError('Unapproved early supplement')
    observed=read(directory/'phase4/source_observations.json')
    table=name_table(observed,read(directory/'phase4/overlap_reconciliation.json'),
                     read(directory/'phase4/structural_assessment.json'),read(directory/'recovery2021/historical_comparison.json'))
    prepared=plans(decisions,table)
    selected=[p['projection'] for p in prepared if p['projection'] is not None]
    if len(selected)!=8592:
        raise ValueError('Not all8592 approved events expressible')
    raw,import_summary=convert(selected,Path(tempfile.gettempdir()))
    rows=parse_standard(raw);summary=verify_subset(rows,prepared);validate_public_loader(raw,rows)
    independent=independent_registry_check(rows,decisions,table)
    previous,previous_files=prior_ids(directory)
    if previous & {r['match_id'] for r in rows}:
        raise ValueError('Cross-competition ID collision')
    frozen_sources={r['audit_id'] for r in observed['historical']}
    frozen_sources.update(r['audit_id'] for rs in observed['modern'].values() for r in rs)
    documentary_events=read(directory/'recovery2021/event_registry.json')['events']
    frozen_sources.update(sid for event in documentary_events for sid in event['source_ids'])
    actual_ids=[sid for d in decisions for sid in d['source_ids']]
    if len(actual_ids)!=10434 or len(set(actual_ids))!=10434 or set(actual_ids)!=frozen_sources:
        raise ValueError('Source-to-event representation loss/duplication')
    earlier_documentary=read(directory/'phase6/documentary_decisions.json')
    earlier_ids={r['documentary_id'] for r in earlier_documentary['decisions']}
    if len(earlier_ids)!=30 or earlier_ids & frozen_sources:
        raise ValueError('Documentary-only population mixed with source union')
    archive_records=[]
    for plan in prepared:
        row=plan['projection'];decision=plan['decision']
        archive_records.append(dict(decision_id=decision['decision_id'],approved_phase6_decision=decision,
                                    standardized_values=row,screened_match_id=row['match_id'] if row else None,
                                    canonical_name_bindings=plan['name_bindings'],
                                    warning='RETROSPECTIVE_INTERNAL_DIAGNOSTICS_ONLY; audit includes noneligible events'))
    receipts={str(p.relative_to(directory)):read(p) for p in sorted(directory.rglob('*.provenance.json'))}
    archive=dict(events=archive_records,counts=dict(events=8724,source_representations=10434,screened=8592,dispositions=EXPECTED),
                 original_source_receipts=receipts,
                 earlier_documentary_only=earlier_documentary,never_use_unscreened_archive_as_training_data=True)
    projected=[r['standardized_values'] for r in archive_records if r['standardized_values'] is not None]
    if Counter(tuple(r[k] for k in OUTPUT_COLUMNS) for r in projected)!=Counter(tuple(r[k] for k in OUTPUT_COLUMNS) for r in rows):
        raise ValueError('Audit/CSV subset differs')
    matrix=[]
    actual_ids={r['match_id'] for r in rows}
    coverage=read(directory/'phase6/season_stage_matrix.json')['coverage']
    for season_coverage in coverage:
        season=season_coverage['season'];ds=[d for d in decisions if d['season']==season]
        actual=summary['seasons'].get(season,0);expected=sum(d['disposition']=='INCLUDE' for d in ds)
        if actual!=expected:
            raise ValueError('Season population mismatch: '+season)
        stage_rows=[]
        for stage in sorted({d['stage'] for d in ds}):
            subset=[d for d in ds if d['stage']==stage]
            stage_actual=sum(p['projection'] is not None and p['projection']['match_id'] in actual_ids
                             and p['decision']['season']==season and p['decision']['stage']==stage for p in prepared)
            if stage_actual!=sum(d['disposition']=='INCLUDE' for d in subset):
                raise ValueError('Season/stage population mismatch: '+season+' '+stage)
            stage_rows.append(dict(stage=stage,dispositions=dict(Counter(d['disposition'] for d in subset)),
                                   standardized=stage_actual))
        matrix.append(dict(season_coverage,approved_include=expected,standardized=actual,stages=stage_rows))
    pairings=defaultdict(list)
    for plan in prepared:
        if plan['projection']:
            r=plan['projection'];pairings[r['season'],r['home_team'],r['away_team']].append(plan)
    rematches=[dict(season=k[0],home=k[1],away=k[2],events=len(v),dates=[p['projection']['date'] for p in v],
                    stages=[p['decision']['stage'] for p in v],match_ids=[p['projection']['match_id'] for p in v])
               for k,v in sorted(pairings.items()) if len(v)>1]
    normalization=[entry for _,entry in sorted(table.items())]
    special=[dict(case_id=p['decision']['case_id'],decision_id=p['decision']['decision_id'],
                  disposition=p['decision']['disposition'],original_date=p['decision']['original_fixture_date'],
                  completion=p['decision']['completion_date'],standardized_values=p['projection'])
             for p in prepared if 'case_id' in p['decision']]
    assessment=dict(summary=summary,independent_registry_check=independent,season_matrix=matrix,canonical_names=normalization,
                    renamed_side_bindings=sum(b['original']!=b['canonical'] for p in prepared for b in p['name_bindings']),
                    rematch_pairs=rematches,special_cases=special,source_ids_unique=10434,
                    frozen_dispositions=EXPECTED,documentary_excluded=30,early_candidates_added=0,
                    historical_certification=False,retrospective_internal_diagnostics=True,
                    publication_timestamp_filter=False,rights_and_model_training_clearance=False,
                    no_global_aliases=True,source_path_mismatch_preserved=True)
    outputs={NAMES[0]:raw,NAMES[1]:encode(archive),NAMES[2]:encode(assessment)}
    manifest=dict(phase=7,league=LEAGUE,schema=list(OUTPUT_COLUMNS),screened_rows=len(rows),
                  match_id_convention='SHA256(UTF8 compact JSON [league,season,date,home_team,away_team]); shared importer',
                  dispositions=EXPECTED,shared_import_summary=import_summary,previous_standardized_files=previous_files,
                  previous_id_collisions=0,protected=protected,
                  implementation_sha256=sha(Path(__file__).read_bytes()),
                  frozen_phase6_registry_sha256=sha((directory/'phase6/decision_registry.json').read_bytes()),
                  source_receipts=[dict(path=str(p.relative_to(directory)),sha256=sha(p.read_bytes())) for p in sorted(directory.rglob('*.provenance.json'))],
                  outputs={n:dict(bytes=len(value),sha256=sha(value)) for n,value in outputs.items()},
                  source_rights='Private only; attribution/reuse/training restrictions preserved, no clearance inferred',
                  forecasting_claim='RETROSPECTIVE_INTERNAL_DIAGNOSTICS_NOT_LEAKAGE_FREE_HISTORICAL_PREDICTION')
    outputs[NAMES[3]]=encode(manifest)
    return outputs


def generate(directory=PRIVATE,output=None):
    output=Path(output) if output else directory
    artifacts=build(directory)
    for name,raw in artifacts.items():
        policy.review.recovery.keep(output/name,raw)
    return {n:dict(sha256=sha(raw),bytes=len(raw)) for n,raw in artifacts.items()}


def verify(directory=PRIVATE):
    with tempfile.TemporaryDirectory(prefix='belgian-phase7-regeneration-') as tmp:
        process=subprocess.run([sys.executable,'-B','-m','scripts.standardize_belgian_pro_league_results','--output',tmp],
            cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True,timeout=180)
        if process.returncode:
            raise ValueError(process.stdout+process.stderr)
        result={}
        for name in NAMES:
            saved,fresh=(directory/name).read_bytes(),(Path(tmp)/name).read_bytes()
            if saved!=fresh:
                raise ValueError('Regeneration differs: '+name)
            result[name]=dict(sha256=sha(saved),bytes=len(saved),byte_identical=True)
    return dict(artifacts=result,protected=protect(directory))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--verify',action='store_true')
    args=parser.parse_args()
    print(json.dumps(verify() if args.verify else generate(output=args.output),indent=2))
