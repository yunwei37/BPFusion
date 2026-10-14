import pathlib,subprocess,json,os,shutil,datetime
r=pathlib.Path('/workspaces/repository');p=pathlib.Path(__file__).parent;os.chdir(r)
assert json.loads((p/'setup.exit.json').read_text())['exit']==0
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()=='07ba7e042fe4c0488fafbc0c515eccf3234327d1'
for name in ['amk_graph','vllm_graph']:
 src=r/'build'/(name+'_uring_loop_coalesced.so');dst=r/'build'/(name+'_uring_loop_coalesced_original.so');shutil.copy2(src,dst)
 (r/'build'/(name+'_uring_loop_coalesced_original')).symlink_to(r/'executor'/(name+'.py'))
(p/'original_saved.json').write_text(json.dumps(dict(source='07ba7e042fe4c0488fafbc0c515eccf3234327d1',utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
env=dict(os.environ,**json.loads((p/'environment.json').read_text()))
commands=[['/usr/bin/python3',str(p/'rebuild_original.py')],['/usr/bin/python3',str(p/'implement.py')],['make','amk-graph-uring-coalesced','vllm-graph-uring-coalesced','VLLM_PYTHON='+str(p/'runtime/bin/python'),'AMK_PYTHON='+str(p/'runtime/bin/python')]]
for i,cmd in enumerate(commands):
 with (p/('candidate_step_'+str(i)+'.stdout')).open('x') as out,(p/('candidate_step_'+str(i)+'.stderr')).open('x') as err:q=subprocess.run(cmd,env=env,stdout=out,stderr=err)
 (p/('candidate_step_'+str(i)+'.exit.json')).write_text(json.dumps(dict(command=cmd,exit=q.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
 if q.returncode:raise SystemExit(q.returncode)
(p/'candidate_build.exit.json').write_text(json.dumps(dict(exit=0,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())))
