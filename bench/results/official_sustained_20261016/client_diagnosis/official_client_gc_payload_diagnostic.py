#!/usr/bin/env python3
"""Bounded offered-arrival remote client; one async task per attempt, no cap."""
import argparse,asyncio,json,os,socket,struct,sys,time,traceback
import uvloop
import multiprocessing,copy,gc
CLIENT_WORKERS=4
FRAME_LOG_FORMAT="arrival_ns and raw SSE data payload text; UTF-8 surrogateescape roundtrip"
from pathlib import Path
def now():return time.monotonic_ns()
async def external_attempt(session,host,ids,gen,row,tokens,arrival,vocab):
 body=json.dumps({"token_ids":ids,"return_token_ids":True,"stream":True,
  "sampling_params":{"max_tokens":gen,"temperature":0.0,"ignore_eos":True,"detokenize":False}},separators=(",",":")).encode()
 row["connect_begin_ns"]=now();row["start_ns"]=now()
 # request-start includes HTTP setup. No invented send-done or connect-end stamps.
 async with session.post("http://"+host+":39404/inference/v1/generate",data=body,headers={"Content-Type":"application/json"}) as response:
  assert response.status==200,(response.status,await response.text())
  assert "text/event-stream" in response.headers.get("Content-Type","")
  pending=b"";done=False;prompt=None;finish=None;row["frames"]=[];row["received_bytes"]=0
  async for chunk in response.content.iter_any():
   seen=now();row["received_bytes"]+=len(chunk);pending+=chunk
   while b"\n\n" in pending:
    frame,pending=pending.split(b"\n\n",1)
    payload=b"\n".join(line[6:] for line in frame.splitlines() if line.startswith(b"data: "))
    if not payload:continue
    assert not done,"payload after DONE"
    if payload==b"[DONE]":done=True;continue
    row["frames"].append((seen,payload.decode("utf-8","surrogateescape")))
    obj=json.loads(payload)
    if "prompt_token_ids" in obj:prompt=obj["prompt_token_ids"]
    for choice in obj["choices"]:
     assert choice["index"]==0,choice
     values=choice.get("token_ids") or []
     assert all(type(x)==int and 0<=x<vocab for x in values)
     tokens.extend(values);arrival.extend([seen]*len(values))
     if choice.get("finish_reason") is not None:finish=choice["finish_reason"]
  assert done and not pending.strip() and prompt==ids and finish=="length" and len(tokens)==gen

