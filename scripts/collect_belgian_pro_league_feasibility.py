"""Phase 2 only: seven approved Belgium originals, immutable fail-closed cache."""
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
PRIVATE = ROOT / 'data/private/belgium/pro_league'
HEAD = '013bb9c195624d5ac290aeb57dae11c4e21c0b5a'
HIST, MODERN = 'jalapic/engsoccerdata', 'openfootball/belgium'
PINS = {HIST: '872c5c354161ace8408f3091b758c6af4cccca94', MODERN: '1166d3c9c5725aec01e1bbeaa20f6467e39ddbb8'}
RSSSF = ('https://www.rsssf.org/tablesb/belg93.html', 'https://www.rsssf.org/tablesb/belg2010.html')
IDENTITIES = (
    (HIST, 'data-raw/belgium.csv', 'MULTISEASON', '949da4ac0a95ec17ffa883b7b497553c9ec38a96', 555878),
    (MODERN, '2018-19/be1.txt', '2018/2019', 'fd7f187a36a4c4c1389aab3d4a736bb1ca3802ee', 22252),
    (MODERN, '2019-20/be1.txt', '2019/2020', 'f1e6e2e6d3684dcf8335efd66473cc54ef2af0c4', 19469),
    (MODERN, '2023-24/be1.txt', '2023/2024', 'c28e1faff98417df5ff0e72085d4fdbdb3d756eb', 26414),
    (MODERN, '2025-26/be1.txt', '2025/2026', 'dbca2186e03f1a8372902f58eddfa174a2124a22', 16867),
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
    return items + [dict(repository='RSSSF', commit=None, original_path=url.split('rsssf.org/')[1],
                         path='rsssf/'+url.split('rsssf.org/')[1], season=season,
                         expected_blob=None, expected_bytes=None, url=url)
                    for url, season in zip(RSSSF, ('1992/1993','2009/2010'))]


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
    # The exact pinned identities are the approved catalogue. No further originals.
    # Existing historical licence/tree evidence is referenced, not altered.
    evidence=root/'data/private/portugal/primeira_liga/metadata/jalapic/engsoccerdata/git_tree.json'
    tree=json.loads(evidence.read_bytes())
    entry=next(x for x in tree['tree'] if x['path']=='data-raw/belgium.csv')
    if tree['sha']!=PINS[HIST] or entry['sha']!=IDENTITIES[0][3] or entry['size']!=IDENTITIES[0][4]:
        raise ValueError('Retained historical tree identity differs')
    return {HIST: dict(tree_sha256=sha(evidence.read_bytes()),reference=str(evidence.relative_to(root))),
            MODERN: dict(commit=PINS[MODERN],catalogue='Approved Phase 1 path/blob/size inventory; original bytes verified on acquisition')}


def request(item, directory):
    if item not in plan(): raise ValueError('Unapproved acquisition item')
    stop=directory/'access'/f"{sha(item['url'].encode())}.STOP.json"
    if stop.exists(): raise RuntimeError('Previous source access restriction; no retry')
    try:
        with build_opener(base.NoRedirect).open(Request(item['url'],headers={'User-Agent':'ThePickSheet-Belgium-bounded-academic-feasibility'}),timeout=30) as response:
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
                     attribution='James Curley' if item['repository']==HIST else 'OpenFootball contributors' if item['repository']==MODERN else 'Page-specific authors and RSSSF; see preserved original notices',
                     licensing=RIGHTS[item['repository']],upstream_provenance='engsoccerdata later periods use Football-Data; OpenFootball independence unestablished; RSSSF page-specific sources preserved',
                     constraints='One bounded request; no retries, redirects or access bypass; private feasibility only')
            save(dest,raw); save(receipt,encode(rec)); time.sleep(2)
        receipts.append(rec)
    manifest=dict(phase=2,scope='Exactly seven approved Belgium originals; no historical policy',files=receipts,blocked=blocked,rights=RIGHTS,protected=protected)
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
