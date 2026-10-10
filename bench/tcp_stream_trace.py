#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Passive loopback TCP metadata capture for the native Qwen token HTTP path."""
import argparse
import json
from pathlib import Path
import socket
import struct
import subprocess
import tempfile
import threading
import time
from resident_dispatch import command,connect,request,oracle_cases

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument("--executor",default="./build/qwen")
args=parser.parse_args()
cases,_=oracle_cases(8)
packets=[]; stop=threading.Event()
with socket.socket(socket.AF_PACKET,socket.SOCK_RAW,socket.htons(0x0800)) as capture:
    capture.bind(("lo",0)); capture.settimeout(.05)
    def collect():
        while not stop.is_set():
            try: packet,address=capture.recvfrom(65535)
            except socket.timeout: continue
            ns=time.monotonic_ns()
            if address[2]==socket.PACKET_OUTGOING or len(packet)<54 or packet[23]!=6: continue
            ip=14+(packet[14]&15)*4
            sport,dport,seq,ack=struct.unpack_from("!HHII",packet,ip)
            if 39403 not in (sport,dport): continue
            end=14+struct.unpack_from("!H",packet,16)[0]
            body=packet[ip+(packet[ip+12]>>4)*4:end]
            kind="request" if body.startswith(b"POST") else "header" if body.startswith(b"HTTP") else "tokens" if body else "empty"
            packets.append({"event":"packet","mono_ns":ns,"sport":sport,"dport":dport,
                "seq":seq,"ack":ack,"flags":packet[ip+13],"bytes":len(body),"kind":kind})
    observer=threading.Thread(target=collect); observer.start()
    executor=None
    with tempfile.TemporaryDirectory(prefix="bpfusion-tcp-trace-") as tmp:
        logpath=Path(tmp)/"executor.log"
        try:
            command("./build/bpfusion_load","stream-attach")
            with logpath.open("w") as log:
                executor=subprocess.Popen([args.executor,"/workspaces/.cache/bpfusion/qwen25-05b-fp16.bin","60"],stdout=log,stderr=subprocess.STDOUT)
            started=time.monotonic()
            while "resident Qwen ready" not in logpath.read_text():
                assert executor.poll() is None and time.monotonic()-started<60,logpath.read_text()
                time.sleep(.05)
            print(json.dumps({"event":"metadata","commit":command("git","rev-parse","HEAD"),"executor":args.executor,"clock":"client and passive capture monotonic_ns; receive timestamps include observer scheduling"}),flush=True)
            with connect() as client:
                for case,(ids,expected) in enumerate(cases):
                    print(json.dumps({"event":"reply","case":case,**request(client,ids,expected)}),flush=True)
            time.sleep(.1)
        finally:
            stop.set(); observer.join()
            for packet in packets: print(json.dumps(packet),flush=True)
            if executor is not None:
                executor.terminate(); executor.wait(timeout=60)
                print(json.dumps({"event":"executor","log":logpath.read_text(),"stats":command("./build/bpfusion_load","stats")}),flush=True)
            command("./build/bpfusion_load","stream-detach")
            command("./build/bpfusion_load","detach","lo")
            for name in ("bpfusion_ctl","bpfusion_stats","bpfusion_db"):
                Path("/sys/fs/bpf",name).unlink(missing_ok=True)
