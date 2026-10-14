# Independent plan review: GPU-local I/O bookkeeping

Reviewed: 2026-10-14, before candidate implementation or GPU preflight.
Reviewer: fresh independent research-experiment-design PLAN REVIEW reviewer.
Round: 1. No desired verdict was supplied.

## Verdict

ADMIT for real preflight and the declared integrated experiment. I found no
scientific or executability defect that invalidates the proposed comparison.
Planned research value is supporting; paper impact is a constructor/workload
boundary and additional serving-path evidence, not a direct thesis challenge.
Admission does not assert a correctness or performance result: the candidate
has not been compiled or exercised by this reviewer.

The retained user question is clear enough to test without inventing a formal
paper RQ: improve delivered latency/TPS of the complete Linux TCP/HTTP,
eBPF/sockmap, shared-queue, resident reused-model GPU and asynchronous kernel
TCP send path with no steady userspace request worker. docs/evaluation.md and
finding0053 retain exactly that scope. No paper thesis contract or new RQ was
introduced. Source selection remains dependent on the actual completed
correctness/performance evidence and its limitations.

## Evidence inspected and current state

I read the skill, current plan.md, original and prospective io_uring_tcp.h,
implement.py/proposed.diff, prepare.py/rebuild_original.py/Makefile.original,
run.py, ordinary short/transfer clients, analysis.py, qualification and
lifecycle recipes, runtime/build receipts and frozen-reference metadata.
I inspected current vllm_graph.cu, qwen_graph.cu, userspace_tcp.h, Makefile,
bpf/uring_loop.bpf.c, queue/control ABI and fusion.bpf.c ownership/recycle
paths, plus evaluation and finding0053. I parsed all eleven relevant Python
recipes without importing or executing their GPU paths.

Live HEAD is 34eb2b0b7b1d282d47766a4125df2e216c952c09 on main. Current transport
bytes equal the saved original header. Git status contains only unrelated
untracked tools/setup_env.sh. setup.exit.json records dependency/control
build completion exit0 at 16:50:07.704773 UTC. Expected Python, loader, loop
object and current/native control libraries exist. The plan is prospective;
no candidate application, build or actual preflight occurred in this review.

I independently reran only the existing CPU posthoc_long_rounds.py analysis
against all ten unchanged finding0053 transfer JSONLs. Its checks confirm
104 complete requests per executor, eight sequential warmups and two32-request
serial cells, admitted=retired104, successful terminal records, zero model
errors, nonoverlapping serial request timestamps and the2088-round deduction.
The captured native CUDA sources match the saved original; all ten captured
client_source strings match current bench/resident_dispatch.py.
The dispatcher increments its launch counter only after successful nonempty
model launches and publishes one token per selected request per round. Thus a
single valid active gen1/gen64 request contributes1/64 rounds in these serial
contexts. Client completion follows the last token's publication; the retained
final-send/recycle ordering prevents another serial request from adding an
unaccounted prior request to a model round.

Recomputed selected/native long/c8 means are260.6/261.8 Smol and259.4/260.8
Qwen. Selected-minus-native vectors are[-2,-1,-2,0,-1] and[0,-1,-2,-2,-2].
This authenticates aggregate round counts, not equal round shapes, GPU time or
mediation of throughput. The prior diagnosis is post-hoc exploratory evidence;
it does not retroactively become finding0053's declared primary result.

## Hypothesis and paper-value admission

The treatment directly tests whether replacing GPU-owned regular bookkeeping
storage improves delivered long-output throughput under the retained serving
constructor. It does not retest the unchanged final-drain intervention.
Source inspection finds frequent pending/accounting/error/record operations
through the mapped report while the host/BPF coordination accesses its control
prefix. Neither previous transfer counters nor prior published performance
can answer changing that storage placement. A private allocation can help,
have no detectable effect or regress because mandatory shared ring/page access,
model-round shape, compiler changes and delivery costs remain. This is not a
definitionally winning comparison.

Positive old-control effects support the local placement constructor. Negative
or inconclusive effects bound it and favor retaining the current policy; mixed
model effects narrow any candidate selection. A native win continues to limit
superiority even if the component control improves. These are different useful
implementation/evidence decisions, so this is not dependency-only activity.
Setup, protocol checks and restoration remain dependencies of this one
experiment, with no independent research contribution.

