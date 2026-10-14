# Pullback scanner - backtest report (`pullback_scanner.py`)

* tickers: 560 / 590 | period: 2016-01-01 -> today
* entry: next open | stop: base_lo | target: 2.0R | max hold: 5 days | dedupe cooldown: 5 bars | combo: daily signal within 15 days after a weekly signal
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
| daily | 5192 | 5143 | 0.458 | -0.017 | [-0.04, 0.01] | 0.949 | 0.059 | 0.209 | 0.049 | 0.009 | -85.083 |
| weekly | 264 | 264 | 0.515 | 0.009 | [-0.07, 0.08] | 1.039 | 0.071 | 0.083 | 0.019 | 0 | 2.274 |
| BUY SIGNAL (daily+weekly) | 33 | 33 | 0.515 | -0.084 | [-0.22, 0.04] | 0.571 | 0.067 | 0.030 | 0 | 0 | -2.758 |
| combo | 36 | 36 | 0.500 | -0.065 | [-0.25, 0.11] | 0.742 | 0.062 | 0.083 | 0 | 0 | -2.327 |
| CONTROL: random days, same exits | 271395 | 271126 | 0.477 | 0.008 | [0.01, 0.01] | 1.026 | 0.062 | 0.229 | 0.066 | 0 | 2321.117 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the tested signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* daily vs CONTROL: avg_R diff = -0.025R, t = -2.13, p = 0.033
* weekly vs CONTROL: avg_R diff = +0.000R, t = 0.01, p = 0.995
* BUY SIGNAL (daily+weekly) vs CONTROL: avg_R diff = -0.092R, t = -1.36, p = 0.175
* combo vs CONTROL: avg_R diff = -0.073R, t = -0.79, p = 0.427

> require-uptrend: buy only when price > SMA200; CONTROL also samples only days with price > SMA200.

## 3. Combo signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=50 | 14 | 14 | 0.571 | -0.026 | [-0.29, 0.23] | 0.882 | 0.004 |
| score=75 | 18 | 18 | 0.389 | -0.162 | [-0.34, 0.04] | 0.375 | 0.018 |
| score=100 | 4 | 4 | 0.750 | 0.238 | [nan, nan] | 1.763 | 0.067 |
| slowing=True | 22 | 22 | 0.455 | -0.089 | [-0.33, 0.14] | 0.668 | 0.027 |
| slowing=False | 14 | 14 | 0.571 | -0.026 | [-0.29, 0.23] | 0.882 | 0.004 |
| drying=True | 4 | 4 | 0.750 | 0.238 | [nan, nan] | 1.763 | 0.067 |
| drying=False | 32 | 32 | 0.469 | -0.103 | [-0.26, 0.05] | 0.578 | 0.012 |
| uptrend=True | 36 | 36 | 0.500 | -0.065 | [-0.25, 0.11] | 0.742 | 0.018 |

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
| 2016 | 7 | 0.571 | -0.109 | -0.762 | 0.043 |
| 2017 | 5 | 1.000 | 0.523 | 2.614 | 0.047 |
| 2018 | 6 | 0.500 | -0.176 | -1.056 | -0.021 |
| 2019 | 4 | 0.250 | -0.183 | -0.734 | -0.011 |
| 2020 | 1 | 0 | -1.000 | -1.000 | -0.194 |
| 2021 | 1 | 0 | -0.469 | -0.469 | -0.008 |
| 2023 | 2 | 0.500 | 0.029 | 0.059 | -0.022 |
| 2024 | 6 | 0.167 | -0.225 | -1.351 | 0.073 |
| 2025 | 3 | 0.667 | 0.031 | 0.092 | 0.005 |
| 2026 | 1 | 1.000 | 0.279 | 0.279 | 0.085 |

## 5. Combo signals per ticker

| ticker | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| NIC | 1 | 0 | -1.250 | -1.250 | 0.047 |
| SBSI | 1 | 0 | -1.000 | -1.000 | 0.014 |
| FLO | 1 | 0 | -1.000 | -1.000 | -0.194 |
| ABR | 1 | 0 | -0.786 | -0.786 | 0.034 |
| HCSG | 1 | 0 | -0.654 | -0.654 | -0.136 |
| MTRN | 1 | 0 | -0.581 | -0.581 | -0.044 |
| SHO | 1 | 0 | -0.495 | -0.495 | 0.004 |
| SBCF | 1 | 0 | -0.492 | -0.492 | -0.072 |
| NHI | 1 | 0 | -0.469 | -0.469 | -0.008 |
| NWL | 1 | 0 | -0.456 | -0.456 | 0.013 |
| WABC | 1 | 0 | -0.451 | -0.451 | -0.031 |
| FULT | 1 | 0 | -0.442 | -0.442 | 0.175 |
| BANF | 1 | 0 | -0.415 | -0.415 | 0.234 |
| BKU | 1 | 0 | -0.238 | -0.238 | -0.105 |
| CHCO | 1 | 0 | -0.110 | -0.110 | 0.001 |
| SNEX | 1 | 0 | -0.072 | -0.072 | 0.081 |
| TMP | 1 | 0 | -0.066 | -0.066 | -0.024 |
| IVT | 1 | 0 | -0.041 | -0.041 | 0.073 |
| OUT | 1 | 1.000 | 0.000 | 0.000 | -0.038 |
| WDFC | 1 | 1.000 | 0.070 | 0.070 | 0.049 |
| DEA | 1 | 1.000 | 0.088 | 0.088 | 0.025 |
| TFIN | 1 | 1.000 | 0.114 | 0.114 | -0.127 |
| AGO | 1 | 1.000 | 0.123 | 0.123 | 0.012 |
| TNC | 1 | 1.000 | 0.125 | 0.125 | -0.021 |
| CAG | 1 | 1.000 | 0.135 | 0.135 | 0.024 |
| NPK | 1 | 1.000 | 0.183 | 0.183 | 0.152 |
| CPF | 1 | 1.000 | 0.231 | 0.231 | -0.072 |
| CWT | 1 | 1.000 | 0.279 | 0.279 | 0.085 |
| FFBC | 1 | 1.000 | 0.333 | 0.333 | -0.011 |
| BRC | 1 | 1.000 | 0.420 | 0.420 | 0.033 |
| WINA | 1 | 1.000 | 0.601 | 0.601 | 0.113 |
| MSGS | 1 | 1.000 | 0.615 | 0.615 | 0.123 |
| CPK | 1 | 1.000 | 0.628 | 0.628 | 0.045 |
| MC | 1 | 1.000 | 0.738 | 0.738 | 0.035 |
| OSIS | 1 | 1.000 | 0.820 | 0.820 | 0.070 |
| FELE | 1 | 1.000 | 1.186 | 1.186 | 0.103 |
