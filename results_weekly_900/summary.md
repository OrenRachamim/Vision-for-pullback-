# Pullback scanner - backtest report (`pullback_scanner.py`)

* tickers: 331 / 898 | period: 2016-01-01 -> today
* entry: next open | stop: base_lo | target: 2.0R | max hold: 20 days | dedupe cooldown: 5 bars
* baseline = every trading day of the same tickers, same period (2,291,105 days)

## 1. Forward returns vs baseline (next open -> close t+h)

| group / horizon | n | mean | median | pct_up | t_vs_base | p |
|---|---|---|---|---|---|---|
| baseline 5d | 2,286,615 | 0.004 | 0.003 | 0.538 |  |  |
| weekly 5d | 524 | -0.001 | -0.001 | 0.483 | -3.283 | 0.001 |
| baseline 10d | 2,282,125 | 0.008 | 0.006 | 0.552 |  |  |
| weekly 10d | 524 | 0.000 | 0.000 | 0.502 | -4.089 | 0.000 |
| baseline 20d | 2,273,145 | 0.017 | 0.012 | 0.568 |  |  |
| weekly 20d | 523 | 0.003 | 0.009 | 0.570 | -4.548 | 0.000 |
| baseline 60d | 2,237,225 | 0.051 | 0.036 | 0.607 |  |  |
| weekly 60d | 521 | 0.004 | 0.016 | 0.582 | -7.693 | 0.000 |

> p is a normal-approx Welch test. Baseline days overlap, so treat p as optimistic.

## 2. Trade simulation with the scanner's own levels

| group | n | trades | win_rate | avg_R | R_ci95 | profit_factor | avg_risk_pct | stopped | hit_target | gap_below_stop | total_R |
|---|---|---|---|---|---|---|---|---|---|---|---|
| weekly | 526 | 524 | 0.542 | 0.093 | [0.02, 0.17] | 1.280 | 0.067 | 0.268 | 0.055 | 0 | 49.670 |
| CONTROL: random days, same exits | 763445 | 759744 | 0.488 | 0.110 | [0.11, 0.11] | 1.255 | 0.067 | 0.367 | 0.155 | 0 | 84745.439 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the tested signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* weekly vs CONTROL: avg_R diff = -0.017R, t = -0.43, p = 0.671

## 3. Weekly signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=25 | 116 | 115 | 0.487 | -0.042 | [-0.24, 0.13] | 0.903 | 0.002 |
| score=50 | 218 | 218 | 0.532 | 0.079 | [-0.04, 0.20] | 1.233 | -0.002 |
| score=75 | 145 | 144 | 0.597 | 0.220 | [0.07, 0.35] | 1.850 | 0.014 |
| score=100 | 47 | 47 | 0.553 | 0.106 | [-0.13, 0.34] | 1.387 | 0.004 |
| slowing=True | 290 | 289 | 0.543 | 0.153 | [0.05, 0.26] | 1.500 | 0.005 |
| slowing=False | 236 | 235 | 0.540 | 0.020 | [-0.09, 0.13] | 1.055 | 0.002 |
| drying=True | 142 | 142 | 0.535 | 0.097 | [-0.05, 0.25] | 1.283 | 0.000 |
| drying=False | 384 | 382 | 0.545 | 0.092 | [0.00, 0.19] | 1.279 | 0.005 |
| uptrend=True | 217 | 216 | 0.616 | 0.173 | [0.07, 0.28] | 1.754 | 0.012 |
| uptrend=False | 309 | 308 | 0.490 | 0.037 | [-0.08, 0.15] | 1.092 | -0.002 |

Phase lengths found by detect() (bars):

| phase | mean | min | 50% | max |
|---|---|---|---|---|
| decline_len | 14.462 | 2.000 | 12 | 53 |
| slowdown_len | 9.625 | 0 | 7.000 | 53 |
| base_len | 2.639 | 2.000 | 2.000 | 6.000 |

## 4. Weekly signals per year

| year | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| 2016 | 41 | 0.732 | 0.384 | 15.752 | 0.033 |
| 2017 | 87 | 0.529 | 0.109 | 9.505 | 0.003 |
| 2018 | 65 | 0.492 | -0.096 | -6.265 | -0.016 |
| 2019 | 42 | 0.690 | 0.352 | 14.764 | 0.023 |
| 2020 | 17 | 0.529 | -0.018 | -0.312 | -0.028 |
| 2021 | 33 | 0.636 | 0.292 | 9.626 | 0.019 |
| 2022 | 12 | 0.250 | -0.452 | -5.425 | -0.009 |
| 2023 | 78 | 0.513 | -0.023 | -1.822 | -0.005 |
| 2024 | 43 | 0.488 | 0.132 | 5.694 | 0.008 |
| 2025 | 67 | 0.463 | -0.072 | -4.842 | -0.010 |
| 2026 | 41 | 0.564 | 0.314 | 12.995 | 0.025 |

## 5. Weekly signals per ticker (15 worst and 15 best by total_R)

| ticker | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| AIG | 5 | 0.200 | -0.798 | -3.992 | -0.054 |
| AOS | 3 | 0 | -1.045 | -3.136 | -0.145 |
| ROP | 2 | 0 | -1.416 | -2.832 | -0.123 |
| HSIC | 6 | 0.500 | -0.397 | -2.380 | -0.035 |
| SR | 2 | 0 | -1.070 | -2.139 | -0.070 |
| FBIN | 2 | 0 | -1.045 | -2.089 | -0.074 |
| AVY | 4 | 0.250 | -0.510 | -2.041 | -0.057 |
| NEE | 2 | 0 | -1.011 | -2.021 | -0.128 |
| MS | 2 | 0 | -1.009 | -2.019 | -0.091 |
| AFG | 2 | 0 | -1.004 | -2.008 | -0.032 |
| STT | 2 | 0 | -1.000 | -2.000 | -0.134 |
| TEL | 2 | 0 | -0.864 | -1.727 | -0.093 |
| XOM | 3 | 0 | -0.524 | -1.573 | -0.032 |
| SUI | 2 | 0 | -0.785 | -1.569 | -0.018 |
| ALLY | 1 | 0 | -1.564 | -1.564 | -0.123 |
| DTE | 2 | 1.000 | 1.147 | 2.294 | 0.046 |
| FTV | 2 | 1.000 | 1.177 | 2.353 | 0.058 |
| DUK | 2 | 1.000 | 1.199 | 2.397 | 0.062 |
| D | 3 | 0.667 | 0.806 | 2.417 | 0.042 |
| MRSH | 2 | 1.000 | 1.211 | 2.422 | 0.052 |
| MO | 2 | 1.000 | 1.305 | 2.611 | 0.024 |
| CL | 2 | 1.000 | 1.318 | 2.637 | 0.092 |
| CASY | 2 | 1.000 | 1.326 | 2.652 | 0.064 |
| CLH | 2 | 1.000 | 1.383 | 2.766 | 0.080 |
| KHC | 4 | 0.750 | 0.734 | 2.934 | 0.024 |
| ACI | 2 | 1.000 | 1.753 | 3.505 | 0.059 |
| AMGN | 2 | 1.000 | 2.000 | 4.000 | 0.128 |
| MRK | 2 | 1.000 | 2.014 | 4.029 | 0.100 |
| RPM | 3 | 1.000 | 1.436 | 4.309 | 0.073 |
| WM | 3 | 1.000 | 1.686 | 5.057 | 0.085 |
