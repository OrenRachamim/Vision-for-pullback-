# Multi-timeframe search - 1467 stocks, entries 2026-08-18 -> 2026-10-16 (43 days); selection < 2026-09-17 <= test

combos: 4 triggers x 5 daily x 4 hourly = 80, x 11 exits = 880 tested configurations

## Exits compared (no filters; avg per trade after costs)

| exit | random entry (all) | all 4 triggers | random, sel half | random, test half |
|---|---|---|---|---|
| eod | -0.163% | -0.164% | -0.235% | -0.093% |
| L5_tight | -0.102% | -0.112% | -0.119% | -0.086% |
| L1h_tight | -0.194% | -0.182% | -0.261% | -0.128% |
| Ld_tight | -0.423% | -0.419% | -0.701% | -0.153% |
| casc_tight | -0.148% | -0.155% | -0.273% | -0.027% |
| casc_nc_tight | -0.304% | -0.313% | -0.486% | -0.128% |
| L5_wide | -0.116% | -0.105% | -0.151% | -0.082% |
| L1h_wide | -0.296% | -0.292% | -0.428% | -0.169% |
| Ld_wide | -0.617% | -0.613% | -1.299% | +0.046% |
| casc_wide | -0.181% | -0.193% | -0.407% | +0.039% |
| casc_nc_wide | -0.441% | -0.469% | -0.893% | -0.002% |

cascade tight: exits at stage 1 62%, stage 2 26%, stage 3 12%

cascade wide: exits at stage 1 62%, stage 2 25%, stage 3 13%

## Top 20 by selection-half excess over random (n_sel >= 100) -> what happened in the test half

| trigger | daily | hourly | exit | n sel | avg sel | excess sel | n test | avg test | random test | excess test |
|---|---|---|---|---|---|---|---|---|---|---|
| rsimacd | high | hup | Ld_wide | 137 | -0.944% | +0.446% | 68 | +0.197% | +0.176% | +0.022% |
| rsimacd | high | hup | Ld_tight | 137 | -0.380% | +0.444% | 68 | -0.177% | +0.091% | -0.268% |
| rsimacd | high | none | casc_wide | 689 | -0.263% | +0.328% | 288 | -0.213% | -0.014% | -0.199% |
| rsimacd | high | hup | casc_wide | 137 | -0.626% | +0.278% | 68 | -0.349% | +0.046% | -0.396% |
| macd | high | hos | L1h_wide | 238 | -0.648% | +0.270% | 45 | -0.189% | -0.374% | +0.185% |
| rsimacd | pull | hconv | Ld_tight | 231 | -0.238% | +0.257% | 81 | +0.217% | -0.435% | +0.652% |
| rsimacd | pull | hconv | Ld_wide | 231 | -0.592% | +0.237% | 81 | +0.184% | -0.345% | +0.529% |
| rsimacd | high | hup | casc_nc_tight | 137 | -0.380% | +0.235% | 68 | -0.682% | +0.021% | -0.702% |
| orb | up | hos | Ld_wide | 429 | -0.508% | +0.224% | 145 | -2.438% | -2.018% | -0.421% |
| rsimacd | high | hup | casc_tight | 137 | -0.383% | +0.219% | 68 | -0.494% | -0.010% | -0.484% |
| rsimacd | none | hconv | casc_wide | 4395 | -0.212% | +0.219% | 4150 | -0.024% | +0.030% | -0.054% |
| rsimacd | high | hos | L1h_wide | 158 | -0.705% | +0.212% | 35 | -0.629% | -0.374% | -0.255% |
| rsimacd | high | hup | L1h_wide | 137 | -0.256% | +0.212% | 68 | -0.011% | -0.070% | +0.058% |
| rsimacd | up | none | casc_wide | 2625 | -0.227% | +0.209% | 1522 | -0.005% | +0.148% | -0.153% |
| rsimacd | none | none | casc_wide | 8383 | -0.206% | +0.201% | 8416 | -0.008% | +0.039% | -0.047% |
| rsimacd | high | hconv | casc_wide | 416 | -0.255% | +0.196% | 99 | -0.168% | +0.011% | -0.179% |
| rsimacd | high | none | casc_tight | 689 | -0.207% | +0.188% | 288 | -0.147% | -0.031% | -0.115% |
| rsimacd | none | hup | L1h_tight | 457 | -0.267% | +0.184% | 577 | +0.223% | -0.038% | +0.261% |
| rsimacd | up | hconv | casc_wide | 1652 | -0.238% | +0.173% | 756 | -0.039% | +0.067% | -0.106% |
| rsimacd | high | hup | L5_wide | 137 | -0.009% | +0.169% | 68 | -0.138% | -0.100% | -0.038% |

top-20 average excess: selection +0.245% -> test -0.086%
all 638 configs: corr(excess sel, excess test) = -0.00; share with positive test excess: 54%; share with positive test avg: 25%

best selected config ('rsimacd', 'high', 'hup', 'Ld_wide'): test avg +0.197%, 95% date-clustered CI [-0.867%, +1.452%], win 51%, n 68
