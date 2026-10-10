#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Live kernel-TX protocol regression: no model inference, synthetic token IDs.
Run from the root after make probes tools and make -C module CC=gcc-15.
Owns only this namespace's BPFusion tc hook and test module for the run.
"""
import ctypes
import errno
import socket
import struct
import subprocess
import time
from llm_executor import (open_page, Page, LLM_HEAD_OFF, BF_LLM_SLOTS,
                          LLM_RING_OFF, LLM_SLOT_SIZE, BF_PENDING, BF_FREE)


def wait_for(fn):
    end = time.monotonic() + 5
    while time.monotonic() < end:
        value = fn()
        if value:
            return value
        time.sleep(0.001)
    raise AssertionError("protocol progress timeout")


def main():
    subprocess.run(["./build/bpfusion_load", "detach", "lo"], check=True)
    subprocess.run(["./build/bpfusion_load", "attach", "lo"], check=True)
    loaded = False
    listener = socket.socket()
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(("127.0.0.1", 39403))
    listener.listen()
    listener.settimeout(5)
    mm, base = open_page()
    page = Page(mm, base)
    try:
        # Reject a genuine but incompatible BPF map FD before array casting.
        lib = ctypes.CDLL(None, use_errno=True)
        libbpf = ctypes.CDLL("libbpf.so.1", use_errno=True)
        wrong = libbpf.bpf_obj_get(b"/sys/fs/bpf/bpfusion_stats")
        assert wrong >= 0
        with open("module/bfusion_tx.ko", "rb") as module:
            ret = lib.syscall(313, module.fileno(), f"map_fd={wrong}".encode(), 0)
            assert ret == -1 and ctypes.get_errno() == errno.EINVAL
        import os
        os.close(wrong)
        print("PASS wrong map rejected", flush=True)
        subprocess.run(["./build/bpfusion_load", "tx-load"], check=True)
        loaded = True
        for trial in range(26):
            head = page.u32(LLM_HEAD_OFF)
            idx = head % BF_LLM_SLOTS
            assert page.slot(idx)[0] == BF_FREE
            client = socket.create_connection(("127.0.0.1", 39403), timeout=5)
            server, _ = listener.accept()
            n = 1 if trial == 0 else 64
            marker = time.monotonic_ns()
            client.sendall(struct.pack("<IIIIQI", 0x514c4d51, 1, n, 0, marker, 42))
            wait_for(lambda: page.u32(LLM_HEAD_OFF) == head + 1)
            assert page.slot(idx)[7] == marker
            disconnected = trial in (7, 17)
            if disconnected:
                client.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack("ii", 1, 0))
                client.close()
            expected = b"".join(struct.pack("<I", trial * 1000 + k) for k in range(n))
            for k in range(n):
                page.set_tok_out(idx, k, trial * 1000 + k)
                page.set_produced(idx, k + 1)
            time.sleep(0.08) # exceeds the former 500 * 60 us reclaim interval
            assert page.slot(idx)[0] == BF_PENDING, "reclaimed while executor owned slot"
            if not disconnected:
                data = b""
                while len(data) < len(expected):
                    # Exercise client stream framing with single-byte reads.
                    chunk = client.recv(1)
                    assert chunk
                    data += chunk
                assert data == expected
            page.finish(idx)
            wait_for(lambda: page.slot(idx)[0] == BF_FREE)
            if not disconnected:
                client.close()
            server.close()
        print("PASS 24 exact TCP replies, 2 resets, 26 DONE/recycle cycles, PENDING preserved", flush=True)
    finally:
        if loaded:
            subprocess.run(["rmmod", "bfusion_tx"], check=True)
        listener.close()
        mm.close()
        subprocess.run(["./build/bpfusion_load", "detach", "lo"], check=True)


if __name__ == "__main__":
    main()
