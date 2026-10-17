$ErrorActionPreference="Stop"
$taskClient=@'
from pathlib import Path
import json,tarfile,io,base64
root=Path("/tmp");name="confirm_s2_p1_native.warmup.jsonl";p=root/name
m=json.loads(p.open().readline());assert m["recorded"]==32 and m["failures"]==0 and m["worker_exit"]==[0]*8
assert not (root/"confirm_s2_p1_native.client.jsonl").exists()
names=list(dict.fromkeys([name]+m["input_files"]+m["worker_files"]))
assert all(Path(n).name==n and n.startswith(name) for n in names)
b=io.BytesIO()
with tarfile.open(fileobj=b,mode="w:gz") as tar:
 for n in names:tar.add(root/n,arcname=n,recursive=False)
data=b.getvalue();(root/"bpfusion_control_connection_warm_20261017.tgz").write_bytes(data)
print(base64.b64encode(data).decode())
'@
$taskData=$taskClient | & .\scripts\kubectl-home.ps1 -n coder exec -i bpfusion-sustained-client-20261016-4h2br '--' python3 -
if($LASTEXITCODE -ne 0){throw "Warm-only recovery source failed"}
$taskSink=@"
from pathlib import Path
import json,tarfile,io,gzip,base64,shutil,subprocess,datetime
r=Path("/workspaces/repository");a=r/"bench/results/graph_network_20261017";d=a/"control_connection_interruption"
assert subprocess.check_output(["git","symbolic-ref","--short","HEAD"],cwd=r,text=True).strip()=="main"
d.mkdir(exist_ok=False)
blob=base64.b64decode("$($taskData -join '')");(d/"original_warm_bundle.tgz").write_bytes(blob);manifest=[]
with tarfile.open(fileobj=io.BytesIO(blob),mode="r:gz") as tar:
 for member in tar:
  assert member.isfile() and Path(member.name).name==member.name
  raw=tar.extractfile(member).read();assert len(raw)==member.size
  compressed=member.name.endswith((".jsonl",".bin"))
  dest=d/(member.name+".gz" if compressed else member.name)
  dest.write_bytes(gzip.compress(raw,mtime=0) if compressed else raw)
  assert (gzip.decompress(dest.read_bytes()) if compressed else dest.read_bytes())==raw
  manifest.append(dict(file=dest.name,bytes=len(raw)))
source=Path("/tmp/bpfusion-mixed-integration-n4cog5c6/graph_network_confirmation");tag="confirm_s2_p1_native"
assert not (source/(tag+".resources.jsonl")).exists()
assert not (source/(tag+".client_exit.json")).exists()
for p in source.glob(tag+".*"):
 assert p.is_file() and p.resolve().is_relative_to(source.resolve())
 raw=p.read_bytes();compressed=p.suffix==".jsonl";dest=d/(p.name+".gz" if compressed else p.name)
 assert not dest.exists()
 dest.write_bytes(gzip.compress(raw,mtime=0) if compressed else raw)
 assert (gzip.decompress(dest.read_bytes()) if compressed else dest.read_bytes())==raw
 manifest.append(dict(file=dest.name,bytes=len(raw)));p.unlink()
(d/"recovery_manifest.json").write_text(json.dumps(dict(files=manifest,
 event="Control-plane exec timeout/502 while stopping the premeasurement idle observer. No main client file or main resource window existed; no measured request was started.",
 retained_warmups=32,measured_attempts=0,server_exit=0,remaining_gpu_contexts=0,
 original_PIDs={"1":"8626595","10909":"8662925"},
 continuation="Resume the same previously unmeasured cell with the original tag/seed/criteria after retaining all warm-only files. This is not repetition or replacement of measured confirmation data.",
 node_state="Original Pod0restarts,Ready,freshLease,existingWorkspace exec works; real host SSH verifies lab,k3s-agent/tailscaled active. No reboot or runtime configuration change.",
 utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
print(json.dumps(dict(recovered_files=len(manifest),warmups=32,measured_attempts=0)))
"@
$taskSink | & .\scripts\kubectl-home.ps1 -n coder exec -i coder-eb48d962-76f4-4ff7-bac5-7bc62ec2ada3-5c8bb655f6-khnns '--' python3 -
if($LASTEXITCODE -ne 0){throw "Warm-only preservation failed"}
$taskRetire=@'
from pathlib import Path
import json
root=Path("/tmp");name="confirm_s2_p1_native.warmup.jsonl";m=json.loads((root/name).open().readline())
d=root/"bpfusion_control_connection_interruption_20261017";d.mkdir(exist_ok=False)
for n in list(dict.fromkeys([name]+m["input_files"]+m["worker_files"])):
 p=root/n;assert p.name==n and n.startswith(name);p.rename(d/n)
print("original warm-only client files retained under a separate prefix")
'@
$taskRetire | & .\scripts\kubectl-home.ps1 -n coder exec -i bpfusion-sustained-client-20261016-4h2br '--' python3 -
if($LASTEXITCODE -ne 0){throw "Original warm prefix retirement failed"}
