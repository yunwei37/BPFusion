# Sustained remote delivery and complete observable resource ledger

Drafted2026-10-16 UTC, updated after official-reference full result/review.
Execution waits for the ongoing TCP_NODELAY full result and ordinary8
qualification, then records the selected source revision before acquisition. This plan preserves
the user's question: does removing the steady userspace network worker improve
real remote delivery or reduce the resources required for the same GPU service?

## Admission and competing evidence
Old finding0046 is finite closed-loop homogeneous serving over Flannel/Tailscale;
its Smol measurements span host faults and it has no complete resource ledger.
Finding0065's mixed scheduler improves both transports locally. Finding0066
diagnoses an adverse historical Qwen tail but does not reproduce its old gap
in the unchanged before condition; the close-guard candidate is not adopted.
Neither old remote closed-loop data nor local short offered-load data answers
sustained remote arrival/tail/cost behavior with the current ordinary source. Finding0069 now exposes a shared persistent
TCP stall; the admitted NODELAY causal matrix is the immediate priority and
must complete before this remote acquisition. It does not retroactively explain
the old kernel-specific6.36ms gap.
No unchanged timer sweep or model math campaign is proposed.

The strongest runnable competing mechanism is efficient native timed epoll
with exactly the same resident mixed GPU executor. Official vLLM is the
completed whole-service reference0069; do not rerun it remotely
merely to increase baseline count. This supporting experiment tests one
performance/resource tradeoff over an actual different-node Linux TCP path.
A positive result could identify a bounded useful operating range. Negative
or mixed results constrain the practical value of the eBPF transport and may
leave only the reusable integration/shared GPU scheduler contribution.
An inconclusive shared-host resource estimate is retained, not converted into
a CPU-saving claim. No thesis/RQ or model computation is rewritten.

## Workload and finite matrix
Original bpfusion-dev Workspace and RTX5090, same source-selected mixed vLLM
backend/checkpoint/runtime as the official-reference result. Qwen2.5-0.5B
revision7ae557604adf67be50417f59c2c2f167def9a775, FP16, explicit16 slots,
four existing prompts, gen64. Both paths use ordinary non-BF_TRACE libraries
and the unchanged transport header. Use the one selected server NODELAY
behavior identically on both paths after its separate qualification. Existing8/16 ABI qualification is reused.

Five paired server process blocks, alternating kernel/native order. Each
process executes both96 and192 requests/s, alternating rate order by block.
Each arrival window lasts60 seconds:5760 or11520 attempted requests per cell,
with the existing normalized gamma(shape1) schedules, seed20261015+block.
Freeze identical per-block offset arrays for both paths before acquisition.
Exclude exactly8 checked gen1 warmups. Retain the entire drain until all
requests terminal, with the existing60-second connect/I/O-operation timeout. The async adapter
uses wait_for around each connect/read/drain/close operation, preserving that
semantics rather than silently replacing it with a60-second total lifetime.
No artificial CPU stress, affinity, host/GPU setting or native queue cap.

The remote client uses Python standard asyncio so the sustained backlog does
not require one OS thread per request. No project concurrency cap is added.
Record schedule, task-start/connection/send/receive timestamps, raw returned
token IDs, errors, timeout/partial outcomes and client scheduling lag.
Every token in the same receive has the same observation stamp. This remains
client-observed per-token gap, not official stream-output ITL. Record zero
gap fraction and positive receive gaps separately.
Validate all lengths/vocabulary/protocol and report exact membership in the
unchanged pre-observation finite output set, with no observed-output expansion.
This ordinary finite fidelity check is not current hidden batch replay or a
universal numerical proof. Unexpected outputs remain visible and qualify
comparison validity; they cannot be silently relabeled correct.

## Real remote placement and lifecycle
Reuse the previous bounded client Job approach, original Workspace only.
Discover current server Pod IP/node/cgroup from live state. A disposable
standard Python client Job uses the existing pinned Python3.12.12 image
provenance and existing scheduler. Require a different eligible node through
anti-affinity against the actual server Pod; do not pin a hostname or add Spark
tolerations. Verify actual node/IP/UID/imageID and server reachability.
This is Flannel/Tailscale/Linux TCP, not bare NIC/ConnectX/GPUDirect.
No new persistent service, Workspace, controller, daemon or schedule.

