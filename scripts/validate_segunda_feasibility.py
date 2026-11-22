"""Offline Phase 2 assessment; preserve source facts, stages and date precision.

This is not a standardizer or historical/administrative certification tool.
"""
import argparse
from collections import Counter, defaultdict
from datetime import date
import html
import json
import re
import unicodedata

from scripts.collect_segunda_feasibility import PRIVATE, ROOT, PLAN, RIGHTS, cached, encode, protect, save, sha, verify_metadata

OUTPUT = 'feasibility_assessment.json'
MONTHS = {s: i+1 for i, s in enumerate('Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split())}
DAYS = 'Mon Tue Wed Thu Fri Sat Sun'.split()
STATUS = re.compile(r'award|abandon|annul|postpon|resum|suspend|cancel|replay|aplaz|reanud|expuls', re.I)

# Human-inspected documentary context, not blanket historical certification or
# processing decisions. No document is used to rewrite an acquired fixture.
EVIDENCE = [
    dict(id='S2-E01', url='https://www.laliga.com/noticias/nota-informativa-164',
         title='Nota Informativa', publication_date='2019-01-28', access='DIRECTLY_INSPECTED',
         establishes='Reus expelled from professional competition for three years; does not certify each later award score or applicable date.'),
    dict(id='S2-E02', url='https://rfef.es/sites/default/files/pdf/resolucion_apelacion_rayo-albacete.pdf',
         title='Comité de Apelación, expediente 276–2019/20', access='DIRECTLY_INSPECTED_PDF',
         establishes='Rayo–Albacete began on 2019-12-15 and was suspended before the second half.'),
    dict(id='S2-E03', url='https://rfef.es/es/noticias/comite-competicion-fija-rayo-albacete-jornada-20-dia-10-junio',
         title='El Comité de Competición fija el Rayo-Albacete de la jornada 20 para el día 10 de junio',
         publication_date='2020-06-03', access='DIRECTLY_INSPECTED',
         establishes='Second half scheduled to resume on 2020-06-10; not itself proof of completion or FT score.'),
    dict(id='S2-E04', url='https://www.laliga.com/noticias/nota-informativa-rayo-albacete',
         title='Nota informativa: suspensión del Rayo Vallecano–Albacete', publication_date='2019-12-15',
         access='DIRECTLY_INSPECTED',
         establishes='Original suspension article carries current match widget: 2020-06-10, Rayo 1–0 Albacete; dynamic widget distinguished from original article date.'),
    dict(id='S2-E05', url='https://memorias.laliga.com/2019/es/actividades-deportivas',
         title='Memoria Anual 2019–2020: Actividades Deportivas', access='DIRECTLY_INSPECTED',
         establishes='Rayo–Albacete resumed after halftime suspension on 2020-06-10; Deportivo–Fuenlabrada ultimately played on Friday 2020-08-07 with Deportivo winning. Passage does not supply exact FT score.'),
    dict(id='S2-E06', url='https://www.laliga.com/noticias/nota-informativa-deportivo-fuenlabrada-play-off-2020',
         title='Horario del RC Deportivo–CF Fuenlabrada y Fechas Play-off de Ascenso',
         access='SEARCH_INDEX_ONLY',
         establishes='Indexed scheduling statement refers to original 2020-07-20 postponement and intermediate 2020-08-05 plan; not the eventual playing date.'),
]


def text_date(match, year):
    weekday, month, number, explicit = match.groups()
    candidates = []
    for y in [int(explicit)] if explicit else [year, year+1]:
        try:
            d = date(y, MONTHS[month], int(number))
        except (ValueError, KeyError):
            continue
        end = date(year+1, 8, 31) if year == 2019 else date(year+1, 6, 30)
        if date(year, 7, 1) <= d <= end and DAYS[d.weekday()] == weekday:
            candidates.append(d.isoformat())
    if len(candidates) != 1:
        raise ValueError('Ambiguous/invalid date, season boundary or weekday: '+match[0])
    return candidates[0]


def fixture(body):
    """Do not manufacture scores for a scheduled v fixture."""
    annotation = ''
    m = re.search(r'\s*(\[[^\]]+\])\s*$', body)
    if m:
        annotation = m[1]; body = body[:m.start()].rstrip()
    ht = None
    if re.search(r'\s+v\s+', body):
        home, tail = re.split(r'\s+v\s+', body, maxsplit=1)
        m = re.fullmatch(r'(.+?)\s{2,}(\d+)-(\d+)(?:\s+\((\d+-\d+)\))?', tail)
        if m:
            away, h, a, ht = m.groups()
        else:
            if re.search(r'\d\s*-|\?\s*-|-\s*\d', tail):
                raise ValueError('Malformed/partial score')
            away = tail; h = a = None
    else:
        m = re.fullmatch(r'(.+?)\s+(\d+)-(\d+)(?:\s+\((\d+-\d+)\))?\s+(.+)', body)
        if not m:
            raise ValueError('Unrecognized fixture: '+body)
        home, h, a, ht, away = m.groups()
    return dict(home=home, away=away, hg=h, ag=a, FT=f'{h}-{a}' if h is not None else None,
                HT=ht, annotation=annotation, source_marked_awarded='award' in annotation.lower())


def parse_text(raw, year):
    text = raw.decode('utf-8-sig'); rows = []; notes = []; current = None; stage = None; round_id = None
    title = False; depth = 0
    for number, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if not s:
            continue
        if depth or s.startswith('('):
            if not rows:
                raise ValueError('Annotation without fixture')
            depth += s.count('(')-s.count(')')
            if depth < 0:
                raise ValueError('Unbalanced annotation')
            notes.append(dict(line=number, kind='scorer_annotation', text=s)); continue
        if s.startswith('#'):
            notes.append(dict(line=number, kind='comment', text=s)); continue
        if s.startswith('='):
            if title or not re.search(r'Segunda Divisi[oó]n', s) or re.search(r'Divisi[oó]n\s+B\b', s):
                raise ValueError('Wrong/duplicate competition title')
            season = re.search(r'(\d{4})/(\d{2,4})', s)
            if not season or int(season[1]) != year or int(season[2]) % 100 != (year+1) % 100:
                raise ValueError('Wrong/missing source season')
            title = True; notes.append(dict(line=number, kind='competition_header', text=s)); continue
        if s.startswith('▪'):
            label = s[1:].strip()
            m = re.fullmatch(r'(?:Matchday (\d+)|(\d+)\. Round|Regular Season - (\d+))', label)
            if m:
                stage = 'REGULAR_SEASON'; round_id = int(next(x for x in m.groups() if x))
                if not 1 <= round_id <= 42:
                    raise ValueError('Unexpected regular round number')
            elif re.search(r'play.?off|promotion|semi.?final|final', label, re.I):
                stage = 'PLAYOFF_OR_OTHER'; round_id = label
            else:
                raise ValueError('Unknown stage: '+label)
            current = None
            notes.append(dict(line=number, kind='stage_header', stage=stage, label=label)); continue
        dm = re.fullmatch(r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun) ([A-Z][a-z]{2}) (\d{1,2})(?: (\d{4}))?', s)
        if dm:
            current = text_date(dm, year); continue
        if s.startswith('[') and s.endswith(']'):
            notes.append(dict(line=number, kind='status_note', text=s)); continue
        kickoff = re.match(r'^(\d{1,2}:\d{2})\s+', s)
        if kickoff:
            h, minute = map(int, kickoff[1].split(':'))
            if h > 23 or minute > 59:
                raise ValueError('Invalid kickoff time')
            s = s[kickoff.end():]
        if not title or stage is None or current is None:
            raise ValueError(f'Fixture without competition/stage/date at line {number}')
        rows.append(dict(source_line=number, raw_record=line, date=current, date_basis='SOURCE_DATE_HEADING',
                         round=round_id, stage=stage, kickoff=kickoff[1] if kickoff else None, **fixture(s)))
    if depth or not title or not rows:
        raise ValueError('Incomplete source/annotation')
    return rows, notes


def rsssf_date(value, year=1996):
    m = re.fullmatch(r'([A-Z][a-z]{2}) (\d{1,2})', value)
    if not m or m[1] not in MONTHS:
        raise ValueError('Unrecognized RSSSF date: '+value)
    month = MONTHS[m[1]]
    return date(year+(month < 7), month, int(m[2])).isoformat()


def parse_rsssf(raw):
    """Select only the named second-tier section, retaining physical HTML lines.

    Round headings supply a date proxy, never individually verified match dates.
    Table aliases and playoff abbreviations remain unchanged.
    """
    text = raw.decode('latin-1'); lines = text.splitlines()
    starts = [i for i, s in enumerate(lines) if s.strip() == 'Spain Segunda Division A 1996/97']
    ends = [i for i, s in enumerate(lines) if s.strip() == 'Spain Segunda Division B (Third Level) 1996/97']
    if len(starts) != 1 or len(ends) != 1 or starts[0] >= ends[0]:
        raise ValueError('RSSSF competition boundaries changed')
    rows = []; notes = []; current = None; round_id = None; state = 'PREAMBLE'; basis = None
    for i in range(starts[0]+1, ends[0]):
        rawline = lines[i]; s = html.unescape(re.sub('<[^>]+>', '', rawline)).strip()
        if not s:
            continue
        rm = re.fullmatch(r'Round (\d+) \[([^\]]+)\]', s)
        if rm:
            round_id = int(rm[1]); current = rsssf_date(rm[2]); state = 'REGULAR_SEASON'; basis = 'ROUND_HEADING_PROXY'
            if not 1 <= round_id <= 38:
                raise ValueError('Unexpected RSSSF round')
            notes.append(dict(line=i+1, kind='round_header', text=s)); continue
        if s == 'Table:':
            state = 'TABLE'; continue
        if s == 'Promotion Playoff':
            state = 'PROMOTION_PLAYOFF'; current = None; continue
        if s == 'Top Goalscorers':
            state = 'SCORERS'; continue
        leg = re.fullmatch(r'(First|Second) leg \[([^\]]+)\]', s)
        if leg:
            if state != 'PROMOTION_PLAYOFF':
                raise ValueError('Leg heading in wrong stage')
            current = rsssf_date(leg[2]); round_id = leg[1]+' leg'; basis = 'LEG_HEADING_PROXY'; continue
        if state not in ('REGULAR_SEASON', 'PROMOTION_PLAYOFF'):
            continue
        # Explicit narrative after the two playoff results is retained, not parsed as a fixture.
        if state == 'PROMOTION_PLAYOFF' and 'promoted' in s.lower():
            notes.append(dict(line=i+1, kind='promotion_note', text=s)); continue
        explicit = re.search(r'\s+\[([A-Z][a-z]{2} \d{1,2})\]$', s)
        day = rsssf_date(explicit[1]) if explicit else current
        if explicit:
            s = s[:explicit.start()]
        if day is None:
            raise ValueError('RSSSF fixture without date context')
        rows.append(dict(source_line=i+1, raw_record=rawline, date=day,
                         date_basis='FIXTURE_EXPLICIT' if explicit else basis, round=round_id,
                         stage=state, kickoff=None, **fixture(s)))
    if not rows:
        raise ValueError('No RSSSF fixture records')
    notes.append(dict(kind='scope', first_html_line=starts[0]+1, last_html_line=ends[0],
                      excluded='Primera, cup and third-tier sections retained in original but not assessed'))
    return rows, notes


def assess(rows, year, clubs):
    regular = [r for r in rows if r['stage'] == 'REGULAR_SEASON']; teams = sorted({r[k] for r in regular for k in ('home', 'away')})
    pairs = Counter((r['home'], r['away']) for r in regular); scores = []; unscored = []; invalid = []; date_errors = []; team_errors = []
    conflicts = []; allocation = {}; norm = defaultdict(list); events = defaultdict(list); rounds = defaultdict(list)
    for name in teams:
        norm[unicodedata.normalize('NFC', name).casefold()].append(name)
        allocation[name] = dict(home=sum(r['home'] == name for r in regular), away=sum(r['away'] == name for r in regular))
    for r in rows:
        h, a = r['hg'], r['ag']
        if h is None and a is None:
            unscored.append(r['source_line'])
        else:
            try:
                # These adapters emit original digit strings, never floating-point
                # values. No dataframe/importer or standardized rows are created
                # in feasibility; keep this assessment standard-library-only.
                if any(not isinstance(x, str) or not re.fullmatch(r'[0-9]+', x) for x in (h, a)):
                    raise ValueError('Source goals must be nonnegative digit strings')
                h, a = int(h), int(a)
                if max(h, a) > 2**63-1:
                    raise ValueError('Source goals exceed shared integer range')
                if min(h, a) < 0 or r['FT'] != f'{h}-{a}':
                    raise ValueError('Invalid FT')
                if r['HT']:
                    hh, aa = map(int, r['HT'].split('-'))
                    if hh > h or aa > a:
                        raise ValueError('HT exceeds FT')
                scores.append((r, '1' if h > a else '2' if h < a else 'X'))
            except (ValueError, TypeError):
                invalid.append(r['source_line'])
        try:
            d = date.fromisoformat(r['date']); end = date(year+1, 8, 31) if year == 2019 else date(year+1, 6, 30)
            if d.isoformat() != r['date'] or not date(year, 7, 1) <= d <= end:
                raise ValueError()
        except (ValueError, TypeError):
            date_errors.append(r['source_line'])
        if r['home'] == r['away'] or any(not t or t != t.strip() or '\ufffd' in t or any(unicodedata.category(c) == 'Cc' for c in t) for t in (r['home'], r['away'])):
            team_errors.append(r['source_line'])
        if r['stage'] == 'REGULAR_SEASON':
            rounds[r['round']].append(r)
            for t in (r['home'], r['away']):
                events[r['date'], t].append(r['source_line'])
    for pair, n in pairs.items():
        if n > 1:
            values = {(r['date'], r['hg'], r['ag']) for r in regular if (r['home'], r['away']) == pair}
            conflicts.append(dict(home=pair[0], away=pair[1], count=n, conflicting=len(values) > 1))
    missing = [(h, a) for h in teams for a in teams if h != a and (h, a) not in pairs]
    allocation_errors = {t: v for t, v in allocation.items() if v != dict(home=clubs-1, away=clubs-1)}
    collisions = [dict(date=d, team=t, lines=ls) for (d, t), ls in sorted(events.items()) if len(ls) > 1]
    round_errors = []; spans = []
    for number, rs in sorted(rounds.items()):
        appearances = Counter(t for r in rs for t in (r['home'], r['away']))
        if len(rs) != clubs//2 or set(appearances) != set(teams) or any(n != 1 for n in appearances.values()):
            round_errors.append(number)
        ds = sorted(r['date'] for r in rs if r['source_line'] not in date_errors)
        if ds and (date.fromisoformat(ds[-1])-date.fromisoformat(ds[0])).days >= 14:
            spans.append(dict(round=number, earliest=ds[0], latest=ds[-1], records=rs))
    aliases = {k: v for k, v in norm.items() if len(v) > 1}
    issues = [name for name, condition in (
        ('fixture_count', len(regular) != clubs*(clubs-1)), ('team_count', len(teams) != clubs),
        ('duplicate_pairings', bool(conflicts)), ('missing_pairings', bool(missing)), ('allocation', bool(allocation_errors)),
        ('round_coverage', set(rounds) != set(range(1, 2*(clubs-1)+1)) or bool(round_errors)),
        ('missing_scores', bool(unscored)), ('invalid_scores', bool(invalid)), ('dates', bool(date_errors)),
        ('teams', bool(team_errors)), ('normalized_name_collision', bool(aliases)), ('same_team_date_collision', bool(collisions))) if condition]
    return dict(season=f'{year}/{year+1}', observed=len(rows), regular=len(regular), other=len(rows)-len(regular),
                stages=dict(Counter(r['stage'] for r in rows)), scored=len(scores), unscored=len(unscored), invalid_scores=len(invalid),
                regular_scored=sum(r['stage'] == 'REGULAR_SEASON' for r, _ in scores), expected_regular=clubs*(clubs-1),
                clubs=len(teams), club_names=teams, non_ascii_names=[t for t in teams if not t.isascii()],
                missing_pairs=missing, duplicate_pairs=conflicts, allocation_errors=allocation_errors,
                round_errors=round_errors, same_team_date_collisions=collisions, normalized_name_collisions=aliases,
                date_error_lines=date_errors, invalid_team_lines=team_errors, invalid_score_lines=invalid,
                unscored_records=[r for r in rows if r['source_line'] in set(unscored)],
                date_bases=dict(Counter(r['date_basis'] for r in rows)), first_date=min(r['date'] for r in rows), last_date=max(r['date'] for r in rows),
                source_marked_awarded=[r for r in rows if r['source_marked_awarded']],
                annotations=[r for r in rows if r['annotation']], wide_rounds=spans,
                outcomes=dict(Counter(o for _, o in scores)), issues=issues, records=rows)


def exceptional_context(seasons):
    by_season = {r['season']: r for r in seasons}
    def bound(report, row):
        return dict(source_file=report['source_file'], source_sha256=report['source_sha256'],
                    original=row, source_fixture_id='segunda:'+sha(encode(dict(
                        file=report['source_file'], sha256=report['source_sha256'], line=row['source_line']))))
    reus_season = by_season['2018/2019']
    reus = [bound(reus_season, r) for r in reus_season['records'] if 'CF Reus Deportiu' in (r['home'], r['away'])]
    current = by_season['2019/2020']
    def one(home, away):
        selected = [r for r in current['records'] if (r['home'], r['away']) == (home, away)]
        if len(selected) != 1:
            raise ValueError('Exceptional fixture missing/ambiguous')
        return bound(current, selected[0])
    return dict(evidence=EVIDENCE, independence='Organizer/federation documentary context distinct from compiler files; no population or exhaustive legal certification.',
                reus=dict(records=reus, source_marked_awarded=sum(r['original']['source_marked_awarded'] for r in reus),
                          expulsion_decision_date='2019-01-28', evidence=['S2-E01'],
                          final_award_results_and_availability='UNRESOLVED: source award scores/dates preserved; obtain operative decisions and appeal outcomes before policy.'),
                rayo_albacete=dict(**one('Rayo Vallecano', 'Albacete'), original_kickoff_date='2019-12-15',
                                   completion_date='2020-06-10', evidence=['S2-E02', 'S2-E03', 'S2-E04', 'S2-E05'],
                                   final_status='PLAYED_FACTS_SUPPORTED; not exhaustive disciplinary clearance'),
                deportivo_fuenlabrada=dict(**one('Deportivo La Coruña', 'CF Fuenlabrada'),
                                          original_scheduled_date='2020-07-20', actual_playing_date='2020-08-07',
                                          kickoff_on_original_scheduled_date=None, evidence=['S2-E05', 'S2-E06'],
                                          final_status='Official retrospective supports actual date and winner; exact 2–1 remains source observation in this limited evidence review.'),
                action='NO_CORRECTIONS_OR_EXCLUSIONS; all source observations retained, processing policy deferred')


def build(directory=PRIVATE, root=ROOT):
    protection = protect(directory, root)
    entries = verify_metadata(directory)
    manifest = json.loads((directory/'acquisition.json').read_text())
    if len(manifest['files']) != 5:
        raise ValueError('Wrong acquired scope')
    seasons = []
    for item, recorded in zip(PLAN, manifest['files'], strict=True):
        receipt = cached(directory, item, entries)
        if receipt != recorded:
            raise ValueError('Aggregate/source receipt mismatch')
        raw = (directory/item['path']).read_bytes(); year = int(item['season'][:4])
        rows, notes = parse_rsssf(raw) if item['source'] == 'RSSSF' else parse_text(raw, year)
        report = assess(rows, year, 20 if year == 1996 else 22)
        report.update(source=item['source'], source_file=item['path'], source_sha256=sha(raw),
                      encoding='ISO-8859-1' if item['source'] == 'RSSSF' else 'UTF-8',
                      CRLF_lines=raw.count(b'\r\n'), notes=notes,
                      status_notes=[n for n in notes if STATUS.search(n.get('text', ''))])
        seasons.append(report)
    protect(directory, root)
    return dict(scope='Phase 2 only: feasibility; no corrections, exclusions, standardized data or historical certification',
                seasons=seasons, exceptions=exceptional_context(seasons), protected=protection, acquisition_sha256=sha((directory/'acquisition.json').read_bytes()),
                rights=RIGHTS, historical_confidence='Source observations only; no population certification',
                model_training_clearance='UNRESOLVED', source_gap='1990/91–2011/12 not covered by a complete approved source',
                warnings=['Source-marked awards are scored records, not certified played games.',
                          'Round-date proxies and scheduled dates are not independently established result-availability dates.',
                          'No score/date/name is corrected or excluded; no team-name mappings applied.'])


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--check', action='store_true'); args = parser.parse_args()
    raw = encode(build()); target = PRIVATE/OUTPUT
    if args.check:
        if target.read_bytes() != raw:
            raise ValueError('Saved assessment differs')
    else:
        save(target, raw)
    for r in json.loads(raw)['seasons']:
        print(r['season'], {k: r[k] for k in ('observed', 'regular', 'other', 'scored', 'unscored', 'clubs', 'issues')})


if __name__ == '__main__':
    main()
