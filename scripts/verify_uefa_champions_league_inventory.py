"""Independent offline UCL Phase 2 reconstruction from original CSV/TXT bytes.

Imports no production acquisition, inventory, stage, period, naming or ID helpers.
Inventory artifacts are comparison targets after reconstructing raw observations.
"""
from collections import Counter, defaultdict
import argparse
import calendar
import csv
from datetime import date, datetime
import hashlib
import io
import json
from pathlib import Path
import re
import tempfile
import unicodedata

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'data/private/europe/champions_league'
PHASE=BASE/'phase2'
INVENTORY=PHASE/'validated'


def digest(raw):return hashlib.sha256(raw).hexdigest()
def wire(value):return (json.dumps(value,sort_keys=True,indent=2,ensure_ascii=False)+'\n').encode()
def read(path):return json.loads(path.read_bytes())
def require(ok,message):
    if not ok:raise ValueError(message)


def private_output(path):
    require(not path.resolve().is_relative_to(ROOT.resolve()) or path.resolve().is_relative_to(PHASE.resolve()),'Independent evidence destination must be private or temporary')
    roots=[PHASE.resolve(),Path(tempfile.gettempdir()).resolve(),Path('/private/tmp').resolve()]
    require(any(path.resolve().is_relative_to(root) for root in roots),'Independent evidence destination must be private or temporary')


def pair(text):
    if not text:return None
    found=re.findall(r'\d+',text)
    return list(map(int,found[:2])) if len(found)>=2 else None


def text_scores(token):
    # Delimit named phases before inspecting numerical pairs. No leading-score shortcut.
    current=token; penalty=None; normal=None; half=None; overtime=None; unassigned=[]
    if ' pen. ' in current:
        shoot,current=current.split(' pen. ',1); penalty=pair(shoot)
    extra=' a.e.t.' in current
    if extra:
        final,remaining=current.split(' a.e.t.',1);overtime=pair(final)
        bracket=re.fullmatch(r'\s*\(([^()]*)\)',remaining)
        parts=[p.strip() for p in bracket[1].split(',')] if bracket else []
        if len(parts)==2:normal,half=map(pair,parts)
        else:unassigned=[pair(p) for p in parts]
    elif penalty:
        unassigned=[pair(current)]
    else:
        head,separator,rest=current.partition(' (');normal=pair(head)
        if separator:half=pair(rest)
    return dict(regulation_time=normal,half_time=half,after_extra_time=overtime,shootout=penalty,
                aggregate=None,extra_time_only=None,unassigned_period_scores=unassigned,
                basis='FOOTBALL_TXT_EXPLICIT_SYNTAX',raw_score_fields={'score_text':token})


def club(text,csv_source):
    if csv_source:
        tokens=text.split(' › ')
        return tokens[0].strip(), tokens[1].split()[0] if len(tokens)==2 else None
    if text.endswith(')') and len(text)>=6 and text[-5]=='(':
        return text[:-5].strip(),text[-4:-1]
    return text.strip(),None


def category(csv_source,qualifier,heading,stage_name,group_name):
    if qualifier or stage_name=='Qualifying' or heading.startswith('Prelim.'):
        if heading.startswith('Prelim.'):value='PRELIMINARY'
        elif 'play' in heading.lower():value='QUALIFYING_PLAYOFF'
        else:
            numbers=re.findall(r'\d+',heading);value='QUALIFYING_ROUND_'+(numbers[0] if numbers else 'UNKNOWN')
        return 'QUALIFYING',value,None
    if stage_name in ('Group','Group 1st','Group 2nd') or heading.startswith(('Group','Gruppe')):
        value='SECOND_GROUP' if stage_name=='Group 2nd' or group_name.startswith('2|') else 'FIRST_GROUP'
        letter=group_name.split('|')[-1] if group_name else (heading.split()[-1] if re.fullmatch(r'(Group|Gruppe) [A-H]',heading) else None)
        return 'MAIN',value,letter
    if heading.startswith('League,'):return 'MAIN','LEAGUE_PHASE',None
    if heading.startswith('Play'):return 'MAIN','KNOCKOUT_PLAYOFF',None
    last=heading.replace('Finals, ','').split(' | ')[0]
    names={'Round of 16':'ROUND_OF_16','Quarterfinals':'QUARTERFINAL','Semifinals':'SEMIFINAL','Final':'FINAL','Round 1':'PRE_GROUP_ROUND_1','Round 2':'PRE_GROUP_ROUND_2'}
    return ('MAIN',names[last],None) if last in names else ('UNKNOWN','UNKNOWN',None)


