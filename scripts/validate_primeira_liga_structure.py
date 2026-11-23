"""Independent Phase 4 structural assessment; no historical decisions or aliases."""
import argparse,csv,io,json,re,subprocess,unicodedata
from collections import Counter,defaultdict
from copy import deepcopy
from datetime import date,datetime
from pathlib import Path
from scripts import collect_primeira_liga_history as acquisition
c=acquisition.c
ROOT,PRIVATE=acquisition.ROOT,acquisition.PRIVATE
BASELINE='phase4_protected_before.json'
COLUMNS=('Date','Season','home','visitor','FT','hgoal','vgoal','division','tier','totgoal','goaldif','result')
OUTPUTS=('phase4_historical_structure.json','phase4_modern_structure.json','phase4_overlap_reconciliation.json','phase4_review_queue.json','phase4_coverage_gap.json','phase4_integrity_manifest.json')


def initialize(directory=PRIVATE,root=ROOT):
    if (directory/BASELINE).exists():return protect(directory,root)
    acquisition.protect(directory,root)
    if subprocess.check_output(['git','branch','--show-current'],cwd=root).decode().strip()!='feature/data-collection':raise ValueError('Unexpected branch')
    receipt=json.loads((directory/'phase3_final_verification.json').read_text())
    for n,item in receipt['private_files_before_receipt'].items():
        if c.sha((directory/n).read_bytes())!=item['sha256']:raise ValueError('Phase3 evidence changed: '+n)
    for n,h in receipt['public_files'].items():
        if c.sha((root/n).read_bytes())!=h:raise ValueError('Phase3 public work changed: '+n)
    files={str(p.relative_to(root)):c.sha(p.read_bytes()) for p in directory.rglob('*') if p.is_file()}
    files.update({n:h for n,h in receipt['public_files'].items() if n!='PLANNING_LOG.md'})
    log=(root/'PLANNING_LOG.md').read_bytes();c.save(directory/BASELINE,c.encode(dict(files=files,planning_log=dict(bytes=len(log),sha256=c.sha(log)),approval='PHASE4_STRUCTURE_ONLY')))
    return protect(directory,root)


def protect(directory=PRIVATE,root=ROOT):
    prior=acquisition.protect(directory,root);saved=json.loads((directory/BASELINE).read_text())
    if not saved['files'] or saved['approval']!='PHASE4_STRUCTURE_ONLY':raise ValueError('Empty/invalid structural baseline')
    for n,h in saved['files'].items():
        p=root/n
        if not p.resolve().is_relative_to(root.resolve()) or c.sha(p.read_bytes())!=h:raise ValueError('Frozen Phase2–3 evidence changed: '+n)
    prefix=saved['planning_log'];log=(root/'PLANNING_LOG.md').read_bytes()
    if len(log)<prefix['bytes'] or c.sha(log[:prefix['bytes']])!=prefix['sha256']:raise ValueError('Planning prefix changed')
    return dict(previous=prior,phase2_3_frozen_entries=len(saved['files']))


def bound(fields,receipt,start,end,literal):
    return dict(fields,source=receipt['path'],source_sha256=receipt['sha256'],source_line=start,source_end_line=end,physical_record_sha256=c.sha(literal),audit_id=c.sha(c.encode([receipt['sha256'],start,end])),provenance={k:receipt[k] for k in ('commit','git_blob_sha1','url')},original_literal=literal.decode('utf-8-sig'),historical_verification='NOT_CERTIFIED',effective_result_availability=None)


