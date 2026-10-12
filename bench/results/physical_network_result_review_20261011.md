# Cross-node result review

Independent reviewer: /root/cross_node_result_review. Reviewed 2026-10-12
17:44 UTC in the original yunwei356/bpfusion-dev Workspace. The reviewer
did not plan, implement, or collect this run and received no desired verdict.
Only this report was written; application source and other documents were
not changed and no commit was made.

## Separate judgments

- Run status: valid and complete for the approved same-compute cross-node matrix.
- Tested hypothesis: inconclusive. Neither primary client TTFT nor primary
  throughput establishes a resident-path advantage for either model.
- Research value: supporting.
- Paper impact: additional evidence defining the current mechanism/workload
  boundary, not a direct challenge to an established paper thesis.
- Next paper decision: close this complete matrix, preserve its inconclusive
  results, and retain cross-node delivery as demonstrated functionality.
  Do not advertise a latency/throughput win or repeat the unchanged matrix
  to search for significance. Further performance work needs a new causal
  discriminator under the retained user question.

The selected question remains the user's request to improve throughput and
latency. There is no formal paper RQ or central thesis in the repository.
This review neither creates one nor treats this supporting comparison as
completion of the whole project.

## Evidence and completion

Read the approved physical_network_plan_20261011.md, its plan review,
physical_network_client_20261011.py, physical_network_analysis_20261011.py,
both full model JSONL files, full invocations, full analysis stdout,
preflight path/environment evidence, full environment/journal, Makefile,
executor/qwen_graph.cu, executor/qwen_graph.py, executor/userspace_tcp.h,
relevant module code, the native benchmark, and the eager-HF oracle source.

Current main remained eaa9c8e6bd5f79d35c0a260770833c7071302380 during review,
matching both full metadata records. Both full raw files contain exactly:
one metadata row, ten launch rows, ten bootstraps, ten warmups, ten executor
records, forty cells, and 2,560 measured requests. Across models that is
80 cells, 5,120 measured requests, 166,400 measured tokens, and 20 normal
executors. Eight warmup requests per executor are additional and do not
enter measured results.

Independent checks established one unique cell for each model/pair/mode/
generation/concurrency combination, all indices 0..63 once per cell,
index-mod-four case assignment, sixteen appearances of each prompt per
cell, no failure row, and no excluded process block. Actual launch order is
R,W for even pairs and W,R for odd pairs. Actual cell order rotates the
four planned conditions by pair in both modes. All twenty warmup records
contain eight requests. There is no selected retry in these full files or
their invocation sequence.

Smol's first-to-last recorded executor completions are
2026-10-12T17:09:18.264029Z through 17:26:18.419748Z; Qwen's are
17:27:40.371477Z through 17:40:08.168572Z. Bootstrap capture is recorded
separately and excluded from client measurements. The invocations preserve
the literal model/case/cell parameters and server wrappers, including actual
BF_BIND=10.42.1.238, existing HF cache, and native 300-second lifetime.
The source-native request/connect functions plus the literal footer form
the client invocation; the approved owning kubectl exec path runs it in
the remote client Pod.

No material change to oracle, timeout, cell matrix, metric definition,
or repetition order was found. The remote client adapter and direct
client-only analyzer were declared in the approved plan. Omitting server
CPU fields is an explicit scope boundary, not a silent zero substitution.

## Correctness and mechanism engagement

The four prompt/reference pairs in each full metadata record exactly match
the previously archived readiness experiment's eager-HF references.
The source of those references, tests/resident_qwen.py:oracle_cases, loads
the original model in FP16 eager mode and generates greedy tokens independently
of the captured resident graph dispatcher. The oracle is not derived from
the proposed path's output. Every measured request has the expected token
sequence of length one or sixty-four. The request function also asserts
HTTP 200, advertised byte length, complete reply bytes, and exact tokens.
Warmups assert the same correctness internally before emitting their
success record, although their individual token arrays are not archived.

Both models and all modes report exactly one host graph launch, 8,580
device model-graph launches, graph_error=0, banks=8, and max_active=8.
This agrees with 256 measured plus eight warmup requests, and 8,320
measured plus 260 warmup tokens per executor.

