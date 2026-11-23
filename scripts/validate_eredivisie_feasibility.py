"""Lossless bounded Eredivisie feasibility; no screening, aliases or corrections."""
from collections import Counter,defaultdict
from datetime import date
from pathlib import Path
import csv,io,json,re,unicodedata
from scripts import collect_eredivisie_feasibility as c
from scripts.validate_ligue2_structure import heading,fixture

PRIVATE=c.PRIVATE
HISTORICAL_YEARS=(1990,2005,2015,2017)
NAMES=('feasibility_assessment.json','coverage_inventory.json','exception_diagnostics.json','overlap_diagnostics.json')
CSV_COLUMNS=('Date','Season','home','visitor','FT','hgoal','vgoal','tier')


def bound(r,receipt,start,end,literal):
    return dict(r,source=receipt['path'],source_sha256=receipt['sha256'],source_line=start,source_end_line=end,physical_record_sha256=c.sha(literal),audit_id=c.sha(c.encode([receipt['sha256'],start,end])),provenance=dict(commit=receipt['commit'],git_blob_sha1=receipt['git_blob_sha1'],url=receipt['url']))


def parse_csv(raw,receipt):
    text=raw.decode('utf-8-sig');lines=raw.splitlines(keepends=True);reader=csv.DictReader(io.StringIO(text,newline=''));columns=tuple(reader.fieldnames or ())
    if columns!=CSV_COLUMNS:raise ValueError('Unexpected historical CSV schema')
    records=[]
    while True:
        start=reader.line_num+1
        try:r=next(reader)
        except StopIteration:break
        end=reader.line_num
        if None in r or any(v is None for v in r.values()):raise ValueError('Malformed historical CSV row')
        if not re.fullmatch(r'\d{4}',r['Season']):raise ValueError('Unknown season label')
        year=int(r['Season']);day=date.fromisoformat(r['Date'])
        if day.isoformat()!=r['Date']:raise ValueError('Noncanonical source date')
        if r['tier']!='1':raise ValueError('Unapproved historical tier')
        for k in ('hgoal','vgoal'):
            if not re.fullmatch(r'0|[1-9]\d*',r[k]):raise ValueError('Missing/nonnumeric historical goals')
        if r['FT']!=r['hgoal']+'-'+r['vgoal']:raise ValueError('Historical FT/goal contradiction')
        record=dict(season=f'{year}/{year+1}',date=r['Date'],home=r['home'],away=r['visitor'],hg=r['hgoal'],ag=r['vgoal'],FT=r['FT'],HT=None,annotation='',round=None,stage='HISTORICAL_TIER1_STAGE_NOT_EXPLICIT',original_fields=r,date_semantics='SOURCE_ISO_DATE_NOT_INDEPENDENT_AVAILABILITY',date_basis='EXPLICIT_ISO_DATE',year_explicit=True)
        records.append(bound(record,receipt,start,end,b''.join(lines[start-1:end])))
    if not records:raise ValueError('Empty historical CSV')
    return records


def parse_text(raw,year,receipt):
    rows=[];notes=[];current=None;rnd=None;stage=None;title=False;physical=raw.splitlines(keepends=True);depth=0;round_occurrences=Counter()
    for number,line in enumerate(raw.decode('utf-8-sig').splitlines(),1):
        t=line.strip()
        if not t:continue
        if t.startswith('#'):notes.append(dict(line=number,kind='COMMENT',text=t));continue
        if depth or t.startswith('('):
            if not rows:raise ValueError('Scorer note without fixture')
            depth+=t.count('(')-t.count(')')
            if depth<0:raise ValueError('Unbalanced note')
            notes.append(dict(line=number,kind='DETAIL',text=t));continue
        if t.startswith('='):
            if title or t!=f'= Netherlands Eredivisie {year}/{(year+1)%100:02}':raise ValueError('Unapproved title')
            title=True;notes.append(dict(line=number,kind='TITLE',text=t));continue
        if t.startswith('▪'):
            m=re.fullmatch(r'▪ (?:Matchday (\d+)|(\d+)\. Round|Regular Season - (\d+))',t)
            if m:
                rnd=int(next(x for x in m.groups() if x));stage='REGULAR_SEASON'
                if not 1<=rnd<=34:raise ValueError('Round outside format')
                round_occurrences[rnd]+=1
            elif re.search(r'play.?off|final|promotion|nacompetitie',t,re.I):stage='OTHER_STAGE';rnd=t
            else:raise ValueError('Unknown stage')
            current=None;notes.append(dict(line=number,kind='ROUND',text=t));continue
        parsed=heading(t,year)
        if parsed:current=dict(parsed,heading_line=number);continue
        if not title or current is None or stage is None:raise ValueError('Fixture without source context')
        body=re.sub(r'^\d{1,2}:\d{2}\s+','',t);r=fixture(body)
        r.update(season=f'{year}/{year+1}',date=current['date'],date_heading=current['date_heading'],date_heading_line=current['heading_line'],date_basis=current['date_basis'],year_explicit=current['year_explicit'],date_semantics='SOURCE_DAY_HEADING_NOT_AVAILABILITY_CERTIFICATION',stage=stage,round=rnd,raw_record=line)
        rows.append(bound(r,receipt,number,number,physical[number-1]))
    if not title or not rows or depth:raise ValueError('Incomplete source grammar')
    return rows,dict(notes=notes,repeated_round_headings={str(k):v for k,v in sorted(round_occurrences.items()) if v>1})


