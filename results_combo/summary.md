# Pullback scanner - backtest report (`pullback_scanner.py`)

* tickers: 878 / 898 | period: 2016-01-01 -> today
* entry: next open | stop: base_lo | target: 2.0R | max hold: 10 days | dedupe cooldown: 5 bars | combo: daily signal within 15 days after a weekly signal
* baseline = every trading day of the same tickers, same period (2,291,105 days)

## 1. Forward returns vs baseline (next open -> close t+h)

| group / horizon | n | mean | median | pct_up | t_vs_base | p |
|---|---|---|---|---|---|---|
| baseline 5d | 2,286,615 | 0.004 | 0.003 | 0.538 |  |  |
| daily 5d | 9,165 | 0.002 | 0.002 | 0.528 | -2.678 | 0.007 |
| weekly 5d | 694 | 0.002 | 0.001 | 0.520 | -1.579 | 0.114 |
| BUY SIGNAL (daily+weekly) 5d | 61 | 0.003 | 0.003 | 0.541 | -0.184 | 0.854 |
| combo 5d | 94 | 0.004 | 0.003 | 0.553 | 0.027 | 0.978 |
| baseline 10d | 2,282,125 | 0.008 | 0.006 | 0.552 |  |  |
| daily 10d | 9,143 | 0.005 | 0.005 | 0.545 | -4.126 | 0.000 |
| weekly 10d | 694 | 0.003 | 0.004 | 0.532 | -2.780 | 0.005 |
| BUY SIGNAL (daily+weekly) 10d | 61 | 0.009 | 0.009 | 0.574 | 0.110 | 0.912 |
| combo 10d | 94 | 0.006 | 0.010 | 0.553 | -0.559 | 0.576 |
| baseline 20d | 2,273,145 | 0.017 | 0.012 | 0.568 |  |  |
| daily 20d | 9,107 | 0.011 | 0.012 | 0.573 | -5.796 | 0.000 |
| weekly 20d | 692 | 0.006 | 0.009 | 0.561 | -4.173 | 0.000 |
| BUY SIGNAL (daily+weekly) 20d | 60 | 0.012 | 0.018 | 0.600 | -0.721 | 0.471 |
| combo 20d | 93 | 0.009 | 0.018 | 0.645 | -1.032 | 0.302 |
| baseline 60d | 2,237,225 | 0.051 | 0.036 | 0.607 |  |  |
| daily 60d | 9,027 | 0.028 | 0.032 | 0.606 | -13.014 | 0.000 |
| weekly 60d | 690 | 0.005 | 0.014 | 0.562 | -8.740 | 0.000 |
| BUY SIGNAL (daily+weekly) 60d | 60 | 0.008 | 0.041 | 0.667 | -2.002 | 0.045 |
| combo 60d | 92 | 0.006 | 0.041 | 0.641 | -2.775 | 0.006 |

> p is a normal-approx Welch test. Baseline days overlap, so treat p as optimistic.

## 2. Trade simulation with the scanner's own levels

| group | n | trades | win_rate | avg_R | R_ci95 | profit_factor | avg_risk_pct | stopped | hit_target | gap_below_stop | total_R |
|---|---|---|---|---|---|---|---|---|---|---|---|
| daily | 9192 | 9035 | 0.508 | 0.071 | [0.05, 0.09] | 1.199 | 0.056 | 0.263 | 0.082 | 0.012 | 656.362 |
| weekly | 696 | 694 | 0.523 | 0.040 | [-0.02, 0.09] | 1.157 | 0.069 | 0.154 | 0.014 | 0 | 28.666 |
| BUY SIGNAL (daily+weekly) | 61 | 61 | 0.574 | 0.072 | [-0.10, 0.24] | 1.300 | 0.070 | 0.164 | 0 | 0 | 4.385 |
| combo | 94 | 94 | 0.553 | 0.066 | [-0.07, 0.20] | 1.262 | 0.067 | 0.160 | 0.011 | 0 | 6.235 |
| CONTROL: random days, same exits | 763445 | 761261 | 0.509 | 0.068 | [0.07, 0.07] | 1.198 | 0.067 | 0.259 | 0.084 | 0 | 52585.225 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the tested signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* daily vs CONTROL: avg_R diff = +0.003R, t = 0.28, p = 0.778
* weekly vs CONTROL: avg_R diff = -0.028R, t = -1.05, p = 0.292
* BUY SIGNAL (daily+weekly) vs CONTROL: avg_R diff = +0.003R, t = 0.04, p = 0.968
* combo vs CONTROL: avg_R diff = -0.002R, t = -0.03, p = 0.977

