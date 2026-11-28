"""Independent final identity/registration audit on the unchanged accepted CSV."""
import argparse,csv,io,json,re
from collections import Counter,defaultdict
from itertools import combinations
from pathlib import Path
from scripts import verify_uefa_europa_league_standardization as v
# Shared declarative association policy only; no finalizer transformation imported.
from scripts.finalize_uefa_europa_league import COUNTRIES,DOMESTIC
PHASE=v.PHASE.parent/'phase5'
def country_scope(value):
 code={k.lower():c for k,c in COUNTRIES.items()}.get(str(value).lower(),str(value).upper())
 return DOMESTIC.get(code,'assoc-'+code)if re.fullmatch('[A-Z]{3}',code)else'unknown:'+str(value)
def sensitive(n):return bool(re.search(r'steaua|\brangers(?: fc)?\b|szeged',n,re.I))and'queens park'not in n.casefold()
def validate_local_registry(r,upstream):
 v.require(r['registration']=='LOCAL_REGISTERED'and r['formal_global_registration']is False,'Unregistered or falsely globally registered code')
 v.require(r['competitions']=={'UEFA Cup':'uefael','UEFA Europa League':'uefael'}and r['identifier_length']==24 and r['country']=='uefa'and set(r['scopes'])=={'MAIN','QUALIFYING'},'Invalid competition prefix/schema/scope')
 v.require(not set(r['competitions'].values())&{x[1]for x in upstream.values()},'Existing competition namespace collision')
