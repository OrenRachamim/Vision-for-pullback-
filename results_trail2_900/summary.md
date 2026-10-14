# Pullback scanner - backtest report (`pullback_scanner.py`)

* tickers: 878 / 898 | period: 2016-01-01 -> today
* entry: next open | stop: base_lo | exit: trailing stop 2.0*ATR14 from highest high, no target | max hold: 60 days | dedupe cooldown: 5 bars | combo: daily signal within 15 days after a weekly signal
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

| group | n | trades | win_rate | avg_R | R_ci95 | profit_factor | avg_risk_pct | stopped | trailed | hit_target | gap_below_stop | total_R |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| daily | 9192 | 9034 | 0.393 | 0.094 | [0.07, 0.12] | 1.289 | 0.056 | 0.071 | 0.912 | 0 | 0.012 | 876.787 |
| weekly | 696 | 693 | 0.395 | 0.061 | [0.01, 0.12] | 1.268 | 0.069 | 0.004 | 0.991 | 0 | 0 | 43.737 |
| BUY SIGNAL (daily+weekly) | 61 | 60 | 0.467 | 0.087 | [-0.07, 0.25] | 1.420 | 0.070 | 0 | 0.984 | 0 | 0 | 5.986 |
| combo | 94 | 93 | 0.484 | 0.188 | [0.03, 0.39] | 1.908 | 0.067 | 0.011 | 0.979 | 0 | 0 | 18.220 |
| CONTROL: random days, same exits | 763445 | 761137 | 0.393 | 0.069 | [0.07, 0.07] | 1.220 | 0.067 | 0.094 | 0.903 | 0 | 0 | 54305.193 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the tested signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* daily vs CONTROL: avg_R diff = +0.025R, t = 1.66, p = 0.096
* weekly vs CONTROL: avg_R diff = -0.009R, t = -0.31, p = 0.760
* BUY SIGNAL (daily+weekly) vs CONTROL: avg_R diff = +0.017R, t = 0.21, p = 0.837
* combo vs CONTROL: avg_R diff = +0.118R, t = 1.27, p = 0.204

## 3. Combo signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=25 | 6 | 6 | 0.667 | 0.208 | [-0.13, 0.51] | 2.885 | 0.003 |
| score=50 | 44 | 43 | 0.419 | 0.135 | [-0.09, 0.36] | 1.601 | 0.007 |
| score=75 | 39 | 39 | 0.564 | 0.290 | [-0.01, 0.67] | 2.476 | 0.017 |
| score=100 | 5 | 5 | 0.200 | -0.183 | [-0.41, 0.07] | 0.258 | -0.031 |
| slowing=True | 69 | 68 | 0.426 | 0.126 | [-0.08, 0.37] | 1.544 | 0.011 |
| slowing=False | 25 | 25 | 0.640 | 0.355 | [0.11, 0.61] | 3.566 | 0.002 |
| drying=True | 10 | 10 | 0.400 | 0.054 | [-0.36, 0.58] | 1.212 | -0.008 |
| drying=False | 84 | 83 | 0.494 | 0.204 | [0.02, 0.40] | 2.015 | 0.011 |
| uptrend=True | 58 | 58 | 0.552 | 0.286 | [0.06, 0.55] | 2.596 | 0.008 |
| uptrend=False | 36 | 35 | 0.371 | 0.025 | [-0.21, 0.27] | 1.098 | 0.010 |

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
| 2016 | 13 | 0.538 | 0.358 | 4.650 | 0.024 |
| 2017 | 18 | 0.389 | 0.144 | 2.593 | 0.010 |
| 2018 | 6 | 0.333 | -0.175 | -1.052 | 0.002 |
| 2019 | 4 | 0.250 | -0.230 | -0.919 | -0.015 |
| 2020 | 7 | 0.429 | 0.371 | 2.595 | -0.066 |
| 2021 | 9 | 0.556 | 0.442 | 3.978 | 0.011 |
| 2023 | 11 | 0.545 | 0.167 | 1.834 | 0.022 |
| 2024 | 7 | 0.429 | 0.100 | 0.703 | 0.016 |
| 2025 | 10 | 0.900 | 0.454 | 4.538 | 0.015 |
| 2026 | 9 | 0.250 | -0.185 | -0.700 | 0.029 |

## 5. Combo signals per ticker (15 worst and 15 best by total_R)

| ticker | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| VIAV | 1 | 0 | -1.000 | -1.000 | 0.061 |
| XYL | 1 | 0 | -0.980 | -0.980 | -0.113 |
| HII | 1 | 0 | -0.909 | -0.909 | -0.096 |
| XOM | 1 | 0 | -0.724 | -0.724 | -0.019 |
| SYK | 1 | 0 | -0.702 | -0.702 | 0.052 |
| EAT | 1 | 0 | -0.653 | -0.653 | 0.018 |
| GPN | 1 | 0 | -0.630 | -0.630 | -0.143 |
| ATR | 1 | 0 | -0.623 | -0.623 | 0.020 |
| PRU | 1 | 0 | -0.597 | -0.597 | -0.050 |
| NFG | 1 | 0 | -0.579 | -0.579 | 0.050 |
| SGI | 1 | 0 | -0.541 | -0.541 | -0.465 |
| APH | 1 | 0 | -0.540 | -0.540 | 0.067 |
| ZTS | 1 | 0 | -0.518 | -0.518 | -0.016 |
| MMS | 1 | 0 | -0.518 | -0.518 | -0.051 |
| FTV | 1 | 0 | -0.506 | -0.506 | 0.076 |
| MO | 1 | 1.000 | 0.964 | 0.964 | 0.022 |
| LEN | 1 | 1.000 | 0.987 | 0.987 | 0.094 |
| HSY | 1 | 1.000 | 1.034 | 1.034 | 0.045 |
| AYI | 1 | 1.000 | 1.093 | 1.093 | 0.043 |
| TXNM | 1 | 1.000 | 1.132 | 1.132 | 0.055 |
| VZ | 2 | 1.000 | 0.581 | 1.162 | 0.069 |
| JNJ | 1 | 1.000 | 1.209 | 1.209 | 0.097 |
| CPT | 1 | 1.000 | 1.264 | 1.264 | 0.076 |
| G | 1 | 1.000 | 1.278 | 1.278 | 0.082 |
| PAYX | 1 | 1.000 | 1.572 | 1.572 | 0.079 |
| DIS | 1 | 1.000 | 1.744 | 1.744 | 0.075 |
| ROL | 1 | 1.000 | 2.051 | 2.051 | 0.125 |
| DGX | 1 | 1.000 | 2.310 | 2.310 | 0.083 |
| NWS | 1 | 1.000 | 3.686 | 3.686 | 0.043 |
| WM | 3 | 1.000 | 1.766 | 5.297 | 0.064 |
