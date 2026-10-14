# Pullback scanner - backtest report (`pullback_scanner.py`)

* tickers: 878 / 898 | period: 2016-01-01 -> today
* entry: next open | stop: base_lo | exit: trailing stop 3.0*ATR14 from highest high, no target | max hold: 60 days | dedupe cooldown: 5 bars | combo: daily signal within 15 days after a weekly signal
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
| daily | 9192 | 9023 | 0.397 | 0.186 | [0.14, 0.23] | 1.438 | 0.056 | 0.186 | 0.776 | 0 | 0.012 | 1706.854 |
| weekly | 696 | 693 | 0.418 | 0.162 | [0.07, 0.25] | 1.511 | 0.069 | 0.056 | 0.904 | 0 | 0 | 114.140 |
| BUY SIGNAL (daily+weekly) | 61 | 60 | 0.533 | 0.195 | [-0.02, 0.41] | 1.777 | 0.070 | 0.049 | 0.902 | 0 | 0 | 12.502 |
| combo | 94 | 93 | 0.516 | 0.277 | [0.05, 0.54] | 2.037 | 0.067 | 0.064 | 0.883 | 0 | 0 | 26.582 |
| CONTROL: random days, same exits | 763445 | 759576 | 0.384 | 0.127 | [0.12, 0.13] | 1.308 | 0.067 | 0.194 | 0.783 | 0 | 0 | 98524.733 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the tested signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* daily vs CONTROL: avg_R diff = +0.060R, t = 2.72, p = 0.007
* weekly vs CONTROL: avg_R diff = +0.036R, t = 0.79, p = 0.430
* BUY SIGNAL (daily+weekly) vs CONTROL: avg_R diff = +0.069R, t = 0.61, p = 0.541
* combo vs CONTROL: avg_R diff = +0.151R, t = 1.18, p = 0.237

## 3. Combo signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=25 | 6 | 6 | 0.667 | -0.021 | [-0.48, 0.40] | 0.917 | 0.003 |
| score=50 | 44 | 43 | 0.512 | 0.178 | [-0.11, 0.47] | 1.579 | 0.007 |
| score=75 | 39 | 39 | 0.513 | 0.442 | [0.01, 1.00] | 2.935 | 0.017 |
| score=100 | 5 | 5 | 0.400 | 0.204 | [-0.43, 1.18] | 1.828 | -0.031 |
| slowing=True | 69 | 68 | 0.485 | 0.305 | [0.01, 0.62] | 2.121 | 0.011 |
| slowing=False | 25 | 25 | 0.600 | 0.203 | [-0.11, 0.55] | 1.795 | 0.002 |
| drying=True | 10 | 10 | 0.400 | 0.087 | [-0.46, 0.75] | 1.252 | -0.008 |
| drying=False | 84 | 83 | 0.530 | 0.300 | [0.05, 0.59] | 2.163 | 0.011 |
| uptrend=True | 58 | 58 | 0.534 | 0.407 | [0.09, 0.77] | 2.840 | 0.008 |
| uptrend=False | 36 | 35 | 0.486 | 0.062 | [-0.23, 0.38] | 1.181 | 0.010 |

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
| 2016 | 13 | 0.615 | 0.334 | 4.342 | 0.024 |
| 2017 | 18 | 0.444 | 0.501 | 9.017 | 0.010 |
| 2018 | 6 | 0.167 | -0.274 | -1.641 | 0.002 |
| 2019 | 4 | 0.250 | -0.435 | -1.739 | -0.015 |
| 2020 | 7 | 0.429 | 0.048 | 0.335 | -0.066 |
| 2021 | 9 | 0.444 | 0.258 | 2.323 | 0.011 |
| 2023 | 11 | 0.636 | 0.606 | 6.669 | 0.022 |
| 2024 | 7 | 0.714 | 0.382 | 2.675 | 0.016 |
| 2025 | 10 | 0.700 | 0.221 | 2.214 | 0.015 |
| 2026 | 9 | 0.500 | 0.201 | 2.387 | 0.029 |

## 5. Combo signals per ticker (15 worst and 15 best by total_R)

| ticker | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| XOM | 1 | 0 | -1.000 | -1.000 | -0.019 |
| HII | 1 | 0 | -1.000 | -1.000 | -0.096 |
| SYK | 1 | 0 | -1.000 | -1.000 | 0.052 |
| XYL | 1 | 0 | -1.000 | -1.000 | -0.113 |
| VIAV | 1 | 0 | -1.000 | -1.000 | 0.061 |
| PPG | 1 | 0 | -1.000 | -1.000 | -0.007 |
| GPN | 1 | 0 | -0.998 | -0.998 | -0.143 |
| BEN | 1 | 0 | -0.967 | -0.967 | -0.163 |
| ZTS | 1 | 0 | -0.887 | -0.887 | -0.016 |
| PRU | 1 | 0 | -0.850 | -0.850 | -0.050 |
| MMS | 1 | 0 | -0.841 | -0.841 | -0.051 |
| BKH | 1 | 0 | -0.819 | -0.819 | -0.092 |
| HXL | 1 | 0 | -0.739 | -0.739 | -0.081 |
| SUI | 1 | 0 | -0.729 | -0.729 | 0.012 |
| MIDD | 1 | 0 | -0.693 | -0.693 | -0.009 |
| LEN | 1 | 1.000 | 0.987 | 0.987 | 0.094 |
| ROST | 2 | 1.000 | 0.509 | 1.018 | 0.044 |
| NFG | 1 | 1.000 | 1.282 | 1.282 | 0.050 |
| LIN | 1 | 1.000 | 1.297 | 1.297 | 0.061 |
| PAYX | 1 | 1.000 | 1.390 | 1.390 | 0.079 |
| DTE | 1 | 1.000 | 1.616 | 1.616 | 0.072 |
| ROL | 1 | 1.000 | 1.688 | 1.688 | 0.125 |
| FTV | 1 | 1.000 | 1.926 | 1.926 | 0.076 |
| DGX | 1 | 1.000 | 1.936 | 1.936 | 0.083 |
| APH | 1 | 1.000 | 2.046 | 2.046 | 0.067 |
| DIS | 1 | 1.000 | 2.165 | 2.165 | 0.075 |
| EXC | 2 | 1.000 | 1.164 | 2.328 | 0.068 |
| ATR | 1 | 1.000 | 2.433 | 2.433 | 0.020 |
| WM | 3 | 0.667 | 2.157 | 6.471 | 0.064 |
| NWS | 1 | 1.000 | 7.556 | 7.556 | 0.043 |
