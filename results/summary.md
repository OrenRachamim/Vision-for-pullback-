# Pullback scanner - backtest report (`pullback_scanner.py`)

* tickers: 30 / 30 | period: 2016-01-01 -> today
* entry: next open | stop: base_lo | target: 2.0R | max hold: 20 days | dedupe cooldown: 5 bars
* baseline = every trading day of the same tickers, same period (81,300 days)

## 1. Forward returns vs baseline (next open -> close t+h)

| group / horizon | n | mean | median | pct_up | t_vs_base | p |
|---|---|---|---|---|---|---|
| baseline 5d | 81,150 | 0.004 | 0.004 | 0.559 |  |  |
| daily 5d | 283 | 0.006 | 0.004 | 0.569 | 1.020 | 0.308 |
| weekly 5d | 28 | 0.001 | -0.002 | 0.429 | -0.790 | 0.429 |
| BUY SIGNAL (daily+weekly) 5d | 4.000 | -0.001 | -0.002 | 0.250 | -2.356 | 0.018 |
| baseline 10d | 81,000 | 0.009 | 0.008 | 0.578 |  |  |
| daily 10d | 283 | 0.008 | 0.009 | 0.601 | -0.412 | 0.680 |
| weekly 10d | 28 | 0.006 | 0.008 | 0.679 | -0.423 | 0.672 |
| BUY SIGNAL (daily+weekly) 10d | 4.000 | -0.004 | -0.005 | 0.500 | -1.042 | 0.297 |
| baseline 20d | 80,700 | 0.019 | 0.017 | 0.605 |  |  |
| daily 20d | 282 | 0.011 | 0.012 | 0.574 | -1.877 | 0.060 |
| weekly 20d | 27 | 0.020 | 0.017 | 0.704 | 0.071 | 0.944 |
| BUY SIGNAL (daily+weekly) 20d | 3.000 | -0.007 | -0.019 | 0.333 | -0.792 | 0.428 |
| baseline 60d | 79,500 | 0.059 | 0.048 | 0.662 |  |  |
| daily 60d | 279 | 0.036 | 0.036 | 0.645 | -3.087 | 0.002 |
| weekly 60d | 27 | 0.024 | 0.035 | 0.704 | -1.677 | 0.094 |
| BUY SIGNAL (daily+weekly) 60d | 3.000 | 0.078 | 0.062 | 0.667 | 0.317 | 0.751 |

> p is a normal-approx Welch test. Baseline days overlap, so treat p as optimistic.

## 2. Trade simulation with the scanner's own levels

| group | n | trades | win_rate | avg_R | R_ci95 | profit_factor | avg_risk_pct | stopped | hit_target | gap_below_stop | total_R |
|---|---|---|---|---|---|---|---|---|---|---|---|
| daily | 285 | 278 | 0.543 | 0.171 | [0.04, 0.29] | 1.463 | 0.059 | 0.295 | 0.126 | 0.014 | 48.456 |
| weekly | 28 | 27 | 0.704 | 0.278 | [0.01, 0.55] | 2.597 | 0.067 | 0.107 | 0 | 0 | 8.351 |
| BUY SIGNAL (daily+weekly) | 4 | 3 | 0.333 | -0.306 | [nan, nan] | 0.377 | 0.072 | 0.250 | 0 | 0 | -0.139 |
| CONTROL: random days, same exits | 27090 | 26969 | 0.515 | 0.172 | [0.16, 0.19] | 1.417 | 0.059 | 0.350 | 0.167 | 0 | 4692.360 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the tested signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* daily vs CONTROL: avg_R diff = -0.001R, t = -0.02, p = 0.987
* weekly vs CONTROL: avg_R diff = +0.106R, t = 0.75, p = 0.455
* BUY SIGNAL (daily+weekly) vs CONTROL: avg_R diff = -0.478R, t = -1.05, p = 0.295

## 3. Daily signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=25 | 26 | 23 | 0.565 | 0.113 | [-0.25, 0.47] | 1.344 | 0.004 |
| score=50 | 137 | 134 | 0.567 | 0.241 | [0.06, 0.43] | 1.725 | 0.014 |
| score=75 | 82 | 81 | 0.481 | 0.089 | [-0.15, 0.33] | 1.201 | 0.008 |
| score=100 | 40 | 40 | 0.575 | 0.139 | [-0.16, 0.46] | 1.368 | 0.010 |
| slowing=True | 124 | 123 | 0.520 | 0.155 | [-0.04, 0.36] | 1.382 | 0.012 |
| slowing=False | 161 | 155 | 0.561 | 0.184 | [0.03, 0.35] | 1.539 | 0.010 |
| drying=True | 71 | 70 | 0.529 | 0.029 | [-0.20, 0.26] | 1.068 | 0.005 |
| drying=False | 214 | 208 | 0.548 | 0.219 | [0.08, 0.36] | 1.626 | 0.013 |
| uptrend=True | 226 | 223 | 0.547 | 0.189 | [0.05, 0.33] | 1.520 | 0.011 |
| uptrend=False | 59 | 55 | 0.527 | 0.098 | [-0.17, 0.37] | 1.249 | 0.009 |

