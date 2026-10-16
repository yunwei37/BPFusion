// Private causal-timeline instrumentation; not a public/runtime option.
#include <ctime>
#include <algorithm>
struct TailRecord {
 unsigned kind,seq,offset,length,header;
 int result;
 unsigned long long ns,client_ns,tag,previous_ns,begin_ns;
};
struct TailBuffer {unsigned count,capacity;TailRecord *records;};
__device__ TailBuffer tail_buffer;
static std::vector<TailRecord> tail_cpu;
static std::vector<TailRecord> tail_calibration;
static unsigned tail_capacity,tail_cpu_overflow;
static TailRecord *tail_device_records;
__device__ unsigned long long tail_now() {
 unsigned long long v;asm volatile("mov.u64 %0, %%globaltimer;":"=l"(v));return v;
}
__device__ void tail_gpu(unsigned kind,unsigned seq,unsigned offset,unsigned length,
 unsigned header,int result,unsigned long long client_ns,unsigned long long tag=0,
 unsigned long long previous=0,unsigned long long begin=0) {
 unsigned n=atomicAdd(&tail_buffer.count,1u);
 if(n<tail_buffer.capacity)tail_buffer.records[n]={kind,seq,offset,length,header,result,tail_now(),client_ns,tag,previous,begin};
}
static unsigned long long tail_host_now() {
 timespec ts{};clock_gettime(CLOCK_MONOTONIC,&ts);return (unsigned long long)ts.tv_sec*1000000000ULL+ts.tv_nsec;
}
static void tail_host(unsigned kind,unsigned offset,unsigned length,unsigned header,
 int result,unsigned long long client_ns) {
 if(tail_cpu.size()<tail_capacity)tail_cpu.push_back({kind,0,offset,length,header,result,tail_host_now(),client_ns,0,0,0});
 else tail_cpu_overflow++;
}
__global__ void tail_clock(unsigned long long *stamp) {
 if(!threadIdx.x&&!blockIdx.x)*stamp=tail_now();
}
static int tail_calibrate(unsigned phase) {
 unsigned long long *p,sample;
 CUDA(cudaMalloc(&p,sizeof(sample)));
 for(unsigned i=0;i<16;i++) {
  auto begin=tail_host_now();tail_clock<<<1,1>>>(p);
  CUDA(cudaDeviceSynchronize());CUDA(cudaMemcpy(&sample,p,sizeof(sample),cudaMemcpyDeviceToHost));
  auto end=tail_host_now();tail_calibration.push_back({100+phase,i,0,0,0,0,sample,begin,0,end,0});
 }
 CUDA(cudaFree(p));return 0;
}
static int tail_initialize(unsigned requests) {
 tail_capacity=requests*(BF_LLM_MAX_TOK*4+16)+1024;
 tail_cpu.reserve(tail_capacity);
 CUDA(cudaMalloc(&tail_device_records,tail_capacity*sizeof(TailRecord)));
 TailBuffer b{0,tail_capacity,tail_device_records};CUDA(cudaMemcpyToSymbol(tail_buffer,&b,sizeof(b)));
 return tail_calibrate(0);
}
static int tail_finish(const char *path) {
 if(tail_calibrate(1))return 1;
 TailBuffer b;CUDA(cudaMemcpyFromSymbol(&b,tail_buffer,sizeof(b)));
 std::vector<TailRecord> records(std::min(b.count,b.capacity));
 CUDA(cudaMemcpy(records.data(),tail_device_records,records.size()*sizeof(TailRecord),cudaMemcpyDeviceToHost));
 std::string output=std::string(path)+".timeline.jsonl";FILE *f=fopen(output.c_str(),"w");if(!f)return 1;
 auto emit=[&](const TailRecord &x,const char *clock) {
  fprintf(f,"{\"kind\":%u,\"seq\":%u,\"offset\":%u,\"length\":%u,\"header\":%u,\"result\":%d,\"ns\":%llu,\"client_ns\":%llu,\"tag\":%llu,\"previous_ns\":%llu,\"begin_ns\":%llu,\"clock\":\"%s\"}\n",
   x.kind,x.seq,x.offset,x.length,x.header,x.result,x.ns,x.client_ns,x.tag,x.previous_ns,x.begin_ns,clock);
 };
 for(auto &x:tail_calibration)emit(x,"bracket_gpu_host");
 for(auto &x:records)emit(x,"gpu_globaltimer");
 for(auto &x:tail_cpu)emit(x,"host_monotonic");
 fprintf(f,"{\"event\":\"terminal\",\"gpu_count\":%u,\"capacity\":%u,\"cpu_count\":%zu,\"cpu_overflow\":%u}\n",b.count,b.capacity,tail_cpu.size(),tail_cpu_overflow);
 int failed=fclose(f)||b.count>b.capacity||tail_cpu_overflow;CUDA(cudaFree(tail_device_records));return failed;
}
