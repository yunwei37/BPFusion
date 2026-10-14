# CQ progress observed before SQ submission

## Question and admission

Retain finding0035's local ordinary-serving question:what client latency/
throughput does the ordinary packed/prefix adapter deliver against the
efficient native network alternative after BF_TRACE is removed? No formal
paper RQ is introduced. Planned role supporting.

Finding0044 closes36 executors/144 cells with roughly96% lower known-worker
CPU than SQPOLL, but no native gen1/c1 latency advantage, lower Qwen gen64/c8
throughput and negative gen1/c8 latency/throughput in both models. Existing
data establishes the boundary but cannot identify its exclusive cause or
supply the absent CQ-snapshot intervention. Do not rerun unchanged conditions
as a new result.

Current BPF code reads CQ tail after bpf_io_uring_submit_sqes and waits for
that value plus1. Upstream io_submit_sqes ends its submission state and flushes
immediate completions before returning; the loop skips sleeping when the
requested CQ index is already reached. Therefore a pre-submit snapshot can
recognize CQ progress produced during this submission. The current snapshot
can require another CQ event instead. This is a source-backed possibility,
not proof of observed unnecessary sleeps or the cause of all delivery loss.

Hypothesis:observing CQ progress before submission improves this loop's client
delivery, with resulting CPU tradeoffs measured, while reusing identical
model and GPU network computation. Largest credible story:an inexpensive
upstream kernel-loop coordination correction recovers a concrete delivery
boundary without a steady userspace request worker, custom TX module or
model-specific arithmetic campaign. No arbitrary-model/total-CPU/SOTA claim.

A positive native contrast supports that scoped delivery metric. Improvement
only over the former loop is a component result, not native superiority.
Negative or inconclusive native effects bound this constructor/workload;
close unchanged timing and keep all negative rows. No equivalence or composite
CPU-and-delivery win is inferred. A contrary result does not directly challenge
a necessary broad thesis:there is no formal paper thesis here.

Best alternative is optimized cross-node deployment, which expands a real
acceptance boundary but cannot test this local source-backed completion
ordering. This tiny causal change is the stronger immediate discriminator
after0044. Additional models or timer sweeps add weaker coverage or confound
the source intervention. No timer-frequency or backend arithmetic search.

## Exact implementation and official precedent

Candidate uses the current loop BPF program with CQ tail captured before SQ
head/tail sampling/submission. Its wait target is that saved value plus1
during service. Existing quiesced cleanup keeps current-tail/no-sleep behavior.
Former-loop control compiles the same BPF source under BF_IO_CQ_AFTER_SUBMIT,
restoring the actual old post-submit snapshot. No new CQ-consumer handshake,
control schema, daemon, proxy or registered-region ABI is introduced.

GPU producer/consumer, SEND/header/partial-byte behavior, model dispatcher,
packed prefill/FIFO-prefix release, KV/head/greedy arithmetic and timer remain
unchanged. Candidate/control ordinary model dispatcher and io_network SASS
must be byte-identical. Baseline has the same model computation, not identical
arrival/batch histories or a GPU network controller.

An optional control object/launcher selects build/uring_loop_after.bpf.o at
bootstrap through the existing loader. Candidate continues the existing
build/uring_loop.bpf.o. Both use SINGLE_ISSUER/DEFER_TASKRUN and no SQPOLL.
No ordinary-probe/default-module dependency or host kernel/base-package change.

Sources:
- https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/loop.c
- https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/bpf-ops.c
- https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/io_uring.c
- https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/net.c

## Comparisons, real assets and fidelity

Candidate:ordinary vllm_graph_uring_loop with pre-submit CQ snapshot.
Main baseline:efficient native timed-epoll TCP, the strongest runnable
same-compute alternative. Matching or losing to it changes the delivery
interpretation; published/old measurements cannot provide a matched changed-
source comparison. Former-loop control:ordinary vllm_graph_uring_loop_after,
a component ablation restoring0044's snapshot semantics, not a second main
baseline. Drop SQPOLL/module rows; their earlier results do not discriminate
this one change.

Use original Workspace/main, same RTX5090/Linux7.3rc3, checkpoint revisions,
FP16, vLLM0.31.0/Torch2.13+cu129/Transformers5.17, normal TCP, wire/client/prompts,
model policy and counters. Official temporary libbpf1.6.3 is common to all
conditions; base/system libraries remain untouched. Native completion wait
and loop multishot timer stay60000ns. Flags/dependencies are identical to0044
except optional before/after object selection. No retained infrastructure delta.

Freeze byte-identical0044 references before new outputs:Qwen17 keys/22 whole
sequences,Smol17/19, derived from prior independent upstream trajectory replay.
Every ordinary valid complete reply must match one exact whole qualified
sequence for its prompt/gen. No tolerance, tokenwise union, teacher forcing,
post-observation expansion or replacement of failed cells. Ordinary current
batch/KV histories remain unobserved; traced strict checks independently
replay actual histories. No identical concurrent-output or task-quality claim.

## Real preflight and integrated qualification

Fresh plan review precedes new serving. Rebuild candidate/control ordinary/
traced plus native and the existing default module trace used by the analyzer.
Qwen preflight runs all3 paths/four cells,8 measured requests/cell and8 excluded
gen1 warmups/executor:120 total requests/3144 checked tokens. At most three
real preflight attempts; preserve any failure.

