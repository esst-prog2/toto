"""Lossless source adapters for the private UEFA Cup/Europa League Phase 2.

No historical acceptance or canonical match output. Unsupported candidates are
explicit records, never silently dropped. Shared UCL score grammar is reused.
"""
from collections import Counter, defaultdict
from datetime import date, datetime
import csv
import html
import io
import json
from pathlib import Path
import re
import unicodedata
import zipfile
from scripts.inventory_uefa_champions_league import txt_periods, label
from scripts.acquire_uefa_europa_league import sha, encode

PERIODS=('regulation_time','half_time','after_extra_time','extra_time_only','shootout','aggregate','published_final','administrative_result')
COUNTRIES='Fni Mal Grk Hon SeM SMr Mon Ice Bih Alb And Arm Aut Aze Azb Bel Blr Bls Bos BiH Bul Cro Cyp Cze Den Eng Esp Est Far Fin Fra FRG GDR Geo Ger Gib Gre Hun Ire Irl Isl Isr Ita Kaz Kos Lat Lie Lit Ltu Lux Lva Mac Mda Mkd Mlt Mol Mne Mng Ned Net Nil Nir Nor Pol Por Rom Rou Rus Sco Ser SMa SMR Slo Sln Srb Sui Svk Swe Tch Tur Ukr URS Wal Yug'.split()
COUNTRY_RE='(?:'+'|'.join(COUNTRIES)+')'
MONTHS={m.lower():i for i,m in enumerate(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],1)}


def pair(s):
    m=re.search(r'(?<!\d)(\d+)\s*[-–:]\s*(\d+)(?!\d)',str(s))
    return [int(m[1]),int(m[2])] if m else None


def periods(**kw):return {k:kw.get(k) for k in PERIODS}


def text(raw):
    try:return raw.decode('utf-8-sig')
    except UnicodeDecodeError:return raw.decode('cp1252',errors='replace')


def plain(s):
    return html.unescape(re.sub(r'<[^>]*>','',s)).replace('\xa0',' ')


def team_key(s):
    """A candidate name key, never a global/legal club identity assertion."""
    s=re.sub(r"[()]",' ',s).replace('Ł','L').replace('ł','l').replace('ø','o').replace('Ø','O').replace('đ','d').replace('Đ','D').replace('ß','ss')
    s=''.join(c for c in unicodedata.normalize('NFKD',s.casefold()) if not unicodedata.combining(c))
    tokens=re.findall(r'[a-z0-9]+',s)
    # Club designators only; geographic/core words are not deleted.
    while len(tokens)>1 and tokens[0] in {'fc','fk','sc','nk','ac','as','afc','cf','rsc','ks','sk','ssc','rc','cd','ud','sd','bk','fk','fsv','vfb','vfl'}:tokens.pop(0)
    while len(tokens)>1 and tokens[-1] in {'fc','fk','sc','cf','afc'}:tokens.pop()
    return ' '.join(tokens)


def season_of(y):return f'{int(y)}/{int(y)+1}'


def parse_day(s,year=None):
    s=plain(str(s)).strip()
    if s.startswith('[') and s.endswith(']'):s=s[1:-1].strip()
    iso=re.search(r'\b(19\d\d|20\d\d)-(\d\d)-(\d\d)\b',s)
    if iso:
        try:return date(*map(int,iso.groups())).isoformat()
        except ValueError:return None
    start=re.search(r'\{\{[Ss]tart date\|(?:df=[^|]+\|)?(\d{4})\|(\d{1,2})\|(\d{1,2})',s)
    if start:
        try:return date(*map(int,start.groups())).isoformat()
        except ValueError:return None
    m=re.search(r'\b(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})\b',s)
    if m:
        try:return date(int(m[3]),MONTHS[m[2][:3].lower()],int(m[1])).isoformat()
        except (ValueError,KeyError):return None
    m=re.search(r'\b([A-Z][a-z]{2})\s+(\d{1,2})(?:,?\s+(\d{4}))?\b',s)
    if m and (m[3] or year is not None):
        month=MONTHS.get(m[1].lower())
        if month:
            y=int(m[3]) if m[3] else year+(month<6)
            try:return date(y,month,int(m[2])).isoformat()
            except ValueError:return None
    return None


