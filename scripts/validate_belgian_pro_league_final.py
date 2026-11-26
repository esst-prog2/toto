"""Independent Belgian Phase8: stdlib raw parsers, registry and CSV reconciliation.

No Phase7 content/naming/ID functions imported. Approved originals and decisions
are read-only. Material mismatches raise BLOCKED, never repair data.
"""
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from html import unescape
from pathlib import Path
import argparse, calendar, csv, hashlib, io, json, os, re, subprocess, sys, tempfile

ROOT=Path(__file__).resolve().parents[1]
PRIVATE=ROOT/'data/private/belgium/pro_league'
HEAD='013bb9c195624d5ac290aeb57dae11c4e21c0b5a'
CSV_NAME='belgian_pro_league_standardized_1995_2026.csv'
CSV_SHA='8d4e37b1697ae94c8a54d2247476578b3b85f7076e58c2fe5d024a7721791475'
COLS=('match_id','date','league','season','home_team','away_team','home_goals','away_goals')
LEAGUE='Belgian Pro League'
DISPOSITIONS={'INCLUDE':8592,'HOLD_OUT':120,'NOT_PLAYED':10,'OUT_OF_SCOPE':2}
STAGES={'REGULAR_SEASON':8370,'CHAMPIONSHIP':113,'EUROPE':83,'PLAYDOWNS':24,'EUROPE_QUALIFICATION':2}
NAMES=('raw_source_traceability.json','record_reconciliation.json','season_stage_and_rematches.json','findings_and_preservation.json')

class Defect(ValueError):pass

def require(ok,message):
    if not ok:raise Defect(message)
def digest(raw):return hashlib.sha256(raw).hexdigest()
def pretty(value):return (json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
def read(path):return json.loads(path.read_text())
def identifier(values):return digest(json.dumps(values,ensure_ascii=False,separators=(',',':')).encode('utf-8'))
def iso(value):
    require(isinstance(value,str) and bool(re.fullmatch(r'\d{4}-\d{2}-\d{2}',value)),'Noncanonical date '+repr(value))
    return date.fromisoformat(value)
def goals(value):
    require(isinstance(value,str) and bool(re.fullmatch(r'(0|[1-9]\d*)-(0|[1-9]\d*)',value)),'Invalid final score '+repr(value))
    return tuple(map(int,value.split('-')))

def protected_signature(path):
    st=path.stat()
    return [st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns,st.st_ctime_ns]

def verify_protected_bytes(path,expected):
    before=protected_signature(path);actual=digest(path.read_bytes());after=protected_signature(path)
    require(actual==expected,'Protected file changed: '+str(path))
    if before!=after:
        # Hydration can replace an inode or restore timestamps. Re-read once;
        # both independent byte reads must equal the approved digest.
        confirm=digest(path.read_bytes());last=protected_signature(path)
        require(confirm==expected,'Protected file changed on confirmation: '+str(path))
        # Only byte equality is the preservation contract. File-provider
        # metadata may keep changing; a new signature invalidates the checkpoint
        # on the next pass, while both actual SHA reads must still match.
        after=last
    return after

def preserve(directory=PRIVATE):
    require(subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='feature/data-collection','Wrong branch')
    require(subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==HEAD,'Wrong HEAD')
    require(not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT),'Unexpected staging')
    start=read(directory/'git_start.json');index=Path(subprocess.check_output(['git','rev-parse','--git-path','index'],cwd=ROOT,text=True).strip())
    if not index.is_absolute():index=ROOT/index
    require(digest(index.read_bytes())==start['index_sha256'],'Index hash changed')
    total=0; expected={}
    for baseline in [directory/'protected_before.json',*sorted(directory.glob('*_protected_before.json'))]:
        saved=read(baseline)
        for kind in ('private','public','files'):
            for name,h in saved.get(kind,{}).items():
                require(not Path(name).is_absolute() and '..' not in Path(name).parts,'Unsafe baseline path')
                require(name not in expected or expected[name]==h,'Conflicting frozen fingerprints: '+name)
                expected[name]=h;total+=1
        prefix=saved.get('planning_log')
        if prefix:require(digest((ROOT/'PLANNING_LOG.md').read_bytes()[:prefix['bytes']])==prefix['sha256'],'Planning prefix changed')
    # Required Phase8 byte scope: all frozen Belgian work, all previous public
    # code, and all prior screened datasets/compatible audit IDs. Older unrelated
    # private regression logs are preserved read-only, not an exhaustive audit.
    before=read(directory/'protected_before.json')
    required=dict(read(directory/'phase8_protected_before.json')['files'])
    required.update(before['public'])
    required.update({n:h for n,h in before['private'].items() if n.endswith('.csv') and ('standardized' in Path(n).name or 'audit_archive' in Path(n).name)})
    unscanned_older_private=len(set(before['private'])-set(required))
    expected=required
    # Checkpoint fresh Phase8 reads outside the project. File stat identity is
    # checked before/after hashing; interrupted runs resume only unchanged files
    # verified under this exact approved baseline. No previous-phase proof reused.
    token=digest((directory/'phase8_protected_before.json').read_bytes())
    cache_path=Path(tempfile.gettempdir())/('belgian-phase8-hashes-'+token+'.json')
    try:cache=read(cache_path)
    except (FileNotFoundError,json.JSONDecodeError):cache={'baseline':token,'files':{}}
    require(cache['baseline']==token,'Wrong checkpoint baseline')
    pending=[]
    for name,h in expected.items():
        signature=protected_signature(ROOT/name);old=cache['files'].get(name,{})
        if old.get('signature')!=signature or old.get('sha256')!=h:pending.append((name,h))
    # Eight local read-only workers avoid serial file-provider latency. Cache
    # mutations remain single-threaded; no original or environment file is written.
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures={pool.submit(verify_protected_bytes,ROOT/name,h):(name,h) for name,h in pending}
        for future in as_completed(futures):
            name,h=futures[future]
            try:signature=future.result()
            except Exception:
                for queued in futures:queued.cancel()
                print('HASH_FAILURE '+name,file=sys.stderr,flush=True)
                raise
            cache['files'][name]={'signature':signature,'sha256':h}
            temporary=cache_path.with_suffix('.pending');temporary.write_bytes(pretty(cache));os.replace(temporary,cache_path)
    return dict(fingerprint_memberships_registered=total,unique_required_fingerprints_checked=len(expected),older_private_files_not_exhaustively_rehashed=unscanned_older_private,all_frozen_belgian_artifacts_checked=True,all_previous_public_code_checked=True,head=HEAD,index_unchanged=True)


