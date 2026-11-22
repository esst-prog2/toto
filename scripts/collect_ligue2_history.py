"""Ligue 2 Phase 3: exactly six approved pinned originals; no overwrite/retry."""
import argparse
import json
import subprocess
import time
from scripts import collect_ligue2_feasibility as base

ROOT, PRIVATE, PIN, REPO = base.ROOT, base.PRIVATE, base.PIN, base.REPO
YEARS = (2015, 2016, 2018, 2020, 2021, 2023)
REUSED = (2014, 2017, 2019, 2022, 2024)
BASELINE = 'phase3_protected_before.json'
MANIFEST = 'phase3_acquisition.json'


def plan():
    return [dict(repository=REPO,commit=PIN,original_path=f'france/{y}-{(y+1)%100:02}_fr2.txt',
                 path=f'{REPO}/france/{y}-{(y+1)%100:02}_fr2.txt',
                 url=f'https://raw.githubusercontent.com/{REPO}/{PIN}/france/{y}-{(y+1)%100:02}_fr2.txt',season=f'{y}/{y+1}') for y in YEARS]


def initialize(directory=PRIVATE,root=ROOT):
    if (directory/BASELINE).exists():return protect(directory,root)
    if subprocess.check_output(['git','branch','--show-current'],cwd=root).decode().strip()!='feature/data-collection':raise ValueError('Wrong branch')
    if subprocess.check_output(['git','rev-parse','HEAD'],cwd=root).decode().strip()!='07efff5f014bdd2e7e423f2fee76333346135790':raise ValueError('Unexpected HEAD')
    base.protect(directory,root);base.verify_originals(directory)
    final=json.loads((directory/'phase2_final_verification.json').read_text())
    for name,item in final['private_files_before_this_receipt'].items():
        if base.sha((directory/name).read_bytes())!=item['sha256']:raise ValueError('Phase 2 evidence changed: '+name)
    for name,digest in final['public_files'].items():
        if base.sha((root/name).read_bytes())!=digest:raise ValueError('Approved public work changed: '+name)
    files={str(p.relative_to(root)):base.sha(p.read_bytes()) for p in directory.rglob('*') if p.is_file()}
    files.update({n:d for n,d in final['public_files'].items() if n!='PLANNING_LOG.md'})
    log=(root/'PLANNING_LOG.md').read_bytes()
    index=subprocess.check_output(['git','rev-parse','--git-path','index'],cwd=root).decode().strip()
    base.save(directory/BASELINE,base.encode(dict(files=files,planning_log=dict(bytes=len(log),sha256=base.sha(log)),
        head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root).decode().strip(),index_sha256=base.sha((root/index).read_bytes()))))
    return protect(directory,root)


def protect(directory=PRIVATE,root=ROOT):
    previous=base.protect(directory,root);frozen=json.loads((directory/BASELINE).read_text())
    if not frozen['files']:raise ValueError('Empty frozen baseline')
    for name,digest in frozen['files'].items():
        p=root/name
        if not p.resolve().is_relative_to(root.resolve()) or base.sha(p.read_bytes())!=digest:raise ValueError('Frozen Phase 2 file changed: '+name)
    prefix=frozen['planning_log'];log=(root/'PLANNING_LOG.md').read_bytes()
    if len(log)<prefix['bytes'] or base.sha(log[:prefix['bytes']])!=prefix['sha256']:raise ValueError('Planning history changed')
    return dict(previous=previous,phase2_protected_entries=len(frozen['files']))


def entries(directory=PRIVATE):
    base.verify_originals(directory)
    return base.base.tree_entries((directory/'metadata/git_tree.json').read_bytes(),PIN,[x['original_path'] for x in plan()])


def collect(directory=PRIVATE,root=ROOT):
    protection=protect(directory,root);tree=entries(directory);receipts=[]
    for item in plan():
        target=directory/item['path'];receipt=target.with_name(target.name+'.provenance.json')
        if target.exists()!=receipt.exists():raise ValueError('Incomplete original/receipt pair')
        if target.exists():
            r=json.loads(receipt.read_text());base.verify_record(directory,item,r,tree)
        else:
            raw=base.request(item['url'],directory);blob=base.base.verify_blob(raw,tree[item['original_path']])
            r=dict(item,kind='dataset',competition='Ligue 2',bytes=len(raw),sha256=base.sha(raw),git_blob_sha1=blob,
                   original_filename=target.name,retrieved_at_utc=base.now(),format='.txt',attribution='OpenFootball contributors',
                   licensing=base.RIGHTS[REPO],source_notices='Unchanged pinned Phase 2 README, LICENSE, france/README and NOTES; original receipts retained',
                   uncertainty='Source assertions only; actual completion, administrative finality and result availability not certified')
            base.save(target,raw);base.save(receipt,base.encode(r));time.sleep(2)
        receipts.append(r)
    result=dict(phase=3,files=receipts,reused_seasons=[f'{y}/{y+1}' for y in REUSED],
                excluded_from_completed_window='2025/2026; original Phase 2 snapshot remains separate',protected=protection)
    content=base.encode(result);target=directory/MANIFEST
    if target.exists():
        if target.read_bytes()!=content:raise ValueError('Phase 3 manifest changed')
    else:base.save(target,content)
    verify_originals(directory);protect(directory,root);return result


def verify_originals(directory=PRIVATE):
    base.verify_originals(directory);tree=entries(directory);m=json.loads((directory/MANIFEST).read_text());expected=plan()
    if (m.get('phase')!=3 or m.get('reused_seasons')!=[f'{y}/{y+1}' for y in REUSED] or
        len(m['files'])!=6 or {r['path'] for r in m['files']}!={r['path'] for r in expected}):raise ValueError('Phase 3 source scope changed')
    for item in expected:
        r=next(r for r in m['files'] if r['path']==item['path']);base.verify_record(directory,item,r,tree)
        target=directory/item['path']
        if json.loads(target.with_name(target.name+'.provenance.json').read_text())!=r:raise ValueError('Receipt/manifest differs')
    return m


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--init',action='store_true');parser.add_argument('--init-only',action='store_true');args=parser.parse_args()
    if args.init or args.init_only:initialize()
    if not args.init_only:print('VERIFIED_OR_ACQUIRED',len(collect()['files']))
