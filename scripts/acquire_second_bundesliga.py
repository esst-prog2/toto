"""Bounded direct-export retrieval for the second-tier source study, never scraping.

Network calls occur only via explicit fetch calls. Original responses and receipts
remain private, immutable and checksum-verified; no DFB or Kicker requests allowed.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

PRIVATE = Path(__file__).resolve().parents[1]/'data/private/germany/second_bundesliga'
LAST_REQUEST = None


def sha(content):
    return hashlib.sha256(content).hexdigest()


def save_once(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != content:
            raise ValueError('Refusing changed artifact: '+str(path))
    else:
        with path.open('xb') as handle:
            handle.write(content)


def fetch(url, relative):
    """One paced allowed export request; verified cache hits never request again."""
    global LAST_REQUEST
    if urlsplit(url).scheme != 'https' or urlsplit(url).netloc not in {'api.github.com','raw.githubusercontent.com'}:
        raise ValueError('Only public GitHub metadata/raw exports supported; no site scraping')
    path=(PRIVATE/relative).resolve()
    if not path.is_relative_to(PRIVATE.resolve()):
        raise ValueError('Output escapes private storage')
    receipt=path.with_name(path.name+'.provenance.json')
    stop=PRIVATE/'ACCESS_STOP.json'
    if receipt.exists():
        entry=json.loads(receipt.read_text());content=path.read_bytes()
        if entry['url'] != url or sha(content) != entry['sha256']:
            raise ValueError('Cached source identity/checksum changed')
        return content
    if path.exists():
        raise ValueError('Existing response without receipt; inspect before resuming')
    if stop.exists():
        raise RuntimeError('Explicit access stop is active; no further requests')
    if LAST_REQUEST is not None:
        time.sleep(max(0,5-(time.monotonic()-LAST_REQUEST)))
    LAST_REQUEST=time.monotonic()
    try:
        with urlopen(Request(url,headers={'User-Agent':'TOTOdology-PrivateDatasetStudy/1.0','Accept':'application/vnd.github+json' if 'api.github.com' in url else '*/*'}),timeout=60) as response:
            content=response.read()
            entry=dict(url=url,final_url=response.url,status=response.status,
                       retrieved_at=datetime.now(timezone.utc).isoformat(),
                       headers={k:v for k,v in response.headers.items() if k.lower()!='set-cookie'},
                       sha256=sha(content),bytes=len(content))
            if response.status!=200 or response.headers.get('Retry-After'):
                raise RuntimeError('Unexpected status or Retry-After; stop')
    except HTTPError as exc:
        body=exc.read();error=dict(url=url,status=exc.code,retrieved_at=datetime.now(timezone.utc).isoformat(),sha256=sha(body))
        save_once(PRIVATE/'failures'/(sha(body)+'.body'),body)
        save_once(PRIVATE/'failures'/(sha(body)+'.json'),(json.dumps(error,indent=2)+'\n').encode())
        if exc.code in (401,403,429,451):save_once(stop,(json.dumps(error,indent=2)+'\n').encode())
        raise
    save_once(path,content)
    save_once(receipt,(json.dumps(entry,indent=2,ensure_ascii=False)+'\n').encode())
    print('SAVED',relative,len(content),flush=True)
    return content


PINS = {
    'engsoccerdata': ('jalapic/engsoccerdata','872c5c354161ace8408f3091b758c6af4cccca94'),
    'allbundesliga': ('thomascamminady/AllBundesligaGamesEver','9da303b7f8ee074c53f64f8f1f54b58013d3a9c3'),
    'openfootball': ('openfootball/deutschland','c34532ab6950aa0089ef1c736ffdb8c818c3356f'),
}


def main():
    """Reproduce the bounded, inspected export snapshot, never follow live branches."""
    paths = {
        'engsoccerdata': [('README.md','metadata/engsoccerdata/README.md'),
                         ('DESCRIPTION','metadata/engsoccerdata/DESCRIPTION'),
                         ('man/germany.Rd','metadata/engsoccerdata/man/germany.Rd'),
                         ('data-raw/munge/germany_munge.R','metadata/engsoccerdata/data-raw/munge/germany_munge.R'),
                         ('data-raw/germany.csv','originals/engsoccerdata_germany.csv')],
        'allbundesliga': [('README.md','metadata/allbundesliga/README.md'),('LICENSE','metadata/allbundesliga/LICENSE'),
                         ('AllBundesligaGamesEver.csv','originals/AllBundesligaGamesEver.csv')],
        'openfootball': [('README.md','metadata/openfootball/README.md'),('LICENSE.md','metadata/openfootball/LICENSE.md'),
                         ('openliga/README.md','metadata/openfootball/openliga/README.md'),
                         ('2025-26/2-bundesliga2.txt','originals/openfootball_2025-26_2-bundesliga2.txt'),
                         ('openliga/2025-26_de.2.txt','originals/openfootball_openliga_2025-26_de.2.txt')],
    }
    for source, entries in paths.items():
        repo,commit=PINS[source]
        for source_path,target in entries:
            fetch(f'https://raw.githubusercontent.com/{repo}/{commit}/{source_path}',target)
    print('PASS: bounded pinned exports and notices present; cached responses checksum-verified.')


if __name__ == '__main__':
    main()
