import datetime,json,os,subprocess
root=os.path.dirname(os.path.abspath(__file__))
record=[]
for name in ("qwen","smol"):
 print("START",name,datetime.datetime.now(datetime.timezone.utc).isoformat(),flush=True)
 with open(root+"/"+name+".driver.stdout","w") as out,open(root+"/"+name+".driver.stderr","w") as err:
  p=subprocess.run(["python3",root+"/driver.py",name],stdout=out,stderr=err,text=True)
 path=root+"/"+name+".results.json"
 r=json.load(open(path)) if os.path.exists(path) else {}
 record.append({"name":name,"exit":p.returncode,"pass":r.get("pass"),"error":r.get("error"),"result_present":os.path.exists(path)})
 print(json.dumps(record[-1]),flush=True)
 if p.returncode or not r.get("pass"):break
open(root+"/pipeline.status.json","w").write(json.dumps(record,indent=2))
print("STREAMING_PIPELINE_TERMINAL",flush=True)
