"""Offline, lossless Phase 2 assessment; never correct, merge or standardize.

Every source record retains physical line, literal source fields and source SHA.
Unknown grammar fails explicitly. Long rounds and unusual scores are review flags.
"""
import argparse
from collections import Counter, defaultdict
import csv
from datetime import date
import io
import json
import re
import unicodedata

from scripts import collect_ligue1_feasibility as c
from scripts.validate_segunda_feasibility import fixture

PRIVATE = c.PRIVATE
HIST = 'jalapic/engsoccerdata/data-raw/france.csv'
OUTPUT = 'feasibility_assessment.json'
MONTHS = {s: n+1 for n, s in enumerate('Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split())}
DAYS = 'Mon Tue Wed Thu Fri Sat Sun'.split()


def goals(value):
    if value is None or value in ('', 'NA'):
        return None
    if not isinstance(value, str) or not re.fullmatch(r'\d+', value):
        raise ValueError('Invalid goal value')
    return int(value)


def outcome(h, a):
    return None if h is None or a is None else 'H' if h > a else 'A' if h < a else 'D'


def historical(raw):
    text = raw.decode('utf-8-sig'); lines = text.splitlines()
    reader = csv.DictReader(io.StringIO(text, newline=''))
    required = {'Date', 'Season', 'home', 'visitor', 'FT', 'hgoal', 'vgoal', 'division', 'tier', 'totgoal', 'goaldif', 'result'}
    if set(reader.fieldnames or ()) != required or len(reader.fieldnames) != len(required):
        raise ValueError('Historical headers changed')
    rows = []
    for r in reader:
        if None in r or any(v is None for v in r.values()) or not re.fullmatch(r'\d{4}', r['Season']):
            raise ValueError('Invalid CSV row shape/season')
        rows.append(dict(source_line=reader.line_num, raw_record=lines[reader.line_num-1],
                         source_fields=r, date=r['Date'], home=r['home'], away=r['visitor'],
                         hg=r['hgoal'], ag=r['vgoal'], FT=r['FT'], HT=None,
                         stage='SOURCE_TIER1_NO_EXPLICIT_STAGE' if r['tier'] == '1' else 'OTHER_TIER',
                         round=None, annotation='', season=f"{r['Season']}/{int(r['Season'])+1}",
                         date_semantics='SOURCE_DATE_ONLY_NOT_HISTORICALLY_CERTIFIED'))
    return rows


def parse_date(s, year):
    m = re.fullmatch(r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun) ([A-Z][a-z]{2}) (\d{1,2})(?: (\d{4}))?(?: (\d{1,2}:\d{2}) UTC[+-]\d+(?:.*))?', s)
    if not m:
        return None
    weekday, month, day, explicit, time = m.groups(); found = []
    for y in (int(explicit),) if explicit else (year, year+1):
        try:
            d = date(y, MONTHS[month], int(day))
        except (ValueError, KeyError):
            continue
        if date(year, 7, 1) <= d <= date(year+1, 6, 30) and DAYS[d.weekday()] == weekday:
            found.append(d.isoformat())
    if len(found) != 1:
        raise ValueError('Ambiguous/invalid source date or weekday: '+s)
    return dict(date=found[0], date_heading=s, year_explicit=bool(explicit), source_time=time)


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
            if title or not re.search(r'\bLigue 1\b', s) or not season or int(season[1]) != year or int(season[2]) % 100 != (year+1) % 100:
                raise ValueError('Wrong/duplicate competition/season title')
            title = True; notes.append(dict(line=number, kind='competition_title', text=s)); continue
        if s.startswith('▪'):
            label = s[1:].strip(); m = re.fullmatch(r'(?:Matchday|Regular Season -) (\d+)', label)
            if m:
                stage = 'REGULAR_SEASON'; round_id = int(m[1])
                if not 1 <= round_id <= (34 if year >= 2023 else 38):
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


def expected_clubs(year):
    if year < 1990:
        return None
    return 18 if 1997 <= year <= 2001 or year >= 2023 else 20


def assess(rows, year):
    teams = sorted({r[k] for r in rows for k in ('home', 'away')}); pairs = defaultdict(list)
    dates = []; invalid_dates = []; invalid_scores = []; unscored = []; scored = 0
    contradictory = []; unusual = []; normalized = defaultdict(list); events = defaultdict(list)
    for name in teams:
        normalized[unicodedata.normalize('NFC', name).casefold()].append(name)
    for r in rows:
        line = r['source_line']; pairs[r['home'], r['away']].append(line)
        try:
            day = date.fromisoformat(r['date'])
            if day.isoformat() != r['date'] or not date(year, 7, 1) <= day <= date(year+1, 6, 30):
                raise ValueError()
            dates.append(r['date'])
        except (ValueError, TypeError):
            invalid_dates.append(line)
        events[r['date'], r['home']].append(line); events[r['date'], r['away']].append(line)
        try:
            h, a = goals(r['hg']), goals(r['ag'])
            if h is None and a is None:
                unscored.append(line); continue
            if h is None or a is None:
                raise ValueError()
            scored += 1
            if r['FT'] != f'{h}-{a}':
                contradictory.append(dict(line=line, kind='FT_GOALS_CONFLICT'))
            fields = r.get('source_fields')
            if fields:
                if fields['result'] != outcome(h, a):
                    contradictory.append(dict(line=line, kind='RESULT_LABEL_GOALS_CONFLICT', source=fields['result'], goal_derived=outcome(h,a)))
                if fields['totgoal'] != str(h+a) or fields['goaldif'] != str(h-a):
                    contradictory.append(dict(line=line, kind='DERIVED_GOAL_FIELDS_CONFLICT'))
            if max(h, a) >= 7 or h+a >= 10:
                unusual.append(dict(line=line, date=r['date'], home=r['home'], away=r['away'], FT=r['FT']))
        except (ValueError, TypeError):
            invalid_scores.append(line)
    missing = [[h,a] for h in teams for a in teams if h != a and (h,a) not in pairs]
    duplicates = [dict(home=h, away=a, lines=ls) for (h,a),ls in sorted(pairs.items()) if len(ls)>1]
    rounds = defaultdict(list)
    for r in rows:
        if r.get('round') is not None:
            rounds[str(r['round'])].append(r)
    wide = []
    for rnd, matches in sorted(rounds.items(), key=lambda x: int(x[0]) if x[0].isdigit() else 1000):
        ds = sorted(m['date'] for m in matches); span = (date.fromisoformat(ds[-1])-date.fromisoformat(ds[0])).days
        if span > 14:
            wide.append(dict(round=rnd, first_date=ds[0], last_date=ds[-1], span_days=span,
                             fixtures=[dict(source_line=m['source_line'],date=m['date'],home=m['home'],away=m['away'],FT=m['FT'],annotation=m['annotation']) for m in matches]))
    n = expected_clubs(year)
    return dict(season=f'{year}/{year+1}', observed=len(rows), scored=scored, unscored=len(unscored),
                invalid_scores=invalid_scores, unscored_lines=unscored, clubs=len(teams), team_names=teams,
                expected_clubs=n, expected_scheduled=n*(n-1) if n else None,
                expected_played=279 if year == 2019 else n*(n-1) if n else None,
                dates=dict(first=min((r['date'] for r in rows),default=None),last=max((r['date'] for r in rows),default=None),
                           distinct=len({r['date'] for r in rows}), outside_or_invalid_lines=invalid_dates,
                           concentrated_dates=[dict(date=d,count=k) for d,k in sorted(Counter(r['date'] for r in rows).items()) if k>max(20,len(teams))]),
                missing_directed_pairs=missing, duplicate_directed_pairs=duplicates,
                invalid_team_lines=[r['source_line'] for r in rows if not r['home'].strip() or not r['away'].strip() or r['home']==r['away'] or any(t != t.strip() or '\ufffd' in t for t in (r['home'],r['away']))],
                normalized_name_collisions={k:v for k,v in normalized.items() if len(v)>1},
                team_date_collisions=[dict(date=d,team=t,lines=ls) for (d,t),ls in sorted(events.items()) if len(ls)>1],
                contradictions=contradictory, unusual_scores=unusual, wide_rounds=wide,
                annotations=[dict(line=r['source_line'],home=r['home'],away=r['away'],date=r['date'],FT=r['FT'],annotation=r['annotation']) for r in rows if r['annotation']],
                stage_counts=dict(Counter(r['stage'] for r in rows)),
                warning='Counts/pairings/date parsing are structural evidence only; stage and historical date/result validity require independent review.')


def compare(left, right, mapping=None):
    """Explicit bijection only; preserve unmatched, duplicate and conflicting facts."""
    mapping = mapping or {t:t for r in right for t in (r['home'],r['away'])}
    names = {r[k] for r in right for k in ('home','away')}
    if set(mapping) != names or len(set(mapping.values())) != len(mapping):
        raise ValueError('Diagnostic mapping must cover right-side labels bijectively')
    l = defaultdict(list); rr = defaultdict(list)
    for r in left:
        l[r['home'], r['away']].append(r)
    for r in right:
        rr[mapping[r['home']], mapping[r['away']]].append(r)
    diffs = []; matched = 0
    for key in sorted(set(l)&set(rr)):
        if len(l[key]) != 1 or len(rr[key]) != 1:
            continue
        a,b = l[key][0],rr[key][0]; matched += 1
        delta = {k:dict(left=a[k],right=b[k]) for k in ('date','hg','ag') if a[k] != b[k]}
        if delta:
            diffs.append(dict(home=key[0],away=key[1],left_line=a['source_line'],right_line=b['source_line'],differences=delta))
    return dict(matched_pairs=matched, mapping=mapping, discrepancies=diffs,
                unmatched_left=[list(k) for k in sorted(set(l)-set(rr))], unmatched_right=[list(k) for k in sorted(set(rr)-set(l))],
                duplicate_left=[list(k) for k,v in l.items() if len(v)>1],duplicate_right=[list(k) for k,v in rr.items() if len(v)>1],
                independence='Unestablished; not independent historical certification. No mapping applied to source or standardized data.')


# Diagnostic 2014/15 correspondence only; verified by bijective fixture comparison.
OVERLAP_NAMES = {
    'AS Monaco':'AS Monaco','AS Saint-Étienne':'AS Saint-Etienne','EA Guingamp':'EA Guingamp',
    'FC Lorient':'FC Lorient','FC Metz':'FC Metz','FC Nantes':'FC Nantes','Girondins Bordeaux':'Girondins Bordeaux',
    'Lille OSC':'Lille OSC','Montpellier HSC':'Montpellier HSC','OGC Nice':'OGC Nice',
    'Olympique Lyonnais':'Olympique Lyon','Olympique Marseille':'Olympique Marseille',
    'Paris Saint-Germain':'Paris Saint-Germain','RC Lens':'RC Lens','SC Bastia':'SC Bastia',
    'SM Caen':'SM Caen','Stade Rennais':'Stade Rennes','Stade de Reims':'Stade Reims',
    'Toulouse FC':'Toulouse FC','Évian Thonon Gaillard':'Evian Thonon Gaillard',
}

DIAGNOSTIC_VARIANTS = {
    'AS Monaco FC':'AS Monaco','AS Nancy Lorraine':'AS Nancy','AS Saint-Étienne':'AS Saint-Etienne',
    'Nîmes Olympique':'Nimes Olympique','Olympique Lyonnais':'Olympique Lyon',
    'Olympique de Marseille':'Olympique Marseille','Paris Saint-Germain FC':'Paris Saint-Germain',
    'RC Strasbourg Alsace':'RC Strasbourg','Racing Club de Lens':'RC Lens',
    'Stade Brestois 29':'Stade Brest','Stade Rennais':'Stade Rennes',
    'Stade Rennais FC 1901':'Stade Rennes','Stade de Reims':'Stade Reims',
    'Évian Thonon Gaillard':'Evian Thonon Gaillard',
}


def build(directory=PRIVATE, root=c.ROOT):
    protection = c.protect(directory,root); manifest = c.verify_originals(directory)
    historical_rows = historical((directory/HIST).read_bytes()); by_year = defaultdict(list)
    for r in historical_rows:
        by_year[int(r['season'][:4])].append(r)
    historic_reports = [assess(rows,y) for y,rows in sorted(by_year.items())]
    modern = []; parsed = {}
    for rec in manifest['files']:
        if rec['kind'] != 'dataset' or not rec['original_path'].endswith('.txt'):
            continue
        year = int(rec['original_filename'][:4]); raw=(directory/rec['path']).read_bytes()
        rows, notes = parse_text(raw,year,rec['original_filename'].endswith('-full.txt'))
        regular = [r for r in rows if r['stage']=='REGULAR_SEASON']; parsed[rec['original_filename']] = regular
        modern.append(dict(source=rec['path'],sha256=rec['sha256'],CRLF_lines=raw.count(b'\r\n'),
                           all_observations=len(rows),other_stage_records=len(rows)-len(regular),
                           assessment=assess(regular,year),records=rows,parser_notes=notes))
    overlap = compare(by_year.get(2014,[]),parsed['2014-15_fr1.txt'],OVERLAP_NAMES)
    overlaps = {}
    for year in (2016,2019,2023):
        modern_rows = parsed[f'{year}-{(year+1)%100:02}_fr1.txt']
        # Only played source observations are compared with the score-only CSV.
        scored = [r for r in modern_rows if r['hg'] is not None and r['ag'] is not None]
        mapping = {t:DIAGNOSTIC_VARIANTS.get(t,t) for r in scored for t in (r['home'],r['away'])}
        overlaps[str(year)] = compare(by_year.get(year,[]),scored,mapping)
    years=sorted(by_year)
    return dict(scope='Ligue 1 Phase 2 feasibility only; no corrections, exclusions, standardization or training',
                acquisition_sha256=c.sha((directory/'acquisition.json').read_bytes()),protected=protection,
                historical=dict(source=HIST,sha256=c.sha((directory/HIST).read_bytes()),rows=len(historical_rows),season_labels=years,
                                missing_labels_between_endpoints=sorted(set(range(years[0],years[-1]+1))-set(years)),
                                missing_target_1990_2013=sorted(set(range(1990,2014))-set(years)),
                                tiers=dict(Counter(r['source_fields']['tier'] for r in historical_rows)),
                                divisions=dict(Counter(r['source_fields']['division'] for r in historical_rows)),
                                stage_limit='No explicit round/stage field: division/tier and fixture structure cannot prove every row is regular season.',
                                seasons=historic_reports,records=historical_rows),
                modern=modern,overlap_2014=overlap,additional_overlaps=overlaps,
                versions_2025=compare(parsed['2025-26_fr1.txt'],parsed['2025-26_fr1-full.txt']),
                rights=manifest['rights'],canonical_league_proposed='Ligue 1')


if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    raw=c.encode(build());target=PRIVATE/OUTPUT
    if args.check:
        if target.read_bytes()!=raw:
            raise ValueError('Assessment not reproducible')
    else:
        c.save(target,raw)
    print('ASSESSMENT_BYTES',len(raw),'SHA256',c.sha(raw))
