# Experiment plan: adaptive kernel-loop wait for bursty serving

## Research question and admission
Retain the user's Linux TCP/HTTP/eBPF/shared-queue/resident reused-GPU-model/
asynchronous kernel TCP server, without a steady userspace request worker,
improving throughput/latency. No formal paper RQ/thesis/idea-story exists.
Specific uncertainty: can request-aware timeout updates reduce executor-process
CPU in bursty serving without introducing lost wakeups, deadline hangs or
adverse delivery? Role supporting, not a new model kernel or timer algorithm.

The largest credible result is lower coordination cost in a reusable network
path with independently history-checked delivery, or a concrete boundary showing
the handshake/timer tradeoff is counterproductive. A continuing reviewer objection
is that removing a userspace request handler does not demonstrate lower cost.
0055/56 leave native gaps;0057 does not identify an exclusive GPU bottleneck;
0058's default ordinary pool failure remains unresolved;0059 qualifies a slower
upstream mode but shows no throughput gain. None measures this idle/request-aware
kernel wait. Reanalysis cannot supply this unrun intervention.
The best alternative is total-host CPU/offered-load observation on unchanged
code, but host totals mix client/other jobs and cannot directly identify this
source-visible avoidable heartbeat. A safe source-local intervention outranks
another publisher fence/mapped-buffer micro-optimization. Record whole-host
ticks descriptively without attributing them exclusively to this service.
A positive result can select lower process coordination cost in this workload;
negative/mixed/inconclusive results retain original behavior and narrow the
constructor/workload claim. Neither outcome settles generic eBPF superiority.
No pool expansion, claim rewrite, new controller, public flag or host change.

## Mechanism and official assets
Current source emits a multishot timeout CQE every60000ns even while idle.
Current host BTF and official Linux7.3-rc3 io_uring/loop.c expose only CQ-index
waiting, not a timeout argument. Official timeout.c always posts multishot
-ETIME/MORE events. The tempting no-CQE wait is not an available drop-in API.
https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/loop.c
https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/timeout.c
Reuse existing IORING_TIMEOUT_UPDATE to change the same pending multishot timer
between60000ns with outstanding requests and remaining service deadline while
idle. No arbitrary idle tuning constant is added. A GPU CQ-processing ack
precedes kernel SQ sampling/sleep while the timer may be idle; this closes the
network-CQ/GPU-SQE lost-wakeup window. Kernel monotonic time in the existing
registered report supplies the remaining relative interval. Update completion
and transient ENOENT/EALREADY are handled; stop/cancel still drain existing ops.
Qualification exposed a real helper-thread stop wakeup defect before the full run: publish stop_requested and forward shutdown SIGTERM to the recorded loop-owner TID when received on a different thread. This changes shutdown only and adds no steady request worker. Rerun both candidate protocol/lifecycle suites with distinct repaired output paths; preserve the manually cleaned first attempt as failed liveness evidence.
The candidate touches only shared loop control, BPF loop and GPU network helper.
The existing BF_IO_CQ_AFTER_SUBMIT variant keeps its original fixed timer and wait behavior; adaptive behavior is limited to the before-submit loop because the after-submit ordering has a reviewed lost-wakeup counterexample. No new flag is added.
Model kernels, graph construction, dispatcher, weights, precision, prefix policy,
admission semantics, private capacities, current active timer and host remain.
Actual pending patch/original snapshots are in this OS TEMP. Inspect real code.

## Comparison and fidelity
Candidate: adaptive existing vllm_graph_uring_loop_trace.
Component ablation: original fixed60000ns vllm_graph_uring_loop_trace.
Single main competing mechanism: efficient native vllm_graph_user_network_wait_trace
with identical default optimized FP16 graph/model computation.
Native is actual epoll/nonblocking TCP, not Python per-token dispatch.
A native match/win limits the overall service story even if candidate beats
the component ablation. Matched runs are necessary on this workload; prior
published numbers lack the idle gaps and intervention.
All conditions use BF_TRACE for exact independently reconstructed graph/KV/
history output checking; no profiler or upstream batch-invariant flag.
This is deliberately a traced default-compute comparison, not a claim about
ordinary untraced output fidelity or direct numerical comparison with0059.
Existing default ordinary reference-pool failure is not repaired/retried.

## Workload, standard metrics and uncertainty
Use two existing fixed cached checkpoints/revisions (Qwen2.5-0.5B-Instruct
7ae557604adf67be50417f59c2c2f167def9a775 and SmolLM2-135M
93efa2f097d58c2a74874c7e644dbc9b0cee75a2), four existing tokenized prompts,
same HTTP token-ID wire. Standard metric definitions:
https://docs.vllm.ai/en/stable/cli/bench/serve/
https://man7.org/linux/man-pages/man3/clock_getcpuclockid.3.html
Source-native client request timestamps define TTFT/completion/TPOT;
existing POSIX executor process CPU clock counts all executor threads.
Primary: executor-process CPU seconds/request in gen64/c8 bursty cell,
candidate minus original, five paired process blocks/model.
This excludes some RX/softirq/io-wq/other kernel CPU; never call it total CPU,
energy or an exclusive BPF cost. Native CPU is the main competitor boundary.
Secondary: all delivered TTFT/completion/TPOT and wall token/s (includes fixed
idle gaps), native contrasts, gen1/c1 cold/warm boundaries, global host ticks.
Wall token/s is achieved delivery under this fixed burst pattern, not saturation
capacity. The predeclared first-by-client-start request of each wave can be reported as a cold
subset; no post-hoc convenient exclusion. Do not substitute latency for primary.

