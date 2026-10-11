# Socket-readiness comparison: independent result review

Reviewer: retained /root/device_graph_trace_result_review, fresh to this
candidate, plan and execution. A new agent could not be created because the
thread limit was reached; this completed reviewer from an unrelated experiment
was reused. The reviewer read the plan, reviewed plan, frozen/current source,
strict/preflight/full raw, native analyses and environment receipts. It did not
modify source or run models, GPU workloads, builds or services.

## Verdict

Run: valid / complete. Tested hypothesis: inconclusive. Research value:
supporting. Paper impact: the current mechanism/workload boundary, with no
formal RQ, external SOTA superiority or complete-goal acceptance. No
invalidating defect was found.

All 120 cells,7680 measured requests,249600 exact tokens and30 executors
complete. Each model has3946 records,60 cells,3840 requests,124800 tokens
and15 normal executors,without failure rows. Five process blocks follow
the planned three-mode orders and four-cell rotation. Each cell includes
four prompts16 times; indices,tokens and timing records agree. All native
analysis means,quantiles,component arrays and24 paired intervals/model
match independent reconstruction.

## Primary and accompanying planned comparisons

CPU and TTFT differences are timed control minus kernel; TPS differences
are kernel minus timed control. Nominal two-sided paired t95 uses five
process blocks,df4,without a familywise adjustment or equivalence margin.

| Model / metric | Kernel | Timed control | Difference | Nominal t95 |
|---|---:|---:|---:|---|
| Smol gen64/c8 bounded CPU,us/request | 745.145853 | 927.288075 | 182.142222 | [-60.833662,425.118106] |
| Qwen gen64/c8 bounded CPU,us/request | 1000.443231 | 1255.726428 | 255.283197 | [-44.867063,555.433457] |
| Smol gen1/c1 TTFT,ms | 2.917334 | 2.726689 | -0.190644 | [-0.562401,0.181112] |
| Qwen gen1/c1 TTFT,ms | 2.242427 | 2.257563 | 0.015137 | [-0.202058,0.232332] |
| Smol gen64/c8 output tokens/s | 1850.077800 | 1850.960533 | -0.882733 | [-4.541080,2.775614] |
| Qwen gen64/c8 output tokens/s | 1417.012211 | 1414.195521 | 2.816690 | [-7.988008,13.621387] |

Both primary CPU intervals cross zero. Smol CPU pairs are
470.433547,270.647031,140.139203,61.751562,-32.260234us/request;
Qwen pairs are176.598891,525.011016,456.430187,-77.609063,195.984953.
Positive means do not establish reliable advantage; crossing zero does
not establish equivalence or regression. Planned TTFT/TPS also remain
inconclusive.

Busy epoll is a CPU/latency tradeoff control. Its gen64/c8 CPU minus
kernel has nominal support: Smol34157.920969
[33304.525555,35011.316383]us/request; Qwen44318.680884
[44076.929141,44560.432628]. This cannot replace the efficient-control
primary judgment. Planned TTFT1/c1 and TPS64/c8 versus busy also cross zero.

## Accounting and timing

All150 idle/cell CPU before/after counters,deltas,sums and process-wise
monotonicity pass reconstruction. Both user controls have zero TX counter.
Resident primary CPU decomposes into executor23.019503 + TX722.126350
us/request for Smol and executor31.456825 + TX968.986406 for Qwen.
The POSIX process clock covers all executor threads. TX is adjusted
task user+system CPU. This is not total service CPU: RX/softirq/BPF and
other TCP work charged elsewhere,client,benchmark,GPU and other host
work are excluded. Whole-host /proc/stat cannot identify service cost.

Sequential sample brackets are not atomic common windows. Smol bracket
min/median/max43.657/90.0375/266.560us; Qwen42.482/94.427/260.538us.
Cell brackets cover actual requests. CPU includes the wider barrier/future
window; TPS uses first-send to last-token-arrival. Common receive completion
can give tokens the same timestamp. TPOT measures client arrival spacing,
not independent GPU token execution time. Connection construction precedes
the window; teardown/reclaim equivalence is not guaranteed.

## Source and mechanism

