"""Read-only checks of the recorded independent review; never applies corrections.

PYTHONPATH=src .venv/bin/python -m scripts.verify_second_bundesliga_review
External observations are manually recorded evidence, not re-fetched by this check.
"""
from collections import Counter
import csv
import hashlib
import io
import json
from pathlib import Path

from scripts.validate_second_bundesliga import PRIVATE, build


def digest(content):
    return hashlib.sha256(content).hexdigest()


def bound_row(directory, binding):
    content = (directory / binding['source_file']).read_bytes()
    if digest(content) != binding['source_sha256']:
        raise ValueError('Source checksum changed')
    for number, row in enumerate(csv.DictReader(io.StringIO(content.decode('utf-8-sig'))), 2):
        if number == binding['source_row']:
            if row != binding['original_fields']:
                raise ValueError('Source row/fields changed')
            return row
    raise ValueError('Source row absent')


def check_correction(directory, correction):
    row = bound_row(directory, correction['source'])
    if correction['applied'] is not False or correction['status'] != 'VERIFIED_PENDING_STANDARDIZATION':
        raise ValueError('Review must not apply corrections')
    expected = dict(Date='2005-11-04', Season='2005', home='Wacker Burghausen',
                    visitor='1860 Munchen', FT='0-2', hgoal='0', vgoal='2', tier='2', division='2')
    replacements = dict(Date='2006-03-29', FT='1-0', hgoal='1', vgoal='0')
    if row != expected or correction['replacements'] != replacements or not correction['evidence']:
        raise ValueError('Unapproved correction')
    return row


def check_samples(samples):
    ids = set()
    full = Counter()
    for sample in samples:
        if sample['sample_id'] in ids:
            raise ValueError('Duplicate sample')
        ids.add(sample['sample_id'])
        observation = sample['observed']
        if not sample['reference_url'].startswith('https://'):
            raise ValueError('Missing source URL')
        if observation['competition'] != '2. Bundesliga' or observation['regular_season'] is not True:
            raise ValueError('Wrong competition')
        for key in ('date', 'home_goals', 'away_goals'):
            if sample[key] != observation[key]:
                raise ValueError('Result discrepancy')
        for key in ('home_team', 'away_team'):
            if sample['team_identity_mapping'].get(observation[key]) != sample[key]:
                raise ValueError('Unexplained team identity')
        if sample['access'] == 'FULL_PAGE':
            full[(int(sample['date'][:4]) // 10) * 10] += 1
        elif sample['access'] != 'INDEXED_ONLY':
            raise ValueError('Unknown evidence access')
    if any(full[d] < 5 for d in (1990, 2000, 2010, 2020)):
        raise ValueError('Insufficient full-page calendar-decade coverage')
    return dict(sorted(full.items()))


def main():
    review = PRIVATE / 'verification'
    read = lambda name: json.loads((review / name).read_text())
    fingerprints = read('protected_before.json')
    for filename, checksum in fingerprints.items():
        if digest(Path(filename).read_bytes()) != checksum:
            raise ValueError('Protected file changed: ' + filename)
    outputs = build()
    for name, content in outputs.items():
        if (PRIVATE / name).read_bytes() != content:
            raise ValueError('Structural audit no longer reproducible: ' + name)
    structural = json.loads(outputs['structural_validation.json'])
    if structural['acquired_source_records'] != 11488 or structural['complete_fixture_seasons'] != 36:
        raise ValueError('Incomplete historical coverage')
    samples = read('independent_verification.json')['matches']
    selected = sum([read(name)['matches'] for name in ('sample_selection.json', 'supplementary_selection.json', 'calendar_supplement_selection.json')], [])
    if len(selected) != len(samples):
        raise ValueError('Selections replaced or removed')
    for selection, sample in zip(selected, samples):
        if any(sample[k] != value for k, value in selection.items()):
            raise ValueError('Selection altered')
        content = (PRIVATE / sample['source_file']).read_bytes()
        if digest(content) != sample['source_sha256']:
            raise ValueError('Sample source changed')
        if sample['source_file'].endswith('.csv'):
            row = next(r for i, r in enumerate(csv.DictReader(io.StringIO(content.decode('utf-8-sig'))), 2) if i == sample['source_row'])
            actual = (row['Date'], row['home'], row['visitor'], int(row['hgoal']), int(row['vgoal']))
            wanted = tuple(sample[k] for k in ('date','home_team','away_team','home_goals','away_goals'))
            if actual != wanted:
                raise ValueError('Sample differs from original')
        else:
            matches = [r for r in structural['extracted_records'] if r['source_row'] == sample['source_row'] and r['season'] == sample['season']]
            if len(matches) != 1 or any(matches[0][k] != sample[k] for k in ('date','home_team','away_team','home_goals','away_goals')):
                raise ValueError('TXT sample differs from original')
    decades = check_samples(samples)
    corrections = read('verified_corrections.json')['corrections']
    if len(corrections) != 1:
        raise ValueError('Unexpected corrections')
    check_correction(PRIVATE, corrections[0])
    policy = read('exception_policy.json')
    if policy['unlisted_training_suitability'] != 'UNRESOLVED' or len(policy['known_match_cases']) != 9:
        raise ValueError('Exception policy changed')
    for case in policy['known_match_cases']:
        bound_row(PRIVATE, case['source'])
        if case['training_suitability'] != 'EXCLUDED':
            raise ValueError('Known exception eligibility assumed')
    print(json.dumps(dict(records=11488, seasons=36, protected_files_unchanged=len(fingerprints),
                         full_page_samples=sum(decades.values()), full_page_calendar_decades=decades,
                         indexed_only_samples=sum(s['access']=='INDEXED_ONLY' for s in samples),
                         exceptions=9, proposed_corrections=1, corrections_applied=0), indent=2))


if __name__ == '__main__':
    main()
