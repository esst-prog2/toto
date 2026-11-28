"""Offline Phase 2 observation/event inventory, preserving all original evidence.

Conditional structural correspondence is not historical acceptance. No production
schema, match IDs, model input or final historical dispositions are generated.
"""
import argparse
from collections import Counter, defaultdict
from datetime import date
import gzip
import json
import mmap
from pathlib import Path
import re
import tempfile
from scripts import uefa_europa_league_sources as adapter
from scripts import acquire_uefa_europa_league as acquisition
from scripts.artifact_io import check_overwrite, serialize_csv

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'data/private/europe/europa_league'
PHASE=BASE/'phase2'
OUTPUT=PHASE/'validated'
sha,encode=adapter.sha,adapter.encode



def read_bytes(path):
    """Read exact immutable bytes without the cloud-backed buffered-read stall."""
    with path.open('rb') as stream:
        if path.stat().st_size==0:return b''
        with mmap.mmap(stream.fileno(),0,access=mmap.ACCESS_READ) as mapped:return mapped[:]


def verify_item(item,directory):
    raw=read_bytes(directory/item['path']);receipt=json.loads(read_bytes(directory/(item['path']+'.provenance.json')))
    if any(receipt.get(k)!=v for k,v in item.items()) or receipt['sha256']!=sha(raw) or receipt['bytes']!=len(raw) or receipt['status']!=200 or not receipt.get('retrieved_at_utc'):
        raise ValueError('Source item/receipt binding differs')
    if not item.get('official_release_redirect') and receipt['final_url']!=item['url']:raise ValueError('Source URL binding differs')
    acquisition.validate(item,directory);acquisition.check_content(item,raw)
    if item.get('permission_reference'):
        notice=directory/item['permission_reference'];permission=json.loads(read_bytes(notice.with_name(notice.name+'.provenance.json')))
        if sha(read_bytes(notice))!=item['permission_sha256'] or permission['sha256']!=item['permission_sha256']:raise ValueError('Permission binding differs')
    return receipt

def inputs():
    phase1=BASE/'phase1';accepted=json.loads(read_bytes(phase1/'verification.json'))
    for name,digest in accepted['private_deliverables'].items():
        if sha(read_bytes(phase1/name))!=digest:raise ValueError('Accepted Phase 1 artifact changed: '+name)
    manifest=json.loads(read_bytes(phase1/'acquisition_manifest.json'))
    if len(manifest)!=75 or sum(r['bytes'] for r in manifest)!=44222060:raise ValueError('Accepted population changed')
    plan={x['path']:x for x in json.loads(read_bytes(phase1/'source_plan.json'))['items']}
    allinputs=[]
    for r in manifest:
        p=phase1/r['path']
        if sha(read_bytes(p))!=r['sha256'] or sha(read_bytes(p.with_name(p.name+'.provenance.json')))!=r['receipt_sha256']:raise ValueError('Accepted original or receipt changed')
        if r['path'] in plan:verify_item(plan[r['path']],phase1)
        item=dict(plan.get(r['path'],{}));item.update(r);item['path']='phase1/'+r['path'];allinputs.append(item)
    supp=PHASE/'supplemental'
    if (supp/'source_plan.json').exists():
        for item in json.loads(read_bytes(supp/'source_plan.json'))['items']:
            r=verify_item(item,supp);r=dict(r);r['path']='phase2/supplemental/'+r['path'];allinputs.append(r)
    return sorted(allinputs,key=lambda r:r['path'])


def raw_inventory():
    observations=[];exceptions=[];accounting=[];records=inputs()
    ordered=sorted([r for r in records if r.get('kind')=='fixture'],key=lambda r:('det.html' in r['path'],r['path']))
    for rec in ordered:
        raw=read_bytes(BASE/rec['path'])
        if '/openfootball/' in rec['path']:fn=adapter.parse_openfootball
        elif rec['path'].endswith('.zip'):fn=adapter.parse_eleven
        elif rec['path'].endswith('.parquet'):fn=adapter.parse_schoch
        elif 'goals_time' in rec['path']:fn=adapter.parse_goals
        elif '/wikipedia/' in rec['path']:fn=adapter.parse_wikipedia
        elif 'det.html' in rec['path']:
            known=[r[side] for r in observations if r['season']==rec['season'] for side in ('home','away')]
            fn=lambda raw,rec:adapter.parse_rsssf_detail(raw,rec,known)
        else:fn=adapter.parse_rsssf_summary
        rows,issues,ledger=fn(raw,rec);observations.extend(rows);exceptions.extend(issues);accounting.append(dict(source=rec['path'],source_sha256=rec['sha256'],**ledger))
    ids=[r['observation_id'] for r in observations]
    if len(ids)!=len(set(ids)):raise ValueError('Duplicate observation locator')
    return observations,exceptions,accounting,records


def namespace(row,side):return (row['season'],row['publisher'],row[side])


class Union:
    def __init__(self):self.parents={}
    def root(self,x):
        self.parents.setdefault(x,x)
        while self.parents[x]!=x:
            self.parents[x]=self.parents[self.parents[x]];x=self.parents[x]
        return x
    def join(self,a,b):
        a,b=self.root(a),self.root(b)
        if a==b:return
        lo,hi=sorted([a,b]);self.parents[hi]=lo


