# Real repeated-library graph qualification

2026-10-17 UTC. Before network-performance acquisition, both cuBLAS8x8FP32
and cuFFT32complex64 pass repetitions1/16/256 on ordinary kernel/native
default8 graph libraries. All12cells pass182checks/cell (2184total),including
180exact numerical outputs,2intended wrong-shape rejects,connection reuse,
ring wrap,pipelining,half-close,RST/fresh request and SIGTERM with queued work.
The stopped-response prefix and trailing partial word are retained; canceled
unobserved work is not called completed. Kernel rings stop normally with
pending/error/reserved/dropped/overflow0,SQ/CQbalanced,accepted=closed.
No model or library arithmetic kernel is changed.

The example now factors capture_graphs and accepts optional --repeat,default1.
All graph/tensor lifetimes remain caller-owned. Shared graph dispatcher and
normal libraries are unchanged. Full commands,rows,input/output hex,server
logs,cleanup receipts and summary are in qualification/. All actual checks
remain in graph_work_qualification.py,with source provenance in receipts.

graph_work_calibration.stdout retains five100-host-replay CUDA-event batches
per operation/repetition. Host submission gaps are included; this is not
pure device-launch time or whole-request latency. Served graphs have no timer
nodes. Performance acquisition/confirmation is still pending at this milestone.