Private BF_BIND uses the discovered current Pod IPv4 only for the bounded
remote run. Record actual command, image, route/RTT and cleanup. No public
endpoint/DNS/firewall change. Test-local Job creation/cleanup is authorized by
the requested benchmark under spark-manageAGENTS§8. Preserve active sessions,
unrelated WIP and all foreign workloads.

## Primary metrics and all-attempt treatment
At192, predeclared component contrasts are kernel-minus-native:
connect-origin completionP99 and complete server-host activeCPU seconds per
attempt. Report nominal paired t95df4 over the five process blocks.
At96 report the same values as the second predeclared operating point.
Also report TTFT/completion/TPOT P50/P95/P99, request and successful-output token
throughput, observed partial tokens, all-observed output throughput, errors,
timeouts, achieved arrival rate, max in-flight, scheduling lag and
scheduled-origin TTFT/completion. All-attempt denominator includes drain.
Failures censor success-only tails: a failed request is not a completed60s
response or evidence for lowP99. No SLO threshold or equivalence conclusion.
Crossing-zero intervals establish neither superiority nor equivalence.

## Resource accounting without missing or double-counting classes
Record raw monotonic sample brackets and units for all quantities. CPU/GPU interval brackets begin
before the remote kubectl exec and end after its terminal return; this includes
control/transfer overhead. Record its actual duration rather than pretending
it equals exactly the60-second arrival window. Warmups precede this bracket. The primary
hostCPU observable is /proc/stat active user+nice+system+irq+softirq ticks across
all CPUs, with idle/iowait/steal separately shown. It includes host kernel
threads and interrupts but also other tenants. It is a full-host observation,
not exclusive per-service causal CPU. Keep all background exposure; no foreign
work is stopped. Report its paired estimate/uncertainty with this limitation.

