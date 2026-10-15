# Pullback scanner - backtest report (`pullback_scanner.py`)

* tickers: 878 / 898 | period: 2016-01-01 -> today
* entry: next open | stop: base_lo | exit: trailing stop 3.0*ATR14 from highest high, no target | max hold: 60 days | dedupe cooldown: 5 bars | index combo (sector): stock daily signal + index pullback signal within 5 days
* baseline = every trading day of the same tickers, same period (2,291,105 days)

## 1. Forward returns vs baseline (next open -> close t+h)

| group / horizon | n | mean | median | pct_up | t_vs_base | p |
|---|---|---|---|---|---|---|
| baseline 5d | 2,286,615 | 0.004 | 0.003 | 0.538 |  |  |
| daily 5d | 9,165 | 0.002 | 0.002 | 0.528 | -2.678 | 0.007 |
| combo 5d | 2,769 | 0.002 | 0.002 | 0.526 | -1.979 | 0.048 |
| baseline 10d | 2,282,125 | 0.008 | 0.006 | 0.552 |  |  |
| daily 10d | 9,143 | 0.005 | 0.005 | 0.545 | -4.126 | 0.000 |
| combo 10d | 2,763 | 0.007 | 0.006 | 0.554 | -1.232 | 0.218 |
| baseline 20d | 2,273,145 | 0.017 | 0.012 | 0.568 |  |  |
| daily 20d | 9,107 | 0.011 | 0.012 | 0.573 | -5.796 | 0.000 |
| combo 20d | 2,760 | 0.014 | 0.014 | 0.576 | -1.703 | 0.089 |
| baseline 60d | 2,237,225 | 0.051 | 0.036 | 0.607 |  |  |
| daily 60d | 9,027 | 0.028 | 0.032 | 0.606 | -13.014 | 0.000 |
| combo 60d | 2,738 | 0.029 | 0.036 | 0.615 | -7.858 | 0.000 |

> p is a normal-approx Welch test. Baseline days overlap, so treat p as optimistic.

## 2. Trade simulation with the scanner's own levels

| group | n | trades | win_rate | avg_R | R_ci95 | profit_factor | avg_risk_pct | stopped | trailed | hit_target | gap_below_stop | total_R |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| daily | 9192 | 9023 | 0.397 | 0.186 | [0.14, 0.23] | 1.438 | 0.056 | 0.186 | 0.776 | 0 | 0.012 | 1706.854 |
| combo | 2787 | 2731 | 0.421 | 0.203 | [0.14, 0.26] | 1.506 | 0.057 | 0.158 | 0.804 | 0 | 0.011 | 562.290 |
| CONTROL: random days, same exits | 763445 | 759805 | 0.368 | 0.138 | [0.13, 0.14] | 1.299 | 0.057 | 0.258 | 0.721 | 0 | 0 | 107800.337 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the tested signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* daily vs CONTROL: avg_R diff = +0.048R, t = 2.17, p = 0.030
* combo vs CONTROL: avg_R diff = +0.065R, t = 2.20, p = 0.028

## 3. Combo signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=25 | 467 | 450 | 0.400 | 0.159 | [0.02, 0.33] | 1.351 | 0.015 |
| score=50 | 1285 | 1265 | 0.425 | 0.207 | [0.13, 0.29] | 1.521 | 0.014 |
| score=75 | 773 | 758 | 0.439 | 0.261 | [0.15, 0.38] | 1.705 | 0.017 |
| score=100 | 262 | 258 | 0.391 | 0.089 | [-0.07, 0.27] | 1.213 | 0.008 |
| slowing=True | 1092 | 1069 | 0.416 | 0.191 | [0.11, 0.29] | 1.474 | 0.011 |
| slowing=False | 1695 | 1662 | 0.425 | 0.211 | [0.14, 0.28] | 1.527 | 0.016 |
| drying=True | 590 | 583 | 0.386 | 0.179 | [0.06, 0.31] | 1.435 | 0.012 |
| drying=False | 2197 | 2148 | 0.431 | 0.210 | [0.14, 0.27] | 1.526 | 0.015 |
| uptrend=True | 1935 | 1903 | 0.439 | 0.220 | [0.15, 0.29] | 1.583 | 0.016 |
| uptrend=False | 852 | 828 | 0.380 | 0.164 | [0.05, 0.29] | 1.360 | 0.011 |