async def main(args):
 cfg=json.loads(Path(args.config).read_text());prompts=cfg["prompts"]
 vocab=cfg["frozen_model"]["vocab"]
 pools={(tuple(r["prompt"]),r["gen"]):r["sequences"] for r in cfg["frozen_model"]["references"]}
 official=None
 if args.mode=="official":
  import aiohttp
  official=aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=0,force_close=True),
    timeout=aiohttp.ClientTimeout(total=None,connect=60,sock_connect=60,sock_read=60),
    headers={"Authorization":"Bearer "+Path(args.key_file).read_text().strip()})
 raw=Path(args.output).open("x",buffering=1)
 gc_pauses=[];log_spans=[];gc_begins={}
 def gc_callback(phase,info):
  generation=info["generation"]
  if phase=="start":gc_begins[generation]=now()
  else:gc_pauses.append((generation,gc_begins.pop(generation,now()),now(),info.get("collected"),info.get("uncollectable")))
 gc.callbacks.append(gc_callback)
 def emit(event,**kw):
  begin=now();encoded=json.dumps(dict(event=event,mono_ns=begin,**kw));serialized=now()
  raw.write(encoded+"\n");written=now()
  if event=="request":log_spans.append((kw["index"],begin,serialized,written))
 emit("client_metadata",python=sys.version,event_loop="uvloop "+uvloop.__version__,frame_log_format=FRAME_LOG_FORMAT,worker_id=getattr(args,"worker_id",None),host=args.host,pair=args.pair,mode=args.mode,rate=args.rate,process_cpu_ns=time.process_time_ns(),scope="remote client-local stamps; no cross-host clock subtraction",source=Path(__file__).read_text(),config=cfg,
      proc={f:Path("/proc/"+f).read_text() for f in ["stat","softirqs","interrupts","net/route","self/stat","self/cgroup","loadavg","pressure/cpu"]})
 async def attempt(index,gen,due=None,warmup=False):
  ids=prompts[index%4];tokens=[];arrival=[];writer=None
  row=dict(index=index,gen=gen,input_ids=ids,scheduled_ns=due,task_start_ns=now(),tokens=tokens,arrival_ns=arrival)
  try:
   if official is not None:
    await external_attempt(official,args.host,ids,gen,row,tokens,arrival,vocab)
    row.update(outcome="success",reference_set_match=tokens in pools[tuple(ids),gen],
       ttft_ms=(arrival[0]-row["start_ns"])/1e6,latency_ms=(arrival[-1]-row["start_ns"])/1e6,
       tpot_ms=(arrival[-1]-arrival[0])/(gen-1)/1e6 if gen>1 else None)
   else:
    row["connect_begin_ns"]=now()
    reader,writer=await asyncio.wait_for(asyncio.open_connection(args.host,39403),60)
    row["connect_end_ns"]=now();row["local_addr"]=writer.get_extra_info("sockname");row["peer_addr"]=writer.get_extra_info("peername")
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
    if warmup:row["tcp_info_hex"]=writer.get_extra_info("socket").getsockopt(socket.IPPROTO_TCP,socket.TCP_INFO,256).hex()
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
   epoch=getattr(args,"epoch_ns",None) or now();emit("arrival_schedule",epoch_ns=epoch,offsets_ns=offsets,scheduled_ns=[epoch+x for x in offsets],seed=20261015+args.pair)
   if getattr(args,"worker_id",None) is not None:assert now()<epoch,"worker schedule serialization missed common epoch"
   for i,offset in enumerate(offsets):
    if getattr(args,"worker_id",None) is not None and i%CLIENT_WORKERS!=args.worker_id:continue
    due=epoch+offset;delay=(due-now())/1e9
    if delay>0:await asyncio.sleep(delay)
    tasks.append(asyncio.create_task(tracked(i,due)))
   results=await asyncio.gather(*tasks);end=now()
   emit("cell",gc_pauses=list(gc_pauses),request_log_spans=list(log_spans),gc_thresholds=list(gc.get_threshold()),attempts=len(results),successes=sum(x["outcome"]=="success" for x in results),failures=sum(x["outcome"]!="success" for x in results),
        epoch_ns=epoch,end_ns=end,max_in_flight=peak,requested_output_tokens=64*len(results),client_process_cpu_ns=time.process_time_ns(),
        proc={f:Path("/proc/"+f).read_text() for f in ["stat","softirqs","interrupts","self/stat","loadavg","pressure/cpu"]})
   emit("client_terminal",exit=0,attempts=len(results));status=0
 except BaseException as e:emit("client_failure",error=repr(e),traceback=traceback.format_exc())
 finally:
  raw.close()
  if gc_callback in gc.callbacks:gc.callbacks.remove(gc_callback)
  if official is not None:await official.close()
 return status
def worker(args):
 raise SystemExit(uvloop.run(main(args)))
