"""Synthetic guards: no private source files or external requests required."""
import csv
import hashlib
import io
from copy import deepcopy

import pytest

from scripts.verify_second_bundesliga_review import bound_row, check_correction, check_samples


def correction_fixture(tmp_path):
    row = dict(Date='2005-11-04', Season='2005', home='Wacker Burghausen',
               visitor='1860 Munchen', FT='0-2', hgoal='0', vgoal='2', tier='2', division='2')
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=row)
    writer.writeheader()
    writer.writerow(row)
    content = stream.getvalue().encode()
    (tmp_path / 'sample.csv').write_bytes(content)
    return dict(applied=False, status='VERIFIED_PENDING_STANDARDIZATION', evidence=['https://example.org/evidence'],
                replacements=dict(Date='2006-03-29', FT='1-0', hgoal='1', vgoal='0'),
                source=dict(source_file='sample.csv', source_sha256=hashlib.sha256(content).hexdigest(),
                            source_row=2, original_fields=row))


def test_guard_does_not_apply_correction(tmp_path):
    correction = correction_fixture(tmp_path)
    before = (tmp_path / 'sample.csv').read_bytes()
    assert check_correction(tmp_path, correction)['FT'] == '0-2'
    assert (tmp_path / 'sample.csv').read_bytes() == before


@pytest.mark.parametrize('fault', ['bytes', 'row', 'fields', 'replacement', 'applied'])
def test_correction_guard_rejects_changes(tmp_path, fault):
    correction = correction_fixture(tmp_path)
    if fault == 'bytes':
        (tmp_path / 'sample.csv').write_bytes(b'changed')
    elif fault == 'row':
        correction['source']['source_row'] = 3
    elif fault == 'fields':
        correction['source']['original_fields']['FT'] = '1-0'
    elif fault == 'replacement':
        correction['replacements']['home'] = 'Renamed'
    else:
        correction['applied'] = True
    with pytest.raises(ValueError):
        check_correction(tmp_path, correction)


def sample_fixture():
    return [dict(sample_id=f'{year}-{i}', date=f'{year}-01-01', home_team='Home', away_team='Away',
                 home_goals=1, away_goals=0, access='FULL_PAGE', reference_url='https://example.org/result',
                 team_identity_mapping={'Heim': 'Home', 'Gast': 'Away'},
                 observed=dict(date=f'{year}-01-01', home_team='Heim', away_team='Gast', home_goals=1,
                               away_goals=0, competition='2. Bundesliga', regular_season=True))
            for year in (1995, 2005, 2015, 2025) for i in range(5)]


def test_calendar_decades_and_explicit_aliases():
    assert check_samples(sample_fixture()) == {1990: 5, 2000: 5, 2010: 5, 2020: 5}


@pytest.mark.parametrize('fault', ['indexed', 'calendar', 'alias', 'score', 'cup', 'duplicate'])
def test_sample_assurance_not_overstated(fault):
    samples = deepcopy(sample_fixture())
    sample = samples[0]
    if fault == 'indexed':
        sample['access'] = 'INDEXED_ONLY'
    elif fault == 'calendar':
        sample['date'] = sample['observed']['date'] = '2000-01-01'
    elif fault == 'alias':
        sample['observed']['home_team'] = 'Unknown'
    elif fault == 'score':
        sample['observed']['home_goals'] = 2
    elif fault == 'cup':
        sample['observed']['regular_season'] = False
    else:
        samples.append(deepcopy(sample))
    with pytest.raises(ValueError):
        check_samples(samples)
