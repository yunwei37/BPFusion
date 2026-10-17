param([string]$ClientPod="bpfusion-sustained-client-20261016-4h2br",[string]$ServerIP="10.42.1.238",
[string]$CellScript,[string]$Build="/tmp/bpfusion-mixed-integration-n4cog5c6/graph_nodelay_build8",
[string]$KubectlHome=".\scripts\kubectl-home.ps1")
$ErrorActionPreference="Stop"
$taskRoot="/workspaces/repository/bench/results/graph_network_20261017"
$taskQuery='import pathlib;print(pathlib.Path("/workspaces/repository/bench/results/graph_network_20261017/confirmation_selection.json").read_text())'
$taskAnswer=& $KubectlHome -n coder exec coder-eb48d962-76f4-4ff7-bac5-7bc62ec2ada3-5c8bb655f6-khnns '--' python3 -c $taskQuery
if($LASTEXITCODE -ne 0){throw "Frozen selection read failed"}
$taskSelection=(($taskAnswer -join [Environment]::NewLine)|ConvertFrom-Json).selected
function Read-Confirmation([string]$Tag){
 $taskCode='from pathlib import Path;p=Path("/workspaces/repository/bench/results/graph_network_20261017/confirmation/{0}.metrics.json");print(p.read_text() if p.exists() else "null")' -f $Tag
 $taskAnswer=& $KubectlHome -n coder exec coder-eb48d962-76f4-4ff7-bac5-7bc62ec2ada3-5c8bb655f6-khnns '--' python3 -c $taskCode
 if($LASTEXITCODE -ne 0){throw "Confirmation receipt read failed"}
 return (($taskAnswer -join [Environment]::NewLine)|ConvertFrom-Json)
}
for($taskIndex=0;$taskIndex -lt $taskSelection.Count;$taskIndex++){
 $taskCell=$taskSelection[$taskIndex]
 for($taskPair=0;$taskPair -lt 5;$taskPair++){
  $taskOrder=if((($taskPair+$taskIndex)%2) -eq 0){@("kernel","native")}else{@("native","kernel")}
  foreach($taskMode in $taskOrder){
   $taskTag="confirm_s"+$taskIndex+"_p"+$taskPair+"_"+$taskMode
   $taskMetric=Read-Confirmation $taskTag
   if($null -eq $taskMetric){
    & $CellScript -ClientPod $ClientPod -ServerIP $ServerIP -Tag $taskTag -Operation $taskCell.operation -Mode $taskMode -Repeat $taskCell.repeat -Cores $taskCell.cores -Rate $taskCell.rate -Seconds 20 -Seed (420261017+$taskIndex*100+$taskPair) -Stage confirmation -Build $Build -KubectlHome $KubectlHome
    if(-not $?){throw "Confirmation execution failed; retain the original"}
   }else{Write-Output "RETAIN $taskTag"}
  }
 }
}
Write-Output "TERMINAL graph_network_confirmation"
