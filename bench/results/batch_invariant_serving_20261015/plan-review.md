# Plan review: upstream batch-invariant matched serving

Reviewed 2026-10-15 UTC in the original yunwei356/bpfusion-dev Workspace. This is the fresh initial review requested by research-experiment-design. I did not edit the plan or production sources, install packages, launch serving, or change controls.

## Verdict

Admit this supporting experiment scientifically. I found a concrete executability blocker in the newly supplied serving adapter, reported it during this initial review, and checked its pre-observation repair. Its valid-response equality compared a list with a tuple; the narrow repair normalizes both sides without changing expected token IDs. I found no remaining scientific or executable blocking defect in the proposed comparison or correctness contract. It adds a justified independent fidelity discriminator after0058 and does not reinterpret that failed experiment. The mode's compatibility and output equality remain hypotheses to test, not facts established by this review.

During review the implementation supplied run.py,setup.py,reference.py,serving.py,analysis.py and a private vllm_graph.py, plus a clarified model order. I examined them and their diffs before completing this report. This is the fresh initial review; the narrow implementation repair was consumed within it. The private adapter correctly supplies the two-mode/32-request/five-block matrix absent from the repository driver. Model order is fixed Qwen then Smol and has no between-model causal interpretation.

## Evidence examined

- Current plan.md in this TEMP; current repository main at3cb7685 with only the existing untracked tools/setup_env.sh.
- executor/vllm_graph.py, particularly original in-process LLM(dtype="half",max_model_len=2*limit), retained graph ownership, capture for query lengths1..64 and batch widths1..8, padded-input metadata construction, and exact replay.
- bench/vllm_serving.py, including argument parsing, mode selection, request budgets, reference lookup, trace replay, untraced sequence checks, native/loop mechanism assertions, and raw client/counter outputs.
- bench/resident_dispatch.py request timing and throughput aggregation.
-0057-long-output-service-timeline.md and0058-batched-token-publication.md, including missing profiler coverage, traced/untraced limitations, independent-review outcomes and the unresolved final-two-token mismatch.
- Archived0058 run.py as evidence that the needed private source-native adaptation pattern already exists, not as a command to rerun0058.
- Exact cached official0.31 wheel source: batch_invariant.py lines1052-1176, config/vllm.py batch-invariance graph policy, model_executor/layers/linear.py lines230-239, and GPU worker initialization callsite.
- Official metric and feature documents: https://docs.vllm.ai/en/stable/cli/bench/serve/ and https://docs.vllm.ai/en/stable/features/batch_invariance/ . Source-native behavior of the pinned wheel takes precedence over moving stable documentation.

## Admission and decision value

The actual uncertainty is whether independently generated official FP16 outputs remain the unique expected outputs when the same upstream model computation is invoked by this GPU-owned service, followed by a matched delivery comparison in that mode. Existing traced replay checks the wrapper's own graph/history execution; existing finite output pools cannot prove equality for new ordinary trajectories.0058 shows that this is a practical qualification problem, while its failure does not establish the numerical cause. Reanalysis cannot create an unrecorded actual batch history or an official-mode run.

Reference generation and width/order checks are dependencies folded into a serving comparison. They must not be reported as a new determinism technique, a separate research contribution, or a performance optimization. The planned role of supporting is appropriate. A fully qualifying result materially strengthens ordinary exact upstream-output evidence within this finite workload. A failure gives a useful compatibility/fidelity boundary and stops the affected performance claim. Either outcome changes what can credibly be compared next.

The strongest alternative, offered-load latency with total CPU accounting, is acknowledged rather than displaced indefinitely. It would also require reliable output qualification. This proposal outranks another isolated publisher knob because it resolves a demonstrated validity uncertainty. It does not settle generic backend support, an OSS-wide architecture, or the overall project objective. No invented formal paper RQ or necessary thesis prediction is needed here.

## Baseline and comparison fairness

The single native timed-epoll TCP path is a credible competing answer to the same serving question: efficient Linux TCP with identical FP16 models, graph computation, request capacities, admission/release policy and timer. It is stronger than a Python per-token loop and has matched/won earlier comparisons. Published numbers cannot settle this new optional-mode comparison on this exact hardware and wrapper. Native matching or winning therefore has a real consequence; it is not a definitionally losing control.