Every resident wrapper records eBPF stream parser/verdict and sockops
attachment, successful normal executor exit, and detach. Its queue receipt
reports 264 stream publications, no sockhash failure, reservation mask zero,
and all eight slots FREE. The retained full journal separately contains
ten resident lifecycles, each with 55,176 transmitted bytes, 264 completions,
zero abandoned requests/retries, and nineteen accepted/closed sockets.
These receipts establish actual TCP replies and reclamation, beyond module
loading or GPU activity.

The userspace baseline engages its intended mechanism in all ten conditions:
native nonblocking TCP/epoll networking, epoll_pwait2 timeout_ns=60000,
nineteen accepted connections, 264 published and completed requests, zero
rejected requests, and normal exit. The recorded wrapper asserts module
absence before and after control execution. There is no failed or disabled
baseline being counted as a proposed-method win.

Source inspection agrees with the earlier strict after-ready tracing:
resident userspace serves initialization and shutdown and sleeps in steady
state; it does not accept, receive, send, or launch one host operation per
request. Kernel TCP work and CPU use nevertheless remain. No new per-cell
syscall trace was collected in the full timing window, as planned.

## Comparison fairness and network scope

Both executors share qwen_graph.py's HF FP16 eager captured computation,
same GPU dispatch function, eight private input/KV/graph banks, greedy
selection, prompt set, token protocol, request count, concurrency, generation
length, listener setup, client TCP_NODELAY, and default server TCP buffering.
Makefile compiles the same native source with only the network-control
macros changed. The source does contain previously qualified capture/math
adaptations, but these are identical across compared modes.

The principal baseline is a credible alternative mechanism: an efficient
userspace network worker while keeping the same resident computation.
It is appropriate for isolating orchestration and networking. It is not an
official general-purpose serving system, and matching/beating it cannot
establish SOTA. Both sides retain their actual readiness and completion
polling policies: kernel usleep_range(60,120) versus control's nominal 60-us
epoll wait. The run tests these complete implementations; it does not
identify one elementary eBPF or poll-delay effect.

Client metadata identifies Raspberry Pi Pod 10.42.0.118 and server lab Pod
10.42.1.238. Preflight packet records verify their bidirectional TCP tuples
through flannel.1/cni0/veth. Physical-carrier observations identify
enp129s0 and the Tailscale peer endpoint. These are different machines
over an existing overlay/Tailscale/Ethernet path. This is not bare-NIC
TCP, GPUDirect, RDMA, or network-stack bypass. The multi-interface inner
capture duplicates forwarding observations, and broad encrypted peer
traffic cannot be attributed entirely to benchmark bytes. Capture was
preflight evidence rather than a retained full-window profiler.

The completed full measurements add numerical cross-node evidence that
the older loopback raw cannot provide. They do not identify a causal
before/after benefit of the binding patch or prior readiness guards.

## Independent metric reconstruction

The client request() and connect() ASTs exactly match the native benchmark.
Connection establishment is before timing. Start precedes sendall, and
each received group uses one client monotonic timestamp. There is no
cross-machine clock subtraction. Tokens received together share a
timestamp; reported TPOT is a client-observed average interval, not
per-token GPU compute time.

Independently recomputed each request's TTFT as (first arrival-start)/1e6,
completion as (last arrival-start)/1e6, and TPOT as
(last-first)/(generation-1)/1e6, or absent for one token. All stored
request metrics and monotonic arrival orders reconstruct exactly.
Independently reconstructed each cell's output-token throughput as
64*generation/((last token arrival-first request start)/1e9); all match.
This denominator includes actual client pacing and serving/network
delivery, but excludes connection setup, bootstrap, and warmup.

For all four cell conditions and both models, independently rebuilt
per-process-block means, all five paired differences, their means and
nominal t95 intervals using t(df=4)=2.7764451051977987 and sample standard
deviation/sqrt(5). Reconstructed every pooled nearest-rank p50/p95/p99
and mean in the archived analysis as well. Both existing analyzer
commands exit zero, and current combined stdout exactly matches the
archived full analysis after stripping its final whitespace. No material
numeric discrepancy was found.

## Planned primary results

