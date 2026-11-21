"""Offline, source-specific Serie B structural audit; diagnostic JSON only.

No standardized data, factual repairs or cross-source fixture merging. Missing
scores/dates remain null. Run with --check to reproduce the saved audit bytes.
"""
import argparse
from collections import Counter
import csv
from datetime import date, datetime
from html import unescape
import io
import json
from pathlib import Path
import re

from scripts.acquire_serie_b import PRIVATE, plan
from scripts.acquire_second_bundesliga import sha, save_once
from toto_estimator.validation import exact_integer


def format_for(year):
    if not 1990 <= year <= 2025:
        raise ValueError('Outside completed target seasons')
    clubs = 20 if year <= 2002 or year >= 2019 else 24 if year == 2003 else 19 if year == 2018 else 22
    return clubs, clubs * (clubs - 1)


def record(line, home, away, hg=None, ag=None, when=None, date_basis='missing', **extra):
    return dict(source_line=line, home=home.strip(), away=away.strip(), hg=hg, ag=ag,
                date=when, date_basis=date_basis, **extra)


def football_data(content, year):
    reader = csv.DictReader(io.StringIO(content.decode('utf-8-sig')))
    required = {'Div','Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR'}
    if not required <= set(reader.fieldnames or []):
        raise ValueError('Missing Football-Data headers')
    rows, excluded, notes = [], [], []
    for row in reader:
        if not any(v.strip() for k,v in row.items() if k is not None and v is not None) and not any(v.strip() for v in row.get(None, [])):
            continue
        if row['Div'] != 'I2':
            raise ValueError(f'Unexpected CSV shape/competition at {reader.line_num}')
        if None in row:
            notes.append(dict(line=reader.line_num,code='extra_csv_fields' if any(v.strip() for v in row[None]) else 'empty_csv_padding',values=row[None]))
        raw = row['Date']; when = None
        for fmt in ('%d/%m/%Y','%d/%m/%y'):
            try:
                when = datetime.strptime(raw, fmt).date().isoformat(); break
            except ValueError:
                pass
        r = record(reader.line_num,row['HomeTeam'],row['AwayTeam'],row['FTHG'] or None,
                   row['FTAG'] or None,when,'source_match' if when else 'missing', source_date=raw)
        rows.append(r)
        if when is None: notes.append(dict(line=reader.line_num,code='invalid_or_missing_date',raw=raw))
        if r['hg'] is not None and r['ag'] is not None:
            h,a=exact_integer(r['hg']),exact_integer(r['ag'])
            if row['FTR'] != ('H' if h>a else 'A' if a>h else 'D'):
                notes.append(dict(line=reader.line_num,code='result_disagreement'))
    return rows, excluded, notes


def football_txt(content, year):
    rows, excluded, notes = [], [], []
    current = None; stage = 'Regular Season'; round_label = None
    for number, line in enumerate(content.decode('utf-8-sig').splitlines(),1):
        s=line.strip()
        if not s or s.startswith('#'): continue
        if s.startswith('=='):
            stage=s.lstrip('=').strip(); current=None; continue
        if s.startswith('='): continue
        if s.startswith('▪'):
            round_label=s[1:].strip()
            if not re.fullmatch(r'(?:Matchday \d+|\d+\. Round)',round_label):
                stage=round_label
            continue
        dm=re.fullmatch(r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun) ([A-Z][a-z]{2}) (\d{1,2})(?: (\d{4}))?',s)
        if dm:
            month=datetime.strptime(dm[2],'%b').month
            y=int(dm[4]) if dm[4] else year+(month<7 or (year==2019 and current is not None and current.startswith('2020') and month in (7,8)))
            current=date(y,month,int(dm[3])).isoformat()
            if date.fromisoformat(current).strftime('%a') != dm[1]:
                notes.append(dict(line=number,code='weekday_mismatch',raw=s))
            continue
        body=re.sub(r'^\d{1,2}:\d{2}\s+','',s)
        if ' v ' in body:
            home, rest=re.split(r'\s+v\s+',body,maxsplit=1)
            m=re.fullmatch(r'(.+?)(?:\s{2,}(\d+)-(\d+)(.*))?',rest)
            if not m: raise ValueError(f'Unrecognized v fixture at {number}')
            away,h,a,tail=m.groups()
            if h is None:
                annotation=re.search(r'\s+\[[^\]]*\]$',away)
                if annotation:
                    tail=annotation.group().strip();away=away[:annotation.start()].rstrip()
        else:
            m=re.fullmatch(r'(.+?)\s{2,}(\d+)-(\d+)(?:\s+(?:a\.e\.t\.|pen\.))?(?:\s+\([^)]*\))?\s{2,}(.+?)(\s+\[[^\]]*\])?',body)
            if not m: raise ValueError(f'Unrecognized Football.TXT line {number}: {s}')
            home,h,a,away,tail=m.groups()
        r=record(number,home,away,h,a,current,'source_match' if current else 'missing',stage=stage,round=round_label,annotation=(tail or '').strip())
        (rows if stage=='Regular Season' else excluded).append(r)
    return rows,excluded,notes


