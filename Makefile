# BPFusion build: eBPF objects and userspace tools.
#
#   make            # build everything into build/
#   make probes     # only the eBPF objects
#   make run-probe  # build + run the ingress-wake probe
#
# Requires: clang, libbpf, libelf, zlib, libcuda/nvcc for the executor.

BUILD    := build
ARCH     := $(shell uname -m | sed 's/x86_64/x86/;s/aarch64/arm64/')
BPF_CFLAGS := -O2 -g -target bpf -mcpu=v3 -D__TARGET_ARCH_$(ARCH) \
              -I/usr/include/$(shell uname -m)-linux-gnu -Ibpf/include \
              -Wall -Werror -Wno-missing-declarations -Wno-unused-value
CC       ?= cc
CFLAGS   ?= -O2 -g -Wall -Wextra -Wno-unused-parameter
LDLIBS   := -lbpf -lelf -lz -lpthread

BPF_SRCS := $(wildcard bpf/*.bpf.c)
BPF_OBJS := $(patsubst bpf/%.bpf.c,$(BUILD)/%.bpf.o,$(BPF_SRCS))
TOOLS    := $(BUILD)/wake_probe $(BUILD)/client $(BUILD)/echo_udp \
            $(BUILD)/bpfusion_load $(BUILD)/perfcount

.PHONY: all probes tools executor clean run-probe run-executor

CUDA_HOME ?= /usr/local/cuda
NVCC      ?= $(CUDA_HOME)/bin/nvcc
SM_ARCH   ?= sm_120

all: probes tools executor

probes: $(BPF_OBJS)

tools: $(TOOLS)

executor: $(BUILD)/executor

$(BUILD)/%.bpf.o: bpf/%.bpf.c bpf/include/bpfusion_queue.h | $(BUILD)
	clang $(BPF_CFLAGS) -c $< -o $@

$(BUILD)/wake_probe: tools/wake_probe/main.c | $(BUILD)
	$(CC) $(CFLAGS) $< -o $@ $(LDLIBS)

$(BUILD)/client: tools/client.c bpf/include/bpfusion_queue.h | $(BUILD)
	$(CC) $(CFLAGS) -Ibpf/include $< -o $@

$(BUILD)/echo_udp: tools/echo_udp.c | $(BUILD)
	$(CC) $(CFLAGS) $< -o $@
$(BUILD)/bpfusion_load: tools/bpfusion_load.c bpf/include/bpfusion_queue.h | $(BUILD)
	$(CC) $(CFLAGS) -Ibpf/include $< -o $@ $(LDLIBS)

$(BUILD)/perfcount: tools/perfcount.c | $(BUILD)
	$(CC) $(CFLAGS) $< -o $@

$(BUILD)/executor: executor/executor.cu bpf/include/bpfusion_queue.h \
                   executor/cuda_timer.h | $(BUILD)
	$(NVCC) -O3 -std=c++17 -arch=$(SM_ARCH) -Iexecutor -Ibpf/include \
		$< -o $@ $(LDLIBS)


run-executor: executor
	./$(BUILD)/executor $${N:-20000} $${WORK:-4} $${BATCH:-1}

$(BUILD):
	mkdir -p $(BUILD)

run-probe: all
	sudo ./$(BUILD)/wake_probe $(BUILD)/wake_probe.bpf.o 20000 50 1
	sudo ./$(BUILD)/wake_probe $(BUILD)/wake_probe.bpf.o 20000 50 0

clean:
	rm -rf $(BUILD)

.PHONY: qwen
qwen: $(BUILD)/qwen

$(BUILD)/qwen: executor/qwen.cu bpf/include/bpfusion_queue.h | $(BUILD)
	$(NVCC) -O3 -std=c++17 -arch=$(SM_ARCH) -Ibpf/include $< -o $@ $(LDLIBS)

# Same device kernel, host dispatch once per request: a mechanism control.
.PHONY: qwen-control
qwen-control: $(BUILD)/qwen_host_launch

$(BUILD)/qwen_host_launch: executor/qwen.cu bpf/include/bpfusion_queue.h | $(BUILD)
	$(NVCC) -O3 -std=c++17 -arch=$(SM_ARCH) -DBF_HOST_LAUNCH -Ibpf/include $< -o $@ $(LDLIBS)

# Device-launched HF graphs; Python captures only during bootstrap.
.PHONY: qwen-graph
qwen-graph: $(BUILD)/qwen_graph.so $(BUILD)/qwen_graph

$(BUILD)/qwen_graph.so: executor/qwen_graph.cu bpf/include/bpfusion_queue.h | $(BUILD)
	$(NVCC) -O3 -std=c++17 -arch=$(SM_ARCH) -rdc=true -shared -Xcompiler=-fPIC \
		-Ibpf/include $< -o $@ $(LDLIBS)

# Same concurrent GPU graph banks; host resumes once per retired request.
.PHONY: qwen-graph-control
qwen-graph-control: $(BUILD)/qwen_graph_host_launch.so $(BUILD)/qwen_graph_host_launch

$(BUILD)/qwen_graph_host_launch.so: executor/qwen_graph.cu bpf/include/bpfusion_queue.h | $(BUILD)
	$(NVCC) -O3 -std=c++17 -arch=$(SM_ARCH) -DBF_HOST_LAUNCH -rdc=true -shared -Xcompiler=-fPIC \
		-Ibpf/include $< -o $@ $(LDLIBS)

$(BUILD)/qwen_graph $(BUILD)/qwen_graph_host_launch $(BUILD)/qwen_graph_user_network $(BUILD)/qwen_graph_user_network_wait: executor/qwen_graph.py | $(BUILD)
	ln -sf $(abspath executor/qwen_graph.py) $@

# Same resident GPU graphs with an epoll userspace TCP/HTTP control.
.PHONY: qwen-graph-user-network
qwen-graph-user-network: $(BUILD)/qwen_graph_user_network.so $(BUILD)/qwen_graph_user_network

$(BUILD)/qwen_graph_user_network.so: executor/qwen_graph.cu executor/userspace_tcp.h bpf/include/bpfusion_queue.h | $(BUILD)
	$(NVCC) -O3 -std=c++17 -arch=$(SM_ARCH) -DBF_USER_NETWORK -rdc=true -shared -Xcompiler=-fPIC \
		-Ibpf/include $< -o $@ $(LDLIBS)

# CPU-efficient network control; model graphs and device dispatcher are unchanged.
.PHONY: qwen-graph-user-network-wait
qwen-graph-user-network-wait: $(BUILD)/qwen_graph_user_network_wait.so $(BUILD)/qwen_graph_user_network_wait

$(BUILD)/qwen_graph_user_network_wait.so: executor/qwen_graph.cu executor/userspace_tcp.h bpf/include/bpfusion_queue.h | $(BUILD)
	$(NVCC) -O3 -std=c++17 -arch=$(SM_ARCH) -DBF_USER_NETWORK -DBF_USER_NETWORK_WAIT -rdc=true -shared -Xcompiler=-fPIC \
		-Ibpf/include $< -o $@ $(LDLIBS)

# Upstream vLLM graphs with bootstrap-owned KV and GPU prefill/decode.
VLLM_PYTHON ?= python3
VLLM_CUDART = $(shell $(VLLM_PYTHON) -c 'import pathlib,torch; print(next(line.rsplit(" ",1)[-1] for line in pathlib.Path("/proc/self/maps").read_text().splitlines() if "/libcudart.so."+torch.version.cuda.split(".")[0] in line))')
VLLM_NAMES := vllm_graph vllm_graph_user_network_wait vllm_graph_trace vllm_graph_user_network_wait_trace vllm_graph_padded vllm_graph_padded_user_network_wait vllm_graph_padded_trace vllm_graph_padded_user_network_wait_trace

.PHONY: vllm-graph vllm-graph-user-network-wait vllm-graph-trace vllm-graph-padded
vllm-graph-padded: $(addprefix $(BUILD)/,$(addsuffix .so,$(filter %padded %padded_trace %padded_user_network_wait %padded_user_network_wait_trace,$(VLLM_NAMES)))) $(addprefix $(BUILD)/,$(filter %padded %padded_trace %padded_user_network_wait %padded_user_network_wait_trace,$(VLLM_NAMES)))
vllm-graph: $(BUILD)/vllm_graph.so $(BUILD)/vllm_graph
vllm-graph-user-network-wait: $(BUILD)/vllm_graph_user_network_wait.so $(BUILD)/vllm_graph_user_network_wait
vllm-graph-trace: $(BUILD)/vllm_graph_trace.so $(BUILD)/vllm_graph_trace $(BUILD)/vllm_graph_user_network_wait_trace.so $(BUILD)/vllm_graph_user_network_wait_trace

$(addprefix $(BUILD)/,$(VLLM_NAMES)): executor/vllm_graph.py | $(BUILD)
	ln -sf $(abspath executor/vllm_graph.py) $@

$(addprefix $(BUILD)/,$(addsuffix .so,$(VLLM_NAMES))): $(BUILD)/%.so: executor/vllm_graph.cu executor/userspace_tcp.h bpf/include/bpfusion_queue.h | $(BUILD)
	$(NVCC) -O3 -std=c++17 -arch=$(SM_ARCH) --cudart=none -dc -Xcompiler=-fPIC -Ibpf/include \
		$(if $(findstring user_network,$*),-DBF_USER_NETWORK -DBF_USER_NETWORK_WAIT) $(if $(findstring trace,$*),-DBF_TRACE) $(if $(findstring padded,$*),-DBF_PAD_PREFILL) $< -o $@.o
	$(NVCC) -arch=$(SM_ARCH) -dlink -Xcompiler=-fPIC $@.o -o $@.dlink.o
	$(CXX) -shared -Wl,-z,defs $@.o $@.dlink.o $(VLLM_CUDART) -Wl,-rpath,$(dir $(VLLM_CUDART)) -o $@ $(LDLIBS)
