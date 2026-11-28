"""Phase 1 immutable, bounded private acquisition; offline verification by default.

Plans and raw data remain private. No normalization, historical adjudication,
production imports, unreviewed redirects, authentication or automatic network retries.
"""
import argparse
import hashlib
import json
import re
import html
from pathlib import Path
from urllib.parse import urlsplit
from urllib.error import HTTPError
from urllib.request import Request, build_opener, HTTPRedirectHandler
from scripts import collect_turkish_super_lig_sources as common

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'data/private/europe/europa_league/phase1'
HOSTS = {'api.github.com', 'raw.githubusercontent.com', 'www.rsssf.org', 'en.wikipedia.org', 'github.com'}
sha, encode, save, now = common.sha, common.encode, common.save, common.now



class ReleaseRedirect(HTTPRedirectHandler):
    """Only GitHub's documented public release distribution redirect."""
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        old, new = urlsplit(req.full_url), urlsplit(newurl)
        if old.hostname != 'github.com' or new.hostname != 'release-assets.githubusercontent.com' or new.scheme != 'https' or new.username or new.password:
            raise ValueError('Unapproved release redirect')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def validate(item, base=BASE):
    u = urlsplit(item['url'])
    if u.scheme != 'https' or u.hostname not in HOSTS or u.username or u.password or u.fragment:
        raise ValueError('Unapproved acquisition URL')
    p = common.destination(base, item['path'])
    if not base.resolve().is_relative_to((ROOT/'data/private').resolve()):
        raise ValueError('Acquisition must remain private')
    if not 0 < item['max_bytes'] <= 150_000_000:
        raise ValueError('Unbounded request')
    if not item.get('permission_basis') or not item.get('publisher'):
        raise ValueError('Missing permission/provenance')
    if item.get('expected_blob') and not item.get('commit'):
        raise ValueError('Git blob must be pinned')
    if item.get('kind') == 'fixture' and not (item.get('permission_reference') or item.get('page_copy_grant')):
        raise ValueError('Fixture requires permission evidence')
    return p


def verify(item, base=BASE):
    p = validate(item, base)
    raw = p.read_bytes(); receipt = json.loads(p.with_name(p.name+'.provenance.json').read_bytes())
    if any(receipt.get(k) != v for k, v in item.items()):
        raise ValueError('Receipt/plan mismatch')
    if receipt['sha256'] != sha(raw) or receipt['bytes'] != len(raw) or receipt['status'] != 200 or (not item.get('official_release_redirect') and receipt['final_url'] != item['url']):
        raise ValueError('Invalid original integrity/provenance')
    if item.get('official_release_redirect') and urlsplit(receipt['final_url']).hostname not in {'github.com','release-assets.githubusercontent.com'}:
        raise ValueError('Unapproved release destination')
    if not receipt.get('retrieved_at_utc'):
        raise ValueError('Missing acquisition date')
    verify_permission(item, base)
    check_content(item, raw)
    return receipt


def check_content(item, raw):
    if item.get('expected_bytes') is not None and len(raw) != item['expected_bytes']:
        raise ValueError('Original size differs')
    if not raw or len(raw) > item['max_bytes']:
        raise ValueError('Empty or oversized original')
    if item.get('expected_sha256') and sha(raw) != item['expected_sha256']:
        raise ValueError('Release digest differs')
    if item.get('expected_blob'):
        common.common.verify_blob(raw, {'sha':item['expected_blob'], 'size':item['expected_bytes']})
    if item.get('encoding'):
        text = raw.decode(item['encoding'])
        if item.get('page_copy_grant') and 'You are free to copy this document' not in ' '.join(html.unescape(re.sub(r'<[^>]*>', ' ', text)).split()):
            raise ValueError('Page-specific copying permission absent')
        if item.get('contains') and item['contains'] not in text:
            raise ValueError('Expected competition/format marker absent')
    if item.get('format') == 'json':
        json.loads(raw)



def verify_permission(item, base):
    if item.get('permission_reference'):
        p = common.destination(base, item['permission_reference'])
        notice = json.loads(p.with_name(p.name+'.provenance.json').read_bytes())
        if sha(p.read_bytes()) != item['permission_sha256'] or notice['sha256'] != item['permission_sha256']:
            raise ValueError('Permission original differs')

def acquire(item, base=BASE, network=False):
    p = validate(item, base); receipt_path = p.with_name(p.name+'.provenance.json')
    if p.exists() != receipt_path.exists():
        raise ValueError('Partial source/receipt pair')
    if p.exists():
        return verify(item, base)
    if not network:
        raise FileNotFoundError(item['path'])
    host = urlsplit(item['url']).hostname
    stop = base/'access'/(host+'.STOP.json')
    if (base/'access'/(host+'.ACCESS_STOP.json')).exists():
        raise RuntimeError('Prior host denial; cached verification only')
    if stop.exists():
        failure = json.loads(stop.read_bytes())
        # A reviewed decoding correction is not an access-control workaround.
        recovery = base/'access'/(host+'.encoding-review.json')
        reviewed = json.loads(recovery.read_bytes()) if recovery.exists() else {}
        if not ("'utf-8' codec can't decode" in failure['error'] and item.get('encoding') == 'latin-1' and reviewed.get('stop_sha256') == sha(stop.read_bytes())):
            raise RuntimeError('Prior host access stop; cached verification only')
    verify_permission(item, base)
    try:
        with build_opener(ReleaseRedirect if item.get('official_release_redirect') else common.common.NoRedirect).open(Request(item['url'], headers={'User-Agent':'TOTOdology-private-academic-acquisition/1.0'}), timeout=45) as response:
            if response.status != 200 or (response.url != item['url'] and not item.get('official_release_redirect')) or response.headers.get('Retry-After'):
                raise ValueError('Restricted or redirected response')
            final_url = response.url.split('?')[0] if item.get('official_release_redirect') else response.url
            raw = response.read(item['max_bytes']+1)
            headers = {k:v for k,v in response.headers.items() if k.lower() != 'set-cookie'}
        check_content(item, raw)
    except Exception as exc:
        if (isinstance(exc, HTTPError) and exc.code in (401,403,429)) or 'redirect' in str(exc).lower() or 'Restricted' in str(exc):
            access_stop = base/'access'/(host+'.ACCESS_STOP.json')
            if not access_stop.exists():
                save(access_stop, encode(dict(url=item['url'], retrieved_at_utc=now(), error=str(exc))))
        failure_path = stop if not stop.exists() else base/'access'/(sha(item['url'].encode())+'.failure.json')
        save(failure_path, encode(dict(url=item['url'], retrieved_at_utc=now(), error=str(exc))))
        raise
    receipt = dict(item, sha256=sha(raw), bytes=len(raw), retrieved_at_utc=now(), status=200,
                   final_url=final_url, response_headers=headers, original_filename=p.name,
                   constraints='Private source assessment only; no redistribution/training clearance inferred')
    save(p, raw); save(receipt_path, encode(receipt))
    return receipt


def run(network=False, base=BASE):
    plan = json.loads((base/'source_plan.json').read_bytes())
    if plan['phase'] != 1:
        raise ValueError('Phase 1 only')
    paths = [x['path'] for x in plan['items']]
    if len(paths) != len(set(paths)) or len({x['url'] for x in plan['items']}) != len(paths):
        raise ValueError('Duplicate plan entries')
    receipts=[]
    for item in plan['items']:
        receipts.append(acquire(item,base,network))
    return receipts


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--network',action='store_true')
    args=parser.parse_args(); result=run(args.network)
    print('PASS',len(result),'payloads;',sum(x['bytes'] for x in result),'bytes')
