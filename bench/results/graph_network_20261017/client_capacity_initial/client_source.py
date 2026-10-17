#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Remote open-loop client for the fixed-shape cuBLAS/cuFFT graph examples."""
import argparse,asyncio,ctypes,heapq,json,math,os,random,resource,socket,struct,subprocess,sys,time,traceback
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

class DeadlineTimer:
    """One kernel high-resolution timer per worker; no early/busy release."""
    class Timespec(ctypes.Structure):
        _fields_=[("sec",ctypes.c_long),("nsec",ctypes.c_long)]
    def __init__(self):
        class Spec(ctypes.Structure):
            _fields_=[("interval",DeadlineTimer.Timespec),("value",DeadlineTimer.Timespec)]
        self.Spec=Spec;self.libc=ctypes.CDLL(None,use_errno=True)
        self.libc.timerfd_create.argtypes=[ctypes.c_int,ctypes.c_int]
        self.libc.timerfd_settime.argtypes=[ctypes.c_int,ctypes.c_int,ctypes.POINTER(Spec),ctypes.c_void_p]
        self.fd=self.libc.timerfd_create(time.CLOCK_MONOTONIC,os.O_NONBLOCK|os.O_CLOEXEC)
        if self.fd<0:raise OSError(ctypes.get_errno(),"timerfd_create")
        self.loop=asyncio.get_running_loop();self.heap=[];self.sequence=0
        self.loop.add_reader(self.fd,self.ready)
    def arm(self):
        while self.heap and self.heap[0][2].cancelled():heapq.heappop(self.heap)
        target=self.heap[0][0] if self.heap else 0
        spec=self.Spec(self.Timespec(0,0),self.Timespec(target//1000000000,target%1000000000))
        if self.libc.timerfd_settime(self.fd,1,ctypes.byref(spec),None):
            raise OSError(ctypes.get_errno(),"timerfd_settime absolute")
    def ready(self):
        try:os.read(self.fd,8)
        except BlockingIOError:pass
        now=time.monotonic_ns()
        while self.heap and self.heap[0][0]<=now:
            _,_,future=heapq.heappop(self.heap)
            if not future.done():future.set_result(None)
        self.arm()
    async def wait(self,target):
        if time.monotonic_ns()>=target:return
        future=self.loop.create_future();self.sequence+=1
        heapq.heappush(self.heap,(target,self.sequence,future));self.arm()
        await future
    def close(self):
        self.loop.remove_reader(self.fd);os.close(self.fd)

deadline_timer=None
async def wait_until(target_ns):
    await deadline_timer.wait(target_ns)

async def worker(args):
    global deadline_timer
    deadline_timer=DeadlineTimer()
    import uvloop
    offsets=json.loads(Path(args.schedule).read_text())
    prefix=Path(args.output);values=patterns(args.operation)
    count=len(offsets);records=prefix.open("x",buffering=65536)
    cpu=time.process_time_ns();active=True;lags=[];failures=0
    def emit(v):records.write(json.dumps(v,separators=(",",":"))+"\n")
    emit(dict(event="worker_metadata",part=args.part,pid=os.getpid(),source=Path(__file__).read_text(),
              cpu_affinity=sorted(os.sched_getaffinity(0)),python=sys.version,uvloop=uvloop.__version__,timer="timerfd absolute CLOCK_MONOTONIC",
              patterns=[dict(input_hex=x.hex(),expected=y) for x,y in values]))
    connections=[]
    for _ in range(args.connections):
        reader,writer=await asyncio.wait_for(asyncio.open_connection(args.host,39403),30)
        connections.append((reader,writer))
    emit(dict(event="worker_connections",part=args.part,connections=[
        dict(index=i,local=writer.get_extra_info("sockname"),peer=writer.get_extra_info("peername"),
             tcp_nodelay=writer.get_extra_info("socket").getsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY))
        for i,(_,writer) in enumerate(connections)]))
    Path(str(prefix)+".ready").write_text(str(time.monotonic_ns()))
    while not Path(args.epoch_file).exists():await asyncio.sleep(.001)
    epoch=int(Path(args.epoch_file).read_text())
    async def timer():
        target=epoch+1000000
        while active:
            await wait_until(target)
            stamp=time.monotonic_ns()
            # Preserve every missed millisecond tick, so long pauses do not
            # count as only one low-weight observation in the lag distribution.
            while target<=stamp:
                lags.append((stamp,target,stamp-target));target+=1000000
    async def stream(local,reader,writer):
        nonlocal failures
        stride=args.workers*args.connections
        first=args.part+args.workers*local
        for index in range(first,count,stride):
            scheduled=epoch+offsets[index];deadline=scheduled+30000000000
            await wait_until(scheduled)
            begin=time.monotonic_ns();sent=None;complete=None;data=b"";outcome="failure";error=None
            pattern=index%len(values);payload,want=values[pattern]
            try:
                if begin>=deadline:raise TimeoutError("scheduled deadline expired before send")
                if writer is None:
                    reader,writer=await asyncio.wait_for(asyncio.open_connection(args.host,39403),(deadline-time.monotonic_ns())/1e9)
                writer.write(struct.pack("<IIIIQ",0x514c4d51,64,64,0,scheduled)+payload)
                await asyncio.wait_for(writer.drain(),max(.000001,(deadline-time.monotonic_ns())/1e9))
                sent=time.monotonic_ns()
                try:data=await asyncio.wait_for(reader.readexactly(256),max(.000001,(deadline-time.monotonic_ns())/1e9))
                except asyncio.IncompleteReadError as e:data=e.partial;raise
                complete=time.monotonic_ns()
                if list(struct.unpack("<64f",data))!=want:raise ValueError("independent numeric oracle mismatch")
                outcome="success"
            except Exception as e:
                error=repr(e);failures+=1
                if writer is not None:writer.close()
                writer=None
            emit(dict(event="request",index=index,pattern=pattern,scheduled_ns=scheduled,
                      begin_ns=begin,sent_ns=sent,complete_ns=complete,end_ns=time.monotonic_ns(),
                      outcome=outcome,error=error,reply_hex=data.hex()))
        if writer is not None:
            writer.close()
            try:await writer.wait_closed()
            except OSError:pass
    monitor=asyncio.create_task(timer())
    await asyncio.gather(*(stream(i,*rw) for i,rw in enumerate(connections)))
    active=False;await monitor;deadline_timer.close()
    emit(dict(event="worker_terminal",end_ns=time.monotonic_ns(),cpu_ns=time.process_time_ns()-cpu,
              failures=failures,timer_lag=lags));records.close()

def main(args):
    prefix=Path(args.output);assert not prefix.exists()
    randomizer=random.Random(args.seed);n=round(args.rate*args.seconds)
    offsets=sorted(int(randomizer.random()*args.seconds*1e9) for _ in range(n))
    schedule=Path(str(prefix)+".schedule.json");schedule.write_text(json.dumps(offsets))
    epoch_file=Path(str(prefix)+".epoch")
    children=[];files=[];started=time.monotonic_ns()
    try:
        for part in range(args.workers):
            dest=Path(str(prefix)+".w"+str(part)+".jsonl");files.append(dest)
            cmd=[sys.executable,__file__,"--host",args.host,"--operation",args.operation,"--output",str(dest),
                 "--part",str(part),"--workers",str(args.workers),"--connections",str(args.connections),
                 "--schedule",str(schedule),"--epoch-file",str(epoch_file)]
            log=Path(str(dest)+".stderr").open("x");p=subprocess.Popen(cmd,stderr=log);log.close();children.append(p)
        while not all(Path(str(p)+".ready").exists() for p in files):
            assert all(p.poll() is None for p in children),"client worker failed before ready"
            assert time.monotonic_ns()-started<60000000000,"client setup timeout"
            time.sleep(.01)
        epoch=time.monotonic_ns()+2000000000
        pending_epoch=Path(str(epoch_file)+".publishing")
        with pending_epoch.open("x") as epoch_output:epoch_output.write(str(epoch))
        pending_epoch.replace(epoch_file)
        exits=[p.wait() for p in children]
        with prefix.open("x") as out:
            out.write(json.dumps(dict(event="client_metadata",source=Path(__file__).read_text(),host=args.host,
             operation=args.operation,rate=args.rate,seconds=args.seconds,seed=args.seed,workers=args.workers,
             connections_per_worker=args.connections,attempts=n,epoch_ns=epoch,
             offsets_ns=offsets,worker_files=[p.name for p in files],worker_exit=exits,
             worker_stderr={p.name:Path(str(p)+".stderr").read_text() for p in files}))+"\n")
            for dest in files:
                for line in dest.open():out.write(line)
            usage=resource.getrusage(resource.RUSAGE_CHILDREN)
            out.write(json.dumps(dict(event="client_terminal",end_ns=time.monotonic_ns(),worker_exit=exits,
                       supervisor_cpu_ns=time.process_time_ns(),child_cpu_s=usage.ru_utime+usage.ru_stime))+"\n")
        assert all(x==0 for x in exits),exits
        print(json.dumps(dict(attempts=n,workers=args.workers,exits=exits)),flush=True)
    finally:
        for p in children:
            if p.poll() is None:p.terminate()
        for p in children:
            if p.poll() is None:
                try:p.wait(timeout=10)
                except subprocess.TimeoutExpired:p.kill();p.wait()

if __name__=="__main__":
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--host",required=True);ap.add_argument("--operation",choices=["matmul","fft"],required=True)
    ap.add_argument("--output",required=True);ap.add_argument("--rate",type=int,default=1000)
    ap.add_argument("--seconds",type=float,default=6);ap.add_argument("--seed",type=int,default=20261017)
    ap.add_argument("--workers",type=int,default=8);ap.add_argument("--connections",type=int,default=16)
    ap.add_argument("--part",type=int);ap.add_argument("--schedule");ap.add_argument("--epoch-file")
    args=ap.parse_args()
    if args.part is not None:
        import uvloop
        uvloop.run(worker(args))
    else:main(args)
