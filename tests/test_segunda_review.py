"""Synthetic evidence-strength, scope, identity and preservation guards."""
from copy import deepcopy
import json

import pytest

from scripts import verify_segunda_review as review


def document():
    return dict(id='doc', url='https://example.org/fixture', title='Synthetic original match account',
                publisher='Synthetic club', document_date='2020-01-01', reviewed_on='2026-11-22',
                finding='Synthetic facts, no real-world certification', limitations='Synthetic test only',
                access='DOCUMENT_OPENED', independence='PRIMARY_EVENT_RECORD',
                supports=sorted(review.FACTS | {'scheduling'}))


def original(key='ordinary', year=2012, **changes):
    r = dict(source_fixture_id=key, season=f'{year}/{year+1}', source_line=1,
             home='Home', away='Away', date=f'{year}-09-01', FT='2-1', round=((year-2012)%3)*14+1,
             source_marked_awarded=False, year_basis='INFERRED_YEAR_SEASON_WINDOW_AND_WEEKDAY')
    return dict(r, **changes)


def claim(r, status='VERIFIED'):
    facts = {k:r[k] for k in review.FACTS}
    return dict(source_fixture_id=r['source_fixture_id'], original=deepcopy(r), status=status,
                confidence='Synthetic', evidence=['doc'], independent_facts=facts,
                fact_support={k:['doc'] for k in facts}, finding='Synthetic independent comparison',
                limitations='Not legal-finality or population certification',
                event_dates=dict(actual_completion=None, result_known_by=None),
                processing_decision='NONE_PHASE5')


def unresolved_award(r):
    c=claim(r,'UNRESOLVED')
    c.update(independent_facts={},fact_support={},administrative_review=dict(
        source_date_proxy=r['date'],source_award=r['FT'],on_field_result=None,
        official_final_result=None,individual_award_decision_date=None,individual_publication_date=None,
        individual_appeal_finality_date=None,earliest_final_result_available=None))
    return c


def test_strong_comparison():
    r = original()
    assert review.check_claim(claim(r), r, {'doc':document()}) == []


@pytest.mark.parametrize('field,value', [('access','INDEX_ONLY'), ('independence','UNKNOWN_UPSTREAM'),
                                        ('independence','SECONDARY_LEGAL_REPORT')])
def test_weak_evidence_cannot_certify(field, value):
    r=original(); d=document(); d[field]=value
    with pytest.raises(ValueError, match='directly inspected'):
        review.check_claim(claim(r), r, {'doc':d})


def test_index_only_remains_partial():
    r=original(); d=document(); d['access']='INDEX_ONLY'
    assert review.check_claim(claim(r,'PARTIAL'), r, {'doc':d}) == []


def test_schedule_is_not_a_score_certificate():
    r=original(); d=document(); d['supports']=['scheduling']
    with pytest.raises(ValueError, match='Scheduling/identity'):
        review.check_claim(claim(r), r, {'doc':d})


def test_original_values_cannot_be_overwritten():
    r=original(); c=claim(r); c['original']['FT']='3-0'
    with pytest.raises(ValueError, match='binding'):
        review.check_claim(c,r,{'doc':document()})


def test_independent_missing_result_stays_additive():
    r=original(FT=None); c=claim(r); c['independent_facts']['FT']='2-1'
    assert review.check_claim(c,r,{'doc':document()}) == []
    assert r['FT'] is None and c['original']['FT'] is None


def test_verified_discrepancy_is_reported_not_repaired():
    r=original(); c=claim(r); c['independent_facts']['date']='2012-09-02'
    assert review.check_claim(c,r,{'doc':document()}) == ['date']
    assert r['date']=='2012-09-01'


def test_administrative_finality_cannot_pass_as_played_verification():
    r=original(source_marked_awarded=True)
    with pytest.raises(ValueError, match='Administrative finality'):
        review.check_claim(claim(r),r,{'doc':document()})


