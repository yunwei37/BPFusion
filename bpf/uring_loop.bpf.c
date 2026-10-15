// SPDX-License-Identifier: Apache-2.0
// Upstream kernel-loop coordination for a GPU-owned io_uring ring.
#include "vmlinux.h"
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_tracing.h>
#include "bpfusion_admission.h"

extern __u8 *bpf_io_uring_get_region(struct iou_ctx *, __u32, const size_t) __ksym;
extern int bpf_io_uring_submit_sqes(struct iou_ctx *, __u32) __ksym;

SEC("struct_ops.s/uring_loop_step")
int BPF_PROG(uring_loop_step, struct iou_ctx *loop_ctx, struct iou_loop_params *lp)
{
    struct bf_uring_loop_control *control =
        (void *)bpf_io_uring_get_region(loop_ctx, IOU_REGION_MEM, sizeof(*control));
    __u8 *rings = bpf_io_uring_get_region(loop_ctx, IOU_REGION_CQ, 4096);
    if (!control || !rings) return IOU_LOOP_STOP;
    if (control->finished) return IOU_LOOP_STOP;
    __u64 now = bpf_ktime_get_ns();
#ifndef BF_IO_CQ_AFTER_SUBMIT
    control->now_ns = now;
#endif
    if (!control->model_quiesced &&
        (control->stop_requested ||
         (control->deadline_ns && now >= control->deadline_ns)))
        return IOU_LOOP_STOP;
    __u32 zero=0;
    struct bf_page *page=bpf_map_lookup_elem(&ctl,&zero);
    if (!page) return IOU_LOOP_STOP;
    __u32 queued=*(volatile __u32 *)&page->llm_queued;
    if(queued>control->backlog_peak)control->backlog_peak=queued;
    if (!control->model_quiesced && !*(volatile __u64 *)&page->stop_ns) {
        struct bf_llm_pending request;
        /* One CPU consumer owns queue -> model-slot admission. Slot recycling
         * still uses the existing CPU atomic bitmap; GPU performs no host CAS. */
        for (__u32 i=0;i<BF_LLM_SLOTS;i++) {
            if (bpf_map_peek_elem(&pending,&request)) break;
            struct bf_llm_slot *slot=llm_reserve(page);
            if (!slot) break;
            /* No other consumer exists, and producers never overwrite. */
            if (bpf_map_pop_elem(&pending,&request)) return IOU_LOOP_STOP;
            llm_publish(slot,&request);
            __sync_fetch_and_sub(&page->llm_queued,1);
        }
    }
    __u32 sh=control->sq_head, st=control->sq_tail, ct=control->cq_tail;
    if (sh>4092 || st>4092 || ct>4092 || ((sh|st|ct)&3)) return IOU_LOOP_STOP;
    /* The after-submit control retains its fixed timer. */
#ifndef BF_IO_CQ_AFTER_SUBMIT
    /* Snapshot before SQ tail so GPU releases include timer updates. */
    __u32 may_idle=*(volatile __u32 *)&control->timer_may_idle;
    __u32 acknowledged=*(volatile __u32 *)&control->cq_seen;
    __u32 observed=*(volatile __u32 *)(rings+ct);
    __u32 admitted=*(volatile __u32 *)&page->llm_head;
    __u32 admission_seen=*(volatile __u32 *)&control->admission_seen;
    __u32 wait=observed+(!may_idle || acknowledged==observed);
    if(admitted!=admission_seen)wait=observed;
#endif
    __u32 head=*(volatile __u32 *)(rings+sh);
    __u32 tail=*(volatile __u32 *)(rings+st);
    if (tail!=head && bpf_io_uring_submit_sqes(loop_ctx,tail-head)<0)
        return IOU_LOOP_STOP;
    /* Do not sleep past GPU processing that may publish timer/SQ updates. */
#ifdef BF_IO_CQ_AFTER_SUBMIT
    lp->cq_wait_idx=*(volatile __u32 *)(rings+ct)+!control->model_quiesced;
#else
    lp->cq_wait_idx=control->model_quiesced ? *(volatile __u32 *)(rings+ct) : wait;
#endif
    return IOU_LOOP_CONTINUE;
}

SEC(".struct_ops.link")
struct io_uring_bpf_ops io_loop = {
    .loop_step = (void *)uring_loop_step,
    .ring_fd = -1,
};
char _license[] SEC("license") = "GPL";
