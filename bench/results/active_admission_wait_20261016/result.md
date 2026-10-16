# Active admission wait: complete ordinary-build result

The fixed primary hypothesis is supported for owned process-group CPU.
All fifteen admitted remote cells completed. Candidate group CPU fell by
63.22% versus before and 18.66% versus native (ratios of condition means).
This is a CPU-efficiency result, not a transport speedup: candidate-before
throughput and completion/token-gap P99 intervals include zero. Candidate
still has lower throughput and higher completion P99 than native epoll.

Production source adoption and independent result review are pending at this
publication. The separately planned candidate creator-TID perf check is also
pending; it cannot replace these fifteen unprofiled performance cells.

## Mechanism and controlled change

The sole candidate production edit is in bpf/uring_loop.bpf.c:
the admitted != admission_seen immediate-return exception applies only when
may_idle is true. During active execution an unconsumed admission previously
forced repeated immediate loop callbacks despite the existing 60 microsecond
timer. The candidate allows the next CQ/timer wait while retaining immediate
admission handling during idle transitions. No model operation, GPU library
SASS, native transport, default slot count, ABI, socket option, timer value or
host setting changed. See plan.md, plan-review.md and qualification.md for
source/build comparisons and lost-wakeup reasoning.

Before and native use the unchanged normal reclamation_sourcebuild16;
candidate uses normal active_wait_sourcebuild16. Both default-eight and
sixteen builds are retained in build_records. The root source contains exactly
the candidate condition as uncommitted WIP during measurement; source_commit
in run receipts is the artifact HEAD, not a claim that this source was already
adopted. Actual BPF source snapshots and compiled-object bindings distinguish
conditions. GPU SASS and the other BPF program match.

## Execution and outcomes

Qwen2.5-0.5B-Instruct FP16, the same RTX5090 and existing resident executor,
fixed four-prompt pool, 64 output tokens, 192 offered requests/s, 60 seconds of
gamma arrivals per cell with full terminal drain. Five paired process blocks,
rotating the three conditions exactly as planned. The same block arrival
offsets are reused across conditions. Eight checked one-token warmups per
process are excluded. Existing 60-second per-I/O timeout and both correctness
oracles are unchanged. There is no profiler in any performance cell.

Each condition has 57,600 attempts, 57,600 completed responses and 3,686,400
measured tokens; the matrix totals 172,800 attempts and 11,059,200 tokens.
Failures, protocol-invalid outcomes and close errors are zero. All fifteen
servers exit zero and leave no BPF pins. Finite reference-pool disagreement
counts are before296, candidate223 and native233 (752 total); these retained
flags preclude an exact full-run model-fidelity claim. Default-eight traced
dual-replay correctness is a separate finite qualification, not an oracle
expansion during this run.

| Metric (mean of five cell statistics) | Before kernel | Active-wait candidate | Native epoll |
|---|---:|---:|---:|
| owned_group_cpu_ms_per_attempt | 1.701533854 | 0.625738952 | 0.769310595 |
| output_tokens_per_s | 11625.993482927 | 11626.456624989 | 11646.715244977 |
| connect_completion_ms_p99 | 3395.012682004 | 3394.068796006 | 3295.820195146 |
| connect_ttft_ms_p99 | 3309.362226162 | 3308.568885374 | 3211.721534570 |
| client_token_gap_ms_p99 | 4.370018774 | 3.993355600 | 4.288793310 |
| server_host_active_cpu_s_per_attempt | 0.071281771 | 0.064653472 | 0.066283333 |
| device_energy_J_per_attempt | 1.698977500 | 1.696229670 | 1.697219688 |

