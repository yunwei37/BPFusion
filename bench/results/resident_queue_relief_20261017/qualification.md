# Qualified32-bank constructor and stop lifecycle

Both checkpointsQwen/Smol,normalMakewithCPPFLAGS=-DBF_LLM_SLOTS=32.
2764outcomes,107136checkedtokens,1027intendedrejects/model; actualbatch1..32.
Both graph replay and independently rebuilt attentionmetadata agree exactly.
CPUarchiveanalysis matches acquisitionstdout byte-for-byte. Initial QwenCPU
analysisfailure/repair remains separately preserved; no model rerun or oracle
change. All frozenoutputs and observed errors remain.

Ordinaryuntraced kernelcandidate32 passes480inputactions/model: RST6*banks
andstop8*banks create realbacklog beyond32; complete/partial/empty canceled
outputs checkedagainst the frozenpool. Normalexit and error/pending/reserved/
drop/overflow0,SQ/CQbalance; originalPIDs,pins,GPUownership clean after checks.
Unadmitted stopqueuedrequests are canceled by teardown,not successful outputs.
Network reply-record truncation is diagnostic and remains in raw results;
GPUtraceoverflows are separate. This is finiteengineeringqualification,not
universalmodel fidelity or throughput evidence.
