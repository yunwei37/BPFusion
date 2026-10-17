#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""CUDA-event host-replay calibration; not an isolated device-launch timing."""
import importlib.util,json,platform,time
from pathlib import Path
import torch
r=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("graph_example",r/"examples/torch_graph_server.py")
example=importlib.util.module_from_spec(spec);spec.loader.exec_module(example)
result=dict(event="calibration",source=Path(__file__).read_text(),example_source=(r/"examples/torch_graph_server.py").read_text(),
            torch=torch.__version__,cuda=torch.version.cuda,device=torch.cuda.get_device_name(0),platform=platform.platform(),cells=[])
for operation in ["matmul","fft"]:
    for repeat in [1,16,256]:
        graphs,inputs,outputs,weights=example.capture_graphs(operation,8,repeat)
        for _ in range(3):graphs[0].replay()
        torch.cuda.synchronize()
        elapsed=[]
        for block in range(5):
            start=torch.cuda.Event(enable_timing=True);end=torch.cuda.Event(enable_timing=True)
            start.record()
            for _ in range(100):graphs[0].replay()
            end.record();end.synchronize();elapsed.append(start.elapsed_time(end)*1000/100)
        result["cells"].append(dict(operation=operation,repeat=repeat,host_replay_event_us_per_graph=elapsed,
          note="CUDA-event batch elapsed includes host submission gaps; no request latency or pure isolated-kernel claim. Served graphs have no timing nodes."))
        del graphs,inputs,outputs,weights
print(json.dumps(result))
