import datetime,importlib.util,json,os,torch
os.chdir("/workspaces/repository");root=os.path.dirname(os.path.abspath(__file__))
spec=importlib.util.spec_from_file_location("original_graph","/workspaces/repository/executor/qwen_graph.py")
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
prompts=[list(range(77+i,77+i+n)) for i,n in enumerate([1,2,5,8,16,31,63,64,2,5,8,1])]
paths=json.load(open(root+"/model_paths.json"))
record={"started":datetime.datetime.now(datetime.timezone.utc).isoformat(),"torch":torch.__version__,"models":{}}
for name,path in paths.items():
    rows=[]
    with torch.no_grad():
        model=module.load_model(path)
        for i,prompt in enumerate(prompts):
            gen=[1,64,1,64,64,1,64,64,1,1,1,64][i]
            ids=torch.tensor([prompt],device="cuda",dtype=torch.long)
            cache=None;tokens=[]
            for step in range(gen):
                result=model(input_ids=ids,past_key_values=cache,use_cache=True,logits_to_keep=1)
                token=int(result.logits[0,-1].argmax().item());tokens.append(token)
                cache=result.past_key_values;ids=torch.tensor([[token]],device="cuda",dtype=torch.long)
            rows.append({"prompt":prompt,"gen":gen,"tokens":tokens})
        record["models"][name]={"path":path,"dtype":str(model.dtype),"rows":rows}
        del model,cache,result,ids
        torch.cuda.empty_cache()
    print("ORACLE",name,"requests",len(rows),"tokens",sum(len(r["tokens"]) for r in rows),flush=True)
record["frozen_at"]=datetime.datetime.now(datetime.timezone.utc).isoformat()
open(root+"/oracle.json","w").write(json.dumps(record,indent=2))
print("ORACLE_COMPLETE",flush=True)
