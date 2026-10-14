# Pullback scanner - backtest report

* tickers: 30 / 30 | period: 2016-01-01 -> today
* entry: next open | stop: base_lo | target: 2.0R | max hold: 20 days | dedupe cooldown: 5 bars
* baseline = every trading day of the same tickers, same period (81,300 days)

## 1. Forward returns vs baseline (next open -> close t+h)

| group / horizon | n | mean | median | pct_up | t_vs_base | p |
|---|---|---|---|---|---|---|
| baseline 5d | 81,150 | 0.004 | 0.004 | 0.559 |  |  |
| daily 5d | 463 | 0.005 | 0.005 | 0.572 | 0.300 | 0.764 |
| weekly 5d | 14 | 0.005 | 0.006 | 0.571 | 0.096 | 0.923 |
| BUY SIGNAL (daily+weekly) 5d | 3.000 | 0.012 | 0.017 | 0.667 | 1.113 | 0.266 |
| baseline 10d | 81,000 | 0.009 | 0.008 | 0.578 |  |  |
| daily 10d | 463 | 0.009 | 0.012 | 0.622 | 0.070 | 0.944 |
| weekly 10d | 14 | 0.008 | 0.013 | 0.643 | -0.100 | 0.921 |
| BUY SIGNAL (daily+weekly) 10d | 3.000 | 0.008 | 0.022 | 0.667 | -0.033 | 0.974 |
| baseline 20d | 80,700 | 0.019 | 0.017 | 0.605 |  |  |
| daily 20d | 459 | 0.017 | 0.017 | 0.597 | -0.452 | 0.651 |
| weekly 20d | 14 | 0.004 | 0.010 | 0.571 | -1.561 | 0.118 |
| BUY SIGNAL (daily+weekly) 20d | 3.000 | 0.013 | 0.040 | 0.667 | -0.190 | 0.849 |
| baseline 60d | 79,500 | 0.059 | 0.048 | 0.662 |  |  |
| daily 60d | 451 | 0.047 | 0.039 | 0.659 | -1.741 | 0.082 |
| weekly 60d | 14 | 0.020 | 0.036 | 0.714 | -2.549 | 0.011 |
| BUY SIGNAL (daily+weekly) 60d | 3.000 | 0.047 | 0.061 | 1.000 | -0.848 | 0.396 |

> p is a normal-approx Welch test. Baseline days overlap, so treat p as optimistic.

## 2. Trade simulation with the scanner's own levels

| group | n | trades | win_rate | avg_R | R_ci95 | profit_factor | avg_risk_pct | stopped | hit_target | gap_below_stop | total_R |
|---|---|---|---|---|---|---|---|---|---|---|---|
| daily | 465 | 453 | 0.561 | 0.273 | [0.16, 0.38] | 1.752 | 0.064 | 0.297 | 0.174 | 0.015 | 124.666 |
| weekly | 14 | 14 | 0.571 | 0.140 | [-0.14, 0.45] | 1.810 | 0.070 | 0.000 | 0.000 | 0.000 | 1.954 |
| BUY SIGNAL (daily+weekly) | 3 | 3 | 0.667 | 0.402 | [nan, nan] | 3.562 | 0.077 | 0.000 | 0.000 | 0.000 | 1.207 |
| CONTROL: random days, same exits | 27090 | 26960 | 0.524 | 0.170 | [0.16, 0.18] | 1.433 | 0.064 | 0.328 | 0.152 | 0.000 | 4629.214 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the daily signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* daily vs CONTROL: avg_R diff = +0.103R, t = 1.90, p = 0.057
* weekly vs CONTROL: avg_R diff = -0.030R, t = -0.19, p = 0.851
* BUY SIGNAL (daily+weekly) vs CONTROL: avg_R diff = +0.232R, t = 0.51, p = 0.609

## 3. Daily signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=25 | 47 | 44 | 0.455 | 0.091 | [-0.24, 0.43] | 1.196 | -0.005 |
| score=50 | 187 | 181 | 0.586 | 0.340 | [0.19, 0.50] | 2.090 | 0.020 |
| score=75 | 167 | 166 | 0.536 | 0.196 | [0.02, 0.37] | 1.480 | 0.018 |
| score=100 | 64 | 62 | 0.629 | 0.414 | [0.11, 0.74] | 2.292 | 0.022 |
| slowing=True | 219 | 212 | 0.608 | 0.326 | [0.18, 0.47] | 1.994 | 0.020 |
| slowing=False | 246 | 241 | 0.519 | 0.227 | [0.08, 0.37] | 1.574 | 0.015 |
| drying=True | 136 | 134 | 0.545 | 0.252 | [0.04, 0.46] | 1.602 | 0.017 |
| drying=False | 329 | 319 | 0.567 | 0.282 | [0.17, 0.40] | 1.829 | 0.017 |
| uptrend=True | 358 | 353 | 0.564 | 0.285 | [0.17, 0.41] | 1.799 | 0.021 |
| uptrend=False | 107 | 100 | 0.550 | 0.230 | [0.01, 0.45] | 1.597 | 0.006 |

