# Source audit: a possible kernel-owned network constructor

2026-10-16 UTC, while the admitted controller-stage matrix is running. This
is a source-grounded next-candidate audit, not a new admitted experiment,
implementation, result, source selection or reason to interrupt the matrix.
No production source/build/GPU workload changes follow from this document.

## Verified enabling API and current constructor

The tested-stack BTF declares IOU_REGION_MEM/CQ/SQ. Current
bpf/uring_loop.bpf.c already obtains writable registered control/CQ regions and
calls bpf_io_uring_submit_sqes; it presently submits GPU-prepared SQEs.
The ordinary mixed Make recipe does not define BF_IO_COALESCED, so
executor/io_uring_tcp.h launches a separate persistent io_network CTA.
Current model dispatch itself is the same algorithm used by native epoll.

Version-pinned primary source:
https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/bpf-ops.c
The region helper returns the registered parameter, combined ring or SQE
region after checking the requested constant size. The submit helper calls
the ordinary kernel SQE submission path. Installation rejects SQPOLL/IOPOLL
and requires DEFER_TASKRUN, consistent with this project's existing setup.
https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/loop.c
The loop invokes BPF under the ring lock, waits for requested CQ progress,
handles task work/local completion work and returns for signals. This does
not by itself demonstrate an application TCP state machine or its correctness.

Current fusion.bpf.c also reclaims final replies using existing SEND/ABORT
tags at io_uring completion. The corrected admission queue, pending-peer EOF
protection and recent lifecycle checks are reusable implementation evidence,
not permission to omit those semantics in another constructor.

## Candidate inference, not a measured conclusion

A possible next driver can have the BPF loop itself consume CQEs, maintain
host-resident connection/reply state and populate/submit SQEs. Startup still
creates the listener/ring and registers memory. Existing GPU model execution
would publish the same shared-page outputs; the BPF loop would consume them
for ordinary kernel TCP sends. It could eliminate the separate GPU network
CTA and its mapped ring/state traffic without changing model arithmetic.

This is more aligned with the requested reusable eBPF server boundary than
trying to tune a model kernel. It is a different placement of network control,
not moving TCP off the CPU: Linux TCP and the BPF loop still consume CPU.
It may permit identical model-controller SASS against native and a cleaner
transport-only comparison, but that equality must actually be built/checked.
No throughput, tail, total-CPU, generic-plugin or novelty win follows yet.

## What remains unproven before implementation or admission

No verifier acceptance or real application execution has been attempted.
A prospective implementation must establish bounded CQ/active-list access,
registered-region layout/user-address translation, CPU/GPU publication order,
partial sends and fd/peer ownership, safe slot reuse, corrected EOF pending
references, cancellation/stop/drain and actual task accounting. It should reuse
the existing admission/parser/backend computation rather than weaken protocol
semantics or insert a userspace request worker. Ordinary before/native remain
needed; old module results and this API audit cannot supply matched numbers.

The complete current timing result/review should first determine whether this
constructor or a smaller evidence-backed data-placement change is the strongest
next discriminator. If admitted, it needs its own fixed primary, ordinary
correctness/build/preflight and full matched source decision. Nothing here
changes the running four-condition plan, offsets, oracle, timeout or primary.

## Source preparation after this audit

A first private source draft is now preserved in kernel_owned_source_draft/:
registered CPU layout/state, BPF CQ/admission/reply/lifetime/timer controller,
host bootstrap/drain/cleanup and ordinary Make entry. The private mixed .cu
has exactly one include-name substitution; dispatch source bytes match current
production. No compile/verifier/runtime/performance/adoption evidence exists.
The source draft does not change the active matrix or its hypothesis. Its
purpose is to make a possible next constructor concrete for review, while
runtime work waits for the current integrated result and selection decision.

## Later engineering status

The separate [build record](kernel_owned_build_checks/engineering.md) now
preserves ordinary8/16 compilation, real verifier rejection/fixes and final
matching8/16 successful verifier-only loads. The initial draft above remains
historical/uncompiled; current private source is under
kernel_owned_build_checks/verifier_accepted_source/. No BPF link/listener/I/O
or model execution has occurred for this candidate and no default changed.
