// SPDX-License-Identifier: Apache-2.0
// BPFusion: kernel-side ingress.
//
// A tc/clsact ingress program on the loopback device (the real ingress hook,
// same place a NIC's XDP-redirect path would land). For every well-formed
// request datagram it
//   1. copies the client's 64-byte float vector into the next control-page
//      slot, together with the client's clock, the parse time
//      (`bpf_ktime_get_ns()`) and the peer address parsed from the headers,
//   2. publishes the slot (payload, then state = PENDING, then head++),
//   3. pushes one byte into a ring buffer so a sleeping executor is woken
//      without polling.
//
// A slot is taken only if it is FREE *and* its completion has been consumed by
// the responder, which is what lets the GPU publish results into the same page
// without the producer clobbering them. Otherwise the datagram counts as a
// drop: there is no back-pressure channel from the GPU to a packet hook.
//
// The program returns TC_ACT_OK, so the datagram still reaches the UDP socket;
// the daemon drains it only to keep the receive queue from overflowing, and
// uses it as the ordinary fallback path for non-magic datagrams.
#include "vmlinux.h"
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_core_read.h>
#include <bpf/bpf_endian.h>
#include "bpfusion_queue.h"


#ifndef TC_ACT_OK
#define TC_ACT_OK 0
#endif
#define ETH_P_IP 0x0800
#define IPPROTO_UDP 17
#define IPPROTO_TCP 6

struct {
	__uint(type, BPF_MAP_TYPE_ARRAY);
	__uint(max_entries, 1);
	__uint(map_flags, BPF_F_MMAPABLE);
	__type(key, __u32);
	__type(value, struct bf_page);
} ctl SEC(".maps");

/* Doorbell: the record's presence is the wakeup, contents are unused. */
struct {
	__uint(type, BPF_MAP_TYPE_RINGBUF);
	__uint(max_entries, 1 << 12);
} doorbell SEC(".maps");

/* Diagnostics, read by the daemon at exit. */
struct {
	__uint(type, BPF_MAP_TYPE_ARRAY);
	__uint(max_entries, 16);
	__type(key, __u32);
	__type(value, __u64);
} stats SEC(".maps");

static __always_inline void bump(__u32 key)
{
	__u64 *v = bpf_map_lookup_elem(&stats, &key);

	if (v)
		__sync_fetch_and_add(v, 1);
}

/* LLM request: header magic + n_prompt + n_gen + client_ns, then n_prompt
 * little-endian token ids. Written into the LLM ring; the executor generates. */
union bf_llm_hdr {
	struct {
		__u32 magic;
		__u32 n_prompt;
		__u32 n_gen;
		__u32 pad;
		__u64 client_ns;
	};
	__u64 v;
};

/* Fill the next LLM slot from a request whose payload starts at `payload`.
 * `flags` = 0 for a UDP datagram (reply goes to addr_be/port_be), 1 for a TCP
 * segment (reply goes to the accepted socket that addr_be/port_be identify). */
static __always_inline int llm_fill(struct __sk_buff *skb, __u32 payload,
				     __u32 addr_be, __u16 port_be, __u16 flags)
{
	struct bf_page *p;
	struct bf_llm_slot *s;
	union bf_llm_hdr h;
	__u32 idx, zero = 0, i;

	if (bpf_skb_load_bytes(skb, payload, &h, sizeof(h)) != 0)
		return TC_ACT_OK;
	if (h.magic != BF_LLM_MAGIC)
		return TC_ACT_OK;
	if (h.n_prompt == 0 || h.n_prompt > BF_LLM_MAX_TOK)
		return TC_ACT_OK;
	if (h.n_gen == 0 || h.n_gen > BF_LLM_MAX_TOK)
		return TC_ACT_OK;
	bump(7); /* llm magic */

	p = bpf_map_lookup_elem(&ctl, &zero);
	if (!p)
		return TC_ACT_OK;
	idx = p->llm_head % BF_LLM_SLOTS;
	s = &p->llm[idx];
	if (s->state != BF_FREE) {
		p->drops++;
		bump(8); /* llm busy */
		return TC_ACT_OK;
	}
	payload += sizeof(h);
#pragma unroll
	for (i = 0; i < BF_LLM_MAX_TOK; i++) {
		if (i < h.n_prompt &&
		    bpf_skb_load_bytes(skb, payload + i * 4,
				       &s->tok_in[i], 4) != 0)
			return TC_ACT_OK;
	}
	s->n_prompt = h.n_prompt;
	s->n_gen = h.n_gen;
	s->produced = 0;
	s->pad = flags;
	s->addr_be = addr_be;
	s->port_be = port_be;
	s->client_ns = h.client_ns;
	s->ingress_ns = bpf_ktime_get_ns();
	p->llm[idx].state = BF_PENDING;
	__sync_fetch_and_add(&p->llm_head, 1);
	return TC_ACT_OK;
}

