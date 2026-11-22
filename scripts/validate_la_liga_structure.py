"""Offline Phase 4 validation; independent parsers, no fact repair or export.

All diagnostics stay private. --check requires byte-identical regeneration.
"""
import argparse
from collections import Counter,defaultdict
import csv
from datetime import date,timedelta
import io
import json
from pathlib import Path
import re
import unicodedata

from scripts.collect_la_liga_feasibility import ROOT,PRIVATE,sha
from scripts.collect_la_liga_history import protect,save
from scripts.validate_la_liga_feasibility import encode,ALIASES_2012
from toto_estimator.outcomes import outcome_from_goals
from toto_estimator.validation import exact_integer

OUTPUT='phase4_structural_validation.json'
HIST='jalapic/engsoccerdata/data-raw/spain.csv'
FIELDS=['Date','Season','home','visitor','HT','FT','hgoal','vgoal','tier','round','group','notes']
MONTHS={s:i+1 for i,s in enumerate('Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split())}
DAYS='Mon Tue Wed Thu Fri Sat Sun'.split()
# Diagnostic equivalences only, with bijective coverage checked per season.
# These are not standardized names or assertions of historical legal continuity.
ALIASES=dict(ALIASES_2012,**{'UD Almería':'UD Almeria','Córdoba CF':'Cordoba CF',
 'Sporting Gijón':'Sporting Gijon','CD Alavés':'CD Alaves','CD Leganés':'CD Leganes','Girona FC':'Girona',
 'Club Atlético de Madrid':'Atletico Madrid','Cádiz CF':'Cadiz CF','Deportivo Alavés':'CD Alaves',
 'RC Celta de Vigo':'Celta Vigo','Real Betis Balompié':'Real Betis','Real Madrid CF':'Real Madrid',
 'Real Sociedad de Fútbol':'Real Sociedad','Real Valladolid CF':'Real Valladolid',
 'RCD Espanyol de Barcelona':'Espanyol Barcelona','Rayo Vallecano de Madrid':'Rayo Vallecano',
 'Barcelona':'FC Barcelona','Villarreal':'Villarreal CF','Sevilla':'Sevilla FC',
 'Atlético de Madrid':'Atletico Madrid','RCD Espanyol':'Espanyol Barcelona','Real Madrid C.F.':'Real Madrid'})
STATUS=re.compile(r'\b(?:award(?:ed)?|abandon(?:ed)?|annul(?:led)?|postpon(?:ed|ement)|resum(?:ed|ption)|suspend(?:ed)?|cancel(?:led)?|replay(?:ed)?|aplazad[oa]|suspendid[oa]|reanud[ao]\w*)\b',re.I)


def parse_csv(raw):
    reader=csv.DictReader(io.StringIO(raw.decode('utf-8-sig')),strict=True)
    if reader.fieldnames!=FIELDS:raise ValueError('Historical header mismatch/duplicate columns')
    rows=[]
    for item in reader:
        if None in item or any(v is None for v in item.values()):raise ValueError(f'Historical malformed row {reader.line_num}')
        y=exact_integer(item['Season'])
        rows.append(dict(item,source_line=reader.line_num,start_year=y))
    return rows


def parse_text(raw,year):
    rows=[];notes=[];headers=[];current=None;stage=None;depth=0;last=False;title=False;previous_year=None
    for line_no,line in enumerate(raw.decode('utf-8-sig').splitlines(),1):
        s=line.strip()
        if not s:continue
        if depth or (last and s.startswith('(')):
            depth+=s.count('(')-s.count(')')
            if depth<0:raise ValueError(f'Unbalanced scorer text at line {line_no}')
            notes.append(dict(line=line_no,kind='scorer',text=s));continue
        last=False
        if s.startswith('#'):notes.append(dict(line=line_no,kind='comment',text=s));continue
        if s.startswith('='):
            if not re.search(r'Primera Divisi[oó]n',s):raise ValueError(f'Wrong competition at {line_no}')
            title=True
            stated=re.search(r'(\d{4})/(\d{2}|\d{4})(?!\d)',s)
            if stated and (int(stated[1])!=year or int(stated[2])!=(year+1 if len(stated[2])==4 else (year+1)%100)):
                raise ValueError(f'Contradictory title season at {line_no}')
            headers.append(dict(line=line_no,text=s));continue
        if s.startswith('▪'):
            m=re.fullmatch(r'▪\s*(Matchday|Regular Season -)\s+(\d+)',s)
            if not m:raise ValueError(f'Unknown/nonregular stage at {line_no}: {s}')
            stage=int(m[2]);notes.append(dict(line=line_no,kind='round',round=stage,text=s));continue
        dm=re.fullmatch(r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun) ([A-Z][a-z]{2}) (\d{1,2})(?: (\d{4}))?',s)
        if dm:
            if dm[2] not in MONTHS:raise ValueError(f'Unknown month at {line_no}')
            month=MONTHS[dm[2]]
            resolved=int(dm[4]) if dm[4] else year+int(month<7 or (year==2019 and previous_year==2020 and month in (7,8)))
            current=date(resolved,month,int(dm[3]));previous_year=resolved
            if DAYS[current.weekday()]!=dm[1]:notes.append(dict(line=line_no,kind='weekday_error',text=s))
            continue
        if not title or stage is None or current is None:raise ValueError(f'Match lacks competition/round/date at {line_no}')
        tm=re.match(r'^(\d{1,2}):(\d{2})\s+',s);kickoff=None
        if tm:
            if not 0<=int(tm[1])<=23 or not 0<=int(tm[2])<=59:raise ValueError(f'Invalid kickoff at {line_no}')
            kickoff=tm.group().strip();s=s[tm.end():]
        if re.search(r'\s+v\s+',s):
            home,rest=re.split(r'\s+v\s+',s,maxsplit=1)
            m=re.fullmatch(r'(.+?)\s{2,}([0-9]+)-([0-9]+)(?:\s+\(([0-9]+)-([0-9]+)\))?(\s+\[[^\]]+\])?',rest)
            if not m:raise ValueError(f'Unparsed/scoreless v fixture at {line_no}: {s}')
            away,hg,ag,hh,ha,annotation=m.groups()
        else:
            m=re.fullmatch(r'(.+?)\s{2,}([0-9]+)-([0-9]+)(?:\s+\(([0-9]+)-([0-9]+)\))?\s{2,}(.+?)(\s+\[[^\]]+\])?',s)
            if not m:raise ValueError(f'Unknown fixture at {line_no}: {s}')
            home,hg,ag,hh,ha,away,annotation=m.groups()
        rows.append(dict(source_line=line_no,date=current.isoformat(),home=home,away=away,hg=hg,ag=ag,
                         HT=None if hh is None else f'{hh}-{ha}',FT=f'{hg}-{ag}',round=stage,kickoff=kickoff,
                         annotation=(annotation or '').strip(),stage='league'))
        last=True
    if depth:raise ValueError('Unclosed scorer annotation')
    if not title:raise ValueError('Missing competition title')
    return rows,notes,headers


def csv_season(allrows,year):
    result=[]
    for r in allrows:
        if r['start_year']!=year:continue
        if r['tier']!='1' or r['round']!='league' or r['group'] not in ('NA',''):
            raise ValueError(f"Unexpected tier/stage/group in selected season, CSV line {r['source_line']}")
        result.append(dict(source_line=r['source_line'],date=r['Date'],home=r['home'],away=r['visitor'],hg=r['hgoal'],ag=r['vgoal'],
                           HT=None if r['HT'] in ('NA','') else r['HT'],FT=r['FT'],round=None,kickoff=None,stage='league',
                           annotation='' if r['notes'] in ('NA','') else r['notes']))
    return result


def validate(rows,year,n):
    errors=[];flags=[];valid=[];outcomes=Counter();pairs=defaultdict(list);dates=defaultdict(list);teams=set();halftime=0
    for r in rows:
        line=r['source_line'];problems=[]
        for t in (r['home'],r['away']):
            teams.add(t)
            if not t or t!=t.strip() or any(unicodedata.category(c)=='Cc' for c in t):problems.append('invalid_team_label')
            if '\ufffd' in t:problems.append('unicode_replacement')
        if r['home']==r['away']:problems.append('same_home_away')
        pairs[r['home'],r['away']].append(r)
        try:
            day=date.fromisoformat(r['date']);end=date(year+1,8,31) if year==2019 else date(year+1,6,30)
            if day.isoformat()!=r['date'] or not date(year,7,1)<=day<=end:problems.append('date_outside_season')
            for t in (r['home'],r['away']):dates[t].append((day,line))
        except (ValueError,TypeError):problems.append('invalid_date')
        try:
            h,a=exact_integer(r['hg']),exact_integer(r['ag'])
            if min(h,a)<0:raise ValueError()
            if r.get('FT')!=f'{h}-{a}':problems.append('FT_disagrees_with_goals')
            outcome=outcome_from_goals(h,a);outcomes[outcome]+=1
            if max(h,a)>=10:flags.append(dict(line=line,kind='unusually_high_score',score=f'{h}-{a}'))
            if r.get('HT') is not None:
                halftime+=1;m=re.fullmatch(r'(\d+)-(\d+)',r['HT'])
                if not m:problems.append('invalid_halftime')
                elif int(m[1])>h or int(m[2])>a:problems.append('halftime_exceeds_fulltime')
        except (ValueError,TypeError):problems.append('invalid_fulltime_goals')
        if r['annotation']:flags.append(dict(line=line,kind='source_annotation',text=r['annotation']))
        if problems:errors.append(dict(line=line,codes=sorted(set(problems))))
        else:valid.append(line)
    unique_errors=set(e['line'] for e in errors)
    for pair,rs in sorted(pairs.items()):
        if len(rs)>1:
            lines=[r['source_line'] for r in rs];unique_errors.update(lines)
            errors.append(dict(lines=lines,codes=['duplicate_ordered_pair'],pair=pair,
                               conflicting_scores=len({(r['hg'],r['ag']) for r in rs})>1))
    missing=sorted((h,a) for h in teams for a in teams if h!=a and (h,a) not in pairs)
    allocation={t:dict(home=sum(r['home']==t for r in rows),away=sum(r['away']==t for r in rows)) for t in sorted(teams)}
    allocation_errors={t:v for t,v in allocation.items() if v!={'home':n-1,'away':n-1}}
    for team,events in sorted(dates.items()):
        events.sort()
        for a,b in zip(events,events[1:]):
            gap=(b[0]-a[0]).days
            if gap==0:
                unique_errors.update((a[1],b[1]));errors.append(dict(lines=[a[1],b[1]],codes=['same_team_same_date'],team=team))
            elif gap==1:flags.append(dict(lines=[a[1],b[1]],kind='consecutive_day_matches',team=team,dates=[str(a[0]),str(b[0])]))
    forms=defaultdict(list)
    for t in sorted(teams):forms[unicodedata.normalize('NFC',t).casefold()].append(t)
    collisions={k:v for k,v in forms.items() if len(v)>1}
    if collisions:errors.append(dict(codes=['normalized_label_collision'],labels=collisions))
    expected=n*(n-1)
    if len(rows)!=expected:errors.append(dict(codes=['fixture_count'],observed=len(rows),expected=expected))
    if len(teams)!=n:errors.append(dict(codes=['team_count'],observed=len(teams),expected=n))
    if missing:errors.append(dict(codes=['missing_pairs'],pairs=missing))
    if allocation_errors:errors.append(dict(codes=['home_away_allocation'],teams=allocation_errors))
    rounds=Counter(r['round'] for r in rows if r['round'] is not None)
    if rounds:
        for rnd in sorted(rounds):
            appearances=Counter(t for r in rows if r['round']==rnd for t in (r['home'],r['away']))
            if set(appearances)!=teams or any(c!=1 for c in appearances.values()):
                errors.append(dict(codes=['round_team_allocation'],round=rnd,appearances=dict(appearances)))
        for half in (1,2):
            unordered=Counter(tuple(sorted((r['home'],r['away']))) for r in rows if (r['round']<=n-1)==(half==1))
            expected_pairs={tuple(sorted((h,a))) for h in teams for a in teams if h!=a}
            if set(unordered)!=expected_pairs or any(c!=1 for c in unordered.values()):
                errors.append(dict(codes=['half_season_opponent_coverage'],half=half))
    if rounds and (set(rounds)!=set(range(1,2*(n-1)+1)) or any(c!=n//2 for c in rounds.values())):
        errors.append(dict(codes=['round_coverage'],round_counts=dict(sorted(rounds.items()))))
    return dict(season=f'{year}/{year+1}',records=len(rows),expected=expected,clubs=len(teams),
                structurally_valid_fixture_records=len(rows)-len(unique_errors),fixture_error_records=len(unique_errors),
                errors=errors,flags=flags,outcomes=dict(sorted(outcomes.items())),halftime_records=halftime,
                team_names=sorted(teams),round_counts=dict(sorted(rounds.items())),
                first_date=min((r['date'] for r in rows),default=None),last_date=max((r['date'] for r in rows),default=None),
                status='STRUCTURAL_PASS' if not errors else 'STRUCTURAL_REVIEW')


def scheduling(rows,notes,span,season):
    round_id=int(re.search(r'(\d+)$',span['stage'])[1]);rs=[r for r in rows if r['round']==round_id]
    ds=sorted(r['date'] for r in rs)
    if min(ds)!=span['first'] or max(ds)!=span['last'] or sorted(r['source_line'] for r in rs)!=sorted(span['lines']):
        raise ValueError('Frozen scheduling candidate/source binding changed')
    # Largest seven-day cluster is a diagnostic reference, not the original schedule.
    windows=[(sum(d<=x<=str(date.fromisoformat(d)+timedelta(days=6)) for x in ds),d) for d in sorted(set(ds))]
    max_count=max(x[0] for x in windows);core=min(d for c,d in windows if c==max_count);end=str(date.fromisoformat(core)+timedelta(days=6))
    identify=lambda r:{k:r[k] for k in ('source_line','date','home','away','hg','ag')}
    outliers=[identify(r) for r in rs if not core<=r['date']<=end]
    repeated=sum(n['kind']=='round' and n.get('round')==round_id for n in notes)>1
    return dict(season=season,round=round_id,stage=span['stage'],earliest=ds[0],latest=ds[-1],span_days=(date.fromisoformat(ds[-1])-date.fromisoformat(ds[0])).days,
                earliest_fixtures=[identify(r) for r in rs if r['date']==ds[0]],latest_fixtures=[identify(r) for r in rs if r['date']==ds[-1]],
                all_round_fixtures=[identify(r) for r in rs],outside_densest_seven_day_cluster=outliers,
                source_hint='Repeated round heading with separate printed date blocks' if repeated else 'Different printed date blocks within one round heading',
                explicit_source_status_notes=[n for n in notes if n['kind']!='scorer' and STATUS.search(n['text'])],
                structural_error=False,decision='UNRESOLVED_HISTORICAL_SCHEDULING',
                limitation='The cluster and date dispersion do not establish postponement, advancement or resumption; no dates changed.')


def compare_sources(old,new,year):
    oldnames={r[k] for r in old for k in ('home','away')};newnames={r[k] for r in new for k in ('home','away')}
    mapping={n:n if n in oldnames else ALIASES.get(n) for n in sorted(newnames)}
    if None in mapping.values() or len(set(mapping.values()))!=len(mapping) or set(mapping.values())!=oldnames:
        raise ValueError(f'Unresolved diagnostic identity mapping {year}: {mapping}')
    older={(r['home'],r['away']):r for r in old}
    if len(older)!=len(old) or len(old)!=len(new):raise ValueError('Overlap fixture scope/duplicates')
    differences=[]
    for r in new:
        o=older.get((mapping[r['home']],mapping[r['away']]))
        if o is None:raise ValueError('Overlap pairing mismatch')
        changed={k:dict(historical=o[k],openfootball=r[k]) for k in ('date','hg','ag') if o[k]!=r[k]}
        if changed:differences.append(dict(home=o['home'],away=o['away'],historical_line=o['source_line'],openfootball_line=r['source_line'],differences=changed))
    return dict(season=f'{year}/{year+1}',compared=len(new),aliases={k:v for k,v in mapping.items() if k!=v},differences=differences,
                status='AGREEMENT' if not differences else 'UNRESOLVED_SOURCE_DISCREPANCY',
                limitation='Diagnostic names only; no source merging or proof of independent lineage or legal club continuity.')


def build(directory=PRIVATE):
    preservation=protect(directory)
    frozen=json.loads((directory/'phase4_protected_before.json').read_text())
    if len(frozen)!=52:raise ValueError('Unexpected Phase 2/3 protected scope')
    for name,digest in frozen.items():
        path=ROOT/name
        if not path.resolve().is_relative_to(ROOT.resolve()) or sha(path.read_bytes())!=digest:raise ValueError('Frozen evidence changed: '+name)
    inventory=json.loads((directory/'phase3_inventory.json').read_text())
    old=parse_csv((directory/HIST).read_bytes());parsed={};notes_by_year={};reports=[]
    for y in range(1990,2026):
        path=HIST if y<=2011 else f'openfootball/espana/{y}-{(y+1)%100:02}/1-liga.txt'
        try:
            if y<=2011:rows=csv_season(old,y);notes=[];headers=[]
            else:rows,notes,headers=parse_text((directory/path).read_bytes(),y)
        except (ValueError,TypeError,KeyError) as exc:raise ValueError(f'{y}/{y+1}, {path}: {exc}') from exc
        report=validate(rows,y,22 if y in (1995,1996) else 20)
        for n in notes:
            if n['kind']=='weekday_error':report['errors'].append(dict(line=n['line'],codes=['weekday_mismatch'],detail=n['text']));report['status']='STRUCTURAL_REVIEW'
        parsed[y]=rows;notes_by_year[y]=notes
        prior=next(r for r in inventory['seasons'] if r['season']==report['season'])
        facts=lambda r:(r['source_line'],r['date'],r['home'],r['away'],str(r['hg']),str(r['ag']))
        if Counter(map(facts,rows))!=Counter(map(facts,prior['records_detail'])):raise ValueError('Independent parser/inventory fact disagreement: '+report['season'])
        metadata=[]
        for note in notes:
            if note['kind']!='comment':continue
            stated=re.fullmatch(r'#\s*(Teams|Matches)\s+(\d+)',note['text'])
            if stated:
                observed=report['clubs'] if stated[1]=='Teams' else report['records']
                metadata.append(dict(line=note['line'],field=stated[1],stated=int(stated[2]),observed=observed))
                if int(stated[2])!=observed:report['errors'].append(dict(line=note['line'],codes=['source_header_count_disagreement'],field=stated[1]));report['status']='STRUCTURAL_REVIEW'
        report.update(file=path,competition_headers=headers,header_count_checks=metadata,source_status_notes=[n for n in notes if n['kind']!='scorer' and STATUS.search(n['text'])])
        reports.append(report)
    scheduling_cases=[]
    for c in inventory['review_candidates']:
        if c['kind']!='WIDE_ROUND_SPAN':raise ValueError('Unprocessed prior candidate type: '+c['kind'])
        y=int(c['season'][:4]);scheduling_cases.append(scheduling(parsed[y],notes_by_year[y],c['details'],c['season']))
    overlaps=[compare_sources(csv_season(old,y),parsed[y],y) for y in range(2012,2025)]
    first=next(c for c in overlaps if c['season']=='2012/2013')
    p2=json.loads((directory/'feasibility_assessment.json').read_text())['boundary']['overlap_2012']
    if first['differences'] or first['compared']!=p2['matches_compared'] or first['aliases']!={k:v for k,v in p2['aliases'].items() if k!=v}:
        raise ValueError('Phase 2 overlap finding changed')
    # Retain each old candidate with its original identity; no automatic disposition.
    p2keys={(c['season'],c['stage']) for c in inventory['phase2_candidates_carried_forward']}
    for c in scheduling_cases:c['origin']='PHASE_2' if (c['season'],c['stage']) in p2keys else 'PHASE_3'
    names=defaultdict(set)
    for y,rows in parsed.items():
        for r in rows:
            for k in ('home','away'):names[r[k]].add(f'{y}/{y+1}')
    changes=[]
    for y in range(1991,2026):
        previous={r[k] for r in parsed[y-1] for k in ('home','away')};current={r[k] for r in parsed[y] for k in ('home','away')}
        changes.append(dict(season=f'{y}/{y+1}',added_labels=sorted(current-previous),absent_labels=sorted(previous-current),
                            interpretation='Observed label changes only; promotion/relegation and spelling/entity changes require season-aware review, not automatic aliasing.'))
    exceptional_leads=[]
    for y,home,away,url,description in [
        (2004,'Real Madrid','Real Sociedad','https://as.com/futbol/2004/12/13/mas_futbol/1102892401_850215.html',
         'Earlier source-discovery lead describes continuation on 5 January after a December interruption; verify original event and date semantics independently.'),
        (2023,'Granada CF','Athletic Club','https://rfef.es/es/noticias/el-granada-athletic-se-reanudara-este-lunes-las-21-horas',
         'Earlier source-discovery RFEF lead describes continuation from minute 17 on 11 December; verify primary decision and final-result/date semantics.')]:
        matches=[r for r in parsed[y] if r['home']==home and r['away']==away]
        if len(matches)!=1:raise ValueError('Prior exceptional-match lead cannot bind uniquely')
        exceptional_leads.append(dict(season=f'{y}/{y+1}',file=reports[y-1990]['file'],record=matches[0],
                                     lead_url=url,description=description,evidence_status='PRIOR_DISCOVERY_LEAD_NOT_NEWLY_ACCESSED_OR_CERTIFIED',
                                     decision='UNRESOLVED_REQUIRES_PHASE5'))
    label_groups=defaultdict(list)
    for name,seasons in sorted(names.items()):
        label_groups[ALIASES.get(name,name)].append(dict(label=name,seasons=sorted(seasons)))
    label_variants={k:v for k,v in label_groups.items() if len(v)>1}
    phase2=[r for r in old if r['round']=='phase2']
    if len(phase2)!=len(inventory['historical_phase2_records_separate']) or any(1990<=r['start_year']<=2025 for r in phase2):
        raise ValueError('Unexpected historical phase2 scope')
    inputs={name:sha((ROOT/name).read_bytes()) for name in sorted(frozen)}
    input_paths=[directory/'phase4_protected_before.json',Path(__file__).resolve(),ROOT/'src/toto_estimator/validation.py',ROOT/'src/toto_estimator/outcomes.py',ROOT/'tests/test_la_liga_structure.py']
    inputs.update({str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in input_paths})
    all_fixture_issues=sum(r['fixture_error_records'] for r in reports)
    flag_lines={(r['season'],line) for r in reports for f in r['flags'] for line in f.get('lines',[f.get('line')]) if line is not None}
    round_lines={(c['season'],r['source_line']) for c in scheduling_cases for r in c['all_round_fixtures']}
    outlier_lines={(c['season'],r['source_line']) for c in scheduling_cases for r in c['outside_densest_seven_day_cluster']}
    differences=[dict(season=o['season'],**d) for o in overlaps for d in o['differences']]
    exceptional_lines={(c['season'],c['record']['source_line']) for c in exceptional_leads}
    focused_lines=round_lines|flag_lines|exceptional_lines
    return dict(date='2026-11-22',scope='Phase 4 structural assessment only; no independent historical certification',
                totals=dict(seasons=len(reports),records=sum(r['records'] for r in reports),expected=sum(r['expected'] for r in reports),
                            fixture_error_records=all_fixture_issues,structural_error_events=sum(len(r['errors']) for r in reports),
                            structurally_valid_fixture_records=sum(r['structurally_valid_fixture_records'] for r in reports),
                            plausibility_flagged_unique_records=len(flag_lines),round_flags=len(scheduling_cases),
                            records_in_flagged_rounds=len(round_lines),diagnostic_outlier_records=len(outlier_lines),
                            source_overlap_compared=sum(o['compared'] for o in overlaps),source_discrepancies=len(differences),
                            exceptional_lead_records=len(exceptional_lines),focused_historical_review_records=len(focused_lines),
                            independently_historically_certified_records=0,unlisted_historical_status='UNRESOLVED'),
                seasons=reports,scheduling_candidates=scheduling_cases,cross_source_comparisons=overlaps,
                source_discrepancies=differences,team_label_catalog={n:sorted(ss) for n,ss in sorted(names.items())},
                interseason_label_changes=changes,diagnostic_label_variant_groups=label_variants,exceptional_match_leads=exceptional_leads,
                historical_phase2_records_excluded_from_scope=len(phase2),
                notes='No source corrections, match exclusions or training eligibility decisions. Scheduling and plausibility flags are review leads, not automatic structural errors.',
                preservation=dict(**preservation,phase2_phase3_files=len(frozen)),inputs=inputs,
                rights=json.loads((directory/'acquisition.json').read_text())['rights'])


def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args();target=PRIVATE/OUTPUT
    if not args.check and target.exists():raise FileExistsError('Assessment exists; use --check')
    result=build();content=encode(result)
    if args.check:
        if target.read_bytes()!=content:raise ValueError('Structural assessment differs')
    else:save(target,content)
    print(json.dumps(result['totals'],indent=2))
    for r in result['seasons']:
        if r['errors'] or r['flags']:print(r['season'],r['errors'],r['flags'])


if __name__=='__main__':main()
