# Pullback scanner - backtest report (`pullback_scanner.py`)

* tickers: 558 / 590 | period: 2016-01-01 -> today
* entry: next open | stop: base_lo | exit: trailing stop 3.0*ATR14 from highest high, no target | max hold: 60 days | dedupe cooldown: 5 bars | combo: daily signal within 15 days after a weekly signal
* baseline = every trading day of the same tickers, same period (1,426,819 days)

## 1. Forward returns vs baseline (next open -> close t+h)

| group / horizon | n | mean | median | pct_up | t_vs_base | p |
|---|---|---|---|---|---|---|
| baseline 5d | 1,423,869 | 0.003 | 0.002 | 0.517 |  |  |
| daily 5d | 4,973 | 0.001 | 0.001 | 0.506 | -2.494 | 0.013 |
| weekly 5d | 272 | 0.000 | 0.002 | 0.533 | -1.237 | 0.216 |
| BUY SIGNAL (daily+weekly) 5d | 27 | 0.001 | 0.007 | 0.630 | -0.259 | 0.796 |
| combo 5d | 47 | 0.003 | 0.007 | 0.617 | -0.074 | 0.941 |
| baseline 10d | 1,420,919 | 0.006 | 0.004 | 0.527 |  |  |
| daily 10d | 4,962 | 0.004 | 0.003 | 0.527 | -2.258 | 0.024 |
| weekly 10d | 272 | -0.001 | -0.003 | 0.474 | -2.000 | 0.046 |
| BUY SIGNAL (daily+weekly) 10d | 27 | -0.008 | 0.000 | 0.519 | -1.900 | 0.057 |
| combo 10d | 47 | -0.002 | 0.004 | 0.532 | -1.273 | 0.203 |
| baseline 20d | 1,415,019 | 0.013 | 0.008 | 0.538 |  |  |
| daily 20d | 4,953 | 0.010 | 0.008 | 0.541 | -2.524 | 0.012 |
| weekly 20d | 272 | -0.001 | -0.008 | 0.445 | -2.933 | 0.003 |
| BUY SIGNAL (daily+weekly) 20d | 27 | -0.021 | -0.021 | 0.407 | -3.129 | 0.002 |
| combo 20d | 47 | -0.012 | 0.003 | 0.511 | -2.363 | 0.018 |
| baseline 60d | 1,391,419 | 0.041 | 0.025 | 0.563 |  |  |
| daily 60d | 4,912 | 0.021 | 0.021 | 0.557 | -8.472 | 0.000 |
| weekly 60d | 271 | -0.007 | 0.003 | 0.517 | -5.599 | 0.000 |
| BUY SIGNAL (daily+weekly) 60d | 27 | -0.002 | 0.031 | 0.556 | -1.840 | 0.066 |
| combo 60d | 47 | 0.016 | 0.035 | 0.574 | -1.307 | 0.191 |

> p is a normal-approx Welch test. Baseline days overlap, so treat p as optimistic.

## 2. Trade simulation with the scanner's own levels

| group | n | trades | win_rate | avg_R | R_ci95 | profit_factor | avg_risk_pct | stopped | trailed | hit_target | gap_below_stop | total_R |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| daily | 4976 | 4915 | 0.357 | 0.074 | [0.03, 0.12] | 1.154 | 0.059 | 0.246 | 0.725 | 0 | 0.009 | 368.326 |
| weekly | 273 | 272 | 0.357 | 0.017 | [-0.12, 0.16] | 1.046 | 0.070 | 0.088 | 0.897 | 0 | 0 | 4.789 |
| BUY SIGNAL (daily+weekly) | 27 | 27 | 0.407 | 0.113 | [-0.19, 0.46] | 1.492 | 0.079 | 0.037 | 0.926 | 0 | 0 | 3.053 |
| combo | 47 | 47 | 0.404 | 0.111 | [-0.22, 0.48] | 1.321 | 0.065 | 0.149 | 0.830 | 0 | 0 | 5.236 |
| CONTROL: random days, same exits | 475467 | 473112 | 0.332 | 0.065 | [0.06, 0.07] | 1.127 | 0.065 | 0.315 | 0.668 | 0 | 0 | 32524.765 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the tested signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* daily vs CONTROL: avg_R diff = +0.009R, t = 0.38, p = 0.701
* weekly vs CONTROL: avg_R diff = -0.048R, t = -0.71, p = 0.479
* BUY SIGNAL (daily+weekly) vs CONTROL: avg_R diff = +0.048R, t = 0.29, p = 0.775
* combo vs CONTROL: avg_R diff = +0.046R, t = 0.25, p = 0.801

