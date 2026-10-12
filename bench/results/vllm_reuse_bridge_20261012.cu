#include <cuda_runtime.h>
#include <vector>
struct Bridge {
 cudaGraphExec_t child=nullptr,parent_exec=nullptr;
 cudaGraph_t parent=nullptr;
 cudaStream_t stream=nullptr;
 int* status=nullptr;
};
__global__ void launch_child(cudaGraphExec_t child,int* status){
 status[0]=(int)cudaGraphLaunch(child,cudaStreamGraphFireAndForget);
 status[1]=1;
}
static cudaError_t catalog(cudaGraph_t graph,int* counts,int size){
 size_t n=0;cudaError_t e=cudaGraphGetNodes(graph,nullptr,&n);if(e)return e;
 std::vector<cudaGraphNode_t> nodes(n);
 e=cudaGraphGetNodes(graph,nodes.data(),&n);if(e)return e;
 for(auto node:nodes){
  cudaGraphNodeType type;e=cudaGraphNodeGetType(node,&type);if(e)return e;
  if((int)type<0||(int)type>=size)return cudaErrorInvalidValue;
  counts[(int)type]++;
  if(type==cudaGraphNodeTypeGraph){
   cudaGraph_t sub;e=cudaGraphChildGraphNodeGetGraph(node,&sub);if(e)return e;
   e=catalog(sub,counts,size);if(e)return e;
  }
 }
 return cudaSuccess;
}
extern "C" int bf_catalog(void* raw,int* counts,int size){
 for(int i=0;i<size;i++)counts[i]=0;
 return (int)catalog((cudaGraph_t)raw,counts,size);
}
extern "C" int bf_destroy(void* opaque){
 Bridge* b=(Bridge*)opaque;if(!b)return 0;
 cudaError_t first=cudaSuccess,e;
 #define CLEAN(call) do{e=(call);if(e && first==cudaSuccess)first=e;}while(0)
 if(b->stream)CLEAN(cudaStreamSynchronize(b->stream));
 if(b->parent_exec)CLEAN(cudaGraphExecDestroy(b->parent_exec));
 if(b->parent)CLEAN(cudaGraphDestroy(b->parent));
 if(b->child)CLEAN(cudaGraphExecDestroy(b->child));
 if(b->status)CLEAN(cudaFree(b->status));
 delete b;return (int)first;
}
extern "C" int bf_create(void* raw,void* stream,void** result,int* stage){
 *result=nullptr;Bridge* b=new Bridge;b->stream=(cudaStream_t)stream;
 cudaError_t e;
 #define TRY_STEP(k,call) do{*stage=k;e=(call);if(e){bf_destroy(b);return (int)e;}}while(0)
 TRY_STEP(1,cudaGraphInstantiateWithFlags(&b->child,(cudaGraph_t)raw,cudaGraphInstantiateFlagDeviceLaunch));
 TRY_STEP(2,cudaGraphUpload(b->child,b->stream));
 TRY_STEP(3,cudaMalloc(&b->status,2*sizeof(int)));
 TRY_STEP(4,cudaStreamSynchronize(b->stream));
 TRY_STEP(5,cudaGraphCreate(&b->parent,0));
 cudaGraphNode_t node;cudaKernelNodeParams params={};
 params.func=(void*)launch_child;params.gridDim=dim3(1);params.blockDim=dim3(1);
 void* args[]={&b->child,&b->status};params.kernelParams=args;
 TRY_STEP(6,cudaGraphAddKernelNode(&node,b->parent,nullptr,0,&params));
 TRY_STEP(8,cudaGraphInstantiateWithFlags(&b->parent_exec,b->parent,0));
 *stage=9;*result=b;return 0;
}
extern "C" int bf_run(void* opaque,int* device_status,int* entered,int* stage){
 Bridge* b=(Bridge*)opaque;cudaError_t e;int state[2]={-1,-1};
 #define RUN_STEP(k,call) do{*stage=k;e=(call);if(e)return (int)e;}while(0)
 RUN_STEP(1,cudaMemsetAsync(b->status,255,2*sizeof(int),b->stream));
 RUN_STEP(2,cudaGraphLaunch(b->parent_exec,b->stream));
 RUN_STEP(3,cudaStreamSynchronize(b->stream));
 RUN_STEP(4,cudaMemcpy(state,b->status,sizeof(state),cudaMemcpyDeviceToHost));
 *device_status=state[0];*entered=state[1];*stage=5;return 0;
}
extern "C" const char* bf_error(int code){return cudaGetErrorString((cudaError_t)code);}
