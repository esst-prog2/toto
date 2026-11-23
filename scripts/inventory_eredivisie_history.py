"""Phase 3 source-preserving 36-season inventory, no screening or source preference."""
from collections import Counter,defaultdict
from copy import deepcopy
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from scripts import collect_eredivisie_history as acquisition
from scripts import validate_eredivisie_feasibility as feasibility
from scripts import verify_eredivisie_feasibility as independent

ROOT,PRIVATE,c=acquisition.ROOT,acquisition.PRIVATE,acquisition.c
NAMES=('phase3_historical_inventory.json','phase3_modern_inventory.json','phase3_coverage_matrix.json','phase3_overlap_registry.json','phase3_review_candidates.json')


def independent_check(historical,modern,coverage,directory):
    with TemporaryDirectory(prefix='eredivisie-phase3-independent-') as temporary:
        temp=Path(temporary);wrapper=dict(historical=historical,modern=modern)
        (temp/'feasibility_assessment.json').write_bytes(c.encode(wrapper));(temp/'coverage_inventory.json').write_bytes(c.encode(coverage))
        for receipt in [historical['receipt'],*[x['receipt'] for x in modern]]:
            target=temp/receipt['path'];target.parent.mkdir(parents=True,exist_ok=True);target.symlink_to((directory/receipt['path']).resolve())
        return independent.reconcile(temp)


def overlap_for_season(historical,modern):
    return dict(exact=feasibility.overlap(historical,modern),conditional=feasibility.identity_overlap(historical,modern))


def coverage_row(year,historical,modern):
    label=f'{year}/{year+1}';h=historical.get(year);m=modern.get(year)
    return dict(season=label,expected_clubs=18,expected_regular_slots=306,historical=h['assessment'] if h else None,modern=m['assessment'] if m else None,source_repositories=([c.HIST] if h else [])+([c.MODERN] if m else []),coverage_status='BOTH_SOURCES' if h and m else 'HISTORICAL_ONLY' if h else 'MODERN_ONLY' if m else 'NO_SOURCE',warning='Source observations are separate; do not add overlap as independent matches. Completeness is not historical certification.')


def review_queue(historical,modern,overlaps,context):
    lookup={r['audit_id']:r for s in historical+modern for r in s['records']};queue={}
    if len(lookup)!=sum(len(s['records']) for s in historical+modern):raise ValueError('Duplicate source audit ID')
    def flag(key,category):
        if key not in lookup:raise ValueError('Review reference not bound to source')
        entry=queue.setdefault(key,dict(original=deepcopy(lookup[key]),categories=[]))
        if category not in entry['categories']:entry['categories'].append(category)
    for source in historical+modern:
        a=source['assessment']
        for wide in a['wide_rounds']:
            for key in wide['fixture_ids']:flag(key,'WIDE_ROUND')
        for pair in a['source_order_reversals']:
            flag(pair['previous_id'],'SOURCE_ORDER_REVERSAL');flag(pair['current_id'],'SOURCE_ORDER_REVERSAL')
        for unusual in a['unusual_scores']:flag(unusual['id'],'UNUSUAL_SCORE')
        for annotation in a['annotations']:flag(annotation['id'],'SOURCE_ANNOTATION')
        for invalid in a['invalid']:flag(invalid['id'],'STRUCTURAL_REVIEW')
        for r in source['records']:
            if r['FT'] is None:flag(r['audit_id'],'SOURCE_UNSCORED')
    for overlap in overlaps:
        for pair in overlap['conditional']['comparisons']:
            for field,category in [('date_equal','CROSS_SOURCE_DATE_DISAGREEMENT'),('score_equal','CROSS_SOURCE_SCORE_DISAGREEMENT')]:
                if not pair[field]:
                    flag(pair['historical_id'],category);flag(pair['modern_id'],category)
    for item in context['exceptions']:
        if 'source_observation' in item:
            row=item['source_observation'];key=row['audit_id']
            if lookup.get(key)!=row:raise ValueError('Frozen documentary source binding differs')
            flag(key,item.get('kind','KNOWN_INTERRUPTION_CONTEXT'))
        elif 'original_comparison' in item:
            pair=item['original_comparison']
            for key in ['historical_id','modern_id']:flag(pair[key],item['kind'])
    entries=sorted(queue.values(),key=lambda x:(x['original']['source'],x['original']['source_line']))
    return dict(distinct_source_observations=len(entries),categories=dict(Counter(k for r in entries for k in r['categories'])),records=entries,warning='Deduplicated per-source queue, not a count of distinct real-world matches; categories overlap; no policy assigned')


