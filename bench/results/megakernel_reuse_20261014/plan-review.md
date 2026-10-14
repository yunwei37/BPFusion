# Fresh plan review: reused AMK backend

Review observation: 2026-10-14. Read-only scientific/source review; no model,
CUDA build, serving process, plan edit or production edit was performed.
Reviewed plan.md, docs/evaluation.md, finding0047, docs/upstream-backends.md,
frozen0045 references, and the actual extracted upstream tree at
884534c4d2dbed4381576f81a79ae97feca53c34. No formal paper RQ/story file is
present; the retained user performance/reuse question is not renamed here.

## Judgment

ADMIT as a supporting backend integration and matched serving experiment.
Its dependency qualification may proceed. Neither a native example pass nor
a toy persistent test is an integration/performance result. Full serving
collection remains the plan's later step after actual same-checkpoint FP16,
device-controlled input/prefill/generation/output, native comparison and
lifecycle qualification. Missing prototype adapters do not block planning.

There is one executable command typo to repair before invoking the official
example: its argparse option is "--tokens 16", not "--tokens16". This does not
change the hypothesis, budget, arithmetic or oracle and does not require
another scientific review. The implementation uncertainties below are real
preflight concerns, not demands to finish implementation before admission.

## Admission and decision value

0047 directly observes substantial model-kernel spans with very short prompts,
but does not identify their arithmetic or ordinary-serving cause. It cannot
predict a fusion win. This untried candidate tests whether an existing reusable
whole-model backend can be integrated and yields a different delivery tradeoff;
an unchanged CQ/timer/copy sweep would add weaker information. Prior rejected
MPK/Plow/model-as-a-kernel/AlpinDale checkpoints and different precision/source
AMK claims do not settle this pinned local Smol FP16 comparison.

Success changes the reusable backend option and supplies a same-backend
transport comparison; faithful negative performance closes its measured
boundary. Numerical or launch failure only changes the candidate capability
decision and must be labeled dependency-only. These are distinct decisions,
rather than every outcome becoming a claimed speed result. Choosing a
supported consumer-GPU source over an unqualified H100 port is defensible.
This does not establish AMK as the best possible fused implementation or remove
the larger text/backend/SLO/CPU objectives. No extra decorative baselines or
new model workload is needed to admit this comparison.

## Pinned upstream behavior and executable hypothesis

generate.py lines11-15 and199-319 explicitly use host control per token.
examples/run_hf_model.py lines63-122 and142-186 use the native CUDA VM only
when "--vm cuda" is selected; the model and program precision are F32 in the
official CLI. HF greedy is computed independently and exact token-list
equality controls the actual exit code. This is an honest first native
dependency probe, not the FP16 experiment oracle or an efficient serving
baseline. CPU fallback, skipped CUDA or build success alone cannot qualify it.

PersistentDecodeVM is experimental, not the default generation interface.
Its tests cover one/two-layer toys; they do not prove real Smol FP16.
loader_persist.py constructs the base VM with cpasync=0 (lines122-127), and
its persistent extension does not carry the default loader's cp.async GEMV
compile flag. Consequently default per-step generation and persistent
generation are not automatically the same compiled arithmetic variant.
Comparing them for conformance is useful; a match is not a byte-identical
machine-code claim. Record actual precision/program/flags and retain the
frozen independent HF acceptance. If it fails, do not switch precision,
relax the oracle, tune kernels or treat F32 success as FP16 success.

The integration hypothesis is plausible but not proven by the Python API.
scheduler_persist.cu lines263-269 stores K, base_pos and first_token as
by-value kernel parameters; decode() performs host reset/synchronization,
and its native C launcher synchronizes the stream after launch. Capturing or
manually creating a graph cannot by itself make these request-time CPU
operations disappear or turn captured scalar arguments into dynamic inputs.
Necessary graph/input/lifetime glue must demonstrate that real arriving token
IDs and the actual request length drive the intended computation with clean
KV/counter state. Any finite preinstantiated scalar/program bank must be
disclosed as such; arbitrary-model/prompt coverage does not follow. Reusing
compiled programs or captured work is legitimate; caching answers or prompt
KV as a substitute for request-time prefill would violate this plan.

The unchanged persistent kernel writes generated[step] into device memory
without BPFusion's produced/DONE protocol. The output adapter needs an actual
ownership/publication path. Do not infer safe streaming or early token
visibility merely from a device pointer or from eventual complete output.
If it publishes only after finite generation, retain that behavior in TTFT/
TPOT/completion observations and use the same behavior in native AMK; it
cannot be described as a token-streaming latency benefit. Existing strict
abort/reset/recycle tests remain necessary because a socket dying does not
by itself retire an in-flight cooperative model or authorize buffer reuse.

