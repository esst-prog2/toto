"""Turkish Phase 1: bounded, immutable originals/receipts; no adjudication.

Explicit private plan; verified offline replay never requests a cached original.
Network is opt-in. Source permissions must be recorded before fixture acquisition.
"""
from pathlib import Path
import argparse
import json
import time
from urllib.parse import urlsplit
from urllib.request import Request, build_opener
from scripts import collect_ligue1_feasibility as common
from scripts.artifact_io import check_overwrite

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = ROOT / 'data/private/turkey/super_lig/phase1'
sha, encode, now = common.sha, common.encode, common.now
ALLOWED_HOSTS = {'raw.githubusercontent.com', 'api.github.com', 'football-data.co.uk', 'www.rsssf.org', 'www.tff.org'}


def save(path, raw):
    check_overwrite([path])
    common.save(path, raw)


def destination(directory, relative):
    path = directory / relative
    if Path(relative).is_absolute() or not path.resolve().is_relative_to(directory.resolve()):
        raise ValueError('Path escapes private scope')
    return path


def validate_plan(plan):
    if plan.get('phase') != 1 or not plan.get('scope') or not plan.get('items'):
        raise ValueError('Invalid Phase 1 plan')
    paths, urls = set(), set()
    for item in plan['items']:
        u = urlsplit(item['url'])
        if u.scheme != 'https' or u.hostname not in ALLOWED_HOSTS or u.username or u.password or u.fragment:
            raise ValueError('Unapproved URL')
        destination(PRIVATE, item['path'])
        if item['path'] in paths or item['url'] in urls:
            raise ValueError('Duplicate source destination/URL')
        paths.add(item['path']); urls.add(item['url'])
        if not all(item.get(k) for k in ('publisher', 'licensing', 'permission_basis', 'kind')):
            raise ValueError('Missing source permission/provenance')
        if item['kind'] == 'fixture' and not item.get('permission_reference'):
            raise ValueError('Fixture needs prior permission evidence')
        if not isinstance(item['max_bytes'], int) or not 0 < item['max_bytes'] <= 2_000_000:
            raise ValueError('Unbounded source')
        if item.get('expected_blob') and not item.get('commit'):
            raise ValueError('Unpinned Git blob')
    return plan


def verify(directory, item, receipt):
    path = destination(directory, item['path']); raw = path.read_bytes()
    if any(receipt.get(k) != v for k, v in item.items()):
        raise ValueError('Receipt differs from approved item')
    if receipt.get('sha256') != sha(raw) or receipt.get('bytes') != len(raw):
        raise ValueError('Original checksum mismatch')
    if not receipt.get('retrieved_at_utc') or receipt.get('status') != 200 or receipt.get('final_url') != item['url']:
        raise ValueError('Invalid retrieval provenance')
    if item.get('expected_blob'):
        common.verify_blob(raw, {'sha': item['expected_blob'], 'size': item['expected_bytes']})
    return raw


def acquire(directory, item, *, network=False, opener=None):
    if network and (directory/'BLOCKED.json').exists():
        raise RuntimeError('Phase blocked; new network execution requires owner review')
    path = destination(directory, item['path'])
    receipt_path = path.with_name(path.name + '.provenance.json')
    stop = directory / 'access' / (sha(item['url'].encode()) + '.STOP.json')
    if path.exists() != receipt_path.exists():
        raise ValueError('Partial original/receipt pair; inspect manually')
    if path.exists():
        receipt = json.loads(receipt_path.read_bytes())
        verify(directory, item, receipt)
        return receipt, False
    if stop.exists():
        raise RuntimeError('Prior access stop; no retry')
    if not network:
        raise FileNotFoundError('Offline original missing: ' + item['path'])
    if item['kind'] == 'fixture':
        permission = destination(directory, item['permission_reference'])
        if not permission.is_file() or not permission.with_name(permission.name + '.provenance.json').is_file():
            raise ValueError('Permission evidence not acquired')
        notice = json.loads(permission.with_name(permission.name + '.provenance.json').read_bytes())
        if sha(permission.read_bytes()) != notice.get('sha256') or notice['sha256'] != item.get('permission_sha256'):
            raise ValueError('Permission evidence checksum mismatch')
    started = time.monotonic()
    try:
        client = opener or build_opener(common.NoRedirect)
        with client.open(Request(item['url'], headers={'User-Agent': 'TOTOdology-private-academic-source-assessment/1.0'}), timeout=25) as response:
            if response.status != 200 or response.url != item['url'] or response.headers.get('Retry-After'):
                raise ValueError('Restricted/redirected response')
            raw = response.read(item['max_bytes'] + 1)
            if len(raw) > item['max_bytes']:
                raise ValueError('Source exceeds acquisition bound')
            headers = {k: v for k, v in response.headers.items() if k.lower() != 'set-cookie'}
        if item.get('expected_blob'):
            common.verify_blob(raw, {'sha': item['expected_blob'], 'size': item['expected_bytes']})
        raw.decode(item.get('encoding', 'utf-8-sig'))
    except Exception as exc:
        save(stop, encode(dict(url=item['url'], retrieved_at_utc=now(), error=str(exc), elapsed_seconds=time.monotonic()-started)))
        raise
    receipt = dict(item, sha256=sha(raw), bytes=len(raw), retrieved_at_utc=now(),
                   status=200, final_url=item['url'], response_headers=headers,
                   request_elapsed_seconds=time.monotonic()-started,
                   original_filename=path.name, constraints='Private academic feasibility only; no training, publication, bypass or automatic retry')
    save(path, raw); save(receipt_path, encode(receipt))
    return receipt, True


def run(directory=PRIVATE, *, network=False, plan_name='source_plan.json'):
    if not directory.resolve().is_relative_to((ROOT/'data/private').resolve()):
        raise ValueError('Destination must be private')
    plan = validate_plan(json.loads(destination(directory,plan_name).read_bytes()))
    result=[]
    for item in plan['items']:
        receipt, downloaded = acquire(directory, item, network=network)
        result.append(dict(path=item['path'],sha256=receipt['sha256'],bytes=receipt['bytes'],downloaded=downloaded))
        print(('ACQUIRED' if downloaded else 'VERIFIED CACHE'),item['path'],receipt['bytes'],flush=True)
        if downloaded:time.sleep(1)
    return result


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--network',action='store_true')
    parser.add_argument('--plan',default='source_plan.json')
    args=parser.parse_args()
    run(network=args.network,plan_name=args.plan)
