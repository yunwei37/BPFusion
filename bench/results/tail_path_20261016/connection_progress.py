from pathlib import Path
import json,re,bisect,statistics,math,sys
from analyze_timeline import open_text
raw=Path(sys.argv[1]);report=json.loads(Path(str(raw)+'.timeline.analysis.json').read_text());results=[]
for run in report['runs']:
 if not run['mode'].startswith('uring'):continue
 prefix=raw.with_suffix('').with_name(raw.stem+'_p'+str(run['pair'])+'_'+run['mode'])
 b0,b1=run['calibration']['100'],run['calibration']['101']
 def host(ns):
  alpha=(ns-b0['gpu'])/(b1['gpu']-b0['gpu'])
  return ns+(b0['low']+b0['high'])/2*(1-alpha)+(b1['low']+b1['high'])/2*alpha
 changes=[]
 for line in open_text(str(prefix)+'.ftrace.txt'):
  if 'io_uring_complete:' not in line:continue
  z=re.search(r' (\d+\.\d+):.*user_data 0x([0-9a-f]+), result (-?\d+)',line);assert z,line
  stamp,tag,res=z.groups();tag=int(tag,16);res=int(res);kind=tag>>56
  if kind==1 and res>=0:changes.append((round(float(stamp)*1e9),1))
  elif kind==4:changes.append((round(float(stamp)*1e9),-1))
 changes.sort();balance=0;low=0
 for _,change in changes:balance+=change;low=min(low,balance)
 live=-low;times=[];values=[]
 for ns,change in changes:live+=change;times.append(ns);values.append(live)
 sampled={}
 for line in open_text(str(prefix)+'.gpu.jsonl.timeline.jsonl'):
  x=json.loads(line)
  if x.get('kind')!=3 or not x['previous_ns']:continue
  key=x['previous_ns']
  if key in sampled:continue
  pos=bisect.bisect_right(times,host(x['ns']))-1
  sampled[key]=dict(progress_interval_ms=(x['ns']-key)/1e6,accepted_minus_closed=values[pos] if pos>=0 else -low)
 strata=[]
 for lo,hi in [(0,32),(33,64),(65,128),(129,256)]:
  v=[x['progress_interval_ms'] for x in sampled.values() if lo<=x['accepted_minus_closed']<=hi]
  if v:strata.append(dict(connections=[lo,hi],samples=len(v),p50_ms=statistics.median(v),p99_ms=sorted(v)[min(len(v)-1,math.ceil(.99*len(v))-1)],mean_ms=statistics.mean(v)))
 results.append(dict(pair=run['pair'],sample_scope='Post-hoc association only. Kernel accepted-minus-closed approximates GPU active-list length with CQ consumption delay; no causal allocation.',inferred_initial_connections=-low,peak_kernel_count=max(values),strata=strata))
print(json.dumps(results,indent=2))