def bind(raw,receipt,line,end,**facts):
    physical=b''.join(raw.splitlines(keepends=True)[line-1:end])
    return dict(source_id=digest(pretty([receipt['sha256'],line,end])),source=receipt['path'],line=line,end=end,
                source_sha256=receipt['sha256'],physical_sha256=digest(physical),**facts)

def parse_csv(raw,rec):
    reader=csv.DictReader(io.StringIO(raw.decode('utf-8-sig'),newline=''),strict=True);rows=[]
    require(set(reader.fieldnames or ())=={'Date','Season','home','visitor','FT','hgoal','vgoal','division','tier','totgoal','goaldif','result'},'Wrong historical columns')
    while True:
        start=reader.line_num+1
        try:r=next(reader)
        except StopIteration:break
        require(r['division']=='B1' and r['tier']=='1','Wrong original competition')
        h,a=goals(r['FT']);year=int(r['Season']);day=iso(r['Date'])
        require(r['hgoal']==str(h) and r['vgoal']==str(a) and r['totgoal']==str(h+a) and r['goaldif']==str(h-a),'Conflicting original goals at '+str(start))
        require(r['result']==('H' if h>a else 'A' if h<a else 'D'),'Conflicting original outcome')
        require(date(year,7,1)<=day<=date(year+1,6,30),'Historical date outside season')
        rows.append(bind(raw,rec,start,reader.line_num,season=f'{year}/{year+1}',date=r['Date'],home=r['home'],away=r['visitor'],FT=r['FT'],stage='UNKNOWN',round=None,leg=None,annotation='',original_fields=r))
    return rows


def heading_day(text,year):
    m=re.fullmatch(r'([A-Za-z]{3}) ([A-Za-z]{3}) (\d{1,2})(?: (\d{4}))?',text)
    if not m:return None
    require(m[1] in calendar.day_abbr and m[2] in calendar.month_abbr,'Unknown calendar heading')
    candidates=[]
    for y in ([int(m[4])] if m[4] else [year,year+1]):
        try:d=date(y,list(calendar.month_abbr).index(m[2]),int(m[3]))
        except ValueError:continue
        if date(year,7,1)<=d<=date(year+1,6,30) and calendar.day_abbr[d.weekday()]==m[1]:candidates.append(d.isoformat())
    require(len(candidates)==1,'Ambiguous calendar heading '+text)
    return candidates[0]


