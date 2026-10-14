# Pullback scanner - backtest report (`pullback_scanner.py`)

* tickers: 813 / 860 | period: 2016-01-01 -> 2021-12-31
* entry: next open | stop: base_lo | target: 2.0R | max hold: 10 days | dedupe cooldown: 5 bars | combo: daily signal within 15 days after a weekly signal
* baseline = every trading day of the same tickers, same period (1,230,726 days)

## 1. Forward returns vs baseline (next open -> close t+h)

| group / horizon | n | mean | median | pct_up | t_vs_base | p |
|---|---|---|---|---|---|---|
| baseline 5d | 1,230,726 | 0.005 | 0.004 | 0.551 |  |  |
| daily 5d | 5,128 | 0.002 | 0.003 | 0.531 | -3.360 | 0.001 |
| weekly 5d | 371 | 0.002 | 0.001 | 0.509 | -1.991 | 0.046 |
| BUY SIGNAL (daily+weekly) 5d | 38 | 0.001 | 0.003 | 0.526 | -0.884 | 0.376 |
| combo 5d | 33 | 0.003 | 0.003 | 0.515 | -0.337 | 0.736 |
| baseline 10d | 1,230,726 | 0.011 | 0.008 | 0.571 |  |  |
| daily 10d | 5,128 | 0.006 | 0.007 | 0.561 | -4.231 | 0.000 |
| weekly 10d | 371 | 0.004 | 0.004 | 0.536 | -2.819 | 0.005 |
| BUY SIGNAL (daily+weekly) 10d | 38 | 0.001 | -0.001 | 0.447 | -1.680 | 0.093 |
| combo 10d | 33 | 0.000 | 0.011 | 0.515 | -1.116 | 0.265 |
| baseline 20d | 1,230,726 | 0.022 | 0.016 | 0.596 |  |  |
| daily 20d | 5,128 | 0.011 | 0.013 | 0.588 | -6.739 | 0.000 |
| weekly 20d | 371 | 0.008 | 0.014 | 0.598 | -3.988 | 0.000 |
| BUY SIGNAL (daily+weekly) 20d | 38 | 0.006 | 0.015 | 0.553 | -1.630 | 0.103 |
| combo 20d | 33 | -0.004 | 0.014 | 0.606 | -1.462 | 0.144 |
| baseline 60d | 1,230,726 | 0.062 | 0.044 | 0.641 |  |  |
| daily 60d | 5,128 | 0.026 | 0.035 | 0.614 | -13.730 | 0.000 |
| weekly 60d | 371 | 0.004 | 0.029 | 0.604 | -7.442 | 0.000 |
| BUY SIGNAL (daily+weekly) 60d | 38 | -0.014 | 0.046 | 0.658 | -2.552 | 0.011 |
| combo 60d | 33 | 0.007 | 0.041 | 0.636 | -1.905 | 0.057 |

> p is a normal-approx Welch test. Baseline days overlap, so treat p as optimistic.

## 2. Trade simulation with the scanner's own levels

| group | n | trades | win_rate | avg_R | R_ci95 | profit_factor | avg_risk_pct | stopped | hit_target | gap_below_stop | total_R |
|---|---|---|---|---|---|---|---|---|---|---|---|
| daily | 5128 | 5056 | 0.525 | 0.088 | [0.06, 0.11] | 1.256 | 0.055 | 0.250 | 0.075 | 0.014 | 442.593 |
| weekly | 371 | 371 | 0.528 | 0.060 | [-0.00, 0.13] | 1.275 | 0.071 | 0.121 | 0.013 | 0 | 22.320 |
| BUY SIGNAL (daily+weekly) | 38 | 38 | 0.447 | -0.019 | [-0.21, 0.17] | 0.926 | 0.071 | 0.158 | 0 | 0 | -0.717 |
| combo | 33 | 33 | 0.515 | 0.078 | [-0.15, 0.30] | 1.363 | 0.077 | 0.152 | 0 | 0 | 2.573 |
| CONTROL: random days, same exits | 281466 | 281466 | 0.540 | 0.067 | [0.06, 0.07] | 1.253 | 0.077 | 0.173 | 0.045 | 0 | 18758.819 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the tested signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* daily vs CONTROL: avg_R diff = +0.021R, t = 1.54, p = 0.124
* weekly vs CONTROL: avg_R diff = -0.006R, t = -0.19, p = 0.849
* BUY SIGNAL (daily+weekly) vs CONTROL: avg_R diff = -0.086R, t = -0.86, p = 0.390
* combo vs CONTROL: avg_R diff = +0.011R, t = 0.10, p = 0.920

