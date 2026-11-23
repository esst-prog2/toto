"""Independent Phase 4 raw structural validation; no historical or screening policy."""
import argparse,calendar,csv,io,json,re,subprocess,unicodedata
from collections import Counter,defaultdict
from datetime import date
from copy import deepcopy
from scripts import collect_eredivisie_history as acquisition

ROOT,PRIVATE,c=acquisition.ROOT,acquisition.PRIVATE,acquisition.c
BASELINE='phase4_protected_before.json'
NAMES=('phase4_historical_structure.json','phase4_modern_structure.json','phase4_overlap_reconciliation.json','phase4_review_queue.json')
COLUMNS=('Date','Season','home','visitor','FT','hgoal','vgoal','tier')
# Explicit per-season links are read from frozen Phase 3, never applied to source values.


def initialize(directory=PRIVATE,root=ROOT):
    if (directory/BASELINE).exists():return protect(directory,root)
    if subprocess.check_output(['git','branch','--show-current'],cwd=root).decode().strip()!='feature/data-collection' or subprocess.check_output(['git','rev-parse','HEAD'],cwd=root).decode().strip()!='4f8c64433cf6168a06dbde0102e822ce6d2eeffa':raise ValueError('Unexpected branch/HEAD')
    acquisition.protect(directory,root);receipt=json.loads((directory/'phase3_final_verification.json').read_text())
    for n,x in receipt['private_files_before_receipt'].items():
        if c.sha((directory/n).read_bytes())!=x['sha256']:raise ValueError('Phase 3 private artifact changed: '+n)
    for n,h in receipt['public_files'].items():
        if c.sha((root/n).read_bytes())!=h:raise ValueError('Phase 3 public work changed: '+n)
    files={str(p.relative_to(root)):c.sha(p.read_bytes()) for p in directory.rglob('*') if p.is_file()};files.update({n:h for n,h in receipt['public_files'].items() if n!='PLANNING_LOG.md'})
    log=(root/'PLANNING_LOG.md').read_bytes();index=subprocess.check_output(['git','rev-parse','--git-path','index'],cwd=root).decode().strip()
    c.save(directory/BASELINE,c.encode(dict(files=files,planning_log=dict(bytes=len(log),sha256=c.sha(log)),head=receipt['head'],index_sha256=c.sha((root/index).read_bytes()))))
    return protect(directory,root)


def protect(directory=PRIVATE,root=ROOT):
    previous=acquisition.protect(directory,root);saved=json.loads((directory/BASELINE).read_text())
    if not saved['files']:raise ValueError('Empty structural baseline')
    for n,h in saved['files'].items():
        if not (root/n).resolve().is_relative_to(root.resolve()) or c.sha((root/n).read_bytes())!=h:raise ValueError('Frozen Phase 2–3 entry changed: '+n)
    log=(root/'PLANNING_LOG.md').read_bytes();prefix=saved['planning_log']
    if len(log)<prefix['bytes'] or c.sha(log[:prefix['bytes']])!=prefix['sha256']:raise ValueError('Planning history changed')
    return dict(previous=previous,phase2_3_entries=len(saved['files']))


def bind(fields,receipt,start,end,literal):
    return dict(fields,source=receipt['path'],source_sha256=receipt['sha256'],source_line=start,source_end_line=end,physical_record_sha256=c.sha(literal),audit_id=c.sha(c.encode([receipt['sha256'],start,end])),provenance={k:receipt[k] for k in ('commit','git_blob_sha1','url')})


