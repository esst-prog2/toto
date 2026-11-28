"""Fresh offline reconstruction from frozen originals through all five phases."""
import argparse,csv,io,json,os,subprocess,sys,tempfile
from pathlib import Path
from scripts import standardize_uefa_europa_league as s
PHASE=s.BASE/'phase5'
def child(fresh):
 import socket
 def deny(*a,**k):raise AssertionError('Offline pipeline prohibits network and DNS')
 socket.socket.connect=deny;socket.create_connection=deny;socket.getaddrinfo=deny
 # Read-only mmap avoids buffered reads of cloud-backed originals.
 Path.read_bytes=lambda path:s.read(path)
 from scripts import assess_uefa_europa_league_phase1 as a
 from scripts import inventory_uefa_europa_league as p2
 from scripts import review_uefa_europa_league_history as p3
 from scripts import verify_uefa_europa_league_inventory as v2
 from scripts import verify_uefa_europa_league_history as v3
 from scripts import verify_uefa_europa_league_standardization as v4
 from scripts import finalize_uefa_europa_league as p5
 from scripts import verify_uefa_europa_league_final as v5
 artifacts=[]
 def compare(label,raw,accepted):
  s.require(raw==s.read(accepted),'Offline byte mismatch: '+label);artifacts.append(dict(path=label,bytes=len(raw),sha256=s.sha(raw)))
 result=a.assess();base=s.BASE/'phase1'
 for name,key in [('acquisition_manifest.json','manifest'),('preliminary_readability.json',None),('wikipedia_attribution.json','wikipedia')]:
  value=result[key]if key else{k:v for k,v in result.items()if k not in('manifest','coverage','wikipedia')};compare('phase1/'+name,a.a.encode(value),base/name)
 buffer=io.StringIO(newline='');writer=csv.DictWriter(buffer,fieldnames=list(result['coverage'][0]));writer.writeheader();writer.writerows(result['coverage']);compare('phase1/season_coverage.csv',buffer.getvalue().encode(),base/'season_coverage.csv')
 t2=fresh/'phase2';p2.run(t2)
 for path in sorted(t2.iterdir()):compare('phase2/'+path.name,s.read(path),s.BASE/'phase2/validated'/path.name)
 result=v2.verify(t2);compare('phase2/independent_validation.json',v2.wire(result),s.BASE/'phase2/independent_validation.json')
 t3=fresh/'phase3';t3.mkdir();p3.P2=t2;p3.run(t3/'final')
 for path in sorted((t3/'final').iterdir()):compare('phase3/'+path.name,s.read(path),s.P3/'final'/path.name)
 result=v3.verify(t3/'final');compare('phase3/independent_validation.json',v3.wire(result),s.P3/'independent_validation.json')
 original3=s.P3;original4=s.PHASE
 for name in [*s.load(original4/'approval.json')['phase3_inputs']]:
  if not name.startswith('final/'):(t3/name).symlink_to(original3/name)
 s.P3=t3;t4=fresh/'phase4';s.run(t4/'validated')
 for path in sorted((t4/'validated').iterdir()):compare('phase4/'+path.name,s.read(path),original4/'validated'/path.name)
 result=v4.verify(t4/'validated');compare('phase4/independent_validation.json',v4.wire(result),original4/'independent_validation.json')
 for name in ['verification.json','approval.json','reference','team_mapping_decisions.json','team_compatibility_final.json','code_policy.json','historical_corrections.json']:(t4/name).symlink_to(original4/name)
 s.PHASE=t4;t5=fresh/'phase5';p5.run(t5)
 for path in sorted(t5.iterdir()):compare('phase5/'+path.name,s.read(path),PHASE/'final'/path.name)
 result=v5.verify(t5);compare('phase5/independent_validation.json',v5.v.wire(result),PHASE/'independent_validation.json')
 receipt=dict(status='PASS',network_and_dns_prohibited=True,fresh_process=True,original_payloads=85,artifacts=artifacts,byte_identical_artifacts=len(artifacts),phase_counts={f'phase{i}':sum(a['path'].startswith(f'phase{i}/')for a in artifacts)for i in range(1,6)},method='No observation cache: original Phase1 diagnostics, fresh raw Phase2 parsing, fresh Phase3 adjudication, fresh standardized projection, final identity reconciliation and independent receipts; frozen decisions and code/reference bindings retained')
 with(fresh/'pipeline_receipt.json').open('xb')as f:f.write(s.wire(receipt))
 return receipt
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--child',type=Path);p.add_argument('--output',type=Path,default=PHASE/'pipeline_reproduction.json');a=p.parse_args()
 if a.child:child(a.child)
 else:
  output=a.output.resolve();s.require(output.is_relative_to(PHASE.resolve())or output.is_relative_to(Path('/private/tmp')),'Private receipt required');fresh=Path(tempfile.mkdtemp(prefix='uel-five-phase-',dir='/private/tmp'));env=os.environ|{'PYTHONPATH':str(s.ROOT/'src')+os.pathsep+str(s.ROOT),'PYTHONDONTWRITEBYTECODE':'1'}
  result=subprocess.run([sys.executable,'-B','-m','scripts.reproduce_uefa_europa_league_pipeline','--child',str(fresh)],env=env,cwd=s.ROOT,capture_output=True)
  with(PHASE/'pipeline_child.log').open('xb')as f:f.write(result.stdout+result.stderr)
  s.require(result.returncode==0,'Offline pipeline failed; inspect private pipeline_child.log')
  raw=s.read(fresh/'pipeline_receipt.json')
  with output.open('xb')as f:f.write(raw)
  print('PASS',json.loads(raw)['byte_identical_artifacts'],'byte-identical artifacts across five phases')
