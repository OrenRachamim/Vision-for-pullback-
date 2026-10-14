# Pullback scanner - backtest report (`pullback_scanner.py`)

* tickers: 858 / 898 | period: 2016-01-01 -> today
* entry: next open | stop: base_lo | target: 2.0R | max hold: 20 days | dedupe cooldown: 5 bars | combo: daily signal within 15 days after a weekly signal
* baseline = every trading day of the same tickers, same period (2,291,105 days)

## 1. Forward returns vs baseline (next open -> close t+h)

| group / horizon | n | mean | median | pct_up | t_vs_base | p |
|---|---|---|---|---|---|---|
| baseline 5d | 2,286,615 | 0.004 | 0.003 | 0.538 |  |  |
| daily 5d | 6,951 | 0.002 | 0.002 | 0.522 | -3.246 | 0.001 |
| weekly 5d | 524 | -0.001 | -0.001 | 0.483 | -3.283 | 0.001 |
| BUY SIGNAL (daily+weekly) 5d | 54 | -0.005 | -0.004 | 0.426 | -2.477 | 0.013 |
| combo 5d | 85 | -0.004 | -0.002 | 0.459 | -2.977 | 0.003 |
| baseline 10d | 2,282,125 | 0.008 | 0.006 | 0.552 |  |  |
| daily 10d | 6,940 | 0.006 | 0.005 | 0.547 | -3.246 | 0.001 |
| weekly 10d | 524 | 0.000 | 0.000 | 0.502 | -4.089 | 0.000 |
| BUY SIGNAL (daily+weekly) 10d | 54 | -0.005 | -0.006 | 0.426 | -2.580 | 0.010 |
| combo 10d | 85 | -0.003 | -0.005 | 0.435 | -2.833 | 0.005 |
| baseline 20d | 2,273,145 | 0.017 | 0.012 | 0.568 |  |  |
| daily 20d | 6,904 | 0.013 | 0.014 | 0.591 | -3.581 | 0.000 |
| weekly 20d | 523 | 0.003 | 0.009 | 0.570 | -4.548 | 0.000 |
| BUY SIGNAL (daily+weekly) 20d | 54 | 0.003 | 0.011 | 0.556 | -1.593 | 0.111 |
| combo 20d | 84 | 0.008 | 0.016 | 0.595 | -1.372 | 0.170 |
| baseline 60d | 2,237,225 | 0.051 | 0.036 | 0.607 |  |  |
| daily 60d | 6,860 | 0.029 | 0.034 | 0.609 | -11.718 | 0.000 |
| weekly 60d | 521 | 0.004 | 0.016 | 0.582 | -7.693 | 0.000 |
| BUY SIGNAL (daily+weekly) 60d | 54 | -0.003 | 0.055 | 0.648 | -2.262 | 0.024 |
| combo 60d | 83 | -0.000 | 0.038 | 0.602 | -3.029 | 0.002 |

> p is a normal-approx Welch test. Baseline days overlap, so treat p as optimistic.

## 2. Trade simulation with the scanner's own levels

| group | n | trades | win_rate | avg_R | R_ci95 | profit_factor | avg_risk_pct | stopped | hit_target | gap_below_stop | total_R |
|---|---|---|---|---|---|---|---|---|---|---|---|
| daily | 6968 | 6847 | 0.505 | 0.155 | [0.13, 0.18] | 1.356 | 0.055 | 0.372 | 0.167 | 0.012 | 1069.102 |
| weekly | 526 | 524 | 0.542 | 0.093 | [0.02, 0.17] | 1.280 | 0.067 | 0.268 | 0.055 | 0 | 49.670 |
| BUY SIGNAL (daily+weekly) | 54 | 54 | 0.481 | -0.071 | [-0.32, 0.19] | 0.841 | 0.062 | 0.352 | 0.037 | 0 | -3.807 |
| combo | 85 | 85 | 0.518 | 0.010 | [-0.20, 0.22] | 1.023 | 0.062 | 0.341 | 0.059 | 0 | 0.813 |
| CONTROL: random days, same exits | 763445 | 760007 | 0.477 | 0.110 | [0.11, 0.11] | 1.241 | 0.062 | 0.395 | 0.174 | 0 | 84578.603 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the tested signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* daily vs CONTROL: avg_R diff = +0.045R, t = 3.12, p = 0.002
* weekly vs CONTROL: avg_R diff = -0.017R, t = -0.42, p = 0.676
* BUY SIGNAL (daily+weekly) vs CONTROL: avg_R diff = -0.181R, t = -1.36, p = 0.174
* combo vs CONTROL: avg_R diff = -0.101R, t = -0.92, p = 0.357