def stage(year,raw,*,qualifier=False,when=None):
    s=raw.casefold().replace('-',' ').replace('1/8','round of 16').replace('1/16','round of 32')
    # Season-specific historical naming: RSSSF 2021+ "First Round" is the
    # summer qualifying play-off, unlike the UEFA Cup first main round.
    qualifying=qualifier or bool(re.search(r'\bqualif(?:ying|ication)\b|\bprelim',s))
    if year>=2009 and s.strip().startswith('first round'):qualifying=True
    if any(t in s for t in ['play off round','playoff round','playoff']) and when and int(when[5:7]) in (6,7,8):qualifying=True
    if qualifying:
        if 'prelim' in s:return 'QUALIFYING','PRELIMINARY'
        if 'play' in s or (year>=2009 and s.strip().startswith('first round')):return 'QUALIFYING','QUALIFYING_PLAYOFF'
        words={'first':1,'second':2,'third':3,'fourth':4,'1st':1,'2nd':2,'3rd':3,'4th':4}
        n=next((v for k,v in words.items() if re.search(r'\b'+k+r'\b',s)),None)
        if n is None:
            m=re.search(r'(?:round|phase)\s+(\d)|(\d)\.\s*round',s);n=int(next(v for v in m.groups() if v)) if m else None
        if n is None and year<=2003:n=1
        if n is None and year>=2021:n=3
        if n==4 and year>=2009:return 'QUALIFYING','QUALIFYING_PLAYOFF'
        return 'QUALIFYING','QUALIFYING_ROUND_'+str(n or 'UNKNOWN')
    if 'league phase' in s or s.startswith('league,'):return 'MAIN','LEAGUE_PHASE'
    if 'group' in s:return 'MAIN','GROUP_STAGE'
    for keys,value in [(['quarter','1/4'],'QUARTERFINAL'),(['semi','1/2'],'SEMIFINAL'),(['round of 32'],'ROUND_OF_32'),(['round of 16'],'ROUND_OF_16')]:
        if any(k in s for k in keys):return 'MAIN',value
    if re.search(r'(?:^|,)\s*final(?:\s*\(|$)',s) or s.startswith('final,') or 'cup final' in s or s.startswith('final (') or s.startswith('final 1st') or s.startswith('final 2nd'):return 'MAIN','FINAL'
    if 'intermediate' in s:return 'MAIN','ROUND_OF_32' if year<=2020 else 'KNOCKOUT_PLAYOFF'
    if 'knockout' in s or 'play' in s:return 'MAIN','KNOCKOUT_PLAYOFF'
    words={'first':1,'second':2,'third':3,'fourth':4,'1st':1,'2nd':2,'3rd':3,'4th':4}
    n=next((v for k,v in words.items() if re.search(r'\b'+k+r'\b',s)),None)
    if re.search(r'\bround\b',s) and n:
        if year>=2009 and n==2:return 'MAIN','ROUND_OF_32'
        if year>=2009 and n==3:return 'MAIN','ROUND_OF_16'
        if 1999<=year<=2008 and n==3:return 'MAIN','ROUND_OF_32'
        if 1999<=year<=2008 and n==4:return 'MAIN','ROUND_OF_16'
        if year<=1998 and n==3:return 'MAIN','ROUND_OF_16'
        return 'MAIN','ROUND_'+str(n)
    # OpenFootball headings "Finals, Round of 16" handled above; its numbered
    # summer rounds are only qualifying when the file itself declares Quali.
    return 'UNKNOWN','UNKNOWN'


def observation(rec,locator,season,home,away,*,raw_fields,when=None,interval=None,raw_date='',raw_stage='',p=None,leg=None,replay=False,kind='fixture',status='published',issues=(),qualifier=False,venue=None,neutral=None,associations=None):
    year=int(season[:4]);scope,st=stage(year,raw_stage,qualifier=qualifier,when=when)
    replay=replay or bool(re.search(r'\breplay(?:ed)?\b',str(raw_fields.get('raw_line',''))+' '+str(raw_fields.get('status_annotation',''))+' '+str(raw_fields.get('header','')),re.I))
    pp=periods(**(p or {}));flags=list(issues)
    if not when:flags.append('DATE_NOT_EXACT')
    if pp['regulation_time'] is None:flags.append('REGULATION_SCORE_UNKNOWN')
    if st=='UNKNOWN':flags.append('STAGE_UNRESOLVED')
    if any(k in status.casefold() for k in ('award','abandon','cancel','withdraw','walkover','w/o','void','postpon')):flags.append('EXCEPTIONAL_STATUS')
    if when and not date(year,6,1)<=date.fromisoformat(when)<=date(year+1,8,31):flags.append('DATE_OUTSIDE_SEASON_WINDOW')
    for k,v in pp.items():
        if v is not None and (len(v)!=2 or any(not isinstance(g,int) or g<0 for g in v)):raise ValueError('Invalid score period '+k)
    result=dict(observation_id=sha(encode([rec['sha256'],locator])),source=rec['path'],source_sha256=rec['sha256'],publisher=rec['publisher'],locator=locator,season=season,competition='UEFA Cup' if year<2009 else 'UEFA Europa League',original_competition=raw_fields.get('competition_name',raw_fields.get('title','UEFA Cup' if year<2009 else 'UEFA Europa League')),representation=kind,source_fields=raw_fields,raw_home=home,raw_away=away,home=home.strip(' *+\t'),away=away.strip(' *+\t'),team_candidates=[team_key(home),team_key(away)],associations=associations or [None,None],date=when,date_interval=interval,raw_date=raw_date,date_precision='SOURCE_EXACT_DAY' if when else 'SOURCE_INTERVAL_OR_UNAVAILABLE',date_role='SCHEDULED_OR_ADMINISTRATIVE_DAY' if any(v in status.casefold() for v in ('award','cancel','walkover')) else 'SOURCE_REPORTED_DAY_NOT_INDEPENDENTLY_VERIFIED' if when else 'ROUND_SCHEDULE_OR_UNAVAILABLE',raw_stage=raw_stage,scope=scope,stage=st,source_leg=leg,replay=replay,periods=pp,status=status,venue=venue,source_neutral_venue=neutral,official_neutral_candidate=(1 if st=='FINAL' and year>=1997 else 0 if st!='UNKNOWN' else None),neutral_status='FORMAT_CANDIDATE_NOT_ADJUDICATED',field_availability={k:('available' if v is not None else 'unknown' if k in ('regulation_time','published_final') else 'unavailable') for k,v in pp.items()},parsing_status='PARSED_WITH_UNCERTAINTY' if flags else 'PARSED',issues=sorted(set(flags)))
    if pp['regulation_time'] is None and (pp['after_extra_time'] is not None or pp['shootout'] is not None):result['field_availability']['regulation_time']='ambiguous'
    if raw_fields.get('extra_time_played')=='0' or raw_fields.get('full_time')=='F' or st in ('GROUP_STAGE','LEAGUE_PHASE'):
        for field in ('after_extra_time','extra_time_only','shootout'):
            if pp[field] is None:result['field_availability'][field]='not_applicable_by_reported_flag_or_format'
    return result


