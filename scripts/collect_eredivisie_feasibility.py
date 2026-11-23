"""Exactly six approved Eredivisie originals; immutable cache, no retries or redirects."""
import argparse
import json
import subprocess
import time
from urllib.request import Request, build_opener
from scripts import collect_ligue1_feasibility as base

ROOT=base.ROOT
PRIVATE=ROOT/'data/private/netherlands/eredivisie'
HIST='jalapic/engsoccerdata'
MODERN='openfootball/europe'
PINS={HIST:'872c5c354161ace8408f3091b758c6af4cccca94',MODERN:'63df627f3c87ce71708f016522ea236cf74332c3'}
YEARS=(2018,2019,2023,2024,2025)
RIGHTS={HIST:'Noncommercial use with attribution in README; GPL >=2 package metadata. Underlying data/upstream rights, redistribution and model-training clearance unresolved. Private feasibility only.',MODERN:'CC0-1.0 for rights held; upstream provenance and third-party clearance not warranted. Model-training and redistribution clearance unresolved.'}
sha,encode,save,now=base.sha,base.encode,base.save,base.now


def plan():
    return [dict(repository=repo,commit=PINS[repo],original_path=path,path=f'{repo}/{path}',url=f'https://raw.githubusercontent.com/{repo}/{PINS[repo]}/{path}',season=season) for repo,path,season in [(HIST,'data-raw/holland.csv','MULTISEASON'),*[(MODERN,f'netherlands/{y}-{(y+1)%100:02}_nl1.txt',f'{y}/{y+1}') for y in YEARS]]]


def initialize(directory=PRIVATE,root=ROOT):
    if (directory/'protected_before.json').exists():return protect(directory,root)
    if subprocess.check_output(['git','branch','--show-current'],cwd=root).decode().strip()!='feature/data-collection' or subprocess.check_output(['git','rev-parse','HEAD'],cwd=root).decode().strip()!='4f8c64433cf6168a06dbde0102e822ce6d2eeffa':raise ValueError('Unexpected branch/HEAD')
    if directory.exists() and any(directory.iterdir()):raise ValueError('Partial initialization')
    if not directory.resolve().is_relative_to((root/'data/private').resolve()):raise ValueError('Working area must be private')
    relative=str((directory/'probe').relative_to(root))
    if subprocess.run(['git','check-ignore','--quiet',relative],cwd=root).returncode:raise ValueError('Private area not ignored')
    files={str(p.relative_to(root)):sha(p.read_bytes()) for p in (root/'data/private').rglob('*') if p.is_file() and not p.is_relative_to(directory)}
    tracked=subprocess.check_output(['git','ls-files','-z'],cwd=root).decode().split('\0');public={n:sha((root/n).read_bytes()) for n in tracked if n and n!='PLANNING_LOG.md' and (root/n).is_file()}
    log=(root/'PLANNING_LOG.md').read_bytes()
    save(directory/'protected_before.json',encode(dict(private=files,public=public,planning_log=dict(bytes=len(log),sha256=sha(log)),git_head='4f8c64433cf6168a06dbde0102e822ce6d2eeffa')))
    return protect(directory,root)


def protect(directory=PRIVATE,root=ROOT):return base.protect(directory,root)


def metadata(directory=PRIVATE):
    previous=ROOT/'data/private/france/ligue_1';base.verify_originals(previous);trees={}
    for repo in PINS:
        source=previous/'metadata'/repo/'git_tree.json';raw=source.read_bytes();r=json.loads(source.with_suffix('.receipt.json').read_text())
        if sha(raw)!=r['sha256'] or r['commit']!=PINS[repo]:raise ValueError('Retained Git tree identity changed')
        notices=('README.md','DESCRIPTION') if repo==HIST else ('README.md','LICENSE.md')
        paths=tuple(i['original_path'] for i in plan() if i['repository']==repo)+notices
        trees[repo]=base.tree_entries(raw,PINS[repo],paths)
        for target,content in [(directory/'metadata'/repo/'git_tree.json',raw),(directory/'metadata'/repo/'git_tree.receipt.json',encode(dict(r,reused_from=str(source.relative_to(ROOT)))) )]:
            if target.exists():
                if target.read_bytes()!=content:raise ValueError('Cached metadata changed')
            else:save(target,content)
        for name in notices:
            src=previous/repo/name;raw=src.read_bytes();base.verify_blob(raw,trees[repo][name]);rec=json.loads(src.with_name(src.name+'.provenance.json').read_text());dest=directory/repo/name
            for target,content in [(dest,raw),(dest.with_name(dest.name+'.provenance.json'),encode(dict(rec,reused_from=str(src.relative_to(ROOT)))) )]:
                if target.exists():
                    if target.read_bytes()!=content:raise ValueError('Cached notice changed')
                else:save(target,content)
    h=trees[HIST]['data-raw/holland.csv']
    if h['sha']!='a84a96a234e7e90dadd3c802b2a277d1e0df33dc' or h['size']!=1215520:raise ValueError('Approved historical identity mismatch')
    if 'non-commer' not in (directory/HIST/'README.md').read_text().lower() or 'GPL' not in (directory/HIST/'DESCRIPTION').read_text() or not (directory/MODERN/'LICENSE.md').read_text().startswith('CC0 1.0 Universal'):raise ValueError('Rights notices changed')
    return trees


