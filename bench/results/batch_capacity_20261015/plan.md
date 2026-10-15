# Same-compute admission/batch capacity experiment

Prepared2026-10-15 from mainfa84cd2289cc904fe446ae066e5ac26334cf2cb2.
Private sources are unbuilt/unexecuted. Production source/default is unchanged.

## Retained question and admission

There is no formal paper RQ/thesis/idea-story contract. Retain the user's complete
Linux TCP/HTTP + eBPF/shared queue -> reused resident real-model GPU -> kernel
TCP reply objective,without a steady userspace request worker,and improve
latency/throughput. This supporting experiment tests whether the current
eight-model-slot service constructor limits useful batching and delivery.

0063's fair-native comparison has no reliable96/s P99/throughput advantage.
Reanalysis of its complete saved histories shows Qwen kernel96/s decode
batch7.5865 mean across blocks,8759/10630 decode rounds at width8; native
7.6493,8838/10544. Both constructors have real pending queues. These are logical
round counts,not time occupancy or proof of a bottleneck. Smol is less full.
The fixed8-slot header independently constrains reusable model capture/KV banks,
and the existing upstream adapter already discovers bank count from the native
library. No earlier comparison changes this shared capacity with fair native
admission. Raw histories cannot supply the missing intervention.

Hypothesis: doubling this constructor to16 slots improves finite high-offered-load
kernel delivery throughput while retaining exact trajectory-matched fidelity.
Largest credible story: a reusable service batching/capacity boundary can improve
the no-userspace-worker server without model arithmetic optimization.
It cannot establish eBPF-specific gain,optimal bank count or peak capacity.

A positive result changes capacity selection for this bounded constructor,
subject to actual compatibility/adoption evidence. Native16 is the strongest
competing alternative; native8 is a capacity ablation. If both improve,credit
shared compute/batching capacity rather than syscall removal. Mixed/adverse/
inconclusive results retain the original default and bound this intervention.
An avoidable baseline/interface/oracle failure is not a kernel victory.

Best alternative is more detailed GPU/CPU timing after0057's incomplete CUPTI
decomposition. Existing8-width saturation plus source-visible capacity gives a
more direct current intervention before adding uncertain clock correlation.
This is one16-vs8 intervention,not an unchanged retry or model/parameter sweep.

## Implementation and comparator

Private candidate8 and candidate16 both reuse0063's qualified eligible-frame FIFO
native header,unchanged loop/kernel/GPU controller and unchanged vllm_graph.cu.
Only semantic compute/transport input difference is BF_LLM_SLOTS8->16 in the
canonical private header. Makefiles only bind source/build paths. Actual graphs
are width-specific upstream FP16 operators; weights,precision,prompts,packing,
prefix release and arithmetic implementation stay fixed. Realized graph width,
KV allocation,metadata,ABI size/resources and admission can differ: this is a
constructor capacity intervention,not identical kernel-sequence execution.

The existing32-bit reservation bitmap can represent16 slots. All producer,
loader,model and transport builds must use the matching private header.
The module/HF/legacy paths are not changed or newly qualified; no candidate
page may be passed to an old module. Only stock BPF-loop/native variants run.
No public mode,permanent setting,resource/CPU placement or host policy is added.

Four conditions: kernel8,current-capacity component control; native8,matched
capacity ablation; kernel16,candidate; native16,the single main competing
mechanism. Native FIFO applies to complete eligible frames; one active response
per connection remains,while kernel can pipeline. Native buffers and finite4096
kernel queue differ. Performance traffic has one request/connection.
No stale FD-priority competitor is rerun.

## Workload, primary and interpretation

Use the same two cached revisions:
Qwen2.5-0.5B-Instruct7ae557604adf67be50417f59c2c2f167def9a775 and
SmolLM2-135M93efa2f097d58c2a74874c7e644dbc9b0cee75a2.
Four short tokenized prompts,gen64,rates96 and192/s,256 independent scheduled
attempts/cell,five process blocks/model. Four-condition order uses a Williams sequence: modes[(j+pair)%4] for
j=(0,1,3,2). First4blocks place every condition in every position once; the
fifth repeatsblock0. Two-rate order rotates. Within a block all conditions use
identical normalized cumulative gamma(shape1) schedules,seed20261015+pair.
One original Workspace/GPU experiment runs sequentially; no foreign workload
is paused or reconfigured. Actual Python scheduling lag stays in results.

Primary per model: kernel16-minus-kernel8 delivered output token/s at192/s.
Use five paired nominal t95df4 intervals. Positive throughput support requires
interval>0 and no failed attempt in either primary condition; failures censor
complete-delivery superiority. Intervals crossing0 are inconclusive,not equivalence.
At96/s TTFT P50/P95/P99,completion/scheduled-origin tails,TPOT,failures and
executor CPU remain prespecified secondary. Both native-capacity and same-width
transport contrasts remain visible. A throughput benefit alone does not establish
latency improvement or promotion over efficient native16.

