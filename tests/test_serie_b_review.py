"""Synthetic independent-review guards; no private historical fixtures."""
from copy import deepcopy
import json

import pytest

from scripts.verify_serie_b_review import binding, check_corrections, check_exceptions, check_samples, period
from scripts.validate_serie_b import sha


def fixture(day='2013-08-24',ident='S1'):
    original=dict(date=day,home='Alpha FC',away='Beta FC',hg=2,ag=1)
    return dict(id=ident,season='2013/2014',source=dict(file='source.txt',line=3,sha256='abc',raw_line='x'),
                original=original,observed=dict(date=day,home='Alpha',away='Beta',hg=2,ag=1,
                competition='Serie B',season='2013/2014',regular_season=True),identity_mapping={'Alpha':'Alpha FC','Beta':'Beta FC'},
                evidence_id='E',verification_status='VERIFIED',comparison='AGREES',evidence_note='Dated complete league result block')


def evidence(access='FULL_RESULTS_PAGE'):
    return {'E':dict(access=access,url='https://archive.example/result',locator='Round 1, dated block',lineage_note='Upstream lineage unresolved')}


@pytest.mark.parametrize('day,wanted',[('1997-08-01','1997–1999'),('1999-12-31','1997–1999'),('2000-01-01','2000–2009'),('2009-12-31','2000–2009'),('2010-01-01','2010–2019'),('2019-12-31','2010–2019'),('2020-01-01','2020–2026'),('2026-05-01','2020–2026')])
def test_calendar_period_boundaries(day,wanted):assert period(day)==wanted


def test_early_and_ongoing_dates_not_counted():
    for day in ('1996-09-01','2027-01-01'):
        with pytest.raises(ValueError):period(day)


def test_full_page_claim_and_explicit_aliases():
    result=check_samples([fixture()],evidence(),False)
    assert result['verified']==1 and not result['disagreements']


@pytest.mark.parametrize('mutation,match',[
    (lambda s:s['observed'].update(competition='Serie A'),'competition'),
    (lambda s:s['observed'].update(regular_season=False),'competition'),
    (lambda s:s['observed'].update(season='2014/2015'),'competition'),
    (lambda s:s['identity_mapping'].update(Alpha='Beta FC'),'identity'),
    (lambda s:s['observed'].update(hg=-1),'score'),
    (lambda s:s['observed'].update(date='2015-08-24'),'outside'),
    (lambda s:s['observed'].update(hg=3),'discrepancy'),
])
def test_false_verification_rejected(mutation,match):
    s=fixture();mutation(s)
    with pytest.raises(ValueError,match=match):check_samples([s],evidence(),False)


def test_snippets_never_satisfy_verification_or_quotas():
    with pytest.raises(ValueError,match='Unsupported verification'):check_samples([fixture()],evidence('INDEXED_ONLY'),False)
    with pytest.raises(ValueError,match='quotas'):check_samples([fixture()],evidence())


def test_duplicate_bindings_rejected_even_if_ids_differ():
    with pytest.raises(ValueError,match='Duplicate'):check_samples([fixture(),fixture(ident='S2')],evidence(),False)


def correction_pair(score=False):
    s=fixture();s['observed']['date']='2013-08-25';s['comparison']='DISAGREES';s['verification_status']='CONFIRMED_CORRECTION'
    replacements={'date':'2013-08-25'}
    if score:s['observed']['hg']=3;replacements['hg']=3
    c=dict(id='C1',sample_id=s['id'],source=s['source'],original=s['original'],replacements=replacements,
           applied=False,status='VERIFIED_PENDING_STANDARDIZATION',evidence_ids=['E'])
    return s,c


def test_guarded_date_correction_and_no_mutation():
    s,c=correction_pair();before=deepcopy((s,c))
    check_corrections([c],[s],evidence())
    assert (s,c)==before
    assert check_samples([s],evidence(),False)['verified']==1


@pytest.mark.parametrize('field,value',[('applied',True),('status','APPROVED_BY_GUESS'),('replacements',{'hg':3}),('evidence_ids',[])])
def test_invalid_correction_guard(field,value):
    s,c=correction_pair();c[field]=value
    with pytest.raises(ValueError):check_corrections([c],[s],evidence())


def test_score_corrections_need_confirmed_final_administrative_outcome():
    s,c=correction_pair(True)
    with pytest.raises(ValueError,match='final outcome'):check_corrections([c],[s],evidence())
    c['final_administrative_status']='CONFIRMED_FINAL';check_corrections([c],[s],evidence())


