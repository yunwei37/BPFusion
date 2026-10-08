# Finding 0010 — matched model-size comparison (0.5B / 1.5B / Qwen3-1.7B)

Status: measured on 2026-10-08, same host/executor, only `--model` differs.
Raw logs: `bench/results/llm_Qwen_Qwen2_5-0_5B-Instruct_20261008T080414Z.txt`,
`bench/results/llm_Qwen_Qwen2_5-1_5B-Instruct_20261008T080351Z.txt`,
`bench/results/llm_Qwen_Qwen3-1_7B_20261008T080626Z.txt`.

The goal asks for a matched larger-model comparison. Qwen2.5 has no 1.7B
checkpoint — **1.7B is Qwen3**, which is a different architecture (Qwen3-1.7B
uses a longer config and its own chat template). Both a same-family upsize
(**Qwen2.5-1.5B**, 3× the 0.5B parameters) and the literal goal size
(**Qwen3-1.7B**) were run through the exact same executor and benches
(`bench/run_llm_model.sh <model> …`), fp16, batch 1, gen=32, so the only
changed variable is the model.


## Results

| model | path | TTFT p50 | TPOT p50 |
|---|---|---|---|
| Qwen2.5-0.5B | direct | 9146 µs | 8346.9 µs |
| | bpfusion (UDP) | 9123 µs | 8299.1 µs |
| | bpfusion-tcp | 11638 µs | 8383.1 µs |
| Qwen2.5-1.5B | direct | 10865 µs | 10146.3 µs |
| | bpfusion (UDP) | 10852 µs | 9884.6 µs |
| | bpfusion-tcp | 13128 µs | 9994.2 µs |
| Qwen3-1.7B | direct | 12993 µs | 12685.9 µs |
| | bpfusion (UDP) | 13075 µs | 12742.8 µs |
| | bpfusion-tcp | 15685 µs | 12716.4 µs |

1. **The packet→page→GPU→page path adds ≈0 at TTFT and ≈0.04–0.26 ms at TPOT,
   for both models.** bpfusion-vs-direct TTFT differences (23 µs, 13 µs) are
   inside run-to-run noise; TPOT is 0.6 % (0.5B) and 2.6 % (1.5B) *faster* on the
   page path (the direct path re-tokenizes and re-allocates per call). The path
   is not a function of model size.
2. **The TCP reply adds +2.27 ms (1.5B), +2.49 ms (0.5B), +2.61 ms (Qwen3-1.7B)
   at TTFT and nothing at TPOT** — the same one-time reply-setup cost seen in
   `0009`, and it does not grow with the model either.
2b. **Qwen3-1.7B behaves like the others on the path** (UDP vs direct TTFT
   12993→13075 µs, TPOT 12686→12743 µs, i.e. within noise), which is the useful
   result: the ingress/page path is model-agnostic even across architectures.
   Its decode (12.7 ms) is slower than Qwen2.5-1.5B (10.1 ms) despite similar
   parameter count — the two models are not the same work, so only the
   *path-overhead* comparison transfers, not a cross-family speed ranking.
3. **Decode is the model-dependent term and scales sub-linearly:** TPOT
   8.35 ms → 10.15 ms for 3× the parameters (1.22×). At batch 1 the 5090 is
   nowhere near compute-bound for a 1.5B fp16 model, so the extra parameters cost
   far less than 3×; the honest conclusion is that single-stream TPOT is
   dominated by per-step launch/overhead plus memory traffic, not FLOPs.
4. **Absolute numbers are not a serving claim.** As in `0005`/`0007`/`0009`: host
   Python `transformers`, batch 1, `argmax` sampling, no KV-cache paging. TTFT ≈
   prefill + first decode; TPOT ≈ single-token decode. The comparison that this
   finding supports is *relative* (model size, path overhead) on one host.

## Ingress counters

Both runs: `llm magic` matches requests, `llm busy=0` (no ring drops),
`drops=0`, and the TCP counters (`tcp dest`, `tcp magic`) match the TCP portion
of the client's packets only. No self-loop, no stray acceptance (the
`BF_PORT` guard from `0009`).

## Reproduce

```
make
./build/bpfusion_load attach lo
./bench/run_llm_model.sh Qwen/Qwen2.5-1.5B-Instruct 100 32 6
./bench/run_llm_model.sh Qwen/Qwen2.5-0.5B-Instruct 90 32 6
./bench/run_llm_model.sh Qwen/Qwen3-1.7B 110 32 6
