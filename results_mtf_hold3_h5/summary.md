# Multi-timeframe strategy - 1489 stocks, 5-min data 2026-08-17 15:10:00-04:00 -> 2026-11-03 15:30:00-05:00

params: D_SPREAD=0.05, D_CONV_DAYS=10, D_FIRST=20, D_HOLD=3, ARM_DAYS=5, H_SPREAD=0.05, RSI_OS=30, RSI_LOOK=6, STOP_BARS=12, COST=0.0005

| group | exit | trades | days | win | avg/trade | 95% CI (date-clustered) | avg R |
|---|---|---|---|---|---|---|---|
| **FULL: daily + hourly + 5m trigger** | eod | 50 | 24 | 42% | +0.008% | [-0.274%, +0.358%] | -0.207 |
| **FULL: daily + hourly + 5m trigger** | 2R | 50 | 24 | 36% | -0.050% | [-0.257%, +0.211%] | -0.032 |
| **FULL: daily + hourly + 5m trigger** | next | 50 | 24 | 30% | +0.206% | [-0.198%, +0.642%] | +0.809 |
| daily + 5m trigger (no hourly filter) | eod | 84 | 26 | 49% | +0.043% | [-0.186%, +0.293%] | +0.375 |
| daily + 5m trigger (no hourly filter) | 2R | 86 | 27 | 42% | -0.033% | [-0.200%, +0.163%] | +0.015 |
| daily + 5m trigger (no hourly filter) | next | 83 | 26 | 33% | +0.217% | [-0.148%, +0.627%] | +0.753 |
| daily + hourly conv + above hourly MAs + 5m | eod | 1 | | | | | |
| daily + hourly conv + above hourly MAs + 5m | 2R | 1 | | | | | |
| daily + hourly conv + above hourly MAs + 5m | next | 1 | | | | | |
| 5m trigger only (all stocks/days) | eod | 26,409 | 55 | 44% | -0.129% | [-0.218%, -0.030%] | -0.340 |
| 5m trigger only (all stocks/days) | 2R | 26,684 | 56 | 37% | -0.136% | [-0.189%, -0.075%] | -0.024 |
| 5m trigger only (all stocks/days) | next | 26,278 | 55 | 25% | -0.155% | [-0.281%, -0.023%] | +0.028 |
| random 5m entry, daily + hourly days | eod | 200 | 36 | 42% | -0.067% | [-0.272%, +0.136%] | -1.917 |
| random 5m entry, daily + hourly days | 2R | 204 | 37 | 35% | -0.076% | [-0.208%, +0.081%] | -0.037 |
| random 5m entry, daily + hourly days | next | 199 | 36 | 20% | +0.098% | [-0.186%, +0.377%] | +0.484 |
| random 5m entry, daily-armed days | eod | 302 | 37 | 45% | -0.033% | [-0.176%, +0.105%] | -0.119 |
| random 5m entry, daily-armed days | 2R | 312 | 38 | 34% | -0.082% | [-0.174%, +0.019%] | -0.041 |
| random 5m entry, daily-armed days | next | 301 | 37 | 21% | +0.073% | [-0.145%, +0.287%] | +0.345 |
| random 5m entry, all stocks/days | eod | 78,041 | 55 | 42% | -0.132% | [-0.197%, -0.064%] | -0.087 |
| random 5m entry, all stocks/days | 2R | 79,189 | 56 | 34% | -0.113% | [-0.143%, -0.083%] | -0.009 |
| random 5m entry, all stocks/days | next | 77,829 | 55 | 16% | -0.149% | [-0.213%, -0.079%] | +0.049 |

daily signals feeding the window: 16 distinct dates, 30 stocks
