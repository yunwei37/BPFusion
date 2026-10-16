# Immutable peer identity: complete fifteen-cell result

The fixed throughput primary is inconclusive. Candidate-minus-before delivered
TPS is+1.390100488, nominal paired95%t(df4) interval[-2.910413831,5.690614807].
There is no established delivery benefit from this immutable-tuple cache.
Candidate-minus-native is-19.271234036[-22.505644825,-16.036823248]tokens/s,
and completionP99 is+104.870609988[74.187468727,135.553751249]ms, both adverse.

The predeclared source decision for an inconclusive primary is to keep the
already-selected0074 header and archive the candidate. Independent result
review and the physical source restoration are pending at this publication;
nothing is promoted from this result. No unchanged rerun, larger N, new flag
or favorable secondary metric replaces the fixed primary.

## Scope and controlled source

Retained same-compute serving throughput/latency question, supporting controller
placement intervention, not model arithmetic or a new formal RQ. See plan.md,
plan-review.md and qualification.md. Only executor/io_uring_tcp.h changes:
copy immutable sockaddr address/port after successful ACCEPT CQ acquisition
into existing device-local IoConn, then use them for existing peer scan and
EOF pending-bucket lookup. Five lines added/five removed, no new allocation,
table, worker, flag, ABI, timer or persistent configuration. Existing IoConn
allocation grows naturally by8bytes per entry. Controller layout/codegen are
part of the intervention; no exclusive physical PCIe mediation is claimed.

Before is the immutable normal active_wait_sourcebuild16, the adopted0074
header, and a component ablation. Native is efficient C++ epoll from that same
build, the main competitor. Candidate is normal peer_identity_sourcebuild16.
Both8/16 builds pass; actual commands retain nvcc -dc and absolute BPF binding.
Both BPF programs' instructions/relocations and native GPU SASS match at8/16.
Candidate controller SASS is expected to differ. All model implementation/
graph capture source, weights/precision, shared ABI, BPF policy, socket option,
native implementation, timer and host settings are unchanged. Actual receipts
use the correct before/candidate header snapshots rather than treating artifact
HEAD as proof of source adoption. Canonical header remains candidate WIP during
the entire frozen matrix; no post-qualification source edit occurred.

## Complete actual remote workload

Qwen2.5-0.5B-Instruct FP16, existing pinned runtime/RTX5090, mixed16 slots,
four fixed short prompts,64 output tokens. Five process blocks each have
before/candidate/native192requests/s for60s, same block gamma offsets and
full terminal drain, with eight checked excluded gen1 warmups per process.
All15 admitted cells are terminal, no replacement or exclusion. Each has
11520 attempts; each condition57600 successes/57600 attempts and3686400
measured tokens. Total172800 successes/11059200 tokens plus120 warmup tokens.
Transport/protocol/close errors and timeouts are zero in the measured matrix;
zero observations do not establish a rare-failure bound.

Finite frozen-reference-pool disagreements are before235,candidate180,native228,
643 total. They remain successful protocol responses and retained flags,
not exact full-run model-fidelity evidence. No pool was expanded, oracle
weakened or timeout changed. Separate default8 trace/dual replay validates
finite correct trajectories, not every untraced full-run output.

| Mean of five cell statistics | Before kernel | Peer identity cache | Native epoll |
|---|---:|---:|---:|
| owned_group_cpu_ms_per_attempt | 0.627792198 | 0.642500531 | 0.779963771 |
| output_tokens_per_s | 11623.356568746 | 11624.746669234 | 11644.017903270 |
| connect_completion_ms_p99 | 3413.675785722 | 3407.237073804 | 3302.366463816 |
| connect_ttft_ms_p99 | 3329.269166984 | 3322.921985522 | 3217.554613432 |
| client_token_gap_ms_p99 | 4.551022722 | 4.724972340 | 4.605980698 |
| server_host_active_cpu_s_per_attempt | 0.068858507 | 0.069992882 | 0.067800521 |
| device_energy_J_per_attempt | 1.697538281 | 1.698141892 | 1.693318681 |

