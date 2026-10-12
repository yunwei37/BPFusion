# Cross-node TCP/HTTP comparison with unchanged model graphs

## Selected question and admission

Retained user question: "性能能不能想办法改进一下. 尤其是 tp / lantency,
理论上应该可以做到很快, 你想想, 往这个目标继续做".
No formal paper RQ or central thesis exists in this repository; this plan
does not invent or narrow one. Specific uncertainty: does the worker-free
kernel/eBPF request path improve client TTFT or throughput over efficient
native userspace networking when the client actually runs on another machine,
with identical qualified GPU computation?

Role: supporting. Largest credible story: normal cross-machine Linux TCP/HTTP
can serve reused resident models without a steady userspace request worker,
with a matched client-performance boundary. It is not external SOTA or
complete-goal acceptance. Strongest reject argument: all current exact
comparisons are loopback; queue/copy/TX effects and network delivery may differ.
Prior loopback raw cannot answer another physical path by reanalysis.

Finding0028's efficient-control CPU/TTFT/TPS result remains inconclusive and
closed. Current expectation is no established speed advantage; actual
cross-node framing/coalescing/load may change the result. A reliable positive
effect supports only that metric/model/network condition; a negative effect
bounds that condition and changes the next request-path decision. Mixed or
inconclusive data retain that outcome and close the matrix without unchanged
retries. If the path fails correctness,the failure is not a performance win.

Best alternatives: another small loopback polling tweak would be redundant
without a new causal discriminator. A strong official serving comparison
remains necessary for broader claims,but matching its compute/API is not yet
qualified. This comparison adds the missing cross-node path while holding
qualified computation fixed; it does not substitute for that later baseline.

## Reused systems and necessary glue

