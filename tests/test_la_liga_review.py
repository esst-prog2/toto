"""Synthetic evidence guards. No private fixture data or network access."""
from copy import deepcopy
import json

import pytest

from scripts import verify_la_liga_review as v


def evidence():
    return {'https://example.test/report': dict(url='https://example.test/report',
            title='Contemporary match report', reviewed_on='2026-11-22', access='DOCUMENT_OPENED')}


def claim():
    return dict(id='L01', original=dict(date='2000-09-01', home='Club A', away='Club B', hg='2', ag='1'),
                observed=dict(date='2000-09-01', home='A', away='B', hg=2, ag=1),
                team_correspondence={'A':'Club A', 'B':'Club B'}, evidence_urls=['https://example.test/report'],
                finding='Teams/date/full-time score directly inspected.', status='VERIFIED',
                independence='EDITORIAL_EVIDENCE', independence_note='Contemporary authored report.',
                proposed_change=None)


def test_claim_check_is_read_only_and_counts_facts():
    c=claim(); before=deepcopy(c)
    assert v.claims([c], evidence())=={'VERIFIED':1}
    assert c==before


@pytest.mark.parametrize('change', ['indexed','lineage','date','home','goals','fraction','missing','repair','reason','duplicate'])
def test_unsupported_fixture_claims_fail_explicitly(change):
    c=claim(); e=evidence(); cs=[c]
    if change=='indexed':e['https://example.test/report']['access']='INDEXED_ONLY'
    if change=='lineage':c['independence']='UNESTABLISHED'
    if change=='date':c['observed']['date']='2000-09-02'
    if change=='home':c['team_correspondence']['A']='Other Club'
    if change=='goals':c['observed']['hg']=3
    if change=='fraction':c['observed']['hg']=2.0
    if change=='missing':del c['observed']['away']
    if change=='repair':c['proposed_change']={'date':'2000-09-02'}
    if change=='reason':c['finding']=''
    if change=='duplicate':cs.append(deepcopy(c))
    with pytest.raises(ValueError):v.claims(cs,e)


def test_unresolved_indexed_evidence_is_permitted_without_observed_facts():
    c=claim(); c.update(status='UNRESOLVED', observed=None, independence='UNESTABLISHED')
    e=evidence(); e['https://example.test/report']['access']='INDEXED_ONLY'
    assert v.claims([c],e)=={'UNRESOLVED':1}
    c['observed']={}
    with pytest.raises(ValueError):v.claims([c],e)


def population():
    return {('source.csv', y): (f'{y}/{y+1}', dict(source_line=y,home='Real Madrid',away='FC Barcelona'))
            for y in range(1990,2026)}


def test_selection_covers_every_season_and_ignores_order():
    rows=population()
    assert v.selection(rows)==v.selection(dict(reversed(list(rows.items()))))
    assert len(v.selection(rows))==36


@pytest.mark.parametrize('change',['missing','duplicate','wrong_home','wrong_away'])
def test_sample_selection_is_unique_and_explicit(change):
    rows=population()
    if change=='missing':del rows['source.csv',1990]
    if change=='duplicate':rows['other.csv',1]=deepcopy(rows['source.csv',1990])
    if change=='wrong_home':rows['source.csv',1990][1]['home']='Real Madrid B'
    if change=='wrong_away':rows['source.csv',1990][1]['away']='Barcelona B'
    with pytest.raises(ValueError):v.selection(rows)


def test_baseline_rejects_change_and_path_escape(tmp_path):
    f=tmp_path/'original'; f.write_bytes(b'unchanged')
    b={'original':v.sha(b'unchanged')}
    assert v.protect(b,tmp_path)==1
    f.write_bytes(b'changed')
    with pytest.raises(ValueError):v.protect(b,tmp_path)
    with pytest.raises(ValueError):v.protect({'../outside':'bad'},tmp_path)


def test_binding_requires_exact_source_hash_line_season_and_facts(tmp_path):
    f=tmp_path/'source'; f.write_bytes(b'original')
    c=dict(source_file='source',source_sha256=v.sha(b'original'),season='2000/2001',original={'source_line':7})
    rows={('source',7):('2000/2001',{'source_line':7})}
    assert v.binding(c,rows,tmp_path)==('source',7)
    c['original']['source_line']=8
    with pytest.raises(ValueError):v.binding(c,rows,tmp_path)
    c['original']['source_line']=7; c['source_sha256']='bad'
    with pytest.raises(ValueError):v.binding(c,rows,tmp_path)


def test_json_duplicate_keys_are_rejected(tmp_path):
    f=tmp_path/'evidence.json'; f.write_text('{"status":"UNRESOLVED","status":"VERIFIED"}')
    with pytest.raises(ValueError,match='Duplicate JSON key'):v.read_json(f)


def synthetic_rounds():
    frozen=[]; items=[]
    for i in range(34):
        rows=[dict(source_line=10*i+j) for j in range(10)]
        outside=rows[:2 if i<18 else 1]
        c=dict(season='2000/2001',all_round_fixtures=rows,outside_densest_seven_day_cluster=outside)
        frozen.append(c)
        items.append(dict(id=f'S{i+1:02}',original=deepcopy(c),evidence_urls=['https://example.test/report'],
                          status='EXPLAINED',finding='Documented scheduling change.',
                          outlier_reviews=[dict(original=deepcopy(r),status='CONTEXT_REVIEWED_NOT_INDIVIDUALLY_CERTIFIED') for r in outside],
                          fixtures_individually_verified_by_round_explanation=False,proposed_change=None))
    return items,frozen


def test_round_counts_do_not_claim_fixture_certification():
    items,frozen=synthetic_rounds()
    counts,fixtures,outliers=v.rounds(items,frozen,evidence())
    assert counts=={'EXPLAINED':34} and len(fixtures)==340 and len(outliers)==52


@pytest.mark.parametrize('change',['lost_case','lost_outlier','changed_source','blanket_claim','indexed','repair'])
def test_round_scope_and_claim_guards(change):
    items,frozen=synthetic_rounds(); e=evidence()
    if change=='lost_case':items.pop()
    if change=='lost_outlier':items[0]['outlier_reviews'].pop()
    if change=='changed_source':items[0]['original']['season']='2001/2002'
    if change=='blanket_claim':items[0]['fixtures_individually_verified_by_round_explanation']=True
    if change=='indexed':e['https://example.test/report']['access']='INDEXED_ONLY'
    if change=='repair':items[0]['proposed_change']={'date':'2001-01-01'}
    with pytest.raises(ValueError):v.rounds(items,frozen,e)
