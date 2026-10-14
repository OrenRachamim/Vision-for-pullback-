# Pullback scanner - backtest report (`pullback_scanner.py`)

* tickers: 847 / 898 | period: 2022-01-01 -> today
* entry: next open | stop: base_lo | target: 2.0R | max hold: 10 days | dedupe cooldown: 5 bars | combo: daily signal within 15 days after a weekly signal
* baseline = every trading day of the same tickers, same period (1,060,379 days)

## 1. Forward returns vs baseline (next open -> close t+h)

| group / horizon | n | mean | median | pct_up | t_vs_base | p |
|---|---|---|---|---|---|---|
| baseline 5d | 1,055,889 | 0.002 | 0.002 | 0.523 |  |  |
| daily 5d | 4,037 | 0.002 | 0.002 | 0.524 | -0.114 | 0.910 |
| weekly 5d | 323 | 0.002 | 0.002 | 0.533 | -0.191 | 0.848 |
| BUY SIGNAL (daily+weekly) 5d | 23 | 0.006 | 0.002 | 0.565 | 0.711 | 0.477 |
| combo 5d | 25 | 0.008 | 0.003 | 0.560 | 0.980 | 0.327 |
| baseline 10d | 1,051,399 | 0.005 | 0.004 | 0.529 |  |  |
| daily 10d | 4,015 | 0.004 | 0.003 | 0.526 | -1.344 | 0.179 |
| weekly 10d | 323 | 0.002 | 0.004 | 0.526 | -1.057 | 0.291 |
| BUY SIGNAL (daily+weekly) 10d | 23 | 0.021 | 0.024 | 0.783 | 1.880 | 0.060 |
| combo 10d | 25 | 0.022 | 0.027 | 0.720 | 1.992 | 0.046 |
| baseline 20d | 1,042,419 | 0.011 | 0.007 | 0.534 |  |  |
| daily 20d | 3,979 | 0.010 | 0.011 | 0.554 | -0.446 | 0.656 |
| weekly 20d | 321 | 0.005 | 0.003 | 0.517 | -1.730 | 0.084 |
| BUY SIGNAL (daily+weekly) 20d | 22 | 0.021 | 0.043 | 0.682 | 0.842 | 0.400 |
| combo 20d | 25 | 0.023 | 0.031 | 0.760 | 1.104 | 0.270 |
| baseline 60d | 1,006,499 | 0.036 | 0.023 | 0.566 |  |  |
| daily 60d | 3,899 | 0.030 | 0.027 | 0.594 | -2.891 | 0.004 |
| weekly 60d | 319 | 0.006 | 0.004 | 0.514 | -4.531 | 0.000 |
| BUY SIGNAL (daily+weekly) 60d | 22 | 0.047 | 0.041 | 0.682 | 0.458 | 0.647 |
| combo 60d | 24 | 0.035 | 0.069 | 0.750 | -0.045 | 0.964 |

> p is a normal-approx Welch test. Baseline days overlap, so treat p as optimistic.

## 2. Trade simulation with the scanner's own levels

| group | n | trades | win_rate | avg_R | R_ci95 | profit_factor | avg_risk_pct | stopped | hit_target | gap_below_stop | total_R |
|---|---|---|---|---|---|---|---|---|---|---|---|
| daily | 4064 | 3979 | 0.486 | 0.051 | [0.02, 0.08] | 1.134 | 0.058 | 0.280 | 0.091 | 0.010 | 213.769 |
| weekly | 325 | 323 | 0.517 | 0.017 | [-0.06, 0.10] | 1.058 | 0.066 | 0.191 | 0.015 | 0 | 6.346 |
| BUY SIGNAL (daily+weekly) | 23 | 23 | 0.783 | 0.222 | [-0.10, 0.53] | 2.043 | 0.070 | 0.174 | 0 | 0 | 5.103 |
| combo | 25 | 25 | 0.720 | 0.277 | [0.01, 0.56] | 2.510 | 0.070 | 0.080 | 0.040 | 0 | 6.932 |
| CONTROL: random days, same exits | 208290 | 207213 | 0.488 | 0.032 | [0.03, 0.04] | 1.091 | 0.070 | 0.261 | 0.074 | 0 | 6901.530 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the tested signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* daily vs CONTROL: avg_R diff = +0.019R, t = 1.17, p = 0.243
* weekly vs CONTROL: avg_R diff = -0.015R, t = -0.35, p = 0.724
* BUY SIGNAL (daily+weekly) vs CONTROL: avg_R diff = +0.190R, t = 1.22, p = 0.223
* combo vs CONTROL: avg_R diff = +0.245R, t = 1.64, p = 0.102

