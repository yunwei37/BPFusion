import pathlib,subprocess
t=pathlib.Path(__file__).parent;r=pathlib.Path('/workspaces/repository')
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
f=r/'executor/vllm_graph.cu';assert f.read_bytes()==(t/'original_vllm_graph.cu').read_bytes()
s=f.read_text()
old='        // Let the kernel consume published I/O before admitting fresh model work.\n        if(c->retired==c->seen &&\n           io_load(io_state->ring.head)!=io_load(io_state->ring.tail))continue;'
new='        // Drain completed responses and published I/O before fresh model work.\n        if(c->retired==c->seen &&\n           (io_state->next_final!=c->retired ||\n            io_load(io_state->ring.head)!=io_load(io_state->ring.tail)))continue;'
assert s.count(old)==1
f.write_text(s.replace(old,new));(t/'candidate_vllm_graph.cu').write_bytes(f.read_bytes())
assert (r/'executor/qwen_graph.cu').read_bytes()==(t/'original_qwen_graph.cu').read_bytes()
subprocess.run(['git','diff','--check'],cwd=r,check=True)
print(subprocess.check_output(['git','diff','--stat'],cwd=r,text=True))