def parse_txt(raw,rec):
    rows=[];year=None;current=None;stage=None;rnd=None
    for line,literal in enumerate(raw.decode('utf-8-sig').splitlines(),1):
        text=literal.strip()
        if not text or text.startswith('#'):continue
        if text.startswith('='):
            m=re.fullmatch(r'= Belgium First Division A (\d{4})/(\d{2})',text)
            require(m is not None and year is None,'Invalid original title')
            year=int(m[1]);require(int(m[2])==(year+1)%100,'Title season mismatch');continue
        require(year is not None,'Fixture without title')
        if text.startswith('▪'):
            bits=[x.strip() for x in text[1:].strip().split(',')]
            types={'Playoff I':'CHAMPIONSHIP','Championship':'CHAMPIONSHIP','Europe':'EUROPE','Relegation':'PLAYDOWNS','ECL Playoff':'EUROPE_QUALIFICATION'}
            require(len(bits)==1 or bits[0] in types,'Unknown original stage')
            stage=types[bits[0]] if len(bits)>1 else 'REGULAR_SEASON'
            rm=re.fullmatch(r'(?:Matchday (\d+)|(\d+)\. Round)',bits[-1])
            require(rm is not None or bits==['ECL Playoff','Final'],'Unknown original round')
            rnd=int(rm[1] or rm[2]) if rm else 'Final'
            if isinstance(rnd,int):
                limit=(34 if year in (2020,2021,2022) else 30) if stage=='REGULAR_SEASON' else 6 if stage=='PLAYDOWNS' or year in (2020,2021,2022) else 10
                require(1<=rnd<=limit,'Round outside competition stage')
            current=None;continue
        d=heading_day(text,year)
        if d:current=d;continue
        require(current is not None and stage is not None,'Undated source fixture')
        body=re.sub(r'^\d{1,2}:\d{2}\s+','',text)
        note=re.search(r'\s+(\[.*\])$',body);annotation=note[1] if note else ''
        if note:body=body[:note.start()]
        sides=re.split(r'\s+v\s+',body);require(len(sides)==2,'Unknown fixture syntax')
        home,tail=sides;score=re.search(r'\s{2,}(\d+)-(\d+)(?:\s+\((\d+)-(\d+)\))?$',tail)
        if score:
            away=tail[:score.start()].strip();ft=score[1]+'-'+score[2];goals(ft)
            if score[3] is not None:require(int(score[3])<=int(score[1]) and int(score[4])<=int(score[2]),'HT exceeds FT')
        else:
            away=tail.strip();ft=None;require(not re.search(r'\s+\d+[-:]|\?',away),'Malformed unscored slot')
        rows.append(bind(raw,rec,line,line,season=f'{year}/{year+1}',date=current,home=home.strip(),away=away,FT=ft,stage=stage,round=rnd,leg=None,annotation=annotation))
    expected=int(rec['season'][:4]);misplaced=rec['path']=='openfootball/belgium/2021-22/be1.txt'
    require(year==(2020 if misplaced else expected),'Unapproved wrong-season file')
    return rows,dict(path=rec['path'],requested=rec['season'],actual=f'{year}/{year+1}',path_mismatch=misplaced)


