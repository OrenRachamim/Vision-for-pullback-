# Pullback scanner - backtest report (`pullback_scanner.py`)

* tickers: 877 / 898 | period: 2016-01-01 -> today
* entry: next open | stop: base_lo | target: 2.0R | max hold: 20 days | dedupe cooldown: 5 bars | combo: daily signal within 15 days after a weekly signal
* baseline = every trading day of the same tickers, same period (2,291,105 days)

## 1. Forward returns vs baseline (next open -> close t+h)

| group / horizon | n | mean | median | pct_up | t_vs_base | p |
|---|---|---|---|---|---|---|
| baseline 5d | 2,286,615 | 0.004 | 0.003 | 0.538 |  |  |
| daily 5d | 9,576 | 0.002 | 0.002 | 0.520 | -3.483 | 0.000 |
| weekly 5d | 717 | -0.000 | -0.000 | 0.492 | -3.269 | 0.001 |
| BUY SIGNAL (daily+weekly) 5d | 72 | -0.003 | -0.002 | 0.444 | -2.246 | 0.025 |
| combo 5d | 113 | -0.001 | -0.001 | 0.487 | -2.226 | 0.026 |
| baseline 10d | 2,282,125 | 0.008 | 0.006 | 0.552 |  |  |
| daily 10d | 9,562 | 0.005 | 0.005 | 0.542 | -4.214 | 0.000 |
| weekly 10d | 717 | 0.001 | 0.002 | 0.515 | -3.937 | 0.000 |
| BUY SIGNAL (daily+weekly) 10d | 72 | 0.001 | -0.000 | 0.472 | -1.629 | 0.103 |
| combo 10d | 113 | -0.002 | -0.001 | 0.478 | -2.476 | 0.013 |
| baseline 20d | 2,273,145 | 0.017 | 0.012 | 0.568 |  |  |
| daily 20d | 9,519 | 0.012 | 0.013 | 0.580 | -5.044 | 0.000 |
| weekly 20d | 715 | 0.005 | 0.009 | 0.568 | -4.565 | 0.000 |
| BUY SIGNAL (daily+weekly) 20d | 72 | 0.010 | 0.015 | 0.583 | -1.021 | 0.307 |
| combo 20d | 111 | 0.006 | 0.015 | 0.604 | -1.474 | 0.140 |
| baseline 60d | 2,237,225 | 0.051 | 0.036 | 0.607 |  |  |
| daily 60d | 9,441 | 0.027 | 0.032 | 0.603 | -13.543 | 0.000 |
| weekly 60d | 713 | 0.002 | 0.014 | 0.562 | -9.410 | 0.000 |
| BUY SIGNAL (daily+weekly) 60d | 72 | 0.001 | 0.048 | 0.639 | -2.677 | 0.007 |
| combo 60d | 110 | -0.001 | 0.035 | 0.600 | -3.661 | 0.000 |

> p is a normal-approx Welch test. Baseline days overlap, so treat p as optimistic.

## 2. Trade simulation with the scanner's own levels

| group | n | trades | win_rate | avg_R | R_ci95 | profit_factor | avg_risk_pct | stopped | hit_target | gap_below_stop | total_R |
|---|---|---|---|---|---|---|---|---|---|---|---|
| daily | 9596 | 9440 | 0.497 | 0.140 | [0.12, 0.16] | 1.316 | 0.055 | 0.378 | 0.166 | 0.011 | 1332.181 |
| weekly | 719 | 717 | 0.543 | 0.114 | [0.05, 0.18] | 1.348 | 0.068 | 0.264 | 0.065 | 0 | 82.420 |
| BUY SIGNAL (daily+weekly) | 72 | 72 | 0.528 | 0.076 | [-0.15, 0.30] | 1.204 | 0.067 | 0.292 | 0.056 | 0 | 5.467 |
| combo | 113 | 113 | 0.540 | 0.086 | [-0.09, 0.28] | 1.226 | 0.064 | 0.310 | 0.071 | 0 | 9.686 |
| CONTROL: random days, same exits | 763445 | 759950 | 0.479 | 0.109 | [0.11, 0.11] | 1.242 | 0.064 | 0.388 | 0.170 | 0 | 83759.329 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the tested signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* daily vs CONTROL: avg_R diff = +0.031R, t = 2.50, p = 0.012
* weekly vs CONTROL: avg_R diff = +0.005R, t = 0.14, p = 0.890
* BUY SIGNAL (daily+weekly) vs CONTROL: avg_R diff = -0.033R, t = -0.28, p = 0.777
* combo vs CONTROL: avg_R diff = -0.023R, t = -0.24, p = 0.807

