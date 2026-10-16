# Temporary benchmark cleanup

2026-10-16 approximately14:00UTC. Before deletion, re-read Job UID
d943952e-bfe4-430a-9768-f0334644ed03 and client Pod UID
06030314-a037-481e-83d8-f95e51a4ea4f, matching its controller owner.
Client restartCount0. All original measured records recovered before deletion;
independent reviewer confirmed no additional client data needed.

Through scripts/kubectl-home.ps1, deleted only coder Job
bpfusion-sustained-client-20261016. Delete returned success; wait --for=delete
on bpfusion-sustained-client-20261016-s2g8m returned condition met.
Subsequent get --ignore-not-found for both Job and Pod returned no object,
command sequence exit0. No persistent benchmark service, scheduler, public
endpoint, network or host tuning was retained.

post_source_runtime_receipt.json records no owned pins or GPU compute process
and unchanged original Coder PID1/10909 starttimes. The matching development
Workspace and its files/session remain. No foreign workload was stopped.
Private source/build/runtime files remain only in Workspace OS TEMP as
reproducibility/debug inputs, not a running service or new development checkout.
