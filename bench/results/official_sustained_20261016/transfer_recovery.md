# Ordinary retry2 post-serving SSH recovery

The first8 planned serving windows finish; source client/model/metrics remain
the frozen8d565c7 input. After window8, archival reports
client_loop: send disconnect: Connection reset, followed by the append guard
assertion. The server destination has a durable3MiB prefix. All8 real server
terminals exit0, no GPU app/pin remains; original PID1/10909 start ticks remain.
Follow-up all11 nodes Ready with Lease ages1.617--10.216s (<40s), and existing
Workspace/Pod/API reads work. This is a recovered transport/acknowledgment
failure, not evidence of an inference timeout or node outage.

Existing fleet Invoke-ControlPlane retries a command on another reachable
gateway after SSH exit255. A remote append can complete before its SSH
acknowledgment is lost; the old single-offset assertion correctly prevents
blind duplicate append, but stops recovery. Raw stdout from a failed read can
also precede the successful failover response. Original source files remain
on the same client Job and compressed prefixes remain in Workspace TEMP.

Necessary acquisition-only repair: take the final successful one-line read
response; make the existing append operation idempotent by verifying every
already-present byte of that exact chunk against original input, then write at that original byte offset with native pwrite. Repeated or
overlapping retries write identical bytes at the same offset and never append
a second copy or truncate a later completed chunk. Length, offset range, original bytes and lossless
gzip checks remain. No SHA gate, new helper/service, client/server/model/oracle/
timer/primary change, alternate cell or measured rerun. Resume original window8
raw recovery, archive all originals, then continue the same full15-cell matrix
at the first unrun condition. All request failures/flags remain unchanged.

The artifact-only checkpoint8e88d46 records6 archived cells and GPU absence at
publication entry and exit (15.156s interval). It changes later receipt HEAD
without changing the measured source/binaries. checkpoint_publication.json
retains exact times. This transfer fault occurs in post-serving recovery.

Real duplicate-chunk replay verifies the already committed1MiB against the source, with file length unchanged at3MiB and no appended bytes. This confirms the acknowledgment-loss case on the actual retained file. The final transfer uses pwrite for overlapping-retry safety without a lock or helper.

Window8 recovery complete: merged client and all4 original worker files are retained and lossless gzip checks pass. A native pwrite replay of the exact1MiB chunk at offset2097152 leaves the entire5193475-byte compressed file byte-identical. All8 completed server terminals exit0, no measured cell is rerun. Continue condition9 via the original fixed matrix.
