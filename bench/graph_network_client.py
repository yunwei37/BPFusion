#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Coordinate native remote load workers; logging/analysis stay off the hot path."""
import argparse,json,os,random,resource,struct,subprocess,sys,time
from pathlib import Path
def patterns(operation):
    result=[]
    for index in range(16):
        if operation=="matmul":
            x=[float((k*11+index*3)%7-3) for k in range(64)]
            w=[float(k%7-3) for k in range(64)]
            y=[sum(x[8*i+k]*w[8*k+j] for k in range(8)) for i in range(8) for j in range(8)]
        else:
            v=float(index%3+1);x=[0.]*64;y=[0.]*64
            if index%4==1:
                x[0]=v
                for k in range(32):y[2*k]=v
            elif index%4==2:
                for k in range(32):x[2*k]=v
                y[0]=32*v
            elif index%4==3:
                for k in range(32):x[2*k]=v if k%2==0 else -v
                y[32]=32*v
        result.append((struct.pack("<64f",*x),y))
    return result


def main(args):
    prefix=Path(args.output);assert not prefix.exists()
    assert not list(prefix.parent.glob(prefix.name+".worker*")),"preserve existing worker files; use a new tag"
    binary=args.native or Path(__file__).with_suffix("")
    if not binary.exists():binary=Path(__file__).resolve().parents[1]/"build/graph_network_client"
    assert binary.is_file(),str(binary)
    values=patterns(args.operation);n=round(args.rate*args.seconds)
    rng=random.Random(args.seed);offsets=sorted(int(rng.random()*args.seconds*1e9) for _ in range(n))
    schedule=Path(str(prefix)+".schedule.bin");pattern_file=Path(str(prefix)+".patterns.bin")
    with schedule.open("xb") as f:f.write(struct.pack("<"+"Q"*n,*offsets))
    with pattern_file.open("xb") as f:
        for payload,want in values:f.write(payload+struct.pack("<64f",*want))
    epoch_file=Path(str(prefix)+".epoch");parts=[];children=[];error=None;epoch=None
    try:
        for part in range(args.workers):
            base=Path(str(prefix)+".worker"+str(part))
            item=dict(part=part,records=base.name+".records.bin",timers=base.name+".timers.bin",
                      ready=base.name+".ready.json",terminal=base.name+".terminal.json",stderr=base.name+".stderr")
            cmd=[str(binary),args.host,str(part),str(args.workers),str(args.connections),str(n),
                 str(schedule),str(pattern_file),str(epoch_file),str(base)]
            item["command"]=cmd;parts.append(item)
            with (prefix.parent/item["stderr"]).open("x") as e:children.append(subprocess.Popen(cmd,stderr=e))
        deadline=time.monotonic()+60
        while not all((prefix.parent/p["ready"]).exists() for p in parts):
            assert all(p.poll() is None for p in children),"native worker failed before ready"
            assert time.monotonic()<deadline,"client setup timeout"
            time.sleep(.001)
        epoch=time.monotonic_ns()+2000000000
        pending=Path(str(epoch_file)+".publishing")
        with pending.open("x") as f:f.write(str(epoch))
        pending.replace(epoch_file)
        exits=[p.wait() for p in children]
    except BaseException as e:
        error=repr(e)
        for p in children:
            if p.poll() is None:p.terminate()
        for p in children:
            try:p.wait(timeout=10)
            except subprocess.TimeoutExpired:p.kill();p.wait()
        exits=[p.returncode for p in children]
    usage=resource.getrusage(resource.RUSAGE_CHILDREN);stats=[];worker_files=[]
    for item in parts:
        for kind in ["records","timers","ready","terminal","stderr"]:
            if (prefix.parent/item[kind]).exists():worker_files.append(item[kind])
        def load(kind):
            p=prefix.parent/item[kind];return json.loads(p.read_text()) if p.exists() else None
        stats.append(dict(part=item["part"],ready=load("ready"),terminal=load("terminal")))
    recorded=sum((x["terminal"] or {}).get("records",0) for x in stats)
    failures=sum((x["terminal"] or {}).get("failures",0) for x in stats)
    meta=dict(event="client_metadata",log_format="native_fixed_records_v1",source=Path(__file__).read_text(),
      native_source=Path(__file__).with_suffix(".cpp").read_text(),host=args.host,operation=args.operation,
      rate=args.rate,seconds=args.seconds,seed=args.seed,workers=args.workers,connections_per_worker=args.connections,
      attempts=n,epoch_ns=epoch,schedule_file=schedule.name,patterns_file=pattern_file.name,
      input_files=[schedule.name,pattern_file.name,epoch_file.name] if epoch_file.exists() else [schedule.name,pattern_file.name],
      worker_parts=parts,worker_files=worker_files,worker_metadata=stats,worker_exit=exits,
      worker_stderr={p["part"]:(prefix.parent/p["stderr"]).read_text() for p in parts},
      recorded=recorded,failures=failures,error=error,
      record_format="<6Q4I256s: index,scheduled,begin,sent,complete,end,pattern,status,bytes,errno,reply",
      timer_format="<3Q: stamp,target,lag",byteorder=sys.byteorder,python=sys.version)
    with prefix.open("x") as out:
        out.write(json.dumps(meta)+"\n")
        out.write(json.dumps(dict(event="client_terminal",end_ns=time.monotonic_ns(),worker_exit=exits,
          supervisor_cpu_ns=time.process_time_ns(),child_cpu_s=usage.ru_utime+usage.ru_stime,error=error))+"\n")
    assert error is None and exits==[0]*args.workers,(error,exits)
    assert recorded==n,(recorded,n)
    print(json.dumps(dict(attempts=n,recorded=recorded,failures=failures,exits=exits)),flush=True)

if __name__=="__main__":
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument("--host",required=True)
    ap.add_argument("--operation",choices=["matmul","fft"],required=True);ap.add_argument("--output",required=True)
    ap.add_argument("--rate",type=int,default=1000);ap.add_argument("--seconds",type=float,default=6)
    ap.add_argument("--seed",type=int,default=20261017);ap.add_argument("--workers",type=int,default=8)
    ap.add_argument("--connections",type=int,default=16);ap.add_argument("--native",type=Path)
    main(ap.parse_args())
