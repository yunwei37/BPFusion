# Native userspace network control: independent plan review

Fresh reviewer: userspace_network_plan_review. Read-only review completed
2026-10-11UTC. No workload or file mutation was performed by the reviewer.

Verdict: admitted. No scientific or executability defect blocks the declared
supporting component ablation. Finding0024 has no userspace network condition;
reanalysis cannot replace this matched comparison. Positive, negative, mixed
and inconclusive effects lead to different optimization decisions. It is not
an external main serving baseline, SOTA comparison or new paper RQ.

The source retains the same HF capture, FP16 computation, private eight-bank
KV/input/output layout, resident GPU dispatch, validation, decode, sampling
and FIFO DONE publication. The control changes transport and the backing page
to an anonymous CUDA-registered mapping, without host model execution or
per-token CUDA launch. One active request per connection matches the measured
closed-loop workload, while pipeline-admission performance remains outside it.

The reactor retains partial-byte offsets, retries nonfatal sends, preserves
peer lifetime through GPU ownership, handles read half-close and only
publishes FREE after DONE plus completion/disconnect. Small response sizes
and finite regressions do not establish exhaustive backpressure robustness.

Important scope: userspace may send header and available body in one busy
iteration. Kernel TX sends one header/body part per poll and sleeps with
usleep_range(60,120). Thus measured effects include transport polling and
write grouping; they cannot isolate syscall removal alone. This is a
limitation, not a blocker, especially for interpreting buffering plateaus.

Independent raw inspection found both cases exit0 and ALL_TWO_COMPLETE at
06:48:39UTC. Each has335 valid requests,20432 exact tokens,259 rejects,
accepted5058,published/completed594,rejected259,one resident launch,
20432 model graphs,banks8,max_active8,graph_error0. All78 printed64-token
reference/actual arrays agree. The unchanged harness checks the remaining
responses. Traces show after-ready accept/receive/send, directed helper
SIGTERM and normal exit. Live module/pin checks are absent. These strace
qualification timings are not performance evidence.

Commands, output paths, independent oracle, alternating order, rotated cells
and completion criteria are executable. Per model:40 cells,2560 measured
requests,83200 tokens,ten normal exits; across both:80 cells,5120 requests,
166400 tokens,20 exits. Each full process serves264 requests/8580 model graphs.

Metrics match the cited NVIDIA definitions. Pairing, signs and nominal df4
two-sided t95 formula support the two declared primary effects. The fresh
result review must independently reconstruct unique cells, prompt/index
coverage, timestamps, counts, order and failures beyond the analyzer checks.

Preserve loopback/token-ID HTTP, closed-loop clients1/8, two checkpoints,
shared GPU, nominal intervals and descriptive global CPU scope. Process CPU
excludes kernel TX/softirq in the kernel condition; it cannot establish total
service CPU savings. No required repair or follow-up review was requested.
