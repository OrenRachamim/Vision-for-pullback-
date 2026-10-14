# Pullback scanner - backtest report (`pullback_scanner.py`)

* tickers: 558 / 590 | period: 2016-01-01 -> today
* entry: next open | stop: base_lo | exit: trailing stop 2.0*ATR14 from highest high, no target | max hold: 60 days | dedupe cooldown: 5 bars | combo: daily signal within 15 days after a weekly signal
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
| daily | 4976 | 4920 | 0.375 | 0.053 | [0.02, 0.09] | 1.145 | 0.059 | 0.101 | 0.887 | 0 | 0.009 | 265.758 |
| weekly | 273 | 272 | 0.371 | 0.035 | [-0.08, 0.18] | 1.132 | 0.070 | 0.018 | 0.978 | 0 | 0 | 9.846 |
| BUY SIGNAL (daily+weekly) | 27 | 27 | 0.370 | -0.127 | [-0.28, 0.04] | 0.437 | 0.079 | 0 | 1.000 | 0 | 0 | -3.422 |
| combo | 47 | 47 | 0.404 | -0.026 | [-0.21, 0.18] | 0.902 | 0.065 | 0.021 | 0.979 | 0 | 0 | -1.224 |
| CONTROL: random days, same exits | 475467 | 474092 | 0.355 | 0.032 | [0.03, 0.04] | 1.079 | 0.065 | 0.188 | 0.809 | 0 | 0 | 16195.232 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the tested signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* daily vs CONTROL: avg_R diff = +0.021R, t = 1.20, p = 0.231
* weekly vs CONTROL: avg_R diff = +0.003R, t = 0.05, p = 0.964
* BUY SIGNAL (daily+weekly) vs CONTROL: avg_R diff = -0.159R, t = -1.93, p = 0.054
* combo vs CONTROL: avg_R diff = -0.058R, t = -0.56, p = 0.575

## 3. Combo signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=25 | 6 | 6 | 0.167 | -0.145 | [-0.39, 0.21] | 0.450 | -0.013 |
| score=50 | 24 | 24 | 0.417 | 0.098 | [-0.19, 0.45] | 1.399 | -0.006 |
| score=75 | 14 | 14 | 0.429 | -0.112 | [-0.39, 0.22] | 0.583 | -0.033 |
| score=100 | 3 | 3 | 0.667 | -0.377 | [nan, nan] | 0.094 | 0.032 |
| slowing=True | 27 | 27 | 0.444 | -0.145 | [-0.35, 0.06] | 0.486 | -0.014 |
| slowing=False | 20 | 20 | 0.350 | 0.134 | [-0.21, 0.56] | 1.551 | -0.010 |
| drying=True | 6 | 6 | 0.500 | -0.331 | [-0.76, 0.01] | 0.062 | -0.028 |
| drying=False | 41 | 41 | 0.390 | 0.019 | [-0.19, 0.25] | 1.073 | -0.010 |
| uptrend=True | 28 | 28 | 0.464 | 0.061 | [-0.23, 0.39] | 1.230 | -0.008 |
| uptrend=False | 19 | 19 | 0.316 | -0.154 | [-0.33, 0.04] | 0.419 | -0.019 |

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
| 2016 | 7 | 0.429 | 0.123 | 0.863 | 0.012 |
| 2017 | 9 | 0.667 | 0.289 | 2.599 | -0.008 |
| 2018 | 7 | 0.286 | -0.089 | -0.624 | -0.023 |
| 2019 | 3 | 0.667 | -0.075 | -0.225 | -0.008 |
| 2020 | 1 | 0 | -0.452 | -0.452 | -0.194 |
| 2021 | 2 | 0.500 | 0.456 | 0.912 | -0.054 |
| 2023 | 6 | 0.167 | -0.381 | -2.287 | -0.017 |
| 2024 | 2 | 0.500 | -0.142 | -0.285 | -0.036 |
| 2025 | 8 | 0.125 | -0.237 | -1.896 | -0.009 |
| 2026 | 2 | 1.000 | 0.085 | 0.171 | 0.068 |

## 5. Combo signals per ticker (15 worst and 15 best by total_R)

| ticker | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| NIC | 1 | 0 | -1.250 | -1.250 | 0.047 |
| FLO | 2 | 0 | -0.584 | -1.167 | -0.139 |
| HSTM | 2 | 0 | -0.582 | -1.164 | 0.017 |
| SBSI | 1 | 0 | -1.000 | -1.000 | 0.014 |
| MTRN | 1 | 0 | -0.873 | -0.873 | -0.044 |
| CNS | 2 | 0 | -0.400 | -0.800 | -0.034 |
| TFIN | 1 | 0 | -0.795 | -0.795 | -0.127 |
| LUMN | 1 | 0 | -0.647 | -0.647 | -0.173 |
| WABC | 1 | 0 | -0.517 | -0.517 | -0.031 |
| HTLD | 1 | 0 | -0.463 | -0.463 | 0.005 |
| BKU | 1 | 0 | -0.444 | -0.444 | -0.105 |
| REYN | 1 | 0 | -0.416 | -0.416 | 0.033 |
| HCSG | 1 | 0 | -0.408 | -0.408 | -0.136 |
| WEN | 1 | 0 | -0.400 | -0.400 | -0.007 |
| CPF | 1 | 0 | -0.392 | -0.392 | -0.072 |
| WDFC | 1 | 1.000 | 0.093 | 0.093 | 0.049 |
| UNF | 1 | 1.000 | 0.126 | 0.126 | 0.031 |
| FCPT | 1 | 1.000 | 0.141 | 0.141 | 0.050 |
| CAG | 1 | 1.000 | 0.191 | 0.191 | 0.024 |
| AGO | 1 | 1.000 | 0.280 | 0.280 | 0.012 |
| DEA | 1 | 1.000 | 0.316 | 0.316 | 0.025 |
| OSIS | 1 | 1.000 | 0.386 | 0.386 | 0.070 |
| TRNO | 1 | 1.000 | 0.510 | 0.510 | 0.055 |
| SPNT | 1 | 1.000 | 0.605 | 0.605 | 0.021 |
| FFBC | 1 | 1.000 | 0.671 | 0.671 | -0.011 |
| SXT | 1 | 1.000 | 0.713 | 0.713 | 0.031 |
| TR | 1 | 1.000 | 1.374 | 1.374 | -0.114 |
| WINA | 1 | 1.000 | 1.465 | 1.465 | 0.113 |
| MSGS | 1 | 1.000 | 1.528 | 1.528 | 0.123 |
| NPK | 1 | 1.000 | 2.680 | 2.680 | 0.152 |