def assess(rows,year):
    n=16 if 1962<=year<=1965 else 18;names=sorted({r[k] for r in rows for k in ('home','away')});pairs=defaultdict(list);invalid=[];rounds=defaultdict(list)
    for r in rows:
        if r['home']==r['away'] or any(not r[k] or r[k]!=r[k].strip() or '\ufffd' in r[k] for k in ('home','away')):invalid.append(dict(id=r['audit_id'],reason='INVALID_TEAM'))
        d=date.fromisoformat(r['date'])
        if not date(year,7,1)<=d<=date(year+1,6,30):invalid.append(dict(id=r['audit_id'],reason='OUTSIDE_SEASON'))
        h,a=r['hg'],r['ag']
        if (h is None)!=(a is None) or (h is not None and (not re.fullmatch(r'0|[1-9]\d*',h) or not re.fullmatch(r'0|[1-9]\d*',a) or r['FT']!=h+'-'+a)):invalid.append(dict(id=r['audit_id'],reason='INVALID_SCORE'))
        if 'cancelled' in r['annotation'].lower() and h is not None:invalid.append(dict(id=r['audit_id'],reason='CANCELLED_WITH_SCORE'))
        pairs[r['home'],r['away']].append(r)
        if r['round'] is not None:rounds[str(r['round'])].append(r)
    wide=[]
    for rnd,rs in sorted(rounds.items()):
        first=min(r['date'] for r in rs);last=max(r['date'] for r in rs);span=(date.fromisoformat(last)-date.fromisoformat(first)).days
        if span>14:wide.append(dict(round=rnd,first_date=first,last_date=last,span_days=span,fixture_ids=[r['audit_id'] for r in rs]))
    normalization=defaultdict(set)
    for name in names:normalization[unicodedata.normalize('NFC',name).casefold()].add(name)
    return dict(season=f'{year}/{year+1}',observed=len(rows),scored=sum(r['hg'] is not None for r in rows),unscored=sum(r['hg'] is None for r in rows),explicitly_cancelled=sum('cancelled' in r['annotation'].lower() for r in rows),unexplained_unscored=sum(r['hg'] is None and 'cancelled' not in r['annotation'].lower() for r in rows),expected_clubs=n,expected_slots=n*(n-1),clubs=len(names),team_labels=names,directed_pairs=len(pairs),missing_pairings=[[h,a] for h in names for a in names if h!=a and (h,a) not in pairs],duplicate_pairings=[dict(home=h,away=a,source_ids=[r['audit_id'] for r in rs],conflicting=len({r['FT'] for r in rs})>1) for (h,a),rs in sorted(pairs.items()) if len(rs)>1],invalid=invalid,date_range=[min(r['date'] for r in rows),max(r['date'] for r in rows)],date_precision_counts=dict(Counter(r['date_basis'] for r in rows)),stage_counts=dict(Counter(r['stage'] for r in rows)),wide_rounds=wide,source_order_reversals=[dict(previous_id=a['audit_id'],current_id=b['audit_id'],previous_date=a['date'],current_date=b['date']) for a,b in zip(rows,rows[1:]) if b['date']<a['date']],unusual_scores=[dict(id=r['audit_id'],date=r['date'],home=r['home'],away=r['away'],FT=r['FT']) for r in rows if r['hg'] is not None and (max(int(r['hg']),int(r['ag']))>=7 or int(r['hg'])+int(r['ag'])>=10)],annotations=[dict(id=r['audit_id'],annotation=r['annotation']) for r in rows if r['annotation']],reserve_labels=[x for x in names if re.search(r'\bJong\b|\bU(?:19|21|23)\b',x,re.I)],casefold_collisions={k:sorted(v) for k,v in normalization.items() if len(v)>1},historical_confidence='NOT_CERTIFIED',availability='UNKNOWN; source dates may be proxies')


