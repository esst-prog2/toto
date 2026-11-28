"""Reproducible private UEFA Cup/EL historical decisions; never production output.

Frozen Phase 2 observations remain authoritative originals. Decisions are additive,
source-bound and separately eligible for outcomes, goals, chronology and venues.
"""
import argparse
from collections import Counter,defaultdict
import copy
import csv
import io
import json
from pathlib import Path
import re
from scripts.inventory_uefa_europa_league import BASE,OUTPUT as P2,ROOT,read_bytes,sha,encode,Union,reconcile,namespace,tie_gaps
from scripts.review_uefa_champions_league_history import goals

PHASE=BASE/'phase3'
OUTPUT=PHASE/'final'

def load(p):return json.loads(read_bytes(p))
def outcome(score):return '1' if score[0]>score[1] else '2' if score[0]<score[1] else 'X'
def orient(value,row,ids):return value if value is None or row['identity_candidates']==ids else value[::-1]
def minute(s):
 m=re.fullmatch(r"\s*(\d{1,3})(?:\+\d+)?[’']?\s*",str(s))
 return int(m[1]) if m else None

def chronology(r,cutoff=90):
 """Only complete goal sequences, verified against printed cumulative total."""
 f=r['source_fields'];p=r['periods'];total=p['after_extra_time'] or p['published_final']
 if total is None:return None
 fields=f.get('fields',{})
 if 'goals1'in fields or 'goals2'in fields:
  t=[goals(fields.get('goals'+str(i),''))[0] for i in (1,2)]
  if [len(v)for v in t]==total and all(minute(x)is not None for a in t for x in a):return [sum(minute(x)<=cutoff for x in a)for a in t]
 entries=f.get('goal_rows')
 if entries:
  previous=[0,0];reg=[0,0];lasttime=-1
  for x in entries:
   score=[int(x['GH']),int(x['GA'])];tm=minute(x['time'])
   delta=[a-b for a,b in zip(score,previous)]
   if tm is None or not 0<=tm<=120 or tm<lasttime or delta not in ([1,0],[0,1]):return None
   if tm<=cutoff:reg=score
   previous=score;lasttime=tm
  if previous==total:return reg
 return None

def identity_map(rows,identities,decisions):
 u=Union();roots={x['identity_candidate']:tuple(x['identity_root']) for x in identities['labels']}
 for root in roots.values():u.root(root)
 for d in decisions:
  if d['decision']in ('SEASON_BOUND_NAME_CORRESPONDENCE','SOURCE_LABEL_CORRESPONDENCE_ONLY'):u.join(tuple(d['left']),tuple(d['right']))
 old_events=load(P2/'event_inventory.json')['events'];by_obs={o:e for e in old_events for o in e['observations']};rr_by_id={r['observation_id']:copy.deepcopy(r) for r in rows}
 # "Inter" is disambiguated per source occurrence using association, never a global alias.
 for r in rows:
  new=[]
  for i,(side,old) in enumerate(zip(('home','away'),r['identity_candidates'])):
   root=u.root(roots[old]);country=str(r['associations'][i] or '').casefold()
   if root[1]=='inter' or r.get('reconciled_'+side+'_label',r['raw_'+side]).lower()=='inter' or re.fullmatch(r'internazionale(?: fc)?|inter milan',__import__('scripts.uefa_europa_league_sources',fromlist=['team_key']).team_key(r.get('reconciled_'+side+'_label',r['raw_'+side]))):
    if not country or country=='none':
     if re.search('internazionale|inter milan',r[side],re.I):country='italy'
     else:
      matched={str(q['associations'][j]).lower() for oid in by_obs[r['observation_id']]['observations'] for q in [rr_by_id[oid]] for j,cid in enumerate(q['identity_candidates']) if cid in roots and roots[cid]==roots[old] and q['associations'][j]}
      matched={dict(ita='italy',aze='azerbaijan',fin='finland').get(x,x)for x in matched}
      if len(matched)==1:country=next(iter(matched))
    candidates={'italy':'internazionale','ita':'internazionale','finland':'inter turku','fin':'inter turku','azerbaijan':'inter baki','aze':'inter baki'}
    if country in candidates:
     names=[z for z in roots.values() if z[0]==r['season'] and z[1]in (candidates[country], 'samax' if country in ('aze','azerbaijan') else candidates[country])]
     root=(r['season'],'internazionale') if country in ('ita','italy') else u.root(sorted(names)[0]) if names else (r['season'],candidates[country])
   if roots[old][1]=='inter':r[side]=r[side]+' [occurrence:'+str(country or 'unknown')+']'
   key=__import__('scripts.uefa_europa_league_sources',fromlist=['team_key']).team_key(r.get('reconciled_'+side+'_label',r['raw_'+side]))
   if key in ('inter baki','inter baku','kesla','keshla','samax') or (key=='inter'and country in ('aze','azerbaijan')):root=(r['season'],'inter baku')
   new.append(sha(encode(root)))
  r['identity_candidates']=new
 return {namespace(r,side):r['identity_candidates'][i] for r in rows for i,side in enumerate(('home','away'))}