## 3. Combo signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=25 | 6 | 6 | 0.500 | -0.012 | [-0.68, 0.59] | 0.969 | 0.003 |
| score=50 | 44 | 44 | 0.523 | 0.011 | [-0.21, 0.24] | 1.037 | 0.007 |
| score=75 | 39 | 39 | 0.641 | 0.157 | [-0.05, 0.35] | 1.822 | 0.017 |
| score=100 | 5 | 5 | 0.200 | -0.062 | [-0.30, 0.25] | 0.637 | -0.031 |
| slowing=True | 69 | 69 | 0.536 | 0.037 | [-0.10, 0.19] | 1.154 | 0.011 |
| slowing=False | 25 | 25 | 0.600 | 0.148 | [-0.18, 0.47] | 1.504 | 0.002 |
| drying=True | 10 | 10 | 0.400 | -0.022 | [-0.36, 0.30] | 0.910 | -0.008 |
| drying=False | 84 | 84 | 0.571 | 0.077 | [-0.07, 0.24] | 1.303 | 0.011 |
| uptrend=True | 58 | 58 | 0.603 | 0.164 | [-0.01, 0.33] | 1.814 | 0.008 |
| uptrend=False | 36 | 36 | 0.472 | -0.091 | [-0.32, 0.13] | 0.730 | 0.010 |

Phase lengths found by detect() (bars):

| phase | mean | min | 50% | max |
|---|---|---|---|---|
| decline_len | 18.521 | 3.000 | 17.500 | 40 |
| slowdown_len | 14.681 | 0 | 11 | 49 |
| base_len | 7.798 | 3.000 | 10 | 10 |
| peak_to_low | 28.872 | 6.000 | 31 | 40 |
| base_above_low | 0.009 | 0 | 0.008 | 0.030 |

## 4. Combo signals per year

| year | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| 2016 | 13 | 0.615 | 0.244 | 3.173 | 0.024 |
| 2017 | 18 | 0.444 | 0.067 | 1.200 | 0.010 |
| 2018 | 6 | 0.333 | -0.289 | -1.733 | 0.002 |
| 2019 | 4 | 0.500 | -0.077 | -0.309 | -0.015 |
| 2020 | 7 | 0.429 | -0.332 | -2.322 | -0.066 |
| 2021 | 9 | 0.444 | -0.007 | -0.063 | 0.011 |
| 2023 | 11 | 0.727 | 0.199 | 2.189 | 0.022 |
| 2024 | 7 | 0.857 | 0.338 | 2.369 | 0.016 |
| 2025 | 10 | 0.700 | 0.367 | 3.666 | 0.015 |
| 2026 | 9 | 0.444 | -0.215 | -1.934 | 0.029 |

## 5. Combo signals per ticker (15 worst and 15 best by total_R)

| ticker | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| SGI | 1 | 0 | -1.220 | -1.220 | -0.465 |
| OMC | 1 | 0 | -1.000 | -1.000 | -0.137 |
| HXL | 1 | 0 | -1.000 | -1.000 | -0.081 |
| XYL | 1 | 0 | -1.000 | -1.000 | -0.113 |
| MIDD | 1 | 0 | -1.000 | -1.000 | -0.009 |
| MMS | 1 | 0 | -1.000 | -1.000 | -0.051 |
| PPG | 1 | 0 | -1.000 | -1.000 | -0.007 |
| PRU | 1 | 0 | -1.000 | -1.000 | -0.050 |
| SSB | 1 | 0 | -1.000 | -1.000 | 0.018 |
| SUI | 1 | 0 | -1.000 | -1.000 | 0.012 |
| GPN | 1 | 0 | -1.000 | -1.000 | -0.143 |
| SYK | 1 | 0 | -1.000 | -1.000 | 0.052 |
| WTS | 1 | 0 | -1.000 | -1.000 | -0.007 |
| BEN | 1 | 0 | -1.000 | -1.000 | -0.163 |
| VIAV | 1 | 0 | -1.000 | -1.000 | 0.061 |
| GPC | 1 | 1.000 | 0.732 | 0.732 | 0.066 |
| PAYX | 1 | 1.000 | 0.733 | 0.733 | 0.079 |
| EPR | 1 | 1.000 | 0.734 | 0.734 | 0.003 |
| ADP | 1 | 1.000 | 0.735 | 0.735 | 0.064 |
| KHC | 1 | 1.000 | 0.920 | 0.920 | 0.051 |
| LEN | 1 | 1.000 | 0.931 | 0.931 | 0.094 |
| TXNM | 1 | 1.000 | 0.995 | 0.995 | 0.055 |
| BMY | 1 | 1.000 | 1.071 | 1.071 | 0.082 |
| POST | 2 | 1.000 | 0.584 | 1.169 | 0.029 |
| KO | 1 | 1.000 | 1.251 | 1.251 | 0.010 |
| G | 1 | 1.000 | 1.264 | 1.264 | 0.082 |
| MO | 1 | 1.000 | 1.430 | 1.430 | 0.022 |
| DGX | 1 | 1.000 | 1.566 | 1.566 | 0.083 |
| WM | 3 | 1.000 | 0.694 | 2.082 | 0.064 |
| AYI | 1 | 1.000 | 2.129 | 2.129 | 0.043 |
