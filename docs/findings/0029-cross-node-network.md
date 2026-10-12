# Cross-node TCP/HTTP with reused model graphs

## Question and current status

Does removing the steady userspace request worker improve client latency or
throughput over efficient native networking on a real cross-node path,with
identical upstream GPU computation?

The [plan](../../bench/results/physical_network_plan_20261011.md) and
[fresh plan review](../../bench/results/physical_network_plan_review_20261011.md)
admit a supporting comparison. There is no formal paper RQ or external SOTA
claim. Finding0028 remains separately closed and inconclusive.
Address compatibility and all four real cross-node preflight executors pass.
The80-cell full comparison and fresh result review remain pending; preflight
numbers do not establish a performance benefit.

## Necessary source adaptation

Graph executors reuse existing BF_BIND with127.0.0.1 default. Kernel TX reads
the concrete local IPv4 address from its owned listener for established-socket
lookup. This preserves network-order address/peer-port and host-order local
port semantics. Legacy reply_addr remains a fallback without a listener FD.
Kernel listener validation includes family,protocol,state,port,address and
network namespace. Wildcard listener,IPv6 and VRF are not qualified.

The four-source change is24 inserted/12 deleted lines: graph binding,kernel
lookup authority,and destination substitutions in existing test/benchmark.
Model computation,precision,eight graph/KV banks,dispatcher,queue ABI,TX
coalescing and wait policies are unchanged.
[Build receipt](../../bench/results/physical_network_build_20261011.stdout.txt)
contains four successful graph builds and the owning module Kbuild.
Existing compiler/pahole warnings and unavailable-vmlinux BTF skip are retained.

## Dependency qualification and default compatibility

[Own-Pod-IP strict stdout](../../bench/results/physical_network_binding_qualification_20261011.stdout.txt)
records normal exits for both kernel models and Qwen timed networking:
1005 valid requests,61296 exact independent eager-HF tokens,777 rejections,
plus5000 empty connections per invocation. Fragmentation,reuse/wrap,
pipeline/half-close,mixed lengths,invalid IDs,after-ready network tracing
and cleanup pass. These connects originate inside the same Workspace;
they prove binding/lookup,not physical delivery.

[Default-loopback preflight raw](../../bench/results/physical_network_loopback_preflight_20261011.jsonl)
and [stdout/native analysis](../../bench/results/physical_network_loopback_preflight_20261011.stdout.txt)
complete three modes,Qwen,12 exact measured one-token replies,three normal
executors,one hostlaunch/264modelgraphsteps/eightbanks/zeroerrors each.
The busy row is compatibility dependency evidence,not another full baseline.

## Actual cross-node preflight

The original server remains bpfusion-dev on lab,PodIP10.42.1.238.
A disposable benchmark client Job runs on raspberrypi,PodIP10.42.0.118,
with Python3.12.12-slim-bookworm and no model or project PVC.
[Exact temporary Job](../../bench/results/physical_network_client_job_20261011.json)
and [environment receipts](../../bench/results/physical_network_environment_20261011.txt)
retain actual identities,imageID,placement and cleanup contract.

[Smol raw](../../bench/results/physical_network_smol_preflight_20261011.jsonl),
[Qwen raw](../../bench/results/physical_network_qwen_preflight_20261011.jsonl)
and [both direct analyses](../../bench/results/physical_network_preflight_analysis_20261011.stdout.txt)
complete four normal executors,four cells,16 measured exact tokens.
Eight warmups/executor are separate and also checked against independent
references. Each executor reports1hostlaunch,264modelgraphsteps,banks8,
graph_error0,maxactive1,as expected for this preflight. Timed controls engage
epoll_pwait2 60000ns,published12/completed12/rejected0 with kernel TX absent.
Each resident kernel lifecycle reports2000bytes,12completions,zeroabandoned/
retries,2accepted/closed.

The [native client adapter](../../bench/results/physical_network_client_20261011.py)
reuses request()/connect() verbatim; [literal invocations](../../bench/results/physical_network_preflight_invocations_20261011.txt)
retain actual case/cell calls. [Analysis](../../bench/results/physical_network_analysis_20261011.py)
recomputes client metrics without fabricated server CPU.
Client-local monotonic durations require no cross-machine clock subtraction.
Descriptive quantiles use nearest rank,unlike older interpolated tables.

[Inner TCP capture](../../bench/results/physical_network_preflight_tcp_20261011.pcap)
and [decoded capture/log](../../bench/results/physical_network_preflight_tcp_20261011.txt)
record the actual10.42.0.118↔10.42.1.238:39403 tuples across flannel/CNI:
3708 captured/received records,zero kernel drops. Multiple forwarding
interfaces duplicate records; this is not3708 unique packets or requests.
Snapshot length256 truncates some payloads; client oracle is the complete
output check. Interface labels are read-time labels; retain SLL2 indices.

[Carrier header examples](../../bench/results/physical_network_preflight_carrier_20261011.txt)
and route/physical-device receipt identify enp129s0 and
128.114.59.130↔128.114.59.42 UDP41641 Tailscale transport.
That capture also includes unrelated encrypted peer traffic; retain bounded
headers only and attribute no carrier byte rate or energy to BPFusion.
This is cross-node Linux TCP over existing flannel/Tailscale and a physical
Ethernet underlay,not bare-NIC TCP,GPUDirect or an OS-bypass service.
Both preflight captures are stopped before full collection.

## Boundary and next action

One management SSH attempt times out across HA servers; later real SSH and
owning API reads confirm Ready nodes and no client Job. No reboot,route or
credential change is made. A later local-path/remote-kubectl setup error
creates no object; stdin succeeds. These are retained setup observations,
not failed model samples. A journal command with ambiguous local timestamps
fails before saving data; the corrected explicit UTC window is retained.
That window has normal own module lifecycles and no matching listed kernel/
GPU/memory/filesystem fault lines. It does not prove continuous isolation.

Server test processes,module and pins are absent after preflight. The single
client Job remains for the admitted full matrix and must be deleted at its
normal or failed completion; the overall benchmark is not restored yet.

Freeze source and run all80 cells/5120 requests/166400 measuredtokens/
20 normalexecutors,with five paired process blocks per model and fresh result
review. Retain negative/inconclusive outcomes. No total service CPU,full text/
JSON,online batching,arbitrary model support or external serving superiority
is established here; those remain under the full retained goal.
