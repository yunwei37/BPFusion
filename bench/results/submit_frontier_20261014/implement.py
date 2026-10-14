import pathlib,subprocess
p=pathlib.Path(__file__).parent;r=pathlib.Path('/workspaces/repository')
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
for name in ['qwen_graph.cu','vllm_graph.cu']:
 f=r/'executor'/name;s=f.read_text();assert f.read_bytes()==(p/('original_'+name)).read_bytes()
 old='        io_progress(io_state);'
 new=old+'\n        // Let the kernel consume published I/O before admitting fresh model work.\n        if(c->retired==c->seen &&\n           io_load(io_state->ring.head)!=io_load(io_state->ring.tail))continue;'
 assert s.count(old)==1;s=s.replace(old,new,1);f.write_text(s);(p/('candidate_'+name)).write_text(s)
subprocess.run(['git','diff','--check'],cwd=r,check=True)
print(subprocess.check_output(['git','diff','--stat'],cwd=r,text=True))
