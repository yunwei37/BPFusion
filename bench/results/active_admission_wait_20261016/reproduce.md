# Reproduce the recorded comparison
Run CPU analysis with Python3 and the archived lossless raw data:
python3 bench/results/active_admission_wait_20261016/active_wait_analysis.py bench/results/active_admission_wait_20261016/active_wait_full

The analysis requires all15 cells. It retains failures, finite-reference
disagreements, scheduling lag and shared resource scopes; it emits one CPU
primary and all declared nominal paired secondary contrasts. It is not a
fresh numerical model evaluation. For the fixed128-attempt setup check, use
the active_wait_preflight directory and append --preflight.

Protocol CPU replay accepts the base .jsonl name and reads its gzip archive:
python3 bench/results/active_admission_wait_20261016/qualification/protocol_analysis.py bench/results/active_admission_wait_20261016/qualification/qwen_active_wait_protocol8.jsonl
Use the corresponding smol base name for its second replay. Original
acquisition analyzers remain separately; reader-only gzip/path shims do not
change the arithmetic or oracle.

Normal Make commands, actual argv and outputs are in build_records/.
Before/candidate loop snapshots differ only in the may_idle condition.
Each binary's absolute BUILD binding must point to its own matching BPF
objects. The immutable before builds come from0072 normal-source integration;
candidate builds compile the actual canonical one-line WIP via normal Make.
Artifact Git HEAD identifies record publication and is not proof of adoption.
Reuse the documented runtime/model revisions and frozen gamma schedules.
Do not change model math, timeout, pool, flags or schedules to make a result pass.

The actual remote command is the archived run_active_wait_matrix.ps1 with
-ClientPod <owned-client> -ServerIP <actual-Workspace-PodIP>; append -Preflight
only for the setup matrix. It runs inside the owning Workspace and uses the
bounded disposable client. Historical absolute TEMP/Pod paths identify this
run and must be adapted to the actual matching environment. See plan.md for
scope, startup/measurement/drain, all-attempt metrics and cleanup boundary.

The separately labeled post-matrix profiler uses run_active_wait_profile.ps1.
Its samples are supporting mechanism context, not a replacement performance
cell or an unprofiled speed estimate. profile_summary.py decodes descriptive
period-weighted categories from the archived standard perf script output.
