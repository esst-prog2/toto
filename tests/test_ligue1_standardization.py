"""Synthetic standardization, exact-subset and private-audit safeguards."""
from copy import deepcopy
from pathlib import Path
import csv
import hashlib
import io
import json

import pytest

from scripts import standardize_ligue1_results as s
from test_ligue1_policy import context, row


def inputs():
    report,ledger,review=context()
    for i,r in enumerate(report['records']):
        if i>=45:
            r['away']='Visitor'+str(i)
    ledger["fixtures"]=[]
    approved=s.policy.make_policy(report,ledger,review)
    return [report,approved,ledger,review]


def projected(ctx):
    plans=s.prepare(*ctx)
    rows=sorted([p['projection'] for p in plans if p['projection']],key=lambda r:tuple(r[k] for k in ('league','season','date','home_team','away_team')))
    return plans,rows


def test_exact_schema_canonical_league_score_types_and_shared_id_algorithm():
    plans,rows=projected(inputs());assert rows
    assert tuple(rows[0])==('match_id','date','league','season','home_team','away_team','home_goals','away_goals')
    for r in rows:
        assert r['league']=='Ligue 1' and type(r['home_goals']) is int
        expected=hashlib.sha256(json.dumps(['Ligue 1',r['season'],r['date'],r['home_team'],r['away_team']],ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
        assert r['match_id']==expected


def test_five_holds_and_not_played_never_receive_projection():
    plans,_=projected(inputs())
    assert sum(p['assessment']['status']=='HOLD_OUT' for p in plans)==5
    assert all(p['projection'] is None for p in plans if p['assessment']['status']!='CANDIDATE_NOT_STANDARDIZED')


def test_partition_recomputed_without_trusting_imported_rows():
    ctx=inputs();plans,rows=projected(ctx);_,counts=s.verify_subset(rows,*ctx)
    assert counts['archived']==len(plans) and counts['screened']==len(rows)
    assert counts['administrative_holdouts']==4 and counts['disputed_date_holdouts']==1 and counts['not_played']==2


@pytest.mark.parametrize('mutation',['score','date','home','away','season','league','id','duplicate','missing','reorder','hold_leak'])
def test_export_mutations_and_silent_losses_fail_closed(mutation):
    ctx=inputs();plans,rows=projected(ctx);rows=deepcopy(rows)
    if mutation=='score':rows[0]['home_goals']+=1
    if mutation=='date':rows[0]['date']='1990-08-02'
    if mutation=='home':rows[0]['home_team']='Other club'
    if mutation=='away':rows[0]['away_team']='Other club'
    if mutation=='season':rows[0]['season']='1994/1995'
    if mutation=='league':rows[0]['league']='La Liga'
    if mutation=='id':rows[0]['match_id']='0'*64
    if mutation=='duplicate':rows.append(deepcopy(rows[0]))
    if mutation=='missing':rows.pop()
    if mutation=='reorder':rows.reverse()
    if mutation=='hold_leak':
        p=next(p for p in plans if p['assessment']['status']=='HOLD_OUT');r=p['original'];a=dict(date=r['date'],league='Ligue 1',season=r['season'],home_team=r['home'],away_team=r['away'],home_goals=int(r['hg']),away_goals=int(r['ag']))
        rows.append({k:({'match_id':s.standard_id(a),**a})[k] for k in s.OUTPUT_COLUMNS})
    with pytest.raises(ValueError):s.verify_subset(rows,*ctx)


def test_numeric_away_goals_override_defective_D_only_for_ordinary_matches():
    ctx=inputs();plans,_=projected(ctx)
    away=next(p for p in plans if 'SYSTEMATIC_SOURCE_LABEL_DEFECT' in p['original']['assessment']['flags'])
    assert away['original']['assessment']['source_result']=='D' and away['assessment']['candidate_outcome']=='A'
    assert away['projection']['home_goals']==0 and away['projection']['away_goals']==2
    assert all(p['projection'] is None for p in plans if p['assessment']['decision']=='HOLD_OUT_ADMIN_SCORE')


def test_replays_have_only_approved_effective_dates_and_Auxerre_stays_held():
    plans,_=projected(inputs())
    replays=[p for p in plans if p['assessment']['decision']=='APPROVED_REPLAY']
    assert {p['projection']['date'] for p in replays}=={'2021-10-27','2023-11-29'}
    aux=next(p for p in plans if p['assessment']['decision']=='HOLD_OUT_DATE_DISPUTE')
    assert aux['original']['date']=='1996-10-26' and aux['projection'] is None


def test_Brest_changes_candidate_labels_only_and_Ajaccio_clubs_stay_distinct():
    ctx=inputs();before=deepcopy(ctx);plans,_=projected(ctx)
    b=[p for p in plans if 'BREST_DUAL_LABEL_IDENTITY' in p['original']['assessment']['flags']]
    assert len(b)==38 and all(p['projection']['home_team']=='Brest Armorique FC' for p in b)
    assert ctx==before
    names={p['projection']['home_team'] for p in plans if p['projection']}
    assert {'AC Ajaccio','Gazélec FC Ajaccio'}<=names


@pytest.mark.parametrize('field,value',[('home_goals','-1'),('home_goals','01'),('home_goals','1.0'),('away_goals',''),('away_goals','١')])
def test_parse_rejects_noncanonical_numeric_scores(field,value):
    _,rows=projected(inputs());r=deepcopy(rows[0]);r[field]=value
    raw=s.serialize_csv([r],s.OUTPUT_COLUMNS)
    with pytest.raises(ValueError):s.parse_standard(raw)


def test_wrong_column_order_rejected():
    _,rows=projected(inputs());raw=s.serialize_csv(rows,tuple(reversed(s.OUTPUT_COLUMNS)))
    with pytest.raises(ValueError,match='schema'):s.parse_standard(raw)


def test_real_shared_importer_preserves_independent_projection_and_reordering(tmp_path):
    ctx=inputs();plans,rows=projected(ctx)
    raw,summary=s.convert(plans,tmp_path);repeat,_=s.convert(list(reversed(plans)),tmp_path)
    assert raw==repeat and s.parse_standard(raw)==rows
    assert summary['rejected']==0 and summary['accepted']==len(rows)


def test_modified_policy_or_source_cannot_be_exported():
    ctx=inputs();ctx[1]['decisions'].pop()
    with pytest.raises(ValueError):s.prepare(*ctx)
    ctx=inputs();ctx[0]['records'][0]['source_line']+=1
    with pytest.raises(ValueError):s.prepare(*ctx)


def test_duplicate_directed_pairing_rejected_even_if_source_ID_differs():
    ctx=inputs();r=deepcopy(ctx[0]['records'][-1]);r['source_line']+=500;r['audit_id']=s.policy.review.structural.source_id(r['source'],r['source_sha256'],r['source_line']);ctx[0]['records'].append(r)
    ctx[1]=s.policy.make_policy(ctx[0],ctx[2],ctx[3])
    with pytest.raises(ValueError,match='Duplicate directed'):s.prepare(*ctx)


def test_raw_audit_binding_cannot_be_changed(tmp_path):
    ctx=inputs();plans,_=projected(ctx);p=plans[0];r=p['original'];path=tmp_path/r['source'];path.parent.mkdir(parents=True)
    lines=[b'placeholder\n']*r['source_line'];lines[-1]=b'wrong raw record\n';path.write_bytes(b''.join(lines))
    documents={r['source']:dict(path=r['source'],url='https://example.org',commit='a'*40,git_blob_sha1='b'*40,sha256=r['source_sha256'])}
    with pytest.raises(ValueError,match='Raw original'):s.archive_records([p],ctx[1],ctx[2],documents,tmp_path)


def test_source_date_is_not_training_permission_and_same_day_denied():
    plans,_=projected(inputs());a=next(p['assessment'] for p in plans if p['projection'])
    assert not s.policy.training_allowed(a,'2030-01-01')
    assert not s.policy.known_strictly_before(a['effective_result_date'],a['effective_result_date'])


@pytest.mark.parametrize('status',['HOLD_OUT','NOT_PLAYED','CANDIDATE_NOT_STANDARDIZED'])
def test_complete_archive_preserves_original_values_and_restricted_null_projection(tmp_path,status):
    literal='Alpha v Béta  0-2 [awarded]\n'.encode()
    name='synthetic.txt';path=tmp_path/name;path.write_bytes(literal)
    r=row(0,source=name,hg=None if status=='NOT_PLAYED' else '0',ag=None if status=='NOT_PLAYED' else '2',label='D')
    r.update(source_sha256=s.base.sha(literal),source_line=1,raw_line_sha256=s.base.sha(literal),raw_record=literal.decode().rstrip('\n'))
    r['audit_id']=s.policy.review.structural.source_id(name,r['source_sha256'],1)
    r['assessment']['chronology']=dict(source_date=r['date'])
    a=dict(audit_id=r['audit_id'],status=status,decision='HOLD_OUT_ADMIN_SCORE' if status=='HOLD_OUT' else 'NOT_PLAYED' if status=='NOT_PLAYED' else 'ORDINARY_NUMERIC_RESULT',
           effective_result_date=r['date'] if status=='CANDIDATE_NOT_STANDARDIZED' else None,availability_basis='SOURCE_REPORTED_DATE_NOT_INDEPENDENTLY_CERTIFIED',availability_verified=False)
    projection=dict(match_id='x') if status=='CANDIDATE_NOT_STANDARDIZED' else None
    docs={name:dict(path=name,url='https://example.org/source',commit='a'*40,git_blob_sha1='b'*40,sha256=s.base.sha(literal))}
    out=s.archive_records([dict(original=r,assessment=a,projection=projection)],dict(decisions=[]),dict(fixtures=[],rounds=[],identity_cases=[]),docs,tmp_path)[0]
    assert out['original']==r and out['literal_original_record']==literal.decode()
    assert out['original']['assessment']['source_result']=='D'
    assert out['pinned_revision']=='a'*40 and out['raw_record_sha256']==s.base.sha(literal)
    if status!='CANDIDATE_NOT_STANDARDIZED':assert out['screened_match_id'] is None and out['approved_standardized_values'] is None


def test_shared_match_ID_distinguishes_league_and_season():
    r=dict(season='2020/2021',date='2020-08-01',home_team='Alpha',away_team='Béta')
    current=s.standard_id(r)
    other=hashlib.sha256(json.dumps(['La Liga',r['season'],r['date'],r['home_team'],r['away_team']],ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
    assert current!=other and s.standard_id({**r,'season':'2021/2022'})!=current
