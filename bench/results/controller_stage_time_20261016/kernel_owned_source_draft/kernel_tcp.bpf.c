// SPDX-License-Identifier: GPL-2.0
// Private prototype: the existing kernel loop, rather than a GPU CTA, owns TCP.
#include "vmlinux.h"
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_tracing.h>
#include <linux/errno.h>
#include "bpfusion_admission.h"
#include "kernel_tcp_state.h"

/* Stable io_uring UAPI flag values, to be checked against actual build headers. */
#define KTCP_CQE_MORE (1u << 1)
#define KTCP_CANCEL_ALL (1u << 0)
#define KTCP_CANCEL_ANY (1u << 2)
#define KTCP_TIMEOUT_UPDATE (1u << 1)
#define KTCP_MSG_NOSIGNAL 0x4000u

extern __u8 *bpf_io_uring_get_region(struct iou_ctx *, __u32, const size_t) __ksym;
extern int bpf_io_uring_submit_sqes(struct iou_ctx *, __u32) __ksym;
/* Derived once from the actual existing stream map, ring setup and allocation;
 * readonly specialization is required for verifier memory bounds, not a knob. */
const volatile struct bf_ktcp_layout config = {};
static const char reply_ok[] =
    "HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: ";
static const char reply_error[] =
    "HTTP/1.1 400 Bad Request\r\nContent-Type: application/octet-stream\r\nContent-Length: ";

