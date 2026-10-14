# Pullback scanner - backtest report (`pullback_scanner.py`)

* tickers: 558 / 590 | period: 2016-01-01 -> today
* entry: next open | stop: base_lo | target: 2.0R | max hold: 5 days | dedupe cooldown: 5 bars | combo: daily signal within 15 days after a weekly signal
* baseline = every trading day of the same tickers, same period (1,426,819 days)

## 1. Forward returns vs baseline (next open -> close t+h)

| group / horizon | n | mean | median | pct_up | t_vs_base | p |
|---|---|---|---|---|---|---|
| baseline 5d | 1,423,869 | 0.003 | 0.002 | 0.517 |  |  |
| daily 5d | 4,973 | 0.001 | 0.001 | 0.506 | -2.494 | 0.013 |
| weekly 5d | 272 | 0.000 | 0.002 | 0.533 | -1.237 | 0.216 |
| BUY SIGNAL (daily+weekly) 5d | 27 | 0.001 | 0.007 | 0.630 | -0.259 | 0.796 |
| combo 5d | 28 | 0.008 | 0.009 | 0.643 | 0.828 | 0.407 |
| baseline 10d | 1,420,919 | 0.006 | 0.004 | 0.527 |  |  |
| daily 10d | 4,962 | 0.004 | 0.003 | 0.527 | -2.258 | 0.024 |
| weekly 10d | 272 | -0.001 | -0.003 | 0.474 | -2.000 | 0.046 |
| BUY SIGNAL (daily+weekly) 10d | 27 | -0.008 | 0.000 | 0.519 | -1.900 | 0.057 |
| combo 10d | 28 | -0.006 | -0.001 | 0.500 | -1.173 | 0.241 |
| baseline 20d | 1,415,019 | 0.013 | 0.008 | 0.538 |  |  |
| daily 20d | 4,953 | 0.010 | 0.008 | 0.541 | -2.524 | 0.012 |
| weekly 20d | 272 | -0.001 | -0.008 | 0.445 | -2.933 | 0.003 |
| BUY SIGNAL (daily+weekly) 20d | 27 | -0.021 | -0.021 | 0.407 | -3.129 | 0.002 |
| combo 20d | 28 | -0.008 | 0.000 | 0.500 | -1.379 | 0.168 |
| baseline 60d | 1,391,419 | 0.041 | 0.025 | 0.563 |  |  |
| daily 60d | 4,912 | 0.021 | 0.021 | 0.557 | -8.472 | 0.000 |
| weekly 60d | 271 | -0.007 | 0.003 | 0.517 | -5.599 | 0.000 |
| BUY SIGNAL (daily+weekly) 60d | 27 | -0.002 | 0.031 | 0.556 | -1.840 | 0.066 |
| combo 60d | 28 | 0.020 | 0.036 | 0.607 | -0.809 | 0.419 |

> p is a normal-approx Welch test. Baseline days overlap, so treat p as optimistic.

## 2. Trade simulation with the scanner's own levels

| group | n | trades | win_rate | avg_R | R_ci95 | profit_factor | avg_risk_pct | stopped | hit_target | gap_below_stop | total_R |
|---|---|---|---|---|---|---|---|---|---|---|---|
| daily | 4976 | 4926 | 0.482 | 0.014 | [-0.01, 0.04] | 1.045 | 0.059 | 0.200 | 0.052 | 0.009 | 70.706 |
| weekly | 273 | 272 | 0.529 | 0.029 | [-0.05, 0.10] | 1.134 | 0.070 | 0.092 | 0.022 | 0 | 8.051 |
| BUY SIGNAL (daily+weekly) | 27 | 27 | 0.630 | 0.055 | [-0.13, 0.26] | 1.349 | 0.079 | 0 | 0.037 | 0 | 1.473 |
| combo | 28 | 28 | 0.607 | -0.017 | [-0.25, 0.24] | 0.930 | 0.069 | 0.107 | 0.036 | 0 | -0.485 |
| CONTROL: random days, same exits | 271395 | 271139 | 0.478 | 0.007 | [0.00, 0.01] | 1.022 | 0.069 | 0.214 | 0.063 | 0 | 1856.369 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the tested signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* daily vs CONTROL: avg_R diff = +0.008R, t = 0.62, p = 0.536
* weekly vs CONTROL: avg_R diff = +0.022R, t = 0.58, p = 0.561
* BUY SIGNAL (daily+weekly) vs CONTROL: avg_R diff = +0.048R, t = 0.47, p = 0.641
* combo vs CONTROL: avg_R diff = -0.024R, t = -0.19, p = 0.847

