// SPDX-License-Identifier: Apache-2.0
// Correctness-first resident Qwen2 reference: one CTA executes full prefill,
// decode, KV attention and greedy sampling, directly on the pinned BPF page.
// No tensor-core optimization; no per-request host launch/copy/sampling.
#include <cuda_runtime.h>
#include <cuda_fp16.h>
#include <bpf/bpf.h>
#include <sys/mman.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <csignal>
#include "bpfusion_queue.h"

#define CUDA(call) do { cudaError_t e = (call); if (e != cudaSuccess) { \
    fprintf(stderr, "%s: %s\n", #call, cudaGetErrorString(e)); exit(1); } } while (0)
constexpr int CTX = 2 * BF_LLM_MAX_TOK;
struct Config { unsigned h, inter, layers, heads, kvheads, vocab; float eps, theta; };
struct Layer { half *norm, *q, *qb, *k, *kb, *v, *vb, *o, *post, *gate, *up, *down; };
struct Model { Config c; half *embed, *norm; Layer *layer; };
struct Scratch { float *x, *norm, *q, *k, *v, *att, *out, *gate, *up, *prob, *logits, *keys, *values; };

__device__ float fp16(float x) { return __half2float(__float2half_rn(x)); }
__device__ float warp_sum(float v) {
    for (int d=16; d; d/=2) v += __shfl_down_sync(0xffffffff, v, d);
    return v;
}
__device__ void matvec(float *out, const half *w, const half *bias,
                      const float *x, int rows, int cols) {
    int lane = threadIdx.x % 32, warp = threadIdx.x / 32;
    for (int row=warp; row<rows; row+=blockDim.x/32) {
        float sum=0;
        for (int col=lane; col<cols; col+=32)
            sum = fmaf(__half2float(w[(size_t)row*cols+col]), x[col], sum);
        sum = warp_sum(sum);
        if (!lane) out[row]=fp16(sum + (bias ? __half2float(bias[row]) : 0));
    }
    __syncthreads();
}
__device__ void rms(float *out, const float *x, const half *w, int n, float eps) {
    __shared__ float sums[8], inv;
    float sum=0;
    for (int i=threadIdx.x; i<n; i+=blockDim.x) sum += x[i]*x[i];
    sum=warp_sum(sum);
    if (!(threadIdx.x%32)) sums[threadIdx.x/32]=sum;
    __syncthreads();
    if (!threadIdx.x) { sum=0; for(int i=0;i<8;i++) sum+=sums[i]; inv=rsqrtf(sum/n+eps); }
    __syncthreads();
    for(int i=threadIdx.x;i<n;i+=blockDim.x) out[i]=fp16(fp16(x[i]*inv)*__half2float(w[i]));
    __syncthreads();
}
__device__ void rope(float *a, float *tmp, int n, int dim, int pos, float theta) {
    for(int i=threadIdx.x;i<n;i+=blockDim.x) {
        int d=i%dim, base=i-d, j=d%(dim/2);
        float angle=pos*powf(theta, -2.0f*j/dim);
        float cs=fp16(cosf(angle)), sn=fp16(sinf(angle));
        float rot=d<dim/2 ? -a[base+d+dim/2] : a[base+d-dim/2];
        tmp[i]=fp16(fp16(a[i]*cs)+fp16(rot*sn));
    }
    __syncthreads();
    for(int i=threadIdx.x;i<n;i+=blockDim.x) a[i]=tmp[i];
    __syncthreads();
}
__device__ void forward(Model m, Scratch s, unsigned token, int pos) {
    Config c=m.c;
    int h=c.h, dim=h/c.heads, kv=c.kvheads*dim;
    for(int i=threadIdx.x;i<h;i+=blockDim.x) s.x[i]=__half2float(m.embed[(size_t)token*h+i]);
    __syncthreads();
    for(unsigned l=0;l<c.layers;l++) {
        Layer w=m.layer[l];
        rms(s.norm,s.x,w.norm,h,c.eps);
        matvec(s.q,w.q,w.qb,s.norm,h,h);
        matvec(s.k,w.k,w.kb,s.norm,kv,h);
        matvec(s.v,w.v,w.vb,s.norm,kv,h);
        rope(s.q,s.out,h,dim,pos,c.theta);
        rope(s.k,s.norm,kv,dim,pos,c.theta);
        float *keys=s.keys+(size_t)l*CTX*kv;
        float *vals=s.values+(size_t)l*CTX*kv;
        for(int i=threadIdx.x;i<kv;i+=blockDim.x) {
            keys[pos*kv+i]=s.k[i]; vals[pos*kv+i]=s.v[i];
        }
        __syncthreads();
        // Each warp computes one head's causal scores and softmax.
        int lane=threadIdx.x%32, warp=threadIdx.x/32;
        for(unsigned head=warp;head<c.heads;head+=8) {
            int kh=head/(c.heads/c.kvheads);
            for(int t=0;t<=pos;t++) {
                float dot=0;
                for(int d=lane;d<dim;d+=32) dot+=s.q[head*dim+d]*keys[t*kv+kh*dim+d];
                dot=warp_sum(dot);
                if(!lane) s.prob[head*CTX+t]=fp16(fp16(dot)/sqrtf((float)dim));
            }
            __syncwarp();
            if(!lane) {
                float mx=-INFINITY, den=0;
                for(int t=0;t<=pos;t++) mx=fmaxf(mx,s.prob[head*CTX+t]);
                for(int t=0;t<=pos;t++) den+=expf(s.prob[head*CTX+t]-mx);
                for(int t=0;t<=pos;t++) s.prob[head*CTX+t]=fp16(expf(s.prob[head*CTX+t]-mx)/den);
            }
            __syncwarp();
            for(int d=lane;d<dim;d+=32) {
                float sum=0;
                for(int t=0;t<=pos;t++) sum=fmaf(s.prob[head*CTX+t],vals[t*kv+kh*dim+d],sum);
                s.att[head*dim+d]=fp16(sum);
            }
        }
        __syncthreads();
        matvec(s.out,w.o,nullptr,s.att,h,h);
        for(int i=threadIdx.x;i<h;i+=blockDim.x) s.x[i]=fp16(s.x[i]+s.out[i]);
        __syncthreads();
        rms(s.norm,s.x,w.post,h,c.eps);
        matvec(s.gate,w.gate,nullptr,s.norm,c.inter,h);
        matvec(s.up,w.up,nullptr,s.norm,c.inter,h);
        for(unsigned i=threadIdx.x;i<c.inter;i+=blockDim.x)
            s.gate[i]=fp16(fp16(s.gate[i]/(1+expf(-s.gate[i])))*s.up[i]);
        __syncthreads();
        matvec(s.out,w.down,nullptr,s.gate,h,c.inter);
        for(int i=threadIdx.x;i<h;i+=blockDim.x) s.x[i]=fp16(s.x[i]+s.out[i]);
        __syncthreads();
    }
}
__device__ unsigned sample(Model m, Scratch s) {
    __shared__ float maxima[256];
    __shared__ unsigned ids[256];
    rms(s.norm,s.x,m.norm,m.c.h,m.c.eps);
    matvec(s.logits,m.embed,nullptr,s.norm,m.c.vocab,m.c.h);
    float mx=-INFINITY; unsigned id=0;
    for(unsigned i=threadIdx.x;i<m.c.vocab;i+=blockDim.x)
        if(s.logits[i]>mx || (s.logits[i]==mx && i<id)) { mx=s.logits[i]; id=i; }
    maxima[threadIdx.x]=mx; ids[threadIdx.x]=id;
    __syncthreads();
    for(int d=128;d;d/=2) {
        if(threadIdx.x<d) {
            unsigned j=threadIdx.x+d;
            if(maxima[j]>maxima[threadIdx.x] || (maxima[j]==maxima[threadIdx.x] && ids[j]<ids[threadIdx.x])) {
                maxima[threadIdx.x]=maxima[j]; ids[threadIdx.x]=ids[j];
            }
        }
        __syncthreads();
    }
    return ids[0];
}
__global__ void resident(bf_page *p, Model m, Scratch s) {
    unsigned seen=0;
    __shared__ unsigned head, state, prompt, gen, token;
    for(;;) {
        __syncthreads();
        if(!threadIdx.x) {
            head=__ldcg(&p->llm_head);
            state=__ldcg(&p->llm[seen%BF_LLM_SLOTS].state);
            if(__ldcg((unsigned long long *)&p->stop_ns)) head=0xffffffff;
        }
        __syncthreads();
        if(head==0xffffffff) return;
        if(head==seen || state!=BF_PENDING) continue;
        bf_llm_slot *slot=&p->llm[seen%BF_LLM_SLOTS];
        if(!threadIdx.x) { prompt=__ldcg(&slot->n_prompt); gen=__ldcg(&slot->n_gen); }
        __syncthreads();
        if(prompt==0 || prompt>BF_LLM_MAX_TOK || gen==0 || gen>BF_LLM_MAX_TOK) return;
        for(unsigned pos=0;pos<prompt;pos++) {
            if(!threadIdx.x) token=__ldcg(&slot->tok_in[pos]);
            __syncthreads();
            if(token>=m.c.vocab) return;
            forward(m,s,token,pos);
        }
        for(unsigned k=0;k<gen;k++) {
            unsigned next=sample(m,s);
            if(!threadIdx.x) token=next;
            __syncthreads();
            if(!threadIdx.x) {
                __stcg(&slot->tok_out[k],token);
                __threadfence_system();
                __stcg(&slot->produced,k+1);
            }
            __syncthreads();
            if(k+1<gen) forward(m,s,token,prompt+k);
        }
        if(!threadIdx.x) {
            __threadfence_system();
            __stcg(&slot->state,(unsigned)BF_DONE);
        }
        __syncthreads();
        seen++;
    }
}

static void stop_signal(int) {}

int main(int argc,char **argv) {
    signal(SIGTERM,stop_signal); signal(SIGINT,stop_signal);
    if(argc<2) { fprintf(stderr,"usage: qwen WEIGHTS.bin [seconds]\n"); return 1; }
    FILE *f=fopen(argv[1],"rb"); if(!f) { perror("weights"); return 1; }
    Config c; if(fread(&c,sizeof(c),1,f)!=1) return 1;
    if(c.h%32 || c.h%c.heads || c.heads%c.kvheads || (c.h/c.heads)%2) return 1;
    fseek(f,0,SEEK_END); size_t bytes=ftell(f)-sizeof(c); fseek(f,sizeof(c),SEEK_SET);
    std::vector<half> host(bytes/sizeof(half));
    if(fread(host.data(),1,bytes,f)!=bytes) return 1;
    fclose(f);
    half *weights; CUDA(cudaMalloc(&weights,bytes));
    CUDA(cudaMemcpy(weights,host.data(),bytes,cudaMemcpyHostToDevice));
    host.clear(); host.shrink_to_fit();
    half *cursor=weights;
    auto take=[&](size_t n) { half *p=cursor; cursor+=n; return p; };
    Model m={}; m.c=c; m.embed=take((size_t)c.vocab*c.h);
    int kv=c.kvheads*(c.h/c.heads);
    std::vector<Layer> layers(c.layers);
    for(auto &l:layers) {
        l.norm=take(c.h); l.q=take((size_t)c.h*c.h); l.qb=take(c.h);
        l.k=take((size_t)kv*c.h); l.kb=take(kv); l.v=take((size_t)kv*c.h); l.vb=take(kv);
        l.o=take((size_t)c.h*c.h); l.post=take(c.h); l.gate=take((size_t)c.inter*c.h);
        l.up=take((size_t)c.inter*c.h); l.down=take((size_t)c.h*c.inter);
    }
    m.norm=take(c.h);
    if((size_t)(cursor-weights)*sizeof(half)!=bytes) { fprintf(stderr,"weight layout mismatch\n"); return 1; }
    CUDA(cudaMalloc(&m.layer,c.layers*sizeof(Layer)));
    CUDA(cudaMemcpy(m.layer,layers.data(),c.layers*sizeof(Layer),cudaMemcpyHostToDevice));
    Scratch s={};
    auto alloc=[&](float **p,size_t n) { CUDA(cudaMalloc(p,n*sizeof(float))); };
    alloc(&s.x,c.h); alloc(&s.norm,c.h); alloc(&s.q,c.h); alloc(&s.k,kv); alloc(&s.v,kv);
    alloc(&s.att,c.h); alloc(&s.out,c.h); alloc(&s.gate,c.inter); alloc(&s.up,c.inter);
    alloc(&s.prob,c.heads*CTX); alloc(&s.logits,c.vocab);
    alloc(&s.keys,(size_t)c.layers*CTX*kv); alloc(&s.values,(size_t)c.layers*CTX*kv);
    int fd=bpf_obj_get("/sys/fs/bpf/bpfusion_ctl"); if(fd<0) { perror("bpf_obj_get"); return 1; }
    auto *page=(bf_page *)mmap(nullptr,BF_PAGE_MMAP_BYTES,PROT_READ|PROT_WRITE,MAP_SHARED,fd,0);
    close(fd); if(page==MAP_FAILED) { perror("mmap"); return 1; }
    CUDA(cudaHostRegister(page,BF_PAGE_MMAP_BYTES,cudaHostRegisterMapped));
    bf_page *device; CUDA(cudaHostGetDevicePointer((void **)&device,page,0));
    int listener=socket(AF_INET,SOCK_STREAM,0), yes=1;
    setsockopt(listener,SOL_SOCKET,SO_REUSEADDR,&yes,sizeof(yes));
    sockaddr_in addr={}; addr.sin_family=AF_INET; addr.sin_port=htons(BF_LLM_TCP_PORT);
    addr.sin_addr.s_addr=htonl(INADDR_LOOPBACK);
    if(bind(listener,(sockaddr *)&addr,sizeof(addr)) || listen(listener,SOMAXCONN)) { perror("listen"); return 1; }
    // Listener creation is bootstrap only. No host accept/read/send loop.
    __atomic_store_n(&page->stop_ns,0,__ATOMIC_RELEASE);
    resident<<<1,256>>>(device,m,s); CUDA(cudaGetLastError());
    printf("resident Qwen ready: %u layers h=%u vocab=%u; one launch, no host request worker\n",c.layers,c.h,c.vocab);
    fflush(stdout);
    sleep(argc>2 ? atoi(argv[2]) : 60);
    __atomic_store_n(&page->stop_ns,1,__ATOMIC_RELEASE);
    CUDA(cudaDeviceSynchronize());
    close(listener);
    CUDA(cudaHostUnregister(page)); munmap(page,BF_PAGE_MMAP_BYTES);
    printf("resident Qwen stopped\n");
    return 0;
}
