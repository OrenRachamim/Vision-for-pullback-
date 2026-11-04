# Multi-timeframe strategy - 1489 stocks, 5-min data 2026-08-17 15:10:00-04:00 -> 2026-11-03 15:30:00-05:00

params: D_SPREAD=0.05, D_CONV_DAYS=10, D_FIRST=20, D_HOLD=5, ARM_DAYS=5, H_SPREAD=0.02, RSI_OS=30, RSI_LOOK=6, STOP_BARS=12, COST=0.0005

| group | exit | trades | days | win | avg/trade | 95% CI (date-clustered) | avg R |
|---|---|---|---|---|---|---|---|
| **FULL: daily + hourly + 5m trigger** | eod | 4 | | | | | |
| **FULL: daily + hourly + 5m trigger** | 2R | 4 | | | | | |
| **FULL: daily + hourly + 5m trigger** | next | 4 | | | | | |
| daily + 5m trigger (no hourly filter) | eod | 65 | 20 | 43% | -0.102% | [-0.316%, +0.116%] | -0.273 |
| daily + 5m trigger (no hourly filter) | 2R | 67 | 21 | 39% | -0.142% | [-0.304%, +0.032%] | -0.021 |
| daily + 5m trigger (no hourly filter) | next | 64 | 20 | 22% | -0.341% | [-0.871%, +0.147%] | -0.206 |
| daily + hourly conv + above hourly MAs + 5m | eod | 0 | | | | | |
| daily + hourly conv + above hourly MAs + 5m | 2R | 0 | | | | | |
| daily + hourly conv + above hourly MAs + 5m | next | 0 | | | | | |
| 5m trigger only (all stocks/days) | eod | 26,409 | 55 | 44% | -0.129% | [-0.218%, -0.030%] | -0.340 |
| 5m trigger only (all stocks/days) | 2R | 26,684 | 56 | 37% | -0.136% | [-0.189%, -0.075%] | -0.024 |
| 5m trigger only (all stocks/days) | next | 26,278 | 55 | 25% | -0.155% | [-0.281%, -0.023%] | +0.028 |
| random 5m entry, daily + hourly days | eod | 14 | 13 | 50% | +0.072% | [-0.304%, +0.398%] | +9.105 |
| random 5m entry, daily + hourly days | 2R | 14 | 13 | 36% | +0.043% | [-0.243%, +0.322%] | -0.041 |
| random 5m entry, daily + hourly days | next | 14 | 13 | 36% | +0.340% | [-0.164%, +0.848%] | +1.355 |
| random 5m entry, daily-armed days | eod | 246 | 31 | 51% | +0.021% | [-0.110%, +0.146%] | +2.078 |
| random 5m entry, daily-armed days | 2R | 254 | 32 | 36% | -0.032% | [-0.133%, +0.063%] | +0.012 |
| random 5m entry, daily-armed days | next | 243 | 31 | 19% | -0.020% | [-0.256%, +0.229%] | +0.326 |
| random 5m entry, all stocks/days | eod | 78,041 | 55 | 42% | -0.132% | [-0.197%, -0.064%] | -0.087 |
| random 5m entry, all stocks/days | 2R | 79,189 | 56 | 34% | -0.113% | [-0.143%, -0.083%] | -0.009 |
| random 5m entry, all stocks/days | next | 77,829 | 55 | 16% | -0.149% | [-0.213%, -0.079%] | +0.049 |

daily signals feeding the window: 2 distinct dates, 2 stocks
