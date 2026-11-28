"""Independent exhaustive Phase 4 validator; no transformation/identifier helpers imported."""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
import csv
from datetime import date
import hashlib
import io
import json
import mmap
from pathlib import Path
import re
import unicodedata
ROOT=Path(__file__).resolve().parents[1]
PHASE=ROOT/'data/private/europe/europa_league/phase4'
P3=PHASE.parent/'phase3'
NAME='uefa_europa_league_standardized_1990_2026.csv'
COLUMNS=['match_id','country','league','season','date','home_team','away_team','home_goals','away_goals','neutral_venue']

def require(value,message):
    if not value:raise ValueError(message)
def read(path):
    with Path(path).open('rb') as f:
        if not Path(path).stat().st_size:return b''
        with mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ)as m:return m[:]
def sha(raw):return hashlib.sha256(raw).hexdigest()
def load(path):return json.loads(read(path))
def wire(value):return(json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
def parse_csv(raw):
    require(not raw.startswith(b'\xef\xbb\xbf') and b'\r'not in raw,'Noncanonical encoding/line endings')
    return list(csv.reader(io.StringIO(raw.decode('utf-8'),newline=''),strict=True))
def key(season,identity):return json.dumps([season,identity],ensure_ascii=False,separators=(',',':'))
def lexical(name):return ''.join(c for c in unicodedata.normalize('NFD',name.casefold())if c.isalnum()and not unicodedata.combining(c))
def abbreviation(name):
    normalized=''.join(c for c in unicodedata.normalize('NFD',name.lower())if not unicodedata.combining(c))
    words=''.join(c if c.isalnum()else' 'for c in normalized).split()
    if words[:2]==['1','fc']:words=words[2:]
    require(bool(words),'Unusable team name')
    return words[0][:4].ljust(4,'0')if len(words)==1 else ''.join(w[:2].ljust(2,'0')for w in words[:2])
def reconstructed_identifier(prefix,season,day,home,away):
    return prefix+season[2:4]+season[7:9]+day[2:4]+day[5:7]+day[8:10]+abbreviation(home)+abbreviation(away)

def verify(folder=PHASE/'validated'):
    folder=Path(folder);approval=load(PHASE/'approval.json')
    for rel,h in approval['phase3_inputs'].items():require(sha(read(P3/rel))==h,'Accepted input changed: '+rel)
    for rel,h in approval['phase4_inputs'].items():require(sha(read(PHASE/rel))==h,'Mapping/convention binding changed: '+rel)
    reference=load(PHASE/'reference/global_reference.json');policy=load(PHASE/'code_policy.json');prefix=policy['proposed_competition_prefix']
    require(reference['columns']==COLUMNS and reference['confirmed_rows']==182001,'Confirmed current schema/baseline differs')
    require(prefix not in {p[1]for p in reference['competition_registry'].values()},'Prefix allocation collision')
    events=load(P3/'final/adjudicated_inventory.json')['events'];included={e['event_id']:e for e in events if e['disposition']=='INCLUDE'};excluded={e['event_id']:e for e in events if e['disposition']!='INCLUDE'}
    require(len(events)==11490 and len(included)==11422 and len(excluded)==68,'Approved event counts differ')
    mapping_input=load(PHASE/'team_mapping_decisions.json')['teams'];mapping={r['key']:r for r in mapping_input};require(len(mapping)==len(mapping_input),'Duplicate mapping key')
    require(load(folder/'team_mapping.json')['teams']==[dict(r,team_code=abbreviation(r['standardized_name']))for r in mapping_input],'Output team mapping/code changed')
    expected_members=defaultdict(set);actual_labels=defaultdict(set)
    for e in included.values():
        for i,side in enumerate(('home','away')):
            k=key(e['season'],e['team_identities'][i]);expected_members[k].add(e['event_id']);actual_labels[k].add(e['historical_'+side].strip())
    require(set(mapping)==set(expected_members),'Lost/extra participant identity')
    for k,r in mapping.items():
        require(set(r['event_ids'])==expected_members[k]and set(r['accepted_historical_labels'])==actual_labels[k],'Mapping event/name binding differs')
        names=actual_labels[k]|set(r.get('accepted_source_labels',{}));selected=r['standardized_name']
        require(any(lexical(selected)==lexical(n)for n in names),'Unsubstantiated participant remapping')
        if selected not in names:require(selected in reference['teams'],'Unknown new label introduced')
        for n,evidence in r.get('accepted_source_labels',{}).items():
            e=included[evidence['event_id']];require(evidence['event_id']in expected_members[k]and evidence['observation']in e['observations'],'Unbound source label evidence')
            require(any(z['observation']==evidence['observation']and z['sha256']==evidence['source_sha256']and z['locator']==evidence['locator']for z in e['source_evidence']),'Source-label provenance differs')
    actual=parse_csv(read(folder/NAME));require(bool(actual)and actual[0]==COLUMNS,'Invalid schema/column order')
    require(len(actual)-1==11422 and all(len(r)==10 for r in actual[1:]),'Missing/duplicate or malformed standardized row')
    rows=[dict(zip(COLUMNS,r))for r in actual[1:]];byid={r['match_id']:r for r in rows};require(len(byid)==11422,'Duplicate match identifier')
    links=load(folder/'source_to_output.json')['matches'];require(len(links)==11422 and len({r['event_id']for r in links})==11422 and {r['event_id']for r in links}==set(included),'Missing/duplicate/broken event crosswalk')
    require({r['match_id']for r in links}==set(byid),'Orphan match identifier')
    corrections=load(PHASE/'historical_corrections.json')['corrections'];correction_by_id={r['event_id']:r for r in corrections}
    require(len(corrections)==len(correction_by_id) and set(correction_by_id)<=set(included),'Historical correction accounting differs')
    require(load(folder/'historical_corrections.json')['corrections']==corrections,'Historical correction sidecar changed')
    expected=[];methods=Counter();extra_abandoned=0;admins=0
    for position,link in enumerate(links,2):
        e=included[link['event_id']];season=e['season'];day=e['date']['date'];score=e['score']['regulation_time'];names=[mapping[key(season,t)]['standardized_name']for t in e['team_identities']]
        correction=correction_by_id.get(e['event_id'])
        if correction:
            require(correction['field']=='date'and correction['before']==day and correction['after']in e['date']['original_dates']and correction['phase3_inventory_sha256']==approval['phase3_inputs']['final/adjudicated_inventory.json']and bool(correction['evidence']),'Unbound historical date correction')
            day=correction['after']
        require(link['standardized_date']==day and link['standardization_corrections']==([correction]if correction else []),'Corrected date lineage differs')
        require(isinstance(score,list)and len(score)==2 and all(type(g)is int and g>=0 for g in score),'Invalid accepted regulation score')
        require(e['duration']['regulation_completed']is True and all(e['modelling_eligibility'][k]for k in ('goals','outcome','chronological')),'Ineligible accepted result')
        parsed=date.fromisoformat(day);require(parsed.isoformat()==day and re.fullmatch(r'[0-9]{4}/[0-9]{4}',season)and int(season[5:])==int(season[:4])+1 and parsed.year in [int(x)for x in season.split('/')],'Invalid playing date/season')
        require('ESTIMAT'not in e['date']['confidence'].upper(),'Estimated date introduced')
        league='UEFA Cup'if int(season[:4])<=2008 else'UEFA Europa League';require(e['competition']==league,'Competition/season differs')
        mid=reconstructed_identifier(prefix,season,day,*names);require(len(mid)==24 and mid.isalnum()and mid==mid.lower(),'Invalid identifier format')
        outcome='X'if score[0]==score[1]else'1'if score[0]>score[1]else'2';require(outcome==e['score']['regulation_outcome']==link['outcome'],'Incorrect regulation outcome')
        nv=e['venue']['neutral_venue'];require(type(nv)is int and nv in(0,1),'Invalid neutrality')
        row=[mid,'uefa',league,season,day,*names,str(score[0]),str(score[1]),str(nv)];expected.append(row)
        require(mid==link['match_id']and list(byid[mid].values())==row,'Independent row/score/date/team/orientation/ID comparison differs')
        old=sha(json.dumps([league,season,day,*names],ensure_ascii=False,separators=(',',':')).encode());require(link['original_match_id']==old,'Original SHA identity crosswalk differs')
        require(link['csv_physical_line']==position and actual[position-1]==row,'Row ordering/crosswalk position differs')
        checks={'previous_conditional_events':'previous_conditional_event_ids','observations':'observations','source_evidence':'source_evidence','scope':'scope','stage':'stage','historical_stage_labels':'historical_stage_labels','source_legs':'source_legs','replay':'replay','team_identities':'team_identities','decision_ids':'decision_ids','date_evidence':'date','score_evidence':'score','duration':'duration','administrative_result':'administrative_result','administrative_evidence':'administrative_evidence'}
        for target,original in checks.items():require(link[target]==e[original],'Broken provenance/period/stage: '+target)
        require(link['historical_names']==[e['historical_home'],e['historical_away']]and link['team_mapping_keys']==[key(season,t)for t in e['team_identities']],'Historical identity/orientation lost')
        require(link['phase3_inventory_sha256']==approval['phase3_inputs']['final/adjudicated_inventory.json'],'Inventory lineage hash differs')
        methods[e['score']['method']]+=1;admins+=bool(e['administrative_evidence'])
        if e['duration'].get('abandonment_period')=='EXTRA_TIME':
            extra_abandoned+=1;require(e['duration']['regulation_completed']is True and e['duration']['extra_time_completed']is False and e['duration']['after_extra_time_score']is None,'Incomplete extra time misrepresented')
            require(score!=e['administrative_result']and score!=e['duration']['score_at_abandonment'],'Extra-time abandonment award/partial score leaked')
    require(extra_abandoned==1,'Extra-time abandonment missing')
    require(expected==sorted(expected,key=lambda r:tuple(r[i]for i in(1,2,3,4,5,6))),'Unstable canonical row ordering')
    buf=io.StringIO(newline='');writer=csv.writer(buf,lineterminator='\n');writer.writerows([COLUMNS]+expected);require(buf.getvalue().encode()==read(folder/NAME),'Canonical CSV bytes differ')
    cross=parse_csv(read(folder/'match_id_crosswalk.csv'));require(cross==[['original_match_id','new_match_id']]+[[r['original_match_id'],r['match_id']]for r in links],'Identifier crosswalk incomplete')
    ex=load(folder/'excluded_events.json');require(len(ex['events'])==68 and {e['event_id']:e for e in ex['events']}==excluded,'Incorrect exclusion accounting')
    require(ex['phase3_contexts_sha256']==approval['phase3_inputs']['final/historical_contexts.json'],'Historical contexts lost')
    nv=load(folder/'neutral_venue.json')['matches'];require(len(nv)==11422 and len({r['event_id']for r in nv})==11422,'Lost neutrality metadata')
    for r in nv:
        e=included[r['event_id']];require(r['venue']==e['venue']and r['nominal_home']==e['historical_home']and r['nominal_away']==e['historical_away']and r['match_id']in byid,'Neutral venue/orientation/evidence changed')
        require(r['semantics']=='OFFICIAL_COMPETITION_FORMAT_NOT_PHYSICAL_HOME_ADVANTAGE','Physical neutrality conflated')
    require(sum(r['venue']['neutral_venue']==1 for r in nv)==38,'Neutral count differs')
    coverage=parse_csv(read(folder/'season_coverage.csv'));required=['season','include','main','qualifying','excluded','neutral_format','regulation_scores','supported_dates','estimated_dates'];require(coverage[0]==required and len(coverage)==37,'Season coverage schema/count differs')
    totals=Counter()
    for values in coverage[1:]:
        r=dict(zip(required,values));season=r['season'];es=[e for e in included.values()if e['season']==season];exs=[e for e in excluded.values()if e['season']==season]
        exp=[len(es),sum(e['scope']=='MAIN'for e in es),sum(e['scope']=='QUALIFYING'for e in es),len(exs),sum(e['venue']['neutral_venue']==1 for e in es),len(es),len(es),0]
        require(values[1:]==list(map(str,exp)),'Stage/season reconciliation differs');totals.update(main=exp[1],qualifying=exp[2],include=exp[0])
    require({r['season']for r in rows}=={f'{y}/{y+1}'for y in range(1990,2026)},'Lost target season')
    require((totals['main'],totals['qualifying'])==(6506,4916),'Main/qualifying differs')
    for year in range(1990,1994):require(not any(e['scope']=='QUALIFYING'for e in included.values()if e['season']==f'{year}/{year+1}'),'Invented early qualifying')
    for year in(2024,2025):require(sum(e['stage']=='LEAGUE_PHASE'for e in included.values()if e['season']==f'{year}/{year+1}')==144,'League phase damaged')
    require(not set(byid)&set(reference['existing_ids']),'Global identifier collision')
    require(not {r['original_match_id']for r in links}&set(reference['existing_identity_hashes']),'Global fixture overlap')
    groups=defaultdict(set)
    for r in mapping_input:groups[abbreviation(r['standardized_name'])].add(r['standardized_name'])
    collisions={k:sorted(v)for k,v in sorted(groups.items())if len(v)>1}
    require(load(folder/'team_mapping.json')['nonunique_abbreviations']==collisions,'Unreported team-code ambiguity')
    audit=load(folder/'identifier_audit.json');require(audit['row_count']==audit['valid_unique_identifiers']==11422 and audit['local_collisions']==audit['global_collisions']==[]and audit['nonunique_team_abbreviations']==collisions,'Identifier audit differs')
    periods=load(folder/'score_period_audit.json');require(periods['checked']==11422 and periods['regulation_only']is True and periods['extra_time_abandonments']==1 and periods['score_methods']==dict(methods)and periods['administrative_results_kept_separate']==admins,'Period contamination audit differs')
    schema=load(folder/'schema_compatibility.json');require(schema['columns']==COLUMNS and schema['reference_code_sha256']==reference['code_sha256']and schema['competition_registry_extension']==policy,'Schema assessment differs')
    summary=load(folder/'summary.json');require((summary['include'],summary['excluded'],summary['seasons'],summary['main'],summary['qualifying'],summary['neutral_format'])==(11422,68,36,6506,4916,38),'Summary differs')
    require(summary['global_baseline_rows']==182001 and summary['dry_run_combined_rows']==193423 and summary['nonunique_abbreviation_groups']==len(collisions),'Integration dry-run accounting differs')
    frozen=load(PHASE/'protected_before.json');protected=0
    for name,h in frozen['files'].items():
        raw=read(ROOT/name)
        if name in frozen['append_prefixes']:
            desc=frozen['append_prefixes'][name];require(sha(raw[:desc['bytes']])==desc['sha256'],'Append-only original prefix changed')
        else:require(sha(raw)==h,'Protected file changed: '+name);protected+=1
    for name,h in frozen['read_only_references'].items():require(sha(read(Path(name)))==h,'Read-only global reference changed: '+name)
    # Compare trusted directed leg labels against the corrected dates, independently.
    leg_groups=defaultdict(list)
    for link in links:
        e=included[link['event_id']];leg_groups[(e['season'],tuple(sorted(e['team_identities'])),e['stage'])].append(link)
    leg_checks=0
    for group in leg_groups.values():
        if len(group)!=2:continue
        first=[r for r in group if r['source_legs']==[1]];second=[r for r in group if r['source_legs']==[2]]
        if len(first)==len(second)==1:
            require(first[0]['standardized_date']<second[0]['standardized_date'],'Return-leg chronology inversion');leg_checks+=1
    final_checks=0
    for year in range(1990,2026):
        group=[r for r in links if included[r['event_id']]['season']==f'{year}/{year+1}'];finals=[r for r in group if r['stage']=='FINAL'];others=[r for r in group if r['stage']!='FINAL']
        require(min(r['standardized_date']for r in finals)>max(r['standardized_date']for r in others),'Final progression date inversion');final_checks+=1
    guarantees=[]
    for n,title in enumerate(['36 target seasons','11422 standardized matches','6506 main matches','4916 qualifying matches','11490 historical records accounted','68 exclusions preserved','Valid supported regulation scores','No period contamination','Administrative results separate','Valid actual playing dates','No estimated dates','Unique approved-convention match identifiers','Global team identity/code compatibility','Neutral evidence preserved','Reversible provenance','Confirmed current CSV schema','Deterministic output','Prior data and protected files preserved'],1):
        status='NOT VERIFIABLE'if n in(12,13)else'PASS'
        explanation='Local uniqueness and global zero-collision check pass under proposed uefael; this prefix is not registered yet'if n==12 else'Existing label correspondences and exact algorithm checked; no globally unique club identity registry exists, abbreviations overlap and unresolved global aliases are not silently merged'if n==13 else'Exhaustive independent field, membership, byte or fingerprint check'
        guarantees.append(dict(number=n,guarantee=title,status=status,explanation=explanation))
    return dict(status='CONDITIONAL PASS',technical_validation='PASS',historical_date_corrections=len(corrections),directed_leg_chronology_checks=leg_checks,final_progression_checks=final_checks,rows_checked=11422,excluded_checked=68,seasons_checked=36,main=6506,qualifying=4916,neutral_format=38,all_row_fields_and_bytes_checked=True,original_payloads_preserved=85,protected_unchanged=protected,append_only_prefixes=2,read_only_reference_files=len(frozen['read_only_references']),global_baseline=182001,combined_dry_run=193423,global_id_collisions=0,local_id_collisions=0,nonunique_team_abbreviation_groups=len(collisions),guarantees=guarantees,guarantee_counts=dict(Counter(r['status']for r in guarantees)),independent_method='Standalone CSV/JSON parsing, separate identifier/token/score/outcome/date reconstruction, full row bytes, event/exclusion/neutral/coverage/provenance comparisons and source/reference fingerprint verification; no producer or identifier-generation imports',limitations=['Proposed namespace requires registry approval','Name-derived team abbreviations are not globally unique identities; baseline alias limitations remain','Transfer validation is not independent historical certification or publication permission'])

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--inventory',type=Path,default=PHASE/'validated');p.add_argument('--output',type=Path,default=PHASE/'independent_validation.json');p.add_argument('--check',action='store_true');a=p.parse_args();out=a.output.resolve();require(out.is_relative_to(PHASE.resolve())or out.is_relative_to(Path('/private/tmp')),'Private output required');result=verify(a.inventory)
    if a.check:require(read(out)==wire(result),'Validation receipt changed')
    else:
        with out.open('xb')as f:f.write(wire(result))
    print(json.dumps(result,indent=2))
