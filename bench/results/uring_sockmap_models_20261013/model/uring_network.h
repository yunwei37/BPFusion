#include <cuda_runtime.h>
#include <linux/io_uring.h>
#include <sys/mman.h>
#include <sys/syscall.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cerrno>
#include <cstdint>

#include <bpf/bpf.h>
#include "bpfusion_queue.h"
struct Ring {
    unsigned *sh,*st,*flags,*ch,*ct,*dropped,*overflow;
    io_uring_sqe *sqes;io_uring_cqe *cqes;unsigned smask,cmask;
};
struct Report {
    unsigned status,accepted,received,sent,bytes,idle_observed,closed,eof;
    unsigned sq_head,sq_tail,cq_head,cq_tail,dropped,overflow,head,reserved;
    int last_res;unsigned last_prompt,last_token;
};
__device__ unsigned acquire(const unsigned *p) {
    unsigned v;asm volatile("ld.acquire.sys.global.u32 %0, [%1];":"=r"(v):"l"(p):"memory");return v;
}
__device__ unsigned long long acquire64(const unsigned long long *p) {
    unsigned long long v;asm volatile("ld.acquire.sys.global.u64 %0, [%1];":"=l"(v):"l"(p):"memory");return v;
}
__device__ void release(unsigned *p,unsigned v) {
    asm volatile("st.release.sys.global.u32 [%0], %1;"::"l"(p),"r"(v):"memory");
}
__device__ unsigned long long timer() {
    unsigned long long v;asm volatile("mov.u64 %0, %%globaltimer;":"=l"(v));return v;
}
__device__ void submit(Ring r,io_uring_sqe entry) {
    unsigned tail=acquire(r.st);
    r.sqes[tail&r.smask]=entry;__threadfence_system();release(r.st,tail+1);
}
__device__ int complete(Ring r,unsigned long long id,Report *out) {
    unsigned h=acquire(r.ch);auto until=timer()+5000000000ULL;
    while(acquire(r.ct)==h) {
        if(timer()>until) {out->status=1;return -10000;}
        __nanosleep(1000);
    }
    auto cqe=r.cqes[h&r.cmask];release(r.ch,h+1);
    out->last_res=cqe.res;
    if(cqe.user_data!=id) {out->status=2;return -10000;}
    return cqe.res;
}
__device__ void idle_check(Ring r,Report *out) {
    auto until=timer()+2000000000ULL;
    while(timer()<until)__nanosleep(100000);
    if(acquire(r.flags)&IORING_SQ_NEED_WAKEUP)++out->idle_observed;
}
__global__ void warm() {}
__global__ void uring_network(Ring r,bf_page *page,unsigned char *buffer,unsigned long long host_buffer,Report *out) {
    if(threadIdx.x||blockIdx.x)return;
    idle_check(r,out);
    int peer=complete(r,0xa77,out);
    if(peer<0) {if(!out->status)out->status=3;goto done;}
    out->accepted=1;
    for(unsigned cycle=0;cycle<12;++cycle) {
        io_uring_sqe entry{};
        entry.opcode=IORING_OP_RECV;entry.fd=peer;entry.addr=host_buffer;
        entry.len=16384;entry.user_data=100+cycle;
        submit(r,entry);
        if(cycle<8)idle_check(r,out);
        int got=complete(r,100+cycle,out);
        if(got<=0) {if(!out->status)out->status=4;goto done;}
        ++out->received;
        unsigned index=cycle%BF_LLM_SLOTS;
        auto *slot=&page->llm[index];
        auto until=timer()+5000000000ULL;
        while(acquire(&slot->state)!=BF_DONE) {
            if(timer()>until) {out->status=5;goto done;}
            __nanosleep(1000);
        }
        unsigned np=acquire(&slot->n_prompt);
        auto *address=(sockaddr_in*)(buffer+20000);
        if(acquire(&page->llm_head)!=cycle+1||!np||np>BF_LLM_MAX_TOK||
           acquire(&slot->n_gen)!=1||acquire64(&slot->client_ns)!=1000+cycle||
           slot->addr_be!=address->sin_addr.s_addr||slot->port_be!=address->sin_port||
           slot->pad!=(cycle%2?2u:1u)||acquire(&slot->produced)!=1) {
            out->status=6;goto done;
        }
        unsigned token=acquire(&slot->tok_out[0]);
        out->last_prompt=np;out->last_token=token;
        unsigned length=0;
        if(cycle%2) {
            const char header[]="HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: 4\r\n\r\n";
            for(unsigned i=0;i<sizeof(header)-1;++i)buffer[22000+length++]=header[i];
        }
        for(unsigned i=0;i<4;++i)buffer[22000+length++]=(token>>(i*8))&255;
        unsigned sent=0;
        while(sent<length) {
            entry={};entry.opcode=IORING_OP_SEND;entry.fd=peer;
            entry.addr=host_buffer+22000+sent;entry.len=length-sent;
            entry.msg_flags=MSG_NOSIGNAL;
            entry.user_data=(0xbff0ULL<<48)|((unsigned long long)(length-sent)<<32)|cycle;
            submit(r,entry);
            int bytes=complete(r,entry.user_data,out);
            if(bytes<=0||(unsigned)bytes>length-sent) {if(!out->status)out->status=7;goto done;}
            sent+=bytes;out->bytes+=bytes;++out->sent;
        }
        // Kernel eBPF completion owns reclamation; no GPU/CPU shared RMW.
    }
    {
        io_uring_sqe entry{};
        entry.opcode=IORING_OP_RECV;entry.fd=peer;entry.addr=host_buffer;entry.len=16384;entry.user_data=0xe0f;
        submit(r,entry);
        int result=complete(r,0xe0f,out);
        if(result!=0) {if(!out->status)out->status=8;goto done;}
        out->eof=1;
        entry={};entry.opcode=IORING_OP_CLOSE;entry.fd=peer;entry.user_data=0xc105e;
        submit(r,entry);
        if(complete(r,0xc105e,out)!=0) {if(!out->status)out->status=9;goto done;}
        out->closed=1;
    }
done:
    out->sq_head=acquire(r.sh);out->sq_tail=acquire(r.st);
    out->cq_head=acquire(r.ch);out->cq_tail=acquire(r.ct);
    out->dropped=acquire(r.dropped);out->overflow=acquire(r.overflow);
    out->head=acquire(&page->llm_head);out->reserved=acquire(&page->llm_reserved);
    __threadfence_system();
}
static void check(cudaError_t e,const char *what) {
    if(e!=cudaSuccess) {fprintf(stderr,"%s: %s\n",what,cudaGetErrorString(e));exit(10);}
}
static void *memory() {
    void *p=mmap(nullptr,65536,PROT_READ|PROT_WRITE,MAP_PRIVATE|MAP_ANONYMOUS,-1,0);
    if(p==MAP_FAILED) {perror("mmap");exit(11);}
    memset(p,0,65536);check(cudaHostRegister(p,65536,cudaHostRegisterMapped),"cudaHostRegister");return p;
}
static void *device(void *p) {void *d;check(cudaHostGetDevicePointer(&d,p,0),"cudaHostGetDevicePointer");return d;}
struct UringNetwork { void *sq,*rings,*buffer;Report *report;int ringfd;cudaStream_t stream; };
static int uring_start(bf_page *page,bf_page *dpage,int listener,UringNetwork *net) {
    int host_atomic=0;check(cudaDeviceGetAttribute(&host_atomic,cudaDevAttrHostNativeAtomicSupported,0),"host atomics");
    printf("CAPABILITY host_native_atomic=%d\n",host_atomic);

    char *sq=(char*)memory(),*rings=(char*)memory(),*buffer=(char*)memory();
    auto *report=(Report*)memory();
    auto *dsq=(char*)device(sq),*drings=(char*)device(rings);
    auto *dbuffer=(unsigned char*)device(buffer);
    auto *dreport=(Report*)device(report);
    *(socklen_t*)(buffer+21000)=sizeof(sockaddr_in);
    io_uring_params p{};p.flags=IORING_SETUP_SQPOLL|IORING_SETUP_NO_MMAP|IORING_SETUP_NO_SQARRAY;
    p.sq_off.user_addr=(uint64_t)sq;p.cq_off.user_addr=(uint64_t)rings;
    int ringfd=syscall(__NR_io_uring_setup,8,&p);
    if(ringfd<0){perror("io_uring_setup");return 16;}
    Ring r{};
    r.sh=(unsigned*)(drings+p.sq_off.head);r.st=(unsigned*)(drings+p.sq_off.tail);
    r.flags=(unsigned*)(drings+p.sq_off.flags);r.ch=(unsigned*)(drings+p.cq_off.head);r.ct=(unsigned*)(drings+p.cq_off.tail);
    r.dropped=(unsigned*)(drings+p.sq_off.dropped);r.overflow=(unsigned*)(drings+p.cq_off.overflow);
    r.sqes=(io_uring_sqe*)dsq;r.cqes=(io_uring_cqe*)(drings+p.cq_off.cqes);
    r.smask=*(unsigned*)(rings+p.sq_off.ring_mask);r.cmask=*(unsigned*)(rings+p.cq_off.ring_mask);
    auto *entries=(io_uring_sqe*)sq;
    entries[0].opcode=IORING_OP_NOP;entries[0].user_data=0xb007;
    entries[1].opcode=IORING_OP_ACCEPT;entries[1].fd=listener;entries[1].addr=(uint64_t)(buffer+20000);
    entries[1].off=(uint64_t)(buffer+21000);entries[1].user_data=0xa77;
    __atomic_store_n((unsigned*)(rings+p.sq_off.tail),2,__ATOMIC_RELEASE);
    if(syscall(__NR_io_uring_enter,ringfd,0,0,IORING_ENTER_SQ_WAKEUP,nullptr,0)<0){perror("wake");return 17;}
    for(unsigned tries=0;__atomic_load_n((unsigned*)(rings+p.cq_off.tail),__ATOMIC_ACQUIRE)==0;++tries) {
        if(tries>=2000)return 18;usleep(1000);
    }
    auto *cqe=(io_uring_cqe*)(rings+p.cq_off.cqes);if(cqe[0].res||cqe[0].user_data!=0xb007)return 19;
    __atomic_store_n((unsigned*)(rings+p.cq_off.head),1,__ATOMIC_RELEASE);
    net->sq=sq;net->rings=rings;net->buffer=buffer;net->report=report;net->ringfd=ringfd;
    check(cudaStreamCreateWithFlags(&net->stream,cudaStreamNonBlocking),"network stream");
    uring_network<<<1,1,0,net->stream>>>(r,dpage,dbuffer,(uint64_t)buffer,dreport);
    check(cudaGetLastError(),"network launch");
    printf("NET_READY pid=%d port=%u setup_flags=%u features=%u\n",getpid(),BF_LLM_TCP_PORT,p.flags,p.features);fflush(stdout);
    return 0;
}
static int uring_finish(UringNetwork *net) {
    check(cudaStreamSynchronize(net->stream),"network finish");
    auto *report=net->report;void *sq=net->sq,*rings=net->rings,*buffer=net->buffer;
    printf("RESULT {\"status\":%u,\"accepted\":%u,\"received\":%u,\"sent\":%u,\"bytes\":%u,"
           "\"idle_observed\":%u,\"closed\":%u,\"eof\":%u,\"sq_head\":%u,\"sq_tail\":%u,"
           "\"cq_head\":%u,\"cq_tail\":%u,\"dropped\":%u,\"overflow\":%u,\"head\":%u,\"reserved\":%u,"
           "\"last_res\":%d,\"last_prompt\":%u,\"last_token\":%u}\n",
           report->status,report->accepted,report->received,report->sent,report->bytes,
           report->idle_observed,report->closed,report->eof,report->sq_head,report->sq_tail,
           report->cq_head,report->cq_tail,report->dropped,report->overflow,report->head,report->reserved,
           report->last_res,report->last_prompt,report->last_token);
    close(net->ringfd);

    for(void *ptr:{(void*)sq,(void*)rings,(void*)buffer,(void*)report}) {
        check(cudaHostUnregister(ptr),"unregister");munmap(ptr,65536);
    }
    puts("CLEANUP ring_closed GPU_accepted_peer_closed buffers_unregistered");
    check(cudaStreamDestroy(net->stream),"network stream destroy");
    return 0;
}
