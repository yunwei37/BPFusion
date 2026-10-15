# Pending admission under offered load

Prepared 2026-10-15 UTC. Scope: kernel-side waiting/admission around existing
reused GPU computation. Do not modify the currently running offered-load
experiment or its source, timeout, oracle, workload or raw outputs.

## Retained question and admission

No formal paper RQ, thesis, docs/idea-story.md or docs/user-instruction.md exists.
The retained user objective is a complete Linux TCP/HTTP + eBPF/shared queue
to resident real-model inference and asynchronous kernel TX, reproducible matched
correctness and latency/throughput, with no steady userspace request worker.

The current offered-load run is still active. Its first complete Qwen pair
has 27/256 kernel timeouts at64 requests/s and67/256 at96; native completes all.
All96 failed markers are absent from independently replayed model admissions.
The eBPF verdict drops valid frames when the eight physical model slots are
reserved. These are preliminary observations, not the full experiment result.
The prior0060 experiment saves idle process CPU but establishes no general
latency/throughput benefit. That evidence makes another timer or model-math
micro-optimization a weaker next action than repairing admission under load.

This is supporting evidence for the retained question. Largest credible story:
the complete driver handles a finite offered-load workload without shifting
unserved requests out of successful-request tail statistics; any lower tail
latency must survive a strong same-compute native comparator. It cannot prove
first-system novelty, arbitrary load reliability or a generic model compiler.
Positive results allow a bounded complete-service tail claim; loss-free but
inconclusive/adverse results establish only a repaired boundary and no speedup;
continued failures reject the candidate's service improvement claim. This
tests an implementation/workload boundary, not a necessary thesis prediction.

## Candidate and comparator

Private candidate/ contains the exact currently tested adaptive-wait source
plus a FIFO BPF pending queue, with capacity discovered from the existing
somaxconn/sockhash authority. Only the existing sleepable io_uring BPF loop
consumes that queue into unchanged eight model slots. The CPU atomic reservation
and kernel TX recycle owner remain unchanged. GPU reads the backlog count and
acknowledges newly admitted work before kernel sleep. EOF/dead connections
cannot recycle while queued work is pending; stop still discards unadmitted
work as the service shuts down, with counts retained.

This is a finite admission backlog, NOT complete TCP backpressure. If that
backlog fills the current candidate still drops, and that remains a failure
boundary to document. No BPF_EXIST overwrite, larger model batch, changed
model math, new steady userspace worker or new public flag is permitted by the
candidate's intended mechanism. Queue capacity is a runtime resource, not an
arbitrary performance knob. The loader supports the existing non-loop path:
only loop bootstrap sets the existing owner word to enable queued admission.

The only numerical competitor is the exact event-driven native TCP source
from the active offered-load run, with the same new tail-only page layout.
It represents efficient CPU orchestration with buffering and the same GPU
graphs. If it matches/wins, kernel-path superiority is not established.
The old dropping constructor is already measured by the active full run;
do not rerun it as a new weak baseline. No additional SOTA rows are needed.

## Workload, metrics and protocol

Same cached Qwen2.5-0.5B-Instruct and SmolLM2-135M, FP16, optimized vLLM graphs,
packed prefill/FIFO prefix release, four existing prompts, gen64, eight model
banks. No profiler or batch-invariant setting. Both paths use identical BF_TRACE
and independent upstream graph/KV/history replay, never method output as oracle.
Reuse source-native bench/vllm_serving.py-derived load.py and resident client.

Reuse pinned vLLM0.31.0 normalized cumulative gamma(shape1) schedules, linear
percentiles and the existing independent-thread, absolute-time release path.
Full: rates4,64,96 requests/s,256 attempts/cell, five paired blocks/model,
alternating path order and rotating rate order. Total20 executors,60 cells,
15360 measured attempts,983040 requested output tokens plus160 checked warmups.
Rate32 from the current run adds no unique next discriminator and is omitted.
Same seed20261015+pair, same schedule within each pair, no client concurrency
cap or completion-driven releases. Connection, scheduling, wire arrival,
partial response, exception and all attempt denominators remain recorded.

Primary: per-model kernel-minus-native connect-begin-to-first-token P99 at
64 requests/s, five paired process-block nominal t95(df4). Lower favors kernel.
Superiority cannot be claimed if any primary requests fail; report the complete
failure denominator and censoring explicitly. Success-conditioned quantiles
are still reported descriptively. CIs crossing0 mean inconclusive, never
equivalence. Same model computation does not imply syscall-only attribution.

Secondary: TTFT/completion P50/P95/P99, scheduled-arrival TTFT/completion tails,
TPOT, successful requests/s and output tokens/s, failures/partial responses,
client scheduling lag, executor process CPU and descriptive global host ticks.
Process CPU is not total kernel/softirq/io-wq CPU or energy; loopback shares host
CPU.256 requests yield only a few observations above P99; do not claim stable
P99.9. Five blocks are finite repetition, not a steady-state capacity proof.

