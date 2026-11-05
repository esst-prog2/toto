"""Acquire only the 36 selected original season CSVs; no DFB access or model use.

Cached original study samples are copied byte-for-byte with original provenance.
Downloads are sequential and paced; errors/access restrictions stop the run.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT=Path(__file__).resolve().parents[1]/'data/private/germany'
DEST=ROOT/'csv_history'
STUDY=ROOT/'source_study'
COMMIT='f64e042d22d2f2a9887c8336125d748ef93269bc'
BASE='https://datahub.io/football/german-bundesliga/_r/-/'


def sha(content):return hashlib.sha256(content).hexdigest()
def save(path,content):
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():
        if path.read_bytes()!=content:raise ValueError(f'Refusing changed content: {path}')
        return
    temporary=path.with_suffix(path.suffix+'.partial')
    with temporary.open('xb') as f:f.write(content)
    temporary.rename(path)


def main():
    DEST.mkdir(parents=True,exist_ok=True)
    manifest_path=DEST/'acquisition.json'
    manifest=json.loads(manifest_path.read_text()) if manifest_path.exists() else dict(
        sources=dict(early_commit=COMMIT,datahub_package=BASE+'datapackage.json'),files={},metadata={})
    cached=[]
    for name in ('sample_retrieval.json','supplement_retrieval.json'):
        cached.extend(json.loads((STUDY/name).read_text()))
    cache={item['url']:(item,STUDY/item['file']) for item in cached if item.get('status')==200}
    last_request=None
    def checkpoint():
        temporary=manifest_path.with_suffix('.next')
        temporary.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
        temporary.replace(manifest_path)
    def acquire(key,url,target,*,group,kind=None,commit=None,reuse=True):
        nonlocal last_request
        registry=manifest[group]
        if key in registry:
            item=registry[key];content=target.read_bytes()
            if sha(content)!=item['sha256']:raise ValueError('Existing checksum mismatch: '+key)
            print('CACHED',key,flush=True);return content
        if reuse and url in cache:
            old,path=cache[url];content=path.read_bytes()
            if sha(content)!=old['sha256']:raise ValueError('Study cache checksum mismatch')
            item={**old,'reused_from':str(path.relative_to(ROOT)),'new_network_download':False}
        else:
            if last_request is not None:time.sleep(max(0,5-(time.monotonic()-last_request)))
            last_request=time.monotonic()
            try:
                with urlopen(Request(url,headers={'User-Agent':'TOTOdology-CSV-Acquisition/1.0'}),timeout=40) as response:
                    content=response.read();status=response.status
                    headers={k:v for k,v in response.headers.items() if k.lower()!='set-cookie'}
                    item=dict(url=url,final_url=response.url,status=status,headers=headers,
                              retrieved_at=datetime.now(timezone.utc).isoformat(),new_network_download=True)
                    if response.headers.get('Retry-After'):raise RuntimeError('Retry-After received; stop for review')
            except HTTPError as exc:
                body=exc.read()
                save(DEST/'failures'/(sha(body)+'.body'),body)
                save(DEST/'failures'/(sha(body)+'.json'),json.dumps(dict(url=url,status=exc.code,error=str(exc)),indent=2).encode())
                raise RuntimeError(f'HTTP {exc.code}; stopped without bypass/retry: {url}') from exc
            if status!=200:raise RuntimeError(f'Unexpected HTTP {status}')
        if kind:
            header=content.splitlines()[0].decode('utf-8-sig' if kind=='early' else 'latin1')
            required=('Round','Date','Team 1','FT','Team 2') if kind=='early' else ('Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR')
            if not set(required)<=set(header.split(',')):raise ValueError('Not the expected CSV schema: '+url)
        save(target,content)
        item.update(file=str(target.relative_to(DEST)),url=url,sha256=sha(content),bytes=len(content),
                    source_commit_sha=commit,source_kind=kind)
        registry[key]=item;checkpoint()
        print('ACQUIRED',key,'reused' if not item['new_network_download'] else 'downloaded',len(content),flush=True)
        return content
    package=acquire('datahub_datapackage',BASE+'datapackage.json',DEST/'metadata/datahub_datapackage.json',group='metadata',reuse=False)
    resources={r['path']:r for r in json.loads(package)['resources']}
    for name,url in [('early_LICENSE',f'https://raw.githubusercontent.com/deadangel33/de-deutschland/{COMMIT}/LICENSE.md'),
                     ('early_SOURCES',f'https://raw.githubusercontent.com/deadangel33/de-deutschland/{COMMIT}/SOURCES.md'),
                     ('datahub_README',BASE+'README.md')]:
        acquire(name,url,DEST/'metadata'/(name+'.md'),group='metadata',commit=COMMIT if name.startswith('early') else None)
    for start in range(1990,2026):
        season=f'{start}/{start+1}'
        if start<1993:
            slug=f'{start}-{(start+1)%100:02d}'
            url=f'https://raw.githubusercontent.com/deadangel33/de-deutschland/{COMMIT}/1990s/{slug}/1-bundesliga.csv'
            kind='early';commit=COMMIT
        else:
            resource=f'season-{start%100:02d}{(start+1)%100:02d}.csv'
            if resource not in resources:raise ValueError('Advertised DataHub resource missing: '+resource)
            url=BASE+resource;kind='datahub';commit=None
        acquire(season,url,DEST/f'originals/{kind}/bundesliga_{start}-{start+1}.csv',group='files',kind=kind,commit=commit)
    print('COMPLETE:',len(manifest['files']),'original seasons',flush=True)


if __name__=='__main__':main()
