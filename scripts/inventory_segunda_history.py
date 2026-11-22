"""Phase 3 source inventory using the frozen Phase 2 grammar; not Phase 4.

Reports observations and review candidates without corrections or eligibility.
"""
import argparse
from collections import Counter, defaultdict
import json
import re
import unicodedata

from scripts import collect_segunda_feasibility as base
from scripts import collect_segunda_history as acquisition
from scripts import validate_segunda_feasibility as feasibility

PRIVATE, ROOT = base.PRIVATE, base.ROOT
OUTPUT = 'phase3_inventory.json'


def label_catalog(seasons):
    names = defaultdict(list); equivalent = defaultdict(list)
    for season in seasons:
        for name in season.get('club_names', []):
            names[name].append(season['season'])
    for name in sorted(names):
        key = ''.join(c for c in unicodedata.normalize('NFD', name).casefold() if not unicodedata.combining(c))
        key = re.sub(r'[^\w]+', ' ', key).strip()
        equivalent[key].append(name)
    reserves = [n for n in sorted(names) if re.search(r'\sB$|Castilla|Sevilla Atl[eé]tico', n)]
    return dict(exact_labels=dict(sorted(names.items())), distinct_exact_labels=len(names),
                accent_case_punctuation_candidates={k: v for k, v in sorted(equivalent.items()) if len(v) > 1},
                reserve_label_candidates=reserves,
                warning='Diagnostic strings only; reserve detection is a review aid, not a club-identity registry. No aliases or continuity mappings applied.')


def check_carried_flags(phase2, modern):
    by_season = {s['season']: s for s in modern}
    carried = []
    for season in phase2['seasons']:
        for flag in season['wide_rounds']:
            current = by_season.get(season['season'])
            if current is not None:
                if flag not in current.get('wide_rounds', []):
                    raise ValueError('Phase 2 modern scheduling candidate changed or lost')
            carried.append(dict(season=season['season'], source_file=season['source_file'],
                                within_modern_scope=current is not None, details=flag))
    return carried