def exception(rec,locator,code,raw,**kw):return dict(exception_id=sha(encode([rec['sha256'],locator,code])),source=rec['path'],source_sha256=rec['sha256'],locator=locator,code=code,raw=raw,**kw)


def parse_openfootball(raw,rec):
    year=int(Path(rec['path']).parent.name[:4]);season=season_of(year);title=text(raw).splitlines()[0]
    if 'Europa League' not in title or f'{year}/{str(year+1)[-2:]}' not in title:raise ValueError('Incorrect TXT competition/season')
    qualifier='Quali' in title;rows=[];exceptions=[];heading='';day=None;date_raw='';date_line=None
    for n,line in enumerate(text(raw).splitlines(),1):
        s=line.strip()
        if not s or s[0] in '#=':continue
        if s.startswith('▪'):heading=s[1:].strip();day=None;date_raw='';continue
        m=re.fullmatch(r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun) ([A-Za-z]{3}) (\d{1,2})(?: (\d{4}))?',s)
        if m:
            date_raw=s;date_line=n;ds=[]
            for y in [int(m[4])] if m[4] else [year,year+1]:
                d=date(y,MONTHS[m[2].lower()],int(m[3]))
                if date(year,6,1)<=d<=date(year+1,8,31) and d.strftime('%a')==m[1]:ds.append(d.isoformat())
            day=ds[0] if len(ds)==1 else None;continue
        m=re.match(r'(?:\d{1,2}:\d\d\s+)?(.+?)\s+v\s+(.+?\([A-Z]{3}\))\s+(.*)$',s)
        if not m:
            exceptions.append(exception(rec,f'line:{n}','UNSUPPORTED_TXT_CANDIDATE',line));continue
        h,away,token=m.groups();p,issues=txt_periods(token);p['published_final']=p['after_extra_time'] or p['regulation_time'];hn,hc=label(h,'txt');an,ac=label(away,'txt')
        rows.append(observation(rec,f'line:{n}',season,hn,an,raw_fields=dict(raw_line=line,title=title,date_heading_line=date_line,score=token),when=day,raw_date=date_raw,raw_stage=heading,p=p,leg=(int(lm[1] or lm[2]) if (lm:=re.search(r'Leg ([12])|([12])(?:st|nd) Leg',heading,re.I)) else None),issues=issues,qualifier=qualifier,associations=[hc,ac]))
    return rows,exceptions,dict(raw_units=len(rows)+len(exceptions),parsed=len(rows),exceptions=len(exceptions),unit='fixture candidate lines')


def parse_eleven(raw,rec):
    rows=[];exceptions=[];context=[]
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        if z.testzip():raise ValueError('Corrupt source ZIP')
        tables={n:list(csv.DictReader(io.TextIOWrapper(z.open(n),encoding='utf-8-sig',newline=''))) for n in z.namelist() if n.endswith('.csv') and n in {'matches.csv','seasons.csv','teams.csv','venues.csv','match_ties.csv','applied_corrections.csv','penalty_shootouts.csv','format_version.csv','competitions.csv'}}
        seasons={r['season_id']:r for r in tables['seasons.csv']};teams={r['team_id']:r for r in tables['teams.csv']};venues={r['venue_id']:r for r in tables['venues.csv']};ties={r['tie_id']:r for r in tables['match_ties.csv']};corrections=defaultdict(list);shoots=defaultdict(list)
        for i,r in enumerate(tables['applied_corrections.csv'],2):corrections[r['match_id']].append(dict(row=i,**r))
        for i,r in enumerate(tables['penalty_shootouts.csv'],2):shoots[r['match_id']].append(dict(row=i,**r))
        excluded=Counter()
        for n,f in enumerate(tables['matches.csv'],2):
            y=int(seasons[f['season_id']]['season']);loc=f'matches.csv:row:{n}'
            if f['competition_code'] not in ('EL','ELQ') or not 1990<=y<=2025:excluded['OUTSIDE_COMPETITION_OR_SEASON']+=1;continue
            h=teams[f['home_team_id']];away=teams[f['away_team_id']]
            def sc(a,b):return [int(f[a]),int(f[b])] if f[a]!='' and f[b]!='' else None
            pub=sc('home_goals','away_goals');reg=sc('home_goals_regular_time','away_goals_regular_time');aet=pub if f['extra_time_played']=='1' and f['status']=='played' else None
            # Only explicitly supplied regular-time components are authoritative
            # in this adapter; provider zeros may also encode sparse old data.
            if reg is None and f['status']=='played' and f['extra_time_played']=='0' and not f['shootout_home_goals']:
                reg=pub
            pp=periods(regulation_time=reg,half_time=sc('home_goals_half_time','away_goals_half_time'),after_extra_time=aet,shootout=sc('shootout_home_goals','shootout_away_goals'),published_final=pub,administrative_result=pub if f['status']=='awarded' else None)
            fields=dict(f);fields['season_record']=seasons[f['season_id']];fields['home_record']=h;fields['away_record']=away;fields['tie_record']=ties.get(f['tie_id']);fields['corrections']=corrections[f['match_id']];fields['penalty_kicks']=shoots[f['match_id']]
            r=observation(rec,loc,season_of(y),h['name'],away['name'],raw_fields=fields,when=f['local_date'] or None,raw_date=f['local_date'],raw_stage=f['stage'],p=pp,leg=int(f['leg']) if f['leg'] else None,status=f['status'],qualifier=f['competition_code']=='ELQ',venue=venues.get(f['venue_id']),neutral=f['neutral_venue'] if f['neutral_venue']!='' else None,associations=[h['country'],away['country']])
            if re.fullmatch(r'\d{4} first round',f['stage']) and 2009<=y<=2015:
                r['scope'],r['stage']='MAIN','GROUP_STAGE';r['source_fields']['stage_rule']='Source year-prefixed first round is the Europa League group stage; fixture dates/topology retained for independent checks'
            elif y in (2018,2019) and f['stage'] in ('first round','second round','third round') and f['local_date'] and int(f['local_date'][5:7]) in (6,7,8):
                r['scope']='QUALIFYING';r['stage']='QUALIFYING_ROUND_'+str({'first round':1,'second round':2,'third round':3}[f['stage']]);r['source_fields']['stage_rule']='Source early-summer numbered qualifying rounds; verify against RSSSF stage progression'
            if f['competition_code']=='ELQ' and y>=2020 and f['stage'] in ('first round','second round','third round'):
                r['scope']='QUALIFYING';r['stage']='QUALIFYING_ROUND_'+str({'first round':1,'second round':2,'third round':3}[f['stage']])
            rows.append(r)
        for n in z.namelist():
            payload=z.read(n);count=payload.count(b'\n')-1
            context.append(dict(member=n,member_sha256=sha(payload),bytes=len(payload),data_rows=count,role='fixture_source' if n=='matches.csv' else 'joined_support' if n in tables else 'contextual_events_players_statistics_not_independent_fixtures'))
    return rows,exceptions,dict(raw_units=len(tables['matches.csv']),parsed=len(rows),exceptions=0,excluded=dict(excluded),members=context,unit='matches.csv rows')


