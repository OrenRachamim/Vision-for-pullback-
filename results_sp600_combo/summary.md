# Pullback scanner - backtest report (`pullback_scanner.py`)

* tickers: 560 / 590 | period: 2016-01-01 -> today
* entry: next open | stop: base_lo | target: 2.0R | max hold: 10 days | dedupe cooldown: 5 bars | combo: daily signal within 15 days after a weekly signal
* baseline = every trading day of the same tickers, same period (1,426,819 days)

## 1. Forward returns vs baseline (next open -> close t+h)

| group / horizon | n | mean | median | pct_up | t_vs_base | p |
|---|---|---|---|---|---|---|
| baseline 5d | 1,423,869 | 0.003 | 0.002 | 0.517 |  |  |
| daily 5d | 5,189 | -0.000 | -0.001 | 0.482 | -4.748 | 0.000 |
| weekly 5d | 264 | -0.002 | 0.002 | 0.519 | -1.796 | 0.073 |
| BUY SIGNAL (daily+weekly) 5d | 33 | -0.004 | 0.000 | 0.515 | -1.550 | 0.121 |
| combo 5d | 53 | -0.000 | 0.003 | 0.528 | -0.745 | 0.456 |
| baseline 10d | 1,420,919 | 0.006 | 0.004 | 0.527 |  |  |
| daily 10d | 5,185 | 0.004 | 0.002 | 0.516 | -2.823 | 0.005 |
| weekly 10d | 264 | 0.000 | -0.001 | 0.492 | -1.683 | 0.092 |
| BUY SIGNAL (daily+weekly) 10d | 33 | 0.004 | 0.011 | 0.576 | -0.275 | 0.783 |
| combo 10d | 53 | 0.007 | 0.012 | 0.604 | 0.182 | 0.856 |
| baseline 20d | 1,415,019 | 0.013 | 0.008 | 0.538 |  |  |
| daily 20d | 5,175 | 0.010 | 0.009 | 0.542 | -2.163 | 0.031 |
| weekly 20d | 264 | 0.000 | -0.007 | 0.451 | -2.490 | 0.013 |
| BUY SIGNAL (daily+weekly) 20d | 33 | -0.004 | -0.005 | 0.485 | -1.171 | 0.242 |
| combo 20d | 53 | 0.002 | 0.012 | 0.566 | -0.929 | 0.353 |
| baseline 60d | 1,391,419 | 0.041 | 0.025 | 0.563 |  |  |
| daily 60d | 5,134 | 0.020 | 0.020 | 0.556 | -9.179 | 0.000 |
| weekly 60d | 263 | -0.009 | 0.005 | 0.529 | -5.484 | 0.000 |
| BUY SIGNAL (daily+weekly) 60d | 33 | -0.015 | 0.003 | 0.515 | -2.156 | 0.031 |
| combo 60d | 53 | 0.010 | 0.035 | 0.585 | -1.540 | 0.124 |

> p is a normal-approx Welch test. Baseline days overlap, so treat p as optimistic.

## 2. Trade simulation with the scanner's own levels

| group | n | trades | win_rate | avg_R | R_ci95 | profit_factor | avg_risk_pct | stopped | hit_target | gap_below_stop | total_R |
|---|---|---|---|---|---|---|---|---|---|---|---|
| daily | 5192 | 5142 | 0.460 | 0.015 | [-0.01, 0.04] | 1.035 | 0.059 | 0.326 | 0.099 | 0.009 | 77.005 |
| weekly | 264 | 264 | 0.489 | 0.063 | [-0.03, 0.15] | 1.235 | 0.071 | 0.148 | 0.049 | 0 | 16.573 |
| BUY SIGNAL (daily+weekly) | 33 | 33 | 0.576 | 0.157 | [-0.08, 0.40] | 1.763 | 0.067 | 0.121 | 0 | 0 | 5.186 |
| combo | 53 | 53 | 0.566 | 0.119 | [-0.11, 0.35] | 1.405 | 0.059 | 0.226 | 0.019 | 0 | 6.284 |
| CONTROL: random days, same exits | 475467 | 474250 | 0.453 | 0.038 | [0.03, 0.04] | 1.084 | 0.059 | 0.376 | 0.144 | 0 | 18099.514 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the tested signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* daily vs CONTROL: avg_R diff = -0.023R, t = -1.57, p = 0.115
* weekly vs CONTROL: avg_R diff = +0.025R, t = 0.52, p = 0.601
* BUY SIGNAL (daily+weekly) vs CONTROL: avg_R diff = +0.119R, t = 0.94, p = 0.349
* combo vs CONTROL: avg_R diff = +0.081R, t = 0.69, p = 0.488

