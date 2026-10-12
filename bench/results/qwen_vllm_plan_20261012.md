# Official token-only optimized serving comparison

The unchanged goal is worker-free real-model TCP/HTTP serving with improved
throughput/latency. No paper RQ or thesis exists; do not invent one.
Prior ablations and copy experiments cannot answer competitiveness: their
host control is serial and deliberately preserves our math. The strongest
available discriminator is official optimized vLLM, not another pointwise
candidate. This integrated comparison is supporting evidence toward the
engineering goal; a smoke/setup result has no independent research value.

Question/hypothesis: does the retained GPU-controlled graph method offer a
client-observed throughput or latency advantage over official optimized
vLLM on matched fp16 Qwen2.5-0.5B token-ID requests on this shared RTX5090?
A loss identifies computation/batching/scheduling as the next priority;
a gain supports only this finite workload/interface/hardware condition;
mixed/inconclusive effects remain mixed. Nothing completes the service goal.

Current method: published442ab45 production Python/native/BPF/module,
eight private batch1 graph/KV banks and GPU fork/join. Use the current
build/qwen_graph and canonical loader/stream attach; no old temporary
compute adapter or transport library. Before collection freeze actual source
and native-library identity and keep it constant across paired processes.
Strongest external competitor: official vLLM0.31.0 token-only server,
immutable cached Qwen revision7ae557604adf67be50417f59c2c2f167def9a775.
Original BPF binary weights derive from this Qwen export; verify exported
fp16 parameter contents against this cached safetensors before measurement.
No quantization, speculative model, eager fallback or artificial scheduler
restriction. Keep default optimized kernels/graphs/scheduler/prefix cache.
Different supported contexts/caches/libraries are reported. vLLM uses
Torch2.13.0+cu129/Transformers5.17.0; method keeps2.14.1+cu130/5.19.0.

Official command:
TEMP/venv/bin/vllm serve MODEL --tokens-only --dtype half --host 127.0.0.1 --port 39404
Differences from generic vllm serve MODEL: tokens-only matches token input/
output instead of tokenizer/chat; half matches fp16 rather than bf16 model
default; private host/port and VLLM_API_KEY ephemeral RAM/env only are benchmark
lifecycle/auth. No key value in source/commands/logs/Git. Retain all other
defaults. At the2026-10-12 refresh, successful nvidia-smi finds no compute apps.
Endpoint reads do not establish continuous isolation.
Try default GPU allocation first. If actual startup reports free-memory
incompatibility, record that failure and use a test-local utilization0.35
only if the live available memory supports that configuration,
not a performance sweep or retained service change. If another substantive
compatibility defect occurs, repair actual path and report deviation; do not
silently degrade optimized competitor or label its failure a method win.

Reuse exact four prompts and independently eager-fp16-derived64-token
reference from qwen_paired_kv_20261010.jsonl metadata; freeze it before run.
BPF must retain exact reference equality. vLLM greedy optimized fp16 may
select different tokens due to kernels/batching. Retain actual tokens,
full reference, per-request exact equality and first mismatch; require
valid vocabulary IDs, requested lengths and greedy/no-EOS settings.
A mismatch does not itself invalidate a fixed-length throughput observation,
but rules out an identical-output comparison/superiority claim. Report
performance and reference agreement separately, never alter oracle,
subset or precision to qualify vLLM or our method. No output quality claim.

Official /inference/v1/generate with token_ids,stream=true,sampling_params:
temperature0,max_tokens1or64,ignore_eos=true,detokenize=false.
No chat template, tokenization or text chunk counting. Actual version0.31
serving uses DELTA outputs, no newer output_mode field. stdlib http.client
handles HTTP transfer framing; timestamp complete SSE frames and count
choice.token_ids; IDs delivered together share arrival. BPF timestamps
completed4-byte tokens. Binary vs JSON/SSE wire/CPU overhead remains a
real interface difference, not isolated GPU scheduler causality.

Fixed full matrix:gen1/64 x concurrency1/8,64requests/cell,fourprompts16each.
Five paired process repetitions alternating method order,rotating cell order.
Eight excluded warmups/process:fourprompts atgen1then64. Count tokens,
not frames. Connections/threads created before ready/timed barriers.
Full40cells2560requests83200actualoutputtokens,ten owned engine shutdowns.
Preflight:onepair,bothmethods,allfourcells,eightrequests/cell,2080tokens.
Default-memory failure is preserved as preflightattempt1; correctedattempt2
uses same matrix/reference/metrics. Requests60s inherit existing benchmark;
startup is ready-or-terminal with no arbitrary deadline; verify live process
rather than restarting on observation timeout. Cleanup only owned processgroup.

