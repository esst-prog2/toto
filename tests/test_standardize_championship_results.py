"""Synthetic Championship conversion regressions; no private data required."""
import csv
import hashlib
import io
import json
import sys

import pytest

from scripts import standardize_championship_results as converter
from scripts.standardize_england_results import convert_rows
from scripts.validate_championship_results import historical_name
from toto_estimator.data import load_historical_data
from toto_estimator.historical_import import OUTPUT_COLUMNS


def match(year=1990, **changes):
    return dict(dict(Date=f'{year}-08-25',Season=f'{year}/{year+1}',HomeTeam='A',AwayTeam='B',
                     hGoal='1',aGoal='0',Score='1-0',Result='H',Tier='2',Division=historical_name(year)),**changes)


@pytest.mark.parametrize('year',[1990,1992,2004,2016])
def test_all_historical_names_use_one_league_and_existing_identity(tmp_path,year):
    rows=[match(year),match(year,Date=f'{year}-09-01',HomeTeam='B',AwayTeam='A',hGoal='0',Score='0-0',Result='D')]
    content,summary=converter.convert_championship_rows(rows,tmp_path)
    assert content==converter.convert_championship_rows(rows[::-1],tmp_path)[0]
    records=list(csv.DictReader(io.StringIO(content.decode())))
    assert tuple(records[0])==OUTPUT_COLUMNS
    assert {r['league'] for r in records}=={'EFL Championship'}
    assert {r['season'] for r in records}=={f'{year}/{year+1}'}
    identity=['EFL Championship',f'{year}/{year+1}',f'{year}-08-25','A','B']
    assert records[0]['match_id']==hashlib.sha256(json.dumps(identity,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
    assert len(load_historical_data(io.StringIO(content.decode())))==2
    assert summary==dict(total=2,accepted=2,rejected=0,duplicates=0,fixtures=0,conflicts=0)
    assert not list(tmp_path.iterdir())


@pytest.mark.parametrize('change',[dict(Tier='1'),dict(Division='EFL Championship'),
                                    dict(HomeTeam=' A '),dict(Result='A'),dict(hGoal=''),dict(Score='2-0')])
def test_wrong_mapping_or_changed_invalid_facts_are_fatal(tmp_path,change):
    with pytest.raises(ValueError):
        converter.convert_championship_rows([match(**change)],tmp_path)


@pytest.mark.parametrize('change',[{},dict(Date='1990-09-01'),dict(hGoal='2',Score='2-0')])
def test_duplicates_not_silently_deduplicated(tmp_path,change):
    with pytest.raises(ValueError,match='importer|duplicate'):
        converter.convert_championship_rows([match(),match(**change)],tmp_path)


def test_league_participates_in_identity_and_pl_defaults_are_preserved(tmp_path):
    champ=match(2004)
    pl=match(2004,Tier='1',Division='Premier League')
    c=list(csv.DictReader(io.StringIO(converter.convert_championship_rows([champ],tmp_path)[0].decode())))[0]
    p=list(csv.DictReader(io.StringIO(convert_rows([pl],tmp_path)[0].decode())))[0]
    assert c['match_id']!=p['match_id']
    assert p['league']=='england.premier-league'
    assert all(c[k]==p[k] for k in OUTPUT_COLUMNS if k not in ('league','match_id'))


def test_creation_refuses_overwrite_before_build(tmp_path,monkeypatch):
    target=tmp_path/converter.OUTPUT_NAMES[0]
    target.write_bytes(b'preserve')
    monkeypatch.setattr(converter,'PRIVATE',tmp_path)
    monkeypatch.setattr(sys,'argv',['standardize_championship_results'])
    def fail_build():
        pytest.fail('must refuse overwrite before conversion')
    monkeypatch.setattr(converter,'build',fail_build)
    with pytest.raises(FileExistsError):converter.main()
    assert target.read_bytes()==b'preserve'


def test_check_reports_mismatch_without_replacing_output(tmp_path,monkeypatch):
    target=tmp_path/converter.OUTPUT_NAMES[0]
    target.write_bytes(b'preserve')
    monkeypatch.setattr(converter,'PRIVATE',tmp_path)
    monkeypatch.setattr(sys,'argv',['standardize_championship_results','--check'])
    monkeypatch.setattr(converter,'build',lambda:{target.name:b'different'})
    with pytest.raises(ValueError,match='differs'):converter.main()
    assert target.read_bytes()==b'preserve'