@pytest.mark.parametrize('mutation', ['status','award','availability','chronology'])
def test_unresolved_award_cannot_gain_unapproved_processing_metadata(mutation):
    r=original(source_marked_awarded=True); c=unresolved_award(r)
    if mutation=='status': c['status']='PARTIAL'
    if mutation=='award': c['administrative_review']['source_award']='0-3'
    if mutation=='availability': c['administrative_review']['earliest_final_result_available']=r['date']
    if mutation=='chronology': c['event_dates']['result_known_by']=r['date']
    with pytest.raises(ValueError):review.check_claim(c,r,{'doc':document()})


def test_result_cannot_be_known_before_completion():
    r=original(); c=claim(r)
    c['event_dates']=dict(actual_completion='2020-06-10',result_known_by='2019-12-15')
    with pytest.raises(ValueError, match='precedes completion'):
        review.check_claim(c,r,{'doc':document()})


def test_no_phase6_decision_allowed():
    r=original(); c=claim(r); c['processing_decision']='EXCLUDE'
    with pytest.raises(ValueError, match='outside Phase 5'):
        review.check_claim(c,r,{'doc':document()})


@pytest.mark.parametrize('score', ['2-?', '-1-0', '2', '2-1-0'])
def test_invalid_independent_scores(score):
    r=original(); c=claim(r); c['independent_facts']['FT']=score
    with pytest.raises(ValueError, match='full-time score'):
        review.check_claim(c,r,{'doc':document()})


def test_unknown_fact_support_rejected():
    r=original(); c=claim(r); c['fact_support']['FT']=['other']
    with pytest.raises(ValueError, match='not bound'):
        review.check_claim(c,r,{'doc':document()})


def test_duplicate_evidence_rejected():
    with pytest.raises(ValueError, match='Duplicate evidence'):
        review.sources([document(),document()])


def test_duplicate_json_keys_rejected(tmp_path):
    p=tmp_path/'duplicate.json'; p.write_text('{"id":1,"id":2}')
    with pytest.raises(ValueError, match='Duplicate JSON'):
        review.read(p)


def test_stratified_selection_deterministic_and_unflagged():
    rs=[original(f'{y}-{j}',y,source_line=j) for y in range(2012,2025) for j in range(3)]
    flagged={f'{y}-0' for y in range(2012,2025)}
    chosen=review.selection(rs,flagged)
    assert chosen==review.selection(list(reversed(rs)),flagged)
    assert len(chosen)==13 and not flagged.intersection(r['source_fixture_id'] for r in chosen)
    assert all(r['year_basis'].startswith('INFERRED') for r in chosen)


def test_empty_sample_stratum_fails():
    with pytest.raises(ValueError, match='Empty ordinary'):
        review.selection([],set())


def synthetic_assessment():
    rs=[original(str(y),y) for y in range(2012,2025)]
    reserves=[original('reserve'+str(i),2012,home=n) for i,n in enumerate(sorted(review.structural.RESERVES))]
    targets=[original('missing',FT=None), original('award',source_marked_awarded=True),
             original('outlier'), original('high',FT='6-6')]
    categories=['MISSING_FULLTIME_SCORE','SOURCE_MARKED_ADMINISTRATIVE_AWARD',
                'DIAGNOSTIC_DATE_OUTLIER','UNUSUAL_SCORE_REVIEW']
    q=[dict(fixture=r,categories=[category]) for r,category in zip(targets,categories)]
    q += [dict(fixture=r,categories=['RESERVE_IDENTITY_REVIEW']) for r in reserves]
    all_rows=rs+reserves+targets
    # Unique physical source lines within season, including synthetic targets.
    for i,r in enumerate(all_rows): r['source_line']=i+1
    span=dict(season='2012/2013',round=1,lines=[targets[2]['source_line']],
              diagnostic_outlier_lines=[targets[2]['source_line']])
    report=dict(records=all_rows,seasons=[dict(season=f'{y}/{y+1}',validation=dict(source_order_reversals=[])) for y in range(2012,2025)],scheduling=[span])
    claims=[claim(r) for r in rs+targets]
    claims[-4]['independent_facts']['FT']='2-1'
    claims[-3]=unresolved_award(targets[1])
    groups=[dict(source_label=r['home'],fixture_ids=[r['source_fixture_id']],seasons=['2012/2013'],
                 keep_separate_from_parent=True,apply_mapping=False,evidence=['doc']) for r in reserves]
    rounds=[dict(season='2012/2013',round=1,original=span,fixture_ids=['outlier'],outlier_ids=['outlier'],
                 evidence=['doc'],status='DOCUMENTED',finding='Synthetic postponement',limitations='Context only')]
    return report,dict(records=q),dict(records=rs),dict(sources=[document()],fixtures=claims,rounds=rounds,identities=groups)