def historical(raw,receipt):
    if c.sha(raw)!=receipt['sha256']:raise ValueError('Historical original checksum differs')
    reader=csv.DictReader(io.StringIO(raw.decode('utf-8-sig'),newline=''),strict=True);physical=raw.splitlines(keepends=True)
    if tuple(reader.fieldnames or ())!=COLUMNS:raise ValueError('Unapproved historical column order')
    rows=[]
    while True:
        start=reader.line_num+1
        try:fields=next(reader)
        except StopIteration:break
        if None in fields or any(x is None for x in fields.values()):raise ValueError('Malformed CSV width at physical line '+str(start))
        if not re.fullmatch(r'\d{4}',fields['Season']):raise ValueError('Ambiguous source season at '+str(start))
        y=int(fields['Season'])
        if not 1994<=y<=2024:raise ValueError('Historical source outside approved represented scope')
        r=dict(season=f'{y}/{y+1}',date=fields['Date'],home=fields['home'],away=fields['visitor'],hg=fields['hgoal'] or None,ag=fields['vgoal'] or None,FT=fields['FT'] or None,HT=None,annotation='',round=None,stage='HISTORICAL_P1_TIER1_STAGE_NOT_EXPLICIT',date_basis='EXPLICIT_ISO_DATE',original_fields=fields)
        rows.append(bound(r,receipt,start,reader.line_num,b''.join(physical[start-1:reader.line_num])))
    if not rows:raise ValueError('Empty historical source')
    return rows


def modern(raw,year,receipt):
    if c.sha(raw)!=receipt['sha256']:raise ValueError('Modern original checksum differs')
    rows=[];notes=[];title=False;context=None;round_id=None;stage=None;depth=0
    for number,literal in enumerate(raw.splitlines(keepends=True),1):
        text=literal.decode('utf-8-sig').rstrip('\r\n');t=text.strip()
        if not t:continue
        if t.startswith('#'):notes.append(dict(line=number,text=t,kind='COMMENT'));continue
        if depth or t.startswith('('):
            if not rows:raise ValueError('Unbound detail')
            depth+=t.count('(')-t.count(')')
            if depth<0:raise ValueError('Unbalanced detail')
            notes.append(dict(line=number,text=t,kind='DETAIL'));continue
        if t.startswith('='):
            if title or t!=f'= Portuguese Primeira Liga {year}/{(year+1)%100:02}':raise ValueError('Wrong/duplicate competition title')
            title=True;continue
        if t.startswith('▪'):
            m=re.fullmatch(r'▪ Matchday (\d+)',t)
            if m:
                round_id=int(m[1]);stage='REGULAR_SEASON'
                if not 1<=round_id<=34:raise ValueError('Unknown round identity')
            elif re.search(r'play.?off|cup|final|promotion',t,re.I):round_id=t;stage='OTHER_STAGE'
            else:raise ValueError('Unknown stage heading')
            context=None;notes.append(dict(line=number,text=t,kind='ROUND'));continue
        m=re.fullmatch(r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun) ([A-Z][a-z]{2}) (\d{1,2})(?: (\d{4}))?',t)
        if m:
            candidates=[]
            for yr in [int(m[4])] if m[4] else [year,year+1]:
                try:day=datetime.strptime(f'{m[2]} {m[3]} {yr}','%b %d %Y').date()
                except ValueError:continue
                limit=date(2020,8,2) if year==2019 else date(year+1,6,30)
                if date(year,7,1)<=day<=limit and day.strftime('%a')==m[1]:candidates.append(day.isoformat())
            if len(candidates)!=1:raise ValueError('Ambiguous/invalid source day at '+str(number))
            context=dict(date=candidates[0],date_heading=t,date_heading_line=number,date_basis='EXPLICIT_DAY_MONTH_YEAR_WEEKDAY' if m[4] else 'EXPLICIT_DAY_MONTH_WITH_SEASON_WEEKDAY_YEAR_RESOLUTION');continue
        if not title or context is None or stage is None:raise ValueError('Unbound fixture at '+str(number))
        content=re.sub(r'^\d{1,2}:\d{2}\s+','',t);annotation='';note=re.search(r'\s+(\[[^\]]+\])$',content)
        if note:annotation=note[1];content=content[:note.start()].rstrip()
        m=re.fullmatch(r'(.+?)\s+v\s+(.+?)\s{2,}(\d+)-(\d+)(?:\s+\((\d+-\d+)\))?',content)
        if m:home,away,hg,ag,ht=m.groups();ft=hg+'-'+ag
        else:
            m=re.fullmatch(r'(.+?)\s+v\s+(.+)',content)
            if not m or re.search(r'\d\s*[-:]|\?\s*[-:]|[-:]\s*\d',content):raise ValueError('Malformed fixture score at '+str(number))
            home,away=m.groups();hg=ag=ht=ft=None
        rows.append(bound(dict(context,season=f'{year}/{year+1}',home=home,away=away,hg=hg,ag=ag,FT=ft,HT=ht,annotation=annotation,round=round_id,stage=stage),receipt,number,number,literal))
    if not rows or not title or depth:raise ValueError('Incomplete modern source')
    return rows,notes


