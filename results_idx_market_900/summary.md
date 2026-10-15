# Pullback scanner - backtest report (`pullback_scanner.py`)

* tickers: 878 / 898 | period: 2016-01-01 -> today
* entry: next open | stop: base_lo | exit: trailing stop 3.0*ATR14 from highest high, no target | max hold: 60 days | dedupe cooldown: 5 bars | index combo (market): stock daily signal + index pullback signal within 5 days
* baseline = every trading day of the same tickers, same period (2,291,105 days)

## 1. Forward returns vs baseline (next open -> close t+h)

| group / horizon | n | mean | median | pct_up | t_vs_base | p |
|---|---|---|---|---|---|---|
| baseline 5d | 2,286,615 | 0.004 | 0.003 | 0.538 |  |  |
| daily 5d | 9,165 | 0.002 | 0.002 | 0.528 | -2.678 | 0.007 |
| combo 5d | 2,003 | 0.003 | 0.002 | 0.526 | -0.357 | 0.721 |
| baseline 10d | 2,282,125 | 0.008 | 0.006 | 0.552 |  |  |
| daily 10d | 9,143 | 0.005 | 0.005 | 0.545 | -4.126 | 0.000 |
| combo 10d | 1,996 | 0.008 | 0.008 | 0.561 | -0.087 | 0.931 |
| baseline 20d | 2,273,145 | 0.017 | 0.012 | 0.568 |  |  |
| daily 20d | 9,107 | 0.011 | 0.012 | 0.573 | -5.796 | 0.000 |
| combo 20d | 1,982 | 0.019 | 0.019 | 0.601 | 1.169 | 0.243 |
| baseline 60d | 2,237,225 | 0.051 | 0.036 | 0.607 |  |  |
| daily 60d | 9,027 | 0.028 | 0.032 | 0.606 | -13.014 | 0.000 |
| combo 60d | 1,965 | 0.035 | 0.037 | 0.617 | -4.879 | 0.000 |

> p is a normal-approx Welch test. Baseline days overlap, so treat p as optimistic.

## 2. Trade simulation with the scanner's own levels

| group | n | trades | win_rate | avg_R | R_ci95 | profit_factor | avg_risk_pct | stopped | trailed | hit_target | gap_below_stop | total_R |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| daily | 9192 | 9023 | 0.397 | 0.186 | [0.14, 0.23] | 1.438 | 0.056 | 0.186 | 0.776 | 0 | 0.012 | 1706.854 |
| combo | 2013 | 1958 | 0.420 | 0.222 | [0.15, 0.29] | 1.546 | 0.061 | 0.157 | 0.796 | 0 | 0.017 | 440.321 |
| CONTROL: random days, same exits | 763445 | 759733 | 0.373 | 0.131 | [0.13, 0.13] | 1.294 | 0.061 | 0.236 | 0.742 | 0 | 0 | 101917.459 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the tested signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* daily vs CONTROL: avg_R diff = +0.055R, t = 2.52, p = 0.012
* combo vs CONTROL: avg_R diff = +0.091R, t = 2.31, p = 0.021

## 3. Combo signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=25 | 324 | 308 | 0.409 | 0.246 | [0.05, 0.46] | 1.514 | 0.028 |
| score=50 | 960 | 940 | 0.424 | 0.192 | [0.10, 0.29] | 1.465 | 0.019 |
| score=75 | 531 | 518 | 0.432 | 0.287 | [0.13, 0.48] | 1.799 | 0.017 |
| score=100 | 198 | 192 | 0.385 | 0.154 | [-0.04, 0.35] | 1.394 | 0.012 |
| slowing=True | 746 | 722 | 0.422 | 0.251 | [0.12, 0.41] | 1.651 | 0.015 |
| slowing=False | 1267 | 1236 | 0.419 | 0.205 | [0.12, 0.30] | 1.489 | 0.022 |
| drying=True | 446 | 436 | 0.367 | 0.166 | [0.02, 0.31] | 1.411 | 0.012 |
| drying=False | 1567 | 1522 | 0.436 | 0.238 | [0.15, 0.33] | 1.584 | 0.021 |
| uptrend=True | 1424 | 1394 | 0.433 | 0.225 | [0.14, 0.32] | 1.590 | 0.019 |
| uptrend=False | 589 | 564 | 0.388 | 0.215 | [0.07, 0.37] | 1.457 | 0.021 |

