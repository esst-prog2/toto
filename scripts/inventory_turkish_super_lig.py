"""Offline Phase 2 inventory; source evidence, conditional links, no adjudication."""
from collections import Counter,defaultdict
import csv,io,json,re
from datetime import date,datetime
from html import unescape
from pathlib import Path
from scripts import collect_turkish_super_lig_sources as c
from scripts import recover_turkish_super_lig_sources as recovery
from scripts.validate_segunda_feasibility import fixture

ROOT=c.ROOT;PRIVATE=c.PRIVATE.parent/'phase2'
OUTPUT=PRIVATE/'validated'
NAMES=('source_inventory.json','overlap_assessment.json','season_stage_coverage.json','discrepancy_registry.json','review_queue.json')


def bound(row,rec,physical,start,end=None,cell=None):
    end=end or start
    row.update(source=rec['root_path'],source_sha256=rec['sha256'],line=start,end_line=end,cell=cell,physical_sha256=c.sha(b''.join(physical[start-1:end])))
    row['source_id']=c.sha(c.encode([rec['sha256'],start,end,cell]))
    return row


def observation(year,home,away,hg=None,ag=None,**extra):
    return dict(season=f'{year}/{year+1}',stage='REGULAR_SEASON',stage_basis='SOURCE_OR_DOCUMENTED_REGULAR_SOURCE_SCHEMA',home=home,away=away,hg=hg,ag=ag,date=None,reported_date=None,date_precision='UNKNOWN',round=None,annotation='',quarantined=False,correction=None,**extra)


def parse_csv(raw,rec,registry):
    hist=rec['kind']=='historical_csv';encoding='utf-8-sig' if raw.startswith(b'\xef\xbb\xbf') or hist else 'iso-8859-1'
    physical=raw.splitlines(keepends=True);reader=csv.DictReader(io.StringIO(raw.decode(encoding),newline=''),strict=True)
    required=('Date','Season','home','visitor','hgoal','vgoal','division','tier') if hist else ('Div','Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR')
    if not set(required)<=set(reader.fieldnames or ()) or len(reader.fieldnames)!=len(set(reader.fieldnames)):raise ValueError('CSV schema')
    rules={r['source_line']:r for r in registry['affected_records']};quarpairs={(r['original_fields']['home'],r['original_fields']['visitor']) for r in rules.values() if r['action'].startswith('QUARANTINE')};out=[]
    while True:
        first=reader.line_num+1
        try:z=next(reader)
        except StopIteration:break
        extra=z.pop(None,[])
        if any(v is None for v in z.values()):raise ValueError('CSV truncated row')
        if hist:
            if z['division']!='T1' or z['tier']!='1':raise ValueError('CSV tier/competition')
            y=int(z['Season']);d=date.fromisoformat(z['Date']).isoformat();home,away=z['home'],z['visitor'];hg,ag=z['hgoal'],z['vgoal']
            if z['FT']!=hg+'-'+ag or z['totgoal']!=str(int(hg)+int(ag)) or z['goaldif']!=str(int(hg)-int(ag)):raise ValueError('CSV auxiliary contradiction')
        else:
            if z['Div']!='T1':raise ValueError('CSV competition')
            y=int(rec['season'][:4]);d=datetime.strptime(z['Date'],'%d/%m/%Y').date().isoformat();home,away=z['HomeTeam'],z['AwayTeam'];hg,ag=z['FTHG'],z['FTAG']
        if not all(re.fullmatch(r'0|[1-9]\d*',s) for s in (hg,ag)):raise ValueError('CSV score')
        if z['result' if hist else 'FTR']!=('H' if int(hg)>int(ag) else 'A' if int(hg)<int(ag) else 'D'):raise ValueError('CSV outcome')
        row=observation(y,home,away,hg,ag);row.update(date=d,reported_date=z['Date'],date_precision='EXPLICIT_DAY',original_fields=z,extra_source_columns=extra)
        if extra and any(s.strip() for s in extra):
            if not (len(extra)==8 and extra[0]=='' and extra[1:3]==[home,away] and extra[5:]==['','','Abandoned'] and all(v.isdigit() for v in extra[3:5])):raise ValueError('Unknown CSV annex')
            row['annotation']='SOURCE_ABANDONMENT_ANNEX';row['source_status']='ABANDONMENT_CONTEXT'
        if hist and first in rules:
            rule=rules[first]
            if rule['original_fields']!=z or rule['physical_sha256']!=c.sha(b''.join(physical[first-1:reader.line_num])):raise ValueError('Recovery record binding')
            if rule['action']=='DERIVED_DATE_CORRECTION':row.update(date=rule['derived_date'],correction='FROZEN_PHASE1_DATE')
            else:row.update(date=None,date_precision='QUARANTINED_EXACT_DAY',quarantined=True,candidate_dates=[rule['fd']['date'],rule['rsssf']['date']])
        if not hist and y==2006 and (home,away) in quarpairs:row['quarantined']=True
        row['source_status']=row.get('source_status','SCORED')
        out.append(bound(row,rec,physical,first,reader.line_num))
    return out,[],[]