def fix_season_candidates(rows):
    declared=defaultdict(list)
    for r in rows:
        if r['date'] and not r['source'].endswith('.parquet'):declared[r['date']].append(r)
    changes=[]
    for r in rows:
        if not r['source'].endswith('.parquet') or not r['date']:continue
        keys=set(r['team_candidates']);candidates=[p for p in declared[r['date']] if keys & set(p['team_candidates'])]
        exact=[p for p in candidates if set(p['team_candidates'])==keys]
        seasons={p['season'] for p in exact or candidates}
        if len(seasons)==1 and r['season'] not in seasons:
            before=r['season'];r['season']=next(iter(seasons));y=int(r['season'][:4]);r['competition']='UEFA Cup' if y<2009 else 'UEFA Europa League'
            changes.append(dict(observation=r['observation_id'],before=before,after=r['season'],method='DECLARED_SOURCE_SAME_DAY_PARTICIPANT_CORRESPONDENCE',evidence=sorted(p['observation_id'] for p in exact or candidates)))
    return changes


def identities(rows):
    u=Union();labels=defaultdict(set);sample={};proofs=[];byid={r['observation_id']:r for r in rows}
    for r in rows:
        for side in ('home','away'):
            ns=namespace(r,side);key=adapter.team_key(r[side]);node=(r['season'],key)
            sample[ns]=node;labels[node].add((r['publisher'],r[side]));u.root(node)
    provider_nodes=defaultdict(lambda:defaultdict(set))
    for r in rows:
        if r['publisher']=='11footy':
            for side in ('home','away'):provider_nodes[r['season']][sample[namespace(r,side)]].add(r['source_fields'][side+'_team_id'])
    # Date + one known opponent establishes a candidate other participant.
    # Accept nontrivial aliases only with at least two distinct fixture proofs;
    # scores never establish an alias on their own.
    buckets=defaultdict(list)
    for r in rows:
        if r['date']:buckets[(r['season'],r['date'])].append(r)
    for iteration in range(8):
        proposals=defaultdict(dict)
        for (season,day),group in buckets.items():
            for i,a in enumerate(group):
                for b in group[i+1:]:
                    if a['source']==b['source']:continue
                    aa=[u.root(sample[namespace(a,s)]) for s in ('home','away')];bb=[u.root(sample[namespace(b,s)]) for s in ('home','away')]
                    for orient in (0,1):
                        bs=bb if not orient else bb[::-1]
                        if (aa[0]==bs[0])+(aa[1]==bs[1])!=1:continue
                        side=1 if aa[0]==bs[0] else 0
                        x,z=aa[side],bs[side]
                        key=tuple(sorted((x,z)))
                        proposals[key][(day,aa[1-side])]=[a['observation_id'],b['observation_id']]
        # Paired-leg topology with a known opponent and separate corroborating
        # score observations supports old undated summary-name candidates.
        dated=defaultdict(list)
        for r in rows:
            if r['date']:
                for side,other in (('home','away'),('away','home')):
                    dated[(r['season'],u.root(sample[namespace(r,other)]),side)].append(r)
        for r in rows:
            if r['date'] or not r['source_leg'] or not r['periods']['published_final']:continue
            for side,other in (('home','away'),('away','home')):
                candidates=dated[(r['season'],u.root(sample[namespace(r,other)]),side)]
                # Scores are auxiliary to season, oriented known opponent and
                # a distinct leg; period disagreement simply prevents inference.
                candidates=[p for p in candidates if p['source']!=r['source'] and p['periods']['published_final']==r['periods']['published_final']]
                roots={u.root(sample[namespace(p,side)]) for p in candidates}
                if len(roots)==1:
                    x=u.root(sample[namespace(r,side)]);z=next(iter(roots))
                    if x!=z:
                        p=sorted(candidates,key=lambda p:p['observation_id'])[0]
                        proposals[tuple(sorted((x,z)))][('leg'+str(r['source_leg']),u.root(sample[namespace(r,other)]))]=[r['observation_id'],p['observation_id']]
        generic={'club','united','city','real','athletic','dinamo','dynamo','sporting','sport','olympic','inter','cska','rapid'}
        def core_supported(k,evidence):
            x,z=k;a=set(x[1].split());b=set(z[1].split())
            return bool((a&b)-generic) and (a<=b or b<=a) and any(not str(signature[0]).startswith('leg') for signature in evidence)
        def distinct_dates(evidence):
            return {byid[a]['date'] or byid[b]['date'] for a,b in evidence.values() if byid[a]['date'] or byid[b]['date']}
        eligible={k:v for k,v in proposals.items() if len(distinct_dates(v))>=2 or core_supported(k,v)}
        neighbors=defaultdict(set)
        for x,z in eligible:neighbors[x].add(z);neighbors[z].add(x)
        additions=0
        for (x,z),evidence in sorted(eligible.items()):
            # A label mapping to several alternative identities stays unresolved.
            # Several labels can name the same club; graph degree alone is
            # not ambiguity. Reject a component only when it would merge two
            # distinct 11footy provider team IDs in the same season.
            roots={u.root(x),u.root(z)}
            provider_ids=set()
            for node,ids in provider_nodes[x[0]].items():
                if u.root(node) in roots:provider_ids.update(ids)
            if len(provider_ids)>1:continue
            if u.root(x)==u.root(z):continue
            u.join(x,z);additions+=1
            multi=len(distinct_dates(evidence))>=2
            selected=sorted(evidence.values()) if multi else [min(pair for pair in evidence.values() if byid[pair[0]]['date'] and byid[pair[1]]['date'])]
            proofs.append(dict(left=list(x),right=list(z),method='MULTI_FIXTURE_OPPONENT_DATE_OR_TWO_LEG_TOPOLOGY' if multi else 'SINGLE_FIXTURE_DATE_OPPONENT_AND_CORE_NAME',status='STRONGLY_SUPPORTED_CONDITIONAL_IDENTITY',evidence=selected,additional_representation_evidence=[pair for pair in sorted(evidence.values()) if pair not in selected],iteration=iteration))
        if not additions:break
    pending={};root_publishers=defaultdict(set)
    for ns,node in sample.items():root_publishers[u.root(node)].add(ns[1])
    for (x,z),evidence in proposals.items():
        left,right=u.root(x),u.root(z)
        if left==right:continue
        left,right=sorted((left,right));cid=sha(encode([left,right]))
        pending[cid]=dict(candidate_id=cid,season=left[0],left=list(left),right=list(right),evidence=sorted(evidence.values()),status='UNRESOLVED_INSUFFICIENT_OR_CONFLICTING_IDENTITY_EVIDENCE')
    inventory=[];mapping={}
    for ns,node in sorted(sample.items()):
        root=u.root(node);key=sha(encode(root));mapping[ns]=key
        inventory.append(dict(season=ns[0],publisher=ns[1],original_label=ns[2],lexical_key=node[1],identity_candidate=key,identity_root=list(root),status='STRONGLY_SUPPORTED_CANDIDATE' if node!=root else 'SOURCE_LABEL_OR_LEXICAL_CANDIDATE',method='SEASON_BOUND_LEXICAL_PLUS_DOCUMENTED_GRAPH_CORRESPONDENCE',cross_source_status='UNMATCHED' if len(root_publishers[root])==1 else 'CONDITIONAL_MATCH',unresolved_identity_candidates=[record for record in pending.values() if list(root) in (record['left'],record['right'])]))
    return mapping,inventory,proofs


