"""Phase 3 only: acquire twelve approved, pinned Primera División originals.

Completed runs are offline/idempotent; partial runs reuse exact cached receipts.
One request per five seconds; any access/fetch failure stops the batch, no retries.
"""
from datetime import datetime,timezone
import json
from pathlib import Path
import time
from urllib.parse import urlsplit
from urllib.request import Request,urlopen

from scripts.collect_la_liga_feasibility import ROOT,PRIVATE,protected,sha
from scripts.validate_la_liga_feasibility import encode

REPO='openfootball/espana'
PIN='80035a93dd4920985af52aa097a54a6fb888563b'
TREE_URL=f'https://api.github.com/repos/{REPO}/git/trees/{PIN}?recursive=1'
MANIFEST='phase3_acquisition.json'
TREE='phase3_git_tree.json'
TREE_RECEIPT='phase3_git_tree_receipt.json'
STOP='phase3_access_stop.json'


def plan():
    return [dict(season=f'{y}/{y+1}',competition='La Liga / Primera División',
                 repository=f'https://github.com/{REPO}',commit=PIN,
                 original_path=f'{y}-{(y+1)%100:02}/1-liga.txt',original_filename='1-liga.txt',format='Football.TXT',
                 path=f'{REPO}/{y}-{(y+1)%100:02}/1-liga.txt',
                 url=f'https://raw.githubusercontent.com/{REPO}/{PIN}/{y}-{(y+1)%100:02}/1-liga.txt') for y in range(2013,2025)]


def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as f:f.write(value)


def protect(directory=PRIVATE):
    count=protected(directory)
    baseline=json.loads((directory/'phase3_protected_before.json').read_text())
    if len(baseline)!=19:raise ValueError('Phase 2 baseline scope changed')
    for name,digest in baseline.items():
        p=ROOT/name
        if not p.resolve().is_relative_to(ROOT.resolve()) or sha(p.read_bytes())!=digest:
            raise ValueError('Phase 2 artifact changed: '+name)
    return dict(previous_competition_files=count,phase2_files=len(baseline))


def verify_file(raw,entry):
    import hashlib
    blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    if len(raw)!=entry['size'] or blob!=entry['sha']:raise ValueError('Pinned Git blob identity/size mismatch')
    return blob


def cached(directory,item,entry):
    p=directory/item['path'];receipt=p.with_name(p.name+'.provenance.json')
    if not p.exists() and not receipt.exists():return None
    if not p.exists() or not receipt.exists():raise ValueError('Incomplete cached original/receipt; manual inspection required')
    r=json.loads(receipt.read_text());raw=p.read_bytes();blob=verify_file(raw,entry)
    if any(r[k]!=v for k,v in item.items()) or r['sha256']!=sha(raw) or r['bytes']!=len(raw) or r['git_blob_sha1']!=blob:
        raise ValueError('Cached receipt/source mismatch')
    return r


def checked_tree(raw):
    tree=json.loads(raw)
    if tree.get('truncated') or tree.get('sha')!=PIN:raise ValueError('Incomplete/wrong pinned Git tree')
    entries={e['path']:e for e in tree['tree'] if e['type']=='blob'}
    if any(i['original_path'] not in entries for i in plan()):raise ValueError('Approved original path missing from pinned tree')
    return entries


