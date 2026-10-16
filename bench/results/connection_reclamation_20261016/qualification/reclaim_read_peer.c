#include <stdio.h>
#include <stdlib.h>
#include <arpa/inet.h>
#include <sys/mman.h>
#include <unistd.h>
#include <bpf/bpf.h>
#include "bpfusion_queue.h"
int main(int argc,char **argv) {
 if(argc!=3)return 2;
 struct in_addr ip;if(inet_pton(AF_INET,argv[1],&ip)!=1)return 2;
 unsigned bucket=bf_pending_bucket(ip.s_addr,htons(atoi(argv[2])));
 int fd=bpf_obj_get("/sys/fs/bpf/bpfusion_ctl");if(fd<0){perror("get");return 3;}
 struct bf_page *p=mmap(0,BF_PAGE_MMAP_BYTES,PROT_READ,MAP_SHARED,fd,0);
 if(p==MAP_FAILED){perror("mmap");return 4;}
 unsigned pending=__atomic_load_n(&p->llm_peer_pending[bucket],__ATOMIC_ACQUIRE);
 unsigned head=__atomic_load_n(&p->llm_head,__ATOMIC_ACQUIRE);
 printf("{\"bucket\":%u,\"pending\":%u,\"head\":%u,\"queued\":%u}\n",bucket,pending,head,__atomic_load_n(&p->llm_queued,__ATOMIC_ACQUIRE));
 munmap(p,BF_PAGE_MMAP_BYTES);close(fd);return 0;
}
