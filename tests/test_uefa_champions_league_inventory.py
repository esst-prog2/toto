"""Synthetic UCL score-period and structural regression cases; no private rows."""
import csv
from datetime import date
import io
from pathlib import Path

import pytest

from scripts import inventory_uefa_champions_league as production
from scripts import verify_uefa_champions_league_inventory as independent


def source(kind='csv',season='2013/2014'):
    return dict(path='synthetic/'+('clq.txt' if kind=='qualifying' else 'champs.csv' if kind=='csv' else 'cl.txt'),
                sha256='a'*64,publisher='footballcsv/europe-champions-league' if kind=='csv' else 'openfootball/champions-league',season=season)


def csv_bytes(**changes):
    row=dict(zip(production.COLUMNS,['Knockout','Final','','(Sat) 24 May 2014 (W20)',
                                    'Alpha, United › ABC (1)','1-1 (*)','0-1','Beta › XYZ (2)',
                                    '2-2 (agg.)','3-1 (a.e.t.)','4-2 (pen.)','']))
    row.update(changes);out=io.StringIO(newline='');w=csv.DictWriter(out,fieldnames=production.COLUMNS,lineterminator='\n');w.writeheader();w.writerow(row)
    return out.getvalue().encode()


@pytest.mark.parametrize('token,reg,after,pens,half',[
    ('2-1 (1-0)',[2,1],None,None,[1,0]),
    ('0-0',[0,0],None,None,None),
    ('4-2 a.e.t. (2-2, 0-1)',[2,2],[4,2],None,[0,1]),
    ('11-10 pen. 2-0 a.e.t. (2-0, 1-0)',[2,0],[2,0],[11,10],[1,0]),
    ('3-4 pen. 1-1 a.e.t. (1-1, 0-0)',[1,1],[1,1],[3,4],[0,0]),
])
def test_named_periods_never_use_leading_shootout_or_extra_time(token,reg,after,pens,half):
    periods,issues=production.txt_periods(token)
    assert not issues
    assert [periods[k] for k in ('regulation_time','after_extra_time','shootout','half_time')]==[reg,after,pens,half]
    assert independent.text_scores(token)==periods


@pytest.mark.parametrize('token',['3-2 pen. 0-0 a.e.t. (0-0)','1-1 a.e.t. (0-0)','2-1 a.e.t.'])
def test_one_or_missing_parenthesis_does_not_infer_regulation_even_when_zero(token):
    periods,issues=production.txt_periods(token)
    assert periods['regulation_time'] is None
    assert periods['after_extra_time'] is not None
    assert 'ET_SINGLE_OR_MISSING_PARENTHESIS_PERIOD_AMBIGUITY' in issues
    assert independent.text_scores(token)==periods


def test_shootout_without_explicit_football_period_is_ambiguous():
    periods,issues=production.txt_periods('5-4 pen. 1-1 (0-0)')
    assert periods['regulation_time'] is None and periods['shootout']==[5,4]
    assert 'SHOOTOUT_WITHOUT_EXPLICIT_PERIOD_BASIS' in issues


def test_administrative_annotation_is_not_assumed_observed_regulation_score():
    periods,issues=production.txt_periods('3-0 [awarded]')
    assert periods['regulation_time'] is None
    assert periods['unassigned_period_scores']==[[3,0]]
    assert 'UNPARSED_SCORE_TRAILER' in issues


def test_csv_periods_aggregate_quoted_names_and_annotations_survive_inventory():
    row=production.parse_csv(csv_bytes(),source())[0]
    assert row['home']=='Alpha, United'
    assert row['raw_home']=='Alpha, United › ABC (1)'
    assert row['home_association']=='ABC'
    assert row['periods']['regulation_time']==[1,1]
    assert row['periods']['after_extra_time']==[3,1]
    assert row['periods']['aggregate']==[2,2]
    assert row['periods']['shootout']==[4,2]
    assert row['periods']['raw_score_fields']['FT']=='1-1 (*)'
    assert row['source_fields']['ET']=='3-1 (a.e.t.)'


def test_multiline_csv_uses_physical_span_and_keeps_original_comment():
    raw=csv_bytes(Comments='source note\ncontinuation')
    row=production.parse_csv(raw,source())[0]
    assert row['line']==2 and row['end_line']==3
    assert row['source_fields']['Comments']=='source note\ncontinuation'
    assert row['physical_sha256']==production.sha(b''.join(raw.splitlines(keepends=True)[1:3]))


def test_csv_wrong_width_fails_closed():
    raw=csv_bytes()+b'bad,short,row\n'
    with pytest.raises(ValueError,match='width'):production.parse_csv(raw,source())


def test_csv_unknown_score_not_guessed_from_embedded_numbers():
    row=production.parse_csv(csv_bytes(FT='90 minute result unspecified; 4-3 shootout'),source())[0]
    assert row['periods']['regulation_time'] is None
    assert 'REGULATION_SCORE_UNKNOWN' in row['issues']


def test_period_annotation_survives_complete_txt_intermediate_record():
    raw=b'= UEFA Champions League 2013/14\n\n\xe2\x96\xaa Final\nSat May 24 2014\n  20:00 Alpha (ABC)  v Beta (XYZ)  5-4 pen. 3-3 a.e.t. (2-2, 1-0)\n'
    row=production.parse_txt(raw,source('txt'))[0]
    assert 'a.e.t.' in row['annotation'] and 'pen.' in row['annotation']
    assert row['periods']['regulation_time']==[2,2]
    assert row['periods']['after_extra_time']==[3,3]
    assert row['periods']['shootout']==[5,4]
    assert row['source_fields']['raw_line'].endswith('(2-2, 1-0)')
    assert row['date_source_line']==4 and row['stage_source_line']==3


