# 0024: concurrent whole-request graph dispatch control

## Question and admission

The user asks for throughput/latency improvement and a reproducible matched comparison of Linux TCP/HTTP -> eBPF/shared queue -> resident real-model inference -> kernel TCP TX. This repository has no paper RQ, thesis or evaluation contract. The supporting engineering question is: does keeping whole-request service dispatch resident improve client TTFT and output throughput when both policies have the same eight private graph/KV banks and GPU-controlled decoding?

Finding0020 measures serial dispatch and finding0023 measures serial-to-concurrent execution. Neither can isolate dispatch against the present concurrent path: its old host control has one bank. Reanalysis cannot restore the missing concurrent host condition. This comparison closes that confound; it is a component ablation, not an external main serving baseline or a headline novelty result. A positive effect supports this local control policy. Null/negative or mixed effects bound its latency/throughput benefit and direct the next effort toward stronger upstream-backend/optimized-server/physical-NIC evidence rather than repeated unchanged dispatch runs.

The more consequential alternative is a matched optimized serving comparison using a qualified upstream megakernel. Current MPK and Plow SM120 qualifications have failed exact output controls; the other candidates need qualification and online lifetime adaptation. Correcting the already-qualified graph control is the strongest currently runnable causal discriminator without another model-math tuning campaign. Its result cannot settle competitiveness or establish the entire service goal.

## Matched implementation

Both modes capture the same BF_LLM_SLOTS graph banks using the same Python source, shared read-only exported Qwen2.5-0.5B fp16 weights, eager HF batch1 computation, device argmax, private input/KV/output layout, graph catalogue, admission loop, FIFO retirement/reclamation and eBPF/kernel TCP path. The control returns after each published DONE, and its host synchronizes and resumes the same service graph; decode remains GPU-tail controlled, with no host token loop.

Sampling now moves an unfinished request from phase1 (child output waiting to be consumed) to phase3 (next model graph waiting to be launched). A host return while retiring another slot must preserve that distinction; otherwise re-entry would read stale output as a new token. The resident path launches phase3 in the same iteration, preserving its computation sequence. Host mode has eight banks, so the earlier single-bank admission restriction is removed. No protocol, page ABI, model arithmetic, precision, checkpoint or persistent runtime setting changes.

Correctness precedes measurement: the existing gen64/prompt-edge TCP/HTTP regression must pass for both modes, including 335 valid requests/20432 exact output tokens, 259 rejections, eight concurrent clients, mixed gen1/gen64 lengths, immediate reuse, ring wrap, ordered pipeline, half-close and all-thread network tracing. Both report banks8/max_active8, graph_error0 and 20432 model steps; host service launches594, resident1. Exact HF oracle and request/shutdown timeouts remain fixed.

## Workload and interpretation

Reuse bench/resident_dispatch.py and the four existing real prompts with independently computed eager-HF fp16 reference tokens. Use gen1/gen64 and closed-loop client concurrency1/8; both modes progress private batch1 requests, not tensor-batched matrix operations. Five paired process blocks alternate mode order, rotate the same cell order within a pair and serve64 measured requests/cell (16 per prompt), plus eight excluded gen1/gen64 warmups/process.

