"""Belgian Phase 2 only: lossless source inventory, stage/overlap diagnostics.

No screening, final match IDs, historical corrections or global club aliases.
Unknown TXT grammar fails; historical stage remains UNKNOWN without source labels.
"""
from collections import Counter, defaultdict
from datetime import date
from html import unescape
from pathlib import Path
import calendar, csv, io, json, re, tempfile
from scripts import collect_belgian_pro_league_feasibility as c
from scripts import validate_primeira_liga_feasibility as shared
from scripts.validate_ligue2_structure import fixture

NAMES=('historical_findings.json','modern_findings.json','stage_diagnostics.json','overlap_findings.json','rsssf_capabilities.json','coverage_matrix.json','provenance_manifest.json')
CSV_COLUMNS=shared.CSV_COLUMNS


def expected_clubs(year):
    return 18 if year<=2008 or 2020<=year<=2022 else 16


def parse_csv(raw,receipt):
    # Reuse the lossless field checks with the Belgian competition identifier.
    physical=raw.splitlines(keepends=True)
    reader=csv.DictReader(io.StringIO(raw.decode('utf-8-sig'),newline=''),strict=True)
    if tuple(reader.fieldnames or ())!=CSV_COLUMNS:raise ValueError('Unexpected Belgian historical schema')
    if c.sha(raw)!=receipt['sha256']:raise ValueError('Historical checksum mismatch')
    rows=[]
    while True:
        start=reader.line_num+1
        try:r=next(reader)
        except StopIteration:break
        if None in r or any(v is None for v in r.values()):raise ValueError('Malformed CSV width')
        if not re.fullmatch(r'\d{4}',r['Season']):raise ValueError('Invalid season')
        y=int(r['Season']);issues=[]
        try:
            if date.fromisoformat(r['Date']).isoformat()!=r['Date']:raise ValueError()
        except ValueError:issues.append('INVALID_DATE')
        if r['division']!='B1' or r['tier']!='1':issues.append('WRONG_COMPETITION')
        h,a=r['hgoal'],r['vgoal']
        if not all(re.fullmatch(r'0|[1-9]\d*',v) for v in (h,a)):issues.append('INVALID_SCORE')
        else:
            hi,ai=int(h),int(a)
            if r['FT']!=h+'-'+a:issues.append('FT_CONTRADICTION')
            if r['totgoal']!=str(hi+ai) or r['goaldif']!=str(hi-ai):issues.append('GOAL_DERIVED_CONTRADICTION')
            if r['result']!=('H' if hi>ai else 'A' if hi<ai else 'D'):issues.append('OUTCOME_CONTRADICTION')
        fields=dict(season=f'{y}/{y+1}',date=r['Date'],home=r['home'],away=r['visitor'],hg=h or None,ag=a or None,FT=r['FT'] or None,HT=None,annotation='',round=None,stage='UNKNOWN',group=None,leg=None,original_fields=r,field_issues=issues,date_basis='EXPLICIT_ISO_DATE',date_semantics='SOURCE_DATE_NOT_VERIFIED_RESULT_AVAILABILITY')
        rows.append(shared.bound(fields,receipt,start,reader.line_num,b''.join(physical[start-1:reader.line_num])))
    if not rows:raise ValueError('Empty historical original')
    return rows


def diagnostic_identity(r):
    """Private diagnostic only; physical source identity remains separately bound."""
    return [r['season'],'Belgian Pro League',r['stage'],r.get('group'),r.get('round'),r.get('leg'),r['date'],r['home'],r['away']]


