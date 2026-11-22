"""Synthetic tests for the independent raw-source verifier."""
import json
import pytest
from scripts import collect_ligue2_feasibility as c
from scripts import validate_ligue2_feasibility as v
from scripts import verify_ligue2_feasibility as independent


def setup_source(tmp_path, body='A v B  2-1'):
    raw=f'= French Ligue 2 2024/25\n▪ Matchday 1\nFri Aug 16 2024\n{body}\n'.encode()
    rows,_=v.parse_text(raw,2024);p=tmp_path/'source.txt';p.write_bytes(raw)
    saved=dict(sources=[dict(receipt=dict(path='source.txt',sha256=c.sha(raw),repository=c.REPO,season='2024/2025'),records=rows)])
    (tmp_path/'feasibility_assessment.json').write_text(json.dumps(saved));return saved


@pytest.mark.parametrize('body',['A v B  2-1','A v B [cancelled]','A v B [postponed]','A v B'])
def test_independent_raw_parser(tmp_path,body):
    setup_source(tmp_path,body);r=independent.reconcile(tmp_path);assert r[0]['raw_records']==1 and r[0]['exact']


@pytest.mark.parametrize('field,value',[('date','2024-08-17'),('home','Changed'),('away','Changed'),('hg','9'),('ag','9'),('round',2),('source_line',100),('annotation','[award]')])
def test_independent_rejects_tampered_assessment(tmp_path,field,value):
    saved=setup_source(tmp_path);saved['sources'][0]['records'][0][field]=value
    (tmp_path/'feasibility_assessment.json').write_text(json.dumps(saved))
    with pytest.raises((AssertionError,ValueError)):independent.reconcile(tmp_path)


def test_independent_rejects_changed_raw(tmp_path):
    setup_source(tmp_path);(tmp_path/'source.txt').write_bytes(b'changed')
    with pytest.raises((AssertionError,ValueError)):independent.reconcile(tmp_path)


def test_orientation_requires_complete_printed_table():
    with pytest.raises(ValueError):independent.orientation_diagnostic('Stages 1-20\nFinal Table:\n',[])
