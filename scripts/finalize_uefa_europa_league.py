"""Finalize the unchanged private CSV and reconcile source-bound club identities.

Match-name tokens are never treated as club identities. Existing project identity
IDs are reused only through an association-qualified, evidence-backed context.
"""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
from itertools import combinations
import csv,io,json,re
from pathlib import Path
from scripts import standardize_uefa_europa_league as s
PHASE=s.BASE/'phase5'
# Same association namespace as the available project identity-v1 implementation.
DOMESTIC={'ENG':'england','GER':'germany','FRA':'france','ITA':'italy','ESP':'spain','POR':'portugal','NED':'netherlands','TUR':'turkey','HUN':'hungary','BEL':'belgium'}
COUNTRIES={'England':'ENG','Germany':'GER','France':'FRA','Italy':'ITA','Spain':'ESP','Portugal':'POR','Netherlands':'NED','Turkey':'TUR','Hungary':'HUN','Belgium':'BEL','Scotland':'SCO','Wales':'WAL','Northern Ireland':'NIR','Ireland':'IRL','Republic of Ireland':'IRL','Austria':'AUT','Switzerland':'SUI','Sweden':'SWE','Norway':'NOR','Denmark':'DEN','Finland':'FIN','Iceland':'ISL','Faroe Islands':'FRO','Luxembourg':'LUX','Liechtenstein':'LIE','Andorra':'AND','San Marino':'SMR','Malta':'MLT','Gibraltar':'GIB','Greece':'GRE','Cyprus':'CYP','Israel':'ISR','Russia':'RUS','Ukraine':'UKR','Belarus':'BLR','Moldova':'MDA','Georgia':'GEO','Armenia':'ARM','Azerbaijan':'AZE','Kazakhstan':'KAZ','Estonia':'EST','Latvia':'LVA','Lithuania':'LTU','Poland':'POL','Czech Republic':'CZE','Czechia':'CZE','Slovakia':'SVK','Romania':'ROU','Bulgaria':'BUL','Albania':'ALB','Serbia':'SRB','Montenegro':'MNE','Kosovo':'KOS','Croatia':'CRO','Slovenia':'SVN','Bosnia and Herzegovina':'BIH','Bosnia-Herzegovina':'BIH','North Macedonia':'MKD','Macedonia':'MKD','USSR':'URS','Soviet Union':'URS','Czechoslovakia':'TCH','Yugoslavia':'YUG','East Germany':'GDR','West Germany':'FRG'}
def scope(value):
    code=next((v for k,v in COUNTRIES.items()if k.casefold()==str(value).casefold()),str(value).upper())
    return DOMESTIC.get(code,'assoc-'+code)if re.fullmatch('[A-Z]{3}',code)else'unknown:'+str(value)
