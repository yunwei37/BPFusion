import pathlib,subprocess,json,os,sys,datetime
t=pathlib.Path(__file__).resolve().parent;r=pathlib.Path("/workspaces/repository")
env=dict(os.environ,**json.loads((t/"environment.json").read_text()));env.pop("VLLM_BATCH_INVARIANT",None)
env["PYTHONPATH"]="/workspaces/repository/executor"+(":"+env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
py=str(t/"runtime/bin/python");models=json.loads((t/"models.json").read_text())
commands=[("module_compat",[py,str(t/"module_compat.py")]),("idle_native",["/usr/bin/python3",str(t/"idle_native.py")])]
for model in ("qwen","smol"):
    commands.append(("protocol_"+model,[py,str(t/"load.py"),"--model",models[model],"--correctness","--output",str(t/("protocol_"+model+".jsonl"))]))
    commands.append(("protocol_compat_"+model,[py,str(t/"load.py"),"--model",models[model],"--uring","--correctness","--output",str(t/("protocol_compat_"+model+".jsonl"))]))
    for condition in ("loop","native"):
        commands.append(("lifecycle_"+model+"_"+condition,[py,str(t/"lifecycle.py"),condition,model]))
(t/"qualification.commands.json").write_text(json.dumps(commands,indent=2));results=[]
for name,cmd in commands:
    print("START",name,flush=True)
    with (t/(name+".driver.stdout")).open("x") as out,(t/(name+".driver.stderr")).open("x") as err:
        z=subprocess.run(cmd,cwd=r,env=env,stdout=out,stderr=err)
    result=dict(name=name,command=cmd,exit=z.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    if name.startswith("protocol_") and z.returncode==0:
        cmd=["/usr/bin/python3",str(t/"protocol_analysis.py"),str(t/(name+".jsonl"))]
        with (t/(name+".analysis.stdout")).open("x") as out,(t/(name+".analysis.stderr")).open("x") as err:
            a=subprocess.run(cmd,cwd=r,stdout=out,stderr=err)
        result.update(analysis_exit=a.returncode,analysis_command=cmd)
    if name.startswith("lifecycle_"):
        _,model,condition=name.split("_")
        p=t/name/(model+".results.json")
        result["lifecycle_pass"]=p.exists() and json.loads(p.read_text()).get("pass") is True
    results.append(result);(t/"qualification.statuses.json").write_text(json.dumps(results,indent=2))
    print("TERMINAL",json.dumps(result),flush=True)
    if z.returncode or result.get("analysis_exit",0) or result.get("lifecycle_pass") is False:break
ok=len(results)==len(commands) and all(x["exit"]==0 and x.get("analysis_exit",0)==0 and x.get("lifecycle_pass",True) for x in results)
(t/"qualification.exit.json").write_text(json.dumps(dict(exit=0 if ok else 1,completed=len(results),expected=len(commands),utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
raise SystemExit(0 if ok else 1)