def overlap(historical,modern):
    # Identity/score/date diagnostics only. Never used to rewrite source records.
    hs={r['home'] for r in historical}|{r['away'] for r in historical};ms={r['home'] for r in modern}|{r['away'] for r in modern}
    exact=hs&ms;left={(r['home'],r['away']):r for r in historical};right={(r['home'],r['away']):r for r in modern};keys=left.keys()&right.keys();comparisons=[]
    for key in sorted(keys):
        a,b=left[key],right[key];comparisons.append(dict(historical_id=a['audit_id'],modern_id=b['audit_id'],home=key[0],away=key[1],historical_date=a['date'],modern_date=b['date'],historical_FT=a['FT'],modern_FT=b['FT'],date_equal=a['date']==b['date'],score_equal=a['FT']==b['FT']))
    return dict(historical_records=len(historical),modern_records=len(modern),exact_shared_labels=sorted(exact),historical_only_labels=sorted(hs-ms),modern_only_labels=sorted(ms-hs),exact_label_pair_matches=len(keys),comparisons=comparisons,identity_rule='Exact source labels only; unmatched labels require diagnostic identity research, no aliases applied',independence='Unestablished; agreement is not independent historical verification')


# Explicit season-local hypotheses for cross-source diagnostics, never normalization.
DIAGNOSTIC_LABEL_PAIRS=(('Heracles','Heracles Almelo'),('AZ Alkmaar','AZ'),('Almere City','Almere City FC'),('FC Twente',"FC Twente '65"),('Feyenoord','Feyenoord Rotterdam'),('NEC Nijmegen','NEC'),('PSV Eindhoven','PSV'),('Vitesse','SBV Vitesse'),('sc Heerenveen','SC Heerenveen'),('Willem II','Willem II Tilburg'))


def identity_overlap(historical,modern):
    hs={r[k] for r in historical for k in ('home','away')};ms={r[k] for r in modern for k in ('home','away')}
    hypotheses=[(a,b) for a,b in DIAGNOSTIC_LABEL_PAIRS if a in hs and b in ms and a not in ms]
    links={a:a for a in hs&ms}
    for a,b in hypotheses:
        if a in links or b in links.values():raise ValueError('Ambiguous diagnostic correspondence')
        links[a]=b
    pairs={(r['home'],r['away']):r for r in modern};compared=[];unmatched=[]
    for r in historical:
        target=(links.get(r['home']),links.get(r['away']));other=pairs.get(target)
        if other is None:unmatched.append(r['audit_id']);continue
        compared.append(dict(historical_id=r['audit_id'],modern_id=other['audit_id'],historical_labels=[r['home'],r['away']],modern_labels=[other['home'],other['away']],historical_date=r['date'],modern_date=other['date'],historical_FT=r['FT'],modern_FT=other['FT'],date_equal=r['date']==other['date'],score_equal=r['FT']==other['FT']))
    return dict(hypothesized_label_correspondences=[dict(historical=a,modern=b,status='DIAGNOSTIC_ONLY_NOT_APPROVED_ALIAS') for a,b in hypotheses],comparison_pairs=len(compared),unmatched_historical_ids=unmatched,unmatched_modern_ids=sorted(set(r['audit_id'] for r in modern)-set(x['modern_id'] for x in compared)),comparisons=compared,warning='Conditional comparison under explicit season-local name hypotheses; no original or model identity is transformed; upstream independence unestablished')


