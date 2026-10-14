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
| combo 5d | 36 | 0.004 | 0.002 | 0.528 | 0.278 | 0.781 |
| baseline 10d | 1,420,919 | 0.006 | 0.004 | 0.527 |  |  |
| daily 10d | 5,185 | 0.004 | 0.002 | 0.516 | -2.823 | 0.005 |
| weekly 10d | 264 | 0.000 | -0.001 | 0.492 | -1.683 | 0.092 |
| BUY SIGNAL (daily+weekly) 10d | 33 | 0.004 | 0.011 | 0.576 | -0.275 | 0.783 |
| combo 10d | 36 | 0.011 | 0.010 | 0.611 | 0.505 | 0.614 |
| baseline 20d | 1,415,019 | 0.013 | 0.008 | 0.538 |  |  |
| daily 20d | 5,175 | 0.010 | 0.009 | 0.542 | -2.163 | 0.031 |
| weekly 20d | 264 | 0.000 | -0.007 | 0.451 | -2.490 | 0.013 |
| BUY SIGNAL (daily+weekly) 20d | 33 | -0.004 | -0.005 | 0.485 | -1.171 | 0.242 |
| combo 20d | 36 | 0.018 | 0.019 | 0.639 | 0.346 | 0.729 |
| baseline 60d | 1,391,419 | 0.041 | 0.025 | 0.563 |  |  |
| daily 60d | 5,134 | 0.020 | 0.020 | 0.556 | -9.179 | 0.000 |
| weekly 60d | 263 | -0.009 | 0.005 | 0.529 | -5.484 | 0.000 |
| BUY SIGNAL (daily+weekly) 60d | 33 | -0.015 | 0.003 | 0.515 | -2.156 | 0.031 |
| combo 60d | 36 | 0.026 | 0.038 | 0.667 | -0.612 | 0.540 |

> p is a normal-approx Welch test. Baseline days overlap, so treat p as optimistic.

## 2. Trade simulation with the scanner's own levels

| group | n | trades | win_rate | avg_R | R_ci95 | profit_factor | avg_risk_pct | stopped | hit_target | gap_below_stop | total_R |
|---|---|---|---|---|---|---|---|---|---|---|---|
| daily | 5192 | 5142 | 0.460 | 0.015 | [-0.01, 0.04] | 1.035 | 0.059 | 0.326 | 0.099 | 0.009 | 77.005 |
| weekly | 264 | 264 | 0.489 | 0.063 | [-0.03, 0.15] | 1.235 | 0.071 | 0.148 | 0.049 | 0 | 16.573 |
| BUY SIGNAL (daily+weekly) | 33 | 33 | 0.576 | 0.157 | [-0.08, 0.40] | 1.763 | 0.067 | 0.121 | 0 | 0 | 5.186 |
| combo | 36 | 36 | 0.583 | 0.137 | [-0.17, 0.42] | 1.429 | 0.062 | 0.250 | 0.028 | 0 | 4.933 |
| CONTROL: random days, same exits | 271395 | 270755 | 0.455 | 0.016 | [0.01, 0.02] | 1.038 | 0.062 | 0.345 | 0.121 | 0 | 4563.846 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the tested signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* daily vs CONTROL: avg_R diff = -0.002R, t = -0.11, p = 0.913
* weekly vs CONTROL: avg_R diff = +0.046R, t = 0.97, p = 0.333
* BUY SIGNAL (daily+weekly) vs CONTROL: avg_R diff = +0.141R, t = 1.10, p = 0.270
* combo vs CONTROL: avg_R diff = +0.121R, t = 0.77, p = 0.439

> require-uptrend: buy only when price > SMA200; CONTROL also samples only days with price > SMA200.

## 3. Combo signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=50 | 14 | 14 | 0.500 | 0.054 | [-0.42, 0.58] | 1.136 | 0.004 |
| score=75 | 18 | 18 | 0.611 | 0.113 | [-0.24, 0.46] | 1.432 | 0.018 |
| score=100 | 4 | 4 | 0.750 | 0.537 | [nan, nan] | 2.719 | 0.067 |
| slowing=True | 22 | 22 | 0.636 | 0.190 | [-0.19, 0.56] | 1.702 | 0.027 |
| slowing=False | 14 | 14 | 0.500 | 0.054 | [-0.42, 0.58] | 1.136 | 0.004 |
| drying=True | 4 | 4 | 0.750 | 0.537 | [nan, nan] | 2.719 | 0.067 |
| drying=False | 32 | 32 | 0.562 | 0.087 | [-0.22, 0.41] | 1.272 | 0.012 |
| uptrend=True | 36 | 36 | 0.583 | 0.137 | [-0.17, 0.42] | 1.429 | 0.018 |