> require-uptrend: buy only when price > SMA200; CONTROL also samples only days with price > SMA200.

## 3. Combo signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=50 | 14 | 14 | 0.643 | 0.120 | [-0.23, 0.54] | 1.548 | -0.009 |
| score=75 | 11 | 11 | 0.545 | -0.140 | [-0.40, 0.11] | 0.421 | -0.018 |
| score=100 | 3 | 3 | 0.667 | -0.207 | [nan, nan] | 0.503 | 0.032 |
| slowing=True | 14 | 14 | 0.571 | -0.154 | [-0.47, 0.11] | 0.447 | -0.007 |
| slowing=False | 14 | 14 | 0.643 | 0.120 | [-0.23, 0.54] | 1.548 | -0.009 |
| drying=True | 3 | 3 | 0.667 | -0.207 | [nan, nan] | 0.503 | 0.032 |
| drying=False | 25 | 25 | 0.600 | 0.005 | [-0.23, 0.27] | 1.024 | -0.013 |
| uptrend=True | 28 | 28 | 0.607 | -0.017 | [-0.25, 0.24] | 0.930 | -0.008 |

Phase lengths found by detect() (bars):

| phase | mean | min | 50% | max |
|---|---|---|---|---|
| decline_len | 14.036 | 3.000 | 11 | 35 |
| slowdown_len | 14.786 | 0 | 11.500 | 47 |
| base_len | 7.286 | 3.000 | 8.000 | 10 |
| peak_to_low | 22.679 | 5.000 | 21.500 | 40 |
| base_above_low | 0.009 | 0 | 0.007 | 0.025 |

## 4. Combo signals per year

| year | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| 2016 | 6 | 0.500 | -0.232 | -1.390 | 0.042 |
| 2017 | 4 | 1.000 | 0.260 | 1.040 | 0.016 |
| 2018 | 6 | 0.500 | -0.176 | -1.056 | -0.021 |
| 2019 | 2 | 0.500 | -0.084 | -0.168 | -0.028 |
| 2020 | 1 | 0 | -1.000 | -1.000 | -0.194 |
| 2021 | 1 | 1.000 | 2.000 | 2.000 | -0.114 |
| 2023 | 3 | 0.333 | -0.132 | -0.396 | -0.010 |
| 2024 | 1 | 1.000 | 0.114 | 0.114 | -0.127 |
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
| SBCF | 1 | 0 | -0.492 | -0.492 | -0.072 |
| HSTM | 1 | 0 | -0.455 | -0.455 | 0.016 |
| WABC | 1 | 0 | -0.451 | -0.451 | -0.031 |
| BKU | 1 | 0 | -0.238 | -0.238 | -0.105 |
| TMP | 1 | 0 | -0.066 | -0.066 | -0.024 |
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
| BMI | 1 | 1.000 | 0.350 | 0.350 | -0.037 |
| BRC | 1 | 1.000 | 0.420 | 0.420 | 0.033 |
| WINA | 1 | 1.000 | 0.601 | 0.601 | 0.113 |
| MSGS | 1 | 1.000 | 0.615 | 0.615 | 0.123 |
| OSIS | 1 | 1.000 | 0.820 | 0.820 | 0.070 |
| TR | 1 | 1.000 | 2.000 | 2.000 | -0.114 |
