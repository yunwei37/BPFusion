$ErrorActionPreference="Stop"
$taskReceipt=Get-Content -Raw -LiteralPath (Join-Path $env:TEMP "bpfusion_client_cleanup_recovered_20261017.json")|ConvertFrom-Json
$taskAbsent=& .\scripts\kubectl-home.ps1 -n coder get job/bpfusion-sustained-client-20261016 pod/bpfusion-sustained-client-20261016-4h2br --ignore-not-found -o name
if($LASTEXITCODE -ne 0 -or (($taskAbsent -join "").Trim())){throw "Client Job/Pod absence check failed"}
$taskNode=(& .\scripts\kubectl-home.ps1 get node lab -o json)|ConvertFrom-Json
if($LASTEXITCODE -ne 0){throw "Node state read failed"}
$taskPod=(& .\scripts\kubectl-home.ps1 -n coder get pod coder-eb48d962-76f4-4ff7-bac5-7bc62ec2ada3-5c8bb655f6-khnns -o json)|ConvertFrom-Json
if($LASTEXITCODE -ne 0){throw "Original Workspace state read failed"}
$taskLease=(& .\scripts\kubectl-home.ps1 -n kube-node-lease get lease lab -o json)|ConvertFrom-Json
if($LASTEXITCODE -ne 0){throw "Lease read failed"}
$taskVolume=(& .\scripts\kubectl-home.ps1 -n longhorn-system get volumes.longhorn.io pvc-5d1b0ce5-fbee-43ef-93f1-d433037bb5e4 -o json)|ConvertFrom-Json
if($LASTEXITCODE -ne 0){throw "Original volume state read failed"}
$taskState=@{observed_utc=[DateTime]::UtcNow.ToString("o");client_job_and_pod_absent=$true;client_cleanup=$taskReceipt;node_ready=@($taskNode.status.conditions|Where-Object type -eq Ready)[0].status;lease=$taskLease.spec.renewTime;workspace_uid=$taskPod.metadata.uid;workspace_restarts=$taskPod.status.containerStatuses.restartCount;pvc_state=$taskVolume.status.state;pvc_robustness=$taskVolume.status.robustness;pvc_node=$taskVolume.status.currentNodeID}|ConvertTo-Json -Depth 8 -Compress
$taskPy=@"
from pathlib import Path
import json,subprocess,os,datetime
r=Path("/workspaces/repository");a=r/"bench/results/graph_network_20261017";t=Path("/tmp/bpfusion-mixed-integration-n4cog5c6")
assert subprocess.check_output(["git","symbolic-ref","--short","HEAD"],cwd=r,text=True).strip()=="main"
v=json.loads(r'''$taskState''')
assert v["workspace_uid"]=="3e8994f8-77ba-4a73-a3a5-35ed69a0a8a2" and v["workspace_restarts"]==0
assert v["node_ready"]=="True" and (v["pvc_state"],v["pvc_robustness"],v["pvc_node"])==("attached","healthy","lab")
v["original_process_start_ticks"]={str(p):Path("/proc/%d/stat"%p).read_text().rsplit(") ",1)[1].split()[19] for p in [1,10909]}
assert v["original_process_start_ticks"]=={"1":"8626595","10909":"8662925"}
v["gpu_compute_apps"]=subprocess.check_output(["nvidia-smi","--query-compute-apps=pid","--format=csv,noheader"],text=True).strip()
v["owned_bpf_pins"]=[str(p) for p in Path("/sys/fs/bpf").glob("bpfusion*")]
assert not v["gpu_compute_apps"] and not v["owned_bpf_pins"]
targets={str(r/"bench/resource_observer.py"),str(r/"examples/torch_graph_server.py"),str(a/"graph_network_server.py")}
active=[]
for p in Path("/proc").glob("[0-9]*/cmdline"):
 try:
  argv=p.read_bytes().decode(errors="replace").split(chr(0))
  if any(x in targets for x in argv[1:]):active.append(int(p.parent.name))
 except OSError:pass
v["remaining_benchmark_server_or_observer_pids"]=active;assert not active
v["legacy_module_loaded"]=Path("/sys/module/bfusion_tx").exists()
v["ephemeral_server_test_key_removed"]=not (t/"official_remote_key").exists()
assert v["ephemeral_server_test_key_removed"]
v["foreign_wip_preserved"]=subprocess.check_output(["git","status","--short","--","tools/setup_env.sh"],cwd=r,text=True).strip()=="?? tools/setup_env.sh"
assert v["foreign_wip_preserved"]
v["source_branch"]="main"
v["post_measurement_node_event"]="Repeated control/node/storage interruption after all 30 measured cells completed; existing infrastructure owner handled recovery. This thread sent no power/ATX action, changed no Workspace/host/credential configuration and retained the original Pod/PVC/PIDs."
v["no_new_gpu_measurement_after_recovery"]=True
v["actual_measurement_end_utc"]=max(json.loads(p.read_text())["end_utc"] for p in (a/"confirmation").glob("*.client_exit.json"))
v["retained_private_runtime_scope"]="Original private build/analysis cache retained for same-Workspace reproduction; not an active server or new persistent service."
(a/"cleanup.json").write_text(json.dumps(v,indent=2))
(a/"client_cleanup_recovered.json").write_text(json.dumps(v["client_cleanup"],indent=2))
print(json.dumps({k:v[k] for k in ["client_job_and_pod_absent","workspace_uid","workspace_restarts","pvc_robustness","original_process_start_ticks","ephemeral_server_test_key_removed","actual_measurement_end_utc"]}))
"@
$taskPy| & .\scripts\kubectl-home.ps1 -n coder exec -i coder-eb48d962-76f4-4ff7-bac5-7bc62ec2ada3-5c8bb655f6-khnns '--' python3 -
if($LASTEXITCODE -ne 0){throw "Final cleanup evidence failed"}
