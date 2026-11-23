"""Phase 2 only: seven approved Portugal originals, immutable fail-closed cache."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time
from urllib.request import Request, build_opener
from scripts import collect_ligue1_feasibility as base

ROOT = base.ROOT
PRIVATE = ROOT / 'data/private/portugal/primeira_liga'
HEAD = '0bb6f393c89fdcc37a52a56bb31e458ff131de47'
HIST, MODERN = 'jalapic/engsoccerdata', 'openfootball/europe'
PINS = {HIST: '872c5c354161ace8408f3091b758c6af4cccca94', MODERN: '63df627f3c87ce71708f016522ea236cf74332c3'}
RSSSF = 'https://www.rsssf.org/tablesp/porthist199091.html'
IDENTITIES = (
    (HIST, 'data-raw/portugal.csv', 'MULTISEASON', 'ffb6afe2e6fd395269edd2cfe00e5de33a30dbc2', 592748),
    (MODERN, 'portugal/2018-19_pt1.txt', '2018/2019', 'fda4562db066b03c72bc7892e5a21527e9e41c5d', 24871),
    (MODERN, 'portugal/2019-20_pt1.txt', '2019/2020', '7d5d7a2df26e2b21be46bb9b08c9c8b007b89632', 25013),
    (MODERN, 'portugal/2021-22_pt1.txt', '2021/2022', 'c448a04c11ae5b96e6bdbedabed75d1558f447df', 24988),
    (MODERN, 'portugal/2024-25_pt1.txt', '2024/2025', '0bf964ac3c7767645b4a084a8b11ec1cc0db0e6d', 25019),
    (MODERN, 'portugal/2025-26_pt1.txt', '2025/2026', '1bc5b5eae05bdcefeb64c2ea71ea931d546a6873', 25060),
)
RIGHTS = {
    HIST: 'README noncommercial use with attribution; package GPL >=2. Upstream ownership, redistribution and model-training permission unresolved; private feasibility only.',
    MODERN: 'CC0-1.0 for rights held; upstream data ownership and independence not warranted; redistribution and training clearance unresolved.',
    'RSSSF': 'Page-specific author/copyright/acknowledgement conditions preserved in original; no general training or commercial clearance inferred.',
}
sha, encode, now = base.sha, base.encode, base.now


def save(path, raw):
    """Publish a complete exclusive file atomically, never replace an original."""
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='.pending-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(raw); stream.flush(); os.fsync(stream.fileno())
        os.link(temporary, path)
    finally:
        os.unlink(temporary)


def keep(path, raw):
    if path.exists():
        if path.read_bytes() != raw: raise ValueError('Immutable artifact differs: '+str(path))
    else: save(path, raw)


def plan():
    items = [dict(repository=repo, commit=PINS[repo], original_path=path, path=f'{repo}/{path}', season=season,
                  expected_blob=blob, expected_bytes=size,
                  url=f'https://raw.githubusercontent.com/{repo}/{PINS[repo]}/{path}')
             for repo, path, season, blob, size in IDENTITIES]
    return items + [dict(repository='RSSSF', commit=None, original_path='tablesp/porthist199091.html',
                         path='rsssf/tablesp/porthist199091.html', season='1990/1991',
                         expected_blob=None, expected_bytes=None, url=RSSSF)]


def initialize(directory=PRIVATE, root=ROOT):
    if (directory/'protected_before.json').exists(): return protect(directory, root)
    if subprocess.check_output(['git','branch','--show-current'],cwd=root).decode().strip()!='feature/data-collection': raise ValueError('Wrong branch')
    if subprocess.check_output(['git','rev-parse','HEAD'],cwd=root).decode().strip()!=HEAD: raise ValueError('Wrong HEAD')
    if subprocess.check_output(['git','diff','--cached','--name-only'],cwd=root): raise ValueError('Unexpected staged changes')
    changed=subprocess.check_output(['git','diff','--name-only'],cwd=root).decode().splitlines()
    if changed: raise ValueError('Unexpected tracked changes: '+repr(changed))
    result=base.initialize(directory, root)
    index=Path(subprocess.check_output(['git','rev-parse','--git-path','index'],cwd=root).decode().strip())
    if not index.is_absolute(): index=root/index
    save(directory/'git_start.json',encode(dict(head=HEAD,index_sha256=sha(index.read_bytes()))))
    return result


def protect(directory=PRIVATE, root=ROOT):
    result=base.protect(directory,root)
    g=json.loads((directory/'git_start.json').read_text())
    if subprocess.check_output(['git','rev-parse','HEAD'],cwd=root).decode().strip()!=g['head']: raise ValueError('HEAD changed')
    index=Path(subprocess.check_output(['git','rev-parse','--git-path','index'],cwd=root).decode().strip())
    if not index.is_absolute(): index=root/index
    if sha(index.read_bytes())!=g['index_sha256']: raise ValueError('Git index changed')
    return result


def metadata(directory=PRIVATE, root=ROOT):
    previous=root/'data/private/netherlands/eredivisie'; trees={}
    for repo in PINS:
        src=previous/'metadata'/repo/'git_tree.json'; raw=src.read_bytes()
        rec=json.loads(src.with_suffix('.receipt.json').read_text())
        if sha(raw)!=rec['sha256'] or rec['commit']!=PINS[repo]: raise ValueError('Retained tree identity differs')
        notices=('README.md','DESCRIPTION') if repo==HIST else ('README.md','LICENSE.md')
        paths=tuple(x['original_path'] for x in plan() if x['repository']==repo)+notices
        tree=base.tree_entries(raw,PINS[repo],paths); trees[repo]=tree
        for item in plan():
            if item['repository']==repo and (tree[item['original_path']]['sha']!=item['expected_blob'] or tree[item['original_path']]['size']!=item['expected_bytes']): raise ValueError('Approved Git identity differs')
        keep(directory/'metadata'/repo/'git_tree.json',raw)
        keep(directory/'metadata'/repo/'git_tree.receipt.json',encode(dict(rec,reused_from=str(src.relative_to(root)))))
        for name in notices:
            source=previous/repo/name; content=source.read_bytes(); base.verify_blob(content,tree[name])
            keep(directory/repo/name,content)
            keep(directory/repo/(name+'.provenance.json'),source.with_name(name+'.provenance.json').read_bytes())
    return trees


def request(item, directory):
    if item not in plan(): raise ValueError('Unapproved acquisition item')
    stop=directory/'access'/f"{sha(item['url'].encode())}.STOP.json"
    if stop.exists(): raise RuntimeError('Previous source access restriction; no retry')
    try:
        with build_opener(base.NoRedirect).open(Request(item['url'],headers={'User-Agent':'ThePickSheet-Portugal-bounded-academic-feasibility'}),timeout=30) as response:
            if response.status!=200 or response.url!=item['url'] or response.headers.get('Retry-After'): raise ValueError('Restricted/redirected response')
            raw=response.read(8000001)
            if len(raw)>8000000: raise ValueError('Response exceeds bound')
            return raw,dict(final_url=response.url,status=response.status,headers=dict(response.headers.items()))
    except Exception as exc:
        save(stop,encode(dict(url=item['url'],retrieved_at_utc=now(),error=str(exc))))
        raise


def verify_record(directory, item, rec):
    raw=(directory/item['path']).read_bytes()
    if any(rec.get(k)!=v for k,v in item.items()) or rec['sha256']!=sha(raw) or rec['bytes']!=len(raw): raise ValueError('Original/receipt mismatch')
    if rec.get('licensing')!=RIGHTS[item['repository']] or not rec.get('retrieved_at_utc') or not rec.get('attribution'): raise ValueError('Missing provenance')
    if item['expected_blob']:
        base.verify_blob(raw,dict(sha=item['expected_blob'],size=item['expected_bytes']))
        if rec['git_blob_sha1']!=item['expected_blob']: raise ValueError('Receipt blob mismatch')
    elif rec['git_blob_sha1'] is not None: raise ValueError('Mutable web document cannot claim Git identity')
    return raw


def collect(directory=PRIVATE, root=ROOT):
    protected=protect(directory,root); metadata(directory,root); receipts=[]; blocked=[]
    for item in plan():
        dest=directory/item['path']; receipt=dest.with_name(dest.name+'.provenance.json')
        if dest.exists()!=receipt.exists(): raise ValueError('Partial original/receipt pair; manual inspection required')
        if dest.exists(): rec=json.loads(receipt.read_text()); verify_record(directory,item,rec)
        else:
            stop=directory/'access'/f"{sha(item['url'].encode())}.STOP.json"
            if stop.exists():
                blocked.append(dict(path=item['path'],error=json.loads(stop.read_text())['error'])); continue
            try: raw,response=request(item,directory)
            except Exception:
                if not stop.exists(): raise
                blocked.append(dict(path=item['path'],error=json.loads(stop.read_text())['error'])); continue
            if item['expected_blob']: base.verify_blob(raw,dict(sha=item['expected_blob'],size=item['expected_bytes']))
            # Encoding is validated, never converted. RSSSF often declares Latin-1.
            encoding='utf-8-sig'
            try: raw.decode(encoding)
            except UnicodeDecodeError:
                if item['repository']!='RSSSF': raise
                encoding='iso-8859-1'
            rec=dict(item,bytes=len(raw),sha256=sha(raw),git_blob_sha1=item['expected_blob'],retrieved_at_utc=now(),
                     original_filename=dest.name,format=dest.suffix,encoding=encoding,response=response,
                     publisher='James Curley / contributors' if item['repository']==HIST else 'OpenFootball contributors' if item['repository']==MODERN else 'RSSSF and page author',
                     attribution='James Curley' if item['repository']==HIST else 'OpenFootball contributors' if item['repository']==MODERN else 'Jorge Miguel Teixeira and RSSSF',
                     licensing=RIGHTS[item['repository']],upstream_provenance='Not independently established; retained repository notices apply',
                     constraints='One bounded request; no retries, redirects or access bypass; private feasibility only')
            save(dest,raw); save(receipt,encode(rec)); time.sleep(2)
        receipts.append(rec)
    manifest=dict(phase=2,scope='Exactly seven approved Portugal originals; no historical policy',files=receipts,blocked=blocked,rights=RIGHTS,protected=protected)
    keep(directory/'acquisition.json',encode(manifest)); verify_originals(directory); protect(directory,root)
    return manifest


def verify_originals(directory=PRIVATE):
    manifest=json.loads((directory/'acquisition.json').read_text()); by={x['path']:x for x in plan()}
    if len({x['path'] for x in manifest['files']})!=len(manifest['files']): raise ValueError('Duplicate receipt')
    if set(by)!=set(x['path'] for x in manifest['files'])|set(x['path'] for x in manifest['blocked']): raise ValueError('Missing/unapproved acquisition')
    for rec in manifest['files']:
        verify_record(directory,by[rec['path']],rec)
        dest=directory/rec['path']
        if json.loads(dest.with_name(dest.name+'.provenance.json').read_text())!=rec: raise ValueError('Receipt binding differs')
    return manifest


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--init',action='store_true');args=parser.parse_args()
    print(initialize() if args.init else collect())
