"""Independent Phase 2 raw parsing and source-to-assessment reconciliation."""
import calendar,csv,io,json,re
from collections import Counter,defaultdict
from datetime import date
from scripts import collect_eredivisie_feasibility as c


def require(value,message):
    if not value:raise ValueError(message)


def reconcile(directory=c.PRIVATE):
    saved=json.loads((directory/'feasibility_assessment.json').read_text());coverage=json.loads((directory/'coverage_inventory.json').read_text());sources=saved['modern'];results=[]
    # Separate CSV parser and independently recomputed season accounting.
    historical=saved['historical'];receipt=historical['receipt'];raw=(directory/receipt['path']).read_bytes();require(c.sha(raw)==receipt['sha256'],'Historical checksum')
    reader=csv.reader(io.StringIO(raw.decode('utf-8-sig'),newline=''));require(next(reader)==['Date','Season','home','visitor','FT','hgoal','vgoal','tier'],'Historical columns')
    grouped=defaultdict(list);bindings={}
    for cells in reader:
        require(len(cells)==8,'CSV width');d,y,h,a,ft,hg,ag,tier=cells;year=int(y);date.fromisoformat(d)
        require(tier=='1' and ft==f'{int(hg)}-{int(ag)}','CSV tier/score');r=dict(date=d,home=h,away=a,hg=hg,ag=ag,FT=ft);grouped[year].append(r);bindings[reader.line_num]=r
    require(sum(map(len,grouped.values()))==historical['total_records'],'Historical total')
    for summary in coverage['seasons']:
        year=int(summary['season'][:4]);rs=grouped[year];names={r[k] for r in rs for k in ('home','away')};pairs=Counter((r['home'],r['away']) for r in rs)
        require(summary['observed']==len(rs) and summary['scored']==len(rs) and summary['clubs']==len(names),'CSV inventory counts')
        require(summary['directed_pairs']==len(pairs),'CSV directed pairs')
        require(set(map(tuple,summary['missing_pairings']))=={(h,a) for h in names for a in names if h!=a and (h,a) not in pairs},'CSV missing fixtures')
    for sample in historical['samples']:
        for row in sample['records']:
            require({k:row[k] for k in ('date','home','away','hg','ag','FT')}==bindings[row['source_end_line']],'Historical sample binding')
    results.append(dict(source=receipt['path'],rows=sum(map(len,grouped.values())),seasons=len(grouped),exact=True))
    months={m:i for i,m in enumerate(calendar.month_abbr) if m};weekdays=list(calendar.day_abbr)
    for source in sources:
        rec=source['receipt'];raw=(directory/rec['path']).read_bytes();require(c.sha(raw)==rec['sha256'],'Modern checksum');year=int(rec['season'][:4]);parsed=[];current=None;rnd=None
        for number,literal in enumerate(raw.splitlines(keepends=True),1):
            line=literal.decode('utf-8-sig').rstrip('\r\n');t=line.strip()
            if t.startswith('▪'):
                m=re.fullmatch(r'▪ Matchday (\d+)',t);require(m is not None,'Independent stage grammar');rnd=int(m[1]);continue
            m=re.fullmatch(r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun) ([A-Z][a-z]{2}) (\d{1,2})(?: (\d{4}))?',t)
            if m:
                w,mon,day,y=m.groups();years=[int(y)] if y else [year,year+1]
                days=[date(yr,months[mon],int(day)) for yr in years if int(day)<=calendar.monthrange(yr,months[mon])[1]]
                days=[d for d in days if weekdays[d.weekday()]==w and date(year,7,1)<=d<=date(year+1,6,30)]
                require(len(days)==1,'Independent date resolution');current=days[0].isoformat();continue
            if not re.search(r'\s+v\s+',t):continue
            body=re.sub(r'^\d{1,2}:\d{2}\s+','',t);annotation='';note=re.search(r'\s+(\[[^\]]+\])$',body)
            if note:annotation=note[1];body=body[:note.start()].rstrip()
            match=re.fullmatch(r'(.+?)\s+v\s+(.+?)\s{2,}(\d+)-(\d+)(?:\s+\((\d+-\d+)\))?',body)
            if match:h,a,hg,ag,ht=match.groups();ft=f'{hg}-{ag}'
            else:
                parts=re.split(r'\s+v\s+',body);require(len(parts)==2,'Independent fixture grammar');h,a=parts;hg=ag=ht=ft=None
            parsed.append(dict(date=current,home=h,away=a,hg=hg,ag=ag,FT=ft,HT=ht,annotation=annotation,round=rnd,source_line=number,physical_record_sha256=c.sha(literal)))
        rows=source['records'];require(len(parsed)==len(rows),'Independent modern row count')
        for expected,actual in zip(parsed,rows):
            for key,value in expected.items():require(actual[key]==value,'Independent mismatch: '+key)
        counts=source['assessment'];require(counts['scored']==sum(r['FT'] is not None for r in parsed),'Scored count')
        require(counts['explicitly_cancelled']==sum(r['annotation']=='[cancelled]' for r in parsed),'Cancelled count')
        results.append(dict(source=rec['path'],rows=len(parsed),scored=sum(r['FT'] is not None for r in parsed),exact=True))
    return dict(phase=2,independent_parser=True,sources=results,original_fields_preserved=True,historical_certification=False)


if __name__=='__main__':
    result=reconcile();raw=c.encode(result);target=c.PRIVATE/'independent_reconciliation.json'
    if target.exists():require(target.read_bytes()==raw,'Independent assessment changed')
    else:c.save(target,raw)
    print(json.dumps(result,indent=2))