def parse_txt(raw,rec):
    lines=raw.splitlines(keepends=True);y=int(rec['season'][:4]);out=[];current=None;rnd=None;notes=[];title=False
    for n,p in enumerate(lines,1):
        s=p.decode('utf-8-sig').strip()
        if not s:continue
        if s.startswith('='):
            if title or s!=f'= Turkish Süper Lig {y}/{(y+1)%100:02}':raise ValueError('TXT title')
            title=True;continue
        if s.startswith('#'):notes.append(dict(line=n,text=s));continue
        if s.startswith('▪'):
            m=re.fullmatch(r'▪ (?:Matchday (\d+)|(\d+)\. Round)',s)
            if not m:raise ValueError('TXT stage/round')
            rnd=int(m[1] or m[2]);current=None;continue
        d=recovery.turkish_heading(s,y)
        if d:current=d['date'];continue
        if not title or rnd is None or current is None:raise ValueError('TXT context')
        f=fixture(re.sub(r'^\d{1,2}:\d{2}\s+','',s));row=observation(y,f['home'],f['away'],f['hg'],f['ag'])
        row.update(date=current,reported_date=current,date_precision='HEADING_DAY',round=rnd,annotation=f['annotation'],ht=f['HT'],source_status='AWARDED_ANNOTATION' if f['source_marked_awarded'] else 'SCORED' if f['hg'] is not None else 'UNSCORED')
        out.append(bound(row,rec,lines,n))
    return out,[],notes


def plain(p):return unescape(re.sub(r'<[^>]*>','',p.decode('iso-8859-2'))).strip()


