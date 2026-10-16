#!/usr/bin/env python3
"""Raw standard-library replay, with client per-token gap/coalescing explicit."""
from pathlib import Path
import argparse,gzip,json,math,statistics
def lines(path):
    p=Path(path)
    return p.read_text().splitlines() if p.exists() else gzip.open(str(p)+'.gz','rt').read().splitlines()
def quantile(values,q):
    if not values:return None
    values=sorted(values);x=(len(values)-1)*q;i=math.floor(x);j=math.ceil(x)
    return values[i]+(values[j]-values[i])*(x-i)
def main(path):
    rows=[json.loads(s) for s in lines(path)];meta=rows[0]
    assert meta['event']=='metadata'
    assert rows[-1]['event']=='terminal' and rows[-1]['exit']==0
    assert not any(x['event']=='failure' for x in rows)
    reps=1 if meta['preflight'] else 5;count=16 if meta['preflight'] else 256
    assert meta['repetitions']==reps and meta['count']==count
    cells=[];total=success=tokens=0
    for pair in range(reps):
      assert [x['mode'] for x in rows if x['event']=='start' and x['pair']==pair]==meta['orders'][pair]
      for mode in meta['modes']:
        selected=[x for x in rows if x.get('pair')==pair and x.get('mode')==mode]
        end=next(x for x in selected if x['event']=='executor')
        assert not end['remaining']
        if mode!='official':
            assert end['exit']==0 and 'graph_error=0' in end['stdout']
            counter={k:int(v) for k,v in __import__('re').findall(r'(\w+)=(\d+)',end['stdout'].split('resident vLLM stopped:',1)[1].splitlines()[0])}
            assert counter['graph_error']==counter['trace_overflows']==0
            assert counter['admitted']==counter['retired']
            successes=sum(x['outcome']=='success' for x in selected if x['event']=='request')
            assert successes+8<=counter['admitted']<=2*count+8
            if mode=='kernel':
                ring=json.loads(next(s[7:] for s in end['stdout'].splitlines() if s.startswith('RESULT ')))
                assert all(ring[k]==0 for k in ['error','pending','reserved','dropped','overflow'])
                assert ring['accepted']==ring['closed']
                assert ring['sqhead']==ring['sqtail'] and ring['cqhead']==ring['cqtail']
        else:
            auth=next(x for x in selected if x['event']=='authentication')
            assert auth['missing']==auth['invalid']==401
        warm=[x for x in selected if x['event']=='warmup'];assert len(warm)==8
        assert all(x['gen']==1 and len(x['tokens'])==len(x['arrival_ns'])==1 for x in warm)
        actual=[x for x in selected if x['event']=='cell']
        assert [x['regime'] for x in actual]==(['offered192','closed16'] if pair%2==0 else ['closed16','offered192'])
        for cell in actual:
            regime=cell['regime'];attempts=[x for x in selected if x['event']=='request' and x['regime']==regime]
            assert sorted(x['index'] for x in attempts)==list(range(count))
            good=[x for x in attempts if x['outcome']=='success'];bad=[x for x in attempts if x['outcome']!='success']
            assert cell['successes']==len(good) and cell['failures']==len(bad) and cell['attempts']==count
            sets={(tuple(x['prompt']),x['gen']):x['sequences'] for x in meta['reference_pool']['references']}
            for x in attempts:
                assert x['input_ids']==meta['prompts'][x['index']%4] and x['gen']==64
                if x['outcome']!='success':continue
                assert len(x['tokens'])==len(x['arrival_ns'])==64 and x['arrival_ns']==sorted(x['arrival_ns'])
                assert all(type(v)==int and 0<=v<meta['vocab'] for v in x['tokens'])
                assert x['reference_set_match']==(x['tokens'] in sets[tuple(x['input_ids']),64])
                assert x['ttft_ms']==(x['arrival_ns'][0]-x['start_ns'])/1e6
                assert x['latency_ms']==(x['arrival_ns'][-1]-x['start_ns'])/1e6
                assert x['tpot_ms']==(x['arrival_ns'][-1]-x['arrival_ns'][0])/63/1e6
            schedule=None
            if regime=='offered192':
                schedule=next(x for x in selected if x['event']=='arrival_schedule' and x['regime']==regime)
                assert len(schedule['scheduled_ns'])==count
                other=next(x for x in rows if x['event']=='arrival_schedule' and x['pair']==pair)
                assert [v-schedule['epoch_ns'] for v in schedule['scheduled_ns']]==[v-other['epoch_ns'] for v in other['scheduled_ns']]
                for x in attempts:
                    assert x['scheduled_ns']==schedule['scheduled_ns'][x['index']]
            duration=(cell['end_ns']-cell['begin_ns'])/1e9;assert duration>0
            delivered=sum(len(x['tokens']) for x in good);assert cell['output_tokens']==delivered
            gaps=[(b-a)/1e6 for x in good for a,b in zip(x['arrival_ns'],x['arrival_ns'][1:])]
            result=dict(event='cell_metrics',pair=pair,mode=mode,regime=regime,attempts=count,successes=len(good),failures=len(bad),
                failure_types=[x.get('error_type') for x in bad],invalid_outcomes=sum(x.get('error_kind')=='protocol_or_validation' for x in bad),partial_tokens=sum(len(x.get('tokens',[])) for x in bad),
                duration_s=duration,output_tokens_per_s=delivered/duration,all_observed_tokens_per_s=(delivered+sum(len(x.get('tokens',[])) for x in bad))/duration,request_throughput=len(good)/duration,
                reference_set_matches=sum(x['reference_set_match'] for x in good),
                client_token_gap_zero_fraction=sum(v==0 for v in gaps)/len(gaps) if gaps else None,
                process_group_cpu_ms_per_attempt=cell['process_group_cpu_ns']/count/1e6 if cell['process_group_cpu_ns'] is not None else None,
                process_group_stable=cell['process_group_stable'],failure_censored=bool(bad))
            for name,values in [('ttft_ms',[x['ttft_ms'] for x in good]),('completion_ms',[x['latency_ms'] for x in good]),('tpot_ms',[x['tpot_ms'] for x in good]),
                                ('client_token_gap_ms',gaps),('positive_receive_gap_ms',[v for v in gaps if v>0])]:
                result[name+'_mean']=statistics.mean(values) if values else None
                for q in [.5,.95,.99]:result[name+'_p'+str(int(100*q))]=quantile(values,q)
            if regime=='offered192':
                for name,values in [('client_scheduling_lag_ms',[(x['thread_start_ns']-x['scheduled_ns'])/1e6 for x in attempts]),
                                    ('scheduled_ttft_ms',[(x['arrival_ns'][0]-x['scheduled_ns'])/1e6 for x in good]),
                                    ('scheduled_completion_ms',[(x['arrival_ns'][-1]-x['scheduled_ns'])/1e6 for x in good]),
                                    ('connect_ttft_ms',[(x['arrival_ns'][0]-x['connect_begin_ns'])/1e6 for x in good])]:
                    for q in [.5,.95,.99]:result[name+'_p'+str(int(q*100))]=quantile(values,q)
            print(json.dumps(result));cells.append(result);total+=count;success+=len(good);tokens+=delivered
    assert len(cells)==reps*6 and total==rows[-1]['attempts'] and success==rows[-1]['successes']
    print(json.dumps(dict(event='coverage',executors=3*reps,cells=len(cells),attempts=total,successes=success,failures=total-success,tokens=tokens,warmups=24*reps)))
    for regime in ['offered192','closed16']:
      for contrast,a,b in [('native_vs_official','native','official'),('kernel_vs_official','kernel','official'),('kernel_vs_native','kernel','native')]:
       for metric in ['output_tokens_per_s','client_token_gap_ms_p99','ttft_ms_p99','completion_ms_p99','tpot_ms_mean','process_group_cpu_ms_per_attempt']:
        aa=[x for x in cells if x['regime']==regime and x['mode']==a];bb=[x for x in cells if x['regime']==regime and x['mode']==b]
        assert [x['pair'] for x in aa]==[x['pair'] for x in bb]==list(range(reps))
        effects=[x[metric]-y[metric] if x[metric] is not None and y[metric] is not None else None for x,y in zip(aa,bb)]
        valid=all(x is not None for x in effects)
        mean=statistics.mean(effects) if valid else None
        margin=2.776445105*statistics.stdev(effects)/math.sqrt(5) if valid and reps==5 else None
        print(json.dumps(dict(event='paired',regime=regime,contrast=contrast,candidate=a,baseline=b,metric=metric,effects=effects,signed_mean=mean,
            signed_t95=[mean-margin,mean+margin] if margin is not None else None,
            failure_censored=any(x['failure_censored'] for x in aa+bb),invalid_outcomes=sum(x['invalid_outcomes'] for x in aa+bb),
            primary=contrast=='native_vs_official' and ((regime=='closed16' and metric=='output_tokens_per_s') or (regime=='offered192' and metric=='client_token_gap_ms_p99')))))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('path',type=Path);main(p.parse_args().path)
