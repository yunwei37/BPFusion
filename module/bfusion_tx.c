// SPDX-License-Identifier: GPL-2.0-only
// Experimental kernel TCP TX for the shared token ring. The executor must
// publish DONE after its last page access; TX alone never reclaims PENDING.
#include <linux/module.h>
#include <linux/kthread.h>
#include <linux/delay.h>
#include <linux/bpf.h>
#include <linux/file.h>
#include <linux/net.h>
#include <net/inet_sock.h>
#include <linux/nsproxy.h>
#include <linux/uio.h>
#include <net/inet_hashtables.h>
#include <net/net_namespace.h>
#include <net/sock.h>
#include <net/tcp.h>
#include "../bpf/include/bpfusion_queue.h"
MODULE_IMPORT_NS("BPF_INTERNAL");

static int map_fd = -1;
module_param(map_fd, int, 0400);
MODULE_PARM_DESC(map_fd, "BPF map FD in the loading process (use bpfusion_load tx-load)");
static u32 reply_addr = 0x0100007fu;
module_param(reply_addr, uint, 0444);
MODULE_PARM_DESC(reply_addr, "local server IPv4 address, network order");
static int listen_fd = -1;
module_param(listen_fd, int, 0400);
MODULE_PARM_DESC(listen_fd, "optional bootstrap listener FD for kernel accept/drain");
static struct socket *listener;
struct peer { struct list_head node; struct socket *socket; };
static LIST_HEAD(peers);
static unsigned long accepted, closed;
static struct net *bf_net;
static struct task_struct *tx_task;
static struct bpf_map *page_map;
static struct bf_page *page;
static struct {
	struct sock *sk; /* lookup owns a reference, held until slot completion */
	u32 bytes;
	bool failed;
	u16 header_length, header_sent;
	char header[128];
} tx[BF_LLM_SLOTS];
static unsigned long sent_bytes, completions, abandoned, retries;

static int reply_tcp(u32 idx, struct bf_llm_slot *s, void *data, u32 bytes,
                     struct sock **locked)
{
	struct sock *sk = tx[idx].sk;
	struct msghdr msg = { .msg_flags = MSG_DONTWAIT | MSG_NOSIGNAL };
	struct kvec vec;
	int ret;

	if (!sk) {
		rcu_read_lock();
		sk = __inet_lookup_established(bf_net, (__be32)s->addr_be,
			(__be16)s->port_be, (__be32)reply_addr, BF_LLM_TCP_PORT, 0, 0);
		rcu_read_unlock();
		if (!sk)
			return -ENOENT;
		if (!sk_fullsock(sk)) {
			sock_gen_put(sk);
			return -ENOTCONN;
		}
		tx[idx].sk = sk;
	}
	vec.iov_base = data;
	vec.iov_len = bytes;
	iov_iter_kvec(&msg.msg_iter, ITER_SOURCE, &vec, 1, vec.iov_len);
	/* No RCU read section across lock_sock/send. No sk_socket dereference:
	 * close can detach that object even while a sock reference is held. */
	lock_sock(sk);
	*locked = sk;
	if (sock_flag(sk, SOCK_DEAD) || (sk->sk_shutdown & SEND_SHUTDOWN) ||
	    (sk->sk_state != TCP_ESTABLISHED && sk->sk_state != TCP_CLOSE_WAIT))
		ret = -ENOTCONN;
	else
		ret = tcp_sendmsg_locked(sk, &msg, vec.iov_len);
	/* Caller recycles a completed slot before releasing incoming backlog. */
	return ret;
}

/* Stream responses must retain request order on a persistent connection,
 * including ring wrap and a partially sent preceding response. */
static bool earlier_peer(u32 idx, struct bf_llm_slot *s)
{
    for (u32 i = 0; i < BF_LLM_SLOTS; i++) {
        struct bf_llm_slot *other = &page->llm[i];
        u32 state;

        if (i == idx)
            continue;
        state = smp_load_acquire(&other->state);
        if ((state == BF_PENDING || state == BF_DONE) &&
            other->addr_be == s->addr_be && other->port_be == s->port_be &&
            other->ingress_ns < s->ingress_ns)
            return true;
    }
    return false;
}

/* Binary replies have no status header. Reject by ending the owned peer,
 * so the client observes EOF and the rest of the GPU queue remains live. */
