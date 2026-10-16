# Experiment plan: reuse packed mixed prefill/decode for complete GPU serving

## Research question

No paper/RQ contract exists in this repository. Retain the user's existing
question without inventing a new RQ: complete Linux TCP/HTTP + eBPF/sockmap ->
shared queue -> resident reused real-model GPU -> asynchronous kernel TCP
reply,without a steady userspace request worker,and improve throughput/latency.

Specific uncertainty: does replacing the constructor's prefill-only interruptions
with packed mixed prefill/decode improve ongoing generation latency under
offered load,when both transports reuse the same upstream computation?
This is driver/execution-adapter scheduling,not local model-operator tuning.

## Paper-value admission

Role: supporting. Largest credible story: a reusable no-userspace-worker driver
can use upstream continuous-batch computation efficiently; identify whether
its current homogeneous-round restriction contributes to service costs.
This is not a claim to invent mixed batching or prove eBPF superiority.

The strongest reject argument is that native CPU removal is irrelevant because
the constructor still serializes prefill and decode or pays padding/metadata
costs. Existing0064 logical histories reveal the gap but cannot measure the
proposed intervention. prior_schedule_analysis.py reuses all40 complete saved
traces. For16 banks,Qwen kernel/native means have388.6/355.2 prefill rounds
with active decode withheld,and3982.4/3535.0 deferred decode request-steps.
Smol has386.0/416.4 rounds and3392.6/3961.2 request-steps. Each executor combines
both prior rate cells plus8 gen1 warmups. These counts do not measure durations
or prove a bottleneck. Earlier publication,timer,residency and capacity evidence
does not test packed mixed execution.

Positive: qualify/select a reusable scheduling improvement only within its
tested mode,and update the main transport comparison against equally improved
native. Both-path gains are constructor gains,not eBPF gains.
Contradictory/mixed/inconclusive: retain the current constructor and bound the
mixed scheduling/packing choice. Do not tune it repeatedly to a favorable rate.
The best alternative is more complete CPU attribution or another backend port.
Those can clarify cost/breadth but do not directly repair this observed
generation/admission scheduling gap; model-specific arithmetic is lower value.

## Expected and alternative outcomes

Expected: ongoing decode can advance in the same model step as newly admitted
prefills,removing some interrupted generation rounds and improving mean TPOT.
Competing explanation: sampling/request padding,attention capture geometry and
extra batch work erase the gain or worsen TTFT/TPS/tails. A nonnegative paired
TPOT effect contradicts the expected improvement; intervals crossing zero are
inconclusive. Existing traces alone cannot decide.

## Published precedent and real assets

Reuse vLLM0.31.0 FP16 graphs/head/weights,KVs and the current source-native
BPF-loop/native TCP clients. vLLM's official optimization guide describes
decode-prioritized mixed batching; its GPU graph manager exposes token-count
mixed descriptors and GPU query offsets. BPFusion does not claim these ideas:

- https://docs.vllm.ai/en/stable/configuration/optimization/#chunked-prefill
- https://raw.githubusercontent.com/vllm-project/vllm/v0.31.0/vllm/v1/worker/gpu/cudagraph_utils.py
- https://raw.githubusercontent.com/vllm-project/vllm/v0.31.0/vllm/v1/worker/gpu/input_batch.py
- https://raw.githubusercontent.com/vllm-project/vllm/v0.31.0/vllm/v1/attention/backends/flash_attn.py
- https://docs.vllm.ai/en/stable/benchmarking/cli/#understanding-the-latency-metrics

Important compatibility uncertainty: the actual host uses FlashAttention2.
Its source labels default support UNIFORM_BATCH and warns that a graph captured
with max_query_len1 cannot run mixed prefills. Do not relabel support or patch
upstream attention. Candidate capture must use the source-native mixed
descriptor(max_query_len defaults to total tokens;N1 is necessarily uniform).
This is a proposed compatibility path requiring real qualification,not a source
claim that it already works on this GPU.

## Comparison

Four conditions at the same16 banks:
original loop,original eligible-frame-FIFO native,mixed loop,mixed FIFO native.
Mixed native is the strongest main competing mechanism: an efficient CPU
network path with the identical improved compute schedule. Original conditions
are component controls,not extra main baselines. The matched numerical run is
needed because published timing on different GPUs/models/transports cannot
answer this contrast. If mixed native matches/wins,no eBPF performance
superiority follows.

Candidate packs all pending valid prefill inputs and one next input for each
active decode into one token-contiguous batch. Preserve FIFO retirement,private
KV ownership,real sequence positions and response ordering. Use upstream
ModelCudaGraphManager FULL descriptors by total input tokens1..1024,with
num_reqs=min(total_tokens,16),zero-query request padding,and a captured gather
of last-token hidden states using GPU query offsets before the unchanged
official logits/sample head. Model kernels,weights,precision,network code,
capacity and timer remain fixed. Shapes/round trajectories change; this is
not identical kernel-sequence execution. No token padding proportional to
max_query times real batch is introduced. Only necessary capture/metadata/
dispatcher/replay glue changes; no runtime plugin framework or production
flag/default is added.

## Workloads and metrics

Same two checkpoints and revisions as0064:
Qwen2.5-0.5B-Instruct7ae55760 and SmolLM2-135M93efa2f0.
Use the same four literal prompts,gen64,offered rates96/192 requests/s,
256 scheduled attempts per cell,eight excluded checked gen1 warmups/executor.
Reuse the existing normalized gamma(shape1)arrival schedules,timeout and
all-attempt client definitions. No new timeout or post-result exclusions.

