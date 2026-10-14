# Reused megakernel backend integration and matched serving comparison

## Question and admission
Retain the user's performance/reuse objective and finding0030's latency question:
can an existing whole-model GPU backend reduce serving latency/raise throughput
while preserving real checkpoint semantics and autonomous Linux TCP/eBPF service?
No formal paper RQ is present or invented. Planned role supporting backend
integration/comparison; native build/correctness probes are dependency-only.

Finding0047 observes about1ms optimized model-kernel spans on small requests,
but does not establish an arithmetic cause or ordinary-stage fraction.
Existing MPK/Plow/model-as-a-kernel/AlpinDale numerical failures and unchanged
upstream revisions must not be rerun unchanged. AutoMegaKernel has not had
local real-checkpoint CUDA qualification. Its default decoder is host-driven;
its experimental PersistentDecodeVM exposes a complete finite device loop.
Equal-BF16 upstream results trail cuBLAS, so no compute gain is assumed.
A local same-checkpoint FP16 serving comparison is not settled by that source
claim or by older HF timelines. No large model-specific tuning campaign.

Largest credible story: integration of an independently qualified reused
whole-model backend with autonomous ordinary Linux I/O, then an explicit
compute-reuse tradeoff and same-backend transport comparison. A positive
result changes which reusable backend the service should expose; a negative
result closes this candidate's fidelity/execution/performance boundary.
A numerical or launch failure produces dependency/capability evidence only,
not a paper speed result. Native qualification is folded into this integration,
not published as an independent contribution.

Best alternatives: port H100-only Hazy kernels, revisit numerically rejected
unchanged MPK, or add NVIDIA LSTM as a new workload. The untried general AMK
interface uses an already cached real model and supported SM120 toolchain,
adds a causal backend alternative, and avoids a model-specific kernel port.
Do not change the research claim if the candidate fails.

## Official sources and actual assets
Pin AMK884534c4d2dbed4381576f81a79ae97feca53c34,MIT.
https://github.com/RightNow-AI/AutoMegaKernel/tree/884534c4d2dbed4381576f81a79ae97feca53c34
generate.py is CPU per-token control; examples/run_hf_model.py defaults to
ReferenceVM/F32, not evidence of native GPU real-checkpoint acceptance.
vm/loader_persist.py and scheduler_persist.cu implement finite generation;
tests/test_persist_decode.py exercises toy1/2layer models, not Smol weights.
No post-hoc model substitutions or relaxed numerical oracle.
PersistentDecodeVM uses by-value first_token/base_pos/K kernel arguments;
a graph adapter must obtain these from actual requests,not fixed prompt answers.
The persistent loader's cpasync=0 base matches its separately compiled
register/coalesced GEMV. Native/kernel controls must use that same variant;
the default per-token loader's differing variant is not silently substituted.

CUDA device-graph requirements permit cooperative kernels without MPS:
https://docs.nvidia.com/cuda/cuda-programming-guide/04-special-topics/cuda-graphs.html
Actual occupancy, instantiated graph behavior and GPU dispatcher co-residency
remain to be tested. Source API permission is not executable evidence.

Keep original bpfusion-dev/main,RTX5090/Linux7.3rc3/driver610/CUDA13.
Cached SmolLM2-135M revision93efa2f097d58c2a74874c7e644dbc9b0cee75a2.
Use upstream importer/default schedule/math. No raw upstream VM/ABI edits,
kernel tuning,INT8/NVFP4 substitutions,host driver or infrastructure changes.
Necessary BPFusion glue concerns graph/control/input/output ownership only.

## Dependency qualification and execution
TEMP=/tmp/bpfusion-megakernel-reuse-oxfus39y
Archive=bench/results/megakernel_reuse_20261014.
First native command, unchanged official example:
python UPSTREAM/examples/run_hf_model.py --model CACHED_SMOL --vm cuda
--prompt 'The capital of France is' --tokens 16
Its F32/HF CPU oracle is only a native dependency qualification, not FP16
equivalence or a performance baseline. Record actual outputs/exits/precision;
skips or CPU fallback are not success.

