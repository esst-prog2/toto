"""Offline structural audit of selected Bundesliga originals, never standardization.

Source-specific parsing is in memory only. Reuses TOTOdology's historical validator,
canonical seasons, exact integers, team checks, outcomes and artifact serializer.
"""
from collections import Counter, defaultdict
import csv
from datetime import date, datetime
import hashlib
import io
import json
from pathlib import Path
import re

import pandas as pd
from scripts.artifact_io import serialize_csv
from toto_estimator.data import validate_historical_data
from toto_estimator.historical_import import canonical_season
from toto_estimator.outcomes import outcome_from_goals
from toto_estimator.validation import exact_integer, team_name

ROOT=Path(__file__).resolve().parents[1]
PRIVATE=ROOT/'data/private/germany/csv_history'
AS_OF=date(2026,11,5)
HDA={'1':'H','X':'D','2':'A'}


def audit_file(path, season, kind, *, include_records=False):
    season=canonical_season(season);start=int(season[:4])
    n=20 if start==1991 else 18;expected=n*(n-1)
    issues=[];notes=[];records=[];optional_missing=Counter();rounds=Counter()
    def issue(line,code,detail):issues.append(dict(source_row=line,code=code,detail=detail))
    text=Path(path).read_bytes().decode('utf-8-sig' if kind=='early' else 'ISO-8859-1')
    reader=csv.DictReader(io.StringIO(text,newline=''),strict=True)
    fields=reader.fieldnames or []
    required={'Round','Date','Team 1','Team 2','FT'} if kind=='early' else {'Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR'}
    if len(fields)!=len(set(fields)) or not required<=set(fields):raise ValueError('Missing/duplicate source CSV headers')
    total=0
    for row in reader:
        total+=1;line=reader.line_num
        if None in row or any(v is None for v in row.values()):
            issue(line,'malformed_csv_row','Row width differs from header');continue
        for field in required:
            if not row[field].strip():issue(line,'missing_required_value',field)
        try:
            if kind=='early':
                day=re.fullmatch(r'\([A-Za-z]{3}\) (\d{1,2} [A-Za-z]{3} \d{4}) \(\d+\)',row['Date'].strip())
                if not day:raise ValueError('Unrecognized annotated English date')
                d=datetime.strptime(day[1],'%d %b %Y').date()
                score=re.fullmatch(r'(\d+)-(\d+)',row['FT'].strip())
                if not score:raise ValueError('Missing/ambiguous full-time score')
                h,a=map(exact_integer,score.groups())
                # Game-count annotations are schema syntax, not historical name aliases.
                home=team_name(re.sub(r'\s+\(\d+\)$','',row['Team 1']))
                away=team_name(re.sub(r'\s+\(\d+\)$','',row['Team 2']))
                rd=exact_integer(row['Round']);rounds[rd]+=1
                if not 1<=rd<=2*(n-1):issue(line,'invalid_round',row['Round'])
                ht=row.get('HT','').strip()
                if ht:
                    half=re.fullmatch(r'(\d+)-(\d+)',ht)
                    if not half:issue(line,'invalid_halftime_score',ht)
                    elif any(x>y for x,y in zip(map(int,half.groups()),(h,a))):issue(line,'halftime_exceeds_fulltime',ht)
            else:
                if not re.fullmatch(r'\d{4}-\d{2}-\d{2}',row['Date']):raise ValueError('Non-ISO source date')
                d=date.fromisoformat(row['Date']);h=exact_integer(row['FTHG']);a=exact_integer(row['FTAG'])
                home=team_name(row['HomeTeam']);away=team_name(row['AwayTeam'])
                expected_result=HDA[outcome_from_goals(h,a)]
                if row['FTR']!=expected_result:issue(line,'score_result_mismatch',f"FTR={row['FTR']}; goals imply {expected_result}")
                hg,ag=row.get('HTHG',''),row.get('HTAG','')
                if bool(hg.strip())!=bool(ag.strip()):issue(line,'partial_halftime_score','Only one halftime goal field is present')
                if hg.strip() and ag.strip():
                    hh,ha=exact_integer(hg),exact_integer(ag)
                    if hh<0 or ha<0 or hh>h or ha>a:issue(line,'halftime_exceeds_fulltime',f'{hh}-{ha} vs {h}-{a}')
                    if row.get('HTR','') and row['HTR']!=HDA[outcome_from_goals(hh,ha)]:issue(line,'halftime_result_mismatch',row['HTR'])
                for field in fields:
                    if field not in required and not row[field].strip():optional_missing[field]+=1
                if 'Div' in row and row['Div']!='D1':issue(line,'wrong_competition',row['Div'])
                if 'Season' in row and canonical_season(row['Season'])!=season:issue(line,'wrong_season',row['Season'])
            if d.year not in (start,start+1):issue(line,'date_outside_season',d.isoformat())
            if d>AS_OF:issue(line,'future_date',d.isoformat())
            if not home or not away or home==away or min(h,a)<0:raise ValueError('Invalid/missing teams or negative goals')
            records.append(dict(source_row=line,season=season,date=d.isoformat(),home_team=home,away_team=away,home_goals=h,away_goals=a))
        except (ValueError,TypeError) as exc:issue(line,'invalid_required_field',str(exc))
    teams=sorted({r[k] for r in records for k in ('home_team','away_team')})
    pairs=defaultdict(list);identities=defaultdict(list)
    for r in records:
        pairs[(r['home_team'],r['away_team'])].append(r)
        identities[(r['date'],r['home_team'],r['away_team'])].append(r)
    for key,rows in pairs.items():
        if len(rows)>1:issue(rows[0]['source_row'],'duplicate_fixture',dict(fixture=key,source_rows=[r['source_row'] for r in rows],scores=[(r['date'],r['home_goals'],r['away_goals']) for r in rows]))
    for key,rows in identities.items():
        if len(rows)>1:
            conflict=len({(r['home_goals'],r['away_goals']) for r in rows})>1
            issue(rows[0]['source_row'],'conflicting_duplicate' if conflict else 'duplicate_match',dict(identity=key,source_rows=[r['source_row'] for r in rows]))
    missing=sorted({(h,a) for h in teams for a in teams if h!=a}-set(pairs))
    if total!=expected:issue(None,'match_count',f'{total} rows, expected {expected}')
    if len(records)!=total:issue(None,'unparsed_records',f'{total-len(records)} records could not be parsed')
    if len(teams)!=n:issue(None,'team_count',f'{len(teams)}, expected {n}')
    if missing:issue(None,'missing_pairings',missing)
    balance={t:dict(home=sum(r['home_team']==t for r in records),away=sum(r['away_team']==t for r in records)) for t in teams}
    if any(v['home']!=n-1 or v['away']!=n-1 for v in balance.values()):issue(None,'unbalanced_home_away',balance)
    if kind=='early' and (set(rounds)!=set(range(1,2*n-1)) or any(c!=n//2 for c in rounds.values())):issue(None,'round_completeness',dict(rounds))
    validator='NOT_RUN_EMPTY'
    if records:
        try:validate_historical_data(pd.DataFrame(records));validator='PASS'
        except ValueError as exc:validator='FAIL';issue(None,'historical_validator',str(exc))
    if kind=='early':notes.append('Source date/game-count annotations parsed in memory; original bytes unchanged. No independent Result column exists.')
    if optional_missing:notes.append('Optional empty fields retained; not missing required match results.')
    dates=sorted(r['date'] for r in records)
    result = dict(season=season,source_kind=kind,matches=total,parsed_matches=len(records),expected_matches=expected,
                teams=len(teams),expected_teams=n,first_date=dates[0] if dates else '',last_date=dates[-1] if dates else '',
                missing_pairings=len(missing),duplicate_fixtures=sum(len(v)-1 for v in pairs.values()),
                historical_validator=validator,optional_missing=dict(optional_missing),notes=notes,issues=issues,
                team_names=teams,balance=balance,round_counts=dict(rounds),status='REVIEW' if issues else 'PASS')
    # Expose the already validated source adapter to offline standardization;
    # the default structural-report bytes remain unchanged.
    if include_records:
        result['records'] = records
    return result


def main():
    manifest=json.loads((PRIVATE/'acquisition.json').read_text());results=[]
    for start in range(1990,2026):
        season=f'{start}/{start+1}';entry=manifest['files'].get(season)
        if entry is None:
            results.append(dict(season=season,status='MISSING',matches=0,issues=[dict(code='missing_file')]))
            continue
        path=PRIVATE/entry['file']
        if hashlib.sha256(path.read_bytes()).hexdigest()!=entry['sha256']:raise ValueError('Checksum mismatch: '+str(path))
        expected_suffix=(f'1990s/{start}-{(start+1)%100:02d}/1-bundesliga.csv' if start<1993 else f'season-{start%100:02d}{(start+1)%100:02d}.csv')
        if not entry['url'].endswith(expected_suffix):raise ValueError('Season/source URL mismatch: '+season)
        result=audit_file(path,season,entry['source_kind']);result.update(source_url=entry['url'],file=entry['file'],sha256=entry['sha256'])
        results.append(result)
    output=dict(scope='1990/1991–2025/2026, source CSV structural audit only',as_of=AS_OF.isoformat(),
                acquisition_sha256=hashlib.sha256((PRIVATE/'acquisition.json').read_bytes()).hexdigest(),
                seasons=results,total_matches=sum(s['matches'] for s in results),
                statuses=dict(Counter(s['status'] for s in results)))
    content=(json.dumps(output,indent=2,ensure_ascii=False)+'\n').encode()
    # Diagnostics may be regenerated byte-for-byte; differing results require review.
    target=PRIVATE/'structural_validation.json'
    if target.exists() and target.read_bytes()!=content:raise ValueError('Refusing differing audit output')
    if not target.exists():target.write_bytes(content)
    print(json.dumps(dict(seasons=len(results),matches=output['total_matches'],statuses=output['statuses'],issue_counts=dict(Counter(i['code'] for s in results for i in s['issues']))),indent=2))


if __name__=='__main__':main()
