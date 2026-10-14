# Pullback scanner - backtest report (`pullback_scanner.py`)

* tickers: 858 / 898 | period: 2016-01-01 -> today
* entry: next open | stop: base_lo | target: 2.0R | max hold: 5 days | dedupe cooldown: 5 bars | combo: daily signal within 15 days after a weekly signal
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
| daily | 6968 | 6867 | 0.507 | 0.033 | [0.01, 0.05] | 1.121 | 0.055 | 0.156 | 0.037 | 0.012 | 229.506 |
| weekly | 526 | 524 | 0.481 | -0.006 | [-0.05, 0.04] | 0.971 | 0.067 | 0.055 | 0.004 | 0 | -2.189 |
| BUY SIGNAL (daily+weekly) | 54 | 54 | 0.426 | -0.102 | [-0.24, 0.04] | 0.586 | 0.062 | 0.093 | 0.019 | 0 | -5.494 |
| combo | 85 | 85 | 0.459 | -0.095 | [-0.19, 0.01] | 0.581 | 0.062 | 0.071 | 0.012 | 0 | -8.106 |
| CONTROL: random days, same exits | 763445 | 762596 | 0.516 | 0.037 | [0.04, 0.04] | 1.133 | 0.062 | 0.177 | 0.044 | 0 | 28271.487 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the tested signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* daily vs CONTROL: avg_R diff = -0.004R, t = -0.39, p = 0.697
* weekly vs CONTROL: avg_R diff = -0.043R, t = -1.94, p = 0.052
* BUY SIGNAL (daily+weekly) vs CONTROL: avg_R diff = -0.139R, t = -1.93, p = 0.053
* combo vs CONTROL: avg_R diff = -0.132R, t = -2.52, p = 0.012

## 3. Combo signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=25 | 21 | 21 | 0.476 | -0.117 | [-0.29, 0.05] | 0.505 | 0.010 |
| score=50 | 37 | 37 | 0.432 | -0.121 | [-0.29, 0.06] | 0.521 | 0.003 |
| score=75 | 24 | 24 | 0.500 | -0.059 | [-0.23, 0.12] | 0.697 | 0.008 |
| score=100 | 3 | 3 | 0.333 | 0.085 | [nan, nan] | 1.772 | 0.038 |
| slowing=True | 56 | 56 | 0.464 | -0.091 | [-0.23, 0.05] | 0.618 | 0.006 |
| slowing=False | 29 | 29 | 0.448 | -0.103 | [-0.24, 0.03] | 0.495 | 0.011 |
| drying=True | 5 | 5 | 0.400 | -0.111 | [-0.54, 0.30] | 0.529 | 0.024 |
| drying=False | 80 | 80 | 0.463 | -0.094 | [-0.20, 0.01] | 0.584 | 0.007 |
| uptrend=True | 33 | 33 | 0.455 | -0.026 | [-0.16, 0.10] | 0.829 | 0.013 |
| uptrend=False | 52 | 52 | 0.462 | -0.139 | [-0.28, 0.01] | 0.492 | 0.004 |

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
| 2016 | 10 | 0.500 | -0.053 | -0.526 | -0.003 |
| 2017 | 12 | 0.417 | -0.234 | -2.813 | -0.002 |
| 2018 | 11 | 0.455 | -0.186 | -2.048 | -0.005 |
| 2019 | 5 | 0.200 | -0.026 | -0.129 | 0.041 |
| 2020 | 5 | 0.400 | -0.105 | -0.527 | -0.014 |
| 2021 | 7 | 0.571 | 0.398 | 2.788 | 0.051 |
| 2022 | 1 | 1.000 | 0.076 | 0.076 | -0.011 |
| 2023 | 14 | 0.500 | -0.091 | -1.271 | -0.012 |
| 2024 | 5 | 0.400 | 0.059 | 0.297 | 0.030 |
| 2025 | 8 | 0.500 | -0.193 | -1.543 | 0.007 |
| 2026 | 7 | 0.429 | -0.344 | -2.411 | 0.037 |

## 5. Combo signals per ticker (15 worst and 15 best by total_R)

| ticker | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| BKH | 2 | 0 | -0.582 | -1.164 | -0.040 |
| XOM | 1 | 0 | -1.000 | -1.000 | -0.032 |
| PRU | 1 | 0 | -1.000 | -1.000 | -0.050 |
| BNY | 1 | 0 | -1.000 | -1.000 | -0.112 |
| OMC | 1 | 0 | -1.000 | -1.000 | -0.137 |
| CUZ | 1 | 0 | -1.000 | -1.000 | -0.013 |
| OGS | 1 | 0 | -1.000 | -1.000 | 0.013 |
| FE | 2 | 0 | -0.474 | -0.948 | 0.013 |
| STAG | 1 | 0 | -0.846 | -0.846 |  |
| HII | 1 | 0 | -0.638 | -0.638 | -0.096 |
| TXNM | 1 | 0 | -0.615 | -0.615 | -0.165 |
| IBM | 1 | 0 | -0.603 | -0.603 | 0.060 |
| SYK | 1 | 0 | -0.547 | -0.547 | 0.052 |
| EAT | 1 | 0 | -0.517 | -0.517 | 0.018 |
| CB | 1 | 0 | -0.491 | -0.491 | -0.005 |
| GPC | 1 | 1.000 | 0.225 | 0.225 | 0.066 |
| HCA | 1 | 1.000 | 0.229 | 0.229 | -0.105 |
| RPM | 1 | 1.000 | 0.237 | 0.237 | 0.031 |
| BXP | 1 | 1.000 | 0.266 | 0.266 | -0.047 |
| PPG | 1 | 1.000 | 0.275 | 0.275 | -0.020 |
| MKC | 1 | 1.000 | 0.345 | 0.345 | 0.047 |
| BMY | 1 | 1.000 | 0.393 | 0.393 | 0.082 |
| SSB | 1 | 1.000 | 0.421 | 0.421 | 0.018 |
| FNF | 1 | 1.000 | 0.427 | 0.427 | 0.009 |
| ROL | 1 | 1.000 | 0.505 | 0.505 | 0.125 |
| PWR | 1 | 1.000 | 0.560 | 0.560 | 0.015 |
| HSIC | 1 | 1.000 | 0.585 | 0.585 | 0.023 |
| MO | 1 | 1.000 | 0.798 | 0.798 | 0.022 |
| WM | 2 | 1.000 | 0.499 | 0.998 | 0.073 |
| GNTX | 1 | 1.000 | 2.000 | 2.000 | 0.190 |
