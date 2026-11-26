"""One approved RSSSF 2021/22 documentary recovery; no historical policy."""
from collections import Counter,defaultdict
from datetime import date,datetime,timezone
from html import unescape
from pathlib import Path
from urllib.request import Request,build_opener,HTTPRedirectHandler
from unittest.mock import patch
import csv,io,json,re,os,tempfile,subprocess,hashlib,sys
from scripts import validate_belgian_pro_league_structure as structural
from scripts.collect_belgian_pro_league_feasibility import save,keep

ROOT,PRIVATE=structural.ROOT,structural.PRIVATE
URL='https://www.rsssf.org/tablesb/belg2022.html'
PATH='rsssf/tablesb/belg2022.html'
NAMES=('documentary_inventory.json','event_registry.json','historical_comparison.json','coverage_provenance.json')
sha,encode=structural.sha,structural.encode


def protect(directory=PRIVATE):
    previous=structural.protect(directory);baseline=json.loads((directory/'recovery2021_protected_before.json').read_text())
    for name,h in baseline['files'].items():
        if sha((ROOT/name).read_bytes())!=h:raise ValueError('Frozen recovery baseline changed: '+name)
    p=baseline['planning_log'];log=(ROOT/'PLANNING_LOG.md').read_bytes()
    if sha(log[:p['bytes']])!=p['sha256']:raise ValueError('Planning prefix changed')
    return dict(previous=previous,frozen_entries=len(baseline['files']))


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):raise ValueError('Redirect not authorized')


def request(url):
    if url!=URL:raise ValueError('Unapproved original URL')
    with build_opener(NoRedirect).open(Request(url,headers={'User-Agent':'ThePickSheet-Belgium-one-page-academic-recovery'}),timeout=30) as response:
        if response.status!=200 or response.url!=URL or response.headers.get('Retry-After'):raise ValueError('Restricted response')
        raw=response.read(2000001)
        if len(raw)>2000000:raise ValueError('Response exceeds bound')
        return raw,dict(final_url=response.url,status=response.status,headers=dict(response.headers.items()))


def verify_original(directory=PRIVATE):
    raw=(directory/PATH).read_bytes();r=json.loads((directory/(PATH+'.provenance.json')).read_text())
    if r['url']!=URL or r['final_url']!=URL or r['original_path']!=PATH or r['bytes']!=len(raw) or r['sha256']!=sha(raw):raise ValueError('Original/receipt differs')
    if r['git_commit'] is not None or r['git_blob'] is not None:raise ValueError('Web document cannot claim Git identity')
    raw.decode(r['encoding'])
    return raw,r


def collect(directory=PRIVATE):
    protect(directory);dest=directory/PATH;receipt=directory/(PATH+'.provenance.json');stop=directory/'recovery2021_ACCESS_STOP.json'
    if dest.exists()!=receipt.exists():raise ValueError('Partial source/receipt pair')
    if dest.exists():return verify_original(directory)[1]
    if stop.exists():raise ValueError('Prior failure; no retry or bypass')
    try:raw,response=request(URL)
    except Exception as e:
        save(stop,encode(dict(url=URL,error=str(e),retrieved_at_utc=datetime.now(timezone.utc).isoformat())));raise
    encoding='utf-8-sig'
    try:text=raw.decode(encoding)
    except UnicodeDecodeError:encoding='iso-8859-1';text=raw.decode(encoding)
    clean=unescape(re.sub('<[^>]+>',' ',text));notices=clean[clean.lower().rfind('about this document'):].strip()
    if not all(x in clean for x in ('Hans Schöggl','Karel Stokkermans')) or not re.search(r'free to copy.*?acknowledg',clean,re.I|re.S):raise ValueError('Expected copying/author conditions not established')
    title=re.search(r'<title>(.*?)</title>',text,re.I|re.S)
    rec=dict(url=URL,final_url=response['final_url'],response=response,original_path=PATH,original_filename='belg2022.html',retrieved_at_utc=datetime.now(timezone.utc).isoformat(),bytes=len(raw),sha256=sha(raw),encoding=encoding,title=title[1] if title else None,authors=['Hans Schöggl','Karel Stokkermans'],attribution='Hans Schöggl, Karel Stokkermans and RSSSF',copyright_and_usage_notice=notices,git_commit=None,git_blob=None,limits='One bounded original, no retries/redirects/substitutes; copying with acknowledgement; independent lineage, commercial/redistribution scope and model-training clearance not established')
    save(dest,raw);save(receipt,encode(rec));verify_original(directory);return rec


