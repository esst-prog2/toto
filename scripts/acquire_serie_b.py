"""Bounded one-off Serie B original-file acquisition for private academic research.

No scraping/crawling, retries or ongoing-season downloads. Cached originals and
HTTP receipts are immutable; denied access stops that host. Football-Data permits
only light personal/academic downloads (at most twice weekly), not AI training or
commercial use. Do not schedule repeated runs. Review docs/serie-b-validation.md.
"""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import json
import time
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from scripts.acquire_second_bundesliga import sha, save_once

ROOT=Path(__file__).resolve().parents[1]
PRIVATE=ROOT/'data/private/italy/serie_b'
PIN='48954d163c312aa705efacb64f771267031fe6eb'
LAST_REQUEST=None


def plan():
    entries=[]
    for year in range(1990,2026):
        if year<1997:
            kind='rsssf';relative=f'originals/rsssf/ital{(year+1)%100:02}.html'
            url=f'https://www.rsssf.org/tablesi/ital{(year+1)%100:02}.html'
            version=None
        elif year<2013:
            kind='football_data';relative=f'originals/football_data/{year}-{year+1}_I2.csv'
            url=f'https://www.football-data.co.uk/mmz4281/{year%100:02}{(year+1)%100:02}/I2.csv'
            version=None
        else:
            kind='openfootball';slug=f'{year}-{(year+1)%100:02}'
            relative=f'originals/openfootball/{slug}_2-serieb.txt'
            url=f'https://raw.githubusercontent.com/openfootball/italy/{PIN}/{slug}/2-serieb.txt'
            version=PIN
        entries.append(dict(season=f'{year}/{year+1}',kind=kind,file=relative,url=url,version=version))
    return entries


def fetch(url,relative,directory=PRIVATE):
    global LAST_REQUEST
    host=urlsplit(url).netloc
    if urlsplit(url).scheme!='https' or host not in {'www.football-data.co.uk','www.rsssf.org','raw.githubusercontent.com','api.github.com'}:
        raise ValueError('Only inspected direct source routes allowed')
    path=directory/relative
    if not path.resolve().is_relative_to(directory.resolve()):raise ValueError('Path outside private storage')
    receipt=path.with_name(path.name+'.provenance.json')
    if receipt.exists():
        meta=json.loads(receipt.read_text());content=path.read_bytes()
        if meta['url']!=url or meta['sha256']!=sha(content) or meta['bytes']!=len(content):
            raise ValueError('Cached source identity/checksum changed')
        return content
    if path.exists():raise ValueError('Existing source without receipt')
    stop=directory/'access_stops'/f'{host}.json'
    if stop.exists():raise RuntimeError('Host stopped after access restriction: '+host)
    if LAST_REQUEST is not None:time.sleep(max(0,5-(time.monotonic()-LAST_REQUEST)))
    LAST_REQUEST=time.monotonic()
    try:
        with urlopen(Request(url,headers={'User-Agent':'TOTOdology-PrivateAcademicHistory/1.0'}),timeout=45) as r:
            if r.status!=200 or r.headers.get('Retry-After'):raise RuntimeError('Unexpected status/Retry-After; stop')
            content=r.read()
            meta=dict(url=url,final_url=r.url,status=r.status,retrieval_date='2026-11-12',
                      retrieved_at_utc=datetime.now(timezone.utc).isoformat(),bytes=len(content),sha256=sha(content),
                      headers={k:v for k,v in r.headers.items() if k.lower()!='set-cookie'},
                      version='Unversioned response; local byte snapshot is identified by SHA-256')
    except HTTPError as exc:
        error=dict(url=url,status=exc.code,retrieval_date='2026-11-12',reason=str(exc))
        save_once(directory/'failures'/f'{sha(url.encode())}.json',(json.dumps(error,indent=2)+'\n').encode())
        if exc.code in (401,403,429,451):save_once(stop,(json.dumps(error,indent=2)+'\n').encode())
        raise
    if host=='www.rsssf.org' and relative.startswith('originals/'):
        # Each downloaded document must actually carry its own copy grant.
        text=content.decode('latin1').lower()
        if 'free to copy' not in text and 'permission is granted' not in text:
            raise ValueError('No explicit document-level copying grant found; do not save: '+url)
    save_once(path,content)
    save_once(receipt,(json.dumps(meta,indent=2,ensure_ascii=False)+'\n').encode())
    print('SAVED',relative,len(content),flush=True)
    return content


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--completed-2025-alternative',action='store_true',help='Retain the inspected whole-season Football-Data alternative and explicit selection; no fixture merging')
    args=parser.parse_args()
    metadata=[
        ('https://www.football-data.co.uk/contact.php','metadata/football_data_contact.html'),
        ('https://www.football-data.co.uk/italym.php','metadata/football_data_italy.html'),
        ('https://www.football-data.co.uk/notes.txt','metadata/football_data_notes.txt'),
        (f'https://raw.githubusercontent.com/openfootball/italy/{PIN}/LICENSE.md','metadata/openfootball_LICENSE.md'),
        (f'https://raw.githubusercontent.com/openfootball/italy/{PIN}/README.md','metadata/openfootball_README.md'),
        (f'https://api.github.com/repos/openfootball/italy/git/trees/{PIN}?recursive=1','metadata/openfootball_tree.json'),
    ]
    for url,target in metadata:fetch(url,target)
    files=[];failures=[]
    for entry in plan():
        try:fetch(entry['url'],entry['file']);files.append(entry)
        except (HTTPError,RuntimeError,ValueError) as exc:
            failures.append(dict(**entry,error=str(exc)));print('UNAVAILABLE',entry['season'],str(exc),flush=True)
    manifest=dict(retrieval_date='2026-11-12',scope='1990/1991–2025/2026 only; no ongoing data',
                  selection='One primary original per season, no factual merging; RSSSF document copy grant checked before saving; Football-Data private academic use only; OpenFootball CC0 limited to rights held.',
                  files=files,failures=failures,metadata=[dict(url=u,file=p) for u,p in metadata])
    save_once(PRIVATE/'acquisition.json',(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n').encode())
    if args.completed_2025_alternative:
        entry=dict(season='2025/2026',kind='football_data',file='alternatives/football_data/2025-2026_I2.csv',
                   url='https://www.football-data.co.uk/mmz4281/2526/I2.csv',version=None)
        fetch(entry['url'],entry['file'])
        selected=[entry if e['season']=='2025/2026' else e for e in files]
        selection=dict(files=selected,reason='Whole-season alternative for 2025/2026: pinned OpenFootball contains 71 unscored fixtures; Football-Data contains 380 dated results. No fixture merging or correction. All other seasons retain initial sources.')
        save_once(PRIVATE/'selection.json',(json.dumps(selection,indent=2,ensure_ascii=False,sort_keys=True)+'\n').encode())
    print('Original season files:',len(files),'unavailable:',len(failures),flush=True)


if __name__=='__main__':main()
