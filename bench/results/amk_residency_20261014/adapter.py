#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Bootstrap upstream AMK graphs for the existing GPU request dispatcher."""
import argparse,ctypes,dataclasses,json,os,pathlib,subprocess,sys,tempfile
import torch

profile_enabled=os.environ.get('BF_DIAGNOSTIC_PROFILE')=='1'
cupti_path=next(line.rsplit(None,1)[-1] for line in pathlib.Path('/proc/self/maps').read_text().splitlines() if 'libcupti.so' in line)
cupti=ctypes.CDLL(cupti_path)
driver=ctypes.CDLL('libcuda.so.1')
if profile_enabled:
 assert not torch.cuda.is_initialized()
 cupti.cuptiActivityEnableDeviceGraph.argtypes=[ctypes.c_uint8]
 cupti.cuptiActivityEnableHWTrace.argtypes=[ctypes.c_uint8]
 device_status=cupti.cuptiActivityEnableDeviceGraph(1)
 driver_status=driver.cuInit(0)
 hardware_status=cupti.cuptiActivityEnableHWTrace(1)
 print('CUPTI_SETUP',json.dumps(dict(library=cupti_path,device_graph_status=device_status,driver_status=driver_status,hardware_trace_status=hardware_status)),flush=True)
 assert device_status==driver_status==hardware_status==0

def catalogue_graph(handle,bank,index,start,length,geometry):
 driver.cuGraphGetNodes.argtypes=[ctypes.c_void_p,ctypes.POINTER(ctypes.c_void_p),ctypes.POINTER(ctypes.c_size_t)]
 driver.cuGraphNodeGetDependencies_v2.argtypes=[ctypes.c_void_p,ctypes.POINTER(ctypes.c_void_p),ctypes.c_void_p,ctypes.POINTER(ctypes.c_size_t)]
 driver.cuGraphNodeGetType.argtypes=[ctypes.c_void_p,ctypes.POINTER(ctypes.c_int)]
 driver.cuGraphKernelNodeGetAttribute.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_void_p]
 cupti.cuptiGetGraphNodeId.argtypes=[ctypes.c_void_p,ctypes.POINTER(ctypes.c_uint64)]
 n=ctypes.c_size_t()
 assert driver.cuGraphGetNodes(handle,None,ctypes.byref(n))==0
 nodes=(ctypes.c_void_p*n.value)()
 assert driver.cuGraphGetNodes(handle,nodes,ctypes.byref(n))==0
 remaining=set(nodes);dependencies={}
 for node in nodes:
  count=ctypes.c_size_t()
  assert driver.cuGraphNodeGetDependencies_v2(node,None,None,ctypes.byref(count))==0
  deps=(ctypes.c_void_p*count.value)()
  edge_data=(ctypes.c_uint8*(8*count.value))()
  result=driver.cuGraphNodeGetDependencies_v2(node,deps,edge_data,ctypes.byref(count)) if count.value else 0
  assert result==0,(bank,index,node,result,count.value)
  dependencies[node]=set(deps)
 ordered=[]
 while remaining:
  roots=[x for x in remaining if not dependencies[x]&remaining]
  assert len(roots)==1,(bank,index,roots)
  ordered+=roots;remaining.remove(roots[0])
 models=[];all_nodes=[]
 for node in ordered:
  kind=ctypes.c_int();assert driver.cuGraphNodeGetType(node,ctypes.byref(kind))==0
  identifier=ctypes.c_uint64();assert cupti.cuptiGetGraphNodeId(node,ctypes.byref(identifier))==0
  # cuda.h: CUkernelNodeAttrValue is a union; cooperative is its leading int.
  storage=(ctypes.c_uint64*32)()
  assert kind.value==0 and driver.cuGraphKernelNodeGetAttribute(node,2,ctypes.byref(storage))==0
  coop=ctypes.cast(storage,ctypes.POINTER(ctypes.c_int)).contents.value
  record=dict(node_id=identifier.value,cooperative=coop)
  if coop:record['position']=start+len(models);models.append(record)
  all_nodes.append(record)
 assert len(models)==length and len(all_nodes)==2*length+1
 return dict(bank=bank,index=index,start=start,count=length,geometry=geometry,nodes=all_nodes,model_nodes=models)
