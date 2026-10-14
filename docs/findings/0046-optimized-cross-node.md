# Optimized module-free cross-node serving

The current resident packed/prefix upstream-vLLM backend completes real
cross-node binary-token HTTP serving using the upstream eBPF/io_uring loop,
without a custom TX module or qualified steady userspace request worker.
The matched client measurements establish no primary performance advantage.
The actual host journal contains global OOM and filesystem faults during
Smol collection, so this is a fault-qualified shared-host observation, not
a clean stable-host causal performance result.

## Question, source and complete execution

Retain finding0029's question: does removing the steady userspace request
worker improve client latency or throughput over efficient native networking
on a real cross-node path, with identical upstream GPU computation?
The [plan](../../bench/results/optimized_cross_node_20261014/plan.md) and
[fresh plan review](../../bench/results/optimized_cross_node_20261014/plan-review.md)
admit supporting work. Old HF cross-node and optimized local measurements
cannot provide this changed-backend/topology comparison.

Frozen execution checkpoint81baa94c84a5567950e87f3310788c000c6e9d6a has the
same production implementation as bd39e59. Both models share FP16 upstream
vLLM0.31.0/Torch2.13.0+cu129/Transformers5.17, pinned checkpoints, packed
prefill/prefix-release source policies and nominal60000ns waits.
The candidate adds GPU io_network and kernel-loop coordination; native is the
efficient timed-epoll same-compute alternative. Actual batch trajectories and
compiled dispatcher SASS differ; no byte-identical machine-code or exclusive
eBPF causal attribution is claimed.

Original server stays lab/bpfusion-dev10.42.1.238; disposable client runs
g10/10.42.6.216 over existing flannel/Tailscale. This is actual different-node
Linux TCP, not direct ConnectX, bare-NIC or GPUDirect.
[Topology receipts](../../bench/results/optimized_cross_node_20261014/client_environment.json)
retain identities and imageID; no hostname pin or persistent network change.

Both actual preflight paths complete80 requests/2096 checked tokens including
16 excluded warmups. Full untraced collection completes20 normal executors,
80 cells,5120 measured requests/166400 measured tokens plus160 checked
excluded gen1 warmups. Five paired process blocks per model alternate path
order and rotate all four gen1/64 by c1/8 cells,64 requests/cell.
Every complete output matches the unchanged pre-observation whole-sequence set:
Qwen17 keys22 sequences; Smol17/19. This is finite-set fidelity, not current
unobserved batch/KV replay, task quality or arbitrary-model qualification.

All actual clients and servers exit0. All10 loop terminals have264 complete
requests,accepted=closed=19,independently drained SQ/CQ,pending/error/reserved/
drop/transport-overflow0. Fixed128-entry reply diagnostics truncate136 records
per executor; all264 client replies remain present. Model trace_overflows0 is
a separate counter. Qualified preflight traces show one steady kernel ENTER,
no serving userspace socket calls or SQPOLL. Ordinary full runs reuse that
source but are not separately syscall-traced. Native performs actual socket
operations and reports timed epoll; the selected strace omits epoll_pwait2.

## Complete observed client comparison

| Model | gen1/c1 mean TTFT loop / native ms | gen64/c8 throughput loop / native token/s |
|---|---:|---:|
| Qwen2.5-0.5B | 3.422434 / 3.418743 | 4288.188620 / 4316.247740 |
| SmolLM2-135M | 3.146517 / 3.169289 | 5020.916572 / 5016.229532 |

All four predeclared primary effects, positive favoring loop, use nominal
paired t95 df4 over five process blocks.

| Model | Primary effect | Mean | Nominal t95 |
|---|---|---:|---|
| Qwen | native-minus-loop TTFT1/c1 ms | -0.003691 | [-0.126505,0.119122] |
| Smol | native-minus-loop TTFT1/c1 ms | +0.022772 | [-0.033461,0.079005] |
| Qwen | loop-minus-native TPS64/c8 | -28.059120 | [-76.190291,20.072051] |
| Smol | loop-minus-native TPS64/c8 | +4.687041 | [-43.215784,52.589865] |