def parse_text(raw,year,receipt):
    if c.sha(raw)!=receipt['sha256']:raise ValueError('TXT checksum mismatch')
    rows=[];notes=[];current=None;stage=None;rnd=None;title=False;physical=raw.splitlines(keepends=True)
    stages={'Playoff I':'CHAMPIONSHIP','Championship':'CHAMPIONSHIP','Europe':'EUROPE','Relegation':'PLAYDOWNS','ECL Playoff':'EUROPE_QUALIFICATION'}
    for number,line in enumerate(raw.decode('utf-8-sig').splitlines(),1):
        text=line.strip()
        if not text:continue
        if text.startswith('#'):notes.append(dict(line=number,kind='COMMENT',text=text));continue
        if text.startswith('='):
            if title or text!=f'= Belgium First Division A {year}/{(year+1)%100:02}':raise ValueError('Wrong/duplicate title')
            title=True;notes.append(dict(line=number,kind='TITLE',text=text));continue
        if text.startswith('▪'):
            m=re.fullmatch(r'▪ (?:(Playoff I|Championship|Europe|Relegation), )?(?:Matchday (\d+)|(\d+)\. Round)',text)
            if m:
                stage=stages[m[1]] if m[1] else 'REGULAR_SEASON';rnd=int(m[2] or m[3])
                if not 1<=rnd<=(30 if stage=='REGULAR_SEASON' else 10):raise ValueError('Round outside source format')
            elif text=='▪ ECL Playoff, Final':stage='EUROPE_QUALIFICATION';rnd='Final'
            else:raise ValueError(f'Unknown stage heading at {number}: {text}')
            current=None;notes.append(dict(line=number,kind='STAGE_ROUND',stage=stage,round=rnd,text=text));continue
        parsed=shared.heading(text,year)
        if parsed:current=dict(parsed,heading_line=number);continue
        if not title or stage is None or current is None:raise ValueError(f'Fixture without context at {number}')
        body=re.sub(r'^\d{1,2}:\d{2}\s+','',text);r=fixture(body)
        r.update(season=f'{year}/{year+1}',date=current['date'],date_basis=current['date_basis'],date_heading=current['date_heading'],date_heading_line=current['heading_line'],date_semantics='SOURCE_HEADING_NOT_RESULT_AVAILABILITY_CERTIFICATION',stage=stage,round=rnd,group=None,leg=None,raw_record=line,field_issues=[])
        rows.append(shared.bound(r,receipt,number,number,physical[number-1]))
    if not title or not rows:raise ValueError('Empty/incomplete TXT original')
    # Comments are diagnostic assertions, not inputs driving fixture classification.
    declared=next((int(m[1]) for n in notes if (m:=re.fullmatch(r'# Matches\s+(\d+)',n['text']))),None)
    return rows,dict(notes=notes,declared_matches=declared,declared_count_matches=declared==len(rows))


