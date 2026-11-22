"""Offline Phase 5 evidence consistency checks, never historical certification.

Reads immutable sources and manually reviewed evidence; writes only the private
assessment when --write is explicit. Does not download, repair or export matches.
"""
import argparse
from collections import Counter
from datetime import date
import json
from pathlib import Path

from scripts.collect_la_liga_feasibility import ROOT, PRIVATE, sha
from scripts.validate_la_liga_feasibility import encode
from scripts.validate_la_liga_structure import HIST, parse_csv, csv_season, parse_text

LEDGER = 'phase5_historical_review.json'
OUTPUT = 'phase5_evidence_check.json'
HOMES = {'Real Madrid', 'Real Madrid C.F.', 'Real Madrid CF'}
AWAYS = {'FC Barcelona', 'Barcelona'}
FACTS = ('date', 'home', 'away', 'hg', 'ag')


def read_json(path):
    def unique(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('Duplicate JSON key: ' + key)
            result[key] = value
        return result
    return json.loads(path.read_text(), object_pairs_hook=unique)


def protect(baseline, root=ROOT):
    for name, digest in baseline.items():
        path = root / name
        if not path.resolve().is_relative_to(root.resolve()):
            raise ValueError('Protected path escapes root')
        if sha(path.read_bytes()) != digest:
            raise ValueError('Protected artifact changed: ' + name)
    return len(baseline)


def records(directory):
    historical = parse_csv((directory / HIST).read_bytes())
    result = {}
    for year in range(1990, 2026):
        season = f'{year}/{year+1}'
        file = HIST if year < 2012 else f'openfootball/espana/{year}-{(year+1)%100:02}/1-liga.txt'
        rows = csv_season(historical, year) if year < 2012 else parse_text((directory / file).read_bytes(), year)[0]
        for row in rows:
            key = (file, row['source_line'])
            if key in result:
                raise ValueError('Duplicate physical binding')
            result[key] = (season, row)
    return result


def selection(rows):
    chosen = []
    for year in range(1990, 2026):
        season = f'{year}/{year+1}'
        found = [(key, row) for key, (s, row) in rows.items()
                 if s == season and row['home'] in HOMES and row['away'] in AWAYS]
        if len(found) != 1:
            raise ValueError('Sample is not unique for ' + season)
        key, row = found[0]
        chosen.append((season, key, row))
    return chosen


def binding(item, rows, directory):
    file = item['source_file']
    path = directory / file
    if not path.resolve().is_relative_to(directory.resolve()):
        raise ValueError('Source path escapes private directory')
    if sha(path.read_bytes()) != item['source_sha256']:
        raise ValueError('Source hash changed')
    key = (file, item['original']['source_line'])
    if key not in rows or rows[key] != (item['season'], item['original']):
        raise ValueError('Original fixture/season binding changed')
    return key


def claims(items, evidence):
    ids = set()
    counts = Counter()
    for item in items:
        if item['id'] in ids:
            raise ValueError('Duplicate claim id')
        ids.add(item['id'])
        if not item['finding'] or not item['evidence_urls']:
            raise ValueError('Missing claim reasoning/source')
        evs = [evidence[url] for url in item['evidence_urls']]
        for ev in evs:
            if not ev['url'].startswith('https://') or not ev['title'] or not ev['reviewed_on']:
                raise ValueError('Missing documentary metadata')
        if item['status'] == 'VERIFIED':
            if not any(ev['access'] == 'DOCUMENT_OPENED' for ev in evs):
                raise ValueError('Indexed-only evidence cannot verify a fixture')
            if item['independence'] != 'EDITORIAL_EVIDENCE' or not item['independence_note']:
                raise ValueError('Unestablished source independence')
            observed = item['observed']
            if not observed or set(observed) != set(FACTS):
                raise ValueError('Verified claim lacks all five facts')
            date.fromisoformat(observed['date'])
            for side in ('home', 'away'):
                if item['team_correspondence'].get(observed[side]) != item['original'][side]:
                    raise ValueError('Unexplained team correspondence')
            for goal in ('hg', 'ag'):
                if type(observed[goal]) is not int or observed[goal] < 0:
                    raise ValueError('Invalid transcribed score')
            if any(observed[k] != item['original'][k] for k in ('date',)) or any(
                    observed[k] != int(item['original'][k]) for k in ('hg', 'ag')):
                raise ValueError('Contradiction requires explicit unresolved/correction review')
        elif item['status'] != 'UNRESOLVED' or item['observed'] is not None:
            raise ValueError('Unknown status or silently resolved claim')
        if item['proposed_change'] is not None:
            raise ValueError('Unexpected fixture correction')
        counts[item['status']] += 1
    return dict(counts)


def rounds(items, frozen, evidence):
    if len(items) != len(frozen) or len(items) != 34:
        raise ValueError('Scheduling case lost')
    counts = Counter()
    fixtures = set()
    outliers = set()
    for index, (item, original) in enumerate(zip(items, frozen), 1):
        if item['id'] != f'S{index:02}' or item['original'] != original:
            raise ValueError('Frozen scheduling evidence changed')
        if item['fixtures_individually_verified_by_round_explanation'] is not False:
            raise ValueError('Round explanation cannot certify fixtures')
        if item['proposed_change'] is not None or not item['finding']:
            raise ValueError('Scheduling repair or missing finding')
        if [x['original'] for x in item['outlier_reviews']] != original['outside_densest_seven_day_cluster']:
            raise ValueError('Diagnostic outlier lost/changed')
        for row in item['outlier_reviews']:
            if row['status'] != 'CONTEXT_REVIEWED_NOT_INDIVIDUALLY_CERTIFIED':
                raise ValueError('Unsupported outlier certification')
        if item['status'] not in ('EXPLAINED', 'PARTIAL', 'UNRESOLVED'):
            raise ValueError('Unknown scheduling status')
        if not item['evidence_urls']:
            raise ValueError('Missing scheduling evidence')
        if item['status'] == 'EXPLAINED' and not any(
                evidence[url]['access'] == 'DOCUMENT_OPENED' for url in item['evidence_urls']):
            raise ValueError('Explanation lacks inspected evidence')
        counts[item['status']] += 1
        for row in original['all_round_fixtures']:
            fixtures.add((original['season'], row['source_line']))
        for row in original['outside_densest_seven_day_cluster']:
            outliers.add((original['season'], row['source_line']))
    if (len(fixtures), len(outliers)) != (340, 52):
        raise ValueError('Scheduling fixture/outlier scope changed')
    return dict(counts), fixtures, outliers


def build(directory=PRIVATE, root=ROOT):
    baseline = read_json(directory / 'phase5_protected_before.json')
    if len(baseline) != 485:
        raise ValueError('Phase 5 protection scope changed')
    protected_count = protect(baseline, root)
    frozen = read_json(directory / 'phase4_structural_validation.json')
    ledger = read_json(directory / LEDGER)
    selected = read_json(directory / 'phase5_sample_selection.json')
    rows = records(directory)
    if len(rows) != 13844:
        raise ValueError('Approved fixture population changed')
    actual = selection(rows)
    if len(ledger['samples']) != 36 or ledger['method'] != selected['method']:
        raise ValueError('Sample procedure/scope changed')
    sample_keys = set()
    for i, (item, fixed, expected) in enumerate(zip(ledger['samples'], selected['samples'], actual), 1):
        key = binding(item, rows, directory)
        if (item['season'], key, item['original']) != expected or item['id'] != f'L{i:02}':
            raise ValueError('Sample differs from reproducible selection')
        if any(item[k] != fixed[k] for k in ('id', 'season', 'original', 'source_file', 'source_sha256')):
            raise ValueError('Frozen sample selection changed')
        sample_keys.add(key)
    sample_counts = claims(ledger['samples'], ledger['sources'])
    extra_keys = {binding(x, rows, directory) for x in ledger['supplemental_fixtures']}
    if len(extra_keys) != len(ledger['supplemental_fixtures']) or sample_keys & extra_keys:
        raise ValueError('Supplemental fixture double-count')
    extra_counts = claims(ledger['supplemental_fixtures'], ledger['sources'])
    round_counts, round_keys, outlier_keys = rounds(ledger['rounds'], frozen['scheduling_candidates'], ledger['sources'])
    groups = frozen['diagnostic_label_variant_groups']
    if len(ledger['identities']) != 18 or {x['group'] for x in ledger['identities']} != set(groups):
        raise ValueError('Identity review group lost')
    for item in ledger['identities']:
        if item['mapping_applied'] is not False or item['labels'] != [r['label'] for r in groups[item['group']]]:
            raise ValueError('Identity mapping applied/labels changed')
    if ledger['applied_corrections'] or ledger['applied_exclusions'] or any(
            x['applied'] is not False for x in ledger['proposed_policy']):
        raise ValueError('Phase 5 must not apply transformations')
    if 'Seven' not in ledger['closure_regression_item']:
        raise ValueError('Separate regression item lost')
    inputs = ['phase5_protected_before.json', 'phase5_sample_selection.json', LEDGER,
              'phase5_review_sources.json', 'phase5_document_discovery.json', 'phase5_document_access.json']
    round_bindings = {(f"openfootball/espana/{s[:4]}-{s[-2:]}/1-liga.txt", line)
                      for s, line in round_keys}
    outlier_bindings = {(f"openfootball/espana/{s[:4]}-{s[-2:]}/1-liga.txt", line)
                        for s, line in outlier_keys}
    all_claims = sample_keys | extra_keys
    return dict(phase=5, original_records=len(rows), protected_files=protected_count,
                samples=sample_counts, supplemental_fixtures=extra_counts,
                distinct_fixture_claims=len(all_claims), scheduling_rounds=round_counts,
                context_and_fixture_review_union=len(all_claims | round_bindings),
                priority_fixture_union=len(all_claims | outlier_bindings),
                outliers_without_individual_full_fact_claim=len(outlier_bindings - all_claims),
                scheduling_fixtures=len(round_keys), diagnostic_outliers=len(outlier_keys),
                identity_groups=18, applied_corrections=0, applied_exclusions=0,
                input_sha256={name:sha((directory/name).read_bytes()) for name in inputs},
                code_sha256={name:sha((root/name).read_bytes()) for name in
                             ['scripts/verify_la_liga_review.py','tests/test_la_liga_review.py']},
                limitation='Consistency and preservation checks only; no population certification or training permission.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--write', action='store_true')
    args = parser.parse_args()
    raw = encode(build())
    target = PRIVATE / OUTPUT
    if args.check:
        if target.read_bytes() != raw:
            raise ValueError('Phase 5 assessment differs from deterministic regeneration')
    else:
        if target.exists():
            if target.read_bytes() != raw:
                raise ValueError('Refusing to overwrite a different assessment')
        else:
            with target.open('xb') as stream:
                stream.write(raw)
    print(raw.decode(), end='')


if __name__ == '__main__':
    main()