Phase lengths found by detect() (bars):

| phase | mean | min | 50% | max |
|---|---|---|---|---|
| decline_len | 15.421 | 2.000 | 13 | 41 |
| slowdown_len | 9.309 | 0 | 5.000 | 59 |
| base_len | 6.526 | 3.000 | 6.000 | 10 |
| peak_to_low | 20.625 | 5.000 | 18 | 40 |
| base_above_low | 0.009 | 0 | 0.003 | 0.030 |

## 4. Daily signals per year

| year | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| 2016 | 40 | 0.486 | -0.013 | -0.497 | -0.004 |
| 2017 | 36 | 0.694 | 0.415 | 14.958 | 0.027 |
| 2018 | 16 | 0.533 | -0.137 | -2.051 | -0.022 |
| 2019 | 21 | 0.429 | 0.009 | 0.194 | 0.001 |
| 2020 | 10 | 0.400 | -0.086 | -0.864 | 0.003 |
| 2021 | 31 | 0.581 | 0.316 | 9.800 | 0.016 |
| 2022 | 15 | 0.467 | 0.023 | 0.347 | -0.003 |
| 2023 | 35 | 0.629 | 0.221 | 7.723 | 0.019 |
| 2024 | 31 | 0.484 | 0.179 | 5.556 | 0.017 |
| 2025 | 32 | 0.531 | 0.123 | 3.950 | 0.017 |
| 2026 | 18 | 0.533 | 0.562 | 9.340 | 0.026 |

## 5. Daily signals per ticker

| ticker | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| CVX | 11 | 0.273 | -0.492 | -5.407 | -0.024 |
| MSFT | 11 | 0.273 | -0.430 | -4.731 | -0.040 |
| MA | 7 | 0.429 | -0.501 | -3.507 | -0.025 |
| V | 6 | 0.200 | -0.492 | -2.461 | 0.021 |
| ADBE | 8 | 0.375 | -0.269 | -2.156 | -0.002 |
| KO | 12 | 0.333 | -0.178 | -2.138 | -0.001 |
| NVDA | 2 | 0 | -0.551 | -1.101 | -0.156 |
| TSLA | 4 | 0.250 | -0.236 | -0.943 | 0.030 |
| XOM | 8 | 0.500 | -0.104 | -0.835 | 0.002 |
| CAT | 7 | 0.429 | -0.097 | -0.679 | -0.003 |
| DE | 15 | 0.533 | -0.015 | -0.220 | 0.002 |
| JPM | 7 | 0.571 | -0.020 | -0.137 | -0.005 |
| AMZN | 2 | 0.500 | 0.210 | 0.420 | 0.004 |
| AMD | 1 | 1.000 | 0.886 | 0.886 | 0.076 |
| CRM | 12 | 0.545 | 0.137 | 1.503 | 0.002 |
| JNJ | 14 | 0.500 | 0.149 | 2.085 | 0.009 |
| LMT | 8 | 0.750 | 0.341 | 2.726 | 0.001 |
| ORCL | 12 | 0.455 | 0.261 | 2.872 | 0.000 |
| NFLX | 15 | 0.600 | 0.206 | 3.086 | 0.017 |
| HD | 5 | 1.000 | 0.806 | 3.165 | 0.047 |
| PEP | 20 | 0.474 | 0.158 | 3.182 | 0.009 |
| WMT | 17 | 0.562 | 0.207 | 3.307 | 0.015 |
| AAPL | 9 | 0.667 | 0.398 | 3.578 | 0.045 |
| GOOGL | 5 | 0.800 | 0.831 | 4.154 | 0.099 |
| UNH | 12 | 0.583 | 0.368 | 4.420 | 0.013 |
| META | 3 | 1.000 | 1.709 | 5.128 | 0.060 |
| AVGO | 5 | 0.800 | 1.036 | 5.182 | 0.069 |
| PG | 14 | 0.786 | 0.507 | 7.095 | 0.024 |
| COST | 14 | 0.692 | 0.675 | 9.556 | 0.034 |
| LLY | 19 | 0.684 | 0.549 | 10.429 | 0.030 |
