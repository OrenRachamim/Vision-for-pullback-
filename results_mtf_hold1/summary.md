# Multi-timeframe strategy - 1489 stocks, 5-min data 2026-08-17 15:10:00-04:00 -> 2026-11-03 15:30:00-05:00

params: D_SPREAD=0.05, D_CONV_DAYS=10, D_FIRST=20, D_HOLD=1, ARM_DAYS=5, H_SPREAD=0.02, RSI_OS=30, RSI_LOOK=6, STOP_BARS=12, COST=0.0005

| group | exit | trades | days | win | avg/trade | 95% CI (date-clustered) | avg R |
|---|---|---|---|---|---|---|---|
| **FULL: daily + hourly + 5m trigger** | eod | 38 | 20 | 37% | -0.207% | [-0.496%, +0.084%] | -0.107 |
| **FULL: daily + hourly + 5m trigger** | 2R | 39 | 21 | 31% | -0.239% | [-0.439%, -0.002%] | -0.306 |
| **FULL: daily + hourly + 5m trigger** | next | 38 | 20 | 18% | -0.420% | [-0.748%, -0.080%] | -0.602 |
| daily + 5m trigger (no hourly filter) | eod | 170 | 37 | 48% | +0.064% | [-0.083%, +0.249%] | +0.376 |
| daily + 5m trigger (no hourly filter) | 2R | 181 | 38 | 40% | -0.074% | [-0.190%, +0.078%] | -0.012 |
| daily + 5m trigger (no hourly filter) | next | 167 | 37 | 29% | +0.027% | [-0.253%, +0.343%] | +0.367 |
| daily + hourly conv + above hourly MAs + 5m | eod | 3 | | | | | |
| daily + hourly conv + above hourly MAs + 5m | 2R | 3 | | | | | |
| daily + hourly conv + above hourly MAs + 5m | next | 3 | | | | | |
| 5m trigger only (all stocks/days) | eod | 26,409 | 55 | 44% | -0.129% | [-0.218%, -0.030%] | -0.340 |
| 5m trigger only (all stocks/days) | 2R | 26,684 | 56 | 37% | -0.136% | [-0.189%, -0.075%] | -0.024 |
| 5m trigger only (all stocks/days) | next | 26,278 | 55 | 25% | -0.155% | [-0.281%, -0.023%] | +0.028 |
| random 5m entry, daily + hourly days | eod | 112 | 37 | 36% | -0.109% | [-0.271%, +0.050%] | -0.578 |
| random 5m entry, daily + hourly days | 2R | 113 | 38 | 28% | -0.117% | [-0.239%, +0.021%] | -0.096 |
| random 5m entry, daily + hourly days | next | 112 | 37 | 20% | -0.047% | [-0.259%, +0.201%] | -0.078 |
| random 5m entry, daily-armed days | eod | 659 | 52 | 43% | -0.023% | [-0.133%, +0.107%] | -0.086 |
| random 5m entry, daily-armed days | 2R | 692 | 53 | 33% | -0.091% | [-0.171%, +0.012%] | -0.017 |
| random 5m entry, daily-armed days | next | 653 | 52 | 20% | -0.025% | [-0.147%, +0.098%] | +0.248 |
| random 5m entry, all stocks/days | eod | 78,041 | 55 | 42% | -0.132% | [-0.197%, -0.064%] | -0.087 |
| random 5m entry, all stocks/days | 2R | 79,189 | 56 | 34% | -0.113% | [-0.143%, -0.083%] | -0.009 |
| random 5m entry, all stocks/days | next | 77,829 | 55 | 16% | -0.149% | [-0.213%, -0.079%] | +0.049 |

daily signals feeding the window: 17 distinct dates, 26 stocks
