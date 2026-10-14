# Full-run execution notes
Frozen source9b3cf6a, unchanged ordinary vllm_graph_uring_loop.so inode265295.
The first ordinary Qwen case is followed by a Windows observer launch-script
NameError (undeclared a while constructing a wrapper) before the next model
process starts. The observation helper is corrected to write a literal wrapper.
No benchmark cell, model process, prompt, oracle or analyzer changes/restarts.
All planned20 cases subsequently end with actual driver and model exits0.
Before/after every executor actual fleet SSH host kernel/GPU/memory observations
are saved. NVRM unsupported-reference warnings remain visible; no Xid/new
OOM/storage/BUG or recovery action is observed in these discrete brackets.
This is not proof of continuous isolation or of harmlessness of those warnings.
No sample/case is excluded. Ordinary and profiled conditions use one actual
ordinary library with source-native requests and fixed outputs.

Archive replay requires trace path relocation after TEMP removal. The analyzer
now prefers each raw case's adjacent archived trace. Initial replay fails by
selecting its own derived .timeline.jsonl as raw input; skip only those derived
files. The failed replay is retained, the final full replay exits0 and stdout
matches original analysis byte-for-byte. No timing cell/oracle/metric changed.