def days_apart(a,b):return abs((date.fromisoformat(a)-date.fromisoformat(b)).days)


def reconcile(rows,mapping):
    byid={r['observation_id']:r for r in rows};groups=defaultdict(list)
    for r in rows:
        r['identity_candidates']=[mapping[namespace(r,s)] for s in ('home','away')]
        groups[(r['season'],tuple(sorted(r['identity_candidates'])))].append(r)
    events=[];links=[];duplicates=[]
    def compatible(a,b):
        # Same source already describes two dates: preserve possible rematches.
        if a['replay']!=b['replay']:return False
        if a['stage'] not in ('UNKNOWN','QUALIFYING_ROUND_UNKNOWN') and b['stage'] not in ('UNKNOWN','QUALIFYING_ROUND_UNKNOWN') and a['stage']!=b['stage']:return False
        return True
    for (season,pairkeys),group in sorted(groups.items()):
        clusters=[];dated=[r for r in group if r['date']];undated=[r for r in group if not r['date']]
        for r in sorted(dated,key=lambda r:(r['date'],r['source'],r['locator'])):
            choices=[]
            for j,cluster in enumerate(clusters):
                same=[p for p in cluster if p['date']==r['date'] and p['replay']==r['replay']]
                if same:choices.append(j)
            if len(choices)==1:clusters[choices[0]].append(r)
            else:clusters.append([r])
        # Conflicting dates are conditionally linked only for a unique directed
        # pair/stage, without putting two different same-source dated fixtures in
        # one event. Distinct rematches/replays are retained.
        changed=True
        while changed:
            changed=False
            for i,c in enumerate(clusters):
                for j in range(i+1,len(clusters)):
                    d=clusters[j]
                    if not any(p['identity_candidates']==q['identity_candidates'] and compatible(p,q) and p['date'] and q['date'] and days_apart(p['date'],q['date'])<=7 for p in c for q in d):continue
                    if {p['source'] for p in c}&{q['source'] for q in d}:continue
                    # More than two dates indicates unresolved chronology.
                    if len({p['date'] for p in c+d if p['date']})>2:continue
                    competitors=[k for k,z in enumerate(clusters) if k not in (i,j) and any(p['identity_candidates']==q['identity_candidates'] and compatible(p,q) and p['date'] and q['date'] and days_apart(p['date'],q['date'])<=7 for p in c+d for q in z)]
                    if competitors:continue
                    clusters[i]+=clusters.pop(j);changed=True;break
                if changed:break
        for r in sorted(undated,key=lambda r:(r['source'],r['locator'])):
            candidates=[]
            for j,cluster in enumerate(clusters):
                oriented=[p for p in cluster if p['identity_candidates']==r['identity_candidates'] and (compatible(p,r) or p['stage']=='UNKNOWN')]
                if not oriented:continue
                if r['source_leg'] and any(p['source_leg'] for p in oriented) and not any(p['source_leg']==r['source_leg'] for p in oriented):continue
                if r['date_interval'] and any(p['date'] for p in oriented):
                    near=[p for p in oriented if p['date'] and min(days_apart(p['date'],v) for v in r['date_interval'])<=14]
                    if not near:continue
                candidates.append(j)
            if not candidates:
                # A unique oriented match in the whole season is still a
                # conditional counterpart when its stage/leg/schedule conflicts.
                # Repeated pairings prevent this fallback; evidence is retained.
                fallback=[j for j,c in enumerate(clusters) if any(p['date'] and p['identity_candidates']==r['identity_candidates'] and p['replay']==r['replay'] for p in c)]
                if len(fallback)==1:
                    candidates=fallback;r['issues']=sorted(set(r['issues']+['CONDITIONAL_UNIQUE_PAIR_STAGE_LEG_SCHEDULE_CONFLICT']))
            if len(candidates)==1:clusters[candidates[0]].append(r)
            else:
                if len(candidates)>1:duplicates.append(dict(observation=r['observation_id'],candidate_member_sets=[sorted(p['observation_id'] for p in clusters[j]) for j in candidates],reason='MULTIPLE_PLAUSIBLE_MATCHES'))
                clusters.append([r])
        for cluster in clusters:
            members=sorted(r['observation_id'] for r in cluster);eid=sha(encode(members));scopes=sorted({r['scope'] for r in cluster if r['scope']!='UNKNOWN'});stages=sorted({r['stage'] for r in cluster if r['stage'] not in ('UNKNOWN','QUALIFYING_ROUND_UNKNOWN')});dates=sorted({r['date'] for r in cluster if r['date']});pubs=sorted({r['publisher'] for r in cluster});anchor=min(cluster,key=lambda r:(r['date'] is None,r['stage']=='UNKNOWN',r['source'],r['locator']));orientation=anchor['identity_candidates'];flags=[]
            if len(dates)>1:flags.append('DATE_CONFLICT')
            if any('CONDITIONAL_UNIQUE_PAIR_STAGE_LEG_SCHEDULE_CONFLICT' in r['issues'] for r in cluster):flags.append('SOURCE_LEG_OR_SCHEDULE_CONFLICT')
            if len(stages)>1 or len(scopes)>1:flags.append('STAGE_CONFLICT')
            if not stages:flags.append('STAGE_UNRESOLVED')
            if not dates:flags.append('DATE_UNRESOLVED')
            if any(r['identity_candidates']!=orientation for r in cluster):flags.append('SOURCE_ORIENTATION_CONFLICT')
            compared={}
            for period in adapter.PERIODS:
                values=defaultdict(list)
                for r in cluster:
                    v=r['periods'][period]
                    if v is not None:values[tuple(v if r['identity_candidates']==orientation else v[::-1])].append(r['observation_id'])
                compared[period]=[dict(value=list(v),observations=sorted(ids)) for v,ids in sorted(values.items())]
                if len(values)>1 and period not in ('published_final','aggregate'):flags.append('SCORE_CONFLICT_'+period.upper())
            extra_claims=sorted(r['observation_id'] for r in cluster if r['periods']['after_extra_time'] is not None)
            ordinary_claims=sorted(r['observation_id'] for r in cluster if r['source_fields'].get('full_time')=='F' or (r['source_fields'].get('extra_time_played')=='0' and r['status']=='played' and not r['source_fields'].get('shootout_home_goals')))
            if extra_claims and ordinary_claims:
                flags.extend(['DURATION_CONFLICT','REGULATION_SCORE_UNRESOLVED'])
            if not compared['regulation_time']:flags.append('REGULATION_SCORE_UNRESOLVED')
            if any('EXCEPTIONAL_STATUS' in r['issues'] or re.search(r'award|abandon|walkover|withdraw|w/o|void|cancel|UEFA decision',str(r['source_fields'].get('raw_line',''))+' '+str(r['source_fields'].get('header',''))+' '+str(r['source_fields'].get('status_annotation','')),re.I) for r in cluster):flags.append('EXCEPTIONAL_STATUS')
            if any(r['official_neutral_candidate']==1 or str(r.get('source_neutral_venue'))=='1' or re.search('neutral|relocat|in [A-Z].*stadium',str(r.get('venue') or ''),re.I) for r in cluster):flags.append('VENUE_REVIEW')
            if len(cluster)==1:flags.append('SINGLE_SOURCE_OBSERVATION')
            event=dict(event_id=eid,season=season,competition=anchor['competition'],observations=members,publishers=pubs,identity_candidates=orientation,date_candidates=dates,date_intervals=[dict(observation=r['observation_id'],interval=r['date_interval']) for r in cluster if r['date_interval']],scope=scopes[0] if len(scopes)==1 else 'UNKNOWN',stage=stages[0] if len(stages)==1 else 'UNKNOWN',stage_candidates=stages,score_evidence=compared,duration_evidence=dict(after_extra_time_claims=extra_claims,ordinary_duration_claims=ordinary_claims),regulation_resolution='UNRESOLVED_DURATION_CONFLICT' if extra_claims and ordinary_claims else 'UNAVAILABLE' if not compared['regulation_time'] else 'SOURCE_SUPPORTED_CANDIDATE_NOT_ADJUDICATED',flags=sorted(set(flags)),resolution='CONDITIONAL_NOT_HISTORICALLY_ADJUDICATED',reconciliation_method='SEASON_TEAM_PAIR_EXACT_DATE_OR_UNIQUE_DIRECTED_STAGE_LEG_CORRESPONDENCE',dispositions_assigned=False)
            events.append(event)
            for r in cluster:
                if r['observation_id']!=anchor['observation_id']:links.append(dict(event_id=eid,observation=r['observation_id'],anchor=anchor['observation_id'],orientation='SAME' if r['identity_candidates']==orientation else 'REVERSED',date_equal=r['date']==anchor['date'],method='CONDITIONAL_STRUCTURAL_CORRESPONDENCE'))
    return sorted(events,key=lambda r:(r['season'],r['event_id'])),links,duplicates


