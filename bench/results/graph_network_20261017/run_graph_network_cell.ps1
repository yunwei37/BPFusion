param([Parameter(Mandatory=$true)][string]$ClientPod,[Parameter(Mandatory=$true)][string]$ServerIP,
[Parameter(Mandatory=$true)][string]$Tag,[Parameter(Mandatory=$true)][string]$Operation,
[Parameter(Mandatory=$true)][string]$Mode,[int]$Repeat=1,[int]$Cores=0,[int]$Rate=1000,
[int]$Seconds=6,[int]$Seed=20261017,[string]$Stage="screen",[string]$KubectlHome=".\scripts\kubectl-home.ps1")
$ErrorActionPreference="Stop"
$taskServerPod="coder-eb48d962-76f4-4ff7-bac5-7bc62ec2ada3-5c8bb655f6-khnns"
$taskTemp="/tmp/bpfusion-mixed-integration-n4cog5c6"
$taskDirectory="$taskTemp/graph_network_$Stage"
$taskArchive="/workspaces/repository/bench/results/graph_network_20261017/$Stage"
$taskPrefix="$taskDirectory/$Tag"
function Invoke-Workspace([string]$Code) {
 $taskAnswer=$Code | & $KubectlHome -n coder exec -i $taskServerPod '--' python3 -
 if($LASTEXITCODE -ne 0){throw "Workspace command failed"}
 return ($taskAnswer -join [Environment]::NewLine)
}
function Receive-ClientFile([string]$Name,[string]$Destination) {
 $taskCompress='import pathlib,gzip,json;p=pathlib.Path("/tmp/{0}");q=pathlib.Path("/tmp/{0}.transfer.gz");raw=p.read_bytes();q.write_bytes(gzip.compress(raw,mtime=0)) if not q.exists() else None;assert gzip.decompress(q.read_bytes())==raw;print(json.dumps([len(raw),q.stat().st_size]))' -f $Name
 $taskReply=& $KubectlHome -n coder exec $ClientPod '--' python3 -c $taskCompress
 if($LASTEXITCODE -ne 0){throw "Prepare original data transfer failed"}
 $taskInfo=@($taskReply)[-1] | ConvertFrom-Json
 $taskInit=@"
from pathlib import Path
p=Path('$Destination.gz')
if not p.exists():p.touch(exist_ok=False)
print(p.stat().st_size)
"@
 $taskInitialOffset=Invoke-Workspace $taskInit
 $taskOffset=[long](($taskInitialOffset -split "\r?\n")[-1])
 if($taskOffset -gt $taskInfo[1]){throw "Existing transfer longer than original"}
 while($taskOffset -lt $taskInfo[1]) {
  $taskChunk=[Math]::Min([long]1048576,[long]$taskInfo[1]-$taskOffset)
  $taskRead='import base64,pathlib;p=pathlib.Path("/tmp/{0}.transfer.gz");print(base64.b64encode(p.read_bytes()[{1}:{2}]).decode())' -f $Name,$taskOffset,($taskOffset+$taskChunk)
  $taskPayload=& $KubectlHome -n coder exec $ClientPod '--' python3 -c $taskRead
  if($LASTEXITCODE -ne 0){throw "Original data chunk read failed; retain durable prefix"}
  $taskPayload=@($taskPayload)[-1]
  $taskWrite='import sys,base64,pathlib,os;p=pathlib.Path("{0}.gz");data=base64.b64decode(sys.stdin.buffer.read());raw=p.read_bytes();assert len(data)=={1} and len(raw)>={2};present=raw[{2}:{2}+len(data)];assert present==data[:len(present)];fd=os.open(p,os.O_WRONLY);written=os.pwrite(fd,data,{2});os.close(fd);assert written==len(data)' -f $Destination,$taskChunk,$taskOffset
  $taskPayload | & $KubectlHome -n coder exec -i $taskServerPod '--' python3 -c $taskWrite
  if($LASTEXITCODE -ne 0){throw "Original data chunk write failed; retain durable prefix"}
  $taskOffset+=$taskChunk
 }
 $taskVerify=@"
from pathlib import Path
import gzip
p=Path('$Destination.gz')
assert p.stat().st_size==$($taskInfo[1])
assert len(gzip.decompress(p.read_bytes()))==$($taskInfo[0])
print('original data transfer complete')
"@
 Invoke-Workspace $taskVerify | Out-Null
}
function Start-Observer([string]$Prefix,[int]$ServerPid) {
 $taskCode=@"
from pathlib import Path
import subprocess,json,os,time
t=Path('$taskTemp');prefix=Path('$Prefix')
env=dict(os.environ,**json.loads((t/'environment.json').read_text()))
with Path(str(prefix)+'.observer.stdout').open('x') as o,Path(str(prefix)+'.observer.stderr').open('x') as e:
 p=subprocess.Popen([str(t/'runtime/bin/python'),str(t/'resource_observer.py'),'--pid','$ServerPid','--output',str(prefix)+'.resources.jsonl'],env=env,stdout=o,stderr=e,start_new_session=True)
Path(str(prefix)+'.observer_started.json').write_text(json.dumps(dict(pid=p.pid,command=p.args)))
while True:
 lines=Path(str(prefix)+'.resources.jsonl').read_text().splitlines() if Path(str(prefix)+'.resources.jsonl').exists() else []
 if len(lines)>=2:
  assert json.loads(lines[1])['event']=='sample';break
 assert p.poll() is None,Path(str(prefix)+'.observer.stderr').read_text()
 time.sleep(.01)
print(p.pid)
"@
 return [int](Invoke-Workspace $taskCode)
}
function Stop-Observer([int]$ObserverPid,[string]$Prefix) {
 $taskCode=@"
from pathlib import Path
import os,signal,time,json
p=Path('$Prefix.resources.jsonl');os.kill($ObserverPid,signal.SIGTERM)
while True:
 lines=p.read_text().splitlines()
 if lines and json.loads(lines[-1])['event']=='observer_terminal':break
 time.sleep(.05)
print('observer terminal')
"@
 Invoke-Workspace $taskCode | Out-Null
}

