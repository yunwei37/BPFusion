import pathlib,subprocess,json,os,datetime,sys
t=pathlib.Path(__file__).resolve().parent;r=pathlib.Path("/workspaces/repository")
env=dict(os.environ,**json.loads((t/"environment.json").read_text()));env.pop("VLLM_BATCH_INVARIANT",None)
models=json.loads((t/"models.json").read_text());py=str(t/"runtime/bin/python")
stage='full';names=['qwen', 'smol'];statuses=[]
for name in names:
    key=stage+"_"+name
    command=[py,str(t/"load.py"),"--model",models[name],"--output",str(t/(key+".jsonl"))]+[]
    print("START",key,flush=True)
    with (t/(key+".driver.stdout")).open("x") as out,(t/(key+".driver.stderr")).open("x") as err:
        z=subprocess.run(command,cwd=r,env=env,stdout=out,stderr=err)
    status=dict(name=key,command=command,exit=z.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    if z.returncode==0:
        analysis=["/usr/bin/python3",str(t/"analyze.py"),str(t/(key+".jsonl"))]
        with (t/(key+".analysis.stdout")).open("x") as out,(t/(key+".analysis.stderr")).open("x") as err:
            a=subprocess.run(analysis,cwd=r,stdout=out,stderr=err)
        status.update(analysis_command=analysis,analysis_exit=a.returncode)
    statuses.append(status);(t/(stage+".statuses.json")).write_text(json.dumps(statuses,indent=2))
    print("TERMINAL",json.dumps(status),flush=True)
    if z.returncode or status.get("analysis_exit",0):break
ok=len(statuses)==len(names) and all(s["exit"]==0 and s.get("analysis_exit",0)==0 for s in statuses)
(t/(stage+".exit.json")).write_text(json.dumps(dict(exit=0 if ok else 1,completed=len(statuses),expected=len(names),utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
sys.exit(0 if ok else 1)