static void reject_binary(struct bf_llm_slot *s)
{
    struct peer *peer;

    list_for_each_entry(peer, &peers, node) {
        struct inet_sock *inet = inet_sk(peer->socket->sk);
        if ((__force u32)inet->inet_daddr == s->addr_be &&
            (__force u16)inet->inet_dport == s->port_be) {
            kernel_sock_shutdown(peer->socket, SHUT_RDWR);
            return;
        }
    }
}

static void poll_slot(u32 idx)
{
	struct bf_llm_slot *s = &page->llm[idx];
	struct sock *locked = NULL, *put = NULL;
	u32 state = smp_load_acquire(&s->state);
	u32 produced;
	u16 flags = READ_ONCE(s->pad), transport = flags & BF_LLM_TRANSPORT_MASK;
	bool header, rejected = flags & BF_LLM_REJECTED;
	int ret;

	if ((state != BF_PENDING && state != BF_DONE) ||
	    (transport != 1 && transport != 2))
		return;
	/* A bodyless rejection header also completes a response. */
	if ((flags & BF_LLM_VALIDATING) || (rejected && state != BF_DONE))
		return;
	if (earlier_peer(idx, s))
		return;
	produced = smp_load_acquire(&s->produced);
	/* Keep the last token until GPU release. Receiving a whole response must
	 * not permit a new request while this slot is still executor-owned. */
	if (state != BF_DONE && produced && produced == READ_ONCE(s->n_gen))
		produced--;
	if (produced > BF_LLM_MAX_TOK || (!rejected && READ_ONCE(s->n_gen) > BF_LLM_MAX_TOK))
		tx[idx].failed = true;
	if (rejected && transport == 1 && !tx[idx].failed) {
		reject_binary(s);
		tx[idx].failed = true;
	}
	if (transport == 2 && !tx[idx].header_length)
		tx[idx].header_length = scnprintf(tx[idx].header, sizeof(tx[idx].header),
			"HTTP/1.1 %s\r\nContent-Type: application/octet-stream\r\nContent-Length: %u\r\n\r\n",
			rejected ? "400 Bad Request" : "200 OK",
			rejected ? 0 : s->n_gen * (u32)sizeof(u32));
	header = tx[idx].header_sent < tx[idx].header_length;
	if (!tx[idx].failed && (header || produced * sizeof(u32) > tx[idx].bytes)) {
		if (header)
			ret = reply_tcp(idx, s, tx[idx].header + tx[idx].header_sent,
				tx[idx].header_length - tx[idx].header_sent, &locked);
		else
			ret = reply_tcp(idx, s, (u8 *)s->tok_out + tx[idx].bytes,
				produced * sizeof(u32) - tx[idx].bytes, &locked);
		if (ret > 0) {
			if (header)
				tx[idx].header_sent += ret;
			else
				tx[idx].bytes += ret; /* exact byte offset, including partial u32 */
			sent_bytes += ret;
		} else {
			retries++;
			if (ret == -EPIPE || ret == -ECONNRESET || ret == -ENOTCONN ||
			    (ret == -ENOENT && state == BF_DONE))
				tx[idx].failed = true;
		}
	}
	/* A disconnected peer cannot release memory still owned by an executor.
	 * DONE is its release; produced == n_gen is not a release. */
	if (state == BF_DONE && (tx[idx].failed ||
	    (tx[idx].header_sent == tx[idx].header_length &&
	    tx[idx].bytes == produced * sizeof(u32)))) {
		put = tx[idx].sk;
		if (tx[idx].failed)
			abandoned++;
		else
			completions++;
		memset(&tx[idx], 0, sizeof(tx[idx]));
		smp_store_release(&s->state, BF_FREE);
	}
	/* release_sock can run the next request's parser from TCP backlog. All
	 * old slot/TX accesses must finish first; keep the sock reference until
	 * after unlocking, even when completion cleared tx[idx].sk. */
	if (locked)
		release_sock(locked);
	if (put)
		sock_put(put);
}

/* The bootstrap process owns the listener file; sockfd_lookup pins it.
 * Accepted sockets and receive-buffer draining are entirely kernel-owned. */
static bool peer_pending(struct sock *sk)
{
	struct inet_sock *inet = inet_sk(sk);

	for (u32 i = 0; i < BF_LLM_SLOTS; i++) {
		struct bf_llm_slot *s = &page->llm[i];
		u32 state = smp_load_acquire(&s->state);

		if (state != BF_FREE && ((s->pad & BF_LLM_TRANSPORT_MASK) == 1 ||
                                  (s->pad & BF_LLM_TRANSPORT_MASK) == 2) &&
		    s->addr_be == (__force u32)inet->inet_daddr &&
		    s->port_be == (__force u16)inet->inet_dport)
			return true;
	}
	return false;
}

