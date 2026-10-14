# Pullback scanner - backtest report (`pullback_scanner.py`)

* tickers: 877 / 898 | period: 2016-01-01 -> today
* entry: next open | stop: base_lo | target: 2.0R | max hold: 10 days | dedupe cooldown: 5 bars | combo: daily signal within 15 days after a weekly signal
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
| daily | 9596 | 9455 | 0.504 | 0.072 | [0.05, 0.09] | 1.201 | 0.055 | 0.263 | 0.083 | 0.011 | 687.037 |
| weekly | 719 | 717 | 0.505 | 0.007 | [-0.04, 0.06] | 1.027 | 0.068 | 0.160 | 0.015 | 0 | 6.110 |
| BUY SIGNAL (daily+weekly) | 72 | 72 | 0.458 | -0.114 | [-0.29, 0.06] | 0.680 | 0.067 | 0.236 | 0.014 | 0 | -8.232 |
| combo | 113 | 113 | 0.469 | -0.112 | [-0.24, 0.02] | 0.674 | 0.064 | 0.221 | 0.009 | 0 | -12.640 |
| CONTROL: random days, same exits | 763445 | 761307 | 0.503 | 0.068 | [0.07, 0.07] | 1.190 | 0.064 | 0.278 | 0.094 | 0 | 52663.013 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the tested signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* daily vs CONTROL: avg_R diff = +0.003R, t = 0.33, p = 0.741
* weekly vs CONTROL: avg_R diff = -0.061R, t = -2.30, p = 0.021
* BUY SIGNAL (daily+weekly) vs CONTROL: avg_R diff = -0.183R, t = -2.00, p = 0.045
* combo vs CONTROL: avg_R diff = -0.180R, t = -2.65, p = 0.008

## 3. Combo signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=25 | 11 | 11 | 0.364 | -0.563 | [-1.17, -0.02] | 0.213 | -0.022 |
| score=50 | 50 | 50 | 0.420 | -0.169 | [-0.36, 0.02] | 0.532 | 0.004 |
| score=75 | 42 | 42 | 0.571 | 0.041 | [-0.16, 0.24] | 1.155 | 0.019 |
| score=100 | 10 | 10 | 0.400 | 0.025 | [-0.26, 0.31] | 1.142 | -0.001 |
| slowing=True | 89 | 89 | 0.461 | -0.077 | [-0.21, 0.07] | 0.750 | 0.014 |
| slowing=False | 24 | 24 | 0.500 | -0.241 | [-0.61, 0.11] | 0.490 | -0.020 |
| drying=True | 16 | 16 | 0.375 | -0.146 | [-0.43, 0.17] | 0.564 | -0.002 |
| drying=False | 97 | 97 | 0.485 | -0.106 | [-0.25, 0.04] | 0.692 | 0.008 |
| uptrend=True | 59 | 59 | 0.576 | 0.084 | [-0.07, 0.24] | 1.389 | 0.010 |
| uptrend=False | 54 | 54 | 0.352 | -0.326 | [-0.53, -0.13] | 0.323 | 0.003 |

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
| 2016 | 14 | 0.571 | 0.208 | 2.917 | 0.016 |
| 2017 | 17 | 0.353 | -0.089 | -1.519 | 0.002 |
| 2018 | 12 | 0.417 | -0.175 | -2.096 | -0.004 |
| 2019 | 9 | 0.444 | -0.065 | -0.581 | 0.030 |
| 2020 | 7 | 0.429 | -0.332 | -2.322 | -0.066 |
| 2021 | 9 | 0.556 | 0.326 | 2.937 | 0.048 |
| 2022 | 1 | 0 | -0.536 | -0.536 | -0.011 |
| 2023 | 16 | 0.500 | -0.417 | -6.671 | -0.008 |
| 2024 | 8 | 0.750 | 0.154 | 1.233 | 0.013 |
| 2025 | 9 | 0.556 | -0.081 | -0.733 | 0.006 |
| 2026 | 11 | 0.273 | -0.479 | -5.271 | 0.027 |

## 5. Combo signals per ticker (15 worst and 15 best by total_R)

| ticker | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| TXNM | 2 | 0.500 | -1.003 | -2.005 | -0.055 |
| SGI | 1 | 0 | -1.220 | -1.220 | -0.465 |
| PSX | 1 | 0 | -1.136 | -1.136 | -0.009 |
| XYL | 1 | 0 | -1.000 | -1.000 | -0.113 |
| INCY | 1 | 0 | -1.000 | -1.000 | -0.027 |
| MIDD | 1 | 0 | -1.000 | -1.000 | -0.009 |
| MMS | 1 | 0 | -1.000 | -1.000 | -0.051 |
| FNF | 1 | 0 | -1.000 | -1.000 | 0.009 |
| NEE | 1 | 0 | -1.000 | -1.000 | -0.047 |
| NEM | 1 | 0 | -1.000 | -1.000 | -0.022 |
| OGS | 1 | 0 | -1.000 | -1.000 | 0.013 |
| HXL | 1 | 0 | -1.000 | -1.000 | -0.081 |
| CUZ | 1 | 0 | -1.000 | -1.000 | -0.013 |
| PRU | 1 | 0 | -1.000 | -1.000 | -0.050 |
| CB | 1 | 0 | -1.000 | -1.000 | -0.005 |
| HSIC | 1 | 1.000 | 0.529 | 0.529 | 0.023 |
| JBL | 1 | 1.000 | 0.540 | 0.540 | -0.040 |
| COR | 2 | 0.500 | 0.324 | 0.648 | 0.023 |
| ROL | 1 | 1.000 | 0.676 | 0.676 | 0.125 |
| GPC | 1 | 1.000 | 0.732 | 0.732 | 0.066 |
| PAYX | 1 | 1.000 | 0.733 | 0.733 | 0.079 |
| EPR | 1 | 1.000 | 0.734 | 0.734 | 0.003 |
| ADP | 1 | 1.000 | 0.735 | 0.735 | 0.064 |
| AKAM | 1 | 1.000 | 0.896 | 0.896 | 0.102 |
| BMY | 1 | 1.000 | 1.071 | 1.071 | 0.082 |
| POST | 2 | 1.000 | 0.584 | 1.169 | 0.029 |
| G | 1 | 1.000 | 1.264 | 1.264 | 0.082 |
| MO | 1 | 1.000 | 1.430 | 1.430 | 0.022 |
| WM | 2 | 1.000 | 0.739 | 1.477 | 0.073 |
| GNTX | 1 | 1.000 | 2.000 | 2.000 | 0.190 |
