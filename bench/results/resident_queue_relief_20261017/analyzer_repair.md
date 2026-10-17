# Offline capacity-check repair

The real32-bank protocol exits0,independent GPU graph replay and freshly rebuilt
attention metadata agree for107136tokens/2764outcomes. The subsequent older
CPU analyzer fails while reconstructing padding because its helper hardcodes
padded=min(input_tokens,8). This is a capacityassumption in analysis,not an
observed model/output failure. Initial stdout/stderr are preserved.

The copied helper now receives banks from the protocol's existing
banks_by_mode metadata and uses min(input_tokens,banks); both caller sites pass
that known constructor width. Every token/history/shape/sequence-length/
padding/release assertion remains. The original measurement/oracle/replay,
client inputs and compiled executable are unchanged. Same saved32 raw passes
the corrected CPU reconstruction. The previous default8 archived protocol is
also checked for identical output; no GPU rerun or relaxation of exactness.
