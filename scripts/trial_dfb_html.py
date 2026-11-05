"""Offline single-snapshot DFB parser trial; no network or crawling capability."""
from dataclasses import asdict
import hashlib
import io
import json
from pathlib import Path


from scripts.artifact_io import check_overwrite, serialize_csv
from toto_estimator.data import load_historical_data
from toto_estimator.dfb_html import COLUMNS, parse_dfb_matchday

PRIVATE = Path(__file__).resolve().parents[1]/'data/private/germany'


def main():
    source=PRIVATE/'bundesliga_1990_1991_md1.html'
    outputs=[PRIVATE/'bundesliga_1990_1991_md1_parsed.csv', PRIVATE/'dfb_html_trial.json']
    check_overwrite(outputs)
    content=source.read_bytes()
    result=parse_dfb_matchday(content.decode('utf-8'),expected_season='1990/91',expected_matchday=1,expected_matches=9)
    if result.issues:
        raise ValueError(result.issues)
    csv_bytes=serialize_csv(result.records,COLUMNS)
    validated=load_historical_data(io.StringIO(csv_bytes.decode()))
    if len(validated)!=9 or len({r[k] for r in result.records for k in ('home_team','away_team')})!=18:
        raise ValueError('trial count/team coverage differs')
    if parse_dfb_matchday(content.decode()).records != result.records:
        raise ValueError('non-reproducible parsing')
    manifest=dict(checked_on='2026-11-05',source_url=result.source_url,
                  source_sha256=hashlib.sha256(content).hexdigest(),source_bytes=len(content),
                  obtained_by='One ordinary public GET of user-specified page for offline inspection; HTTP 200. No login, anti-bot bypass, assets, match-detail retrieval or crawling.',
                  result=asdict(result),existing_historical_validator='PASS, 9 records',
                  output_sha256=hashlib.sha256(csv_bytes).hexdigest(),
                  robots_status='HTTP 404 for https://datencenter.dfb.de/robots.txt; no usable directives; not a reuse grant.',
                  collection_permission='NOT ESTABLISHED: DFB general terms section 5 restrict unauthorized crawling/scraping; obtain written permission/licensed export before systematic collection.',
                  scope='Single current HTML layout only. No multi-season validation or independent result verification; no collection authorization inferred.')
    with outputs[0].open('xb') as handle:handle.write(csv_bytes)
    with outputs[1].open('x',encoding='utf-8') as handle:json.dump(manifest,handle,indent=2,ensure_ascii=False);handle.write('\n')
    print(f'PASS: {len(result.records)} results, 18 teams, zero row issues; source SHA-256 {manifest["source_sha256"]}')


if __name__=='__main__':main()
