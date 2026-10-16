param([Parameter(Mandatory=$true)][string]$ClientPod,[Parameter(Mandatory=$true)][string]$ServerIP,[switch]$Preflight,[string]$KubectlHome=".\scripts\kubectl-home.ps1")
$ErrorActionPreference="Stop"
$taskServerPod="coder-eb48d962-76f4-4ff7-bac5-7bc62ec2ada3-5c8bb655f6-khnns"
$taskTemp="/tmp/bpfusion-mixed-integration-n4cog5c6"
$taskStage=if($Preflight){"preflight"}else{"full"}
$taskDirectory="$taskTemp/remote_$taskStage"
function Invoke-Workspace([string]$Code) {
 $taskAnswer=$Code | & $KubectlHome -n coder exec -i $taskServerPod '--' python3 -
 if($LASTEXITCODE -ne 0){throw "Workspace command failed"}
 return ($taskAnswer -join [Environment]::NewLine)
}
function Receive-ClientFile([string]$Name,[string]$Destination) {
 $taskCompress='import base64,gzip,pathlib;print(base64.b64encode(gzip.compress(pathlib.Path("/tmp/{0}").read_bytes())).decode())' -f $Name
 $taskPayload=& $KubectlHome -n coder exec $ClientPod '--' python3 -c $taskCompress
 if($LASTEXITCODE -ne 0){throw "Client data transfer failed"}
 $taskSink='import sys,base64,pathlib;pathlib.Path("{0}.gz").write_bytes(base64.b64decode(sys.stdin.buffer.read()))' -f $Destination
 $taskPayload | & $KubectlHome -n coder exec -i $taskServerPod '--' python3 -c $taskSink
 if($LASTEXITCODE -ne 0){throw "Workspace data write failed"}
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
Invoke-Workspace "from pathlib import Path;Path('$taskDirectory').mkdir()" | Out-Null
$taskPairs=if($Preflight){@(0)}else{@(0,1,2,3,4)}
foreach($taskPair in $taskPairs) {
 $taskModes=if($taskPair%2 -eq 0){@("kernel","native")}else{@("native","kernel")}
 foreach($taskMode in $taskModes) {
  $taskTag=$taskStage+"_p"+$taskPair+"_"+$taskMode
  $taskPrefix=$taskDirectory+"/"+$taskTag
  $taskServerPid=$null;$taskObserverPid=$null
  Write-Output "START $taskStage pair=$taskPair mode=$taskMode"
  try {
   $taskCode=@"
from pathlib import Path
import subprocess,json,time
t=Path('$taskTemp');prefix=Path('$taskPrefix')
with Path(str(prefix)+'.wrapper.stdout').open('x') as o,Path(str(prefix)+'.wrapper.stderr').open('x') as e:
 p=subprocess.Popen(['/usr/bin/python3',str(t/'remote_server.py'),'--prefix',str(prefix),'--bind','$ServerIP','--build',str(t/'tcp_sourcebuild16'),'--pair','$taskPair','--mode','$taskMode'],stdout=o,stderr=e,start_new_session=True)
while True:
 log=Path(str(prefix)+'.server.stdout');terminal=Path(str(prefix)+'.server_terminal.json')
 assert not terminal.exists(),terminal.read_text() if terminal.exists() else ''
 if log.exists() and 'resident vLLM ready:' in log.read_text():break
 time.sleep(.1)
print(json.loads(Path(str(prefix)+'.server_started.json').read_text())['pid'])
"@
   $taskServerPid=[int](Invoke-Workspace $taskCode)
   $taskWarm=$taskTag+".warmup.jsonl"
   & $KubectlHome -n coder exec $ClientPod '--' python3 /tmp/remote_async_client.py --host $ServerIP --config /tmp/qwen_frozen.json --offsets /tmp/remote_offsets.json --output "/tmp/$taskWarm" --pair $taskPair --mode $taskMode --rate 96 --warmup
   if($LASTEXITCODE -ne 0){throw "Warmup failed"}
   Receive-ClientFile $taskWarm "$taskPrefix.warmup.jsonl"
   $taskCell="$taskPrefix.idle";$taskObserverPid=Start-Observer $taskCell $taskServerPid
   Start-Sleep -Seconds 5
   Stop-Observer $taskObserverPid $taskCell;$taskObserverPid=$null
   $taskRates=if($taskPair%2 -eq 0){@(96,192)}else{@(192,96)}
   foreach($taskRate in $taskRates) {
    $taskCell=$taskPrefix+"_r"+$taskRate
    $taskName=$taskTag+"_r"+$taskRate+".client.jsonl"
    $taskObserverPid=Start-Observer $taskCell $taskServerPid
    Write-Output "CELL pair=$taskPair mode=$taskMode rate=$taskRate begin"
    $taskClientArgs=@("python3","/tmp/remote_async_client.py","--host",$ServerIP,"--config","/tmp/qwen_frozen.json","--offsets","/tmp/remote_offsets.json","--output","/tmp/$taskName","--pair","$taskPair","--mode",$taskMode,"--rate","$taskRate")
    if($Preflight){$taskClientArgs+="--preflight"}
    $taskBegin=[DateTime]::UtcNow.ToString('o')
    $taskClientOutput=& $KubectlHome -n coder exec $ClientPod '--' @taskClientArgs 2>&1
    $taskClientExit=$LASTEXITCODE;$taskEnd=[DateTime]::UtcNow.ToString('o')
    Stop-Observer $taskObserverPid $taskCell;$taskObserverPid=$null
    $taskReceipt=@{command=$taskClientArgs;exit=$taskClientExit;stdout_stderr=($taskClientOutput -join [Environment]::NewLine);begin_utc=$taskBegin;end_utc=$taskEnd;clientPod=$ClientPod}
    $taskReceiptJSON=$taskReceipt|ConvertTo-Json -Depth 5 -Compress
    $taskSink='import sys,pathlib;pathlib.Path("{0}.client_exit.json").write_bytes(sys.stdin.buffer.read())' -f $taskCell
    $taskReceiptJSON | & $KubectlHome -n coder exec -i $taskServerPod '--' python3 -c $taskSink
    if($LASTEXITCODE -ne 0){throw "Receipt write failed"}
    Receive-ClientFile $taskName "$taskCell.client.jsonl"
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
  Write-Output "PASS $taskStage pair=$taskPair mode=$taskMode"
 }
}
$taskExtra=if($Preflight){",'--preflight'"}else{""}
$taskCode=@"
from pathlib import Path
import subprocess,json
t=Path('$taskTemp');d=Path('$taskDirectory')
cmd=['/usr/bin/python3',str(t/'remote_analysis.py'),str(d)$taskExtra]
with (d/'analysis.stdout').open('x') as o,(d/'analysis.stderr').open('x') as e:p=subprocess.run(cmd,stdout=o,stderr=e)
(d/'analysis_exit.json').write_text(json.dumps(dict(command=cmd,exit=p.returncode)))
assert p.returncode==0,(d/'analysis.stderr').read_text()
print('analysis terminal0')
"@
Invoke-Workspace $taskCode
Write-Output "TERMINAL $taskStage"