def raw_inventory(manifest):
    out=[];counts={}; marker_ids=set(); header_checks=[]
    plan=read(BASE/'phase1_research/proposed_acquisition_plan.v2.json');planned={x['url']:x for x in plan['items']}
    require(len(manifest['originals'])==41 and len(planned)==41,'Source population differs')
    for rec in manifest['originals']:
        p=BASE/rec['path'];raw=p.read_bytes();physical=raw.splitlines(keepends=True);csv_source=p.suffix=='.csv';year=int(rec['season'][:4]);qualifier=p.name=='clq.txt';entries=[]
        require(digest(raw)==rec['sha256'] and len(raw)==rec['bytes'],'Original digest/size changed')
        expected=planned[rec['url']]
        require(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==expected['expected_blob'] and len(raw)==expected['expected_bytes'],'Git blob binding failed')
        receipt_path=p.with_name(p.name+'.provenance.json');receipt=read(receipt_path)
        require(digest(receipt_path.read_bytes())==rec['receipt_sha256'] and receipt['sha256']==rec['sha256'] and receipt['status']==200 and receipt['url']==rec['url']==receipt['final_url'],'Receipt binding failed')
        license_file=BASE/rec['permission_reference']
        require(digest(license_file.read_bytes())==rec['permission_sha256'] and license_file.read_text().startswith('CC0 1.0 Universal'),'Permission binding failed')
        if csv_source:
            reader=csv.DictReader(io.StringIO(raw.decode('utf-8-sig'),newline=''),strict=True)
            require(reader.fieldnames==['Stage','Round','Group','Date','Team 1','FT','HT','Team 2','∑FT','ET','P','Comments'],'CSV schema changed')
            while True:
                begin=reader.line_num+1
                try:f=next(reader)
                except StopIteration:break
                require(None not in f and all(x is not None for x in f.values()),'CSV width differs')
                parts=f['Date'].split();d=datetime.strptime(' '.join(parts[1:4]),'%d %b %Y').date();require(calendar.day_abbr[d.weekday()]==parts[0].strip('()'),'Date weekday mismatch')
                periods=dict(regulation_time=pair(f['FT']),half_time=pair(f['HT']),after_extra_time=pair(f['ET']),shootout=pair(f['P']),aggregate=pair(f['∑FT']),extra_time_only=None,unassigned_period_scores=[],basis='EXPLICIT_NAMED_CSV_FIELDS',raw_score_fields={k:f[k] for k in ('FT','HT','ET','P','∑FT')})
                entries.append((begin,reader.line_num,f,f['Team 1'],f['Team 2'],d.isoformat(),f['Stage'],f['Round'],f['Group'],'EXPLICIT_DAY',periods,f['Comments']))
        else:
            current_heading='';current_date=None;precision='';date_lines={};stage_lines={};dl=None;sl=None
            for n,line in enumerate(physical,1):
                s=line.decode('utf-8-sig').strip()
                if not s or s[0] in '#=':continue
                if s[0]=='▪':current_heading=s[1:].strip();current_date=None;sl=n;continue
                if s[:3] in list(calendar.day_abbr) and ' v ' not in s:
                    parts=s.split();years=[int(parts[3])] if len(parts)==4 else [year,year+1];choices=[]
                    for y in years:
                        month=list(calendar.month_abbr).index(parts[1]);d=date(y,month,int(parts[2]))
                        if date(year,6,1)<=d<=date(year+1,8,31) and calendar.day_abbr[d.weekday()]==parts[0]:choices.append(d.isoformat())
                    require(len(choices)==1,'Nonunique raw source date');current_date=choices[0];dl=n;precision='EXPLICIT_HEADING_YEAR' if len(parts)==4 else 'SOURCE_SEASON_WEEKDAY_RESOLVED_YEAR';continue
                home,tail=s.split(' v ',1);home=re.sub(r'^\d{1,2}:\d{2}\s+','',home).strip()
                match=re.search(r'(?<=\))\s+(?=\d+-\d+)',tail);require(match is not None,'Unrecognized fixture separation')
                away=tail[:match.start()].strip();token=tail[match.end():]
                entries.append((n,n,{'raw_line':line.decode('utf-8-sig').rstrip('\r\n')},home,away,current_date,'',current_heading,'',precision,text_scores(token),token))
                date_lines[n]=dl;stage_lines[n]=sl
            header=re.search(r'^# Matches\s+(\d+)',raw.decode('utf-8-sig'),re.M)
            require(header and int(header[1])==len(entries),'Publisher count and independently parsed fixtures differ')
            header_checks.append(rec['path'])
        counts[rec['path']]=len(entries)
        for first,last,fields,h,a,day,st,rnd,g,precision,periods,note in entries:
            hn,ha=club(h,csv_source);an,aa=club(a,csv_source);scope,stage,grp=category(csv_source,qualifier,rnd,st,g)
            oid=digest(wire([rec['sha256'],first,last]));leg=re.findall(r'Leg ([12])',rnd);matchday=re.findall(r'Matchday (\d+)',rnd)
            row=dict(observation_id=oid,source=rec['path'],source_sha256=rec['sha256'],line=first,end_line=last,physical_sha256=digest(b''.join(physical[first-1:last])),publisher=rec['publisher'],season=rec['season'],source_fields=fields,date=day,date_precision=precision,raw_home=h,raw_away=a,home=hn,away=an,home_association=ha,away_association=aa,raw_stage=st,raw_round=rnd,raw_group=g,scope=scope,stage=stage,group=grp,matchday=int(matchday[0]) if matchday else None,source_leg=int(leg[0]) if leg else None,replay='Replay' in rnd,annotation=note,periods=periods)
            row['date_source_line']=first if csv_source else date_lines[first]
            row['stage_source_line']=first if csv_source else stage_lines[first]
            out.append(row)
            if periods['after_extra_time'] is not None:marker_ids.add(oid)
    return out,counts,marker_ids,header_checks


