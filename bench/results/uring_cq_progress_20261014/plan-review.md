# PLAN REVIEW round 1: CQ progress observed before SQ submission

Reviewed on 2026-10-14 by fresh reviewer /root/uring_cq_progress_plan_review under research-experiment-design. Review performed against retained yunwei356/bpfusion-dev, /workspaces/repository, main, published HEAD f5a555d9ca0c7914f50a8ef2496109bc3b30b0a8. Reviewer read the skill, new plan, current evaluation and finding0044, finding0044's independent result review, current BPF loop, shared io_uring transport, Makefile, serving driver and analyzer. No source or plan edits, serving, builds, publication or infrastructure mutation were performed. Only this review file is written.

## Verdict

**ADMIT the planned supporting intervention. No scientific or executability defect invalidating the declared comparison was found.** Admission concerns the proposed experiment, not a claim that its new binaries are already built or qualified. At review time only the new archive and unrelated tools/setup_env.sh are untracked; current application source still implements the former post-submit snapshot. Complete the plan's implementation, real preflight and qualification before timing.

The retained local question is:

> what client latency/throughput does the ordinary packed/prefix adapter deliver against the efficient native network alternative after BF_TRACE is removed?

docs/evaluation.md explicitly records no formal paper RQ/thesis contract. This review does not invent or rename one. Planned role remains supporting, with preflight, protocol/lifecycle checks and source-isolation receipts dependency evidence.

## Admission, expectation and counter-outcomes

The prior complete, independently reviewed finding0044 supports a roughly96% reduction in bounded known-worker CPU against SQPOLL, but does not establish native serving superiority. It reports negative Qwen long-output throughput and negative concurrent gen1 delivery effects in both models. Those data cannot measure a missing before-submit intervention by reanalysis. The new run adds a distinct source-backed causal discriminator rather than another unchanged sample or known-weak transport row.

The largest credible outcome is recovering a concrete delivery boundary through kernel-loop coordination while retaining the existing compute and no steady userspace request worker. The source hypothesis is plausible: current BPF chooses its wait target after SQ submission, while its upstream helper can publish completion progress during that submission. Capturing the earlier tail can avoid asking for an additional completion in that situation. This does not establish that the old runs actually slept unnecessarily or that the snapshot caused all their loss.

Expected improvement and contradictory/mixed outcomes change the next decision. A positive candidate/native interval supports only the selected native delivery metric; former-loop improvement without a native advantage remains a component result. Negative or crossing-zero native effects retain a constructor/workload boundary and close unchanged timing. CPU tradeoffs remain separate. No compound CPU-and-delivery victory, equivalence, broad thesis challenge, universal model claim or total-service CPU conclusion is admitted.

The plan compares this small intervention with optimized cross-node deployment as the next alternative. The latter expands deployment acceptance but cannot distinguish this exact local ordering. After0044 the proposed change is a defensible immediate discriminator; requiring more models, timer sweeps or an external serving system would change this experiment's question without repairing an identified defect.

## Source grounding and implementation isolation

Primary upstream sources were opened during review:

- [Linux v7.3-rc3 loop.c](https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/loop.c): the requested CQ index is compared with current CQ tail; positive outstanding distance can wait, while reached progress permits continuing. Local work and check_cq also affect waiting.
- [Linux v7.3-rc3 bpf-ops.c](https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/bpf-ops.c): the submit kfunc calls io_submit_sqes; installing loop operations rejects SQPOLL/IOPOLL and requires DEFER_TASKRUN.
- [Linux v7.3-rc3 io_uring.c](https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/io_uring.c): io_submit_sqes calls io_submit_state_end before return; that state-ending path flushes submission completions.

These support the possibility stated in the plan. Progress already pending from another event, GPU publication timing, timer scheduling, asynchronous task work and batching remain competing explanations. A before/after delivery result identifies the intervention's aggregate effect within this implementation; it cannot independently prove the frequency or duration of avoided sleeps.

The planned BF_IO_CQ_AFTER_SUBMIT object is a clean former-loop component control if it restores actual old steady and quiesced behavior. Only BPF ordering and bootstrap object selection should differ between candidate and control. The existing60us multishot timeout, ring flags, GPU network logic, wire/header/partial-send behavior, device dispatcher and model arithmetic remain common. The predeclared compiled model-dispatch and io_network SASS identity check is appropriate evidence of that isolation, not a replacement for end-to-end correctness.

At this review snapshot the new object/control targets, loader selection and --loop-progress-comparison wiring are not yet implemented. Existing mode==uring_loop special cases appear in driver task checks, steady ENTER checks, queue draining and analyzer task/ring checks; a new uring_loop_after mode must receive the same loop semantics rather than the current generic uring/SQPOLL semantics. It must also inherit the same packed-prefill/prefix-release flags and correct launcher library mapping. These are implementation tasks already entailed by the proposed comparison, not plan blockers or a request for new interfaces. Preflight should expose any omission; do not weaken assertions to accommodate it.

## Baseline roles, workloads and fidelity

The sole main baseline is efficient native timed-epoll TCP with the same optimized model computation. It represents a credible alternative answer to whether removing the steady request worker improves client delivery. If native matches or wins, the interpretation materially changes. Historical means cannot provide a matched numerical comparison to changed source and the actual new execution window.

