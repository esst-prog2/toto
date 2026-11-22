"""Bounded Ligue 2 Phase 2 acquisition: seven approved originals only.

Reuse verified pinned metadata/notices already retained by Ligue 1. No retries,
redirects, revision changes or overwrites; no standardization or model use.
"""
import argparse
import json
from pathlib import Path
import time
import subprocess
from urllib.request import Request, build_opener
from scripts import collect_ligue1_feasibility as base

ROOT = base.ROOT
PRIVATE = ROOT/'data/private/france/ligue_2'
PIN = '63df627f3c87ce71708f016522ea236cf74332c3'
REPO = 'openfootball/europe'
YEARS = (2014, 2017, 2019, 2022, 2024, 2025)
PATHS = tuple(f'france/{y}-{(y+1)%100:02}_fr2.txt' for y in YEARS)
NOTICES = ('README.md', 'LICENSE.md', 'france/README.md', 'france/NOTES.md')
RSSSF = 'https://www.rsssf.org/tablesf/fran99.html'
RIGHTS = {
 REPO: 'CC0-1.0 for rights held; upstream provenance/third-party rights not warranted; redistribution and model-training clearance unresolved.',
 'rsssf': 'Copyright Jerome Faugeras, Frederic Pauron and RSSSF 1999/2000; copying with author acknowledgement permitted; all rights reserved. Automated downstream reuse/model-training clearance unresolved.'}
sha, encode, save, now = base.sha, base.encode, base.save, base.now


def initialize(directory=PRIVATE, root=ROOT):
    if (root == ROOT and
        (subprocess.check_output(['git','branch','--show-current'],cwd=root).decode().strip()!='feature/data-collection' or
         subprocess.check_output(['git','rev-parse','HEAD'],cwd=root).decode().strip()!='07efff5f014bdd2e7e423f2fee76333346135790')):
        raise ValueError('Unexpected branch or starting HEAD')
    return base.initialize(directory, root)


def protect(directory=PRIVATE, root=ROOT):
    return base.protect(directory, root)


def metadata(directory=PRIVATE):
    previous=ROOT/'data/private/france/ligue_1'
    base.verify_originals(previous)
    source=previous/'metadata'/REPO/'git_tree.json'
    raw=source.read_bytes(); entries=base.tree_entries(raw,PIN,PATHS+NOTICES)
    receipt=json.loads(source.with_suffix('.receipt.json').read_text())
    if receipt['sha256']!=sha(raw) or receipt['commit']!=PIN: raise ValueError('Prior tree changed')
    dest=directory/'metadata/git_tree.json'
    for target, content in [(dest,raw),(dest.with_suffix('.receipt.json'),encode(dict(receipt,reused_from=str(source.relative_to(ROOT)))))]:
        if target.exists():
            if target.read_bytes()!=content:raise ValueError('Reused metadata changed')
        else:save(target,content)
    for name in NOTICES:
        original=previous/REPO/name; data=original.read_bytes(); base.verify_blob(data,entries[name])
        target=directory/REPO/name
        rec=json.loads(original.with_name(original.name+'.provenance.json').read_text())
        content=encode(dict(rec,reused_from=str(original.relative_to(ROOT))))
        for target,blob in [(target,data),(target.with_name(target.name+'.provenance.json'),content)]:
            if target.exists():
                if target.read_bytes()!=blob:raise ValueError('Reused notice changed')
            else:save(target,blob)
    if not (directory/REPO/'LICENSE.md').read_text().startswith('CC0 1.0 Universal'):raise ValueError('Licence changed')
    return entries


def request(url, directory):
    if (directory/'ACCESS_STOP.json').exists():raise RuntimeError('Prior failure; explicit review required before retry')
    try:
        with build_opener(base.NoRedirect).open(Request(url,headers={'User-Agent':'ThePickSheet-Ligue2-bounded-feasibility'}),timeout=30) as r:
            if r.status!=200 or r.url!=url or r.headers.get('Retry-After'):raise ValueError('Unexpected access response')
            raw=r.read(8_000_001)
            if len(raw)>8_000_000:raise ValueError('Size limit exceeded')
            return raw
    except Exception as exc:
        save(directory/'ACCESS_STOP.json',encode(dict(url=url,error=str(exc),timestamp_utc=now())))
        raise