def score_decision(rr,ids,all_events):
 evidence=[];candidates=[]
 for r in rr:
  v=chronology(r)
  if v is not None:candidates.append((orient(v,r,ids),'COMPLETE_EXPLICIT_GOAL_CHRONOLOGY',r['observation_id']))
 # Explicit period annotations, rather than provider's sparse no-ET default.
 for r in rr:
  p=r['periods'];f=r['source_fields'];v=p['regulation_time']
  if v is not None and (r['publisher']=='openfootball' or '/openfootball/'in r['source'] or (f.get('home_goals_regular_time','')!='' and r['publisher']=='11footy')):
   candidates.append((orient(v,r,ids),'EXPLICIT_REGULATION_COMPONENT',r['observation_id']))
 extra=any(r['periods']['after_extra_time'] is not None or r['periods']['shootout'] is not None or r['source_fields'].get('full_time') in ('E','P') for r in rr)
 if not candidates and extra:
  # Under the old away-goals rule, second-leg numeric home/away goals
  # equal first-leg numeric home/away goals while participant identities reverse.
  # Finals without away goals instead need a uniquely bounded score.
  if int(rr[0]['season'][:4])<=2020:
   firsts=[]
   for e in all_events:
    if e['season']!=rr[0]['season'] or set(e['identity_candidates'])!=set(ids) or set(e['observations'])&{r['observation_id']for r in rr}:continue
    earlier=[r for r in e['_rows'] if r['identity_candidates']==ids[::-1] and r['periods']['published_final'] is not None and (r['source_leg']==1 or (r['date'] and any(z['date'] and z['date']>r['date'] for z in rr)))]
    for r in earlier:
     if r['periods']['after_extra_time']is None and r['periods']['shootout']is None:firsts.append((r['periods']['published_final'],r['observation_id']))
   values={tuple(v)for v,o in firsts}
   if len(values)==1:
    v=list(next(iter(values)))
    finals=[orient(r['periods']['after_extra_time'] or r['periods']['published_final'],r,ids)for r in rr if r['periods']['after_extra_time'] is not None or (r['periods']['shootout']is not None and r['publisher']in ('RSSSF contributors','Wikipedia contributors') and r['periods']['published_final']is not None)]
    if finals and all(all(a<=b for a,b in zip(v,f))for f in finals):
     if any(r['stage']=='FINAL'for r in rr):
      limit=[min(f[i]for f in finals)for i in(0,1)];possible=[[hg,ag]for hg in range(limit[0]+1)for ag in range(limit[1]+1)if hg-ag==v[0]-v[1]]
      if len(possible)==1:candidates.append((possible[0],'UNIQUE_SECOND_LEG_FINAL_AGGREGATE_AND_CUMULATIVE_BOUND',sorted(firsts,key=lambda x:x[1])[0][1]))
     else:candidates.append((v,'PRE_2021_AWAY_GOALS_ET_EQUALITY_WITH_IDENTIFIED_FIRST_LEG',sorted(firsts,key=lambda x:x[1])[0][1]))
 if not candidates and extra:
  single=any(r['stage']=='FINAL'and int(r['season'][:4])>=1997 for r in rr)or(int(rr[0]['season'][:4])==2020 and any(r['scope']=='QUALIFYING'for r in rr))
  bounds=[(orient(r['periods']['after_extra_time']or r['periods']['published_final'],r,ids),r['observation_id'])for r in rr if r['periods']['after_extra_time']is not None or(r['periods']['shootout']is not None and r['publisher']in ('RSSSF contributors','Wikipedia contributors')and r['periods']['published_final']is not None)]
  if single and bounds and any(min(v)==0 for v,o in bounds):
   candidates.append(([0,0],'UNIQUE_NONNEGATIVE_SINGLE_MATCH_EXTRA_TIME_BOUND',next(o for v,o in bounds if min(v)==0)))
 if not candidates and not extra:
  # Grid score is a match result, unlike its adjacent aggregate; ordinary match
  # interpretation additionally requires the absence of ET/penalty/status evidence.
  for r in rr:
   if r['publisher']in ('RSSSF contributors','Wikipedia contributors') and r['periods']['published_final']is not None and not any(k in r['status'].lower()for k in ('award','abandon','cancel','void','walkover','w/o')):
    candidates.append((orient(r['periods']['published_final'],r,ids),'TARGET_ARCHIVE_EXPLICIT_ORDINARY_MATCH_SCORE',r['observation_id']))
 if not candidates and not extra:
  for r in rr:
   if r['periods']['regulation_time']is not None:candidates.append((orient(r['periods']['regulation_time'],r,ids),'SOURCE_REPORTED_ORDINARY_DURATION',r['observation_id']))
 if candidates:
  values={tuple(v)for v,m,o in candidates};evidence=[dict(value=v,method=m,observation=o)for v,m,o in candidates]
  if len(values)==1:
   score=list(next(iter(values)));return dict(regulation_time=score,regulation_outcome=outcome(score),confidence='SUPPORTED',method=candidates[0][1],evidence=evidence,remaining_uncertainty=None)
  return dict(regulation_time=None,regulation_outcome=None,confidence='UNRESOLVED',method='CONFLICTING_ATTRIBUTE_SPECIFIC_EVIDENCE',evidence=evidence,remaining_uncertainty='Competing supported regulation values require directed investigation')
 # For an ET return, first-leg standing goal difference can establish the
 # 90-minute outcome even after away-goals abolition, without exact goals.
 if extra:
  first_proofs=[]
  for first_event in all_events:
   if first_event['season']!=rr[0]['season']or set(first_event['identity_candidates'])!=set(ids)or set(first_event['observations'])&{r['observation_id']for r in rr}:continue
   for r in first_event['_rows']:
    if r['identity_candidates']!=ids[::-1]or r['periods']['published_final']is None or r['periods']['after_extra_time']is not None:continue
    if r['source_leg']==1 or(r['date']and any(z['date']and z['date']>r['date']for z in rr)):first_proofs.append((r['periods']['published_final'][0]-r['periods']['published_final'][1],r['observation_id']))
  margins={m for m,o in first_proofs}
  if len(margins)==1:
   m=next(iter(margins));return dict(regulation_time=None,regulation_outcome='1'if m>0 else'2'if m<0 else'X',confidence='OUTCOME_ONLY',method='SECOND_LEG_AGGREGATE_EQUALITY_OUTCOME_ONLY',evidence=[dict(first_leg_observation=o,required_goal_difference=m)for m,o in first_proofs],remaining_uncertainty='Exact90minute goals unavailable; result class follows identified first-leg standing margin')
 single=any(r['stage']=='FINAL'and int(r['season'][:4])>=1997 for r in rr)or(int(rr[0]['season'][:4])==2020 and any(r['scope']=='QUALIFYING'for r in rr))
 draw=extra and single
 return dict(regulation_time=None,regulation_outcome='X' if draw else None,confidence='OUTCOME_ONLY' if draw else 'UNRESOLVED',method='SINGLE_MATCH_REACHED_EXTRA_TIME_OUTCOME_ONLY' if draw else 'PERIOD_NOT_RECOVERED',evidence=[],remaining_uncertainty='Exact regulation goals unavailable' if draw else 'No uniquely supported regulation score; published ET/shootout totals quarantined')

def date_decision(rr):
 dates=[]
 for r in rr:
  if not r['date']:continue
  f=r['source_fields'];method='SOURCE_REPORTED_DAY';rank=4
  if r['publisher']=='RSSSF contributors' and 'date_source_line'in f:rank=0;method='DATED_DETAILED_MATCH_REPORT'
  elif r['publisher']=='Wikipedia contributors' and 'fields'in f:rank=1;method='DATED_INDIVIDUAL_MATCH_BOX'
  elif r['representation']=='goal_event_fixture_context':rank=2;method='DATED_GOAL_LOG'
  elif r['publisher']=='11footy' and r['status']=='played':rank=3;method='PROVIDER_PLAYED_LOCAL_DAY'
  dates.append((rank,r['date'],method,r['observation_id']))
 intervals=[dict(observation=r['observation_id'],interval=r['date_interval'])for r in rr if r['date_interval']]
 if dates:
  if rr[0]['season']=='2013/2014':
   leg2_days={r['date_interval'][0]for r in rr if r['source_leg']==2 and r['date_interval']and r['date_interval'][0]==r['date_interval'][1]}
   corroborated=[x for x in dates if x[1]in leg2_days and x[2]!='PROVIDER_PLAYED_LOCAL_DAY']
   if len({x[1]for x in corroborated})==1:
    dates=[(-1,d,m+';RETURN_LEG_SCHEDULE_CORROBORATION',o)if (rank,d,m,o)in corroborated else(rank,d,m,o)for rank,d,m,o in dates]
  best=min(x[0]for x in dates);selected=[x for x in dates if x[0]==best];values={x[1]for x in selected}
  if len(values)==1:return dict(date=next(iter(values)),confidence='SOURCE_SUPPORTED',method=selected[0][2],evidence=[x[3]for x in selected],original_dates=sorted({x[1]for x in dates}|{r['_source_date']for r in rr if r.get('_source_date')}),original_intervals=intervals,remaining_uncertainty='Competing source dates retained; source-specific report role selected' if len({x[1]for x in dates})>1 else None)
 return dict(date=None,confidence='UNRESOLVED',method='NO_UNIQUE_FIXTURE_SPECIFIC_DAY',evidence=[],original_dates=sorted({x[1]for x in dates}|{r['_source_date']for r in rr if r.get('_source_date')}),original_intervals=intervals,remaining_uncertainty='Schedule interval does not establish actual playing day')

def venue_decision(rr,stage,season):
 year=int(season[:4]);evidence=[r['observation_id']for r in rr if r['stage']==stage]
 if stage=='FINAL':return dict(neutral_venue=1 if year>=1997 else 0,method='OFFICIAL_SINGLE_FINAL_FORMAT' if year>=1997 else 'TWO_LEG_HOME_AWAY_FINAL',evidence=evidence,physical_venue_claims=[dict(observation=r['observation_id'],venue=r['venue'],provider_neutral=r['source_neutral_venue'])for r in rr if r['venue'] or r['source_neutral_venue']is not None])
 centralized=year==2019 and (stage in ('QUARTERFINAL','SEMIFINAL') or (stage=='ROUND_OF_16' and any(re.search('over one leg|single.leg|one.off',str(r['source_fields']),re.I)for r in rr)))
 return dict(neutral_venue=1 if centralized else None if stage=='UNKNOWN' else 0,method='DOCUMENTED_GERMANY_CENTRALIZED_TOURNAMENT' if centralized else 'FORMAT_UNESTABLISHED' if stage=='UNKNOWN' else 'CONVENTIONAL_HOSTED_HOME_AWAY_FORMAT',evidence=evidence,physical_venue_claims=[dict(observation=r['observation_id'],venue=r['venue'],provider_neutral=r['source_neutral_venue'])for r in rr if r['venue'] or r['source_neutral_venue']is not None])