Every primary interval crosses zero. No reliable native delivery advantage,
equivalence, zero-effect or familywide superiority follows. Keep all blocks.
The [independent result review](../../bench/results/optimized_cross_node_20261014/result-review.md)
replays both analyses byte-identically and separately reconstructs timestamps,
throughput, paired effects and intervals.

Retain observed secondary negatives: Smol gen64/c1 loop TPS is lower by
20.927330 token/s,t95[17.416961,24.437698],negative in all five blocks.
Completion is slower by0.792989ms,t95[0.663935,0.922043],and TPOT by
0.013440ms/token,t95[0.010434,0.016445]. These are concordant observations,
not clean causal effects or predeclared primary confirmations.
Qwen several latency/throughput point estimates also favor native; all
secondary cells,tails and extremes are retained in the complete review.
No remote per-cell server CPU,total CPU,energy,SLO or transport-stage timing
is measured. Prior local CPU values cannot be relabeled cross-node measurements.

## Actual failures, host fault and interpretation

A preflight wrapper omits source-native post-detach pin removal; native
bootstrap fails before model launch or client samples. Adding the same three
owned pin unlinks repairs reporting/lifecycle glue; valid candidate output is
preserved. An artifact-transfer command exceeds Windows command length after
the client completed; chunked transfer preserves its actual logs.
[Qualification](../../bench/results/optimized_cross_node_20261014/qualification.md)
retains both failures, with no timing/oracle/model modification.

After12 full executions, Cloudflare SSH observation fails with a websocket
bad handshake. Existing Kubernetes observation confirms the same original
server PID296241 alive and ready, and client not yet started; that process
continues through its single actual client and normal terminal. No executor
or row is replaced. Exact observer failure instant is unrecorded.
[Reconnection evidence](../../bench/results/optimized_cross_node_20261014/reconnection_observation.md)
and actual process receipts preserve the limited evidence.

The actual [kernel journal](../../bench/results/optimized_cross_node_20261014/kernel_journal.json)
and retained raw log record global OOM and EXT4/I/O failures at05:28:38 UTC.
Qwen ends before this burst; Smol's whole matrix spans it and the accompanying
resource-state change. Own normal replies do not rule out interference;
nominal intervals do not repair environmental confounding. No rows are
dropped and no clean-host causal interpretation is made.
[Host fault scope](../../bench/results/optimized_cross_node_20261014/host_fault_scope.md)
uses stable filesystem UUIDs to map the affected retained volumes and
records existing-controller remount/recreation; it does not certify all
other-project AI sessions or full filesystem integrity.

Independent review judges complete serving/finite shared-host observation
valid, primary gain hypothesis inconclusive, research role supporting,
impact additional RQ/environment boundary. This closes the unchanged matrix,
not the full project objective. Further experiments need a useful causal
discriminator after actual host/storage validation; no favorable timer search
or model-specific arithmetic campaign follows from these outputs.

## Restoration and reproduction

[Final restoration](../../bench/results/optimized_cross_node_20261014/final_restoration.json)
removes the temporary client Job/Pod,runtime and13 named build entries.
Original Workspace/PVC,boot,base packages,default HF library,Coder processes
and unrelated tools/setup_env.sh remain. No own module,pins or GPU app remains
at the final endpoint; this is not continuous isolation.

The linked archive contains exact pinned dependency/build commands, source-native
client functions and literal per-executor client/server commands, raw output,
actual exits and analysis. Recreate a fresh temporary environment and substitute
its path for the removed historical TEMP; bind the current discovered concrete
Workspace IPv4 and execute the client on a different eligible node.
Replay the retained metrics from the repository root with:

    python3 bench/results/optimized_cross_node_20261014/analysis.py bench/results/optimized_cross_node_20261014/qwen_full.jsonl bench/results/optimized_cross_node_20261014/smol_full.jsonl

GPU model computation is reused. General text/JSON serving, backend portability,
full SLO/CPU/stage measurements and an established performance contribution
remain unfulfilled under the retained full objective.
