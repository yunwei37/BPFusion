# Kernel-owned network placement: ordinary matched serving intervention

2026-10-16 UTC. Current selected main entry1a2e2be; source candidates remain
private/unselected. Uses research-experiment-design full loop.
There is no formal paper RQ/thesis/idea-story file. The retained user objective,
verbatim from evaluation.md, is: "a complete Linux TCP/HTTP + eBPF/shared queue
to resident real-model inference and asynchronous kernel TX, with reproducible
matched correctness and throughput/latency evidence." This plan tests one
network-placement hypothesis within it, not a model-kernel optimization.

## Admission and decision value

0076 completes the current timing discriminator: a small instrumented dispatch
association, material measurement perturbation and concurrent GPU network
connection/reply residence. Ordinary selected loop remains24.638tokens/s slower
and completionP99+130.692ms versus efficient native, despite lower owned CPU.
Old6.36ms does not reproduce and is not a valid additive allocation target.
0075 peer cache is closed/rejected. Another unchanged run, sleep/cache sweep
or more duration instrumentation cannot answer avoidability.

Hypothesis: moving CQ/SQ and connection/reply progression from independent GPU
io_network to the existing BPF loop improves ordinary client-delivered throughput
with reused GPU model/controller unchanged. This bundled placement intervention
includes CPU-owned registered state/token copies and removes the GPU I/O CTA;
it does not isolate a single PCIe fence, softirq or sleep instruction.
The largest credible story is an application-level eBPF service mechanism with
reuse of upstream computation and a causally matched network-placement benefit,
not a generic GPU-networking novelty claim. Upstream io_uring BPF is prior work;
docs/background-related-work.md/source audit remain the closest-work map.

Planned role: supporting intervention toward the serving RQ. Positive result
with finite correctness could justify this source route; negative/inconclusive
result rejects its performance case and keeps0074, without larger N or renamed
primary. An application/lifetime failure requires an actual repair, not dropping
that case or weakening its oracle. Native winning bounds the implementation;
it does not falsify every possible eBPF driver. This adds the missing ordinary
network-placement ablation; no prior dataset contains this constructor.
It outranks smaller mapped-peer/timer changes by directly testing removal of
the concurrent GPU I/O control work without rewriting any model kernel.

## Comparison and fixed primary

Main competitor N: efficient C++ epoll/timed completion wait using the exact
same resident upstream-vLLM GPU generation/checkpoint/FP16. It represents the
credible userspace mechanism and must engage successfully. Component ablation
L: selected0074 GPU-I/O/BPF-loop network with the same model algorithm.
Candidate K: kernel-owned BPF CQ/SQ/connection/reply path and unchanged GPU
dispatch source. GPU emitted dispatch instructions must be compared, not
assumed from source. N plus L are needed to distinguish improvement over the
current implementation from beating the competing mechanism; no extra weak
baseline. Official vLLM0069 remains a separately dated whole-service reference;
its HTTP/token/KV/scheduler differences cannot isolate this intervention.
No new official-vLLM run is needed for this mechanism decision.

Primary K-minus-L delivered output tokens/s, five paired process blocks,
nominal paired95%t(df4;2.776445105). Standard throughput/TTFT/TPOT/ITL metrics
reuse the official-vLLM definitions:
https://docs.vllm.ai/en/stable/benchmarking/cli/#understanding-the-latency-metrics
Primary interval above0 supports local improvement; below0 contradicts it;
zero-crossing is inconclusive, not equivalence. Report K-minus-N and L-minus-N
alongside all completion/TTFT/TPOT/receive-gapP95/P99, mean/scheduling lag,
all-attempt failures and full retained resource views. Correctness or comparison
unfairness can invalidate the performance case. CPU/energy tradeoffs remain
explicit and cannot be promoted to exclusive totals; no speed/CPU conjunction
or post-result alternate-primary selection.

## Constructor and boundaries

Reuse current framing/admission, canonical bf_page ABI, FIFO reserve/publish/
completion tags, corrected pending-peer EOF/non-EOF guards, model-page output
publication and upstream model/math. The only mixed .cu change is the host
transport include; kernel_tcp.h owns bootstrap/ring/map attachment/stop/drain.
BPF owns connection/reply progression using registered CPU memory and normal
kernel TCP/io_uring. No steady userspace request worker or GPU I/O kernel.
The same60us active multishot timeout and idle deadline policy are retained.
The host report uses the existing RESULT prefix, not a new parser/oracle.
No new persistent entity, service, worker or host setting. Kernel CPU work
remains real and may increase. Kernel API/version and current source are
archived, not claimed portable or universally novel.

