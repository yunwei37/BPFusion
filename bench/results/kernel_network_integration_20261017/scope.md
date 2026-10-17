# Ordinary-source kernel-network integration scope

2026-10-17 UTC, entry main9d810138035ac3b0c1e6af64f5e4204ab73166fe.
This is engineering qualification of the user's ordinary-source and reusable-
backend goal, not another paper-performance experiment or a new primary.
0077/0078 already bound performance; no rerun of those matrices or model math
optimization is justified by source relocation.

The qualified private kernel-owned network is now executor/kernel_tcp.h,
bpf/kernel_tcp.bpf.c and shared CPU-state bpf/include/kernel_tcp_state.h.
Only each file's maturity comment changes from archived0077. Ordinary mixed
and opaque graph adapters choose this header with BF_KERNEL_TCP, leaving their
GPU dispatch and computation intact. Normal Make has explicit experimental
vllm-mixed-kernel-network[-trace] and graph-server-kernel-network targets.
Selected0074 targets/default8/ABI and model arithmetic are retained.
The new BPF program is omitted from generic default probes, like uring_loop.

Actual normal builds cover8(default)/16 with candidate,selected,native,trace
and matchingloader/BPF; graphcandidate/native/oldloop at8. Existing protocol/
dual graph replay and ordinary cancellation are reused for Qwen/Smol at8;
existing independent analytic cuBLAS8x8/cuFFT32 lifecycle checks are reused for
opaquegraphcandidate/native. These finite engineering checks do not establish
arbitrary model/kernel/plugin compatibility or universal numerical parity.
No runtime registry, model-specific kernel, daemon, persistent setting or
deployment is added. Build/test source paths and raw outcomes are retained here.

Source acceptance starts only after the complete ordinary official comparison
has stopped and its source/data/results have been pushed. Original PID1/10909,
foreign setup_env.sh, Workspace/PVC and other CPU work remain. The temporary
remote client has already been deleted. Final checks preserve original PIDs,
no own pins/GPU processes,default source meaning and all failed outcomes.
