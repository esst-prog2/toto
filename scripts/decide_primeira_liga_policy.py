"""Phase 6 only: source-bound provisional decisions and fail-closed chronology.

No standardized CSV, final audit archive, global aliases or application integration.
"""
import argparse
from collections import Counter,defaultdict
from copy import deepcopy
from datetime import date
import json,re,subprocess
from pathlib import Path
from scripts import verify_primeira_liga_review as review
c=review.c
ROOT,PRIVATE=review.ROOT,review.PRIVATE
BASELINE='phase6_protected_before.json'
NAMES=('phase6_source_observation_policy.json','phase6_unique_fixture_policy.json',
       'phase6_source_selection_registry.json','phase6_exception_registry.json',
       'phase6_chronology_registry.json','phase6_policy_summary.json','phase6_policy_manifest.json')
DISPOSITIONS={'COMPLETED_RESULT_CANDIDATE','HOLD_OUT','NOT_PLAYED'}
KNOWN_FLAGS={'WIDE_ROUND','SOURCE_ORDER_REVERSAL','UNUSUAL_SCORE','SOURCE_DISAGREEMENT','KNOWN_ABANDONMENT_REQUIRES_REVIEW','SOURCE_FIELD_OR_LABEL'}
HIST_PATH='jalapic/engsoccerdata/data-raw/portugal.csv'
HIST_PIN='872c5c354161ace8408f3091b758c6af4cccca94'
MODERN_PIN='63df627f3c87ce71708f016522ea236cf74332c3'
# IDs select cases; labels/date/score/physical lines also have to agree exactly.
SPECS={
'SANTA_PACOS':dict(season='2019/2020',score='2-1',completion='2020-02-02',kickoff=None,evidence='E0ca6a2deb4cf1d2a',rows=[('33862b4501af82fe70d76532a67a228dee8f326b6136ba54ef3dba90d8bab0a2',7290,'2020-02-01','Santa Clara','Pacos Ferreira'),('87d755690d6f59d64062dcec4f832c2ff220c3b65ce50ef518daaac10fbfecb8',298,'2020-02-02','CD Santa Clara','Paços de Ferreira')]),
'SANTA_BENFICA':dict(season='2020/2021',score='1-1',completion='2021-01-04',kickoff='2021-01-03',evidence='Eb98306db9fa073df',rows=[('07e7ee52db6b6ec435b234243d03e1ab9fb89b4cd4e4571aa587e7e06c1be69d',7532,'2021-01-03','Santa Clara','Benfica'),('7d350c9a6179c225329dbe7c3ec85aede0f7d538a0d8b53e9ef3fe4d26828c26',192,'2021-01-04','CD Santa Clara','SL Benfica')]),
'BELENENSES_BENFICA':dict(season='2021/2022',score='0-7',completion=None,kickoff='2021-11-27',evidence='E743f4cb2ffd885b5',rows=[('26b0148abfd2b370cf6d06a838a61f067cb93ddbeb693a132e5fdc73a08f74bc',7838,'2021-11-27','Belenenses','Benfica'),('422e5675208bd540a079b9a9cd94eb773db0e3efc128ed42b4da1f69480ddb9f',187,'2021-11-27','Belenenses SAD','SL Benfica')]),
'FEIRENSE_NACIONAL':dict(season='2011/2012',score='0-0',completion=None,kickoff=None,evidence='E5fffdc976f255faa',rows=[('5265c556cbad744e664ed5f55bec58e0117a48b279d3ef3aa1f435b2753aa25b',4877,'2011-08-14','Feirense ','Nacional')]),
'BENFICA_SALGUEIROS':dict(season='1995/1996',score='0-0',completion=None,kickoff=None,evidence='E9711d66249d15bab',rows=[('2675bb5e1717d5c4f907df689ded4a41889858974d19d18892a3035cb827570a',308,'1995-08-20','Benfica','Salgueiros')]),
'NACIONAL_BENFICA':dict(season='2024/2025',score='0-2',completion='2024-12-19',kickoff='2024-10-06',evidence='E6cf539bf7db64abd',rows=[('04a240ec3a2d9e77cceec3b782bc854f068b27feadd4e46ecf09168c44ccb3b9',8779,'2024-12-19','Nacional','Benfica'),('7a4a507f2e90976518ac3037c1d5d8f5ae433b521d1a6f17b4d4f05bd885272d',230,'2024-12-19','CD Nacional','Sport Lisboa e Benfica')]),
'LEIRIA_FEIRENSE':dict(season='2011/2012',score='0-4',completion=None,kickoff=None,evidence='E78919b2e402516bd',rows=[('187a370c18418bea735c0a27add3d826c1cc8e01ba6af2d2ee9524bfafed2cbd',5094,'2012-04-29','Leiria','Feirense')])}