def verify(folder=PHASE/'final'):
 folder=Path(folder);base=v.verify();v.require(base['technical_validation']=='PASS','Accepted standardization failed')
 frozen=v.load(PHASE/'input_freeze.json')
 for rel,h in frozen['inputs'].items():v.require(v.sha(v.read(v.ROOT/rel))==h,'Final input changed '+rel)
 ref=v.load(PHASE/'model_reference.json')
 for path,h in ref['sources'].items():v.require(v.sha(v.read(Path(path)))==h,'Read-only identity reference changed')
 global_ref=v.load(v.PHASE/'reference/global_reference.json');reg=v.load(v.ROOT/'config/uefa_competition_registry.json');validate_local_registry(reg,global_ref['competition_registry'])
 report=v.load(folder/'final_dataset.json');v.require(report['dataset_sha256']==v.sha(v.read(v.PHASE/'validated'/v.NAME))=='7d1a4084094368b2a8b17be84b87124ec65d53b0f4beb4184290ceb6e7d43fde'and report['csv_changed']is False,'Final CSV changed')
 v.require(report['local_match_id_collisions']==report['global_match_id_collisions']==0 and report['global_rows']==182001 and report['prospective_combined_rows']==193423,'Final integration accounting differs')
 v.require(report['local_registration']is True and report['formal_global_registration']is False,'Registry scope overstated')
 proposal=v.load(folder/'registration_proposal.json');v.require(proposal['local_registry']==reg and proposal['add_entries']=={k:['uefa',n]for k,n in reg['competitions'].items()}and proposal['formal_global_registration']is False,'Wrong global integration proposal')
 mappings=v.load(v.PHASE/'team_mapping_decisions.json')['teams'];accepted={r['key']:r for r in mappings};decl={r['key']:r['declarations']for r in v.load(PHASE/'participant_associations.json')['participants']};links=v.load(folder/'club_identity_crosswalk.json')['mapping'];by={r['key']:r for r in links}
 v.require(len(links)==len(by)==4936 and set(by)==set(accepted)==set(decl),'Identity mapping lost/repeated')
 source={r['observation_id']:r for r in v.load(v.PHASE.parent/'phase2/validated/source_inventory.json')['observations']};repairs=v.load(v.P3/'final/observation_repairs.json');source.update({r['observation_id']:r for r in repairs['additional_observations']})
 for repair in repairs['occurrence_repairs']:source[repair['observation']].update(repair['changes'])
 events={e['event_id']:e for e in v.load(v.P3/'final/adjudicated_inventory.json')['events']};names={};scopes={};bylabel=defaultdict(list);byqualified=defaultdict(list)
 for row in ref['mapping']:bylabel[row['original_label']].append(row);byqualified[(row['scope'],row['original_label'])].append(row)
 for k,r in by.items():
  a=accepted[k];ns=set(a['accepted_historical_labels'])|set(a.get('accepted_source_labels',{}))|set(a['existing_registry_candidates'])|{a['standardized_name']};names[k]=ns
  v.require(set(r['historical_aliases'])==ns and r['event_ids']==a['event_ids']and r['phase3_identity']==a['phase3_identity']and r['display_name']==a['standardized_name']and r['identifier_abbreviation']==v.abbreviation(a['standardized_name']),'Identity/display/token distinction broken')
  v.require(r['evidence_declarations']==decl[k],'Association evidence lost')
  for d in decl[k]:
   original=source[d['observation']];v.require(original['associations'][d['side']]==d['value']and original['source_sha256']==d['sha256']and original['locator']==d['locator'],'Association source binding differs')
   v.require(any(any(z['observation']==d['observation']and z['identity_candidates'][d['side']]==a['phase3_identity']for z in events[eid]['source_evidence'])for eid in a['event_ids']),'Association orientation/participant binding differs')
   if d.get('provider_club_id'):v.require(original['publisher']=='11footy'and original['source_fields'].get(('home'if d['side']==0 else'away')+'_team_id')==d['provider_club_id']and not(original.get('reconciled_home_label')or original.get('reconciled_away_label')),'Unsafe provider alias binding')
  sc={country_scope(d['value'])for d in decl[k]};sc={c for c in sc if not c.startswith('unknown:')};scopes[k]=sc;v.require(r['association_contexts']==sorted(sc),'Changed association scope')
  candidates=[]
  if len(sc)==1:
   for n in ns:
    for c in [next(iter(sc)),next(iter(sc))+'|season:'+a['season']]:candidates+=byqualified.get((c,n),[])
  ids=sorted({x['club_id']for x in candidates});v.require(r['candidate_project_ids']==ids and r['existing_registry_rows']==sorted({x['reference_row']for x in candidates}),'Project identity candidate reference differs')
  v.require(r['canonical_club_id']==(ids[0]if len(ids)==1 else None),'Unsupported or accidental club merger')
  v.require(r['status']==('LINKED_EXISTING_PROJECT_IDENTITY'if len(ids)==1 else'RETAIN_SEASONAL_IDENTITY'),'Unresolved identity silently promoted')
 contexts=defaultdict(set)
 for k,ns in names.items():
  for n in ns:contexts[n]|=scopes[k]
 for n,rs in bylabel.items():
  contexts[n].update(r['scope'].split('|')[0]for r in rs if not r['scope'].startswith('uefa-unresolved'))
 cases=v.load(folder/'identity_case_dispositions.json')['cases'];assessment=v.load(v.PHASE/'team_compatibility_final.json');expected={f'UEL5-LOCAL-{code}':ns for code,ns in assessment['nonunique_local_abbreviation_groups'].items()};expected.update({f'UEL5-CROSS-{i:03d}':[n,*ns]for i,(n,ns)in enumerate(sorted(assessment['new_label_abbreviations_also_used_by_other_baseline_labels'].items()),1)})
 v.require(len(cases)==len(expected)==228 and {c['case_id']for c in cases}==set(expected),'Case accounting differs')
 manual={tuple(sorted(r['labels'])):r for r in v.load(PHASE/'identity_research.json')['decisions']}
 global_rows=list(csv.DictReader(io.StringIO(v.read(v.ROOT.parent/'toto/data/final_data/final_data_sum.csv').decode())));rows=list(csv.DictReader(io.StringIO(v.read(v.PHASE/'validated'/v.NAME).decode())));opponents={r['match_id']:frozenset([r['home_team'],r['away_team']])for r in global_rows+rows}
 for c in cases:
  v.require(c['labels']==expected[c['case_id']]and c['match_identifier_changes']==0,'Changed case scope/IDs')
  v.require({tuple(sorted([r['left'],r['right']]))for r in c['pair_decisions']}==set(combinations(sorted(set(c['labels'])),2)),'Pair decision lost')
  for d in c['pair_decisions']:
   a,b=d['left'],d['right'];pair=tuple(sorted([a,b]));method=d['method'];evidence=d['evidence']
   if method=='FULL_LABEL_ORTHOGRAPHY_ONLY':v.require(v.lexical(a)==v.lexical(b)and not(contexts[a]and contexts[b]and contexts[a].isdisjoint(contexts[b]))and evidence==[a,b]and d['status']=='ORTHOGRAPHIC_LABEL_CORRESPONDENCE','False full-label spelling correspondence')
   elif method=='DIRECTED_PRIMARY_IDENTITY_EVIDENCE':v.require(pair in manual and evidence==manual[pair]['evidence']and d['status']==manual[pair]['status'],'Unbound historical alias decision')
   elif method=='COOCCURRING_OPPONENTS':v.require(d['status']=='DISTINCT'and evidence and all(opponents[x]==frozenset(pair)for x in evidence),'Wrong distinct-club opponent proof')
   elif method=='EXISTING_SOURCE_QUALIFIED_PROJECT_IDENTITY':
    aa={r['club_id']for r in bylabel[a]if not r['scope'].startswith('uefa-unresolved')};bb={r['club_id']for r in bylabel[b]if not r['scope'].startswith('uefa-unresolved')};v.require(aa==bb==set(evidence)and len(aa)==1 and not(sensitive(a)or sensitive(b)),'Unsafe global alias proof')
   elif method=='ACCEPTED_COOEVAL_PARTICIPANT_ALIAS':v.require(evidence and all({a,b}<=names[k]for k in evidence)and not(sensitive(a)or sensitive(b))and d['status']=='ALIAS_IN_DOCUMENTED_SEASONS','Unsupported coeval alias')
   elif method=='ASSOCIATION_QUALIFIED_PROVIDER_CLUB_ID':
    v.require(evidence and not(sensitive(a)or sensitive(b))and d['status']=='ALIAS_IN_PROVIDER_CATALOGUE','Unsafe catalogue merge')
    for proof in evidence:
     ks=proof['participant_keys'];v.require({a,b}<=set().union(*(names[k]for k in ks)),'Missing catalogue alias labels')
     v.require(all(any(x.get('provider_club_id')==proof['provider_club_id']and country_scope(x['value'])==proof['association']and not x.get('refounded_on')for x in decl[k])for k in ks),'Broken catalogue continuity proof')
   elif method=='DISJOINT_DOCUMENTED_ASSOCIATION_CONTEXTS':v.require(contexts[a]and contexts[b]and contexts[a].isdisjoint(contexts[b])and evidence==[sorted(contexts[a]),sorted(contexts[b])],'False distinct association claim')
   else:v.require(method=='PRESERVE_DISTINCT_SEASONAL_IDENTITIES'and d['status']=='UNRESOLVED'and not evidence,'Unsupported case resolution')
  v.require(c['status']==('RESOLVED'if all(r['status']!='UNRESOLVED'for r in c['pair_decisions'])else'UNRESOLVED_OR_PARTIAL'),'Reviewed case miscounted as resolved')
 v.require(report['identity_case_results']==dict(Counter(c['status']for c in cases))and report['seasonal_identity_results']==dict(Counter(r['status']for r in links)),'Final identity counters differ')
 prepared=list(csv.DictReader(io.StringIO(v.read(Path(ref['prepared_records'])).decode())));v.require(len(prepared)==182001 and {r['original_match_id']for r in prepared}==set(global_ref['existing_ids']),'Current project reference inventory differs')
 semantic={(r['recorded_date'],*sorted([r['home_club_id'],r['away_club_id']]))for r in prepared};exact={(r['date'],*sorted([v.lexical(r['home_team']),v.lexical(r['away_team'])]))for r in global_rows};qualified=0
 for r in v.load(v.PHASE/'validated/source_to_output.json')['matches']:
  a,b=[by[k]['canonical_club_id']for k in r['team_mapping_keys']]
  if a and b:qualified+=1;v.require((r['standardized_date'],*sorted([a,b]))not in semantic,'Cross-competition semantic fixture overlap')
 for r in rows:v.require((r['date'],*sorted([v.lexical(r['home_team']),v.lexical(r['away_team'])]))not in exact,'Literal semantic overlap')
 v.require(report['globally_linked_matches']==qualified and not report['identified_semantic_overlap']and report['semantic_uniqueness_fully_certified']is False,'Semantic coverage overstated')
 guarantees=base['guarantees']
 guarantees[11]['explanation']='Format and collision checks pass and owner-accepted prefix is registered locally; formal original-worktree registration remains pending'
 guarantees[12]['explanation']='All228previous ambiguity cases investigated; supported project IDs reused, but unresolved aliases and sensitive continuity remain season-isolated'
 return dict(status='CONDITIONAL PASS',technical_validation='PASS',rows_checked=11422,seasonal_identities_checked=4936,identity_cases_checked=228,identity_case_results=report['identity_case_results'],seasonal_identity_results=report['seasonal_identity_results'],qualified_semantic_match_checks=qualified,global_rows=182001,prospective_rows=193423,local_registration='PASS',formal_global_registration='NOT VERIFIABLE',complete_global_identity_compatibility='NOT VERIFIABLE',match_id_collisions=0,csv_unchanged=True,guarantees=guarantees,guarantee_counts=base['guarantee_counts'],method='Inherited independent exhaustive accepted-row audit plus separately reconstructed identity candidates, original association bindings, registry IDs and every pair proof; only declarative country policy shared',limits=['Documented provider/coeval alias correspondence is not legal succession certification','Complete semantic uniqueness cannot be certified for unresolved aliases','No global registry or prior model identity mapping was modified'])
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--inventory',type=Path,default=PHASE/'final');p.add_argument('--output',type=Path,default=PHASE/'independent_validation.json');a=p.parse_args();out=a.output.resolve();v.require(out.is_relative_to(PHASE.resolve())or out.is_relative_to(Path('/private/tmp')),'Private output required');result=verify(a.inventory)
 with out.open('xb')as f:f.write(v.wire(result))
 print(json.dumps(result,indent=2))
