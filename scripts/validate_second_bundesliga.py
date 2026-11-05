"""Offline source-schema/format audit; never standardization or model integration.

PYTHONPATH=src .venv/bin/python -m scripts.validate_second_bundesliga [--check]
Original bytes are read-only. Derived source-schema extract and diagnostics stay private.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import csv
from datetime import date, datetime
import io
import json
from pathlib import Path
import re

import pandas as pd
from scripts.acquire_second_bundesliga import PRIVATE, sha, save_once
from scripts.artifact_io import serialize_csv
from toto_estimator.data import validate_historical_data
from toto_estimator.historical_import import canonical_season
from toto_estimator.outcomes import outcome_from_goals
from toto_estimator.validation import exact_integer, team_name

AS_OF=date(2026,11,5)
ENG='originals/engsoccerdata_germany.csv'
MAIN='originals/openfootball_2025-26_2-bundesliga2.txt'
OPENLIGA='originals/openfootball_openliga_2025-26_de.2.txt'
ALL='originals/AllBundesligaGamesEver.csv'
MONTHS={name:i for i,name in enumerate(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],1)}


def format_for(year):
    if not 1990<=year<=2025:raise ValueError('Completed season starts must be 1990–2025')
    teams=24 if year in (1991,1992) else 20 if year in (1990,1993) else 18
    return dict(season=f'{year}/{year+1}',teams=teams,matches=384 if year==1991 else teams*(teams-1))


def read_original(directory,name):
    path=directory/name;content=path.read_bytes()
    receipt=json.loads(path.with_name(path.name+'.provenance.json').read_text())
    if receipt['status']!=200 or sha(content)!=receipt['sha256'] or len(content)!=receipt['bytes']:
        raise ValueError('Original checksum/status mismatch: '+name)
    return content,receipt


def parse_eng(content):
    reader=csv.DictReader(io.StringIO(content.decode('utf-8-sig'),newline=''),strict=True)
    expected=('Date','Season','home','visitor','FT','hgoal','vgoal','tier','division')
    if tuple(reader.fieldnames or ())!=expected:raise ValueError('Unexpected engsoccerdata schema')
    selected=[];records=[];issues=[]
    for row in reader:
        line=reader.line_num
        if None in row or any(v is None for v in row.values()):raise ValueError('Malformed source CSV row')
        if row['tier']!='2':continue
        try:year=exact_integer(row['Season'])
        except ValueError:raise ValueError('Ambiguous tier-2 season')
        if not 1990<=year<=2024:continue
        selected.append(row)
        season=canonical_season(f'{year}/{year+1}')
        try:
            if any(not str(v).strip() or v=='NA' for v in row.values()):raise ValueError('Missing required field')
            expected_divisions={'2North','2South'} if year==1991 else {'2'}
            if row['division'] not in expected_divisions:raise ValueError('Wrong competition/division')
            day=date.fromisoformat(row['Date'])
            if day.isoformat()!=row['Date'] or day.year not in (year,year+1) or day>AS_OF:
                raise ValueError('Invalid/out-of-season date')
            names=[team_name(row[k]) for k in ('home','visitor')]
            if names!=[row[k] for k in ('home','visitor')] or names[0]==names[1]:raise ValueError('Invalid team names')
            h,a=exact_integer(row['hgoal']),exact_integer(row['vgoal'])
            if min(h,a)<0 or row['FT']!=f'{h}-{a}':raise ValueError('FT/goals inconsistency')
            records.append(dict(source_row=line,season=season,date=row['Date'],home_team=names[0],away_team=names[1],
                                home_goals=h,away_goals=a,division=row['division']))
        except (ValueError,TypeError) as exc:issues.append(dict(source_row=line,season=season,code='invalid_source_field',detail=str(exc)))
    return list(expected),selected,records,issues


def parse_football_txt(content,season):
    """Observed full Football.TXT export subset, with fail-closed line diagnostics.

    Goal-event continuations and venues are not match rows. Missing scores remain
    unscored fixtures, not zeros. Calendar years derive from explicit season/month.
    """
    season=canonical_season(season);year=int(season[:4]);day=None;round_no=None
    records=[];issues=[];heading=None;fixtures=0
    for line_no,line in enumerate(content.decode('utf-8-sig').splitlines(),1):
        text=line.strip()
        if not text or text.startswith('#'):continue
        if text.startswith('='):
            if heading is not None:raise ValueError('Multiple competition sections')
            heading=text
            if not re.fullmatch(r'= (?:Deutsche 2\. Bundesliga|2\. Fußball-Bundesliga) '+re.escape(season)+r'|= Deutsche 2\. Bundesliga '+str(year)+r'/'+str((year+1)%100).zfill(2),text):
                raise ValueError('Wrong competition/season heading')
            continue
        rd=re.fullmatch(r'▪ (\d+)\. (?:Round|Spieltag)',text)
        if rd:
            round_no=int(rd[1]);day=None;continue
        dt=re.fullmatch(r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun) ([A-Z][a-z]{2}) (\d{1,2})(?: (\d{4}))?',text)
        if dt:
            month=MONTHS[dt[2]];y=int(dt[4]) if dt[4] else year+(month<7)
            try:
                parsed=date(y,month,int(dt[3]))
                if parsed.year not in (year,year+1) or parsed>AS_OF or parsed.strftime('%a')!=dt[1]:raise ValueError('Calendar/weekday mismatch')
                day=parsed.isoformat()
            except ValueError as exc:day=None;issues.append(dict(source_row=line_no,code='invalid_date',detail=str(exc)))
            continue
        if ' v ' in line:
            fixtures+=1
            home,tail=re.split(r'\s+v\s+',text,maxsplit=1)
            home=re.sub(r'^\d{1,2}:\d{2}\s+','',home)
            scored=re.fullmatch(r'(.+?)\s{2,}(\d+)-(\d+)(?:\s+\((\d+)-(\d+)\))?(?:\s+@.*)?',tail)
            away=scored[1] if scored else tail.split('  @')[0].strip()
            if not heading or day is None or round_no is None:
                issues.append(dict(source_row=line_no,code='missing_fixture_context',detail=text));continue
            if not scored:
                issues.append(dict(source_row=line_no,code='unscored_fixture',detail=text));continue
            h,a=exact_integer(scored[2]),exact_integer(scored[3])
            if scored[4] and (int(scored[4])>h or int(scored[5])>a):
                issues.append(dict(source_row=line_no,code='halftime_exceeds_fulltime',detail=text))
            if not home.strip() or not away.strip() or home.strip()==away.strip():
                issues.append(dict(source_row=line_no,code='invalid_teams',detail=text));continue
            records.append(dict(source_row=line_no,season=season,date=day,matchday=round_no,
                                home_team=home.strip(),away_team=away.strip(),home_goals=h,away_goals=a,division='2'))
            continue
        if re.match(r'^\(?\d+-\d+\s+',text):continue # goal events, not fixtures
        issues.append(dict(source_row=line_no,code='unrecognized_line',detail=text))
    if heading is None:raise ValueError('Missing competition heading')
    return records,issues,fixtures


def pairing_issues(rows,teams):
    counts=Counter((r['home_team'],r['away_team']) for r in rows)
    expected={(h,a) for h in teams for a in teams if h!=a}
    return dict(missing=sorted(expected-set(counts)),unexpected=sorted(set(counts)-expected),
                repeated=[dict(home=h,away=a,count=n) for (h,a),n in sorted(counts.items()) if n!=1])


def special_1991(rows):
    """Two 12-club regions: 132 first-phase + two six-club groups (60), each.

    The observed first phase is in 1991, second phase in 1992. This explicit
    season-specific boundary is tested, not inferred by taking the first 132 rows.
    """
    issues=[];regions=[];rosters=[]
    for division in ('2North','2South'):
        region=[r for r in rows if r['division']==division]
        first=[r for r in region if r['date']<'1992-01-01']
        second=[r for r in region if r['date']>='1992-01-01']
        teams={r[k] for r in region for k in ('home_team','away_team')};rosters.append(teams)
        if len(teams)!=12 or len(first)!=132 or len(second)!=60:
            issues.append(dict(code='regional_phase_counts',division=division,teams=len(teams),first=len(first),second=len(second)))
        first_pairs=pairing_issues(first,teams)
        if any(first_pairs.values()):issues.append(dict(code='regional_first_phase_pairings',division=division,detail=first_pairs))
        # Derive top/bottom six from the first-phase two-points table, then require
        # actual second-phase fixtures to be exactly those two independent schedules.
        stats={t:[0,0,0] for t in teams}
        for r in first:
            h,a=r['home_team'],r['away_team'];hg,ag=r['home_goals'],r['away_goals']
            if h not in stats or a not in stats:continue
            result=outcome_from_goals(hg,ag)
            stats[h][0]+=2 if result=='1' else 1 if result=='X' else 0
            stats[a][0]+=2 if result=='2' else 1 if result=='X' else 0
            stats[h][1]+=hg-ag;stats[a][1]+=ag-hg;stats[h][2]+=hg;stats[a][2]+=ag
        ranked=sorted(teams,key=lambda t:(*[-v for v in stats[t]],t))
        if len(ranked)>=7 and stats[ranked[5]]==stats[ranked[6]]:
            issues.append(dict(code='ambiguous_phase_group_boundary',division=division))
        groups=[]
        allowed=set()
        for label,group in [('promotion',set(ranked[:6])),('relegation',set(ranked[6:]))]:
            allowed|={(h,a) for h in group for a in group if h!=a}
            group_rows=[r for r in second if r['home_team'] in group and r['away_team'] in group]
            pairs=pairing_issues(group_rows,group)
            if len(group)!=6 or len(group_rows)!=30 or any(pairs.values()):
                issues.append(dict(code='second_phase_group_schedule',division=division,group=label,detail=pairs,actual=len(group_rows)))
            groups.append(dict(kind=label,teams=sorted(group),matches=len(group_rows),expected=30))
        outsiders=[r['source_row'] for r in second if (r['home_team'],r['away_team']) not in allowed]
        if outsiders:issues.append(dict(code='cross_group_second_phase_fixtures',division=division,source_rows=outsiders))
        balance={t:dict(home=sum(r['home_team']==t for r in region),away=sum(r['away_team']==t for r in region)) for t in sorted(teams)}
        if any(v!=dict(home=16,away=16) for v in balance.values()):issues.append(dict(code='regional_home_away_balance',division=division))
        regions.append(dict(division=division,teams=sorted(teams),first_phase_matches=len(first),second_phase_matches=len(second),
                            first_phase_last=max((r['date'] for r in first),default=None),second_phase_first=min((r['date'] for r in second),default=None),
                            groups=groups,balance=balance))
    if rosters[0]&rosters[1]:issues.append(dict(code='overlapping_regional_rosters'))
    return regions,issues


def validate_season(rows,year,source_count=None):
    fmt=format_for(year);issues=[];teams=sorted({r[k] for r in rows for k in ('home_team','away_team')})
    if len(rows)!=fmt['matches'] or len(teams)!=fmt['teams']:
        issues.append(dict(code='season_count',parsed=len(rows),expected=fmt['matches'],teams=len(teams)))
    if source_count is not None and source_count!=len(rows):issues.append(dict(code='unparsed_source_records',count=source_count-len(rows)))
    dated=defaultdict(list)
    for r in rows:dated[(r['date'],r['home_team'],r['away_team'])].append(r)
    for key,group in dated.items():
        if len(group)>1:
            conflicts=len({(r['home_goals'],r['away_goals']) for r in group})>1
            issues.append(dict(code='conflicting_duplicate' if conflicts else 'duplicate_match',fixture=key,source_rows=[r['source_row'] for r in group]))
    special=None
    if year==1991:
        special,phase_issues=special_1991(rows);issues.extend(phase_issues)
    else:
        pairs=pairing_issues(rows,teams)
        if any(pairs.values()):issues.append(dict(code='regular_season_pairings',detail=pairs))
    validator='NOT_RUN_EMPTY'
    if rows:
        try:validate_historical_data(pd.DataFrame(rows));validator='PASS'
        except ValueError as exc:validator='FAIL';issues.append(dict(code='historical_validator',detail=str(exc)))
    rounds=Counter(r['matchday'] for r in rows if 'matchday' in r)
    if rounds and (set(rounds)!=set(range(1,35)) or any(v!=9 for v in rounds.values())):
        issues.append(dict(code='round_completeness',counts=dict(rounds)))
    for matchday in rounds:
        participants=Counter(r[k] for r in rows if r['matchday']==matchday for k in ('home_team','away_team'))
        if set(participants)!=set(teams) or any(n!=1 for n in participants.values()):
            issues.append(dict(code='round_team_coverage',matchday=matchday))
    return dict(**fmt,actual_matches=len(rows),actual_teams=len(teams),first_date=min((r['date'] for r in rows),default=None),
                last_date=max((r['date'] for r in rows),default=None),issues=issues,
                special_format=special,historical_validator=validator,status='PASS' if not issues else 'REVIEW')


def build(directory=PRIVATE):
    directory=Path(directory);content,eng_receipt=read_original(directory,ENG)
    columns,selected,eng_records,parse_issues=parse_eng(content)
    open_content,open_receipt=read_original(directory,OPENLIGA)
    open_records,open_issues,open_fixtures=parse_football_txt(open_content,'2025/2026')
    main_content,main_receipt=read_original(directory,MAIN)
    main_records,main_issues,main_fixtures=parse_football_txt(main_content,'2025/2026')
    counts=Counter(int(r['Season']) for r in selected)
    records=eng_records+open_records;seasons=[]
    for year in range(1990,2026):
        season=f'{year}/{year+1}';result=validate_season([r for r in records if r['season']==season],year,counts[year] if year<2025 else open_fixtures)
        result['issues'].extend([i for i in parse_issues if i['season']==season] if year<2025 else open_issues)
        result['status']='REVIEW' if result['issues'] else 'PASS'
        result['source']='engsoccerdata' if year<2025 else 'OpenFootball/OpenLigaDB'
        seasons.append(result)
    all_content,all_receipt=read_original(directory,ALL)
    all_rows=[]
    for line,row in enumerate(csv.DictReader(io.StringIO(all_content.decode('utf-8')),delimiter=';'),2):
        if row['League']=='2. Bundesliga' and 1990<=int(row['SeasonFrom'])<=2025:
            all_rows.append(dict(row,source_row=line))
    comparison=[]
    for year in range(1990,2026):
        subset=[r for r in all_rows if int(r['SeasonFrom'])==year]
        duplicates=Counter((r['Date'],r['Home'],r['Guest'],r['Score90']) for r in subset)
        comparison.append(dict(season=f'{year}/{year+1}',raw_rows=len(subset),
                               exact_duplicate_excess=sum(n-1 for n in duplicates.values()),
                               source_flags=[r for r in subset if r['Aborted']=='True' or r['Annulled']=='True']))
    output=dict(reviewed_on=AS_OF.isoformat(),scope='Source-format extraction and structural validation only; not standardized match IDs or independent sample verification',
                expected_matches=11488,acquired_source_records=len(selected)+open_fixtures,parsed_scored_records=len(records),
                complete_fixture_seasons=sum(not s['issues'] for s in seasons),seasons=seasons,
                source_sha256={ENG:eng_receipt['sha256'],OPENLIGA:open_receipt['sha256'],MAIN:main_receipt['sha256'],ALL:all_receipt['sha256']},
                main_openfootball_2025=dict(fixtures=main_fixtures,scored=len(main_records),issues=main_issues,selected=False),
                allbundesliga_inventory=comparison,allbundesliga_selected=False,
                assurance='FT/goals consistency and calendar/schedule validity, not exhaustive historical correctness or certified finality. Administrative/replayed cases require separate evidence review.',
                extracted_records=records)
    return {'engsoccerdata_second_tier_1990_2024.csv':serialize_csv(selected,columns),
            'structural_validation.json':(json.dumps(output,indent=2,ensure_ascii=False)+'\n').encode()}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    outputs=build()
    for name,content in outputs.items():
        if args.check:
            if (PRIVATE/name).read_bytes()!=content:raise ValueError('Saved output differs: '+name)
        else:save_once(PRIVATE/name,content)
    report=json.loads(outputs['structural_validation.json'])
    print(json.dumps(dict(records=report['acquired_source_records'],scored=report['parsed_scored_records'],complete_fixture_seasons=report['complete_fixture_seasons'],
                          issues={s['season']:s['issues'] for s in report['seasons'] if s['issues']},main_openfootball_scored=report['main_openfootball_2025']['scored']),indent=2,ensure_ascii=False))


if __name__=='__main__':main()
