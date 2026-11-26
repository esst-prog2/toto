"""Independent raw census, source bindings, cache replay and byte reproduction."""
from collections import Counter
from pathlib import Path
from unittest.mock import patch
import csv,io,json,re,tempfile
from scripts import collect_belgian_pro_league_history as a
from scripts import inventory_belgian_pro_league_history as i


def verify(directory=a.PRIVATE):
    c=a.c;originals=c.verify_originals(directory)['files']+a.verify_originals(directory)['files'];saved=directory/'phase3'
    hi=json.loads((saved/'historical_inventory.json').read_text());mi=json.loads((saved/'modern_inventory.json').read_text());over=json.loads((saved/'overlap_inventory.json').read_text());events=json.loads((saved/'event_diagnostics.json').read_text());queue=json.loads((saved/'review_queue.json').read_text())
    rows={r['audit_id']:r for r in hi['observations']};census={}
    for rec in originals:
        raw=(directory/rec['path']).read_bytes()
        if rec['repository']==c.HIST:
            rr=list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))));actual=Counter(r['Season'] for r in rr)
            if len(rr)!=hi['observed'] or dict(actual)!={y:r['observed'] for y,r in hi['seasons'].items()}:raise ValueError('CSV census differs')
            for source,parsed in zip(rr,hi['observations']):
                if source!=parsed['original_fields']:raise ValueError('Original CSV fields differ')
            census['historical']=len(rr)
        elif rec['repository']==c.MODERN:
            report=mi[rec['original_path']];physical=[n for n,s in enumerate(raw.decode('utf-8-sig').splitlines(),1) if ' v ' in s]
            if physical!=[r['source_line'] for r in report['observations']]:raise ValueError('Independent TXT census differs')
            first=raw.decode('utf-8-sig').splitlines()[0];declared=re.search(r'(\d{4})/(\d{2})$',first)
            if int(report['declared_season'][:4])!=int(declared[1]):raise ValueError('Declared season differs')
            counts=Counter();stage=None
            for line in raw.decode('utf-8-sig').splitlines():
                t=line.strip()
                if t.startswith('▪ '):
                    stage='CHAMPIONSHIP' if 'Championship,' in t or 'Playoff I,' in t else 'EUROPE_QUALIFICATION' if 'ECL Playoff,' in t else 'EUROPE' if 'Europe,' in t else 'PLAYDOWNS' if 'Relegation,' in t else 'REGULAR_SEASON'
                if ' v ' in line:counts[stage]+=1
            if dict(counts)!=report['all_stages']['stage_counts']:raise ValueError('Independent stage census differs')
            rows.update({r['audit_id']:r for r in report['observations']});census[rec['original_path']]=len(physical)
    all_h=set();all_m=set()
    for path,o in over.items():
        mapping={x['modern']:x['historical'] for x in o.get('candidate_correspondences',[])}
        for pair in o.get('comparisons',[]):
            h,m=rows[pair['historical_id']],rows[pair['modern_id']]
            if h['audit_id'] in all_h or m['audit_id'] in all_m:raise ValueError('Representation linked more than once')
            all_h.add(h['audit_id']);all_m.add(m['audit_id'])
            if h['season']!=m['season'] or mapping[m['home']]!=h['home'] or mapping[m['away']]!=h['away']:raise ValueError('Season/participant binding differs')
            if pair['date_equal']!=(h['date']==m['date']) or pair['score_equal']!=(h['FT']==m['FT']):raise ValueError('Conflict accounting differs')
    if len(rows)-len(all_h)!=events['conditional_match_events'] or len(events['conditional_events'])!=events['conditional_match_events']:raise ValueError('Conditional event reconciliation differs')
    represented=[sid for event in events['conditional_events'] for sid in event['source_ids']]
    if len(represented)!=len(rows) or set(represented)!=set(rows):raise ValueError('Source representations lost/duplicated')
    if len({q['conditional_event_anchor'] for q in queue['items']})!=len(queue['items']):raise ValueError('Queue not deduplicated')
    repro={}
    with tempfile.TemporaryDirectory(prefix='belgium-phase3-regen-') as temp:
        temp=Path(temp);i.generate(directory,temp/'phase3');i.v.generate(directory,temp/'phase2')
        for name in (*i.NAMES,'reproducibility.json'):
            left=(saved/name).read_bytes();right=(temp/'phase3'/name).read_bytes()
            if left!=right:raise ValueError('Phase3 regeneration differs: '+name)
            repro['phase3/'+name]=c.sha(left)
        for name in (*i.v.NAMES,'reproducibility.json'):
            left=(directory/'phase2'/name).read_bytes();right=(temp/'phase2'/name).read_bytes()
            if left!=right:raise ValueError('Frozen Phase2 regeneration differs: '+name)
            repro['phase2/'+name]=c.sha(left)
    before={str(p.relative_to(directory)):c.sha(p.read_bytes()) for p in directory.rglob('*') if p.is_file()}
    with patch.object(a,'request',side_effect=AssertionError('Phase3 cache requested network')),patch.object(c,'request',side_effect=AssertionError('Phase2 cache requested network')):
        a.collect(directory);c.collect(directory)
    after={str(p.relative_to(directory)):c.sha(p.read_bytes()) for p in directory.rglob('*') if p.is_file()}
    if before!=after:raise ValueError('Cache changed private files')
    return dict(phase=3,originals=len(originals),independent_census=census,source_observations=len(rows),matched_pairs=len(all_h),conditional_match_events=events['conditional_match_events'],queue_events=queue['fixture_events'],regenerated_sha256=repro,byte_identical=True,cache_requests=0,cache_unchanged=True,protected=a.protect(directory))


if __name__=='__main__':print(json.dumps(verify(),indent=2))