Source-native standard throughput/TTFT definitions and arrival precedent:
https://docs.vllm.ai/en/stable/cli/bench/serve/
https://raw.githubusercontent.com/vllm-project/vllm/v0.31.0/vllm/benchmarks/serve.py
This token-ID adapter is not an official text/JSON endpoint benchmark.
Finite delivered-window TPS is not saturation capacity.256 attempts/cell cannot
support precise P99/P99.9/production-SLO guarantees. Partial executor CPU excludes
client/RX/softirq/someio-wq and energy.

Full:40 executors,80cells,20480 measured attempts,1310720 requested measured
tokens,plus320 checked gen1 warmups. Keep all adverse,outlier,failed and
inconclusive cells. No favorable replacement,oracle/timeout/metric relaxation or
new precision mode. BF_TRACE is common to all four conditions; do not transfer
a positive result to ordinary untraced serving without actual evidence.

## Correctness and executable stages

Run /usr/bin/python3 -u run.py in this owned test directory. It sequences setup,
real preflight and qualification. Inspect the recorded ordinary lifecycle
findings,diagnose any actual transport/resource fault,and then run
/usr/bin/python3 -u full.py for the admitted traced matrix. A finite ordinary
reference-pool miss alone does not invalidate traced numerical replay. Never
start overlapping GPU copies. All app source,
builds and tests remain in original bpfusion-dev Workspace/main.

setup.py uses pinned vLLM0.31/Torch2.13cu129/Transformers5.17/NumPy2.3.5 and
libbpf1.6.3 as0063,one owned runtime and separate build8/build16 normal Makefile
outputs with private header precedence. Preserve original8setup/build files,
unownedtools/setup_env.sh,Coder processes,base packages,weights and sessions.

Real preflight attempt1: Qwen,all four conditions,rates96/256,32attempts/cell,
256 measured requests16384tokens plus32 warmups. Both widths must execute
their intended banks and independently replay; configured width is not proof
of actual width16. Record actual batches and queue/slot/ring state. At most
three attempts; preserve failure receipts and any repair before full collection.

Qualification runs only changed16-capacity protocol/lifecycle cases for both
models/paths; unchanged8-capacity full correctness remains0063's evidence with
fresh source/build binding checks. The fixed protocol driver expands concurrency
1..16,wrap/reject and mixed lanes to16; unchanged fragmented prompts,pipeline/
half-close,reuse,5000empty connections and helper-stop checks remain.
Each1284-outcome protocol executor includes515 intended rejections and47200
replayed tokens; four total5136outcomes/188800tokens. Require actual width16.
Physical-bank ownership/release checks use the declared native width rather
than hardcoded8; numeric ordering checks handle two-digit slot indices.
Independent upstream graph/head replay and exact client/reference tokens remain
the oracle,not a candidate-derived expected-output pool.

Retained ordinary lifecycle native remains32 actions/model. Loop expands the
queued-reset burst24->48 frames so it still exceeds twice the new capacity;
64-stop-clients remain. Total144loop actions,78connections; observed complete/
partial wire bytes retain the frozen complete-output/prefix pool. Canceled
unobserved frames are explicitly not complete numerical checks. Stop page
head+queued accounting changes120->144. The fixed128-entry reply diagnostic
uses trace_overflow=max(0,head-128),not a numerical-history loss exemption.
Broad arbitrary-overload/native queued-stop coverage is not claimed.
Ordinary lifecycle findings are recorded separately from traced-performance
qualification. If the finite frozen pool cannot qualify a new16-wide ordinary
output,retain the failure/ambiguity and withhold ordinary-default adoption;
do not expand the pool after observation. This alone does not invalidate
separately replayed BF_TRACE results. A genuine transport/resource corruption
requires diagnosis,not automatic classification as an oracle-coverage issue.
The wrapper requires both traced protocol analyses before full; it records all
four ordinary lifecycle outcomes without making finite-pool membership a
scope-mismatched throughput-validity gate. Leaked serving resources prevent
starting another executor until the real fault is repaired through its owner.
Any nonzero ordinary lifecycle subprocess exit also returns for diagnosis;
a handled exit0/passfalse outcome remains recorded for root interpretation.

full.py runs both full model drivers and fixed analyze.py. Every executor,
cell,driver,reference replay and analysis must reach terminal. Record actual
1..16/1..8 batches,all per-condition queue engagement and final native deque/
kernel reservations/SQ/CQ drain. Model-generation replay owns its previous
replayed outputs and actual KV/slot history; no admitted response is unchecked.

## Review, artifacts and restoration

One fresh plan review before execution,and one different fresh result reviewer
after full terminal. Review baseline fairness,actual16-width engagement,header/
ABI/binary bindings,oracle independence,all failures/metrics/uncertainty and
ordinary lifecycle scope. Research-experiment-design owns the protocol; this
plan does not create another authority or scheduler.

Keep this plan,one plan-review.md,raw outputs,diffs,commands,pinned versions,
one result-review.md and a complete table/figure. Preserve host phase/boot/GPU
ownership and ambient CPU observations; sparse samples are not continuous
isolation. Runtime/build/dependency trees stay out of Git.

After needed work and no active users,remove only owned temporary resources,
replay copied CPU analyses without temporary paths,verify original state,update
OSS evidence docs and main commit/push. No production default selection is
implied by a private run. The broader performance/serving objective stays active.
