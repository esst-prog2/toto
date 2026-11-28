"""Private, deterministic Phase 4 projection using the confirmed final-data conventions.

The upstream identifier implementation is an immutable code snapshot, not a new
identifier architecture. Its proposed Europa League registry entry stays local.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from datetime import date
import hashlib
import importlib.util
import json
import mmap
from pathlib import Path
import re
import unicodedata
from scripts.artifact_io import serialize_csv
from toto_estimator.match_schema import canonical_match_id

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'data/private/europe/europa_league'
PHASE = BASE / 'phase4'
P3 = BASE / 'phase3'
NAME = 'uefa_europa_league_standardized_1990_2026.csv'
COLUMNS = ('match_id','country','league','season','date','home_team','away_team','home_goals','away_goals','neutral_venue')

def read(path):
    with Path(path).open('rb') as f:
        if not Path(path).stat().st_size: return b''
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as m: return m[:]
def load(path): return json.loads(read(path))
def sha(raw): return hashlib.sha256(raw).hexdigest()
def wire(value): return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2)+'\n').encode()
def require(value, message):
    if not value: raise ValueError(message)
def lexical(name):
    return ''.join(c for c in unicodedata.normalize('NFD',name.casefold()) if c.isalnum() and not unicodedata.combining(c))
def mapping_key(season, identity): return json.dumps([season,identity],ensure_ascii=False,separators=(',',':'))
def identifier_module():
    path=PHASE/'reference/build_final_data_sum.py'
    require(sha(read(path))==load(PHASE/'reference/global_reference.json')['code_sha256'],'Identifier implementation changed')
    spec=importlib.util.spec_from_file_location('uel_final_conventions',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def prepare_mapping(events, reference):
    """Exact or accent/punctuation-only existing-label correspondence; no fuzzy merger."""
    labels=defaultdict(Counter); participants=defaultdict(list)
    for e in events:
        if e['disposition']!='INCLUDE': continue
        for i,side in enumerate(('home','away')):
            key=mapping_key(e['season'],e['team_identities'][i]);labels[key][e['historical_'+side].strip()]+=1;participants[key].append(e['event_id'])
    existing=defaultdict(list)
    for name in reference['teams']: existing[lexical(name)].append(name)
    result=[]
    for key,names in sorted(labels.items()):
        exact=sorted(n for n in names if n in reference['teams'])
        variants=sorted({n for label in names for n in existing[lexical(label)]})
        candidates=exact or variants
        preferred=sorted(names,key=lambda n:(-names[n],n))[0]
        selected=preferred if preferred in candidates else candidates[0] if len(candidates)==1 else preferred
        result.append(dict(key=key,season=json.loads(key)[0],phase3_identity=json.loads(key)[1],accepted_historical_labels=dict(sorted(names.items())),standardized_name=selected,existing_registry_candidates=candidates,basis='EXACT_EXISTING_LABEL' if selected in exact else 'LEXICAL_EXISTING_LABEL' if selected in variants else 'PRESERVED_PHASE3_LABEL',identity_scope='Seasonal accepted identity; display correspondence is not a legal-successor assertion',event_ids=sorted(set(participants[key]))))
    return result

def project(event, mapping, convention, prefix, correction=None):
    require(event['disposition']=='INCLUDE','Excluded event cannot be standardized')
    require(all(event['modelling_eligibility'][k] for k in ('outcome','goals','chronological')),'Ineligible record')
    score=event['score']['regulation_time']
    require(isinstance(score,list) and len(score)==2 and all(type(x) is int and x>=0 for x in score),'Invalid regulation score')
    require(event['duration']['regulation_completed'] is True,'Regulation incomplete')
    outcome='1' if score[0]>score[1] else '2' if score[0]<score[1] else 'X'
    require(outcome==event['score']['regulation_outcome'],'Regulation outcome differs')
    day=event['date']['date']
    if correction is not None:
        require(correction['event_id']==event['event_id'] and correction['field']=='date' and correction['before']==day and correction['after'] in event['date']['original_dates'] and bool(correction['evidence']),'Unbound historical correction')
        day=correction['after']
    season=event['season'];parsed=date.fromisoformat(day)
    require(parsed.isoformat()==day and re.fullmatch(r'\d{4}/\d{4}',season) and int(season[5:])==int(season[:4])+1 and parsed.year in map(int,season.split('/')),'Invalid playing date/season')
    require('ESTIMAT' not in event['date']['confidence'].upper(),'Estimated date prohibited')
    names=[mapping[mapping_key(season,t)]['standardized_name'] for t in event['team_identities']]
    require(all(isinstance(n,str) and n==n.strip() and n for n in names) and names[0]!=names[1],'Invalid participant mapping')
    neutral=event['venue']['neutral_venue'];require(type(neutral) is int and neutral in (0,1),'Unestablished official format')
    league=event['competition'];require(league==('UEFA Cup' if int(season[:4])<=2008 else 'UEFA Europa League'),'Historical competition changed')
    mid=prefix+convention.season_code(season)+convention.date_code(day)+''.join(convention.team_code(n) for n in names)
    require(len(mid)==24 and mid.isalnum() and mid==mid.lower(),'Invalid UEFA identifier')
    row=dict(zip(COLUMNS,(mid,'uefa',league,season,day,*names,*score,neutral)))
    return row,outcome,canonical_match_id(league,season,day,*names)

def build():
    approval=load(PHASE/'approval.json')
    for rel,h in approval['phase3_inputs'].items(): require(sha(read(P3/rel))==h,'Accepted input changed: '+rel)
    for rel,h in approval['phase4_inputs'].items(): require(sha(read(PHASE/rel))==h,'Standardization binding changed: '+rel)
    reference=load(PHASE/'reference/global_reference.json');convention=identifier_module();policy=load(PHASE/'code_policy.json');prefix=policy['proposed_competition_prefix']
    require(prefix not in {v[1] for v in reference['competition_registry'].values()},'Competition prefix already allocated')
    events=load(P3/'final/adjudicated_inventory.json')['events'];require(len(events)==11490,'Accepted population changed')
    mappings=load(PHASE/'team_mapping_decisions.json')['teams'];mapping={r['key']:r for r in mappings};require(len(mapping)==len(mappings),'Duplicate team mapping')
    corrections=load(PHASE/'historical_corrections.json')['corrections'];correction_by_id={r['event_id']:r for r in corrections};require(len(correction_by_id)==len(corrections),'Duplicate historical correction')
    for r in corrections:require(r['phase3_inventory_sha256']==approval['phase3_inputs']['final/adjudicated_inventory.json'],'Correction input binding changed')
    rows=[];links=[];excluded=[];neutral=[]
    for e in events:
        if e['disposition']!='INCLUDE': excluded.append(e);continue
        row,outcome,original=project(e,mapping,convention,prefix,correction_by_id.get(e['event_id']));rows.append(row)
        links.append(dict(match_id=row['match_id'],original_match_id=original,event_id=e['event_id'],previous_conditional_events=e['previous_conditional_event_ids'],observations=e['observations'],source_evidence=e['source_evidence'],historical_names=[e['historical_home'],e['historical_away']],team_identities=e['team_identities'],team_mapping_keys=[mapping_key(e['season'],t) for t in e['team_identities']],scope=e['scope'],stage=e['stage'],historical_stage_labels=e['historical_stage_labels'],source_legs=e['source_legs'],replay=e['replay'],outcome=outcome,decision_ids=e['decision_ids'],date_evidence=e['date'],standardized_date=row['date'],standardization_corrections=[correction_by_id[e['event_id']]] if e['event_id'] in correction_by_id else [],score_evidence=e['score'],duration=e['duration'],administrative_result=e['administrative_result'],administrative_evidence=e['administrative_evidence'],phase3_inventory_sha256=approval['phase3_inputs']['final/adjudicated_inventory.json']))
        neutral.append(dict(match_id=row['match_id'],event_id=e['event_id'],nominal_home=e['historical_home'],nominal_away=e['historical_away'],venue=e['venue'],semantics='OFFICIAL_COMPETITION_FORMAT_NOT_PHYSICAL_HOME_ADVANTAGE'))
    rows.sort(key=lambda r:tuple(r[k] for k in ('country','league','season','date','home_team','away_team')))
    ids=[r['match_id'] for r in rows];require(len(ids)==len(set(ids))==11422,'Match identifier collision or lost match')
    require(not set(ids).intersection(reference['existing_ids']),'Global identifier collision')
    positions={r['match_id']:i+2 for i,r in enumerate(rows)};links.sort(key=lambda r:positions[r['match_id']]);neutral.sort(key=lambda r:positions[r['match_id']])
    for r in links:r['csv_physical_line']=positions[r['match_id']]
    require(not {r['original_match_id'] for r in links}.intersection(reference['existing_identity_hashes']),'Existing global fixture overlap')
    coverage=[]
    for year in range(1990,2026):
        season=f'{year}/{year+1}';ls=[r for r in links if mapping[r['team_mapping_keys'][0]]['season']==season]
        rs=[r for r in rows if r['season']==season];ex=[e for e in excluded if e['season']==season]
        coverage.append(dict(season=season,include=len(rs),main=sum(r['scope']=='MAIN' for r in ls),qualifying=sum(r['scope']=='QUALIFYING' for r in ls),excluded=len(ex),neutral_format=sum(r['neutral_venue']==1 for r in rs),regulation_scores=len(rs),supported_dates=len(rs),estimated_dates=0))
    codes=defaultdict(set)
    for r in mappings:codes[convention.team_code(r['standardized_name'])].add(r['standardized_name'])
    code_groups={code:sorted(names) for code,names in sorted(codes.items()) if len(names)>1}
    summary=dict(historical_date_corrections=len(corrections),phase=4,status='CONDITIONAL PASS',include=len(rows),excluded=len(excluded),seasons=len(coverage),main=sum(r['main'] for r in coverage),qualifying=sum(r['qualifying'] for r in coverage),neutral_format=sum(r['neutral_venue']==1 for r in rows),regulation_only=True,estimated_dates=0,global_baseline_rows=reference['confirmed_rows'],local_identifier_collisions=0,global_identifier_collisions=0,overlapping_global_fixtures=0,dry_run_combined_rows=reference['confirmed_rows']+len(rows),competition_prefix=prefix,prefix_status=policy['status'],distinct_team_labels=len({r['standardized_name'] for r in mappings}),nonunique_abbreviation_groups=len(code_groups),limits=['Proposed Europa League prefix is not yet in the approved global registry','Four-character abbreviations are not globally unique club identifiers; seasonal identities and full labels remain separate','Standardization verification does not certify every historical source fact or redistribution right'])
    require((summary['main'],summary['qualifying'],summary['neutral_format'],len(excluded))==(6506,4916,38,68),'Accepted counters differ')
    schema=dict(status='CONFIRMED',columns=COLUMNS,encoding='UTF-8 without BOM',line_ending='LF',ordering=['country','league','season','date','home_team','away_team'],country='uefa',historical_competition_labels=['UEFA Cup','UEFA Europa League'],neutral_venue='Approved official-format semantics: 0 hosted, 1 neutral format; physical evidence remains separate',competition_registry_extension=policy,reference_code_sha256=reference['code_sha256'])
    audit=dict(status='PASS',row_count=len(rows),valid_unique_identifiers=len(set(ids)),local_collisions=[],global_collisions=[],global_reference_rows=reference['confirmed_rows'],unusable_team_names=[],nonunique_team_abbreviations=code_groups,abbreviation_semantics='Name-derived tokens, not unique club registry IDs; collisions cannot be resolved by merging clubs',proposed_prefix=prefix,prefix_registered=False,original_sha256_identity_crosswalk=True)
    return {'historical_corrections.json':wire(dict(corrections=corrections)),NAME:serialize_csv(rows,COLUMNS),'source_to_output.json':wire(dict(matches=links)),'match_id_crosswalk.csv':serialize_csv([dict(original_match_id=r['original_match_id'],new_match_id=r['match_id']) for r in links],('original_match_id','new_match_id')),'excluded_events.json':wire(dict(events=excluded,phase3_contexts_sha256=approval['phase3_inputs']['final/historical_contexts.json'])),'neutral_venue.json':wire(dict(matches=neutral)),'season_coverage.csv':serialize_csv(coverage,tuple(coverage[0])),'team_mapping.json':wire(dict(teams=[dict(r,team_code=convention.team_code(r['standardized_name'])) for r in mappings],nonunique_abbreviations=code_groups)),'schema_compatibility.json':wire(schema),'identifier_audit.json':wire(audit),'summary.json':wire(summary),'score_period_audit.json':wire(dict(status='PASS',checked=len(rows),regulation_only=True,score_methods=dict(Counter(r['score_evidence']['method'] for r in links)),administrative_results_kept_separate=sum(bool(r['administrative_evidence']) for r in links),extra_time_abandonments=sum(r['duration'].get('abandonment_period')=='EXTRA_TIME' for r in links),details='Every result compared to accepted regulation fields; source periods and awards retained through immutable Phase3 lineage'))}

def run(output=PHASE/'validated',check=False):
    output=Path(output).resolve();require(output.is_relative_to(PHASE.resolve()) or output.is_relative_to(Path('/private/tmp')),'Private or temporary output required')
    artifacts=build()
    if check:
        for n,raw in artifacts.items():require(read(output/n)==raw,'Reproduction differs: '+n)
    else:
        require(not any((output/n).exists() for n in artifacts),'Refusing to overwrite output');output.mkdir(parents=True,exist_ok=True)
        for n,raw in artifacts.items():
            with (output/n).open('xb') as f:f.write(raw)
    return {n:dict(bytes=len(raw),sha256=sha(raw)) for n,raw in artifacts.items()}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=PHASE/'validated');p.add_argument('--check',action='store_true');a=p.parse_args();print(json.dumps(run(a.output,a.check),indent=2))