def request(url,directory):
    if (directory/'ACCESS_STOP.json').exists():raise RuntimeError('Prior access failure: no retry')
    try:
        with build_opener(base.NoRedirect).open(Request(url,headers={'User-Agent':'ThePickSheet-Eredivisie-bounded-feasibility'}),timeout=30) as response:
            if response.status!=200 or response.url!=url or response.headers.get('Retry-After'):raise ValueError('Unexpected access response')
            raw=response.read(8000001)
            if len(raw)>8000000:raise ValueError('Response too large')
            return raw
    except Exception as exc:
        save(directory/'ACCESS_STOP.json',encode(dict(url=url,error=str(exc),retrieved_at_utc=now())));raise


def verify_record(directory,item,receipt,tree):
    raw=(directory/item['path']).read_bytes();blob=base.verify_blob(raw,tree[item['original_path']])
    expected=dict(item,bytes=len(raw),sha256=sha(raw),git_blob_sha1=blob,licensing=RIGHTS[item['repository']],kind='dataset')
    if any(receipt.get(k)!=v for k,v in expected.items()) or not receipt.get('retrieved_at_utc') or not receipt.get('attribution'):raise ValueError('Source receipt mismatch')
    return raw


def collect(directory=PRIVATE,root=ROOT):
    protected=protect(directory,root);trees=metadata(directory);receipts=[]
    for item in plan():
        dest=directory/item['path'];rec=dest.with_name(dest.name+'.provenance.json')
        if dest.exists()!=rec.exists():raise ValueError('Partial source/receipt pair')
        if dest.exists():
            r=json.loads(rec.read_text());verify_record(directory,item,r,trees[item['repository']])
        else:
            raw=request(item['url'],directory);blob=base.verify_blob(raw,trees[item['repository']][item['original_path']])
            r=dict(item,kind='dataset',bytes=len(raw),sha256=sha(raw),git_blob_sha1=blob,original_filename=dest.name,format=dest.suffix,retrieved_at_utc=now(),licensing=RIGHTS[item['repository']],attribution='James Curley' if item['repository']==HIST else 'OpenFootball contributors',retrieval='One bounded request; no retries/redirects; pinned blob verified before save',competition='Eredivisie; actual contents require assessment')
            save(dest,raw);save(rec,encode(r));time.sleep(2)
        receipts.append(r)
    result=dict(phase=2,scope='Exactly six approved originals; historical full bytes retained, detailed analysis limited to approved sample',files=receipts,rights=RIGHTS,protected=protected,source_independence='Not established from repository agreement')
    target=directory/'acquisition.json';raw=encode(result)
    if target.exists():
        if target.read_bytes()!=raw:raise ValueError('Acquisition manifest changed')
    else:save(target,raw)
    protect(directory,root);return result


def verify_originals(directory=PRIVATE):
    trees=metadata(directory);m=json.loads((directory/'acquisition.json').read_text());items=plan()
    if len(m['files'])!=6 or {r['path'] for r in m['files']}!={r['path'] for r in items} or m['rights']!=RIGHTS:raise ValueError('Acquisition scope changed')
    for item in items:
        r=next(x for x in m['files'] if x['path']==item['path']);verify_record(directory,item,r,trees[item['repository']])
        dest=directory/item['path']
        if json.loads(dest.with_name(dest.name+'.provenance.json').read_text())!=r:raise ValueError('Receipt/manifest differs')
    return m


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--init-only',action='store_true');args=parser.parse_args()
    if args.init_only:print(initialize());print('Verified pinned paths:',[(r['path'],metadata()[r['repository']][r['original_path']]['sha']) for r in plan()])
    else:print('VERIFIED_OR_ACQUIRED',len(collect()['files']))
