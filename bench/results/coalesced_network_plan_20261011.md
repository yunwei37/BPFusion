# Matched network comparison after HTTP header/first-token coalescing

## Objective and admission

The repository has no formal paper RQ or thesis contract. This is a supporting
engineering experiment under the retained user objective: improve throughput
and latency of ordinary Linux TCP/HTTP + eBPF/sockmap -> shared queue ->
resident real-model inference -> asynchronous kernel TX, while reusing model
compute and comparing against credible optimized userspace request control.

Question: with identical resident GPU computation and default server TCP,
does removing the native userspace request/reply worker improve client latency
or throughput once BOTH transports submit the HTTP header and first available
tokens in one vectored send?

The largest credible outcome is additional evidence for the complete serving
path with existing computation, on two architecture families. It cannot prove
SOTA, real-NIC performance, total CPU savings or novelty.

Finding0025 supplies 80 valid cells but retains a roughly40ms plateau in both
transports. Finding0018's separate packet traces motivate header/body ACK/Nagle
buffering. Candidate coalescing changes an observed transport mechanism while
holding computation fixed, so this is not an unchanged repeat. Correctness and
passive traces are dependencies, not additional scientific contributions.

Positive primary intervals support only the measured latency/throughput
conditions. Negative intervals contradict superiority for those conditions.
Crossing-zero intervals are inconclusive, not equivalence. A mixed result is
reported by metric/model. None alone refutes the user's larger engineering
objective. If coalescing removes the plateau but the optimized native control
matches or wins, the next decision is to report that boundary and investigate
attributed host cost, contention/tails or physical networking, not tune model
math or add weaker baselines.

This outranks more model-specific kernel forks: the complete path and strict
compute are already available; the untested load-bearing issue is fair control
comparison after the common transport problem is repaired.

## Conditions

Reuse bench/resident_dispatch.py unchanged. Strongest runnable fair comparison
is resident kernel request/reply versus native user-network epoll request/reply,
both using the SAME FP16 HF graph executor, 8 private graph/KV banks and device
dispatcher. The optimized control submits whole resident GPU requests and does
not incur a deliberately slow Python token loop. This is a component ablation,
not an external SOTA baseline; TensorRT/SGLang comparisons remain separate.

Models: HuggingFaceTB/SmolLM2-135M and Qwen/Qwen2.5-0.5B-Instruct.
Matrix per model: output lengths1/64 crossed with closed-loop clients1/8.
Five paired process blocks, alternating mode order and rotating matrix order.
64 measured requests per cell, balanced four real prompt cases; eight warmups
per process precede measurement. Planned totals:80 cells,5120 requests,
166400 exact measured tokens,20 normal executor exits.

Both transports coalesce valid HTTP header/first tokens; kernel uses kvec and
tcp_sendmsg_locked, userspace uses iovec/sendmsg. Rejection/partial-send,
DONE/FREE/FIFO semantics remain unchanged. Server TCP defaults; existing common
client TCP_NODELAY remains. No QUICKACK, server NODELAY, sleep tuning, precision,
sampling or model arithmetic change. Anonymous versus kernel page backing and
polling still differ, so this cannot attribute an effect to syscalls alone.

Build/strict qualification receipts must precede collection:
tests/resident_qwen.py --gen 64 --prefill-edges, each transport x each model.
Expected per regression:335 exact valid replies/20432 tokens,259 rejections,
5000 empty connections, eight-client concurrency/ring reuse/mixed lengths/
pipelining/half-close/helper-thread signal termination, graph_error0,1 resident
launch; user accept/receive/send traced, kernel none after ready.
Numerical oracle, native timeout and correctness path are fixed.

Existing bench/tcp_stream_trace.py supplies passive loopback metadata and
independent eager HF token agreement for four real prompts/8 output tokens.
Run sequentially for each candidate transport/model after qualification.
Inspect whether a response header packet contains token bytes and whether any
long ACK-delayed gaps remain. Packet-arrival observer scheduling is a limitation.
These traces are mechanism diagnostics, not performance results and not a
matched old/new speedup comparison. Preserve failures and original exits.

## Metrics and interpretation