def parse_rsssf(raw,rec):
    rows=[];inside=False;stage=None;rnd=None;leg=None;current=None;pending=None
    stage_names={'reg':'REGULAR','po1':'CHAMPIONSHIP','po2':'EUROPE','prorel':'PROMOTION_RELEGATION'}
    for number,literal in enumerate(raw.decode(rec['encoding']).splitlines(),1):
        if '<h4>' in literal.lower():
            inside=bool(re.search(r'name="pro"',literal));stage=None
        if not inside:continue
        for anchor,kind in stage_names.items():
            if re.search('name="'+anchor+'"',literal):stage=kind;rnd=None;leg=None;current=None
        if stage is None:continue
        plain=unescape(re.sub('<[^>]*>','',literal)).strip()
        rm=re.match(r'Round (\d+)',plain)
        if rm:rnd=int(rm[1]);leg=None;current=None
        if plain.startswith(('First Leg','Second Leg')):leg=1 if plain.startswith('First') else 2;rnd=None;current=None
        dm=re.search(r'\[([A-Z][a-z]{2}) (\d{1,2})\]',plain)
        if dm:
            month=list(calendar.month_abbr).index(dm[1]);current=date(2021 if month>=7 else 2022,month,int(dm[2])).isoformat()
        literal_clean=re.sub('<[^>]*>','',literal).strip()
        m=re.match(r'^([A-Za-z].*?)\s{2,}(\d+-\d+|awd|abd|n/p)\s+(.+)$',literal_clean)
        if m:
            require(current is not None,'Undated RSSSF fixture')
            home,token,tail=m.groups();parts=re.split(r'\s{2,}',tail,maxsplit=1);away=parts[0];note=parts[1] if len(parts)>1 else ''
            bracket=re.search(r'\s+(\[.*)',away)
            if bracket:note=bracket[1]+(' '+note if note else '');away=away[:bracket.start()]
            if note and not note.startswith('['):
                require(pending is not None,'Unbound RSSSF trailing annotation');rows[pending]['annotation']+=' '+unescape(note)
                if ']' in note:pending=None
                note=''
            sid=digest(pretty([rec['sha256'],number,'RSSSF_2021_RECOVERY']))
            rows.append(dict(source_id=sid,source='rsssf/tablesb/belg2022.html',line=number,end=number,
                 source_sha256=rec['sha256'],physical_sha256=digest(raw.splitlines(keepends=True)[number-1]),
                 season='2021/2022',date=current,home=unescape(home),away=unescape(away),token=token,
                 FT=token if re.fullmatch(r'\d+-\d+',token) else None,stage=stage,round=rnd,leg=leg,
                 annotation=unescape(note),raw_html=literal))
            if note and ']' not in note:pending=len(rows)-1
        elif pending is not None and plain:
            rows[pending]['annotation']+=' '+plain
            if ']' in plain:pending=None
    require(pending is None,'Unclosed RSSSF note')
    for r in rows:
        if r['token']=='awd':
            match=re.search(r'awarded (\d+-\d+)',r['annotation']);require(match is not None,'Unresolved numerical award');r['FT']=match[1]
    return rows


def source_rows(directory):
    receipts=read(directory/'acquisition.json')['files']+read(directory/'phase3_acquisition.json')['files']
    recovered=read(directory/'rsssf/tablesb/belg2022.html.provenance.json')
    allrows=[];notes=[];raw_files={}
    for rec in receipts:
        raw=(directory/rec['path']).read_bytes();require(digest(raw)==rec['sha256'] and len(raw)==rec['bytes'],'Original checksum mismatch '+rec['path']);raw_files[rec['path']]=raw
        if rec.get('git_blob_sha1'):
            blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
            require(blob==rec['git_blob_sha1']==rec['expected_blob'],'Pinned Git blob mismatch')
        if rec['path'].endswith('belgium.csv'):allrows.extend(parse_csv(raw,rec))
        elif rec['path'].endswith('be1.txt'):
            parsed,note=parse_txt(raw,rec);allrows.extend(parsed);notes.append(note)
    raw=(directory/'rsssf/tablesb/belg2022.html').read_bytes()
    require(digest(raw)==recovered['sha256'] and len(raw)==recovered['bytes'],'Recovery original checksum mismatch')
    raw_files['rsssf/tablesb/belg2022.html']=raw
    rsssf=parse_rsssf(raw,recovered);allrows.extend(rsssf)
    lookup={r['source_id']:r for r in allrows}
    require(len(lookup)==len(allrows)==10434,'Independent original population differs')
    return lookup,notes,raw_files