| Contrast | Metric | Signed mean | Nominal paired95%t interval |
|---|---|---:|---|
| candidate minus before | connect_completion_ms_p99 | -6.438711918 | [-33.15079794103217, 20.27337410503237] |
| candidate minus before | server_host_active_cpu_s_per_attempt | 0.001134375 | [-0.010796244706858108, 0.013064994706858119] |
| candidate minus before | owned_group_cpu_ms_per_attempt | 0.014708333 | [-0.008151109567430287, 0.03756777640770806] |
| candidate minus before | device_energy_J_per_attempt | 0.000603611 | [-0.008848842132668249, 0.010056064354890518] |
| candidate minus before | output_tokens_per_s | 1.390100488 | [-2.9104138308779977, 5.690614807095745] |
| candidate minus before | client_token_gap_ms_p99 | 0.173949618 | [-0.7495913313569557, 1.0974905673569602] |
| candidate minus before | connect_ttft_ms_p99 | -6.347181462 | [-32.16808290182054, 19.473719977820302] |
| candidate minus native | connect_completion_ms_p99 | 104.870609988 | [74.18746872748505, 135.55375124851471] |
| candidate minus native | server_host_active_cpu_s_per_attempt | 0.002192361 | [-0.00862938845007176, 0.01301411067229399] |
| candidate minus native | owned_group_cpu_ms_per_attempt | -0.137463240 | [-0.1606762772272471, -0.1142502031546974] |
| candidate minus native | device_energy_J_per_attempt | 0.004823212 | [-0.004048204856793176, 0.013694628467904297] |
| candidate minus native | output_tokens_per_s | -19.271234036 | [-22.505644824799198, -16.036823247922918] |
| candidate minus native | client_token_gap_ms_p99 | 0.118991642 | [-0.5801214903189198, 0.8181047743189236] |
| candidate minus native | connect_ttft_ms_p99 | 105.367372090 | [74.34199558573209, 136.39274859426777] |

All46 predeclared paired contrasts (one throughput primary) and every cell's
mean/P50/P95/P99 TTFT, completion, TPOT and client scheduling lag remain in
peer_identity_full/analysis.stdout. Intervals are nominal, no multiplicity
correction; five fixed rotating process orders and shared-host variation
limit generalization. Crossing zero proves neither equality nor noninferiority.
Candidate-before completionP99, receive-gapP99, CPU and shared resource
contrasts are also inconclusive. Lower candidate group CPU versus native is
already present in the before path after0074; it is not this cache's gain.

Offered output demand12288tokens/s exceeds delivery in every condition.
Accumulated queueing is compatible with the seconds-long completion tails
and their sensitivity to small capacity differences. This is an inference,
not measured stage attribution. Client receive gaps include coalescing and
scheduling and are not GPU-generation timestamps. No additive explanation or
claimed repair of historical14.72 vs8.36ms (+6.36ms) follows.

## Correctness, resources and deviations

Normal default8 qualification completes1280 two-model protocol outcomes,
518 intended rejects and46752 exact dual-replayed tokens. Both ordinary loop
lifecycles pass144 outcomes each, preserving partial/unobserved cancellations,
idle transitions/reuse/half-close/reset/backlog stop. Four ordinary cuBLAS8x8/
cuFFT32 native/loop graph cases each pass182 analytic/lifecycle checks.
HF shared controller compiles only; optional AMK vm dependency is unavailable,
so no new AMK runtime or arbitrary-model/backend qualification is claimed.

Preflight attempt1 omitted an existing128-prefix offset file, and client
failed before scheduling any measured request. Its8 checked warmups,
client failure traceback, observer/server source/terminal are retained in
peer_identity_preflight. Attempt2 copied the unchanged file, verified it is
the exact first128 offsets, and completed384 successes/24576 measured tokens,
24 excluded warmups and2 retained finite-pool flags. See preflight-deviation.md.
Full stage and source/oracle/timeout/metric definitions never changed.
The setup-only Windows-path submission error preceded one successful Job
creation; it is recorded, not hidden or counted as a measured result.

Owned group CPU uses process CPU clocks/all attempts. io-wq time in the
service TGID is included once; thread scheduler runtime is a nested view,
never added again. Kernel threads, irq/softirq, cgroup, observer and device
records stay separate. Host/device/Workspace include retained other work,
so these data do not establish exclusive service CPU, whole-machine savings
or energy benefit. Loaded-idle brackets are separate. No profiler overlaps
preflight or full performance cells; no foreign work was stopped.

Client compression/transfer and per-cell archive occur after that server
stops, before the next cell. Heavy aggregate analysis/plot/Git waits until all
fifteen finish. Preflight publication completed before first full observer.
CPU-only archive replay exits0, byte-identical stdout and empty stderr;
resource_details.py output preserves nonadditive thread/resource context.
All server terminals exit0 with no pins; postmatrix_runtime.json confirms
no GPU application/pins and preserved original sessions1/10909.

## Figure, reproduction and closure

[Figure](peer_identity_full/peer_identity_comparison.png) and PDF show all
fifteen observations for TPS, completionP99 and group CPU. Lines join paired
blocks, horizontal bars are means, not confidence intervals. Interpret the
reported paired intervals rather than visual mean ranking. Rendered PNG is
visually checked; all labels/units and adverse native rows are retained.

See reproduce.md for actual normal build, qualification and full-run commands.
Raw requests, metadata/source/argv, idle/active observers, terminal receipts,
analysis and replay are under peer_identity_full. At this publication the
independent review, selected-source restoration and bounded client cleanup
remain separate delivery work. Full speed objective is not declared achieved
by protocol success or this inconclusive supporting result.
