# Experiment plan: chained device-graph dispatch

## Retained question and paper-value admission

No formal paper RQ/thesis exists. Preserve the complete Linux TCP/HTTP to eBPF/shared queue, resident real-model inference and asynchronous kernel TX objective. Specific uncertainty: can attaching the unchanged GPU dispatcher after upstream model/head graphs and tail-launching the next step reduce client latency and improve throughput against the current separate parent/fire-and-forget dispatcher, with identical compute and transport?

Role supporting. The largest credible story is a reusable device-scheduling improvement across architectures, distinct from an eBPF transport advantage. The current parent launches model work and itself separately for every step. Findings0032-0035 do not contain the missing chained condition; no reanalysis can answer this. Official CUDA semantics establish legality, not latency. A reviewer can reject the existing path as paying unnecessary GPU control overhead. Positive results justify adopting a simpler launch sequence after fidelity/lifecycle checks; negative/inconclusive results close this candidate without asserting a gain or changing ordinary defaults. This tests an implementation boundary, not a necessary novelty thesis.

The strongest alternative is service-attributed CPU/interference measurement or an official host scheduler comparison. Those are useful for proving CPU-path value, but cannot eliminate the identified redundant graph launch or answer the user's request to improve current latency/TP. This candidate changes only reusable orchestration and directly tests a source-visible cost; avoid single-model arithmetic tuning or an unchanged transport repetition.

## Expected answer and official assets

Prediction: one device launch instead of two per model step lowers latency and increases gen64 throughput. Competing explanation: upstream GPU compute dominates, while changed graph environment/dependencies cancel the saved launch or regress scheduling. An interval wholly negative contradicts that metric; including zero is inconclusive, not equivalence.

Reuse vLLM0.31.0 FULL body/head/greedy sampler, Torch2.13.0+cu129, Transformers5.17.0, FP16, original pinned Qwen2.5-0.5B-Instruct and SmolLM2-135M cached checkpoints, eight request/KV slots, all520 graph catalogue entries, packed prefill/prefix release, native60000ns epoll wait and loopback TCP.
CUDA tail-launch and self-launch semantics:
https://docs.nvidia.com/cuda/cuda-programming-guide/04-special-topics/cuda-graphs.html#tail-launch
Metrics/client definitions:
https://docs.vllm.ai/en/v0.31.0/design/metrics/

Source base main fdcd111f6bef1127a7fadc4dcc63e32da475b667. Work only in original /workspaces/repository. Temporary runtime /tmp/bpfusion-tail-chain-cwekbdzh/venv via official venv --without-pip and pip --python, preserving base. Native scheduling candidate adds dispatcher as a dependent kernel after head and tail-launches the chosen next combined graph, including permitted self-tail launch. Metadata, model/head/sampling, wire, BPF/module and output lifetime remain unchanged. Bootstrap pointers/queue/control are allocated before combined graph instantiation; graphs synchronize before destruction. The only added benchmark/build surface is the existing-style candidate comparison, not a persistent service or controller.

## Fair comparison and numerical contract

Current separate dispatcher is the strongest competing implementation for this source-local scheduling question; a matched A/B is necessary and has never run. Kernel and efficient native transports are strata/mechanism controls, not external SOTA baselines. Both conditions use same arithmetic, precision, metadata policy, budgets, client, graph capture and either both traced setup or both untraced timing. Actual batch schedules and FP16 sequences may differ.

Trace setup first uses the existing exact independent host replay: each model history advances from its own computed reference output, with real admission/compute/release/cache ownership reconstructed. No served-token forcing/tolerance change. Run full strict protocol for four conditions on both models (8 executors,4976 requests/177792 tokens,2072 intentional rejects,40000 empty connects). This checks fragmentation, prompt/block boundaries, concurrency1..8, wrap/reuse, mixed outputs, pipelines/half-close, rejection/subsequent validity and helper-thread SIGTERM. After-ready all-thread strace proves kernel has no steady accept/recv/send and native engages intended calls. All launches/graph errors/output bytes/counters/slot recycling must pass.

A traced four-condition Qwen preflight uses four normal prompts,gen1/64,c1/8,8 measured requests/cell plus8 warmups/executor and independent replay. This is integrated setup, not performance evidence.

