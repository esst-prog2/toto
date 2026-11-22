"""Offline structural assessment of only the approved La Liga feasibility files.

No standardization, model use or historical corrections. --check compares bytes.
"""
import argparse
from collections import Counter,defaultdict
import csv
from datetime import date,datetime
import io
import json
import re
import unicodedata

from scripts.collect_la_liga_feasibility import PRIVATE,protected,sha
from scripts.artifact_io import check_overwrite
from toto_estimator.validation import exact_integer

HIST='jalapic/engsoccerdata/data-raw/spain.csv'
TARGETS=(1990,1995,1996,2011)
OUTPUT='feasibility_assessment.json'


def encode(value):return (json.dumps(value,indent=2,ensure_ascii=False,sort_keys=True)+'\n').encode()


def historical(raw):
    text=raw.decode('utf-8-sig');reader=csv.DictReader(io.StringIO(text))
    required={'Date','Season','home','visitor','FT','hgoal','vgoal','tier','round','group','notes'}
    if not required<=set(reader.fieldnames or ()):raise ValueError('Historical required headers missing')
    rows=[]
    for r in reader:
        if None in r or any(v is None for v in r.values()):raise ValueError('Historical CSV row shape')
        r=dict(r,source_line=reader.line_num)
        rows.append(r)
    return rows


def text_results(raw,year):
    text=raw.decode('utf-8-sig');rows=[];notes=[];stage=None;day=None;annotation_depth=0;last_match=False
    for number,line in enumerate(text.splitlines(),1):
        s=line.strip()
        if not s:continue
        if annotation_depth:
            annotation_depth+=s.count('(')-s.count(')')
            if annotation_depth<0:raise ValueError('Unbalanced scorer annotation')
            notes.append(dict(line=number,kind='scorer_annotation',text=s));continue
        if s.startswith('(') and last_match:
            annotation_depth=s.count('(')-s.count(')')
            if annotation_depth<0:raise ValueError('Unbalanced scorer annotation')
            notes.append(dict(line=number,kind='scorer_annotation',text=s));continue
        last_match=False
        if s.startswith('#'):notes.append(dict(line=number,kind='comment',text=s));continue
        if s.startswith('='):
            if not ('Primera División' in s or 'Primera Division' in s):raise ValueError('Unexpected competition heading')
            notes.append(dict(line=number,kind='competition_header',text=s));continue
        if s.startswith('▪'):
            label=s[1:].strip()
            if not re.fullmatch(r'(?:Matchday \d+|Regular Season - \d+)',label):raise ValueError('Unexpected stage: '+label)
            stage=label;notes.append(dict(line=number,kind='round_header',text=s));continue
        dm=re.fullmatch(r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun) ([A-Z][a-z]{2}) (\d{1,2})(?: (\d{4}))?',s)
        if dm:
            month=datetime.strptime(dm[2],'%b').month
            y=int(dm[4]) if dm[4] else year+(month<7)
            day=date(y,month,int(dm[3])).isoformat()
            if date.fromisoformat(day).strftime('%a')!=dm[1]:notes.append(dict(line=number,kind='weekday_mismatch',text=s))
            continue
        body=re.sub(r'^\d{1,2}:\d{2}\s+','',s)
        if ' v ' in body:
            h,rest=re.split(r'\s+v\s+',body,maxsplit=1)
            m=re.fullmatch(r'(.+?)\s{2,}(\d+)-(\d+)(?:\s+\(\d+-\d+\))?(\s+\[[^\]]+\])?',rest)
            if m:a,hg,ag,tail=m.groups()
            else:
                m=re.fullmatch(r'(.+?)(\s+\[[^\]]+\])?',rest)
                a,tail=m.groups();hg=ag=None
        else:
            m=re.fullmatch(r'(.+?)\s{2,}(\d+)-(\d+)(?:\s+\(\d+-\d+\))?\s{2,}(.+?)(\s+\[[^\]]+\])?',body)
            if not m:raise ValueError(f'Unrecognized fixture text at {number}: {s}')
            h,hg,ag,a,tail=m.groups()
        if stage is None or day is None:raise ValueError('Match without stage/date')
        rows.append(dict(source_line=number,date=day,home=h,away=a,hg=hg,ag=ag,stage=stage,annotation=(tail or '').strip()))
        last_match=True
    if annotation_depth:raise ValueError('Unterminated scorer annotation')
    return rows,notes