def parse_rsssf(raw,rec):
    lines=raw.splitlines(keepends=True);y=int(rec['season'][:4]);lo,hi=rec['top_span'];out=[];tables=[];notes=[];current=None;context=None;rnd=None;active=False;stage='REGULAR_SEASON';group=None;nominal=None
    if f'<TITLE>Turkey {y}/{(y+1)%100:02}</TITLE>'.encode() not in raw:raise ValueError('RSSSF title')
    gridheads=[];gridcols=None;narrative=False
    for n in range(lo,hi+1):
        s=plain(lines[n-1])
        if not s:narrative=False;continue
        if s.startswith('NB:'):narrative=True
        if narrative:notes.append(dict(line=n,kind='NARRATIVE_CONTEXT',text=s));continue
        if 'name="1cham"' in lines[n-1].decode('iso-8859-2'):stage='CHAMPIONSHIP_PLAYOFF'
        if 'name="1euro"' in lines[n-1].decode('iso-8859-2'):stage='EUROPE_PLAYOFF'
        if 'name="1toto"' in lines[n-1].decode('iso-8859-2'):stage='SPOR_TOTO_GROUP'
        if s in ('Grup A','Grup B'):group=s[-1]
        if s.startswith('Final [') and y==2011:stage='SPOR_TOTO_FINAL_SCOPE_UNRESOLVED';group=None;active=True;current=f'{y+1}-05-13';rnd='Final';continue
        if s in ('Final Table:','Final Tables:'):active=False
        # Table observations are aggregate evidence, never manufactured fixtures.
        tm=re.match(r'^(\d+|-)\.\s*(.+?)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*-\s*(\d+)\s+(-?\d+)(.*)$',s)
        if tm:
            rank,club,g,w,d,l,gf,ga,pts,note=tm.groups();tables.append(bound(dict(season=rec['season'],stage=stage,group=group,club=club.strip(),games=int(g),won=int(w),drawn=int(d),lost=int(l),gf=int(gf),ga=int(ga),points=int(pts),annotation=note.strip()),rec,lines,n));continue
        oldtable=re.match(r'^\d+\s+(\S+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(-?\d+)',s) if y==1993 else None
        if oldtable:
            club,g,w,d,l,gf,ga,pts,gd=oldtable.groups();tables.append(bound(dict(season=rec['season'],stage=stage,group=group,club=club,games=int(g),won=int(w),drawn=int(d),lost=int(l),gf=int(gf),ga=int(ga),points=int(pts),annotation='SOURCE_GOAL_DIFFERENCE:'+gd),rec,lines,n));continue
        if y==1993 and re.fullmatch(r'(?:[a-z]+\s+){15}[a-z]+',s):
            gridheads.append(s.split())
            if len(gridheads)==3:gridcols=[''.join(t) for t in zip(*gridheads)]
            continue
        gm=re.fullmatch(r'([a-z]+)\s*\|(.+)\|',s) if y==1993 else None
        if gm:
            if gridcols is None:raise ValueError('Grid headers missing')
            cells=gm[2].split('|')
            if len(cells)!=16:raise ValueError('Grid width')
            for i,cell in enumerate(cells):
                if cell=='---':
                    if gm[1]!=gridcols[i]:raise ValueError('Grid diagonal')
                    continue
                m=re.fullmatch(r'(\d+)-(\d+)',cell)
                if not m:raise ValueError('Grid score')
                row=observation(y,gm[1],gridcols[i],m[1],m[2]);row.update(date_precision='UNDATED_RESULT_GRID',source_status='SCORED_UNDATED')
                out.append(bound(row,rec,lines,n,cell=i+1))
            continue
        if y==1992:
            rm=re.fullmatch(r'(\d+)\.\s*Round(?:\s*\(([^)]+)\))?',s)
            if rm:rnd=int(rm[1]);active=True;nominal=rm[2];continue
            if re.fullmatch(r'\([^)]+\)',s):nominal=s[1:-1];continue
            fm=re.fullmatch(r'(.+?)\s+-\s+(.+?)\s*:\s*(\d+)-(\d+)',s)
            if fm:
                if not active or not rnd:raise ValueError('Early fixture lacks round')
                h,aw,hg,ag=fm.groups();row=observation(y,h.strip(),aw.strip(),hg,ag);row.update(round=rnd,date_precision='ROUND_DATE_NOT_CERTIFIED_EXACT_DAY',nominal_date_heading=nominal,source_status='SCORED_DATE_UNCERTIFIED')
                out.append(bound(row,rec,lines,n));continue
        rm=re.fullmatch(r'Round (\d+)(.*)',s)
        if rm:
            rnd=int(rm[1]);active=True;current=None;context=None;s=rm[2].strip()
            if not s or s.startswith('- played'):continue
        dm=re.fullmatch(r'\[([A-Z][a-z]{2}) (\d{1,2})\]',s)
        if dm:
            month=recovery.MONTHS[dm[1]];current=date(y if month>=7 else y+1,month,int(dm[2])).isoformat();context=current;continue
        if s=='[cancelled matches]':current=None;context='CANCELLED_MATCHES_HEADING';continue
        if s.endswith(' bye'):
            notes.append(dict(line=n,kind='BYE_NOT_FIXTURE',text=s));continue
        if not active:
            notes.append(dict(line=n,kind='TABLE_OR_CONTEXT',text=s));continue
        # Only an explicit score token between separated team fields is a fixture.
        fm=re.match(r'^(.+?)\s+(\d+-\d+|awd|abd|n/p)\s+(.+)$',s)
        if not fm:
            notes.append(dict(line=n,kind='NARRATIVE_CONTEXT',text=s));continue
        home,token,tail=fm.groups();parts=re.split(r'\s{2,}|\s+\[',tail,maxsplit=1);away=parts[0].strip();annotation=s[s.find(away)+len(away):].strip();hg=ag=None
        if re.fullmatch(r'\d+-\d+',token):hg,ag=token.split('-')
        if token=='awd':
            award=re.search(r'awarded (\d+)-(\d+)',annotation)
            if award:hg,ag=award.groups()
        row=observation(y,home.strip(),away,hg,ag);row.update(stage=stage,round=rnd,source_token=token,annotation=annotation,date=current,reported_date=current,date_precision='HEADING_DAY' if current else 'NO_EXACT_DAY',source_status={'awd':'AWARDED_DOCUMENTARY','abd':'ABANDONED_DOCUMENTARY','n/p':'NOT_PLAYED_MARKER'}.get(token,'SCORED'),source_context=context)
        if token=='awd' and y==2022:row.update(date=None,date_precision='AWARD_SLOT_NO_VERIFIED_PLAY_DATE')
        out.append(bound(row,rec,lines,n))
    return out,tables,notes


