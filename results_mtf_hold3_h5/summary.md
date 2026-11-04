# Multi-timeframe strategy - 1489 stocks, 5-min data 2026-08-17 15:10:00-04:00 -> 2026-11-03 15:30:00-05:00

params: D_SPREAD=0.05, D_CONV_DAYS=10, D_FIRST=20, D_HOLD=3, ARM_DAYS=5, H_SPREAD=0.05, RSI_OS=30, RSI_LOOK=6, STOP_BARS=12, COST=0.0005

| group | exit | trades | days | win | avg/trade | 95% CI (date-clustered) | avg R |
|---|---|---|---|---|---|---|---|
| **FULL: daily + hourly + 5m trigger** | eod | 50 | 24 | 42% | +0.008% | [-0.274%, +0.358%] | -0.207 |
| **FULL: daily + hourly + 5m trigger** | 2R | 50 | 24 | 36% | -0.050% | [-0.257%, +0.211%] | -0.032 |
| **FULL: daily + hourly + 5m trigger** | next | 50 | 24 | 30% | +0.206% | [-0.198%, +0.642%] | +0.809 |
| **FULL: daily + hourly + 5m trigger** | tt_sqrt0.5 | 50 | 24 | 46% | -0.032% | [-0.214%, +0.132%] | +0.071 |
| **FULL: daily + hourly + 5m trigger** | tt_sqrt0.3 | 50 | 24 | 52% | -0.037% | [-0.190%, +0.105%] | +0.037 |
| **FULL: daily + hourly + 5m trigger** | tt_sqrt1.0 | 50 | 24 | 30% | +0.173% | [-0.287%, +0.648%] | +0.909 |
| **FULL: daily + hourly + 5m trigger** | tt_lin0.5+1 | 50 | 24 | 42% | -0.006% | [-0.240%, +0.201%] | +0.215 |
| **FULL: daily + hourly + 5m trigger** | tt_lin0.3+0.5 | 50 | 24 | 48% | -0.028% | [-0.214%, +0.131%] | +0.077 |
| **FULL: daily + hourly + 5m trigger** | tt_sqrt0.5_nostop | 50 | 24 | 84% | +0.438% | [-0.020%, +0.791%] | +2.445 |
| daily + 5m trigger (no hourly filter) | eod | 84 | 26 | 49% | +0.043% | [-0.186%, +0.293%] | +0.375 |
| daily + 5m trigger (no hourly filter) | 2R | 86 | 27 | 42% | -0.033% | [-0.200%, +0.163%] | +0.015 |
| daily + 5m trigger (no hourly filter) | next | 83 | 26 | 33% | +0.217% | [-0.148%, +0.627%] | +0.753 |
| daily + 5m trigger (no hourly filter) | tt_sqrt0.5 | 86 | 27 | 51% | +0.041% | [-0.146%, +0.198%] | +0.141 |
| daily + 5m trigger (no hourly filter) | tt_sqrt0.3 | 86 | 27 | 60% | +0.012% | [-0.110%, +0.123%] | +0.083 |
| daily + 5m trigger (no hourly filter) | tt_sqrt1.0 | 86 | 27 | 34% | +0.139% | [-0.216%, +0.436%] | +0.603 |
| daily + 5m trigger (no hourly filter) | tt_lin0.5+1 | 86 | 27 | 44% | +0.035% | [-0.154%, +0.216%] | +0.194 |
| daily + 5m trigger (no hourly filter) | tt_lin0.3+0.5 | 86 | 27 | 53% | +0.001% | [-0.164%, +0.142%] | +0.081 |
| daily + 5m trigger (no hourly filter) | tt_sqrt0.5_nostop | 84 | 26 | 90% | +0.653% | [+0.345%, +0.883%] | +2.528 |
| daily + hourly conv + above hourly MAs + 5m | eod | 1 | | | | | |
| daily + hourly conv + above hourly MAs + 5m | 2R | 1 | | | | | |
| daily + hourly conv + above hourly MAs + 5m | next | 1 | | | | | |
| daily + hourly conv + above hourly MAs + 5m | tt_sqrt0.5 | 1 | | | | | |
| daily + hourly conv + above hourly MAs + 5m | tt_sqrt0.3 | 1 | | | | | |
| daily + hourly conv + above hourly MAs + 5m | tt_sqrt1.0 | 1 | | | | | |
| daily + hourly conv + above hourly MAs + 5m | tt_lin0.5+1 | 1 | | | | | |
| daily + hourly conv + above hourly MAs + 5m | tt_lin0.3+0.5 | 1 | | | | | |
| daily + hourly conv + above hourly MAs + 5m | tt_sqrt0.5_nostop | 1 | | | | | |
| 5m trigger only (all stocks/days) | eod | 26,409 | 55 | 44% | -0.129% | [-0.218%, -0.030%] | -0.340 |
| 5m trigger only (all stocks/days) | 2R | 26,684 | 56 | 37% | -0.136% | [-0.189%, -0.075%] | -0.024 |
| 5m trigger only (all stocks/days) | next | 26,278 | 55 | 25% | -0.155% | [-0.281%, -0.023%] | +0.028 |
| 5m trigger only (all stocks/days) | tt_sqrt0.5 | 26,836 | 56 | 54% | -0.117% | [-0.151%, -0.082%] | +0.024 |
| 5m trigger only (all stocks/days) | tt_sqrt0.3 | 26,861 | 56 | 60% | -0.111% | [-0.138%, -0.083%] | +0.030 |
| 5m trigger only (all stocks/days) | tt_sqrt1.0 | 26,716 | 56 | 37% | -0.152% | [-0.216%, -0.083%] | -0.013 |
| 5m trigger only (all stocks/days) | tt_lin0.5+1 | 26,785 | 56 | 43% | -0.127% | [-0.175%, -0.079%] | +0.029 |
| 5m trigger only (all stocks/days) | tt_lin0.3+0.5 | 26,850 | 56 | 55% | -0.113% | [-0.145%, -0.081%] | +0.035 |
| 5m trigger only (all stocks/days) | tt_sqrt0.5_nostop | 26,478 | 56 | 79% | -0.086% | [-0.228%, +0.054%] | -0.262 |
| random 5m entry, daily + hourly days | eod | 200 | 36 | 42% | -0.067% | [-0.272%, +0.136%] | -1.917 |
| random 5m entry, daily + hourly days | 2R | 204 | 37 | 35% | -0.076% | [-0.208%, +0.081%] | -0.037 |
| random 5m entry, daily + hourly days | next | 199 | 36 | 20% | +0.098% | [-0.186%, +0.377%] | +0.484 |
| random 5m entry, daily + hourly days | tt_sqrt0.5 | 204 | 37 | 33% | -0.055% | [-0.185%, +0.125%] | -0.022 |
| random 5m entry, daily + hourly days | tt_sqrt0.3 | 205 | 37 | 41% | -0.073% | [-0.165%, +0.040%] | +0.005 |
| random 5m entry, daily + hourly days | tt_sqrt1.0 | 199 | 37 | 20% | +0.077% | [-0.248%, +0.425%] | +0.571 |
| random 5m entry, daily + hourly days | tt_lin0.5+1 | 204 | 37 | 25% | -0.004% | [-0.257%, +0.230%] | +0.020 |
| random 5m entry, daily + hourly days | tt_lin0.3+0.5 | 204 | 37 | 35% | -0.075% | [-0.176%, +0.048%] | -0.082 |
| random 5m entry, daily + hourly days | tt_sqrt0.5_nostop | 193 | 37 | 89% | +0.643% | [+0.282%, +0.947%] | +9.073 |
| random 5m entry, daily-armed days | eod | 302 | 37 | 45% | -0.033% | [-0.176%, +0.105%] | -0.119 |
| random 5m entry, daily-armed days | 2R | 312 | 38 | 34% | -0.082% | [-0.174%, +0.019%] | -0.041 |
| random 5m entry, daily-armed days | next | 301 | 37 | 21% | +0.073% | [-0.145%, +0.287%] | +0.345 |
| random 5m entry, daily-armed days | tt_sqrt0.5 | 312 | 38 | 35% | -0.023% | [-0.126%, +0.100%] | +0.612 |
| random 5m entry, daily-armed days | tt_sqrt0.3 | 313 | 38 | 42% | -0.069% | [-0.139%, +0.011%] | +0.003 |
| random 5m entry, daily-armed days | tt_sqrt1.0 | 306 | 38 | 21% | +0.054% | [-0.152%, +0.278%] | +0.862 |
| random 5m entry, daily-armed days | tt_lin0.5+1 | 312 | 38 | 28% | +0.029% | [-0.136%, +0.194%] | +0.561 |
| random 5m entry, daily-armed days | tt_lin0.3+0.5 | 312 | 38 | 37% | -0.057% | [-0.136%, +0.034%] | +0.542 |
| random 5m entry, daily-armed days | tt_sqrt0.5_nostop | 291 | 38 | 90% | +0.733% | [+0.440%, +0.983%] | +10.471 |
| random 5m entry, all stocks/days | eod | 78,041 | 55 | 42% | -0.132% | [-0.197%, -0.064%] | -0.087 |
| random 5m entry, all stocks/days | 2R | 79,189 | 56 | 34% | -0.113% | [-0.143%, -0.083%] | -0.009 |
| random 5m entry, all stocks/days | next | 77,829 | 55 | 16% | -0.149% | [-0.213%, -0.079%] | +0.049 |
| random 5m entry, all stocks/days | tt_sqrt0.5 | 79,302 | 56 | 41% | -0.100% | [-0.124%, -0.077%] | +0.201 |
| random 5m entry, all stocks/days | tt_sqrt0.3 | 79,368 | 56 | 49% | -0.097% | [-0.112%, -0.082%] | +0.219 |
| random 5m entry, all stocks/days | tt_sqrt1.0 | 79,070 | 56 | 24% | -0.124% | [-0.168%, -0.077%] | +0.130 |
| random 5m entry, all stocks/days | tt_lin0.5+1 | 79,203 | 56 | 30% | -0.105% | [-0.139%, -0.069%] | +0.181 |
| random 5m entry, all stocks/days | tt_lin0.3+0.5 | 79,325 | 56 | 42% | -0.098% | [-0.118%, -0.078%] | +0.175 |
| random 5m entry, all stocks/days | tt_sqrt0.5_nostop | 77,453 | 56 | 77% | -0.082% | [-0.220%, +0.055%] | +0.082 |

daily signals feeding the window: 16 distinct dates, 30 stocks
