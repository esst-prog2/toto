"""Phase 3 only: seven approved Ligue 1 originals at the frozen Europe pin.

Reuse Phase 2 metadata/originals without rewriting. No retry or extra dataset.
"""
import argparse
import json
from pathlib import Path
import time

from scripts import collect_ligue1_feasibility as base

ROOT, PRIVATE = base.ROOT, base.PRIVATE
REPO = 'openfootball/europe'
PIN = '63df627f3c87ce71708f016522ea236cf74332c3'
YEARS = (2015, 2017, 2018, 2020, 2021, 2022, 2024)
REUSED = (2014, 2016, 2019, 2023, 2025)
BASELINE = 'phase3_protected_before.json'
MANIFEST = 'phase3_acquisition.json'


def plan():
    return [dict(repository=REPO, commit=PIN, season=f'{y}/{y+1}', competition='Ligue 1',
                 original_path=f'france/{y}-{(y+1)%100:02}_fr1.txt',
                 path=f'{REPO}/france/{y}-{(y+1)%100:02}_fr1.txt',
                 url=f'https://raw.githubusercontent.com/{REPO}/{PIN}/france/{y}-{(y+1)%100:02}_fr1.txt')
            for y in YEARS]


def initialize(directory=PRIVATE, root=ROOT):
    if (directory/BASELINE).exists():
        return protect(directory, root)
    base.protect(directory, root); base.verify_originals(directory)
    final = json.loads((directory/'phase2_final_verification.json').read_text())
    if final['status'] != 'COMPLETE_PENDING_USER_REVIEW' or final['tests']['repository_passed'] != 1110:
        raise ValueError('Wrong approved Phase 2 evidence')
    for name, record in final['private_files_before_this_receipt'].items():
        if base.sha((directory/name).read_bytes()) != record['sha256']:
            raise ValueError('Approved Phase 2 evidence changed: '+name)
    for name, digest in final['public_files'].items():
        if base.sha((root/name).read_bytes()) != digest:
            raise ValueError('Approved Phase 2 public work changed: '+name)
    files = {str(p.relative_to(root)): base.sha(p.read_bytes()) for p in directory.rglob('*') if p.is_file()}
    files.update({n: h for n,h in final['public_files'].items() if n != 'PLANNING_LOG.md'})
    log = (root/'PLANNING_LOG.md').read_bytes()
    base.save(directory/BASELINE, base.encode(dict(files=files, planning_log=dict(bytes=len(log), sha256=base.sha(log)))))
    return protect(directory, root)


def protect(directory=PRIVATE, root=ROOT):
    previous = base.protect(directory, root)
    baseline = json.loads((directory/BASELINE).read_text())
    if not baseline['files']:
        raise ValueError('Empty Phase 2 protection scope')
    for name, digest in baseline['files'].items():
        path = root/name
        if not path.resolve().is_relative_to(root.resolve()) or base.sha(path.read_bytes()) != digest:
            raise ValueError('Frozen Phase 2 artifact changed: '+name)
    prefix=baseline['planning_log'];log=(root/'PLANNING_LOG.md').read_bytes()
    if len(log)<prefix['bytes'] or base.sha(log[:prefix['bytes']])!=prefix['sha256']:
        raise ValueError('Phase 2 planning history changed')
    return dict(previous=previous, frozen_phase2_entries=len(baseline['files']))


def metadata(directory=PRIVATE):
    base.verify_originals(directory)
    raw=(directory/'metadata'/REPO/'git_tree.json').read_bytes()
    return base.tree_entries(raw, PIN, [p['original_path'] for p in plan()])


def cached(directory, item, entries):
    path=directory/item['path']; receipt=path.with_name(path.name+'.provenance.json')
    if not path.exists() and not receipt.exists():
        return None
    if path.exists()!=receipt.exists():
        raise ValueError('Incomplete original/receipt pair')
    raw=path.read_bytes();r=json.loads(receipt.read_text());blob=base.verify_blob(raw, entries[item['original_path']])
    required=dict(item,sha256=base.sha(raw),git_blob_sha1=blob,bytes=len(raw),kind='dataset',format='.txt',
                  licensing=base.RIGHTS[REPO], attribution='OpenFootball contributors')
    if any(r.get(k)!=v for k,v in required.items()):
        raise ValueError('Pinned original/receipt mismatch')
    return r


def collect(directory=PRIVATE, root=ROOT):
    protection=protect(directory,root);entries=metadata(directory);receipts=[]
    for item in plan():
        r=cached(directory,item,entries)
        if r is None:
            raw=base.request(item['url'], directory);blob=base.verify_blob(raw,entries[item['original_path']])
            r=dict(item,sha256=base.sha(raw),git_blob_sha1=blob,bytes=len(raw),kind='dataset',format='.txt',
                   original_filename=Path(item['original_path']).name,retrieved_at_utc=base.now(),
                   attribution='OpenFootball contributors',licensing=base.RIGHTS[REPO],
                   source_notices='Unchanged pinned README.md, LICENSE.md, france/README.md, france/NOTES.md and their Phase 2 receipts')
            target=directory/item['path'];base.save(target,raw);base.save(target.with_name(target.name+'.provenance.json'),base.encode(r))
            time.sleep(2)
        receipts.append(r)
    phase2=base.verify_originals(directory)
    reused=[r for r in phase2['files'] if r['kind']=='dataset' and r['repository']==REPO and not r['original_filename'].endswith('-full.txt')]
    if len(reused)!=5 or {int(r['original_filename'][:4]) for r in reused}!=set(REUSED):
        raise ValueError('Wrong Phase 2 ordinary-season reuse scope')
    value=dict(scope='Ligue 1 Phase 3 only: seven new, five reused ordinary originals',commit=PIN,
               acquired=receipts,reused_phase2=reused,modern_sources=12,
               phase2_acquisition_sha256=base.sha((directory/'acquisition.json').read_bytes()),
               protected=protection,rights=base.RIGHTS)
    content=base.encode(value);target=directory/MANIFEST
    if target.exists():
        if target.read_bytes()!=content:
            raise ValueError('Acquisition manifest changed')
    else:
        base.save(target,content)
    protect(directory,root)
    return value


def verify(directory=PRIVATE):
    entries=metadata(directory);manifest=json.loads((directory/MANIFEST).read_text())
    expected={p['path']:p for p in plan()}
    if (manifest['commit']!=PIN or manifest['modern_sources']!=12 or len(manifest['acquired'])!=7 or
            {r['path'] for r in manifest['acquired']}!=set(expected) or manifest['rights']!=base.RIGHTS or
            manifest['phase2_acquisition_sha256']!=base.sha((directory/'acquisition.json').read_bytes())):
        raise ValueError('Phase 3 manifest scope changed')
    for r in manifest['acquired']:
        if cached(directory,expected[r['path']],entries)!=r:
            raise ValueError('Manifest and per-file receipt differ')
    phase2=base.verify_originals(directory)
    reused=[r for r in phase2['files'] if r['kind']=='dataset' and r['repository']==REPO and not r['original_filename'].endswith('-full.txt')]
    if manifest['reused_phase2']!=reused:
        raise ValueError('Reused source provenance changed')
    return manifest


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--init',action='store_true');args=p.parse_args()
    if args.init:initialize()
    result=collect();print('ACQUIRED_OR_VERIFIED',len(result['acquired']),'REUSED',len(result['reused_phase2']))
