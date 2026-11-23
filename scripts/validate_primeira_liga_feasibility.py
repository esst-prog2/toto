"""Lossless bounded Primeira Liga feasibility; no screening, aliases or corrections."""
from collections import Counter,defaultdict
from datetime import date
from pathlib import Path
import csv,io,json,re,unicodedata
from scripts import collect_primeira_liga_feasibility as c
from scripts.validate_ligue2_structure import fixture

PRIVATE=c.PRIVATE
HISTORICAL_YEARS=(1994,2005,2006,2013,2014)
NAMES=('feasibility_assessment.json','coverage_inventory.json','exception_diagnostics.json','overlap_diagnostics.json')
CSV_COLUMNS=('Date','Season','home','visitor','FT','hgoal','vgoal','division','tier','totgoal','goaldif','result')


def bound(r,receipt,start,end,literal):
    return dict(r,source=receipt['path'],source_sha256=receipt['sha256'],source_line=start,source_end_line=end,physical_record_sha256=c.sha(literal),audit_id=c.sha(c.encode([receipt['sha256'],start,end])),provenance=dict(commit=receipt['commit'],git_blob_sha1=receipt['git_blob_sha1'],url=receipt['url']))


def expected_clubs(year):
    if year == 1990: return 20
    return 16 if 2006 <= year <= 2013 else 18


def season_end(year):
    return date(2020, 8, 2) if year == 2019 else date(year+1, 6, 30)


def heading(text, year):
    import calendar
    m=re.fullmatch(r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun) ([A-Z][a-z]{2}) (\d{1,2})(?: (\d{4}))?',text)
    if not m:return None
    months={name:i for i,name in enumerate(calendar.month_abbr) if name}; found=[]
    for y in [int(m[4])] if m[4] else [year,year+1]:
        try:d=date(y,months[m[2]],int(m[3]))
        except (KeyError,ValueError):continue
        if date(year,7,1)<=d<=season_end(year) and calendar.day_abbr[d.weekday()]==m[1]:found.append(d.isoformat())
    if len(found)!=1:raise ValueError('Invalid/ambiguous date heading: '+text)
    return dict(date=found[0],date_heading=text,year_explicit=bool(m[4]),date_basis='EXPLICIT_DAY_MONTH_YEAR_WEEKDAY' if m[4] else 'EXPLICIT_DAY_MONTH_WITH_SEASON_WEEKDAY_YEAR_RESOLUTION')


