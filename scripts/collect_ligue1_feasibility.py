"""Ligue 1 Phase 2 only: seven approved immutable originals, bounded requests.

No retries, redirects, other seasons, overwrite, standardization or model use.
Run --init before acquisition. Cached originals are verified, never downloaded again.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import time
from urllib.request import Request, HTTPRedirectHandler, build_opener

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = ROOT / 'data/private/france/ligue_1'
SOURCES = (
    ('jalapic/engsoccerdata', '872c5c354161ace8408f3091b758c6af4cccca94',
     ('README.md', 'DESCRIPTION', 'man/france.Rd'), ('data-raw/france.csv',)),
    ('openfootball/europe', '63df627f3c87ce71708f016522ea236cf74332c3',
     ('README.md', 'LICENSE.md', 'france/README.md', 'france/NOTES.md'),
     tuple('france/'+n for n in ('2014-15_fr1.txt', '2016-17_fr1.txt', '2019-20_fr1.txt',
                                '2023-24_fr1.txt', '2025-26_fr1.txt', '2025-26_fr1-full.txt'))),
)
RIGHTS = {
    'jalapic/engsoccerdata': 'README noncommercial use; package GPL >=2. Dataset/upstream rights and model-training permission unresolved. Private academic feasibility only.',
    'openfootball/europe': 'CC0-1.0 for rights held; third-party rights and source lineage not warranted. Model-training clearance unresolved.',
}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encode(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False)+'\n').encode()


def save(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(raw)


def now():
    return datetime.now(timezone.utc).isoformat()


def initialize(directory=PRIVATE, root=ROOT):
    if (directory/'protected_before.json').exists():
        return protect(directory, root)
    if directory.exists() and any(directory.iterdir()):
        raise ValueError('Partial initialization; inspect manually')
    if not directory.resolve().is_relative_to((root/'data/private').resolve()):
        raise ValueError('Working area must be private')
    check = subprocess.run(['git', 'check-ignore', '--quiet', str(directory/'probe')], cwd=root)
    if check.returncode:
        raise ValueError('Working area is not Git-ignored')
    files = {str(p.relative_to(root)): sha(p.read_bytes()) for p in (root/'data/private').rglob('*')
             if p.is_file() and not p.is_relative_to(directory)}
    tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=root).decode().split('\0')
    public = {n: sha((root/n).read_bytes()) for n in tracked
              if n and n != 'PLANNING_LOG.md' and (root/n).is_file()}
    if not files or not public:
        raise ValueError('Empty protected scope')
    log = (root/'PLANNING_LOG.md').read_bytes()
    save(directory/'protected_before.json', encode(dict(private=files, public=public,
         planning_log=dict(bytes=len(log), sha256=sha(log)),
         git_head=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root).decode().strip())))
    return protect(directory, root)


def protect(directory=PRIVATE, root=ROOT):
    baseline = json.loads((directory/'protected_before.json').read_text())
    for group in ('private', 'public'):
        if not baseline[group]:
            raise ValueError('Empty protection group')
        for name, digest in baseline[group].items():
            path = root/name
            if not path.resolve().is_relative_to(root.resolve()) or sha(path.read_bytes()) != digest:
                raise ValueError('Protected file changed: '+name)
    prefix = baseline['planning_log']; log = (root/'PLANNING_LOG.md').read_bytes()
    if len(log) < prefix['bytes'] or sha(log[:prefix['bytes']]) != prefix['sha256']:
        raise ValueError('Planning history changed')
    return {k: len(baseline[k]) for k in ('private', 'public')}


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError('Unexpected redirect: stop for review')


def request(url, directory):
    if (directory/'ACCESS_STOP.json').exists():
        raise RuntimeError('Prior access failure; no automatic retry')
    try:
        with build_opener(NoRedirect).open(Request(url, headers={'User-Agent': 'ThePickSheet-Ligue1-bounded-feasibility'}), timeout=30) as response:
            if response.status != 200 or response.headers.get('Retry-After') or response.url != url:
                raise ValueError('Unexpected access response')
            raw = response.read(8_000_001)
            if len(raw) > 8_000_000:
                raise ValueError('Bounded response exceeded')
            return raw
    except Exception as exc:
        save(directory/'ACCESS_STOP.json', encode(dict(url=url, error=str(exc), timestamp_utc=now())))
        raise


def tree_entries(raw, commit, paths):
    tree = json.loads(raw)
    if tree.get('truncated') or tree.get('sha') != commit:
        raise ValueError('Wrong or truncated Git tree')
    entries = {e['path']: e for e in tree['tree'] if e['type'] == 'blob'}
    if not set(paths) <= entries.keys():
        raise ValueError('Approved path missing from pinned Git tree')
    return entries


def verify_blob(raw, entry):
    blob = hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    if blob != entry['sha'] or len(raw) != entry['size']:
        raise ValueError('Pinned Git blob or size mismatch')
    return blob


def collect(directory=PRIVATE, root=ROOT):
    protection = protect(directory, root); receipts = []; trees = {}
    # Validate BOTH complete approved path sets before requesting any original.
    for repo, commit, notices, datasets in SOURCES:
        target = directory/'metadata'/repo/'git_tree.json'
        url = f'https://api.github.com/repos/{repo}/git/trees/{commit}?recursive=1'
        if not target.exists():
            raw = request(url, directory)
            tree_entries(raw, commit, notices+datasets)
            save(target, raw)
            save(target.with_suffix('.receipt.json'), encode(dict(url=url, commit=commit, sha256=sha(raw), retrieved_at_utc=now())))
            time.sleep(2)
        raw = target.read_bytes(); receipt = json.loads(target.with_suffix('.receipt.json').read_text())
        if receipt['sha256'] != sha(raw) or receipt['commit'] != commit or receipt['url'] != url:
            raise ValueError('Git tree receipt changed')
        trees[repo] = tree_entries(raw, commit, notices+datasets)
    for kind in ('metadata', 'dataset'):
        for repo, commit, notices, datasets in SOURCES:
            for path in notices if kind == 'metadata' else datasets:
                dest = directory/repo/path; rec = dest.with_name(dest.name+'.provenance.json')
                url = f'https://raw.githubusercontent.com/{repo}/{commit}/{path}'
                if dest.exists() != rec.exists():
                    raise ValueError('Incomplete original/receipt pair')
                if dest.exists():
                    raw = dest.read_bytes(); item = json.loads(rec.read_text())
                    blob = verify_blob(raw, trees[repo][path])
                    wanted = dict(repository=repo, commit=commit, original_path=path, url=url,
                                  path=str(dest.relative_to(directory)), kind=kind, bytes=len(raw),
                                  sha256=sha(raw), git_blob_sha1=blob, licensing=RIGHTS[repo])
                    if any(item.get(k) != v for k, v in wanted.items()):
                        raise ValueError('Cached original receipt mismatch')
                else:
                    raw = request(url, directory); blob = verify_blob(raw, trees[repo][path])
                    item = dict(repository=repo, commit=commit, original_path=path, original_filename=Path(path).name,
                                path=str(dest.relative_to(directory)), url=url, kind=kind, format=Path(path).suffix,
                                competition='French top division / Ligue 1', bytes=len(raw), sha256=sha(raw),
                                git_blob_sha1=blob, retrieved_at_utc=now(), licensing=RIGHTS[repo],
                                attribution='James Curley' if repo.startswith('jalapic/') else 'OpenFootball contributors')
                    save(dest, raw); save(rec, encode(item)); time.sleep(2)
                receipts.append(item)
        if kind == 'metadata':
            if 'non-commer' not in (directory/'jalapic/engsoccerdata/README.md').read_text().lower():
                raise ValueError('Historical use notice changed; review before acquisition')
            if 'GPL' not in (directory/'jalapic/engsoccerdata/DESCRIPTION').read_text():
                raise ValueError('Package licence changed')
            if not (directory/'openfootball/europe/LICENSE.md').read_text().startswith('CC0 1.0 Universal'):
                raise ValueError('OpenFootball licence changed')
    manifest = dict(scope='Ligue 1 Phase 2 only: exactly seven originals', files=receipts, rights=RIGHTS,
                    protected=protection, independent_lineage='Not established; agreement is not independent certification')
    content = encode(manifest); target = directory/'acquisition.json'
    if target.exists():
        if target.read_bytes() != content:
            raise ValueError('Manifest changed')
    else:
        save(target, content)
    protect(directory, root)
    return manifest


def verify_originals(directory=PRIVATE):
    manifest = json.loads((directory/'acquisition.json').read_text())
    expected = {(repo, path): (commit, kind) for repo, commit, notices, datasets in SOURCES
                for kind, paths in (('metadata', notices), ('dataset', datasets)) for path in paths}
    if manifest['rights'] != RIGHTS or len(manifest['files']) != len(expected) or {(r['repository'], r['original_path']) for r in manifest['files']} != set(expected):
        raise ValueError('Acquisition scope changed')
    for repo, commit, notices, datasets in SOURCES:
        tree = directory/'metadata'/repo/'git_tree.json'; raw = tree.read_bytes()
        receipt = json.loads(tree.with_suffix('.receipt.json').read_text())
        if receipt['sha256'] != sha(raw) or receipt['commit'] != commit:
            raise ValueError('Tree receipt changed')
        entries = tree_entries(raw, commit, notices+datasets)
        for r in (r for r in manifest['files'] if r['repository'] == repo):
            path = directory/repo/r['original_path']; original = path.read_bytes()
            if (r['path'] != str(path.relative_to(directory)) or r['commit'] != commit or
                    r['url'] != f'https://raw.githubusercontent.com/{repo}/{commit}/{r["original_path"]}' or
                    r['licensing'] != RIGHTS[repo] or
                    r['kind'] != expected[repo, r['original_path']][1] or
                    r['sha256'] != sha(original) or r['bytes'] != len(original) or
                    r['git_blob_sha1'] != verify_blob(original, entries[r['original_path']]) or
                    json.loads(path.with_name(path.name+'.provenance.json').read_text()) != r):
                raise ValueError('Original/receipt mismatch')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--init', action='store_true'); args = parser.parse_args()
    if args.init:
        initialize()
    result = collect()
    print('VERIFIED_OR_ACQUIRED', sum(r['kind'] == 'dataset' for r in result['files']), 'PROTECTED', result['protected'])
