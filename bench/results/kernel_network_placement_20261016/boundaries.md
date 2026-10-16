# Test boundary and restoration

Requested bounded benchmark under spark-manage AGENTS8. Original bpfusion-dev
Workspace/PVC and PIDs1/10909 remain. No active GPU service or client Job remains
after0076; no service pause/restoration, new credentials, model or host settings.
Original foreign setup_env.sh and unrelated busy lab CPU workload are preserved.
Server uses existing lab RTX5090 allocation in the owning Coder Workspace.
Source/build/test occur there; the disposable remote-client Job has no GPU,
host pin, resource limits or credentials and excludes the current Workspace
host via its actual Workspace identity. Client address/image/UID/placement are
recorded live. Private cluster TCP only.

Individual actual server commands retain300s qualification/600s acquisition
lifetime and explicit signal/drain end. The Job holds only the benchmark client
between cells and is removed after originaldata transfer and terminal analysis,
including failure cleanup. No durable service/schedule/framework is retained.
No global investigation deadline or changed timeout/oracle.

Stop owned process groups withSIGTERM through existing lifecycle, wait for
server terminal/drain and run existing stream-detach/remove owned BPF pins.
Delete only actual matching client Job UID and verify Job/Pod absence.
Verify original PIDs/startticks, source/WIP/main synchronization, GPU apps/pins,
node Ready and disk/crash state; retain only requested nonsecret artifacts.
Outcome is passed-restored, failed-restored or restore-blocked at closeout.
