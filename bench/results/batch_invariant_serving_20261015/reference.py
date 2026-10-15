import os,sys,json,math,pathlib,datetime
t=pathlib.Path(__file__).resolve().parent;r=pathlib.Path('/workspaces/repository')
import torch
from vllm import LLM,SamplingParams
from transformers import AutoTokenizer,AutoConfig
from vllm.v1.worker.gpu_worker import Worker
from vllm.v1.kv_cache_interface import FullAttentionSpec
from vllm.model_executor.determinism import batch_invariant as bi
assert os.environ['VLLM_BATCH_INVARIANT']=='1'
key=sys.argv[1];asset=json.loads((r/'bench/results/output_publication_20261015/frozen_references.json').read_text());model=asset['models'][key]['model']
tokenizer=AutoTokenizer.from_pretrained(model);cfg=AutoConfig.from_pretrained(model)
prompts=[tokenizer(x).input_ids for x in ("The capital of France is","What is 2 plus 2?","Write a short greeting.","Linux is")]
cases=prompts+[(prompts[0]*math.ceil(n/len(prompts[0])))[:n] for n in (1,15,16,17,32,64)]
original=Worker.determine_available_memory
def queue_memory(worker):
 specs=worker.get_kv_cache_spec();assert specs and all(type(x) is FullAttentionSpec for x in specs.values())
 sizes={x.block_size for x in specs.values()};assert len(sizes)==1
 needed=1+8*math.ceil(128/next(iter(sizes)));worker.cache_config.kv_cache_memory_bytes=needed*sum(x.page_size_bytes for x in specs.values())
 print(json.dumps(dict(event='reference_cache',needed_blocks=needed,cache_bytes=worker.cache_config.kv_cache_memory_bytes)),flush=True)
 return original(worker)
Worker.determine_available_memory=queue_memory
try:llm=LLM(model=model,dtype='half',max_model_len=128)
finally:Worker.determine_available_memory=original
assert bi._batch_invariant_MODE
raw=(t/(key+'.official.jsonl')).open('x',buffering=1)
def emit(**d):raw.write(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),**d))+'\n')
emit(event='metadata',model=model,precision='fp16',cases=cases,source='official LLM.generate before observing BPFusion',batch_invariant_enabled=bi._batch_invariant_MODE,settings={k:os.environ.get(k) for k in ['VLLM_BATCH_INVARIANT','CUBLAS_WORKSPACE_CONFIG','CUBLASLT_WORKSPACE_SIZE','VLLM_USE_BREAKABLE_CUDAGRAPH','VLLM_USE_AOT_COMPILE']})
references={}
def generate(ids,gen,label):
 params=SamplingParams(temperature=0,ignore_eos=True,max_tokens=gen,detokenize=False)
 results=llm.generate([dict(prompt_token_ids=x) for x in ids],params,use_tqdm=False)
 assert len(results)==len(ids)
 for prompt,result in zip(ids,results):
  tokens=result.outputs[0].token_ids
  emit(event='generation',condition=label,batch=len(ids),gen=gen,prompt=prompt,tokens=tokens)
  assert len(tokens)==gen
  if label=='serial64':references[tuple(prompt)]=tokens
  else:assert tokens==references[tuple(prompt)][:gen],('official batch invariance mismatch',label,len(ids),gen,prompt,tokens,references[tuple(prompt)][:gen])
for prompt in cases:generate([prompt],64,'serial64')
for gen in [1,64]:
 for width in range(1,9):
  for order in ['forward','reverse']:
   selected=cases if order=='forward' else cases[::-1]
   selected=(selected*math.ceil((math.ceil(len(selected)/width)*width)/len(selected)))[:math.ceil(len(selected)/width)*width]
   for pos in range(0,len(selected),width):generate(selected[pos:pos+width],gen,order)
emit(event='terminal',exit_code=0,unique_prompts=len(references))
raw.close()
frozen=dict(model=model,vocab=cfg.vocab_size,precision='fp16',references=[dict(prompt=list(ids),gen=gen,sequences=[tokens[:gen]]) for ids,tokens in references.items() for gen in [1,64]])
(t/(key+'.frozen.json')).write_text(json.dumps(frozen,indent=2))
