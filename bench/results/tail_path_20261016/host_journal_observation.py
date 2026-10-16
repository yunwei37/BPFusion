from pathlib import Path
import json,subprocess,datetime,time
begin=time.monotonic_ns()
cmd=['journalctl','-k','--since','2026-10-16 08:21:00 UTC','--no-pager','-o','short-iso']
z=subprocess.run(cmd,capture_output=True,text=True)
selected=[line for line in z.stdout.splitlines() if any(w in line.lower() for w in ['nvrm','xid','gpu','iommu','io_page_fault'])]
g=subprocess.run(['nvidia-smi','--query-gpu=name,driver_version,power.limit,clocks.sm,temperature.gpu','--format=csv,noheader'],capture_output=True,text=True)
a=subprocess.run(['nvidia-smi','--query-compute-apps=pid,process_name,used_gpu_memory','--format=csv,noheader'],capture_output=True,text=True)
print(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),begin_ns=begin,end_ns=time.monotonic_ns(),boot_id=Path('/proc/sys/kernel/random/boot_id').read_text().strip(),kernel_journal=dict(command=cmd,exit=z.returncode,stderr=z.stderr,selected=selected,all_line_count=len(z.stdout.splitlines())),gpu=dict(exit=g.returncode,stdout=g.stdout,stderr=g.stderr),apps=dict(exit=a.returncode,stdout=a.stdout,stderr=a.stderr),scope='Bounded kernel journal read and endpoint GPU snapshot; not continuous exclusive ownership.')))
