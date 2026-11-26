"""Authorized Phase 1 recovery: source-bound metadata, no standardized records.

All original bytes and prior phase decisions remain frozen. Exact date conflicts
are quarantined across the compared representations, without choosing a winner.
"""
from collections import Counter, defaultdict
import csv
from datetime import date, datetime
from html import unescape
import io
import json
from pathlib import Path
import re
from scripts import collect_turkish_super_lig_sources as c
from scripts import assess_turkish_super_lig_sources as a

OLD=c.PRIVATE
PRIVATE=OLD.parent/'phase1_followup'
HIST='originals/jalapic/engsoccerdata/data-raw/turkey.csv'
FD='originals/football-data/0607/T1.csv'
RSS='originals/rsssf/tur07.html'
NAMES=('recovery_registry.json','source_feasibility.json','recovery_manifest.json')
# Explicit coeval source labels only, not global club/legal identity aliases.
COEVAL={'Ankaraspor':'Ankaraspor','Galatasaray':'Galatasaray','Kayserispor':'Kayserispor','Trabzonspor':'Trabzonspor','Fenerbahçe':'Fenerbahce','Kayseri Erciyesspor':'Erciyesspor','Erciyesspor':'Erciyesspor','Erciyespor':'Erciyesspor','Gaziantepspor':'Gaziantepspor','Denizlispor':'Denizlispor','Vestel Manisaspor':'Manisaspor','vestel Manisaspor':'Manisaspor','Beşiktaş':'Besiktas','Bursaspor':'Bursaspor','Ankaragücü':'Ankaragucu','Sivasspor':'Sivasspor','Gençlerbirliği':'Genclerbirligi','Antalyaspor':'Antalyaspor','Çaykur Rizespor':'Rizespor','Konyaspor':'Konyaspor','Sakaryaspor':'Sakaryaspor','Malatyaspor':'Malatyaspor','Samsunspor':'Samsunspor','Diyarbakırspor':'Diyarbakirspor'}
MONTHS={n:i+1 for i,n in enumerate('Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split())}


def classify(*,bounded,provenance_ok,privacy_ok,corroborated):
    if not bounded or not provenance_ok or not privacy_ok:return 'SYSTEMIC_BLOCKED'
    return 'RECOVERABLE_SOURCE_ISSUE' if corroborated else 'ISOLATED_QUARANTINE'


def csv_original(raw):
    reader=csv.DictReader(io.StringIO(raw.decode('utf-8-sig'),newline=''),strict=True)
    if tuple(reader.fieldnames or ())!=a.HIST_COLUMNS:raise ValueError('Historical schema mismatch')
    physical=raw.splitlines(keepends=True);result=[]
    for row in reader:
        if None in row or any(v is None for v in row.values()):raise ValueError('Historical row width')
        result.append(dict(fields=row,line=reader.line_num,physical_sha256=c.sha(physical[reader.line_num-1])))
    return result


def direct_rows(raw):
    reader=csv.DictReader(io.StringIO(raw.decode('iso-8859-1'),newline=''),strict=True);out=[];physical=raw.splitlines(keepends=True)
    if not {'Div','Date','HomeTeam','AwayTeam','FTHG','FTAG'}<=set(reader.fieldnames or ()):raise ValueError('Direct schema')
    for row in reader:
        padding=row.pop(None,[])
        annex=(len(padding)==8 and padding[0]=='' and padding[1:3]==[row.get('HomeTeam'),row.get('AwayTeam')]
               and all(re.fullmatch(r'0|[1-9]\d*',v) for v in padding[3:5])
               and padding[5:]==['','','Abandoned'])
        if (any(value.strip() for value in padding) and not annex) or any(v is None for v in row.values()) or row['Div']!='T1':raise ValueError('Direct shape/division')
        d=datetime.strptime(row['Date'],'%d/%m/%Y').date()
        if not date(2006,7,1)<=d<=date(2007,6,30):raise ValueError('Direct source season')
        out.append(dict(home=row['HomeTeam'],away=row['AwayTeam'],hg=row['FTHG'],ag=row['FTAG'],date=d.isoformat(),line=reader.line_num,physical_sha256=c.sha(physical[reader.line_num-1]),raw_fields=row,extra_source_columns=padding,annex_kind='ABANDONMENT_CONTEXT_NOT_RESULT_ADJUDICATION' if annex else 'EMPTY_PADDING' if padding else None))
    return out


def rsssf_rows(raw,year):
    if f'<TITLE>Turkey {year}/{(year+1)%100:02}</TITLE>'.encode() not in raw:raise ValueError('RSSSF season title')
    if b'You are free to copy this document' not in raw:raise ValueError('RSSSF copying grant')
    out=[];notes=[];active=False;current=None;rnd=None
    for lineno,physical in enumerate(raw.splitlines(keepends=True),1):
        text=unescape(re.sub(r'<[^>]+>','',physical.decode('iso-8859-2'))).strip()
        if not active:
            if re.fullmatch(r'Round 1\s*',text):active=True
            else:continue
        if text=='Final Table:':break
        rm=re.match(r'^Round (\d+)(.*)$',text)
        if rm:
            rnd=int(rm[1]);current=None;text=rm[2].strip()
            if not text or text.startswith('- played'):continue
        dm=re.fullmatch(r'\[([A-Z][a-z]{2}) (\d{1,2})\]',text)
        if dm:
            month=MONTHS[dm[1]];current=date(year if month>=7 else year+1,month,int(dm[2])).isoformat();continue
        # Parse the source's awarded number separately from an ordinary FT.
        awarded=re.fullmatch(r'(.+?)\s+awd\s+(.+?)\s+\[awarded (\d+)-(\d+);.*',text)
        ordinary=re.fullmatch(r'(.+?)\s+(\d+)-(\d+)\s+(.+?)(?:\s{2,}.*)?',text.split(' [')[0])
        if awarded:
            h,aw,hg,ag=awarded.groups();kind='SOURCE_AWARDED_NUMBER_NOT_PLAYED_STATUS_DECISION'
        elif ordinary:
            h,hg,ag,aw=ordinary.groups();kind='SOURCE_REPORTED_SCORE'
        else:
            if text:notes.append(dict(line=lineno,text=text))
            continue
        if h not in COEVAL or aw not in COEVAL:
            notes.append(dict(line=lineno,text=text,reason='UNMAPPED_LABEL_NO_GUESSED_IDENTITY'));continue
        if current is None or rnd is None:raise ValueError('RSSSF fixture lacks exact context')
        out.append(dict(home=COEVAL[h],away=COEVAL[aw],hg=hg,ag=ag,date=current,round=rnd,line=lineno,physical_sha256=c.sha(physical),raw_home=h,raw_away=aw,kind=kind))
    if not active:raise ValueError('RSSSF top-flight section missing')
    return out,notes


def unique_pairs(rows):
    result={}
    for r in rows:
        pair=r['home'],r['away']
        if pair in result:raise ValueError('Ambiguous repeated pairing within scoped regular season')
        result[pair]=r
    return result


def recover(historical,fd,rsssf,previous):
    f=unique_pairs(fd);r=unique_pairs(rsssf);review=[];first=[]
    season=[h for h in historical if h['fields']['Season']=='2006']
    if len(season)!=306 or len(fd)!=306 or len(rsssf)!=306:raise ValueError('Scoped population changed')
    for h in season:
        z=h['fields'];pair=z['home'],z['visitor'];fr=f.get(pair);rr=r.get(pair)
        if fr is None or rr is None:raise ValueError('Unbound scoped fixture')
        if (z['hgoal'],z['vgoal'])!=(fr['hg'],fr['ag']) or (fr['hg'],fr['ag'])!=(rr['hg'],rr['ag']):raise ValueError('Unexpected score disagreement; inspect expanded scope')
        if z['Date']>= '2006-07-01':
            if not z['Date']==fr['date']==rr['date']:raise ValueError('Uncontained first-half source disagreement')
            first.append(h['line']);continue
        # This exact source defect is bounded by Season, physical row and all
        # three matching fixture scores/participants, never dates alone.
        upstream_year_evidence=str(int(z['Date'][:4])+1)+z['Date'][4:]
        if upstream_year_evidence!=fr['date']:raise ValueError('Different date defect requires explicit containment')
        agrees=fr['date']==rr['date'];issue=classify(bounded=True,provenance_ok=True,privacy_ok=True,corroborated=agrees)
        prev=[dict(line=p['line'],date=p['date']) for p in previous if (p['home'],p['away'],p['hg'],p['ag'])==(z['home'],z['visitor'],z['hgoal'],z['vgoal'])]
        review.append(dict(source_line=h['line'],physical_sha256=h['physical_sha256'],original_fields=z,source_season='2006/2007',issue_class=issue,action='DERIVED_DATE_CORRECTION' if agrees else 'QUARANTINE_ALL_COMPARED_REPRESENTATIONS',derived_date=rr['date'] if agrees else None,derived_season='2006/2007' if agrees else None,football_result_decision=None,fd=fr,rsssf=rr,previous_season_same_pair_score_coincidences=prev,reason='Unique directed fixture/score matches in two2006/07originals;exactdateagreement' if agrees else 'Season/pair/score agree,but exactdates differ;no automatic source preference',independence='RSSSF distinct attributed compilation;no Football-Data citation observed in acquired top-flight section;fully independent upstream lineage not established. FD/engsoccerdata are upstream/derivative,not independent votes.'))
    if len(review)!=153:raise ValueError('Affected population changed')
    return dict(status='PASS_WITH_ISOLATED_QUARANTINE',scope='Source date/season repair only;not historical match eligibility',affected_records=review,first_half_verified_lines=first,summary=dict(affected=153,season_pair_score_corroborated=153,derived_date_corrected=sum(x['derived_date'] is not None for x in review),quarantined=sum(x['derived_date'] is None for x in review),unchanged_first_half=len(first)),source_name_correspondences=COEVAL)


def apply_metadata(raw,registry):
    if registry.get('source_sha256')!=c.sha(raw):raise ValueError('Repair bound to another original')
    byline={r['source_line']:r for r in registry['affected_records']}
    if len(byline)!=153:raise ValueError('Repair population invalid')
    rows=[];excluded=[];seen=set()
    for h in csv_original(raw):
        z=dict(h['fields']);rule=byline.get(h['line'])
        if rule:
            if rule['physical_sha256']!=h['physical_sha256'] or rule['original_fields']!=z:raise ValueError('Repair input record differs')
            seen.add(h['line'])
            if rule['action']=='QUARANTINE_ALL_COMPARED_REPRESENTATIONS':excluded.append(h['line']);continue
            if rule['action']!='DERIVED_DATE_CORRECTION' or not rule['derived_date']==rule['fd']['date']==rule['rsssf']['date']:raise ValueError('Unsupported correction')
            z['Date']=rule['derived_date']
        rows.append(z)
    if seen!=set(byline):raise ValueError('Repair record missing')
    # Source-schema scratch serialization in memory only. No dataset is written.
    scratch=io.StringIO(newline='');writer=csv.DictWriter(scratch,fieldnames=a.HIST_COLUMNS);writer.writeheader();writer.writerows(rows)
    result=a.csv_summary(scratch.getvalue().encode(),True,season_ends={2019:date(2020,7,26)})
    return result,excluded


def turkish_heading(text,year):
    # Reuse existing weekday/season heading logic, then enforce the Turkish end.
    from scripts.validate_primeira_liga_feasibility import heading
    found=heading(text,year)
    if found and year==2019 and found['date']>'2020-07-26':raise ValueError('Beyond Turkish COVID season end')
    return found


def source_candidates(rows,registry,season):
    """Carry a source-level quarantine across alternatives in the same season."""
    if season!='2006/2007':return list(rows)
    blocked={(r['original_fields']['home'],r['original_fields']['visitor'])
             for r in registry['affected_records']
             if r['action']=='QUARANTINE_ALL_COMPARED_REPRESENTATIONS'}
    return [r for r in rows if (r['home'],r['away']) not in blocked]


def verified_sources(directory):
    receipts=[]
    for base,plans in [(OLD,['source_plan.json','fixture_plan.json','documentary_plan.json']),(directory,['source_plan.json'])]:
        for name in plans:
            plan=c.validate_plan(json.loads((base/name).read_bytes()))
            for item in plan['items']:
                receipt,new=c.acquire(base,item,network=False)
                if new:raise ValueError('Offline replay performed request')
                receipts.append(dict(scope='initial' if base==OLD else 'followup',**receipt))
    return receipts


def build(directory=PRIVATE):
    receipts=verified_sources(directory);raw=(OLD/HIST).read_bytes();historical=csv_original(raw)
    fd=direct_rows((directory/FD).read_bytes());rss,notes=rsssf_rows((directory/RSS).read_bytes(),2006)
    if notes:raise ValueError('Unparsed target RSSSF content')
    prev,previous_notes=rsssf_rows((directory/'originals/rsssf/tur06.html').read_bytes(),2005)
    registry=recover(historical,fd,rss,prev);registry.update(source_sha256=c.sha(raw),comparison_sources={FD:c.sha((directory/FD).read_bytes()),RSS:c.sha((directory/RSS).read_bytes()),'originals/rsssf/tur06.html':c.sha((directory/'originals/rsssf/tur06.html').read_bytes())},previous_season_parser_limits=previous_notes)
    hist,excluded=apply_metadata(raw,registry)
    modern={}
    for receipt in receipts:
        if receipt['path'].endswith('_tr1.txt'):
            y=int(Path(receipt['path']).name[:4]);modern[str(y)]=a.txt_summary((OLD/receipt['path']).read_bytes(),y,date_parser=turkish_heading)
    direct25=a.csv_summary((OLD/'originals/football-data/2526/T1.csv').read_bytes(),False)
    quarantine_pairs={(r['original_fields']['home'],r['original_fields']['visitor']) for r in registry['affected_records'] if r['action']=='QUARANTINE_ALL_COMPARED_REPRESENTATIONS'}
    safe_fd=source_candidates(fd,registry,'2006/2007');safe_rss=source_candidates(rss,registry,'2006/2007')
    if len(safe_fd)!=296 or len(safe_rss)!=296 or hist['2006']['dated_scored']!=296:raise ValueError('Quarantine not contained across representations')
    matrix=[]
    for y in range(1990,2026):
        h=hist.get(str(y));o=modern.get(str(y));d=direct25.get(str(y));rawcount=sum(r['fields']['Season']==str(y) for r in historical)
        matrix.append(dict(season=f'{y}/{y+1}',historical_raw_rows=rawcount,historical_source_usable=h,openfootball=o,direct_2025=d,quarantined_source_fixtures=10 if y==2006 else 0,derived_date_corrections=143 if y==2006 else 0,source_gap=not any([h,o,d]),stage_or_historical_acceptance='NOT_ADJUDICATED_PHASE1',additional_2006_sources=dict(football_data_raw=len(fd),rsssf_scored_descriptions=len(rss),usable_each_after_quarantine=296) if y==2006 else None))
    feasibility=dict(status='PASS_WITH_ISOLATED_QUARANTINE',coverage=matrix,original_network_count=len(receipts),new_original_count=3,old_original_count=23,quarantine_propagation=dict(historical_lines=excluded,fixture_pairs=[list(p) for p in sorted(quarantine_pairs)],fd_excluded_lines=[r['line'] for r in fd if (r['home'],r['away']) in quarantine_pairs],rsssf_excluded_lines=[r['line'] for r in rss if (r['home'],r['away']) in quarantine_pairs]),rsssf_old_documentary_context={name:a.rsssf_summary((OLD/f'originals/rsssf/{name}.html').read_bytes(),name) for name in ['tur91','tur92','tur93','tur94','tur2012','tur2023','tur2026']},limitations=['Fourearlyseasonsremainexactdatedsourcegaps','2011/12playoffsnotcomplete','2009/10omissionsnotadjudicated','Modernawardsandunscoredslotsnotacceptedfootballresults','RSSSFunderlyingindependencenotfullyestablished','NoTFFretryoradditionalFDdownloadsauthorizedafterthisplan'],source_usable_historical_total=sum(x['dated_scored'] for x in hist.values()),source_raw_historical_total=len(historical))
    manifest=dict(phase=1,files=[dict(scope=r['scope'],path=r['path'],url=r['url'],sha256=r['sha256'],bytes=r['bytes'],retrieved_at_utc=r['retrieved_at_utc'],licensing=r['licensing']) for r in receipts],originals_private=True,prior_initial_phase_status_preserved='BLOCKED record remains as historical evidence;superseded by approvedfollowup containment',policy='Retrospective originalfootball dates and acceptedfinalresults;no administrativepublicationdate filtering;no match dispositions decided')
    return {NAMES[0]:c.encode(registry),NAMES[1]:c.encode(feasibility),NAMES[2]:c.encode(manifest)}


if __name__=='__main__':
    import argparse
    import tempfile
    parser=argparse.ArgumentParser();parser.add_argument('--verify',action='store_true');parser.add_argument('--output-dir',type=Path);args=parser.parse_args();artifacts=build()
    dest=args.output_dir or PRIVATE
    allowed=(PRIVATE,Path(tempfile.gettempdir()),Path('/private/tmp'))
    if not any(dest.resolve().is_relative_to(p.resolve()) for p in allowed):
        raise ValueError('Recovery artifacts must remain private or in temporary storage')
    for name,raw in artifacts.items():
        if args.verify:
            if (dest/name).read_bytes()!=raw:raise ValueError('Reproduction differs: '+name)
        else:c.save(dest/name,raw)
    print(('VERIFIED' if args.verify else 'SAVED'),'Phase1recovery metadata and aggregate coverage;143datecorrections,10quarantined;no standardizedrecords')