> require-uptrend: buy only when price > SMA200; CONTROL also samples only days with price > SMA200.

## 3. Combo signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=50 | 8 | 8 | 0.625 | 0.203 | [-0.38, 0.75] | 1.729 | -0.024 |
| score=75 | 22 | 22 | 0.545 | 0.064 | [-0.18, 0.30] | 1.323 | 0.012 |
| score=100 | 3 | 3 | 0 | -0.157 | [nan, nan] | 0 | -0.063 |
| slowing=True | 25 | 25 | 0.480 | 0.038 | [-0.18, 0.26] | 1.195 | 0.003 |
| slowing=False | 8 | 8 | 0.625 | 0.203 | [-0.38, 0.75] | 1.729 | -0.024 |
| drying=True | 3 | 3 | 0 | -0.157 | [nan, nan] | 0 | -0.063 |
| drying=False | 30 | 30 | 0.567 | 0.101 | [-0.13, 0.33] | 1.460 | 0.002 |
| uptrend=True | 33 | 33 | 0.515 | 0.078 | [-0.15, 0.30] | 1.363 | -0.004 |

Phase lengths found by detect() (bars):

| phase | mean | min | 50% | max |
|---|---|---|---|---|
| decline_len | 19.364 | 5.000 | 19 | 36 |
| slowdown_len | 13.939 | 0 | 11 | 40 |
| base_len | 8.394 | 3.000 | 10 | 10 |
| peak_to_low | 27.788 | 7.000 | 30 | 40 |
| base_above_low | 0.011 | 0 | 0.013 | 0.030 |

## 4. Combo signals per year

| year | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| 2016 | 9 | 0.556 | 0.257 | 2.309 | 0.014 |
| 2017 | 9 | 0.444 | 0.036 | 0.328 | 0.013 |
| 2018 | 3 | 0.667 | 0.135 | 0.405 | 0.016 |
| 2019 | 2 | 0 | -0.506 | -1.011 | -0.041 |
| 2020 | 4 | 0.500 | -0.249 | -0.998 | -0.104 |
| 2021 | 6 | 0.667 | 0.257 | 1.540 | 0.014 |

## 5. Combo signals per ticker

| ticker | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| SGI | 1 | 0 | -1.220 | -1.220 | -0.465 |
| WTS | 1 | 0 | -1.000 | -1.000 | -0.007 |
| MMS | 1 | 0 | -1.000 | -1.000 | -0.051 |
| HXL | 1 | 0 | -1.000 | -1.000 | -0.081 |
| GPN | 1 | 0 | -1.000 | -1.000 | -0.143 |
| AZO | 1 | 0 | -0.405 | -0.405 | -0.038 |
| FE | 1 | 0 | -0.309 | -0.309 | 0.017 |
| DE | 1 | 0 | -0.280 | -0.280 | -0.055 |
| TYL | 1 | 0 | -0.226 | -0.226 | -0.029 |
| HCA | 1 | 0 | -0.178 | -0.178 | -0.105 |
| EXPO | 1 | 0 | -0.143 | -0.143 | -0.023 |
| COR | 1 | 0 | -0.137 | -0.137 | 0.050 |
| ILMN | 1 | 0 | -0.107 | -0.107 | 0.014 |
| ABT | 1 | 0 | -0.066 | -0.066 | 0.047 |
| GWRE | 1 | 0 | -0.011 | -0.011 | -0.031 |
| D | 1 | 0 | -0.009 | -0.009 | -0.001 |
| RTX | 1 | 1.000 | 0.210 | 0.210 | 0.024 |
| HON | 1 | 1.000 | 0.220 | 0.220 | 0.018 |
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
| LEN | 1 | 1.000 | 0.931 | 0.931 | 0.094 |
| TXNM | 1 | 1.000 | 0.995 | 0.995 | 0.055 |
| WM | 1 | 1.000 | 1.232 | 1.232 | 0.124 |
| G | 1 | 1.000 | 1.264 | 1.264 | 0.082 |