def format_inventory(rows,events,accounting):
    output=[]
    for year in range(1990,2026):
        season=adapter.season_of(year);selected=[r for r in rows if r['season']==season];ev=[e for e in events if e['season']==season]
        if year<=1996:expected=126;formula='64-team main knockout, all ties including final two legs: 2*(32+16+8+4+2+1)'
        elif year<=1998:expected=125;formula='64-team main knockout; single final: 64+32+16+8+4+1'
        elif year<=2003:expected=205;formula='96 first-round clubs; Champions League transfers before third round: 96+48+32+16+8+4+1'
        elif year<=2008:expected=221;formula='80 first-round matches + 8 five-team single-round-robin groups (80) + 61 knockouts'
        elif year==2019:expected=197;formula='COVID main competition: 144+32+14+4+2+1; verify two round-of-16 single-leg ties'
        elif year<=2020:expected=205;formula='12 four-team double-round-robin groups (144) + 61 knockouts'
        elif year<=2023:expected=141;formula='8 four-team double-round-robin groups (96) + 16 knockout play-off + 29 knockouts; 2021/22 includes two unplayed slots'
        else:expected=189;formula='36*8/2 league games + 16 knockout play-off + 29 knockouts'
        refs=sorted({r['source'] for r in selected if '/rsssf/' in r['source'] or '/wikipedia/' in r['source']}|{a['source'] for a in accounting if a.get('title','').startswith(str(year))})
        group_format=({'groups':8,'clubs_per_group':5,'meetings_per_pair':1} if 2004<=year<=2008 else {'groups':12,'clubs_per_group':4,'meetings_per_pair':2} if 2009<=year<=2020 else {'groups':8,'clubs_per_group':4,'meetings_per_pair':2} if 2021<=year<=2023 else None)
        league_format={'clubs':36,'opponents':8,'home':4,'away':4,'top_eight_bye_to_round_of_16':True,'places_9_to_24_knockout_playoff':True} if year>=2024 else None
        output.append(dict(season=season,competition='UEFA Cup' if year<2009 else 'UEFA Europa League',qualifying_applicable=year>=1994,qualifying_evidence='Acquired target-specific first round contains 32 two-leg ties and no earlier stage' if year<1994 else 'Explicit target qualifying/preliminary headings',evidence_sources=refs,final_format='TWO_LEGGED_HOME_AWAY' if year<=1996 else 'SINGLE_MATCH_FORMAT_NEUTRAL_CANDIDATE',stages=dict(Counter(r['stage'] for r in selected)),raw_stage_labels=dict(Counter(r['raw_stage'] for r in selected)),expected_main_format_slots=expected,expected_main_formula=formula,expected_status='FORMAT_DIAGNOSTIC_NOT_VERIFIED_PLAYED_TOTAL',qualifying_expected_total=None,main_group_format=group_format,league_phase_format=league_format,ordinary_knockout_legs=2,qualifying_leg_format='SINGLE_LEG_COVID_EXCEPTION_ALL_ROUNDS' if year==2020 else 'TWO_LEG_EXCEPT_SOURCE_DOCUMENTED_EXCEPTIONS',covid_knockout_exceptions='Two individually source-annotated single-leg round-of-16 ties; single-leg quarterfinals/semifinals' if year==2019 else None,entry_mechanisms='Domestic qualification under season-specific association/cup rules; incoming eliminated clubs only where source bracket documents them; no fixtures from their former competition',incoming_cl_main_group_transfers='Eight clubs in the documented main bracket' if 1999<=year<=2023 else 'Not a league-phase drop mechanism' if year>=2024 else 'Unestablished; do not assume modern rules',byes_and_withdrawals_evidence='See target-section source-accounting context_items, original notes and explicit no-play tie records',replays_evidence=[r['observation_id'] for r in selected if r['replay']],parsed_observations=len(selected),conditional_events=len(ev),main_events=sum(e['scope']=='MAIN' for e in ev),qualifying_events=sum(e['scope']=='QUALIFYING' for e in ev),unknown_scope_events=sum(e['scope']=='UNKNOWN' for e in ev),single_publisher_events=sum(len(e['publishers'])==1 for e in ev),multi_publisher_events=sum(len(e['publishers'])>1 for e in ev),exact_date_events=sum(bool(e['date_candidates']) for e in ev),date_conflict_events=sum('DATE_CONFLICT' in e['flags'] for e in ev),regulation_supported_events=sum(bool(e['score_evidence']['regulation_time']) for e in ev),score_period_unknown_events=sum('REGULATION_SCORE_UNRESOLVED' in e['flags'] for e in ev),duration_conflict_events=sum('DURATION_CONFLICT'in e['flags'] for e in ev),exceptional_events=sum('EXCEPTIONAL_STATUS' in e['flags'] for e in ev),orientation_conflicts=sum('SOURCE_ORIENTATION_CONFLICT' in e['flags'] for e in ev),source_observations=dict(Counter(r['publisher'] for r in selected))))
    return output


