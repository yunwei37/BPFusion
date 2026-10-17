
from pathlib import Path
import subprocess,re,json
t=Path(__file__).parent
def sass(path,kind="dispatch"):
 text=subprocess.check_output(["/usr/local/cuda/bin/cuobjdump","--dump-sass",str(path)],text=True)
 sections=text.split("Function : ")[1:]
 section=next(s for s in sections if kind in s.splitlines()[0])
 # Exact instruction/control encoding pairs, not a source/hash equality proxy.
 pairs=re.findall(r"/\*[0-9a-f]+\*/\s+.*?/\* (0x[0-9a-f]+) \*/\s*/\* (0x[0-9a-f]+) \*/",section)
 assert pairs
 return pairs,[s.splitlines()[0] for s in sections]
records={}
for banks in [8,16]:
 b=t/("kernel_network_sourcebuild"+str(banks));old=t/("kernel_owned_build"+str(banks))
 names={"candidate":"vllm_mixed_kernel_network","native":"vllm_mixed_user_network_wait","selected":"vllm_mixed_uring_loop","candidate_trace":"vllm_mixed_kernel_network_trace","native_trace":"vllm_mixed_user_network_wait_trace"}
 data={k:sass(b/(v+".so")) for k,v in names.items()}
 original=sass(old/"vllm_mixed_uring_loop.so")
 original_trace=sass(old/"vllm_mixed_uring_loop_trace.so")
 rec=dict(dispatch_instruction_counts={k:len(v[0]) for k,v in data.items()},
  ordinary_candidate_native_selected_equal=data["candidate"][0]==data["native"][0]==data["selected"][0],
  trace_candidate_native_equal=data["candidate_trace"][0]==data["native_trace"][0],
  candidate_equal_original_measured_candidate=data["candidate"][0]==original[0],
  candidate_trace_equal_original_qualified_candidate=data["candidate_trace"][0]==original_trace[0],
  candidate_no_io_network=not any("io_network" in name for name in data["candidate"][1]),
  selected_has_io_network=any("io_network" in name for name in data["selected"][1]))
 assert all(v for k,v in rec.items() if k!="dispatch_instruction_counts"),rec
 records[str(banks)]=rec
b=t/"kernel_network_sourcebuild8"
candidate=sass(b/"graph_server_kernel_network.so","graph_dispatch")
native=sass(b/"graph_server_user_network_wait.so","graph_dispatch")
original=sass(t/"kernel_network_graph8/graph_server_uring_loop.so","graph_dispatch")
records["opaque_graph_default8"]=dict(instruction_count=len(candidate[0]),candidate_native_equal=candidate[0]==native[0],candidate_equal_private_graph=candidate[0]==original[0],candidate_no_io_network=not any("io_network" in name for name in candidate[1]))
assert all(v for k,v in records["opaque_graph_default8"].items() if k!="instruction_count")
(t/"kernel_network_source_compiled_controls.json").write_text(json.dumps(records,indent=2))
print(json.dumps(records,indent=2))