def parse_historical(raw,receipt):
    if c.sha(raw)!=receipt['sha256']:raise ValueError('Historical SHA mismatch')
    physical=raw.splitlines(keepends=True);reader=csv.DictReader(io.StringIO(raw.decode('utf-8-sig'),newline=''),strict=True)
    if tuple(reader.fieldnames or ())!=COLUMNS:raise ValueError('Unexpected exact historical columns')
    rows=[]
    while True:
        start=reader.line_num+1
        try:r=next(reader)
        except StopIteration:break
        if None in r or any(x is None for x in r.values()):raise ValueError('Malformed CSV observation')
        if not re.fullmatch(r'\d{4}',r['Season']) or r['tier']!='1':raise ValueError('Unapproved season/tier at line '+str(start))
        y=int(r['Season']);end=reader.line_num
        fields=dict(season=f'{y}/{y+1}',date=r['Date'],home=r['home'],away=r['visitor'],hg=r['hgoal'],ag=r['vgoal'],FT=r['FT'],HT=None,annotation='',round=None,stage='HISTORICAL_TIER1_STAGE_NOT_EXPLICIT',original_fields=r,date_semantics='SOURCE_ISO_DATE_NOT_INDEPENDENT_AVAILABILITY',date_basis='EXPLICIT_ISO_DATE',year_explicit=True)
        rows.append(bind(fields,receipt,start,end,b''.join(physical[start-1:end])))
    if not rows:raise ValueError('Empty historical source')
    return rows


def parse_modern(raw,year,receipt):
    if c.sha(raw)!=receipt['sha256']:raise ValueError('Modern SHA mismatch')
    rows=[];notes=[];current=None;round_id=None;stage=None;title=False;headings=Counter();months={m:i for i,m in enumerate(calendar.month_abbr) if m};weekdays=list(calendar.day_abbr);depth=0
    for number,literal in enumerate(raw.splitlines(keepends=True),1):
        line=literal.decode('utf-8-sig').rstrip('\r\n');text=line.strip()
        if not text:continue
        if text.startswith('#'):notes.append(dict(line=number,kind='COMMENT',text=text));continue
        if depth or text.startswith('('):
            if not rows:raise ValueError('Detail before fixture')
            depth+=text.count('(')-text.count(')')
            if depth<0:raise ValueError('Unbalanced detail')
            notes.append(dict(line=number,kind='DETAIL',text=text));continue
        if text.startswith('='):
            if title or text!=f'= Netherlands Eredivisie {year}/{(year+1)%100:02}':raise ValueError('Wrong title/season')
            title=True;notes.append(dict(line=number,kind='TITLE',text=text));continue
        if text.startswith('▪'):
            m=re.fullmatch(r'▪ (?:Matchday (\d+)|(\d+)\. Round|Regular Season - (\d+))',text)
            if m:
                round_id=int(next(x for x in m.groups() if x));stage='REGULAR_SEASON';headings[round_id]+=1
                if not 1<=round_id<=34:raise ValueError('Round out of bounds')
            elif re.search(r'play.?off|final|nacompetitie|promotion',text,re.I):stage='OTHER_STAGE';round_id=text
            else:raise ValueError('Unknown stage')
            notes.append(dict(line=number,kind='ROUND',text=text));current=None;continue
        m=re.fullmatch(r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun) ([A-Z][a-z]{2}) (\d{1,2})(?: (\d{4}))?',text)
        if m:
            weekday,month,day,explicit=m.groups();candidates=[]
            for y in ([int(explicit)] if explicit else [year,year+1]):
                try:d=date(y,months[month],int(day))
                except (ValueError,KeyError):continue
                if date(year,7,1)<=d<=date(year+1,6,30) and weekdays[d.weekday()]==weekday:candidates.append(d.isoformat())
            if len(candidates)!=1:raise ValueError('Ambiguous/invalid date heading')
            current=dict(date=candidates[0],date_heading=text,date_heading_line=number,date_basis='EXPLICIT_DAY_MONTH_YEAR_WEEKDAY' if explicit else 'EXPLICIT_DAY_MONTH_WITH_SEASON_WEEKDAY_YEAR_RESOLUTION',year_explicit=bool(explicit));continue
        if not title or current is None or stage is None:raise ValueError('Unbound fixture at physical line '+str(number))
        body=re.sub(r'^\d{1,2}:\d{2}\s+','',text);annotation='';note=re.search(r'\s+(\[[^\]]+\])$',body)
        if note:annotation=note[1];body=body[:note.start()].rstrip()
        if not re.search(r'\s+v\s+',body):raise ValueError('Unknown fixture grammar')
        home,tail=re.split(r'\s+v\s+',body,maxsplit=1);score=re.fullmatch(r'(.+?)\s{2,}([0-9]+)-([0-9]+)(?:\s+\(([0-9]+-[0-9]+)\))?',tail)
        if score:away,hg,ag,ht=score.groups();ft=f'{hg}-{ag}'
        else:
            if re.search(r'\d\s*[-:]|[-:]\s*\d|\?\s*[-:]',tail):raise ValueError('Malformed partial score')
            away=tail;hg=ag=ht=ft=None
        fields=dict(home=home,away=away,hg=hg,ag=ag,HT=ht,FT=ft,annotation=annotation,season=f'{year}/{year+1}',**current,date_semantics='SOURCE_DAY_HEADING_NOT_AVAILABILITY_CERTIFICATION',stage=stage,round=round_id,raw_record=line)
        rows.append(bind(fields,receipt,number,number,literal))
    if not title or not rows or depth:raise ValueError('Missing or unterminated source content')
    return rows,dict(notes=notes,repeated_round_headings={str(k):n for k,n in sorted(headings.items()) if n>1})


