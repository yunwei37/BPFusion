# Mixed scheduling is available through ordinary source targets

The qualified mixed prefill/decode dispatcher is now ordinary source:
[Cu](../../executor/vllm_mixed.cu), [upstream bootstrap](../../executor/vllm_mixed.py)
and [exact replay](../../executor/mixed_replay.py). The normal Makefile exposes
vllm-mixed-uring-loop, vllm-mixed-user-network-wait and vllm-mixed-trace.
Default capacity remains8; the guide uses the explicit module-free mixed
target. Old homogeneous, grouped, release and transport controls retain their
original source and semantics for reproducibility.

Cu/replay are byte-identical to the measured mixed candidate. Python changes
only repository/library discovery so ordinary symlinks work in any checkout.
No arithmetic, weight, precision, wait/timer, admission ownership or close-scan
change is introduced. The recent close-scan candidate is not adopted.

[Actual source integration evidence](../../bench/results/mixed_source_20261016/)
records successful normal Make8/16 builds, including both ordinary/traced
transports and matching BPF/loader/page ABIs. Default8 root-source protocol
runs on both Qwen2.5-0.5B and SmolLM2-135M complete2560 outcomes,1036 intended
rejections and93504 exact output tokens. All actual batch sizes1..8 engage;
captured-history and fresh upstream attention-metadata replay agree for all
completed trajectories, with ownership, clean shutdown and drained ring checks.
The finite128-entry reply sample truncates512 records per640-outcome kernel
executor; this is separate from model trace_overflows=0.

Four ordinary non-BF_TRACE lifecycle runs pass352 outcomes:144 per loop and32
per native model. They include idle/reuse, HTTP400/recovery, invalid binaryEOF,
half-close, first-tokenRST, loop backlogRST and mid-outputSIGTERM. All observed
complete outputs and incomplete prefixes match the unchanged finite
pre-observation reference set. Unobserved cancels remain incomplete.
See ordinary-summary.json for the exact complete/prefix token counts; these
are finite engineering checks, not universal numerical or reliability proof.

The actual source-backed commands and Python/library bindings are retained;
no original build, Coder session or unrelated tools/setup_env.sh is replaced.
No own pins remain after qualification. Explicit16 is compile coverage here;
the earlier same-Cu16 experiment and subsequent real16 API preflight have
their own scopes. This adoption selects the shared scheduler whose measured
mean-generation improvement occurs on both transports. It establishes no
eBPF performance advantage or new measurement beyond finding0065/0066.
[Getting started](../getting-started.md) gives the ordinary user path.