def build(directory=PRIVATE,root=c.ROOT):
    protected=c.protect(directory,root);m=c.verify_originals(directory);hr=next(r for r in m['files'] if r['repository']==c.HIST);historical=parse_csv((directory/hr['path']).read_bytes(),hr)
    grouped=defaultdict(list)
    for r in historical:grouped[int(r['season'][:4])].append(r)
    inventory=[assess(rs,y) for y,rs in sorted(grouped.items())];modern=[]
    for receipt in m['files']:
        if receipt['repository']!=c.MODERN:continue
        year=int(receipt['season'][:4]);rows,notes=parse_text((directory/receipt['path']).read_bytes(),year,receipt);modern.append(dict(receipt=receipt,records=rows,assessment=assess(rows,year),notes=notes))
    selected=[dict(season=f'{y}/{y+1}',present=y in grouped,records=grouped.get(y,[]),assessment=assess(grouped[y],y) if y in grouped else None) for y in HISTORICAL_YEARS]
    assessment=dict(phase=2,scope='Six approved originals; detailed historical samples and modern overlap only',protected=protected,historical=dict(receipt=hr,columns=list(CSV_COLUMNS),date_format='YYYY-MM-DD explicit',season_format='starting-year integer text',tier_values=sorted({r['original_fields']['tier'] for r in historical}),total_records=len(historical),earliest_season=min(grouped),latest_season=max(grouped),samples=selected),modern=modern,rights=c.RIGHTS,policy='No normalization, corrections, screening, standardization, integration or training')
    coverage=dict(phase=2,columns=list(CSV_COLUMNS),total_records=len(historical),seasons=inventory,advertised='README 1956–2025 versus old package docs 1956/57–2015/16; actual contents measured here',metadata_only_outside_samples=True)
    overlap_results=[dict(season=x['assessment']['season'],**overlap(grouped.get(int(x['assessment']['season'][:4]),[]),x['records'])) for x in modern]
    special=[]
    selectors=[('AFC Ajax','Feyenoord Rotterdam','2023-09-24','2023-09-27','0-4'),('RKC Waalwijk','AFC Ajax','2023-09-30','2023-12-06','2-3'),('AZ','NEC','2023-10-29','2023-12-06','1-2')]
    for home,away,kickoff,completion,ft in selectors:
        matches=[r for x in modern if x['assessment']['season']=='2023/2024' for r in x['records'] if r['home']==home and r['away']==away]
        if len(matches)!=1:raise ValueError('Missing/ambiguous interruption selector')
        r=matches[0];special.append(dict(original=r,research_kickoff_date=kickoff,research_completion_date=completion,research_reported_FT=ft,source_date_agrees_with_completion=r['date']==completion,effective_availability=None,decision='NOT_DECIDED; verify in Phase 5 and decide in Phase 6'))
    exceptions=dict(phase=2,special_interruption_cases=special,modern_review=[dict(season=x['assessment']['season'],wide_rounds=x['assessment']['wide_rounds'],source_order_reversals=x['assessment']['source_order_reversals'],annotations=x['assessment']['annotations'],repeated_round_headings=x['notes']['repeated_round_headings'],invalid=x['assessment']['invalid']) for x in modern],historical_stage_warning='Tier1 only; no explicit per-row stage. Pairing/count checks are structural evidence, not historical stage certification.',identity_warning='Original labels retained; all predecessor/reserve continuity remains evidence-dependent')
    return {NAMES[0]:assessment,NAMES[1]:coverage,NAMES[2]:exceptions,NAMES[3]:dict(phase=2,comparisons=overlap_results),'identity_overlap_diagnostics.json':dict(phase=2,seasons=[dict(season=x['assessment']['season'],**identity_overlap(grouped.get(int(x['assessment']['season'][:4]),[]),x['records'])) for x in modern])}


if __name__=='__main__':
    outputs=build()
    for name,obj in outputs.items():
        raw=c.encode(obj);target=PRIVATE/name
        if target.exists():
            if target.read_bytes()!=raw:raise ValueError('Assessment changed: '+name)
        else:c.save(target,raw)
    print(json.dumps(dict(historical=outputs[NAMES[1]]['total_records'],coverage=[(s['season'],s['observed']) for s in outputs[NAMES[1]]['seasons']],modern=[x['assessment'] for x in outputs[NAMES[0]]['modern']]),indent=2,ensure_ascii=False))