def test_assessment_deduplicates_groups_and_does_not_certify_reserves():
    r,q,s,l=synthetic_assessment(); result,matrix=review.assess(r,q,s,l)
    assert result['individually_reviewed']==17
    assert result['grouped_reserve_observations']==6
    assert result['unresolved_administrative_awards']==1
    assert result['missing_original_scores']==1
    assert result['fixture_status_counts']=={'VERIFIED':16,'UNRESOLVED':1}
    assert sum(x['fixture_review_status']=='NOT_INDIVIDUALLY_REVIEWED' for x in matrix)==6
    assert not result['confirmed_source_discrepancies']


@pytest.mark.parametrize('mutation', ['sample','omitted_claim','omitted_round','reserve_merge','reserve_mapping','duplicate_claim','round_binding'])
def test_assessment_scope_failures(mutation):
    r,q,s,l=synthetic_assessment()
    if mutation=='sample': s['records']=s['records'][:-1]
    if mutation=='omitted_claim': l['fixtures'].pop()
    if mutation=='omitted_round': l['rounds']=[]
    if mutation=='reserve_merge': l['identities'][0]['keep_separate_from_parent']=False
    if mutation=='reserve_mapping': l['identities'][0]['apply_mapping']=True
    if mutation=='duplicate_claim': l['fixtures'].append(deepcopy(l['fixtures'][0]))
    if mutation=='round_binding': l['rounds'][0]['outlier_ids']=[]
    with pytest.raises(ValueError): review.assess(r,q,s,l)


def test_frozen_files_and_append_only_log(tmp_path,monkeypatch):
    root=tmp_path; directory=root/'private';directory.mkdir()
    (root/'old').write_bytes(b'original'); (root/'PLANNING_LOG.md').write_bytes(b'history\n')
    baseline=dict(files={'old':review.base.sha(b'original')},planning_log=dict(bytes=8,sha256=review.base.sha(b'history\n')))
    (directory/review.BASELINE).write_text(json.dumps(baseline))
    monkeypatch.setattr(review.structural,'protect',lambda *args:{'protected':True})
    assert review.protect(directory,root)['phase2_4_files']==1
    (root/'PLANNING_LOG.md').write_bytes(b'history\nappend\n')
    review.protect(directory,root)
    (root/'old').write_bytes(b'changed')
    with pytest.raises(ValueError,match='protected file'):review.protect(directory,root)


def test_rewriting_planning_history_rejected(tmp_path,monkeypatch):
    directory=tmp_path/'private';directory.mkdir();(tmp_path/'old').write_bytes(b'x')
    (tmp_path/'PLANNING_LOG.md').write_bytes(b'edited')
    (directory/review.BASELINE).write_text(json.dumps(dict(files={'old':review.base.sha(b'x')},planning_log=dict(bytes=3,sha256=review.base.sha(b'old')))))
    monkeypatch.setattr(review.structural,'protect',lambda *args:{})
    with pytest.raises(ValueError,match='Planning history'):review.protect(directory,tmp_path)
