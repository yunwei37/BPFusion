# Isolated short-output observation

Each model/path/trace condition has one process, 32 measured gen1/c8 requests and eight excluded sequential warmups. This is descriptive sensitivity, not neutrality, equivalence or mediation proof for the ordinary five-block matrix. Raw serving results and independent replay remain the authority.

| Model | Condition | Path | Measured model rounds | Client TTFT ms |
|---|---|---|---:|---:|
| Smol135M | ordinary | uring_loop_coalesced_original | 26 | 7.401656 |
| Smol135M | ordinary | userspace | 8 | 2.047399 |
| Smol135M | ordinary | uring_loop_coalesced | 9 | 3.097042 |
| Smol135M | trace | uring_loop_coalesced_original | 26 | 7.472170 |
| Smol135M | trace | userspace | 8 | 2.010669 |
| Smol135M | trace | uring_loop_coalesced | 19 | 5.751040 |
| Qwen0.5B | ordinary | uring_loop_coalesced_original | 26 | 8.922232 |
| Qwen0.5B | ordinary | userspace | 8 | 2.665664 |
| Qwen0.5B | ordinary | uring_loop_coalesced | 21 | 7.561046 |
| Qwen0.5B | trace | uring_loop_coalesced_original | 24 | 8.335259 |
| Qwen0.5B | trace | userspace | 8 | 2.565763 |
| Qwen0.5B | trace | uring_loop_coalesced | 14 | 5.359445 |

The candidate changes from9 ordinary to19 traced measured rounds for Smol, and21 ordinary to14 traced rounds for Qwen. These differences prohibit treating the traced batch history as authenticated ordinary full-matrix history. Association, unique IDs, every gen1 compute/release exactly once, warmup isolation, graph-counter agreement, unchanged output pool membership and independent trace replay pass for these selected observations.

The initial analyzer file-glob failure is retained with the corrected-source analysis. No serving executor or raw metric/oracle was changed or repeated.
