"""Bounded Segunda Phase 2 acquisition; five originals, no automatic retries.

Git metadata/notices are reused from the immutable La Liga evidence bundle.
No season outside PLAN is requested; all acquired bytes remain Git-ignored.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import time
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = ROOT / 'data/private/spain/segunda_division'
PIN = '80035a93dd4920985af52aa097a54a6fb888563b'
REPO = 'openfootball/espana'
RSSSF = 'https://www.rsssf.org/tabless/span97.html'
YEARS = (2012, 2018, 2019, 2025)
PLAN = tuple(dict(season=f'{y}/{y+1}', path=f'{REPO}/{y}-{(y+1)%100:02}/2-liga2.txt',
                  original_path=f'{y}-{(y+1)%100:02}/2-liga2.txt', commit=PIN,
                  url=f'https://raw.githubusercontent.com/{REPO}/{PIN}/{y}-{(y+1)%100:02}/2-liga2.txt',
                  source='OpenFootball', format='Football.TXT') for y in YEARS) + (
    dict(season='1996/1997', path='rsssf/span97.html', original_path='tabless/span97.html',
         commit=None, url=RSSSF, source='RSSSF', format='HTML'),)
RIGHTS = {
    'OpenFootball': 'CC0-1.0 for rights held; third-party provenance/rights not warranted. Model-training clearance unresolved.',
    'RSSSF': 'Juan Pedro Adrados and RSSSF 1999/2000; copying permitted with author acknowledgement, all rights reserved. Model-training and redistribution scope require separate assessment.'}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encode(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + '\n').encode()


def save(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(raw)


def now():
    return datetime.now(timezone.utc).isoformat()


def initialize(directory=PRIVATE, root=ROOT):
    """Freeze all seven prior private bundles plus tracked public implementation."""
    target = directory / 'protected_before.json'
    if target.exists():
        protect(directory, root)
        return
    if directory.exists() and any(directory.iterdir()):
        raise ValueError('Partial initialization; inspect rather than overwrite')
    if not directory.resolve().is_relative_to((root/'data/private').resolve()):
        raise ValueError('Working area must be private')
    tracked = subprocess.check_output(['git', '--no-optional-locks', 'ls-files', '-z'], cwd=root).decode().split('\0')
    files = {str(p.relative_to(root)): sha(p.read_bytes()) for p in (root/'data/private').rglob('*')
             if p.is_file() and not p.is_relative_to(directory)}
    if not files:
        raise ValueError('No previous competition baseline')
    public = {n: sha((root/n).read_bytes()) for n in tracked
              if n and n != 'PLANNING_LOG.md' and (root/n).is_file()}
    log = (root/'PLANNING_LOG.md').read_bytes()
    baseline = dict(private=files, public=public, planning_log=dict(bytes=len(log), sha256=sha(log)),
                    git_head=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root).decode().strip())
    save(target, encode(baseline))
    old = root/'data/private/spain/la_liga'
    acquisition = json.loads((old/'acquisition.json').read_text())
    notices = []
    for name in ('README.md', 'LICENSE.md', 'NOTES.md'):
        item = next(r for r in acquisition['files'] if r['path'] == f'{REPO}/{name}')
        raw = (old/item['path']).read_bytes()
        if item['commit'] != PIN or sha(raw) != item['sha256']:
            raise ValueError('Existing licence/provenance evidence changed')
        dest = 'metadata/'+name
        save(directory/dest, raw)
        notices.append(dict(path=dest, original_receipt=item, sha256=sha(raw), bytes=len(raw)))
    raw = (old/'phase3_git_tree.json').read_bytes()
    receipt = json.loads((old/'phase3_git_tree_receipt.json').read_text())
    if sha(raw) != receipt['sha256']:
        raise ValueError('Existing pinned Git tree receipt mismatch')
    checked_tree(raw)
    save(directory/'metadata/git_tree.json', raw)
    notices.append(dict(path='metadata/git_tree.json', original_receipt=receipt, sha256=sha(raw), bytes=len(raw)))
    save(directory/'metadata_receipts.json', encode(notices))
    protect(directory, root)


def protect(directory=PRIVATE, root=ROOT):
    baseline = json.loads((directory/'protected_before.json').read_text())
    for group in ('private', 'public'):
        if not baseline[group]:
            raise ValueError('Empty protected group')
        for name, digest in baseline[group].items():
            path = root/name
            if not path.resolve().is_relative_to(root.resolve()) or sha(path.read_bytes()) != digest:
                raise ValueError('Protected file changed: '+name)
    log = (root/'PLANNING_LOG.md').read_bytes(); prefix = baseline['planning_log']
    if len(log) < prefix['bytes'] or sha(log[:prefix['bytes']]) != prefix['sha256']:
        raise ValueError('Earlier planning history changed')
    return {group: len(baseline[group]) for group in ('private', 'public')}


def checked_tree(raw):
    tree = json.loads(raw)
    if tree.get('truncated') or tree.get('sha') != PIN:
        raise ValueError('Wrong/incomplete pinned tree')
    entries = {e['path']: e for e in tree['tree'] if e['type'] == 'blob'}
    if not {p['original_path'] for p in PLAN[:4]} <= entries.keys():
        raise ValueError('Approved Segunda path missing')
    return entries


def verify_metadata(directory):
    metadata = json.loads((directory/'metadata_receipts.json').read_text())
    expected = {'metadata/'+n for n in ('README.md', 'LICENSE.md', 'NOTES.md', 'git_tree.json')}
    if len(metadata) != 4 or {r['path'] for r in metadata} != expected:
        raise ValueError('Incomplete/changed supporting metadata registry')
    for r in metadata:
        raw = (directory/r['path']).read_bytes()
        if sha(raw) != r['sha256'] or len(raw) != r['bytes']:
            raise ValueError('Reused metadata changed')
    if not (directory/'metadata/LICENSE.md').read_text().startswith('CC0 1.0 Universal'):
        raise ValueError('OpenFootball licence requires review')
    return checked_tree((directory/'metadata/git_tree.json').read_bytes())


def verify(raw, item, entries):
    if item['source'] == 'OpenFootball':
        entry = entries[item['original_path']]
        blob = hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        if len(raw) != entry['size'] or blob != entry['sha']:
            raise ValueError('Pinned Git blob/size mismatch')
        return blob
    # Verify document identity and attribution, not truth of every historical fact.
    text = raw.decode('latin-1')
    required = ('Spain 1996/97', 'Spain Segunda Division A 1996/97',
                'Juan Pedro Adrados', 'You are free to copy', 'All rights reserved')
    if not all(s in text for s in required):
        raise ValueError('Unexpected RSSSF document or access/attribution notice')
    return None


def cached(directory, item, entries):
    file = directory/item['path']; receipt = file.with_name(file.name+'.provenance.json')
    if not file.exists() and not receipt.exists():
        return None
    if not file.exists() or not receipt.exists():
        raise ValueError('Incomplete source/receipt; manual inspection required')
    raw = file.read_bytes(); saved = json.loads(receipt.read_text())
    blob = verify(raw, item, entries)
    if any(saved[k] != v for k, v in item.items()) or saved['sha256'] != sha(raw) or saved['bytes'] != len(raw) or saved['git_blob_sha1'] != blob:
        raise ValueError('Cached source/receipt mismatch')
    return saved


def collect(directory=PRIVATE, root=ROOT):
    protection = protect(directory, root)
    entries = verify_metadata(directory)
    receipts = []; last = None
    for item in PLAN:
        saved = cached(directory, item, entries)
        if saved is None:
            if (directory/'ACCESS_STOP.json').exists():
                raise RuntimeError('Prior access failure: stop, no automatic retry')
            if last is not None:
                time.sleep(max(0, 5-(time.monotonic()-last)))
            last = time.monotonic()
            try:
                request = Request(item['url'], headers={'User-Agent': 'ThePickSheet-bounded-Segunda-feasibility'})
                with urlopen(request, timeout=30) as response:
                    final = response.url
                    if response.status != 200 or response.headers.get('Retry-After'):
                        raise ValueError('Unexpected status/Retry-After')
                    u = urlsplit(final); expected = urlsplit(item['url'])
                    if u.scheme != 'https' or u.hostname != expected.hostname or u.path != expected.path or u.query:
                        raise ValueError('Unexpected source redirect')
                    raw = response.read(2_000_001)
                    if len(raw) > 2_000_000:
                        raise ValueError('Bounded response size exceeded')
                    headers = {k: response.headers.get(k) for k in ('Content-Type', 'Last-Modified', 'ETag')}
                blob = verify(raw, item, entries)
            except Exception as exc:
                save(directory/'ACCESS_STOP.json', encode(dict(url=item['url'], error=str(exc), timestamp_utc=now())))
                raise
            saved = dict(item, final_url=final, retrieved_at_utc=now(), original_filename=Path(item['path']).name,
                         bytes=len(raw), sha256=sha(raw), git_blob_sha1=blob, headers=headers,
                         attribution='openfootball contributors' if blob else 'Juan Pedro Adrados and RSSSF, 1999/2000',
                         licensing=RIGHTS[item['source']], snapshot_identity='SHA256:'+sha(raw))
            file = directory/item['path']; save(file, raw)
            save(file.with_name(file.name+'.provenance.json'), encode(saved))
        receipts.append(saved)
    value = dict(scope='Segunda Phase 2 only: five approved originals', files=receipts,
                 protected=protection, rights=RIGHTS, metadata_sha256=sha((directory/'metadata_receipts.json').read_bytes()))
    raw = encode(value); target = directory/'acquisition.json'
    if target.exists():
        if target.read_bytes() != raw:
            raise ValueError('Acquisition manifest changed')
    else:
        save(target, raw)
    protect(directory, root)
    return value


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--init', action='store_true'); args = parser.parse_args()
    if args.init:
        initialize()
    result = collect()
    print('VERIFIED_OR_ACQUIRED', len(result['files']), 'PROTECTED', result['protected'])


if __name__ == '__main__':
    main()
