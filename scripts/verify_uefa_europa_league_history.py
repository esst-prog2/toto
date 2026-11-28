"""Independent Phase 3 artifact and high-risk attribute reconstruction.

No Phase 3 production parser, aliases, IDs, period or eligibility helpers imported.
All regulation decisions are checked; URL factual notes require the documented
historical research and are not falsely certified as downloaded primary originals.
"""
import argparse
from collections import Counter,defaultdict
import copy
import csv
import hashlib
import html
import io
import json
import mmap
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'data/private/europe/europa_league'
PHASE=BASE/'phase3'

def read(p):
 with Path(p).open('rb')as f:
  if not Path(p).stat().st_size:return b''
  with mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ)as m:return m[:]
def load(p):return json.loads(read(p))
def digest(b):return hashlib.sha256(b).hexdigest()
def wire(x):return(json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
def require(ok,message):
 if not ok:raise ValueError(message)
def minute(v):
 m=re.fullmatch(r"\s*(\d{1,3})(?:\+\d+)?['’]?\s*",str(v));return int(m.group(1))if m else None

def timed(r,cutoff=90):
 f=r['source_fields'];total=r['periods']['after_extra_time']or r['periods']['published_final']
 if total is None:return None
 if 'goal_rows'in f:
  prev=(0,0);result=(0,0);last=-1
  for g in f['goal_rows']:
   current=(int(g['GH']),int(g['GA']));t=minute(g['time']);delta=tuple(a-b for a,b in zip(current,prev))
   if t is None or t<last or t>120 or delta not in ((1,0),(0,1)):return None
   if t<=cutoff:result=current
   prev=current;last=t
  return list(result)if list(prev)==total else None
 fs=f.get('fields',{})
 if not({'goals1','goals2'}&fs.keys()):return None
 times=[]
 for side in ('goals1','goals2'):
  values=[]
  for body in re.findall(r'\{\{\s*goal\s*\|([^{}]*)\}\}',fs.get(side,''),re.I):
   values.extend(a.strip()for a in body.split('|')if re.fullmatch(r'\d+(?:\+\d+)?',a.strip()))
  times.append(values)
 if [len(x)for x in times]!=total:return None
 return [sum(minute(t)<=cutoff for t in x)for x in times]


def independent_qualifying_counts(events):
 vocabulary='Eng Sco Wal Nir Nil Ire Irl Ned Net Ger FRG GDR Aut Sui Ita Fra Esp Por Bel Den Nor Swe Fin Fni Isl Ice Far Pol Tch Cze Svk Hun Hon Rom Rou Bul Gre Grk Tur URS Rus Ukr Bls Blr Est Lat Lva Lit Ltu Mol Mda Geo Arm Aze Azb Isr Cyp Mlt Mal Lie Lux And SMa SMr SMR Gib Kaz Mac Mkd Alb Bos BiH Bih Cro Slo Sln Ser Srb SeM Yug Mng Mne Mon Kos'.split();codes='|'.join(vocabulary)
 results=[]
 for p in sorted((BASE/'phase1/originals/rsssf').glob('*.html')):
  if'det'in p.name:continue
  year=int(p.name[2:6]);season=f'{year}/{year+1}';raw=read(p)
  try:markup=raw.decode('utf-8-sig')
  except UnicodeDecodeError:markup=raw.decode('cp1252')
  anchor=re.search(r'<a\b[^>]*(?:name|id)\s*=\s*["\']?uefa(?:["\']|\s|>)',markup,re.I)
  if not anchor:continue
  fragment=markup[anchor.end():];end=re.search(r'<h2\b',fragment,re.I);fragment=fragment[:end.start()]if end else fragment;fragment=re.sub(r'^.*?</h2>', '',fragment,count=1,flags=re.I)if'</h2>'in fragment.split('\n')[0].lower()else fragment
  lines=[html.unescape(re.sub('<[^>]+>','',line)).replace('\xa0',' ')for line in fragment.splitlines()];stage=None;count=0;accepted=[]
  for index,line in enumerate(lines):
   t=line.strip()
   if re.match(r'^(?:Preliminary (?:Round|Phase)|Qualifying (?:Round|Phase)|(?:First|Second|Third) Qualifying (?:Phase|Round)|Play.?off Round)',t,re.I):stage='Q'
   elif year>=2009 and re.match(r'^First Round',t,re.I):stage='Q'
   elif re.match(r'^UIC (?:Semi|Final)',t,re.I):stage='OUT'
   elif re.match(r'^(?:First Round|Group (?:Phase|Stage)|Intermediate|1/[248] Finals|Quarter|Semi|Final)',t,re.I):stage='MAIN'
   if stage!='Q':continue
   scorestart=re.search(r'\bawd\b|\d+-\d+',t)
   if not scorestart:continue
   prefix=t[:scorestart.start()].rstrip();countrymatches=list(re.finditer(r'('+codes+r')\*?(?:\s+|$)',prefix))
   if len(countrymatches)<2:continue
   tail=t[scorestart.start():];tokens=re.findall(r'\bawd\b|\d+-\d+[a-z*]*',tail)
   if not tokens:continue
   markers=set(re.findall(r'\d+-\d+\*?([a-z])',tail));notes=[]
   for subsequent in lines[index+1:]:
    if re.match(r'^\s*(?:Preliminary Round|Qualifying Round|First Round|Second Round|Third Round|Fourth Round)',subsequent):break
    mm=re.match(r'^\s*([a-z])\s+(.+)',subsequent)
    if mm and mm[1]in markers:notes.append(mm[2])
   if any(re.search(r'Inter.?toto.*(?:Semi|Final)',s,re.I)for s in notes):continue
   # Three columns include aggregate; a fourth numeric column is shootout.
   legs=2 if len(tokens)>=3 else 1;count+=legs;accepted.append((t,legs))
  actual=sum(e['scope']=='QUALIFYING'and e['status']in('PLAYED_SOURCE_SUPPORTED','PLAYED_ADMINISTRATIVE_EXCEPTION','ABANDONED_INCOMPLETE')for e in events if e['season']==season)
  expected=count-(1 if year==2020 else 0);results.append(dict(season=season,raw_bracket_fixture_descriptions=count,documented_no_kickoff_adjustment=1 if year==2020 else 0,expected_qualifying_kickoffs=expected,adjudicated_qualifying_kickoffs=actual,difference=actual-expected))
 return results

def verify(directory=PHASE/'final'):
 directory=Path(directory);p2=BASE/'phase2/validated';freeze=load(directory/'input_freeze.json')
 for name,h in freeze['phase2_artifacts'].items():require(digest(read(p2/name))==h,'Phase2 changed '+name)
 for name,h in freeze['decision_files'].items():require(digest(read(PHASE/name))==h,'Decision input changed '+name)
 for item in freeze['source_inputs']['inputs']:
  raw=read(BASE/item['path']);require(len(raw)==item['bytes']and digest(raw)==item['sha256'],'Original changed '+item['path'])
 src=load(p2/'source_inventory.json');original={r['observation_id']:r for r in src['observations']};rows=copy.deepcopy(original);old_events=load(p2/'event_inventory.json')['events'];oldcases=load(p2/'review_queue.json')['cases'];repairs=load(directory/'observation_repairs.json')
 for fix in repairs['repairs']:
  r=rows[fix['observation']];require(r['source_sha256']==fix['source_sha256']and r['periods']==fix['before'],'Period correction binding')
  tokens=re.findall(r'(?<!\d)\*?\d+-\d+[a-z*]?',r['source_fields']['raw_line']);require(len(tokens)==3 and tokens[2].endswith('p'),'Not an aggregate footnote repair')
  scores=[list(map(int,re.search(r'(\d+)-(\d+)',t).groups()))for t in tokens];require(scores[2]==[scores[0][i]+scores[1][i]for i in (0,1)],'Third column is not corroborated aggregate')
  leg=r['source_leg']or 1;expected=copy.deepcopy(r['periods']);expected.update(shootout=None,published_final=scores[leg-1]if leg==1 else scores[leg-1][::-1],aggregate=scores[2]if leg==1 else scores[2][::-1])
  if 'aet'not in r['source_fields']['raw_line'].lower():expected['after_extra_time']=None
  require(expected==fix['after'],'Repaired periods differ from raw columns');r['periods']=expected;r['source_leg']=leg
 for r in repairs['additional_observations']:
  require(r['observation_id']not in rows,'Repeated recovered observation');parent=rows[r['derived_from_observation']];tokens=re.findall(r'(?<!\d)\*?\d+-\d+[a-z*]?',parent['source_fields']['raw_line']);score=list(map(int,re.search(r'(\d+)-(\d+)',tokens[1]).groups()))[::-1]
  require(r['source_sha256']==parent['source_sha256']and r['raw_home']==parent['raw_away']and r['raw_away']==parent['raw_home'],'Recovered participants differ');require(r['periods']['published_final']==score and r['source_leg']==2,'Recovered return score/leg differs');require(r['observation_id']==digest(wire([r['source_sha256'],r['locator']])),'Recovered ID differs');rows[r['observation_id']]=copy.deepcopy(r)
 occurrence=load(PHASE/'observation_decisions.json')['decisions'];require([r['observation']for r in occurrence]==[r['observation']for r in repairs['occurrence_repairs']],'Occurrence corrections omitted')
 for rule in occurrence:
  r=rows[rule['observation']];require(r['source_sha256']==rule['source_sha256']and r['locator']==rule['locator'],'Occurrence binding');require(bool(rule['rationale'])and bool(rule['evidence']),'Unsupported occurrence correction')
  for k,v in rule['changes'].items():r[k]=copy.deepcopy(v)
 inventory=load(directory/'adjudicated_inventory.json');events=inventory['events'];cases=load(directory/'review_dispositions.json')['cases'];summary=load(directory/'numerical_reconciliation.json');cross=load(directory/'event_crosswalk.json');by={e['event_id']:e for e in events};require(len(by)==len(events),'Duplicate event ID')
 membership=Counter(o for e in events for o in e['observations']);require(set(membership)==set(rows)and set(membership.values())=={1},'Observation lost or repeated')
 require(len(original)==38126 and len(old_events)==12311 and len(oldcases)==1896,'Accepted baseline differs')
 require({c['original_case_id']for c in cases}=={c['case_id']for c in oldcases}and len(cases)==1896,'Original case missing/duplicated')
 case_index={c['original_case_id']:c for c in cases}
 for c in oldcases:
  v=case_index[c['case_id']];require(v['original_issues']==c['issues']and v['original_priority']==c['priority'],'Case identifiers/issues/priority changed');require({r['issue']for r in v['issue_results']}==set(c['issues']),'Issue dropped')
  require((v['resolution']=='RESOLVED')==all(i['resolved']for i in v['issue_results']),'Reviewed incorrectly counted resolved');require(bool(v['investigation_method'])and bool(v['resulting_decisions']or v['original_source_exception']or v.get('directed_coverage_evidence')),'Case without findings/evidence')
 old_member={o:e['event_id']for e in old_events for o in e['observations']};forward=defaultdict(set);edge=0;new=0
 for e in events:
  expected=sorted({old_member[o]for o in e['observations']if o in old_member});require(expected==e['previous_conditional_event_ids'],'Incorrect old-event lineage');edge+=len(expected);new+=not expected
  for oid in expected:forward[oid].add(e['event_id'])
  require(e['event_id']==digest(wire(['UEL_PHASE3',sorted(e['observations'])])),'Unstable event ID')
 require(set(forward)=={e['event_id']for e in old_events},'Old event disappeared')
 splits=sum(len(v)-1 for v in forward.values());merges=sum(max(0,len(e['previous_conditional_event_ids'])-1)for e in events)
 require(12311+splits-merges+new==len(events),'Numerical bridge fails');require(summary['split_increments']==splits and summary['merge_decrements']==merges and summary['new_fixture_events']==new,'Bridge metrics differ')
 require(cross['previous_to_adjudicated']=={k:sorted(v)for k,v in forward.items()},'Crosswalk differs')
 manual=load(PHASE/'historical_decisions.json')['decisions'];rule_by_obs=defaultdict(list)
 for rule in manual:
  require(rule['observation']in rows and rows[rule['observation']]['source_sha256']==rule['source_sha256'],'Historical rule binding');require(rule['evidence']and rule['rationale'],'Empty historical decision');rule_by_obs[rule['observation']].append(rule)
 methods=Counter();venue_checked=0;explicit_manual=0;corrections_checked=0
 assigned={}
 for e in events:
  require(e['disposition']in ('INCLUDE','HOLD OUT','NOT PLAYED','OUT OF SCOPE'),'Invalid disposition');require(e['status']in ('PLAYED_SOURCE_SUPPORTED','PLAYED_ADMINISTRATIVE_EXCEPTION','ABANDONED_INCOMPLETE','NOT PLAYED','ADMINISTRATIVE_ONLY','OUT OF SCOPE'),'Invalid historical status')
  evidence={x['observation']:x for x in e['source_evidence']};require(set(evidence)==set(e['observations']),'Missing original provenance')
  for oid,x in evidence.items():
   r=rows[oid];require((x['source'],x['sha256'],x['locator'])==(r['source'],r['source_sha256'],r['locator']),'Provenance differs');require(set(x['identity_candidates'])==set(e['team_identities']),'Participant projection differs');assigned[oid]=x['identity_candidates']
  def projection(value,oid):return value if value is None or evidence[oid]['identity_candidates']==e['team_identities']else value[::-1]
  def label_key(text):
   import unicodedata
   text=''.join(c for c in unicodedata.normalize('NFKD',text.casefold())if not unicodedata.combining(c));words=re.findall('[a-z0-9]+',text)
   while len(words)>1 and words[0]in('fc','fk','sc','sk','cf','ac','rsc','rc','cd','nk'):words.pop(0)
   return ' '.join(words)
  for oid in e['observations']:
   r=rows[oid]
   for side in('home','away'):
    key='reconciled_'+side+'_label'
    if key in r:
     normalized=label_key(r[key]);partners=[other for other in e['observations']if other!=oid and any(label_key(rows[other]['raw_'+s])==normalized for s in('home','away'))]
     require(partners,'Corrected participant has no other preserved description in the adjudicated fixture')
  rr=[rows[o]for o in e['observations']];score=e['score'];value=score['regulation_time'];method=score['method'];methods[method]+=1
  if value is not None:
   require(len(value)==2 and all(type(g)is int and g>=0 for g in value),'Invalid exact goals');expected_outcome='X'if value[0]==value[1]else'1'if value[0]>value[1]else'2';require(score['regulation_outcome']==expected_outcome,'Outcome differs from90minute goals')
  if method=='COMPLETE_EXPLICIT_GOAL_CHRONOLOGY':
   reconstructed={tuple(projection(v,r['observation_id']))for r in rr if(v:=timed(r))is not None};require(reconstructed=={tuple(value)},'Timed goal reconstruction differs')
  elif method=='EXPLICIT_REGULATION_COMPONENT':
   supported=[projection(r['periods']['regulation_time'],r['observation_id'])for r in rr if('/openfootball/'in r['source']or(r['publisher']=='11footy'and r['source_fields'].get('home_goals_regular_time','')!=''))and r['periods']['regulation_time']is not None];require(value in supported,'Explicit90minute component differs')
  elif method=='PRE_2021_AWAY_GOALS_ET_EQUALITY_WITH_IDENTIFIED_FIRST_LEG':
   require(int(e['season'][:4])<=2020,'Post-abolition away-goals inference');proof=score['evidence'][0];first=rows[proof['observation']];require(first['periods']['published_final']==value,'Return-leg goals wrongly reversed');first_event=next(z for z in events if first['observation_id']in z['observations']);require(first_event['season']==e['season']and set(first_event['team_identities'])==set(e['team_identities'])and first_event['event_id']!=e['event_id'],'First leg from different tie');require(assigned.get(first['observation_id'],next(x['identity_candidates']for x in first_event['source_evidence']if x['observation']==first['observation_id']))==e['team_identities'][::-1],'First leg orientation not opposite')
   finals=[projection(r['periods']['after_extra_time']or r['periods']['published_final'],r['observation_id'])for r in rr if r['periods']['after_extra_time']is not None or(r['periods']['shootout']is not None and r['publisher']in ('RSSSF contributors','Wikipedia contributors'))];require(finals and all(all(a<=b for a,b in zip(value,f))for f in finals),'90minute goals exceed cumulative final')
  elif method=='UNIQUE_SECOND_LEG_FINAL_AGGREGATE_AND_CUMULATIVE_BOUND':
   proof=score['evidence'][0];first=rows[proof['observation']];first_score=first['periods']['published_final'];finals=[projection(r['periods']['after_extra_time']or r['periods']['published_final'],r['observation_id'])for r in rr if r['periods']['after_extra_time']is not None or(r['periods']['shootout']is not None and r['publisher']in('RSSSF contributors','Wikipedia contributors'))];require(e['stage']=='FINAL'and int(e['season'][:4])<=1996 and finals,'Invalid two-leg final inference');limit=[min(f[i]for f in finals)for i in(0,1)];possible=[[hg,ag]for hg in range(limit[0]+1)for ag in range(limit[1]+1)if hg-ag==first_score[0]-first_score[1]];require(possible==[value],'Final aggregate/cumulative bound not unique')
  elif method=='UNIQUE_NONNEGATIVE_SINGLE_MATCH_EXTRA_TIME_BOUND':
   require(value==[0,0]and(e['stage']=='FINAL'or(int(e['season'][:4])==2020 and e['scope']=='QUALIFYING')),'Invalid zero-bound inference')
  elif method=='DIRECTED_HISTORICAL_EVIDENCE':
   expected=[projection(rule['changes']['regulation_time'],r['observation_id'])for r in rr for rule in rule_by_obs[r['observation_id']]if'regulation_time'in rule['changes']];require(value in expected,'Directed regulation rule not applied');explicit_manual+=1
  elif method in ('TARGET_ARCHIVE_EXPLICIT_ORDINARY_MATCH_SCORE','SOURCE_REPORTED_ORDINARY_DURATION'):
   candidates=[projection(r['periods']['published_final']if method.startswith('TARGET')else r['periods']['regulation_time'],r['observation_id'])for r in rr if(method=='SOURCE_REPORTED_ORDINARY_DURATION'or r['publisher']in ('RSSSF contributors','Wikipedia contributors'))];require(value in candidates,'Ordinary match score lacks source support');require(not any(r['periods']['after_extra_time']is not None or r['periods']['shootout']is not None or r['source_fields'].get('full_time')in('E','P')for r in rr),'ET/shootout admitted as ordinary regulation')
  else:require(value is None,'Unknown score decision method')
  half=score.get('half_time');half_manual=[projection(rule['changes']['half_time'],r['observation_id'])for r in rr for rule in rule_by_obs[r['observation_id']]if'half_time'in rule['changes']]
  if half is not None:
   half_chron={tuple(projection(v,r['observation_id']))for r in rr if(v:=timed(r,45))is not None}
   half_source={tuple(projection(r['periods']['half_time'],r['observation_id']))for r in rr if r['periods']['half_time']is not None}
   require(half in half_manual or half_chron=={tuple(half)}or(not half_chron and half_source=={tuple(half)}),'Unsupported halftime decision')
  duration=e['duration'];require(duration['regulation_completed']in(True,False,None),'Invalid regulation completion metadata')
  for r in rr:
   for rule in rule_by_obs[r['observation_id']]:
    for key,v in rule['changes'].get('duration',{}).items():require(duration.get(key)==v,'Directed duration decision differs')
  if duration.get('abandonment_period')=='EXTRA_TIME':require(duration['regulation_completed']is True and duration['extra_time_completed']is False and duration['after_extra_time_score']is None and value is not None,'Extra-time abandonment lost completed regulation or fabricated completed ET')
  complete=e['status']in ('PLAYED_SOURCE_SUPPORTED','PLAYED_ADMINISTRATIVE_EXCEPTION')and e['identity_confidence']!='UNRESOLVED'and duration['regulation_completed']is True;eligible=e['modelling_eligibility'];require(eligible['outcome']==(complete and score['regulation_outcome']is not None),'Incorrect outcome eligibility');require(eligible['goals']==(complete and value is not None),'Incorrect goal eligibility');require(eligible['chronological']==(eligible['outcome']and e['date']['date']is not None),'Incorrect chronological eligibility');require(eligible['venue_dependent']==(eligible['outcome']and e['venue']['neutral_venue']==0),'Incorrect venue-dependent eligibility')
  if e['status']in ('NOT PLAYED','ADMINISTRATIVE_ONLY'):require(value is None and e['date']['date']is None,'No-kickoff event has playing score/date')
  if e['status']=='ABANDONED_INCOMPLETE':require(value is None and not eligible['outcome']and not eligible['goals'],'Incomplete score entered modelling')
  if e['status']=='PLAYED_ADMINISTRATIVE_EXCEPTION':require(e['administrative_evidence']and value is not None,'Played award lacks observed90minute decision')
  require((e['disposition']=='INCLUDE')==eligible['outcome'],'Disposition/eligibility mismatch')
  dates={r.get('_source_date',r['date'])for r in rr if r.get('_source_date',r['date'])};require(dates<=set(e['date']['original_dates']),'Original date uncertainty discarded')
  manual_dates=[rule['changes']['date']for r in rr for rule in rule_by_obs[r['observation_id']]if'date'in rule['changes']]
  if e['date']['date']is not None:require(e['date']['date']in {r['date']for r in rr}|set(manual_dates),'Unsupported selected date')
  require(e['venue']['neutral_venue']in (0,1,None),'Venue not tri-state');manual_venues=[rule['changes']['neutral_venue']for r in rr for rule in rule_by_obs[r['observation_id']]if'neutral_venue'in rule['changes']]
  if manual_venues:require(e['venue']['neutral_venue']in manual_venues,'Directed venue decision differs')
  elif e['stage']=='FINAL':require(e['venue']['neutral_venue']==(1 if int(e['season'][:4])>=1997 else 0),'Final-format neutrality differs')
  elif e['season']=='2019/2020'and e['stage']in('QUARTERFINAL','SEMIFINAL'):require(e['venue']['neutral_venue']==1,'COVID central tournament not neutral')
  venue_checked+=1
  if any(o in {d['observation']for d in occurrence}for o in e['observations']):corrections_checked+=1
 countries=defaultdict(set);names=defaultdict(set)
 country_alias={'ita':'italy','aze':'azerbaijan','fin':'finland','cyp':'cyprus','gre':'greece','grk':'greece','cze':'czech','czech-republic':'czech','blr':'belarus','bls':'belarus'}
 for oid,ids in assigned.items():
  r=rows[oid]
  for i,cid in enumerate(ids):
   country=str(r['associations'][i]or'').casefold();countries[(r['season'],cid)].add(country_alias.get(country,country));names[(r['season'],cid)].add(r.get('reconciled_'+('home'if i==0 else'away')+'_label',r['raw_home'if i==0 else'raw_away']).casefold())
 for key,countryset in countries.items():
  joined=' '.join(names[key])
  if'aek'in joined:require(not{'greece','cyprus'}<=countryset,'Greek/Cypriot AEK identities merged')
  if'slavia'in joined:require(not{'czech','belarus'}<=countryset,'Czech/Belarus Slavia identities merged')
  if'inter'in joined:require(not('italy'in countryset and countryset&{'azerbaijan','finland'}),'Italian/Azeri/Finnish Inter identities merged')
 require(summary['original_observations']+summary['new_observations']==len(rows),'Observation bridge differs');require(summary['adjudicated_events']==len(events),'Event summary differs');require(summary['review_resolutions']==dict(Counter(c['resolution']for c in cases)),'Case totals differ')
 require(summary['dispositions']==dict(Counter(e['disposition']for e in events)),'Disposition summary differs')
 for key in ('outcome','goals','chronological','venue_dependent'):require(summary['eligibility'][key]==sum(e['modelling_eligibility'][key]for e in events),'Eligibility summary differs')
 coverage=load(directory/'season_coverage.json')['seasons'];csvrows=list(csv.DictReader(io.StringIO(read(directory/'season_coverage.csv').decode())));require(len(coverage)==len(csvrows)==36,'Season coverage missing')
 for c,line in zip(coverage,csvrows):
  year=int(c['season'][:4]);slots=126 if year<=1996 else 125 if year<=1998 else 205 if year<=2003 else 221 if year<=2008 else 197 if year==2019 else 205 if year<=2020 else 141 if year<=2023 else 189
  expected=slots-{2001:1,2004:1,2006:2,2020:1,2021:2}.get(year,0)
  ev=[e for e in events if e['season']==c['season']];require(c['historical_events']==len(ev)and int(line['historical_events'])==len(ev),'Season event total differs');require(c['goal_eligible']==sum(e['modelling_eligibility']['goals']for e in ev),'Season eligibility differs');actual_main=sum(e['scope']=='MAIN'and e['status']in('PLAYED_SOURCE_SUPPORTED','PLAYED_ADMINISTRATIVE_EXCEPTION','ABANDONED_INCOMPLETE')for e in ev);require(actual_main==expected==c['expected_main_kickoffs_format_and_documented_exceptions'],'Main kickoff total differs');require(c['main_kickoff_difference']==0 and c['qualifying_kickoff_difference']==0,'Coverage gap unresolved')
 for season in ('2024/2025','2025/2026'):
  phase=[e for e in events if e['season']==season and e['stage']=='LEAGUE_PHASE'];apps=Counter(cid for e in phase for cid in e['team_identities']);homes=Counter(e['team_identities'][0]for e in phase);aways=Counter(e['team_identities'][1]for e in phase);require(len(phase)==144 and len(apps)==36 and set(apps.values())=={8}and set(homes.values())==set(aways.values())=={4},'Recent league phase damaged')
 qualifying=independent_qualifying_counts(events)
 require(len(qualifying)==33 and all(c['difference']==0 for c in qualifying),'Independent raw qualifying bracket differs')
 fixed_counts={c['season']:c for c in load(PHASE/'qualifying_count_evidence.json')['seasons']}
 for c in qualifying:require(c['expected_qualifying_kickoffs']==fixed_counts[c['season']]['expected_qualifying_kickoffs'],'Frozen qualifying evidence differs')
 for season in ('2024/2025','2025/2026'):
  path=fixed_counts[season]['evidence_source'];text=read(BASE/path).decode();count=sum(bool(re.search(r'\sv\s',line))for line in text.splitlines());actual=sum(e['scope']=='QUALIFYING'and e['status']in('PLAYED_SOURCE_SUPPORTED','PLAYED_ADMINISTRATIVE_EXCEPTION','ABANDONED_INCOMPLETE')for e in events if e['season']==season);require(count==actual==fixed_counts[season]['expected_qualifying_kickoffs'],'Recent raw qualifying TXT count differs');qualifying.append(dict(season=season,expected_qualifying_kickoffs=count,adjudicated_qualifying_kickoffs=actual,difference=0,evidence='Independent raw TXT line count'))
 actual=sum(e['scope']=='QUALIFYING'and e['status']in('PLAYED_SOURCE_SUPPORTED','PLAYED_ADMINISTRATIVE_EXCEPTION','ABANDONED_INCOMPLETE')for e in events if e['season']=='2023/2024');require(actual==34,'2023/24 official7+10two-leg ties differs');qualifying.append(dict(season='2023/2024',expected_qualifying_kickoffs=34,adjudicated_qualifying_kickoffs=actual,difference=0,evidence='Directed official access-structure note; not a frozen primary fixture payload'))
 for year in range(1990,1994):
  season=f'{year}/{year+1}';first=[e for e in events if e['season']==season and e['stage']=='ROUND_1'];apps=Counter(cid for e in first for cid in e['team_identities']);require(len(first)==64 and len(apps)==64 and set(apps.values())=={2},'Early64club bracket damaged');require(not any(e['scope']=='QUALIFYING'for e in events if e['season']==season),'Invented early qualifying')
 contexts=load(directory/'historical_contexts.json');require({x['original_exception']['exception_id']for x in contexts['original_contexts']}=={x['exception_id']for x in src['exceptions']},'Original non-event context lost')
 newcases=load(directory/'new_review_cases.json')['cases'];require(len({c['case_id']for c in newcases})==len(newcases)==summary['new_review_cases'],'New case accounting differs')
 # Explicit anti-contamination and replay checks over the complete result.
 for e in events:
  require(e['replay']==any(rows[o]['replay']for o in e['observations']),'Replay marker lost or invented')
 return dict(status='PASS',original_payloads_verified=len(freeze['source_inputs']['inputs']),original_observations=len(original),additional_observations=len(rows)-len(original),adjudicated_records=len(events),original_cases_checked=len(cases),independent_qualifying_counts=sorted(qualifying,key=lambda c:c['season']),new_cases_checked=len(newcases),all_regulation_methods_checked=dict(methods),directed_regulation_decisions_checked=explicit_manual,venue_records_checked=venue_checked,corrected_occurrence_events_checked=corrections_checked,all_memberships_crosswalks_and_eligibility_checked=True,independent_method='Original-byte hash checks; independent raw-score-column and timed-goal reconstruction; rule bindings, pre-2021 first-leg equality, original dates, tri-state venue, event/case/eligibility/coverage accounting. No production adjudication helpers imported.',limitations=['Factual research notes are not frozen full-text publisher payloads','Upstream publisher independence is not certified','Historical identity meaning and directed evidence require the documented research; code validates bound decisions, not an independent human opinion','Absent private domestic/UCL archives are not certified'],network_requests=0)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--inventory',type=Path,default=PHASE/'final');p.add_argument('--output',type=Path,default=PHASE/'independent_validation.json');p.add_argument('--check',action='store_true');a=p.parse_args();out=a.output.resolve();require(out.is_relative_to(PHASE.resolve())or out.is_relative_to(Path('/private/tmp')),'Private verification output only');result=verify(a.inventory)
 if a.check:require(read(out)==wire(result),'Independent verification receipt differs')
 else:
  with out.open('xb')as f:f.write(wire(result))
 print(json.dumps(result,indent=2))
