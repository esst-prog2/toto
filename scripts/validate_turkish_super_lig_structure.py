"""Independent stdlib-only Phase 2 reconstruction from frozen originals.

No production parser, fixture/date helper, alias resolver or grouping function is
imported. Inventory files are comparison targets after independent reconstruction.
"""
from collections import Counter,defaultdict
from datetime import date,datetime
from html.parser import HTMLParser
from pathlib import Path
import csv,io,json,re,hashlib,calendar,subprocess,tempfile,sys,os
ROOT=Path(__file__).resolve().parents[1];PRIVATE=ROOT/'data/private/turkey/super_lig/phase2'
OUTPUT=PRIVATE/'validated'


def sha(raw):return hashlib.sha256(raw).hexdigest()
def enc(x):return (json.dumps(x,sort_keys=True,indent=2,ensure_ascii=False)+'\n').encode()
def load(p):return json.loads(p.read_bytes())


class Text(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.parts=[]
    def handle_data(self,data):self.parts.append(data)


def text(raw):
    p=Text();p.feed(raw.decode('iso-8859-2'));return ''.join(p.parts).strip()


def record(rec,physical,line,year,home,away,hg=None,ag=None,**more):
    cell=more.pop('cell',None);end=more.pop('end',line)
    r=dict(source=rec['root_path'],source_id=sha(enc([rec['sha256'],line,end,cell])),line=line,end_line=end,cell=cell,physical_sha256=sha(b''.join(physical[line-1:end])),source_sha256=rec['sha256'],season=f'{year}/{year+1}',stage='REGULAR_SEASON',home=home,away=away,hg=hg,ag=ag,date=None,round=None,annotation='',quarantined=False,correction=None)
    r['source_status']='SCORED' if hg is not None else 'UNSCORED'
    r.update(more);return r


def parse_csv(raw,rec,rules):
    historical=rec['kind']=='historical_csv';p=raw.splitlines(keepends=True);reader=csv.reader(io.StringIO(raw.decode('utf-8-sig' if historical or raw.startswith(b'\xef\xbb\xbf') else 'iso-8859-1'),newline=''),strict=True);headers=next(reader);out=[]
    assert len(headers)==len(set(headers))
    qpair={(r['original_fields']['home'],r['original_fields']['visitor']) for r in rules.values() if r['derived_date'] is None}
    while True:
        line=reader.line_num+1
        try:cells=next(reader)
        except StopIteration:break
        assert len(cells)>=len(headers);fields=dict(zip(headers,cells));extras=cells[len(headers):]
        if historical:
            assert len(cells)==12 and fields['division']=='T1' and fields['tier']=='1';year=int(fields['Season']);home,away=fields['home'],fields['visitor'];hg,ag=fields['hgoal'],fields['vgoal'];day=date.fromisoformat(fields['Date']).isoformat()
            assert fields['FT']==hg+'-'+ag and int(fields['totgoal'])==int(hg)+int(ag) and int(fields['goaldif'])==int(hg)-int(ag)
        else:
            assert fields['Div']=='T1';year=int(rec['season'][:4]);home,away=fields['HomeTeam'],fields['AwayTeam'];hg,ag=fields['FTHG'],fields['FTAG'];dd,mm,yyyy=map(int,fields['Date'].split('/'));day=date(yyyy,mm,dd).isoformat()
        assert hg.isdigit() and ag.isdigit();assert fields['result' if historical else 'FTR']==('H' if int(hg)>int(ag) else 'A' if int(hg)<int(ag) else 'D')
        row=record(rec,p,line,year,home,away,hg,ag,end=reader.line_num,date=day,original_fields=fields,extra_source_columns=extras,date_precision='EXPLICIT_DAY')
        if extras and any(extras):
            assert extras==['',home,away,'1','1','','','Abandoned'];row['annotation']='SOURCE_ABANDONMENT_ANNEX';row['source_status']='ABANDONMENT_CONTEXT'
        if historical and line in rules:
            rule=rules[line];assert fields==rule['original_fields'] and row['physical_sha256']==rule['physical_sha256']
            row['date']=rule['derived_date'];row['quarantined']=rule['derived_date'] is None
            if row['quarantined']:row['date_precision']='QUARANTINED_EXACT_DAY'
            if row['date']:row['correction']='FROZEN_PHASE1_DATE'
        if not historical and year==2006 and (home,away) in qpair:row['quarantined']=True
        out.append(row)
    return out,[]


def parse_txt(raw,rec):
    physical=raw.splitlines(keepends=True);year=int(rec['season'][:4]);out=[];day=None;rnd=None
    assert physical[0].decode('utf-8-sig').strip()==f'= Turkish Süper Lig {year}/{(year+1)%100:02}'
    for n,literal in enumerate(physical,1):
        s=literal.decode('utf-8-sig').strip()
        if not s or s.startswith(('#','=')):continue
        if s[0]=='▪':
            found=re.findall(r'\d+',s);assert len(found)==1;rnd=int(found[0]);day=None;continue
        if re.match(r'^(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\b',s):
            parts=s.split();weekday,mon,dd=parts[:3];years=[int(parts[3])] if len(parts)==4 else [year,year+1];possible=[]
            for y in years:
                try:d=datetime.strptime(f'{mon} {dd} {y}','%b %d %Y').date()
                except ValueError:continue
                end=date(2020,7,26) if year==2019 else date(year+1,6,30)
                if date(year,7,1)<=d<=end and calendar.day_abbr[d.weekday()]==weekday:possible.append(d.isoformat())
            assert len(possible)==1;day=possible[0];continue
        assert day and rnd
        body=re.sub(r'^\d\d?:\d\d\s+','',s);sides=re.split(r'\s+v\s+',body);assert len(sides)==2
        home,tail=sides;note=''
        if '[' in tail:tail,note=tail.split('[',1);note='['+note.strip();tail=tail.rstrip()
        score=re.fullmatch(r'(.+?)\s+(\d+)-(\d+)(?:\s+\((\d+)-(\d+)\))?',tail)
        if score:away,hg,ag,hh,ha=score.groups()
        else:away=tail;hg=ag=None;assert not re.search(r'\d\s*-|-\s*\d',tail)
        out.append(record(rec,physical,n,year,home,away,hg,ag,date=day,round=rnd,annotation=note,date_precision='HEADING_DAY',source_status='AWARDED_ANNOTATION' if 'award' in note.lower() else 'SCORED' if hg is not None else 'UNSCORED'))
    return out,[]


def parse_rsssf(raw,rec):
    p=raw.splitlines(keepends=True);year=int(rec['season'][:4]);out=[];tables=[];stage='REGULAR_SEASON';group=None;roundno=None;day=None;active=False;narrative=False;heads=[];cols=None
    assert f'<TITLE>Turkey {year}/{(year+1)%100:02}</TITLE>'.encode() in raw
    for n in range(rec['top_span'][0],rec['top_span'][1]+1):
        literal=p[n-1];s=text(literal)
        if not s:narrative=False;continue
        if s.startswith('NB:'):narrative=True
        if narrative:continue
        for marker,label in [('name="1cham"','CHAMPIONSHIP_PLAYOFF'),('name="1euro"','EUROPE_PLAYOFF'),('name="1toto"','SPOR_TOTO_GROUP')]:
            if marker.encode() in literal:stage=label
        if s in ['Grup A','Grup B']:group=s[-1]
        if s=='Final [May 13]' and year==2011:stage='SPOR_TOTO_FINAL_SCOPE_UNRESOLVED';active=True;day='2012-05-13';roundno='Final';continue
        if s in ['Final Table:','Final Tables:']:active=False
        # Independently decode aggregate table rows; they are not fixtures.
        table=re.fullmatch(r'(?:\d+|-)\.\s*(.+?)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*-\s*(\d+)\s+(-?\d+)(.*)',s)
        if table:
            club,g,w,d,l,gf,ga,pts,tail=table.groups();tables.append(dict(source_id=sha(enc([rec['sha256'],n,n,None])),club=club.strip(),season=rec['season'],stage=stage,group=group,games=int(g),won=int(w),drawn=int(d),lost=int(l),gf=int(gf),ga=int(ga),points=int(pts)));continue
        if year==1993:
            tokens=s.split()
            if len(tokens)==16 and all(re.fullmatch('[a-z]',t) for t in tokens):
                heads.append(tokens)
                if len(heads)==3:cols=[''.join(letters) for letters in zip(*heads)]
                continue
            if '|' in s:
                home,body=s.split('|',1);home=home.strip();cells=body.rstrip('|').split('|');assert cols and len(cells)==16
                for col,value in enumerate(cells):
                    if value=='---':assert home==cols[col];continue
                    h,a=value.split('-');out.append(record(rec,p,n,year,home,cols[col],h,a,cell=col+1,date_precision='UNDATED_RESULT_GRID',source_status='SCORED_UNDATED'))
                continue
            if tokens and tokens[0].isdigit() and len(tokens)>=10:
                _,club,g,w,d,l,gf,ga,pts,gd,*rest=tokens;tables.append(dict(source_id=sha(enc([rec['sha256'],n,n,None])),club=club,season=rec['season'],stage=stage,group=group,games=int(g),won=int(w),drawn=int(d),lost=int(l),gf=int(gf),ga=int(ga),points=int(pts)));continue
        if year==1992:
            if re.match(r'^\d+\.\s*Round',s):roundno=int(s.split('.')[0]);active=True;continue
            if ' : ' in s or re.search(r':\s*\d+-\d+$',s):
                body,score=s.rsplit(':',1);home,away=re.split(r'\s+-\s+',body);hg,ag=score.strip().split('-');out.append(record(rec,p,n,year,home.strip(),away.strip(),hg,ag,round=roundno,date_precision='ROUND_DATE_NOT_CERTIFIED_EXACT_DAY',source_status='SCORED_DATE_UNCERTIFIED'));continue
        if s.startswith('Round '):
            m=re.match(r'Round (\d+)(.*)',s);roundno=int(m[1]);active=True;day=None;s=m[2].strip()
            if s.startswith('- played') or not s:continue
        if s=='[cancelled matches]':day=None;continue
        if re.fullmatch(r'\[[A-Z][a-z]{2} \d{1,2}\]',s):
            mon,dd=s.strip('[]').split();month=datetime.strptime(mon,'%b').month;day=date(year if month>=7 else year+1,month,int(dd)).isoformat();continue
        if not active or s.endswith(' bye'):continue
        candidate=re.fullmatch(r'(.+?)\s+(\d+-\d+|awd|abd|n/p)\s+(.+)',s)
        if not candidate:continue
        home,token,tail=candidate.groups();parts=re.split(r'\s\s+|\s+\[',tail,maxsplit=1);away=parts[0].strip();annotation=s[s.find(away)+len(away):].strip();hg=ag=None
        if '-' in token:hg,ag=token.split('-')
        elif token=='awd':
            result=re.search(r'awarded (\d+)-(\d+)',annotation)
            if result:hg,ag=result.groups()
        out.append(record(rec,p,n,year,home.strip(),away,hg,ag,date=None if year==2022 and token=='awd' else day,round=roundno,stage=stage,annotation=annotation,date_precision='AWARD_SLOT_NO_VERIFIED_PLAY_DATE' if year==2022 and token=='awd' else 'HEADING_DAY' if day else 'NO_EXACT_DAY',source_status={'awd':'AWARDED_DOCUMENTARY','abd':'ABANDONED_DOCUMENTARY','n/p':'NOT_PLAYED_MARKER'}.get(token,'SCORED')))
    return out,tables


def names(primary,secondary):
    # Separate implementation: index unique raw signatures, count label evidence,
    # then resolve rare forms using the independently resolved opposite side.
    buckets=defaultdict(list)
    for r in primary:
        if r['date'] and r['hg'] is not None:buckets[(r['date'],r['hg'],r['ag'])].append(r)
    votes=defaultdict(Counter)
    for r in secondary:
        candidates=buckets.get((r['date'],r['hg'],r['ag']),[])
        if len(candidates)==1:
            for field in ('home','away'):votes[r[field]][candidates[0][field]]+=1
    mapping={}
    for key,counts in votes.items():
        ranked=counts.most_common()
        if ranked[0][1]>=2 and (len(ranked)==1 or ranked[0][1]>ranked[1][1]):mapping[key]=ranked[0][0]
    for _ in range(2*len(votes)+1):
        previous=len(mapping)
        for r in secondary:
            for field,opposite in [('home','away'),('away','home')]:
                if r[field] in mapping or r[opposite] not in mapping:continue
                targets={p[field] for p in buckets.get((r['date'],r['hg'],r['ag']),[]) if p[opposite]==mapping[r[opposite]]}
                if len(targets)==1:mapping[r[field]]=next(iter(targets))
        if len(mapping)==previous:break
    return mapping


def validate(directory=OUTPUT):
    config=load(PRIVATE/'config.json');registry=load(ROOT/config['recovery_path']);assert sha((ROOT/config['recovery_path']).read_bytes())==config['recovery_sha256'];rules={r['source_line']:r for r in registry['affected_records']};rows=[];tables=[];source_counts={}
    for rec in config['files']:
        raw=(ROOT/rec['root_path']).read_bytes();assert sha(raw)==rec['sha256'] and len(raw)==rec['bytes']
        if rec['kind'].endswith('csv'):rs,ts=parse_csv(raw,rec,rules)
        elif rec['kind']=='txt':rs,ts=parse_txt(raw,rec)
        elif rec['kind']=='rsssf':rs,ts=parse_rsssf(raw,rec)
        else:rs,ts=[],[]
        source_counts[rec['root_path']]=dict(observations=len(rs),table_rows=len(ts));rows+=rs;tables+=ts
    inventory=load(directory/'source_inventory.json');actual={r['source_id']:r for r in inventory['observations']};assert len(actual)==len(rows) and set(actual)=={r['source_id'] for r in rows}
    groups=defaultdict(lambda:defaultdict(list))
    for r in rows:groups[r['season']][r['source']].append(r)
    parent={r['source_id']:r['source_id'] for r in rows};allmaps={}
    def find(x):
        while parent[x]!=x:x=parent[x]
        return x
    for season,sources in sorted(groups.items()):
        ordered=sorted(sources,key=lambda p:(0 if p.endswith('turkey.csv') else 1 if p.endswith('T1.csv') else 2,p));anchors=sources[ordered[0]];pairs=defaultdict(list)
        for r in anchors:pairs[r['stage'],r['home'],r['away']].append(r)
        for source in ordered[1:]:
            secondary=sources[source];mapping=names(anchors,[r for r in secondary if r['stage']=='REGULAR_SEASON']);allmaps[season,source]=mapping
            frequencies=Counter((r['stage'],mapping.get(r['home'],r['home']),mapping.get(r['away'],r['away'])) for r in secondary)
            for r in secondary:
                if r['home'] not in mapping or r['away'] not in mapping or r['stage']!='REGULAR_SEASON':continue
                key=(r['stage'],mapping[r['home']],mapping[r['away']]);options=pairs[key]
                if frequencies[key]>1:options=[x for x in options if x['date'] is not None and x['date']==r['date']]
                if len(options)==1:parent[find(r['source_id'])]=find(options[0]['source_id'])
                if season=='2006/2007' and source.endswith('tur07.html'):
                    q={(z['original_fields']['home'],z['original_fields']['visitor']) for z in rules.values() if z['derived_date'] is None}
                    if key[1:] in q:r['quarantined']=True
    for r in rows:
        for key,value in r.items():assert actual[r['source_id']][key]==value,(r['source'],r['line'],key,value,actual[r['source_id']].get(key))
    actualtables={t['source_id']:t for t in inventory['aggregate_tables']};assert set(actualtables)=={t['source_id'] for t in tables}
    for t in tables:
        for key,value in t.items():assert actualtables[t['source_id']][key]==value,(t,key)
    components=defaultdict(list)
    for r in rows:components[find(r['source_id'])].append(r)
    overlap=load(directory/'overlap_assessment.json');actualevents={tuple(e['source_ids']):e for e in overlap['conditional_events']};assert set(actualevents)=={tuple(sorted(r['source_id'] for r in members)) for members in components.values()}
    issues=Counter();byseason=Counter();mult=Counter()
    for members in components.values():
        event=actualevents[tuple(sorted(r['source_id'] for r in members))];dates={r['date'] for r in members if r['date']};scored={r['date'] for r in members if r['date'] and r['hg'] is not None};scores={(r['hg'],r['ag']) for r in members if r['hg'] is not None};expected=[]
        if len(scored)>1:expected.append('DATE_CONFLICT')
        elif len(dates)>1:expected.append('SCHEDULE_DATE_DIFFERENCE')
        if len(scores)>1:expected.append('SCORE_CONFLICT')
        if any(r['quarantined'] for r in members):expected.append('FROZEN_PHASE1_QUARANTINE')
        assert event['issues']==expected and event['quarantined']==any(k!='SCHEDULE_DATE_DIFFERENCE' for k in expected)
        issues.update(expected);byseason[members[0]['season']]+=1;mult[len(members)]+=1
    coverage=load(directory/'season_stage_coverage.json')['coverage'];assert len(coverage)==36
    for entry in coverage:
        s=entry['season'];assert entry['conditional_events']==byseason[s];assert entry['source_observations']==sum(r['season']==s for r in rows)
        assert entry['aggregate_rows']==sum(t['season']==s for t in tables)
        for source in entry['sources']:
            rs=[r for r in rows if r['season']==s and r['source']==source['source']];assert source['observations']==len(rs);assert source['scored']==sum(r['hg'] is not None for r in rs);assert source['quarantined']==sum(r['quarantined'] for r in rs)
    discrepancy=load(directory/'discrepancy_registry.json');assert len(discrepancy['corrections'])==sum(r['correction'] is not None for r in rows)==143;assert len(discrepancy['quarantined_observations'])==sum(r['quarantined'] for r in rows)==30
    queue=load(directory/'review_queue.json')['items'];assert len(queue)==len({i['queue_id'] for i in queue});assert all(set(i['source_ids'])<=set(actual) for i in queue)
    checks=load(directory/'structural_checks.json');diagnostics={(d['season'],d['source'],d['stage']):d for d in checks['source_stage_checks']};batches=defaultdict(list)
    for r in rows:batches[r['season'],r['source'],r['stage']].append(r)
    repeated=set()
    for key,rs in batches.items():
        s,source,stage=key;mapping=allmaps.get((s,source),{});clubs={mapping.get(r[side],r[side]) for r in rs for side in ['home','away']};pairs=Counter((mapping.get(r['home'],r['home']),mapping.get(r['away'],r['away'])) for r in rs);d=diagnostics[key]
        assert d['coeval_identity_count']==len(clubs) and d['distinct_directed_pairs']==len(pairs)
        assert set(map(tuple,d['pairing_gaps_among_observed_identities']))=={(h,a) for h in clubs for a in clubs if h!=a and (h,a) not in pairs}
        assert d['round_observation_counts']==dict(Counter(str(r['round']) for r in rs if r['round'] is not None))
        participation=Counter(mapping.get(r[side],r[side]) for r in rs for side in ['home','away']);assert d['club_participations']==dict(participation)
        signatures=Counter((r['date'],r['home'],r['away'],r['hg'],r['ag'],r['round']) for r in rs);assert d['exact_repeated_observation_count']==sum(n-1 for n in signatures.values())
        rawpairs=Counter((r['home'],r['away']) for r in rs)
        repeated.update(r['source_id'] for r in rs if rawpairs[r['home'],r['away']]>1)
        year=int(s[:4]);n=16 if year<1994 else {2020:21,2021:20,2022:19,2023:20,2024:19}.get(year,18);assert config['expected_regular_clubs'][str(year)]==n
        for r in rs:
            if isinstance(r['round'],int):assert 1<=r['round']<=(2*n if n%2 else 2*(n-1))
    assert set(checks['quarantined_event_ids'])=={e['event_id'] for e in actualevents.values() if e['quarantined']}
    assert set(checks['all_structural_quarantine_source_ids'])=={s for e in actualevents.values() if e['quarantined'] for s in e['source_ids']}
    queued={tuple(i['source_ids']):set(i['categories']) for i in queue if i['kind']=='CONDITIONAL_EVENT'};expectedqueue={}
    for members in components.values():
        key=tuple(sorted(r['source_id'] for r in members));e=actualevents[key];reasons=set(e['issues'])
        for r in members:
            if r['source_id'] in repeated:reasons.add('REPEATED_SOURCE_PAIRING')
            if r['hg'] is None:reasons.add('UNSCORED_OR_INTERRUPTED')
            if r['annotation']:reasons.add('SOURCE_ANNOTATION')
            if not r['date']:reasons.add('DATE_NOT_EXACT')
            if r['hg'] is not None and (int(r['hg'])+int(r['ag'])>=10 or abs(int(r['hg'])-int(r['ag']))>=7):reasons.add('EXTREME_SCORE_RESEARCH')
        if members[0]['stage']!='REGULAR_SEASON':reasons.add('STAGE_SCOPE_RESEARCH')
        if reasons:expectedqueue[key]=reasons
    assert queued==expectedqueue
    # Catalogued physical spans must cover every original byte-line once.
    for rec in inventory['catalogue']:
        lines=(ROOT/rec['root_path']).read_bytes().splitlines(keepends=True);covered=[]
        for segment in rec['sections']:
            start,end=segment['start'],segment['end'];assert sha(b''.join(lines[start-1:end]))==segment['sha256'];covered+=range(start,end+1)
        assert covered==list(range(1,len(lines)+1)) and rec['fixture_observations']==source_counts[rec['root_path']]['observations']
    return dict(status='PASS',originals=len(config['files']),source_observations=len(rows),aggregate_rows=len(tables),conditional_events=len(components),multiplicity={str(k):v for k,v in sorted(mult.items())},issues=dict(issues),corrections=143,quarantined_source_representations=30,queue_items=len(queue),source_counts=source_counts,method='IndependentpositionalCSV/HTMLParser/TXTgrammar,coevalnameinferenceandunion-find;no productioncontenthelpersimported')


if __name__=='__main__':
    p=__import__('argparse').ArgumentParser();p.add_argument('--verify',action='store_true');args=p.parse_args();raw=enc(validate());target=OUTPUT/'independent_validation.json'
    if args.verify:assert target.read_bytes()==raw
    else:
        with target.open('xb') as f:f.write(raw)
    print(raw.decode())
