# Paper artifact validation

2026-10-17 Los Angeles. Sole-thread work; paper entry revision ad7982f.
The paper source/PDF are unchanged by this thread.

**Current status: complete with one reported paper rounding difference.**
Final published replay3d551783:134PASS,1MISMATCH,0PAPER_CHANGED,
196.142s in a new plotting-only environment without Torch/vLLM or visible GPU.
Both current graph and LLM smokes pass. Detailed historical checkpoints below
are retained as development provenance,not outstanding work.

## Initial development checkpoint (historical)
- All eight archived primary raw-data stages are executable; original main
  graph raw replay checks 90 cells.
- A development check using those already-recomputed stage outputs produces
  121 numerical passes and one Figure3 rounding mismatch. This is not the
  final clean acceptance.
- A new Python3.12 environment installs Matplotlib3.11.2/NumPy2.5.4 and
  torch2.13.0+cu129. Ordinary current-source graph smoke passes4cells/
  64exact replies in16.255s,normal shutdown and detach.
- Initial explicit libbpf1.6.3 header selection fails on bpf_stream_vprintk.
  The successful build uses existing system1.3 headers and1.6.3 runtime.
- First parser attempts visibly reject table headers and P99's literal99;
  corrected extraction excludes headers and metric names. No archived
  data or paper number is altered.

Next: publish the replay entrypoint, download/export a clean source into a new
directory, execute unmodified full replay and GPU smoke there, record exact
input availability and cleanup. Completion is not claimed at this checkpoint.

See [ARTIFACT](../../../ARTIFACT.md) for the complete map and commands.

## Clean offline milestone

Public download: HTTP200, canonical remote discovered after project rename;
2,473,754,167 compressed bytes,4,240,192,222 regular-file bytes. Base archive
7ccc1850 is updated with byte-verified public forward files to a1f79236,
including the paper owner's06d2c598 rename. Source executes as clean-source,
without Git metadata,original private runtime helpers or Python site packages.

The full unmodified offline command exits1 in205.397s with a completed
comparison:131 PASS,1 MISMATCH,0 PAPER_CHANGED. The only discrepancy is the
documented Figure3 residual rounding. No raw-validation exception occurred.
Both PNG/PDF data figures are regenerated; legends are visually checked.

7182 actually read input files (1,270,399,873 compressed/on-disk bytes) are
tracked,downloaded and match committed object sizes. No missing raw input.
Both original perf binaries decompress with valid PERFILE2 headers.
See input-availability.json,inputs.txt and publication receipts.

Independent clean graph smoke:4cells/64exact replies,PASS in16.352s,normal
exit/detach. Host kernel/CUDA and installed libbpf are reused prerequisites;
source and Python environment are new. The pinned public model checkpoint
is cached for the optional new LLM smoke.

The first LLM harness correctly receives32 successful64-token native16 replies
plus8warmups but incorrectly expects128. Its assertion failure and normal
40-admission shutdown are retained. The archived transport client defines its
preflight as32;the later capacity client uses128. Correct the new harness/
instructions,not the immutable client. Fresh four-condition LLM smoke remains
pending at this milestone. The original paper is untouched by artifact commits.

## Final acceptance

- [validation.json](validation.json) records the final135 numerical comparisons,
  new source/environment, exact command exits and evidence paths.
- [comparison.md](comparison.md) shows every number; exit1 is the completed
  Figure3 rounding report,not a replay exception.
- [input audit](input-availability.json):7182 public committed reads/no missing
  data; both original perf binaries also validate.
- [graph smoke](graph-smoke.json):4ordinary cells/64exact replies,16.352s.
- [LLM smoke](llm-smoke.json):native16/kernel16/native32/official,128requests/
  8192tokens plus32excluded gen1 warmups,185.343s. Every server exits0.
  One native16 finite-reference flag is retained; protocol pass is not universal
  exact trajectory fidelity. Raw clients,workers and failed first harness
  attempt are retained in llm-smoke-raw/ and llm-first-harness-attempt/.
  Server log copies omit API-key configuration lines; client records are intact.
- [PDF spot check](pdf-consistency.json):four pages and ten key published values
  agree with the TeX-replayed results.
- [runtime receipt](runtime-safety.json):original PID starts preserved,GPU apps/
  BPF pins/test keys/semaphores absent. A transient kubelet502 interrupted a
  later control call;existing SSH/exec returned with the same host boot/Pod/PIDs
  and attached healthy PVC. No host/Workspace mutation or GPU rerun occurred.
- [owner review](self-review.md) and [relative links](authored-link-audit.json)
  complete;no delegated agent,PR,new CI or serving-default change.

The original 205.397s full clean replay and296.989s plotting-only replay precede
the final196.142s run. They agree numerically;the final version adds three prose
checks and derives the failure denominator from raw attempts. Their wall times
are validation timings,not paper performance results.
