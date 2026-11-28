"""Synthetic finalization policy/identity regressions; no private artifacts."""
from copy import deepcopy
from collections import defaultdict
import pytest
from scripts import finalize_uefa_europa_league as f
from scripts import verify_uefa_europa_league_final as v

@pytest.mark.parametrize('raw,expected',[('Italy','italy'),('ITA','italy'),('ita','italy'),('Scotland','assoc-SCO'),('Northern Ireland','assoc-NIR'),('Czechia','assoc-CZE'),('Germany','germany'),('USSR','assoc-URS')])
def test_scope_matches_available_registry_namespace(raw,expected):assert f.scope(raw)==v.country_scope(raw)==expected

def registry():return dict(registration='LOCAL_REGISTERED',formal_global_registration=False,competitions={'UEFA Cup':'uefael','UEFA Europa League':'uefael'},identifier_length=24,country='uefa',scopes=['MAIN','QUALIFYING'])
def test_local_registry_valid_and_formal_status_distinct():v.validate_local_registry(registry(),{'Other':['uefa','uefabl']})
@pytest.mark.parametrize('change',[{'registration':'PROPOSED'},{'formal_global_registration':True},{'identifier_length':20},{'country':'england'},{'scopes':['MAIN']},{'competitions':{'UEFA Cup':'other'}}])
def test_invalid_registry_rejected(change):
 r=registry();r.update(change)
 with pytest.raises(ValueError):v.validate_local_registry(r,{})
def test_registered_code_collision_rejected():
 with pytest.raises(ValueError):v.validate_local_registry(registry(),{'Other':['uefa','uefael']})
def pair(**kw):
 args=dict(a='Alpha',b='Alpine',contexts={},registry={},positive={},opponents={});args.update(kw);return f.evaluate_pair(**args)
def test_abbreviation_does_not_establish_identity():assert pair()['status']=='UNRESOLVED'
def test_opponent_proof_establishes_distinct_clubs():assert pair(opponents={('Alpha','Alpine'):['synthetic-match']})['status']=='DISTINCT'
def test_source_qualified_existing_registry_alias():
 r={'scope':'england','club_id':'club-existing'}
 assert pair(registry={'Alpha':[r],'Alpine':[r]})['status']=='ALIAS'
def test_two_provisional_ids_not_silently_merged():
 assert pair(registry={'Alpha':[{'scope':'england','club_id':'one'}],'Alpine':[{'scope':'england','club_id':'two'}]})['status']=='UNRESOLVED'
def test_positive_participant_alias_is_scoped():
 assert pair(positive={('Alpha','Alpine'):['seasonal-key']})['status']=='ALIAS_IN_DOCUMENTED_SEASONS'
def test_different_associations_preserved():assert pair(contexts={'Alpha':{'england'},'Alpine':{'france'}})['status']=='DISTINCT_CONTEXTS'
def test_full_label_spelling_correspondence_does_not_allocate_canonical_id():
 r=pair(a='Álpha',b='Alpha');assert r['status']=='ORTHOGRAPHIC_LABEL_CORRESPONDENCE'and'canonical_club_id'not in r
@pytest.mark.parametrize('label',['Steaua Example','Rangers FC','Szeged'])
def test_sensitive_aliases_remain_separate(label):
 a,b=sorted([label,'Other Name']);r=pair(a=a,b=b,positive={(a,b):['synthetic-key']});assert r['status']=='UNRESOLVED'
def test_catalogue_evidence_not_legal_succession():
 r=pair(catalogue={('Alpha','Alpine'):[{'provider_club_id':'7'}]});assert r['status']=='ALIAS_IN_PROVIDER_CATALOGUE'and'legal'in r['qualification']
def test_explicit_primary_identity_decision():
 r=pair(manual={('Alpha','Alpine'):dict(status='DISTINCT',evidence=['primary'],qualification='historical context')});assert r['method']=='DIRECTED_PRIMARY_IDENTITY_EVIDENCE'
