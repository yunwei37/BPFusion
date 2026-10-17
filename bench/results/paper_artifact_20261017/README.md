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