Primary per model: mixed-loop minus original-loop mean request TPOT at96/s.
TPOT=(last-first token arrival)/63,following official terminology.
Secondary: delivered-window TPS,connect-inclusive and scheduled-origin TTFT/
completion P50/P95/P99,client scheduling lag,failures,process CPU,and mixed-loop
minus mixed-native at both rates. Include adverse rows;P99 has limited order
statistics and does not establish P99.9 or production SLOs. Process CPU is partial.

Five paired process blocks/model;balanced Williams condition order over the
first four blocks,fifth repeats block0,and rotate rate order. Use nominal
paired t95df4 on block statistics,not pooled request inference. One integrated
matrix,40 executors/80 cells/20480 attempts. No favorable model/rate/pair
replacement. Expected cost is source/build preparation and hours of repeated
upstream bootstrap/serving/replay on the existing GPU; no new allocation or
persistent service.

## Correctness and executable workflow

All measured paths retain BF_TRACE equally; there is no CUPTI or
batch-invariant mode. Exact wire tokens must match independently CPU-built
upstream graph/KV/history replay for every actual admission/compute/release.
Mixed replay reconstructs each row's query length and position from its input
and prior history,not from the candidate's internal phase counters. Validate
packed offsets,total input tokens,slot ownership,complete retirement,zero
trace overflow,zero graph errors and transport shutdown.

The mixed capture additionally needs exact sampled-token agreement against
a source-native fresh-attention-metadata model forward at the same padded
batch geometry,using independently reconstructed per-round CPU query/sequence
metadata. Reconstruct clean histories from request starts before replay;
never reuse candidate-observed KV values as the expected state. No tolerance,
accepted-output union or serving-derived sequence is a correctness substitute.
If this official path cannot run/match,the candidate is unqualified and no
performance comparison is reported as valid. Any implementation repair retains
this check. Finite correctness does not imply arbitrary-model/task quality.

Reuse0064's real correctness suite,updated only for candidate shape bindings
and independent mixed reconstruction,for bothmodels/transports. Cover lengths
1/2/5/8/16/31/63/64,gen1/64,fragmentation,reuse,pipelines,half-close,rejections,
reset/stop and free queues. These are dependencies,not paper experiments.
No untraced timing or general ordinary fidelity is claimed.

Authoritative workflow: adapt the already executed0064 setup/load/analyze/
preflight/qualification/full scripts with the two constructor variants and
new mixed metadata. Build through the existing Make/nvcc recipes into owned
temporary directories. Freeze actual source,commands and checks before GPU
preflight. Concrete entrypoints in this TEMP:

    /usr/bin/python3 setup.py
    runtime/bin/python preflight.py
    runtime/bin/python qualification.py qwen
    runtime/bin/python qualification.py smol
    runtime/bin/python full.py

Real preflight: Qwen,four actual serving conditions,32 gen64 arrivals/condition
at96/s with the real TCP/HTTP path,metrics,wire checks and independent replays.
Protocol/semantic controls precede full collection. Full completion requires
all fixed cells and analyses terminal;partial prefixes remain incomplete.
Raw output remains in this TEMP,then bench/results/mixed_batching_20261015.
One fresh plan review before GPU execution,and one fresh result review after
terminal,following the owning research-experiment-design skill. No unchanged
matrix rerun to obtain a different sign.

## Interpretation and restoration

A negative primary signed TPOT interval supports a per-model generation
latency improvement only. Report TTFT,completion,TPS and failures separately;
do not call it universal latency improvement or erase an adverse competing
metric. Integrity/fairness failures invalidate affected comparisons,not turn
them into wins. Mixed native is always retained as the strongest competitor.
A result cannot establish exclusive cause from logical counts or total CPU/
energy savings. Target: one four-condition per-model table/figure with both
rates,all block statistics and signed effects.

Preserve main cf6bfee,unowned tools/setup_env.sh,eight original file fingerprints,
Coder process identities,base packages and existing caches/weights.
No clone/worktree/branch,host tuning,service/schedule/Workspace change.
Test-local16 is already within the requested benchmark scope;default8 stays.
Remove only owned TEMP/build/dependencies after no process/FD/map/cwd user and
after records/replays are saved. Select production changes only if justified
by actual qualification/results;otherwise retain current source.

## Pre-execution implementation clarification

Plan-review follow-up1 keeps admission valid. The new protocol reuses the
complete0064 suite for mixed loop/native in both models,including helper-thread
SIGTERM only after completed work. Unchanged original16 conditions retain
cf6bfee protocol/lifecycle evidence and receive all four-condition real
preflight/full wire/history checks. Existing unchanged transport RST/mid-
generation stop evidence is reused; mixed-constructor partial-stop numerical
fidelity is not newly qualified here. No incomplete-prefix acceptance mode is
added: any unexpected partial/new-run replay/release failure remains a failure.
Any later source adoption must separately address required integration coverage.

The optional review suggestion is adopted as a descriptive secondary client ITL
P50/P95/P99 over adjacent token-arrival gaps per cell. Zero/coalesced gaps remain;
these are neither isolated GPU steps nor independent process replicates.
Primary mean request TPOT,conditions,correctness and matrix are unchanged.
