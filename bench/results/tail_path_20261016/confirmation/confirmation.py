from pathlib import Path
import os,subprocess,json,time,datetime,sys
t=Path(__file__).resolve().parent;r=Path('/workspaces/repository');d=t/'confirm'
print('WAIT candidate safety',flush=True)
while not (t/'fixed_safety.exit.json').exists():time.sleep(1)
assert json.loads((t/'fixed_safety.exit.json').read_text())['exit']==0
assert not list(Path('/sys/fs/bpf').glob('bpfusion*'))
assert not [p for p in Path('/sys/kernel/tracing/instances').glob('bpfusion-tail-*')]
archive=r/'bench/results/tail_path_20261016/confirmation_sources';archive.mkdir()
for f in d.iterdir():
 if f.is_file():(archive/f.name).write_bytes(f.read_bytes())
(archive/'fixed_build.py').write_bytes((t/'fixed_build.py').read_bytes())
(archive/'fixed.Makefile').write_bytes((t/'fixed.Makefile').read_bytes())
for n in ['fixed_build.statuses.json','fixed_build.exit.json','fixed_build8.stdout','fixed_build8.stderr','fixed_build16.stdout','fixed_build16.stderr','environment.json','models.json']:
 (archive/n).write_bytes((t/n).read_bytes())
env=dict(os.environ,**json.loads((t/'environment.json').read_text()))
model=json.loads((t/'models.json').read_text())['qwen'];statuses=[]
for stage,extra in [('preflight',['--preflight']),('full',[])]:
 path=d/(stage+'.jsonl');cmd=[str(t/'runtime/bin/python'),str(d/'load.py'),'--model',model,'--output',str(path),'--banks','16']+extra
 print('START',stage,flush=True)
 with (d/(stage+'.stdout')).open('x') as out,(d/(stage+'.stderr')).open('x') as err:z=subprocess.run(cmd,cwd=r,env=env,stdout=out,stderr=err)
 rec=dict(stage=stage,command=cmd,exit=z.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 if z.returncode==0:
  ac=['/usr/bin/python3',str(d/'analyze.py'),str(path)]
  with (d/(stage+'.analysis.stdout')).open('x') as out,(d/(stage+'.analysis.stderr')).open('x') as err:az=subprocess.run(ac,cwd=r,stdout=out,stderr=err)
  rec.update(analysis_command=ac,analysis_exit=az.returncode)
 statuses.append(rec);(t/'confirmation.statuses.json').write_text(json.dumps(statuses,indent=2));print('TERMINAL',rec,flush=True)
 if z.returncode or rec.get('analysis_exit',0):break
ok=len(statuses)==2 and all(x['exit']==0 and x.get('analysis_exit',0)==0 for x in statuses)
(t/'confirmation.exit.json').write_text(json.dumps(dict(exit=0 if ok else 1,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())))
sys.exit(0 if ok else 1)