def parse_schoch(raw,rec):
    import pyarrow.parquet as pq
    allrows=pq.read_table(io.BytesIO(raw)).to_pylist();rows=[];excluded=Counter();exceptions=[]
    for n,f in enumerate(allrows):
        if f['competition']!='UEFA EL':excluded['OTHER_COMPETITION']+=1;continue
        day=str(f['date']);dt=date.fromisoformat(day);y=dt.year-(dt.month<6)
        if not 1990<=y<=2025:excluded['OUTSIDE_TARGET_ERA']+=1;continue
        home=f['home'] or re.sub(r'\s*\([^()]*\)$','',f.get('home_ident') or '')
        away=f['away'] or re.sub(r'\s*\([^()]*\)$','',f.get('away_ident') or '')
        if not home or not away:
            exceptions.append(exception(rec,f'parquet:row:{n}','MISSING_SOURCE_TEAM', {k:str(v) if isinstance(v,date) else v for k,v in f.items()}));continue
        p=periods(published_final=[int(f['gh']),int(f['ga'])] if f['gh'] is not None and f['ga'] is not None else None)
        if f['full_time']=='F':p['regulation_time']=p['published_final']
        elif f['full_time']=='E':p['after_extra_time']=p['published_final']
        flags=[]
        if not f['home'] or not f['away']:flags.append('DISPLAY_NAME_UNAVAILABLE_SOURCE_IDENTIFIER_USED')
        if f['full_time'] in ('E','P'):flags.append('SCHOCH_ET_OR_PENALTIES_INCLUDED_UNSPLIT')
        fields={k:(str(v) if isinstance(v,date) else v) for k,v in f.items()};fields['season_assignment']='JUNE_TO_MAY_CANDIDATE_RECONCILE_DECLARED_SOURCES'
        rows.append(observation(rec,f'parquet:row:{n}',season_of(y),home,away,raw_fields=fields,when=day,raw_date=day,p=p,issues=flags,associations=[f.get('home_country'),f.get('away_country')]))
    return rows,exceptions,dict(raw_units=len(allrows),parsed=len(rows),exceptions=len(exceptions),excluded=dict(excluded),unit='zero-based parquet rows')


def parse_goals(raw,rec):
    reader=csv.DictReader(io.StringIO(text(raw),newline=''));groups=defaultdict(list);exceptions=[];rows=[];total=0
    for n,f in enumerate(reader,2):groups[(f['game'],f['date'],f['season'])].append((n,f));total+=1
    for (game,day,season),entries in sorted(groups.items()):
        m=re.match(r'(.+?) vs\. (.+?) (\d+):(\d+)(.*)',game,re.S)
        if not m:
            exceptions.append(exception(rec,'csv:rows:'+','.join(str(n) for n,_ in entries),'UNSUPPORTED_GOAL_GAME_HEADER',dict(game=game,rows=entries)));continue
        h,away,hg,ag,annotation=m.groups();y=int(season[:4]);pp=periods(published_final=[int(hg),int(ag)])
        if 'n.V.' in annotation:pp['after_extra_time']=pp['published_final']
        rows.append(observation(rec,'csv:rows:'+','.join(str(n) for n,_ in entries),season_of(y),h,away,raw_fields=dict(game=game,date=day,season=season,goal_rows=[dict(row=n,**f) for n,f in entries]),when=day,raw_date=day,p=pp,kind='goal_event_fixture_context',issues=['GOAL_LOG_NOT_COMPLETE_FIXTURE_OR_PERIOD_AUTHORITY']))
    return rows,exceptions,dict(raw_units=total,parsed=len(rows),represented_goal_rows=sum(len(x['source_fields']['goal_rows']) for x in rows),exceptions=len(exceptions),unit='goal events grouped into fixture contexts; not independent matches')


