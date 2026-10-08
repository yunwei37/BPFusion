# Finding 0009 — TCP path (stream request in, stream tokens out)

Status: measured on 2026-10-08, same host as `bench/results/HOST.md`.
Raw log: `bench/results/llmtcp_20261008T074651Z.txt`.

The goal's serving path is TCP: a request arrives on a stream socket, eBPF sees
it at ingress, the GPU executor produces tokens, and the completion re-enters
the socket path. This finding adds that path and measures it against the two
paths already built.

## What changed

- **`bpf/fusion.bpf.c`** — the tc/clsact ingress now also parses `IPPROTO_TCP`.
  For a segment whose `dest == BF_LLM_TCP_PORT (39403)` and whose payload begins
  with `BF_LLM_MAGIC`, it extracts `doff` and reads the request header + prompt
  token ids starting at `l4 + doff*4` into the same token ring. The slot records
  `pad = 1` (transport flag) and the client's `saddr:sport` so the executor can
  find the reply socket. UDP behavior is byte-identical (the LLM UDP branch and
  the MLP magic branch are unchanged); the refactor is a single `llm_fill()`
  shared by both transports.
- **`executor/llm_executor.py --tcp`** — a listener on `BF_LLM_TCP_PORT`; a
  background thread accepts and stores connections keyed by peer `(ip, port)`.
  For a slot with `pad==1` the executor looks up that peer's socket and streams
  each generated token id as a little-endian `u32` as it is produced. The
  accepted connection is also drained so the RX queue never fills.
- **`tools/llm_tcp_client.py`**, **`tools/llm_bench.py --tcp`**,
  **`bench/run_llm_tcp.sh`**.

The reply rides the **normal TCP stack** on the accepted socket (event-driven,
one `send` per token, `TCP_NODELAY`), which is the honest "GPU completion
re-enters the socket path" reading of the goal. A `sockmap`/`sockops`
kernel-TX reply is a later refinement, not this finding.

## Results (gen=32, rounds=6, Qwen2.5-0.5B fp16, single stream)

| path | TTFT p50 | TPOT p50 |
|---|---|---|
| direct (in-process `model.generate`) | 9047 µs | 8308.0 µs |
| bpfusion (UDP → tc → ring → page poll) | 8999 µs | 8236.4 µs |
| **bpfusion-tcp (TCP → tc → ring → socket reply)** | **11624 µs** | **8340.0 µs** |

Second client (`tools/llm_tcp_client.py`, 6 rounds): TTFT p50 11857 µs, TPOT
p50 8363 µs. TTFT min ≈ 11.2 ms / max ≈ 12.4 ms; no long tail on a single
stream. Ingress counters confirm the route: `tcp dest=440`, `tcp magic=13`,
`llm magic=20`, `llm busy=0` (no ring drops).

## Interpretation

- **The TCP path costs ~+2.6 ms TTFT over UDP/direct** (11.6 ms vs 9.0 ms), and
  **TPOT is unchanged** (8.34 ms vs 8.24–8.31 ms, within noise). That is the
  expected shape: the request-side detour (TCP ingress instead of UDP ingress)
  and the reply-side cost (a per-token `send` on an established TCP connection,
  each paying loopback stack + ACK) add a one-time reply-setup cost visible at
  the first token, not per token — TPOT is dominated by the ~8.3 ms fp16
  decode either way.
- **The kernel path itself is a rounding error** relative to the 8–9 ms decode:
  verify + ingress + page handoff + reply never exceed ~2.6 ms of the first
  token, and TPOT adds ≈0. The tuning that matters is the model executor, not
  the transport.
- **Claim boundary.** The TCP reply is userspace `sendall` on the accepted
  socket, not a kernel `sockmap` TX, and the executor is host Python driving HF
  (batch 1). The relative comparison (direct vs UDP vs TCP, identical model
  both sides) is valid; the absolute TTFT/TPOT are not a serving claim. As with
  `0005`/`0007`, TPOT ≈ single-token decode and TTFT ≈ prefill + first decode.

## Regression check

The MLP path was re-run through `bench/run_e2e.sh` after the header/ingress
change on the historical config (work=4, idle=0,
`bench/results/e2e_20261008T075017Z.txt`): verify `max |GPU-CPU| = 1.021e-11`
OK, own p50 **40.4 µs** (0004: 41.3 µs), 22473 req/s one-at-a-time, 26499 req/s
at depth 8, 0 drops — no regression. A larger run (work=8, idle=1,
`bench/results/e2e_20261008T074814Z.txt`) gives own p50 65.8 µs, depth-8
38.2 k req/s, and the executor reports GPU occupancy 85.2 %.

## Caveats

- **The `BF_LLM_TCP_PORT` first-segment assumption:** the client sends the whole
  request in one `write`, and only the segment whose payload starts with the
  magic fills a slot. A request split across multiple segments would only be
  seen from its first segment (correct today, fragile to change); a
  `sockmap`/seq-tracking version would remove the assumption.
- **Loopback only measured.** The veth path (`0006`) is UDP; a TCP run over
  veth is not yet taken.
- **A pre-existing loopback subtlety surfaced while debugging:** the responder
  replies with the same `BF_MAGIC`, and on loopback the reply's source port is
  the server port, so a reply re-entering the ingress looks like a `BF_PORT`
  request. This was already masked by the `udp.dest == BF_PORT` guard, which the
  TCP refactor briefly dropped; it is restored and the guard is what keeps the
  reply path one-way.

## Reproduce

```
make
./build/bpfusion_load attach lo
HOME=/root PYTHONPATH=executor python3 executor/llm_executor.py --seconds 70 --tcp &
HOME=/root PYTHONPATH=executor python3 tools/llm_bench.py --tcp --gen 32 --rounds 6
# or: ./bench/run_llm_tcp.sh 70 32 6
```
