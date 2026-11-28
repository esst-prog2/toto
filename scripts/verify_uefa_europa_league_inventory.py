"""Independent Phase 2 checks against original bytes; no production parser import.

Reconstructs structured/TXT/wiki record boundaries and important fields, checks
HTML candidates/locators and independently proves every identity/event merge.
This is code-independent structural validation, not historical certification.
"""
import argparse
from collections import Counter, defaultdict
from datetime import date,datetime
import csv
import hashlib
import html
import io
import json
import mmap
from pathlib import Path
import re
import tempfile
import unicodedata
import zipfile

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'data/private/europe/europa_league'
PHASE=BASE/'phase2'


def digest(b):return hashlib.sha256(b).hexdigest()
def wire(v):return (json.dumps(v,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
def read_bytes(p):
    with p.open('rb') as stream:
        if p.stat().st_size==0:return b''
        with mmap.mmap(stream.fileno(),0,access=mmap.ACCESS_READ) as view:return bytes(view)
def load(p):return json.loads(read_bytes(p))
def require(ok,msg):
    if not ok:raise ValueError(msg)


def pair(s):
    match=re.search(r'(\d+)\s*[-–:]\s*(\d+)',s or '')
    return [int(x) for x in match.groups()] if match else None


def name(s):
    for a,b in [('Ł','L'),('ł','l'),('Ø','O'),('ø','o'),('đ','d'),('Đ','D'),('ß','ss')]:s=s.replace(a,b)
    normalized=unicodedata.normalize('NFKD',s.lower());letters=''.join(c for c in normalized if not unicodedata.combining(c));tokens=re.findall('[a-z0-9]+',letters)
    prefixes={'fc','fk','sc','nk','ac','as','afc','cf','rsc','ks','sk','ssc','rc','cd','ud','sd','bk','fsv','vfb','vfl'}
    while len(tokens)>1 and tokens[0] in prefixes:tokens=tokens[1:]
    while len(tokens)>1 and tokens[-1] in {'fc','fk','sc','cf','afc'}:tokens=tokens[:-1]
    return ' '.join(tokens)


def html_text(b):
    try:s=b.decode('utf-8-sig')
    except UnicodeDecodeError:s=b.decode('cp1252',errors='replace')
    return '\n'.join(html.unescape(re.sub('<[^>]+>','',line)).replace('\xa0',' ') for line in s.splitlines())


def wikitext_tokens(body):
    # Independent character-depth splitter, retaining nested links/templates.
    splits=[];level=0;link=0;start=0;i=0
    while i<len(body):
        two=body[i:i+2]
        if two=='{{':level+=1;i+=2;continue
        if two=='}}':level-=1;i+=2;continue
        if two=='[[':link+=1;i+=2;continue
        if two==']]':link-=1;i+=2;continue
        if body[i]=='|' and level==0 and link==0:splits.append(body[start:i]);start=i+1
        i+=1
    return splits+[body[start:]]


def wiki_templates(s):
    # Locate only match-bearing template names, then independently balance them.
    out=[]
    for m in re.finditer(r'\{\{(?:[Ff]ootball[_ ]?box|#[Ii]nvoke:[Ff]ootball box|[Tt]wo[Ll]eg[Rr]esult2?)\b',s):
        i=m.start();depth=0
        while i<len(s)-1:
            if s[i:i+2]=='{{':depth+=1;i+=2
            elif s[i:i+2]=='}}':
                depth-=1;i+=2
                if depth==0:out.append((m.start(),i,s[m.start()+2:i-2]));break
            else:i+=1
    return out


def strip_wiki(s):
    s=re.sub(r'<ref\b[^>]*>.*?</ref>','',s,flags=re.S|re.I)
    s=re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]',lambda x:x[2],s)
    s=re.sub(r'\[\[([^\]]+)\]\]',lambda x:x[1],s)
    while re.search(r'\{\{[^{}]*\}\}',s):s=re.sub(r'\{\{[^{}]*\}\}','',s)
    return html.unescape(re.sub('<[^>]+>','',s)).replace("'''",'').replace("''",'').strip()


def raw_checks(freeze,observations,exceptions):
    bysource=defaultdict(list);issues=defaultdict(list)
    for r in observations:bysource[r['source']].append(r)
    for r in exceptions:issues[r['source']].append(r)
    counts={};independent={};html_boundaries={}
    for item in freeze['inputs']:
        raw=read_bytes(BASE/item['path']);require(digest(raw)==item['sha256'] and len(raw)==item['bytes'],'Frozen original differs')
        if item.get('kind')!='fixture':continue
        rows=bysource[item['path']];actual={r['locator']:r for r in rows};expected={};excluded=0
        if item['path'].endswith('.zip'):
            with zipfile.ZipFile(io.BytesIO(raw)) as z:
                require(z.testzip() is None,'Independent archive CRC failed')
                def table(n):return list(csv.DictReader(io.TextIOWrapper(z.open(n),encoding='utf-8-sig',newline='')))
                teams={r['team_id']:r for r in table('teams.csv')};seasons={r['season_id']:r for r in table('seasons.csv')}
                allrows=table('matches.csv')
                for i,f in enumerate(allrows,2):
                    year=int(seasons[f['season_id']]['season'])
                    if f['competition_code'] not in ('EL','ELQ') or not 1990<=year<=2025:excluded+=1;continue
                    loc='matches.csv:row:'+str(i);require(loc in actual,'Lost ZIP fixture row');r=actual[loc]
                    require(r['season']==f'{year}/{year+1}' and r['date']==f['local_date'],'ZIP season/date differs')
                    require(r['raw_home']==teams[f['home_team_id']]['name'] and r['raw_away']==teams[f['away_team_id']]['name'],'ZIP participant differs')
                    for key,value in f.items():require(r['source_fields'][key]==value,'ZIP raw field differs')
                    def score(a,b):return [int(f[a]),int(f[b])] if f[a] and f[b] else None
                    pp=r['periods'];pub=score('home_goals','away_goals');reg=score('home_goals_regular_time','away_goals_regular_time')
                    if reg is None and f['extra_time_played']=='0' and f['status']=='played' and not f['shootout_home_goals']:reg=pub
                    require(pp['regulation_time']==reg and pp['published_final']==pub,'ZIP regulation basis differs')
                    require(pp['shootout']==score('shootout_home_goals','shootout_away_goals') and pp['half_time']==score('home_goals_half_time','away_goals_half_time'),'ZIP auxiliary periods differ')
                    require(pp['after_extra_time']==(pub if f['extra_time_played']=='1' and f['status']=='played' else None),'ZIP ET differs')
                    require(pp['administrative_result']==(pub if f['status']=='awarded' else None),'Award treated as played regulation')
                    require(r['source_neutral_venue']==(f['neutral_venue'] if f['neutral_venue'] else None),'Provider neutrality changed')
                    expected[loc]=r
        elif item['path'].endswith('.parquet'):
            import pyarrow.parquet as pq
            source=pq.read_table(io.BytesIO(raw)).to_pylist()
            for i,f in enumerate(source):
                d=f['date'];year=d.year-(d.month<6)
                if f['competition']!='UEFA EL' or year<1990 or year>2025:excluded+=1;continue
                loc=f'parquet:row:{i}';require(loc in actual,'Lost relevant parquet row');r=actual[loc]
                for key,value in f.items():require(r['source_fields'][key]==(str(value) if isinstance(value,date) else value),'Parquet original field differs')
                require(r['date']==str(d),'Parquet date differs')
                for side in ('home','away'):
                    label=f[side] or (f.get(side+'_ident') or '').rsplit(' (',1)[0]
                    require(r[side]==label,'Parquet source label/identifier differs')
                pub=[int(f['gh']),int(f['ga'])] if f['gh'] is not None and f['ga'] is not None else None
                require(r['periods']['published_final']==pub and r['periods']['regulation_time']==(pub if f['full_time']=='F' else None),'Parquet E/P conflated with regulation')
                require(r['periods']['after_extra_time']==(pub if f['full_time']=='E' else None),'Parquet extra-time duration result differs')
                expected[loc]=r
        elif 'goals_time' in item['path']:
            groups=defaultdict(list)
            for i,f in enumerate(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'),newline='')),2):groups[(f['game'],f['date'],f['season'])].append((i,f))
            for key,items in groups.items():
                loc='csv:rows:'+','.join(str(i) for i,_ in items);require(loc in actual,'Lost goal-log group');r=actual[loc];game,d,season=key
                require(r['date']==d and r['season']==season[:4]+'/'+str(int(season[:4])+1),'Goal context date/season differs')
                match=re.match(r'(.*?) vs\. (.*?) (\d+):(\d+)',game,re.S);require(match is not None,'Independent goal header unsupported')
                require([r['home'],r['away']]==[match[1],match[2]],'Goal context labels differ')
                require(r['periods']['published_final']==[int(match[3]),int(match[4])] and r['periods']['regulation_time'] is None,'Goal log wrongly supplies regulation')
                require(r['source_fields']['goal_rows']==[dict(row=i,**f) for i,f in items],'Goal events lost')
                expected[loc]=r
        elif '/openfootball/' in item['path']:
            # Independent named-period decoder from the earlier UCL verifier,
            # never the production grammar shared by the new adapter.
            from scripts.verify_uefa_champions_league_inventory import text_scores
            heading='';day=None;year=int(Path(item['path']).parent.name[:4]);date_heading=''
            for i,line in enumerate(raw.decode('utf-8-sig').splitlines(),1):
                s=line.strip()
                if not s or s[0] in '#=':continue
                if s.startswith('▪'):heading=s[1:].strip();day=None;continue
                if s[:3] in ('Mon','Tue','Wed','Thu','Fri','Sat','Sun') and ' v ' not in s:
                    words=s.split();years=[int(words[3])] if len(words)==4 else [year,year+1];matches=[]
                    for y in years:
                        candidate=datetime.strptime(f'{words[1]} {words[2]} {y}','%b %d %Y').date()
                        if date(year,6,1)<=candidate<=date(year+1,8,31) and candidate.strftime('%a')==words[0]:matches.append(str(candidate))
                    day=matches[0] if len(matches)==1 else None;date_heading=s;continue
                loc=f'line:{i}';require(loc in actual,'Lost TXT candidate');r=actual[loc]
                body=re.sub(r'^\d\d?:\d\d\s+','',s);h,tail=body.split(' v ',1);sep=re.search(r'\([A-Z]{3}\)(?=\s)',tail)
                require(sep is not None,'Independent TXT boundary missing');away=tail[:sep.end()].strip();scoretext=tail[sep.end():].strip()
                require(r['home']==re.sub(r'\s+\([A-Z]{3}\)$','',h.strip()).strip() and r['away']==re.sub(r'\s+\([A-Z]{3}\)$','',away),'TXT names differ')
                require(r['date']==day and r['raw_stage']==heading,'TXT heading differs');pp=text_scores(scoretext)
                # Annotated administrative trailers require preserving the pair
                # as unassigned, as opposed to verifier's ordinary-score branch.
                if '[' in scoretext or any(t in scoretext.lower() for t in ('award','abandon')):
                    require(r['periods']['regulation_time'] is None,'Annotated TXT score promoted')
                else:
                    for k in ('regulation_time','half_time','after_extra_time','shootout'):require(r['periods'][k]==pp[k],'TXT named period differs: '+k)
                expected[loc]=r
        elif '/wikipedia/' in item['path']:
            page=json.loads(raw)['query']['pages'][0];rev=page['revisions'][0];s=rev['slots']['main']['content']
            for start,end,body in wiki_templates(s):
                tokens=wikitext_tokens(body);typ=tokens[0].lower();loc=f'revision:{rev["revid"]}:chars:{start}:{end}'
                if 'football' in typ:
                    f={p.split('=',1)[0].strip().lower():p.split('=',1)[1].strip() for p in tokens[1:] if '=' in p}
                    if not {'team1','team2','score'}<=set(f):continue
                    require(loc in actual,'Lost Wikipedia box');r=actual[loc]
                    require(r['source_fields']['fields']==f and r['source_fields']['wikitext']==s[start:end],'Wikipedia box raw field/span differs')
                    require([r['home'],r['away']]==[strip_wiki(f['team1']),strip_wiki(f['team2'])],'Wikipedia team labels differ')
                    require(r['periods']['published_final']==pair(f['score']),'Wikipedia printed score differs')
                    require(r['periods']['regulation_time'] is None,'Wikipedia final silently promoted to regulation')
                    expected[loc]=r
                else:
                    pos=[t for t in tokens[1:] if not re.match(r'^\s*[A-Za-z0-9_]+\s*=',t)]
                    if len(pos)<7:continue
                    for leg in (1,2):
                        key=loc+f':leg:{leg}';require(key in actual,'Lost Wikipedia tie leg');r=actual[key];h,a=(pos[0],pos[3]) if leg==1 else (pos[3],pos[0]);score=pair(pos[4+leg]);score=score if leg==1 or score is None else score[::-1]
                        require([r['home'],r['away']]==[strip_wiki(h),strip_wiki(a)] and r['periods']['published_final']==score,'Wikipedia tie orientation/score differs')
                        require(r['source_fields']['wikitext']==s[start:end],'Wikipedia tie span differs');expected[key]=r
        elif '/rsssf/' in item['path']:
            lines=html_text(raw).splitlines()
            # Every HTML observation must point to exact original text and named
            # competition anchors; all unsupported candidates retain raw spans.
            for r in rows:
                m=re.match(r'line:(\d+)',r['locator']);require(m is not None,'HTML locator missing');n=int(m[1]);require(1<=n<=len(lines),'HTML locator out of bounds')
                require('uefa' in raw.decode('latin1').lower(),'Wrong competition content')
                f=r['source_fields'];original_line=lines[n-1]
                require(not re.match(r'^.+?\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s*[-–]\s*\d+\s+\d+\s*$',original_line.strip()),'Standings row parsed as a fixture')
                supplied=f.get('raw_line',f.get('header'))
                if supplied is not None:require(supplied.strip()==original_line.strip(),'HTML original locator/text differs')
                if ':leg:' in r['locator']:
                    first_score=re.search(r'\bawd\b|(?<!\d)[*]?\d+-\d+[a-z*]?',original_line)
                    prefix=original_line[:first_score.start()].rstrip()
                    last_code=re.search(r'([A-Za-z]{3})\*?$',prefix);require(last_code is not None,'Grid second association absent')
                    names_prefix=prefix[:last_code.start()]
                    vocabulary='Eng Sco Wal Nir Nil Ire Irl Ned Net Ger FRG GDR Aut Sui Ita Fra Esp Por Bel Den Nor Swe Fin Fni Isl Ice Far Pol Tch Cze Svk Hun Hon Rom Rou Bul Gre Grk Tur URS Rus Ukr Bls Blr Est Lat Lva Lit Ltu Mol Mda Geo Arm Aze Azb Isr Cyp Mlt Mal Lie Lux And SMa SMr SMR Gib Kaz Mac Mkd Alb Bos BiH Bih Cro Slo Sln Ser Srb SeM Yug Mng Mne Mon Kos'.split()
                    first_code=re.search(r'(?<![A-Za-z])('+'|'.join(vocabulary)+r')\*?\s+',names_prefix,re.I)
                    if first_code is None:
                        # Fixed-width long names can touch the capitalized code,
                        # e.g. a city suffix immediately followed by Est.
                        first_code=re.search('('+'|'.join(vocabulary)+r')\*?\s+',names_prefix)
                    require(first_code is not None,'Grid first association absent')
                    participants=[names_prefix[:first_code.start()].strip(' *+\t'),names_prefix[first_code.end():].strip(' *+\t')]
                    if r['locator'].endswith(':2'):participants.reverse()
                    require([r['home'],r['away']]==participants,'Independent HTML grid participant differs')
                    score_tokens=re.findall(r'\bawd\b|(?<!\d)\d+-\d+[a-z*]?',original_line);plain_scores=[p for p in score_tokens if not p.endswith('p')];leg=int(r['locator'].rsplit(':',1)[1]);v=pair(plain_scores[leg-1]);v=v[::-1] if leg==2 and v is not None else v
                    require(r['periods']['published_final']==v,'HTML leg score/orientation differs')
                    if len(plain_scores)>=3:
                        aggregate=pair(plain_scores[2]);require(r['periods']['aggregate']==(aggregate if leg==1 else aggregate[::-1]),'HTML aggregate mixed with leg')
                elif f.get('header'):
                    scores=re.search(r'(\d+)\s*[-–]\s*(\d+)(?:\D|$)',original_line);require(scores is not None,'Detail header has no score');require(r['periods']['published_final']==[int(x) for x in scores.groups()],'Detail printed score differs')
                else:
                    content=re.sub(r'^[A-Z][a-z]{2}\s+\d{1,2}:\s*','',original_line.strip())
                    half=list(re.finditer(r'\((\d+|-)\)\s*(\d+)',content))
                    if len(half)==2:
                        home=content[:half[0].start()].strip();away=content[half[0].end():half[1].start()].strip()
                        require([r['home'],r['away']]==[home.strip(' *+\t'),away.strip(' *+\t')],'HTML half-score participant boundary differs')
                        require(r['periods']['published_final']==[int(m[2]) for m in half],'HTML final score differs')
                        hh=[int(m[1]) for m in half] if all(m[1].isdigit() for m in half) else None
                        require(r['periods']['half_time']==hh,'HTML half-time values differ')
                    elif ':pair' in r['locator']:
                        first=re.match(r'^(.+?)\s+(\d+)(?:\s+\(.*)?$',original_line.strip());second=re.match(r'^(.+?)\s+(\d+)(?:\s+\(.*)?$',lines[n].strip())
                        require(first is not None and second is not None and r['periods']['published_final']==[int(first[2]),int(second[2])],'HTML report pair differs')
                    else:
                        simple=re.match(r'^(.+?)\s{2,}(\d+)\s{2,}(.+?)\s{2,}(\d+)',content)
                        require(simple is not None and r['periods']['published_final']==[int(simple[2]),int(simple[4])],'HTML bare group result differs')
                require(r['periods']['regulation_time'] is None,'HTML printed score promoted without evidence')
                expected[r['locator']]=r
            # Full independent scan of target sections counts score-like physical
            # lines against parsed headers + explicit exception/context coverage.
            covered={int(re.search(r'line:(\d+)',r['locator'])[1]) for r in rows}
            covered|={int(re.search(r'line:(\d+)',x['locator'])[1]) for x in issues[item['path']] if re.search(r'line:(\d+)',x['locator'])}
            try:markup=raw.decode('utf-8-sig')
            except UnicodeDecodeError:markup=raw.decode('cp1252',errors='replace')
            candidates=set()
            detail='det.html' in item['path']
            anchors=['uefaqdet','uefadet'] if detail else ['uefa']
            for anchor in anchors:
                anchor_match=re.search(r'<a\b[^>]*(?:name|id)\s*=\s*["\']?'+anchor+r'(?:["\']|\s|>)',markup,re.I)
                if anchor_match is None:continue
                end_heading=re.search(r'<h[123]\b' if detail else r'<h2\b',markup[anchor_match.end():],re.I)
                stop=anchor_match.end()+end_heading.start() if end_heading else len(markup)
                first=markup[:markup.rfind('\n',0,anchor_match.start())+1].count('\n')+1
                last=markup[:stop].count('\n')+1
                for line_number in range(first,min(last,len(lines))+1):
                    value=lines[line_number-1].strip()
                    if not detail:
                        if re.match(r'^[A-Z][a-z]{2}\s+\d{1,2}:',value) or len(re.findall(r'\(\d+\)\s*\d+',value))==2 or re.search(r'\s[A-Za-z]{3}\s{2,}.+[A-Za-z]{3}\s+[*]?(?:\d+-\d+|w/o)',value):candidates.add(line_number)
                    elif re.match(r'^.+?\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s*[-–]\s*\d+\s+\d+\s*$',value):continue
                    elif ':' not in value and not re.match(r"^\d+(?:\+\d+)?['’]",value):
                        head=re.match(r'^(.+?)\s+(\d+)\s*[-–]\s*(\d+)',value)
                        if head and re.search('[-–]',head[1]) and ',' not in head[1] and not re.search(r'\d+\s*[-–]\s*\d+',head[1]):candidates.add(line_number)
            # A two-leg grid must contribute both leg observations, not just
            # one covered physical line. Contextual no-play ties stay exceptions.
            for n in sorted(candidates):
                existing=[r for r in rows if r['locator'].startswith(f'line:{n}:leg:')]
                if not existing:continue
                tokens=re.findall(r'\bawd\b|(?<!\d)\d+-\d+[a-z*]?',lines[n-1]);published=[t for t in tokens if not t.endswith('p')]
                required={f'line:{n}:leg:{i}' for i in ((1,2) if len(published)>=3 else (1,))}
                require({r['locator'] for r in existing}==required,'Incomplete independently reconstructed HTML leg population')
            missing=sorted(candidates-covered)
            require(not missing,'Independent HTML candidate not accounted: '+item['path']+' lines '+str(missing[:10]))
            html_boundaries[item['path']]=dict(parsed_locators=len(expected),covered_scored_context_lines=len(covered),independently_detected_candidate_lines=len(candidates),unaccounted_candidate_lines=missing,exception_records=len(issues[item['path']]),method='Independent original physical-line and score orientation checks; unparsed contextual lines retained in source accounting')
        else:raise ValueError('Unaccounted fixture payload: '+item['path'])
        for x in issues[item['path']]:
            require(x['source_sha256']==item['sha256'] and x['exception_id']==digest(wire([item['sha256'],x['locator'],x['code']])),'Non-event record provenance differs')
            if x['locator'].startswith('line:') and isinstance(x['raw'],str) and '/rsssf/' in item['path']:
                line_number=int(x['locator'].split(':')[1]);require(html_text(raw).splitlines()[line_number-1].strip()==x['raw'].strip(),'Non-event original text differs')
            if x['code']=='HISTORICAL_SCORE_CONTEXT':
                require(x['reported_score']==pair(x['raw']) and x['score_period']=='UNKNOWN_NOT_ASSUMED_REGULATION','Original score note conflated with regulation')
        require(set(actual)==set(expected),'Source candidate population differs: '+item['path'])
        counts[item['path']]=dict(observations=len(expected),excluded_records=excluded,exceptions=len(issues[item['path']]))
        independent.update({r['observation_id']:r for r in expected.values()})
    for r in observations:
        require(r['observation_id']==digest(wire([r['source_sha256'],r['locator']])),'Observation ID/provenance differs')
    return counts,independent,html_boundaries


def verify(inventory):
    original=load(inventory/'source_inventory.json');rows=original['observations'];byid={r['observation_id']:r for r in rows};require(len(byid)==len(rows),'Duplicate observation ID')
    counts,reconstructed,html_checks=raw_checks(load(inventory/'input_freeze.json'),rows,original['exceptions']);require(set(reconstructed)==set(byid),'Independent raw accounting incomplete')
    names=load(inventory/'team_identity_inventory.json');parents={}
    def root(x):
        x=tuple(x);parents.setdefault(x,x)
        while parents[x]!=x:x=parents[x]
        return x
    for r in rows:
        require(r['team_candidates']==[name(r[s]) for s in ('home','away')],'Independent lexical candidate differs')
    for proof in names['nontrivial_correspondences']:
        x,z=root(proof['left']),root(proof['right']);signatures=set()
        require(x!=z,'Redundant identity proof')
        for aid,bid in proof['evidence']:
            a,b=byid[aid],byid[bid];require(a['season']==b['season'] and a['source']!=b['source'],'Identity proof not across distinct source files in one season')
            aa=[root((a['season'],name(a[s]))) for s in ('home','away')];bb=[root((b['season'],name(b[s]))) for s in ('home','away')]
            choices=[]
            for flip in (False,True):
                bs=bb[::-1] if flip else bb
                for side in (0,1):
                    if aa[1-side]==bs[1-side] and {aa[side],bs[side]}=={x,z}:choices.append((side,flip,aa[1-side]))
            require(choices,'Identity proof has no established shared opponent')
            if a['date'] and b['date']:
                require(a['date']==b['date'],'Identity proof dates conflict');signatures.add((a['date'],choices[0][2]))
            else:
                undated=a if not a['date'] else b
                require(undated['source_leg'] is not None and a['periods']['published_final']==b['periods']['published_final'],'Undated identity lacks paired-leg support')
                signatures.add(((a['date'] or b['date']),choices[0][2]))
        distinct_days={signature[0] for signature in signatures}
        if len(distinct_days)<2:
            first=set(proof['left'][1].split());second=set(proof['right'][1].split());generic={'club','united','city','real','athletic','dinamo','dynamo','sporting','sport','olympic','inter','cska','rapid'}
            require(proof['method']=='SINGLE_FIXTURE_DATE_OPPONENT_AND_CORE_NAME' and len(signatures)==1 and bool((first&second)-generic) and (first<=second or second<=first) and not str(next(iter(signatures))[0]).startswith('leg'),'Identity correspondence lacks corroborated name/date/opponent evidence')
        low,high=sorted([x,z]);parents[high]=low
    mapping={}
    for item in names['labels']:
        node=root((item['season'],name(item['original_label'])));require(item['identity_root']==list(node),'Identity root differs')
        require(item['identity_candidate']==digest(wire(node)),'Identity candidate digest differs')
        mapping[(item['season'],item['publisher'],item['original_label'])]=item['identity_candidate']
    for r in rows:require(r['identity_candidates']==[mapping[(r['season'],r['publisher'],r[s])] for s in ('home','away')],'Observation identity not proven')
    events=load(inventory/'event_inventory.json')['events'];membership=Counter(i for e in events for i in e['observations']);require(set(membership)==set(byid) and set(membership.values())=={1},'Event accounting loses or duplicates observations')
    event_by_observation={i:e['event_id'] for e in events for i in e['observations']};exact=defaultdict(set)
    for r in rows:
        if r['date']:exact[(r['season'],tuple(sorted(r['identity_candidates'])),r['date'],r['replay'])].add(event_by_observation[r['observation_id']])
    require(all(len(v)==1 for v in exact.values()),'Identical date/pair candidate split across events')
    for e in events:
        members=[byid[i] for i in e['observations']];require(e['event_id']==digest(wire(sorted(e['observations']))),'Conditional event ID differs')
        require(len({r['season'] for r in members})==1 and len({tuple(sorted(r['identity_candidates'])) for r in members})==1,'Unsupported participant/season merge')
        require(e['date_candidates']==sorted({r['date'] for r in members if r['date']}),'Event dates differ')
        for field,values in e['score_evidence'].items():
            expected=defaultdict(list)
            for r in members:
                p=r['periods'][field]
                if p is not None:expected[tuple(p if r['identity_candidates']==e['identity_candidates'] else p[::-1])].append(r['observation_id'])
            require(values==[dict(value=list(p),observations=sorted(ids)) for p,ids in sorted(expected.items())],'Event period comparison mixes periods/orientation')
        positive=[r for r in members if r['periods']['after_extra_time'] is not None]
        negative=[r for r in members if r['source_fields'].get('full_time')=='F' or (r['source_fields'].get('extra_time_played')=='0' and r['status']=='played' and not r['source_fields'].get('shootout_home_goals'))]
        require(('DURATION_CONFLICT' in e['flags'])==bool(positive and negative),'Contradictory explicit duration claims not isolated')
        if positive and negative:require('REGULATION_SCORE_UNRESOLVED'in e['flags'],'Duration conflict silently accepted as settled regulation')
        require(not e['dispositions_assigned'],'Unauthorized historical decision')
    coverage=load(inventory/'structural_validation.json')['season_coverage'];require(len(coverage)==36,'Incomplete seasons')
    for year,c in zip(range(1990,2026),coverage,strict=True):
        season=f'{year}/{year+1}';rr=[r for r in rows if r['season']==season];ee=[e for e in events if e['season']==season]
        require(c['season']==season and c['parsed_observations']==len(rr) and c['conditional_events']==len(ee),'Independent season totals differ')
        require(c['main_events']==sum(e['scope']=='MAIN' for e in ee) and c['qualifying_events']==sum(e['scope']=='QUALIFYING' for e in ee),'Scope counts differ')
        if year<1994:require(not c['qualifying_applicable'] and not any(r['scope']=='QUALIFYING' for r in rr),'Early competition format misclassified')
    csv_path=inventory/'season_coverage.csv'
    if csv_path.exists():
        csv_coverage=list(csv.DictReader(io.StringIO(read_bytes(csv_path).decode('utf-8'))))
        require(len(csv_coverage)==36,'CSV coverage does not contain 36 seasons')
        for left,right in zip(csv_coverage,coverage,strict=True):
            require(left['season']==right['season'] and int(left['parsed_observations'])==right['parsed_observations'] and int(left['conditional_events'])==right['conditional_events'],'CSV matrix differs from independently recounted population')
    format_checks=[]
    for year in range(1990,1994):
        selected=[r for r in rows if r['source'].endswith(f'ec{year}{(year+1)%100:02}.html') and r['raw_stage'].startswith('First Round')]
        if selected:
            require(len(selected)==64 and len({r[side] for r in selected for side in ('home','away')})==64,'Early 64-club first-round bracket does not reconcile')
            format_checks.append(dict(season=f'{year}/{year+1}',check='64_CLUB_TWO_LEG_FIRST_ROUND_WITH_NO_PRIOR_TARGET_STAGE',observations=64))
    league=defaultdict(list)
    for r in rows:
        if r['publisher']=='11footy' and r['raw_stage']=='league phase':league[r['season']].append(r)
    for season,group in league.items():
        played=Counter(r['source_fields'][side+'_team_id'] for r in group for side in ('home','away'));home=Counter(r['source_fields']['home_team_id'] for r in group);away=Counter(r['source_fields']['away_team_id'] for r in group)
        require(len(group)==144 and len(played)==36 and set(played.values())=={8} and set(home.values())=={4} and set(away.values())=={4},'Independent league-phase topology differs')
        format_checks.append(dict(season=season,check='36_CLUBS_EIGHT_OPPONENTS_FOUR_HOME_FOUR_AWAY',observations=144))
    for change in names['source_season_reassignments']:
        r=byid[change['observation']];require(r['season']==change['after'],'Season reassignment not applied consistently')
        evidence=[byid[oid] for oid in change['evidence']]
        require(evidence and all(q['date']==r['date'] and q['season']==r['season'] and set(q['team_candidates'])&set(r['team_candidates']) for q in evidence),'Season assignment lacks source-date-participant evidence')
    queue=load(inventory/'review_queue.json')['cases'];queueevents={q['event_id'] for q in queue};required={'DATE_CONFLICT','DATE_UNRESOLVED','STAGE_CONFLICT','STAGE_UNRESOLVED','REGULATION_SCORE_UNRESOLVED','EXCEPTIONAL_STATUS','SOURCE_ORIENTATION_CONFLICT','VENUE_REVIEW','SOURCE_LEG_OR_SCHEDULE_CONFLICT','DURATION_CONFLICT'}
    require(all(e['event_id'] in queueevents for e in events if set(e['flags'])&required or any(f.startswith('SCORE_CONFLICT') for f in e['flags'])),'Material event not in review queue')
    summary=load(inventory/'summary.json');require(summary['observations']==len(rows) and summary['conditional_events']==len(events) and summary['canonical_records_generated']==0,'Summary/phase boundary differs')
    return dict(status='PASS',source_files=len(counts),original_payloads_verified=len(load(inventory/'input_freeze.json')['inputs']),observations=len(rows),conditional_events=len(events),independently_checked_identity_correspondences=len(names['nontrivial_correspondences']),all_observations_accounted_once=True,independent_format_checks=format_checks,source_counts=counts,html_checks=html_checks,limitations='HTML verification independently checks original locators, scores and orientation; it is not an independently researched historical truth. Alias proofs independently checked; upstream independence unestablished.',network_requests=0)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--inventory',type=Path,default=PHASE/'validated');p.add_argument('--output',type=Path);args=p.parse_args();result=verify(args.inventory)
    if args.output:
        resolved=args.output.resolve();require(resolved.is_relative_to(PHASE.resolve()) or resolved.is_relative_to(Path(tempfile.gettempdir()).resolve()),'Independent output must remain private/temporary');args.output.parent.mkdir(parents=True,exist_ok=True)
        with args.output.open('xb') as f:f.write(wire(result))
    print(json.dumps({k:v for k,v in result.items() if k not in ('source_counts','html_checks')},indent=2))
