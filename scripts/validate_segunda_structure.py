"""Phase 4 offline independent raw parsing, validation and deduplicated review.

No acquisition, source repair, historical decision, screening or standardization.
"""
import argparse
from collections import Counter, defaultdict
from datetime import date
import hashlib
import json
import re
import unicodedata

from scripts import collect_segunda_feasibility as base
from scripts import collect_segunda_history as acquisition

ROOT, PRIVATE = base.ROOT, base.PRIVATE
BASELINE = 'phase4_protected_before.json'
REPORT = 'phase4_structural_validation.json'
QUEUE = 'phase4_review_queue.json'
PUBLIC = acquisition.PHASE2_PUBLIC + ('scripts/collect_segunda_history.py',
    'scripts/inventory_segunda_history.py', 'tests/test_segunda_history.py', 'docs/segunda-division-inventory.md')
MONTHS = {m: i+1 for i, m in enumerate('Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split())}
DAYS = 'Mon Tue Wed Thu Fri Sat Sun'.split()
FIELDS = ('source_line', 'raw_record', 'date', 'home', 'away', 'hg', 'ag', 'FT', 'HT',
          'round', 'stage', 'kickoff', 'annotation', 'source_marked_awarded')
RESERVES = {'Athletic Club B', 'FC Barcelona B', 'Real Madrid Castilla', 'Real Sociedad B',
            'Sevilla Atlético', 'Villarreal CF B'}


def initialize(directory=PRIVATE, root=ROOT):
    acquisition.protect(directory, root)
    target = directory/BASELINE
    if target.exists():
        return protect(directory, root)
    approved = json.loads((directory/'phase3_verification.json').read_text())
    for name, digest in approved['public_sha256'].items():
        if base.sha((root/name).read_bytes()) != digest:
            raise ValueError('Approved Phase 3 public file changed: '+name)
    for name, digest in approved['phase3_artifacts_sha256'].items():
        if base.sha((directory/name).read_bytes()) != digest:
            raise ValueError('Approved Phase 3 evidence changed: '+name)
    files = {str(p.relative_to(root)): base.sha(p.read_bytes()) for p in directory.rglob('*') if p.is_file()}
    files.update({n: base.sha((root/n).read_bytes()) for n in PUBLIC})
    log = (root/'PLANNING_LOG.md').read_bytes()
    base.save(target, base.encode(dict(files=files, planning_log=dict(bytes=len(log), sha256=base.sha(log)))))
    return protect(directory, root)


def protect(directory=PRIVATE, root=ROOT):
    previous = acquisition.protect(directory, root)
    saved = json.loads((directory/BASELINE).read_text())
    if not saved['files']:
        raise ValueError('Empty Phase 4 baseline')
    for name, digest in saved['files'].items():
        path = root/name
        if not path.resolve().is_relative_to(root.resolve()) or base.sha(path.read_bytes()) != digest:
            raise ValueError('Frozen existing artifact changed: '+name)
    raw = (root/'PLANNING_LOG.md').read_bytes(); prefix = saved['planning_log']
    if len(raw) < prefix['bytes'] or base.sha(raw[:prefix['bytes']]) != prefix['sha256']:
        raise ValueError('Planning history changed')
    return dict(previous=previous, phase2_3_files=len(saved['files']))


def source_id(file, digest, line):
    return 'segunda:'+base.sha(base.encode(dict(file=file, sha256=digest, line=line)))


def parse_source(raw, year):
    """Independent grammar, not the Phase 2/3 parser or saved parsed records.

    Preserve date headings and explicitly disclose inferred calendar years.
    Unknown syntax fails with physical source-line diagnostics.
    """
    text = raw.decode('utf-8-sig'); raw_lines = raw.splitlines(keepends=True)
    records = []; notes = []; header = {}; current = None; round_no = None
    heading_line = None; heading_text = None; year_basis = None; title = False; depth = 0
    for number, original in enumerate(text.splitlines(), 1):
        s = original.strip()
        if not s:
            continue
        def fail(message):
            raise ValueError(f'line {number}: {message}')
        if depth or s.startswith('('):
            if not records:
                fail('scorer annotation without a fixture')
            depth += s.count('(')-s.count(')')
            if depth < 0:
                fail('unbalanced scorer annotation')
            notes.append(dict(line=number, kind='scorer_annotation', text=s)); continue
        if s.startswith('='):
            if title or not re.search(r'Segunda Divisi[oó]n(?!\s+B\b)', s):
                fail('wrong/duplicate competition title')
            stated = re.search(r'(\d{4})/(\d{2}(?:\d{2})?)(?!\d)', s)
            if not stated or int(stated[1]) != year or int(stated[2]) != (year+1 if len(stated[2]) == 4 else (year+1) % 100):
                fail('missing/contradictory season')
            title = True; header['title'] = s; continue
        if s.startswith('#'):
            count = re.fullmatch(r'#\s*(Teams|Matches)\s+(\d+)', s)
            if count:
                if count[1] in header:
                    fail('duplicate count header')
                header[count[1]] = int(count[2])
            notes.append(dict(line=number, kind='comment', text=s)); continue
        if s.startswith('▪'):
            match = re.fullmatch(r'▪\s*(?:Matchday\s+(\d+)|(\d+)\. Round|Regular Season -\s+(\d+))', s)
            if not match:
                fail('unknown/nonregular stage')
            round_no = int(next(n for n in match.groups() if n is not None))
            current = None
            notes.append(dict(line=number, kind='round_header', round=round_no, text=s)); continue
        match = re.fullmatch(r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun) ([A-Z][a-z]{2}) (\d{1,2})(?: (\d{4}))?', s)
        if match:
            weekday, month, day, explicit_year = match.groups()
            if month not in MONTHS:
                fail('unknown month')
            candidates = []
            for candidate_year in ([int(explicit_year)] if explicit_year else [year, year+1]):
                try:
                    d = date(candidate_year, MONTHS[month], int(day))
                except ValueError:
                    continue
                end = date(year+1, 8, 31) if year == 2019 else date(year+1, 6, 30)
                if date(year, 7, 1) <= d <= end and DAYS[d.weekday()] == weekday:
                    candidates.append(d)
            if len(candidates) != 1:
                fail('ambiguous year, weekday contradiction or out-of-season date')
            current = candidates[0].isoformat(); heading_text = s; heading_line = number
            year_basis = 'EXPLICIT_IN_DATE_HEADING' if explicit_year else 'INFERRED_YEAR_SEASON_WINDOW_AND_WEEKDAY'
            continue
        if s.startswith('[') and s.endswith(']'):
            notes.append(dict(line=number, kind='status_note', text=s)); continue
        if not title or current is None or round_no is None:
            fail('fixture lacks competition/round/date')
        clock = re.match(r'^(\d{1,2}):(\d{2})\s+', s); kickoff = None
        if clock:
            if int(clock[1]) > 23 or int(clock[2]) > 59:
                fail('invalid kickoff time')
            kickoff = clock[1]+':'+clock[2]; s = s[clock.end():]
        annotation = ''
        annotation_match = re.search(r'\s+(\[[^\]]+\])$', s)
        if annotation_match:
            annotation = annotation_match[1]; s = s[:annotation_match.start()].rstrip()
        half = None
        if re.search(r'\s+v\s+', s):
            home, rest = re.split(r'\s+v\s+', s, maxsplit=1)
            columns = re.split(r'\s{2,}', rest)
            if len(columns) == 1:
                away = columns[0]
                if re.search(r'\d\s*-|-\s*\d|\?\s*-', away):
                    fail('malformed/partial FT score')
                h = a = None
            elif len(columns) == 2:
                away = columns[0]
                score = re.fullmatch(r'([0-9]+)-([0-9]+)(?:\s+\(([0-9]+-[0-9]+)\))?', columns[1])
                if not score:
                    fail('malformed FT/HT score')
                h, a, half = score.groups()
            else:
                fail('unexpected fixture columns')
        else:
            score = re.fullmatch(r'(.+?)\s{2,}([0-9]+)-([0-9]+)(?:\s+\(([0-9]+-[0-9]+)\))?\s{2,}(.+)', s)
            if not score:
                fail('unrecognized score-between-teams fixture')
            home, h, a, half, away = score.groups()
        records.append(dict(source_line=number, raw_record=original,
                            raw_line_sha256=base.sha(raw_lines[number-1]),
                            date=current, date_heading=heading_text, date_heading_line=heading_line,
                            year_basis=year_basis, home=home, away=away, hg=h, ag=a,
                            FT=None if h is None else h+'-'+a, HT=half, round=round_no,
                            stage='REGULAR_SEASON', kickoff=kickoff, annotation=annotation,
                            source_marked_awarded=bool(re.search('award', annotation, re.I))))
    if depth or not title or not records:
        raise ValueError('Incomplete source/annotation')
    return records, notes, header


def nonnegative_integer(value):
    if not isinstance(value, str) or not re.fullmatch(r'[0-9]+', value) or int(value) > 2**63-1:
        raise ValueError('Expected nonnegative integer source string')
    return int(value)


def validate(records, year, clubs=22):
    errors = defaultdict(set); flags = defaultdict(set); incomplete = set(); outcomes = Counter()
    pairs = defaultdict(list); rounds = defaultdict(list); events = defaultdict(list); names = set(); halftime = 0
    season_errors = []; calendar = {}; high_scores = []
    for r in records:
        line = r['source_line']; names.update((r['home'], r['away']))
        pairs[r['home'], r['away']].append(line); rounds[r['round']].append(r)
        for name in (r['home'], r['away']):
            if not name or name != name.strip() or '\ufffd' in name or any(unicodedata.category(c).startswith('C') for c in name):
                errors[line].add('INVALID_TEAM_LABEL')
        if r['home'] == r['away']:
            errors[line].add('SAME_HOME_AWAY')
        if r['stage'] != 'REGULAR_SEASON':
            errors[line].add('NONREGULAR_STAGE')
        try:
            day = date.fromisoformat(r['date']); end = date(year+1, 8, 31) if year == 2019 else date(year+1, 6, 30)
            if day.isoformat() != r['date'] or not date(year, 7, 1) <= day <= end:
                raise ValueError()
            calendar[line] = day
            for name in (r['home'], r['away']):
                events[name].append((day, line))
        except (ValueError, TypeError):
            errors[line].add('INVALID_DATE_OR_SEASON_BOUNDARY')
        if r['hg'] is None and r['ag'] is None:
            incomplete.add(line); flags[line].add('MISSING_FULLTIME_SCORE')
            if r['FT'] is not None:
                errors[line].add('MISSING_GOALS_WITH_FT_STRING')
        else:
            try:
                h, a = nonnegative_integer(r['hg']), nonnegative_integer(r['ag'])
                if r['FT'] != r['hg']+'-'+r['ag']:
                    raise ValueError()
                outcomes['1' if h > a else '2' if h < a else 'X'] += 1
                if max(h, a) >= 8 or h+a >= 10:
                    flags[line].add('UNUSUAL_SCORE_REVIEW'); high_scores.append(line)
                if r['HT'] is not None:
                    halftime += 1
                    hh, aa = r['HT'].split('-'); hh, aa = nonnegative_integer(hh), nonnegative_integer(aa)
                    if hh > h or aa > a:
                        raise ValueError('HT exceeds FT')
            except (ValueError, TypeError):
                errors[line].add('INVALID_OR_CONTRADICTORY_SCORE')
        if r['annotation']:
            flags[line].add('SOURCE_ANNOTATION')
        if r['source_marked_awarded']:
            flags[line].add('SOURCE_MARKED_ADMINISTRATIVE_AWARD')
        if r['home'] in RESERVES or r['away'] in RESERVES:
            flags[line].add('RESERVE_IDENTITY_REVIEW')
    for pair, lines in pairs.items():
        if len(lines) > 1:
            for line in lines:
                errors[line].add('DUPLICATE_DIRECTED_PAIR')
    missing = [(h, a) for h in sorted(names) for a in sorted(names) if h != a and (h, a) not in pairs]
    if len(records) != clubs*(clubs-1): season_errors.append('FIXTURE_COUNT')
    if len(names) != clubs: season_errors.append('CLUB_COUNT')
    if missing: season_errors.append('MISSING_DIRECTED_PAIRS')
    if set(rounds) != set(range(1, 2*(clubs-1)+1)): season_errors.append('ROUND_NUMBER_COVERAGE')
    allocation = {name: dict(home=sum(r['home'] == name for r in records), away=sum(r['away'] == name for r in records)) for name in sorted(names)}
    if any(v != dict(home=clubs-1, away=clubs-1) for v in allocation.values()): season_errors.append('APPEARANCE_ALLOCATION')
    for number, rs in rounds.items():
        appearances = Counter(n for r in rs for n in (r['home'], r['away']))
        if len(rs) != clubs//2 or set(appearances) != names or any(v != 1 for v in appearances.values()):
            season_errors.append('ROUND_ALLOCATION:'+str(number))
            for r in rs: errors[r['source_line']].add('ROUND_ALLOCATION')
    halves = []
    for half in (0, 1):
        rs = [r for r in records if half*(clubs-1) < r['round'] <= (half+1)*(clubs-1)]
        unordered = Counter(tuple(sorted((r['home'], r['away']))) for r in rs)
        okay = len(unordered) == clubs*(clubs-1)//2 and all(n == 1 for n in unordered.values())
        if not okay: season_errors.append('HALF_SEASON_PAIRING:'+str(half+1))
        halves.append(dict(half=half+1, unique_pairs=len(unordered), complete=okay))
    normalized = defaultdict(list)
    for name in sorted(names): normalized[unicodedata.normalize('NFC', name).casefold()].append(name)
    collisions = {k: v for k, v in normalized.items() if len(v) > 1}
    if collisions:
        season_errors.append('TEAM_IDENTITY_COLLISION')
        for r in records:
            if any(r['home'] in labels or r['away'] in labels for labels in collisions.values()):
                errors[r['source_line']].add('TEAM_IDENTITY_COLLISION')
    rest = []
    for name, appearances in events.items():
        appearances.sort()
        for (earlier, first), (later, second) in zip(appearances, appearances[1:]):
            if (later-earlier).days <= 1:
                kind = 'SAME_TEAM_DATE_COLLISION' if later == earlier else 'SHORT_REST_DATE_REVIEW'
                for line in (first, second):
                    (errors if later == earlier else flags)[line].add(kind)
                rest.append(dict(team=name, first_line=first, second_line=second, days=(later-earlier).days))
    reversals = []
    for first, second in zip(records, records[1:]):
        a, b = first['source_line'], second['source_line']
        if a in calendar and b in calendar and calendar[b] < calendar[a]:
            # A date reversal in round-ordered storage is not a factual error.
            reversals.append(dict(previous_line=a, line=b, previous_date=first['date'], date=second['date']))
    return dict(observed=len(records), score_bearing=sum(r['hg'] is not None and r['ag'] is not None for r in records),
                incomplete=len(incomplete), structurally_invalid=len(errors), complete_structurally_valid=sum(
                    r['source_line'] not in incomplete and r['source_line'] not in errors for r in records),
                fixture_errors={str(k): sorted(v) for k, v in sorted(errors.items())},
                flags={str(k): sorted(v) for k, v in sorted(flags.items())}, season_errors=sorted(set(season_errors)),
                expected=clubs*(clubs-1), clubs=len(names), team_names=sorted(names), missing_pairs=missing,
                duplicate_pairs=[dict(home=h, away=a, lines=ls) for (h, a), ls in sorted(pairs.items()) if len(ls) > 1],
                allocation=allocation, half_seasons=halves, normalized_collisions=collisions,
                halftime_present=halftime, outcomes=dict(outcomes), short_rest_events=rest,
                source_order_reversals=reversals, unusual_score_lines=high_scores)


def wide_rounds(records):
    by_round = defaultdict(list)
    for r in records: by_round[r['round']].append(r)
    result = []
    for number, rs in sorted(by_round.items()):
        dates = sorted(r['date'] for r in rs)
        if (date.fromisoformat(dates[-1])-date.fromisoformat(dates[0])).days >= 14:
            # Densest seven-day cluster is diagnostic only, never original schedule.
            windows = [(sum(0 <= (date.fromisoformat(r['date'])-date.fromisoformat(d)).days <= 6 for r in rs), d) for d in sorted(set(dates))]
            largest = max(n for n, d in windows)
            start = min(d for n, d in windows if n == largest)
            outliers = [r['source_line'] for r in rs if not 0 <= (date.fromisoformat(r['date'])-date.fromisoformat(start)).days <= 6]
            result.append(dict(round=number, earliest=dates[0], latest=dates[-1], lines=sorted(r['source_line'] for r in rs),
                               diagnostic_outlier_lines=outliers, diagnostic_cluster_start=start))
    return result


def context_binding(case, by_line, receipt):
    line = case['original']['source_line']
    if (case['source_sha256'] != receipt['sha256'] or
            case['source_fixture_id'] != source_id(receipt['path'], receipt['sha256'], line) or
            line not in by_line or any(by_line[line][k] != case['original'][k] for k in FIELDS)):
        raise ValueError('Known case source identity/facts changed')


def label_variants(records):
    groups = defaultdict(set)
    for r in records:
        for name in (r['home'], r['away']):
            key = ''.join(c for c in unicodedata.normalize('NFD', name).casefold() if not unicodedata.combining(c))
            key = re.sub(r'[^\w]+', ' ', key).strip()
            groups[key].add(name)
    return {k: sorted(v) for k, v in sorted(groups.items()) if len(v) > 1}


def chronology(record, context):
    line = record['source_line']
    value = dict(source_date=record['date'], source_date_heading=record['date_heading'], year_basis=record['year_basis'],
                 source_kickoff_time=record['kickoff'], scheduled_date=None, original_kickoff_date=None,
                 actual_completion_date=None, actual_playing_date=None, administrative_decision_date=None,
                 effective_result_date=None, policy_status='NOT_DECIDED_PHASE4', evidence_ids=[],
                 availability='UNVERIFIED_SOURCE_PLAYING_DATE_PROXY', on_field_result=None,
                 source_reported_result=record['FT'], source_administrative_result=None)
    if record['hg'] is None or record['ag'] is None:
        value.update(scheduled_date=record['date'], availability='MISSING_RESULT_NO_AVAILABILITY_DATE')
    elif record['source_marked_awarded']:
        value.update(scheduled_date=record['date'], source_administrative_result=record['FT'],
                     availability='UNRESOLVED_ADMINISTRATIVE_RESULT_AND_AVAILABILITY')
        if 'CF Reus Deportiu' in (record['home'], record['away']):
            value.update(administrative_decision_date=context['reus']['expulsion_decision_date'], evidence_ids=context['reus']['evidence'])
    for key in ('rayo_albacete', 'deportivo_fuenlabrada'):
        case = context[key]
        if case['source_file'] == record['source_file'] and case['original']['source_line'] == line:
            if key == 'rayo_albacete':
                value.update(original_kickoff_date=case['original_kickoff_date'], actual_completion_date=case['completion_date'],
                             on_field_result=record['FT'], availability='DOCUMENTED_COMPLETION_CONTEXT_POLICY_PENDING')
            else:
                value.update(scheduled_date=case['original_scheduled_date'], actual_playing_date=case['actual_playing_date'],
                             availability='DOCUMENTED_PLAYING_DATE_CONTEXT_SCORE_CERTIFICATION_PENDING')
            value['evidence_ids'] = case['evidence']
    return value


def build(directory=PRIVATE, root=ROOT):
    preservation = protect(directory, root)
    inventory_raw = (directory/'phase3_inventory.json').read_bytes(); inventory = json.loads(inventory_raw)
    manifest = json.loads((directory/acquisition.MANIFEST).read_text())
    entries = base.verify_metadata(directory)
    items = acquisition.plan()+[p for p in base.PLAN if int(p['season'][:4]) in acquisition.REUSED]
    plans = {p['path']: p for p in items}; receipts = manifest['acquired']+manifest['reused_phase2']
    if len(receipts) != 13 or len({r['path'] for r in receipts}) != 13 or set(plans) != {r['path'] for r in receipts}:
        raise ValueError('Wrong/duplicated acquired source scope')
    old = {s['source_file']: s for s in inventory['seasons']}
    if set(old) != set(plans) or len(inventory['seasons']) != 13:
        raise ValueError('Phase 3 season scope changed')
    seasons = []; all_records = []; all_spans = []; queue = {}; names = defaultdict(list)
    context = inventory['preserved_phase2_exception_context']; seen_ids = set()
    for receipt in sorted(receipts, key=lambda r: r['season']):
        file = receipt['path']; year = int(receipt['season'][:4]); raw = (directory/file).read_bytes()
        if base.cached(directory, plans[file], entries) != receipt:
            raise ValueError('Source receipt/manifest disagreement: '+file)
        records, notes, header = parse_source(raw, year)
        previous = old[file]['records']
        if len(records) != len(previous):
            raise ValueError('Raw/Phase 3 count disagreement: '+file)
        indexed = {r['source_line']: r for r in previous}
        if len(indexed) != len(previous) or set(indexed) != {r['source_line'] for r in records}:
            raise ValueError('Raw/Phase 3 source-line disagreement: '+file)
        for record in records:
            if any(record[k] != indexed[record['source_line']][k] for k in FIELDS):
                raise ValueError(f'Raw/Phase 3 field disagreement: {file}:{record["source_line"]}')
        result = validate(records, year); spans = wide_rounds(records)
        for name in result['team_names']: names[name].append(receipt['season'])
        source_errors = []
        if header.get('Teams') != result['clubs']: source_errors.append('TEAM_HEADER_CONTRADICTION')
        if header.get('Matches') != result['observed']: source_errors.append('MATCH_HEADER_CONTRADICTION')
        by_line = {r['source_line']: r for r in records}
        for span in spans:
            all_spans.append(dict(season=receipt['season'], source_file=file, **span))
            for line in span['lines']: result['flags'].setdefault(str(line), []).append('WIDE_ROUND_CONTEXT')
            for line in span['diagnostic_outlier_lines']: result['flags'].setdefault(str(line), []).append('DIAGNOSTIC_DATE_OUTLIER')
        for key in ('rayo_albacete', 'deportivo_fuenlabrada'):
            case = context[key]
            if case['source_file'] == file:
                line = case['original']['source_line']
                context_binding(case, by_line, receipt)
                result['flags'].setdefault(str(line), []).append('KNOWN_INTERRUPTION_OR_POSTPONEMENT')
        for case in context['reus']['records']:
            if case['source_file'] == file:
                context_binding(case, by_line, receipt)
        for record in records:
            record.update(source_file=file, source_sha256=receipt['sha256'], source_commit=receipt['commit'],
                          source_fixture_id=source_id(file, receipt['sha256'], record['source_line']), season=receipt['season'])
            if record['source_fixture_id'] in seen_ids: raise ValueError('Duplicate source audit identity')
            seen_ids.add(record['source_fixture_id'])
            record['chronology'] = chronology(record, context)
            categories = set(result['flags'].get(str(record['source_line']), []))
            if str(record['source_line']) in result['fixture_errors']: categories.add('STRUCTURAL_ERROR')
            if categories:
                queue[record['source_fixture_id']] = dict(fixture=record, categories=sorted(categories),
                                                         structural_errors=result['fixture_errors'].get(str(record['source_line']), []),
                                                         status='REVIEW_ONLY_NO_CORRECTION_OR_EXCLUSION')
        seasons.append(dict(season=receipt['season'], source_file=file, source_sha256=receipt['sha256'],
                            git_blob_sha1=receipt['git_blob_sha1'], bytes=len(raw), CRLF_lines=raw.count(b'\r\n'),
                            header=header, source_errors=source_errors, validation=result, notes=notes, wide_rounds=spans,
                            date_year_bases=dict(Counter(r['year_basis'] for r in records)),
                            first_date=min(r['date'] for r in records), last_date=max(r['date'] for r in records)))
        all_records.extend(records)
    frozen_spans = {(r['season'], r['details']['round']): r for r in inventory['scheduling']['modern_cases']}
    if len(frozen_spans) != len(inventory['scheduling']['modern_cases']) or set(frozen_spans) != {(r['season'], r['round']) for r in all_spans}:
        raise ValueError('Scheduling candidate missing/duplicated')
    for span in all_spans:
        before = frozen_spans[span['season'], span['round']]['details']
        if span['earliest'] != before['earliest'] or span['latest'] != before['latest'] or span['lines'] != sorted(r['source_line'] for r in before['records']):
            raise ValueError('Frozen scheduling dates/fixtures changed')
    variants = label_variants(all_records); variant_names = {n for group in variants.values() for n in group}
    for record in all_records:
        if record['home'] in variant_names or record['away'] in variant_names:
            row = queue.setdefault(record['source_fixture_id'], dict(fixture=record, categories=[], structural_errors=[],
                                                                     status='REVIEW_ONLY_NO_CORRECTION_OR_EXCLUSION'))
            row['categories'] = sorted(set(row['categories']) | {'POTENTIAL_TEAM_LABEL_VARIANT'})
    queue_rows = [queue[k] for k in sorted(queue)]
    category_counts = Counter(c for r in queue_rows for c in r['categories'])
    overlaps = Counter(' + '.join(r['categories']) for r in queue_rows)
    totals = {k: sum(s['validation'][k] for s in seasons) for k in ('observed', 'score_bearing', 'incomplete', 'structurally_invalid', 'complete_structurally_valid')}
    totals.update(flagged_unique=len(queue_rows), unflagged=len(all_records)-len(queue_rows),
                  season_error_events=sum(len(s['validation']['season_errors'])+len(s['source_errors']) for s in seasons),
                  wide_rounds=len(all_spans), wide_round_fixture_context=sum(len(s['lines']) for s in all_spans))
    if totals['observed'] != totals['complete_structurally_valid']+totals['incomplete']+totals['structurally_invalid']:
        # Invalid/incomplete overlap is reported explicitly; never silently force a partition.
        totals['invalid_incomplete_overlap'] = sum(r['fixture']['hg'] is None and bool(r['structural_errors']) for r in queue_rows)
    turnover = []
    for first, second in zip(seasons, seasons[1:]):
        a, b = set(first['validation']['team_names']), set(second['validation']['team_names'])
        turnover.append(dict(from_season=first['season'], to_season=second['season'], entered_labels=sorted(b-a), left_labels=sorted(a-b),
                             warning='Promotion/relegation or spelling/identity changes require evidence; no identity inference made.'))
    queue_doc = dict(scope='Phase 4 deduplicated fixture-level review queue, not processing decisions',
                     counts=totals, category_counts=dict(sorted(category_counts.items())), overlap_combinations=dict(sorted(overlaps.items())),
                     records=queue_rows, evidence_context=context,
                     rules=dict(wide_round_days=14, diagnostic_cluster_days=7, short_rest_days=1,
                                unusual_single_team_goals=8, unusual_total_goals=10),
                     warning='Categories overlap. Ordinary source dates are uncertified proxies; flags do not imply incorrectness or exclusion.')
    report = dict(scope='Segunda Phase 4 only: independent structural validation, no historical decisions',
                  seasons=seasons, totals=totals, records=all_records, scheduling=all_spans,
                  categories=dict(sorted(category_counts.items())),
                  chronology_classes=dict(Counter(r['chronology']['availability'] for r in all_records)),
                  effective_dates_policy='No approved effective result dates assigned; source proxies, context dates and administrative uncertainty remain distinct.',
                  name_catalog=dict(exact_labels=dict(sorted(names.items())), reserves=sorted(RESERVES & names.keys()), season_label_turnover=turnover,
                                    potential_accent_case_punctuation_variants=variants,
                                    warning='No aliases, parent/reserve merges or historical continuity mappings applied.'),
                  preserved_phase2_flags=inventory['scheduling']['phase2_carried'], gaps=inventory['gaps'],
                  incomplete_modern=[dict(source_file=r['source_file'], source_line=r['source_line'], source_fixture_id=r['source_fixture_id'],
                                          home=r['home'], away=r['away'], source_date=r['date']) for r in all_records if r['hg'] is None],
                  preservation=preservation, phase3_inventory_sha256=base.sha(inventory_raw),
                  review_queue_sha256=base.sha(base.encode(queue_doc)), rights=inventory['rights'], model_training_clearance='UNRESOLVED')
    protect(directory, root)
    return {REPORT: base.encode(report), QUEUE: base.encode(queue_doc)}


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--init', action='store_true'); parser.add_argument('--check', action='store_true'); args = parser.parse_args()
    if args.init: initialize()
    if not args.check and any((PRIVATE/n).exists() for n in (REPORT, QUEUE)):
        raise FileExistsError('Outputs exist; use --check')
    values = build()
    for name, raw in values.items():
        if args.check:
            if (PRIVATE/name).read_bytes() != raw: raise ValueError('Saved output differs: '+name)
        else: base.save(PRIVATE/name, raw)
    print(json.loads(values[REPORT])['totals'])


if __name__ == '__main__': main()
