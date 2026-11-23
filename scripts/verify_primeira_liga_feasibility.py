"""Separate raw-parser reconciliation of Portugal Phase 2, never match policy."""
import calendar
from collections import Counter,defaultdict
import csv
from datetime import date
from html import unescape
import io,json,re
from scripts import collect_primeira_liga_feasibility as c


def require(value,message):
    if not value:raise ValueError(message)


def reconcile(directory=c.PRIVATE):
    manifest=c.verify_originals(directory);saved=json.loads((directory/'feasibility_assessment.json').read_text());coverage=json.loads((directory/'coverage_inventory.json').read_text());overlaps=json.loads((directory/'overlap_diagnostics.json').read_text());bindings={};groups=defaultdict(list);results=[]
    receipt=saved['historical']['receipt'];raw=(directory/receipt['path']).read_bytes();reader=csv.reader(io.StringIO(raw.decode('utf-8-sig'),newline=''))
    require(next(reader)==['Date','Season','home','visitor','FT','hgoal','vgoal','division','tier','totgoal','goaldif','result'],'Independent historical columns')
    for cells in reader:
        require(len(cells)==12,'Historical width');d,y,h,a,ft,hg,ag,div,tier,total,diff,outcome=cells
        require(div=='P1' and tier=='1','Historical scope');require(ft==f'{int(hg)}-{int(ag)}' and int(total)==int(hg)+int(ag) and int(diff)==int(hg)-int(ag),'Derived scores')
        require(outcome==('H' if int(hg)>int(ag) else 'A' if int(hg)<int(ag) else 'D'),'Outcome');require(date.fromisoformat(d).isoformat()==d,'Historical date')
        r=dict(date=d,home=h,away=a,hg=hg,ag=ag,FT=ft);bindings[(receipt['path'],reader.line_num)]=r;groups[int(y)].append(r)
    require(sum(map(len,groups.values()))==coverage['total_records']==saved['historical']['total_records'],'Historical accounting')
    require([int(x['season'][:4]) for x in coverage['seasons']]==sorted(groups),'All historical seasons')
    for summary in coverage['seasons']:
        y=int(summary['season'][:4]);rs=groups[y];names={r[k] for r in rs for k in ('home','away')};pairs=Counter((r['home'],r['away']) for r in rs)
        require((summary['observed'],summary['scored'],summary['clubs'],summary['directed_pairs'])==(len(rs),len(rs),len(names),len(pairs)),'Historical counts/pairs')
        require(set(map(tuple,summary['missing_pairings']))=={(h,a) for h in names for a in names if h!=a and (h,a) not in pairs},'Historical missing pairs')
    for sample in saved['historical']['samples']:
        for r in sample['records']:require({k:r[k] for k in ('date','home','away','hg','ag','FT')}==bindings[(receipt['path'],r['source_end_line'])],'Historical exact sample binding')
    results.append(dict(path=receipt['path'],rows=sum(map(len,groups.values())),seasons=len(groups)))
    modern_lookup={};months={m:i for i,m in enumerate(calendar.month_abbr) if m}
    for source in saved['modern']:
        rec=source['receipt'];raw=(directory/rec['path']).read_bytes();y=int(rec['season'][:4]);end=date(2020,8,2) if y==2019 else date(y+1,6,30);rows=[];day=None;rnd=None
        for line_no,literal in enumerate(raw.splitlines(keepends=True),1):
            t=literal.decode('utf-8-sig').strip()
            if t.startswith('▪'):
                m=re.fullmatch(r'▪ Matchday (\d+)',t);require(m is not None,'Independent round grammar');rnd=int(m[1]);continue
            m=re.fullmatch(r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun) ([A-Z][a-z]{2}) (\d+)(?: (\d{4}))?',t)
            if m:
                ds=[]
                for yr in [int(m[4])] if m[4] else [y,y+1]:
                    try:d=date(yr,months[m[2]],int(m[3]))
                    except ValueError:continue
                    if date(y,7,1)<=d<=end and calendar.day_abbr[d.weekday()]==m[1]:ds.append(d.isoformat())
                require(len(ds)==1,'Independent date resolution');day=ds[0];continue
            if not re.search(r'\s+v\s+',t):continue
            body=re.sub(r'^\d{1,2}:\d{2}\s+','',t);annotation='';note=re.search(r'\s+(\[[^\]]+\])$',body)
            if note:annotation=note[1];body=body[:note.start()].rstrip()
            m=re.fullmatch(r'(.+?)\s+v\s+(.+?)\s{2,}(\d+)-(\d+)(?:\s+\((\d+-\d+)\))?',body)
            if m:h,a,hg,ag,ht=m.groups();ft=f'{hg}-{ag}'
            else:
                fields=re.split(r'\s+v\s+',body);require(len(fields)==2,'Independent fixture');h,a=fields;hg=ag=ht=ft=None
            r=dict(date=day,home=h,away=a,hg=hg,ag=ag,FT=ft,HT=ht,annotation=annotation,round=rnd,source_line=line_no,physical_record_sha256=c.sha(literal));rows.append(r);modern_lookup[(rec['path'],line_no)]=r
        require(len(rows)==len(source['records']),'Modern observations')
        for r,actual in zip(rows,source['records']):
            for k,value in r.items():require(actual[k]==value,'Modern exact binding '+k)
        a=source['assessment'];names={r[k] for r in rows for k in ('home','away')};pairs=Counter((r['home'],r['away']) for r in rows)
        require(a['scored']==sum(r['FT'] is not None for r in rows) and a['clubs']==len(names) and a['directed_pairs']==len(pairs),'Modern measured counts')
        require(set(map(tuple,a['missing_pairings']))=={(h,v) for h in names for v in names if h!=v and (h,v) not in pairs},'Modern pair coverage')
        results.append(dict(path=rec['path'],rows=len(rows),scored=a['scored'],unscored=a['unscored']))
    # Independently re-evaluate every claimed comparison and mapping bijection.
    hlookup={r['audit_id']:r for s in saved['historical']['samples'] for r in s['records']};mlookup={r['audit_id']:r for s in saved['modern'] for r in s['records']}
    for o in overlaps['seasons']:
        mapping={r['historical']:r['modern'] for r in o['mapping']};require(len(set(mapping.values()))==len(mapping),'Mapping collision')
        require(len(o['comparisons'])==o['comparison_pairs'],'Comparison accounting');seen=set()
        for p in o['comparisons']:
            h,m=hlookup[p['historical_id']],mlookup[p['modern_id']];require(h['season']==m['season']==o['season'],'Season boundary')
            require((mapping[h['home']],mapping[h['away']])==(m['home'],m['away']),'Scoped pairing')
            require(p['date_equal']==(h['date']==m['date']) and p['score_equal']==(h['FT']==m['FT']),'Conflict correctness');require(p['modern_id'] not in seen,'Overlap double count');seen.add(p['modern_id'])
    rr=next((r for r in manifest['files'] if r['repository']=='RSSSF'),None)
    if rr:
        raw=(directory/rr['path']).read_bytes();text=unescape(raw.decode(rr['encoding']));block=text.split('Cross Table')[1].split('Accumulated Table')[0]
        lines=[l for l in block.splitlines() if re.match(r'^\s*\d+\s+[A-Za-z]',l)];cells=[re.findall(r'(?<!\w)\d+-\d+(?!\w)|\bX\b',l) for l in lines]
        require(len(cells)==20 and all(len(row)==20 and row[i]=='X' for i,row in enumerate(cells)),'Independent RSSSF geometry')
        s=json.loads((directory/'rsssf_capabilities.json').read_text());require(sum(x!='X' for row in cells for x in row)==s['reconstructable_scores']==380 and s['dated_fixtures']==0,'RSSSF result/date distinction')
        require(len(s['fixtures'])==380 and all(x['date'] is None for x in s['fixtures']),'No inferred dates')
        results.append(dict(path=rr['path'],undated_scores=380))
    return dict(phase=2,independent_parser=True,sources=results,exact_source_bindings=True,no_standardization=True,independent_historical_certification=False)


if __name__=='__main__':
    result=reconcile();c.keep(c.PRIVATE/'independent_reconciliation.json',c.encode(result));print(json.dumps(result,indent=2))