Invoke-Workspace "from pathlib import Path;Path('$taskDirectory').mkdir(exist_ok=True);Path('$taskArchive').mkdir(exist_ok=True)" | Out-Null
$taskServerPid=$null;$taskObserverPid=$null
try {
 $taskCode=@"
from pathlib import Path
import subprocess,json,time
t=Path('$taskTemp');prefix=Path('$taskPrefix');r=Path('/workspaces/repository')
with Path(str(prefix)+'.wrapper.stdout').open('x') as o,Path(str(prefix)+'.wrapper.stderr').open('x') as e:
 p=subprocess.Popen(['/usr/bin/python3',str(r/'bench/results/graph_network_20261017/graph_network_server.py'),
 '--runtime',str(t),'--prefix',str(prefix),'--bind','$ServerIP','--mode','$Mode',
 '--operation','$Operation','--repeat','$Repeat','--cores','$Cores'],stdout=o,stderr=e,start_new_session=True)
while True:
 log=Path(str(prefix)+'.server.stdout');terminal=Path(str(prefix)+'.server_terminal.json')
 assert not terminal.exists(),terminal.read_text() if terminal.exists() else ''
 if log.exists() and 'graph backend ready:' in log.read_text():break
 assert p.poll() is None,'wrapper exited';time.sleep(.1)
print(json.loads(Path(str(prefix)+'.server_started.json').read_text())['pid'])
"@
 $taskServerPid=[int](Invoke-Workspace $taskCode)
 Write-Output "READY $Tag service_pid=$taskServerPid"
 $taskWarm="$Tag.warmup.jsonl"
 & $KubectlHome -n coder exec $ClientPod '--' python3 /tmp/graph_network_client.py --host $ServerIP --operation $Operation --rate 1000 --seconds 0.032 --seed $Seed --output "/tmp/$taskWarm"
 if($LASTEXITCODE -ne 0){throw "Warmup execution failed"}
 $taskWarmCheck='import json,pathlib;rows=[json.loads(x) for x in pathlib.Path("/tmp/{0}").read_text().splitlines()];q=[x for x in rows if x["event"]=="request"];assert len(q)==32 and all(x["outcome"]=="success" for x in q);print("32 numerical warmups passed")' -f $taskWarm
 & $KubectlHome -n coder exec $ClientPod '--' python3 -c $taskWarmCheck
 if($LASTEXITCODE -ne 0){throw "Warmup numerical validation failed"}

 if($Cores -gt 0){
  Invoke-Workspace @"
from pathlib import Path
import os,json
receipt=json.loads(Path('$taskPrefix.server_started.json').read_text())
pid=receipt['pid'];assert pid==$taskServerPid
allowed=set(receipt['service_affinity']);rows=[]
for p in Path('/proc/%d/task'%pid).iterdir():
 tid=int(p.name);previous=sorted(os.sched_getaffinity(tid));os.sched_setaffinity(tid,allowed)
 current=sorted(os.sched_getaffinity(tid));assert set(current)==allowed
 rows.append(dict(tid=tid,before=previous,after=current))
Path('$taskPrefix.affinity_applied.json').write_text(json.dumps(dict(pid=pid,threads=rows,scope='only this benchmark service TGID'),indent=2))
print('owned service thread affinity applied')
"@ | Out-Null
 }
 $taskObserverPid=Start-Observer "$taskPrefix.idle" $taskServerPid
 Start-Sleep -Seconds 3
 Stop-Observer $taskObserverPid "$taskPrefix.idle";$taskObserverPid=$null
 $taskObserverPid=Start-Observer $taskPrefix $taskServerPid
 $taskName="$Tag.client.jsonl"
 $taskStart=[DateTime]::UtcNow.ToString('o')
 & $KubectlHome -n coder exec $ClientPod '--' python3 /tmp/graph_network_client.py --host $ServerIP --operation $Operation --rate $Rate --seconds $Seconds --seed $Seed --output "/tmp/$taskName"
 $taskClientExit=$LASTEXITCODE;$taskEnd=[DateTime]::UtcNow.ToString('o')
 Stop-Observer $taskObserverPid $taskPrefix;$taskObserverPid=$null
 $taskJSON=@{exit=$taskClientExit;begin_utc=$taskStart;end_utc=$taskEnd;rate=$Rate;seconds=$Seconds;seed=$Seed;operation=$Operation;mode=$Mode;repeat=$Repeat;cores=$Cores;clientPod=$ClientPod}|ConvertTo-Json -Compress
 $taskSink='import sys,pathlib;pathlib.Path("{0}.client_exit.json").write_bytes(sys.stdin.buffer.read())' -f $taskPrefix
 $taskJSON | & $KubectlHome -n coder exec -i $taskServerPod '--' python3 -c $taskSink
 if($LASTEXITCODE -ne 0){throw "Client receipt write failed"}
 if($taskClientExit -ne 0){throw "Client execution failed"}
 Write-Output "MEASURED $Tag"
} finally {
 if($taskObserverPid){Stop-Observer $taskObserverPid $taskPrefix}
 if($taskServerPid){
  Invoke-Workspace @"
from pathlib import Path
import os,signal,time,json
os.killpg($taskServerPid,signal.SIGTERM)
p=Path('$taskPrefix.server_terminal.json')
while not p.exists():time.sleep(.1)
row=json.loads(p.read_text());assert row.get('exit')==0 and not row.get('remaining_pins'),row
print('server terminal')
"@ | Out-Null
 }
}
Receive-ClientFile $taskWarm "$taskPrefix.warmup.jsonl"
Receive-ClientFile $taskName "$taskPrefix.client.jsonl"
$taskProofCode=@"
from pathlib import Path
import json
p=Path('/tmp/$taskName');proof=[];original=None;meta=None
with p.open('rb') as source:
 for line in source:
  if meta is None:meta=json.loads(line);continue
  if line.startswith(b'{"event":"worker_metadata"'):
   assert original is None
   part=json.loads(line)['part'];name=meta['worker_files'][part]
   original=(p.parent/name).open('rb');size=0
  if original is not None:
   assert original.readline()==line,(name,'merged worker bytes differ')
   size+=len(line)
  if line.startswith(b'{"event":"worker_terminal"'):
   assert original.read(1)==b'';original.close();original=None
   proof.append(dict(name=name,bytes=size))
