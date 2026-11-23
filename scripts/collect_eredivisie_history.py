"""Phase 3: acquire exactly three pinned modern originals, reuse frozen Phase 2."""
import argparse,json,subprocess,time
from scripts import collect_eredivisie_feasibility as c
ROOT,PRIVATE,PIN,REPO=c.ROOT,c.PRIVATE,c.PINS[c.MODERN],c.MODERN
YEARS=(2020,2021,2022)
BASELINE='phase3_protected_before.json'
MANIFEST='phase3_acquisition.json'


def plan():
    return [dict(repository=REPO,commit=PIN,original_path=f'netherlands/{y}-{(y+1)%100:02}_nl1.txt',path=f'{REPO}/netherlands/{y}-{(y+1)%100:02}_nl1.txt',url=f'https://raw.githubusercontent.com/{REPO}/{PIN}/netherlands/{y}-{(y+1)%100:02}_nl1.txt',season=f'{y}/{y+1}') for y in YEARS]


def initialize(directory=PRIVATE,root=ROOT):
    if (directory/BASELINE).exists():return protect(directory,root)
    if subprocess.check_output(['git','branch','--show-current'],cwd=root).decode().strip()!='feature/data-collection' or subprocess.check_output(['git','rev-parse','HEAD'],cwd=root).decode().strip()!='4f8c64433cf6168a06dbde0102e822ce6d2eeffa':raise ValueError('Unexpected branch/HEAD')
    c.protect(directory,root);c.verify_originals(directory);r=json.loads((directory/'phase2_final_verification.json').read_text())
    for n,item in r['private_files_before_this_receipt'].items():
        if c.sha((directory/n).read_bytes())!=item['sha256']:raise ValueError('Phase 2 private evidence changed: '+n)
    for n,h in r['public_files'].items():
        if c.sha((root/n).read_bytes())!=h:raise ValueError('Phase 2 public evidence changed: '+n)
    files={str(p.relative_to(root)):c.sha(p.read_bytes()) for p in directory.rglob('*') if p.is_file()};files.update({n:h for n,h in r['public_files'].items() if n!='PLANNING_LOG.md'})
    log=(root/'PLANNING_LOG.md').read_bytes();index=subprocess.check_output(['git','rev-parse','--git-path','index'],cwd=root).decode().strip()
    c.save(directory/BASELINE,c.encode(dict(files=files,planning_log=dict(bytes=len(log),sha256=c.sha(log)),head=r['head'],index_sha256=c.sha((root/index).read_bytes()))))
    return protect(directory,root)


def protect(directory=PRIVATE,root=ROOT):
    previous=c.protect(directory,root);frozen=json.loads((directory/BASELINE).read_text())
    if not frozen['files']:raise ValueError('Empty Phase 2 baseline')
    for n,h in frozen['files'].items():
        if not (root/n).resolve().is_relative_to(root.resolve()) or c.sha((root/n).read_bytes())!=h:raise ValueError('Frozen Phase 2 entry changed: '+n)
    prefix=frozen['planning_log'];log=(root/'PLANNING_LOG.md').read_bytes()
    if len(log)<prefix['bytes'] or c.sha(log[:prefix['bytes']])!=prefix['sha256']:raise ValueError('Planning history changed')
    return dict(previous=previous,phase2_protected_entries=len(frozen['files']))


def entries(directory=PRIVATE):
    c.verify_originals(directory)
    return c.base.tree_entries((directory/'metadata'/REPO/'git_tree.json').read_bytes(),PIN,[x['original_path'] for x in plan()])


def collect(directory=PRIVATE,root=ROOT):
    protected=protect(directory,root);tree=entries(directory);receipts=[]
    for item in plan():
        dest=directory/item['path'];receipt=dest.with_name(dest.name+'.provenance.json')
        if dest.exists()!=receipt.exists():raise ValueError('Partial original/receipt pair')
        if dest.exists():
            r=json.loads(receipt.read_text());c.verify_record(directory,item,r,tree)
        else:
            raw=c.request(item['url'],directory/'phase3_access');blob=c.base.verify_blob(raw,tree[item['original_path']])
            r=dict(item,kind='dataset',bytes=len(raw),sha256=c.sha(raw),git_blob_sha1=blob,original_filename=dest.name,format=dest.suffix,retrieved_at_utc=c.now(),licensing=c.RIGHTS[REPO],attribution='OpenFootball contributors',retrieval='One bounded request, no retries or redirects; fixed approved revision and blob verified',competition='Eredivisie, inventory not historical certification',uncertainty='Source-date, administrative and result-availability semantics unverified; no downstream rights clearance')
            c.save(dest,raw);c.save(receipt,c.encode(r));time.sleep(2)
        receipts.append(r)
    result=dict(phase=3,scope='Exactly three additional modern originals; all six Phase 2 originals unchanged',files=receipts,reused_phase2_originals=6,rights=c.RIGHTS,protected=protected)
    dest=directory/MANIFEST;raw=c.encode(result)
    if dest.exists():
        if dest.read_bytes()!=raw:raise ValueError('Acquisition manifest changed')
    else:c.save(dest,raw)
    verify_originals(directory);protect(directory,root);return result


def verify_originals(directory=PRIVATE):
    tree=entries(directory);r=json.loads((directory/MANIFEST).read_text());items=plan()
    if len(r['files'])!=3 or {x['path'] for x in r['files']}!={x['path'] for x in items} or r['rights']!=c.RIGHTS:raise ValueError('Acquisition scope changed')
    for item in items:
        rec=next(x for x in r['files'] if x['path']==item['path']);c.verify_record(directory,item,rec,tree);dest=directory/item['path']
        if json.loads(dest.with_name(dest.name+'.provenance.json').read_text())!=rec:raise ValueError('Receipt/manifest mismatch')
    return r


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--init-only',action='store_true');args=parser.parse_args()
    if args.init_only:print(initialize());print([(x['original_path'],entries()[x['original_path']]['sha']) for x in plan()])
    else:print('VERIFIED_OR_ACQUIRED',len(collect()['files']))
