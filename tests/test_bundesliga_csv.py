"""CSV schema/coverage regressions using fictional data only."""
import csv
from pathlib import Path

from scripts.validate_bundesliga_csv import audit_file


def datahub(path,rows):
    with path.open('w',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=['Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR'])
        writer.writeheader();writer.writerows(rows)


def complete_rows():
    return [dict(Date='2000-08-15',HomeTeam=f'Team {h}',AwayTeam=f'Team {a}',FTHG='2',FTAG='0',FTR='H')
            for h in range(18) for a in range(18) if h!=a]


def test_complete_datahub_season_uses_existing_validator(tmp_path):
    path=tmp_path/'season.csv';datahub(path,complete_rows())
    result=audit_file(path,'2000/01','datahub')
    assert result['status']=='PASS' and result['matches']==306 and result['teams']==18
    assert result['missing_pairings']==0 and result['historical_validator']=='PASS'
    assert all(v==dict(home=17,away=17) for v in result['balance'].values())


def test_plausible_total_cannot_hide_missing_and_duplicate_fixtures(tmp_path):
    rows=complete_rows();rows[-1]={**rows[0],'Date':'2000-08-16'}
    path=tmp_path/'season.csv';datahub(path,rows)
    result=audit_file(path,'2000/01','datahub')
    codes={i['code'] for i in result['issues']}
    assert result['matches']==306 and result['status']=='REVIEW'
    assert 'duplicate_fixture' in codes and 'missing_pairings' in codes


def test_missing_scores_and_wrong_results_are_reported_not_repaired(tmp_path):
    rows=complete_rows();rows[0]['FTHG']='';rows[1]['FTR']='A';rows[2]['Date']='1998-08-01'
    path=tmp_path/'season.csv';datahub(path,rows)
    original=path.read_bytes();result=audit_file(path,'2000/01','datahub')
    codes={i['code'] for i in result['issues']}
    assert {'missing_required_value','score_result_mismatch','date_outside_season'}<=codes
    assert result['parsed_matches']<result['matches'] and path.read_bytes()==original


def test_early_twenty_team_schedule_annotations_and_names(tmp_path):
    n=20;clubs=list(range(n));rounds=[]
    for _ in range(n-1):
        rounds.append([(clubs[i],clubs[-1-i]) for i in range(n//2)])
        clubs=[clubs[0],clubs[-1],*clubs[1:-1]]
    rounds += [[(a,h) for h,a in pairs] for pairs in rounds]
    path=tmp_path/'early.csv'
    with path.open('w',newline='',encoding='utf-8') as handle:
        writer=csv.DictWriter(handle,fieldnames=['Round','Date','Team 1','FT','HT','Team 2']);writer.writeheader()
        for day,pairs in enumerate(rounds,1):
            for h,a in pairs:
                writer.writerow({'Round':day,'Date':'(Sat) 3 Aug 1991 (30)','Team 1':f'Club {h} ({day})',
                                 'Team 2':f'Club {a} ({day})','FT':'2-1','HT':'1-0'})
    before=path.read_bytes();result=audit_file(path,'1991/92','early')
    assert result['status']=='PASS' and result['matches']==380 and result['teams']==20
    assert len(result['round_counts'])==38 and result['expected_matches']==380
    assert all('(' not in t for t in result['team_names']) and path.read_bytes()==before


def test_halftime_greater_than_administrative_result_is_flagged_for_review(tmp_path):
    path=tmp_path/'early.csv'
    path.write_text('Round,Date,Team 1,FT,HT,Team 2\n1,(Sat) 3 Aug 1991 (30),Old Name (1),2-0,1-3,Opponent (1)\n')
    result=audit_file(path,'1991/92','early')
    assert any(i['code']=='halftime_exceeds_fulltime' for i in result['issues'])
    assert result['matches']==1 and result['status']=='REVIEW'
