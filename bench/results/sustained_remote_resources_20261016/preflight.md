# Real different-node/resource preflight

Actual client bpfusion-sustained-client-20261016-s2g8m runs on g10/IP10.42.6.217;
original Workspace/server is lab/IP10.42.1.238. Actual imageID matches the
previous version-pinned Python3.12.12 image, with no restart. See client_environment.json.

The actual run_remote_matrix.ps1 -ClientPod NAME -ServerIP10.42.1.238
-Preflight exits0. Both ordinary root-source16 paths and both arrival-prefix
rates execute. All4 cells have32/32 successes:128 requests/8192 tokens plus16
separate excluded warmups. Both servers admit/retire72, exit0 and remove own pins.
All observers terminate with retained raw host/cgroup/group/thread/device samples;
archive CPU analysis reproduces bytewise without the GPU runtime.

This dependency establishes executable real workload, metric, resource and raw
paths, not a performance/energy result. In these32-attempt short prefixes,
the roughly3-second resource brackets contain substantial Kubernetes exec/control
overhead beyond the subsecond arrival interval; do not present those per-attempt
resource numbers as sustained costs. Full60-second windows retain the same
honest bracket definition and report actual duration/observer overhead.

Actual io-wq worker741801 reports Tgid741545, the kernel server process, with
Kthread0. Its CPU belongs inside the high-resolution process/group clock;
do not add it again as an external kernel-thread cost. No such worker appears
in native snapshots. The1-second thread census is finite and may miss short-lived
workers; the group clock still includes its owned threads. Root kthreads and
softirq/TCP work remain only partly attributable from shared-host counters.

Read-only map metadata shows stream/pending capacity4096 and actual shared-page
value21824bytes; source formulas and GPU static resource usage are preserved.
Hardware-reported device energy is available, not inferred from GPU utilization.
Whole device/host/cgroup include background and observer work and are not summed
with each other or called exclusive service cost.

An initial data-copy command was incompatible with kubectl-home's single-quote
argument contract before any server started. The ordinary orchestration adapter
now uses quote-compatible Python -c arguments; infrastructure helper is unchanged.
Actual scripts/client source and per-cell exec receipts are retained.
No failed GPU preflight or replaced cell occurs.

Host kernel journal11:04UTC through the pre-full check is retained. It contains
the existing exporter AppArmor denials/CNI traffic, with no matched EXT4/I/O/OOM/
Xid/BUG/Oops/NVMe/AER failure pattern. Finite observation is not hardware isolation.
Workspace filesystem has14.4GB free and temporary filesystem319.8GB at preflight
endpoint; no foreign workload or data was removed.

The temporary client Job remains only to run the admitted full matrix.
The source-selected CUDA/transport implementation remains2c0cf7b, with later
record commits only. All10 servers/20 sustained cells remain to run.
