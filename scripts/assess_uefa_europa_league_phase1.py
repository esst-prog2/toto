"""Offline acquisition-level readability/coverage diagnostics, not a Phase 2 inventory.

No fixture reconciliation, event IDs, canonical records or historical decisions.
Run with the existing research environment (pandas, pyarrow, beautifulsoup4).
"""
import csv
import io
import json
import re
import zipfile
from pathlib import Path
from scripts import acquire_uefa_europa_league as a


def rsssf_section(raw):
    from bs4 import BeautifulSoup
    text=raw.decode('utf-8') if is_utf8(raw) else raw.decode('latin-1')
    heading = re.search(r'<h2\b[^>]*>.*?<a\s+[^>]*(?:name|id)\s*=\s*["\']?uefa(?:["\']|\s|>).*?</h2>', text, re.I|re.S)
    # Bound the search to the exact competition anchor's own heading: a lazy
    # match may begin at an earlier heading, but its end is the target heading.
    if heading is None:raise ValueError('Target competition heading absent')
    tail=text[heading.end():]
    boundary=re.search(r'<h2\b',tail,re.I)
    section=BeautifulSoup(tail[:boundary.start()] if boundary else tail,'html.parser').get_text()
    if len(section)<100:raise ValueError('Empty target section')
    return section


def is_utf8(raw):
    try:raw.decode('utf-8');return True
    except UnicodeDecodeError:return False