import torch.utils.cpp_extension as cpp
# Let the installed PyTorch choose the host C++ standard. CUDA flags are unchanged.
original_load=cpp.load
def compatible_load(*args,**kwargs):
 if kwargs.get('extra_cflags'):
  kwargs['extra_cflags']=[x for x in kwargs['extra_cflags'] if not x.startswith('-std=')]
 return original_load(*args,**kwargs)
cpp.load=compatible_load
from transformers import AutoModelForCausalLM
from schedule.ir import DType,TARGETS
from schedule.graph import from_hf,weights_from_hf
from schedule.lower import lower
from vm.loader_persist import PersistentDecodeVM

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument('model');ap.add_argument('seconds',type=int,nargs='?',default=60)
 args=ap.parse_args()
 repo=pathlib.Path('/workspaces/repository');os.chdir(repo)
 entry=pathlib.Path(sys.argv[0]).absolute()
 library=entry.with_suffix('.so') if entry.name.startswith('amk_graph') and entry.suffix!='.py' else repo/'build/amk_graph_uring_loop.so'
 serving=ctypes.CDLL(str(library))
 serving.max_tokens.restype=serving.max_requests.restype=ctypes.c_uint
 limit=serving.max_tokens();bank_count=serving.max_requests();count=3*limit-1
 bridge=ctypes.CDLL(str(repo/'build/amk_graph_builder.so'))
 bridge.amk_args_size.restype=ctypes.c_size_t;assert bridge.amk_args_size()==24*8
 bridge.amk_stage.restype=ctypes.c_char_p
 bridge.amk_open.argtypes=[ctypes.c_char_p,ctypes.POINTER(ctypes.c_void_p)]
 bridge.amk_close.argtypes=[ctypes.c_void_p]
 bridge.amk_graph_create.argtypes=[ctypes.c_void_p,ctypes.POINTER(ctypes.c_int64),ctypes.c_void_p,ctypes.c_uint,ctypes.c_uint,ctypes.c_void_p,ctypes.c_void_p,ctypes.POINTER(ctypes.c_void_p)]
 bridge.amk_graph_destroy.argtypes=[ctypes.c_void_p]
 model=AutoModelForCausalLM.from_pretrained(args.model,dtype=torch.float16).eval()
 graph=from_hf(model);weights=weights_from_hf(model)
 prop=torch.cuda.get_device_properties(0)
 # Upstream's named rtx5090 target describes an82-SM laptop. Discover this card.
 target=dataclasses.replace(TARGETS['rtx5090'],num_sms=prop.multi_processor_count)
 program=lower(graph,target=target,pos=0,dtype=DType.F16)
 banks=[];raw=[];outputs=[];inputs=[];modules=[];graphs=[];catalogue=[]
 try:
  for bank in range(bank_count):
   vm=PersistentDecodeVM(program,weights,device='cuda')
   vm.decode(0,0,1)
   base=vm.base_vm;la=list(base._launch_args);la[9]=base.num_sms
   token=torch.zeros(1,dtype=torch.int32,device='cuda')
   selected=torch.zeros(1,dtype=torch.int64,device='cuda')
   prompt=torch.zeros(limit,dtype=torch.int64,device='cuda')
   error=torch.zeros(1,dtype=torch.int32,device='cuda')
   arguments=(ctypes.c_int64*24)(*(la+[1,0,base._buf_tensor[vm._pos_bid].data_ptr(),base._buf_tensor[vm._token_bid].data_ptr(),la[0],vm._logits_bid,token.data_ptr(),0]))
   with tempfile.TemporaryDirectory(prefix='bpfusion-amk-cubin-') as temporary:
    subprocess.run(['/usr/local/cuda/bin/cuobjdump','--extract-elf','all',vm.ext.__file__],cwd=temporary,check=True,stdout=subprocess.DEVNULL)
    cubins=list(pathlib.Path(temporary).glob('*.cubin'));chosen=None
    for cubin in cubins:
     dump=subprocess.check_output(['/usr/local/cuda/bin/cuobjdump','--dump-elf-symbols',str(cubin)],text=True)
     if 'STO_ENTRY      amk_megakernel_persist' in dump:chosen=cubin;break
    assert chosen is not None,'upstream persistent kernel cubin missing'
    module=ctypes.c_void_p();status=bridge.amk_open(str(chosen).encode(),ctypes.byref(module));assert status==0,('module',status)
   modules.append(module);raw.append(0);outputs.append(0)
   for index in range(1,count):
    start=0 if index<=limit else index-limit
    length=index if index<=limit else 1
    handle=ctypes.c_void_p()
    status=bridge.amk_graph_create(module,arguments,prompt.data_ptr(),start,length,selected.data_ptr(),error.data_ptr(),ctypes.byref(handle))
    assert status==0,(bank,index,status,bridge.amk_stage().decode())
    graphs.append(handle);raw.append(handle.value);outputs.append(selected.data_ptr())
    if profile_enabled:catalogue.append(catalogue_graph(handle,bank,index,start,length,dict(grid=la[13],block=la[14],dynamic_shared=la[15])))
   inputs.append(prompt.data_ptr());banks.append((vm,token,selected,prompt,error))
   print('AMK_BANK',bank,'graphs',count-1,'grid',base.grid_dim,'sms',base.num_sms,flush=True)
  print(json.dumps(dict(event='amk_bootstrap',model=args.model,precision='FP16',banks=bank_count,graphs_per_bank=count-1,context=2*limit,actual_sms=prop.multi_processor_count,program_sms=target.num_sms,knobs={'cpasync':0},protocol='unchanged binary token HTTP',compute='upstream AMK persistent kernel; GPU graph prefill/decode')),flush=True)
  if profile_enabled:
   (entry.parent/'graph_catalogue.json').write_text(json.dumps(catalogue))
  ptr=ctypes.POINTER(ctypes.c_ulonglong)
  serving.serve.argtypes=[ptr,ptr,ctypes.c_uint,ptr]+[ctypes.c_uint]*4
  serving.serve.restype=ctypes.c_int
  if profile_enabled:
   with torch.profiler.profile(activities=[torch.profiler.ProfilerActivity.CPU,torch.profiler.ProfilerActivity.CUDA]) as profile:
    status=serving.serve((ctypes.c_ulonglong*len(raw))(*raw),(ctypes.c_ulonglong*len(outputs))(*outputs),count,(ctypes.c_ulonglong*len(inputs))(*inputs),model.config.vocab_size,model.config.num_hidden_layers,model.config.hidden_size,args.seconds)
   profile.export_chrome_trace(str(entry.parent/'trace.json.gz'))
   print('TRACE_EXPORTED',str(entry.parent/'trace.json.gz'),flush=True)
  else:
   status=serving.serve((ctypes.c_ulonglong*len(raw))(*raw),(ctypes.c_ulonglong*len(outputs))(*outputs),count,(ctypes.c_ulonglong*len(inputs))(*inputs),model.config.vocab_size,model.config.num_hidden_layers,model.config.hidden_size,args.seconds)
  errors=[b[4].cpu().item() for b in banks]
  print(json.dumps(dict(event='amk_graph_errors',errors=errors)),flush=True)
  assert status==0 and not any(errors),(status,errors)
 finally:
  torch.cuda.synchronize()
  for handle in graphs:bridge.amk_graph_destroy(handle)
  for module in modules:bridge.amk_close(module)
if __name__=='__main__':main()
