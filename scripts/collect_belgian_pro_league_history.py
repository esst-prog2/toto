"""Phase 3 only: two additional pinned originals; Phase 2 remains frozen."""
import argparse,json,subprocess,time
from urllib.request import Request,build_opener
from scripts import collect_belgian_pro_league_feasibility as c
ROOT,PRIVATE=c.ROOT,c.PRIVATE
YEARS=(2021,2024)
EXPECTED=(('2e554912605069d2979b413ae696bf2aced1e4d1',27360),('a883cd17078b92e876a11e150538c39122769b51',26302))


def plan():
    return [dict(repository=c.MODERN,commit=c.PINS[c.MODERN],original_path=f'{y}-{(y+1)%100:02}/be1.txt',path=f'{c.MODERN}/{y}-{(y+1)%100:02}/be1.txt',season=f'{y}/{y+1}',expected_blob=blob,expected_bytes=size,url=f'https://raw.githubusercontent.com/{c.MODERN}/{c.PINS[c.MODERN]}/{y}-{(y+1)%100:02}/be1.txt') for y,(blob,size) in zip(YEARS,EXPECTED)]


def initialize(directory=PRIVATE,root=ROOT):
    if (directory/'phase3_protected_before.json').exists():return protect(directory,root)
    c.protect(directory,root)
    if subprocess.check_output(['git','branch','--show-current'],cwd=root).decode().strip()!='feature/data-collection':raise ValueError('Wrong branch')
    receipt=json.loads((directory/'phase2_final_verification.json').read_text())
    for n,h in receipt['public_files'].items():
        if c.sha((root/n).read_bytes())!=h:raise ValueError('Phase2 public work changed: '+n)
    files={str(p.relative_to(root)):c.sha(p.read_bytes()) for p in directory.rglob('*') if p.is_file()}
    files.update({n:h for n,h in receipt['public_files'].items() if n!='PLANNING_LOG.md'})
    log=(root/'PLANNING_LOG.md').read_bytes()
    c.save(directory/'phase3_protected_before.json',c.encode(dict(files=files,planning_log=dict(bytes=len(log),sha256=c.sha(log)),approval='PHASE3_TWO_MODERN_ORIGINALS_ONLY')))
    return protect(directory,root)


def protect(directory=PRIVATE,root=ROOT):
    previous=c.protect(directory,root);saved=json.loads((directory/'phase3_protected_before.json').read_text())
    if not saved['files'] or saved['approval']!='PHASE3_TWO_MODERN_ORIGINALS_ONLY':raise ValueError('Invalid Phase3 baseline')
    for n,h in saved['files'].items():
        p=root/n
        if not p.resolve().is_relative_to(root.resolve()) or c.sha(p.read_bytes())!=h:raise ValueError('Frozen Phase2 entry changed: '+n)
    log=(root/'PLANNING_LOG.md').read_bytes();prefix=saved['planning_log']
    if len(log)<prefix['bytes'] or c.sha(log[:prefix['bytes']])!=prefix['sha256']:raise ValueError('Planning prefix changed')
    return dict(previous=previous,phase2_frozen_entries=len(saved['files']))


def entries(directory=PRIVATE):
    c.verify_originals(directory)
    return {x['original_path']:dict(sha=x['expected_blob'],size=x['expected_bytes']) for x in plan()}


def request(item,directory):
    if item not in plan():raise ValueError('Unapproved acquisition')
    stop=directory/'phase3_access'/'ACCESS_STOP.json'
    if stop.exists():raise RuntimeError('Prior access failure; no automatic retry')
    try:
        with build_opener(c.base.NoRedirect).open(Request(item['url'],headers={'User-Agent':'ThePickSheet-Belgium-bounded-phase3'}),timeout=30) as response:
            if response.status!=200 or response.url!=item['url'] or response.headers.get('Retry-After'):raise ValueError('Restricted/redirected response')
            raw=response.read(8000001)
            if len(raw)>8000000:raise ValueError('Response exceeds bound')
            return raw,dict(final_url=response.url,status=response.status,headers=dict(response.headers.items()))
    except Exception as exc:
        c.save(stop,c.encode(dict(url=item['url'],error=str(exc),retrieved_at_utc=c.now())));raise


def collect(directory=PRIVATE,root=ROOT):
    protected=protect(directory,root);tree=entries(directory);receipts=[]
    for item in plan():
        dest=directory/item['path'];receipt=dest.with_name(dest.name+'.provenance.json')
        if dest.exists()!=receipt.exists():raise ValueError('Partial original/receipt pair')
        if dest.exists():r=json.loads(receipt.read_text());c.verify_record(directory,item,r)
        else:
            raw,response=request(item,directory);c.base.verify_blob(raw,tree[item['original_path']]);raw.decode('utf-8-sig')
            r=dict(item,bytes=len(raw),sha256=c.sha(raw),git_blob_sha1=item['expected_blob'],retrieved_at_utc=c.now(),original_filename=dest.name,format=dest.suffix,encoding='utf-8-sig',response=response,publisher='OpenFootball contributors',attribution='OpenFootball contributors',licensing=c.RIGHTS[c.MODERN],upstream_provenance='Not independently established; retained CC0 notices apply to rights held',constraints='One bounded request; no retries, redirects, revision substitution or access bypass; private inventory only')
            c.save(dest,raw);c.save(receipt,c.encode(r));time.sleep(2)
        receipts.append(r)
    result=dict(phase=3,files=receipts,reused_phase2_originals=7,protected=protected,rights=c.RIGHTS,scope='Exactly two additional Belgium top-flight originals; no policy or standardization')
    c.keep(directory/'phase3_acquisition.json',c.encode(result));verify_originals(directory);protect(directory,root);return result


def verify_originals(directory=PRIVATE):
    entries(directory);r=json.loads((directory/'phase3_acquisition.json').read_text());items={x['path']:x for x in plan()}
    if len(r['files'])!=2 or {x['path'] for x in r['files']}!=set(items):raise ValueError('Wrong Phase3 scope')
    for rec in r['files']:
        c.verify_record(directory,items[rec['path']],rec);dest=directory/rec['path']
        if json.loads(dest.with_name(dest.name+'.provenance.json').read_text())!=rec:raise ValueError('Receipt binding changed')
    return r


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--init',action='store_true');a=p.parse_args()
    print(initialize() if a.init else {'acquired_or_reused':len(collect()['files'])})