def review_queue(events,exceptions,duplicates,rows):
    queue=[]
    material={'DATE_CONFLICT','DATE_UNRESOLVED','STAGE_CONFLICT','STAGE_UNRESOLVED','SOURCE_ORIENTATION_CONFLICT','REGULATION_SCORE_UNRESOLVED','EXCEPTIONAL_STATUS','VENUE_REVIEW','SOURCE_LEG_OR_SCHEDULE_CONFLICT','DURATION_CONFLICT'}
    for e in events:
        codes=[f for f in e['flags'] if f in material or f.startswith('SCORE_CONFLICT_')]
        if not codes:continue
        priority=1 if any(f.startswith('SCORE_CONFLICT') or f in ('EXCEPTIONAL_STATUS','DATE_CONFLICT','SOURCE_ORIENTATION_CONFLICT','DURATION_CONFLICT') for f in codes) else 2 if any(f in ('REGULATION_SCORE_UNRESOLVED','DATE_UNRESOLVED','STAGE_UNRESOLVED','STAGE_CONFLICT') for f in codes) else 3
        queue.append(dict(case_id=sha(encode([e['event_id'],sorted(codes)])),season=e['season'],event_id=e['event_id'],observations=e['observations'],issues=codes,priority=priority,competing_interpretations=dict(duration_claims=e['duration_evidence'],dates=e['date_candidates'],stages=e['stage_candidates'],score_evidence=e['score_evidence']),materiality='Fixture chronology/identity, regulation 1/X/2 eligibility or official-format neutrality; no INCLUDE/HOLD_OUT decision assigned',investigation='Inspect linked original locators and period/status annotations; corroborate targeted historical evidence; preserve unresolved values',additional_sources='Existing RSSSF detail/Wikipedia revisions first; permitted club/contemporary reports if needed'))
    for x in exceptions:
        if x['code'] in ('OTHER_COMPETITION_DETAIL_PAGE','UNSUPPORTED_RSSSF_SCORE_CONTEXT','UNSUPPORTED_DETAIL_SCORED_CONTEXT'):continue
        queue.append(dict(case_id=x['exception_id'],season=x.get('season'),event_id=None,observations=[],issues=[x['code']],priority=1 if 'NONPLAYED' in x['code'] or x['code']=='HISTORICAL_SCORE_CONTEXT' else 2,source_exception=x,materiality='Source candidate not silently included; inspect participant/status boundary',investigation='Resolve original source context before any later historical decision'))
    for x in duplicates:queue.append(dict(case_id=sha(encode(x)),season=next(r['season'] for r in rows if r['observation_id']==x['observation']),event_id=None,observations=[x['observation']],issues=['AMBIGUOUS_DUPLICATE_CANDIDATE'],priority=1,evidence=x,materiality='Conditional event count may overstate unique fixtures',investigation='Compare dates, stage, leg, source identity and replay context'))
    return sorted(queue,key=lambda q:(q['priority'],q.get('season') or '',q['case_id']))



