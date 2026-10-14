import pathlib,json,sys,os,datetime,traceback,functools
r=pathlib.Path(__file__).parent
upstream=r/'AutoMegaKernel-884534c4d2dbed4381576f81a79ae97feca53c34'
sys.path.insert(0,str(upstream))
import torch,torch.utils.cpp_extension as cpp
original=cpp.load
def compatible_load(*args,**kwargs):
 flags=kwargs.get('extra_cflags')
 if flags and '-std=c++17' in flags:kwargs['extra_cflags']=['-std=c++20' if x=='-std=c++17' else x for x in flags]
 return original(*args,**kwargs)
cpp.load=compatible_load
from transformers import AutoModelForCausalLM
from schedule.ir import DType,TARGETS,BufferKind
from schedule.graph import from_hf,weights_from_hf
from schedule.lower import lower,TOKEN_NAME,POS_NAME,RESHAPE_ID_NAME
import vm.loader
NativeVM=vm.loader.MegakernelVM
# Match the persistent backend's documented register/coalesced variant.
vm.loader.MegakernelVM=functools.partial(NativeVM,knobs={'cpasync':0})
from generate import generate
from vm.loader_persist import PersistentDecodeVM
cfg=json.loads((r/'smol_frozen.json').read_text())
pool={(tuple(x['prompt']),x['gen']):{tuple(y) for y in x['sequences']} for x in cfg['frozen_model']['references']}
raw=(r/'fp16_probe.jsonl').open('x',buffering=1)
def emit(event,**fields):
 raw.write(json.dumps(dict(event=event,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),**fields))+'\n')
 print(event,fields.get('case',''),fields.get('gen',''),fields.get('method',''),flush=True)
emit('metadata',checkpoint=cfg['model'],source_revision='884534c4d2dbed4381576f81a79ae97feca53c34',torch=torch.__version__,cuda=torch.version.cuda,device=torch.cuda.get_device_name(),precision='FP16',knobs={'cpasync':0},prompts=cfg['prompts'],frozen_model=cfg['frozen_model'],probe_source=pathlib.Path(__file__).read_text())
code=1
try:
 model=AutoModelForCausalLM.from_pretrained(cfg['model'],dtype=torch.float16).eval()
 graph=from_hf(model);weights=weights_from_hf(model);target=TARGETS['rtx5090']
 for gen in [1,64]:
  for case,ids in enumerate(cfg['prompts']):
   emit('start',case=case,gen=gen,method='official_per_step')
   actual=generate(model,'rtx5090',ids,gen,device='cuda',dtype=DType.F16,verify=False)
   tokens=actual['generated']
   emit('output',case=case,gen=gen,method='official_per_step',tokens=tokens,matches_frozen=tuple(tokens) in pool[(tuple(ids),gen)])
   assert len(tokens)==gen and tuple(tokens) in pool[(tuple(ids),gen)],('per_step',case,gen,tokens)
   emit('start',case=case,gen=gen,method='official_persistent')
   base=len(ids)-1
   pvm=PersistentDecodeVM(lower(graph,target=target,pos=base,dtype=DType.F16),weights,device='cuda')
   kv={}
   for pos,token in enumerate(ids[:-1]):
    vm=NativeVM(lower(graph,target=target,pos=pos,dtype=DType.F16),weights,device='cuda',knobs={'cpasync':0})
    out=vm.run({TOKEN_NAME:torch.tensor([token],dtype=torch.int32,device='cuda'),POS_NAME:torch.tensor([pos],dtype=torch.int32,device='cuda'),RESHAPE_ID_NAME:torch.tensor([0],dtype=torch.int32,device='cuda')},kv=kv)
    kv={b.name:out[b.name] for b in vm.prog.buffers if b.kind==BufferKind.KV_CACHE and b.name in out}
   result=pvm.decode(ids[-1],base,gen,kv=kv)
   tokens2=result['tokens']
   emit('output',case=case,gen=gen,method='official_persistent',tokens=tokens2,status=result['status'],matches_frozen=tuple(tokens2) in pool[(tuple(ids),gen)],matches_per_step=tokens2==tokens)
   assert len(tokens2)==gen and tokens2==tokens and tuple(tokens2) in pool[(tuple(ids),gen)],('persistent',case,gen,tokens2)
 code=0
except BaseException as e:
 emit('failure',error=repr(e),traceback=traceback.format_exc());traceback.print_exc()
finally:
 emit('terminal',exit=code);raw.close()
raise SystemExit(code)
