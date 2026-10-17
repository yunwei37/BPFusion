# Paper artifact validation

2026-10-17 Los Angeles. Sole-thread work; paper entry revision ad7982f.
The paper source/PDF are unchanged.

Initial development:
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
