# Causal test of persistent-connection delivery stalls

2026-10-16 UTC. Retained question: can Linux TCP/eBPF around reused resident GPU
computation improve delivery latency/throughput against efficient native TCP?
No formal paper/RQ file exists; retain that question without rewriting it.
Read evaluation, findings0065/0066/0069, official-reference raw/review and
background-related-work before this proposal.

## Admission, hypothesis and paper decision
Current official-reference closed16 has client per-token-gapP99 about40.4ms
and83.4% zero gaps in both own transports, versus official4.87ms.
Both own server listeners omit TCP_NODELAY; client-side NODELAY only controls
the client sender. Nagle holds small writes while earlier data is unacknowledged:
[tcp(7)](https://man7.org/linux/man-pages/man7/tcp.7.html),
[matching Linux source](https://github.com/torvalds/linux/blob/v7.3-rc3/net/ipv4/tcp_output.c).
The40ms pattern alone is not proof. No existing capture records actual ACKs,
send-queue state or controlled server option. Reanalysis cannot settle cause.

Hypothesis: server Nagle/receiver delayed-ACK interaction is a material cause
of the reproducible persistent streaming stall. Enabling only server TCP_NODELAY
before listen should remove the ACK-dependent hold and improve client gapP99.
Competing explanations: GPU publication/scan gaps, host/client scheduling,
cork flags, or parser coalescing. A valid null/contradictory effect leaves
NODELAY unselected and redirects diagnosis to whichever phase the evidence
identifies. Positive evidence selects an ordinary transport fix shared by
both paths; mixed evidence narrows scope. None proves eBPF superiority or
quantitatively explains the old unreproduced kernel-specific6.36ms difference.

Role supporting, mechanism/workload boundary. This direct discriminator outranks
long remote/resource collection with a known unresolved delivery defect.
No model math change, polling/timer sweep, affinity or host/sysctl tuning.

## Paths, control and intervention
Same original Workspace/RTX5090, Qwen revision7ae55760, FP16/runtime0.31 and
ordinary mixed source45f0ec2 with16 slots, existing four prompts, gen64.
Efficient timed-epoll native remains the strongest component competitor.
Original kernel/native sourcebuild16 are before controls.
Private candidate changes only checked TCP_NODELAY on the listener before
listen/accept, with necessary netinet/tcp.h include. Freeze source/diff/build
commands; GPU computation and transport headers stay identical.
Listener inheritance and accepted-socket value are checked for our own sockets
where available, without changing permissions or foreign processes.
Do not mutate canonical source before evidence and lifecycle qualification.

## Integrated acquisition
First diagnostic preflight runs actual Qwen persistent16 before/after for both
paths,32 requests/cell, same client as official-reference. A bounded AF_PACKET
capture on loopback records only benchmark-port TCP headers/timestamps,
sequence/ACK/payload lengths and drop counters; no foreign payload is persisted.
Record actual own accepted TCP_NODELAY/TCP_INFO where possible. Raw diagnostic
overhead means this is mechanism evidence, not performance-primary acquisition.
Look for server sends acknowledged only after the stall and queued unsent bytes
despite completed send work, with the hold removed by the single intervention.
Do not claim cause from packet gaps alone if application publication is unknown.
Use own-socket TCP_INFO notsent/unacked or a bounded syscall/send completion
trace to distinguish buffered network data from late application/GPU production.
No arbitrary40ms cutoff defines success. Preserve observer clock/cadence/loss
and missing attribution explicitly. At most3 preflight attempts; repair real
execution defects, retain failures.

After executable preflight, full matrix:5 process blocks,4 conditions
[kernel_before,kernel_after,native_before,native_after], balanced Williams order
[0,1,3,2],[1,2,0,3],[2,3,1,0],[3,0,2,1],[0,1,3,2].
Each process runs persistent16 and normalized-gamma offered192 (seed20261015+
block) with256 measured attempts each; alternate regime order. Exclude exactly
8 checked gen1 warmups/process. All20 executors/40 cells/10240 attempts and
655360 requested tokens run to terminal. Packet capture is off in full runs.
Original60s request timeout, partial outcomes/errors/task lag all retained.
Retain old official result as dated reference, do not rerun it just for count.

## Metrics, correctness and interpretation
Use exactly official-reference CPU-only analyzer/client metric definitions,
linear percentiles and mean process statistics. Client per-token gapP99
retains coalesced-token zero gaps; not official stream-output ITL.
Report positive receive-gap distribution/zero fraction, TTFT/completion/TPOT
P50/P95/P99, successful/all-observed throughput, failures/timeouts, client lag,
scheduled-origin tails and groupCPU. No processCPU-as-total-resource claim.
Metric definitions: [official vLLM benchmarking](https://github.com/vllm-project/vllm/blob/main/docs/benchmarking/cli.md);
the explicitly named token-gap metric follows the existing project protocol.

Primary candidate-minus-before persistent16 token-gapP99 is separately paired
within kernel and native, nominal t95df4. Full interval below0 supports a
beneficial streaming effect for that path; crossing0 is inconclusive, not
equivalence. State magnitude and throughput/other tails/adverse outcomes.
Failures censor successful tails; no favorable exclusions/replacement blocks.
Protocol/length/vocabulary/prompt/finish valid; report membership in unchanged
pre-observation finite output set, no observed-output expansion or universal
numerical-parity claim. Any source adoption additionally requires normal
default8 protocol and mid-output cancellation checks for both qualified models
and transports, reusing the existing independent replay/oracle fixtures.

## Runnable path, publication and cleanup
TEMP/tcp_nodelay.py --output PATH [--preflight] will reuse the frozen official
driver with only condition/build selection and bounded diagnostic hooks.
CPU analysis reuses official_analysis.py with four condition contrasts;
raw/gzip/source/diff/commands/review stay in this directory. One fresh plan
review before actual acquisition, one fresh result review after terminal.
No paper/idea/RQ edits. Commit/push each completed qualified stage on main.
Same loopback39403/private runtime, no public/persistent service or new scheduler.
Stop only owned server/capture groups and remove owned pins; preserve original
Coder identities/builds/WIP. Keep shared TEMP until later requested tasks finish.
