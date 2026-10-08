#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# BPFusion: TCP client for the LLM path.
#
# The request travels TCP -> tc ingress -> the token ring in the pinned page;
# the executor streams generated token ids back over the *same* accepted TCP
# socket. This measures TTFT/TPOT on the socket reply path (the path that will
# eventually be an async kernel TX), not the page-poll shortcut.
import argparse, socket, struct, time

BF_LLM_TCP_PORT = 39403
BF_LLM_MAGIC = 0x514c4d51


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=BF_LLM_TCP_PORT)
    ap.add_argument("--prompt", default="The capital of France is")
    ap.add_argument("--gen", type=int, default=32)
    ap.add_argument("--rounds", type=int, default=5)
    ap.add_argument("--model", default="Qwen/Qwen2.5-0.5B-Instruct")
    a = ap.parse_args()

    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(a.model)
    ids = tok(a.prompt).input_ids
    n_prompt = len(ids)

    ttft, tpot = [], []
    for r in range(a.rounds):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((a.host, a.port))
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        hdr = struct.pack("<IIIIQ", BF_LLM_MAGIC, n_prompt, a.gen, 0,
                          time.monotonic_ns())
        payload = hdr + struct.pack(f"<{n_prompt}I", *ids)
        t_send = time.perf_counter()
        s.sendall(payload)

        toks, stamps = [], []
        need = a.gen * 4
        buf = b""
        while len(toks) < a.gen:
            chunk = s.recv(min(4096, need - len(buf)))
            if not chunk:
                break
            buf += chunk
            while len(buf) >= 4 and len(toks) < a.gen:
                toks.append(struct.unpack("<I", buf[:4])[0])
                stamps.append(time.perf_counter())
                buf = buf[4:]
        s.close()
        if len(toks) < a.gen:
            print(f"round {r}: short read ({len(toks)} tok)")
            continue
        ttft.append((stamps[0] - t_send) * 1e6)
        tpot.append((stamps[-1] - stamps[0]) / (a.gen - 1) * 1e6)
        if r == 0:
            print("text:", repr(tok.decode(toks[:24])))

    if not ttft:
        print("no samples")
        return
    ttft.sort(); tpot.sort()
    n = len(ttft)
    print(f"tcp reply path: TTFT us p50={ttft[n//2]:.0f} "
          f"min={ttft[0]:.0f} max={ttft[-1]:.0f} | "
          f"TPOT us p50={tpot[n//2]:.1f} min={tpot[0]:.1f} max={tpot[-1]:.1f}")


if __name__ == "__main__":
    main()
