// SPDX-License-Identifier: GPL-2.0-only
// Experimental kernel TCP TX for the shared token ring. The executor must
// publish DONE after its last page access; TX alone never reclaims PENDING.
#include <linux/module.h>
#include <linux/kthread.h>
#include <linux/delay.h>
#include <linux/bpf.h>
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
static struct net *bf_net;
static struct task_struct *tx_task;
static struct bpf_map *page_map;
static struct bf_page *page;
static struct {
	struct sock *sk; /* lookup owns a reference, held until slot completion */
	u32 bytes;
	bool failed;
} tx[BF_LLM_SLOTS];
static unsigned long sent_bytes, completions, abandoned, retries;

static int reply_tcp(u32 idx, struct bf_llm_slot *s, u32 produced)
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
	vec.iov_base = (u8 *)s->tok_out + tx[idx].bytes;
	vec.iov_len = produced * sizeof(u32) - tx[idx].bytes;
	iov_iter_kvec(&msg.msg_iter, ITER_SOURCE, &vec, 1, vec.iov_len);
	/* No RCU read section across lock_sock/send. No sk_socket dereference:
	 * close can detach that object even while a sock reference is held. */
	lock_sock(sk);
	if (sock_flag(sk, SOCK_DEAD) || (sk->sk_shutdown & SEND_SHUTDOWN) ||
	    (sk->sk_state != TCP_ESTABLISHED && sk->sk_state != TCP_CLOSE_WAIT))
		ret = -ENOTCONN;
	else
		ret = tcp_sendmsg_locked(sk, &msg, vec.iov_len);
	release_sock(sk);
	return ret;
}

static void poll_slot(u32 idx)
{
	struct bf_llm_slot *s = &page->llm[idx];
	u32 state = smp_load_acquire(&s->state);
	u32 produced;
	int ret;

	if ((state != BF_PENDING && state != BF_DONE) || READ_ONCE(s->pad) != 1)
		return;
	produced = smp_load_acquire(&s->produced);
	if (produced > BF_LLM_MAX_TOK || READ_ONCE(s->n_gen) > BF_LLM_MAX_TOK)
		tx[idx].failed = true;
	if (!tx[idx].failed && produced * sizeof(u32) > tx[idx].bytes) {
		ret = reply_tcp(idx, s, produced);
		if (ret > 0) {
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
	    tx[idx].bytes == produced * sizeof(u32))) {
		if (tx[idx].sk)
			sock_put(tx[idx].sk);
		if (tx[idx].failed)
			abandoned++;
		else
			completions++;
		memset(&tx[idx], 0, sizeof(tx[idx]));
		smp_store_release(&s->state, BF_FREE);
	}
}

static int tx_thread(void *unused)
{
	while (!kthread_should_stop()) {
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
	tx_task = kthread_run(tx_thread, NULL, "bfusion_tx");
	if (IS_ERR(tx_task)) {
		err = PTR_ERR(tx_task);
		put_net(bf_net);
		goto out_map;
	}
	pr_info("bfusion_tx: map id=%u size=%u ring=%zu slot=%zu net=%u\n",
		page_map->id, page_map->value_size, offsetof(struct bf_page, llm),
		sizeof(struct bf_llm_slot), bf_net->ns.inum);
	return 0;
out_map:
	bpf_map_put(page_map);
	return err;
}

static void __exit bf_exit(void)
{
	kthread_stop(tx_task);
	for (u32 i = 0; i < BF_LLM_SLOTS; i++)
		if (tx[i].sk)
			sock_put(tx[i].sk);
	bpf_map_put(page_map);
	put_net(bf_net);
	pr_info("bfusion_tx: exit bytes=%lu completed=%lu abandoned=%lu retries=%lu\n",
		sent_bytes, completions, abandoned, retries);
}
module_init(bf_init);
module_exit(bf_exit);
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("BPFusion experimental asynchronous kernel TCP reply");
