# Private kernel-owned TCP source preparation

2026-10-16 UTC, same existing owning Workspace and OS temp. Source-only WIP.
Prepared shared CPU state/layout, BPF CQ/admission/reply/connection/timer loop
and host startup/registered-memory/attach/drain/cleanup. The model-page ABI,
model arithmetic and current production source remain unchanged.

No compile, verifier load, target integration, GPU experiment, correctness
qualification, source decision or performance admission has occurred. Existing
controller-stage acquisition has priority and remains byte-for-byte unchanged.
The prototype is not a completed implementation, scientific result or selected
transport. Actual build/verifier/reliability tests and a reviewed matched source
decision are required. Remaining risk includes readonly-config verifier bounds,
BTF initial-data mapping, lifetime/partial-send/cancel semantics and real cleanup.

Initial source self-review keeps the existing60us timer value but queues its
first SQE until the first BPF callback: verifier/JIT time cannot fill the CQ
with timer ticks before the controller runs. Actual dropped/overflow offsets
and terminal SQ/CQ balance are preserved rather than reported as synthetic0.
No compiler, verifier or runtime has yet checked this source.

Private source-native Make entry is prepared for default8/explicit16, using
only a private .cu include replacement and CPU-only transport header. A future
python3 build.py uses ordinary -dc/device-link/native targets and the new BPF
loop; it is NOT executed while the current matrix is collecting. Model
computation/dispatch source differs only in its host transport include name.
Actual SASS equality, BPF verifier acceptance and protocol behavior are unproven.
