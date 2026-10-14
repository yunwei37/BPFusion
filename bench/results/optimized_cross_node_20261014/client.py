import os,socket,struct,time,json,threading,sys
from concurrent.futures import ThreadPoolExecutor
def request(client,ids,expected,gen=None):
    # A dynamic-batch backend validates against independent trajectory replay.
    if expected is not None: gen=len(expected)
    assert isinstance(gen,int) and gen>0
    client_ns=time.monotonic_ns()
    body=struct.pack("<IIIIQ",0x514c4d51,len(ids),gen,0,client_ns)+struct.pack(f"<{len(ids)}I",*ids)
    wire=f"POST /generate HTTP/1.1\r\nHost: localhost\r\nContent-Length: {len(body)}\r\n\r\n".encode()+body
    start=time.monotonic_ns()
    client.sendall(wire)
    header=b""; data=b""; arrivals=[]
    while len(data)<4*gen:
        chunk=client.recv(4096)
        arrived=time.monotonic_ns()
        assert chunk,"short reply"
        if header is not None:
            header+=chunk
            if b"\r\n\r\n" not in header: continue
            head,chunk=header.split(b"\r\n\r\n",1)
            assert head.startswith(b"HTTP/1.1 200 OK\r\n"),head
            assert f"Content-Length: {4*gen}".encode() in head,head
            header=None
        data+=chunk
        arrivals.extend([arrived]*((len(data)//4)-len(arrivals)))
    assert len(data)==4*gen,data
    actual=list(struct.unpack(f"<{gen}I",data))
    if expected is not None: assert actual==expected,(ids,actual,expected)
    return {"client_ns":client_ns,"start_ns":start,"arrival_ns":arrivals,"tokens":actual,
            "ttft_ms":(arrivals[0]-start)/1e6,
            "latency_ms":(arrivals[-1]-start)/1e6,
            "tpot_ms":(arrivals[-1]-arrivals[0])/(gen-1)/1e6 if gen>1 else None}

def connect():
    client=socket.create_connection((os.environ.get("BF_BIND","127.0.0.1"),39403),timeout=60)
    client.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)
    return client
def emit(event,**kw):
    print(json.dumps(dict(event=event,**BASE,**kw)),flush=True)
def check(row,ids,gen):
    key=(tuple(ids),gen)
    assert tuple(row["tokens"]) in POOL[key],(ids,gen,row["tokens"])
def run():
    emit("client_environment",python=sys.version,server=os.environ["BF_BIND"])
    with connect() as client:
        for i in range(8):
            ids=PROMPTS[i%4]
            row=request(client,ids,None,gen=1);check(row,ids,1)
            emit("request",kind="warmup",input_ids=ids,gen=1,case=i%4,**row)
    for gen,concurrency in MATRIX:
        rows=[];ready=threading.Barrier(concurrency+1);barrier=threading.Barrier(concurrency+1)
        def lane(i):
            with connect() as client:
                ready.wait(timeout=60);barrier.wait(timeout=60)
                for index in range(i,COUNT,concurrency):
                    ids=PROMPTS[index%4]
                    row=request(client,ids,None,gen=gen)
                    check(row,ids,gen)
                    rows.append(dict(row,index=index,case=index%4,input_ids=ids))
        try:
            with ThreadPoolExecutor(max_workers=concurrency) as pool:
                futures=[pool.submit(lane,i) for i in range(concurrency)]
                ready.wait(timeout=60);barrier.wait(timeout=60)
                for f in futures:f.result()
        finally:
            for row in sorted(rows,key=lambda x:x["index"]):
                emit("request",kind="measured",gen=gen,concurrency=concurrency,**row)
        first=min(r["start_ns"] for r in rows);last=max(r["arrival_ns"][-1] for r in rows)
        emit("cell",gen=gen,concurrency=concurrency,requests=COUNT,tokens=COUNT*gen,
             first_ns=first,last_ns=last,output_tokens_per_s=COUNT*gen/((last-first)/1e9))
    emit("client_terminal",exit_code=0)