Ordinary Make default8/explicit16, actual object/library binding and verifier-only
loads are setup dependencies. Current source draft now passed matching8/16
verifier-only loads but has never attached/served. Keep all real failures and
source revisions. Before serving, rebuild final host interface, compare compiled
dispatch/BPF controls and snapshot source. Do not change measured source,
client, oracle, timer, analysis or timeout during the full matrix.

## Executable qualification and real preflight

Reuse existing active_wait_protocol_load.py, ordinary lifecycle, source-native
mixed_replay.py and their fixed request/oracle logic. Necessary adapters only:
candidate build path, source receipt, artifact prefix and matching RESULT log
interface. Do not weaken old assertions. Candidate default8 Qwen and Smol
protocol checks cover TCP/HTTP fragmentation, invalid inputs, concurrency,
reuse/half-close/reset and partial output; trace replay checks actual captured
trajectory plus fresh upstream attention metadata. Existing ordinary lifecycle
checks cover idle/reuse/reject/backlog and mid-generation stop/drain without
timing macros. Current native/old-loop source qualification is unchanged and
already complete; do not repeat identical broad checks just for activity.

Real performance-path preflight: K/L/N, first128 block0 remote offsets at192/s,
64 outputs each, eight excluded checked gen1 warmups/process. Existing frozen
pool membership stays a reported flag, not a changed oracle. Additional candidate
trace replay qualification supplies finite exact correctness; ordinary full
runs remain untraced to avoid0076's perturbation. No exact full-run untraced or
eager-HF/general-model fidelity claim. At most3 real preflight attempts per skill.
Verifier/compilation alone do not count as an executed model preflight.

## Full integrated run and terminal rule

One Qwen checkpoint/frozen revision and FP16, RTX5090, slots16, existing four
frozen prompts and gamma arrival offsets/seeds20261015+block. Five blocks,
conditions K/L/N with orders K,L,N; L,N,K; N,K,L; K,N,L; L,K,N.
Each11520 scheduled requests at192/s for60s plus full drain;15 cells,
172800attempts/11059200 measured output tokens if all succeed. Eight checked
gen1 warmups each process are excluded from client metrics; internal scopes
include warmup/start/idle/stop. Per-I/O60s timeout unchanged, retain all
failures/partial tokens/client scheduling delays and no faster-prefix censoring.
No profiler, GPU trace, other GPU service, build or heavy archival during
measured cells. After serving stops, transfer/compress originals and analyze.

Reuse remote_async_client.py/config/offsets and existing resource_observer.py,
5s loaded-idle context and ordinary analysis/plot routines with condition names
adapted before preflight. A bounded disposable client Job uses its already
declared owner path, unpinned to a specific host; excludes current GPUserver node
through actual Workspace placement. No service needs pausing. Own UID/cleanup/
original PIDs/source/WIP preserved, no exclusive-host claim with foreign lab work.

Commands: TEMP/runtime/bin/python TEMP/kernel_network_acceptance.py;
Windows run_kernel_network_matrix.ps1 -ClientPod <actual owned Pod>
-ServerIP <actual Workspace-IP> -Preflight, then without -Preflight.
The prepared scripts reside in this archive and existing TEMP root.
All paths/commands/source/version receipts and fixed scripts are archived before
execution. Full completion requires15 client/server terminals, all fixed
analysis/checks, archive CPU replay, fresh independent result review and actual
owned-client cleanup. Failed/invalid outcomes are retained; no unchanged rerun/
larger sample/timer sweep. Commit/push each completed milestone on main.
Target figure is paired K/L/N TPS and completion/receive-gap tails/CPU, with
all cell values and uncertainty, not another duration-stack latency allocation.

## Selection and remaining scope

No source adoption from successful verifier or smoke. A valid primary effect
addresses ordinary placement benefit only; source adoption additionally needs
the unchanged finite protocol/lifetime/cancel qualification and honest tail/
CPU tradeoff disclosure. If inconclusive/adverse, keep0074 and close the tested
constructor without weakening the hypothesis. General backend/plugin support,
long-duration reset pressure, total service CPU and historical6.36ms allocation
remain distinct open limits. One Qwen workload cannot prove all-model benefit.
