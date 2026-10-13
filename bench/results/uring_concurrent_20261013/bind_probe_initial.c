#include <bpf/bpf.h>
#include <linux/io_uring.h>
#include <sys/syscall.h>
#include <unistd.h>
#include <stdio.h>
struct owner {unsigned pid,pad;unsigned long long ring;};
int main(){unsigned k=0;struct owner o={getpid(),0,0};int f=bpf_obj_get("/sys/fs/bpf/bpfusion_uring_owner");bpf_map_update_elem(f,&k,&o,BPF_ANY);struct io_uring_params p={};int ring=syscall(__NR_io_uring_setup,8,&p);bpf_map_lookup_elem(f,&k,&o);printf("pid=%u ringfd=%d bound=%d\n",o.pid,ring,o.ring!=0);close(ring);close(f);return 0;}