def read(path):return json.loads(path.read_text())


def initialize(directory=PRIVATE,root=ROOT):
    if (directory/BASELINE).exists():return protect(directory,root)
    review.protect(directory,root);receipt=read(directory/'phase5_final_verification.json')
    for name,item in receipt['private_files_before_receipt'].items():
        if c.sha((directory/name).read_bytes())!=item['sha256']:raise ValueError('Phase5 private artifact changed: '+name)
    for name,digest in receipt['public_files'].items():
        if c.sha((root/name).read_bytes())!=digest:raise ValueError('Phase5 public artifact changed: '+name)
    files={str(p.relative_to(root)):c.sha(p.read_bytes())for p in directory.rglob('*')if p.is_file()}
    files.update({n:h for n,h in receipt['public_files'].items()if n!='PLANNING_LOG.md'})
    log=(root/'PLANNING_LOG.md').read_bytes()
    c.save(directory/BASELINE,c.encode(dict(approval='PHASE6_POLICY_ONLY',files=files,planning_log=dict(bytes=len(log),sha256=c.sha(log)))))
    return protect(directory,root)


def protect(directory=PRIVATE,root=ROOT):
    previous=review.protect(directory,root);saved=read(directory/BASELINE)
    if not saved['files']or saved['approval']!='PHASE6_POLICY_ONLY':raise ValueError('Empty/invalid Phase6 baseline')
    for name,digest in saved['files'].items():
        path=root/name
        if not path.resolve().is_relative_to(root.resolve())or c.sha(path.read_bytes())!=digest:raise ValueError('Frozen Phase2–5 entry changed: '+name)
    prefix=saved['planning_log'];log=(root/'PLANNING_LOG.md').read_bytes()
    if len(log)<prefix['bytes']or c.sha(log[:prefix['bytes']])!=prefix['sha256']:raise ValueError('Planning prefix changed')
    if subprocess.check_output(['git','branch','--show-current'],cwd=root).decode().strip()!='feature/data-collection':raise ValueError('Wrong branch')
    if subprocess.check_output(['git','diff','--cached','--name-only'],cwd=root):raise ValueError('Unexpected staged changes')
    return dict(previous=previous,phase2_5_entries=len(saved['files']))


def day(value):
    if not isinstance(value,str)or not re.fullmatch(r'\d{4}-\d{2}-\d{2}',value):raise ValueError('Canonical day required')
    return date.fromisoformat(value)


def primary(rows):
    if not rows or len({r['season']for r in rows})!=1:raise ValueError('Invalid group season')
    season=rows[0]['season'];year=int(season[:4])
    if season!=f'{year}/{year+1}'or not 1994<=year<=2025:raise ValueError('Outside approved dated scope')
    historical=[r for r in rows if r['source']==HIST_PATH]
    modern=[r for r in rows if r['source']==f'openfootball/europe/portugal/{year}-{(year+1)%100:02}_pt1.txt']
    if len(historical)+len(modern)!=len(rows)or len(historical)>1 or len(modern)>1:raise ValueError('Ambiguous source representations')
    if historical and historical[0]['provenance']['commit']!=HIST_PIN:raise ValueError('Historical revision differs')
    if modern and modern[0]['provenance']['commit']!=MODERN_PIN:raise ValueError('Modern revision differs')
    if year==2025:
        if historical or len(modern)!=1:raise ValueError('Latest-season source differs')
        return modern[0],'MODERN_2025_26_PRIMARY'
    if len(historical)!=1:raise ValueError('Unapproved historical primary-source gap')
    return historical[0],'HISTORICAL_CONTIGUOUS_BASELINE'


