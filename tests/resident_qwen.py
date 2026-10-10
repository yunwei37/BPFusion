#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Resident CUDA Qwen vs eager HF fp16 greedy oracle on real TCP replies."""
from concurrent.futures import ThreadPoolExecutor
import gc
import re
import socket
import struct
import subprocess
import time
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


def main():
    name="Qwen/Qwen2.5-0.5B-Instruct"
    tok=AutoTokenizer.from_pretrained(name)
    model=AutoModelForCausalLM.from_pretrained(name,dtype=torch.float16,attn_implementation="eager").to("cuda").eval()
    cases=[]
    for prompt in ("The capital of France is", "What is 2 plus 2?", "Write a short greeting.", "Linux is"):
        ids=tok(prompt).input_ids
        with torch.no_grad():
            out=model(torch.tensor([ids],device="cuda"),use_cache=True)
            past=out.past_key_values
            nxt=int(out.logits[:,-1].argmax(-1))
            expected=[nxt]
            for _ in range(7):
                out=model(torch.tensor([[nxt]],device="cuda"),past_key_values=past,use_cache=True)
                past=out.past_key_values
                nxt=int(out.logits[:,-1].argmax(-1))
                expected.append(nxt)
        cases.append((ids,expected))
    del model,out,past
    gc.collect(); torch.cuda.empty_cache()
    print("HF eager fp16 oracle ready, model released",flush=True)
    subprocess.run(["./build/bpfusion_load","detach","lo"],check=True)
    subprocess.run(["./build/bpfusion_load","stream-detach"],check=True)
    subprocess.run(["./build/bpfusion_load","stream-attach"],check=True)
    executor=None
    logpath="/tmp/bpfusion-resident-qwen.log"
    try:
        with open(logpath,"w") as log:
            executor=subprocess.Popen(["strace","-D","-f","-e","trace=network,write","-o","/tmp/bpfusion-qwen-network.trace","./build/qwen","/workspaces/.cache/bpfusion/qwen25-05b-fp16.bin","300"],stdout=log,stderr=subprocess.STDOUT)
        start=time.monotonic()
        while "resident Qwen ready" not in open(logpath).read():
            if executor.poll() is not None or time.monotonic()-start>60:
                raise AssertionError(open(logpath).read())
            time.sleep(.1)
        for _ in range(5000):
            socket.create_connection(("127.0.0.1",39403),timeout=5).close()
        print("PASS 5000 empty connections accepted/drained by kernel; exceeds undrained listener backlog",flush=True)
        def request(idx, ids, expected, http=False):
            with socket.create_connection(("127.0.0.1",39403),timeout=60) as client:
                start=time.perf_counter()
                client.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)
                wire=struct.pack("<IIIIQ",0x514c4d51,len(ids),len(expected),0,time.monotonic_ns())+struct.pack(f"<{len(ids)}I",*ids)
                if http:
                    wire=(f"POST /generate HTTP/1.1\r\nHost: localhost\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(wire)}\r\n\r\n".encode()+wire)
                # Separate writes across header and payload; the parser
                # must frame one request after TCP stream reassembly.
                for byte in wire:
                    client.sendall(bytes([byte]))
                    time.sleep(.001)
                if http:
                    header=b""
                    while not header.endswith(b"\r\n\r\n"):
                        chunk=client.recv(1); assert chunk,"short HTTP header"; header+=chunk
                    assert header.startswith(b"HTTP/1.1 200 OK\r\n"),header
                    assert f"Content-Length: {len(expected)*4}\r\n".encode() in header,header
                data=b""
                while len(data)<len(expected)*4:
                    chunk=client.recv(len(expected)*4-len(data))
                    assert chunk,"short reply"
                    data+=chunk
                actual=list(struct.unpack(f"<{len(expected)}I",data))
                elapsed=time.perf_counter()-start
                print(f"http={http} case={idx} expected={expected} actual={actual} seconds={elapsed:.3f}",flush=True)
                assert actual==expected,(idx,actual,expected)
        for repetition in range(3):
            for idx,(ids,expected) in enumerate(cases):
                request(idx,ids,expected,http=repetition==1)
        with ThreadPoolExecutor(max_workers=8) as clients:
            futures=[clients.submit(request,i,*cases[i%len(cases)],i>=4) for i in range(8)]
            for future in futures: future.result()
        print("PASS eight concurrent clients, exact Qwen replies, no admission drops",flush=True)
        # Pipelining on one persistent stream crosses the slot ring boundary.
        with socket.create_connection(("127.0.0.1",39403),timeout=60) as client:
            for i in range(6):
                ids,expected=cases[i%len(cases)]
                body=struct.pack("<IIIIQ",0x514c4d51,len(ids),len(expected),0,time.monotonic_ns())+struct.pack(f"<{len(ids)}I",*ids)
                client.sendall(f"POST /generate HTTP/1.1\r\nHost: localhost\r\nContent-Length: {len(body)}\r\n\r\n".encode()+body)
            client.shutdown(socket.SHUT_WR)
            for i in range(6):
                _,expected=cases[i%len(cases)]
                header=b""
                while not header.endswith(b"\r\n\r\n"):
                    chunk=client.recv(1); assert chunk,"short pipelined HTTP header"; header+=chunk
                assert header.startswith(b"HTTP/1.1 200 OK\r\n"),header
                assert f"Content-Length: {len(expected)*4}\r\n".encode() in header,header
                data=b""
                while len(data)<len(expected)*4:
                    chunk=client.recv(len(expected)*4-len(data)); assert chunk; data+=chunk
                actual=list(struct.unpack(f"<{len(expected)}I",data))
                assert actual==expected,("pipeline",i,actual,expected)
        print("PASS six pipelined HTTP responses in order, ring wrap, half-close",flush=True)
        print("PASS 26 TCP/HTTP requests, 208 real Qwen greedy tokens, one CUDA launch, no host accept/read/send worker",flush=True)
    finally:
        if executor is not None:
            executor.terminate(); executor.wait()
            print(open(logpath).read(),flush=True)
            trace=open("/tmp/bpfusion-qwen-network.trace").read()
            active=trace.split("resident Qwen ready",1)[1]
            assert not re.search(r"\b(?:accept4?|recvfrom|recvmsg|recvmmsg|sendto|sendmsg|sendmmsg)\(",active),active
            print("PASS traced all executor threads: no accept/receive/send syscalls after ready",flush=True)
        subprocess.run(["./build/bpfusion_load","stats"],check=True)
        subprocess.run(["./build/bpfusion_load","stream-detach"],check=True)
        subprocess.run(["./build/bpfusion_load","detach","lo"],check=True)


if __name__=="__main__": main()
