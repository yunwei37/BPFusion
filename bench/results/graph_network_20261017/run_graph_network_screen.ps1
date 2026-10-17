param([string]$ClientPod="bpfusion-sustained-client-20261016-4h2br",[string]$ServerIP="10.42.1.238",
[string]$CellScript,[string]$Build="/tmp/bpfusion-mixed-integration-n4cog5c6/graph_nodelay_build8",[string]$KubectlHome=".\scripts\kubectl-home.ps1")
$ErrorActionPreference="Stop"
function Read-Metric([string]$Tag) {
 $taskQuery='import pathlib;p=pathlib.Path("/workspaces/repository/bench/results/graph_network_20261017/screen/{0}.metrics.json");print(p.read_text() if p.exists() else "null")' -f $Tag
 $taskReply=& $KubectlHome -n coder exec coder-eb48d962-76f4-4ff7-bac5-7bc62ec2ada3-5c8bb655f6-khnns '--' python3 -c $taskQuery
 if($LASTEXITCODE -ne 0){throw "Read completed metric failed"}
 return (($taskReply -join [Environment]::NewLine)|ConvertFrom-Json)
}
$taskCases=@()
foreach($taskOp in @("matmul","fft")){
 foreach($taskRep in @(1,16,256)){$taskCases+=@{operation=$taskOp;repeat=$taskRep;cores=0}}
 foreach($taskCore in @(1,2)){$taskCases+=@{operation=$taskOp;repeat=1;cores=$taskCore}}
}
$taskIndex=0
foreach($taskCase in $taskCases){
 $taskOrder=if(($taskIndex % 2) -eq 0){@("kernel","native")}else{@("native","kernel")}
 $taskStopped=@{}
 foreach($taskRate in @(1000,4000,16000,64000,256000)){
  foreach($taskMode in $taskOrder){
   if($taskStopped.ContainsKey($taskMode)){continue}
   $taskTag="screen_nodelay_"+$taskCase.operation+"_w"+$taskCase.repeat+"_c"+$taskCase.cores+"_r"+$taskRate+"_"+$taskMode
   $taskSeed=20261017+$taskIndex*1000+$taskRate
   $taskMetric=Read-Metric $taskTag
   if($null -eq $taskMetric){
    & $CellScript -ClientPod $ClientPod -ServerIP $ServerIP -Tag $taskTag -Operation $taskCase.operation -Mode $taskMode -Repeat $taskCase.repeat -Cores $taskCase.cores -Rate $taskRate -Seconds 6 -Seed $taskSeed -Stage screen -Build $Build -KubectlHome $KubectlHome
    if(-not $?){throw "Cell driver failed"}
    $taskMetric=Read-Metric $taskTag
   } else {Write-Output "RETAIN $taskTag"}
   if($taskMetric.failure_types.PSObject.Properties.Name -match "numeric"){throw "Numerical failure; retain original and repair before continuing"}
   if(-not $taskMetric.group_stable){throw "Unstable process group; inspect before continuing"}
   $taskTail=$taskMetric.latency.scheduled_response_ms
   $taskLimit=if($null -eq $taskTail){1}else{[Math]::Max(1,.1*$taskTail.p99)}
   if($taskMetric.latency.timer_dispatch_lag_ms.p99 -gt $taskLimit){throw "CLIENT_LIMIT timing gate failed; retain prefix and diagnose before ranking server capacity"}
   if(($taskCase.cores -gt 0) -and (-not $taskMetric.service_affinity_verified)){throw "Service affinity escaped; inspect before claiming core pressure"}
   $taskGrowing=($null -ne $taskMetric.first_quarter_response_mean_ms) -and ($null -ne $taskMetric.last_quarter_response_mean_ms) -and ($taskMetric.last_quarter_response_mean_ms -gt ($taskMetric.first_quarter_response_mean_ms+100)) -and ($taskMetric.last_quarter_response_mean_ms -gt (2*$taskMetric.first_quarter_response_mean_ms))
   $taskSaturated=($taskMetric.throughput -lt (.9*$taskRate)) -or ($taskMetric.failure_fraction -gt .01) -or $taskGrowing
   Write-Output "SCREEN $taskTag saturated=$taskSaturated"
   if($taskSaturated){$taskStopped[$taskMode]=$true}
  }
  if($taskStopped.Count -eq 2){break}
 }
 $taskIndex++
}
Write-Output "TERMINAL graph_network_screen"
