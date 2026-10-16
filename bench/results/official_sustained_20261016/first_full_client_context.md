# First full block: client-engagement context only

All3 completed cells remain separate from the full retry. No partial paired
primary/server ranking is computed. Five-block full acquisition is incomplete.

|Condition|Attempts/successes/failures|Lag P99 ms|Max lag ms|Worker CPU fractions|Pool flags|
|---|---:|---:|---:|---|---:|
|candidate|11520/11520/0|1.464120|19.568789|0.702539, 0.701099|61|
|native|11520/11520/0|1.746057|35.022716|0.711665, 0.713921|145|
|official|11520/11520/0|416.759742|796.373255|0.915668, 0.911600|221|

Linear P99 uses the fixed analysis convention; earlier415.447ms diagnostic
used nearest order and is kept labeled as such in first_full.md. All worker
requests join exactly; zero actual request failures do not cure a distorted
arrival/client baseline. CPU fractions are per worker acquisition intervals,
not exclusive host capacity or proof of which parser operation caused lag.

All3 actual server terminals exit0, no remaining GPU app/pin/process besides
the original sessions after stop. Original gzip lossless bytes and complete
source/counters/rejections/flags are retained. No old/new source cells mix.
