# GPU-local I/O bookkeeping: completed throughput discriminator

This experiment moves regular I/O accounting into device memory while keeping
the existing host/BPF loop-control prefix shared. Its predeclared gen64/c8
output-throughput contrasts against current host bookkeeping are inconclusive
for both models. Candidate-minus-native Smol throughput is negative; Qwen's
native contrast crosses zero. Correct execution does not establish a winning
placement policy. The completed independent review confirms this bounded result. Main retains the already-selected host-bookkeeping constructor; the candidate is archived only.

## Question and intervention

The retained objective is Linux TCP/HTTP + eBPF/sockmap -> shared queue ->
resident real-model GPU -> asynchronous kernel TCP reply without a steady
userspace request worker, improving latency/TPS while reusing model computation.
This is a supporting constructor experiment within that serving-path question,
not a model-arithmetic contribution or a new formal paper RQ.

The preceding existing-data analysis in finding0053 found that additional model
rounds do not explain the remaining mean long-output native gap. Source
inspection identified regular IoStats reads/writes in mapped CPU memory as
a distinct candidate. The intervention changes bookkeeping placement, not model
math, timer cadence, queue publication, admission or TCP operations. CUDA's
[zero-copy guidance](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#zero-copy)
motivates device-local storage for repeatedly accessed mapped data; it does not
prove this workload's bottleneck.

In existing BF_IO_COALESCED builds, uring_start allocates device IoStats and
copies the fully initialized report after timer/bootstrap pending state is
established. IoState.out points to that device allocation; a separate control
pointer still addresses the mapped host/BPF loop prefix. model_quiesced and
finished access that shared prefix. After shutdown-worker stream synchronization,
uring_finish downloads only the suffix beginning at accepted, preserving live
stop/deadline/quiescence/finished fields, then frees the allocation. Source adds
29 lines and deletes2 in executor/io_uring_tcp.h. Other/default builds retain
their prior host-bookkeeping path. The shared conditional also serves optional
AMK coalesced builds; this run qualifies only the two vLLM models, with no AMK
performance transfer or repair of its earlier strict-HF failure.

The changed compiled layout/control indirection is part of the constructor.
No per-access PCIe measurement or exclusive physical mediation is claimed.
The strongest competing delivery mechanism is efficient native timed-epoll TCP
with identical reused vLLM computation. Current host-bookkeeping coalesced
serving is a component control, not another external baseline.

## Collection and reconstruction

[Plan](../../bench/results/device_stats_20261014/plan.md) and
[plan review](../../bench/results/device_stats_20261014/plan-review.md) predeclare
five paired blocks/three paths/two checkpoints, split ordinary short gen1/c8
and transfer gen1/c1,gen64/c1,gen64/c8 processes. Each cell has32 measured
requests, each executor8 sequential gen1 warmups. Odd blocks reverse context,
model and transfer-cell order; five of six path permutations leave residual
imbalance and small-N/drift limits.

All20 drivers/60 executors/120 cells terminated successfully at
2026-10-14T17:47:25.139737UTC:3840 measured requests124800 tokens plus480
one-token warmups =4320 complete responses125280 tokens. No serving cell was
failed, excluded, restarted or replaced. No oracle, metric, timeout or evaluation
path changed. Real preflight completed12 executors/24 cells192 measured requests
6240 tokens plus96 warmups, with all fixed raw analyses passing.

Base is34eb2b0b7b1d282d47766a4125df2e216c952c09 on original bpfusion-dev/main.
The source snapshot predates full collection and matches all captured paths
after collection; run.py records all20 expanded commands before the first driver.
The rebuilt host-stats component control matches the saved old ELF's normalized
SASS:3 functions4888 instruction lines. This does not claim candidate instruction
equality. Common runtime is vLLM0.31.0/Torch2.13.0+cu129/Transformers5.17.0;
model revisions, FP16 precision and build/environment receipts are archived.
The separate preparation SyntaxError was before recipe materialization/source
mutation/serving and is recorded independently; it produced no measurement.

## Primary delivered throughput

Means are five process-block cell means; higher output token/s is better.

| Model | Host bookkeeping | Native epoll | GPU bookkeeping | GPU versus host mean |
|---|---:|---:|---:|---:|
| Smol135M | 5362.058559 | 5616.194253 | 5408.676747 | +0.8694% |
| Qwen0.5B | 4601.192658 | 4757.707058 | 4628.035685 | +0.5834% |

Signed GPU-minus-control effects use nominal paired t95(df4), coefficient2.776445105; these are not simultaneous familywise intervals.

| Model | Control | Difference, token/s | Nominal paired t95 |
|---|---|---:|---|
| Smol135M | host bookkeeping | +46.618188 | [-0.127400,93.363776] |
| Smol135M | native epoll | -207.517505 | [-233.892259,-181.142752] |
| Qwen0.5B | host bookkeeping | +26.843027 | [-4.781485,58.467539] |
| Qwen0.5B | native epoll | -129.671373 | [-295.373506,36.030760] |

Smol's five host-control differences are all positive, but its interval still
crosses zero; Qwen has four positive and one negative difference. Neither
supports a reliable primary throughput gain, and zero crossing is not proof
of zero effect, equivalence or noninferiority. Smol loses to native in all
five blocks. Qwen's native differences are mixed. No primary native superiority
is established; secondary latency cannot replace this declared primary.

## Secondary latency, CPU and aggregate rounds

[Full analysis](../../bench/results/device_stats_20261014/full.analysis.json)
retains all24 means72 signed metric contrasts; no adverse row is removed.

| Model | Host gen1/c8 TTFT, ms | Native | GPU | GPU-minus-host nominal t95 |
|---|---:|---:|---:|---|
| Smol135M | 2.095576 | 2.177632 | 2.050390 | [-0.160768,0.070395] |
| Qwen0.5B | 2.472095 | 2.643542 | 2.471685 | [-0.102887,0.102068] |

Both short-TTFT host-control intervals cross zero. Qwen GPU-minus-native short
TTFT is-0.171856ms[-0.238178,-0.105534], but host bookkeeping already has nearly
the same2.472095ms mean versus GPU2.471685ms; that comparator result does not
identify a bookkeeping-placement improvement. Smol short native TTFT crosses0.

Smol gen64/c8 completion and TPOT improve versus host bookkeeping with nominal
intervals excluding0 (-0.815584ms[-1.586500,-0.044668] and
-0.012270ms[-0.021941,-0.002599]). These secondary local results remain reported,
without replacing inconclusive primary TPS or claiming familywise significance.
Smol loses gen1/c1 TTFT/TPS, gen64/c1 completion/TPS/TPOT and gen64/c8
completion/TPS/TPOT to native with nominal intervals excluding0. Qwen gen64/c1
TTFT loses to native (+0.034151ms[0.004287,0.064016]); other transfer boundaries
remain as their signed raw intervals. No universal latency/throughput win.

Known-worker CPU brackets include executor process and any reported TX-task
accounting only, excluding unaccounted kernel/BPF/softirq/client/energy. Neither
model's gen64/c8 CPU contrast against host excludes0; candidate mean decreases
for Smol but increases for Qwen. Both gen64/c1 candidate-minus-native CPU
contrasts are positive with nominal intervals excluding0. This is not total
CPU removal or an energy result.

The same ordinary short processes authenticate8 warmup rounds; subtracting
them yields measured mean rounds:

| Model | Host | Native | GPU |
|---|---:|---:|---:|
| Smol135M | 5.2 | 8.2 | 5.2 |
| Qwen0.5B | 5.4 | 8.0 | 5.4 |

GPU-minus-host mean round difference is0 for each model, with intervals
crossing0; GPU-minus-native short-round contrasts are negative. Aggregate
rounds do not give batch membership, GPU execution time or exclusive mediation.

[Prospectively secondary long-counter analysis](../../bench/results/device_stats_20261014/long_counter.analysis.stdout)
authenticates2088 serial/warmup rounds by captured source, complete request
counts and serial non-overlapping client timestamps before subtraction.

| Model | Host gen64/c8 mean rounds | Native | GPU |
|---|---:|---:|---:|
| Smol135M | 259.6 | 261.6 | 259.8 |
| Qwen0.5B | 259.4 | 260.2 | 260.0 |

GPU-minus-host long rounds+0.2Smol/+0.6Qwen have intervals crossing0.
GPU-minus-native Smol rounds-1.8[-3.160175,-0.439825] while throughput remains
lower, again bounding a simple additional-round explanation. Qwen's native
round contrast crosses0. Whole-transfer excess multishot CQ fractions remain
large (host/GPU about88%Smol and92%Qwen), not per-cell timing, cache/PCIe
attribution or evidence for a winning timer cadence.

## Correctness, shutdown and host observations

Each candidate model completes the existing622-request22224-token protocol,
259 rejects and5000 empty connections, with actual traced batches1..8 and
reused graph trace/history/KV replay. Ordinary timing qualifies finite frozen
complete-output-set membership; it does not observe the current batch trajectory
or establish fresh eager-HF arithmetic parity. Stronger old AMK failures remain.

Each32-action lifecycle validates652 complete-or-prefix tokens,13 connections,
32 completions3aborts, all8 physical slots FREE, admission bitmap0,recycle32,
pending/errors/drop/overflow0 and separately balanced SQ/CQ. Intentional stop
has admitted32/retired31; this is scoped abort accounting, not a silent mismatch.
Shared quiescence is supported by retained source and successful shutdown,
not direct after-free sampling. No pins remain; resource-release output is present.

Protocol strace records zero post-ready accept/recv/send-family calls and one
steady io_uring_enter invocation. Model/network userspace bootstrap and kernel/
timer/TCP CPU work remain. Finite syscall/protocol qualification is not arbitrary
reliability or elimination of all host CPU.

Host preflight17:08:26.956293, before17:20:12.933890,
during17:21:15.659531, mid17:33:21.106460 and after17:47:52.467895UTC
share boot04dc0087-5ccc-4c46-9997-b9a92f0e5167. Selected kernel-fault
observations retain33 older NVRM warnings, latest10:50:43UTC, without newly
selected lines. Before/after GPU-app snapshots are empty; during/mid show one
compute process. These sparse observations do not prove continuous isolation,
an entirely clean journal or harmlessness of old warnings.

## Review, selection and replay

[Fresh independent result review](../../bench/results/device_stats_20261014/result-review.md)
is complete and classifies the run valid/completed, old-control TPS hypothesis
inconclusive for both models, Smol native superiority contradicted and Qwen
native superiority inconclusive. It independently recomputes all24 means,
72 metric contrasts,30 short/30 long counter rows and eight round contrasts,
and finds no blocking finite correctness defect.

The owning source decision keeps host bookkeeping. The candidate's additional
allocation/control split is not justified by a demonstrated primary gain or
a correctness need; secondary local observations are preserved without
replacing primary TPS. The uncommitted candidate header is restored byte-for-
byte to base34eb; no commit is undone, no new option is retained and production
code growth is0. [Selection receipt](../../bench/results/device_stats_20261014/selected_source.json)
and [final restoration](../../bench/results/device_stats_20261014/final_restoration.json)
separate collected candidate from unchanged main. All candidate source/diff
and complete results remain in the archive.

CPU replay uses the archive's analysis.py with 'full', the two explicit
qualification_vllm_smol.jsonl/qualification_vllm_qwen.jsonl names through
analysis.analyze, analysis_lifecycle.py and long_counter_analysis.py. Raw
logs/references/source/build/commands preserve the actual collected constructor.
These replay commands do not require a GPU; lifecycle replay changes only its
fresh UTC stamp. See the archive README for actual commands.

The primary result bounds this bookkeeping constructor/workload; it is not
a direct challenge to removing the steady userspace request worker. Do not rerun
the unchanged matrix or round the near-zero Smol bound into a pass. Further
performance work needs a distinct discriminator rather than model arithmetic
tuning or a larger collection solely to cross a significance boundary.