Phase lengths found by detect() (bars):

| phase | mean | min | 50% | max |
|---|---|---|---|---|
| decline_len | 16.163 | 2.000 | 14 | 41 |
| slowdown_len | 7.969 | 0 | 4.000 | 56 |
| base_len | 6.003 | 3.000 | 5.000 | 10 |
| peak_to_low | 21.697 | 0 | 20 | 40 |
| base_above_low | 0.007 | 0 | 0 | 0.044 |

## 4. Combo signals per year

| year | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| 2016 | 340 | 0.517 | 0.365 | 121.510 | 0.035 |
| 2017 | 410 | 0.457 | 0.329 | 133.437 | 0.013 |
| 2018 | 280 | 0.325 | -0.112 | -30.657 | -0.009 |
| 2019 | 170 | 0.432 | 0.235 | 39.692 | 0.012 |
| 2020 | 104 | 0.327 | -0.041 | -4.141 | -0.033 |
| 2021 | 183 | 0.432 | 0.180 | 32.961 | 0.019 |
| 2022 | 86 | 0.209 | -0.250 | -21.486 | -0.001 |
| 2023 | 360 | 0.374 | 0.297 | 105.830 | 0.015 |
| 2024 | 406 | 0.469 | 0.259 | 104.324 | 0.026 |
| 2025 | 261 | 0.400 | 0.101 | 26.171 | 0.011 |
| 2026 | 187 | 0.472 | 0.291 | 54.650 | 0.025 |

## 5. Combo signals per ticker (15 worst and 15 best by total_R)

| ticker | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| UHS | 8 | 0 | -0.922 | -7.375 | -0.027 |
| SR | 8 | 0.125 | -0.726 | -5.810 | -0.039 |
| PRU | 8 | 0 | -0.702 | -5.618 | -0.073 |
| VMI | 7 | 0 | -0.734 | -5.140 | -0.034 |
| VRSK | 5 | 0 | -1.023 | -5.116 | 0.011 |
| MOH | 4 | 0 | -1.255 | -5.021 | -0.071 |
| CNC | 4 | 0 | -1.225 | -4.902 | 0.030 |
| AXTA | 6 | 0 | -0.817 | -4.900 | -0.049 |
| OXY | 6 | 0 | -0.763 | -4.575 | -0.017 |
| UDR | 6 | 0 | -0.710 | -4.260 | -0.001 |
| MZTI | 2 | 0 | -2.120 | -4.240 | -0.052 |
| CB | 6 | 0 | -0.678 | -4.066 | -0.013 |
| VLY | 6 | 0.167 | -0.660 | -3.960 | 0.015 |
| EEFT | 5 | 0 | -0.969 | -3.877 | -0.067 |
| NBIX | 4 | 0 | -0.940 | -3.759 | -0.061 |
| GDDY | 3 | 0.667 | 3.094 | 9.282 | 0.152 |
| KEYS | 5 | 0.800 | 1.922 | 9.609 | 0.046 |
| EXR | 6 | 0.500 | 1.650 | 9.899 | 0.045 |
| DLTR | 3 | 0.667 | 3.343 | 10.028 | 0.122 |
| CDP | 4 | 1.000 | 2.549 | 10.195 | 0.081 |
| HAL | 6 | 0.500 | 1.868 | 11.207 | 0.008 |
| AEP | 7 | 0.833 | 1.995 | 11.970 | 0.035 |
| ETR | 13 | 0.769 | 0.924 | 12.009 | 0.031 |
| CNH | 6 | 0.500 | 2.079 | 12.476 | -0.012 |
| AVAV | 3 | 0.667 | 4.211 | 12.633 | 0.070 |
| BKNG | 3 | 0.667 | 4.512 | 13.535 | 0.045 |
| NWE | 7 | 0.500 | 2.536 | 15.403 | 0.020 |
| WTW | 7 | 0.714 | 2.306 | 16.140 | 0.032 |
| SWKS | 2 | 1.000 | 9.888 | 19.776 | 0.134 |
| PCAR | 6 | 0.667 | 3.853 | 23.119 | 0.058 |
