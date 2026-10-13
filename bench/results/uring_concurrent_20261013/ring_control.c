#include <bpf/bpf.h>
#include <linux/io_uring.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/syscall.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include "bpfusion_queue.h"
struct owner {unsigned pid,pad;unsigned long long ring,nsdev,nsino;};
struct ring {int fd;struct io_uring_params p;char *mem;struct io_uring_sqe *sq;};
static struct ring create(void){
    struct ring r={};r.mem=mmap(0,65536,PROT_READ|PROT_WRITE,MAP_PRIVATE|MAP_ANONYMOUS,-1,0);
    r.sq=mmap(0,65536,PROT_READ|PROT_WRITE,MAP_PRIVATE|MAP_ANONYMOUS,-1,0);
    r.p.flags=IORING_SETUP_NO_MMAP|IORING_SETUP_NO_SQARRAY;
    r.p.sq_off.user_addr=(unsigned long long)r.sq;r.p.cq_off.user_addr=(unsigned long long)r.mem;
    r.fd=syscall(__NR_io_uring_setup,8,&r.p);return r;
}
static int abort_slot(struct ring *r){
    memset(&r->sq[0],0,sizeof(r->sq[0]));r->sq[0].opcode=IORING_OP_NOP;r->sq[0].user_data=0xbff1ULL<<48;
    __atomic_store_n((unsigned*)(r->mem+r->p.sq_off.tail),1,__ATOMIC_RELEASE);
    int result=syscall(__NR_io_uring_enter,r->fd,1,1,IORING_ENTER_GETEVENTS,0,0);
    struct io_uring_cqe *cqe=(void*)(r->mem+r->p.cq_off.cqes);
    return result>=0&&cqe[0].user_data==(0xbff1ULL<<48)&&cqe[0].res==0;
}
int main(){
    unsigned key=0;struct stat ns;stat("/proc/self/ns/pid",&ns);
    struct owner o={getpid(),0,0,ns.st_dev,ns.st_ino};
    int fd=bpf_obj_get("/sys/fs/bpf/bpfusion_uring_owner");
    if(fd<0||bpf_map_update_elem(fd,&key,&o,BPF_ANY))return 1;
    struct ring owned=create();if(owned.fd<0)return 2;
    bpf_map_lookup_elem(fd,&key,&o);if(!o.ring)return 3;
    int ctl=bpf_obj_get("/sys/fs/bpf/bpfusion_ctl");
    struct bf_page *page=mmap(0,BF_PAGE_MMAP_BYTES,PROT_READ|PROT_WRITE,MAP_SHARED,ctl,0);
    page->llm_head=1;page->llm_reserved=1;page->llm[0].state=BF_DONE;
    struct ring foreign=create();if(foreign.fd<0)return 4;
    int f=abort_slot(&foreign),untouched=page->llm[0].state==BF_DONE&&page->llm_reserved==1;
    int a=abort_slot(&owned),reclaimed=page->llm[0].state==BF_FREE&&page->llm_reserved==0;
    printf("RESULT namespace_bound=1 foreign_completed=%d foreign_did_not_recycle=%d owned_completed=%d owned_recycled=%d\n",f,untouched,a,reclaimed);
    close(owned.fd);close(foreign.fd);close(fd);close(ctl);
    munmap(owned.mem,65536);munmap(owned.sq,65536);munmap(foreign.mem,65536);munmap(foreign.sq,65536);munmap(page,BF_PAGE_MMAP_BYTES);
    return !(f&&untouched&&a&&reclaimed);
}
