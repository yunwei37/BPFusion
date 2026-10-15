# Experiment plan: offered-load tail latency with request-driven waiting

## Research question and paper-value admission

Retain the user's existing Linux TCP/eBPF/shared-queue/resident reused-model/
asynchronous TCP server objective, no steady userspace request worker, and
improve latency/TPS. No formal paper RQ/thesis exists; do not invent or rewrite it.
Specific hypothesis: with identical optimized model computation and request-aware
waiting on both sides, GPU/kernel-owned serving reduces client P99 connect-begin-to-first-token latency at
64 requests/s without obtaining that benefit by failing requests.

Role: supporting load-dependent evidence toward the service question.
Largest credible story: a measured latency/load advantage over a credible native
mechanism, or a concrete limit showing that request-worker removal still does
not win under independent arrivals. The strongest reviewer objection is that
closed-loop burst means and a native fixed60us idle poll do not establish a
useful service advantage. Finding0060 supports partial process-CPU saving but
has adverse Smol burst TPS; prior fixed-concurrency data cannot reconstruct
unobserved independent arrivals or the improved native mechanism.

Positive results can select a useful measured service regime; negative/mixed/
inconclusive results retain current production defaults and narrow the claim.
This does not redefine success as CPU reduction, dependency readiness or a new
timer invention. Best alternative: another backend integration/port; existing
MPK RTX5090 compatibility is unqualified, AMK has a pinned fidelity failure.
This same-compute service test answers a more direct, runnable uncertainty
without a model arithmetic campaign. Total service CPU remains a separate
measurement gap; this loopback test will not falsely claim to close it.

## Mechanisms and comparison

Proposed: repaired adaptive before-submit BPF/io_uring loop from0060, preserved
production-candidate sources. No new unreviewed kernel alteration.
Single main competitor: native timed epoll with the same reused vLLM model
graphs/dispatcher. It keeps60000ns GPU-completion checks only while requests
are outstanding or a complete buffered request waits for a slot; otherwise
epoll waits for socket readiness or the remaining service deadline.
An eventfd wakes epoll persistently on shutdown, including helper-thread
signals, avoiding a signal-before-sleep lost-wakeup race. No request worker,
scheduler/controller or model math is added to the proposed side. All source
changes remain private until evidence warrants selection.

A fixed-idle-poll native repeat is an already-measured weak control for the CPU
question, so cite0060 instead of adding a third full path. Matched numerical
main comparison is still necessary: no published result answers this same
hardware/model/wire/control combination. A native match/win limits the service
claim rather than becoming a proposed-method victory.
Both use existing default optimized FP16 computation and BF_TRACE independent
history qualification, no profiler or upstream batch-invariant mode.
This tests traced serving; it cannot close0058's ordinary untraced pool failure.

## Published protocol, metrics and workload

Reuse source-native bench/vllm_serving.py, resident_dispatch.request()/connect(),
executor/vllm_graph.py graph/KV/history replay, existing622-request protocol and
32-action lifecycle procedures, official Makefile and the recorded0060 pinned
private setup. Necessary glue replaces only closed-loop cell scheduling with
independent arrivals and preserves every request's schedule/outcome.
Official vLLM serving benchmark defines Poisson arrivals, request rate and
TTFT/P99:
https://docs.vllm.ai/en/stable/cli/bench/serve/
Pinned upstream implementation:
https://github.com/vllm-project/vllm/blob/v0.31.0/vllm/benchmarks/serve.py
https://man7.org/linux/man-pages/man2/epoll_pwait2.2.html

Models/revisions: same cached Qwen2.5-0.5B-Instruct7ae557604adf67be50417f59c2c2f167def9a775
and SmolLM2-135M93efa2f097d58c2a74874c7e644dbc9b0cee75a2.
Four existing tokenizer prompts, gen64, token-ID HTTP and default TCP.
Rates4,32,64,96req/s bracket idle/moderate/near-capacity/overload using existing
continuous-load native observations (~75Qwen/~88Smol req/s); they are not
retuned after outcomes. Per rate/process256 requests,8 separate checked gen1
warmups. Five paired process blocks/model, alternating path order and rotating
rate order. Full20 executors80 cells20480 measured attempts1310720 requested tokens plus160
warmups. Separate models are not paired causal effects.

Precompute gamma(shape=1,scale=1/rate) intervals and normalize cumulative delays
to exactly N/rate as pinned vLLM0.31.0 does, fixed
seed20261015+block, and preserve identical per-block schedules across paths.
Each request is launched at its absolute scheduled monotonic time in a separate
source-native blocking request thread; there is no completion-driven admission,
client semaphore or configured concurrency cap. Record schedule, thread start,
connect begin/end, request send start, every token arrival, finish/error and
actual in-flight count. Preserve scheduling lateness; do not silently shift a
late schedule or trim it. Same loopback client shares host CPU, limiting cost
attribution and high-rate load-generator conclusions.