Definitions/protocol sources:
https://docs.vllm.ai/en/stable/cli/bench/serve/
https://raw.githubusercontent.com/vllm-project/vllm/v0.31.0/vllm/benchmarks/serve.py
https://kernel.org/doc/html/next/bpf/map_queue_stack.html

## Real execution and controls

All edits/builds/tests run only in the original bpfusion-dev Workspace on main.
Source snapshots here are not checkouts. Preserve root tools/setup_env.sh,
the original eight setup/build file stat records, base packages, Coder sessions
and cached weights. No existing running experiment is changed or interrupted.
Do not build/start the new comparison until the existing full reaches terminal
and its raw results have been secured and reviewed.

Prepare with /usr/bin/python3 -u setup.py in this directory. It uses normal
make rules rebound to private candidate/ and native/ inputs, builds the
private fusion loader/object and both traced/untraced paths, and installs the
same pinned runtime as the current run in owned temporary directories.
The page adds8 tail bytes without changing existing slot offsets. The existing
module explicitly requires map->value_size==sizeof(*page), so old module binaries
must be rebuilt. Setup therefore also runs make -C candidate/module CC=gcc-15,
against the same private queue header. qualification.py first runs the existing
tests/kernel_tx.py with paths rebound in module_compat.py to the private loader
and module; its incompatible-map, byte/send/recycle and reset cases are unchanged.
This is a layout/transport compatibility dependency, not a real-model result.
The original module/build files remain preserved and no module is loaded while
the current full run is active.

Run qualification.py for existing full real-model protocol, fragmented and
pipelined HTTP/TCP, idle/helper-stop, half-close, reset and in-flight stop checks.
Retain the frozen pre-observation lifecycle/whole-output controls unchanged.
The actual compatibility commands are runtime/bin/python load.py --uring
--correctness --model <cached-model> --output protocol_compat_<model>.jsonl
for each model; setup builds vllm_graph_uring_trace and qualification.py invokes
them. Queue stays disabled there. Main loop/native protocol expands the existing
half-close pipeline from6 to24 requests, retaining exact independent replay;
compatibility keeps6. Loop lifecycle adds24-request backlog RST and64-connection
backlog stop with explicit before-action queued>8 receipts, then recovery/cleanup.
All observed stop wire prefixes use unchanged frozen complete outputs. Requests
whose replies are intentionally unobserved after RST remain canceled/unobserved,
never claimed complete or numerically checked. Native retains original32 actions.
New pending pin is included in the existing lifecycle cleanup list. No fixture-only test substitutes for serving.

Run preflight.py: Qwen, one pair,32 attempts each at4 and256 requests/s.
This is an execution/mechanism check, not a performance result. Record admission
backlog peak, counters, full model replay and zero final queue/reservation.
If it never actually exceeds model-slot pressure, report that limitation and
use the full96-rate observation to establish engagement, not fabricate it.
At most three preflight attempts; fixes and all failures remain recorded.

Then run /usr/bin/python3 -u full.py. Each source-native driver retains its
300s executor lifetime,60s socket timeout and15/30s existing lifecycle waits.
Both model drivers must reach terminal; analyze.py recomputes full coverage,
timestamps, schedule identity, tokens/references, counters, and signed effects.
Do not change timeout/oracle/metric after observation, replace favorable cells,
drop errors, or treat a partial prefix as the complete experiment.
A real source/runtime defect needs recorded repair and affected comparisons.

## Cost, output and interpretation

Setup and qualification may take tens of minutes; full is roughly an hour
depending on timeouts, plus independent replay. No competing GPU run.
One plan, one plan-review.md, all raw outputs, one fresh result-review.md.
Main table: each rate/model/path's failure fraction, TTFT/completion P95/P99,
delivered throughput and partial process CPU; primary paired differences and
uncertainty separately. Keep all adverse/mixed rows and initial failures.

After actual terminal, fresh independent result review audits completion,
baseline engagement, queue/wakeup/EOF/stop ownership, independent correctness,
all metric recomputation, failed-request censoring, and uncertainty. Report
valid/invalid/incomplete, supported/contradicted/inconclusive, supporting value
and implementation/workload boundary. No reviewer verdict is an approval
to broaden the goal or weaken the experiment.

A correctness repair may be retained only after real protocol/lifecycle and
matched evidence; performance promotion needs honest full results. Preserve
source/raw failures and annotate finite queue overflow limitation either way.
Remove only owned temporary runtime/build outputs after no live users, prove
original state preserved, archive replayable artifacts, update existing OSS
docs in paragraphs, and commit/push validated own paths on main. Root default
source remains unchanged until validation; publication is already authorized.
The full user goal stays active regardless of this experiment's outcome.
