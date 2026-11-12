"""Download bounded, commit-pinned original files; never scrape websites.

Default destination is Git-ignored. Refuses existing destinations before network I/O.
Run: python3 -m scripts.collect_serie_a
The saved snapshot was retrieved 2026-11-12; reruns record their actual UTC timestamp.
Source terms were reviewed before selection; see docs/serie-a-validation.md.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

from scripts.artifact_io import check_overwrite

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = ROOT/'data/private/italy/serie_a'
SOURCES = [
    ('jalapic/engsoccerdata','872c5c354161ace8408f3091b758c6af4cccca94',
     ['README.md','DESCRIPTION','man/italy.Rd','data-raw/italy.csv']),
    ('openfootball/italy','48954d163c312aa705efacb64f771267031fe6eb',
     ['README.md','LICENSE.md','2025-26/1-seriea.txt','2025-26/1-seriea-full.txt']),
]


def collect(directory=PRIVATE):
    plan = [(repo,sha,path,directory/repo.split('/')[0]/path)
            for repo,sha,paths in SOURCES for path in paths]
    check_overwrite([*(dest for _,_,_,dest in plan),directory/'acquisition.json'])
    manifest, downloads = [], []
    for repo,sha,path,dest in plan:
        url=f'https://raw.githubusercontent.com/{repo}/{sha}/{path}'
        with urlopen(url,timeout=60) as response:
            content=response.read()
        manifest.append(dict(file=str(dest.relative_to(directory)),url=url,
                             repository='https://github.com/'+repo,commit=sha,
                             retrieval_date=datetime.now(timezone.utc).date().isoformat(),
                             retrieved_at_utc=datetime.now(timezone.utc).isoformat(),
                             bytes=len(content),sha256=hashlib.sha256(content).hexdigest()))
        downloads.append((dest,content))
    for dest,content in downloads:
        dest.parent.mkdir(parents=True,exist_ok=True)
        with dest.open('xb') as handle: handle.write(content)
    with (directory/'acquisition.json').open('x') as handle:
        json.dump(manifest,handle,indent=2);handle.write('\n')


if __name__ == '__main__': collect()
