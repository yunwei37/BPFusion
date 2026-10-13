import datetime,importlib.util,json,os,subprocess,torch
os.chdir("/workspaces/repository")
root=os.path.dirname(os.path.abspath(__file__))
spec=importlib.util.spec_from_file_location("original_graph","/workspaces/repository/executor/qwen_graph.py")
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
prompts=[list(range(77+i,77+i+n)) for i,n in enumerate([1,2,5,8,16,31,63,64,2,5,8,1])]
paths=json.load(open(root+"/model_paths.json"))
record={"started":datetime.datetime.now(datetime.timezone.utc).isoformat(),"torch":torch.__version__,"models":{}}
for name,path in paths.items():
    with torch.no_grad():
        model=module.load_model(path)
        rows=[]
        for prompt in prompts:
            ids=torch.tensor([prompt],device="cuda",dtype=torch.long)
            logits=model(input_ids=ids,use_cache=False).logits
            token=int(logits[0,-1].argmax().item())
            rows.append({"prompt":prompt,"gen":1,"tokens":[token]})
        record["models"][name]={"path":path,"dtype":str(model.dtype),"rows":rows}
        del model
        torch.cuda.empty_cache()
    print("ORACLE",name,len(rows),flush=True)
record["frozen_at"]=datetime.datetime.now(datetime.timezone.utc).isoformat()
open(root+"/oracle.json","w").write(json.dumps(record,indent=2))
print("ORACLE_COMPLETE",flush=True)
