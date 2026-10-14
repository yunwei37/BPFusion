# Experiment Plan: GPU-local I/O bookkeeping with shared loop control

## Research Question

The retained user question is improving latency/TPS of the complete Linux
TCP/HTTP + eBPF/sockmap -> shared queue -> resident real-model GPU ->
asynchronous kernel TCP send path, without a steady userspace request worker,
while reusing model kernels. No formal paper RQ exists to quote or rename.

This experiment asks whether keeping regular GPU-owned I/O bookkeeping in
device memory improves remaining delivered long-output throughput while
preserving the exact shared stop/quiescence/finish control and final report.
It does not optimize model arithmetic or claim total CPU elimination.

## Paper-Value Admission

Planned role: supporting. The largest credible story is that a reusable
GPU-driven serving path can retain Linux TCP and ordinary OS coordination
without forcing GPU-only bookkeeping through host-mapped memory on every
progression step. This would strengthen a model-kernel-independent driver
story, not create a separate model-math contribution or general SOTA claim.

Finding0053 fixes the large concurrent-short-output scheduling loss, but Smol
long-output TPS still loses versus efficient native TCP and Qwen transfer is
inconclusive. Its post-hoc ordinary transfer analysis authenticates that the
selected path already uses fewer aggregate gen64/c8 model rounds than native.
An extra-round explanation therefore cannot account for that remaining gap;
per-round shape/padding, I/O work, waits and client delivery remain competitors.

Source inspection independently finds frequent regular IoStats updates in
host-mapped memory, although CPU/BPF steady coordination uses only its control
prefix. Existing data cannot test changing that placement. The intervention
adds new evidence beyond admission/cursor/round counts; it is not a tautology,
because CUDA layout/caching, mandatory ring/page access and model costs could
dominate and a private allocation could provide no benefit or regress.

Positive effects support this narrow driver constructor; contradictory,
mixed or inconclusive effects retain the current policy or narrow a candidate
selection and bound bookkeeping's relevance. They do not force a new thesis
or a model-specific tuning exception. The best immediate alternative is a
heartbeat-period sweep: whole-transfer excess CQ traffic is88–92%, but
changing cadence also trades kernel submission latency and is not an isolated
empty-read repair. Async receive is already present. Bookkeeping placement
has higher decision value because it avoids that timing tradeoff and preserves
network operation/wakeup semantics. Extra models, unchanged matrices and
weak baselines are not substitutes for this discriminator.

## Expected And Alternative Outcomes

Expected: candidate improves gen64/c8 output tokens/s versus the captured
current coalesced control in one or both qualified models, possibly reduces
single-request delivery overhead, with valid output/recycle/shutdown receipts.
Alternative: mandatory shared ring/page/CQ reads, model-round shape or
coordination dominate, so TPS intervals cross0 or favor the control.
A correctness defect in control separation/cold report copying invalidates
the candidate until repaired within the same hypothesis. No correctness,
oracle, timeout or metric relaxation is permitted.

Source placement is the treatment; its compiled layout/control-pointer
indirection also changes. No isolated PCIe transaction, cache-miss, GPU-time
or latency-mediation claim follows from elapsed serving metrics alone.

## Published Precedent And Real Assets

Reuse original bpfusion-dev/main, current code base
34eb2b0b7b1d282d47766a4125df2e216c952c09, selected finding0053 coalesced policy,
source-native matched TCP clients/adapters, existing builds/loaders and frozen
model references. The native competitor uses the same captured vLLM graphs,
FP16 weights/KV, packed/prefix policies and four prompts as each coalesced path.

