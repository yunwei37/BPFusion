# Fresh plan review: AMK residency and model-overlap discriminator

Observation: 2026-10-14. Original Workspace repository HEAD ea23b08c3fe512ee08acd6eca3b31e12276a9d6f. This review changes only this ordinary Markdown report in the caller's owned temporary directory. No experiment was run, production or paper files edited, numerical reference changed, or infrastructure mutated.

## Verdict

**ADMIT for real preflight and, after successful preflight and source/command freeze, the declared full experiment.** No scientific or executability defect currently invalidates the proposed bounded discriminator. Runtime support and trace completeness remain to be established by actual preflight; they are not assumed proved by documentation or finding0047.

Role: supporting. Retain the user's performance/reuse objective and finding0030 question; no formal RQ exists in docs/evaluation.md, and none is invented here. A positive result would support a constructor/backend scheduling boundary and inform a model-independent driver change, not a general eBPF speedup or necessary-thesis claim.

## Evidence read and checked

Read the complete current plan, docs/evaluation.md, findings0030/0048, complete previous AMK result-review.md, previous matched runner/analyzer and raw full.jsonl, AMK graph builder, resident qwen_graph.cu, network launch source, post-run resource inspection and compiler resource receipts, and finding0047 profiling adapter/setup. docs/idea-story.md and docs/background-related-work.md do not exist; the available retained objective and explicit evaluation limitations are authoritative, rather than an invented paper contract.

Independently scanned the previous full raw: 15 start/ready/executor/verified/terminal-success records, 60 cells, 3960 complete request records, and terminal exit0 at 08:55:34 UTC. From raw cell values, long-output throughput means are:
- native c1 165.099036 and c8 303.376970 tokens/s;
- loop c1 164.203653 and c8 158.094137 tokens/s.

Those numbers confirm a real new uncertainty rather than an unexecuted hypothesis. Prior max_active8 proves active graphs/requests, not concurrent cooperative model executions. Resource receipts show AMK REG106/STACK256/static shared34448 and io_network REG40/STACK768/static shared0; they do not settle placement, dynamic shared allocation, overlap, or causality.

The actual current source launches io_network with one block and one thread on a cudaStreamNonBlocking stream (executor/io_uring_tcp.h lines418-419). The dispatcher launches private model child graphs fire-and-forget then tail-resumes after children finish. AMK builder explicitly marks the original model nodes cooperative and device-updatable. These observations support the proposed residency question without answering it.

## Scientific admission and nonduplication

The hypothesis is not that removing CPU work must improve every backend. It asks whether this additional resident GPU work is sufficient to reproduce the observed AMK c8 loss without network traffic, together with measured model-overlap changes. That is a useful causal discriminator inside the retained driver/backend objective.

The existing full matrix contains no model activity timelines or native-plus-resident counterfactual. Neither numerical reanalysis nor static resources can reconstruct them. A matched new run is therefore necessary for this limited question. The native loop engagement rows would be redundant alone; their role here is contemporaneous replication and mechanism engagement for the missing control/timeline relation.

Positive, negative and inconclusive results lead to different decisions:
- slowdown in ordinary native-plus-resident, with trustworthy reduced overlap, supports sufficiency of that control and prioritizes the driver residency/scheduling boundary;
- unchanged control with loop overlap loss narrows attention toward actual network work or progress, but does not prove residency harmless because the park kernel differs;
- longer kernels with similar overlap shifts attention toward execution/resource interference rather than loss of whole-kernel overlap;
- instrumentation-sensitive or incomplete timelines leave ordinary causal transfer inconclusive, while complete ordinary counterfactual performance may still bound that specific control.

This outranks another unchanged timer/CQ sweep or an unqualified backend port because it can change the implementation decision without a model-arithmetic campaign. It does not require proving a universal cause or selecting a redesign before the data.

## Baseline/control fairness and attribution

The same-AMK native TCP alternative is credible and efficient, with real CPU epoll networking and the same resident model/private-bank dispatcher. Current loop is the candidate. Native-plus-resident is a null/resource control, correctly not presented as an external baseline. No extra vLLM or general serving baseline is required for this within-AMK causal comparison; prior finding0048 already records the faster vLLM practical backend.

All conditions must retain the same checkpoint, FP16 program/cubin, cpasync variant, eight banks, discovered170-SM geometry, K1 construction, request inputs, generation budgets, network defaults and runtime/build lineage. Preserve actual code/environment bytes in metadata. Native and native-plus-resident should differ only in the recorded launch/teardown hook and added temporary kernel; any compiler/entry differences remain explicit.

One thread consumes a warp/block allocation and has real instructions, mapping traffic, registers and instruction-fetch behavior. It is not zero-cost or a bit-identical occupancy surrogate for io_network. The plan acknowledges this correctly: a positive result establishes sufficiency of the specific control collectively, not SM occupancy alone or proof that every component of real networking is unnecessary. A negative result cannot eliminate the actual resident networking kernel's resource explanation. Record actual compiled resources and dynamic shared/launch geometry; do not replace those observations with arithmetic based only on static receipts.

