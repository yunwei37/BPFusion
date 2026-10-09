# Finding 0011 — external HTTP baseline (vLLM) vs the bpfusion paths

Status: measured on 2026-10-09, same host as `bench/results/HOST.md`.
Raw log: `bench/results/http_20261009T135404Z.txt` (0.5B); the bpfusion numbers
this is compared against are in
`bench/results/llm_Qwen_Qwen2_5-0_5B-Instruct_20261008T080414Z.txt` (finding
`0010`).

## Question

The bpfusion LLM path so far compares against an **in-process HuggingFace
`model()` loop** (`0010`). That is not the ordinary serving stack a real user
runs. This measures the fair external baseline: a standard OpenAI-compatible
**HTTP server (vLLM)** on the same model, with the same TTFT/TPOT definition the
bpfusion clients use (request write -> first content token; mean inter-token
gap).

## Setup

- `python3 -m vllm.entrypoints.openai.api_server --model
  Qwen/Qwen2.5-0.5B-Instruct --dtype float16 --max-model-len 512`.
- Client: `tools/llm_http_client.py` — a raw streaming `POST
  /v1/chat/completions`, `temperature 0`, `max_tokens 32`, reading SSE frames and
  timing only frames with a non-empty `delta.content`.
- Driver: `bench/run_http.sh Qwen/Qwen2.5-0.5B-Instruct 32 8`.
- 8 rounds after a 4-token warmup, one request at a time (batch 1, no
  concurrency), `prompt = "The capital of France is"`.

## Result

| path | TTFT p50 (µs) | TPOT p50 (µs) | decode engine |
|---|---|---|---|
| **vLLM HTTP** (this log) | **6203** | **852.7** | vLLM (CUDA-graph/paged-attention decode) |
| bpfusion direct (in-process HF, `0010`) | 9146 | 8347 | naive HF `model()` per step |
| bpfusion UDP page path (`0010`) | 9123 | 8299 | naive HF `model()` per step |
| bpfusion TCP reply socket (`0010`) | 11638 | 8383 | naive HF `model()` per step |

TTFT spread within the vLLM run: min 5805 / max 8489 µs; TPOT min 753 / max 1720
µs. The bpfusion numbers are single runs from `0010` (different date); treat the
µs-level comparison as indicative, not as a same-run A/B.

## What this means (honest scope)

- **The path overhead is not the dominant term.** bpfusion UDP adds ~0 µs of
  TTFT and ~-48 µs of TPOT over its own direct baseline — i.e. the
  kernel→page→executor path is within noise of in-process for this prompt. The
  large gap to vLLM is **decode**, not transport: vLLM is ~**9.8× faster per
  token** (0.85 ms vs 8.3 ms) because the naive HF loop re-runs the full model
  per token with no CUDA graphs / paged attention / batching.
- So the correct current claim is: *bpfusion moves the request and the token
  stream through the eBPF/kernel page path with negligible added latency; its
  current decode engine is ~10× slower than a production serving stack.*
  Closing that decode gap (GPU-side sampling, continuous batching, CUDA graphs)
  is a separate, not-yet-done piece of the goal — the page path is orthogonal
  to it.
- The vLLM TTFT (6.2 ms) is below the bpfusion direct baseline (9.1 ms): vLLM's
  optimized prefill beats a naive HF prefill even with HTTP/SSE on top. This is
  a decode/prefill-engine effect, not a transport effect.

## Not measured here

- Concurrency: this baseline is batch-1 sequential, matching the bpfusion
  `llm_bench` runs; vLLM continuous batching is not exercised.
- The 1.5B / Qwen3-1.7B HTTP comparison (only 0.5B here); the bpfusion
  size-comparison lives in `0010`.
