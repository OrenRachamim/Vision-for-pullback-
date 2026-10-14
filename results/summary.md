# Pullback scanner - backtest report (`pullback_scanner.py`)

* tickers: 30 / 30 | period: 2016-01-01 -> today
* entry: next open | stop: base_lo | target: 2.0R | max hold: 20 days | dedupe cooldown: 5 bars
* baseline = every trading day of the same tickers, same period (81,300 days)

## 1. Forward returns vs baseline (next open -> close t+h)

| group / horizon | n | mean | median | pct_up | t_vs_base | p |
|---|---|---|---|---|---|---|
| baseline 5d | 81,150 | 0.004 | 0.004 | 0.559 |  |  |
| daily 5d | 302 | 0.006 | 0.003 | 0.546 | 0.972 | 0.331 |
| weekly 5d | 28 | 0.004 | 0.002 | 0.607 | -0.086 | 0.931 |
| BUY SIGNAL (daily+weekly) 5d | 3.000 | 0.002 | 0.003 | 0.667 | -1.029 | 0.304 |
| baseline 10d | 81,000 | 0.009 | 0.008 | 0.578 |  |  |
| daily 10d | 302 | 0.009 | 0.010 | 0.623 | -0.153 | 0.879 |
| weekly 10d | 28 | 0.006 | 0.003 | 0.607 | -0.447 | 0.655 |
| BUY SIGNAL (daily+weekly) 10d | 3.000 | -0.014 | -0.018 | 0.333 | -1.843 | 0.065 |
| baseline 20d | 80,700 | 0.019 | 0.017 | 0.605 |  |  |
| daily 20d | 299 | 0.012 | 0.013 | 0.572 | -1.655 | 0.098 |
| weekly 20d | 28 | 0.019 | 0.016 | 0.643 | 0.015 | 0.988 |
| BUY SIGNAL (daily+weekly) 20d | 3.000 | -0.004 | -0.011 | 0.333 | -0.716 | 0.474 |
| baseline 60d | 79,500 | 0.059 | 0.048 | 0.662 |  |  |
| daily 60d | 296 | 0.037 | 0.036 | 0.649 | -3.049 | 0.002 |
| weekly 60d | 28 | 0.030 | 0.044 | 0.714 | -1.414 | 0.157 |
| BUY SIGNAL (daily+weekly) 60d | 3.000 | 0.108 | 0.076 | 1.000 | 1.246 | 0.213 |

> p is a normal-approx Welch test. Baseline days overlap, so treat p as optimistic.

## 2. Trade simulation with the scanner's own levels

| group | n | trades | win_rate | avg_R | R_ci95 | profit_factor | avg_risk_pct | stopped | hit_target | gap_below_stop | total_R |
|---|---|---|---|---|---|---|---|---|---|---|---|
| daily | 304 | 295 | 0.542 | 0.196 | [0.08, 0.32] | 1.534 | 0.058 | 0.286 | 0.135 | 0.013 | 58.732 |
| weekly | 28 | 28 | 0.643 | 0.257 | [-0.04, 0.55] | 2.180 | 0.067 | 0.107 | 0.036 | 0 | 7.189 |
| BUY SIGNAL (daily+weekly) | 3 | 3 | 0.333 | -0.306 | [nan, nan] | 0.377 | 0.083 | 0.333 | 0 | 0 | -0.917 |
| CONTROL: random days, same exits | 27090 | 26974 | 0.515 | 0.175 | [0.16, 0.19] | 1.421 | 0.058 | 0.355 | 0.170 | 0 | 4769.851 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the tested signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* daily vs CONTROL: avg_R diff = +0.021R, t = 0.33, p = 0.744
* weekly vs CONTROL: avg_R diff = +0.082R, t = 0.52, p = 0.602
* BUY SIGNAL (daily+weekly) vs CONTROL: avg_R diff = -0.481R, t = -1.05, p = 0.292

## 3. Daily signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=25 | 37 | 34 | 0.441 | 0.052 | [-0.31, 0.42] | 1.112 | 0.005 |
| score=50 | 141 | 138 | 0.572 | 0.249 | [0.07, 0.43] | 1.765 | 0.013 |
| score=75 | 81 | 78 | 0.487 | 0.080 | [-0.15, 0.32] | 1.191 | 0.008 |
| score=100 | 45 | 45 | 0.622 | 0.341 | [0.02, 0.67] | 2.036 | 0.021 |
| slowing=True | 131 | 128 | 0.555 | 0.239 | [0.05, 0.43] | 1.668 | 0.019 |
| slowing=False | 173 | 167 | 0.533 | 0.162 | [0.00, 0.32] | 1.436 | 0.008 |
| drying=True | 69 | 67 | 0.597 | 0.212 | [-0.04, 0.47] | 1.579 | 0.011 |
| drying=False | 235 | 228 | 0.526 | 0.191 | [0.05, 0.33] | 1.521 | 0.013 |
| uptrend=True | 238 | 234 | 0.547 | 0.205 | [0.07, 0.35] | 1.571 | 0.012 |
| uptrend=False | 66 | 61 | 0.525 | 0.159 | [-0.10, 0.43] | 1.405 | 0.012 |