Each full process:8 sequential checked gen1 warmups, then cells gen1/c1 and
gen64/c8. Each cell has four waves of8 requests, with1s quiet gaps after waves
0/1/2. Total32 measured requests/cell,64/executor2080tokens plus8warmups.
Forc1 each wave's eight requests are sequential; forc8 all eight begin via
existing barriers. Keep connections/driver timing definitions documented.
Five paired process blocks rotate six permutations of three conditions and
cell order. Qwen then Smol; no between-model causal claim.
Full30executors60cells1920measured requests62400tokens plus240warmups.
Nominal paired t95df4, signed differences; CI crossing zero is inconclusive,
not equality/noninferiority. Record all effects/outliers and partial CPU limits.
Lower CPU alone does not justify default selection if delivery/regressions fail;
inconclusive latency cannot prove no penalty.

## Concrete workflow and correctness
Base main d87b8e0bc1584123f2c0296ae13ab2dac999a2d6 in original
yunwei356/bpfusion-dev /workspaces/repository. Keep existing WIP/build8paths,
base Torch2.14.1/TF5.19/NP2.5.3, Coder processes, cached weights and shared caches.
Private setup reuses source-native Makefile and pinned vLLM0.31/Torch2.13cu129/
Transformers5.17/NumPy2.3.5/libbpf1.6.3/NVCC13.0.88. Original and candidate
builds use exact snapshotted sources/headers; private bootstrap only redirects
the BPF object path to the matching private build. Native uses original source.
No persistent runtime config, driver/clock/power/kernel/permission changes.

One command sequence in owned OS TEMP: python3 run.py setup, preflight,
qualification, full. Scripts/expanded vectors/env/raw/stdout/stderr retained.
Private serving adapter reuses bench/vllm_serving.py, changes only matrix/
source paths/wave gaps and captures process CPU before first wave/after last.
Existing analysis independently checks every request against exact upstream
graph/KV/history replay, native/loop engagement and ring lifetime invariants.
No reference pool is used for this matrix. All trace capacity/overflow checks
remain fixed; bounded network reply diagnostic overflow is a separate counter.

Real preflight: actual Qwen original/candidate/native, both cells, one process
each; same four waves/gaps and metric/raw path. Includes actual candidate
empty/idle deadline exit with real model and two-second service duration.
Retain actual source-native60s client/socket timeout (the earlier15s statement was incorrect); the separate empty deadline check has a fixed15s post-ready observation bound. Record a deadline hang as failure.
At most three preflight attempts under owning skill; no oracle/timeout widening.
Qualification: candidate both models, existing622-request protocol including
259 rejections/5000empty connections, all concurrency1..8, exact independent
history replay and all-thread network checks. Exercise idle-before-request and
in-flight stop/reset using existing source-native lifecycle procedures; preserve
their frozen output prefix controls rather than silently widen them. A failure
closes that path or gets a documented source repair with affected reruns.
HF/after/coalesced compatibility must be described accurately: shared helper
changes require affected regression before selecting a production change, not
a universal support claim based on the main matrix.

Full only after preflight/qualification succeed. Require all planned cells,
requests, traces, analyses, and terminal statuses; never call a prefix complete.
No excluded/replaced/failing-output rerun until favorable. Preserve every failure.
Record sparse host GPU/PID/ownership/boot/warnings before/active/after tied to
actual processes; no continuous-isolation claim.
Fresh plan review before actual setup/run, fresh result review after terminal.
Expected full cost roughly30-40min plus protocol/lifecycle setup, refined from
actual preflight; this is not a deadline or investigation limit.
Archive exact source/patch and raw results, restore unselected candidate,
remove only owned runtime/build, verify original state, update honest OSS
evaluation/finding/docs, main commit+push under user authorization.
No production selection is pre-authorized by a plan/reviewer; selection follows
actual correctness/performance and repository default-first policy.

## Interpretation
Primary CPU reduction with valid delivery supports this finite bursty mechanism
only. An adverse/native-winning result bounds it; mixed or CIs crossing zero
remain inconclusive. Any lost wakeup, deadline, FIFO, output or resource failure
invalidates its performance comparison and cannot count as a candidate win.
Do not infer universal CPU elimination, full-service CPU/energy, saturation TPS,
ordinary untraced equivalence, new model optimization or a direct thesis result.
Target table: process CPU/request and standard latency/delivery for all three
conditions/two models, with signed block-level uncertainty and unavailable cells
where execution fails. Larger goal remains active after this experiment.