def group_bindings(decisions,lookup):
    used=[];events=[]
    for d in decisions:
        require(d['disposition'] in DISPOSITIONS,'Unknown disposition')
        rs=[]
        for representation in d['representations']:
            b=representation['binding']
            bindings=[b] if representation['kind']=='CSV_TXT' else b['representations']
            for binding in bindings:
                sid=binding.get('audit_id',binding.get('source_id'));require(sid in lookup,'Unknown original source ID '+str(sid))
                r=lookup[sid];used.append(sid);rs.append(r)
                for field in ('source','season','date','home','away'):
                    require(r[field]==binding[field],'Source fact mismatch '+sid+' '+field)
                require(r['line']==binding['source_line'] and r['end']==binding.get('source_end_line',binding['source_line']) and r['source_sha256']==binding['source_sha256'],'Source provenance differs '+sid)
                require(r['round']==binding.get('round') and r['leg']==binding.get('leg') and binding.get('group') is None,'Original round/leg/group differs '+sid)
                physical=binding.get('physical_record_sha256',binding.get('source_line_sha256'))
                require(r['physical_sha256']==physical,'Physical source hash differs '+sid)
                if representation['kind']=='CSV_TXT':require(r['FT']==binding['FT'] and r['stage']==binding['stage'],'Source score/stage differs '+sid)
                else:require(r['token']==binding['score_token'] and r['stage']==binding['stage'] and r['raw_html']==binding['raw_html'],'Documentary token/stage differs '+sid)
        require(sorted(r['source_id'] for r in rs)==sorted(d['source_ids']),'Decision source membership differs '+d['decision_id'])
        by_source_id={r['source_id']:r for r in rs}
        for context in d['stage_identity_bindings']:
            for sid in context['source_ids']:
                r=by_source_id[sid]
                require((r['stage'],r['round'],r['leg'],context['group'])==(context['stage'],context['round'],context['leg'],None),'Stage audit context differs '+sid)
        require(d['representations_count']==len(rs),'Decision representation count differs')
        stages={r['stage'] for r in rs if r['stage']!='UNKNOWN'}
        stages={'REGULAR_SEASON' if x=='REGULAR' else x for x in stages}
        inferred=next(iter(stages)) if len(stages)==1 else 'REGULAR_SEASON' if not stages and all('jalapic/' in r['source'] for r in rs) else None
        require(inferred==d['stage'],'Event stage differs '+d['decision_id'])
        terminal=[r for r in rs if r.get('token')!='abd']
        require({r['date'] for r in terminal}=={d['original_fixture_date']},'Event source dates conflict '+d['decision_id'])
        require({r['FT'] for r in terminal}=={d['reported_score']},'Event final source scores conflict '+d['decision_id'])
        require({r['season'] for r in rs}=={d['season']},'Mixed-season event')
        events.append((d,rs))
    require(len(used)==len(set(used))==10434 and set(used)==set(lookup),'Lost/reused original representation')
    require(len({d['decision_id'] for d in decisions})==len(decisions)==8724,'Event IDs/population differ')
    require(dict(Counter(d['disposition'] for d in decisions))==DISPOSITIONS,'Disposition totals differ')
    return events


def coeval_names(events):
    names={};evidence=defaultdict(list)
    def add(key,value,proof):
        require(key not in names or names[key]==value,'Ambiguous independent name correspondence '+repr(key))
        names[key]=value;evidence[key].append(proof)
    for d,rows in events:
        history=[r for r in rows if 'jalapic/' in r['source']]
        if history:
            require(len(history)==1,'Multiple historical anchors')
            h=history[0]
            for r in rows:
                for side in ('home','away'):add((d['season'],r['source'],r[side]),h[side],d['decision_id'])
        elif d['season']=='2025/2026':
            for r in rows:
                for side in ('home','away'):add((d['season'],r['source'],r[side]),r[side],d['decision_id'])
    # Source-local injectivity prevents one city/label from collapsing two clubs.
    grouped=defaultdict(dict)
    for (season,source,original),target in names.items():
        require(target not in grouped[season,source] or grouped[season,source][target]==original,'Many-to-one name collapse')
        grouped[season,source][target]=original
    return names,evidence