Frozen source is b129c331cfa8fb0582c791315ed3748bd867a353. Six relevant
current files match it. Relative to d16fac01,the only behavior change is
module8 inserted/1 deleted lines: linux/poll.h and two readiness guards.
Model math,dispatcher,native controls,benchmark and oracle remain unchanged.
Three modes reuse the same capture source and differ in request/control mode.

Exact Linux v7.3-rc3 source supports this use: listener poll checks the
accept queue; TCP poll includes EOF/error and sk_is_readable; BPF protocol
sets that callback to sk_msg_is_readable ingress-message readiness. A NULL
poll table registers no waiters. Guarding accept/recv preserves release,
peer ownership and TX lifecycle. No dynamic skip counter or same-window
old/new comparison exists,so no causal historical CPU reduction follows.
Finding0027 remains separately closed.

Sources:
[TCP poll](https://github.com/torvalds/linux/blob/v7.3-rc3/net/ipv4/tcp.c),
[BPF readable callback](https://github.com/torvalds/linux/blob/v7.3-rc3/net/ipv4/tcp_bpf.c),
[ingress readability](https://github.com/torvalds/linux/blob/v7.3-rc3/net/core/skmsg.c),
[poll_wait](https://github.com/torvalds/linux/blob/v7.3-rc3/include/linux/poll.h).

## Correctness, engagement and lifecycle

Both affected-kernel strict runs complete335 valid/20432 exacttokens/
259 rejects,exit0. They cover fragmentation,empty connections,reuse/wrap,
mixed lengths,pipeline,half-close,invalid IDs and after-ready all-thread
network trace. The visible78 expected/actual pairs,4992 tokens,all match.
Other strict requests rely on the checked native per-request assertions and
normal exit,not archived printing of every token. Independent eager-HF
references are generated before service launch; requests do not provide
expected output to the GPU,avoiding a circular correctness oracle.

Reused unchanged userspace strict qualification from finding0027 also
passes335/20432/259 for both models. Current preflight/full confirm all
three modes' engagement and exact outputs.

All30 full executors report1 host launch,8580 graphsteps,graph_error0,
banks8,max_active8. Both user controls accepted19/published264/completed264/
rejected0. Resident ends with8 FREE,zero reservations/queueerrors.
Ten kernel lifecycles each report55176bytes,264 completions,zero
abandoned/retries,19 accepted/closed. Bytes independently reconstruct from
132gen1 +132gen64 requests,including8 warmups,and real HTTP headers.
Strict593completed/1abandoned corresponds to intentional binary rejection
disconnect,not a failed performance sample.

Bootstrap mean seconds,kernel/busy/timed:
Smol61.109553/61.182273/61.230615;
Qwen56.762053/59.202633/56.065060.
Across all20 active cells/mode,CPU seconds:
Smol kernel process0.035237 + TX0.772204,busy50.931886,timed1.147362;
Qwen kernel process0.037152 + TX0.820107,busy52.317823,timed1.295239.
Idle resident has measurable process+TX cost; it is not zero CPU.
Coarse100Hz executor ticks and nanosecond process+TX have different scopes.

## Environment and next decision

Original Pod/boot and source remain stable. Full retained journal has no
matching OOM/Xid/Oops/BUG/CallTrace/I/O/EXT4 fault lines. Before/after GPU
compute-app lists are empty; two during receipts map listed GPU PIDs to
own runner/executor by cmdline/cgroup. These discrete observations do not
establish continuous isolation or equal host load. One SSH read timeout
does not interrupt the runner; both real commands exit0 without restart.
Own runner/executor,module and pins are absent after normal completion.

Close and publish this matrix. Efficient-control CPU advantage is not
established. Avoid rerunning an unchanged matrix to seek significance.
Results support worker-free kernel-path correctness and bounded component
measurement,not total CPU,SOTA,physical NIC or full-text serving superiority.
Retaining readiness guards is an engineering judgment,not a performance
benefit promise or a reason to undo the already published source.

Finding0028/README/evaluation/architecture still describe collection/review
as pending; update them and link full raw/nativeanalysis/this review. That
documentation lag does not invalidate the completed experiment.