def build(directory=PRIVATE, root=ROOT):
    protection = acquisition.protect(directory, root)
    entries = base.verify_metadata(directory)
    manifest = json.loads((directory/acquisition.MANIFEST).read_text())
    if manifest['commit'] != base.PIN or manifest['approved_new_files'] != 10 or manifest['modern_sources'] != 13:
        raise ValueError('Changed acquisition scope/revision')
    receipts = manifest['acquired']+manifest['reused_phase2']
    if len(receipts) != 13 or len({r['path'] for r in receipts}) != 13:
        raise ValueError('Missing/duplicate source receipt')
    by_path = {r['path']: r for r in receipts}
    plans = {p['path']: p for p in acquisition.plan()}
    plans.update({p['path']: p for p in base.PLAN if int(p['season'][:4]) in acquisition.REUSED})
    if set(plans) != set(by_path):
        raise ValueError('Acquired files differ from approved 13-season scope')
    phase2_raw = (directory/feasibility.OUTPUT).read_bytes(); phase2 = json.loads(phase2_raw)
    if base.encode(feasibility.build(directory, root)) != phase2_raw:
        raise ValueError('Phase 2 assessment no longer reproduces')
    seasons = []; missing = []; parse_errors = []; wide = []
    for year in range(2012, 2025):
        file = f'{base.REPO}/{year}-{(year+1)%100:02}/2-liga2.txt'; item = plans[file]
        receipt = base.cached(directory, item, entries)
        if receipt is None:
            missing.append(file)
            seasons.append(dict(season=f'{year}/{year+1}', source_file=file, status='MISSING', expected_regular=462))
            continue
        if receipt != by_path[file]:
            raise ValueError('Aggregate/individual source receipt differs: '+file)
        raw = (directory/file).read_bytes()
        try:
            rows, notes = feasibility.parse_text(raw, year)
            report = feasibility.assess(rows, year, 22)
            header_values = {}
            for n in notes:
                h = re.fullmatch(r'#\s*(Teams|Matches)\s+(\d+)', n.get('text', ''))
                if h:
                    if h[1] in header_values:
                        raise ValueError('Duplicate source count header')
                    header_values[h[1]] = int(h[2])
            contradictions = {k: dict(source=v, observed=report['clubs'] if k == 'Teams' else report['observed'])
                              for k, v in header_values.items() if v != (report['clubs'] if k == 'Teams' else report['observed'])}
            report.update(source_file=file, source_sha256=receipt['sha256'], source_commit=base.PIN,
                          git_blob_sha1=receipt['git_blob_sha1'], bytes=receipt['bytes'], encoding='UTF-8 strict',
                          CRLF_lines=raw.count(b'\r\n'), notes=notes, source_count_headers=header_values,
                          header_contradictions=contradictions,
                          status_notes=[n for n in notes if feasibility.STATUS.search(n.get('text', ''))],
                          status='INVENTORIED_REVIEW' if report['issues'] or contradictions else 'INVENTORIED')
            seasons.append(report)
            for flag in report['wide_rounds']:
                wide.append(dict(season=report['season'], source_file=file, source_sha256=receipt['sha256'], details=flag))
        except (ValueError, TypeError, KeyError) as exc:
            parse_errors.append(dict(source_file=file, error=str(exc)))
            seasons.append(dict(season=f'{year}/{year+1}', source_file=file, source_sha256=receipt['sha256'],
                                expected_regular=462, status='PARSE_REVIEW', error=str(exc)))
    good = [s for s in seasons if 'observed' in s]
    carried = check_carried_flags(phase2, seasons)
    old_refs = {(r['season'], r['details']['round']) for r in carried if r['within_modern_scope']}
    for before in phase2['seasons']:
        if before['season'] in ('2012/2013', '2018/2019', '2019/2020'):
            after = next(s for s in seasons if s['season'] == before['season'])
            if before['records'] != after.get('records') or before['annotations'] != after.get('annotations'):
                raise ValueError('Reused Phase 2 source observations/annotations changed')
    if len(good) == 13:
        if feasibility.exceptional_context(good) != phase2['exceptions']:
            raise ValueError('Known exceptional facts or uncertainty changed')
    newer = next(s for s in phase2['seasons'] if s['season'] == '2025/2026')
    older_sample = next(s for s in phase2['seasons'] if s['season'] == '1996/1997')
    acquisitions = [directory/acquisition.BASELINE, directory/acquisition.MANIFEST,
                    directory/'acquisition.json', directory/feasibility.OUTPUT,
                    directory/'metadata_receipts.json', directory/'metadata/git_tree.json']
    for r in receipts:
        f = directory/r['path']; acquisitions.extend([f, f.with_name(f.name+'.provenance.json')])
    result = dict(scope='Phase 3 only: source acquisition/inventory, not independent structural validation or historical certification',
                  seasons=seasons, scope_counts=dict(requested=13, accounted=len(seasons), parsed=len(good),
                  missing_files=missing, parse_errors=parse_errors),
                  totals={k: sum(s[k] for s in good) for k in ('observed', 'regular', 'other', 'scored', 'unscored', 'invalid_scores')},
                  expected_regular=13*462,
                  administrative_awards=[dict(season=s['season'], source_file=s['source_file'], original=r)
                                         for s in good for r in s['source_marked_awarded']],
                  scheduling=dict(modern_cases=wide, phase2_carried=carried,
                                  new_modern_cases=[r for r in wide if (r['season'], r['details']['round']) not in old_refs],
                                  warning='Wide span is a review candidate, not an error or exclusion.'),
                  names=label_catalog(good), preserved_phase2_exception_context=phase2['exceptions'],
                  gaps=dict(older=dict(start='1990/1991', end='2011/2012', seasons=22,
                                       status='NO_APPROVED_COMPLETE_SOURCE', rsssf_sample=dict(source_file=older_sample['source_file'],
                                       regular=older_sample['regular'], date_bases=older_sample['date_bases'],
                                       warning='A single round-date-proxy sample does not close the coverage gap.')),
                            newer=dict(season='2025/2026', source_file=newer['source_file'], observed=newer['observed'],
                                       scored=newer['scored'], unscored=newer['unscored'],
                                       status='FROZEN_INCOMPLETE_SOURCE_OUTSIDE_MODERN_SCOPE')),
                  preservation=protection, rights=base.RIGHTS, model_training_clearance='UNRESOLVED',
                  input_sha256={str(p.relative_to(directory)): base.sha(p.read_bytes()) for p in sorted(acquisitions) if p.exists()},
                  limitations='No source patch, name mapping, exclusion/acceptance decision, standardized output or application integration.')
    acquisition.protect(directory, root)
    return result


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--check', action='store_true'); args = parser.parse_args()
    raw = base.encode(build()); target = PRIVATE/OUTPUT
    if args.check:
        if target.read_bytes() != raw:
            raise ValueError('Saved inventory differs')
    else:
        base.save(target, raw)
    data = json.loads(raw)
    for s in data['seasons']:
        print(s['season'], {k: s.get(k) for k in ('observed', 'scored', 'unscored', 'regular', 'other', 'clubs', 'status')})
    print('TOTALS', data['totals']); print('WIDE_ROUNDS', len(data['scheduling']['modern_cases']))


if __name__ == '__main__':
    main()