def correspond(anchor,other):
    """Co-eval proof by repeated unique date/score matches, then known opponent."""
    signatures=defaultdict(list)
    for r in anchor:
        if r['date'] and r['hg'] is not None:signatures[r['date'],r['hg'],r['ag']].append(r)
    evidence=defaultdict(lambda:defaultdict(list));mapping={}
    for r in other:
        hits=signatures.get((r['date'],r['hg'],r['ag']),[])
        if len(hits)==1:
            for side in ['home','away']:evidence[r[side]][hits[0][side]].append([r['source_id'],hits[0]['source_id']])
    for name,targets in evidence.items():
        ranked=sorted(targets,key=lambda k:(-len(targets[k]),k))
        if len(targets[ranked[0]])>=2 and (len(ranked)==1 or len(targets[ranked[0]])>len(targets[ranked[1]])):mapping[name]=ranked[0]
    # A one-off spelling can be bound only by exact date/score AND already
    # evidenced opposite participant, with exactly one original counterpart.
    changed=True
    while changed:
        changed=False
        for r in other:
            for side,opp in [('home','away'),('away','home')]:
                if r[side] in mapping or r[opp] not in mapping:continue
                hits=[z for z in anchor if z['date'] and z['date']==r['date'] and (z['hg'],z['ag'])==(r['hg'],r['ag']) and z[opp]==mapping[r[opp]]]
                if len(hits)==1:mapping[r[side]]=hits[0][side];evidence[r[side]][hits[0][side]].append([r['source_id'],hits[0]['source_id']]);changed=True
    for r in other:
        if r['home'] in mapping and r['away'] in mapping and mapping[r['home']]==mapping[r['away']]:raise ValueError('Club identity collapse')
    proofs=[dict(original=name,anchor=target,evidence=evidence[name][target]) for name,target in sorted(mapping.items())]
    return mapping,proofs


def reconcile(rows):
    byseason=defaultdict(lambda:defaultdict(list))
    for r in rows:byseason[r['season']][r['source']].append(r)
    events=[];maps=[]
    for season,sources in sorted(byseason.items()):
        ordered=sorted(sources,key=lambda s:(0 if s.endswith('turkey.csv') else 1 if s.endswith('T1.csv') else 2,s))
        anchors=[];groups={};anchor_pairs=defaultdict(list)
        for index,source in enumerate(ordered):
            source_rows=sources[source];regular=[r for r in source_rows if r['stage']=='REGULAR_SEASON']
            mapping,proof=correspond(anchors,regular) if anchors else ({},[])
            maps.append(dict(season=season,source=source,anchor_source=ordered[0],correspondences=proof,unresolved=sorted({r[k] for r in regular for k in ['home','away']}-set(mapping)) if anchors else []))
            freq=Counter((r['stage'],mapping.get(r['home'],r['home']),mapping.get(r['away'],r['away'])) for r in source_rows)
            for r in source_rows:
                h=mapping.get(r['home'],r['home']);a=mapping.get(r['away'],r['away']);key=(r['stage'],h,a);candidate=[]
                if index and r['stage']=='REGULAR_SEASON' and r['home'] in mapping and r['away'] in mapping:
                    candidate=anchor_pairs[key]
                    if freq[key]>1:candidate=[z for z in candidate if z['date'] and z['date']==r['date']]
                if len(candidate)==1:anchor=candidate[0]['source_id']
                else:anchor=r['source_id']
                groups.setdefault(anchor,[]).append(r)
                if index==0:
                    anchors.append(r);anchor_pairs[key].append(r)
            # Later source-only events remain separate unless a proven anchor
            # exists; no fuzzy date or name joining of orphan fixtures.
        for anchor,members in sorted(groups.items()):
            eventid=c.sha(c.encode(sorted(r['source_id'] for r in members)));dates=sorted({r['date'] for r in members if r['date']});scores=sorted({(r['hg'],r['ag']) for r in members if r['hg'] is not None})
            issues=[];scored_dates={r['date'] for r in members if r['date'] and r['hg'] is not None}
            if len(scored_dates)>1:issues.append('DATE_CONFLICT')
            elif len(dates)>1:issues.append('SCHEDULE_DATE_DIFFERENCE')
            if len(scores)>1:issues.append('SCORE_CONFLICT')
            if any(r['quarantined'] for r in members):issues.append('FROZEN_PHASE1_QUARANTINE')
            events.append(dict(event_id=eventid,season=season,stage=members[0]['stage'],source_ids=sorted(r['source_id'] for r in members),candidate_dates=dates,candidate_scores=[list(s) for s in scores],quarantined=any(k!='SCHEDULE_DATE_DIFFERENCE' for k in issues),issues=issues,link_basis='SOURCE_SEASON_DIRECTED_PAIR_WITH_COEVAL_PROOFS;REPEATED_PAIR_REQUIRES_EXACT_DATE',anchor=anchor))
    return events,maps