def identity_links(rows):
    mappings=[];links=[]
    for y in range(2011,2016):
        season=f'{y}/{y+1}';left=[r for r in rows if r['season']==season and r['scope']=='MAIN' and r['publisher'].startswith('footballcsv')];right=[r for r in rows if r['season']==season and r['publisher'].startswith('openfootball')]
        evidence=defaultdict(set);labels={r[s] for r in right for s in ('home','away')};mapping={}
        signatures=defaultdict(list)
        for r in left:signatures[(r['date'],r['stage'],tuple(r['periods']['regulation_time']))].append(r)
        for r in right:
            if r['periods']['regulation_time'] is None:continue
            candidates=signatures[(r['date'],r['stage'],tuple(r['periods']['regulation_time']))]
            if len(candidates)==1:
                p=candidates[0]
                for s in ('home','away'):
                    if p[s+'_association']==r[s+'_association']:evidence[(r[s],p[s])].add((p['observation_id'],r['observation_id']))
        for label in labels:
            source_assoc={r[s+'_association'] for r in right for s in ('home','away') if r[s]==label}
            canonical=lambda s:' '.join(unicodedata.normalize('NFC',s).split())
            exact={r[s] for r in left for s in ('home','away') if canonical(r[s])==canonical(label) and r[s+'_association'] in source_assoc}
            candidates=sorted(((len(v),target) for (origin,target),v in evidence.items() if origin==label),reverse=True)
            if len(exact)==1:mapping[label]=exact.pop()
            elif candidates and candidates[0][0]>=2 and (len(candidates)==1 or candidates[0][0]>candidates[1][0]):mapping[label]=candidates[0][1]
        while True:
            additions={}
            for r in right:
                for s,other in [('home','away'),('away','home')]:
                    if r[s] in mapping or r[other] not in mapping:continue
                    candidates=[p for p in left if (p['date'],p['stage'],p[other],p[s+'_association'])==(r['date'],r['stage'],mapping[r[other]],r[s+'_association'])]
                    if len(candidates)==1:
                        p=candidates[0];evidence[(r[s],p[s])].add((p['observation_id'],r['observation_id']))
                        if len(evidence[(r[s],p[s])])>=2:additions[r[s]]=p[s]
            if not additions:break
            mapping.update(additions)
        require(len(mapping)==len(set(mapping.values())),'Seasonal correspondences collide')
        mappings.extend((season,k,v) for k,v in mapping.items())
        for r in right:
            same=[p for p in left if (p['stage'],p['home'],p['away'])==(r['stage'],mapping.get(r['home']),mapping.get(r['away']))]
            reverse=[] if r['stage']!='FINAL' else [p for p in left if (p['stage'],p['away'],p['home'])==(r['stage'],mapping.get(r['home']),mapping.get(r['away']))]
            candidates=same or reverse
            if len(candidates)==1:links.append((candidates[0]['observation_id'],r['observation_id'],'SAME' if same else 'REVERSED_SOURCE_DESIGNATION'))
    return mappings,links