Official CPU-scheduled LLM.generate is correctly labeled a correctness control rather than a speed baseline. No extra default-mode performance baseline is required: the plan explicitly declines an estimate of mode overhead and keeps older results as context. Failing native fidelity or capture must not be scored as a loop win. Both measured transports need the same effective upstream mode, dtype, checkpoint, graph settings and runtime. The official control may use the official scheduler and does not need the service's graph mutation adapter; this independence is useful.

No more baselines or models are needed as a condition of execution. The finite models and token-ID HTTP interface are explicit and do not support claims of arbitrary text APIs or model universality.

## Correctness and exact upstream sources

The frozen single complete sequence per prompt is noncircular if it is produced solely by official LLM.generate before observing any serving output. Multiple official widths and reversed orders test the relevant invariance promise instead of adding observed wrapper outputs to an accepted pool. Freeze all ten distinct qualification prompt inputs, not just the four ordinary prompts: the protocol also uses lengths1/15/16/17/32/64. Warmup gen1 and all valid stopped-prefix checks must use the corresponding prefix of that same64-token sequence. Rejected inputs must retain empty output checks. An official disagreement is a failure, not grounds to select a convenient sequence.

A 64-token complete reference per prompt is an appropriate finite exact-token oracle. It is independent of the custom GPU schedule and changes the meaning of untraced checks from membership in observed variants to equality with official output. It does not establish eager-HF equivalence, logits equality, task quality or universal batch invariance. Existing independent graph/KV/history replay in qualification remains valuable as a separate check; neither check substitutes for the other.

I verified that enabling the official flag does affect real paths in the pinned source. GPU worker initialization calls init_batch_invariance. That function initializes tuned configs, environment settings and operation overrides. UnquantizedLinearMethod.apply dispatches to linear_batch_invariant when the flag is enabled. The BF16 tuned breakable-graph policy is conditional on model.dtype==torch.bfloat16; the service's FP16 choice avoids that particular automatic policy, but does not prove graph capture/device launch legality. CUDA non-SM80 initialization sets CUBLAS_WORKSPACE_CONFIG=:16:8 and CUBLASLT_WORKSPACE_SIZE=1, disables reduced-precision reduction and prefers cuBLASLt; other upstream settings also change. Record the actual effective mode and backend, not merely the requested environment flag.

The wheel's non-SM80 comments name SM90/100, while the actual branch also covers this SM120 GPU. That is an empirical compatibility uncertainty; it is not evidence of support or grounds to patch upstream kernels. The present preflight and fixed failure interpretation are appropriate.

## Metrics, repetitions and inference

Client output token/s, TTFT, completion latency and TPOT are recognizable standard serving quantities with the official benchmark citation. The existing client computes TTFT from request start to first received token, completion to last token, and TPOT=(last-first)/(gen-1), leaving gen1 TPOT unavailable. The raw cell throughput uses total delivered output tokens divided by first-request-start to last-token-receipt. Preserve that exact window definition in reporting rather than imply an official CLI run or offered-load/SLO experiment.

The primary gen64/c8 loop-minus-native difference with five paired process blocks and nominal t95df4 is coherent. Pair on the declared block and model, report all five signed differences, and do not pool individual requests as independent replications. Crossing zero is inconclusive, not equivalence. The primary and secondary hierarchy is clear; a latency improvement cannot silently replace failed or inconclusive primary throughput. Any correctness failure invalidates its own speed comparison, which is an appropriate veto.

The planned full arithmetic is consistent:2models*5blocks*2transports=20executors, four cells/executor gives80cells,32requests/cell gives2560 measured requests. Each executor delivers32*(1+64+1+64)=4160 measured tokens, hence83200 measured tokens plus160 gen1 warmups.32 requests/cell give only a small closed-loop sample; this bounds tail interpretation but is not a blocker for the stated paired throughput question. Report raw outliers without claiming production p99 stability. Partial known-worker CPU cannot be promoted to total CPU or energy evidence.

## Defect found and repaired during review