def evaluate(events,names,expected_count=8592,expected_stages=None,expected_rematches=(222,444)):
    if expected_stages is None:expected_stages=STAGES
    expected=[];by_id={};trace=[];season=defaultdict(Counter);stage=Counter();pairings=defaultdict(list)
    resumed={'beerschot_cercle_resumed':('2021-07-24','2021-07-27','0-1'),
             'seraing_union_resumed':('2022-01-15','2022-01-18','0-4')}
    cases={'standard_anderlecht_2019':('HOLD_OUT',None),'standard_westerlo_2024':('NOT_PLAYED',None),
           'leuven_mechelen_2022':('NOT_PLAYED',None),'union_beerschot_2022':('INCLUDE','5-0'),
           'standard_charleroi_2021':('INCLUDE','0-3')}
    for d,rs in events:
        season[d['season']][d['disposition']]+=1
        case=d.get('case_id');selected=None
        if case in cases:
            require((d['disposition'],d['accepted_score'])==cases[case],'Approved award decision differs '+case)
        if d['disposition']=='INCLUDE':
            sides={side:{names.get((d['season'],r['source'],r[side])) for r in rs} for side in ('home','away')}
            require(all(None not in v and len(v)==1 for v in sides.values()),'Unresolved source-bound team identity '+d['decision_id'])
            home,away=next(iter(sides['home'])),next(iter(sides['away']))
            require(home!=away and home.strip()==home and away.strip()==away and '\ufffd' not in home+away,'Invalid canonical teams')
            chosen=d['chosen_match_date'];day=iso(chosen);year=int(d['season'][:4])
            require(d['season']==f'{year}/{year+1}' and 1995<=year<=2025 and date(year,7,1)<=day<=date(year+1,6,30),'Season/date mismatch')
            h,a=goals(d['accepted_score']);require(d['accepted_score']==d['reported_score'],'Unapproved score correction')
            require(d['accepted_outcome']==('H' if h>a else 'A' if h<a else 'D'),'Accepted outcome contradiction')
            if case in resumed:
                kickoff,completion,ft=resumed[case]
                require((chosen,d['completion_date'],d['accepted_score'])==(kickoff,completion,ft),'Resumption date/result differs')
                require(any(r['date']==kickoff and r.get('token')=='abd' for r in rs),'Missing original interruption')
            else:require(chosen==d['original_fixture_date'],'Judgment/unapproved date substituted')
            mid=identifier([LEAGUE,d['season'],chosen,home,away]);require(mid not in by_id,'Stage/fixture shared-ID collision')
            selected=dict(zip(COLS,[mid,chosen,LEAGUE,d['season'],home,away,h,a]));expected.append(selected);by_id[mid]=d
            stage[d['stage']]+=1;pairings[d['season'],home,away].append(dict(match_id=mid,date=chosen,stage=d['stage'],decision_id=d['decision_id']))
        else:
            require(d['accepted_score'] is None and d['chosen_match_date'] is None,'Excluded event carries accepted values')
            if d['disposition']=='NOT_PLAYED' and case is None:
                require(d['season']=='2019/2020' and any('cancelled' in r['annotation'] for r in rs),'Unexplained NOT_PLAYED')
            if d['disposition']=='HOLD_OUT' and case is None:
                require(d['season']=='2025/2026' and all(r['FT'] is None for r in rs),'Unexplained HOLD_OUT')
            if d['disposition']=='OUT_OF_SCOPE':require(d['stage']=='PROMOTION_RELEGATION','Wrong cross-division exclusion')
        trace.append(dict(decision_id=d['decision_id'],source_ids=[r['source_id'] for r in rs],disposition=d['disposition'],match_id=selected['match_id'] if selected else None,stage=d['stage']))
    require(len(expected)==expected_count and dict(stage)==expected_stages,'Accepted population/stages differ')
    rematches=[dict(season=k[0],home=k[1],away=k[2],fixtures=v) for k,v in sorted(pairings.items()) if len(v)>1]
    require((len(rematches),sum(len(x['fixtures']) for x in rematches))==expected_rematches,'Rematch totals differ')
    for group in rematches:require(len({x['date'] for x in group['fixtures']})==len(group['fixtures']),'Same-date rematch collision')
    return sorted(expected,key=lambda r:tuple(r[k] for k in ('league','season','date','home_team','away_team'))),by_id,trace,season,stage,rematches


def csv_bytes(rows):
    buffer=io.StringIO(newline='');writer=csv.DictWriter(buffer,fieldnames=COLS,lineterminator='\n');writer.writeheader();writer.writerows(rows)
    return buffer.getvalue().encode('utf-8')

