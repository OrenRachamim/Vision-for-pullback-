# Pullback scanner - backtest report (`pullback_scanner.py`)

* tickers: 815 / 860 | period: 2016-01-01 -> 2021-12-31
* entry: next open | stop: base_lo | target: 2.0R | max hold: 10 days | dedupe cooldown: 5 bars | combo: daily signal within 15 days after a weekly signal
* baseline = every trading day of the same tickers, same period (1,230,726 days)

## 1. Forward returns vs baseline (next open -> close t+h)

| group / horizon | n | mean | median | pct_up | t_vs_base | p |
|---|---|---|---|---|---|---|
| baseline 5d | 1,230,726 | 0.005 | 0.004 | 0.551 |  |  |
| daily 5d | 5,379 | 0.002 | 0.002 | 0.526 | -3.899 | 0.000 |
| weekly 5d | 397 | -0.000 | -0.002 | 0.474 | -3.187 | 0.001 |
| BUY SIGNAL (daily+weekly) 5d | 41 | -0.004 | -0.004 | 0.415 | -2.261 | 0.024 |
| combo 5d | 36 | -0.002 | -0.002 | 0.444 | -1.434 | 0.152 |
| baseline 10d | 1,230,726 | 0.011 | 0.008 | 0.571 |  |  |
| daily 10d | 5,379 | 0.006 | 0.006 | 0.554 | -4.504 | 0.000 |
| weekly 10d | 397 | 0.003 | 0.002 | 0.519 | -3.375 | 0.001 |
| BUY SIGNAL (daily+weekly) 10d | 41 | -0.001 | -0.002 | 0.415 | -2.129 | 0.033 |
| combo 10d | 36 | -0.002 | 0.003 | 0.500 | -1.520 | 0.129 |
| baseline 20d | 1,230,726 | 0.022 | 0.016 | 0.596 |  |  |
| daily 20d | 5,379 | 0.012 | 0.013 | 0.592 | -6.718 | 0.000 |
| weekly 20d | 397 | 0.007 | 0.015 | 0.610 | -4.069 | 0.000 |
| BUY SIGNAL (daily+weekly) 20d | 41 | 0.014 | 0.016 | 0.610 | -0.827 | 0.408 |
| combo 20d | 36 | 0.002 | 0.016 | 0.611 | -1.270 | 0.204 |
| baseline 60d | 1,230,726 | 0.062 | 0.044 | 0.641 |  |  |
| daily 60d | 5,379 | 0.024 | 0.033 | 0.608 | -14.637 | 0.000 |
| weekly 60d | 397 | -0.002 | 0.027 | 0.592 | -8.304 | 0.000 |
| BUY SIGNAL (daily+weekly) 60d | 41 | -0.018 | 0.057 | 0.659 | -2.737 | 0.006 |
| combo 60d | 36 | -0.000 | 0.037 | 0.639 | -2.288 | 0.022 |

> p is a normal-approx Welch test. Baseline days overlap, so treat p as optimistic.

## 2. Trade simulation with the scanner's own levels

| group | n | trades | win_rate | avg_R | R_ci95 | profit_factor | avg_risk_pct | stopped | hit_target | gap_below_stop | total_R |
|---|---|---|---|---|---|---|---|---|---|---|---|
| daily | 5379 | 5308 | 0.517 | 0.083 | [0.06, 0.11] | 1.242 | 0.054 | 0.252 | 0.077 | 0.013 | 442.509 |
| weekly | 397 | 397 | 0.509 | 0.039 | [-0.03, 0.10] | 1.169 | 0.069 | 0.126 | 0.013 | 0 | 15.519 |
| BUY SIGNAL (daily+weekly) | 41 | 41 | 0.415 | -0.014 | [-0.20, 0.19] | 0.943 | 0.071 | 0.146 | 0.024 | 0 | -0.585 |
| combo | 36 | 36 | 0.500 | 0.062 | [-0.14, 0.26] | 1.299 | 0.078 | 0.111 | 0 | 0 | 2.224 |
| CONTROL: random days, same exits | 281466 | 281466 | 0.541 | 0.067 | [0.06, 0.07] | 1.257 | 0.079 | 0.171 | 0.045 | 0 | 18840.674 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the tested signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* daily vs CONTROL: avg_R diff = +0.016R, t = 1.23, p = 0.217
* weekly vs CONTROL: avg_R diff = -0.028R, t = -0.85, p = 0.397
* BUY SIGNAL (daily+weekly) vs CONTROL: avg_R diff = -0.081R, t = -0.80, p = 0.426
* combo vs CONTROL: avg_R diff = -0.005R, t = -0.05, p = 0.959

> require-uptrend: buy only when price > SMA200; CONTROL also samples only days with price > SMA200.