def rsssf(content, year):
    # Strip tags but preserve physical source lines and retain the whole original.
    lines=[unescape(re.sub('<[^>]*>','',s)) for s in content.decode('latin1').splitlines()]
    starts=[i for i,s in enumerate(lines) if re.fullmatch(r'\s*(?:SERIE B|Italy Second Division \(Serie B\)|Second Level \(Serie B\))\s*',s,re.I)]
    if len(starts)!=1: raise ValueError('Ambiguous RSSSF Serie B boundary')
    start=starts[0]+1
    end=next((i for i in range(start,len(lines)) if re.match(r'\s*(?:SERIE C|Italy Third Division|Third Level)',lines[i],re.I)),len(lines))
    section=list(enumerate(lines[start:end],start+1))
    rows=[]; excluded=[];notes=[]
    if year<=1994:
        pair=re.compile(r'^\s*(.+?)\s+-\s+(.+?)\s*=\s*(\d+)\s*-\s*(\d+)\s*\*\s*(\d+)\s*-\s*(\d+)\s*(.*)$')
        rounds=None
        for n,s in section:
            rm=re.fullmatch(r'Stages (\d+)-(\d+)',s.strip())
            if rm: rounds=tuple(map(int,rm.groups()));continue
            if s.strip().startswith('FINAL TABLE'): break
            m=pair.fullmatch(s)
            if m:
                if rounds is None: raise ValueError('Paired fixture before rounds')
                home,away,h,a,rh,ra,tail=m.groups()
                source_home,source_away=home,away
                home=home.replace('*','').strip();away=away.replace('*','').strip()
                if source_home!=home or source_away!=away:
                    notes.append(dict(line=n,code='footnote_marker',source_home=source_home,source_away=source_away))
                rows.extend([record(n,home,away,h,a,round=rounds[0],annotation=tail),record(n,away,home,ra,rh,round=rounds[1],annotation=tail)])
            elif '=' in s and '-' in s: raise ValueError(f'Unparsed paired fixture {n}')
        if len(rows)!=380: notes.append(dict(code='paired_results_count',count=len(rows)))
    elif year==1995:
        current=None;round_no=None
        for n,s in section:
            if s.strip().startswith('FINAL TABLE'): break
            rm=re.fullmatch(r'Round (\d+) \(([A-Za-z]+) (\d+)\)\s*',s)
            if rm:
                round_no=int(rm[1]);month=datetime.strptime(rm[2],'%B').month
                current=date(year+(month<7),month,int(rm[3])).isoformat();continue
            m=re.fullmatch(r'\s*(.+?)\s+-\s+(.+?)\s{2,}(?:(\d+)-(\d+)|Abd)(.*)',s)
            if m:
                home,away,h,a,tail=m.groups()
                rows.append(record(n,home,away,h,a,current,'source_round_only',round=round_no,annotation=tail.strip()))
            elif ' - ' in s: raise ValueError(f'Unparsed round fixture {n}: {s}')
    else:
        matrix=[]
        for n,s in section:
            if s.strip().startswith('FINAL TABLE'): break
            if not re.match(r'\s*\d+\.\s*',s): continue
            tokens=list(re.finditer(r'\d+-\d+|(?<!\S)-(?!\S)',s))
            if len(tokens)!=20: raise ValueError(f'Invalid matrix row {n}')
            name=re.sub(r'^\s*\d+\.\s*','',s[:tokens[0].start()]).strip()
            matrix.append((n,name,[m.group() for m in tokens]))
        if len(matrix)!=20: raise ValueError('Matrix must have 20 rows')
        for i,(n,home,cells) in enumerate(matrix):
            for j,score in enumerate(cells):
                if i==j:
                    if score!='-': raise ValueError('Nonempty matrix diagonal')
                else:
                    if score=='-': raise ValueError('Missing matrix score')
                    h,a=score.split('-');rows.append(record(n,home,matrix[j][1],h,a,matrix_column=j+1))
    # Early decisive/tie-break fixtures are outside the double round robin.
    decisive=False
    for n,s in section:
        if re.search(r'decisive match',s,re.I): decisive=True;continue
        if decisive:
            tm=re.match(r'^(.+?)\s+-\s+(.+?)\s{2,}(\d+)-(\d+)(.*)',s)
            if tm:
                home,away,h,a,tail=tm.groups()
                excluded.append(record(n,home,away,h,a,stage='Decisive tie-break',annotation=tail.strip()))
                decisive=False
            elif s.strip().startswith('Top scorers'): decisive=False
    # Internal arithmetic evidence, not independent result verification. Only
    # case and table footnotes are removed for comparison; no club alias repair.
    gf,ga=Counter(),Counter()
    for r in rows:
        if r['hg'] is not None and r['ag'] is not None:
            home,away=r['home'].upper(),r['away'].upper()
            gf[home]+=int(r['hg']);gf[away]+=int(r['ag'])
            ga[home]+=int(r['ag']);ga[away]+=int(r['hg'])
    for n,s in section:
        tm=re.match(r'^\d+\.\s*(.+?)\s+38\s+(.*)',s)
        if not tm: continue
        name=re.sub(r'\s*\([^)]*\)','',tm[1]).strip().upper()
        nums=re.findall(r'\d+',tm[2])
        if name in gf and len(nums)>=3:
            table=list(map(int,nums[-3:-1]));observed=[gf[name],ga[name]]
            if observed!=table:
                notes.append(dict(line=n,code='table_goal_disagreement',team=name,
                                  parsed_goals=observed,table_goals=table))
    # Retain complete Serie B section text privately, including all footnotes,
    # tie-break dates/results and continuation lines; never export it publicly.
    notes.append(dict(code='section_text',lines=[dict(line=n,text=s) for n,s in section]))
    # Preserve excluded/tie-break/administrative text as exact line references.
    for n,s in section:
        if re.search(r'decisive|play.?off|deduct|abandon|disturbance|awarded|relegated|penalty',s,re.I):
            notes.append(dict(line=n,code='historical_note',raw=s.strip()))
    return rows,excluded,notes