## 3. Combo signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=25 | 5 | 5 | 0.400 | 0.070 | [-0.32, 0.46] | 1.389 | -0.020 |
| score=50 | 22 | 22 | 0.591 | 0.163 | [-0.21, 0.54] | 1.543 | -0.006 |
| score=75 | 22 | 22 | 0.545 | 0.009 | [-0.30, 0.33] | 1.030 | 0.005 |
| score=100 | 4 | 4 | 0.750 | 0.537 | [nan, nan] | 2.719 | 0.067 |
| slowing=True | 34 | 34 | 0.618 | 0.152 | [-0.12, 0.42] | 1.572 | 0.005 |
| slowing=False | 19 | 19 | 0.474 | 0.058 | [-0.34, 0.45] | 1.171 | -0.002 |
| drying=True | 8 | 8 | 0.500 | 0.040 | [-0.64, 0.80] | 1.098 | 0.005 |
| drying=False | 45 | 45 | 0.578 | 0.132 | [-0.10, 0.37] | 1.489 | 0.002 |
| uptrend=True | 36 | 36 | 0.583 | 0.137 | [-0.17, 0.42] | 1.429 | 0.018 |
| uptrend=False | 17 | 17 | 0.529 | 0.079 | [-0.23, 0.37] | 1.338 | -0.031 |

Phase lengths found by detect() (bars):

| phase | mean | min | 50% | max |
|---|---|---|---|---|
| decline_len | 16.189 | 3.000 | 14 | 40 |
| slowdown_len | 16.604 | 0 | 13 | 47 |
| base_len | 7.189 | 3.000 | 8.000 | 10 |
| peak_to_low | 26.736 | 5.000 | 30 | 40 |
| base_above_low | 0.012 | 0 | 0.012 | 0.029 |

## 4. Combo signals per year

| year | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| 2016 | 8 | 0.625 | -0.004 | -0.036 | 0.016 |
| 2017 | 8 | 0.875 | 0.786 | 6.285 | 0.018 |
| 2018 | 7 | 0.286 | -0.263 | -1.843 | -0.023 |
| 2019 | 4 | 0.250 | -0.414 | -1.657 | -0.011 |
| 2020 | 1 | 0 | -1.000 | -1.000 | -0.194 |
| 2021 | 2 | 0.500 | 0.202 | 0.403 | -0.001 |
| 2022 | 1 | 1.000 | 0.952 | 0.952 | -0.050 |
| 2023 | 6 | 0.500 | -0.255 | -1.530 | -0.036 |
| 2024 | 8 | 0.750 | 0.639 | 5.116 | 0.066 |
| 2025 | 7 | 0.429 | -0.085 | -0.592 | -0.013 |
| 2026 | 1 | 1.000 | 0.185 | 0.185 | 0.085 |

## 5. Combo signals per ticker (15 worst and 15 best by total_R)

| ticker | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| FLO | 2 | 0 | -1.000 | -2.000 | -0.139 |
| NIC | 1 | 0 | -1.250 | -1.250 | 0.047 |
| ABR | 1 | 0 | -1.000 | -1.000 | 0.034 |
| WABC | 1 | 0 | -1.000 | -1.000 | -0.031 |
| APLE | 1 | 0 | -1.000 | -1.000 | 0.031 |
| BKU | 1 | 0 | -1.000 | -1.000 | -0.105 |
| SBSI | 1 | 0 | -1.000 | -1.000 | 0.014 |
| CPF | 1 | 0 | -1.000 | -1.000 | -0.072 |
| NTST | 1 | 0 | -1.000 | -1.000 | -0.126 |
| MTRN | 1 | 0 | -1.000 | -1.000 | -0.044 |
| HCSG | 1 | 0 | -1.000 | -1.000 | -0.136 |
| SBCF | 1 | 0 | -0.786 | -0.786 | -0.072 |
| NWL | 1 | 0 | -0.532 | -0.532 | 0.013 |
| TFIN | 1 | 0 | -0.449 | -0.449 | -0.127 |
| CHCO | 1 | 0 | -0.380 | -0.380 | 0.001 |
| SXT | 1 | 1.000 | 0.760 | 0.760 | 0.031 |
| REYN | 1 | 1.000 | 0.781 | 0.781 | 0.033 |
| TRNO | 1 | 1.000 | 0.812 | 0.812 | 0.055 |
| SNEX | 1 | 1.000 | 0.870 | 0.870 | 0.081 |
| FFBC | 1 | 1.000 | 0.905 | 0.905 | -0.011 |
| MPT | 1 | 1.000 | 0.952 | 0.952 | -0.050 |
| NPK | 1 | 1.000 | 1.038 | 1.038 | 0.152 |
| OSIS | 1 | 1.000 | 1.050 | 1.050 | 0.070 |
| WINA | 1 | 1.000 | 1.058 | 1.058 | 0.113 |
| MC | 1 | 1.000 | 1.214 | 1.214 | 0.035 |
| MSGS | 1 | 1.000 | 1.308 | 1.308 | 0.123 |
| FULT | 1 | 1.000 | 1.360 | 1.360 | 0.175 |
| BANF | 1 | 1.000 | 1.540 | 1.540 | 0.234 |
| IVT | 1 | 1.000 | 1.834 | 1.834 | 0.073 |
| FELE | 1 | 1.000 | 2.000 | 2.000 | 0.103 |
