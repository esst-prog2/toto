"""One bounded feasibility acquisition: three revision-pinned Spain datasets.

Metadata first; no Football-Data requests, crawling, retries or remaining seasons.
All original bytes remain private. Refuse overwrites; require a protected baseline.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

from scripts.artifact_io import check_overwrite

ROOT=Path(__file__).resolve().parents[1]
PRIVATE=ROOT/'data/private/spain/la_liga'
SOURCES=[('jalapic/engsoccerdata','872c5c354161ace8408f3091b758c6af4cccca94',
          ['README.md','DESCRIPTION','man/spain.Rd'],['data-raw/spain.csv']),
         ('openfootball/espana','80035a93dd4920985af52aa097a54a6fb888563b',
          ['README.md','LICENSE.md','NOTES.md'],['2012-13/1-liga.txt','2025-26/1-liga.txt'])]


def sha(raw):return hashlib.sha256(raw).hexdigest()


def protected(directory):
    p=directory/'protected_competitions_before.json'
    files=json.loads(p.read_text())
    if not files:raise ValueError('Empty baseline')
    for name,digest in files.items():
        path=ROOT/name
        if not path.resolve().is_relative_to((ROOT/'data/private').resolve()) or sha(path.read_bytes())!=digest:
            raise ValueError('Protected artifact changed: '+name)
    return len(files)


def collect(directory=PRIVATE):
    protected(directory)
    plan=[(repo,commit,path,kind) for repo,commit,meta,data in SOURCES
          for kind,paths in [('metadata',meta),('dataset',data)] for path in paths]
    targets=[directory/repo/path for repo,_,path,_ in plan]
    check_overwrite([*targets,directory/'acquisition.json',directory/'source_paths.json'])
    # Inspect exact paths against the immutable tree before any file download.
    trees=[]
    for repo,commit,meta,data in SOURCES:
        url=f'https://api.github.com/repos/{repo}/git/trees/{commit}?recursive=1'
        with urlopen(Request(url,headers={'User-Agent':'TOTOdology-bounded-feasibility'}),timeout=45) as response:
            raw=response.read();tree=json.loads(raw)
        found={e['path']:e for e in tree['tree'] if e['type']=='blob'}
        if tree.get('truncated') or not set(meta+data)<=set(found):raise ValueError('Approved paths absent or incomplete tree')
        trees.append(dict(repository=repo,commit=commit,url=url,tree_response_sha256=sha(raw),
                          retrieved_at_utc=datetime.now(timezone.utc).isoformat(),
                          files={p:dict(blob=found[p]['sha'],bytes=found[p].get('size')) for p in meta+data}))
    downloads=[];receipts=[]
    # Preserve notices and verify applicable statements before fetching datasets.
    for stage in ('metadata','dataset'):
        for repo,commit,path,kind in plan:
            if kind!=stage:continue
            url=f'https://raw.githubusercontent.com/{repo}/{commit}/{path}'
            with urlopen(Request(url,headers={'User-Agent':'TOTOdology-bounded-feasibility'}),timeout=45) as response:
                if response.status!=200:raise ValueError('Unexpected source status')
                raw=response.read();final=response.url
            expected=next(t for t in trees if t['repository']==repo)['files'][path]
            blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
            if blob!=expected['blob'] or len(raw)!=expected['bytes']:raise ValueError('Git blob identity mismatch')
            downloads.append((repo,path,raw))
            receipts.append(dict(repository='https://github.com/'+repo,commit=commit,url=url,final_url=final,
                                 path=f'{repo}/{path}',original_filename=Path(path).name,kind=kind,
                                 format=Path(path).suffix.lstrip('.'),bytes=len(raw),sha256=sha(raw),git_blob_sha1=blob,
                                 retrieved_at_utc=datetime.now(timezone.utc).isoformat()))
        if stage=='metadata':
            texts={(repo,path):raw.decode('utf-8-sig') for repo,path,raw in downloads}
            if 'non-commer' not in texts[('jalapic/engsoccerdata','README.md')].lower():raise ValueError('Historical use notice changed; review required')
            if 'GPL' not in texts[('jalapic/engsoccerdata','DESCRIPTION')]:raise ValueError('Package licence changed')
            if not texts[('openfootball/espana','LICENSE.md')].startswith('CC0 1.0 Universal'):raise ValueError('OpenFootball licence changed')
    manifest=dict(scope='PHASE 2 ONLY: bounded feasibility, no full acquisition or standardization',files=receipts,
                  source_lineage='Compiler references preserved in READMEs and NOTES; independent lineage not established.',
                  rights={'jalapic/engsoccerdata':'Noncommercial use statement and GPL >=2 package metadata; dataset/upstream scope and model-training permission unresolved. Private academic feasibility only.',
                          'openfootball/espana':'CC0 1.0 for rights held; no third-party clearance warranty. No model training or redistribution authorized by this acquisition.'},
                  approved_datasets=3,protected_files=protected(directory))
    for repo,path,raw in downloads:
        dest=directory/repo/path;dest.parent.mkdir(parents=True,exist_ok=True)
        with dest.open('xb') as f:f.write(raw)
    for name,value in [('source_paths.json',trees),('acquisition.json',manifest)]:
        with (directory/name).open('x') as f:json.dump(value,f,indent=2,ensure_ascii=False,sort_keys=True);f.write('\n')
    print('Acquired',sum(r['kind']=='dataset' for r in receipts),'datasets and',sum(r['kind']=='metadata' for r in receipts),'metadata files')


if __name__=='__main__':collect()
