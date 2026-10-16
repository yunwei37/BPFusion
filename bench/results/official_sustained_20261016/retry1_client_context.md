# Four-worker prefix: client engagement, no server ranking

|Condition|Attempts/successes/failures|Lag P99 ms|Max lag ms|Worker CPU fractions|Pool flags|
|---|---:|---:|---:|---|---:|
|candidate|11520/11520/0|1.566641|28.501799|0.456493, 0.456808, 0.460760, 0.454542|25|
|native|11520/11520/0|1.297426|12.305131|0.459785, 0.459052, 0.457896, 0.455441|30|
|official|11520/11520/0|208.800613|474.880003|0.583041, 0.583301, 0.581399, 0.582196|295|

All34560 outcomes/worker joins remain, and all3 server terminals exit0.
This3-of15 prefix is incomplete and cannot rank servers. Official substantial
lag persists despite lower per-worker CPU; a root cause is not established.
Post-serving WebSocket recovery failure is separate; all original gzip files
are now recovered/validated. No measured row was retried or replaced.
