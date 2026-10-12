#!/usr/bin/env python3
"""Descriptive planned secondary metrics; process-group CPU is not total service CPU."""
import json,pathlib,statistics,math
root=pathlib.Path('/workspaces/repository')
rows=[json.loads(l) for l in (root/'bench/results/qwen_vllm_20261012.jsonl').read_text().splitlines()]
requests=[r for r in rows if r['event']=='request']
cells=[r for r in rows if r['event']=='cell']
assert len(requests)==2560 and len(cells)==40
cpu=[]
for r in rows:
    if r['event'] not in ['cell','idle']:continue
    before,after=r['cpu_before'],r['cpu_after']
    assert before.keys()==after.keys(),(r['event'],r['pair'],r['mode'])
    assert all(after[k]>=before[k] for k in before)
    value=sum(after.values())-sum(before.values())
    assert abs(value-r['process_group_cpu_s'])<1e-9
    cpu.append(dict(event=r['event'],pair=r['pair'],mode=r['mode'],gen=r.get('gen'),concurrency=r.get('concurrency'),window_ns=r['window_ns'],process_group_cpu_s=value,process_group_us_per_request=value/r['requests']*1e6 if r['event']=='cell' else None))
assert len(cpu)==50
print(json.dumps({'cpu_read_brackets':len(cpu),'tick_hz':rows[0]['cpu_tick_hz'],'scope':'owned process-group only, excludes kernel TX/RX/softirq/driver/clients/other owners; zero ticks not exact zero work'}))
for gen in [1,64]:
    for conc in [1,8]:
        output={}
        for mode in ['bpfusion','vllm']:
            group=[r for r in requests if (r['gen'],r['concurrency'],r['mode'])==(gen,conc,mode)]
            assert len(group)==320
            q={}
            for metric in ['ttft_ms','latency_ms','tpot_ms']:
                values=[r[metric] for r in group if r[metric] is not None]
                if values:q[metric]={'p50':statistics.quantiles(values,n=100,method='inclusive')[49],'p99':statistics.quantiles(values,n=100,method='inclusive')[98]}
            proc=[r['process_group_us_per_request'] for r in cpu if (r['event'],r['gen'],r['concurrency'],r['mode'])==('cell',gen,conc,mode)]
            output[mode]=dict(pooled_requests=len(group),inclusive_percentiles=q,process_group_us_per_request_blocks=proc,process_group_us_per_request_mean=statistics.mean(proc))
        print(json.dumps({'gen':gen,'concurrency':conc,'descriptive_secondary':output}))
for mode in ['bpfusion','vllm']:
    engines=[r for r in rows if r['event']=='executor' and r['mode']==mode]
    print(json.dumps({'mode':mode,'startup_s_blocks':[r['startup_s'] for r in engines],'startup_mean_s':statistics.mean(r['startup_s'] for r in engines),'idle_process_group_s':[r['process_group_cpu_s'] for r in cpu if r['event']=='idle' and r['mode']==mode]}))
print('SECONDARY_ANALYSIS_EXIT 0')
