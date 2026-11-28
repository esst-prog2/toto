"""Repeat accepted corruption checks and attack the new final identity ledger."""
import json
from pathlib import Path
from scripts import check_uefa_europa_league_corruption as old
from scripts import verify_uefa_europa_league_final as final

def run():
 result=old.run();checks=result['results'];v=final.v;original=v.read;cache={}
 def baseline(path):
  name=str(Path(path))
  if name not in cache:cache[name]=original(path)
  return cache[name]
 def mutate(name,path,change):
  obj=json.loads(baseline(path));change(obj);changed=v.wire(obj);v.read=lambda p:changed if Path(p)==path else baseline(p)
  try:final.verify()
  except(ValueError,KeyError,IndexError)as error:checks.append(dict(test=name,status='DETECTED',reason=str(error)))
  else:raise AssertionError('Undetected final corruption: '+name)
  finally:v.read=baseline
 p=final.PHASE
 try:
  mutate('invalid competition prefix',v.ROOT/'config/uefa_competition_registry.json',lambda x:x['competitions'].__setitem__('UEFA Cup','invalid'))
  mutate('unregistered local competition code',v.ROOT/'config/uefa_competition_registry.json',lambda x:x.__setitem__('registration','PROPOSED'))
  mutate('false formal global registration',p/'final/final_dataset.json',lambda x:x.__setitem__('formal_global_registration',True))
  mutate('incorrect canonical club mapping',p/'final/club_identity_crosswalk.json',lambda x:x['mapping'][0].__setitem__('canonical_club_id','club-synthetic-wrong'))
  def merge(x):
   unresolved=next(r for r in x['mapping']if r['canonical_club_id']is None);unresolved['canonical_club_id']=next(r['canonical_club_id']for r in x['mapping']if r['canonical_club_id'])
  mutate('accidental unresolved-club merger',p/'final/club_identity_crosswalk.json',merge)
  mutate('incorrect historical alias',p/'final/club_identity_crosswalk.json',lambda x:x['mapping'][0]['historical_aliases'].append('Synthetic unrelated club'))
  mutate('lost original identity case',p/'final/identity_case_dispositions.json',lambda x:x['cases'].pop())
  mutate('unresolved identity falsely closed',p/'final/identity_case_dispositions.json',lambda x:next(c for c in x['cases']if c['status']!='RESOLVED').__setitem__('status','RESOLVED'))
  mutate('unreported global identifier collision',p/'final/final_dataset.json',lambda x:x.__setitem__('global_match_id_collisions',1))
  mutate('semantic coverage overstated',p/'final/final_dataset.json',lambda x:x.__setitem__('semantic_uniqueness_fully_certified',True))
  mutate('lost historical competition registration',p/'final/registration_proposal.json',lambda x:x['add_entries'].pop('UEFA Cup'))
 finally:v.read=original
 return dict(status='PASS',scenarios=len(checks),inherited_scenarios=22,new_final_scenarios=11,original_files_mutated=False,results=checks)
if __name__=='__main__':
 result=run()
 with(final.PHASE/'adverse_validation.json').open('xb')as f:f.write(final.v.wire(result))
 print('PASS',result['scenarios'],'adverse corruptions detected')
