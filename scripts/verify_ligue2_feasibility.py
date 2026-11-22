"""Independent Phase 2 raw reconciliation; no corrections or standardization.

Uses its own source parser rather than the production feasibility parser.
All RSSSF aliases and score orientations below are diagnostic only.
"""
import re
import html
import json
import hashlib
import collections
from datetime import datetime,date
from scripts import collect_ligue2_feasibility as c



def require(condition, message):
    if not condition:raise ValueError(message)


def orientation_diagnostic(text, literals):
    """Compare two readings with printed standings; neither is a correction."""
    table=text.split('Stages 1-20',1)[1].split('Final Table:',1)[1]
    labels=['St.Étienne','Sedan','Troyes','Lille','Caen','Gueugnon','Guingamp','Châteauroux','Ajaccio','Laval','Niort','Cannes','Nîmes','Nice','Wasquehal','Amiens','Le Mans','Valence','Red Star','Beauvais']
    printed={}; bindings={}
    for line in table.splitlines():
        m=re.fullmatch(r'\s*(\d+)\.(.+?)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)-(\d+)\s+\d+.*',line)
        if not m:continue
        index=int(m[1])-1
        if not 0<=index<20 or labels[index] in printed:raise ValueError('Unexpected standings binding')
        printed[labels[index]]=[int(x) for x in m.groups()[2:]]
        bindings[labels[index]]=m[2].strip()
        if len(printed)==20:break
    if len(printed)!=20:raise ValueError('Incomplete diagnostic standings')
    variants={};aliases={'Beuvais':'Beauvais','St.Étieene':'St.Étienne'}
    for interpretation in ('SCORES_IN_HOME_AWAY_ORDER','RETURN_SCORE_IN_ORIGINAL_LEFT_RIGHT_ORDER'):
        totals=collections.defaultdict(lambda:[0,0,0,0,0,0])
        for i,(h,a,x,y) in enumerate(literals):
            h,a=aliases.get(h,h),aliases.get(a,a)
            if i%2 and interpretation=='RETURN_SCORE_IN_ORIGINAL_LEFT_RIGHT_ORDER':x,y=y,x
            for t,gf,ga in [(h,x,y),(a,y,x)]:
                z=totals[t];z[0]+=1;z[1]+=gf>ga;z[2]+=gf==ga;z[3]+=gf<ga;z[4]+=gf;z[5]+=ga
        differences=[dict(team=t,computed=totals[t],printed=printed[t]) for t in sorted(printed) if totals[t]!=printed[t]]
        variants[interpretation]=dict(matching_clubs=20-len(differences),differing_clubs=len(differences),differences=differences)
    return dict(standings_name_bindings=bindings,variants=variants,
                conclusion='Neither candidate is automatically approved; literal source columns preserved. Any residual discrepancies require independent evidence.')

def reconcile(D=c.PRIVATE):
    saved=json.loads((D/'feasibility_assessment.json').read_text());results=[]
    for s in saved['sources']:
     raw=(D/s['receipt']['path']).read_bytes();require(hashlib.sha256(raw).hexdigest()==s['receipt']['sha256'],'Source hash changed')
     if s['receipt']['repository']=='openfootball/europe':
      rows=[];current=None;year=int(s['receipt']['season'][:4]);rnd=None
      for n,l in enumerate(raw.decode('utf8').splitlines(),1):
       if l.startswith('▪'):rnd=int(re.search(r'\d+',l)[0])
       day=re.fullmatch(r'\s*(Mon|Tue|Wed|Thu|Fri|Sat|Sun) ([A-Z][a-z]{2}) (\d{1,2})(?: (\d{4}))?\s*',l)
       if day:
        candidates=[]
        for y in (year,year+1):
         try:d=datetime.strptime(f'{y} {day[2]} {day[3]}','%Y %b %d').date()
         except ValueError:continue
         if d.strftime('%a')==day[1] and date(year,7,1)<=d<=date(year+1,6,30):candidates.append(d.isoformat())
        require(len(candidates)==1,'Independent date parsing ambiguous');current=candidates[0]
       if ' v ' not in l:continue
       l=re.sub(r'^\s*\d\d:\d\d\s*','',l).strip();home,tail=re.split(r'\s+v\s+',l);m=re.fullmatch(r'(.+?)(?:\s{2,}(\d+)-(\d+)(?:\s+\([^)]*\))?)?(?:\s+\[(.*?)\])?',tail)
       require(m is not None,f'Unknown fixture grammar at line {n}');away,h,a,note=m.groups();rows.append((n,current,home,away,h,a,rnd,note or ''))
      expected=[(r['source_line'],r['date'],r['home'],r['away'],r['hg'],r['ag'],r['round'],r['annotation'].strip('[]')) for r in s['records']];require(rows==expected,'Independent fixture facts differ')
      results.append(dict(season=s['receipt']['season'],raw_records=len(rows),scored=sum(x[4] is not None for x in rows),unscored=sum(x[4] is None for x in rows),exact=True))
     else:
      text=html.unescape(re.sub('<[^>]+>','',raw.decode('latin1')));block=text.split('Stages 1-20',1)[1].split('Final Table:',1)[0]
      matches=re.findall(r'^(.+?)\s+-\s+(.+?)\s*=\s*(\d+)-(\d+)\s+-\s+(\d+)-(\d+)\s*$',block,re.M)
      require(len(matches)==190,'RSSSF paired-line inventory differs')
      literals=[]
      for h,a,x,y,u,v in matches:literals.extend([(h.strip(),a.strip(),int(x),int(y)),(a.strip(),h.strip(),int(u),int(v))])
      require(literals==[(r['home'],r['away'],int(r['hg']),int(r['ag'])) for r in s['records']],'RSSSF literal extraction differs')
      # Explicit diagnostic substitutions only; never mutate source/assessment records.
      diagnostic={'Beuvais':'Beauvais','St.Étieene':'St.Étienne'}
      pairs=collections.Counter((diagnostic.get(h,h),diagnostic.get(a,a)) for h,a,_,_ in literals);teams={t for pair in pairs for t in pair}
      require(len(teams)==20 and len(pairs)==380 and set(pairs.values())=={1},'Diagnostic pairing reconciliation differs')
      totals=collections.defaultdict(lambda:[0,0,0,0,0,0])
      for h,a,x,y in literals:
       h,a=diagnostic.get(h,h),diagnostic.get(a,a)
       for t,gf,ga in [(h,x,y),(a,y,x)]:
        z=totals[t];z[0]+=1;z[1]+=gf>ga;z[2]+=gf==ga;z[3]+=gf<ga;z[4]+=gf;z[5]+=ga
      results.append(dict(season='1998/1999',paired_lines=190,observations=380,literal_clubs=len({r[k] for r in s['records'] for k in ['home','away']}),diagnostic_mappings=diagnostic,diagnostic_clubs=len(teams),diagnostic_unique_pairs=len(pairs),aggregate_stats=dict(sorted(totals.items())),orientation_diagnostic=orientation_diagnostic(text,literals),dates='All 380 are round-heading proxies, not independently verified dates',exact=True))
    return results


if __name__=='__main__':
    results=reconcile();target=c.PRIVATE/'independent_raw_reconciliation.json';content=c.encode(results)
    if target.exists():
        if target.read_bytes()!=content:raise ValueError('Independent assessment changed')
    else:c.save(target,content)
    print(json.dumps(results,indent=2,ensure_ascii=False))