The [NVIDIA metric definitions](https://docs.nvidia.com/nim/benchmarking/llm/metrics) supply client TTFT, TPOT excluding the first token, completion latency and aggregate output TPS over first-send/last-token-arrival. Primary concurrent gen64 effects are host-minus-resident mean TTFT and resident-minus-host TPS, assessed separately. Report every pair and nominal two-sided t95 intervals, df4, using the [NIST critical value](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3672.htm). Positive intervals support a local benefit; negative intervals contradict it in that cell; crossing zero is inconclusive, not equivalence. Clear tradeoffs are mixed support. Gen1, one-client cells, completion and TPOT remain diagnostics rather than hidden vetoes. No familywise superiority or robust P99 claim is made from five pairs.

Connection/thread creation, model load/capture, warmup, GPU queries and shutdown precede or follow the measurement windows. Multiple tokens completed in one recv share an arrival timestamp. Bootstrap duration is recorded separately. Executor process CPU includes its threads but excludes kernel TX/softirq. Raw global /proc/stat counters additionally record user+nice+system+irq+softirq CPU work in approximately the same cell window, including client threads, kernel work and unrelated host workloads. They are descriptive whole-host observations, not an attribution of service cost or energy savings.

Both use the canonical default listener buffering: no temporary TCP_NODELAY build or transport tuning. Both clients use the existing common TCP_NODELAY setting. Prior NODELAY runs are historical evidence, not numeric controls for this collection. Another project's SGLang workload stays in place on the shared RTX5090; record coarse GPU state and host process residency/boot/Xid observations. Alternating pairs reduce but cannot eliminate temporal confounding. No isolated speedup, GPU-ready latency, physical-NIC, text/tokenization, integrated energy or optimized-serving claim follows.

## Execution and completeness

Build with make qwen-graph qwen-graph-control in the original bpfusion-dev Workspace/main. Native default binaries, capture code, weights and oracle are identical across preflight/full run. The runner waits for readiness or process exit rather than the obsolete60-second capture cap; record this before execution because eight banks take longer to capture. Original request and shutdown timeouts are unchanged.

Commands:

```sh
HF_HOME=/workspaces/.cache/huggingface python3 tests/resident_qwen.py --gen 64 --prefill-edges --executor ./build/qwen_graph_host_launch
HF_HOME=/workspaces/.cache/huggingface python3 tests/resident_qwen.py --gen 64 --prefill-edges --executor ./build/qwen_graph
HF_HOME=/workspaces/.cache/huggingface python3 bench/resident_dispatch.py --gen 64 --preflight --resident-executor ./build/qwen_graph --host-executor ./build/qwen_graph_host_launch --output bench/results/concurrent_graph_dispatch_preflight_20261011.jsonl
HF_HOME=/workspaces/.cache/huggingface python3 bench/resident_dispatch.py --gen 64 --resident-executor ./build/qwen_graph --host-executor ./build/qwen_graph_host_launch --output bench/results/concurrent_graph_dispatch_20261011.jsonl
python3 bench/resident_dispatch.py --analyze --output bench/results/concurrent_graph_dispatch_20261011.jsonl
```

Preflight has four exact measured gen1 requests/mode following the same eight warmups. Full completion requires40 unique cells,2560 measured requests,83200 exact measured tokens, ten normal process exits, every index0..63 present once/cell and all five pairs retained. Each full process serves264 requests/8580 model graphs, reports banks8/max_active8 and graph_error0; resident service launches1 and host264. Every process has zero registration/admission drops, all eight final slots FREE, and module/hook/pin cleanup. Approximate cost is ten bank-capture starts plus the complete serving matrix, around fifteen minutes on the shared device; it is not a fixed investigation limit.

Preserve stdout and raw request/cell/bootstrap/idle/executor/failure records. A partial prefix or successful trigger is incomplete. Keep failed attempts with distinct paths and unchanged oracle. Fresh plan review precedes real preflight; a fresh result reviewer independently reconstructs counts, timestamps, metric signs, CPU counter scope, resource matching and all reported effects. Review is diagnostic, not an extra permission gate. The intended table contains both matched modes and every paired effect; historical serial-control results remain unchanged.

## Correctness result

Both native Makefile targets build successfully after the shared dispatcher change. The [concurrent host raw](../../bench/results/qwen_concurrent_host_control_correctness_20261011.txt) and [resident raw](../../bench/results/qwen_concurrent_resident_correctness_20261011.txt) each complete the unchanged strict regression:335 valid requests/20432 exact generated tokens,259 rejects,5000 empty connections, eight persistent clients, mixed decode lengths, immediate reuse, wrap, ordered pipeline and half-close. Both record20432 model graphs,graph_error0,banks8,max_active8 and eight final FREE slots; service launches are594/1 respectively. Independent raw reconstruction checks all39 printed expected/actual arrays and the after-ready network syscall search; the full original traces are preserved in those raws. Resident qualification has an explicit exit0 receipt. The first host launcher did not retain a wait()/exit-code receipt; its terminal PASS output and absent process are recorded without inventing that status.

These qualify the concurrent control and re-entry/lifetime behavior, not a serving speedup. Old one-bank results remain historical. No arithmetic or upstream-backend change follows.


## Independent plan review

A fresh read-only reviewer checked admission, the native phase1/phase3 state
transition, FIFO retirement and host re-entry, identical eight-bank capture,
strict correctness receipts, published metric definitions, paired sampling,
commands, resource conditions and interpretation. The review found no scientific
or execution defect that invalidates the planned component comparison, so it
can proceed to real preflight and full collection.

The review identified missing paired TPS intervals and completion aggregation
in the existing analysis output. The minimal analysis change now reports
resident-minus-host TPS for every pair and its nominal df4 t95 interval,
completion mean and the descriptive whole-host CPU observations. One focused
read-only follow-up verified the signs, formula and diagnostic scope. Preflight
has one pair and reports null intervals; it cannot establish a performance
effect.

Fresh result review must independently check the complete unique matrix,
request indices and prompt balance, exact tokens, timestamp-derived metrics,
native launch counts, zero drops and final FREE slots. These are evidence checks,
not a new runtime control interface. No reviewer ran GPU work or edited source.
