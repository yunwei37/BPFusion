#!/usr/bin/env python3
"""Bounded offered-arrival remote client; one async task per attempt, no cap."""
import argparse,asyncio,json,os,socket,struct,sys,time,traceback
from pathlib import Path
def now():return time.monotonic_ns()
async def main(args):
 cfg=json.loads(Path(args.config).read_text());prompts=cfg["prompts"]
 vocab=cfg["frozen_model"]["vocab"]
 pools={(tuple(r["prompt"]),r["gen"]):r["sequences"] for r in cfg["frozen_model"]["references"]}
 raw=Path(args.output).open("x",buffering=1)
 def emit(event,**kw):raw.write(json.dumps(dict(event=event,mono_ns=now(),**kw))+"\n")
 emit("client_metadata",python=sys.version,host=args.host,pair=args.pair,mode=args.mode,rate=args.rate,process_cpu_ns=time.process_time_ns(),scope="remote client-local stamps; no cross-host clock subtraction",source=Path(__file__).read_text(),config=cfg,
      proc={f:Path("/proc/"+f).read_text() for f in ["stat","softirqs","interrupts","self/stat","self/cgroup","loadavg","pressure/cpu"]})
 async def attempt(index,gen,due=None,warmup=False):
  ids=prompts[index%4];tokens=[];arrival=[];writer=None
  row=dict(index=index,gen=gen,input_ids=ids,scheduled_ns=due,task_start_ns=now(),tokens=tokens,arrival_ns=arrival)
  try:
   row["connect_begin_ns"]=now()
   reader,writer=await asyncio.wait_for(asyncio.open_connection(args.host,39403),60)
   row["connect_end_ns"]=now()
   writer.get_extra_info("socket").setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)
   stamp=now();body=struct.pack("<IIIIQ",0x514c4d51,len(ids),gen,0,stamp)+struct.pack("<"+"I"*len(ids),*ids)
   wire=("POST /generate HTTP/1.1\r\nHost: localhost\r\nContent-Length: %d\r\n\r\n"%len(body)).encode()+body
   row["client_ns"]=stamp;row["start_ns"]=now();writer.write(wire);await asyncio.wait_for(writer.drain(),60);row["send_done_ns"]=now()
   header=b"";data=b"";row["received_bytes"]=0
   while len(data)<4*gen:
    chunk=await asyncio.wait_for(reader.read(4096),60);seen=now()
    if not chunk:raise ConnectionError("short reply")
    row["received_bytes"]+=len(chunk)
    if header is not None:
     header+=chunk
     if b"\r\n\r\n" not in header:continue
     head,chunk=header.split(b"\r\n\r\n",1)
     assert head.startswith(b"HTTP/1.1 200 OK\r\n") and ("Content-Length: %d"%(gen*4)).encode() in head,head
     row["response_header_hex"]=head.hex();header=None
    data+=chunk
    complete=len(data)//4
    tokens[:]=list(struct.unpack("<"+"I"*complete,data[:complete*4]))
    arrival.extend([seen]*(complete-len(arrival)))
    row["partial_bytes_hex"]=data[complete*4:].hex()
   assert len(data)==4*gen and len(tokens)==len(arrival)==gen
   assert all(type(v)==int and 0<=v<vocab for v in tokens)
   row.update(outcome="success",reference_set_match=tokens in pools[tuple(ids),gen],ttft_ms=(arrival[0]-row["start_ns"])/1e6,
              latency_ms=(arrival[-1]-row["start_ns"])/1e6,tpot_ms=(arrival[-1]-arrival[0])/(gen-1)/1e6 if gen>1 else None)
  except BaseException as e:
   row.update(outcome="error",error_type=type(e).__name__,error=str(e),error_kind="protocol_or_validation" if isinstance(e,AssertionError) else "transport")
  finally:
   row["finish_ns"]=now()
   if writer is not None:
    writer.close()
    try:await asyncio.wait_for(writer.wait_closed(),60)
    except (OSError,TimeoutError,asyncio.CancelledError) as e:row["close_error"]=repr(e)
   row["closed_ns"]=now()
  emit("warmup" if warmup else "request",**row)
  return row
 status=1
 try:
  if args.warmup:
   results=[]
   for i in range(8):results.append(await attempt(i,1,warmup=True))
   assert all(x["outcome"]=="success" and x["reference_set_match"] for x in results)
   emit("client_terminal",exit=0,warmups=8);status=0
  else:
   offsets=json.loads(Path(args.offsets).read_text())[str(args.pair)+"_"+str(args.rate)]
   if args.preflight:offsets=offsets[:32]
   # Preflight reuses the real schedule prefix, no invented workload or parser.
   tasks=[];peak=0;active=0
   async def tracked(i,due):
    nonlocal active,peak
    active+=1;peak=max(peak,active)
    try:return await attempt(i,64,due)
    finally:active-=1
   epoch=now();emit("arrival_schedule",epoch_ns=epoch,offsets_ns=offsets,scheduled_ns=[epoch+x for x in offsets],seed=20261015+args.pair)
   for i,offset in enumerate(offsets):
    due=epoch+offset;delay=(due-now())/1e9
    if delay>0:await asyncio.sleep(delay)
    tasks.append(asyncio.create_task(tracked(i,due)))
   results=await asyncio.gather(*tasks);end=now()
   emit("cell",attempts=len(results),successes=sum(x["outcome"]=="success" for x in results),failures=sum(x["outcome"]!="success" for x in results),
        epoch_ns=epoch,end_ns=end,max_in_flight=peak,requested_output_tokens=64*len(results),client_process_cpu_ns=time.process_time_ns(),
        proc={f:Path("/proc/"+f).read_text() for f in ["stat","softirqs","interrupts","self/stat","loadavg","pressure/cpu"]})
   emit("client_terminal",exit=0,attempts=len(results));status=0
 except BaseException as e:emit("client_failure",error=repr(e),traceback=traceback.format_exc())
 finally:raw.close()
 return status
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--host",required=True);ap.add_argument("--config",required=True);ap.add_argument("--offsets",required=True)
 ap.add_argument("--output",required=True);ap.add_argument("--pair",type=int,required=True);ap.add_argument("--rate",type=int,choices=[96,192],required=True)
 ap.add_argument("--mode",choices=["kernel","native"],required=True);ap.add_argument("--warmup",action="store_true");ap.add_argument("--preflight",action="store_true")
 raise SystemExit(asyncio.run(main(ap.parse_args())))