def test_missing_or_duplicate_corrections_and_index_only_evidence_rejected():
    s,c=correction_pair()
    with pytest.raises(ValueError,match='Missing'):check_corrections([],[s],evidence())
    with pytest.raises(ValueError,match='Duplicate'):check_corrections([c,c],[s],evidence())
    with pytest.raises(ValueError,match='full evidence'):check_corrections([c],[s],evidence('INDEXED_ONLY'))


def policy():
    cases=[]
    for i in range(5):
        cases.append(dict(id=str(i),source=dict(file='s.txt',line=i+1),classification='PLAYED_ADMINISTRATIVE_STATUS_UNRESOLVED',
            training_suitability='UNRESOLVED',official_final_result=None,future_training_action='HOLD_OUT_PENDING_REVIEW',
            reason='Final order unlocated; on-field result known',evidence_ids=['E']))
    return dict(regular_cases=cases,unlisted_training_suitability='UNRESOLVED')


def test_unresolved_cases_are_not_automatically_ineligible_or_final():
    p=policy();assert check_exceptions(p,evidence())=={'UNRESOLVED':5}
    p['regular_cases'][0]['official_final_result']='2-0'
    with pytest.raises(ValueError,match='silently settled'):check_exceptions(p,evidence())


def test_unplayed_awards_cannot_have_invented_playing_events():
    p=policy();c=p['regular_cases'][0]
    c.update(classification='UNPLAYED_ADMINISTRATIVE_AWARD',training_suitability='EXCLUDED',actual_date=None,on_field_result=None)
    check_exceptions(p,evidence())
    c['actual_date']='2020-10-31'
    with pytest.raises(ValueError,match='unplayed'):check_exceptions(p,evidence())


def test_fixing_exclusion_needs_played_evidence():
    p=policy();p['regular_cases'][0].update(classification='PLAYED_MATCH_FIXING_CASE',training_suitability='EXCLUDED',actual_date='2013-08-24',on_field_result='2-1')
    check_exceptions(p,evidence())
    with pytest.raises(ValueError):check_exceptions(p,evidence('INDEXED_ONLY'))


def test_unlisted_eligibility_and_missing_exceptions_rejected():
    p=policy();p['unlisted_training_suitability']='ELIGIBLE'
    with pytest.raises(ValueError,match='Unlisted'):check_exceptions(p,evidence())
    p=policy();p['regular_cases'].pop()
    with pytest.raises(ValueError,match='Missing'):check_exceptions(p,evidence())


def test_exact_source_hash_line_scope_and_facts_binding(tmp_path):
    raw=b'= Synthetic\nFri Aug 23 2013\nAlpha  v Beta  2-1\n';p=tmp_path/'s.txt';p.write_bytes(raw)
    source=dict(file='s.txt',sha256=sha(raw),line=3,raw_line='Alpha  v Beta  2-1')
    details=[dict(file='s.txt',season='2013/2014',records=[dict(source_line=3,date='2013-08-23',home='Alpha',away='Beta',hg='2',ag='1')])]
    season,facts=binding(tmp_path,source,details)
    assert season=='2013/2014' and facts['hg']==2
    bad=dict(source,raw_line='changed')
    with pytest.raises(ValueError,match='line'):binding(tmp_path,bad,details)
    with pytest.raises(ValueError,match='outside'):binding(tmp_path,dict(source,file='../escape'),details)
    p.write_bytes(raw+b'changed')
    with pytest.raises(ValueError,match='checksum'):binding(tmp_path,source,details)


def test_aggregate_comparison_catches_score_changes():
    from scripts.verify_serie_b_review import aggregate_results
    rows=[dict(home='Alpha',away='Beta',hg='2',ag='1'),dict(home='Beta',away='Alpha',hg='0',ag='0')]
    totals=aggregate_results(rows)
    assert totals['Alpha']==dict(W=1,D=1,L=0,GF=2,GA=1,points=4)
    rows[0]['ag']='2'
    assert aggregate_results(rows)!=totals


def test_format_review_covers_every_surplus_row_and_its_sample_binding():
    from scripts.verify_serie_b_review import check_format_report
    s=fixture();s['source']['file']='source.csv'
    details=[dict(season='2003/2004',notes=[dict(code='extra_csv_fields',line=3)])]
    report=dict(file='source.csv',sha256='abc',rows=[dict(line=3,raw_line='x',sample_id='S1')])
    check_format_report(report,[s],details)
    report['rows']=[]
    with pytest.raises(ValueError,match='incompletely'):check_format_report(report,[s],details)
