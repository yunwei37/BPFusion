# Paper

[bpf-gpu-server.pdf](bpf-gpu-server.pdf) is a four-page workshop-style report:
*Does Kernel-Owned Networking Make GPU Serving Cheaper? Lessons from an eBPF-Driven GPU Server*.
It summarizes the design, the same-executor comparison against native epoll,
the small-request experiment and why the kernel-owned path saves no CPU.

Every number in the report comes from the findings in [docs/findings](../docs/findings),
mainly 0065, 0070, 0072, 0073, 0074, 0078, 0080 and 0081, and their raw archives
under [bench/results](../bench/results).

Build with a TeX Live installation that provides `acmart`, `tikz` and `pgfplots`:

~~~sh
cd paper
latexmk -pdf bpf-gpu-server.tex
~~~

Blog posts based on the report:
[English](https://eunomia.dev/blog/2026/10/17/bpf-gpu-server/) and
[中文](https://eunomia.dev/zh/blog/2026/10/17/bpf-gpu-server/).
