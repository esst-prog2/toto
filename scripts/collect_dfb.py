"""DFB collection CLI. Offline by default; network mode requires written approval."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.artifact_io import serialize_csv
from toto_estimator.dfb_collection import (build_report, coverage_markdown, ingest_exports,
                                         inventory_from_html, load_reviews)
from toto_estimator.dfb_html import COLUMNS
from toto_estimator.historical_import import canonical_season
from toto_estimator.dfb_transport import (AccessStopped, AuthorizedFetcher, ResponseCache,
                                        digest, json_bytes, write_once)

PRIVATE = Path(__file__).resolve().parents[1]/'data/private/germany'


def private_path(value):
    path=Path(value).resolve()
    if not path.is_relative_to(PRIVATE.resolve()):
        raise ValueError('All inputs and outputs must remain under data/private/germany/')
    return path


def season_argument(value):
    """Accept explicit adjacent-year seasons using the existing canonicalizer."""
    try:
        season = canonical_season(value)
        if '/' not in season or not 1990 <= int(season[:4]) <= 2026:
            raise ValueError('choose a season from 1990/91 through 2026/27')
        return season
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed',required=True,help='Saved German full-page DFB HTML with season selector')
    parser.add_argument('--season',type=season_argument,help='One season, e.g. 1990/91 or 1990/1991; default: all target seasons')
    parser.add_argument('--exports',help='Local export/saved-sample manifest with checksums and provenance')
    parser.add_argument('--reviews',help='Response-bound final-status/awarded-outcome evidence')
    parser.add_argument('--cache',default=str(PRIVATE/'collection/cache'))
    parser.add_argument('--output',default=str(PRIVATE/'collection/runs'))
    parser.add_argument('--network',action='store_true',help='Explicit opt-in, also requires authorization evidence')
    parser.add_argument('--authorization',help='Private written-authorization evidence/configuration JSON')
    parser.add_argument('--include-ongoing',action='store_true',help='Network inventory includes separate 2026/27 partition')
    args=parser.parse_args()
    if args.network and args.season == '2026/2027' and not args.include_ongoing:
        parser.error('--season 2026/27 network collection also requires --include-ongoing')
    seed=private_path(args.seed);cache=ResponseCache(private_path(args.cache))
    output=private_path(args.output)
    inventory=inventory_from_html(seed.read_bytes().decode('utf-8'))
    if args.season:
        inventory = {**inventory, 'seasons': [s for s in inventory['seasons'] if s['season'] == args.season]}
    exports=private_path(args.exports) if args.exports else None
    reviews_path=private_path(args.reviews) if args.reviews else None
    if args.authorization and not args.network:
        raise ValueError('Authorization config does not imply network opt-in')
    export_import = None
    if exports:
        allowed_urls = {url for s in inventory['seasons'] for url in s['urls'] if url} if args.season else None
        export_import = ingest_exports(cache, exports, allowed_urls=allowed_urls)
    reviews=load_reviews(reviews_path)
    stopped=None
    if args.network:
        approval=json.loads(private_path(args.authorization).read_text()) if args.authorization else None
        if approval:
            approval['evidence_path']=str(private_path(approval['evidence_path']))
        fetcher=AuthorizedFetcher(cache,approval)
        try:
            for fmt in inventory['seasons']:
                if fmt['ongoing'] and not args.include_ongoing:continue
                if fmt['slug'] is None:
                    raise AccessStopped(f"Season not advertised: {fmt['season']}")
                for url in fmt['urls']:
                    fetcher.fetch(url)
        except (AccessStopped,ValueError,OSError) as exc:
            stopped=str(exc)
            cache.event(action='run_stopped',reason=stopped)
    report=build_report(inventory,cache,reviews)
    report['network_stop']=stopped
    report['selected_season']=args.season
    report['export_import']=export_import
    report['network_opt_in']=args.network
    report['code_sha256']={name:digest((Path(__file__).resolve().parents[1]/name).read_bytes()) for name in (
        'src/toto_estimator/dfb_html.py','src/toto_estimator/dfb_collection.py','src/toto_estimator/dfb_transport.py','scripts/collect_dfb.py')}
    report['input_manifest_sha256']=digest(exports.read_bytes()) if exports else None
    report['status_reviews_sha256']=digest(reviews_path.read_bytes()) if reviews_path else None
    run=output/digest(json_bytes(report))
    records={partition:[] for partition in ('completed_history','ongoing')}
    for season in report['seasons']:records[season['partition']].extend(season['records'])
    candidates = {partition: [] for partition in records}
    matchdays = []
    for fmt, season in zip(inventory['seasons'], report['seasons']):
        observations = sorted(season['accepted_matches'] + season['uncertain_matches'],
                              key=lambda r: (r['matchday'], r['row']))
        candidates[season['partition']].extend(r['record'] for r in observations if r['record'])
        for day, url in enumerate(fmt['urls'], 1):
            page = cache.get(url) if url else None
            status = 'INVALID_CACHED' if url in season['invalid_pages'] else 'CACHED' if page else 'MISSING'
            matchdays.append(dict(season=fmt['season'], matchday=day, url=url or '',
                                  cache_status=status, sha256=page[0]['sha256'] if page else ''))
    artifacts={'validation.json':json_bytes(report),'coverage.md':coverage_markdown(report).encode(),
               'inventory.json':json_bytes(inventory),
               'completed_history.csv':serialize_csv(records['completed_history'],COLUMNS),
               'ongoing.csv':serialize_csv(records['ongoing'],COLUMNS),
               'completed_history_candidates.csv':serialize_csv(candidates['completed_history'],COLUMNS),
               'ongoing_candidates.csv':serialize_csv(candidates['ongoing'],COLUMNS),
               'matchday_inventory.csv':serialize_csv(matchdays,('season','matchday','url','cache_status','sha256'))}
    for name,content in artifacts.items():write_once(run/name,content)
    write_once(run/'checksums.json',json_bytes({name:digest(content) for name,content in artifacts.items()}))
    print(json.dumps(dict(report=str(run/'validation.json'),**report['summary'])))
    if stopped:raise SystemExit(f'NETWORK STOPPED: {stopped}. Partial coverage saved; no archive continuation.')


if __name__=='__main__':main()