def collect(directory=PRIVATE):
    preservation=protect(directory)
    old=json.loads((directory/'acquisition.json').read_text())
    for r in old['files']:
        raw=(directory/r['path']).read_bytes()
        if sha(raw)!=r['sha256'] or len(raw)!=r['bytes']:raise ValueError('Phase 2 source receipt changed')
    licence=(directory/REPO/'LICENSE.md').read_text()
    if not licence.startswith('CC0 1.0 Universal'):raise ValueError('Approved licence changed')
    last=None
    def get(url):
        nonlocal last
        if (directory/STOP).exists():raise RuntimeError('Prior access stop requires manual review')
        if urlsplit(url).scheme!='https' or urlsplit(url).hostname not in {'api.github.com','raw.githubusercontent.com'}:
            raise ValueError('Unapproved acquisition route')
        if last is not None:time.sleep(max(0,5-(time.monotonic()-last)))
        last=time.monotonic()
        try:
            with urlopen(Request(url,headers={'User-Agent':'TOTOdology-bounded-LaLiga-history'}),timeout=45) as r:
                if r.status!=200 or r.headers.get('Retry-After'):raise RuntimeError('Unexpected status/Retry-After')
                if urlsplit(r.url).hostname!=urlsplit(url).hostname:raise RuntimeError('Unexpected redirect host')
                return r.read(),dict(url=url,final_url=r.url,status=r.status,retrieved_at_utc=datetime.now(timezone.utc).isoformat())
        except Exception as exc:
            save(directory/STOP,encode(dict(url=url,error=str(exc),timestamp_utc=datetime.now(timezone.utc).isoformat(),action='STOP; no automatic retry')))
            raise
    tp=directory/TREE;trp=directory/TREE_RECEIPT
    if tp.exists()!=trp.exists():raise ValueError('Incomplete cached tree/receipt')
    if tp.exists():
        raw=tp.read_bytes();receipt=json.loads(trp.read_text())
        if receipt['url']!=TREE_URL or receipt['sha256']!=sha(raw):raise ValueError('Cached tree changed')
    else:
        raw,receipt=get(TREE_URL);checked_tree(raw)
        save(tp,raw);save(trp,encode(dict(receipt,bytes=len(raw),sha256=sha(raw),commit=PIN)))
    entries=checked_tree(raw);receipts=[];new_count=0
    for item in plan():
        entry=entries[item['original_path']]
        r=cached(directory,item,entry)
        if r is None:
            raw,access=get(item['url']);blob=verify_file(raw,entry)
            r=dict(item,**{k:v for k,v in access.items() if k!='url'},bytes=len(raw),sha256=sha(raw),git_blob_sha1=blob,
                   licence='CC0-1.0 for rights held; third-party rights and model-training clearance unresolved',
                   source_metadata=[f'{REPO}/README.md',f'{REPO}/LICENSE.md',f'{REPO}/NOTES.md'],
                   phase2_metadata_manifest_sha256=sha((directory/'acquisition.json').read_bytes()))
            p=directory/item['path'];save(p,raw);save(p.with_name(p.name+'.provenance.json'),encode(r));new_count+=1
            print('ACQUIRED',item['season'],len(raw),flush=True)
        else:print('REUSED_CACHED',item['season'],flush=True)
        receipts.append(r)
    reused=[]
    for r in old['files']:
        if r['kind']=='dataset':
            item=dict(r,competition='La Liga / Primera División',acquisition='REUSED_PHASE2')
            if r['path'].endswith('spain.csv'):item['selected_seasons']=[f'{y}/{y+1}' for y in range(1990,2012)]
            else:item['selected_seasons']=['2012/2013' if '/2012-13/' in r['path'] else '2025/2026']
            reused.append(item)
    manifest=dict(scope='Phase 3 acquisition only; 1990/1991–2025/2026',additional_files=receipts,reused_phase2_datasets=reused,
                  approved_additional_files=12,source_dataset_files=15,source_seasons=36,
                  tree_sha256=sha(tp.read_bytes()),phase2_acquisition_sha256=sha((directory/'acquisition.json').read_bytes()),
                  phase2_diagnostics_sha256=sha((directory/'feasibility_diagnostics.json').read_bytes()),
                  preservation=protect(directory),rights=old['rights'],
                  limits='No source merge, results correction, standardization, historical certification, integration or training.')
    target=directory/MANIFEST;content=encode(manifest)
    if target.exists():
        if target.read_bytes()!=content:raise ValueError('Saved Phase 3 acquisition manifest differs')
    else:save(target,content)
    print('PASS',preservation,'new this invocation',new_count,'cached additional',12-new_count,flush=True)


if __name__=='__main__':collect()
