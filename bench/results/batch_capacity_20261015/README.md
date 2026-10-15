# Same-compute batch-capacity comparison — running

This is an uncompleted experiment checkpoint,not a performance result.
[plan.md](plan.md) and [plan-review.md](plan-review.md) preserve the admitted
comparison and the two resolved execution followups. running_checkpoint.json
identifies the actual existing process and observed setup state.

## Question and planned comparison

Complete0063 saved-data reanalysis (prior_batch_analysis.py/json) finds Qwen96/s
kernel8759/10630 decode rounds at width8,and mean block batch7.5865; native
8838/10544,mean7.6493. These are logical counts,not time occupancy or proof of
a bottleneck. This motivates a direct8-vs16 capacity intervention.

candidate8/candidate16 are source snapshots,not checkouts. Both use0063's
qualified eligible-frame FIFO native admission and unchanged optimized model/
transport source. capacity.diff changes only BF_LLM_SLOTS8->16; Makefile
path bindings match each private build. Upstream graphs and KV/bank setup
discover the native bank count. Width/resource/ABI/workload grouping can differ;
this is not identical kernel-sequence execution or intrinsic eBPF attribution.

Four matched conditions are kernel8,native8,kernel16,native16.
Native16 is the single main competitor;8-width conditions are capacity
controls. Both models,gen64,rates96/192,256 attempts/cell,five process blocks
fix40executors/80cells/20480 measured attempts/1310720 requested tokens,
plus320 gen1warmups. Primary per-model is kernel16-minus-kernel8 delivered
token/s at192/s,nominal paired t95df4.96/s tails and same-width transport/
native-capacity contrasts remain secondary; failures censor superiority.

## Actual workflow and scope

Use only original bpfusion-dev Workspace/main. The existing owned test root is
/tmp/bpfusion-batch-capacity-tkii8tus;all.process.json identifies its only
sequential setup->preflight->qualification wrapper. Do not start another copy.
After root interprets actual ordinary lifecycle outcomes,full.py runs the
admitted traced matrix. Recorded paths can be rebound to a fresh owned directory
for an intentional later reproduction after this run reaches terminal.

Normal Makefile rules build each matching header,loader,BPF and GPU/native
variant in build8/build16. Pinned runtime matches0063; exact installed package
comparison remains required. No production source/default,model arithmetic,
precision,CPU placement,host policy or other Workspace is changed.

16-capacity protocol exercises1..16concurrent clients,reuse,fragmentation,
pipeline/half-close,rejection,wrap and helper stop with independent upstream
history replay. Retained ordinary lifecycle outputs use a finite historical
reference pool: an outside-pool response remains unqualified/ambiguous and
blocks ordinary adoption,but does not by itself invalidate independently
replayed traced performance. Unexpected driver exit or actual transport/
resource corruption returns for diagnosis; it is not automatically an oracle
ambiguity. Read the exact reviewed plan for counts and limits.

No new result,default adoption,preciseP99.9,steady-state capacity,totalCPU/energy,
continuous isolation or general model/backend support follows from setup.
The full user serving/performance objective remains active.

## Setup completion update

Both capacity builds exit0 at13:58:58.736238UTC;setup terminal is
13:58:59.851179UTC. Actual compiler logs bind each private header/source to
its matching BPF,loader and CUDA variants. Installed measurement package
versions match0063 exactly (package_comparison.json is empty).
The same wrapper has entered the real Qwen preflight.16-capacity real-model
qualification,complete performance collection and result review remain open.

## Real preflight completion update

The one Qwen real preflight completes all four conditions and8cells:
256 measured requests,zero failures,16384 checked measured tokens plus32
gen1warmups. Both16-capacity paths actually execute every batch width1..16;
both8-capacity controls execute1..8. The copied fixed CPU analysis exits0
and matches saved stdout bytewise. preflight_completion.json retains actual
queue peaks,terminal and coverage. This is setup/correctness evidence only.
The same original wrapper now continues the16-capacity protocol/lifecycle
qualification. Full performance collection and independent result review
remain unfinished; no ordinary default is selected.

## Qwen protocol qualification update

Both16-capacity Qwen protocol executors and the fixed analysis exit0 at
14:14:00.186222UTC. Together they complete2568 outcomes,including1030 intended
rejections,and94400 independently replayed output tokens. Both actually execute
batch widths1..16. Wire/history ownership,recycling,network syscall checks and
normal helper-stop cleanup pass. Copied protocol analysis matches stdout
bytewise (qwen_protocol_completion.json). These are not2568 successful
inference responses. Ordinary lifecycle and Smol qualification remain running;
full performance collection has not started.

## Qwen loop lifecycle update

Ordinary16-capacity kernel-loop lifecycle exits0/pass true at14:18:02.471368UTC:
144actions,78accepted/closed connections,max16active requests,zero graph error,
zero pending/error/reserved/drop/overflow,and drained SQ/CQ. Final admission
head96 plus48queued cancellations accounts for144 actions. All owned pins are
removed. Complete/prefix bytes use the unchanged pre-observation frozen pools;
unobserved canceled frames are not complete numerical responses.
qwen_loop_lifecycle_completion.json and lifecycle_qwen_loop/ retain exact scope.
Native lifecycle and both Smol qualifications remain unfinished.

## Complete Qwen16 qualification update

All three Qwen qualification commands pass by14:21:47.817205UTC:
the two-path1284-outcome protocol per path,ordinary kernel-loop lifecycle,
and ordinary native lifecycle. Native retains32actions with13connections,
32published/31completed/10rejected and no graph error or remaining pins.
Partial stop observations are not32complete numerical replies.
qwen_qualification_completion.json links the completed scope.
The same original wrapper has advanced to Smol16 qualification. Full
throughput/tail collection remains unstarted and no performance benefit
or production default selection is inferred.
