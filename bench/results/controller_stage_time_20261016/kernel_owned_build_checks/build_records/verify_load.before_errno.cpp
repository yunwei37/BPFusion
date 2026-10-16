// SPDX-License-Identifier: Apache-2.0
// Real verifier-only diagnostic; never attaches a BPF link or submits I/O.
// This is not an application/oracle/performance test.
#include "kernel_tcp.h"
int main(int argc,char **argv){
    if(argc!=3){fprintf(stderr,"usage: verify_load object actual_capacity\n");return 2;}
    unsigned capacity=strtoul(argv[2],nullptr,10),entries=1;
    if(!capacity)return 2;
    while(entries<capacity+BF_LLM_SLOTS+2)entries*=2;
    UringNetwork net{};
    net.sq_bytes=io_align((size_t)entries*sizeof(io_uring_sqe));
    net.ring_bytes=io_align(4096+(size_t)2*entries*sizeof(io_uring_cqe));
    auto &layout=net.layout;layout.capacity=capacity;layout.entries=entries;
    layout.ring_bytes=net.ring_bytes;layout.listener=-1; // no TCP listener
    size_t cursor=(sizeof(bf_ktcp_shared)+63)&~size_t(63);
    layout.conns=cursor;cursor+=(size_t)capacity*sizeof(bf_ktcp_conn);
    cursor=(cursor+63)&~size_t(63);
    layout.buffers=cursor;cursor+=(size_t)capacity*BF_KTCP_RX_STRIDE;
    layout.tx=cursor;cursor+=(size_t)BF_LLM_SLOTS*BF_KTCP_TX_STRIDE;
    layout.tick=cursor;cursor+=sizeof(__kernel_timespec);
    net.mem_bytes=io_align(cursor);if(net.mem_bytes>UINT32_MAX)return 2;
    layout.mem_bytes=net.mem_bytes;
    net.sq=kernel_memory(net.sq_bytes);net.rings=kernel_memory(net.ring_bytes);
    net.memory=kernel_memory(net.mem_bytes);
    if(!net.sq||!net.rings||!net.memory)return 3;
    layout.user_base=(uint64_t)net.memory;
    io_uring_params parameters{};
    parameters.flags=IORING_SETUP_NO_MMAP|IORING_SETUP_NO_SQARRAY|
                     IORING_SETUP_SINGLE_ISSUER|IORING_SETUP_DEFER_TASKRUN;
    parameters.sq_off.user_addr=(uint64_t)net.sq;
    parameters.cq_off.user_addr=(uint64_t)net.rings;
    net.ringfd=syscall(__NR_io_uring_setup,entries,&parameters);
    if(net.ringfd<0){perror("verifier diagnostic ring");return 3;}
    layout.sh=parameters.sq_off.head;layout.st=parameters.sq_off.tail;
    layout.ch=parameters.cq_off.head;layout.ct=parameters.cq_off.tail;
    layout.cqes=parameters.cq_off.cqes;layout.dropped=parameters.sq_off.dropped;
    layout.overflow=parameters.cq_off.overflow;
    io_uring_region_desc region{};
    region.user_addr=layout.user_base;region.size=net.mem_bytes;
    region.flags=IORING_MEM_REGION_TYPE_USER;
    io_uring_mem_region_reg registration{};registration.region_uptr=(uint64_t)&region;
    int reg=syscall(__NR_io_uring_register,net.ringfd,IORING_REGISTER_MEM_REGION,
                    &registration,1);
    bpf_object *object=nullptr;int result=0;
    if(reg<0){perror("verifier diagnostic memory region");result=3;}
    else{
        object=bpf_object__open_file(argv[1],nullptr);
        if(!object||libbpf_get_error(object)){object=nullptr;result=4;}
        else{
            auto *pending=bpf_object__find_map_by_name(object,"pending");
            if(!pending||bpf_map__set_max_entries(pending,capacity)||
               kernel_configure(object,layout))result=5;
            else{
                result=bpf_object__load(object);
                printf("{\"event\":\"verifier_only\",\"capacity\":%u,"
                       "\"entries\":%u,\"registered_bytes\":%zu,"
                       "\"load_return\":%d,\"errno\":%d,\"attached\":false,"
                       "\"network_listener\":false,\"io_submitted\":false}\n",
                       capacity,entries,net.mem_bytes,result,errno);
            }
        }
    }
    bpf_object__close(object);close(net.ringfd);
    munmap(net.sq,net.sq_bytes);munmap(net.rings,net.ring_bytes);
    munmap(net.memory,net.mem_bytes);
    printf("verifier-only object/ring/memory closed; no BPF link created\n");
    return result?1:0;
}