Both models then run all3 paths through the existing622-request traced and
ordinary strict protocols:12 executors/7464 requests/266688 valid tokens,
3108 intended rejects/60000 empty connections. Keep actual fragmentation,
prompt/block edges, concurrency1..8, reuse/wrap, mixed pacing, pipeline,
half-close, rejection, following valid requests and helper-thread SIGTERM.
Loop candidate/control each show one blocking steady io_uring_enter and no
userspace socket calls or SQPOLL task. Native engages actual accept/recv/send.
Each ring drains SQ and CQ separately with pending/error/drop/reservation0.

Candidate HF shared transport also runs both original eight-idle-cycle/
lifecycle workloads from0044:32 requests/652 checked complete/prefix tokens
per model,13 closed connections and3 expected aborts. Reuse exact original
oracle,wire,pacing,cases and SIGTERM target; adapt only root/binary. These
checks are dependencies, not independent paper/performance results.

## Full runs and primary metrics

Existing source-native bench adds --loop-progress-comparison with modes
(uring_loop,userspace,uring_loop_after). Four cells gen1/64 at c1/8,64 measured
requests/cell,8 excluded checked warmups/executor. Both models,all6 transport
permutations,identical cell rotation as0044; Qwen thenSmol without overlap.
Full scope36 executors/144 cells/9216 measured requests/299520 tokens plus288
excluded warmups. Do not replace timing cells.

Four predeclared primary native contrasts,two/model:
1. native-minus-candidate mean TTFT at gen1/c8;
2. candidate-minus-native output tokens/s at gen64/c8.
Both positive favor candidate. Gen1/c8 is selected before outputs because
0044 negatively bounds this condition for both models, rather than selecting
a favorable new cell after observation. Keep gen1/c1 and gen64/c1 as secondary.
Former-loop before/after TTFT/TPS effects are component contrasts, reported
separately; all CPU,completion/TPOT/p50/p99 effects are secondary.

Six process blocks—not pooled requests—form paired units. Nominal two-sided
t95 df5,critical2.570581835636305/sqrt6. Report all four primary intervals and
every negative estimate/outlier; no familywide superiority, equivalence,
noninferiority cutoff or overall score. Positive,negative,crossing-zero
intervals respectively support,contradict,leave inconclusive that scoped
native delivery metric. Component improvement alone cannot establish a native
win. CPU is a tradeoff, not a latency benefit or arbitrary veto, except faults
or unfair mechanism engagement invalidate comparison.

TTFT/TPOT/TPS follow versioned official vLLM serving metrics:
https://github.com/vllm-project/vllm/blob/v0.31.0/vllm/benchmarks/serve.py
https://docs.vllm.ai/en/v0.31.0/design/metrics/
Known-worker CPU uses existing CLOCK_PROCESS_CPUTIME_ID brackets and actual
worker identities,including creator kernel work once. RX/softirq/BPF/TCP
elsewhere,client and energy are excluded. Clock definition:
https://man7.org/linux/man-pages/man3/clock_gettime.3.html

## Execution, reproducibility and decisions

Use existing driver/analyzer,not a toy runner or experiment-control layer.
Concrete command/environment bindings are archived before serving. Build with:

    make vllm-graph-uring-loop vllm-graph-uring-loop-after vllm-graph-user-network-wait vllm-graph-trace VLLM_PYTHON=ENV/bin/python
    ENV/bin/python bench/vllm_serving.py --loop-progress-comparison --untraced --reference-path FROZEN --preflight --model QWEN --output TEMP/preflight.jsonl
    ENV/bin/python bench/vllm_serving.py --loop-progress-comparison --correctness --model MODEL --output TEMP/MODEL_traced_correctness.jsonl
    ENV/bin/python bench/vllm_serving.py --loop-progress-comparison --untraced --reference-path FROZEN --correctness --model MODEL --output TEMP/MODEL_correctness.jsonl
    ENV/bin/python bench/vllm_serving.py --loop-progress-comparison --untraced --reference-path FROZEN --model MODEL --output TEMP/MODEL_performance.jsonl
    /usr/bin/python3 bench/vllm_serving_analysis.py RAW

Qualify source,commit/push main and freeze one revision before timing. Prior0044
analysis replay must remain byte-identical; no new numerical set or pacing.
Archive plan/plan-review,source/build/package/command/failure receipts,raw
arrivals/outputs/counters/clocks,analysis and one fresh result review. Target
report table gives all four primary effects plus same-cell former-loop and
known-worker CPU tradeoffs. No unsupported cause of old0044 loss follows.

After full run,fresh review reconstructs completion,commands/changes,baseline
engagement,source-isolation,metrics,uncertainty,numerical limits,all primaries,
negative secondary cells and CPU scope. Cleanup only owned TEMP/builds after
review; preserve original Workspace/Coder/boot/base/global caches/WIP. No endpoint
or empty journal proves continuous isolation. Publish honest main records,
close unchanged timing and continue the full retained project objective.


Concrete TEMP: /tmp/bpfusion-uring-cq-progress-jf93e9xn; ENV=TEMP/runtime; FROZEN=TEMP/frozen_references.json.
