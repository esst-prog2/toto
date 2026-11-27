"""Synthetic schema/migration compatibility regressions; no historical rows."""
import csv
import hashlib
import io
import json

import pandas as pd
import pytest

from scripts.artifact_io import serialize_csv
from scripts.extend_domestic_neutrality import extend_bytes
from toto_estimator.config import HISTORICAL_DATA_PATH, SAMPLE_TICKET_PATH
from toto_estimator.data import load_historical_data, load_ticket_data, validate_historical_data
from toto_estimator.historical_import import HistoricalSource, import_historical_csvs
from toto_estimator.match_schema import CANONICAL_COLUMNS, LEGACY_COLUMNS, canonical_match_id, neutral_value, validate_canonical_records
from toto_estimator.models import DataValidationError
from toto_estimator.service import run_workflow


def record(**changes):
    row=dict(zip(LEGACY_COLUMNS,('', '2024-05-01','Synthetic League','2023/2024','Alpha, United','Béta','1','1')))
    row.update(changes)
    row['match_id']=canonical_match_id(*(row[c] for c in ('league','season','date','home_team','away_team')))
    return row


@pytest.mark.parametrize('value,expected',[(0,0),(1,1),('0',0),('1',1),('',None),(None,None)])
def test_neutral_wire_values(value,expected):
    assert neutral_value(value)==expected


@pytest.mark.parametrize('value',[True,False,2,-1,0.0,1.0,'0.0','NA',' 1','unknown',[]])
def test_neutral_wire_rejects_invalid_values(value):
    with pytest.raises(ValueError):neutral_value(value)


@pytest.mark.parametrize('value',[0,1,None])
def test_migration_preserves_bytes_rows_fields_and_ids(value):
    rows=[record(),record(date='2024-04-01',home_team='Béta',away_team='Alpha, United')]
    raw=serialize_csv(rows,LEGACY_COLUMNS)
    payload,report=extend_bytes(raw,value)
    r=csv.DictReader(io.StringIO(payload.decode()));actual=list(r)
    assert tuple(r.fieldnames)==CANONICAL_COLUMNS
    assert [{c:x[c] for c in LEGACY_COLUMNS} for x in actual]==rows
    assert serialize_csv(({c:x[c] for c in LEGACY_COLUMNS} for x in actual),LEGACY_COLUMNS)==raw
    assert report['changed_preexisting_fields']==report['changed_match_ids']==0
    assert report['unchanged_preexisting_fields']==16
    assert all(x['neutral_venue']==('' if value is None else str(value)) for x in actual)


def test_migration_refuses_already_migrated_or_noncanonical_bytes():
    old=serialize_csv([record()],LEGACY_COLUMNS)
    new,_=extend_bytes(old,0)
    with pytest.raises(ValueError,match='exact v1'):extend_bytes(new,0)
    with pytest.raises(ValueError,match='byte projection'):extend_bytes(old.replace(b'\n',b'\r\n'),0)


def test_migration_application_rejects_public_receipt_before_reading_plan(tmp_path):
    from scripts import extend_domestic_neutrality as migration
    with pytest.raises(ValueError,match='remain private'):
        migration.apply(tmp_path/'missing-plan.json', tmp_path, migration.ROOT/'docs/private-receipt.json')


def test_identity_is_exact_legacy_algorithm_and_excludes_new_metadata():
    r=record();identity=[r[c] for c in ('league','season','date','home_team','away_team')]
    assert r['match_id']==hashlib.sha256(json.dumps(identity,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
    for value in (0,1,None):
        extended=dict(r,neutral_venue=value)
        assert validate_canonical_records([extended])==1
    with pytest.raises(ValueError,match='duplicate'):validate_canonical_records([dict(r,neutral_venue=0)]*2)


@pytest.mark.parametrize('column,value',[('match_id','wrong'),('neutral_venue','2'),('date','2025-05-01'),('home_goals','1.0'),('home_team',' Alpha ')])
def test_canonical_validator_rejects_unapproved_mutation(column,value):
    r=dict(record(),neutral_venue=0);r[column]=value
    with pytest.raises(ValueError):validate_canonical_records([r])


def test_importer_explicit_v2_mode_preserves_v1_and_ids(tmp_path):
    p=tmp_path/'source.csv';p.write_text('Date,HomeTeam,AwayTeam,FTHG,FTAG\n01/05/2024,Alpha,Beta,1,1\n')
    source=HistoricalSource(p,'Synthetic',season='2023/2024',neutral_venue=1)
    old=import_historical_csvs([source]);new=import_historical_csvs([source],include_neutral_venue=True)
    assert tuple(old.records[0])==LEGACY_COLUMNS and tuple(new.records[0])==CANONICAL_COLUMNS
    assert {k:v for k,v in new.records[0].items() if k!='neutral_venue'}==old.records[0]
    assert new.records[0]['neutral_venue']==1
    conflict=import_historical_csvs([source,HistoricalSource(p,'Synthetic',season='2023/2024',neutral_venue=0)],include_neutral_venue=True)
    assert conflict.summary['conflicts']==2 and not conflict.records


@pytest.mark.parametrize('value',[0,1,pd.NA,None])
def test_synthetic_demo_predictions_unchanged_with_neutral_metadata(value):
    history=load_historical_data(HISTORICAL_DATA_PATH);ticket=load_ticket_data(SAMPLE_TICKET_PATH)
    expected=run_workflow(history,ticket)
    extended=history.copy(deep=True);extended['neutral_venue']=pd.array([value]*len(extended),dtype='Int8')
    validated=validate_historical_data(extended)
    assert str(validated['neutral_venue'].dtype)=='Int8'
    assert run_workflow(extended,ticket)==expected
    assert 'neutral_venue' not in history


def test_loader_accepts_blank_neutral_and_rejects_invalid_tokens(tmp_path):
    p=tmp_path/'history.csv';p.write_bytes(serialize_csv([dict(record(),neutral_venue=None)],CANONICAL_COLUMNS))
    frame=load_historical_data(p);assert frame['neutral_venue'].isna().all() and frame['result'].tolist()==['X']
    p.write_bytes(serialize_csv([dict(record(),neutral_venue='0.0')],CANONICAL_COLUMNS))
    with pytest.raises(DataValidationError) as exc:load_historical_data(p)
    assert exc.value.issues[0].code=='invalid_neutral_venue'