static __always_inline int llm_ingress(struct __sk_buff *skb, __u32 l4,
				       struct udphdr *udp, struct iphdr *ip)
{
	return llm_fill(skb, l4 + sizeof(*udp), ip->saddr, udp->source, 0);
}

static __always_inline int llm_ingress_tcp(struct __sk_buff *skb, __u32 payload,
					   struct tcphdr *tcp, struct iphdr *ip)
{
	return llm_fill(skb, payload, ip->saddr, tcp->source, 1);
}

SEC("classifier")
int ingress(struct __sk_buff *skb)
{
	struct bf_page *p;
	struct bf_req_hdr h;
	struct iphdr ip;
	struct udphdr udp;
	__u32 head, idx, zero = 0, l4;
	struct bf_ctl_slot *s;
	void *d;

	bump(0); /* seen */
	if (skb->protocol != bpf_htons(ETH_P_IP))
		return TC_ACT_OK;
	/* Loopback uses the usual 14-byte Ethernet header on this kernel; a
	 * raw-IP path (no L2) is handled by the fallback below. */
	if (bpf_skb_load_bytes(skb, 12, &udp, 2) == 0 &&
	    *(__be16 *)&udp != bpf_htons(ETH_P_IP))
		return TC_ACT_OK;
	if (bpf_skb_load_bytes(skb, 14, &ip, sizeof(ip)) != 0)
		return TC_ACT_OK;
	if (ip.protocol != IPPROTO_UDP) {
		struct tcphdr tcp;
		__u32 thl;

		if (ip.protocol != IPPROTO_TCP)
			return TC_ACT_OK;
		bump(1);
		l4 = 14 + (__u32)(ip.ihl * 4);
		if (bpf_skb_load_bytes(skb, l4, &tcp, sizeof(tcp)) != 0)
			return TC_ACT_OK;
		/* Only the first payload segment matters: the client sends the
		 * whole LLM request in one write. */
		if (tcp.dest != bpf_htons(BF_LLM_TCP_PORT))
			return TC_ACT_OK;
		bump(9); /* tcp dest match */
		thl = (__u32)(tcp.doff * 4);
		if (bpf_skb_load_bytes(skb, l4 + thl, &h,
				       sizeof(h.magic)) != 0)
			return TC_ACT_OK;
		if (h.magic != BF_LLM_MAGIC)
			return TC_ACT_OK;
		bump(10); /* tcp magic */
		return llm_ingress_tcp(skb, l4 + thl, &tcp, &ip);
	}
	l4 = 14 + (__u32)(ip.ihl * 4);
	if (bpf_skb_load_bytes(skb, l4, &udp, sizeof(udp)) != 0)
		return TC_ACT_OK;
	if (udp.dest == bpf_htons(BF_LLM_PORT))
		return llm_ingress(skb, l4, &udp, &ip);
	if (udp.dest != bpf_htons(BF_PORT))
		return TC_ACT_OK;
	bump(1); /* ip+udp */

	if (bpf_skb_load_bytes(skb, l4 + sizeof(udp), &h, sizeof(h)) != 0)
		return TC_ACT_OK;
	if (h.magic != BF_MAGIC)
		return TC_ACT_OK;
	bump(2); /* magic */

	p = bpf_map_lookup_elem(&ctl, &zero);
	if (!p)
		return TC_ACT_OK;

	head = p->head;
	idx = head % BF_SLOTS;
	s = &p->slots[idx];
	if (s->state != BF_FREE || p->done[idx].state != BF_FREE) {
		p->drops++;
		bump(3);
		bump(s->state != BF_FREE ? 5 : 6); /* 5: ctl busy, 6: done busy */
		goto out;
	}
	/* bf_req_hdr: magic(4) pad(4) client_ns(8), then x[] at offset 16. */
	if (bpf_skb_load_bytes(skb, l4 + sizeof(udp) + 16, s->x,
			       sizeof(s->x)) != 0)
		goto out;
	s->id = head;
	s->client_ns = h.client_ns;
	s->ingress_ns = bpf_ktime_get_ns();
	p->peers[idx].addr_be = ip.saddr;
	p->peers[idx].port_be = udp.source;
	s->state = BF_PENDING;
	__sync_fetch_and_add(&p->head, 1);
	bump(4); /* published */
out:
	d = bpf_ringbuf_reserve(&doorbell, 1, 0);
	if (d)
		bpf_ringbuf_submit(d, 0);
	return TC_ACT_OK;
}


