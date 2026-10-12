#!/usr/bin/env python3
"""Pinned upstream backend qualification; complete independent HF token oracles."""
import pathlib,os,sys,json,time,subprocess,gc,types,traceback,datetime
root=pathlib.Path(__file__).resolve().parent
repo=pathlib.Path('/workspaces/repository')
os.environ['CUDA_HOME']='/usr/local/cuda'
os.environ['PATH']=str(root/'deps/bin')+':/usr/local/cuda/bin:'+os.environ['PATH']
os.environ['TORCH_EXTENSIONS_DIR']=str(root/'build')
os.environ['PYTHONPATH']=str(root/'deps')+':'+os.environ.get('PYTHONPATH','')
sys.path.insert(0,str(root/'deps'));sys.path.insert(0,str(root/'upstream'))
import torch,transformers
from transformers import AutoModelForCausalLM,AutoTokenizer
result=repo/'bench/results/alpindale_qualification_20261012.jsonl'
raw=result.open('w')
def emit(event,**data):
    raw.write(json.dumps(dict(event=event,**data))+'\n');raw.flush()
    print(event,json.dumps(data)[:500],flush=True)
checkpoint='/workspaces/.cache/huggingface/hub/models--Qwen--Qwen3-0.6B/snapshots/c1899de289a04d12100db370d81485cdf75e47ca'
prompts=['Hello','The capital of France is','Write a Python function to add two numbers.','Explain why the sky appears blue in one sentence.']
try:
    source_files={str(p.relative_to(root/'upstream')):p.read_text() for p in (root/'upstream').rglob('*') if p.is_file()}
    emit('metadata',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),production_commit=subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip(),upstream_revision='5030e154d39ecd054df03eb4dd9c8aa8185414d1',checkpoint=checkpoint,checkpoint_config=json.loads((pathlib.Path(checkpoint)/'config.json').read_text()),torch=torch.__version__,transformers=transformers.__version__,torch_cuda=torch.version.cuda,source_files=source_files,qualifier_source=pathlib.Path(__file__).read_text(),dependency_install=(root/'dependency-install.txt').read_text(),gpu_before=subprocess.check_output(['nvidia-smi','--query-compute-apps=pid,process_name,used_memory','--format=csv,noheader'],text=True))
    tokenizer=AutoTokenizer.from_pretrained(checkpoint,local_files_only=True)
    ids=[tokenizer.encode(p,add_special_tokens=True) for p in prompts]
    references={}
    for attention in ['eager','default']:
        kwargs={} if attention=='default' else dict(attn_implementation='eager')
        model=AutoModelForCausalLM.from_pretrained(checkpoint,dtype=torch.bfloat16,local_files_only=True,**kwargs).to('cuda').eval()
        refs=[]
        for case,prompt_ids in enumerate(ids):
            with torch.no_grad():
                out=model(torch.tensor([prompt_ids],device='cuda'),use_cache=True)
                past=out.past_key_values;nxt=int(out.logits[:,-1].argmax(-1));expected=[nxt]
                for _ in range(63):
                    out=model(torch.tensor([[nxt]],device='cuda'),past_key_values=past,use_cache=True)
                    past=out.past_key_values;nxt=int(out.logits[:,-1].argmax(-1));expected.append(nxt)
            refs.append(expected)
            emit('reference',attention=attention,actual_attention=model.config._attn_implementation,case=case,prompt=prompts[case],input_ids=prompt_ids,expected=expected)
        references[attention]=refs
        del model,out,past;gc.collect();torch.cuda.empty_cache()
    # Only loader compatibility: avoid an absent accelerate dependency.
    model_path=root/'upstream/qwen_megakernel/model.py';original=model_path.read_text()
    needle='dtype=torch.bfloat16, device_map="cuda"\n    )'
    assert original.count(needle)==1
    compatible=original.replace(needle,'dtype=torch.bfloat16\n    ).to("cuda")')
    model_path.write_text(compatible)
    emit('loader_compatibility',before=needle,after='dtype=torch.bfloat16\n    ).to("cuda")',actual_source=compatible)
    start=time.monotonic()
    import qwen_megakernel
    emit('native_build',seconds=time.monotonic()-start,extension_dir=str(root/'build'),cuda_source_changed=False,bindings_source_changed=False)
    groups={}
    for condition,theta in [('upstream_theta',10000),('checkpoint_theta',1000000)]:
        module=types.ModuleType('qualification_'+condition)
        candidate=compatible if theta==10000 else compatible.replace('10000.0 **','1000000.0 **')
        if theta!=10000:assert compatible.count('10000.0 **')==1
        exec(compile(candidate,str(root/(condition+'.py')),'exec'),module.__dict__)
        emit('importer',condition=condition,theta=theta,source=candidate)
        dec=module.Decoder(model_name=checkpoint,verbose=False)
        for mode in ['step','bulk']:
            for repetition in range(2):
                for case,prompt_ids in enumerate(ids):
                    dec.reset()
                    for tid in prompt_ids[:-1]:dec.step(tid)
                    start=time.monotonic()
                    if mode=='step':
                        token=prompt_ids[-1];actual=[]
                        for _ in range(64):
                            token=dec.step(token);actual.append(token)
                    else:
                        args=[getattr(dec,x) for x in ['_embed_weight','_layer_weights_packed','_final_norm_weight','_lm_head_weight','_cos_table','_sin_table','_k_cache','_v_cache','_hidden','_act','_res','_q','_k','_v','_attn_out','_mlp_inter','_norm_out','_bmax_vals','_bmax_idxs']]
                        out=torch.ops.qwen_megakernel_C.generate_nosync(prompt_ids[-1],64,*args,module.NUM_LAYERS,dec._position,module.MAX_SEQ_LEN,dec._attn_scale)
                        dec._position+=64;actual=out.cpu().tolist()
                    torch.cuda.synchronize()
                    expected=references['eager'][case];default=references['default'][case]
                    mismatch=next((i for i,(a,b) in enumerate(zip(actual,expected)) if a!=b),None)
                    assert len(actual)==len(expected)==64
                    groups[(condition,mode,repetition,case)]=actual
                    emit('generation',condition=condition,mode=mode,repetition=repetition,case=case,input_ids=prompt_ids,actual=actual,expected=expected,default_expected=default,eager_exact=actual==expected,default_exact=actual==default,first_eager_mismatch=mismatch,decode_call_seconds=time.monotonic()-start,position=dec.position)
        del dec;gc.collect();torch.cuda.empty_cache()
    qualifications={}
    for condition in ['upstream_theta','checkpoint_theta']:
        eager=all(groups[(condition,m,r,c)]==references['eager'][c] for m in ['step','bulk'] for r in range(2) for c in range(4))
        default=all(groups[(condition,m,r,c)]==references['default'][c] for m in ['step','bulk'] for r in range(2) for c in range(4))
        modes=all(groups[(condition,'step',r,c)]==groups[(condition,'bulk',r,c)] for r in range(2) for c in range(4))
        repeat=all(groups[(condition,m,0,c)]==groups[(condition,m,1,c)] for m in ['step','bulk'] for c in range(4))
        qualifications[condition]=dict(eager_exact_all=eager,default_exact_all=default,modes_agree=modes,repeats_agree=repeat,strict_qualified=eager and modes and repeat)
    emit('summary',sequences=len(groups),tokens=sum(len(x) for x in groups.values()),conditions=qualifications)
    emit('terminal',exit=0)
except BaseException:
    emit('failure',traceback=traceback.format_exc());emit('terminal',exit=1)
    raise
finally:raw.close()
