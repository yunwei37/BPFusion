# Pending-admission service comparison

Complete collection and independent result review are preserved. The review
finds valid supporting finite-workload correctness and inconclusive primary
performance superiority. Production selection and owned cleanup/restoration
remain pending. This archive publishes the complete evidence on main; publication does not
select production behavior.
All ten qualification commands have completed.
Six real-model protocol executors have completed:
Qwen and Smol each have loop/native640-request cases and a non-loop622-request
compatibility case, totaling3804 requests and137952 independently replayed
model tokens. All four saved protocol analyses replay byte for byte from copied
data. These are correctness dependencies, not performance results.

Qwen loop/native lifecycle cases have also completed. Loop exercises120 actions
and78 connections, including a24-request RST backlog and64-connection stop.
Before RST16 requests are queued; before stop56 are queued. All connections
close and physical reservations clear. The56 unadmitted stop requests remain
explicit cancellations until owned map destruction. Native retains32 actions;
31 complete before stop. Partial prefixes/canceled responses are not complete
numerical deliveries. Smol loop lifecycle now passes with the same16/56 backlog
counts and120 actions/78 closed connections. Final native Smol lifecycle also
passes with32 actions and31 completions under stop, retaining its frozen
complete/prefix controls.

Real Qwen offered-load preflight attempt1 completed at10:27:15UTC:128 measured
attempts/8192 tokens plus16 gen1 warmups, both paths loss-free, kernel queued
peak16 and final queue/reservations0. The copied analyzer replays byte for byte.
Full collection started10:31:56UTC and ended11:21:07.991049UTC. Both model
drivers, fixed analyses and full wrapper exit0:20 executors,60 cells,15360
measured attempts,983040 successfully delivered measured tokens plus160 checked
gen1 warmups. Both paths have zero failed measured attempts for each model.
All seven copied-data CPU analyzers reproduce saved stdout byte for byte.

The predeclared64req/s first-token P99 differences (kernel minus native) are:

| Model | Mean difference ms | Nominal paired t95df4 ms | Failed-request censoring |
|---|---:|---:|---|
| Qwen | -14.175554 | [-53.893458,25.542351] | false |
| Smol | 25.391696 | [-29.697391,80.480783] | false |

Both intervals cross zero. Neither establishes the declared P99 superiority;
neither establishes equivalence. The private candidate remains unselected.
Zero failures on this finite workload do not establish arbitrary-overload
reliability or complete TCP backpressure. Keep all adverse effects and outliers.

## Purpose and sources

The reviewed plan tests a finite kernel-side FIFO waiting queue against
event-driven native TCP with identical reused FP16 vLLM graphs, eight model
banks, KV precision and prompts. The queue avoids the old constructor's immediate
drop on a reserved next physical model slot. It is finite, discovered from the
existing somaxconn authority, and is not complete TCP backpressure.

The complete earlier dropping-constructor result is
[offered_load_20261015](../offered_load_20261015/). It contains709 kernel timeouts
and none on native. It is retained as prior evidence, not rerun as a weak baseline.

- plan.md and plan-review.md retain the actual review and executable agreement.
- candidate/, native/, original/ and diffs/ preserve actual private sources.
- setup.py and build/install logs retain runtime/compiler bindings.
- qualification_initial/ retains the initial module-fixture failure and cleanup.
- implementation-notes.md records the existing-header-path build repair and the
  final-token/DONE fixture correction, including their scope and initial failures.
- protocol_*.jsonl, trace/reference sidecars and analysis outputs retain complete
  protocol cases; lifecycle_*/ retains complete/prefix and cancellation evidence.
- *_preservation_checkpoint.json records historical closed-data copies/replays.
- packages.json and package_comparison_0061.json show the same installed package
  versions as the prior measurement environment.
- host_before.json is a sparse actual pre-execution host observation, not proof
  of continuous exclusivity or fault-free hosting.

