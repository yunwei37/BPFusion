# Same-compute service tails with fair native admission

Prepared 2026-10-15 UTC from main70988bed7d25f313e85277fa420894f1ff835bcf.
Private sources are unbuilt and unexecuted; main application source is unchanged.

## Retained question and admission rationale

There is no formal paper RQ/thesis/idea-story contract. The retained user
objective is complete Linux TCP/HTTP + eBPF/shared queue -> reused resident
real-model GPU -> asynchronous kernel TCP TX without a steady userspace request
worker, reproducible correctness and improved latency/throughput.

Finding0062 completes15360 successful measured requests with the finite FIFO
kernel loop and an event-driven native competitor. Its fixed64/s P99 effects
are inconclusive. At secondary Qwen96/s, kernel/native P99 is280/1418 ms but
P50 is134/30 ms and process CPU is higher on kernel. Subsequent saved-trace
analysis finds native maximum bypass by later-client-stamped requests
149/175/165/72/159 versus1/2/2/1/1 on kernel. Stamps are not exact ingress times.
The native source scans peers in FD order, allowing newly recycled lower-FD
peers to precede already waiting higher-FD peers. Thus scheduling fairness is
a concrete competing explanation for the apparent high-load tail advantage.

Hypothesis: on this finite high-load workload, a kernel-loop TTFT-P99 advantage
persists against event-driven native TCP after replacing FD-priority admission
with FIFO among complete eligible native frames. The largest credible story is
conditional complete-service value beyond the exposed native fairness weakness;
it cannot establish syscall-only causality, first-system novelty or a generic
model compiler. Role supporting; impact mechanism/workload boundary.

A positive matched result permits only a bounded advantage against this stronger
competitor. A loss-free inconclusive/adverse result withdraws any general tail
advantage inference and prioritizes actual coordination/compute costs. If native
FIFO ordering does not engage or an avoidable native implementation/interface
failure occurs, it is not a kernel win. No outcome proves the previous
FD-priority result was a causal old/new effect estimate.

This adds new evidence that raw-data reanalysis cannot supply: a matched real
execution after removing the known avoidable admission priority. Another timer
or model arithmetic change is a weaker next use of effort while that reject
argument remains. Do not rerun the obsolete FD-priority native as a main
baseline or add weak throughput rows. Its published full data remains context,
not a simultaneously matched causal ablation.

## Implementation and comparator

The only main competitor is private native eligible-frame FIFO TCP, the
stronger available current alternative. Both paths use the same snapshotted
vllm_graph.cu, FP16 upstream graph banks, KV setup, packed prefill/prefix release,
weights, prompts and batch limit8. The kernel constructor is unchanged from
the independently reviewed and integrated finite FIFO driver.

Native adds a deque of complete eligible frames, one queued entry per Peer.
Enqueue occurs when receive readiness reveals a complete frame or a prior reply
retires. FIFO head obtains the same next physical model slot; no FD scan can
overtake an already queued eligible frame. Existing framing/rejection, response
streaming, 60us active epoll progression, idle socket/deadline wait and eventfd
shutdown remain. A shared_ptr keeps an old/reset Peer distinct from a recycled
FD; disconnected queued entries are skipped. No model math, CPU placement,
transport flags, new public mode, persistent configuration or external worker.

This aligns fairness class within the measured one-request-per-connection
workload, not every protocol policy. Native retains one active response per
connection; the kernel can pipeline multiple frames into model slots. Eligible
observation/event order is not identical to BPF ingress order. Native buffering
is not given an artificial new cap; the kernel remains finite4096 FIFO with
drop-on-full. No full cell approaches that limit or supports arbitrary overload.

## Workload and fixed metrics

Same cached revisions of Qwen2.5-0.5B-Instruct and SmolLM2-135M; same four
short prompts and gen64. Both paths identically BF_TRACE, with the unchanged
independent upstream body/head graph, metadata, KV/history and output replay.
The candidate's own outputs never define the oracle.

Full matrix: rates64,96 requests/s,256 attempts/cell,five paired process blocks
per model. Alternate path order and rotate the two rate orders. Identical
per-pair normalized cumulative gamma(shape1) absolute schedules from pinned
vLLM0.31/NumPy2.3.5,seed20261015+pair. Independent request threads, no
completion cap. Total20 executors,40 cells,10240 measured attempts,
655360 requested output tokens,plus160 checked gen1 warmups. Low-load4/s is
not repeated: the unresolved question is the previously exposed high-load tail,
and low-load costs remain in0062 without transferring a new low-load claim.