Primary latency: mean client TTFT for gen1/clients1; effect user minus kernel.
Primary throughput: aggregate output tokens/s for gen64/clients8; kernel minus
user. Five paired estimates and nominal two-sided Student t95(df4) intervals,
computed by native analyze(); four model/metric intervals are descriptive
without a family-wide significance claim. P50/P99 TTFT, TPOT, completion,
other matrix cells and per-pair values are secondary context.

TTFT/TPOT definitions follow vLLM's official serving benchmark metrics:
https://docs.vllm.ai/en/latest/api/vllm/benchmarks/serve/
Same-compute comparison precedent: Blink section6.1 compares the same TensorRT
engines to isolate orchestration (https://arxiv.org/html/2604.07609v1).
Native measurement retains monotonic request/token arrivals; tokens in one recv
share an arrival timestamp. Independently reconstruct all cell TPS and
latency/TPOT summaries, token agreement, order and paired intervals.

Executor process CPU excludes kernel TX/softirq. Global /proc/stat includes
clients and unrelated host work, so CPU numbers are descriptive and cannot
establish service-attributed savings. Preserve GPU clocks/power/temp per cell.
The existing SGLang service stays running on shared RTX5090. Record original
service process, GPU residency and host health before/during/after; pairing does
not prove the GPU was interference-free. All published claims remain
loopback/token-ID HTTP, short prompts, two small checkpoints and that hardware.

No causal old-versus-new coalescing speedup is claimed. Comparing this run's
numbers to finding0025 is historical context only. A quantitative optimization
effect would require a separately matched before/after experiment; it is not
silently inferred from these independent runs.

## Execution, evidence and completion

Run only in original yunwei356/bpfusion-dev Workspace /workspaces/repository,
on main. Preserve existing service and unrelated tools/setup_env.sh. Commit/
push qualified source and this plan before full collection; freeze commit,
commands, sources, configs and native raw outputs. No concurrent experiment,
new Workspace, external clone, model deployment, custom control interface or
runner replacement.

Exact preflight commands, sequentially:
```bash
HF_HOME=/workspaces/.cache/huggingface /usr/bin/python3 bench/resident_dispatch.py --preflight --gen 64 --resident-executor ./build/qwen_graph --user-network-executor ./build/qwen_graph_user_network --model HuggingFaceTB/SmolLM2-135M --output bench/results/coalesced_network_smol_preflight_retry1_20261011.jsonl
HF_HOME=/workspaces/.cache/huggingface /usr/bin/python3 bench/resident_dispatch.py --preflight --gen 64 --resident-executor ./build/qwen_graph --user-network-executor ./build/qwen_graph_user_network --model Qwen/Qwen2.5-0.5B-Instruct --output bench/results/coalesced_network_qwen_preflight_retry1_20261011.jsonl
```

Exact full commands, sequentially:
```bash
HF_HOME=/workspaces/.cache/huggingface /usr/bin/python3 bench/resident_dispatch.py --gen 64 --resident-executor ./build/qwen_graph --user-network-executor ./build/qwen_graph_user_network --model HuggingFaceTB/SmolLM2-135M --output bench/results/coalesced_network_smol_retry1_20261011.jsonl
HF_HOME=/workspaces/.cache/huggingface /usr/bin/python3 bench/resident_dispatch.py --gen 64 --resident-executor ./build/qwen_graph --user-network-executor ./build/qwen_graph_user_network --model Qwen/Qwen2.5-0.5B-Instruct --output bench/results/coalesced_network_qwen_retry1_20261011.jsonl
```

Archive exact native stdout/exit, source snapshot and host observations.
Do not restart on observation timeout; inspect the same live process.

Completion requires all80 cells/5120 requests/166400 exact measured tokens,
20 normal exits, native publication/completion/graph counters and cleanup.
Preserve negative, failed and inconclusive rows. A failed correctness/fairness
condition invalidates the affected comparison; do not count it as a win.
Fresh result reviewer independently audits complete raw evidence and estimates.
Update docs/evaluation.md and the existing finding sequence with honest
qualified implementation/diagnostic/matched-result boundaries.


## Recorded failed attempt and source repair (2026-10-11 UTC)

The original frozen 00d8ae3 full command exited1 at 08:34:27 UTC during
Smol pair2/resident/gen64/client8. Its
[raw output](coalesced_network_smol_20261011.jsonl) and
[native stdout](coalesced_network_20261011.stdout.txt) remain preserved.
There are17 complete cells,1144 exact measured replies,four completed executor
records and one failure. Qwen did not start. This prefix cannot support the
declared five-pair performance estimate.

The failure records one busy refusal at observed head72, stateBF_WRITING,
head_changed0. The former producer first reserved slot state and then advanced
head; its bounded loop could exhaust on that transient reservation. The repair
uses the existing adjacent head/pad bytes as one aligned64-bit admission word:
low32 head and high32 physical-slot reservation bitmap. A successful CAS
advances head and reserves its slot together. The bit protects the slot even
before that producer sets WRITING/PENDING. TX clears it atomically only after
finishing old slot accesses and publishing FREE. Concurrent clears preserve
head and other reservations. Capacity and retry count remain BF_LLM_SLOTS;
this does not promise lossless overload admission or unlimited contention.

The canonical layout size/offsets are unchanged. UDP and stream producers share
the reservation operation; kernel TX, native user control and the historical
CPU bridge release the bitmap. The bridge uses the existing host libatomic
through ctypes because a Python mmap read/modify/write could lose concurrent
head advances. No extra map, service or control interface is added.

The native user reactor records its physical-slot ownership in the same word.
Its single producer retains its existing publication sequence. All model
capture, GPU dispatcher, numerical oracle, client timeout, service lifetime,
matrix, repetition order and primary-effect definitions are unchanged.
Native cuobjdump verifies1536 identical dispatcher instruction/encoding rows
across frozen00d8ae3 kernel and repaired kernel/user binaries.

Qualification is rerun using the same four strict two-model/two-transport
commands and fresh native real preflights; source must be committed/pushed
before full retry. The current full commands above use fresh retry1 paths.
The entire80-cell matrix is rerun from the beginning; no successful prefix
is stitched across source versions. Previous preflights/diagnostics qualify
their historical source only. The
[repair qualification receipt](coalescing_admission_repair_20261011.stdout.txt)
retains exact source, commands and terminal outputs.

Follow-up1 identified a historical bridge consumer that skipped requests in
the head-before-PENDING window. It now waits without advancing seen until the
reserved request is published; graph consumers already wait. Compatibility is
qualified separately with real Qwen TCP requests and a delayed-publication
case, rather than inferred from graph tests. Kernel reservation release now
uses atomic64_fetch_andnot_release: the previous actual x86 locked operation
was ordered, but the explicit API expresses the portable ownership contract.
Both affected kernel regressions are rerun after rebuilding that module; the
two user regressions retain unchanged source/binaries. Fresh preflight paths
above retain the historical files and satisfy native exclusive output creation.

Qualification completed on the repaired source: both native user regressions
remain terminal0; both kernel regressions reran terminal0 after explicit
release. The original bridge test delivered48 exact replies but exited1 in
cleanup because rmmod is absent. Only that test cleanup was changed to native
x86 delete_module, matching the graph executor; oracle/input/timeout unchanged.
The rerun exits0 for both24-reply modes, and the actual-main publication-gap
diagnostic exits0 with8 exact Qwen tokens and native reservation preservation.
Original failed output remains in the same receipt. Final module/hook/pin
cleanup was separately verified before preflight.

Both fresh repaired-source preflights exited0, Smol09:06:00UTC and
Qwen09:08:10UTC. Native analysis and separate counter/cleanup inspection
verify16 exact measured one-token replies/four normal executors,264 graphs
and launch1/error0 each, kernel busy0/reserved0/eightFREE. They establish
executability only; the published source will be frozen for the full retry.

## Terminal full run and result review (2026-10-11 UTC)

Frozen source cc07226eb9680c90134279bce0d58fc0b730280e completed the entire
retry1 matrix with both native commands above. Smol exited0 at09:28:06 UTC;
Qwen exited0 at09:42:08 UTC. All80 cells/5120 measured requests/166400 exact
tokens/20 normal executors are retained. The [analysis receipt](coalesced_network_analysis_20261011.stdout.txt)
contains native analysis and a separate complete reconstruction. The
[result review](coalesced_network_result_review_20261011.md) confirms completion
and records its follow-up correction for a global OOM during Qwen user pair3
throughput. All four primary intervals cross zero. No sample is removed, no
failed prefix is stitched, and no selective retry is run. The comparison closes
as supporting and inconclusive; the unequal OOM exposure also prevents Qwen
transport-only throughput attribution. Full-goal work continues separately.
