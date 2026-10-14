import pathlib,subprocess,json,datetime
root=pathlib.Path('/tmp/bpfusion-optimized-latency-profile-bk8ztoin')
key='preflight_qwen_p0_profiled'
cmd=['/usr/bin/python3',str(root/'case.py'),'qwen','0','profiled','preflight']
with (root/(key+'.driver.stdout')).open('w') as a,(root/(key+'.driver.stderr')).open('w') as b:r=subprocess.run(cmd,stdout=a,stderr=b)
(root/(key+'.exit.json')).write_text(json.dumps(dict(cmd=cmd,exit=r.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
