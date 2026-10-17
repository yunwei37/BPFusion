# Lossless worker recovery after measurement

The first real screening cell recovered all eight original worker files by
separate transfers. worker_reconstruction_validation.json verifies their full
bytes equal the corresponding contiguous raw blocks in the merged client log.
The client itself merges by copying original lines without parsing/reserializing.

Later cells transfer the original merged log once. After observer and server
stop, a client-side streaming comparison checks EVERY original worker line
against its merged block and exact EOF,retaining names/byte counts. Server-side
streaming recovery gzip-encodes those same bytes into the original worker
filenames; receipts retain the proof. Main/worker source,timestamps,rows,errors
and timer records stay verbatim. There is no data exclusion or serving/client/
primary-metric change. This removes redundant data transfers and round trips,
all outside measurement windows. Failed transfer/proof retains original files.
