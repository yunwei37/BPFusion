import datetime,json,os,subprocess
root=os.path.dirname(os.path.abspath(__file__))
record=[]
for name in ("qwen","smol"):
    cmd=["python3",root+"/driver.py",name]
    print("START",name,datetime.datetime.now(datetime.timezone.utc).isoformat(),flush=True)
    with open(root+"/"+name+".driver.stdout","w") as out,open(root+"/"+name+".driver.stderr","w") as err:
        p=subprocess.run(cmd,stdout=out,stderr=err,text=True)
    r=json.load(open(root+"/"+name+".results.json"))
    record.append({"name":name,"cmd":cmd,"exit":p.returncode,"pass":r.get("pass"),"error":r.get("error")})
    print(json.dumps(record[-1]),flush=True)
    if p.returncode or not r.get("pass"):break
open(root+"/pipeline.status.json","w").write(json.dumps(record,indent=2))
print("MODEL_PIPELINE_TERMINAL",flush=True)