assert original is None and len(proof)==meta['workers']
print(json.dumps(proof))
"@
$taskProofOutput=$taskProofCode | & $KubectlHome -n coder exec -i $ClientPod '--' python3 -
if($LASTEXITCODE -ne 0){throw "Original worker byte proof failed"}
$taskProofJSON=$taskProofOutput -join [Environment]::NewLine
Invoke-Workspace @"
from pathlib import Path
import gzip,json
d=Path('$taskDirectory');proof=json.loads('''$taskProofJSON''')
expected={x['name']:x['bytes'] for x in proof};meta=None;dest=None;count=0;written=[]
with gzip.open(d/'$Tag.client.jsonl.gz','rb') as source:
 for line in source:
  if meta is None:meta=json.loads(line);continue
  if line.startswith(b'{"event":"worker_metadata"'):
   assert dest is None
   name=meta['worker_files'][json.loads(line)['part']]
   assert name in expected and Path(name).name==name
   dest=gzip.GzipFile(filename=str(d/(name+'.gz')),mode='wb',mtime=0);count=0
  if dest is not None:dest.write(line);count+=len(line)
  if line.startswith(b'{"event":"worker_terminal"'):
   dest.close();dest=None;assert count==expected[name];written.append(name)
assert dest is None and set(written)==set(expected)
(d/'$Tag.worker_reconstruction.json').write_text(json.dumps(dict(original_client_byte_comparison_passed=True,workers=proof),indent=2))
print('original worker bytes recovered from lossless merged log')
"@ | Out-Null
Invoke-Workspace @"
from pathlib import Path
import gzip,json,shutil,subprocess
d=Path('$taskDirectory');out=Path('$taskArchive')
for p in d.glob('$Tag.*'):
 if not p.is_file():continue
 dest=out/(p.name+'.gz' if p.suffix=='.jsonl' else p.name);assert not dest.exists(),dest
 if p.suffix=='.jsonl':dest.write_bytes(gzip.compress(p.read_bytes(),mtime=0));assert gzip.decompress(dest.read_bytes())==p.read_bytes()
 else:shutil.copyfile(p,dest)
cmd=['/usr/bin/python3','/workspaces/repository/bench/graph_network_analysis.py',str(out/'$Tag')]
with (out/'$Tag.analysis.stdout').open('x') as o,(out/'$Tag.analysis.stderr').open('x') as e:
 z=subprocess.run(cmd,stdout=o,stderr=e)
(out/'$Tag.analysis_exit.json').write_text(json.dumps(dict(command=cmd,exit=z.returncode)))
assert z.returncode==0,(out/'$Tag.analysis.stderr').read_text()
m=json.loads((out/'$Tag.metrics.json').read_text())
print(json.dumps({k:m[k] for k in ['tag','attempts','failures','throughput','owned_group_cpu_ms_per_attempt','latency']}))
"@
Write-Output "PASS $Tag"