def section_lines(raw,anchor='uefa',detail=False):
    s=text(raw)
    # Exact anchor, not href to another competition. Physical lines inside the
    # source interval remain stable; HTML entities/tags never modify originals.
    pattern=r'<a\b[^>]*(?:name|id)\s*=\s*["\']?'+re.escape(anchor)+r'(?:["\']|\s|>)'
    m=re.search(pattern,s,re.I)
    if not m:return []
    end=re.search(r'<h[123]\b',s[m.end():],re.I) if detail else re.search(r'<h2\b',s[m.end():],re.I)
    stop=m.end()+end.start() if end else len(s)
    begin=s.rfind('\n',0,m.start())+1
    lineno=s[:begin].count('\n')+1
    result=[]
    for i,line in enumerate(s[begin:stop].splitlines()):
        if i==0:
            close=re.search(r'</h[123]>',line,re.I)
            if close:line=line[close.end():]
        result.append((lineno+i,plain(line)))
    return result


def round_dates(s,y):
    # Scheduled/nominal round dates, never silently promoted to playing dates.
    current_month=None;out=[]
    for token in re.findall(r'([A-Z][a-z]{2})\s+(\d{1,2})|\b(\d{1,2})\b',s):
        if token[0]:current_month=MONTHS.get(token[0].lower());d=token[1]
        else:d=token[2]
        if current_month:
            try:out.append(date(y+(current_month<6),current_month,int(d)).isoformat())
            except ValueError:pass
    return out[:2]


def rsssf_periods(token,*,aet=False,pen=False,administrative=False):
    pp=periods(published_final=pair(token))
    if administrative:pp['administrative_result']=pp['published_final']
    elif aet:pp['after_extra_time']=pp['published_final']
    # Unmarked printed scores retain uncertain period semantics, rather than
    # treating every historical published score as a proven regulation result.
    return pp


def parse_rsssf_summary(raw,rec):
    year=int(rec['season'][:4]);rows=[];exceptions=[];lines=section_lines(raw);heading='';sched=[];ctx=[];last_context=[];group=None
    # Save every context line; notes can apply to several earlier fixtures.
    for n,s in lines:
        t=s.strip()
        if not t:continue
        if re.match(r'^(?:First|Second|Third|Fourth|Prelim|Qualif|Group Phase|Group Stage|League Phase|Quarter|Semi|1/[248]|Final|Intermediate|Play)',t,re.I) and not re.search(r'\s\d+-\d+',t):
            heading=t;group=None;ds=round_dates(t,year);sched=ds if ds else [];ctx.append([n,t]);continue
        if re.fullmatch(r'Group [A-L]',t):group=t[-1];ctx.append([n,t]);continue
        if re.fullmatch(r'\([A-Z][a-z]{2}.*\)',t):sched=round_dates(t,year);ctx.append([n,t]);continue
        # Grid: directed first-listed participants, association codes, separate
        # leg results and aggregate. Return leg switches BOTH names and scores.
        m=re.match(r'^(.+?)\s*('+COUNTRY_RE+r')\*?\s+(.+?)\s*('+COUNTRY_RE+r')\*?\s+((?:[*]?\d+\s*-\s*\d+|awd|w/o|withdraw|bye|cancel).*)$',s.strip())
        if m:
            h,hc,away,ac,tail=m.groups();tokens=re.findall(r'\bawd\b|(?<!\d)[*]?\d+-\d+[a-z*]?',tail);score_tokens=[v for v in tokens if not v.endswith('p')]
            if not score_tokens:
                if re.search(r'w/o|withdraw|bye|cancel|not play',tail,re.I):
                    exceptions.append(exception(rec,f'line:{n}','NONPLAYED_TIE_WITHOUT_LEG_RESULTS',s,season=rec['season'],stage=heading,participants=[h,away]));continue
                ctx.append([n,t]);continue
            tie=len(score_tokens)>=3
            count=2 if tie else 1
            for leg in range(count):
                hh,aa=(h,away) if leg==0 else (away,h);hc2,ac2=(hc,ac) if leg==0 else (ac,hc);pp=rsssf_periods(score_tokens[leg],aet=('aet' in tail.lower() and (leg==1 or not tie)),administrative=score_tokens[leg]=='awd' or bool(re.search('award|w/o',tail,re.I)))
                if leg==1:
                    for k,v in pp.items():
                        if v is not None:pp[k]=v[::-1]
                if tie:
                    agg=pair(score_tokens[2]);pp['aggregate']=agg if leg==0 else agg[::-1]
                pens=next((pair(x) for x in tokens if x.endswith('p')),None)
                if pens and (leg==1 or not tie):pp['shootout']=pens if leg==0 else pens[::-1]
                interval=[sched[min(leg,len(sched)-1)]]*2 if sched else None
                markers=set(re.findall(r'\d+-\d+([a-z])',tail))
                annotations=[]
                if markers:
                    for nn,note in lines:
                        if nn<=n:continue
                        if re.match(r'^(?:First|Second|Third|Fourth|Prelim|Qualif|Group Phase|Quarter|Semi|Final|1/[248]|Intermediate)',note.strip(),re.I):break
                        nm=re.match(r'^\s*([a-z])\s+(.+)',note)
                        if nm and nm[1] in markers:annotations.append(note)
                note_text='; '.join(annotations)
                rows.append(observation(rec,f'line:{n}:leg:{leg+1}',rec['season'],hh,aa,raw_fields=dict(raw_line=s,round_context=ctx[-4:],group=group,status_annotation=note_text),interval=interval,raw_date='; '.join(v for _,v in ctx[-3:]),raw_stage=heading,p=pp,leg=leg+1 if tie else None,status='awarded_unscored' if score_tokens[leg]=='awd' else 'published',associations=[hc2,ac2]))
            continue
        simple_group=re.match(r'^([A-Z][a-z]{2})\s+(\d{1,2}):\s*(.+?)\s{2,}(\d+)\s{2,}(.+?)\s{2,}(\d+)(.*)$',t)
        if simple_group:
            mon,dd,h,hg,away,ag,tail=simple_group.groups();when=parse_day(mon+' '+dd,year)
            rows.append(observation(rec,f'line:{n}',rec['season'],h,away,raw_fields=dict(raw_line=s,group=group,round_context=ctx[-4:]),when=when,raw_date=mon+' '+dd,raw_stage='Group Stage',p=periods(published_final=[int(hg),int(ag)])))
            continue
        # Group/final descriptions publish halftime and final as separate values.
        g=re.match(r'^(?:(?P<mon>[A-Z][a-z]{2})\s+(?P<day>\d{1,2}):\s*)?(?P<h>.+?)\s*\((?P<hht>\d+|-)\)\s*(?P<hg>\d+)\s+(?P<a>.+?)\s*\((?P<aht>\d+|-)\)\s*(?P<ag>\d+)(?P<tail>.*)$',t)
        if g:
            f=g.groupdict();when=parse_day((f['mon'] or '')+' '+(f['day'] or ''),year) if f['mon'] else parse_day(heading,year)
            pp=periods(half_time=[int(f['hht']),int(f['aht'])] if f['hht'].isdigit() and f['aht'].isdigit() else None,published_final=[int(f['hg']),int(f['ag'])])
            if 'aet' in f['tail'].lower():pp['after_extra_time']=pp['published_final']
            rows.append(observation(rec,f'line:{n}',rec['season'],f['h'],f['a'],raw_fields=dict(raw_line=s,group=group,round_context=ctx[-4:]),when=when,raw_date=t[:8] if f['mon'] else heading,raw_stage='Group Stage' if f['mon'] else heading,p=pp));continue
        historical_score=re.fullmatch(r'([A-ZÀ-ž][A-Za-zÀ-ž .()’\'-]+?)\s+(\d+-\d+)\s+([A-ZÀ-ž][A-Za-zÀ-ž .()’\'-]+)',t)
        if historical_score and not re.search(r'aggregate|penalt|\bwon\b|\bwin\b|\bleg\b',t,re.I):
            exceptions.append(exception(rec,f'line:{n}','HISTORICAL_SCORE_CONTEXT',s,season=rec['season'],stage=heading,participant_candidates=[historical_score[1],historical_score[3]],reported_score=pair(historical_score[2]),score_period='UNKNOWN_NOT_ASSUMED_REGULATION',classification='CONTEXTUAL_ORIGINAL_RESULT_NOT_ASSUMED_ADDITIONAL_FIXTURE'));continue
        if re.match(r'^[A-Z][a-z]{2}\s+\d{1,2}:',t):
            exceptions.append(exception(rec,f'line:{n}','UNSUPPORTED_DATED_FIXTURE_CONTEXT',s,season=rec['season'],stage=heading));continue
        if re.search(r'\d+\s*-\s*\d+',t) and re.match(r'[A-ZÀ-ž*+]',t) and not re.match(r'(NB|HT|Ref|Att|[a-z] |The |Final|Group|Index|UEFA|Copyright|Author|Last)',t):
            exceptions.append(exception(rec,f'line:{n}','UNSUPPORTED_RSSSF_SCORE_CONTEXT',s,season=rec['season'],stage=heading))
        ctx.append([n,t])
    return rows,exceptions,dict(raw_units=len(rows)+len(exceptions),parsed=len(rows),exceptions=len(exceptions),context_items=[dict(line=nn,raw=ss) for nn,ss in lines if re.search(r'bye|withdraw|walkover|w/o|award|abandon|cancel|replay|not.play|postpon|neutral',ss,re.I)],context_lines=len(lines),context_sha256=sha(encode(lines)),unit='leg observations plus non-fixture/unsupported scored contexts',early_qualifying_applicable=False if year<1994 and not any(r['scope']=='QUALIFYING' for r in rows) else True)


