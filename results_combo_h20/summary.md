# Pullback scanner - backtest report (`pullback_scanner.py`)

* tickers: 877 / 898 | period: 2016-01-01 -> today
* entry: next open | stop: base_lo | target: 2.0R | max hold: 20 days | dedupe cooldown: 5 bars | combo: daily signal within 15 days after a weekly signal
* baseline = every trading day of the same tickers, same period (2,291,105 days)

## 1. Forward returns vs baseline (next open -> close t+h)

| group / horizon | n | mean | median | pct_up | t_vs_base | p |
|---|---|---|---|---|---|---|
| baseline 5d | 2,286,615 | 0.004 | 0.003 | 0.538 |  |  |
| daily 5d | 9,499 | 0.002 | 0.002 | 0.521 | -3.382 | 0.001 |
| weekly 5d | 717 | -0.000 | -0.000 | 0.492 | -3.269 | 0.001 |
| BUY SIGNAL (daily+weekly) 5d | 73 | -0.003 | -0.002 | 0.452 | -2.215 | 0.027 |
| combo 5d | 115 | -0.002 | -0.001 | 0.478 | -2.488 | 0.013 |
| baseline 10d | 2,282,125 | 0.008 | 0.006 | 0.552 |  |  |
| daily 10d | 9,485 | 0.005 | 0.005 | 0.542 | -4.155 | 0.000 |
| weekly 10d | 717 | 0.001 | 0.002 | 0.515 | -3.937 | 0.000 |
| BUY SIGNAL (daily+weekly) 10d | 73 | 0.001 | -0.000 | 0.479 | -1.621 | 0.105 |
| combo 10d | 115 | -0.002 | -0.001 | 0.470 | -2.594 | 0.009 |
| baseline 20d | 2,273,145 | 0.017 | 0.012 | 0.568 |  |  |
| daily 20d | 9,442 | 0.012 | 0.013 | 0.581 | -4.961 | 0.000 |
| weekly 20d | 715 | 0.005 | 0.009 | 0.568 | -4.565 | 0.000 |
| BUY SIGNAL (daily+weekly) 20d | 73 | 0.009 | 0.014 | 0.589 | -1.044 | 0.296 |
| combo 20d | 113 | 0.006 | 0.014 | 0.602 | -1.585 | 0.113 |
| baseline 60d | 2,237,225 | 0.051 | 0.036 | 0.607 |  |  |
| daily 60d | 9,364 | 0.027 | 0.032 | 0.603 | -13.544 | 0.000 |
| weekly 60d | 713 | 0.002 | 0.014 | 0.562 | -9.410 | 0.000 |
| BUY SIGNAL (daily+weekly) 60d | 73 | 0.001 | 0.041 | 0.644 | -2.684 | 0.007 |
| combo 60d | 112 | -0.001 | 0.035 | 0.607 | -3.687 | 0.000 |

> p is a normal-approx Welch test. Baseline days overlap, so treat p as optimistic.

## 2. Trade simulation with the scanner's own levels

| group | n | trades | win_rate | avg_R | R_ci95 | profit_factor | avg_risk_pct | stopped | hit_target | gap_below_stop | total_R |
|---|---|---|---|---|---|---|---|---|---|---|---|
| daily | 9519 | 9364 | 0.497 | 0.141 | [0.12, 0.17] | 1.319 | 0.055 | 0.378 | 0.166 | 0.011 | 1333.107 |
| weekly | 719 | 717 | 0.543 | 0.114 | [0.05, 0.18] | 1.348 | 0.068 | 0.264 | 0.065 | 0 | 82.420 |
| BUY SIGNAL (daily+weekly) | 73 | 73 | 0.534 | 0.076 | [-0.14, 0.32] | 1.209 | 0.066 | 0.288 | 0.055 | 0 | 5.583 |
| combo | 115 | 115 | 0.539 | 0.077 | [-0.10, 0.27] | 1.200 | 0.064 | 0.313 | 0.070 | 0 | 8.802 |
| CONTROL: random days, same exits | 763445 | 759985 | 0.478 | 0.109 | [0.11, 0.11] | 1.240 | 0.064 | 0.391 | 0.172 | 0 | 83696.865 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the tested signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* daily vs CONTROL: avg_R diff = +0.032R, t = 2.60, p = 0.009
* weekly vs CONTROL: avg_R diff = +0.005R, t = 0.14, p = 0.888
* BUY SIGNAL (daily+weekly) vs CONTROL: avg_R diff = -0.032R, t = -0.28, p = 0.778
* combo vs CONTROL: avg_R diff = -0.032R, t = -0.34, p = 0.731