Official CUDA graph requirements allow cooperative kernel nodes when MPS is
absent. They also require a device-launch-instantiated/uploaded eligible graph,
single-device permitted nodes, and prohibit CDP in its kernels. The documented
permission is confirmed, not inferred from a kernel name:
https://docs.nvidia.com/cuda/cuda-programming-guide/04-special-topics/cuda-graphs.html#device-graph-requirements
The source's standalone occupancy cap uses device-wide resident capacity;
it does not prove concurrent residency with BPFusion's dispatcher/io kernels.
Real instantiate/device-launch/co-residency and normal completion are the
preflight proof. Preserve a launch/deadlock/unsupported result honestly rather
than replacing the path with a steady host worker. No driver/MPS/host change
is justified by this admission.

## Independent correctness and comparison fairness

The frozen0045 FP16 file precedes this candidate and contains checkpoint-
specific prompt/gen complete-sequence pools. Matching one complete accepted
sequence is independent of AMK's own answers and avoids tokenwise mixing.
Keep that finite-set strength distinct from an exact replay of current
unobserved batch/KV histories, universal FP16 equivalence or task quality.
The unchanged strict independent replay controls add appropriate lifecycle/
history evidence. Full serving must preserve exact requested generation
length rather than silently truncating at EOS through the example's HF
generate defaults. The four literal prompts plus independent frozen controls
are a defensible fixed workload; no workload broadening is required.

The ordinary vLLM kernel loop is a credible current-practice compute-reuse
alternative and native TCP plus the same AMK generation is the credible
mechanism alternative. Neither is a deliberately slow Python-token-loop
baseline. Keeping vLLM's qualified tensor batching intact avoids artificially
favoring a batch1 backend. AMK single-lane/cooperative occupancy and any
serialization must be matched across native/kernel AMK and reported, rather
than silently assigning different queue/batching budgets. An AMK/vLLM gain
changes computation and cannot be assigned to eBPF; AMK/native isolates the
serving-control alternative only to its measured matched extent. If native
fails an avoidable adapter/ownership path, that is an invalid comparison,
not a proposed-method win.

## Workload, metrics, execution and interpretation

The integrated matrix is internally consistent: three paths times five
paired process blocks times four cells times64 measured requests yields
3840 measured requests and124800 measured tokens, plus120 checked excluded
gen1 warmups. Repetition at the process-block level is appropriate; requests
are not independent replication units. Alternation and balanced cell/prompt
order reduce simple ordering confounds. Three-way blocks must have a concrete
recorded order before collection; exact equality of every order count is
not possible with five blocks and is not required.

Client TTFT and output throughput use the source-native protocol and official
vLLM metric definitions cited by the plan. Four model-specific primary
contrasts, their paired uncertainty, all cells/tails and negative effects
must be retained. A nominal t95 interval across five blocks is not equivalence,
familywise inference or immunity to host interference. Known-worker CPU
brackets are supporting costs, not all kernel networking/total CPU/energy.
Compilation/bootstrap are separate from steady request latency. Correctness,
normal actual child exits, drain/recycle and matching computation are valid
vetoes; a secondary performance sign alone is not grounds to discard a
primary result.

The first official native command, actual cached checkpoint, precision,
fixed source, raw archive and completion intent are executable now after
the flag typo. Adapter/server commands necessarily arrive with prototype
implementation and must be archived and frozen before serving/full timing.
No fabricated runnable command or new experiment-control interface is needed.
Record deviations before affected collection; oracle/arithmetic changes
cannot be quiet repairs. Before/after real host observations, preservation
of earlier OOM/NVRM records and owning-path fault diagnosis are appropriate,
without pretending discrete brackets prove continuous isolation.

Positive, negative, mixed and inconclusive outputs lead to the plan's bounded
backend/control decisions. Native correctness only remains dependency-only.
No completed prefix or compatibility fallback satisfies the integrated
experiment or full project goal. The current plan supplies sufficient
scientific scope to proceed; strongest unresolved risks are numerical
qualification and actual device-controlled cooperative integration, which
the planned real qualification can discriminate.

## Same-review follow-up after routine source clarification

The root corrected the official example flag to "--tokens 16" and added
the persistent cpasync=0 and real-request scalar requirements to the plan.
The typo is resolved; ADMIT is unchanged.

The official CUDA Runtime Graph Management reference also documents device
cudaGraphKernelNodeSetParam for device-updatable nodes on the same GPU.
Installed CUDA13 headers contain the device-updatable launch/node attribute.
Thus by-value upstream kernel parameters are an integration problem to test,
not proof that immutable AMK computation cannot accept dynamic requests.
A legitimate device-side parameter update adapter may satisfy the plan
without editing upstream math/ABI. Actual export, allowed graph attributes,
updates, ordering and cooperative device launch remain unqualified until the
real implementation exercises them. This does not relax input correctness or
permit steady host parameter updates during requests.

Source: https://docs.nvidia.com/cuda/cuda-runtime-api/cuda_runtime_api/group__CUDART__GRAPH.html
