import json,os,socket,subprocess,time,datetime,shutil
root=os.path.dirname(os.path.abspath(__file__))
expected=bytes((frame*17+i)%251 for frame in range(32) for i in range(128))
results=[]
for mode in ("idle-recv",):
    cmd=[shutil.which("strace"),"-f","-ttt","-o",root+"/"+mode+".strace",
         "-e","trace=accept,accept4,recvfrom,recvmsg,sendto,sendmsg,io_uring_setup,io_uring_enter,io_uring_register,shutdown",
         root+"/probe",mode]
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    first=p.stdout.readline()
    if not first.startswith("PORT "):
        tail,err=p.communicate(timeout=20)
        result={"mode":mode,"start":start,"cmd":cmd,"exit":p.returncode,"stdout":first+tail,"stderr":err}
        results.append(result);open(root+"/"+mode+".json","w").write(json.dumps(result,indent=2))
        raise RuntimeError(result)
    client=socket.create_connection(("127.0.0.1",int(first.split()[1])),timeout=10)
    client.settimeout(10)
    ready=p.stdout.readline()
    while ready and not ready.startswith("READY "):
        first+=ready;ready=p.stdout.readline()
    ready_time_ns=time.time_ns()
    if mode=="idle-recv":
        time.sleep(2.2);client.sendall(bytes([77]))
    received=bytearray();client_error=None
    try:
        while True:
            data=client.recv(8192)
            if not data:break
            received.extend(data)
    except Exception as error:client_error=repr(error)
    client.close()
    tail,err=p.communicate(timeout=20)
    stdout=first+ready+tail
    stats=next((json.loads(l[7:]) for l in stdout.splitlines() if l.startswith("RESULT ")),None)
    result={"mode":mode,"start":start,"end":datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "cmd":cmd,"ready_time_ns":ready_time_ns,"exit":p.returncode,"stdout":stdout,"stderr":err,"client_error":client_error,
            "client_bytes":len(received),"client_exact":received==expected,"client_hex":received.hex(),
            "stats":stats}
    if mode in ("hot","idle-wake","idle-recv"):
        result["expected_outcome"]=bool(stats and stats["status"]==0 and stats["bytes"]==4096
            and stats["completed"]==stats["submitted"] and stats["sq_head"]==stats["sq_tail"]
            and stats["cq_head"]==stats["cq_tail"] and stats["dropped"]==0 and stats["overflow"]==0
            and received==expected and client_error is None and p.returncode==0
            and "CLEANUP " in stdout and stats["cpu_wakes"]==(mode=="idle-wake"))
    else:
        result["expected_outcome"]=bool(stats and stats["status"]==1 and stats["submitted"]==1
            and stats["completed"]==0 and stats["flags_before"]&1 and stats["flags_after"]&1
            and stats["cpu_wakes"]==0 and p.returncode==0 and "CLEANUP " in stdout)
    result["receive_verified"]="RECEIVE completed=1 byte=77 flags_after_receive=0" in stdout
    results.append(result)
    open(root+"/"+mode+".json","w").write(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k not in ("cmd","client_hex")}),flush=True)
open(root+"/results.json","w").write(json.dumps(results,indent=2))
print("DIAGNOSIS_COMPLETE",flush=True)
