"""Owner-only independent-code audit of actual native logs; no other reviewer."""
from pathlib import Path
import argparse,gzip,json,math,statistics,subprocess
import numpy as np
FROZEN="3d3878c80edbaa7cc1a0bb7c87519b737ffae4f1"
def raw(path):
    if not path.exists():path=Path(str(path)+".gz")
    return gzip.decompress(path.read_bytes()) if path.suffix==".gz" else path.read_bytes()
def records(path):
    return [json.loads(l) for l in raw(path).splitlines()]
def close(a,b):
    assert math.isclose(float(a),float(b),rel_tol=3e-11,abs_tol=2e-7),(a,b)
DT=np.dtype([("index","<u8"),("scheduled","<u8"),("begin","<u8"),("sent","<u8"),
 ("complete","<u8"),("end","<u8"),("pattern","<u4"),("status","<u4"),("bytes","<u4"),("errno","<u4"),
 ("reply","u1",(256,))])
assert DT.itemsize==320
def audit_cell(prefix,source):
    path=prefix.parent;meta=records(Path(str(prefix)+".client.jsonl.gz"))[0]
    assert meta["source"]==source["bench/graph_network_client.py"]
    assert meta["native_source"]==source["bench/graph_network_client.cpp"]
    assert meta["worker_exit"]==[0]*8 and meta["workers"]==8 and meta["connections_per_worker"]==16
    schedule=np.frombuffer(raw(path/meta["schedule_file"]),dtype="<u8")
    pattern=np.frombuffer(raw(path/meta["patterns_file"]),dtype="<f4").reshape(16,128)
    inputs=pattern[:,:64];oracle=pattern[:,64:];wanted=[]
    for x in inputs:
        if meta["operation"]=="matmul":
            w=(np.arange(64)%7-3).reshape(8,8)
            expected=x.astype(np.float64).reshape(8,8)@w
            wanted.append(expected.ravel())
        else:
            z=x[::2].astype(np.float64)+1j*x[1::2].astype(np.float64)
            transformed=np.fft.fft(z);expected=np.empty(64)
            expected[::2]=transformed.real;expected[1::2]=transformed.imag
            # These finite basis patterns have exact integer-valued DFTs.
            assert np.max(np.abs(expected-np.rint(expected)))<1e-10
            wanted.append(np.rint(expected))
    wanted=np.asarray(wanted);assert np.array_equal(oracle,wanted)
    chunks=[];timers=[]
    for part in meta["worker_parts"]:
        data=np.frombuffer(raw(path/part["records"]),dtype=DT)
        terminal=json.loads(raw(path/part["terminal"]));ready=json.loads(raw(path/part["ready"]))
        assert np.all(data["index"]%8==part["part"]) and terminal["records"]==len(data)
        assert np.all(data["bytes"]<=256) and np.all(data["pattern"]==data["index"]%16)
        assert terminal["failures"]==int(np.sum(data["status"]!=0))
        assert all(x["tcp_nodelay"]==1 for x in ready["connections"])
        good=data[data["status"]==0]
        reply=good["reply"].copy().view("<f4").reshape(-1,64)
        assert np.array_equal(reply,wanted[good["pattern"]])
        assert np.all(good["bytes"]==256)
        assert np.all(good["complete"]>=good["sent"]) and np.all(good["sent"]>=good["begin"])
        chunks.append(data)
        timer=np.frombuffer(raw(path/part["timers"]),dtype="<u8").reshape(-1,3)
        assert np.all(timer[:,0]>=timer[:,1]) and np.all(timer[:,2]==timer[:,0]-timer[:,1])
        timers.append(timer[:,2])
    data=np.concatenate(chunks);assert len(data)==meta["attempts"]==len(schedule)
    assert np.array_equal(np.sort(data["index"]),np.arange(len(data)))
    assert np.all(data["scheduled"]==meta["epoch_ns"]+schedule[data["index"]])
    assert np.all(data["begin"]>=data["scheduled"]) and np.all(data["end"]>=data["begin"])
    good=data[data["status"]==0];failures=len(data)-len(good)
    values={
      "scheduled_response_ms":(good["complete"]-good["scheduled"])/1e6,
      "begin_response_ms":(good["complete"]-good["begin"])/1e6,
      "client_connection_wait_ms":(data["begin"]-data["scheduled"])/1e6,
      "timer_dispatch_lag_ms":np.concatenate(timers)/1e6}
    metric=json.loads(Path(str(prefix)+".metrics.json").read_text())
    for key,series in values.items():
        result=metric["latency"][key]
        if not len(series):assert result is None;continue
        close(np.mean(series),result["mean"]);close(np.max(series),result["max"])
        for q,label in [(.5,"p50"),(.9,"p90"),(.95,"p95"),(.99,"p99"),(.999,"p999")]:
            close(np.quantile(series,q,method="linear"),result[label])
    assert metric["attempts"]==len(data) and metric["failures"]==failures
    duration=max(meta["seconds"],(int(np.max(data["end"]))-meta["epoch_ns"])/1e9)
    close(len(good)/duration,metric["throughput"])
    if len(good)>1:
        adjusted=.99*(len(data)-1)/(len(good)-1)
        expected=None if adjusted>1 else float(np.quantile(values["scheduled_response_ms"],adjusted,method="linear"))
    else:expected=None
    if expected is None:assert metric["failure_aware_p99_ms"] is None
    else:close(expected,metric["failure_aware_p99_ms"])
    obs=records(Path(str(prefix)+".resources.jsonl.gz"))
    assert obs[0]["source"]==source["bench/resource_observer.py"]
    samples=[x for x in obs if x["event"]=="sample"];first,last=samples[0],samples[-1]
    groups=[x["process_group"] for x in samples]
    ids=lambda v:{k:x["stat"].rsplit(") ",1)[1].split()[19] for k,x in v.items()}
    assert all(ids(v)==ids(groups[0]) for v in groups)
    cpu=(sum(x["cpu_ns"] for x in groups[-1].values())-sum(x["cpu_ns"] for x in groups[0].values()))/1e6/len(data)
    close(cpu,metric["owned_group_cpu_ms_per_attempt"])
    ha=np.asarray(first["host"]["stat"].splitlines()[0].split()[1:],dtype=np.int64)
    hb=np.asarray(last["host"]["stat"].splitlines()[0].split()[1:],dtype=np.int64)
    host=(hb-ha)[[0,1,2,5,6]].sum()/obs[0]["clock_tick"]*1000/len(data)
    close(host,metric["host_active_cpu_ms_per_attempt"])
    gpu=[x for x in samples if x["device"]]
    assert len(gpu)==2 and samples[0]["device"] and samples[-1]["device"]
    gpu_owned=all(str(app["pid"]) in x["process_group"] for x in gpu for app in x["device"]["compute_apps"])
    receipt=json.loads(Path(str(prefix)+".server_started.json").read_text())
    for name,text in receipt["sources"].items():assert text==source[name],name
    assert metric["service_affinity_verified"]
    masks=[]
    requested=set(receipt["service_affinity"])
    for sample in samples:
        for tid,thread in sample.get("service_threads",{}).items():
            value=next(x.split(":",1)[1].strip() for x in thread["status"].splitlines() if x.startswith("Cpus_allowed_list:"))
            actual=set()
            for part in value.split(","):
                left,sep,right=part.partition("-")
                actual.update(range(int(left),int(right)+1) if sep else [int(left)])
            assert actual and actual<=requested
            masks.append(value)
    assert masks
    assert gpu_owned
    warm=records(Path(str(prefix)+".warmup.jsonl.gz"))[0]
    assert warm["operation"]==meta["operation"] and warm["attempts"]==32
    checked_warm=0
    for part in warm["worker_parts"]:
        wr=np.frombuffer(raw(path/part["records"]),dtype=DT)
        assert np.all(wr["status"]==0) and np.all(wr["bytes"]==256)
        assert np.array_equal(wr["reply"].copy().view("<f4").reshape(-1,64),wanted[wr["pattern"]])
        checked_warm+=len(wr)
    assert checked_warm==32
    for label,subset in [("first",good["index"]<len(data)//4),("last",good["index"]>=3*len(data)//4)]:
        v=values["scheduled_response_ms"][subset]
        if len(v):close(float(np.mean(v)),metric[label+"_quarter_response_mean_ms"])
        else:assert metric[label+"_quarter_response_mean_ms"] is None
    # Convert no values from missing interval GPU samples to zero.
    return dict(tag=prefix.name,attempts=len(data),failures=failures,
      recorded_worker_files=len(meta["worker_parts"]),all_sample_group_stable=True,
      observed_gpu_boundaries=2,gpu_boundaries_owned=gpu_owned,
      interval_gpu_samples_unavailable=len(samples)-2,
      scalar=dict(cpu=float(cpu),host=float(host),p99=metric["latency"]["scheduled_response_ms"]["p99"] if len(good) else None,
                  throughput=metric["throughput"]))
def critical_t4():
    # Independently invert exact df4 CDF: .5+.75s-.25s^3,s=t/sqrt(t^2+4).
    low,high=0.,20.
    for _ in range(100):
        mid=(low+high)/2;s=mid/math.sqrt(mid*mid+4)
        if .5+.75*s-.25*s*s*s<.975:low=mid
        else:high=mid
    return (low+high)/2
def validate_screen(root,checked):
    rows={x["tag"]:json.loads((root/"screen"/(x["tag"]+".metrics.json")).read_text()) for x in checked}
    consumed=set();boundaries=[]
    configs=[]
    for op in ["matmul","fft"]:
        configs.extend((op,rep,0) for rep in [1,16,256])
        configs.extend((op,1,c) for c in [1,2])
    rates=[1000,4000,16000,64000,256000]
    for index,(op,rep,cores) in enumerate(configs):
        for mode in ["kernel","native"]:
            saturated=False;previous=None
            for rate in rates:
                tag=("screen_cpp_recovered_" if (op,rep,cores)==("fft",1,2) else "screen_cpp_")+"%s_w%d_c%d_r%d_%s"%(op,rep,cores,rate,mode)
                if saturated:assert tag not in rows;continue
                assert tag in rows,tag
                m=rows[tag];consumed.add(tag)
                assert m["seed"]==20261017+index*1000+rate+(1000000 if (op,rep,cores)==("fft",1,2) else 0) and m["offered_seconds"]==6
                assert m["attempts"]==6*rate and m["service_affinity_verified"]
                tail=m["latency"]["scheduled_response_ms"];timer=m["latency"]["timer_dispatch_lag_ms"]
                assert timer["p99"]<=max(1,.1*tail["p99"]) if tail else timer["p99"]<=1
                first,last=m["first_quarter_response_mean_ms"],m["last_quarter_response_mean_ms"]
                growing=first is not None and last is not None and last-first>100 and last>2*first
                saturated=m["throughput"]/rate<.9 or m["failure_fraction"]>.01 or growing
                if saturated:
                    boundaries.append(dict(operation=op,repeat=rep,cores=cores,mode=mode,
                        previous_offered_rate=previous,first_saturated_offered_rate=rate,
                        observed_delivery=m["throughput"],growing_backlog=growing))
                previous=rate
            if not saturated:boundaries.append(dict(operation=op,repeat=rep,cores=cores,mode=mode,
                first_saturated_offered_rate=None,tested_through=256000))
    assert consumed==set(rows)
    return dict(configurations=len(configs),paths=20,cells=len(rows),boundaries=boundaries,
      scope="Observed brackets of this 8-slot/128-connection configuration, not exact crossover or hardware maxima.")
def confirm_effects(root):
    result=json.loads((root/"confirmation_summary.json").read_text());out=[]
    critical=critical_t4()
    for item in result["cells"]:
        independently={}
        confirmed_cells=[]
        chosen=item["cell"]
        for pair in range(5):
            for mode in ["kernel","native"]:
                m=json.loads((root/"confirmation"/("confirm_s%d_p%d_%s.metrics.json"%(item["selection"],pair,mode))).read_text())
                assert (m["operation"],m["repeat"],m["cores"],m["offered_rate"])==(chosen["operation"],chosen["repeat"],chosen["cores"],chosen["rate"])
                assert m["seed"]==420261017+item["selection"]*100+pair and m["offered_seconds"]==20
                confirmed_cells.append(m)
        independent_valid=all(m["failures"]==0 and m["group_stable"] and m["service_affinity_verified"] and
          m["latency"]["timer_dispatch_lag_ms"]["p99"]<=max(1,.1*m["latency"]["scheduled_response_ms"]["p99"]) for m in confirmed_cells)
        assert item["valid_confirmation"]==independent_valid
        for key,getter in [("group_cpu",lambda m:m["owned_group_cpu_ms_per_attempt"]),
            ("host_active_cpu",lambda m:m["host_active_cpu_ms_per_attempt"]),
            ("scheduled_p99",lambda m:m["latency"]["scheduled_response_ms"]["p99"]),
            ("begin_p99",lambda m:m["latency"]["begin_response_ms"]["p99"]),
            ("throughput",lambda m:m["throughput"]),
            ("timer_dispatch_p99",lambda m:m["latency"]["timer_dispatch_lag_ms"]["p99"])]:
            pairs=[]
            for p in range(5):
                values=[]
                for mode in ["kernel","native"]:
                    m=json.loads((root/"confirmation"/("confirm_s%d_p%d_%s.metrics.json"%(item["selection"],p,mode))).read_text())
                    values.append(getter(m))
                pairs.append(values)
            x=np.log(np.asarray(pairs)[:,0]/np.asarray(pairs)[:,1]);mean=float(np.mean(x))
            delta=critical*float(np.std(x,ddof=1))/math.sqrt(5)
            effect=[math.exp(mean),math.exp(mean-delta),math.exp(mean+delta)]
            original=item["effects"][key]
            close(effect[0],original["geometric_ratio"])
            for one,two in zip(effect[1:],original["t95_ratio"]):close(one,two)
            independently[key]=effect
        cpu,p99,tp=[independently[k] for k in ["group_cpu","scheduled_p99","throughput"]]
        valid=item["valid_confirmation"]
        assert item["cpu_criterion_met"]==bool(valid and tp[1]>=.98 and cpu[2]<.9 and p99[2]<=1.05)
        assert item["tail_criterion_met"]==bool(valid and tp[1]>=.98 and p99[2]<.9 and cpu[2]<=1.05)
        out.append(dict(selection=item["selection"],independent_ratios=independently))
    assert result["any_prespecified_local_advantage"]==any(x["cpu_criterion_met"] or x["tail_criterion_met"] for x in result["cells"])
    return dict(df4_critical=critical,selections=out)
def main(args):
    root=args.root;repo=root.parents[2]
    names=["bench/graph_network_client.py","bench/graph_network_client.cpp","bench/resource_observer.py"]
    sample=json.loads(next((root/args.phase).glob("*.server_started.json")).read_text())
    names+=list(sample["sources"])
    source={name:subprocess.check_output(["git","show",FROZEN+":"+name],cwd=repo,text=True) for name in set(names)}
    checked=[]
    for path in sorted((root/args.phase).glob("*.metrics.json")):
        checked.append(audit_cell(path.with_name(path.name.removesuffix(".metrics.json")),source))
    assert checked
    out=dict(phase=args.phase,frozen_source=FROZEN,cells=len(checked),attempts=sum(x["attempts"] for x in checked),
      failures=sum(x["failures"] for x in checked),checks=checked,
      review_scope="Sole-thread independent-code recomputation; no independent-person review. GPU observations only at boundaries.")
    if args.phase=="screen":out["coverage"]=validate_screen(root,checked)
    elif args.phase=="confirmation":out["paired_effect_recomputation"]=confirm_effects(root)
    else:out["retention_scope"]="Original invalid client-timing pair; no server-capacity ranking or selection."
    (root/(args.phase+"_owner_audit.json")).write_text(json.dumps(out,indent=2))
    print(json.dumps({k:v for k,v in out.items() if k not in ["checks","coverage","paired_effect_recomputation"]}))
if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("root",type=Path);ap.add_argument("phase",choices=["screen","confirmation","client_dispatch_initial"])
    main(ap.parse_args())
