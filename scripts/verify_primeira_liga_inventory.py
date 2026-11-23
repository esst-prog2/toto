"""Independent Phase 3 source/inventory reconciliation using Phase 2 raw parsers."""
from collections import Counter,defaultdict
from datetime import date
import json
from scripts import collect_primeira_liga_history as acquisition
from scripts import validate_primeira_liga_feasibility as earlier
c=acquisition.c


def verify(directory=acquisition.PRIVATE):
    h=json.loads((directory/'phase3_historical_inventory.json').read_text());m=json.loads((directory/'phase3_modern_inventory.json').read_text());o=json.loads((directory/'phase3_overlap_registry.json').read_text());coverage=json.loads((directory/'phase3_coverage_matrix.json').read_text());q=json.loads((directory/'phase3_review_candidates.json').read_text());f=json.loads((directory/'phase3_feirense_diagnostic.json').read_text())
    if not h['seasons'] or not m['seasons']:raise ValueError('Empty source inventory')
    rec=h['seasons'][0]['receipt'];raw=(directory/rec['path']).read_bytes();all_h=earlier.parse_csv(raw,rec);grouped=defaultdict(list)
    for r in all_h:grouped[r['season']].append(r)
    if set(grouped)!={s['assessment']['season'] for s in h['seasons']}:raise ValueError('Historical season inventory differs')
    for s in h['seasons']:
        if s['records']!=grouped[s['assessment']['season']]:raise ValueError('Historical original fields/source binding differs')
    for s in m['seasons']:
        rec=s['receipt'];rs,notes=earlier.parse_text((directory/rec['path']).read_bytes(),int(rec['season'][:4]),rec)
        if rs!=s['records'] or notes!=s['notes']:raise ValueError('Modern independent original/line parsing differs')
    lookup={r['audit_id']:r for s in h['seasons']+m['seasons'] for r in s['records']};categories=defaultdict(set);wide=[];reversals=[]
    for s in h['seasons']+m['seasons']:
        rows=s['records'];a=s['assessment'];names={r[k] for r in rows for k in ('home','away')};pairs=defaultdict(list);rounds=defaultdict(list)
        for r in rows:
            pairs[r['home'],r['away']].append(r)
            if r['round'] is not None:rounds[str(r['round'])].append(r)
            if any(r[k]!=r[k].strip() or not r[k] or '\ufffd' in r[k] for k in ('home','away')) or r['home']==r['away'] or r.get('field_issues'):categories[r['audit_id']].add('SOURCE_FIELD_OR_LABEL')
            if r['hg'] is None:categories[r['audit_id']].add('UNSCORED')
            elif max(int(r['hg']),int(r['ag']))>=7 or int(r['hg'])+int(r['ag'])>=10:categories[r['audit_id']].add('UNUSUAL_SCORE')
            if r['annotation']:categories[r['audit_id']].add('SOURCE_ANNOTATION')
        if (a['observed'],a['scored'],a['unscored'],a['clubs'],a['directed_pairs'])!=(len(rows),sum(r['FT'] is not None for r in rows),sum(r['FT'] is None for r in rows),len(names),len(pairs)):raise ValueError('Independent source counts differ')
        missing={(x,y) for x in names for y in names if x!=y and (x,y) not in pairs}
        if set(map(tuple,a['missing_pairings']))!=missing:raise ValueError('Missing pair inventory differs')
        if {(x['home'],x['away']) for x in a['duplicate_pairings']}!={k for k,rs in pairs.items() if len(rs)>1}:raise ValueError('Duplicate inventory differs')
        actual_wide=[]
        for rnd,rs in rounds.items():
            first=min(r['date'] for r in rs);last=max(r['date'] for r in rs);span=(date.fromisoformat(last)-date.fromisoformat(first)).days
            if span>14:
                actual_wide.append((rnd,first,last,span,tuple(r['audit_id'] for r in rs)))
                for r in rs:categories[r['audit_id']].add('WIDE_ROUND')
        if sorted(actual_wide)!=sorted((x['round'],x['first_date'],x['last_date'],x['span_days'],tuple(x['fixture_ids'])) for x in a['wide_rounds']):raise ValueError('Wide-round binding differs')
        wide+=actual_wide
        actual_rev=[(x['audit_id'],y['audit_id']) for x,y in zip(rows,rows[1:]) if x['date']>y['date']]
        if actual_rev!=[(x['previous_id'],x['current_id']) for x in a['source_order_reversals']]:raise ValueError('Source order reversal differs')
        for x,y in actual_rev:categories[x].add('SOURCE_ORDER_REVERSAL');categories[y].add('SOURCE_ORDER_REVERSAL')
        reversals+=actual_rev
    conflicts=[]
    for season in o['seasons']:
        mapping={x['historical']:x['modern'] for x in season['mapping']}
        if len(mapping)!=len(season['mapping']) or len(set(mapping.values()))!=len(mapping):raise ValueError('Nonbijective diagnostic mapping')
        seen_h=set();seen_m=set()
        for p in season['comparisons']:
            hr,mr=lookup[p['historical_id']],lookup[p['modern_id']]
            if hr['season']!=mr['season'] or hr['season']!=season['season'] or (mapping[hr['home']],mapping[hr['away']])!=(mr['home'],mr['away']):raise ValueError('Cross-season/identity mismatch')
            if p['historical_id'] in seen_h or p['modern_id'] in seen_m:raise ValueError('Overlap duplication')
            seen_h.add(p['historical_id']);seen_m.add(p['modern_id'])
            if p['date_equal']!=(hr['date']==mr['date']) or p['score_equal']!=(hr['FT']==mr['FT']):raise ValueError('Hidden overlap conflict')
            if not p['date_equal'] or not p['score_equal']:
                conflicts.append((p['historical_id'],p['modern_id']))
                categories[p['historical_id']].add('SOURCE_DISAGREEMENT');categories[p['modern_id']].add('SOURCE_DISAGREEMENT')
        if len(season['comparisons'])!=season['comparison_pairs']:raise ValueError('Overlap count differs')
        hs={r['audit_id'] for r in all_h if r['season']==season['season']};ms={r['audit_id'] for s in m['seasons'] if s['assessment']['season']==season['season'] for r in s['records']}
        if hs-seen_h!=set(season['unmatched_historical_ids']) or ms-seen_m!=set(season['unmatched_modern_ids']):raise ValueError('Unmatched inventory differs')
    if set(conflicts)!={(x['historical_id'],x['modern_id']) for x in o['conflicts']}:raise ValueError('Conflict registry differs')
    for r in q['belenenses']['originals']:
        if r!=lookup.get(r['audit_id']) or r['date']!='2021-11-27' or r['FT']!='0-7':raise ValueError('Belenenses exception altered')
        categories[r['audit_id']].add('KNOWN_ABANDONMENT_REQUIRES_REVIEW')
    if {r['original']['audit_id']:set(r['categories']) for r in q['records']}!=dict(categories):raise ValueError('Deduplicated review queue differs')
    if q['distinct_flagged_source_observations']!=len(categories) or q['category_counts']!=dict(Counter(k for vals in categories.values() for k in vals)):raise ValueError('Queue count mismatch')
    original=f['original_observation'];rs=[dict(r) for r in all_h if r['season']=='2011/2012']
    if original!=lookup.get(original['audit_id']) or original['home']!='Feirense ' or original['date']!='2011-08-14' or original['away']!='Nacional':raise ValueError('Whitespace selector changed')
    for r in rs:
        if r['audit_id']==original['audit_id']:r['home']='Feirense'
    names={r[k] for r in rs for k in ('home','away')};pairs=Counter((r['home'],r['away']) for r in rs)
    if len(names)!=16 or len(pairs)!=240 or any(n!=1 for n in pairs.values()):raise ValueError('Whitespace-only reconciliation not lossless')
    for row in coverage['seasons']:
        label=row['season'];hn=sum(len(s['records']) for s in h['seasons'] if s['assessment']['season']==label);mn=sum(len(s['records']) for s in m['seasons'] if s['assessment']['season']==label);on=sum(s['comparison_pairs'] for s in o['seasons'] if s['season']==label)
        if (row['historical_observations'],row['modern_observations'],row['matched_overlap_pairs'],row['conditional_distinct_slots'])!=(hn,mn,on,hn+mn-on):raise ValueError('Coverage row differs')
    if len(coverage['seasons'])!=36 or len({x['season'] for x in coverage['seasons']})!=36:raise ValueError('Coverage scope differs')
    return dict(phase=3,independent_phase2_parsers=True,historical_records=len(all_h),modern_records=sum(len(s['records']) for s in m['seasons']),overlap_pairs=sum(s['comparison_pairs'] for s in o['seasons']),conflicts=len(conflicts),wide_rounds=len(wide),source_reversal_pairs=len(reversals),deduplicated_review_observations=len(categories),coverage=coverage['totals'],source_fields_unchanged=True,no_historical_certification=True)


if __name__=='__main__':
    result=verify();c.keep(acquisition.PRIVATE/'phase3_independent_reconciliation.json',c.encode(result));print(json.dumps(result,indent=2))
