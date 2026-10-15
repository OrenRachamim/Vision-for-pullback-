# Pullback scanner - backtest report (`pullback_scanner.py`)

* tickers: 558 / 590 | period: 2016-01-01 -> today
* entry: next open | stop: base_lo | exit: trailing stop 3.0*ATR14 from highest high, no target | max hold: 60 days | dedupe cooldown: 5 bars | index combo (sector): stock daily signal + index pullback signal within 5 days
* baseline = every trading day of the same tickers, same period (1,426,819 days)

## 1. Forward returns vs baseline (next open -> close t+h)

| group / horizon | n | mean | median | pct_up | t_vs_base | p |
|---|---|---|---|---|---|---|
| baseline 5d | 1,423,869 | 0.003 | 0.002 | 0.517 |  |  |
| daily 5d | 4,973 | 0.001 | 0.001 | 0.506 | -2.494 | 0.013 |
| combo 5d | 1,282 | 0.002 | 0.000 | 0.501 | -0.754 | 0.451 |
| baseline 10d | 1,420,919 | 0.006 | 0.004 | 0.527 |  |  |
| daily 10d | 4,962 | 0.004 | 0.003 | 0.527 | -2.258 | 0.024 |
| combo 10d | 1,281 | 0.009 | 0.005 | 0.536 | 1.275 | 0.202 |
| baseline 20d | 1,415,019 | 0.013 | 0.008 | 0.538 |  |  |
| daily 20d | 4,953 | 0.010 | 0.008 | 0.541 | -2.524 | 0.012 |
| combo 20d | 1,280 | 0.017 | 0.009 | 0.541 | 1.642 | 0.101 |
| baseline 60d | 1,391,419 | 0.041 | 0.025 | 0.563 |  |  |
| daily 60d | 4,912 | 0.021 | 0.021 | 0.557 | -8.472 | 0.000 |
| combo 60d | 1,274 | 0.025 | 0.032 | 0.593 | -3.615 | 0.000 |

> p is a normal-approx Welch test. Baseline days overlap, so treat p as optimistic.

## 2. Trade simulation with the scanner's own levels

| group | n | trades | win_rate | avg_R | R_ci95 | profit_factor | avg_risk_pct | stopped | trailed | hit_target | gap_below_stop | total_R |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| daily | 4976 | 4915 | 0.357 | 0.074 | [0.03, 0.12] | 1.154 | 0.059 | 0.246 | 0.725 | 0 | 0.009 | 368.326 |
| combo | 1285 | 1263 | 0.378 | 0.153 | [0.07, 0.24] | 1.343 | 0.060 | 0.225 | 0.743 | 0 | 0.013 | 195.331 |
| CONTROL: random days, same exits | 475467 | 473137 | 0.327 | 0.069 | [0.06, 0.07] | 1.129 | 0.060 | 0.338 | 0.645 | 0 | 0 | 34397.249 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the tested signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* daily vs CONTROL: avg_R diff = +0.006R, t = 0.23, p = 0.818
* combo vs CONTROL: avg_R diff = +0.085R, t = 1.86, p = 0.063

## 3. Combo signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=25 | 226 | 221 | 0.416 | 0.176 | [-0.03, 0.41] | 1.356 | 0.023 |
| score=50 | 562 | 551 | 0.385 | 0.186 | [0.05, 0.33] | 1.423 | 0.020 |
| score=75 | 378 | 374 | 0.358 | 0.112 | [-0.04, 0.28] | 1.253 | 0.010 |
| score=100 | 119 | 117 | 0.342 | 0.093 | [-0.15, 0.39] | 1.222 | 0.020 |
| slowing=True | 515 | 505 | 0.352 | 0.117 | [-0.02, 0.26] | 1.261 | 0.013 |
| slowing=False | 770 | 758 | 0.396 | 0.178 | [0.06, 0.29] | 1.397 | 0.020 |
| drying=True | 332 | 329 | 0.389 | 0.159 | [-0.01, 0.35] | 1.369 | 0.021 |
| drying=False | 953 | 934 | 0.375 | 0.152 | [0.05, 0.25] | 1.334 | 0.016 |
| uptrend=True | 828 | 816 | 0.360 | 0.132 | [0.02, 0.25] | 1.305 | 0.015 |
| uptrend=False | 457 | 447 | 0.412 | 0.194 | [0.05, 0.35] | 1.406 | 0.022 |