Then before any untraced observation freeze an exact complete-sequence union by model/prompt/gen from prior finding0034 references plus this experiment's successful independently replayed strict and traced-preflight references. Record contributing files, pinned model/vocab/FP16, source revision and freeze timestamp. This rule is fixed now; do not add untraced outputs or post-hoc variants. Every valid untraced reply including warmups/preflight must match a WHOLE previously qualified sequence. No tokenwise mixing/prefix-only gen64/served history forcing. Finite-set membership is weaker than replay of current unobserved batch/cache/ownership and cannot prove universal numerical correctness/task quality/batch invariance. A previously valid alternative could pass. Retain that limit and prior traced qualification separately. A novel untraced complete sequence fails this contract; retain raw failure, do not weaken check or promote timing.

A four-condition Qwen untraced preflight repeats the same small real cells after freeze. Final aggregate counters, reserved0/eight FREE, published=completed and all native exits/detach/module/pin cleanup are validity requirements. Add a native successful-device-launch counter: separate=2*model_steps, chained=model_steps, independently compare trace steps during traced setup and source/log mode during untraced runs. Per-cell untraced graph/batch counts remain null.

## Full matrix and interpretation

Two models x separate/chained x kernel/native x gen1/64 x clients1/8 x five alternating process blocks =40 executors/160 cells/10240 measured requests/332800 tokens plus320 checked gen1 warmups. Use the existing four prompts,64 requests per cell. Existing alternating four-condition order rotates/reverses by block to distribute exposure; all rows/outliers remain. No historical old/new subtraction.

Primary metrics, separately per model/transport: gen1/c1 mean client TTFT and gen64/c8 output tokens/s, chained versus separate. Positive gain means separate-minus-chained TTFT or chained-minus-separate throughput. Five process-level paired differences, nominal two-sided t95 df4; requests are not independent extra repetitions. Report all eight primaries and every secondary TTFT/completion/TPOT/quantile plus chained kernel/native differences. No multiplicity-adjusted universal claim. A wholly positive interval supports the scoped improvement, wholly negative contradicts, crossing zero is inconclusive; heterogeneous results stay mixed. Correctness/fairness alone can invalidate comparisons. No CPU/energy/external SOTA claim.

## Commands, completion and recovery

Build existing make targets plus candidate vllm-graph-chained, ordinary and BF_TRACE variants with VLLM_PYTHON=/tmp/bpfusion-tail-chain-cwekbdzh/venv/bin/python. PATH points to that runtime, VLLM_ENABLE_V1_MULTIPROCESSING=0, HF_HOME=/workspaces/.cache/huggingface.

    python3 bench/vllm_serving.py --dispatch-comparison --correctness --model PINNED_MODEL_PATH --output /tmp/bpfusion-tail-chain-cwekbdzh/MODEL_correctness.jsonl
    python3 bench/vllm_serving.py --dispatch-comparison --preflight --model QWEN_PINNED_PATH --output /tmp/bpfusion-tail-chain-cwekbdzh/traced_preflight.jsonl
    python3 bench/vllm_serving.py --dispatch-comparison --untraced --reference-path /tmp/bpfusion-tail-chain-cwekbdzh/frozen_references.json --preflight --model QWEN_PINNED_PATH --output /tmp/bpfusion-tail-chain-cwekbdzh/untraced_preflight.jsonl
    python3 bench/vllm_serving.py --dispatch-comparison --untraced --reference-path /tmp/bpfusion-tail-chain-cwekbdzh/frozen_references.json --model PINNED_MODEL_PATH --output /tmp/bpfusion-tail-chain-cwekbdzh/MODEL_performance.jsonl
    python3 bench/vllm_serving_analysis.py RAW

Fresh plan review precedes real serving. Strict and both preflights pass before full collection. Run both complete five-block model matrices and all analyses to terminal; retain failures/deviations and wait the same live handles. Runtime capture/setup dominates cost. Native seconds/trace-request budgets retain existing bounded test-local behavior. Exact commands/source snapshots/raw/stdout/status go under the temp directory and durable bench/results/tail_chain_20261012/. One fresh combined result reviewer independently recomputes membership, timing, paired effects, mechanism counters, exact setup replay, fairness and lifecycle. Preserve kernel journal/co-tenant endpoint evidence without claiming isolation. Archive before removing only owned temp/build output, preserve original Coder sessions/base/modelcache/tools/setup_env.sh. Publish own validated main paths and honest README/evaluation/finding. Do not adopt default merely because builds/preflight pass; require measured benefit and stable correctness, otherwise retain ordinary default.
