# Same-compute batch-capacity comparison — complete

The complete traced collection,independent result review and owned cleanup
are finished. Read result-review.md and final_restoration.json for scope and
actual restoration. This does not select an ordinary runtime default.
[plan.md](plan.md) and [plan-review.md](plan-review.md) preserve the admitted
comparison and the two resolved execution followups. running_checkpoint.json
records the early setup observation. full.process.json identifies the completed
measurement process;all.exit.json covers the three preparation stages.
full.exit.json records measurement completion.

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

Use only original bpfusion-dev Workspace/main. The recorded owned test root was
/tmp/bpfusion-batch-capacity-tkii8tus and is now removed. all.process.json
identifies the original sequential setup->preflight->qualification wrapper;
full.process.json identifies the subsequently completed traced matrix.
Recorded paths can be rebound to a fresh owned directory for an intentional
later reproduction;do not resume the removed completed run.

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

## Complete qualification and full collection start

All6qualification commands pass at14:35:58.407703UTC. Four16-capacity protocol
executors complete5136 outcomes,including2060 intended rejections,and188800
independently replayed tokens. Both models and both paths actually exercise
widths1..16. Both copied protocol analyses and the real-preflight analysis
match saved stdout bytewise.

All four retained ordinary lifecycle cases also pass. Each loop has144actions/
78connections with16active requests,queued RST and64-connection active stop;
each native case has32actions,including a partial stop. Their exact complete/
prefix/cancellation scope remains in qualification_completion.json and raw folders.

The original preparation wrapper is terminal. After inspecting every outcome,
checking preserved original files,and confirming no remaining owned pins/module,
root starts exactly one full.py at14:38:25.993951UTC,PID611266,start50647799.
The prelaunch short GPU snapshot is14:38:02.651149UTC with no reported app;
the full host snapshot is during earlier lifecycle bootstrap. Neither establishes
continuous isolation. The full40-executor80-cell matrix is running.
No full performance result,ordinary default selection or overall goal completion
is claimed. Preserve the active owned runtime/build directory until work ends.

## Complete Qwen collection; Smol continues

The Qwen full driver and fixed analysis exit0 at15:00:58.704112UTC.
All20executors/40cells complete10240 measured attempts without failures,
655360 delivered measured tokens and160 checked gen1warmups. Its complete raw
histories,references and analysis are saved here. Running the copied analyze.py
against the copied raw files reproduces saved stdout bytewise.
This is one completed model within the still-running two-model experiment;
no complete-matrix performance interpretation or default selection follows.

The same full.py process611266/start50647799 has advanced to Smol.
host_full_qwen_short1_phase.json places the Qwen snapshot4.167s after its
preceding measured cell,not inside measurement. In contrast,the short Smol
snapshot15:01:55.107858..55.197721UTC falls inside pair0 kernel8's192/s
measured cell,with one reported GPU app in the owning Workspace cgroup.
Both are sparse observations,not continuous isolation or total CPU evidence.
Both-model completion,fresh result review,plots and owned cleanup remain open.


## Collection completion checkpoint before review

The original full.py ends15:22:39.023596UTC with both model driver/analysis
pairs exit0. All40executors/80cells complete20480 measured attempts,zero failures,
1310720 measured tokens plus320 checked gen1warmups. Five copied CPU analyses
reproduce saved stdout bytewise. All raw files,full terminal records,figure
PNG/PDF/data and post-full host snapshot are archived here.
Finding0064 documents the primary effects and adverse same-width comparisons.
At this checkpoint,independent result review and owned cleanup remained pending;
main application source/defaults were unchanged. Do not restart the completed full process.


## Independent review and final restoration

The single fresh result-review.md judges the complete traced run valid,both
primary capacity hypotheses supported,and research value supporting. It retains
native16 counterevidence,all timing/CPU/adverse TPOT rows and shared-host limits.
Root visually inspected the actual canonical PNG and corrected only annotation
placement;all plotted values remain unchanged. Existing measured packages were
unchanged when plot-only dependencies were installed after full terminal.

final_restoration.json records removal of the completed owned temporary tree,
after no remaining process,pin,module,cwd,mapping or open-file user was observed.
Original8file fingerprints,the two Coder session identities,base packages and
ordinary application source remain unchanged. Five copied CPU analyses reproduce
saved stdout bytewise after removal. Historical checkpoint sections above remain
historical;this final record is the current state. No default is selected and
the broader project goal remains active.