def detail_sections(raw):
    out=[]
    for anchor in ('uefaqdet','uefadet'):
        lines=section_lines(raw,anchor,True)
        if lines:out.append((anchor,lines))
    return out


def parse_rsssf_detail(raw,rec,known_names=()):
    year=int(rec['season'][:4]);rows=[];exceptions=[];sections=detail_sections(raw);lex={team_key(s) for s in known_names};context=[]
    if not sections:
        return [],[exception(rec,'document','OTHER_COMPETITION_DETAIL_PAGE',dict(title=re.search(r'<title>(.*?)</title>',text(raw),re.I|re.S)[1] if re.search(r'<title>(.*?)</title>',text(raw),re.I|re.S) else 'unknown'),season=rec['season'])],dict(raw_units=0,parsed=0,exceptions=1,classification='NO_UEFA_CUP_DETAIL_ANCHORS')
    for anchor,lines in sections:
        heading='Qualifying Round' if anchor=='uefaqdet' else '';day=None;day_raw='';day_line=None
        for i,(n,s) in enumerate(lines):
            t=s.strip()
            if re.match(r'^(FIRST|SECOND|THIRD|FOURTH|[1-4](?:st|nd|rd|th) Qualifying|1/16|1/8|1/4|1/2|ROUND|QUARTER|SEMI|FINAL|GROUP|UEFA.CUP FINAL)',t,re.I) and len(t)<120 and not re.search(r'\d\s*-\s*\d',t):heading=t
            if re.match(r'^.+?\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s*[-–]\s*\d+\s+\d+\s*$',t):
                context.append(dict(section=anchor,line=n,raw=t,classification='STANDINGS_NOT_FIXTURE'));continue
            if re.fullmatch(r'\[[A-Z][a-z]{2}.*\]',t):day=parse_day(t,year);day_raw=t;day_line=n
            elif re.match(r'^\d{1,2} [A-Za-z]+ \d{4}\b',t):day=parse_day(t);day_raw=t;day_line=n
            m=re.match(r'^(.+?)\s+(\d+)\s*[-–]\s*(\d+)(.*)$',t)
            if m and re.search(r'[A-Za-z]',m[1]) and not re.match(r"^\d+(?:\+\d+)?['’]",t) and ',' not in m[1] and not re.search(r'\d+\s*[-–]\s*\d+',m[1]) and (re.search('[-–]',m[1]) or (not re.search(r'won|win|aggregate|penalt|after',m[1],re.I) and any(m[1][j-1].isspace() and (team_key(m[1][:j]) in lex or team_key(m[1][j:]) in lex) for j in range(1,len(m[1]))))) and not t.startswith(('HT','Ref','Att')):
                names,hg,ag,trailer=m.groups();candidates=[]
                for match in re.finditer('[-–]',names):
                    h=names[:match.start()].strip();away=names[match.end():].strip()
                    if h and away:candidates.append((h,away))
                if not candidates:
                    candidates=[(names[:j].strip(),names[j:].strip()) for j in range(1,len(names)) if names[j-1].isspace() and (team_key(names[:j]) in lex or team_key(names[j:]) in lex)]
                block=lines[i:min(i+16,len(lines))]
                explicit=[(names[:m.start()].strip(),names[m.end():].strip()) for m in re.finditer(r'\s+[-–]\s+',names)]
                roster_labels=set()
                for _,v in block:
                    rm=re.match(r'^\s*([^:]{2,45}):',v)
                    if rm and rm[1].casefold() not in ('coach','referee','penalties','yc','rc'):roster_labels.add(team_key(rm[1]))
                roster=[c for c in candidates if team_key(c[0]) in roster_labels and team_key(c[1]) in roster_labels]
                preferred=[c for c in candidates if team_key(c[0]) in lex and team_key(c[1]) in lex]
                roster_prefix=[c for c in candidates if any(team_key(side)==v or (len(v.split())>=2 and team_key(side).startswith(v+' ')) for side in c for v in roster_labels)]
                chosen=explicit[0] if len(explicit)==1 else roster[0] if len(roster)==1 else preferred[0] if len(preferred)==1 else roster_prefix[0] if len(roster_prefix)==1 else candidates[0] if len(candidates)==1 else None
                date_line=next((v for _,v in block[1:9] if parse_day(v) and not re.search(r'coach|referee',v,re.I)),None)
                if chosen is None:
                    exceptions.append(exception(rec,f'line:{n}','AMBIGUOUS_DETAIL_TEAM_DELIMITER',dict(header=t,candidates=candidates,block=block),season=rec['season']));continue
                when=parse_day(date_line) if date_line else day;pp=periods(published_final=[int(hg),int(ag)])
                ht=next((pair(v) for _,v in block if v.strip().startswith('HT:')),None);pp['half_time']=ht
                if re.search('extra time|aet|a.e.t',trailer,re.I):pp['after_extra_time']=pp['published_final']
                if re.search('award|UEFA decision',trailer,re.I):pp['administrative_result']=pair(trailer)
                rows.append(observation(rec,f'line:{n}',rec['season'],*chosen,raw_fields=dict(header=t,block=block,date_context=date_line or day_raw,date_source_line=next((nn for nn,v in block if v==date_line),day_line),section=anchor),when=when,raw_date=date_line or day_raw,raw_stage=date_line.split(' - ')[0] if date_line and re.search(r'qualifying|round|final',date_line.split(' - ')[0],re.I) else heading,p=pp,qualifier=anchor=='uefaqdet',venue=date_line.split(' - ',1)[-1] if date_line else None));continue
            # Alternative match report format: two successive team-score lines,
            # followed by HT/attendance, with optional wrapped scorer text.
            m=re.match(r'^([A-Za-zÀ-ž][^:]+?)\s+(\d+)(?:\s+\(.*)?$',t)
            if m and i+1<len(lines):
                nxt=lines[i+1][1].strip();a=re.match(r'^([A-Za-zÀ-ž][^:]+?)\s+(\d+)(?:\s+\(.*)?$',nxt)
                if a and not re.match(r'(UEFA|ROUND|GROUP|HT|Ref)',t):
                    block=lines[max(0,i-2):min(i+5,len(lines))];pp=periods(published_final=[int(m[2]),int(a[2])],half_time=next((pair(v) for _,v in block if v.strip().startswith('HT:')),None))
                    rows.append(observation(rec,f'line:{n}:pair',rec['season'],m[1],a[1],raw_fields=dict(block=block,section=anchor),when=day,raw_date=next((v for _,v in reversed(lines[:i]) if v.strip().startswith('[')),''),raw_stage=heading,p=pp,qualifier=anchor=='uefaqdet'));continue
            if re.search(r'^\D+[A-Za-z]\s+\d+\s*-\s*\d+',t) and not re.match(r'(HT|Ref|Att|Coach|aggregate|After|Won|First|Second|Third)',t,re.I):
                exceptions.append(exception(rec,f'line:{n}','UNSUPPORTED_DETAIL_SCORED_CONTEXT',t,season=rec['season']))
        context.append(dict(section=anchor,text_lines=len(lines),sha256=sha(encode(lines)),context_items=[dict(line=nn,raw=ss) for nn,ss in lines if re.search(r'bye|withdraw|walkover|w/o|award|abandon|cancel|replay|not.play|postpon|neutral',ss,re.I)]))
    return rows,exceptions,dict(raw_units=len(rows)+len(exceptions),parsed=len(rows),exceptions=len(exceptions),sections=context,unit='identified match headers and unsupported scored contexts')


