// SPDX-License-Identifier: Apache-2.0
// GPU-tail graph dispatch: host work is model/graph bootstrap and shutdown only.
#include <cuda_runtime.h>
#include <bpf/bpf.h>
#include <sys/mman.h>
#include <sys/syscall.h>
#include <fcntl.h>
#include <netinet/in.h>
#include <unistd.h>
#include <cstdio>
#include <csignal>
#include <vector>
#include "bpfusion_queue.h"
#define CUDA(x) do { cudaError_t e=(x); if(e!=cudaSuccess) { fprintf(stderr,"%s: %s\n",#x,cudaGetErrorString(e)); return (int)e; } } while(0)
struct Step { cudaGraphExec_t graph; long long *output; };
struct Control { unsigned seen,k,prompt,gen,step,phase,error,launches; };

// System-scope acquire protects host publication and forbids polling-load
// elimination; a cache modifier alone does not give synchronization semantics.
__device__ unsigned queue_load(const unsigned *p) {
    unsigned value;asm volatile("ld.acquire.sys.global.u32 %0, [%1];" : "=r"(value) : "l"(p) : "memory");return value;
}
__device__ unsigned long long queue_load(const unsigned long long *p) {
    unsigned long long value;asm volatile("ld.acquire.sys.global.u64 %0, [%1];" : "=l"(value) : "l"(p) : "memory");return value;
}