def build(directory=PRIVATE):
    config=json.loads((directory/'config.json').read_bytes());registry=json.loads((ROOT/config['recovery_path']).read_bytes())
    if c.sha((ROOT/config['recovery_path']).read_bytes())!=config['recovery_sha256']:raise ValueError('Frozen recovery altered')
    observations=[];aggregates=[];catalogue=[];context=[]
    for rec in config['files']:
        raw=(ROOT/rec['root_path']).read_bytes()
        if c.sha(raw)!=rec['sha256'] or len(raw)!=rec['bytes']:raise ValueError('Original changed')
        physical=raw.splitlines(keepends=True);rows=[];tables=[];notes=[]
        if rec['kind']=='historical_csv':rows,tables,notes=parse_csv(raw,rec,registry)
        elif rec['kind']=='direct_csv':rows,tables,notes=parse_csv(raw,rec,registry)
        elif rec['kind']=='txt':rows,tables,notes=parse_txt(raw,rec)
        elif rec['kind']=='rsssf':rows,tables,notes=parse_rsssf(raw,rec)
        if rec['kind']=='rsssf' and rec['season']=='2006/2007':
            pairs={(x['original_fields']['home'],x['original_fields']['visitor']) for x in registry['affected_records'] if x['action'].startswith('QUARANTINE')}
            # Existing frozen source/season correspondence, never a global alias.
            for row in rows:
                pair=tuple(recovery.COEVAL.get(row[k],row[k]) for k in ['home','away'])
                if pair in pairs:row['quarantined']=True
        observations.extend(rows);aggregates.extend(tables);context.extend(dict(source=rec['root_path'],**n) for n in notes)
        lo,hi=rec.get('top_span',[1,len(physical)]);spans=[]
        for start,end,role in [(1,lo-1,'NON_TARGET_DOCUMENTARY'),(lo,hi,'TARGET_SECTION' if rec['kind']=='rsssf' else rec['kind'].upper()),(hi+1,len(physical),'NON_TARGET_DOCUMENTARY')]:
            if start<=end:spans.append(dict(start=start,end=end,role=role,sha256=c.sha(b''.join(physical[start-1:end]))))
        catalogue.append(dict(**rec,physical_lines=len(physical),sections=spans,fixture_observations=len(rows),aggregate_table_rows=len(tables)))
    # Propagate approved original-to-date metadata without dropping any record.
    ids=[r['source_id'] for r in observations]
    for row in observations:
        year=int(row['season'][:4]);end=date(2020,7,26) if year==2019 else date(year+1,6,30)
        if row['date'] and not date(year,7,1)<=date.fromisoformat(row['date'])<=end:raise ValueError('Uncontained source date outside season')
        if not row['home'] or not row['away'] or row['home']==row['away']:raise ValueError('Invalid source team identity')
        if row['round'] is not None and isinstance(row['round'],int):
            n=config['expected_regular_clubs'][str(year)];maximum=2*(n-1) if n%2==0 else 2*n
            if not 1<=row['round']<=maximum:raise ValueError('Round outside format era')
    if len(ids)!=len(set(ids)):raise ValueError('Duplicate source locator')
    events,mappings=reconcile(observations);byid={r['source_id']:r for r in observations};seen=Counter(s for e in events for s in e['source_ids'])
    if set(seen)!=set(ids) or set(seen.values())!={1}:raise ValueError('Event reconciliation loss/reuse')
    queue=[];discrepancies=[];coverage=[];contexts=[]
    repeated=set()
    batches=defaultdict(list)
    for r in observations:batches[r['source'],r['season'],r['stage'],r['home'],r['away']].append(r)
    for batch in batches.values():
        if len(batch)>1:repeated.update(r['source_id'] for r in batch)
    for e in events:
        reasons=set(e['issues']);members=[byid[s] for s in e['source_ids']]
        for r in members:
            if r['source_id'] in repeated:reasons.add('REPEATED_SOURCE_PAIRING')
            if r['hg'] is None:reasons.add('UNSCORED_OR_INTERRUPTED')
            if r['annotation']:reasons.add('SOURCE_ANNOTATION')
            if not r['date']:reasons.add('DATE_NOT_EXACT')
            if r['hg'] is not None and (int(r['hg'])+int(r['ag'])>=10 or abs(int(r['hg'])-int(r['ag']))>=7):reasons.add('EXTREME_SCORE_RESEARCH')
        if e['stage']!='REGULAR_SEASON':reasons.add('STAGE_SCOPE_RESEARCH')
        if reasons:queue.append(dict(queue_id=e['event_id'],kind='CONDITIONAL_EVENT',season=e['season'],stage=e['stage'],categories=sorted(reasons),source_ids=e['source_ids']))
        if e['issues']:discrepancies.append(e)
    for y in range(1990,2026):
        season=f'{y}/{y+1}';rs=[r for r in observations if r['season']==season];es=[e for e in events if e['season']==season];n=config['expected_regular_clubs'][str(y)];expected=n*(n-1)
        source_stats=[]
        for source in sorted({r['source'] for r in rs}):
            s=[r for r in rs if r['source']==source];reg=[r for r in s if r['stage']=='REGULAR_SEASON'];pairs=Counter((r['home'],r['away']) for r in reg);rounds=defaultdict(list)
            for r in s:
                if r['round'] is not None:rounds[str(r['round'])].append(r)
            names=next((m for m in mappings if m['season']==season and m['source']==source),None)
            mapping={m['original']:m['anchor'] for m in names['correspondences']} if names else {}
            source_stats.append(dict(source=source,observations=len(s),scored=sum(r['hg'] is not None for r in s),exact_dated_scored=sum(r['date'] is not None and r['hg'] is not None for r in s),quarantined=sum(r['quarantined'] for r in s),clubs=len({r[k] for r in reg for k in ['home','away']}),coeval_identities=len({mapping.get(r[k],r[k]) for r in reg for k in ['home','away']}),directed_pairs=len(pairs),repeated_pairs=[dict(home=h,away=a,count=k) for (h,a),k in sorted(pairs.items()) if k>1],rounds={k:dict(observations=len(v),dates=sorted({r['date'] for r in v if r['date']})) for k,v in sorted(rounds.items())},stages=dict(Counter(r['stage'] for r in s))))
        regular=sum(e['stage']=='REGULAR_SEASON' for e in es)
        coverage.append(dict(season=season,expected_regular_clubs=n,nominal_regular_slots=expected,source_observations=len(rs),conditional_events=len(es),regular_conditional_events=regular,stage_events=dict(Counter(e['stage'] for e in es)),exact_date_gap=y<1994,sources=source_stats,aggregate_rows=sum(t['season']==season for t in aggregates)))
        if y<1994 or regular!=expected or y in [2006,2009,2011,2019,2022,2024,2025]:
            contexts.append(dict(queue_id='SEASON:'+season,kind='SEASON_CONTEXT',season=season,categories=['FORMAT_COVERAGE_AND_HISTORICAL_CONTEXT'],nominal_regular_slots=expected,observed_regular_conditional_events=regular,source_ids=[]))
    queue.extend(contexts)
    return dict(zip(NAMES,[c.encode(dict(catalogue=catalogue,observations=observations,aggregate_tables=aggregates,context_lines=context)),c.encode(dict(conditional_events=events,source_season_correspondences=mappings,totals=dict(source_observations=len(observations),conditional_events=len(events),aggregate_rows=len(aggregates),originals=len(catalogue)))),c.encode(dict(coverage=coverage,stage_expectations_2011=dict(REGULAR_SEASON=306,CHAMPIONSHIP_PLAYOFF=12,EUROPE_PLAYOFF=12,SPOR_TOTO_GROUP_A=12,SPOR_TOTO_GROUP_B=12,SPOR_TOTO_FINAL_SCOPE_UNRESOLVED=1),expectation_basis='ConfiguredformatandRSSSFgamesparticipationtables;notfabricatedfixtures')),c.encode(dict(discrepancies=discrepancies,corrections=[r for r in observations if r['correction']],quarantined_observations=[r['source_id'] for r in observations if r['quarantined']],policy='Structuralquarantineonly;noPhase3dispositions')),c.encode(dict(items=sorted(queue,key=lambda x:x['queue_id']),event_items=sum(x['kind']=='CONDITIONAL_EVENT' for x in queue),context_items=len(contexts),purpose='Deduplicatedrisk-basedresearch;dateuncertifiedearlyevidencecanremainagapwithoutmanualresearchoneveryfixture'))]))


