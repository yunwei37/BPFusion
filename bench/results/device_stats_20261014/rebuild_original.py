import pathlib,os,json,subprocess,shutil,datetime,re
repo=pathlib.Path('/workspaces/repository');os.chdir(repo);t=pathlib.Path(__file__).parent
env=dict(os.environ,**json.loads((t/'environment.json').read_text()))
d=t/'original/executor';d.mkdir(parents=True,exist_ok=True)
for name in ['io_uring_tcp.h','vllm_graph.cu']:
 source=(t/('original_'+name)).read_bytes()
 if not (d/name).exists() or (d/name).read_bytes()!=source:(d/name).write_bytes(source)
for name in ['vllm_graph']:
 old=repo/'build'/(name+'_uring_loop_coalesced_original.so')
 if old.exists():shutil.copy2(old,t/(name+'_original_before_rebuild.so'))
command=['make','-f',str(t/'Makefile.original'),'original-baselines','VLLM_PYTHON='+str(t/'runtime/bin/python')]
with (t/'original_rebuild.stdout').open('x') as out,(t/'original_rebuild.stderr').open('x') as err:
 r=subprocess.run(command,env=env,stdout=out,stderr=err)
receipt=dict(command=command,exit=r.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
(t/'original_rebuild.exit.json').write_text(json.dumps(receipt,indent=2))
if r.returncode:raise SystemExit(r.returncode)
def sass(path):
 raw=subprocess.check_output(['/usr/local/cuda/bin/cuobjdump','--dump-sass',str(path)],text=True)
 result={};name=None
 for line in raw.splitlines():
  if 'Function :' in line:name=line.split('Function :',1)[1].strip();result.setdefault(name,[])
  elif name and re.match(r'\s*/\*[0-9a-f]+\*/',line):
   instruction=re.sub(r'/\*.*?\*/','',line).strip()
   if instruction:result[name].append(instruction)
 return result
for name in ['vllm_graph']:
 before=t/(name+'_original_before_rebuild.so');after=repo/'build'/(name+'_uring_loop_coalesced_original.so')
 if not before.exists():
  receipt[name]=dict(fresh_original_snapshot_build=True)
  continue
 first=sass(before);second=sass(after)
 receipt[name]=dict(functions=len(first),instruction_lines=sum(map(len,first.values())),normalized_sass_equal=first==second)
 assert first==second,(name,[(k,len(v),len(second.get(k,[]))) for k,v in first.items() if v!=second.get(k)])
(t/'original_rebuild.exit.json').write_text(json.dumps(receipt,indent=2))
