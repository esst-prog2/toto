"""Offline Phase 3 source inventory; no standardized data or factual corrections.

Reports missing/unparseable seasons without forcing totals. --check is read-only.
"""
import argparse
from collections import Counter,defaultdict
from datetime import date
import json
import re

from scripts.collect_la_liga_feasibility import ROOT,PRIVATE,sha
from scripts.collect_la_liga_history import MANIFEST,REPO,PIN,TREE,checked_tree,plan,protect,verify_file,save
from scripts.validate_la_liga_feasibility import historical,hist_season,text_results,assess,encode,HIST

OUTPUT='phase3_inventory.json'


def parse_text(raw,year):
    """Reuse feasibility grammar, explicitly resolve omitted COVID July years.

    Only a parsing view changes; source bytes and source line numbers stay intact.
    Season 2019/20 can continue into July/August 2020 after its stated 2020 dates.
    """
    text=raw.decode('utf-8-sig');lines=text.splitlines();previous=None
    for i,line in enumerate(lines):
        m=re.fullmatch(r'(\s*)(Mon|Tue|Wed|Thu|Fri|Sat|Sun) ([A-Z][a-z]{2}) (\d{1,2})(?: (\d{4}))?\s*',line)
        if not m:continue
        from datetime import datetime
        month=datetime.strptime(m[3],'%b').month
        if m[5]:resolved=int(m[5])
        else:
            resolved=year+(month<7 or (year==2019 and previous==2020 and month in (7,8)))
            lines[i]=f'{m[1]}{m[2]} {m[3]} {m[4]} {resolved}'
        previous=resolved
    return text_results('\n'.join(lines).encode('utf-8'),year)


def inventory_rows(rows,year,n,notes=()):
    report=assess(rows,year,n)
    if year==2019:
        # assess() uses an ordinary June cutoff: expose it separately from the
        # known extended-season calendar rather than rewriting Phase 2 behavior.
        extended=[];remaining=[]
        for r in rows:
            try:
                d=date.fromisoformat(r['date'])
                if date(2020,7,1)<=d<=date(2020,8,31):extended.append(r['source_line'])
                elif r['source_line'] in report['date_error_lines']:remaining.append(r['source_line'])
            except (ValueError,TypeError):remaining.append(r['source_line'])
        report['ordinary_cutoff_date_error_lines']=report['date_error_lines']
        report['date_error_lines']=remaining
        report['documented_extended_calendar_lines']=extended
        report['calendar_rule']='2019/2020 explicitly allows COVID-delayed July/August 2020; no fixture date corrected'
        if not remaining:report['issues']=[i for i in report['issues'] if i!='date_errors']
    weekdays=[n for n in notes if n['kind']=='weekday_mismatch']
    if weekdays:report['issues'].append('weekday_mismatch')
    report['weekday_mismatches']=weekdays
    report['status']='INVENTORY_COMPLETE' if not report['issues'] else 'REVIEW'
    groups=defaultdict(list)
    for r in rows:groups[r['stage']].append(r)
    wide=[]
    for stage,rs in groups.items():
        if stage=='league':continue
        try:
            ds=sorted(r['date'] for r in rs)
            if (date.fromisoformat(ds[-1])-date.fromisoformat(ds[0])).days>=14:
                wide.append(dict(stage=stage,first=ds[0],last=ds[-1],lines=[r['source_line'] for r in rs]))
        except (TypeError,ValueError):pass
    report['wide_round_spans']=wide
    report['round_headers']=sum(n['kind']=='round_header' for n in notes)
    report['distinct_round_labels']=len(groups) if notes else None
    report['source_notes']=list(notes)
    return report