def inspect_record(r):
    errors=[];flags=[];cancelled='cancelled' in r['annotation'].lower();unscored=r['hg'] is None and r['ag'] is None;h=a=None
    for key in ('home','away'):
        text=r[key]
        if not isinstance(text,str) or not text or text!=text.strip() or '\ufffd' in text or any(unicodedata.category(x).startswith('C') for x in text):errors.append('INVALID_TEAM_LABEL')
    if r['home']==r['away']:errors.append('IDENTICAL_TEAMS')
    try:
        d=date.fromisoformat(r['date']);y=int(r['season'][:4])
        if d.isoformat()!=r['date'] or r['season']!=f'{y}/{y+1}' or not date(y,7,1)<=d<=date(y+1,6,30):errors.append('INVALID_SEASON_DATE')
    except (ValueError,TypeError):errors.append('INVALID_DATE')
    if (r['hg'] is None)!=(r['ag'] is None):errors.append('PARTIAL_SCORE')
    if not unscored:
        if not all(isinstance(r[k],str) and re.fullmatch(r'0|[1-9][0-9]*',r[k]) and int(r[k])<=2**63-1 for k in ('hg','ag')):errors.append('INVALID_SCORE')
        else:
            h,a=int(r['hg']),int(r['ag'])
            if r['FT']!=f'{h}-{a}':errors.append('FT_GOAL_CONFLICT')
    elif r['FT'] is not None:errors.append('FT_WITHOUT_GOALS')
    if r['HT'] is not None:
        ht=re.fullmatch(r'([0-9]+)-([0-9]+)',r['HT'])
        if not ht or h is None or int(ht[1])>h or int(ht[2])>a:errors.append('HT_FT_CONFLICT')
    if cancelled and not unscored:errors.append('CANCELLED_WITH_SCORE')
    if r['stage'] not in {'REGULAR_SEASON','HISTORICAL_TIER1_STAGE_NOT_EXPLICIT'}:errors.append('OTHER_STAGE')
    if r['annotation']:flags.append('SOURCE_ANNOTATION')
    if unscored:flags.append('SOURCE_UNSCORED')
    if h is not None and (max(h,a)>=7 or h+a>=10):flags.append('UNUSUAL_SCORE')
    if unscored and not cancelled:flags.append('UNEXPLAINED_INCOMPLETE')
    if errors:flags.append('STRUCTURAL_REVIEW')
    return dict(structurally_valid=not errors,errors=sorted(set(errors)),score_bearing=h is not None and a is not None,unscored=unscored,result_incomplete=unscored,unexplained_incomplete=unscored and not cancelled,source_marked_cancelled=cancelled,goal_derived_outcome=None if h is None else 'H' if h>a else 'A' if h<a else 'D',flags=sorted(flags),historical_certification='NOT_CLAIMED',chronology=dict(source_date=r['date'],source_heading_date=r.get('date_heading',r['date']),scheduled_date=r['date'] if cancelled else None,actual_kickoff_date=None,actual_completion_date=None,administrative_publication_date=None,administrative_finality_date=None,effective_availability=None,meaning='SOURCE_DATE_NOT_INDEPENDENT_AVAILABILITY'),processing_policy='NOT_DECIDED')