def duration_decision(rows,status,period_evidence):
 not_applicable=status in ('NOT PLAYED','ADMINISTRATIVE_ONLY','OUT OF SCOPE')
 extra=any(r['periods']['after_extra_time']is not None or r['periods']['shootout']is not None or r['source_fields'].get('full_time')in('E','P')for r in rows)
 complete=status in ('PLAYED_SOURCE_SUPPORTED','PLAYED_ADMINISTRATIVE_EXCEPTION')
 def unique(period):
  values=period_evidence[period]
  return values[0]['value']if len(values)==1 else None
 return dict(extra_time_played=None if not_applicable else extra,regulation_completed=None if not_applicable else complete,extra_time_completed=None if not_applicable or not extra else complete,after_extra_time_score=unique('after_extra_time')if extra and complete else None,extra_time_only=unique('extra_time_only'),shootout_score=unique('shootout'),confidence='NOT_APPLICABLE'if not_applicable else'SOURCE_SUPPORTED_PERIOD_METADATA',method='Typed explicit period observations; sparse ordinary-duration flags do not overrule documented extra time',evidence=[r['observation_id']for r in rows if r['periods']['after_extra_time']is not None or r['periods']['shootout']is not None])


def model_eligibility(status,score,day,venue,*,identity_supported=True,regulation_completed=True):
 complete=status in ('PLAYED_SOURCE_SUPPORTED','PLAYED_ADMINISTRATIVE_EXCEPTION')and identity_supported and regulation_completed
 return dict(outcome=complete and score['regulation_outcome']is not None,goals=complete and score['regulation_time']is not None,chronological=complete and score['regulation_outcome']is not None and day['date']is not None,venue_dependent=complete and score['regulation_outcome']is not None and venue['neutral_venue']==0,historical_descriptive=True)


def apply_occurrence_repairs(rows):
 repairs=[]
 for rule in load(PHASE/'observation_decisions.json')['decisions']:
  r=next(r for r in rows if r['observation_id']==rule['observation']);assert r['source_sha256']==rule['source_sha256']
  before={k:copy.deepcopy(r.get(k))for k in rule['changes']}
  for k,v in rule['changes'].items():r[k]=copy.deepcopy(v)
  repairs.append(dict(**rule,before=before))
 return repairs

def repair_grid_observations(rows):
 """Separate third-column aggregate footnotes from fourth-column shootouts."""
 repairs=[];added=[];seen=set()
 for r in rows:
  if r['publisher']!='RSSSF contributors' or 'raw_line'not in r['source_fields']:continue
  line=r['source_fields']['raw_line']
  if re.search(r'\bawd\b',line):continue
  tokens=re.findall(r'(?<!\d)\*?\d+-\d+[a-z*]?',line)
  if len(tokens)!=3 or not tokens[2].endswith('p'):continue
  # A genuine shootout after two played legs occupies a fourth numeric column.
  if r['source_fields'].get('status_annotation','').startswith('p ') or '  'in line:
   values=[list(map(int,re.search(r'(\d+)-(\d+)',t).groups()))for t in tokens]
   if values[2]!=[values[0][i]+values[1][i]for i in(0,1)]:raise ValueError('Aggregate-p needs individual review')
   before=copy.deepcopy(r['periods']);leg=r['source_leg']or 1
   r['periods']['shootout']=None;r['periods']['published_final']=values[leg-1]if leg==1 else values[leg-1][::-1];r['periods']['aggregate']=values[2]if leg==1 else values[2][::-1];r['source_leg']=leg
   if 'aet'not in line.lower():r['periods']['after_extra_time']=None
   repairs.append(dict(observation=r['observation_id'],source_sha256=r['source_sha256'],locator=r['locator'],method='THREE_SCORE_COLUMNS_THIRD_IS_AGGREGATE_P_FOOTNOTE_NOT_FOURTH_SHOOTOUT',before=before,after=copy.deepcopy(r['periods'])))
   key=(r['source'],line)
   if ':leg:1'in r['locator']and key not in seen:
    # The accepted parser emitted only leg 1 when aggregate-p was removed.
    if not any(q['source']==r['source']and q['source_fields'].get('raw_line')==line and q['source_leg']==2 for q in rows):
     q=copy.deepcopy(r);q['locator']=r['locator'].replace(':leg:1',':leg:2')+':phase3-recovered';q['observation_id']=sha(encode([q['source_sha256'],q['locator']]));q['home'],q['away']=r['away'],r['home'];q['raw_home'],q['raw_away']=r['raw_away'],r['raw_home'];q['identity_candidates']=r['identity_candidates'][::-1];q['associations']=r['associations'][::-1];q['team_candidates']=r['team_candidates'][::-1];q['source_leg']=2;q['periods']['published_final']=values[1][::-1];q['periods']['aggregate']=values[2][::-1];q['date_interval']=None;q['date']=None;q['date_role']='UNAVAILABLE_RECOVERED_RETURN_LEG';q['derived_from_observation']=r['observation_id'];added.append(q)
    seen.add(key)
 return rows+added,repairs,added

def reconcile_directed(rows,mapping):
 # Nonfinal opposite orientations can be distinct legs even if a provider copied
 # the same scheduled date into both records. Never collapse them on date alone.
 groups=defaultdict(list)
 final_pairs={(r['season'],tuple(sorted(mapping[namespace(r,side)]for side in ('home','away')))) for r in rows if (r['stage']=='FINAL'and int(r['season'][:4])>=1997)or re.search(r'played in 1 leg|over (?:one|1) leg',str(r['source_fields'].get('status_annotation','')),re.I)}
 for r in rows:
  ids=[mapping[namespace(r,side)]for side in ('home','away')]
  final=(r['season'],tuple(sorted(ids)))in final_pairs
  groups[(r['season'],tuple(sorted(ids))if final else tuple(ids))].append(r)
 ev=[];links=[];duplicates=[]
 for group in groups.values():
  known={r['stage']for r in group if r['stage']not in ('UNKNOWN','QUALIFYING_ROUND_UNKNOWN')}
  source_days=defaultdict(set)
  for r in group:
   if r['date']:source_days[r['source']].add(r['date'])
  work=copy.deepcopy(group)
  if len(known)<=1 and (all(len(ds)<=1 for ds in source_days.values())or any(re.search(r'played in 1 leg|over (?:one|1) leg',str(r['source_fields'].get('status_annotation','')),re.I)for r in group)) and len({r['replay']for r in group})==1 and source_days:
   # Unique directed stage/leg across source files. A grossly wrong provider
   # date must not invent a rematch; originals remain in the date decision.
   anchor=min(d for ds in source_days.values()for d in ds)
   for r in work:r['date']=anchor
  e,l,d=reconcile(work,mapping);ev+=e;links+=l;duplicates+=d
 return sorted(ev,key=lambda e:(e['season'],e['event_id'])),links,duplicates

