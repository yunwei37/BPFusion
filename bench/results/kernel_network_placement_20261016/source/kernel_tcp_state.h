/* SPDX-License-Identifier: Apache-2.0
 * Private kernel-owned transport candidate; not runtime qualified or selected.
 * Existing model-page ABI is unchanged; these are CPU-only registered bytes.
 */
#ifndef BF_KERNEL_TCP_STATE_H
#define BF_KERNEL_TCP_STATE_H
#include "bpfusion_queue.h"
#define BF_KTCP_RX_STRIDE 4160u
#define BF_KTCP_TX_STRIDE 512u
struct bf_ktcp_layout {
    __u64 user_base;
    __u32 capacity, entries, ring_bytes, mem_bytes;
    __u32 conns, buffers, tx, tick;
    __u32 sh, st, ch, ct, cqes, dropped, overflow;
    int listener;
};
struct bf_ktcp_conn {
    int fd, next, reply, last;
    __u32 receiving, closing, eof, dead, generation;
};
struct bf_ktcp_request {
    int conn, next;
    __u32 seq, ng, sent, header, header_ready, active, busy, final;
    __u64 tag, client_ns;
    __u32 sends, early, bytes;
};
struct bf_ktcp_record {
    __u32 seq, gen, sends, early, bytes, aborted;
    __u64 client_ns;
};
struct bf_ktcp_shared {
    struct bf_uring_loop_control loop;
    __u32 accepted, received, sends, bytes, completed, closed, aborted;
    __u32 max_connections, max_requests, pending, error;
    __u32 head, reserved, dropped, overflow, sqhead, sqtail, cqhead, cqtail;
    __u32 trace_count, trace_overflow;
    int free, active, accepting;
    __u32 connections, seen, next_final;
    __u32 stopping, cancelled, cancel_done;
    __u32 timeout_active, timeout_removing, timeout_idle, timeout_updating;
    struct bf_ktcp_request requests[BF_LLM_SLOTS];
    struct bf_ktcp_record records[128];
};
#endif
