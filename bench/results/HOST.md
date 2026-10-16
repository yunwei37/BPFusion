# Host under test

- CPU: Intel(R) Core(TM) Ultra 9 285K (24 logical CPUs, single NUMA node)
- GPU: NVIDIA GeForce RTX 5090, 32 GB, driver 610.57.04, CUDA 13.3, `sm_120`
- Kernel: 7.3.0-070300rc3-generic (`PREEMPT_DYNAMIC`), BTF + tracefs + bpffs present
- Containers/cgroup: full root in a privileged container, `panic=10 iommu=pt`
- Loopback only for the first probes; no DPDK/AF_XDP, no upstream NIC verified yet
  (no `eth*`/infiniband peers inspected beyond what the workspace exposes)


Onboarding observation,2026-10-16UTC:the installed compiler at
/usr/local/cuda/bin/nvcc is CUDA toolkit13.0,V13.0.88.
The13.3 displayed by the driver is its CUDA compatibility level,not the
installed toolkit version. The qualified Python vLLM environment separately
uses Torch2.13.0+cu129 and CUDA-Python12.9 bindings.