def assess(rows,year,modern_source=False):
    n=16 if 2006<=year<=2013 else 18;names=sorted({r[k] for r in rows for k in ('home','away')});pairs=defaultdict(list);rounds=defaultdict(list);invalid=[];incomplete=[];unusual=[];annotations=[];label_issues=[]
    for r in rows:
        errors=[]
        try:
            d=date.fromisoformat(r['date']);end=date(2020,8,2) if year==2019 else date(year+1,6,30)
            if d.isoformat()!=r['date'] or not date(year,7,1)<=d<=end:errors.append('INVALID_OR_OUTSIDE_DATE')
        except (ValueError,TypeError):errors.append('INVALID_DATE')
        if any(not r[k] or r[k]!=r[k].strip() or '\ufffd' in r[k] for k in ('home','away')) or r['home']==r['away']:label_issues.append(r['audit_id']);errors.append('SOURCE_LABEL_DEFECT')
        h,a=r['hg'],r['ag']
        if h is None and a is None and r['FT'] is None:incomplete.append(r['audit_id'])
        elif not isinstance(h,str) or not isinstance(a,str) or not re.fullmatch(r'0|[1-9]\d*',h) or not re.fullmatch(r'0|[1-9]\d*',a) or r['FT']!=h+'-'+a:errors.append('MALFORMED_OR_CONTRADICTORY_SCORE')
        else:
            hi,ai=int(h),int(a)
            if max(hi,ai)>=7 or hi+ai>=10:unusual.append(r['audit_id'])
            if 'original_fields' in r:
                f=r['original_fields']
                if f['division']!='P1' or f['tier']!='1':errors.append('WRONG_TIER_OR_DIVISION')
                if f['totgoal']!=str(hi+ai) or f['goaldif']!=str(hi-ai) or f['result']!=('H' if hi>ai else 'A' if hi<ai else 'D'):errors.append('DERIVED_FIELD_CONTRADICTION')
            if r['HT'] is not None:
                ht=re.fullmatch(r'(\d+)-(\d+)',r['HT'])
                if not ht or int(ht[1])>hi or int(ht[2])>ai:errors.append('HT_EXCEEDS_FT_OR_INVALID')
        if r['annotation']:annotations.append(dict(id=r['audit_id'],annotation=r['annotation']))
        if modern_source and r['stage']!='REGULAR_SEASON':errors.append('OTHER_STAGE')
        if errors:invalid.append(dict(id=r['audit_id'],reasons=errors))
        pairs[r['home'],r['away']].append(r)
        if r['round'] is not None:rounds[str(r['round'])].append(r)
    wide=[]
    for rnd,rs in sorted(rounds.items()):
        start=min(r['date'] for r in rs);end=max(r['date'] for r in rs);span=(date.fromisoformat(end)-date.fromisoformat(start)).days
        if span>14:wide.append(dict(round=rnd,first_date=start,last_date=end,span_days=span,fixture_ids=[r['audit_id'] for r in rs]))
    folded=defaultdict(set);whitespace=defaultdict(set)
    for label in names:folded[unicodedata.normalize('NFC',label).casefold()].add(label);whitespace[label.strip()].add(label)
    round_errors=[]
    if modern_source:
        for rnd in map(str,range(1,35)):
            rs=rounds.get(rnd,[]);participants=[r[k] for r in rs for k in ('home','away')]
            if len(rs)!=9 or len(set(participants))!=18:round_errors.append(dict(round=rnd,records=len(rs),distinct_participants=len(set(participants))))
    return dict(season=f'{year}/{year+1}',observed=len(rows),scored=sum(r['hg'] is not None and r['ag'] is not None for r in rows),unscored=len(incomplete),expected_clubs=n,clubs=len(names),team_labels=names,expected_slots=n*(n-1),directed_pairs=len(pairs),missing_pairings=[[h,a] for h in names for a in names if h!=a and (h,a) not in pairs],duplicate_pairings=[dict(home=h,away=a,ids=[r['audit_id'] for r in rs],conflicting=len({(r['date'],r['FT']) for r in rs})>1) for (h,a),rs in sorted(pairs.items()) if len(rs)>1],invalid=invalid,label_issues=label_issues,incomplete_ids=incomplete,structurally_valid=len(rows)-len({x['id'] for x in invalid}|set(incomplete)),date_range=[min(r['date'] for r in rows),max(r['date'] for r in rows)],date_precision_counts=dict(Counter(r['date_basis'] for r in rows)),stage_counts=dict(Counter(r['stage'] for r in rows)),round_counts={k:len(v) for k,v in sorted(rounds.items())},round_errors=round_errors,wide_rounds=wide,source_order_reversals=[dict(previous_id=x['audit_id'],current_id=y['audit_id']) for x,y in zip(rows,rows[1:]) if y['date']<x['date']],unusual_scores=unusual,annotations=annotations,casefold_collisions={k:sorted(v) for k,v in folded.items() if len(v)>1},whitespace_collisions={k:sorted(v) for k,v in whitespace.items() if len(v)>1},reserve_labels=[s for s in names if re.search(r'\bB$|\bU(?:19|21|23)\b',s,re.I)],historical_truth='NOT_CERTIFIED',result_availability='UNKNOWN; no chronology eligibility policy')