## 3. Combo signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=25 | 21 | 21 | 0.429 | -0.257 | [-0.69, 0.18] | 0.542 | 0.010 |
| score=50 | 42 | 42 | 0.571 | 0.045 | [-0.26, 0.35] | 1.106 | -0.003 |
| score=75 | 42 | 42 | 0.548 | 0.151 | [-0.13, 0.42] | 1.499 | 0.007 |
| score=100 | 10 | 10 | 0.600 | 0.597 | [-0.01, 1.21] | 5.101 | 0.032 |
| slowing=True | 82 | 82 | 0.537 | 0.130 | [-0.08, 0.33] | 1.368 | 0.007 |
| slowing=False | 33 | 33 | 0.545 | -0.056 | [-0.43, 0.30] | 0.877 | 0.003 |
| drying=True | 12 | 12 | 0.500 | 0.390 | [-0.20, 0.98] | 2.709 | 0.027 |
| drying=False | 103 | 103 | 0.544 | 0.040 | [-0.17, 0.23] | 1.100 | 0.004 |
| uptrend=True | 62 | 62 | 0.613 | 0.276 | [0.05, 0.52] | 2.066 | 0.008 |
| uptrend=False | 53 | 53 | 0.453 | -0.157 | [-0.44, 0.11] | 0.701 | 0.003 |

Phase lengths found by detect() (bars):

| phase | mean | min | 50% | max |
|---|---|---|---|---|
| decline_len | 37 | 3.000 | 31 | 109 |
| slowdown_len | 26.757 | 0 | 21 | 108 |
| base_len | 7.783 | 3.000 | 9.000 | 10 |
| peak_to_low | 58.165 | 7.000 | 49 | 120 |
| base_above_low | 0.010 | 0 | 0.010 | 0.030 |

## 4. Combo signals per year

| year | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| 2016 | 15 | 0.600 | 0.326 | 4.886 | 0.011 |
| 2017 | 17 | 0.529 | 0.153 | 2.599 | 0.002 |
| 2018 | 12 | 0.583 | -0.083 | -0.995 | -0.004 |
| 2019 | 10 | 0.700 | 0.487 | 4.869 | 0.027 |
| 2020 | 7 | 0.429 | 0.051 | 0.360 | -0.066 |
| 2021 | 9 | 0.778 | 0.371 | 3.343 | 0.048 |
| 2022 | 1 | 0 | -1.000 | -1.000 | -0.011 |
| 2023 | 16 | 0.438 | -0.353 | -5.653 | -0.008 |
| 2024 | 8 | 0.500 | 0.058 | 0.466 | 0.013 |
| 2025 | 9 | 0.556 | 0.006 | 0.054 | 0.006 |
| 2026 | 11 | 0.364 | -0.012 | -0.127 | 0.027 |

## 5. Combo signals per ticker (15 worst and 15 best by total_R)

| ticker | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| TXNM | 2 | 0.500 | -0.940 | -1.879 | -0.055 |
| SGI | 1 | 0 | -1.220 | -1.220 | -0.465 |
| PSX | 1 | 0 | -1.136 | -1.136 | -0.009 |
| XYL | 1 | 0 | -1.000 | -1.000 | -0.113 |
| EBAY | 1 | 0 | -1.000 | -1.000 | -0.009 |
| EGP | 1 | 0 | -1.000 | -1.000 |  |
| OGS | 1 | 0 | -1.000 | -1.000 | 0.013 |
| FNF | 1 | 0 | -1.000 | -1.000 | 0.009 |
| HCA | 1 | 0 | -1.000 | -1.000 | -0.105 |
| HII | 1 | 0 | -1.000 | -1.000 | -0.096 |
| STAG | 1 | 0 | -1.000 | -1.000 |  |
| XOM | 1 | 0 | -1.000 | -1.000 | -0.032 |
| PRU | 1 | 0 | -1.000 | -1.000 | -0.050 |
| INCY | 1 | 0 | -1.000 | -1.000 | -0.027 |
| OMC | 1 | 0 | -1.000 | -1.000 | -0.137 |
| DIS | 1 | 1.000 | 1.238 | 1.238 | 0.075 |
| BMY | 1 | 1.000 | 1.264 | 1.264 | 0.082 |
| ADP | 1 | 1.000 | 1.292 | 1.292 | 0.064 |
| CPT | 1 | 1.000 | 1.459 | 1.459 | 0.076 |
| PAYX | 1 | 1.000 | 1.460 | 1.460 | 0.079 |
| G | 1 | 1.000 | 1.632 | 1.632 | 0.082 |
| IDXX | 1 | 1.000 | 1.642 | 1.642 | 0.092 |
| GNTX | 1 | 1.000 | 2.000 | 2.000 | 0.190 |
| NWS | 1 | 1.000 | 2.000 | 2.000 | 0.043 |
| AKAM | 1 | 1.000 | 2.000 | 2.000 | 0.102 |
| RPM | 1 | 1.000 | 2.000 | 2.000 | 0.031 |
| ROL | 1 | 1.000 | 2.000 | 2.000 | 0.125 |
| WM | 2 | 1.000 | 1.154 | 2.308 | 0.073 |
| DTE | 1 | 1.000 | 2.701 | 2.701 | 0.072 |
| EXC | 3 | 1.000 | 1.278 | 3.833 | 0.061 |