struct step {
    __u8 *memory, *rings, *sq;
    struct bf_ktcp_shared *s;
    struct bf_page *page;
    __u32 sh, st, cqhead;
};
static __always_inline void order_memory(void)
{
    asm volatile("" ::: "memory");
}
static __always_inline __u32 load32(const __u32 *p)
{
    __u32 value = *(volatile const __u32 *)p;
    order_memory();
    return value;
}
static __always_inline struct bf_ktcp_conn *connection(struct step *x, __u32 i)
{
    if (i >= config.capacity) return 0;
    return (void *)(x->memory + config.conns + i * sizeof(struct bf_ktcp_conn));
}
static __always_inline __u64 operation_id(__u32 kind, __u32 value, __u32 generation)
{
    return ((__u64)kind << 56) | ((__u64)(generation & 0xffffffu) << 32) | value;
}
static __always_inline int enqueue(struct step *x, const struct io_uring_sqe *entry)
{
    if (x->st - x->sh >= config.entries) return 0;
    __u32 i = x->st & (config.entries - 1);
    struct io_uring_sqe *sqe = (void *)(x->sq + i * sizeof(*sqe));
    __builtin_memcpy(sqe, entry, sizeof(*sqe));
    x->st++;
    x->s->pending++;
    return 1;
}
static __always_inline void publish(struct step *x)
{
    order_memory();
    *(volatile __u32 *)(x->rings + config.st) = x->st;
}
static __noinline int admit(struct bf_page *page)
{
    struct bf_llm_pending request;
    for (__u32 n = 0; n < BF_LLM_SLOTS; n++) {
        if (bpf_map_peek_elem(&pending, &request)) break;
        struct bf_llm_slot *slot = llm_reserve(page);
        if (!slot) break;
        if (bpf_map_pop_elem(&pending, &request)) return -1;
        llm_publish(slot, &request);
        __sync_fetch_and_sub(&page->llm_queued, 1);
        __sync_fetch_and_sub(&page->llm_peer_pending[
            bf_pending_bucket(request.addr_be, request.port_be)], 1);
    }
    return 0;
}
static __always_inline int retire(struct step *x, __u32 i, int aborted)
{
    struct bf_ktcp_shared *s = x->s;
    if (i >= BF_LLM_SLOTS) return -1;
    struct bf_ktcp_request *r = &s->requests[i];
    if (r->conn >= 0) {
        struct bf_ktcp_conn *c = connection(x, (__u32)r->conn);
        if (!c) return -1;
        c->reply = r->next;
        if (c->reply < 0) c->last = -1;
    }
    __u32 record = s->trace_count++;
    if (record < 128) {
        s->records[record] = (struct bf_ktcp_record){
            r->seq, r->ng, r->sends, r->early, r->bytes,
            (__u32)aborted, r->client_ns
        };
    } else s->trace_overflow++;
    s->completed++;
    if (aborted) s->aborted++;
    r->active = 0;
    return 0;
}
static __noinline int drain_completions(struct step *x)
{
    struct bf_ktcp_shared *s = x->s;
    __u32 end = load32((void *)(x->rings + config.ct));
    for (__u32 n = 0; n < 2 * config.entries; n++) {
        if (x->cqhead == end) break;
        __u32 j = x->cqhead & (2 * config.entries - 1);
        struct io_uring_cqe *cq = (void *)(x->rings + config.cqes +
                                         j * sizeof(struct io_uring_cqe));
        struct io_uring_cqe e;
        __builtin_memcpy(&e, cq, sizeof(e));
        x->cqhead++;
        __u32 kind = e.user_data >> 56, index = (__u32)e.user_data;
        if (kind == 8 && (e.flags & KTCP_CQE_MORE)) continue;
        if (!s->pending) return -1;
        s->pending--;
        __u32 prefix = e.user_data >> 48;
        if (prefix == BF_IO_SEND_TAG || prefix == BF_IO_ABORT_TAG) kind = 7;
        if (kind == 1) {
            struct bf_ktcp_conn *c = connection(x, index);
            if (!c) return -1;
            s->accepting = -1;
            if (e.res >= 0) {
                c->fd = e.res; c->next = s->active; s->active = index;
                s->connections++; s->accepted++;
                if (s->connections > s->max_connections)
                    s->max_connections = s->connections;
                if (s->stopping) c->dead = 1;
            } else {
                c->next = s->free; s->free = index;
                if (e.res != -ECANCELED) return -1;
            }
        } else if (kind == 2) {
            struct bf_ktcp_conn *c = connection(x, index);
            if (!c) return -1;
            c->receiving = 0;
            if (e.res > 0) s->received++;
            else if (e.res == 0) c->eof = 1;
            else if (e.res != -EAGAIN && e.res != -EINTR) c->dead = 1;
        } else if (kind == 3 || kind == 7) {
            __u32 i = index % BF_LLM_SLOTS;
            struct bf_ktcp_request *r = &s->requests[i];
            if (!r->active || !r->busy || r->tag != e.user_data) return -1;
            r->busy = 0;
            if (prefix == BF_IO_ABORT_TAG) {
                if (e.res || r->seq != s->next_final || retire(x, i, 1)) return -1;
                s->next_final++;
            } else if (e.res > 0) {
                r->sent += e.res; r->bytes += e.res; s->bytes += e.res;
                r->sends++; s->sends++; if (!r->final) r->early++;
                __u32 length = (e.user_data >> 32) & 0xffff;
                if (kind == 7 && (__u32)e.res == length) {
                    if (r->seq != s->next_final || retire(x, i, 0)) return -1;
                    s->next_final++;
                }
            } else if (r->conn >= 0) {
                struct bf_ktcp_conn *c = connection(x, (__u32)r->conn);
                if (!c) return -1;
                c->dead = 1;
            }
        } else if (kind == 4) {
            struct bf_ktcp_conn *c = connection(x, index);
            if (!c) return -1;
            c->fd = -1; c->closing = 0; s->closed++;
        } else if (kind == 5) s->cancel_done = 1;
        else if (kind == 6) { /* target RECV retains its own CQE */ }
        else if (kind == 8) {
            s->timeout_active = 0;
            if (e.res != -ECANCELED) return -1;
        } else if (kind == 9) {
            if (e.res == -ENOENT) s->timeout_removing = 0;
            else if (e.res < 0) return -1;
        } else if (kind == 10) {
            s->timeout_updating = 0;
            if (!e.res) s->timeout_idle = index;
            s->loop.timer_may_idle = s->timeout_idle;
            if (e.res < 0 && e.res != -ENOENT && e.res != -EALREADY &&
                !(s->stopping && e.res == -ECANCELED)) return -1;
        } else return -1;
    }
    order_memory();
    *(volatile __u32 *)(x->rings + config.ch) = x->cqhead;
    return 0;
}