@pytest.mark.parametrize('raw_stage,raw_round,raw_group,expected',[
    ('Qualifying','Playoff Round | Leg 2','','QUALIFYING_PLAYOFF'),
    ('','Playoffs, Matchday 1','','KNOCKOUT_PLAYOFF'),
    ('Group 1st','Matchday ?','1|A','FIRST_GROUP'),
    ('Group 2nd','Matchday ?','2|A','SECOND_GROUP'),
    ('','Round 1 | Leg 2','','PRE_GROUP_ROUND_1'),
    ('','Prelim. Round | Leg 1','','PRELIMINARY'),
])
def test_era_and_scope_specific_stage_membership(raw_stage,raw_round,raw_group,expected):
    assert production.stage('csv',raw_stage,raw_round,raw_group)[1]==expected


def test_june_qualification_and_august_covid_date_windows():
    june='= UEFA Champions League - Quali 2015/16\n▪ Round 1\nTue Jun 30 2015\nAlpha (ABC) v Beta (XYZ)  1-0\n'.encode()
    row=production.parse_txt(june,source('qualifying','2015/2016'))[0]
    assert row['date']=='2015-06-30' and not row['issues'] and row['scope']=='QUALIFYING'
    august='= UEFA Champions League 2019/20\n▪ Final\nSun Aug 23 2020\nAlpha (ABC) v Beta (XYZ)  1-0\n'.encode()
    assert production.parse_txt(august,source('txt','2019/2020'))[0]['date']=='2020-08-23'


def test_invalid_heading_isolated_without_assigning_a_date():
    raw='= UEFA Champions League 2013/14\n▪ Final\nMon May 24 2014\nAlpha (ABC) v Beta (XYZ)  1-0\n'.encode()
    row=production.parse_txt(raw,source('txt'))[0]
    assert row['date'] is None
    assert 'AMBIGUOUS_OR_INVALID_DATE_HEADING' in row['issues']


def test_new_stage_does_not_inherit_previous_date_heading():
    raw='= UEFA Champions League 2013/14\n▪ Semifinals\nTue Apr 22 2014\nAlpha (ABC) v Beta (XYZ)  1-0\n▪ Final\nGamma (GAM) v Delta (DEL)  1-0\n'.encode()
    row=production.parse_txt(raw,source('txt'))[-1]
    assert row['date'] is None and row['date_source_line'] is None
    assert 'MISSING_EXACT_DATE' in row['issues']


def test_unrecognized_source_line_not_silently_discarded():
    with pytest.raises(ValueError,match='Unrecognized'):
        production.parse_txt(b'= UCL\nUnknown fixture without separator\n',source('txt'))


def test_replay_remains_an_extra_observation_for_review():
    raw=csv_bytes(Round='Round 1 | Replay')
    row=production.parse_csv(raw,source())[0]
    assert row['replay'] and row['stage']=='PRE_GROUP_ROUND_1'


def test_output_refuses_overwrite(tmp_path,monkeypatch):
    monkeypatch.setattr(production,'build',lambda:{'summary.json':{'x':1}})
    production.run(tmp_path)
    with pytest.raises(FileExistsError):production.run(tmp_path)
    production.run(tmp_path,check=True)
    (tmp_path/'summary.json').write_text('{}')
    with pytest.raises(ValueError,match='reproduction'):production.run(tmp_path,check=True)


def overlap_row(oid,publisher,home,away,goals,stage='FINAL'):
    return dict(observation_id=oid,publisher=publisher,season='2011/2012',scope='MAIN',stage=stage,
                date='2012-05-19',home=home,away=away,
                home_association='ABC' if home=='Alpha' else 'XYZ',
                away_association='ABC' if away=='Alpha' else 'XYZ',
                periods=dict(regulation_time=goals,half_time=None,after_extra_time=None,shootout=None))


def test_neutral_final_orientation_compared_without_rewriting_sources():
    left=overlap_row('left','footballcsv/europe-champions-league','Alpha','Beta',[2,1])
    right=overlap_row('right','openfootball/champions-league','Beta','Alpha',[1,2])
    links,names,membership=production.reconcile([left,right])
    assert links[0]['orientation']=='REVERSED_SOURCE_DESIGNATION'
    assert links[0]['periods_equal']['regulation_time'] is True
    assert right['home']=='Beta' and right['periods']['regulation_time']==[1,2]
    assert independent.identity_links([left,right])[1]==[('left','right','REVERSED_SOURCE_DESIGNATION')]


def test_exact_club_correspondence_exposes_score_conflict_instead_of_avoiding_link():
    left=overlap_row('left','footballcsv/europe-champions-league','Alpha','Beta',[2,1])
    right=overlap_row('right','openfootball/champions-league','Alpha','Beta',[3,1])
    links,_,_=production.reconcile([left,right])
    assert len(links)==1 and links[0]['periods_equal']['regulation_time'] is False


def test_comparator_does_not_fill_unknown_original_regulation_score():
    left=overlap_row('left','footballcsv/europe-champions-league','Alpha','Beta',[0,0])
    right=overlap_row('right','openfootball/champions-league','Alpha','Beta',None)
    links,_,_=production.reconcile([left,right])
    assert len(links)==1 and links[0]['periods_equal']['regulation_time'] is None
    assert right['periods']['regulation_time'] is None


def test_detailed_outputs_refuse_public_repository_destination(monkeypatch):
    public=Path(__file__).resolve().parents[1]/'docs'/'_private_inventory_must_not_be_written'
    monkeypatch.setattr(production,'build',lambda:{'summary.json':{'x':1}})
    with pytest.raises(ValueError,match='private'):production.run(public)
    with pytest.raises(ValueError,match='private'):independent.private_output(public)
    assert not public.exists()