def verify(inventory=INVENTORY):
    manifest=read(PHASE/'acquisition_manifest.json');rows,counts,markers,headers=raw_inventory(manifest);byid={r['observation_id']:r for r in rows}
    require(len(byid)==len(rows),'Duplicate independent raw identities')
    target=read(inventory/'source_inventory.json')['observations'];actual={r['observation_id']:r for r in target}
    require(set(actual)==set(byid),'Source population incomplete')
    for oid,row in byid.items():
        for k,v in row.items():require(actual[oid][k]==v,f'Independent field mismatch {oid}: {k}')
    names,links=identity_links(rows);observed=read(inventory/'overlap_assessment.json')
    require(set(names)=={(r['season'],r['source_label'],r['target_label']) for r in observed['season_bound_names']},'Independent name correspondences differ')
    require(set(links)=={(r['left'],r['right'],r['orientation']) for r in observed['links']},'Independent cross-source correspondences differ')
    for r in observed['links']:
        a,b=byid[r['left']],byid[r['right']];require(r['date_equal']==(a['date']==b['date']),'Date comparison differs')
        for field,value in r['periods_equal'].items():
            x,z=a['periods'][field],b['periods'][field]
            expected=None if x is None or z is None else x==(z if r['orientation']=='SAME' else z[::-1])
            require(value==expected,'Score comparison mixes periods or orientation')
    coverage=read(inventory/'structural_validation.json')['season_coverage'];independent_counts=[];components=[]
    for y,c in zip(range(1992,2026),coverage,strict=True):
        season=f'{y}/{y+1}';selected=[r for r in rows if r['season']==season and r['publisher'].startswith('footballcsv' if y<2016 else 'openfootball')];main=[r for r in selected if r['scope']=='MAIN'];qual=[r for r in selected if r['scope']=='QUALIFYING']
        require(c['season']==season and c['primary_main_records']==len(main) and c['primary_qualifying_records']==len(qual),'Primary coverage differs')
        require(c['main_regulation_known']==sum(r['periods']['regulation_time'] is not None for r in main) and c['qualifying_regulation_known']==sum(r['periods']['regulation_time'] is not None for r in qual),'Period coverage differs')
        # Independent expected main total; a replay is an extra source event, not a format fixture.
        expected=73 if y==1992 else 75 if y==1993 else 61 if y in (1994,1995,1996) else 85 if y in (1997,1998) else 157 if y in range(1999,2003) else 119 if y==2019 else 189 if y>=2024 else 125
        require(len(main)==expected+sum(r['replay'] for r in main),'Main season count fails actual format/replay accounting')
        if y==1992:stage_expect={'PRE_GROUP_ROUND_1':33,'PRE_GROUP_ROUND_2':16,'FIRST_GROUP':24,'FINAL':1}
        elif y==1993:stage_expect={'PRE_GROUP_ROUND_1':32,'PRE_GROUP_ROUND_2':16,'FIRST_GROUP':24,'SEMIFINAL':2,'FINAL':1}
        elif y<=1998:stage_expect={'FIRST_GROUP':48 if y<=1996 else 72,'QUARTERFINAL':8,'SEMIFINAL':4,'FINAL':1}
        elif y<=2002:stage_expect={'FIRST_GROUP':96,'SECOND_GROUP':48,'QUARTERFINAL':8,'SEMIFINAL':4,'FINAL':1}
        elif y<=2023:stage_expect={'FIRST_GROUP':96,'ROUND_OF_16':16,'QUARTERFINAL':4 if y==2019 else 8,'SEMIFINAL':2 if y==2019 else 4,'FINAL':1}
        else:stage_expect={'LEAGUE_PHASE':144,'KNOCKOUT_PLAYOFF':16,'ROUND_OF_16':16,'QUARTERFINAL':8,'SEMIFINAL':4,'FINAL':1}
        require(dict(Counter(r['stage'] for r in main))==stage_expect,'Independent season/stage format mismatch')
        # Reconstruct group components without inventing missing Group A-H labels.
        for group_stage in ('FIRST_GROUP','SECOND_GROUP'):
            group_rows=[r for r in main if r['stage']==group_stage]
            if not group_rows:continue
            graph=defaultdict(set)
            for r in group_rows:graph[r['home']].add(r['away']);graph[r['away']].add(r['home'])
            unseen=set(graph);groups=[]
            while unseen:
                component={next(iter(unseen))};front=list(component)
                while front:
                    for neighbor in graph[front.pop()]-component:component.add(neighbor);front.append(neighbor)
                unseen-=component;matches=[r for r in group_rows if r['home'] in component];pairs={(r['home'],r['away']) for r in matches}
                require(len(component)==4 and len(matches)==12 and len(pairs)==12,'Independent group topology fails')
                groups.append(dict(clubs=sorted(component),observations=sorted(r['observation_id'] for r in matches),source_group_labels=sorted({r['group'] for r in matches if r['group']})))
            components.append(dict(season=season,stage=group_stage,components=sorted(groups,key=lambda g:g['clubs'])))
        league=[r for r in main if r['stage']=='LEAGUE_PHASE']
        if league:
            played=Counter(r[s] for r in league for s in ['home','away']);home=Counter(r['home'] for r in league);away=Counter(r['away'] for r in league)
            require(len(league)==144 and len(played)==36 and set(played.values())=={8} and set(home.values())=={4} and set(away.values())=={4},'Independent league-phase structure fails')
            require(len({tuple(sorted([r['home'],r['away']])) for r in league})==144,'League phase repeats opponents')
        independent_counts.append(dict(season=season,main=len(main),qualifying=len(qual),main_stages=stage_expect,replay_descriptions=sum(r['replay'] for r in main)))
    event_rows=read(inventory/'event_inventory.json')['events'];membership=Counter(oid for event in event_rows for oid in event['observations'])
    require(set(membership)==set(byid) and set(membership.values())=={1},'Event membership loses or duplicates evidence')
    linked_sets={frozenset([a,b]) for a,b,_ in links}
    for e in event_rows:
        members=e['observations'];require(e['event_id']==digest(wire(sorted(members))),'Event locator differs')
        require(len(members)==1 or len(members)==2 and frozenset(members) in linked_sets,'Unsupported event merge')
    summary=read(inventory/'summary.json')
    require(summary['observations']==len(rows) and summary['conditional_events']==len(rows)-len(links),'Population totals differ')
    require(summary['explicit_extra_time_observations']==len(markers),'Period annotation lost in intermediate inventory')
    unknown=[r['observation_id'] for r in rows if r['periods']['regulation_time'] is None]
    issue_rows=read(inventory/'unresolved_issues.json')['observation_issues'];issues={r['observation_id']:r['codes'] for r in issue_rows}
    require(all('REGULATION_SCORE_UNKNOWN' in issues.get(oid,[]) for oid in unknown),'Ambiguity not isolated in issue registry')
    require(not summary['dispositions_assigned'] and summary['canonical_records_generated']==0,'Unauthorized later phase work')
    return dict(status='PASS',originals=41,source_observations=len(rows),conditional_events=len(event_rows),independent_overlap_links=len(links),independent_season_counts=independent_counts,
                raw_fields_dates_names_stages_scores_physical_locators_reconstructed=True,independent_source_parser=True,
                extra_time_observations=len(markers),shootout_observations=sum(r['periods']['shootout'] is not None for r in rows),
                unresolved_regulation_observation_ids=sorted(unknown),txt_publisher_headers_independently_recounted=len(headers),
                independent_group_components=components,source_counts=counts,network_requests=0,
                upstream_independence='NOT_ESTABLISHED',all_source_observations_accounted_once=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--inventory',type=Path,default=INVENTORY);parser.add_argument('--output',type=Path)
    args=parser.parse_args();result=verify(args.inventory)
    if args.output:
        private_output(args.output)
        args.output.parent.mkdir(parents=True,exist_ok=True)
        with args.output.open('xb') as f:f.write(wire(result))
    print(json.dumps({k:v for k,v in result.items() if k not in ('independent_group_components','source_counts','independent_season_counts')},indent=2))
