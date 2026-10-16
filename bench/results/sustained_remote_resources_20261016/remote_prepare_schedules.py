from pathlib import Path
import json,numpy as np
t=Path(__file__).resolve().parent
s={}
for block in range(5):
 for rate in [96,192]:
  count=60*rate;rng=np.random.RandomState(20261015+block)
  delays=np.cumsum([rng.gamma(shape=1.0,scale=1.0/rate) for _ in range(count)])
  delays*=60/delays[-1]
  s[str(block)+'_'+str(rate)]=[int(v*1e9) for v in delays]
(t/'remote_offsets.json').write_text(json.dumps(s,separators=(',',':')))