> require-uptrend: buy only when price > SMA200; CONTROL also samples only days with price > SMA200.

## 3. Combo signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=50 | 10 | 10 | 0.700 | 0.279 | [-0.25, 0.82] | 2.290 | 0.023 |
| score=75 | 13 | 13 | 0.769 | 0.306 | [-0.07, 0.63] | 2.941 | 0.024 |
| score=100 | 2 | 2 | 0.500 | 0.081 | [nan, nan] | 1.428 | 0.019 |
| slowing=True | 15 | 15 | 0.733 | 0.276 | [-0.04, 0.58] | 2.705 | 0.023 |
| slowing=False | 10 | 10 | 0.700 | 0.279 | [-0.25, 0.82] | 2.290 | 0.023 |
| drying=True | 2 | 2 | 0.500 | 0.081 | [nan, nan] | 1.428 | 0.019 |
| drying=False | 23 | 23 | 0.739 | 0.294 | [0.01, 0.61] | 2.607 | 0.024 |
| uptrend=True | 25 | 25 | 0.720 | 0.277 | [0.01, 0.56] | 2.510 | 0.023 |

Phase lengths found by detect() (bars):

| phase | mean | min | 50% | max |
|---|---|---|---|---|
| decline_len | 14.160 | 4.000 | 11 | 32 |
| slowdown_len | 18.360 | 0 | 16 | 49 |
| base_len | 7.160 | 3.000 | 8.000 | 10 |
| peak_to_low | 28 | 6.000 | 30 | 40 |
| base_above_low | 0.010 | 0 | 0.011 | 0.028 |

## 4. Combo signals per year

| year | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| 2023 | 9 | 0.778 | 0.180 | 1.622 | 0.016 |
| 2024 | 3 | 1.000 | 0.845 | 2.536 | 0.023 |
| 2025 | 6 | 0.833 | 0.715 | 4.287 | 0.032 |
| 2026 | 7 | 0.429 | -0.216 | -1.513 | 0.025 |

## 5. Combo signals per ticker

| ticker | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| SUI | 1 | 0 | -1.000 | -1.000 | 0.012 |
| XYL | 1 | 0 | -1.000 | -1.000 | -0.113 |
| ZTS | 1 | 0 | -0.700 | -0.700 | -0.016 |
| HII | 1 | 0 | -0.685 | -0.685 | -0.096 |
| FAST | 1 | 0 | -0.460 | -0.460 | 0.007 |
| DTE | 1 | 0 | -0.367 | -0.367 | 0.072 |
| TXRH | 1 | 1.000 | 0.008 | 0.008 | -0.050 |
| EXC | 2 | 0.500 | 0.048 | 0.096 | 0.068 |
| FTV | 1 | 1.000 | 0.129 | 0.129 | 0.076 |
| JNJ | 1 | 1.000 | 0.150 | 0.150 | 0.097 |
| ROST | 1 | 1.000 | 0.321 | 0.321 | 0.053 |
| MKC | 1 | 1.000 | 0.454 | 0.454 | 0.047 |
| POST | 1 | 1.000 | 0.483 | 0.483 | 0.031 |
| APH | 1 | 1.000 | 0.517 | 0.517 | 0.067 |
| ACI | 1 | 1.000 | 0.518 | 0.518 | 0.035 |
| JBL | 1 | 1.000 | 0.540 | 0.540 | -0.040 |
| EPR | 1 | 1.000 | 0.734 | 0.734 | 0.003 |
| VZ | 1 | 1.000 | 0.751 | 0.751 | 0.121 |
| COR | 1 | 1.000 | 0.785 | 0.785 | -0.005 |
| WM | 2 | 1.000 | 0.425 | 0.850 | 0.035 |
| KO | 1 | 1.000 | 1.251 | 1.251 | 0.010 |
| MO | 1 | 1.000 | 1.430 | 1.430 | 0.022 |
| AYI | 1 | 1.000 | 2.129 | 2.129 | 0.043 |