def season_check(rows,year,modern):
    n=16 if 1962<=year<=1965 else 18;names={r[k] for r in rows for k in ('home','away')};pairs=defaultdict(list);rounds=defaultdict(list);events=defaultdict(list)
    for r in rows:
        r['structural']=inspect_record(r);pairs[r['home'],r['away']].append(r)
        if modern:rounds[str(r['round'])].append(r)
        for team in (r['home'],r['away']):events[r['date'],team].append(r)
    missing=sorted([h,a] for h in names for a in names if h!=a and (h,a) not in pairs);duplicates=[dict(home=h,away=a,ids=[r['audit_id'] for r in rs],conflicting=len({r['FT'] for r in rs})>1) for (h,a),rs in sorted(pairs.items()) if len(rs)>1]
    collisions=[dict(date=d,team=t,ids=[r['audit_id'] for r in rs]) for (d,t),rs in sorted(events.items()) if len(rs)>1];wide=[];round_checks=[]
    for rnd,rs in sorted(rounds.items(),key=lambda x:int(x[0]) if x[0].isdigit() else 999):
        first=min(r['date'] for r in rs);last=max(r['date'] for r in rs);span=(date.fromisoformat(last)-date.fromisoformat(first)).days;counts=Counter(r[k] for r in rs for k in ('home','away'))
        issues=[]
        if len(rs)!=n//2:issues.append('ROUND_FIXTURE_COUNT')
        if set(counts)!=names or any(v!=1 for v in counts.values()):issues.append('ROUND_TEAM_COVERAGE')
        round_checks.append(dict(round=rnd,observed=len(rs),issues=issues))
        if span>14:
            wide.append(dict(round=rnd,first_date=first,last_date=last,span_days=span,fixture_ids=[r['audit_id'] for r in rs]))
            for r in rs:r['structural']['flags'].append('WIDE_ROUND')
    reversals=[]
    for previous,current in zip(rows,rows[1:]):
        if current['date']<previous['date']:
            reversals.append(dict(previous_id=previous['audit_id'],current_id=current['audit_id'],previous_date=previous['date'],current_date=current['date']))
            for r in (previous,current):r['structural']['flags'].append('SOURCE_ORDER_REVERSAL')
    for duplicate in duplicates:
        for rs in pairs.values():
            for r in rs:
                if r['audit_id'] in duplicate['ids']:r['structural']['flags'].append('CONFLICTING_PAIR' if duplicate['conflicting'] else 'DUPLICATE_PAIR')
    for collision in collisions:
        for r in rows:
            if r['audit_id'] in collision['ids']:r['structural']['flags'].append('TEAM_SAME_DAY_COLLISION')
    normalization=defaultdict(set)
    for name in names:normalization[unicodedata.normalize('NFC',name).casefold()].add(name)
    normalized={k:sorted(v) for k,v in normalization.items() if len(v)>1};format_issues=[]
    if len(names)!=n:format_issues.append('CLUB_COUNT')
    if duplicates:format_issues.append('DUPLICATE_PAIRINGS')
    if collisions:format_issues.append('TEAM_SAME_DAY_COLLISION')
    if missing and year!=2019:format_issues.append('MISSING_PAIRINGS')
    if len(rows)!=(232 if year==2019 and not modern else n*(n-1)):format_issues.append('OBSERVED_COUNT')
    if modern and set(rounds)!={str(i) for i in range(1,35)}:format_issues.append('ROUND_SET')
    if any(x['issues'] for x in round_checks):format_issues.append('ROUND_STRUCTURE')
    for r in rows:r['structural']['flags']=sorted(set(r['structural']['flags']))
    return dict(season=f'{year}/{year+1}',observed=len(rows),expected_slots=n*(n-1),clubs=len(names),team_labels=sorted(names),scored=sum(r['structural']['score_bearing'] for r in rows),unscored=sum(r['structural']['unscored'] for r in rows),valid=sum(r['structural']['structurally_valid'] for r in rows),invalid=sum(not r['structural']['structurally_valid'] for r in rows),unexplained_incomplete=sum(r['structural']['unexplained_incomplete'] for r in rows),missing_pairings=missing,duplicate_pairings=duplicates,same_day_collisions=collisions,normalized_label_collisions=normalized,wide_rounds=wide,reversals=reversals,round_checks=round_checks,format_issues=format_issues,stage_counts=dict(Counter(r['stage'] for r in rows)),goal_outcomes=dict(Counter(r['structural']['goal_derived_outcome'] for r in rows if r['structural']['score_bearing'])),score_distribution=dict(sorted(Counter(r['FT'] for r in rows if r['FT'] is not None).items())),date_range=[min(r['date'] for r in rows),max(r['date'] for r in rows)],date_basis_counts=dict(Counter(r['date_basis'] for r in rows)))


