# Pullback scanner - backtest report (`pullback_scanner.py`)

* tickers: 30 / 30 | period: 2016-01-01 -> today
* entry: next open | stop: base_lo | target: 2.0R | max hold: 20 days | dedupe cooldown: 5 bars
* baseline = every trading day of the same tickers, same period (81,300 days)

## 1. Forward returns vs baseline (next open -> close t+h)

| group / horizon | n | mean | median | pct_up | t_vs_base | p |
|---|---|---|---|---|---|---|
| baseline 5d | 81,150 | 0.004 | 0.004 | 0.559 |  |  |
| daily 5d | 240 | 0.004 | 0.001 | 0.517 | 0.052 | 0.959 |
| weekly 5d | 22 | 0.009 | 0.004 | 0.727 | 1.298 | 0.194 |
| BUY SIGNAL (daily+weekly) 5d | 3.000 | 0.002 | 0.003 | 0.667 | -1.029 | 0.304 |
| baseline 10d | 81,000 | 0.009 | 0.008 | 0.578 |  |  |
| daily 10d | 240 | 0.007 | 0.008 | 0.608 | -0.738 | 0.461 |
| weekly 10d | 22 | 0.014 | 0.012 | 0.636 | 0.701 | 0.483 |
| BUY SIGNAL (daily+weekly) 10d | 3.000 | -0.014 | -0.018 | 0.333 | -1.843 | 0.065 |
| baseline 20d | 80,700 | 0.019 | 0.017 | 0.605 |  |  |
| daily 20d | 238 | 0.011 | 0.012 | 0.563 | -1.936 | 0.053 |
| weekly 20d | 22 | 0.022 | 0.019 | 0.636 | 0.284 | 0.776 |
| BUY SIGNAL (daily+weekly) 20d | 3.000 | -0.004 | -0.011 | 0.333 | -0.716 | 0.474 |
| baseline 60d | 79,500 | 0.059 | 0.048 | 0.662 |  |  |
| daily 60d | 237 | 0.039 | 0.040 | 0.679 | -2.914 | 0.004 |
| weekly 60d | 22 | 0.044 | 0.044 | 0.773 | -0.791 | 0.429 |
| BUY SIGNAL (daily+weekly) 60d | 3.000 | 0.108 | 0.076 | 1.000 | 1.246 | 0.213 |

> p is a normal-approx Welch test. Baseline days overlap, so treat p as optimistic.

## 2. Trade simulation with the scanner's own levels

| group | n | trades | win_rate | avg_R | R_ci95 | profit_factor | avg_risk_pct | stopped | hit_target | gap_below_stop | total_R |
|---|---|---|---|---|---|---|---|---|---|---|---|
| daily | 242 | 234 | 0.521 | 0.162 | [0.02, 0.30] | 1.413 | 0.055 | 0.318 | 0.136 | 0.017 | 38.670 |
| weekly | 22 | 22 | 0.636 | 0.323 | [-0.02, 0.65] | 2.737 | 0.068 | 0.045 | 0.045 | 0.000 | 7.110 |
| BUY SIGNAL (daily+weekly) | 3 | 3 | 0.333 | -0.306 | [nan, nan] | 0.377 | 0.083 | 0.333 | 0.000 | 0.000 | -0.917 |
| CONTROL: random days, same exits | 27090 | 26972 | 0.508 | 0.170 | [0.16, 0.18] | 1.396 | 0.055 | 0.369 | 0.178 | 0.000 | 4635.005 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the daily signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* daily vs CONTROL: avg_R diff = -0.008R, t = -0.12, p = 0.908
* weekly vs CONTROL: avg_R diff = +0.153R, t = 0.87, p = 0.386
* BUY SIGNAL (daily+weekly) vs CONTROL: avg_R diff = -0.476R, t = -1.04, p = 0.297

## 3. Daily signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=25 | 34 | 31 | 0.419 | 0.041 | [-0.33, 0.46] | 1.086 | 0.012 |
| score=50 | 100 | 97 | 0.526 | 0.203 | [-0.01, 0.41] | 1.550 | 0.012 |
| score=75 | 65 | 63 | 0.492 | 0.050 | [-0.20, 0.32] | 1.116 | 0.007 |
| score=100 | 43 | 43 | 0.628 | 0.320 | [-0.00, 0.66] | 1.966 | 0.015 |
| slowing=True | 119 | 117 | 0.556 | 0.205 | [0.01, 0.41] | 1.555 | 0.016 |
| slowing=False | 123 | 117 | 0.487 | 0.119 | [-0.08, 0.32] | 1.286 | 0.006 |
| drying=True | 60 | 58 | 0.621 | 0.226 | [-0.05, 0.50] | 1.635 | 0.006 |
| drying=False | 182 | 176 | 0.489 | 0.140 | [-0.02, 0.31] | 1.348 | 0.013 |
| uptrend=True | 180 | 177 | 0.525 | 0.170 | [0.01, 0.34] | 1.439 | 0.010 |
| uptrend=False | 62 | 57 | 0.509 | 0.134 | [-0.14, 0.43] | 1.334 | 0.015 |