B1: private serving.py inserted official-output check originally compared row["tokens"] (a list from the actual client) with next(iter(reference_pool[...] )) (a tuple built at reference_pool construction). Python list equality with a tuple is false even for identical token IDs. Every valid response would fail by representation, invalidating intended qualification. I reported it before any actual setup or GPU run. The root changed equality to tuple(row["tokens"])==(() if row["bad"] else expected_tuple), preserving exact IDs and empty rejection behavior. I inspected the fixed source. This was a pre-observation runner repair; the frozen oracle and generation did not change. B1 is resolved.

## Concrete adapter examination and nonblocking suggestions

1. The supplied run.py now has concrete separate stage commands, saved subprocess vectors and terminal statuses. setup.py uses private venv/libbpf/BUILD, checks main/base/original build metadata and redirects only owned build symlinks. serving.py maps two conditions,5blocks and32requests, alternates transport order, rotates cell order, uses the private builds, and retains native transport and queue assertions. No production CUDA arithmetic or transport implementation diff exists. The shell-style brace line in plan.md should be read as a choice of stage; actual saved commands are python3 run.py setup, then reference,preflight,qualification,full. Explicitly documenting those commands is useful but not a scientific blocker.
2. reference.py explicitly uses dtype='half',max_model_len=128, same checkpoint cache and the same eight-slot KV-memory sizing as the bootstrap. Official LLM.generate uses token-ID prompts, greedy ignore_eos generation without retokenization/chat template. All10prompt inputs are generated serially64first, then gen1/64 at widths1..8 in forward/reverse chunked mixed-prompt groups with every returned output compared to the frozen prefix. Raw per-call token outputs and effective mode settings are saved. Those details resolve the constructor/coverage ambiguity in the initial prose. Reference width/order testing is empirical finite support, not a universal guarantee.
3. The private bootstrap changes only its root path and a startup assertion/settings print for the enabled upstream mode. The graph capture/replay body is unchanged. This supports matching the intended compute path; actual graph capture legality and performance still require preflight.
4. The new serving.py applies its independent official equality to both traced qualification and untraced performance, while preserving the original exact graph/KV/history replay. After the B1 repair that is the correct integration. analysis.py independently reconstructs ordinary reference equality and metrics. Its traced branch presently rechecks trajectory replay but does not independently reapply the official asset; adding that same exact comparison there is a useful nonblocking reproducibility improvement since the driver already performs it and the complete asset/raw responses remain available for fresh result review.
5. Save all actual versions, compile commands, environment differences and source changes before the corresponding executions. The setup dependency work is not a performance result. The private runtime must not replace base packages, original build artifacts or existing sessions.
6. Retain a brief estimated cost once actual setup/preflight provides a basis; no arbitrary deadline or time cap is needed. Host snapshots should be tied to a confirmed live process for the active sample. The plan correctly refuses to infer continuous isolation from sparse samples.

These points do not require another scientific design, extra baseline, wider model suite or an unchanged-plan rereview. If implementation forces a changed oracle, workload, mode, timeout or evaluation path, record the change under the owning skill and rerun affected comparisons; never use it to turn observed disagreement into agreement.

## Completion and interpretation

Preflight must exercise both actual transports and official control with real checkpoints, actual network path and recorded raw outputs. Passing setup/imports or offline reference generation alone is not preflight. Respect the owning skill's maximum three preflight attempts without replacing the fixed correctness contract.

Full completion needs all planned models/blocks/cells, exact official equality, terminal driver and analysis success, ring/error/lifetime assertions, and cleanup/restoration. If official invariance, graph capture or service fidelity fails, retain the failing inputs/tokens/logs and all unavailable cells; a partial prefix is not a complete performance result. Complete the fresh result review on the terminal evidence even for such a failed path.

A positive performance estimate only supports this optional backend mode/workload/hardware and matched native alternative. A negative estimate bounds this transport arrangement in that mode; it is not a universal indictment of eBPF or resident execution. Successful finite correctness does not explain0058's mismatch, and a compatibility failure does not prove0058 corruption. No mode-overhead, total-CPU, zero-host-work or new GPU-kernel claim follows.

Final judgment: supporting experiment admitted, with no remaining scientific or executable blocker after B1's pre-observation representation repair. Proceed with the fixed preflight and qualification path. Do not rerun0058 or relax its historical outcome.