def parse_document(raw,rec):
    if sha(raw)!=rec['sha256']:raise ValueError('Document checksum differs')
    physical=raw.splitlines(keepends=True);lines=raw.decode(rec['encoding']).splitlines();stage=None;round_id=None;leg=None;current=None;date_line=None;inside=False;rows=[];headings=[];pending=None
    stage_names={'reg':'REGULAR','po1':'CHAMPIONSHIP','po2':'EUROPE','prorel':'PROMOTION_RELEGATION'}
    for number,literal in enumerate(lines,1):
        if re.search(r'<h4>.*name="pro"',literal,re.I):inside=True
        elif re.search(r'<h4>',literal,re.I):inside=False;stage=None
        if not inside:continue
        for anchor,name in stage_names.items():
            if re.search(r'<a name="'+anchor+r'">',literal,re.I):stage=name;round_id=None;leg=None;current=None;headings.append(dict(line=number,stage=name,raw_html=literal))
        text=unescape(re.sub('<[^>]*>','',literal)).strip()
        if stage is None:continue
        rnd=re.match(r'Round (\d+)',text)
        lg=re.match(r'(First|Second) Leg',text)
        if rnd:round_id=int(rnd[1]);leg=None;current=None
        if lg:leg=1 if lg[1]=='First' else 2;round_id=None;current=None
        dm=re.search(r'\[([A-Z][a-z]{2}) (\d{1,2})\]',text)
        if dm:
            import calendar
            if dm[1] not in calendar.month_abbr:raise ValueError('Unknown month')
            month=list(calendar.month_abbr).index(dm[1]);y=2021 if month>=7 else 2022
            current=date(y,month,int(dm[2])).isoformat();date_line=number
        if not text or not text[0].isalpha() or text.startswith(('NB:','Final Table:','Round ','First Leg','Second Leg','Playoff ','Regular Stage','Promotion/Relegation')):continue
        # Parse alignment before HTML entity decoding to preserve source spellings.
        plain=re.sub('<[^>]*>','',literal).strip()
        m=re.fullmatch(r'(.+?)\s{2,}(\d+-\d+|abd|awd|n/p)\s+(.+)',plain)
        if not m:
            if re.search(r'\s{2,}(?:\d+[-:]\?|\?[-:]\d+|\d+-\d+)',plain):raise ValueError(f'Malformed documentary fixture at {number}')
            if pending is not None:
                rows[pending]['annotation_parts'].append(dict(line=number,text=text))
                if ']' in text:pending=None
            continue
        if current is None or (round_id is None and leg is None):raise ValueError('Fixture lacks dated stage/round/leg')
        home_html,score,tail=m.groups();parts=re.split(r'\s{2,}',tail,maxsplit=1);away_html=parts[0];trailing=unescape(parts[1]) if len(parts)>1 else ''
        # A bracketed note may start after a single space following the away label.
        single=re.search(r'\s+(\[.*)$',away_html)
        if single:trailing=unescape(single[1])+(' '+trailing if trailing else '');away_html=away_html[:single.start()]
        note='';foreign=None
        if trailing.startswith('['):note=trailing
        elif trailing:
            if pending is None:raise ValueError('Unbound trailing documentary note: '+trailing)
            foreign=pending;rows[pending]['annotation_parts'].append(dict(line=number,text=trailing))
            if ']' in trailing:pending=None
        source_id=sha(encode([rec['sha256'],number,'RSSSF_2021_RECOVERY']))
        rows.append(dict(source_id=source_id,source=PATH,source_sha256=rec['sha256'],source_line=number,source_line_sha256=sha(physical[number-1]),raw_html=literal,season='2021/2022',stage=stage,round=round_id,leg=leg,home=unescape(home_html),away=unescape(away_html),home_html=home_html,away_html=away_html,date=current,date_heading_line=date_line,date_basis='EXPLICIT_DAY_MONTH_WITH_SEASON_YEAR_CONTEXT',date_semantics='DOCUMENTARY_EVENT_CONTEXT_NOT_CERTIFIED_AVAILABILITY',score_token=score,annotation_parts=[dict(line=number,text=note)] if note else [],trailing_note_belongs_to_source_id=rows[foreign]['source_id'] if foreign is not None else None))
        if note and ']' not in note:pending=len(rows)-1
    if pending is not None:raise ValueError('Unclosed documentary annotation')
    if not rows:raise ValueError('No First Division A fixtures')
    for r in rows:
        r['annotation']=' '.join(p['text'] for p in r['annotation_parts'])
        r['numeric_score']=r['score_token'] if re.fullmatch(r'\d+-\d+',r['score_token']) else None
        award=re.search(r'awarded (\d+-\d+)',r['annotation'],re.I)
        r['reported_award_score']=award[1] if r['score_token']=='awd' and award else None
        r['representation_kind']='INITIAL_INTERRUPTION' if r['score_token']=='abd' else 'REPORTED_ADMINISTRATIVE_AWARD' if r['score_token']=='awd' else 'CONTINUATION_RESULT' if re.search(r'remaining|second half',r['annotation'],re.I) else 'NUMERIC_REPORTED_RESULT' if r['numeric_score'] else 'OTHER_MARKER'
    return rows,headings