def tie_gaps(events,observations=()):
    byid={r['observation_id']:r for r in observations}
    groups=defaultdict(list)
    for e in events:
        y=int(e['season'][:4]);st=e['stage']
        if st in ('UNKNOWN','GROUP_STAGE','LEAGUE_PHASE'):continue
        if st=='FINAL' and y>=1997:continue
        if y==2019 and st in ('QUARTERFINAL','SEMIFINAL'):continue
        if y==2020 and e['scope']=='QUALIFYING':continue
        groups[(e['season'],st,tuple(sorted(e['identity_candidates'])))].append(e)
    result=[]
    for (season,stage,pair),group in sorted(groups.items()):
        if season=='2019/2020' and stage=='ROUND_OF_16' and any(re.search(r'over one leg|single.leg|one.off',str(byid.get(oid,{}).get('source_fields',{}).get('status_annotation','')),re.I) for e in group for oid in e['observations']):continue
        if len(group)==2 and len({tuple(e['identity_candidates']) for e in group})==2:continue
        result.append(dict(candidate_id=sha(encode([season,stage,pair])),season=season,stage=stage,identity_candidates=list(pair),events=[e['event_id'] for e in group],conditional_observed_slots=len(group),format_expected_legs=2,classification='MISSING_RETURN_OBSERVATION_OR_UNRESOLVED_IDENTITY' if len(group)<2 else 'DUPLICATE_REPLAY_OR_STAGE_IDENTITY_CANDIDATE',historically_verified_missing=False,investigation='Inspect linked participant/date/leg evidence before claiming a missing fixture; byes, awards and historical exceptions remain possible'))
    return result

