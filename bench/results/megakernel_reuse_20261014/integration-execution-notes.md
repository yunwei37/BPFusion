# Integration and runtime execution notes

The previous turn completed implementation and c1/c8 finite-set serving checks
on baseTorch2.14.1+cu130. The stronger tests/resident_qwen.py eager-HF exact
diagnostic fails on the third gen64 output. Native170 per-step and persistent
AMK independently reproduce that same output. The failed diagnostic remains
failed; no references are expanded. The admitted experiment uses the
pre-observation0045 whole-output pools, which remain byte-identical.

Both backends now share temporaryTorch2.13.0+cu129, Transformers5.17.0 and
vLLM0.31.0. Installed base packages are unchanged. AMK's upstream native JIT
and the graph builder use existing nvcc13.0; vLLM device code and its host
bridge retain the earlier qualified CUDA12.9 runtime linkage. Each actual
backend/compiler/runtime is reported; a common Torch package does not mean
identical GPU kernels, and cross-backend effects are not eBPF effects.

The original plan's native AMK alternative is implemented as the same
resident private-bank dispatcher/model graphs with existing efficient epoll
TCP, preserving identical computation and GPU scheduling across the
transport control. It does not add a host per-token launch loop. The
candidate replaces network request handling with the existing upstream
sleepable eBPF/io_uring loop. Upstream whole-generation K is used asK=1
per graph so the existing system-scope per-token publication and final-CQ
reclamation remain the sole serving lifetime path. No raw VM/math is edited.

The temporary protocol adapter derives from bench/vllm_serving.py. It only
selects the two AMK launchers/readiness strings and verifies the actual
qwen_graph.cu graph accounting plus transport counters instead of nonexistent
vLLM GPU counters. All fragmentation/concurrency/rejection/wrap/pipeline/
half-close cases, frozen whole-output checks and syscall checks stay intact.
The archived diff makes this transformation inspectable. Numerical
set-membership scope is explicit and remains weaker than exact eager-HF
or current trajectory replay.

The existing hf_loop lifecycle driver is adapted to the same planned literal
prompts and unchanged frozen pools; all eight long idle periods, invalid
HTTP/binary handling, reset after first token, later exact output and stop
with generation/receive/accept pending remain. It checks complete frozen
sequences or already-frozen prefixes, not candidate-authored answers.

The full source-native serving matrix will retain three backends, five
process blocks, fourgen/c cells and64 measured requests/cell. Its first five
permutations balance the AMK transport order3/2; cell order rotates by block.
The analyzer retains arrival-derived metrics, actual worker brackets,
queues and all five process differences with nominal t95df4. No new
performance cutoff or favorable rerun is introduced. Full source and
commands will be frozen onmain before collection.

## Native lifecycle accounting adapter correction
The first native lifecycle driver completes all32 selected request/check
actions and exits0 with zero graph errors, but reports passfalse because
the new native predicate mistakenly expects32 completed transmissions.
userspace_tcp.h exits its service loop on SIGTERM, disconnects peers and
reports completed before qwen_graph.cu sets stop, synchronizes CUDA and
frees the anonymous page. The final gen64 request is intentionally stopped
after one token, so it is published but not a completed TCP reply. Native
accounting must therefore be published32/completed31/rejected10/accepted13
for this specific workload, unlike loop cancellation accounting. Preserve
the first failed predicate and rerun the native lifecycle actions with this
source-backed correction, then execute the loop case. No model/transport
code, request action, output oracle, runtime or numerical criterion changes.
