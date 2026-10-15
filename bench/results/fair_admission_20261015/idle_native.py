import pathlib,subprocess,json,os,signal,time,datetime,re
t=pathlib.Path(__file__).resolve().parent;r=pathlib.Path("/workspaces/repository")
model=json.loads((t/"models.json").read_text())["qwen"]
for case in ("deadline","helper_idle"):
    prefix=t/("idle_native_"+case)
    command=["strace","-D","-f","-ttt","-e","trace=epoll_pwait2,eventfd2,write,read,epoll_ctl","-o",str(prefix)+".strace",
             str(t/"build/vllm_graph_user_network_wait_trace"),model,"2" if case=="deadline" else "300",
             "--trace-output",str(prefix)+".gpu.jsonl","--trace-requests","1"]
    with pathlib.Path(str(prefix)+".stdout").open("x") as out:
        p=subprocess.Popen(command,cwd=r,stdout=out,stderr=subprocess.STDOUT)
        while "resident vLLM ready" not in pathlib.Path(str(prefix)+".stdout").read_text():
            if p.poll() is not None:raise RuntimeError(pathlib.Path(str(prefix)+".stdout").read_text())
            time.sleep(.1)
        ready=time.monotonic_ns()
        evidence=dict(case=case,pid=p.pid,command=command,ready_ns=ready,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
        if case=="helper_idle":
            time.sleep(1)
            tasks=[int(q.name) for q in pathlib.Path(f"/proc/{p.pid}/task").iterdir() if int(q.name)!=p.pid]
            assert tasks
            import ctypes
            evidence["signal_ns"]=time.monotonic_ns();evidence["helper_tid"]=tasks[0]
            evidence["tgkill_result"]=ctypes.CDLL(None).tgkill(p.pid,tasks[0],signal.SIGTERM);assert evidence["tgkill_result"]==0
        try:evidence["exit"]=p.wait(timeout=15)
        except subprocess.TimeoutExpired:
            evidence["failed_observation_ns"]=time.monotonic_ns()
            pathlib.Path(str(prefix)+".failure.json").write_text(json.dumps(evidence,indent=2))
            p.terminate();p.wait();raise
    evidence["end_ns"]=time.monotonic_ns()
    log=pathlib.Path(str(prefix)+".stdout").read_text()
    assert evidence["exit"]==0 and "graph_error=0" in log
    assert "published=0 completed=0 rejected=0" in log
    trace=pathlib.Path(str(prefix)+".strace").read_text()
    assert "eventfd2(" in trace and "epoll_pwait2(" in trace
    events=[json.loads(s) for s in pathlib.Path(str(prefix)+".gpu.jsonl").open()]
    assert len(events)==1 and events[0]["event"]=="terminal" and events[0]["overflows"]==0
    evidence["ready_to_python_exit_s"]=(evidence["end_ns"]-ready)/1e9
    evidence["scope"]="includes upstream replay/teardown; strace diagnostic, not production deadline/latency SLO"
    pathlib.Path(str(prefix)+".result.json").write_text(json.dumps(evidence,indent=2))
    print(json.dumps(evidence),flush=True)