Alongside it, collect high-resolution owned-process-group CPU, thread identity/
TGID/starttime/comm/flags and per-thread runtime/tick snapshots, owning cgroup
cpu.stat/pressure/max/weight and memory observations, and observerCPU separately.
Keep process/group, cgroup and host totals as nested views, never add them.
Modern io-wq workers are created with CLONE_THREAD; verify actual identities
and account this subset once inside the service group, rather than assuming
all io-wq work is outside the process:
[io-wq source](https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/io-wq.c),
[thread creation](https://github.com/torvalds/linux/blob/v7.3-rc3/kernel/fork.c#L2536).
The cgroup interface accounts its processes and descendants:
[cgroupCPU](https://docs.kernel.org/admin-guide/cgroup-v2.html#cpu).
IRQ accounting depends on actual kernel configuration and context:
[CPU accounting source](https://github.com/torvalds/linux/blob/v7.3-rc3/kernel/sched/cputime.c).
Read the running configuration/available counters. Host softirq counts/times
are separate exposure; they are not all attributable to this socket.
Unattributed root ksoftirqd/IRQ/driver work is explicitly unknown, not zero.
Do not assert a true total service CPU saving from groupCPU alone.

Read-only preflight capability query confirms NVML cumulative energy is
available on this RTX5090. Record hardware-reported energy deltas alongside
NVML power/clock/memory/utilization; unavailable/unstable reads remain missing. Unsupported energy is unavailable;
a power-sample integral is labeled an estimate with cadence/missing coverage,
not exact energy. Device-wide readings include all GPU users; retain observed
PIDs. Resident kernels can make utilization100% with few occupied SM resources,
so this is not proof that all compute is saturated. Reuse normal cuobjdump
resource information for the dispatcher and additional GPU I/O CTA, plus
source launch dimensions and queue/pinned allocation sizes. This is a static
footprint, not a dynamic per-kernel execution-time or SM-attribution claim.
No unavailable/incomplete device-graph CUPTI count is treated as complete.

Each server has a declared5-second service-idle bracket after warmup to show
heartbeat/persistent-queue cost. Report idle and active separately; subtracting
a noisy host idle bracket does not manufacture a clean service-only estimate.
The existing timestamp diagnostic supplies qualitative GPU queue latency,
not additive marginalP99 allocation or replacement energy/cost measurements.
Record observer overhead and missing/unstable identity/counter coverage.
The existing cgroup2 mount exposes the actual Workspace container path;
root cpu.stat is the whole hierarchy and must not be confused with it.
Observer snapshots device/host/cgroup/group at actual approximately100ms
cadence and service-thread identities/runtime at approximately1s, with full
begin/end detail. Process CPU includes all threads even when short-lived
workers escape that detail census. Namespace-visible root kthreads are only a
partial census; do not call an absent root worker zero.
The100ms cadence is observational, not a retained server runtime change.

## Execution and review
After final admission and fresh plan review, run one real short two-path remote
preflight using the actual endpoint, client, counters and analysis, then all
10 server processes/20 sustained cells to terminal. The full matrix contains
172800 measured attempts and11059200 requested output tokens, plus80 warmups.
This is acquisition volume, not a research contribution. Preserve failures
and exact partial prefixes; do not replace unfavorable blocks or tune rates.
At most3 real preflight attempts, one fresh result review after full execution.
Record and diagnose actual host/storage faults before further long acquisition;
normal replies alone do not prove host/storage health.

Freeze actual source/client/offsets/image/commands and implement the runnable
entrypoint before preflight. Keep ordinary code, raw per-process files, counter
snapshots, analysis and reviews in this archive; compress large data losslessly.
After each validated stage commit/push main. Remove own client Job/Pod,
server children and pins at the end, verify original Coder/build/WIP state,
and retain the shared temporary runtime until no requested task uses it.
No partial prefix is a complete experiment or project-goal completion.

## Concrete prepared commands and operational receipts
Prepared only in the original Workspace TEMP:
remote_prepare_schedules.py freezes all10 offset arrays before acquisition;
remote_async_client.py --host DISCOVERED_IP --config qwen_frozen.json
--offsets remote_offsets.json --output PATH --pair BLOCK --rate96or192
[--warmup|--preflight] runs in the disposable client Pod.
resource_observer.py --pid OWN_SERVER_PID --output PATH runs beside the server
under the existing pinned runtime; stop it by SIGTERM after client terminal.
The outer owner uses scripts/kubectl-home.ps1 for creation/exec/removal, as in
the previous admitted cross-node benchmark. No alternate cluster control plane.
Actual stdout/raw files are retained in Workspace, not streamed per-token into
Windows timing loops. CPU-only analysis consumes the per-attempt client and
server observer files and fixed source-native metric definitions.

Live read-only discovery during preparation2026-10-16UTC still finds original server Pod UID
3e8994f8-77ba-4a73-a3a5-35ed69a0a8a2 on lab/IP10.42.1.238, and no old BPFusion
client Job remains. Rediscover before creation; these observations are not
hard-coded placement/configuration. Reuse old benchmark Job shape and
workspace-label anti-affinity, same version-pinned Python image. No new Job has
been created by this proposal. Application code/builds/analysis remain in
the original Workspace; the separate Pod is only the requested load generator.

Static candidate cuobjdump currently reports dispatch40 registers/zero local/
zero shared and IO kernel48registers/168stack/zero shared/zero local bytes.
The launch dimensions are dispatch<<<1,32>>> and extra IO<<<1,1>>>.
These are compiled static resources, not actual SM-time or proof of saturation.
Archive both path binaries' resource reports after final source selection.

Outer real command after the selected source build and client discovery:
powershell -File run_remote_matrix.ps1 -ClientPod DISCOVERED_CLIENT
-ServerIP DISCOVERED_SERVER_IP -Preflight
then the same command without-Preflight runs all five paired blocks.
The script only orchestrates existing Kubernetes exec operations; server,
observer and analysis execute in the original Workspace, with only the explicit
load generator in the disposable client Pod. It neither changes host settings
nor creates a second development environment. Client raw data is compressed
after resource sampling stops and transferred byte-exact via base64/gzip;
per-token stdout transfer is excluded from resource intervals.
Actual exec brackets include connection/control latency, not exactly60s.

The pending client_job.json reuses the previous benchmark Job shape, no new
persistent service. The Job remains owner-cleaned after all terminal results;
no timer, deadline, resource cap, host pin or credential is added.

## Selected source after completed repair
TCP_NODELAY full matrix and independent review are valid/supporting, followed
by all6 default8 qualification commands and ordinary root-source8/16 builds.
Selected serving implementation is2c0cf7b0daa81b3d65f4232f1b14def0966ec887.
No further server source/default change is planned during this remote matrix.
Ordinary build directory is TEMP/tcp_sourcebuild16, both transports; no tracing.
The observer records actual own BPF object fdinfo/map_info at setup as resource
metadata, without creating objects or adding steady-state probes.