def correspondence(historical_rows,modern_rows,mapping,season):
    hs={r[k] for r in historical_rows for k in ('home','away')};ms={r[k] for r in modern_rows for k in ('home','away')}
    links={}
    for x in mapping:
        if x['season']!=season or x['historical'] in links:raise ValueError('Cross-season or duplicate diagnostic mapping')
        links[x['historical']]=x['modern']
    if set(links)!=hs or set(links.values())!=ms or len(set(links.values()))!=len(links):raise ValueError('Incomplete/ambiguous diagnostic identity boundary')
    right={}
    for r in modern_rows:
        if r['season']!=season:raise ValueError('Wrong modern season')
        key=(r['home'],r['away'])
        if key in right:raise ValueError('Duplicate modern correspondence target')
        right[key]=r
    compared=[];unmatched=[];seen=set()
    for r in historical_rows:
        if r['season']!=season:raise ValueError('Wrong historical season')
        other=right.get((links[r['home']],links[r['away']]))
        if other is None:unmatched.append(r['audit_id']);continue
        if other['audit_id'] in seen:raise ValueError('Many-to-one correspondence')
        seen.add(other['audit_id']);compared.append(dict(historical_id=r['audit_id'],modern_id=other['audit_id'],historical_labels=[r['home'],r['away']],modern_labels=[other['home'],other['away']],historical_date=r['date'],modern_date=other['date'],historical_FT=r['FT'],modern_FT=other['FT'],date_equal=r['date']==other['date'],score_equal=r['FT']==other['FT'],historical_line=r['source_line'],modern_line=other['source_line']))
    return dict(season=season,mapping=mapping,comparisons=compared,matched=len(compared),unmatched_historical=unmatched,unmatched_modern=sorted({r['audit_id'] for r in modern_rows}-seen),identity_status='Explicit frozen season-bound diagnostic links; no legal entity continuity approval or global aliases')