def build(directory=PRIVATE):
    protection=protect(directory)
    base=json.loads((directory/'acquisition.json').read_text())
    prior=json.loads((directory/'feasibility_diagnostics.json').read_text())
    tree=checked_tree((directory/TREE).read_bytes())
    manifest=json.loads((directory/MANIFEST).read_text())
    receipts={r['path']:r for r in base['files']}
    receipts.update({r['path']:r for r in manifest['additional_files']})
    for name,r in receipts.items():
        b=(directory/name).read_bytes()
        if sha(b)!=r['sha256'] or len(b)!=r['bytes']:raise ValueError('Source checksum changed: '+name)
        if name.startswith(REPO+'/') and r.get('format') in ('Football.TXT','txt'):
            verify_file(b,tree[name.removeprefix(REPO+'/')])
    old=historical((directory/HIST).read_bytes())
    out=[];missing=[];candidates=[]
    for year in range(1990,2026):
        season=f'{year}/{year+1}';path=HIST if year<=2011 else f'{REPO}/{year}-{(year+1)%100:02}/1-liga.txt'
        header=dict(season=season,file=path,expected=(22 if year in (1995,1996) else 20)*(21 if year in (1995,1996) else 19),source='engsoccerdata' if year<=2011 else 'OpenFootball')
        if not (directory/path).exists():
            missing.append(path);out.append(dict(header,status='MISSING',records=None,scored=None));continue
        try:
            if year<=2011:
                rows=hist_season(old,year);notes=[]
            else:rows,notes=parse_text((directory/path).read_bytes(),year)
            r=inventory_rows(rows,year,22 if year in (1995,1996) else 20,notes)
            r.update(file=path,source=header['source'],source_sha256=receipts[path]['sha256'],
                     source_commit=receipts[path]['commit'],encoding='UTF-8 strict',
                     replacement_character_present='\ufffd' in (directory/path).read_bytes().decode('utf-8-sig'))
            if r['replacement_character_present']:r['issues'].append('unicode_replacement_character');r['status']='REVIEW'
            out.append(r)
            for span in r['wide_round_spans']:candidates.append(dict(season=season,file=path,kind='WIDE_ROUND_SPAN',details=span))
            for event in r['annotations']:candidates.append(dict(season=season,file=path,kind='SOURCE_ANNOTATION',details=event))
            for issue in r['issues']:candidates.append(dict(season=season,file=path,kind='INVENTORY_ISSUE',details=issue))
        except (ValueError,TypeError,KeyError) as exc:
            out.append(dict(header,status='PARSE_REVIEW',records=None,scored=None,error=str(exc)))
            candidates.append(dict(season=season,file=path,kind='PARSER_REVIEW',details=str(exc)))
    # All historical non-league rows remain a separate diagnostic, never selected.
    phases=[r for r in old if r['round']=='phase2']
    outside=[r for r in old if int(r['Season'])<1990 or int(r['Season'])>2011 or r['tier']!='1' or r['round']!='league']
    covered=[r for r in out if r['records'] is not None]
    # Verify exact retention of each Phase 2 candidate with source physical lines.
    for c in prior['round_spans_at_least_14_days']:
        match=next(r for r in out if r['season']==c['season'])
        found=[x for x in match.get('wide_round_spans',[]) if x['stage']==c['stage'] and x['first']==c['first'] and x['last']==c['last']]
        if len(found)!=1 or sorted(found[0]['lines'])!=sorted(r['line'] for r in c['records']):
            raise ValueError('Phase 2 scheduling candidate missing/changed')
    # Freeze actual Phase 2/3 inputs; later unrelated phase files must not
    # invalidate reproduction of this historical inventory.
    frozen=json.loads((directory/'phase3_protected_before.json').read_text())
    input_paths=[ROOT/name for name in frozen if (ROOT/name).resolve().is_relative_to(directory.resolve())]
    input_paths += [directory/name for name in ('phase3_protected_before.json',TREE,'phase3_git_tree_receipt.json',MANIFEST)]
    for item in plan():
        source=directory/item['path'];input_paths.extend([source,source.with_name(source.name+'.provenance.json')])
    return dict(scope='Phase 3 acquisition and inventory only; structural correctness and historical certification deferred',
                source_scope=dict(seasons_requested=36,accounted=len(out),seasons_parsed=len(covered),
                                  primary_dataset_files=15,new_originals=12,reused_originals=3,missing_files=sorted(set(missing))),
                totals=dict(observed=sum(r['records'] for r in covered),scored=sum(r['scored'] for r in covered),
                            expected=sum(r['expected'] for r in out),parse_review_seasons=sum(r['status']=='PARSE_REVIEW' for r in out)),
                seasons=out,review_candidates=candidates,phase2_candidates_carried_forward=prior['round_spans_at_least_14_days'],
                phase2_candidate_count=len(prior['round_spans_at_least_14_days']),historical_phase2_records_separate=phases,
                historical_outside_selected_window_or_stage_count=len(outside),
                preservation=protection,rights=base['rights'],
                inputs={str(p.relative_to(directory)):sha(p.read_bytes()) for p in sorted(input_paths)},
                assurance='Counts are measured, not forced. No correction, exclusion, alias reconciliation, source merge, standardized IDs or training eligibility assigned.')


def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args()
    target=PRIVATE/OUTPUT
    if not args.check and target.exists():raise FileExistsError('Inventory already exists; use --check')
    result=build();raw=encode(result)
    if args.check:
        if target.read_bytes()!=raw:raise ValueError('Saved inventory differs')
    else:save(target,raw)
    for r in result['seasons']:print(r['season'],r['records'],r['scored'],r['expected'],r['status'],r.get('issues',r.get('error')))
    print('TOTAL',result['totals']);print('CANDIDATES',len(result['review_candidates']))


if __name__=='__main__':main()
