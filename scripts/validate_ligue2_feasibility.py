"""Lossless Ligue 2 Phase 2 assessment; no corrections or eligibility decisions."""
import argparse
from collections import Counter, defaultdict
from datetime import date
from html.parser import HTMLParser
import html
import json
import re
from scripts import collect_ligue2_feasibility as c
from scripts.validate_ligue1_feasibility import parse_date, goals, outcome, assess as common_assess
from scripts.validate_segunda_feasibility import fixture
PRIVATE = c.PRIVATE
OUTPUT = 'feasibility_assessment.json'

def parse_text(raw, year, full=False):
    rows = []; notes = []; current = None; stage = None; round_id = None; title = False
    depth = 0; detail_context = False
    for number, line in enumerate(raw.decode('utf-8-sig').splitlines(), 1):
        s = line.strip()
        if not s:
            continue
        if depth or s.startswith('('):
            if not rows:
                raise ValueError('Scorer annotation before any fixture')
            depth += s.count('(')-s.count(')')
            if depth < 0:
                raise ValueError('Unbalanced scorer annotation')
            notes.append(dict(line=number, kind='scorer_annotation', text=s)); continue
        if s.startswith('#'):
            notes.append(dict(line=number, kind='comment', text=s)); continue
        if s.startswith('='):
            season = re.search(r'(\d{4})/(\d{2,4})', s)
            if title or not re.search(r'\bLigue 2\b', s) or not season or int(season[1]) != year or int(season[2]) != ((year+1)%100 if len(season[2])==2 else year+1):
                raise ValueError('Wrong/duplicate competition/season title')
            title = True; notes.append(dict(line=number, kind='competition_title', text=s)); continue
        if s.startswith('▪'):
            label = s[1:].strip(); m = re.fullmatch(r'(?:Matchday (\d+)|Regular Season - (\d+)|(\d+)\. Round)' , label)
            if m:
                stage = 'REGULAR_SEASON'; round_id = int(next(x for x in m.groups() if x))
                if not 1 <= round_id <= (34 if year >= 2024 else 38):
                    raise ValueError('Unexpected regular round')
            elif re.search(r'play.?off|promotion|final', label, re.I):
                stage = 'OTHER_STAGE'; round_id = label
            else:
                raise ValueError('Unknown stage: '+label)
            current = None; detail_context = False
            notes.append(dict(line=number, kind='stage_heading', stage=stage, label=label)); continue
        parsed = parse_date(s, year)
        if parsed:
            current = parsed; detail_context = False; continue
        if full and rows:
            latest = rows[-1]
            prefixes = (latest['home']+':', latest['away']+':', 'Refs:', 'Yellow:', 'Red:')
            if s.startswith(prefixes):
                detail_context = True
                notes.append(dict(line=number, kind='lineup_discipline_or_official', text=s)); continue
            if detail_context and line.startswith('    ') and not re.search(r'\s+v\s+|\s\d+-\d+\s', s):
                notes.append(dict(line=number, kind='detail_continuation', text=s)); continue
        body = re.sub(r'^\d{1,2}:\d{2}\s+', '', s)
        if not title or stage is None or current is None:
            raise ValueError(f'Fixture without title/stage/date at line {number}: {s}')
        try:
            r = fixture(body)
        except ValueError as exc:
            raise ValueError(f'Unknown fixture/details grammar line {number}: {s}') from exc
        r.update(current, source_line=number, raw_record=line, stage=stage, round=round_id,
                 season=f'{year}/{year+1}', date_semantics='SOURCE_DATE_HEADING_NOT_COMPLETION_CERTIFICATION')
        rows.append(r); detail_context = False
    if depth or not title or not rows:
        raise ValueError('Unterminated annotation or missing title/fixtures')
    return rows, notes



def assess(rows, year):
    regular=[r for r in rows if r['stage']=='REGULAR_SEASON']
    other=[r for r in rows if r['stage']!='REGULAR_SEASON']
    result=common_assess(regular,year)
    n=18 if year>=2024 else 20
    result.update(expected_clubs=n,expected_scheduled=n*(n-1),expected_played=280 if year==2019 else n*(n-1),
                  total_observations=len(rows),other_stage_observations=len(other),
                  source_cancelled_lines=[r['source_line'] for r in regular if re.search(r'cancel',r['annotation'],re.I)],
                  other_stage_records=other)
    result['date_precision']='Source day/month/weekday headings; year resolved against stated season. Not independent actual-completion certification.'
    result['identity_risks']=[t for t in result['team_names'] if re.search(r'Ajaccio|Bastia|Annecy|Boulogne|Bourg|Quevilly|Paris|Red Star|Evian',t,re.I)]
    return result