def group_events(rows):
    by=defaultdict(list)
    for r in rows:by[(r['season'],r['stage'],r['round'],r['leg'],r['home'],r['away'])].append(r)
    events=[]
    for key,observations in sorted(by.items(),key=lambda x:repr(x[0])):
        initial=[r for r in observations if r['representation_kind']=='INITIAL_INTERRUPTION'];terminal=[r for r in observations if r['numeric_score'] or r['reported_award_score']]
        linked=len(initial)==1 and len(terminal)==1 and terminal[0]['representation_kind']=='CONTINUATION_RESULT'
        ambiguous=len(terminal)!=1 or (len(observations)>1 and not linked)
        chosen=terminal[0] if not ambiguous else None
        events.append(dict(diagnostic_event_key=list(key),source_ids=[r['source_id'] for r in observations],representations=observations,explicit_continuation_group=linked,ambiguous=ambiguous,reported_result_source_id=chosen['source_id'] if chosen else None,comparison_score=(chosen['numeric_score'] or chosen['reported_award_score']) if chosen else None,comparison_date=chosen['date'] if chosen else None,initial_dates=[r['date'] for r in initial],status='DOCUMENTARY_CANDIDATE_NOT_FINAL_HISTORICAL_ADJUDICATION'))
    return events


def historical(directory=PRIVATE):
    rec=json.loads((directory/'acquisition.json').read_text())['files'][0];raw=(directory/rec['path']).read_bytes()
    if sha(raw)!=rec['sha256']:raise ValueError('Historical original changed')
    reader=csv.DictReader(io.StringIO(raw.decode('utf-8-sig'),newline=''));physical=raw.splitlines(keepends=True);rows=[]
    if tuple(reader.fieldnames)!=structural.COLUMNS:raise ValueError('Historical schema differs')
    while True:
        start=reader.line_num+1
        try:r=next(reader)
        except StopIteration:break
        if r['Season']!='2021':continue
        if r['division']!='B1' or r['tier']!='1':raise ValueError('Wrong historical competition')
        rows.append(dict(source_id=structural.sid(rec['sha256'],start,reader.line_num),source=rec['path'],source_sha256=rec['sha256'],source_line=start,source_end_line=reader.line_num,raw_record_sha256=sha(b''.join(physical[start-1:reader.line_num])),home=r['home'],away=r['visitor'],date=r['Date'],score=r['FT'],original_fields=r))
    return rows


def compare(events,hist):
    regular=[e for e in events if e['diagnostic_event_key'][1]=='REGULAR'];labels=sorted({e['diagnostic_event_key'][k] for e in regular for k in (4,5)});historical_labels={r[k] for r in hist for k in ('home','away')}
    # Explicit single-season/source correspondence candidates; never rewrite originals.
    differences={'Union':'Royal Union Saint-Gilloise','Sint-Truiden':'St Truiden','Kortrĳk':'Kortrijk','Beerschot':'Beerschot VA','Seraing':'Seraing','Leuven':'Oud-Heverlee Leuven','Zulte Waregem':'Waregem'}
    mapping={name:(name if name in historical_labels else differences.get(name)) for name in labels}
    if any(x not in historical_labels for x in mapping.values()) or len(set(mapping.values()))!=len(mapping):raise ValueError('Unresolved/ambiguous source label correspondence')
    hidx=defaultdict(list)
    for r in hist:hidx[r['home'],r['away']].append(r)
    matches=[];used=set();unmatched=[]
    for e in regular:
        key=e['diagnostic_event_key'];pair=mapping[key[4]],mapping[key[5]];candidates=hidx.get(pair,[])
        if len(candidates)!=1 or e['ambiguous']:unmatched.append(e['source_ids']);continue
        h=candidates[0]
        if h['source_id'] in used:raise ValueError('Historical fixture matched twice')
        used.add(h['source_id']);matches.append(dict(historical=h,documentary=e,date_equal=h['date']==e['comparison_date'],score_equal=h['score']==e['comparison_score'],historical_date_matches_initial=h['date'] in e['initial_dates'],correspondence='2021/22_SOURCE_BOUND_DIAGNOSTIC_ONLY'))
    return dict(historical_observations=len(hist),rsssf_regular_events=len(regular),matched=len(matches),unmatched_historical=[r['source_id'] for r in hist if r['source_id'] not in used],unmatched_documentary=unmatched,date_conflicts=sum(not r['date_equal'] for r in matches),score_conflicts=sum(not r['score_equal'] for r in matches),mapping=[dict(rsssf=k,historical=v,scope='2021/2022 only; candidate correspondence not legal identity') for k,v in sorted(mapping.items())],matches=matches,source_independence='NOT_ESTABLISHED; no claim of primary historical certification')


