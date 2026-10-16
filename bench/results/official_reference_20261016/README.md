# Current official serving reference

The [plan](plan.md) and [plan review/follow-up](plan-review.md) admit one Qwen
whole-service comparison, retaining kernel/native same-executor controls.
Source-selected mixed executors are frozen at45f0ec2 with the unchanged
close-scan header. The official server keeps optimized defaults and the same
GPU/checkpoint/FP16 runtime; different cache/capacity/API/trajectories prevent
an eBPF causal claim against it.

Real preflight2 passes3 executors/6 cells/96 measured requests/6144 tokens plus
24 gen1 warmups. Auth missing/invalid checks401; actual FLASH_ATTN version2,
torch.compile and CUDA Graph capture engage. Driver analysis independently
reruns byte-identically from this archive. Preflight is dependency evidence,
not the five-block performance result.

Preflight1 preserves a completed40-reply kernel prefix, then a duplicate utc
keyword in the collector's stop receipt raises TypeError and its cleanup
logging raises the same error. The actual executor exits0 with drained rings.
No native/official sample is collected. Original source/raw/tracebacks are in
failed_preflight1/. The stopped own pins are explicitly removed; the repair
renames stop_utc and performs pin cleanup before emitting cleanup records.
No workload, timeout, reference pool, metric or model source is changed.
The full corrected3-condition preflight is rerun, not treated as a partial pass.

Official parent wait0 does not imply graceful children: its server logs force
killing EngineCore during shutdown and a semaphore warning. The harness
reports no own forced cleanup and no remaining group. GPU/pins are empty
after preflight. These warnings stay visible.

Portable CPU replay from repo root:
python3 bench/results/official_reference_20261016/official_analysis.py bench/results/official_reference_20261016/preflight2/preflight.jsonl
The logical .jsonl path resolves a lossless .gz sidecar. Actual acquisition
scripts keep their original TEMP/source/model-cache paths. The full fixed
15-executor/30-cell matrix is the next pending stage; do not report a partial
prefix or preflight performance as a completed comparison.
