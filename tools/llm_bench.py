#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# BPFusion: LLM-path benchmark.
#
# Two matched paths, same model, same host, same process count:
#   A. direct   : tokenize -> model.generate() in-process (vLLM-style baseline)
#   B. bpfusion : packet -> tc ingress eBPF -> pinned page -> resident executor
#                 -> generated tokens streamed back through the same page
#
# Reports TTFT (send -> first token visible) and TPOT (mean inter-token gap).
import argparse, struct, socket, time
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from llm_executor import (BF_LLM_SLOTS, LLM_HEAD_OFF, open_page, Page,
                          BF_PENDING)

BF_LLM_PORT = 39402
BF_LLM_MAGIC = 0x514c4d51


def direct(model, tok, prompt, n_gen):
    ids = tok(prompt).input_ids
    inp = torch.tensor([ids], device="cuda")
    with torch.no_grad():
        t0 = time.perf_counter()
        out = model(inp, use_cache=True)
        past = out.past_key_values
        nxt = int(out.logits[:, -1].argmax(-1))
        t_first = time.perf_counter()
        times = [t_first - t0]
        for _ in range(n_gen - 1):
            out = model(torch.tensor([[nxt]], device="cuda"),
                        past_key_values=past, use_cache=True)
            past = out.past_key_values
            nxt = int(out.logits[:, -1].argmax(-1))
            times.append(time.perf_counter() - t0)
    ttft = (times[0]) * 1e6
    tpot = (times[-1] - times[0]) / (n_gen - 1) * 1e6
    return ttft, tpot, tok.decode([nxt])


def bpfusion(page, s, dest, ids, n_gen):
    n_prompt = len(ids)
    client_ns = time.monotonic_ns()
    hdr = struct.pack("<IIIIQ", BF_LLM_MAGIC, n_prompt, n_gen, 0, client_ns)
    payload = hdr + struct.pack(f"<{n_prompt}I", *ids)
    t_send = time.perf_counter()
    s.sendto(payload, dest)
    # find our slot by client_ns
    slot = None
    deadline = t_send + 30
    while time.perf_counter() < deadline:
        head = page.u32(LLM_HEAD_OFF)
        for k in range(BF_LLM_SLOTS):
            idx = (head - 1 - k) % BF_LLM_SLOTS
            v = page.slot(idx)
            if v[7] == client_ns and v[0] == BF_PENDING:
                slot = idx
                break
        if slot is not None:
            break
    if slot is None:
        return None
    stamps = []
    last = 0
    while time.perf_counter() < deadline:
        v = page.slot(slot)
        produced = v[3]
        if produced > last:
            now = time.perf_counter()
            while last < produced:
                stamps.append(now)
                last += 1
            if produced >= n_gen:
                break
    if not stamps:
        return None
    ttft = (stamps[0] - t_send) * 1e6
    tpot = (stamps[-1] - stamps[0]) / max(1, len(stamps) - 1) * 1e6
    return ttft, tpot, page.slot(slot)[11][:n_gen]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen2.5-0.5B-Instruct")
    ap.add_argument("--prompt", default="The capital of France is")
    ap.add_argument("--gen", type=int, default=32)
    ap.add_argument("--rounds", type=int, default=5)
    a = ap.parse_args()

    tok = AutoTokenizer.from_pretrained(a.model)
    model = AutoModelForCausalLM.from_pretrained(
        a.model, dtype=torch.float16).to("cuda").eval()
    ids = tok(a.prompt).input_ids

    mm, base = open_page()
    page = Page(mm, base)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dest = ("127.0.0.1", BF_LLM_PORT)

    # warm both paths
    direct(model, tok, a.prompt, 4)
    bpfusion(page, s, dest, ids, 4)

    print(f"prompt={a.prompt!r} prompt_tok={len(ids)} gen={a.gen}")
    for name, fn in (("direct", lambda: direct(model, tok, a.prompt, a.gen)),
                     ("bpfusion", lambda: bpfusion(page, s, dest, ids, a.gen))):
        tt, tp = [], []
        for _ in range(a.rounds):
            r = fn()
            if r is None:
                continue
            tt.append(r[0]); tp.append(r[1])
        if not tt:
            print(f"{name}: no samples")
            continue
        tt.sort(); tp.sort()
        n = len(tt)
        print(f"{name:9s} TTFT us: p50={tt[n//2]:.0f} min={tt[0]:.0f} "
              f"max={tt[-1]:.0f} | TPOT us: p50={tp[n//2]:.1f} "
              f"min={tp[0]:.1f} max={tp[-1]:.1f}")


if __name__ == "__main__":
    main()
