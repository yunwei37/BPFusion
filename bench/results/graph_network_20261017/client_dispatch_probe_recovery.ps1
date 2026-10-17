$ErrorActionPreference="Stop"
$taskRecover=@'
from pathlib import Path
import json,gzip,base64,statistics
workers=[json.loads(Path("/tmp/bpfusion_dispatch_probe_20261017.worker%d.json"%p).read_text()) for p in range(8)]
lags=sorted(x for w in workers for x in w["lag_ns"]);rank=(len(lags)-1)*.99;i=int(rank);p99=lags[i]+(rank-i)*(lags[i+1]-lags[i])
result=dict(workers=workers,p99_ms=p99/1e6,max_ms=max(lags)/1e6,
 retained_raw_timer_samples=len(lags),original_absolute_epoch_unknown=True,
 original_before_after_stdout_not_archived="Windows ssh argv limit interrupted transfer after probe; original per-worker files recovered without rerunning.",
 later_environment={k:Path(p).read_text() for k,p in {"cpu_max":"/sys/fs/cgroup/cpu.max","cpu_stat":"/sys/fs/cgroup/cpu.stat","host_cpu_pressure":"/proc/pressure/cpu","cgroup_cpu_pressure":"/sys/fs/cgroup/cpu.pressure","io_pressure":"/proc/pressure/io","loadavg":"/proc/loadavg"}.items()},
 scope="Client-only 8-worker timerfd execution diagnostic, not network/server-capacity evidence. Later snapshot cannot identify historical pause.")
data=gzip.compress(json.dumps(result).encode(),mtime=0);Path("/tmp/bpfusion_dispatch_probe_20261017.json.gz").write_bytes(data)
print(base64.b64encode(data).decode())
'@
$taskResult=$taskRecover | & .\scripts\kubectl-home.ps1 -n coder exec -i bpfusion-sustained-client-20261016-4h2br '--' python3 -
if($LASTEXITCODE -ne 0){throw "Probe raw recovery failed"}
$taskSink=@"
from pathlib import Path
import base64,gzip,json
p=Path("/workspaces/repository/bench/results/graph_network_20261017/client_dispatch_probe.json.gz")
p.write_bytes(base64.b64decode("$($taskResult -join '')"))
v=json.loads(gzip.decompress(p.read_bytes()))
print(json.dumps({k:v[k] for k in ["p99_ms","max_ms","retained_raw_timer_samples"]}))
"@
$taskSink| & .\scripts\kubectl-home.ps1 -n coder exec -i coder-eb48d962-76f4-4ff7-bac5-7bc62ec2ada3-5c8bb655f6-khnns '--' python3 -
if($LASTEXITCODE -ne 0){throw "Probe archival failed"}
