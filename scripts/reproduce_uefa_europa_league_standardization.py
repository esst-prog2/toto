"""Fresh-process, network-disabled byte reproduction of private Phase 4 artifacts."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from scripts import standardize_uefa_europa_league as s

CHILD="""import runpy,socket,sys
socket.socket.connect=lambda *a,**k:(_ for _ in ()).throw(AssertionError('Offline reproduction forbids connections'))
socket.create_connection=socket.socket.connect
socket.getaddrinfo=socket.socket.connect
module=sys.argv.pop(1)
runpy.run_module(module,run_name='__main__')
"""
def run():
    fresh=Path(tempfile.mkdtemp(prefix='uel-phase4-offline-',dir='/private/tmp'))
    env=os.environ|{'PYTHONPATH':str(s.ROOT/'src')+os.pathsep+str(s.ROOT),'PYTHONDONTWRITEBYTECODE':'1'}
    commands=[('scripts.standardize_uefa_europa_league',['--output',str(fresh)]),('scripts.verify_uefa_europa_league_standardization',['--inventory',str(fresh),'--output',str(fresh/'independent_validation.json')])]
    for module,args in commands:
        result=subprocess.run([sys.executable,'-B','-c',CHILD,module,*args],cwd=s.ROOT,env=env,capture_output=True)
        with(fresh/(module.rsplit('.',1)[-1]+'.log')).open('xb')as f:f.write(result.stdout+result.stderr)
        s.require(result.returncode==0,'Offline child failed: '+module+'; see private temporary logs')
    names=sorted(p.name for p in(s.PHASE/'validated').iterdir()if p.is_file())
    artifacts=[]
    for name in names:
        raw=s.read(fresh/name);s.require(raw==s.read(s.PHASE/'validated'/name),'Rebuild differs: '+name);artifacts.append(dict(path=name,bytes=len(raw),sha256=s.sha(raw)))
    raw=s.read(fresh/'independent_validation.json');s.require(raw==s.read(s.PHASE/'independent_validation.json'),'Rebuilt independent receipt differs');artifacts.append(dict(path='independent_validation.json',bytes=len(raw),sha256=s.sha(raw)))
    return dict(status='PASS',fresh_processes=2,network_and_dns_prohibited=True,producer_artifacts=len(names),identical_artifacts=len(artifacts),artifacts=artifacts,method='Fresh private temporary directory, accepted Phase3 and frozen convention/mapping inputs; deterministic data and independent receipt byte comparison')
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=s.PHASE/'reproduction.json');a=p.parse_args();out=a.output.resolve();s.require(out.is_relative_to(s.PHASE.resolve())or out.is_relative_to(Path('/private/tmp')),'Private output required');result=run()
    with out.open('xb')as f:f.write(s.wire(result))
    print('PASS',result['identical_artifacts'],'byte-identical artifacts')