def plan():
    return [dict(repository=REPO,commit=PIN,original_path=n,path=f'{REPO}/{n}',
                 url=f'https://raw.githubusercontent.com/{REPO}/{PIN}/{n}',season=f'{y}/{y+1}')
            for y,n in zip(YEARS,PATHS)]+[dict(repository='rsssf',commit=None,original_path='tablesf/fran99.html',
                path='rsssf/fran99.html',url=RSSSF,season='1998/1999')]


def verify_record(directory,item,r,entries):
    raw=(directory/item['path']).read_bytes()
    expected=dict(item,bytes=len(raw),sha256=sha(raw),kind='dataset',competition='Ligue 2',
                  original_filename=Path(item['original_path']).name,licensing=RIGHTS[item['repository']],
                  git_blob_sha1=base.verify_blob(raw,entries[item['original_path']]) if item['commit'] else None)
    if any(r.get(k)!=v for k,v in expected.items()):raise ValueError('Original/receipt mismatch')
    if not r.get('retrieved_at_utc') or not r.get('attribution'):raise ValueError('Incomplete provenance')
    return raw


def collect(directory=PRIVATE,root=ROOT):
    protected=protect(directory,root);entries=metadata(directory);receipts=[]
    for item in plan():
        target=directory/item['path'];receipt=target.with_name(target.name+'.provenance.json')
        if target.exists()!=receipt.exists():raise ValueError('Incomplete source/receipt pair')
        if target.exists():
            r=json.loads(receipt.read_text());verify_record(directory,item,r,entries)
        else:
            raw=request(item['url'],directory)
            blob=base.verify_blob(raw,entries[item['original_path']]) if item['commit'] else None
            if not item['commit']:
                text=raw.decode('latin-1')
                if 'France 1998/99' not in text or 'Stages 1-20' not in text:raise ValueError('Unexpected RSSSF document')
            r=dict(item,bytes=len(raw),sha256=sha(raw),git_blob_sha1=blob,kind='dataset',competition='Ligue 2',
                   original_filename=Path(item['original_path']).name,retrieved_at_utc=now(),
                   licensing=RIGHTS[item['repository']],attribution='OpenFootball contributors' if item['commit'] else 'Jerome Faugeras, Frederic Pauron; second-division results credited to Sorin Arotaritei; RSSSF',
                   format=target.suffix,uncertainty='Original source assertions, not historical certification; dates and administrative semantics require assessment')
            save(target,raw);save(receipt,encode(r));time.sleep(2)
        receipts.append(r)
    manifest=dict(scope='Ligue 2 Phase 2: exactly seven approved originals',files=receipts,rights=RIGHTS,
                  protected=protected,source_independence='Not established by different file/provider identity')
    target=directory/'acquisition.json';content=encode(manifest)
    if target.exists():
        if target.read_bytes()!=content:raise ValueError('Acquisition manifest changed')
    else:save(target,content)
    verify_originals(directory);protect(directory,root)
    return manifest


def verify_originals(directory=PRIVATE):
    m=json.loads((directory/'acquisition.json').read_text());items=plan()
    if len(m['files'])!=7 or m['rights']!=RIGHTS or {(r['repository'],r['path']) for r in m['files']}!={(r['repository'],r['path']) for r in items}:raise ValueError('Acquisition scope changed')
    tree=directory/'metadata/git_tree.json';raw=tree.read_bytes();tr=json.loads(tree.with_suffix('.receipt.json').read_text())
    if sha(raw)!=tr['sha256'] or tr['commit']!=PIN or tr['url']!=f'https://api.github.com/repos/{REPO}/git/trees/{PIN}?recursive=1':raise ValueError('Tree receipt changed')
    entries=base.tree_entries(raw,PIN,PATHS+NOTICES)
    for n in NOTICES:
        path=directory/REPO/n;rec=json.loads(path.with_name(path.name+'.provenance.json').read_text());data=path.read_bytes()
        if sha(data)!=rec['sha256'] or rec['commit']!=PIN or base.verify_blob(data,entries[n])!=rec['git_blob_sha1']:raise ValueError('Notice changed')
    for item in items:
        r=next(r for r in m['files'] if r['path']==item['path']);verify_record(directory,item,r,entries)
        target=directory/item['path']
        if json.loads(target.with_name(target.name+'.provenance.json').read_text())!=r:raise ValueError('Manifest/receipt differs')
    return m


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--init',action='store_true');args=parser.parse_args()
    if args.init:initialize()
    m=collect();print('ACQUIRED_OR_VERIFIED',len(m['files']),'PROTECTED',m['protected'])