__global__ void dispatch(bf_page *p,Step *steps,long long *input,unsigned vocab,Control *c) {
    if(threadIdx.x || blockIdx.x) return;
    bf_llm_slot *slot=&p->llm[c->seen%BF_LLM_SLOTS];
    if(!c->phase) {
        // Idle waiting is on the GPU. A tail launch resumes after all model
        // graph work finishes, so no completion flag races graph reuse.
        while(queue_load(&p->llm_head)==c->seen || queue_load(&slot->state)!=BF_PENDING) {
            if(queue_load((unsigned long long *)&p->stop_ns)) return;
        }
        if(queue_load((unsigned long long *)&p->stop_ns)) return;
        unsigned np=__ldcg(&slot->n_prompt),ng=__ldcg(&slot->n_gen);
        bool bad=!np || np>BF_LLM_MAX_TOK || !ng || ng>BF_LLM_MAX_TOK;
        for(unsigned i=0;i<np && i<BF_LLM_MAX_TOK;i++) {
            unsigned token=__ldcg(&slot->tok_in[i]);
            if(token>=vocab) bad=true;
            input[i]=token;
        }
        unsigned short flags=__ldcg(&slot->pad);
        __threadfence_system();
        __stcg(&slot->pad,(unsigned short)((flags&~BF_LLM_VALIDATING)|(bad ? BF_LLM_REJECTED : 0)));
        if(bad) {
            __stcg(&slot->produced,0u);__threadfence_system();__stcg(&slot->state,(unsigned)BF_DONE);
            c->seen++;
            cudaError_t e=cudaGraphLaunch(cudaGetCurrentGraphExec(),cudaStreamGraphTailLaunch);
            if(e!=cudaSuccess) c->error=e;
            return;
        }
        c->prompt=np;c->gen=ng;c->k=0;c->step=np;c->phase=1;
    } else {
        unsigned token=(unsigned)*steps[c->step].output;
        __stcg(&slot->tok_out[c->k],token);__threadfence_system();__stcg(&slot->produced,c->k+1);
        if(++c->k==c->gen) {
            __threadfence_system();__stcg(&slot->state,(unsigned)BF_DONE);
            c->seen++;c->phase=0;
            cudaError_t e=cudaGraphLaunch(cudaGetCurrentGraphExec(),cudaStreamGraphTailLaunch);
            if(e!=cudaSuccess) c->error=e;
            return;
        }
        input[0]=token;c->step=BF_LLM_MAX_TOK+c->prompt+c->k-1;
    }
    cudaError_t e=cudaGraphLaunch(steps[c->step].graph,cudaStreamGraphTailLaunch);
    if(e!=cudaSuccess) { c->error=e;return; }
    c->launches++;
    e=cudaGraphLaunch(cudaGetCurrentGraphExec(),cudaStreamGraphTailLaunch);
    if(e!=cudaSuccess) c->error=e;
}
extern "C" unsigned max_tokens() { return BF_LLM_MAX_TOK; }
static void stop_signal(int) {}
extern "C" int serve(const unsigned long long *graphs,const unsigned long long *outputs,unsigned count,unsigned long long input_ptr,unsigned vocab,unsigned layers,unsigned h,unsigned seconds) {
    std::vector<Step> host(count);
    for(unsigned i=1;i<count;i++) {
        CUDA(cudaGraphInstantiate(&host[i].graph,(cudaGraph_t)graphs[i],cudaGraphInstantiateFlagDeviceLaunch));
        CUDA(cudaGraphUpload(host[i].graph,0));host[i].output=(long long *)outputs[i];
    }
    Step *steps;CUDA(cudaMalloc(&steps,count*sizeof(Step)));CUDA(cudaMemcpy(steps,host.data(),count*sizeof(Step),cudaMemcpyHostToDevice));
    Control *control;CUDA(cudaMalloc(&control,sizeof(Control)));CUDA(cudaMemset(control,0,sizeof(Control)));
    int fd=bpf_obj_get("/sys/fs/bpf/bpfusion_ctl");if(fd<0) { perror("bpf_obj_get");return 1; }
    bf_page *page=(bf_page *)mmap(nullptr,BF_PAGE_MMAP_BYTES,PROT_READ|PROT_WRITE,MAP_SHARED,fd,0);
    if(page==MAP_FAILED) { perror("mmap");return 1; }
    CUDA(cudaHostRegister(page,BF_PAGE_MMAP_BYTES,cudaHostRegisterMapped));
    bf_page *device;CUDA(cudaHostGetDevicePointer((void **)&device,page,0));
    int listener=socket(AF_INET,SOCK_STREAM,0),yes=1;setsockopt(listener,SOL_SOCKET,SO_REUSEADDR,&yes,sizeof(yes));
    sockaddr_in addr={};addr.sin_family=AF_INET;addr.sin_port=htons(BF_LLM_TCP_PORT);addr.sin_addr.s_addr=htonl(INADDR_LOOPBACK);
    if(bind(listener,(sockaddr *)&addr,sizeof(addr)) || listen(listener,SOMAXCONN)) { perror("listen");return 1; }
    __atomic_store_n(&page->stop_ns,0,__ATOMIC_RELEASE);
    long long *input=(long long *)input_ptr;
    void *args[]={&device,&steps,&input,&vocab,&control};
    cudaKernelNodeParams params={};params.func=(void *)dispatch;params.gridDim=dim3(1);params.blockDim=dim3(32);params.kernelParams=args;
    cudaGraph_t graph;CUDA(cudaGraphCreate(&graph,0));cudaGraphNode_t node;CUDA(cudaGraphAddKernelNode(&node,graph,nullptr,0,&params));
    cudaGraphExec_t parent;CUDA(cudaGraphInstantiate(&parent,graph,cudaGraphInstantiateFlagDeviceLaunch));CUDA(cudaGraphUpload(parent,0));CUDA(cudaDeviceSynchronize());
    int module=open("module/bfusion_tx.ko",O_RDONLY|O_CLOEXEC);if(module<0) { perror("module open");return 1; }
    char params_module[80];snprintf(params_module,sizeof(params_module),"map_fd=%d listen_fd=%d",fd,listener);
    if(syscall(SYS_finit_module,module,params_module,0)) { perror("finit_module");return 1; }
    close(module);close(fd);
    signal(SIGTERM,stop_signal);signal(SIGINT,stop_signal);
    cudaError_t launched=cudaGraphLaunch(parent,0);
    if(launched==cudaSuccess) {
        printf("resident Qwen ready: %u layers h=%u vocab=%u; device-tail graphs, dispatch=resident\n",layers,h,vocab);fflush(stdout);
        sleep(seconds);
    }
    __atomic_store_n(&page->stop_ns,1,__ATOMIC_RELEASE);
    cudaError_t finished=cudaDeviceSynchronize();
    if(syscall(SYS_delete_module,"bfusion_tx",0)) { perror("delete_module");return 1; }
    close(listener);CUDA(launched);CUDA(finished);
    Control result;CUDA(cudaMemcpy(&result,control,sizeof(result),cudaMemcpyDeviceToHost));
    CUDA(cudaHostUnregister(page));munmap(page,BF_PAGE_MMAP_BYTES);
    CUDA(cudaGraphExecDestroy(parent));CUDA(cudaGraphDestroy(graph));CUDA(cudaFree(steps));CUDA(cudaFree(control));
    for(unsigned i=1;i<count;i++) CUDA(cudaGraphExecDestroy(host[i].graph));
    printf("resident Qwen stopped: dispatch=resident launches=1 device_graph_launches=%u graph_error=%u\n",result.launches,result.error);fflush(stdout);
    return result.error;
}