Official CUDA [zero-copy guidance](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#zero-copy)
motivates reducing repeated mapped accesses by using device memory; it does
not prove this workload's bottleneck or a measured gain. Official vLLM
[latency definitions](https://docs.vllm.ai/en/stable/benchmarking/cli/#understanding-the-latency-metrics)
define TTFT and TPOT. Source-native TPS is output tokens divided by first-send
to last-token span for the fixed measured cell, not overall process duration.

TEMP runtime reuses vLLM0.31.0, Torch2.13.0+cu129, Transformers5.17.0 and
libbpf1.6.3. All actual package/compiler/GPU/kernel/model revisions and
commands are recorded anew; historical means are not reused as controls.

## Proposed Source And Ownership

Prospective implement.py/proposed_io_uring_tcp.h/proposed.diff materialize the
candidate. No production patch or real GPU experiment has run at plan entry;
dependency/control build setup is preparation only.

Only BF_IO_COALESCED regular IoStats bookkeeping gets a private cudaMalloc
object. Initialize it after bootstrap timeout pending=1 is set, using the
existing initial report. IoState.out points to this object, while its distinct
control pointer points to the original mapped host report's control prefix.
The private object's copied control prefix is unused for coordination.
Both GPU quiescence loads and finished stores use the live control pointer;
all host/BPF registrations, reads and writes keep the existing report region.

After network-stream synchronization, cudaMemcpy copies only
[offsetof(IoStats,accepted),sizeof(IoStats)) to the existing host report.
It never overwrites live stop/deadline/quiescence/finished fields. Results and
reply records retain their format/accounting. The private object remains alive
through model and shutdown I/O work and is freed after the final download.

Shared queue/loop control ABI, ring/SQE/CQE/buffer placement, timer60us,
network operations, FIFO/recycle/admission policy, workers and model code are
unchanged. No new public mode/knob/helper/service or persistent configuration.
Other/default modes retain host bookkeeping via the existing preprocessor
path. The common transport header also serves experimental AMK builds, but
this experiment qualifies only the two already-output-qualified vLLM models;
AMK's older strict-HF failure and rejected performance transfer remain intact.
No arbitrary-backend/kernel/text/fairness/rollover claim is made.

## Comparison

One competing delivery mechanism: efficient native epoll TCP with matched
reused vLLM computation. It must run fresh under the common environment/input
because prior results cannot settle this changed constructor. Native matching
or winning limits superiority; crossing0 is not equivalence/noninferiority.

Component control: captured current coalesced header with host-mapped
bookkeeping and finding0053 admission. Rebuild under the original suffix and
compare normalized SASS with the saved freshly built current ELF before
applying the candidate. This reconstructs the control, not candidate equality.
Both paths use identical model source, compiler flags/runtime, precision,
prompt/reference budget and warmups; no per-condition tuning.

## Workloads And Metrics

Models: SmolLM2-135M and Qwen2.5-0.5B-Instruct, their existing exact cached
revisions, four frozen prompts, token-ID local HTTP/binary scope.
Primary performance outcome: gen64/c8 client output tokens/s, candidate minus
old and native, separately per model. Secondary transfer: gen1/c8 TTFT,
gen1/c1 and gen64/c1 TTFT/completion/TPS/TPOT and partial known-worker CPU.
Retain all signed values and nominal paired t95(df4) intervals, coefficient
2.776445105; no pooled-request pseudo-replication, threshold score, NI margin
or familywise confidence claim.

Existing split ordinary contexts are reused: short_serving.py only((1,8),);
transfer_serving.py((1,1),(64,1),(64,8)). Each cell32 measured requests;
each executor eight sequential gen1 warmups. This authenticates short rounds
minus8 and long/c8 rounds minus2088 from the same ordinary processes.
These are secondary aggregate counters, not batch membership/GPU time.
Predeclare the same source/timestamp subtraction proof from the existing-data
diagnosis. Whole-transfer CQ-SQ excess is descriptive multishot traffic;
it is not per-cell time or a primary outcome.

Correctness remains the unchanged finite whole-output pools for untraced
timing, actual client HTTP status/length/token arrival, model errors, complete
prefix/accounting, BPF physical FREE slots/bitmap/recycle, ring/pending/errors.
Protocol qualification for each candidate model622 requests/22224 tokens,
259 rejections and5000 empty connections; selected BF_TRACE/history/KV replay
reruns reused vLLM graphs, not fresh independent eager-HF arithmetic parity.
Two32-action lifecycle runs include idle reconnect, rejection, pipeline/
half-close, reset and stop in active inference; independently inspect raw slot,
bitmap/recycle/queue and shutdown/source receipts, not only pass booleans.
Each checks652 complete-or-prefix tokens; intentional aborted long replies
and admitted32/retired31 stop accounting retain their established scope.

Five paired process blocks, five of six path permutations; odd blocks reverse
contexts/models/transfer-cell order. Preserve residual imbalance/drift and
small-N limits. Same original Workspace, GPU/PVC/session; no host tuning or
other workload interruption. Sparse actual host before/during/mid/after
observations contextualize results without continuous-isolation claims.

## Planned Runs

| Run group | Role | Workload | Paths | Repetitions | Decision |
|---|---|---|---|---:|---|
| Ordinary short+transfer | proposed, native competitor, component control | two models/four cells | GPU-local stats/native/current host stats | 5 paired blocks | primary TPS with latency/correctness boundaries |
| Protocol and lifecycle | integrated qualification | two candidate models | GPU-local stats | one existing suite each | invalidates a faulty constructor |

Full:20 drivers/60 executors/120 cells,3840 measured requests124800 tokens,
plus480 one-token warmups =4320 complete replies125280 tokens. Source/model
captures dominate cost; expect roughly30 minutes ordinary serving plus setup
and integrated qualification, not a new enforced deadline/budget.

## Execution

Original source/build/tests stay in /workspaces/repository/main within original
Workspace. Temporary recipes/runtime/raw outputs stay under this plan's TEMP.
Setup runs setup.py; after ADMIT, prepare.py reconstructs the old control,
executes implement.py and builds the candidate through existing Make targets.
Do not execute prepare.py or actual preflight before independent plan admission.

Real preflight: python3 TEMP/run.py preflight1 then its fixed analysis.
Four drivers/12 executors/24 cells,192 measured requests6240 tokens plus96
warmups. Existing run_qualification.py and run_lifecycle.py then actual raw CPU
analysis. A maximum of three real preflight attempts follows the skill;
failures are retained, repaired only on the fixed scientific path.

Freeze candidate/source/build/environment/model receipts and all expanded full
commands before collection. Authoritative full command: python3 TEMP/run.py
full; wrappers call the source-native adapters, not a toy system.
Full completion means all20 driver/60 executor terminal exits and fixed raw
analysis of every cell, not a prefix or observer timeout. Retain stdout/stderr/
commands/exit records, no silent replacement. Continue the same actual handle
until terminal. Fresh independent result review follows completed collection.

After valid diagnosis/selection, preserve full evidence in one archive,
synchronize honest OSS docs, clean only owned TEMP/build artifacts, verify
post-cleanup CPU replays and original preservation, commit/push on main and
verify public bytes. Those logistics have no independent research value.

## Interpretation And Reproducibility

Positive primary effect: candidate-minus-old TPS interval above0 supports
local bookkeeping-placement benefit for that model. Candidate-minus-native
above0 supports only the tested finite superiority claim; native win bounds
it. Contradictory/zero-crossing primary results are retained per model, without
claiming equivalence/non-regression. Secondary latency matters to source
selection but is a scientific veto only when it invalidates correctness,
fairness or the precise claim. Aggregate rounds alone cannot establish TPS
benefit or replace primary metrics.

Target table: both-model gen64/c8 TPS and signed old/native differences,
with transfer TTFT/CPU and same-process round/context counters linked.
No unchanged rerun, model arithmetic sweep, weak baseline or packaging result
is a separate contribution. A negative result is a constructor/workload
boundary, not a direct thesis challenge.

Preserve unrelated tools/setup_env.sh, default qwen_graph.so inode262875
size1032248, four unowned loop_trace artifacts, base packages
2.14.1+cu130/5.19.0/2.5.3 and Coder PIDs1/10909. No persistent runtime,
credential/network/storage/machine or scheduler change. Source/recipe
preparation errors are recorded separately from serving; none has changed
metric/oracle/timeout or produced a measurement.
