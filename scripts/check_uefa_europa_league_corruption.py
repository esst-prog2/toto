"""Exercise the independent Phase 4 validator on disposable in-memory copies."""
from __future__ import annotations
import argparse
from copy import deepcopy
import csv
import io
import json
from pathlib import Path
from scripts import verify_uefa_europa_league_standardization as v

def run(folder=v.PHASE/'validated'):
    folder=Path(folder);original_read=v.read;cache={};results=[]
    def baseline(path):
        k=str(Path(path))
        if k not in cache:cache[k]=original_read(path)
        return cache[k]
    def mutation(name,target,alter,kind='json'):
        raw=baseline(folder/target)
        obj=json.loads(raw)if kind=='json'else list(csv.reader(io.StringIO(raw.decode())))
        alter(obj)
        if kind=='json':changed=v.wire(obj)
        else:
            buffer=io.StringIO(newline='');csv.writer(buffer,lineterminator='\n').writerows(obj);changed=buffer.getvalue().encode()
        v.read=lambda p:changed if Path(p)==folder/target else baseline(p)
        try:
            v.verify(folder)
        except (ValueError,KeyError,IndexError)as error:
            results.append(dict(test=name,status='DETECTED',reason=str(error)))
        else:raise AssertionError('Corruption not detected: '+name)
        finally:v.read=baseline
    try:
        mutation('missing standardized match',v.NAME,lambda x:x.pop(),'csv')
        mutation('duplicate standardized match',v.NAME,lambda x:x.append(x[1].copy()),'csv')
        mutation('duplicate match identifier',v.NAME,lambda x:x[2].__setitem__(0,x[1][0]),'csv')
        mutation('invalid identifier format',v.NAME,lambda x:x[1].__setitem__(0,'invalid'),'csv')
        mutation('incorrect team mapping',v.NAME,lambda x:x[1].__setitem__(5,'Synthetic Wrong Club'),'csv')
        def reverse(x):
            x[1][5],x[1][6]=x[1][6],x[1][5];x[1][7],x[1][8]=x[1][8],x[1][7]
        mutation('reversed nominal orientation',v.NAME,reverse,'csv')
        mutation('changed regulation score',v.NAME,lambda x:x[1].__setitem__(7,str(int(x[1][7])+1)),'csv')
        links=json.loads(baseline(folder/'source_to_output.json'))['matches']
        def period_substitution(field):
            chosen=next(r for r in links if r['duration'].get(field)is not None and r['duration'][field]!=r['score_evidence']['regulation_time'])
            def alter(x):
                row=next(r for r in x[1:]if r[0]==chosen['match_id']);row[7:9]=list(map(str,chosen['duration'][field]))
            return alter
        mutation('extra-time score substituted',v.NAME,period_substitution('after_extra_time_score'),'csv')
        mutation('shootout score substituted',v.NAME,period_substitution('shootout_score'),'csv')
        mutation('incorrect outcome','source_to_output.json',lambda x:x['matches'][0].__setitem__('outcome','invalid'))
        mutation('invalid date',v.NAME,lambda x:x[1].__setitem__(4,'2010-02-30'),'csv')
        mutation('incorrect season',v.NAME,lambda x:x[1].__setitem__(3,'1900/1901'),'csv')
        mutation('incorrect stage','source_to_output.json',lambda x:x['matches'][0].__setitem__('stage','SYNTHETIC_WRONG_STAGE'))
        mutation('lost neutral metadata','neutral_venue.json',lambda x:x['matches'].pop())
        mutation('incorrect exclusion accounting','excluded_events.json',lambda x:x['events'].pop())
        mutation('broken provenance crosswalk','source_to_output.json',lambda x:x['matches'][0]['observations'].pop())
        mutation('invalid column order',v.NAME,lambda x:x[0].reverse(),'csv')
        mutation('altered team code','team_mapping.json',lambda x:x['teams'][0].__setitem__('team_code','zzzz'))
        mutation('lost original identifier crosswalk','match_id_crosswalk.csv',lambda x:x.pop(),'csv')
        mutation('corrupted season total','season_coverage.csv',lambda x:x[1].__setitem__(1,'0'),'csv')
        mutation('administrative score substituted',v.NAME,period_admin(links),'csv')
        corrected=next(r for r in links if r['standardization_corrections'])
        def revert_date(x):
            row=next(r for r in x[1:]if r[0]==corrected['match_id']);row[4]=corrected['date_evidence']['date']
        mutation('historically corrected date reverted',v.NAME,revert_date,'csv')
    finally:v.read=original_read
    return dict(status='PASS',scenarios=len(results),all_detected=True,original_files_mutated=False,method='In-memory serialized copies; independently reparsed by validator; immutable originals remain untouched',results=results)

def period_admin(links):
    chosen=next(r for r in links if r['administrative_result']is not None and r['administrative_result']!=r['score_evidence']['regulation_time'])
    def alter(x):
        row=next(r for r in x[1:]if r[0]==chosen['match_id']);row[7:9]=list(map(str,chosen['administrative_result']))
    return alter

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--inventory',type=Path,default=v.PHASE/'validated');p.add_argument('--output',type=Path,default=v.PHASE/'adverse_validation.json');a=p.parse_args();out=a.output.resolve();v.require(out.is_relative_to(v.PHASE.resolve())or out.is_relative_to(Path('/private/tmp')),'Private output required');result=run(a.inventory)
    with out.open('xb')as f:f.write(v.wire(result))
    print('PASS',result['scenarios'],'adverse corruptions detected')