def assess(rows,year):
    names=sorted({r[k] for r in rows for k in ('home','away')});pairs=defaultdict(list);ids=defaultdict(list);rounds=defaultdict(list);invalid=[]
    for r in rows:
        pairs[r['home'],r['away']].append(r);ids[json.dumps(diagnostic_identity(r),ensure_ascii=False)].append(r)
        if r['round'] is not None:rounds[r['stage'],str(r['round'])].append(r)
        issues=list(r['field_issues'])
        if r['home']==r['away'] or any(not r[k] or r[k]!=r[k].strip() or '\ufffd' in r[k] for k in ('home','away')):issues.append('INVALID_TEAM')
        try:
            d=date.fromisoformat(r['date'])
            if not date(year,7,1)<=d<=date(year+1,6,30):issues.append('OUTSIDE_SEASON')
        except ValueError:issues.append('INVALID_DATE')
        if (r['hg'] is None)!=(r['ag'] is None):issues.append('PARTIAL_SCORE')
        if issues:invalid.append(dict(source_id=r['audit_id'],issues=sorted(set(issues))))
    wide=[]
    for (stage,rnd),rs in sorted(rounds.items()):
        first=min(r['date'] for r in rs);last=max(r['date'] for r in rs);span=(date.fromisoformat(last)-date.fromisoformat(first)).days
        if span>14:wide.append(dict(stage=stage,round=rnd,earliest=first,latest=last,span_days=span,source_ids=[r['audit_id'] for r in rs]))
    duplicate_pairs=[dict(home=h,away=a,source_ids=[r['audit_id'] for r in rs],stages=[r['stage'] for r in rs],dates=[r['date'] for r in rs],kind='CROSS_STAGE_REPEAT' if len({r['stage'] for r in rs})>1 else 'REQUIRES_REVIEW') for (h,a),rs in sorted(pairs.items()) if len(rs)>1]
    n=expected_clubs(year)
    prefix=rows[:len(names)*(len(names)-1)]
    prefix_complete=len(prefix)==len(names)*(len(names)-1) and len({(r['home'],r['away']) for r in prefix})==len(prefix) and all(r['home']!=r['away'] for r in prefix)
    provisional=dict(basis='FIRST_COMPLETE_DIRECTED_PAIR_PREFIX_NOT_FINAL_STAGE_POLICY',candidate_regular=len(prefix) if prefix_complete else None,additional_observations=len(rows)-len(prefix) if prefix_complete else None,source_stage_unchanged=True)
    return dict(provisional_pairing_partition=provisional,season=f'{year}/{year+1}',observed=len(rows),scored=sum(r['hg'] is not None for r in rows),unscored=sum(r['hg'] is None for r in rows),explicit_cancelled=sum('cancelled' in r['annotation'].lower() for r in rows),expected_clubs=n,nominal_regular_slots=n*(n-1),clubs=len(names),team_labels=names,directed_pairs=len(pairs),missing_directed_pairs_relative_to_observed_clubs=[[h,a] for h in names for a in names if h!=a and (h,a) not in pairs],pairing_scope='Apply regular-pair expectations only to regular or provisional historical subset; not all-stage total',stage_counts=dict(sorted(Counter(r['stage'] for r in rows).items())),date_range=[min(r['date'] for r in rows),max(r['date'] for r in rows)],invalid=invalid,pairing_repeats=duplicate_pairs,duplicate_diagnostic_identities=[dict(identity=json.loads(k),source_ids=[r['audit_id'] for r in rs]) for k,rs in sorted(ids.items()) if len(rs)>1],wide_rounds=wide,annotations=[dict(source_id=r['audit_id'],annotation=r['annotation']) for r in rows if r['annotation']],source_order_reversals=[dict(previous_id=a['audit_id'],current_id=b['audit_id']) for a,b in zip(rows,rows[1:]) if b['date']<a['date']],unusual_scores=[dict(source_id=r['audit_id'],FT=r['FT']) for r in rows if all(isinstance(r[k],str) and r[k].isdigit() for k in ('hg','ag')) and (max(int(r['hg']),int(r['ag']))>=7 or int(r['hg'])+int(r['ag'])>=10)],status='INVENTORY_ONLY_NOT_HISTORICALLY_CERTIFIED',availability='UNVERIFIED')


def overlap(historical,modern):
    """Season-bound candidate labels inferred from event signatures, never aliases."""
    seasons={r['season'] for r in historical+modern}
    if len(seasons)!=1:raise ValueError('Overlap must be season-bound')
    regular=[r for r in modern if r['stage']=='REGULAR_SEASON']
    def signatures(rows):
        d=defaultdict(set)
        for r in rows:
            if r['FT'] is not None:
                d[r['home']].add((r['date'],'HOME',r['FT']));d[r['away']].add((r['date'],'AWAY',r['FT']))
        return d
    hs,ms=signatures(historical),signatures(modern);proposals={};details=[]
    for modern_name,sig in sorted(ms.items()):
        candidates=[(len(sig&other)/min(len(sig),len(other)),name) for name,other in hs.items()]
        candidates.sort(reverse=True)
        if candidates and candidates[0][0]>=0.8 and (len(candidates)==1 or candidates[0][0]>candidates[1][0]):
            quality,name=candidates[0];proposals[modern_name]=name;details.append(dict(modern=modern_name,historical=name,signature_agreement=quality,status='SEASON_BOUND_DIAGNOSTIC_CANDIDATE_NOT_IDENTITY_CERTIFICATION'))
    if len(set(proposals.values()))!=len(proposals):raise ValueError('Ambiguous label correspondence')
    left=defaultdict(list);right=defaultdict(list)
    for r in historical:left[r['home'],r['away']].append(r)
    for r in modern:
        if r['home'] in proposals and r['away'] in proposals:right[proposals[r['home']],proposals[r['away']]].append(r)
    comparisons=[];matched_h=set();matched_m=set();ambiguous=[]
    for key in sorted(left.keys()&right.keys()):
        # Pair+date resolves rematches; scores are compared, not used to force equality.
        for h in left[key]:
            candidates=[m for m in right[key] if m['date']==h['date']]
            if len(candidates)!=1:
                candidates=right[key] if len(left[key])==len(right[key])==1 else []
            if len(candidates)!=1:
                ambiguous.append(dict(pair=list(key),historical_id=h['audit_id']));continue
            m=candidates[0]
            if m['audit_id'] in matched_m:raise ValueError('Overlap event reused')
            matched_h.add(h['audit_id']);matched_m.add(m['audit_id'])
            comparisons.append(dict(historical_id=h['audit_id'],modern_id=m['audit_id'],modern_stage=m['stage'],historical_stage='UNKNOWN',stage_correspondence='DIAGNOSTIC_ONLY',date_equal=h['date']==m['date'],score_equal=h['FT']==m['FT'],historical_date=h['date'],modern_date=m['date'],historical_FT=h['FT'],modern_FT=m['FT']))
    return dict(historical_observations=len(historical),modern_observations=len(modern),modern_regular=len(regular),candidate_correspondences=details,candidate_event_matches=len(comparisons),matched_modern_stage_counts=dict(Counter(x['modern_stage'] for x in comparisons)),comparisons=comparisons,date_conflicts=sum(not x['date_equal'] for x in comparisons),score_conflicts=sum(not x['score_equal'] for x in comparisons),unmatched_historical=[r['audit_id'] for r in historical if r['audit_id'] not in matched_h],unmatched_modern=[r['audit_id'] for r in modern if r['audit_id'] not in matched_m],unmatched_modern_regular=[r['audit_id'] for r in regular if r['audit_id'] not in matched_m],postseason_not_matched=[r['audit_id'] for r in modern if r['stage']!='REGULAR_SEASON' and r['audit_id'] not in matched_m],ambiguous_pairings=ambiguous,independence='UNESTABLISHED; agreement is not independent historical proof')



