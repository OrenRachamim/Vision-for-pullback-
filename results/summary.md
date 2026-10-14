# Pullback scanner - backtest report (`pullback_scanner.py`)

* tickers: 30 / 30 | period: 2016-01-01 -> today
* entry: next open | stop: base_lo | target: 2.0R | max hold: 20 days | dedupe cooldown: 5 bars
* baseline = every trading day of the same tickers, same period (81,300 days)

## 1. Forward returns vs baseline (next open -> close t+h)

| group / horizon | n | mean | median | pct_up | t_vs_base | p |
|---|---|---|---|---|---|---|
| baseline 5d | 81,150 | 0.004 | 0.004 | 0.559 |  |  |
| daily 5d | 303 | 0.006 | 0.003 | 0.548 | 0.823 | 0.410 |
| weekly 5d | 28 | 0.004 | 0.002 | 0.607 | -0.086 | 0.931 |
| BUY SIGNAL (daily+weekly) 5d | 3.000 | 0.002 | 0.003 | 0.667 | -1.029 | 0.304 |
| baseline 10d | 81,000 | 0.009 | 0.008 | 0.578 |  |  |
| daily 10d | 303 | 0.009 | 0.010 | 0.624 | -0.212 | 0.832 |
| weekly 10d | 28 | 0.006 | 0.003 | 0.607 | -0.447 | 0.655 |
| BUY SIGNAL (daily+weekly) 10d | 3.000 | -0.014 | -0.018 | 0.333 | -1.843 | 0.065 |
| baseline 20d | 80,700 | 0.019 | 0.017 | 0.605 |  |  |
| daily 20d | 300 | 0.012 | 0.012 | 0.573 | -1.760 | 0.078 |
| weekly 20d | 28 | 0.019 | 0.016 | 0.643 | 0.015 | 0.988 |
| BUY SIGNAL (daily+weekly) 20d | 3.000 | -0.004 | -0.011 | 0.333 | -0.716 | 0.474 |
| baseline 60d | 79,500 | 0.059 | 0.048 | 0.662 |  |  |
| daily 60d | 297 | 0.038 | 0.036 | 0.653 | -2.889 | 0.004 |
| weekly 60d | 28 | 0.030 | 0.044 | 0.714 | -1.414 | 0.157 |
| BUY SIGNAL (daily+weekly) 60d | 3.000 | 0.108 | 0.076 | 1.000 | 1.246 | 0.213 |

> p is a normal-approx Welch test. Baseline days overlap, so treat p as optimistic.

## 2. Trade simulation with the scanner's own levels

| group | n | trades | win_rate | avg_R | R_ci95 | profit_factor | avg_risk_pct | stopped | hit_target | gap_below_stop | total_R |
|---|---|---|---|---|---|---|---|---|---|---|---|
| daily | 305 | 296 | 0.544 | 0.188 | [0.07, 0.31] | 1.513 | 0.058 | 0.289 | 0.131 | 0.013 | 56.575 |
| weekly | 28 | 28 | 0.643 | 0.257 | [-0.04, 0.55] | 2.180 | 0.067 | 0.107 | 0.036 | 0 | 7.189 |
| BUY SIGNAL (daily+weekly) | 3 | 3 | 0.333 | -0.306 | [nan, nan] | 0.377 | 0.083 | 0.333 | 0 | 0 | -0.917 |
| CONTROL: random days, same exits | 27090 | 26981 | 0.511 | 0.165 | [0.15, 0.18] | 1.394 | 0.059 | 0.359 | 0.169 | 0 | 4507.013 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the tested signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* daily vs CONTROL: avg_R diff = +0.022R, t = 0.36, p = 0.720
* weekly vs CONTROL: avg_R diff = +0.092R, t = 0.58, p = 0.559
* BUY SIGNAL (daily+weekly) vs CONTROL: avg_R diff = -0.471R, t = -1.03, p = 0.302

## 3. Daily signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=25 | 31 | 28 | 0.536 | 0.118 | [-0.24, 0.51] | 1.315 | 0.011 |
| score=50 | 147 | 143 | 0.587 | 0.292 | [0.12, 0.48] | 1.926 | 0.015 |
| score=75 | 84 | 82 | 0.439 | -0.023 | [-0.25, 0.20] | 0.950 | 0.003 |
| score=100 | 43 | 43 | 0.605 | 0.287 | [-0.03, 0.63] | 1.820 | 0.018 |
| slowing=True | 130 | 127 | 0.512 | 0.162 | [-0.03, 0.36] | 1.406 | 0.013 |
| slowing=False | 175 | 169 | 0.568 | 0.207 | [0.05, 0.36] | 1.606 | 0.011 |
| drying=True | 74 | 73 | 0.548 | 0.125 | [-0.11, 0.39] | 1.307 | 0.008 |
| drying=False | 231 | 223 | 0.543 | 0.208 | [0.06, 0.34] | 1.590 | 0.013 |
| uptrend=True | 240 | 236 | 0.547 | 0.192 | [0.06, 0.33] | 1.532 | 0.012 |
| uptrend=False | 65 | 60 | 0.533 | 0.172 | [-0.09, 0.46] | 1.443 | 0.013 |