def templates(s):
    """Balanced outer/nested wikitext spans; offsets bind original revision text."""
    stack=[];i=0;out=[]
    while i<len(s)-1:
        if s[i:i+2]=='{{':stack.append(i);i+=2
        elif s[i:i+2]=='}}' and stack:
            start=stack.pop();out.append((start,i+2,s[start+2:i]));i+=2
        else:i+=1
    return sorted(out)


def split_wiki(s):
    out=[];current=[];braces=links=0;i=0
    while i<len(s):
        token=s[i:i+2]
        if token in ('{{','[['):
            if token=='{{':braces+=1
            else:links+=1
            current.append(token);i+=2;continue
        if token in ('}}',']]'):
            if token=='}}':braces-=1
            else:links-=1
            current.append(token);i+=2;continue
        if s[i]=='|' and not braces and not links:out.append(''.join(current));current=[]
        else:current.append(s[i])
        i+=1
    out.append(''.join(current));return out


def wiki_label(s):
    s=re.sub(r'<ref\b[^>]*>.*?</ref>','',s,flags=re.S|re.I)
    s=re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]',lambda m:m[2],s)
    s=re.sub(r'\[\[([^\]]+)\]\]',lambda m:m[1],s)
    for _,_,body in sorted(templates(s),reverse=True):
        s=s.replace('{{'+body+'}}','')
    return plain(s).replace("'''",'').replace("''",'').strip()


