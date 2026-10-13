// SPDX-License-Identifier: Apache-2.0
// GPU-owned asynchronous TCP control around the unchanged eBPF/model queue.
#ifndef BPFUSION_IO_URING_TCP_H
#define BPFUSION_IO_URING_TCP_H
#include <cuda_runtime.h>
#include <utility>
#include "bpfusion_queue.h"
#include <linux/io_uring.h>
#include <bpf/bpf.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/syscall.h>
#include <unistd.h>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <cerrno>
using UringIdentity=bf_uring_context;
struct IoRing {
    unsigned *head,*tail,*cqhead,*cqtail,*flags,*dropped,*overflow;
    io_uring_sqe *sqes;io_uring_cqe *cqes;unsigned mask,cqmask;
};
struct IoConn { int fd,next,reply,last;unsigned receiving,closing,dead,eof,generation; };
struct IoRequest {
    int conn,next;unsigned seq,ng,header,sent,busy,active,final,header_ready;
    unsigned long long tag,client_ns;unsigned sends,early,bytes;
};
struct IoRecord {unsigned seq,gen,sends,early,bytes,aborted;unsigned long long client_ns;};
struct IoStats {
    unsigned accepted,closed,received,sends,bytes,completed,aborted,max_connections,max_requests;
    unsigned pending,error,head,reserved,dropped,overflow,sqhead,sqtail,cqhead,cqtail;
    unsigned model_quiesced,trace_count,trace_overflow;IoRecord records[128];
};
__device__ unsigned io_load(const unsigned *p) {
    unsigned v;asm volatile("ld.acquire.sys.global.u32 %0,[%1];":"=r"(v):"l"(p):"memory");return v;
}
__device__ unsigned long long io_load64(const unsigned long long *p) {
    unsigned long long v;asm volatile("ld.acquire.sys.global.u64 %0,[%1];":"=l"(v):"l"(p):"memory");return v;
}
__device__ void io_store(unsigned *p,unsigned v) {
    asm volatile("st.release.sys.global.u32 [%0],%1;"::"l"(p),"r"(v):"memory");
}
__device__ bool io_submit(IoRing ring,io_uring_sqe entry,IoStats *stats) {
    unsigned tail=io_load(ring.tail);
    if(tail-io_load(ring.head)>ring.mask)return false;
    ring.sqes[tail&ring.mask]=entry;__threadfence_system();io_store(ring.tail,tail+1);stats->pending++;
    return true;
}
__device__ unsigned long long io_id(unsigned kind,unsigned value,unsigned generation=0) {
    return ((unsigned long long)kind<<56)|((unsigned long long)(generation&0xffffff)<<32)|value;
}
__device__ void io_retire(IoRequest *requests,IoConn *conns,unsigned i,IoStats *out,bool aborted) {
    auto &r=requests[i];
    if(r.conn>=0) {
        auto &c=conns[r.conn];c.reply=r.next;if(c.reply<0)c.last=-1;
    }
    unsigned index=out->trace_count++;
    if(index<128)out->records[index]={r.seq,r.ng,r.sends,r.early,r.bytes,(unsigned)aborted,r.client_ns};
    else out->trace_overflow++;
    out->completed++;if(aborted)out->aborted++;
    r.active=0;
}
__global__ void io_network(IoRing ring,bf_page *page,IoConn *conns,unsigned capacity,
                          unsigned char *buffer,unsigned long long host_buffer,IoStats *out,int listener) {
    if(threadIdx.x||blockIdx.x)return;
    constexpr unsigned stride=4160,txstride=512;
    for(unsigned i=0;i<capacity;++i)conns[i]={-1,i+1<capacity?(int)i+1:-1,-1,-1,0,0,0,0,0};
    int free=0,active=-1,accepting=-1;
    unsigned connections=0,seen=0,next_final=0;bool stopping=false,cancelled=false,cancel_done=false;
    IoRequest requests[BF_LLM_SLOTS]={};
    for(auto &r:requests){r.conn=-1;r.next=-1;}
    for(;;) {
        if(io_load64((unsigned long long*)&page->stop_ns))stopping=true;
        // Drain completions before publishing new work or reusing any buffer.
        unsigned ch=io_load(ring.cqhead);
        while(ch!=io_load(ring.cqtail)) {
            auto e=ring.cqes[ch&ring.cqmask];io_store(ring.cqhead,++ch);out->pending--;
            unsigned kind=e.user_data>>56,index=(unsigned)e.user_data;
            if((e.user_data>>48)==BF_IO_SEND_TAG || (e.user_data>>48)==BF_IO_ABORT_TAG)kind=7;
            if(kind==1) {
                accepting=-1;auto &c=conns[index];
                if(e.res>=0) {
                    c.fd=e.res;c.next=active;active=index;connections++;out->accepted++;
                    if(connections>out->max_connections)out->max_connections=connections;
                    if(stopping)c.dead=1;
                }else {c.next=free;free=index;if(e.res!=-ECANCELED)out->error=1;}
            }else if(kind==2) {
                auto &c=conns[index];c.receiving=0;
                if(e.res>0)out->received++;
                else if(e.res==0)c.eof=1;
                else c.dead=1;
            }else if(kind==3 || kind==7) {
                unsigned i=index%BF_LLM_SLOTS;auto &r=requests[i];
                if(!r.active || !r.busy || r.tag!=e.user_data){out->error=2;continue;}
                r.busy=0;
                if((e.user_data>>48)==BF_IO_ABORT_TAG) {
                    if(e.res!=0||r.seq!=next_final)out->error=3;else {io_retire(requests,conns,i,out,true);next_final++;}
                }else if(e.res>0) {
                    r.sent+=e.res;r.bytes+=e.res;out->bytes+=e.res;r.sends++;out->sends++;
                    if(!r.final)r.early++;
                    unsigned expected=(e.user_data>>32)&0xffff;
                    if(kind==7 && (unsigned)e.res==expected) {
                        if(r.seq!=next_final)out->error=3;
                        else {io_retire(requests,conns,i,out,false);next_final++;}
                    }
                }else {if(r.conn>=0)conns[r.conn].dead=1;}
            }else if(kind==4) {
                auto &c=conns[index];c.fd=-1;c.closing=0;out->closed++;
                // Removing from the active list occurs below after CQ drain.
            }else if(kind==5 || kind==6) {
                if(kind==5)cancel_done=true;
                // Cancellation completion; the target operation has its own CQE.
            }else out->error=4;
        }
        if(stopping&&!cancelled) {
            io_uring_sqe e{};e.opcode=IORING_OP_ASYNC_CANCEL;e.cancel_flags=IORING_ASYNC_CANCEL_ALL|IORING_ASYNC_CANCEL_ANY;
            e.user_data=io_id(5,0);
            if(io_submit(ring,e,out))cancelled=true;
        }
        if(stopping&&!cancel_done){__nanosleep(1000);continue;}
        // Claim eBPF slots in original admission order. Match by actual peer.
        while(seen!=io_load(&page->llm_head)) {
            unsigned i=seen%BF_LLM_SLOTS;auto &r=requests[i];auto *slot=&page->llm[i];
            unsigned state=io_load(&slot->state);
            if(r.active||(state!=BF_PENDING&&state!=BF_DONE))break;
            int peer=active;
            while(peer>=0) {
                auto *addr=(sockaddr_in*)(buffer+(unsigned)peer*stride+4096);
                if(slot->addr_be==addr->sin_addr.s_addr&&slot->port_be==addr->sin_port)break;
                peer=conns[peer].next;
            }
            if(peer<0&&!stopping)break;
            r={peer,-1,seen,io_load(&slot->n_gen),0,0,0,1,0,0,0,io_load64(&slot->client_ns),0,0,0};
            if(peer>=0) {
                auto &c=conns[peer];
                if(c.last>=0)requests[c.last].next=i;else c.reply=i;
                c.last=i;
            }
            seen++;
        }
        unsigned active_requests=0;
        for(unsigned i=0;i<BF_LLM_SLOTS;++i) {
            auto &r=requests[i];if(!r.active)continue;active_requests++;
            if(r.busy)continue;
            auto *slot=&page->llm[i];unsigned state=io_load(&slot->state);
            bool gone=r.conn<0||conns[r.conn].dead||stopping;
            if(gone) {
                if(r.seq!=next_final)continue;
                if(state!=BF_DONE) {
                    if(!stopping||!io_load(&out->model_quiesced))continue;
                    __threadfence_system();io_store(&slot->state,BF_DONE);
                }
                io_uring_sqe e{};e.opcode=IORING_OP_NOP;e.user_data=(BF_IO_ABORT_TAG<<48)|r.seq;
                if(io_submit(ring,e,out)){r.busy=1;r.tag=e.user_data;r.final=1;}
                continue;
            }
            auto &c=conns[r.conn];if(c.reply!=(int)i)continue;
            unsigned short flags=__ldcg(&slot->pad);
            if(flags&BF_LLM_VALIDATING)continue;
            bool bad=flags&BF_LLM_REJECTED;
            if(bad && (state!=BF_DONE || r.seq!=next_final))continue;
            if(bad && (flags&BF_LLM_TRANSPORT_MASK)==1){c.dead=1;continue;}
            auto *tx=buffer+capacity*stride+i*txstride;
            if(!r.header_ready) {
                r.header_ready=1;
                if((flags&BF_LLM_TRANSPORT_MASK)==2) {
                    const char ok[]="HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: ";
                    const char error[]="HTTP/1.1 400 Bad Request\r\nContent-Type: application/octet-stream\r\nContent-Length: ";
                    const char *prefix=bad?error:ok;
                    for(unsigned j=0;prefix[j];++j)tx[r.header++]=prefix[j];
                    unsigned value=bad?0:r.ng*4,n=0;char digits[4];
                    do{digits[n++]=value%10+'0';value/=10;}while(value);
                    while(n)tx[r.header++]=digits[--n];
                    const char end[]="\r\n\r\n";for(unsigned j=0;j<4;++j)tx[r.header++]=end[j];
                }
            }
            unsigned produced=bad?0:io_load(&slot->produced);
            // Publish final responses in admission order: physical-slot order
            // can expose a later completion while the wrap target is reserved.
            if((state!=BF_DONE || r.seq!=next_final)&&produced==r.ng&&produced)produced--;
            bool final=state==BF_DONE&&r.seq==next_final&&(bad||produced==r.ng);
            if(!produced&&!bad)continue;
            unsigned total=r.header+produced*4;if(total<=r.sent)continue;
            for(unsigned j=0;j<produced;++j) {
                unsigned token=io_load(&slot->tok_out[j]);
                for(unsigned byte=0;byte<4;++byte)tx[r.header+j*4+byte]=(token>>(byte*8))&255;
            }
            io_uring_sqe e{};e.opcode=IORING_OP_SEND;e.fd=c.fd;e.addr=host_buffer+capacity*stride+i*txstride+r.sent;
            e.len=total-r.sent;e.msg_flags=MSG_NOSIGNAL;
            e.user_data=final?((BF_IO_SEND_TAG<<48)|((unsigned long long)e.len<<32)|r.seq):io_id(3,r.seq);
            if(io_submit(ring,e,out)){r.busy=1;r.tag=e.user_data;r.final=final;}
        }
        if(active_requests>out->max_requests)out->max_requests=active_requests;
        // Rearm receive and close only after replies and receive references end.
        int *link=&active;
        while(*link>=0) {
            unsigned i=*link;auto &c=conns[i];
            if(c.fd<0&&!c.closing) {
                *link=c.next;c.next=free;free=i;connections--;continue;
            }
            if(stopping)c.dead=1;
            if(c.dead&&c.receiving&&!c.closing) {
                io_uring_sqe e{};e.opcode=IORING_OP_ASYNC_CANCEL;e.addr=io_id(2,i,c.generation);e.user_data=io_id(6,i,c.generation);
                if(io_submit(ring,e,out))c.closing=2; // wait for receive CQE
            }
            if((c.dead||c.eof)&&!c.receiving&&c.reply<0&&seen==io_load(&page->llm_head)&&c.closing!=1) {
                io_uring_sqe e{};e.opcode=IORING_OP_CLOSE;e.fd=c.fd;e.user_data=io_id(4,i,c.generation);
                if(io_submit(ring,e,out))c.closing=1;
            }else if(!c.dead&&!c.eof&&!c.receiving&&!stopping) {
                io_uring_sqe e{};e.opcode=IORING_OP_RECV;e.fd=c.fd;e.addr=host_buffer+i*stride;e.len=4096;e.user_data=io_id(2,i,c.generation);
                if(io_submit(ring,e,out))c.receiving=1;
            }
            link=&c.next;
        }
        if(!stopping&&accepting<0&&free>=0) {
            unsigned i=free;auto &c=conns[i];int next=c.next;
            auto *len=(socklen_t*)(buffer+i*stride+4112);*len=sizeof(sockaddr_in);
            io_uring_sqe e{};e.opcode=IORING_OP_ACCEPT;e.fd=listener;e.addr=host_buffer+i*stride+4096;
            e.off=host_buffer+i*stride+4112;e.user_data=io_id(1,i,c.generation+1);
            if(io_submit(ring,e,out)){free=next;accepting=i;c={-1,-1,-1,-1,0,0,0,0,c.generation+1};}
        }
        if(stopping&&cancelled&&!out->pending&&active<0&&!active_requests)break;
        __nanosleep(1000);
    }
    out->head=io_load(&page->llm_head);out->reserved=io_load(&page->llm_reserved);
    out->sqhead=io_load(ring.head);out->sqtail=io_load(ring.tail);
    out->cqhead=io_load(ring.cqhead);out->cqtail=io_load(ring.cqtail);
    out->dropped=io_load(ring.dropped);out->overflow=io_load(ring.overflow);
    __threadfence_system();
}
static void io_check(cudaError_t status,const char *what) {
    if(status){fprintf(stderr,"%s: %s\n",what,cudaGetErrorString(status));exit(10);}
}
static size_t io_align(size_t bytes){return (bytes+4095)&~(size_t)4095;}
static void *io_memory(size_t bytes) {
    void *p=mmap(nullptr,bytes,PROT_READ|PROT_WRITE,MAP_PRIVATE|MAP_ANONYMOUS,-1,0);
    if(p==MAP_FAILED){perror("io mmap");exit(11);}
    memset(p,0,bytes);io_check(cudaHostRegister(p,bytes,cudaHostRegisterMapped),"io register");return p;
}
static void *io_device(void *p) {
    void *d;io_check(cudaHostGetDevicePointer(&d,p,0),"io device pointer");return d;
}
struct UringNetwork {
    void *sq,*rings,*buffer;IoStats *report;IoConn *conns;int ringfd;
    size_t sq_bytes,ring_bytes,buffer_bytes;cudaStream_t stream;
};
static int uring_start(bf_page *page,bf_page *device,int listener,UringNetwork *net) {
    int streams=bpf_obj_get("/sys/fs/bpf/bpfusion_streams");
    bpf_map_info info{};unsigned size=sizeof(info);
    if(streams<0||bpf_obj_get_info_by_fd(streams,&info,&size)){perror("io stream map");return 1;}
    close(streams);unsigned capacity=info.max_entries,entries=1;
    while(entries<capacity+BF_LLM_SLOTS+2)entries*=2;
    net->sq_bytes=io_align(entries*sizeof(io_uring_sqe));
    net->ring_bytes=io_align(4096+entries*2*sizeof(io_uring_cqe));
    net->buffer_bytes=io_align((size_t)capacity*4160+BF_LLM_SLOTS*512);
    net->sq=io_memory(net->sq_bytes);net->rings=io_memory(net->ring_bytes);net->buffer=io_memory(net->buffer_bytes);
    net->report=(IoStats*)io_memory(65536);
    io_check(cudaMalloc(&net->conns,capacity*sizeof(IoConn)),"io connections");
    auto *dsq=(char*)io_device(net->sq),*dring=(char*)io_device(net->rings);
    auto *dbuffer=(unsigned char*)io_device(net->buffer);auto *dreport=(IoStats*)io_device(net->report);
    int identity=bpf_obj_get("/sys/fs/bpf/bpfusion_uring_owner");unsigned key=0;
    struct stat namespace_info{};
    if(stat("/proc/self/ns/pid",&namespace_info)){perror("io PID namespace");return 2;}
    UringIdentity owner{(unsigned)getpid(),0,0,(unsigned long long)namespace_info.st_dev,(unsigned long long)namespace_info.st_ino};
    if(identity<0||bpf_map_update_elem(identity,&key,&owner,BPF_ANY)){perror("io identity");return 2;}
    io_uring_params p{};p.flags=IORING_SETUP_SQPOLL|IORING_SETUP_NO_MMAP|IORING_SETUP_NO_SQARRAY;
    p.sq_off.user_addr=(uint64_t)net->sq;p.cq_off.user_addr=(uint64_t)net->rings;
    net->ringfd=syscall(__NR_io_uring_setup,entries,&p);
    if(net->ringfd<0){perror("io setup");return 3;}
    if(p.cq_off.cqes+p.cq_entries*sizeof(io_uring_cqe)>net->ring_bytes)return 4;
    if(bpf_map_lookup_elem(identity,&key,&owner)){perror("io bind lookup");return 5;}
    if(!owner.ring){fprintf(stderr,"io PID namespace binding returned no ring\n");return 5;}
    close(identity);
    IoRing ring{};
    ring.head=(unsigned*)(dring+p.sq_off.head);ring.tail=(unsigned*)(dring+p.sq_off.tail);
    ring.cqhead=(unsigned*)(dring+p.cq_off.head);ring.cqtail=(unsigned*)(dring+p.cq_off.tail);
    ring.flags=(unsigned*)(dring+p.sq_off.flags);ring.dropped=(unsigned*)(dring+p.sq_off.dropped);
    ring.overflow=(unsigned*)(dring+p.cq_off.overflow);ring.sqes=(io_uring_sqe*)dsq;ring.cqes=(io_uring_cqe*)(dring+p.cq_off.cqes);
    ring.mask=*(unsigned*)((char*)net->rings+p.sq_off.ring_mask);
    ring.cqmask=*(unsigned*)((char*)net->rings+p.cq_off.ring_mask);
    // A bootstrap NOP starts an observed active SQPOLL epoch.
    auto *sqe=(io_uring_sqe*)net->sq;sqe[0].opcode=IORING_OP_NOP;sqe[0].user_data=0xb007;
    __atomic_store_n((unsigned*)((char*)net->rings+p.sq_off.tail),1,__ATOMIC_RELEASE);
    if(syscall(__NR_io_uring_enter,net->ringfd,0,0,IORING_ENTER_SQ_WAKEUP,nullptr,0)<0)return 6;
    while(!__atomic_load_n((unsigned*)((char*)net->rings+p.cq_off.tail),__ATOMIC_ACQUIRE))usleep(1000);
    auto *cqe=(io_uring_cqe*)((char*)net->rings+p.cq_off.cqes);
    if(cqe[0].user_data!=0xb007||cqe[0].res)return 7;
    __atomic_store_n((unsigned*)((char*)net->rings+p.cq_off.head),1,__ATOMIC_RELEASE);
    io_check(cudaStreamCreateWithFlags(&net->stream,cudaStreamNonBlocking),"io stream");
    io_network<<<1,1,0,net->stream>>>(ring,device,net->conns,capacity,dbuffer,(uint64_t)net->buffer,dreport,listener);
    io_check(cudaGetLastError(),"io launch");
    printf("NET_READY pid=%d port=%u ring_bound=1 capacity=%u sq=%u cq=%u\n",getpid(),BF_LLM_TCP_PORT,capacity,p.sq_entries,p.cq_entries);fflush(stdout);
    return 0;
}
static void uring_quiesce(UringNetwork *net) {
    __atomic_store_n(&net->report->model_quiesced,1,__ATOMIC_RELEASE);
    syscall(__NR_io_uring_enter,net->ringfd,0,0,IORING_ENTER_SQ_WAKEUP,nullptr,0);
}
static int uring_finish(UringNetwork *net) {
    io_check(cudaStreamSynchronize(net->stream),"io finish");
    auto &r=*net->report;
    printf("RESULT {\"accepted\":%u,\"closed\":%u,\"received\":%u,\"sends\":%u,\"bytes\":%u,"
           "\"completed\":%u,\"aborted\":%u,\"max_connections\":%u,\"max_requests\":%u,\"pending\":%u,"
           "\"error\":%u,\"head\":%u,\"reserved\":%u,\"dropped\":%u,\"overflow\":%u,"
           "\"sqhead\":%u,\"sqtail\":%u,\"cqhead\":%u,\"cqtail\":%u,\"trace_count\":%u,\"trace_overflow\":%u}\n",
           r.accepted,r.closed,r.received,r.sends,r.bytes,r.completed,r.aborted,r.max_connections,r.max_requests,
           r.pending,r.error,r.head,r.reserved,r.dropped,r.overflow,r.sqhead,r.sqtail,r.cqhead,r.cqtail,r.trace_count,r.trace_overflow);
    for(unsigned i=0;i<r.trace_count&&i<128;++i) {
        auto &v=r.records[i];
        printf("REPLY {\"seq\":%u,\"gen\":%u,\"sends\":%u,\"early\":%u,\"bytes\":%u,\"aborted\":%u,\"client_ns\":%llu}\n",
               v.seq,v.gen,v.sends,v.early,v.bytes,v.aborted,v.client_ns);
    }
    unsigned error=r.error;
    close(net->ringfd);io_check(cudaFree(net->conns),"io connections free");
    for(auto pair:{std::pair<void*,size_t>{net->sq,net->sq_bytes},{net->rings,net->ring_bytes},{net->buffer,net->buffer_bytes},{net->report,65536}}) {
        io_check(cudaHostUnregister(pair.first),"io unregister");munmap(pair.first,pair.second);
    }
    io_check(cudaStreamDestroy(net->stream),"io stream destroy");
    puts("CLEANUP ring_connections_buffers_released");fflush(stdout);
    return error?1:0;
}

#endif