Only source and ordinary evidence are archived. Private runtime/build binaries,
CUDA JIT output, weights, downloaded packages and libbpf build trees are excluded.

## Reproduction

Use the original model revisions and pinned dependencies in models.json and
setup.py. Rebind recorded absolute temporary source/build paths to the rerun
directory, then run the normal setup, qualification, preflight and full scripts.
The module uses its supported KDIR override for the running-kernel headers
already installed in /usr/src; no host configuration was changed.

CPU analysis is portable and needs ordinary Python3, not CUDA or the private
runtime. Each sidecar name is derived from the supplied raw filename:

    python3 protocol_analysis.py protocol_qwen.jsonl
    python3 protocol_analysis.py protocol_compat_qwen.jsonl
    python3 protocol_analysis.py protocol_smol.jsonl
    python3 protocol_analysis.py protocol_compat_smol.jsonl
    python3 analyze.py preflight_qwen.jsonl
    python3 analyze.py full_qwen.jsonl
    python3 analyze.py full_smol.jsonl

These commands check saved replay evidence. Original backends performed the
independent upstream graph/KV/history replay before exiting; a CPU replay is not
another GPU numerical execution.

The planned full comparison fixes rates4/64/96,256 attempts/cell, five paired
blocks/model, gen64, absolute per-pair schedules, alternating path order and
rotating rate order. Its primary is connect-inclusive first-token P99 at64req/s;
any failed primary request censors superiority. Success-only timing, process
CPU, a dependency pass or a partial matrix cannot establish a complete-service
win. Actual client scheduling lag and all failures must remain visible.

## Shared host CPU observation before full

After preflight and before full, the sparse host CPU sample at10:29:41UTC
observed about21 CPU cores of process time across the24-core host. The top
sampled processes are named repl in a different Kubernetes cgroup
(podc21d7b4c-745d-469a-b804-32c7cdb0f79e), distinct from this Workspace.
No process/configuration was changed. host_cpu_before_full.json retains the
raw two-snapshot sample. host_before_full.json has no GPU compute applications,
the same boot and the same56 selected historical fault lines.

The planned matched comparison remains a finite shared-host service comparison
under recorded ambient load. It is not a controlled CPU-stress experiment,
exclusive-host latency, or causal attribution of all host CPU to this driver.
Original scheduling-lag and scheduled-origin metrics remain. The matrix,
primary, oracle, timeouts and path order are unchanged.

## Host timing scope

host_full_observation1/2 are post-measurement Qwen replay/teardown snapshots;
their phase records prevent interpreting them as serving isolation evidence.
host_measured_qwen_short and host_measured_smol_short have explicit monotonic
bounds inside actual measured cells, with host-to-namespace GPU PID ownership.
They remain sparse observations. host_after is78.767603s after full terminal,
with no GPU compute application, the same boot and56 unchanged selected
historical fault lines. None proves continuous exclusivity or all possible faults.

## Independently reviewed interpretation

See [result-review.md](result-review.md) for the complete independent report,
and [finding0062](../../../docs/findings/0062-pending-admission-tails.md) for the
public summary. At secondary Qwen/96, first-token P99 is280.139/1418.437 ms
kernel/native, with a nominal paired difference-1138.298 ms
[-1647.711,-628.885]. Median TTFT is worse134.386/30.120 ms; executor process
CPU increases, and throughput advantage is not established. Smol primary
outlier and its218.468 ms block scheduling-lag P99 remain. These observations
do not isolate syscall removal or prove a general service speedup.

plot_results.py reproduces pending_admission_results.png/.pdf and its data
from the two saved full analyses. Plotting dependencies were installed only
after full terminal, without changing existing measured package versions.
The private temporary runtime remains available for unfinished integration
work; no final cleanup or production selection is claimed here.

Archived source, diff and terminal-output whitespace is preserved verbatim.
Git whitespace diagnostics on those evidence files are not cleaned by altering
the recorded inputs; authored summary documentation passes whitespace checks.