Phase lengths found by detect() (bars):

| phase | mean | min | 50% | max |
|---|---|---|---|---|
| decline_len | 22.707 | 2.000 | 17 | 116 |
| slowdown_len | 15.914 | 0 | 8.000 | 98 |
| base_len | 6.546 | 3.000 | 6.000 | 10 |
| peak_to_low | 34.612 | 5.000 | 23 | 120 |
| base_above_low | 0.009 | 0 | 0.004 | 0.030 |

## 4. Daily signals per year

| year | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| 2016 | 40 | 0.514 | 0.007 | 0.261 | -0.003 |
| 2017 | 38 | 0.684 | 0.441 | 16.752 | 0.027 |
| 2018 | 17 | 0.500 | -0.191 | -3.051 | -0.023 |
| 2019 | 24 | 0.458 | 0.051 | 1.235 | 0.005 |
| 2020 | 12 | 0.417 | 0.011 | 0.136 | 0.008 |
| 2021 | 30 | 0.567 | 0.274 | 8.233 | 0.011 |
| 2022 | 16 | 0.438 | -0.024 | -0.387 | -0.001 |
| 2023 | 38 | 0.605 | 0.285 | 10.842 | 0.021 |
| 2024 | 35 | 0.514 | 0.266 | 9.324 | 0.020 |
| 2025 | 33 | 0.515 | 0.170 | 5.621 | 0.021 |
| 2026 | 21 | 0.562 | 0.546 | 9.766 | 0.025 |

## 5. Daily signals per ticker

| ticker | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| CVX | 9 | 0.222 | -0.582 | -5.235 | -0.026 |
| MSFT | 11 | 0.273 | -0.424 | -4.660 | -0.043 |
| MA | 8 | 0.375 | -0.563 | -4.507 | -0.023 |
| KO | 14 | 0.357 | -0.177 | -2.479 | 0.002 |
| JNJ | 14 | 0.357 | -0.167 | -2.337 | -0.001 |
| ADBE | 8 | 0.375 | -0.269 | -2.156 | -0.002 |
| XOM | 9 | 0.444 | -0.162 | -1.462 | -0.001 |
| NVDA | 3 | 0 | -0.382 | -1.145 | -0.105 |
| TSLA | 4 | 0.250 | -0.236 | -0.943 | 0.030 |
| V | 7 | 0.333 | -0.077 | -0.461 | 0.027 |
| AMD | 1 | 1.000 | 0.886 | 0.886 | 0.076 |
| DE | 15 | 0.533 | 0.069 | 1.034 | 0.007 |
| WMT | 16 | 0.533 | 0.087 | 1.307 | 0.009 |
| CAT | 8 | 0.500 | 0.165 | 1.321 | 0.002 |
| AMZN | 4 | 0.667 | 0.388 | 1.343 | 0.016 |
| CRM | 12 | 0.545 | 0.137 | 1.503 | 0.002 |
| GOOGL | 4 | 0.750 | 0.551 | 2.203 | 0.081 |
| JPM | 10 | 0.700 | 0.242 | 2.415 | 0.009 |
| HD | 5 | 1.000 | 0.853 | 3.350 | 0.055 |
| LMT | 8 | 0.750 | 0.431 | 3.447 | 0.018 |
| AAPL | 9 | 0.667 | 0.398 | 3.578 | 0.043 |
| NFLX | 13 | 0.615 | 0.286 | 3.718 | 0.020 |
| META | 3 | 1.000 | 1.709 | 5.128 | 0.060 |
| ORCL | 14 | 0.538 | 0.455 | 5.912 | 0.011 |
| UNH | 14 | 0.571 | 0.426 | 5.967 | 0.018 |
| AVGO | 7 | 0.833 | 1.052 | 6.256 | 0.075 |
| PG | 17 | 0.706 | 0.416 | 7.074 | 0.020 |
| PEP | 23 | 0.545 | 0.381 | 8.564 | 0.017 |
| LLY | 20 | 0.650 | 0.478 | 9.554 | 0.026 |
| COST | 14 | 0.692 | 0.675 | 9.556 | 0.034 |
