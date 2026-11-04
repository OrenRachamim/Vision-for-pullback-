# Multi-timeframe strategy - 1489 stocks, 5-min data 2026-08-17 15:10:00-04:00 -> 2026-11-03 15:30:00-05:00

params: D_SPREAD=0.05, D_CONV_DAYS=10, D_FIRST=20, D_HOLD=1, ARM_DAYS=5, H_SPREAD=0.02, RSI_OS=30, RSI_LOOK=6, STOP_BARS=12, COST=0.0005

| group | exit | trades | days | win | avg/trade | 95% CI (date-clustered) | avg R |
|---|---|---|---|---|---|---|---|
| **FULL: daily + hourly + 5m trigger** | eod | 38 | 20 | 37% | -0.207% | [-0.496%, +0.084%] | -0.107 |
| **FULL: daily + hourly + 5m trigger** | 2R | 39 | 21 | 31% | -0.239% | [-0.439%, -0.002%] | -0.306 |
| **FULL: daily + hourly + 5m trigger** | next | 38 | 20 | 18% | -0.420% | [-0.748%, -0.080%] | -0.602 |
| **FULL: daily + hourly + 5m trigger** | tt_sqrt0.5 | 39 | 21 | 33% | -0.230% | [-0.498%, +0.055%] | -0.441 |
| **FULL: daily + hourly + 5m trigger** | tt_sqrt0.3 | 39 | 21 | 36% | -0.237% | [-0.493%, +0.027%] | -0.403 |
| **FULL: daily + hourly + 5m trigger** | tt_sqrt1.0 | 39 | 21 | 31% | +0.083% | [-0.347%, +0.600%] | -0.149 |
| **FULL: daily + hourly + 5m trigger** | tt_lin0.5+1 | 39 | 21 | 31% | -0.100% | [-0.430%, +0.261%] | -0.311 |
| **FULL: daily + hourly + 5m trigger** | tt_lin0.3+0.5 | 39 | 21 | 36% | -0.224% | [-0.485%, +0.049%] | -0.409 |
| **FULL: daily + hourly + 5m trigger** | tt_sqrt0.5_nostop | 39 | 21 | 69% | -0.048% | [-0.834%, +0.622%] | +1.148 |
| daily + 5m trigger (no hourly filter) | eod | 170 | 37 | 48% | +0.064% | [-0.083%, +0.249%] | +0.376 |
| daily + 5m trigger (no hourly filter) | 2R | 181 | 38 | 40% | -0.074% | [-0.190%, +0.078%] | -0.012 |
| daily + 5m trigger (no hourly filter) | next | 167 | 37 | 29% | +0.027% | [-0.253%, +0.343%] | +0.367 |
| daily + 5m trigger (no hourly filter) | tt_sqrt0.5 | 181 | 38 | 48% | -0.098% | [-0.299%, +0.080%] | +0.102 |
| daily + 5m trigger (no hourly filter) | tt_sqrt0.3 | 181 | 38 | 58% | -0.076% | [-0.272%, +0.078%] | +0.113 |
| daily + 5m trigger (no hourly filter) | tt_sqrt1.0 | 181 | 38 | 35% | +0.162% | [-0.111%, +0.399%] | +0.417 |
| daily + 5m trigger (no hourly filter) | tt_lin0.5+1 | 181 | 38 | 39% | -0.015% | [-0.243%, +0.182%] | +0.117 |
| daily + 5m trigger (no hourly filter) | tt_lin0.3+0.5 | 181 | 38 | 51% | -0.080% | [-0.276%, +0.072%] | +0.138 |
| daily + 5m trigger (no hourly filter) | tt_sqrt0.5_nostop | 174 | 38 | 86% | +0.508% | [+0.129%, +0.828%] | +2.153 |
| daily + hourly conv + above hourly MAs + 5m | eod | 3 | | | | | |
| daily + hourly conv + above hourly MAs + 5m | 2R | 3 | | | | | |
| daily + hourly conv + above hourly MAs + 5m | next | 3 | | | | | |
| daily + hourly conv + above hourly MAs + 5m | tt_sqrt0.5 | 3 | | | | | |
| daily + hourly conv + above hourly MAs + 5m | tt_sqrt0.3 | 3 | | | | | |
| daily + hourly conv + above hourly MAs + 5m | tt_sqrt1.0 | 3 | | | | | |
| daily + hourly conv + above hourly MAs + 5m | tt_lin0.5+1 | 3 | | | | | |
| daily + hourly conv + above hourly MAs + 5m | tt_lin0.3+0.5 | 3 | | | | | |
| daily + hourly conv + above hourly MAs + 5m | tt_sqrt0.5_nostop | 3 | | | | | |
| 5m trigger only (all stocks/days) | eod | 26,409 | 55 | 44% | -0.129% | [-0.218%, -0.030%] | -0.340 |
| 5m trigger only (all stocks/days) | 2R | 26,684 | 56 | 37% | -0.136% | [-0.189%, -0.075%] | -0.024 |
| 5m trigger only (all stocks/days) | next | 26,278 | 55 | 25% | -0.155% | [-0.281%, -0.023%] | +0.028 |
| 5m trigger only (all stocks/days) | tt_sqrt0.5 | 26,836 | 56 | 54% | -0.117% | [-0.151%, -0.082%] | +0.024 |
| 5m trigger only (all stocks/days) | tt_sqrt0.3 | 26,861 | 56 | 60% | -0.111% | [-0.138%, -0.083%] | +0.030 |
| 5m trigger only (all stocks/days) | tt_sqrt1.0 | 26,716 | 56 | 37% | -0.152% | [-0.216%, -0.083%] | -0.013 |
| 5m trigger only (all stocks/days) | tt_lin0.5+1 | 26,785 | 56 | 43% | -0.127% | [-0.175%, -0.079%] | +0.029 |
| 5m trigger only (all stocks/days) | tt_lin0.3+0.5 | 26,850 | 56 | 55% | -0.113% | [-0.145%, -0.081%] | +0.035 |
| 5m trigger only (all stocks/days) | tt_sqrt0.5_nostop | 26,478 | 56 | 79% | -0.086% | [-0.228%, +0.054%] | -0.262 |
| random 5m entry, daily + hourly days | eod | 112 | 37 | 36% | -0.109% | [-0.271%, +0.050%] | -0.578 |
| random 5m entry, daily + hourly days | 2R | 113 | 38 | 28% | -0.117% | [-0.239%, +0.021%] | -0.096 |
| random 5m entry, daily + hourly days | next | 112 | 37 | 20% | -0.047% | [-0.259%, +0.201%] | -0.078 |
| random 5m entry, daily + hourly days | tt_sqrt0.5 | 113 | 38 | 31% | -0.117% | [-0.297%, +0.040%] | -0.208 |
| random 5m entry, daily + hourly days | tt_sqrt0.3 | 113 | 38 | 38% | -0.147% | [-0.301%, -0.018%] | -0.073 |
| random 5m entry, daily + hourly days | tt_sqrt1.0 | 113 | 38 | 26% | +0.027% | [-0.230%, +0.278%] | +0.106 |
| random 5m entry, daily + hourly days | tt_lin0.5+1 | 113 | 38 | 29% | -0.036% | [-0.246%, +0.145%] | -0.081 |
| random 5m entry, daily + hourly days | tt_lin0.3+0.5 | 113 | 38 | 34% | -0.150% | [-0.317%, -0.007%] | -0.164 |
| random 5m entry, daily + hourly days | tt_sqrt0.5_nostop | 111 | 38 | 67% | -0.416% | [-1.010%, +0.117%] | -8.111 |
| random 5m entry, daily-armed days | eod | 659 | 52 | 43% | -0.023% | [-0.133%, +0.107%] | -0.086 |
| random 5m entry, daily-armed days | 2R | 692 | 53 | 33% | -0.091% | [-0.171%, +0.012%] | -0.017 |
| random 5m entry, daily-armed days | next | 653 | 52 | 20% | -0.025% | [-0.147%, +0.098%] | +0.248 |
| random 5m entry, daily-armed days | tt_sqrt0.5 | 693 | 53 | 37% | -0.036% | [-0.123%, +0.057%] | +0.189 |
| random 5m entry, daily-armed days | tt_sqrt0.3 | 695 | 53 | 44% | -0.079% | [-0.141%, -0.018%] | +0.147 |
| random 5m entry, daily-armed days | tt_sqrt1.0 | 686 | 53 | 21% | +0.027% | [-0.106%, +0.171%] | +0.543 |
| random 5m entry, daily-armed days | tt_lin0.5+1 | 692 | 53 | 29% | -0.008% | [-0.130%, +0.112%] | +0.340 |
| random 5m entry, daily-armed days | tt_lin0.3+0.5 | 694 | 53 | 39% | -0.070% | [-0.139%, -0.001%] | +0.174 |
| random 5m entry, daily-armed days | tt_sqrt0.5_nostop | 649 | 53 | 84% | +0.491% | [+0.270%, +0.696%] | +4.857 |
| random 5m entry, all stocks/days | eod | 78,041 | 55 | 42% | -0.132% | [-0.197%, -0.064%] | -0.087 |
| random 5m entry, all stocks/days | 2R | 79,189 | 56 | 34% | -0.113% | [-0.143%, -0.083%] | -0.009 |
| random 5m entry, all stocks/days | next | 77,829 | 55 | 16% | -0.149% | [-0.213%, -0.079%] | +0.049 |
| random 5m entry, all stocks/days | tt_sqrt0.5 | 79,302 | 56 | 41% | -0.100% | [-0.124%, -0.077%] | +0.201 |
| random 5m entry, all stocks/days | tt_sqrt0.3 | 79,368 | 56 | 49% | -0.097% | [-0.112%, -0.082%] | +0.219 |
| random 5m entry, all stocks/days | tt_sqrt1.0 | 79,070 | 56 | 24% | -0.124% | [-0.168%, -0.077%] | +0.130 |
| random 5m entry, all stocks/days | tt_lin0.5+1 | 79,203 | 56 | 30% | -0.105% | [-0.139%, -0.069%] | +0.181 |
| random 5m entry, all stocks/days | tt_lin0.3+0.5 | 79,325 | 56 | 42% | -0.098% | [-0.118%, -0.078%] | +0.175 |
| random 5m entry, all stocks/days | tt_sqrt0.5_nostop | 77,453 | 56 | 77% | -0.082% | [-0.220%, +0.055%] | +0.082 |

daily signals feeding the window: 17 distinct dates, 26 stocks
