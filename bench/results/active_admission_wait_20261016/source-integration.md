# Ordinary-source adoption

2026-10-16 UTC. Retain exactly the already built and qualified one-line
candidate condition in bpf/uring_loop.bpf.c after the complete matrix and
independent result review. Current file byte-matches
uring_loop.candidate.bpf.c; no additional code or build flag is introduced.

Normal Make default8/explicit16 builds, actual GPU SASS equality, BPF
disassembly/bindings, two-model protocol/dual replay and ordinary
idle/reuse/reset/partial-stop checks already executed this exact canonical
candidate. Generic cuBLAS/cuFFT loop/native checks also passed. See
qualification.md/build_records; repeating unchanged acceptance is unnecessary.
No new source change occurred after qualification or during measurement.

Adopt this as a measured process-group CPU repair, with the complete
before/candidate/native throughput and tails retained. This does not select
a faster transport or alter the shared model arithmetic, default8 slots,
ABI,60us timer, network ownership or native baseline. Roll-forward handling
would be required for any future defect; no commit is undone here.
Temporary Job/Pod cleanup and preserved original Workspace/PIDs/WIP are
recorded in client_cleanup.json and cleanup_runtime.json.