static __noinline int claim_requests(struct step *x)
{
    struct bf_ktcp_shared *s = x->s;
    for (__u32 n = 0; n < BF_LLM_SLOTS; n++) {
        if (s->seen == load32(&x->page->llm_head)) break;
        __u32 i = s->seen % BF_LLM_SLOTS;
        struct bf_ktcp_request *r = &s->requests[i];
        struct bf_llm_slot *slot = &x->page->llm[i];
        __u32 state = load32(&slot->state);
        if (r->active || (state != BF_PENDING && state != BF_DONE)) break;
        int peer = s->active;
        for (__u32 k = 0; k < config.capacity && peer >= 0; k++) {
            struct bf_ktcp_conn *c = connection(x, (__u32)peer);
            if (!c) return -1;
            struct sockaddr_in *addr = (void *)(x->memory + config.buffers +
                              (__u32)peer * BF_KTCP_RX_STRIDE + 4096);
            if (slot->addr_be == addr->sin_addr.s_addr &&
                slot->port_be == addr->sin_port) break;
            peer = c->next;
        }
        if (peer < 0 && !s->stopping) break;
        *r = (struct bf_ktcp_request){
            .conn = peer, .next = -1, .seq = s->seen,
            .ng = load32(&slot->n_gen), .active = 1,
            .client_ns = *(volatile __u64 *)&slot->client_ns
        };
        if (peer >= 0) {
            struct bf_ktcp_conn *c = connection(x, (__u32)peer);
            if (!c) return -1;
            if (c->last >= 0) {
                if ((__u32)c->last >= BF_LLM_SLOTS) return -1;
                s->requests[c->last].next = i;
            } else c->reply = i;
            c->last = i;
        }
        s->seen++;
    }
    return 0;
}
static __noinline int prepare_header(struct step *x, __u32 i, __u32 bad, __u32 flags)
{
    if (i >= BF_LLM_SLOTS) return -1;
    struct bf_ktcp_request *r = &x->s->requests[i];
    __u8 *tx = x->memory + config.tx + i * BF_KTCP_TX_STRIDE;
    __u32 count = 0;
    if ((flags & BF_LLM_TRANSPORT_MASK) == 2) {
        if (bad) {
            __builtin_memcpy(tx, reply_error, sizeof(reply_error)-1);
            count = sizeof(reply_error)-1;
        } else {
            __builtin_memcpy(tx, reply_ok, sizeof(reply_ok)-1);
            count = sizeof(reply_ok)-1;
        }
        __u32 value = bad ? 0 : r->ng * 4;
        if (value > BF_LLM_MAX_TOK * 4) return -1;
        char digits[4];
        __u32 n = 0;
        for (__u32 k = 0; k < 4; k++) {
            digits[n++] = '0' + value % 10; value /= 10;
            if (!value) break;
        }
        for (__u32 k = 0; k < 4; k++) {
            if (!n) break;
            tx[count++] = digits[--n];
        }
        tx[count++] = '\r'; tx[count++] = '\n';
        tx[count++] = '\r'; tx[count++] = '\n';
    }
    r->header = count; r->header_ready = 1;
    return 0;
}
static __noinline int send_replies(struct step *x)
{
    struct bf_ktcp_shared *s = x->s;
    __u32 active_requests = 0;
    for (__u32 i = 0; i < BF_LLM_SLOTS; i++) {
        struct bf_ktcp_request *r = &s->requests[i];
        if (!r->active) continue;
        active_requests++;
        if (r->busy) continue;
        struct bf_llm_slot *slot = &x->page->llm[i];
        __u32 state = load32(&slot->state);
        struct bf_ktcp_conn *c = 0;
        if (r->conn >= 0) {
            c = connection(x, (__u32)r->conn);
            if (!c) return -1;
        }
        int gone = !c || c->dead || s->stopping;
        if (gone) {
            if (r->seq != s->next_final) continue;
            if (state != BF_DONE) {
                if (!s->stopping || !load32(&s->loop.model_quiesced)) continue;
                order_memory(); *(volatile __u32 *)&slot->state = BF_DONE;
            }
            struct io_uring_sqe entry = {};
            entry.opcode = IORING_OP_NOP;
            entry.user_data = (BF_IO_ABORT_TAG << 48) | r->seq;
            if (enqueue(x, &entry)) {
                r->busy = 1; r->tag = entry.user_data; r->final = 1;
            }
            continue;
        }
        if (c->reply != (int)i) continue;
        __u32 flags = *(volatile __u16 *)&slot->pad;
        if (flags & BF_LLM_VALIDATING) continue;
        __u32 bad = flags & BF_LLM_REJECTED;
        if (bad && (state != BF_DONE || r->seq != s->next_final)) continue;
        if (bad && (flags & BF_LLM_TRANSPORT_MASK) == 1) {
            c->dead = 1; continue;
        }
        if (!r->header_ready && prepare_header(x, i, bad, flags)) return -1;
        if (r->header > BF_KTCP_TX_STRIDE - 4 * BF_LLM_MAX_TOK) return -1;
        __u32 produced = bad ? 0 : load32(&slot->produced);
        if (produced > BF_LLM_MAX_TOK) return -1;
        if ((state != BF_DONE || r->seq != s->next_final) &&
            produced && produced == r->ng) produced--;
        int final = state == BF_DONE && r->seq == s->next_final &&
                    (bad || produced == r->ng);
        if (!produced && !bad) continue;
        __u32 total = r->header + produced * 4;
        if (total <= r->sent) continue;
        __u32 first = r->sent > r->header ? (r->sent-r->header)/4 : 0;
        __u8 *tx = x->memory + config.tx + i * BF_KTCP_TX_STRIDE;
        for (__u32 j = 0; j < BF_LLM_MAX_TOK; j++) {
            if (j < first) continue;
            if (j >= produced) break;
            __u32 token = load32(&slot->tok_out[j]);
            for (__u32 byte = 0; byte < 4; byte++)
                tx[r->header+j*4+byte] = (token >> (8*byte)) & 255;
        }
        struct io_uring_sqe entry = {};
        entry.opcode = IORING_OP_SEND; entry.fd = c->fd;
        entry.addr = config.user_base + config.tx +
                     i * BF_KTCP_TX_STRIDE + r->sent;
        entry.len = total-r->sent; entry.msg_flags = KTCP_MSG_NOSIGNAL;
        entry.user_data = final ? ((BF_IO_SEND_TAG << 48) |
            ((__u64)entry.len << 32) | r->seq) : operation_id(3, r->seq, 0);
        if (enqueue(x, &entry)) {
            r->busy = 1; r->tag = entry.user_data; r->final = final;
        }
    }
    if (active_requests > s->max_requests) s->max_requests = active_requests;
    return active_requests;
}
static __noinline int progress_connections(struct step *x)
{
    struct bf_ktcp_shared *s = x->s;
    int previous = -1, current = s->active;
    for (__u32 n = 0; n < config.capacity && current >= 0; n++) {
        __u32 i = current;
        struct bf_ktcp_conn *c = connection(x, i);
        if (!c) return -1;
        if (c->fd < 0 && !c->closing) {
            int next = c->next;
            if (previous < 0) s->active = next;
            else {
                struct bf_ktcp_conn *p = connection(x, (__u32)previous);
                if (!p) return -1;
                p->next = next;
            }
            c->next = s->free; s->free = i; s->connections--;
            current = next; continue;
        }
        if (s->stopping) c->dead = 1;
        if (c->dead && c->receiving && !c->closing) {
            struct io_uring_sqe entry = {};
            entry.opcode = IORING_OP_ASYNC_CANCEL;
            entry.addr = operation_id(2, i, c->generation);
            entry.user_data = operation_id(6, i, c->generation);
            if (enqueue(x, &entry)) c->closing = 2;
        }
        int reclaim = (c->dead || c->eof) && !c->receiving &&
                      c->reply < 0 && c->closing != 1;
        if (reclaim) {
            __u32 queued;
            if (c->eof) {
                struct sockaddr_in *peer = (void *)(x->memory + config.buffers +
                                           i * BF_KTCP_RX_STRIDE + 4096);
                queued = load32(&x->page->llm_peer_pending[
                    bf_pending_bucket(peer->sin_addr.s_addr, peer->sin_port)]);
            } else queued = load32(&x->page->llm_queued);
            /* Preserve corrected pending-acquire before fresh admission head. */
            reclaim = (s->stopping || !queued) &&
                      s->seen == load32(&x->page->llm_head);
        }
        if (reclaim) {
            struct io_uring_sqe entry = {};
            entry.opcode = IORING_OP_CLOSE; entry.fd = c->fd;
            entry.user_data = operation_id(4, i, c->generation);
            if (enqueue(x, &entry)) c->closing = 1;
        } else if (!c->dead && !c->eof && !c->receiving && !s->stopping) {
            struct io_uring_sqe entry = {};
            entry.opcode = IORING_OP_RECV; entry.fd = c->fd;
            entry.addr = config.user_base + config.buffers + i*BF_KTCP_RX_STRIDE;
            entry.len = 4096; entry.user_data = operation_id(2, i, c->generation);
            if (enqueue(x, &entry)) c->receiving = 1;
        }
        previous = i; current = c->next;
    }
    if (!s->stopping && s->accepting < 0 && s->free >= 0) {
        __u32 i = s->free;
        struct bf_ktcp_conn *c = connection(x, i);
        if (!c) return -1;
        int next = c->next;
        __u32 *length = (void *)(x->memory + config.buffers +
                                i*BF_KTCP_RX_STRIDE + 4112);
        *length = sizeof(struct sockaddr_in);
        struct io_uring_sqe entry = {};
        entry.opcode = IORING_OP_ACCEPT; entry.fd = config.listener;
        entry.addr = config.user_base + config.buffers + i*BF_KTCP_RX_STRIDE + 4096;
        entry.off = config.user_base + config.buffers + i*BF_KTCP_RX_STRIDE + 4112;
        entry.user_data = operation_id(1, i, c->generation+1);
        if (enqueue(x, &entry)) {
            s->free = next; s->accepting = i;
            __u32 generation = c->generation+1;
            *c = (struct bf_ktcp_conn){
                .fd=-1, .next=-1, .reply=-1, .last=-1, .generation=generation
            };
        }
    }
    return 0;
}
static __noinline int progress_timer(struct step *x)
{
    struct bf_ktcp_shared *s = x->s;
    if (s->stopping && s->cancel_done &&
        s->timeout_active && !s->timeout_removing) {
        struct io_uring_sqe entry = {};
        entry.opcode = IORING_OP_TIMEOUT_REMOVE;
        entry.addr = 8ULL << 56; entry.user_data = operation_id(9, 0, 0);
        if (enqueue(x, &entry)) s->timeout_removing = 1;
    }
    __u64 now = s->loop.now_ns, deadline = s->loop.deadline_ns;
    int idle = s->seen == s->next_final &&
               s->seen == load32(&x->page->llm_head) &&
               !load32(&x->page->llm_queued) && now && deadline > now;
    if (!s->stopping && s->timeout_active && !s->timeout_updating &&
        (__u32)idle != s->timeout_idle) {
        struct __kernel_timespec *tick = (void *)(x->memory + config.tick);
        __u64 ns = idle ? deadline-now : 60000;
        tick->tv_sec = ns / 1000000000ULL;
        tick->tv_nsec = ns % 1000000000ULL;
        struct io_uring_sqe entry = {};
        entry.opcode = IORING_OP_TIMEOUT_REMOVE;
        entry.addr = 8ULL << 56;
        entry.off = config.user_base + config.tick;
        entry.timeout_flags = KTCP_TIMEOUT_UPDATE;
        entry.user_data = operation_id(10, idle, 0);
        if (enqueue(x, &entry)) s->timeout_updating = 1;
    }
    return 0;
}
static __always_inline int submit(struct step *x, struct iou_ctx *ctx)
{
    if (x->st == x->sh) return 0;
    publish(x);
    return bpf_io_uring_submit_sqes(ctx, x->st-x->sh) < 0 ? -1 : 0;
}
SEC("struct_ops.s/kernel_tcp_step")
int BPF_PROG(kernel_tcp_step, struct iou_ctx *ctx, struct iou_loop_params *lp)
{
    __u8 *memory = bpf_io_uring_get_region(ctx, IOU_REGION_MEM, config.mem_bytes);
    __u8 *rings = bpf_io_uring_get_region(ctx, IOU_REGION_CQ, config.ring_bytes);
    __u8 *sq = bpf_io_uring_get_region(ctx, IOU_REGION_SQ,
                                      config.entries*sizeof(struct io_uring_sqe));
    if (!memory || !rings || !sq) return IOU_LOOP_STOP;
    struct bf_ktcp_shared *s = (void *)memory;
    if (s->loop.finished) return IOU_LOOP_STOP;
    __u64 now = bpf_ktime_get_ns(); s->loop.now_ns = now;
    if (!s->loop.model_quiesced && (s->loop.stop_requested ||
        (s->loop.deadline_ns && now >= s->loop.deadline_ns)))
        return IOU_LOOP_STOP;
    __u32 zero = 0;
    struct bf_page *page = bpf_map_lookup_elem(&ctl, &zero);
    if (!page) return IOU_LOOP_STOP;
    if (s->loop.model_quiesced || *(volatile __u64 *)&page->stop_ns)
        s->stopping = 1;
    __u32 queued = load32(&page->llm_queued);
    if (queued > s->loop.backlog_peak) s->loop.backlog_peak = queued;
    struct step x = {
        .memory=memory, .rings=rings, .sq=sq, .s=s, .page=page,
        .sh=load32((void *)(rings+config.sh)),
        .st=load32((void *)(rings+config.st)),
        .cqhead=load32((void *)(rings+config.ch))
    };
    if (drain_completions(&x)) { s->error=1; return IOU_LOOP_STOP; }
    if (!s->stopping && admit(page)) { s->error=2; return IOU_LOOP_STOP; }
    if (s->stopping && !s->cancelled) {
        struct io_uring_sqe entry = {};
        entry.opcode=IORING_OP_ASYNC_CANCEL;
        entry.cancel_flags=KTCP_CANCEL_ALL|KTCP_CANCEL_ANY;
        entry.user_data=operation_id(5,0,0);
        if (enqueue(&x,&entry)) s->cancelled=1;
    }
    if (s->stopping && !s->cancel_done) {
        if (submit(&x,ctx)) {s->error=3;return IOU_LOOP_STOP;}
        lp->cq_wait_idx=x.cqhead+1;
        return IOU_LOOP_CONTINUE;
    }
    if (claim_requests(&x)) {s->error=4;return IOU_LOOP_STOP;}
    int active_requests=send_replies(&x);
    if (active_requests<0) {s->error=5;return IOU_LOOP_STOP;}
    if (progress_connections(&x)) {s->error=6;return IOU_LOOP_STOP;}
    if (progress_timer(&x)) {s->error=7;return IOU_LOOP_STOP;}
    s->loop.admission_seen=s->seen;
    s->loop.cq_seen=x.cqhead;
    if (submit(&x,ctx)) {s->error=8;return IOU_LOOP_STOP;}
    if (s->stopping && s->cancelled && !s->pending &&
        s->active<0 && !active_requests) {
        s->head=load32(&page->llm_head);s->reserved=load32(&page->llm_reserved);
        s->sqhead=load32((void *)(rings+config.sh));s->sqtail=x.st;
        s->cqhead=x.cqhead;s->cqtail=load32((void *)(rings+config.ct));
        s->dropped=load32((void *)(rings+config.dropped));
        s->overflow=load32((void *)(rings+config.overflow));
        order_memory();s->loop.finished=1;
        return IOU_LOOP_STOP;
    }
    /* CQ consumer is CPU-owned here; newly completed inline submissions must
     * cause another iteration, while future GPU outputs use the existing timer. */
    lp->cq_wait_idx=x.cqhead+1;
    return IOU_LOOP_CONTINUE;
}
SEC(".struct_ops.link")
struct io_uring_bpf_ops io_loop = {
    .loop_step=(void *)kernel_tcp_step,
    .ring_fd=-1,
};
char _license[] SEC("license")="GPL";
