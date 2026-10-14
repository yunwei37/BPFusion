import os,subprocess,json,datetime
root=os.path.dirname(os.path.abspath(__file__))
records=[]
for name in ("qwen","smol"):
 print("HF_START",name,datetime.datetime.now(datetime.timezone.utc).isoformat(),flush=True)
 with open(root+"/"+name+".driver.stdout","w") as out,open(root+"/"+name+".driver.stderr","w") as err:
  p=subprocess.run(["/usr/bin/python3",root+"/driver.py",name],stdout=out,stderr=err)
 path=root+"/"+name+".results.json"
 r=json.load(open(path)) if os.path.exists(path) else {}
 records.append({"name":name,"exit":p.returncode,"pass":r.get("pass"),"error":r.get("error")})
 open(root+"/pipeline.status.json","w").write(json.dumps(records,indent=2))
 print(json.dumps(records[-1]),flush=True)
 if p.returncode or not r.get("pass"):break
print("HF_PIPELINE_TERMINAL",flush=True)
