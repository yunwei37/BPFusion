# Qualification and reconstruction

First preflight preserves a valid AMK prefix and failed pre-CUDA vLLM assertion.
Second preflight completes all9 actual executors/36 cells,288 measured
requests/9360 tokens plus72 excluded checked warmups; native queue/model
checks and source-native analysis pass.

Selected candidate protocol qualification completes three executors,622
requests/22224 tokens and259 expected rejects each, plus5000 empty connections
each. Both vLLM traces independently replay current model batch/KV history
under original upstream computation; fixed whole-output pools also match.
AMK remains bounded to the unchanged pool; its old eager-HF diagnostic stays
failed. Candidate lifecycle runs32 actions per workload, including2.2s idle,
binary/HTTP reuse, rejection, RST and inflight SIGTERM. All three exit0 with
13 closed/accepted connections,32 completions,3 expected aborts and empty
independent SQ/CQ; all complete/prefix checked outputs pass.

Original baseline sources were captured from pre-edit main82d31c8 and actual
pre-edit binaries saved before shared-header changes. Rebuilding those selected
snapshots through Makefile.original matches all normalized GPU SASS: AMK
2functions/2776 instruction lines; vLLM2/3872. This validates GPU code identity
for this reconstruction, not whole host ELF equivalence or all model semantics.
Reproducer materializes original/executor from the single captured source
home, then uses the source-native make variables/flags/runtime. It can build
fresh original libraries/entrypoints; no second repository checkout is used.

Exact full ordinary wrapper/runtime environment and15 expanded commands will
be frozen before collection. Paired source-native metrics cover partial
recovery/native gaps and independent vLLM transfers; no equivalence/randomization
claim or model-specific arithmetic optimization is introduced.