def case_kind(rows):
    ids={r['audit_id']for r in rows};matched=[k for k,v in SPECS.items()if ids&{r[0]for r in v['rows']}]
    if len(matched)>1:raise ValueError('Mixed exception groups')
    if not matched:return None
    kind=matched[0];spec=SPECS[kind]
    if ids!={r[0]for r in spec['rows']}:raise ValueError('Incomplete exception group')
    expected={row[0]:row[1:]for row in spec['rows']}
    for r in rows:
        if (r['source_line'],r['date'],r['home'],r['away'])!=tuple(expected[r['audit_id']])or r['season']!=spec['season']or r['FT']!=spec['score']:raise ValueError('Exception source binding changed')
    return kind


def decide(rows,historical_reviews,flags,references):
    """Pure provisional decision. Production build verifies originals, overlaps and evidence bytes."""
    selected,selection=primary(rows);ids=sorted(r['audit_id']for r in rows)
    if len(ids)!=len(set(ids)):raise ValueError('Duplicate source identity')
    for r in rows:
        day(r['date'])
        if not all(isinstance(r[k],str)and re.fullmatch(r'0|[1-9]\d*',r[k])for k in ('hg','ag'))or r['FT']!=f"{r['hg']}-{r['ag']}":raise ValueError('Invalid scored observation')
        if r['stage']not in ('HISTORICAL_P1_TIER1_STAGE_NOT_EXPLICIT','REGULAR_SEASON'):raise ValueError('Non-approved stage')
        if set(flags.get(r['audit_id'],[]))-KNOWN_FLAGS:raise ValueError('Unknown flag requires explicit review')
        h=historical_reviews.get(r['audit_id'])
        if h and h['original']!=r:raise ValueError('Historical binding differs')
        if r['annotation']:raise ValueError('Unreviewed source annotation requires explicit policy')
    kind=case_kind(rows);fixture_id=c.sha(c.encode(['Primeira Liga',selected['season'],selected['home'],selected['away']]))
    approved={k:selected[k]for k in ('date','home','away','FT','hg','ag')}
    chronology=dict(source_dates={r['audit_id']:r['date']for r in rows},source_date_proxy=selected['date'],scheduled_date=None,actual_kickoff_date=None,interruption_date=None,resumption_date=None,completion_date=None,administrative_decision_publication_date=None,administrative_finality_date=None,effective_result_availability_date=None,availability_day_verified=False,intraday_order_verified=False,date_interpretation='UNVERIFIED_ORDINARY_SOURCE_DATE_PROXY')
    disposition='COMPLETED_RESULT_CANDIDATE';policy='ORDINARY_SOURCE_CANDIDATE';hold_type=None
    reason='Structurally complete scored regular-season observation; no unresolved material conflict identified. Not historical certification, chronology eligibility or rights clearance.'
    eids=sorted({e for r in rows for e in historical_reviews.get(r['audit_id'],{}).get('assessment',{}).get('evidence_ids',[])})
    unresolved_admin=False;event=None
    if kind:
        spec=SPECS[kind];policy=kind;eids=sorted(set(eids)|{spec['evidence']})
        ref=references.get(spec['evidence'])
        if not ref:raise ValueError('Missing exception reference')
        if kind not in ('BELENENSES_BENFICA',)and ref['inspection']!='DIRECT_DOCUMENT':raise ValueError('Approved exception requires inspected documentary evidence')
        event=dict(original_score=spec['score'],original_kickoff=spec['kickoff'],documented_completion=spec['completion'],evidence_id=spec['evidence'])
        if kind=='BELENENSES_BENFICA':
            disposition='HOLD_OUT';hold_type='UNRESOLVED_ADMINISTRATIVE_FINALITY';unresolved_admin=True
            reason='Played but abnormally terminated event: recorded 0-7 is not verified administrative finality. Official FPF documents remain restricted; recognized final score, appeal/finality and availability not established. Not NOT_PLAYED.'
            chronology.update(actual_kickoff_date='2021-11-27',source_date_proxy=None,date_interpretation='UNRESOLVED_TERMINATION_AND_FINALITY')
        elif kind=='BENFICA_SALGUEIROS':
            disposition='HOLD_OUT';hold_type='UNRESOLVED_MATERIAL_COMPLETION_DATE'
            reason='CSV August20 and direct fan archive September6 conflict. Indexed contemporary preview is not directly inspected completion evidence. Neither date selected.'
            chronology.update(source_date_proxy=None,date_interpretation='UNRESOLVED_AUG20_VS_SEP06');event['alternative_reported_date']='1995-09-06'
        elif kind=='FEIRENSE_NACIONAL':
            approved['home']='Feirense'
            reason='Only the exact line4877/audit-ID interpretation Feirense<space>→Feirense is approved: one isolated whitespace defect, direct contemporary fixture identity and season pairing restoration. Original literal remains unchanged; no global trim.'
        elif kind=='LEIRIA_FEIRENSE':
            chronology['completion_date']='2012-04-29'
            reason='Direct contemporary report supports actual 0-4 with eight Leiria starters. Unusual participation is not an awarded score. First defensible availability not separately certified.'
            event['participation_context']='Eight Leiria starters during player strike; no score award established'
        else:
            approved['date']=spec['completion']
            chronology.update(source_date_proxy=None,actual_kickoff_date=spec['kickoff'],completion_date=spec['completion'],effective_result_availability_date=spec['completion'],availability_day_verified=True,date_interpretation='APPROVED_ACTUAL_COMPLETION_DAY_NO_INTRADAY_TIMESTAMP')
            if kind=='SANTA_PACOS':
                event['reported_scheduled_date']='2020-02-01'
                event['scheduled_date_verified']=False
                # Completion is directly established; protest finality is a separate unresolved consumer guard.
                unresolved_admin=True
                event['schedule_basis']='February1 historical source date; postponement/FPF details remain indexed only'
                reason='Direct completed-match reporting supports February2 and unchanged2-1; historical February1 remains preserved. No inspected evidence establishes a changed result. Candidate represents played result; known protest finality is not established, so chronology use remains blocked.'
            else:
                chronology.update(interruption_date=spec['kickoff'],resumption_date=spec['completion'])
                reason='Direct completion narrative supports unchanged score on approved completion day; interrupted kickoff preserved separately. No material contradictory final-result evidence identified; no invented publication timestamp.'
    else:
        contradictions=[historical_reviews[r['audit_id']]['assessment']['contradicted']for r in rows if r['audit_id']in historical_reviews and historical_reviews[r['audit_id']]['assessment']['contradicted']]
        if len({r['date']for r in rows})>1 or len({r['FT']for r in rows})>1 or contradictions:
            disposition='HOLD_OUT';hold_type='UNRESOLVED_MATERIAL_CONTRADICTION';reason='Unreviewed material score/date contradiction cannot silently pass source hierarchy.'
        if any('KNOWN_ABANDONMENT_REQUIRES_REVIEW'in flags.get(r['audit_id'],[])for r in rows):
            disposition='HOLD_OUT';hold_type='UNRESOLVED_ADMINISTRATIVE_FINALITY';unresolved_admin=True;reason='Known abnormal termination without an exact approved completed-result decision.'
        if any(r['home']!=r['home'].strip()or r['away']!=r['away'].strip()for r in rows):raise ValueError('Unapproved whitespace interpretation required')
    if any(e not in references for e in eids):raise ValueError('Unbound decision evidence')
    return dict(fixture_id=fixture_id,decision_id='PT-P6-'+policy+'-'+fixture_id,league='Primeira Liga',season=selected['season'],source_observation_ids=ids,selected_source_id=selected['audit_id'],comparator_source_ids=[i for i in ids if i!=selected['audit_id']],selection_reason=selection,disposition=disposition,hold_type=hold_type,policy=policy,reason=reason,approved_values=approved if disposition=='COMPLETED_RESULT_CANDIDATE'else None,chronology=chronology,unresolved_administration=unresolved_admin,event_context=event,evidence_ids=eids,source_bindings={r['audit_id']:deepcopy(r)for r in rows},historical_reviews={r['audit_id']:deepcopy(historical_reviews[r['audit_id']]['assessment'])for r in rows if r['audit_id']in historical_reviews},review_flags={r['audit_id']:deepcopy(flags.get(r['audit_id'],[]))for r in rows},identity_policy='Selected literal labels, one exact Feirense interpretation, exact season-bound overlap pairs only; no global aliases or legal-entity merges',structural_acceptance='POLICY_ACCOUNTED',historical_certification='NOT_DATASET_WIDE',administrative_finality='NOT_CERTIFIED'if not unresolved_admin else'KNOWN_UNRESOLVED',redistribution_permission='NOT_CLEARED',model_training_permission='NOT_CLEARED',model_training_suitability='NOT_CLEARED',supplement_approved=False)