| Contrast | Metric | Signed mean | Nominal paired 95% t interval |
|---|---|---:|---|
| candidate minus before | connect_completion_ms_p99 | -0.943885998 | [-44.277690293371045, 42.38991829737078] |
| candidate minus before | server_host_active_cpu_s_per_attempt | -0.006628299 | [-0.01673658933709858, 0.0034799921148763596] |
| candidate minus before | owned_group_cpu_ms_per_attempt | -1.075794902 | [-1.2227967814299296, -0.9287930226325705] |
| candidate minus before | device_energy_J_per_attempt | -0.002747830 | [-0.007482107450932938, 0.0019864477287105916] |
| candidate minus before | output_tokens_per_s | 0.463142062 | [-8.973088628683275, 9.899372752278818] |
| candidate minus before | client_token_gap_ms_p99 | -0.376663174 | [-1.2167136391805682, 0.46338729118055677] |
| candidate minus before | connect_ttft_ms_p99 | -0.793340788 | [-43.94748092247099, 42.36079934647094] |
| candidate minus native | connect_completion_ms_p99 | 98.248600860 | [48.69998349469164, 147.79721822530814] |
| candidate minus native | server_host_active_cpu_s_per_attempt | -0.001629861 | [-0.017459817300904974, 0.014200095078682756] |
| candidate minus native | owned_group_cpu_ms_per_attempt | -0.143571643 | [-0.1820942554818668, -0.10504903021257772] |
| candidate minus native | device_energy_J_per_attempt | -0.000990017 | [-0.012785659982924002, 0.010805625260701746] |
| candidate minus native | output_tokens_per_s | -20.258619989 | [-30.272903312565937, -10.244336665012055] |
| candidate minus native | client_token_gap_ms_p99 | -0.295437710 | [-0.6693116589442293, 0.07843623894421337] |
| candidate minus native | connect_ttft_ms_p99 | 96.847350804 | [47.583732969292996, 146.11096863870677] |

The intervals use five paired block effects, t(df=4), without multiplicity
correction. One group-CPU primary was fixed before execution. All 46 promised
paired contrasts, all per-cell distributions and failed/adverse/inconclusive
rows are in active_wait_full/analysis.stdout. An interval crossing zero is
inconclusive, not equivalence or noninferiority. Zero observed failures is not
a rare-failure bound.

The offered output demand is 12,288 tokens/s, above delivered throughput in
all conditions. Thus accumulated queueing is a plausible explanation for the
roughly 3.3-second request completion P99 and its sensitivity to a small
throughput difference; this is an inference from load and delivery, not an
additive queue-stage attribution. Receive-gap P99 is measured at the client
and includes receive coalescing/scheduling; it is not a GPU-generation timestamp.

## Resources and validity limits

Group CPU is the owned service process-group CPU clock divided by all
attempts. io-wq threads in its TGID are already included, never added again.
Thread scheduler runtime, cgroup, host irq/softirq, observer and device energy
remain separate nested/context views in resource JSONL and details.stdout.
The shared host and device are not exclusive: host/device/cgroup totals
include other work, so these data do not establish whole-machine or energy
savings. The observer is separately accounted. Each process also has its
separate loaded-idle resource bracket. Remote client work and scheduling lag
remain in raw records. No foreign process was stopped.

The original 14.72 vs8.36ms token-gap P99 (+6.36ms) was not reproduced under
the later matched controls even before this edit. Prior tracing did not permit
an additive allocation of that historical P99 to softirq/io-wq/GPU polling/TX.
This intervention tests the coordination-CPU mechanism identified by the
creator-TID profile; it does not retroactively explain or fix exactly6.36ms.
The shared TCP_NODELAY fix, per-peer EOF reclamation fix, official vLLM
reference and generic backend qualification remain distinct findings.

## Reproduction and publication

See reproduce.md and run_active_wait_matrix.ps1. Original clients, terminal
receipts, server source/argv, observers and full analysis are under
active_wait_full. archive_replay.stdout is byte-identical to analysis.stdout;
both analyzer stderr files are empty. The plot uses all fifteen cells,
shows individual paired observations and condition means, and is visually
checked. No partial prefix is promoted.

The preflight publication finished before the first full observer began.
Client compression/transfer occurs only after each server stops, before the
next cell. Larger archive/replay/plot work occurs after the entire matrix.
The temporary client Job remains solely for the planned post-matrix perf
check and is removed on closure. Original Workspace sessions1/10909 and
foreign tools/setup_env.sh are preserved; postmatrix_runtime.json records no
GPU compute applications or pins after the matrix.