def build(cache=None):
    if cache:
        cached=json.loads(read_bytes(Path(cache)));rows,exceptions,accounting=cached['observations'],cached['exceptions'],cached['accounting'];records=inputs()
    else:rows,exceptions,accounting,records=raw_inventory()
    changes=fix_season_candidates(rows);mapping,names,proofs=identities(rows);events,links,duplicates=reconcile(rows,mapping);coverage=format_inventory(rows,events,accounting);queue=review_queue(events,exceptions,duplicates,rows)
    # Gap candidates are diagnostics, never fabricated event rows.
    gaps=[]
    for c in coverage:
        if c['main_events']!=c['expected_main_format_slots'] or c['unknown_scope_events']:
            gaps.append(dict(season=c['season'],code='MAIN_FORMAT_COUNT_OR_UNCLASSIFIED_EVENTS',expected_format_slots=c['expected_main_format_slots'],conditional_main=c['main_events'],unknown_scope=c['unknown_scope_events'],classification='UNRESOLVED_SOURCE_GAP_VS_DUPLICATES_OR_STAGE_IDENTITY',evidence=c['evidence_sources'],action='Reconcile stage/name/date candidates before claiming missing played fixtures'))
    pending={record['candidate_id']:record for label in names for record in label['unresolved_identity_candidates']}
    for record in pending.values():
        queue.append(dict(case_id=record['candidate_id'],season=record['season'],event_id=None,observations=sorted({oid for pair in record['evidence'] for oid in pair}),issues=['UNRESOLVED_TEAM_IDENTITY_CANDIDATE'],priority=1,evidence=record,competing_interpretations=[record['left'][1],record['right'][1]],materiality='Club identity and duplicate/coverage accounting; no global club merge assigned',investigation='Inspect historical names, provider IDs, association and matched opponent/date evidence; do not merge by city or scores alone'))
    topology=tie_gaps(events,rows)
    for gap in topology:
        queue.append(dict(case_id=gap['candidate_id'],season=gap['season'],event_id=None,observations=sorted({oid for e in events if e['event_id'] in gap['events'] for oid in e['observations']}),issues=['TIE_TOPOLOGY_COVERAGE_CANDIDATE'],priority=2,evidence=gap,materiality='Completeness or unresolved duplicate/club/stage identity; not an invented missing match',investigation=gap['investigation']))
    summary=dict(phase=2,status='CANDIDATE',seasons=36,fixture_payloads=len(accounting),source_publishers=len({r['publisher'] for r in rows}),observations=len(rows),conditional_events=len(events),main_events=sum(e['scope']=='MAIN' for e in events),qualifying_events=sum(e['scope']=='QUALIFYING' for e in events),unknown_scope_events=sum(e['scope']=='UNKNOWN' for e in events),single_publisher_events=sum(len(e['publishers'])==1 for e in events),multi_publisher_events=sum(len(e['publishers'])>1 for e in events),source_exceptions=len(exceptions),tie_topology_candidates=len(topology),duplicate_candidates=len(duplicates),identity_correspondences=len(proofs),unresolved_identity_candidates=len(pending),review_cases=len(queue),review_issue_counts=dict(Counter(code for q in queue for code in q['issues'])),canonical_records_generated=0,dispositions_assigned=False,upstream_independence='NOT_ESTABLISHED')
    return {'source_inventory.json':dict(observations=sorted(rows,key=lambda r:(r['source'],r['locator'])),source_accounting=accounting,exceptions=exceptions),'event_inventory.json':dict(events=events),'team_identity_inventory.json':dict(labels=names,nontrivial_correspondences=proofs,unresolved_candidates=list(pending.values()),source_season_reassignments=changes),'structural_validation.json':dict(season_coverage=coverage,missing_fixture_candidates=gaps,tie_topology_candidates=topology),'overlap_assessment.json':dict(links=links,ambiguous_duplicate_candidates=duplicates),'review_queue.json':dict(cases=sorted(queue,key=lambda q:(q['priority'],q.get('season') or '',q['case_id']))),'score_semantics_exceptions.json':dict(unresolved_event_ids=[e['event_id'] for e in events if 'REGULATION_SCORE_UNRESOLVED' in e['flags']],conflict_event_ids=[e['event_id'] for e in events if any(f.startswith('SCORE_CONFLICT') for f in e['flags'])],unresolved_observation_ids=[r['observation_id'] for r in rows if r['periods']['regulation_time'] is None],published_score_disagreement_event_ids=[e['event_id'] for e in events if len(e['score_evidence']['published_final'])>1],aggregate_disagreement_event_ids=[e['event_id'] for e in events if len(e['score_evidence']['aggregate'])>1],basis='Published-score differences can reflect unlike periods; do not classify them automatically as regulation conflicts. Full source-period evidence remains in source_inventory and event_inventory; unavailable periods are not inferred'),'date_exceptions.json':dict(conflicting_event_ids=[e['event_id'] for e in events if 'DATE_CONFLICT' in e['flags']],undated_event_ids=[e['event_id'] for e in events if not e['date_candidates']],interval_observations=[dict(observation=r['observation_id'],interval=r['date_interval'],raw_date=r['raw_date']) for r in rows if r['date_interval']],season_reassignments=changes),'summary.json':summary,'input_freeze.json':dict(phase1_manifest_sha256=sha(read_bytes(BASE/'phase1/acquisition_manifest.json')),inputs=[dict(path=r['path'],sha256=r['sha256'],bytes=r['bytes'],url=r['url'],kind=r.get('kind','metadata')) for r in records])}



