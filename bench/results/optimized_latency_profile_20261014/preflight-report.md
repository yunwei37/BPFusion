# Actual preflight and host qualification
Qwen ordinary and profiled cases both terminate normally with8 checked gen1
requests each (4 excluded warmups each), actual server exits0 and drained SQ/CQ.
The replay analyzer exits0. Profile coverage is2168 model kernels (271/request)
and8 graph memcpy records, matching actual recursive body/head catalogue.
Ordinary measured TTFT1.40864975ms; profiled1.4825175ms. Profiled model span
1.2748325ms, kernel union1.135072021484375ms. These are setup observations,
not a completed full-run result.

At06:22:53 actual host journal records an NVRM refcnt state1 request failure
with status0x56 during profiled bootstrap. Official NVIDIA nvstatuscodes.h
maps0x56 to NV_ERR_NOT_SUPPORTED; that mapping does not establish the failed
reference's purpose or cause. Read-only diagnosis at06:26:22 verifies nvidia-smi
-q exit0, Recovery Action None, no compute applications, no Xid/new OOM/storage
fault in the selected current-window journal, and unchanged boot. Actual
profile/model exits and all expected activities are normal. No driver, GPU
reset, permission or power mutation is justified or performed.

Resume the planned finite supporting observation, retaining this warning and
every later health bracket. Do not label the host journal clean or infer zero
profiling effect/continuous isolation. Per-executor observations remain required.
Command: /usr/bin/python3 TEMP/case.py qwen 0 CONDITION preflight
Replay: /usr/bin/python3 TEMP/analysis.py TEMP preflight
Official status mapping:
https://raw.githubusercontent.com/NVIDIA/open-gpu-kernel-modules/main/src/common/sdk/nvidia/inc/nvstatuscodes.h