def reconcile_rows(rows,prior):
    actual={r['audit_id']:r for r in rows};expected={r['audit_id']:r for r in prior}
    if len(actual)!=len(rows) or len(expected)!=len(prior) or actual.keys()!=expected.keys():raise ValueError('Ambiguous or missing source identity')
    for key,original in expected.items():
        for field,value in original.items():
            if actual[key].get(field)!=value:raise ValueError('Raw/Phase 3 mismatch: '+field)
    return dict(observations=len(rows),all_original_fields_equal=True)


def compare_sources(historical,modern,hypotheses):
    hs={r[k] for r in historical for k in ('home','away')};ms={r[k] for r in modern for k in ('home','away')};links={x:x for x in hs&ms}
    for pair in hypotheses:
        h,m=pair['historical'],pair['modern']
        if pair['status']!='DIAGNOSTIC_ONLY_NOT_APPROVED_ALIAS' or h not in hs or m not in ms or h in links or m in links.values():raise ValueError('Ambiguous/unbound diagnostic label correspondence')
        links[h]=m
    left=defaultdict(list);right=defaultdict(list)
    for r in historical:left[links.get(r['home']),links.get(r['away'])].append(r)
    for r in modern:right[r['home'],r['away']].append(r)
    if any(len(rs)>1 for rs in left.values()) or any(len(rs)>1 for rs in right.values()):raise ValueError('Ambiguous overlap pairing')
    matched=[]
    for pair,rs in sorted(left.items(),key=lambda x:str(x[0])):
        if None in pair or pair not in right:continue
        a,b=rs[0],right[pair][0];matched.append(dict(historical_id=a['audit_id'],modern_id=b['audit_id'],historical_labels=[a['home'],a['away']],modern_labels=[b['home'],b['away']],historical_date=a['date'],modern_date=b['date'],historical_FT=a['FT'],modern_FT=b['FT'],date_equal=a['date']==b['date'],score_equal=a['FT']==b['FT']))
    return dict(matches=matched,unmatched_historical=sorted(set(r['audit_id'] for r in historical)-{m['historical_id'] for m in matched}),unmatched_modern=sorted(set(r['audit_id'] for r in modern)-{m['modern_id'] for m in matched}),diagnostic_name_hypotheses=deepcopy(hypotheses),historical_independence='UNESTABLISHED')