def assess(rows,year,expected_teams):
    issues=[];scored=0;date_errors=[];scores=[];teams=set();pairs=Counter();events=defaultdict(list)
    for r in rows:
        teams.update((r['home'],r['away']));pairs[r['home'],r['away']]+=1
        if not r['home'] or not r['away'] or r['home']==r['away']:issues.append('invalid_teams')
        if any(t!=t.strip() for t in (r['home'],r['away'])):issues.append('team_whitespace')
        try:
            day=date.fromisoformat(r['date'])
            if day.isoformat()!=r['date'] or not date(year,7,1)<=day<=date(year+1,6,30):raise ValueError()
        except (TypeError,ValueError):date_errors.append(r['source_line'])
        for team in (r['home'],r['away']):events[r['date'],team].append(r['source_line'])
        try:
            hg,ag=exact_integer(r['hg']),exact_integer(r['ag'])
            if min(hg,ag)<0:raise ValueError()
            scored+=1
            if 'FT' in r and r['FT']!=f'{hg}-{ag}':issues.append('FT_score_disagreement')
        except (TypeError,ValueError):scores.append(r['source_line'])
    normalized=defaultdict(list)
    for t in sorted(teams):normalized[unicodedata.normalize('NFC',t).casefold()].append(t)
    aliases={k:v for k,v in normalized.items() if len(v)>1}
    missing=[(h,a) for h in sorted(teams) for a in sorted(teams) if h!=a and (h,a) not in pairs]
    duplicates=[dict(home=h,away=a,count=n) for (h,a),n in pairs.items() if n>1]
    collisions=[dict(date=d,team=t,lines=ls) for (d,t),ls in events.items() if len(ls)>1]
    allocation={t:dict(home=sum(r['home']==t for r in rows),away=sum(r['away']==t for r in rows)) for t in sorted(teams)}
    allocation_errors={t:c for t,c in allocation.items() if c!={'home':expected_teams-1,'away':expected_teams-1}}
    expected=expected_teams*(expected_teams-1)
    if len(rows)!=expected:issues.append('fixture_count')
    if len(teams)!=expected_teams:issues.append('team_count')
    if date_errors:issues.append('date_errors')
    if scores:issues.append('missing_or_invalid_scores')
    if duplicates:issues.append('duplicate_pairings')
    if missing:issues.append('missing_pairings')
    if collisions:issues.append('same_team_date_collisions')
    if aliases:issues.append('normalized_team_collisions')
    if allocation_errors:issues.append('appearance_allocation')
    return dict(season=f'{year}/{year+1}',records=len(rows),scored=scored,expected=expected,teams=len(teams),
                first_date=min((r['date'] for r in rows),default=None),last_date=max((r['date'] for r in rows),default=None),
                date_error_lines=date_errors,invalid_score_lines=scores,missing_pairings=missing,duplicates=duplicates,
                team_date_collisions=collisions,normalized_name_collisions=aliases,allocation_errors=allocation_errors,
                team_names=sorted(teams),non_ascii_names=sorted(t for t in teams if not t.isascii()),
                annotations=[r for r in rows if r.get('annotation')],issues=sorted(set(issues)),
                status='STRUCTURAL_PASS' if not issues else 'REVIEW',records_detail=rows)


def hist_season(rows,year):
    selected=[r for r in rows if int(r['Season'])==year]
    bad=[r for r in selected if r['tier']!='1' or r['round']!='league' or r['group'] not in ('NA','')]
    if bad:raise ValueError('Unexpected tier/stage/group in feasibility season')
    return [dict(source_line=r['source_line'],date=r['Date'],home=r['home'],away=r['visitor'],hg=r['hgoal'],ag=r['vgoal'],
                 FT=r['FT'],annotation='' if r['notes'] in ('NA','') else r['notes'],stage=r['round']) for r in selected]


ALIASES_2012={'Athletic Club':'Athletic Bilbao','Atlético Madrid':'Atletico Madrid','CA Osasuna':'CA Osasuna',
              'Deportivo La Coruña':'Deportivo La Coruna','Espanyol Barcelona':'Espanyol Barcelona','FC Barcelona':'FC Barcelona',
              'Getafe CF':'Getafe CF','Granada CF':'Granada CF','Levante UD':'Levante UD','Málaga CF':'Malaga CF',
              'RC Celta':'Celta Vigo','RCD Mallorca':'RCD Mallorca','Rayo Vallecano':'Rayo Vallecano','Real Betis':'Real Betis',
              'Real Madrid':'Real Madrid','Real Sociedad':'Real Sociedad','Real Valladolid':'Real Valladolid',
              'Real Zaragoza':'Real Zaragoza','Sevilla FC':'Sevilla FC','Valencia CF':'Valencia CF'}


