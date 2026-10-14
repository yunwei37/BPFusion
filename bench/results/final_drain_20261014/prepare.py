import pathlib,subprocess,json,os,shutil,datetime
r=pathlib.Path('/workspaces/repository');t=pathlib.Path(__file__).parent;os.chdir(r)
assert json.loads((t/'setup.exit.json').read_text())['exit']==0
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],text=True).strip()=='main'
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()=='f232b475a4663731636067c0d2a95fc52603cd82'
assert (r/'executor/vllm_graph.cu').read_bytes()==(t/'original_vllm_graph.cu').read_bytes()
src=r/'build/vllm_graph_uring_loop_coalesced.so';dst=r/'build/vllm_graph_uring_loop_coalesced_original.so';assert not dst.exists();shutil.copy2(src,dst)
entry=r/'build/vllm_graph_uring_loop_coalesced_original';assert not entry.exists() and not entry.is_symlink();entry.symlink_to(r/'executor/vllm_graph.py')
(t/'original_saved.json').write_text(json.dumps(dict(source='f232b475a4663731636067c0d2a95fc52603cd82',utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
env=dict(os.environ,**json.loads((t/'environment.json').read_text()))
commands=[['/usr/bin/python3',str(t/'rebuild_original.py')],['/usr/bin/python3',str(t/'implement.py')],['make','vllm-graph-uring-coalesced','VLLM_PYTHON='+str(t/'runtime/bin/python')]]
for i,cmd in enumerate(commands):
 with (t/('candidate_step_'+str(i)+'.stdout')).open('x') as out,(t/('candidate_step_'+str(i)+'.stderr')).open('x') as err:p=subprocess.run(cmd,cwd=r,env=env,stdout=out,stderr=err)
 (t/('candidate_step_'+str(i)+'.exit.json')).write_text(json.dumps(dict(command=cmd,exit=p.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
 if p.returncode:raise SystemExit(p.returncode)
(t/'candidate_build.exit.json').write_text(json.dumps(dict(exit=0,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
