# Reproduce the peer identity intervention

All build, model and server execution uses the original owning Workspace.
See plan.md for pinned environment/model/source identities, actual normal
Make commands, the three conditions, same-compute baseline and full matrix.
build_records contains expanded normal commands and terminal statuses.
client_job.json is the bounded private remote client, deleted on closure.

The Windows-side driver orchestrates only the Workspace and disposable client
through the existing spark-manage scripts/kubectl-home.ps1 entrypoint:

    & <OS-TEMP>/run_peer_identity_matrix.ps1 -ClientPod <owned-client> -ServerIP <Workspace-Pod-IP> -Preflight
    & <OS-TEMP>/run_peer_identity_matrix.ps1 -ClientPod <owned-client> -ServerIP <Workspace-Pod-IP>

The prepared script is the archived run_peer_identity_matrix.ps1. It uses the
unchanged frozen remote_async_client/config/offsets and existing resource
observer from0074. Actual server source receipts include the correct immutable
before/candidate header and identical BPF/model sources. Artifact Git HEAD is
not source-adoption proof. No profiler overlaps preflight/full performance.

After terminal full collection, CPU-only replay from this directory:

    python3 peer_identity_analysis.py peer_identity_full

Acquisition/replay stdout must match. For traced qualification from its
qualification directory, set PYTHONDONTWRITEBYTECODE=1 to avoid generated
checkout cache and run the reader-only gzip-compatible analysis:

    python3 protocol_analysis.py qwen_peer_identity_protocol8.jsonl
    python3 protocol_analysis.py smol_peer_identity_protocol8.jsonl

The absent plain filename resolves to its losslessly compressed .gz archive.
Compare stdout to each model's archived analysis.stdout/archive_replay.stdout.
Acquisition versions of both readers are retained and differ only in
compression input handling; mathematical/fixed oracle logic is unchanged.
Generic and ordinary lifecycle raw records state their finite cancellation
and analytic-oracle scope. No source promotion follows from a smoke pass.

## Source selection and cleanup

This candidate is not selected. Current executor/io_uring_tcp.h matches
io_uring_tcp.before.h and the previously accepted0074 source. Reproducing the
candidate requires the archived candidate header/diff in the owning Workspace,
normal Make builds and the recorded same-capacity ABI; a current main build
alone produces the selected before condition. Do not treat artifact-publication
HEAD as a candidate source revision. See selection.md and result-review.md.
client_cleanup.json records actual Job/Pod deletion; cleanup_runtime.json
records preserved original sessions and no remaining GPU applications/pins.
