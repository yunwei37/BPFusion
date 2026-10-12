// SPDX-License-Identifier: Apache-2.0
#include <cuda_runtime.h>
struct State {
 cudaGraphExec_t child;
 int *ids,*seq_lens,*block_table;
 long long *positions,*slot_mapping,*sampled,*output;
 unsigned batch,tokens,block_size,table_stride;
 unsigned step,child_launches,parent_calls,writes;
 int error;
};
struct Generation {
 State initial;
 State* state=nullptr;
 cudaGraph_t combined=nullptr,parent=nullptr;
 cudaGraphExec_t child=nullptr,parent_exec=nullptr;
 cudaStream_t stream=nullptr;
};
__global__ void generate_tokens(State* c){
 if(threadIdx.x || blockIdx.x)return;
 c->parent_calls++;
 if(c->error)return;
 if(c->step){
  for(unsigned i=0;i<c->batch;i++){
   c->output[i*c->tokens+c->step]=c->sampled[i];c->writes++;
  }
  if(c->step+1==c->tokens)return;
  for(unsigned i=0;i<c->batch;i++){
   long long position=++c->positions[i];
   unsigned column=(unsigned)(position/c->block_size);
   if(position<0 || column>=c->table_stride){c->error=-1;return;}
   c->ids[i]=(int)c->sampled[i];c->seq_lens[i]++;
   c->slot_mapping[i]=(long long)c->block_table[i*c->table_stride+column]*c->block_size+position%c->block_size;
  }
 }else{
  for(unsigned i=0;i<c->batch;i++){c->output[i*c->tokens]=c->ids[i];c->writes++;}
 }
 __threadfence();
 cudaError_t e=cudaGraphLaunch(c->child,cudaStreamGraphFireAndForget);
 if(e){c->error=(int)e;return;}
 c->child_launches++;c->step++;
 e=cudaGraphLaunch(cudaGetCurrentGraphExec(),cudaStreamGraphTailLaunch);
 if(e)c->error=(int)e;
}
extern "C" int gen_destroy(void* opaque){
 auto g=(Generation*)opaque;if(!g)return 0;cudaError_t first=cudaSuccess,e;
 #define CLEAN(call) do{e=call;if(e && first==cudaSuccess)first=e;}while(0)
 CLEAN(cudaStreamSynchronize(g->stream));
 if(g->parent_exec)CLEAN(cudaGraphExecDestroy(g->parent_exec));
 if(g->parent)CLEAN(cudaGraphDestroy(g->parent));
 if(g->child)CLEAN(cudaGraphExecDestroy(g->child));
 if(g->combined)CLEAN(cudaGraphDestroy(g->combined));
 if(g->state)CLEAN(cudaFree(g->state));
 delete g;return (int)first;
}
extern "C" int gen_create(void* body,void* head,void* stream,
 const unsigned long long* pointers,unsigned batch,unsigned tokens,
 unsigned block_size,unsigned table_stride,void** result,int* stage){
 *result=nullptr;auto g=new Generation;g->stream=(cudaStream_t)stream;cudaError_t e;
 #define STEP(k,call) do{*stage=k;e=call;if(e){gen_destroy(g);return (int)e;}}while(0)
 State c={};c.ids=(int*)pointers[0];c.positions=(long long*)pointers[1];
 c.seq_lens=(int*)pointers[2];c.slot_mapping=(long long*)pointers[3];
 c.block_table=(int*)pointers[4];c.sampled=(long long*)pointers[5];c.output=(long long*)pointers[6];
 c.batch=batch;c.tokens=tokens;c.block_size=block_size;c.table_stride=table_stride;
 STEP(1,cudaGraphCreate(&g->combined,0));cudaGraphNode_t body_node,head_node;
 STEP(2,cudaGraphAddChildGraphNode(&body_node,g->combined,nullptr,0,(cudaGraph_t)body));
 STEP(3,cudaGraphAddChildGraphNode(&head_node,g->combined,&body_node,1,(cudaGraph_t)head));
 STEP(4,cudaGraphInstantiateWithFlags(&g->child,g->combined,cudaGraphInstantiateFlagDeviceLaunch));
 STEP(5,cudaGraphUpload(g->child,g->stream));c.child=g->child;g->initial=c;
 STEP(6,cudaMalloc(&g->state,sizeof(State)));
 STEP(7,cudaGraphCreate(&g->parent,0));cudaGraphNode_t node;cudaKernelNodeParams params={};
 params.func=(void*)generate_tokens;params.gridDim=dim3(1);params.blockDim=dim3(32);
 void* args[]={&g->state};params.kernelParams=args;
 STEP(8,cudaGraphAddKernelNode(&node,g->parent,nullptr,0,&params));
 STEP(9,cudaGraphInstantiateWithFlags(&g->parent_exec,g->parent,cudaGraphInstantiateFlagDeviceLaunch));
 STEP(10,cudaGraphUpload(g->parent_exec,g->stream));
 STEP(11,cudaStreamSynchronize(g->stream));
 *stage=12;*result=g;return 0;
}
extern "C" int gen_run(void* opaque,unsigned* counters,int* device_error,int* stage){
 auto g=(Generation*)opaque;cudaError_t e;State final;
 #define RUN(k,call) do{*stage=k;e=call;if(e)return (int)e;}while(0)
 RUN(1,cudaMemcpyAsync(g->state,&g->initial,sizeof(State),cudaMemcpyHostToDevice,g->stream));
 RUN(2,cudaMemsetAsync(g->initial.output,255,g->initial.batch*g->initial.tokens*sizeof(long long),g->stream));
 RUN(3,cudaGraphLaunch(g->parent_exec,g->stream));
 RUN(4,cudaStreamSynchronize(g->stream));
 RUN(5,cudaMemcpy(&final,g->state,sizeof(State),cudaMemcpyDeviceToHost));
 counters[0]=final.child_launches;counters[1]=final.parent_calls;counters[2]=final.writes;
 *device_error=final.error;*stage=6;return 0;
}
extern "C" const char* gen_error(int code){return cudaGetErrorString((cudaError_t)code);}
