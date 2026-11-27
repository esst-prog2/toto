"""Execute only the owner-approved 41-file pinned UCL plan; offline by default.

References nine frozen Phase 1 samples in place. No UEFA/RSSSF/API acquisition,
redirects, retries, new seasons, source overwrites or model use.
"""
import argparse
import json
from pathlib import Path
import time

from scripts import collect_turkish_super_lig_sources as acquisition

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'data/private/europe/champions_league'
RESEARCH = BASE / 'phase1_research'
PHASE = BASE / 'phase2'
DOWNLOAD = PHASE / 'acquisition'
PLAN = RESEARCH / 'proposed_acquisition_plan.v2.json'
PINS = {'footballcsv/europe-champions-league': '66393c8dc5c86b459dc700a0ae3a0bd0abedb56e',
        'openfootball/champions-league': 'abfaeddc2ee3d14f99ecc163c9ddb46cb4d67cef'}
EXTRA_RECEIPT = {'sha256', 'bytes', 'retrieved_at_utc', 'status', 'final_url',
                 'response_headers', 'request_elapsed_seconds', 'original_filename', 'constraints'}


def load(path):
    return json.loads(path.read_bytes())


def approved_items():
    plan = load(PLAN)
    items = plan['items']
    if (len(items), sum(i['expected_bytes'] for i in items),
            sum(not i['already_sampled'] for i in items)) != (41, 701486, 32):
        raise ValueError('Approved acquisition bounds differ')
    seen = set()
    for item in items:
        publisher = item['publisher']; owner = publisher.split('/')[0]
        year = int(item['season'][:4]); short = f'{year}-{(year+1)%100:02d}'
        filename = item['url'].rsplit('/', 1)[1]
        if publisher not in PINS or item['commit'] != PINS[publisher]:
            raise ValueError('Unapproved publisher or pin')
        allowed = ((owner == 'footballcsv' and 1992 <= year <= 2015 and filename == 'champs.csv') or
                   (owner == 'openfootball' and 2011 <= year <= 2025 and filename == 'cl.txt') or
                   (owner == 'openfootball' and year in (2024, 2025) and filename == 'clq.txt'))
        url = f'https://raw.githubusercontent.com/{publisher}/{PINS[publisher]}/{short}/{filename}'
        path = (f'phase1_research/samples/{owner}/{short}/{filename}' if item['already_sampled'] else
                f'phase1/originals/{owner}/{short}/{filename}')
        if not allowed or item['url'] != url or item['path'] != path or url in seen:
            raise ValueError('Source exceeds exact approved scope')
        seen.add(url)
        notice = BASE / item['license_reference']
        if acquisition.sha(notice.read_bytes()) != item['license_sha256'] or not notice.read_text().startswith('CC0 1.0 Universal'):
            raise ValueError('Pinned permission evidence differs')
        tree = load(RESEARCH / 'metadata' / owner / 'tree.json')
        if tree.get('truncated') or tree['sha'] != PINS[publisher]:
            raise ValueError('Pinned tree differs')
        blob = next(x for x in tree['tree'] if x['path'] == f'{short}/{filename}')
        if (blob['sha'], blob['size']) != (item['expected_blob'], item['expected_bytes']):
            raise ValueError('Plan/blob binding differs')
    return items


def verify_original(item):
    path = BASE / item['path'] if item['already_sampled'] else DOWNLOAD / item['path'].removeprefix('phase1/')
    receipt = load(path.with_name(path.name + '.provenance.json'))
    original_item = {k: v for k, v in receipt.items() if k not in EXTRA_RECEIPT}
    directory = RESEARCH if item['already_sampled'] else DOWNLOAD
    raw = acquisition.verify(directory, original_item, receipt)
    if receipt['url'] != item['url'] or len(raw) != item['expected_bytes']:
        raise ValueError('Original/plan identity differs')
    acquisition.common.verify_blob(raw, {'sha': item['expected_blob'], 'size': item['expected_bytes']})
    return raw, receipt


def run(network=False):
    items = approved_items(); results = []
    # A new scoped execution area retains the earlier sandbox-DNS failure receipt.
    # Permission bytes are references/copies of existing originals, never new requests.
    for owner in ('footballcsv', 'openfootball'):
        old = RESEARCH / 'metadata' / owner / 'LICENSE.md'
        for source in (old, old.with_name(old.name + '.provenance.json')):
            dest = DOWNLOAD / 'permissions' / owner / source.name
            if dest.exists():
                if dest.read_bytes() != source.read_bytes():
                    raise ValueError('Permission copy changed')
            else:
                acquisition.save(dest, source.read_bytes())
    # Recent-season completeness first; no invented numerical time weights.
    for item in sorted(items, key=lambda x: (x['season'], x['url']), reverse=True):
        if not item['already_sampled']:
            entry = dict(url=item['url'], path=item['path'].removeprefix('phase1/'), max_bytes=item['max_bytes'],
                         publisher=item['publisher'], kind='fixture',
                         licensing='Pinned CC0 rights held only; third-party rights and training clearance unresolved; private inventory only',
                         permission_basis='Owner approved Phase 2 bounded 41-file plan, 2026-11-26',
                         permission_reference=f"permissions/{item['publisher'].split('/')[0]}/LICENSE.md", permission_sha256=item['license_sha256'],
                         encoding='utf-8', commit=item['commit'], expected_blob=item['expected_blob'],
                         expected_bytes=item['expected_bytes'])
            _, downloaded = acquisition.acquire(DOWNLOAD, entry, network=network)
            if downloaded:
                print('ACQUIRED', item['path'], flush=True)
                time.sleep(.4)
        raw, receipt = verify_original(item)
        physical = BASE / item['path'] if item['already_sampled'] else DOWNLOAD / item['path'].removeprefix('phase1/')
        results.append(dict(path=str(physical.relative_to(BASE)), approved_plan_path=item['path'], publisher=item['publisher'], season=item['season'],
                            scope=item['scope'], sha256=acquisition.sha(raw), bytes=len(raw),
                            git_blob=item['expected_blob'], url=item['url'],
                            reused_phase1_sample=item['already_sampled'],
                            receipt_sha256=acquisition.sha(physical.with_name(physical.name+'.provenance.json').read_bytes()),
                            retrieved_at_utc=receipt['retrieved_at_utc'],
                            permission_reference=item['license_reference'], permission_sha256=item['license_sha256']))
    result = dict(phase=2, approved_plan_sha256=acquisition.sha(PLAN.read_bytes()),
                  originals=sorted(results, key=lambda x: x['path']), files=41, bytes=701486,
                  reused_samples=9, newly_acquired=32, newly_acquired_bytes=562642,
                  rights='Private inventory; CC0 for rights held; upstream independence, third-party rights and model-training clearance unresolved',
                  excluded_sources=['UEFA platforms', 'Kassies access stop', 'unapproved RSSSF pages', 'licensed APIs', 'European Cup extension', '2026/27'])
    path = PHASE / 'acquisition_manifest.json'; raw = acquisition.encode(result)
    if path.exists():
        if path.read_bytes() != raw:
            raise ValueError('Frozen acquisition manifest differs')
    else:
        acquisition.save(path, raw)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--network', action='store_true')
    args = parser.parse_args()
    result = run(args.network)
    print('PASS', result['files'], 'originals', result['bytes'], 'bytes')
