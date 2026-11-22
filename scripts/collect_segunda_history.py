"""Phase 3 only: ten approved pinned Segunda sources; preserve Phase 2.

No retry, extra dataset, overwrite, historical decision or standardization.
"""
import argparse
import json
from pathlib import Path
import subprocess
import time
from urllib.parse import urlsplit
from urllib.request import Request, HTTPRedirectHandler, build_opener

from scripts import collect_segunda_feasibility as base

ROOT, PRIVATE, PIN, REPO = base.ROOT, base.PRIVATE, base.PIN, base.REPO
YEARS = (2013, 2014, 2015, 2016, 2017, 2020, 2021, 2022, 2023, 2024)
REUSED = (2012, 2018, 2019)
BASELINE = 'phase3_protected_before.json'
MANIFEST = 'phase3_acquisition.json'
STOP = 'PHASE3_ACCESS_STOP.json'
PHASE2_PUBLIC = ('scripts/collect_segunda_feasibility.py', 'scripts/validate_segunda_feasibility.py',
                 'tests/test_segunda_feasibility.py', 'docs/segunda-division-feasibility.md')


def plan():
    return [dict(season=f'{y}/{y+1}', path=f'{REPO}/{y}-{(y+1)%100:02}/2-liga2.txt',
                 original_path=f'{y}-{(y+1)%100:02}/2-liga2.txt', commit=PIN,
                 url=f'https://raw.githubusercontent.com/{REPO}/{PIN}/{y}-{(y+1)%100:02}/2-liga2.txt',
                 source='OpenFootball', format='Football.TXT') for y in YEARS]


def initialize(directory=PRIVATE, root=ROOT):
    base.protect(directory, root)
    target = directory/BASELINE
    if target.exists():
        return protect(directory, root)
    phase2 = directory/'phase2_verification.json'
    verification = json.loads(phase2.read_text())
    # Check the actual approved Phase 2 run, not merely a newly calculated baseline.
    for name, digest in verification['artifacts_before_receipt'].items():
        if base.sha((directory/name).read_bytes()) != digest:
            raise ValueError('Phase 2 artifact differs from approved verification: '+name)
    for name, digest in verification['public_sha256'].items():
        if base.sha((root/name).read_bytes()) != digest:
            raise ValueError('Phase 2 public file differs from approved verification: '+name)
    files = {str(p.relative_to(root)): base.sha(p.read_bytes()) for p in directory.rglob('*') if p.is_file()}
    files.update({n: base.sha((root/n).read_bytes()) for n in PHASE2_PUBLIC})
    log = (root/'PLANNING_LOG.md').read_bytes()
    base.save(target, base.encode(dict(files=files, planning_log=dict(bytes=len(log), sha256=base.sha(log)),
                                      head=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root).decode().strip())))
    return protect(directory, root)


def protect(directory=PRIVATE, root=ROOT):
    previous = base.protect(directory, root)
    baseline = json.loads((directory/BASELINE).read_text())
    if not baseline['files']:
        raise ValueError('Empty Phase 3 preservation baseline')
    for name, digest in baseline['files'].items():
        path = root/name
        if not path.resolve().is_relative_to(root.resolve()) or base.sha(path.read_bytes()) != digest:
            raise ValueError('Frozen Phase 2 artifact changed: '+name)
    log = (root/'PLANNING_LOG.md').read_bytes(); prefix = baseline['planning_log']
    if len(log) < prefix['bytes'] or base.sha(log[:prefix['bytes']]) != prefix['sha256']:
        raise ValueError('Existing planning history changed')
    return dict(previous_competitions=previous, phase2_files=len(baseline['files']))


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError('Redirect forbidden; stop before requesting a different URL')


def fetch(request, timeout):
    return build_opener(NoRedirect()).open(request, timeout=timeout)


def collect(directory=PRIVATE, root=ROOT):
    preservation = protect(directory, root)
    entries = base.verify_metadata(directory)
    items = plan()
    if any(i['original_path'] not in entries for i in items):
        raise ValueError('Approved path absent from complete pinned Git tree')
    phase2 = json.loads((directory/'acquisition.json').read_text())
    for item, saved in zip(base.PLAN, phase2['files'], strict=True):
        if base.cached(directory, item, entries) != saved:
            raise ValueError('Phase 2 receipt/source changed')
    last = None; receipts = []; new = 0
    for item in items:
        receipt = base.cached(directory, item, entries)
        if receipt is None:
            if (directory/STOP).exists():
                raise RuntimeError('Prior access stop requires review, not automatic retry')
            if last is not None:
                time.sleep(max(0, 5-(time.monotonic()-last)))
            last = time.monotonic()
            try:
                request = Request(item['url'], headers={'User-Agent': 'ThePickSheet-bounded-Segunda-phase3'})
                with fetch(request, timeout=30) as response:
                    if response.status != 200 or response.headers.get('Retry-After') or response.url != item['url']:
                        raise ValueError('Unexpected status/Retry-After/URL')
                    raw = response.read(2_000_001)
                    if len(raw) > 2_000_000:
                        raise ValueError('Response size limit exceeded')
                    headers = {k: response.headers.get(k) for k in ('Content-Type', 'Last-Modified', 'ETag')}
                blob = base.verify(raw, item, entries)
            except Exception as exc:
                base.save(directory/STOP, base.encode(dict(url=item['url'], error=str(exc), timestamp_utc=base.now())))
                raise
            receipt = dict(item, final_url=item['url'], retrieved_at_utc=base.now(), original_filename='2-liga2.txt',
                           bytes=len(raw), sha256=base.sha(raw), git_blob_sha1=blob, headers=headers,
                           attribution='openfootball contributors', licensing=base.RIGHTS['OpenFootball'],
                           snapshot_identity='SHA256:'+base.sha(raw),
                           metadata_registry_sha256=base.sha((directory/'metadata_receipts.json').read_bytes()))
            file = directory/item['path']; base.save(file, raw)
            base.save(file.with_name(file.name+'.provenance.json'), base.encode(receipt)); new += 1
            print('ACQUIRED', item['season'], receipt['bytes'], flush=True)
        else:
            print('REUSED_CACHE', item['season'], flush=True)
        receipts.append(receipt)
    reused = [r for r in phase2['files'] if int(r['season'][:4]) in REUSED]
    if len(reused) != 3:
        raise ValueError('Wrong reused modern scope')
    value = dict(scope='Phase 3 only: 2012/13–2024/25 modern source inventory', commit=PIN,
                 acquired=receipts, reused_phase2=reused, approved_new_files=10, modern_sources=13,
                 preservation=preservation, metadata_registry_sha256=base.sha((directory/'metadata_receipts.json').read_bytes()),
                 gaps=dict(older='1990/91–2011/12: 22 seasons without approved complete source',
                           newer='2025/26 pinned sample preserved separately: 131 scored / 331 unscored'),
                 rights=base.RIGHTS, limits='No correction, exclusion, identity mapping, historical certification or training clearance')
    raw = base.encode(value); target = directory/MANIFEST
    if target.exists():
        if target.read_bytes() != raw:
            raise ValueError('Acquisition manifest changed')
    else:
        base.save(target, raw)
    protect(directory, root)
    print('NEW', new, 'CACHED', len(receipts)-new, 'PHASE2_REUSED', len(reused), flush=True)
    return value


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--init', action='store_true'); args = parser.parse_args()
    if args.init:
        initialize()
    collect()


if __name__ == '__main__':
    main()