class Pre(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.depth=0;self.parts=[];self.blocks=[]
    def handle_starttag(self,tag,attrs):
        if tag=='pre':self.depth+=1;self.parts=[]
    def handle_endtag(self,tag):
        if tag=='pre' and self.depth:self.blocks.append(''.join(self.parts));self.depth-=1
    def handle_data(self,data):
        if self.depth:self.parts.append(data)


def rsssf(raw):
    # Explicit original charset; never decode with replacement or guess aliases.
    head=raw[:5000].decode('ascii',errors='ignore')
    m=re.search(r'charset\s*=\s*["\']?([\w-]+)',head,re.I)
    encoding=m[1] if m else 'iso-8859-1'
    text=raw.decode(encoding); parser=Pre();parser.feed(text)
    candidates=[b for b in parser.blocks if 'Stages 1-20' in b]
    if len(candidates)!=1:raise ValueError('Missing/ambiguous second-division paired-results block')
    block=candidates[0];rows=[];headers=[];ignored=[];current=None
    for line_no,line in enumerate(block.splitlines(),1):
        s=line.strip()
        if not s:continue
        if current and s == 'Final Table:':break
        h=re.fullmatch(r'Stages\s+(\d+)-(\d+)\s+(\d{2}\.\d{2}\.)\s+(\d{2}\.\d{2}\.)',s)
        if h:
            current=h.groups();headers.append(dict(block_line=line_no,raw=line,rounds=[int(h[1]),int(h[2])],date_headings=[h[3],h[4]]));continue
        match=re.fullmatch(r'(.+?)\s+-\s+(.+?)\s*=\s*(\d+)-(\d+)\s+-\s+(\d+)-(\d+)(.*)',s)
        if match:
            if current is None:raise ValueError('Paired fixture without headings')
            home,away,hg,ag,rhg,rag,note=match.groups()
            for index,(h,a,g1,g2) in enumerate([(home,away,hg,ag),(away,home,rhg,rag)]):
                heading=current[index+2];d,mn=map(int,heading.strip('.').split('.'));y=1998 if mn>=7 else 1999
                day=date(y,mn,d).isoformat()
                rows.append(dict(home=h,away=a,hg=g1,ag=g2,FT=f'{g1}-{g2}',HT=None,annotation=note.strip(),
                     date=day,date_heading=heading,date_semantics='ROUND_HEADING_PROXY_NOT_EXPLICIT_FIXTURE_DATE',
                     round=int(current[index]),stage='REGULAR_SEASON',season='1998/1999',block_line=line_no,
                     source_line=None,raw_record=line,paired_leg=index+1,source_left_team=home,source_right_team=away,
                     source_score_left=g1,source_score_right=g2,
                     venue_and_score_semantics='PROVISIONAL_FIRST_LEG' if index==0 else 'RETURN_VENUE_AND_SCORE_ORIENTATION_UNRESOLVED'))
            continue
        if current and ('=' in s or re.search(r'\d+-\d+',s)) and not re.fullmatch(r'[_ -]+',s):raise ValueError('Unknown result grammar: '+s)
        ignored.append(dict(block_line=line_no,text=line))
    if not rows:raise ValueError('Empty second-division sample')
    return rows,dict(encoding=encoding,headers=headers,other_block_text=ignored,
        selection='Unique PRE block containing Stages 1-20; return venue reversal is provisional; literal score columns, raw lines and proxy headings retained; no historical score-orientation certification',
        historical_date_confidence='No individual fixture-date certification from round headings')


def rsssf_assess(rows):
    names=sorted({r[k] for r in rows for k in ('home','away')});pairs=defaultdict(list)
    for r in rows:pairs[r['home'],r['away']].append([r['block_line'],r['paired_leg']])
    return dict(season='1998/1999',observed=len(rows),scored=sum(r['hg'] is not None and r['ag'] is not None for r in rows),
        unscored=sum(r['hg'] is None or r['ag'] is None for r in rows),expected_clubs=20,expected_scheduled=380,
        literal_clubs=len(names),team_labels=names,distinct_directed_pairs=len(pairs),
        duplicate_literal_pairs=[dict(home=h,away=a,bindings=ls) for (h,a),ls in sorted(pairs.items()) if len(ls)>1],
        missing_literal_pairs=[[h,a] for h in names for a in names if h!=a and (h,a) not in pairs],
        date_precision_counts=dict(Counter(r['date_semantics'] for r in rows)),
        warning='Literal name variants are not silently merged. Round-heading dates remain proxies; no complete historical-date claim.')


def build(directory=PRIVATE,root=c.ROOT):
    protection=c.protect(directory,root);m=c.verify_originals(directory);sources=[]
    for receipt in m['files']:
        raw=(directory/receipt['path']).read_bytes();year=int(receipt['season'][:4])
        if receipt['repository']==c.REPO:
            rows,notes=parse_text(raw,year);assessment=assess(rows,year)
        else:
            rows,notes=rsssf(raw);assessment=rsssf_assess(rows)
        for r in rows:
            r.update(source=receipt['path'],source_sha256=receipt['sha256'],
                     raw_line_sha256=c.sha(r['raw_record'].encode('utf-8')),
                     audit_id=c.sha(c.encode([receipt['sha256'],r.get('source_line'),r.get('block_line'),r.get('paired_leg')])) )
        sources.append(dict(receipt=receipt,assessment=assessment,notes=notes,records=rows))
    return dict(phase=2,scope='Six approved modern samples and one RSSSF historical original only',
                canonical_league='Ligue 2',sources=sources,protected=protection,
                rights=c.RIGHTS,historical_coverage='1990/91–2013/14 remains an unresolved 24-season acquisition objective; one RSSSF feasibility original is not continuous coverage',
                policy='No corrections, aliases, exclusions, standardization or training; technical facts do not certify history or licensing')


if __name__=='__main__':
    result=build();target=PRIVATE/OUTPUT;content=c.encode(result)
    if target.exists():
        if target.read_bytes()!=content:raise ValueError('Assessment differs: inspect before replacing')
    else:c.save(target,content)
    for source in result['sources']:print(source['receipt']['season'],json.dumps(source['assessment'],ensure_ascii=False))
