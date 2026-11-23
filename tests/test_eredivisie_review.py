"""Synthetic evidence safeguards: no private fixtures or network needed."""
from copy import deepcopy
import json
from pathlib import Path
import pytest
from scripts import verify_eredivisie_review as review


def reference(access='DIRECT'):
    return dict(id='E1', url='https://example.test/report', title='Report', organization='Club',
                author=None, publication_date=None, retrieval_date='2026-11-23', access=access,
                independence='UNESTABLISHED', finding='Supported fact', rights='No training clearance')


def assessment():
    return dict(status='FULLY CORROBORATED', evidence_ids=['E1'],
                corroborated_core_facts=['home','away','date','FT','competition_season_context'],
                targeted_research=True, unresolved=['Finality not exhaustively investigated'])


def fixture(year, key, date=None, home='A', away='B', source='one', flags=None, scored=True):
    return dict(audit_id=key, season=f'{year}/{year+1}',date=date or f'{year}-08-01',
                home=home,away=away,source=source,structural=dict(score_bearing=scored,flags=flags or []))


def population():
    return [fixture(y, str(y)) for y in range(1990,2026)]


def test_selection_all_36_seasons():
    rows=population(); assert review.select(rows)==rows


def test_selection_is_order_independent():
    rows=population(); assert review.select(rows)==review.select(list(reversed(rows)))


def test_selection_excludes_flagged_and_null():
    rows=population()+[fixture(1990,'flag',date='1990-07-01',flags=['UNUSUAL_SCORE']),fixture(1990,'null',date='1990-07-02',scored=False)]
    assert review.select(rows)[0]['audit_id']=='1990'


def test_selection_requires_every_season():
    with pytest.raises(ValueError,match='Missing ordinary'):review.select(population()[:-1])


def test_selection_tie_break_literal_source():
    rows=population()+[fixture(1990,'tie',source='aaa')]
    assert review.select(rows)[0]['audit_id']=='tie'


def test_selection_does_not_modify_sources():
    rows=population();before=deepcopy(rows);review.select(rows);assert rows==before


@pytest.mark.parametrize('access',['DIRECT','INDEX_ONLY','DIRECT_TITLE_DATE_ONLY','DIRECT_MAINTENANCE'])
def test_explicit_access_classes(access):
    assert review.validate_references([reference(access)])['E1']['access']==access


@pytest.mark.parametrize('key',['title','organization','author','publication_date','retrieval_date','independence','rights'])
def test_reference_requires_metadata(key):
    item=reference();del item[key]
    with pytest.raises(ValueError,match='Missing reference'):review.validate_references([item])


def test_duplicate_reference_rejected():
    with pytest.raises(ValueError,match='duplicate reference'):review.validate_references([reference(),reference()])


def test_unknown_access_rejected():
    with pytest.raises(ValueError,match='Unknown access'):review.validate_references([reference('CERTIFIED_FROM_SNIPPET')])


def test_reference_requires_https():
    r=reference();r['url']='file:///private/source'
    with pytest.raises(ValueError):review.validate_references([r])


def test_direct_core_corroboration_valid_but_not_processing_policy():
    r=assessment();review.validate_review(r,{'E1':reference()});assert 'eligibility' not in r


@pytest.mark.parametrize('access',['INDEX_ONLY','DIRECT_TITLE_DATE_ONLY','DIRECT_MAINTENANCE'])
def test_uninspected_body_cannot_certify_core(access):
    with pytest.raises(ValueError,match='Index cannot certify'):review.validate_review(assessment(),{'E1':reference(access)})


def test_full_classification_requires_every_core_field():
    r=assessment();r['corroborated_core_facts'].remove('date')
    with pytest.raises(ValueError,match='lacks fields'):review.validate_review(r,{'E1':reference()})


def test_unknown_reference_rejected():
    with pytest.raises(ValueError,match='Unbound'):review.validate_review(assessment(),{})


def test_invalid_confidence_rejected():
    r=assessment();r['status']='AUTOMATICALLY ACCEPTED'
    with pytest.raises(ValueError):review.validate_review(r,{'E1':reference()})


def test_partial_index_lead_retains_unverified_state():
    r=assessment();r.update(status='UNRESOLVED',corroborated_core_facts=[])
    review.validate_review(r,{'E1':reference('INDEX_ONLY')})


def test_conditional_groups_link_only_approved_pairs():
    rows=[fixture(2023,'a'),fixture(2023,'b'),fixture(2023,'c')]
    result=review.groups(rows,[{'matches':[dict(historical_id='a',modern_id='b')]}])
    assert result=={'a':'a','b':'a','c':'c'}


def test_grouping_preserves_conflicting_original_scores():
    rows=[dict(fixture(2023,'a'),FT='1-3'),dict(fixture(2023,'b'),FT='1-2')];original=deepcopy(rows)
    review.groups(rows,[{'matches':[dict(historical_id='a',modern_id='b')]}]);assert rows==original


def test_unbound_group_raises():
    with pytest.raises(KeyError):review.groups([fixture(2023,'a')],[{'matches':[dict(historical_id='a',modern_id='missing')]}])


def test_duplicate_json_keys_rejected(tmp_path):
    p=tmp_path/'input.json';p.write_text('{"a":1,"a":2}')
    with pytest.raises(ValueError,match='Duplicate JSON'):review.read(p)