def reconcile(rows,decisions):
    assigned=[i for d in decisions for i in d['source_observation_ids']]
    if len(assigned)!=len(rows)or len(set(assigned))!=len(assigned)or set(assigned)!={r['audit_id']for r in rows}:raise ValueError('Lost/duplicated original observation')
    if len({d['fixture_id']for d in decisions})!=len(decisions)or any(d['disposition']not in DISPOSITIONS for d in decisions):raise ValueError('Duplicate unique disposition or invalid category')
    for d in decisions:
        if d['selected_source_id']not in d['source_observation_ids']or set(d['source_bindings'])!=set(d['source_observation_ids']):raise ValueError('Incomplete selected/source bindings')
    return dict(source_observations=len(rows),unique_fixture_slots=len(decisions),overlap_representations=len(rows)-len(decisions),dispositions=dict(Counter(d['disposition']for d in decisions)),source_dispositions=dict(Counter(d['disposition']for d in decisions for _ in d['source_observation_ids'])))


def verify_correspondences(historical,modern,overlap):
    """Reconstruct exact directed pair joins, independently compare every saved paired fact."""
    by_season_h={s['assessment']['season']:s['records']for s in historical['seasons']}
    by_season_m={s['assessment']['season']:s['records']for s in modern['seasons']}
    result=[];expected_conflicts={tuple(sorted(x[0]for x in SPECS[k]['rows']))for k in ['SANTA_PACOS','SANTA_BENFICA']};actual_conflicts=set()
    for saved in overlap['seasons']:
        season=saved['season'];left=by_season_h[season];right=by_season_m[season]
        aliases={a['historical']:a['modern']for a in saved['mapping']}
        if len(aliases)!=len(saved['mapping'])or len(set(aliases.values()))!=len(aliases)or any(a['season']!=season for a in saved['mapping']):raise ValueError('Ambiguous or cross-season overlap labels')
        if set(aliases)!={r[k]for r in left for k in ['home','away']}or set(aliases.values())!={r[k]for r in right for k in ['home','away']}:raise ValueError('Incomplete label correspondence')
        lookup={(r['home'],r['away']):r for r in right}
        if len(lookup)!=len(right):raise ValueError('Duplicate comparator pairing')
        expected={x['historical_id']:x for x in saved['comparisons']};seen=set();pairs=[]
        for r in left:
            other=lookup[(aliases[r['home']],aliases[r['away']])];pair=expected[r['audit_id']]
            if other['audit_id']in seen or pair['modern_id']!=other['audit_id']:raise ValueError('Overlap binding mismatch')
            seen.add(other['audit_id'])
            if r['FT']!=other['FT']:raise ValueError('Unapproved cross-source score contradiction')
            ids=tuple(sorted([r['audit_id'],other['audit_id']]))
            if r['date']!=other['date']:actual_conflicts.add(ids)
            pairs.append(dict(source_ids=list(ids),correspondence_id='PT-P6-PAIR-'+c.sha(c.encode(ids))))
        if len(seen)!=len(right)or len(expected)!=len(left)or len(pairs)!=306:raise ValueError('Incomplete overlap fixture coverage')
        result.append(dict(season=season,status='APPROVED_EXACT_SEASON_FIXTURE_REPRESENTATION_ONLY',scope='Exact original fixture pairs in this season only; not global aliases or legal continuity',literal_label_links=deepcopy(saved['mapping']),pairs=pairs))
    if len(result)!=7 or sum(len(x['pairs'])for x in result)!=2142 or actual_conflicts!=expected_conflicts:raise ValueError('Overlap scope/conflicts changed')
    return result