/* TCP sequencing/reassembly precedes this stream parser. */
struct bf_flow { __u32 local, remote, local_port, remote_port; };
struct {
    __uint(type, BPF_MAP_TYPE_SOCKHASH);
    __uint(max_entries, BF_SLOTS);
    __type(key, struct bf_flow);
    __type(value, __u32);
} streams SEC(".maps");

SEC("sockops")
int stream_sockops(struct bpf_sock_ops *ctx)
{
    if (ctx->op == BPF_SOCK_OPS_PASSIVE_ESTABLISHED_CB &&
        ctx->family == 2 && ctx->local_port == BF_LLM_TCP_PORT) {
        struct bf_flow key = { ctx->local_ip4, ctx->remote_ip4,
                              ctx->local_port, ctx->remote_port };
        if (bpf_sock_hash_update(ctx, &streams, &key, BPF_NOEXIST)) bump(13);
        else bump(12);
    }
    return 0;
}

extern void *bpf_cast_to_kern_ctx(void *ctx) __ksym;

/* strparser can clone one skb for several messages. load_bytes offsets are
 * skb-relative; the message does not necessarily start at its data[0]. */
static __always_inline __u32 stream_offset(struct __sk_buff *ctx)
{
    struct sk_buff *skb=bpf_cast_to_kern_ctx(ctx);
    struct sk_skb_cb *cb=(void *)skb->cb;
    return BPF_CORE_READ(cb,strp.strp.offset);
}

/* Minimal Content-Length POST transport for the existing binary token API.
 * bpf_loop follows available stream bytes; no separate header-size tuning. */
struct http_scan {
    __u32 rolling, line_pos, end, length, value;
    int match, reading, digits, have_length, error;
};
__noinline int http_step(struct http_scan *s, __u8 c)
{
    if (!s) return 1;
    const char name[]="content-length";
    __u8 lower=c>='A' && c<='Z' ? c+32 : c;
    if (c=='\n') {
        if (s->reading) {
            if (!s->digits || s->have_length) { s->error=1; return 1; }
            s->length=s->value; s->have_length=1;
        }
        s->line_pos=0; s->match=0; s->reading=0; s->digits=0; s->value=0;
    } else {
        if (s->line_pos<14) {
            if (s->match>=0 && lower==name[s->line_pos]) s->match++;
            else s->match=-1;
        } else if (s->line_pos==14 && c==':' && s->match==14) {
            s->reading=1;
        } else if (s->reading) {
            if (c>='0' && c<='9') {
                if (s->value>sizeof(union bf_llm_hdr)+BF_LLM_MAX_TOK*4) { s->error=1; return 1; }
                s->value=s->value*10+c-'0'; s->digits=1;
            } else if (c!=' ' && c!='\t' && c!='\r') { s->error=1; return 1; }
        }
        if (s->line_pos<15) s->line_pos++; /* only header-name positions matter */
    }
    s->rolling=(s->rolling<<8)|c;
    if (s->rolling==0x0d0a0d0a) { return 1; }
    return 0;
}
struct http_scan_ctx {
    struct __sk_buff *skb;
    __u32 base;
    struct http_scan state;
};
static long http_byte(__u32 off, void *opaque)
{
    struct http_scan_ctx *s=opaque;
    __u8 c;
    if (bpf_skb_load_bytes(s->skb,s->base+off,&c,1)) return 1;
    int done=http_step(&s->state,c);
    if (done && !s->state.error) s->state.end=off+1;
    /* Global-function verification does not propagate return bounds. */
    asm volatile("%0 &= 1" : "+r"(done));
    return done;
}
static __always_inline int frame_info(struct __sk_buff *skb, __u32 *body, __u16 *http)
{
    __u32 magic, offset=stream_offset(skb);
    union bf_llm_hdr h;
    *body=0; *http=0;
    if (offset>skb->len) return -1;
    __u32 available=skb->len-offset;
    if (available<4 || bpf_skb_load_bytes(skb,offset,&magic,4)) return 0;
    if (magic==0x54534f50) { /* POST */
        struct http_scan_ctx ctx={.skb=skb,.base=offset};
        struct http_scan *scan=&ctx.state;
        if (bpf_loop(available,http_byte,&ctx,0)<0 || scan->error) return -1;
        if (!scan->end) return 0;
        if (!scan->have_length || scan->length<sizeof(h) ||
            scan->length>sizeof(h)+BF_LLM_MAX_TOK*4) return -1;
        *body=scan->end; *http=1;
        return scan->end+scan->length;
    }
    if (available<sizeof(h) || bpf_skb_load_bytes(skb,offset,&h,sizeof(h))) return 0;
    if (h.magic!=BF_LLM_MAGIC || !h.n_prompt || h.n_prompt>BF_LLM_MAX_TOK ||
        !h.n_gen || h.n_gen>BF_LLM_MAX_TOK) return -1;
    return sizeof(h)+h.n_prompt*4;
}
SEC("sk_skb/stream_parser")
int stream_parse(struct __sk_buff *skb)
{
    __u32 body; __u16 http;
    int length;
    bump(14);
    length=frame_info(skb,&body,&http);
    if (length<0) bump(15);
    return length;
}