Phase lengths found by detect() (bars):

| phase | mean | min | 50% | max |
|---|---|---|---|---|
| decline_len | 15.856 | 2.000 | 14 | 41 |
| slowdown_len | 9.279 | 0 | 5.000 | 59 |
| base_len | 6.518 | 3.000 | 6.000 | 10 |
| peak_to_low | 21.233 | 5.000 | 20 | 40 |
| base_above_low | 0.008 | 0 | 0.004 | 0.030 |

## 4. Daily signals per year

| year | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| 2016 | 40 | 0.514 | 0.007 | 0.261 | -0.003 |
| 2017 | 36 | 0.694 | 0.427 | 15.378 | 0.027 |
| 2018 | 17 | 0.500 | -0.191 | -3.051 | -0.023 |
| 2019 | 24 | 0.458 | 0.051 | 1.235 | 0.005 |
| 2020 | 13 | 0.385 | -0.066 | -0.864 | 0.006 |
| 2021 | 30 | 0.567 | 0.274 | 8.233 | 0.011 |
| 2022 | 16 | 0.438 | -0.024 | -0.387 | -0.001 |
| 2023 | 39 | 0.615 | 0.287 | 11.210 | 0.021 |
| 2024 | 36 | 0.528 | 0.265 | 9.528 | 0.020 |
| 2025 | 33 | 0.515 | 0.160 | 5.264 | 0.019 |
| 2026 | 21 | 0.562 | 0.546 | 9.766 | 0.025 |

## 5. Daily signals per ticker

| ticker | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| CVX | 10 | 0.300 | -0.503 | -5.031 | -0.023 |
| MSFT | 11 | 0.273 | -0.424 | -4.660 | -0.043 |
| MA | 8 | 0.375 | -0.563 | -4.507 | -0.023 |
| KO | 14 | 0.357 | -0.203 | -2.835 | -0.001 |
| JNJ | 14 | 0.357 | -0.167 | -2.337 | -0.001 |
| ADBE | 8 | 0.375 | -0.269 | -2.156 | -0.002 |
| NVDA | 3 | 0 | -0.382 | -1.145 | -0.105 |
| TSLA | 4 | 0.250 | -0.236 | -0.943 | 0.030 |
| XOM | 8 | 0.500 | -0.104 | -0.835 | 0.002 |
| V | 7 | 0.333 | -0.077 | -0.461 | 0.027 |
| AMD | 1 | 1.000 | 0.886 | 0.886 | 0.076 |
| DE | 15 | 0.533 | 0.069 | 1.034 | 0.007 |
| WMT | 16 | 0.533 | 0.087 | 1.307 | 0.009 |
| CAT | 8 | 0.500 | 0.165 | 1.321 | 0.002 |
| AMZN | 4 | 0.667 | 0.388 | 1.343 | 0.016 |
| CRM | 12 | 0.545 | 0.137 | 1.503 | 0.002 |
| GOOGL | 4 | 0.750 | 0.551 | 2.203 | 0.081 |
| JPM | 10 | 0.700 | 0.242 | 2.415 | 0.009 |
| NFLX | 15 | 0.600 | 0.206 | 3.086 | 0.017 |
| HD | 5 | 1.000 | 0.853 | 3.350 | 0.055 |
| LMT | 8 | 0.750 | 0.431 | 3.447 | 0.018 |
| AAPL | 9 | 0.667 | 0.398 | 3.578 | 0.043 |
| ORCL | 13 | 0.500 | 0.326 | 3.912 | 0.004 |
| META | 3 | 1.000 | 1.709 | 5.128 | 0.060 |
| UNH | 14 | 0.571 | 0.426 | 5.967 | 0.018 |
| AVGO | 7 | 0.833 | 1.052 | 6.256 | 0.075 |
| PG | 17 | 0.706 | 0.416 | 7.074 | 0.020 |
| PEP | 23 | 0.545 | 0.381 | 8.564 | 0.017 |
| LLY | 20 | 0.650 | 0.478 | 9.554 | 0.026 |
| COST | 14 | 0.692 | 0.675 | 9.556 | 0.034 |