Primary: per-process linear-interpolated P99 connect-begin-to-first-token
latency at64req/s, proposed minus
native, five paired differences/model with nominal t95df4. P99 has only256
samples/block and wide uncertainty is a valid inconclusive outcome.
All failed/time-out attempts remain in the denominator and get their own
success/failure/request-throughput rows. A lower success rate cannot support a
no-failed-request latency advantage. If either primary cell has failed requests,
report conditional successful-request P99 descriptively and mark unconditional
primary superiority inconclusive/censored; do not pretend failures are fast or
drop them. An accepted output that fails independent model replay is a
correctness failure, not an overload success or an exclusion.

This follows the official endpoint timing boundary before connection setup;
retain source-native post-connect TTFT separately. Use the same linear
percentiles as NumPy/vLLM; the stdlib analysis implements that formula.
Secondary: all-rate P50/P95/P99 connect-inclusive and post-connect
TTFT/completion/TPOT, scheduled-to-first/last
latencies including client/connect delay, realized arrival rate, connection/
scheduling lag, successful request/token throughput, every failure, partial
executor process CPU/request and global CPU counters descriptive only.
No invented SLO, custom weighted score, total-service CPU/energy or saturation
capacity claim from a finite curve. CI crossing zero is not equivalence or
noninferiority; no multiple-testing correction or pooled cross-model claim.
Keep all path/block/arrival outliers.

## Execution and qualification

Original Workspace /workspaces/repository main9cfcf98a5dbda283c3e06474c74ca3aab59b65a6.
Private owned TEMP /tmp/bpfusion-offered-load-6k3zzurc.
No production files changed, private patch available for review.
Base packages/Coder processes/8original build/setup files, weights/global caches,
original Pod/PVC preserved; no host/driver/power/security/runtime-service change.
No new persistent entity/flag/framework.

Actual workflow command sequence in TEMP, to be implemented with source-native
scripts before execution:
python3 setup.py
python3 qualification.py
python3 load.py --preflight --model <cached-qwen-path> --output preflight_qwen.jsonl
python3 load.py --model <cached-qwen-path> --output full_qwen.jsonl
python3 load.py --model <cached-smol-path> --output full_smol.jsonl
python3 analyze.py <raw.jsonl>

Setup reuses pinned vLLM0.31/Torch2.13cu129/TF5.17/NP2.3.5/libbpf1.6.3/NVCC13.0.88.
Private source/header/BPF-object paths bind each actual build to its snapshot.
Both protocol paths/two models and unchanged frozen complete/prefix lifecycle
check natural stop/recycle; existing source-native socket60s/owning lifecycle
timeouts stay fixed. Native additionally checks zero-request2s deadline and
helper-stop while idle; the eventfd is shutdown-only, not model-completion I/O.
Preflight both paths on real Qwen,16requests each at4 and64req/s with the actual
scheduler/raw metrics/history replay; keep actual source versions and attempts.
No full run from a partial protocol/preflight or changed oracle/timeout.

Full completion means all20 process exits and80cells/20480attempts, failure
outcomes included, exact successful-output references, fixed analyses terminal.
Estimated full collection40-70min plus setup/protocol/lifecycle/replay, refined
from real preflight; this is not a deadline or investigation cap.
Log partial/failed work and resume only a valid missing suffix; do not rerun
unfavorable cells. Native/proposed connection capacities are their real current
constructors; overload capacity/rejection differences remain visible, not a
syscall-only effect. Actual rate scheduling and code must be reviewed for
unintended client backpressure before GPU execution.

Fresh plan review precedes real setup/preflight. Fresh result review follows
terminal full results. Save exact commands/sources/versions/raw outputs and
sparse actual host/PID/boot/fault receipts. No continuous isolation claim.
Archive coherent finding/evaluation/README/architecture and commit/push main
after source selection and own dependency cleanup. Selecting a retained shared
source patch needs its affected compatibility qualification; unselected private
constructors do not create broad supported-model claims.

## Interpretation and next decision

Supported primary negative difference with valid complete delivery can support
only this model/load/constructor's P99 advantage. Worse or inconclusive primary,
failure-censored tails, native win or mixed models do not establish a default
optimization. Partial CPU savings cannot replace latency primary. Keep original
source unless real service evidence warrants the extra complexity.
Impact is additional RQ evidence/mechanism-workload boundary, not a direct
thesis challenge or new novelty claim. Close the unchanged matrix after result
review; next work needs a different meaningful discriminator.

Pre-observation review correction: primary starts before connection setup;
retain post-connect timing diagnostically. Align schedules with pinned vLLM
cumulative normalization and percentiles with linear interpolation. Script
metadata preserves all original primary/secondary definitions. All full token
counts above are requested maxima; actual successful delivery is measured.
