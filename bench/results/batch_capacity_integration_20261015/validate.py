from pathlib import Path
import os,subprocess,json,datetime,traceback
t=Path(__file__).resolve().parent;r=Path('/workspaces/repository')
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
env=dict(os.environ,**json.loads((t/'environment.json').read_text()))
env.pop('VLLM_BATCH_INVARIANT',None)
base=dict(os.environ,LD_LIBRARY_PATH=str(t/'libbpf_install/usr/lib64'))
models=json.loads((t/'models.json').read_text())
status=[];exit_code=1
def run(label,cmd,environ):
    rec=dict(label=label,command=cmd,start=stamp());status.append(rec)
    (t/'validation_status.json').write_text(json.dumps(status,indent=2))
    print('START',label,rec['start'],flush=True)
    with (t/(label+'.stdout')).open('x') as out,(t/(label+'.stderr')).open('x') as err:
        p=subprocess.Popen(cmd,cwd=r,env=environ,stdout=out,stderr=err)
        rec.update(pid=p.pid,proc_stat=Path('/proc/'+str(p.pid)+'/stat').read_text())
        (t/'validation_status.json').write_text(json.dumps(status,indent=2))
        rec['exit']=p.wait()
    rec['end']=stamp()
    (t/'validation_status.json').write_text(json.dumps(status,indent=2))
    print('END',label,rec['exit'],flush=True)
    assert rec['exit']==0,rec
try:
    assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
    assert not Path('/sys/module/bfusion_tx').exists()
    assert not any(Path('/sys/fs/bpf',n).exists() for n in ['bpfusion_ctl','bpfusion_stats','bpfusion_db'])
    for banks in [8,16]:
        for name,model in models.items():
            label='protocol_'+name+'_'+str(banks)
            cmd=[str(t/'runtime/bin/python'),str(t/'load.py'),'--correctness','--banks',str(banks),'--model',model,'--output',str(t/(label+'.jsonl'))]
            if banks==8:cmd+=['--native-only']
            run(label,cmd,env)
            run(label+'_analysis',['/usr/bin/python3',str(t/'protocol_analysis.py'),str(t/(label+'.jsonl'))],env)
    for backend in ['vllm','hf']:
        for name in models:
            run('lifecycle_'+backend+'_'+name+'_8',[str(t/'runtime/bin/python') if backend=='vllm' else '/usr/bin/python3',str(t/'lifecycle.py'),'native',name,'8',backend],env if backend=='vllm' else base)
            result=json.loads((t/('lifecycle_'+backend+'_'+name+'_8')/(name+'.results.json')).read_text())
            assert result['pass'] is True,result.get('error',result)
    exit_code=0
except BaseException:
    (t/'validation_failure.txt').write_text(traceback.format_exc());traceback.print_exc()
finally:
    (t/'validation.exit.json').write_text(json.dumps(dict(exit=exit_code,utc=stamp()),indent=2))
    print('VALIDATION_TERMINAL',exit_code,stamp(),flush=True)
raise SystemExit(exit_code)
