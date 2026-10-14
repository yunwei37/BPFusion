import pathlib,os,json,subprocess,shutil,datetime
repo=pathlib.Path('/workspaces/repository');os.chdir(repo);t=pathlib.Path(__file__).parent
env=dict(os.environ,**json.loads((t/'environment.json').read_text()))
command=['make','build/vllm_graph_uring_loop.so','build/vllm_graph_user_network_wait.so','build/vllm_graph_uring_loop','build/vllm_graph_user_network_wait','VLLM_PYTHON='+str(t/'runtime/bin/python')]
with (t/'original_build.stdout').open('x') as out,(t/'original_build.stderr').open('x') as err:
 r=subprocess.run(command,env=env,stdout=out,stderr=err)
(t/'original_build.exit.json').write_text(json.dumps(dict(command=command,exit=r.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())))
if r.returncode:raise SystemExit(r.returncode)
for name in ['amk_graph','vllm_graph']:
 original=repo/'build'/(name+'_uring_loop.so');saved=repo/'build'/(name+'_uring_loop_original.so')
 assert not saved.exists();shutil.copy2(original,saved)
 entry=saved.with_suffix('');entry.symlink_to(repo/'executor'/(name+'.py'))
(t/'original_saved.json').write_text(json.dumps(dict(source=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),libraries=['build/amk_graph_uring_loop_original.so','build/vllm_graph_uring_loop_original.so'],source_snapshots=['original_io_uring_tcp.h','original_qwen_graph.cu','original_vllm_graph.cu','original_Makefile']),indent=2))
