# Host under test

- CPU: Intel(R) Core(TM) Ultra 9 285K (24 logical CPUs, single NUMA node)
- GPU: NVIDIA GeForce RTX 5090, 32 GB, driver 610.57.04, CUDA 13.3, `sm_120`
- Kernel: 7.3.0-070300rc3-generic (`PREEMPT_DYNAMIC`), BTF + tracefs + bpffs present
- Containers/cgroup: full root in a privileged container, `panic=10 iommu=pt`
- Loopback only for the first probes; no DPDK/AF_XDP, no upstream NIC verified yet
  (no `eth*`/infiniband peers inspected beyond what the workspace exposes)
