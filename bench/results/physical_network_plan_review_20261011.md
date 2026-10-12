# Cross-node plan review

Reviewer: retained /root/readiness_network_plan_review,fresh to this candidate
and plan; read-only. Reviewed main85da89f7b8cbfa3ed8f81be539218ba33c5707e9,
four tracked source diffs,plan,client/analysis adapters,build,binding
qualification and finding0028. No edits,builds,inference or clients created.

## Verdict: admit; no blocking defect remains

Proceed through declared default-loopback compatibility,real cross-node
preflight,frozen full matrix and fresh result review. No extra baseline or
workload is required for this scope.

Existing exact comparisons are loopback; their raw cannot establish
cross-machine delivery or interactions with framing/coalescing/request paths.
This adds that missing condition while preserving qualified computation.
Positive/negative/mixed/inconclusive results produce meaningful scoped decisions.
Supporting is the appropriate role; cross-node correctness alone is dependency
evidence. Full matched TTFT/TPS establishes only a network/workload boundary,
not SOTA or complete-goal acceptance. Efficient same-graph native networking
is the strongest currently runnable fair alternative; a different framework
introduces unqualified compute/API differences.

## Source binding and lookup

BF_BIND uses inet_pton and preserves loopback default. Kernel validates
AF_INET,TCP,LISTEN,local port,concrete address and netns before deriving
reply_addr. Linux copies sin_addr.s_addr to inet_rcv_saddr; established lookup
expects network-order peer/local addresses and peer port plus host-order local
hnum. Units remain correct. BPF records actual peer tuple. Listener/reference,
RCU lookup,send locks and final reclamation are unchanged.

[Binding source](https://github.com/torvalds/linux/blob/v7.3-rc3/net/ipv4/af_inet.c#L536),
[lookup source](https://github.com/torvalds/linux/blob/v7.3-rc3/net/ipv4/inet_hashtables.c#L530).

Wildcard listener is unsupported for kernel TX; the concrete PodIPv4 avoids
ambiguity. No VRF,bound-device or IPv6 coverage is claimed. Own-Pod-IP strict
receipts pass both kernel models and Qwen timed control,including exact tokens,
reuse,rejection,pipeline/half-close,tracing and cleanup. This is binding/lookup
compatibility,not cross-node delivery.

## Fairness and metrics

Both modes use identical HF FP16 computation,graphs,eight private KV banks,
dispatcher,protocol and workload. Dropping busy from full matrix avoids a weak
extra baseline. Client request()/connect() ASTs match native source.
Connections precede timing. Durations use a single client monotonic clock;
TPS uses first-send through last received token. TTFT/TPOT/TPS agree with
[NVIDIA conventions](https://docs.nvidia.com/nim/benchmarking/llm/metrics).
Token-ID scope excludes tokenizer/detokenizer.

Five paired blocks,alternating modes and rotated cells suffice for declared
nominal per-model intervals,not familywide superiority/equivalence/robustness.
Matrix counts reconstruct80cells,5120 measuredrequests,166400tokens,
20 normalexecutors,with eight separate warmups/executor.

## Resolved analysis clarification

The initial question was that older native --analyze unconditionally requires
server CPU fields. Root clarified the plan and supplied
physical_network_analysis_20261011.py. Its explicit command recomputes client
timing/TPS/paired intervals without filling unavailable CPU with zero.
It validates tokens,counts,indices,prompt distribution and arrival metrics.
Descriptive quantiles use nearest rank; older native analyzer interpolates,
so comparisons must label this distinction.

The two adapters are necessary ordinary reproducibility code,not a new
experiment-control framework. Executor/module builds pass. Code growth and
source scope are justified by the missing endpoint and remote timing path.

## Evidence required during execution

Preflight must prove client/server placement,TCP tuples and traversed interfaces.
Preserve literal invocations and frozen adapter metadata for reproducibility.
Label actual overlay/Tailscale routes; cross-node does not establish bare-NIC
TCP,GPUDirect or historical causal improvement. Retain shared-device/network
exposure,all pairs and failed prefixes. Remove preflight capture before full
timing. No remaining scientific or executability defect blocks the plan.