def assess(base=a.BASE):
    import pandas as pd
    plan=json.loads((base/'source_plan.json').read_bytes())
    manifest=[]; rss={}; of={}; wiki=[]
    for item in plan['items']:
        r=a.verify(item,base);raw=(base/item['path']).read_bytes()
        row={k:r[k] for k in ('path','url','publisher','bytes','sha256','retrieved_at_utc','kind') if k in r}
        row['receipt_sha256']=a.sha((base/(item['path']+'.provenance.json')).read_bytes())
        row['inspection_encoding']='utf-8' if is_utf8(raw) else ('binary' if not item.get('encoding') else 'latin-1')
        if item.get('kind')=='fixture' and '/rsssf/' in item['path']:
            if 'det.html' not in item['path']:
                s=rsssf_section(raw)
                # Text lines, NOT fixtures or legs. May include annotations/overlap.
                count=sum(bool(re.search(r'\s\d{1,2}-\d{1,2}(?:\s|[a-z*]|$)',x)) for x in s.splitlines())
                rss[item['season']]=dict(score_bearing_lines=count,qualifying_headings=bool(re.search('qualifying|preliminary',s,re.I)),main_heading=bool(re.search('first round|group|final',s,re.I)))
                row['target_score_bearing_lines']=count
            else:
                row['target_section_check']='UEFA target detail anchors present' if re.search(b'uefa',raw,re.I) else 'unverified'
        if item.get('kind')=='fixture' and '/openfootball/' in item['path']:
            text=raw.decode('utf-8');lines=[x for x in text.splitlines() if re.search(r'\bv\s+.+?\d+-\d+',x)]
            if not text.startswith('= UEFA Europa League') or not lines:raise ValueError('Unexpected OpenFootball content')
            year=int(Path(item['path']).parent.name[:4]);season=f'{year}/{year+1}'
            scope='qualifying' if Path(item['path']).name=='elq.txt' else 'main'
            of.setdefault(season,{})[scope]=len(lines);row['scored_description_lines']=len(lines)
        if '/wikipedia/' in item['path'] and item.get('kind')=='fixture':
            pages=json.loads(raw)['query']['pages'];p=pages[0];rev=p['revisions'][0]
            if p.get('missing') or not rev['slots']['main']['content']:raise ValueError('Empty Wikipedia revision')
            wiki.append(dict(path=item['path'],title=p['title'],revid=rev['revid'],timestamp=rev['timestamp'],permalink=f'https://en.wikipedia.org/w/index.php?oldid={rev["revid"]}',history='https://en.wikipedia.org/w/index.php?title='+p['title'].replace(' ','_')+'&action=history',license='CC BY-SA 4.0; Wikipedia contributors'))
        manifest.append(row)
    bootstrap=base/'discovery/openfootball-tree.json'
    bootstrap_raw=bootstrap.read_bytes();r=json.loads(bootstrap.with_name(bootstrap.name+'.provenance.json').read_bytes())
    tree=json.loads(bootstrap_raw)
    if a.sha(bootstrap_raw)!=r['sha256'] or tree.get('truncated') or tree['sha']!='abfaeddc2ee3d14f99ecc163c9ddb46cb4d67cef':
        raise ValueError('Bootstrap discovery metadata changed')
    manifest.append(dict(path='discovery/openfootball-tree.json',url=r['url'],publisher='openfootball/champions-league',kind='discovery',bytes=len(bootstrap_raw),sha256=a.sha(bootstrap_raw),retrieved_at_utc=r['retrieved_at_utc'],receipt_sha256=a.sha(bootstrap.with_name(bootstrap.name+'.provenance.json').read_bytes()),note=r['note']))
    # Complete original mixed archive is preserved; only EL is inspected here.
    parquet=base/'originals/schochastics/football-data/data/results/games.parquet'
    df=pd.read_parquet(parquet);el=df[df.competition=='UEFA EL']
    dates=pd.to_datetime(el.date)
    target_dates=el[(dates>='1990-07-01') & (dates<'2026-07-01')]
    schoch=dict(container_rows=len(df),el_all_dates=len(el),el_target_era_date_window_rows=len(target_dates),date_min=str(el.date.min()),date_max=str(el.date.max()),period_flags=el.full_time.value_counts(dropna=False).to_dict(),limitation='No season or stage column. Date-window rows are not source-declared season totals. gh/ga include extra time and penalties per README.')
    goals=pd.read_csv(base/'originals/schochastics/football-data/data/goals_time/europa-league.csv')
    schoch['goal_event_rows']=len(goals)
    archive=next((base/'originals/fm-devlab/11footy-dataset').rglob('*.zip'))
    with zipfile.ZipFile(archive) as z:
        if z.testzip() is not None:raise ValueError('ZIP CRC failure')
        seasons=pd.read_csv(z.open('seasons.csv'));matches=pd.read_csv(z.open('matches.csv'))
        comps=pd.read_csv(z.open('competitions.csv'))
        if set(matches.competition_code)-{'EL','ELQ'} or set(comps.code)-{'EL','ELQ'}:raise ValueError('Unrelated competition in scoped archive')
        m=matches.merge(seasons[['season_id','season']],on='season_id',validate='many_to_one');m=m[(m.season>=1990)&(m.season<=2025)]
        eleven={}
        for y,g in m.groupby('season'):
            q=g.competition_code.eq('ELQ') | g.stage.fillna('').str.contains('qualif',case=False)
            # Summer play-off rounds before main competition; other ambiguous stage names stay visible.
            q=q | (g.stage.isin(['play-off round','playoff round','playoff']) & pd.to_datetime(g.local_date).dt.month.isin([7,8]))
            eleven[f'{y}/{y+1}']=dict(rows=len(g),qualifying_tagged_rows=int(q.sum()),other_rows=int((~q).sum()),stage_counts=g.stage.value_counts().to_dict(),status_counts=g.status.value_counts().to_dict(),date_nulls=int(g.local_date.isna().sum()),score_nulls=int(g.home_goals.isna().sum()),explicit_regular_time_rows=int(g.home_goals_regular_time.notna().sum()))
        archive_counts=dict(all_rows=len(matches),target_season_rows=len(m),outside_target_rows=len(matches)-len(m),target_status_counts=m.status.value_counts().to_dict(),target_explicit_regular_time_rows=int(m.home_goals_regular_time.notna().sum()),crc='PASS',member_count=len(z.infolist()))
    coverage=[]
    for y in range(1990,2026):
        season=f'{y}/{y+1}';r=rss.get(season);n=eleven.get(season);o=of.get(season,{})
        acquired=['Schoch (calendar-date source; stage unknown; 2025/26 ends in qualifying period)']
        if r:acquired.append('RSSSF summary')
        if n:acquired.append('11footy')
        if o:acquired.append('OpenFootball')
        notes=['Unique fixture totals and completeness unverified; overlaps retained.']
        if y<2001:notes.append('No 11footy file coverage; dates rely on Schoch and targeted Wikipedia/round-date RSSSF evidence.')
        if y in (2002,2004,2005):notes.append('11footy qualifying gap indicated by source stages; RSSSF summary/detail acquired.')
        if y in (2009,2013):notes.append('11footy potential qualifier omissions; compare RSSSF/other source in Phase 2.')
        if y>=2023:notes.append('Recent RSSSF raw copy-grant recognition failed; rendered footer grant observed; no raw copy preserved.')
        if y==2025:notes.append('No OpenFootball main file or verified RSSSF season page; 11footy main plus Wikipedia league/knockout revisions acquired.')
        coverage.append(dict(season=season,competition='UEFA Cup' if y<2009 else 'UEFA Europa League',primary='11footy' if n else 'Schoch + RSSSF',corroborating='RSSSF; OpenFootball where present; targeted Wikipedia (upstream independence unproven)',acquired_sources='; '.join(acquired),main='source content present; completeness unverified',qualifying=('not shown in target section; historical non-applicability preliminary' if y<1994 else 'content present; completeness unverified'),rsssf_score_bearing_lines=r['score_bearing_lines'] if r else '',openfootball_main_lines=o.get('main',''),openfootball_qualifying_lines=o.get('qualifying',''),eleven_source_rows=n['rows'] if n else '',eleven_qualifying_tagged_rows=n['qualifying_tagged_rows'] if n else '',dates='explicit per-record dates in Schoch/11footy; source accuracy unverified; RSSSF often round headers',scores='original reported scores retained; annotations/awards preserved',regulation='partial/ambiguous; no inferred 90-minute scores',license='all raw private; CC0 / ODC-By / author acknowledgement / CC BY-NC / targeted CC BY-SA',remaining_gaps=' '.join(notes)))
    return dict(manifest=manifest,coverage=coverage,rsssf=rss,openfootball=of,eleven=eleven,archive_counts=archive_counts,schoch=schoch,wikipedia=wiki)


def write_reports(base=a.BASE):
    result=assess(base)
    for name,key in [('acquisition_manifest.json','manifest'),('preliminary_readability.json',None),('wikipedia_attribution.json','wikipedia')]:
        value=result[key] if key else {k:v for k,v in result.items() if k not in ('manifest','coverage','wikipedia')}
        raw=a.encode(value);p=base/name
        if p.exists() and p.read_bytes()!=raw:raise ValueError('Frozen diagnostic differs: '+name)
        if not p.exists():a.save(p,raw)
    out=io.StringIO(newline='');writer=csv.DictWriter(out,fieldnames=list(result['coverage'][0]));writer.writeheader();writer.writerows(result['coverage'])
    p=base/'season_coverage.csv';raw=out.getvalue().encode()
    if p.exists() and p.read_bytes()!=raw:raise ValueError('Frozen coverage differs')
    if not p.exists():a.save(p,raw)
    print(json.dumps(dict(payloads=len(result['manifest']),fixture_payloads=sum(x.get('kind')=='fixture' for x in result['manifest']),bytes=sum(x['bytes'] for x in result['manifest']),seasons=len(result['coverage']),archive=result['archive_counts'],schoch=result['schoch']),indent=2))
    return result


if __name__=='__main__':write_reports()
