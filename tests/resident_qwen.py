#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Resident CUDA Qwen vs eager HF fp16 greedy oracle on real TCP replies."""
from concurrent.futures import ThreadPoolExecutor
from contextlib import nullcontext
from threading import Barrier
import argparse
import gc
import re
import socket
import struct
import subprocess
import time
from pathlib import Path
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


def oracle_cases(gen):
    name="Qwen/Qwen2.5-0.5B-Instruct"
    tok=AutoTokenizer.from_pretrained(name)
    model=AutoModelForCausalLM.from_pretrained(name,dtype=torch.float16,attn_implementation="eager").to("cuda").eval()
    vocab=model.config.vocab_size
    cases=[]
    for prompt in ("The capital of France is", "What is 2 plus 2?", "Write a short greeting.", "Linux is"):
        ids=tok(prompt).input_ids
        with torch.no_grad():
            out=model(torch.tensor([ids],device="cuda"),use_cache=True)
            past=out.past_key_values
            nxt=int(out.logits[:,-1].argmax(-1))
            expected=[nxt]
            for _ in range(gen-1):
                out=model(torch.tensor([[nxt]],device="cuda"),past_key_values=past,use_cache=True)
                past=out.past_key_values
                nxt=int(out.logits[:,-1].argmax(-1))
                expected.append(nxt)
        cases.append((ids,expected))
    del model,out,past
    gc.collect(); torch.cuda.empty_cache()
    return cases,vocab


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--gen",type=int,default=8,choices=range(1,65))
    parser.add_argument("--executor",default="./build/qwen")
    args=parser.parse_args()
    cases,vocab=oracle_cases(args.gen)
    print("HF eager fp16 oracle ready, model released",flush=True)
    subprocess.run(["./build/bpfusion_load","detach","lo"],check=True)
    subprocess.run(["./build/bpfusion_load","stream-detach"],check=True)
    subprocess.run(["./build/bpfusion_load","stream-attach"],check=True)
    executor=None
    complete=False
    logpath="/tmp/bpfusion-resident-qwen.log"
    try:
        with open(logpath,"w") as log:
            executor=subprocess.Popen(["strace","-D","-f","-e","trace=network,write","-o","/tmp/bpfusion-qwen-network.trace",args.executor,"/workspaces/.cache/bpfusion/qwen25-05b-fp16.bin","300"],stdout=log,stderr=subprocess.STDOUT)
        start=time.monotonic()
        while "resident Qwen ready" not in open(logpath).read():
            if executor.poll() is not None or time.monotonic()-start>60:
                raise AssertionError(open(logpath).read())
            time.sleep(.1)
        for _ in range(5000):
            socket.create_connection(("127.0.0.1",39403),timeout=5).close()
        print("PASS 5000 empty connections accepted/drained by kernel; exceeds undrained listener backlog",flush=True)
        def request(idx, ids, expected, http=False, client=None, split=True, reject=False):
            with (nullcontext(client) if client is not None else socket.create_connection(("127.0.0.1",39403),timeout=60)) as client:
                start=time.perf_counter()
                client.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)
                wire=struct.pack("<IIIIQ",0x514c4d51,len(ids),len(expected),0,time.monotonic_ns())+struct.pack(f"<{len(ids)}I",*ids)
                if http:
                    wire=(f"POST /generate HTTP/1.1\r\nHost: localhost\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(wire)}\r\n\r\n".encode()+wire)
                # Separate writes across header and payload; the parser
                # must frame one request after TCP stream reassembly.
                if split:
                    for byte in wire:
                        client.sendall(bytes([byte]))
                        time.sleep(.001)
                else:
                    client.sendall(wire)
                reply=[] if reject else expected
                if http:
                    header=b""
                    while not header.endswith(b"\r\n\r\n"):
                        chunk=client.recv(1); assert chunk,"short HTTP header"; header+=chunk
                    status=b"400 Bad Request" if reject else b"200 OK"
                    assert header.startswith(b"HTTP/1.1 "+status+b"\r\n"),header
                    assert f"Content-Length: {len(reply)*4}\r\n".encode() in header,header
                data=b""
                while len(data)<len(reply)*4:
                    chunk=client.recv(len(reply)*4-len(data))
                    assert chunk,"short reply"
                    data+=chunk
                actual=list(struct.unpack(f"<{len(reply)}I",data))
                elapsed=time.perf_counter()-start
                if split:
                    print(f"http={http} case={idx} expected={expected} actual={actual} seconds={elapsed:.3f}",flush=True)
                assert actual==reply,(idx,actual,reply)
        for repetition in range(3):
            for idx,(ids,expected) in enumerate(cases):
                request(idx,ids,expected,http=repetition==1)
        with ThreadPoolExecutor(max_workers=8) as clients:
            futures=[clients.submit(request,i,*cases[i%len(cases)],i>=4) for i in range(8)]
            for future in futures: future.result()
        print("PASS eight concurrent clients, exact Qwen replies, no admission drops",flush=True)
        # A reply must return queue ownership before the immediate next send.
        # Eight persistent closed-loop clients repeatedly wrap the eight slots.
        barrier=Barrier(8)
        def closed_loop(i):
            with socket.create_connection(("127.0.0.1",39403),timeout=60) as client:
                barrier.wait(timeout=60)
                for repeat in range(32):
                    ids,expected=cases[(i+repeat)%len(cases)]
                    invalid=ids.copy(); invalid[0]=vocab
                    request(i+8*repeat,invalid,expected,http=True,client=client,split=False,reject=True)
                    request(i+8*repeat,ids,expected,http=True,client=client,split=False)
        with ThreadPoolExecutor(max_workers=8) as clients:
            futures=[clients.submit(closed_loop,i) for i in range(8)]
            for future in futures: future.result()
        print("PASS 256 HTTP rejections immediately followed by 256 exact valid replies on eight persistent clients, repeated ring wrap",flush=True)
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
        ids,expected=cases[0]
        bad_last=ids.copy(); bad_last[-1]=vocab
        bad_first=ids.copy(); bad_first[0]=0xffffffff
        def body(tokens):
            return struct.pack("<IIIIQ",0x514c4d51,len(tokens),len(expected),0,time.monotonic_ns())+struct.pack(f"<{len(tokens)}I",*tokens)
        # An invalid request must not terminate the grid or poison a later
        # request on this same stream, including coalesced skb framing.
        with socket.create_connection(("127.0.0.1",39403),timeout=60) as client:
            for tokens in (bad_last,ids,bad_first,ids):
                payload=body(tokens)
                client.sendall(f"POST /generate HTTP/1.1\r\nHost: localhost\r\nContent-Length: {len(payload)}\r\n\r\n".encode()+payload)
            for invalid in (True,False,True,False):
                header=b""
                while not header.endswith(b"\r\n\r\n"):
                    chunk=client.recv(1); assert chunk,"short rejection/pipeline header"; header+=chunk
                status=b"400 Bad Request" if invalid else b"200 OK"
                assert header.startswith(b"HTTP/1.1 "+status+b"\r\n"),header
                count=0 if invalid else len(expected)*4
                assert f"Content-Length: {count}\r\n".encode() in header,header
                data=b""
                while len(data)<count:
                    chunk=client.recv(count-len(data)); assert chunk; data+=chunk
                if not invalid: assert list(struct.unpack(f"<{len(expected)}I",data))==expected
        with socket.create_connection(("127.0.0.1",39403),timeout=60) as client:
            client.sendall(body(bad_first))
            assert client.recv(1)==b"","binary rejection must close the connection"
        request(0,ids,expected)
        print("PASS invalid first/last token IDs: HTTP 400, binary EOF, same-stream and later requests still exact",flush=True)
        print(f"PASS 285 valid TCP/HTTP requests, {285*args.gen} real Qwen greedy tokens, 259 rejections, no host accept/read/send worker",flush=True)
        complete=True
    finally:
        try:
            if executor is not None:
                executor.terminate(); executor.wait()
                log=open(logpath).read()
                print(log,flush=True)
                if complete and "dispatch=host-launch" in log:
                    assert "dispatch=host-launch launches=544" in log,log
                elif complete:
                    assert "dispatch=resident launches=1" in log,log
                if complete: print("PASS expected CUDA launch count for the selected dispatch",flush=True)
                trace=open("/tmp/bpfusion-qwen-network.trace").read()
                active=trace.split("resident Qwen ready",1)[1]
                assert not re.search(r"\b(?:accept4?|recvfrom|recvmsg|recvmmsg|sendto|sendmsg|sendmmsg)\(",active),active
                print("PASS traced all executor threads: no accept/receive/send syscalls after ready",flush=True)
            subprocess.run(["./build/bpfusion_load","stats"],check=True)
        finally:
            subprocess.run(["./build/bpfusion_load","stream-detach"],check=True)
            subprocess.run(["./build/bpfusion_load","detach","lo"],check=True)
            for name in ("bpfusion_ctl","bpfusion_stats","bpfusion_db"):
                Path("/sys/fs/bpf",name).unlink(missing_ok=True)
            print("PASS test map pins removed after module shutdown and hook detach",flush=True)



if __name__=="__main__": main()