def rsssf(raw,receipt):
    text=raw.decode(receipt['encoding']);lines=text.splitlines();physical=raw.splitlines(keepends=True);sections=[];fixtures=[];round_id=None;day=None;stage='UNKNOWN';in_top=False;date_line=None
    for number,literal in enumerate(lines,1):
        s=unescape(re.sub('<[^>]+>','',literal)).strip()
        if '<a name="reg">Regular Stage' in literal:in_top=True;stage='REGULAR_SEASON'
        if '<h4>' in literal.lower() and 'name="pro"' not in literal.lower():in_top=False
        if '<a name="2play">Promotion/Relegation Playoff' in literal:in_top=True;stage='CROSS_DIVISION';day=None;sections.append(dict(line=number,text=s,stage=stage))
        if not in_top:continue
        if re.search(r'Championship Playoff|Playoff II|Group [AB]|Europa League Playoff|Euro League Playoff|^Final$',s) and len(s)<70:
            if 'Championship' in s:stage='CHAMPIONSHIP'
            elif 'Playoff II' in s:stage='EUROPE'
            elif 'Group' in s:stage='EUROPE_'+s[-1]
            elif 'Europa League' in s or 'Euro League' in s:stage='EUROPE_QUALIFICATION'
            elif s=='Final':stage='EUROPE_GROUP_FINAL'
            sections.append(dict(line=number,text=s,stage=stage));day=None
        m=re.match(r'Round (\d+)',s)
        if m:round_id=int(m[1]);day=None
        if re.search(r'\[(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d',s):day=s;date_line=number
        note=re.search(r'\s+(\[.*)$',s)
        body=s[:note.start()] if note else s
        m=re.fullmatch(r'(.+?)\s+(\d+-\d+|awd|n/p)\s+(.+)',body)
        if m and s[0].isalpha() and not m[3][0].isdigit() and not s.startswith(('NB:', 'record at exclusion:')):
            home,score,away=m.groups();annotation=note[1] if note else ''
            fixtures.append(dict(line=number,source_line_sha256=c.sha(physical[number-1]),stage=stage,round=round_id,date_heading=day,date_heading_line=date_line,home=home,away=away,score=score,annotation=annotation,date_semantics='HEADING_CONTEXT_NOT_CERTIFIED_ACTUAL_DATE',raw_text=s))
    title=re.search(r'<title>(.*?)</title>',text,re.I|re.S)
    return dict(title=title[1] if title else None,encoding=receipt['encoding'],source_sha256=receipt['sha256'],sections=sections,fixture_line_candidates=fixtures,fixture_candidates=len(fixtures),stage_counts=dict(Counter(r['stage'] for r in fixtures)),score_token_counts=dict(Counter('NUMERIC' if re.fullmatch(r'\d+-\d+',r['score']) else r['score'] for r in fixtures)),notices=[dict(line=i,text=unescape(re.sub('<[^>]+>','',line)).strip()) for i,line in enumerate(lines,1) if re.search('copyright|acknowledg|author:|prepared|updated|annulled|excluded|forfeit',line,re.I)],standings_only=not fixtures,limitations='Candidate documentary extraction, not imported match data; no invented fixture dates or final dispositions')