Phase lengths found by detect() (bars):

| phase | mean | min | 50% | max |
|---|---|---|---|---|
| decline_len | 26.471 | 2.000 | 21 | 116 |
| slowdown_len | 20.946 | 0.000 | 16 | 98 |
| base_len | 6.851 | 3.000 | 7.000 | 10 |
| peak_to_low | 40.740 | 5.000 | 30 | 120 |
| base_above_low | 0.010 | 0.000 | 0.008 | 0.029 |

## 4. Daily signals per year

| year | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| 2016 | 32 | 0.552 | 0.122 | 3.540 | 0.001 |
| 2017 | 39 | 0.641 | 0.335 | 13.065 | 0.027 |
| 2018 | 17 | 0.562 | -0.002 | -0.026 | -0.005 |
| 2019 | 15 | 0.267 | -0.379 | -5.683 | -0.018 |
| 2020 | 9 | 0.333 | -0.250 | -2.249 | -0.007 |
| 2021 | 19 | 0.526 | 0.229 | 4.350 | 0.006 |
| 2022 | 13 | 0.538 | 0.167 | 2.177 | 0.017 |
| 2023 | 31 | 0.548 | 0.219 | 6.778 | 0.018 |
| 2024 | 27 | 0.481 | 0.265 | 7.153 | 0.019 |
| 2025 | 25 | 0.480 | 0.107 | 2.678 | 0.009 |
| 2026 | 15 | 0.545 | 0.549 | 6.888 | 0.032 |

## 5. Daily signals per ticker

| ticker | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| MSFT | 8 | 0.125 | -0.562 | -4.500 | -0.053 |
| MA | 6 | 0.333 | -0.592 | -3.551 | -0.015 |
| JNJ | 15 | 0.333 | -0.222 | -3.337 | -0.006 |
| CVX | 9 | 0.333 | -0.314 | -2.822 | -0.015 |
| DE | 12 | 0.417 | -0.212 | -2.547 | -0.010 |
| XOM | 8 | 0.375 | -0.280 | -2.238 | -0.010 |
| TSLA | 2 | 0.000 | -1.000 | -2.000 | -0.073 |
| ADBE | 6 | 0.333 | -0.229 | -1.373 | -0.005 |
| NVDA | 1 | 0.000 | -0.044 | -0.044 | -0.003 |
| AMZN | 3 | 0.333 | 0.016 | 0.049 | -0.007 |
| KO | 13 | 0.385 | 0.019 | 0.243 | 0.005 |
| JPM | 5 | 0.600 | 0.064 | 0.320 | -0.008 |
| V | 6 | 0.400 | 0.108 | 0.539 | 0.034 |
| GOOGL | 2 | 0.500 | 0.286 | 0.572 | 0.078 |
| CAT | 6 | 0.500 | 0.126 | 0.756 | -0.002 |
| AMD | 1 | 1.000 | 0.886 | 0.886 | 0.076 |
| AVGO | 3 | 0.500 | 0.500 | 0.942 | 0.056 |
| META | 1 | 1.000 | 1.058 | 1.058 | 0.069 |
| NFLX | 9 | 0.667 | 0.156 | 1.404 | 0.032 |
| AAPL | 7 | 0.571 | 0.288 | 2.017 | 0.042 |
| WMT | 14 | 0.615 | 0.166 | 2.157 | 0.015 |
| CRM | 7 | 0.667 | 0.370 | 2.223 | 0.018 |
| HD | 5 | 1.000 | 0.853 | 3.350 | 0.055 |
| LMT | 8 | 0.750 | 0.436 | 3.488 | 0.017 |
| ORCL | 11 | 0.500 | 0.427 | 4.267 | 0.023 |
| UNH | 9 | 0.667 | 0.589 | 5.301 | 0.037 |
| PEP | 23 | 0.500 | 0.299 | 6.770 | 0.013 |
| LLY | 16 | 0.625 | 0.447 | 7.154 | 0.014 |
| PG | 16 | 0.750 | 0.505 | 8.074 | 0.022 |
| COST | 10 | 0.778 | 0.970 | 9.510 | 0.050 |