Primary standard metrics:gen64 throughput,TTFT,TPOT atclients1/8.
TTFT=firstarrival-send;TPOT=(last-first)/63;throughput=tokens/(lastarrival-
firstsend). NVIDIA definitions:
https://docs.nvidia.com/nim/benchmarking/llm/metrics
Five block means;separate nominal paired df4 two-sidedt95 intervals,positive
gain=methodTPS-vllmTPS orvllmLatency-methodLatency. No multiplicity correction,
family-wide win or new weighted score. Secondarygen1/completion,p50/p99,
warmstartup,fullownedprocess-groupCPU/idle at100Hz,GPUendpoint snapshots.
FullprocessgroupCPU includes vLLM API/engine children vs method bootstrap/
sleep process;excludes kernel TX/softirq/clients/other host work,not totalhost.
SharedGPU/warmcache/fourshortrepeatedprompts/closedloop32GB constrain scope.
Automatic prefixcache behavior remains default;shortprompts under blocksize
may not hit. Logs preserve cache/scheduler/kernel choices,not infer hits.

Reuse bench/resident_dispatch.py native request/connect and ready barrier
semantics;necessary adapter adds official HTTP tokenstream and lifecycle,
not a new control framework/toy runner. Freeze actual script,reference,
commands,upstream protocol versions and collectionHEAD. RawJSONL ordinary
metadata/requests/cells/executor/failure events,all partial attempts retained.

Runnable:HF_HOME=/workspaces/.cache/huggingface python3 TEMP/compare.py
--preflight --output bench/results/qwen_vllm_preflight_default_20261012.jsonl
Default failure correction adds --gpu-memory-utilization0.35 and distinctraw.
Full removes--preflight,uses same selectedconfig,and writesqwen_vllm_20261012.jsonl.
Analyze actualraw with compare.py --analyze;fresh result reviewer independently
recomputes counts/timestamps/cells/outputdifferences/counters/intervals
and separately audits intended vLLMoptimizedmechanism.

Plan review before GPU/tokenpreflight;fresh terminalresultreview aftercomplete.
OriginalWorkspace/PVC/session/untrackedtools/setup_env.sh/other owners preserved.
Root cleanup owner,lifetimeonlythiscomparison,noDNS/gateway/Flux/Secrets.
Each engine uses own processgroup;SIGTERM onlythatgroup,wait for terminal,
reportforcedcleanupifneeded,never broadpkill. Remove BPFpins/module through
existingloader aftermethod;removevenvonlyafterterminal artifactfreeze/noowners.


2026-10-12 continuation: original installation is terminal exit0 and its
process49482 is absent. Reuse that same existing temporary venv. Earlier
readiness/cross-node/short-input work has changed the current source and
identified captured compute as dominant; it does not replace this missing
optimized-serving comparison. The AlpinDale qualification is separately
terminal, and its numerical disagreement is not a competitive win.
This is supporting evidence toward the user engineering objective; no
paper-level RQ/thesis exists and none is invented. Upstream/default-kernel
output agreement remains a separate observation rather than a replacement
for BPFusion strict correctness. Source-native vLLM optimization must engage
without artificial slowdowns or an eager fallback.

Plan review round1 identifies an actual failure-cleanup defect in the
prepared adapter: an exited API parent could leave its engine child in the
owned process group without receiving SIGTERM. Before any GPU preflight,
stop() now signals that same owned group when either parent or group remains;
ProcessLookupError is harmless. A child-group timeout sends SIGKILL only to
that group and raises a retained failure. No healthy other process is targeted.
The actual full run must verify ten normal owned group shutdowns.

Real preflight attempt1 (default optimized settings) reaches model/
FlashAttention2/torch.compile and CUDA-graph capture, but terminates before
requests because FlashInfer sampling JIT cannot find ninja. The installed
venv already contains ninja; absolute invocation did not expose its bin
directory to subprocess PATH. Preserve the complete default attempt raw/
stdout. Driver/API/engine are absent and successful nvidia-smi is empty.
The smallest existing-path repair exposes venv/bin to only the vLLM child,
as normal venv activation does. It changes no package/kernel/scheduler/
precision/metric/oracle. Attempt2 uses a new raw name and the unchanged
8-cell preflight matrix; no utilization or eager fallback is added.

Attempt2 completes all8 preflight cells/64 measured requests/2080 output
tokens,16 declared warmups and two normal engine exits0. Authentication
missing/invalid401 checks pass. Native analysis exits0; all BPF replies
equal the frozen oracle. vLLM outputs disagree on some cells and are retained
separately as planned. Own driver/API/engine/model/module/pins absent;
successful nvidia-smi is empty before full collection. Begin unchanged
five-pair40-cell full matrix on source442ab45 with the repaired child PATH.

Terminal audit clarification: ten recorded wait exit0 codes belong to
launching parents. The official vLLM shutdown can force-kill its EngineCore
child and native HF shutdown logs SubprocPool unclean exit. Retain those
framework messages; do not claim every child exited0 or wholly graceful
shutdown. Adapter timeout-force cleanup is not observed. Owned groups
clear and all measured requests are complete; the detached wrapper wait
code was not retained, while actual replay analysis exits0.
