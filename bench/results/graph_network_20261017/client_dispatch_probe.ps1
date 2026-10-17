$ErrorActionPreference="Stop"
$taskProbe=@'
from pathlib import Path
import ctypes,os,time,json,struct,gzip,base64,statistics
lib=ctypes.CDLL(None,use_errno=True)
class Timespec(ctypes.Structure):_fields_=[("sec",ctypes.c_long),("nsec",ctypes.c_long)]
class Spec(ctypes.Structure):_fields_=[("interval",Timespec),("value",Timespec)]
def snap():
 return {k:Path(p).read_text() for k,p in {"cpu_max":"/sys/fs/cgroup/cpu.max","cpu_stat":"/sys/fs/cgroup/cpu.stat","host_cpu_pressure":"/proc/pressure/cpu","cgroup_cpu_pressure":"/sys/fs/cgroup/cpu.pressure","io_pressure":"/proc/pressure/io","loadavg":"/proc/loadavg"}.items()}
epoch=time.monotonic_ns()+1000000000;before=snap();pids=[]
for part in range(8):
 pid=os.fork()
 if pid==0:
  fd=lib.timerfd_create(1,0);assert fd>=0
  setting=Spec(Timespec(0,1000000),Timespec(epoch//1000000000,epoch%1000000000))
  assert lib.timerfd_settime(fd,1,ctypes.byref(setting),None)==0
  lags=[];next_tick=0;cpu=time.process_time_ns()
  while next_tick<6000:
   count=struct.unpack("<Q",os.read(fd,8))[0];stamp=time.monotonic_ns()
   for i in range(min(count,6000-next_tick)):lags.append(stamp-epoch-(next_tick+i)*1000000)
   next_tick+=count
  os.close(fd)
  Path("/tmp/bpfusion_dispatch_probe_20261017.worker%d.json"%part).write_text(json.dumps(dict(part=part,lag_ns=lags,cpu_ns=time.process_time_ns()-cpu)))
  os._exit(0)
 pids.append(pid)
assert all(os.waitpid(p,0)[1]==0 for p in pids)
workers=[json.loads(Path("/tmp/bpfusion_dispatch_probe_20261017.worker%d.json"%p).read_text()) for p in range(8)]
lags=sorted(x for w in workers for x in w["lag_ns"]);rank=(len(lags)-1)*.99;i=int(rank);p99=lags[i]+(rank-i)*(lags[i+1]-lags[i])
result=dict(epoch_ns=epoch,before=before,after=snap(),workers=workers,p99_ms=p99/1e6,max_ms=max(lags)/1e6,
 scope="Client-only 8-worker timerfd execution diagnostic, not network/server-capacity evidence; later snapshot cannot identify historical pause cause.")
print(base64.b64encode(gzip.compress(json.dumps(result).encode(),mtime=0)).decode())
'@
$taskProbeBytes=$taskProbe| & .\scripts\kubectl-home.ps1 -n coder exec -i bpfusion-sustained-client-20261016-4h2br '--' python3 -
if($LASTEXITCODE -ne 0){throw "Client execution diagnostic failed"}
$taskArchiveCode='from pathlib import Path;import base64,gzip,json;p=Path("/workspaces/repository/bench/results/graph_network_20261017/client_dispatch_probe.json.gz");p.write_bytes(base64.b64decode("' + ($taskProbeBytes -join "") + '"));v=json.loads(gzip.decompress(p.read_bytes()));print(json.dumps({k:v[k] for k in ["p99_ms","max_ms","scope"]}))'
& .\scripts\kubectl-home.ps1 -n coder exec coder-eb48d962-76f4-4ff7-bac5-7bc62ec2ada3-5c8bb655f6-khnns '--' python3 -c $taskArchiveCode
if($LASTEXITCODE -ne 0){throw "Probe archival failed"}
