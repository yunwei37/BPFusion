# Pending-admission plan review

2026-10-15 UTC. Independent reviewer: /root/pending_admission_plan_review.
No GPU experiment was run or interrupted by the reviewer.

## Round 1

Scientific question and strongest same-compute native comparison acceptable.
Not admitted to execution until three executable omissions are repaired:
1. Lifecycle direct pin cleanup omits bpfusion_pending.
2. Promised non-loop compatibility lacks build and source-native command;
   load.py unconditionally overrides --uring with loop comparison.
3. Existing lifecycle cases never exercise queued work beyond model capacity.

Static map reuse, single-consumer peek/reserve/pop, CPU-owned atomic slot
reservation and admission_seen-after-timer/SQ handshake appear reasonable.
Actual verifier, weak ordering and lifecycle behavior remain unproven.
Global queued count delays unrelated dead sockets conservatively, and finite
somaxconn-sized queue is not complete TCP backpressure. Remaining backlog at
stop is cancellation, not completed computation. queued_peak>0 alone is not
evidence of model-slot pressure. Fixed HEAD provenance must follow any intervening
publication. Reviewer requests no extra baseline or model expansion.

## Root repairs before follow-up 1

Added pending to existing lifecycle pin cleanup. Built non-loop traced target
in setup and actual --uring protocol commands for each model in qualification;
mode override now preserves that existing flag. Expanded existing half-close
pipeline6->24 on loop/native, with unchanged independent replay and explicit
640-request/23376-token expected accounting (non-loop retains622/22224).
Loop lifecycle now adds24-request backlog RST, a checked recovery request and
64-connection backlog stop. Each destructive test requires a raw receipt with
queued>8 after all frames are accounted for. Stop bytes are compared as prefixes
of the unchanged frozen complete outputs. Unobserved RST replies remain labeled
unobserved/canceled. Final head+queued accounting retains unadmitted stop work.
Native keeps original32 lifecycle actions.
Private Python AST checks pass only; no build/verifier/model execution yet.
The running offered-load experiment remains unchanged.

## Follow-up 1

2026-10-15 UTC, same independent reviewer: ADMIT. The three executable
omissions are repaired and no new scientific/executability defect identified.
Actual candidate remains unbuilt/unexecuted. The reviewer independently
confirms120 lifecycle actions/78 connections and head+queued accounting,
unobserved RST labeling, compatibility622/22224 and main640/23376 accounting,
matching candidate/native page headers and private build bindings.
Execute only after old full terminal, preservation and fresh result review.
Before setup, synchronize provenance if old results publication changes HEAD.
Literal newline escapes in the added plan prose may be normalized directly.
No additional baseline or review was requested.

## Follow-up 2 (final scoped follow-up)

2026-10-15 UTC: ADMIT. Same independent reviewer verifies private module sources
byte-equal to originals, relative include resolves the candidate page header,
private make/loader/.ko paths and existing TX assertions are correct, and
fixture unload/detach paths are retained. No build/load/test executed.
This is page-layout compatibility dependency, not a model/performance result.
All plan-review rounds are now closed; no additional reviewer resets.
Before execution verify the old full terminal and actual port/module ownership.