def sensitive(label):return bool(re.search(r'steaua|\brangers(?: fc)?\b|szeged',label,re.I))and 'queens park'not in label.casefold()
def evaluate_pair(a,b,contexts,registry,positive,opponents,catalogue=None,manual=None):
    pair=tuple(sorted((a,b)))
    if manual and pair in manual:return dict(status=manual[pair]['status'],method='DIRECTED_PRIMARY_IDENTITY_EVIDENCE',evidence=manual[pair]['evidence'],qualification=manual[pair]['qualification'])
    if pair in opponents:return dict(status='DISTINCT',method='COOCCURRING_OPPONENTS',evidence=opponents[pair])
    ca,cb=contexts.get(a,set()),contexts.get(b,set())
    if s.lexical(a)==s.lexical(b)and not(ca and cb and ca.isdisjoint(cb)):
        return dict(status='ORTHOGRAPHIC_LABEL_CORRESPONDENCE',method='FULL_LABEL_ORTHOGRAPHY_ONLY',evidence=[a,b],qualification='Full-label punctuation/diacritic correspondence only; canonical IDs and sensitive seasonal continuity remain separate')
    ids_a={r['club_id']for r in registry.get(a,[])if not r['scope'].startswith('uefa-unresolved')};ids_b={r['club_id']for r in registry.get(b,[])if not r['scope'].startswith('uefa-unresolved')}
    if ids_a==ids_b and len(ids_a)==1 and not(sensitive(a)or sensitive(b)):return dict(status='ALIAS',method='EXISTING_SOURCE_QUALIFIED_PROJECT_IDENTITY',evidence=sorted(ids_a&ids_b))
    if pair in positive and not(sensitive(a)or sensitive(b)):return dict(status='ALIAS_IN_DOCUMENTED_SEASONS',method='ACCEPTED_COOEVAL_PARTICIPANT_ALIAS',evidence=positive[pair],qualification='Alias evidence is season-bound; it does not assert legal continuity across every occurrence')
    if catalogue and pair in catalogue and not(sensitive(a)or sensitive(b)):
        return dict(status='ALIAS_IN_PROVIDER_CATALOGUE',method='ASSOCIATION_QUALIFIED_PROVIDER_CLUB_ID',evidence=catalogue[pair],qualification='Recorded provider continuity only; preserve seasonal identities and do not infer legal succession')
    ca,cb=contexts.get(a,set()),contexts.get(b,set())
    if ca and cb and ca.isdisjoint(cb):return dict(status='DISTINCT_CONTEXTS',method='DISJOINT_DOCUMENTED_ASSOCIATION_CONTEXTS',evidence=[sorted(ca),sorted(cb)],qualification='Distinct source contexts, not a legal finding about every historical successor or association transfer')
    return dict(status='UNRESOLVED',method='PRESERVE_DISTINCT_SEASONAL_IDENTITIES',evidence=[],qualification='No complete positive identity or distinct-club path; abbreviation alone proves neither')
def reconcile(mappings,associations,reference,case_inventory,rows,global_rows,manual_rules=()):
    by_scope_label=defaultdict(list);by_label=defaultdict(list)
    for r in reference['mapping']:by_scope_label[(r['scope'],r['original_label'])].append(r);by_label[r['original_label']].append(r)
    declarations={r['key']:r['declarations']for r in associations['participants']};contexts=defaultdict(set);positive=defaultdict(list);links=[]
    all_labels={n for labels in case_inventory.values()for n in labels}
    for r in mappings:
        names=set(r['accepted_historical_labels'])|set(r.get('accepted_source_labels',{}))|set(r['existing_registry_candidates'])|{r['standardized_name']}
        scopes={scope(d['value'])for d in declarations[r['key']]};scopes={v for v in scopes if not v.startswith('unknown:')}
        candidates=[]
        if len(scopes)==1:
            sc=next(iter(scopes))
            for name in names:
                variants=[sc,sc+'|season:'+r['season']]
                for v in variants:candidates+=by_scope_label.get((v,name),[])
        ids=sorted({x['club_id']for x in candidates});canonical=ids[0]if len(ids)==1 else None
        link=dict(key=r['key'],season=r['season'],phase3_identity=r['phase3_identity'],display_name=r['standardized_name'],identifier_abbreviation=__import__('scripts.verify_uefa_europa_league_standardization',fromlist=['abbreviation']).abbreviation(r['standardized_name']),canonical_club_id=canonical,status='LINKED_EXISTING_PROJECT_IDENTITY'if canonical else'RETAIN_SEASONAL_IDENTITY',candidate_project_ids=ids,association_contexts=sorted(scopes),historical_aliases=sorted(names),event_ids=r['event_ids'],existing_registry_rows=sorted({x['reference_row']for x in candidates}),evidence_declarations=declarations[r['key']],impact='No CSV/name/token/match-ID changes; project IDs are reversible metadata, not new model integration')
        links.append(link)
        for n in names:contexts[n]|=scopes
        for pair in combinations(sorted(names&all_labels),2):positive[pair].append(r['key'])
    for label in all_labels:
        for r in by_label.get(label,[]):
            if not r['scope'].startswith('uefa-unresolved'):contexts[label].add(r['scope'].split('|')[0])
    opponents=defaultdict(list)
    for row in rows+global_rows:
        a,b=row['home_team'],row['away_team']
        if a in all_labels and b in all_labels:opponents[tuple(sorted((a,b)))].append(row['match_id'])
    catalogue_nodes=defaultdict(set);catalogue_keys=defaultdict(set)
    for r in links:
        for d in r['evidence_declarations']:
            if d.get('provider_club_id')and not d.get('refounded_on'):
                token=(scope(d['value']),d['provider_club_id']);catalogue_nodes[token].update(set(r['historical_aliases'])&all_labels);catalogue_keys[token].add(r['key'])
    catalogue=defaultdict(list)
    for token,names in catalogue_nodes.items():
        for pair in combinations(sorted(names),2):catalogue[pair].append(dict(provider='11footy',association=token[0],provider_club_id=token[1],participant_keys=sorted(catalogue_keys[token])))
    manual={tuple(sorted(r['labels'])):r for r in manual_rules}
    cases=[]
    for case_id,labels in sorted(case_inventory.items()):
        pairs=[dict(left=a,right=b,**evaluate_pair(a,b,contexts,by_label,positive,opponents,catalogue,manual))for a,b in combinations(sorted(set(labels)),2)]
        cases.append(dict(case_id=case_id,labels=labels,status='RESOLVED'if all(r['status']!='UNRESOLVED'for r in pairs)else'UNRESOLVED_OR_PARTIAL',pair_decisions=pairs,affected_event_ids=sorted({eid for r in links if r['display_name']in labels for eid in r['event_ids']}),match_identifier_changes=0,modelling_effect='Use qualified existing IDs only where linked; preserve unresolved and sensitive seasonal contexts separately'))
    return links,cases