def build(directory=c.PRIVATE):
    manifest=c.verify_originals(directory);historical=[];modern={};grammar={};documents={}
    for rec in manifest['files']:
        raw=(directory/rec['path']).read_bytes()
        if rec['repository']==c.HIST:historical=parse_csv(raw,rec)
        elif rec['repository']==c.MODERN:
            year=int(rec['season'][:4]);modern[year],grammar[year]=parse_text(raw,year,rec)
        else:documents[rec['original_path']]=rsssf(raw,rec)
    by=defaultdict(list)
    for r in historical:by[int(r['season'][:4])].append(r)
    history={str(y):assess(rs,y) for y,rs in sorted(by.items())};modern_results={str(y):dict(all_stages=assess(rs,y),regular=assess([r for r in rs if r['stage']=='REGULAR_SEASON'],y),grammar=grammar[y],observations=rs) for y,rs in sorted(modern.items())}
    matrix=[]
    for y in range(1990,2026):
        h=history.get(str(y));m=modern_results.get(str(y));n=expected_clubs(y)
        matrix.append(dict(season=f'{y}/{y+1}',expected_clubs=n,nominal_slots=n*(n-1),historical=h,modern=dict(all_stages=m['all_stages'],regular=m['regular']) if m else None,stage_scope='Historical UNKNOWN (regular-only documentation claim); modern headings explicit',rights='NOT_CLEARED_FOR_TRAINING_OR_REDISTRIBUTION',historical_date_completeness='SOURCE_DATES_ONLY' if h else 'NO_ACQUIRED_DATED_SOURCE',special_context={2002:'Lommel nominal 306 versus final-table 272; no dispositions',2008:'Title test separate; assess repeated pairs',2009:'Mouscron nominal 240 versus final-table 210; no dispositions',2019:'COVID: played versus explicitly cancelled source slots'}.get(y)))
    overlap_results={str(y):overlap(by[y],rs) if by.get(y) else dict(historical_observations=0,modern_observations=len(rs),status='NO_HISTORICAL_OVERLAP') for y,rs in sorted(modern.items())}
    outputs=dict(zip(NAMES,[dict(schema=list(CSV_COLUMNS),observed=len(historical),seasons=history,observations=historical),modern_results,dict(historical_repeats={y:h['pairing_repeats'] for y,h in history.items() if h['pairing_repeats']},modern_repeats={y:m['all_stages']['pairing_repeats'] for y,m in modern_results.items()},identity_fields=['season','competition','stage','group','round','leg','source_date','home','away'],source_identity='source SHA256 plus physical line range; diagnostic identity is not final match_id'),overlap_results,documents,matrix,dict(phase=2,originals=manifest['files'],blocked=manifest['blocked'],canonical_league='Belgian Pro League',policy='NO_SCREENING_NO_FINAL_IDS_NO_HISTORICAL_DISPOSITIONS',rights=c.RIGHTS)]))
    return outputs


def generate(directory=c.PRIVATE,output=None):
    output=Path(output) if output else directory/'phase2';outputs=build(directory)
    for name,obj in outputs.items():c.keep(output/name,c.encode(obj))
    hashes={name:c.sha(c.encode(obj)) for name,obj in outputs.items()}
    c.keep(output/'reproducibility.json',c.encode(dict(artifacts=hashes)))
    return hashes


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);a=p.parse_args();print(generate(output=a.output))
