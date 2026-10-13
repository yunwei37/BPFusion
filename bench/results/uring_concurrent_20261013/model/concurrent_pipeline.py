import os,subprocess,json,datetime
root=os.path.dirname(os.path.abspath(__file__))
records=[]
for name in ("qwen","smol"):
 print("START",name,datetime.datetime.now(datetime.timezone.utc).isoformat(),flush=True)
 with open(root+"/"+name+".concurrent.driver.stdout","w") as out,open(root+"/"+name+".concurrent.driver.stderr","w") as err:
  p=subprocess.run(["python3",root+"/driver.py",name,"concurrent"],stdout=out,stderr=err,text=True)
 path=root+"/"+name+".concurrent.results.json"
 r=json.load(open(path)) if os.path.exists(path) else {}
 records.append({"name":name,"exit":p.returncode,"pass":r.get("pass"),"error":r.get("error"),"result_present":os.path.exists(path)})
 print(json.dumps(records[-1]),flush=True)
 if p.returncode or not r.get("pass"):break
open(root+"/concurrent.pipeline.status.json","w").write(json.dumps(records,indent=2))
print("CONCURRENT_PIPELINE_TERMINAL",flush=True)