SEC("sk_skb/stream_verdict")
int stream_publish(struct __sk_buff *skb)
{
    union bf_llm_hdr h;
    __u32 tokens[BF_LLM_MAX_TOK] = {};
    __u32 zero=0, head, idx, body;
    __u16 http;
    __u32 offset=stream_offset(skb);
    int length=frame_info(skb,&body,&http);
    struct bf_page *p;
    struct bf_llm_slot *slot;
    if (length<=0 || offset>skb->len || length>skb->len-offset || bpf_skb_load_bytes(skb,offset+body,&h,sizeof(h)) ||
        h.magic!=BF_LLM_MAGIC || length!=body+sizeof(h)+h.n_prompt*4 ||
        !h.n_prompt || h.n_prompt > BF_LLM_MAX_TOK ||
        !h.n_gen || h.n_gen > BF_LLM_MAX_TOK) return SK_DROP;
#pragma unroll
    for (__u32 i=0;i<BF_LLM_MAX_TOK;i++)
        if (i<h.n_prompt && bpf_skb_load_bytes(skb,offset+body+sizeof(h)+i*4,&tokens[i],4)) return SK_DROP;
    p=bpf_map_lookup_elem(&ctl,&zero);
    if (!p) return SK_DROP;
    int reserved=0;
    for (__u32 attempt=0;attempt<BF_LLM_SLOTS;attempt++) {
        head=p->llm_head;
        idx=head%BF_LLM_SLOTS;
        slot=&p->llm[idx];
        if (__sync_val_compare_and_swap(&slot->state,BF_FREE,BF_WRITING)!=BF_FREE) break;
        if (__sync_val_compare_and_swap(&p->llm_head,head,head+1)==head) {
            reserved=1; break;
        }
        slot->state=BF_FREE;
    }
    if (!reserved) { bump(8); __sync_fetch_and_add(&p->drops,1); return SK_DROP; }
    for (__u32 i=0;i<BF_LLM_MAX_TOK;i++) slot->tok_in[i]=tokens[i];
    slot->n_prompt=h.n_prompt; slot->n_gen=h.n_gen; slot->produced=0; slot->pad=(http ? 2 : 1) | BF_LLM_VALIDATING;
    slot->addr_be=skb->remote_ip4; slot->port_be=(__u16)(skb->remote_port>>16);
    slot->client_ns=h.client_ns; slot->ingress_ns=bpf_ktime_get_ns(); slot->gpu_done_ns=0;
    slot->state=BF_PENDING;
    bump(11);
    return SK_PASS;
}

char _license[] SEC("license") = "GPL";
