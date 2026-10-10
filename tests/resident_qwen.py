#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Resident CUDA Qwen vs eager HF fp16 greedy oracle on real TCP replies."""
import gc
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
    subprocess.run(["./build/bpfusion_load","attach","lo"],check=True)
    loaded=False
    executor=None
    logpath="/tmp/bpfusion-resident-qwen.log"
    try:
        subprocess.run(["./build/bpfusion_load","tx-load"],check=True)
        loaded=True
        with open(logpath,"w") as log:
            executor=subprocess.Popen(["./build/qwen","/workspaces/.cache/bpfusion/qwen25-05b-fp16.bin","300"],stdout=log,stderr=subprocess.STDOUT)
        start=time.monotonic()
        while "resident Qwen ready" not in open(logpath).read():
            if executor.poll() is not None or time.monotonic()-start>60:
                raise AssertionError(open(logpath).read())
            time.sleep(.1)
        for repetition in range(3):
            for idx,(ids,expected) in enumerate(cases):
                with socket.create_connection(("127.0.0.1",39403),timeout=60) as client:
                    start=time.perf_counter()
                    client.sendall(struct.pack("<IIIIQ",0x514c4d51,len(ids),len(expected),0,time.monotonic_ns())+struct.pack(f"<{len(ids)}I",*ids))
                    data=b""
                    while len(data)<len(expected)*4:
                        chunk=client.recv(len(expected)*4-len(data))
                        assert chunk,"short reply"
                        data+=chunk
                    actual=list(struct.unpack(f"<{len(expected)}I",data))
                    elapsed=time.perf_counter()-start
                    print(f"rep={repetition} case={idx} expected={expected} actual={actual} seconds={elapsed:.3f}",flush=True)
                    assert actual==expected,(idx,actual,expected)
        print("PASS 12 TCP requests, 96 real Qwen greedy tokens, one CUDA launch, no host accept/read/send worker",flush=True)
    finally:
        if executor is not None:
            executor.terminate(); executor.wait()
            print(open(logpath).read(),flush=True)
        if loaded:
            subprocess.run(["rmmod","bfusion_tx"],check=True)
        subprocess.run(["./build/bpfusion_load","detach","lo"],check=True)


if __name__=="__main__": main()