## 3. Combo signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=25 | 6 | 6 | 0.167 | -0.330 | [-0.65, 0.09] | 0.255 | -0.013 |
| score=50 | 24 | 24 | 0.542 | 0.460 | [-0.07, 1.14] | 2.773 | -0.006 |
| score=75 | 14 | 14 | 0.286 | -0.297 | [-0.59, 0.05] | 0.307 | -0.033 |
| score=100 | 3 | 3 | 0.333 | 0.111 | [nan, nan] | 1.233 | 0.032 |
| slowing=True | 27 | 27 | 0.444 | 0.243 | [-0.22, 0.82] | 1.772 | -0.014 |
| slowing=False | 20 | 20 | 0.350 | -0.067 | [-0.44, 0.39] | 0.829 | -0.010 |
| drying=True | 6 | 6 | 0.167 | -0.201 | [-0.87, 0.64] | 0.592 | -0.028 |
| drying=False | 41 | 41 | 0.439 | 0.157 | [-0.19, 0.60] | 1.482 | -0.010 |
| uptrend=True | 28 | 28 | 0.393 | -0.059 | [-0.39, 0.30] | 0.851 | -0.008 |
| uptrend=False | 19 | 19 | 0.421 | 0.362 | [-0.21, 1.18] | 2.303 | -0.019 |

Phase lengths found by detect() (bars):

| phase | mean | min | 50% | max |
|---|---|---|---|---|
| decline_len | 16.511 | 3.000 | 14 | 40 |
| slowdown_len | 15.957 | 0 | 13 | 47 |
| base_len | 7.255 | 3.000 | 8.000 | 10 |
| peak_to_low | 26.383 | 5.000 | 31 | 40 |
| base_above_low | 0.011 | 0 | 0.010 | 0.029 |

## 4. Combo signals per year

| year | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| 2016 | 7 | 0.571 | 0.351 | 2.458 | 0.012 |
| 2017 | 9 | 0.444 | 0.097 | 0.873 | -0.008 |
| 2018 | 7 | 0.286 | -0.344 | -2.410 | -0.023 |
| 2019 | 3 | 0.667 | -0.152 | -0.455 | -0.008 |
| 2020 | 1 | 0 | -1.000 | -1.000 | -0.194 |
| 2021 | 2 | 0.500 | 0.592 | 1.185 | -0.054 |
| 2023 | 6 | 0.167 | 0.146 | 0.879 | -0.017 |
| 2024 | 2 | 0.500 | 2.346 | 4.692 | -0.036 |
| 2025 | 8 | 0.250 | -0.384 | -3.074 | -0.009 |
| 2026 | 2 | 1.000 | 1.044 | 2.089 | 0.068 |

## 5. Combo signals per ticker (15 worst and 15 best by total_R)

| ticker | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| FLO | 2 | 0 | -1.000 | -2.000 | -0.139 |
| CNS | 2 | 0 | -0.714 | -1.429 | -0.034 |
| NIC | 1 | 0 | -1.250 | -1.250 | 0.047 |
| ABR | 1 | 0 | -1.000 | -1.000 | 0.034 |
| TFIN | 1 | 0 | -1.000 | -1.000 | -0.127 |
| SBSI | 1 | 0 | -1.000 | -1.000 | 0.014 |
| MTRN | 1 | 0 | -1.000 | -1.000 | -0.044 |
| WABC | 1 | 0 | -0.938 | -0.938 | -0.031 |
| AMSF | 1 | 0 | -0.787 | -0.787 | 0.020 |
| CPF | 1 | 0 | -0.744 | -0.744 | -0.072 |
| BKU | 1 | 0 | -0.668 | -0.668 | -0.105 |
| FIZZ | 1 | 0 | -0.640 | -0.640 | -0.060 |
| HCSG | 1 | 0 | -0.631 | -0.631 | -0.136 |
| TMP | 1 | 0 | -0.471 | -0.471 | -0.024 |
| BRC | 1 | 0 | -0.445 | -0.445 | 0.033 |
| WDFC | 1 | 1.000 | 0.132 | 0.132 | 0.049 |
| SPNT | 1 | 1.000 | 0.194 | 0.194 | 0.021 |
| AGO | 1 | 1.000 | 0.201 | 0.201 | 0.012 |
| FCPT | 1 | 1.000 | 0.333 | 0.333 | 0.050 |
| OSIS | 1 | 1.000 | 0.402 | 0.402 | 0.070 |
| REYN | 1 | 1.000 | 0.577 | 0.577 | 0.033 |
| SXT | 1 | 1.000 | 0.679 | 0.679 | 0.031 |
| MSGS | 1 | 1.000 | 1.186 | 1.186 | 0.123 |
| TR | 1 | 1.000 | 1.374 | 1.374 | -0.114 |
| WINA | 1 | 1.000 | 1.378 | 1.378 | 0.113 |
| CWT | 1 | 1.000 | 1.755 | 1.755 | 0.085 |
| LUMN | 1 | 1.000 | 1.926 | 1.926 | -0.173 |
| HSTM | 2 | 0.500 | 1.242 | 2.484 | 0.017 |
| NPK | 1 | 1.000 | 2.712 | 2.712 | 0.152 |
| TRNO | 1 | 1.000 | 5.692 | 5.692 | 0.055 |