def coverage_csv(artifacts):
    observations=artifacts['source_inventory.json']['observations'];events=artifacts['event_inventory.json']['events'];queue=artifacts['review_queue.json']['cases'];labels=artifacts['team_identity_inventory.json']['labels'];output=[]
    for c in artifacts['structural_validation.json']['season_coverage']:
        season=c['season'];rows=[r for r in observations if r['season']==season];selected=[e for e in events if e['season']==season];cases=[q for q in queue if q.get('season')==season]
        raw_records={(r['source'],r['locator'].split(':leg:')[0]) for r in rows if r['representation']!='goal_event_fixture_context'}
        goals=sum(len(r['source_fields']['goal_rows']) for r in rows if r['representation']=='goal_event_fixture_context')
        record=dict(season=season,competition=c['competition'],applicable_stages=';'.join(sorted(c['stages'])),raw_fixture_related_records_represented=len(raw_records),auxiliary_raw_goal_event_rows=goals,parsed_observations=c['parsed_observations'],conditional_events=c['conditional_events'],main_events=c['main_events'],qualifying_events=c['qualifying_events'],unknown_scope_events=c['unknown_scope_events'],single_publisher_events=c['single_publisher_events'],multi_publisher_events=c['multi_publisher_events'],reconciled_extra_observations=len(rows)-len(selected),duplicate_candidate_cases=sum('AMBIGUOUS_DUPLICATE_CANDIDATE'in q['issues'] for q in cases),identity_candidate_cases=sum('UNRESOLVED_TEAM_IDENTITY_CANDIDATE'in q['issues'] for q in cases),unmatched_cross_source_labels=sum(r['season']==season and r['cross_source_status']=='UNMATCHED' for r in labels),unresolved_stage_events=sum('STAGE_UNRESOLVED'in e['flags'] or 'STAGE_CONFLICT'in e['flags'] for e in selected),exact_source_date_events=c['exact_date_events'],date_conflicts=c['date_conflict_events'],undated_events=sum(not e['date_candidates'] for e in selected),source_interval_observations=sum(bool(r['date_interval'])for r in rows),published_score_events=sum(bool(e['score_evidence']['published_final']) for e in selected),regulation_supported_events=c['regulation_supported_events'],regulation_unresolved_events=c['score_period_unknown_events'],duration_conflict_events=c['duration_conflict_events'],regulation_conflict_events=sum('SCORE_CONFLICT_REGULATION_TIME'in e['flags'] for e in selected),result_class_conflict_events=sum(len({(v['value'][0]>v['value'][1])-(v['value'][0]<v['value'][1]) for v in e['score_evidence']['regulation_time']})>1 for e in selected),exceptional_events=c['exceptional_events'],orientation_conflicts=c['orientation_conflicts'],venue_review_events=sum('VENUE_REVIEW'in e['flags'] for e in selected),tie_coverage_candidates=sum('TIE_TOPOLOGY_COVERAGE_CANDIDATE'in q['issues'] for q in cases),expected_main_format_slots=c['expected_main_format_slots'],independently_verified_played_total='UNKNOWN',expected_qualifying_total='UNKNOWN',qualifying_applicable=c['qualifying_applicable'],source_observation_counts=json.dumps(c['source_observations'],sort_keys=True),rights='Private originals/intermediates; source-specific CC0, ODC-By, acknowledgement, CC BY-NC, CC BY-SA; no downstream clearance inferred')
        output.append(record)
    return serialize_csv(output,list(output[0]))

def destination(output):
    resolved=output.resolve()
    if resolved.is_relative_to(ROOT.resolve()) and not resolved.is_relative_to(PHASE.resolve()):raise ValueError('Inventory output must remain private')
    if not any(resolved.is_relative_to(p.resolve()) for p in (PHASE,Path(tempfile.gettempdir()),Path('/private/tmp'))):raise ValueError('Unapproved output root')


def run(output=OUTPUT,check=False,cache=None):
    destination(output);artifacts=build(cache)
    if 'structural_validation.json' in artifacts:artifacts['season_coverage.csv']=coverage_csv(artifacts)
    if not check:check_overwrite([output/name for name in artifacts])
    for name,value in artifacts.items():
        raw=value if isinstance(value,bytes) else encode(value);path=output/name
        if check:
            if read_bytes(path)!=raw:raise ValueError('Deterministic reproduction mismatch: '+name)
        else:acquisition.save(path,raw)
    print(json.dumps(artifacts['summary.json'],indent=2));return artifacts


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=OUTPUT);p.add_argument('--check',action='store_true');p.add_argument('--cache',type=Path,help='Exploratory only; final validation must reparse originals');args=p.parse_args();run(args.output,args.check,args.cache)
