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

# Same GPU dispatcher/model graphs, one host service-graph launch per request.
.PHONY: qwen-graph-control
qwen-graph-control: $(BUILD)/qwen_graph_host_launch.so $(BUILD)/qwen_graph_host_launch

$(BUILD)/qwen_graph_host_launch.so: executor/qwen_graph.cu bpf/include/bpfusion_queue.h | $(BUILD)
	$(NVCC) -O3 -std=c++17 -arch=$(SM_ARCH) -DBF_HOST_LAUNCH -rdc=true -shared -Xcompiler=-fPIC \
		-Ibpf/include $< -o $@ $(LDLIBS)

$(BUILD)/qwen_graph $(BUILD)/qwen_graph_host_launch: executor/qwen_graph.py | $(BUILD)
	ln -sf $(abspath executor/qwen_graph.py) $@
