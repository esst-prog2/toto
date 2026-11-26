"""Synthetic Phase 5 safeguards; no network and no private data required."""
from copy import deepcopy
import pytest
from scripts import verify_belgian_pro_league_review as review


def evidence(access='PRIMARY_DIRECT'):
    return {'source': dict(id='source', access=access, url='https://example.org/decision',
                           title='Decision', publisher='Federation', retrieved_date='2026-11-25',
                           independence='Original adjudicative document', rights='Not cleared',
                           document_kind='DECISION', supported_facts='Score fixed on appeal')}


def assessment(status='FULL_CORE'):
    return dict(status=status, evidence_ids=['source'], facts_checked=['teams', 'date', 'score', 'competition'])


@pytest.mark.parametrize('access', ['PRIMARY_DIRECT', 'SECONDARY_DIRECT'])
def test_direct_evidence_can_support_core(access):
    review.validate_evidence(evidence(access))
    review.validate_assessment(assessment(), evidence(access))


@pytest.mark.parametrize('access', ['SEARCH_INDEX_ONLY', 'INACCESSIBLE'])
def test_search_or_inaccessible_not_full(access):
    with pytest.raises(ValueError, match='inspected'):
        review.validate_assessment(assessment(), evidence(access))


@pytest.mark.parametrize('status', ['PARTIAL', 'UNRESOLVED', 'CONTEXT_ONLY', 'CONTRADICTED'])
def test_uncertain_status_is_not_silently_full(status):
    review.validate_assessment(assessment(status), evidence('SEARCH_INDEX_ONLY'))


@pytest.mark.parametrize('field', ['title', 'publisher', 'retrieved_date', 'independence', 'rights', 'document_kind'])
def test_provenance_required(field):
    e = evidence(); del e['source'][field]
    with pytest.raises(ValueError, match='metadata'):
        review.validate_evidence(e)


@pytest.mark.parametrize('field', ['eligible', 'disposition', 'standardized_date', 'canonical_team'])
def test_phase6_fields_forbidden(field):
    a = assessment(); a[field] = 'proposed'
    with pytest.raises(ValueError, match='Phase 6'):
        review.validate_assessment(a, evidence())


def test_statistical_lineage_does_not_imply_independence():
    e = evidence(); e['source']['independence'] = 'Statistical database: independent upstream not established'
    with pytest.raises(ValueError, match='independent corroboration'):
        review.validate_assessment(assessment(), e)


def test_missing_fact_coverage_fails():
    a = assessment(); a['facts_checked'].remove('date')
    with pytest.raises(ValueError, match='fact coverage'):
        review.validate_assessment(a, evidence())


def test_dangling_evidence_fails():
    with pytest.raises(ValueError, match='Dangling'):
        review.validate_assessment(assessment(), {})


def synthetic_sources():
    historical = []
    for year in range(1995, 2025):
        historical.extend([dict(season=f'{year}/{year+1}', date=f'{year}-09-03', home='Anderlecht',
                                away='Club Brugge', FT='1-0', stage='UNKNOWN', source_line=2),
                           dict(season=f'{year}/{year+1}', date=f'{year}-08-03', home='Club Brugge',
                                away='Anderlecht', FT='2-1', stage='UNKNOWN', source_line=3)])
    modern = {'2025-26/be1.txt': [dict(season='2025/2026', date='2025-08-03', home='Club Brugge KV',
                                     away='RSC Anderlecht', FT=None, stage='REGULAR_SEASON', source_line=1),
                                dict(season='2025/2026', date='2025-09-03', home='RSC Anderlecht',
                                     away='Club Brugge KV', FT='1-0', stage='REGULAR_SEASON', source_line=2)]}
    return historical, modern


def test_samples_cover_31_and_do_not_change_inputs():
    h, m = synthetic_sources(); before = deepcopy((h, m))
    s = review.select_samples(h, m)
    assert len(s) == 31 and len({r['season'] for r in s}) == 31
    assert all(r['observation']['date'].endswith('08-03') for r in s[:-1])
    assert s[-1]['observation']['FT'] == '1-0'
    assert (h, m) == before


