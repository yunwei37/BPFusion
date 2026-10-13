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

struct Report {
    unsigned stage, status, submitted, completed, bytes, flags_before, flags_after;
    unsigned sq_head, sq_tail, cq_head, cq_tail, dropped, overflow;
    int last_res;
    unsigned long long last_id;
};
struct Ring {
    unsigned *sh,*st,*flags,*ch,*ct,*dropped,*overflow;
    io_uring_sqe *sqes;
    io_uring_cqe *cqes;
    unsigned smask,cmask;
};
__device__ unsigned acquire(unsigned *p) {
    unsigned v; asm volatile("ld.acquire.sys.global.u32 %0, [%1];":"=r"(v):"l"(p):"memory"); return v;
}
__device__ void release(unsigned *p,unsigned v) {
    asm volatile("st.release.sys.global.u32 [%0], %1;"::"l"(p),"r"(v):"memory");
}
__device__ unsigned long long timer() {
    unsigned long long v; asm volatile("mov.u64 %0, %%globaltimer;":"=l"(v)); return v;
}
__global__ void warm() {}
__global__ void send_frames(Ring r,unsigned char *payload,unsigned long long host_payload,int fd,
                            Report *out,bool idle) {
    if(threadIdx.x||blockIdx.x) return;
    if(idle) {
        auto until=timer()+2000000000ULL;
        while(timer()<until) __nanosleep(100000);
    }
    out->flags_before=acquire(r.flags);
    for(unsigned frame=0;frame<32;++frame) {
        for(unsigned i=0;i<128;++i) payload[i]=(frame*17+i)%251;
        unsigned offset=0;
        while(offset<128) {
            unsigned tail=acquire(r.st),head=acquire(r.sh);
            if(tail-head>r.smask) {out->status=2;goto done;}
            io_uring_sqe entry{};
            entry.opcode=IORING_OP_SEND; entry.fd=fd;
            entry.addr=host_payload+offset; entry.len=128-offset;
            entry.msg_flags=MSG_NOSIGNAL;
            entry.user_data=(unsigned long long)frame*128+offset+1;
            r.sqes[tail&r.smask]=entry;
            __threadfence_system();
            release(r.st,tail+1);
            ++out->submitted;
            release(&out->stage,1);
            unsigned cqhead=acquire(r.ch);
            auto limit=timer()+2000000000ULL;
            while(acquire(r.ct)==cqhead) {
                if(timer()>limit) {out->status=1;goto done;}
                __nanosleep(1000);
            }
            auto cqe=r.cqes[cqhead&r.cmask];
            out->last_res=cqe.res;out->last_id=cqe.user_data;
            release(r.ch,cqhead+1);
            ++out->completed;
            if(cqe.user_data!=entry.user_data || cqe.res<=0 || (unsigned)cqe.res>128-offset) {
                out->status=3;goto done;
            }
            offset+=cqe.res;out->bytes+=cqe.res;
        }
    }
done:
    out->flags_after=acquire(r.flags);
    out->sq_head=acquire(r.sh);out->sq_tail=acquire(r.st);
    out->cq_head=acquire(r.ch);out->cq_tail=acquire(r.ct);
    out->dropped=acquire(r.dropped);out->overflow=acquire(r.overflow);
    __threadfence_system();release(&out->stage,2);
}
static void check(cudaError_t e,const char *what) {
    if(e!=cudaSuccess) {fprintf(stderr,"%s: %s\n",what,cudaGetErrorString(e));exit(10);}
}
static void *memory() {
    void *p=mmap(nullptr,65536,PROT_READ|PROT_WRITE,MAP_PRIVATE|MAP_ANONYMOUS,-1,0);
    if(p==MAP_FAILED) {perror("mmap");exit(11);}
    memset(p,0,65536);check(cudaHostRegister(p,65536,cudaHostRegisterMapped),"cudaHostRegister");
    return p;
}
static void *device(void *p) {
    void *d;check(cudaHostGetDevicePointer(&d,p,0),"cudaHostGetDevicePointer");return d;
}
int main(int argc,char **argv) {
    if(argc!=2) return 12;
    bool idle=strcmp(argv[1],"hot")!=0, wake=strcmp(argv[1],"idle-wake")==0;
    setbuf(stdout,nullptr);
    int listener=socket(AF_INET,SOCK_STREAM,0);
    sockaddr_in a{};a.sin_family=AF_INET;a.sin_addr.s_addr=htonl(INADDR_LOOPBACK);
    if(listener<0||bind(listener,(sockaddr*)&a,sizeof(a))||listen(listener,1)) {perror("listener");return 13;}
    socklen_t alen=sizeof(a);getsockname(listener,(sockaddr*)&a,&alen);
    printf("PORT %u\n",ntohs(a.sin_port));
    int peer=accept(listener,nullptr,nullptr);close(listener);
    if(peer<0) {perror("accept");return 14;}
    check(cudaSetDeviceFlags(cudaDeviceMapHost),"cudaSetDeviceFlags");
    warm<<<1,1>>>();check(cudaDeviceSynchronize(),"warm");
    char *sq=(char*)memory(), *rings=(char*)memory(), *payload=(char*)memory();
    auto *report=(Report*)memory();
    auto *dsq=(char*)device(sq), *dring=(char*)device(rings);
    auto *dpayload=(unsigned char*)device(payload);auto *dreport=(Report*)device(report);
    io_uring_params p{};
    p.flags=IORING_SETUP_SQPOLL|IORING_SETUP_NO_MMAP|IORING_SETUP_NO_SQARRAY;
    p.sq_off.user_addr=(uint64_t)sq;p.cq_off.user_addr=(uint64_t)rings;
    int ringfd=syscall(__NR_io_uring_setup,8,&p);
    if(ringfd<0) {perror("io_uring_setup");return 15;}
    if(p.cq_off.cqes+p.cq_entries*sizeof(io_uring_cqe)>65536 ||
       p.sq_entries*sizeof(io_uring_sqe)>65536) return 16;
    Ring r{};
    r.sh=(unsigned*)(dring+p.sq_off.head);r.st=(unsigned*)(dring+p.sq_off.tail);
    r.flags=(unsigned*)(dring+p.sq_off.flags);
    r.ch=(unsigned*)(dring+p.cq_off.head);r.ct=(unsigned*)(dring+p.cq_off.tail);
    r.dropped=(unsigned*)(dring+p.sq_off.dropped);r.overflow=(unsigned*)(dring+p.cq_off.overflow);
    r.sqes=(io_uring_sqe*)dsq;r.cqes=(io_uring_cqe*)(dring+p.cq_off.cqes);
    r.smask=*(unsigned*)(rings+p.sq_off.ring_mask);r.cmask=*(unsigned*)(rings+p.cq_off.ring_mask);
    printf("READY mode=%s setup_flags=%u features=%u sq=%u cq=%u idle_arg=%u host_device_alias=%d\n",
           argv[1],p.flags,p.features,p.sq_entries,p.cq_entries,p.sq_thread_idle,
           sq==dsq&&rings==dring&&payload==(char*)dpayload);
    send_frames<<<1,1>>>(r,dpayload,(uint64_t)payload,peer,dreport,idle);
    check(cudaGetLastError(),"launch");
    int wake_count=0,wake_result=0,wake_errno=0;
    if(wake) {
        while(__atomic_load_n(&report->stage,__ATOMIC_ACQUIRE)==0) usleep(1000);
        wake_result=syscall(__NR_io_uring_enter,ringfd,0,0,IORING_ENTER_SQ_WAKEUP,nullptr,0);
        wake_errno=errno;++wake_count;
    }
    check(cudaDeviceSynchronize(),"send_frames");
    printf("RESULT {\"status\":%u,\"submitted\":%u,\"completed\":%u,\"bytes\":%u,"
           "\"flags_before\":%u,\"flags_after\":%u,\"sq_head\":%u,\"sq_tail\":%u,"
           "\"cq_head\":%u,\"cq_tail\":%u,\"dropped\":%u,\"overflow\":%u,"
           "\"last_res\":%d,\"last_id\":%llu,\"cpu_wakes\":%d,\"wake_result\":%d,\"wake_errno\":%d}\n",
           report->status,report->submitted,report->completed,report->bytes,
           report->flags_before,report->flags_after,report->sq_head,report->sq_tail,
           report->cq_head,report->cq_tail,report->dropped,report->overflow,
           report->last_res,report->last_id,wake_count,wake_result,wake_errno);
    close(ringfd);shutdown(peer,SHUT_WR);close(peer);
    for(void *ptr:{(void*)sq,(void*)rings,(void*)payload,(void*)report}) {
        check(cudaHostUnregister(ptr),"cudaHostUnregister");munmap(ptr,65536);
    }
    printf("CLEANUP ring_and_socket_closed buffers_unregistered_and_unmapped\n");
    return report==nullptr;
}