def check_csv(raw,expected):
    reader=csv.DictReader(io.StringIO(raw.decode('utf-8')),strict=True);require(tuple(reader.fieldnames or ())==COLS,'Wrong CSV schema/order')
    actual=[];ids=set()
    for row in reader:
        require(None not in row and all(v is not None for v in row.values()),'Malformed CSV width')
        for col in ('home_goals','away_goals'):
            require(bool(re.fullmatch(r'0|[1-9][0-9]*',row[col])),'Invalid CSV goals');row[col]=int(row[col])
        require(row['league']==LEAGUE,'Wrong CSV league');iso(row['date'])
        mid=identifier([row['league'],row['season'],row['date'],row['home_team'],row['away_team']])
        require(row['match_id']==mid and mid not in ids,'Wrong/duplicate CSV ID '+row['match_id']);ids.add(mid);actual.append(row)
    require(actual==expected,'Exact CSV/approved-registry rows or ordering differ')
    require(raw==csv_bytes(expected),'Independent CSV regeneration differs byte-for-byte')
    return actual


def build(directory=PRIVATE):
    protected=preserve(directory);lookup,notes,raw_files=source_rows(directory)
    decisions=read(directory/'phase6/decision_registry.json')['decisions'];events=group_bindings(decisions,lookup)
    names,evidence=coeval_names(events)
    expected,by_id,trace,seasons,stages,rematches=evaluate(events,names)
    raw=(directory/CSV_NAME).read_bytes();require(digest(raw)==CSV_SHA,'Approved CSV SHA mismatch');actual=check_csv(raw,expected)
    archive=read(directory/'belgian_pro_league_audit_archive_1995_2026.json');arch={r['decision_id']:r for r in archive['events']}
    require(len(arch)==8724,'Archive event count/duplicates')
    projections={r['match_id']:r for r in expected}
    trace_by_decision={item['decision_id']:item for item in trace}
    for d,rs in events:
        a=arch[d['decision_id']];require(a['approved_phase6_decision']==d,'Audit changed authoritative decision')
        mid=trace_by_decision[d['decision_id']]['match_id']
        require(a['screened_match_id']==mid and a['standardized_values']==projections.get(mid),'Audit/output binding differs')
        for binding in a['canonical_name_bindings']:
            key=(binding['season'],binding['source'],binding['original'])
            require(names.get(key)==binding['canonical'],'Audit name proof differs')
            require(any(r['source']==binding['source'] and r[binding['side']]==binding['original'] for r in rs),'Name proof detached from source event')
            require(mid is not None and projections[mid][binding['side']+'_team']==binding['canonical'],'Name proof disagrees with standardized side')
    docs=read(directory/'phase6/documentary_decisions.json')['decisions'];require(len(docs)==30,'Documentary population differs')
    for doc in docs:
        b=doc['source_binding'];literal=raw_files[b['source']].splitlines(keepends=True)[b['source_line']-1]
        require(digest(literal)==b['source_line_sha256'],'Documentary physical binding differs')
        require(doc['disposition'] in {'HOLD_OUT','NOT_PLAYED'} and doc['accepted_score'] is None and doc['chosen_match_date'] is None,'Documentary-only inclusion')
        plain=unescape(re.sub('<[^>]*>','',literal.decode('utf-8'))).strip()
        require(b['home'] in plain and b['away'] in plain and b['score'] in plain,'Documentary source facts differ')
        require(doc['documentary_id'] not in lookup,'Earlier documentary mixed into union')
    require(archive['earlier_documentary_only']==read(directory/'phase6/documentary_decisions.json'),'Archive documentary mismatch')
    require(read(directory/'early_recovery/assessment/supplemental_registry.json')['candidates']==[],'Unapproved early candidates')
    prior=read(directory/'protected_before.json')['private'];old_ids=set();historical=ongoing=0
    for path,h in prior.items():
        if not path.endswith('.csv') or not ('standardized' in Path(path).name or 'audit_archive' in Path(path).name):continue
        blob=(ROOT/path).read_bytes()
        if blob.splitlines()[0].lstrip(b'\xef\xbb\xbf')!=','.join(COLS).encode():continue
        require(digest(blob)==h,'Previous standard/audit changed')
        rows=list(csv.DictReader(io.StringIO(blob.decode('utf-8-sig'))));old_ids.update(r['match_id'] for r in rows)
        if 'standardized' in Path(path).name:
            if 'ongoing' in path:ongoing+=len(rows)
            else:historical+=len(rows)
    require(not old_ids.intersection(by_id),'Prior competition ID collision');require((historical,ongoing)==(137189,258),'Previous competition counts differ')
    matrix=[dict(season=f'{y}/{y+1}',dispositions=dict(seasons[f'{y}/{y+1}']),standardized=sum(r['season']==f'{y}/{y+1}' for r in actual),coverage_gap=y<1995,incomplete_snapshot=y==2025) for y in range(1990,2026)]
    for row in matrix:require(row['standardized']==row['dispositions'].get('INCLUDE',0),'Season count differs')
    for y,count in {2018:269,2019:232,2020:330,2021:329,2023:312,2024:313,2025:121}.items():require(seasons[f'{y}/{y+1}']['INCLUDE']==count,'Sensitive season differs')
    require(any(r['date']=='2025-05-29' and r['home_team']=='Antwerp' and r['away_team']=='Charleroi' and (r['home_goals'],r['away_goals'])==(1,2) for r in actual),'Missing qualifier')
    outputs=dict(zip(NAMES,[dict(raw_observations=list(lookup.values()),source_notes=notes,source_event_output_links=trace),
        dict(rows_checked=len(actual),csv_sha256=digest(raw),schema=list(COLS),decision_links=[dict(match_id=k,decision_id=v['decision_id']) for k,v in sorted(by_id.items())],independent_name_proofs=[dict(season=k[0],source=k[1],original=k[2],canonical=v,coeval_decisions=sorted(set(evidence[k]))) for k,v in sorted(names.items())],all_ids_recomputed=True),
        dict(seasons=matrix,stages=dict(stages),rematches=rematches,rematch_pairs=len(rematches),rematch_events=444),
        dict(status='PASS',material_findings=[],historical_certification=False,licensing_or_training_clearance=False,protected=protected,previous_historical_records=historical,previous_ongoing_records=ongoing,source_representations=10434,events=8724,screened=8592,documentary_separate=30,dispositions=DISPOSITIONS,independent_csv_byte_identical=True)]))
    return outputs,csv_bytes(expected)


