from pathlib import Path
import sys,json,gzip,math,bisect
root=Path(sys.argv[1])
files=sorted(root.glob("*_p0_official_r192.worker*.jsonl*"))
def union(intervals):
 out=[]
 for a,b in sorted(intervals):
  if b<=a:continue
  if out and a<=out[-1][1]:out[-1][1]=max(out[-1][1],b)
  else:out.append([a,b])
 return out
def subtract(left,right):
 out=[];j=0
 for a,b in left:
  while j<len(right) and right[j][1]<=a:j+=1
  pos=a;k=j
  while k<len(right) and right[k][0]<b:
   c,d=right[k]
   if c>pos:out.append([pos,min(c,b)])
   pos=max(pos,d)
   if pos>=b:break
   k+=1
  if pos<b:out.append([pos,b])
 return out
def cover(intervals,ends,a,b):
 if b<=a:return 0
 i=bisect.bisect_right(ends,a);total=0
 while i<len(intervals) and intervals[i][0]<b:
  c,d=intervals[i];total+=max(0,min(b,d)-max(a,c));i+=1
 return total
all_windows=[];total_tokens=0
for file in files:
 op=gzip.open if file.suffix==".gz" else open
 with op(file,"rt") as f:
  meta=json.loads(next(f));requests=[];cell=None;terminal=None;flags=0;tokens=0
  for line in f:
   row=json.loads(line)
   if row["event"]=="request":
    assert row["outcome"]=="success" and len(row["tokens"])==64
    tokens+=len(row["tokens"]);flags+=not row["reference_set_match"]
    requests.append((row["index"],row["scheduled_ns"],row["task_start_ns"]))
   elif row["event"]=="cell":cell=row
   elif row["event"]=="client_terminal":terminal=row
 assert terminal["exit"]==0 and cell["successes"]==len(requests) and cell["failures"]==0
 total_tokens+=tokens
 gc=union([(x[1],x[2]) for x in cell["gc_pauses"]])
 logs=union([(x[1],x[3]) for x in cell["request_log_spans"]])
 logs_without_gc=subtract(logs,gc)
 ge=[x[1] for x in gc];le=[x[1] for x in logs_without_gc]
 values=[]
 for index,a,b in requests:
  signed=b-a;delay=max(0,signed);g=cover(gc,ge,a,b);l=cover(logs_without_gc,le,a,b);residual=delay-g-l
  assert residual>=0,(index,delay,g,l)
  values.append(dict(worker=meta["worker_id"],index=index,lag_ns=signed,gc_ns=g,logging_excluding_gc_ns=l,residual_ns=residual))
 all_windows.extend(values)
 print(json.dumps(dict(event="worker_context",worker=meta["worker_id"],requests=len(requests),pool_flags=flags,
   gc_thresholds=cell["gc_thresholds"],gc_by_generation={g:dict(count=sum(x[0]==g for x in cell["gc_pauses"]),
   max_ms=max([(x[2]-x[1])/1e6 for x in cell["gc_pauses"] if x[0]==g],default=0)) for g in [0,1,2]},
   serialize_max_ms=max((x[2]-x[1])/1e6 for x in cell["request_log_spans"]),
   write_max_ms=max((x[3]-x[2])/1e6 for x in cell["request_log_spans"]))))
assert len(all_windows)==11520 and sorted(x["index"] for x in all_windows)==list(range(11520))
top=sorted(all_windows,key=lambda x:x["lag_ns"],reverse=True)[:math.ceil(len(all_windows)*.01)]
total=sum(max(0,x["lag_ns"]) for x in top)
ordered=sorted(x["lag_ns"]/1e6 for x in all_windows);q=.99*(len(ordered)-1);lo=int(q);p99=ordered[lo]+(ordered[math.ceil(q)]-ordered[lo])*(q-lo)
print(json.dumps(dict(event="diagnostic_summary",requests=len(all_windows),successes=len(all_windows),output_tokens=total_tokens,
 lag_p99_ms=p99,lag_max_ms=max(ordered),lag_min_ms=min(ordered),tail_selection="largest ceil(1%*N) actual same-worker task-start delays; posthoc client diagnostic, not a server primary",
 tail_count=len(top),tail_total_delay_ms=total/1e6,
 tail_gc_covered_ms=sum(x["gc_ns"] for x in top)/1e6,
 tail_logging_excluding_gc_ms=sum(x["logging_excluding_gc_ns"] for x in top)/1e6,
 tail_residual_ms=sum(x["residual_ns"] for x in top)/1e6,
 tail_gc_share=sum(x["gc_ns"] for x in top)/total,
 scope="Exclusive interval coverage on same-worker scheduled-to-task-start windows; no marginal P99 addition, no GPU/Linux stage attribution.")))
for x in top[:12]:print(json.dumps(dict(event="largest_delay_example",**{k:(v/1e6 if k.endswith("_ns") else v) for k,v in x.items()},time_units="ms")))
