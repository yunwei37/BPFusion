# Default8 qualification and ordinary-source adoption

All6 commands pass, terminal2026-10-16T11:04:40UTC:
two model protocol programs each exercise both transports, plus four ordinary
lifecycle cases. Protocol totals2560 outcomes,1036 intended rejections and
93504 exact tokens independently verified by full history and fresh metadata
replay. Actual mixed widths1..8 execute.

Ordinary lifecycle totals352 outcomes:2728 checked complete tokens and218
observed prefix tokens;94 queued/reset cancellations are explicitly unobserved.
Qwen loop/native prefixes91/2, Smol123/2. Reuse, idle, HTTP400 recovery, binary
rejection, half-close, RST, queued RST and mid-output SIGTERM/queue drain pass.
Partial-output checks remain prefixes, not full-response accuracy claims.

The tested private .cu is byte-identical to adopted executor/vllm_mixed.cu.
Normal repository Make builds default8 and explicit16 ordinary/traced targets,
BPF and loader successfully in tcp_sourcebuild8/16. Source build commands/logs
are here; before controls remain in their separate existing directories.
Only TCP_NODELAY include and checked listener option are adopted. Old
homogeneous controls and generic graph source retain their original behavior.

cuobjdump --dump-sass comparison of before/candidate GPU code is byte-identical
for both transports at16, recorded in sass-comparison.json files. The measured
intervention changes host socket setup, not model or GPU network kernels.

Raw files are lossless gzip. Acquisition analysis sources are preserved as
*.acquisition.py; archived analysis files add only transparent gzip input,
with unchanged metric/replay logic. Both archived CPU analyses reproduce
acquisition stdout bytewise, without the temporary GPU runtime:
python3 bench/results/tcp_nodelay_20261016/qualification/protocol_analysis.py bench/results/tcp_nodelay_20261016/qualification/qwen_nodelay_protocol8.jsonl
and substitute smol for the second model. No fixture/oracle/tolerance is changed.

All qualification servers stop and owned pins/GPU apps are empty at its endpoint.
Shared TEMP is retained for the separately authorized remote/resource task;
original Coder/build paths and unrelated tools/setup_env.sh remain preserved.
