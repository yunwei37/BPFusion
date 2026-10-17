param([string]$CellScript,[string]$ClientPod="bpfusion-sustained-client-20261016-4h2br",
[string]$ServerIP="10.42.1.238",[string]$Build="/tmp/bpfusion-mixed-integration-n4cog5c6/graph_nodelay_build8")
$ErrorActionPreference="Stop";$taskStopped=@{}
foreach($taskRate in @(1000,4000,16000,64000,256000)){
 foreach($taskMode in @("native","kernel")){
  if($taskStopped.ContainsKey($taskMode)){continue}
  $taskTag="screen_cpp_recovered_fft_w1_c2_r"+$taskRate+"_"+$taskMode
  & $CellScript -ClientPod $ClientPod -ServerIP $ServerIP -Tag $taskTag -Operation fft -Mode $taskMode -Repeat 1 -Cores 2 -Rate $taskRate -Seconds 6 -Seed (21270017+$taskRate) -Stage screen -Build $Build
  if(-not $?){throw "Recovered cell execution failed; preserve original"}
  $taskCode='from pathlib import Path;print(Path("/workspaces/repository/bench/results/graph_network_20261017/screen/{0}.metrics.json").read_text())' -f $taskTag
  $taskReply=& .\scripts\kubectl-home.ps1 -n coder exec coder-eb48d962-76f4-4ff7-bac5-7bc62ec2ada3-5c8bb655f6-khnns '--' python3 -c $taskCode
  if($LASTEXITCODE -ne 0){throw "Read recovered metric failed"}
  $taskMetric=(($taskReply -join [Environment]::NewLine)|ConvertFrom-Json)
  if(-not $taskMetric.group_stable -or -not $taskMetric.service_affinity_verified){throw "Resource identity/mask failed"}
  $taskLimit=[Math]::Max(1,.1*$taskMetric.latency.scheduled_response_ms.p99)
  if($taskMetric.latency.timer_dispatch_lag_ms.p99 -gt $taskLimit){throw "CLIENT_LIMIT unchanged timing gate failed; preserve original"}
  if($taskMetric.failure_types.PSObject.Properties.Name -match "numeric"){throw "Numerical failure"}
  $taskGrowing=($null -ne $taskMetric.first_quarter_response_mean_ms) -and ($null -ne $taskMetric.last_quarter_response_mean_ms) -and ($taskMetric.last_quarter_response_mean_ms -gt ($taskMetric.first_quarter_response_mean_ms+100)) -and ($taskMetric.last_quarter_response_mean_ms -gt 2*$taskMetric.first_quarter_response_mean_ms)
  $taskSaturated=($taskMetric.throughput -lt .9*$taskRate) -or ($taskMetric.failure_fraction -gt .01) -or $taskGrowing
  Write-Output "SCREEN $taskTag saturated=$taskSaturated"
  if($taskSaturated){$taskStopped[$taskMode]=$true}
 }
 if($taskStopped.Count -eq 2){break}
}
Write-Output "TERMINAL graph_network_screen_recovered"
