# Host-fault interpretation and current recovery boundary

Actual kernel journal at05:28:38 UTC contains global OOM and EXT4/I/O failures.
Stable filesystem UUID mapping—not transient /dev/sdX guesses—maps old sdn
UUID d273db2c-6d6f-44ea-b4b3-9c6d30cd0e8b to original retained
pvc-15127d26-3c24-40f5-ab48-556be201595e (gpu-smt-dev), and old sdt
UUID d5e013d3-cb45-4b3c-af15-131104ffc9f9 to original retained
pvc-9464f7be-753c-4b58-bb6a-c958bd651f9e (social-manager).
Kernel logs show automatic rw remounts at05:29:08 on the same UUIDs.
Existing controllers recreate both affected Pods at05:29:08; retained volumes
are attached/healthy, directories readable and mounts rw on the live checks.
This is not proof every interrupted AI session resumed or a complete
filesystem-integrity examination. No manual restart, fsck, data deletion,
credential/config change or other-project agent takeover was performed.

Original BPFusion volume pvc-5d1b0ce5-fbee-43ef-93f1-d433037bb5e4 remains
rw/readable; Workspace UID and boot unchanged. Real fleet SSH and required
host services work, nodes are Ready, memory available approximately114GiB
at the check, no later matching fault line is observed in the selected
post-run journal. These are current-state checks, not continuous isolation,
proof of permanent recovery or a cause of the earlier fault. OOM kills
Lean49PreparedB processes around99GB RSS; exact causal attribution remains
unproved. Cloudflare SSH observation failure also has no proved cause.

Preserve all experiment rows. The known host discontinuity materially
qualifies Smol performance interpretation even though own clients/servers
complete and first resumed client starts after the logged burst. Qwen ends
before it, but no clean continuous-host proof follows. No clean causal speedup/
regression, equivalence, or total CPU inference is made.
