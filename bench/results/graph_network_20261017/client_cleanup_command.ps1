$ErrorActionPreference="Stop"
$taskRaw=& .\scripts\kubectl-home.ps1 -n coder get job/bpfusion-sustained-client-20261016 pod/bpfusion-sustained-client-20261016-4h2br -o json
if($LASTEXITCODE -ne 0){throw "Cleanup identity read failed"}
$taskObjects=(($taskRaw -join [Environment]::NewLine)|ConvertFrom-Json).items
$taskJob=@($taskObjects|Where-Object kind -eq Job)[0]
$taskPod=@($taskObjects|Where-Object kind -eq Pod)[0]
if($taskJob.metadata.uid -ne "279160d8-b0b7-46d8-b89a-82a67ec3ace7" -or $taskPod.metadata.uid -ne "9dce0ac1-a881-471b-9103-e9938a551369" -or $taskPod.metadata.ownerReferences.uid -ne $taskJob.metadata.uid){throw "Cleanup UID/owner mismatch"}
$taskCode='from pathlib import Path;import json;p=Path("/tmp/official_remote_key");assert not p.is_symlink();v=p.exists();p.unlink(missing_ok=True);print(json.dumps({"ephemeral_test_key_existed":v,"removed":not p.exists()}))'
$taskClientKey=& .\scripts\kubectl-home.ps1 -n coder exec bpfusion-sustained-client-20261016-4h2br '--' python3 -c $taskCode
if($LASTEXITCODE -ne 0){throw "Client ephemeral-key cleanup failed"}
$taskBody=@{apiVersion="v1";kind="DeleteOptions";propagationPolicy="Foreground";preconditions=@{uid=$taskJob.metadata.uid}}|ConvertTo-Json -Compress
$taskDeleted=$taskBody| & .\scripts\kubectl-home.ps1 delete --raw "/apis/batch/v1/namespaces/coder/jobs/bpfusion-sustained-client-20261016" -f -
if($LASTEXITCODE -ne 0){throw "UID-preconditioned benchmark Job deletion failed"}
$taskResponse=(($taskDeleted -join [Environment]::NewLine)|ConvertFrom-Json)
$taskReceipt=@{utc=[DateTime]::UtcNow.ToString("o");job_uid=$taskJob.metadata.uid;pod_uid=$taskPod.metadata.uid;owner_verified=$true;pod_restarts=$taskPod.status.containerStatuses.restartCount;pod_node=$taskPod.spec.nodeName;delete_options=($taskBody|ConvertFrom-Json);response_kind=$taskResponse.kind;response_uid=$taskResponse.metadata.uid;response_status=$taskResponse.status;client_ephemeral_key=(($taskClientKey -join [Environment]::NewLine)|ConvertFrom-Json)}|ConvertTo-Json -Depth 8 -Compress
$taskSink=@"
from pathlib import Path
Path("/workspaces/repository/bench/results/graph_network_20261017/client_cleanup_request.json").write_text('''$taskReceipt''')
print("UID-preconditioned cleanup receipt saved")
"@
$taskSink| & .\scripts\kubectl-home.ps1 -n coder exec -i coder-eb48d962-76f4-4ff7-bac5-7bc62ec2ada3-5c8bb655f6-khnns '--' python3 -
if($LASTEXITCODE -ne 0){throw "Cleanup receipt archival failed"}
& .\scripts\kubectl-home.ps1 -n coder wait --for=delete job/bpfusion-sustained-client-20261016 pod/bpfusion-sustained-client-20261016-4h2br --timeout=55s
if($LASTEXITCODE -ne 0){throw "Actual client absence not yet verified"}
Write-Output "Original benchmark Job and Pod deletion observed"