Phase lengths found by detect() (bars):

| phase | mean | min | 50% | max |
|---|---|---|---|---|
| decline_len | 14.278 | 3.000 | 11 | 35 |
| slowdown_len | 15.861 | 0 | 12.500 | 47 |
| base_len | 6.806 | 3.000 | 7.000 | 10 |
| peak_to_low | 24.083 | 5.000 | 24 | 40 |
| base_above_low | 0.011 | 0 | 0.012 | 0.028 |

## 4. Combo signals per year

| year | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| 2016 | 7 | 0.571 | -0.044 | -0.308 | 0.043 |
| 2017 | 5 | 0.800 | 0.932 | 4.659 | 0.047 |
| 2018 | 6 | 0.333 | -0.298 | -1.787 | -0.021 |
| 2019 | 4 | 0.250 | -0.414 | -1.657 | -0.011 |
| 2020 | 1 | 0 | -1.000 | -1.000 | -0.194 |
| 2021 | 1 | 0 | -0.083 | -0.083 | -0.008 |
| 2023 | 2 | 1.000 | 0.048 | 0.097 | -0.022 |
| 2024 | 6 | 0.833 | 0.884 | 5.304 | 0.073 |
| 2025 | 3 | 0.667 | -0.159 | -0.476 | 0.005 |
| 2026 | 1 | 1.000 | 0.185 | 0.185 | 0.085 |

## 5. Combo signals per ticker

| ticker | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| NIC | 1 | 0 | -1.250 | -1.250 | 0.047 |
| ABR | 1 | 0 | -1.000 | -1.000 | 0.034 |
| WABC | 1 | 0 | -1.000 | -1.000 | -0.031 |
| BKU | 1 | 0 | -1.000 | -1.000 | -0.105 |
| CPF | 1 | 0 | -1.000 | -1.000 | -0.072 |
| MTRN | 1 | 0 | -1.000 | -1.000 | -0.044 |
| HCSG | 1 | 0 | -1.000 | -1.000 | -0.136 |
| FLO | 1 | 0 | -1.000 | -1.000 | -0.194 |
| SBSI | 1 | 0 | -1.000 | -1.000 | 0.014 |
| SBCF | 1 | 0 | -0.786 | -0.786 | -0.072 |
| NWL | 1 | 0 | -0.532 | -0.532 | 0.013 |
| TFIN | 1 | 0 | -0.449 | -0.449 | -0.127 |
| CHCO | 1 | 0 | -0.380 | -0.380 | 0.001 |
| NHI | 1 | 0 | -0.083 | -0.083 | -0.008 |
| OUT | 1 | 0 | -0.015 | -0.015 | -0.038 |
| TMP | 1 | 1.000 | 0.006 | 0.006 | -0.024 |
| BRC | 1 | 1.000 | 0.080 | 0.080 | 0.033 |
| CAG | 1 | 1.000 | 0.086 | 0.086 | 0.024 |
| TNC | 1 | 1.000 | 0.090 | 0.090 | -0.021 |
| SHO | 1 | 1.000 | 0.150 | 0.150 | 0.004 |
| CWT | 1 | 1.000 | 0.185 | 0.185 | 0.085 |
| WDFC | 1 | 1.000 | 0.254 | 0.254 | 0.049 |
| DEA | 1 | 1.000 | 0.401 | 0.401 | 0.025 |
| AGO | 1 | 1.000 | 0.444 | 0.444 | 0.012 |
| CPK | 1 | 1.000 | 0.553 | 0.553 | 0.045 |
| SNEX | 1 | 1.000 | 0.870 | 0.870 | 0.081 |
| FFBC | 1 | 1.000 | 0.905 | 0.905 | -0.011 |
| NPK | 1 | 1.000 | 1.038 | 1.038 | 0.152 |
| OSIS | 1 | 1.000 | 1.050 | 1.050 | 0.070 |
| WINA | 1 | 1.000 | 1.058 | 1.058 | 0.113 |
| MC | 1 | 1.000 | 1.214 | 1.214 | 0.035 |
| MSGS | 1 | 1.000 | 1.308 | 1.308 | 0.123 |
| FULT | 1 | 1.000 | 1.360 | 1.360 | 0.175 |
| BANF | 1 | 1.000 | 1.540 | 1.540 | 0.234 |
| IVT | 1 | 1.000 | 1.834 | 1.834 | 0.073 |
| FELE | 1 | 1.000 | 2.000 | 2.000 | 0.103 |
