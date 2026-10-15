from pathlib import Path
import subprocess,json,datetime,os
t=Path(__file__).resolve().parent;r=Path('/workspaces/repository')
command=['/usr/bin/python3','-m','pip','--python',str(t/'runtime/bin/python'),'install','cuda-python==12.9.7','cuda-bindings==12.9.9']
with (t/'pin_repair.stdout').open('x') as out,(t/'pin_repair.stderr').open('x') as err:
 z=subprocess.run(command,cwd=r,stdout=out,stderr=err)
assert z.returncode==0
with (t/'packages.json').open('w') as out:subprocess.run(['/usr/bin/python3','-m','pip','--python',str(t/'runtime/bin/python'),'list','--format=json'],stdout=out,check=True)
old=json.loads((r/'bench/results/batch_capacity_20261015/packages.json').read_text());new=json.loads((t/'packages.json').read_text())
aa={x['name'].lower():x['version'] for x in old};bb={x['name'].lower():x['version'] for x in new}
delta={k:[aa.get(k),bb.get(k)] for k in sorted(aa.keys()|bb.keys()) if aa.get(k)!=bb.get(k)}
(t/'package_comparison.json').write_text(json.dumps(delta,indent=2));assert not delta,delta
entry=json.loads((t/'entry.json').read_text())
for n,old in entry['preserved'].items():
 p=r/n;s=p.lstat();actual=dict(inode=s.st_ino,size=s.st_size,mtime_ns=s.st_mtime_ns,symlink=str(p.readlink()) if p.is_symlink() else None)
 assert old==actual,n
record=dict(exit=0,command=command,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),package_comparison=delta,scope='Pinned only2 test-runtime packages to the previous qualified versions before any GPU serving. Successful existing builds reused; first setup failure remains recorded.')
(t/'dependency_repair.json').write_text(json.dumps(record,indent=2));(t/'setup.exit.json').write_text(json.dumps(record,indent=2))
print(json.dumps(record))
