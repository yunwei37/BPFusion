/* SPDX-License-Identifier: Apache-2.0
 * BPFusion: canonical layout of the kernel<->GPU control page.
 *
 * Included by the eBPF ingress program, the resident GPU executor and the
 * gateway. POD only. The page is a single `BPF_MAP_TYPE_ARRAY` entry with
 * `BPF_F_MMAPABLE`, so the very same bytes are written by the BPF program in
 * softirq context and read/written by both userspace processes over the same
 * mapping.
 *
 * Ownership (one writer per field, no locks):
 *   slots[i].state    producer: FREE -> PENDING. GPU: PENDING -> FREE once the
 *                     request is in registers.
 *   done[i].state     executor: FREE -> DONE after done[i] is complete.
 *                     gateway:  DONE -> FREE once the response is on the wire.
 *   head              producer: requests published so far.
 *   done_seq          executor: futex word, bumped after each batch.
 *   published         executor: completions made visible (== head consumed).
 *   acked             gateway: responses sent (== completions consumed).
 *   ready             executor: 1 once calibrated and looping.
 *   drops             producer: requests that found the slot still busy.
 *
 * A slot is recyclable only when both `slots[i].state` and `done[i].state` are
 * FREE, so a completion cannot be overwritten before the gateway has sent it.
 *
 * The payload is exactly what the client sent: a 64-byte float vector plus its
 * own monotonic timestamp, echoed back in the response, so the client measures
 * a round trip without trusting server clocks.
 */
#ifndef BPFUSION_QUEUE_H
#define BPFUSION_QUEUE_H

#ifndef __VMLINUX_H__
typedef unsigned int __u32;
typedef unsigned long long __u64;
typedef unsigned short __u16;
#endif

#define BF_PORT 39400

/* LLM request ring: a second, independent slot ring that carries token ids
 * instead of a float vector. The BPF producer fills `tok_in` from the packet;
 * the resident model executor generates into `tok_out`, bumping `produced`
 * after each token so a client can measure TTFT (first token) and TPOT
 * (inter-token) over the same kernel->page path. */
#define BF_LLM_PORT 39402
#define BF_LLM_TCP_PORT 39403 /* same LLM ring, over stream TCP */
#define BF_LLM_MAGIC 0x514c4d51u /* 'Q','M','L','Q' little-endian */
#define BF_LLM_SLOTS 8
#define BF_LLM_MAX_TOK 64
#define BF_LLM_TRANSPORT_MASK 3u
#define BF_LLM_VALIDATING 4u /* stream request awaits model-vocabulary check */
#define BF_LLM_REJECTED 8u /* executor rejected request before producing tokens */


#define BF_SLOTS 64
#define BF_MAX_BATCH 16
#define BF_VEC 16

struct bf_llm_slot {
	__u32 state;      /* producer FREE->PENDING; executor ->DONE; TX ->FREE */
	__u32 n_gen;      /* tokens requested */
	__u32 n_prompt;   /* prompt tokens written to tok_in */
	__u32 produced;   /* tokens written to tok_out so far (executor) */
	__u32 addr_be;    /* client peer, network order */
	__u16 port_be;
	__u16 pad;       /* transport 1=TCP, 2=HTTP; producer VALIDATING, GPU status */
	__u64 client_ns;
	__u64 ingress_ns;
	__u64 gpu_done_ns;
	__u32 tok_in[BF_LLM_MAX_TOK];
	__u32 tok_out[BF_LLM_MAX_TOK];
};

/* Wire layout of a request datagram. */
#define BF_MAGIC 0x46504251u /* 'Q','B','P','F' little-endian */
struct bf_req_hdr {
	__u32 magic;
	__u32 pad;
	__u64 client_ns;
	float x[BF_VEC];
};

/* Wire layout of a response datagram. */
struct bf_resp_hdr {
	__u32 magic;
	__u32 id;
	__u32 pad;
	__u32 pad2;
	__u64 client_ns;  /* echoed from the request */
	__u64 ingress_ns; /* kernel parse time, CLOCK_MONOTONIC */
	__u64 gpu_start_ns;
	__u64 gpu_done_ns;
	float y[BF_VEC];
};

enum bf_state {
	BF_FREE = 0,
	BF_PENDING = 1,
	BF_DONE = 2,
	BF_WRITING = 3, /* producer reservation, before publishing PENDING */
};

struct bf_ctl_slot {
	__u32 state;
	__u32 id;
	__u64 client_ns;
	__u64 ingress_ns; /* bpf_ktime_get_ns() / CLOCK_MONOTONIC */
	float x[BF_VEC];
};

struct bf_done_slot {
	__u32 id;
	__u32 state;
	__u64 client_ns; /* copied from the request: the responder echoes it */
	__u64 ingress_ns;
	__u64 gpu_start_ns; /* %globaltimer */
	__u64 gpu_done_ns;  /* %globaltimer */
	float y[BF_VEC];
};

/* Where to send the answer, recorded by the producer for each slot. */
struct bf_peer {
	__u32 addr_be; /* IPv4, network order */
	__u16 port_be;
	__u16 pad2;
};
struct bf_page {
	__u32 head;
	__u32 done_seq;
	__u32 published;
	__u32 acked;
	__u32 drops;
	__u32 ready;
	__u32 n_slots;
	__u32 served;      /* completions published to done[] (GPU-owned) */
	__u32 pad0;
	__u64 stop_ns;     /* host CLOCK_MONOTONIC deadline for the resident
			    * kernel; 0 means "not set". */

	struct bf_ctl_slot slots[BF_SLOTS];
	struct bf_peer peers[BF_SLOTS];
	struct bf_done_slot done[BF_SLOTS];

	/* LLM request ring (see bf_llm_slot above). Kept at the tail so the
	 * MLP offsets are unchanged. */
	__u32 llm_head;
	__u32 llm_pad;
	struct bf_llm_slot llm[BF_LLM_SLOTS];
};

#define BF_PAGE_BYTES ((int)sizeof(struct bf_page))

/* A BPF_F_MMAPABLE array map exposes its value at offset 0 and the region is
 * the value size rounded up to a page multiple. Mapping only BF_PAGE_BYTES
 * (or a fixed two pages) is wrong: the page is 12832 bytes, so a short
 * mapping turns the tail of `done[]` into out-of-bounds writes. */
#define BF_PAGE_MMAP_BYTES \
	((long)((((long)BF_PAGE_BYTES + 4095L) / 4096L) * 4096L))

#endif /* BPFUSION_QUEUE_H */