def overlap(old,new):
    oldteams={r[k] for r in old for k in ('home','away')};newteams={r[k] for r in new for k in ('home','away')}
    if set(ALIASES_2012)!=newteams or set(ALIASES_2012.values())!=oldteams or len(set(ALIASES_2012.values()))!=len(ALIASES_2012):
        raise ValueError('Explicit diagnostic name mapping does not cover teams bijectively')
    older={(r['home'],r['away']):r for r in old}
    if len(older)!=len(old):raise ValueError('Duplicate historical overlap pairing')
    if len(new)!=len(old):raise ValueError('Incomplete overlap scope')
    # Keep each discrepancy with both exact physical source locations.
    result=[]
    for n in new:
        o=older[ALIASES_2012[n['home']],ALIASES_2012[n['away']]]
        diff={f:dict(historical=o[f],openfootball=n[f]) for f in ('date','hg','ag') if str(o[f])!=str(n[f])}
        if diff:result.append(dict(home=o['home'],away=o['away'],historical_line=o['source_line'],openfootball_line=n['source_line'],differences=diff))
    return dict(matches_compared=len(new),aliases=ALIASES_2012,discrepancies=result,
                independence='Unestablished; cross-source agreement is not independent historical certification. No merge or correction.')


def build(directory=PRIVATE):
    count=protected(directory);manifest=json.loads((directory/'acquisition.json').read_text())
    for r in manifest['files']:
        raw=(directory/r['path']).read_bytes()
        if len(raw)!=r['bytes'] or sha(raw)!=r['sha256']:raise ValueError('Original source changed')
    raw=(directory/HIST).read_bytes();allrows=historical(raw)
    reports=[]
    for y in TARGETS:reports.append(dict(source=HIST,**assess(hist_season(allrows,y),y,22 if y in (1995,1996) else 20)))
    parsed={}
    for y in (2012,2025):
        path=f'openfootball/espana/{y}-{(y+1)%100:02}/1-liga.txt';b=(directory/path).read_bytes()
        rows,notes=text_results(b,y);parsed[y]=rows
        reports.append(dict(source=path,**assess(rows,y,20),parser_notes=notes,
                            encoding='UTF-8',CRLF_lines=b.count(b'\r\n')))
    overlap_old=hist_season(allrows,2012)
    boundary=dict(older_last_season='2011/2012',newer_first_season='2012/2013',
                  missing_season_at_boundary=False,overlap_2012=overlap(overlap_old,parsed[2012]),
                  historical_2012_structure=assess(overlap_old,2012,20),
                  historical_last_available_start_year=max(int(r['Season']) for r in allrows))
    coverage=Counter(r['Season'] for r in allrows)
    notes=[dict(line=r['source_line'],season=r['Season'],home=r['home'],away=r['visitor'],notes=r['notes']) for r in allrows if r['notes'] not in ('NA','')]
    return dict(scope='Approved bounded feasibility only; no standardized output, training or independent historical certification',
                historical_inventory=dict(rows=len(allrows),season_counts=dict(sorted(coverage.items(),key=lambda x:int(x[0]))),
                tier_counts=dict(Counter(r['tier'] for r in allrows)),stage_counts=dict(Counter(r['round'] for r in allrows)),notes=notes,
                encoding='UTF-8 strict decoding',replacement_character_present='\ufffd' in raw.decode('utf-8-sig')),
                seasons=reports,boundary=boundary,protected_files_unchanged=count,
                missing_status_warning='Absence of source annotations does not establish that all fixtures were ordinary uninterrupted played matches.',
                rights=manifest['rights'],acquisition_sha256=sha((directory/'acquisition.json').read_bytes()))


def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args()
    target=PRIVATE/OUTPUT
    if not args.check:check_overwrite([target])
    result=build();content=encode(result)
    if args.check:
        if target.read_bytes()!=content:raise ValueError('Assessment differs')
    else:
        with target.open('xb') as f:f.write(content)
    for r in result['seasons']:print(r['season'],r['records'],r['scored'],r['expected'],r['status'],r['issues'])
    print('Overlap discrepancies',len(result['boundary']['overlap_2012']['discrepancies']))
    print('Protected unchanged',result['protected_files_unchanged'])


if __name__=='__main__':main()
