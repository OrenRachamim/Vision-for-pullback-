# Pullback scanner - backtest report (`pullback_scanner.py`)

* tickers: 558 / 590 | period: 2016-01-01 -> today
* entry: next open | stop: base_lo | exit: trailing stop 3.0*ATR14 from highest high, no target | max hold: 60 days | dedupe cooldown: 5 bars | index combo (market): stock daily signal + index pullback signal within 5 days
* baseline = every trading day of the same tickers, same period (1,426,819 days)

## 1. Forward returns vs baseline (next open -> close t+h)

| group / horizon | n | mean | median | pct_up | t_vs_base | p |
|---|---|---|---|---|---|---|
| baseline 5d | 1,423,869 | 0.003 | 0.002 | 0.517 |  |  |
| daily 5d | 4,973 | 0.001 | 0.001 | 0.506 | -2.494 | 0.013 |
| combo 5d | 1,087 | 0.003 | -0.000 | 0.499 | -0.091 | 0.928 |
| baseline 10d | 1,420,919 | 0.006 | 0.004 | 0.527 |  |  |
| daily 10d | 4,962 | 0.004 | 0.003 | 0.527 | -2.258 | 0.024 |
| combo 10d | 1,081 | 0.010 | 0.006 | 0.547 | 2.041 | 0.041 |
| baseline 20d | 1,415,019 | 0.013 | 0.008 | 0.538 |  |  |
| daily 20d | 4,953 | 0.010 | 0.008 | 0.541 | -2.524 | 0.012 |
| combo 20d | 1,081 | 0.015 | 0.007 | 0.537 | 0.535 | 0.592 |
| baseline 60d | 1,391,419 | 0.041 | 0.025 | 0.563 |  |  |
| daily 60d | 4,912 | 0.021 | 0.021 | 0.557 | -8.472 | 0.000 |
| combo 60d | 1,064 | 0.024 | 0.028 | 0.583 | -3.398 | 0.001 |

> p is a normal-approx Welch test. Baseline days overlap, so treat p as optimistic.

## 2. Trade simulation with the scanner's own levels

| group | n | trades | win_rate | avg_R | R_ci95 | profit_factor | avg_risk_pct | stopped | trailed | hit_target | gap_below_stop | total_R |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| daily | 4976 | 4915 | 0.357 | 0.074 | [0.03, 0.12] | 1.154 | 0.059 | 0.246 | 0.725 | 0 | 0.009 | 368.326 |
| combo | 1089 | 1072 | 0.384 | 0.154 | [0.05, 0.27] | 1.349 | 0.062 | 0.210 | 0.752 | 0 | 0.008 | 164.799 |
| CONTROL: random days, same exits | 475467 | 473091 | 0.330 | 0.068 | [0.06, 0.07] | 1.130 | 0.062 | 0.328 | 0.655 | 0 | 0 | 34111.513 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the tested signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* daily vs CONTROL: avg_R diff = +0.006R, t = 0.25, p = 0.802
* combo vs CONTROL: avg_R diff = +0.086R, t = 1.52, p = 0.128

## 3. Combo signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=25 | 167 | 166 | 0.410 | 0.203 | [-0.08, 0.52] | 1.415 | 0.025 |
| score=50 | 447 | 437 | 0.412 | 0.264 | [0.08, 0.48] | 1.648 | 0.017 |
| score=75 | 355 | 351 | 0.362 | 0.044 | [-0.10, 0.21] | 1.097 | 0.011 |
| score=100 | 120 | 118 | 0.314 | 0.003 | [-0.24, 0.29] | 1.006 | 0.004 |
| slowing=True | 487 | 478 | 0.345 | 0.060 | [-0.11, 0.25] | 1.130 | 0.007 |
| slowing=False | 602 | 594 | 0.416 | 0.230 | [0.09, 0.37] | 1.539 | 0.021 |
| drying=True | 313 | 309 | 0.359 | 0.107 | [-0.06, 0.30] | 1.240 | 0.012 |
| drying=False | 776 | 763 | 0.394 | 0.173 | [0.04, 0.32] | 1.394 | 0.016 |
| uptrend=True | 717 | 706 | 0.381 | 0.121 | [0.01, 0.23] | 1.284 | 0.013 |
| uptrend=False | 372 | 366 | 0.391 | 0.217 | [-0.00, 0.47] | 1.463 | 0.018 |