def build(directory=PRIVATE,root=ROOT):
    protected=protect(directory,root);old=c.verify_originals(directory);new=acquisition.verify_originals(directory)
    old_h=json.loads((directory/'phase3_historical_inventory.json').read_text());old_m=json.loads((directory/'phase3_modern_inventory.json').read_text());old_overlap=json.loads((directory/'phase3_overlap_registry.json').read_text());old_queue=json.loads((directory/'phase3_review_candidates.json').read_text())
    hr=next(r for r in old['files'] if r['repository']==c.HIST);all_historical=parse_historical((directory/hr['path']).read_bytes(),hr);groups=defaultdict(list)
    for r in all_historical:groups[int(r['season'][:4])].append(r)
    all_summaries=[season_check(rs,y,False) for y,rs in sorted(groups.items())];historical=[r for r in all_historical if 1990<=int(r['season'][:4])<=2024]
    historical_reconciliation=reconcile_rows(historical,[r for s in old_h['seasons'] for r in s['records']]);modern=[];modern_summaries=[];source_notes=[]
    receipts=[r for r in old['files']+new['files'] if r['repository']==c.MODERN]
    if len(receipts)!=8 or {r['season'] for r in receipts}!={f'{y}/{y+1}' for y in range(2018,2026)}:raise ValueError('Modern receipt set differs')
    for receipt in sorted(receipts,key=lambda r:r['season']):
        y=int(receipt['season'][:4]);rs,notes=parse_modern((directory/receipt['path']).read_bytes(),y,receipt);modern_summaries.append(season_check(rs,y,True));modern.extend(rs);source_notes.append(dict(source=receipt['path'],**notes))
    modern_reconciliation=reconcile_rows(modern,[r for s in old_m['seasons'] for r in s['records']]);mh=defaultdict(list);hh=defaultdict(list)
    for r in modern:mh[r['season']].append(r)
    for r in historical:hh[r['season']].append(r)
    overlaps=[]
    for old_item in old_overlap['overlaps']:
        season=old_item['season'];comparison=compare_sources(hh[season],mh[season],old_item['conditional']['hypothesized_label_correspondences'])
        if sorted(comparison['matches'],key=lambda x:x['historical_id'])!=sorted(old_item['conditional']['comparisons'],key=lambda x:x['historical_id']) or comparison['unmatched_historical']!=sorted(old_item['conditional']['unmatched_historical_ids']) or comparison['unmatched_modern']!=sorted(old_item['conditional']['unmatched_modern_ids']):raise ValueError('Independent overlap differs from Phase 3')
        overlaps.append(dict(season=season,**comparison))
    lookup={r['audit_id']:r for r in historical+modern};context=old_queue['documentary_context'];leads=defaultdict(list)
    for item in context['exceptions']:
        if 'source_observation' in item:
            original=item['source_observation'];key=original['audit_id']
            if key not in lookup or any(lookup[key].get(k)!=v for k,v in original.items()):raise ValueError('Documentary source binding differs')
            leads[key].append(deepcopy(item));lookup[key]['structural']['flags'].append(item.get('kind','KNOWN_INTERRUPTION_CONTEXT'))
        elif 'original_comparison' in item:
            for field in ('historical_id','modern_id'):
                key=item['original_comparison'][field]
                if key not in lookup:raise ValueError('Unbound documentary conflict')
                leads[key].append(deepcopy(item));lookup[key]['structural']['flags'].append(item['kind'])
    for overlap in overlaps:
        for pair in overlap['matches']:
            for field,flag in [('date_equal','CROSS_SOURCE_DATE_DISAGREEMENT'),('score_equal','CROSS_SOURCE_SCORE_DISAGREEMENT')]:
                if not pair[field]:
                    for key in ('historical_id','modern_id'):lookup[pair[key]]['structural']['flags'].append(flag)
    for r in lookup.values():r['structural']['flags']=sorted(set(r['structural']['flags']))
    queue=[dict(original={k:deepcopy(v) for k,v in r.items() if k!='structural'},assessment=deepcopy(r['structural']),evidence_leads=leads.get(r['audit_id'],[])) for r in sorted(lookup.values(),key=lambda r:(r['source'],r['source_line'])) if r['structural']['flags']]
    previous_queue={r['original']['audit_id']:r for r in old_queue['queue']['records']};current_queue={r['original']['audit_id']:r for r in queue}
    if not previous_queue.keys()<=current_queue.keys():raise ValueError('Prior review candidates lost')
    for key,r in previous_queue.items():
        if r['original']!=current_queue[key]['original'] or not set(r['categories'])<=set(current_queue[key]['assessment']['flags']):raise ValueError('Prior queue binding/category lost')
    cancellations=next(o for o in overlaps if o['season']=='2019/2020');missing=next(s for s in all_summaries if s['season']=='2019/2020')['missing_pairings'];unmatched=[lookup[k] for k in cancellations['unmatched_modern']]
    if set(map(tuple,missing))!={(r['home'] if r['home']!='Heracles Almelo' else 'Heracles',r['away'] if r['away']!='Heracles Almelo' else 'Heracles') for r in unmatched}:raise ValueError('Absent/cancelled identities differ')
    if not all(r['FT'] is None and r['annotation']=='[cancelled]' for r in unmatched):raise ValueError('2019 source cancellation discrepancy')
    scores=[r for r in historical+modern if r['structural']['score_bearing']];unscored=[r for r in historical+modern if r['structural']['unscored']];pairs_matched=sum(len(o['matches']) for o in overlaps)
    unique_scored=len(scores)-pairs_matched;unique_slots=unique_scored+len(unscored)
    labels=sorted({r[k] for r in historical+modern for k in ('home','away')});combinations=Counter('+'.join(r['assessment']['flags']) for r in queue)
    summary=dict(target_seasons=len(set(hh)|set(mh)),source_observations=len(historical)+len(modern),historical_target=len(historical),modern=len(modern),structurally_valid=sum(r['structural']['structurally_valid'] for r in historical+modern),structurally_invalid=sum(not r['structural']['structurally_valid'] for r in historical+modern),score_bearing=len(scores),unscored=len(unscored),result_incomplete=len(unscored),unexplained_incomplete=sum(r['structural']['unexplained_incomplete'] for r in historical+modern),conditional_unique_scored_identities=unique_scored,conditional_unique_slots=unique_slots,expected_slots=36*306,matched_scored_source_pairs=pairs_matched,score_disagreements=sum(not x['score_equal'] for o in overlaps for x in o['matches']),date_disagreements=sum(not x['date_equal'] for o in overlaps for x in o['matches']),wide_round_contexts=sum(len(s['wide_rounds']) for s in modern_summaries),wide_members=sum(len(w['fixture_ids']) for s in modern_summaries for w in s['wide_rounds']),reversal_pairs=sum(len(s['reversals']) for s in modern_summaries),reversal_endpoints=len({key for s in modern_summaries for pair in s['reversals'] for key in [pair['previous_id'],pair['current_id']]}),queue=len(queue),previous_queue=len(previous_queue),literal_labels=len(labels),not_accepted_or_certified_count=True)
    # Expectation mismatches remain visible; no corrections or counts are forced.
    return {NAMES[0]:dict(phase=4,receipt=hr,all_source_records=all_historical,all_source_seasons=all_summaries,target_reconciliation=historical_reconciliation,protected=protected,policy='Basic structure for entire original; target research window remains 1990/91–2025/26'),NAMES[1]:dict(phase=4,receipts=receipts,records=modern,seasons=modern_summaries,source_notes=source_notes,reconciliation=modern_reconciliation,protected=protected),NAMES[2]:dict(phase=4,summary=summary,overlaps=overlaps,cancellation_2019_20=dict(historical_scored=len(hh['2019/2020']),modern_slots=len(mh['2019/2020']),missing_historical=len(missing),explicit_unscored_modern=len(unmatched),exact_identity_reconciliation=True),labels=labels,coverage=[dict(season=f'{y}/{y+1}',expected_slots=306,historical=next((s for s in all_summaries if s['season']==f'{y}/{y+1}'),None),modern=next((s for s in modern_summaries if s['season']==f'{y}/{y+1}'),None)) for y in range(1990,2026)],identity_review=old_queue['identity'],upstream_independence='UNESTABLISHED',rights=c.RIGHTS),NAMES[3]:dict(phase=4,summary=summary,records=queue,categories=dict(Counter(flag for r in queue for flag in r['assessment']['flags'])),category_combinations=dict(combinations),new_review_ids=sorted(current_queue.keys()-previous_queue.keys()),documentary_context=context,warning='Source-bound observations, not real-world matches; no HOLD OUT/NOT PLAYED/source preference or availability policy')}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--init',action='store_true');args=parser.parse_args()
    if args.init:initialize()
    outputs=build()
    for name,obj in outputs.items():
        raw=c.encode(obj);target=PRIVATE/name
        if target.exists():
            if target.read_bytes()!=raw:raise ValueError('Structural output changed: '+name)
        else:c.save(target,raw)
    print(json.dumps(outputs[NAMES[2]]['summary'],indent=2))
