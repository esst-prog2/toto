"""Aggregate Phase 1 source feasibility only; no event inventory or decisions."""
from collections import Counter, defaultdict
import csv
from datetime import date, datetime
from html import unescape
import io
import json
import re
from scripts import collect_turkish_super_lig_sources as c
from scripts.validate_ligue1_feasibility import parse_date
from scripts.validate_segunda_feasibility import fixture

HIST_COLUMNS=('Date','Season','home','visitor','FT','hgoal','vgoal','division','tier','totgoal','goaldif','result')


def csv_summary(raw, historical, *, season_ends=None):
    encoding='utf-8-sig' if historical or raw.startswith(b'\xef\xbb\xbf') else 'iso-8859-1'
    reader=csv.DictReader(io.StringIO(raw.decode(encoding),newline=''),strict=True)
    required=HIST_COLUMNS if historical else ('Div','Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR')
    if not set(required)<=set(reader.fieldnames or ()) or len(set(reader.fieldnames))!=len(reader.fieldnames):
        raise ValueError('Unexpected CSV schema')
    if historical and tuple(reader.fieldnames)!=HIST_COLUMNS:raise ValueError('Historical column order changed')
    groups=defaultdict(list)
    for r in reader:
        if None in r or any(v is None for v in r.values()):raise ValueError('CSV row width mismatch')
        if historical:
            y=int(r['Season']);d=date.fromisoformat(r['Date']);h,a=r['hgoal'],r['vgoal'];home,away=r['home'],r['visitor']
            if r['division']!='T1' or r['tier']!='1':raise ValueError('Wrong historical competition/tier')
        else:
            y=2025;d=datetime.strptime(r['Date'],'%d/%m/%Y').date();h,a=r['FTHG'],r['FTAG'];home,away=r['HomeTeam'],r['AwayTeam']
            if r['Div']!='T1':raise ValueError('Wrong direct source competition')
        end=(season_ends or {}).get(y,date(y+1,6,30))
        if not date(y,7,1)<=d<=end or not home.strip() or not away.strip():raise ValueError('Invalid date/team')
        if not re.fullmatch(r'0|[1-9]\d*',h) or not re.fullmatch(r'0|[1-9]\d*',a):raise ValueError('Incomplete numeric score')
        if historical and (r['FT']!=h+'-'+a or int(r['totgoal'])!=int(h)+int(a) or int(r['goaldif'])!=int(h)-int(a)):
            raise ValueError('Contradictory source score fields')
        outcome='H' if int(h)>int(a) else 'A' if int(h)<int(a) else 'D'
        if r['result' if historical else 'FTR']!=outcome:raise ValueError('Contradictory outcome')
        groups[str(y)].append((d.isoformat(),home,away))
    if not groups:raise ValueError('Empty CSV')
    return {y:dict(observations=len(rows),dated_scored=len(rows),clubs=len({n for _,h,a in rows for n in (h,a)}),first_date=min(d for d,_,_ in rows),last_date=max(d for d,_,_ in rows),duplicate_date_pairings=len(rows)-len(set(rows))) for y,rows in sorted(groups.items())}


def txt_summary(raw,year, *, date_parser=parse_date):
    title=False;current=None;round_seen=False;observations=scored=0;dates=[];annotations=Counter();clubs=set();declared={}
    for literal in raw.decode('utf-8-sig').splitlines():
        t=literal.strip()
        if not t:continue
        if t.startswith('='):
            if title or t!=f'= Turkish Süper Lig {year}/{(year+1)%100:02}':raise ValueError('Wrong/duplicate title')
            title=True;continue
        if t.startswith('#'):
            m=re.fullmatch(r'# (Teams|Matches)\s+(\d+)',t)
            if m:declared[m[1]]=int(m[2])
            continue
        if t.startswith('▪'):
            if not re.fullmatch(r'▪ (?:Matchday \d+|\d+\. Round)',t):raise ValueError('Unsupported Turkish stage heading')
            current=None;round_seen=True;continue
        d=date_parser(t,year)
        if d:current=d['date'];continue
        if not title or not round_seen or current is None:raise ValueError('Fixture without context')
        r=fixture(re.sub(r'^\d{1,2}:\d{2}\s+','',t));observations+=1;clubs.update((r['home'],r['away']))
        if not r['home'] or not r['away'] or r['home']==r['away']:raise ValueError('Invalid team labels')
        if r['hg'] is not None:scored+=1;dates.append(current)
        if r['annotation']:annotations[r['annotation']]+=1
    if not title or not observations:raise ValueError('Empty/malformed TXT')
    return dict(observations=observations,dated_scored=scored,unscored=observations-scored,clubs=len(clubs),declared=declared,first_scored_date=min(dates) if dates else None,last_scored_date=max(dates) if dates else None,source_annotations=dict(annotations))


