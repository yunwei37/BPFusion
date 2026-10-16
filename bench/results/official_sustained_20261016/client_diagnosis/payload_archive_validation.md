# Raw-payload archive validation

All11520 measured requests/737280 output tokens reconstruct exactly from
retained original SSE JSON data payload text: prompt IDs, choice0, finish=length,
token IDs and per-token chunk timestamps match the client rows. 725852
JSON data payloads retained; 156 frozen-pool flags remain unchanged.
This is transport-record validation, not eager/model fidelity or full wire
capture: HTTP/SSE comments/line framing and literal DONE bytes are not archived.
Existing live client still checks HTTP status/content type/DONE/length/range.
No request, flag or partial outcome is removed; all actual outcomes succeed.

The independent same-worker stall analysis succeeds and stores full stdout
and stderr. CPU replay uses actual lossless gzip archives only.