Phase lengths found by detect() (bars):

| phase | mean | min | 50% | max |
|---|---|---|---|---|
| decline_len | 18.647 | 2.000 | 20 | 35 |
| slowdown_len | 1.727 | 1.000 | 1.000 | 10 |
| base_len | 6.049 | 3.000 | 5.000 | 10 |

## 4. Daily signals per year

| year | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| 2016 | 48 | 0.533 | 0.084 | 3.766 | 0.010 |
| 2017 | 40 | 0.700 | 0.606 | 24.228 | 0.048 |
| 2018 | 32 | 0.452 | -0.135 | -4.170 | -0.020 |
| 2019 | 51 | 0.549 | 0.130 | 6.612 | 0.017 |
| 2020 | 34 | 0.412 | 0.136 | 4.607 | 0.021 |
| 2021 | 49 | 0.633 | 0.572 | 28.012 | 0.027 |
| 2022 | 31 | 0.500 | 0.086 | 2.593 | -0.003 |
| 2023 | 49 | 0.646 | 0.355 | 17.047 | 0.026 |
| 2024 | 55 | 0.574 | 0.376 | 20.324 | 0.029 |
| 2025 | 44 | 0.523 | 0.124 | 5.473 | 0.002 |
| 2026 | 32 | 0.556 | 0.561 | 16.172 | 0.015 |

## 5. Daily signals per ticker

| ticker | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| MSFT | 13 | 0.308 | -0.366 | -4.757 | -0.048 |
| DE | 21 | 0.476 | -0.070 | -1.477 | 0.001 |
| CVX | 14 | 0.429 | -0.105 | -1.467 | -0.006 |
| TSLA | 11 | 0.273 | -0.126 | -1.382 | -0.011 |
| AMZN | 14 | 0.385 | -0.110 | -1.256 | 0.011 |
| KO | 11 | 0.455 | -0.021 | -0.230 | 0.003 |
| MA | 9 | 0.667 | 0.072 | 0.647 | 0.004 |
| GOOGL | 10 | 0.500 | 0.160 | 1.604 | 0.030 |
| CAT | 16 | 0.438 | 0.118 | 1.895 | 0.004 |
| WMT | 16 | 0.533 | 0.129 | 1.935 | 0.011 |
| V | 8 | 0.429 | 0.286 | 2.001 | 0.039 |
| LMT | 10 | 0.600 | 0.324 | 3.242 | 0.009 |
| ADBE | 21 | 0.524 | 0.170 | 3.580 | 0.006 |
| XOM | 13 | 0.615 | 0.291 | 3.781 | 0.042 |
| JPM | 14 | 0.643 | 0.302 | 4.225 | 0.013 |
| UNH | 18 | 0.500 | 0.244 | 4.386 | -0.018 |
| NVDA | 16 | 0.500 | 0.280 | 4.476 | 0.021 |
| META | 7 | 0.571 | 0.691 | 4.835 | 0.037 |
| AVGO | 13 | 0.667 | 0.423 | 5.022 | 0.042 |
| HD | 7 | 1.000 | 0.961 | 5.707 | 0.065 |
| PEP | 21 | 0.500 | 0.277 | 5.718 | 0.015 |
| COST | 15 | 0.571 | 0.392 | 6.262 | 0.021 |
| JNJ | 20 | 0.600 | 0.314 | 6.288 | 0.014 |
| NFLX | 27 | 0.538 | 0.245 | 6.362 | 0.038 |
| AMD | 8 | 0.750 | 0.910 | 7.276 | 0.096 |
| PG | 18 | 0.722 | 0.486 | 8.746 | 0.023 |
| CRM | 23 | 0.667 | 0.495 | 10.394 | 0.011 |
| LLY | 28 | 0.630 | 0.430 | 11.598 | 0.026 |
| AAPL | 19 | 0.789 | 0.658 | 12.494 | 0.048 |
| ORCL | 24 | 0.609 | 0.555 | 12.761 | 0.021 |