## 3. Combo signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=25 | 21 | 21 | 0.429 | -0.257 | [-0.69, 0.18] | 0.542 | 0.010 |
| score=50 | 37 | 37 | 0.541 | -0.010 | [-0.32, 0.29] | 0.977 | 0.003 |
| score=75 | 24 | 24 | 0.542 | 0.188 | [-0.15, 0.58] | 1.661 | 0.008 |
| score=100 | 3 | 3 | 0.667 | 0.691 | [nan, nan] | 70.225 | 0.038 |
| slowing=True | 56 | 56 | 0.536 | 0.106 | [-0.15, 0.36] | 1.288 | 0.006 |
| slowing=False | 29 | 29 | 0.483 | -0.177 | [-0.54, 0.20] | 0.653 | 0.011 |
| drying=True | 5 | 5 | 0.400 | 0.158 | [-0.56, 0.93] | 1.600 | 0.024 |
| drying=False | 80 | 80 | 0.525 | 0.000 | [-0.21, 0.23] | 1.001 | 0.007 |
| uptrend=True | 33 | 33 | 0.606 | 0.247 | [-0.05, 0.56] | 1.948 | 0.013 |
| uptrend=False | 52 | 52 | 0.462 | -0.141 | [-0.42, 0.13] | 0.727 | 0.004 |

Phase lengths found by detect() (bars):

| phase | mean | min | 50% | max |
|---|---|---|---|---|
| decline_len | 42.118 | 3.000 | 36 | 109 |
| slowdown_len | 28.847 | 2.000 | 22 | 108 |
| base_len | 7.788 | 3.000 | 9.000 | 10 |
| peak_to_low | 64.706 | 7.000 | 57 | 120 |
| base_above_low | 0.010 | 0 | 0.010 | 0.029 |

## 4. Combo signals per year

| year | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| 2016 | 10 | 0.500 | 0.115 | 1.155 | -0.003 |
| 2017 | 12 | 0.500 | 0.088 | 1.054 | -0.002 |
| 2018 | 11 | 0.545 | -0.109 | -1.198 | -0.005 |
| 2019 | 5 | 0.800 | 0.618 | 3.088 | 0.041 |
| 2020 | 5 | 0.400 | -0.041 | -0.204 | -0.014 |
| 2021 | 7 | 0.714 | 0.369 | 2.580 | 0.051 |
| 2022 | 1 | 0 | -1.000 | -1.000 | -0.011 |
| 2023 | 14 | 0.429 | -0.471 | -6.588 | -0.012 |
| 2024 | 5 | 0.800 | 0.544 | 2.722 | 0.030 |
| 2025 | 8 | 0.500 | -0.001 | -0.011 | 0.007 |
| 2026 | 7 | 0.286 | -0.112 | -0.785 | 0.037 |

## 5. Combo signals per ticker (15 worst and 15 best by total_R)

| ticker | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| TXNM | 1 | 0 | -3.000 | -3.000 | -0.165 |
| XOM | 1 | 0 | -1.000 | -1.000 | -0.032 |
| HXL | 1 | 0 | -1.000 | -1.000 | -0.081 |
| STAG | 1 | 0 | -1.000 | -1.000 |  |
| SSB | 1 | 0 | -1.000 | -1.000 | 0.018 |
| MIDD | 1 | 0 | -1.000 | -1.000 | -0.009 |
| EBAY | 1 | 0 | -1.000 | -1.000 | -0.009 |
| SUI | 1 | 0 | -1.000 | -1.000 | 0.012 |
| NEE | 1 | 0 | -1.000 | -1.000 | -0.047 |
| FNF | 1 | 0 | -1.000 | -1.000 | 0.009 |
| PRU | 1 | 0 | -1.000 | -1.000 | -0.050 |
| HCA | 1 | 0 | -1.000 | -1.000 | -0.105 |
| HII | 1 | 0 | -1.000 | -1.000 | -0.096 |
| OMC | 1 | 0 | -1.000 | -1.000 | -0.137 |
| OGS | 1 | 0 | -1.000 | -1.000 | 0.013 |
| GPC | 1 | 1.000 | 0.946 | 0.946 | 0.066 |
| IFF | 1 | 1.000 | 0.949 | 0.949 | 0.068 |
| ROST | 2 | 1.000 | 0.515 | 1.030 | 0.044 |
| BDX | 1 | 1.000 | 1.059 | 1.059 | 0.040 |
| APH | 1 | 1.000 | 1.147 | 1.147 | 0.067 |
| VZ | 2 | 1.000 | 0.587 | 1.175 | 0.069 |
| EXC | 1 | 1.000 | 1.176 | 1.176 | 0.049 |
| DIS | 1 | 1.000 | 1.238 | 1.238 | 0.075 |
| BMY | 1 | 1.000 | 1.264 | 1.264 | 0.082 |
| IDXX | 1 | 1.000 | 1.642 | 1.642 | 0.092 |
| RPM | 1 | 1.000 | 2.000 | 2.000 | 0.031 |
| GNTX | 1 | 1.000 | 2.000 | 2.000 | 0.190 |
| ROL | 1 | 1.000 | 2.000 | 2.000 | 0.125 |
| WM | 2 | 1.000 | 1.154 | 2.308 | 0.073 |
| DTE | 1 | 1.000 | 2.701 | 2.701 | 0.072 |