def main():
    import argparse,tempfile
    p=argparse.ArgumentParser();p.add_argument('--verify',action='store_true');p.add_argument('--output-dir',type=Path);a=p.parse_args();dest=a.output_dir or OUTPUT
    if not any(dest.resolve().is_relative_to(t.resolve()) for t in [PRIVATE,Path(tempfile.gettempdir()),Path('/private/tmp')]):raise ValueError('Private/temp outputs only')
    artifacts=build()
    artifacts['structural_checks.json']=c.encode(structural_diagnostics(json.loads(artifacts['source_inventory.json']),json.loads(artifacts['overlap_assessment.json'])))
    for name,raw in artifacts.items():
        if a.verify:
            if (dest/name).read_bytes()!=raw:raise ValueError('Reproduction differs:'+name)
        else:c.save(dest/name,raw)
    print('Phase2 inventory '+('verified' if a.verify else 'saved'))


def structural_diagnostics(inventory,overlap):
    """Format checks over the one authoritative inventory, without re-parsing."""
    maps={(m['season'],m['source']):{v['original']:v['anchor'] for v in m['correspondences']} for m in overlap['source_season_correspondences']}
    groups=defaultdict(list)
    for row in inventory['observations']:groups[row['season'],row['source'],row['stage']].append(row)
    results=[]
    for (season,source,stage),rows in sorted(groups.items()):
        mapping=maps.get((season,source),{});names=sorted({mapping.get(r[k],r[k]) for r in rows for k in ('home','away')});pairs=Counter((mapping.get(r['home'],r['home']),mapping.get(r['away'],r['away'])) for r in rows)
        missing=[[h,a] for h in names for a in names if h!=a and (h,a) not in pairs]
        rounds=defaultdict(list)
        for r in rows:
            if r['round'] is not None:rounds[str(r['round'])].append(r)
        wide=[]
        for rnd,rs in sorted(rounds.items()):
            dates=sorted({r['date'] for r in rs if r['date']})
            if dates and (date.fromisoformat(dates[-1])-date.fromisoformat(dates[0])).days>14:wide.append(dict(round=rnd,first=dates[0],last=dates[-1],source_ids=[r['source_id'] for r in rs]))
        signatures=Counter((r['date'],r['home'],r['away'],r['hg'],r['ag'],r['round']) for r in rows)
        participations=Counter(mapping.get(r[k],r[k]) for r in rows for k in ['home','away'])
        results.append(dict(season=season,source=source,stage=stage,coeval_identity_count=len(names),observations=len(rows),distinct_directed_pairs=len(pairs),pairing_gaps_among_observed_identities=missing,pairing_gap_limit='Observedidentitysetonly;notfabricatedfixtures;uncertainrawlabelsremainuncertain',repeated_pairings=[dict(home=h,away=a,count=n) for (h,a),n in sorted(pairs.items()) if n>1],exact_repeated_observation_count=sum(n-1 for n in signatures.values()),club_participations=dict(sorted(participations.items())),round_observation_counts={k:len(v) for k,v in sorted(rounds.items())},wide_rounds=wide,date_first=min((r['date'] for r in rows if r['date']),default=None),date_last=max((r['date'] for r in rows if r['date']),default=None),halftime_exceeds_reported_final=[r['source_id'] for r in rows if r.get('ht') and r['hg'] is not None and any(int(x)>int(y) for x,y in zip(r['ht'].split('-'),[r['hg'],r['ag']]))]))
    quarantined=[e for e in overlap['conditional_events'] if e['quarantined']]
    return dict(source_stage_checks=results,all_structural_quarantine_source_ids=sorted({s for e in quarantined for s in e['source_ids']}),quarantined_event_ids=sorted(e['event_id'] for e in quarantined),definition='Nominalformatandobservedpairingsareseparate;replaydescriptionsandbyesarenotdeduplicatedasordinaryfixtures')


if __name__=='__main__':main()