def parse_csv(raw,receipt):
    if c.sha(raw)!=receipt['sha256']:raise ValueError('Historical checksum mismatch')
    physical=raw.splitlines(keepends=True);reader=csv.DictReader(io.StringIO(raw.decode('utf-8-sig'),newline=''),strict=True)
    if tuple(reader.fieldnames or ())!=CSV_COLUMNS:raise ValueError('Unexpected Portugal historical schema')
    rows=[]
    while True:
        start=reader.line_num+1
        try:r=next(reader)
        except StopIteration:break
        if None in r or any(v is None for v in r.values()):raise ValueError('Malformed CSV width')
        if not re.fullmatch(r'\d{4}',r['Season']):raise ValueError('Unknown season')
        y=int(r['Season']);issues=[]
        try:
            d=date.fromisoformat(r['Date'])
            if d.isoformat()!=r['Date']:raise ValueError('noncanonical')
        except ValueError:issues.append('INVALID_DATE')
        if r['tier']!='1' or r['division']!='P1':issues.append('WRONG_COMPETITION')
        h,a=r['hgoal'],r['vgoal']
        if not re.fullmatch(r'0|[1-9]\d*',h) or not re.fullmatch(r'0|[1-9]\d*',a):issues.append('INVALID_SCORE')
        else:
            hi,ai=int(h),int(a)
            if r['FT']!=h+'-'+a:issues.append('FT_CONTRADICTION')
            if r['totgoal']!=str(hi+ai) or r['goaldif']!=str(hi-ai):issues.append('GOAL_DERIVED_CONTRADICTION')
            if r['result']!=('H' if hi>ai else 'A' if hi<ai else 'D'):issues.append('OUTCOME_CONTRADICTION')
        fields=dict(season=f'{y}/{y+1}',date=r['Date'],home=r['home'],away=r['visitor'],hg=h if h else None,ag=a if a else None,FT=r['FT'] if r['FT'] else None,HT=None,annotation='',round=None,stage='HISTORICAL_P1_TIER1_STAGE_NOT_EXPLICIT',original_fields=r,field_issues=issues,date_semantics='SOURCE_DATE_NOT_VERIFIED_AVAILABILITY',date_basis='EXPLICIT_ISO_DATE',year_explicit=True)
        rows.append(bound(fields,receipt,start,reader.line_num,b''.join(physical[start-1:reader.line_num])))
    if not rows:raise ValueError('Empty historical original')
    return rows


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
            if title or t!=f'= Portuguese Primeira Liga {year}/{(year+1)%100:02}':raise ValueError('Unapproved title')
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
    n=expected_clubs(year);names=sorted({r[k] for r in rows for k in ('home','away')});pairs=defaultdict(list);invalid=[];rounds=defaultdict(list)
    for r in rows:
        if r['home']==r['away'] or any(not r[k] or r[k]!=r[k].strip() or '\ufffd' in r[k] for k in ('home','away')):invalid.append(dict(id=r['audit_id'],reason='INVALID_TEAM'))
        d=date.fromisoformat(r['date'])
        if not date(year,7,1)<=d<=season_end(year):invalid.append(dict(id=r['audit_id'],reason='OUTSIDE_SEASON'))
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
    return dict(season=f'{year}/{year+1}',observed=len(rows),scored=sum(r['hg'] is not None for r in rows),unscored=sum(r['hg'] is None for r in rows),explicitly_cancelled=sum('cancelled' in r['annotation'].lower() for r in rows),unexplained_unscored=sum(r['hg'] is None and 'cancelled' not in r['annotation'].lower() for r in rows),expected_clubs=n,expected_slots=n*(n-1),clubs=len(names),team_labels=names,directed_pairs=len(pairs),missing_pairings=[[h,a] for h in names for a in names if h!=a and (h,a) not in pairs],duplicate_pairings=[dict(home=h,away=a,source_ids=[r['audit_id'] for r in rs],conflicting=len({r['FT'] for r in rs})>1) for (h,a),rs in sorted(pairs.items()) if len(rs)>1],invalid=invalid,date_range=[min(r['date'] for r in rows),max(r['date'] for r in rows)],date_precision_counts=dict(Counter(r['date_basis'] for r in rows)),stage_counts=dict(Counter(r['stage'] for r in rows)),wide_rounds=wide,source_order_reversals=[dict(previous_id=a['audit_id'],current_id=b['audit_id'],previous_date=a['date'],current_date=b['date']) for a,b in zip(rows,rows[1:]) if b['date']<a['date']],unusual_scores=[dict(id=r['audit_id'],date=r['date'],home=r['home'],away=r['away'],FT=r['FT']) for r in rows if r['hg'] is not None and (max(int(r['hg']),int(r['ag']))>=7 or int(r['hg'])+int(r['ag'])>=10)],annotations=[dict(id=r['audit_id'],annotation=r['annotation']) for r in rows if r['annotation']],reserve_labels=[x for x in names if re.search(r'\bB$|\bU(?:19|21|23)\b',x,re.I)],casefold_collisions={k:sorted(v) for k,v in normalization.items() if len(v)>1},historical_confidence='NOT_CERTIFIED',availability='UNKNOWN; source dates may be proxies')


def overlap(historical,modern):
    # Identity/score/date diagnostics only. Never used to rewrite source records.
    hs={r['home'] for r in historical}|{r['away'] for r in historical};ms={r['home'] for r in modern}|{r['away'] for r in modern}
    exact=hs&ms;left={(r['home'],r['away']):r for r in historical};right={(r['home'],r['away']):r for r in modern};keys=left.keys()&right.keys();comparisons=[]
    for key in sorted(keys):
        a,b=left[key],right[key];comparisons.append(dict(historical_id=a['audit_id'],modern_id=b['audit_id'],home=key[0],away=key[1],historical_date=a['date'],modern_date=b['date'],historical_FT=a['FT'],modern_FT=b['FT'],date_equal=a['date']==b['date'],score_equal=a['FT']==b['FT']))
    return dict(historical_records=len(historical),modern_records=len(modern),exact_shared_labels=sorted(exact),historical_only_labels=sorted(hs-ms),modern_only_labels=sorted(ms-hs),exact_label_pair_matches=len(keys),comparisons=comparisons,identity_rule='Exact source labels only; unmatched labels require diagnostic identity research, no aliases applied',independence='Unestablished; agreement is not independent historical verification')



