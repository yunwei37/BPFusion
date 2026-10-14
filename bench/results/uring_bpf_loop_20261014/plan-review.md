# Fresh plan review — round 1

**Verdict: admit the supporting experiment. No result-invalidating scientific or executability defect found in the proposed plan.** Proceed to implementation and the declared real preflight. This reviews the design and its source-backed feasibility; the candidate has not yet been implemented or demonstrated.

Reviewed `/workspaces/repository/bench/results/uring_bpf_loop_20261014/plan.md`, finding0035, completed findings0042/0043, `docs/evaluation.md`, current GPU network/lifecycle code, benchmark/analysis paths, running-kernel UAPI and upstream loop implementation. Repository HEAD was `11ae59142a732b9ff7e5552863a2bf088085ae46`. No files changed or models launched.

## Admission and scientific scope

The intervention adds independent evidence. Findings0042/0043 establish substantial stock known-worker CPU cost but cannot reconstruct the absent sleeping-loop condition. Reanalyzing their raw outputs cannot answer whether this replacement lowers CPU or changes delivery.

The retained local ordinary-serving question remains intact. A CPU reduction would support this coordination mechanism within the declared accounting scope; CPU failure would contradict its intended benefit. Delivery improvement, loss and inconclusive intervals produce different conclusions. These outcomes do not depend on claiming external SOTA, arbitrary-model support or a formal paper thesis.

The supporting role is appropriate. Compared with another unchanged copy matrix or extra model/scale points, this intervention addresses a measured unresolved cost. Cross-node serving remains valuable but answers a different uncertainty.

## Comparison and inference

Native timed-epoll TCP is a credible main mechanism alternative. Current incremental SQPOLL is correctly labeled a component control. Dropping the module row avoids repeating a condition that cannot identify this intervention.

All three paths share the checkpoint, arithmetic, graph/KV policy, client/wire and workload. The plan correctly treats the change as a complete coordination-path effect: submission behavior, timeout work and scheduling also change. It does not attribute every difference exclusively to polling.

The four-cell workload and two architectures provide enough coverage for the stated local claim. Six paired process blocks, all six transport permutations and common cell rotation are appropriate. The six primaries remain separate, with nominal paired t95 intervals using process blocks rather than pooled requests. Crossing-zero results do not establish equivalence, and a CPU win cannot establish delivery superiority.

The frozen complete-sequence checks and independent traced replay are complementary. The plan explicitly preserves the weaker meaning of ordinary reference-set membership and permits different actual batching/FP16 trajectories.

## Executability and lifecycle

The proposed upstream path is supported at the design level. BPF attachment requires `DEFER_TASKRUN` and rejects SQPOLL/IOPOLL; `SINGLE_ISSUER` and retaining the creator as the steady-loop task match these ownership requirements. [Upstream BPF implementation](https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/bpf-ops.c)

The kernel loop waits on a CQ index, processes deferred work and checks pending signals. GPU SQ publication therefore needs an independent wake source; the planned kernel timeout supplies it without a userspace request proxy. [Upstream loop implementation](https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/loop.c)

The multishot bookkeeping requirement is real: repeated `MORE` CQEs retain one outstanding timeout, whose terminal CQE retires it. Timeout completion itself runs through task work and rearms the timer, making creator ownership material. The nominal 60us setting is not a guarantee of exact wake spacing. [Upstream timeout implementation](https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/timeout.c)

The plan also addresses the existing shutdown hazards:

- Helper-thread SIGTERM publishes a loop-visible stop flag.
- Steady entry returns before model shutdown and quiescence.
- Cleanup continues submitting/draining GPU-published work after cancellation removes the periodic wake source.
- GPU completion is release-published only after final counters.
- Ring, timeout, CQ, buffer and CUDA lifetimes remain live until their owners finish.

These are necessary implementation properties already present in the plan, not additional experiments or approval gates. The unchanged idle/protocol/half-close/helper-thread workloads are suitable ways to expose broken integration.

The existing benchmark and analyzer provide a plausible source-native execution path. Loop mode, syscall expectations and task-identity assertions need the stated adaptation before preflight; their present SQPOLL-specific behavior is not evidence against the proposed design.

## Nonblocking documentation suggestion

Add a defining POSIX/Linux citation for the CPU-clock primary alongside the vLLM delivery-metric citations. Its formula and exclusions are already explicit, so this is citation completeness rather than an invalid measurement design.

**Next step:** implement the planned candidate and source-native benchmark adaptation, then run the declared real preflight. No plan revision or extra baseline is required by this review.

<oai-mem-citation>
<citation_entries>
MEMORY.md:59-60|note=[prior workflow context checked against current completed findings]
</citation_entries>
<rollout_ids>
01a1237b-bc13-7d90-a3d1-22ef8fc29d7e
</rollout_ids>
</oai-mem-citation>