def keep(path,raw):
    if path.exists():require(path.read_bytes()==raw,'Refusing to change saved assessment '+str(path));return
    path.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(dir=path.parent)
    try:
        with os.fdopen(fd,'wb') as f:f.write(raw)
        os.link(tmp,path)
    finally:os.unlink(tmp)

def generate(directory=PRIVATE,output=None,regenerated_csv=None):
    objects,csv_raw=build(directory);output=Path(output) if output else directory/'phase8'
    artifacts={n:pretty(v) for n,v in objects.items()}
    artifacts['reproducibility.json']=pretty(dict(artifacts={n:digest(raw) for n,raw in artifacts.items()},implementation_sha256=digest(Path(__file__).read_bytes()),approved_csv_sha256=CSV_SHA,independently_regenerated_csv_sha256=digest(csv_raw),imports_phase7_content_functions=False))
    for n,raw in artifacts.items():keep(output/n,raw)
    if regenerated_csv:keep(Path(regenerated_csv),csv_raw)
    return {n:digest(raw) for n,raw in artifacts.items()}

def verify(directory=PRIVATE):
    with tempfile.TemporaryDirectory(prefix='belgium-phase8-independent-') as tmp:
        csv_path=Path(tmp)/'independently_regenerated.csv'
        proc=subprocess.run([sys.executable,'-B',str(Path(__file__).resolve()),'--output',tmp,'--regenerated-csv',str(csv_path)],cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True,timeout=240)
        require(proc.returncode==0,'Independent child regeneration failed: '+proc.stdout+proc.stderr)
        hashes={}
        for n in (*NAMES,'reproducibility.json'):
            a,b=(directory/'phase8'/n).read_bytes(),(Path(tmp)/n).read_bytes();require(a==b,'Assessment bytes differ '+n);hashes[n]=dict(sha256=digest(a),byte_identical=True)
        require(csv_path.read_bytes()==(directory/CSV_NAME).read_bytes(),'Independent regenerated CSV bytes differ')
    return dict(assessments=hashes,independent_csv_sha256=CSV_SHA,protected=preserve(directory))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path);parser.add_argument('--verify',action='store_true');parser.add_argument('--regenerated-csv',type=Path);a=parser.parse_args()
    try:print(json.dumps(verify() if a.verify else generate(output=a.output,regenerated_csv=a.regenerated_csv),indent=2))
    except (ValueError,KeyError,UnicodeError,csv.Error) as exc:
        print(json.dumps(dict(status='BLOCKED',material_inconsistency=str(exc))));sys.exit(2)