# Candidate source-label links for diagnostics only. Each use is explicitly scoped
# to one acquired overlap season; these never normalize stored club identities.
LABEL_CANDIDATES = {
    'Aves': ('CD Aves',), 'Belenenses': ('Belenenses SAD',),
    'Benfica': ('SL Benfica','Sport Lisboa e Benfica'), 'Boavista': ('Boavista','Boavista FC'),
    'Chaves': ('GD Chaves',), 'Feirense': ('CD Feirense',), 'Guimaraes': ('Vitória Guimarães',),
    'Maritimo': ('CS Marítimo',), 'Moreirense': ('Moreirense FC',), 'Nacional': ('CD Nacional',),
    'Portimonense': ('Portimonense SC',), 'Porto': ('FC Porto',), 'Rio Ave': ('Rio Ave FC',),
    'Santa Clara': ('CD Santa Clara',), 'Setubal': ('Vitória Setúbal',),
    'Sp Braga': ('Sporting Braga','Sporting Clube de Braga'),
    'Sp Lisbon': ('Sporting CP','Sporting Clube de Portugal'), 'Tondela': ('CD Tondela',),
    'Famalicao': ('FC Famalicão',), 'Gil Vicente': ('Gil Vicente','Gil Vicente FC'),
    'Pacos Ferreira': ('Paços de Ferreira',), 'Arouca': ('FC Arouca',),
    'Estoril': ('GD Estoril','GD Estoril Praia'), 'FC Vizela': ('FC Vizela',),
    'AVS Futebol SAD': ('AVS',), 'Casa Pia AC': ('Casa Pia AC',),
    'Estrela da Amadora': ('CF Estrela da Amadora',), 'Farense': ('SC Farense',),
}


def identity_overlap(historical, modern):
    seasons={r['season'] for r in historical+modern}
    if len(seasons)!=1:raise ValueError('Diagnostic comparison must be season-bound')
    hs={r[k] for r in historical for k in ('home','away')};ms={r[k] for r in modern for k in ('home','away')};links={};mapping=[]
    for h in sorted(hs):
        options=[m for m in LABEL_CANDIDATES.get(h,(h,)) if m in ms]
        if len(options)>1:raise ValueError('Ambiguous diagnostic label')
        if options:
            m=options[0]
            if m in links.values():raise ValueError('Diagnostic identity collision')
            links[h]=m;mapping.append(dict(season=next(iter(seasons)),historical=h,modern=m,status='DIAGNOSTIC_ONLY_NOT_IDENTITY_APPROVAL',basis='Exact label or explicit Portuguese label hypothesis; fixture pairing consistency tested separately',identity_warning='Belenenses/SAD continuity not approved' if h=='Belenenses' else 'No global club equivalence'))
    by={}
    for r in modern:
        key=(r['home'],r['away'])
        if key in by:raise ValueError('Duplicate comparator fixture')
        by[key]=r
    compared=[];unmatched=[]
    for r in historical:
        other=by.get((links.get(r['home']),links.get(r['away'])))
        if other is None:unmatched.append(r['audit_id']);continue
        compared.append(dict(historical_id=r['audit_id'],modern_id=other['audit_id'],historical_labels=[r['home'],r['away']],modern_labels=[other['home'],other['away']],historical_date=r['date'],modern_date=other['date'],historical_FT=r['FT'],modern_FT=other['FT'],date_equal=r['date']==other['date'],score_equal=r['FT']==other['FT']))
    return dict(season=next(iter(seasons)),mapping=mapping,comparison_pairs=len(compared),comparisons=compared,unmatched_historical_ids=unmatched,unmatched_modern_ids=sorted({r['audit_id'] for r in modern}-{r['modern_id'] for r in compared}),independence='UNESTABLISHED; no global aliases or historical correction')


def rsssf_capabilities(raw, receipt):
    from html import unescape
    text=unescape(raw.decode(receipt['encoding']))
    if 'Cross Table' not in text or 'Accumulated Table' not in text:raise ValueError('RSSSF section structure differs')
    block=text.split('Cross Table',1)[1].split('Accumulated Table',1)[0];table=[]
    for number,line in enumerate(text.splitlines(),1):
        if line in block.splitlines():
            m=re.fullmatch(r'\s*(\d+)\s+(.+?)\s{2,}((?:\d+-\d+|X)(?:\s+(?:\d+-\d+|X))*)\s*',line)
            if m:table.append((int(m[1]),m[2],m[3].split(),number))
    if len(table)!=20 or [r[0] for r in table]!=list(range(1,21)):raise ValueError('RSSSF rows incomplete')
    fixtures=[]
    for index,home,cells,line in table:
        if len(cells)!=20 or cells[index-1]!='X' or cells.count('X')!=1:raise ValueError('RSSSF cell geometry differs')
        for j,score in enumerate(cells):
            if j==index-1:continue
            h,a=score.split('-');fixtures.append(dict(home=home,away=table[j][1],FT=score,hg=h,ag=a,date=None,source_line=line,source_sha256=receipt['sha256'],date_status='UNAVAILABLE',historical_legal_finality='NOT_ESTABLISHED'))
    copyright_block=re.sub('<[^>]+>',' ',text.split('About this document',1)[-1])
    return dict(receipt=receipt,standings_present='Final Table' in text,cross_table_clubs=20,reconstructable_scores=len(fixtures),dated_fixtures=0,round_dates_present=False,fixture_dates_present=False,other_stages_present=False,annotations_in_score_cells=False,fixtures=fixtures,notices=' '.join(copyright_block.split()),scope='Result-only documentary reconstruction; not standardized, not final legal certification; author update date is not a match date')


