#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Tokenize text locally and call the resident server over TCP or binary HTTP."""
import argparse
import socket
import struct
import time

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=39403)
    ap.add_argument("--prompt", default="The capital of France is")
    ap.add_argument("--gen", type=int, default=32)
    ap.add_argument("--rounds", type=int, default=5)
    ap.add_argument("--model", default="Qwen/Qwen2.5-0.5B-Instruct")
    ap.add_argument("--http", action="store_true", help="POST /generate using binary token IDs")
    a = ap.parse_args()
    if not 1 <= a.gen <= 64 or a.rounds < 1:
        ap.error("--gen must be 1..64 and --rounds must be positive")
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(a.model)
    ids = tok(a.prompt).input_ids
    if not 1 <= len(ids) <= 64:
        ap.error("the tokenized prompt must contain 1..64 tokens")

    ttft, tpot = [], []
    for r in range(a.rounds):
        body = struct.pack("<IIIIQ", 0x514c4d51, len(ids), a.gen, 0, time.monotonic_ns())
        body += struct.pack(f"<{len(ids)}I", *ids)
        wire = body
        if a.http:
            wire = (f"POST /generate HTTP/1.1\r\nHost: {a.host}\r\n"
                    f"Content-Type: application/octet-stream\r\n"
                    f"Content-Length: {len(body)}\r\n\r\n").encode() + body
        with socket.create_connection((a.host, a.port), timeout=60) as client:
            client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            start = time.perf_counter()
            client.sendall(wire)
            tokens, stamps, pending = [], [], b""
            header = b"" if a.http else None
            while len(tokens) < a.gen:
                chunk = client.recv(4096)
                arrived = time.perf_counter()
                if not chunk:
                    raise RuntimeError(f"short reply: received {len(tokens)} of {a.gen} tokens")
                if header is not None:
                    header += chunk
                    if b"\r\n\r\n" not in header:
                        continue
                    head, chunk = header.split(b"\r\n\r\n", 1)
                    fields = dict(line.split(b":", 1) for line in head.split(b"\r\n")[1:] if b":" in line)
                    length = next((v.strip() for k, v in fields.items() if k.lower() == b"content-length"), None)
                    if not head.startswith(b"HTTP/1.1 200 OK\r\n") or length != str(a.gen * 4).encode():
                        raise RuntimeError(f"unexpected HTTP reply: {head!r}")
                    header = None
                pending += chunk
                while len(pending) >= 4 and len(tokens) < a.gen:
                    tokens.append(struct.unpack("<I", pending[:4])[0])
                    stamps.append(arrived)
                    pending = pending[4:]
            if pending:
                raise RuntimeError("unexpected bytes after the token response")
        ttft.append((stamps[0] - start) * 1e6)
        if a.gen > 1:
            tpot.append((stamps[-1] - stamps[0]) / (a.gen - 1) * 1e6)
        if r == 0:
            print("text:", repr(tok.decode(tokens)))

    ttft.sort(); tpot.sort()
    print(f"TCP reply TTFT us: p50={ttft[len(ttft)//2]:.0f} min={ttft[0]:.0f} max={ttft[-1]:.0f}")
    if tpot:
        print(f"TPOT us: p50={tpot[len(tpot)//2]:.1f} min={tpot[0]:.1f} max={tpot[-1]:.1f}")
    else:
        print("TPOT: n/a (one output token)")
    print("Client arrival timings include receive coalescing; use bench/ for controlled comparisons.")

if __name__ == "__main__":
    main()
