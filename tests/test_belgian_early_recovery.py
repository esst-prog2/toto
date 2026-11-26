"""Synthetic gates and validators; never claim unavailable seasons were checked."""
from copy import deepcopy
from pathlib import Path
import pytest
from scripts import assess_belgian_early_recovery as r


def row(**changes):
    d=dict(season='1992/1993',competition='Belgian Pro League',stage='REGULAR_SEASON',
           date='1992-08-15',date_basis='EXPLICIT_MATCH_DATE',home='Club Brugge',away='Cercle Brugge',
           FT='2-1',hg='2',ag='1',source_id='source',original_sha256='a'*64,source_line=1)
    d.update(changes);return d


def receipt(raw=b'original'):
    return dict(acquisition_authorized=True,permission_basis='Explicit scoped synthetic grant',season='1992/1993',
                url='https://example.org/original',final_url='https://example.org/original',sha256=r.sha(raw),
                bytes=len(raw),retrieved_at_utc='2026-11-25T12:00:00+00:00',publisher='Example',encoding='utf-8',source_kind='WEB',git_commit=None,git_blob=None)


def test_permission_and_original_receipt_validated():
    r.require_permitted_original(receipt(),b'original')


@pytest.mark.parametrize('field,value',[('acquisition_authorized',False),('permission_basis','')])
def test_robots_or_public_readability_does_not_authorize_acquisition(field,value):
    rec=receipt();rec[field]=value
    with pytest.raises(ValueError,match='permission'):
        r.require_permitted_original(rec,b'original')


@pytest.mark.parametrize('field,value',[('season','1989/1990'),('season','1995/1996'),('sha256','wrong'),
 ('bytes',0),('url',''),('final_url',''),('retrieved_at_utc',''),('publisher',''),('git_commit','invented'),('git_blob','invented')])
def test_bad_or_unscoped_provenance_rejected(field,value):
    rec=receipt();rec[field]=value
    with pytest.raises(ValueError):
        r.require_permitted_original(rec,b'original')


def test_valid_row_preserves_names_and_date():
    original=row(home='RFC Liège',away='Cercle Brugge');before=deepcopy(original)
    assert r.row_errors(original)==[]
    assert original==before


@pytest.mark.parametrize('changes,error',[
 (dict(season='1995/1996'),'OUTSIDE_APPROVED_SEASONS'),
 (dict(competition='Belgian Cup'),'WRONG_COMPETITION_OR_STAGE'),
 (dict(stage='PROMOTION_RELEGATION'),'WRONG_COMPETITION_OR_STAGE'),
 (dict(date='1992-02-30'),'INVALID_EXPLICIT_MATCH_DATE'),
 (dict(date='1992-8-15'),'INVALID_EXPLICIT_MATCH_DATE'),
 (dict(date=None),'INVALID_EXPLICIT_MATCH_DATE'),
 (dict(date='1994-01-01'),'DATE_OUTSIDE_SEASON'),
 (dict(date_basis='ROUND_HEADING_PROXY'),'UNVERIFIED_DATE_PROXY'),
 (dict(home='Cercle Brugge'),'INVALID_PARTICIPANTS'),
 (dict(home=''),'INVALID_PARTICIPANTS'),
 (dict(home='Li\ufffdge'),'ENCODING_OR_CONTROL_CHARACTER'),
 (dict(away='Cercle\nBrugge'),'ENCODING_OR_CONTROL_CHARACTER'),
 (dict(FT=None),'MISSING_OR_INVALID_FINAL_SCORE'),
 (dict(FT='2-?'),'MISSING_OR_INVALID_FINAL_SCORE'),
 (dict(FT='-1-0'),'MISSING_OR_INVALID_FINAL_SCORE'),
 (dict(ag='2'),'SCORE_FIELDS_DISAGREE'),
 (dict(source_id=''),'MISSING_PHYSICAL_SOURCE_BINDING'),
 (dict(source_line=0),'MISSING_PHYSICAL_SOURCE_BINDING'),
 (dict(original_sha256=''),'MISSING_PHYSICAL_SOURCE_BINDING')])
def test_structural_errors_explicit(changes,error):
    assert error in r.row_errors(row(**changes))


