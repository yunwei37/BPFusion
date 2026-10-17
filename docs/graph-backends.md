# Supplying a captured CUDA graph

BPFusion now has an experimental one-shot graph adapter independent of LLM
model metadata. A caller supplies one CUDA graph and device input/output buffer
per slot. The server copies opaque32-bit words from the existing shared queue,
launches the graph on the GPU, waits for its child work, publishes output and
retires requests in FIFO order. Both transports use the same graph adapter.
The computation remains in the caller's captured graph.

See [graph_backend.h](../executor/graph_backend.h) for ABI version1 and buffer
ownership. Every graph must support CUDA device launch; host callbacks, host
transfers and graph allocation/free nodes are outside this interface. Referenced
tensors/graphs must stay alive until serve returns. Capture/capability errors
are reported; there is no fallback CPU computation.

## Run the existing cuBLAS/cuFFT examples

Use the Linux/GPU/CUDA/libbpf/Python prerequisites in
[getting started](getting-started.md). Activate that environment, then:

~~~sh
make build/fusion.bpf.o build/bpfusion_load \
  graph-server-uring-loop graph-server-user-network-wait
./build/bpfusion_load stream-uring-attach
python3 examples/torch_graph_server.py build/graph_server_uring_loop.so matmul --seconds 120
~~~

Wait for the ready line with abi=1, slots=8, input_words=64, output_words=64.
For FFT, substitute fft for matmul. Stop one server and clean its pins before
starting another. After it exits:

~~~sh
./build/bpfusion_load stats
./build/bpfusion_load stream-detach
rm -f /sys/fs/bpf/bpfusion_ctl /sys/fs/bpf/bpfusion_stats /sys/fs/bpf/bpfusion_db
~~~

The matched native path needs no BPF attach:

~~~sh
python3 examples/torch_graph_server.py build/graph_server_user_network_wait.so matmul --seconds 120
~~~

The example captures upstream torch.mm (cuBLAS) or torch.fft.fft (cuFFT).
Python remains alive to own the allocations; it does not execute per-request
computation. Input/output are each64 raw float32 words: matmul takes a row-major
8x8 left matrix and multiplies by fixed W[i,j]=(8*i+j)%7-3. FFT takes32
complex64 values as interleaved real/imaginary words.

A minimal binary client, in another terminal:

~~~python
import socket, struct, time
x = [float(i % 7 - 3) for i in range(64)]
body = struct.pack("<IIIIQ", 0x514c4d51, 64, 64, 0, time.monotonic_ns())
body += struct.pack("<64f", *x)
with socket.create_connection(("127.0.0.1", 39403), timeout=15) as sock:
    sock.sendall(body)
    output = bytearray()
    while len(output) < 256:
        part = sock.recv(256-len(output))
        if not part:
            raise RuntimeError("short reply")
        output.extend(part)
print(struct.unpack("<64f", output))
~~~

HTTP uses the same binary frame with Content-Length, as in the LLM transport.
A valid frame with the wrong backend input/output count receives HTTP400 or
binary EOF. There is no tokenizer, vocabulary check, text or JSON tensor API.

## Experimental BPF-owned networking

The same captured-graph caller and arithmetic can use the
[ordinary kernel-network candidate](findings/0079-kernel-network-source-integration.md):

~~~sh
make build/fusion.bpf.o build/bpfusion_load graph-server-kernel-network
./build/bpfusion_load stream-uring-attach
python3 examples/torch_graph_server.py build/graph_server_kernel_network.so matmul --seconds 120
~~~

Substitute fft for matmul,then use the same client/cleanup above. This transport
moves io_uring CQ/SQ,connection/reply lifetime into BPF and removes the GPU I/O
CTA. It changes no caller graph,buffer,ABI or graph-dispatch instruction.
Default8 cuBLAS/cuFFT finite numerical/lifecycle qualification is recorded in0079.
It is an experimental control,not a selected faster transport or stable
arbitrary-kernel plugin. The autoregressive scheduler stays a separate adapter.

## Qualified boundary

[Four real lifecycle runs](findings/0067-opaque-graph-backend.md) cover both
operations and transports at default8 on the existing qualified stack. These
are finite engineering checks, not throughput, universal numerical accuracy or
arbitrary CUDA/library compatibility evidence. The on-wire names and internal
queue layout still carry historical LLM naming, and lengths are limited to64
words. There is no dynamic shape negotiation, backend registry, model loader
or stable arbitrary-kernel plugin promise. The autoregressive LLM scheduler is
a separate adapter. This small interface proves a reusable transport boundary
without rewriting cuBLAS, cuFFT or model kernels.
