param([Parameter(Mandatory=$true)][string]$ClientPod,[Parameter(Mandatory=$true)][string]$ServerIP,[string]$KubectlHome=".\scripts\kubectl-home.ps1")
$ErrorActionPreference="Stop"
$taskServerPod="coder-eb48d962-76f4-4ff7-bac5-7bc62ec2ada3-5c8bb655f6-khnns"
$taskTemp="/tmp/bpfusion-mixed-integration-n4cog5c6"
$taskStage="active_wait_profile"
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
  $taskChunk=[Math]::Min([long]262144,[long]$taskInfo[1]-$taskOffset)
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
Invoke-Workspace "from pathlib import Path;Path('$taskDirectory').mkdir(exist_ok=False)" | Out-Null
foreach($taskMode in @("kernel")) {
 $taskPrefix="$taskDirectory/$($taskStage)_p0_$taskMode"
 $taskCell="$($taskPrefix)_r192";$taskServerPid=$null;$taskObserverPid=$null;$taskPerfPid=$null
 Write-Output "START $taskStage $taskMode"
 try {
  $taskServerPid=[int](Invoke-Workspace @"
from pathlib import Path
import subprocess,json,time
t=Path('$taskTemp');prefix=Path('$taskPrefix')
with Path(str(prefix)+'.wrapper.stdout').open('x') as o,Path(str(prefix)+'.wrapper.stderr').open('x') as e:
 p=subprocess.Popen(['/usr/bin/python3',str(t/'active_wait_server.py'),'--prefix',str(prefix),'--bind','$ServerIP','--build',str(t/'active_wait_sourcebuild16'),'--pair','0','--mode','$taskMode'],stdout=o,stderr=e,start_new_session=True)
while True:
 terminal=Path(str(prefix)+'.server_terminal.json')
 assert not terminal.exists(),terminal.read_text() if terminal.exists() else ''
 log=Path(str(prefix)+'.server.stdout')
 if log.exists() and 'resident vLLM ready:' in log.read_text():break
 time.sleep(.1)
print(json.loads(Path(str(prefix)+'.server_started.json').read_text())['pid'])
"@)
  $taskWarm="$($taskStage)_p0_$taskMode.warmup.jsonl"
  & $KubectlHome -n coder exec $ClientPod '--' python3 /tmp/remote_async_client.py --host $ServerIP --config /tmp/qwen_frozen.json --offsets /tmp/remote_offsets.json --output "/tmp/$taskWarm" --pair 0 --mode $taskMode --rate 192 --warmup
  if($LASTEXITCODE -ne 0){throw "Actual warmup failed"}
  $taskObserverPid=Start-Observer $taskCell $taskServerPid
  $taskPerfPid=[int](Invoke-Workspace @"
from pathlib import Path
import subprocess,json,time
t=Path('$taskTemp');prefix=Path('$taskCell')
with Path(str(prefix)+'.perf_wrapper.stdout').open('x') as o,Path(str(prefix)+'.perf_wrapper.stderr').open('x') as e:
 p=subprocess.Popen(['/usr/bin/python3',str(t/'cpu_profile_record.py'),'--prefix',str(prefix),'--pid','$taskServerPid'],stdout=o,stderr=e,start_new_session=True)
started=Path(str(prefix)+'.perf_started.json');terminal=Path(str(prefix)+'.perf_terminal.json')
while not started.exists():
 assert p.poll() is None;time.sleep(.01)
time.sleep(.25)
assert not terminal.exists(),terminal.read_text() if terminal.exists() else ''
record=json.loads(started.read_text());assert Path('/proc/'+str(record['pid'])).exists()
print(record['pid'])
"@)
  $taskName="$($taskStage)_p0_$($taskMode)_r192.client.jsonl"
  $taskOffsets="/tmp/remote_offsets.json"
  & $KubectlHome -n coder exec $ClientPod '--' python3 /tmp/remote_async_client.py --host $ServerIP --config /tmp/qwen_frozen.json --offsets $taskOffsets --output "/tmp/$taskName" --pair 0 --mode $taskMode --rate 192
  $taskExit=$LASTEXITCODE
  Invoke-Workspace "from pathlib import Path;import json;Path('$taskCell.client_exit.json').write_text(json.dumps(dict(exit=$taskExit)))" | Out-Null
  if($taskExit -ne 0){throw "Client process failed; preserve all data"}
 } finally {
  if($taskPerfPid) {
   Invoke-Workspace @"
from pathlib import Path
import os,signal,time,json
p=Path('$taskCell.perf_terminal.json')
if not p.exists():os.kill($taskPerfPid,signal.SIGINT)
while not p.exists():time.sleep(.05)
print(p.read_text())
"@ | Write-Output
   $taskPerfPid=$null
  }
  if($taskObserverPid){Stop-Observer $taskObserverPid $taskCell;$taskObserverPid=$null}
  if($taskServerPid) {
   Invoke-Workspace @"
from pathlib import Path
import os,signal,time,json
p=Path('$taskPrefix.server_terminal.json')
if not p.exists():os.killpg($taskServerPid,signal.SIGTERM)
while not p.exists():time.sleep(.05)
print(p.read_text()[-1500:])
"@ | Write-Output
  }
 }
 Receive-ClientFile $taskWarm "$taskPrefix.warmup.jsonl"
 Receive-ClientFile $taskName "$taskCell.client.jsonl"
 Write-Output "CELL terminal $taskMode"
}
Invoke-Workspace "import subprocess;subprocess.run(['/usr/bin/python3','$taskTemp/active_wait_profile_archive.py','$taskDirectory'],check=True)" | Write-Output
Write-Output "TERMINAL $taskStage"