## 3. Combo signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=25 | 11 | 11 | 0.364 | -0.651 | [-1.28, -0.05] | 0.205 | -0.022 |
| score=50 | 50 | 50 | 0.480 | 0.026 | [-0.25, 0.29] | 1.062 | 0.004 |
| score=75 | 42 | 42 | 0.714 | 0.313 | [0.05, 0.60] | 2.374 | 0.019 |
| score=100 | 10 | 10 | 0.300 | 0.240 | [-0.42, 0.98] | 1.742 | -0.001 |
| slowing=True | 89 | 89 | 0.562 | 0.156 | [-0.04, 0.37] | 1.469 | 0.014 |
| slowing=False | 24 | 24 | 0.458 | -0.176 | [-0.60, 0.26] | 0.682 | -0.020 |
| drying=True | 16 | 16 | 0.375 | 0.116 | [-0.39, 0.68] | 1.298 | -0.002 |
| drying=False | 97 | 97 | 0.567 | 0.081 | [-0.11, 0.28] | 1.213 | 0.008 |
| uptrend=True | 59 | 59 | 0.627 | 0.322 | [0.07, 0.55] | 2.351 | 0.010 |
| uptrend=False | 54 | 54 | 0.444 | -0.173 | [-0.44, 0.11] | 0.677 | 0.003 |

Phase lengths found by detect() (bars):

| phase | mean | min | 50% | max |
|---|---|---|---|---|
| decline_len | 19.381 | 3.000 | 18 | 40 |
| slowdown_len | 16.168 | 0 | 15 | 49 |
| base_len | 7.850 | 3.000 | 9.000 | 10 |
| peak_to_low | 30.097 | 6.000 | 33 | 40 |
| base_above_low | 0.010 | 0 | 0.009 | 0.030 |

## 4. Combo signals per year

| year | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| 2016 | 14 | 0.643 | 0.420 | 5.886 | 0.016 |
| 2017 | 17 | 0.529 | 0.153 | 2.599 | 0.002 |
| 2018 | 12 | 0.583 | -0.083 | -0.995 | -0.004 |
| 2019 | 9 | 0.667 | 0.528 | 4.753 | 0.030 |
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
| EBAY | 1 | 0 | -1.000 | -1.000 | -0.009 |
| EGP | 1 | 0 | -1.000 | -1.000 |  |
| NEM | 1 | 0 | -1.000 | -1.000 | -0.022 |
| FNF | 1 | 0 | -1.000 | -1.000 | 0.009 |
| PRU | 1 | 0 | -1.000 | -1.000 | -0.050 |
| HCA | 1 | 0 | -1.000 | -1.000 | -0.105 |
| HII | 1 | 0 | -1.000 | -1.000 | -0.096 |
| WTS | 1 | 0 | -1.000 | -1.000 | -0.007 |
| HXL | 1 | 0 | -1.000 | -1.000 | -0.081 |
| OMC | 1 | 0 | -1.000 | -1.000 | -0.137 |
| INCY | 1 | 0 | -1.000 | -1.000 | -0.027 |
| KMB | 1 | 0 | -1.000 | -1.000 | -0.017 |
| DIS | 1 | 1.000 | 1.238 | 1.238 | 0.075 |
| BMY | 1 | 1.000 | 1.264 | 1.264 | 0.082 |
| ADP | 1 | 1.000 | 1.292 | 1.292 | 0.064 |
| CPT | 1 | 1.000 | 1.459 | 1.459 | 0.076 |
| PAYX | 1 | 1.000 | 1.460 | 1.460 | 0.079 |
| G | 1 | 1.000 | 1.632 | 1.632 | 0.082 |
| IDXX | 1 | 1.000 | 1.642 | 1.642 | 0.092 |
| ROL | 1 | 1.000 | 2.000 | 2.000 | 0.125 |
| GNTX | 1 | 1.000 | 2.000 | 2.000 | 0.190 |
| AKAM | 1 | 1.000 | 2.000 | 2.000 | 0.102 |
| RPM | 1 | 1.000 | 2.000 | 2.000 | 0.031 |
| NWS | 1 | 1.000 | 2.000 | 2.000 | 0.043 |
| WM | 2 | 1.000 | 1.154 | 2.308 | 0.073 |
| DTE | 1 | 1.000 | 2.701 | 2.701 | 0.072 |
| EXC | 3 | 1.000 | 1.278 | 3.833 | 0.061 |