## 3. Combo signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=50 | 8 | 8 | 0.500 | 0.055 | [-0.48, 0.59] | 1.176 | -0.047 |
| score=75 | 21 | 21 | 0.524 | 0.045 | [-0.19, 0.27] | 1.217 | 0.023 |
| score=100 | 7 | 7 | 0.429 | 0.121 | [-0.13, 0.41] | 2.379 | -0.006 |
| slowing=True | 28 | 28 | 0.500 | 0.064 | [-0.14, 0.27] | 1.360 | 0.015 |
| slowing=False | 8 | 8 | 0.500 | 0.055 | [-0.48, 0.59] | 1.176 | -0.047 |
| drying=True | 7 | 7 | 0.429 | 0.121 | [-0.13, 0.41] | 2.379 | -0.006 |
| drying=False | 29 | 29 | 0.517 | 0.048 | [-0.19, 0.27] | 1.202 | 0.003 |
| uptrend=True | 36 | 36 | 0.500 | 0.062 | [-0.14, 0.26] | 1.299 | 0.002 |

Phase lengths found by detect() (bars):

| phase | mean | min | 50% | max |
|---|---|---|---|---|
| decline_len | 19.194 | 5.000 | 18.500 | 36 |
| slowdown_len | 14.556 | 0 | 12 | 40 |
| base_len | 8.083 | 3.000 | 10 | 10 |
| peak_to_low | 28.056 | 7.000 | 30 | 40 |
| base_above_low | 0.011 | 0 | 0.012 | 0.030 |

## 4. Combo signals per year

| year | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| 2016 | 10 | 0.500 | 0.205 | 2.054 | 0.004 |
| 2017 | 9 | 0.333 | -0.112 | -1.010 | -0.000 |
| 2018 | 3 | 0.667 | 0.085 | 0.256 | 0.020 |
| 2019 | 5 | 0.400 | -0.124 | -0.618 | 0.030 |
| 2020 | 4 | 0.500 | -0.249 | -0.998 | -0.104 |
| 2021 | 5 | 0.800 | 0.508 | 2.540 | 0.045 |

## 5. Combo signals per ticker

| ticker | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| SGI | 1 | 0 | -1.220 | -1.220 | -0.465 |
| WTS | 1 | 0 | -1.000 | -1.000 | -0.007 |
| MMS | 1 | 0 | -1.000 | -1.000 | -0.051 |
| HXL | 1 | 0 | -1.000 | -1.000 | -0.081 |
| NWE | 1 | 0 | -0.691 | -0.691 | 0.039 |
| MKC | 1 | 0 | -0.407 | -0.407 | -0.027 |
| AZO | 1 | 0 | -0.405 | -0.405 | -0.038 |
| FE | 1 | 0 | -0.309 | -0.309 | 0.017 |
| DE | 1 | 0 | -0.280 | -0.280 | -0.055 |
| FIX | 1 | 0 | -0.256 | -0.256 | -0.090 |
| TYL | 1 | 0 | -0.226 | -0.226 | -0.029 |
| HCA | 1 | 0 | -0.178 | -0.178 | -0.105 |
| EXPO | 1 | 0 | -0.143 | -0.143 | -0.023 |
| COR | 1 | 0 | -0.137 | -0.137 | 0.050 |
| ILMN | 1 | 0 | -0.107 | -0.107 | 0.014 |
| ABT | 1 | 0 | -0.066 | -0.066 | 0.047 |
| GWRE | 1 | 0 | -0.011 | -0.011 | -0.031 |
| D | 1 | 0 | -0.009 | -0.009 | -0.001 |
| AVT | 1 | 1.000 | 0.071 | 0.071 | 0.031 |
| IDXX | 1 | 1.000 | 0.188 | 0.188 | 0.092 |
| RTX | 1 | 1.000 | 0.210 | 0.210 | 0.024 |
| CPT | 1 | 1.000 | 0.227 | 0.227 | 0.076 |
| WHR | 1 | 1.000 | 0.233 | 0.233 | 0.002 |
| DIS | 1 | 1.000 | 0.239 | 0.239 | 0.075 |
| NWS | 1 | 1.000 | 0.333 | 0.333 | 0.043 |
| BAX | 1 | 1.000 | 0.362 | 0.362 | 0.003 |
| BG | 1 | 1.000 | 0.373 | 0.373 | -0.023 |
| GGG | 1 | 1.000 | 0.396 | 0.396 | 0.022 |
| DVA | 1 | 1.000 | 0.494 | 0.494 | 0.013 |
| POST | 1 | 1.000 | 0.686 | 0.686 | 0.027 |
| PAYX | 1 | 1.000 | 0.733 | 0.733 | 0.079 |
| ADP | 1 | 1.000 | 0.735 | 0.735 | 0.064 |
| AKAM | 1 | 1.000 | 0.896 | 0.896 | 0.102 |
| TXNM | 1 | 1.000 | 0.995 | 0.995 | 0.055 |
| WM | 1 | 1.000 | 1.232 | 1.232 | 0.124 |
| G | 1 | 1.000 | 1.264 | 1.264 | 0.082 |
