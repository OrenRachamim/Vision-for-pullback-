# Pullback scanner - backtest report (`pullback_scanner.py`)

* tickers: 858 / 898 | period: 2016-01-01 -> today
* entry: next open | stop: base_lo | target: 2.0R | max hold: 10 days | dedupe cooldown: 5 bars | combo: daily signal within 15 days after a weekly signal
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
| daily | 6968 | 6858 | 0.510 | 0.075 | [0.05, 0.10] | 1.209 | 0.055 | 0.263 | 0.081 | 0.012 | 516.833 |
| weekly | 526 | 524 | 0.492 | -0.006 | [-0.07, 0.05] | 0.980 | 0.067 | 0.156 | 0.013 | 0 | -2.194 |
| BUY SIGNAL (daily+weekly) | 54 | 54 | 0.407 | -0.205 | [-0.41, 0.01] | 0.495 | 0.062 | 0.278 | 0.019 | 0 | -11.078 |
| combo | 85 | 85 | 0.424 | -0.169 | [-0.33, -0.01] | 0.546 | 0.062 | 0.247 | 0.012 | 0 | -14.366 |
| CONTROL: random days, same exits | 763445 | 761311 | 0.502 | 0.069 | [0.07, 0.07] | 1.189 | 0.062 | 0.283 | 0.096 | 0 | 53053.664 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the tested signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* daily vs CONTROL: avg_R diff = +0.006R, t = 0.47, p = 0.637
* weekly vs CONTROL: avg_R diff = -0.075R, t = -2.45, p = 0.014
* BUY SIGNAL (daily+weekly) vs CONTROL: avg_R diff = -0.274R, t = -2.56, p = 0.011
* combo vs CONTROL: avg_R diff = -0.238R, t = -3.00, p = 0.003

## 3. Combo signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=25 | 21 | 21 | 0.381 | -0.316 | [-0.69, 0.04] | 0.365 | 0.010 |
| score=50 | 37 | 37 | 0.351 | -0.294 | [-0.50, -0.07] | 0.333 | 0.003 |
| score=75 | 24 | 24 | 0.542 | 0.102 | [-0.13, 0.35] | 1.506 | 0.008 |
| score=100 | 3 | 3 | 0.667 | 0.236 | [nan, nan] | 79.883 | 0.038 |
| slowing=True | 56 | 56 | 0.429 | -0.114 | [-0.28, 0.07] | 0.655 | 0.006 |
| slowing=False | 29 | 29 | 0.414 | -0.275 | [-0.58, 0.01] | 0.391 | 0.011 |
| drying=True | 5 | 5 | 0.600 | 0.006 | [-0.52, 0.38] | 1.030 | 0.024 |
| drying=False | 80 | 80 | 0.412 | -0.180 | [-0.34, -0.02] | 0.530 | 0.007 |
| uptrend=True | 33 | 33 | 0.545 | 0.076 | [-0.13, 0.28] | 1.383 | 0.013 |
| uptrend=False | 52 | 52 | 0.346 | -0.324 | [-0.54, -0.13] | 0.329 | 0.004 |

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
| 2016 | 10 | 0.400 | -0.002 | -0.025 | -0.003 |
| 2017 | 12 | 0.167 | -0.224 | -2.686 | -0.002 |
| 2018 | 11 | 0.364 | -0.235 | -2.590 | -0.005 |
| 2019 | 5 | 0.600 | 0.045 | 0.225 | 0.041 |
| 2020 | 5 | 0.400 | -0.240 | -1.201 | -0.014 |
| 2021 | 7 | 0.571 | 0.341 | 2.388 | 0.051 |
| 2022 | 1 | 0 | -0.536 | -0.536 | -0.011 |
| 2023 | 14 | 0.429 | -0.524 | -7.340 | -0.012 |
| 2024 | 5 | 1.000 | 0.495 | 2.475 | 0.030 |
| 2025 | 8 | 0.500 | -0.183 | -1.467 | 0.007 |
| 2026 | 7 | 0.286 | -0.516 | -3.609 | 0.037 |

## 5. Combo signals per ticker (15 worst and 15 best by total_R)

| ticker | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| TXNM | 1 | 0 | -3.000 | -3.000 | -0.165 |
| XOM | 1 | 0 | -1.000 | -1.000 | -0.032 |
| HXL | 1 | 0 | -1.000 | -1.000 | -0.081 |
| MIDD | 1 | 0 | -1.000 | -1.000 | -0.009 |
| NEE | 1 | 0 | -1.000 | -1.000 | -0.047 |
| NEM | 1 | 0 | -1.000 | -1.000 | -0.022 |
| FNF | 1 | 0 | -1.000 | -1.000 | 0.009 |
| OGS | 1 | 0 | -1.000 | -1.000 | 0.013 |
| OMC | 1 | 0 | -1.000 | -1.000 | -0.137 |
| PRU | 1 | 0 | -1.000 | -1.000 | -0.050 |
| CUZ | 1 | 0 | -1.000 | -1.000 | -0.013 |
| CB | 1 | 0 | -1.000 | -1.000 | -0.005 |
| BNY | 1 | 0 | -1.000 | -1.000 | -0.112 |
| INCY | 1 | 0 | -1.000 | -1.000 | -0.027 |
| SSB | 1 | 0 | -1.000 | -1.000 | 0.018 |
| RPM | 1 | 1.000 | 0.424 | 0.424 | 0.031 |
| VZ | 2 | 0.500 | 0.213 | 0.426 | 0.069 |
| D | 2 | 0.500 | 0.217 | 0.433 | 0.025 |
| MKC | 1 | 1.000 | 0.454 | 0.454 | 0.047 |
| POST | 1 | 1.000 | 0.483 | 0.483 | 0.031 |
| APH | 1 | 1.000 | 0.517 | 0.517 | 0.067 |
| ACI | 1 | 1.000 | 0.518 | 0.518 | 0.035 |
| HSIC | 1 | 1.000 | 0.529 | 0.529 | 0.023 |
| ROL | 1 | 1.000 | 0.676 | 0.676 | 0.125 |
| GPC | 1 | 1.000 | 0.732 | 0.732 | 0.066 |
| BMY | 1 | 1.000 | 1.071 | 1.071 | 0.082 |
| IBM | 1 | 1.000 | 1.123 | 1.123 | 0.060 |
| MO | 1 | 1.000 | 1.430 | 1.430 | 0.022 |
| WM | 2 | 1.000 | 0.739 | 1.477 | 0.073 |
| GNTX | 1 | 1.000 | 2.000 | 2.000 | 0.190 |