def parse_wikipedia(raw,rec):
    document=json.loads(raw);page=document['query']['pages'][0];rev=page['revisions'][0];s=rev['slots']['main']['content'];year=int(page['title'][:4]);season=season_of(year);rows=[];exceptions=[];context=[]
    spans=templates(s)
    for start,end,body in spans:
        parts=split_wiki(body);name=parts[0].strip().casefold().replace('_',' ');loc=f'revision:{rev["revid"]}:chars:{start}:{end}'
        heading_matches=list(re.finditer(r'^={2,5}([^=]+)={2,5}\s*$',s[:start],re.M));headings=[m[1].strip() for m in heading_matches];heading=next((h for h in reversed(headings) if re.search(r'round|final|qualifying|prelim|group|league|play.off|knockout',h,re.I)),page['title'].split('UEFA ')[-1]);
        if name in ('football box','footballbox','#invoke:football box'):
            fields={}
            for token in parts[1:]:
                if '=' in token:
                    k,v=token.split('=',1);fields[k.strip().casefold()]=v.strip()
            if not {'team1','team2','score'}<=set(fields):
                exceptions.append(exception(rec,loc,'UNSUPPORTED_FOOTBALL_BOX',dict(fields=fields,title=page['title']),season=season));continue
            token=fields['score'];pp=periods(published_final=pair(token),shootout=([int(fields['penalties1']),int(fields['penalties2'])] if fields.get('penalties1','').isdigit() and fields.get('penalties2','').isdigit() else None))
            aet=fields.get('aet') or re.search(r'\{\{aet|after extra|a\.e\.t',token,re.I)
            if aet:pp['after_extra_time']=pp['published_final']
            date_raw=fields.get('date','');when=parse_day(date_raw);issues=[]
            if not pp['published_final']:issues.append('UNSCORED_OR_ADMINISTRATIVE_BOX')
            rows.append(observation(rec,loc,season,wiki_label(fields['team1']),wiki_label(fields['team2']),raw_fields=dict(fields=fields,title=page['title'],revision=rev['revid'],wikitext=s[start:end],headings=headings[-4:]),when=when,raw_date=date_raw,raw_stage=('League phase' if 'league phase' in page['title'] else heading),p=pp,issues=issues,status='administrative_or_unscored' if not pp['published_final'] else 'published',venue=wiki_label(fields.get('stadium','')),replay='replay' in heading.casefold()));continue
        if name in ('twolegresult','twolegresult2'):
            if len(parts)<8:
                exceptions.append(exception(rec,loc,'UNSUPPORTED_TWO_LEG_TEMPLATE',s[start:end],season=season));continue
            positional=[v for v in parts[1:] if not re.match(r'^\s*[A-Za-z0-9_]+\s*=',v)]
            if len(positional)<7:
                exceptions.append(exception(rec,loc,'UNSUPPORTED_TWO_LEG_TEMPLATE',s[start:end],season=season));continue
            home,c1,agg,away,c2,leg1,leg2=positional[:7]
            for i,token in enumerate((leg1,leg2)):
                pp=periods(published_final=pair(token),aggregate=pair(agg));aet='aet' in token.casefold()
                if aet:pp['after_extra_time']=pp['published_final']
                if i:
                    pp={k:(v[::-1] if v is not None else None) for k,v in pp.items()}
                rows.append(observation(rec,loc+f':leg:{i+1}',season,wiki_label(home if i==0 else away),wiki_label(away if i==0 else home),raw_fields=dict(title=page['title'],revision=rev['revid'],wikitext=s[start:end],arguments=parts[1:],headings=headings[-4:]),raw_stage=heading,p=pp,leg=i+1,associations=[wiki_label(c1 if i==0 else c2),wiki_label(c2 if i==0 else c1)]))
        elif name.startswith(('#lst:','#section-h:',':')):
            dependency=parts[0].split(':',1)[1].strip()
            if 'UEFA Cup' in dependency or 'UEFA Europa' in dependency:
                context.append(dict(locator=loc,dependency=dependency,section=parts[1:] or None,classification='EXTERNAL_TRANSCLUSION_NOT_CONTAINED_IN_THIS_PAYLOAD'))
    return rows,exceptions,dict(raw_units=len(rows)+len(exceptions),parsed=len(rows),exceptions=len(exceptions),transclusions=context,title=page['title'],revision=rev['revid'],unit='match boxes and individual legs in summary templates; overlaps retained')
