# Replay after paper-owner corrections

The paper owner committed1e2303ee (Figure3 rounding and native-only32-slot
measurement scope) and5b7dbb75 (FFT1.1%/GEMM1.9% CPU prose). This thread
preserves both commits and changes no paper file.

[Comparison](comparison.md):136PASS,0MISMATCH,0PAPER_CHANGED; command exit0,
214.085s in a new Python3.12 plotting environment, no inference packages or
visible GPU. Eight archived primary stages and90 main graph cells replay
from raw records. The exact7182-input list matches [the original](../inputs.txt);
no raw data, numerical tolerance, metric or underlying analyzer is changed.

The replay parser now checks both newly explicit workload percentages against
their separate unrounded CPU means. Both regenerated data figures are retained.
The previous134PASS/1MISMATCH record remains historical and reproducible against
its original paper revision; it is not the current paper's status.

Run from the source root:

~~~sh
python bench/reproduce_paper.py --output ../artifact-output
~~~

See [command](command.json), [environment](environment.txt) and
[validation](validation.json). Existing GPU smokes and the previous PDF spot
check are historical; no new GPU experiment or PDF compilation is claimed.
Numerical agreement does not settle the interpretation limits in
[ARTIFACT](../../../../ARTIFACT.md).

Sole-thread self-review: the changed expression uses FFT N/K and GEMM N/K
high-resolution process totals in the existing figure order; both are recomputed
from raw counters. Printed decimal precision still controls the same tolerance.
Only the obsolete prose matcher is replaced. Table/plot/other-prose checks and
all frozen results stay unchanged.