def audit(rows, year):
    n,expected=format_for(year);teams=sorted({r[k] for r in rows for k in ('home','away')})
    pairs=Counter((r['home'],r['away']) for r in rows)
    issues=[];missing_dates=0;round_dates=0;missing_scores=0
    for r in rows:
        if not r['home'] or not r['away'] or r['home']==r['away']: issues.append('invalid_teams')
        if r['date'] is None: missing_dates+=1
        else:
            try:
                d=date.fromisoformat(r['date'])
                end=date(year+1,8,31) if year==2019 else date(year+1,6,30)
                if not date(year,7,1)<=d<=end: issues.append('date_outside_season')
            except ValueError: issues.append('invalid_date')
        if r['date_basis']=='source_round_only': round_dates+=1
        if r['hg'] is None or r['ag'] is None: missing_scores+=1
        else:
            try:
                if min(exact_integer(r['hg']),exact_integer(r['ag']))<0: issues.append('negative_score')
            except (ValueError,TypeError): issues.append('invalid_score')
    home_counts=Counter(r['home'] for r in rows);away_counts=Counter(r['away'] for r in rows)
    appearance_errors={t:dict(home=home_counts[t],away=away_counts[t]) for t in teams if home_counts[t]!=n-1 or away_counts[t]!=n-1}
    if appearance_errors: issues.append('team_fixture_allocation')
    missing_pairs=[(h,a) for h in teams for a in teams if h!=a and (h,a) not in pairs]
    duplicates=sum(v-1 for v in pairs.values() if v>1)
    if len(rows)!=expected: issues.append('fixture_count')
    if len(teams)!=n: issues.append('team_count')
    if duplicates: issues.append('duplicate_fixtures')
    if missing_pairs: issues.append('missing_pairings')
    if missing_scores: issues.append('missing_final_scores')
    status='STRUCTURAL_PASS' if not issues else 'REVIEW'
    if not issues and missing_dates: status='UNDATED_RESULTS'
    if not issues and round_dates: status='ROUND_DATES_ONLY'
    return dict(season=f'{year}/{year+1}',teams=len(teams),expected_teams=n,records=len(rows),expected=expected,
                scored_records=len(rows)-missing_scores,missing_dates=missing_dates,round_dates=round_dates,
                missing_scores=missing_scores,duplicate_fixtures=duplicates,missing_pairs=missing_pairs,
                issues=sorted(set(issues)),status=status,team_names=teams,appearance_errors=appearance_errors)


