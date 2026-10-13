import json,os,socket,subprocess,time,datetime,shutil
root=os.path.dirname(os.path.abspath(__file__))
cmd=[shutil.which("strace"),"-f","-ttt","-o",root+"/cycles.strace","-e",
     "trace=accept,accept4,recvfrom,recvmsg,sendto,sendmsg,io_uring_setup,io_uring_enter,io_uring_register,shutdown",
     root+"/probe","idle-recv"]
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
first=p.stdout.readline();assert first.startswith("PORT "),first
client=socket.create_connection(("127.0.0.1",int(first.split()[1])),timeout=10);client.settimeout(10)
ready=p.stdout.readline()
while ready and not ready.startswith("READY "):
    first+=ready;ready=p.stdout.readline()
ready_time_ns=time.time_ns();assert ready.startswith("READY "),first+ready
received=bytearray();cycles=[];client_error=None
try:
    for cycle in range(8):
        time.sleep(2.2)
        sent_ns=time.time_ns();client.sendall(bytes([77+cycle]))
        data=bytearray()
        while len(data)<4096:
            part=client.recv(4096-len(data))
            if not part:raise RuntimeError("early EOF")
            data.extend(part)
        expected=bytes((frame*17+i+77+cycle)%251 for frame in range(cycle*32,(cycle+1)*32) for i in range(128))
        cycles.append({"cycle":cycle,"request_byte":77+cycle,"sent_ns":sent_ns,"received_bytes":len(data),"exact":data==expected})
        received.extend(data)
    client.shutdown(socket.SHUT_WR)
    assert client.recv(1)==b"","extra response"
except Exception as error:client_error=repr(error)
client.close()
tail,err=p.communicate(timeout=20);stdout=first+ready+tail
stats=next((json.loads(l[7:]) for l in stdout.splitlines() if l.startswith("RESULT ")),None)
receive_line=next((l for l in stdout.splitlines() if l.startswith("RECEIVE ")),None)
result={"start":start,"end":datetime.datetime.now(datetime.timezone.utc).isoformat(),"cmd":cmd,
        "ready_time_ns":ready_time_ns,"exit":p.returncode,"stdout":stdout,"stderr":err,
        "client_error":client_error,"client_bytes":len(received),"client_hex":received.hex(),"cycles":cycles,"stats":stats}
result["pass"]=bool(stats and stats["status"]==0 and stats["bytes"]==32768 and stats["submitted"]==stats["completed"]
    and stats["cpu_wakes"]==0 and stats["sq_head"]==stats["sq_tail"] and stats["cq_head"]==stats["cq_tail"]
    and stats["dropped"]==stats["overflow"]==0 and len(cycles)==8 and all(c["exact"] for c in cycles)
    and client_error is None and p.returncode==0 and "CLEANUP " in stdout
    and receive_line=="RECEIVE completed=8 byte=84 flags_after_receive=0 idle_observed=8 gpu_recv_armed=8 eof=1")
open(root+"/results.json","w").write(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items() if k!="client_hex"}),flush=True)
print("DIAGNOSIS_COMPLETE",flush=True)