def build(directory=PRIVATE, root=c.ROOT):
    protected=c.protect(directory,root);manifest=c.verify_originals(directory)
    hr=next(r for r in manifest['files'] if r['repository']==c.HIST);historical=parse_csv((directory/hr['path']).read_bytes(),hr);grouped=defaultdict(list)
    for r in historical:grouped[int(r['season'][:4])].append(r)
    inventory=[]
    for year,rs in sorted(grouped.items()):
        a=assess(rs,year);a['field_issues']=[dict(id=r['audit_id'],issues=r['field_issues']) for r in rs if r['field_issues']];inventory.append(a)
    modern=[]
    for receipt in manifest['files']:
        if receipt['repository']!=c.MODERN:continue
        y=int(receipt['season'][:4]);raw=(directory/receipt['path']).read_bytes()
        if c.sha(raw)!=receipt['sha256']:raise ValueError('Modern hash mismatch')
        rows,notes=parse_text(raw,y,receipt);modern.append(dict(receipt=receipt,records=rows,assessment=assess(rows,y),notes=notes))
    detailed=sorted(set(HISTORICAL_YEARS)|{int(x['receipt']['season'][:4]) for x in modern if int(x['receipt']['season'][:4]) in grouped})
    samples=[dict(season=f'{y}/{y+1}',purpose='APPROVED_SAMPLE' if y in HISTORICAL_YEARS else 'APPROVED_OVERLAP',records=grouped[y],assessment=assess(grouped[y],y)) for y in detailed if y in grouped]
    overlaps=[identity_overlap(grouped[int(x['receipt']['season'][:4])],x['records']) for x in modern if int(x['receipt']['season'][:4]) in grouped]
    rsssf=next((r for r in manifest['files'] if r['repository']=='RSSSF'),None)
    rss=rsssf_capabilities((directory/rsssf['path']).read_bytes(),rsssf) if rsssf else dict(status='RESTRICTED_OR_UNAVAILABLE',details=manifest['blocked'])
    special=[r for x in modern if x['receipt']['season']=='2021/2022' for r in x['records'] if r['home']=='Belenenses SAD' and r['away']=='SL Benfica']
    if len(special)!=1:raise ValueError('Belenenses source selector ambiguous/missing')
    return {
        'feasibility_assessment.json':dict(phase=2,historical=dict(receipt=hr,columns=list(CSV_COLUMNS),total_records=len(historical),earliest_season=min(grouped),latest_season=max(grouped),samples=samples),modern=modern,protected=protected,rights=c.RIGHTS,policy='No match screening, standardization, final match IDs or historical adjudication'),
        'coverage_inventory.json':dict(phase=2,total_records=len(historical),seasons=inventory,unsupported_target_seasons=[f'{y}/{y+1}' for y in range(1990,1994) if y not in grouped],metadata_only_outside_samples=True),
        'overlap_diagnostics.json':dict(phase=2,seasons=overlaps),
        'rsssf_capabilities.json':rss,
        'exception_diagnostics.json':dict(phase=2,belenenses_benfica= dict(original=special[0],actual_completion_date=None,administrative_decision_date=None,effective_availability=None,status='REQUIRES_INDEPENDENT_HISTORICAL_REVIEW; no final disposition'),modern=[dict(season=x['receipt']['season'],wide_rounds=x['assessment']['wide_rounds'],reversals=x['assessment']['source_order_reversals'],unusual_scores=x['assessment']['unusual_scores'],annotations=x['assessment']['annotations']) for x in modern],historical_field_or_label_issues=[dict(season=x['season'],invalid=x['invalid'],field_issues=x['field_issues'],clubs=x['clubs'],expected_clubs=x['expected_clubs'],missing_pairings=x['missing_pairings']) for x in inventory if x['invalid'] or x['field_issues'] or x['clubs']!=x['expected_clubs']],identity_warning='Belenenses/SAD, senior/reserve, Vitoria SC/FC, AVS/Aves and historic successor continuity remain unapproved; literal labels preserved',chronology_warning='2019/20 extended season explicitly allowed; all source dates remain uncertified availability proxies')}


if __name__=='__main__':
    for name,obj in build().items():c.keep(PRIVATE/name,c.encode(obj))
    print('VERIFIED_PHASE2_ASSESSMENTS')