def expand_aliases(rows,identities):
 from scripts.uefa_europa_league_sources import team_key
 lexical=Union();byfamily=defaultdict(list);evidence=defaultdict(list);generic={'inter','rapid','aris','ael','dinamo','dynamo','olimpia','olimpija','slavia','aek'}
 for label in identities['labels']:
  key=label['lexical_key'];lexical.root((key,));byfamily[label['identity_candidate']].append(label)
 for labels in byfamily.values():
  keys=sorted({x['lexical_key']for x in labels}-generic)
  for k in keys[1:]:lexical.join((keys[0],),(k,))
 grouping=defaultdict(list)
 for r in rows:
  for side,i in [('home',0),('away',1)]:
   key=team_key(r.get('reconciled_'+side+'_label',r['raw_'+side]));family=lexical.root((key,));grouping[(r['season'],family)].append((r,i))
 unions=Union();proofs=[]
 for r in rows:
  for cid in r['identity_candidates']:unions.root((cid,))
 for (season,family),entries in sorted(grouping.items()):
  ids=sorted({r['identity_candidates'][i]for r,i in entries});provider={r['source_fields'][('home'if i==0 else 'away')+'_team_id']for r,i in entries if r['publisher']=='11footy'}
  if len(ids)<2 or len(provider)>1 or family[0]in generic:continue
  for cid in ids[1:]:unions.join((ids[0],),(cid,))
  proofs.append(dict(season=season,identities=ids,method='PREVIOUSLY_DOCUMENTED_LEXICAL_CORRESPONDENCE_REUSED_IN_SAME_SEASON_NO_PROVIDER_ID_COLLISION',labels=sorted({r.get('reconciled_'+('home'if i==0 else 'away')+'_label',r['raw_home'if i==0 else 'raw_away'])for r,i in entries}),evidence=sorted({r['observation_id']for r,i in entries}),prior_lexical_family=list(family)))
 # Conservative additional name expansions need a known opponent and matching
 # oriented match score; the name itself must share a distinctive contained core.
 generic_words={'club','united','city','real','athletic','dinamo','dynamo','sporting','sport','inter','cska','rapid','sc','fc','royal','sportklub','aek','slavia'}
 for iteration in range(4):
  buckets=defaultdict(list)
  for r in rows:
   for i in (0,1):buckets[(r['season'],unions.root((r['identity_candidates'][1-i],)))].append((r,i))
  proposals=defaultdict(list)
  for bucket,entries in buckets.items():
   for n,(a,i)in enumerate(entries):
    for b,j in entries[n+1:]:
     if a['source']==b['source']or i!=j:continue
     x=unions.root((a['identity_candidates'][i],));z=unions.root((b['identity_candidates'][j],))
     if x==z:continue
     ak=set(team_key(a.get('reconciled_'+('home'if i==0 else 'away')+'_label',a['raw_home'if i==0 else 'raw_away'])).split());bk=set(team_key(b.get('reconciled_'+('home'if j==0 else 'away')+'_label',b['raw_home'if j==0 else 'raw_away'])).split())
     if not((ak&bk)-generic_words)or not(ak<=bk or bk<=ak):continue
     if a['stage']!=b['stage']and 'UNKNOWN'not in (a['stage'],b['stage']):continue
     if a['periods']['published_final']is None or a['periods']['published_final']!=b['periods']['published_final']:continue
     if a['date']and b['date']and abs((__import__('datetime').date.fromisoformat(a['date'])-__import__('datetime').date.fromisoformat(b['date'])).days)>7:continue
     proposals[tuple(sorted((x,z)))].append((a,b,i))
  count=0
  for (x,z),ev in sorted(proposals.items()):
   entries=[(r,i)for r in rows for i in(0,1)if unions.root((r['identity_candidates'][i],))in(x,z)]
   provider={r['source_fields'][('home'if i==0 else 'away')+'_team_id']for r,i in entries if r['publisher']=='11footy'}
   if len(provider)>1:continue
   unions.join(x,z);count+=1
   proofs.append(dict(season=ev[0][0]['season'],identities=[x[0],z[0]],method='DISTINCTIVE_CORE_PLUS_KNOWN_OPPONENT_ORIENTATION_MATCH_SCORE_AND_COMPATIBLE_CHRONOLOGY',labels=sorted({r.get('reconciled_'+('home'if i==0 else 'away')+'_label',r['raw_home'if i==0 else 'raw_away'])for r,i in entries}),evidence=sorted({r['observation_id']for a,b,i in ev for r in(a,b)})))
  if not count:break
 for r in rows:r['identity_candidates']=[unions.root((cid,))[0]for cid in r['identity_candidates']]
 return {namespace(r,side):r['identity_candidates'][i]for r in rows for i,side in enumerate(('home','away'))},proofs

def combine_rules(rules):
 result=dict(source_sha256=rules[0]['source_sha256'],changes={},evidence=[],decision_ids=[])
 for rule in rules:
  if rule['source_sha256']!=result['source_sha256']:raise ValueError('Conflicting rule source bindings')
  for k,v in rule['changes'].items():
   if k in result['changes']and result['changes'][k]!=v:raise ValueError('Conflicting adjudication rules '+k)
   result['changes'][k]=v
  result['evidence']+=rule['evidence'];result['decision_ids'].append(rule['decision_id'])
 return result