def _eligible(expected,supplied,prediction_day):
    """Expected must come from a freshly verified policy registry, never caller-supplied trust."""
    if expected!=supplied:raise ValueError('Altered/incomplete decision or source binding')
    cutoff=day(prediction_day);chrono=expected['chronology'];completed=chrono['completion_date'];available=chrono['effective_result_availability_date']
    return (expected['disposition']=='COMPLETED_RESULT_CANDIDATE'and expected['unresolved_administration']is False and chrono['availability_day_verified']is True and completed is not None and available is not None and day(completed)<=day(available)<cutoff and expected['supplement_approved']is False)


def build(directory=PRIVATE,root=ROOT):
    protected=protect(directory,root);frozen=review.build(directory,root)
    for n,obj in frozen.items():
        if c.encode(obj)!=(directory/n).read_bytes():raise ValueError('Frozen Phase5 regeneration differs: '+n)
    h=read(directory/'phase4_historical_structure.json');m=read(directory/'phase4_modern_structure.json');o=read(directory/'phase4_overlap_reconciliation.json');queue=read(directory/'phase4_review_queue.json')
    rows=[r for season in h['seasons']+m['seasons']for r in season['records']];groups=review.group_rows(rows,o);correspondences=verify_correspondences(h,m,o)
    members=defaultdict(list)
    for row in rows:members[groups[row['audit_id']]].append(row)
    historical={r['original']['audit_id']:r for r in frozen['phase5_review_registry.json']['records']};flags={r['original']['audit_id']:r['categories']for r in queue['records']};refs={r['evidence_id']:r for r in frozen['phase5_documentary_evidence_index.json']['references']}
    expected_population=dict(source_observations=11406,historical=8958,modern=2448,overlap=2142,conditional_distinct=9264,represented_seasons=32)
    if any(queue['totals'][k]!=value for k,value in expected_population.items())or len(historical)!=392:raise ValueError('Approved review population changed')
    decisions=[decide(sorted(rs,key=lambda r:r['audit_id']),historical,flags,refs)for _,rs in sorted(members.items())]
    counts=reconcile(rows,decisions)
    if counts['unique_fixture_slots']!=9264 or counts['source_observations']!=11406:raise ValueError('Source/disposition reconciliation failed')
    exceptions=[d for d in decisions if d['policy']in SPECS or d['disposition']!='COMPLETED_RESULT_CANDIDATE']
    if {d['policy']for d in exceptions if d['policy']in SPECS}!=set(SPECS):raise ValueError('Missing approved special case')
    # Decision counts are measured, not forced to an assumed number of HOLD OUTs.
    source_records=[]
    for d in decisions:
        for i,r in d['source_bindings'].items():source_records.append(dict(original=deepcopy(r),fixture_id=d['fixture_id'],decision_id=d['decision_id'],source_role='SELECTED'if i==d['selected_source_id']else'COMPARATOR_RETAINED',disposition=d['disposition'],historical_review_id=i if i in historical else None,policy=d['policy']))
    source_records.sort(key=lambda r:r['original']['audit_id']);decisions.sort(key=lambda d:d['fixture_id'])
    # Recheck approved interpretation does not create identity collisions or lose pairings.
    pairs=set()
    for d in decisions:
        r=d['approved_values']or d['source_bindings'][d['selected_source_id']];key=(d['season'],r['home'],r['away'])
        if key in pairs:raise ValueError('Interpreted fixture identity collision')
        pairs.add(key)
    for season in {d['season']for d in decisions}:
        clubs={name for y,h,a in pairs if y==season for name in (h,a)};n=16 if 2006<=int(season[:4])<=2013 else 18
        if len(clubs)!=n or {(h,a)for y,h,a in pairs if y==season}!={(h,a)for h in clubs for a in clubs if h!=a}:raise ValueError('Incomplete interpreted season pairing coverage')
    season_counts={s:dict(Counter(d['disposition']for d in decisions if d['season']==s))for s in sorted({d['season']for d in decisions})}
    summary=dict(phase=6,league='Primeira Liga',**counts,historical_observations=8958,modern_observations=2448,represented_seasons=32,source_selection=dict(Counter(d['selection_reason']for d in decisions)),selected_observations=len(decisions),comparator_observations=sum(len(d['comparator_source_ids'])for d in decisions),hold_outs=[dict(fixture_id=d['fixture_id'],decision_id=d['decision_id'],policy=d['policy'],original=d['source_bindings'][d['selected_source_id']],reason=d['reason'])for d in decisions if d['disposition']=='HOLD_OUT'],not_played=counts['dispositions'].get('NOT_PLAYED',0),other_exclusions=0,season_dispositions=season_counts,phase5_source_confidence=read(directory/'phase5_confidence_summary.json')['source_confidence'],retained_review_observations=392,retained_flagged_observations=207,wide_round_contexts=18,reversal_contexts=13,exception_decisions=len(exceptions),completion_day_decisions=sum(d['chronology']['availability_day_verified']for d in decisions),eligible_day_gate_with_late_cutoff=sum(_eligible(d,d,'2026-11-24')for d in decisions),model_training_eligible=0,early_gap=dict(target='1990/91–2025/26',missing_seasons=['1990/1991','1991/1992','1992/1993','1993/1994'],expected_slots=1298,dated_observations=0,not_a_disposition=True),protected=protected,phase7_expected_screened_rows=counts['dispositions'].get('COMPLETED_RESULT_CANDIDATE',0),phase7_expected_archive_fixture_entries=counts['unique_fixture_slots'],phase7_expected_original_observation_references=counts['source_observations'],final_standardization_generated=False,limits='Candidate screening is not historical certification or chronological eligibility. All rights/model-training clearances unresolved; no application use.')
    outputs={NAMES[0]:dict(phase=6,records=source_records),NAMES[1]:dict(phase=6,records=decisions),NAMES[2]:dict(phase=6,hierarchy='Historical 1994/95–2024/25; modern2025/26; seven modern overlap seasons comparator-only; exact exceptions, no global corrections',rationale='Historical source provides31 complete season inventories and coherent repeated literals; all2142 comparator joins have matching scores and only the two explicitly resolved date disagreements. Modern source supplies the sole approved2025/26 inventory. This does not assert historical independence, global accuracy superiority or rights clearance.',overlap_correspondences=correspondences,global_aliases=[],selected_count=len(decisions),comparator_count=2142),NAMES[3]:dict(phase=6,records=exceptions,preserved_scheduling=frozen['phase5_scheduling_assessment.json'],preserved_phase5_issues=frozen['phase5_documentary_evidence_index.json']['issues'],special_case_specs=SPECS,unusual_score_decision_refs=[dict(fixture_id=d['fixture_id'],decision_id=d['decision_id'],disposition=d['disposition'],source_ids=d['source_observation_ids'],evidence_ids=d['evidence_ids'])for d in decisions if any('UNUSUAL_SCORE'in fs for fs in d['review_flags'].values())]),NAMES[4]:dict(phase=6,records=[dict(fixture_id=d['fixture_id'],decision_id=d['decision_id'],disposition=d['disposition'],chronology=d['chronology'],unresolved_administration=d['unresolved_administration'])for d in decisions],rule='Known completion and defensible availability both strictly before prediction day; same-day/future/unknown/restricted dispositions or unresolved administration reject. No intraday assumptions. CSV alone is insufficient. All training remains separately blocked pending rights and suitability clearance.'),NAMES[5]:summary}
    outputs[NAMES[6]]=dict(phase=6,input_hashes={n:c.sha((directory/n).read_bytes())for n in [BASELINE,'phase6_approval_receipt.json',*review.OUTPUTS,'phase5_research_inputs.json']},public_policy_sha256=c.sha((root/'scripts/decide_primeira_liga_policy.py').read_bytes()),outputs={n:dict(bytes=len(c.encode(obj)),sha256=c.sha(c.encode(obj)))for n,obj in outputs.items()},scope='Private processing metadata only; not final Phase7 CSV or complete audit archive')
    return outputs


