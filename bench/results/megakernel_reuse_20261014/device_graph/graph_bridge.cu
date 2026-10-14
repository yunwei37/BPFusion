#include <cuda.h>
#include <cuda_runtime.h>
#include <cstdint>
#include <cstddef>
#include "amk_persist.cuh"

struct Bridge { CUmodule module{}; CUgraph graph{}; CUgraphExec exec{}; cudaGraphDeviceNode_t node{}; int* flags{}; };
static const char* last_stage="";
extern "C" const char* bridge_stage() { return last_stage; }
__global__ void acknowledge(int* flags) {
    __threadfence_system();
    atomicExch(flags+1,1);
}
__global__ void drive(cudaGraphExec_t exec,cudaGraphDeviceNode_t node,const int* input,int* flags) {
    if(threadIdx.x||blockIdx.x)return;
    cudaError_t err=cudaGraphKernelNodeSetParam(node,offsetof(amk_persist_program,K),input[2]);
    if(!err)err=cudaGraphKernelNodeSetParam(node,offsetof(amk_persist_program,base_pos),input[1]);
    if(!err)err=cudaGraphKernelNodeSetParam(node,offsetof(amk_persist_program,first_token),input[0]);
    if(!err)err=cudaGraphLaunch(exec,cudaStreamGraphFireAndForget);
    flags[0]=err;
    if(err)return;
    while(!atomicAdd(flags+1,0)) { __nanosleep(100); }
    __threadfence_system();
    atomicExch(flags+2,1);
}
static void release(Bridge* b) {
    if(b->exec)cuGraphExecDestroy(b->exec);
    if(b->graph)cuGraphDestroy(b->graph);
    if(b->module)cuModuleUnload(b->module);
    delete b;
}
extern "C" int bridge_create(const char* cubin,const amk_persist_launch_args* a,int* flags,Bridge** result) {
    Bridge* b=new Bridge; b->flags=flags;
#define C(call) do {last_stage=#call; CUresult e=(call); if(e){release(b);return (int)e;}} while(0)
#define R(call) do {last_stage=#call; cudaError_t e=(call); if(e){release(b);return 10000+(int)e;}} while(0)
    C(cuModuleLoad(&b->module,cubin));
    CUfunction function{}; C(cuModuleGetFunction(&function,b->module,"amk_megakernel_persist"));
    int device=0,sms=0,blocks=0;
    C(cuCtxGetDevice(&device));
    C(cuDeviceGetAttribute(&sms,CU_DEVICE_ATTRIBUTE_MULTIPROCESSOR_COUNT,device));
    C(cuOccupancyMaxActiveBlocksPerMultiprocessor(&blocks,function,a->threads_per_block,a->dyn_smem_bytes));
    if(a->grid_dim>blocks*sms){last_stage="cooperative occupancy insufficient";release(b);return 10001;}
    amk_persist_program pp{};
    pp.base.buffers=(const amk_buffer_t*)a->buffers_ptr; pp.base.n_buffers=a->n_buffers;
    pp.base.counters=(amk_counter_t*)a->counters_ptr; pp.base.n_counters=a->n_counters;
    pp.base.instructions=(const amk_instruction_t*)a->instructions_ptr; pp.base.n_instructions=a->n_instructions;
    pp.base.sm_queue_flat=(const int32_t*)a->sm_queue_flat_ptr;
    pp.base.sm_queue_off=(const int32_t*)a->sm_queue_off_ptr; pp.base.sm_queue_len=(const int32_t*)a->sm_queue_len_ptr;
    pp.base.num_sms=a->num_sms; pp.base.scratch=(unsigned char*)a->scratch_ptr;
    pp.base.scratch_bytes=a->scratch_bytes; pp.base.abort_flag=(int32_t*)a->abort_flag_ptr;
    pp.K=a->K; pp.base_pos=a->base_pos; pp.pos_cell=(int32_t*)a->pos_cell_ptr;
    pp.token_cell=(int32_t*)a->token_cell_ptr;
    pp.logits=(const amk_buffer_t*)a->buffers_table_ptr+a->logits_buf_idx;
    pp.generated=(int32_t*)a->generated_ptr; pp.first_token=a->first_token;
    void* model_args[]={&pp};
    C(cuGraphCreate(&b->graph,0));
    CUDA_KERNEL_NODE_PARAMS model{};
    model.func=function; model.gridDimX=a->grid_dim; model.gridDimY=model.gridDimZ=1;
    model.blockDimX=a->threads_per_block; model.blockDimY=model.blockDimZ=1;
    model.sharedMemBytes=a->dyn_smem_bytes; model.kernelParams=model_args;
    CUgraphNode node{}; C(cuGraphAddKernelNode(&node,b->graph,nullptr,0,&model));
    CUkernelNodeAttrValue attribute{}; attribute.cooperative=1;
    C(cuGraphKernelNodeSetAttribute(node,CU_KERNEL_NODE_ATTRIBUTE_COOPERATIVE,&attribute));
    attribute={}; attribute.deviceUpdatableKernelNode.deviceUpdatable=1;
    C(cuGraphKernelNodeSetAttribute(node,CU_KERNEL_NODE_ATTRIBUTE_DEVICE_UPDATABLE_KERNEL_NODE,&attribute));
    C(cuGraphKernelNodeGetAttribute(node,CU_KERNEL_NODE_ATTRIBUTE_DEVICE_UPDATABLE_KERNEL_NODE,&attribute));
    b->node=(cudaGraphDeviceNode_t)attribute.deviceUpdatableKernelNode.devNode;
    cudaFunction_t ack{}; R(cudaGetFuncBySymbol(&ack,(const void*)acknowledge));
    CUDA_KERNEL_NODE_PARAMS completion{};
    completion.func=(CUfunction)ack; completion.gridDimX=completion.gridDimY=completion.gridDimZ=1;
    completion.blockDimX=completion.blockDimY=completion.blockDimZ=1;
    void* ack_args[]={&flags}; completion.kernelParams=ack_args;
    CUgraphNode done{}; C(cuGraphAddKernelNode(&done,b->graph,&node,1,&completion));
    C(cuGraphInstantiate(&b->exec,b->graph,CUDA_GRAPH_INSTANTIATE_FLAG_DEVICE_LAUNCH));
    C(cuGraphUpload(b->exec,nullptr)); R(cudaDeviceSynchronize());
    *result=b; last_stage="created";return 0;
#undef C
#undef R
}
extern "C" int bridge_run(Bridge* b,const int* input) {
    CUgraph graph{}; CUgraphExec exec{}; CUgraphNode node{};
#define RUN(call) do {last_stage=#call; CUresult err=(call); if(err){if(exec)cuGraphExecDestroy(exec);if(graph)cuGraphDestroy(graph);return (int)err;}} while(0)
    cudaFunction_t function{}; cudaError_t err=cudaGetFuncBySymbol(&function,(const void*)drive);
    if(err)return 10000+err;
    cudaGraphExec_t child=(cudaGraphExec_t)b->exec;
    void* args[]={&child,&b->node,&input,&b->flags};
    CUDA_KERNEL_NODE_PARAMS params{};
    params.func=(CUfunction)function;params.gridDimX=params.gridDimY=params.gridDimZ=1;
    params.blockDimX=32;params.blockDimY=params.blockDimZ=1;params.kernelParams=args;
    RUN(cuGraphCreate(&graph,0)); RUN(cuGraphAddKernelNode(&node,graph,nullptr,0,&params));
    RUN(cuGraphInstantiate(&exec,graph,CUDA_GRAPH_INSTANTIATE_FLAG_DEVICE_LAUNCH));
    RUN(cuGraphUpload(exec,nullptr)); RUN(cuGraphLaunch(exec,nullptr)); RUN(cuCtxSynchronize());
    cuGraphExecDestroy(exec);cuGraphDestroy(graph);last_stage="run_complete";return 0;
#undef RUN
}
extern "C" void bridge_destroy(Bridge* b) { release(b); }
extern "C" size_t bridge_args_size() { return sizeof(amk_persist_launch_args); }