def sharded(args):
 # Common unrestricted async clients, one unchanged global arrival schedule.
 parent_start=time.process_time_ns();epoch=now()+1000000000
 output=Path(args.output);raw=output.open("x",buffering=1);workers=[]
 try:
  for index in range(CLIENT_WORKERS):
   child=copy.copy(args);child.worker_id=index;child.epoch_ns=epoch
   child.output=str(output).removesuffix(".client.jsonl")+".worker"+str(index)+".jsonl"
   proc=multiprocessing.Process(target=worker,args=(child,));proc.start()
   workers.append((proc,Path(child.output)))
  for proc,_ in workers:proc.join()
  batches=[]
  for proc,path in workers:
   lines=path.read_text().splitlines();rows=[json.loads(x) for x in lines]
   assert proc.exitcode==0 and rows[-1]["event"]=="client_terminal" and rows[-1]["exit"]==0,(path,proc.exitcode)
   batches.append((lines,rows))
  metadata=copy.deepcopy(batches[0][1][0])
  assert all(x[1][0]["config"]==metadata["config"] and x[1][0]["mode"]==metadata["mode"] for x in batches)
  schedules=[next(x for x in rows if x["event"]=="arrival_schedule") for _,rows in batches]
  assert all(x["mono_ns"]<epoch for x in schedules),"worker not ready before shared epoch"
  assert all({k:v for k,v in x.items() if k!="mono_ns"}=={k:v for k,v in schedules[0].items() if k!="mono_ns"} for x in schedules)
  requests=sorted([(obj,line) for lines,rows in batches for line,obj in zip(lines,rows) if obj["event"]=="request"],key=lambda x:x[0]["index"])
  n=len(schedules[0]["offsets_ns"])
  assert [x[0]["index"] for x in requests]==list(range(n))
  assert all(x["scheduled_ns"]==schedules[0]["scheduled_ns"][x["index"]] for x,_ in requests)
  cells=[next(x for x in rows if x["event"]=="cell") for _,rows in batches]
  assert sum(c["attempts"] for c in cells)==n
  # Shared local monotonic timestamps: never use process start/finish as duration.
  end=max(x["closed_ns"] for x,_ in requests)
  changes=sorted([(x["task_start_ns"],1) for x,_ in requests]+[(x["closed_ns"],-1) for x,_ in requests])
  active=0;peak=0
  for _,delta in changes:active+=delta;peak=max(peak,active)
  assert active==0
  metadata.update(worker_id=None,workers=CLIENT_WORKERS,worker_files=[x.name for _,x in workers],
    client_cpu_scope="sum of child acquisition CPU deltas plus supervisor startup/wait/merge; raw worker counters retained",
    duration_scope="one common future scheduled epoch through last original request close",
    inflight_scope="task-start through request-close timestamps",
    worker_metadata=[rows[0] for _,rows in batches])
  raw.write(json.dumps(metadata)+"\n");raw.write(json.dumps(schedules[0])+"\n")
  for _,line in requests:raw.write(line+"\n")
  supervisor_cpu=time.process_time_ns()-parent_start
  children_cpu=sum(c["client_process_cpu_ns"]-rows[0]["process_cpu_ns"] for c,(_,rows) in zip(cells,batches))
  cell=dict(event="cell",mono_ns=now(),attempts=n,successes=sum(x["outcome"]=="success" for x,_ in requests),
    failures=sum(x["outcome"]!="success" for x,_ in requests),epoch_ns=epoch,end_ns=end,max_in_flight=peak,
    requested_output_tokens=64*n,client_cpu_ns=children_cpu+supervisor_cpu,child_cpu_ns=children_cpu,
    supervisor_cpu_ns=supervisor_cpu,worker_cells=cells)
  raw.write(json.dumps(cell)+"\n")
  raw.write(json.dumps(dict(event="client_terminal",mono_ns=now(),exit=0,attempts=n))+"\n")
  return 0
 except BaseException as error:
  raw.write(json.dumps(dict(event="client_failure",error=repr(error),traceback=traceback.format_exc()))+"\n")
  raw.write(json.dumps(dict(event="client_terminal",exit=1))+"\n")
  return 1
 finally:
  raw.close()
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--host",required=True);ap.add_argument("--config",required=True);ap.add_argument("--offsets",required=True)
 ap.add_argument("--output",required=True);ap.add_argument("--pair",type=int,required=True);ap.add_argument("--rate",type=int,choices=[96,192],required=True)
 ap.add_argument("--mode",choices=["kernel","native","official"],required=True);ap.add_argument("--key-file",default="/tmp/official_remote_key");ap.add_argument("--warmup",action="store_true");ap.add_argument("--preflight",action="store_true")
 args=ap.parse_args()
 raise SystemExit(uvloop.run(main(args)) if args.warmup else sharded(args))