def build(directory=PRIVATE):
    manifest=json.loads((directory/'acquisition.json').read_text())
    summaries=[];details=[]
    # Verify every acquired original, including the unselected 2025/26 candidate.
    for receipt_path in directory.rglob('*.provenance.json'):
        original=receipt_path.with_name(receipt_path.name.removesuffix('.provenance.json'))
        receipt=json.loads(receipt_path.read_text());content=original.read_bytes()
        if sha(content)!=receipt['sha256'] or len(content)!=receipt['bytes']:
            raise ValueError('Acquired original/metadata checksum mismatch: '+str(original))
    selection_path=directory/'selection.json'
    entries=json.loads(selection_path.read_text())['files'] if selection_path.exists() else manifest['files']
    if sorted(e['season'] for e in entries)!=[f'{y}/{y+1}' for y in range(1990,2026)]:
        raise ValueError('Selection must cover exactly the 36 completed seasons')
    for original in manifest['files']:
        p=directory/original['file']
        receipt=json.loads(p.with_name(p.name+'.provenance.json').read_text())
        if receipt['url']!=original['url'] or sha(p.read_bytes())!=receipt['sha256']:
            raise ValueError('Initial acquisition manifest/receipt mismatch')
    for entry in entries:
        path=directory/entry['file']
        if not path.resolve().is_relative_to(directory.resolve()):
            raise ValueError('Selection outside private source directory')
        content=path.read_bytes()
        receipt=json.loads(path.with_name(path.name+'.provenance.json').read_text())
        if sha(content)!=receipt['sha256'] or len(content)!=receipt['bytes'] or entry['url']!=receipt['url']:
            raise ValueError('Source receipt mismatch: '+entry['file'])
        year=int(entry['season'][:4]);parser={'rsssf':rsssf,'football_data':football_data,'openfootball':football_txt}[entry['kind']]
        rows,excluded,notes=parser(content,year)
        summary=audit(rows,year);summary.update(source=entry['kind'],file=entry['file'],sha256=sha(content),excluded_records=len(excluded),source_notes=len(notes))
        if any(note['code'] not in ('historical_note','empty_csv_padding','footnote_marker','section_text') for note in notes): summary['status']='REVIEW'
        summary['note_codes']=dict(Counter(note['code'] for note in notes))
        summaries.append(summary);details.append(dict(**entry,records=rows,excluded=excluded,notes=notes))
    for meta in manifest['metadata']:
        p=directory/meta['file'];r=json.loads(p.with_name(p.name+'.provenance.json').read_text())
        if sha(p.read_bytes())!=r['sha256']: raise ValueError('Metadata checksum mismatch')
    return dict(scope='Private source diagnostics, not standardized or verified results',seasons=summaries,details=details)


def encode(value):
    return (json.dumps(value,indent=2,ensure_ascii=False,sort_keys=True)+'\n').encode()


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    result=build();content=encode(result);target=PRIVATE/'structural_audit.json'
    if args.check:
        if target.read_bytes()!=content: raise ValueError('Saved audit does not reproduce')
    else: save_once(target,content)
    for s in result['seasons']:
        print(s['season'],s['source'],s['records'],s['scored_records'],s['expected'],s['teams'],s['missing_dates'],s['missing_scores'],s['status'],s['issues'])
    print('Total',sum(s['records'] for s in result['seasons']),'scored',sum(s['scored_records'] for s in result['seasons']))


if __name__=='__main__': main()