Phase lengths found by detect() (bars):

| phase | mean | min | 50% | max |
|---|---|---|---|---|
| decline_len | 16.242 | 2.000 | 14 | 41 |
| slowdown_len | 7.586 | 0 | 4.000 | 56 |
| base_len | 5.637 | 3.000 | 5.000 | 10 |
| peak_to_low | 21.662 | 0 | 20 | 40 |
| base_above_low | 0.007 | 0 | 0 | 0.044 |

## 4. Combo signals per year

| year | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| 2016 | 338 | 0.517 | 0.518 | 168.387 | 0.042 |
| 2017 | 314 | 0.447 | 0.193 | 59.783 | 0.016 |
| 2018 | 152 | 0.302 | -0.143 | -21.350 | -0.003 |
| 2019 | 151 | 0.453 | 0.352 | 52.742 | 0.024 |
| 2020 | 50 | 0.673 | 0.785 | 38.457 | 0.046 |
| 2021 | 134 | 0.466 | 0.320 | 42.600 | 0.028 |
| 2022 | 101 | 0.297 | -0.042 | -4.284 | 0.013 |
| 2023 | 237 | 0.440 | 0.547 | 127.006 | 0.028 |
| 2024 | 295 | 0.338 | -0.101 | -29.505 | -0.002 |
| 2025 | 132 | 0.438 | 0.091 | 11.802 | 0.017 |
| 2026 | 109 | 0.241 | -0.124 | -5.317 | 0.000 |

## 5. Combo signals per ticker (15 worst and 15 best by total_R)

| ticker | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| FFIV | 3 | 0 | -1.976 | -5.927 | -0.038 |
| SIGI | 5 | 0 | -1.101 | -5.506 | -0.036 |
| UHS | 5 | 0 | -1.057 | -5.285 | -0.006 |
| NDSN | 5 | 0.200 | -0.895 | -4.474 | -0.020 |
| AXTA | 6 | 0.167 | -0.732 | -4.392 | -0.041 |
| MTB | 5 | 0.200 | -0.821 | -4.105 | -0.019 |
| MSFT | 4 | 0 | -1.010 | -4.042 | -0.047 |
| OXY | 5 | 0 | -0.804 | -4.022 | -0.041 |
| BBY | 4 | 0 | -0.959 | -3.835 | -0.024 |
| USB | 6 | 0.167 | -0.633 | -3.798 | 0.009 |
| MUR | 4 | 0 | -0.933 | -3.732 | 0.006 |
| COO | 6 | 0.167 | -0.607 | -3.643 | -0.024 |
| ZBH | 4 | 0 | -0.906 | -3.625 | -0.065 |
| GNTX | 5 | 0 | -0.698 | -3.491 | -0.067 |
| IRT | 5 | 0 | -0.690 | -3.450 | -0.044 |
| LOPE | 2 | 1.000 | 3.742 | 7.484 | 0.177 |
| LECO | 8 | 0.625 | 0.975 | 7.796 | 0.054 |
| IT | 3 | 0.667 | 2.599 | 7.797 | 0.077 |
| AXON | 3 | 1.000 | 2.758 | 8.274 | 0.301 |
| GDDY | 3 | 0.667 | 2.823 | 8.469 | 0.150 |
| PM | 4 | 0.500 | 2.201 | 8.804 | 0.036 |
| HLT | 2 | 1.000 | 4.456 | 8.913 | 0.076 |
| AM | 3 | 0.333 | 3.139 | 9.417 | 0.015 |
| TTWO | 5 | 0.600 | 2.066 | 10.332 | 0.063 |
| DLTR | 5 | 0.800 | 2.179 | 10.896 | 0.096 |
| LIN | 3 | 0.667 | 3.780 | 11.340 | 0.039 |
| BKNG | 3 | 0.667 | 4.512 | 13.535 | 0.045 |
| SWKS | 1 | 1.000 | 17.990 | 17.990 | 0.146 |
| CSCO | 4 | 0.250 | 5.236 | 20.943 | 0.025 |
| R | 2 | 1.000 | 15.446 | 30.892 | 0.139 |
