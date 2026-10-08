/* SPDX-License-Identifier: Apache-2.0
 * BPFusion: load and attach the ingress classifier, report its counters.
 *
 *   bpfusion_load attach [ifname]   create clsact, load, attach tc ingress
 *   bpfusion_load detach [ifname]   remove the filter and the clsact qdisc
 *   bpfusion_load stats             print BPF counters and page header
 *
 * The tc ingress hook is used because a `BPF_PROG_TYPE_SOCKET_FILTER` socket
 * filter exposes only helpers, not `skb->remote_ip4`/`remote_port`, on this
 * kernel; tc/clsact is the real ingress hook and is where a NIC's XDP-redirect
 * path would land anyway.
 */
#define _GNU_SOURCE
#include <errno.h>
#include <net/if.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/mman.h>

#include <bpf/bpf.h>
#include <bpf/libbpf.h>

#include "bpfusion_queue.h"

static const char *stats_name[] = {"seen pkts", "ip+udp/ip+tcp pkts",
				   "magic pkts", "drops", "published",
				   "drop: ctl busy", "drop: done busy",
				   "llm magic", "llm busy",
				   "tcp dest", "tcp magic"};

int main(int argc, char **argv)
{
	const char *cmd = argc > 1 ? argv[1] : "attach";
	const char *ifname = argc > 2 ? argv[2] : "lo";
	struct bpf_object *bo;
	struct bpf_program *prog;
	int err, ctl_fd, stats_fd;
	struct bf_page *page;
	struct bpf_tc_hook hook;
	struct bpf_tc_opts opts;
	uint64_t v;
	int i;

	if (!strcmp(cmd, "attach")) {
		/* Drop stale pins from a previous run: a fresh object otherwise
		 * cannot take the same pin path, and the daemon would map the
		 * *old* page while the new program writes to the new one. */
		unlink("/sys/fs/bpf/bpfusion_ctl");
		unlink("/sys/fs/bpf/bpfusion_stats");
		unlink("/sys/fs/bpf/bpfusion_db");
	}

	if (!strcmp(cmd, "stats")) {
		/* Read the *pinned* maps: the running program writes to those,
		 * not to a freshly loaded copy. */
		ctl_fd = bpf_obj_get("/sys/fs/bpf/bpfusion_ctl");
		stats_fd = bpf_obj_get("/sys/fs/bpf/bpfusion_stats");
		if (ctl_fd < 0 || stats_fd < 0) {
			fprintf(stderr, "no pinned maps: %s\n", strerror(errno));
			return 1;
		}
		page = (struct bf_page *)mmap(NULL, BF_PAGE_MMAP_BYTES,
					      PROT_READ | PROT_WRITE,
					      MAP_SHARED, ctl_fd, 0);
		if (page == MAP_FAILED) {
			perror("mmap ctl");
			return 1;
		}
		for (i = 0; i < 11; i++) {
			__u32 k = (__u32)i;

			if (bpf_map_lookup_elem(stats_fd, &k, &v) == 0)
				printf("%-14s %llu\n", stats_name[i],
				       (unsigned long long)v);
		}
		printf("head=%u done_seq=%u published=%u acked=%u drops=%u "
		       "ready=%u\n",
		       page->head, page->done_seq, page->published, page->acked,
		       page->drops, page->ready);
		for (i = 0; i < 4 && i < BF_SLOTS; i++)
			printf("slot[%d]: state=%u id=%u client_ns=%llu x[0]=%f "
			       "| done state=%u id=%u y[0]=%f\n",
			       i, page->slots[i].state, page->slots[i].id,
			       (unsigned long long)page->slots[i].client_ns,
			       page->slots[i].x[0], page->done[i].state,
			       page->done[i].id, page->done[i].y[0]);
		return 0;
	}

	bo = bpf_object__open_file("build/fusion.bpf.o", NULL);
	if (!bo) {
		perror("open bpf object");
		return 1;
	}
	{
		struct bpf_map *m;

		m = bpf_object__find_map_by_name(bo, "ctl");
		bpf_map__set_pin_path(m, "/sys/fs/bpf/bpfusion_ctl");
		m = bpf_object__find_map_by_name(bo, "stats");
		bpf_map__set_pin_path(m, "/sys/fs/bpf/bpfusion_stats");
		m = bpf_object__find_map_by_name(bo, "doorbell");
		bpf_map__set_pin_path(m, "/sys/fs/bpf/bpfusion_db");
	}
	if ((err = bpf_object__load(bo))) {
		fprintf(stderr, "load: %s\n", strerror(-err));
		return 1;
	}
	ctl_fd = bpf_map__fd(bpf_object__find_map_by_name(bo, "ctl"));
	stats_fd = bpf_map__fd(bpf_object__find_map_by_name(bo, "stats"));
	page = (struct bf_page *)mmap(NULL, BF_PAGE_MMAP_BYTES, PROT_READ | PROT_WRITE,
				      MAP_SHARED, ctl_fd, 0);
	if (page == MAP_FAILED) {
		perror("mmap ctl");
		return 1;
	}

	memset(&hook, 0, sizeof(hook));
	hook.sz = sizeof(hook);
	hook.ifindex = if_nametoindex(ifname);
	hook.attach_point = BPF_TC_INGRESS;
	if (hook.ifindex == 0) {
		fprintf(stderr, "no such interface: %s\n", ifname);
		return 1;
	}

	if (!strcmp(cmd, "detach")) {
		memset(&opts, 0, sizeof(opts));
		opts.sz = sizeof(opts);
		bpf_tc_detach(&hook, &opts);
		bpf_tc_hook_destroy(&hook);
		printf("detached from %s\n", ifname);
		return 0;
	}

	/* clsact survives process exits, and every attach adds another
	 * filter, so old ones keep running (and keep bumping the counters)
	 * after new ones are added. Start from a clean hook. */
	bpf_tc_hook_destroy(&hook);
	if (bpf_tc_hook_create(&hook) && errno != EEXIST) {
		fprintf(stderr, "hook create: %s\n", strerror(errno));
		return 1;
	}
	prog = bpf_object__find_program_by_name(bo, "ingress");
	memset(&opts, 0, sizeof(opts));
	opts.sz = sizeof(opts);
	opts.prog_fd = bpf_program__fd(prog);
	if ((err = bpf_tc_attach(&hook, &opts))) {
		fprintf(stderr, "tc attach: %s\n", strerror(-err));
		return 1;
	}
	printf("attached to %s (prog_id %u), ctl map=%d page=%p\n", ifname,
	       opts.prog_id, ctl_fd, (void *)page);
	return 0;
}