Primary precedent:
[Blink sections4 and6](https://arxiv.org/html/2604.07609v1) separates device
computation reuse and serving orchestration.
[GPU-centric networking,EdgeSys2024](https://girondi.net/pub/gpunetworking24-cc.pdf)
reuses compiled model graphs and measures network inference.
TTFT/TPOT follow [NVIDIA client latency conventions](https://docs.nvidia.com/nim/benchmarking/llm/metrics).

Reuse original bpfusion-dev Workspace,RTX5090,HF FP16 capture source,
device dispatcher,eight independent graph/KV banks,TCP framing,native request()
and connect(),and independent references already archived by finding0028.
No new model arithmetic,precision,sampling,speculation,batching policy or
request correctness oracle.

Necessary address adapter: graph executors reuse existing BF_BIND with
loopback default. Kernel TX derives its local lookup address from the actual
IPv4 listener; a concrete bound address is required. Without a listener,
the legacy reply_addr fallback remains. The strict suite/native benchmark
use the same BF_BIND endpoint. Four-source diff is24 inserted/12 deleted
lines,including test/measurement destination substitutions. Build passes.

Cross-node client adapter is
bench/results/physical_network_client_20261011.py. request()/connect() are
copied verbatim from current source; the client loop retains native
connections-before-timing,barriers,index/prompt distribution and first-send/
last-token TPS. It omits local-server CPU readings because the server is on
another machine. It has no new CLI parser,input schema,controller or promotion
format. The invocation appends ordinary Python literals for existing cases,
cell parameters and run metadata. It runs real requests,not simulated models.

## Comparison and workload

Proposed: ./build/qwen_graph with eBPF stream admission/kernel TCP TX.
Main alternative mechanism: ./build/qwen_graph_user_network_wait with native
epoll_pwait2 60000ns and the same resident GPU dispatcher/model graphs.
Competing position: an efficient userspace network worker is already sufficient;
removing it need not improve client performance. A matched numerical run is
needed; unrelated published RDMA/SmartNIC or generic framework results do not
settle this TCP/compute pair. If it matches/wins,no superiority follows.
Busy epoll is already covered and is not rerun as another weak main baseline.

Models: SmolLM2-135M and Qwen2.5-0.5B-Instruct. Same four archived independent
eager-HF prompt/reference pairs,gen1/64,clients1/8,64 requests/cell.
Five paired process blocks/model; R,W for even pairs and W,R for odd pairs.
Rotate the four-cell order by pair. Reuse one remote client Pod throughout
preflight/full. Eight warmups/executor are separate.
Matrix: two models x5pairs x2modes x4cells =80cells,5120 measuredrequests,
166400 exacttokens,20 normalexecutors. Each executor publishes264requests
and8580 modelgraphsteps,banks8,maxactive8. Correctness remains token-exact.

Primary effects per model: W-R mean client TTFT at gen1/c1; R-W output
tokens/s at gen64/c8. Five process-block differences,nominal two-sided
t95,df4. Report both separately,no familywide superiority/equivalence
claim. Other TTFT/TPOT/completion quantiles and cells are descriptive.
No bounded or total service-CPU claim is tested by this matrix.
No cross-machine clock subtraction: each client duration uses its own
monotonic clock. Tokens completed in one recv share arrival timestamp.
Network/Tailscale/overlay jitter,client node capacity and shared GPU activity
are possible competing explanations; retain observations and all pairs.

## Execution and lifecycle

The original server Pod is coder-eb48d962-76f4-4ff7-bac5-7bc62ec2ada3-5c8bb655f6-khnns
on lab,IP10.42.1.238 at preparation. Discover/revalidate it through the
owning kubectl-home.ps1 path before test; do not change routes or addresses.
Each server command uses BF_BIND=<actual PodIPv4> HF_HOME=/workspaces/.cache/huggingface
<executor> <existing model argument> 300. Preserve original source/WIP/session.

One disposable benchmark-only Job,namespace coder,image
python:3.12.12-slim-bookworm,provides the external stdlib client.
Official registry manifest is HTTP200 and declares amd64/arm64.
Required affinity to the existing control-plane node group makes this client
non-Spark and physically separate from the lab server; it is not pinned to
one hostname. Retain actual scheduler placement and imageID. No resources,
limits,helper daemon,Service,permission,credential or persistent configuration.
Its command waits for test execs; delete the Job/Pod when benchmark ends.
This is a bounded test-local client under spark-manage§8,not another
development Workspace or a replacement writer. Source editing/builds stay
inside the original matching Workspace.

Use scripts/kubectl-home.ps1 exec -i -n coder <clientPod> -- python3 -
with the frozen native client source plus literal case/cell invocation.
Save actual stdout/exit and append native JSON request/cell rows in the
original Workspace. Ordinary outer orchestration launches/stops only own
executor; no project-authored control protocol or persistent runner is added.

Dependency qualification already ran in the original Workspace against its
own PodIP: both kernel models and Qwen timed control complete strict gen64
prefill-edge tests. This tests binding/lookup only,NOT physical-NIC delivery.
Add one default-loopback native three-mode Qwen preflight for compatibility;
its busy row is dependency-only,not a full-matrix main baseline.

Real cross-node preflight: both models and both modes,8warmups then4 measured
gen1/c1 requests/condition. Four normalexecutors,16 exact measuredtokens.
Verify actual remote source/destination addresses,normal replies,one GPU
hostlaunch,264modelgraphsteps,banks8,zeroerrors,and kernel absence in control.
Capture preflight TCP tuples with existing host tcpdump,actual client/server
nodes,routes,overlay/interface and physical-link observations. Cross-node
overlay/Tailscale is not direct bare-NIC TCP or GPUDirect; label it accurately.
No profiler/capture is retained in the full timing window.

Freeze and publish source/plan after qualification and review and before
full collection. Archive preflight/full source revision,commands,all raw
rows,executor logs/environment and cleanup. Full collection runs every
planned cell to terminal status; leave failures and incomplete prefixes visible.
A read timeout does not imply stopped work: inspect the same process/Pod.
Use the original lifecycle to stop only own executor and detach own hooks/pins.

Full raw paths:
bench/results/physical_network_smol_20261011.jsonl,
bench/results/physical_network_qwen_20261011.jsonl;
stdout/environment are retained beside them. Exact analysis command:
python3 bench/results/physical_network_analysis_20261011.py <raw.jsonl>.
This direct adaptation of native metric formulas recomputes only client
timing/TPS and exact completeness; it neither requires missing server CPU
fields nor replaces them with zero. resident_dispatch.py --analyze is not
used for cross-node raw. Both .py adapters are ordinary reproducibility
artifacts,not a new experiment-control interface.
Fresh result reviewer recomputes counts,tokens,timing,TPS and intervals,
audits all20 executor engagements,actual cross-node path and limitations.
Target table: per-model primary TTFT/TPS means,differences and nominal t95,
plus explicit network path. Expected bootstrap cost~20minutes; actual
cross-network request duration is unknown until real preflight.

If unanticipated deployment/network conditions make this exact comparison
unexecutable,repair only ordinary test-local glue or return that boundary.
Do not change the oracle or silently present local fallback as remote success.
Remaining full goal includes strong official serving,total CPU attribution,
full text/API,broader model/backend qualification and online batching.

## Test-local resource contract

Exact temporary mutation is archived in physical_network_client_job_20261011.json.
One client Job for this preflight and full matrix only; it runs no model,
does not mount project PVCs,weights or Git/AI credentials,and does not
replace a Workspace; ordinary cluster defaults apply.
Root owns cleanup on normal or failed termination:
powershell -ExecutionPolicy Bypass -File scripts/kubectl-home.ps1 delete job
-n coder bpfusion-cross-node-client-20261011 --wait=true.
No server service is paused,replaced or reconfigured. Restore requires own
executor/module/hooks/pins and client Job/Pod absent,original Pod ready and
unrelated tools/setup_env.sh preserved. Existing300-second executor lifetime
and native60-second request waits bound each run; the Job is removed at the
collection boundary rather than retained for later reuse.
Descriptive quantiles use nearest rank and are not numerically interchangeable
with older native interpolated quantiles. Primary means/TPS/t95 are unchanged.