def test_sample_deterministic_for_equal_date():
    h, m = synthetic_sources()
    h[0]['date'] = h[1]['date']
    assert review.select_samples(h, m)[0]['observation']['home'] == 'Anderlecht'


def test_missing_season_does_not_silently_reduce_sample():
    h, m = synthetic_sources()
    with pytest.raises(ValueError, match='No deterministic'):
        review.select_samples(h[2:], m)


def test_unscored_or_wrong_stage_not_sampled():
    h, m = synthetic_sources(); m['2025-26/be1.txt'][1]['stage'] = 'EUROPE'
    with pytest.raises(ValueError, match='2025/2026'):
        review.select_samples(h, m)


def test_same_city_does_not_merge_cercle_and_club():
    h, m = synthetic_sources(); h[0]['away'] = 'Cercle Brugge'; h[1]['home'] = 'Cercle Brugge'
    with pytest.raises(ValueError, match='1995/1996'):
        review.select_samples(h, m)


def test_malformed_access_fails():
    e = evidence('PRIMARY_ASSUMED')
    with pytest.raises(ValueError, match='identity/access'):
        review.validate_evidence(e)


def test_case_cannot_bind_wrong_score():
    case = dict(id='case', date='2022-01-01', home='Home', away='Away', score='5-0')
    row = dict(date='2022-01-01', home='Home', away='Away', FT='0-0')
    with pytest.raises(ValueError, match='immutable'):
        review.bind_cases([case], [row], [])


def test_case_cannot_invent_missing_observation():
    with pytest.raises(ValueError, match='immutable'):
        review.bind_cases([dict(id='missing', date='2022-01-01', home='H', away='A', score='5-0')], [], [])


def synthetic_contexts():
    sources = {}; contexts = []; index = {}
    for n in range(15):
        sid = str(n)
        row = dict(audit_id=sid, date='2020-09-01')
        index[sid] = row
        sources[str(n)] = dict(assessment=dict(wide_rounds=[dict(round='1', earliest=row['date'], latest=row['date'], source_ids=[sid])]))
        contexts.append(dict(path=str(n), round='1', status='PARTIAL', evidence_ids=[]))
    return dict(modern_sources=sources), contexts, index


def test_all_wide_contexts_preserve_exact_bindings():
    s, c, i = synthetic_contexts(); out = review.scheduling(s, c, i)
    assert len(out) == 15
    assert all(not r['all_fixtures_individually_verified'] and not r['confirmed_date_error'] for r in out)
    assert out[0]['source_bindings'] == [i['0']]


def test_missing_context_fails():
    s, c, i = synthetic_contexts()
    with pytest.raises(ValueError, match='Unreviewed'):
        review.scheduling(s, c[:-1], i)


def test_duplicate_context_fails():
    s, c, i = synthetic_contexts()
    with pytest.raises(ValueError, match='Duplicate'):
        review.scheduling(s, c + c[:1], i)


def test_context_cannot_claim_fixture_certification():
    s, c, i = synthetic_contexts(); c[0]['status'] = 'FULL_CORE'
    with pytest.raises(ValueError, match='context status'):
        review.scheduling(s, c, i)


def test_date_binding_change_fails():
    s, c, i = synthetic_contexts(); i['0']['date'] = '2020-10-01'
    with pytest.raises(ValueError, match='range'):
        review.scheduling(s, c, i)


def test_queue_cannot_hide_category_binding():
    q = dict(items=[dict(anchor='x', bindings=[dict(audit_id='x')], categories={'WIDE_ROUND': ['y']})])
    with pytest.raises(ValueError, match='Category'):
        review.queue_review(q, {}, [], [])


def test_queue_does_not_trust_different_saved_row():
    q = dict(items=[dict(anchor='x', bindings=[dict(audit_id='x', FT='5-0')], categories={})])
    with pytest.raises(ValueError, match='binding differs'):
        review.queue_review(q, {'x': dict(audit_id='x', FT='0-0')}, [], [])


def test_queue_must_not_drop_entries():
    with pytest.raises(ValueError, match='membership'):
        review.queue_review(dict(items=[], category_counts={}), {}, [], [])


def test_unknown_status_fails():
    with pytest.raises(ValueError, match='status'):
        review.validate_assessment(assessment('ASSUMED_CORRECT'), evidence())
