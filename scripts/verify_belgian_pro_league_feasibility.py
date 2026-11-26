"""Offline independent Phase 2 reconciliation and temporary byte regeneration."""
from collections import Counter
import csv, io, json, tempfile
from pathlib import Path
from unittest.mock import patch
from scripts import collect_belgian_pro_league_feasibility as c
from scripts import validate_belgian_pro_league_feasibility as v


def verify(directory=c.PRIVATE):
    manifest=c.verify_originals(directory);saved=directory/'phase2'
    counts={};seen=set()
    for rec in manifest['files']:
        raw=(directory/rec['path']).read_bytes();seen.add(rec['path'])
        if rec['repository']==c.HIST:
            rows=list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))));counts['historical']=len(rows)
            observed=Counter(r['Season'] for r in rows)
            report=json.loads((saved/'historical_findings.json').read_text())
            if report['observed']!=len(rows) or {k:r['observed'] for k,r in report['seasons'].items()}!=dict(observed):raise ValueError('Independent CSV reconciliation differs')
            for y in observed:
                raw_rows=[r for r in rows if r['Season']==y]
                if sum(r['hgoal'].isdigit() and r['vgoal'].isdigit() for r in raw_rows)!=report['seasons'][y]['scored']:raise ValueError('Independent score tally differs')
        elif rec['repository']==c.MODERN:
            # Independent source-line census: every literal fixture delimiter must bind once.
            lines=raw.decode('utf-8-sig').splitlines();physical=[i for i,s in enumerate(lines,1) if ' v ' in s]
            year=rec['season'][:4];report=json.loads((saved/'modern_findings.json').read_text())[year]
            if physical!=[r['source_line'] for r in report['observations']]:raise ValueError('TXT fixture census differs')
            counts[rec['season']]=len(physical)
    if seen!={x['path'] for x in c.plan()}:raise ValueError('Bounded source population differs')
    with tempfile.TemporaryDirectory(prefix='belgium-phase2-reproduce-') as name:
        target=Path(name);v.generate(directory,target);comparisons={}
        for artifact in (*v.NAMES,'reproducibility.json'):
            a=(saved/artifact).read_bytes();b=(target/artifact).read_bytes()
            if a!=b or c.sha(a)!=c.sha(b):raise ValueError('Regeneration differs: '+artifact)
            comparisons[artifact]=dict(bytes=len(a),sha256=c.sha(a),byte_identical=True)
    # A complete cached replay must work with all requests forbidden.
    before={str(p.relative_to(directory)):c.sha(p.read_bytes()) for p in directory.rglob('*') if p.is_file()}
    with patch.object(c,'request',side_effect=AssertionError('Cache unexpectedly requested network')):
        c.collect(directory)
    after={str(p.relative_to(directory)):c.sha(p.read_bytes()) for p in directory.rglob('*') if p.is_file()}
    if before!=after:raise ValueError('Cache replay altered artifacts')
    protected=c.protect(directory)
    return dict(phase=2,source_count=len(seen),source_census=counts,regeneration=comparisons,cache_requests=0,cache_byte_unchanged=True,protected=protected,scope='FEASIBILITY_ONLY_NO_SCREENED_OUTPUT')


if __name__=='__main__':print(json.dumps(verify(),indent=2))
