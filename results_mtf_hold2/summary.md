# Multi-timeframe strategy - 1489 stocks, 5-min data 2026-08-17 15:10:00-04:00 -> 2026-11-03 15:30:00-05:00

params: D_SPREAD=0.05, D_CONV_DAYS=10, D_FIRST=20, D_HOLD=2, ARM_DAYS=5, H_SPREAD=0.02, RSI_OS=30, RSI_LOOK=6, STOP_BARS=12, COST=0.0005

| group | exit | trades | days | win | avg/trade | 95% CI (date-clustered) | avg R |
|---|---|---|---|---|---|---|---|
| **FULL: daily + hourly + 5m trigger** | eod | 7 | 7 | 29% | -0.457% | [-1.275%, +0.246%] | -0.181 |
| **FULL: daily + hourly + 5m trigger** | 2R | 7 | 7 | 14% | -0.345% | [-0.630%, -0.071%] | -0.567 |
| **FULL: daily + hourly + 5m trigger** | next | 7 | 7 | 0% | -0.776% | [-1.321%, -0.392%] | -0.977 |
| daily + 5m trigger (no hourly filter) | eod | 80 | 23 | 45% | -0.111% | [-0.314%, +0.075%] | +0.382 |
| daily + 5m trigger (no hourly filter) | 2R | 85 | 24 | 34% | -0.175% | [-0.310%, -0.015%] | -0.168 |
| daily + 5m trigger (no hourly filter) | next | 79 | 23 | 28% | -0.009% | [-0.367%, +0.429%] | +0.184 |
| daily + hourly conv + above hourly MAs + 5m | eod | 0 | | | | | |
| daily + hourly conv + above hourly MAs + 5m | 2R | 0 | | | | | |
| daily + hourly conv + above hourly MAs + 5m | next | 0 | | | | | |
| 5m trigger only (all stocks/days) | eod | 26,409 | 55 | 44% | -0.129% | [-0.218%, -0.030%] | -0.340 |
| 5m trigger only (all stocks/days) | 2R | 26,684 | 56 | 37% | -0.136% | [-0.189%, -0.075%] | -0.024 |
| 5m trigger only (all stocks/days) | next | 26,278 | 55 | 25% | -0.155% | [-0.281%, -0.023%] | +0.028 |
| random 5m entry, daily + hourly days | eod | 23 | 16 | 35% | -0.249% | [-0.652%, +0.023%] | -3.255 |
| random 5m entry, daily + hourly days | 2R | 23 | 16 | 22% | -0.156% | [-0.245%, -0.062%] | -0.406 |
| random 5m entry, daily + hourly days | next | 23 | 16 | 17% | +0.236% | [-0.223%, +0.839%] | +0.425 |
| random 5m entry, daily-armed days | eod | 303 | 32 | 48% | -0.058% | [-0.156%, +0.047%] | -0.377 |
| random 5m entry, daily-armed days | 2R | 317 | 33 | 33% | -0.116% | [-0.185%, -0.047%] | -0.082 |
| random 5m entry, daily-armed days | next | 299 | 32 | 18% | -0.067% | [-0.233%, +0.097%] | +0.066 |
| random 5m entry, all stocks/days | eod | 78,041 | 55 | 42% | -0.132% | [-0.197%, -0.064%] | -0.087 |
| random 5m entry, all stocks/days | 2R | 79,189 | 56 | 34% | -0.113% | [-0.143%, -0.083%] | -0.009 |
| random 5m entry, all stocks/days | next | 77,829 | 55 | 16% | -0.149% | [-0.213%, -0.079%] | +0.049 |

daily signals feeding the window: 4 distinct dates, 4 stocks
