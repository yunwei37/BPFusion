// SPDX-License-Identifier: Apache-2.0
// Bootstrap glue only. All model instructions remain in upstream AMK's cubin.
#include <cuda.h>
#include <cuda_runtime.h>
#include <cstdint>
#include <cstddef>
#include "amk_persist.cuh"
struct Model { CUmodule module{}; CUfunction function{}; };
static const char* last_stage="";
extern "C" const char* amk_stage() { return last_stage; }
extern "C" size_t amk_args_size() { return sizeof(amk_persist_launch_args); }
__global__ void prepare(cudaGraphDeviceNode_t node,const long long* input,unsigned index,int* error) {
    if(threadIdx.x)return;
    int token=(int)input[index];
    cudaError_t e=cudaGraphKernelNodeSetParam(node,offsetof(amk_persist_program,first_token),token);
    if(e)atomicCAS(error,0,(int)e);
}
__global__ void selected(const int* token,long long* output) { if(!threadIdx.x)*output=*token; }
extern "C" int amk_open(const char* cubin,Model** output) {
    Model* m=new Model;CUresult e=cuModuleLoad(&m->module,cubin);
    if(!e)e=cuModuleGetFunction(&m->function,m->module,"amk_megakernel_persist");
    if(e){if(m->module)cuModuleUnload(m->module);delete m;return e;}
    *output=m;return 0;
}
extern "C" void amk_close(Model* m) { cuModuleUnload(m->module);delete m; }
extern "C" int amk_graph_create(Model* m,const amk_persist_launch_args* a,
    const long long* input,unsigned start,unsigned count,long long* output,int* error,CUgraph* result) {
    CUgraph graph{};CUresult e;
#define C(call) do {last_stage=#call;e=(call);if(e){if(graph)cuGraphDestroy(graph);return (int)e;}} while(0)
#define R(call) do {last_stage=#call;cudaError_t x=(call);if(x){if(graph)cuGraphDestroy(graph);return 10000+(int)x;}} while(0)
    cudaFunction_t prep{},head{};R(cudaGetFuncBySymbol(&prep,(const void*)prepare));
    R(cudaGetFuncBySymbol(&head,(const void*)selected));
    C(cuGraphCreate(&graph,0));
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
    pp.K=1;
    CUgraphNode previous{};
    for(unsigned position=start;position<start+count;position++) {
        pp.base_pos=position;pp.first_token=0;
        void* model_args[]={&pp};
        CUDA_KERNEL_NODE_PARAMS model{};
        model.func=m->function;model.gridDimX=a->grid_dim;model.gridDimY=model.gridDimZ=1;
        model.blockDimX=a->threads_per_block;model.blockDimY=model.blockDimZ=1;
        model.sharedMemBytes=a->dyn_smem_bytes;model.kernelParams=model_args;
        CUgraphNode model_node{};C(cuGraphAddKernelNode(&model_node,graph,nullptr,0,&model));
        CUkernelNodeAttrValue attribute{};attribute.cooperative=1;
        C(cuGraphKernelNodeSetAttribute(model_node,CU_KERNEL_NODE_ATTRIBUTE_COOPERATIVE,&attribute));
        attribute={};attribute.deviceUpdatableKernelNode.deviceUpdatable=1;
        C(cuGraphKernelNodeSetAttribute(model_node,CU_KERNEL_NODE_ATTRIBUTE_DEVICE_UPDATABLE_KERNEL_NODE,&attribute));
        C(cuGraphKernelNodeGetAttribute(model_node,CU_KERNEL_NODE_ATTRIBUTE_DEVICE_UPDATABLE_KERNEL_NODE,&attribute));
        cudaGraphDeviceNode_t node=(cudaGraphDeviceNode_t)attribute.deviceUpdatableKernelNode.devNode;
        unsigned input_index=count==1?0:position;
        void* prep_args[]={&node,&input,&input_index,&error};
        CUDA_KERNEL_NODE_PARAMS params{};params.func=(CUfunction)prep;
        params.gridDimX=params.gridDimY=params.gridDimZ=1;params.blockDimX=params.blockDimY=params.blockDimZ=1;
        params.kernelParams=prep_args;
        CUgraphNode prep_node{};C(cuGraphAddKernelNode(&prep_node,graph,previous?&previous:nullptr,previous?1:0,&params));
        C(cuGraphAddDependencies(graph,&prep_node,&model_node,nullptr,1));
        previous=model_node;
    }
    int* token=(int*)a->generated_ptr;void* head_args[]={&token,&output};
    CUDA_KERNEL_NODE_PARAMS params{};params.func=(CUfunction)head;
    params.gridDimX=params.gridDimY=params.gridDimZ=1;params.blockDimX=params.blockDimY=params.blockDimZ=1;params.kernelParams=head_args;
    CUgraphNode final{};C(cuGraphAddKernelNode(&final,graph,&previous,1,&params));
    *result=graph;last_stage="graph_created";return 0;
#undef C
#undef R
}
extern "C" int amk_graph_destroy(CUgraph graph) { return cuGraphDestroy(graph); }