Then call official generate()/amk_greedy_decode() with DType.F16 on the same
cached weights and four existing literal token prompts,gen1/64. Compare exact
whole sequences to the frozen pre-observation HF FP16 references already
qualified in0045; do not expand them. Confirm actual native single-launch
generation for all cases against independently computed reference and official
per-step path before constructing the network adapter.

Use a device-launchable graph around unchanged upstream model work with
BPFusion input/output/lifetime glue. Prefill must be GPU-controlled at request
time; leaving upstream CPU prefill/argmax per request does not meet the goal.
A resident GPU dispatcher accepts generic backend graph/control descriptors
and publishes output without steady host model/request handling.
No fake model,precomputed answer or client-side model substitution.

This is a prototype integration; concrete adapter/build/server invocations
will be archived before first serving. They do not yet exist and are not
claimed qualified. Record necessary implementation/runner deviations before
affected validation. Stop this candidate's integration if the official/native
path cannot qualify without arithmetic/oracle changes; preserve original
backend and continue the larger objective through another useful path.

## Comparisons and full workload after qualification
Strong current practice: existing qualified ordinary vLLM kernel-loop backend.
Same-backend competing mechanism: efficient native TCP submitting AMK's whole
GPU generation per request. Do not force a Python token loop as this baseline.
Candidate: same AMK computation under autonomous eBPF/kernel/GPU control.

FP16 checkpoint,token-ID HTTP protocol,K/greedy semantics and client prompts
stay matched. Native and kernel AMK must share identical upstream program/
computation and scheduling/batching policy. Current vLLM retains its qualified
tensor batching,not deliberately disabled to favor batch1 megakernel.
Backend-vLLM effects are compute-reuse effects,never eBPF cause.
AMK-versus-native effects are the serving/control comparison, with remaining
native control/compiled differences stated explicitly.

Four standard cellsgen1/64 byc1/8,64 requests/cell,8 excluded checkedgen1
warmups/executor,5 alternating paired process blocks,3paths/15executors.
3840 measured requests/124800 measured tokens plus120 checked warmups.
Rotate cell/prompt order equally; process blocks are replication units.
Primary outputs: gen1/c1 client TTFT and gen64/c8 throughput. Report all four
AMK-vLLM/AMK-native model-specific primary contrasts, nominal paired t95df4.
TPOT/completion/tails and actual worker CPU brackets are supporting tradeoffs,
not total CPU/energy or SLO proof. Metrics reuse source-native resident_dispatch
and official vLLM serving definitions:
https://github.com/vllm-project/vllm/blob/v0.31.0/vllm/benchmarks/serve.py

Correctness before/full serving: unchanged strict fragmentation,pipeline,
half-close,reset/abort,rejection/recycle and output oracle controls.
Actual per-request ownership, SQ/CQ drain and executor exits must be normal.
No ordinary current-batch replay or arbitrary-model claim from finite sets.
Same-native computation qualification must precede timing. Freeze runnable
source before full collection; fresh independent result review after terminal.
No incomplete prefix is full evidence, and no failed baseline is a win.

## Interpretation and restoration
Native/fused correctness alone is dependency-only and cannot finish the goal.
Primary gain with qualified native control supports only the measured backend/
workload tradeoff. Null/negative effects close this candidate without a
favorable repeat or tiny timer/CQ search. A source/runtime compatibility
failure is not measured performance. Direct thesis challenge is not presumed.
Report compilation/bootstrap and single-lane/batching limitations.

Before/after actual host GPU/memory/kernel journal observations; keep prior
OOM and profiler NVRM warnings visible. New genuine faults use existing owning
diagnosis without discarding rows or interfering with other projects.
Restore/remove only owned TEMP and named builds after review, preserving
original Workspace/PVC/boot/default library/base/Coder/cache/tools/setup_env.sh.
Honest finding/evaluation and main publication follow actual evidence; full
generic text/backend/SLO/performance acceptance remains open.