def rsssf_summary(raw,name):
    text=unescape(re.sub(r'<[^>]+>','',raw.decode('iso-8859-1')))
    if 'You are free to copy this document' not in text or 'Copyright' not in text:raise ValueError('RSSSF copying notice missing')
    if name in ('tur91','tur92'):
        return dict(coverage='TOP_FLIGHT_TABLE_ONLY',dated_scored_certified=0)
    if name=='tur94':
        return dict(coverage='TOP_FLIGHT_TABLE_AND_UNDATED_RESULT_GRID',dated_scored_certified=0,grid_score_cells=len(re.findall(r'\|\d+-\d+(?=\|)',text.split('FEDERASYON')[0])))
    if name=='tur93':
        section=text.split('FEDERASYON')[0]
        headers=re.findall(r'^\s*\d+\.\s*Round\s*\(([^)]+)\)',section,re.M)
        rows=re.findall(r'^.*?\s-\s.*?:\s*\d+-\d+\s*$',section,re.M)
        return dict(coverage='ROUND_RESULTS_WITH_SINGLE_AND_RANGE_DATE_HEADINGS',scored_descriptions=len(rows),round_headings=len(headers),range_date_headings=sum(bool(re.search(r'\d\s*[-/]\s*\d',h)) for h in headers),dated_scored_certified=0,reason='Round dates not certified as exact individual kickoff dates; do not assign one day from a range')
    return dict(coverage='TARGETED_STAGE_ADMINISTRATIVE_OR_TABLE_DOCUMENTARY_CONTEXT',dated_scored_certified=None,reason='No fixture extraction or historical adjudication in Phase 1')


def build(directory=c.PRIVATE):
    reports={};receipts=[]
    for plan_name in ('source_plan.json','fixture_plan.json','documentary_plan.json','tff_metadata_plan.json'):
        plan=c.validate_plan(json.loads((directory/plan_name).read_bytes()))
        for item in plan['items']:
            path=directory/item['path'];receipt=json.loads(path.with_name(path.name+'.provenance.json').read_bytes());raw=c.verify(directory,item,receipt);receipts.append(receipt)
            if item['path'].endswith('turkey.csv'):reports['historical']=csv_summary(raw,True)
            elif item['path'].endswith('T1.csv'):reports['direct_2025']=csv_summary(raw,False)
            elif item['path'].endswith('_tr1.txt'):
                y=int(path.name[:4]);reports.setdefault('openfootball',{})[str(y)]=txt_summary(raw,y)
            elif '/rsssf/' in item['path']:reports.setdefault('rsssf',{})[path.stem]=rsssf_summary(raw,path.stem)
    matrix=[]
    for y in range(1990,2026):
        h=reports['historical'].get(str(y));o=reports['openfootball'].get(str(y));d=reports['direct_2025'].get(str(y))
        matrix.append(dict(season=f'{y}/{y+1}',historical=h,openfootball=o,direct_football_data=d,source_gap=not any([h,o,d]),status='NO_CERTIFIED_EXACT_DATED_FIXTURE_SOURCE' if not any([h,o,d]) else 'DATED_SCORED_SOURCE_OBSERVATIONS_NOT_HISTORICALLY_ADJUDICATED',overlap_season=bool(h and o) or bool(o and d)))
    return dict(phase=1,scope='Source feasibility aggregates only; no event inventory, dispositions, canonical records or source corrections',sources=reports,coverage=matrix,manifest=[dict(path=r['path'],url=r['url'],sha256=r['sha256'],bytes=r['bytes'],retrieved_at_utc=r['retrieved_at_utc'],publisher=r['publisher'],licensing=r['licensing'],commit=r.get('commit'),expected_blob=r.get('expected_blob')) for r in receipts])


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--verify',action='store_true');args=parser.parse_args()
    raw=c.encode(build());p=c.PRIVATE/'feasibility.json'
    if args.verify:
        if p.read_bytes()!=raw:raise ValueError('Feasibility reproduction differs')
        print('PASS: all source receipts and deterministic feasibility bytes')
    else:
        c.save(p,raw);print('Saved Phase 1 aggregate feasibility; no records standardized')
