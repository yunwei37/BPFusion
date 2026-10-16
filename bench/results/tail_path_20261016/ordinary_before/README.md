# Ordinary default8 lifecycle acceptance (before transport candidate)
All four untraced ordinary executors pass:Qwen/Smol,kernel-loop/native.
The default8 mixed constructor remains a private candidate; this does not
promote serving source or establish a performance benefit.

Cases include idle/reuse,HTTP400 and recovery,binary EOF,half-close,real
first-token RST,backlogged RST and in-flight SIGTERM. Every observed ordinary
token/prefix is checked against a pre-observation frozen exact complete-output
set from earlier independently qualified traces; current untraced batch
history is unobserved. The large kernel backlog includes intentionally
unobserved canceled requests, not complete validated answers. summary.json
separates exact complete tokens,prefix tokens and unobserved cancellations.
Raw wire hex,syscall trace,commands,process result and cleanup records remain.

The missing-gen1-reference preparation assertion occurs before any ordinary
executor starts. The final frozen set draws the already qualified0065 gen1
references and current default8 references,before any ordinary observation;
there is no post-failure output-set expansion. The actual frozen files and
sources are included. All4 driver cases returnpass; no ordinary runtime
failure or retry occurs.