Bookkeeping placement is a reasonable strongest runnable next discriminator.
The88–92% excess-CQ fractions are whole-transfer multishot traffic counts,
not measured GPU-cost fractions. A timer-period sweep changes submission
latency as well as CQ traffic and is less discriminating at this point.
Actual receive SQEs already use asynchronous RECV with zero message flags;
there is no deliberate MSG_DONTWAIT empty-receive retry loop in this source.
New models or unchanged reruns do not resolve this concrete uncertainty.
The source-location treatment is stronger than merely counting more CQEs, but
it still changes compiled layout and control-pointer indirection. The plan
correctly disclaims isolated PCIe/cache/time or exclusive causal mediation.

## Baselines, workloads, metrics and inference

Native epoll TCP is the one main competitor: it implements the credible
alternative of efficient CPU delivery with the same resident reused vLLM math.
It is operational in the inspected source, uses nonblocking receive/send and
60us epoll_pwait2 completion waiting, and is rebuilt/rerun fresh. Matching or
beating the candidate changes the serving-path interpretation. A numerical
matched run is needed for this changed constructor; citation cannot settle it.
The saved host-bookkeeping coalesced path is correctly a component control,
not a second external main baseline. No extra baseline is required.

The original-source target reconstructs the same BF_URING_NETWORK,
BF_URING_BPF_LOOP, BF_IO_COALESCED, BF_PAD_PREFILL and BF_PREFIX_RELEASE
flags. Its normalized-SASS comparison is against the fresh saved current ELF;
it validates control reconstruction, not candidate equality. Native/candidate
share model code, runtime, compiler, FP16/KV, prompts, output budgets and
packed/prefix policy. Different scheduling/round shapes are possible outcomes
of the delivery mechanisms, not grounds for pretending model time is fixed.

Primary gen64/c8 output tokens/s is appropriate for delivered throughput;
its32*64 tokens divided by first measured send to last measured token formula
is explicit and independently recomputable. The plan links the official vLLM
benchmark page, which reports output-token throughput and defines client TTFT
and TPOT. Its source-native finite-cell boundary must remain explicit rather
than implying it ran the official vLLM OpenAI benchmark. Completion is the
last requested token arrival, not process exit or ACK. Token-ID HTTP/binary,
four short prompts and two small checkpoints are narrow but aligned with the
constructor question; arbitrary-text/model/SOTA claims remain excluded.

Five process blocks provide five paired cell contrasts, not3840 independent
samples. Five of six permutations and reversed model/context/cell order reduce
but cannot eliminate drift or residual order imbalance. Nominal t95(df4)
intervals assume the paired-block distribution is adequate at small N; they
are not simultaneous coverage, equivalence or noninferiority. Retaining all
signed rows and per-model interpretation is appropriate. Known-worker CPU is
partial process/attributable TX CPU, not all kernel/BPF/softirq/client work.
Sparse host observations give context rather than continuous isolation.

Primary interpretation is coherent: candidate-minus-old above0 supports the
narrow benefit; candidate-minus-native above0 additionally supports tested
finite superiority. Zero-crossing stays inconclusive. Secondary latency may
inform selection, but does not veto a valid throughput effect unless it breaks
correctness, fairness or the exact asserted claim.

## Prospective control, initialization and lifetime audit

IoStats begins with unchanged bf_uring_loop_control. Proposed IoState adds an
internal pointer only under BF_IO_COALESCED; source ABI for the shared queue,
BPF registration and host report region stays unchanged. The private object
is uploaded after bootstrap pending=1, so the indefinite timeout's pending
operation is retained. Its copied loop prefix is unused: io_progress reads
model_quiesced and writes finished through the new live control pointer to
original mapped dreport->loop. Host deadline/signal/stop/drain and BPF loop
access that same registered region. Neither host nor BPF uses ordinary
bookkeeping as a steady coordination input.

All normal GPU accounting, pending/error decisions and reply records use the
private out pointer. Cancellation, TIMEOUT_REMOVE, final SEND/abort tags,
FIFO final frontier, peer matching and physical slot recycling are unchanged.
The BPF completion path releases only the tagged exact final completion and
clears the same admission bit. No new request worker or timer is added.

