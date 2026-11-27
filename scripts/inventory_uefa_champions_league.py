"""Offline, lossless UCL Phase 2 inventory; no adjudication or canonical records.

The independent verifier has its own raw readers and does not import this module.
"""
import argparse
from collections import Counter, defaultdict
from datetime import date, datetime
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import tempfile
import unicodedata

from scripts import acquire_uefa_champions_league as acquisition
from scripts.artifact_io import check_overwrite

BASE = acquisition.BASE
PHASE = acquisition.PHASE
OUTPUT = PHASE / 'validated'
COLUMNS = ('Stage', 'Round', 'Group', 'Date', 'Team 1', 'FT', 'HT', 'Team 2', '∑FT', 'ET', 'P', 'Comments')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encode(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()


def score(token):
    if not token:
        return None
    m = re.search(r'(?<!\d)(\d+)-(\d+)(?!\d)', token)
    return [int(m[1]), int(m[2])] if m else None


def label(raw, kind):
    if kind == 'csv':
        parts = raw.split(' › ')
        if len(parts) != 2:
            return raw.strip(), None
        name, suffix = parts
        assoc = re.fullmatch(r'([A-Z]{3})(?: \(\d+\))?', suffix)
        return name.strip(), assoc[1] if assoc else None
    m = re.fullmatch(r'(.+?)\s+\(([A-Z]{3})\)', raw)
    return (m[1].strip(), m[2]) if m else (raw.strip(), None)


def stage(kind, raw_stage, raw_round, raw_group):
    text = raw_stage + ' ' + raw_round
    if kind == 'qualifying' or raw_stage == 'Qualifying' or 'Prelim.' in raw_round:
        if 'Prelim' in raw_round:
            return 'QUALIFYING', 'PRELIMINARY', None
        if re.search('play', raw_round, re.I):
            return 'QUALIFYING', 'QUALIFYING_PLAYOFF', None
        n = re.search(r'(?:Round\s+(\d+)|(\d+)\. Round)', raw_round)
        return 'QUALIFYING', 'QUALIFYING_ROUND_' + (next(x for x in n.groups() if x) if n else 'UNKNOWN'), None
    if raw_stage.startswith('Group') or re.search(r'\b(?:Group|Gruppe)\b', raw_round):
        second = raw_stage == 'Group 2nd' or raw_group.startswith('2|')
        letter = raw_group.split('|')[-1] if raw_group else None
        m = re.search(r'(?:Group|Gruppe) ([A-H])\b', raw_round)
        return 'MAIN', 'SECOND_GROUP' if second else 'FIRST_GROUP', letter or (m[1] if m else None)
    if raw_round.startswith('League,'):
        return 'MAIN', 'LEAGUE_PHASE', None
    if re.search('Play', raw_round):
        return 'MAIN', 'KNOCKOUT_PLAYOFF', None
    for needle, value in [('Round of 16', 'ROUND_OF_16'), ('Quarterfinal', 'QUARTERFINAL'),
                          ('Semifinal', 'SEMIFINAL'), ('Final', 'FINAL')]:
        if needle in text:
            return 'MAIN', value, None
    m = re.match(r'Round ([12])\b', raw_round)
    return ('MAIN', 'PRE_GROUP_ROUND_' + m[1], None) if m else ('UNKNOWN', 'UNKNOWN', None)


def fixture(rec, physical, first, last, fields, *, when, home, away, raw_stage, raw_round,
            raw_group='', kind='csv', periods=None, issues=(), date_precision='EXPLICIT_DAY', note=''):
    scope, normalized, group = stage(kind, raw_stage, raw_round, raw_group)
    hname, hassoc = label(home, 'csv' if kind == 'csv' else 'txt')
    aname, aassoc = label(away, 'csv' if kind == 'csv' else 'txt')
    m = re.search(r'Leg ([12])', raw_round)
    md = re.search(r'Matchday (\d+)', raw_round)
    row = dict(observation_id=sha(encode([rec['sha256'], first, last])), source=rec['path'],
               source_sha256=rec['sha256'], line=first, end_line=last,
               physical_sha256=sha(b''.join(physical[first-1:last])), publisher=rec['publisher'],
               season=rec['season'], source_fields=fields, date=when, date_precision=date_precision,
               raw_home=home, raw_away=away, home=hname, away=aname,
               home_association=hassoc, away_association=aassoc,
               raw_stage=raw_stage, raw_round=raw_round, raw_group=raw_group,
               scope=scope, stage=normalized, group=group, matchday=int(md[1]) if md else None,
               source_leg=int(m[1]) if m else None, replay='Replay' in raw_round,
               source_path_label=None, neutral_venue='UNVERIFIED', annotation=note,
               periods=periods, issues=list(issues), status='SCORED' if periods['regulation_time'] is not None else 'SCORE_PERIOD_UNRESOLVED')
    if scope == 'UNKNOWN':
        row['issues'].append('UNCLASSIFIED_STAGE')
    if not hname or not aname or hname == aname:
        row['issues'].append('INVALID_TEAM_IDENTITY')
    if when:
        y = int(rec['season'][:4]); day = date.fromisoformat(when)
        if not date(y, 6, 1) <= day <= date(y+1, 8, 31):
            row['issues'].append('DATE_OUTSIDE_SOURCE_SEASON_WINDOW')
    else:
        row['issues'].append('MISSING_EXACT_DATE')
    if periods['regulation_time'] is None:
        row['issues'].append('REGULATION_SCORE_UNKNOWN')
    ft, ht, aet = (periods[k] for k in ('regulation_time', 'half_time', 'after_extra_time'))
    if ft and ht and any(a < b for a, b in zip(ft, ht)):
        row['issues'].append('HALFTIME_EXCEEDS_REGULATION')
    if ft and aet and any(a < b for a, b in zip(aet, ft)):
        row['issues'].append('EXTRA_TIME_CUMULATIVE_CONTRADICTION')
    if re.search(r'award|abandon|cancel|postpon|void', note, re.I):
        row['status'] = 'EXCEPTIONAL_STATUS_ANNOTATION'
        row['issues'].append('ADMINISTRATIVE_OR_INTERRUPTED_CONTEXT')
    return row


def parse_csv(raw, rec):
    physical = raw.splitlines(keepends=True)
    reader = csv.reader(io.StringIO(raw.decode('utf-8-sig'), newline=''), strict=True)
    if tuple(next(reader)) != COLUMNS:
        raise ValueError('Unexpected FootballCSV schema')
    rows = []
    while True:
        first = reader.line_num + 1
        try:
            cells = next(reader)
        except StopIteration:
            break
        if len(cells) != len(COLUMNS):
            raise ValueError('CSV width mismatch at physical row ' + str(first))
        f = dict(zip(COLUMNS, cells)); issues = []
        dm = re.fullmatch(r'\(([A-Za-z]{3})\) (\d{1,2} [A-Za-z]{3} \d{4}) \(W\d+\)', f['Date'])
        when = None
        if dm:
            day = datetime.strptime(dm[2], '%d %b %Y').date(); when = day.isoformat()
            if day.strftime('%a') != dm[1]:
                issues.append('WEEKDAY_MISMATCH')
        else:
            issues.append('UNPARSED_DATE_FIELD')
        for key in ('FT', 'HT', 'ET', 'P', '∑FT'):
            if f[key] and not re.fullmatch(r'(?:\(a\) )?\d+-\d+(?: \(\*\)| \(a\.e\.t\.\)| \(pen\.\)| \(agg\.\))?', f[key]):
                issues.append('UNPARSED_SCORE_FIELD_' + key)
        periods = dict(regulation_time=score(f['FT']), half_time=score(f['HT']),
                       after_extra_time=score(f['ET']), shootout=score(f['P']), aggregate=score(f['∑FT']),
                       extra_time_only=None, unassigned_period_scores=[],
                       basis='EXPLICIT_NAMED_CSV_FIELDS', raw_score_fields={k: f[k] for k in ('FT', 'HT', 'ET', 'P', '∑FT')})
        for key, field in [('FT','regulation_time'),('HT','half_time'),('ET','after_extra_time'),('P','shootout'),('∑FT','aggregate')]:
            if 'UNPARSED_SCORE_FIELD_'+key in issues:periods[field]=None
        row=fixture(rec, physical, first, reader.line_num, f, when=when,
                            home=f['Team 1'], away=f['Team 2'], raw_stage=f['Stage'],
                            raw_round=f['Round'], raw_group=f['Group'], periods=periods,
                            issues=issues, note=f['Comments'])
        row['date_source_line']=first;row['stage_source_line']=first;rows.append(row)
    return rows


def txt_periods(text):
    """Never use the leading pair when ET/shootout syntax assigns another period."""
    result = dict(regulation_time=None, half_time=None, after_extra_time=None, shootout=None,
                  aggregate=None, extra_time_only=None, unassigned_period_scores=[],
                  basis='FOOTBALL_TXT_EXPLICIT_SYNTAX', raw_score_fields={'score_text': text})
    issues = []
    m = re.fullmatch(r'(?:(\d+-\d+) pen\. )?(\d+-\d+)( a\.e\.t\.)?(?: \((\d+-\d+)(?:, (\d+-\d+))?\))?(.*)', text)
    if not m:
        return result, ['UNPARSED_SCORE_SYNTAX']
    pen, leading, aet, first, second, tail = m.groups()
    result['shootout'] = score(pen)
    if aet:
        result['after_extra_time'] = score(leading)
        if first and second:
            result['regulation_time'], result['half_time'] = score(first), score(second)
        else:
            result['unassigned_period_scores'] = [score(first)] if first else []
            issues.append('ET_SINGLE_OR_MISSING_PARENTHESIS_PERIOD_AMBIGUITY')
    elif pen:
        result['unassigned_period_scores'] = [score(leading)] + ([score(first)] if first else [])
        issues.append('SHOOTOUT_WITHOUT_EXPLICIT_PERIOD_BASIS')
    else:
        result['regulation_time'], result['half_time'] = score(leading), score(first)
        if second:
            issues.append('UNEXPECTED_SECOND_PARENTHESIS_SCORE')
    if tail.strip():
        issues.append('UNPARSED_SCORE_TRAILER')
        if result['regulation_time'] is not None:
            result['unassigned_period_scores'].insert(0,result['regulation_time'])
            result['regulation_time']=None
    return result, issues


def parse_txt(raw, rec):
    physical = raw.splitlines(keepends=True); rows = []; heading = ''; day = None; precision = ''; date_issues = []; date_line=None;stage_line=None
    year = int(rec['season'][:4]); qualifying = '/clq.txt' in rec['path']
    for n, line in enumerate(physical, 1):
        s = line.decode('utf-8-sig').strip()
        if not s or s.startswith(('#', '=')):
            continue
        if s.startswith('▪'):
            heading = s[1:].strip(); day = None;stage_line=n;date_line=None;date_issues=[];precision=''
            continue
        dm = re.fullmatch(r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun) ([A-Z][a-z]{2}) (\d{1,2})(?: (\d{4}))?', s)
        if dm:
            candidates = []
            for y in [int(dm[4])] if dm[4] else [year, year+1]:
                d = datetime.strptime(f'{dm[2]} {dm[3]} {y}', '%b %d %Y').date()
                if date(year, 6, 1) <= d <= date(year+1, 8, 31) and d.strftime('%a') == dm[1]:
                    candidates.append(d.isoformat())
            date_line=n;date_issues = [] if len(candidates) == 1 else ['AMBIGUOUS_OR_INVALID_DATE_HEADING']
            day = candidates[0] if len(candidates) == 1 else None
            precision = 'EXPLICIT_HEADING_YEAR' if dm[4] else 'SOURCE_SEASON_WEEKDAY_RESOLVED_YEAR'
            continue
        body = re.sub(r'^\d{1,2}:\d{2}\s+', '', s)
        if ' v ' not in body:
            raise ValueError(f'Unrecognized physical source line {n}: {s}')
        home, tail = re.split(r'\s+v\s+', body, maxsplit=1)
        m = re.fullmatch(r'(.+?\([A-Z]{3}\))\s+(\d+-\d+.*)', tail)
        if not m:
            raise ValueError(f'Unparsed fixture at physical line {n}')
        away, token = m.groups(); periods, issues = txt_periods(token)
        row=fixture(rec, physical, n, n, {'raw_line': line.decode('utf-8-sig').rstrip('\r\n')},
                            when=day, home=home, away=away, raw_stage='', raw_round=heading,
                            kind='qualifying' if qualifying else 'txt', periods=periods,
                            issues=date_issues+issues, date_precision=precision, note=token)
        row['date_source_line']=date_line;row['stage_source_line']=stage_line;rows.append(row)
    return rows


def name_key(s):
    return ' '.join(unicodedata.normalize('NFC', s).split())


def reconcile(rows):
    """Conditional, source/season-bound correspondences; no global identity repair."""
    overlaps = []; names = []; membership = {r['observation_id']: r['observation_id'] for r in rows}
    for year in range(2011, 2016):
        season = f'{year}/{year+1}'
        left = [r for r in rows if r['season'] == season and r['scope'] == 'MAIN' and r['publisher'].startswith('footballcsv/')]
        right = [r for r in rows if r['season'] == season and r['publisher'].startswith('openfootball/')]
        buckets = defaultdict(list); votes = defaultdict(Counter); proofs = defaultdict(list)
        for r in left:
            if r['periods']['regulation_time'] is not None:
                buckets[(r['date'], r['stage'], tuple(r['periods']['regulation_time']))].append(r)
        for r in right:
            if r['periods']['regulation_time'] is None:
                continue
            candidates = buckets.get((r['date'], r['stage'], tuple(r['periods']['regulation_time'])), [])
            if len(candidates) == 1:
                p = candidates[0]
                for side in ('home', 'away'):
                    if p[side+'_association'] == r[side+'_association']:
                        votes[r[side]][p[side]] += 1
                        proofs[(r[side], p[side])].append([p['observation_id'], r['observation_id']])
        mapping = {}
        for r in right:
            for side in ('home', 'away'):
                source = r[side]
                exact = {p[s] for p in left for s in ('home', 'away')
                         if name_key(p[s]) == name_key(source) and p[s+'_association'] == r[side+'_association']}
                counts = votes[source]; best = counts.most_common()
                if len(exact) == 1:
                    mapping[source] = next(iter(exact))
                elif best and best[0][1] >= 2 and (len(best) == 1 or best[0][1] > best[1][1]):
                    mapping[source] = best[0][0]
        # Independently bound opponent/date topology supplies additional evidence
        # for rare labels whose score/date signature alone was not unique.
        for _ in range(len(right)+1):
            additions = {}
            for r in right:
                for side, other in (('home','away'),('away','home')):
                    if r[side] in mapping or r[other] not in mapping:
                        continue
                    candidates = [p for p in left if p['date']==r['date'] and p['stage']==r['stage']
                                  and p[other]==mapping[r[other]] and p[side+'_association']==r[side+'_association']]
                    if len(candidates)==1:
                        p=candidates[0]; key=(r[side],p[side])
                        proof=[p['observation_id'],r['observation_id']]
                        if proof not in proofs[key]:proofs[key].append(proof)
                        if len(proofs[key])>=2:additions[r[side]]=p[side]
            if not additions:break
            mapping.update(additions)
        if len(set(mapping.values())) != len(mapping):
            raise ValueError('Non-injective seasonal name correspondence')
        for a, b in sorted(mapping.items()):
            names.append(dict(season=season, source_publisher='openfootball/champions-league',
                              target_publisher='footballcsv/europe-champions-league', source_label=a,
                              target_label=b, evidence=proofs[(a,b)], status='CONDITIONAL_STRUCTURAL_CORRESPONDENCE_NOT_GLOBAL_ALIAS'))
        index = defaultdict(list)
        for r in left:
            index[(r['stage'], r['home'], r['away'])].append(r)
        seen = set()
        for r in right:
            candidates = index.get((r['stage'], mapping.get(r['home']), mapping.get(r['away'])), [])
            orientation='SAME'
            if not candidates and r['stage']=='FINAL':
                candidates=index.get((r['stage'],mapping.get(r['away']),mapping.get(r['home'])),[])
                orientation='REVERSED_SOURCE_DESIGNATION'
            # Orientation and stage identify the fixture independently of date/result agreement.
            if len(candidates) == 1:
                p = candidates[0]; seen.add(p['observation_id']); membership[r['observation_id']] = p['observation_id']
                compared = {k: None if p['periods'][k] is None or r['periods'][k] is None else p['periods'][k] == (r['periods'][k] if orientation=='SAME' else r['periods'][k][::-1])
                            for k in ('regulation_time', 'half_time', 'after_extra_time', 'shootout')}
                overlaps.append(dict(season=season, left=p['observation_id'], right=r['observation_id'],
                                     orientation=orientation,
                                     date_equal=p['date'] == r['date'], periods_equal=compared,
                                     status='CONDITIONAL_CORRESPONDENCE', independent_upstreams='NOT_ESTABLISHED'))
    return overlaps, names, membership


def primary(row):
    y = int(row['season'][:4])
    return row['publisher'].startswith('footballcsv/') if y <= 2015 else row['publisher'].startswith('openfootball/')


def structural(rows):
    reports = []
    for (season, source), group in sorted(_groups(rows, lambda r: (r['season'], r['source'])).items()):
        stages = Counter(r['stage'] for r in group); issues = []; directed = defaultdict(list)
        for r in group:
            directed[(r['stage'], r['group'], r['home'], r['away'])].append(r)
        repeated = [dict(observation_ids=[r['observation_id'] for r in rs], stage=k[0]) for k, rs in directed.items() if len(rs) > 1]
        # Replays are preserved and reviewed, never collapsed or silently removed.
        for rep in repeated:
            issues.append(dict(code='REPEATED_DIRECTED_PAIR', **rep))
        for (st, g), rs in _groups(group, lambda r: (r['stage'], r['group'])).items():
            if st not in ('FIRST_GROUP', 'SECOND_GROUP'):
                continue
            if g is None:
                issues.append(dict(code='GROUP_MEMBERSHIP_NOT_EXPLICIT', stage=st, records=len(rs)))
                continue
            clubs = {r[s] for r in rs for s in ('home', 'away')}
            pairs = {(r['home'], r['away']) for r in rs}
            if len(rs) != 12 or len(clubs) != 4 or len(pairs) != 12:
                issues.append(dict(code='GROUP_ROUND_ROBIN_MISMATCH', stage=st, group=g, records=len(rs), clubs=len(clubs)))
        league = [r for r in group if r['stage'] == 'LEAGUE_PHASE']
        if league:
            appearances = Counter(r[s] for r in league for s in ('home','away'))
            venues = Counter((r[s], s) for r in league for s in ('home','away'))
            opponents = defaultdict(set)
            for r in league:
                opponents[r['home']].add(r['away']); opponents[r['away']].add(r['home'])
            if len(league) != 144 or len(appearances) != 36 or any(v != 8 for v in appearances.values()) or any(v != 4 for v in venues.values()) or any(len(v) != 8 for v in opponents.values()):
                issues.append(dict(code='LEAGUE_PHASE_STRUCTURE_MISMATCH'))
        ties = []
        for (st, teams), rs in _groups(group, lambda r: (r['stage'], tuple(sorted((r['home'],r['away']))))).items():
            if st in ('FIRST_GROUP','SECOND_GROUP','LEAGUE_PHASE','FINAL') or st == 'UNKNOWN':
                continue
            actual = len(rs); special_single = season == '1993/1994' and st == 'SEMIFINAL' or season == '2019/2020' and st in ('QUARTERFINAL','SEMIFINAL')
            expected = 1 if special_single else 2
            reverse = actual == 2 and rs[0]['home'] == rs[1]['away'] and rs[1]['home'] == rs[0]['away']
            flags = []
            if actual != expected or expected == 2 and not reverse:
                flags.append('TIE_LEG_STRUCTURE_REVIEW')
            labels = [r['source_leg'] for r in rs]
            if any(x is not None for x in labels) and not (len(rs)==2 and sorted(labels)==[1,2]):
                flags.append('SOURCE_LEG_LABEL_REVIEW')
            ties.append(dict(stage=st, teams=teams, observations=[r['observation_id'] for r in rs], source_leg_labels=labels, issues=flags))
        reports.append(dict(season=season, source=source, records=len(group), stages=dict(stages), issues=issues, ties=ties))
    return reports


def _groups(rows, key):
    out = defaultdict(list)
    for r in rows:
        out[key(r)].append(r)
    return out


def build():
    manifest = acquisition.run(network=False); rows = []
    for rec in manifest['originals']:
        raw = (BASE / rec['path']).read_bytes()
        if sha(raw) != rec['sha256']:
            raise ValueError('Changed original')
        rows += parse_csv(raw, rec) if rec['path'].endswith('.csv') else parse_txt(raw, rec)
    ids = {r['observation_id'] for r in rows}
    if len(ids) != len(rows):
        raise ValueError('Duplicate source locator identity')
    overlap, names, membership = reconcile(rows); structure = structural(rows); issue_map = defaultdict(set)
    for r in rows:
        issue_map[r['observation_id']].update(r['issues'])
    for report in structure:
        for issue in report['issues']:
            for oid in issue.get('observation_ids', []):
                issue_map[oid].add(issue['code'])
        for tie in report['ties']:
            for oid in tie['observations']:
                issue_map[oid].update(tie['issues'])
    for link in overlap:
        bad = (['CROSS_SOURCE_DATE_CONFLICT'] if not link['date_equal'] else []) + ['CROSS_SOURCE_' + k.upper() + '_CONFLICT' for k,v in link['periods_equal'].items() if v is False]
        if link['orientation']!='SAME':bad.append('NEUTRAL_FINAL_SOURCE_ORIENTATION_DIFFERENCE')
        for oid in (link['left'],link['right']):
            issue_map[oid].update(bad)
    linked={x['right'] for x in overlap}
    for r in rows:
        if 2011<=int(r['season'][:4])<=2015 and r['publisher'].startswith('openfootball/') and r['observation_id'] not in linked:
            issue_map[r['observation_id']].add('UNMATCHED_OVERLAP_OBSERVATION')
    events = _groups(rows, lambda r: membership[r['observation_id']]); registry = []; matrix = []
    for key, group in sorted(events.items()):
        codes = sorted({c for r in group for c in issue_map[r['observation_id']]})
        registry.append(dict(event_id=sha(encode(sorted(r['observation_id'] for r in group))), season=group[0]['season'],
                             observations=sorted(r['observation_id'] for r in group), issues=codes,
                             status='REVIEW_REQUIRED' if codes else 'STRUCTURAL_CANDIDATE_ONLY'))
    for y in range(1992,2026):
        season=f'{y}/{y+1}'; selected=[r for r in rows if r['season']==season and primary(r)]
        main=[r for r in selected if r['scope']=='MAIN']; qual=[r for r in selected if r['scope']=='QUALIFYING']
        expected=73 if y==1992 else 75 if y==1993 else 61 if y<=1996 else 85 if y<=1998 else 157 if y<=2002 else 119 if y==2019 else 125 if y<=2023 else 189
        matrix.append(dict(season=season, primary_main_records=len(main), nominal_main_expected=expected,
                           main_replay_descriptions=sum(r['replay'] for r in main),
                           main_count_status='MATCHES_FORMAT_COUNT' if len(main)==expected else 'EXCEPTION_REVIEW',
                           primary_qualifying_records=len(qual), qualifying_gap=not qual,
                           main_regulation_known=sum(r['periods']['regulation_time'] is not None for r in main),
                           qualifying_regulation_known=sum(r['periods']['regulation_time'] is not None for r in qual),
                           main_stages=dict(Counter(r['stage'] for r in main)),qualifying_stages=dict(Counter(r['stage'] for r in qual)),
                           unique_main_clubs=len({r[s] for r in main for s in ('home','away')}),
                           source_observations=sum(r['season']==season for r in rows),
                           priority_rank=2026-y, numerical_time_weight=None,
                           assurance='SOURCE_INVENTORY_AND_FORMAT_CHECKS;NOT_HISTORICAL_ADJUDICATION'))
    queue=[e for e in registry if e['issues']]
    summary=dict(phase=2, observations=len(rows), conditional_events=len(registry), primary_observations=sum(primary(r) for r in rows),
                 overlap_links=len(overlap), review_events=len(queue), observation_issue_counts=dict(Counter(c for r in rows for c in issue_map[r['observation_id']])),
                 explicit_extra_time_observations=sum(r['periods']['after_extra_time'] is not None for r in rows),
                 shootout_observations=sum(r['periods']['shootout'] is not None for r in rows),
                 unknown_regulation_observations=sum(r['periods']['regulation_time'] is None for r in rows),
                 primary_unknown_regulation=sum(primary(r) and r['periods']['regulation_time'] is None for r in rows),
                 exact_duplicate_source_identities=0, canonical_records_generated=0, independent_upstreams='NOT_ESTABLISHED',
                 exact_duplicate_fixture_groups=sum(len(group)>1 for group in _groups(rows,lambda r:(r['source'],r['season'],r['stage'],r['group'],r['date'],r['home'],r['away'])).values()),
                 dispositions_assigned=False, numerical_time_weights='UNSPECIFIED;RECENT_FIRST_PRIORITY_ONLY')
    return {'source_inventory.json':dict(observations=rows,acquisition_manifest_sha256=sha((PHASE/'acquisition_manifest.json').read_bytes())),
            'structural_validation.json':dict(sources=structure,season_coverage=matrix),
            'overlap_assessment.json':dict(links=overlap,season_bound_names=names),
            'event_inventory.json':dict(events=registry),
            'unresolved_issues.json':dict(event_queue=queue,observation_issues=[dict(observation_id=r['observation_id'],codes=sorted(issue_map[r['observation_id']])) for r in rows if issue_map[r['observation_id']]],
                                          contexts=[dict(season=r['season'],code='QUALIFYING_SOURCE_GAP') for r in matrix if r['qualifying_gap']] +
                                          [dict(season=r['season'],source=r['source'],code=i['code']) for r in structure for i in r['issues'] if i['code']=='GROUP_MEMBERSHIP_NOT_EXPLICIT']),
            'summary.json':summary}


def run(output=OUTPUT, check=False):
    if output.resolve().is_relative_to(acquisition.ROOT.resolve()) and not output.resolve().is_relative_to(PHASE.resolve()):
        raise ValueError('Detailed inventory destination must be private or temporary')
    allowed=(PHASE.resolve(),Path(tempfile.gettempdir()).resolve(),Path('/private/tmp').resolve())
    if not any(output.resolve().is_relative_to(root) for root in allowed):
        raise ValueError('Detailed inventory destination must be private or temporary')
    artifacts=build()
    for name, value in artifacts.items():
        raw=encode(value); path=output/name
        if check:
            if path.read_bytes()!=raw:raise ValueError('Offline reproduction differs: '+name)
        else:
            check_overwrite([path]); path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(raw)
    return artifacts


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');parser.add_argument('--output',type=Path,default=OUTPUT)
    args=parser.parse_args();result=run(args.output,args.check);print(json.dumps(result['summary.json'],indent=2))
