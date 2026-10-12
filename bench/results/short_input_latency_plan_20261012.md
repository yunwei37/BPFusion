# Short-input first-token latency localization

User question: why do2/5/8-token inputs still take about3ms and what is the
bottleneck? Keep the retained serving/performance goal intact. This is a
dependency diagnosis for selecting the next same-compute serving experiment,
not a separate paper RQ, speedup result or completed-goal boundary.

Reuse before collecting: finding0029's completed cross-node matrix cannot
attribute its client TTFT. The archived older one-request Qwen CUPTI preflight
has808 model kernels,4.337094ms model span and4.531205ms client TTFT.
That is older source under profiling and cannot explain the current3ms
numerically. It does supply a concrete competing explanation to needless
receive draining: reused HF graph computation may dominate.

Use current published9954855 computation/native/module source with no
production change. Temporary adapters add only the already qualified
process-local CUPTI device-graph/HW tracing, installed torch.profiler export,
source graph node-type catalogue and two CPU monotonic clock anchors.
[Official profiler export](https://docs.pytorch.org/docs/2.14/profiler.html) and
[CUDA13 CUPTI activity](https://docs.nvidia.com/cupti/13.0.0/api/group__CUPTI__ACTIVITY__API.html)
are the reused tools. No arithmetic,precision,queue ABI,network setting or
driver/package change. No hardware-wide counter session or new client Job.

Two sequential model processes: SmolLM2-135M and Qwen2.5-0.5B,current cached
HF names and unchanged archived eager-HF cases. One persistent loopback
connection,gen1,one client; four declared warmups then16 measured requests
(four cases repeated4times,input lengths5/8/5/2). Native request/connect,
existing300s executor lifetime and60s shutdown/request handling. Actual
CUPTI capture contains all20 requests/model. No selected exclusion/retry.

After each actual reply,read the existing BPF map through libbpf and derive
layout via offsetof/sizeof from the canonical queue header. No duplicated ABI.
With only one client,maximum client_ns identifies the current slot; require
client_ns<=native start<=ingress_ns<=first arrival. Map reads are outside
request timing and their pacing/instrumentation remain a scope limitation.

Trace CPU user_annotation anchors bracket CLOCK_MONOTONIC and provide offset
bounds into the profiler's common CPU/GPU time axis. Verify begin/end anchor
consistency and request-to-activity attribution; report mapping uncertainty.
Exclude persistent dispatch kernels and setup. For each request,reconstruct
model-kernel count,span,interval union and gaps. Check complete activity
against actual captured kernel-node counts for bank/prompt length; never
interpret missing activity as zero compute.

Descriptive stages: client start→BPF ingress; ingress→first model kernel;
model kernel span; last model kernel→client first token. The last stage
includes GPU sampling/publication,kernel polling/TCP and client receive;
it is not a pure network measurement. This single-host clock path permits
same-domain differences. It does not assign the older cross-node3ms by
subtracting clocks or historical means. Profiler overhead prevents a new
unprofiled serving-speed/CPU/energy claim.

Decision: if current model spans dominate instrumented local TTFT,prioritize
qualified existing faster compute backends and same-backend comparisons;
do not attribute the floor to eBPF. If queue/post-model spans dominate,
investigate that concrete service mechanism instead. Mixed/missing coverage
keeps uncertainty visible; do not silently change math/oracle to pass.

Actual command:
HF_HOME=/workspaces/.cache/huggingface python3 /tmp/bpfusion-short-input-latency-uhkfzipi/diagnose.py
Ordinary raw JSONL and both gzip Chrome traces are
bench/results/short_input_latency*_20261012.*.
Record source/adapters,versions at observation time,counters,all request rows,
normal exits and cleanup. Stop only own model processes,detach own hooks/pins,
close own mapFD and retain original Workspace/WIP. No persistent helper.
