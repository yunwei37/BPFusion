param([Parameter(Mandatory=$true)][string]$ClientPod,[Parameter(Mandatory=$true)][string]$ServerIP,[switch]$Preflight,[string]$KubectlHome=".\scripts\kubectl-home.ps1")
$ErrorActionPreference="Stop"
$taskServerPod="coder-eb48d962-76f4-4ff7-bac5-7bc62ec2ada3-5c8bb655f6-khnns"
$taskTemp="/tmp/bpfusion-mixed-integration-n4cog5c6"
$taskStage="official_client_gc_payload_diagnostic"
$taskDirectory="$taskTemp/$taskStage"
function Invoke-Workspace([string]$Code) {
 $taskAnswer=$Code | & $KubectlHome -n coder exec -i $taskServerPod '--' python3 -
 if($LASTEXITCODE -ne 0){throw "Workspace command failed"}
 return ($taskAnswer -join [Environment]::NewLine)
}
function Receive-ClientFile([string]$Name,[string]$Destination) {
 $taskCompress='import pathlib,gzip,json;p=pathlib.Path("/tmp/{0}");q=pathlib.Path("/tmp/{0}.transfer.gz");raw=p.read_bytes();q.write_bytes(gzip.compress(raw,mtime=0)) if not q.exists() else None;assert gzip.decompress(q.read_bytes())==raw;print(json.dumps([len(raw),q.stat().st_size]))' -f $Name
 $taskReply=& $KubectlHome -n coder exec $ClientPod '--' python3 -c $taskCompress
 if($LASTEXITCODE -ne 0){throw "Prepare original data transfer failed"}
 $taskInfo=($taskReply -join "") | ConvertFrom-Json
 $taskInit=@"
from pathlib import Path
p=Path('$Destination.gz')
if not p.exists():p.touch(exist_ok=False)
print(p.stat().st_size)
"@
 $taskOffset=[long](Invoke-Workspace $taskInit)
 if($taskOffset -gt $taskInfo[1]){throw "Existing transfer longer than original"}
 while($taskOffset -lt $taskInfo[1]) {
  $taskChunk=[Math]::Min([long]1048576,[long]$taskInfo[1]-$taskOffset)
  $taskRead='import base64,pathlib;p=pathlib.Path("/tmp/{0}.transfer.gz");print(base64.b64encode(p.read_bytes()[{1}:{2}]).decode())' -f $Name,$taskOffset,($taskOffset+$taskChunk)
  $taskPayload=& $KubectlHome -n coder exec $ClientPod '--' python3 -c $taskRead
  if($LASTEXITCODE -ne 0){throw "Original data chunk read failed; retain durable prefix"}
  $taskWrite='import sys,base64,pathlib;p=pathlib.Path("{0}.gz");data=base64.b64decode(sys.stdin.buffer.read());assert len(data)=={1} and p.stat().st_size=={2};p.open("ab").write(data)' -f $Destination,$taskChunk,$taskOffset
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
Invoke-Workspace "from pathlib import Path;Path('$taskDirectory').mkdir(exist_ok=True)" | Out-Null
$taskPairs=@(0)
foreach($taskPair in $taskPairs) {
 $taskOrders=@(@("candidate","native","official"),@("native","official","candidate"),@("official","candidate","native"),@("official","native","candidate"),@("native","candidate","official"))
 $taskConditions=@("official")
 foreach($taskCondition in $taskConditions) {
  $taskMode=if($taskCondition -eq "candidate"){"kernel"}else{$taskCondition}
  $taskBuild=if($taskCondition -eq "candidate"){"kernel_owned_build16"}else{"active_wait_sourcebuild16"}
  $taskTag=$taskStage+"_p"+$taskPair+"_"+$taskCondition
  $taskPrefix=$taskDirectory+"/"+$taskTag
  $taskRetained=Invoke-Workspace @"
from pathlib import Path
import json
p=Path('$taskPrefix.server_terminal.json')
if p.exists():
 row=json.loads(p.read_text());assert row.get('exit')==0 and not row.get('pins')
 archive=Path('/workspaces/repository/bench/results/official_sustained_20261016')/'$taskStage'
 assert (archive/('$taskTag'+'_r192.client.jsonl.gz')).exists()
 print('retained')
else:print('pending')
"@
  if($taskRetained -eq "retained"){Write-Output "RETAIN completed pair=$taskPair condition=$taskCondition";continue}
  $taskServerPid=$null;$taskObserverPid=$null
  Write-Output "START $taskStage pair=$taskPair mode=$taskMode"
  try {
   $taskCode=@"
from pathlib import Path
import subprocess,json,time
t=Path('$taskTemp');prefix=Path('$taskPrefix')
with Path(str(prefix)+'.wrapper.stdout').open('x') as o,Path(str(prefix)+'.wrapper.stderr').open('x') as e:
 p=subprocess.Popen(['/usr/bin/python3',str(t/'official_remote_server.py'),'--prefix',str(prefix),'--bind','$ServerIP','--build',str(t/'$taskBuild'),'--pair','$taskPair','--mode','$taskMode'],stdout=o,stderr=e,start_new_session=True)
while True:
 log=Path(str(prefix)+'.server.stdout');terminal=Path(str(prefix)+'.server_terminal.json')
 assert not terminal.exists(),terminal.read_text() if terminal.exists() else ''
 if ('$taskCondition'=='official' and Path(str(prefix)+'.official_ready.json').exists()) or ('$taskCondition'!='official' and log.exists() and 'resident vLLM ready:' in log.read_text()):break
 time.sleep(.1)
print(json.loads(Path(str(prefix)+'.server_started.json').read_text())['pid'])
"@
   $taskServerPid=[int](Invoke-Workspace $taskCode)
   $taskWarm=$taskTag+".warmup.jsonl"
   & $KubectlHome -n coder exec $ClientPod '--' python3 /tmp/official_client_gc_payload_diagnostic.py --host $ServerIP --config /tmp/qwen_frozen.json --offsets /tmp/remote_offsets.json --output "/tmp/$taskWarm" --pair $taskPair --mode $taskMode --rate 96 --warmup
   if($LASTEXITCODE -ne 0){throw "Warmup failed"}
   $taskCell="$taskPrefix.idle";$taskObserverPid=Start-Observer $taskCell $taskServerPid
   Start-Sleep -Seconds 5
   Stop-Observer $taskObserverPid $taskCell;$taskObserverPid=$null
   $taskRates=@(192)
   foreach($taskRate in $taskRates) {
    $taskCell=$taskPrefix+"_r"+$taskRate
    $taskName=$taskTag+"_r"+$taskRate+".client.jsonl"
    $taskObserverPid=Start-Observer $taskCell $taskServerPid
    Write-Output "CELL pair=$taskPair mode=$taskMode rate=$taskRate begin"
    $taskClientArgs=@("python3","/tmp/official_client_gc_payload_diagnostic.py","--host",$ServerIP,"--config","/tmp/qwen_frozen.json","--offsets","/tmp/remote_offsets.json","--output","/tmp/$taskName","--pair","$taskPair","--mode",$taskMode,"--rate","$taskRate")
    
    if($Preflight){
     $taskOffsetIndex=[array]::IndexOf($taskClientArgs,"/tmp/remote_offsets.json")
     $taskClientArgs[$taskOffsetIndex]="/tmp/cpu_profile_preflight_offsets.json"
    }
    $taskBegin=[DateTime]::UtcNow.ToString('o')
    $taskClientOutput=& $KubectlHome -n coder exec $ClientPod '--' @taskClientArgs 2>&1
    $taskClientExit=$LASTEXITCODE;$taskEnd=[DateTime]::UtcNow.ToString('o')
    Stop-Observer $taskObserverPid $taskCell;$taskObserverPid=$null
    $taskReceipt=@{command=$taskClientArgs;exit=$taskClientExit;stdout_stderr=($taskClientOutput -join [Environment]::NewLine);begin_utc=$taskBegin;end_utc=$taskEnd;clientPod=$ClientPod}
    $taskReceiptJSON=$taskReceipt|ConvertTo-Json -Depth 5 -Compress
    $taskSink='import sys,pathlib;pathlib.Path("{0}.client_exit.json").write_bytes(sys.stdin.buffer.read())' -f $taskCell
    $taskReceiptJSON | & $KubectlHome -n coder exec -i $taskServerPod '--' python3 -c $taskSink
    if($LASTEXITCODE -ne 0){throw "Receipt write failed"}
    if($taskClientExit -ne 0){throw "Client execution failed"}
    Write-Output "CELL pair=$taskPair mode=$taskMode rate=$taskRate terminal"
   }
  } finally {
   if($taskObserverPid){Stop-Observer $taskObserverPid $taskCell}
   if($taskServerPid) {
    $taskCode=@"
from pathlib import Path
import os,signal,time,json
os.killpg($taskServerPid,signal.SIGTERM)
p=Path('$taskPrefix.server_terminal.json')
while not p.exists():time.sleep(.1)
row=json.loads(p.read_text());assert row.get('exit')==0 and not row.get('pins'),row
print('server terminal')
"@
    Invoke-Workspace $taskCode | Out-Null
   }
  }
  Receive-ClientFile $taskWarm "$taskPrefix.warmup.jsonl"
  Receive-ClientFile $taskName "$taskCell.client.jsonl"
  $taskWorkerListing='import json,pathlib;p=pathlib.Path("/tmp/{0}");print("\n".join(json.loads(p.open().readline())["worker_files"]))' -f $taskName
  $taskWorkerNames=& $KubectlHome -n coder exec $ClientPod '--' python3 -c $taskWorkerListing
  if($LASTEXITCODE -ne 0){throw "Actual worker list read failed"}
  foreach($taskWorkerName in $taskWorkerNames){
   Receive-ClientFile $taskWorkerName "$taskDirectory/$taskWorkerName"
  }
  $taskCode=@"
from pathlib import Path
import gzip,json,shutil
d=Path('$taskDirectory');out=Path('/workspaces/repository/bench/results/official_sustained_20261016')/('$taskStage')
out.mkdir(exist_ok=True)
terminal=json.loads(Path('$taskPrefix.server_terminal.json').read_text());assert terminal['exit']==0 and not terminal['pins']
count=0
for p in d.glob('$taskTag.*'):
 if not p.is_file():continue
 dest=out/(p.name+'.gz' if p.suffix=='.jsonl' else p.name)
 assert not dest.exists(),dest
 if p.suffix=='.jsonl':
  dest.write_bytes(gzip.compress(p.read_bytes()));assert gzip.decompress(dest.read_bytes())==p.read_bytes()
 else:shutil.copyfile(p,dest)
 count+=1
for p in d.glob('$taskTag'+'_r*'):
 if not p.is_file():continue
 dest=out/(p.name+'.gz' if p.suffix=='.jsonl' else p.name)
 assert not dest.exists(),dest
 if p.suffix=='.jsonl':
  dest.write_bytes(gzip.compress(p.read_bytes()));assert gzip.decompress(dest.read_bytes())==p.read_bytes()
 else:shutil.copyfile(p,dest)
 count+=1
print('archived',count,'files after server stop')
"@
  Invoke-Workspace $taskCode
  Write-Output "PASS $taskStage pair=$taskPair condition=$taskCondition" 
 }
}
Write-Output "DIAGNOSTIC terminal; no server performance ranking"