class PredictionGate:
    """Load/compare all regenerated policy bytes; retain detached expected decisions."""
    def __init__(self,directory=PRIVATE,root=ROOT):
        expected=build(directory,root)
        for n,obj in expected.items():
            if not(directory/n).exists()or(directory/n).read_bytes()!=c.encode(obj):raise ValueError('Altered/missing policy registry: '+n)
        self._expected={d['fixture_id']:deepcopy(d)for d in expected[NAMES[1]]['records']}

    def eligible_for_prediction(self,decision,prediction_day):
        if decision.get('fixture_id')not in self._expected:raise ValueError('Unknown fixture decision')
        return _eligible(self._expected[decision['fixture_id']],decision,prediction_day)

    def training_allowed(self,decision,prediction_day):
        return self.eligible_for_prediction(decision,prediction_day)and decision['model_training_permission']=='CLEARED'and decision['model_training_suitability']=='CLEARED'


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--init',action='store_true');parser.add_argument('--output-directory',type=Path,default=PRIVATE);args=parser.parse_args()
    if args.init:initialize()
    outputs=build();args.output_directory.mkdir(exist_ok=True,parents=True)
    for n,obj in outputs.items():c.keep(args.output_directory/n,c.encode(obj))
    print(json.dumps(outputs[NAMES[5]],indent=2))

if __name__=='__main__':main()
