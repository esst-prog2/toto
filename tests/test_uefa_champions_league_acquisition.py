"""Synthetic metadata-only bounds/permission tests; no downloads or private inputs."""
import json
from pathlib import Path

import pytest

from scripts import acquire_uefa_champions_league as module


@pytest.fixture
def plan(tmp_path,monkeypatch):
    research=tmp_path/'phase1_research';research.mkdir();items=[];trees={}
    tuples=[('footballcsv',y,'champs.csv') for y in range(1992,2016)]
    tuples += [('openfootball',y,'cl.txt') for y in range(2011,2026)]
    tuples += [('openfootball',y,'clq.txt') for y in (2024,2025)]
    for i,(owner,y,name) in enumerate(tuples):
        publisher='footballcsv/europe-champions-league' if owner=='footballcsv' else 'openfootball/champions-league'
        short=f'{y}-{(y+1)%100:02}';size=17109 if i<40 else 17126;sample=i<9
        license_path=research/'metadata'/owner/'LICENSE.md';license_path.parent.mkdir(parents=True,exist_ok=True);license_path.write_text('CC0 1.0 Universal — synthetic unit-test notice\n')
        tree=trees.setdefault(owner,{'sha':module.PINS[publisher],'truncated':False,'tree':[]})
        tree['tree'].append({'path':f'{short}/{name}','sha':'a'*40,'size':size,'type':'blob'})
        items.append(dict(publisher=publisher,commit=module.PINS[publisher],season=f'{y}/{y+1}',url=f'https://raw.githubusercontent.com/{publisher}/{module.PINS[publisher]}/{short}/{name}',path=f'phase1_research/samples/{owner}/{short}/{name}' if sample else f'phase1/originals/{owner}/{short}/{name}',already_sampled=sample,expected_bytes=size,expected_blob='a'*40,license_reference=str(license_path.relative_to(tmp_path)),license_sha256=module.acquisition.sha(license_path.read_bytes())))
    for owner,t in trees.items():(research/'metadata'/owner/'tree.json').write_text(json.dumps(t))
    plan=research/'plan.json';plan.write_text(json.dumps({'items':items}))
    monkeypatch.setattr(module,'BASE',tmp_path);monkeypatch.setattr(module,'RESEARCH',research);monkeypatch.setattr(module,'PLAN',plan)
    return plan,items


def test_exact_bounded_plan_accepted_without_network(plan):
    assert len(module.approved_items())==41


@pytest.mark.parametrize('change',['url','year','duplicate','size','license','tree'])
def test_scope_and_provenance_mutation_refused(plan,change):
    path,items=plan
    if change=='url':items[0]['url']=items[0]['url'].replace('raw.githubusercontent.com','example.org')
    elif change=='year':items[0]['season']='1991/1992'
    elif change=='duplicate':items[1]=dict(items[0])
    elif change=='size':items[0]['expected_bytes']+=1
    elif change=='license':items[0]['license_sha256']='b'*64
    elif change=='tree':
        p=module.RESEARCH/'metadata/footballcsv/tree.json';v=json.loads(p.read_text());v['truncated']=True;p.write_text(json.dumps(v))
    path.write_text(json.dumps({'items':items}))
    with pytest.raises(ValueError):module.approved_items()
