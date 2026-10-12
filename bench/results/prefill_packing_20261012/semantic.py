#!/usr/bin/env python3
"""Compare real hidden states for left-padding versus compact varlen metadata."""
import argparse,ctypes,inspect,json,os,runpy,sys,traceback
from pathlib import Path
import torch
ap=argparse.ArgumentParser();ap.add_argument("model");ap.add_argument("output");args=ap.parse_args()
root=Path("/workspaces/repository");out=Path(args.output);raw=out.open("w",buffering=1)
def emit(event,**kw):raw.write(json.dumps(dict(event=event,**kw))+"\n")
original=ctypes.CDLL
class ServeProbe:
 def __call__(self,*unused):
  local=inspect.currentframe().f_back.f_locals
  runner=local["runner"];buf=local["buf"];bt=local["bt"];graphs=local["graphs"];pages=local["pages"];rows=local["rows"];managers=local["managers"]
  from vllm.v1.worker.gpu.sample.gumbel import gumbel_sample
  from transformers import AutoTokenizer
  tok=AutoTokenizer.from_pretrained(args.model)
  prompts=[tok(text).input_ids for text in ("The capital of France is","What is 2 plus 2?","Write a short greeting.","Linux is")]
  pattern=prompts[0];edges=[(pattern*((n+len(pattern)-1)//len(pattern)))[:n] for n in (1,15,16,17,32,64)]
  cases=prompts+edges
  groups=[cases[:4]*2,edges+[prompts[3],prompts[1]]]+[cases[:batch] for batch in range(1,9)]
  passed=True
  with torch.inference_mode():
   for index,group in enumerate(groups):
    batch=len(group);query=max(map(len,group));count=batch*query
    hidden=[];tokens=[]
    for padded in (True,False):
     ids=[];positions=[];slots=[];padding=[];starts=[0];real_indices=[];last_indices=[]
     for row,prompt in enumerate(group):
      n=len(prompt);pad=query-n if padded else 0
      begin=len(ids)
      ids+=[0]*pad+prompt;positions+=[0]*pad+list(range(n));padding+=[True]*pad+[False]*n
      slots+=[-1]*pad+[rows[row][p//bt.kernel_block_sizes[0]]*bt.kernel_block_sizes[0]+p%bt.kernel_block_sizes[0] for p in range(n)]
      real_indices.extend(range(begin+pad,begin+pad+n));last_indices.append(begin+pad+n-1);starts.append(len(ids))
      bt.input_block_tables[0][row,:pages.shape[1]].copy_(pages[row])
     trailing=count-len(ids)
     ids+=[0]*trailing;positions+=[0]*trailing;slots+=[-1]*trailing;padding+=[True]*trailing
     buf.input_ids[:count].copy_(torch.tensor(ids,dtype=torch.int32,device="cuda"))
     buf.positions[:count].copy_(torch.tensor(positions,dtype=torch.int64,device="cuda"))
     buf.seq_lens[:batch].copy_(torch.tensor(list(map(len,group)),dtype=torch.int32,device="cuda"))
     buf.query_start_loc[:batch+1].copy_(torch.tensor(starts,dtype=torch.int32,device="cuda"))
     buf.is_padding[:count].copy_(torch.tensor(padding,dtype=torch.bool,device="cuda"))
     bt.slot_mappings[0,:count].copy_(torch.tensor(slots,dtype=torch.int64,device="cuda"))
     graphs[query*local["banks"]+batch-1][0].replay()
     hs=managers[query-1].hidden_states
     real=hs[torch.tensor(real_indices,device="cuda")].clone()
     last=hs[torch.tensor(last_indices,device="cuda")].clone()
     logits=runner.get_model().compute_logits(last)
     sampled=gumbel_sample(logits,torch.arange(batch,dtype=torch.int32,device="cuda"),
      torch.zeros(batch,device="cuda"),torch.zeros(batch,dtype=torch.int64,device="cuda"),
      torch.tensor([len(p)-1 for p in group],dtype=torch.int64,device="cuda"),
      apply_temperature=False,is_drafting=False)
     hidden.append(real.cpu());tokens.append(sampled.cpu().tolist())
    finite=all(bool(torch.isfinite(h).all()) for h in hidden);equal=torch.equal(hidden[0].view(torch.int16),hidden[1].view(torch.int16))
    close=True;error=None
    try:torch.testing.assert_close(hidden[0],hidden[1])
    except AssertionError as exc:close=False;error=str(exc)
    emit("group",index=index,batch=batch,query=query,prompt_lengths=list(map(len,group)),
     active_elements=hidden[0].numel(),finite=finite,bit_identical=equal,torch_default_close=close,
     max_abs_diff=float((hidden[0].float()-hidden[1].float()).abs().max()),padded_tokens=tokens[0],compact_tokens=tokens[1],error=error)
    passed=passed and finite and close
  emit("verified",groups=len(groups),passed=passed);return 0 if passed else 1
class ProbeLibrary(original):
 def __init__(self,path,*a,**kw):
  super().__init__(path,*a,**kw)
  if str(path).endswith("/build/vllm_graph.so"):self.serve=ServeProbe()
ctypes.CDLL=ProbeLibrary
emit("metadata",model=args.model,source=Path(__file__).read_text(),backend_source=(root/"executor/vllm_graph.py").read_text(),
 semantics="same captured total token shape; padded real rows versus compact actual cu_query_lens with trailing ignored slots",
 tolerance="torch.testing.assert_close defaults for fp16; no tolerance adjustment")
code=1
try:
 sys.argv=[str(root/"executor/vllm_graph.py"),args.model]
 runpy.run_path(str(root/"executor/vllm_graph.py"),run_name="__main__");code=0
except BaseException as exc:emit("failure",kind=type(exc).__name__,message=str(exc),traceback=traceback.format_exc());traceback.print_exc()
finally:emit("terminal",exit_code=code);raw.close()
sys.exit(code)
