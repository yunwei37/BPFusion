# Reproduce current controller stage timing

Plan.md fixes the question, conditions, metrics, schedules, correctness and
scope. Private sources are the archived instrumented .cu/.h, whose before
snapshots equal selected0074 production source. No production source is edited.
The actual normal Make rule is used with only source path redirected, explicit
executor include path, BUILD temp path and16slots. No BF_IO_COALESCED is defined.

In the owning Workspace, copy the archived private .cu/.h into
/tmp/bpfusion-mixed-integration-n4cog5c6/controller_stage_sources, then use
controller_stage_build.py with its archived Makefile. Environment.json/models/
client assets are the unchanged pinned records linked in0074/0075; do not
confuse their artifact Git HEAD with the actual source snapshot.

The Windows orchestration entry point is run_controller_stage_matrix.ps1 with
-ClientPod <owned bounded client> -ServerIP <Workspace-Pod-IP> -Preflight,
then without -Preflight. All client/config/offset files, including the128-prefix
preflight file, are copied before either. The script uses existing kubectl-home
and runs source/build/model/replay only in the owning Workspace. The remote
client uses the archived bounded Job lifecycle; both Job and Pod are deleted
on closure. No schedule, new persistent helper or host setting is created.

After collection, CPU-only archive replay:

    PYTHONDONTWRITEBYTECODE=1 python3 controller_stage_analysis.py controller_stage_preflight --preflight
    PYTHONDONTWRITEBYTECODE=1 python3 controller_stage_analysis.py controller_stage_full

The reader resolves absent .jsonl inputs to their lossless .jsonl.gz archives.
Full instrumented server termination includes existing source-native two-pass
replay. Its literal stdout and trace/reference/fresh-metadata files are preserved.
Stage counter ordering/clock, launch histogram and every observed client token
are audited against those existing logical records. Replay is a finite model-
trajectory oracle, not a new general model-quality result.
