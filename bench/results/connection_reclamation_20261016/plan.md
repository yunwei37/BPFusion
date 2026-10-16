# Connection reclamation under sustained remote load

2026-10-16 UTC. Supporting causal repair within the retained serving-performance
RQ: does removing the steady userspace network worker improve remote delivery
or resources with matched resident GPU execution? No RQ/thesis/model math change.

## Admission

Finding0071 completes the requested sustained test and exposes6.816% kernel192
timeouts. One835-timeout cell has exactly835 sockhash insertion failures;
one cell reaches4096 active connections. This is new evidence requiring a
specific causal discriminator, not another unchanged load sweep. The strongest
current alternative is efficient native epoll with identical mixed executor;
official vLLM reference0069 already exists and is not rerun just for count.
A successful repair can remove a real implementation confound before assessing
the mechanism. Failure narrows the cause and leaves sustained kernel serving
unqualified; mixed/inconclusive outcomes retain all errors. It is supporting
workload/lifetime evidence, not intrinsically a paper throughput contribution.
Changing capacity, polling intervals, model kernels or host settings is not
the intervention. Existing untouched0071 remains the historical control.

## Hypothesis and discriminator

Current close guard requires EOF/dead, no receive/reply references, seen=head,
and global llm_queued=0. Continuous unrelated backlog can retain completed
connections, fill sockhash/accept capacity and lose admission. Alternatives:
sockhash EEXIST/ENOMEM, delayed parser/redirect, independent admission/slot races,
shared CPU scheduling. First instrument the existing reserved admission_pad
field on the insertion-failure branch with the first negative errno (positive
magnitude), plus read-only map/FD/connection census during actual failure.
No extra BPF map, daemon, host tuning or persistent state. Record actual errno
and active socket states rather than assuming E2BIG.

A candidate may replace global queued dependence with conservative per-peer
pending references in the existing shared page. Proposed shared hash buckets
delay reclamation on collision but must never close early. Producer increments
before publishing pending; rollback on push failure; single consumer publishes
the slot before decrement. Peer-local reclamation applies only to actual RECV EOF, not arbitrary send
error or canceled receive. Dead without EOF keeps the original global guard;
stop retains the existing override. Linux tcp_bpf_recvmsg_parser holds the socket
lock, processes preaccept receive data and drains ingress before reporting EOF:
https://github.com/torvalds/linux/blob/v7.3-rc3/net/ipv4/tcp_bpf.c#L207 .
This is not a claim to solve indefinite RST floods.
GPU first acquires own pending bucket, then freshly
checks head/seen so a popped/published request cannot be missed. EOF/receive and
active reply ownership remain required. Pending cancellation/stop and every
producer/consumer must preserve references. All ABI-dependent8/16 components
are rebuilt together. If actual errno/census contradicts lifetime/capacity,
repair the demonstrated cause and record the plan change rather than forcing
this hypothesis. Candidate is not adopted before real qualification.

## Integrated comparison

Primary main baseline: efficient native epoll, same GPU/model/NODELAY16.
Mechanism control: kernel global close guard with the same reference accounting/
ABI as candidate (common instrumentation overhead), clearly labeled component
ablation rather than strongest competitor. Candidate: local pending guard.
One192/s operating point,60s normalized gamma schedules,11520 attempts/cell,
gen64 and the same frozen4prompts/revisions/runtime as0071. Five process blocks,
three conditions with rotated/reversed order:
global/local/native; native/local/global; local/global/native;
native/global/local; global/native/local.
Use identical offsets seed20261015+block for all three conditions.15 processes,
172800 measured attempts,120 excluded checked gen1 warmups. No extra96 repeat
solely to add rows. Existing96 and qualification cover the lower-load scope.

Primary causal contrast: local-minus-global failed-attempt fraction, paired
nominal t95df4 across5blocks, all attempts retained. Full all-attempt successful
token throughput and connect-origin TTFT/completion/gapP99 (success conditional)
remain paired secondary outcomes, alongside CPU/cgroup/host/device views with
the same observer/control brackets. Report local/native separately; zero
observed failures is finite evidence, not equivalence. Failed requests do not
become60s completed responses. No exclusion of inconvenient blocks or new SLO.
Primary standard delivery metrics follow the existing vLLM benchmark reference:
https://github.com/vllm-project/vllm/blob/main/docs/benchmarking/cli.md .
Failure fraction is failed attempts/attempts. No invented aggregate score.
Finite frozen-reference disagreements remain visible, no observed-output pool
expansion. Source-native dual replay qualifies the engineering surface separately.

## Real execution/qualification

Existing Workspace, sequential GPU, same temporary g10 client Job and private
bind. Reuse remote_server.py, remote_async_client.py and resource_observer.py
with only condition/build selection and single-rate matrix adaptation.
Keep original60-second per-I/O-operation timeout and full drain. Archive every
terminal server before starting the next one so compression does not overlap
measured cells. Preserve unrelated work/Coder sessions and foreign tenants.
No new Job/Workspace/scheduler/public endpoint.

Real preflight includes both efficient native and actual kernel paths and
enough real requests to cross4096 cumulative connections (at least4608 at192).
Expected global-control timeouts are outcomes, not runner errors. At most3
preflight attempts per experiment skill; no favorable unchanged rerun.
Read-only errno/map/socket snapshots establish mechanism engagement.
If short workload never engages the hypothesized retention, use the full60s
window as the diagnostic preflight, preserving its outputs and limitations.

Before source adoption qualify default8 Qwen/Smol normal builds, traced protocol
dual replay, normal queuedRST/mid-output stop/drain, and targeted real request
hash collisions/peer reuse/EOF while another peer is queued. Counter collision
must delay close only. Normal8/16 BPF/loader/GPU builds all pass. If common
transport/header changes, rerun the existing cuBLAS/cuFFT ordinary lifecycle
surface. Do not claim these dependency checks as separate scientific results.

## Interpretation / artifacts

First outcome is errno+census evidence and root cause. Full outcome includes
all15 terminal processes/cells and every failure. If local removes insertion
failures but has no speed advantage over native, report only a reliability
repair. If adverse effects remain, sustained serving stays unqualified.
If global fails to engage, no causal lifetime claim even if local looks faster.
Keep raw JSONL lossless gzip, commands/source/build receipts and stdlib replay,
one result and fresh independent result review. Publish each completed step
directly main as authorized. Cleanup client Job after bounded repair/retest.
No assertion that old unreproduced6.36ms is now quantitatively decomposed.