def build(directory=PRIVATE):
    raw,rec=verify_original(directory);rows,headings=parse_document(raw,rec);events=group_events(rows);hist=historical(directory);comparison=compare(events,hist);stage_counts=Counter(r['stage'] for r in rows);event_counts=Counter(e['diagnostic_event_key'][1] for e in events)
    stage_details={}
    for stage in sorted(stage_counts):
        es=[e for e in events if e['diagnostic_event_key'][1]==stage];clubs=sorted({e['diagnostic_event_key'][k] for e in es for k in (4,5)});pairs=Counter((e['diagnostic_event_key'][4],e['diagnostic_event_key'][5]) for e in es)
        stage_details[stage]=dict(observations=stage_counts[stage],conditional_events=len(es),clubs=len(clubs),literal_labels=clubs,directed_pairings=len(pairs),repeated_pairings=[list(k) for k,n in pairs.items() if n>1],missing_directed_pairings=[[h,a] for h in clubs for a in clubs if h!=a and (h,a) not in pairs],rounds=sorted({str(e['diagnostic_event_key'][2]) for e in es}),ambiguous_events=sum(e['ambiguous'] for e in es))
    return dict(zip(NAMES,[dict(receipt=rec,headings=headings,observations=rows,observation_count=len(rows),stage_counts=dict(stage_counts),score_tokens=dict(Counter(r['score_token'] if not r['numeric_score'] else 'NUMERIC' for r in rows)),stages=stage_details),dict(events=events,event_count=len(events),stage_event_counts=dict(event_counts),explicit_continuations=[e for e in events if e['explicit_continuation_group']],award_candidates=[e for e in events if any(r['score_token']=='awd' for r in e['representations'])],ambiguous_events=[e for e in events if e['ambiguous']]),comparison,dict(receipt=rec,original_phase4_population=dict(csv_txt_observations=10100,conditional_events=8698,unchanged=True),supplemental_population=dict(documentary_observations=len(rows),conditional_documentary_events=len(events),regular_counterparts=comparison['matched'],new_postseason_event_candidates=sum(v for k,v in event_counts.items() if k!='REGULAR')),combined_diagnostic_match_population=dict(csv_txt_representations=10100,supplementary_documentary_representations=len(rows),combined_representations=10100+len(rows),conditional_events_if_only_documented_306_links=8698+len(events)-comparison['matched']),misplaced_original=dict(path='openfootball/belgium/2021-22/be1.txt',declared_season='2020/2021',unchanged=True),scope='TARGETED_RECOVERY_NOT_PHASE5_NO_CORRECTIONS_NO_DISPOSITIONS',rights='Copying with attribution; redistribution/commercial/model-training clearance not inferred')]))


def generate(directory=PRIVATE,output=None):
    output=Path(output) if output else directory/'recovery2021';out=build(directory)
    for name,value in out.items():keep(output/name,encode(value))
    hashes={n:sha(encode(v)) for n,v in out.items()};keep(output/'reproducibility.json',encode(dict(artifacts=hashes)));return hashes


def verify(directory=PRIVATE):
    with tempfile.TemporaryDirectory(prefix='belgium-2021-recovery-') as name:
        proc=subprocess.run([sys.executable,'-B','-m','scripts.recover_belgian_2021_22','--output',name],cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True,timeout=90)
        if proc.returncode:raise ValueError(proc.stdout+proc.stderr)
        result={}
        for artifact in (*NAMES,'reproducibility.json'):
            a=(directory/'recovery2021'/artifact).read_bytes();b=(Path(name)/artifact).read_bytes()
            if a!=b:raise ValueError('Regeneration differs: '+artifact)
            result[artifact]=dict(sha256=sha(a),bytes=len(a),byte_identical=True)
    before={str(p.relative_to(directory)):sha(p.read_bytes()) for p in directory.rglob('*') if p.is_file()}
    with patch(__name__+'.request',side_effect=AssertionError('Cached request forbidden')):collect(directory)
    after={str(p.relative_to(directory)):sha(p.read_bytes()) for p in directory.rglob('*') if p.is_file()}
    if before!=after:raise ValueError('Cache modified evidence')
    return dict(artifacts=result,cache_requests=0,cache_unchanged=True,protected=protect(directory))


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--collect',action='store_true');p.add_argument('--verify',action='store_true');p.add_argument('--output',type=Path);a=p.parse_args()
    print(json.dumps(collect() if a.collect else verify() if a.verify else generate(output=a.output),indent=2))