The added control polls the existing stop with system acquire and exits before page unregister/free. This preserves the mapped-pointer lifetime. Actual preflight must demonstrate normal stop/quiescence for it, rather than relying on a timeout. Adding a test-local control does not authorize a production daemon, scheduling policy, arithmetic retarget, exclusive GPU slot or runtime mutation.

## CUDA/CUPTI feasibility and instrumentation limits

The official CUDA API path and existing successful device-controlled AMK graphs make this executable in principle. Cooperative launch permission does not guarantee simultaneous executions; real timeline evidence is the purpose of this experiment. The plan does not require a predicted overlap count as a correctness condition.

NVIDIA documents that concurrent activity tracing allows concurrent kernel execution, whereas serial kernel tracing changes execution by serialization. Concurrent tracing can still perturb short-kernel durations. Therefore explicit concurrent/HES/device-graph setup, successful API statuses and ordinary/profiled paired delivery are justified; neither an enabled flag nor an overlap-looking Chrome row alone proves correct collection. [CUPTI12.9 usage](https://docs.nvidia.com/cupti/12.9.1/main/main.html)

The activity structure documents graph/node identifiers, launch type, launch geometry and resource fields. Official graph-node IDs should be obtained through CUPTI's graph APIs/resource correlation and associated with actual constructed bank/position nodes; pointer values and kernel name alone are insufficient. [Kernel activity metadata](https://docs.nvidia.com/cupti/api/structCUpti__ActivityKernel8.html), [CUPTI activity API](https://docs.nvidia.com/cupti/api/group__CUPTI__ACTIVITY__API.html)

Finding0047 profiled only the current vLLM short-input construction. It is useful adapter evidence, not proof that Torch/Kineto's exported fields or CUPTI collection cover this AMK concurrent cooperative/device-updatable construction. Preflight must exercise each real path and profiled collection, inspect actual field presence/launch geometry, observe complete model-node coverage, and retain dropped-event/status evidence. A standard direct activity adapter is acceptable if the existing export lacks documented fields; synthetic records or serialized/toy fallback are not.

Ordinary and profiled measurement pairs must retain identical compute construction. If profiles materially alter delivery or the between-condition pattern, report profiled overlap descriptively and ordinary causal transfer inconclusive. Crossing-zero overhead intervals do not prove equivalence. No arbitrary percentage cutoff is needed.

## Trace attribution and numerical scope

Expected model calls are prompt_length+gen-1 per request: prefill runs every actual prompt position, then gen-1 decode positions. The existing dispatcher device_graph_launch count equals generated tokens, so it cannot substitute for model-kernel coverage. Include warmups in trace total coverage, then exclude exactly the declared warmups from cell metrics.

The model catalogue must map real graph/node IDs to private bank, prefill graph/count and per-position decode node. Validate ordered position sequences for each bank across reuse, actual full coverage and cell boundaries; count-only validation can miss duplication, omission or wrong-bank launches. Retain unrelated prepare/selected/dispatch/network/park activity separately. Correlating GPU cells with client time must keep calibration uncertainty; do not assign boundary events by an unsupported exact CPU/GPU offset or convert TTFT-minus-span into pure TCP delay.

Model sum-duration divided by occupied union is an overlap diagnostic, not GPU utilization or SM occupancy. Maximum overlapping execution intervals can include tiny scheduling overlap and is not itself a full throughput explanation. Joint per-model durations, occupied union/full span and ordinary throughput provide the appropriate bounded interpretation.

The unchanged pre-observation0045 whole-sequence pools are independent of this counterfactual and are suitable for the declared finite workload. Keep complete sequence membership, not tokenwise mixing or expansion after observations. The eager-HF exact failure stays failed. This experiment cannot claim all-input parity, current batch/KV replay or a repair of the previous numerical discrepancy.

## Workload, metrics, uncertainty and cost

The arithmetic of the matrix is consistent: three paths times two instrumentation states times five blocks =30 actual executors; two cells of8 requests gives480 measured requests and30720 measured tokens; eight gen1 warmups per executor adds240 checked excluded outputs. The finite single wave at c8 is sufficient for an overlap counterfactual, not a steady offered-load capacity, tail/SLO or representative request-distribution claim.

Process-block paired effects are the relevant replicate; 480 requests do not make480 independent experimental replicates. Nominal t95 with df4 is acceptable for the declared supporting result, retaining all five signed differences and no favorable exclusions. Path-order permutations and reversed instrumentation order reduce some order confounding but do not certify isolation.

One minor documentation clarification should be completed before full collection: the plan calls client metrics standard but does not yet link their defining benchmark or spell out their formulas. Retain the existing source-native definitions:
- throughput = total measured output tokens / (last measured token arrival minus first measured request send);
- completion = last-token arrival minus request send;
- TTFT = first-token arrival minus request send;
- TPOT, if retained secondarily = (completion minus TTFT)/(output count-1).

The official vLLM benchmark documentation provides the standard client-latency terminology; explicitly describe the finite cell window as the local sampling convention rather than silently equating it with another benchmark's timed window. [vLLM benchmark CLI](https://docs.vllm.ai/en/stable/benchmarking/cli/)

This is a citation/formula clarification, not a scientific rejection or demand to add metrics, more samples or wider models. Existing source-native analyzer arithmetic is sound for this declared window.

## Execution, completion and restoration

The exact adapters/build/run command are not yet materialized in the reviewed archive. The plan explicitly requires archiving them before full collection and uses the original authoritative model/server/client path. That is adequate to admit necessary implementation and real preflight, not a claim that a full command already exists.

Complete all30 executors and both cells, record real child exits and the exact frozen source before full collection, preserve failed attempts/partial data, and distinguish terminal command failure from observer timeout. Real profile inability closes the timeline claim as declared, rather than inviting an unbounded substitute experiment.

All full outputs, graph/update errors, admissions/reclamation, SQ and CQ independently empty, and owned-resource shutdown must be checked. Actual host journal/GPU/memory brackets keep existing warnings and new faults visible; neither endpoint absence nor journal absence proves continuous isolation. The default library, base packages, original Workspace/PVC/Coder sessions/cache and unrelated tools/setup_env.sh must remain preserved. Only owned TEMP/build resources are removed after review.

No added infrastructure, arithmetic tuning, formal-RQ rewrite, repeated unchanged review or expanded baseline matrix is required. Proceed with actual preflight under the admitted plan and bring the completed raw matrix to one fresh result reviewer.

## Same-review follow-up: source/instantiated graph identity unavailable after preflight3

Observation: 2026-10-14, after the caller's three recorded preflight attempts. Read preflight-repairs.md, actual preflight3.jsonl, all three profiled trace.json.gz/graph_catalogue.json artifacts and the test-local residency hook. This is the first follow-up in the same review; it neither resets the review limit nor runs another preflight.

**Verdict: retain ADMIT for the unchanged30-executor counterfactual matrix, with the plan's explicit unsupported-timeline fallback exercised.** Per-bank/position trace proof and its causal model-overlap claim are unavailable. That missing proof does not invalidate ordinary throughput, numerical-set correctness or the independently randomized/ordered native-plus-park versus native intervention.

The actual raw has six start/ready/executor/verified/executor-terminal-success records, twelve measured cells and144 complete replies, ending exit0 at09:48:11 UTC. Each executor records24 requests/1032 output tokens, one root launch, zero graph errors and eight zero AMK argument-update errors. Both loop variants independently report SQhead=SQtail and CQhead=CQtail and normal transport cleanup. These are real serving results rather than a profile-only toy.

Each of the three profiled traces contains1128 amk_megakernel_persist records with grid[170,1,1], block[256,1,1]. Raw-graph catalogues contain official source-node identities and cooperative attributes, but activity records identify instantiated graphs: for example first activity graph1529/node6567004995584 cannot be authenticated as the raw catalogue's corresponding bank/prefill/position. The instantiate API activities inspected do not supply source/exec graph identifiers. Kernel name, expected count, source geometry and numeric ID patterns cannot repair that identity relation. Thus1128 matching counts are an observation, not complete node/sequence validation. Similarly Kineto's estimated occupancy fields are estimates, not measured residency.

The missing identity invalidates a claim that every event follows the correct private-bank/prefill/decode trajectory, and prevents the required authenticated cell/bank overlap attribution. Close that planned timeline claim, keep the actual trace/catalogue and unsuccessful lookup visible, and do not infer an ID offset, silently convert the failed trace assertion into a full-pass flag, or advertise exact trace coverage. Whole-session name-filtered durations can at most remain descriptive unvalidated diagnostics; they cannot supply the promised causal proof.

The ordinary counterfactual is still a direct, previously absent intervention: same real model and native TCP, with only this extra resident control and its documented launch/teardown hook. A reproducible effect can establish sufficiency of this specific control collectively to degrade throughput without network handling. It does not establish that reduced cooperative-model overlap is the mediator, isolate SM occupancy, or prove that io_network has precisely the same cause. An unaffected control also remains decision-relevant, within its differing footprint limitation. Neither decision was supplied by finding0048.

Retain the full hypothesis wording and matrix, including ordinary/profiled delivery checks. Report the ordinary primary throughput result separately; the conjunctive suppression-of-overlap mechanism remains incomplete/inconclusive. This is the predeclared fallback, not a newly convenient easier hypothesis or permission to declare the originally promised timeline achieved. No additional preflight or interface repair is authorized by this follow-up.

Before full collection, document this preflight limitation in the ordinary plan/execution notes so the fresh result reviewer receives the failed coverage evidence alongside the unchanged30-executor command. That reviewer must separately assess metric validity, counterfactual effect and unavailable mechanism claim. Publish neither preflight magnitudes as the final result nor a bank/position-concurrency conclusion. The remaining ordinary effect retains supporting research value and justifies the already-admitted complete matrix; source freeze, complete outputs, normal lifecycle, all negatives, actual host observations and restoration obligations remain unchanged.
