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
#include <bpf/bpf_endian.h>
#include "bpfusion_queue.h"


#ifndef TC_ACT_OK
#define TC_ACT_OK 0
#endif
#define ETH_P_IP 0x0800
#define IPPROTO_UDP 17

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
	__uint(max_entries, 8);
	__type(key, __u32);
	__type(value, __u64);
} stats SEC(".maps");

static __always_inline void bump(__u32 key)
{
	__u64 *v = bpf_map_lookup_elem(&stats, &key);

	if (v)
		__sync_fetch_and_add(v, 1);
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
	if (ip.protocol != IPPROTO_UDP)
		return TC_ACT_OK;
	l4 = 14 + (__u32)(ip.ihl * 4);
	if (bpf_skb_load_bytes(skb, l4, &udp, sizeof(udp)) != 0)
		return TC_ACT_OK;
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

char _license[] SEC("license") = "GPL";