Primary per model: kernel-minus-FIFO-native connect-begin-to-first-token P99
at96/s, five paired nominal t95df4. This is a NEW follow-up hypothesis motivated
by0062's secondary observation; do not relabel0062's original64/s primary.
Any failed primary request censors superiority. Intervals crossing0 are
inconclusive, never equivalence. Secondary64/s tails, P50/P95, completion
tails, scheduled-origin metrics, TPOT, delivered requests/tokens per complete
cell window, failures/partial outcomes, scheduling lag and partial process CPU
all remain. Keep adverse median/CPU/throughput effects and outliers.

Source-native metric definitions/protocol:
https://docs.vllm.ai/en/stable/cli/bench/serve/
https://raw.githubusercontent.com/vllm-project/vllm/v0.31.0/vllm/benchmarks/serve.py
This token-ID HTTP adapter reuses the arrival/metric protocol; it is not an
official text/JSON endpoint benchmark.256 attempts put few observations in a
P99 tail: no P99.9, precise rare-event or steady-state capacity claim. Five
sequential paired blocks on a shared host give nominal finite-run uncertainty.
Partial process CPU excludes client/RX/softirq/io-wq work and energy.

## Executable path and dependencies

Only original yunwei356/bpfusion-dev Workspace; main and original WIP/build
artifacts/Coder sessions/base packages/weights remain intact. No concurrent GPU
experiment or other writer. Source copies here are snapshots,not checkouts.

Run /usr/bin/python3 -u setup.py here. It creates only a test-local runtime,
reuses the prior pinned installed package versions and libbpf1.6.3, then normal
Makefile rules with only source inputs rebound. BUILD is one private directory
for loop/native binaries and BPF objects. No module or ABI change is introduced,
so do not repeat unchanged module/non-loop compatibility as a paper experiment.

Run qualification.py. Two native idle deadline/helper-stop cases establish
eventfd and epoll engagement. For each model, the existing fixed correctness
driver runs loop/native, each640 outcomes/23376 replayed tokens, batches1..8,
fragmentation/reuse/wrap/reject/pipeline/half-close/helper stop. Native existing
32-action lifecycle checks frozen whole outputs and partial/reset/stop outcomes.
That lifecycle is not new proof of cancellation for a large queued backlog.
Queued-entry reset handling additionally receives source audit; the full
measurement has no deliberate reset/stop before drain. Do not claim unobserved
canceled responses are complete numerical checks or broad lifecycle coverage.
Unchanged loop lifecycle evidence remains in0062.

Run preflight.py: Qwen,one pair,32 attempts/rate at64 and256/s,both paths,
128 measured requests8192 tokens plus16 warmups. Both paths must run with
fixed full timing/CPU collection and replay. Native USER_ADMISSION reports
FIFO policy,executor-wide peak and queued_at_stop; final backlog must clear.
Report whether positive backlog pressure actually engages; do not infer it
from configured rate. Existing driver retains300s lifetime and60s socket timeout.
At most three preflight attempts; failures and repairs remain recorded.

After successful preflight run /usr/bin/python3 -u full.py. Both model drivers,
all20 executors and fixed analyses must reach terminal. No favorable cell
replacement, model-oracle/timeout/metric relaxation or failed-attempt deletion.
A systematic execution defect needs an explicit record and affected rerun.

analyze.py replays coverage,timestamps,schedules,client/reference output bytes,
complete model-history/counter ownership and nominal paired effects. Native
must report the FIFO mechanism and empty final deque. Existing admission_order.py
compares client-stamp and GPU admission order for every full cell as a mechanism
diagnostic; not exact ingress order or a newly invented paper score. It must be
interpreted with event/client scheduling and eligibility differences. Large
bypass or lack of queue engagement invalidates fairness attribution rather
than creating an automatic speedup. Source and raw independent replay must
also establish native uses the same computation and a real engaged wait path.

Before/full/after host observations retain boot/GPU ownership/ambient CPU scope.
Use actual phase timestamps; a setup/replay snapshot is not measurement
exclusivity. Do not stop other Workspace processes or alter host settings.

## Result review, decision and restoration

Setup/qualification may take tens of minutes; full roughly40minutes depending
on host/replay. No partial prefix is the experiment result. One fresh plan
review with at most two followups, one result review after complete collection.
Review fairness/source bindings,actual queue engagement,history/wire numerical
fidelity,all results/failures,uncertainty and competing explanations. No desired
verdict. No reviewer verdict authorizes broader scope or endless reruns.

After review, retain honest full positive/adverse/mixed evidence; select native
FIFO into main only if its correctness/lifecycle scope justifies adoption.
Do not promote kernel performance merely because a dependency passes. Cleanup
only owned runtime/build/source snapshots after archive and no live users,
prove original state preserved and all copied CPU analyses replay without
temporary paths, update OSS docs in paragraphs and commit/push own paths on main.
The full retained project objective remains active regardless of this result.
