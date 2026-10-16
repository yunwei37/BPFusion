from pathlib import Path
import json,time,subprocess,os
t=Path(__file__).resolve().parent
while not (t/"verified_reclaim_acceptance.exit.json").exists():time.sleep(.2)
assert json.loads((t/"verified_reclaim_acceptance.exit.json").read_text())["exit"]==0
assert not list(Path("/sys/fs/bpf").glob("bpfusion*"))
env=dict(os.environ,**json.loads((t/"environment.json").read_text()))
cmd=[str(t/"runtime/bin/python"),str(t/"verified_reclaim_collision_trace.py"),"loop","qwen","8","vllm"]
print("START verified collision",flush=True)
with (t/"verified_reclaim_collision_driver.stdout").open("x") as o,(t/"verified_reclaim_collision_driver.stderr").open("x") as e:z=subprocess.run(cmd,cwd="/workspaces/repository",env=env,stdout=o,stderr=e)
print("TERMINAL command exit",z.returncode,flush=True)