def test_missing_coverage_is_not_a_fabricated_fixture_list():
    assessed=r.assess_rows([])
    assert assessed['observations']==assessed['scored']==assessed['directed_pairs']==0
    assert assessed['nominal_uncovered_slots']==306
    assert assessed['individual_fixture_validation']=='NOT_EXECUTED_NO_OBSERVATIONS'
    assert assessed['observed_home_away']=={}


def test_one_fixture_does_not_make_full_306_season():
    d=r.assess_rows([row()])
    assert d['observations']==1 and d['nominal_uncovered_slots']==305
    assert d['observed_home_away']['Club Brugge']==dict(home=1,away=0)
    assert d['observed_home_away']['Cercle Brugge']==dict(home=0,away=1)


def test_duplicate_and_conflicting_directed_fixture():
    d=r.assess_rows([row(),row(FT='0-0',hg='0',ag='0')])
    assert d['directed_pairs']==1 and d['duplicates'][0]['conflicting_scores']
    assert d['nominal_uncovered_slots']==305


def test_home_away_direction_is_distinct():
    d=r.assess_rows([row(),row(home='Cercle Brugge',away='Club Brugge')])
    assert d['directed_pairs']==2 and d['duplicates']==[]


@pytest.mark.parametrize('lineage,expected',[({},'PARTIAL'),({'a':'shared','b':'shared'},'PARTIAL'),
 ({'a':'independent_a','b':'independent_b'},'FULL_CORE')])
def test_agreement_requires_explicit_source_independence(lineage,expected):
    d=r.compare_explicit_rows([row(source_id='a'),row(source_id='b')],lineage)
    assert len(d)==1 and d[0]['corroboration']==expected
    assert d[0]['adjudicated'] is False


@pytest.mark.parametrize('change',[dict(date='1992-08-16'),dict(FT='0-0',hg='0',ag='0')])
def test_material_cross_source_discrepancies_remain_unresolved(change):
    rows=[row(source_id='a'),row(source_id='b',**change)]
    d=r.compare_explicit_rows(rows,dict(a='one',b='two'))[0]
    assert d['corroboration']=='CONFLICTING' and d['preliminary_recommendation']=='UNRESOLVED'


def test_date_proxy_cannot_become_fully_corroborated_candidate():
    d=r.compare_explicit_rows([row(source_id='a'),row(source_id='b',date_basis='ROUND_HEADING')],dict(a='one',b='two'))[0]
    assert d['corroboration']=='UNRESOLVED' and d['preliminary_recommendation']=='UNRESOLVED'


def test_award_or_interruption_needs_supplemental_adjudication():
    d=r.compare_explicit_rows([row(administrative_or_interruption_flag=True)],{})[0]
    assert d['preliminary_recommendation']=='UNRESOLVED'


def test_no_global_aliases_or_distinct_brugge_club_merge():
    d=r.compare_explicit_rows([row(),row(home='Brugge')],{})
    assert len(d)==2


def test_atomic_private_write_does_not_replace_original(tmp_path):
    f=tmp_path/'original.txt';r.policy.review.recovery.keep(f,b'original')
    r.policy.review.recovery.keep(f,b'original')
    with pytest.raises(ValueError):r.policy.review.recovery.keep(f,b'changed')
    assert f.read_bytes()==b'original'


def standings():
    # Balanced synthetic table, not historical evidence or a fixture reconstruction.
    return ('First Division (Eerste Klasse)\n'+''.join(f'{n}.Club{n} 34 10 14 10 30-30 34\n' for n in range(1,19))+'Second Division (Tweede Klasse)').encode()


def test_standings_only_corroborate_structure():
    d=r.rsssf_standings(standings())
    assert d['clubs']==18 and d['played_sum']==612 and d['nominal_aggregate_fixture_count']==306
    assert d['dated_fixture_observations']==0 and d['no_dates_or_scores_reconstructed']


def test_inconsistent_standings_not_forced_to_nominal_totals():
    with pytest.raises(ValueError,match='arithmetic'):
        r.rsssf_standings(standings().replace(b'34 10 14 10',b'33 10 14 10',1))


def test_duplicate_standings_club_detected():
    with pytest.raises(ValueError,match='population'):
        r.rsssf_standings(standings().replace(b'18.Club18',b'18.Club1'))