static void accept_and_drain(void)
{
	struct socket *socket;
	struct peer *peer, *next;

	if (!listener)
		return;
	while (kernel_accept(listener, &socket, O_NONBLOCK) == 0) {
		peer = kmalloc(sizeof(*peer), GFP_KERNEL);
		if (!peer) {
			sock_release(socket);
			continue;
		}
		peer->socket = socket;
		list_add_tail(&peer->node, &peers);
		accepted++;
	}
	list_for_each_entry_safe(peer, next, &peers, node) {
		char discard[256];
		struct kvec vec = { .iov_base = discard, .iov_len = sizeof(discard) };
		int ret;

		do {
			struct msghdr msg = {};

			ret = kernel_recvmsg(peer->socket, &msg, &vec, 1,
					     sizeof(discard), MSG_DONTWAIT);
		} while (ret > 0);
		if ((ret == 0 && !peer_pending(peer->socket->sk)) ||
		    (ret < 0 && ret != -EAGAIN && ret != -EWOULDBLOCK)) {
			list_del(&peer->node);
			sock_release(peer->socket);
			kfree(peer);
			closed++;
		}
	}
}

static int tx_thread(void *unused)
{
	while (!kthread_should_stop()) {
		accept_and_drain();
		for (u32 i = 0; i < BF_LLM_SLOTS; i++)
			poll_slot(i);
		usleep_range(60, 120);
	}
	return 0;
}

static int __init bf_init(void)
{
	struct bpf_array *array;
	int err;

	/* bpf_map_get validates the actual BPF FD and acquires a map reference.
	 * A bpffs filp_open FD is a seq_file, not a BPF map FD. */
	page_map = bpf_map_get(map_fd);
	if (IS_ERR(page_map))
		return PTR_ERR(page_map);
	if (page_map->map_type != BPF_MAP_TYPE_ARRAY ||
	    !(page_map->map_flags & BPF_F_MMAPABLE) ||
	    page_map->max_entries != 1 || page_map->value_size != sizeof(*page)) {
		err = -EINVAL;
		goto out_map;
	}
	array = container_of(page_map, struct bpf_array, map);
	page = (struct bf_page *)array->value;
	bf_net = get_net(current->nsproxy->net_ns);
	if (listen_fd >= 0) {
		listener = sockfd_lookup(listen_fd, &err);
		if (!listener)
			goto out_net;
		if (listener->type != SOCK_STREAM || listener->sk->sk_protocol != IPPROTO_TCP ||
		    listener->sk->sk_state != TCP_LISTEN ||
		    inet_sk(listener->sk)->inet_num != BF_LLM_TCP_PORT ||
		    !net_eq(sock_net(listener->sk), bf_net)) {
			err = -EINVAL;
			goto out_listener;
		}
	}
	tx_task = kthread_run(tx_thread, NULL, "bfusion_tx");
	if (IS_ERR(tx_task)) {
		err = PTR_ERR(tx_task);
		goto out_listener;
	}
	pr_info("bfusion_tx: map id=%u size=%u ring=%zu slot=%zu net=%u\n",
		page_map->id, page_map->value_size, offsetof(struct bf_page, llm),
		sizeof(struct bf_llm_slot), bf_net->ns.inum);
	return 0;
out_listener:
	if (listener)
		sockfd_put(listener);
out_net:
	put_net(bf_net);
out_map:
	bpf_map_put(page_map);
	return err;
}

static void __exit bf_exit(void)
{
	struct peer *peer, *next;

	kthread_stop(tx_task);
	list_for_each_entry_safe(peer, next, &peers, node) {
		list_del(&peer->node);
		sock_release(peer->socket);
		kfree(peer);
	}
	if (listener)
		sockfd_put(listener);
	for (u32 i = 0; i < BF_LLM_SLOTS; i++)
		if (tx[i].sk)
			sock_put(tx[i].sk);
	bpf_map_put(page_map);
	put_net(bf_net);
	pr_info("bfusion_tx: exit bytes=%lu completed=%lu abandoned=%lu retries=%lu accepted=%lu closed=%lu\n",
		sent_bytes, completions, abandoned, retries, accepted, closed);
}
module_init(bf_init);
module_exit(bf_exit);
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("BPFusion experimental asynchronous kernel TCP reply");