Phase lengths found by detect() (bars):

| phase | mean | min | 50% | max |
|---|---|---|---|---|
| decline_len | 15.791 | 2.000 | 14 | 40 |
| slowdown_len | 8.413 | 0 | 5.000 | 57 |
| base_len | 5.463 | 3.000 | 5.000 | 10 |
| peak_to_low | 21.937 | 0 | 21 | 40 |
| base_above_low | 0.008 | 0 | 0 | 0.090 |

## 4. Combo signals per year

| year | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| 2016 | 167 | 0.519 | 0.917 | 148.634 | 0.067 |
| 2017 | 188 | 0.326 | -0.029 | -5.356 | 0.006 |
| 2018 | 127 | 0.222 | -0.282 | -35.533 | -0.015 |
| 2019 | 119 | 0.407 | 0.128 | 15.057 | 0.006 |
| 2020 | 28 | 0.296 | 0.090 | 2.443 | -0.035 |
| 2021 | 82 | 0.287 | -0.095 | -7.561 | 0.017 |
| 2022 | 56 | 0.232 | -0.320 | -17.911 | 0.030 |
| 2023 | 146 | 0.372 | 0.230 | 33.328 | 0.015 |
| 2024 | 195 | 0.448 | 0.352 | 68.348 | 0.030 |
| 2025 | 105 | 0.350 | -0.251 | -25.832 | -0.002 |
| 2026 | 72 | 0.554 | 0.281 | 19.713 | 0.019 |

## 5. Combo signals per ticker (15 worst and 15 best by total_R)

| ticker | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| DMC | 6 | 0 | -0.853 | -5.117 | -0.065 |
| AKR | 6 | 0 | -0.778 | -4.670 | -0.039 |
| KOP | 4 | 0 | -1.064 | -4.255 | -0.052 |
| FUL | 5 | 0.200 | -0.850 | -4.248 | -0.069 |
| WU | 4 | 0 | -0.906 | -3.624 | -0.052 |
| REYN | 4 | 0 | -0.849 | -3.397 | -0.003 |
| MD | 3 | 0 | -1.113 | -3.340 | -0.037 |
| ECPG | 3 | 0 | -1.092 | -3.275 | 0.088 |
| HZO | 1 | 0 | -3.201 | -3.201 | -0.128 |
| POOL | 3 | 0 | -1.040 | -3.120 | 0.011 |
| ITGR | 5 | 0.200 | -0.610 | -3.050 | 0.003 |
| MAC | 4 | 0 | -0.758 | -3.033 | -0.055 |
| LAZ | 3 | 0 | -1.000 | -3.000 | -0.048 |
| VSH | 3 | 0 | -1.000 | -3.000 | -0.096 |
| TILE | 5 | 0 | -0.586 | -2.929 | -0.011 |
| RUN | 1 | 1.000 | 7.385 | 7.385 | 0.086 |
| RNST | 5 | 0.500 | 1.906 | 7.625 | 0.075 |
| IART | 3 | 0.333 | 2.557 | 7.672 | 0.083 |
| GOLF | 3 | 0.667 | 2.700 | 8.101 | 0.080 |
| RUSHA | 4 | 0.750 | 2.068 | 8.271 | 0.061 |
| TFIN | 2 | 0.500 | 4.163 | 8.326 | 0.045 |
| AAT | 5 | 0.600 | 1.704 | 8.521 | 0.081 |
| MDU | 7 | 0.714 | 1.236 | 8.654 | 0.054 |
| NPK | 6 | 0.667 | 1.621 | 9.725 | 0.055 |
| DCOM | 5 | 0.600 | 2.002 | 10.009 | 0.069 |
| TMP | 7 | 0.714 | 1.532 | 10.727 | 0.077 |
| GFF | 4 | 0.750 | 2.691 | 10.763 | 0.067 |
| WOR | 6 | 0.500 | 1.828 | 10.968 | 0.015 |
| SKYW | 3 | 0.667 | 4.053 | 12.158 | 0.077 |
| CWST | 1 | 1.000 | 14.588 | 14.588 | 0.224 |