vllm serve synchronizes the model stream before publishing model_quiesced,
launches the shutdown-only I/O worker, drains on shared finished, and performs
cudaDeviceSynchronize before uring_finish. Proposed finish additionally waits
for the network stream, downloads only the suffix beginning at
offsetof(IoStats,accepted), prints report/records and then frees state/stats.
It therefore preserves live control and retains the private allocation through
both model-root progress and shutdown work. Signal_control is nulled before
report unregistration. Early error paths keep the existing fail/exit behavior;
no successful clean-shutdown claim should be inferred from an abnormal exit.
Default/noncoalesced builds take the existing mapped bookkeeping path; all
relevant Make coalesced targets define the BPF loop too. AMK compatibility is
not qualified or transferred by this vLLM experiment.

## Commands, completion and remaining execution notes

The real paths are executable as written: setup receipt -> prepare.py control
reconstruction -> implement.py exact-source transform -> existing Make target;
run.py expands the20 full driver commands before running them. Two models,
two contexts, three paths and five blocks give60 executors/120 cells,
3840 measured requests124800 tokens plus480 warmup tokens. The four-driver
preflight yields12 executors/24 cells,192 measured requests6240 tokens plus96
warmups. Python recipe parsing passed; runtime behavior still needs the actual
fixed real preflight, which this review did not substitute.

run.py full is collection only: analysis.py TEMP full is a distinct required
next command. The wrappers preserve raw stdout/stderr/exit records and stop
at an actual failure rather than silently substituting another cell. Existing
client/executor timeouts, correctness, oracle and evaluation path stay fixed.
A failed or interrupted prefix is incomplete and must be preserved; the owner
must record any affected rerun/deviation rather than overwrite successful rows.
No observer timeout or terminal trigger establishes full completion.

One reporting detail needs explicit completion, but does not block collection:
TEMP analysis.py currently computes short-only rounds, not the predeclared
long/c8 counters or whole-transfer CQ summaries. The already inspected existing
posthoc_long_rounds.py can analyze the full TEMP's10 transfer files directly:

    python3 bench/results/final_drain_20261014/posthoc_long_rounds.py /tmp/bpfusion-device-stats-o8xxqd_q

For this new experiment those counters are prospectively secondary in plan.md,
not post-hoc merely because the reused script has that name. Preserve its
stdout and explicitly mark the new interpretation. Authenticate captured
source and timestamp subtraction as done above; do not blindly claim a
counter result from total launches alone. The script's2088 deduction and32
request checks are for the full run, not the8-request preflight. No primary
metric or additional GPU run needs changing to complete this analysis.

Candidate protocol qualification has the unchanged622-request/22224-token,
259-rejection/5000-empty-connection suite and reused-graph trace/history/KV
replay. Lifecycle uses the same whole-output pools, signal/reset/half-close,
32-action and complete-or-prefix scope. Driver success booleans alone do not
establish BPF physical FREE slots/bitmap/recycle or model quiescence; the plan
properly requires independently inspecting raw accounting, slot/queue and
shutdown/source receipts. Frozen pools permit only the known sequences and
are not independent fresh eager-HF parity. Prior strict AMK failure remains
failed. These limitations do not invalidate this matched vLLM constructor.

Full collection plus fixed raw analyses, every required qualification/lifecycle
receipt and fresh independent result review are the completion boundary.
Source selection/publication/restoration follow actual evidence, not ADMIT.

## References and reviewer boundary

Primary references checked live:
[CUDA zero-copy guidance](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#zero-copy)
supports device caching of repeatedly accessed mapped data as motivation.
[vLLM benchmark metrics](https://docs.vllm.ai/en/stable/benchmarking/cli/#understanding-the-latency-metrics)
supports the latency definitions and output-token-throughput terminology.
Neither proves the proposed workload's bottleneck or superiority.

I wrote only this review file. I did not edit the plan, production source or
raw outputs; implement/build/install/run GPU serving/preflight; stop sessions;
change runtime configuration; publish; or clean TEMP/build resources.
All read/CPU-analysis subprocesses have returned. I retain no active TEMP or
build handle; the owner can continue the admitted protocol.