def feirense(rows):
    rs=[r for r in rows if r['season']=='2011/2012'];found=[r for r in rs if r['source_line']==4877 and r['date']=='2011-08-14' and r['home']=='Feirense ' and r['away']=='Nacional']
    if len(found)!=1:raise ValueError('Exact frozen Feirense observation missing/ambiguous')
    copied=deepcopy(rs)
    for r in copied:
        if r['audit_id']==found[0]['audit_id']:r['home']='Feirense'
    if len(copied)!=len(rs) or [r['audit_id'] for r in copied]!=[r['audit_id'] for r in rs]:raise ValueError('Hypothesis lost observations')
    return dict(original=found[0],literal=assess(rs,2011),hypothetical_one_occurrence=assess(copied,2011),policy_question='Phase5 evidence then Phase6 explicit decision for only this source observation; no approved trim/name/alias',original_unchanged=True)


def build(directory=PRIVATE,root=ROOT):
    protected=protect(directory,root);old=c.verify_originals(directory);new=acquisition.verify_originals(directory)
    receipt=next(r for r in old['files'] if r['repository']==c.HIST);raw=(directory/receipt['path']).read_bytes();hs=historical(raw,receipt);groups=defaultdict(list)
    for r in hs:groups[r['season']].append(r)
    hist=[dict(receipt=receipt,records=rs,assessment=assess(rs,int(season[:4]))) for season,rs in sorted(groups.items())]
    modern_sources=[]
    for rec in sorted([r for r in old['files']+new['files'] if r['repository']==c.MODERN],key=lambda r:r['season']):
        year=int(rec['season'][:4]);rows,notes=modern((directory/rec['path']).read_bytes(),year,rec);modern_sources.append(dict(receipt=rec,records=rows,notes=notes,assessment=assess(rows,year,True)))
    # Independently parsed original facts must reconcile every saved Phase3 row.
    old_h=json.loads((directory/'phase3_historical_inventory.json').read_text());old_m=json.loads((directory/'phase3_modern_inventory.json').read_text());p3rows=[r for s in old_h['seasons']+old_m['seasons'] for r in s['records']]
    rows=hs+[r for s in modern_sources for r in s['records']];lookup={r['audit_id']:r for r in rows}
    if len(lookup)!=len(rows) or set(lookup)!={r['audit_id'] for r in p3rows}:raise ValueError('Source population mismatch or duplicated audit binding')
    fields=('season','date','home','away','hg','ag','FT','HT','annotation','round','stage','source','source_sha256','source_line','source_end_line','physical_record_sha256','provenance')
    for prior in p3rows:
        actual=lookup[prior['audit_id']]
        if any(actual[k]!=prior[k] for k in fields) or ('original_fields' in prior and actual['original_fields']!=prior['original_fields']):raise ValueError('Independent source fact mismatch: '+prior['audit_id'])
    frozen=json.loads((directory/'phase3_overlap_registry.json').read_text());mb={s['assessment']['season']:s for s in modern_sources};overlaps=[];related=defaultdict(list)
    for item in frozen['seasons']:
        season=item['season'];comparison=correspondence(groups[season],mb[season]['records'],item['mapping'],season)
        projection=lambda p:{k:p[k] for k in ('historical_id','modern_id','historical_labels','modern_labels','historical_date','modern_date','historical_FT','modern_FT','date_equal','score_equal')}
        if [projection(p) for p in comparison['comparisons']]!=[projection(p) for p in item['comparisons']]:raise ValueError('Phase3 overlap reconciliation differs')
        overlaps.append(comparison)
        for p in comparison['comparisons']:related[p['historical_id']].append(p['modern_id']);related[p['modern_id']].append(p['historical_id'])
    conflicts=[dict(p,season=o['season'],structural_explanation='Both date strings are valid and within season; source-date interpretation unresolved; no historical date selected') for o in overlaps for p in o['comparisons'] if not p['date_equal'] or not p['score_equal']]
    selectors=[('2019/2020',7290,298,'2020-02-01','2020-02-02','2-1'),('2020/2021',7532,192,'2021-01-03','2021-01-04','1-1')]
    for season,hl,ml,hd,md,ft in selectors:
        matches=[p for p in conflicts if p['season']==season and p['historical_line']==hl and p['modern_line']==ml]
        if len(matches)!=1 or (matches[0]['historical_date'],matches[0]['modern_date'],matches[0]['historical_FT'],matches[0]['modern_FT'])!=(hd,md,ft,ft):raise ValueError('Frozen conflict binding differs')
    bel=[r for r in rows if r['season']=='2021/2022' and ((r['source_line']==7838 and r['source']==receipt['path']) or (r['source_line']==187 and r['source'].endswith('2021-22_pt1.txt')))]
    if len(bel)!=2 or any(r['date']!='2021-11-27' or r['FT']!='0-7' for r in bel):raise ValueError('Frozen Belenenses exception differs')
    categories=defaultdict(set);reasons={
        'WIDE_ROUND':'Round spans over 14 days; scheduling review, not proof of error',
        'SOURCE_ORDER_REVERSAL':'Physical source sequence moves backwards in date; not actual chronological contradiction',
        'UNUSUAL_SCORE':'At least seven goals by one side or ten combined; no automatic correction',
        'SOURCE_DISAGREEMENT':'Bound original dates or scores disagree; authoritative value not selected',
        'KNOWN_ABANDONMENT_REQUIRES_REVIEW':'Source score lacks administrative finality/availability certification; Phase5 documentary research required',
        'SOURCE_FIELD_OR_LABEL':'Explicit structural or literal label defect; source retained',
        'UNSCORED':'Source lacks both final goals; no inferred values'}
    for s in hist+modern_sources:
        a=s['assessment']
        for x in a['invalid']:categories[x['id']].add('SOURCE_FIELD_OR_LABEL')
        for key in a['incomplete_ids']:categories[key].add('UNSCORED')
        for w in a['wide_rounds']:
            for key in w['fixture_ids']:categories[key].add('WIDE_ROUND')
        for rev in a['source_order_reversals']:
            categories[rev['previous_id']].add('SOURCE_ORDER_REVERSAL');categories[rev['current_id']].add('SOURCE_ORDER_REVERSAL')
        for key in a['unusual_scores']:categories[key].add('UNUSUAL_SCORE')
        for x in a['annotations']:categories[x['id']].add('SOURCE_ANNOTATION');reasons['SOURCE_ANNOTATION']='Literal source annotation requires review; no automatic historical disposition'
    for p in conflicts:
        for key in ('historical_id','modern_id'):categories[p[key]].add('SOURCE_DISAGREEMENT')
    for r in bel:categories[r['audit_id']].add('KNOWN_ABANDONMENT_REQUIRES_REVIEW')
    queue=[dict(original=lookup[key],categories=sorted(cats),reasons={k:reasons[k] for k in sorted(cats)},related_overlap_observations=related[key],historical_confidence='UNVERIFIED; no upgrade',actual_completion_date=None,administrative_finality=None,effective_result_availability=None) for key,cats in sorted(categories.items(),key=lambda item:(lookup[item[0]]['source'],lookup[item[0]]['source_line']))]
    priorq=json.loads((directory/'phase3_review_candidates.json').read_text());before={r['original']['audit_id']:set(r['categories']) for r in priorq['records']}
    if any(not cats<=categories[key] for key,cats in before.items()):raise ValueError('Lost frozen review membership')
    coverage=[]
    for year in range(1990,2026):
        season=f'{year}/{year+1}';h=groups.get(season,[]);m=mb[season]['records'] if season in mb else [];o=next((o for o in overlaps if o['season']==season),None);n=20 if year==1990 else 16 if 2006<=year<=2013 else 18
        coverage.append(dict(season=season,expected_clubs=n,expected_slots=n*(n-1),historical=len(h),modern=len(m),overlap=o['matched'] if o else 0,conditional_distinct=len(h)+len(m)-(o['matched'] if o else 0),gap=not h and not m))
    rsssf=json.loads((directory/'rsssf_capabilities.json').read_text());rr=next(r for r in old['files'] if r['repository']=='RSSSF')
    if rsssf['dated_fixtures']!=0 or rsssf['reconstructable_scores']!=380 or any(r['source']==rr['path'] for r in rows):raise ValueError('Undated RSSSF improperly mixed into dated observations')
    totals=dict(historical=len(hs),modern=sum(len(s['records']) for s in modern_sources),source_observations=len(rows),overlap=sum(o['matched'] for o in overlaps),conditional_distinct=sum(x['conditional_distinct'] for x in coverage),represented_seasons=sum(not x['gap'] for x in coverage),expected_full_target=sum(x['expected_slots'] for x in coverage),missing_early_expected=sum(x['expected_slots'] for x in coverage if x['gap']),structurally_valid=sum(s['assessment']['structurally_valid'] for s in hist+modern_sources),label_defects=sum(len(s['assessment']['label_issues']) for s in hist+modern_sources),incomplete=sum(s['assessment']['unscored'] for s in hist+modern_sources),malformed_score_or_derived=sum(any(k!='SOURCE_LABEL_DEFECT' for k in x['reasons']) for s in hist+modern_sources for x in s['assessment']['invalid']),flagged_source_observations=len(queue),unflagged_source_observations=len(rows)-len(queue))
    outputs={OUTPUTS[0]:dict(phase=4,seasons=hist,feirense=feirense(hs)),OUTPUTS[1]:dict(phase=4,seasons=modern_sources),OUTPUTS[2]:dict(phase=4,seasons=overlaps,conflicts=conflicts,belenenses_originals=bel,upstream_independence='UNESTABLISHED'),OUTPUTS[3]:dict(phase=4,totals=totals,category_counts=dict(Counter(k for r in queue for k in r['categories'])),records=queue,identity_review=[dict(source=s['receipt']['path'],season=s['assessment']['season'],literal_labels=s['assessment']['team_labels'],reserve_labels=s['assessment']['reserve_labels'],casefold_collisions=s['assessment']['casefold_collisions'],whitespace_collisions=s['assessment']['whitespace_collisions']) for s in hist+modern_sources],identity_limitations='Belenenses/SAD and AVS/Aves not merged; senior/B sides, Vitoria SC/FC and historical/administrative continuity remain evidence questions'),OUTPUTS[4]:dict(phase=4,seasons=coverage,totals=totals,rsssf_snapshot=rr,rsssf_result_only_count=380,rsssf_dated_count=0,early_gap_status='MISSING_APPROVED_DATED_SOURCE; not NOT PLAYED or proven exclusion',future_research='Separate approval required for early-period dated-source discovery; no Phase5 research here')}
    outputs[OUTPUTS[5]]=dict(phase=4,protected=protected,totals=totals,source_integrity=[{k:r[k] for k in ('path','sha256','bytes','commit','git_blob_sha1','url')} for r in old['files']+new['files']],output_hashes={n:c.sha(c.encode(o)) for n,o in outputs.items()},scope='STRUCTURAL_ONLY; no decisions, standardized dataset, model eligibility, historical certification or rights clearance')
    return outputs


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--init',action='store_true');p.add_argument('--output-directory',type=Path);args=p.parse_args()
    if args.init:print(initialize())
    else:
        target=args.output_directory or PRIVATE
        for n,o in build().items():c.keep(target/n,c.encode(o))
        print('VERIFIED_PHASE4_STRUCTURE')