def build():
    v=s.load(s.PHASE/'verification.json')
    for n,desc in v['artifacts'].items():s.require(s.sha(s.read(s.PHASE/'validated'/n))==desc['sha256'],'Accepted Phase4 changed: '+n)
    frozen=s.load(PHASE/'input_freeze.json')
    for rel,h in frozen['inputs'].items():s.require(s.sha(s.read(s.ROOT/rel))==h,'Final input changed: '+rel)
    registry=s.load(s.ROOT/'config/uefa_competition_registry.json');current=s.load(s.PHASE/'reference/global_reference.json')
    s.require(registry['competitions']=={'UEFA Cup':'uefael','UEFA Europa League':'uefael'}and registry['registration']=='LOCAL_REGISTERED'and not registry['formal_global_registration'],'Invalid local competition registry')
    s.require('uefael'not in {r[1]for r in current['competition_registry'].values()},'Global competition prefix conflict')
    rows=list(csv.DictReader(io.StringIO(s.read(s.PHASE/'validated'/s.NAME).decode())));reference=s.load(PHASE/'model_reference.json');associations=s.load(PHASE/'participant_associations.json');mappings=s.load(s.PHASE/'team_mapping_decisions.json')['teams'];assessment=s.load(s.PHASE/'team_compatibility_final.json')
    global_path=s.ROOT.parent/'toto/data/final_data/final_data_sum.csv';global_rows=list(csv.DictReader(io.StringIO(s.read(global_path).decode())))
    s.require(len(global_rows)==current['confirmed_rows']==182001 and {r['match_id']for r in global_rows}==set(current['existing_ids']),'Current global inventory changed')
    cases={f'UEL5-LOCAL-{code}':names for code,names in assessment['nonunique_local_abbreviation_groups'].items()}
    cases.update({f'UEL5-CROSS-{i:03d}':[name,*names]for i,(name,names)in enumerate(sorted(assessment['new_label_abbreviations_also_used_by_other_baseline_labels'].items()),1)})
    identity,cases=reconcile(mappings,associations,reference,cases,rows,global_rows,s.load(PHASE/'identity_research.json')['decisions'])
    require_ids=set(current['existing_ids']);s.require(not require_ids&{r['match_id']for r in rows},'Global match collision')
    prepared=list(csv.DictReader(io.StringIO(s.read(Path(reference['prepared_records'])).decode())));s.require({r['original_match_id']for r in prepared}==require_ids,'Project model registry input set differs')
    semantic={(r['recorded_date'],*sorted([r['home_club_id'],r['away_club_id']])):r['original_match_id']for r in prepared};exact={(r['date'],*sorted([s.lexical(r['home_team']),s.lexical(r['away_team'])])):r['match_id']for r in global_rows}
    mapping={r['key']:r for r in identity};links=s.load(s.PHASE/'validated/source_to_output.json')['matches'];overlap=[];qualified=0
    for link in links:
        a,b=[mapping[k]['canonical_club_id']for k in link['team_mapping_keys']];day=link['standardized_date']
        if a and b:
            qualified+=1
            if (day,*sorted([a,b]))in semantic:overlap.append(link['match_id'])
    for r in rows:
        if (r['date'],*sorted([s.lexical(r['home_team']),s.lexical(r['away_team'])]))in exact:overlap.append(r['match_id'])
    s.require(not overlap,'Identified semantic duplicate risk')
    summary=dict(status='CONDITIONAL PASS',dataset_path=str((s.BASE/'phase4/validated'/s.NAME).relative_to(s.ROOT)),dataset_sha256=s.sha(s.read(s.PHASE/'validated'/s.NAME)),csv_changed=False,include=11422,excluded=68,seasons=36,main=6506,qualifying=4916,neutral_format=38,identity_cases=len(cases),identity_case_results=dict(Counter(r['status']for r in cases)),seasonal_identity_results=dict(Counter(r['status']for r in identity)),globally_linked_matches=qualified,global_rows=len(global_rows),prospective_combined_rows=len(global_rows)+len(rows),local_match_id_collisions=0,global_match_id_collisions=0,identified_semantic_overlap=[],semantic_uniqueness_fully_certified=False,local_registration=True,formal_global_registration=False,limits=['Formal registration requires a separately authorized original-worktree registry extension','Unresolved cross-competition aliases/continuity remain isolated; semantic absence of overlap is certified only for supported mappings and literal names','No model training, combined integration or public data redistribution authorized'])
    return {'final_dataset.json':s.wire(summary),'club_identity_crosswalk.json':s.wire(dict(mapping=identity,existing_reference_sha256=s.sha(s.read(PHASE/'model_reference.json')))),'identity_case_dispositions.json':s.wire(dict(cases=cases)),'registration_proposal.json':s.wire(dict(local_registry=registry,upstream_target='scripts/build_final_data_sum.py:COMPETITIONS',add_entries={'UEFA Cup':['uefa','uefael'],'UEFA Europa League':['uefa','uefael']},preserve_existing_entries=True,formal_global_registration=False))}

def run(output=PHASE/'final',check=False):
    output=Path(output).resolve();s.require(output.is_relative_to(PHASE.resolve())or output.is_relative_to(Path('/private/tmp')),'Private output required');artifacts=build()
    if check:
        for n,raw in artifacts.items():s.require(s.read(output/n)==raw,'Final artifact differs: '+n)
    else:
        s.require(not any((output/n).exists()for n in artifacts),'Refusing overwrite');output.mkdir(parents=True,exist_ok=True)
        for n,raw in artifacts.items():
            with(output/n).open('xb')as f:f.write(raw)
    return {n:s.sha(raw)for n,raw in artifacts.items()}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=PHASE/'final');p.add_argument('--check',action='store_true');a=p.parse_args();print(json.dumps(run(a.output,a.check),indent=2))