Phase lengths found by detect() (bars):

| phase | mean | min | 50% | max |
|---|---|---|---|---|
| decline_len | 15.162 | 2.000 | 13 | 41 |
| slowdown_len | 9.417 | 0 | 6.000 | 57 |
| base_len | 5.560 | 3.000 | 5.000 | 10 |
| peak_to_low | 22.076 | 0 | 21 | 40 |
| base_above_low | 0.008 | 0 | 0 | 0.071 |

## 4. Combo signals per year

| year | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| 2016 | 133 | 0.591 | 0.954 | 125.969 | 0.076 |
| 2017 | 214 | 0.385 | 0.150 | 32.017 | 0.004 |
| 2018 | 88 | 0.341 | -0.190 | -16.720 | -0.022 |
| 2019 | 96 | 0.396 | 0.183 | 17.545 | 0.014 |
| 2020 | 53 | 0.283 | 0.436 | 23.100 | 0.013 |
| 2021 | 37 | 0.297 | -0.272 | -10.069 | -0.002 |
| 2022 | 54 | 0.333 | -0.065 | -3.485 | 0.062 |
| 2023 | 151 | 0.309 | -0.118 | -17.642 | -0.002 |
| 2024 | 176 | 0.351 | 0.009 | 1.635 | 0.002 |
| 2025 | 18 | 0.500 | -0.129 | -2.317 | 0.018 |
| 2026 | 69 | 0.414 | 0.258 | 14.764 | 0.020 |

## 5. Combo signals per ticker (15 worst and 15 best by total_R)

| ticker | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| LRN | 2 | 0 | -2.736 | -5.472 | -0.098 |
| FUL | 7 | 0.143 | -0.705 | -4.932 | -0.070 |
| VSH | 4 | 0 | -0.955 | -3.821 | -0.068 |
| PLAB | 1 | 0 | -3.818 | -3.818 | -0.063 |
| MDU | 8 | 0.286 | -0.543 | -3.802 | 0.024 |
| AKR | 7 | 0.143 | -0.540 | -3.777 | -0.011 |
| JOE | 6 | 0.167 | -0.615 | -3.689 | -0.040 |
| HSTM | 4 | 0 | -0.916 | -3.663 | -0.012 |
| HASI | 4 | 0 | -0.869 | -3.478 | 0.040 |
| AIN | 6 | 0 | -0.549 | -3.296 | -0.029 |
| CACC | 2 | 0 | -1.642 | -3.284 | 0.020 |
| DMC | 5 | 0.200 | -0.612 | -3.058 | -0.033 |
| PFS | 4 | 0 | -0.762 | -3.047 | -0.016 |
| UCB | 3 | 0 | -1.000 | -3.000 | -0.077 |
| TR | 7 | 0.286 | -0.419 | -2.936 | 0.009 |
| RUSHA | 3 | 1.000 | 2.073 | 6.220 | 0.087 |
| KMPR | 6 | 0.500 | 1.049 | 6.296 | 0.029 |
| SCL | 4 | 1.000 | 1.637 | 6.549 | -0.007 |
| NXRT | 4 | 0.500 | 1.651 | 6.604 | 0.027 |
| NIC | 5 | 0.600 | 1.330 | 6.650 | 0.052 |
| KOP | 3 | 0.333 | 2.364 | 7.091 | 0.005 |
| GFF | 1 | 1.000 | 7.144 | 7.144 | 0.136 |
| IART | 3 | 0.333 | 2.386 | 7.159 | 0.079 |
| VVX | 2 | 0.500 | 3.870 | 7.740 | 0.186 |
| TFIN | 3 | 0.333 | 2.739 | 8.216 | 0.026 |
| SKYW | 1 | 1.000 | 9.189 | 9.189 | 0.152 |
| GTY | 8 | 0.375 | 1.353 | 10.821 | 0.014 |
| NPK | 5 | 1.000 | 2.180 | 10.900 | 0.064 |
| CWST | 2 | 1.000 | 7.843 | 15.685 | 0.154 |
| CVSA | 2 | 1.000 | 15.117 | 30.234 | 0.104 |