def build(directory=PRIVATE,root=ROOT):
    protected=acquisition.protect(directory,root);old=c.verify_originals(directory);new=acquisition.verify_originals(directory)
    # Reproduce frozen Phase 2 before extending its assessment scope.
    for name,obj in feasibility.build(directory,root).items():
        if (directory/name).read_bytes()!=c.encode(obj):raise ValueError('Frozen Phase 2 assessment differs: '+name)
    if (directory/'independent_reconciliation.json').read_bytes()!=c.encode(independent.reconcile(directory)):raise ValueError('Frozen Phase 2 independent results differ')
    hr=next(r for r in old['files'] if r['repository']==c.HIST);all_historical=feasibility.parse_csv((directory/hr['path']).read_bytes(),hr);groups=defaultdict(list)
    for r in all_historical:groups[int(r['season'][:4])].append(r)
    if set(groups)!=set(range(1956,2025)):raise ValueError('Historical source coverage changed')
    historical=[dict(receipt=hr,records=groups[y],assessment=feasibility.assess(groups[y],y)) for y in range(1990,2025)]
    modern_receipts=[r for r in old['files']+new['files'] if r['repository']==c.MODERN]
    if len(modern_receipts)!=8 or {r['season'] for r in modern_receipts}!={f'{y}/{y+1}' for y in range(2018,2026)}:raise ValueError('Modern source file inventory differs')
    modern=[]
    for receipt in sorted(modern_receipts,key=lambda r:r['season']):
        year=int(receipt['season'][:4]);rows,notes=feasibility.parse_text((directory/receipt['path']).read_bytes(),year,receipt)
        modern.append(dict(receipt=receipt,records=rows,assessment=feasibility.assess(rows,year),notes=notes))
    hmap={int(s['assessment']['season'][:4]):s for s in historical};mmap={int(s['assessment']['season'][:4]):s for s in modern}
    matrix=[coverage_row(y,hmap,mmap) for y in range(1990,2026)]
    overlaps=[dict(season=f'{y}/{y+1}',**overlap_for_season(hmap[y]['records'],mmap[y]['records'])) for y in range(2018,2025)]
    context=json.loads((directory/'phase2_documentary_context.json').read_text());queue=review_queue(historical,modern,overlaps,context)
    h2019=hmap[2019]['assessment'];m2019=mmap[2019]['assessment'];paired=next(o for o in overlaps if o['season']=='2019/2020')['conditional'];matched_ids={r['modern_id'] for r in paired['comparisons']};unmatched=[r for r in mmap[2019]['records'] if r['audit_id'] not in matched_ids]
    cancellations=dict(historical_scored=h2019['scored'],historical_absent_pairs=len(h2019['missing_pairings']),modern_observed=m2019['observed'],modern_scored=m2019['scored'],modern_source_cancelled=m2019['explicitly_cancelled'],modern_absent_pairs=len(m2019['missing_pairings']),matched_scored=len(paired['comparisons']),unmatched_modern=len(unmatched),all_unmatched_explicitly_cancelled=all(r['FT'] is None and r['annotation']=='[cancelled]' for r in unmatched),policy='No invented scores, no blanket annulment, no screening; source absence and explicit cancellation separate')
    inventory69=[feasibility.assess(rows,y) for y,rows in sorted(groups.items())];independent_result=independent_check(dict(receipt=hr,total_records=len(all_historical),samples=historical),modern,dict(seasons=inventory69),directory)
    label_occurrences=defaultdict(list)
    for source in historical+modern:
        for label in source['assessment']['team_labels']:label_occurrences[label].append(dict(source=source['receipt']['path'],season=source['assessment']['season']))
    identity=dict(literal_labels=sorted(label_occurrences),occurrences=dict(sorted(label_occurrences.items())),risk_labels=[label for label in sorted(label_occurrences) if any(s.casefold() in label.casefold() for s in ['ne.c','nec','rkc','nac','zwolle','den haag','dordrecht','svv','jong','vitesse'])],reserve_labels=sorted({n for source in historical+modern for n in source['assessment']['reserve_labels']}),policy='Original labels only; season-local comparison hypotheses are not global aliases or predecessor/successor mergers')
    summary=dict(target_seasons=36,historical_seasons=35,historical_target_observations=sum(len(s['records']) for s in historical),historical_all_source_rows=len(all_historical),historical_all_source_seasons=len(groups),modern_seasons=8,modern_observations=sum(len(s['records']) for s in modern),modern_scored=sum(s['assessment']['scored'] for s in modern),modern_unscored=sum(s['assessment']['unscored'] for s in modern),historical_modern_scored_comparisons=sum(o['conditional']['comparison_pairs'] for o in overlaps),score_disagreements=sum(not r['score_equal'] for o in overlaps for r in o['conditional']['comparisons']),date_disagreements=sum(not r['date_equal'] for o in overlaps for r in o['conditional']['comparisons']),unmatched_historical_in_overlaps=sum(len(o['conditional']['unmatched_historical_ids']) for o in overlaps),modern_wide_rounds=sum(len(s['assessment']['wide_rounds']) for s in modern),modern_wide_members=sum(len(w['fixture_ids']) for s in modern for w in s['assessment']['wide_rounds']),source_queue=queue['distinct_source_observations'],no_source_preference=True,no_standardized_or_accepted_count=True)
    return {NAMES[0]:dict(phase=3,receipt=hr,columns=list(feasibility.CSV_COLUMNS),all_source_season_metadata=inventory69,seasons=historical,protected=protected),NAMES[1]:dict(phase=3,seasons=modern,protected=protected),NAMES[2]:dict(phase=3,summary=summary,seasons=matrix,cancellation_2019_20=cancellations,independent_reconciliation=independent_result,rights=c.RIGHTS,historical_certification=False),NAMES[3]:dict(phase=3,overlaps=overlaps,nonoverlap_2025_26='Historical CSV has no 2025/26 rows; no supplemental result inserted',upstream_independence='UNESTABLISHED'),NAMES[4]:dict(phase=3,queue=queue,documentary_context=context,identity=identity,chronological_rule='Source date is not independently verified availability; no eligibility decisions in Phase 3',rights=c.RIGHTS)}


if __name__=='__main__':
    outputs=build()
    for name,obj in outputs.items():
        raw=c.encode(obj);target=PRIVATE/name
        if target.exists():
            if target.read_bytes()!=raw:raise ValueError('Inventory changed: '+name)
        else:c.save(target,raw)
    print(json.dumps(outputs[NAMES[2]]['summary'],indent=2))
