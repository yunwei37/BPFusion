# Additional GPU residency reproduces the AMK c8 loss

With unchanged upstream AMK computation, efficient native TCP plus a low-activity
resident GPU control loses about half the tested c8 output throughput. Actual
eBPF/io_uring serving has a similar measured loss. This establishes sufficiency
of this specific additional resident control without TCP work. It does not
establish model-overlap suppression, pure SM occupancy, or an all-backend cause.

## Question, comparison and complete collection

The [plan and fresh review](../../bench/results/amk_residency_20261014/plan.md)
retain finding0030's question: can the CPU request path be removed while
retaining efficient reusable real-model GPU execution? This is supporting
evidence for a driver/backend resource boundary. Finding0048's loss did not
include a residency counterfactual or model activity.

The original bpfusion-dev Workspace/main and RTX5090/170SMs run pinned
SmolLM2-135M revision93efa2f0, AMK884534c4, FP16, cpasync0, eight private banks
and upstream K=1 model nodes. Torch2.13+cu129/Transformers5.17 matches0048.
Model math, weights and bank policy remain the same across all three paths.

The competing mechanism is efficient native epoll TCP. The candidate uses the
existing module-free eBPF/io_uring path with its independent io_network GPU
kernel. The resource ablation adds one block/one thread on a nonblocking,
default-priority stream to native TCP. It performs no network or model work:
it polls the existing mapped stop flag with system acquire and nanosleep1000.
It starts after bootstrap CUDA synchronization and exits before page cleanup.
The control is test-local; production code and defaults are unchanged.

Actual I/O and control both use one block/one thread, but their resource
footprints differ. Profiled control reports16 registers/thread while static cuobjdump reports8;
this discrepancy is retained. Both report no static shared memory;
actual I/O reports40 registers/thread. This is a collective
residency control, not an identical-resource or pure-occupancy experiment.

The complete matrix is three paths times ordinary/profiled times five paired
process blocks:30 executors,60 cells,480 measured requests/30720 tokens plus
240 checked excluded gen1 warmups. Each cell contains8 real gen64 requests at
c1 or c8 over preopened persistent localhost connections, with four literal
prompts. Path and instrumentation order change by block; cell order alternates.
This finite-wave measurement is not offered-load capacity, a tail/SLO result,
or a representative prompt distribution.

All actual executors exit0. All720 complete replies match unchanged
pre-observation0045 whole-output pools; model/graph errors are zero and each
executor has one host root launch and1032 device graph launches. Loop
admission/completion/close and independently empty SQ/CQ checks pass; native
publication/completion and owned-resource shutdown checks pass. The stronger
eager-HF exact discrepancy from0048 remains failed. Fixed-pool membership does
not establish all-input parity or an observed current KV/batch trajectory.

## Ordinary serving results

Means of five process blocks; latency is measured at the client.

| Path | c1 TTFT ms | c1 output token/s | c8 output token/s | c8 completion ms |
|---|---:|---:|---:|---:|
| Efficient native TCP |18.249451|165.083649|309.140757|1652.564841|
| Native TCP plus resident control |18.348098|164.318631|157.765344|3238.916568|
| eBPF/io_uring loop |18.329069|164.341743|157.769889|3237.313627|

The primary ordinary c8 control-minus-native effect is−151.375413 token/s,
nominal pairedt95df4[−152.840219,−149.910607]. All five signed differences
are negative:−151.619264,−151.127902,−151.169466,−153.120608,−149.839823.
The ratio of the displayed means is about49% lower output throughput.
Similar point estimates for control and actual I/O do not establish
equivalence between those mechanisms. The much smaller c1 differences and
the c8 loss narrow the next driver investigation toward residency/scheduling;
they do not repair the experimental AMK backend's absolute latency.

Metrics retain the source-native client convention:
TTFT=first-token arrival minus request send; completion=last-token arrival
minus request send; finite-cell throughput=total output tokens divided by
(last token arrival minus first request send). Latency terms follow the
[official vLLM benchmark terminology](https://docs.vllm.ai/en/stable/benchmarking/cli/).
The sampling window is the declared local finite cell convention.

## Timeline limitation and instrumentation

All15 standard CUPTI/HES/device-graph traces contain exactly1128 model
activities each, with grid170/block256. CUPTI setup statuses are zero and
resident control engagement is visible. However, all raw-graph catalogues have
zero model-node identity matches against instantiated-graph activity IDs.
The recorded instantiation APIs do not supply the missing mapping. No graph-ID
offset inference, per-bank/position validation, cell-overlap attribution or
TTFT-minus-model-span decomposition is used.

Thus the full conjunctive hypothesis about overlap suppression is only
partially tested: the independent throughput counterfactual is supported,
while the suppression mechanism remains inconclusive. The plan's timeline
fallback and review follow-up retain the ordinary primary experiment.
Three real preflights are retained: the first two fail before profiled serving
at dependency-introspection API adaptation; the third completes all six paths.
There is no fourth preflight or substituted toy timeline.

Profile-minus-ordinary c8 throughput differences are−0.377675 for loop,
+0.760852 for native and−0.244096 token/s for control. Their nominal paired
t95 intervals are[−0.689056,−0.066294], [−0.951381,2.473085] and
[−0.368180,−0.120012]. Instrumentation is not zero-overhead or equivalent.
Those comparisons do not restore missing timeline identity.

Actual host brackets retain15 additional NVRM refcntRequestReference status0x56
warnings during full profiled bootstraps, on top of the preflight/historical
warnings. No new selected Xid/reset/OOM/storage failure appears in those
brackets; boot remains04dc0087 and the final GPU application list is empty.
This is not a clean-journal, harmlessness or continuous-isolation claim.

## Reproduction and next decision

The [complete raw archive](../../bench/results/amk_residency_20261014/)
contains plan/review, source-native adapter/build/client commands, package
versions, frozen references, complete arrivals/replies, standard traces,
catalogues, actual exits, analysis and host observations. Serving source
was frozen on main eb92fffe67daf588f711979e60cfe851b5a3e353 before full collection.

After reproducing the archived test-local setup/build paths, the recorded
full command is runtime/bin/python run.py full. Independent analysis needs
only the archive and standard Python:

    python3 bench/results/amk_residency_20261014/analysis.py \
        bench/results/amk_residency_20261014 full

Prioritize a model-independent driver experiment that avoids or changes
additional GPU residency while preserving upstream model computation.
Do not infer that newer Linux, model arithmetic tuning or arbitrary backend
porting solves this observed boundary. The generic text/backend/latency/SLO
objective remains active; this finite counterfactual is not full completion.


[The fresh independent result review](../../bench/results/amk_residency_20261014/result-review.md)
judges ordinary fixed-output-set counterfactual delivery valid, the sufficiency
component supported, the full overlap hypothesis inconclusive, value supporting
and impact a mechanism/workload boundary. It independently recomputes every
client metric/reference/lifecycle check, verifies103 unchanged upstream source
files and1536 normalized dispatch SASS lines identical across native/control/
loop, and retains the static/runtime control-register discrepancy. It does not
establish identical whole transport binaries or authenticated activity identity.

[Final restoration](../../bench/results/amk_residency_20261014/final_restoration.json)
removes only owned TEMP and7 named builds after review. Base package versions,
the default HF library inode/size, original Coder sessions/cache/Workspace and
unrelated WIP remain preserved. Full archived analysis after TEMP removal exits0
and replays byte-identically. No persistent resident-control feature or AMK
service is installed.
