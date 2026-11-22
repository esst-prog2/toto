"""Offline Phase 3 inventory only; no corrections, policies or standardization."""
from collections import Counter, defaultdict
import json
from pathlib import Path
import tempfile
import unicodedata
from scripts import collect_ligue2_history as c
from scripts import validate_ligue2_feasibility as feasibility
from scripts import verify_ligue2_feasibility as independent

PRIVATE = c.PRIVATE
OUTPUT = 'phase3_inventory.json'


def receipts(directory):
    prior=c.base.verify_originals(directory);new=c.verify_originals(directory)
    records=[r for r in prior['files']+new['files'] if r['repository']==c.REPO and 2014<=int(r['season'][:4])<=2024]
    if len(records)!=11 or len({r['season'] for r in records})!=11:raise ValueError('Modern season inventory differs')
    return sorted(records,key=lambda r:r['season'])


def summarize(sources):
    counts=Counter();groups=defaultdict(list);queue={}
    for source in sources:
        a=source['assessment'];rows=source['records'];byline={r['source_line']:r for r in rows}
        if len(byline)!=len(rows):raise ValueError('Duplicate source-line bindings')
        counts.update(dict(observed=a['observed'],scored=a['scored'],unscored=a['unscored'],other_stages=a['other_stage_observations'],expected=a['expected_scheduled']))
        for t in a['team_names']:
            key=unicodedata.normalize('NFC',t).casefold();groups[key].append(dict(label=t,season=a['season']))
        def flag(r,category):
            k=r['audit_id'];item=queue.setdefault(k,dict(audit_id=k,source=r['source'],source_sha256=r['source_sha256'],source_line=r['source_line'],season=r['season'],date=r['date'],home=r['home'],away=r['away'],FT=r['FT'],annotation=r['annotation'],categories=[]))
            if category not in item['categories']:item['categories'].append(category)
        for w in a['wide_rounds']:
            for member in w['fixtures']:flag(byline[member['source_line']],'WIDE_ROUND')
        for r in rows:
            if r['FT'] is None:flag(r,'SOURCE_CANCELLED' if 'cancelled' in r['annotation'].lower() else 'UNSCORED_UNEXPLAINED')
            if r['annotation'] and 'cancelled' not in r['annotation'].lower():flag(r,'SOURCE_ANNOTATION')
            if 'Bordeaux' in r['home'] and 'Rodez' in r['away'] and r['season']=='2022/2023':flag(r,'BORDEAUX_RODEZ_ADMINISTRATIVE_REVIEW')
        for unusual in a['unusual_scores']:flag(byline[unusual['line']],'UNUSUAL_SCORE')
    members=sorted(queue.values(),key=lambda r:(r['season'],r['source_line']))
    return dict(totals=dict(counts),wide_rounds=sum(len(s['assessment']['wide_rounds']) for s in sources),
                wide_round_members=sum(len(w['fixtures']) for s in sources for w in s['assessment']['wide_rounds']),
                deduplicated_review_candidates=len(members),review_category_members=dict(Counter(k for r in members for k in r['categories'])),review_candidates=members,
                literal_label_changes=[dict(key=k,occurrences=rs) for k,rs in sorted(groups.items()) if len({r['label'] for r in rs})>1],
                identity_policy='Diagnostics only; no global aliases, club mergers or reserve-side assumptions')


def independent_check(sources,directory):
    # Separate parser, temporary wrapper and read-only symlinks; original bytes never copied over.
    with tempfile.TemporaryDirectory(prefix='ligue2-phase3-raw-') as t:
        temp=Path(t);(temp/'feasibility_assessment.json').write_bytes(c.base.encode(dict(sources=sources)))
        for s in sources:
            p=temp/s['receipt']['path'];p.parent.mkdir(parents=True,exist_ok=True);p.symlink_to((directory/s['receipt']['path']).resolve())
        return independent.reconcile(temp)


def build(directory=PRIVATE,root=c.ROOT):
    protected=c.protect(directory,root);sources=[]
    frozen=json.loads((directory/feasibility.OUTPUT).read_text())
    for receipt in receipts(directory):
        raw=(directory/receipt['path']).read_bytes();year=int(receipt['season'][:4]);rows,notes=feasibility.parse_text(raw,year)
        for r in rows:
            r.update(source=receipt['path'],source_sha256=receipt['sha256'],raw_line_sha256=c.base.sha(r['raw_record'].encode('utf-8')),
                     audit_id=c.base.sha(c.base.encode([receipt['sha256'],r['source_line'],None,None])))
        result=dict(receipt=receipt,assessment=feasibility.assess(rows,year),notes=notes,records=rows)
        prior=next((s for s in frozen['sources'] if s['receipt']['path']==receipt['path']),None)
        if prior is not None and result!=prior:raise ValueError('Reused Phase 2 assessment differs')
        sources.append(result)
    snapshot=next(s for s in frozen['sources'] if s['receipt']['season']=='2025/2026')
    historical=next(s for s in frozen['sources'] if s['receipt']['repository']=='rsssf')
    return dict(phase=3,scope='2014/15–2024/25 modern source inventory only',canonical_league='Ligue 2',protected=protected,
                sources=sources,summary=summarize(sources),independent_raw_reconciliation=independent_check(sources,directory),
                incomplete_2025_26=dict(receipt=snapshot['receipt'],assessment=snapshot['assessment'],excluded_from_modern_totals=True),
                rsssf_1998_99=dict(receipt=historical['receipt'],assessment=historical['assessment'],interpretation='UNRESOLVED; preserve frozen Phase 2 diagnostics, no mapping/date/score decision'),
                documentary_context=json.loads((directory/'phase2_documentary_context.json').read_text()),
                historical_gap='All 24 seasons 1990/91–2013/14 lack an approved complete primary source; 2025/26 incomplete snapshot remains separate',
                policy='No corrections, effective-date changes, exclusions, HOLD OUT decisions, standardization, application integration or training',rights=c.base.RIGHTS)


if __name__=='__main__':
    result=build();content=c.base.encode(result);target=PRIVATE/OUTPUT
    if target.exists():
        if target.read_bytes()!=content:raise ValueError('Inventory changed; inspect rather than overwrite')
    else:c.base.save(target,content)
    print(json.dumps({k:v for k,v in result['summary'].items() if k!='review_candidates'},ensure_ascii=False,indent=2))
