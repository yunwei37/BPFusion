# Default8 mixed-constructor protocol qualification

Four real executors: Qwen and Smol, kernel-loop and efficient native.
All640 outcomes/executor complete:2560 total, including1036 intended rejects;
93504 exact output tokens. Actual batches1..8 engage in every executor.
Existing captured/history and independent fresh-attention-metadata replays
both pass exactly; transport lifetime/counters/queues and syscall checks pass.
Raw requests, GPU histories, references, fresh metadata, strace and logs remain.

This qualifies the traced candidate at8; ordinary mid-output cancellation and
source selection remain pending. Normal untraced8/16 Make targets compile,
but compilation alone does not establish ordinary runtime acceptance.
No serving source/default is promoted by these records.
The failed first attempt ends before attach/bootstrap because archive metadata
looked for an unused original-variant source. The metadata binding repair and
successful rerun preserve the failed attempt; no oracle changed.

CPU replay in the original owning Workspace (copy these sibling scripts with
their relative imports intact if reconstructing elsewhere):

    python3 protocol_analysis.py qwen_protocol8.jsonl
    python3 protocol_analysis.py smol_protocol8.jsonl

Runtime setup/build/driver recipes retain their original owned TEMP paths as
historical commands. Reconstruct a new owned TEMP and pinned requirements;
do not overwrite existing builds or this evidence. Source snapshots and
versions, not the temporary path, identify the tested constructor.