The old post-submit loop is correctly labeled a component control, not an additional main baseline. SQPOLL and the custom module do not discriminate the snapshot change and are properly dropped; their existing findings remain cited. The native comparison is a same-compute mechanism alternative, not official vLLM-server SOTA. No additional baseline is necessary for this local claim.

Both checkpoint revisions, precision, runtime, prompts, concurrency, wire/client, model policy, queue semantics, timeout and libbpf dependency remain fixed/common. The native and loop60us parameters are nominal settings, not a guarantee of identical actual wake spacing. Different arrival/batch/KV histories are possible and must remain an interpretation limit.

I directly verified that the new temporary frozen_references.json is byte-identical to finding0044's archived asset. It retains FP16, source commit8323c32e19a1fcdf326beba405a411a6276aa8dc, Qwen17 keys/22 whole sequences and Smol17/19, with pinned checkpoint paths. Ordinary outputs must match one exact pre-observation complete sequence. This avoids post-observation reference expansion and tokenwise unions, but is weaker than replaying the current ordinary batch trajectory. Traced qualification supplies independent actual-history replay; neither establishes arbitrary-model correctness or task quality.

## Metrics, primary interpretation and uncertainty

TTFT and output-token throughput are established serving metrics. The plan cites the [versioned official vLLM v0.31.0 serving benchmark](https://github.com/vllm-project/vllm/blob/v0.31.0/vllm/benchmarks/serve.py) and [official metrics documentation](https://docs.vllm.ai/en/v0.31.0/design/metrics/). I opened the benchmark and verified that it reports mean TTFT and output tokens divided by benchmark duration. The repository's token-ID client measures first token arrival and its own fixed cell duration; this is a metric-definition reuse, not execution of the official text-serving benchmark.

The four primaries are predeclared native-minus-candidate mean TTFT at gen1/c8 and candidate-minus-native TPS at gen64/c8 for both models. Concurrent gen1 is selected from an already observed negative0044 boundary before candidate observations, rather than because a new favorable cell was found. Retaining gen1/c1 and gen64/c1 as secondary prevents those conditions disappearing. Former-loop contrasts, CPU, completion, TPOT and percentiles remain secondary and separately labeled.

Six process blocks are the paired units, with nominal two-sided t95, df5. Six permutations balance transport order, although finite sample and time-varying interference remain limitations. Report all four primary estimates/intervals, all component contrasts and negative secondary cells; no familywide superiority or equivalence follows from individual nominal intervals. A secondary metric can invalidate a comparison through a real correctness/fairness/mechanism fault, but must not become an arbitrary veto or be promoted after observing results.

Known-worker CPU uses established CLOCK_PROCESS_CPUTIME_ID brackets with a [clock definition](https://man7.org/linux/man-pages/man3/clock_gettime.3.html). Count all process threads and creator kernel work once; retain documented exclusions for Linux networking elsewhere, clients and energy. Faster delivery at increased CPU would be a measured tradeoff, not a hidden failure.

## Executable scope, correctness and completion

The reused source-native driver/analyzer has existing real-model runs, per-request arrival timestamps, complete outputs, worker clock brackets, counter checks, all6 permutations and cell rotations. The planned extension fits this path without a toy runner or new experiment-control layer. Concrete runtime/model/raw command bindings remain a required pre-serving artifact as already specified by the plan; placeholders in the prose are not themselves execution receipts.

Planned scope is internally consistent: both models, three modes, six blocks, four cells,64 measured requests/cell yield36 executors/144 cells/9216 measured requests/299520 output tokens plus288 excluded gen1 warmups. The all3-path Qwen preflight has120 total requests/3144 checked tokens. Existing traced and ordinary strict protocols yield12 executors/7464 requests/266688 valid tokens,3108 intended rejects and60000 empty connections. Candidate HF shared transport adds unchanged idle/lifecycle workloads for both models as dependency checks.

The fixed oracle, fragmentation/concurrency/reuse/half-close/reject protocol, helper-thread SIGTERM, ring drainage, zero pending/error/drop/reservation checks and real native network engagement are sufficient for this finite comparison. Separate SQ and CQ drainage is correct for multishot semantics. Both loop modes must show one blocking steady io_uring_enter, no steady userspace socket calls and no SQPOLL; native must actually accept/receive/send. Ordinary timing is untraced, so qualification tracing must not be described as timed per-request tracing.

The implementation and qualification are incomplete now; this is ordinary staged executability, not an invalid experiment. Real preflight allows at most three attempts. Failures, necessary deviations and affected reruns must remain recorded. Qualify and freeze one committed main revision before full timing, preserve all planned cells and numerical sets, replay old0044 analysis byte-identically, and give one fresh result reviewer raw evidence for independent reconstruction. Completion requires the full integrated matrix; a prefix is not a result. Cleanup must preserve original Workspace/Coder/base/boot/cache and unrelated WIP.

## Blocking defects and optional refinements

**Blocking scientific/execution defects: none found in the proposed plan.**

No follow-up review is needed for unchanged implementation of this admitted plan. The main caution is interpretive: keep the source-backed potential for an unnecessary wait distinct from measured proof of that event, and distinguish the native primary hypothesis from the secondary before/after mechanism contrast. No extra instrumentation, workload, baseline, timer search, infrastructure entity or publication gate is requested.