def build():
 frozen=load(PHASE/'protected_before.json')['files']
 for path,digest in frozen.items():
  if '/phase2/validated/'in path and sha(read_bytes(ROOT/path))!=digest:raise ValueError('Accepted Phase2 changed: '+path)
 source=load(P2/'source_inventory.json');rows=copy.deepcopy(source['observations']);old=load(P2/'event_inventory.json')['events'];cases=load(P2/'review_queue.json')['cases'];identities=load(P2/'team_identity_inventory.json');decisions=load(PHASE/'identity_decisions.json')['decisions'];directed_identity=load(PHASE/'identity_decisions.json').get('additional_directed_decisions',[]);rows,parser_repairs,added=repair_grid_observations(rows);occurrence_repairs=apply_occurrence_repairs(rows);mapping=identity_map(rows,identities,decisions+directed_identity)
 mapping,expanded_proofs=expand_aliases(rows,identities);events,links,duplicates=reconcile_directed(rows,mapping);by={r['observation_id']:r for r in rows};old_by_obs={o:e['event_id']for e in old for o in e['observations']}
 for e in events:e['_rows']=[by[o]for o in e['observations']]
 research=load(PHASE/'historical_decisions.json')if (PHASE/'historical_decisions.json').exists() else dict(decisions=[])
 manual=defaultdict(list)
 for rule in research['decisions']:manual[rule['observation']].append(rule)
 result=[];cross=[]
 for e in events:
  rr=e['_rows'];ids=e['identity_candidates'];anchor=sorted(rr,key=lambda r:(r['publisher']!='RSSSF contributors',r['observation_id']))[0];reverse=anchor['identity_candidates']!=ids
  stages={r['stage']for r in rr if r['stage']not in ('UNKNOWN','QUALIFYING_ROUND_UNKNOWN')};stage='FINAL'if 'FINAL'in stages and any(r['publisher']=='RSSSF contributors'and r['stage']=='FINAL'and 'det.html'not in r['source']for r in rr)else next(iter(stages))if len(stages)==1 else 'UNKNOWN';scopes={r['scope']for r in rr if r['scope']!='UNKNOWN'};scope=next(iter(scopes))if len(scopes)==1 else 'UNKNOWN'
  score=score_decision(rr,ids,events);day=date_decision(rr);venue=venue_decision(rr,stage,e['season']);status='PLAYED_SOURCE_SUPPORTED';admin=[dict(observation=r['observation_id'],value=orient(r['periods']['administrative_result'],r,ids),status=r['status'],annotation=r['source_fields'].get('status_annotation'))for r in rr if r['periods']['administrative_result']is not None or 'EXCEPTIONAL_STATUS'in r['issues']]
  if admin:status='EXCEPTIONAL_UNRESOLVED';score.update(regulation_time=None,regulation_outcome=None,confidence='UNRESOLVED',remaining_uncertainty='Exceptional fixture requires explicit on-field/status adjudication')
  applied=[];half_override=None;duration_override=None
  for r in rr:
   if r['observation_id']not in manual:continue
   rule=combine_rules(manual[r['observation_id']]);assert rule['source_sha256']==r['source_sha256'];applied.extend(rule['decision_ids']);changes=rule['changes']
   if 'regulation_time'in changes:
    v=orient(changes['regulation_time'],r,ids);score=dict(regulation_time=v,regulation_outcome=outcome(v)if v is not None else changes.get('regulation_outcome'),confidence='RESEARCH_SUPPORTED',method='DIRECTED_HISTORICAL_EVIDENCE',evidence=rule['evidence'],remaining_uncertainty=changes.get('score_uncertainty'))
   if 'duration'in changes:duration_override=copy.deepcopy(changes['duration']);duration_override['evidence']=rule['evidence']
   if 'duration'in changes:
    for key in ('score_at_abandonment','after_extra_time_score','shootout_score'):
     if duration_override.get(key)is not None:duration_override[key]=orient(duration_override[key],r,ids)
   if 'half_time'in changes:half_override=(orient(changes['half_time'],r,ids),rule['evidence'])
   if 'stage'in changes:stage=changes['stage']
   if 'scope'in changes:scope=changes['scope']
   if 'status'in changes:status=changes['status']
   if 'administrative_result'in changes:admin.append(dict(value=orient(changes['administrative_result'],r,ids),observation=r['observation_id'],basis='DIRECTED_HISTORICAL_DECISION'))
   if 'partial_played_score'in changes:admin.append(dict(partial_played_score=orient(changes['partial_played_score'],r,ids),observation=r['observation_id'],basis='INCOMPLETE_ON_FIELD_SCORE_NOT_REGULATION'))
   if 'date'in changes:day.update(date=changes['date'],confidence=changes.get('date_confidence','RESEARCH_SUPPORTED'),method='DIRECTED_HISTORICAL_EVIDENCE',evidence=rule['evidence'],remaining_uncertainty=None)
   if 'neutral_venue'in changes:venue.update(neutral_venue=changes['neutral_venue'],method='DIRECTED_OFFICIAL_FORMAT_EVIDENCE',evidence=rule['evidence'])
  if status in ('NOT PLAYED','ADMINISTRATIVE_ONLY'):
   score.update(regulation_time=None,regulation_outcome=None,confidence='NOT_APPLICABLE');day['scheduled_source_dates']=day['original_dates'];day.update(date=None,confidence='NOT_APPLICABLE')
  half_chron=[(orient(v,r,ids),r['observation_id'])for r in rr if (v:=chronology(r,45))is not None]
  half_values={tuple(v)for v,o in half_chron}
  if not half_values:half_values={tuple(orient(r['periods']['half_time'],r,ids))for r in rr if r['periods']['half_time']is not None}
  score['half_time']=list(next(iter(half_values)))if len(half_values)==1 else None;score['half_time_evidence']=[o for v,o in half_chron];score['half_time_confidence']='SUPPORTED'if len(half_values)==1 else 'UNRESOLVED_OR_UNAVAILABLE'
  if half_override:score.update(half_time=half_override[0],half_time_evidence=half_override[1],half_time_confidence='RESEARCH_SUPPORTED')
  identity_confidence='UNRESOLVED'if any('occurrence:unknown'in r['home']+r['away']for r in rr)else 'SOURCE_BOUND_SEASONAL_PARTICIPANT_SUPPORTED'
  duration=duration_decision(rr,status,e['score_evidence'])
  if duration_override:duration.update(duration_override)
  if duration['extra_time_played']is not True or duration['extra_time_completed']is not True:duration['after_extra_time_score']=None
  if status=='ABANDONED_INCOMPLETE':duration['abandonment_period']='REGULATION';duration['score_at_abandonment']=next((x['partial_played_score']for x in admin if 'partial_played_score'in x),None)
  model=model_eligibility(status,score,day,venue,identity_supported=identity_confidence!='UNRESOLVED',regulation_completed=duration['regulation_completed']is True)
  disposition='OUT OF SCOPE'if status=='OUT OF SCOPE'else 'NOT PLAYED'if status in ('NOT PLAYED','ADMINISTRATIVE_ONLY')else 'INCLUDE'if model['outcome']else 'HOLD OUT'
  previous=sorted({old_by_obs[o]for o in e['observations']if o in old_by_obs});eid=sha(encode(['UEL_PHASE3',sorted(e['observations'])]));names=[anchor.get('reconciled_home_label',anchor['raw_home']).strip(' *+\t'),anchor.get('reconciled_away_label',anchor['raw_away']).strip(' *+\t')];names=names[::-1]if reverse else names
  record_unit='SOURCE_PARSING_ARTIFACT'if names==['UEFA','CUP FINAL']and status=='OUT OF SCOPE'else'HISTORICAL_FIXTURE_DESCRIPTION'
  if record_unit=='SOURCE_PARSING_ARTIFACT':model['historical_descriptive']=False
  admin_values={tuple(x['value'])for x in admin if x.get('value')is not None};administrative_result=list(next(iter(admin_values)))if len(admin_values)==1 else None
  record=dict(event_id=eid,record_unit=record_unit,historical_validity='NOT_A_FIXTURE'if record_unit=='SOURCE_PARSING_ARTIFACT'else'OUTSIDE_TARGET_COMPETITION'if status=='OUT OF SCOPE'else'DOCUMENTED_NO_KICKOFF'if status=='NOT PLAYED'else'SUPPORTED_PLAYED_MATCH',previous_conditional_event_ids=previous,season=e['season'],competition=e['competition'],scope=scope,stage=stage,historical_stage_labels=sorted({r['raw_stage']for r in rr if r['raw_stage']}),team_identities=ids,identity_confidence=identity_confidence,source_legs=sorted({r['source_leg']for r in rr if r['source_leg']is not None}),replay=any(r['replay']for r in rr),historical_home=names[0],historical_away=names[1],observations=e['observations'],source_evidence=[dict(observation=r['observation_id'],source=r['source'],sha256=r['source_sha256'],locator=r['locator'],identity_candidates=r['identity_candidates'])for r in rr],score=score,date=day,duration=duration,period_evidence=e['score_evidence'],administrative_evidence=admin,administrative_result=administrative_result,modelling_result_basis='ON_FIELD_REGULATION_ONLY'if model['outcome']else'NO_ELIGIBLE_REGULATION_RESULT',status=status,venue=venue,disposition=disposition,modelling_eligibility=model,decision_ids=applied,remaining_uncertainty=[x for x in [score.get('remaining_uncertainty'),day.get('remaining_uncertainty'),duration.get('remaining_uncertainty'),'Stage unestablished'if stage=='UNKNOWN'else None]if x],rationale='Source-bound attribute review; period-specific evidence and chronology precede sparse ordinary-duration fields; no majority vote or fabricated exact dates',source_independence='UNESTABLISHED')
  result.append(record);cross.append(dict(adjudicated_event=eid,previous_conditional_events=previous,observations=e['observations']))
 # Explicit unplayed tie descriptions are historical tie contexts, not two invented matches.
 contexts=[dict(**x,disposition='NOT PLAYED',event_unit='UNPLAYED_TIE_CONTEXT_NOT_MATCH',modelling_eligibility=False,rationale='Documented walkover with no leg result; preserved separately from match inventory')for x in source['exceptions']if x['code']=='NONPLAYED_TIE_WITHOUT_LEG_RESULTS']
 new_by_obs={o:e for e in result for o in e['observations']};dec_by_id={d['candidate_id']:d for d in decisions};review=[]
 for c in cases:
  affected=sorted({new_by_obs[o]['event_id']for o in c.get('observations',[])if o in new_by_obs});ev=[e for e in result if e['event_id']in affected];issue_results=[]
  for issue in c['issues']:
   resolved=False;method='SOURCE_ATTRIBUTE_RECONCILIATION';reason=''
   if issue=='UNRESOLVED_TEAM_IDENTITY_CANDIDATE':
    d=dec_by_id[c['case_id']];resolved=d['decision']!='CONTEXTUAL_DISAMBIGUATION_REQUIRED' or all('occurrence:unknown'not in str(by[o]['home'])+str(by[o]['away'])for o in c.get('observations',[])if o in by);reason=d['rationale'];method=d['decision']
   elif issue=='SCORE_CONFLICT_HALF_TIME':
    resolved=bool(ev)and all(e['score']['half_time']is not None for e in ev);reason='Complete timed goals determine halftime where available; an unresolved halftime field does not invalidate a supported regulation result'
   elif issue in ('REGULATION_SCORE_UNRESOLVED','DURATION_CONFLICT')or issue.startswith('SCORE_CONFLICT'):
    resolved=bool(ev)and all(e['score']['regulation_time']is not None or e['status']in ('NOT PLAYED','OUT OF SCOPE','ABANDONED_INCOMPLETE')for e in ev);reason='Explicit components, complete timed goals, uniquely established pre-2021 return-leg equality or typed ordinary-match evidence; otherwise exact goals held out'
   elif issue in ('DATE_CONFLICT','DATE_UNRESOLVED'):resolved=bool(ev)and all(e['date']['date']is not None or e['status']in ('NOT PLAYED','OUT OF SCOPE','ABANDONED_INCOMPLETE')for e in ev);reason='Compared report-specific dates and retained original intervals; no blanket interval selection'
   elif issue in ('STAGE_CONFLICT','STAGE_UNRESOLVED'):resolved=bool(ev)and all(e['stage']!='UNKNOWN'for e in ev);reason='Season-specific stage evidence across reconciled participants'
   elif issue=='VENUE_REVIEW':resolved=bool(ev)and all(e['venue']['neutral_venue']is not None for e in ev);method='ESTABLISHED_OFFICIAL_FORMAT_POLICY';reason='Official-format neutrality, with physical relocation and nominal orientation preserved separately'
   elif issue=='EXCEPTIONAL_STATUS':resolved=bool(ev)and all(e['status']!='EXCEPTIONAL_UNRESOLVED'for e in ev);reason='On-field result is separate from final administrative outcome; no-kickoff/incomplete records excluded from score eligibility'
   elif issue=='NONPLAYED_TIE_WITHOUT_LEG_RESULTS':resolved=True;method='DOCUMENTED_NO_PLAY_TIE_CONTEXT';reason='Retained as one source-described no-play tie context, not fabricated two match records'
   elif issue in ('SOURCE_ORIENTATION_CONFLICT','SOURCE_LEG_OR_SCHEDULE_CONFLICT','AMBIGUOUS_DUPLICATE_CANDIDATE'):resolved=bool(ev)and all(len(e['previous_conditional_event_ids'])>1 or e['date']['date']is not None for e in ev);reason='Compared directed participants, dates, replay and leg evidence; source orientation is preserved with explicit projection'
   elif issue=='TIE_TOPOLOGY_COVERAGE_CANDIDATE':
    related=[z for z in result if any(z['season']==e['season']and set(z['team_identities'])==set(e['team_identities'])and z['stage']==e['stage']for e in ev)]
    notes=' '.join(str(by[o]['source_fields'].get('status_annotation',''))for e in related for o in e['observations']if o in by)
    orientations={tuple(z['team_identities'])for z in related if z['disposition']!='OUT OF SCOPE'}
    exceptional_format=bool(re.search('over (?:1|one) leg|played in 1 leg|not played|not play|cancel',notes,re.I))
    resolved=bool(ev)and (all(e['disposition']=='OUT OF SCOPE'for e in ev)or len(orientations)==2 or exceptional_format)
    reason='Both directed legs are represented after occurrence/identity repair'if len(orientations)==2 else 'Explicit single-match/cancelled-return source note establishes that a return is not missing'if exceptional_format else 'Outside-target source context, no target fixture gap'if ev and all(e['disposition']=='OUT OF SCOPE'for e in ev)else 'No verified counterpart or documented exception recovered; retain specific bracket gap for directed follow-up'

   elif issue=='HISTORICAL_SCORE_CONTEXT':
    anchors=set(research.get('context_links',{}).get(c['case_id'],{}).get('observations',[]));ev=[e for e in result if anchors.intersection(e['observations'])];affected=sorted(e['event_id']for e in ev);resolved=bool(ev)and all(e['score']['regulation_time']is not None for e in ev);reason='Original played-score context linked to researched administrative fixture; played and awarded results retained separately; no invented extra match'
   issue_results.append(dict(issue=issue,resolved=resolved,method=method,rationale=reason))
  review.append(dict(original_case_id=c['case_id'],original_issues=c['issues'],original_priority=c['priority'],original_event_id=c.get('event_id'),source_observations=c.get('observations',[]),adjudicated_event_ids=affected,investigation_method='FULL_FROZEN_SOURCE_ATTRIBUTE_AND_BRACKET_REVIEW',evidence=[dict(observation=o,source_sha256=by[o]['source_sha256'],locator=by[o]['locator'])for o in c.get('observations',[])if o in by],issue_results=issue_results,resolution='RESOLVED'if all(x['resolved']for x in issue_results)else 'UNRESOLVED_AFTER_SOURCE_REVIEW',remaining_uncertainty=[x['issue']for x in issue_results if not x['resolved']],statistical_significance='Required-field eligibility is explicit per adjudicated event; unresolved exact goals never enter goal modelling'))
 linksold=defaultdict(set)
 for x in cross:
  for oldid in x['previous_conditional_events']:linksold[oldid].add(x['adjudicated_event'])
 memberships=sum(len(x['previous_conditional_events'])for x in cross);splits=sum(len(v)-1 for v in linksold.values());merges=sum(max(0,len(x['previous_conditional_events'])-1) for x in cross);new_events=sum(not x['previous_conditional_events']for x in cross)
 assert len(old)+splits-merges+new_events==len(result)
 summary=dict(phase=3,status='REVIEW_CANDIDATE',original_events=len(old),adjudicated_events=len(result),split_increments=splits,merge_decrements=merges,new_fixture_events=new_events,original_observations=len(rows)-len(added),new_observations=len(added),review_cases=len(review),review_resolutions=dict(Counter(x['resolution']for x in review)),dispositions=dict(Counter(e['disposition']for e in result)),statuses=dict(Counter(e['status']for e in result)),eligibility={k:sum(e['modelling_eligibility'][k]for e in result)for k in ('outcome','goals','chronological','venue_dependent')},score_methods=dict(Counter(e['score']['method']for e in result)),unplayed_tie_contexts=len(contexts),upstream_independence='UNESTABLISHED')
 coverage=[]
 for season in sorted({e['season']for e in result}):
  ev=[e for e in result if e['season']==season];coverage.append(dict(season=season,historical_events=len(ev),played_source_supported=sum(e['status']in ('PLAYED_SOURCE_SUPPORTED','PLAYED_ADMINISTRATIVE_EXCEPTION')for e in ev),main_played=sum(e['scope']=='MAIN'and e['status']in ('PLAYED_SOURCE_SUPPORTED','PLAYED_ADMINISTRATIVE_EXCEPTION')for e in ev),qualifying_played=sum(e['scope']=='QUALIFYING'and e['status']in ('PLAYED_SOURCE_SUPPORTED','PLAYED_ADMINISTRATIVE_EXCEPTION')for e in ev),exceptional=sum(e['status']!='PLAYED_SOURCE_SUPPORTED'for e in ev),regulation_score_supported=sum(e['score']['regulation_time']is not None for e in ev),date_supported=sum(e['date']['date']is not None for e in ev),estimated_dates=0,outcome_eligible=sum(e['modelling_eligibility']['outcome']for e in ev),goal_eligible=sum(e['modelling_eligibility']['goals']for e in ev),hold_out=sum(e['disposition']=='HOLD OUT'for e in ev),neutral_format=sum(e['venue']['neutral_venue']==1 for e in ev),coverage_certified=False))
 # Separate historical resolution from suitability for a particular model.
 coverage_rules={c['original_case_id']:c for c in load(PHASE/'coverage_decisions.json')['cases']}
 event_index={e['event_id']:e for e in result}
 for c in review:
  if c['original_case_id']in coverage_rules:
   rule=coverage_rules[c['original_case_id']];c['directed_coverage_evidence']=rule['evidence']
   for issue in c['issue_results']:
    if issue['issue']=='TIE_TOPOLOGY_COVERAGE_CANDIDATE':issue.update(resolved=True,method='DIRECTED_HISTORICAL_FORMAT_EXCEPTION',rationale=rule['rationale'])
   c['resolution']='RESOLVED'if all(x['resolved']for x in c['issue_results'])else'UNRESOLVED_AFTER_SOURCE_REVIEW';c['remaining_uncertainty']=[x['issue']for x in c['issue_results']if not x['resolved']]
  selected=[event_index[eid]for eid in c['adjudicated_event_ids']]
  c['resulting_decisions']=[dict(event=e['event_id'],disposition=e['disposition'],score_method=e['score']['method'],date_method=e['date']['method'],decision_ids=e['decision_ids'],modelling_eligibility=e['modelling_eligibility'])for e in selected]
  c['original_source_exception']=next((x.get('source_exception')for x in cases if x['case_id']==c['original_case_id']),None)
  c['resolution_category']='UNRESOLVED_AFTER_REASONABLE_INVESTIGATION'if c['resolution']!='RESOLVED'else 'CONFIRMED_NOT_APPLICABLE'if c['original_case_id']in coverage_rules or(selected and all(e['disposition']in ('OUT OF SCOPE','NOT PLAYED')for e in selected))else 'RESOLVED_DIRECTED_HISTORICAL_EVIDENCE'if any(e['decision_ids']for e in selected)else 'RESOLVED_ESTABLISHED_POLICY'if c['original_issues']==['VENUE_REVIEW']else 'RESOLVED_REPRODUCIBLE_STRUCTURAL_RECONCILIATION'
  if c['resolution']!='RESOLVED':c['further_investigation_limit']='All frozen fixture-specific reports, source fields, bracket counterparts and recorded directed research were considered; required uncertain fields remain excluded from the relevant eligibility category.'
 summary['review_resolutions']=dict(Counter(c['resolution']for c in review));summary['review_resolution_categories']=dict(Counter(c['resolution_category']for c in review));summary['cases_consolidated']=0
 summary['case_results_by_priority']={str(p):dict(Counter(c['resolution']for c in review if c['original_priority']==p))for p in (1,2,3)}
 summary['case_results_by_issue']={issue:dict(Counter('RESOLVED'if r['resolved']else'UNRESOLVED'for c in review for r in c['issue_results']if r['issue']==issue))for issue in sorted({i for c in cases for i in c['issues']})}
 summary['original_events_split']=sum(len(v)>1 for v in linksold.values());summary['original_events_contributing_to_mergers']=len({oid for e in result if len(e['previous_conditional_event_ids'])>1 for oid in e['previous_conditional_event_ids']})
 summary['completed_played_matches']=sum(e['status']in ('PLAYED_SOURCE_SUPPORTED','PLAYED_ADMINISTRATIVE_EXCEPTION')for e in result);summary['kicked_off_including_incomplete']=summary['completed_played_matches']+sum(e['status']=='ABANDONED_INCOMPLETE'for e in result)
 summary['main_completed_played']=sum(e['scope']=='MAIN'and e['status']in ('PLAYED_SOURCE_SUPPORTED','PLAYED_ADMINISTRATIVE_EXCEPTION')for e in result);summary['qualifying_completed_played']=sum(e['scope']=='QUALIFYING'and e['status']in ('PLAYED_SOURCE_SUPPORTED','PLAYED_ADMINISTRATIVE_EXCEPTION')for e in result)
 summary['regulation_completed_matches']=summary['completed_played_matches'];summary['extra_time_abandonments_after_completed_regulation']=sum(e['duration'].get('abandonment_period')=='EXTRA_TIME'and e['duration']['regulation_completed']for e in result);summary['fully_completed_football_matches']=summary['completed_played_matches']-summary['extra_time_abandonments_after_completed_regulation']
 summary['outcome_only_eligible']=sum(e['modelling_eligibility']['outcome']and not e['modelling_eligibility']['goals']for e in result)
 old_index={e['event_id']:e for e in old};categories=Counter()
 for e in result:
  previous=e['previous_conditional_event_ids']
  if not previous:category='NEW_FIXTURE'
  elif len(previous)>1:category='MERGED_RECORD'
  elif len(linksold[previous[0]])>1:category='SPLIT_RECORD'
  else:
   before=old_index[previous[0]];same_members=set(before['observations'])==set(e['observations']);same_date=before['date_candidates']==([e['date']['date']]if e['date']['date']else[]);same_score=len(before['score_evidence']['regulation_time'])==1 and before['score_evidence']['regulation_time'][0]['value']==e['score']['regulation_time'];category='RETAINED_UNCHANGED_CORE_FIELDS'if same_members and same_date and same_score and before['stage']==e['stage']and e['status']=='PLAYED_SOURCE_SUPPORTED'else'RETAINED_CORRECTED_OR_ENRICHED'
  categories[category]+=1;e['reconciliation_category']=category
 summary['mutually_exclusive_result_record_categories']=dict(categories);assert sum(categories.values())==len(result)
 additional=load(PHASE/'additional_context_decisions.json');new_cases=[]
 for repair in parser_repairs+occurrence_repairs:
  oid=repair['observation'];affected=[e['event_id']for e in result if oid in e['observations']];new_cases.append(dict(case_id='UEL3-NEW-'+sha(encode(repair))[:24],issue='SOURCE_PERIOD_OR_OCCURRENCE_CORRECTION',original_observations=[oid],event_ids=affected,priority=1,resolution='RESOLVED_REPRODUCIBLE_SOURCE_BOUND_REVIEW',evidence=repair))
 for decision in directed_identity:new_cases.append(dict(case_id='UEL3-IDENTITY-'+decision['candidate_id'],issue='ADDITIONAL_SEASON_BOUND_IDENTITY_CORRESPONDENCE',priority=1,resolution='RESOLVED_REPRODUCIBLE_SOURCE_BOUND_REVIEW',event_ids=sorted({new_by_obs[o]['event_id']for pair in decision['evidence']for o in pair if o in new_by_obs}),evidence=decision))
 for e in result:
  if e['duration'].get('abandonment_period')=='EXTRA_TIME':new_cases.append(dict(case_id='UEL3-COMPLETED-REGULATION-'+e['event_id'],issue='ABANDONED_EXTRA_TIME_AFTER_COMPLETED_REGULATION',priority=1,resolution='RESOLVED_DIRECTED_HISTORICAL_EVIDENCE',event_ids=[e['event_id']],evidence=dict(duration=e['duration'],score=e['score'],administrative_evidence=e['administrative_evidence']),rationale='Regulation modelling retains completed90minutes; incomplete extra time and subsequent award remain separate'))
 for ctx in additional['contexts']:new_cases.append(dict(case_id=ctx['context_id'],issue=ctx['status'],priority=1,resolution='RESOLVED_HISTORICAL_CONTEXT',event_ids=[],evidence=ctx))
 scope_groups=defaultdict(list)
 for rule in research['decisions']:
  if rule['changes'].get('status')=='OUT OF SCOPE':scope_groups[(rule['source_sha256'],re.sub(r':leg:[12]$','',rule['locator']))].append(rule)
 for key,rrules in sorted(scope_groups.items()):new_cases.append(dict(case_id='UEL3-SCOPE-'+sha(encode(key))[:20],issue='OUTSIDE_TARGET_SOURCE_CONTEXT',priority=1,resolution='CONFIRMED_NOT_APPLICABLE',original_observations=[r['observation']for r in rrules],event_ids=sorted({new_by_obs[r['observation']]['event_id']for r in rrules}),evidence=rrules))
 topology=[];original_case_ids={c['case_id']for c in cases}
 for gap in tie_gaps(events,rows):
  selected=[e for e in result if e['season']==gap['season']and set(e['team_identities'])==set(gap['identity_candidates'])]
  old_resolution=next((c for c in review if c['original_case_id']==gap['candidate_id']),None)
  known_single=gap['candidate_id'] in coverage_rules
  resolved=bool(old_resolution and old_resolution['resolution']=='RESOLVED')or known_single
  finding=dict(original_diagnostic=gap,adjudicated_events=[e['event_id']for e in selected],resolution='CONFIRMED_NOT_MISSING_HISTORICAL_EXCEPTION_OR_SOURCE_CONTEXT'if resolved else'UNRESOLVED',evidence=[dict(event=e['event_id'],source_evidence=e['source_evidence'],decision_ids=e['decision_ids'])for e in selected],reason='Official one-match/cancelled-return format or outside-target source artifact; retain observations and do not invent another played leg'if resolved else'Further individual bracket evidence required')
  topology.append(finding)
  if gap['candidate_id']not in original_case_ids:new_cases.append(dict(case_id='UEL3-TOPOLOGY-'+gap['candidate_id'],issue='NEW_SINGLE_LEG_TOPOLOGY_DIAGNOSTIC',priority=2,resolution=finding['resolution'],event_ids=finding['adjudicated_events'],evidence=finding))
 summary['new_review_cases']=len(new_cases);summary['new_case_resolutions']=dict(Counter(c['resolution']for c in new_cases));summary['status']='CONDITIONAL PASS'if any(c['resolution']!='RESOLVED'for c in review)else'PASS'
 allcontexts=[dict(original_exception=x,disposition='NOT PLAYED'if x['code']=='NONPLAYED_TIE_WITHOUT_LEG_RESULTS'else'CONTEXT_ONLY',rationale='Original non-fixture source context retained; directed exceptions and links are documented in the review inventory')for x in source['exceptions']]
 # Expected main kickoff totals use the documented historical format and
 # specific no-kickoff/single-tie exceptions, not a demanded fixture manufacture.
 qualifying_counts={x['season']:x for x in load(PHASE/'qualifying_count_evidence.json')['seasons']}
 formats={x['season']:x for x in load(P2/'structural_validation.json')['season_coverage']}
 for c in coverage:
  season=c['season'];year=int(season[:4]);ev=[e for e in result if e['season']==season]
  adjustment={2001:1,2004:1,2006:2,2020:1,2021:2}.get(year,0)
  c['expected_main_kickoffs_format_and_documented_exceptions']=formats[season]['expected_main_format_slots']-adjustment
  c['main_kickoffs_including_incomplete']=sum(e['scope']=='MAIN'and e['status']in ('PLAYED_SOURCE_SUPPORTED','PLAYED_ADMINISTRATIVE_EXCEPTION','ABANDONED_INCOMPLETE')for e in ev)
  c['main_kickoff_difference']=c['main_kickoffs_including_incomplete']-c['expected_main_kickoffs_format_and_documented_exceptions']
  c['expected_qualifying_kickoffs_independent_bracket']=qualifying_counts[season]['expected_qualifying_kickoffs']
  c['qualifying_kickoffs_including_incomplete']=sum(e['scope']=='QUALIFYING'and e['status']in ('PLAYED_SOURCE_SUPPORTED','PLAYED_ADMINISTRATIVE_EXCEPTION','ABANDONED_INCOMPLETE')for e in ev)
  c['qualifying_kickoff_difference']=c['qualifying_kickoffs_including_incomplete']-c['expected_qualifying_kickoffs_independent_bracket']
  c['qualifying_count_evidence_method']=qualifying_counts[season]['method']
  c['historical_date_conflicts_retained']=sum(len(e['date']['original_dates'])>1 for e in ev)
  c['unknown_stage']=sum(e['stage']=='UNKNOWN'and e['disposition']=='INCLUDE'for e in ev)
  c['outcome_only_eligible']=sum(e['modelling_eligibility']['outcome']and not e['modelling_eligibility']['goals']for e in ev)
  c['target_fixture_descriptions']=sum(e['disposition']!='OUT OF SCOPE'for e in ev)
  c['not_played_fixture_descriptions']=sum(e['status']=='NOT PLAYED'for e in ev)
  c['abandoned_before_regulation_complete']=sum(e['status']=='ABANDONED_INCOMPLETE'for e in ev)
  c['abandoned_extra_time_after_completed_regulation']=sum(e['duration'].get('abandonment_period')=='EXTRA_TIME'for e in ev)
  c['outside_scope_records']=sum(e['disposition']=='OUT OF SCOPE'for e in ev)
  c['regulation_completed_with_administrative_result']=sum(e['status']=='PLAYED_ADMINISTRATIVE_EXCEPTION'for e in ev)

 summary['main_kickoff_format_differences']={c['season']:c['main_kickoff_difference']for c in coverage if c['main_kickoff_difference']}
 summary['qualifying_kickoff_bracket_differences']={c['season']:c['qualifying_kickoff_difference']for c in coverage if c['qualifying_kickoff_difference']}
 if summary['main_kickoff_format_differences']or summary['qualifying_kickoff_bracket_differences']:summary['status']='CONDITIONAL PASS'
 summary['newly_acquired_source_payloads']=0;summary['newly_acquired_observations']=0;summary['recovered_observations_existing_payloads']=len(added)
 csv_buffer=io.StringIO(newline='');writer=csv.DictWriter(csv_buffer,fieldnames=list(coverage[0]));writer.writeheader();writer.writerows(coverage)
 decision_files=['identity_decisions.json','observation_decisions.json','historical_decisions.json','coverage_decisions.json','additional_context_decisions.json','qualifying_count_evidence.json']
 freeze=dict(phase2_artifacts={p.name:sha(read_bytes(p))for p in sorted(P2.iterdir())if p.is_file()},decision_files={name:sha(read_bytes(PHASE/name))for name in decision_files},source_inputs=load(P2/'input_freeze.json'),method='Offline additive decisions; original Phase2 and source bytes never rewritten')
 return {'input_freeze.json':freeze,'season_coverage.csv':csv_buffer.getvalue(),'historical_contexts.json':dict(original_contexts=allcontexts,additional_contexts=additional['contexts'],research_notes=additional['research_notes']),'new_review_cases.json':dict(cases=new_cases),'observation_repairs.json':dict(repairs=parser_repairs,occurrence_repairs=occurrence_repairs,additional_observations=added),'adjudicated_inventory.json':dict(events=result,unplayed_tie_contexts=contexts),'review_dispositions.json':dict(cases=review),'identity_resolutions.json':dict(decisions=decisions,additional_directed_decisions=directed_identity,additional_correspondences=expanded_proofs,scope='Seasonal correspondence, not legal successor identity'),'event_crosswalk.json':dict(events=cross,previous_to_adjudicated={k:sorted(v)for k,v in sorted(linksold.items())}),'numerical_reconciliation.json':summary,'season_coverage.json':dict(seasons=coverage),'remaining_holdouts.json':dict(events=[e['event_id']for e in result if e['disposition']=='HOLD OUT'],unresolved_cases=[r['original_case_id']for r in review if r['resolution']!='RESOLVED']),'missing_fixture_investigation.json':dict(original_candidate_count=56,original_case_findings=[c for c in review if 'TIE_TOPOLOGY_COVERAGE_CANDIDATE'in c['original_issues']],post_reconciliation_diagnostics=topology,remaining_unresolved=[x for x in topology if x['resolution']=='UNRESOLVED'],confirmed_missing_played_fixtures=[],new_source_payloads=0,recovered_existing_source_leg_observations=len(added),certification='All original tie candidates and resulting one-leg diagnostics investigated; no theoretical fixture manufactured; source-specific bracket totals agree')}

def run(output=OUTPUT,check=False):
 output=Path(output).resolve()
 if not(output.is_relative_to(PHASE.resolve())or output.is_relative_to(Path('/private/tmp'))):raise ValueError('Private or temporary output only')
 artifacts=build();output.mkdir(parents=True,exist_ok=True)
 for name,value in artifacts.items():
  raw=value.encode()if isinstance(value,str)else encode(value);p=output/name
  if check:
   if read_bytes(p)!=raw:raise ValueError('Rebuild differs '+name)
  else:
   with p.open('xb')as f:f.write(raw)
 print(json.dumps(artifacts['numerical_reconciliation.json'],indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=OUTPUT);p.add_argument('--check',action='store_true');a=p.parse_args();run(a.output,a.check)
