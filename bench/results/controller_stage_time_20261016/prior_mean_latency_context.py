from pathlib import Path
import json,statistics,math
a=Path(__file__).resolve().parent
source=a.parent/"peer_identity_cache_20261016/peer_identity_full/analysis.stdout"
cells=[x for x in map(json.loads,source.read_text().splitlines()) if x.get("event")=="cell_metrics"]
assert len(cells)==15
for x in cells:
 assert x["successes"]==x["attempts"]==11520
 assert abs(x["connect_completion_ms_mean"]-x["connect_ttft_ms_mean"]-63*x["tpot_ms_mean"])<1e-8
left=sorted([x for x in cells if x["condition"]=="before"],key=lambda x:x["pair"])
right=sorted([x for x in cells if x["condition"]=="native"],key=lambda x:x["pair"])
assert [x["pair"] for x in left]==[x["pair"] for x in right]==list(range(5))
for metric,multiplier in [("connect_completion_ms_mean",1),("connect_ttft_ms_mean",1),("tpot_ms_mean",63),("client_scheduling_lag_ms_mean",1)]:
 effects=[multiplier*(x[metric]-y[metric]) for x,y in zip(left,right)]
 mean=statistics.mean(effects);margin=2.776445105*statistics.stdev(effects)/math.sqrt(5)
 print(json.dumps(dict(event="prior_mean_latency_context",contrast="selected before minus native",metric="receive_span_ms_mean" if multiplier==63 else metric,effects=effects,signed_mean_ms=mean,signed_t95_ms=[mean-margin,mean+margin])))
print("All15 cell mean identities hold. Means decompose exactly; marginal P99s do not. This is prior context, not new measured or primary evidence.")
