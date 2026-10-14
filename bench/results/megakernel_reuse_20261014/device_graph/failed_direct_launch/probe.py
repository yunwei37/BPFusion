import pathlib,sys,json,ctypes,datetime,traceback
r=pathlib.Path(__file__).resolve().parents[1];d=r/'device_graph'
sys.path.insert(0,str(r/'AutoMegaKernel-884534c4d2dbed4381576f81a79ae97feca53c34'))
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
from vm.loader import MegakernelVM
from vm.loader_persist import PersistentDecodeVM
cfg=json.loads((r/'smol_frozen.json').read_text())
pool={(tuple(x['prompt']),x['gen']):{tuple(y) for y in x['sequences']} for x in cfg['frozen_model']['references']}
raw=(d/'raw.jsonl').open('x',buffering=1)
def emit(event,**fields):
 raw.write(json.dumps(dict(event=event,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),**fields))+'\n')
 print(event,fields.get('case',''),fields.get('gen',''),fields.get('flags',''),flush=True)
lib=ctypes.CDLL(str(d/'graph_bridge.so'))
lib.bridge_create.argtypes=[ctypes.c_char_p,ctypes.POINTER(ctypes.c_int64),ctypes.c_void_p,ctypes.POINTER(ctypes.c_void_p)]
lib.bridge_run.argtypes=[ctypes.c_void_p,ctypes.c_void_p]
lib.bridge_destroy.argtypes=[ctypes.c_void_p]
lib.bridge_args_size.restype=ctypes.c_size_t
lib.bridge_stage.restype=ctypes.c_char_p
assert lib.bridge_args_size()==24*8
emit('metadata',checkpoint=cfg['model'],source_revision='884534c4d2dbed4381576f81a79ae97feca53c34',torch=torch.__version__,cuda=torch.version.cuda,precision='FP16',knobs={'cpasync':0},frozen_model=cfg['frozen_model'],bridge_source=(d/'graph_bridge.cu').read_text(),probe_source=pathlib.Path(__file__).read_text(),cubin=str(d/'amk_persist_ext_sm120.1.sm_120.cubin'))
code=1
try:
 model=AutoModelForCausalLM.from_pretrained(cfg['model'],dtype=torch.float16).eval()
 graph=from_hf(model);weights=weights_from_hf(model);target=TARGETS['rtx5090']
 for case,ids in enumerate(cfg['prompts']):
  emit('prepare',case=case)
  base=len(ids)-1;kv={}
  for pos,token in enumerate(ids[:-1]):
   vm=MegakernelVM(lower(graph,target=target,pos=pos,dtype=DType.F16),weights,device='cuda',knobs={'cpasync':0})
   out=vm.run({TOKEN_NAME:torch.tensor([token],dtype=torch.int32,device='cuda'),POS_NAME:torch.tensor([pos],dtype=torch.int32,device='cuda'),RESHAPE_ID_NAME:torch.tensor([0],dtype=torch.int32,device='cuda')},kv=kv)
   kv={b.name:out[b.name] for b in vm.prog.buffers if b.kind==BufferKind.KV_CACHE and b.name in out}
  pvm=PersistentDecodeVM(lower(graph,target=target,pos=base,dtype=DType.F16),weights,device='cuda')
  initial=pvm.decode(ids[-1],base,1,kv=kv)
  assert tuple(initial['tokens']) in pool[(tuple(ids),1)]
  b=pvm.base_vm;la=list(b._launch_args);la[9]=b.num_sms
  output=torch.full((64,),-1,dtype=torch.int32,device='cuda')
  flags=torch.zeros(3,dtype=torch.int32,device='cuda')
  args=(ctypes.c_int64*24)(*(la+[1,0,b._buf_tensor[pvm._pos_bid].data_ptr(),b._buf_tensor[pvm._token_bid].data_ptr(),la[0],pvm._logits_bid,output.data_ptr(),0]))
  handle=ctypes.c_void_p()
  torch.cuda.synchronize()
  status=lib.bridge_create(str(d/'amk_persist_ext_sm120.1.sm_120.cubin').encode(),args,flags.data_ptr(),ctypes.byref(handle))
  emit('create',case=case,status=status,stage=lib.bridge_stage().decode(),grid=b.grid_dim,threads=b.threads_per_block)
  assert status==0
  try:
   for gen in [1,64]:
    for name,t in b._kv_tensors.items():
     if name in kv:t.copy_(kv[name])
    b._counters.zero_();b._abort.zero_();output.fill_(-1);flags.zero_()
    inputs=torch.tensor([ids[-1],base,gen],dtype=torch.int32,device='cuda')
    torch.cuda.synchronize()
    emit('start',case=case,gen=gen,input_values=[ids[-1],base,gen],initial_graph_values=[0,0,1])
    status=lib.bridge_run(handle,inputs.data_ptr())
    actual=output[:gen].cpu().tolist();actual_flags=flags.cpu().tolist()
    emit('output',case=case,gen=gen,status=status,flags=actual_flags,tokens=actual,matches_frozen=tuple(actual) in pool[(tuple(ids),gen)])
    assert status==0 and actual_flags==[0,1,1]
    assert tuple(actual) in pool[(tuple(ids),gen)]
  finally:lib.bridge_destroy(handle)
 code=0
except BaseException as e:
 emit('failure',error=repr(e),traceback=traceback.format_exc());traceback.print_exc()
finally:
 emit('terminal',exit=code);raw.close()
raise SystemExit(code)
