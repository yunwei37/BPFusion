# Native token HTTP functions and cross-node timing adapter; actual invocation appends literals.
import os,socket,struct,time,json,threading
from concurrent.futures import ThreadPoolExecutor

def request(client,ids,expected):
    body=struct.pack("<IIIIQ",0x514c4d51,len(ids),len(expected),0,time.monotonic_ns())+struct.pack(f"<{len(ids)}I",*ids)
    wire=f"POST /generate HTTP/1.1\r\nHost: localhost\r\nContent-Length: {len(body)}\r\n\r\n".encode()+body
    start=time.monotonic_ns()
    client.sendall(wire)
    header=b""; data=b""; arrivals=[]
    while len(data)<4*len(expected):
        chunk=client.recv(4096)
        arrived=time.monotonic_ns()
        assert chunk,"short reply"
        if header is not None:
            header+=chunk
            if b"\r\n\r\n" not in header: continue
            head,chunk=header.split(b"\r\n\r\n",1)
            assert head.startswith(b"HTTP/1.1 200 OK\r\n"),head
            assert f"Content-Length: {4*len(expected)}".encode() in head,head
            header=None
        data+=chunk
        arrivals.extend([arrived]*((len(data)//4)-len(arrivals)))
    assert len(data)==4*len(expected),data
    actual=list(struct.unpack(f"<{len(expected)}I",data))
    assert actual==expected,(ids,actual,expected)
    return {"start_ns":start,"arrival_ns":arrivals,"tokens":actual,
            "ttft_ms":(arrivals[0]-start)/1e6,
            "latency_ms":(arrivals[-1]-start)/1e6,
            "tpot_ms":(arrivals[-1]-arrivals[0])/(len(expected)-1)/1e6 if len(expected)>1 else None}


def connect():
    client=socket.create_connection((os.environ.get("BF_BIND","127.0.0.1"),39403),timeout=60)
    client.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)
    return client



def emit(event,base,**values):
    print(json.dumps(dict(event=event,**base,**values)),flush=True)


def warmup(cases):
    with connect() as client:
        for gen in (1,64):
            for ids,expected in cases:
                request(client,ids,expected[:gen])


def run(cases,gen,concurrency,count,base):
    rows=[]
    ready=threading.Barrier(concurrency+1)
    barrier=threading.Barrier(concurrency+1)
    def worker(worker_id):
        with connect() as client:
            ready.wait(timeout=60)
            barrier.wait(timeout=60)
            for index in range(worker_id,count,concurrency):
                case=index%len(cases);ids,expected=cases[case]
                row=request(client,ids,expected[:gen])
                row.update(index=index,case=case)
                rows.append(row)
    try:
        with ThreadPoolExecutor(max_workers=concurrency) as pool:
            futures=[pool.submit(worker,i) for i in range(concurrency)]
            ready.wait(timeout=60)
            barrier.wait(timeout=60)
            for future in futures:future.result()
    finally:
        for row in sorted(rows,key=lambda row:row["index"]):
            emit("request",base,**row)
    first=min(row["start_ns"] for row in rows)
    last=max(row["arrival_ns"][-1] for row in rows)
    emit("cell",base,requests=count,output_tokens_per_s=count*gen/((last-first)/1e9))
