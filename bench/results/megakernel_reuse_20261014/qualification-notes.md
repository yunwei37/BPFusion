# Native dependency qualification in progress
Original official F32 Smol CUDA example fails before output generation at the
host extension compile: installedTorch2.14 requiresC++20; upstream appends
-std=c++17 afterTorch's default-std=c++20. All CUDA objects compile.
Initial exit1/raw logs remain. A temporary adapter replaces only host
extra_cflags17with20 before the original cpp_extension.load. CUDA flags,
raw VM/source,model checkpoint,F32precision and upstream exactHF oracle
remain unchanged. Actual compatibility-adapted command is separately recorded.
This is dependency-only; neither compilation nor a laterF32pass substitutes
for plannedFP16/resident service qualification or measured performance.

Compatibility-adapted official example terminates0 at07:12:36UTC. Its CUDA
VM generates16 tokens exactly matching independent officialHFCPU/F32greedy.
No CUDA/VM/source/oracle edit. This qualifies only that one nativeF32example;
plannedFP16/persistent/device-controlled server paths remain unqualified.

FP16 native probe terminates0 at07:19:07UTC. Four literal prompts,gen1/64,
official per-step and experimental persistent paths produce16 complete
sequences/520 tokens. Every whole output is in unchanged pre-observation0045
HF FP16 references, and persistent equals per-step. Both use register/coalesced
cpasync0; no oracle expansion or VM/math edit. All103 upstream source files
compare byte-identically to the pinned archive. Actual after-host observations
retain earlier profiler warnings but no new selected Xid/OOM/storage fault and
no remaining compute app.

This is completed dependency qualification, not native latency/TPS or a server
performance result. Request-time GPU prefill, device-updatable argument flow,
dispatcher/graph co-residency, safe streaming/recycling and same-backend native
network comparison remain unimplemented/unqualified. TEMP remains owned for
continued integration, not a persistent service or infrastructure change.

## Integration update

The earlier unimplemented status above is historical. Current same-backend
c1/c8 TCP checks pass, but strict eager-HF qualification fails and the
performance experiment remains incomplete. See
[the current finding](../../../docs/findings/0048-reused-amk-dispatch.md)
for the implemented boundary and retained failure.

The strict case2 mismatch is independently reproduced by both official AMK
per-step and persistent execution under the current170-SM target/runtime.
Both exactly equal the new server output; the stronger eager-HF exact check
remains failed. See native170_comparison.json and the finding for scope.