R denotes resident kernel/eBPF networking; W denotes timed userspace
networking. TTFT differences are W-R, so positive favors R. Throughput
differences are R-W, so positive favors R. Values below are unrounded
in the linked raw/analysis; this table rounds to six decimals.

| Model / primary condition | R mean | W mean | Paired difference | Nominal paired t95 |
|---|---:|---:|---:|---|
| Smol gen1/c1 TTFT, ms | 3.804418 | 3.590233 | -0.214185 | [-0.526943, 0.098572] |
| Qwen gen1/c1 TTFT, ms | 3.189486 | 3.034464 | -0.155022 | [-0.564566, 0.254522] |
| Smol gen64/c8 output tokens/s | 1825.315649 | 1843.902505 | -18.586856 | [-70.530540, 33.356828] |
| Qwen gen64/c8 output tokens/s | 1420.733955 | 1418.596725 | +2.137230 | [-4.588850, 8.863310] |

Every primary interval contains zero. Both TTFT point estimates favor W;
Smol throughput favors W and Qwen throughput favors R. None demonstrates
a stable advantage or regression, and lack of significance does not prove
equivalence. All sixteen TTFT/TPS intervals across the four conditions
and two models also contain zero. Descriptive quantiles cannot override
these predeclared primary results or become a selected tail-latency claim.

Process blocks are the uncertainty unit, not the 320 individual request
samples per pooled condition. Five blocks provide limited precision.
Intervals are nominal per metric/model, with no multiple-comparison
adjustment, equivalence margin, network-day generalization, or tail
confidence interval. For example, Smol gen64/c8's fourth-pair difference
is -93.256038 tokens/s and materially widens its interval. That pair
remains included; its cause was not measured and is not assigned to a
specific subsystem.

## Limits, restoration and research decision

The reused eager-HF oracle and token-ID HTTP interface establish exact
generation for these four short prompts and fixed generation lengths.
They do not evaluate task quality, tokenizer/detokenizer cost, full text
or OpenAI API service compatibility, long context, streaming SSE,
continuous batching, overload behavior, or arbitrary model support.
The eight graph banks represent matched concurrent independent requests,
not a qualified online batching policy. Bootstrap costs are outside the
primary steady-state claim.

No total or bounded server CPU metric is present in this remote matrix.
It cannot establish CPU savings, power savings, or zero CPU. Client
capacity, Python threading/GIL, TCP buffering, overlay/Tailscale jitter,
shared host/GPU activity, and GPU computation may mask request-path
differences. No causal breakdown among them was collected. Preserve the
uncertainty rather than treating any of these explanations as demonstrated.

Current review-time observation at 17:44:35Z finds the same RTX 5090 UUID,
15 MiB device memory, zero GPU utilization, no compute applications,
the TX module absent, all three own pins absent, and unrelated
tools/setup_env.sh preserved. The root's recorded 17:41:39Z API receipt
reports the original server UID/container Running/Ready with zero
restarts and an empty client item list after cleanup. The full-window
journal records clean TX lifecycles. These endpoint/discrete observations
do not prove continuous isolation or equal machine load throughout timing.
The raw gpu_after empty strings do not independently prove successful GPU
queries: early/per-executor return statuses were not archived. Software
versions in the full environment are explicitly post-collection observations
(torch 2.14.1, transformers 5.19.0, kernel 7.3.0-070300rc3-generic),
not a continuous full-window attestation. Current cached HF main references
observed during review are Smol 93efa2f097d58c2a74874c7e644dbc9b0cee75a2
and Qwen 7ae557604adf67be50417f59c2c2f167def9a775; these current observations
are not independent proof that future unpinned model-name downloads reproduce
the same weights. Root owns the authoritative overall cleanup verification.

This completed comparison supports the feasibility of ordinary cross-node
Linux TCP service without a steady userspace request worker. Its performance
hypothesis remains inconclusive for the tested same-compute conditions.
It changes the evidence frontier from loopback to actual cross-machine
delivery/performance, but does not establish a headline speed contribution.
Keep the result and move to a new discriminator with better expected
decision value, such as direct request-path attribution or a justified
compute-matched configuration that makes the suspected bottleneck visible.
This is a research recommendation, not authorization for new runtime
configuration or an unchanged retry. The retained full goal still requires
its broader serving, model reuse and performance claims to be qualified.
