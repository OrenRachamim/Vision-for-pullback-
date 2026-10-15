# Pullback scanner - backtest report (`pullback_scanner.py`)

* tickers: 878 / 898 | period: 2016-01-01 -> today
* entry: next open | stop: base_lo | target: 2.0R | max hold: 10 days | dedupe cooldown: 5 bars | index combo (market): stock daily signal + index pullback signal within 5 days
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
| daily | 9192 | 9035 | 0.508 | 0.071 | [0.05, 0.09] | 1.199 | 0.056 | 0.263 | 0 | 0.082 | 0.012 | 656.362 |
| combo | 2013 | 1964 | 0.526 | 0.082 | [0.04, 0.12] | 1.244 | 0.061 | 0.235 | 0 | 0.066 | 0.017 | 162.820 |
| CONTROL: random days, same exits | 763445 | 761358 | 0.497 | 0.066 | [0.06, 0.07] | 1.177 | 0.061 | 0.294 | 0 | 0.102 | 0 | 50939.726 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the tested signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* daily vs CONTROL: avg_R diff = +0.005R, t = 0.49, p = 0.621
* combo vs CONTROL: avg_R diff = +0.016R, t = 0.76, p = 0.449

## 3. Combo signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=25 | 324 | 311 | 0.527 | 0.108 | [-0.01, 0.24] | 1.273 | 0.028 |
| score=50 | 960 | 942 | 0.513 | 0.039 | [-0.02, 0.10] | 1.111 | 0.019 |
| score=75 | 531 | 519 | 0.557 | 0.148 | [0.07, 0.23] | 1.511 | 0.017 |
| score=100 | 198 | 192 | 0.510 | 0.077 | [-0.05, 0.20] | 1.252 | 0.012 |
| slowing=True | 746 | 725 | 0.546 | 0.117 | [0.05, 0.18] | 1.382 | 0.015 |
| slowing=False | 1267 | 1239 | 0.515 | 0.062 | [0.01, 0.12] | 1.174 | 0.022 |
| drying=True | 446 | 436 | 0.489 | 0.061 | [-0.03, 0.15] | 1.186 | 0.012 |
| drying=False | 1567 | 1528 | 0.537 | 0.089 | [0.04, 0.14] | 1.260 | 0.021 |
| uptrend=True | 1424 | 1395 | 0.535 | 0.088 | [0.04, 0.13] | 1.278 | 0.019 |
| uptrend=False | 589 | 569 | 0.506 | 0.068 | [-0.02, 0.16] | 1.175 | 0.021 |

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
| 2016 | 338 | 0.652 | 0.266 | 86.367 | 0.042 |
| 2017 | 314 | 0.540 | 0.128 | 39.676 | 0.016 |
| 2018 | 152 | 0.356 | -0.173 | -25.813 | -0.003 |
| 2019 | 151 | 0.593 | 0.218 | 32.658 | 0.024 |
| 2020 | 50 | 0.673 | 0.320 | 15.685 | 0.046 |
| 2021 | 134 | 0.564 | 0.134 | 17.836 | 0.028 |
| 2022 | 101 | 0.436 | -0.136 | -13.732 | 0.013 |
| 2023 | 237 | 0.522 | 0.101 | 23.364 | 0.028 |
| 2024 | 295 | 0.447 | -0.052 | -15.253 | -0.002 |
| 2025 | 132 | 0.508 | 0.039 | 5.121 | 0.017 |
| 2026 | 109 | 0.462 | -0.042 | -3.089 | 0.000 |

## 5. Combo signals per ticker (15 worst and 15 best by total_R)

| ticker | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| FFIV | 3 | 0 | -2.004 | -6.011 | -0.038 |
| SIGI | 5 | 0 | -1.101 | -5.506 | -0.036 |
| UHS | 5 | 0 | -0.941 | -4.705 | -0.006 |
| BBY | 4 | 0 | -1.000 | -4.000 | -0.024 |
| CLX | 4 | 0 | -1.000 | -4.000 | -0.045 |
| DOV | 5 | 0.200 | -0.754 | -3.772 | -0.028 |
| MSFT | 4 | 0 | -0.881 | -3.523 | -0.047 |
| MTB | 5 | 0.400 | -0.696 | -3.478 | -0.019 |
| OXY | 5 | 0.200 | -0.625 | -3.126 | -0.041 |
| GWW | 6 | 0.333 | -0.513 | -3.076 | 0.001 |
| AA | 3 | 0 | -1.007 | -3.020 | -0.057 |
| UTHR | 3 | 0 | -1.000 | -3.000 | -0.006 |
| GNTX | 5 | 0.400 | -0.595 | -2.973 | -0.067 |
| JNJ | 4 | 0.250 | -0.739 | -2.956 | -0.008 |
| IRT | 5 | 0.200 | -0.588 | -2.940 | -0.044 |
| WTS | 4 | 0.750 | 0.950 | 3.800 | 0.027 |
| MLI | 5 | 0.800 | 0.767 | 3.834 | 0.072 |
| ASH | 5 | 1.000 | 0.823 | 3.852 | 0.022 |
| AWK | 4 | 1.000 | 0.968 | 3.873 | 0.061 |
| KBH | 5 | 0.800 | 0.789 | 3.944 | 0.094 |
| JKHY | 4 | 1.000 | 0.994 | 3.975 | 0.058 |
| MOS | 2 | 1.000 | 2.000 | 4.000 | -0.008 |
| NNN | 2 | 1.000 | 2.000 | 4.000 | 0.123 |
| AXON | 3 | 1.000 | 1.467 | 4.401 | 0.301 |
| ROK | 4 | 1.000 | 1.545 | 4.634 | 0.074 |
| VOYA | 3 | 1.000 | 1.599 | 4.798 | 0.090 |
| EVR | 4 | 0.750 | 1.297 | 5.189 | 0.115 |
| COST | 5 | 1.000 | 1.077 | 5.384 | 0.074 |
| PTC | 2 | 1.000 | 3.026 | 6.053 | 0.113 |
| EHC | 3 | 1.000 | 2.102 | 6.305 | 0.034 |
